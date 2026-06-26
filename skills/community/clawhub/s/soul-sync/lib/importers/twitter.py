#!/usr/bin/env python3
"""
Twitter/X Importer — Analyzes public Twitter profile and tweets for personality insights.
Uses Nitter instances (no API key needed) or Twitter API if token available.

Falls back to scraping public profile data.
"""
import os
import sys
import json
import urllib.request
import re
from datetime import datetime, timezone
from collections import Counter

IMPORT_DIR = "/tmp/soulsync"

# Nitter instances to try (public, no auth needed)
NITTER_INSTANCES = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
    "https://nitter.1d4.us",
]

def fetch_url(url, timeout=10):
    """Fetch URL content."""
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None

def scrape_nitter(username):
    """Scrape Twitter profile via Nitter."""
    for instance in NITTER_INSTANCES:
        url = f"{instance}/{username}"
        html = fetch_url(url)
        if html and "doesn't exist" not in html.lower():
            return html, instance
    return None, None

def parse_nitter_profile(html, username):
    """Extract profile data from Nitter HTML."""
    profile = {"username": username}
    
    # Display name
    match = re.search(r'class="profile-card-fullname"[^>]*>([^<]+)', html)
    if match:
        profile["name"] = match.group(1).strip()
    
    # Bio
    match = re.search(r'class="profile-bio"[^>]*>(.*?)</p>', html, re.DOTALL)
    if match:
        bio = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        profile["bio"] = bio
    
    # Location
    match = re.search(r'class="profile-location"[^>]*>([^<]+)', html)
    if match:
        profile["location"] = match.group(1).strip()
    
    # Stats
    for stat in ["tweets", "following", "followers"]:
        match = re.search(rf'class="profile-stat-num"[^>]*>([^<]+)</[^>]*>\s*<[^>]*>{stat}', html, re.IGNORECASE)
        if match:
            val = match.group(1).strip().replace(",", "")
            profile[stat] = val
    
    return profile

def parse_nitter_tweets(html):
    """Extract recent tweets from Nitter HTML."""
    tweets = []
    
    # Find tweet content blocks
    tweet_blocks = re.findall(
        r'class="tweet-content[^"]*"[^>]*>(.*?)</div>',
        html, re.DOTALL
    )
    
    for block in tweet_blocks[:50]:
        text = re.sub(r'<[^>]+>', ' ', block).strip()
        text = re.sub(r'\s+', ' ', text)
        if text and len(text) > 10:
            tweets.append(text)
    
    return tweets

def analyze_tweets(tweets, profile):
    """Extract personality insights from tweet content."""
    if not tweets:
        return {}
    
    # Topic extraction via word frequency
    stop_words = set("the a an is are was were be been being have has had do does did will would shall should may might can could i me my we our you your he she it they them their this that these those and but or nor for yet so at by from in into of on to with as".split())
    
    words = []
    hashtags = []
    mentions = []
    urls = 0
    questions = 0
    exclamations = 0
    
    for tweet in tweets:
        # Count punctuation patterns
        if "?" in tweet:
            questions += 1
        if "!" in tweet:
            exclamations += 1
        if "http" in tweet:
            urls += 1
        
        # Extract hashtags
        hashtags.extend(re.findall(r'#(\w+)', tweet))
        
        # Extract mentions
        mentions.extend(re.findall(r'@(\w+)', tweet))
        
        # Word frequency
        for word in tweet.lower().split():
            word = re.sub(r'[^a-z0-9]', '', word)
            if word and word not in stop_words and len(word) > 2:
                words.append(word)
    
    word_freq = Counter(words)
    hashtag_freq = Counter(hashtags)
    
    # Determine tone
    tone_signals = []
    if exclamations / max(len(tweets), 1) > 0.3:
        tone_signals.append("enthusiastic")
    if questions / max(len(tweets), 1) > 0.2:
        tone_signals.append("curious/engaging")
    if urls / max(len(tweets), 1) > 0.4:
        tone_signals.append("shares links/resources frequently")
    
    avg_length = sum(len(t) for t in tweets) / max(len(tweets), 1)
    if avg_length < 100:
        tone_signals.append("concise tweeter")
    elif avg_length > 200:
        tone_signals.append("writes longer-form tweets/threads")
    
    # Top interests from word frequency and hashtags
    interests = [w for w, _ in word_freq.most_common(20) if len(w) > 3]
    hashtag_interests = [f"#{h}" for h, _ in hashtag_freq.most_common(10)]
    
    return {
        "tone": ", ".join(tone_signals) if tone_signals else "measured, balanced",
        "interests": interests[:15],
        "hashtags": hashtag_interests,
        "communication_style": f"Avg tweet length: {avg_length:.0f} chars. {'Thread writer' if avg_length > 200 else 'Concise communicator'}.",
        "engagement_style": f"{questions} questions, {exclamations} exclamations, {urls} links shared in {len(tweets)} tweets",
        "top_mentions": [f"@{m}" for m, _ in Counter(mentions).most_common(5)],
    }

def import_twitter(username):
    """Main import function."""
    html, instance = scrape_nitter(username)
    
    if not html:
        return {
            "source": "twitter",
            "error": "Could not fetch Twitter profile. Nitter instances may be down.",
            "processed_at": datetime.now(timezone.utc).isoformat(),
        }
    
    profile = parse_nitter_profile(html, username)
    tweets = parse_nitter_tweets(html)
    analysis = analyze_tweets(tweets, profile)
    
    return {
        "source": "twitter",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "insights": {
            "communication_style": analysis.get("communication_style", ""),
            "tone": analysis.get("tone", ""),
            "interests": analysis.get("interests", []),
            "key_contacts": analysis.get("top_mentions", []),
            "hashtags": analysis.get("hashtags", []),
            "engagement": analysis.get("engagement_style", ""),
            "profile": profile,
        },
        "confidence": min(len(tweets) / 30, 1.0),
        "items_processed": len(tweets),
        "nitter_instance": instance,
    }

if __name__ == "__main__":
    os.makedirs(IMPORT_DIR, exist_ok=True)
    
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: twitter.py <username>"}))
        sys.exit(1)
    
    username = sys.argv[1].lstrip("@")
    
    if "--check" in sys.argv:
        html, instance = scrape_nitter(username)
        print(json.dumps({"available": html is not None, "instance": instance}))
        sys.exit(0)
    
    result = import_twitter(username)
    
    output_path = os.path.join(IMPORT_DIR, "twitter.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print(json.dumps(result, indent=2))
