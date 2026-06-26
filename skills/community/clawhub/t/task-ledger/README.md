# Task Ledger

Task Ledger is a durable workflow layer for OpenClaw.

It turns long-running, multi-stage, multi-agent work into recoverable task objects, execution bindings, dependency-aware task graphs, and auditable outputs.

If OpenClaw is the execution substrate, Task Ledger is the durable operations notebook that keeps long-running work intelligible.

## Why

OpenClaw 3.7 gives you stronger execution primitives and platform stability: better ACP continuity, more reliable routing, stronger compaction behavior, richer plugin lifecycles, and better session recovery.

Task Ledger does **not** replace those platform capabilities.
It adds a workflow layer on top of them.

Use Task Ledger when execution alone is not enough and you need the work itself to become:

- durable
- resumable
- auditable
- dependency-aware
- safe to hand off

In practice, that means turning fragile chat context into:

- a task object
- explicit stages
- execution references
- recovery rules
- output artifacts
- short chat updates backed by file-based reports

## Positioning in the OpenClaw stack

OpenClaw provides the execution substrate:

- `exec` / `process`
- `sessions_spawn`
- ACP sessions
- sub-agents
- `cron`
- messaging and channel delivery
- plugins and context engines

Task Ledger provides the durable task layer on top:

- task objects in `tasks/`
- execution logs in `logs/`
- reports and artifacts in `outputs/`
- bindings to process/session/cron references
- parent/child task trees
- dependency and readiness checks
- recovery and reporting protocol

A useful shorthand:

- **OpenClaw runs work**
- **Task Ledger governs long-running work**

## Relationship to ACP, sub-agents, skills, and cron

Task Ledger is not a competing execution runtime.
It is the durable task layer that sits above OpenClaw execution primitives.

### ACP

ACP provides persistent execution spaces and thread-bound agent work.
Task Ledger provides the task object that explains what that ACP work is for, how many stages it has, what session it is bound to, and how it should be resumed or finalized.

### Sub-agents

Sub-agents provide isolated workers.
Task Ledger provides the parent/child task structure that keeps those workers organized, especially when several branches run in parallel.

### Skills

Skills perform domain work such as coding, publishing, GitHub operations, or document sync.
Task Ledger does not replace those skills.
It governs long-running work that uses those skills.

### `exec` / `process`

`exec` and `process` provide runtime execution handles.
Task Ledger binds those handles to durable task state.

### `cron`

`cron` provides scheduling and recurrence.
Task Ledger provides task identity, task history, and recovery semantics around scheduled work.

## Architecture pattern

A practical mental model:

```text
OpenClaw primitives → do the work
Task Ledger       → describes, tracks, and recovers the work
```

For simple work, a single task object is enough.
For larger or parallel work, Task Ledger works best as a task tree:

- one parent task for orchestration
- one child task per worker or branch
- explicit execution bindings on each child task
- readiness checks before finalization

## Release intent for 0.3.0

Version 0.3.0 is intentionally a **positioning and workflow-model release**.
It sharpens what Task Ledger is for.
It does not try to turn the project into a full workflow engine in one jump.

That means 0.3.0 focuses on:

- naming the product correctly
- documenting the parent/child task model
- documenting the right usage boundary
- documenting the relationship to OpenClaw platform primitives

Deeper aggregation and orchestration helpers belong in `0.3.1+`.

## What changed in 0.3.0

Positioning update for the OpenClaw 3.7 era:

- redefine Task Ledger as a durable workflow layer instead of a platform-gap patch
- document parent/child task trees and parallel orchestration explicitly
- clarify when to use Task Ledger and when not to
- emphasize execution bindings, readiness checks, and recovery protocol
- keep short-first reporting as a first-class workflow pattern

## What changed in 0.2.4

- fixed final-stage advance behavior so `task-advance.py` clears `stage` when the last stage completes instead of logging a redundant self-transition
- preserved explicit close guidance in `nextAction` after the final stage completes

## Includes

- `SKILL.md` — agent-facing operating instructions
- `toolkit/scripts/` — helper scripts for lifecycle, recovery, control-plane relations, scheduling, migration, export, and reporting
- `toolkit/task-templates/` — generic templates, specialized examples, schema, and recovery notes
- `toolkit/tasks/README.md` — runtime directory guide
- `CHANGELOG.md` — tracked version history

## Runtime layout

