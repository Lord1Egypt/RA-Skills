# Dogfood Run #1 — skill-release-lifecycle (waste-audit as test case)

**Date:** 2026-05-24
**Lifecycle version tested:** 0.1.0 → 0.1.1
**Test case:** `waste-audit` SKILL.md as A–E gate evaluation target

## What was tested

Applied the A–E gate to `waste-audit` using `skill-release-lifecycle` as the evaluation tool.
Ran the full lifecycle: gate evaluation → issue identification → patch → verification → handoff → publish.

## Three issues found in dogfood run #1

These three issues were identified during dogfood run #1 and patched in 0.1.1:

### 1. Evidence source labeling
**Issue:** Gate reports should distinguish `direct inspection` vs `reference-derived` vs `historical claim` vs `unverified`.
**Resolution:** Skill updated to explicitly label evidence source in gate reports (lines 255–259 of SKILL.md).
**Status:** Patched in 0.1.1.

### 2. Anti-scope placement rule
**Issue:** `waste-audit` had an anti-scope sentence under `Activation`, not a standalone "What This Will Not Do" section. The lifecycle wording was ambiguous about whether this passed or failed Identity.
**Resolution:** Anti-scope placement rules clarified (lines 161–165 of SKILL.md):
- New public skills: must have standalone "What This Will Not Do" section
- Existing published skills: may temporarily pass if they have a clear anti-scope statement
- Missing anti-scope entirely: Identity HARD Fail, no exception
**Status:** Patched in 0.1.1.

### 3. Changelog evidence location
**Issue:** `waste-audit` had no changelog section in SKILL.md. The lifecycle did not clarify whether changelog evidence could live in ClawHub release metadata, a release report, or a references file.
**Resolution:** Changelog evidence location rule added (lines 232–239 of SKILL.md):
- Evidence may live in: SKILL.md changelog, ClawHub release metadata, release report, or references file
- Gate report must cite where changelog evidence was found
**Status:** Patched in 0.1.1.

## Additional observations

- The lifecycle correctly applied A–E gates to `waste-audit` end-to-end
- The `references/publish-gate-example.md` was useful as a concrete example but slightly too clean — it did not expose the anti-scope and changelog ambiguities that dogfood did
- Recommended future update: add a `Notes / Ambiguities` subsection to `references/publish-gate-example.md` showing how to handle partial evidence
- The risk-based release threshold model (documentation/checklist tier = 1 run minimum) correctly allowed this skill to reach Public Experimental after one dogfood run
- No hard gate blockers were found for `skill-release-lifecycle` itself after patching the three issues

## Does this count?

Yes — counts as dogfood run #1 for `skill-release-lifecycle`.

Criteria met:
- Used a real published skill (`waste-audit`) as a non-trivial test case
- Applied A–E gate criteria end-to-end
- Produced actionable issue identification and patch
- Output was recorded and can be used for future patch decisions

## What would make this skill promotion-ready

- Dogfood run #2 with a different skill type (e.g., a read-only diagnostic skill) to confirm the risk-based threshold table applies correctly
- At least one more external signal or feedback item from real usage
- A standalone "What This Will Not Do" section (per the anti-scope preference for new public skills)