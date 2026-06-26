#!/usr/bin/env python3
"""
Fetch YouTube comments from a video or channel's recent videos.
Uses YouTube Data API v3 (API key only, no OAuth needed for reading public comments).
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import HTTPError

API_KEY = os.environ.get("YOUTUBE_API_KEY")
BASE_URL = "https://www.googleapis.com/youtube/v3"
OUTPUT_DIR = "data/youtube-comment-moderator"


def api_get(endpoint, params):
    """Make a GET request to the YouTube API."""
    params["key"] = API_KEY
    url = f"{BASE_URL}/{endpoint}?{urlencode(params)}"
    req = Request(url, headers={"User-Agent": "YT-Moderator/1.0"})
    try:
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        body = e.read().decode()
        print(f"API error {e.code}: {body[:300]}", file=sys.stderr)
        return None


def get_channel_videos(channel_id, max_videos=10):
    """Get recent video IDs from a channel."""
    # First get the uploads playlist
    data = api_get("channels", {
        "part": "contentDetails",
        "id": channel_id
    })
    if not data or not data.get("items"):
        print(f"Channel {channel_id} not found", file=sys.stderr)
        return []
    
    uploads_playlist = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    
    # Get videos from uploads playlist
    videos = []
    page_token = None
    while len(videos) < max_videos:
        params = {
            "part": "snippet",
            "playlistId": uploads_playlist,
            "maxResults": min(50, max_videos - len(videos))
        }
        if page_token:
            params["pageToken"] = page_token
        
        data = api_get("playlistItems", params)
        if not data or not data.get("items"):
            break
        
        for item in data["items"]:
            videos.append({
                "video_id": item["snippet"]["resourceId"]["videoId"],
                "title": item["snippet"]["title"],
                "published_at": item["snippet"]["publishedAt"]
            })
        
        page_token = data.get("nextPageToken")
        if not page_token:
            break
    
    return videos[:max_videos]


def get_video_info(video_id):
    """Get video title and stats."""
    data = api_get("videos", {
        "part": "snippet,statistics",
        "id": video_id
    })
    if not data or not data.get("items"):
        return None
    item = data["items"][0]
    return {
        "video_id": video_id,
        "title": item["snippet"]["title"],
        "channel_title": item["snippet"]["channelTitle"],
        "comment_count": int(item["statistics"].get("commentCount", 0)),
        "view_count": int(item["statistics"].get("viewCount", 0))
    }


def get_comments(video_id, max_comments=100):
    """Fetch comment threads for a video."""
    comments = []
    page_token = None
    
    while len(comments) < max_comments:
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": min(100, max_comments - len(comments)),
            "order": "time",
            "textFormat": "plainText"
        }
        if page_token:
            params["pageToken"] = page_token
        
        data = api_get("commentThreads", params)
        if not data:
            break
        
        if "items" not in data:
            break
        
        for item in data["items"]:
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "comment_id": item["id"],
                "video_id": video_id,
                "author": snippet["authorDisplayName"],
                "author_channel_id": snippet.get("authorChannelId", {}).get("value", ""),
                "text": snippet["textDisplay"],
                "like_count": snippet["likeCount"],
                "published_at": snippet["publishedAt"],
                "updated_at": snippet["updatedAt"],
                "reply_count": item["snippet"]["totalReplyCount"]
            })
        
        page_token = data.get("nextPageToken")
        if not page_token:
            break
    
    return comments[:max_comments]


def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube comments")
    parser.add_argument("--video-id", help="Specific video ID to fetch comments from")
    parser.add_argument("--channel-id", help="Channel ID to fetch recent videos from")
    parser.add_argument("--max-videos", type=int, default=10, help="Max videos to check (channel mode)")
    parser.add_argument("--max-comments", type=int, default=100, help="Max comments per video")
    parser.add_argument("--output", default=None, help="Output file path")
    args = parser.parse_args()
    
    if not API_KEY:
        print("Error: YOUTUBE_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = args.output or os.path.join(OUTPUT_DIR, "comments-raw.json")
    
    all_comments = []
    
    if args.video_id:
        # Single video mode
        info = get_video_info(args.video_id)
        if info:
            print(f"Video: {info['title']} ({info['comment_count']} comments, {info['view_count']} views)")
        
        comments = get_comments(args.video_id, args.max_comments)
        all_comments.extend(comments)
        print(f"Fetched {len(comments)} comments from {args.video_id}")
    
    elif args.channel_id:
        # Channel mode
        videos = get_channel_videos(args.channel_id, args.max_videos)
        print(f"Found {len(videos)} videos from channel {args.channel_id}")
        
        for video in videos:
            comments = get_comments(video["video_id"], args.max_comments)
            all_comments.extend(comments)
            print(f"  {video['title'][:60]}... → {len(comments)} comments")
    
    else:
        print("Error: provide --video-id or --channel-id", file=sys.stderr)
        sys.exit(1)
    
    # Write output
    result = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_comments": len(all_comments),
        "comments": all_comments
    }
    
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\nTotal: {len(all_comments)} comments → {output_path}")


if __name__ == "__main__":
    main()
