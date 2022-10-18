##
## NifiCheckTweetStatus.py
##
## The program is called from Nifi, DoesTweetDeleted (ExceuteStreamCommand Processor)
## The program checks if the tweet was deleted
##
## parameters:
##    1. Twitter's Customer key
##    2. Twitter's Customer secret
##    3. Twitter's Access Token
##    4. Twitter's Access  secret
##    5. Tweet ID
##
## Return values:
##      Y - Tweet was deleted
##      N - Tweet was not deleted

import sys
import tweepy as tw
#from tweepy import Stream
from tweepy import OAuthHandler


consumer_key = "{}".format(sys.argv[1])
consumer_secret = "{}".format(sys.argv[2])
access_token = "{}".format(sys.argv[3])
access_secret = "{}".format(sys.argv[4])
tweet_id = "{}".format(sys.argv[5])

# authenticate
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Check tweet status.
# api.statuses_lookup supported in old version of Python.
# In Python3 it should be changed to api.lookup_statuses
tweet_status = api.statuses_lookup([tweet_id])

if len(tweet_status) == 0:
    print ("Y")
else:
    print("N")