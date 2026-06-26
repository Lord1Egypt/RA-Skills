#!/usr/bin/env python3
"""Index embeddings for chunks and reply_pairs.

Processes rows with NULL embedding, stores results in DB.
Interruptible and resumable — skips already-embedded rows.

Usage:
    python3 scripts/index_embeddings.py              # index all unembedded rows
    python3 scripts/index_embeddings.py --limit 100  # index only N rows
    python3 scripts/index_embeddings.py --table reply_pairs  # only reply pairs
    python3 scripts/index_embeddings.py --dry-run    # show count of unembedded rows
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
import time
from pathlib import Path

# Allow running as script from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.embeddings import get_embedding, get_embedding_model_id, serialize_embedding
from app.core.settings import get_settings
from app.db.bootstrap import resolve_sqlite_path

BATCH_SIZE = 50


def _ensure_embedding_columns(conn: sqlite3.Connection) -> None:
    """Add embedding columns to tables that exist yet.

    Existence-guarded ALTER: on a fresh instance pre-ingest the `chunks`
    and `reply_pairs` tables don't exist, so an unconditional
    ``ALTER TABLE chunks ADD COLUMN`` would raise OperationalError and the
    indexer step in the nightly would WARN-out. We just no-op for tables
    that aren't there yet — ingestion creates them, and the next indexer
    run picks them up.

    ``embedding_model_id`` is stored alongside ``embedding`` so a future
    model swap can identify (and re-embed) rows that were written with a
    different embedding model. NULL on legacy rows means "trust as-is",
    so existing instances aren't forced to re-embed on upgrade.
    """
    existing_tables = {
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    for table in ("chunks", "reply_pairs"):
        if table not in existing_tables:
            # Table will be created by ingestion; nothing to migrate yet.
            continue
        cols = {row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
        if "embedding" not in cols:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN embedding BLOB")
            print(f"  Migrated: added embedding column to {table}")
        if "embedding_model_id" not in cols:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN embedding_model_id TEXT")
            print(f"  Migrated: added embedding_model_id column to {table}")
    conn.commit()


def _count_unembedded(conn: sqlite3.Connection, table: str) -> int:
    row = conn.execute(f"SELECT COUNT(*) FROM {table} WHERE embedding IS NULL").fetchone()
    return row[0] if row else 0


def _get_text_for_row(row: sqlite3.Row, table: str) -> str:
    if table == "chunks":
        return row["content"] or ""
    else:  # reply_pairs
        inbound = row["inbound_text"] or ""
        reply = row["reply_text"] or ""
        return f"{inbound}\n{reply}"


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    ).fetchone()
    return row is not None


def _index_table(
    conn: sqlite3.Connection,
    table: str,
    *,
    limit: int | None = None,
    dry_run: bool = False,
) -> int:
    """Index unembedded rows in a single table. Returns number of rows processed."""
    # Pre-first-ingest the chunks/reply_pairs tables don't exist yet.
    # `_ensure_embedding_columns` already no-ops in that case; mirror it
    # here so the indexer completes cleanly on a fresh instance instead
    # of erroring out the nightly's embedding step.
    if not _table_exists(conn, table):
        print(f"  {table}: table not created yet (pre-ingest)")
        return 0

    total_unembedded = _count_unembedded(conn, table)
    if dry_run:
        print(f"  {table}: {total_unembedded} unembedded rows")
        return 0

    if total_unembedded == 0:
        print(f"  {table}: all rows already embedded")
        return 0

    target = min(total_unembedded, limit) if limit else total_unembedded
    print(f"  {table}: {total_unembedded} unembedded rows, will process {target}")

    # Snapshot the model id once per run rather than re-resolving per row —
    # consistent with what _load_model() will use, and cheap.
    model_id = get_embedding_model_id()

    processed = 0
    while processed < target:
        batch_limit = min(BATCH_SIZE, target - processed)
        conn.row_factory = sqlite3.Row
        if table == "chunks":
            rows = conn.execute(
                "SELECT id, content FROM chunks WHERE embedding IS NULL LIMIT ?",
                (batch_limit,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, inbound_text, reply_text FROM reply_pairs WHERE embedding IS NULL LIMIT ?",
                (batch_limit,),
            ).fetchall()

        if not rows:
            break

        for row in rows:
            text = _get_text_for_row(row, table)
            if not text.strip():
                # Store a zero-length blob to mark as "processed but empty";
                # record model_id even for empties so stale-detection is uniform.
                conn.execute(
                    f"UPDATE {table} SET embedding = ?, embedding_model_id = ? WHERE id = ?",
                    (b"", model_id, row["id"]),
                )
                processed += 1
                continue

            try:
                emb = get_embedding(text)
                blob = serialize_embedding(emb)
                conn.execute(
                    f"UPDATE {table} SET embedding = ?, embedding_model_id = ? WHERE id = ?",
                    (blob, model_id, row["id"]),
                )
            except Exception as exc:
                print(f"  WARNING: failed to embed {table} id={row['id']}: {exc}")
                # Store empty blob to avoid infinite retry; tag with current
                # model_id so a later model swap re-tries instead of repeating
                # the same failure forever.
                conn.execute(
                    f"UPDATE {table} SET embedding = ?, embedding_model_id = ? WHERE id = ?",
                    (b"", model_id, row["id"]),
                )

            processed += 1

        conn.commit()
        pct = (processed / target) * 100
        print(f"  Embedded {processed}/{target} {table} ({pct:.1f}%)...")

    return processed


def main() -> None:
    parser = argparse.ArgumentParser(description="Index embeddings for YouOS corpus")
    parser.add_argument("--limit", type=int, default=None, help="Max rows to process")
    parser.add_argument(
        "--table",
        choices=["chunks", "reply_pairs"],
        default=None,
        help="Only process this table",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show unembedded counts without processing")
    args = parser.parse_args()

    settings = get_settings()
    db_path = resolve_sqlite_path(settings.database_url)
    if not db_path.exists():
        print(f"Database not found at {db_path}. Run bootstrap_db.py first.")
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        _ensure_embedding_columns(conn)

        tables = [args.table] if args.table else ["chunks", "reply_pairs"]
        start = time.time()
        total = 0
        for table in tables:
            total += _index_table(conn, table, limit=args.limit, dry_run=args.dry_run)

        if not args.dry_run:
            elapsed = time.time() - start
            print(f"Done. Processed {total} rows in {elapsed:.1f}s")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
