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


if len(sys.argv) < 3:
    die(f"Usage: {Path(sys.argv[0]).name} <taskId> <jobId> [--schedule <expr>] [--next-run-at <iso>]")

task_id = sys.argv[1]
job_id = sys.argv[2]
schedule = None
next_run_at = None
args = sys.argv[3:]
i = 0
while i < len(args):
    arg = args[i]
    if arg == '--schedule':
        i += 1
        if i >= len(args): die('--schedule requires a value')
        schedule = args[i]
    elif arg == '--next-run-at':
        i += 1
        if i >= len(args): die('--next-run-at requires a value')
        next_run_at = args[i]
    else:
        die(f'unknown argument: {arg}')
    i += 1

path = TASKS_DIR / f"{task_id}.json"
if not path.exists():
    die(f"Task not found: {task_id}", 2)

data = json.loads(path.read_text())
old_job = (data.get('cron') or {}).get('jobId')
old_schedule = (data.get('cron') or {}).get('schedule')
old_next = (data.get('cron') or {}).get('nextRunAt')
data.setdefault('cron', {})['jobId'] = job_id
if schedule is not None:
    data['cron']['schedule'] = schedule
if next_run_at is not None:
    data['cron']['nextRunAt'] = next_run_at

ts = iso_now_local()
data['updatedAt'] = ts
data.setdefault('events', []).append({
    'ts': ts,
    'type': 'cron.bound',
    'message': 'Cron binding updated for task',
    'details': {
        'oldJobId': old_job,
        'newJobId': job_id,
        'oldSchedule': old_schedule,
        'newSchedule': data['cron'].get('schedule'),
        'oldNextRunAt': old_next,
        'newNextRunAt': data['cron'].get('nextRunAt'),
    },
})

path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print(f'Bound cron to task: {task_id} -> {job_id}')
