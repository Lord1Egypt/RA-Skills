# Dogfood Run 002 — skill-release-lifecycle self-evaluation

## Date

2026-05-24

## Tested Skill

- Lifecycle under test: `skill-release-lifecycle`
- Evaluated file: `/root/.hermes/skills/workflow-kits/skill-release-lifecycle/SKILL.md`
- Evaluation type: A–E gate self-assessment against own criteria

## Input Used

Local SKILL.md, all sections reviewed via direct inspection.
Dogfood run record: `references/dogfood-run-001-waste-audit.md` (used as reference-derived evidence for previous run context).
No `clawhub inspect`, no public page verification — pre-release local assessment only.

## A–E Gate Results

### A. Utility / Recurrence — PASS

**Evidence:**

- 1 non-trivial dogfood run completed against `waste-audit` as the test case — recorded in `references/dogfood-run-001-waste-audit.md`
- Skill type: documentation / checklist / meta workflow → minimum threshold is 1 run → threshold met
- Output was produced and acted upon: gate assessment was written, three lifecycle issues were identified and patched, patch verification report was produced
- Dogfood run record documents issues found: evidence-source labeling ambiguity, anti-scope placement rule ambiguity, changelog-location ambiguity — all subsequently patched

**Evidence source:** `direct inspection` (current SKILL.md) + `reference-derived` (dogfood-run-001-waste-audit.md record)

**Note:** The "at least 2 distinct input scenarios when multiple runs are available" clause is satisfied by the conditional framing. With 1 run available, the 2-scenario requirement does not apply as a hard gate condition.

### B. Identity — PASS

**Evidence:**

- Narrow scope: skill defines its job as "a publish/no-publish quality gate and post-release iteration loop for OpenClaw/ClawHub skills"
- Clear boundary with "This kit should not duplicate" list
- "When Not to Use" section provides explicit anti-scope content:
  - does not write SKILL.md syntax
  - does not run publish commands
  - does not cover personal local-only skills
  - does not optimize ClawHub ranking/distribution

**Evidence source:** `direct inspection` — SKILL.md lines 15–56

**Structural note (non-blocking):** The skill uses "When Not to Use" for anti-scope rather than a standalone "What This Will Not Do" section. Per the anti-scope placement rules (lines 161–165), new public skills "should" have a standalone section but existing skills with a clear anti-scope statement "may temporarily pass." A future re-release should convert this to a standalone section.

**Anti-scope rule check:**

- New public skill: standalone section not present — not fully compliant with preferred format
- Clear anti-scope statement exists in "When Not to Use" — satisfies the temporary pass provision
- Missing anti-scope content entirely — not applicable; content exists

### C. Safety — PASS

**Evidence:**

- Skill is documentation-only: describes process rules, not executable operations
- No default deletion, disabling, uploading, sending, committing, or production mutation described
- No tokens, API keys, credentials, or secrets appear in the skill content
- No destructive behavior paths described
- Default behavior is to evaluate, assess, and report — all read-only operations

**Evidence source:** `direct inspection` — full SKILL.md content reviewed

### D. UX — PASS

**Evidence:**

- Clear purpose statement: "A publish/no-publish quality gate and post-release iteration loop"
- Clear "When to Use" and "When Not to Use" sections
- Clear workflow structure with numbered parts and labeled sections
- Clear output contract in the Quick Report Template
- "Do not call it Stable. Do not modify clawhub-auto-publish." appears explicitly as an execution constraint

**Soft note (non-blocking):** The skill does not include a user-facing activation phrase or install command. For a documentation/meta workflow skill, this is acceptable per the risk table. The skill activates through agent reasoning, not through a user command phrase.

### E. Maintenance — PASS

**Evidence:**

- Feedback path: "DM me on X: @BeeGeeEth" in dogfood-run-001-waste-audit.md — evidence source is `reference-derived`
- Version bumps tied to actual changes: patches from dogfood run applied, version bump to 0.2.0 pending
- Changelog evidence location clearly defined in skill itself
- Post-release iteration loop defined in Part 3 with 7 explicit steps
- Decision rules for feedback are explicit

**Evidence source:** `direct inspection` (changelog location rule, iteration loop structure) + `reference-derived` (dogfood run record for feedback path)

**Changelog evidence:** No changelog section in current SKILL.md. Changelog evidence lives in `references/dogfood-run-001-waste-audit.md`. Per the skill's own rule, the gate report cites where changelog evidence was found.

## Gate Summary

| Gate | Type | Result | Hard Blocker? |
|---|---|---|---|
| A. Utility / Recurrence | HARD | PASS | No |
| B. Identity | HARD | PASS | No |
| C. Safety | HARD | PASS | No |
| D. UX | SOFT | PASS | No |
| E. Maintenance | SOFT | PASS | No |

**All gates pass. Release approved from gate perspective.**

## Pre-release Metadata Changes Required

- `version: 0.1.0` → `version: 0.2.0` — reflects post-dogfood patch
- `status: draft` → `status: experimental` — aligns with Public Experimental label
- Add visible `Release status: Public Experimental` line in body

## Structural Issue Found and Fixed

The Pre-release Verification section had a duplicate numbering error: steps 2 and 3 appeared twice (source-of-truth check duplicated, then activation check appeared with the wrong number, then anti-scope and safety checks also used wrong numbers starting from 2 and 3). Fixed to a clean sequential 1–7 list.

## Lessons Learned

1. When a skill evaluates itself, evidence source labeling is particularly important to distinguish between what was directly inspected versus reference-derived from prior dogfood records.
2. Anti-scope placement rules create a structural preference vs. a hard fail for existing skills. The distinction matters: temporary pass is allowed but a future re-release should clean up the format.
3. For documentation/meta workflow skills, the absence of a user-facing activation phrase is not a hard UX gate failure — the skill activates through agent reasoning rather than command invocation.
4. The Pre-release Verification steps must be numbered cleanly. Duplicate numbering (steps 2 and 3 appearing twice) is a structural error that should be caught in the local review step.