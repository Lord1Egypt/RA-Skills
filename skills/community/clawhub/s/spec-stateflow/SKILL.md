---
name: spec-stateflow
description: "Structured software engineering workflow with state-driven execution: requirement analysis → technical design → task planning → execution with state navigation and session recovery. Triggers: new feature, complex architecture, multi-module integration, database/UI design, or any task requiring structured planning and execution. Trigger words: new feature, architecture design, requirement implementation, spec workflow, state recovery, task tracking, 新功能, 复杂架构, 多模块, 需求实现, spec工作流, 状态恢复, 任务追踪"
alwaysApply: false
---

# Spec Stateflow

**Important: You must follow these rules. Each phase must be confirmed by the user before proceeding to the next phase.**

## When to Use This Skill

Use this skill for **structured development workflow** when you need to:

- Develop new features from scratch
- Design complex architecture
- Integrate multiple modules
- Ensure high-quality requirement analysis and acceptance criteria

**Do NOT use for:**
- Simple requirements
- Simple bug fixes (single file / single method / obvious root cause)
- Documentation updates
- Configuration changes

> **Fix vs Simple bug fix boundary**: A "Fix" task (use Spec) involves **cross-module impact**, **systematic tech debt**, or **requires design before coding**. A "Simple bug fix" (no Spec) is a **localized, obvious fix** in ≤1 file with no architectural implications.

## How to Use This Skill

1. **Follow the four phases in order** — each phase requires user confirmation before proceeding:
   - **Phase 1:** Write requirements using EARS syntax → `requirements.md`
   - **Phase 2:** Design technical solution (architecture, API, DB, etc.) → `design.md`
   - **Phase 3:** Break down tasks with field-level specifics → `tasks.md`
   - **Phase 4:** Execute tasks with state tracking, compression recovery, and context switching
2. **[HIGHEST PRIORITY]Real-time `tasks.md` updates** — After completing each small task, you MUST immediately update `{SPEC_PATH}/tasks.md`, before compilation, testing, or starting the next task. Not updated = not done. See Phase 4 State Assurance for details

**Testing:** This skill includes `test-prompts.json` with 10 test scenarios covering all phases and edge cases. Use them to validate skill behavior.

## Path Convention

All Spec files use the following placeholders. Actual paths are defined in the user's project configuration:

| Placeholder | Meaning |
|------------|---------|
| `{SPEC_DIR}` | Spec file root directory |
| `{SPEC_NAME}` | Current spec name |
| `{SPEC_PATH}` | Full path = `{SPEC_DIR}/{SPEC_NAME}` |

**Spec file list:**

| File | Description |
|------|-------------|
| `{SPEC_PATH}/requirements.md` | Requirements document (Phase 1 output) |
| `{SPEC_PATH}/design.md` | Technical design document (Phase 2 output) |
| `{SPEC_PATH}/tasks.md` | Task breakdown & progress tracker (Phase 3 output, **single source of truth**) |

## Entry Points

