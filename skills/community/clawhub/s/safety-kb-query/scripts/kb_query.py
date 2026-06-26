# -*- coding: utf-8 -*-
"""
safety-kb-query: Safety Review Knowledge Base Query Tool
==========================================================
A unified CLI tool for querying the safety-review knowledge base (SQLite).
Supports multiple query modes, auto schema detection, and formatted output.

Usage:
  python kb_query.py search <keyword> [--mode fuzzy|exact] [--limit N]
  python kb_query.py check <standard_numbers...>
  python kb_query.py info <regulation_id>
  python kb_query.py clauses <regulation_id> [--filter <keyword>]
  python kb_query.py stats
  python kb_query.py schema
  python kb_query.py conflicts

Examples:
  python kb_query.py search GB16423
  python kb_query.py check GB16423 AQ2033 "国发23号"
  python kb_query.py info 94
  python kb_query.py stats
"""

import sqlite3
import sys
import json
import os
import argparse
from datetime import datetime

# Default knowledge database path (can be overridden via KB_PATH env var)
DEFAULT_DB_PATH = os.path.expanduser(
    r"~\.openclaw-autoclaw\skills\safety-review\db\knowledge.db"
)


def get_connection(db_path=None):
    """Connect to knowledge base with proper settings."""
    path = db_path or os.environ.get("KB_PATH", DEFAULT_DB_PATH)
    if not os.path.exists(path):
        print(f"ERROR: Database not found at {path}", file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def detect_schema(conn):
    """Detect table structure and return column names for key tables."""
    schema = {}
    for table in ["regulations", "clauses", "std_registry", "books"]:
        try:
            cursor = conn.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]
            schema[table] = columns
        except sqlite3.OperationalError:
            schema[table] = []
    return schema


