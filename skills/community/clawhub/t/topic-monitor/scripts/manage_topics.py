#!/usr/bin/env python3
"""
Topic management CLI for topic-monitor.

Usage:
    python3 manage_topics.py add "Topic Name" --query "search" --keywords "a,b,c"
    python3 manage_topics.py list
    python3 manage_topics.py edit <id> --frequency hourly
    python3 manage_topics.py remove <id>
    python3 manage_topics.py test <id>
    python3 manage_topics.py discover-feed https://example.com/blog
    python3 manage_topics.py import-opml feeds.opml
"""

import sys
import argparse
import re
import json
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import load_config, save_config, get_topic, load_state, get_settings
from monitor import monitor_topic, discover_feed_urls, github_release_feed_url


def generate_id(name: str) -> str:
    topic_id = name.lower()
    topic_id = re.sub(r'[^\w\s-]', '', topic_id)
    topic_id = re.sub(r'[-\s]+', '-', topic_id)
    return topic_id.strip('-')


def split_csv(value: str):
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def ensure_topic_defaults(topic: dict) -> dict:
    topic.setdefault("keywords", [])
    topic.setdefault("feeds", [])
    topic.setdefault("github_repos", [])
    topic.setdefault("exclude_keywords", [])
    topic.setdefault("required_keywords", [])
    topic.setdefault("alert_on_sentiment_shift", False)
    topic.setdefault("frequency", "daily")
    topic.setdefault("importance_threshold", "medium")
    topic.setdefault("channels", ["telegram"])
    topic.setdefault("context", "")
    topic.setdefault("alert_on", [])
    topic.setdefault("ignore_sources", [])
    topic.setdefault("boost_sources", [])
    return topic


def add_topic(args):
    config = load_config()
    topic_id = args.id or generate_id(args.name)
    existing_ids = [t.get("id") for t in config.get("topics", [])]
    if topic_id in existing_ids:
        print(f"❌ Topic with ID '{topic_id}' already exists", file=sys.stderr)
        sys.exit(1)

    feeds = split_csv(args.feeds)
    if args.discover_feeds:
        discovered = []
        for candidate in split_csv(args.discover_feeds):
            discovered.extend(discover_feed_urls(candidate))
        feeds = list(dict.fromkeys(feeds + discovered))

    github_repos = split_csv(args.github_repos)
    alert_on = split_csv(args.alert_on)
    if github_repos and "github_release" not in alert_on:
        alert_on.append("github_release")

    topic = ensure_topic_defaults({
        "id": topic_id,
        "name": args.name,
        "query": args.query or "",
        "keywords": split_csv(args.keywords),
        "feeds": feeds,
        "github_repos": github_repos,
        "exclude_keywords": split_csv(args.exclude_keywords),
        "required_keywords": split_csv(args.required_keywords),
        "frequency": args.frequency,
        "importance_threshold": args.importance,
        "channels": split_csv(args.channels) if args.channels else ["telegram"],
        "context": args.context or "",
        "alert_on": alert_on,
        "alert_on_sentiment_shift": args.alert_on_sentiment_shift,
        "ignore_sources": [],
        "boost_sources": [],
    })

    config.setdefault("topics", []).append(topic)
    save_config(config)

    print(f"✅ Added topic: {args.name} ({topic_id})")
    if topic.get("query"):
        print(f"   Query: {topic['query']}")
    if topic.get("feeds"):
        print(f"   Feeds: {len(topic['feeds'])}")
    if topic.get("github_repos"):
        print(f"   GitHub repos: {', '.join(topic['github_repos'])}")
    if topic.get("required_keywords"):
        print(f"   Required keywords: {', '.join(topic['required_keywords'])}")
    if topic.get("exclude_keywords"):
        print(f"   Exclude keywords: {', '.join(topic['exclude_keywords'])}")


def list_topics(args):
    config = load_config()
    topics = config.get("topics", [])
    if not topics:
        print("No topics configured")
        return

    print(f"\n📋 Configured Topics ({len(topics)})\n")
    for topic in topics:
        topic = ensure_topic_defaults(topic)
        print(f"{'='*60}")
        print(f"ID:         {topic.get('id')}")
        print(f"Name:       {topic.get('name')}")
        print(f"Query:      {topic.get('query') or '—'}")
        print(f"Keywords:   {', '.join(topic.get('keywords', [])) or '—'}")
        print(f"Feeds:      {', '.join(topic.get('feeds', [])) or '—'}")
        print(f"GitHub:     {', '.join(topic.get('github_repos', [])) or '—'}")
        print(f"Required:   {', '.join(topic.get('required_keywords', [])) or '—'}")
        print(f"Excluded:   {', '.join(topic.get('exclude_keywords', [])) or '—'}")
        print(f"Frequency:  {topic.get('frequency')}")
        print(f"Importance: {topic.get('importance_threshold')}")
        print(f"Channels:   {', '.join(topic.get('channels', []))}")
        print(f"Sentiment shift alerts: {topic.get('alert_on_sentiment_shift')}")
        if topic.get('context'):
            print(f"Context:    {topic.get('context')}")
        print()


