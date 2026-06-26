#!/usr/bin/env python3
"""
Profile lookup for TikTok, Instagram, X/Twitter, and YouTube.
Outputs normalized profile JSON by default.

Usage:
    python3 fetch_profile.py --platform tiktok --username "khaby.lame"
    python3 fetch_profile.py --platform instagram --username "natgeo"
    python3 fetch_profile.py --platform twitter --username "elonmusk"
    python3 fetch_profile.py --platform youtube --channel-url "https://www.youtube.com/@MrBeast"
"""

import sys
import os
import json
import argparse

# Allow imports from the same directory even when invoked by absolute path.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apify_client import run_actor
from normalize import normalize


def fetch_tiktok_profile(username):
    """Fetch TikTok profile information from the author metadata on one video."""
    items = run_actor("tiktok", {
        "profiles": [username],
        "resultsPerPage": 1,
        "profileScrapeSections": ["videos"],
    })
    if not items:
        print(f"No data found for TikTok user: {username}", file=sys.stderr)
        sys.exit(1)
    return items[0]


def fetch_instagram_profile(username):
    """Fetch Instagram profile information via the details result type."""
    items = run_actor("instagram", {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsType": "details",
        "resultsLimit": 1,
    })
    if not items:
        print(f"No data found for Instagram user: {username}", file=sys.stderr)
        sys.exit(1)
    return items[0]


def fetch_twitter_profile(username):
    """
    Fetch X/Twitter profile information by retrieving one tweet and reading its author block.
    Uses twitter-scraper-lite because it has no minimum item requirement.
    """
    items = run_actor("twitter_unlimited", {
        "twitterHandles": [username],
        "maxItems": 1,
    })
    if not items:
        print(f"No data found for Twitter user: {username}", file=sys.stderr)
        sys.exit(1)
    return items[0]


def fetch_youtube_profile(channel_url):
    """Fetch YouTube channel information from a channel URL."""
    items = run_actor("youtube", {
        "startUrls": [{"url": channel_url}],
        "maxResults": 1,
        "maxResultsShorts": 0,
        "maxResultStreams": 0,
    })
    if not items:
        print(f"No data found for YouTube channel: {channel_url}", file=sys.stderr)
        sys.exit(1)
    return items[0]


def main():
    parser = argparse.ArgumentParser(description="Fetch social media profile information")
    parser.add_argument("--platform", required=True, choices=["tiktok", "instagram", "twitter", "youtube"])
    parser.add_argument("--username", help="Username for TikTok, Instagram, or X/Twitter")
    parser.add_argument("--channel-url", help="YouTube channel URL")
    parser.add_argument("--raw", action="store_true", help="Return raw actor output instead of normalized data")
    args = parser.parse_args()

    if args.platform == "youtube":
        if not args.channel_url:
            print("Error: --channel-url is required for YouTube", file=sys.stderr)
            sys.exit(1)
        raw_result = fetch_youtube_profile(args.channel_url)
    else:
        if not args.username:
            print(f"Error: --username is required for {args.platform}", file=sys.stderr)
            sys.exit(1)
        fetchers = {
            "tiktok": fetch_tiktok_profile,
            "instagram": fetch_instagram_profile,
            "twitter": fetch_twitter_profile,
        }
        raw_result = fetchers[args.platform](args.username)

    result = raw_result if args.raw else normalize(args.platform, "profile", raw_result)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
