#!/usr/bin/env python3
"""
Project Tracker Parser (JIRA / Linear)

Parses JIRA CSV exports and Linear JSON exports to extract issue activity
from a target user.

Usage:
    python3 project_tracker_parser.py --file jira_export.csv --target "Alex Chen" --output /tmp/jira_out.txt
    python3 project_tracker_parser.py --file linear_export.json --target "alex" --output /tmp/linear_out.txt
"""

from __future__ import annotations

import csv
import json
import argparse
import sys
from pathlib import Path


def parse_jira_csv(file_path: Path, target: str) -> list:
    """Parse JIRA CSV export."""
    items = []
    target_lower = target.lower()

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check if target is assignee, reporter, or in comments
            assignee = row.get("Assignee", row.get("assignee", "")).lower()
            reporter = row.get("Reporter", row.get("reporter", "")).lower()

            if target_lower not in assignee and target_lower not in reporter:
                continue

            items.append({
                "key": row.get("Issue key", row.get("Key", row.get("key", ""))),
                "type": row.get("Issue Type", row.get("Type", row.get("issuetype", ""))),
                "summary": row.get("Summary", row.get("summary", "")),
                "status": row.get("Status", row.get("status", "")),
                "priority": row.get("Priority", row.get("priority", "")),
                "assignee": row.get("Assignee", row.get("assignee", "")),
                "reporter": row.get("Reporter", row.get("reporter", "")),
                "description": row.get("Description", row.get("description", ""))[:2000],
                "created": row.get("Created", row.get("created", "")),
                "resolved": row.get("Resolved", row.get("resolved", "")),
            })

    return items


def parse_linear_json(file_path: Path, target: str) -> list:
    """Parse Linear JSON export."""
    items = []
    target_lower = target.lower()

    data = json.loads(file_path.read_text(encoding="utf-8"))

    # Linear export structure varies
    issues = data if isinstance(data, list) else data.get("issues", data.get("data", []))

    for issue in issues:
        assignee = ""
        if isinstance(issue.get("assignee"), dict):
            assignee = issue["assignee"].get("name", issue["assignee"].get("displayName", ""))
        elif isinstance(issue.get("assignee"), str):
            assignee = issue["assignee"]

        creator = ""
        if isinstance(issue.get("creator"), dict):
            creator = issue["creator"].get("name", "")
        elif isinstance(issue.get("creator"), str):
            creator = issue["creator"]

        if target_lower not in assignee.lower() and target_lower not in creator.lower():
            continue

        items.append({
            "key": issue.get("identifier", issue.get("id", "")),
            "type": issue.get("type", "Issue"),
            "summary": issue.get("title", ""),
            "status": issue.get("state", {}).get("name", "") if isinstance(issue.get("state"), dict) else str(issue.get("state", "")),
            "priority": str(issue.get("priority", "")),
            "assignee": assignee,
            "description": (issue.get("description") or "")[:2000],
            "created": issue.get("createdAt", ""),
        })

    return items


def main():
    parser = argparse.ArgumentParser(description="Parse JIRA/Linear exports")
    parser.add_argument("--file", required=True, help="Path to CSV (JIRA) or JSON (Linear) export")
    parser.add_argument("--target", required=True, help="Target user name")
    parser.add_argument("--output", required=True, help="Output file path")

    args = parser.parse_args()
    file_path = Path(args.file)

    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    # Detect format
    if file_path.suffix.lower() == ".csv":
        items = parse_jira_csv(file_path, args.target)
        source = "JIRA"
    elif file_path.suffix.lower() == ".json":
        items = parse_linear_json(file_path, args.target)
        source = "Linear"
    else:
        # Try CSV first
        try:
            items = parse_jira_csv(file_path, args.target)
            source = "JIRA"
        except Exception:
            items = parse_linear_json(file_path, args.target)
            source = "Linear"

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# {source} Issues for {args.target}\n")
        f.write(f"# Total: {len(items)} issues\n\n")

        for item in items:
            f.write(f"## [{item['key']}] {item['summary']}\n")
            f.write(f"Type: {item['type']} | Status: {item['status']} | Priority: {item.get('priority', 'N/A')}\n")
            f.write(f"Assignee: {item.get('assignee', 'N/A')}\n")
            if item.get("created"):
                f.write(f"Created: {item['created']}\n")
            if item.get("description"):
                f.write(f"\n{item['description']}\n")
            f.write("\n---\n\n")

    print(f"✅ Parsed {len(items)} {source} issues → {args.output}")


if __name__ == "__main__":
    main()
