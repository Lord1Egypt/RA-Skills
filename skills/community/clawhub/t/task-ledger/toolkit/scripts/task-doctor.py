#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / 'tasks'
VALID_STATUSES = {'pending', 'running', 'waiting', 'blocked', 'succeeded', 'failed', 'cancelled', 'partial'}
VALID_STAGE_STATUSES = {'todo', 'running', 'done', 'failed', 'skipped'}
VALID_PRIORITIES = {'low', 'normal', 'high', 'urgent'}
VALID_ROLLBACK = {'not-applicable', 'available', 'in-progress', 'completed', 'failed', 'not-needed'}
CLOSED_STATUSES = {'succeeded', 'failed', 'cancelled', 'partial'}
OPEN_STATUSES = {'pending', 'running', 'waiting', 'blocked'}
SATISFIED = {'succeeded'}
UNSATISFIABLE = {'failed', 'cancelled'}

args = sys.argv[1:]
as_json = False
strict = False
task_filter = None
i = 0
while i < len(args):
    arg = args[i]
    if arg == '--json':
        as_json = True
    elif arg == '--strict':
        strict = True
    else:
        if task_filter is not None:
            print('Usage: task-doctor.py [taskId] [--strict] [--json]', file=sys.stderr)
            raise SystemExit(1)
        task_filter = arg
    i += 1

errors = []
warnings = []
paths = [TASKS_DIR / f'{task_filter}.json'] if task_filter else sorted(TASKS_DIR.glob('*.json'))
all_tasks = {}
for p in sorted(TASKS_DIR.glob('*.json')):
    try:
        all_tasks[p.stem] = json.loads(p.read_text())
    except Exception:
        pass

if not paths:
    out = {'ok': True, 'errors': [], 'warnings': [], 'tasks': []}
    print(json.dumps(out, ensure_ascii=False, indent=2) if as_json else 'No task files found.')
    raise SystemExit(0)

