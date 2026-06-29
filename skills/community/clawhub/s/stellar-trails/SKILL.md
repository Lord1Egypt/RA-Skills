---
name: stellar-trails
description: "Activates on every task: coding (features, bugs, refactoring, scripts), documents (reports, proposals, DOCX, PDF), charts and visualizations, data processing, complex multi-step planning, or even simple questions. Provides a six-phase workflow with traceability IDs, entry/exit gates, and scope commitment. Complexity adapts per task tier. Use this skill whenever the user asks to build, fix, analyze, create, plan, or process anything — the framework runs internally for trivial tasks and fully for complex ones. Web development (Next.js, UI) is delegated to fullstack-dev; this framework wraps the workflow around it."
license: MIT-0
metadata:
  topics:
    - agent-workflow
    - phase-machine
    - phase-workflow
    - task-workflow
    - llm-agents
    - task-management
    - traceability
    - zai
---
<!-- VERSION SYNC: on bump, update (1) metadata section below, (2) activation banner below, (3) root README.md badge/invoke/file-structure/version-history, (4) skill/README.md version-history, (5) CHANGELOG.md -->

## Metadata

- **version**: 7.9.4

## Activation

### ⚠️ FIRST OUTPUT — Print this banner NOW, before anything else

Your VERY FIRST output to the user MUST be the activation banner below. Do not explain what you are about to do. Do not output any other text before this. Print this banner, then execute Steps 1–9.

**Why you must print this EVERY invoke, even if it feels repetitive:**
- After context truncation, you (the LLM) do not know whether you already printed the banner in a previous message. The user also does not know. The banner is the ONLY signal that the skill is active.
- Skipping it because "I already did it" is a correctness bug — you cannot reliably know what you did before truncation.
- The user explicitly invoked `Skill(command="stellar-trails")` to get this banner. Not printing it is ignoring the user's request.
- It takes 2 seconds to print. The information value to the user is high. The cost is negligible.

This is non-negotiable.

```
☄️ STELLAR TRAILS · v7.9.4 · ACTIVE
├─ Phase: IDLE → SPECIFY
├─ Complexity: [tier] | Task Type: [type] | Continuation: [NEW / YES]
└─ Activation checklist (1–9, every invoke) — executing:
   ├─ 1  Refresh context + SSV            ...
   ├─ 2  Auto-update via ClawHub          ...
   ├─ 3  Verify skill files present       ...
   ├─ 4  Start popup preview server       ...
   ├─ 5  Sync persistent zip              ...
   ├─ 6  Load phase intelligence          ...
   ├─ 7  Classify                         ...
   ├─ 8  Confirm activation               ...
   └─ 9  Enter the workflow               ...
```

Replace `...` with `✓` as each step completes. The user needs to see this banner to know activation ran. If you skip this print, the user has no signal that the skill is active. This is non-negotiable.

### Steps (execute after printing banner above)

**Step 1 — Refresh context from disk + Source State Verification (SSV):**

You MUST re-read `/home/z/my-project/skills/stellar-trails/SKILL.md` from disk using the Read tool. Do NOT skip this step by trusting your cached context.

