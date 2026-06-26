#!/usr/bin/env python3
"""
daily_check.py — Daily review monitoring check.

Fetches current reviews for all configured businesses, compares with stored state,
and outputs a summary of changes. Designed to be run by a cron job.

Usage:
    python3 daily_check.py [--config path/to/config.json] [--state-dir path/to/state/]

Output: JSON summary to stdout with changes detected.
"""

import sys
import os
import json
from datetime import datetime, timezone
from pathlib import Path
import importlib.util
import re

# Import fetch_reviews_places from same directory
SCRIPT_DIR = Path(__file__).parent
spec = importlib.util.spec_from_file_location("fetch_reviews_places", SCRIPT_DIR / "fetch_reviews_places.py")
fetcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetcher)


def slugify(name: str) -> str:
    """Convert business name to slug for filenames."""
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    return slug[:50]


def load_state(state_path: Path) -> dict:
    """Load existing state file or return empty state."""
    if state_path.exists():
        with open(state_path) as f:
            return json.load(f)
    return {}


def save_state(state_path: Path, state: dict):
    """Save state to file."""
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with open(state_path, 'w') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def check_business(query: str, name: str, api_key: str, state_dir: Path) -> dict:
    """Check one business and return change summary."""
    slug = slugify(name)
    state_path = state_dir / f"{slug}.json"
    old_state = load_state(state_path)
    
    # Fetch current data
    data = fetcher.fetch_reviews(query, api_key)
    
    if not data.get("place"):
        return {
            "business": name,
            "error": f"Could not find business: {query}",
            "changes": []
        }
    
    # Build result
    result = {
        "business": data["place"]["name"],
        "placeId": data["place"]["id"],
        "rating": data["rating"],
        "reviewCount": data["reviewCount"],
        "previousRating": old_state.get("rating"),
        "previousReviewCount": old_state.get("reviewCount"),
        "changes": [],
        "newReviews": [],
        "alerts": []
    }
    
    # Detect changes
    if old_state.get("rating") is not None:
        if data["rating"] != old_state["rating"]:
            delta = data["rating"] - old_state["rating"]
            direction = "up" if delta > 0 else "down"
            result["changes"].append(f"Rating {direction}: {old_state['rating']} → {data['rating']} ({delta:+.1f})")
            if delta < 0:
                result["alerts"].append({
                    "type": "rating_drop",
                    "message": f"Rating dropped from {old_state['rating']} to {data['rating']}"
                })
    
    if old_state.get("reviewCount") is not None:
        new_count = (data["reviewCount"] or 0) - (old_state.get("reviewCount") or 0)
        if new_count > 0:
            result["changes"].append(f"+{new_count} new review(s) (total: {data['reviewCount']})")
    
    # Check for negative reviews in fetched set
    for review in data.get("reviews", []):
        if review.get("rating", 5) <= 2:
            result["alerts"].append({
                "type": "negative_review",
                "author": review.get("author", "Unknown"),
                "rating": review["rating"],
                "text": review.get("text", "")[:200],
                "time": review.get("relativeTime", "")
            })
    
    # Find new reviews by comparing authors (rough — API only returns 5)
    old_authors = {r.get("author") for r in old_state.get("latestReviews", [])}
    for review in data.get("reviews", []):
        if review.get("author") not in old_authors:
            result["newReviews"].append({
                "author": review["author"],
                "rating": review["rating"],
                "text": review.get("text", "")[:200],
                "time": review.get("relativeTime", "")
            })
    
    # Update state
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    new_state = {
        "business": data["place"]["name"],
        "placeId": data["place"]["id"],
        "lastChecked": datetime.now(timezone.utc).isoformat(),
        "rating": data["rating"],
        "reviewCount": data["reviewCount"],
        "history": old_state.get("history", []),
        "latestReviews": [
            {
                "author": r["author"],
                "rating": r["rating"],
                "relativeTime": r["relativeTime"],
                "publishTime": r.get("publishTime", ""),
            }
            for r in data.get("reviews", [])
        ]
    }
    
    # Add to history if date is new
    if not new_state["history"] or new_state["history"][-1].get("date") != today:
        new_state["history"].append({
            "date": today,
            "rating": data["rating"],
            "reviewCount": data["reviewCount"]
        })
    
    # Keep last 90 days of history
    new_state["history"] = new_state["history"][-90:]
    
    save_state(state_path, new_state)
    
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Daily review monitoring check")
    parser.add_argument("--config", default=None, help="Path to config.json")
    parser.add_argument("--state-dir", default=None, help="Path to state directory")
    args = parser.parse_args()
    
    # Find config
    skill_dir = SCRIPT_DIR.parent
    config_path = Path(args.config) if args.config else skill_dir / "config.json"
    state_dir = Path(args.state_dir) if args.state_dir else skill_dir / "state"
    
    if not config_path.exists():
        print(json.dumps({"error": f"Config not found: {config_path}", "businesses": []}))
        sys.exit(1)
    
    with open(config_path) as f:
        config = json.load(f)
    
    api_key = fetcher.get_api_key()
    
    results = []
    for biz in config.get("businesses", []):
        query = biz.get("searchQuery", f"{biz['name']} {biz.get('location', '')}")
        result = check_business(query, biz["name"], api_key, state_dir)
        results.append(result)
    
    summary = {
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "businessCount": len(results),
        "totalAlerts": sum(len(r.get("alerts", [])) for r in results),
        "businesses": results
    }
    
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
