#!/usr/bin/env python3
"""
query_memory.py — 查询 Synapse 记忆记录

用法:
    python3 query_memory.py /path/to/project --task-type debug --limit 5
    python3 query_memory.py /path/to/project --contains "登录 bug"
    python3 query_memory.py /path/to/project --list-types

功能:
1. 按 task_type 查询历史记录
2. 按关键词搜索记录
3. 列出所有可用的 task_type
"""

import sys
import argparse
import json
from pathlib import Path
from datetime import datetime


def get_memory_dir(project: Path) -> Path:
    """Get synapse memory directory."""
    return project / ".synapse" / "memory"


def list_task_types(memory_dir: Path) -> list:
    """List all available task types."""
    if not memory_dir.exists():
        return []

    task_types = []
    for item in memory_dir.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            task_types.append(item.name)
    return sorted(task_types)


def get_records_by_task_type(memory_dir: Path, task_type: str, limit: int = 10) -> list:
    """Get records for a specific task type."""
    task_type_dir = memory_dir / task_type
    if not task_type_dir.exists():
        return []

    records = []
    # Get markdown files, sorted by modification time (newest first)
    md_files = sorted(
        task_type_dir.glob("*.md"),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )[:limit]

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")
            # Extract first line as title/description
            first_line = content.split("\n")[0].strip()
            records.append({
                "file": md_file.name,
                "description": first_line,
                "created": datetime.fromtimestamp(md_file.stat().st_ctime).isoformat(),
                "path": str(md_file)
            })
        except Exception as e:
            records.append({
                "file": md_file.name,
                "error": str(e),
                "path": str(md_file)
            })

    return records