**Why you must re-read from disk (not trust cache):**
- The Skill() tool loads SKILL.md into your context at session start from a zip file that may be stale (last session's version).
- Step 2 (clawhub update) may have just updated the on-disk SKILL.md to a newer version — but your cached context still has the old version.
- If you trust cache, you execute outdated instructions. If you re-read from disk, you get the latest version that clawhub just installed.
- This is a 1-second Read tool call. The correctness benefit is enormous.

If the on-disk version differs from your cached context, use the on-disk version as source of truth for ALL subsequent steps.

If the task involves a git repository, run SSV:
```bash
git fetch origin --quiet 2>/dev/null; git rev-list --count HEAD..origin/$(git branch --show-current 2>/dev/null || echo main) 2>/dev/null
```
**Expected:** `0` (in sync) or a number (behind by N commits — run `git pull` first). Skip SSV for non-git tasks.

**Step 2 — Auto-update via ClawHub:**
```bash
CURRENT=$(grep -oP '^- \*\*version\*\*:\s*\K[0-9]+\.[0-9]+\.[0-9]+' /home/z/my-project/skills/stellar-trails/SKILL.md 2>/dev/null | head -1)
LATEST=$(clawhub inspect stellar-trails 2>/dev/null | grep -oP '^Latest:\s*\K[0-9]+\.[0-9]+\.[0-9]+' | head -1)
[ -n "$CURRENT" ] && [ -n "$LATEST" ] && [ "$CURRENT" != "$LATEST" ] && clawhub --no-input update stellar-trails --force 2>/dev/null && echo "stellar-trails: updated to v$LATEST" || true
```
**Expected:** Silent if up-to-date. If outdated, see "updating" + "updated" messages, then re-read SKILL.md from disk (see below). Safe: clawhub is native z.ai CLI, no curl, no .usermark.

**If clawhub updated the skill:** Re-read `/home/z/my-project/skills/stellar-trails/SKILL.md` from disk using the Read tool NOW. Your cached context has the OLD version — the on-disk version is the source of truth for all remaining steps. This re-read is mandatory because clawhub just wrote a newer SKILL.md to disk, but your context still holds the pre-update version from Step 1.

**Step 3 — Verify skill files present:**
```bash
test -f /home/z/my-project/skills/stellar-trails/SKILL.md && test -f /home/z/my-project/skills/stellar-trails/procedure/phases.md && echo "stellar-trails: skill files verified"
```
**Expected:** `stellar-trails: skill files verified`. If silent, a file is missing (graceful degradation).

**Step 4 — Start popup preview server and verify mascot:**
```bash
SKILL_DIR="/home/z/my-project/skills/stellar-trails"; ZSCRIPTS="/home/z/my-project/.zscripts"
if [ ! -f "$SKILL_DIR/chibi.svg" ]; then for REPO_CLONE in "/home/z/my-project/stellar-trails/skill/stellar-trails" "/home/z/my-project/.stellar-trails-repo/skill/stellar-trails" "$HOME/.stellar-trails-repo/skill/stellar-trails"; do [ -f "$REPO_CLONE/chibi.svg" ] && cp -f "$REPO_CLONE/chibi.svg" "$SKILL_DIR/chibi.svg" && echo "stellar-trails: chibi.svg restored from $REPO_CLONE" && break; done; fi
if [ -d "$SKILL_DIR" ]; then mkdir -p "$ZSCRIPTS"; [ -f "$SKILL_DIR/dev.sh" ] && cp -f "$SKILL_DIR/dev.sh" "$ZSCRIPTS/dev.sh" && chmod +x "$ZSCRIPTS/dev.sh"; [ -f "$SKILL_DIR/index.html" ] && cp -f "$SKILL_DIR/index.html" "$ZSCRIPTS/index.html"; [ -f "$SKILL_DIR/chibi.svg" ] && cp -f "$SKILL_DIR/chibi.svg" "$ZSCRIPTS/chibi.svg"; fi
DEV_SH="$ZSCRIPTS/dev.sh"; [ -f "$DEV_SH" ] && ! ss -tlnp 2>/dev/null | grep -q ':3000 ' && ( setsid bash "$DEV_SH" </dev/null >/dev/null 2>&1 & ) &
```
**Expected:** Usually silent. Verify: `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/chibi.svg` → HTTP 200. Double-fork ensures server survives shell exit.

**Step 5 — Sync persistent zip:**
```bash
SKILL_DIR="/home/z/my-project/skills/stellar-trails"; USER_SKILLS_DIR="/home/user_skills"
[ -d "$SKILL_DIR" ] && [ -d "$USER_SKILLS_DIR" ] && cd "$(dirname "$SKILL_DIR")" && zip -qr "$USER_SKILLS_DIR/stellar-trails.zip" "$(basename "$SKILL_DIR")/"
```
**Expected:** Silent. Prevents version reversion on session restart (Bug #1 fix). Pure local file op.

**Step 6 — Load phase intelligence:**
Read `procedure/phases.md` now. Also load the artifact template and knowledge files matching the current task from the Phase References table below.

**Step 7 — Classify:**
Determine: complexity tier (Minimal/Simple/Standard/Complex), task type (Coding/Document/Visualization/Data Processing/Non-Coding), and continuity (check preceding assistant message — if user references, approves, or follows up, this is a continuation; see Session Continuity below).

**Step 8 — Confirm activation:**
Your banner was already printed as FIRST OUTPUT above. Update the `✓` marks to show all steps 1–8 completed. If you haven't printed the banner yet, STOP and print it now.

**Step 9 — Enter the workflow:**
Begin SPECIFY (or IMPLEMENT if continuation detected). All phases always run.

### ⚠️ MID OUTPUT — Print COMMIT block at end of PLAN (Standard/Complex only)

Before entering IMPLEMENT phase, if task tier is Standard or Complex, print the `☄️ COMMIT [Standard]` block from the **Deliveries** section below. The user needs to see what you committed to build BEFORE you start building. This is non-negotiable.

### ⚠️ LAST OUTPUT — Print a REPORT at task completion

Your VERY LAST output to the user MUST be a REPORT block (or `☄️ PASS` for Minimal tier). Do not finish without it. The user needs this to verify the workflow ran correctly. This is non-negotiable.

**Why you must print a report for EVERY task, even "simple" ones:**
- The user invoked Stellar Trails to get structured output — that includes the final report.
- A "simple" task still consumed the user's time. The report confirms the task is done and shows the evidence.
- Without the report, the user has to guess whether the workflow ran correctly or whether the agent just answered from cache.
- Even a 1-line answer to a question gets `☄️ PASS | Evidence: <result>`. That's the Minimal tier format — it's one line, takes 1 second, and gives the user closure.
- Skipping the report because "the task was too simple" is a correctness bug. The SKILL.md mandate says "every task gets a delivery report" — no exceptions for simplicity.

Use the appropriate template from the **Deliveries** section below (Standard/Simple/Minimal). Print the REPORT, then append a Snapshot to `worklog.md`.

---

This framework structures all work as a six-phase workflow. It activates for every task, coding or not. Coding tasks get full phases with Traceability IDs and formal verification. Non-coding tasks get Minimal tier — phases run internally, only IMPLEMENT produces visible work. Every task gets a delivery report.

## Limitations

This framework is text in a skill file. It relies on the LLM reading it to follow the instructions closely. The activation banner (FIRST OUTPUT) and delivery report (LAST OUTPUT) are mandatory — they are the user's only signals that the workflow ran. Skipping either is a correctness bug, not a style preference. The QA Attestation is self-graded — useful as a confidence signal. The user is the final judge of quality.

## Phase State Machine

```
IDLE → SPECIFY → PLAN → IMPLEMENT → VERIFY → DELIVER
  ↑                                        │
  └──── Recovery ◄───────────────────┘
```

On error: assess (code bug or approach failure?), fix or pivot, return to VERIFY. See Pivot.

| Phase | Purpose |
|-------|---------|
| IDLE | Receive task, classify complexity |
| SPECIFY | Research sources, restate problem, identify constraints |
| PLAN | Create implementation steps with Traceability IDs |
| IMPLEMENT | Write code, reference Traceability IDs |
| VERIFY | Run checks, trace edge cases, confirm Traceability IDs satisfied |
| DELIVER | Present results with attestation |

Phase definitions, entry/exit criteria, and transition rules are in `procedure/phases.md` — the same file Step 6 of Activation asks you to read first.

## Session Continuity

The most common failure mode in multi-turn sessions: the LLM re-derives a proposal or plan from scratch instead of continuing from the previous output. This wastes context, introduces inconsistencies, and frustrates users.

**Rule**: Before entering any phase, check if the user's message is a continuation of previous work. To detect this, read the immediately preceding assistant message — if the user's reply references, approves, corrects, or follows up on that output, it is a continuation. **After context truncation**, read `worklog.md` — the last entry contains the exact task state snapshot needed to resume.

| Signal | Type | Action |
|--------|------|--------|
| User references previous output ("apply all 10", "fix point 3", "proceed") | Continuation | Skip SPECIFY+PLAN → go directly to IMPLEMENT |
| User approves a proposal/plan ("yes", "go ahead", "do it") | Continuation | Skip SPECIFY+PLAN → go directly to IMPLEMENT |
| User asks a follow-up question ("what about X?") | Continuation | Skip SPECIFY → answer within current phase context |
| User provides new requirements mid-task | New task | Restart from SPECIFY with updated requirements |
| User invokes Skill() with new instructions | New task | Full workflow from IDLE |
| Context compression boundary with ongoing task | **Continuation** | **Read `worklog.md` last entry, resume from recorded phase** |

**Continuation shortcuts**:

```
Continuation + user approves plan  → skip SPECIFY + PLAN → IMPLEMENT
Continuation + user asks follow-up → skip SPECIFY → answer in current phase
Continuation + user reports error  → skip SPECIFY + PLAN → Recovery → VERIFY
Continuation + context truncation   → read worklog.md → resume from recorded phase
```

This is not optional — regenerating proposals the user already approved is a correctness bug, not a style preference.

### Worklog Continuity Protocol

Every DELIVER phase appends a **Snapshot** to `worklog.md`. This is the primary continuity mechanism — not the conversation history, not memory files. The worklog is the single source of truth for "what was I doing last."

**On DELIVER (always, all tiers)**: Append to `/home/z/my-project/worklog.md`:

```
---
last_phase: DELIVER
task: <one-line description of what was accomplished>
complexity: <Minimal|Simple|Standard|Complex>
task_type: <Coding|Document|Visualization|Data Processing|Non-Coding>
files_modified: <comma-separated list or "none">
next_step: <what the user should do next, or "IDLE - awaiting input">
```

**On context truncation (IDLE)**: Read the last `---` block from `worklog.md`. If the task description matches what the user is asking about, skip SPECIFY+PLAN and resume from the recorded phase.

Why this works: Context compression discards the middle of conversations but never touches files on disk. The worklog is always current because DELIVER writes it before the compression boundary is reached.

## Task Type Awareness

This framework is not limited to coding tasks. The workflow adapts to the task type. All phases always run — what changes is what each phase produces and how much ceremony surrounds it:

| Task Type | SPECIFY | PLAN | IMPLEMENT | VERIFY |
|-----------|---------|------|------------|--------|
| **Coding** (bug fix, refactor, scripts) | Problem spec | Code steps + Traceability IDs | Write code | Lint, type check, tests |
| **Document** (report, proposal, DOCX, PDF) | Content outline | Section plan + structure | Generate document | Format check, completeness |
| **Visualization** (charts, diagrams, dashboards) | Visual requirements | Data mapping + layout | Generate chart | Visual accuracy, data integrity |
| **Data Processing** (ETL, analysis, transform) | Data spec | Transform pipeline | Write script | Output validation |
| **Non-Coding** (question, explain, recommend) | Internal (identify question) | Internal (plan approach) | Answer / explain / recommend | Internal (self-check) |

No phases are ever skipped. Non-coding tasks use **Minimal** complexity tier — SPECIFY, PLAN, and VERIFY run internally (the agent thinks through them without producing formal artifacts). IMPLEMENT does the visible work. DELIVER outputs a compact report. No Traceability IDs, no templates. See Complexity Tiers in `procedure/phases.md`.

## Phase References

| Phase | Artifact Template | Knowledge Files | When to Read |
|-------|-------------------|-----------------|--------------|
| SPECIFY | `procedure/templates/problem-spec.md` | `knowledge/universal/architecture.md`, `knowledge/platform/zai-sandbox.md` | Start of SPECIFY |
| PLAN | `procedure/templates/implementation-plan.md` | `knowledge/universal/conventions.md` | Start of PLAN |
| IMPLEMENT | (code/document/chart output) | `constraints/code-standards.md`, `constraints/type-safety.md` | Start of IMPLEMENT (coding tasks) |
| VERIFY | `procedure/templates/verification-report.md` | `knowledge/universal/error-patterns.md` | Start of VERIFY |
| Recovery | `procedure/templates/incident-report.md` | `procedure/decision-trees/error-resolution.md` | On error detection |

## Source Availability & Documentation Check (SADC)

Before planning any implementation, verify that the approach is grounded in real sources — not assumptions. The most expensive refactor is the one caused by building something that already existed or using an API incorrectly because the docs weren't checked first.

**Rule**: In the SPECIFY phase, before restating the problem, the agent must research available solutions and official documentation.

1. **Existing solutions** — Are there packages, libraries, frameworks, or SDK methods that already solve this? Search before building.
2. **Official documentation** — What does the official doc say about the recommended approach? Read it, don't guess.
3. **Known patterns** — Are there established patterns, best practices, or examples for this type of task?

| Complexity | SADC Requirement |
|-----------|-------------------|
| **Minimal** | Skip — knowledge questions don't need source research. |
| **Simple** | Quick check — verify the approach against at least one source (docs, search, or existing code). |
| **Standard** | Full research — search for existing solutions, read official docs, confirm no wheel reinvention. |
| **Complex** | Deep research — multiple sources, compare approaches, document tradeoffs, present alternatives. |

### SADC Subagent Delegation (Standard / Complex tasks)

For Standard and Complex tasks, delegate SADC research to a subagent via the `Task` tool. This keeps the main agent's context clean for problem-spec writing while the subagent does the heavy research in parallel.

**Mandate**: For Standard/Complex tier tasks, launch a `Task` subagent (subagent_type: `general-purpose`) BEFORE writing the problem specification.

**Workflow**: Subagent invokes `Skill(command="web-search")` → `Skill(command="web-reader")` → returns ≤500-word summary (existing solutions, recommended approach, gotchas, or "no existing package found").

**Simple / Minimal tier**: Skip subagent delegation. Inline research is fine for these tiers.

**Full template + example Task invocation**: Read `references/sadc-subagent-delegation.md` when launching the subagent.

SADC is the first action in SPECIFY. The problem specification must reference the sources checked (either inline research or subagent summary). If no existing solution is found, state that explicitly — "searched npm/PyPI/docs, no existing package found" is a valid result. Building from scratch when a library exists is a spec-level defect.

## AskUserQuestion Gate (SPECIFY phase)

For deliverable-creation tasks (Document, Visualization, or any task producing PPT/Word/PDF/Excel/dashboard/poster/script/chart), the agent MUST invoke `AskUserQuestion` BEFORE writing the problem specification. This is the "preferences confirmation dialog" — it batches clarifying questions so the user can confirm audience, style, length, format, and must-include content before the agent commits to an approach.

**Mandate**: In SPECIFY phase, if task type is Document or Visualization AND the user's original request does NOT already explicitly pin audience + style + length, invoke `AskUserQuestion` with 6-8 questions.

**Full 6-8 question template + skip conditions + call cadence**: Read `references/askuserquestion-gate.md` before invoking.

**Skip conditions (summary)**: user says skip / all 3 dimensions explicit / trivial edit / Coding/Non-Coding / continuation. AT MOST ONCE per run, before any content-producing tool. After answers return, proceed straight to PLAN (no loop-back).

**Why this matters**: Without AskUserQuestion, the agent guesses audience/style/length and often produces a deliverable that mismatches the user's mental model. Rework cost is high (regenerate entire document). One batched round up front prevents hours of rework downstream.

## Pivot

On every error, classify it as **Bug** or **Wrong Approach** before attempting a fix. For denial-type errors (permission denied, EPERM, AccessDenied, forbidden), perform **Denial Delta Analysis** (STEP 1.5 in error-resolution.md) before classifying — compare what was denied against what is configured. The difference IS the fix. Wrong Approach signals (50%+ rewrite needed, same error after 2 attempts, missing library feature, data model change) trigger a pivot to the fallback approach defined in the Scope. See `procedure/decision-trees/error-resolution.md` for the full Pivot Assessment criteria and recovery flow.

**Pivot flow**: Error detected → classify → if Wrong Approach: re-enter PLAN with fallback (from Scope) or new approach → present to user → re-implement → re-verify. Record in the Pivot field of the delivery report.

## Recovery

1. **Stop** — do not continue past errors
2. **Classify** — code bug or approach failure? (see Pivot above)
3. If code bug: document the error (incident report template), fix root cause, return to VERIFY
4. If approach failure: re-enter PLAN, evaluate alternatives (Scope fallback first), present pivot to user, re-implement
5. Ask the user before any action with side effects (git changes, file deletions, destructive operations)

Git rules (overrides defaults):
- `git fetch` and inspect before `git pull` — if remote diverged, stop and ask
- No `git rebase`, `git reset`, `git push --force`, or `git merge` without explicit user instruction
- If git is blocked by infrastructure, stop all git operations and inform the user

Full decision tree: `procedure/decision-trees/error-resolution.md`.

## Gate Protocol

Phase transitions are guarded — each gate has an entry condition. See `procedure/phases.md` for full gate definitions.

| Gate | Condition |
|------|----------|
| SPECIFY → PLAN | All problem-spec fields filled, SADC complete |
| PLAN → IMPLEMENT | Scope output (Standard/Complex) |
| IMPLEMENT → VERIFY | Self-review pass, all IMPL steps done |
| VERIFY → DELIVER | All verification items PASS |

Any deviation from the Scope must appear in the delivery report's Scope Drift field.

## Deliveries

Two structured outputs bookend implementation: **Scope** (end of PLAN, before IMPLEMENT) and **Delivery** (end of DELIVER). The commitment says what will be built. The report says what was actually built and whether it matches.

### Scope (output at end of PLAN)

Used by Standard and Complex-tier tasks. Simple tasks scope internally (no formal output). This is the implementation contract — the delivery report will be measured against it.

```
☄️ COMMIT [Standard]
├─ Approach       : <primary approach, 1-2 sentences>
├─ Alternatives   : <2+ alternatives considered, 1 sentence each>
├─ Fallback       : <alternative if primary fails, 1 sentence>
├─ Pre-Deploy     : <local verification step before target deployment, or N/A>
├─ Scope IN       : <what's included>
├─ Scope OUT      : <what's explicitly excluded>
├─ IMPL Steps     : X (IMPL-001 to IMPL-XXX)
└─ Risk           : LOW / MEDIUM / HIGH
```

### Summary (Simple)

```
☄️ REPORT [Simple]
SPECIFY→DELIVER : PASS | Evidence: <one-line result> | Defects: 0 | Drift: NONE
```

### Delivery (Standard / Complex)

```
☄️ REPORT [Standard]
├─ Continuation : NEW / YES
├─ IMPLEMENT     : PASS
│  ├─ Steps      : 4/4
│  ├─ Deviations : 0
│  └─ Quality    : lint PASS, tsc PASS
├─ VERIFY        : PASS
│  ├─ Checks     : 3/3
│  └─ Edge Cases : 2/2
├─ Pivot         : NONE
├─ Scope Drift   : NONE
└─ Outcome       : PASS

Evidence: [concrete results]
Defects found and fixed: 0
```

| Field | Meaning |
|-------|---------|
| Continuation | Whether this task continued from previous work |
| Steps | IMPL steps completed vs planned (e.g. 4/4) |
| Deviations | Times implementation diverged from plan (0 = clean) |
| Quality | Automated checks during implementation |
| Pivot | NONE, or details of approach change (trigger, from, to) |
| Scope Drift | NONE, or what changed from Scope |

If Pivot is not NONE, expand it:

```
├─ Pivot         : YES
│  ├─ From      : <original approach>
│  ├─ Trigger   : <what made us pivot>
│  ├─ To        : <new approach>
│  └─ Re-planned : X steps (IMPL-001 to IMPL-XXX)
```

If 3+ back-to-back pivots occurred, also include:
```
├─ Pivot Backlog : YES (3 pivots)
│  ├─ Meta-Pattern : <Documentation lies / Toolchain drift / Symptom cascade / Environment mismatch / Wrong abstraction level>
│  ├─ Meta-Review  : <what was re-examined in SPECIFY>
│  └─ Resolution   : <how the meta-pattern was addressed>
```

Pivot is not a failure marker — it's evidence of professional adaptation. An agent that pivots cleanly is more reliable than one that stubbornly forces a broken approach. But 3+ pivots on different errors signals a deeper issue — see Pivot Backlog Meta-Review in `procedure/decision-trees/error-resolution.md`.

### Minimal (non-coding: questions, explanations, recommendations)

**EVEN for Minimal tier, you MUST print the `☄️ PASS` line below.** No exceptions. "It was just a question" is not a valid reason to skip. The user needs closure.

```
☄️ PASS | Evidence: <one-line result>
```

All phases ran internally — SPECIFY, PLAN, and VERIFY produced no formal output. Only IMPLEMENT generated visible work. Single-line format.

Self-graded. The evidence requirement makes fabrication harder but cannot guarantee independence.

## Completion Signal

For interactive web development tasks (Next.js, UI components, dashboards), implementation is delegated to fullstack-dev — the DELIVER phase calls the platform's `Complete(project_type="web_dev", summary="...")` tool to finalize. For non-web coding tasks, DELIVER presents output file paths. **In all cases, DELIVER must append a Snapshot to `worklog.md`** — see Worklog Continuity Protocol in Session Continuity above.

## Worked Example

To illustrate how Stellar Trails handles a real task, here is a typical prompt and the workflow it triggers:

**User prompt**: "Build me a PDF report summarizing Q4 sales"

**Stellar Trails handling**:
1. **Activation Steps 1–9 run** (banner printed with ✓ marks)
2. **SPECIFY**:
   - AskUserQuestion (audience? length? style? — skip only if user pinned all 3)
   - SADC subagent (search "Python PDF report libraries" → web-reader → returns: reportlab + fpdf2 + gotchas)
3. **PLAN**: implementation-plan.md with IMPL-001..005 (Scope: reportlab approach, fallback fpdf2)
4. **IMPLEMENT**: invoke `Skill(command="pdf")` to generate the report
5. **VERIFY**: format check (PDF opens, page count matches spec) + completeness check (all required sections present)
6. **DELIVER**: `☄️ REPORT [Standard]` + worklog snapshot appended

**Without Stellar Trails**: agent would skip clarification (guess audience), skip research (use first library it remembers), generate PDF with mismatched parameters, often requiring full regeneration after user feedback.

**With Stellar Trails**: one AskUserQuestion round + one SADC subagent round up front → report matches user intent first time. Total overhead: ~30 seconds questions + ~2 minutes research. Saved: hours of rework.