def edit_topic(args):
    config = load_config()
    topics = config.get("topics", [])
    topic_idx = None
    for idx, topic in enumerate(topics):
        if topic.get("id") == args.topic_id:
            topic_idx = idx
            break
    if topic_idx is None:
        print(f"❌ Topic '{args.topic_id}' not found", file=sys.stderr)
        sys.exit(1)

    topic = ensure_topic_defaults(topics[topic_idx])

    if args.name:
        topic["name"] = args.name
    if args.query is not None:
        topic["query"] = args.query
    if args.keywords is not None:
        topic["keywords"] = split_csv(args.keywords)
    if args.feeds is not None:
        topic["feeds"] = split_csv(args.feeds)
    if args.github_repos is not None:
        topic["github_repos"] = split_csv(args.github_repos)
        if topic["github_repos"] and "github_release" not in topic["alert_on"]:
            topic["alert_on"].append("github_release")
    if args.exclude_keywords is not None:
        topic["exclude_keywords"] = split_csv(args.exclude_keywords)
    if args.required_keywords is not None:
        topic["required_keywords"] = split_csv(args.required_keywords)
    if args.frequency:
        topic["frequency"] = args.frequency
    if args.importance:
        topic["importance_threshold"] = args.importance
    if args.channels:
        topic["channels"] = split_csv(args.channels)
    if args.context is not None:
        topic["context"] = args.context
    if args.alert_on is not None:
        topic["alert_on"] = split_csv(args.alert_on)
    if args.alert_on_sentiment_shift is not None:
        topic["alert_on_sentiment_shift"] = args.alert_on_sentiment_shift

    if args.discover_feeds:
        discovered = []
        for candidate in split_csv(args.discover_feeds):
            discovered.extend(discover_feed_urls(candidate))
        topic["feeds"] = list(dict.fromkeys(topic.get("feeds", []) + discovered))

    topics[topic_idx] = topic
    config["topics"] = topics
    save_config(config)
    print(f"✅ Updated topic: {topic.get('name')} ({args.topic_id})")


def remove_topic(args):
    config = load_config()
    topics = config.get("topics", [])
    new_topics = [t for t in topics if t.get("id") != args.topic_id]
    if len(new_topics) == len(topics):
        print(f"❌ Topic '{args.topic_id}' not found", file=sys.stderr)
        sys.exit(1)
    config["topics"] = new_topics
    save_config(config)
    print(f"✅ Removed topic: {args.topic_id}")


def test_topic(args):
    topic = get_topic(args.topic_id)
    if not topic:
        print(f"❌ Topic '{args.topic_id}' not found", file=sys.stderr)
        sys.exit(1)
    print(f"🧪 Testing topic: {topic.get('name')}\n")
    state = load_state()
    settings = get_settings()
    monitor_topic(topic, state, settings, dry_run=True, verbose=True)


def discover_feed(args):
    urls = discover_feed_urls(args.url)
    if not urls:
        print("No feeds discovered", file=sys.stderr)
        sys.exit(1)
    for url in urls:
        print(url)


def import_opml(args):
    config = load_config()
    config.setdefault("topics", [])
    tree = ET.parse(args.opml_file)
    root = tree.getroot()
    outlines = root.findall(".//outline")

    added = 0
    for outline in outlines:
        xml_url = outline.attrib.get("xmlUrl") or outline.attrib.get("xmlurl")
        title = outline.attrib.get("title") or outline.attrib.get("text") or outline.attrib.get("xmlUrl")
        html_url = outline.attrib.get("htmlUrl") or outline.attrib.get("htmlurl")
        if not xml_url:
            continue

        topic_name = title or xml_url
        topic_id = generate_id(topic_name)
        existing = next((t for t in config["topics"] if t.get("id") == topic_id), None)
        feed_list = [xml_url]
        if html_url:
            feed_list.extend([u for u in discover_feed_urls(html_url) if u != xml_url])

        if existing:
            merged = list(dict.fromkeys(existing.get("feeds", []) + feed_list))
            existing["feeds"] = merged
            if html_url and not existing.get("query"):
                existing["query"] = html_url
        else:
            topic = ensure_topic_defaults({
                "id": topic_id,
                "name": topic_name,
                "query": html_url or "",
                "keywords": [],
                "feeds": list(dict.fromkeys(feed_list)),
                "github_repos": [],
                "exclude_keywords": [],
                "required_keywords": [],
                "frequency": args.frequency,
                "importance_threshold": args.importance,
                "channels": split_csv(args.channels) if args.channels else ["telegram"],
                "context": args.context or "Imported from OPML",
                "alert_on": [],
                "alert_on_sentiment_shift": False,
                "ignore_sources": [],
                "boost_sources": [],
            })
            config["topics"].append(topic)
            added += 1

    save_config(config)
    print(f"✅ Imported OPML: added {added} topic(s), updated matching topics where needed")


