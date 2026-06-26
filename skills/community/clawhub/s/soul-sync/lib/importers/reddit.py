#!/usr/bin/env python3
"""
Reddit Importer — Analyzes public Reddit profile for true interests and opinions.
Reddit is gold for personalization — people are more honest on Reddit than anywhere else.
Uses old.reddit.com JSON endpoints (no API key needed for public profiles).
"""
import os
import sys
import json
import urllib.request
import time
from datetime import datetime, timezone
from collections import Counter

IMPORT_DIR = "/tmp/soulsync"

def fetch_json(url):
    """Fetch JSON from Reddit."""
    req = urllib.request.Request(url, headers={
        "User-Agent": "OpenClaw-Soulsync/1.0 (personalization skill)"
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception:
        return None

def get_user_posts(username, limit=100):
    """Fetch user's recent posts and comments."""
    posts = []
    comments = []
    
    # Submissions
    data = fetch_json(f"https://www.reddit.com/user/{username}/submitted.json?limit={limit}&sort=new")
    if data and "data" in data:
        for child in data["data"].get("children", []):
            post = child.get("data", {})
            posts.append({
                "title": post.get("title", ""),
                "subreddit": post.get("subreddit", ""),
                "score": post.get("score", 0),
                "text": post.get("selftext", "")[:500],
                "created": post.get("created_utc", 0),
            })
    
    time.sleep(1)  # Rate limit respect
    
    # Comments
    data = fetch_json(f"https://www.reddit.com/user/{username}/comments.json?limit={limit}&sort=new")
    if data and "data" in data:
        for child in data["data"].get("children", []):
            comment = child.get("data", {})
            comments.append({
                "body": comment.get("body", "")[:500],
                "subreddit": comment.get("subreddit", ""),
                "score": comment.get("score", 0),
                "created": comment.get("created_utc", 0),
            })
    
    return posts, comments

def get_user_about(username):
    """Fetch user profile info."""
    data = fetch_json(f"https://www.reddit.com/user/{username}/about.json")
    if data and "data" in data:
        return data["data"]
    return {}

def analyze_reddit(username):
    """Full Reddit analysis."""
    about = get_user_about(username)
    posts, comments = get_user_posts(username)
    
    if not posts and not comments:
        return {
            "source": "reddit",
            "error": f"No public data found for u/{username}. Profile may be private.",
        }
    
    # Subreddit frequency (strongest interest signal)
    subreddits = Counter()
    for post in posts:
        subreddits[post["subreddit"]] += 2  # Posts weighted higher
    for comment in comments:
        subreddits[comment["subreddit"]] += 1
    
    top_subreddits = [s for s, _ in subreddits.most_common(20)]
    
    # Categorize subreddits into interest areas
    interest_categories = {
        "technology": ["programming", "technology", "python", "javascript", "linux", "android", "apple", "webdev", "machinelearning", "artificial", "compsci", "coding", "learnprogramming", "devops", "homelab", "selfhosted"],
        "finance": ["bitcoin", "cryptocurrency", "wallstreetbets", "investing", "personalfinance", "stocks", "ethereum", "fire", "financialindependence"],
        "gaming": ["gaming", "pcgaming", "ps5", "xbox", "nintendo", "steam", "buildapc", "pcmasterrace"],
        "creative": ["art", "photography", "design", "writing", "diy", "woodworking", "3dprinting", "crafts"],
        "science": ["science", "space", "physics", "biology", "chemistry", "askscience", "dataisbeautiful"],
        "politics": ["politics", "news", "worldnews", "conservative", "liberal", "libertarian"],
        "lifestyle": ["fitness", "cooking", "travel", "outdoors", "camping", "hiking", "running"],
        "entertainment": ["movies", "television", "books", "music", "anime", "memes", "funny"],
    }
    
    detected_categories = Counter()
    for sub in top_subreddits:
        sub_lower = sub.lower()
        for category, keywords in interest_categories.items():
            if any(k in sub_lower for k in keywords):
                detected_categories[category] += 1
    
    # Analyze communication style from comments
    all_text = [c["body"] for c in comments if c["body"]]
    avg_length = sum(len(t) for t in all_text) / max(len(all_text), 1)
    
    questions = sum(1 for t in all_text if "?" in t)
    helpful = sum(1 for t in all_text if any(w in t.lower() for w in ["here's how", "you can", "try this", "i recommend", "in my experience"]))
    snarky = sum(1 for t in all_text if any(w in t.lower() for w in ["lol", "lmao", "/s", "bruh"]))
    
    total = max(len(all_text), 1)
    
    tone_signals = []
    if avg_length > 200:
        tone_signals.append("writes detailed, thorough responses")
    elif avg_length < 50:
        tone_signals.append("keeps it brief")
    if helpful / total > 0.2:
        tone_signals.append("helpful — gives advice and recommendations")
    if questions / total > 0.15:
        tone_signals.append("curious — asks questions")
    if snarky / total > 0.2:
        tone_signals.append("uses humor and casual internet tone")
    
    # Karma analysis
    total_post_karma = sum(p["score"] for p in posts)
    total_comment_karma = sum(c["score"] for c in comments)
    
    traits = []
    if total_comment_karma > total_post_karma * 2:
        traits.append("commenter > poster — engages more than broadcasts")
    elif total_post_karma > total_comment_karma * 2:
        traits.append("content creator — shares more than comments")
    
    account_age_days = (time.time() - about.get("created_utc", time.time())) / 86400
    if account_age_days > 365 * 5:
        traits.append("long-time Reddit user")
    
    if about.get("link_karma", 0) + about.get("comment_karma", 0) > 10000:
        traits.append("active community participant")
    
    return {
        "source": "reddit",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "insights": {
            "interests": top_subreddits[:15],
            "interest_categories": [c for c, _ in detected_categories.most_common(5)],
            "top_subreddits": top_subreddits,
            "communication_style": f"Avg comment: {avg_length:.0f} chars. {len(posts)} posts, {len(comments)} comments.",
            "tone": ", ".join(tone_signals) if tone_signals else "neutral",
            "personality_traits": traits,
            "key_contacts": [],
            "profile": {
                "username": username,
                "karma": about.get("link_karma", 0) + about.get("comment_karma", 0),
                "account_age_days": int(account_age_days),
            },
        },
        "confidence": min((len(posts) + len(comments)) / 50, 1.0),
        "items_processed": len(posts) + len(comments),
    }

if __name__ == "__main__":
    os.makedirs(IMPORT_DIR, exist_ok=True)
    
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: reddit.py <username>"}))
        sys.exit(1)
    
    username = sys.argv[1].lstrip("u/").lstrip("/")
    result = analyze_reddit(username)
    
    output_path = os.path.join(IMPORT_DIR, "reddit.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print(json.dumps(result, indent=2))
