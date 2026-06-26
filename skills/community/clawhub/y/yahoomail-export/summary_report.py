#!/usr/bin/env python3
"""
Summary Report - Final triage summary with statistics and top emails.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

# EDIT THIS: Set your base directory for the email purge project
BASE_DIR = Path("~/email-purge").expanduser()
DB_FILE = BASE_DIR / "vectors" / "email_index.db"
REPORT_FILE = BASE_DIR / "summary_report.md"

def main():
    if not DB_FILE.exists():
        print("No database found. Run the pipeline first.")
        return
    
    conn = sqlite3.connect(str(DB_FILE))
    conn.row_factory = sqlite3.Row
    
    # Overall stats
    total = conn.execute("SELECT COUNT(*) FROM emails").fetchone()[0]
    
    by_classification = conn.execute("""
        SELECT classification, COUNT(*) as cnt
        FROM emails GROUP BY classification
    """).fetchall()
    
    by_category = conn.execute("""
        SELECT category, COUNT(*) as cnt
        FROM emails WHERE category IS NOT NULL
        GROUP BY category ORDER BY cnt DESC
    """).fetchall()
    
    by_importance = conn.execute("""
        SELECT 
            SUM(CASE WHEN importance >= 80 THEN 1 ELSE 0 END) as critical,
            SUM(CASE WHEN importance >= 60 AND importance < 80 THEN 1 ELSE 0 END) as high,
            SUM(CASE WHEN importance >= 40 AND importance < 60 THEN 1 ELSE 0 END) as medium,
            SUM(CASE WHEN importance >= 20 AND importance < 40 THEN 1 ELSE 0 END) as low,
            SUM(CASE WHEN importance < 20 THEN 1 ELSE 0 END) as junk
        FROM emails WHERE importance IS NOT NULL
    """).fetchone()
    
    # Top 50 most important emails
    top_emails = conn.execute("""
        SELECT subject, "from", date, importance, category, triage_reason
        FROM emails
        WHERE importance IS NOT NULL
        ORDER BY importance DESC
        LIMIT 50
    """).fetchall()
    
    # Emails with search term matches
    search_matches = conn.execute("""
        SELECT subject, "from", date, importance, reasons
        FROM emails
        WHERE reasons LIKE '%search_match%'
        ORDER BY date DESC
        LIMIT 30
    """).fetchall()
    
    # Build report
    report = []
    report.append("# Email Purge Summary Report")
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append("")
    report.append("## Overview")
    report.append(f"- **Total emails indexed:** {total}")
    report.append("")
    
    report.append("## Classification")
    for row in by_classification:
        report.append(f"- **{row['classification']}:** {row['cnt']} ({row['cnt']/total*100:.1f}%)")
    report.append("")
    
    report.append("## By Category")
    for row in by_category:
        report.append(f"- **{row['category']}:** {row['cnt']}")
    report.append("")
    
    if by_importance:
        imp = by_importance
        report.append("## Importance Distribution")
        report.append(f"- Critical (80-100): {imp['critical'] or 0}")
        report.append(f"- High (60-79): {imp['high'] or 0}")
        report.append(f"- Medium (40-59): {imp['medium'] or 0}")
        report.append(f"- Low (20-39): {imp['low'] or 0}")
        report.append(f"- Junk (0-19): {imp['junk'] or 0}")
        report.append("")
    
    report.append("## Top 50 Most Important Emails")
    report.append("| # | Importance | From | Date | Subject |")
    report.append("|---|-----------|------|------|---------|")
    for i, row in enumerate(top_emails, 1):
        subj = (row['subject'] or '')[:60]
        from_addr = (row['from'] or '')[:30]
        date = (row['date'] or '')[:10]
        report.append(f"| {i} | {row['importance']} | {from_addr} | {date} | {subj} |")
    report.append("")
    
    if search_matches:
        report.append("## Search Term Matches (Recent)")
        report.append("| Date | From | Subject | Importance |")
        report.append("|------|------|---------|-----------|")
        for row in search_matches:
            subj = (row['subject'] or '')[:50]
            from_addr = (row['from'] or '')[:30]
            date = (row['date'] or '')[:10]
            imp = row['importance'] or '?'
            report.append(f"| {date} | {from_addr} | {subj} | {imp} |")
        report.append("")
    
    report.append("## Actions")
    report.append("1. Review `escalate.jsonl` for emails needing human attention")
    report.append("2. Confirm drops in `drop.jsonl` before deletion")
    report.append("3. Keep confirmed important emails")
    report.append("4. Archive or delete the rest")
    
    # Write report
    with open(REPORT_FILE, "w") as f:
        f.write("\n".join(report))
    
    print(f"Report written to {REPORT_FILE}")
    
    # Print summary to console
    print("\n=== SUMMARY ===")
    print(f"Total: {total}")
    for row in by_classification:
        print(f"  {row['classification']}: {row['cnt']}")
    if by_importance:
        print(f"\nImportance:")
        print(f"  Critical: {by_importance['critical'] or 0}")
        print(f"  High:     {by_importance['high'] or 0}")
        print(f"  Medium:   {by_importance['medium'] or 0}")
        print(f"  Low:      {by_importance['low'] or 0}")
        print(f"  Junk:     {by_importance['junk'] or 0}")
    
    conn.close()

if __name__ == "__main__":
    main()
