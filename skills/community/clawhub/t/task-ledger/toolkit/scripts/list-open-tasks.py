#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / 'tasks'
OPEN_STATUSES = {'running', 'waiting', 'blocked', 'partial'}
SATISFIED = {'succeeded'}
UNSATISFIABLE = {'failed', 'cancelled'}


def readiness_for(task_id, data, tasks):
    deps = data.get('dependsOn') or []
    if not deps:
        return 'ready'
    missing = [dep for dep in deps if dep not in tasks]
    if missing:
        return 'missing-deps'
    unsatisfied = [dep for dep in deps if tasks[dep].get('status') in UNSATISFIABLE]
    if unsatisfied:
        return 'unsatisfied'
    waiting = [dep for dep in deps if tasks[dep].get('status') not in SATISFIED]
    if waiting:
        return 'waiting-deps'
    return 'ready'


tasks = {}
for path in sorted(TASKS_DIR.glob('*.json')):
    try:
        tasks[path.stem] = json.loads(path.read_text())
    except Exception:
        continue

rows = []
for path in sorted(TASKS_DIR.glob('*.json')):
    try:
        data = json.loads(path.read_text())
    except Exception as e:
        rows.append((path.name, 'INVALID', '-', '-', '-', '-', '-', f'parse error: {e}'))
        continue

    status = data.get('status', '-')
    if status not in OPEN_STATUSES:
        continue
    task_id = data.get('taskId', path.stem)
    rows.append((
        task_id,
        status,
        readiness_for(task_id, data, tasks),
        data.get('stage', '-'),
        data.get('executionMode', '-'),
        data.get('parentTaskId') or '-',
        len(data.get('dependsOn') or []),
        data.get('title', '-')
    ))

if not rows:
    print('No open tasks.')
    raise SystemExit(0)

w1 = max(len(str(r[0])) for r in rows + [('TASK ID', '', '', '', '', '', '', '')])
w2 = max(len(str(r[1])) for r in rows + [('', 'STATUS', '', '', '', '', '', '')])
w3 = max(len(str(r[2])) for r in rows + [('', '', 'READY', '', '', '', '', '')])
w4 = max(len(str(r[3])) for r in rows + [('', '', '', 'STAGE', '', '', '', '')])
w5 = max(len(str(r[4])) for r in rows + [('', '', '', '', 'MODE', '', '', '')])
w6 = max(len(str(r[5])) for r in rows + [('', '', '', '', '', 'PARENT', '', '')])
w7 = max(len(str(r[6])) for r in rows + [('', '', '', '', '', '', 'DEPS', '')])

print(f"{'TASK ID'.ljust(w1)}  {'STATUS'.ljust(w2)}  {'READY'.ljust(w3)}  {'STAGE'.ljust(w4)}  {'MODE'.ljust(w5)}  {'PARENT'.ljust(w6)}  {'DEPS'.ljust(w7)}  TITLE")
print(f"{'-'*w1}  {'-'*w2}  {'-'*w3}  {'-'*w4}  {'-'*w5}  {'-'*w6}  {'-'*w7}  {'-'*20}")
for task_id, status, ready, stage, mode, parent, deps, title in rows:
    print(f"{str(task_id).ljust(w1)}  {str(status).ljust(w2)}  {str(ready).ljust(w3)}  {str(stage).ljust(w4)}  {str(mode).ljust(w5)}  {str(parent).ljust(w6)}  {str(deps).ljust(w7)}  {title}")
