#!/usr/bin/env python3
"""
storage_find.py - Universal fast search across indexed code, documents, and text files.
Uses SQLite FTS5 with BM25 ranking and bulletproof query sanitization.

Usage:
  python3 storage_find.py "<query>" [--db /path/to/db] [--limit 10] [--type code|docs|all]
"""

import json
import os
import re
import sys
import sqlite3
from pathlib import Path

DEFAULT_LOCAL_DBS = [
    Path("./storage_rag.db"),
    Path("./.openclaw/storage_rag.db"),
]

CONFIG_PATH = Path.home() / ".config" / "smart-storage-triage" / "config.json"
RESERVED_FTS_KEYWORDS = {"AND", "OR", "NOT", "NEAR"}

def find_database(custom_path=None):
    if custom_path and Path(custom_path).exists():
        return Path(custom_path)
    env_db = os.environ.get("STORAGE_RAG_DB")
    if env_db and Path(env_db).exists():
        return Path(env_db)
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                cfg_db = cfg.get("default_db")
                if cfg_db and Path(cfg_db).exists():
                    return Path(cfg_db)
        except Exception:
            pass
    for p in DEFAULT_LOCAL_DBS:
        if p.exists():
            return p
    return None

def sanitize_fts_query(q: str) -> str:
    """Bulletproof sanitizer for FTS5 queries.
    Prevents syntax crashes from colons, asterisks, unbalanced quotes,
    parentheses, percentages, and reserved boolean operators.
    """
    clean_q = q.replace("\\", "/")
    raw_tokens = re.findall(r'"[^"]+"|[^\s"()\[\]{}%*+^~;]+', clean_q)
    tokens = []

    for t in raw_tokens:
        t = t.strip()
        if not t:
            continue
        if t.startswith('"') and t.endswith('"'):
            inner = t[1:-1].strip()
            if inner:
                tokens.append(f'"{inner}"')
        else:
            if t.upper() in RESERVED_FTS_KEYWORDS:
                continue
            t = re.sub(r"^[:,\.]+|[:,\.]+$", "", t)
            if not t:
                continue
            if any(c in t for c in "-/.:@_"):
                tokens.append(f'"{t}"')
            else:
                tokens.append(t)

    return " ".join(tokens) if tokens else re.sub(r'[^\w\s]', ' ', q).strip()

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        sys.exit(0)

    query = sys.argv[1].strip()
    if not query:
        print("❌ Search query cannot be empty.")
        sys.exit(1)

    db_path = None
    limit = 10
    filter_type = "all"

    idx = 2
    while idx < len(sys.argv):
        arg = sys.argv[idx]
        if arg == "--db" and idx + 1 < len(sys.argv):
            db_path = sys.argv[idx + 1]
            idx += 2
        elif arg == "--limit" and idx + 1 < len(sys.argv):
            try:
                limit = int(sys.argv[idx + 1])
            except ValueError:
                pass
            idx += 2
        elif arg == "--type" and idx + 1 < len(sys.argv):
            filter_type = sys.argv[idx + 1].lower()
            idx += 2
        else:
            idx += 1

    resolved_db = find_database(db_path)
    if not resolved_db:
        print("❌ Search index database not found.")
        print("💡 Run 'python3 triage_index.py <directory>' to build an index for your project or drive.")
        sys.exit(1)

    conn = sqlite3.connect(str(resolved_db))
    c = conn.cursor()

    tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    table_name = "chunks_fts" if "chunks_fts" in tables else "files_fts"

    if table_name not in tables:
        print(f"❌ Full-text index table not found in {resolved_db}")
        sys.exit(1)

    cols = [r[1] for r in c.execute(f"PRAGMA table_info({table_name})").fetchall()]
    has_page = "page_num" in cols
    has_rel = "rel_path" in cols

    page_col = "page_num" if has_page else "1"
    rel_col = "rel_path" if has_rel else "file_name"

    sql = f"""
        SELECT file_name, {rel_col}, {page_col}, snippet({table_name}, 0, '<b>', '</b>', '...', 25), rank
        FROM {table_name}
        WHERE {table_name} MATCH ?
        ORDER BY rank
        LIMIT ?
    """

    safe_query = sanitize_fts_query(query)
    rows = []

    # 1. Try strict MATCH with sanitized query
    if safe_query:
        try:
            rows = c.execute(sql, (safe_query, limit)).fetchall()
        except Exception:
            rows = []

    # 2. If strict MATCH returned 0 and query has multiple words, try OR search for soft match
    if not rows and safe_query and " " in safe_query:
        words = [w for w in safe_query.split() if w.upper() not in RESERVED_FTS_KEYWORDS]
        if len(words) > 1:
            or_query = " OR ".join(words)
            try:
                rows = c.execute(sql, (or_query, limit)).fetchall()
            except Exception:
                rows = []

    # 3. Fallback to LIKE substring search if MATCH yielded nothing
    if not rows:
        clean_kw = re.sub(r'[^\w\s-]', '', query).strip()
        if clean_kw:
            first_word = clean_kw.split()[0]
            like_sql = f"""
                SELECT file_name, {rel_col}, {page_col}, substr(content, 1, 150), 0
                FROM {table_name}
                WHERE content LIKE ?
                LIMIT ?
            """
            try:
                rows = c.execute(like_sql, (f"%{first_word}%", limit)).fetchall()
            except Exception:
                rows = []

    if not rows:
        print(f"🔍 No results found for '{query}' in {resolved_db.name}")
        return

    print(f"🎯 Found {len(rows)} matching snippet(s) in {resolved_db.name}:\n")
    for fname, rel, page, snippet, _ in rows:
        loc = f" (line/page {page})" if page and str(page) != "0" else ""
        print(f"📄 {fname}{loc}")
        print(f"   Path: {rel}")
        print(f"   Excerpt: {snippet.strip()}\n")

if __name__ == "__main__":
    main()
