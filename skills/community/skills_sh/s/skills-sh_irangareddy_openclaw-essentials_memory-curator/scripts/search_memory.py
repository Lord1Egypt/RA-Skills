#!/usr/bin/env python3
"""
Search across all memory files (daily logs + MEMORY.md).

Usage:
    python search_memory.py --workspace ~/.openclaw/workspace --query "GraphQL"
    python search_memory.py --workspace ~/.openclaw/workspace --query "bug fix" --days 7
    python search_memory.py --workspace ~/.openclaw/workspace --recent 5
"""

import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path


def search_file(file_path: Path, query: str, context_lines: int = 2) -> list:
    """Search file for query and return matches with context."""
    matches = []

    try:
        lines = file_path.read_text().split('\n')
    except Exception:
        return matches

    for i, line in enumerate(lines):
        if re.search(query, line, re.IGNORECASE):
            # Get context lines
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            context = lines[start:end]

            matches.append({
                'line_number': i + 1,
                'line': line,
                'context': context,
                'file': file_path
            })

    return matches


def get_recent_logs(workspace: Path, days: int = None) -> list:
    """Get recent daily log files."""
    memory_dir = workspace / "memory"
    if not memory_dir.exists():
        return []

    log_files = []
    for file_path in memory_dir.glob("????-??-??.md"):
        # Parse date from filename
        try:
            date_str = file_path.stem
            log_date = datetime.strptime(date_str, "%Y-%m-%d")

            if days:
                cutoff = datetime.now() - timedelta(days=days)
                if log_date < cutoff:
                    continue

            log_files.append((log_date, file_path))
        except ValueError:
            continue

    # Sort by date, most recent first
    log_files.sort(reverse=True)
    return [f for _, f in log_files]


def show_recent_logs(workspace: Path, count: int) -> None:
    """Show most recent log files."""
    logs = get_recent_logs(workspace)[:count]

    for log_path in logs:
        date = log_path.stem
        print(f"\n{'='*60}")
        print(f"📅 {date}")
        print('='*60)
        content = log_path.read_text()
        print(content)


def search_memory(workspace: Path, query: str, days: int = None) -> list:
    """Search all memory files."""
    memory_dir = workspace / "memory"
    all_matches = []

    # Search MEMORY.md if exists
    memory_file = workspace / "MEMORY.md"
    if memory_file.exists():
        matches = search_file(memory_file, query)
        if matches:
            all_matches.append(('MEMORY.md', matches))

    # Search daily logs
    if memory_dir.exists():
        log_files = get_recent_logs(workspace, days)
        for log_path in log_files:
            matches = search_file(log_path, query)
            if matches:
                all_matches.append((log_path.name, matches))

    return all_matches


def main():
    parser = argparse.ArgumentParser(description="Search memory files")
    parser.add_argument("--workspace", required=True, help="Agent workspace path")
    parser.add_argument("--query", help="Search query (regex)")
    parser.add_argument("--days", type=int, help="Limit search to recent N days")
    parser.add_argument("--recent", type=int, help="Show N most recent logs")

    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser()

    if args.recent:
        show_recent_logs(workspace, args.recent)
        return

    if not args.query:
        print("Error: --query required (or use --recent)")
        return 1

    results = search_memory(workspace, args.query, args.days)

    if not results:
        print(f"No matches found for: {args.query}")
        return

    print(f"Found matches in {len(results)} file(s):\n")

    for filename, matches in results:
        print(f"\n{'='*60}")
        print(f"📄 {filename}")
        print('='*60)

        for match in matches:
            print(f"\nLine {match['line_number']}:")
            print('-' * 40)
            for ctx_line in match['context']:
                if ctx_line == match['line']:
                    print(f">>> {ctx_line}")
                else:
                    print(f"    {ctx_line}")


if __name__ == "__main__":
    main()
