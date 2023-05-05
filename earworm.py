import tweepy
import pymongo
import random
import time

# Twitter API credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create Tweepy API object
api = tweepy.API(auth)

# MongoDB credentials
mongo_username = "YOUR_MONGO_USERNAME"
mongo_password = "YOUR_MONGO_PASSWORD"
mongo_dbname = "YOUR_MONGO_DBNAME"

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://" + mongo_username + ":" + mongo_password + 
                             "@cluster0.mongodb.net/" + mongo_dbname + "?retryWrites=true&w=majority")

# Retrieve a random song lyric from MongoDB
db = client.lyrics_db
lyrics_collection = db.lyrics_collection
num_lyrics = lyrics_collection.count_documents({})

if num_lyrics > 0:
    random_index = random.randint(0, num_lyrics - 1)
    random_lyric = lyrics_collection.find().limit(-1).skip(random_index).next()["lyric"]
    
    # Post the lyric to Twitter
    api.update_status(random_lyric)
    
    # Wait for a day before posting another lyric
    time.sleep(86400)
