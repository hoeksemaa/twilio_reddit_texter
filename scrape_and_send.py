import argparse
import praw
from twilio.rest import Client

import twilio_auth
import reddit_auth
import contacts

def scrape_reddit(subreddit, reddit):
    hot_posts = reddit.subreddit(subreddit).hot(limit=10)
    for post in hot_posts:
        if post.url.endswith(".jpg") or post.url.endswith(".png"):
            return {"title": post.title, "image_url": post.url, "link": post.shortlink}

def send_twilio_text(message_block, from_number, to_number, client):
    message = client.messages \
            .create(
                body=message_block["title"] + '\n' + message_block["link"],
                media_url=message_block["image_url"],
                from_=from_number,
                to=to_number
            )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--subreddit", type=str, required=True, help="subreddit to scrape image from")
    parser.add_argument("-p", "--person", type=str, required=True, help="name of the person to send image to")
    args = vars(parser.parse_args())

    reddit = praw.Reddit(
            client_id=reddit_auth.creds["client_id"], 
            client_secret=reddit_auth.creds["client_secret"], 
            user_agent=reddit_auth.creds["user_agent"])
    message_block = scrape_reddit(
            args["subreddit"],
            reddit)
    client = Client(
            twilio_auth.creds["account_sid"], 
            twilio_auth.creds["auth_token"])
    send_twilio_text(
            message_block, 
            contacts.contacts["twilio"], 
            contacts.contacts[args["person"]], 
            client)

if __name__=='__main__':
    main()
