#!/usr/bin/env python3
"""
Facebook Importer — Analyzes Facebook data export for personality insights.
Facebook doesn't have a public scraping path like Twitter, so this works with
the user's data download (Settings → Your Information → Download Your Information).

Supports: JSON format export from Facebook (profile, posts, likes, friends).
"""
import os
import sys
import json
import glob
from datetime import datetime, timezone
from collections import Counter

IMPORT_DIR = "/tmp/soulsync"

def find_facebook_export():
    """Look for Facebook data export in common locations."""
    search_paths = [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace")),
    ]
    
    for base in search_paths:
        if not os.path.isdir(base):
            continue
        # Facebook exports are usually in a folder like facebook-username or facebook-data
        for pattern in ["facebook-*", "fb_data*", "your_facebook_data"]:
            matches = glob.glob(os.path.join(base, pattern))
            for match in matches:
                if os.path.isdir(match):
                    return match
        # Also check for zip extraction
        for d in os.listdir(base):
            full = os.path.join(base, d)
            if os.path.isdir(full) and os.path.exists(os.path.join(full, "profile_information")):
                return full
    
    return None

def read_fb_json(export_dir, *path_parts):
    """Read a JSON file from Facebook export structure."""
    filepath = os.path.join(export_dir, *path_parts)
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

def decode_fb_text(text):
    """Facebook exports encode text in latin-1 mojibake. Fix it."""
    if isinstance(text, str):
        try:
            return text.encode("latin-1").decode("utf-8")
        except (UnicodeDecodeError, UnicodeEncodeError):
            return text
    return text

def analyze_export(export_dir):
    """Analyze Facebook data export."""
    insights = {
        "interests": [],
        "personality_traits": [],
        "communication_style": "",
        "tone": "",
        "key_contacts": [],
    }
    items_processed = 0
    
    # Profile information
    profile = read_fb_json(export_dir, "profile_information", "profile_information.json")
    if profile:
        profile_data = profile.get("profile_v2", {})
        name = decode_fb_text(profile_data.get("name", {}).get("full_name", ""))
        bio = decode_fb_text(profile_data.get("intro_bio", ""))
        insights["profile"] = {"name": name, "bio": bio}
    
    # Page likes → interests
    likes = read_fb_json(export_dir, "likes_and_reactions", "pages.json")
    if likes:
        page_categories = Counter()
        page_names = []
        for page in likes.get("page_likes_v2", []):
            name = decode_fb_text(page.get("name", ""))
            if name:
                page_names.append(name)
            items_processed += 1
        insights["liked_pages"] = page_names[:30]
        insights["interests"].extend(page_names[:20])
    
    # Posts → communication style and tone
    posts = read_fb_json(export_dir, "posts", "your_posts_1.json")
    if posts:
        post_texts = []
        post_lengths = []
        questions = 0
        exclamations = 0
        links = 0
        photos = 0
        
        for post in posts[:200]:
            data = post.get("data", [{}])
            for d in data:
                text = decode_fb_text(d.get("post", ""))
                if text:
                    post_texts.append(text)
                    post_lengths.append(len(text))
                    if "?" in text:
                        questions += 1
                    if "!" in text:
                        exclamations += 1
                    if "http" in text:
                        links += 1
            
            attachments = post.get("attachments", [])
            for att in attachments:
                for ad in att.get("data", []):
                    if ad.get("media"):
                        photos += 1
            
            items_processed += 1
        
        total = max(len(post_texts), 1)
        avg_len = sum(post_lengths) / max(len(post_lengths), 1)
        
        tone_signals = []
        if exclamations / total > 0.3:
            tone_signals.append("enthusiastic")
        if questions / total > 0.2:
            tone_signals.append("inquisitive")
        if links / total > 0.3:
            tone_signals.append("shares resources")
        if photos / total > 0.5:
            tone_signals.append("visual communicator")
        
        if avg_len < 100:
            tone_signals.append("concise poster")
        elif avg_len > 300:
            tone_signals.append("writes longer-form posts")
        
        insights["tone"] = ", ".join(tone_signals) if tone_signals else "balanced"
        insights["communication_style"] = f"Avg post: {avg_len:.0f} chars. {photos} photos in {total} posts."
    
    # Friends → key contacts (just count, not names for privacy)
    friends = read_fb_json(export_dir, "friends_and_followers", "friends.json")
    if friends:
        friend_list = friends.get("friends_v2", [])
        insights["network_size"] = len(friend_list)
        # Only include first names for privacy
        insights["key_contacts"] = [
            decode_fb_text(f.get("name", "")).split()[0]
            for f in friend_list[:10]
            if f.get("name")
        ]
    
    # Groups → community interests
    groups = read_fb_json(export_dir, "groups", "your_group_membership_activity.json")
    if groups:
        group_names = []
        for group in groups.get("groups_joined_v2", []):
            name = decode_fb_text(group.get("name", ""))
            if name:
                group_names.append(name)
                insights["interests"].append(name)
        insights["groups"] = group_names[:15]
    
    return {
        "source": "facebook",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "insights": insights,
        "confidence": min(items_processed / 100, 1.0),
        "items_processed": items_processed,
    }

if __name__ == "__main__":
    os.makedirs(IMPORT_DIR, exist_ok=True)
    
    # Check for explicit path argument
    export_dir = None
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        export_dir = sys.argv[1]
    else:
        export_dir = find_facebook_export()
    
    if not export_dir:
        result = {
            "source": "facebook",
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "error": "No Facebook data export found.",
            "setup_help": (
                "To use this importer:\n"
                "1. Go to Facebook → Settings → Your Information → Download Your Information\n"
                "2. Select JSON format, Medium quality\n"
                "3. Download and extract to ~/Downloads/\n"
                "4. Run this importer again"
            ),
        }
    else:
        result = analyze_export(export_dir)
    
    output_path = os.path.join(IMPORT_DIR, "facebook.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print(json.dumps(result, indent=2))
