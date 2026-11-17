#!/usr/bin/env python3
"""
Token usage breakdown by source type for Dashboard.
Returns daily aggregates for: channel sessions, thread sessions, cron jobs.
"""

import sqlite3, json, sys
from pathlib import Path
from datetime import datetime, timedelta

LEDGER_DB = Path.home() / ".openclaw/ledger.db"

def query_daily_breakdown(days: int = 30):
    """Get daily token usage breakdown by source category."""
    db = sqlite3.connect(str(LEDGER_DB))
    db.row_factory = sqlite3.Row

    # Date range
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    # Query 1: Daily breakdown by source category
    # Note: Also check session_key for ':cron:' pattern to handle legacy data
    sql = """
    WITH daily_calls AS (
        SELECT
            date(ts) as day,
            CASE
                WHEN source_kind = 'cron' OR session_key LIKE '%:cron:%' THEN 'cron'
                WHEN thread_id IS NOT NULL AND thread_id != '' THEN 'thread'
                ELSE 'channel'
            END as source_type,
            input_tokens,
            output_tokens,
            cache_read_tokens,
            cache_write_tokens,
            cost_total
        FROM calls
        WHERE ts >= date('now', '-{days} days')
          AND ts < date('now', '+1 day')
    )
    SELECT
        day,
        source_type,
        COUNT(*) as call_count,
        SUM(input_tokens) as input_tokens,
        SUM(output_tokens) as output_tokens,
        SUM(cache_read_tokens) as cache_read_tokens,
        SUM(cache_write_tokens) as cache_write_tokens,
        SUM(input_tokens + output_tokens + cache_read_tokens + cache_write_tokens) as total_tokens,
        ROUND(SUM(cost_total), 4) as cost_usd
    FROM daily_calls
    GROUP BY day, source_type
    ORDER BY day DESC, source_type
    """.format(days=days)

    rows = db.execute(sql).fetchall()

    # Query 2: Cron job details (local vs API)
    # Extract job ID from session_key for legacy records
    cron_sql = """
    SELECT
        date(ts) as day,
        COALESCE(cron_job_id, 
            CASE 
                WHEN session_key LIKE 'agent:main:cron:%' 
                THEN substr(session_key, 18, instr(substr(session_key, 18), ':') - 1)
                ELSE 'unknown'
            END
        ) as job_id,
        COUNT(*) as call_count,
        SUM(input_tokens) as input_tokens,
        SUM(output_tokens) as output_tokens,
        SUM(cache_read_tokens) as cache_read_tokens,
        SUM(cache_write_tokens) as cache_write_tokens,
        SUM(input_tokens + output_tokens + cache_read_tokens + cache_write_tokens) as total_tokens,
        ROUND(SUM(cost_total), 4) as cost_usd
    FROM calls
    WHERE (source_kind = 'cron' OR session_key LIKE '%:cron:%')
      AND ts >= date('now', '-{days} days')
    GROUP BY day, job_id
    ORDER BY day DESC, cost_usd DESC
    """.format(days=days)

    cron_rows = db.execute(cron_sql).fetchall()

    # Query 3: Summary totals
    summary_sql = """
    SELECT
        CASE
            WHEN source_kind = 'cron' OR session_key LIKE '%:cron:%' THEN 'cron'
            WHEN thread_id IS NOT NULL AND thread_id != '' THEN 'thread'
            ELSE 'channel'
        END as source_type,
        COUNT(*) as total_calls,
        SUM(input_tokens + output_tokens + cache_read_tokens + cache_write_tokens) as total_tokens,
        ROUND(SUM(cost_total), 4) as total_cost
    FROM calls
    WHERE ts >= date('now', '-{days} days')
    GROUP BY source_type
    """.format(days=days)

    summary_rows = db.execute(summary_sql).fetchall()

    db.close()

    # Format results
    result = {
        "period": {"days": days, "start": start_date, "end": end_date},
        "summary": {row["source_type"]: dict(row) for row in summary_rows},
        "daily": {},
        "cron_details": {}
    }

    # Group daily by date
    for row in rows:
        day = row["day"]
        if day not in result["daily"]:
            result["daily"][day] = {}
        result["daily"][day][row["source_type"]] = {
            "calls": row["call_count"],
            "input_tokens": row["input_tokens"],
            "output_tokens": row["output_tokens"],
            "cache_read_tokens": row["cache_read_tokens"],
            "cache_write_tokens": row["cache_write_tokens"],
            "total_tokens": row["total_tokens"],
            "cost_usd": row["cost_usd"]
        }

    # Group cron details by date
    for row in cron_rows:
        day = row["day"]
        if day not in result["cron_details"]:
            result["cron_details"][day] = []
        result["cron_details"][day].append({
            "job_id": row["job_id"],
            "calls": row["call_count"],
            "input_tokens": row["input_tokens"],
            "output_tokens": row["output_tokens"],
            "cache_read_tokens": row["cache_read_tokens"],
            "cache_write_tokens": row["cache_write_tokens"],
            "total_tokens": row["total_tokens"],
            "cost_usd": row["cost_usd"]
        })

    return result

if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    result = query_daily_breakdown(days)
    print(json.dumps(result, indent=2))
