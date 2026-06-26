#!/usr/bin/env python3
"""
dream.py — Memory Distillation Engine

Inspired by MiMo Code's /dream command: periodically reviews historical daily
logs, deduplicates them, compresses new learnings into MEMORY.md, and removes
outdated or contradictory entries.

Usage:
  python3 dream.py --run                    # Run full distillation
  python3 dream.py --dry-run                # Preview what would change
  python3 dream.py --report                 # Show what's been recently learned
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta

from pathlib import Path

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
MEMORY_MD = os.path.join(WORKSPACE, "MEMORY.md")
TOOLS_MD = os.path.join(WORKSPACE, "TOOLS.md")
DREAMS_DIR = os.path.join(MEMORY_DIR, ".dreams")

# ── Section anchors in MEMORY.md ──────────────────────────────────

# These sections exist in MEMORY.md and we should place new content
# under the appropriate section:
SECTION_TAGS = {
    "tool_behavior": ["工具", "Tool", "Prefer", "use read", "exec", "web_fetch",
                       "search", "skill", "API", "cron"],
    "user_preferences": ["用户", "偏好", "prefer", "want", "like", "prefer",
                          "沟通", "中文", "直接", "format"],
    "lessons_learned": ["教训", "lesson", "mistake", "错误", "should",
                         "shouldn", "must", "never", "always", "recurring"],
    "capabilities": ["可以", "can do", "able", "capable", "feature",
                      "功能", "new skill", "cron job"],
    "known_issues": ["bug", "issue", "problem", "问题", "broken", "fail",
                      "timeout", "error", "超时"],
    "self_improvement": ["improve", "self", "改进", "优化", "evolution",
                          "进化"],
    "key_events": ["event", "事件", "decision", "决定", "project",
                    "project", "里程碑"],
}

SECTION_HEADERS = {
    "tool_behavior": "### Tool Selection",
    "user_preferences": "### Communication",
    "lessons_learned": "### Problem Solving",
    "capabilities": "### Capabilities",
    "known_issues": "### Known Issues",
    "self_improvement": "### Self-Improvement",
    "key_events": "## Key Events",
}


def parse_memory_file(path):
    """Parse a daily memory file, extracting structured entries."""
    entries = []
    try:
        with open(path) as f:
            content = f.read()
    except Exception:
        return entries

    date_str = os.path.basename(path).replace(".md", "")
    lines = content.split("\n")
    current_entry = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Match: ### ✅ HH:MM - description
        m = re.match(r"###\s+([✅❌💡📌🤖])\s+(\d{2}:\d{2})\s*[-–—]\s*(.+)", line)
        if m:
            emoji, time_str, text = m.groups()
            entry_type = {
                "✅": "success", "❌": "error",
                "💡": "insight", "📌": "preference",
                "🤖": "cycle",
            }.get(emoji, "other")

            current_entry = {
                "date": date_str,
                "time": time_str,
                "type": entry_type,
                "emoji": emoji,
                "text": text.strip(),
                "details": [],
            }
            entries.append(current_entry)
            continue

        # Match: bullet continuation lines
        if current_entry and (line.startswith("-") or line.startswith("   ")):
            current_entry["details"].append(line.lstrip("- ").strip())

    return entries


def scan_daily_logs(days=14):
    """Scan daily memory files from the past N days."""
    all_entries = []
    cutoff = datetime.now() - timedelta(days=days)

    for f in sorted(Path(MEMORY_DIR).glob("20??-??-??.md")):
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if mtime >= cutoff:
            entries = parse_memory_file(str(f))
            all_entries.extend(entries)

    return all_entries


def read_existing_memory():
    """Read existing MEMORY.md content."""
    try:
        with open(MEMORY_MD) as f:
            return f.read()
    except FileNotFoundError:
        return "# MEMORY.md\n\n(No previous memories)\n"


def find_section(content, section_name):
    """Find the start and end position of a section in MEMORY.md."""
    header = SECTION_HEADERS.get(section_name, "")
    if not header:
        return None, None

    lines = content.split("\n")
    start = None
    end = None

    for i, line in enumerate(lines):
        if line.strip() == header:
            start = i
        elif start is not None and line.startswith("##") and i > start:
            end = i
            break

    return start, end


def classify_entry(entry):
    """Classify an entry into a MEMORY.md section."""
    text = entry["text"].lower()
    for detail in entry.get("details", []):
        text += " " + detail.lower()

    scores = {}
    for section, keywords in SECTION_TAGS.items():
        score = sum(1 for kw in keywords if kw.lower() in text)
        scores[section] = score

    # Default to a section based on entry type
    if entry["type"] == "error":
        scores["known_issues"] += 3
    elif entry["type"] == "insight":
        scores["lessons_learned"] += 3
    elif entry["type"] == "preference":
        scores["user_preferences"] += 5
    elif entry["type"] == "cycle":
        scores["self_improvement"] += 3

    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "key_events"
    return best


def extract_principle(entry):
    """Extract a concise one-line principle from an entry."""
    text = entry["text"].strip()

    # Remove leading artifacts
    text = re.sub(r'^\d+[\.\)]\s*', '', text)
    text = re.sub(r'^[-–—]\s*', '', text)

    # If it's already concise (under 120 chars), use as-is
    if len(text) <= 120:
        return text

    # Try to truncate at the first natural break
    for sep in ["。", "；", "，", ";", ",", "—", " - "]:
        idx = text.find(sep)
        if 20 < idx < 120:
            return text[:idx + len(sep)]

    return text[:120]


def is_duplicate(principle, existing_content):
    """Check if a principle is already present in MEMORY.md."""
    p_lower = principle.lower().strip()
    if len(p_lower) < 10:
        return True  # Too short to be meaningful

    content_lower = existing_content.lower()

    # Check exact substring match
    if p_lower in content_lower:
        return True

    # Check high-overlap fingerprint
    words = set(p_lower.split())
    if len(words) < 3:
        return False

    # Sample check: if key phrase appears
    key_phrase = " ".join(list(words)[:max(2, len(words)//2)])
    if key_phrase in content_lower:
        return True

    return False


def distill(days=14, dry_run=False):
    """Main distillation function. Returns (new_entries, sections_updated)."""
    os.makedirs(DREAMS_DIR, exist_ok=True)

    print(f"🌙 Dream — Memory Distillation (past {days} days)")
    print(f"{'='*55}\n")

    # 1. Scan daily logs
    entries = scan_daily_logs(days)
    print(f"📁 Scanned {len(entries)} entries from past {days} days")

    if not entries:
        print("   No entries to process")
        return [], {}

    # 2. Read existing memory
    existing = read_existing_memory()

    # 3. Extract principles from recent entries only
    now = datetime.now()
    recent_threshold = now - timedelta(days=14)
    recent_entries = [e for e in entries if e["date"] >= recent_threshold.strftime("%Y-%m-%d")]

    # 4. Deduplicate and classify
    classified = {}  # section -> [principles]
    stats = {"total": len(recent_entries), "new": 0, "duplicate": 0, "filtered": 0}

    for entry in recent_entries:
        if entry["type"] == "other":
            stats["filtered"] += 1
            continue

        principle = extract_principle(entry)

        if is_duplicate(principle, existing):
            stats["duplicate"] += 1
            continue

        # Check dedup across new entries
        if principle in [p for sec_items in classified.values() for p in sec_items]:
            stats["duplicate"] += 1
            continue

        section = classify_entry(entry)
        if section not in classified:
            classified[section] = []
        classified[section].append(principle)
        stats["new"] += 1

    print(f"🔍 Analysis: {stats['total']} entries → "
          f"{stats['new']} new, {stats['duplicate']} duplicates, "
          f"{stats['filtered']} filtered")

    if dry_run:
        print(f"\n📋 Would add to MEMORY.md:\n")
        for section, principles in classified.items():
            header = SECTION_HEADERS.get(section, section)
            print(f"  {header}")
            for p in principles:
                print(f"    → {p[:100]}")
            print()
        return classified, {}

    if not classified:
        print("   ✅ MEMORY.md is already up to date")
        # Save dream log
        _save_dream_log(stats, {})
        return [], {}

    # 5. Apply to MEMORY.md — insert in reverse line order to avoid position drift
    updated_sections = {}
    lines = existing.split("\n")

    # Sort sections by header position descending (last section first)
    section_positions = []
    for section, principles in classified.items():
        header = SECTION_HEADERS.get(section)
        if not header:
            continue
        start, _ = find_section(existing, section)
        if start is None:
            continue
        section_positions.append((start, section, principles))

    section_positions.sort(key=lambda x: x[0], reverse=True)  # process back-to-front

    if not section_positions:
        print("   ✅ MEMORY.md is already up to date")
        _save_dream_log(stats, {})
        return [], {}

    for start, section, principles in section_positions:
        section_content = "- " + "\n- ".join(principles)
        lines.insert(start + 1, section_content)
        updated_sections[section] = len(principles)

    new_content = "\n".join(lines)

    if updated_sections:
        with open(MEMORY_MD, "w") as f:
            f.write(new_content)
        print(f"\n💾 Updated MEMORY.md: {sum(updated_sections.values())} new principles across "
              f"{len(updated_sections)} sections")
        for sec, count in updated_sections.items():
            print(f"   {SECTION_HEADERS.get(sec, sec)}: +{count}")

        # Track change in learning trail
        _track_change(stats)

    # 6. Save dream log
    _save_dream_log(stats, updated_sections)

    return classified, updated_sections


def _save_dream_log(stats, sections):
    """Save dream execution log."""
    dream_id = datetime.now().strftime("%Y%m%d-%H%M")
    log = {
        "id": dream_id,
        "timestamp": datetime.now().isoformat(),
        "stats": stats,
        "sections": {k: v for k, v in sections.items()},
    }
    log_path = os.path.join(DREAMS_DIR, f"{dream_id}.json")
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)


def _track_change(stats):
    """Record this dream run in the learning trail."""
    trail_path = os.path.join(MEMORY_DIR, ".learning-trail.json")
    try:
        with open(trail_path) as f:
            trail = json.load(f)
    except Exception:
        return

    trail.setdefault("dreams", []).append({
        "timestamp": datetime.now().isoformat(),
        "stats": stats,
    })
    try:
        with open(trail_path, "w") as f:
            json.dump(trail, f, indent=2)
    except Exception:
        pass


def report_recent(days=14):
    """Show what's been learned recently (from dream logs)."""
    logs = sorted(Path(DREAMS_DIR).glob("*.json"), reverse=True)
    if not logs:
        print("No dream logs yet. Run --run first.")
        return

    print(f"🌙 Recent Dreams ({len(logs)} runs)\n")
    for log_file in logs[:7]:
        with open(log_file) as f:
            log = json.load(f)
        ts = log["timestamp"][:16].replace("T", " ")
        s = log["stats"]
        print(f"  {ts} | {s.get('new',0)} new, {s.get('duplicate',0)} dup "
              f"({s.get('total',0)} total)")


def main():
    parser = argparse.ArgumentParser(
        description="🌙 Memory Distillation — /dream for OpenClaw")
    parser.add_argument("--run", action="store_true",
                        help="Run full distillation")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview what would change (no writes)")
    parser.add_argument("--days", type=int, default=14,
                        help="Days of logs to scan (default: 14)")
    parser.add_argument("--report", action="store_true",
                        help="Show recent dream activity")
    args = parser.parse_args()

    if args.report:
        report_recent(args.days)
        return

    if args.run:
        distill(args.days, dry_run=False)
    elif args.dry_run:
        distill(args.days, dry_run=True)
    else:
        print("Usage: dream.py --run | --dry-run | --report")
        sys.exit(1)


if __name__ == "__main__":
    main()
