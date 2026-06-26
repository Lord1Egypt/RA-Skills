import argparse
import json
import sqlite3
import statistics
from pathlib import Path
from typing import Any


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report YouOS ingestion health from the local SQLite corpus database.")
    parser.add_argument(
        "--db-path",
        type=Path,
        default=Path("var/youos.db"),
        help="SQLite database path. Defaults to var/youos.db.",
    )
    parser.add_argument(
        "--sample-limit",
        type=int,
        default=3,
        help="Number of recent sample rows to show per section.",
    )
    return parser


def corpus_report(db_path: Path, sample_limit: int = 3) -> dict[str, Any]:
    """Generate a corpus health report as a dict."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        pair_count = conn.execute("SELECT COUNT(*) FROM reply_pairs").fetchone()[0]
        doc_count = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]

        feedback_count = 0
        try:
            feedback_count = conn.execute("SELECT COUNT(*) FROM feedback_pairs").fetchone()[0]
        except Exception:
            pass

        # Embedding coverage
        embedding_pct = 0.0
        try:
            total_docs = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
            embedded = conn.execute("SELECT COUNT(*) FROM documents WHERE embedding IS NOT NULL").fetchone()[0]
            embedding_pct = round((embedded / total_docs * 100) if total_docs > 0 else 0.0, 1)
        except Exception:
            pass

        # Quality score distribution
        quality_scores: list[float] = []
        try:
            rows = conn.execute("SELECT quality_score FROM reply_pairs WHERE quality_score IS NOT NULL").fetchall()
            quality_scores = [float(r[0]) for r in rows]
        except Exception:
            pass

        quality_min = round(min(quality_scores), 2) if quality_scores else None
        quality_max = round(max(quality_scores), 2) if quality_scores else None
        quality_median = round(statistics.median(quality_scores), 2) if quality_scores else None

        # Top 5 senders by pair count
        top_senders: list[dict[str, Any]] = []
        try:
            rows = conn.execute(
                "SELECT email, display_name, reply_count FROM sender_profiles ORDER BY reply_count DESC LIMIT ?",
                (sample_limit if sample_limit >= 5 else 5,),
            ).fetchall()
            for r in rows:
                top_senders.append({"email": r["email"], "display_name": r["display_name"], "reply_count": r["reply_count"]})
        except Exception:
            pass

        return {
            "pair_count": pair_count,
            "doc_count": doc_count,
            "feedback_pairs": feedback_count,
            "embedding_pct": embedding_pct,
            "quality_score": {
                "min": quality_min,
                "median": quality_median,
                "max": quality_max,
            },
            "top_senders": top_senders,
        }
    finally:
        conn.close()


def main() -> None:
    args = build_parser().parse_args()
    if args.sample_limit <= 0:
        raise SystemExit("--sample-limit must be greater than 0.")
    if not args.db_path.exists():
        raise SystemExit(f"Database not found: {args.db_path}")

    connection = sqlite3.connect(args.db_path)
    connection.row_factory = sqlite3.Row
    try:
        print(f"Database: {args.db_path}")
        _print_run_summary(connection)
        _print_corpus_summary(connection)
        _print_recent_runs(connection, sample_limit=args.sample_limit)
        _print_document_samples(connection, sample_limit=args.sample_limit)
        _print_reply_pair_samples(connection, sample_limit=args.sample_limit)
        _print_feedback_summary(connection)
    finally:
        connection.close()


def _print_run_summary(connection: sqlite3.Connection) -> None:
    row = connection.execute(
        """
        SELECT
            COUNT(*) AS total_runs,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_runs,
            SUM(CASE WHEN status = 'completed_with_warnings' THEN 1 ELSE 0 END) AS warning_runs,
            SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed_runs
        FROM ingest_runs
        """
    ).fetchone()
    print("")
    print("Run summary")
    print(f"  total={row['total_runs'] or 0}")
    print(f"  completed={row['completed_runs'] or 0}")
    print(f"  completed_with_warnings={row['warning_runs'] or 0}")
    print(f"  failed={row['failed_runs'] or 0}")


def _print_corpus_summary(connection: sqlite3.Connection) -> None:
    doc_rows = connection.execute(
        """
        SELECT source_type, COUNT(*) AS row_count
        FROM documents
        GROUP BY source_type
        ORDER BY source_type
        """
    ).fetchall()
    chunk_count = connection.execute("SELECT COUNT(*) AS row_count FROM chunks").fetchone()["row_count"]
    pair_count = connection.execute("SELECT COUNT(*) AS row_count FROM reply_pairs").fetchone()["row_count"]

    print("")
    print("Corpus summary")
    for row in doc_rows:
        print(f"  documents[{row['source_type']}]={row['row_count']}")
    print(f"  chunks={chunk_count}")
    print(f"  reply_pairs={pair_count}")


def _print_recent_runs(connection: sqlite3.Connection, *, sample_limit: int) -> None:
    rows = connection.execute(
        """
        SELECT
            run_id,
            source,
            status,
            started_at,
            completed_at,
            discovered_count,
            fetched_count,
            stored_document_count,
            stored_chunk_count,
            stored_reply_pair_count,
            error_summary
        FROM ingest_runs
        ORDER BY started_at DESC
        LIMIT ?
        """,
        (sample_limit,),
    ).fetchall()
    print("")
    print("Recent runs")
    if not rows:
        print("  none")
        return
    for row in rows:
        print(
            "  "
            f"{row['run_id']} source={row['source']} status={row['status']} "
            f"discovered={row['discovered_count']} fetched={row['fetched_count']} "
            f"documents={row['stored_document_count']} chunks={row['stored_chunk_count']} "
            f"reply_pairs={row['stored_reply_pair_count']}"
        )
        print(f"  started_at={row['started_at']} completed_at={row['completed_at']}")
        if row["error_summary"]:
            print(f"  error={row['error_summary']}")


def _print_document_samples(connection: sqlite3.Connection, *, sample_limit: int) -> None:
    rows = connection.execute(
        """
        SELECT source_type, source_id, title, thread_id, created_at, metadata_json
        FROM documents
        ORDER BY id DESC
        LIMIT ?
        """,
        (sample_limit,),
    ).fetchall()
    print("")
    print("Recent documents")
    if not rows:
        print("  none")
        return
    for row in rows:
        metadata = _load_json(row["metadata_json"])
        account_email = metadata.get("account_email")
        print(
            "  "
            f"{row['source_type']} source_id={row['source_id']} title={row['title']!r} "
            f"thread_id={row['thread_id']} account={account_email} created_at={row['created_at']}"
        )


def _print_reply_pair_samples(connection: sqlite3.Connection, *, sample_limit: int) -> None:
    rows = connection.execute(
        """
        SELECT source_id, thread_id, inbound_author, reply_author, paired_at
        FROM reply_pairs
        ORDER BY id DESC
        LIMIT ?
        """,
        (sample_limit,),
    ).fetchall()
    print("")
    print("Recent reply pairs")
    if not rows:
        print("  none")
        return
    for row in rows:
        print(
            "  "
            f"{row['source_id']} thread_id={row['thread_id']} "
            f"inbound_author={row['inbound_author']!r} reply_author={row['reply_author']!r} "
            f"paired_at={row['paired_at']}"
        )


def _print_feedback_summary(connection: sqlite3.Connection) -> None:
    try:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total,
                AVG(edit_distance_pct) AS avg_edit_distance,
                MIN(edit_distance_pct) AS min_edit_distance,
                MAX(edit_distance_pct) AS max_edit_distance
            FROM feedback_pairs
            WHERE edit_distance_pct IS NOT NULL
            """
        ).fetchone()
    except Exception:
        return
    print("")
    print("Feedback summary")
    total = row["total"] or 0
    if total == 0:
        print("  no feedback pairs with edit distance data")
        return
    print(f"  pairs_with_edit_distance={total}")
    print(f"  avg_edit_distance_pct={row['avg_edit_distance']:.4f}")
    print(f"  min={row['min_edit_distance']:.4f}  max={row['max_edit_distance']:.4f}")


def _load_json(value: str) -> dict:
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


if __name__ == "__main__":
    main()
