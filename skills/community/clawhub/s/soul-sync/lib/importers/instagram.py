#!/usr/bin/env python3
"""
Instagram Importer — Analyzes Instagram data export for personality insights.
Works with the JSON data download from Instagram (Settings → Your Activity → Download Your Information).

Also supports basic public profile scraping via web fetch as fallback.
"""
import os
import sys
import json
import glob
import re
from datetime import datetime, timezone
from collections import Counter

IMPORT_DIR = "/tmp/soulsync"

def find_instagram_export():
    """Look for Instagram data export in common locations."""
    search_paths = [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace")),
    ]
    
    for base in search_paths:
        if not os.path.isdir(base):
            continue
        for pattern in ["instagram-*", "ig_data*", "your_instagram_activity"]:
            matches = glob.glob(os.path.join(base, pattern))
            for match in matches:
                if os.path.isdir(match):
                    return match
        # Check for nested structure
        for d in os.listdir(base):
            full = os.path.join(base, d)
            if os.path.isdir(full):
                # Instagram exports have specific structure
                if any(os.path.exists(os.path.join(full, sub)) for sub in
                       ["personal_information", "content", "your_instagram_activity"]):
                    return full
    
    return None

def read_ig_json(export_dir, *path_parts):
    """Read a JSON file from Instagram export."""
    filepath = os.path.join(export_dir, *path_parts)
    if not os.path.exists(filepath):
        # Try alternate paths (Instagram export structure varies)
        alt_paths = [
            os.path.join(export_dir, "your_instagram_activity", *path_parts),
            os.path.join(export_dir, "instagram", *path_parts),
        ]
        for alt in alt_paths:
            if os.path.exists(alt):
                filepath = alt
                break
        else:
            return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

def decode_ig_text(text):
    """Instagram exports have the same mojibake issue as Facebook."""
    if isinstance(text, str):
        try:
            return text.encode("latin-1").decode("utf-8")
        except (UnicodeDecodeError, UnicodeEncodeError):
            return text
    return text

