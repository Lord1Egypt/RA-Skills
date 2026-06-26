#!/usr/bin/env python3
# report.py - Generate skill usage frequency report
# Usage: python3 report.py [--period today|week|month|all] [--format text|json] [--lang en|zh]

import json
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from path_utils import get_usage_file, get_registry_file
import i18n

CAT_EMOJI = {
    "development": "🔧", "agent": "🤖", "security": "🔒",
    "integration": "🔗", "automation": "⚙️", "utility": "🛠️",
    "search": "🔍", "vcs": "📦", "knowledge": "🧠", "multimodal": "🎨"
}

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--period', default='all', choices=['today', 'week', 'month', 'all'])
    parser.add_argument('--format', default='text', choices=['text', 'json'])
    parser.add_argument('--lang', default=None, choices=['en', 'zh'])
    args = parser.parse_args()

    lang = args.lang or i18n.detect_lang()
    T = lambda k, **kw: i18n.t(k, lang, **kw)

    usage_data = load_json(get_usage_file())
    registry_data = load_json(get_registry_file())

    if not usage_data:
        print(f"Error: usage data not found at {get_usage_file()}")
        sys.exit(1)

    records = usage_data.get("records", [])
    registry = registry_data.get("skills", []) if registry_data else []

    now = datetime.now(timezone(timedelta(hours=8)))

    if args.period == "today":
        boundary = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif args.period == "week":
        boundary = now - timedelta(days=7)
    elif args.period == "month":
        boundary = now - timedelta(days=30)
    else:
        boundary = None

    if boundary:
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
    skill_success = {}
    skill_failed = {}
    for r in records:
        skill = r["skill"]
        skill_counts[skill] = skill_counts.get(skill, 0) + 1
        outcome = r.get("outcome", "success")
        if outcome == "success":
            skill_success[skill] = skill_success.get(skill, 0) + 1
        elif outcome in ("failed", "error"):
            skill_failed[skill] = skill_failed.get(skill, 0) + 1

    skill_meta = {}
    for s in registry:
        skill_meta[s["name"]] = {
            "category": s.get("category", "unknown"),
            "installed": s.get("installed", True),
            "description": s.get("description", ""),
        }

    sorted_skills = sorted(skill_counts.items(), key=lambda x: -x[1])
    period_key = args.period
    period_label = {"today": T("report_title"), "week": T("report_title"), "month": T("report_title"), "all": T("report_title")}[period_key]
    period_text_map = {"today": {"en": "Today", "zh": "今日"}, "week": {"en": "This week", "zh": "本周"}, "month": {"en": "This month", "zh": "本月"}, "all": {"en": "All time", "zh": "全部时间"}}
    period_text = period_text_map.get(args.period, {}).get(lang, args.period)

    if args.format == "json":
        output = {
            "period": args.period,
            "period_label": period_text,
            "generated_at": now.isoformat(),
            "total_calls": len(records),
            "unique_skills_used": len(skill_counts),
            "skill_counts": [
                {
                    "skill": skill,
                    "count": count,
                    "category": skill_meta.get(skill, {}).get("category", "unknown"),
                    "installed": skill_meta.get(skill, {}).get("installed", True)
                }
                for skill, count in sorted_skills
            ]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  📊 {T('report_title')} — {period_text}")
    print(f"{sep}")
    print(f"  {T('generated')} {now.strftime('%Y-%m-%d %H:%M')} ({T('beijing_time')})")
    print(f"  {T('total_calls')} {len(records)}")
    print(f"  {T('active_skills')} {len(skill_counts)}")
    print(f"{sep.replace('=', '-')}")

    if not sorted_skills:
        print(f"  ({T('none')})")
    else:
        cats = {}
        for skill, count in sorted_skills:
            cat = skill_meta.get(skill, {}).get("category", "unknown")
            if cat not in cats:
                cats[cat] = []
            cats[cat].append((skill, count))

        for cat, items in cats.items():
            emoji = CAT_EMOJI.get(cat, "📁")
            cat_label = i18n.cat_name(cat, lang)
            print(f"\n  {emoji} {cat_label}")
            for skill, count in items:
                bar = "█" * min(count, 20)
                installed = "✅" if skill_meta.get(skill, {}).get("installed", True) else "❌"
                ok = skill_success.get(skill, 0)
                fail = skill_failed.get(skill, 0)
                unit = T("call_unit")
                if fail > 0:
                    pct = int(ok / count * 100) if count > 0 else 0
                    rate = f"📗{ok} 📕{fail} ({pct}%)"
                elif ok > 0:
                    rate = f"📗{ok}"
                else:
                    rate = ""
                print(f"    {installed} {skill:<35} {count:>3}{unit}  {bar}  {rate}")

    if sorted_skills:
        print(f"\n{sep.replace('=', '-')}")
        print(f"  🏆 {T('top_skills')}:")
        for i, (skill, count) in enumerate(sorted_skills[:3], 1):
            desc = skill_meta.get(skill, {}).get("description", "")[:40]
            unit = T("call_unit")
            print(f"     {i}. {skill} ({count}{unit}) — {desc}")

        registry_names = [s["name"] for s in registry if s.get("installed", True)]
        zero_skills = [s for s in registry_names if s not in skill_counts]
        if zero_skills:
            print(f"\n  😴 {T('unused_skills')} ({len(zero_skills)}):")
            for s in zero_skills[:5]:
                print(f"     — {s}")
            if len(zero_skills) > 5:
                n_others = len(zero_skills) - 5
                print(f"     ... {T('and_n_others', n=n_others)}")

    print(f"\n{sep}")

if __name__ == "__main__":
    main()
