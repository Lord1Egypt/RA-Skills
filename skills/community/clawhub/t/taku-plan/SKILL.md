---
name: taku-plan
description: >
  Turn an approved design into an executable implementation plan. Three-step pipeline:
  scope + architecture review → design review (UI only) → plan writing. Auto-detects
  which step to start from based on project state. Invoke when DESIGN.md exists and
  is approved. Triggers on "write the plan", "create implementation plan", "plan this",
  "review this plan", "scope check", "architecture review", "design review",
  "is this plan buildable", "what could go wrong", "写计划", "制定方案",
  "规划实施", "架构评审", "这个方案可行吗", "有什么风险", or after /taku-think completes.
---

# Taku Plan — Review + Plan Pipeline

Rule labels: `[IRON LAW]` means a non-negotiable correctness constraint. `[GUIDANCE]` means a strong default that may adapt when context justifies it.

[GUIDANCE] Default path: run the three steps in sequence. Each gate must pass before the next unless the project state clearly shows that step is already complete.

## Step Detection

Check project state to determine where to start:

1. **DESIGN.md exists but not reviewed** → Start from Step 1 (Scope + Architecture Review)
2. **Design reviewed, UI project, design review not done** → Start from Step 2 (Design Review)
3. **All reviews done or not needed** → Go to Step 3 (Write Plan)

Announce which step you're starting from.

---

## Step 1: Scope + Architecture Review

Run when the design hasn't been through strategic and technical review. Catches scope mistakes (cheap to fix now, expensive later) and architecture gaps before code is written.

**Output destination:** Review artifacts (scope assessment, architecture diagram, edge cases, failure modes, test mapping) are appended to `DESIGN.md`, NOT to `PLAN.md`. The plan document is pure execution content.

Full process in `references/plan-review.md`. Load it and follow the instructions.

Quick summary:
- **Scope review:** Challenge premises, identify blind spots, pick a scope mode (EXPANSION / SELECTIVE EXPANSION / HOLD / REDUCTION)
- **Architecture review:** Component boundaries, data flow, edge cases, failure modes, test mapping
- Default: run both in sequence. Auto-detect scope-only or arch-only from phrasing.

If review produces critical gaps → stop and address them with the user before proceeding.

---

## Step 2: Design Review (UI Projects Only)

Only for projects with UI/UX components. Skip entirely for CLI, API, backend, infra.

**Output destination:** Design review scores and fixes are appended to `DESIGN.md`, NOT to `PLAN.md`.

Scores 9 dimensions (aesthetic, typography, color, spacing, layout, motion, responsiveness, accessibility, content hierarchy). Each gets 0-10, with specific fixes for anything below 8.

Full process in `references/design-review.md`. Load it and follow the instructions.

Skip when: no UI, or project uses an existing design system without customization.

---

## Step 3: Write the Plan

### Template Selection

Use `DEPTH_TIER` (set by the think phase or user) to pick the plan template:

| Tier | Criteria | Template |
|------|----------|----------|
| **Lightweight** | <50 files OR single-file change (1 dir touched) | Minimal — goal, files, spec per task |
| **Standard** | 50-500 files, moderate scope | Full template with Execution Hints |
| **Deep** | >500 files OR cross-cutting change (3+ dirs touched) | Standard + mandatory architecture diagram in header |

**Auto-reclassification:** If scope expands mid-sprint (e.g., a "simple bugfix" touches 6 files across 3 modules), escalate one tier. Log: `DEPTH ESCALATION: Lightweight -> Standard (reason: scope expanded to N files across M modules)`.

### Prerequisites

- Approved `DESIGN.md` exists
- Reviews completed (scope, architecture, design — as applicable)
- Read the design doc thoroughly before writing a single task

### File Structure Mapping

Before writing tasks, map every file that will be created or modified:

- Design units with clear boundaries and well-defined interfaces
- Prefer smaller, focused files — easier to reason about, more reliable edits
- Files that change together should live together (split by responsibility, not layer)
- In existing codebases, follow established patterns

### Task Granularity

Each task is a coherent unit of work — one responsibility, one set of files, one TDD anchor. The TDD cycle (write test → verify fail → implement → verify pass) is enforced by `/taku-build` at build time, not repeated in every task.

Instead of enumerating every TDD step per task, define WHAT the task must deliver: behavior, contracts, key assertions, and edge cases. The build agent reads the spec and applies TDD against it.

**Why spec over steps:** A 5-task plan with full TDD steps per task produces 25 checklist items where ~15 are boilerplate. Specs keep the plan focused on what matters — what to build and how to verify it — while the build agent handles the how.

### Plan Document Header

Use `references/plan.md` as the local starting scaffold for Standard and Deep plans. The rules below override the scaffold if they differ.

Every plan starts with:

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** Use `/taku-build` to implement this plan. The build agent should choose sequential, parallel, or hybrid execution unless the user explicitly overrides it.
>
> **Review context:** Scope and architecture reviews are in `DESIGN.md`. This document is execution-only.
>
> **Build Agent Contract:**
> - **Required:** Goal, Tech Stack, Execution Hints (if present), all Tasks (Depends on + Spec + Files)
> - **Optional:** Architecture details (in DESIGN.md), review artifacts (in DESIGN.md)
> - **Skip during execution:** Scope review, architecture review sections (already in DESIGN.md)

