#!/usr/bin/env python3
"""
Interactive onboarding wizard for topic-monitor skill.
Runs on first use when no config.json exists.
"""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"


def print_welcome():
    print()
    print("=" * 55)
    print("  🔍 Topic Monitor - Setup Wizard")
    print("=" * 55)
    print()
    print("Welcome! Let's set up your personal topic monitoring.")
    print("You can mix web search, RSS/Atom feeds, and GitHub release feeds.")
    print()


def prompt(question: str, default: str = None) -> str:
    question = f"{question} [{default}]: " if default else f"{question}: "
    response = input(question).strip()
    return response if response else (default or "")


def prompt_yes_no(question: str, default: bool = True) -> bool:
    default_hint = "Y/n" if default else "y/N"
    response = input(f"{question} ({default_hint}): ").strip().lower()
    if not response:
        return default
    return response in ('y', 'yes', 'ja', 'si', 'oui')


def prompt_choice(question: str, choices: list, default: str = None) -> str:
    print(f"\n{question}")
    for i, choice in enumerate(choices, 1):
        marker = " *" if choice == default else ""
        print(f"  {i}. {choice}{marker}")
    while True:
        response = input(f"\nEnter number or value [{default or choices[0]}]: ").strip()
        if not response:
            return default or choices[0]
        try:
            idx = int(response)
            if 1 <= idx <= len(choices):
                return choices[idx - 1]
        except ValueError:
            pass
        for choice in choices:
            if choice.lower() == response.lower():
                return choice
        print(f"  Please enter a number 1-{len(choices)} or a valid option.")


def prompt_multiline(question: str, hint: str = None) -> list:
    print(f"\n{question}")
    if hint:
        print(f"  {hint}")
    print("  (Enter each item on a new line. Empty line when done)")
    print()
    items = []
    while True:
        line = input("  > ").strip()
        if not line:
            break
        items.append(line)
    return items


def prompt_csv(question: str) -> list:
    response = input(f"  {question}: ").strip()
    if not response:
        return []
    return [item.strip() for item in response.split(",") if item.strip()]


def create_topic_id(name: str) -> str:
    topic_id = name.lower().replace(" ", "-")
    topic_id = "".join(c for c in topic_id if c.isalnum() or c == "-")
    topic_id = "-".join(filter(None, topic_id.split("-")))
    return topic_id[:30]


def gather_topics() -> list:
    topics = []
    print("-" * 55)
    print("📋 STEP 1: Topics to Monitor")
    print("-" * 55)
    topic_names = prompt_multiline(
        "What topics do you want to monitor?",
        "Examples: AI Models, Security Alerts, Product Updates"
    )
    if not topic_names:
        print("\n⚠️  No topics entered. You can add them later with manage_topics.py")
        return []

    for i, name in enumerate(topic_names, 1):
        print(f"\n--- Topic {i}/{len(topic_names)}: {name} ---")
        query = prompt(f"  Search query for '{name}'", f"{name} news updates")
        keywords = prompt_csv(f"Keywords for '{name}' (comma-separated)")
        feeds = prompt_csv(f"RSS/Atom feeds for '{name}' (comma-separated, optional)")
        github_repos = prompt_csv(f"GitHub repos for release monitoring (owner/repo, optional)")
        required_keywords = prompt_csv(f"Required keywords (all must appear, optional)")
        exclude_keywords = prompt_csv(f"Exclude keywords (filter out if present, optional)")
        alert_on_sentiment_shift = prompt_yes_no("Alert on sentiment shift?", default=False)

        topic = {
            "id": create_topic_id(name),
            "name": name,
            "query": query,
            "keywords": keywords,
            "feeds": feeds,
            "github_repos": github_repos,
            "required_keywords": required_keywords,
            "exclude_keywords": exclude_keywords,
            "frequency": None,
            "importance_threshold": None,
            "channels": ["telegram"],
            "context": "",
            "alert_on": ["keyword_exact_match"] + (["github_release"] if github_repos else []),
            "alert_on_sentiment_shift": alert_on_sentiment_shift,
            "ignore_sources": [],
            "boost_sources": [],
        }
        topics.append(topic)
    return topics


def gather_settings() -> dict:
    print()
    print("-" * 55)
    print("⚙️  STEP 2: Monitoring Settings")
    print("-" * 55)
    frequency = prompt_choice("How often should I check for updates?", ["hourly", "daily", "weekly"], default="daily")
    importance = prompt_choice("Importance threshold for alerts?", ["low", "medium", "high"], default="medium")
    digest_enabled = prompt_yes_no("Enable weekly digest?", default=True)
    digest_day = "sunday"
    if digest_enabled:
        digest_day = prompt_choice("Which day should I send the digest?", ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"], default="sunday")

    return {
        "frequency": frequency,
        "importance_threshold": importance,
        "digest_enabled": digest_enabled,
        "digest_day": digest_day,
        "digest_time": "18:00",
        "max_alerts_per_day": 5,
        "max_alerts_per_topic_per_day": 2,
        "deduplication_window_hours": 72,
        "learning_enabled": True,
        "quiet_hours": {"enabled": False, "start": "22:00", "end": "08:00"},
    }


def build_config(topics: list, settings: dict) -> dict:
    frequency = settings.pop("frequency")
    importance = settings.pop("importance_threshold")
    for topic in topics:
        topic["frequency"] = frequency
        topic["importance_threshold"] = importance

    return {
        "topics": topics,
        "settings": settings,
        "channels": {
            "telegram": {
                "enabled": True,
                "chat_id": None,
                "silent": False,
                "effects": {"high_importance": "🔥", "medium_importance": "📌"},
            },
            "discord": {"enabled": False, "webhook_url": None, "username": "Topic Monitor", "avatar_url": None},
            "email": {
                "enabled": False,
                "to": None,
                "from": "monitor@yourdomain.com",
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "smtp_user": None,
                "smtp_password": None,
            },
        },
    }


def save_config(config: dict):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def print_summary(config: dict):
    print()
    print("=" * 55)
    print("  ✅ Setup Complete!")
    print("=" * 55)
    print()
    for topic in config.get("topics", []):
        print(f"• {topic['name']}")
        print(f"  Query: {topic['query'] or '—'}")
        print(f"  Keywords: {', '.join(topic.get('keywords', [])) or '—'}")
        print(f"  Feeds: {', '.join(topic.get('feeds', [])) or '—'}")
        print(f"  GitHub repos: {', '.join(topic.get('github_repos', [])) or '—'}")
        print(f"  Required keywords: {', '.join(topic.get('required_keywords', [])) or '—'}")
        print(f"  Exclude keywords: {', '.join(topic.get('exclude_keywords', [])) or '—'}")
        print(f"  Sentiment shift alerts: {topic.get('alert_on_sentiment_shift')}")
        print()
    print("Test with: python3 scripts/monitor.py --dry-run --verbose")
    print()


def main():
    if CONFIG_FILE.exists():
        print("\n⚠️  config.json already exists!\n")
        if not prompt_yes_no("Do you want to start fresh and overwrite it?", default=False):
            print("\nKeeping existing config. Use manage_topics.py to edit topics.")
            sys.exit(0)

    print_welcome()
    try:
        topics = gather_topics()
        settings = gather_settings()
        config = build_config(topics, settings)
        save_config(config)
        print_summary(config)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled. No changes made.")
        sys.exit(1)
    except EOFError:
        print("\n\n⚠️  Input ended. No changes made.")
        sys.exit(1)


if __name__ == "__main__":
    main()
