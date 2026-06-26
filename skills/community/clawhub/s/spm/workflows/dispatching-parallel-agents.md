# Dispatching Parallel Agents (with WBS Binding)

## Overview

Dispatch multiple subagents simultaneously for independent tasks. Each agent updates its WBS task entry.

**WBS Binding:** Each parallel task must have its OWN WBS row. All tasks are dispatched with `status=doing` simultaneously. Each returns with `status=done` + evidence individually.

## Prerequisites

OpenClaw parallel subagent support: **CONFIRMED WORKING** (tested 2026-05-04 — 3 subagents dispatched simultaneously, all completed independently without blocking each other.)

## When to Use Parallel

Use when:
- Multiple independent tasks exist (different files, different subsystems)
- Tasks have NO inter-dependencies
- No shared state between tasks

Don't use when:
- Tasks share files or state
- One task's output is input for another
- Need to understand full system state

## The Process

```
1. Identify parallel-eligible tasks from WBS ledger:
   - Check dependencies: none between these tasks?
   - Check file conflicts: different file sets?

2. For EACH task:
   - Update WBS: status=doing
   - Build dispatch prompt (full text, file context, task ID)

3. Dispatch ALL subagents SIMULTANEOUSLY:
   sessions_spawn(task="[Task 1]", ...)
   sessions_spawn(task="[Task 2]", ...)
   sessions_spawn(task="[Task 3]", ...)

4. WAIT for ALL to return:
   - Use sessions_yield to wait for completion events

5. For EACH returned subagent:
   - Read completion report
   - Update WBS: status=done + attach evidence
   - If blocked: update WBS: status=blocked + reason

6. REVIEW results:
   - Verify no conflicts between parallel changes
   - Run full test suite
   - If conflicts: fix manually
```

## Example

```markdown
WBS:
| ID | Work Package | Dependencies | Exit Criteria | Status |
|----|-------------|---------|---------------|--------|
| 2  | Add user model | 1 | Schema created, migration works | doing |
| 3  | Add auth endpoints | 1 | API returns tokens | doing |
| 4  | Add email validator | 1 | Validates correctly | doing |

All 3 tasks depend on Task 1 only (not on each other).
All 3 dispatched in parallel to different subagents.
```
