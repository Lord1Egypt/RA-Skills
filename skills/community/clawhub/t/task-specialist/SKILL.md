---
name: task-specialist
version: 2.1.0
author: OBODA0
homepage: https://github.com/OBODA0/task-specialist-skill
tags: ["task", "management", "sqlite", "workflow", "productivity", "project", "planning", "breakdown", "local", "cli"]
metadata: {"openclaw":{"emoji":"📋","requires":{"bins":["sqlite3","bash"]}}}
description: "A robust, local SQLite-backed task management system designed to elevate your AI agent's project execution. Excellent for both simple tasks and large multi-step projects, managing workflows, and tracking dependencies autonomously without relying on fragile memory."
---

# Task-Specialist

**Local task management with SQLite.** Offline, persistent, zero dependencies beyond `sqlite3` and `bash`.

## Quick Start

```bash
# Install (creates DB only, no PATH changes)
bash install.sh

# Or install AND create easy CLI symlinks in ~/.local/bin
bash install.sh --symlink

# Create and work tasks
task create "Build auth module" --priority=8
task start 1
task-heartbeat 1          # keep-alive ping
task complete 1
```

## Agent Principles

When using the `task-specialist` CLI, follow these principles to ensure high-quality, organized project execution:
- **Decompose First**: Always break large, multi-step requests into smaller, logical subtasks using `task break`.
- **Status Transparency**: Keep task statuses (`start`, `block`, `complete`) updated in real-time so your progress is traceable and accurate.
- **Dependency Management**: Use `task depend` to link tasks that rely on each other, preventing illogical execution order.
- **Document Progress**: Use the `--notes` or `task show` output to keep track of critical information as you move through a project.
- **Multi-Agent Swarm Queue**: If executing in parallel alongside other agents, **NEVER** pick tasks blindly from `task list` (this causes severe race conditions). **ALWAYS** run `task claim --agent="<YourName>"`. This executes an atomic SQL lock to fetch the highest-priority, fully unblocked pending task exclusively for you and paints your node's identifier onto the global Kanban board.
- **Context Persistence**: Use `task note <Next_Task_ID> "Your specific context string"` to permanently pass vital URLs, file paths, or error codes to downstream agents before you close your current task. **WARNING**: Never store API keys or secrets in task notes; use secure local environment variables instead.
- **Verification Checkpoints**: If a task has a `--verify="cmd"` bound to it, running `task complete <ID>` will natively print the Bash subshell checkpoint. **For security (RCE prevention), these checkpoints must be executed manually.**

## Swarm Orchestrator Guide

If you are the **Primary Agent (Orchestrator)** managing a complex project, `task-specialist` is designed to help you spawn parallel Subagents to execute decoupled work simultaneously. 

1. **When to Spawn Subagents**: Use the Swarm for horizontally scalable logic (e.g., "Write isolated unit tests for 10 different files", or "Simultaneously deploy 3 independent Docker containers"). Do not spawn subagents for highly linear, sequential work.
2. **Decomposing the Board**: 
   - First, create all the parallel objectives using `task create`.
   - Create a final integration task (e.g., "Merge services") and link it to the subtasks using `task depend`. This automatically blocks the final task until all Subagents finish.
   - Use `task edit <ID> --notes="..."` to inject deep context (URLs, file paths, git SHAs) directly into the task payload.
