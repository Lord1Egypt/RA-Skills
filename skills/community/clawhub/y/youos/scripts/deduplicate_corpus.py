#!/usr/bin/env python3
"""Deduplicate reply_pairs and documents in the YouOS corpus.

Usage:
    python3 scripts/deduplicate_corpus.py --dry-run   # show duplicates
    python3 scripts/deduplicate_corpus.py              # remove duplicates
"""

from __future__ import annotations

import argparse
import hashlib
import sqlite3
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.core.diff import hybrid_similarity  # noqa: E402
from app.core.settings import get_settings  # noqa: E402
from app.db.bootstrap import resolve_sqlite_path  # noqa: E402


def _hash_text(text: str | None) -> str:
    return hashlib.md5((text or "").encode()).hexdigest()


def find_duplicate_reply_pairs(conn: sqlite3.Connection) -> list[int]:
    """Find duplicate reply_pairs by (source_type, source_id) or (thread_id, inbound_text hash)."""
    dupe_ids: list[int] = []

    # Duplicates by (source_type, source_id)
    rows = conn.execute(
        """
        SELECT source_type, source_id, GROUP_CONCAT(id) as ids, COUNT(*) as cnt
        FROM reply_pairs
        WHERE source_id IS NOT NULL
        GROUP BY source_type, source_id
        HAVING cnt > 1
        """
    ).fetchall()
    for row in rows:
        ids = [int(x) for x in row[2].split(",")]
        dupe_ids.extend(ids[1:])  # Keep first, remove rest

    # Duplicates by (thread_id, inbound_text hash)
    all_pairs = conn.execute("SELECT id, thread_id, inbound_text FROM reply_pairs WHERE thread_id IS NOT NULL").fetchall()
    seen: dict[tuple[str, str], int] = {}
    for pair_id, thread_id, inbound_text in all_pairs:
        key = (thread_id, _hash_text(inbound_text))
        if key in seen:
            if pair_id not in dupe_ids:
                dupe_ids.append(pair_id)
        else:
            seen[key] = pair_id

    return dupe_ids


def find_similar_reply_pairs(conn: sqlite3.Connection, threshold: float = 0.90) -> list[int]:
    """E10: Find near-duplicate reply pairs within the same thread (>90% inbound similarity).

    Within each thread, groups pairs and removes the lower-quality duplicate.
    """
    try:
        rows = conn.execute(
            "SELECT id, thread_id, inbound_text, COALESCE(quality_score, 1.0) as quality "
            "FROM reply_pairs WHERE thread_id IS NOT NULL ORDER BY thread_id, quality DESC"
        ).fetchall()
    except sqlite3.OperationalError:
        rows = conn.execute(
            "SELECT id, thread_id, inbound_text, 1.0 as quality FROM reply_pairs WHERE thread_id IS NOT NULL ORDER BY thread_id"
        ).fetchall()

    # Group by thread_id
    by_thread: dict[str, list[tuple[int, str, float]]] = {}
    for row in rows:
        tid = row[1]
        by_thread.setdefault(tid, []).append((row[0], row[2] or "", float(row[3])))

    to_remove: list[int] = []
    for _tid, pairs in by_thread.items():
        if len(pairs) <= 1:
            continue
        # Pairs sorted quality DESC; mark lower-quality ones that are near-dups of a better one
        keep_set = list(range(len(pairs)))
        for i in range(len(pairs)):
            if i not in keep_set:
                continue
            for j in range(i + 1, len(pairs)):
                if j not in keep_set:
                    continue
                sim = hybrid_similarity(pairs[i][1], pairs[j][1])
                if sim >= threshold:
                    # pairs[i] has higher quality (sorted DESC), remove pairs[j]
                    keep_set.remove(j)
                    to_remove.append(pairs[j][0])
    return to_remove


def find_duplicate_documents(conn: sqlite3.Connection) -> list[int]:
    """Find duplicate documents by (source_type, source_id)."""
    rows = conn.execute(
        """
        SELECT source_type, source_id, GROUP_CONCAT(id) as ids, COUNT(*) as cnt
        FROM documents
        WHERE source_id IS NOT NULL
        GROUP BY source_type, source_id
        HAVING cnt > 1
        """
    ).fetchall()
    dupe_ids: list[int] = []
    for row in rows:
        ids = [int(x) for x in row[2].split(",")]
        dupe_ids.extend(ids[1:])
    return dupe_ids


def deduplicate(dry_run: bool = False) -> dict[str, int]:
    settings = get_settings()
    db_path = resolve_sqlite_path(settings.database_url)
    if not db_path.exists():
        print(f"Database not found: {db_path}")
        return {"reply_pairs": 0, "documents": 0, "total": 0}

    conn = sqlite3.connect(db_path)
    try:
        dupe_pairs = find_duplicate_reply_pairs(conn)
        similar_pairs = find_similar_reply_pairs(conn)
        # Combine, avoiding double-counting
        all_pair_ids = list(set(dupe_pairs + similar_pairs))
        dupe_docs = find_duplicate_documents(conn)

        # Count unique threads among duplicate pairs
        if all_pair_ids:
            placeholders = ",".join("?" * len(all_pair_ids))
            thread_rows = conn.execute(
                f"SELECT DISTINCT thread_id FROM reply_pairs WHERE id IN ({placeholders})",
                all_pair_ids,
            ).fetchall()
            unique_threads = len(thread_rows)
        else:
            unique_threads = 0

        print(f"Found {len(dupe_pairs)} exact duplicate reply_pairs + {len(similar_pairs)} near-similar ({unique_threads} unique threads)")
        print(f"Found {len(dupe_docs)} duplicate documents")

        if dry_run:
            print("Dry run — no rows removed.")
            return {"reply_pairs": len(all_pair_ids), "documents": len(dupe_docs), "total": 0}

        removed = 0
        if all_pair_ids:
            placeholders = ",".join("?" * len(all_pair_ids))
            conn.execute(f"DELETE FROM reply_pairs WHERE id IN ({placeholders})", all_pair_ids)
            removed += len(all_pair_ids)
        if dupe_docs:
            placeholders = ",".join("?" * len(dupe_docs))
            conn.execute(f"DELETE FROM documents WHERE id IN ({placeholders})", dupe_docs)
            removed += len(dupe_docs)
        conn.commit()
        print(f"Removed {removed} rows total.")
        return {"reply_pairs": len(dupe_pairs), "documents": len(dupe_docs), "total": removed}
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Deduplicate YouOS corpus")
    parser.add_argument("--dry-run", action="store_true", help="Show duplicates without removing")
    args = parser.parse_args()
    deduplicate(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
