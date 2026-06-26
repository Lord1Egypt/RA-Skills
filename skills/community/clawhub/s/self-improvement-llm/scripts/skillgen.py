#!/usr/bin/env python3
"""
skillgen.py — Auto Skill Generator

Analyzes the learning trail for recurring workflow patterns and generates
skill skeleton (SKILL.md) drafts for the agent to review and approve.

Usage:
  python3 scripts/skillgen.py --scan              # Scan trail for skill-worthy patterns
  python3 scripts/skillgen.py --generate <id>     # Generate skill from a pattern
  python3 scripts/skillgen.py --auto              # Full auto: scan + generate all ready patterns
  python3 scripts/skillgen.py --list              # List drafted skills awaiting approval
  python3 scripts/skillgen.py --approve <name>    # Approve and install a drafted skill
  python3 scripts/skillgen.py --status            # Show skillgen stats
"""

import argparse
import json
import os
import re
import string
import random
from datetime import datetime, timedelta

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", "/home/admin/.openclaw/workspace")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
SKILLS_DIR = os.path.join(WORKSPACE, "skills")
DRAFTS_DIR = os.path.join(WORKSPACE, "memory", ".skill-drafts")
LEARNING_TRAIL_PATH = os.path.join(MEMORY_DIR, ".learning-trail.json")


def load_trail():
    """Load learning trail."""
    if not os.path.exists(LEARNING_TRAIL_PATH):
        return {"entries": [], "skills_generated": []}
    with open(LEARNING_TRAIL_PATH) as f:
        return json.load(f)


def save_trail(trail):
    with open(LEARNING_TRAIL_PATH, "w") as f:
        json.dump(trail, f, indent=2)


def ensure_drafts_dir():
    os.makedirs(DRAFTS_DIR, exist_ok=True)


# ── Pattern Detection ─────────────────────────────────────────────

# Keywords that suggest a repeatable workflow / skill candidate
WORKFLOW_KEYWORDS = [
    "weather", "天气", "爬虫", "scrape", "fetch", "抓", "搜索", "search",
    "转换", "convert", "生成", "generate", "结算", "settle", "报表",
    "report", "同步", "sync", "分析", "analyze", "提取", "extract",
    "解析", "parse", "格式化", "format", "上传", "upload", "下载",
    "download", "监控", "monitor", "通知", "notify", "计算", "calculate",
    "汇率", "rate", "翻译", "translate", "总结", "summarize",
    "merge", "split", "rename", "批量", "batch", "定时", "cron",
    "schedule", "自动", "auto", "检测", "detect", "check",
]

SKILL_TEMPLATES = {
    "weather": {"name": "weather-query", "desc": "天气查询"},
    "search": {"name": "web-search", "desc": "网络搜索"},
    "scrape": {"name": "web-scraper", "desc": "网页爬取"},
    "convert": {"name": "file-converter", "desc": "文件转换"},
    "sync": {"name": "data-sync", "desc": "数据同步"},
    "translate": {"name": "text-translator", "desc": "文本翻译"},
    "analyze": {"name": "data-analyzer", "desc": "数据分析"},
    "extract": {"name": "data-extractor", "desc": "数据提取"},
    "monitor": {"name": "monitor", "desc": "监控告警"},
    "summarize": {"name": "summarizer", "desc": "内容摘要"},
    "汇率": {"name": "exchange-rate", "desc": "汇率查询"},
    "结算": {"name": "settlement", "desc": "结算处理"},
    "结算": {"name": "settlement", "desc": "结算处理"},
}


