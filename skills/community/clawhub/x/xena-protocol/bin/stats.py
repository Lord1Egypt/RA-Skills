"""Print local scan stats from the SQLite cache. Run: `python -m bin.stats`"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

DEFAULT_DB = Path.home() / ".openclaw" / "phishing-detection" / "cache.db"


def run(db_path: Path) -> int:
    if not db_path.exists():
        print(f"no cache db at {db_path} — the skill has not run yet.")
        return 1

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        total = conn.execute("SELECT COUNT(*) AS n FROM scan_events").fetchone()["n"]
        detected = conn.execute(
            "SELECT COUNT(*) AS n FROM scan_events WHERE verdict != 'safe'"
        ).fetchone()["n"]
        reported = conn.execute(
            "SELECT COUNT(*) AS n FROM scan_events WHERE verdict = 'reported'"
        ).fetchone()["n"]

        by_category = conn.execute(
            """
            SELECT category, COUNT(*) AS n
            FROM scan_events
            WHERE category IS NOT NULL
            GROUP BY category
            ORDER BY n DESC
            """
        ).fetchall()

        recent = conn.execute(
            """
            SELECT sender, verdict, category, confidence, created_at
            FROM scan_events
            ORDER BY created_at DESC
            LIMIT 10
            """
        ).fetchall()

    print(f"OpenClaw — local scan stats  ({db_path})")
    print(f"  total scanned:  {total}")
    print(f"  detected:       {detected}")
    print(f"  reported:       {reported}")
    if by_category:
        print("  by category:")
        for row in by_category:
            print(f"    - {row['category']}: {row['n']}")
    print()
    print("recent detections:")
    for row in recent:
        print(
            f"  {row['created_at']}  {row['verdict']:10s} "
            f"conf={row['confidence'] or '-'} "
            f"{row['category'] or '-':14s} "
            f"{row['sender'] or '(unknown)'}"
        )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="Path to cache.db")
    args = parser.parse_args()
    raise SystemExit(run(args.db))


if __name__ == "__main__":
    main()
