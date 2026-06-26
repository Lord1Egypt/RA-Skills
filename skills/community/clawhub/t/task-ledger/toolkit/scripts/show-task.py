#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / 'tasks'

if len(sys.argv) != 2:
    print(f"Usage: {Path(sys.argv[0]).name} <taskId>", file=sys.stderr)
    raise SystemExit(1)

task_id = sys.argv[1]
path = TASKS_DIR / f"{task_id}.json"
if not path.exists():
    print(f"Task not found: {task_id}", file=sys.stderr)
    raise SystemExit(2)

data = json.loads(path.read_text())

print(f"taskId:        {data.get('taskId', '-')}")
print(f"title:         {data.get('title', '-')}")
print(f"goal:          {data.get('goal', '-')}")
print(f"status:        {data.get('status', '-')}")
print(f"priority:      {data.get('priority', '-')}")
print(f"stage:         {data.get('stage', '-')}")
print(f"mode:          {data.get('executionMode', '-')}")
print(f"createdAt:     {data.get('createdAt', '-')}")
print(f"updatedAt:     {data.get('updatedAt', '-')}")
print(f"startedAt:     {data.get('startedAt', '-')}")
print(f"completedAt:   {data.get('completedAt', '-')}")
print(f"parentTaskId:  {data.get('parentTaskId', '-')}")
print(f"childTaskIds:  {', '.join(data.get('childTaskIds', []) or []) or '-'}")
print(f"dependsOn:     {', '.join(data.get('dependsOn', []) or []) or '-'}")
print(f"blockedBy:     {', '.join(data.get('blockedBy', []) or []) or '-'}")
print(f"blockedReason: {data.get('blockedReason', '-')}")
print(f"nextAction:    {data.get('nextAction', '-')}")
print(f"resumeHint:    {data.get('resumeHint', '-')}")

artifacts = data.get('artifacts', {}) or {}
print(f"logPath:       {artifacts.get('logPath', '-')}")
print(f"outputDir:     {artifacts.get('outputDir', '-')}")

process = data.get('process', {}) or {}
subtask = data.get('subtask', {}) or {}
cron = data.get('cron', {}) or {}
print(f"processId:     {process.get('sessionId', '-')}")
print(f"subSession:    {subtask.get('sessionKey', '-')}")
print(f"cronJobId:     {cron.get('jobId', '-')}")

print('stages:')
for stage in data.get('stages', []):
    sid = stage.get('id', '-')
    sst = stage.get('status', '-')
    print(f"  - {sid}: {sst}")

events = data.get('events', []) or []
print(f"events:        {len(events)}")
for event in events[-5:]:
    print(f"  - [{event.get('ts', '-')}] {event.get('type', '-')}: {event.get('message', '-')}")

if data.get('error') is not None:
    print('error:')
    print(json.dumps(data['error'], ensure_ascii=False, indent=2))
if data.get('result') is not None:
    print('result:')
    print(json.dumps(data['result'], ensure_ascii=False, indent=2))
