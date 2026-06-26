# Dogfood Run 001 — skill-release-lifecycle (Self-Gate)

## Date

2026-05-24

## Tested Skill

- Skill under test: `skill-release-lifecycle`
- Case: self-gate evaluation against own SKILL.md at version 0.1.0 (pre-patch)
- Evaluated file: `/root/.hermes/skills/workflow-kits/skill-release-lifecycle/SKILL.md`

## Input Used

Self-evaluation using the skill's own A–E gate framework:
- Applied gates A–E to the current local SKILL.md
- Inspected all six parts of the lifecycle document
- Checked frontmatter, maturity ladder, anti-scope rules, changelog location rule, evidence labeling, install/activation/feedback sections

## A–E Gate Results

### A. Utility / Recurrence — PASS

- 1 non-trivial dogfood run completed (tested against `waste-audit`)
- Skill type: documentation / checklist / meta workflow → minimum threshold is 1 run → met
- Output was produced and acted upon: three issues identified, patches applied
- Skill is a recurring use case for the OpenClaw ecosystem

**Source:** direct inspection + reference-derived (dogfood-run-001-waste-audit.md)

### B. Identity — PASS (soft structural note)

- Narrow scope: publish/no-publish quality gate + iteration loop
- "When Not to Use" section (lines 49–56) provides explicit anti-scope content
- Structural note: uses "When Not to Use" rather than standalone "What This Will Not Do" section — acceptable under the temporary pass provision (line 163)
- Future re-release should convert to standalone section

**Source:** direct inspection

### C. Safety — PASS

- Documentation-only skill; no destructive operations described
- No secret exposure, no default mutation
- Default behavior is evaluate/assess/report — all read-only

**Source:** direct inspection (full file reviewed)

### D. UX — PASS (soft fix candidate)

- Clear purpose, workflow structure, output contract (Quick Report Template)
- Meta workflow skill — activation is through agent reasoning, not a user command phrase
- Acceptable per risk table for documentation/checklist skills

**Source:** direct inspection

### E. Maintenance — PASS

- Feedback path: DM on X (@BeeGeeEth) — source: reference-derived
- Version bumps tied to actual changes
- Changelog location rule defined; current evidence lives in dogfood run record
- Iteration loop with 7 explicit steps and decision rules

**Source:** direct inspection + reference-derived

## Issues Found (Pre-Patch)

Three dogfood run #1 issues were already identified in `dogfood-run-001-waste-audit.md`. This self-gate confirmed they were patched in the current SKILL.md:

1. **Evidence source labeling** — present in "How to Run the Gate" step 3 (lines 255–259)
2. **Anti-scope placement rules** — present in lines 161–165
3. **Changelog evidence location** — present in lines 232–239

## Soft Fixes Applied in Same Session

After gate pass, three soft fixes were applied before publishing:

1. **Install section added** — `openclaw skills install skill-release-lifecycle --global`
2. **Activation section added** — user-facing trigger statement
3. **Feedback section added** — DM path near end of document

## Frontmatter Updates Applied

- `version: 0.1.0` → `0.1.1`
- `status: draft` → `public-experimental` (duplicate status:draft line removed)

## Hard Gate Status

| Gate | Result | Hard Blocker? |
|---|---|---|
| A. Utility / Recurrence | PASS | No |
| B. Identity | PASS | No |
| C. Safety | PASS | No |
| D. UX | PASS | No |
| E. Maintenance | PASS | No |

**All hard gates pass. Eligible for Public Experimental release.**

## Handoff Decision

After version/status update: skill is ready for Public Experimental release.
Hand off to `clawhub-auto-publish` after all patches applied.
Do not call it Stable. Do not imply fully validated.