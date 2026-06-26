---
name: refactoring
description: Deep refactoring workflow—characterization tests, incremental steps, behavior preservation, design direction, and verification. Use when improving structure without changing external behavior, or paying down tech debt safely.
---

# Refactoring (Deep Workflow)

Refactoring changes **structure**, not **behavior**. Safety comes from **small steps**, **fast feedback**, and verification (tests, golden outputs, or controlled manual checks).

## When to Offer This Workflow

**Trigger conditions:**

- Code is hard to change; duplication; unclear module boundaries
- Need to prepare an area for a new feature without mixing behavior change
- Paying down tech debt with management expecting “no user-visible change”

**Initial offer:**

Use **six stages**: (1) clarify goal & scope, (2) establish safety net, (3) plan increments, (4) execute with reviewable commits, (5) verify behavior, (6) document & follow-ups). Confirm test coverage and release pressure.

---

## Stage 1: Clarify Goal & Scope

**Goal:** Why refactor now—reduce coupling, enable feature X, remove dead code, improve naming.

**Exit condition:** Explicit **non-goals** (no feature changes in this effort unless separately scoped).

---

## Stage 2: Establish Safety Net

**Goal:** Prefer characterization tests for legacy; golden outputs for data pipelines; use snapshot tests sparingly.

### If tests are weak

- Approval tests, short exploratory scripts, or pair review with domain expert

---

## Stage 3: Plan Increments

**Goal:** Small commits, each leaving the codebase **working** (not necessarily perfect).

### Practices

- Move code, then change behavior in separate steps (Fowler-style when helpful)
- Separate mechanical renames from logic edits for reviewability

---

## Stage 4: Execute With Reviewable Commits

**Goal:** Each PR/commit tells a story; avoid thousand-line “cleanup” dumps.

---

## Stage 5: Verify Behavior

**Goal:** CI green; compare outputs for batch jobs; manual smoke on critical paths when needed.

---

## Stage 6: Document & Follow-Ups

**Goal:** ADR or short module README for new boundaries; tickets for remaining debt accepted consciously.

---

## Final Review Checklist

- [ ] Scope and non-goals explicit
- [ ] Safety net matches risk
- [ ] Incremental, reviewable steps
- [ ] Behavior verified
- [ ] Follow-up debt tracked

## Tips for Effective Guidance

- Keep refactor commits separate from feature commits when possible.
- If behavior must change, it is not “pure refactoring”—plan as a migration with communication.
- Under hotfix pressure, minimize refactor scope or defer.

## Handling Deviations

- **Strangler** refactors: maintain adapters at boundaries until cutover is complete.
