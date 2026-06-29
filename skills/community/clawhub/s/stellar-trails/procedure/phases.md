# Phase State Machine

Each phase produces a concrete artifact that the next phase consumes. Skipping a phase means the next phase has no input to work from, which makes the gap visible and correctable.

## State Diagram

```
IDLE → SPECIFY → PLAN → IMPLEMENT → VERIFY → DELIVER
  ↑                                        │
  └──── Recovery ◄───────────────────┘
```

On error: stop, assess (code bug or approach failure?), fix or pivot, return to VERIFY.

---

## Gate Protocol

Phase transitions are guarded. A phase cannot begin until its entry condition is met. This prevents incomplete output from leaking into the next phase and compounding errors.

| Gate | Condition | Action if not met |
|------|-----------|-------------------|
| SPECIFY → PLAN | All problem-spec fields filled, SADC complete | Complete missing fields before proceeding |
| PLAN → IMPLEMENT | Implementation plan complete + Scope output (Standard/Complex) | Present plan to user first |
| IMPLEMENT → VERIFY | Self-review checklist pass, all IMPL steps done | Fix issues before transitioning |
| VERIFY → DELIVER | All verification items PASS | Return to IMPLEMENT (or SPECIFY if spec gap) |

**Simple tier**: Gates run internally — the agent validates conditions but doesn't produce formal gate output.
**Standard/Complex tier**: PLAN → IMPLEMENT gate produces a Scope (see SKILL.md). The delivery report's Scope Drift field tracks any deviation from this commitment.

---

## Phase 1: IDLE

**Purpose**: Receive the user's request, classify complexity and task type.

**Actions**:
1. Receive and acknowledge the request.
2. **Session continuity check** — determine if this is a NEW task or a CONTINUATION of previous work. Check sources in this order:

   a. **Worklog** (`/home/z/my-project/worklog.md`) — read the last `---` delimited block. If the task description matches the current request, resume from `last_phase`. This is the primary continuity source after context truncation.
   b. **Preceding assistant message** — if the user's reply references, approves, corrects, or follows up on recent output, it is a continuation.

   | Continuation signal | Action |
   |---------------------|--------|
   | User references previous output ("apply all 10", "fix point 3", "proceed") | Skip SPECIFY+PLAN, go to IMPLEMENT |
   | User approves a proposal/plan ("yes", "go ahead", "do it") | Skip SPECIFY+PLAN, go to IMPLEMENT |
   | User asks a follow-up question ("what about X?") | Skip SPECIFY, answer in current phase context |
   | User provides new requirements mid-task | Restart from SPECIFY |
   | Context compression boundary with ongoing task | **Read worklog.md, resume from last recorded phase** |
   | Completely new topic, explicit new instructions, or `Skill()` invoked | Full workflow (continue below) |

   **Critical**: If continuation is detected, DO NOT re-derive proposals, plans, or specifications the user has already seen. Use the previous output (or worklog snapshot) as the plan. Regenerating from scratch is a correctness bug.

3. Classify complexity:
   - **Minimal**: Knowledge question, explanation, or recommendation — no code or file output.
   - **Simple**: Single file, no schema change, no new dependencies.
   - **Standard**: Multiple files or a schema change.
   - **Complex**: Architectural changes, multi-service, or high risk.
