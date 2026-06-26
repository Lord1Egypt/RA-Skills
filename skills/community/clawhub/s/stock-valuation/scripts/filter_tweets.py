#!/usr/bin/env python3
"""Filter tweets by engagement from stdin. Outputs JSON array to stdout."""
import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="Filter tweets by engagement metrics.")
    parser.add_argument("--min-likes", type=int, default=0, help="Minimum likes threshold (default: 0)")
    parser.add_argument("--min-retweets", type=int, default=0, help="Minimum retweets threshold (default: 0)")
    parser.add_argument("--min-engagement", type=int, default=0, help="Minimum total engagement (likes + retweets, default: 0)")
    parser.add_argument("--top", type=int, default=0, help="Return only top N tweets by engagement (0 = all)")
    args = parser.parse_args()

    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps([]))
        return

    try:
        tweets = json.loads(raw)
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON on stdin", file=sys.stderr)
        sys.exit(1)

    if not isinstance(tweets, list):
        tweets = [tweets]

    filtered = []
    for tweet in tweets:
        text = tweet.get("text", tweet.get("content", tweet.get("body", "")))
        author = tweet.get("author", tweet.get("user", tweet.get("username", "")))
        likes = int(tweet.get("likes", tweet.get("like_count", tweet.get("favorite_count", 0))))
        retweets = int(tweet.get("retweets", tweet.get("retweet_count", 0)))
        engagement = likes + retweets

        if likes < args.min_likes:
            continue
        if retweets < args.min_retweets:
            continue
        if engagement < args.min_engagement:
            continue

        filtered.append({
            "text": text,
            "author": author,
            "likes": likes,
            "retweets": retweets,
        })

    # Sort by total engagement descending
    filtered.sort(key=lambda t: t["likes"] + t["retweets"], reverse=True)

    if args.top > 0:
        filtered = filtered[:args.top]

    print(json.dumps(filtered, indent=2))


if __name__ == "__main__":
    main()