**Goal:** [One sentence]

**Architecture:** [2-3 sentences]

**Tech Stack:** [Key technologies]

---
```

### Execution Hints

*(Standard and Deep tiers only — skip for Lightweight)*

After the header and before tasks, include an optional execution hints section. The plan phase understands the dependency graph best — this section advises the build agent on execution mode and wave grouping. The build agent owns the final decision and may override.

```markdown
## Execution Hints

**Suggested mode:** [Sequential | Parallel | Hybrid]

**Wave 1** — [Wave purpose]
- Task 1: [short name]
- Task 2: [short name]

**Wave 2** — [Wave purpose]  *(if applicable)*
- Task 3: [short name]
- Task 4: [short name]

**Wave 3** — [Integration]  *(if applicable)*
- Task 5: [short name]
```

Omit this section entirely for plans with 1-2 tightly coupled tasks (sequential is obvious). Include it when:
- 3+ tasks exist and some are independent
- The dependency graph reveals parallelization opportunities
- Hybrid wave execution is the likely best choice

### Lightweight Template

For Lightweight tier only. Use this instead of the full Plan Document Header + Task Structure:

```markdown
# [Feature Name] Plan

> **Build Agent Contract:**
> - **Required:** Goal, Tech Stack, all Tasks (Spec + Files)
> - **Skip during execution:** Execution Hints (not needed for Lightweight)

**Goal:** [One sentence]
**Tech Stack:** [Key technologies]

### Task 1: [Name]
**Depends on:** none
**Files:** [paths]
**Spec:** [What to build, key assertions, edge cases]
**TDD anchor:** [Test file + test name]
```

### Task Structure

````markdown
### Task N: [Component Name]

**Depends on:** [Task M, ...] or `none`

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Spec:**

[What to build — describe behavior, contracts, and key assertions.]

Test that `function_name()`:
- returns [expected] when [condition]
- handles [edge case] by [behavior]
- raises [error] when [invalid input]

Edge cases: [empty input, concurrent access, boundary values, etc.]

**TDD anchor:** `tests/path/test.py::test_specific_behavior`
````

When the contract is non-obvious or the implementation approach is genuinely hard to describe, include a code sketch as part of the spec. Code blocks are optional context, not mandatory scaffolding.

### No Placeholders — Ever

These are plan failures:

- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases" — without specifying what errors, what validation, which cases
- "Write tests for the above" (without describing what the tests verify)
- "Similar to Task N" (repeat the spec — tasks may be read out of order)
- Specs that describe intent without defining verifiable behavior
- References to types, functions, or methods not defined in any task

### Self-Review Checklist

After writing the complete plan, run this against the design doc:

1. **Spec coverage:** Can you point every requirement to a specific task? List any gaps.
2. **Placeholder scan:** Search for TBD, TODO, "appropriate", "similar to". Fix them.
3. **Type consistency:** Do types, method signatures, and names match across tasks?
4. **Dependency integrity:** Every `Depends on` reference points to a real task. No circular dependencies. Tasks that can run in parallel have no mutual dependency.
5. **Spec verifiability:** Every task's spec describes concrete, testable behavior — not vague intent.
6. **Spec testability:** Can each spec's key assertions be written as automated test cases? Flag specs where testability is unclear — e.g., "handles edge cases gracefully" without specifying what "graceful" means.

Find issues? Fix inline.

### Scope Check

If the design covers multiple independent subsystems, suggest breaking into separate plans. If the plan exceeds 15 tasks, decompose by subsystem or dependency layer.

### Output

Save to `PLAN.md` at project root (or user-specified location).

### Execution Handoff

After saving:

"Plan saved to `PLAN.md`. If the plan is self-reviewed and within the approved scope, continue directly to BUILD.

At BUILD start, choose the execution mode yourself: sequential, parallel, or hybrid wave-based execution.

Announce a short BUILD PREFLIGHT that includes:
- chosen mode
- one-line reason
- execution waves when applicable, with `wave-slug: [task-slug, ...]`

Only stop before BUILD if the plan changed scope materially, introduced a costly or risky action, or left a key ambiguity unresolved."

---

## Known Pitfalls

**Skipping reviews because the plan "looks simple."** The design was a 2-page doc for "add notifications." Scope review found it touched 4 subsystems, required a new queue service, and had implications for the mobile app. "Simple" plans hide complexity in assumptions.

*Prevention:* Step detection is state-based, not subjective. If DESIGN.md hasn't been reviewed, run reviews.

**Plan references types or functions not defined in any task.** Task 3 calls `UserStore.findById()` but no task defines `UserStore`.

*Prevention:* Self-review checklist item 3. Read through all tasks sequentially and verify every reference has a definition.

**TDD ordering violated — code step before test step.** The implementer wrote the function, then wrote tests that pass against it — proving nothing.

*Prevention:* TDD is enforced by `/taku-build` at build time, not by the plan. Each task's spec defines testable behavior, and the build agent applies the write-test-first cycle automatically.

**Plan exceeds 15 tasks / 130+ steps.** Context limits were hit at task 14. The second half produced degraded quality.

*Prevention:* Scope check. Each plan produces working, testable software. Split by subsystem or dependency layer.
