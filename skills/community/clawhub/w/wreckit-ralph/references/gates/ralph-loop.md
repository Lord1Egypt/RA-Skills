# Gate: Ralph Loop

**Question:** Does the implementation satisfy the requirements?

The Ralph loop is the BUILD engine. Three phases, fresh context per iteration.

## Phase 1: Planning (no code)

1. Read PRD/spec/issue and existing codebase
2. Gap analysis: compare requirements against current code
3. Produce `IMPLEMENTATION_PLAN.md` — prioritized task list, single source of truth
4. Each task: one sentence, no "and"
5. **No code changes in this phase.**

Usually 1-2 iterations. Regenerate plan if it drifts — cheaper than salvaging.

## Phase 2: Building (one task per iteration, fresh context)

Each iteration is a **fresh session**. Context accumulation causes hallucination.

1. Read `IMPLEMENTATION_PLAN.md` + relevant code (nothing else)
2. Pick highest-priority incomplete task
3. Investigate codebase (don't assume)
4. Implement ONE task only
5. Run backpressure gates: slop scan + type check on diff
6. Gates pass → run tests, commit, update plan, exit
7. Gates fail → fix in same iteration, re-run
8. Exit → fresh context → next iteration

**Why fresh context:** No accumulated mistakes. Full token budget for THIS task. Reduced hallucination. Natural checkpoints.

**Backpressure:** Loop CANNOT advance past a failing gate. Environment rejects bad work automatically.

## Phase 3: Verification (after all tasks complete)

1. All tasks in plan marked complete
2. All programmatic gates passing
3. Run remaining gates (test quality, mutation kill, etc.)
4. Verification fails → loop back to Phase 2 with fix tasks

## Worker Roles

| Role | Use For |
|------|---------|
| **Architect** | Phase 1: design, data modeling, API contracts |
| **Implementer** | Phase 2: write code, implement features |
| **Tester** | Phase 2: test authoring, edge cases |
| **Reviewer** | Phase 3: code review, quality assessment |

Each role is a prompt prefix. One worker, one role, one task.

## Stopping Conditions

- ✅ All tasks complete + all gates pass
- ⚠️ Hard cap hit (default: 50 iterations) → Blocked with all evidence
- 🛑 Manual stop (`/stop` or `/subagents kill all`)
