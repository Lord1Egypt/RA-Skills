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


if len(sys.argv) not in {3, 5}:
    die(f"Usage: {Path(sys.argv[0]).name} <taskId> <sessionKey> [--agent-id <agentId>]")

task_id = sys.argv[1]
session_key = sys.argv[2]
agent_id = None
if len(sys.argv) == 5:
    if sys.argv[3] != '--agent-id':
        die('expected --agent-id <agentId>')
    agent_id = sys.argv[4]

path = TASKS_DIR / f"{task_id}.json"
if not path.exists():
    die(f"Task not found: {task_id}", 2)

data = json.loads(path.read_text())
old_key = (data.get('subtask') or {}).get('sessionKey')
old_agent = (data.get('subtask') or {}).get('agentId')
data.setdefault('subtask', {})['sessionKey'] = session_key
if agent_id is not None:
    data['subtask']['agentId'] = agent_id

ts = iso_now_local()
data['updatedAt'] = ts
data.setdefault('events', []).append({
    'ts': ts,
    'type': 'subtask.bound',
    'message': 'Subtask session bound to task',
    'details': {
        'oldSessionKey': old_key,
        'newSessionKey': session_key,
        'oldAgentId': old_agent,
        'newAgentId': data['subtask'].get('agentId'),
    },
})

path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print(f'Bound subtask to task: {task_id} -> {session_key}')