def slugify(text):
    """Convert text to a filesystem-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-{2,}', '-', text)
    if not text:
        text = 'skill-' + ''.join(random.choices(string.ascii_lowercase, k=6))
    return text[:50]


def detect_skill_candidates(trail, min_recurrence=3, days_window=30):
    """
    Scan learning trail for patterns that could become skills.
    Returns list of candidates.
    """
    entries = trail.get("entries", [])
    now = datetime.now()
    cutoff = now - timedelta(days=days_window)

    # Group by pattern-key or by category
    patterns = {}
    for entry in entries:
        status = entry.get("status", "")
        if status in ("wont_fix", "reverted"):
            continue

        entry_date = entry.get("last_seen") or entry.get("logged_date", "")
        if entry_date:
            try:
                if datetime.strptime(entry_date, "%Y-%m-%d") < cutoff:
                    continue
            except ValueError:
                pass

        recurrence = entry.get("recurrence_count", 1)
        pattern_key = entry.get("pattern_key", "")
        category = entry.get("category", entry.get("area", "general"))
        summary = entry.get("summary", "")
        entry_id = entry.get("id", "")

        # Use pattern_key if available, else derive from summary
        key = pattern_key if pattern_key else slugify(summary)[:30]
        if not key:
            continue

        if key not in patterns:
            patterns[key] = {
                "pattern_key": key,
                "entry_ids": [],
                "total_recurrence": 0,
                "summaries": [],
                "categories": set(),
                "first_seen": entry_date or "unknown",
                "last_seen": entry_date or "unknown",
                "area": category,
            }

        patterns[key]["entry_ids"].append(entry_id)
        patterns[key]["total_recurrence"] += recurrence
        if summary and summary not in patterns[key]["summaries"]:
            patterns[key]["summaries"].append(summary[:80])
        patterns[key]["categories"].add(category)

    # Filter: candidates with enough recurrence
    candidates = []
    for key, info in patterns.items():
        if info["total_recurrence"] >= min_recurrence or len(info["entry_ids"]) >= 2:
            # Try to match a skill type
            skill_type = None
            for kw, tmpl in SKILL_TEMPLATES.items():
                if kw in key.lower() or any(kw in s.lower() for s in info["summaries"]):
                    skill_type = tmpl
                    break

            candidates.append({
                "id": f"SKILL-{slugify(key)[:20]}-{datetime.now().strftime('%Y%m%d')}",
                "pattern_key": key,
                "recurrence": info["total_recurrence"],
                "entry_count": len(info["entry_ids"]),
                "summaries": info["summaries"][:3],
                "area": info["area"],
                "skill_type": skill_type,
                "first_seen": info["first_seen"],
                "last_seen": info["last_seen"],
            })

    # Sort by recurrence descending
    candidates.sort(key=lambda c: c["recurrence"], reverse=True)
    return candidates


# ── Skill Generation ──────────────────────────────────────────────

SKILL_MD_TEMPLATE = """---
name: {name}
description: {description}
version: 0.1.0
created: {created}
source: auto-generated from learning trail (pattern: {pattern_key})
---

# {title}

> ⚠️ This skill was **auto-generated** from observed workflow patterns.
> Review and refine before relying on it.

## Trigger Conditions

When to activate this skill (auto-detected from usage patterns):

{triggers}

## Workflow

{workflow}

## Notes

{notes}

## Next Steps

