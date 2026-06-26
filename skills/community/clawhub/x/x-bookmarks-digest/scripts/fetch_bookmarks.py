#!/usr/bin/env python3
"""Fetch X/Twitter bookmarks via xurl CLI with state management."""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
STATE_FILE = os.path.join(BASE_DIR, "state.json")
MIN_INTERVAL_SECS = 3600  # 1 hour


def load_state() -> dict:
    """Load state from state.json, return defaults if missing."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_bookmark_id": None, "last_run_ts": None, "processed_count": 0}


def save_state(state: dict):
    """Persist state to state.json."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def check_rate_limit(state: dict, force: bool) -> bool:
    """Return True if allowed to run, False if rate-limited."""
    if force or state["last_run_ts"] is None:
        return True

    last_run = datetime.fromisoformat(state["last_run_ts"])
    elapsed = (datetime.now(timezone.utc) - last_run).total_seconds()

    if elapsed < MIN_INTERVAL_SECS:
        remaining = int((MIN_INTERVAL_SECS - elapsed) / 60)
        print(
            json.dumps({
                "error": "rate_limited",
                "message": f"Last run was {int(elapsed / 60)} mins ago. Wait {remaining} more mins or use --force.",
                "last_run": state["last_run_ts"],
            }),
            file=sys.stderr,
        )
        return False

    return True


def fetch_bookmarks(count: int) -> list:
    """Call xurl bookmarks and return parsed JSON list."""
    try:
        result = subprocess.run(
            ["xurl", "bookmarks", "-n", str(count)],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except FileNotFoundError:
        print(json.dumps({"error": "xurl_not_found", "message": "xurl not installed. Run: brew install xurl"}), file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(json.dumps({"error": "timeout", "message": "xurl timed out after 30s"}), file=sys.stderr)
        sys.exit(1)

    if result.returncode != 0:
        stderr = result.stderr.strip()
        # Try to parse as JSON for structured error
        try:
            err = json.loads(stderr)
            status = err.get("status", result.returncode)
        except (json.JSONDecodeError, TypeError):
            status = result.returncode
            err = {"detail": stderr}

        if status == 401:
            print(json.dumps({
                "error": "unauthorized",
                "message": "xurl auth failed. Run: xurl auth apps add <app> --client-id <id> --client-secret <secret>",
            }), file=sys.stderr)
        elif status == 429:
            print(json.dumps({
                "error": "rate_limited_api",
                "message": "X API rate limit hit. Wait 15 minutes.",
            }), file=sys.stderr)
        else:
            print(json.dumps({
                "error": "xurl_error",
                "message": f"xurl failed (exit {result.returncode}): {err.get('detail', stderr)}",
            }), file=sys.stderr)
        sys.exit(1)

    # Parse xurl output
    raw = result.stdout.strip()
    if not raw:
        return []

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print(json.dumps({"error": "parse_error", "message": "Could not parse xurl output as JSON"}), file=sys.stderr)
        sys.exit(1)

    # xurl bookmarks returns {"data": [...], "meta": {...}} or just a list
    if isinstance(data, dict):
        bookmarks = data.get("data", [])
    elif isinstance(data, list):
        bookmarks = data
    else:
        bookmarks = []

    return bookmarks


def filter_new_bookmarks(bookmarks: list, last_id: str | None, fetch_all: bool) -> list:
    """Filter out already-processed bookmarks."""
    if fetch_all or last_id is None:
        return bookmarks

    new = []
    for bm in bookmarks:
        bm_id = bm.get("id", "")
        if bm_id == last_id:
            break
        new.append(bm)

    return new


def main():
    parser = argparse.ArgumentParser(description="Fetch X bookmarks via xurl")
    parser.add_argument("--count", type=int, default=50, help="Number of bookmarks to fetch (1-100)")
    parser.add_argument("--force", action="store_true", help="Skip rate limit check")
    parser.add_argument("--all", action="store_true", help="Reprocess all bookmarks (ignore last-checked ID)")
    parser.add_argument("--dry-run", action="store_true", help="Fetch but don't update state")
    args = parser.parse_args()

    args.count = max(1, min(100, args.count))

    state = load_state()

    if not check_rate_limit(state, args.force):
        sys.exit(2)

    bookmarks = fetch_bookmarks(args.count)

    if not bookmarks:
        print(json.dumps([]))
        if not args.dry_run:
            state["last_run_ts"] = datetime.now(timezone.utc).isoformat()
            save_state(state)
        return

    new_bookmarks = filter_new_bookmarks(bookmarks, state["last_bookmark_id"], args.all)

    # Output new bookmarks as JSON
    print(json.dumps(new_bookmarks, indent=2))

    # Update state (unless dry run)
    if not args.dry_run and new_bookmarks:
        newest_id = bookmarks[0].get("id")  # First bookmark is newest
        if newest_id:
            state["last_bookmark_id"] = newest_id
        state["last_run_ts"] = datetime.now(timezone.utc).isoformat()
        state["processed_count"] = state.get("processed_count", 0) + len(new_bookmarks)
        save_state(state)


if __name__ == "__main__":
    main()
