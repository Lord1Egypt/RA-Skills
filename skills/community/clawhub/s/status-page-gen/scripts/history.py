#!/usr/bin/env python3
"""
history.py — Track uptime history and compute uptime percentages.

Appends check results to a rolling JSON log file.
Computes uptime percentages over 24h, 7d, and 30d windows.

Usage:
    # Append a check result to history
    python3 history.py --append /tmp/status_check.json --db assets/history.json

    # Query uptime stats (outputs JSON)
    python3 history.py --stats --db assets/history.json

    # Prune old entries (keep last N days)
    python3 history.py --prune 30 --db assets/history.json
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone


DEFAULT_DB = "assets/history.json"
DEFAULT_RETENTION_DAYS = 90


def load_db(db_path: str) -> dict:
    """Load the history database. Creates empty structure if not found."""
    if os.path.exists(db_path):
        with open(db_path) as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(
                    f"WARNING: History DB is corrupt, starting fresh: {db_path}",
                    file=sys.stderr,
                )
    return {"entries": []}


def save_db(db: dict, db_path: str) -> None:
    """Save the history database."""
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    with open(db_path, "w") as f:
        json.dump(db, f, indent=2)


def parse_iso(ts: str) -> datetime:
    """Parse an ISO 8601 timestamp to an aware UTC datetime."""
    # Python 3.7+ handles most formats; normalize trailing Z
    ts = ts.replace("Z", "+00:00")
    return datetime.fromisoformat(ts)


def append_check(check_path: str, db_path: str) -> None:
    """Append a check_services.py result to the history log."""
    if not os.path.exists(check_path):
        print(f"ERROR: Check file not found: {check_path}", file=sys.stderr)
        sys.exit(1)

    with open(check_path) as f:
        try:
            check_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in check file: {e}", file=sys.stderr)
            sys.exit(1)

    checked_at = check_data.get("checked_at", datetime.now(timezone.utc).isoformat())

    # Build a compact entry per service
    entry = {
        "ts": checked_at,
        "services": {},
    }

    for svc in check_data.get("services", []):
        name = svc.get("name", "?")
        entry["services"][name] = {
            "status": svc.get("status", "unknown"),
            "response_time_ms": svc.get("http", {}).get("response_time_ms"),
        }

    db = load_db(db_path)
    db["entries"].append(entry)
    save_db(db, db_path)

    print(
        f"Appended entry for {checked_at} ({len(entry['services'])} services) → {db_path}",
        file=sys.stderr,
    )


def compute_uptime(entries: list, service_name: str, window_hours: int) -> float | None:
    """
    Compute uptime percentage for a service over the past N hours.
    Returns a float 0–100, or None if no data in window.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
    in_window = [
        e for e in entries if parse_iso(e["ts"]) >= cutoff
    ]

    if not in_window:
        return None

    up_count = 0
    total = 0

    for entry in in_window:
        svc_data = entry.get("services", {}).get(service_name)
        if svc_data is None:
            continue
        total += 1
        if svc_data.get("status") == "up":
            up_count += 1

    if total == 0:
        return None

    return round((up_count / total) * 100, 2)


def get_stats(db_path: str) -> dict:
    """Compute uptime stats for all services over 24h, 7d, 30d."""
    db = load_db(db_path)
    entries = db.get("entries", [])

    if not entries:
        return {"error": "No history data available", "services": {}}

    # Collect all unique service names
    all_names: set = set()
    for entry in entries:
        all_names.update(entry.get("services", {}).keys())

    stats = {}
    for name in sorted(all_names):
        stats[name] = {
            "uptime_24h": compute_uptime(entries, name, 24),
            "uptime_7d": compute_uptime(entries, name, 24 * 7),
            "uptime_30d": compute_uptime(entries, name, 24 * 30),
        }

    return {
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "total_entries": len(entries),
        "oldest_entry": min(e["ts"] for e in entries),
        "newest_entry": max(e["ts"] for e in entries),
        "services": stats,
    }


def prune_old_entries(db_path: str, retain_days: int) -> None:
    """Remove entries older than retain_days from the history log."""
    db = load_db(db_path)
    cutoff = datetime.now(timezone.utc) - timedelta(days=retain_days)

    before = len(db["entries"])
    db["entries"] = [
        e for e in db["entries"] if parse_iso(e["ts"]) >= cutoff
    ]
    after = len(db["entries"])

    save_db(db, db_path)
    print(
        f"Pruned {before - after} entries older than {retain_days}d. "
        f"Remaining: {after}",
        file=sys.stderr,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Track uptime history and compute uptime percentages."
    )
    parser.add_argument(
        "--db",
        default=DEFAULT_DB,
        help=f"Path to history database (default: {DEFAULT_DB})",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--append",
        metavar="CHECK_JSON",
        help="Append a check_services.py result file to history",
    )
    group.add_argument(
        "--stats",
        action="store_true",
        help="Print uptime statistics as JSON",
    )
    group.add_argument(
        "--prune",
        type=int,
        metavar="DAYS",
        help=f"Remove entries older than N days (default: {DEFAULT_RETENTION_DAYS})",
    )

    parser.add_argument(
        "--output",
        default=None,
        help="Write stats JSON to this file instead of stdout (--stats only)",
    )

    args = parser.parse_args()

    if args.append:
        append_check(args.append, args.db)

    elif args.stats:
        stats = get_stats(args.db)
        output_json = json.dumps(stats, indent=2)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output_json)
        else:
            print(output_json)

    elif args.prune is not None:
        prune_old_entries(args.db, args.prune)


if __name__ == "__main__":
    main()
