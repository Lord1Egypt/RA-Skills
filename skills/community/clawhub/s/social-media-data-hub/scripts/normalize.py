#!/usr/bin/env python3
"""
Cross-platform normalization helpers.
Maps raw TikTok, Instagram, X/Twitter, and YouTube data into a unified schema.
"""

import sys
import json
import re
from datetime import datetime


def _parse_twitter_date(date_str):
    """Parse the X/Twitter date format: 'Fri Nov 24 17:49:36 +0000 2023'."""
    try:
        dt = datetime.strptime(date_str, "%a %b %d %H:%M:%S %z %Y")
        return dt.isoformat()
    except (ValueError, TypeError):
        return date_str


def _extract_hashtags_from_text(text):
    """Extract hashtags from free text."""
    if not text:
        return []
    return re.findall(r"#(\w+)", text)


# Post normalization

def normalize_tiktok_post(raw):
    """Normalize a TikTok post."""
    author = raw.get("authorMeta", {})
    return {
        "platform": "tiktok",
        "post_id": str(raw.get("id", "")),
        "post_url": raw.get("webVideoUrl", ""),
        "text": raw.get("text", ""),
        "created_at": raw.get("createTimeISO", ""),
        "author_name": author.get("name", ""),
        "author_display_name": author.get("nickName", ""),
        "likes": raw.get("diggCount", 0),
        "comments": raw.get("commentCount", 0),
        "shares": raw.get("shareCount", 0),
        "views": raw.get("playCount", 0),
        "saves": raw.get("collectCount", 0),
        "hashtags": [h.get("name", "") for h in raw.get("hashtags", [])],
        "media_type": "carousel" if raw.get("isSlideshow") else "video",
    }


def normalize_instagram_post(raw):
    """Normalize an Instagram post."""
    media_type = (raw.get("type", "Image") or "Image").lower()
    type_map = {"image": "image", "video": "video", "sidecar": "carousel"}
    return {
        "platform": "instagram",
        "post_id": raw.get("shortCode", raw.get("id", "")),
        "post_url": raw.get("url", ""),
        "text": raw.get("caption", ""),
        "created_at": raw.get("timestamp", ""),
        "author_name": raw.get("ownerUsername", ""),
        "author_display_name": raw.get("ownerFullName", ""),
        "likes": raw.get("likesCount", 0),
        "comments": raw.get("commentsCount", 0),
        "shares": None,
        "views": raw.get("videoViewCount", None),
        "saves": None,
        "hashtags": raw.get("hashtags", []) or _extract_hashtags_from_text(raw.get("caption", "")),
        "media_type": type_map.get(media_type, media_type),
    }


def normalize_twitter_post(raw):
    """Normalize an X/Twitter post."""
    author = raw.get("author", {})
    text = raw.get("text", "")
    return {
        "platform": "twitter",
        "post_id": str(raw.get("id", "")),
        "post_url": raw.get("url", ""),
        "text": text,
        "created_at": _parse_twitter_date(raw.get("createdAt", "")),
        "author_name": author.get("userName", ""),
        "author_display_name": author.get("name", ""),
        "likes": raw.get("likeCount", 0),
        "comments": raw.get("replyCount", 0),
        "shares": raw.get("retweetCount", 0),
        "views": None,
        "saves": raw.get("bookmarkCount", 0),
        "hashtags": _extract_hashtags_from_text(text),
        "media_type": "text",
    }


def normalize_youtube_post(raw):
    """Normalize a YouTube video."""
    return {
        "platform": "youtube",
        "post_id": raw.get("id", ""),
        "post_url": raw.get("url", ""),
        "text": raw.get("title", ""),
        "created_at": raw.get("date", ""),
        "author_name": raw.get("channelName", ""),
        "author_display_name": raw.get("channelName", ""),
        "likes": raw.get("likes", 0),
        "comments": raw.get("commentsCount", 0),
        "shares": None,
        "views": raw.get("viewCount", 0),
        "saves": None,
        "hashtags": _extract_hashtags_from_text(raw.get("text", "")),
        "media_type": "video",
    }


# Profile normalization

def normalize_tiktok_profile(raw):
    """Normalize a TikTok profile using author metadata from a post."""
    author = raw.get("authorMeta", raw)
    name = author.get("name", "")
    return {
        "platform": "tiktok",
        "username": name,
        "display_name": author.get("nickName", name),
        "bio": author.get("signature", ""),
        "followers": author.get("fans", 0),
        "following": author.get("following", 0),
        "posts_count": author.get("video", None),
        "profile_url": author.get("profileUrl", f"https://www.tiktok.com/@{name}"),
        "verified": author.get("verified", False),
    }


