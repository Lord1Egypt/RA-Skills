#!/usr/bin/env python3
"""
memory_decay.py — Temporal decay and archival for memory files.

Moves stale entries from MEMORY.md and memory/*.md to memory/archive/.
Preserves high-value entries (LESSON, active PROJECT) based on rules.
"""

import argparse
import os
import re
import shutil
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace")))
MEMORY_FILE = WORKSPACE / "MEMORY.md"
MEMORY_DIR = WORKSPACE / "memory"
ARCHIVE_DIR = MEMORY_DIR / "archive"

TYPE_PATTERNS = {
    "PREF": re.compile(r"\[PREF\]", re.IGNORECASE),
    "PROJ": re.compile(r"\[PROJ\]", re.IGNORECASE),
    "TECH": re.compile(r"\[TECH\]", re.IGNORECASE),
    "LESSON": re.compile(r"\[LESSON\]", re.IGNORECASE),
    "PEOPLE": re.compile(r"\[PEOPLE\]", re.IGNORECASE),
    "TEMP": re.compile(r"\[TEMP\]", re.IGNORECASE),
}

DATE_PATTERN = re.compile(r"(\d{4}-\d{2}-\d{2})")


def detect_type(line: str) -> str | None:
    """Detect memory type from a line."""
    for mem_type, pattern in TYPE_PATTERNS.items():
        if pattern.search(line):
            return mem_type
    return None


def get_file_age(filepath: Path) -> int:
    """Get file age in days."""
    mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
    return (datetime.now() - mtime).days


def parse_daily_files(max_age_days: int, dry_run: bool) -> dict:
    """Find and categorize daily memory files by age."""
    results = {"archived": [], "kept": [], "skipped": []}

    if not MEMORY_DIR.exists():
        return results

    for f in MEMORY_DIR.glob("*.md"):
        if f.name == "archive":
            continue
        # Extract date from filename
        match = DATE_PATTERN.search(f.name)
        if not match:
            results["skipped"].append(str(f))
            continue

        file_date = datetime.strptime(match.group(1), "%Y-%m-%d")
        age = (datetime.now() - file_date).days

        if age > max_age_days:
            archive_subdir = ARCHIVE_DIR / file_date.strftime("%Y-%m")
            if not dry_run:
                archive_subdir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(f), str(archive_subdir / f.name))
            results["archived"].append({
                "file": str(f),
                "age_days": age,
                "destination": str(archive_subdir / f.name) if not dry_run else "would archive"
            })
        else:
            results["kept"].append({"file": str(f), "age_days": age})

    return results


def decay_memory_md(max_age_days: int, dry_run: bool) -> dict:
    """Analyze MEMORY.md for stale sections and orphaned entries."""
    results = {"sections": 0, "orphaned_lines": 0, "suggestions": []}

    if not MEMORY_FILE.exists():
        return results

    content = MEMORY_FILE.read_text(encoding="utf-8")
    lines = content.split("\n")
    current_section = None
    section_lines = {}

    for i, line in enumerate(lines):
        if line.startswith("## "):
            current_section = line.strip()
            section_lines[current_section] = {"start": i, "lines": []}
        elif current_section and line.strip():
            section_lines.setdefault(current_section, {"start": i, "lines": []})
            if current_section in section_lines:
                section_lines[current_section]["lines"].append((i, line))

    results["sections"] = len(section_lines)

    # Find lines without type tags in typed sections
    typed_sections = {k: v for k, v in section_lines.items()
                      if any(f"[{t}]" in k for t in TYPE_PATTERNS)}

    for section, data in typed_sections.items():
        for line_no, line in data["lines"]:
            if line.strip().startswith("-") and not detect_type(line):
                results["orphaned_lines"] += 1
                results["suggestions"].append(
                    f"Line {line_no + 1}: '{line.strip()[:60]}...' — missing type tag"
                )

    return results


