---
name: taku-build
description: >
  Execute an approved implementation plan. Triggers after /taku-plan, or on
  "build this", "implement the plan", "start coding", "run the plan",
  "execute tasks", "写代码", "开始实现", "执行计划", "开发吧", "开始写".
  Also handles worktree setup on "create a worktree", "isolated environment",
  "new branch workspace", "创建工作树".
---

# Taku Build - Auditable Implementation

Build implements the approved contract and leaves Review enough evidence to
decide whether the work can ship.

Rule labels: `[IRON LAW]` means a non-negotiable correctness constraint. `[GUIDANCE]` means a strong default that may adapt when context justifies it.

[IRON LAW] No production code without a failing test, reproduction, or explicit
verification anchor first. If the repo lacks a test harness, create the smallest
reproducible check and say why.

## Preflight

Before editing:

1. Read `PLAN.md`, an approved Quick mini design, or the explicit user-approved
   task contract.
2. If the plan has a `Build Agent Contract`, read Required fields first and use
   Optional fields only for context.
3. Load `references/tdd.md` for the local TDD cycle.
4. Use `references/worktrees.md` only when isolation is needed.
5. Choose execution mode yourself: sequential, parallel, or hybrid.

Do not ask the user to choose a mode unless the choice changes product scope,
cost, or risk.

## Output Contract

Build speaks in three stable shapes only.

### BUILD PREFLIGHT

```text
BUILD PREFLIGHT
- Mode: sequential | parallel | hybrid
- Reason: [one sentence]
- Subagents: available | unavailable; using sequential wave execution
- Waves: [wave-slug: task-slug list, or wave-1 for single task]
- Worktree: not needed | [path]
- TDD: enabled
- Ledger:
  - task-slug: files=[...] | tdd=[...] | status=pending | deviation=none | evidence=none
- Next: [first wave/task]
```

### BUILD UPDATE

```text
BUILD UPDATE
- Completed: [wave-slug or task-slug]
- Tasks: [task-slug list]
- Result: [tests/repro/spec check observed]
- Deviations: none | approved: [...] | needs-review: [...]
- Ledger delta: [only changed rows]
- Next: [next wave/task or REVIEW]
```

### BUILD COMPLETE

```text
BUILD COMPLETE
- Executed waves: [...]
- Task ledger: [all done | exceptions listed]
- Changed files: [...]
- Verification evidence: [commands and outcomes]
- Deviations: none | approved: [...] | needs-review: [...]
- Residual risk: none | [...]
- Status: READY_FOR_REVIEW | BLOCKED
- Next: REVIEW
```

The ledger is a handoff artifact, not a diary. Keep one row per task with these
fields: `task-slug`, `files`, `tdd`, `status`, `deviation`, `evidence`.

## Mode Selection

- **Sequential:** tasks are tightly coupled or there are 1-2 obvious steps.
- **Parallel:** tasks are independent and touch disjoint files.
- **Hybrid:** waves depend on earlier waves, but tasks inside a wave are
  independent.

Preserve plan task IDs when available. If the plan lacks IDs, create stable
kebab-case slugs. If a file appears in multiple tasks, those tasks are dependent
and must not run in parallel.

When subagents are unavailable, keep the same wave schedule and execute each
wave locally in order. Report that in `BUILD PREFLIGHT`.

## Execution Loop

For each task or wave:

1. Mark ledger row(s) `in_progress`.
2. Create the failing test, reproduction, or verification anchor.
3. Implement the smallest change that satisfies the spec.
4. Run the task verification.
5. Check spec compliance before code quality.
6. Update the ledger with status, evidence, and deviations.
7. Emit `BUILD UPDATE`.

Do not mark a task `done` until its spec and TDD/verification anchor have
evidence.

## Deviation Policy

Use the approved contract as the boundary.

- `deviation=none`: implementation matches the plan.
- `deviation=approved`: user explicitly approved the difference; preserve the
  approval in later summaries.
- `deviation=needs-review`: implementation differs from plan and has not been
  approved.

`needs-review` deviations block `READY_FOR_REVIEW` unless the deviation is the
only safe path and is clearly documented for Review.

## Reconciliation

After every parallel or hybrid wave:

- check for overlapping file changes
- run the smallest integration verification
- verify no task leaked outside its assigned files without recording a deviation

Reconciliation is required even when all individual tasks report done.

## Completion Gate

Before routing to Review:

- every task is `done` or explicitly `not-done` with reason
- every done task has evidence
- all deviations are either `none`, `approved`, or `needs-review`
- changed files are listed
- verification evidence is listed

Then emit `BUILD COMPLETE` and route to `/taku-review`.

## Known Pitfalls

**Ledger missing at Review.** Review cannot distinguish approved deviation from
scope drift.

Prevention: create the ledger in `BUILD PREFLIGHT` and preserve task slugs in
every update.

**Parallel tasks touched the same file.** One task overwrote another.

Prevention: duplicate file paths create dependencies; run them sequentially.

**TDD anchor skipped after a test-harness failure.** The agent called the code
"probably correct."

Prevention: debug or bound the harness failure, then preserve a verifiable
anchor before claiming completion.
