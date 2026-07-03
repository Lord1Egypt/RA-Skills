---
name: wip
description: |
  Track in-session work progress. Register steps for 3+ step tasks, update status per step, handle completion/abort.
  On /wip invocation, when remaining tasks exist, AskUserQuestion is required for the per-item direction (proceed / split / merge / hold / delete) — asking only about start priority is forbidden.
  After a compact, show prior-work summary then AskUserQuestion(multiSelect) for restore selection and re-register via TodoWrite.
  antigravity - task.md artifact-based checklist (Antigravity environment) [antigravity.md],
  claude - TodoWrite/TaskCreate API guide (Claude Code environment) [claude.md],
  resume - environment-agnostic task cleanup + remaining-work workflow [resume.md].
  "wip", "track progress", "register tasks", "task register", "step tracking", "compact recovery", "task resume", "resume task", "cleanup + resume" triggers.
metadata:
  author: es6kr
  version: "0.1.1"
---

# WIP (Work In Progress)

Track current session work as a checklist.

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| antigravity | task.md artifact-based checklist for Antigravity sessions | [antigravity.md](./antigravity.md) |
| claude | TodoWrite/TaskCreate API for Claude Code sessions | [claude.md](./claude.md) |
| resume | Environment-agnostic task cleanup + remaining-work workflow | [resume.md](./resume.md) |

## Topic Dependencies

```text
wip (entry — /wip or "task cleanup + remaining work")
  └─→ resume (environment-agnostic workflow)
        ├─→ claude (Claude Code: TaskList/TaskCreate/TaskUpdate/AskUserQuestion)
        └─→ antigravity (Antigravity: task.md artifact + ask.md emulation)
```

- **resume**: workflow procedure (cleanup → per-item direction ask → execute). Environment-agnostic.
- **claude / antigravity**: per-environment tooling. Defines how resume Step 1–3 is implemented in each environment.

## Purpose

Record in-progress work via **at least one** of:
1. **TodoWrite / TaskCreate** — in-session tracking
2. `checklist.md`, `fix_plan.md` and similar markdown files — persists across sessions
3. **Commit** — preserve incomplete code with a `WIP:` tag for later amend/squash

Emitting only a text summary without persistent recording does not satisfy `/wip`.

## When to Use

- Starting a multi-step task (3+ steps)
- User gives a large task instruction
- Need to show progress to the user
- When you want to record/preserve the current state mid-session
- "task cleanup + remaining work", "task cleanup", "remaining work", "resume" invocations

## /wip Entry Procedure (CRITICAL)

`/wip` or "task cleanup + remaining work" invocations must follow the **3 steps in [resume.md](./resume.md)** in order. Skipping steps is forbidden:

1. **Step 1 — Cleanup**: immediately delete stale completed/in_progress entries (no user confirmation required)
2. **Step 2 — Per-item direction ask**: for each remaining item, decide proceed / split / merge / hold / delete
3. **Step 3 — Start priority + execute**: among items decided as "proceed", choose start priority, mark in_progress, and execute

Environment implementations:
- Claude Code → [claude.md](./claude.md) (TaskList/TaskCreate/AskUserQuestion)
- Antigravity → [antigravity.md](./antigravity.md) (task.md + ask.md)

**Violation history**:
- **2026-05-03 (1st)**: With 5 pending tasks, `/wip` was invoked and only "which one first?" was asked — per-item direction (split/merge/delete) was skipped.
- **2026-05-03 (2nd)**: With 6 completed entries lingering in TaskList, `/wip` asked per-item direction only for pending #20 — completed tasks were not cleaned up. User pointed out: completed tasks unrelated to the remaining ones must be cleaned. Step 1 (cleanup of completed/irrelevant tasks) was promoted to an explicit step.
- **2026-05-20 (resume topic introduced)**: The "task cleanup + remaining work" natural-language trigger was split across cleanup Phase 0 and wip Step A — a single entry point was missing. The resume topic was introduced to unify them.

## Quick Reference

### Resume (environment-agnostic)

`/wip` or "task cleanup + remaining work" → Step 1 cleanup → Step 2 per-item direction ask → Step 3 execute. Per-environment tooling lives in claude / antigravity.

See [detailed guide](./resume.md).

### Claude

Use `TodoWrite` for sequential steps, `TaskCreate` for parallel tasks with dependencies.
After compact, restore prior work: show summary → multiSelect → re-register via TodoWrite.

See [detailed guide](./claude.md).

### Antigravity

Use `task.md` artifact with standard markdown checkboxes (`- [ ]`, `- [/]`, `- [x]`).
Do NOT wrap checkboxes in backticks.

See [detailed guide](./antigravity.md).

## Skip Conditions

WIP tracking is unnecessary for:
- Single command execution (kubectl get, ls, etc.)
- Tasks with 2 or fewer steps
- Read-only queries
- User explicitly says "keep it simple"

## Rules (Sequential Flow)

- **One in_progress at a time** — applies to ordered/sequential tracking (TodoWrite/checklist mode)
- **Update immediately on completion** — mark completed as soon as done
- **No skipping** — proceed in order, don't start next step before completing current
