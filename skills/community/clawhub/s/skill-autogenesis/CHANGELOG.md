# Changelog

## 1.3.2

- Added hard stop rules that explicitly block invalid `skill_manage(create)` usage.
- Tightened lifecycle rules so only `knowledge_type=procedure` may enter procedural skill actions.
- Added `references/hard-stop-rules.md` with a fast test for valid skill candidates.
- Updated the README to surface hard interception behavior.

## 1.3.1

- Added a mandatory internal classification template before any persistence action.
- Added a checklist gate that must fully pass before create or patch is allowed.
- Extended verification rules so create and patch require a completed decision record.
- Updated the README to emphasize classification template first, file writes second.

## 1.3.0

- Added an explicit decision matrix to route outcomes to skill, memory, prompt, or no-op.
- Added an output contract so agents classify the result before writing files.
- Added a recurrence warning that repeated rules still do not qualify as skills without executable procedure.
- Added `references/classification-examples.md` with concrete examples of what should and should not become a skill.

## 1.2.2

- Changed the default posture from implied creation to explicit classification first.
- Added a hard gate that only executable reusable procedures may become skills.
- Added routing guidance for non-skill outcomes such as preferences, policies, boundaries, and prompt-level governance.
- Added a pitfall warning that rules are not skills unless they contain trigger, action, and verification.
- Updated the bilingual README to reduce the common misread that this skill should create a new rule after every success.

## 1.2.1

- Refined positioning to emphasize verification-gated skill creation rather than unconditional autonomous writes.
- Clarified that skill creation happens only when recurrence, stability, and environment policy permit it.
- Tightened README wording to better communicate lifecycle controls and safety boundaries.
- Kept local fallback reference behavior for GitHub sources.

## 1.2.0

- Added explicit source resolution policy: GitHub first, local fallback second, `[UNVERIFIED]` last.
- Added local fallback reference files under `references/fallback/`.
- Added `skill_manage`-style lifecycle handling for create, patch, edit, write_file, remove_file, and guarded delete.
- Added reusable template file for generated skills.

## 1.1.0

- Added lifecycle-oriented behavior modeled after `skill_manage`.
- Added support for supporting-file management and duplicate-skill avoidance.

## 1.0.0

- Initial release.
- Added automatic workflow distillation, recurrence detection, and skill generation guidance.
