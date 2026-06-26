# Tasks Runtime Directory

This directory holds live task checkpoint files.

## Purpose

Files in `tasks/` are the runtime state for long or recoverable tasks. Each task should have:

- `tasks/<taskId>.json` — structured checkpoint state
- `logs/<taskId>.log` — execution log
- `outputs/<taskId>/` — task outputs/artifacts

## Naming

Recommended task id format:

```text
<slug>-YYYYMMDD-HHMM
```

Examples:

- `deploy-api-20260307-1231`
- `sync-feishu-doc-20260307-1241`

## Standard lifecycle

```text
create -> start -> advance -> close
```

Typical command flow:

```bash
./scripts/new-task.sh <slug> <title> [goal] [executionMode] [stagesCsv] [priority] [owner]
python3 ./scripts/update-task.py <taskId> --mark-started
python3 ./scripts/task-advance.py <taskId>
python3 ./scripts/close-task.py <taskId> succeeded "summary"
```

## Recovery lifecycle

```text
read task -> resume-summary -> verify reality -> correct mismatch -> continue remaining work
```

Typical recovery flow:

```bash
python3 ./scripts/task-resume-summary.py <taskId>
python3 ./scripts/task-resume-summary.py <taskId> --markdown
python3 ./scripts/task-verify.py <taskId> "<what reality says>"
```

## Control-plane lifecycle

```text
parent/child tree + dependsOn graph + readiness checks + doctor validation
```

Useful commands:

```bash
./scripts/list-open-tasks.py
python3 ./scripts/task-ls-tree.py
python3 ./scripts/task-ready.py <taskId>
python3 ./scripts/show-task.py <taskId>
```

## Human-friendly export

You can export a task for reports, handoff, or note-taking:

```bash
python3 ./scripts/task-export.py <taskId>
python3 ./scripts/task-export.py <taskId> --format markdown
python3 ./scripts/task-export.py <taskId> --format json
```

## Creation flow

1. Create the task skeleton first
2. Write the initial task JSON
3. Make sure the task has an `events` array with an initial creation event
4. Only then start execution
5. Update task state after every completed stage and append lifecycle events

## Recovery flow

When resuming:

1. Find candidate tasks in this directory, or run `./scripts/list-open-tasks.py`
2. Prefer statuses: `running`, `waiting`, `blocked`, `partial`
3. Read `./scripts/task-resume-summary.py <taskId>`
4. Verify real state before trusting the checkpoint
5. Correct the task file if reality differs with `task-verify.py`
6. Continue only the unfinished work
7. Follow `scripts/resume-task.md` as the operational playbook

## Readiness flow

To see whether a task can start yet:

```bash
python3 ./scripts/task-ready.py <taskId>
python3 ./scripts/task-ready.py <taskId> --json
```

Readiness values:

- `ready`
- `waiting-deps`
- `unsatisfied`
- `missing-deps`

## New 0.2 fields worth watching

- `priority`
- `startedAt`
- `completedAt`
- `lastVerifiedAt`
- `parentTaskId`
- `childTaskIds`
- `dependsOn`
- `decisionNotes`
- `workingSummary`
- `rollback`
- `notifications`

## Status reminder

Top-level task statuses:

- `pending`
- `running`
- `waiting`
- `blocked`
- `succeeded`
- `failed`
- `cancelled`
- `partial`

Stage statuses:

- `todo`
- `running`
- `done`
- `failed`
- `skipped`

## Helper scripts

- `./scripts/new-task.sh <slug> <title> [goal] [executionMode] [stagesCsv] [priority] [owner]` — create a task skeleton, optionally with custom stages
- `./scripts/list-open-tasks.py` — list unfinished tasks with readiness, parent, and dependency columns
- `python3 ./scripts/task-ls-tree.py` — show parent/child task tree view
- `python3 ./scripts/task-ready.py <taskId> [--json]` — evaluate whether dependencies currently allow a task to start
- `./scripts/show-task.py <taskId>` — show one task in a human-readable view, including relations
- `./scripts/task-events.py <taskId> [limit] [--type <eventType>] [--json]` — inspect task event history
- `./scripts/task-advance.py <taskId> [nextAction]` — mark the current stage done and advance to the next stage
- `./scripts/task-bind-process.py <taskId> <processSessionId> [pid] [--state <state>]` — bind a background process reference to a task
- `./scripts/task-bind-subtask.py <taskId> <sessionKey> [--agent-id <agentId>]` — bind a sub-session to a task
- `./scripts/task-bind-cron.py <taskId> <jobId> [--schedule <expr>] [--next-run-at <iso>]` — bind a cron reference to a task
- `./scripts/task-verify.py <taskId> <summary> ...` — record real-world verification and optional corrections
- `./scripts/task-resume-summary.py <taskId> [--json|--markdown]` — print a recovery briefing for humans or machines
- `./scripts/task-export.py <taskId> [--format markdown|json]` — export a task for handoff, reports, or archival
- `./scripts/update-task.py <taskId> ...` — update common task fields safely, including relations/dependencies
- `./scripts/close-task.py <taskId> <final-status> [summary]` — close a task with a final state
- `./scripts/task-doctor.py [taskId] [--strict] [--json]` — validate task files, relation consistency, and scheduling readiness
- `scripts/resume-task.md` — recovery playbook

## Tracked vs runtime files

- `tasks/README.md` should stay in git
- `tasks/*.json` are runtime task instances and are typically ignored

## Practical rule

Task files are for continuity, not fantasy.
If the JSON and reality disagree, reality wins.
