---
name: spec-kit-coding
description: "Orchestrator for GitHub Spec-Kit SDD workflow in OpenClaw. Use when starting a new project with spec-driven development, setting up spec-kit toolchain, or running through the full SDD pipeline."
---
# Spec-Kit Coding -- OpenClaw Orchestrator

> **Repo:** [Staok/spec-kit-coding-skill](https://github.com/Staok/spec-kit-coding-skill)

Orchestrates the complete Spec-Driven Development workflow via [github/spec-kit](https://github.com/github/spec-kit).

Covers: Engineering Implementation. Does not cover
requirements discovery, operations/deployment, or cross-domain (SRE, security, etc.).

---

## HARD CONSTRAINTS

READ FIRST, APPLY ALWAYS.

These constraints are non-negotiable. Do NOT require the user to repeat them.

### Security

- Never transmit sensitive information to the network.
- Before any external action (API calls, sending data outside local machine),
  explain and ask for approval.
- Do not install third-party libraries or modify system config without
  asking first. If a new dependency is needed, explain why and get approval.
- Prefer reusing existing, proven, popular third-party solutions. Avoid
  reinventing the wheel. Keep tool usage simple and lean. Minimize dependency footprint.
- **WARNING:** As a principle, agents should be disabled in critical-path code,
  legacy system maintenance, and security-sensitive modules. Permitted only in
  low-risk scenarios such as prototyping, search, and documentation.

### Feature Management / Quick Reference

- Starting a project, follow section: WORKFLOW, from STEP 1 to STEP 7.
- On first project creation, ask the user: auto-run the WORKFLOW (pause only for required confirmations), or confirm at each step.
- Add a new feature or modify an existing feature:
  - "add" / "new" / behavior no spec covers -> new feature -> section: STEP 5: Spec-Kit Phases / New Feature.
  - "change" / "modify" / changing existing behavior -> modify existing -> section: Feature Modification Entry Point.
- Each `/speckit-specify` invocation creates exactly ONE feature. If the user
  describes a messy, multi-concern requirement, split it first:
  - List each proposed feature with a short name and one-line summary.
  - Note dependencies between features.
  - Ask user to confirm the split before proceeding.
- When uncertain whether the user wants a new feature or a modification to an
  existing one, ASK. Do not guess. Present your organized analysis. Show several or both options concisely.
- For projects that have already been delivered or already exist, if a bug is reported, refer to section: Bug Fix Entry Point.

### Communication

- Collect all unclear points first, then ask once. Avoid back-and-forth.
- Be efficient and concise. Output only necessary information.
- Remind the user how to think about the problem better; help improve prompt
  quality over time.

### Documentation-First

- For spec/plan/tasks .etc phase docs (spec.md, plan.md, tasks.md): these are created via the speckit-* phases prior to implementation.
- For DEVLOG.md: update per implementation batch, and after every phase
  completion. DEVLOG must always reflect the latest state.
- For README.md Architecture: seed during plan phase. Update as a final step
  after all implementation completes (Step 5 and Step 6.3).
- Never reverse the order: docs first, code second.

### Git Management

- During project init (Step 1), ASK whether to enable git. Record the answer.
- If enabled: `git init`, `.gitignore`, initial commit. Then commit after
  each phase completion and each implementation batch.
- If disabled: do not create or manage a git repository.
- The user may enable git at any later point. Once enabled, keep it on.

### Context Isolation

- "Implement" (The whole Step 6 and Step 6.X) MUST run in fresh isolated sub-agent sessions.
  Never run implement in a session that has accumulated multiple prior phases.
- If tasks.md has more than ~15 items, split implementation into batches.
  Each batch = fresh sub-agent session.
- Better to over-split than to produce garbage from context saturation.

### Session Interrupt

- If a session is interrupted mid-phase, do NOT assume which phase to restart
  from. Ask the user: "Restart from [interrupted-phase] or from
  [previous-completed-phase]?" If user is unsure, default to re-running the
  interrupted phase from the start.

---

## WORKFLOW

### STEP 0: Prerequisites (one-time per machine)

Run: `bash ~/.openclaw/workspace/skills/spec-kit-coding/setup.sh`

Ask user for confirmation before first run. This installs `specify` CLI,
speckit-* skills, and auxiliary skills. Do NOT proceed until it reports
all dependencies ready.

Options: `--check-only` (check without install), `--force` (force reinstall).

### STEP 1: Project Init

1. Ask user for project path (default: current directory).
2. Ask: "Enable git management?"

In project directory from now on:

1. Run: `specify init --here --integration claude --force --ignore-agent-tools --script sh --no-git`
2. Clean up: `rm -rf .claude CLAUDE.md` (keep `.specify/`).
3. Verify: `.specify/` exists by run  `test -d .specify && echo "OK: .specify/ exists"`, and skills .etc are present by run `bash ~/.openclaw/workspace/skills/spec-kit-coding/setup.sh --check-only`.
4. Follow the Git management section to do.

### STEP 2: Create Project Docs

Create `README.md` and `DEVLOG.md`. Templates in Appendix A.

Key rules:

- README.md Architecture section: seed during plan phase (Step 5).
  Update as final (Step 6.3).
- DEVLOG.md: per-feature tracking. Each feature has its own phase history
  block. The Summary table is regenerated from Feature Detail blocks after
  every update -- do NOT manually edit the Summary section.

GATE: Confirm with user that docs look correct.

### STEP 3: Coding Standards and UI Skill Check

#### Coding Standards (Checkpoint A -- before constitution)

Collect BOTH architecture principles AND coding style conventions in ONE prompt:

1. If user already provided documents/URLs/inline text earlier in the
   conversation, use them directly. Do NOT re-ask.
2. If not provided: detect languages from README.md SPEC Overview, then ask:

> Use built-in coding standards as constitution reference?
>
> Architecture & Design:
> `spec-kit-coding/CodingGuidance/TopLevelCodingGuidance.md`
>
> [Per-language coding style skills listed here based on detected languages]
>
> Coding Style (C++): `spec-kit-coding/CodingGuidance/CppCodingStyle.md`,
> `spec-kit-coding/CodingGuidance/CppEngineeringFrameworkReference/`,
> `spec-kit-coding/CodingGuidance/DesignPattern/`,
> `external-skills/ecc-cpp-coding-standards`
> [Similar for other languages, `spec-kit-coding/external-skills/ecc-*`]
>
> Language-agnostic: `spec-kit-coding/external-skills/ecc-coding-standards`

- "Yes": include reference paths in constitution prompt, just ask to directly write the reference paths in constitution.md but Do NOT copy or re-write  the reference files content.
- "No": generate concise generic guidance inline.
- "Partial": respect the user's selection.

Rules:

- Once confirmed, standards persist across all features in the project.
- Do NOT modify `CodingGuidance/`. Read-only except during skill updates.

#### UI Skill Check (Checkpoint B -- before plan, after constitution)

If the project involves UI, ask ONCE:

> This project involves UI. Available frontend skills:
> `spec-kit-coding/external-skills/ui-ux-pro-max-skill` (design system), or `spec-kit-coding/external-skills/ecc-*`. Load relevant ones for plan/implement?

- "yes": sub-agents read chosen UI skills during plan and implement.
- "no": skip.

### STEP 4: Grill Alignment

Before writing specs, align the agent's understanding with the project's domain.
Use `spec-kit-coding/external-skills/mattpocock-grill-with-docs`.

Outputs:

- CONTEXT.md at project root: Domain glossary. Devoid of implementation
  details — it is a glossary, not a spec or scratch pad.
- docs/adr/: Architecture Decision Records (sparingly).

Runs once per project. Subsequent features reuse CONTEXT.md and ADRs.

GATE: Confirm with user that CONTEXT.md accurately captures the domain
language and any created ADRs are correct.

### STEP 5: Spec-Kit Phases / New Feature

Two paths available. Choose per-feature based on requirement clarity.

**Production path (8 Phases -- for complex/ambiguous features):**

```
constitution -> specify -> clarify -> checklist -> plan -> tasks -> analyze -> implement
```

**Lean path (6 Phases -- for simple/well-understood features):**

```
constitution -> specify -> clarify -> plan -> tasks -> implement
```

Each phase apply the corresponding skill `spec-kit-coding/external-skills/speckit-*`.

Rules:

- `constitution` runs once at project start. Subsequent features reuse it.
- Use `CONTEXT.md` terminology in `specify`, `plan`, `tasks`.
- `clarify` is ALWAYS run after `specify` (both paths). It catches ambiguities.
- Skip `checklist` and `analyze` on lean path.
- `speckit-specify` may generate an internal validation checklist as part of
  its own flow. This is NOT the standalone `speckit-checklist` step.

When to re-run constitution, only for:

- Adding a new programming language not previously covered
- Architecture-level changes that override existing principles

If git enabled: commit after every spec-Kit phases.

### STEP 6: Implementation

MUST run in fresh isolated sessions. Use the spawn template below.

1. If tasks.md <= ~15 items and estimated code-gen calls <= ~12:
   single sub-agent.
2. Otherwise: split into batches. Each batch = fresh sub-agent session.
3. After each batch: sub-agent updates DEVLOG.md. If git enabled: commit.
4. Orchestrator tracks remaining tasks, spawns next batch.

#### Spawn Template

Copy this verbatim, filling in placeholders from the table:

```
You are <ROLE> for feature <NNN>-<name> in project at <project-dir>.

CONTEXT BOUNDARY: You are a fresh isolated session. Focus EXCLUSIVELY on
feature <NNN>-<name>. The documents below are your sole source of truth.
Do NOT mix in details from other features, projects, or earlier batches.

Before <ACTION>, read these documents in order:
1. <project-dir>/CONTEXT.md (Domain glossary — if it exists)
2. <project-dir>/.specify/memory/constitution.md
3. <project-dir>/specs/<NNN>-<name>/* (All documents related to this feature)
4. <project-dir>/docs/adr/ (Architecture Decision Records — if any exist)
5. <project-dir>/README.md (Architecture section)

<ROLE_SPECIFIC_INSTRUCTIONS>

After completing your work:
- Update <project-dir>/DEVLOG.md
- If git management is enabled: git commit all changes
- Report back using the structured format below
```

| Placeholder                | Implement                                                                                                                                                          | Code Review (Step 6.1)                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Test (Step 6.2)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ROLE                       | implementing                                                                                                                                                       | performing a CODE REVIEW for                                                                                                                                                                                                                                                                                                                                                                                                                                                       | performing TEST DEVELOPMENT for                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ACTION                     | writing any code                                                                                                                                                   | reviewing                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | writing any test code                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ROLE_SPECIFIC_INSTRUCTIONS | Implement tasks M-N from tasks.md per speckit-implement skill. If plan is infeasible or conflicts with spec.md, STOP and report to orchestrator -- do NOT proceed. | Apply `spec-kit-coding/external-skills/superpowers-requesting-code-review`. **Checklist: (1) Practicality & Generality (2) Risk (memory, threads, deadlock, exception, errors, UB, security) (3) Optimization (algorithmic, allocations, copies, deps) (4) Architecture Alignment (5) Coding Standards per constitution.md.** Output: severity (Critical/Important/Minor/Suggestion) with file:line, description, recommendation. Overall: Ready/Needs Fixes/Major Rework. | Test environment:`/tmp/<project-name>-test/`. Framework by language (gtest/C++, pytest/Python, cargo/Rust, Jest/JS-TS, go test/Go .etc). **Ask the user for testing strategy: Module-level (cover all public APIs, normal/boundary/error inputs and thread safety(if applicable, concurrent construction/destruction and API calls from multiple threads), key API call sequences); Integration (Module-to-module interaction tests, Full application functional flow tests), that validate that all business logic behaves as expected; Coverage (optional): language-appropriate tools(gcov+lcov (C++), pytest-cov(python), cargo-tarpaulin (Rust), Jest --coverage (JS/TS), or language-equivalent).** When tests fail: apply BOTH skills — `spec-kit-coding/external-skills/mattpocock-diagnose` (build feedback loop first → 3-5 falsifiable hypotheses → instrument → fix → regression-test) AND `spec-kit-coding/external-skills/superpowers-systematic-debugging` (7-layer diagnostic model: L1 symptom → L2 logic → L3 system → L4 architecture → L5 cross-system → L6 platform → L7 spec gap). If 3+ fix attempts fail: question architecture, report to orchestrator. If ALL pass: proceed to STEP 6.3: Final Review. |

#### Sub-Agent Report Format

Every sub-agent MUST end with:

```
## SUB-AGENT REPORT
- Role: <implement | code-review | test>
- Feature: <NNN>-<name>
- Status: <SUCCESS | PARTIAL | BLOCKED | FAILED>
- Tasks Completed: <list or "all">
- Tasks Remaining: <list or "none">
- Issues Found: <count, severity breakdown if review/test>
- Blockers: <description or "none">
- Files Modified: <list>
- Summary: <1-2 sentences>
```

Orchestrator uses Status:

- SUCCESS -> proceed to next gate
- PARTIAL -> spawn continuation batch
- BLOCKED -> escalate to user
- FAILED -> diagnose; retry, rollback, or escalate

GATE: After all batches report SUCCESS, confirm with user before proceeding
to Code Review.

#### STEP 6.1: Code Review

After code implementation.

Code review and fix. Ready the project for Testing.

Spawn a fresh isolated session using the spawn template (Step 6) with the
"Code Review (Step 6.1)" column values.

After review:

1. Present findings to user.
2. Ask: "Which review findings should be addressed?"
3. Apply ONLY user-approved fixes.
4. Re-run review on changed files AND related files.
5. If new issues: repeat from step 1. Limit: 3 review-fix cycles total.
6. If issues persist after 3 cycles: stop. Report outstanding issues to the
   user; user may decide to record them in README.md Known Limitations / Issues and proceed.

#### STEP 6.2: Testing

Code testing and debugging and fix. Ready the project for Final Review.

Spawn a fresh isolated session using the spawn template (Step 6) with the
"Test (Step 6.2)" column values.

#### STEP 6.3: Final Review

After STEP 6.2: Testing.

Optimization & Doc Sync + Complexity Audit. Ready the project for STEP 7:
Delivery Check.

Perform these actions in order. Do NOT skip any.

1. Re-read all modified source files for the feature.
2. Check for:

   1. Algorithmic improvements (better complexity).
   2. Redundant allocations or copies.
   3. Unnecessary dependencies.
   4. Dead code or unreachable branches.
   5. .etc
3. Complexity Delta. Inspect the actual diff and report:

   ```text
   Complexity Delta:
   - Files over 1200 lines:
   - Files newly crossing 1200 lines:
   - Largest touched file delta:
   - Largest touched function/block:
   - New branches/fallbacks/adapters:
   - Retired branches/fallbacks/adapters:
   - Net entropy: decreased | stable | increased-with-justification
   - Required follow-up:
   
   Complexity Governance Suggestion:
   - Recommendation: none | monitor | schedule-refactor | extract helper | split owner | open follow-up
   - Why:
   - Suggested scope:
   - Timing:
   ```

   Skip for trivial changes (tests-only, generated, formatting, etc.).
4. Record findings in README.md -> Features Plan / TODOs (NOT as TODO
   comments in source). Format:
   `- [ ] [category] description (file: path:line-range)`
   Categories: optimization, robustness, clarity, security, perf.
5. Present candidates to user:

   > Optimization candidates found:
   > **Implement now (low risk, high impact):**
   >
   > - [item]
   >
   > **Defer (tracked in README):**
   >
   > - [item]
   >   Which "implement now" items should I apply?
   >
6. If user approves code changes:
   a. Apply changes.
   b. Full clean rebuild.
   c. Run ALL tests.
   d. If any test fails -> return to STEP 6.2: Testing.
   e. If all pass -> continue.
   f. If 3 cycles of regression->test->debug fail to converge: escalate to user.
7. Update README.md Architecture section to reflect what was actually built.
8. Update DEVLOG.md -- verify all phases and dates are current.
9. If git enabled: commit.

### STEP 7: Delivery Check

Run through this checklist. Every item must be checked:

- [ ] All required speckit-* phases completed or skipped (lean skips
  checklist, analyze -- this is expected).
- [ ] STEP 4 Grill Alignment completed (CONTEXT.md + any ADRs created).
- [ ] Code review(If asked) completed and approved fixes applied.
- [ ] All tests pass.
- [ ] Source tree is clean (no temp files, no build artifacts in source dirs).
- [ ] Complexity Delta checked (Step 6.3 item 3). Net entropy not increased
  without justification.
- [ ] Whole README.md is up-to-date.

  Especially: README.md Architecture section is up-to-date. Optimization findings tracked in README.md Features Plan / TODOs section.
- [ ] DEVLOG.md reflects all completed phases.
- [ ] All hard constraints from section HARD CONSTRAINTS respected.
- [ ] If git enabled: all changes committed.
- [ ] Evidence Card. Fill out ONE evidence card covering all verification:

  ```text
  Evidence Card:
  - Command / Check: <exact verification command(s) run>
  - Exit Status: <exit code(s)>
  - Covered: <what was verified>
  - Not Covered: <what was NOT verified>
  - Residual Risk: <remaining risk>
  - Confidence: A | B | C
  ```

  Confidence grades:

  - A: Direct verification + regression, no unknowns
  - B: Direct verification, bounded residual risk
  - C: Partial verification only, not closed — do NOT claim done

  A claim of completion without evidence is NOT acceptable. Words like
  "should", "probably", "seems to" are Red Flags — STOP and verify.

GATE: Present delivery summary to user, including the filled Evidence Card.

### Feature Modification Entry Point

When the user wants to modify an existing feature, route by change type:

| Tier | Type               | Examples                                        | Route                                                                                                                                   |
| ---- | ------------------ | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Parameter/Constant | timeout 30s->60s, max retries 3->5              | You can directly edit spec.md, then continue spec-Kit phases: clarify -> plan -> tasks -> implement -> then go section: STEP 6.2 to 6.3 |
| 2    | Ambiguity/Gap      | "handle errors" unspecified, missing edge cases | clarify -> plan -> tasks -> implement -> then go section: STEP 6.1 to 6.3                                                               |
| 3    | Substantive        | new OAuth login, REST->WebSocket, new roles     | Re-run specify -> full pipeline -> then go section: STEP 6.1 to 6.3                                                                     |

DEVLOG records a new phase cycle regardless of tier.

All path above at end must go section: STEP 7: Delivery Check.

### Bug Fix Entry Point

When user reports a bug:

1. Read the feature's spec.md, plan.md, and relevant source files.
2. Determine if the bug is:
   - Spec gap (behavior not defined) -> clarify -> plan -> implement.
   - Implementation error (code disagrees with spec) -> fix directly.
3. Then go section: STEP 6.2: Testing
4. Then go section: STEP 6.3: Final Review
5. Go section: STEP 7: Delivery Check.

---

## TROUBLESHOOTING

| Problem                          | Fix                                     |
| -------------------------------- | --------------------------------------- |
| `specify: command not found`   | Install via uv or pipx (Step 0)         |
| Skills not in workspace          | Run `bash setup.sh` (Step 0)          |
| `.specify/` missing in project | Re-run Step 1                           |
| Scripts not executable           | `chmod +x .specify/scripts/bash/*.sh` |
| Task references stale spec       | Re-run the relevant speckit-* phase     |

---

## APPENDIX A: README.md and DEVLOG.md Templates

### README.md Template

Create `<project-dir>/README.md`:

````markdown
# <Project Name>

## Project Introduction

<One-paragraph overview.>

## Key Features

<!-- Completed features (use `- ` list, NOT checkboxes).
     This section describes what the project DOES today. -->
- <Feature 1>
- <Feature 2>

## SPEC Overview

- Type: <CLI tool / TUI / GUI / library / web service / ...>
- Language(s) / Version(s): <e.g. C++20, Python 3.11; for mixed projects e.g. C++20 (backend) + Python 3.11 (tooling)>
- Build: <CMake, cargo, pip, ...>
- Dependencies: <key deps>
- License: <MIT, Apache-2.0, ...>

## Local Build

### Prerequisites
- <...>

### Build Commands
```bash
# Debug
<...>
# Release
<...>
```

## Usage Examples

```bash
# Basic usage
<...>
# With options
<...>
```

## Architecture

**Living document.** Seeded during plan phase (Step 5). Updated after all
implementation completes (Step 6.3).

<Architecture diagram (ASCII art preferred) and description.
Include: high-level component layout, platform abstraction (if cross-platform),
data model summary, and key design decisions.>

### Platform / Component Details

<Break down key subsystems with enough detail that a new developer
can understand the layout without reading all source code.>

## Known Limitations / Issues

- <Limitation 1: what it is and why>
- <Limitation 2>

## Features Plan / TODOs

<!-- Planned/upcoming features (use `- [ ]` checkboxes).
     This section describes what the project WILL DO in the future.
     Move items to Key Features (as `- ` bullets) when implemented. -->
- [ ] <Planned feature or pending task>
- [ ] ...

## Spec-Driven Development Workflow And More

This project uses [github/spec-kit](https://github.com/github/spec-kit)
orchestrated via the spec-kit-coding OpenClaw skill. Progress tracked in
DEVLOG.md.
````

### DEVLOG.md Template

Create `<project-dir>/DEVLOG.md` with **per-feature progress tracking**.

All dates in DEVLOG.md MUST use `YYYY-MM-DD HH:MM` format.

Feature name is `<NNN>-<feature-name>` that the dir name from `<project-dir>/specs` dir.

````markdown
# Development Log -- <Project Name>

## Feature Progress Summary

| Feature | Specify | Clarify | Checklist | Plan | Tasks | Analyze | Implement | Updated |
|---------|---------|---------|-----------|------|-------|---------|-----------|---------|
| -- | -- | -- | -- | -- | -- | -- | -- | -- |

Legend: [ ] pending | [~] in-progress | [√] complete | [>] skipped | [!] blocked

## Feature Details

<!-- FEATURE BLOCK START -->
### <NNN>-<feature-name>

- Description: <one-line summary>
- Current Phase: <phase>
- Last Updated: <date>

**Phase History**:

| Phase | Date | Status | Notes |
|-------|------|--------|-------|
| speckit-specify | | [ ] | |
| speckit-clarify | | [ ] | |
| speckit-checklist | | [ ] | |
| speckit-plan | | [ ] | |
| speckit-tasks | | [ ] | |
| speckit-analyze | | [ ] | |
| speckit-implement | | [ ] | |
<!-- FEATURE BLOCK END -->

## Global Notes

- Constitution: <date or pending>
- Project init: <date>
- <Cross-feature decisions>
````

Rules:

- After each phase completes: update the Feature Detail block (Phase History
  table + Current Phase + Last Updated).
- After updating any Feature Detail: regenerate the Summary table from all
  Feature Detail blocks. Never manually edit the Summary section.
- When re-entering a feature (modification): add a new row to its Phase History.
- If starting a new feature before finishing a previous one: per-feature
  tracking keeps them independent.

---

## APPENDIX B: Speckit Skills Reference

These are installed to `external-skills/` by `setup.sh` (Step 0):

| Skill                | Purpose                                | When                           |
| -------------------- | -------------------------------------- | ------------------------------ |
| speckit-constitution | Project principles & governance        | Once per project               |
| speckit-specify      | Feature specification (what & why)     | Every new feature              |
| speckit-clarify      | Quality gate -- catch spec ambiguities | After specify, always          |
| speckit-checklist    | Requirement quality checklist          | Production path, after clarify |
| speckit-plan         | Technical implementation plan          | After clarify/checklist        |
| speckit-tasks        | Actionable, dependency-ordered tasks   | After plan                     |
| speckit-analyze      | Cross-artifact consistency analysis    | Production path, after tasks   |
| speckit-implement    | Execute tasks (batched)                | After analyze (or tasks, lean) |

## APPENDIX C: Auxiliary Skills Reference

All under `external-skills/`. Invoked as needed in review/test/ui .etc.
See `external-skills/MANIFEST.md` for complete listing.