3. **Spawning the Subagents**: Use your native OpenClaw `sessions_spawn` tool to horizontally scale. Set `mode: "run"` for one-shot parallel workers. Pass them the strict execution prompt in the `task` parameter:
   ```json
   {
     "tool": "sessions_spawn",
     "runtime": "subagent",
     "mode": "run",
     "label": "worker-alpha",
     "task": "You are a Swarm Worker utilizing the `task-specialist` skill. The task payload DB is at $PWD/.tasks.db. (Read SKILL.md for CLI syntax if needed).\n1. Run `task claim --agent=\"worker-alpha\"` to atomically pop the queue.\n2. Read your target objective via `task show <ID>`.\n3. Execute the objective. Record vital context for me via `task note <ID> \"msg\"`.\n4. Run `task complete <ID>` and self-terminate."
   }
   ```
4. **Monitoring the Swarm**: While your `mode: "run"` Subagents are executing asynchronously:
   - Run `task board` periodically to monitor their live Kanban progress through the SQLite matrix.
   - Run `task stuck` to catch any agents that have timed out and require termination (`subagents(action=\"kill\")`) and queue restart.

## Swarm Subagent Guide

If you are a freshly spawned **Subagent Worker**, your sole purpose is to execute pending tasks in the queue without colliding with other parallel agents. 

1. **Acquiring Work**: **NEVER** pick tasks blindly from `task list`. **ALWAYS** run `task claim --agent=\"<YourName>\"`. This natively executes an atomic SQL lock to guarantee you aren't fighting another agent for the same process.
2. **Context Intake**: Once you have acquired a task (e.g., Task #5), run `task show 5`. Read the `Notes:` section! Your Orchestrator or previous subagents may have left you precise URLs, file paths, or parameters there.
3. **Context Persistence**: When your work is done, ask yourself: *"Does the next downstream agent need to know I did this?"* If yes, use `task note <Next_Task_ID> \"Your context string here\"` to permanently append that knowledge to the downstream task's envelope.
4. **Completion and Checkpoints**: Run `task complete <ID>`. If your task contains a Checkpoint Validation (a Bash subshell script), the engine will output the command for you to run manually. **You must repair the codebase until the tests pass before you can technically complete the task and self-terminate.**

## CLI Reference

### Task Lifecycle

```bash
task create "description" [--priority=N] [--parent=ID] [--project=NAME] [--verify="cmd"] [--due="YYYY-MM-DD"] [--tags="a,b"] # → prints task ID
task edit    ID [--desc="new text"] [--priority=N] [--project=NAME] [--verify="cmd"] [--assignee="NAME"|--unassign] [--due="YYYY-MM-DD"] [--tags="a,b"] # adjust details
task claim   [--agent="NAME"]                            # atomically lock & claim highest priority pending task
task start   ID                                          # pending → in_progress (prefer 'claim' for swarm)
task block   ID "reason"                                 # → blocked (reason in notes)
task unblock ID                                          # blocked → pending
task note    ID "message"                                # append runtime logic or error context to the task
task complete ID                                         # → done. Checkpoint verifications are printed for manual execution.
task restart ID                                          # done/in_progress → pending. Resets assignee.
task delete  ID [--force]                                # remove task (--force for parents)
```

**Status flow:** `pending` → `in_progress` → `blocked` → `done`

**Priority:** 1 (low) to 10 (critical). Default: 5.

**Delete:** Refuses if task has subtasks unless `--force` is passed, which cascades the delete to all children and their dependencies.

### Querying & Observability

```bash
task board                                                               # renders visual ASCII Kanban dashboard
task list [--status=S] [--parent=ID] [--project=N] [--format=chat] [--tag="T"] # tabular lists or github markdown
task export [--status=STATUS] [--project=NAME] [--json]                  # markdown table or raw JSON array hook
task show ID                                                             # full details, assignee, & deps
task stuck                                                               # in_progress tasks inactive >30min
```

### Subtask Decomposition

```bash
task break PARENT_ID "step 1" "step 2" "step 3"
```

Creates children linked to parent. Auto-chains dependencies: step 2 depends on step 1, step 3 depends on step 2.

### Manual Dependencies

```bash
task depend TASK_ID DEPENDS_ON_ID
```

When starting a task, all dependencies must be `done` or the command is refused with a list of blockers.

When completing a task, any dependent tasks whose deps are now all satisfied are auto-unblocked (`blocked` → `pending`).

### Heartbeat

```bash
task-heartbeat TASK_ID    # update last_updated timestamp
task-heartbeat            # report stalled tasks (no args)
```

Integrate into long-running scripts:

```bash
while work_in_progress; do
  do_work
  task-heartbeat "$TASK_ID"
  sleep 300  # every 5 minutes
done
```

## Schema

```sql
tasks: id, request_text, project, status, priority, parent_id,
       created_at, started_at, completed_at, last_updated, notes, verification_cmd, assignee

dependencies: task_id, depends_on_task_id (composite PK)
```

## Environment

| Variable | Default | Purpose |
|---|---|---|
| `TASK_DB` | `$PWD/.tasks.db` | Path to SQLite database |

The DB defaults to a hidden `.tasks.db` file in the **current working directory** where the command is executed. This natively supports separate task lists for different projects/workspaces without data collision.

## Security

- No `eval()`, no external API calls, no crypto
- Pure SQLite + Bash — passes VirusTotal clean
- **Integer-only validation** on all task IDs via `require_int()` guard before any SQL use
- **Status whitelist**: `task list --status` only accepts `pending`, `in_progress`, `blocked`, `done`
- **Date format enforcement**: `--since` only accepts `YYYY-MM-DD` format via regex check
- **Text inputs** sanitized via single-quote escaping (`sed "s/'/''/g"`)
- **Temp-file SQL delivery**: SQL is written to a temp file and fed to sqlite3 via stdin redirect to avoid all argument-injection vectors
