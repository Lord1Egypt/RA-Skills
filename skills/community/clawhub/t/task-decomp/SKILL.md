---
name: task-decomp
description: "Plan, track, and learn from complex multi-step tasks. Decomposes requests into dependency-aware subtasks with parallel execution, progress tracking, and a learning loop that improves future plans from past outcomes. Use when: (1) A request involves 3+ steps with dependencies, (2) Work spans multiple tools or sub-agents, (3) User says 'plan this out', 'break this down', or 'how should we approach this', (4) Managing a project, workflow, or multi-phase build, (5) Coordinating parallel workstreams. Improves over time — completed plans feed back into planning intelligence. NOT for: simple one-shot requests, single tool calls, or conversational exchanges."
---

# Task Decomposition

Plan complex work. Track it. Learn from it. Get better at planning over time.

## Plan Format

Store plans in `plans/` (workspace-relative). Name: `[slug].plan.md`. Multiple concurrent plans supported.

```markdown
# Plan: Deploy new API
Started: 2026-03-03 11:00
Status: in-progress
Revised: 1

## Tasks

- [x] 1. (S) Provision database — Postgres 16, endpoint saved to .env
- [ ] 2. (M) Build auth middleware (depends: 1)
- [ ] 3. (M) Build CRUD endpoints (depends: 1)
      ↳ parallel with 2
- [ ] 4. (L) Integration tests (depends: 2, 3)
- [ ] 5. (S) Deploy to staging (depends: 4) ⚠️ blocked: waiting on VPN access
      spawned: session-k9x2

## Retro
<!-- filled on completion -->
```

### Notation
- **Size:** `(S)` <30min, `(M)` 30min-2h, `(L)` 2h+
- **Dependencies:** `(depends: 1, 3)` = must complete first
- **Parallel:** `↳ parallel with N` = concurrent with task N
- **Blocked:** `⚠️ blocked: [reason]`
- **Delegated:** `spawned: [session-id]`
- **Done:** `- [x]` with outcome after dash: `— result summary`

## Planning

1. Read the FULL request before decomposing
2. Identify boundaries: different tools, contexts, or outputs = different tasks
3. Mark real dependencies only — parallel what CAN be parallel
4. Size each task (S/M/L) — makes progress reports honest
5. Action-oriented names: "Install X", "Configure Y", "Verify Z"
6. **Check `plans/` for similar past plans** — reuse what worked, avoid what didn't

## Execution

1. Work in dependency order, parallelize where noted
2. Update plan after each TASK completes (not each tool call)
3. Blocked? Mark it, work next unblocked task
4. Record outcomes — future you needs them

## Revision

Plans change mid-flight. When they do:
- **Insert:** Add with next number, update downstream `depends:`
- **Remove:** ~~Strikethrough~~, don't renumber (preserves refs)
- **Reorder:** Update `depends:` only
- **Bump** the `Revised:` counter

Don't follow a bad plan to completion.

## Resume (After Restart)

When you find an existing plan:
1. Read it — check Status
2. Find first unchecked, unblocked task
3. Quick sanity check that prior tasks still hold
4. Continue — or revise first if context changed

## Failure

- Task fails → note it, assess: can downstream tasks still run?
- Unrecoverable → Status: `abandoned`, explain why
- Always record what DID work — partial progress has value

## Sub-agent Delegation

- One sub-agent per independent BRANCH, not per task
- Record session ID on the task line
- Don't poll in loops — check on events or when asked

## Progress Report

When asked "status?" or "where are we?":
```
📋 Plan: Deploy new API
Progress: 3/7 tasks (1L + 2S remaining)
Current: Task 4 (L) — running integration tests
Blocked: Task 5 — waiting on VPN access
Revised: 1x
```

Size-aware > task-count. "1/5 done" is misleading when the 4 remaining are all (L).

## Learning Loop ← what makes plans improve

### Retro (on completion)

When a plan finishes (completed or abandoned), fill the `## Retro` section:

```markdown
## Retro
- **What worked:** Parallelizing tasks 2+3 saved ~1h
- **What didn't:** Underestimated task 4 (sized M, was actually L)
- **Sizing accuracy:** 3/5 tasks sized correctly
- **Dependencies missed:** Task 5 actually needed task 2 directly, not just via 4
- **Reusable pattern:** [If this plan type recurs, note the template]
```

### Patterns File

Maintain `plans/patterns.md` — distilled lessons from retros:

```markdown
# Planning Patterns (learned from retros)

## Sizing
- API integration tasks: usually (M), not (S)
- "Write tests" is always bigger than you think → size up one level
- Database migrations with data backfill: always (L)

## Dependencies
- Auth must come before any authenticated endpoint work
- Don't parallelize tasks that write to the same config file

## Templates
- **API build:** provision → auth + endpoints (parallel) → tests → deploy
- **Research report:** gather sources → analyze (parallel per source) → synthesize → review
```

This file gets checked during Step 6 of Planning ("check past plans"). Over time, sizing gets more accurate, dependency mistakes stop repeating, and common project types get reusable templates.

### Decay

Review `patterns.md` monthly. Remove patterns that:
- Haven't applied in 30+ days
- Were wrong more than once
- Are too project-specific to generalize

## Archive

Completed/abandoned plans → rename `[date]-[slug].plan.md`:
```
plans/
├── deploy-api.plan.md              # active
├── patterns.md                     # learned patterns
├── 2026-03-01-setup-acw.plan.md    # archived
└── 2026-03-02-osint-recon.plan.md  # archived
```

## Anti-patterns

- **Over-decomposition:** 15 tasks for 4 steps of real work
- **Phantom dependencies:** Marking sequential what's actually parallel
- **Plan worship:** Following a wrong plan because it exists
- **Size blindness:** "4/5 done!" when the remaining task is (L)
- **Skipping retros:** No retro = no learning = same mistakes forever
