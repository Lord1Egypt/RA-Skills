#!/usr/bin/env python3
"""
Single-post lookup with automatic platform detection.
Returns normalized post details for a supported URL.

Usage:
    python3 fetch_single_post.py --url "https://www.tiktok.com/@user/video/123456"
    python3 fetch_single_post.py --url "https://www.instagram.com/p/ABC123/"
    python3 fetch_single_post.py --url "https://x.com/user/status/123456"
    python3 fetch_single_post.py --url "https://www.youtube.com/watch?v=ABC123"
"""

import sys
import os
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apify_client import run_actor
from normalize import normalize


def detect_platform(url):
    """Detect the platform from a post URL."""
    url_lower = url.lower()
    if "tiktok.com" in url_lower:
        return "tiktok"
    elif "instagram.com" in url_lower:
        return "instagram"
    elif "twitter.com" in url_lower or "x.com" in url_lower:
        return "twitter"
    elif "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    else:
        return None


def fetch_tiktok_single(url):
    """Fetch details for a single TikTok video."""
    items = run_actor("tiktok", {
        "postURLs": [url],
    })
    if not items:
        print(f"No data found for TikTok URL: {url}", file=sys.stderr)
        sys.exit(1)
    return items[0]


def fetch_instagram_single(url):
    """Fetch details for a single Instagram post."""
    items = run_actor("instagram", {
        "directUrls": [url],
        "resultsType": "posts",
        "resultsLimit": 1,
    })
    if not items:
        print(f"No data found for Instagram URL: {url}", file=sys.stderr)
        sys.exit(1)
    return items[0]


def fetch_twitter_single(url):
    """
    Fetch details for a single X/Twitter post.
    Uses twitter-scraper-lite because the V2 actor is not designed for single-item retrieval.
    """
    items = run_actor("twitter_unlimited", {
        "startUrls": [{"url": url}],
        "maxItems": 1,
    })
    if not items:
        print(f"No data found for Twitter URL: {url}", file=sys.stderr)
        sys.exit(1)
    return items[0]


def fetch_youtube_single(url):
    """Fetch details for a single YouTube video."""
    items = run_actor("youtube", {
        "startUrls": [{"url": url}],
        "maxResults": 1,
        "maxResultsShorts": 0,
        "maxResultStreams": 0,
    })
    if not items:
        print(f"No data found for YouTube URL: {url}", file=sys.stderr)
        sys.exit(1)
    return items[0]


def main():
    parser = argparse.ArgumentParser(description="Fetch one social media post by URL")
    parser.add_argument("--url", required=True, help="Post or video URL")
    parser.add_argument("--platform", choices=["tiktok", "instagram", "twitter", "youtube"],
                        help="Explicit platform override (default: auto-detect)")
    parser.add_argument("--raw", action="store_true", help="Return raw actor output instead of normalized data")
    args = parser.parse_args()

    platform = args.platform or detect_platform(args.url)
    if not platform:
        print(f"Error: Cannot detect platform from URL: {args.url}", file=sys.stderr)
        print("Please specify --platform explicitly.", file=sys.stderr)
        sys.exit(1)

    fetchers = {
        "tiktok": fetch_tiktok_single,
        "instagram": fetch_instagram_single,
        "twitter": fetch_twitter_single,
        "youtube": fetch_youtube_single,
    }

    raw_result = fetchers[platform](args.url)
    result = raw_result if args.raw else normalize(platform, "post", raw_result)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
