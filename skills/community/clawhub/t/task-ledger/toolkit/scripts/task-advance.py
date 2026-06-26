#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / 'tasks'


def iso_now_local():
    return datetime.now().astimezone().isoformat(timespec='milliseconds')


def die(msg, code=1):
    print(msg, file=sys.stderr)
    raise SystemExit(code)


if len(sys.argv) < 2:
    die(f"Usage: {Path(sys.argv[0]).name} <taskId> [nextAction]")

task_id = sys.argv[1]
next_action_override = sys.argv[2] if len(sys.argv) >= 3 else None
path = TASKS_DIR / f"{task_id}.json"
if not path.exists():
    die(f"Task not found: {task_id}", 2)

data = json.loads(path.read_text())
stages = data.get('stages', [])
if not stages:
    die('Task has no stages')

# Backfill 0.2 fields for older tasks.
data.setdefault('startedAt', None)
data.setdefault('completedAt', None)
data.setdefault('lastVerifiedAt', None)
data.setdefault('workingSummary', '')
current_stage_id = data.get('stage')
current_index = None
for i, stage in enumerate(stages):
    if stage.get('id') == current_stage_id:
        current_index = i
        break
if current_index is None:
    die(f'Current stage not found in stages: {current_stage_id}')

old_status = data.get('status')
ts = iso_now_local()
if data.get('startedAt') is None:
    data['startedAt'] = ts
if old_status in {'pending', 'waiting', 'blocked'}:
    data['status'] = 'running'

current_stage = stages[current_index]
old_current_status = current_stage.get('status')
if old_current_status in {'todo', 'running'}:
    current_stage['status'] = 'done'

old_stage = current_stage_id
new_stage = current_stage_id
next_stage = stages[current_index + 1] if current_index + 1 < len(stages) else None

if next_stage is not None:
    old_next_status = next_stage.get('status')
    if old_next_status == 'todo':
        next_stage['status'] = 'running'
    data['stage'] = next_stage.get('id')
    new_stage = data['stage']
    data['nextAction'] = next_action_override if next_action_override is not None else f"Start {next_stage.get('id')}"
else:
    old_next_status = None
    data['stage'] = None
    new_stage = None
    data['nextAction'] = next_action_override if next_action_override is not None else 'No further stages; close the task when validation is complete'

stage_changes = [
    {'id': current_stage_id, 'old': old_current_status, 'new': current_stage.get('status')},
]
if next_stage is not None:
    stage_changes.append({'id': next_stage.get('id'), 'old': old_next_status, 'new': next_stage.get('status')})

data['updatedAt'] = ts
data.setdefault('events', []).append({
    'ts': ts,
    'type': 'stage.completed',
    'message': f'Completed stage {current_stage_id}',
    'details': {
        'stage': current_stage_id,
        'oldStatus': old_current_status,
        'newStatus': current_stage.get('status'),
    },
})
if next_stage is not None:
    data.setdefault('events', []).append({
        'ts': ts,
        'type': 'stage.started',
        'message': f'Started stage {next_stage.get("id")}',
        'details': {
            'stage': next_stage.get('id'),
            'oldStatus': old_next_status,
            'newStatus': next_stage.get('status'),
        },
    })

data.setdefault('events', []).append({
    'ts': ts,
    'type': 'task.updated',
    'message': 'Task advanced via task-advance.py',
    'details': {
        'oldStage': old_stage,
        'newStage': new_stage,
        'oldStatus': old_status,
        'newStatus': data.get('status'),
        'stageChanges': stage_changes,
        'nextAction': data.get('nextAction'),
    },
})

path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print(f"Advanced task: {task_id} ({old_stage} -> {new_stage})")
