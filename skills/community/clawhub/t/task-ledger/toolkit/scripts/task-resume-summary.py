#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / 'tasks'


def die(msg, code=1):
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def load_summary(task_id):
    path = TASKS_DIR / f"{task_id}.json"
    if not path.exists():
        die(f"Task not found: {task_id}", 2)
    data = json.loads(path.read_text())
    return {
        'taskId': data.get('taskId', task_id),
        'title': data.get('title'),
        'status': data.get('status'),
        'priority': data.get('priority', 'normal'),
        'currentStage': data.get('stage'),
        'startedAt': data.get('startedAt'),
        'lastVerifiedAt': data.get('lastVerifiedAt'),
        'blockedReason': data.get('blockedReason'),
        'nextAction': data.get('nextAction'),
        'workingSummary': data.get('workingSummary'),
        'parentTaskId': data.get('parentTaskId'),
        'childTaskIds': data.get('childTaskIds', []),
        'dependsOn': data.get('dependsOn', []),
        'rollback': data.get('rollback'),
        'process': (data.get('process') or {}).get('sessionId'),
        'subtask': (data.get('subtask') or {}).get('sessionKey'),
        'cron': (data.get('cron') or {}).get('jobId'),
        'stages': data.get('stages', []),
    }


if len(sys.argv) < 2:
    die(f"Usage: {Path(sys.argv[0]).name} <taskId> [--json|--markdown]")

task_id = sys.argv[1]
mode = 'text'
if len(sys.argv) == 3:
    if sys.argv[2] == '--json':
        mode = 'json'
    elif sys.argv[2] == '--markdown':
        mode = 'markdown'
    else:
        die('only --json or --markdown is supported as optional argument')
elif len(sys.argv) != 2:
    die(f"Usage: {Path(sys.argv[0]).name} <taskId> [--json|--markdown]")

summary = load_summary(task_id)

if mode == 'json':
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    raise SystemExit(0)

if mode == 'markdown':
    print(f"# Resume Summary — {summary['taskId']}")
    print()
    print(f"- **Title:** {summary['title']}")
    print(f"- **Status:** `{summary['status']}`")
    print(f"- **Priority:** `{summary['priority']}`")
    print(f"- **Current Stage:** `{summary['currentStage']}`")
    print(f"- **Started:** {summary['startedAt']}")
    print(f"- **Last Verified:** {summary['lastVerifiedAt']}")
    print(f"- **Parent:** {summary['parentTaskId'] or '-'}")
    print(f"- **Children:** {', '.join(summary['childTaskIds']) if summary['childTaskIds'] else '-'}")
    print(f"- **Depends On:** {', '.join(summary['dependsOn']) if summary['dependsOn'] else '-'}")
    print()
    print('## Stages')
    print()
    for st in summary['stages']:
        print(f"- `{st.get('id')}` — **{st.get('status')}**")
    print()
    print('## Execution References')
    print()
    print(f"- **process.sessionId:** {summary['process']}")
    print(f"- **subtask.sessionKey:** {summary['subtask']}")
    print(f"- **cron.jobId:** {summary['cron']}")
    print()
    print('## Rollback')
    print()
    rb = summary['rollback'] or {}
    print(f"- **Available:** {rb.get('available')}")
    print(f"- **Strategy:** {rb.get('strategy')}")
    print(f"- **Status:** {rb.get('status')}")
    print()
    print('## Next Action')
    print()
    print(summary['nextAction'] or '-')
    print()
    print('## Working Summary')
    print()
    print(summary['workingSummary'] or '-')
    raise SystemExit(0)

print(f"Task: {summary['taskId']}")
print(f"Title: {summary['title']}")
print(f"Status: {summary['status']}")
print(f"Priority: {summary['priority']}")
print(f"Current stage: {summary['currentStage']}")
print(f"Started: {summary['startedAt']}")
print(f"Last verified: {summary['lastVerifiedAt']}")
print(f"Parent: {summary['parentTaskId'] or 'none'}")
print(f"Children: {', '.join(summary['childTaskIds']) if summary['childTaskIds'] else 'none'}")
print(f"Depends on: {', '.join(summary['dependsOn']) if summary['dependsOn'] else 'none'}")
print('\nStages:')
for st in summary['stages']:
    print(f"- {st.get('id'):<16} {st.get('status')}")
print('\nBlocked:')
print(f"- {summary['blockedReason'] or 'none'}")
print('\nExecution refs:')
print(f"- process.sessionId: {summary['process']}")
print(f"- subtask.sessionKey: {summary['subtask']}")
print(f"- cron.jobId: {summary['cron']}")
print('\nRollback:')
rb = summary['rollback'] or {}
print(f"- available: {rb.get('available')}")
print(f"- strategy: {rb.get('strategy')}")
print(f"- status: {rb.get('status')}")
print('\nNext action:')
print(f"- {summary['nextAction']}")
print('\nWorking summary:')
print(f"- {summary['workingSummary'] or ''}")
