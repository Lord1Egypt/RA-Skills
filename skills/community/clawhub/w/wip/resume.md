# Resume — Task cleanup and remaining work

Environment-agnostic (Claude Code / Antigravity) **task cleanup + remaining-work** workflow.

- **Cleanup** = remove completed/stale items (no user confirmation required)
- **Remaining work** = per-item direction ask → execute selected items

## When to Use

- User invokes "task cleanup and remaining work", "task cleanup", "remaining work", "resume task", "task resume"
- Immediately after `/wip` (SKILL.md "/wip Entry Procedure" references this topic)
- Resuming after a compact (need to identify outstanding work)

## Environment Detection

| Environment | Data medium | Tool guide |
|-------------|-------------|------------|
| Claude Code | `TaskList` / `TaskCreate` / `TaskUpdate` API | [claude.md](./claude.md) |
| Antigravity (Gemini) | `<appDataDir>/brain/<conversation-id>/task.md` artifact + `ask.md` emulation | [antigravity.md](./antigravity.md) |

Environment detection:
1. `TaskList` tool callable → Claude Code
2. `task.md` artifact exists or `appDataDir` context present → Antigravity
3. If both, prefer Claude Code (TaskList is more reliable)

## Step 1. Cleanup (FIRST — no user confirmation required)

Remove stale items immediately. The goal is to take them out of the selectable list so the next step's context is not muddied.

### Deletion targets

| Status | Deletion condition |
|--------|--------------------|
| `completed` | Completed tasks have no tracking value in the next session (their summary is already reflected in persistent files such as fix_plan.md) |
| `in_progress` (residue from a prior session) | `in_progress` from before the compact is meaningless due to broken context |
| `pending` (unrelated) | Stale items unrelated to other pending entries or new work |

### Do NOT delete

- The user has explicitly asked to "keep completed tasks"
- Tasks that belong to **an in-flight fix procedure** such as the `fix-*` series

### Per-environment commands

| Environment | Cleanup command |
|-------------|-----------------|
| Claude Code | `TaskList` → identify deletion targets → call `TaskUpdate(taskId, status: "deleted")` for each |
| Antigravity | Read `task.md` → identify lines to delete → remove those lines via `replace_file_content` |

## Step 2. Per-item direction ask

After Step 1, ask the direction for each remaining incomplete item (`pending` + `in_progress`).

### Direction options

| Label | Meaning |
|-------|---------|
| **Proceed** | Start execution as currently defined |
| **Split** | Split the larger task into smaller sub-tasks |
| **Merge** | Combine with another task into a single one |
| **Hold** | Defer until another task completes (precedence dependency) |
| **Delete** | No longer needed |

### Don't / Do — environment-agnostic

