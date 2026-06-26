---
name: spec-executor
description: "Execution companion for spec-workflow: state navigation, task tracking via tasks.md, incremental delivery, and session recovery. Use after spec-workflow produces the plan."
source: claude-code-skill
created: 2025-04-30
---

# Spec Executor

Execution workflow centered on **state navigation** and **state assurance**. At any moment, know where you are, what comes next, and how to recover if interrupted.

---

## ⚠️ Dependency Notice

**This skill CANNOT be used standalone.** It depends on `spec-workflow` to produce the plan and `tasks.md` tracker before execution begins.

| Skill | Phase | Responsibility |
|-------|-------|---------------|
| `spec-workflow` | **Planning** | Requirements → Design → Task breakdown |
| `spec-executor` | **Execution** | State navigation → Task execution → State recovery |

**Handoff example:**

```
spec-workflow output:
  docs/login-feature/tasks.md
  docs/login-feature/requirements.md
  docs/login-feature/design.md

spec-executor input:
  Read docs/login-feature/tasks.md
  Execute tasks in order
  Update tasks.md after each task
```

Do NOT use this skill for work that has not been planned by `spec-workflow`.

**Validation:** Before executing, confirm `tasks.md` exists and contains valid task entries (Scope + Verification fields). If the file is missing or malformed, stop and ask the user.

---

## Quick Start

First time using this skill with a confirmed `tasks.md`:

```
1. Read tasks.md → find first [ ] task
2. Mark it [~] → execute per Scope description
3. When done: mark [✓], fill Verification, stage changes
4. Show diff → wait for user review and explicit commit approval
5. User says "next" → repeat from step 1
```