| Your situation | Start here |
|----------------|-----------|
| New feature / complex task | **Phase 1** (full workflow: Phase 1 → 2 → 3 → 4) |
| Ready to execute (user confirmed plan) | **Phase 4 → Quick Start** |
| User authorized continuous batch / driver-monitor automation | **Phase 4 → [Continuous Operation Mode](#continuous-operation-mode)** |
| Session compressed / interrupted | **Phase 4 → Compression Recovery** |
| User says "updatecode" / "continue" / "resume" | **Phase 4 → Quick Start** (read tasks.md → locate breakpoint → continue) |

> For all runtime states (error, context switch, task completion, etc.), see **Phase 4 → State Navigation**.

## Workflow Rules

1. When you determine that the user's input implies a new requirement (not explicitly stated), you may work independently following standard software engineering practices. Confirm with the user when necessary.

2. When the user explicitly states a new requirement, you must follow the full workflow: understand the problem and requirements clearly, and confirm with the user before proceeding to the next phase.

---

## Phase 1: Requirements Document and Acceptance Criteria Design

First complete the requirements design using EARS (Easy Approach to Requirements Syntax) method. You must confirm requirement details with the user. After final confirmation, the requirements are finalized, then proceed to the next phase.

Save to `{SPEC_PATH}/requirements.md`. After confirming with the user, proceed to the next phase.

**If user rejects or requests changes:** Update requirements.md and re-confirm. Do NOT proceed to Phase 2 until user explicitly approves.

**Reference format:**

```markdown
# Requirements Document

## Introduction

Requirement description

## Requirements

### Requirement 1 - Requirement Name

**User Story:** User story content

#### Acceptance Criteria

1. Use EARS syntax: While <optional precondition>, when <optional trigger>, the <system name> shall <system response>. For example: When "Mute" is selected, the laptop shall suppress all audio output.
2. ...
...
```

---

## Phase 2: Technical Solution Design

After completing the requirements design, based on the current technical architecture and the confirmed requirements above, design the technical solution. It should be concise but accurately describe the technical architecture (e.g., architecture, tech stack, technology selection, database/interface design, test strategy, security). Use mermaid diagrams when necessary.

**Must include chapters:** Background, Design Goals, Business Model, System Design (precise to package path, class name, method signature), Refactoring Design (if applicable), Deployment Plan (for large tasks), Risk Assessment (for large tasks).

Save to `{SPEC_PATH}/design.md`. You must confirm with the user clearly, then proceed to the next phase.

**If user rejects or requests changes:** Update design.md and re-confirm. Do NOT proceed to Phase 3 until user explicitly approves.

**Reference format:**

```markdown
# Technical Solution Design

## Background
Why this design is needed — business context and problem statement

## Design Goals
- Goal 1: ...
- Goal 2: ...

## Business Model
Core domain models, entity relationships, key data flows

## System Design
### Architecture Overview
(mermaid diagram or component description)

### Module: {module-name}
- **Package:** `com.example.module`
- **New classes:**
  - `ClassName` — responsibility description
  - `InterfaceName` — method signatures: `ReturnType methodName(ParamType param)`
- **Modified classes:**
  - `ExistingClass` — add method `newMethod()`, change field `field` scope

### API Design
| Endpoint | Method | Request | Response |
|----------|--------|---------|----------|
| `/api/xxx` | POST | `{field: type}` | `{field: type}` |

### Database Design
Table name, columns, indexes, migration steps

### Test Strategy
Unit test scope, integration test plan, verification methods

## Refactoring Design (if applicable)
What to refactor, why, and how to do it incrementally

## Deployment Plan (for large tasks)
Environments, rollout steps, rollback plan

## Risk Assessment (for large tasks)
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| ... | High/Med/Low | High/Med/Low | ... |
```

---

## Phase 3: Task Breakdown

After completing the technical solution design, based on the requirements document and technical solution, break down specific tasks. You must confirm with the user clearly, then save to `{SPEC_PATH}/tasks.md`. After confirming with the user, proceed to the next phase.

**If user rejects or requests changes:** Adjust task breakdown and re-confirm. Do NOT proceed to Phase 4 until user explicitly approves.

### Task Field Specification

Every task in `{SPEC_PATH}/tasks.md` must contain the following fields:

| Field | Specification | Example |
|-------|--------------|---------|
| **Task name** | Verb-object structure, ≤10 words | `Remove unused methods from IMultiAppInfo` |
| **Scope** | Files directly modified by this task | `IMultiAppInfoProxyInterface.java`, `MultiAppInfoProxy.java` |
| **Affected** | Files that need sync changes due to this task (imports, calls, etc.) | `NoticeService.java`, `BpmService.java` |
| **Specifics** | **Most critical field.** Precise down to method/field level | `Interface remove methodA(), methodB(); add methodC(String)` |
| **Status** | `[✓]` Done / `[ ]` Not started / `[~]` In progress or paused / `[⏭]` Skipped (user decision only; dependencies not auto-blocked, flag in final summary) | `[✓]` |
| **Verification** | How to verify (compile, test, grep, etc.) | `grep signatures + compile verification` |
| **Commit** | Backfill **after** git commit: actual commit message + short hash | `feat(proxy): remove unused methods (a1b2c3d)` |
| **User corrections** | Count of user corrections; ≥2 triggers escalation | `0` |
| **Notes** | Dependencies, blockers, scope changes | `Depends on task 1` |

**Critical field — Specifics:** Must be precise down to method/field level. After session compression, recovery depends entirely on this field to reconstruct what was done and what remains.

**Status values:**
- `[ ]` — Not started
- `[~]` — In progress
- `[✓]` — Done
- `[⏭]` — Skipped (only when user explicitly decides to skip; agent cannot self-skip; skipped tasks are excluded from execution — dependencies are not auto-blocked, but flag them in the final task summary)

### Task Format Reference

```markdown
# Implementation Plan

- [✓] 1. Remove unused methods from IMultiAppInfo
  - Scope: `IMultiAppInfoProxyInterface.java`, `MultiAppInfoProxy.java`
  - Affected: `NoticeService.java`
  - Specifics: Interface remove getCachedV2AppInfo(), listV1OfflineApps(); impl class sync
  - Verification: grep signatures + compile verification
  - Commit: feat(proxy): remove unused methods (a1b2c3d)
  - User corrections: 0
  - Notes: User requested keeping getV1AppInfo 3-param overload
  - _Requirement: R1

- [ ] 2. Add getAppName method
  - Scope: `IMultiAppInfoProxyInterface.java`, `MultiAppInfoProxy.java`
  - Affected: —
  - Specifics: Interface add getAppName(String); impl class add getAppName(String)
  - Verification: —
  - Commit: —
  - User corrections: —
  - Notes: Depends on task 1 completion
  - _Requirement: R2
```

---

## Phase 4: Task Execution

Execute tasks in order from `{SPEC_PATH}/tasks.md`. This phase covers execution mechanics, state navigation, and session recovery.

**Validation:** Before executing, confirm `{SPEC_PATH}/tasks.md` exists, contains valid task entries (Scope + Specifics + Verification fields), and **all tasks have valid status markers** (`[ ]` / `[~]` / `[✓]` / `[⏭]`). If the file is missing, malformed, or has tasks with missing/invalid status markers, stop and fix the format before proceeding.

### Quick Start

First time with a confirmed `tasks.md`:

```
0. Validate tasks.md format — ensure every task has a valid status marker [ ]/[~]/[✓]/[⏭]. Fix any missing/invalid markers before proceeding.
1. Read {SPEC_PATH}/tasks.md → if any [~] task exists, continue it; otherwise find first [ ] task
2. Mark it [~] → execute per Specifics description
3. When done: mark [✓], fill Verification, stage changes
4. Show diff → wait for user review and explicit commit approval (**skipped in [Continuous Operation Mode](#continuous-operation-mode)**)
5. If user approves: commit → backfill Commit field with actual message + short hash → next task. If user rejects: revert status to [~], address feedback, repeat from step 2
6. User says "next" → repeat from step 1
```

**Session compressed?** Jump to [Compression Recovery](#compression-recovery).
**Continuous batch authorized by the user (e.g. "you may continue implementing" / "complete the rest without asking"), or running under driver/monitor automation?** Jump to [Continuous Operation Mode](#continuous-operation-mode).

### State Navigation

#### Where Am I?

```
Received user instruction
│
├─ Is the scope clear and small? ──→ YES → Do NOT use this skill, execute directly
│                                    NO
├─ Does it need design/architecture? → YES → Plan first → Write tasks.md → Execute
│                                    NO (unclear)
└─ Investigate → Reclassify
```

| Current State | What To Do Next | Key Output |
|---------------|-----------------|------------|
| Just received instruction | Classify task (simple / complex / fix / routine) → see Entry Points for entry decisions | Decision: plan or execute directly |
| Planning in progress (Phase 1-3) | Continue current phase → wait for user confirmation before next phase | Confirmed spec doc |
| Ready to implement | Read `{SPEC_PATH}/tasks.md`, mark first pending task as `[~]` | Task in progress |
| Just finished a task | Update `tasks.md` to `[✓]` → verify → commit → next task | Updated tracker |
| Hit an error | Stop → diagnose → fix → re-verify → **wait for user confirmation** → judge next step based on user's direction | Documented fix |
| Session interrupted / compressed | Jump to [Compression Recovery](#compression-recovery) | Recovered context |
| User asks unrelated question | Handle query → return to previous state, do NOT modify tracker | Continuity preserved |
| User starts a new feature mid-task | Pause current (mark `[~]`) → create new tracker → see Context Switching | New `{SPEC_PATH}` |
| User changes direction mid-task | Stop → document in Notes → wait for confirmation | Updated tracker |
| User corrects design assumption | Update `tasks.md` Notes **and** `design.md` → wait for confirmation | Synced docs |
| All tasks done | Generate final summary → wait for user confirmation → complete | See Task Completion |

#### Task Completion

When all tasks in `tasks.md` are `[✓]` or `[⏭]`:

1. **Generate final summary** including:
   - Total tasks: done / skipped
   - Skipped tasks list (if any) — flag each with its original scope and reason for skip
   - User corrections total across all tasks
2. **Present summary to user** and wait for confirmation
3. After user confirms: the spec workflow is complete. Spec files (`requirements.md`, `design.md`, `tasks.md`) are retained as project documentation

#### State Transition Rules

The State Navigation table is the primary reference. The flow diagram below illustrates the core state machine; all scenarios in the table are authoritative.

```
[Classified] --(simple/routine)--> [Direct Execution] --> [Done]
      │
      └─(complex/fix)--> [Planning] --(confirmed)--> [Executing] --(task done)--> [Update tracker] --(more tasks)--> [Executing]
                             │                                                                    └─(all done)--> [Complete]
                             └─(rejected)--> [Revise plan]

[Executing] --(error)--> [Diagnosing] --(fixed)--> [Update tracker] --> [Executing]
                                    └─(stuck)--> [Ask user] --(user responds)--> [Judge next step based on user's direction]

[Complete] --(user confirms)--> [Done]

[Any state] --(unrelated user query)--> [Handle query] --> [Return to prior state]
[Any state] --(user changes direction)--> [Stop + document] --> [Wait for confirmation]
[Any state] --(user corrects design assumption)--> [Update tasks.md + design.md] --> [Wait for confirmation]
[Any state] --(session compressed/interrupted)--> [Recovery] --(tracker reconciled)--> [Resume prior state]
```

> **Scope note:** The diagram above covers only tasks that enter the Spec workflow (Complex / Fix). Simple and Routine tasks are executed directly without entering this state machine.

**Critical rule:** You cannot transition from `[Executing]` to the next task without updating the tracker. Updating `tasks.md` is the **definition** of task completion.

### Continuous Operation Mode

Skips per-task `show diff → wait approval`. Auto-advances to next `[ ]` task. All other tracker disciplines remain mandatory.

#### Activation

- User explicitly authorizes continuous batch (e.g. `you may continue implementing` / `complete the rest without asking`)
- Invoked by driver/monitor automation

Ambiguous confirmations (`OK` / `continue` / `okay`) **do NOT** activate. Authorization does **not** survive session compression.

#### Behavior Diff

| Discipline | Status |
|------------|--------|
| Mark `[~]` / `[✓]`, fill Verification + Commit | ✅ Kept |
| Run verification (compile / test / grep) | ✅ Kept |
| Per-task independent commit | ✅ Kept |
| Increment User corrections on rejection | ✅ Kept |
| Show diff → wait approval | ❌ Skipped |
| Wait for `next` between tasks | ❌ Auto-advance |

#### Auto-Pause Triggers

Reverts to Default Mode immediately on:

| Trigger | Action |
|---------|--------|
| Compilation / verification fails | Rollback to `[~]`, record in Notes |
| User corrections ≥ 2 | Escalate per project config |
| Scope expansion | Record drift, wait for confirmation |
| Risky ops (force push, reset --hard, schema migration, etc.) | Stop and ask |
| User interrupts | Stop after current task's commit |
| All tasks complete | Switch to Task Completion |
| Session compression recovery | Revert to Default, re-confirm |

### State Assurance

#### The Tracker (`tasks.md`)

`{SPEC_PATH}/tasks.md` is the primary state reference. If memory, conversation, and tracker disagree, **pause and reconcile with the user** — never silently override user intent.

Key reminders for execution:

- **Specifics is the most critical field** — must be precise down to method/field level; after session compression, recovery depends entirely on this field
- **Status values:** `[ ]` Not started / `[~]` In progress (set **before** editing code) / `[✓]` Done (set **before** committing) / `[⏭]` Skipped (user decision only)
- **User corrections:** ≥2 triggers escalation (user's project configuration defines the escalation behavior)

#### Timeliness Guarantee

`{SPEC_PATH}/tasks.md` must be updated in real time — never retroactively:

| Event | Action | Why |
|-------|--------|-----|
| Start a task | `[ ]` → `[~]` **before** editing code | Prevents duplicate work |
| Finish a task (before commit) | `[~]` → `[✓]`, fill Verification **immediately** | Defines completion |
| Finish a task (after commit) | Backfill Commit field with actual message + short hash | Traceability |
| User changes scope | Record in Notes **immediately**, increment User corrections | Prevents drift |
| Session compresses | `[~]` → `[ ]` if uncertain about state | Prevents false progress |

**Precedence:** This takes precedence over compilation, testing, and starting the next task. A task whose tracker entry is not updated is considered NOT done.

**Prohibited:**
- Never reconstruct progress after compression without re-verifying code state first
- Never write progress retroactively after compression — progress not written before compression is unreliable

### Compression Recovery

`{SPEC_PATH}/tasks.md` is the operational basis for recovery.

**Trigger:** System message "This session is being continued from a previous conversation" or when memory is fuzzy.

| Quick Step | Full Step Mapping |
|-----------|------------------|
| Read and confirm progress | Step 1 |
| Verify code state | Step 2-3 |
| Determine next step | Step 4-6 |

#### Full Compression Recovery Flow (6 Steps)

**Step 1: Read Spec files, confirm `{SPEC_PATH}/tasks.md` progress**
- Read `{SPEC_PATH}/requirements.md`, `{SPEC_PATH}/design.md`, `{SPEC_PATH}/tasks.md`
- `tasks.md` is the **only trustworthy state source** — summary progress descriptions are NOT reliable
- **Special cases:**
  - **If Spec files don't exist:**
    - If context indicates a Simple task (no requirement ID, no Spec): run `git status` and `git diff`, determine progress from working tree state, continue directly
    - Otherwise (Complex/Fix): Spec planning hasn't started. Re-run "Where Am I?" classification
  - **If files exist but `tasks.md` is missing:** Rebuild `tasks.md` from `design.md`, note in remarks "table rebuilt after compression recovery"
  - **If all files exist:** Proceed to Step 2

**Step 2: Verify actual code state**
- Run `git status` and `git diff` to confirm working tree state
- **If no `[✓]` rows in `tasks.md`** (no tasks completed yet): first `[ ]` or `[~]` row is the next task, skip the rest of this step and all of Step 3 → go to Step 4
- **If `[✓]` rows exist:** **Only verify the last `[✓]` row** (state boundary), re-execute verification per "Scope + Specifics + Verification" fields
- If verification passes → trust all prior `[✓]`; if fails → change that task status to `[ ]`, consider backtracking
- If `tasks.md` doesn't match actual state, **fix `tasks.md` first, then continue**

**Step 3: Do not trust summary "completed" conclusions**
- Summary claims of "completed", "aligned", "fixed" — only verify the **last completed task**
- Especially for precision-critical conclusions (interface/impl alignment, method signature matching, compile status)
- If verification fails, revert that task to `[ ]`, consider backtracking

**Step 4: Re-confirm next task**
- Explicitly state the next task name and scope
- Do not continue based on vague summary descriptions (e.g., "continue fixing remaining interfaces")

**Step 5: Use programmatic verification, not manual reading**
- For "does it exist", "is it aligned", "does it match" — prefer Bash tools (grep, javap, diff) for programmatic verification
- Never judge interface/impl alignment, method existence, or parameter matching by reading alone

**Step 6: Update `tasks.md` before executing**
- Before making any code changes, update `{SPEC_PATH}/tasks.md` first
- Ensure `tasks.md` is consistent with actual state

### Context Switching

| Scenario | Rule |
|----------|------|
| User starts a new feature | Pause current task (mark `[~]`), create new tracker for new work |
| User raises multiple parallel requests | Confirm priority and order with user; create separate Spec directories (different `{SPEC_NAME}`) for each; execute sequentially, never mix tasks.md |

**Key principle:** One `tasks.md` per requirement. Different requirements must have different `{SPEC_PATH}`.

**Do not abandon unfinished tasks.** Unless user explicitly says "cancel" or "skip", mark unfinished tasks as `[~]` and record progress.

**When returning to a previous task, re-verify state.** Verify the last `[✓]` row per Step 2 of Compression Recovery.

---

## Key Principles

1. **[HIGHEST PRIORITY]Real-Time Task Tracking** — Updating `{SPEC_PATH}/tasks.md` is the definition of task completion; it takes precedence over all other operations
2. **User Confirmation Required** — Each phase must be confirmed by the user before proceeding to the next
3. **Tracker is truth** — When memory conflicts with tracker, trust the tracker; pause and reconcile with the user on conflicts
4. **Verify with tools** — Prefer programmatic verification (grep, diff, compiler); never rely on reading or memory for precision questions
5. **Cross-check conclusions** — Any conclusion from indirect observation must be independently verified
