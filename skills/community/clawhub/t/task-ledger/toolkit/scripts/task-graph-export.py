#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / 'tasks'
OPEN_STATUSES = {'pending', 'running', 'waiting', 'blocked', 'partial'}


def die(msg, code=1):
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def load_all():
    tasks = {}
    for path in sorted(TASKS_DIR.glob('*.json')):
        try:
            tasks[path.stem] = json.loads(path.read_text())
        except Exception:
            continue
    return tasks


def graph_markdown(tasks, only_open=False):
    items = []
    for task_id, data in sorted(tasks.items()):
        status = data.get('status')
        if only_open and status not in OPEN_STATUSES:
            continue
        items.append((task_id, data))

    lines = ['# Task Graph', '']
    for task_id, data in items:
        title = data.get('title', task_id)
        status = data.get('status', '-')
        stage = data.get('stage', '-')
        parent = data.get('parentTaskId') or '-'
        children = data.get('childTaskIds') or []
        deps = data.get('dependsOn') or []
        blocked = data.get('blockedBy') or []
        lines.append(f"## {task_id}")
        lines.append('')
        lines.append(f"- **Title:** {title}")
        lines.append(f"- **Status:** `{status}`")
        lines.append(f"- **Stage:** `{stage}`")
        lines.append(f"- **Parent:** {parent}")
        lines.append(f"- **Children:** {', '.join(children) if children else '-'}")
        lines.append(f"- **Depends On:** {', '.join(deps) if deps else '-'}")
        lines.append(f"- **Blocked By:** {', '.join(blocked) if blocked else '-'}")
        lines.append('')
    return '\n'.join(lines) + '\n'


def graph_dot(tasks, only_open=False):
    lines = ['digraph task_graph {', '  rankdir=LR;', '  node [shape=box, style=rounded];']
    included = {}
    for task_id, data in sorted(tasks.items()):
        status = data.get('status')
        if only_open and status not in OPEN_STATUSES:
            continue
        label = f"{task_id}\\n{status}\\n{data.get('stage', '-') }"
        lines.append(f'  "{task_id}" [label="{label}"];')
        included[task_id] = data
    for task_id, data in included.items():
        parent = data.get('parentTaskId')
        if parent and parent in included:
            lines.append(f'  "{parent}" -> "{task_id}" [label="child", color="blue"];')
        for dep in data.get('dependsOn') or []:
            if dep in included:
                lines.append(f'  "{dep}" -> "{task_id}" [label="depends", style="dashed", color="darkgreen"];')
    lines.append('}')
    return '\n'.join(lines) + '\n'


args = sys.argv[1:]
fmt = 'markdown'
only_open = False
while args:
    arg = args.pop(0)
    if arg == '--format':
        if not args:
            die('--format requires markdown|dot|json')
        fmt = args.pop(0)
    elif arg == '--open-only':
        only_open = True
    else:
        die('Usage: task-graph-export.py [--format markdown|dot|json] [--open-only]')

if fmt not in {'markdown', 'dot', 'json'}:
    die('format must be markdown, dot, or json')

tasks = load_all()
if fmt == 'json':
    payload = {}
    for task_id, data in tasks.items():
        if only_open and data.get('status') not in OPEN_STATUSES:
            continue
        payload[task_id] = {
            'status': data.get('status'),
            'stage': data.get('stage'),
            'parentTaskId': data.get('parentTaskId'),
            'childTaskIds': data.get('childTaskIds', []),
            'dependsOn': data.get('dependsOn', []),
            'blockedBy': data.get('blockedBy', []),
        }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
elif fmt == 'dot':
    print(graph_dot(tasks, only_open), end='')
else:
    print(graph_markdown(tasks, only_open), end='')