def search_records_by_keyword(memory_dir: Path, keyword: str, limit: int = 10) -> list:
    """Search records by keyword across all task types."""
    if not memory_dir.exists():
        return []

    results = []
    keyword_lower = keyword.lower()

    for task_type_dir in memory_dir.iterdir():
        if not task_type_dir.is_dir() or task_type_dir.name.startswith("."):
            continue

        for md_file in task_type_dir.glob("*.md"):
            try:
                # 优化：先检查文件名，再逐行读取（避免整个文件读入内存 + 小写转换）
                if keyword_lower in md_file.name.lower():
                    content = md_file.read_text(encoding="utf-8")
                    matching_lines = [
                        line.strip() for line in content.split("\n")
                        if keyword_lower in line.lower()
                    ]
                    results.append({
                        "task_type": task_type_dir.name,
                        "file": md_file.name,
                        "matching_lines": matching_lines[:3],
                        "created": datetime.fromtimestamp(md_file.stat().st_ctime).isoformat(),
                        "path": str(md_file)
                    })
                    if len(results) >= limit:
                        return results
                    continue

                # 逐行读取，避免大文件一次性读入
                matched = False
                matching_lines = []
                with open(md_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if keyword_lower in line.lower():
                            matched = True
                            matching_lines.append(line.strip())
                            if len(matching_lines) >= 3:
                                break

                if matched:
                    results.append({
                        "task_type": task_type_dir.name,
                        "file": md_file.name,
                        "matching_lines": matching_lines,
                        "created": datetime.fromtimestamp(md_file.stat().st_ctime).isoformat(),
                        "path": str(md_file)
                    })
                    if len(results) >= limit:
                        return results

            except Exception:
                continue

    return results


def get_log_entries(project: Path, limit: int = 10) -> list:
    """Get recent entries from .knowledge/log.md."""
    log_file = project / ".knowledge" / "log.md"
    if not log_file.exists():
        return []

    try:
        content = log_file.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Skip header lines (frontmatter and title)
        start_idx = 0
        in_frontmatter = False
        for i, line in enumerate(lines):
            if line.startswith("---"):
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    start_idx = i + 1
                    break

        # Get last N entries (each entry starts with "## " or "- ")
        entries = []
        current_entry = []
        for line in lines[start_idx:]:
            if line.startswith("## ") or line.startswith("- ["):
                if current_entry:
                    entries.append("\n".join(current_entry))
                current_entry = [line]
            elif current_entry:
                current_entry.append(line)

        if current_entry:
            entries.append("\n".join(current_entry))

        return entries[-limit:]
    except Exception:
        return []


def main():
    parser = argparse.ArgumentParser(
        description="Query Synapse memory records",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/project --task-type debug --limit 5
  %(prog)s /path/to/project --contains "登录 bug"
  %(prog)s /path/to/project --list-types
  %(prog)s /path/to/project --recent-logs
        """
    )
    parser.add_argument("project", type=Path, help="Project root path")
    parser.add_argument("--task-type", "-t", help="Filter by task type (debug, refactor, etc.)")
    parser.add_argument("--contains", "-c", dest="contains", help="Search by keyword")
    parser.add_argument("--list-types", "-l", action="store_true", help="List all task types")
    parser.add_argument("--recent-logs", "-r", action="store_true", help="Show recent log entries")
    parser.add_argument("--limit", "-n", type=int, default=10, help="Max results to return")
    parser.add_argument("--json", "-j", action="store_true", dest="json_output", help="Output as JSON")

    args = parser.parse_args()

    project = args.project.resolve()
    memory_dir = get_memory_dir(project)

    if not memory_dir.exists():
        if args.json_output:
            print(json.dumps({"error": f"Memory directory not found: {memory_dir}"}))
        else:
            print(f"Error: Memory directory not found: {memory_dir}")
            print(f"  Run: /synapse-code init {project}")
        sys.exit(1)

    # --list-types
    if args.list_types:
        task_types = list_task_types(memory_dir)
        if args.json_output:
            print(json.dumps({"task_types": task_types}, ensure_ascii=False, indent=2))
        else:
            print(f"Available task types in {memory_dir}:")
            for tt in task_types:
                count = len(list((memory_dir / tt).glob("*.md")))
                print(f"  - {tt} ({count} records)")
        sys.exit(0)

    # --recent-logs
    if args.recent_logs:
        entries = get_log_entries(project, args.limit)
        if args.json_output:
            print(json.dumps({"log_entries": entries}, ensure_ascii=False, indent=2))
        else:
            print(f"Recent log entries from {project}/.knowledge/log.md:")
            print("-" * 60)
            for entry in entries:
                print(entry)
                print()
        sys.exit(0)

    # --contains (keyword search)
    if args.contains:
        results = search_records_by_keyword(memory_dir, args.contains, args.limit)
        if args.json_output:
            print(json.dumps({"results": results, "keyword": args.contains}, ensure_ascii=False, indent=2))
        else:
            print(f"Search results for '{args.contains}':")
            print("-" * 60)
            if not results:
                print("  No matches found.")
            else:
                for r in results:
                    print(f"[{r['task_type']}] {r['file']}")
                    print(f"  Created: {r['created']}")
                    print(f"  Matches: {' | '.join(r['matching_lines'])}")
                    print()
            print(f"Total: {len(results)} records")
        sys.exit(0)

    # --task-type
    if args.task_type:
        records = get_records_by_task_type(memory_dir, args.task_type, args.limit)
        if args.json_output:
            print(json.dumps({"task_type": args.task_type, "records": records}, ensure_ascii=False, indent=2))
        else:
            print(f"Records for task_type '{args.task_type}':")
            print("-" * 60)
            if not records:
                print(f"  No records found for '{args.task_type}'.")
            else:
                for r in records:
                    print(f"## {r['file']}")
                    print(f"   Created: {r['created']}")
                    if 'description' in r:
                        print(f"   {r['description']}")
                    print()
            print(f"Total: {len(records)} records")
        sys.exit(0)

    # Default: show summary
    task_types = list_task_types(memory_dir)
    total_records = sum(
        len(list((memory_dir / tt).glob("*.md")))
        for tt in task_types
    )

    if args.json_output:
        print(json.dumps({
            "project": str(project),
            "memory_dir": str(memory_dir),
            "task_types": task_types,
            "total_records": total_records
        }, ensure_ascii=False, indent=2))
    else:
        print(f"Synapse Memory Summary for {project}:")
        print("-" * 60)
        print(f"Memory directory: {memory_dir}")
        print(f"Total records: {total_records}")
        print()
        print("Task types:")
        for tt in task_types:
            count = len(list((memory_dir / tt).glob("*.md")))
            print(f"  - {tt}: {count} records")
        print()
        print("Use --help for query options.")


if __name__ == "__main__":
    main()
