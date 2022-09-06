from TwitterAPI import TwitterAPI, TwitterOAuth
import time
import pandas as pd
from pymongo import MongoClient
import pymongo
import os

def main():
    o = TwitterOAuth.read_file(os.path.join('.', 'credentials.txt'))
    api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type='oAuth2', api_version='2')

    r = api.request('tweets/search/stream/rules', {'add':[{'value': 'Bolsonaro'}, 
                                                          {'value': 'Lula'},
                                                          {'value': 'Ciro'},
                                                          {'value': 'Tebet'},
                                                          {'value': 'Olavo'},
                                                          {'value': '7 de setembro'},
                                                          {'value': 'independência'}
                                                         ]})
    if r.status_code != 201:
        print(r)
        exit(-1)

    r = api.request('tweets/search/stream/rules', method_override='GET')
    print(f'[{r.status_code}] RULES: {r.text}')

    if r.status_code != 200:
        print(r)
        exit(-1)

    CONNECTION_STRING = "mongodb://localhost:27017/tweets"
    while True:
        client = MongoClient(CONNECTION_STRING)
        database = client['dados']
        tweets_collections = database["tweets"]
        r = api.request('tweets/search/stream', params={ 'tweet.fields': ['entities'], 
                                                         'user.fields': ['username'], 
                                                         'expansions': [] })
        print(f'[{r.status_code} START...')
        
        if r.status_code != 200:
            print(f'[{r.status_code}] RULES: {r.text}')
            exit(-1)
        for item in r:
            tweet = item['data']
            print(tweet)
            try:
                ## Usando id do tweet para evitar tweets repetidos
                tweet['_id'] = tweet['id']
                del tweet['id']
                tweets_collections.insert_one(tweet)
            except Exception as ex:
                print(ex)

if __name__ == "__main__":
    main()