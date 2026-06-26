#!/usr/bin/env python3
"""Random quote picker for TweetNugget skill."""

import argparse
import json
import random
import sys
from pathlib import Path

REFERENCES_DIR = Path(__file__).parent.parent / "references"
MAX_FILE_SIZE = 1024 * 1024  # 1MB safety limit


def load_quotes(collection=None):
    """Load quotes from JSON files in references/ directory.

    Args:
        collection: Optional filename (e.g. 'stoic-quotes.json') to load only one collection.

    Returns:
        List of quote dicts, or empty list on failure.
    """
    quotes = []

    if collection:
        files = [REFERENCES_DIR / collection]
    else:
        files = sorted(REFERENCES_DIR.glob("*.json"))

    for filepath in files:
        if not filepath.is_file() or filepath.is_symlink():
            continue
        try:
            if filepath.stat().st_size > MAX_FILE_SIZE:
                continue
            with open(filepath) as fp:
                data = json.load(fp)
            if isinstance(data, dict) and "quotes" in data and isinstance(data["quotes"], list):
                quotes.extend(data["quotes"])
        except (OSError, json.JSONDecodeError, KeyError) as e:
            print(f"Error reading {filepath.name}: {e}", file=sys.stderr)

    return quotes


def format_quote(quote):
    """Format a quote dict for display."""
    return f'"{quote["text"]}" - {quote["author"]}'


def get_random_quote():
    """Pick a random quote from all collections."""
    quotes = load_quotes()
    if not quotes:
        print("No quotes found.")
        return
    print(format_quote(random.choice(quotes)))


def get_surprise_quote():
    """Pick a random collection, then a random quote from it."""
    files = sorted(REFERENCES_DIR.glob("*.json"))
    if not files:
        print("No quote collections found.")
        return

    # Try up to 3 random collections in case one fails to load
    for _ in range(3):
        chosen = random.choice(files)
        quotes = load_quotes(collection=chosen.name)
        if quotes:
            print(format_quote(random.choice(quotes)))
            return

    print("Could not load a quote.")


def get_filtered_quote(tag):
    """Pick a random quote matching a tag. Falls back to random if no match."""
    quotes = load_quotes()
    if not quotes:
        print("No quotes found.")
        return

    tag_lower = tag.lower()
    filtered = [q for q in quotes if any(tag_lower in t.lower() for t in q.get("tags", []))]

    if filtered:
        print(format_quote(random.choice(filtered)))
    else:
        print(f'(No quotes tagged "{tag}", here is a random one:)')
        print(format_quote(random.choice(quotes)))


def main():
    parser = argparse.ArgumentParser(description="TweetNugget quote picker")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--tag", help="Filter quotes by tag (partial match)")
    group.add_argument("--surprise", action="store_true", help="Random collection, then random quote")
    args = parser.parse_args()

    if args.tag:
        get_filtered_quote(args.tag)
    elif args.surprise:
        get_surprise_quote()
    else:
        get_random_quote()


if __name__ == "__main__":
    main()
