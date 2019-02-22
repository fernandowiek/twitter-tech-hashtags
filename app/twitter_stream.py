import json
import time
from datetime import datetime
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from elasticsearch import Elasticsearch
import pytz
import logging

# create instance of elasticsearch
es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
logging.getLogger("elasticsearch").setLevel(logging.CRITICAL)

HASHTAG_FILTER = [
    "openbanking", 
    "apifirst", 
    "devops", 
    "cloudfirst",
    "microservices",
    "apigateway",
    "oauth",
    "swagger",
    "raml",
    "openapis"
]

class TweetStreamListener(StreamListener):

    # on success
    def on_data(self, data):
        is_elasticsearch_available = False
        while not is_elasticsearch_available:
            try:
                es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
                if not es.ping():
                    print("Waiting for Elasticsearch...")
                    time.sleep(1)
                else:
                    is_elasticsearch_available = True
            except:
                time.sleep(1)
                pass

        # decode json
        tweet = json.loads(data)
 
        hashtags = [str(item['text']) for item in tweet["entities"]["hashtags"] if item['text'] in HASHTAG_FILTER]
        
        parsed_date = datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
        timestamp = parsed_date.replace(tzinfo = pytz.timezone('UTC'))

        tweet_hashtags = tweet['entities']['hashtags']
        hashtags = [
            item['text'].lower() \
            for item in tweet_hashtags \
                if item['text'].lower() in map(str.lower, HASHTAG_FILTER) \
        ]

        tweet_id = tweet['id_str']
        body = {
            "timestamp": timestamp,
            "id": tweet_id,
            "message": tweet["text"],
            "username": tweet["user"]["screen_name"],
            "followers": tweet["user"]["followers_count"],
            "hashtags": hashtags,
            "lang": tweet["lang"],
            "location": tweet["user"]["location"],
            "created_at": tweet["created_at"]
        }

        print(body)
        
        if len(hashtags) > 0:
            es.index(
                index="tweets", 
                doc_type='tweet',
                id=tweet_id, 
                body=body)

        return True

    # on failure
    def on_error(self, status):
        if status == 420:
            return False
        print(status)

if __name__ == '__main__':

    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # Load credentials from json file
    with open("twitter_credentials.json", "r") as file:  
        creds = json.load(file)
    auth = OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
    auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_TOKEN_SECRET'])

    # create instance of the tweepy stream
    stream = Stream(auth, listener)

    # search twitter for hashtags list
    stream.filter(track=HASHTAG_FILTER)