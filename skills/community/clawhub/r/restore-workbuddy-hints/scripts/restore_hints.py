#!/usr/bin/env python3
"""
restore_hints.py — Restore dismissed WorkBuddy UI hints/tips.

When a user clicks "Don't show again" on an in-app tip,
WorkBuddy records it in user-state.json under tipShowHistory.
This script clears those records so dismissed hints reappear.

Usage:
    python restore_hints.py --list          List currently dismissed hints
    python restore_hints.py --all           Restore ALL dismissed hints
    python restore_hints.py --key <name>    Restore a specific hint by its key
"""

import json
import os
import sys
import argparse
from pathlib import Path


def get_user_state_path() -> Path:
    """Return the path to user-state.json."""
    home = Path(os.environ.get("USERPROFILE", os.path.expanduser("~")))
    return home / ".workbuddy" / "user-state.json"


def load_json(path: Path) -> dict:
    """Load a JSON file, return empty dict if missing."""
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict):
    """Save data as JSON to path."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  [SAVED] {path}")


def list_dismissed() -> dict:
    """List all currently dismissed hints."""
    path = get_user_state_path()
    data = load_json(path)
    history = data.get("tipShowHistory", {})

    print("=" * 56)
    print("  WorkBuddy Dismissed Hints")
    print("=" * 56)
    if not history:
        print("  (none) — No dismissed hints found")
    else:
        for i, (key, value) in enumerate(history.items(), 1):
            print(f"  [{i}] {key} = {value}")
    print("=" * 56)
    return history


def restore_all():
    """Restore all dismissed hints."""
    path = get_user_state_path()
    data = load_json(path)
    history = data.get("tipShowHistory", {})

    if not history:
        print("No dismissed hints to restore.")
        return

    count = len(history)
    data["tipShowHistory"] = {}
    save_json(path, data)
    print(f"\nRestored {count} hint(s). Restart WorkBuddy for changes to take effect.")


def restore_key(key: str):
    """Restore a specific dismissed hint by its key."""
    path = get_user_state_path()
    data = load_json(path)
    history = data.get("tipShowHistory", {})

    if key not in history:
        print(f"Hint '{key}' not found. Use --list to see available hints.")
        return

    del history[key]
    data["tipShowHistory"] = history
    save_json(path, data)
    print(f"\nRestored hint '{key}'. Restart WorkBuddy for changes to take effect.")


def main():
    parser = argparse.ArgumentParser(
        description="Restore WorkBuddy hints dismissed via 'Don't show again'"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--list", action="store_true",
        help="List all currently dismissed hints"
    )
    group.add_argument(
        "--all", action="store_true",
        help="Restore all dismissed hints"
    )
    group.add_argument(
        "--key", type=str, metavar="HINT_KEY",
        help="Restore a specific hint by its key (use --list to see keys)"
    )

    args = parser.parse_args()
    print()

    if args.list:
        list_dismissed()
    elif args.all:
        restore_all()
    elif args.key:
        restore_key(args.key)


if __name__ == "__main__":
    main()