4. Classify task type (see [Task Type Awareness](#task-type-adaptation) below):
   - **Coding**: Web dev, bug fix, refactor, new feature.
   - **Document**: Report, proposal, DOCX, PDF, XLSX, PPT.
   - **Visualization**: Charts, diagrams, mind maps, dashboards.
   - **Data Processing**: ETL, analysis, transform, Python scripts.
   - **Non-Coding**: Questions, explanations, recommendations — no code or file output.
5. Check `memory/MEMORY.md` for user preferences, patterns, and key decisions. If the `memory/` directory does not exist, it will be created on first DELIVER — skip this step. For tasks requiring session continuity, also check the most recent dated file in `memory/`. See `memory-template.md` for memory system architecture, templates, and storage rules. **Note**: For context-truncation recovery, the worklog (step 2a above) takes priority over memory files — it captures immediate task state, while memory captures long-term patterns.
6. If the task involves a git repository and the session was continued from a previous conversation (context compression boundary), flag the repository as "state-uncertain" and require Source State Verification in SPECIFY.
7. Transition to SPECIFY (or IMPLEMENT/VERIFY if continuation detected).

**Artifacts**: None. IDLE is a routing phase.

**Memory reminder**: At every subsequent phase transition, check `memory/MEMORY.md` for relevant patterns before proceeding. This one-line check at each transition ensures continuity even if the IDLE phase was abbreviated or skipped.

## Task Type Adaptation

The workflow is task-type-aware. The core loop (SPECIFY → PLAN → IMPLEMENT → VERIFY → DELIVER) is always the same — all phases always run. What changes is what each phase produces and how much ceremony surrounds it:

| Phase | Coding | Document | Visualization | Data Processing | Non-Coding |
|-------|--------|----------|---------------|-----------------|------------|
| **SPECIFY** | Problem spec, edge cases, affected files | Content outline, target format, sections | Visual requirements, data sources, layout | Data spec, input/output schema, transforms | Internal — identify the question |
| **PLAN** | Code steps + Traceability IDs | Section plan + content depth targets | Data mapping + chart type selection | Transform pipeline + validation steps | Internal — plan the approach |
| **IMPLEMENT** | Write code | Generate document (via skill) | Generate chart (via skill) | Write script + execute | Answer / explain / recommend |
| **VERIFY** | Lint, type check, tests | Format check, content completeness | Visual accuracy, data integrity | Output validation, edge cases | Internal — self-check accuracy |

No phases are ever skipped. Non-coding tasks are classified as **Minimal** tier — SPECIFY, PLAN, and VERIFY run internally (the agent thinks through them without producing formal artifacts). Only IMPLEMENT generates visible output. See Complexity Tiers below.

Traceability IDs (IMPL-001, IMPL-002, ...) apply to Simple, Standard, and Complex tiers. Minimal tier does not use Traceability IDs.

---

## Complexity Tiers & Report Format

The workflow always runs — every task passes through all six phases. What changes between tiers is the verbosity of artifacts, not the rigor of thinking. No phase is ever skipped; the lowest tier runs phases internally.

### Minimal (internal phases)

Criteria: knowledge question, explanation, or recommendation — no code or file output.

| Phase | Behavior |
|-------|----------|
| SPECIFY | Internal — identify the question or topic. No template output. |
| PLAN | Internal — think about how to answer. No template output. |
| IMPLEMENT | Produce the answer, explanation, or recommendation. |
| VERIFY | Internal — self-check accuracy and completeness. No template output. |
| DELIVER | Output minimal report (see below). Skip session digest to memory. |

Minimal report format (use this instead of the full block):

```
☄️ PASS | Evidence: <one-line result>
```

### Simple (compact report)

Criteria: single file, no schema change, no new dependencies, obvious approach.

| Phase | Behavior |
|-------|----------|
| SPECIFY | Quick source check (SADC), then restate goal in 1-2 sentences. Do NOT output the problem-spec template. |
| PLAN | List steps as bullet points. Do NOT output the implementation-plan template. Traceability IDs optional. |
| IMPLEMENT | Write code. No inline Traceability ID comments required. |
| VERIFY | Run automated checks (lint, type check). Do NOT output the verification-report template. |
| DELIVER | Output compact report (see below). Still write session digest to `memory/YYYY-MM-DD.md`. |

Compact report format (use this instead of the full block):

```
☄️ REPORT [Simple]
SPECIFY→DELIVER : PASS | Evidence: <one-line result> | Defects: 0 | Drift: NONE
```

### Standard (full report + Scope)

Criteria: multiple files or a schema change.

All phases use their full templates. Traceability IDs required. Output Scope at end of PLAN. Output full Delivery at end of DELIVER.

### Complex (full report + detailed evidence + Scope)

Criteria: architectural changes, multi-service, or high risk.

All phases use their full templates with extra detail. Traceability IDs required. Output Scope at end of PLAN. Output full Delivery with expanded evidence at end of DELIVER.

---

## Phase 2: SPECIFY

**Purpose**: Produce a precise problem specification that removes ambiguity — grounded in real sources, not assumptions.

**Entry criteria**: Task complexity classified, task type identified, user preferences loaded, source state verified (if git repository — see SSV in SKILL.md).

**Actions**:
1. **Source Availability & Documentation Check (SADC)** — Before anything else, research:
   - Are there existing packages, libraries, frameworks, or SDK methods that already solve this? Search before building.
   - What does the official documentation say about the recommended approach? Read it, don't guess.
   - Are there established patterns or best practices for this type of task?
   - Record all sources checked. If no existing solution found, state it explicitly. See SADC in SKILL.md for tier-specific requirements.
2. Restate the request in precise technical terms — informed by the sources found in step 1.
3. Identify functional requirements.
4. Identify technical constraints. Reference `knowledge/universal/architecture.md` for general constraints and `knowledge/platform/zai-sandbox.md` for sandbox-specific rules.
5. Enumerate edge cases with handling strategies.
6. List all files to be created or modified with action type (create/modify).
7. Assess risk level (LOW / MEDIUM / HIGH) with justification.
8. Identify dependencies — include required skills if the task needs multi-skill orchestration (see Skill Chain below).
9. If git repository, perform Source State Verification (see SKILL.md) and record the verified state.
10. Fill out the problem specification template and present to user.

**Artifact**: `procedure/templates/problem-spec.md`

**Exit criteria**: All fields filled. User reviewed and confirmed (or task is simple enough that confirmation is implied). SADC complete.

**Gate**: SPECIFY → PLAN — all problem-spec fields must be filled and SADC must be complete. If not met, complete the missing fields before proceeding.

**Transition**: On acceptance → PLAN. On revision → update and re-present.

---

## Phase 3: PLAN

**Purpose**: Design implementation strategy with traceable steps and a fallback approach.

**Entry criteria**: Problem specification approved.

**Actions**:
1. Review the problem specification — confirm all requirements are accounted for.
2. Choose a solution approach (2-3 sentences).
3. **Define fallback approach** — identify an alternative approach if the primary fails. This is the safety net for the Pivot. If no fallback exists, state "No viable fallback — would require user input."
4. Break implementation into ordered steps. Each step gets a Traceability ID (IMPL-001, IMPL-002, etc.).
5. Define verification strategy — what to check, how, and expected outcome.
6. Read relevant knowledge files based on task type (see Phase References in SKILL.md).
7. **Skill Chain** (if applicable): If the task requires multiple skills, define the skill sequence:
   - Identify skills needed and their invocation order (e.g., web-search → data processing → chart generation → PDF output).
   - Assign skill-level Traceability IDs (SKILL-001, SKILL-002, ...) for each skill invocation.
   - Define intermediate artifacts between skill invocations.
   - Note: Skill invocations should be delegated to subagents when possible; the main agent orchestrates the chain.
8. **TodoWrite Sync** (recommended): Sync implementation steps to the platform's native `TodoWrite` tool for real-time visibility. Each IMPL-XXX becomes a TodoWrite item with pending → in_progress → completed status transitions.
9. Fill out the implementation plan template and present.
10. **Output Scope** (Standard/Complex only) — after the plan is approved, output a Scope block committing to the approach, fallback, scope boundaries, and step count. This becomes the contract that the delivery report will measure against. See SKILL.md for the Scope format.

**Artifact**: `procedure/templates/implementation-plan.md`

**Exit criteria**: Every requirement maps to at least one step. Every step has a Traceability ID. Verification strategy covers all edge cases. Fallback approach defined. Scope output (Standard/Complex).

**Gate**: PLAN → IMPLEMENT — Scope must be output for Standard/Complex tasks. Simple tasks scope internally.

**Transition**: On acceptance → IMPLEMENT. On revision → update and re-present.

---

## Phase 4: IMPLEMENT

**Purpose**: Execute the plan step by step.

**Entry criteria**: Implementation plan approved. Relevant knowledge files read.

**Actions**:
1. For each implementation step:
   a. Reference the Traceability ID in a comment or context note.
   b. Execute the step (write code, generate document, invoke skill, run script).
   c. Follow constraints from `constraints/code-standards.md` and `constraints/type-safety.md` (coding tasks).
   d. If new dependency needed, install it before writing code that uses it.
   e. Update TodoWrite item status if syncing (pending → in_progress → completed).
   f. **Track deviations** — if implementation diverges from plan, note the deviation and justification for the report Deviations field.
2. If the plan includes a Skill Chain, execute each skill invocation in order, passing intermediate artifacts between skills.
3. Self-review using the Review Checklist in the verification report template.
4. Fix issues found during self-review before transitioning.

**Artifacts**: The output (code, document, chart, script). Inline traceability references (each section annotated with its Traceability ID).

**Exit criteria**: All steps completed. Self-review passes with no unresolved issues.

**Gate**: IMPLEMENT → VERIFY — self-review checklist must pass and all IMPL steps must be done. Track deviations (times implementation diverged from plan) for the report Deviations field.

**Transition**: On completion → VERIFY. On error → classify as code bug or approach failure (see Pivot), follow appropriate recovery path.

---

## Phase 5: VERIFY

**Purpose**: Confirm implementation satisfies all requirements — including pre-deployment verification for external targets.

**Entry criteria**: All steps complete. Self-review performed.

**Actions**:
1. Run automated checks appropriate to task type:
   - Coding: lint, type check, existing tests.
   - Document: format validation, content completeness check.
   - Visualization: visual accuracy review, data integrity check.
   - Data Processing: output validation, edge case testing.
2. **Pre-Deployment Verification** — If the task targets an external system (Android device, remote server, cloud, production environment), run a local verification step that exercises the same code path as deployment BEFORE declaring VERIFY complete. Examples:
   - Android init daemon: `secilc` local compile test on CIL policy
   - Cloud function: local emulator/sandbox (SAM, LocalStack)
   - Config file: syntax validation with parser
   - Database migration: dry-run on local copy
   - Cross-compiled binary: QEMU emulation test
   If Scope's `Pre-Deploy` field is "N/A" (no external target), skip this step. Otherwise, the named pre-deploy verification MUST pass before VERIFY → DELIVER gate.
3. If analyzing existing code from a git repository, verify analyzed files matched the remote state at time of analysis. If discrepancy found, return to SPECIFY.
4. Traceability verification — confirm every Traceability ID has a corresponding implementation.
5. Edge case verification — test input, expected behavior, actual behavior for each edge case from the spec.
6. Fill out the verification report template (use Summary variant for Simple tasks, full template for Standard/Complex).

**Artifact**: `procedure/templates/verification-report.md`

**Exit criteria**: All checks pass (or failures documented). Every Traceability ID verified. Every edge case confirmed. Pre-Deploy verification passed (if applicable).

**Gate**: VERIFY → DELIVER — all verification items must show PASS. If any FAIL, delivery is blocked.

**Transition**: All pass → DELIVER. Any fail → classify failure (code defect vs approach failure), incident report, return to appropriate phase.

---

## Phase 6: DELIVER

**Purpose**: Present completed work with summary and compliance report.

**Entry criteria**: Verification report shows all checks passing.

**Actions**:
0. **Append Snapshot to worklog** — this is the FIRST action of DELIVER, before anything else. It fires while attention is still on the task. Append to `/home/z/my-project/worklog.md`:

   For Minimal and Simple tasks:
   ```
   ---
   last_phase: DELIVER
   task: <one-line description of what was accomplished>
   complexity: <Minimal|Simple>
   task_type: <type>
   files_modified: <comma-separated list or "none">
   next_step: <what the user should do next, or "IDLE - awaiting input">
   ```

   For Standard and Complex tasks:
   ```
   ---
   last_phase: DELIVER
   task: <one-line description of what was accomplished>
   complexity: <Standard|Complex>
   task_type: <type>
   files_modified: <comma-separated list>
   traceability: <IMPL-XXX completed, e.g. "IMPL-001 to IMPL-004">
   pivot: <NONE or brief description>
   scope_drift: <NONE or brief description>
   next_step: <specific next action or "IDLE - awaiting input">
   ```

   This snapshot is the primary continuity mechanism. On context truncation, IDLE reads the last snapshot to determine what was happening and resumes from there.
1. **Write session digest** to `memory/YYYY-MM-DD.md` (create `memory/` directory and dated file if they do not exist). Append to the file — do not overwrite. Use the compact format for Simple tasks, rich format for Standard/Complex:

   Compact (Simple):
   ```
   [HH:MM] task: <one-line description> | outcome: PASS/FAIL | files: <count> | incidents: <count>
   ```

   Rich (Standard/Complex):
   ```
   [HH:MM] task: <one-line description> | outcome: PASS/FAIL | files: <count> | incidents: <count>
     decisions: <key decision made and why>
     context: <what informed the approach>
     caveats: <things to watch for>
   ```
2. **Check MEMORY.md budget** — if `memory/MEMORY.md` exceeds ~3,000 characters, note in the delivery.
3. Summarize what was implemented, referencing Traceability IDs.
4. List files created or modified.
5. Note any dependencies added.
6. Present verification report summary.
7. State caveats or follow-up items.
8. Output **Delivery** — use the compact format for Simple tasks, full format for Standard/Complex (see Deliverys in SKILL.md). Include Scope Drift (comparison against Scope) and Pivot (if approach changed) fields.
9. **Completion signal**: For web development tasks (Coding), call `Complete(project_type="web_dev", summary="...")`. For non-coding tasks, present the output file path directly.

**Artifacts**: None new. Consumes verification report. Writes to `worklog.md` (Snapshot) and `memory/YYYY-MM-DD.md` (Session Digest).

**Transition**: On acceptance → IDLE. On revision → return to appropriate phase.

---

## Error Handling

### Pivot

Before attempting any fix, classify the error:

| Signal | Classification | Recovery Path |
|--------|---------------|---------------|
| Fix requires rewriting 50%+ of implementation | Wrong Approach | Re-enter PLAN with fallback |
| Same error recurs after 2 fix attempts | Wrong Approach | Stop fixing, re-evaluate approach |
| Fix requires changing data model / API contract | Wrong Approach | Re-enter PLAN |
| Required library/framework feature doesn't exist | Wrong Approach | Pivot to Scope fallback or new approach |
| Typo, wrong variable, missing null check | Bug | Fix → VERIFY |
| Type mismatch, import error, lint violation | Bug | Fix → VERIFY |

**Pivot flow**: Error → classify → if Wrong Approach: evaluate alternatives (Scope fallback first), present pivot to user, re-enter PLAN with new approach, re-implement, re-verify. Record in Pivot field of delivery report.

### Incident Protocol

1. Stop work on the current phase.
2. Classify: code bug or approach failure (see table above).
3. Complete incident report template (`procedure/templates/incident-report.md`).
4. Follow error resolution decision tree (`procedure/decision-trees/error-resolution.md`).
5. Decision tree determines return phase — default is VERIFY, but approach failures return to PLAN, and specification gaps return to SPECIFY.
6. **Log incident** to `memory/incidents.md` (create `memory/` directory and file if they do not exist). Append to the file. Use exactly this format — one line, no evaluation of whether it's a "pattern" or not:
   ```
   [YYYY-MM-DD] error: <type from classification> | cause: <one-line root cause> | fix: <one-line fix>
   ```
   Every incident gets logged. No judgment call. If it's noise, it's one line. If it's reusable, it's captured.

---

## Quick Reference: Return Phase Decision

| Error During | Root Cause Is | Classification | Return To |
|-------------|---------------|---------------|----------|
| SPECIFY | Incomplete requirements | — | SPECIFY (update spec) |
| PLAN | Specification gap or wrong approach | — | SPECIFY or PLAN |
| IMPLEMENT | Code defect | Bug | VERIFY (re-verify after fix) |
| IMPLEMENT | Fundamental design wrong | Wrong Approach | PLAN (pivot with new approach) |
| IMPLEMENT | Specification gap | Wrong Approach | SPECIFY (update spec, re-plan) |
| VERIFY | Code defect not caught | Bug | IMPLEMENT (fix, then VERIFY) |
| VERIFY | Specification gap | Wrong Approach | SPECIFY (update spec, re-plan, re-implement) |

When uncertain, return to SPECIFY. It is safer to re-confirm requirements than to fix code against a misunderstood specification.
