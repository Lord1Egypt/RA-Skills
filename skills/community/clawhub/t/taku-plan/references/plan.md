# Implementation Plan Scaffold

Use this scaffold for Standard and Deep `/taku-plan` output. Replace every
placeholder before handoff.

> **For agentic workers:** Use `/taku-build` to implement this plan. The build
> agent chooses sequential, parallel, or hybrid execution unless the user
> explicitly overrides it.
>
> **Build Agent Contract:**
> - **Required:** Goal, Tech Stack, Execution Hints if present, all Tasks
>   with Depends on, Spec, Files, and TDD anchor.
> - **Optional:** Architecture details and review artifacts from `DESIGN.md`.
> - **Skip during execution:** Scope and architecture reviews already recorded
>   upstream.

**Goal:** {one sentence}
**Architecture:** {two or three sentences}
**Tech Stack:** {key technologies}

## Execution Hints

**Suggested mode:** Sequential | Parallel | Hybrid

**Wave 1** - {purpose}
- Task 1: {short name}

## Task 1: {task name}

**Depends on:** none

**Files:**
- Create: `{exact/path}`
- Modify: `{exact/path}`
- Test: `{exact/test/path}`

**Spec:**

{Concrete behavior, contracts, assertions, and edge cases.}

**TDD anchor:** `{test/path.py::test_behavior}`

## Task Summary

| # | Task | Depends On | TDD Anchor | Status |
|---|------|------------|------------|--------|
| 1 | {name} | none | {test} | Pending |
