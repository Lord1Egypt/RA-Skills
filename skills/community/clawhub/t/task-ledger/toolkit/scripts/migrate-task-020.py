#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / 'tasks'
CLOSED = {'succeeded', 'failed', 'cancelled', 'partial'}
VALID_ROLLBACK = {'not-applicable', 'available', 'in-progress', 'completed', 'failed', 'not-needed'}


def iso_now_local():
    return datetime.now().astimezone().isoformat(timespec='milliseconds')


def load_paths(args):
    if not args:
        return sorted(TASKS_DIR.glob('*.json'))
    out = []
    for a in args:
        p = TASKS_DIR / f'{a}.json'
        if not p.exists():
            print(f'skip missing task: {a}', file=sys.stderr)
            continue
        out.append(p)
    return out


paths = load_paths(sys.argv[1:])
if not paths:
    print('No task files selected.')
    raise SystemExit(0)

migrated = 0
for path in paths:
    data = json.loads(path.read_text())
    ts = iso_now_local()
    task_id = data.get('taskId', path.stem)
    changes = []
    stage_cleanup = []

    def ensure(field, value):
        if field not in data:
            data[field] = value
            changes.append(field)

    ensure('priority', 'normal')
    ensure('startedAt', None)
    ensure('completedAt', None)
    ensure('lastVerifiedAt', None)
    ensure('owner', data.get('ownerSession', 'main'))
    ensure('assignedAgent', None)
    ensure('dependsOn', [])
    ensure('blockedBy', [])
    ensure('blockedReason', None)
    ensure('decisionNotes', '')
    ensure('workingSummary', '')

    if 'artifacts' in data and isinstance(data['artifacts'], dict) and 'files' not in data['artifacts']:
        data['artifacts']['files'] = []
        changes.append('artifacts.files')

    rollback = data.get('rollback')
    if rollback is None or not isinstance(rollback, dict):
        data['rollback'] = {
            'available': False,
            'strategy': None,
            'status': 'not-applicable',
            'artifacts': [],
        }
        changes.append('rollback')
    else:
        if rollback.get('status') not in VALID_ROLLBACK:
            rollback['status'] = 'not-applicable'
            changes.append('rollback.status')
        rollback.setdefault('available', False)
        rollback.setdefault('strategy', None)
        rollback.setdefault('artifacts', [])

    notifications = data.get('notifications')
    if notifications is None or not isinstance(notifications, dict):
        data['notifications'] = {
            'notifiedStart': data.get('notifiedStart', False),
            'notifiedCompletion': data.get('notifiedCompletion', False),
            'notifiedRecovery': False,
        }
        changes.append('notifications')
    else:
        notifications.setdefault('notifiedStart', data.get('notifiedStart', False))
        notifications.setdefault('notifiedCompletion', data.get('notifiedCompletion', False))
        notifications.setdefault('notifiedRecovery', False)

    status = data.get('status')
    if status in CLOSED:
        if data.get('completedAt') is None:
            data['completedAt'] = data.get('updatedAt', ts)
            changes.append('completedAt')
        for st in data.get('stages', []):
            if st.get('status') == 'todo':
                stage_cleanup.append({'id': st.get('id'), 'old': 'todo', 'new': 'skipped'})
                st['status'] = 'skipped'

    if changes or stage_cleanup:
        data['updatedAt'] = ts
        data.setdefault('events', []).append({
            'ts': ts,
            'type': 'task.migrated',
            'message': 'Migrated legacy task file to 0.2 baseline',
            'details': {
                'changes': changes,
                'stageCleanup': stage_cleanup,
            },
        })
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        migrated += 1
        print(f'migrated: {task_id}')
    else:
        print(f'unchanged: {task_id}')

print(f'\nMigration complete. Updated {migrated} task(s).')