def normalize_instagram_profile(raw):
    """Normalize an Instagram profile."""
    return {
        "platform": "instagram",
        "username": raw.get("username", ""),
        "display_name": raw.get("fullName", ""),
        "bio": raw.get("biography", ""),
        "followers": raw.get("followersCount", 0),
        "following": raw.get("followsCount", 0),
        "posts_count": raw.get("postsCount", None),
        "profile_url": f"https://www.instagram.com/{raw.get('username', '')}/",
        "verified": raw.get("verified", False),
    }


def normalize_twitter_profile(raw):
    """Normalize an X/Twitter profile using the author object from a post."""
    author = raw.get("author", raw)
    username = author.get("userName", "")
    return {
        "platform": "twitter",
        "username": username,
        "display_name": author.get("name", ""),
        "bio": author.get("description", ""),
        "followers": author.get("followers", 0),
        "following": author.get("following", 0),
        "posts_count": None,
        "profile_url": f"https://x.com/{username}",
        "verified": author.get("isVerified", False) or author.get("isBlueVerified", False),
    }


def normalize_youtube_profile(raw):
    """Normalize a YouTube channel profile."""
    return {
        "platform": "youtube",
        "username": raw.get("channelName", ""),
        "display_name": raw.get("channelName", ""),
        "bio": raw.get("channelDescription", ""),
        "followers": raw.get("numberOfSubscribers", 0),
        "following": None,
        "posts_count": raw.get("channelTotalVideos", None),
        "profile_url": raw.get("channelUrl", ""),
        "verified": None,
    }


# Comment normalization

def normalize_tiktok_comment(raw):
    """Normalize a TikTok comment."""
    return {
        "platform": "tiktok",
        "comment_id": str(raw.get("cid", raw.get("id", ""))),
        "text": raw.get("text", ""),
        "author_name": raw.get("uniqueId", raw.get("nickName", "")),
        "likes": raw.get("diggCount", 0),
        "created_at": raw.get("createTimeISO", ""),
        "reply_count": raw.get("replyCommentTotal", 0),
    }


def normalize_instagram_comment(raw):
    """Normalize an Instagram comment."""
    return {
        "platform": "instagram",
        "comment_id": str(raw.get("id", "")),
        "text": raw.get("text", ""),
        "author_name": raw.get("ownerUsername", ""),
        "likes": raw.get("likesCount", 0),
        "created_at": raw.get("timestamp", ""),
        "reply_count": 0,
    }


def normalize_twitter_comment(raw):
    """Normalize an X/Twitter reply."""
    author = raw.get("author", {})
    return {
        "platform": "twitter",
        "comment_id": str(raw.get("id", "")),
        "text": raw.get("text", ""),
        "author_name": author.get("userName", ""),
        "likes": raw.get("likeCount", 0),
        "created_at": _parse_twitter_date(raw.get("createdAt", "")),
        "reply_count": raw.get("replyCount", 0),
    }


# Dispatch table

NORMALIZERS = {
    "post": {
        "tiktok": normalize_tiktok_post,
        "instagram": normalize_instagram_post,
        "twitter": normalize_twitter_post,
        "youtube": normalize_youtube_post,
    },
    "profile": {
        "tiktok": normalize_tiktok_profile,
        "instagram": normalize_instagram_profile,
        "twitter": normalize_twitter_profile,
        "youtube": normalize_youtube_profile,
    },
    "comment": {
        "tiktok": normalize_tiktok_comment,
        "instagram": normalize_instagram_comment,
        "twitter": normalize_twitter_comment,
    },
}


def normalize(platform, data_type, raw_data):
    """
    Normalize one raw object.

    Args:
        platform: tiktok / instagram / twitter / youtube
        data_type: post / profile / comment
        raw_data: raw JSON object as a dict

    Returns:
        dict: normalized output
    """
    normalizer = NORMALIZERS.get(data_type, {}).get(platform)
    if not normalizer:
        raise ValueError(f"No normalizer for {platform}/{data_type}")
    return normalizer(raw_data)


def normalize_list(platform, data_type, raw_list):
    """Normalize a list of raw objects."""
    return [normalize(platform, data_type, item) for item in raw_list]


# CLI entry point

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Normalize social media data into a shared schema")
    parser.add_argument("--platform", required=True, choices=["tiktok", "instagram", "twitter", "youtube"])
    parser.add_argument("--type", required=True, choices=["post", "profile", "comment"], dest="data_type")
    args = parser.parse_args()

    raw_input = sys.stdin.read().strip()
    if not raw_input:
        print("Error: No input data (pipe JSON via stdin)", file=sys.stderr)
        sys.exit(1)

    data = json.loads(raw_input)
    if isinstance(data, list):
        result = normalize_list(args.platform, args.data_type, data)
    else:
        result = normalize(args.platform, args.data_type, data)

    print(json.dumps(result, indent=2, ensure_ascii=False))
