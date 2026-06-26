#!/usr/bin/env python3
# analyze.py - Analyze unused skills and provide recommendations
# Usage: python3 analyze.py [--period 30] [--lang en|zh]

import json
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from path_utils import get_usage_file, get_registry_file
import i18n

RED = '\033[0;31m'
YELLOW = '\033[1;33m'
GREEN = '\033[0;32m'
BOLD = '\033[1m'
NC = '\033[0m'

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def reason_text(key, lang, **kw):
    return i18n.t(key, lang, **kw)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--period', type=int, default=30)
    parser.add_argument('--show-all', action='store_true')
    parser.add_argument('--lang', default=None, choices=['en', 'zh'])
    args = parser.parse_args()

    lang = args.lang or i18n.detect_lang()
    T = lambda k, **kw: i18n.t(k, lang, **kw)

    usage_data = load_json(get_usage_file()) or {"records": []}
    registry_data = load_json(get_registry_file()) or {"skills": []}

    records = usage_data.get("records", [])
    registry = registry_data.get("skills", [])

    now = datetime.now(timezone(timedelta(hours=8)))
    boundary = now - timedelta(days=args.period)

    filtered = []
    for r in records:
        try:
            ts = datetime.fromisoformat(r["timestamp"])
            if ts >= boundary:
                filtered.append(r)
        except (ValueError, TypeError):
            pass
    records = filtered

    skill_counts = {}
    for r in records:
        skill_counts[r["skill"]] = skill_counts.get(r["skill"], 0) + 1

    installed_skills = [s for s in registry if s.get("installed", False)]

    results = {"KEEP": [], "REVIEW": [], "UNINSTALL": []}

    for skill_obj in installed_skills:
        name = skill_obj["name"]
        count = skill_counts.get(name, 0)
        category = skill_obj.get("category", "unknown")
        access_type = skill_obj.get("access_type", "route")
        tags = skill_obj.get("tags", [])
        desc = skill_obj.get("description", "")

        score = 0
        reasons = []

        if access_type in ("tool", "script"):
            key = "reason_access_tool" if access_type == "tool" else "reason_access_script"
            results["REVIEW"].append({
                "skill": name, "count": count, "category": category,
                "description": desc,
                "reasons": [reason_text(key, lang)]
            })
            continue

        if category in ["agent", "security", "system"]:
            score += 2
            reasons.append(reason_text("reason_core_category", lang, cat=category))

        if count > 0:
            score += min(count * 2, 10)
            reasons.append(reason_text("reason_recently_used", lang, n=count))

        if skill_obj.get("use_cases"):
            score += 1
            reasons.append(reason_text("reason_has_use_cases", lang))

        critical_skills = ["proactive-agent", "agent-superpowers", "skill-vetter", "self-improving-agent"]
        if name in critical_skills:
            score += 5
            reasons.append(reason_text("reason_critical", lang))

        if count > 5:
            results["KEEP"].append({"skill": name, "count": count, "category": category, "description": desc, "reasons": reasons})
        elif count > 0:
            results["REVIEW"].append({"skill": name, "count": count, "category": category, "description": desc, "reasons": reasons})
        else:
            if "cron" in tags or category == "automation":
                score += 2
                reasons.append(reason_text("reason_scheduled", lang))
            if category in ["security", "vcs", "knowledge"]:
                score += 1
                reasons.append(reason_text("reason_specialized", lang))

            if score >= 3:
                results["REVIEW"].append({
                    "skill": name, "count": 0, "category": category,
                    "description": desc,
                    "reasons": reasons + [reason_text("reason_zero_but_keep", lang)]
                })
            else:
                results["UNINSTALL"].append({
                    "skill": name, "count": 0, "category": category,
                    "description": desc,
                    "reasons": reasons
                })

    for cat in results:
        results[cat].sort(key=lambda x: -x["count"])

    period_days = args.period
    sep = "=" * 65

    print(f"\n{sep}")
    title = T("analysis_title")
    print(f"  🔍 {title} ({T('period_days', n=period_days)})")
    print(sep)
    print(f"  {T('analyzed')} {now.strftime('%Y-%m-%d %H:%M')} ({T('beijing_time')})")
    print(f"  {T('period')} {T('last_n_days', n=period_days)}")
    print(f"  {T('total_records')} {len(filtered)}")
    print(f"  {T('installed_skills')} {len(installed_skills)}")
    print(f"  {T('active')} {len([s for s in installed_skills if skill_counts.get(s['name'], 0) > 0])}")
    print(f"  {T('zero_use')} {len([s for s in installed_skills if skill_counts.get(s['name'], 0) == 0])}")
    print(sep.replace("=", "-"))

    def print_section(title, emoji, color, items):
        none_text = T("none")
        desc_label = T("desc")
        cat_label = T("category")
        call_label = T("calls")
        unit = T("call_unit")
        reasons_label = T("reasons")
        no_desc = T("no_description")
        print(f"\n  {color}{emoji} {title} ({len(items)}){NC}")
        print("  " + "─" * 60)
        if not items:
            print(f"    ({none_text})")
            return
        for item in items:
            desc_short = item["description"][:45] if item["description"] else no_desc
            print(f"  {BOLD}▪ {item['skill']}{NC}")
            print(f"    {cat_label}: {item['category']} | {call_label}: {item['count']}{unit}")
            print(f"    {desc_label}: {desc_short}")
            if item["reasons"]:
                print(f"    {reasons_label}: {'; '.join(item['reasons'])}")
            print()

    print_section(T("keep"), "✅", GREEN, results["KEEP"])
    print_section(T("review"), "👀", YELLOW, results["REVIEW"])
    print_section(T("uninstall"), "🗑️", RED, results["UNINSTALL"])

    print(sep)
    unit = T("call_unit")
    print(f"  {T('summary')} {len(results['KEEP'])} {T('keep')} / {len(results['REVIEW'])} {T('review')} / {len(results['UNINSTALL'])} {T('uninstall')}")
    print(sep)

    if results["UNINSTALL"]:
        print(f"\n  💡 {T('uninstall_rec')}")
        no_desc = T("no_description")
        for item in results["UNINSTALL"]:
            desc_short = item["description"][:50] if item["description"] else no_desc
            print(f"    • {item['skill']} — {desc_short}")

if __name__ == "__main__":
    main()
