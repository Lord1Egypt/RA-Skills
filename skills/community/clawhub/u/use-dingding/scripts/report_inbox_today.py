#!/usr/bin/env python3
"""
Report Inbox Today

View today's received reports with details.
Usage: python report_inbox_today.py [--date 2024-03-29]
"""

import argparse
import subprocess
import json
import sys
from datetime import datetime


def run_dws(args):
    """Run dws command and return JSON output."""
    cmd = ["dws"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def get_received_reports(date):
    """Get received reports for a specific date."""
    result = run_dws([
        "report", "list",
        "--type", "received",
        "--start-date", date,
        "--end-date", date
    ])
    if not result:
        return []
    return result.get("result", [])


def main():
    parser = argparse.ArgumentParser(description="View today's received reports")
    parser.add_argument("--date", help="Date (YYYY-MM-DD), defaults to today")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    
    args = parser.parse_args()
    
    # Use today's date if not specified
    if args.date:
        date = args.date
    else:
        date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"Received reports for {date}:\n")
    
    reports = get_received_reports(date)
    
    if not reports:
        print("No reports received today")
        sys.exit(0)
    
    if args.format == "json":
        print(json.dumps(reports, indent=2, ensure_ascii=False))
    else:  # table
        # Calculate column widths
        titles = [r.get("title", "") for r in reports]
        senders = [r.get("senderName", "") for r in reports]
        times = [r.get("createTime", "")[:16] for r in reports]
        
        title_width = max(len("Title"), max(len(t) for t in titles) if titles else 0)
        sender_width = max(len("Sender"), max(len(s) for s in senders) if senders else 0)
        time_width = max(len("Time"), max(len(t) for t in times) if times else 0)
        
        print(f"{'Title':<{title_width}} | {'Sender':<{sender_width}} | {'Time':<{time_width}} | Status")
        print("-" * (title_width + sender_width + time_width + 15))
        
        for report in reports:
            title = report.get("title", "")[:50]  # Truncate long titles
            sender = report.get("senderName", "Unknown")
            time = report.get("createTime", "")[:16]
            status = report.get("status", "")
            print(f"{title:<{title_width}} | {sender:<{sender_width}} | {time:<{time_width}} | {status}")
    
    print(f"\nTotal: {len(reports)} report(s)")


if __name__ == "__main__":
    main()
