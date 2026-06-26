#!/usr/bin/env python3
"""Quote Tweet
用法:
  python3 twitter_quote.py --tweet_id 1234567890 --text "评论内容"
"""
import argparse, json, os, sys
import tweepy

CONSUMER_KEY = os.environ["TW_CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["TW_CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["TW_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["TW_ACCESS_TOKEN_SECRET"]


def quote_tweet(tweet_id: str, text: str):
    client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )
    resp = client.create_tweet(text=text, quote_tweet_id=tweet_id)
    quote_id = resp.data["id"]

    me = client.get_me()
    username = me.data.username

    return {
        "success": True,
        "quote_id": quote_id,
        "url": f"https://x.com/{username}/status/{quote_id}",
        "quote_of": tweet_id,
        "text": text,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tweet_id", required=True)
    parser.add_argument("--text", required=True)
    args = parser.parse_args()

    try:
        result = quote_tweet(args.tweet_id, args.text)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)