for path in paths:
    task_name = path.stem
    if not path.exists():
        errors.append((task_name, 'task file not found'))
        continue
    try:
        data = json.loads(path.read_text())
    except Exception as e:
        errors.append((task_name, f'invalid json: {e}'))
        continue

    task_id = data.get('taskId', task_name)
    status = data.get('status')
    if status not in VALID_STATUSES:
        errors.append((task_id, f'invalid status: {status}'))

    priority = data.get('priority', 'normal')
    if data.get('priority') is None:
        warnings.append((task_id, 'legacy task missing priority; assuming normal'))
    elif priority not in VALID_PRIORITIES:
        errors.append((task_id, f'invalid priority: {priority}'))

    stages = data.get('stages', [])
    running_stages = [s.get('id', '?') for s in stages if s.get('status') == 'running']
    bad_stage_status = [f"{s.get('id', '?')}={s.get('status')}" for s in stages if s.get('status') not in VALID_STAGE_STATUSES]
    if bad_stage_status:
        errors.append((task_id, 'invalid stage statuses: ' + ', '.join(bad_stage_status)))
    if len(running_stages) > 1:
        errors.append((task_id, 'multiple running stages: ' + ', '.join(running_stages)))

    current_stage = data.get('stage')
    if current_stage and stages:
        known = {s.get('id') for s in stages}
        if current_stage not in known:
            errors.append((task_id, f'current stage not found in stages: {current_stage}'))

    artifacts = data.get('artifacts', {}) or {}
    log_path = artifacts.get('logPath')
    output_dir = artifacts.get('outputDir')
    if not log_path:
        errors.append((task_id, 'missing artifacts.logPath'))
    elif not (ROOT / log_path).exists():
        warnings.append((task_id, f'missing log file: {log_path}'))
    if not output_dir:
        errors.append((task_id, 'missing artifacts.outputDir'))
    elif not (ROOT / output_dir).exists():
        warnings.append((task_id, f'missing output dir: {output_dir}'))

    depends_on = data.get('dependsOn', [])
    waiting_deps = []
    missing_deps = []
    unsatisfied_deps = []
    if data.get('dependsOn') is None:
        warnings.append((task_id, 'legacy task missing dependsOn; assuming []'))
        depends_on = []
    elif not isinstance(depends_on, list):
        errors.append((task_id, 'dependsOn must be an array'))
    elif task_id in depends_on:
        errors.append((task_id, 'dependsOn cannot include the task itself'))
    else:
        for dep in depends_on:
            dep_task = all_tasks.get(dep)
            if dep_task is None:
                missing_deps.append(dep)
                warnings.append((task_id, f'dependency task missing: {dep}'))
            else:
                dep_status = dep_task.get('status')
                if dep_status in UNSATISFIABLE:
                    unsatisfied_deps.append((dep, dep_status))
                    warnings.append((task_id, f'dependency task is not satisfiable: {dep} [{dep_status}]'))
                elif dep_status not in SATISFIED:
                    waiting_deps.append((dep, dep_status))

    blocked_by = data.get('blockedBy', [])
    if data.get('blockedBy') is None:
        warnings.append((task_id, 'legacy task missing blockedBy; assuming []'))
        blocked_by = []
    elif not isinstance(blocked_by, list):
        errors.append((task_id, 'blockedBy must be an array'))
    else:
        for blocker in blocked_by:
            if blocker not in all_tasks and blocker not in {'user-confirmation', 'external-approval', 'manual-check'}:
                warnings.append((task_id, f'blockedBy references unknown blocker: {blocker}'))

    parent = data.get('parentTaskId')
    if parent:
        if parent == task_id:
            errors.append((task_id, 'parentTaskId cannot equal taskId'))
        elif parent not in all_tasks:
            warnings.append((task_id, f'parent task missing: {parent}'))
        else:
            parent_children = all_tasks[parent].get('childTaskIds') or []
            if task_id not in parent_children:
                warnings.append((task_id, f'parent task does not list child: {parent}'))

    child_ids = data.get('childTaskIds', []) or []
    if not isinstance(child_ids, list):
        errors.append((task_id, 'childTaskIds must be an array'))
    else:
        if task_id in child_ids:
            errors.append((task_id, 'childTaskIds cannot include task itself'))
        for child in child_ids:
            if child not in all_tasks:
                warnings.append((task_id, f'child task missing: {child}'))
            else:
                child_parent = all_tasks[child].get('parentTaskId')
                if child_parent != task_id:
                    warnings.append((task_id, f'child task does not point back to parent: {child}'))

    rollback = data.get('rollback')
    if rollback is None:
        warnings.append((task_id, 'legacy task missing rollback; assuming not-applicable'))
    else:
        rollback_status = (rollback or {}).get('status')
        if rollback_status not in VALID_ROLLBACK:
            errors.append((task_id, f'invalid rollback.status: {rollback_status}'))

    notifications = data.get('notifications')
    if notifications is None:
        warnings.append((task_id, 'legacy task missing notifications object'))
    elif not isinstance(notifications, dict):
        errors.append((task_id, 'notifications must be an object'))

    completed_at = data.get('completedAt')
    if completed_at and status in OPEN_STATUSES:
        errors.append((task_id, 'open task has completedAt set'))

    if status in CLOSED_STATUSES and running_stages:
        errors.append((task_id, 'closed task still has running stages: ' + ', '.join(running_stages)))

    if status == 'blocked' and not data.get('blockedReason') and not blocked_by:
        warnings.append((task_id, 'blocked task is missing blockedReason/blockedBy'))

    if status in {'succeeded', 'failed', 'cancelled'}:
        unfinished = [s.get('id', '?') for s in stages if s.get('status') in {'todo', 'running'}]
        if unfinished:
            warnings.append((task_id, 'closed task still has unfinished stages: ' + ', '.join(unfinished)))

    mode = data.get('executionMode')
    if status in {'running', 'waiting', 'blocked', 'partial'}:
        if mode == 'background-process' and not ((data.get('process') or {}).get('sessionId')):
            warnings.append((task_id, 'open background-process task missing process.sessionId'))
        elif mode in {'subsession', 'subtask-session'} and not ((data.get('subtask') or {}).get('sessionKey')):
            warnings.append((task_id, 'open subsession task missing subtask.sessionKey'))
        elif mode in {'cron', 'scheduled'} and not ((data.get('cron') or {}).get('jobId')):
            warnings.append((task_id, 'open cron task missing cron.jobId'))

    if status in {'pending', 'waiting', 'blocked'} and depends_on:
        if missing_deps:
            warnings.append((task_id, 'readiness: missing dependencies prevent start'))
        elif unsatisfied_deps:
            warnings.append((task_id, 'readiness: unsatisfied dependencies prevent start'))
        elif waiting_deps:
            warnings.append((task_id, 'readiness: waiting on dependency completion before start'))

result = {
    'ok': not errors and not warnings,
    'errors': [{'taskId': t, 'issue': i} for t, i in errors],
    'warnings': [{'taskId': t, 'issue': i} for t, i in warnings],
    'tasks': [p.stem for p in paths],
}

if as_json:
    print(json.dumps(result, ensure_ascii=False, indent=2))
else:
    if not errors and not warnings:
        print('Task doctor: no issues found.')
    else:
        print('Task doctor findings:')
        for task_id, issue in errors:
            print(f'- ERROR {task_id}: {issue}')
        for task_id, issue in warnings:
            print(f'- WARN  {task_id}: {issue}')

if errors:
    raise SystemExit(1)
if warnings and strict:
    raise SystemExit(1)
raise SystemExit(0)
