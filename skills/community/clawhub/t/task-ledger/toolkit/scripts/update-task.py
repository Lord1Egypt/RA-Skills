#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / 'tasks'
VALID_STATUSES = {'pending', 'running', 'waiting', 'blocked', 'succeeded', 'failed', 'cancelled', 'partial'}
VALID_STAGE_STATUSES = {'todo', 'running', 'done', 'failed', 'skipped'}
VALID_PRIORITIES = {'low', 'normal', 'high', 'urgent'}
VALID_ROLLBACK_STATUSES = {'not-applicable', 'available', 'in-progress', 'completed', 'failed', 'not-needed'}
CLOSED_STATUSES = {'succeeded', 'failed', 'cancelled', 'partial'}
OPEN_STATUSES = {'pending', 'running', 'waiting', 'blocked'}


def iso_now_local():
    return datetime.now().astimezone().isoformat(timespec='milliseconds')


def die(msg, code=1):
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def ensure_event(data, ts, event_type, message, details):
    data.setdefault('events', []).append({
        'ts': ts,
        'type': event_type,
        'message': message,
        'details': details,
    })


def find_stage(data, stage_id):
    for st in data.get('stages', []):
        if st.get('id') == stage_id:
            return st
    return None


def parse_csv_or_null(raw):
    if raw in {'', 'null'}:
        return []
    return [x.strip() for x in raw.split(',') if x.strip()]


def task_exists(task_id):
    return (TASKS_DIR / f'{task_id}.json').exists()


def validate(data):
    status = data.get('status')
    if status not in VALID_STATUSES:
        die(f'invalid status: {status}')

    priority = data.get('priority', 'normal')
    if priority not in VALID_PRIORITIES:
        die(f'invalid priority: {priority}')

    rollback_status = ((data.get('rollback') or {}).get('status'))
    if rollback_status not in VALID_ROLLBACK_STATUSES:
        die(f'invalid rollback status: {rollback_status}')

    stages = data.get('stages', [])
    known = {s.get('id') for s in stages}
    current_stage = data.get('stage')
    if current_stage and current_stage not in known:
        die(f'current stage not found in stages: {current_stage}')

    running = [s.get('id') for s in stages if s.get('status') == 'running']
    invalid_stage_statuses = [f"{s.get('id')}={s.get('status')}" for s in stages if s.get('status') not in VALID_STAGE_STATUSES]
    if invalid_stage_statuses:
        die('invalid stage statuses: ' + ', '.join(invalid_stage_statuses))
    if len(running) > 1:
        die('multiple running stages: ' + ', '.join(running))
    if status in CLOSED_STATUSES and running:
        die('closed task cannot have running stages')
    if data.get('completedAt') is not None and status in OPEN_STATUSES:
        die('open task cannot have completedAt set')

    parent = data.get('parentTaskId')
    task_id = data.get('taskId')
    if parent == task_id:
        die('parentTaskId cannot equal taskId')
    if parent and not task_exists(parent):
        die(f'parent task not found: {parent}')

    child_ids = data.get('childTaskIds', [])
    if not isinstance(child_ids, list):
        die('childTaskIds must be an array')
    if task_id in child_ids:
        die('childTaskIds cannot include task itself')
    for child in child_ids:
        if not task_exists(child):
            die(f'child task not found: {child}')

    depends_on = data.get('dependsOn', [])
    if not isinstance(depends_on, list):
        die('dependsOn must be an array')
    if task_id in depends_on:
        die('dependsOn cannot include task itself')
    for dep in depends_on:
        if not task_exists(dep):
            die(f'dependency task not found: {dep}')


if len(sys.argv) < 2:
    die(
        f"Usage: {Path(sys.argv[0]).name} <taskId> [--status S] [--stage CURRENT] [--next-action TEXT] "
        "[--set-stage-status ID=STATUS] [--priority P] [--owner OWNER] [--assigned-agent AGENT] "
        "[--parent-task TASK|null] [--child-task-ids csv|null] [--depends-on csv|null] [--blocked-by csv|null] "
        "[--started-at ISO] [--completed-at ISO|null] [--last-verified-at ISO|null] [--decision-notes TEXT] "
        "[--working-summary TEXT] [--blocked-reason TEXT|null] [--rollback-available true|false] "
        "[--rollback-strategy TEXT|null] [--rollback-status STATUS] [--process-session ID] [--subsession KEY] "
        "[--cron-job ID] [--result-json JSON] [--error-json JSON] [--mark-started] [--mark-blocked] [--mark-unblocked]"
    )

task_id = sys.argv[1]
path = TASKS_DIR / f"{task_id}.json"
if not path.exists():
    die(f"Task not found: {task_id}", 2)

data = json.loads(path.read_text())
args = sys.argv[2:]
changes = []
stage_changes = []
events = []


def record_change(field, old, new):
    changes.append({'field': field, 'old': old, 'new': new})


