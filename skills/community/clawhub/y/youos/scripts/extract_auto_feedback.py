"""Extract auto-feedback pairs from your sent emails.

Compares YouOS-generated drafts against your actual replies to create
implicit training signal for fine-tuning.
"""

from __future__ import annotations

import argparse
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from app.core.diff import is_meaningfully_different
from app.core.settings import get_settings
from app.db.bootstrap import resolve_sqlite_path
from app.generation.service import DraftRequest, generate_draft

ROOT_DIR = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Extract auto-feedback from sent email reply pairs")
    p.add_argument("--days", type=int, default=1, help="Look back N days (default: 1)")
    p.add_argument("--dry-run", action="store_true", help="Show pairs without saving")
    p.add_argument("--db", type=str, default=None, help="Database path override")
    p.add_argument("--threshold", type=float, default=0.80, help="Similarity threshold (default: 0.80)")
    p.add_argument(
        "--auto-threshold",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Auto-calibrate threshold based on corpus size (default: True)",
    )
    p.add_argument(
        "--organic",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Capture organic pairs (sent emails with no YouOS draft, default: True)",
    )
    return p.parse_args()


def _get_db_path(db_override: str | None) -> Path:
    if db_override:
        return Path(db_override)
    settings = get_settings()
    return resolve_sqlite_path(settings.database_url)


def _get_unprocessed_pairs(conn: sqlite3.Connection, since: str) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT id, inbound_text, reply_text, source_type, source_id
        FROM reply_pairs
        WHERE auto_feedback_processed = 0
          AND created_ts >= ?
        ORDER BY created_ts DESC
        """,
        (since,),
    ).fetchall()


def auto_calibrate_threshold(conn: sqlite3.Connection) -> tuple[float, int]:
    """Determine similarity threshold based on corpus size.

    Returns (threshold, pair_count).
    """
    count = conn.execute("SELECT COUNT(*) FROM reply_pairs").fetchone()[0]
    if count < 100:
        return 0.65, count
    if count < 500:
        return 0.72, count
    return 0.80, count


def _capture_organic_pairs(conn: sqlite3.Connection, *, dry_run: bool = False) -> int:
    """Capture organic pairs: sent replies with no corresponding YouOS draft.

    These are emails you sent that have inbound context (replies, not fresh sends)
    but no YouOS-generated draft.
    """
    # Ensure row_factory is set for dict-style access
    conn.row_factory = sqlite3.Row

    # Ensure organic column exists
    cols = {row[1] for row in conn.execute("PRAGMA table_info(feedback_pairs)").fetchall()}
    if "organic" not in cols:
        conn.execute("ALTER TABLE feedback_pairs ADD COLUMN organic BOOLEAN DEFAULT 0")

    import re as _re

    _ACK_PATTERN = _re.compile(
        r"^\s*(ok|okay|k|sure|thanks|thank you|ty|thx|noted|got it|will do|sounds good|great|perfect|"
        r"received|ack|acknowledged|\+1|roger|copy that|understood)\s*[.!]?\s*$",
        _re.IGNORECASE,
    )

    rows = conn.execute(
        """
        SELECT rp.id, rp.inbound_text, rp.reply_text FROM reply_pairs rp
        WHERE rp.auto_feedback_processed = 0
          AND rp.id NOT IN (SELECT DISTINCT reply_pair_id FROM feedback_pairs WHERE reply_pair_id IS NOT NULL)
          AND LENGTH(rp.reply_text) >= 10
        """
    ).fetchall()

    count = 0
    for row in rows:
        reply = (row["reply_text"] or "").strip()
        # E11: skip pure acknowledgments
        if _ACK_PATTERN.match(reply):
            continue
        if dry_run:
            print(f"  [organic] pair {row['id']}: {(row['inbound_text'] or '')[:60]}...")
        else:
            conn.execute(
                """
                INSERT INTO feedback_pairs
                    (inbound_text, generated_draft, edited_reply, feedback_note, edit_distance_pct, rating, used_in_finetune, organic)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (row["inbound_text"], reply, reply, "organic pair — no YouOS draft", 0.0, 3, 0, 1),
            )
        count += 1
    return count


