from TwitterAPI import TwitterAPI
import time
import pandas as pd
from pymongo import MongoClient
import pymongo


def main():
    twitter_api = TwitterAPI(consumer_key='AVENRyVYojZGeGChzHo68v0kA',
                             consumer_secret='KMWJdlaRidl4dvBjtT6x6NRwkik0wL7k27szWrUF4v1CXlCrGC',
                             access_token_key='14613563-MZqEZPbp8nTsx41n7knc0MXxSizwbWi3zgwKytOGy',
                             access_token_secret='qqdTpEixDeLdtTjtH8dun8lu85ZZj2KyVaxJzXeoUUnIO')

    filters = {"locations": "-73.9872354804, -33.7683777809, -34.7299934555, 5.2444863956"}

    tweet_stream = twitter_api.request('statuses/filter', filters).get_iterator()

    CONNECTION_STRING = "mongodb://localhost:27017/tweets"
    while True:
        client = MongoClient(CONNECTION_STRING)
        database = client['dados']
        tweets_collections = database["tweets"]
        for tweet in tweet_stream:
            try:
                ## Usando id do tweet para evitar tweets repetidos
                tweet['_id'] = tweet['id']
                del tweet['id']
                tweets_collections.insert_one(tweet)
            except Exception as ex:
                print(ex)

if __name__ == "__main__":
    main()