def cmd_search(args):
    """Search regulations by keyword."""
    conn = get_connection()
    schema = detect_schema(conn)

    # Determine searchable columns
    reg_cols = schema.get("regulations", [])
    search_cols = []
    for col in ["title", "document_number", "keywords", "full_text"]:
        if col in reg_cols:
            search_cols.append(col)

    keyword = args.keyword
    mode = args.mode
    limit = args.limit

    if mode == "exact":
        where_clauses = [f"({c} = ?)" for c in search_cols[:3]]  # Only title/doc_no/keywords for exact
        params = tuple([keyword] * len(where_clauses))
        sql = f"SELECT id, document_number, title, status FROM regulations WHERE {' OR '.join(where_clauses)} LIMIT ?"
        params += (limit,)
    else:
        where_clauses = [f"({c} LIKE ?)" for c in search_cols]
        params = tuple([f"%{keyword}%"] * len(where_clauses))
        sql = f"SELECT id, document_number, title, status FROM regulations WHERE {' OR '.join(where_clauses)} LIMIT ?"
        params += (limit,)

    rows = conn.execute(sql, params).fetchall()

    result = {
        "query": keyword,
        "mode": mode,
        "count": len(rows),
        "results": [
            {
                "id": r["id"],
                "document_number": r["document_number"],
                "title": r["title"][:80] if r["title"] else "",
                "status": r["status"],
            }
            for r in rows
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    conn.close()


def cmd_check(args):
    """Check which standards from a list exist in the knowledge base."""
    conn = get_connection()
    schema = detect_schema(conn)
    reg_cols = schema.get("regulations", [])

    targets = args.standards
    results = []

    for target in targets:
        # Try multiple columns for matching
        found = False
        for col in ["document_number", "title"]:
            if col not in reg_cols:
                continue
            row = conn.execute(
                f"SELECT id, document_number, title, status, length(full_text) as text_len "
                f"FROM regulations WHERE [{col}] LIKE ? LIMIT 1",
                (f"%{target}%",),
            ).fetchone()

            if row:
                clause_count = conn.execute(
                    "SELECT COUNT(*) as cnt FROM clauses WHERE regulation_id=?", (row["id"],)
                ).fetchone()["cnt"]

                results.append({
                    "query": target,
                    "found": True,
                    "match_column": col,
                    "id": row["id"],
                    "document_number": row["document_number"],
                    "title": (row["title"] or "")[:60],
                    "status": row["status"],
                    "text_length": row["text_len"] or 0,
                    "clause_count": clause_count,
                })
                found = True
                break

        if not found:
            results.append({
                "query": target,
                "found": False,
                "match_column": None,
                "id": None,
                "document_number": None,
                "title": None,
                "status": None,
                "text_length": 0,
                "clause_count": 0,
            })

    output = {"checked": len(targets), "found": sum(1 for r in results if r["found"]), "missing": sum(1 for r in results if not r["found"]), "results": results}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    conn.close()


def cmd_info(args):
    """Get detailed info about a specific regulation."""
    conn = get_connection()
    reg_id = args.regulation_id

    row = conn.execute("SELECT * FROM regulations WHERE id=?", (reg_id,)).fetchone()
    if not row:
        print(json.dumps({"error": f"Regulation ID {reg_id} not found"}, ensure_ascii=False))
        conn.close()
        return

    clause_count = conn.execute(
        "SELECT COUNT(*) as cnt FROM clauses WHERE regulation_id=?", (reg_id,)
    ).fetchone()["cnt"]

    # Get std_registry info if available
    std_info = None
    doc_no = row["document_number"]
    if doc_no:
        std_row = conn.execute(
            "SELECT * FROM std_registry WHERE standard_no LIKE ? LIMIT 1",
            (f"{doc_no.split()[0]}%",) if doc_no and " " in doc_no else (f"%{doc_no}%",),
        ).fetchone()
        if std_info is None:
            pass
        if std_row:
            std_info = dict(std_row)

    info = dict(row)
    info["clause_count"] = clause_count
    info["std_registry"] = std_info

    # Remove full_text to keep output manageable (it can be huge)
    if info.get("full_text") and len(info["full_text"]) > 500:
        info["full_text_preview"] = info["full_text"][:500] + "...(truncated)"
        del info["full_text"]

    print(json.dumps(info, ensure_ascii=False, indent=2, default=str))
    conn.close()


def cmd_clauses(args):
    """Query clauses for a regulation."""
    conn = get_connection()
    reg_id = args.regulation_id
    filter_kw = args.filter

    if filter_kw:
        rows = conn.execute(
            "SELECT id, article_number, content, chapter FROM clauses "
            "WHERE regulation_id=? AND content LIKE ? ORDER BY id",
            (reg_id, f"%{filter_kw}%"),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, article_number, content, chapter FROM clauses "
            "WHERE regulation_id=? ORDER BY id LIMIT 50",
            (reg_id,),
        ).fetchall()

    result = {
        "regulation_id": reg_id,
        "filter": filter_kw,
        "count": len(rows),
        "clauses": [
            {
                "id": r["id"],
                "article_number": r["article_number"],
                "content": (r["content"] or "")[:200],
                "chapter": r["chapter"],
            }
            for r in rows
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    conn.close()


def cmd_stats(_args):
    """Show overall statistics of the knowledge base."""
    conn = get_connection()

    reg_total = conn.execute("SELECT COUNT(*) FROM regulations").fetchone()[0]
    clause_total = conn.execute("SELECT COUNT(*) FROM clauses").fetchone()[0]
    book_total = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]

    # Status breakdown
    status_rows = conn.execute(
        "SELECT status, COUNT(*) as cnt FROM regulations GROUP BY status"
    ).fetchall()

    # Domain breakdown
    domain_rows = None
    try:
        domain_rows = conn.execute(
            "SELECT domains, COUNT(*) as cnt FROM regulations GROUP BY domains"
        ).fetchall()
    except sqlite3.OperationalError:
        pass

    stats = {
        "total_regulations": reg_total,
        "total_clauses": clause_total,
        "total_books": book_total,
        "status_breakdown": [dict(r) for r in status_rows],
        "domain_breakdown": [dict(r) for r in domain_rows] if domain_rows else [],
        "queried_at": datetime.now().isoformat(),
    }
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    conn.close()


def cmd_schema(_args):
    """Print detected schema information."""
    conn = get_connection()
    schema = detect_schema(conn)

    # Also get table list
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()

    output = {"tables": [t["name"] for t in tables], "columns": schema}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    conn.close()


def cmd_conflicts(_args):
    """Detect potential data quality issues in the knowledge base."""
    conn = get_connection()
    issues = []

    # 1. Regulations with empty or very short full_text
    rows = conn.execute(
        "SELECT id, document_number, title, length(full_text) as len "
        "FROM regulations WHERE full_text IS NULL OR length(full_text) < 100"
    ).fetchall()
    for r in rows:
        issues.append({"type": "empty_content", "severity": "high", "id": r["id"], "doc_no": r["document_number"], "title": (r["title"] or "")[:40], "text_len": r["len"]})

    # 2. Regulations with no clauses
    rows = conn.execute(
        "SELECT r.id, r.document_number, r.title, "
        "(SELECT COUNT(*) FROM clauses c WHERE c.regulation_id=r.id) as cc "
        "FROM regulations r WHERE cc = 0"
    ).fetchall()
    for r in rows:
        issues.append({"type": "no_clauses", "severity": "medium", "id": r["id"], "doc_no": r["document_number"], "title": (r["title"] or "")[:40], "clause_count": 0})

    # 3. Potential mislabeled records (title doesn't match document_number pattern)
    rows = conn.execute(
        "SELECT id, document_number, title FROM regulations "
        "WHERE document_number IS NOT NULL AND document_number != ''"
    ).fetchall()
    for r in rows:
        doc_no = r["document_number"]
        title = r["title"] or ""
        # Simple heuristic: if doc_no contains GB/AQ but title doesn't mention it
        keywords_in_docno = []
        for kw in ["GB", "AQ", "矿山", "安全", "规程"]:
            if kw in (doc_no or ""):
                keywords_in_docno.append(kw)
        if keywords_in_docno and not any(kw in title for kw in keywords_in_docno):
            issues.append({
                "type": "mismatch_title_docno",
                "severity": "high",
                "id": r["id"],
                "doc_no": doc_no,
                "title": title[:50],
                "hint": f"Document number contains {keywords_in_docno} but title does not",
            })

    output = {"total_issues": len(issues), "issues": issues}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Safety Review Knowledge Base Query Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # search
    p_search = subparsers.add_parser("search", help="Search regulations by keyword")
    p_search.add_argument("keyword", help="Search keyword")
    p_search.add_argument("--mode", choices=["fuzzy", "exact"], default="fuzzy", help="Match mode (default: fuzzy)")
    p_search.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    p_search.set_defaults(func=cmd_search)

    # check
    p_check = subparsers.add_parser("check", help="Check if standards exist in KB")
    p_check.add_argument("standards", nargs="+", help="Standard numbers or names to check")
    p_check.set_defaults(func=cmd_check)

    # info
    p_info = subparsers.add_parser("info", help="Get detailed info about a regulation")
    p_info.add_argument("regulation_id", type=int, help="Regulation ID")
    p_info.set_defaults(func=cmd_info)

    # clauses
    p_clauses = subparsers.add_parser("clauses", help="Query clauses of a regulation")
    p_clauses.add_argument("regulation_id", type=int, help="Regulation ID")
    p_clauses.add_argument("--filter", default=None, help="Filter clauses by keyword")
    p_clauses.set_defaults(func=cmd_clauses)

    # stats
    p_stats = subparsers.add_parser("stats", help="Show knowledge base statistics")
    p_stats.set_defaults(func=cmd_stats)

    # schema
    p_schema = subparsers.add_parser("schema", help="Show database schema")
    p_schema.set_defaults(func=cmd_schema)

    # conflicts
    p_conflicts = subparsers.add_parser("conflicts", help="Detect data quality issues")
    p_conflicts.set_defaults(func=cmd_conflicts)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