i = 0
while i < len(args):
    arg = args[i]
    if arg == '--status':
        i += 1
        if i >= len(args): die('--status requires a value')
        value = args[i]
        if value not in VALID_STATUSES:
            die(f'invalid status: {value}')
        old = data.get('status')
        data['status'] = value
        record_change('status', old, value)
    elif arg == '--stage':
        i += 1
        if i >= len(args): die('--stage requires a value')
        value = args[i]
        if find_stage(data, value) is None:
            die(f'stage not found: {value}')
        old = data.get('stage')
        data['stage'] = value
        record_change('stage', old, value)
    elif arg == '--next-action':
        i += 1
        if i >= len(args): die('--next-action requires a value')
        old = data.get('nextAction')
        data['nextAction'] = args[i]
        record_change('nextAction', old, args[i])
    elif arg == '--set-stage-status':
        i += 1
        if i >= len(args): die('--set-stage-status requires ID=STATUS')
        raw = args[i]
        if '=' not in raw:
            die('--set-stage-status must be ID=STATUS')
        sid, sstatus = raw.split('=', 1)
        if sstatus not in VALID_STAGE_STATUSES:
            die(f'invalid stage status: {sstatus}')
        st = find_stage(data, sid)
        if st is None:
            die(f'stage not found: {sid}')
        old = st.get('status')
        st['status'] = sstatus
        stage_changes.append({'id': sid, 'old': old, 'new': sstatus})
    elif arg == '--priority':
        i += 1
        if i >= len(args): die('--priority requires a value')
        value = args[i]
        if value not in VALID_PRIORITIES:
            die(f'invalid priority: {value}')
        old = data.get('priority')
        data['priority'] = value
        record_change('priority', old, value)
    elif arg == '--owner':
        i += 1
        if i >= len(args): die('--owner requires a value')
        old = data.get('owner')
        data['owner'] = args[i]
        record_change('owner', old, args[i])
    elif arg == '--assigned-agent':
        i += 1
        if i >= len(args): die('--assigned-agent requires a value')
        value = None if args[i] in {'null', ''} else args[i]
        old = data.get('assignedAgent')
        data['assignedAgent'] = value
        record_change('assignedAgent', old, value)
    elif arg == '--parent-task':
        i += 1
        if i >= len(args): die('--parent-task requires a value')
        value = None if args[i] == 'null' else args[i]
        old = data.get('parentTaskId')
        data['parentTaskId'] = value
        record_change('parentTaskId', old, value)
    elif arg == '--child-task-ids':
        i += 1
        if i >= len(args): die('--child-task-ids requires a value')
        value = parse_csv_or_null(args[i])
        old = data.get('childTaskIds', [])
        data['childTaskIds'] = value
        record_change('childTaskIds', old, value)
    elif arg == '--depends-on':
        i += 1
        if i >= len(args): die('--depends-on requires a value')
        value = parse_csv_or_null(args[i])
        old = data.get('dependsOn', [])
        data['dependsOn'] = value
        record_change('dependsOn', old, value)
    elif arg == '--blocked-by':
        i += 1
        if i >= len(args): die('--blocked-by requires a value')
        value = parse_csv_or_null(args[i])
        old = data.get('blockedBy', [])
        data['blockedBy'] = value
        record_change('blockedBy', old, value)
    elif arg == '--started-at':
        i += 1
        if i >= len(args): die('--started-at requires a value')
        value = None if args[i] == 'null' else args[i]
        old = data.get('startedAt')
        data['startedAt'] = value
        record_change('startedAt', old, value)
    elif arg == '--completed-at':
        i += 1
        if i >= len(args): die('--completed-at requires a value')
        value = None if args[i] == 'null' else args[i]
        old = data.get('completedAt')
        data['completedAt'] = value
        record_change('completedAt', old, value)
    elif arg == '--last-verified-at':
        i += 1
        if i >= len(args): die('--last-verified-at requires a value')
        value = None if args[i] == 'null' else args[i]
        old = data.get('lastVerifiedAt')
        data['lastVerifiedAt'] = value
        record_change('lastVerifiedAt', old, value)
    elif arg == '--decision-notes':
        i += 1
        if i >= len(args): die('--decision-notes requires a value')
        old = data.get('decisionNotes')
        data['decisionNotes'] = args[i]
        record_change('decisionNotes', old, args[i])
    elif arg == '--working-summary':
        i += 1
        if i >= len(args): die('--working-summary requires a value')
        old = data.get('workingSummary')
        data['workingSummary'] = args[i]
        record_change('workingSummary', old, args[i])
    elif arg == '--blocked-reason':
        i += 1
        if i >= len(args): die('--blocked-reason requires a value')
        value = None if args[i] == 'null' else args[i]
        old = data.get('blockedReason')
        data['blockedReason'] = value
        record_change('blockedReason', old, value)
    elif arg == '--rollback-available':
        i += 1
        if i >= len(args): die('--rollback-available requires true|false')
        raw = args[i].lower()
        if raw not in {'true', 'false'}:
            die('--rollback-available requires true|false')
        value = raw == 'true'
        old = ((data.get('rollback') or {}).get('available'))
        data.setdefault('rollback', {})['available'] = value
        record_change('rollback.available', old, value)
    elif arg == '--rollback-strategy':
        i += 1
        if i >= len(args): die('--rollback-strategy requires a value')
        value = None if args[i] == 'null' else args[i]
        old = ((data.get('rollback') or {}).get('strategy'))
        data.setdefault('rollback', {})['strategy'] = value
        record_change('rollback.strategy', old, value)
    elif arg == '--rollback-status':
        i += 1
        if i >= len(args): die('--rollback-status requires a value')
        value = args[i]
        if value not in VALID_ROLLBACK_STATUSES:
            die(f'invalid rollback status: {value}')
        old = ((data.get('rollback') or {}).get('status'))
        data.setdefault('rollback', {})['status'] = value
        record_change('rollback.status', old, value)
    elif arg == '--process-session':
        i += 1
        if i >= len(args): die('--process-session requires a value')
        old = (data.get('process') or {}).get('sessionId')
        data.setdefault('process', {})['sessionId'] = args[i]
        record_change('process.sessionId', old, args[i])
    elif arg == '--subsession':
        i += 1
        if i >= len(args): die('--subsession requires a value')
        old = (data.get('subtask') or {}).get('sessionKey')
        data.setdefault('subtask', {})['sessionKey'] = args[i]
        record_change('subtask.sessionKey', old, args[i])
    elif arg == '--cron-job':
        i += 1
        if i >= len(args): die('--cron-job requires a value')
        old = (data.get('cron') or {}).get('jobId')
        data.setdefault('cron', {})['jobId'] = args[i]
        record_change('cron.jobId', old, args[i])
    elif arg == '--result-json':
        i += 1
        if i >= len(args): die('--result-json requires a value')
        parsed = json.loads(args[i])
        old = data.get('result')
        data['result'] = parsed
        record_change('result', old, parsed)
    elif arg == '--error-json':
        i += 1
        if i >= len(args): die('--error-json requires a value')
        parsed = json.loads(args[i])
        old = data.get('error')
        data['error'] = parsed
        record_change('error', old, parsed)
    elif arg == '--mark-started':
        ts = iso_now_local()
        if data.get('startedAt') is None:
            old = data.get('startedAt')
            data['startedAt'] = ts
            record_change('startedAt', old, ts)
        if data.get('status') == 'pending':
            old = data.get('status')
            data['status'] = 'running'
            record_change('status', old, 'running')
        events.append(('task.started', 'Task execution started', {}))
    elif arg == '--mark-blocked':
        old = data.get('status')
        data['status'] = 'blocked'
        record_change('status', old, 'blocked')
        events.append(('task.blocked', 'Task marked blocked', None))
    elif arg == '--mark-unblocked':
        old = data.get('status')
        data['status'] = 'running'
        record_change('status', old, 'running')
        old_reason = data.get('blockedReason')
        data['blockedReason'] = None
        record_change('blockedReason', old_reason, None)
        events.append(('task.unblocked', 'Task unblocked', {}))
    else:
        die(f'unknown argument: {arg}')
    i += 1

