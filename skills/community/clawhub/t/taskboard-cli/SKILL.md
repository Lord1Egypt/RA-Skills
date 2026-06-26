---
name: taskboard-cli
version: 3.0.1
description: "Lightweight task management CLI for multi-agent workflows. SQLite backend, no external dependencies or credentials. Status-change hooks emit agent instructions (message, session) but do not auto-execute. Use when managing tasks across agents, tracking work status, assigning tasks, generating board summaries, or orchestrating cross-agent handoffs. Triggers on \"create task\", \"task board\", \"taskboard\", \"list tasks\", \"assign task\", \"board summary\", \"project tasks\"."
---

# Taskboard CLI

SQLite-backed task management for multi-agent projects. No network calls, no credentials, no environment variables.

## Quick Start

```bash
# Create tasks
python3 scripts/taskboard.py create "Build auth" --assign code-engineer --priority high
python3 scripts/taskboard.py create "Design UI" --assign designer --criteria "Responsive, mobile-first"

# Manage tasks
python3 scripts/taskboard.py update 1 --status in_progress --author code-engineer
python3 scripts/taskboard.py comment 1 "PR #42 ready" --author code-engineer
python3 scripts/taskboard.py update 1 --status done --author code-engineer --note "Merged to main"

# View board
python3 scripts/taskboard.py list --status in_progress
python3 scripts/taskboard.py show 1
python3 scripts/taskboard.py show 1 --json
python3 scripts/taskboard.py summary

# Subtasks
python3 scripts/taskboard.py create "Write tests" --parent 1 --assign code-engineer

# Thread linking
python3 scripts/taskboard.py set-thread 1 1484268803994026085
python3 scripts/taskboard.py get-thread 1

# Change history
python3 scripts/taskboard.py history 1
```

## Custom Database Path

By default the database lives at `scripts/taskboard.db`. Override with `--db`:

```bash
python3 scripts/taskboard.py --db /path/to/my.db list
```

## Task Statuses

`todo` → `in_progress` → `done`

Also: `blocked`, `rejected`

No "review" status — use hooks to create follow-up tasks or notify agents.

## Hooks (Cross-Agent Orchestration)

Hooks fire when task status changes. They print instructions to stdout for the calling agent to execute — no auto-execution, no network calls.

```bash
# When task is started (ack'd), print a notification instruction
python3 scripts/taskboard.py create "Build auth" \
  --on-ack "message:CHANNEL_ID:🔨 {task.title} started by {task.assigned_to}"

# When done, instruct the agent to create a review task
python3 scripts/taskboard.py create "Design UI" \
  --on-done "session:tech-lead:Review {task.title} and create QA task"

# Add/update hooks on existing task
python3 scripts/taskboard.py update 1 --on-done "message:CHANNEL_ID:Done!"
```

Hook output format:
```
🔔 ON_ACK: message:CHANNEL_ID:🔨 Build auth started
🔔 ON_DONE: session:tech-lead:Review Build auth and create QA task
```

The agent reads these lines and decides how to act (send a message, spawn a session, create a task, etc.).

## Data Model

- **tasks** — id, title, description, acceptance_criteria, status, priority, assigned_to, created_by, parent_id, thread_id, on_ack, on_done, timestamps
- **task_comments** — per-task comment history
- **task_updates** — audit log of all field changes

Schema auto-initializes on first run. Upgrades from v1 (missing on_ack/on_done columns) are handled automatically.

## Reference

- `references/webhook-integration.md` — How to add Discord/webhook notifications on top of taskboard
- `references/github-backend.md` — Syncing tasks with GitHub Issues
- `references/taskboard-setup.md` — Task lifecycle, cross-agent handoff protocol, cron integration
