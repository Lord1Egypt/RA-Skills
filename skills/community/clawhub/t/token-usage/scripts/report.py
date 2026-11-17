#!/usr/bin/env python3
"""Generate token usage reports from SQLite database.

Usage:
    python report.py --yesterday        # yesterday's report
    python report.py --today           # today's report so far
    python report.py --week            # last 7 days
    python report.py --month         # this month
"""

import sqlite3
import argparse
from pathlib import Path
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import sys
sys.path.insert(0, str(Path(__file__).parent))
from common import LOCAL_TZ

DB_PATH = Path(__file__).parent / "usage.db"


def get_report(db_path, since_date, until_date=None):
    """Get aggregated report for date range."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    sql = """
        SELECT date, model, job_type, input_tokens, output_tokens, cache_read_tokens, cache_write_tokens, messages, cost_usd
        FROM daily_totals
        WHERE date >= ? AND date <= ?
        ORDER BY date DESC, job_type
    """
    if until_date is None:
        until_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    c.execute(sql, (since_date, until_date))
    rows = c.fetchall()
    conn.close()
    return rows


def get_monthly_report(db_path, month):
    """Get monthly aggregated report."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute("""
        SELECT month, model, job_type, input_tokens, output_tokens, messages, cost_usd
        FROM monthly_totals
        WHERE month = ?
        ORDER BY job_type
    """, (month,))
    rows = c.fetchall()
    conn.close()
    return rows


def format_report(rows, title):
    if not rows:
        return f"## {title}\n\nNo data available."
    
    # Group by date, then by job_type
    by_day = defaultdict(lambda: defaultdict(lambda: {
        "input": 0, "output": 0, "cache": 0, "messages": 0, "cost": 0.0, "models": set()
    }))
    
    for date, model, job_type, inp, out, cache_read, cache_write, msgs, cost in rows:
        d = by_day[date][job_type]
        d["input"] += inp
        d["output"] += out
        d["cache"] += cache_read + cache_write
        d["messages"] += msgs
        d["cost"] += cost
        d["models"].add(model)
    # Add totals from the grouped rows.
    grand = {"input": 0, "output": 0, "cache": 0, "messages": 0, "cost": 0.0}
    for date, job_type, data in [(d, j, by_day[d][j]) for d in by_day for j in by_day[d]]:
        grand["input"] += data["input"]
        grand["output"] += data["output"]
        grand["cache"] += data["cache"]
        grand["messages"] += data["messages"]
        grand["cost"] += data["cost"]
    
    lines = [f"## {title}", ""]
    
    for day in sorted(by_day.keys(), reverse=True):
        lines.append(f"### {day}")
        
        day_total = {"input": 0, "output": 0, "cache": 0, "messages": 0, "cost": 0.0}
        
        # Sort by cost descending
        jobs = sorted(by_day[day].items(), key=lambda x: x[1]["cost"], reverse=True)
        
        for job_type, data in jobs:
            name = job_type if len(job_type) <= 30 else job_type[:27] + "..."
            models = ", ".join(sorted(data["models"])) if data["models"] else "unknown"
            
            lines.append(f"  {name:<30}  msgs={data['messages']:>4}  in={data['input']:>10,}  out={data['output']:>8,}  cache={data['cache']:>8,}  ${data['cost']:.4f}")
            
            for k in ["input", "output", "cache", "messages", "cost"]:
                day_total[k] += data[k]
        
        lines.append(f"  {'DAY TOTAL':<30}  msgs={day_total['messages']:>4}  in={day_total['input']:>10,}  out={day_total['output']:>8,}  cache={day_total['cache']:>8,}  ${day_total['cost']:.4f}")
        lines.append("")
    
    lines.append(f"**GRAND TOTAL**: msgs={grand['messages']:,}  in={grand['input']:,}  out={grand['output']:,}  cache={grand['cache']:,}  ${grand['cost']:.4f}")
    
    return "\n".join(lines)


def format_compact(rows, title):
    """Compact format for cron messages (Telegram-friendly)."""
    if not rows:
        return f"📊 {title}: No data"
    
    # Group by job_type only (collapse dates)
    by_job = defaultdict(lambda: {"input": 0, "output": 0, "messages": 0, "cost": 0.0})
    grand = {"input": 0, "output": 0, "messages": 0, "cost": 0.0}
    
    for date, model, job_type, inp, out, cache_read, cache_write, msgs, cost in rows:
        by_job[job_type]["input"] += inp
        by_job[job_type]["output"] += out
        by_job[job_type]["messages"] += msgs
        by_job[job_type]["cost"] += cost
        grand["input"] += inp
        grand["output"] += out
        grand["messages"] += msgs
        grand["cost"] += cost
    
    lines = [f"📊 {title}", ""]
    lines.append(f"| Type | Msgs | Input | Output | Cost |")
    lines.append(f"|------|------|-------|--------|------|")
    
    for job_type in sorted(by_job.keys(), key=lambda x: by_job[x]["cost"], reverse=True):
        d = by_job[job_type]
        name = job_type if len(job_type) <= 24 else job_type[:21] + "..."
        lines.append(f"| {name:<24} | {d['messages']:>4} | {d['input']:>10,} | {d['output']:>8,} | ${d['cost']:.4f} |")
    
    lines.append(f"| {'TOTAL':<24} | {grand['messages']:>4} | {grand['input']:>10,} | {grand['output']:>8,} | ${grand['cost']:.4f} |")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate token usage reports")
    parser.add_argument("--yesterday", action="store_true", help="Report for yesterday")
    parser.add_argument("--today", action="store_true", help="Report for today")
    parser.add_argument("--week", action="store_true", help="Report for last 7 days")
    parser.add_argument("--month", action="store_true", help="Report for this month")
    parser.add_argument("--compact", action="store_true", help="Compact format for messages")
    args = parser.parse_args()
    
    if not DB_PATH.exists():
        print("Database not found. Run `ingest.py --init` first.")
        return
    
    now = datetime.now(LOCAL_TZ)
    
    if args.yesterday:
        since = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        until = since
        title = f"Token Usage — {since}"
    elif args.today:
        since = now.strftime("%Y-%m-%d")
        until = since
        title = f"Token Usage — Today ({since})"
    elif args.week:
        since = (now - timedelta(days=7)).strftime("%Y-%m-%d")
        until = now.strftime("%Y-%m-%d")
        title = f"Token Usage — Last 7 Days ({since} to {until})"
    elif args.month:
        since = now.strftime("%Y-%m-01")
        until = now.strftime("%Y-%m-%d")
        title = f"Token Usage — This Month ({since} to {until})"
    else:
        args.yesterday = True
        since = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        until = since
        title = f"Token Usage — {since}"
    
    rows = get_report(DB_PATH, since, until)
    
    if args.compact:
        print(format_compact(rows, title))
    else:
        print(format_report(rows, title))


if __name__ == "__main__":
    main()
