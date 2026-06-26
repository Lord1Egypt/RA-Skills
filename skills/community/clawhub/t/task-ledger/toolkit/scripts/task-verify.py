#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / 'tasks'
VALID_STATUSES = {'pending', 'running', 'waiting', 'blocked', 'succeeded', 'failed', 'cancelled', 'partial'}
ACTIVE_STATUSES = {'running', 'waiting', 'blocked', 'partial'}


def iso_now_local():
    return datetime.now().astimezone().isoformat(timespec='milliseconds')


def die(msg, code=1):
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def find_stage(data, stage_id):
    for st in data.get('stages', []):
        if st.get('id') == stage_id:
            return st
    return None


if len(sys.argv) < 3:
    die(f"Usage: {Path(sys.argv[0]).name} <taskId> <summary> [--correct-status <status>] [--correct-stage <stageId>] [--working-summary <text>]")

task_id = sys.argv[1]
summary = sys.argv[2]
args = sys.argv[3:]

path = TASKS_DIR / f"{task_id}.json"
if not path.exists():
    die(f"Task not found: {task_id}", 2)

data = json.loads(path.read_text())
data.setdefault('lastVerifiedAt', None)
data.setdefault('workingSummary', '')
data.setdefault('startedAt', None)

correct_status = None
correct_stage = None
working_summary = None

i = 0
while i < len(args):
    arg = args[i]
    if arg == '--correct-status':
        i += 1
        if i >= len(args): die('--correct-status requires a value')
        correct_status = args[i]
        if correct_status not in VALID_STATUSES:
            die(f'invalid status: {correct_status}')
    elif arg == '--correct-stage':
        i += 1
        if i >= len(args): die('--correct-stage requires a value')
        correct_stage = args[i]
        if find_stage(data, correct_stage) is None:
            die(f'stage not found: {correct_stage}')
    elif arg == '--working-summary':
        i += 1
        if i >= len(args): die('--working-summary requires a value')
        working_summary = args[i]
    else:
        die(f'unknown argument: {arg}')
    i += 1

ts = iso_now_local()
changes = {}
old_status = data.get('status')
old_stage = data.get('stage')
old_started = data.get('startedAt')
if correct_status and correct_status != old_status:
    data['status'] = correct_status
    changes['status'] = {'old': old_status, 'new': correct_status}
if correct_stage and correct_stage != old_stage:
    data['stage'] = correct_stage
    changes['stage'] = {'old': old_stage, 'new': correct_stage}
if working_summary is not None:
    data['workingSummary'] = working_summary

if data.get('startedAt') is None and (correct_status in ACTIVE_STATUSES or data.get('status') in ACTIVE_STATUSES):
    data['startedAt'] = ts
    changes['startedAt'] = {'old': old_started, 'new': ts}

old_verified = data.get('lastVerifiedAt')
data['lastVerifiedAt'] = ts
data['updatedAt'] = ts

data.setdefault('events', []).append({
    'ts': ts,
    'type': 'recovery.checked',
    'message': 'Verified real state before resuming',
    'details': {
        'summary': summary,
        'oldLastVerifiedAt': old_verified,
        'newLastVerifiedAt': ts,
    },
})

if changes:
    data.setdefault('events', []).append({
        'ts': ts,
        'type': 'recovery.corrected',
        'message': 'Corrected task state to match reality',
        'details': changes,
    })

path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print(f'Verified task reality: {task_id}')
