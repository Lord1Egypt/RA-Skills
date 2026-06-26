---
name: build
description: Use when an approved plan exists and needs execution, or when a hotfix/one-sentence scope needs direct TDD implementation — dispatches subagents per task, validates, reports
---

# /build

Execute plan tasks via subagents, validate, report.

**Announce:** "Starting /build — executing plan with subagent dispatch."

## Prerequisites

- Plan approved by `/review` (Step 4), OR one-sentence scope / hotfix (no plan)
- Working in a linked worktree (not primary)

## With Plan

### 1. Load

Read `ai-workspace/plans/<name>.md`. Extract tasks into ordered batches:
- Tasks under the same step or marked parallel = one batch
- Tasks with dependencies on prior tasks = separate sequential batch
- Note file paths, test expectations, and acceptance criteria per task

### 2. Execute Batches

Batches run sequentially. Tasks within a batch dispatch in parallel via subagents.

**Agent selection per task:**

| Plan structure | Agent | Notes |
|---|---|---|
| Separate "write test" + "implement" tasks | `test-writer` (RED) then `implementer` (GREEN) | Sequential within the pair |
| Combined task ("implement X with tests") | `implementer` | Handles TDD internally |
| Docs-only task | `doc-writer` | |

**Parallel safety:** only dispatch tasks in parallel when they touch different files.

**Subagent prompt — provide each agent:**

```
You are implementing Task N: [task name]

## Task Description
[FULL TEXT from plan — paste it, don't make the subagent read the file]

## Context
[Where this fits, what earlier batches produced, architectural decisions]

## Working Directory
[Absolute path to worktree]

## Project Conventions
- TDD: write failing test first, make it pass, refactor
- Commit after task completes (conventional commits) AND ensure your work is on disk before reporting DONE — the inter-batch step commits a batch boundary, but your task-level commits make recovery from inter-batch failures cleaner
- TypeScript strict, ESM, Biome, Vitest, Pino logger, no barrel exports
- Self-review before reporting back

## Report: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
```

**Handle responses:**

| Status | Action |
|---|---|
| DONE | Mark task complete |
| DONE_WITH_CONCERNS | Read concerns — if correctness/scope, address before continuing |
| NEEDS_CONTEXT | Provide missing context, re-dispatch |
| BLOCKED | Assess: more context? more capable model? break smaller? escalate to human? |
| Task touches protected file | Stop immediately — never dispatch |

Never retry BLOCKED without changing something.

**Inter-batch check** — after each batch, verify no regressions AND commit the batch's output before starting the next batch:

```bash
pnpm typecheck && pnpm test
git -C "$WORKTREE" add -A
git -C "$WORKTREE" commit -m "<type>(<scope>): batch N — <summary>"
```

Per-task commits inside a batch are best-effort; **batch-boundary commits are mandatory** (per `/task` invariant `REQUIRE batch.commit BEFORE batch.next`). A batch that finishes verify but doesn't commit can lose all its work if the next batch fails or the session ends. The wip-checkpoint Stop hook (ADR-008) captures dirty state at session end as a backstop, but inter-batch commits keep the recovery shape clean — per-batch granularity in branch history rather than a single dirty-state blob on the side ref.

### 3. Validate (Hard Gate)

After ALL batches complete:

```bash
pnpm validate
```

Read the output. Never claim success without evidence. If it fails:
1. Diagnose the failure
2. Fix (dispatch subagent or fix directly for small issues)
3. Re-run `pnpm validate`
4. Max 3 fix-validate cycles. If still failing, stop and report.

Step 6 (`/review`) CANNOT begin until validate passes.

### 4. Report

```
Build complete.
Tasks: <completed>/<total>
Validate: PASS
Next step: /review (Step 6)
```

Include any DONE_WITH_CONCERNS notes. Update `.branch-context.md` with decisions made during build.

## Without Plan (Hotfix / One-Sentence Scope)

Implement directly — no subagent orchestration for small scope.

1. **TDD**: write failing test (RED), implement fix (GREEN), refactor
2. **Minimal change**: fix the defect, nothing else (hotfixes)
3. **Root cause**: document in commit message body (hotfixes)
4. **Validate**: `pnpm validate` — same hard gate, same 3-attempt max

## Codex / Cursor Fallback

No subagent dispatch. Execute tasks sequentially in main session. Same validation gate applies.

## Integration

| Relation | Skill |
|---|---|
| Called by | `/task` (Step 5) |
| Depends on | `/blueprint` (Step 3) + `/review` plan approval (Step 4) |
| Followed by | `/review` build review (Step 6) |