def analyze_export(export_dir):
    """Analyze Instagram data export."""
    insights = {
        "interests": [],
        "personality_traits": [],
        "communication_style": "",
        "tone": "",
        "key_contacts": [],
    }
    items_processed = 0
    
    # Profile info
    profile = read_ig_json(export_dir, "personal_information", "personal_information.json")
    if profile:
        pi = profile.get("profile_user", [{}])
        if isinstance(pi, list) and pi:
            pi = pi[0]
        string_data = pi.get("string_map_data", {})
        insights["profile"] = {
            "username": string_data.get("Username", {}).get("value", ""),
            "bio": decode_ig_text(string_data.get("Bio", {}).get("value", "")),
            "name": decode_ig_text(string_data.get("Name", {}).get("value", "")),
        }
    
    # Posts → captions → interests and tone
    posts = read_ig_json(export_dir, "content", "posts_1.json")
    if not posts:
        posts = read_ig_json(export_dir, "your_instagram_activity", "content", "posts_1.json")
    
    if posts:
        captions = []
        hashtags = Counter()
        mentions = Counter()
        post_hours = Counter()
        
        post_list = posts if isinstance(posts, list) else []
        
        for post in post_list[:300]:
            # Extract caption
            media_list = post.get("media", [])
            if isinstance(media_list, list):
                for media in media_list:
                    title = decode_ig_text(media.get("title", ""))
                    if title:
                        captions.append(title)
                        # Extract hashtags
                        for tag in re.findall(r'#(\w+)', title):
                            hashtags[tag.lower()] += 1
                        # Extract mentions
                        for mention in re.findall(r'@(\w+)', title):
                            mentions[mention.lower()] += 1
                    
                    # Track posting time
                    ts = media.get("creation_timestamp")
                    if ts:
                        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
                        post_hours[dt.hour] += 1
            
            items_processed += 1
        
        # Analyze captions
        total = max(len(captions), 1)
        avg_len = sum(len(c) for c in captions) / total if captions else 0
        emoji_count = sum(1 for c in captions for ch in c if ord(ch) > 0x1F000)
        questions = sum(1 for c in captions if "?" in c)
        
        tone_signals = []
        if emoji_count / total > 1:
            tone_signals.append("emoji-heavy communicator")
        if avg_len < 50:
            tone_signals.append("minimal captions — lets photos speak")
        elif avg_len > 200:
            tone_signals.append("storyteller — uses long captions")
        if questions / total > 0.15:
            tone_signals.append("engagement-focused — asks questions")
        
        insights["tone"] = ", ".join(tone_signals) if tone_signals else "visual-first communicator"
        insights["communication_style"] = f"Avg caption: {avg_len:.0f} chars across {len(captions)} posts"
        insights["hashtags"] = [f"#{h}" for h, _ in hashtags.most_common(15)]
        insights["interests"].extend([h for h, _ in hashtags.most_common(20)])
        insights["key_contacts"] = [f"@{m}" for m, _ in mentions.most_common(10)]
        
        # Peak posting times
        if post_hours:
            peak = [h for h, _ in post_hours.most_common(3)]
            insights["posting_pattern"] = f"Most active: {', '.join(f'{h}:00' for h in peak)}"
    
    # Liked posts → interests
    likes = read_ig_json(export_dir, "likes", "liked_posts.json")
    if likes:
        liked_accounts = Counter()
        like_list = likes.get("likes_media_likes", []) if isinstance(likes, dict) else likes
        for like in like_list[:200]:
            if isinstance(like, dict):
                sd = like.get("string_list_data", [{}])
                for item in sd:
                    href = item.get("href", "")
                    if href:
                        # Extract username from URL
                        match = re.search(r'instagram\.com/([^/]+)', href)
                        if match:
                            liked_accounts[match.group(1)] += 1
            items_processed += 1
        
        insights["frequently_liked"] = [a for a, _ in liked_accounts.most_common(10)]
    
    # Following → interests (who they chose to follow)
    following = read_ig_json(export_dir, "connections", "followers_and_following", "following.json")
    if not following:
        following = read_ig_json(export_dir, "followers_and_following", "following.json")
    
    if following:
        follow_list = following.get("relationships_following", [])
        insights["following_count"] = len(follow_list)
        # First 20 follows are usually the most important
        insights["key_follows"] = [
            decode_ig_text(f.get("string_list_data", [{}])[0].get("value", ""))
            for f in follow_list[:20]
            if f.get("string_list_data")
        ]
    
    # Followers count
    followers = read_ig_json(export_dir, "connections", "followers_and_following", "followers_1.json")
    if not followers:
        followers = read_ig_json(export_dir, "followers_and_following", "followers_1.json")
    if followers:
        insights["followers_count"] = len(followers) if isinstance(followers, list) else 0
    
    # Determine personality traits from content patterns
    traits = []
    if insights.get("following_count", 0) > 1000:
        traits.append("broad interests — follows many accounts")
    if items_processed > 200:
        traits.append("active content creator")
    if insights.get("hashtags"):
        traits.append("community-engaged — uses hashtags to connect")
    
    insights["personality_traits"] = traits
    
    return {
        "source": "instagram",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "insights": insights,
        "confidence": min(items_processed / 100, 1.0),
        "items_processed": items_processed,
    }

if __name__ == "__main__":
    os.makedirs(IMPORT_DIR, exist_ok=True)
    
    export_dir = None
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        export_dir = sys.argv[1]
    else:
        export_dir = find_instagram_export()
    
    if not export_dir:
        result = {
            "source": "instagram",
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "error": "No Instagram data export found.",
            "setup_help": (
                "To use this importer:\n"
                "1. Go to Instagram → Settings → Your Activity → Download Your Information\n"
                "2. Select 'All time', JSON format\n"
                "3. Request download, wait for email\n"
                "4. Download and extract to ~/Downloads/\n"
                "5. Run this importer again"
            ),
        }
    else:
        result = analyze_export(export_dir)
    
    output_path = os.path.join(IMPORT_DIR, "instagram.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print(json.dumps(result, indent=2))
