#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / 'tasks'
VALID_FINAL = {'succeeded', 'failed', 'cancelled', 'partial'}


def iso_now_local():
    return datetime.now().astimezone().isoformat(timespec='milliseconds')


def die(msg, code=1):
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def append_event(data, ts, event_type, message, details=None):
    data.setdefault('events', []).append({
        'ts': ts,
        'type': event_type,
        'message': message,
        'details': details or {},
    })


if len(sys.argv) < 3:
    die(f"Usage: {Path(sys.argv[0]).name} <taskId> <final-status> [summary]")

task_id = sys.argv[1]
final_status = sys.argv[2]
summary = sys.argv[3] if len(sys.argv) >= 4 else None

if final_status not in VALID_FINAL:
    die(f"invalid final status: {final_status}")

path = TASKS_DIR / f"{task_id}.json"
if not path.exists():
    die(f"Task not found: {task_id}", 2)

data = json.loads(path.read_text())
old_status = data.get('status')
ts = iso_now_local()

data['status'] = final_status
data['updatedAt'] = ts
data['completedAt'] = ts
if not data.get('startedAt'):
    data['startedAt'] = ts

data.setdefault('notifications', {})['notifiedCompletion'] = False

if final_status in {'succeeded', 'partial', 'cancelled'}:
    data['error'] = None
if final_status in {'failed', 'cancelled'}:
    data['result'] = None

if summary:
    if final_status == 'failed':
        data['error'] = data.get('error') or {}
        if isinstance(data['error'], dict):
            data['error']['summary'] = summary
        else:
            data['error'] = {'summary': summary}
    else:
        data['result'] = data.get('result') or {}
        if isinstance(data['result'], dict):
            data['result']['summary'] = summary
        else:
            data['result'] = {'summary': summary}

stage_cleanup = []
for stage in data.get('stages', []):
    old = stage.get('status')
    new = old
    if old == 'running':
        if final_status in {'succeeded', 'partial'}:
            new = 'done'
        elif final_status == 'cancelled':
            new = 'skipped'
        elif final_status == 'failed':
            new = 'failed'
    elif old == 'todo':
        new = 'skipped'
    if new != old:
        stage['status'] = new
        stage_cleanup.append({'id': stage.get('id'), 'old': old, 'new': new})

append_event(data, ts, 'task.closed', 'Task closed via close-task.py', {
    'oldStatus': old_status,
    'newStatus': final_status,
    'summary': summary,
    'stageCleanup': stage_cleanup,
})

path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print(f"Closed task: {task_id} -> {final_status}")