| # | Don't | Do |
|---|-------|-----|
| 1 | Ask only "which one first?" (priority alone) | Decide **per-item** direction (proceed / split / merge / hold / delete) first |
| 2 | Compress 5 items into a single ask | One independent question per item (Claude's `questions` array maxes at 4 — report the rest as "deferred") |
| 3 | Bundle tasks under one ask via `multiSelect` | Each question independently decides the direction of its task |
| 4 | Mark the first item `in_progress` without the direction ask | Step 3 may only be entered after Step 2 is complete |

### Per-environment ask method

| Environment | Ask method |
|-------------|-----------|
| Claude Code | `AskUserQuestion` — one question per task in the `questions` array, max 4 (details: [claude.md](./claude.md) → "AskUserQuestion — per-item direction ask") |
| Antigravity | `ask.md` emulation (`ArtifactType: "other"`, `RequestFeedback: true`) — per-item options + Pros/Cons (details: [antigravity.md](./antigravity.md) → "Workflow → 1. Interactive Task Selection") |

### Auto-proceed exception (Claude Code)

If a task subject contains only simple **lookup/check keywords**, execute it immediately without asking and reflect the result (see [claude.md](./claude.md) → "Auto-proceed — verification/lookup tasks need no ask").

| Example keyword | Auto-run command |
|-----------------|------------------|
| "CI result", "PR state", "deploy check" | `gh pr checks` / `gh pr view` / `curl` |

The check result is reflected in **both** the task subject update **and** the matching `[x]` in the checklist file.

## Step 3. Decide start priority and execute

Among the items decided as "Proceed" in Step 2, decide the start priority → mark the first item `in_progress` → perform the work.

### Per-environment execution

| Environment | Execution |
|-------------|-----------|
| Claude Code | `TaskUpdate(taskId, status: "in_progress")` → work → `TaskUpdate(status: "completed")` |
| Antigravity | Change the matching line in `task.md` to `- [/]` → work → change to `- [x]` |

### When there are 5 or more items

The ask-medium ceiling (Claude `questions` max 4, Antigravity `ask.md` visibility) means only the top 4 by priority are asked. The rest are reported in the "deferred / external wait" category only (re-ask on the next `/wip`).

## Task decomposition — synchronization with checklist files (MANDATORY)

`[ ]` open items in `fix_plan.md` / `checklist.md` are **pulled into tasks for execution tracking**.

### Core distinction

| Checklist item | Task handling |
|----------------|---------------|
| `[ ]` open (autonomously actionable) | **Register as an execution task** |
| `[ ] [BLOCKED]` (waiting on external response / permission) | **Do NOT create a task**. Leave it in the checklist; promote it to a task when the trigger arrives |
| `[x]` completed | **Bundle into a single cleanup task** (Completed move) — not one per item |

### Medium separation principle (HARD STOP)

| # | Don't | Do |
|---|-------|-----|
| 1 | Register a `[BLOCKED]` item as a task | Keep it in the checklist's hold section; do not register a task |
| 2 | Double-register BLOCKED items under the rationale "having it in the task list helps me not forget" | The checklist is reloaded every session, so it won't be forgotten. Duplicating the medium increases sync overhead |
| 3 | Use `[BLOCKED]` as a task subject prefix | Use the checklist's `## Hold` section: `- [ ] [BLOCKED] <subject> (trigger: ...)` |
| 4 | Report "BLOCKED still BLOCKED" on every `/wip` for external-wait tasks | If it is not in the task list, it is not a reporting target. When the response arrives, promote it from the checklist to a task |

### Ordering principle

Execution tasks (work to do now) come **first (top)**, hold tasks last. Because environment-specific additions append to the end:

1. Temporarily remove existing hold tasks
2. Extract all `[ ]` open items from the checklist → register them as execution tasks (top of the list)
3. Register a single `[x]` Completed-move task (if needed)
4. Re-register the hold tasks (bottom of the list)

## Violation history

- 2026-05-03 (wip 2nd recurrence): With 5 remaining items, only "which one first?" was asked → Step 2 was skipped. Reinforced via the "/wip Entry Procedure" added to SKILL.md.
- 2026-05-12 (D 2nd recurrence): Only the `[x]` items were turned into a cleanup task while the `[ ]` open work was not promoted to tasks → "Don't just leave it sitting in fix_plan — pull it into the task list" feedback received.
- 2026-05-20 (origin of this topic): The natural-language trigger "task cleanup and remaining work" was scattered across cleanup Phase 0 and wip Step A, lacking a single entry point. The resume topic was introduced to unify them.

## Quick Reference

```text
/wip or "task cleanup and remaining work" invocation
  ↓
Step 1: Cleanup (immediate, no ask)
  ├─ Claude: TaskList → TaskUpdate(status:"deleted") × N
  └─ Antigravity: task.md → replace_file_content
  ↓
Step 2: Per-item direction ask
  ├─ Claude: AskUserQuestion (questions array, 1 question per task, max 4)
  └─ Antigravity: ask.md (RequestFeedback: true)
  ↓
Step 3: Start priority + execute
  ├─ Claude: TaskUpdate(in_progress) → work → TaskUpdate(completed)
  └─ Antigravity: - [/] → work → - [x]
```