def extract_auto_feedback(
    *,
    days: int = 1,
    dry_run: bool = False,
    db_path: Path | None = None,
    threshold: float = 0.80,
    auto_threshold: bool = True,
    database_url: str | None = None,
    configs_dir: Path | None = None,
    organic: bool = True,
) -> dict:
    """Main extraction logic. Returns summary dict."""
    if db_path is None:
        db_path = _get_db_path(None)

    if database_url is None:
        database_url = f"sqlite:///{db_path}"
    if configs_dir is None:
        configs_dir = ROOT_DIR / "configs"

    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        # Auto-calibrate threshold based on corpus size
        if auto_threshold:
            threshold, corpus_count = auto_calibrate_threshold(conn)
            print(f"Auto-threshold: {threshold} (corpus: {corpus_count} pairs)")
        # Check if auto_feedback_processed column exists
        cols = [row[1] for row in conn.execute("PRAGMA table_info(reply_pairs)").fetchall()]
        if "auto_feedback_processed" not in cols:
            print("Error: auto_feedback_processed column missing. Run bootstrap_db.py first.")
            return {"captured": 0, "total": 0, "skipped": 0, "errors": 0}

        pairs = _get_unprocessed_pairs(conn, since)
        total = len(pairs)
        captured = 0
        skipped = 0
        errors = 0

        print(f"Found {total} unprocessed reply pairs from last {days} day(s)")

        for pair in pairs:
            pair_id = pair["id"]
            inbound = pair["inbound_text"]
            actual_reply = pair["reply_text"]

            # Generate a draft via YouOS
            try:
                response = generate_draft(
                    DraftRequest(inbound_message=inbound),
                    database_url=database_url,
                    configs_dir=configs_dir,
                )
                generated_draft = response.draft
            except Exception as exc:
                print(f"  [skip] pair {pair_id}: draft generation failed: {exc}")
                errors += 1
                continue

            # Check if meaningfully different
            if not is_meaningfully_different(generated_draft, actual_reply, threshold):
                if dry_run:
                    print(f"  [skip] pair {pair_id}: too similar (YouOS already nails it)")
                skipped += 1
                # Still mark as processed
                if not dry_run:
                    conn.execute(
                        "UPDATE reply_pairs SET auto_feedback_processed = 1 WHERE id = ?",
                        (pair_id,),
                    )
                continue

            if dry_run:
                print(f"  [capture] pair {pair_id}:")
                print(f"    inbound: {inbound[:100]}...")
                print(f"    draft:   {generated_draft[:100]}...")
                print(f"    actual:  {actual_reply[:100]}...")
            else:
                conn.execute(
                    """
                    INSERT INTO feedback_pairs
                        (inbound_text, generated_draft, edited_reply, feedback_note, rating, used_in_finetune)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (inbound, generated_draft, actual_reply, "auto-captured from sent email", 4, 0),
                )
                conn.execute(
                    "UPDATE reply_pairs SET auto_feedback_processed = 1 WHERE id = ?",
                    (pair_id,),
                )

            captured += 1

        # Organic pair capture
        organic_count = 0
        if organic:
            organic_count = _capture_organic_pairs(conn, dry_run=dry_run)
            if organic_count:
                action_label = "Would capture" if dry_run else "Captured"
                print(f"{action_label} {organic_count} organic pairs (no YouOS draft)")

        if not dry_run:
            conn.commit()

    finally:
        conn.close()

    action = "Would capture" if dry_run else "Captured"
    print(f"\n{action} {captured} new feedback pairs from {total} reply pairs")
    if skipped:
        print(f"  Skipped {skipped} near-identical pairs")
    if errors:
        print(f"  Errors: {errors} pairs failed draft generation")

    return {"captured": captured, "total": total, "skipped": skipped, "errors": errors, "organic": organic_count}


def main() -> None:
    args = parse_args()
    db_path = Path(args.db) if args.db else None
    extract_auto_feedback(
        days=args.days,
        dry_run=args.dry_run,
        db_path=db_path,
        threshold=args.threshold,
        auto_threshold=args.auto_threshold,
        organic=args.organic,
    )


if __name__ == "__main__":
    main()