def promote_lessons(min_references: int = 2, dry_run: bool = False) -> dict:
    """Find LESSON entries in daily files referenced 2+ times, promote to MEMORY.md."""
    results = {"candidates": [], "promoted": []}

    if not MEMORY_DIR.exists():
        return results

    # Collect all LESSON entries from daily files
    lesson_entries = {}  # normalized_text -> [{"file", "line", "text"}]
    for f in MEMORY_DIR.glob("*.md"):
        if f.name == "archive":
            continue
        content = f.read_text(encoding="utf-8")
        for i, line in enumerate(content.split("\n"), 1):
            if detect_type(line) == "LESSON" and line.strip().startswith("-"):
                # Normalize for comparison
                clean = re.sub(r"\[LESSON\]\s*", "", line.strip()).strip()
                clean = re.sub(r"^-\s*", "", clean).strip()
                key = clean.lower()[:80]  # First 80 chars for matching
                if key not in lesson_entries:
                    lesson_entries[key] = []
                lesson_entries[key].append({"file": str(f), "line": i, "text": clean})

    # Find entries appearing in 2+ different files
    for key, occurrences in lesson_entries.items():
        unique_files = set(o["file"] for o in occurrences)
        if len(unique_files) >= min_references:
            results["candidates"].append({
                "text": occurrences[0]["text"],
                "references": len(unique_files),
                "files": list(unique_files),
            })

    # Check which are NOT already in MEMORY.md
    if MEMORY_FILE.exists():
        memory_content = MEMORY_FILE.read_text(encoding="utf-8").lower()
    else:
        memory_content = ""

    for candidate in results["candidates"]:
        # Simple substring check
        if candidate["text"].lower()[:60] not in memory_content:
            results["promoted"].append(candidate)
            if not dry_run:
                # Append to LESSON section in MEMORY.md
                if MEMORY_FILE.exists():
                    content = MEMORY_FILE.read_text(encoding="utf-8")
                    if "## [LESSON]" in content:
                        content = re.sub(
                            r"(## \[LESSON\][^\n]*)",
                            f"\\1\n- {candidate['text']}",
                            content,
                            count=1,
                        )
                    else:
                        content += f"\n\n## [LESSON] Lessons Learned\n- {candidate['text']}\n"
                    MEMORY_FILE.write_text(content, encoding="utf-8")

    return results


def run_decay(max_age_days: int, archive_dir: Path, dry_run: bool) -> None:
    """Main decay runner."""
    global ARCHIVE_DIR
    ARCHIVE_DIR = archive_dir

    print(f"=== Memory Decay {'(DRY RUN)' if dry_run else ''} ===")
    print(f"Max age: {max_age_days} days")
    print(f"Archive dir: {ARCHIVE_DIR}")
    print()

    # 1. Process daily files
    print("--- Daily Memory Files ---")
    daily_results = parse_daily_files(max_age_days, dry_run)

    if daily_results["archived"]:
        print(f"Archived {len(daily_results['archived'])} files:")
        for item in daily_results["archived"]:
            print(f"  {item['file']} (age: {item['age_days']}d) → {item['destination']}")
    else:
        print("No files to archive.")

    print(f"Kept {len(daily_results['kept'])} recent files.")
    if daily_results["skipped"]:
        print(f"Skipped {len(daily_results['skipped'])} non-date files.")
    print()

    # 2. Analyze MEMORY.md
    print("--- MEMORY.md Analysis ---")
    md_results = decay_memory_md(max_age_days, dry_run)
    print(f"Sections: {md_results['sections']}")
    print(f"Orphaned lines (missing type tag): {md_results['orphaned_lines']}")
    if md_results["suggestions"]:
        print("Suggestions:")
        for s in md_results["suggestions"][:10]:
            print(f"  - {s}")
        if len(md_results["suggestions"]) > 10:
            print(f"  ... and {len(md_results['suggestions']) - 10} more")

    print()
    # 3. Promote LESSON entries
    print("--- LESSON Promotion ---")
    lesson_results = promote_lessons(dry_run=dry_run)
    if lesson_results["candidates"]:
        print(f"Found {len(lesson_results['candidates'])} LESSON candidates (referenced 2+ files):")
        for c in lesson_results["candidates"][:5]:
            print(f"  [{c['references']} refs] {c['text'][:60]}")
        if lesson_results["promoted"]:
            action = "Promoted" if not dry_run else "Would promote"
            print(f"{action} {len(lesson_results['promoted'])} to MEMORY.md")
        else:
            print("All candidates already in MEMORY.md.")
    else:
        print("No LESSON entries with 2+ references found.")
    print()

    print("=== Decay Complete ===")


def main():
    parser = argparse.ArgumentParser(description="Memory decay and archival tool")
    parser.add_argument("--max-age-days", type=int, default=90,
                        help="Archive daily files older than N days (default: 90)")
    parser.add_argument("--archive-dir", type=Path, default=ARCHIVE_DIR,
                        help="Archive directory (default: memory/archive)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done without making changes")
    parser.add_argument("--promote-only", action="store_true",
                        help="Only run LESSON promotion, skip archival")
    args = parser.parse_args()

    if args.promote_only:
        print(f"=== LESSON Promotion {'(DRY RUN)' if args.dry_run else ''} ===")
        lesson_results = promote_lessons(dry_run=args.dry_run)
        if lesson_results["candidates"]:
            print(f"Found {len(lesson_results['candidates'])} LESSON candidates (referenced 2+ files):")
            for c in lesson_results["candidates"][:10]:
                print(f"  [{c['references']} refs] {c['text'][:70]}")
            if lesson_results["promoted"]:
                action = "Promoted" if not args.dry_run else "Would promote"
                print(f"{action} {len(lesson_results['promoted'])} to MEMORY.md")
            else:
                print("All candidates already in MEMORY.md.")
        else:
            print("No LESSON entries with 2+ references found.")
        return

    run_decay(args.max_age_days, args.archive_dir, args.dry_run)


if __name__ == "__main__":
    main()
