from apify_client import ApifyClient
import sys
import time
import csv

def main():
    try:
        # Initialize the ApifyClient with API token
        client = ApifyClient("apify_api_4hcn8uOCvOisvEQVyaE0aysSXfd3xb46c3Ck")
        
        # Get Twitter handles from terminal input (comma-separated)
        handles_input = input("Enter Twitter handles (comma-separated): ")
        handles = [handle.strip() for handle in handles_input.split(",")]

        # Get number of tweets to scrape per user
        tweets_desired = int(input("Enter the number of tweets to scrape per user: "))
        
        # Prepare the Actor input
        run_input = {
            "handles": handles,  # List of Twitter handles from input
            "tweetsDesired": tweets_desired,  # Number of tweets per user
            "addUserInfo": True,  # Whether to add user info in the output
            "startUrls": [],  # Optional: You can add specific start URLs if needed
            "proxyConfig": {"useApifyProxy": True},  # Use Apify proxy
        }

        # Run the Actor and wait for it to finish
        run = client.actor("u6ppkMWAx2E2MpEuF").call(run_input=run_input)
        print(f"Actor started, run ID: {run['id']}")

        # Poll the actor run status until it completes
        while run['status'] not in ['SUCCEEDED', 'FAILED', 'TIMED_OUT']:
            time.sleep(5) 
            run = client.actor("u6ppkMWAx2E2MpEuF").get_run(run['id'])
            print(f"Current status: {run['status']}")

# Fetch and print Actor results from the run's dataset to inspect structure
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
           print(item)  

        if run['status'] == 'SUCCEEDED':
            print("Scraping complete, fetching results...")       

            # Prepare CSV file for output
            with open('tweets_pulling.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Username", "Tweet Text", "Tweet Date", "Likes", "Retweets"]) 

                # Fetch and write Actor results from the run's dataset to the CSV
                for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                    username = item['user']['screen_name']
                    tweet_text = item['text']
                    tweet_date = item['created_at']
                    likes = item['favorite_count']
                    retweets = item['retweet_count']

                    # Write each tweet to the CSV file
                    writer.writerow([username, tweet_text, tweet_date, likes, retweets])

            print("Tweets have been written to 'scraped_tweets.csv'.")
        else:
            print(f"Actor run failed with status: {run['status']}")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
