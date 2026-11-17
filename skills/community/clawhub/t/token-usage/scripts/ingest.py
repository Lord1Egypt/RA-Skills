#!/usr/bin/env python3
"""Incremental token usage ingestion into SQLite.

Only processes new or modified session files since last run.
Tracks state in `ingestion_log` table.
"""

import json
import gzip
import sqlite3
import argparse
import re
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
from common import find_sessions as find_shared_sessions, parse_session as parse_shared_session, normalize_model, estimate_cost as estimate_shared_cost, local_date, _zstd_open

DB_PATH = Path(__file__).parent / "usage.db"
SESSION_PATHS = [
    Path.home() / ".openclaw" / "agents" / "main" / "sessions",
    Path.home() / ".openclaw" / "agents" / "sub" / "sessions",
]


def init_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS daily_totals (
            date TEXT,
            model TEXT,
            job_type TEXT,
            input_tokens INTEGER DEFAULT 0,
            output_tokens INTEGER DEFAULT 0,
            cache_read_tokens INTEGER DEFAULT 0,
            cache_write_tokens INTEGER DEFAULT 0,
            messages INTEGER DEFAULT 0,
            cost_usd REAL DEFAULT 0.0,
            PRIMARY KEY (date, model, job_type)
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS monthly_totals (
            month TEXT,
            model TEXT,
            job_type TEXT,
            input_tokens INTEGER DEFAULT 0,
            output_tokens INTEGER DEFAULT 0,
            messages INTEGER DEFAULT 0,
            cost_usd REAL DEFAULT 0.0,
            PRIMARY KEY (month, model, job_type)
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS ingestion_log (
            session_file TEXT PRIMARY KEY,
            file_mtime REAL,
            bytes_processed INTEGER,
            records_ingested INTEGER,
            ingested_at TEXT
        )
    """)
    
    conn.commit()
    conn.close()


def load_pricing():
    pricing_file = Path(__file__).parent / "pricing.json"
    if pricing_file.exists():
        with open(pricing_file) as f:
            return json.load(f)
    return {}


def find_sessions():
    return find_shared_sessions()


def classify_session(path):
    """Return job_type: 'user', 'cron:<name>', 'background:codex', or 'background'."""
    path_str = str(path)
    # Codex app-server rollouts are always background work, not user sessions.
    if "codex-home/sessions" in path_str:
        return "background:codex"
    if path_str.endswith(".zst"):
        open_fn = _zstd_open
    elif path_str.endswith(".gz"):
        open_fn = gzip.open
    else:
        open_fn = open
    try:
        with open_fn(path, "rt", encoding="utf-8", errors="replace") as f:
            # Scan up to the first N user messages for the [cron:...] marker.
            # The marker is injected into the session context but is NOT always
            # in the very first user message (which may be empty or an image).
            # Limit the scan so we don't read an entire large session just to
            # classify it.
            user_msgs_seen = 0
            MAX_USER_MSGS = 20
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if msg.get("type") != "message":
                    continue
                m = msg.get("message", {})
                if m.get("role") != "user":
                    continue
                user_msgs_seen += 1
                if user_msgs_seen > MAX_USER_MSGS:
                    break
                content = m.get("content", [])
                text = ""
                if isinstance(content, str):
                    # Plain-string content (e.g. cron system-prompt injections).
                    text = content
                else:
                    for c in content:
                        if isinstance(c, dict) and c.get("type") == "text":
                            text += c.get("text", "")

                # Detect cron
                match = re.search(r'\[cron:([a-f0-9\-]+)\s+([^\]]+)\]', text)
                if match:
                    return f"cron:{match.group(2).strip()}"
                match2 = re.search(r'\[cron:([a-z0-9\-]+)\s+([^\]]+)\]', text)
                if match2:
                    return f"cron:{match2.group(2).strip()}"

                # Detect background
                if "bg:" in str(path) or "background" in text.lower():
                    return "background"

            # No marker found in the scanned window — treat as interactive.
            return "user"
    except Exception:
        pass
    return "user"


def parse_session(path):
    """Yield (date, model, usage_dict, job_type) for each assistant message."""
    job_type = classify_session(path)
    for ts, model, usage in parse_shared_session(path):
        date = local_date(ts)
        yield date, model, usage, job_type


def estimate_cost(usage, model, pricing):
    return shared_cost if (shared_cost := estimate_shared_cost(usage, normalize_model(model), pricing)) is not None else 0.0


def ingest(sessions, db_path, pricing):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Get already processed files
    c.execute("SELECT session_file, file_mtime FROM ingestion_log")
    processed = {row[0]: row[1] for row in c.fetchall()}
    
    total_new = 0
    total_updated = 0
    
    for spath in sessions:
        spath_str = str(spath)
        mtime = spath.stat().st_mtime
        
        if spath_str in processed:
            if processed[spath_str] >= mtime:
                continue
            total_updated += 1
        else:
            total_new += 1
        
        # Aggregate this session
        by_key = defaultdict(lambda: {
            "input": 0, "output": 0, "cache_read": 0, "cache_write": 0, "messages": 0, "cost": 0.0
        })
        
        records = 0
        for date, model, usage, job_type in parse_session(spath):
            key = (date, model, job_type)
            d = by_key[key]
            d["input"] += usage.get("input", 0)
            d["output"] += usage.get("output", 0)
            d["cache_read"] += usage.get("cacheRead", 0)
            d["cache_write"] += usage.get("cacheWrite", 0)
            d["messages"] += 1
            d["cost"] += estimate_cost(usage, model, pricing)
            records += 1
        
        # Upsert into daily_totals
        for (date, model, job_type), d in by_key.items():
            c.execute("""
                INSERT INTO daily_totals (date, model, job_type, input_tokens, output_tokens, cache_read_tokens, cache_write_tokens, messages, cost_usd)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(date, model, job_type) DO UPDATE SET
                    input_tokens = input_tokens + excluded.input_tokens,
                    output_tokens = output_tokens + excluded.output_tokens,
                    cache_read_tokens = cache_read_tokens + excluded.cache_read_tokens,
                    cache_write_tokens = cache_write_tokens + excluded.cache_write_tokens,
                    messages = messages + excluded.messages,
                    cost_usd = cost_usd + excluded.cost_usd
            """, (date, model, job_type, d["input"], d["output"], d["cache_read"], d["cache_write"], d["messages"], round(d["cost"], 6)))
        
        # Update ingestion log
        c.execute("""
            INSERT INTO ingestion_log (session_file, file_mtime, bytes_processed, records_ingested, ingested_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(session_file) DO UPDATE SET
                file_mtime = excluded.file_mtime,
                bytes_processed = excluded.bytes_processed,
                records_ingested = excluded.records_ingested,
                ingested_at = excluded.ingested_at
        """, (spath_str, mtime, spath.stat().st_size, records, datetime.now(timezone.utc).isoformat()))
    
    conn.commit()
    conn.close()
    
    return total_new, total_updated


def rotate(db_path):
    """Roll up daily data older than 90 days into monthly_totals."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Find dates to roll up
    c.execute("""
        SELECT DISTINCT substr(date, 1, 7) as month, model, job_type,
               SUM(input_tokens), SUM(output_tokens), SUM(messages), SUM(cost_usd)
        FROM daily_totals
        WHERE date < date('now', '-90 days')
        GROUP BY month, model, job_type
    """)
    
    rows = c.fetchall()
    for row in rows:
        month, model, job_type, inp, out, msgs, cost = row
        c.execute("""
            INSERT INTO monthly_totals (month, model, job_type, input_tokens, output_tokens, messages, cost_usd)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(month, model, job_type) DO UPDATE SET
                input_tokens = input_tokens + excluded.input_tokens,
                output_tokens = output_tokens + excluded.output_tokens,
                messages = messages + excluded.messages,
                cost_usd = cost_usd + excluded.cost_usd
        """, (month, model, job_type, inp, out, msgs, cost))
    
    if rows:
        c.execute("DELETE FROM daily_totals WHERE date < date('now', '-90 days')")
        c.execute("VACUUM")
        print(f"Rotated {len(rows)} daily records to monthly.")
    
    conn.commit()
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Ingest token usage into SQLite")
    parser.add_argument("--init", action="store_true", help="Initialize database schema")
    parser.add_argument("--rotate", action="store_true", help="Rotate old daily data to monthly")
    args = parser.parse_args()
    
    if args.init:
        init_db(DB_PATH)
        print(f"Initialized {DB_PATH}")
        return
    
    if args.rotate:
        rotate(DB_PATH)
        return
    
    pricing = load_pricing()
    sessions = find_sessions()
    if not sessions:
        print("No session files found.")
        return
    
    new, updated = ingest(sessions, DB_PATH, pricing)
    print(f"Ingested: {new} new files, {updated} updated files → {DB_PATH}")


if __name__ == "__main__":
    main()
