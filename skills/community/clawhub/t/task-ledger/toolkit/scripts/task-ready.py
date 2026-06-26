#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / 'tasks'
SATISFIED = {'succeeded'}
CLOSED = {'succeeded', 'failed', 'cancelled', 'partial'}
UNSATISFIABLE = {'failed', 'cancelled'}
ACTIVE = {'pending', 'running', 'waiting', 'blocked', 'partial'}


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
    if task_id not in tasks:
        die(f'Task not found: {task_id}', 2)
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
        if dep_status in SATISFIED:
            satisfied.append(row)
            closed.append(row)
            continue
        if dep_status in CLOSED:
            closed.append(row)
        if dep_status in UNSATISFIABLE:
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

    return {
        'taskId': task_id,
        'status': data.get('status'),
        'currentStage': data.get('stage'),
        'dependsOn': deps,
        'readiness': readiness,
        'config': cfg,
        'missing': missing,
        'satisfied': satisfied,
        'closed': closed,
        'unsatisfied': unsatisfied,
        'waiting': waiting,
    }


if len(sys.argv) not in {2, 3}:
    die(f"Usage: {Path(sys.argv[0]).name} <taskId> [--json]")

task_id = sys.argv[1]
as_json = len(sys.argv) == 3 and sys.argv[2] == '--json'
if len(sys.argv) == 3 and not as_json:
    die('only --json is supported as optional argument')

result = evaluate(task_id, load_all())
if as_json:
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0)

print(f"Task: {result['taskId']}")
print(f"Status: {result['status']}")
print(f"Stage: {result['currentStage']}")
print(f"Readiness: {result['readiness']}")
print(f"Policy: {result['config']['successPolicy']}")
print(f"Allow Start When: {result['config']['allowStartWhen']}")
print(f"Allow Partial Dependencies: {result['config']['allowPartialDependencies']}")
if result['dependsOn']:
    print('Dependencies:')
    for dep in result['dependsOn']:
        print(f"- {dep}")
if result['missing']:
    print('Missing dependencies:')
    for dep in result['missing']:
        print(f"- {dep}")
if result['satisfied']:
    print('Satisfied dependencies:')
    for dep in result['satisfied']:
        print(f"- {dep['taskId']} [{dep['status']}]")
if result['unsatisfied']:
    print('Unsatisfied dependencies:')
    for dep in result['unsatisfied']:
        print(f"- {dep['taskId']} [{dep['status']}]")
if result['waiting']:
    print('Waiting on dependencies:')
    for dep in result['waiting']:
        print(f"- {dep['taskId']} [{dep['status']}]")
