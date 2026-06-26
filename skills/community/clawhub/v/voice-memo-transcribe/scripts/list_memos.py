#!/usr/bin/env python3
"""List Apple Voice Memos from CloudRecordings.db."""
import sqlite3
import argparse
import os
from datetime import datetime, timedelta

# Apple Core Data epoch: 2001-01-01 00:00:00 UTC
APPLE_EPOCH = datetime(2001, 1, 1)

DB_PATH = os.path.expanduser(
    "~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/CloudRecordings.db"
)


def format_duration(seconds):
    if seconds is None:
        return "0:00"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def apple_to_datetime(apple_ts):
    """Convert Apple Core Data timestamp to datetime."""
    if apple_ts is None:
        return None
    return APPLE_EPOCH + timedelta(seconds=apple_ts)


def main():
    parser = argparse.ArgumentParser(description="List Apple Voice Memos")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--search", type=str, default=None)
    parser.add_argument("--after", type=str, default=None, help="YYYY-MM-DD")
    parser.add_argument("--before", type=str, default=None, help="YYYY-MM-DD")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if not os.path.exists(DB_PATH):
        print("ERROR: Database not found.")
        print("  1. Enable iCloud sync for Voice Memos (System Settings → Apple ID → iCloud)")
        print("  2. Grant Full Disk Access to your terminal app")
        return 1

    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)

    query = """
        SELECT ZENCRYPTEDTITLE, ZCUSTOMLABEL, ZDATE, ZDURATION, ZPATH
        FROM ZCLOUDRECORDING
        WHERE ZPATH IS NOT NULL
    """
    params = []

    if args.search:
        query += " AND (ZENCRYPTEDTITLE LIKE ? OR ZCUSTOMLABEL LIKE ?)"
        params.extend([f"%{args.search}%", f"%{args.search}%"])
    if args.after:
        dt = datetime.strptime(args.after, "%Y-%m-%d")
        delta = dt - APPLE_EPOCH
        query += " AND ZDATE >= ?"
        params.append(delta.total_seconds())
    if args.before:
        dt = datetime.strptime(args.before, "%Y-%m-%d")
        delta = dt - APPLE_EPOCH
        query += " AND ZDATE <= ?"
        params.append(delta.total_seconds())

    query += " ORDER BY ZDATE DESC LIMIT ? OFFSET ?"
    params.extend([args.limit, args.offset])

    try:
        rows = conn.execute(query, params).fetchall()
    except sqlite3.OperationalError as e:
        print(f"ERROR: Database query failed: {e}")
        conn.close()
        return 1
    finally:
        conn.close()

    if args.json:
        import json
        results = []
        for enc_title, label, date_val, duration, path in rows:
            ts = apple_to_datetime(date_val)
            title = enc_title or label or "Untitled"
            results.append({
                "title": title,
                "date": ts.isoformat() if ts else "Unknown",
                "duration": format_duration(duration),
                "path": path
            })
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"{'#':<4} {'Title':<30} {'Date':<20} {'Duration':<10} {'Path'}")
        print("-" * 80)
        for i, (enc_title, label, date_val, duration, path) in enumerate(rows, 1):
            ts = apple_to_datetime(date_val)
            date_str = ts.strftime("%Y-%m-%d %H:%M") if ts else "Unknown"
            title = enc_title or label or "Untitled"
            print(f"{i:<4} {title:<30} {date_str:<20} {format_duration(duration):<10} {path}")

    return 0


if __name__ == "__main__":
    exit(main())
