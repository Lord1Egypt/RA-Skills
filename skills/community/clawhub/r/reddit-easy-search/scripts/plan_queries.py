#!/usr/bin/env python3
"""Create a small, diverse set of web queries for public Reddit research."""

from __future__ import annotations

import argparse
import json
import re


INTENTS = (
    "issue workaround",
    "repo workflow production",
    "\"after 1 month\" experience",
    "regression problems complaints",
    "setup best practices",
    "alternatives comparison switched",
)


def clean(value: str) -> str:
    return " ".join(value.split()).strip()


def normalize_subreddit(value: str | None) -> str | None:
    if not value:
        return None
    value = re.sub(r"^(?:https?://)?(?:www\.)?reddit\.com/r/", "", value.strip(), flags=re.I)
    value = re.sub(r"^r/", "", value, flags=re.I).strip("/")
    if not re.fullmatch(r"[A-Za-z0-9_]+", value):
        raise ValueError("subreddit must contain only letters, numbers, or underscores")
    return value


def plan_queries(
    topic: str,
    subreddit: str | None = None,
    time_range: str | None = None,
    max_queries: int = 5,
) -> list[str]:
    topic = clean(topic)
    if not topic:
        raise ValueError("topic must not be empty")
    if not 1 <= max_queries <= len(INTENTS):
        raise ValueError(f"max_queries must be between 1 and {len(INTENTS)}")

    subreddit = normalize_subreddit(subreddit)
    scope = f"site:reddit.com/r/{subreddit}" if subreddit else "site:reddit.com"
    suffix = f" {clean(time_range)}" if time_range else ""
    return [f"{scope} {topic} {intent}{suffix}" for intent in INTENTS[:max_queries]]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic")
    parser.add_argument("--subreddit")
    parser.add_argument("--time-range")
    parser.add_argument("--max-queries", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        queries = plan_queries(
            args.topic,
            subreddit=args.subreddit,
            time_range=args.time_range,
            max_queries=args.max_queries,
        )
    except ValueError as exc:
        parser.error(str(exc))

    if args.json:
        print(json.dumps({"queries": queries}, ensure_ascii=False, indent=2))
    else:
        print("\n".join(queries))


if __name__ == "__main__":
    main()
