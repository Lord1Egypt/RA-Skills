#!/usr/bin/env python3
"""
Bulk post retrieval for TikTok, Instagram, X/Twitter, and YouTube.
Fetches recent content for an account and returns a normalized JSON array.

Usage:
    python3 fetch_posts.py --platform tiktok --username "khaby.lame" --count 20
    python3 fetch_posts.py --platform instagram --username "natgeo" --count 30
    python3 fetch_posts.py --platform twitter --username "elonmusk" --count 100
    python3 fetch_posts.py --platform youtube --channel-url "https://www.youtube.com/@MrBeast" --count 50
"""

import sys
import os
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apify_client import run_actor
from normalize import normalize_list


def fetch_tiktok_posts(username, count, sort="latest"):
    """Fetch a TikTok user's videos."""
    items = run_actor("tiktok", {
        "profiles": [username],
        "resultsPerPage": count,
        "profileScrapeSections": ["videos"],
        "profileSorting": sort,
    })
    return normalize_list("tiktok", "post", items)


def fetch_instagram_posts(username, count):
    """Fetch an Instagram user's posts."""
    items = run_actor("instagram", {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsType": "posts",
        "resultsLimit": count,
    })
    return normalize_list("instagram", "post", items)


def fetch_twitter_posts(username, count):
    """
    Fetch an X/Twitter user's tweets.
    Use tweet-scraper for 50 or more items because it is cheaper.
    Use twitter-scraper-lite for smaller batches because it has no minimum.
    """
    if count >= 50:
        actor_key = "twitter"
        input_data = {
            "twitterHandles": [username],
            "maxItems": count,
            "sort": "Latest",
        }
    else:
        actor_key = "twitter_unlimited"
        input_data = {
            "twitterHandles": [username],
            "maxItems": count,
            "sort": "Latest",
        }
    items = run_actor(actor_key, input_data)
    return normalize_list("twitter", "post", items)


def fetch_youtube_posts(channel_url, count, sort="NEWEST"):
    """Fetch videos from a YouTube channel."""
    items = run_actor("youtube", {
        "startUrls": [{"url": channel_url}],
        "maxResults": count,
        "maxResultsShorts": 0,
        "maxResultStreams": 0,
        "sortVideosBy": sort,
    })
    return normalize_list("youtube", "post", items)


def main():
    parser = argparse.ArgumentParser(description="Fetch social media posts in bulk")
    parser.add_argument("--platform", required=True, choices=["tiktok", "instagram", "twitter", "youtube"])
    parser.add_argument("--username", help="Username for TikTok, Instagram, or X/Twitter")
    parser.add_argument("--channel-url", help="YouTube channel URL")
    parser.add_argument("--count", type=int, default=20, help="Number of items to fetch (default: 20)")
    parser.add_argument("--sort", default=None, help="Sort mode (TikTok: latest/popular; YouTube: NEWEST/POPULAR)")
    args = parser.parse_args()

    if args.platform == "youtube":
        if not args.channel_url:
            print("Error: --channel-url is required for YouTube", file=sys.stderr)
            sys.exit(1)
        result = fetch_youtube_posts(args.channel_url, args.count, args.sort or "NEWEST")
    else:
        if not args.username:
            print(f"Error: --username is required for {args.platform}", file=sys.stderr)
            sys.exit(1)

        if args.platform == "tiktok":
            result = fetch_tiktok_posts(args.username, args.count, args.sort or "latest")
        elif args.platform == "instagram":
            result = fetch_instagram_posts(args.username, args.count)
        elif args.platform == "twitter":
            result = fetch_twitter_posts(args.username, args.count)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
