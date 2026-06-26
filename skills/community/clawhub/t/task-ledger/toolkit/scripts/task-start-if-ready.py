#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / 'tasks'
STARTABLE = {'pending', 'waiting', 'blocked'}
READY_STATES = {'ready', 'ready-with-failures'}


def iso_now_local():
    return datetime.now().astimezone().isoformat(timespec='milliseconds')


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


def get_readiness_config(data):
    readiness = data.get('readiness') or {}
    return {
        'successPolicy': readiness.get('successPolicy', 'all-succeeded'),
        'allowStartWhen': readiness.get('allowStartWhen', 'deps-satisfied'),
        'allowPartialDependencies': readiness.get('allowPartialDependencies', False),
    }


def evaluate(task_id, tasks):
    data = tasks[task_id]
    deps = data.get('dependsOn') or []
    cfg = get_readiness_config(data)
    missing = []
    unsatisfied = []
    waiting = []
    satisfied = []
    closed = []
    for dep in deps:
        dep_task = tasks.get(dep)
        if dep_task is None:
            missing.append(dep)
            continue
        dep_status = dep_task.get('status')
        row = {'taskId': dep, 'status': dep_status}
        if dep_status == 'succeeded':
            satisfied.append(row)
            closed.append(row)
            continue
        if dep_status in {'succeeded', 'failed', 'cancelled', 'partial'}:
            closed.append(row)
        if dep_status in {'failed', 'cancelled'}:
            unsatisfied.append(row)
        else:
            waiting.append(row)

    policy = cfg['successPolicy']
    allow_start_when = cfg['allowStartWhen']
    allow_partial = cfg['allowPartialDependencies']

    if missing:
        readiness = 'missing-deps'
    elif policy == 'all-succeeded':
        if unsatisfied:
            readiness = 'unsatisfied'
        elif waiting:
            readiness = 'waiting-deps'
        else:
            readiness = 'ready'
    elif policy == 'fail-fast':
        if unsatisfied:
            readiness = 'unsatisfied'
        elif waiting:
            readiness = 'waiting-deps'
        else:
            readiness = 'ready'
    elif policy == 'wait-all':
        if waiting:
            readiness = 'waiting-deps'
        elif unsatisfied:
            readiness = 'ready-with-failures' if allow_partial else 'unsatisfied'
        else:
            readiness = 'ready'
    elif policy == 'partial-allowed':
        if allow_start_when == 'deps-closed':
            if len(closed) == len(deps):
                readiness = 'ready'
            elif waiting:
                readiness = 'waiting-deps'
            else:
                readiness = 'ready'
        else:
            if satisfied:
                readiness = 'ready'
            elif waiting:
                readiness = 'waiting-deps'
            elif unsatisfied:
                readiness = 'ready-with-failures' if allow_partial else 'unsatisfied'
            else:
                readiness = 'ready'
    else:
        die(f'invalid readiness successPolicy: {policy}')
    return readiness, cfg, missing, satisfied, closed, unsatisfied, waiting


if len(sys.argv) not in {2, 3}:
    die(f"Usage: {Path(sys.argv[0]).name} <taskId> [nextAction]")

task_id = sys.argv[1]
next_action_override = sys.argv[2] if len(sys.argv) == 3 else None
path = TASKS_DIR / f"{task_id}.json"
if not path.exists():
    die(f"Task not found: {task_id}", 2)

tasks = load_all()
if task_id not in tasks:
    die(f"Task not found: {task_id}", 2)

data = tasks[task_id]
if data.get('status') not in STARTABLE:
    die(f"task status is not startable: {data.get('status')}")

readiness, cfg, missing, satisfied, closed, unsatisfied, waiting = evaluate(task_id, tasks)
if readiness not in READY_STATES:
    details = {
        'readiness': readiness,
        'config': cfg,
        'missing': missing,
        'satisfied': satisfied,
        'closed': closed,
        'unsatisfied': unsatisfied,
        'waiting': waiting,
    }
    print(json.dumps(details, ensure_ascii=False, indent=2))
    raise SystemExit(3)

stages = data.get('stages', [])
current_stage_id = data.get('stage')
current_stage = None
for st in stages:
    if st.get('id') == current_stage_id:
        current_stage = st
        break
if current_stage is None:
    die(f'current stage not found: {current_stage_id}')

old_status = data.get('status')
old_stage_status = current_stage.get('status')
ts = iso_now_local()
if data.get('startedAt') is None:
    data['startedAt'] = ts
data['status'] = 'running'
if current_stage.get('status') == 'todo':
    current_stage['status'] = 'running'
if next_action_override is not None:
    data['nextAction'] = next_action_override

data['updatedAt'] = ts
data.setdefault('events', []).append({
    'ts': ts,
    'type': 'task.started',
    'message': 'Task started via task-start-if-ready.py',
    'details': {
        'oldStatus': old_status,
        'newStatus': data['status'],
        'stage': current_stage_id,
        'oldStageStatus': old_stage_status,
        'newStageStatus': current_stage.get('status'),
        'readiness': readiness,
        'readinessConfig': cfg,
        'nextAction': data.get('nextAction'),
    },
})

path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print(f'Started task: {task_id}')
