import tweepy
# Autenticantion
consumer_key = 'H6lZ8EfhIOrNdgpzvhBmht409'
consumer_secret = 'IAiIkAVla1X9Hzxdgpei8ksvQ8vv5aeptdBFpCXCGw1dSw5AJS'
access_token = '285203034-WTJiYqfS9L9RRZWidOVziz9JPb3zOia0oeRdr7In'
access_token_secret = '2L2wnxsFizrSqCnO72dijiLAjgifcy5fguMsUTzLDe08n'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

