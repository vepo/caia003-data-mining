import os
import pandas as pd
from pymongo import MongoClient
import pymongo
import csv

def main():
    CONNECTION_STRING = "mongodb://localhost:27017/tweets"
    client = MongoClient(CONNECTION_STRING)
    database = client['dados']
    tweets_collections = database["tweets"]
    cursor = tweets_collections.find({})
    with open('tweets.csv', 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "TEXT"])
        for document in cursor:
            writer.writerow([document['_id'], document['text'].replace('\n', '\\n').replace('\r', '')])

if __name__ == "__main__":
    main()