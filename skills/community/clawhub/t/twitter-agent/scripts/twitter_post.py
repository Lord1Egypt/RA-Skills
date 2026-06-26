#!/usr/bin/env python3
"""发布推文（支持纯文字或带图片）
用法:
  python3 twitter_post.py --text "推文内容"
  python3 twitter_post.py --text "推文内容" --image /path/to/image.png
"""
import argparse, json, os, sys
import tweepy

CONSUMER_KEY = os.environ["TW_CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["TW_CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["TW_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["TW_ACCESS_TOKEN_SECRET"]


def post_tweet(text: str, image_path: str = None):
    client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )

    media_id = None
    if image_path:
        auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api_v1 = tweepy.API(auth)
        media = api_v1.media_upload(filename=image_path)
        media_id = media.media_id

    kwargs = {"text": text}
    if media_id:
        kwargs["media_ids"] = [media_id]

    resp = client.create_tweet(**kwargs)
    tweet_id = resp.data["id"]

    me = client.get_me()
    username = me.data.username

    return {
        "success": True,
        "tweet_id": tweet_id,
        "url": f"https://x.com/{username}/status/{tweet_id}",
        "text": text,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--image", default=None)
    args = parser.parse_args()

    try:
        result = post_tweet(args.text, args.image)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)