When installed into a workspace, the toolkit expects:

- `tasks/`
- `logs/`
- `outputs/`
- `scripts/`
- `task-templates/`

## When to use Task Ledger

Task Ledger is a good fit when any of these are true:

- the task will likely run longer than 5 minutes
- the task has more than 3 stages
- the task uses background `exec`
- the task uses `sessions_spawn`
- the task uses `cron`
- the task has external side effects
- the user wants the work to be recoverable, resumable, or auditable
- multiple agents or sub-agents will work in parallel
- downstream work should wait on readiness or dependencies
- you need a short chat summary backed by a durable long report

## When *not* to use Task Ledger

Task Ledger is usually overkill for:

- short one-shot questions
- trivial file edits
- one-step commands that are cheap to rerun
- stateless lookups
- quick experiments where no durable record matters

Do not turn every tiny action into a task object.
Use it when the cost of losing state is real.

## Core workflow

1. Confirm plan with the user
2. Create the task skeleton first
3. Bind execution references as they appear
4. Advance stage-by-stage
5. Update task state after every meaningful step
6. Verify reality before resuming interrupted work
7. Correct stale task state when reality disagrees
8. Prefer short user-facing updates with file-backed long reports
9. Close the task explicitly

## Parallel orchestration pattern

Task Ledger works best for multi-agent work when you treat the task set as a tree, not a shared whiteboard.

Recommended pattern:

- create **one parent task** for the overall goal
- create **one child task per worker**
- bind each child task to its own execution reference
- let the parent task orchestrate readiness and finalization
- avoid having multiple workers write to the same task file

### Parent task responsibilities

A parent task should usually own:

- the overall goal
- `childTaskIds`
- dependency and readiness decisions
- final aggregation
- final side effects such as publish/deploy/finalize
- final report

### Child task responsibilities

A child task should usually own:

- its own stages
- its own `process.sessionId`, `subtask.sessionKey`, or `cron.jobId`
- its own result or error
- its own logs and artifacts

### Recommended parent stages

A practical default:

- `checkpoint`
- `spawn-children`
- `wait-for-children`
- `verify-readiness`
- `finalize`
- `report`

### Recommended child stages

A practical default:

- `inspect`
- `execute`
- `verify`
- `report`

## Typical flow

1. Create a parent task or single task
2. Add child tasks when the work should be parallelized or separated
3. Bind sessions/processes/cron jobs to the right task objects
4. Use dependency and readiness helpers before starting downstream work
5. Summarize progress in short form during execution
6. Export long-form reports when the task needs audit or handoff

## Example use cases

- safe OpenClaw gateway restarts
- service deployment with backup and rollback path
- long-running repair and migration tasks
- multi-stage maintenance workflows with recoverable state
- subtask-driven document or remote sync jobs
- parent/child task trees for larger maintenance programs
- multi-agent parallel release work with final readiness gates
- scheduling dependent tasks only when upstream work is actually done
- handoff or archival of task state and task graphs as Markdown
- short chat updates backed by full report files

## 0.3 roadmap

### 0.3.0 — positioning and workflow model

- redefine Task Ledger as a durable workflow layer for OpenClaw
- document when to use it and when not to
- document parent/child task trees and parallel orchestration explicitly
- clarify its relationship to ACP, sub-agents, `exec`, and `cron`

### 0.3.1 — parent/child aggregation

- improve parent-task summaries
- improve child-task completion aggregation
- improve task-tree and export views for orchestration work
- first implementation shipped via export-time child aggregation in `task-export.py`

### 0.3.2 — dependency and readiness semantics

- strengthen readiness-driven orchestration patterns
- improve dependency expression and downstream start conditions
- document or add helper patterns for fail-fast, wait-all, and partial-allowed workflows
- first implementation shipped via explicit task-level `readiness` config plus upgraded `task-ready.py` and `task-start-if-ready.py`

### 0.3.3 — deeper platform integration

- improve ACP and sub-agent binding guidance and helpers
- improve cron-linked task patterns
- strengthen restart, recovery, and finalization workflow templates

## Non-goals

Task Ledger is not:

- a replacement for OpenClaw runtime internals
- a replacement for ACP or sub-agents
- a generic workflow engine for every tiny action
- a substitute for platform-level routing, compaction, or session continuity

It is a lightweight but durable task governance layer on top of existing OpenClaw primitives.
