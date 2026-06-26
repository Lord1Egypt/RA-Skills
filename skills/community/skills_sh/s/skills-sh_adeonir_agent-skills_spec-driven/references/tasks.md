# Task Decomposition

Break design into implementable tasks.

## Contents

- [When to Use](#when-to-use)
- [Depth Scaling](#depth-scaling)
- [Workflow](#workflow)
- [Task Size Guidelines](#task-size-guidelines)
- [Dependency Markers](#dependency-markers)
- [Guidelines](#guidelines)
- [Commit Boundary Grouping](#commit-boundary-grouping)
- [Tasks Template](#tasks-template)
- [Error Handling](#error-handling)

## When to Use

- Scope is **Medium**, **Large**, or **Complex** (check `scope:` in spec.md frontmatter) — depth scales with scope (see Depth Scaling below)
- design.md is complete
- Ready to define implementation steps

## Depth Scaling

Tasks runs at every scope above Small. What scales is depth:

- **Medium — light (flat step list).** Emit the canonical steps as a flat task
  list, each with Done-when and a Satisfaction sketch, plus Quality Gates and
  Requirements Coverage. Dispatch the Plan subagent (Step 4) at light depth. Skip
  the heavy execution-plan diagram and cross-story dependency analysis — a
  canonical reapplication has no branching to graph.
- **Large/Complex — full.** The full breakdown below: story grouping, ID
  monotonicity, dependency markers, execution-plan diagram; the Plan subagent
  (Step 4) runs at full depth.

If the flat Medium list surfaces hidden decisions or branching dependencies,
escalate Medium → Large (see [auto-sizing.md](auto-sizing.md) Safety Valve).

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

Track each step as it completes — mark it done before moving to the next.
In Claude Code, create a task list at phase start (TaskCreate) and update
each step as it completes (TaskUpdate).

### Step 1: Resolve Feature

1. If a name is given -> match `.artifacts/specs/{date}-{name}/` (glob `*-{name}` or `*-{name}-*` for a collision variant)
2. If no name -> match current git branch to `branch:` in spec.md frontmatter
3. If multiple or no match -> list available specs and ask user

### Step 2: Load Context

Read:
- `spec.md` (requirements)
- `design.md` (architecture)
- `decisions.md` (if exists, for resolved gray areas)

**Blocking-question gate:** If spec.md `## Open Questions` holds any question that
would change the task breakdown you are about to produce (a blocking question), halt:
list the blocking items, route to [discuss](discuss.md) or the user to resolve, then
exit. Non-blocking questions — tentative, deferred-with-reason, or immaterial to this
phase — do not gate; proceed.

### Step 3: Detect Quality Gates

Read `package.json`:
- Lint script
- Typecheck script
- Test script

### Step 4: Dispatch Tasks Plan subagent

Steps 5-7 are owned by a Plan subagent. Main agent dispatches once,
receives structured slot fillers, composes tasks.md per the tasks
template (below), then runs Step 8 pre-approval checks against the
artifact before advancing to Step 9.

Why dispatched: Steps 5-7 are intelligence-sensitive (story grouping,
top-to-bottom ID monotonicity, forward-dependency detection, execution
plan diagram). Isolating them in a Plan subagent keeps main context
clean for the user-visible pre-approval checks and approval gate.
Plan is read-only by harness contract (Edit/Write/NotebookEdit
excluded), so it returns structured slot fillers; main composes the
artifact via the canonical template (pattern A1: Plan returns slots,
main fills template).

At **Medium**, dispatch the Plan subagent at light depth (Steps 5-7 with the
reduced slot set). Run Steps 5-7 inline only when subagent support is
unavailable; main agent executes them directly in that case.

Subagent brief:

- Inputs (paths only -- Plan reads from disk):
  - `.artifacts/specs/{date}-{name}/spec.md`
  - `.artifacts/specs/{date}-{name}/design.md`
  - `.artifacts/specs/{date}-{name}/decisions.md` (if exists)
  - Quality gate commands from Step 3 (lint, typecheck, test)
- Reference: the tasks template inlined at the bottom of this
  reference — return chunks matching the template section order and
  table shapes exactly
- Process: follow Step 5 (Decompose Tasks, including story order,
  ID monotonicity, commit boundary, forward-dependency rules), Step 6
  (Execution Plan diagram), Step 7 prep (organize chunks per template
  section). Run the Commit-Boundary Viability Check internally
  (silent) before returning -- resolve any hidden forward dependency
  via restructure, reorder, or escalation back to design.
- Return shape (structured slot fillers per template section, no
  surrounding prose):
  - Summary: total task count
  - Execution Plan: ASCII diagram (sequential `→`, parallel
    branches `├→`/`└→`, convergence points)
  - Quality Gates: lint, typecheck, test commands from Step 3
  - Tasks: story groups in spec.md order (`### US-N [Px] Title`),
    each containing tasks with monotonic IDs top-to-bottom, dependency
    markers (`[P]`, `[B:T-X]`), Tests / Gate / Done when fields
    (Tests and Gate only when test infrastructure detected in Step 3),
    Satisfaction sketch field per task (one line: why this
    implementation actually moves the criterion -- mechanisms cited
    must exist within the task's own scope or in earlier tasks),
    Candidate trace sub-block (investigation tasks only -- enumerate
    every candidate from the spec with evidence for and against,
    omit on non-investigation tasks)
  - Requirements Coverage: Story-to-Tasks mapping rows, AC-to-Tasks
    mapping rows
- Do NOT return: prose narration, Files/Reference/Commit metadata
  lines per task, Phase 0 / Setup sections outside the story
  structure, Commit-Boundary Viability Check `[pass]` lines (silent
  per Step 8)

Main agent composes `tasks.md` by writing Plan's chunks into the
tasks template (below) slots. Preserve template section order, story
order from spec.md, and ID monotonicity exactly. After writing, run
Step 8 pre-approval checks against the composed artifact -- display
each item as `[pass]` or `[fail]`. If any item fails, re-dispatch
Plan with the failure list as additional brief context.

_Steps 5-7 below describe the process Plan follows. Read them as
Plan's substeps when dispatched, or as main agent's process when
dispatch is skipped._

### Step 5: Decompose Tasks

Group tasks by user story. Each user story in spec.md becomes a `### US-N [Px] {User Story Title}` section in tasks.md. Tasks within a group implement that user story's acceptance criteria.

**Story order is fixed.** Emit user stories in the exact order they appear in spec.md: US-1 first, then US-2, then US-3, and so on. Do not reorder user stories by technical dependency, risk, or setup-first instinct -- the user reads and commits user stories in the order the spec declares them.

**Task IDs are assigned top-to-bottom, in document order.** The first task listed in tasks.md is `T-1`. The second is `T-2`. Numbering is monotonic as the reader scrolls down. This means:

- All of US-1's tasks are listed first and get IDs `T-1..T-k`
- US-2's tasks follow and get `T-(k+1)..T-m`
- US-3 continues from there, and so on

Never assign a low ID (e.g. `T-1`) to a task that appears later in the document than a higher ID. A reader scanning top-to-bottom must see ascending IDs.

**Commit boundary: each user story is independently shippable.** The user must be able to execute and commit only US-1's tasks without pulling in work from US-2 or later user stories. This forbids **forward dependencies**:

- Allowed: `T-5 [B:T-2]` inside US-2 blocking on T-2 inside US-1 (backward dep)
- Forbidden: `T-2 [B:T-5]` inside US-1 blocking on T-5 inside US-2 (forward dep)

If a task seems to need something from a later user story, the dependency is a signal the user stories are wrong -- either merge them, reorder them in spec.md (then reflect here), or pull the shared prerequisite into the earlier user story.

**Shared infrastructure tasks** (test tooling, lint config, base types used by every user story) belong to the first user story that needs them -- typically US-1. Do not invent a "Phase 0" or "Setup" section outside the story structure; setup that serves one user story lives in that user story.

Within each story group, generate tasks following natural order:
1. Setup (config, deps) -- only if not already done in an earlier user story
2. Types (interfaces)
3. Implementation (core logic, tests included per task)
4. Integration (connect)

Each task should be:
- **Atomic**: Completable in one session
- **Testable**: Has verifiable outcome
- **Independent**: Minimal dependencies
- **Traceable**: Maps to requirements

**Task ID format:** `T-1, T-2, T-3...` -- sequential across the entire tasks.md in document order, dash-separated with no padding, never reused.

**Task description format:**

Without test infrastructure:
```text
- [ ] T-1 [P] {verb} {what}
  - **Done when:** {verifiable outcome}
  - **Satisfaction sketch:** {one line: why this implementation actually moves the criterion}
```

With test infrastructure (test script detected in Step 3):
```text
- [ ] T-1 [P] {verb} {what}
  - **Tests:** unit|integration|e2e|none
  - **Gate:** quick|full|build
  - **Done when:** {verifiable outcome}; gate passes, no tests deleted
  - **Satisfaction sketch:** {one line: why this implementation actually moves the criterion}
```

`Tests` declares the test type written in this task. `Gate` declares which gate command to run.
`Done when` is a concrete, verifiable condition. When test infrastructure exists it must
confirm the gate passes and no tests were deleted (count after ≥ count before).

`Satisfaction sketch` is a one-line rationale for why the proposed implementation actually
moves the criterion. The mechanisms cited must exist within the task's own scope or in
earlier tasks -- if the rationale depends on a missing or later task, the Done when must
be relaxed or the missing task must be added.

**Investigation-task shape:** Tasks that profile, analyze, or trace (rather than build)
must include a `Candidate trace` sub-block enumerating every candidate from the spec
with evidence for and against each. A mitigation may only be chosen after every candidate
is evaluated; premature rejection is a smell.

```text
- [ ] T-1 [P] {verb} {what}
  - **Done when:** {verifiable outcome}
  - **Satisfaction sketch:** {one line: why this implementation actually moves the criterion}
  - **Candidate trace:**
    | Candidate | Evidence For | Evidence Against | Status |
    |-----------|--------------|------------------|--------|
    | {name}    | {observation} | {observation}   | {chosen / ruled out} |
```

Omit `Candidate trace` for non-investigation tasks.

**Metadata split:** What/Where/Reuses live in design.md Component Design and Patterns & Reuse.
Do not duplicate them per task -- tasks own Tests, Gate, Done when, Satisfaction sketch,
and (when applicable) Candidate trace only.

### Step 6: Create Execution Plan

**Large/Complex only.** At Medium the flat step list has no branching to show —
skip the diagram.

Before writing tasks, create an ASCII diagram showing the execution flow:
- Sequential dependencies as arrows (`→`)
- Parallel tasks as branches (`├→`, `└→`)
- Convergence points where branches merge

This gives an overview of parallelism and critical path before the detailed
breakdown. The diagram also serves as the implement subagent's ordering
hint -- it reads the diagram alongside tasks.md to decide internal
execution order. Main agent does not consume the diagram for fan-out.

### Step 7: Generate tasks.md

Use the template (at the bottom of this reference) as the canonical
structure — it wins over any existing breakdown. Do not read sibling
specs in `.artifacts/specs/` or anything in `.artifacts/archive/`; the
only cross-feature input is `.artifacts/knowledge.md`.

Generate tasks following the template structure:
- Summary (total count)
- Execution Plan (ASCII diagram of task flow)
- Quality Gates (lint, typecheck, test commands)
- Tasks grouped by commit boundary (T-1 [P] for parallel, T-2 [B:T-1] for dependent), each with "Done when"
- Requirements Coverage (mapping ACs to tasks)

After generating tasks.md, update spec.md: for each AC mapped to a task in Requirements Coverage,
change its status tag from `` `in-design` `` to `` `in-tasks` ``. For Medium scope (no design phase),
change from `` `pending` `` directly to `` `in-tasks` ``.

### Step 8: Pre-Approval Checks

Run all four checks before writing tasks.md. Display the result of each check explicitly —
`[pass]` or `[fail]` per item. Fix all `[fail]` items before writing. Do not run
these checks silently. Exception: the Commit-Boundary Viability Check (last) is
reasoned about internally and not echoed into the artifact — the artifact stays
focused on tasks, not process logs.

#### Story Order and ID Monotonicity Check

Verify the document order enforces the commit-boundary contract.

- `[pass|fail]` User stories appear in spec.md order (US-1 first, then US-2, ...)
- `[pass|fail]` Task IDs are monotonic top-to-bottom (first listed task = T-1)
- `[pass|fail]` Each user story's tasks are contiguous -- no user story is split across non-adjacent sections
- `[pass|fail]` No forward dependencies -- no task blocks on a task with a higher ID
- `[pass|fail]` Shared setup (test infra, types) lives inside the first user story that needs it, not in a separate "Phase 0"

If any fail: re-emit user stories in spec.md order, reassign IDs top-to-bottom, and move or rewrite any forward-dependent task.

#### Diagram-Definition Cross-Check

Verify the execution diagram arrows match every task's dependency markers.
These are written independently and can drift.

For each task, confirm:
- Every `[B:T-X]` marker has a corresponding arrow in the diagram
- Every arrow in the diagram has a corresponding `[B:T-X]` in the target task
- Tasks shown as parallel `[P]` do not depend on each other

If any mismatch: fix the diagram or the marker, not both arbitrarily.

#### Satisfaction Sketch Check

Every task must carry a Satisfaction sketch, and every sketch must reference only mechanisms that exist within its own scope or in earlier tasks.

- `[pass|fail]` Every task has a non-empty Satisfaction sketch
- `[pass|fail]` Each Satisfaction sketch cites a mechanism present in the task's own scope or in an earlier task -- never a future task
- `[pass|fail]` No Done when relies on a mechanism that no task implements

If any fail: relax the Done when, add the missing task, or rewrite the sketch against an existing mechanism.

#### Test Co-location Check

Only applies when a test script was detected in Step 3. Skip entirely if no test infrastructure.

For each task that creates or modifies a code layer:
- Tests for that layer must be included in the same task
- "Tested in T-X" or "tests added later" is a violation -- merge the tests into the task

If any task defers its tests: merge them in before proceeding.

#### Commit-Boundary Viability Check (implicit)

Reason about this silently. Do not print `[pass]` lines for this check into
tasks.md -- the artifact should not contain a compile/test log per prefix.

For each user story prefix (US-1, then US-1+US-2, then US-1+US-2+US-3, ...), the
codebase state after applying those tasks in order must stand alone:

- Compiles, lint and typecheck pass, tests (if present) pass
- No unresolved reference to a primitive owned by a later user story
- No task in an earlier user story silently depends on a symbol, function, or
  module that a later user story defines

If an intermediate state would fail, the problem is a hidden forward
dependency the `[B:T-X]` markers did not surface. Resolve it before writing
the artifact -- pick one:

- Restructure: have the earlier user story ship an inline implementation that the
  later user story refactors into a shared primitive, and add a `[B:T-X]`
  refactor marker
- Reorder user stories in spec.md so the primitive is owned by an earlier user story
  (keep IDs monotonic after the reorder)
- Escalate to design.md: relocate component ownership and update the
  Requirements Traceability table, then regenerate tasks.md against the new
  design

Do not ship a tasks.md whose commits do not stand alone. "Compiles only at
the end" is not an acceptable execution plan.

### Step 9: Approval Gate

Present a summary and wait for approval:

```text
Tasks ready: `.artifacts/specs/{date}-{name}/tasks.md`
Tasks: {count} | Components: {list}

Approve to proceed, or describe changes.
```

- If changes: update tasks.md, re-run pre-approval checks, re-present gate.
- If approved: run `implement`.

Do not suggest `implement` until approved.

## Task Size Guidelines

| Size | Description | Example |
|------|-------------|---------|
| Small | Mechanical change, no decisions | "Add type export" |
| Medium | Bounded logic, single concern, reapplies a known pattern | "Create API endpoint" |
| Large | Multiple concerns or a load-bearing decision inside the task | "Implement auth flow" - split into smaller tasks |

Prefer Small and Medium tasks. If a task carries more than one decision
or spans multiple concerns, split it — file count is incidental.

## Dependency Markers

| Marker | Meaning |
|--------|---------|
| [P] | Parallel-safe, no dependencies |
| [B:T-1] | Blocked by T-1 |
| [B:T-1,T-2] | Blocked by multiple |

## Guidelines

**DO:**
- Keep tasks atomic -- single, clear action per task
- Respect dependencies -- same component = sequential
- Mark independent tasks as [P] to enable parallelization
- Group by commit boundary -- each group forms one atomic commit
- Cover all ACs -- every AC-N has at least one task
- Run quality gates after each task, not as separate tasks
- Pair every Done when with a Satisfaction sketch citing a mechanism present in this task or earlier
- Enumerate every candidate from the spec with evidence for and against in `Candidate trace` before choosing a mitigation in an investigation task

**DON'T:**
- Add Files:/Reference:/Commit: metadata lines in task descriptions
- Create tasks that span multiple unrelated concerns
- Leave AC-N requirements without corresponding tasks
- Bundle quality gates as tasks in the breakdown
- Defer tests to a later task when test infrastructure exists (contrasts: include tests in the task that creates the code)
- Present tasks before running the pre-approval checks (contrasts: run checks first, restructure if needed)
- Ship a Done when whose mechanism does not exist in the task's own scope or earlier (contrasts: every Satisfaction sketch cites a mechanism present in this task or earlier)
- Choose a mitigation in an investigation task before evaluating every candidate from the spec (contrasts: enumerate every candidate with evidence in `Candidate trace`, then choose)

## Commit Boundary Grouping

Each user story group (`### US-N`) is one atomic commit boundary -- the default
unit a commit closes. A user story's tasks must leave the codebase in a stable,
committable state once all of them are done:
- **Self-contained**: the codebase compiles and works after the story is done
- **Logically cohesive**: every task in the story serves that story's purpose
- **Minimal but complete**: no half-implemented feature left behind

Finer-than-story commits (one per task) are an implement-time choice, requested
in the implement prompt -- not declared here. tasks.md groups by user story only.

### Dependencies

Never create a dedicated "install all dependencies" task. Each dependency is installed in the task that first needs it, as part of its implementation. This keeps each user story self-contained with only the deps it actually uses.

Example:
```markdown
### US-1 [P1] Authentication

- [ ] T-1 [P] Create auth types in types/auth.ts
- [ ] T-2 [B:T-1] Implement AuthService in services/auth.ts
- [ ] T-3 [B:T-2] Add auth middleware in middleware.ts
- [ ] T-4 [B:T-3] Protect routes with auth middleware
```

After completing the user story's tasks, the code is in a stable, committable state.

## Tasks Template

ALWAYS use this exact template structure:

````markdown
---
name: {{name}}
status: draft
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
sources: []
---

# Tasks: {{Feature}}

## Summary

Total: {{count}} | Completed: 0 | Remaining: {{count}}

## Execution Plan

```text
T-1 → T-2 → T-3
                 ├→ T-4 --┐
                 └→ T-5 --┼→ T-7
                 T-6 -------┘
```

## Quality Gates

Run after each task or batch:

- {{lint command}}
- {{typecheck command}}
- {{test command}}

## Tasks

### US-1 [P1] {{User Story Title}}

- [ ] T-1 [P] {{verb}} {{what}}
  - **Tests:** {{unit|integration|e2e|none}}
  - **Gate:** {{quick|full|build}}
  - **Done when:** {{verifiable outcome}}; gate passes, no tests deleted
  - **Satisfaction sketch:** {{one line: why this implementation actually moves the criterion}}

- [ ] T-2 [B:T-1] {{dependent task}}
  - **Tests:** {{unit|integration|e2e|none}}
  - **Gate:** {{quick|full|build}}
  - **Done when:** {{verifiable outcome}}; gate passes, no tests deleted
  - **Satisfaction sketch:** {{one line: why this implementation actually moves the criterion}}

### US-2 [P2] {{User Story Title}}

- [ ] T-3 [B:T-2] {{verb}} {{what}}
  - **Tests:** {{unit|integration|e2e|none}}
  - **Gate:** {{quick|full|build}}
  - **Done when:** {{verifiable outcome}}; gate passes, no tests deleted
  - **Satisfaction sketch:** {{one line: why this implementation actually moves the criterion}}
  - **Candidate trace:** (investigation tasks only — omit otherwise)
    | Candidate | Evidence For | Evidence Against | Status |
    |-----------|--------------|------------------|--------|
    | {{name}} | {{observation}} | {{observation}} | {{chosen / ruled out}} |

## Requirements Coverage

| User Story | Tasks    |
|------------|----------|
| US-1       | T-1, T-2 |
| US-2       | T-3      |

| Requirement | Tasks      |
| ----------- | ---------- |
| AC-1        | T-1, T-2   |
````

## Error Handling

- Design not found: Suggest `design`
- No clear components: Ask for clarification
