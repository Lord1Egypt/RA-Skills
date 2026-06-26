# Task Templates

These files are the agent-side survival kit for long tasks.

## Files

- `task.template.json` — generic 0.2 task ledger template for any checkpointed task
- `task.schema.json` — structural schema for 0.2 task files
- `deploy-api.example.json` — concrete example for a multi-stage deploy task
- `deploy-service.example.json` — specialized deploy + rollback template
- `restart-openclaw-gateway.example.json` — specialized restart + healthcheck + notify template
- `sync-feishu-doc.example.json` — concrete example for a document sync task via sub-session
- `RECOVERY.md` — recovery playbook for interrupted long tasks

## When to use

Use a task file when any of these are true:

- estimated runtime > 5 minutes
- more than 3 stages
- uses background `exec`
- uses `sessions_spawn`
- uses `cron`
- has external side effects
- user explicitly wants the task to be recoverable

## Required flow

1. Create `tasks/<taskId>.json`
2. Create `logs/<taskId>.log`
3. Create `outputs/<taskId>/`
4. Write initial task state
5. Choose stages that match the task; do not force everything into `prepare/execute/verify`
6. Only then start execution
7. Update the task file after every completed stage
8. On recovery, verify reality first, then continue remaining stages only

## New 0.2 fields

### Lifecycle and ownership

- `priority` — `low|normal|high|urgent`
- `owner` — logical owner of the task
- `assignedAgent` — which agent is actively responsible
- `parentTaskId` — optional parent task for task trees
- `childTaskIds` — optional child tasks tracked under this task
- `startedAt` — true execution start time
- `completedAt` — closure time
- `lastVerifiedAt` — last time real backing state was checked

### Recovery and decision support

- `decisionNotes` — why the task is structured or handled a certain way
- `workingSummary` — short operational summary for resume and handoff
- `rollback` — rollback availability, strategy, and status
- `notifications` — whether start/completion/recovery notifications have been sent

### Blocking and dependencies

- `dependsOn` — logical task dependencies
- `blockedBy` — current blockers
- `blockedReason` — short human-readable reason for the block

## Status values

Top-level task status:

- `pending`
- `running`
- `waiting`
- `blocked`
- `succeeded`
- `failed`
- `cancelled`
- `partial`

Stage status:

- `todo`
- `running`
- `done`
- `failed`
- `skipped`

Rollback status:

- `not-applicable`
- `available`
- `in-progress`
- `completed`
- `failed`
- `not-needed`

## Recommended event types

- `task.created`
- `task.started`
- `task.updated`
- `task.blocked`
- `task.unblocked`
- `stage.started`
- `stage.completed`
- `stage.failed`
- `stage.skipped`
- `process.bound`
- `subtask.bound`
- `cron.bound`
- `recovery.checked`
- `recovery.corrected`
- `task.closed`

## Execution references

Record whichever applies:

- `process.sessionId` for background `exec`
- `subtask.sessionKey` for `sessions_spawn`
- `cron.jobId` for scheduled work

## Control-plane relationships

Use `parentTaskId` and `childTaskIds` when a larger task is split into sub-tasks that should still be tracked as one tree.

Use `dependsOn` when a task cannot proceed until another task logically completes.

Useful commands:

- `./scripts/list-open-tasks.py` — tabular open-task view with parent/dependency columns
- `python3 ./scripts/task-ls-tree.py` — tree view of parent/child task relationships
- `python3 ./scripts/show-task.py <taskId>` — detailed per-task view including relations

## Template selection guide

Use `task.template.json` when the task is general-purpose and you want a neutral starting point.

Use `restart-openclaw-gateway.example.json` when the task involves:

- service restart
- post-restart health checks
- reconciliation after restart
- explicit user-visible notification after recovery

Use `deploy-service.example.json` when the task involves:

- backup before deployment
- deploy verification
- explicit rollback path

Use `sync-feishu-doc.example.json` when the task is driven by a sub-session and remote verification matters.

## Recovery rule

Never trust the task file alone.

When resuming:

1. Read the task file
2. Read the resume summary
3. Check the real backing state (process, sub-session, cron, service, file, doc)
4. Correct the task file if needed
5. Continue only the unfinished work

## Practical note

Task files are not truth. They are a cached description of truth.
Reality wins.
