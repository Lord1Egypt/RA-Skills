#!/usr/bin/env python3
"""
YouTube Importer — Analyzes YouTube watch history and subscriptions for deep interest mapping.
Supports: Google Takeout export (watch-history.json, subscriptions.json)
and YouTube Data API v3 if token available.

YouTube watch history is one of the richest signals for true interests —
what you watch when nobody's looking reveals more than what you post publicly.
"""
import os
import sys
import json
import glob
from datetime import datetime, timezone
from collections import Counter

IMPORT_DIR = "/tmp/soulsync"

def find_youtube_export():
    """Find Google Takeout YouTube data."""
    search_paths = [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Desktop"),
    ]
    
    for base in search_paths:
        if not os.path.isdir(base):
            continue
        # Google Takeout structure
        for d in os.listdir(base):
            full = os.path.join(base, d)
            yt_path = os.path.join(full, "YouTube and YouTube Music")
            if os.path.isdir(yt_path):
                return yt_path
            # Alt path
            yt_path2 = os.path.join(full, "Takeout", "YouTube and YouTube Music")
            if os.path.isdir(yt_path2):
                return yt_path2
    
    return None

def parse_watch_history(export_dir):
    """Parse YouTube watch history from Takeout export."""
    history_path = os.path.join(export_dir, "history", "watch-history.json")
    if not os.path.exists(history_path):
        return []
    
    try:
        with open(history_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return []

def parse_subscriptions(export_dir):
    """Parse YouTube subscriptions."""
    sub_path = os.path.join(export_dir, "subscriptions", "subscriptions.json")
    if not os.path.exists(sub_path):
        # Try CSV format
        sub_csv = os.path.join(export_dir, "subscriptions", "subscriptions.csv")
        if os.path.exists(sub_csv):
            channels = []
            with open(sub_csv, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) >= 3 and parts[0] != "Channel Id":
                        channels.append(parts[2] if len(parts) > 2 else parts[0])
            return channels
        return []
    
    try:
        with open(sub_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [item.get("snippet", {}).get("title", "") for item in data if item.get("snippet")]
    except:
        return []

def analyze_youtube(export_dir):
    """Analyze YouTube data for personality insights."""
    watch_history = parse_watch_history(export_dir)
    subscriptions = parse_subscriptions(export_dir)
    
    # Analyze watch history
    channels_watched = Counter()
    watch_hours = Counter()
    watch_days = Counter()
    titles = []
    
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for entry in watch_history[:1000]:
        # Channel
        subtitles = entry.get("subtitles", [])
        for sub in subtitles:
            channel = sub.get("name", "")
            if channel:
                channels_watched[channel] += 1
        
        # Title for topic analysis
        title = entry.get("title", "").replace("Watched ", "")
        if title:
            titles.append(title)
        
        # Timing
        time_str = entry.get("time", "")
        if time_str:
            try:
                dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
                watch_hours[dt.hour] += 1
                watch_days[day_names[dt.weekday()]] += 1
            except:
                pass
    
    # Topic extraction from titles
    stop_words = set("the a an is are was were be been have has had do does did will would can could i me my we you he she it they this that and but or for to in of on at by from with as how what why when where who".split())
    
    words = Counter()
    for title in titles:
        for word in title.lower().split():
            word = ''.join(c for c in word if c.isalnum())
            if word and word not in stop_words and len(word) > 3:
                words[word] += 1
    
    top_topics = [w for w, _ in words.most_common(25)]
    top_channels = [c for c, _ in channels_watched.most_common(15)]
    peak_hours = [h for h, _ in watch_hours.most_common(3)]
    peak_days = [d for d, _ in watch_days.most_common(3)]
    
    # Infer content type preferences
    content_types = Counter()
    tech_keywords = ["tutorial", "how to", "review", "guide", "explained", "course", "learn"]
    entertainment_keywords = ["vlog", "reaction", "funny", "comedy", "prank", "challenge"]
    news_keywords = ["news", "update", "breaking", "report", "analysis", "opinion"]
    music_keywords = ["official", "music video", "lyrics", "live", "concert", "remix"]
    
    for title in titles:
        t = title.lower()
        if any(k in t for k in tech_keywords):
            content_types["educational/tech"] += 1
        if any(k in t for k in entertainment_keywords):
            content_types["entertainment"] += 1
        if any(k in t for k in news_keywords):
            content_types["news/analysis"] += 1
        if any(k in t for k in music_keywords):
            content_types["music"] += 1
    
    # Determine learning style
    traits = []
    total = max(len(titles), 1)
    if content_types.get("educational/tech", 0) / total > 0.3:
        traits.append("self-learner — watches educational content heavily")
    if content_types.get("news/analysis", 0) / total > 0.2:
        traits.append("stays informed — consumes news/analysis")
    if content_types.get("entertainment", 0) / total > 0.4:
        traits.append("uses YouTube for entertainment/relaxation")
    if content_types.get("music", 0) / total > 0.3:
        traits.append("music-oriented")
    
    # Watch pattern insights
    if watch_hours:
        night_watches = sum(watch_hours.get(h, 0) for h in range(22, 24)) + sum(watch_hours.get(h, 0) for h in range(0, 6))
        if night_watches / max(sum(watch_hours.values()), 1) > 0.3:
            traits.append("night owl — watches late")
    
    return {
        "source": "youtube",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "insights": {
            "interests": top_topics[:15],
            "top_channels": top_channels,
            "subscriptions": subscriptions[:20],
            "content_preferences": dict(content_types.most_common(5)),
            "personality_traits": traits,
            "watch_patterns": {
                "peak_hours": [f"{h}:00" for h in peak_hours],
                "peak_days": peak_days,
            },
            "communication_style": "",
            "tone": "",
        },
        "confidence": min(len(watch_history) / 200, 1.0),
        "items_processed": len(watch_history),
    }

if __name__ == "__main__":
    os.makedirs(IMPORT_DIR, exist_ok=True)
    
    export_dir = None
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        export_dir = sys.argv[1]
    else:
        export_dir = find_youtube_export()
    
    if not export_dir:
        result = {
            "source": "youtube",
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "error": "No YouTube data export found.",
            "setup_help": (
                "To use this importer:\n"
                "1. Go to takeout.google.com\n"
                "2. Deselect all, then select only 'YouTube and YouTube Music'\n"
                "3. Choose JSON format\n"
                "4. Download and extract to ~/Downloads/\n"
                "5. Run this importer again"
            ),
        }
    else:
        result = analyze_youtube(export_dir)
    
    output_path = os.path.join(IMPORT_DIR, "youtube.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print(json.dumps(result, indent=2))
