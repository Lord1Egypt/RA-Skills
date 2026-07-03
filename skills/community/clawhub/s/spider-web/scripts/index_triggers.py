#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spider Web - Trigger Index Engine
Scans all installed skills and builds a unified trigger-word database.
Supports: single-line desc, quoted desc, YAML folded scalar (>), trigger word extraction in Chinese/English.
"""
import os, re, json, sys, time
from pathlib import Path

def setup_encoding():
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        except: pass

def extract_frontmatter(content):
    """Extract YAML frontmatter block."""
    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    return m.group(1) if m else ""

def extract_description(fm):
    """Extract description value from YAML frontmatter. Handles all formats."""
    lines = fm.split('\n')
    desc_parts = []
    in_desc = False
    mode = None  # 'plain', 'quoted', 'folded'

    for line in lines:
        m = re.match(r'^description:', line)
        if m:
            in_desc = True
            rest = line[m.end():].strip()
            if rest.startswith('>'):
                mode = 'folded'
                if len(rest) > 1 and rest[1:].strip():
                    desc_parts.append(rest[1:].strip())
            elif rest.startswith('|'):
                mode = 'literal'
                if len(rest) > 1 and rest[1:].strip():
                    desc_parts.append(rest[1:].strip())
            elif rest.startswith('"'):
                mode = 'quoted'
                inner = rest[1:]
                if '"' in inner:
                    # Single line quoted
                    inner = inner[:inner.rindex('"')]
                    desc_parts.append(inner)
                    break
                else:
                    desc_parts.append(inner)
            else:
                mode = 'plain'
                if rest:
                    desc_parts.append(rest)
            continue

        if not in_desc:
            continue

        stripped = line.strip()
        # Stop conditions
        if mode == 'plain':
            if re.match(r'^\w[\w-]*:', stripped):
                break
        elif mode in ('folded', 'literal'):
            if re.match(r'^\w[\w-]*:', stripped) and not stripped.startswith(' '):
                break
        elif mode == 'quoted':
            if stripped.endswith('"'):
                desc_parts.append(stripped[:-1])
                break
            else:
                desc_parts.append(stripped)

        if stripped:
            # Continue accumulating for folded/literal
            if mode in ('folded', 'literal'):
                desc_parts.append(stripped)
            elif mode == 'plain':
                if not re.match(r'^\w[\w-]*:', stripped):
                    desc_parts.append(stripped)
                else:
                    break

    desc = ' '.join(desc_parts).strip()
    # Clean up
    desc = desc.strip('"').strip()
    return desc

def extract_triggers(desc):
    """Extract trigger words from description string. Supports Chinese and English markers."""
    triggers = []
    # All possible trigger markers - CHECK CHINESE FIRST (more common)
    markers = [
        '触发词：', '触发词:', '触发词 :', '触发词 ：',
        'Triggers: ', 'Triggers:', 'Triggers：', 'Triggers ：',
        'Trigger: ', 'Trigger:', 'Trigger：',
    ]

    for marker in markers:
        idx = desc.find(marker)
        if idx < 0:
            continue
        trigger_str = desc[idx + len(marker):]
        # Cut at boundaries
        for cut in ['. GitHub:', '. GitHub', 'GitHub:', '\n']:
            ci = trigger_str.find(cut)
            if 0 < ci < 500:
                trigger_str = trigger_str[:ci]
                break
        trigger_str = trigger_str.strip().rstrip('.。')
        # Split
        parts = re.split(r'[,，;；、]', trigger_str)
        for p in parts:
            p = p.strip().strip('.。').strip()
            if p and not p.startswith('http') and not p.startswith('GitHub'):
                triggers.append(p)
        break  # First match wins

    # Fallback: no explicit trigger markers found, extract from description itself
    if not triggers:
        triggers = extract_keywords_from_desc(desc)

    return triggers


def extract_keywords_from_desc(desc):
    """
    Fallback: extract meaningful keywords from description when no explicit triggers.
    Looks for phrases after '查询', '分析', '生成' etc. and standalone meaningful terms.
    """
    keywords = []
    # Remove common filler
    desc_clean = re.sub(r'(AI|自动|系统|助手|一键|智能|交互式|可视化|HTML|报告)', '', desc)

    # Extract meaningful short phrases (2-6 chars)
    # Find noun phrases after action verbs
    patterns = [
        r'查询([\u4e00-\u9fff]{2,8})',
        r'分析([\u4e00-\u9fff]{2,8})',
        r'生成([\u4e00-\u9fff]{2,8})',
        r'支持([\u4e00-\u9fff]{2,8})',
        r'覆盖([\u4e00-\u9fff]{2,8})',
        r'提供([\u4e00-\u9fff]{2,8})',
        r'管理([\u4e00-\u9fff]{2,8})',
        r'识别([\u4e00-\u9fff]{2,8})',
        r'监控([\u4e00-\u9fff]{2,8})',
    ]
    for pat in patterns:
        for m in re.finditer(pat, desc_clean):
            kw = m.group(1).strip()
            if len(kw) >= 2 and kw not in keywords:
                keywords.append(kw)

    # Also grab standalone English words / acronyms (2+ uppercase chars)
    for m in re.finditer(r'\b([A-Z]{2,}|[A-Z][a-z]+)\b', desc):
        kw = m.group(1)
        if kw not in ['AI', 'HTML', 'API']:
            keywords.append(kw.lower())

    return keywords[:15]  # Cap at 15 auto-extracted keywords

def index_all_skills(skills_dir=None):
    """Index all skills and return trigger database."""
    if skills_dir is None:
        skills_dir = os.path.expanduser("~/.workbuddy/skills/")

    result = {}
    skipped = []
    errors = []

    for d in sorted(os.listdir(skills_dir)):
        skill_path = os.path.join(skills_dir, d)
        if not os.path.isdir(skill_path):
            continue
        md_path = os.path.join(skill_path, "SKILL.md")
        if not os.path.exists(md_path):
            continue

        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            errors.append((d, f"read error: {e}"))
            continue

        fm = extract_frontmatter(content)
        if not fm:
            skipped.append((d, "no frontmatter"))
            continue

        desc = extract_description(fm)
        if not desc:
            skipped.append((d, "no description"))
            continue

        triggers = extract_triggers(desc)
        if triggers:
            result[d] = triggers
        else:
            skipped.append((d, f"no triggers found in: {desc[:80]}..."))

    # Build reverse index
    reverse_index = {}
    for skill_name, triggers in result.items():
        for t in triggers:
            key = t.strip().lower()
            if key not in reverse_index:
                reverse_index[key] = []
            if skill_name not in reverse_index[key]:
                reverse_index[key].append(skill_name)

    # Also index by skill name and display_name for broader matching
    skill_names_index = {}
    for skill_name in result:
        skill_names_index[skill_name.lower()] = skill_name

    total_skills = len(result)
    total_triggers = sum(len(v) for v in result.values())
    unique_triggers = len(reverse_index)
    overlap_count = sum(1 for v in reverse_index.values() if len(v) > 1)

    db = {
        "meta": {
            "version": "1.0.0",
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_skills": total_skills,
            "total_triggers": total_triggers,
            "unique_triggers": unique_triggers,
            "overlap_triggers": overlap_count,
            "avg_per_skill": round(total_triggers / total_skills, 1) if total_skills else 0,
        },
        "skills": result,
        "skill_names_index": skill_names_index,
        "reverse_index": reverse_index,
        "skipped": [{"skill": s, "reason": r} for s, r in skipped],
        "errors": [{"skill": s, "error": str(e)} for s, e in errors],
    }

    return db

def save_db(db, output_path=None):
    """Save trigger database to file."""
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "trigger_db.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    return output_path

def load_db(path=None):
    """Load trigger database from file."""
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "trigger_db.json")
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def print_report(db):
    """Print a human-readable indexing report."""
    meta = db['meta']
    print("=" * 60)
    print("  🕷️  SPIDER WEB - Trigger Index Report")
    print("=" * 60)
    print(f"  Skills indexed:      {meta['total_skills']}")
    print(f"  Total triggers:      {meta['total_triggers']}")
    print(f"  Unique triggers:     {meta['unique_triggers']}")
    print(f"  Overlap triggers:    {meta['overlap_triggers']}")
    print(f"  Avg per skill:       {meta['avg_per_skill']}")
    print(f"  Skipped:             {len(db['skipped'])}")
    print(f"  Errors:              {len(db['errors'])}")
    print()

    # Top skills
    sorted_skills = sorted(db['skills'].items(), key=lambda x: len(x[1]), reverse=True)
    print("Top 20 skills by trigger count:")
    for i, (name, triggers) in enumerate(sorted_skills[:20]):
        preview = ', '.join(triggers[:3])
        print(f"  {i+1:2d}. {name:<35s} {len(triggers):3d} triggers | {preview}")

    # Overlap
    overlap_sorted = sorted(
        [(t, s) for t, s in db['reverse_index'].items() if len(s) > 1],
        key=lambda x: len(x[1]), reverse=True
    )
    if overlap_sorted:
        print(f"\nOverlapping triggers ({len(overlap_sorted)}):")
        for t, skills in overlap_sorted[:10]:
            print(f"  [{len(skills)} skills] '{t}' -> {skills}")

    # Skipped
    if db['skipped']:
        print(f"\nSkipped skills ({len(db['skipped'])}):")
        for item in db['skipped'][:10]:
            print(f"  - {item['skill']}: {item['reason'][:80]}")
        if len(db['skipped']) > 10:
            print(f"  ... and {len(db['skipped']) - 10} more")


def main():
    setup_encoding()
    skills_dir = os.path.expanduser("~/.workbuddy/skills/")
    output_path = os.path.join(os.path.dirname(__file__), "trigger_db.json")

    print("Scanning skills...")
    db = index_all_skills(skills_dir)
    path = save_db(db, output_path)
    print_report(db)
    print(f"\nDatabase saved to: {path}")
    print(f"Size: {os.path.getsize(path):,} bytes")


if __name__ == "__main__":
    main()
