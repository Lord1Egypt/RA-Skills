#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / 'tasks'


def die(msg, code=1):
    print(msg, file=sys.stderr)
    raise SystemExit(code)


if len(sys.argv) < 2:
    die(f"Usage: {Path(sys.argv[0]).name} <taskId> [limit] [--type <eventType>] [--json]")

task_id = sys.argv[1]
limit = None
event_type = None
as_json = False
args = sys.argv[2:]
i = 0
while i < len(args):
    arg = args[i]
    if arg == '--type':
        i += 1
        if i >= len(args): die('--type requires a value')
        event_type = args[i]
    elif arg == '--json':
        as_json = True
    else:
        if limit is not None:
            die('limit may only be provided once')
        try:
            limit = int(arg)
        except ValueError:
            die('limit must be an integer')
    i += 1

path = TASKS_DIR / f"{task_id}.json"
if not path.exists():
    die(f"Task not found: {task_id}", 2)

data = json.loads(path.read_text())
events = data.get('events', []) or []
if event_type is not None:
    events = [ev for ev in events if ev.get('type') == event_type]
if limit is not None:
    if limit < 0:
        die('limit must be >= 0')
    events = events[-limit:]

if as_json:
    print(json.dumps(events, ensure_ascii=False, indent=2))
    raise SystemExit(0)

print(f"taskId: {data.get('taskId', task_id)}")
print(f"events: {len(events)}")
if not events:
    raise SystemExit(0)

for idx, ev in enumerate(events, 1):
    print(f"\n{idx}. [{ev.get('ts', '-')}] {ev.get('type', '-')}")
    print(f"   message: {ev.get('message', '-')}")
    details = ev.get('details')
    if details is not None:
        print('   details:')
        rendered = json.dumps(details, ensure_ascii=False, indent=2).splitlines()
        for line in rendered:
            print(f"     {line}")
