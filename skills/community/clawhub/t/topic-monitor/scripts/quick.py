#!/usr/bin/env python3
"""
Quick Start - One-liner topic monitoring setup.
"""

import sys
import argparse
import re
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

try:
    from config import load_config, save_config, CONFIG_FILE
except ImportError:
    CONFIG_FILE = Path(__file__).parent.parent / "config.json"

    def load_config():
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                return json.load(f)
        return {"topics": [], "settings": {}}

    def save_config(config):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)


def generate_id(name: str) -> str:
    topic_id = name.lower()
    topic_id = re.sub(r'[^\w\s-]', '', topic_id)
    topic_id = re.sub(r'[-\s]+', '-', topic_id)
    return topic_id.strip('-')[:30]


def split_csv(value: str):
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def quick_add(args):
    config = load_config()
    topic_id = generate_id(args.topic)
    existing_ids = [t.get("id") for t in config.get("topics", [])]
    if topic_id in existing_ids:
        print(f"⚠️  Topic '{topic_id}' already exists. Use manage_topics.py to edit.")
        sys.exit(1)

    query = args.query or f"{args.topic} news updates"
    if args.keywords:
        keywords = split_csv(args.keywords)
    else:
        words = re.findall(r'\b[A-Za-z]{3,}\b', args.topic)
        keywords = list(dict.fromkeys(words))[:5]

    topic = {
        "id": topic_id,
        "name": args.topic,
        "query": query,
        "keywords": keywords,
        "feeds": split_csv(args.feeds),
        "github_repos": split_csv(args.github_repos),
        "exclude_keywords": split_csv(args.exclude_keywords),
        "required_keywords": split_csv(args.required_keywords),
        "frequency": args.frequency,
        "importance_threshold": args.importance,
        "channels": [args.channel],
        "context": args.context or f"Monitoring {args.topic}",
        "alert_on": ["github_release"] if args.github_repos else [],
        "alert_on_sentiment_shift": args.alert_on_sentiment_shift,
        "created": datetime.now().isoformat(),
    }

    config.setdefault("topics", []).append(topic)
    config.setdefault("settings", {
        "digest_day": "sunday",
        "digest_time": "18:00",
        "max_alerts_per_day": 5,
        "deduplication_window_hours": 72,
    })

    save_config(config)

    print()
    print("✅ Topic created!")
    print()
    print(f"   📌 {args.topic}")
    print(f"   🔍 Query: {query or '—'}")
    print(f"   🏷️  Keywords: {', '.join(keywords) or '—'}")
    if topic['feeds']:
        print(f"   📰 Feeds: {', '.join(topic['feeds'])}")
    if topic['github_repos']:
        print(f"   🚀 GitHub repos: {', '.join(topic['github_repos'])}")
    print(f"   ⏰ Frequency: {args.frequency}")
    print(f"   🔔 Alert threshold: {args.importance}")
    print(f"   📱 Channel: {args.channel}")
    print()
    print("Next steps:")
    print(f"   • Test:    python3 scripts/monitor.py --topic {topic_id} --dry-run --verbose")
    print(f"   • Run:     python3 scripts/monitor.py --topic {topic_id}")
    print(f"   • Edit:    python3 scripts/manage_topics.py edit {topic_id} --frequency hourly")
    print(f"   • Remove:  python3 scripts/manage_topics.py remove {topic_id}")
    print()
    return topic_id


def main():
    parser = argparse.ArgumentParser(description="Quick Start - Add a topic to monitor in one command")
    parser.add_argument("topic", help="Topic name to monitor")
    parser.add_argument("--query", "-q", help="Custom search query")
    parser.add_argument("--keywords", "-k", help="Comma-separated keywords to watch for")
    parser.add_argument("--feeds", help="Comma-separated RSS/Atom feed URLs")
    parser.add_argument("--github-repos", help="Comma-separated owner/repo values for release monitoring")
    parser.add_argument("--exclude-keywords", help="Comma-separated keywords to filter out")
    parser.add_argument("--required-keywords", help="Comma-separated keywords that must all appear")
    parser.add_argument("--frequency", "-f", choices=["hourly", "daily", "weekly"], default="daily")
    parser.add_argument("--importance", "-i", choices=["high", "medium", "low"], default="medium")
    parser.add_argument("--channel", "-c", default="telegram", help="Where to send alerts")
    parser.add_argument("--context", help="Why this topic matters to you")
    parser.add_argument("--alert-on-sentiment-shift", action="store_true", help="Alert when sentiment changes")
    args = parser.parse_args()
    quick_add(args)


if __name__ == "__main__":
    main()
