#!/usr/bin/env python3
"""
Comment retrieval for TikTok, Instagram, and X/Twitter.
Use a dedicated YouTube comments actor for YouTube.

Usage:
    python3 fetch_comments.py --url "https://www.tiktok.com/@user/video/123456" --count 50
    python3 fetch_comments.py --url "https://www.instagram.com/p/ABC123/" --count 30
    python3 fetch_comments.py --url "https://x.com/user/status/123456" --count 100
"""

import sys
import os
import json
import re
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apify_client import run_actor
from normalize import normalize_list


def detect_platform(url):
    """Detect the platform from a content URL."""
    url_lower = url.lower()
    if "tiktok.com" in url_lower:
        return "tiktok"
    elif "instagram.com" in url_lower:
        return "instagram"
    elif "twitter.com" in url_lower or "x.com" in url_lower:
        return "twitter"
    elif "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    return None


def extract_twitter_status_id(url):
    """Extract the status ID from an X/Twitter URL."""
    match = re.search(r"/status/(\d+)", url)
    return match.group(1) if match else None


def fetch_tiktok_comments(url, count):
    """
    Fetch TikTok video comments.
    Comments are requested as part of the post fetch via commentsPerPost.
    """
    items = run_actor("tiktok", {
        "postURLs": [url],
        "commentsPerPost": count,
    })
    # TikTok may return comments nested inside the post payload.
    comments = []
    for item in items:
        if "comments" in item and isinstance(item["comments"], list):
            comments.extend(item["comments"])
        # Some runs emit comments as standalone items.
        elif item.get("type") == "comment" or "cid" in item:
            comments.append(item)

    if not comments:
        # Fallback if comments were emitted as standalone dataset items.
        comments = [item for item in items if "text" in item and "cid" in item]

    return normalize_list("tiktok", "comment", comments[:count])


def fetch_instagram_comments(url, count):
    """Fetch Instagram post comments, capped at 50 comments per post."""
    effective_count = min(count, 50)
    items = run_actor("instagram", {
        "directUrls": [url],
        "resultsType": "comments",
        "resultsLimit": effective_count,
    })
    if count > 50:
        print("Warning: Instagram comments limited to 50 per post", file=sys.stderr)
    return normalize_list("instagram", "comment", items)


def fetch_twitter_comments(url, count):
    """
    Fetch X/Twitter replies from a post conversation.
    Uses twitter-scraper-lite with a conversation_id search.
    """
    status_id = extract_twitter_status_id(url)
    if not status_id:
        print(f"Error: Cannot extract status ID from URL: {url}", file=sys.stderr)
        sys.exit(1)

    items = run_actor("twitter_unlimited", {
        "searchTerms": [f"conversation_id:{status_id}"],
        "maxItems": count,
        "sort": "Latest",
    })
    # Filter out the source post and keep replies only.
    replies = [item for item in items if item.get("isReply", False) or str(item.get("id", "")) != status_id]
    return normalize_list("twitter", "comment", replies[:count])


def main():
    parser = argparse.ArgumentParser(description="Fetch comments for a supported social media post")
    parser.add_argument("--url", required=True, help="Post or video URL")
    parser.add_argument("--count", type=int, default=30, help="Number of comments to fetch (default: 30)")
    parser.add_argument("--platform", choices=["tiktok", "instagram", "twitter"],
                        help="Explicit platform override (default: auto-detect)")
    args = parser.parse_args()

    platform = args.platform or detect_platform(args.url)
    if not platform:
        print(f"Error: Cannot detect platform from URL: {args.url}", file=sys.stderr)
        sys.exit(1)

    if platform == "youtube":
        print("Error: YouTube comments require a dedicated Actor (YouTube Comments Scraper).", file=sys.stderr)
        print("This script does not support YouTube comments.", file=sys.stderr)
        sys.exit(1)

    fetchers = {
        "tiktok": fetch_tiktok_comments,
        "instagram": fetch_instagram_comments,
        "twitter": fetch_twitter_comments,
    }

    result = fetchers[platform](args.url, args.count)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
