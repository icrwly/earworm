import tweepy
import pymongo
import random
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Twitter API credentials
consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create Tweepy API object
api = tweepy.API(auth)

# MongoDB credentials
mongo_uri = os.environ.get("MONGODB_URI")

# Connect to MongoDB
client = pymongo.MongoClient(mongo_uri)

# Retrieve a random song lyric from MongoDB
db = client.get_default_database()
lyrics_collection = db.lyrics_collection
num_lyrics = lyrics_collection.count_documents({})

if num_lyrics > 0:
    random_index = random.randint(0, num_lyrics - 1)
    random_lyric = lyrics_collection.find().limit(-1).skip(random_index).next()["lyric"]
    
    # Post the lyric to Twitter
    api.update_status(random_lyric)
    
    # Wait for a day before posting another lyric
    time.sleep(86400)