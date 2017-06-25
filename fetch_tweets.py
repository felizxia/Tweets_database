import tweepy
import sqlite3
from tweepy import OAuthHandler
import json

CONSUMER_KEY = 'kbm9lBjjsG4vzhvruZKSzriD1' 			# enter your consumer key
CONSUMER_SECRET = 'm4UF9oZcBEDLjpWFdiwNwDMFrFQnWjMTIW0bpGUwP8Qzn0GnEx' 		# enter your consumer secret
ACCESS_TOKEN = '778631251934769152-d1GudDjfHjwpXV6X827PmtAByZSihcr' 			# enter your access token
ACCESS_TOKEN_SECRET = 'VSXFLj5OHr5TkePouydWLcziG6cdlWT0H52SimPJogcfz' 	# enter your access token secret


# Authorization setup to access the Twitter API
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
reset = True

conn = sqlite3.connect('tweets.db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS Tweets")
cur.execute("DROP TABLE IF EXISTS Hashtags")
cur.execute("DROP TABLE IF EXISTS Connects")
t="CREATE TABLE IF NOT EXISTS "
t+="Tweets(tweet_id INTERGER, tweet_text TEXT, likes INTERGER)"
cur.execute(t)
h="CREATE TABLE IF NOT EXISTS "
h+= "Hashtags(hashtag_id INTERGER,hashtag_text TEXT, num_occurences INTERGER)"
cur.execute(h)
m="CREATE TABLE IF NOT EXISTS "
m+= "Connectmap(tweet_id INTERGER, hashtag_id INTERGER)"
cur.execute(m)

add_tweets="INSERT INTO Tweets VALUES(?,?,?)"
add_hashtags="INSERT INTO Hashtags VALUES(?,?,?)"
add_connect="INSERT INTO Connectmap VALUES(?,?)"
# Fetch Taylor Swift's 300 most recent tweets and save them to tweets.json
hash_num={}

page = 1
while page < 16:
	tweets = api.user_timeline('taylorswift13',page=page,count=20)
	if tweets:
		for tweet in tweets:
			json_tweet = tweet._json # convert to JSON format
			tweet_id=json_tweet["id"]
			tweet_text=json_tweet['text']
			tweet_likes=json_tweet['favorite_count']
			tweets_content= (tweet_id,tweet_text,tweet_likes)
			cur.execute(add_tweets, tweets_content)
			# tweetsinfo.append(tweets_content)
			hashid = json_tweet['entities']['user_mentions']
			for id in hashid:
				hashtag_id = id["id"]
				select = json_tweet['entities']['hashtags']
				if select == []:
					pass
				else:
					for text in select:
						hashtags = text['text']
						# text_hash.append(hashtags)
						if hashtags not in hash_num:
							hash_num[hashtags] = 1
						else:
							hash_num[hashtags] = hash_num[hashtags] + 1
				tweets_hashtags = (hashtag_id, hashtags, hash_num[hashtags])
				cur.execute(add_hashtags,tweets_hashtags)
				# hashtaginfo.append(tweets_hashtags)
				mapinfo = (tweet_id, hashtag_id)
				cur.execute(add_connect,mapinfo)
	else:
		break
	page += 1

conn.commit()
conn.close()