if any(e[0] == 'task.blocked' for e in events) and not data.get('blockedReason') and not data.get('blockedBy'):
    die('--mark-blocked requires --blocked-reason or --blocked-by to be set before validation')

# Backfill new fields for older tasks.
data.setdefault('priority', 'normal')
data.setdefault('owner', data.get('ownerSession', 'main'))
data.setdefault('assignedAgent', None)
data.setdefault('parentTaskId', None)
data.setdefault('childTaskIds', [])
data.setdefault('startedAt', None)
data.setdefault('completedAt', None)
data.setdefault('lastVerifiedAt', None)
data.setdefault('dependsOn', [])
data.setdefault('blockedBy', [])
data.setdefault('blockedReason', None)
data.setdefault('decisionNotes', '')
data.setdefault('workingSummary', '')
data.setdefault('rollback', {'available': False, 'strategy': None, 'status': 'not-applicable', 'artifacts': []})
data.setdefault('notifications', {
    'notifiedStart': data.get('notifiedStart', False),
    'notifiedCompletion': data.get('notifiedCompletion', False),
    'notifiedRecovery': False,
})
data.setdefault('artifacts', {}).setdefault('files', [])

validate(data)

ts = iso_now_local()
data['updatedAt'] = ts
for event_type, message, details in events:
    if event_type == 'task.blocked' and details is None:
        details = {'blockedReason': data.get('blockedReason'), 'blockedBy': data.get('blockedBy')}
    ensure_event(data, ts, event_type, message, details or {})
if changes or stage_changes:
    ensure_event(data, ts, 'task.updated', 'Task updated via update-task.py', {
        'changes': changes,
        'stageChanges': stage_changes,
    })
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print(f'Updated task: {task_id}')