- [ ] Review and refine trigger conditions
- [ ] Add concrete scripts/tools if needed
- [ ] Test with real inputs
- [ ] Remove this checklist and mark as stable
"""


def generate_skill_md(candidate):
    """Generate SKILL.md content from a candidate pattern."""
    name = candidate.get("skill_type", {}).get("name") or slugify(candidate["pattern_key"])
    desc = candidate.get("skill_type", {}).get("desc") or candidate["pattern_key"]
    title = desc.replace("-", " ").title()
    created = datetime.now().strftime("%Y-%m-%d %H:%M")
    pattern_key = candidate["pattern_key"]

    # Generate triggers from summaries
    triggers = ""
    for s in candidate["summaries"]:
        triggers += f"- \"{s}\" (observed {candidate['recurrence']}x)\n"
    if not triggers:
        triggers = "- (Review: what user requests should trigger this skill?)\n"

    # Generate workflow placeholder
    workflow = "Based on observed patterns:\n\n"
    for i, s in enumerate(candidate["summaries"], 1):
        workflow += f"{i}. **{s}** — (fill in concrete steps)\n"
    workflow += f"\n> Recurrence: {candidate['recurrence']}x across {candidate['entry_count']} session(s)"

    notes = (
        f"- **Area:** {candidate['area']}\n"
        f"- **First seen:** {candidate['first_seen']}\n"
        f"- **Last seen:** {candidate['last_seen']}\n"
        f"- **Pattern key:** `{pattern_key}`"
    )

    return SKILL_MD_TEMPLATE.format(
        name=name,
        description=desc,
        created=created,
        pattern_key=pattern_key,
        title=title,
        triggers=triggers,
        workflow=workflow,
        notes=notes,
    )


def save_draft(candidate):
    """Save a skill draft to the drafts directory."""
    name = candidate.get("skill_type", {}).get("name") or slugify(candidate["pattern_key"])
    draft_dir = os.path.join(DRAFTS_DIR, name)
    os.makedirs(draft_dir, exist_ok=True)

    skill_md = generate_skill_md(candidate)
    skill_md_path = os.path.join(draft_dir, "SKILL.md")

    # Don't overwrite existing drafts
    if os.path.exists(skill_md_path):
        # Append a note about new detection
        with open(skill_md_path) as f:
            content = f.read()
        if candidate["id"] not in content:
            with open(skill_md_path, "a") as f:
                f.write(f"\n\n<!-- Updated: {datetime.now().isoformat()} | New recurrence detected: {candidate['recurrence']}x -->\n")
        return skill_md_path, False

    with open(skill_md_path, "w") as f:
        f.write(skill_md)

    # Save metadata
    meta = {
        "id": candidate["id"],
        "name": name,
        "pattern_key": candidate["pattern_key"],
        "recurrence": candidate["recurrence"],
        "created": datetime.now().isoformat(),
        "status": "draft",
    }
    with open(os.path.join(draft_dir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    return skill_md_path, True


def approve_draft(name):
    """Approve a drafted skill and move it to skills/ directory."""
    draft_dir = os.path.join(DRAFTS_DIR, name)
    if not os.path.isdir(draft_dir):
        print(f"❌ Draft '{name}' not found in {DRAFTS_DIR}")
        return False

    skill_md_path = os.path.join(draft_dir, "SKILL.md")
    if not os.path.exists(skill_md_path):
        print(f"❌ SKILL.md not found in draft '{name}'")
        return False

    dest_dir = os.path.join(SKILLS_DIR, name)
    os.makedirs(dest_dir, exist_ok=True)

    # Copy SKILL.md to skills/
    import shutil
    for item in os.listdir(draft_dir):
        src = os.path.join(draft_dir, item)
        dst = os.path.join(dest_dir, item)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
        elif os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)

    # Update meta
    meta_path = os.path.join(draft_dir, "meta.json")
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            meta = json.load(f)
        meta["status"] = "approved"
        meta["approved"] = datetime.now().isoformat()
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)

    # Mark in learning trail
    trail = load_trail()
    trail.setdefault("skills_generated", []).append({
        "id": meta.get("id", "unknown"),
        "name": name,
        "status": "approved",
        "approved_at": meta["approved"],
    })
    save_trail(trail)

    print(f"✅ Skill '{name}' approved and installed to skills/{name}/")
    return True


# ── CLI Commands ──────────────────────────────────────────────────

def cmd_scan(args):
    """Scan learning trail for skill candidates."""
    trail = load_trail()
    candidates = detect_skill_candidates(trail)

    if not candidates:
        print("🔍 No skill-worthy patterns found.")
        print(f"   (Minimum recurrence: {args.min_recurrence}x, window: {args.days} days)")
        return

    print(f"\n🔍 Found {len(candidates)} skill-worthy pattern(s):\n")
    for i, c in enumerate(candidates, 1):
        print(f"  {i}. [{c['id']}] {c['pattern_key']}")
        print(f"     Recurrence: {c['recurrence']}x | Sessions: {c['entry_count']}")
        for s in c["summaries"]:
            print(f"     → {s}")
        if c["skill_type"]:
            print(f"     Type: {c['skill_type']['name']} ({c['skill_type']['desc']})")
        print()


def cmd_generate(args):
    """Generate skill draft from a pattern ID."""
    trail = load_trail()
    candidates = detect_skill_candidates(trail)

    if args.id:
        # Match by pattern key or id
        target = None
        for c in candidates:
            if args.id.lower() in c["id"].lower() or args.id.lower() in c["pattern_key"].lower():
                target = c
                break
        if not target:
            # Try listing candidates
            print(f"❌ No candidate matching '{args.id}'. Available:")
            for c in candidates:
                print(f"  {c['id']}: {c['pattern_key']}")
            return
        candidates = [target]

    for c in candidates:
        path, is_new = save_draft(c)
        if is_new:
            print(f"📝 Draft created: {path}")
        else:
            print(f"📝 Draft updated: {path}")


def cmd_auto(args):
    """Full auto: scan + generate all candidates."""
    trail = load_trail()
    candidates = detect_skill_candidates(trail)

    if not candidates:
        print("🔍 No patterns ready for skill generation.")
        return

    ensure_drafts_dir()
    print(f"\n🔍 Found {len(candidates)} pattern(s), generating drafts...\n")

    for c in candidates:
        path, is_new = save_draft(c)
        if is_new:
            print(f"  ✅ {c['pattern_key']} → {path}")
        else:
            print(f"  🔄 {c['pattern_key']} → {path} (updated)")

    print(f"\n💡 Use 'python3 scripts/skillgen.py --list' to review drafts")
    print(f"   Use 'python3 scripts/skillgen.py --approve <name>' to install")

    # Update trail stats
    trail["stats"]["total_skills_generated"] = trail["stats"].get("total_skills_generated", 0) + len(candidates)
    trail.setdefault("skills_generated", []).extend([
        {"id": c["id"], "name": c["pattern_key"], "status": "draft", "created": datetime.now().isoformat()}
        for c in candidates
    ])
    save_trail(trail)


def cmd_list(args):
    """List drafted skills."""
    ensure_drafts_dir()
    if not os.path.isdir(DRAFTS_DIR):
        print("No skill drafts yet.")
        return

    drafts = []
    for name in sorted(os.listdir(DRAFTS_DIR)):
        meta_path = os.path.join(DRAFTS_DIR, name, "meta.json")
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                meta = json.load(f)
            drafts.append(meta)
        elif os.path.exists(os.path.join(DRAFTS_DIR, name, "SKILL.md")):
            drafts.append({"name": name, "status": "unknown"})

    if not drafts:
        print("No skill drafts yet.")
        return

    print(f"\n📋 Skill Drafts ({len(drafts)}):\n")
    for d in drafts:
        status = d.get("status", "unknown")
        emoji = "📝" if status == "draft" else "✅" if status == "approved" else "❓"
        print(f"  {emoji} {d['name']}")
        if "pattern_key" in d:
            print(f"     Pattern: {d['pattern_key']}")
        if "recurrence" in d:
            print(f"     Recurrence: {d['recurrence']}x")
        print()


def cmd_status(args):
    """Show skillgen stats."""
    trail = load_trail()
    skills = trail.get("skills_generated", [])
    total = len(skills)
    approved = sum(1 for s in skills if s.get("status") == "approved")
    draft = sum(1 for s in skills if s.get("status") == "draft")

    print(f"\n📊 Skill Generation Stats:\n")
    print(f"  Total generated: {total}")
    print(f"  Approved: {approved}")
    print(f"  Drafts: {draft}")
    print()

    if skills:
        print("  Recent:")
        for s in skills[-5:]:
            status = "✅" if s.get("status") == "approved" else "📝"
            print(f"    {status} {s.get('name', '?')} ({s.get('status', '?')})")
        print()


# ── Main ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Auto Skill Generator")
    parser.add_argument("--scan", action="store_true", help="Scan trail for skill candidates")
    parser.add_argument("--generate", type=str, nargs="?", const="all", metavar="ID",
                        help="Generate skill draft(s). Optional: specific pattern ID")
    parser.add_argument("--auto", action="store_true", help="Full auto: scan + generate all")
    parser.add_argument("--list", action="store_true", help="List drafted skills")
    parser.add_argument("--approve", type=str, metavar="NAME", help="Approve and install a drafted skill")
    parser.add_argument("--status", action="store_true", help="Show skillgen stats")
    parser.add_argument("--min-recurrence", type=int, default=3, help="Min recurrence to qualify (default: 3)")
    parser.add_argument("--days", type=int, default=30, help="Lookback window in days (default: 30)")

    args = parser.parse_args()

    if args.scan:
        cmd_scan(args)
    elif args.generate:
        cmd_generate(args)
    elif args.auto:
        cmd_auto(args)
    elif args.list:
        cmd_list(args)
    elif args.approve:
        approve_draft(args.approve)
    elif args.status:
        cmd_status(args)
    else:
        # Default: scan
        cmd_scan(args)


if __name__ == "__main__":
    main()
