import tweepy
import json

# Set your API keys here  
API_KEY = 'shEiAheGtEhz2Pkezvi95d0j4'
API_SECRET_KEY = 'cQBKwde73D2HlH8oRXsmAQLu8H8tbq2EviQWCA8abeyoHZwCre'
ACCESS_TOKEN = '1439610266291953665-OQxQZvdDjERwW8ggAOSogYOLkm68Ru'
ACCESS_TOKEN_SECRET = '68ms3cxlMHb1tAGeQ1jfVbnNprBk1KlYjwcIfdfWziqqB'

# Authenticate to Twitter API
auth = tweepy.OAuth1UserHandler(
    API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
api = tweepy.API(auth)

def search_recent_tweets(username, tweet_count=5):
    try:
        # Search for recent tweets from the specified user
        tweets = api.user_timeline(screen_name=username, count=tweet_count, tweet_mode="extended")

        # Prepare tweet data for JSON
        tweet_data = []
        for tweet in tweets:
            tweet_data.append({
                'tweet_text': tweet.full_text,
                'created_at': tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'username': tweet.user.screen_name,
                'retweet_count': tweet.retweet_count
            })

        return tweet_data
    except tweepy.TweepyException as e:
        print(f"Error fetching tweets: {e}")
        return None

def write_to_json(data, filename='crawled_tweets.json'):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Successfully written tweets to {filename}")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")

def main():
    username = input("Enter the Twitter username: ")
    tweet_count = int(input("Enter the number of recent tweets to fetch: "))

    tweets = search_recent_tweets(username, tweet_count)

    if tweets:
        write_to_json(tweets)
    else:
        print(f"No tweets found for {username}.")

if __name__ == "__main__":
    main()