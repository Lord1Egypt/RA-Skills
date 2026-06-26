#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

GALIM = Path('/root/.openclaw/workspace/skills/webtop-galim/scripts/galim_fetch_tasks.py')
OFEK = Path('/root/.openclaw/workspace/skills/webtop-galim/scripts/fetch_tasks.py')
WEBTOP = Path('/root/.openclaw/workspace/skills/webtop-galim/scripts/webtop_fetch_summary.py')


def run_json(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    return json.loads(proc.stdout)


def add_ofek_details(lines, ofek_child, limit: int):
    urgent = ofek_child.get('urgent_activities') or []
    overdue = ofek_child.get('overdue_activities') or []

    if urgent:
        lines.append('  דחופות באופק:')
        for task in urgent[:limit]:
            teacher = f" | {task['teacher']}" if task.get('teacher') else ''
            lines.append(f"  - {task['title']}")
            lines.append(f"    {task['subject']}{teacher}")
            lines.append(f"    יעד: {task['due_at']}")

    if overdue:
        lines.append('  באיחור באופק:')
        for task in overdue[:limit]:
            teacher = f" | {task['teacher']}" if task.get('teacher') else ''
            lines.append(f"  - {task['title']}")
            lines.append(f"    {task['subject']}{teacher}")
            lines.append(f"    יעד: {task['due_at']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=30)
    ap.add_argument('--limit', type=int, default=8)
    args = ap.parse_args()

    galim = run_json([sys.executable, str(GALIM), '--json', '--hide-overdue', '--due-within-days', str(args.days)])
    ofek = run_json([sys.executable, str(OFEK), '--json'])
    webtop = run_json([sys.executable, str(WEBTOP)])

    ofek_by_child = {x['child_name']: x for x in ofek}

    lines = ['📚 *דוח מורחב - תלמידים*', '']
    for child in galim:
        name = child['child_name']
        lines.append(f'👤 *{name}*')
        if child.get('success'):
            lines.append(f"גלים: {child.get('task_count', 0)} משימות רלוונטיות")
            for task in child.get('tasks', [])[:args.limit]:
                lines.append(f"- {task['title']}")
                lines.append(f"  {task['subject']} | {task['task_type']}")
                lines.append(f"  יעד: {task['due_at']}")
        else:
            lines.append(f"גלים: ❌ {child.get('error','שגיאה')}")

        o = ofek_by_child.get(name)
        if o and not o.get('error'):
            lines.append(
                f"אופק: לביצוע {o.get('open_count', '?')}, לתיקון {o.get('fix_count', '?')}, "
                f"ממתינות {o.get('waiting_count', '?')}, נבדקו {o.get('checked_count', '?')}"
            )
            add_ofek_details(lines, o, args.limit)
        else:
            lines.append(f"אופק: ❌ {o.get('error') if o else 'אין נתונים'}")
        lines.append('')

    lines.append('📝 *וובטופ*')
    raw = (webtop.get('raw_text') or '').strip()
    lines.append(raw or 'אין נתונים')
    print('\n'.join(lines).strip())


if __name__ == '__main__':
    main()
