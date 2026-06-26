#!/usr/bin/env python3
"""Fetch top trending YouTube videos via YouTube Data API v3."""

import json
import os
import re
import sys
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timezone

API_KEY = os.environ.get("YOUTUBE_API_KEY", "")
REGION = sys.argv[1].upper() if len(sys.argv) > 1 else ""
COUNT = int(sys.argv[2]) if len(sys.argv) > 2 else 25
CATEGORY = sys.argv[3] if len(sys.argv) > 3 else ""

CATEGORY_NAMES = {
    "0": "All", "1": "Film & Animation", "2": "Autos & Vehicles",
    "10": "Music", "15": "Pets & Animals", "17": "Sports",
    "19": "Travel & Events", "20": "Gaming", "22": "People & Blogs",
    "23": "Comedy", "24": "Entertainment", "25": "News & Politics",
    "26": "Howto & Style", "27": "Education", "28": "Science & Technology",
    "29": "Nonprofits & Activism",
}

BASE_URL = "https://www.googleapis.com/youtube/v3/videos"


def format_count(n: int) -> str:
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.1f}B"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def format_duration(iso: str) -> str:
    """Convert ISO 8601 duration (PT1H2M3S) to HH:MM:SS or MM:SS."""
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso)
    if not m:
        return iso
    h, mn, s = (int(x or 0) for x in m.groups())
    if h:
        return f"{h}:{mn:02d}:{s:02d}"
    return f"{mn}:{s:02d}"


def fetch_trending(api_key: str) -> list[dict]:
    params: dict = {
        "part": "snippet,statistics,contentDetails",
        "chart": "mostPopular",
        "maxResults": min(COUNT, 50),
        "key": api_key,
    }
    if REGION:
        params["regionCode"] = REGION
    if CATEGORY:
        params["videoCategoryId"] = CATEGORY

    url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())["items"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            msg = json.loads(body)["error"]["message"]
        except Exception:
            msg = body[:200]
        print(f"API error {e.code}: {msg}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if not API_KEY:
        print("Error: YOUTUBE_API_KEY environment variable is not set.", file=sys.stderr)
        print("Get a free key at: https://console.cloud.google.com/", file=sys.stderr)
        print("Enable 'YouTube Data API v3', then create an API key.", file=sys.stderr)
        print("", file=sys.stderr)
        if sys.platform == "win32":
            print("  CMD:        set YOUTUBE_API_KEY=your_key", file=sys.stderr)
            print("  PowerShell: $env:YOUTUBE_API_KEY='your_key'", file=sys.stderr)
        else:
            print("  macOS/Linux: export YOUTUBE_API_KEY=your_key", file=sys.stderr)
        sys.exit(1)

    label = f"[{REGION}]" if REGION else "[Global]"
    cat_label = f" · {CATEGORY_NAMES.get(CATEGORY, f'cat:{CATEGORY}')}" if CATEGORY else ""
    print(f"▶  YouTube Trending — Top {COUNT}{cat_label}  {label}")
    print(f"   {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print("━" * 56)

    items = fetch_trending(API_KEY)
    if not items:
        print("No trending videos found.")
        sys.exit(0)

    for i, item in enumerate(items, 1):
        vid_id = item["id"]
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})
        details = item.get("contentDetails", {})

        title = snippet.get("title", "?")
        channel = snippet.get("channelTitle", "?")
        published = snippet.get("publishedAt", "")[:10]
        duration = format_duration(details.get("duration", ""))
        views = format_count(int(stats.get("viewCount", 0)))
        likes = format_count(int(stats.get("likeCount", 0))) if "likeCount" in stats else "N/A"
        comments = format_count(int(stats.get("commentCount", 0))) if "commentCount" in stats else "N/A"

        print(f"\n{i:>2}. {title}")
        print(f"    📺 {channel}  ·  🕒 {duration}  ·  📅 {published}")
        print(f"    👁  {views} views  ·  👍 {likes}  ·  💬 {comments}")
        print(f"    🔗 https://www.youtube.com/watch?v={vid_id}")

    print(f"\n{'─'*56}")
    print(f"Source: YouTube Data API v3  |  {label}  |  top {len(items)}")


if __name__ == "__main__":
    main()
