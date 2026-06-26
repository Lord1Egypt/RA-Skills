#!/usr/bin/env python3
"""One-shot backfill: derive ``feedback_pairs.sender_type`` for historical rows.

Phase 1 of per-persona adapters added the column with NULL on existing
rows. This script joins each NULL-sender_type feedback_pair to its linked
``reply_pairs.inbound_author`` and classifies, so historical pairs aren't
left "unclassified" forever (which would mean they never contribute to a
per-persona cohort's training data in Phase 2).

Idempotent: only touches rows where ``sender_type IS NULL``. Safe to
re-run; subsequent calls do nothing.

Rows whose ``reply_pair_id`` is NULL (or whose linked reply_pair is gone,
or has no inbound_author) stay NULL — there's nothing to classify from.
Downstream consumers treat NULL as the "unknown" cohort.

Usage:
    python3 scripts/backfill_feedback_sender_type.py            # backfill active instance
    python3 scripts/backfill_feedback_sender_type.py --dry-run  # report counts only
    python3 scripts/backfill_feedback_sender_type.py --db /path # explicit DB path
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from collections import Counter
from pathlib import Path

# Allow running as script from repo root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.sender import classify_sender  # noqa: E402
from app.core.settings import get_settings  # noqa: E402
from app.db.bootstrap import resolve_sqlite_path  # noqa: E402


def backfill_sender_types(db_path: Path, *, dry_run: bool = False) -> dict[str, int]:
    """Return a Counter-style dict of {sender_type: backfilled_count, "skipped": N}."""
    if not db_path.exists():
        return {"error_db_missing": 1}

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        cols = {row[1] for row in conn.execute("PRAGMA table_info(feedback_pairs)").fetchall()}
        if "sender_type" not in cols:
            # Pre-migration DB — nothing to backfill yet. Bootstrap should
            # have added the column already; bail loudly so the user runs
            # `youos bootstrap` first.
            return {"error_column_missing": 1}

        # Pull every NULL-sender_type row that has a reply_pair_id we can
        # resolve. LEFT JOIN so rows with a stale/missing reply_pair are
        # surfaced (left as NULL — there's nothing to classify from).
        rows = conn.execute(
            """
            SELECT fp.id AS fp_id, rp.inbound_author AS inbound_author
            FROM feedback_pairs fp
            LEFT JOIN reply_pairs rp ON fp.reply_pair_id = rp.id
            WHERE fp.sender_type IS NULL
            """
        ).fetchall()

        counts: Counter[str] = Counter()
        updates: list[tuple[str, int]] = []
        for row in rows:
            if not row["inbound_author"]:
                counts["skipped_no_inbound_author"] += 1
                continue
            st = classify_sender(row["inbound_author"])
            updates.append((st, row["fp_id"]))
            counts[st] += 1

        if not dry_run and updates:
            conn.executemany(
                "UPDATE feedback_pairs SET sender_type = ? WHERE id = ?",
                updates,
            )
            conn.commit()

        return dict(counts)
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill feedback_pairs.sender_type")
    parser.add_argument(
        "--db",
        type=str,
        default=None,
        help="Path to SQLite DB (defaults to active instance's DB)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Count what would be backfilled, but don't write",
    )
    args = parser.parse_args()

    if args.db:
        db_path = Path(args.db).expanduser().resolve()
    else:
        db_path = resolve_sqlite_path(get_settings().database_url)

    print(f"Backfilling sender_type for feedback_pairs in {db_path}")
    if args.dry_run:
        print("  (dry-run: no writes)")

    counts = backfill_sender_types(db_path, dry_run=args.dry_run)
    if "error_db_missing" in counts:
        print(f"  ERROR: DB not found at {db_path}")
        sys.exit(1)
    if "error_column_missing" in counts:
        print("  ERROR: feedback_pairs.sender_type column missing — run `youos bootstrap` first")
        sys.exit(1)

    total = sum(v for k, v in counts.items() if k != "skipped_no_inbound_author")
    skipped = counts.get("skipped_no_inbound_author", 0)
    print(f"  Classified: {total}")
    for st in ("internal", "external_client", "personal", "automated", "unknown"):
        if st in counts:
            print(f"    {st}: {counts[st]}")
    if skipped:
        print(f"  Skipped (no linked inbound_author): {skipped}")
    print("Done." if not args.dry_run else "Dry run complete — re-run without --dry-run to apply.")


if __name__ == "__main__":
    main()
