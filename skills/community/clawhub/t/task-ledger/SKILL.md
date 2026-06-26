---
name: task-ledger
description: Durable workflow layer for OpenClaw long-running work. Use when tasks are multi-stage, recoverable, parallelized across sub-agents/ACP, use background exec or cron, have external side effects, or need auditable outputs and resumable execution.
metadata:
  {
    "openclaw": {
      "emoji": "🧾",
      "requires": { "bins": ["python3", "bash"] }
    }
  }
---

# task-ledger

Use Task Ledger to turn long-running agent work into durable task objects instead of relying on fragile chat context.

Task Ledger is a workflow layer on top of OpenClaw execution primitives.
It does **not** replace ACP, sub-agents, exec, cron, or skills.
It gives them a durable task structure:

- checkpoint files in `tasks/`
- execution logs in `logs/`
- artifacts and reports in `outputs/`
- execution bindings for process/session/cron references
- parent/child task trees
- dependency and readiness checks
- recovery protocol
- short-first reporting

## Trigger

Use this skill when any of these are true:

- task runtime will likely exceed 5 minutes
- task has more than 3 stages
- task uses background `exec`
- task uses `sessions_spawn`
- task uses `cron`
- task has external side effects
- task involves restart / deploy / maintenance workflows with risky side effects
- task should be split into parent/child tasks or tracked with dependencies
- multiple agents or sub-agents will work in parallel
- task readiness should be checked before starting downstream work
- task reporting should prefer short updates backed by long file-based reports
- the user wants the work to be recoverable / resumable / auditable

Do **not** use this skill for every tiny action.
It is meant for work where losing state or execution structure would be costly.

## What this skill provides

This package includes:

- task checkpoint JSON files in `tasks/`
- execution logs in `logs/`
- outputs/artifacts in `outputs/`
- lifecycle helpers for create/update/advance/close
- recovery helpers for verify/resume-summary
- binding helpers for process/subtask/cron references
- rollback metadata in the task schema
- parent/child task relations and dependency-aware tooling
- readiness-aware scheduling helpers
- specialized templates for restart and deployment workflows
- human-friendly export for reports, handoff, archival, and graph views
- short-first reporting with optional file-backed long reports

Bundled files live next to this skill under `toolkit/`.

## First-use bootstrap

If the current workspace does not already contain the toolkit, copy these bundled assets into the workspace root:

- `toolkit/scripts/*` → `<workspace>/scripts/`
- `toolkit/task-templates/*` → `<workspace>/task-templates/`
- `toolkit/tasks/README.md` → `<workspace>/tasks/README.md`

Always create the runtime directories if missing:

- `tasks/`
- `logs/`
- `outputs/`

Do **not** overwrite user-modified files silently unless explicitly asked.
Prefer copying only missing files and then report what was installed.

## Operating protocol

1. Confirm the plan with the user before execution.
2. Create the task skeleton first.
3. Choose explicit stages that match reality.
4. Record execution references (`process.sessionId`, `subtask.sessionKey`, `cron.jobId`) when they exist.
5. Link parent/child tasks and dependencies when the work is larger than a single task object.
6. If work is parallelized, prefer **one parent task plus one child task per worker**.
7. Check readiness before starting dependent tasks; use start-if-ready when appropriate.
8. Update the task file after every completed stage.
9. On recovery, read the resume summary and verify real state first.
10. If reality and the checkpoint disagree, correct the checkpoint before continuing.
11. Continue only the unfinished work.
12. Prefer short user-facing summaries and keep long reports on file when appropriate.
13. Export or summarize task state in a human-friendly form when needed.
14. Proactively notify on completion.
15. If execution was interrupted and later resumed/reconnected, proactively notify that too.

## Parallel task pattern

For multi-agent or multi-sub-agent work:

- create one **parent task** for the overall goal
- create one **child task** per worker / subtask branch
- bind each child task to its own execution reference
- keep detailed stage tracking on child tasks
- let the parent task orchestrate readiness, finalization, and reporting

Avoid treating one task JSON file as a shared concurrent write target.
Task trees are safer than shared state.

## Core commands

Create a task skeleton:

```bash
./scripts/new-task.sh <slug> <title> [goal] [executionMode] [stagesCsv] [priority] [owner]
```

Useful helpers:

```bash
./scripts/list-open-tasks.py
python3 ./scripts/task-ls-tree.py
python3 ./scripts/task-ready.py <taskId> [--json]
python3 ./scripts/task-start-if-ready.py <taskId> [nextAction]
python3 ./scripts/task-graph-export.py [--format markdown|dot|json] [--open-only]
./scripts/show-task.py <taskId>
./scripts/task-events.py <taskId> [limit] [--type <eventType>] [--json]
./scripts/update-task.py <taskId> ...
./scripts/task-advance.py <taskId> [nextAction]
./scripts/task-bind-process.py <taskId> <processSessionId> [pid] [--state <state>]
./scripts/task-bind-subtask.py <taskId> <sessionKey> [--agent-id <agentId>]
./scripts/task-bind-cron.py <taskId> <jobId> [--schedule <expr>] [--next-run-at <iso>]
./scripts/task-verify.py <taskId> <summary> ...
./scripts/task-resume-summary.py <taskId> [--json|--markdown]
./scripts/task-export.py <taskId> [--format markdown|json|short] [--write-report]
./scripts/close-task.py <taskId> <final-status> [summary]
./scripts/task-doctor.py [taskId] [--strict] [--json]
```

## Specialized templates

Use bundled examples for common risky workflows:

- `restart-openclaw-gateway.example.json`
- `deploy-service.example.json`
- `sync-feishu-doc.example.json`

## Practical rule

Task files are not truth.
They are cached descriptions of truth.
Reality wins.