**Session compressed?** Jump to [Session Recovery](#session-recovery-after-interruption).

---

## State Navigation

### Where Am I?

```
Received user instruction
│
├─ Is the scope clear and small? ──→ YES → Execute directly (Simple Task)
│                                    NO
├─ Does it need design/architecture? → YES → Plan first → Write tasks.md → Execute
│                                    NO (unclear)
└─ Investigate → Reclassify
```

| Current State | What To Do Next | Key Output |
|---------------|-----------------|------------|
| Just received instruction | Classify task (simple / complex / exploratory) | Decision: plan or execute directly |
| Planning in progress | Write design doc + tasks.md → wait for user confirmation | Confirmed `tasks.md` |
| Ready to implement | Read `tasks.md`, mark first pending task as `[~]` | Task in progress |
| Just finished a task | Update `tasks.md` to `[✓]` → verify → commit → next task | Updated tracker |
| Hit an error | Stop → diagnose → fix → re-verify → resume | Documented fix |
| Session interrupted | Read `tasks.md` → verify last done task → resume first pending | Recovered context |
| User inserts unrelated query | Handle query → return to previous state without losing position | Continuity preserved |

### State Transition Rules

```
[Classified] --(simple)--> [Executing] --(task done)--> [Update tracker] --(more tasks)--> [Executing]
      │                              │                                    └─(all done)--> [Complete]
      └─(complex)--> [Planning] --(confirmed)--> [Executing]
                             └─(rejected)--> [Revise plan]

[Executing] --(error)--> [Diagnosing] --(fixed)--> [Update tracker] --> [Executing]
                                    └─(stuck)--> [Ask user]

[Any state] --(unrelated user query)--> [Handle query] --> [Return to prior state]
```

**Critical rule:** You cannot transition from `[Executing]` to the next task without updating the tracker. Updating `tasks.md` is the **definition** of task completion.

---

## Task Classification

Before writing code, classify the task:

| Type | Criteria | Planning Required |
|------|----------|-----------------|
| **Complex** | New feature, architecture change, multi-file refactor, API design | Yes — use `spec-workflow` to produce design doc + tasks.md |
| **Simple** | Single-file change, config tweak, clear bug fix with known scope | No — brief explanation, then implement |
| **Exploratory** | Unclear scope, needs investigation to understand the problem | Investigate first, then reclassify |

**Boundary rule:** If a "simple" task grows to need design decisions, interface changes, or cross-file coordination, **stop immediately** and upgrade to "complex" with planning.

### Task Type Reference

| User Intent | Type | Action |
|-------------|------|--------|
| New feature, architecture change, large refactor | Complex | Trigger `spec-workflow` for full planning |
| Bug fix with ticket/reference, interface alignment | Fix / Complex | Trigger `spec-workflow`, Phase 1-2 may be simplified |
| Single-file change, config tweak, clear small fix | Simple | Brief explanation, then implement directly |
| Explain code, check logs, `updatecode`, info query | Routine | Execute directly, no Spec |

**Session split rule:** If `tasks.md` has > 8 pending tasks or estimated work > 2 hours, suggest `/clean` and continue in a new session.

### Must Ask the User

Stop and ask before proceeding when:

| Situation | Question to Ask |
|-----------|-----------------|
| Unclear requirement background | "What problem should this code solve?" |
| Design conflict (A vs B) | "Both approaches have tradeoffs — what's your priority?" |
| Deleting code | "This code appears used in X — are you sure you want to delete it?" |
| Deleting code — verification | Run `grep -r "ClassName" --include="*.java" --include="*.xml"` to confirm no downstream references before deleting |
| Scope expands beyond original | "This seems broader than the original request — should we expand the design?" |
| Better approach found | "I see a better refactoring path — can you explain the original design intent?" |
| Uncommitted user changes exist | "I see you have uncommitted changes — should I work from the latest code?" |

---

## State Assurance

### The Tracker (`tasks.md`)

`tasks.md` is the primary state reference. If memory, conversation, and tracker disagree, **pause and reconcile with the user** — never silently override user intent.

**Location:** `docs/{feature-name}/tasks.md` (or project-defined location).

**Format:**

```markdown
- [ ] Task name (≤10 words)
  - Scope: files and specific methods/fields changed
  - Affected: files that need sync changes due to this task
  - Verification: how to verify (compile, test, grep, etc.)
  - Commit: the actual commit message used
  - User corrections: 0 | Compression recoveries: 0
  - Notes: dependencies, blockers, scope changes
```

**Critical field — Scope:** Must be precise down to method/field level. After session compression, recovery depends entirely on this field to reconstruct what was done and what remains.

**Example:**

```markdown
# Implementation Plan

- [✓] 1. Add user authentication endpoint
  - Scope: `AuthController.java` add `login()` method; `AuthService.java` add `authenticate()`
  - Affected: `UserRepository.java` (add `findByUsername`)
  - Verification: `./gradlew :api:compileJava` passes
  - Commit: `feat(auth): add login endpoint`
  - User corrections: 0 | Compression recoveries: 0
  - Notes: depends on task 0 (DB schema)

- [~] 2. Add JWT token generation
  - Scope: `JwtUtil.java` add `generateToken()`; `AuthService.java` inject JwtUtil
  - Affected: `application.yml` (add jwt.secret)
  - Verification: —
  - Commit: —
  - User corrections: 0 | Compression recoveries: 0
  - Notes: —

- [ ] 3. Add auth middleware
  - Scope: ...
```

**Status values:**
- `[ ]` — Not started
- `[~]` — In progress (set this **before** editing code)
- `[✓]` — Done (set this **before** committing or starting next task)
- `[⏭]` — Skipped

**Correction tracking:**
- **User corrections ≥ 2:** Escalate — record the pattern in Notes and adjust approach
- **Compression recoveries ≥ 6:** Suggest user `/clean` and start fresh

### Real-Time Update Discipline

| Event | Action | Why |
|-------|--------|-----|
| Start a task | Change `[ ]` → `[~]` | Prevents duplicate work |
| Finish a task | Change `[~]` → `[✓]`, fill Verification + Commit | Defines completion |
| User changes scope | Add note, increment User corrections | Prevents drift |
| Session compresses | Mark `[~]` → `[ ]` if uncertain | Prevents false progress |

**This takes precedence over compilation, testing, and starting the next task.** A task whose tracker entry is not updated is considered NOT done.

#### Timeliness Guarantee

`tasks.md` must be updated in real time — never retroactively:
- After completing a task → update status, verification, and commit message **immediately**
- After starting a task → change `[ ]` to `[~]` **before** editing code
- After session compression → mark `[~]` → `[ ]` if uncertain about state
- After user adds/changes scope → record in Notes **immediately**
- **Never** reconstruct progress after compression without re-verifying code state first

### Compression Recovery

`tasks.md` is the operational basis for recovery:

| Step | How to use `tasks.md` |
|------|----------------------|
| Read and confirm progress | Scan statuses in order; identify boundary between `[✓]` and `[ ]` |
| Verify code state | **Only verify the last `[✓]` row** (state boundary). Re-run its verification method. If it fails, state is stale — pause and reconcile |
| Determine next step | Find first `[ ]` or `[~]` row; execute from its Scope description |

### Session Recovery (After Interruption)

When context is compressed and the session continues:

1. **Report count** — state "This session has recovered from compression N times"
2. **Read `tasks.md`** — scan statuses, identify the boundary between `[✓]` and `[ ]`
3. **Validate tracker** — verify `tasks.md` structure is intact (expected fields, no corruption). If malformed, ask user before proceeding.
4. **Verify boundary** — re-run the verification for the last `[✓]` task. If it fails, the state is stale; pause and reconcile.
5. **Resume** — mark the first `[ ]` task as `[~]` and continue from its Scope description.
6. **Count recoveries** — increment Compression recoveries. If ≥ 6, stop execution, update tasks.md to `[~]`, and wait for user `/clean`

### Context Switching

| Scenario | Rule |
|----------|------|
| User asks unrelated question | Handle it, do NOT modify tracker, return to prior task afterward |
| User starts a new feature | Pause current task (mark `[~]`), create new tracker for new work |
| User changes direction mid-task | Treat as error response: stop, document in Notes, wait for confirmation |
| User corrects design assumption | Not a context switch — follow Error Response Protocol. Update `tasks.md` Notes and `design.md` if assumptions changed |

**Key principle:** One `tasks.md` per feature. Different features must have different tracker files.

---

## Execution Rules

### Incremental Delivery

- Implement **one small task at a time**
- Max ~300 lines changed per task
- Stop for review after each task unless user explicitly authorizes continuous mode
- Update `tasks.md` status **immediately** after each task — before committing or starting the next

#### Task Size Exemptions

| Scenario | Relaxed Limit | Required Condition |
|----------|--------------|-------------------|
| User authorizes continuous mode | ≤ 500 lines | User explicitly says "continuous implement" or "finish the rest" |
| Pure deletion | No limit | Only removing code, no new logic, verified no downstream references |
| Batch rename/migration | ≤ 500 lines | Mechanical replacement (e.g., package rename), zero logic change |
| Config/constant extraction | ≤ 400 lines | Extracting scattered magic values to unified constants, no behavior change |

**If exceeding limit:** Must split into smaller tasks or explain split plan to user and get approval.

### Continuous Mode Authorization

Only proceed without stopping for review when user explicitly says:
- "You can continuous implement"
- "Finish the rest without asking"
- "Batch execute the remaining tasks"

**NOT authorization:** "OK", "Continue", "Go ahead", "Sure" — these confirm the current task only. **Must ask:** "Do you mean I can continuously implement remaining tasks, or just confirming this one?"

When in continuous mode:
- Each task must still be independently verified (compile/type-check)
- Each task must still be independently committed
- `tasks.md` must be updated before starting the next task
- User can interrupt at any time — stop immediately when they do

### Risk Prediction (Before Starting Each Task)

Spend 30 seconds on pre-flight risk analysis:

1. **Match task type** — What category is this? (API alignment / dependency injection / method refactor / DTO addition / deletion)
2. **Extract lessons** — What has gone wrong with this type of task before?
3. **Pre-verify** — Run the recommended verification before writing code:
   - **API alignment:** Extract signatures with language-specific tools, diff against interface
   - **Deletion:** `grep -r "targetName"` to confirm no downstream references
   - **Method refactor:** `grep -r "oldMethodName"` to find all call sites
   - **Dependency change:** Verify all injection points and mock references
   - **DTO addition:** Check serialization paths and downstream consumers
   - **Mock update:** Verify test files reference the correct type (interface vs concrete)
   - **Package rename:** `grep -r "old.package.name"` to find all imports

### Review Rules

**Default:** Stop and wait for user review after every task.

**Review exemptions** (no need to stop, but still run quality gates):

| Scenario | Condition |
|----------|-----------|
| User authorized continuous mode | Explicit continuous implement statement |
| Pure formatting | Only whitespace, line breaks, import sorting — zero logic change |
| Pure test data adjustment | Only test inputs or expected values — no production code touched |
| Emergency hotfix | User explicitly says "urgent fix" and change is ≤ 10 lines |

### Code Quality Gates

Before marking any task `[✓]`:

- [ ] **Compiles** — no build/type errors. Prefer quiet single-module compilation.
  - Build tool available: run `./gradlew :module:compileJava --quiet` or equivalent
  - Build tool **unavailable**: use `javap -public` to extract signatures, or `grep`/`diff` to verify definitions align
- [ ] **No dead code** — unused imports, helpers, or fields removed
- [ ] **No magic values** — hardcoded literals (appearing 2+ times) extracted to named constants
- [ ] **Size limits** — methods ≤ 30 lines, nesting ≤ 2 levels, files ≤ 500 lines
- [ ] **Naming** — booleans use `is`/`has`/`should` prefixes, names are self-explanatory
- [ ] **Task status updated** — `tasks.md` reflects current state with verification and commit message

### Pre-Commit Checklist

Before every commit:

- [ ] Change scope matches the task (or fits within an exemption)
- [ ] All quality gates passed
- [ ] No secrets or credentials in diff
- [ ] Diff reviewed — user has seen the changes and approved
- [ ] Commit message provided and follows project convention
- [ ] `tasks.md` updated with status, commit message, and verification
- [ ] **Self-check:** Did I follow the risk prediction? Did I avoid patterns known to fail?

**Do not commit if self-check fails.**

---

## Error Response Protocol

When compilation fails, tests fail, tools error, or user points out a mistake:

1. **Stop** — no further edits until resolved
2. **Locate** — identify affected files and methods from error output
3. **Verify root cause** — use tools (grep, diff, compiler) to confirm. Never rely on reading alone.
4. **Fix** — apply minimal corrective change
5. **Document** — distinguish the nature of the fix:
   - **Code error:** Record cause and fix in `tasks.md` Notes
   - **User corrected design assumption:** Update `tasks.md` Notes **and** sync changes to `design.md`
6. **Re-verify** — run full quality gates and pre-commit checklist
7. **Resume** — only after explicit user confirmation

### Tool Verification Rules

- **Agent** is for exploration (reading code, gathering context) — **never** for precision verification
- **Bash** is for precision (grep, diff, compiler output, line counts) — always cross-check agent conclusions
- **Never** judge signature alignment, overload resolution, or parameter types by reading alone
- **Never** trust "looks correct" from an agent without independent verification

---

## Core Principles

- **State over speed** — document progress before moving on
- **Verify with tools** — grep, diff, compiler; never eyeball
- **Stop and ask** — when uncertain, pause for clarification
- **Tracker is truth** — if memory and tracker disagree, the tracker wins
- **Agent is not evidence** — agent conclusions require Bash cross-check
- **Plan before complex work** — multi-file or architectural changes need design first

