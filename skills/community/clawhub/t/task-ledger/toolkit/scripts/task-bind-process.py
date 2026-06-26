#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / 'tasks'
VALID_STATES = {'running', 'exited', 'unknown'}


def iso_now_local():
    return datetime.now().astimezone().isoformat(timespec='milliseconds')


def die(msg, code=1):
    print(msg, file=sys.stderr)
    raise SystemExit(code)


if len(sys.argv) < 3:
    die(f"Usage: {Path(sys.argv[0]).name} <taskId> <processSessionId> [pid] [--state running|exited|unknown]")

task_id = sys.argv[1]
process_session_id = sys.argv[2]
pid = None
state = None
args = sys.argv[3:]
i = 0
while i < len(args):
    arg = args[i]
    if arg == '--state':
        i += 1
        if i >= len(args):
            die('--state requires a value')
        state = args[i]
        if state not in VALID_STATES:
            die(f'invalid process state: {state}')
    else:
        if pid is not None:
            die('pid may only be provided once')
        try:
            pid = int(arg)
        except ValueError:
            die('pid must be an integer')
    i += 1

path = TASKS_DIR / f"{task_id}.json"
if not path.exists():
    die(f"Task not found: {task_id}", 2)

data = json.loads(path.read_text())
old_process = dict(data.get('process') or {})
data.setdefault('process', {})['sessionId'] = process_session_id
if pid is not None:
    data['process']['pid'] = pid
if state is not None:
    data['process']['state'] = state

ts = iso_now_local()
data['updatedAt'] = ts
data.setdefault('events', []).append({
    'ts': ts,
    'type': 'process.bound',
    'message': 'Background process bound to task',
    'details': {
        'oldProcess': old_process,
        'newProcess': data['process'],
    },
})

path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print(f"Bound process to task: {task_id} -> {process_session_id}")
