#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / 'tasks'
OPEN_STATUSES = {'pending', 'running', 'waiting', 'blocked', 'partial'}

rows = {}
children = {}
roots = []

for path in sorted(TASKS_DIR.glob('*.json')):
    try:
        data = json.loads(path.read_text())
    except Exception:
        continue
    task_id = data.get('taskId', path.stem)
    rows[task_id] = data

for task_id, data in rows.items():
    parent = data.get('parentTaskId')
    if parent and parent in rows:
        children.setdefault(parent, []).append(task_id)
    else:
        roots.append(task_id)

for key in children:
    children[key].sort()
roots.sort()


def label(task_id):
    data = rows[task_id]
    status = data.get('status', '-')
    stage = data.get('stage', '-')
    title = data.get('title', '-')
    dep = data.get('dependsOn') or []
    dep_txt = f" deps={len(dep)}" if dep else ''
    return f"{task_id} [{status}] ({stage}) {title}{dep_txt}"


def walk(task_id, prefix='', seen=None):
    seen = seen or set()
    cycle = task_id in seen
    print(prefix + label(task_id) + (' [cycle]' if cycle else ''))
    if cycle:
        return
    seen = set(seen)
    seen.add(task_id)
    kids = children.get(task_id, [])
    for idx, child in enumerate(kids):
        branch = '└─ ' if idx == len(kids) - 1 else '├─ '
        next_prefix = prefix + ('   ' if idx == len(kids) - 1 else '│  ')
        walk(child, prefix + branch, seen)

open_roots = [rid for rid in roots if rows[rid].get('status') in OPEN_STATUSES or children.get(rid)]
if not open_roots:
    print('No task tree to show.')
    raise SystemExit(0)

for idx, root in enumerate(open_roots):
    walk(root)
    if idx != len(open_roots) - 1:
        print()
