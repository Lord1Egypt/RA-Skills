---
name: writing-plans-enhanced
description: Use when you have a spec or requirements for a multi-step task, before touching code. Enhanced version with milestone timelines, data flow diagrams, mockups, and risk tables.
---

# Writing Plans — Enhanced

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase. Document everything they need to know: which files to touch, data flow, mockups, risks. Give them the whole plan as bite-sized tasks.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Effort:** ~N weeks | **Surfaces touched:** N packages | **New tables:** N | **Feature flag:** name
```

## Milestone Timeline

Ship in slices, each independently reviewable and each behind the flag. Nothing is user-visible until the last slice.

```markdown
### Milestone 1: Schema & API Contract (Week 1 · Mon–Tue)

New tables, migrations, and API stubs. No UI. Contract reviewed before anything else lands.

- `packages/db` — new migrations
- `packages/api` — tRPC router stubs

### Milestone 2: Core Component (Week 1 · Wed–Fri)

Static component rendered from fixtures. Optimistic insert on submit, rollback on failure.

- `apps/web` — new component
- `apps/storybook` — fixture stories

### Milestone 3: Realtime Integration (Week 2 · Mon–Wed)

Subscribe to changes. Track state for sidebar digest.

### Milestone 4: Notifications & Ramp (Week 2 · Thu–Fri)

Mention detection → notification row, email digest fallback, ramp feature flag.
```

## Data Flow

Describe the data flow from client to persistence. Use ASCII diagrams with solid = request/response, dashed = realtime/async.

```markdown
### Data Flow: Optimistic Write Path

Client                    API Server              Database
  │                          │                       │
  ├─► POST /tasks (optimistic)                       │
  │  ├─► update local cache immediately              │
  │  └─► send mutation ─────►┤                       │
  │                           ├─► validate ─────────►┤
  │                           │                       │
  │                           │◄─ 200 OK ─────────────┤
  │◄─ cache update ──────────┤                       │
  │                          │                       │

### Realtime Fan-Out (dashed path)

Database ─ ─ ─► WebSocket ─ ─ ─► Other clients
  │              │                  │
  └─► trigger ──►┤                  └─► re-render
                 └─► push notification
```

## Mockups

Not pixel-final — just enough that the reviewer and implementer agree on layout and placement.

```markdown
### A · Thread Inside an Open Task Card

┌──────────────────────────────────────┐
│  Ship onboarding empty-state rewrite  │
│  BIR-1142 · Assigned to Priya · Due  │
├──────────────────────────────────────┤
│  Priya: Should we add an illustration?│
│  You: Yes, let me mock it up          │
│                                       │
│  ┌─────────────────────────────────┐ │
│  │ Add a comment...          Post │ │
│  └─────────────────────────────────┘ │
└──────────────────────────────────────┘

### B · Sidebar Unread Digest

┌──────────────────────────────────────┐
│ 🔴 Jonah commented on BIR-1142       │
│    "Should the illustration swap..."  │
│ 🔵 Aiko mentioned you on BIR-1098    │
│    "@priya can you confirm..."        │
└──────────────────────────────────────┘
```

## Risk Table

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Migration locks table during deploy | Medium | High | Run with `CONCURRENTLY`; schedule off-peak |
| Realtime subscription leaks memory | Low | Medium | Add max-subscription cap; monitor heap |
| Feature flag not ramped correctly | Medium | Medium | Auto-alert if flag stuck > 3 days |

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**

- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

## Task Structure

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**
[code block]

**Step 2: Run test to verify it fails**
Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**
[code block]

**Step 4: Run test to verify it passes**
Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**
```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/plans/<filename>.md`. Two execution options:**

1. **Subagent-Driven (this session)** — I dispatch fresh subagent per task, review between tasks
2. **Parallel Session (separate)** — Open new session with executing-plans, batch execution with checkpoints

Which approach?"