def main():
    parser = argparse.ArgumentParser(description="Manage research topics")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new topic")
    add_parser.add_argument("name", help="Topic name")
    add_parser.add_argument("--id", help="Custom topic ID")
    add_parser.add_argument("--query", help="Search query")
    add_parser.add_argument("--keywords", help="Comma-separated keywords")
    add_parser.add_argument("--feeds", help="Comma-separated RSS/Atom feed URLs")
    add_parser.add_argument("--discover-feeds", help="Comma-separated web URLs to auto-discover feeds from")
    add_parser.add_argument("--github-repos", help="Comma-separated owner/repo values for GitHub release monitoring")
    add_parser.add_argument("--exclude-keywords", help="Comma-separated keywords to filter out before scoring")
    add_parser.add_argument("--required-keywords", help="Comma-separated keywords that must all appear")
    add_parser.add_argument("--frequency", choices=["hourly", "daily", "weekly"], default="daily")
    add_parser.add_argument("--importance", choices=["high", "medium", "low"], default="medium")
    add_parser.add_argument("--channels", default="telegram", help="Comma-separated channels")
    add_parser.add_argument("--context", help="Why this topic matters to you")
    add_parser.add_argument("--alert-on", help="Comma-separated alert conditions")
    add_parser.add_argument("--alert-on-sentiment-shift", action="store_true", help="Alert when sentiment changes from previous findings")
    add_parser.set_defaults(func=add_topic)

    list_parser = subparsers.add_parser("list", help="List all topics")
    list_parser.set_defaults(func=list_topics)

    edit_parser = subparsers.add_parser("edit", help="Edit a topic")
    edit_parser.add_argument("topic_id", help="Topic ID to edit")
    edit_parser.add_argument("--name", help="New name")
    edit_parser.add_argument("--query", help="New query (empty string allowed)")
    edit_parser.add_argument("--keywords", help="New keywords")
    edit_parser.add_argument("--feeds", help="New feed URLs")
    edit_parser.add_argument("--discover-feeds", help="Discover and append feeds from these URLs")
    edit_parser.add_argument("--github-repos", help="New GitHub repos")
    edit_parser.add_argument("--exclude-keywords", help="New exclude keywords")
    edit_parser.add_argument("--required-keywords", help="New required keywords")
    edit_parser.add_argument("--frequency", choices=["hourly", "daily", "weekly"])
    edit_parser.add_argument("--importance", choices=["high", "medium", "low"])
    edit_parser.add_argument("--channels", help="New channels")
    edit_parser.add_argument("--context", help="New context")
    edit_parser.add_argument("--alert-on", help="New alert conditions")
    edit_parser.add_argument("--alert-on-sentiment-shift", action=argparse.BooleanOptionalAction, default=None, help="Toggle sentiment shift alerts")
    edit_parser.set_defaults(func=edit_topic)

    remove_parser = subparsers.add_parser("remove", help="Remove a topic")
    remove_parser.add_argument("topic_id", help="Topic ID to remove")
    remove_parser.set_defaults(func=remove_topic)

    test_parser = subparsers.add_parser("test", help="Test a topic")
    test_parser.add_argument("topic_id", help="Topic ID to test")
    test_parser.set_defaults(func=test_topic)

    discover_parser = subparsers.add_parser("discover-feed", help="Discover feed URLs from a webpage URL")
    discover_parser.add_argument("url", help="Webpage URL to inspect")
    discover_parser.set_defaults(func=discover_feed)

    opml_parser = subparsers.add_parser("import-opml", help="Import RSS/Atom feeds from an OPML file")
    opml_parser.add_argument("opml_file", help="Path to OPML file")
    opml_parser.add_argument("--frequency", choices=["hourly", "daily", "weekly"], default="daily")
    opml_parser.add_argument("--importance", choices=["high", "medium", "low"], default="medium")
    opml_parser.add_argument("--channels", default="telegram", help="Comma-separated channels")
    opml_parser.add_argument("--context", help="Context applied to imported topics")
    opml_parser.set_defaults(func=import_opml)

    args = parser.parse_args()
    try:
        args.func(args)
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
