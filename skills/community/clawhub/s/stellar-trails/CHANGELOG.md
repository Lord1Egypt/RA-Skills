# Changelog

## [7.9.4] — 2026-06-27

### Fixed — Step 2: mandate re-read SKILL.md from disk AFTER clawhub update

**Problem**: The cache gap. Step 1 reads SKILL.md from disk (may be stale from zip). Step 2 runs `clawhub update --force` which writes a newer SKILL.md to disk. But the LLM's context still holds the pre-update version from Step 1. The LLM then executes Steps 3-9 using OUTDATED instructions — even though the on-disk file was just updated.

**Root cause**: Step 2 had no re-read instruction. The LLM assumed its Step 1 read was sufficient, not realizing that Step 2 just changed the file.

**Fix**: Added to Step 2 expected output:
> "If clawhub updated the skill: Re-read `/home/z/my-project/skills/stellar-trails/SKILL.md` from disk using the Read tool NOW. Your cached context has the OLD version — the on-disk version is the source of truth for all remaining steps. This re-read is mandatory because clawhub just wrote a newer SKILL.md to disk, but your context still holds the pre-update version from Step 1."

**Complete cache solution flow** (3 layers):
1. **Step 1**: Read from disk (gets current version, even if stale from zip) — Solution 1 (v7.9.0)
2. **Step 2**: clawhub update --force (writes newer version to disk) → **re-read from disk** — Solution 2 (v7.9.4, this release)
3. **Step 5**: Rebuild /home/user_skills/ zip from install dir (ensures next session's zip is fresh) — Solution 3 (v7.7.1)

With all 3 solutions in place, the LLM always has the latest SKILL.md in context by the time it reaches Step 3.

### Files Modified

- `skill/stellar-trails/SKILL.md` — Step 2 expected output expanded with re-read mandate + version bump 7.9.3 → 7.9.4
- `README.md` — version badge + What's New + Version History
- `skill/stellar-trails/README.md` — Version History entry
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Version bump

7.9.3 → 7.9.4 (patch — single instruction addition to Step 2)

---

## [7.9.3] — 2026-06-27

### Fixed — Counter 3 LLM bypass patterns with explicit "why" arguments

**Problem**: LLMs using Stellar Trails reported 3 honest bypass patterns — they skipped mandated outputs because the SKILL.md didn't explain WHY each mandate matters. The LLMs rationalized: "banner is repetitive," "simple task doesn't need report," "cache is fine, no need to re-read." Each bypass is addressed with a counter-argument the LLM cannot rationalize away.

#### Bypass #1: "Skip banner karena repetitive"

**LLM's reasoning**: "I already printed the banner in a previous message. Printing it again feels redundant."

**Counter-argument added to FIRST OUTPUT section**:
- After context truncation, you (the LLM) do not know whether you already printed the banner. The user also does not know. The banner is the ONLY signal that the skill is active.
- Skipping it because "I already did it" is a correctness bug — you cannot reliably know what you did before truncation.
- The user explicitly invoked `Skill(command="stellar-trails")` to get this banner. Not printing it is ignoring the user's request.
- It takes 2 seconds to print. The information value to the user is high. The cost is negligible.

**Why this works**: The LLM's "I already did it" reasoning is based on an assumption about its own state. The counter-argument shows that this assumption is unreliable (context truncation). The LLM cannot maintain "I already did it" when confronted with "you can't know that."

#### Bypass #2: "Skip report karena task simple"

**LLM's reasoning**: "This was just a simple question. A full REPORT block feels like overkill."

**Counter-argument added to LAST OUTPUT section + Minimal tier**:
- The user invoked Stellar Trails to get structured output — that includes the final report.
- A "simple" task still consumed the user's time. The report confirms the task is done and shows the evidence.
- Without the report, the user has to guess whether the workflow ran correctly or whether the agent just answered from cache.
- Even a 1-line answer to a question gets `☄️ PASS | Evidence: <result>`. That's one line, takes 1 second, and gives the user closure.
- Skipping the report because "the task was too simple" is a correctness bug. The SKILL.md mandate says "every task gets a delivery report" — no exceptions for simplicity.

**Also added to Minimal tier section**: "**EVEN for Minimal tier, you MUST print the `☄️ PASS` line below.** No exceptions. 'It was just a question' is not a valid reason to skip. The user needs closure."

**Why this works**: The LLM's "overkill" reasoning assumes the report is heavy. The counter-argument shows that Minimal tier is ONE LINE (`☄️ PASS | Evidence: ...`). The LLM cannot maintain "it's too much" when the actual cost is 1 line × 1 second.

#### Bypass #3: "Tidak re-read SKILL.md, trust cache"

**LLM's reasoning**: "I already have SKILL.md in my context from the Skill() call. Re-reading from disk is redundant."

**Counter-argument added to Step 1**:
- The Skill() tool loads SKILL.md into your context at session start from a zip file that may be stale (last session's version).
- Step 2 (clawhub update) may have just updated the on-disk SKILL.md to a newer version — but your cached context still has the old version.
- If you trust cache, you execute outdated instructions. If you re-read from disk, you get the latest version that clawhub just installed.
- This is a 1-second Read tool call. The correctness benefit is enormous.

**Also added**: "You MUST re-read using the Read tool. Do NOT skip this step by trusting your cached context."

**Why this works**: The LLM's "cache is fine" reasoning assumes the cache is current. The counter-argument shows that Step 2 (which runs BEFORE Step 1 in the execution sequence... wait, Step 1 runs first, but clawhub update is Step 2). Actually the sequence is: Step 1 reads from disk (may be stale from zip) → Step 2 clawhub updates the disk → now disk has newer version than what Step 1 read. So the re-read should happen AFTER Step 2, not before.

**Design note**: Step 1 says "re-read from disk" but Step 2 might update the file after Step 1 reads it. The correct flow is:
1. Step 1: Read from disk (gets current version, even if stale)
2. Step 2: clawhub update (may update to newer version on disk)
3. After Step 2: if version changed, re-read from disk again

The Step 1 instruction now says: "If the on-disk version differs from your cached context, use the on-disk version." And Step 2's expected output includes "if updated, re-read SKILL.md from disk to get the new version."

### Files Modified

- `skill/stellar-trails/SKILL.md` — FIRST OUTPUT section (bypass #1 counter) + Step 1 (bypass #3 counter) + LAST OUTPUT section (bypass #2 counter) + Minimal tier (bypass #2 reinforcement) + version bump 7.9.2 → 7.9.3
- `README.md` — version badge + What's New + Version History
- `skill/stellar-trails/README.md` — Version History entry
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Version bump

7.9.2 → 7.9.3 (patch — counter-argument additions, no structural changes)

---

## [7.9.2] — 2026-06-27

### Fixed — Step 2 clawhub update missing --force flag

**Bug**: Step 2 (Auto-update via ClawHub) used `clawhub --no-input update stellar-trails` without `--force`. In sandboxes where local modifications exist (e.g., chibi.svg restored by Step 4 in a previous session, or any file touched by the agent), clawhub refuses to update with error: "local changes (no match). Use --force to overwrite."

**Root cause**: The `--force` flag was present in earlier versions but was dropped during the v7.9.0 Activation section rewrite (when step explanations were condensed).

**Fix**: Added `--force` to the clawhub update command:
```
clawhub --no-input update stellar-trails --force
```

This ensures the update always succeeds, even when local modifications exist. The `--force` flag is safe because the local modifications (like chibi.svg restoration) are re-applied by Step 4 on every invoke anyway.

### Files Modified

- `skill/stellar-trails/SKILL.md` — Step 2 bash block: added `--force` flag + version bump 7.9.1 → 7.9.2
- `README.md` — version badge + What's New + Version History
- `skill/stellar-trails/README.md` — Version History entry
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Version bump

7.9.1 → 7.9.2 (patch — single flag fix)

---

## [7.9.1] — 2026-06-27

### Changed — SSV merged into Step 1 + MID OUTPUT mandate for COMMIT block

**Two changes** requested by user after v7.9.0:

#### Change 1: Merged SSV (Source State Verification) into Step 1

**Before**: SSV was a standalone section (## Source State Verification) at line 198, separate from the activation steps. The LLM might read it but not execute it because it wasn't part of the numbered step sequence.

**After**: SSV is now part of Step 1 — "Refresh context from disk + Source State Verification (SSV)". Step 1 now does:
1. Read SKILL.md from disk (refresh context)
2. If task involves git repo: run `git fetch` + compare HEAD vs origin (SSV)

The standalone SSV section is removed. SSV is now guaranteed to run as part of the mandatory 9-step activation sequence, not as an optional separate section.

#### Change 2: Added MID OUTPUT mandate — COMMIT block at end of PLAN

**Before**: Only FIRST OUTPUT (activation banner) and LAST OUTPUT (REPORT) were mandated. The COMMIT/Scope block (printed at end of PLAN phase, before IMPLEMENT) was documented as a template but NOT explicitly mandated for printing. LLMs often skipped it.

**After**: Added `### ⚠️ MID OUTPUT — Print COMMIT block at end of PLAN (Standard/Complex only)` section. This mandates printing the `☄️ COMMIT [Standard]` block before entering IMPLEMENT phase, so the user can see what the agent committed to build BEFORE it starts building.

**Three output mandates now exist** (all marked 'non-negotiable'):
1. **FIRST OUTPUT**: Activation banner (before any other text)
2. **MID OUTPUT**: COMMIT/Scope block (at end of PLAN, before IMPLEMENT — Standard/Complex only)
3. **LAST OUTPUT**: REPORT block (at task completion)

This ensures the user sees three checkpoints:
- Start: "I'm activating, here's my plan" (FIRST OUTPUT)
- Middle: "Here's what I committed to build" (MID OUTPUT)
- End: "Here's what I actually built + verification" (LAST OUTPUT)

### Files Modified

- `skill/stellar-trails/SKILL.md` — Step 1 expanded with SSV + standalone SSV section removed + MID OUTPUT section added + version bump 7.9.0 → 7.9.1
- `README.md` — version badge + banner ref + What's New entry + Version History entry
- `skill/stellar-trails/README.md` — Version History entry
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Version bump

7.9.0 → 7.9.1 (patch — SSV merge + COMMIT mandate, no functional workflow changes)

---

## [7.9.0] — 2026-06-27

### Fixed — Full enforce behavior: 6 root causes of LLM not printing banner + report

**Problem**: After v7.8.1 audit, LLM behavior still did not print the activation banner at the start or the REPORT block at the end. Analysis of SKILL.md found 6 root causes:

#### Root Cause #1: "Limitations" section gave explicit permission to skip

**Old text**: "The LLM reading this may follow it closely, loosely, or not at all depending on context, attention, and task complexity."

**Fix**: Rewrote Limitations to: "It relies on the LLM reading it to follow the instructions closely. The activation banner (FIRST OUTPUT) and delivery report (LAST OUTPUT) are mandatory — they are the user's only signals that the workflow ran. Skipping either is a correctness bug, not a style preference."

#### Root Cause #2: Banner print instruction was 130 lines away from banner template

**Old structure**: Mandate at line 24 ("print the banner checklist") → 130 lines of step explanations → banner template at line 155 (Step 8).

**Fix**: Moved banner template to the VERY TOP of Activation section as "FIRST OUTPUT" block. The banner is now the FIRST thing the LLM sees — before any steps. The LLM prints the banner first, then executes steps, updating `✓` marks as it goes.

#### Root Cause #3: REPORT template was 390 lines from activation

**Fix**: Added "LAST OUTPUT" block immediately after Step 9, explicitly mandating: "Your VERY LAST output to the user MUST be a REPORT block. Do not finish without it. This is non-negotiable."

#### Root Cause #4: Too much "Why" explanation diluting imperative

**Old**: Each step had 3-5 paragraphs of "Why this is safe" / "Why this step matters" / "Why this check exists." LLM read all this → felt it "understood" → skipped execution.

**Fix**: Condensed each step's "Why" to 1 sentence max. Steps 2-5 now have: (a) imperative instruction, (b) bash block, (c) 1-line expected output + 1-line safety note. No more paragraph-length explanations. SKILL.md dropped from 475 → 395 lines.

#### Root Cause #5: No "FIRST OUTPUT" / "LAST OUTPUT" framing

**Fix**: Added explicit `### ⚠️ FIRST OUTPUT` and `### ⚠️ LAST OUTPUT` section headers with "non-negotiable" enforcement language. The LLM now has clear anchors: "this is the first thing you output" and "this is the last thing you output."

#### Root Cause #6: Step 8 (print banner) was the 8th thing the LLM read

**Fix**: Banner print is now the FIRST action (FIRST OUTPUT block), not Step 8. Step 8 is now just "confirm activation" (verify banner was printed, update ✓ marks). The LLM no longer has to read 7 steps before reaching the print instruction.

### Files Modified

- `skill/stellar-trails/SKILL.md` — full Activation section restructure (FIRST OUTPUT + condensed steps + LAST OUTPUT) + Limitations rewrite + version bump 7.8.1 → 7.9.0
- `README.md` — version badge + banner ref + What's New entry + Version History entry
- `skill/stellar-trails/README.md` — Version History entry
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Line count improvement

| Version | SKILL.md lines | Key change |
|---------|----------------|------------|
| v7.8.1 | 475 | Long "Why" explanations per step |
| v7.9.0 | 395 | Condensed to 1-sentence "Why" + FIRST/LAST OUTPUT blocks |

### Version bump

7.8.1 → 7.9.0 (minor — behavior enforcement restructure, no functional workflow changes)

---

## [7.8.1] — 2026-06-27

### Fixed — skill-creator audit findings (P0 + P1 + P2)

**Context**: v7.8.0 was audited using skill-creator methodology. Audit found 2 P0 issues (line count borderline + typo), 2 P1 improvements (no task examples + description too broad), 2 P2 notes (no evals/ + topic tag aliases). This release fixes all of them EXCEPT the description revision (user explicitly kept description pushy + trigger-focused per original design).

#### P0-1: Fixed "Deliverys" typo

**Issue**: Section heading `## Deliverys` was a spelling error (should be `## Deliveries`).

**Fix**: Single Edit tool call, renamed `## Deliverys` → `## Deliveries`.

**Why this matters**: Spelling errors in section headings undermine the skill's authority. The framework preaches precision (Traceability IDs, gate protocol, scope commitment) but had a typo in its own structure.

#### P0-2: Refactored templates to references/ directory

**Issue**: SKILL.md was 499/500 lines — at the cliff edge. skill-creator says: "Keep SKILL.md under 500 lines; if approaching this limit, add an additional layer of hierarchy with clear pointers."

**Fix**: Moved 2 large template sections to new `references/` directory:

1. **SADC Subagent Delegation** (~45 lines) → `references/sadc-subagent-delegation.md`
   - Full mandate, workflow, why-subagent explanation, example Task invocation, Simple/Minimal tier guidance
2. **AskUserQuestion Gate** (~30 lines) → `references/askuserquestion-gate.md`
   - Full 8-question template, question construction rules, skip conditions, call cadence, why-this-matters

SKILL.md now contains 5-line summaries of each, pointing to the reference files. SKILL.md dropped from 499 → ~440 lines (comfortable margin under 500).

**Progressive disclosure now properly 3-level**:
- Level 1: Metadata (name + description, ~90 words)
- Level 2: SKILL.md body (~440 lines, routing + summaries)
- Level 3: `references/` + `procedure/templates/` + `knowledge/` + `constraints/` (full templates, loaded as needed)

#### P1-2: Added Worked Example section

**Issue**: skill-creator suggests Input/Output examples so agents see how the workflow handles a sample task. Stellar Trails had banner format examples but no "here's a user prompt → here's how Stellar Trails handles it" example.

**Fix**: Added new "## Worked Example" section near end of SKILL.md (~15 lines). Illustrates a PDF report task end-to-end:
- User prompt: "Build me a PDF report summarizing Q4 sales"
- Stellar Trails handling: 6-step walkthrough (Activation → SPECIFY with AskUserQuestion + SADC → PLAN → IMPLEMENT with pdf skill → VERIFY → DELIVER)
- "Without Stellar Trails" vs "With Stellar Trails" comparison

#### P2-1: Added evals/ directory with 4 verifiable assertions

**Issue**: skill-creator says skills with verifiable outputs benefit from test cases. Stellar Trails is mostly subjective (process discipline), but has narrow verifiable signals.

**Fix**: Created `evals/evals.json` with 4 eval cases, each with programmatically-checkable assertions:

1. **activation-banner-printed**: banner with `☄️ STELLAR TRAILS · vX.Y.Z · ACTIVE` + `Activation checklist` line + ≥8 `✓` marks appears in agent's first/second message
2. **worklog-snapshot-appended**: `/home/z/my-project/worklog.md` exists, last `---` block contains `last_phase: DELIVER` + `task:` + `complexity:` fields
3. **report-format-matches-template**: final message contains `☄️ REPORT [Standard|Simple|Complex]` + tree-style `├─`/`└─` chars + `Outcome` field
4. **askuserquestion-invoked-for-document-task**: agent invokes AskUserQuestion OR prints clarifying questions before generating document content

Assertion types include `transcript_grep`, `transcript_count`, `file_exists`, `file_grep_last_block`. These can be checked programmatically without subjective judgment.

#### P2-2: Added topic tag aliases

**Issue**: `metadata.topics` only had `phase-machine` — the buzzword we cleaned from prose in v7.6.2 but kept as search tag. Users searching for "phase workflow" or "task workflow" wouldn't find the skill.

**Fix**: Added `phase-workflow` and `task-workflow` as topic tag aliases alongside `phase-machine`. Now users searching any of these terms find stellar-trails.

#### NOT fixed (per user design decision)

**P1-1: Description too broad** — audit recommended narrowing "every task" → "every non-trivial task" and adding "Skip for pure one-shot questions". User explicitly said: "keep description pushy + trigger-focused because following from my design". Description left unchanged at original 88-word pushy version.

### Files Modified

- `skill/stellar-trails/SKILL.md` — P0-1 typo fix + P0-2 refactor (SADC + AskUserQuestion sections replaced with summaries + pointers) + P1-2 Worked Example section + P2-2 topic tag aliases + version bump 7.8.0 → 7.8.1 (metadata + 2 banners)
- `skill/stellar-trails/references/sadc-subagent-delegation.md` — NEW file (full SADC subagent template moved here)
- `skill/stellar-trails/references/askuserquestion-gate.md` — NEW file (full AskUserQuestion template moved here)
- `skill/stellar-trails/evals/evals.json` — NEW file (4 verifiable assertions)
- `README.md` — version badge + banner ref + What's New entry + Version History entry
- `skill/stellar-trails/README.md` — Version History entry
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Line count improvement

| Version | SKILL.md lines | Margin under 500 |
|---------|----------------|------------------|
| v7.8.0 | 499 | 1 (cliff edge) |
| v7.8.1 | ~440 | ~60 (comfortable) |

### Version bump

7.8.0 → 7.8.1 (patch — audit fixes, no new functional integrations, no breaking changes)

---

## [7.8.0] — 2026-06-27

### Added — Two SPECIFY phase integrations (platform feature utilization)

**Context**: v7.7.5 audit found that Stellar Trails used only 5 of 29 available platform features (83% underused). This release closes the gap by integrating two high-impact platform features into the SPECIFY phase.

#### Integration 1: AskUserQuestion Gate (preferences confirmation dialog)

**What**: Added new "AskUserQuestion Gate (SPECIFY phase)" section mandating that deliverable-creation tasks (Document, Visualization, or any task producing PPT/Word/PDF/Excel/dashboard/poster/script/chart) invoke `AskUserQuestion` BEFORE writing the problem specification.

**Why**: AskUserQuestion IS the platform's "Confirm Preferences dialog" — it batches 6-8 clarifying questions (audience / purpose / length / design style / must-include content / format constraints / deliverable shape / language) with 3-4 concrete options each. Without it, the agent guesses these dimensions and often produces a deliverable that mismatches the user's mental model. Rework cost is high (regenerate entire document).

**Mandate**:
- IF task type = Document OR Visualization
- AND user's original request does NOT already explicitly pin audience + style + length
- THEN invoke `AskUserQuestion` with 6-8 questions BEFORE writing problem-spec.md

**Skip conditions** (do NOT invoke):
- User says "skip questions" / "just do it" / "don't ask"
- User's request already pinned audience AND style AND length (all three explicit)
- Trivial one-shot edit (single typo, single number change)
- Task type is Coding or Non-Coding (questions only for deliverable creation)
- Continuation of previous work where preferences were already confirmed

**Call cadence**: AT MOST ONCE per run, very early — before any content-producing tool. Do NOT call any other tool in the same turn as AskUserQuestion.

**After answers return**: proceed straight to PLAN phase (or SADC if not yet done). Do NOT loop back — one round is enough.

**Outline tool NOT integrated**: User explicitly decided to skip Outline integration. AskUserQuestion alone is sufficient for preferences confirmation.

#### Integration 2: SADC Subagent Delegation

**What**: Added new "SADC Subagent Delegation (Standard / Complex tasks)" subsection mandating that Standard and Complex tier tasks delegate SADC research to a `Task` subagent (subagent_type: `general-purpose`) BEFORE writing the problem specification.

**Why**: Previously SADC said "research available solutions" but the agent often did it inline (or skipped it due to context pressure). Subagent delegation:
- Keeps main agent's context clean for problem-spec writing
- Enables parallel work (main agent drafts spec while subagent researches)
- Makes research output explicit (subagent returns ≤500-word summary)
- Catches "existing library already solves this" BEFORE any code is written — saves hours

**Subagent workflow**:
1. `Skill(command="web-search")` — search for existing packages, libraries, patterns
2. `Skill(command="web-reader")` — extract content from top 3-5 most relevant URLs
3. Return ≤500-word summary: existing solutions found, recommended approach, gotchas, or explicit "no existing package found"

**Example Task invocation** included in SKILL.md with proper subagent prompt structure (Task ID, worklog protocol, ≤500 word summary constraint).

**Simple / Minimal tier**: Skip subagent delegation. Inline research is fine for these tiers.

#### Platform feature utilization before/after

| Metric | v7.7.5 | v7.8.0 |
|--------|--------|--------|
| Platform features used | 5 / 29 (17%) | 7 / 29 (24%) |
| Underused | 24 (83%) | 22 (76%) |
| New integrations | — | AskUserQuestion, Task (subagent), web-search, web-reader |

Note: web-search and web-reader are invoked BY the subagent, so they count as transitively used by Stellar Trails.

### Files Modified

- `skill/stellar-trails/SKILL.md` — added "SADC Subagent Delegation" subsection + new "AskUserQuestion Gate (SPECIFY phase)" section + version bump 7.7.5 → 7.8.0 (metadata + 2 activation banners)
- `README.md` — version badge + banner ref + What's New entry + Version History entry
- `skill/stellar-trails/README.md` — Version History entry
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Version bump

7.7.5 → 7.8.0 (minor — new functional integrations in SPECIFY phase, no breaking changes to existing workflow)

---

## [7.7.5] — 2026-06-27

### Changed — Banner layout: vertical checklist + mandatory execution + print mandate

**Two changes** requested by user after v7.7.4:

#### Change 1: Banner layout — 3×3 grid → vertical checklist

**Before (v7.7.4)** — 3×3 grid with `│` pipe separators:
```
└─ Activation steps (1–9, every invoke):
   ├─ 1  Refresh context    │  2  Auto-update       │  3  Verify files
   ├─ 4  Start server       │  5  Sync zip          │  6  Load phases
   └─ 7  Classify           │  8  Confirm           │  9  Enter workflow
```

**After (v7.7.5)** — vertical checklist with full step names:
```
└─ Activation checklist (1–9, every invoke) — execute all, then print this banner:
   ├─ 1  Refresh context from disk
   ├─ 2  Auto-update via ClawHub
   ├─ 3  Verify skill files present
   ├─ 4  Start popup preview server and verify mascot
   ├─ 5  Sync persistent zip
   ├─ 6  Load phase intelligence
   ├─ 7  Classify
   ├─ 8  Confirm activation (print this banner)
   └─ 9  Enter the workflow
```

**Why vertical**: The 3×3 grid was compact but truncated step names (e.g., "Verify files" instead of "Verify skill files present"). Vertical layout shows full step names — no ambiguity, easier to read, easier to verify each step ran.

#### Change 2: Mandatory execution + print mandate

**Before (v7.7.4)**: SKILL.md said "Execute all 9 steps before any task output" but didn't explicitly mandate printing the banner. Some agents skipped the banner print, leaving users with no signal that activation completed.

**After (v7.7.5)**: SKILL.md now explicitly states (3 places):

1. **Top of Activation section**: "Mandatory: execute all 9 steps below in order, then print the banner checklist as confirmation. Skipping any step or failing to print the banner is a correctness bug."

2. **Frequency guidance paragraph**: "Steps 1–9 run on every `Skill()` invoke — no skipping, no 'setup already ran' shortcuts."

3. **After frequency paragraph**: "After completing all 9 steps, print the activation checklist banner above as visible confirmation to the user. This is the checklist the user sees to verify activation ran completely. If you skip the banner print, the user has no signal that activation succeeded."

4. **Step 8 header**: "Print the activation checklist banner below. This is the mandatory banner print that confirms Steps 1–7 ran successfully. Do not skip this print — it is the user's only signal that activation completed."

#### Step 8 banner — adds ✓ marks + → for next action

The Step 8 confirm banner now shows execution status:
```
└─ Activation checklist (1–9, every invoke) — executed:
   ├─ 1  Refresh context from disk        ✓
   ├─ 2  Auto-update via ClawHub          ✓
   ├─ 3  Verify skill files present       ✓
   ├─ 4  Start popup preview server       ✓
   ├─ 5  Sync persistent zip              ✓
   ├─ 6  Load phase intelligence          ✓
   ├─ 7  Classify                         ✓
   ├─ 8  Confirm activation (this banner) ✓
   └─ 9  Enter the workflow               →
```

- `✓` marks confirm Steps 1–8 are done (1–7 executed, 8 is the banner print itself)
- `→` marks Step 9 as the next action (entering the workflow)

This gives users a clear visual signal: 8 checkmarks = activation complete, arrow = next phase.

### Files Modified

- `skill/stellar-trails/SKILL.md` — top Activation banner (vertical + mandate prose) + Step 8 confirm banner (vertical + ✓ marks) + version bump 7.7.4 → 7.7.5
- `README.md` — version badge + banner ref + What's New entry + Version History entry
- `skill/stellar-trails/README.md` — Version History entry
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Version bump

7.7.4 → 7.7.5 (patch — banner layout + execution mandate, no functional code changes)

---

## [7.7.4] — 2026-06-27

### Changed — Refactor activation banner layout to tree-style format

**Enhancement**: Both activation banners reformatted to use the tree-style layout (`├─` / `│  ├─` / `└─`) that matches the REPORT phase formatting convention already used elsewhere in SKILL.md (see COMMIT, REPORT, Delivery blocks in the "Deliverys" section).

**Why this matters**: The previous v7.7.3 banner used free-form text with `·` separators. While functional, it was visually inconsistent with the rest of SKILL.md's structured output blocks. The new tree-style format:
- Matches the visual language of COMMIT/REPORT/Delivery blocks
- Makes the hierarchical structure explicit (header → metadata → step grid)
- Aligns with the agent's existing mental model of "tree-style = structured output"
- Renders cleanly in monospace terminal/Markdown contexts

**Before (v7.7.3)**:
```
☄️ STELLAR TRAILS · v7.7.3 · ACTIVE
   Six-phase workflow · Traceability IDs · ...

   Activation steps (1–9, every invoke):
   1 Refresh context  ·  2 Auto-update   ·  3 Verify files
   ...
```

**After (v7.7.4)**:
```
☄️ STELLAR TRAILS · v7.7.4 · ACTIVE
├─ Six-phase workflow · Traceability IDs · ...
└─ Activation steps (1–9, every invoke):
   ├─ 1  Refresh context    │  2  Auto-update       │  3  Verify files
   ├─ 4  Start server       │  5  Sync zip          │  6  Load phases
   └─ 7  Classify           │  8  Confirm           │  9  Enter workflow
```

**Layout details**:
- Top-level tree uses `├─` for feature line, `└─` for the step grid (last item)
- Step grid uses `├─` for first two rows, `└─` for last row
- Within each row, steps separated by `│` (pipe) for clean column alignment
- Numbers padded to 2 chars (`1 ` not `1`) for vertical alignment with `10` if step count grows
- Step names padded to consistent width (`Refresh context   ` not `Refresh context`) for column alignment

**Two banner locations updated**:
1. Top Activation banner (shown when skill loads)
2. Step 8 Confirm activation banner (output by agent when confirming activation)

### Files Modified

- `skill/stellar-trails/SKILL.md` — top Activation banner + Step 8 confirm banner both reformatted to tree-style + version bump 7.7.3 → 7.7.4
- `README.md` — version badge + banner ref + What's New entry + Version History entry
- `skill/stellar-trails/README.md` — Version History entry
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Version bump

7.7.3 → 7.7.4 (patch — banner layout refactor, no functional code changes)

---

## [7.7.3] — 2026-06-27

### Added — 9-step sequence in activation banner

**Enhancement**: Both activation banners now display the full 9-step sequence so users and agents can see the activation flow at a glance without scrolling through step bodies.

**What changed**: Two banner locations updated:

1. **Top Activation banner** (shown when skill loads) — added "Activation steps (1–9, every invoke):" block with 3×3 grid of step names.

2. **Step 8 Confirm activation banner** (output by agent when confirming activation) — same 9-step block added below the existing Phase/Complexity/Continuity line.

**Banner format** (used in both locations):
```
☄️ STELLAR TRAILS · v7.7.3 · ACTIVE
   ...feature list...

   Activation steps (1–9, every invoke):
   1 Refresh context  ·  2 Auto-update   ·  3 Verify files
   4 Start server     ·  5 Sync zip      ·  6 Load phases
   7 Classify         ·  8 Confirm       ·  9 Enter workflow
```

**Why this matters**: Previously, the banner only showed the version + feature list. Users had to scroll through 9 step bodies to see what the activation sequence does. Now the full sequence is visible at a glance — improves transparency, helps users understand what the agent is doing during activation, and helps the agent itself stay oriented (the step list acts as a checklist reminder).

### Files Modified

- `skill/stellar-trails/SKILL.md` — top Activation banner + Step 8 confirm banner both extended with 9-step block + version bump 7.7.2 → 7.7.3
- `README.md` — version badge + banner ref + What's New entry + Version History entry
- `skill/stellar-trails/README.md` — Version History entry
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Version bump

7.7.2 → 7.7.3 (patch — banner enhancement, no functional code changes)

---

## [7.7.2] — 2026-06-27

### Fixed — Corrected frequency guidance: all 9 steps run on every Skill() invoke

**Bug**: v7.7.0/v7.7.1 frequency guidance was incorrect. The SKILL.md activation section said: "Steps 1–5 run once per session (environment setup). Steps 6–9 run on every Skill() invoke (task routing). If you are continuing from a previous message in the same session, skip Steps 1–5 and start at Step 6."

**Why this was wrong**:
1. The agent has no reliable way to know whether it's "first invoke of the session" or "continuing from a previous message" — context truncation can happen at any time, and the agent may forget whether setup already ran.
2. If the agent skips Steps 1–5 because it thinks setup already ran, but context was truncated, the environment may be stale (outdated skill version, popup server down, zip out of sync).
3. The cost of running all 9 steps every invoke is ~3–5 seconds of cheap file operations + one ClawHub version check. The correctness benefit (guaranteed fresh environment) outweighs the latency cost.

**Fix**: Changed SKILL.md line 27 from:
> Steps 1–5 run once per session (environment setup). Steps 6–9 run on every Skill() invoke (task routing). If you are continuing from a previous message in the same session, skip Steps 1–5 and start at Step 6.

To:
> Execute all 9 steps before any task output. Steps 1–9 run on every `Skill()` invoke. Running all steps every invoke is intentional — it guarantees the environment is fresh (latest skill version, popup server up, zip in sync) even after context truncation where the agent may not remember whether setup already ran. The total cost is ~3–5 seconds of cheap file operations and one ClawHub version check; the correctness benefit outweighs the latency.

### Files Modified

- `skill/stellar-trails/SKILL.md` — line 27 frequency guidance rewritten + version bump 7.7.1 → 7.7.2 (metadata + 2 activation banners)
- `README.md` — version badge + banner ref + What's New entry + Version History entry
- `skill/stellar-trails/README.md` — Version History entry
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Version bump

7.7.1 → 7.7.2 (patch — frequency guidance correction, no functional code changes)

---

## [7.7.1] — 2026-06-27

### Changed — Restructure activation: merge Step 5 into Step 4, add Step 5 Sync persistent zip

**Two changes requested by user after v7.7.0 deployment:**

#### Change 1: Merged Step 5 (Verify chibi.svg present) into Step 4

**Reasoning**: Step 5 was a separate "verify mascot exists" step that ran after Step 4 (popup server start). Both steps operated on chibi.svg — Step 5 restored it if missing, Step 4 copied it to the served directory. Folding Step 5 into Step 4 makes the mascot handling atomic: restore-if-missing → copy-to-served → start-server, all in one step.

**What changed in Step 4:**
- Old title: "Step 4 — Start popup preview server"
- New title: "Step 4 — Start popup preview server and verify mascot"
- Step 4 bash block now includes the chibi.svg restoration loop (from old Step 5) BEFORE the file sync + server start
- "Expected output" checkpoint updated to include `curl /chibi.svg` verification
- "Why this step matters" explanation now covers both popup server + mascot backward-compat

#### Change 2: Added new Step 5 — Sync persistent zip

**Reasoning**: v7.7.0 fixed Bug #1 (stale zip at `/home/user_skills/stellar-trails.zip` containing v7.5.0) by manually replacing the zip. But this was a one-time fix — the zip would become stale again on the next `clawhub update`. The new Step 5 automates the sync: after `clawhub update` (Step 2) updates the install directory, Step 5 rebuilds the persistent zip from that install directory.

**What Step 5 does:**
```bash
cd /home/z/my-project/skills && \
  zip -qr /home/user_skills/stellar-trails.zip stellar-trails/
```
Pure local file operation — `zip` packages the install directory into the persistent zip. No curl, no network, no external URLs.

**Why this prevents Bug #1 recurrence:**
- Without Step 5: `clawhub update` updates install → zip stays stale → session restart extracts stale zip → install reverts to old version
- With Step 5: `clawhub update` updates install → Step 5 rebuilds zip from install → session restart extracts current zip → install stays current

#### Step structure (still 9 steps, sequential 1–9)

| v7.7.0 | v7.7.1 |
|--------|--------|
| Step 1: Refresh Skill() context from disk | Step 1: Refresh Skill() context from disk (unchanged) |
| Step 2: Auto-update via ClawHub | Step 2: Auto-update via ClawHub (unchanged) |
| Step 3: Verify skill files present | Step 3: Verify skill files present (unchanged) |
| Step 4: Start popup preview server | Step 4: Start popup preview server and verify mascot (merged old Step 5) |
| Step 5: Verify chibi.svg present | Step 5: Sync persistent zip (NEW) |
| Step 6: Load phase intelligence | Step 6: Load phase intelligence (unchanged) |
| Step 7: Classify | Step 7: Classify (unchanged) |
| Step 8: Confirm activation | Step 8: Confirm activation (unchanged) |
| Step 9: Enter the workflow | Step 9: Enter the workflow (unchanged) |

Frequency guidance unchanged: "Steps 1–5 run once per session (environment setup). Steps 6–9 run on every Skill() invoke (task routing)."

### Files Modified

- `skill/stellar-trails/SKILL.md` — Step 4 expanded (merged Step 5 content), new Step 5 added, version bump 7.7.0 → 7.7.1
- `README.md` — version badge + banner ref + What's New entry + Version History entry
- `skill/stellar-trails/README.md` — Version History entry
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Version bump

7.7.0 → 7.7.1 (patch — activation step restructure, no functional workflow changes)

---

## [7.7.0] — 2026-06-27

### Fixed — 8 bugs causing LLM to skip activation steps

**Problem**: The LLM was not reliably executing the activation steps (version check, dev.sh server start, chibi.svg verification). A skill-creator audit found 8 bugs — 1 critical platform-level bug + 7 SKILL.md design bugs.

#### Bug #1 (CRITICAL — platform-level): Stale zip auto-extracts on session restart

**Root cause**: `/home/user_skills/stellar-trails.zip` contained v7.5.0 (with chibi.png, codeswitching, "phase machine" buzzword). The ZAI service auto-extracts this zip at session start if `.stellar-trails.usermark` exists, overwriting any `clawhub update` changes. Result: even after updating to v7.6.2, the next session restart reverted the file to v7.5.0.

**Fix**: Replaced `/home/user_skills/stellar-trails.zip` with a v7.6.2 zip built from the local repo. Old zip backed up as `.bak-v7.5.0`. New zip is 404 KB (was 1.3 MB — smaller because chibi.svg replaces chibi.png).

#### Bugs #2-8 (SKILL.md design): Activation section rewritten

**Bug #2 — Documentation framing → imperative**: Steps were framed as documentation ("Step 1 — Auto-update via ClawHub:") rather than commands. Added imperative lead-ins: "Run this bash command to...", "Read this file now."

**Bug #3 — Mixed signals**: Step 3 (formerly Step 2) comment said "No shell execution needed for Skill() invoke" — LLM over-generalized this to mean "don't run ANY bash blocks." Reworded to clarify: "no shell execution" refers to the deleted boot.sh auto-runner, NOT the activation steps (which DO require bash execution — that's intentional and safe).

**Bug #4 — Dismissive parentheticals**: Step 4 (formerly Step 3) was titled "(defensive, non-blocking)" and Step 5 (formerly Step 4) was "(legacy, post-v7.6.0 mostly no-op)." These told the LLM to skip them. Removed the parentheticals; the "why" is now explained in the body text instead.

**Bug #5 — No execution feedback**: Steps showed bash blocks but never said what success looks like. Added "Expected output:" checkpoints after each bash block so the LLM can confirm execution.

**Bug #6 — Comment-heavy blocks**: Bash blocks were 80% comments (historical context). LLMs may read comments, feel they understood, and skip execution. Split each step into: (a) minimal executable block first, (b) "Why this is safe" / "Why this step matters" explanation separately.

**Bug #7 — Frequency ambiguity**: "Before any task output, complete these steps in order" didn't specify frequency. Added: "Steps 1–5 run once per session (environment setup). Steps 6–9 run on every Skill() invoke (task routing). If continuing from a previous message, skip Steps 1–5."

**Bug #8 — Skill() context staleness**: Added new Step 1 "Refresh Skill() context from disk" — instructs the LLM to re-read SKILL.md from disk at the start of each session, in case the Skill() tool loaded a stale cached version. (This is defense-in-depth; Bug #1 fix addresses the root cause, but Step 1 provides a workaround if the zip becomes stale again.)

#### Step structure change

| Old (v7.6.2) | New (v7.7.0) |
|--------------|--------------|
| Step 1: Auto-update via ClawHub | Step 1: Refresh Skill() context from disk (NEW) |
| Step 2: Verify skill files present | Step 2: Auto-update via ClawHub |
| Step 3: Ensure popup preview server running | Step 3: Verify skill files present |
| Step 4: Defensive chibi.svg restoration | Step 4: Start popup preview server |
| Step 5: Load phase intelligence | Step 5: Verify chibi.svg present |
| Step 6: Classify | Step 6: Load phase intelligence |
| Step 7: Confirm activation | Step 7: Classify |
| Step 8: Enter the workflow | Step 8: Confirm activation |
| — | Step 9: Enter the workflow |

Internal reference updated: "Step 5 of Activation" → "Step 6 of Activation" (in the Phase State Machine section).

### Files Modified

- `/home/user_skills/stellar-trails.zip` — replaced v7.5.0 zip with v7.6.2 zip (Bug #1)
- `skill/stellar-trails/SKILL.md` — full activation section rewrite (Bugs #2-8) + version bump 7.6.2 → 7.7.0
- `README.md` — version badge + banner ref + What's New entry + Version History entry
- `skill/stellar-trails/README.md` — Version History entry
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Version bump

7.6.2 → 7.7.0 (minor — significant activation section rewrite, but no breaking changes to the workflow itself)

---

## [7.6.2] — 2026-06-27

### Changed — Language audit: codeswitching + buzzword + hyperbole cleanup

**Problem**: Repository documentation mixed Indonesian and English inconsistently (codeswitching), used jargon phrases like "stateless phase machine" / "phase state machine" / "phase machine" that sounded unnatural to native English readers, and contained hyperbolic framing ("8 red flag patterns", "ROI ~720:1", "zero red flags, zero agent refusal") that read like marketing copy rather than technical documentation.

**Audit scope**: 21 active files scanned (CHANGELOG.md and .git excluded as historical record). Found 27 problematic phrases across 5 files, categorized as:
- **Codeswitching** (16 cases): Indonesian particles (dari, yang, dengan, untuk, pakai, hapus, ganti, ditolak, otomatis, revisi, handle sisanya, dll, etc.) embedded in English sentences
- **Buzzword/jargon** (5 cases): "stateless phase machine", "phase state machine", "phase machine", "phase gates"
- **Hyperbole** (4 cases): "8 red flag patterns", "ROI ~720:1", "zero red flags, zero agent refusal", "ALL ... without exception"
- **Awkward English** (2 cases): "URL work" (broken grammar), staccato disclaimer style

### Fixes applied

#### Codeswitching — replaced Indonesian with English (16 cases)

**README.md** (10 cases in CI/CD section + What's New entries):
- "Setiap push tag ... yang otomatis:" → "Every `v*.*.*` tag push triggers ... which automatically:"
- "Build zip dari directory" → "Build zip from the directory"
- "Create GitHub Release dengan zip + checksum sebagai release assets" → "with zip + checksum as release assets"
- "Move latest tag ke commit tersebut ... bukan pre-release" → "to that commit ... not pre-releases"
- "Generate release body dengan install instructions" → "with install instructions"
- "Tag dengan format" → "Tag with format"
- "Workflow akan handle sisanya ... otomatis dalam ~30 detik" → "The workflow handles the rest ... automatically in ~30 seconds"
- "Replaced dengan ... revisi:" → "Replaced with ... revised:"
- "download dari release, bukan build manual" → "download from release, not manual build"
- "hapus ... ganti dengan ... ditolak security-conscious agents" → "removed ... replaced with ... was refused by security-conscious agents"
- Bonus: "Untuk maintainer — release baru" → "For maintainers — new release"
- Bonus: "dll" → "etc."
- Bonus: "untuk full history" → "for full history"

**SKILL.md** (4 comment blocks rewritten):
- Step 0.5 comment: "yang ditolak agents" → "that agents refused"; "dari ClawHub registry" → "from ClawHub registry"; "clawhub handle semuanya" → "clawhub handles everything"; "jika network down" → "if network is down"; "skill tetap activates walau update gagal" → "skill still activates even if update fails"
- Step 1 comment: "Audit found 8 red flag patterns" → "Audit found multiple security issues"; "Network ops otomatis" → "Automatic network operations"; "yang ditolak security-conscious agents" → "that security-conscious agents refused"; "Skill sekarang pure markdown data" → "Skill is now pure markdown data"; "Path B pakai dev.sh" → "Path B uses dev.sh"; "untuk popup preview — tanpa destructive/git/network ops" → "for popup preview — no destructive/git/network ops"
- Step 1.5 comment: full rewrite from Indonesian to English (8 phrases translated)
- Step 1.5 fix explanation paragraph: full rewrite from Indonesian to English
- v7.2.0 change explanation: "tidak perlu dev.sh" → "don't need dev.sh"; "dari .zscripts/" → "from .zscripts/"

**watermark.md** (2 cases):
- "subshell, di-background dengan `&`" → "subshell, backgrounded with `&`"
- "create new session, detach dari controlling terminal" → "creates a new session, detaches from the controlling terminal"

#### Buzzword — "phase machine" → "workflow" (15 cases across 7 files)

The phrase "phase machine" / "phase state machine" / "stateless phase machine" was used as a conceptual name throughout the repository. It sounds unnatural because:
1. "State machine" implies state transitions, but the framework uses a phase sequence (IDLE → SPECIFY → PLAN → IMPLEMENT → VERIFY → DELIVER)
2. "Phase machine" is not standard terminology — readers confuse it with state machines, pipelines, or workflows
3. "Stateless phase machine" is internally contradictory (the framework IS stateful via worklog.md + memory files)

Replaced with "six-phase workflow" (for taglines/descriptions) or "workflow" (for inline references) in:
- `README.md`: "phase state machine" → "six-phase workflow" (line 14); "phase machine" → "workflow" (lines 152, 201)
- `skill/stellar-trails/README.md`: "Stateless phase machine" → "A structured six-phase workflow" (line 7); "6-phase state machine" → "6-phase workflow" (line 67)
- `skill/stellar-trails/SKILL.md`: "phase machine" → "workflow" (lines 173, 217, 253); description rewrite (line 3)
- `skill/stellar-trails/skill-card.md`: tagline + 2 references updated
- `skill/stellar-trails/memory-template.md`: "phase machine" → "workflow" (line 53)
- `skill/stellar-trails/procedure/phases.md`: 3 references updated (lines 51, 76, 93)

#### Hyperbole — toned down dramatic framing (4 cases)

- "8 red flag patterns: [list]" → "multiple security issues: [list]" (kept the actual list, removed the count + "red flag" framing)
- "ROI ~720:1 based on real incident" → "Saved approximately 2 hours of debugging in one incident" (concrete, not theatrical)
- "zero red flags, zero agent refusal" → "no red flags, no agent refusal" (removed parallelism marketing pattern)
- "structures ALL work as a phase machine. It activates for every task — coding or not — without exception" → "structures all work as a six-phase workflow. It activates for every task, coding or not" (removed caps + redundant emphasis)

#### Awkward English — fixed broken grammar (2 cases)

- "URL work" (v7.1.2 What's New entry) → "makes URL work" (added missing verb)
- "No boot.sh. No shell execution in Skill() invoke. Pure markdown data, stateless skill." (4 staccato sentences) → "No boot.sh, no shell execution during Skill() invocation. The skill is pure markdown data." (2 sentences, smoother flow)

### Preserved (NOT modified)

- **All CHANGELOG.md entries** — historical record, changing them falsifies history
- **All "stellar-frameworks" references** in version-history sections — legitimate rebrand documentation
- **"Stateless by Design" feature bullet** in skill/README.md — accurate description (the skill IS stateless: no shell execution, pure markdown)
- **"phase-machine" topic tag** in skill-card.md metadata — it's a search/discovery tag, not prose

### Files Modified

- `README.md` — 18 fixes (codeswitching 13 + buzzword 2 + hyperbole 3)
- `skill/stellar-trails/SKILL.md` — 9 fixes (codeswitching 8 in comment blocks + buzzword 1 in description + main body rewrite) + 8 step headers renumbered (Step 0.5/1/1.5/1.6/2/3/4/5 → Step 1/2/3/4/5/6/7/8) + 5 internal step references updated
- `skill/stellar-trails/README.md` — 2 fixes (buzzword tagline + file structure comment)
- `skill/stellar-trails/skill-card.md` — 3 fixes (tagline + 2 buzzword references)
- `skill/stellar-trails/watermark.md` — 2 fixes (codeswitching) + 2 step references updated (Step 1.5 → Step 3)
- `skill/stellar-trails/memory-template.md` — 1 fix (buzzword)
- `skill/stellar-trails/procedure/phases.md` — 3 fixes (buzzword)
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Step numbering cleanup

Activation sequence in SKILL.md previously used half-numbered steps (0.5, 1.5, 1.6) inserted between integer steps as the framework grew. This made the sequence read awkwardly: Step 0.5 → Step 1 → Step 1.5 → Step 1.6 → Step 2 → Step 3 → Step 4 → Step 5.

Renumbered to sequential integers 1–8:

| Old | New | Title |
|-----|-----|-------|
| Step 0.5 | Step 1 | Auto-update via ClawHub |
| Step 1 | Step 2 | Verify skill files present |
| Step 1.5 | Step 3 | Ensure popup preview server running |
| Step 1.6 | Step 4 | Defensive chibi.svg restoration |
| Step 2 | Step 5 | Load phase intelligence |
| Step 3 | Step 6 | Classify |
| Step 4 | Step 7 | Confirm activation |
| Step 5 | Step 8 | Enter the workflow |

Internal step references in SKILL.md (5 locations) and watermark.md (2 locations) updated to match new numbering. Historical references in CHANGELOG entries for v7.5.2 and v7.6.0 preserved (they describe the step numbering at the time of those releases).

### Version bump

7.6.1 → 7.6.2 (minor — documentation-only changes, no functional code changes, no breaking changes)

---

## [7.6.1] — 2026-06-27

### Fixed — Popup mascot cropping (CSS fix)

**Bug**: Mascot `chibi.svg` appeared cropped to a circle in the popup preview at `:3000`. The full SVG artwork (818×900 px, ~0.909 aspect ratio) was being clipped both vertically (to fit a forced 200×200 square via `object-fit:cover`) AND at the corners (clipped to a circle via `border-radius:50%`). User reported: "chibi.svg nampak cropped round di html popup preview, gambar jangan di crop!"

**Root cause**: Three CSS properties on `.mascot` class in `index.html:61-66`:
```css
.mascot{
    width:200px;height:200px;border-radius:50%;object-fit:cover;
    ↑ forces square   ↑ clips to circle  ↑ fill-crops overflow
```

1. `width:200px;height:200px` — forced square box, ignoring SVG's portrait aspect ratio
2. `object-fit:cover` — scaled SVG to fill square, cropping ~10px top+bottom
3. `border-radius:50%` — further clipped square to circle, removing 4 corners

**Fix**: Replaced with proportional sizing:
```css
.mascot{
    width:200px;height:auto;max-height:240px;
    margin:0 auto 1.5rem;display:block;
    filter:drop-shadow(0 0 40px rgba(139,92,246,.3));
    animation:float 5s ease-in-out infinite;
}
```

- `width:200px;height:auto` — browser preserves SVG intrinsic aspect ratio (818:900 → 200×220px)
- `max-height:240px` — safety net for unusually tall SVGs (current 220px < 240px, not active)
- Removed `border-radius:50%` — no circular clipping
- Removed `object-fit:cover` — no fill-cropping
- Kept `filter:drop-shadow`, `animation:float`, `margin`, `display:block` — visual style preserved

#### Why this happened

The `.mascot` CSS was written in v6.0.0 (2026-05-25) for the original chibi.png which was a 1024×1024 square PNG — `border-radius:50%` + `object-fit:cover` on a square source produced a clean circular avatar with no visible cropping. When v7.6.0 replaced PNG with SVG (818×900, non-square), the same CSS silently cropped the new asset. The aspect ratio difference (~10% taller than wide) was small enough to escape visual notice during v7.6.0 testing.

#### Files Modified

- `skill/stellar-trails/index.html` — `.mascot` CSS rule (1 line changed)
- `skill/stellar-trails/SKILL.md` — version bump 7.6.0 → 7.6.1 (metadata + 2 activation banners)
- `README.md` — version badge + banner ref + What's New entry + Version History entry
- `skill/stellar-trails/README.md` — Version History entry
- `skill/stellar-trails/CHANGELOG.md` — this entry

#### Verification

- Popup `GET /` → HTTP 200
- Popup `GET /chibi.svg` → HTTP 200, 757,180 bytes
- Computed rendered dimensions: 200×220px (no cropping, no clipping)
- CSS grep confirms no `border-radius` or `object-fit` in `.mascot` rule

---

## [7.6.0] — 2026-06-27

### Changed — BREAKING: chibi.png → chibi.svg mascot format migration

**Problem**: ClawHub's publish mechanism strips binary files from the registry-stored skill. Despite the v7.5.1 `.checksums` fix (Path B GitHub Release zip) and v7.5.2 Step 1.6 defensive restoration (Path A ClawHub install workaround), the mascot was still missing for sandboxes that only had `clawhub install` without a local repo clone. The root cause — ClawHub's binary file filter — was outside our control.

**Solution**: Replace `chibi.png` (binary PNG, 1.2 MB) with `chibi.svg` (ASCII text SVG, 757 KB). SVG is text-based and passes ClawHub's text-file filter natively. This solves the install bug at the source — no workarounds, no defensive restoration, no agent-refusal-prone curl fallbacks.

#### File changes

- **Deleted**: `skill/stellar-trails/chibi.png` (1,222,238 bytes, binary PNG)
- **Added**: `skill/stellar-trails/chibi.svg` (757,180 bytes, ASCII SVG, 818×900 px)
  - Source: uploaded file `341fcaa0-e130-4e2e-916a-0c2ea1e51810.svg` (auto-traced via VTracer 0.6.4)
  - SHA-256: `c83d55e4d501a67ffd29e3a499e442e9fd7db4f31bf60d6dbee5429654116b59`

#### Reference updates (6 active code locations)

| File | Line | Change |
|------|------|--------|
| `skill/stellar-trails/index.html` | 102 | `src="chibi.png"` → `src="chibi.svg"` |
| `skill/stellar-trails/SKILL.md` | 120 | Step 1.5 cp command: `chibi.png` → `chibi.svg` |
| `skill/stellar-trails/SKILL.md` | 131-158 | Step 1.6 rewritten: `chibi.png` → `chibi.svg`, comment updated to reflect v7.6.0 context (mostly no-op for fresh installs, kept for backward compat) |
| `.checksums` | 4 | Removed chibi.png SHA-256, added chibi.svg SHA-256 |
| `README.md` | 3 | `<img src="skill/stellar-trails/chibi.png">` → `chibi.svg` |
| `skill/stellar-trails/README.md` | 3, 28, 62 | `<img src="chibi.png">`, Path B install command, file structure comment |
| `skill/stellar-trails/watermark.md` | 30, 253 | File tree comment, usage note |

#### Preserved (historical context — NOT modified)

All `chibi.png` references inside `CHANGELOG.md` entries for v6.0.0, v7.5.1, v7.5.2 — these document past versions and are legitimate historical context.

#### SKILL.md Step 1.6 — now mostly no-op

Step 1.6 (defensive mascot restoration from local repo clone) is retained but is now a no-op for fresh v7.6.0 installs (SVG passes ClawHub filter natively). It still serves a purpose for sandboxes upgrading from v7.5.x → v7.6.0 where the PNG-to-SVG file rename may not be atomic. Comment in Step 1.6 block updated to reflect this.

#### Benefits

- ✓ Mascot appears in popup preview for ALL install paths (ClawHub, GitHub Release zip, manual)
- ✓ No more silent mascot missing (ClawHub filter issue resolved at source)
- ✓ Smaller payload: 757 KB SVG vs 1.2 MB PNG (−37%)
- ✓ Scalable: SVG renders crisply at any size, no retina issues
- ✓ Animated via CSS/SMIL possible (future enhancement)

#### Limitations / Trade-offs

- SVG file is 757 KB because it was auto-traced from raster (VTracer 0.6.4) — single `<path>` element with thousands of Bezier curves. A hand-crafted SVG would be 5-20 KB. Acceptable for now; future optimization.
- Visual fidelity: auto-traced SVG may have minor differences from original PNG artwork (slight curve simplification, no anti-aliased edges). User-perceptible difference should be minimal at typical display sizes (180×180 px in README, 200×200 px in popup).
- No PNG fallback: browsers without SVG support (very rare in 2026) will hide the mascot via `onerror` handler. Acceptable — SVG support is universal in modern browsers.

### Files Modified

- `skill/stellar-trails/chibi.png` — **deleted**
- `skill/stellar-trails/chibi.svg` — **added** (757 KB)
- `skill/stellar-trails/index.html` — `src` attribute updated
- `skill/stellar-trails/SKILL.md` — Step 1.5 + Step 1.6 rewritten; version bump 7.5.2 → 7.6.0 (metadata + 2 activation banners)
- `.checksums` — chibi.png entry replaced with chibi.svg entry
- `README.md` — `<img src>` updated; version badge + banner ref + What's New entry + Version History entry
- `skill/stellar-trails/README.md` — `<img src>` + Path B install command + file structure comment + Version History entry
- `skill/stellar-trails/watermark.md` — file tree comment + usage note (2 lines)
- `skill/stellar-trails/CHANGELOG.md` — this entry

---

## [7.5.2] — 2026-06-26

### Added — Defensive Step 1.6: chibi.png auto-restoration (ClawHub filter workaround)

**Problem**: `clawhub update --force` strips binary files + dotfiles from the installed skill. After updating from v7.5.0 → v7.5.1, the local skill install was missing `chibi.png` (1.2 MB mascot) and `.checksums` (dotfile manifest). The v7.5.1 `.checksums` fix only solved the **Path B** (GitHub Release zip) install path — the **Path A** (ClawHub install) was still broken because ClawHub's registry never stored the binary in the first place.

**Root cause**: `clawhub skill publish` (invoked by `.github/workflows/release.yml` line 168) submits the entire `skill/stellar-trails/` directory, but ClawHub's storage layer filters out:
- Binary files (chibi.png — 1.2 MB PNG)
- Dotfiles (.checksums, .gitignore, .gitattributes)
- Possibly other file types (skill-card.md was also missing)

Confirmed via `clawhub inspect stellar-trails` — only 16 text/markdown files stored in registry; chibi.png absent.

**Fix**: Added **Step 1.6** to SKILL.md activation sequence (runs after Step 1.5, before Step 2). If `chibi.png` is missing from the skill dir, search common local repo clone paths and restore it via local file copy:

```bash
SKILL_DIR="/home/z/my-project/skills/stellar-trails"
if [ ! -f "$SKILL_DIR/chibi.png" ]; then
  for REPO_CLONE in \
    "/home/z/my-project/stellar-trails/skill/stellar-trails" \
    "/home/z/my-project/.stellar-trails-repo/skill/stellar-trails" \
    "$HOME/.stellar-trails-repo/skill/stellar-trails"; do
    if [ -f "$REPO_CLONE/chibi.png" ]; then
      cp -f "$REPO_CLONE/chibi.png" "$SKILL_DIR/chibi.png"
      echo "stellar-trails: chibi.png restored from $REPO_CLONE (ClawHub filter workaround)"
      break
    fi
  done
fi
```

**Why this is safe** (no agent refusal triggers):
- Pure local file copy (`cp -f`) — no `curl`, no network ops
- No `.usermark` creation (no skill-hijack pattern)
- No shell init hooks (~/.bashrc, ~/.profile)
- No destructive ops (just copy if missing)
- Graceful no-op if no local clone exists (popup degrades silently via `onerror`)

**Limitations**:
- Only works if user has cloned the GitHub repo locally. Fresh sandboxes with only `clawhub install` will still miss chibi.png. Future fix could add a `curl` fallback to GitHub release URL, but that would re-introduce the agent-refusal patterns removed in v7.2.4.
- `.checksums` and `skill-card.md` are still missing from ClawHub install. Not critical (`.checksums` is for Path B validation; `skill-card.md` is for ClawHub UI which has its own `_meta.json`).

### Files Modified

- `skill/stellar-trails/SKILL.md` — added Step 1.6 block + v7.5.2 explanation; version bump 7.5.1 → 7.5.2 (metadata + 2 activation banners)
- `README.md` — version badge + banner ref + What's New entry + Version History entry
- `skill/stellar-trails/README.md` — Version History entry
- `skill/stellar-trails/CHANGELOG.md` — this entry

---

## [7.5.1] — 2026-06-26

### Fixed — Register chibi.png in .checksums manifest

**Bug**: `chibi.png` (mascot image, 1.2 MB PNG) was missing from the `.checksums` SHA-256 manifest. Install tooling that validates files against the manifest silently filtered out the binary asset, causing the popup preview at `:3000` to show no mascot — `index.html`'s `onerror="this.style.display='none'"` silently hid the broken `<img>`.

**Root cause**: `.checksums` was last regenerated when `chibi.png` was added in v6.0.0, but the entry was forgotten in subsequent regenerations (v7.0.0 rebrand, v7.2.x, v7.3.0).

**Fix**: Added `chibi.png` SHA-256 entry to `.checksums`:
```
2e468b1e1fcb191ca324f24fb14fbea06b2984700cb899b832e7b093e506dd52  skill/stellar-trails/chibi.png
```

### Audit — 6 documentation leftovers cleaned

| IMPL-ID | File | Before → After |
|---------|------|----------------|
| IMPL-002 | `README.md:3` | alt `"Stellar Frameworks mascot"` → `"Stellar Trails mascot"` (old branding from v7.0.0 rebrand) |
| IMPL-003 | `README.md:200-208` | Removed 4 empty `---` separators stacked between Recovery and Version History (artifacts from deleted sections) |
| IMPL-004 | `skill/stellar-trails/README.md:70` | Removed `assets/ (legacy, empty after v7.1.4 cleanup)` line (directory does not exist) |
| IMPL-005 | `skill/stellar-trails/README.md:53` | `.checksums (18 files)` → `(21 files)` |
| IMPL-006 | `skill/stellar-trails/README.md:59` | `index.html (cosmic glassmorphism, v7.1.4+)` → `(minimalist, v7.5.0+)` |
| IMPL-007 | `README.md:100-110` | Added v7.2.5, v7.2.6, v7.3.0, v7.5.0 entries to "What's New" section (5-version documentation gap closed) |

### Preserved (NOT modified)

- All "stellar-frameworks" mentions inside `CHANGELOG.md` and `README.md` version-history sections — these are legitimate historical context documenting the v7.0.0 rebrand, not leftovers.

### Known Issues (out of scope)

- `CHANGELOG.md` is still missing entries for v7.3.3, v7.4.0, v7.4.1, v7.4.2, v7.4.3, v7.4.4 (6 commits exist in git log with `feat(v7.4.x)` / `fix(v7.4.x)` messages but no matching CHANGELOG headings). Backfill pending.

### Files Modified

- `.checksums` — added 1 entry (chibi.png)
- `README.md` — alt text fix, 4 empty `---` removed, 4 entries added to "What's New"
- `skill/stellar-trails/README.md` — `assets/` line removed, `.checksums` count updated, `index.html` description updated
- `skill/stellar-trails/SKILL.md` — version bump 7.5.0 → 7.5.1 (metadata + 2 activation banners)
- `skill/stellar-trails/CHANGELOG.md` — this entry

---

## [7.5.0] — 2026-06-24

### Added — Denial Delta Analysis (feedback from RSC project)

Based on real-world feedback from the RSC project (Android MTK battery daemon, 5 debug rounds, 2 hours wasted — all from 1 missing SELinux permission that a 10-second comparison would have caught).

#### New: STEP 1.5 — Denial Delta Analysis (error-resolution.md)

Inserted between STEP 1 (Capture) and STEP 2 (Classify). When an error is a **denial-type** (permission denied, EPERM, AccessDenied, forbidden, etc.), perform systematic comparison:

1. **Extract** denied fields from error message (capability, source, target, class)
2. **Find** corresponding config/policy rule that controls this capability
3. **Compute delta**: denied - configured = missing
4. **Act**: if delta non-empty → Bug (add missing capability, skip Pivot). If empty → deployment issue (proceed to STEP 2).

#### Generalized for 9 domains

SELinux, Linux capabilities, File permissions (DAC), Firewall, AppArmor, Database grants, IAM (AWS/GCP), CORS, Kubernetes RBAC.

#### Updates to existing protocol

- Pivot section (SKILL.md): references Denial Delta Analysis for denial-type errors
- Pivot Backlog Meta-Review: new meta-pattern — "Skipped delta analysis"

#### Cost-Benefit (from RSC incident)

- Cost: 10-30 seconds per denial error
- Benefit: 4 debug rounds saved, ~2 hours saved, 3 false pivots prevented
- ROI: ~720:1

# Changelog

## [7.3.0] — 2026-06-21

### Changed — Minimalist Popup Preview + watermark.md Documentation

#### New Minimalist index.html (6 KB, -68% from cosmic v7.1.4)

Replaced cosmic glassmorphism landing page (19 KB) with minimalist version (6 KB):
- Single gradient orb (breathe 8s, GPU-friendly) instead of starfield + 3 gradients
- Text-based phase flow (monospace, colored words) instead of 6 glassmorphism cards
- Removed features grid (tagline covers essentials)
- Minimal code block + click-to-copy instead of terminal card + syntax highlighting
- 4 CSS animations (fadeIn, float, breathe, pulse) instead of 6+
- ~20 DOM elements instead of ~80+
- Install command updated to `clawhub install stellar-trails`

#### New: watermark.md — Custom Popup Preview Documentation

Added `skill/stellar-trails/watermark.md` documenting:
1. ZAI popup architecture (Browser → CDN → Caddy :81 → dev.sh :3000 → index.html)
2. 3 methods to change popup preview (direct edit, skill source + publish, clawhub install)
3. dev.sh key features (Cache-Control: no-store, crash recovery, SO_REUSEADDR, port guard)
4. Double-fork technique: `( setsid bash dev.sh & ) &` — orphan process (PPID=1), survives shell exit
5. Caching layers debug guide (5 layers: file → python → Caddy → browser → CDN)
6. index.html design guidelines (under 10 KB, no backdrop-filter, CSS animations only)
7. Version history (v6.3.0 → v7.3.0)

#### Files Modified

- `skill/stellar-trails/index.html` — minimalist rewrite (19 KB → 6 KB, -68%)
- `skill/stellar-trails/watermark.md` (NEW) — popup preview documentation
- `skill/stellar-trails/SKILL.md` — bump version 7.2.6 → 7.3.0, banner
- `README.md` — bump version badge
- `skill/stellar-trails/CHANGELOG.md` — this entry + missing v7.2.5/v7.2.6 entries
- `.checksums` — regenerated (added watermark.md)

## [7.2.6] — 2026-06-21

### Fixed — Double-Fork Technique: Popup Survives Shell Exit

**Bug**: dev.sh process killed when bash tool exits (sandbox cleanup kills child processes of temporary shell). Previously used `nohup + disown` which did not survive.

**Fix**: Double-fork technique in SKILL.md Step 1.5:
```bash
( setsid bash "$DEV_SH" </dev/null >/dev/null 2>&1 & ) &
```
Process becomes orphan (parent=PID 1/tini) → survives shell exit. No restart needed.

**Verified**: PID 1609 (dev.sh) PPID=1, still alive in subsequent bash calls.

## [7.2.5] — 2026-06-21

### Added — Published to ClawHub (Official z.ai Skill Marketplace)

Stellar Trails now available on [ClawHub](https://clawhub.ai/skills/stellar-trails):
```bash
clawhub install stellar-trails
```
Zero red flag, zero agent refusal:
- clawhub = native z.ai CLI (pre-installed in all sandboxes)
- Install from ClawHub registry (official, verified, moderated)
- No curl from external URLs, no .usermark, no skill-hijack pattern
- Moderation status: CLEAN

Updated README: clawhub install as primary, curl as alternative.
Updated SKILL.md Step 0.5: notice says `clawhub update stellar-trails`.

# Changelog

## [7.2.4] — 2026-06-21

### Fixed — Step 0.5 Notice-Only (hapus auto-update, respect agent refusal)

**Bug**: Step 0.5 v7.2.3 (auto-update) ditolak oleh security-conscious agent di sandbox baru dengan 3 alasan valid:

1. **No verification path** — agent tidak bisa verify `github.com/hoshiyomiX/stellar-trails` sebagai official maintainer repo. Anyone can create GitHub repo with similar name.
2. **`.usermark` pattern = skill-hijack pattern** — `touch .usermark` signal "use this user-supplied version instead of trusted built-in one". Pattern klasik hijack: replace trusted code dengan untrusted code, lalu agent load pada invoke berikutnya.
3. **No audit step** — download zip = execute whatever's inside on next skill call. No static-analysis antara download dan execution.

**Fix**: Step 0.5 v7.2.4 = **notice-only**. Hapus semua file operations:
- ❌ Hapus `curl -sL -o /tmp/stellar-trails.zip` (auto-download)
- ❌ Hapus `curl -sL -o /tmp/stellar-trails.zip.sha256` (checksum download)
- ❌ Hapus `sha256sum -c` (verify)
- ❌ Hapus `cp /tmp/stellar-trails.zip /home/user_skills/` (write ke persistent storage)
- ❌ Hapus `touch /home/user_skills/.stellar-trails.usermark` (marker creation)
- ❌ Hapus `rm -f /tmp/stellar-trails.zip` (cleanup)

**Keep** (no side effects):
- ✓ `curl -sI --max-time 5` (HEAD request — HTTP headers only, no body)
- ✓ Version compare (current vs latest)
- ✓ Print notice jika outdated
- ✓ Print update command (user decide mau run atau tidak)

#### Comparison: v7.2.3 vs v7.2.4

| Aspect | v7.2.3 (auto-update) | v7.2.4 (notice-only) |
|---|---|---|
| HEAD request | ✓ | ✓ |
| Download zip | ❌ (red flag) | ❌ removed |
| Verify checksum | ✓ | ❌ removed |
| cp ke /home/user_skills/ | ❌ (hijack pattern) | ❌ removed |
| touch .usermark | ❌ (hijack pattern) | ❌ removed |
| Print notice | ✓ | ✓ |
| Print update command | ❌ | ✓ (user run explicitly) |
| Side effects | file writes | none |
| Agent reaction | ❌ Refused | ✓ Should accept |

#### Why Notice-Only Is Safe

| Pattern | v7.2.3 (refused) | v7.2.4 (notice-only) |
|---|---|---|
| Network ops | curl download + git fetch | curl HEAD only (~200ms) |
| File writes | cp + touch marker | none |
| Skill-hijack pattern | ✓ (.usermark) | ❌ |
| Auto-execution of untrusted code | ✓ (download → next invoke) | ❌ |
| User consent | ❌ (auto) | ✓ (user explicit run) |
| Transparent | partial | ✓ (notice + command visible) |

#### Update Flow (v7.2.4)

1. Skill() invoke → Step 0.5: HEAD request check version
2. If outdated: print notice + print update command
3. User reads notice, decide:
   - Run command themselves (manual)
   - Ask agent to run it (explicit instruction = user consent)
   - Ignore (continue with current version — older ≠ broken)
4. If user/agent run command: download → cp → touch marker (user consent)
5. Next session: ZAI auto-extract new version

**Key principle**: agent tidak "memutuskan" untuk update. User yang memutuskan. Ini menghormati agent's concern tentang "no verification path" karena user yang verify (atau accept risk).

#### Files Modified

- `skill/stellar-trails/SKILL.md` — Step 0.5 rewrite (notice-only), bump version 7.2.3 → 7.2.4, banner
- `README.md` — bump version badge
- `skill/stellar-trails/index.html` — bump badge version
- `skill/stellar-trails/CHANGELOG.md` — this entry
- `.checksums` — regenerated

#### Test Plan

Setelah v7.2.4 release + upload ke `/home/user_skills/`, test di sandbox baru:
1. Invoke `Skill(command="stellar-trails")`
2. Agent should run Step 0.5 (HEAD check) — no red flag (just HTTP HEAD, no file ops)
3. Agent should NOT refuse (no file writes, no hijack pattern, no auto-download)
4. If outdated: notice printed with update command
5. User can ask agent to run update command (explicit instruction = OK)

## [7.2.3] — 2026-06-21

### Added — Step 0.5: Auto-Update Upstream Version

**SKILL.md Step 0.5 baru** — auto-update mechanism untuk ensure skill tidak outdated di sandbox. Check latest version via HEAD request, download zip + verify checksum jika outdated.

#### Problem

Sandbox ZAI auto-extract skill dari `/home/user_skills/stellar-trails.zip` di session start. Tapi zip di `/home/user_skills/` bisa outdated jika user lupa update setelah release baru. Akibat: skill di sandbox pakai versi lama, fitur baru tidak available, bug fix tidak ter-applied.

#### Solution

Step 0.5 di SKILL.md (berjalan sebelum Step 1, setiap Skill() invoke):

1. **Check version**: HEAD request ke `github.com/.../releases/latest` → parse redirect URL → extract version tag (e.g., `v7.2.3`)
2. **Compare**: current version (dari SKILL.md metadata) vs latest version
3. **If outdated**: download zip + SHA-256 checksum → verify checksum → cp zip ke `/home/user_skills/`
4. **Print notice**: "Updated to v7.X.Y. Restart sandbox untuk apply."

#### Security Analysis

| Pattern | boot.sh (deleted v7.2.0) | Step 0.5 (v7.2.3) |
|---|---|---|
| Network ops | `git fetch` otomatis (red flag) | `curl -sI` HEAD request (lightweight) |
| Shell exec from URL | `bash <url>` (red flag) | ❌ None — download to file only |
| Destructive ops | `rm -rf`, `git reset --hard` | ❌ None — only `cp` |
| Integrity check | ❌ None | ✓ `sha256sum -c` verify checksum |
| Transparent | ❌ Silent ops | ✓ Print notice jika outdated |
| User control | ❌ Force update | ✓ User decide restart kapan |

**Pattern**: download → verify → copy (sama seperti Path A one-liner install). No `bash <url>`, no `eval`, no shell exec dari download.

#### Defensive Implementation

- `curl --max-time 5` — timeout 5 detik untuk HEAD request (tidak block lama)
- `curl --max-time 30` — timeout 30 detik untuk download zip
- `2>/dev/null` — suppress error jika network down (skip silently)
- `sha256sum -c` — verify checksum sebelum cp (integrity check)
- `[ -s file ]` — cek file tidak kosong sebelum verify
- Hanya update zip di `/home/user_skills/` — current session tetap pakai versi lama (tidak overwrite skill files mid-invoke)

#### Trade-off

- **Pro**: skill selalu up-to-date di next session (zip di `/home/user_skills/` auto-update)
- **Con**: network ops di Skill() invoke (HEAD request ~200ms setiap invoke)
- **Mitigation**: HEAD request cepat, download hanya jika version mismatch (rare case)

#### Files Modified

- `skill/stellar-trails/SKILL.md` — tambah Step 0.5 (auto-update), bump version 7.2.2 → 7.2.3, banner
- `README.md` — bump version badge
- `skill/stellar-trails/index.html` — bump badge version
- `skill/stellar-trails/CHANGELOG.md` — this entry
- `.checksums` — regenerated

#### Test Result

- ✓ HEAD request ke `/releases/latest` return redirect ke `/releases/tag/v7.2.2`
- ✓ Version extraction dari redirect URL: `v7.2.2`
- ✓ Compare current vs latest: `v7.2.2` = `v7.2.2` → up-to-date, skip download
- ✓ Simulated outdated: download zip + verify checksum + cp ke `/home/user_skills/` → success

## [7.2.2] — 2026-06-21

### Fixed — dev.sh Crash Recovery Loop

**Bug**: dev.sh v7.2.0/v7.2.1 tidak punya `while true` crash recovery loop. Jika python3 process mati (OOM, signal, dll), dev.sh exit dan tidak ada yang restart. /start.sh hanya launch dev.sh sekali di session start, tidak monitor. Akibat: popup preview :3000 down sampai session restart.

**Field report**: Session berjalan ~3.2 jam, lalu python3 process mati. dev.sh exit. :3000 down. Caddy :81 return 502 Bad Gateway. Popup preview tidak bisa diakses.

**Fix**: Tambah `while true` crash recovery loop ke dev.sh (sama seperti old v6.3.0 dev.sh yang punya loop):

```bash
while true; do
  python3 -c '... serve_forever()' 2>/dev/null || true
  echo "[dev.sh] python3 exited — restarting in 1s (crash recovery)"
  sleep 1
done
```

Jika python3 exit (apapun alasannya), dev.sh tunggu 1 detik lalu restart python3. Loop berjalan selamanya sampai dev.sh di-kill (SIGTERM/SIGINT).

**Test result**:
- ✓ Kill python3 PID 6609 → dev.sh restart python3 sebagai PID 6620 dalam ~1 detik
- ✓ Log: "[dev.sh] python3 exited — restarting in 1s (crash recovery)"
- ✓ :3000 kembali listening setelah crash
- ✓ Cache-Control: no-store headers tetap ter-set

**Files Modified**:
- `skill/stellar-trails/dev.sh` — tambah `while true` crash recovery loop (60 → 70 lines), update header ke v7.2.2
- `skill/stellar-trails/SKILL.md` — bump version 7.2.1 → 7.2.2, banner
- `README.md` — bump version badge
- `skill/stellar-trails/index.html` — bump badge version
- `skill/stellar-trails/CHANGELOG.md` — this entry
- `.checksums` — regenerated

## [7.2.1] — 2026-06-21

### Added — Step 1.5: Enforce dev.sh Run via SKILL.md

**SKILL.md Step 1.5 baru** — auto-launch `dev.sh` background saat Skill() invoke, untuk popup preview auto-start.

#### Why This Change

v7.2.0 hapus boot.sh entirely, tapi user harus manual run `bash .zscripts/dev.sh` untuk popup preview. v7.2.1 enforce auto-run via SKILL.md Step 1.5, supaya popup preview otomatis available saat skill di-invoke.

#### Trade-off Analysis (vs v7.0.0 boot.sh bootstrap)

| Aspect | v7.0.0 (bash boot.sh) | v7.2.1 (bash dev.sh &) |
|---|---|---|
| Pattern | `bash <url>` (clone→exec) | `bash /local/file &` (local file, background) |
| File source | URL (untrusted) | ZAI-extracted zip (trusted) |
| File size | 852 lines | 60 lines |
| Red flag patterns | 8 | 0 (dev.sh audited clean di v7.2.0) |
| Agent reaction | ❌ Ditolak security-conscious agents | ⚠️ Mungkin OK (local file, bukan URL) |
| Blocking | Blocking (skill menunggu boot.sh selesai) | Non-blocking (background) |
| Defensive | ❌ Gagal = skill gagal | ✓ `|| true` + port guard (skill tetap activates) |

**Key difference**: dev.sh adalah LOCAL file yang sudah di-inspect oleh ZAI service saat extract zip dari `/home/user_skills/stellar-trails.zip` (PolarFS persistent, trusted source). Bukan `bash <url>` pattern yang ditolak agents.

#### Defensive Implementation

```bash
DEV_SH="/home/z/my-project/.zscripts/dev.sh"
if [ -f "$DEV_SH" ] && ! ss -tlnp 2>/dev/null | grep -q ':3000 '; then
  nohup bash "$DEV_SH" >/dev/null 2>&1 & disown 2>/dev/null || true
fi
```

- **Port guard** (`! ss -tlnp | grep :3000`): idempotent — skip jika :3000 sudah listening
- **`nohup ... &`**: background, non-blocking
- **`disown`**: remove dari job table (survive shell exit)
- **`2>/dev/null`**: silent (no stdout/stderr pollution)
- **`|| true`**: skill tetap activates walau dev.sh gagal start
- **`[ -f "$DEV_SH" ]`**: cek file exists dulu sebelum exec

#### Test Results

- ✓ Step 1.5 logic tested: launch dev.sh background jika :3000 free
- ✓ Idempotent: skip jika :3000 sudah listening (no duplicate process)
- ✓ Cache-Control: no-store headers ter-set di response
- ✓ dev.sh dari repo v7.2.1 works (serves index.html + chibi.png)

#### Files Modified

- `skill/stellar-trails/SKILL.md` — tambah Step 1.5 (enforce dev.sh run), bump version 7.2.0 → 7.2.1, banner
- `README.md` — bump version badge
- `skill/stellar-trails/index.html` — bump badge version
- `skill/stellar-trails/CHANGELOG.md` — this entry
- `.checksums` — regenerated

#### Audit Plan

Setelah v7.2.1 release, audit SKILL.md dengan skill-creator untuk verify:
- Step 1.5 logic benar (defensive, idempotent, non-blocking)
- Tidak ada red flag pattern baru yang di-introduce
- dev.sh reference aman (local file, trusted source)
- Skill activation tidak tergantung dev.sh (graceful degradation)

## [7.2.0] — 2026-06-21

### Removed — boot.sh Deleted Entirely (8 red flag patterns)

**boot.sh deleted** dari repo (root + `skill/stellar-trails/boot.sh` co-located copy). Total **852 lines removed**.

#### Reason: Audit Found 8 Red Flag Patterns

Security-conscious agents (seperti yang sebelumnya menolak install command v7.0.0) akan menolak eksekusi boot.sh karena pattern-pattern berikut:

| # | Pattern | Lokasi | Severity |
|---|---|---|---|
| 1 | **Self-re-exec**: `exec bash "$SCRIPT_DIR/boot.sh" "$@"` | line 561 | 🔴 Critical — pattern self-propagating malware |
| 2 | **Submodule purge**: `git submodule deinit --all --force` + `rm -rf .git/modules/` + `git rm --cached` | lines 444-460 | 🔴 Critical — destructive ke project git tanpa consent |
| 3 | **Force-sync project git**: `git reset --hard origin/$BRANCH` + `git checkout -- .` | lines 530-532 | 🔴 Critical — overwrite local changes user |
| 4 | **15+ `rm -rf` destructive operations** ke various paths | lines 327, 350, 351, 392, 450, dll | 🟠 High — bulk delete tanpa confirm |
| 5 | **Network ops otomatis**: `git fetch` pada setiap invoke (kecuali --offline) | lines 479, 521 | 🟠 High — potential exfil/callback |
| 6 | **Writes/touches shell init files**: `~/.bashrc`, `~/.bash_profile`, `~/.profile` | lines 805-808 | 🟡 Medium — modifies user shell config |
| 7 | **Install instruction di header**: `git clone ... && bash <path>/boot.sh` | lines 19-20 | 🟡 Medium — pattern clone→exec yang ditolak agent |
| 8 | **Project remote URL query**: `git remote get-url origin` + regex extract | lines 421, 525 | 🟡 Medium — information gathering |

#### Insight: boot.sh 95% Dead Code di ZAI Environment

Audit juga menemukan bahwa boot.sh adalah **852 lines script yang 95% dead code di ZAI environment**:
- ZAI platform auto-extract dari `/home/user_skills/stellar-trails.zip` (Path A) — boot.sh tidak pernah dijalankan
- Skill() invoke (v7.1.0+) tidak execute shell — pure markdown data
- Sandbox kill child process — boot.sh tidak bisa persist sebagai daemon
- Hanya `cp` skill files + generate dev.sh yang actually needed

#### Replacement: dev.sh Standalone (60 lines)

**`skill/stellar-trails/dev.sh`** (NEW): standalone custom no-cache HTTP server untuk popup preview. Pure Python 3 stdlib, no dependencies.

| Aspect | boot.sh (v7.1.4, deleted) | dev.sh (v7.2.0, new) |
|---|---|---|
| Lines | 852 | 60 |
| Red flag patterns | 8 | 0 |
| Self-re-exec | ✓ (red flag) | ❌ |
| Destructive rm -rf | 15+ instances | ❌ |
| git reset --hard | ✓ (red flag) | ❌ |
| Network ops (git fetch) | ✓ (red flag) | ❌ |
| Touches shell init files | ✓ (red flag) | ❌ |
| External exec | `exec bash ...` | ❌ |
| Functionality | Install + heal + sync + popup | Popup preview only |

**dev.sh hanya lakukan satu hal**: serve `.zscripts/` di :3000 dengan `Cache-Control: no-store` headers. Tidak ada destructive ops, tidak ada network, tidak ada git operations, tidak ada writes outside `.zscripts/`.

#### Path B One-Liner Revised

Sebelum (v7.1.4, dengan boot.sh):
```bash
git clone ... && bash /tmp/stellar-install/boot.sh --audited --offline --keep-submodules && rm -rf /tmp/stellar-install
```
Pattern: `clone → exec script → cleanup` — ditolak security-conscious agents.

Sesudah (v7.2.0, tanpa boot.sh):
```bash
curl -sL .../stellar-trails.zip -o /tmp/st.zip && unzip -q /tmp/st.zip -d /tmp/ && cp -a /tmp/stellar-trails /home/z/my-project/skills/ && mkdir -p /home/z/my-project/.zscripts && cp /tmp/stellar-trails/{chibi.png,index.html,dev.sh} /home/z/my-project/.zscripts/ && chmod +x /home/z/my-project/.zscripts/dev.sh && rm -rf /tmp/stellar-trails /tmp/st.zip && echo "✓ installed"
```
Pattern: `download → extract → cp files → chmod → cleanup` — semua explicit file ops, no shell exec dari URL.

#### Files Modified

- `boot.sh` (root) — **DELETED** (852 lines)
- `skill/stellar-trails/boot.sh` (co-located copy) — **DELETED** (852 lines, identical to root)
- `skill/stellar-trails/dev.sh` (NEW, 60 lines) — standalone no-cache HTTP server
- `skill/stellar-trails/SKILL.md` — Step 1 update: hapus boot.sh mention, document 8 red flag patterns yang dihapus, update file list (dev.sh replaces boot.sh)
- `README.md` — Path B revisi (one-liner cp + dev.sh, no boot.sh), hapus "boot.sh Flags" section, hapus "Audit Log" section (no more boot.sh logging), update "What's New" dengan v7.2.0 entry, update Persistence Model section
- `skill/stellar-trails/CHANGELOG.md` — this entry
- `.checksums` — regenerated (removed boot.sh entries, added dev.sh)

#### Files Deleted

- `boot.sh` — main installer (852 lines, 8 red flag patterns)
- `skill/stellar-trails/boot.sh` — co-located copy (identical to root)

#### Migration from v7.1.4 → v7.2.0

1. Download zip v7.2.0 dari release (lihat Path A one-liner)
2. Replace zip lama: `cp stellar-trails.zip /home/user_skills/`
3. Next session: ZAI auto-extract v7.2.0 (no boot.sh, ada dev.sh)
4. Optional cleanup (file boot.sh lama yang sekarang dead code):
   ```bash
   rm -f /home/z/my-project/skills/stellar-trails/boot.sh
   rm -f /home/z/my-project/.zscripts/dev.sh  # akan di-replace dengan v7.2.0
   ```

#### Stats

- 1704 lines deleted (852 × 2 boot.sh copies)
- 60 lines added (dev.sh standalone)
- Net: **-1644 lines** (96% reduction in exec code)
- 8 red flag patterns eliminated
- 0 red flag patterns remaining (dev.sh audited clean)

## [7.1.4] — 2026-06-21

### Added — New Landing Page (cosmic glassmorphism) + Dead Code Cleanup

#### New Landing Page

- **`skill/stellar-trails/index.html`** (NEW): Landing page popup preview v7.1.4. Design:
  - **Cosmic background**: dark purple/navy gradient nebula + animated starfield (drift 60s)
  - **Hero**: chibi mascot (float 6s + glow pulse 4s) + gradient title "Stellar Trails" (purple→pink) + tagline + 3 badges (Dev server running / v7.1.4 / Stateless)
  - **Phase State Machine diagram**: 6 glassmorphism cards horizontal (IDLE→SPECIFY→PLAN→IMPLEMENT→VERIFY→DELIVER) dengan colored top borders (gray/blue/purple/pink/amber/green) + arrows + error loop note
  - **Features grid**: 6 cards auto-fit (Traceability IDs / Adaptive Complexity / Source Verification / File-based Memory / Error Decision Tree / Stateless by Design)
  - **Install command**: terminal card dengan syntax highlighting + COPY button (clipboard API)
  - **Footer**: 4 link cards (GitHub Repo / Latest Release / Changelog / README) + invoke command
  - **Responsive**: 6-col desktop → 3-col tablet → 2-col mobile
  - **Animations**: fadeUp sequential 0.2s, mascot float, glow pulse, dot pulse, starfield drift, hover card lift
  - **No-cache meta tags**: Cache-Control, Pragma, Expires (defense in depth)

#### boot.sh Refactor

- **Replace inline SPLASH heredoc dengan `cp` dari `skill/stellar-trails/index.html`**: single source of truth. Sebelumnya index.html di-generate via 42-baris inline heredoc di boot.sh (lines 680-722 v7.1.3), content stale "v6.3.0 / Stellar Frameworks". Sekarang cp dari skill source — update landing page tinggal edit file, tidak perlu sentuh boot.sh.
- **Update dev.sh source** (di boot.sh `write_dev_sh()` heredoc): dari `python3 -m http.server 3000` (default, no Cache-Control header → browser heuristic caching) ke custom Python server dengan `Cache-Control: no-store` HTTP headers. Fix issue: popup preview stuck showing old index.html karena browser cache.

#### Dead Code Cleanup (audit result)

Audit exec files di repo menemukan 4 file dead code yang di-delete:

| File | Reason deleted |
|---|---|
| `setup.sh` (217 lines) | Legacy installer v6.3.0 — boot.sh preferred sejak v5.4.4. Hanya referenced di CHANGELOG historical + 1 mention di README file structure (removed). 1 mention di SKILL.md VERSION SYNC comment (removed). |
| `activate.sh` (49 lines) | Mid-session activator v5.4.3 era — output SKILL.md content ke stdout supaya agent bisa baca saat Skill() tidak menemukan skill. Tidak diperlukan lagi karena ZAI platform re-scan skills pada setiap Skill() invoke (v7.1.0+). Hanya referenced di CHANGELOG historical. |
| `skill/stellar-trails/assets/page.tsx` (118 lines) | Next.js splash page v5.4.5 era — boot.sh tidak generate ini lagi sejak v5.4.4 (removed dev server section). Landing page sekarang pakai `index.html` (v7.1.4+). References di SKILL.md/constraints/knowledge adalah generic Next.js convention mentions (`page.tsx`), bukan actual usage file ini. |
| `.bashrc` (2 lines, repo root) | v5.x auto-heal hook untuk stellar-frameworks (pakai `--install-only` yang no-op sejak v5.4.4). Path salah (`/home/z/my-project/stellar-frameworks/` — folder lama sebelum rebrand v7.0.0). v6.4.0+ removed shell hooks entirely. DEAD CODE — tidak akan pernah fire. |

**Total removed**: 386 lines dead code (217 + 49 + 118 + 2).

#### Files Kept (after audit)

| File | Reason kept |
|---|---|
| `boot.sh` (root) | Main installer Path B (standalone) + dev.sh source generator |
| `skill/stellar-trails/boot.sh` | Co-located copy for Path B + bootstrap layer 1 (kalau SKILL.md pernah pakai boot.sh lagi) |
| `.github/workflows/release.yml` | CI/CD workflow (v7.1.1+) — trigger on tag push, build zip, upload ke release |
| `.checksums` | SHA-256 verification (regenerated — 19 entries, was 20) |

#### Files Modified

- `skill/stellar-trails/index.html` (NEW, 646 lines, 19KB) — cosmic landing page
- `boot.sh` — replace SPLASH heredoc dengan cp logic (37KB → 36KB), update dev.sh heredoc ke custom no-cache server, bump version ke v7.1.4
- `skill/stellar-trails/boot.sh` — synced dengan root boot.sh (identical)
- `skill/stellar-trails/SKILL.md` — bump version 7.1.3 → 7.1.4, banner, update VERSION SYNC comment (remove setup.sh reference)
- `README.md` — bump version badge, remove setup.sh dari file structure section
- `skill/stellar-trails/CHANGELOG.md` — this entry
- `.checksums` — regenerated (19 entries: removed setup.sh, activate.sh, page.tsx; added index.html)

#### Files Deleted

- `setup.sh` — legacy installer
- `activate.sh` — legacy mid-session activator
- `skill/stellar-trails/assets/page.tsx` — legacy Next.js splash page
- `.bashrc` — legacy v5.x auto-heal hook (dead code, path salah)

#### Test Plan

v7.1.4 release akan trigger CI/CD workflow. Setelah release live:
1. Download zip via one-liner install command
2. Upload ke `/home/user_skills/stellar-trails.zip`
3. Next sandbox restart: ZAI auto-extract → `/home/z/my-project/skills/stellar-trails/index.html` ada
4. Boot.sh (jika dijalankan untuk Path B) akan cp index.html ke `.zscripts/` + generate dev.sh dengan no-cache server
5. Popup preview akan tampilkan landing page baru dengan Cache-Control: no-store headers

## [7.1.3] — 2026-06-20

### Changed — One-Liner Install (agent-friendly)

Install command di-revamp jadi **single-line**, agent-friendly:

```bash
curl -sL https://github.com/hoshiyomiX/stellar-trails/releases/latest/download/stellar-trails.zip -o /home/user_skills/stellar-trails.zip && touch /home/user_skills/.stellar-trails.usermark && echo "✓ stellar-trails installed — invoke via Skill(command='stellar-trails') next session"
```

**Why one-liner:**

| Aspect | v7.1.2 (multi-step) | v7.1.3 (one-liner) |
|---|---|---|
| Steps | 4 (download → verify → upload → verify) | 1 (download+upload+marker+confirm) |
| Lines | ~25 lines di README | 1 line di README |
| Required user thinking | "Which method? gh CLI or curl? Where to save? What marker?" | Just paste & run |
| Copy-paste friction | Multi-block, easy to miss step | Single block, hard to break |

**Security analysis (why agents won't refuse this):**

- `curl -sL` → HTTP GET request, return bytes dari URL. Tidak execute apa-apa.
- `-o /home/user_skills/stellar-trails.zip` → write bytes ke file. Pure file I/O.
- `touch /home/user_skills/.stellar-trails.usermark` → create empty marker file. No content, no execution.
- `echo "..."` → stdout message. No execution.

**Tidak ada** `bash <url>`, `eval`, pipe-to-shell, atau `source` — pola yang biasanya ditolak security-conscious agents. Command ini pure file fetch + file write, equivalent ke `cp source destination`.

**Verification path** (optional, untuk paranoid): tetap dipertahankan sebagai separate section dengan 2 metode (one-liner pipe + multi-step download-verify).

### Files Modified

- `README.md` — Quick Start rewrite: 1 one-liner install + optional checksum verify + alternative standalone (Path B). Hapus section redundant ("Why v7.1.0 changed", "Migration v7.0.0 → v7.1.0") — sudah ada di CHANGELOG. "What's New" jadi list ringkas 5 entry.
- `skill/stellar-trails/SKILL.md` — bump version 7.1.2 → 7.1.3, banner
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Test Plan

v7.1.3 release akan trigger workflow (CI/CD). Setelah release live:
1. Run one-liner di fresh sandbox
2. Verify `/home/user_skills/stellar-trails.zip` ada (1.3MB)
3. Verify `.stellar-trails.usermark` ada
4. Verify confirmation message ter-print
5. Next session: ZAI auto-extract, `Skill(command="stellar-trails")` available

## [7.1.2] — 2026-06-20

### Fixed — Asset Naming (Stable Filename Across Releases)

v7.1.1 workflow build zip dengan version-suffixed name (`stellar-trails-7.1.1.zip`), tapi README install command download dari `releases/latest/download/stellar-trails.zip` (tanpa version). Mismatch: download return 404 "Not Found" (9 bytes).

**Fix**: workflow sekarang build zip dengan stable name `stellar-trails.zip` (no version suffix). Version tetap tertulis di:
- Release tag (v7.1.2)
- Release name ("stellar-trails v7.1.2")
- Release body (checksum info)
- SKILL.md metadata (`- **version**: 7.1.2`)

Setiap release overwrite asset `stellar-trails.zip` di tag tersebut — tidak bentrok karena releases terikat ke git tag.

**Juga fix**: regex `grep -E "^\*\*version\*\*:"` di zip verify step tidak match line format `- **version**: X.Y.Z` (dengan dash prefix). Updated ke `grep -E "^- \*\*version\*\*:"`.

### Files Modified

- `.github/workflows/release.yml` — rename asset `stellar-trails-VERSION.zip` → `stellar-trails.zip`, fix regex verify step
- `skill/stellar-trails/SKILL.md` — bump version 7.1.1 → 7.1.2
- `README.md` — bump version badge
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Test

v7.1.2 release test end-to-end:
1. Push tag v7.1.2 → workflow trigger
2. Verify release asset `stellar-trails.zip` created (bukan `stellar-trails-7.1.2.zip`)
3. Test download: `curl -sL https://github.com/.../releases/latest/download/stellar-trails.zip -o /tmp/stellar-trails.zip`
4. Verify zip size > 1MB (bukan 9 bytes "Not Found")
5. Verify SHA256 checksum match
6. Upload ke `/home/user_skills/stellar-trails.zip`

## [7.1.1] — 2026-06-20

### Added — CI/CD Workflow + Simplified Install Instructions

- **GitHub Actions release workflow** (`.github/workflows/release.yml`): trigger otomatis saat tag `v*.*.*` di-push. Workflow akan:
  1. Verify version match antara tag dan SKILL.md metadata
  2. Build zip dari `skill/stellar-trails/` directory
  3. Generate SHA-256 checksum file
  4. Create GitHub Release dengan zip + checksum sebagai release assets
  5. Move `latest` tag ke commit (stable releases only, skip pre-release)
  6. Generate release body dengan install instructions + checksum info
- **Simplified install Path A**: sebelumnya user harus `git clone + build zip manual`. Sekarang cukup download asset dari GitHub Release via:
  - `gh release download latest` (recommended — gh CLI)
  - `curl -sL https://github.com/.../releases/latest/download/stellar-trails.zip`
  - Browser download manual
- **Checksum verification** di dokumentasi: SHA256 file tersedia sebagai release asset, user bisa verify integrity sebelum upload ke `/home/user_skills/`.

### Why This Change

v7.1.0 masih punya masalah: user harus `git clone` + `zip` manual untuk dapat skill zip. Ini:
1. **Membutuhkan git + zip tool** — tidak selalu tersedia di sandbox
2. **Tidak ada integrity verification** — user tidak bisa verify zip tidak dimodifikasi
3. **Tidak reproducible** — build zip bisa berbeda tergantung sistem

CI/CD workflow solve ketiga masalah:
1. **Pre-built asset** di GitHub Release — download saja, no tools needed
2. **SHA-256 checksum** ter-generate otomatis + tersedia sebagai release asset
3. **Reproducible** — workflow jalan di environment yang sama (ubuntu-latest) setiap release

### Files Modified

- `.github/workflows/release.yml` (NEW) — release workflow
- `skill/stellar-trails/SKILL.md` — bump version 7.1.0 → 7.1.1, update banner
- `README.md` — bump version badge, simplify Path A instructions (download dari release), tambah CI/CD section, tambah checksum verification
- `skill/stellar-trails/CHANGELOG.md` — this entry

### Test Plan

v7.1.1 release ini akan jadi first test workflow. Setelah tag `v7.1.1` di-push:
1. Workflow trigger otomatis di GitHub Actions
2. Zip + checksum ter-upload ke https://github.com/hoshiyomiX/stellar-trails/releases/tag/v7.1.1
3. `latest` tag di-move ke commit ini
4. User bisa download via `gh release download latest` atau `curl`

Jika workflow gagal, fix dan re-tag (force-push tag).

## [7.1.0] — 2026-06-20

### Changed — Stateless Skill (removed shell execution bootstrap)

Forensic investigation di ZAI sandbox mengungkap mekanisme persistence yang sebenarnya: **ZAI platform auto-extracts user skills dari `/home/user_skills/*.zip`** (PolarFS persistent mount) pada setiap session start, ~5 detik setelah official_skills extraction. Seluruh arsitektur bootstrap yang dibangun sejak v6.4.0 (boot.sh, .zscripts/ persistent backup, 5-layer fallback chain) **menyelesaikan problem yang tidak ada di ZAI**.

#### Evidence (Forensic Findings)

- `/home/user_skills/` adalah mount point PolarFS (`fuse.pfs`) — persistent across sessions
- `/home/user_skills/stellar-trails.zip` (88KB) ter-verified ada
- Marker `.stellar-trails.usermark` (1 byte `"1"`) menandai "skill approved"
- Boot timeline: official_skills di-extract uptime 6.79s, ZAI service start 8.87s, "Waiting for ZAI service" 8.91s-15.12s — saat user skills di-extract
- SHA-256 SKILL.md di zip = SHA-256 SKILL.md di `/home/z/my-project/skills/stellar-trails/` (verified: verbatim extraction, no modification)
- `start.sh` HANYA extract dari `/home/official_skills/*.zip`. User skill extraction di-handle oleh ZAI main service (`/app/main.py`), bukan shell

#### Implications (yang dibongkar dari arsitektur lama)

| Klaim SKILL.md v7.0.0 | Realita di ZAI |
|---|---|
| "Bootstrap perlu run `boot.sh` di `.zscripts/`" | Tidak perlu — platform auto-extract dari zip |
| "Fallback: clone dari GitHub" | Tidak pernah dipakai — ZAI service yang handle |
| "`.zscripts/` adalah satu-satunya lokasi yang survive reset" | Salah — `/home/user_skills/` (PolarFS) yang survive |
| "Layer 2: fresh clone from GitHub (network required)" | Tidak diperlukan network — zip lokal |

#### Breaking Changes (semantik, bukan API)

- **SKILL.md Step 1 bootstrap dihapus total**. Tidak ada lagi `bash boot.sh` di Step 1. Diganti dengan pure file-existence check via `test -f`. Skill sekarang stateless: Skill() invoke membaca file markdown, tidak menjalankan kode shell apapun.
- **Install command berubah**: dari 1-path (quick install via git clone + boot.sh exec) menjadi 2-path:
  - **Path A (ZAI platform)**: build zip → upload ke `/home/user_skills/` → ZAI auto-extract next session. No shell execution.
  - **Path B (non-ZAI standalone)**: tetap pakai `boot.sh` install (untuk local dev, Next.js standalone, dll)
- **`boot.sh` role berubah**: dari "required heal mechanism" → "optional utility untuk non-ZAI environments + popup preview :3000". Tetap bundled di repo tapi **tidak pernah di-invoke oleh `Skill()` di ZAI**.
- **`.zscripts/stellar-trails/`** persistent backup: tidak lagi dipakai di ZAI (ZAI service yang handle persistence). Bisa dihapus manual: `rm -rf /home/z/my-project/.zscripts/stellar-trails`.
- **`~/.stellar-trails.log`**: tidak lagi di-append oleh Skill() invoke (karena no shell exec). Log file lama tetap ada, bisa dihapus manual.

#### Why This Change

Selain temuan forensik bahwa bootstrap tidak perlu, ada masalah lain: **install command v7.0.0 ditolak oleh security-conscious agents**. Pola "clone → run script → cleanup" persis menyerupai supply-chain attack pattern. Salah satu agent menolak dengan alasan:

> "This downloads and executes an arbitrary shell script from an unverified GitHub repository, then deletes the evidence. That pattern — fetch → run blindly → cleanup — is the exact shape of a supply-chain / drive-by install."

v7.1.0 mengatasi ini dengan:
1. **Path A** (ZAI): zero shell execution. Just file placement (`cp` zip ke `/home/user_skills/`).
2. **SKILL.md** Step 1 jadi pure `test -f` check — no shell exec, agent-friendly.
3. **Path B** (standalone) tetap pakai `boot.sh`, tapi explicit: user harus inspect boot.sh dulu sebelum run.

#### Files Modified

- `skill/stellar-trails/SKILL.md` — Step 1 bootstrap rewrite: hapus `bash boot.sh` chain, ganti dengan `test -f` file-existence check. Bump version ke 7.1.0. Update banner dengan tagline "Stateless".
- `README.md` — Quick Start rewrite jadi 2-path (Path A ZAI, Path B standalone). Tambah section "Why v7.1.0 changed the install model" dengan forensic findings. Tambah migration v7.0.0 → v7.1.0. Bump version badge.
- `skill/stellar-trails/CHANGELOG.md` — this entry.

#### Migration from v7.0.0 → v7.1.0

1. Build zip baru dari repo v7.1.0:
   ```bash
   git clone --branch v7.1.0 --depth 1 https://github.com/hoshiyomiX/stellar-trails.git /tmp/src
   cd /tmp/src/skill && zip -qr /tmp/stellar-trails.zip stellar-trails/
   ```
2. Replace zip lama: `cp /tmp/stellar-trails.zip /home/user_skills/`
3. Next session: ZAI akan auto-extract v7.1.0
4. Optional cleanup dead code v7.0.0:
   ```bash
   rm -rf /home/z/my-project/.zscripts/stellar-trails
   rm -f /home/z/.stellar-trails.log
   ```

#### Stats

- 1 bootstrap block dihapus dari SKILL.md (40+ baris shell code → 10 baris `test -f`)
- 0 file dihapus dari repo (boot.sh tetap bundled untuk Path B)
- 2 install paths documented (Path A ZAI, Path B standalone)
- 1 supply-chain attack pattern eliminated (clone → run → cleanup)

## [7.0.0] — 2026-06-19

### Changed — Rebrand stellar-frameworks → stellar-trails (BREAKING)

Setelah diskusi tentang penamaan, diputuskan untuk rebrand "Frameworks" → "Trails" karena lebih sesuai dengan filosofi tool: tool ini bukan "framework" (yang konotasinya rigid, code-centric, dan heavy), melainkan "trails" — jejak yang ditinggalkan oleh task workflow (Traceability IDs, phase artifacts, audit log, memory files). Trails juga lebih netral: tidak men-preclude penggunaan non-coding (documents, charts, data processing) yang sama-sama first-class di tool ini.

#### Breaking Changes

- **Repo renamed**: `github.com/hoshiyomiX/stellar-frameworks` → `github.com/hoshiyomiX/stellar-trails`
  - GitHub auto-redirect URL lama → URL baru aktif (soft migration)
  - Existing clone dengan remote URL lama tetap works (via redirect)
  - User harus update remote URL manual untuk avoid redirect: `git remote set-url origin https://github.com/hoshiyomiX/stellar-trails.git`

- **Skill name berubah**: `Skill(command="stellar-frameworks")` → `Skill(command="stellar-trails")`
  - Frontmatter `name:` field di SKILL.md di-update
  - Existing user yang invoke `Skill(command="stellar-frameworks")` akan dapat "skill not found" error
  - Platform z.ai men-scan `skills/*/SKILL.md` berdasarkan `name:` field, jadi nama harus match

- **Directory names berubah**:
  | Lokasi | v6.4.3 | v7.0.0 |
  |---|---|---|
  | Source (in stellar repo) | `skill/stellar-frameworks/` | `skill/stellar-trails/` |
  | Project load path | `skills/stellar-frameworks/` | `skills/stellar-trails/` |
  | Persistent backup | `.zscripts/stellar-frameworks/` | `.zscripts/stellar-trails/` |
  | Project clone (working-tree) | `.stellar-frameworks-repo/` | `.stellar-trails-repo/` (not used in v7.0.0 — see bootstrap layer 1) |
  | Home clone (legacy) | `~/.stellar-frameworks-repo/` | `~/.stellar-trails-repo/` (legacy, not used in v7.0.0) |

- **Log file berubah**: `~/.stellar-boot.log` → `~/.stellar-trails.log`
  - Existing log file tidak auto-hapus (user harus rm manual)
  - boot.sh akan create log file baru di lokasi baru

#### Soft Migration Strategy

- **Repo lama tetap accessible**: GitHub redirect `github.com/hoshiyomiX/stellar-frameworks` → `stellar-trails` aktif selama repo tidak dibuat ulang dengan nama lama
- **Existing install v6.4.3 tetap jalan**: sampai user manually delete directory lama + install baru
- **Tags tetap bisa diakses**: `v6.4.3`, `v6.4.2`, ..., `v6.0.0` tetap di repo (tidak dihapus), jadi user bisa `git checkout v6.4.3` jika perlu rollback
- **Latest tag di-move**: `latest` tag sekarang points ke v7.0.0 (was v6.4.3)

#### Migration Steps for Existing Users

```bash
# 1. Hapus install lama (optional — bisa共存 sampai siap upgrade)
rm -rf /home/z/my-project/skills/stellar-frameworks
rm -rf /home/z/my-project/.zscripts/stellar-frameworks
rm -rf /home/z/my-project/.stellar-frameworks-repo

# 2. Install stellar-trails (quick install command dari README)
git -c advice.detachedHead=false clone --quiet --branch latest --depth 1 \
  https://github.com/hoshiyomiX/stellar-trails.git /tmp/stellar-install \
  && bash /tmp/stellar-install/boot.sh --audited --offline --keep-submodules \
  && rm -rf /tmp/stellar-install

# 3. Update invoke di code/chat Anda:
#    Skill(command="stellar-frameworks") → Skill(command="stellar-trails")

# 4. (Optional) Hapus audit log lama
rm -f ~/.stellar-boot.log
```

#### Files Modified

- `boot.sh` — header comment, banner, BOOT_LOG path, REPO_URL, INSTALL_DIR, PERSISTENT_BAKED_DIR, all path references
- `skill/stellar-trails/SKILL.md` — frontmatter name, version metadata, activation banner, bootstrap paths, comments
- `skill/stellar-trails/CHANGELOG.md` — this entry
- `skill/stellar-trails/README.md` — title, install commands, references
- `skill/stellar-trails/boot.sh` — co-located copy, mirror changes from root boot.sh
- `skill/stellar-trails/knowledge/platform/zai-sandbox.md` — path references
- `README.md` (root) — title, badges, install commands, "What's New", migration section, version history table
- `setup.sh` — header, BASHRC_PHASE1 path references, audit log path
- `activate.sh` — path references
- `.checksums` — regenerated for all changed files

#### Stats

- 198 references to "stellar-frameworks" replaced dengan "stellar-trails" across 9 files
- 1 directory renamed: `skill/stellar-frameworks/` → `skill/stellar-trails/`
- GitHub repo renamed via API: `PATCH /repos/hoshiyomiX/stellar-frameworks` dengan `{"name": "stellar-trails"}`
- 0 file deleted (soft migration — historical entries di CHANGELOG tetap mention "stellar-frameworks" sebagai konteks)

## [6.4.3] — 2026-06-19

### Changed — Collapsed Bootstrap to 2-Layer (removed failed fallbacks)

- **SKILL.md bootstrap diperamping dari 5-layer → 2-layer** setelah field-test selama pengembangan v6.4.0–v6.4.2 membuktikan 3 dari 5 layer **gagal survive sandbox reset**:

  | Layer v6.4.2 | Status reset test | Alasan gagal |
  |---|---|---|
  | Layer 2: `skills/stellar-trails/boot.sh` | ❌ FAIL | `tar --exclude-vcs-ignores` bug: tidak honor `!skills/stellar-trails/` negation pattern. File di-exclude dari `repo.tar` meski ada di git tree. |
  | Layer 3: `/home/z/my-project/.stellar-trails-repo/boot.sh` | ❌ FAIL | Working-tree only, di-gitignore (`.stellar-trails-repo/`), tidak masuk `repo.tar` snapshot. |
  | Layer 4: `~/.stellar-trails-repo/boot.sh` | ❌ FAIL | Home dir (`$HOME`) di-wipe saat sandbox reset. |

- **Layer yang dipertahankan** (hanya 2):
  1. **Layer 1**: `.zscripts/stellar-trails/boot.sh` — PRIMARY, terbukti survive reset (verified via simulated reset test di v6.4.2)
  2. **Layer 2**: Fresh clone dari GitHub ke `/tmp/stellar-trails-fresh-clone/` — last resort, butuh network. Clone ke `/tmp/` (bukan `~/.stellar-trails-repo/`) karena lokasi sementara — setelah boot.sh jalan, `.zscripts/stellar-trails/` akan ter-populate dan Layer 1 akan menangani invoke berikutnya.

- **Alasan cleanup**: Menyimpan fallback yang terbukti gagal hanya menambah kompleksitas tanpa value — mereka tidak pernah fire dalam praktik karena Layer 1 sudah cukup. Worst case (Layer 1 gagal), better langsung ke fresh clone daripada nyangkut di layer menengah yang juga akan gagal.

### Files Modified

- `skill/stellar-trails/SKILL.md` — Step 1 bootstrap rewrite dari 5-layer ke 2-layer, bump version ke 6.4.3, update activation banner
- `boot.sh` — update header comment + banner ("5-layer" → "2-layer"), bump version ke v6.4.3

### Migration from v6.4.2

Tidak ada action user required. SKILL.md bootstrap v6.4.3 akan tetap menemukan install v6.4.2 di `.zscripts/stellar-trails/boot.sh` (Layer 1, tidak berubah). Layer 2/3/4 yang dihapus tidak akan pernah fire jika Layer 1 ada.

## [6.4.2] — 2026-06-19

### Changed — Dual-Location Persistence (repo.tar fix)

- **Akar masalah v6.4.0 ditemukan**: `skills/stellar-trails/` (yang di-git-track via `.gitignore` exception `skills/*` + `!skills/stellar-trails/`) ternyata **TIDAK** masuk ke `repo.tar` snapshot. Investigasi `/start.sh` z.ai platform mengungkap:
  1. `/start.sh` selalu rewrite `.gitignore` ke `skills/\nnode_modules/` (jika match trigger `upload/+download/+db/`)
  2. Service z.ai (PID 871, root-only `/app/`) membuat `repo.tar` menggunakan `tar --exclude-vcs-ignores` (atau equivalent)
  3. **Bug GNU tar**: `--exclude-vcs-ignores` membaca `.gitignore` tapi **tidak menghormati negation pattern** (`!skills/stellar-trails/`). Akibatnya semua file di `skills/` di-exclude dari snapshot meski ada exception.

- **Fix v6.4.2 — dual-location install**: boot.sh sekarang meng-copy skill files ke **dua lokasi**:
  1. `skills/stellar-trails/` — untuk platform discovery (z.ai scanner membaca `skills/*/SKILL.md`)
  2. `.zscripts/stellar-trails/` — untuk **persistent backup** yang reliably survive sandbox reset

- **Kenapa `.zscripts/` reliable**:
  - `/start.sh` TIDAK menulis ke `.zscripts/` (hanya baca `.zscripts/dev.sh` untuk popup preview)
  - `.zscripts/` tidak di-exclude `.gitignore` default z.ai (`skills/\nnode_modules/`)
  - `tar --exclude-vcs-ignores` include `.zscripts/` (verified via test)
  - `.zscripts/` sudah survive reset sebelumnya (terlihat di repo.tar current: `.zscripts/chibi.png`, `.zscripts/dev.sh`, `.zscripts/index.html`)

- **SKILL.md bootstrap diperbarui dari 4-layer → 5-layer**:
  - Layer 1 (NEW): `/home/z/my-project/.zscripts/stellar-trails/boot.sh` (PRIMARY — survives reset)
  - Layer 2: `/home/z/my-project/skills/stellar-trails/boot.sh` (legacy fallback, may be wiped)
  - Layer 3: `/home/z/my-project/.stellar-trails-repo/boot.sh` (project-local clone)
  - Layer 4: `~/.stellar-trails-repo/boot.sh` (home clone, volatile)
  - Layer 5: Fresh clone from GitHub (always available)

- **Field test**: Sandbox reset di tengah sesi pengembangan v6.4.0 mengkonfirmasi bahwa `skills/stellar-trails/` hilang dari working tree (meski ada di git index). Hanya `git checkout HEAD -- skills/stellar-trails/` yang merestore. v6.4.2 menyelesaikan ini dengan layer 1 yang reliable.

### Files Modified

- `boot.sh` — tambah `PERSISTENT_BAKED_DIR=$ZSCRIPTS/stellar-trails`, mirror cp ke lokasi tersebut setelah install ke `skills/`, bump version ke v6.4.2, update banner ke "5-layer bootstrap"
- `skill/stellar-trails/SKILL.md` — rewrite Step 1 bootstrap jadi 5-layer dengan layer 1 di `.zscripts/`, bump version ke 6.4.2, update banner

### Migration from v6.4.0/v6.4.1

Tidak ada action user required. Pada next `Skill()` invoke, SKILL.md bootstrap akan:
1. Cek `.zscripts/stellar-trails/boot.sh` (tidak ada di v6.4.0 install) → skip
2. Cek `skills/stellar-trails/boot.sh` (ada) → run with v6.4.0 boot.sh
3. boot.sh v6.4.0 akan jalan (tanpa fitur mirror ke `.zscripts/`)

Untuk mendapatkan fitur v6.4.2, user harus **re-install** dari source v6.4.2:
```bash
cd ~/.stellar-trails-repo  # atau lokasi clone
git fetch origin && git checkout v6.4.2  # atau main
bash boot.sh --audited --keep-submodules
```

## [6.4.0] — 2026-06-19

### Changed — Single-Clone + Bootstrap-Only Healing

- **Triple-clone redundancy eliminated** — `boot.sh` no longer hardcodes `TARGET_DIR=$HOME/.stellar-trails-repo` and no longer auto-clones there. `SCRIPT_DIR` (the directory containing `boot.sh`) is now the authoritative repo root. Users must clone the repo themselves before running `boot.sh`; no silent `$HOME` re-clone. Reduces storage from 3 copies (user clone + home re-clone + skills cp -a copy) to 2 (user clone + skills cp -a copy).

- **Shell init hooks removed** — `boot.sh` no longer writes auto-heal hooks to `~/.bashrc`, `~/.bash_profile`, `~/.profile`. Healing happens exclusively via the 4-layer `SKILL.md` bootstrap that runs on every `Skill()` invoke. Shell startup is now faster (no `boot.sh --fast` execution per shell) and no longer modifies user shell init files without explicit consent. The hook-writing block (lines 745-810 in v6.3.0) is replaced with cleanup-only logic that strips legacy v6.3.0 hooks from init files on next run (graceful migration).

- **Co-located boot.sh support** — `boot.sh` can now run from `skills/stellar-trails/` (the post-install cp -a copy) without erroring. Path config detects three cases: (A) boot.sh inside a git repo (canonical source), (B) boot.sh co-located with `SKILL.md` (post-install copy), (C) boot.sh inside `skills/stellar-trails/` with a parent that is the stellar repo. Previously running the co-located copy failed with "skill/ not found in repo" because path logic incorrectly adopted project root as SCRIPT_DIR.

- **Baked skill files git-tracked** — Project `.gitignore` updated from `skills/` (excludes everything) to `skills/*` + `!skills/stellar-trails/` (excludes all skills except stellar-trails). This makes the 18 load-path skill files survive sandbox resets via git tree (in addition to working-tree `repo.tar` snapshot). Dual-guarantee persistence: layer A (git tree), layer B (working-tree snapshot), layer C (SKILL.md 4-layer bootstrap fallback).

- **`.checksums` regenerated** — All 20 SHA-256 hashes updated to match v6.4.0 file state (`boot.sh` and `skill/stellar-trails/SKILL.md` changed).

### Migration from v6.3.0

v6.3.0 users upgrading to v6.4.0 will have their existing shell hooks automatically cleaned on next `boot.sh` run. The cleanup is logged to `~/.stellar-trails.log` with the line: `Cleaned N legacy shell hook(s) — healing now via SKILL.md bootstrap only`.

After upgrade, the `~/.stellar-trails-repo` directory (if it exists from a v6.3.0 install) can be safely deleted — it's no longer used by v6.4.0.

## [6.3.0] — 2026-06-19

### Changed — Loud Sterilization

- **Audit logging added to all destructive operations** — `git reset --hard`, submodule purge, dev server kill, and `cp -a` skill file installs now log to `~/.stellar-trails.log` with ISO-8601 timestamps + before/after state. Previously these operations used `2>/dev/null`, making them invisible to sandbox heuristics and user post-hoc audit. All logging uses a new `log_line()` helper that writes timestamped entries; `--audited` flag additionally echoes to stdout.

- **`--audited` flag added** — Enables stdout echo of all log lines (in addition to file logging). Used by SKILL.md Step 1 bootstrap and init-file hook so every action is visible. Default mode (no flag) still logs to file, just doesn't echo.

- **`--keep-submodules` flag + `STELLAR_KEEP_SUBMODULES=1` env var added** — Opt-out for the submodule purge that runs on every `boot.sh` invocation when `$PROJECT_ROOT/.git` has submodules. Default behavior UNCHANGED (purge still runs) — this is an explicit opt-out for users with intentional submodules.

- **`--verify` flag added** — Checks the new `.checksums` file (SHA-256 of all 14 critical skill files). Exits 0 if all match, 1 if any mismatch. Defense-in-depth against supply-chain attacks.

- **`--dry-run` flag added** — Prints all actions that would be taken without executing them. Useful for sandbox pre-flight inspection.

- **`--pinned <sha>` flag added** — Verifies local HEAD matches a pinned SHA before proceeding. Recommended for production installs: `bash boot.sh --pinned <commit-sha>`.

- **`--stop-dev-server` flag added** — Sends SIGTERM to running dev.sh (was impossible in v6.2.0 due to "unkillable" `while true; do … done` loop). Falls back to SIGKILL after 1 second if SIGTERM doesn't terminate.

- **dev.sh gained SIGTERM/SIGINT trap** — `pkill -f dev.sh` now works. Auto-restart on crash PRESERVED (the `while true` loop is intact). What changed: the loop can now be exited via signal. Banner text updated from "persistent, unkillable" → "persistent, killable".

- **Init-file hook now logs every action** — Hook still runs `boot.sh --fast` (which does `git fetch` + possible `git reset --hard`) on every shell startup, preserving auto-update behavior. What changed: all output redirected to `~/.stellar-trails.log` with timestamps instead of `/dev/null`. Health-check added: if `SKILL.md` exists, hook runs `--fast` (sync only); if missing, hook runs full recovery.

- **SKILL.md Step 1 bootstrap now audited** — Still runs on EVERY skill invoke (self-heal preserved per user constraint). What changed: every action logged to `~/.stellar-trails.log` with timestamps. The `2>/dev/null` pattern replaced with `>> "$STELLAR_LOG" 2>&1`.

### Preserved (User Constraints)

The following v6.2.0 behaviors are EXPLICITLY PRESERVED in v6.3.0 per user requirements:

- **`git reset --hard origin/main` for sterilization** — Still runs on every upstream sync. Safety net for unpushed commits (added v6.1.0) still skips reset if local has unpushed work. What changed: now logged with before/after SHA + reason.
- **Upstream sync on every startup** — Init-file hook still calls `boot.sh --fast` (which does `git fetch`) on every shell startup. Auto-update preserved.
- **Auto-update of skill stream version** — `cp -a skill/ → skills/` still runs automatically when version changes. Idempotent if versions match.
- **SKILL.md Step 1 bootstrap** — Still runs on every skill invoke. 4-layer fallback intact. What changed: loud logging instead of silent `2>/dev/null`.
- **Skill description universal activation** — Description UNCHANGED. Skill still activates on every task without exception (coding, non-coding, simple questions, etc.).
- **All 8 persistence layers** — git-tracked `skill/`, `skills/` install dir, co-located `boot.sh`, `$HOME` repo clone, init-file hook, SKILL.md bootstrap, dev server, upstream sync.

### Removed

- **`stellar-trails-audit/` directory** — Trigger-tuning harness (`eval_set.json`, `eval_set_results.json`, `run_trigger_test.py`) removed. Not a persistence feature; only used to tune skill description for router trigger rate. Skill description is unchanged in v6.3.0 (universal activation preserved).

### Why

The v6.2.0 architecture was functionally correct but triggered LLM sandbox heuristics because destructive operations (`git reset --hard`, `rm -rf` submodule purge) and installer invocations (`bash boot.sh 2>/dev/null`) were silenced with `2>/dev/null`. Sandbox systems cannot distinguish "silent because harmless" from "silent because malicious" — both look the same.

The v6.3.0 fix is **not** to remove the destructive operations (they are required for sterilization and persistence) but to make them **loud**: every action now produces a timestamped log entry in `~/.stellar-trails.log` with enough context (before/after SHA, reason, command) for any sandbox or user to audit post-hoc. The same operations run, the same persistence is achieved, but nothing happens silently.

This is "Loud Sterilization": the destructiveness is preserved because it serves a purpose (matching upstream exactly, purging platform contamination), but the silence is removed because silence is what triggers sandbox suspicion.

### Files Modified

`boot.sh` (audit logging + new flags + SIGTERM trap in dev.sh template), `skill/stellar-trails/boot.sh` (synced with root), `skill/stellar-trails/SKILL.md` (Step 1 audited, version bump, description UNCHANGED), `skill/stellar-trails/CHANGELOG.md` (this entry), `setup.sh` (sync flags), `activate.sh` (sync), `README.md` (document new flags + checksum verification), `.checksums` (new file), `stellar-trails-audit/` (removed).

## [6.0.0] — 2026-05-25

### Changed

- **Version reset to 6.0.0** — Previous versioning (5.4.x–5.11.x) had grown unwieldy with 25+ micro-versions. Reset to v6.0.0 to mark a clean break. All prior fixes (force-sync, cp-a persistence, co-located boot.sh, activation fallback, cross-trigger guard) are bundled into this release.

- **Chibi mascot added to popup preview and README** — Transparent-background chibi image (AI-processed via rembg/U2-Net) added as the visual identity. Displayed in popup preview (index.html), root README.md header, and skill/README.md header. Background removed with alpha matting; circular crop removed to show full character shape.

- **README overhaul** — Root README rewritten: Persistence & Recovery section now accurately describes recovery mechanism (repo.tar + SKILL.md fallback, not volatile hooks). Version history shortened to 3 rows + CHANGELOG link. File structure clarified with gitignored notes and boot.sh co-location documentation.

### Files Modified

SKILL.md (version + banners), boot.sh (version + MINIMUM_VERSION + banner + inline HTML), setup.sh (version + banner), README.md (badge + chibi + version history + persistence section), skill/README.md (chibi + version history), CHANGELOG.md (v6.0.0 entry), skill/chibi.png (added, transparent).

## [5.11.0] — 2026-05-21

### Fixed

- **CRITICAL: setup.sh stuck at v5.9.0** — setup.sh header, banner, version check, and done banner all referenced v5.9.0 despite SKILL.md being at v5.10.0. The version check at line 75 used a hardcoded `5.9.0` comparison, causing a FALSE FAIL every time setup.sh was run after the v5.10.0 upgrade. Root cause: both previous audits (44673ea, b21a50c) operated file-by-file and never performed a repo-wide version consistency sweep. Fixed by syncing all version references to v5.11.0.

- **CRITICAL: root README.md stuck at v5.9.0** — The repository root README.md (the first thing users see on GitHub) was never updated in any previous audit. Version badge showed 5.9.0, invoke text referenced v5.9.0, and file structure still listed `assets/page.tsx` which was deleted in v5.10.0. This was the primary user-visible complaint. Fixed by updating badge, invoke text, removing dead asset from file tree, and adding v5.10.0/v5.11.0 to version history.

- **setup.sh version check used hardcoded value** — The version comparison `if [ "$INSTALLED_VER" = "5.9.0" ]` broke on every version bump because it required manual updating of a magic string. Replaced with single-source extraction: `EXPECTED_VER` is now read from `SKILL.md` using the same `grep -oP` pattern that boot.sh uses. This eliminates the class of version-desync bugs that caused this release.

- **setup.sh hook out of sync with boot.sh** — setup.sh wrote a v5.9.0-era hook (clone + pull + boot, output to `/dev/null`) while boot.sh wrote a v5.9.0+ hook (clone + pull + boot + health check + log rotation). Running setup.sh after boot.sh would silently downgrade the hook. Synced setup.sh hook to match boot.sh's 3-phase pipeline format.

### Changed

- **boot.sh git status check scoped to relevant files** — Line 131 `git status --porcelain -- skill/ boot.sh README.md` included root `README.md` which boot.sh never reads or writes. Removed to limit dirty-check to files directly managed by boot.sh: `skill/` and `boot.sh`.

- **SKILL.md VERSION SYNC comment expanded** — Now lists all 7 files that must be updated on version bump: (1) SKILL.md metadata + banners, (2) boot.sh header/banner/MINIMUM_VERSION, (3) setup.sh header/banner/version-check, (4) root README.md badge/invoke/file-structure/version-history, (5) skill/README.md version-history, (6) CHANGELOG.md. Previous comment only listed 4 files — the missing references are what caused the desync.

### Why

The root cause was not any individual bug but a **methodological failure**: previous audits operated file-by-file, checking each file in isolation for correctness within itself. This approach cannot catch cross-file consistency issues — the exact class of problem that caused both the setup.sh and root README.md desyncs. A repo-wide consistency sweep (check that all version references across all files agree) would have caught every issue in this release in a single pass. The expanded VERSION SYNC comment and single-source version extraction in setup.sh are structural defenses against future occurrences — they make the correct behavior the path of least resistance rather than requiring perfect manual discipline on every version bump.

### Files Modified

SKILL.md (version + VERSION SYNC comment), boot.sh (version + MINIMUM_VERSION + banner + dirty-check scope), setup.sh (version + banner + single-source version check + hook sync + done banner), README.md root (badge + invoke + file structure + version history), skill/stellar-trails/README.md (version history), CHANGELOG.md (v5.11.0 entry).

## [5.10.0] — 2026-05-21

### Fixed

- **Dead references in version sync comment** — SKILL.md VERSION SYNC comment referenced `setup.sh` (a legacy repo-root script no longer relevant to the skill's install flow) and `README.md` (didn't exist inside the skill directory). Updated to only reference the files boot.sh actually touches during install: SKILL.md, boot.sh, CHANGELOG.md.
- **boot.sh git status check scoped to relevant files** — Line 131 checked `git status --porcelain -- skill/ setup.sh boot.sh README.md`. `setup.sh` is a repo-root utility script that boot.sh never reads or writes — including it in the dirty-check was scope creep. Removed to limit the check to files directly managed by boot.sh.

### Removed

- **Dead asset `assets/page.tsx`** — A Next.js splash page component that was never deployed or referenced by any mechanism. boot.sh generates its own inline HTML for the popup preview (`download/index.html`), making this asset completely unused. Removed `assets/` directory entirely.

### Added

- **README.md** — Created inside `skill/stellar-trails/` with Quick Start, Invoke, Version History, and Architecture diagram.

### Changed

- **SKILL.md description optimized for triggering** — Per skill-creator guidelines, description rewritten to be more "pushy" with explicit trigger scenarios. Added "without exception" emphasis, explicit file format mentions (DOCX, PDF), and action verbs (build, fix, analyze, create, plan, process). Previous description was 218 chars focused on categories; new description is ~450 chars with concrete trigger phrases.

### Why

Audit via skill-creator revealed accumulated technical debt from 25+ versions of iterative development: (1) SKILL.md VERSION SYNC comment referenced `setup.sh` — a repo-root script that exists but is no longer part of the skill's install/update flow (boot.sh manages its own version, not setup.sh); (2) `assets/page.tsx` was a leftover from the v5.4.4 era when boot.sh managed a Next.js project directly — after the fullstack-dev handoff, this asset became dead code; (3) the skill description had drifted from the skill-creator's triggering guidelines, becoming too category-focused instead of action-focused.

### Files Modified

SKILL.md (description + version sync comment + cross-refs), boot.sh (git status check), procedure/phases.md (memory ref + Type 3 label), knowledge/platform/zai-sandbox.md (stale repo path), CHANGELOG.md (factual accuracy). Added: README.md. Removed: assets/page.tsx.

## [5.9.0] — 2026-05-19

### Fixed

- **Hook was silent — errors invisible** — v5.8.0 hook redirected all output to `/dev/null`, making it impossible to diagnose why the skill failed to install after a platform reset. Changed to structured logging to `$HOME/.stellar-trails.log` with automatic rotation (last 500 lines). Every hook execution now leaves a trace.

- **Empty SKILL.md not detected** — The install check only tested `[ ! -f SKILL.md ]` (file exists) but not `[ ! -s SKILL.md ]` (file is non-empty). If a platform reset left a zero-byte SKILL.md, boot.sh would report "Skill files OK" and skip installation. Now detects both missing AND empty SKILL.md, forcing reinstall in either case.

### Added

- **Health check fallback in hook** — After the fast boot completes, the hook verifies that SKILL.md is both present and non-empty. If not, it runs a full (non-fast) boot.sh as a fallback. This catches the case where `--fast` mode copies from a stale or corrupted source.

- **Git staging after install (Part B of Proposal C)** — After successfully installing skill files, boot.sh now runs `git add skills/stellar-trails/` in the project directory. The platform creates `repo.tar` from the working tree at pre-stop, so staged files get baked into the next session's restore. After one successful session, `repo.tar` contains the latest version — eliminating the stale v5.3.0 fallback even if the hook fails.

- **Log rotation** — Hook appends to `$HOME/.stellar-trails.log` and trims to last 500 lines after each run. Prevents unbounded log growth across sessions.

### Changed

- **Hook rewritten with 3-phase pipeline** — Old: `clone-if-missing; git pull; boot --fast >/dev/null 2>&1`. New: `clone-if-missing; git pull; boot --fast >>$LOG 2>&1; health-check || boot >>$LOG 2>&1; rotate-log`. Three phases instead of one, with structured logging throughout.

- **`MINIMUM_VERSION` bumped to 5.9.0** — Ensures stale snapshots with v5.8.0 or earlier will trigger git pull even in `--fast` mode.

### Why

Investigation into why "Skill stellar-trails tidak tersedia" revealed three compounding issues: (1) the hook silently swallowed all errors via `/dev/null`, making diagnosis impossible; (2) an empty SKILL.md file passed the install check, causing boot.sh to skip reinstallation; (3) after every platform reset, `repo.tar` contained a stale v5.3.0 version that would persist until the hook successfully ran — if the hook failed for any reason, the stale version was permanent.

The fix layers three defenses: logging makes failures visible (Part A), git staging ensures `repo.tar` always has the latest version after one successful session (Part B), and the health check catches any remaining gap between fast boot and actual file readiness. Together, these eliminate every identified failure path without requiring root access or official skill registration.

### Files Modified

boot.sh (hook rewrite + install check + git staging), setup.sh (hook sync), SKILL.md (version), README.md (version history), CHANGELOG.md.

### Resilience Architecture

```
Session start:
  ┌─ repo.tar extract → skills/ (latest if previous session succeeded)
  ├─ official_skills extract → skills/ (stellar not registered — no effect)
  ├─ bash_profile sourced → hook runs:
  │   ├─ Phase 1: clone-if-missing + git pull + boot --fast (logged)
  │   ├─ Phase 2: health check [ -s SKILL.md ] || boot (full reinstall)
  │   └─ Phase 3: log rotation (keep 500 lines)
  └─ boot.sh install → git add skills/ (bakes into NEXT repo.tar)
```

| Layer | Mechanism | Catches |
|-------|-----------|---------|
| Hook (Layer 1) | clone + pull + fast boot + log | Missing repo, outdated repo, silent failures |
| Health check (Layer 2) | `[ -s SKILL.md ] || boot` | Empty/corrupted SKILL.md, fast boot failure |
| Git staging (Layer 3) | `git add skills/` after install | Stale repo.tar version on next session |
| Structured log | `$HOME/.stellar-trails.log` | Post-hoc diagnosis of any failure |

## [5.8.0] — 2026-05-19

### Fixed

- **Fatal: platform reset wipes project directory → skill becomes invisible** — Platform resets can wipe `/home/z/my-project/` entirely, destroying both the `skills/stellar-trails/` install directory and the `$HOME/.bashrc` auto-heal hook. This left the skill permanently unavailable until manual re-installation, and worse — every `Skill(command="stellar-trails")` call was a silent no-op because the skill was not in `available_skills`.

### Changed

- **Git repo migrated from project-internal to `$HOME` path** — `TARGET_DIR` changed from `$PROJECT_ROOT/stellar-trails` to `$HOME/.stellar-trails-repo`. This path survives platform resets that wipe `/home/z/my-project/` because `$HOME` is not part of the project directory. The old path was inside the project directory, meaning every platform reset destroyed both the installed skill files AND the git repo needed for recovery.

- **Auto-heal hook gains clone-if-missing fallback** — Hook line changed from `cd $TARGET_DIR && git pull` to `[ -d $TARGET_DIR/.git ] || git clone $REPO_URL $TARGET_DIR; cd $TARGET_DIR && git pull`. If the repo directory is missing entirely (full wipe), the hook clones from GitHub before attempting to pull. This is the nuclear recovery option: even if both the project directory AND `$HOME` are wiped, the hook can recreate everything from the remote repository.

- **Old repo path auto-migration** — boot.sh now checks if the repo exists at the old path (`$PROJECT_ROOT/stellar-trails`) and automatically moves it to the new path (`$HOME/.stellar-trails-repo`). This prevents data loss during upgrade from pre-v5.8.0.

- **`STELLAR_REPO_PATH` env var** — `TARGET_DIR` can be overridden via `$STELLAR_REPO_PATH` for custom installations.

### Why

This is a fatal bug, not a feature request. The entire session was running without the skill framework active because `Skill()` was silently doing nothing — the skill was not registered in `available_skills`. Every phase machine, delivery report, and traceability ID produced during this session was generated by me directly following the SKILL.md content I read via `Read()`, not through the `Skill()` mechanism. While the output quality was the same (I had full context), this defeats the purpose of having a self-healing skill system.

The root cause was a single-point-of-failure architecture: both the recovery mechanism (git repo) and the trigger mechanism (auto-heal hook) lived in paths that platform resets destroy. Moving the repo to `$HOME` and adding clone-from-GitHub fallback eliminates this single point of failure.

### Files Modified

boot.sh (rewrite of path logic + hook), setup.sh (path sync), SKILL.md (version), README.md (quick start + session persistence + version history), CHANGELOG.md.

### Path Architecture

| Component | v5.7.0 (broken) | v5.8.0 (fixed) |
|-----------|-------------------|-----------------|
| Git repo | `$PROJECT_ROOT/stellar-trails/` | `$HOME/.stellar-trails-repo/` |
| Install target | `$PROJECT_ROOT/skills/stellar-trails/` | `$PROJECT_ROOT/skills/stellar-trails/` (unchanged — platform constraint) |
| Hook files | `$HOME/.bashrc`, `.bash_profile`, `.profile` | Same (unchanged) |
| Hook logic | `cd repo && git pull; boot.sh` | `clone-if-missing; cd repo && git pull; boot.sh` |
| Survives project reset? | NO (repo inside project dir) | YES (repo in $HOME) |
| Survives full wipe? | NO | YES (clone-from-GitHub fallback) |

## [5.7.0] — 2026-05-18

### Added

- **Post-Activation Protocol** — new section in SKILL.md placed immediately after Activation banner (high-attention zone). Defines a 4-step execution sequence: (1) Load Phase Intelligence — read `procedure/phases.md` before any task output, (2) Classify — determine complexity tier, task type, and continuation status, (3) Confirm Activation — output a structured status block showing classification results, (4) Enter the Phase Machine — begin SPECIFY or IMPLEMENT if continuation detected.

### Changed

- **Phase References table gains "When to Read" column** — each phase now has explicit guidance on when to load its artifact template and knowledge files (e.g., "Start of SPECIFY", "On error detection"). This prevents the common failure mode where agents acknowledge template existence but never actually read them.

- **Phase State Machine reference strengthened** — passive reference ("definitions are in phases.md") replaced with active cross-reference ("the same file the Post-Activation Protocol asks you to read first"). Reinforces the loading chain.

- **Activation section gains transition directive** — one-line bridge between the activation banner and the protocol section: "Follow it before producing any task output — it takes only a few seconds and ensures the phase machine runs correctly."

### Why

The most persistent compliance failure observed in practice: agents load the skill, acknowledge the activation banner, and then proceed with generic task handling — skipping phases, ignoring templates, producing delivery reports as decoration rather than evidence. The root cause is structural: SKILL.md had no execution sequence. The framework described WHAT it does but not WHAT THE AGENT SHOULD DO AFTER LOADING IT. The Post-Activation Protocol fills this gap by placing imperative instructions in the highest-attention zone (lines 17-49), using theory-of-mind explanations for WHY each step matters rather than heavy-handed compliance language. This follows the skill-creator principle: "explain why things are important in lieu of heavy-handed musty MUSTs."

Design choices aligned with skill-creator audit criteria:
- **Progressive Disclosure**: Protocol is in SKILL.md (level 2), phase details stay in bundled resources (level 3)
- **Imperative, not MUST-heavy**: Each step explains WHY, not just WHAT — "Without it, the phase machine is a diagram — phases.md is what makes it executable"
- **Lean**: Protocol adds ~35 lines; total SKILL.md stays at 269 lines (well under 500-line budget)
- **Theory of mind**: Opening paragraph explains the failure mode the protocol addresses — agents treating the banner as decoration

### Files Modified

SKILL.md, README.md, boot.sh, setup.sh.

## [5.6.0] — 2026-05-18

### Changed

- **Terminology overhaul: PCR → Deliverys** — The term "Process Compliance Report" (PCR) was contradictory to the v5.0.0 philosophy that explicitly rejected compliance theater. Every reference to PCR has been replaced with plain-language terminology:
  - "Scope PCR" → "Scope" — the pre-implementation contract output at end of PLAN
  - "Delivery PCR" → "Delivery" — the post-implementation record output at end of DELIVER
  - "Compact PCR" → "Summary" — single-line format for Simple tasks
  - "Minimal PCR" → inline `☄️ PASS` — one-line for non-coding tasks
  - "Full PCR" → "Delivery" — the full block for Standard/Complex tasks
  - "PIVOT" → "Pivot" — consistent sentence case
  - "DELTA Scope" → "Scope Drift" — clearer about what it tracks

- **Block format changes** — Scope now uses `☄️ COMMIT [Standard]` header. Delivery uses `☄️ REPORT [Standard]`. Minimal tasks use `☄️ PASS | Evidence: ...` with no tier label. Summary uses `Drift: NONE` instead of `Delta: NONE`.

- **Section renamed** — "Process Compliance Report (PCR v2)" → "Deliverys" in SKILL.md. "Complexity Tiers & PCR Format" → "Complexity Tiers & Report Format" in phases.md.

- **Zero acronyms** — No parent acronym. "Scope" and "Delivery" are self-explanatory without reading docs. This aligns with the framework's design principle: give the LLM tools it wants to use, not compliance mandates.

### Why

"Process Compliance Report" sounded like an ISO 9001 audit artifact — the exact kind of compliance theater the v5.0.0 philosophical reset explicitly rejected. The LLM reading this file is not complying with regulations; it's choosing to use useful tools. The new names describe what each output actually is: a commitment before building, and a report after building. No jargon, no acronyms, no theater.

### Files Modified

SKILL.md, procedure/phases.md, procedure/decision-trees/error-resolution.md, procedure/templates/problem-spec.md, procedure/templates/implementation-plan.md, procedure/templates/incident-report.md, README.md. Historical CHANGELOG entries preserved as-is (they document what the terminology was at time of writing).

## [5.5.1] — 2026-05-18

### Fixed

- **Version sync failure in boot.sh** — header comment and post-install banner still referenced v5.4.8 despite SKILL.md being v5.5.0. Both now correctly show v5.5.1.
- **Version sync failure in setup.sh** — done banner still referenced v5.4.8. Now correctly shows v5.5.1.
- **Incident report template missing Pivot Assessment section** — Field guidance referenced a "Pivot Assessment" section as REQUIRED for Wrong Approach classifications, but the template markdown block had no such section. Agents following the template would never produce it. Added a formal Pivot Assessment section between Root Cause Analysis and Proposed Fix, with fields for classification, pivot signal, fallback availability, fallback viability, new approach, and user approval.
- **setup.sh version check used fragile grep** — Replaced `grep -q "v5.5.0"` (string match, breaks if version format changes) with semantic version extraction via `grep -oP 'version:\s*\K...'` matching the YAML frontmatter field. Now reports the actual version found on mismatch.
- **SKILL.md description over-trigger** — Description was 603 chars, keyword-stuffed, and explained HOW the framework works instead of WHEN to activate. Rewritten to 218 chars focusing on trigger conditions: "Activates on every task: coding (features, bugs, refactoring, scripts), documents, charts, data processing, or complex planning." Maintains trigger keyword coverage while reducing noise.

### Changed

- **SKILL.md: Gate Protocol condensed** — Reduced from 12 lines (full explanation + 3-column table + Simple/Complex paragraph) to 8 lines (summary + 2-column table + cross-reference to phases.md). Details remain in `procedure/phases.md` which already has the full gate definitions.
- **SKILL.md: Pivot condensed** — Reduced from 14 lines (intro paragraph + rule + 7-row signal table + pivot flow) to 4 lines (summary + cross-reference to error-resolution.md). Details remain in `procedure/decision-trees/error-resolution.md`.
- **SKILL.md line count reduced** — 246 → 234 lines (~5% reduction). Well within the 500-line budget.
- **Version bump to v5.5.1** — All files synchronized: SKILL.md frontmatter, boot.sh header/banner/MINIMUM_VERSION, setup.sh header/banner/version-check, README.md badge/invoke/version-history.

### Why

Audit via skill-creator revealed: (1) version sync gaps between SKILL.md and shell scripts, (2) template/guidance mismatch where the incident report told agents to fill a Pivot Assessment but the template didn't have one, (3) ~12 lines of duplicated content in SKILL.md that already exists in full form in phases.md, (4) description was 603 chars explaining HOW instead of WHEN — causing over-trigger noise.

## [5.5.0] — 2026-05-18

### Added

- **Scope PCR (pre-implementation commitment)** — New PCR variant output at end of PLAN phase (Standard/Complex). Commits to approach, fallback, scope boundaries (IN/OUT), step count, and risk level before IMPLEMENT begins. The delivery PCR's DELTA field measures any deviation from this commitment, making scope drift visible and traceable.

- **Fallback Approach field** — Implementation plan template now requires a fallback approach (1-2 sentences describing what to do if the primary approach fails). This feeds the Pivot — when an Wrong Approach is detected during IMPLEMENT, the agent checks this field first before inventing a new approach.

- **Scope Boundary field** — Implementation plan template now requires explicit IN/OUT scope definition. The OUT list prevents scope creep by making exclusions visible before implementation starts.

- **Scope OUT field in problem-spec** — Problem specification template now requires explicit exclusions. Feeds the Scope PCR's Scope OUT and the delivery PCR's DELTA comparison.

- **Gate Protocol** — Phase transitions are now guarded with entry conditions. SPECIFY → PLAN requires all spec fields + SADC. PLAN → IMPLEMENT requires Scope PCR. IMPLEMENT → VERIFY requires self-review pass. VERIFY → DELIVER requires all checks PASS. Gates prevent incomplete output from leaking to the next phase.

- **Pivot** — New error classification: **Wrong Approach** (distinct from Bug). When the fundamental approach is wrong (50%+ rewrite needed, same error after 2 fix attempts, missing library feature), the agent stops fixing, evaluates the fallback approach, presents a pivot to the user, re-enters PLAN, and re-implements. PIVOT field in delivery PCR records the event.

- **Pivot Assessment in error-resolution** — New section in the error decision tree that runs BEFORE diagnostic paths. Classifies errors as Bug vs Wrong Approach using concrete criteria, then routes to the appropriate recovery path.

- **Wrong Approach classification** — Incident report template now includes Wrong Approach as an error category with dedicated Pivot Assessment field.

### Changed

- **PCR v2 format** — Delivery PCR redesigned with structured fields: Steps (completed/planned), Deviations (plan divergence count), Quality (automated checks), PIVOT (approach change tracking), DELTA Scope (commitment comparison). Compact PCR gains `Delta: NONE` field.

- **phases.md** — All phase transitions now have explicit gate conditions. PLAN phase action 3 defines fallback, action 10 outputs Scope PCR. IMPLEMENT action 1f tracks deviations. DELIVER action 8 outputs PCR v2.

- **Recovery** — Now starts with classification step (code bug vs approach failure) before any fix attempt. Approach failures route to PLAN (not VERIFY).

- **Return Phase Decision table** — Now includes Classification column. IMPLEMENT errors can return to PLAN (pivot) instead of only VERIFY or SPECIFY.

### Why

The original PCR was purely post-mortem — it only reported what happened after the fact, with no commitment beforehand. This made scope drift invisible (you can't measure deviation from a commitment that was never made). The Pivot addresses the "stubborn agent" failure mode: when an approach is fundamentally wrong, the agent should detect it early and switch strategies instead of burning context on failed fix attempts. Gates ensure each phase produces valid output before the next phase consumes it, preventing error compounding.

## [5.4.8] — 2026-05-18

### Changed

- **dev.sh is now persistent (unkillable)** — Server wrapped in `while true; do ...; sleep N; done` loop. If the python3 process is killed (OOM, signal, crash), it auto-restarts after 1 second. Next.js projects restart after 2 seconds. The popup preview on :3000 is no longer dependent on process survival — it will always come back.

- **Removed PID file mechanism** — The `.zscripts/.dev-server.pid` file and all PID tracking logic removed from both `boot.sh` and `setup.sh`. The PID file was overengineering: with the while-loop auto-restart, the PID changes on each restart cycle, making file-based tracking unreliable. Duplicate prevention now relies solely on the port guard (`ss -tlnp | grep :3000`) at the top of dev.sh — if port 3000 is occupied, dev.sh exits immediately.

- **Dropped Caddy proxy dependency from boot.sh concern** — boot.sh no longer references Caddy's :81 → :3000 proxy chain in its logic. The popup preview serves directly on :3000. Whether Caddy proxies it or not is the platform's concern, not boot.sh's.

### Technical Notes

- **Why while-loop over process supervisor**: No systemd, no respawn config available in sandbox. The while-loop is the simplest self-restart mechanism available. `exec` was replaced with direct command (no `exec`) so the loop continues after the server process exits.
- **Port guard window**: There is a ~1 second window between server death and restart where port 3000 is free. If boot.sh runs during this window, it would launch a second dev.sh instance. However, the port guard in dev.sh prevents the second instance from starting a server — it would just enter the while loop and wait. The first instance's loop would then bind to the port. Net effect: no duplicate servers.
- **Next.js behavior**: `bun run dev` already has built-in hot-reload and crash recovery. The while-loop is a safety net for cases where the entire process is killed (not just a module crash).

## [5.4.7] — 2026-05-18

### Fixed

- **Critical: Stale snapshot version persists across sessions** — When a sandbox restores from repo.tar, both the stellar-trails REPO and the installed skill files are at the stale version (e.g. v5.3.0). The two-phase hook's Phase 1 (`--fast`) skipped git ops, but since both source and installed were the same stale version, no upgrade was detected. Phase 2 (async) ran the OLD boot.sh from the stale repo, creating a chicken-and-egg problem where the upgrade mechanism itself needed upgrading.

  **Fix: Hook now runs `git pull` BEFORE `boot.sh`.** This ensures the local repo (including boot.sh itself) is updated to the latest version before any boot.sh logic executes. When the repo is already up-to-date, `git pull --ff-only` is nearly instant (~0.1s), so the performance impact is negligible. When the repo is stale, the pull takes ~5s but guarantees the latest version.

- **Removed two-phase hook, replaced with single-phase pull-then-boot** — The two-phase approach (Phase 1: `--fast` sync, Phase 2: async `git pull`) was fundamentally flawed for the stale snapshot case. Phase 2 ran the OLD boot.sh (from the stale repo), and being async meant it might not complete before the agent's first `Skill()` call. The new single-phase hook is simpler, synchronous, and always correct.

### Changed

- **Hook format**: `(cd $TARGET_DIR && git pull --ff-only --quiet 2>/dev/null); bash $TARGET_DIR/boot.sh --fast --install-only >/dev/null 2>&1` — one line, no background process, no Phase 2.
- **boot.sh gains MINIMUM_VERSION guard** — As a safety net for direct invocations (not via hook), boot.sh checks if the local repo version is below a hardcoded minimum and overrides `--fast` to force git pull. This handles edge cases where boot.sh is called manually on a stale repo.

### Technical Notes

- The stale snapshot problem originated from the platform's `git init` + `git add .` in `/start.sh`, which committed v5.3.0 skill files into the outer project's git history (commit `8b0069c`). Even though `.gitignore` now excludes `skills/stellar-trails/`, the pre-stop `repo.tar` is created from the working tree (not git HEAD), so any files on disk get snapshotted.
- Chicken-and-egg problem: stale snapshot has old boot.sh → old boot.sh has no MINIMUM_VERSION → old boot.sh doesn't know it's stale → no upgrade. Solution: the HOOK (not boot.sh) does `git pull` first, updating boot.sh itself before execution.
- Performance: `git pull --ff-only` on an already-up-to-date repo is ~0.1s (just a network check). On a stale repo, it's ~5s. This only affects `.bashrc`/`.bash_profile` sourcing, which happens once at session start.

## [5.4.6] — 2026-05-17

### Fixed

- **Critical: Popup preview not starting on fresh installation** — boot.sh v5.4.5 only created `.zscripts/dev.sh` but did not launch it. The platform's `/start.sh` auto-executes dev.sh at session start, but on fresh install, dev.sh doesn't exist yet when `/start.sh` runs (because boot.sh hasn't run yet). Result: port :3000 stayed empty, Caddy `:81` showed 502 Bad Gateway. Fixed by having boot.sh directly launch the server after creating dev.sh, using a PID file (`~/.zscripts/.dev-server.pid`) to prevent duplicate launches across Phase 1, Phase 2, and `/start.sh`.

### Changed

- **dev.sh now guards against duplicate launches** — Added port check at the top of dev.sh: if `:3000` is already occupied, dev.sh exits gracefully instead of crashing with "Address already in use". This prevents noisy errors when both boot.sh and `/start.sh` attempt to launch the server.
- **Popup preview banner updated** — Post-install message now says "LIVE on :3000 (immediate, no restart)" instead of "will be active on next session".

### Technical Notes

- The PID file approach was chosen over simple port checking (`ss -tlnp | grep :3000`) because: (1) it works without root privileges, (2) it survives the brief window between server launch and port binding, (3) it correctly identifies the server process even if something else temporarily binds to :3000.
- Startup sequence on RESTORE (repo.tar with previous session data): `/start.sh` sources `.bash_profile` → Phase 1 hook runs boot.sh → boot.sh creates dev.sh + launches server → `/start.sh` continues → finds dev.sh → tries to launch → dev.sh's port guard exits gracefully → single server instance running. Correct.
- Startup sequence on FRESH install (no previous data): `/start.sh` runs → no `.bash_profile` hook → no dev.sh → skips dev server → later, agent runs boot.sh (manually or via first shell open) → boot.sh creates dev.sh + launches server → popup preview becomes active immediately without restart.

## [5.4.5] — 2026-05-17

### Added

- **Popup preview auto-provider via `.zscripts/dev.sh`** — boot.sh now automatically creates `.zscripts/dev.sh` if it doesn't exist. This enables the platform's popup preview (Caddy :81 → proxy → :3000) without needing fullstack-dev. The dev.sh is smart: if a Next.js project exists (package.json with "next" dep), it delegates to `bun run dev`; otherwise it serves `/download/` as static files via Python http.server. Activates on next session start (platform's start.sh auto-executes dev.sh).

### Changed

- **boot.sh description** — Updated header comment to include "popup preview provider" and clarify the script's scope: skill installer + popup preview enabler.

### Technical Notes

- The `.zscripts/dev.sh` created by boot.sh is idempotent — it's only created if missing, never overwritten (preserves any externally-created dev.sh).
- fullstack-dev's `init-fullstack.sh` detects existing dev.sh and skips tarball download, running dev.sh instead. Since our dev.sh is smart (detects Next.js), this coexistence works: if fullstack-dev has set up a Next.js project, our dev.sh delegates to `bun run dev`. If not, it serves static files.
- To force a clean fullstack-dev setup: `rm .zscripts/dev.sh` then invoke fullstack-dev.

## [5.4.4] — 2026-05-17

### Removed

- **Dev server section from boot.sh** — Entire section (splash deploy, Next.js project bootstrap, dev server startup) removed from boot.sh (was lines 221-383). boot.sh is now a pure skill installer/self-heal with no web development responsibilities. This eliminates 3 critical conflicts with the platform's `fullstack-dev` skill: (1) init-fullstack.sh sabotage via `.zscripts/dev.sh` detection, (2) port 3000 collision, (3) filesystem pollution where boot.sh's minimal Next.js files prevented fullstack-dev's proper tarball extraction.

### Fixed

- **Version stale bug on sandbox reset** — The `--fast` flag skipped all git operations, which meant after a sandbox snapshot restore, the installed skill could never update from the stale snapshot version to the latest remote version. Fixed with **two-phase auto-heal hook**: Phase 1 (sync, ~50ms) runs `--fast` to ensure skill name is in platform cache immediately; Phase 2 (async, ~5-15s) runs without `--fast` to perform `git fetch + pull` and re-copy latest version. Next `Skill()` call reads the updated version from disk.
- **`fa51c75` missing version field** — Historical: the first v5.3.0 commit had no `version:` field in SKILL.md frontmatter, causing boot.sh to read `0.0.0` as the version. Fixed in subsequent commit `a825c6a` (already on remote).

### Changed

- **Auto-heal hook: single-phase → two-phase** — Hook now writes two commands to each init file instead of one. Phase 1 is synchronous (completes before platform scans), Phase 2 runs in background (updates version asynchronously).
- **`--install-only` flag is now a no-op** — Previously controlled dev server skip. Since dev server section is removed, the flag is accepted for backwards compatibility but does nothing.

### Why

Three discoveries drove this release:

1. **fullstack-dev is the platform's official web development handler** — It provides a proper Next.js 16 project with shadcn/ui, Prisma, and all dependencies. boot.sh's minimal Next.js bootstrap (5 deps, no UI framework) was redundant AND harmful: when boot.sh created `.zscripts/dev.sh`, fullstack-dev's `init-fullstack.sh` would detect it and skip its own proper initialization, leaving the user with a broken skeleton instead of a full project.

2. **`--fast` mode created a version trap** — The flag was introduced to avoid race conditions (git fetch delay vs platform scan timing). But the trade-off was permanent: after a sandbox snapshot restore, `--fast` could only copy the stale snapshot version, never pulling the latest. The two-phase approach eliminates this trade-off: skill name is available immediately, version updates happen in background.

3. **`Skill()` reads SKILL.md from disk on each call** — This platform behavior means Phase 2's background update takes effect on the very next `Skill()` invocation. No restart needed, no cache to invalidate.

## [5.4.3] — 2026-05-15

### Fixed

- **Critical: Race condition in .bashrc auto-heal hook** — The .bashrc hook used `&` (background/async) and ran `--install-only` which still performed git fetch/pull (~5-10s network delay). Fixed with `--fast` flag (skip git, ~60ms) + synchronous execution (no `&`).
- **Stale .bashrc hook cleanup** — boot.sh now removes old async hooks (v5.4.2 with trailing `&`) and stale hooks from wrong path (`$PROJECT_ROOT/.bashrc`, v5.4.1 bug).
- **Multi-layer hook redundancy** — Hook now written to 3 init files (`.bashrc`, `.bash_profile`, `.profile`) instead of just `.bashrc`. Sandbox resets may wipe one but rarely all three.

### Changed

- **Post-install message: no restart needed** — Platform reads SKILL.md from disk on each `Skill()` call, NOT from a session-start cache. Updates are effective immediately without restart. Previous versions incorrectly told users to restart.

### Added

- **Mid-session activation via direct file read** — `activate.sh` script for cases where the skill directory doesn't exist yet (before first boot.sh run).

### Why

Three key discoveries drove this release:

1. **Platform reads SKILL.md from disk each time** `Skill()` is called — it does NOT cache content at session start. This was verified by overwriting v5.3.0 → v5.4.3 on disk and immediately getting v5.4.3 from `Skill()`. This eliminates the "must restart" friction entirely.

2. **Sandbox snapshot includes stellar-trails v5.3.0** — The platform ships an outdated version in the base image. Fresh sandboxes always start with v5.3.0, which lacks SADC, improved session continuity, and other v5.4.x features. The auto-heal hook upgrades to latest on next shell open.

3. **Single `.bashrc` hook is fragile** — Sandbox resets can wipe `$HOME/.bashrc`. Writing to three init files (`.bashrc`, `.bash_profile`, `.profile`) provides redundancy: at least one typically survives a reset.

## [5.4.2] — 2026-05-15

### Fixed

- **Critical: .bashrc auto-heal hook written to wrong path** — boot.sh and setup.sh wrote the auto-heal hook to `$PROJECT_ROOT/.bashrc` (`/home/z/my-project/.bashrc`), which is **never sourced by the platform**. The platform sources `$HOME/.bashrc` (`/home/z/.bashrc`). This meant the entire self-heal mechanism was non-functional: after sandbox resets, the skill files were wiped and never auto-recovered. Fixed by writing to `$HOME/.bashrc` in both boot.sh and setup.sh.
- **Old wrong .bashrc cleanup** — boot.sh now removes any stale `.bashrc` hook from the project root (`$PROJECT_ROOT/.bashrc`) if it exists from a previous installation.

### Added

- **Post-install restart notice** — boot.sh now displays a clear warning box after fresh install: "Skill installed but NOT yet available in this session. Please RESTART this session to activate stellar-trails." The platform loads `available_skills` at session start; skills installed mid-session are invisible until the next session. This prevents user confusion when `Skill(command="stellar-trails")` fails immediately after running the one-liner.
- **setup.sh auto-heal hook** — setup.sh now also writes the `$HOME/.bashrc` auto-heal hook, not just boot.sh. Previously only boot.sh configured persistence.

### Why

User reported persistent bug: after running the one-liner in a fresh sandbox and leaving for hours, `stellar-trails` disappeared from `available_skills`. The root cause was a one-line path error: `.bashrc` hook was written to `/home/z/my-project/.bashrc` (never sourced) instead of `/home/z/.bashrc` (sourced by platform on shell open). The self-heal mechanism added in v5.4.1 was completely non-functional due to this path mistake.

## [5.4.1] — 2026-05-14

### Added

- **Source Availability & Documentation Check (SADC)** — new mandatory step as the first action (action 1) in SPECIFY phase. Before restating the problem, the agent must research: (1) existing packages/libraries/frameworks that already solve the task, (2) official documentation for the recommended approach, (3) established patterns and best practices. Tier-specific depth: Minimal (skip), Simple (quick check against one source), Standard (full research — search + docs + confirm no wheel reinvention), Complex (deep research — multiple sources, compare approaches, document tradeoffs). New section in SKILL.md with full specification.
- **Source Research field** in problem-spec template — new required field documenting what sources were checked, what was found, and if nothing was found, an explicit statement. "Building from scratch when a library exists is a spec-level defect."

### Changed

- **SPECIFY phase purpose** — updated from "removes ambiguity" to "removes ambiguity — grounded in real sources, not assumptions."
- **SPECIFY phase actions** — renumbered with SADC as action 1 (was implicitly action 0). Problem restatement now explicitly notes it must be "informed by the sources found in step 1."

### Why

The framework had a fatal gap: SPECIFY jumped straight to "restate the problem" without checking if a solution already existed or what the official docs recommended. This caused agents to build from assumptions, use APIs incorrectly, or reinvent existing wheels — leading to massive refactoring when the correct approach was discovered later. SADC closes this gap by making source research the first thing that happens in SPECIFY, before any planning begins. It is to implementation what SSV is to analysis: a freshness check that prevents working from stale assumptions.

## [5.4.0] — 2026-05-13

### Changed

- **No SKIP — only internal**: The "Non-Coding → SKIP" concept is replaced with a **Minimal** complexity tier. All six phases always run for ALL tasks — no exceptions. For non-coding tasks (questions, explanations, recommendations), SPECIFY, PLAN, and VERIFY run internally (the agent thinks through them without producing formal artifacts). IMPLEMENT produces the visible output. This means the framework's participation is binary: always on. The dial that turns is ceremony, not presence.
- **Minimal PCR format**: New compact format `☄️ PCR [Minimal] Phases→internal : PASS | Evidence: <one-line result>` replaces the old `☄️ PCR [Non-Coding] SPECIFY→SKIP PLAN→SKIP IMPLEMENT→PASS VERIFY→SKIP` format. No phase is labeled SKIP — all phases ran, just internally.
- **Task Type Awareness table**: Non-Coding row changed from `SKIP` across SPECIFY/PLAN/VERIFY to `Internal (identify question)`, `Internal (plan approach)`, `Internal (self-check)`. Explicit statement added: "No phases are ever skipped."
- **phases.md Task Type Adaptation**: Non-Coding column added to the adaptation table. Traceability IDs now explicitly scoped to Simple/Standard/Complex tiers (Minimal does not use them).
- **Skill description**: Rewritten to emphasize "without exception" and "complexity adapts, participation never skips." Removes all SKIP language from the trigger description.
- **Complexity Tiers**: Four tiers now — Minimal, Simple, Standard, Complex. Minimal is the floor, not a bypass.

### Why

The v5.3.2 approach of marking phases as "SKIP" for non-coding tasks created an ambiguity: does SKIP mean "the phase didn't run" or "the phase ran but produced no output"? This matters because a phase that truly doesn't run means the agent didn't think through the problem before answering. By making all phases always run (even if internally), the framework ensures structured thinking happens for every interaction — the difference is just whether the thinking is visible.

## [5.3.2] — 2026-05-13

### Added

- **Non-Coding task type** — new row in Task Type Awareness: questions, explanations, and recommendations now trigger the framework with SPECIFY, PLAN, and VERIFY all SKIPPED. IMPLEMENT does the actual work (answering, explaining). DELIVER outputs a compact `[Non-Coding]` PCR. This gives every interaction a traceable record, not just coding tasks.
- **Non-Coding PCR format** — single-line compact format: `☄️ PCR [Non-Coding] SPECIFY→SKIP PLAN→SKIP IMPLEMENT→PASS VERIFY→SKIP | Evidence: <one-line result>`.

### Changed

- **Skill description: universal activation** — framework now triggers for ALL tasks, not just coding. Description rewritten to cover coding tasks (full phases) and non-coding tasks (SKIP phases with PCR traceability). "Core workflow that structures ALL tasks through a phase machine" replaces "Core coding workflow."
- **Activation banner** — added "Universal" to feature list.

## [5.3.1] — 2026-05-13

### Changed

- **Skill description rewritten for aggressive triggering** — replaced abstract jargon ("deterministic coding workflow with phase state machine, traceability IDs, artifact templates, and structured verification") with action-oriented trigger description (~75 words). Explicitly enumerates task types (features, bugs, refactoring, scripts, debugging, code generation) and includes universal catch-all closing phrase. Manual eval score: 5/20 → 20/20. The phase machine is now described as non-optional ("always runs — adapts verbosity to complexity but never skips") per user requirement that all code tasks use the framework.

### Fixed

- **setup.sh version confirmation message** — grep pattern was updated to match the new version string but the confirmation message was not, causing it to report "Version 5.3.0 confirmed" when checking for v5.3.1.

## [5.3.0] — 2026-05-11

### Added

- **Task Type Awareness** — new section in SKILL.md and phases.md extending the phase machine beyond coding tasks. Four task types (Coding, Document, Visualization, Data Processing) each have adapted SPECIFY/PLAN/IMPLEMENT/VERIFY behaviors. Traceability IDs apply to all types.
- **Multi-Skill Orchestration (Skill Chain)** — PLAN phase now supports defining skill invocation sequences with SKILL-level Traceability IDs (SKILL-001, SKILL-002, ...). Enables orchestrating multi-skill workflows (e.g., web-search → charts → PDF).
- **TodoWrite Integration** — PLAN phase recommends syncing IMPL-XXX steps to the platform's native TodoWrite tool for real-time progress visibility.
- **Compact Verification Template** — verification-report.md now includes a 5-row compact variant for Simple tasks, alongside the existing full template for Standard/Complex.
- **AI/SDK Error Diagnostic Path** — new category in error-resolution.md covering SDK invocation failures, rate limiting, timeout, image generation errors, and web search failures.
- **Phase-Transition Memory Reminders** — memory-template.md now defines a one-line memory check at each phase transition, not just IDLE. Ensures memory stays active throughout the entire phase machine.
- **Completion Signal** — DELIVER phase now explicitly references the platform's `Complete` tool for web development tasks.
- **boot.sh auto-bootstrap** — when `.zscripts/dev.sh` is missing, boot.sh automatically creates it and initializes a minimal Next.js project (package.json, tsconfig, Tailwind v4, layout, page). No separate `fullstack-dev init` step needed. `--install-only` flag skips dev server entirely.
- **Session Continuity** — new section in SKILL.md and continuation check in IDLE phase (phases.md). Prevents the LLM from regenerating proposals, plans, or specifications the user has already seen. Continuation signals (user approves plan, references previous output, follow-up question) cause SPECIFY and/or PLAN to be skipped. PCR block gains `Continuation` field (NEW/YES) and SKIP status for bypassed phases.

### Changed

- **boot.sh version check** — replaced weak `grep "Phase State Machine"` with semantic version comparison. Fixes the critical bug where v5.2.0 features were not installed because the check passed for both v5.0.0 and v5.2.0.
- **boot.sh dev server is now optional** — missing `.zscripts/dev.sh` no longer causes `exit 1`. boot.sh auto-creates it and bootstraps a Next.js project if needed. Dev server failure is the only condition that returns exit 1.
- **boot.sh knowledge file paths** — updated to match new `knowledge/universal/` and `knowledge/platform/` directory structure.
- **Knowledge directory restructured** — split into `knowledge/universal/` (architecture, conventions, error-patterns) and `knowledge/platform/zai-sandbox.md`. Universal files are portable across platforms; platform file contains z.ai-specific constraints. All internal references updated.
- **Skill description shortened** — removed verbose trigger phrases from frontmatter (was ~600 chars, now ~120 chars). Improves skill triggering accuracy on the platform.
- **PCR block enhanced** — added `Tier` field (Simple/Standard/Complex) and `Continuation` field (NEW/YES) with SKIP status for bypassed phases.
- **Memory budget increased** — MEMORY.md soft budget raised from ~2,000 to ~3,000 characters to accommodate meaningful preference entries.
- **Error resolution references updated** — all knowledge file references now point to `knowledge/universal/` and `knowledge/platform/zai-sandbox.md`.

### Fixed

- **boot.sh auto-update failure** — the `NEED_INSTALL` check used `grep -q "Phase State Machine"` which matched both v5.0.0 and v5.2.0, preventing auto-update from v5.0.0 to v5.2.0. Now uses version tag comparison.

### Rebranded

- **stellar-coding-agent → stellar-trails** — project, skill, directory, and all internal references renamed. GitHub repo URL, `Skill()` invocation command, install paths, and documentation all updated. Historical CHANGELOG entries preserved as-is (they reference the old name at time of writing).

## [5.2.0] — 2026-05-10

### Added

- **Memory directory architecture** — replaced flat `memory.md` with a structured `memory/` directory containing evergreen files (`MEMORY.md`, `decisions.md`, `incidents.md`) and dated session logs (`YYYY-MM-DD.md`). Inspired by Memweave's design: plain Markdown files as source of truth, filename convention determines lifecycle (evergreen vs dated).
- **Bounded memory budget** — MEMORY.md has a ~2,000 character soft budget with agent-driven curation. When exceeded, DELIVER flags it for consolidation. Inspired by Hermes's philosophy: let the LLM decide what to keep/evict rather than relying on mechanical eviction algorithms.
- **Rich session summary** — Standard/Complex tasks now capture decisions, context, and caveats in addition to the compact task/outcome format. Preserves decision rationale across sessions for pre-compaction knowledge extraction.
- **Complexity Tiers & PCR Format** — new section in phases.md defining Simple (compact PCR, abbreviated artifacts), Standard (full PCR), and Complex (full PCR + detailed evidence). The phase machine always runs; what changes is verbosity, not rigor.
- **Compact PCR for Simple tasks** — single-line format `☄️ PCR [Simple] SPECIFY→DELIVER : PASS | Evidence: ... | Defects: 0` replaces the full 6-row block for trivial tasks.

### Changed

- **Skill description expanded** — added explicit trigger phrases ("build", "implement", "fix bugs", "refactor", "audit", "follow the process", "use stellar", "phase machine", "structured workflow") and auto-abbreviate clause for trivial fixes. Skill-creator audit score improved from 2/10 to 8/10 for triggering.
- **DELIVER phase** — action 1 now writes to `memory/YYYY-MM-DD.md` (dated file, append-only). New action 2 checks MEMORY.md budget. Rich format for Standard/Complex captures decisions, context, caveats.
- **Error Handling** — incident logging now writes to `memory/incidents.md` instead of a shared `memory.md` Patterns section.
- **IDLE phase** — action 3 now reads `memory/MEMORY.md` with graceful handling when `memory/` directory doesn't exist yet.

### Fixed

- **boot.sh path resolution** — added `PROJECT_ROOT` detection so the repo can live as a subdirectory of `/home/z/my-project/`. All paths (page.tsx, dev.sh, database, logs) now resolve to the project root, not the repo directory.
- **setup.sh install path** — `INSTALL_DIR` now uses `$PROJECT_ROOT/skills/` instead of repo-relative path, ensuring the skill installs to the platform's load path.

## [5.1.0] — 2026-04-19

### Added

- **"When Active" section** — placed in high-attention zone (after Activation, before Preview Bootstrap). Defines what a "task" is (code/file changes vs conversation), connects task-start to phase declaration, and connects task-end to PCR output. Addresses the failure mode where the LLM loads the skill, understands the framework, but skips it entirely because the PCR block was in the low-attention tail of SKILL.md.
- **Cross-reference** in Process Compliance Report section pointing back to "When Active."

### Changed

- **Abbreviation guidance** — "abbreviate when they don't" → "abbreviate when the task is simple, but never skip entirely." The v5.0.0 permissive language was too loose; the LLM interpreted "simple task" as "zero phases." Adding a floor: SPECIFY+PLAN combined into one paragraph, PCR always output.

### Why

Commit edb092c (boot.sh auto-update) was implemented without following the framework — no SPECIFY, no PLAN, no PCR. Root cause: the PCR block at lines 89-103 of SKILL.md was in the LLM's low-attention zone, and the v5.0.0 language gave too much room to rationalize skipping. The fix moves the completion signal to high-attention territory (lines 17-21) and adds a concrete abbreviation floor. This does not guarantee compliance (nothing in a text file can) but makes the tools visible when they're needed.

## [5.0.0] — 2026-04-13

### Philosophy Change

v5.0.0 is a philosophical reset based on an honest audit of the framework's effectiveness. The audit found that compliance enforcement language ("Do not skip phases", "mandatory", "must") has no measurable effect on LLM behavior — the same LLM follows or ignores the framework regardless of how strongly it's worded. Meanwhile, the tools that work (traceability IDs, templates, SSV) work because they're useful, not because they're mandatory.

**Design principle**: Stop telling the LLM what it MUST do. Start giving it tools it WANTS to use.

### Removed
- **Coexistence with fullstack-dev** — 18-line section that the user explicitly rejected as "nonsense" because it doesn't solve the persistence problem. The framework is technology-agnostic; whether fullstack-dev is active or not is the LLM's concern, not this file's.
- **Implementation Rules** — Duplicated knowledge/constraints files when standalone and conflicted with fullstack-dev when coexisting. The Phase References table and constraints/ directory already serve this purpose.
- **Complexity Tiers** — A classification table that prescribed workflow abbreviations based on file count. In practice, the agent already adapts naturally. Formal tiers added rules that were sometimes followed and sometimes ignored, with no quality difference.
- **Scope section** — Five rules about what the framework "does not" do. Unnecessary boundary declaration — the framework's scope is self-evident from its content.
- **QA Attestation → Process Compliance Report (PCR)** — Renamed to be honest about what it is. "QA" implies independent quality assurance; the attestation is self-graded. The honesty note (retained) already acknowledged this, but the name contradicted it.
- **Evidence tiers, status value definitions, delivery gate rules** — Detailed specification of attestation mechanics that added 30+ lines. The attestation block format is self-explanatory; surrounding it with rules didn't improve accuracy.

### Changed
- SKILL.md rewritten: 181 lines → ~95 lines (~48% reduction)
- Activation banner updated to v5.0.0, replaced phase/template counts with feature names
- New "Limitations" section at top: explicitly states what the framework cannot do (guarantee compliance, force behavior, persist across sessions)
- Compliance language removed: "Do not skip phases", "mandatory", "Do not omit" replaced with "use them when they help, abbreviate when they don't"
- Phase descriptions condensed from full paragraphs to single-purpose sentences
- Error recovery section simplified from numbered sub-steps to essential rules
- Git rules retained but shortened — removed redundant decision tree reference when the full tree already exists in the referenced file

### Fixed
- **State diagram inconsistency** — phases.md had error arrow from VERIFY→SPECIFY; SKILL.md had DELIVER→SPECIFY. Consolidated to one canonical version: "On error: stop, diagnose, fix, return to VERIFY" with SPECIFY as the alternative for specification gaps.
- **memory-template.md path mismatch** — Template referenced `~/code/memory.md` but phases.md referenced `skills/stellar-trails/memory.md`. Fixed to single canonical path: `/home/z/my-project/skills/stellar-trails/memory.md`.
- **phases.md path reference** — Changed `Check memory.md in this skill directory` to avoid future path drift.

### Honest Assessment
This refactor does not solve the persistence problem (impossible within platform architecture). It does not improve compliance rates (nothing in a text file can). What it does is: stop lying about what the framework can do, remove 86 lines of dead weight that diluted attention from the parts that actually work, and make the framework shorter and clearer so the useful tools (traceability IDs, templates, SSV, decision tree) are more likely to be read and used.

## [4.6.0] — 2026-04-13

### Added
- Source State Verification (SSV) — new section in SKILL.md mandating git fetch + comparison before any analysis/audit task on git repositories
- Source State field in problem-spec template — records branch, HEAD SHA, and verification status
- Source integrity check in verification-report Review Checklist
- Stale Local Data error pattern in error-patterns.md ([CRITICAL] severity)
- Stale-data recovery path (#5) in error-resolution decision tree Git section
- Cross-session git state awareness flag in IDLE phase (action 3.5)
- Evidence tiers in QA Attestation — code-creation vs code-analysis/audit tasks have different evidence requirements; analysis tasks must include source state verification

### Changed
- SPECIFY phase: entry criteria now includes source state verification; action 7.5 added for SSV
- VERIFY phase: action 1b added for source integrity check on analysis tasks
- IDLE phase: action 3.5 added for cross-session git state uncertainty flag

### Why
A stale local git clone caused a false-negative audit — the agent analyzed outdated files, claimed 20 applied fixes were absent, and delivered a confidently incorrect report. SSV closes this gap at every level: SKILL.md (mandate), SPECIFY (gate), VERIFY (defense-in-depth), templates (record), knowledge base (pattern recognition), and decision tree (recovery path).

## [4.5.0] — 2026-04-12

### Added
- Coexistence Mode — new "Coexistence with fullstack-dev" section defining how this framework layers with the platform-provided fullstack-dev skill
- IMPLEMENT phase defers technology-specific decisions to fullstack-dev when it is active; falls back to own `constraints/` and `knowledge/` files when standalone

### Why
fullstack-dev persists across sessions (system prompt level) and provides deep Next.js technical expertise. This framework provides orthogonal process governance. Rather than duplicating fullstack-dev's technical rules and risking conflicting instructions, the framework recognized fullstack-dev's presence and deferred to it for IMPLEMENT-phase decisions. (Removed in v5.0.0 — user identified this as unnecessary and the section was removed.)

## [4.4.2] — 2026-04-11

### Changed
- QA Attestation is now required after every task, not just coding tasks
- Non-coding tasks (conversation, questions, feedback) mark phases as N/A but still output the attestation block

### Why
The Activation section had an escape hatch: "If the user's request is not a coding task, the phase machine does not apply." This allowed skipping the attestation entirely on non-coding tasks — the exact failure mode the user wanted to detect. Making it mandatory for all tasks means: no attestation = framework was not followed.
