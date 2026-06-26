# Evolution Rules

Use this file when creating, approving, publishing, rolling back, or auto-promoting managed skills.

## Workspace Assumptions

- The current workspace root is the only writable scope for this skill.
- Create state files only inside the current workspace.
- Never inspect or modify global skill directories as part of this skill.

## Runtime State

Create these on first use if they do not already exist:

- `./.skill-evolver/candidates/`
- `./.skill-evolver/backups/`
- `./.skill-evolver/audit/`
- `./.skill-evolver/registry.json`
- `./.skill-evolver/config.json`

Initialize `./.skill-evolver/registry.json` with:

```json
{
  "version": 1,
  "records": []
}
```

Initialize `./.skill-evolver/config.json` with:

```json
{
  "version": 1,
  "autonomy_mode": "manual"
}
```

## Autonomy Modes

Supported values:

- `manual`
- `assisted`
- `autonomous`

Mode behavior:

- `manual`
  - create candidates only
  - require human approval before publish
- `assisted`
  - auto-approve low-risk updates
  - keep publishing manual
- `autonomous`
  - auto-publish low-risk `patch_skill` updates to `main`
  - auto-publish low-risk `create_skill` candidates to `canary`
  - leave medium- and high-risk changes in review

## Registry Fields

Each registry record must contain these fields:

- `candidate_id`
- `status`
- `source_summary`
- `signal_type`
- `signal_count`
- `target_skill`
- `change_type`
- `risk_level`
- `dedupe_basis`
- `merged_into`
- `matched_rules`
- `source_tools`
- `diff_summary`
- `failure_reason`
- `review_suggestions`
- `revision_count`
- `created_at`
- `approved_at`
- `published_version`
- `rollback_of`
- `publish_effect`
- `autonomy_mode`
- `promotion_channel`

Recommended status values:

- `pending_review`
- `approved`
- `rejected`
- `published`
- `rolled_back`
- `merged`
- `revision_requested`

## Structured Audit Log

Write one JSON audit artifact per lifecycle event into `./.skill-evolver/audit/`.

Recommended file name format:

- `YYYYMMDD-HHMMSS-<event>-<id>.json`

Every audit event should capture:

- `event_type`
- `candidate_id`
- `target_skill`
- `status_before`
- `status_after`
- `decision_reason`
- `matched_rules`
- `dedupe_basis`
- `diff_summary`
- `failure_reason`
- `publish_effect`
- `autonomy_mode`
- `promotion_channel`

Recommended event types:

- `candidate_created`
- `candidate_merged`
- `candidate_approved`
- `candidate_rejected`
- `candidate_revised`
- `candidate_published`
- `skill_rolled_back`
- `mode_changed`

## Naming

- Candidate id format: `candidate-YYYYMMDD-HHMMSS-<slug>`
- New managed skill format: `learned-<slug>`
- Canary skill format: `learned-<slug>-canary`
- Backup directory format: `./.skill-evolver/backups/<skill-name>/`
- Backup file format: `YYYYMMDD-HHMMSS-v<version>-SKILL.md`

## Allowed Change Types

Candidates may only use these `change_type` values:

- `create_skill`
- `patch_skill`
- `deprecate_skill`

Use:

- `create_skill` for a new `learned-<slug>` skill
- `patch_skill` when updating an existing managed skill
- `deprecate_skill` when marking a managed skill as obsolete and guiding the user away from it

## Candidate Creation Procedure

1. Confirm the workflow is reusable and safe.
2. Read existing managed skills under `./skills/learned-*/SKILL.md`.
3. Read non-final candidates under `./.skill-evolver/candidates/`.
4. Determine whether the workflow is:
   - a patch to an existing managed skill
   - a merge into an already-open candidate
   - a genuinely new skill
5. Prefer reuse over proliferation. Only create a new `learned-<slug>` skill when no safe target fits.
6. Derive the target skill:
   - If an existing managed skill already matches the workflow, target that skill and use `patch_skill`.
   - If a pending candidate already targets the same workflow, update or merge that candidate instead of creating a new one.
   - Otherwise create a new `learned-<slug>` skill and use `create_skill`.
7. Record the dedupe decision in `dedupe_basis`.
8. Render the proposed skill from [../templates/managed-skill-template.md](../templates/managed-skill-template.md).
9. Render the candidate record from [../templates/candidate-record-template.md](../templates/candidate-record-template.md).
10. Write the candidate record to `./.skill-evolver/candidates/<candidate-id>.md`.
11. Append a registry record with:
   - `status: "pending_review"`
   - `approved_at: null`
   - `published_version: null`
   - `rollback_of: null`
   - `autonomy_mode: <current-mode>`
   - `promotion_channel: null`
12. Write a `candidate_created` audit event.
13. Apply the current autonomy mode only if the candidate stays within the allowed low-risk boundary.
14. Ask for review when the mode does not auto-promote the candidate.

## Dedupe And Merge Heuristics

Use these checks before creating a new managed skill:

1. Exact target match:
   - same target skill name
   - same core scenario
2. High overlap in:
   - trigger signals
   - required tools
   - standard steps
3. User intent overlap:
   - same repeated request pattern
   - same correction category
4. Existing candidate overlap:
   - same target and same problem class

Decision rules:

- If overlap is high and the target skill already exists, use `patch_skill`.
- If overlap is high and the target is still only a pending candidate, merge into that candidate and mark the newer record as `merged`.
- If overlap is low but adjacent, prefer patching over creating a second near-duplicate skill.
- Only create a new `learned-*` skill when the workflow is materially distinct in purpose, steps, or required tools.

`dedupe_basis` should briefly explain the decision, for example:

- `matched learned-foo on triggers+tools`
- `merged into candidate-20260409-103000-foo`
- `new workflow: no managed skill covers review+publish loop`

## Review Procedure

### `review skill candidates`

- Read `registry.json`
- Show candidates in `pending_review` or `approved`
- Keep the summary short and actionable

### `approve candidate <id>`

- Update the matching registry record to `status: "approved"`
- Set `approved_at` to the current ISO-8601 timestamp if missing
- Do not write into `./skills/`
- Write a `candidate_approved` audit event

### `reject candidate <id>`

- Update the matching registry record to `status: "rejected"`
- Do not modify published skills
- Set `failure_reason` when rejection is due to safety, duplication, or target mismatch
- Write a `candidate_rejected` audit event

### `revise candidate <id> with suggestions: <feedback>`

- Update the matching registry record to `status: "revision_requested"`
- Append the user's suggestions into `review_suggestions`
- Increment `revision_count`
- Revise the candidate draft to reflect the feedback while preserving safety constraints
- Return the candidate to `pending_review` after the draft is updated
- Write a `candidate_revised` audit event

### `show skill-evolver mode`

- Read `config.json`
- Return the current mode plus a one-line behavior summary

### `set skill-evolver mode <manual|assisted|autonomous>`

- Update `config.json`
- Write a `mode_changed` audit event
- Confirm the new mode and its publish behavior

## Auto-Promotion Procedure

Only allow auto-promotion when the candidate is `low` risk.

### `manual`

- keep the candidate in `pending_review`
- never auto-publish

### `assisted`

- auto-approve low-risk `patch_skill` and low-risk `deprecate_skill`
- keep low-risk `create_skill` candidates in review
- never auto-publish

### `autonomous`

- auto-publish low-risk `patch_skill` candidates to `main`
- auto-publish low-risk `create_skill` candidates to `canary`
- auto-approve, but do not auto-publish, low-risk `deprecate_skill`
- leave medium- and high-risk candidates in review

## Publish Procedure

Only publish when one of these is true:

- The candidate status is already `approved`
- The tool is auto-promoting a low-risk candidate under the current mode
- The user gives an unambiguous direct reply to the current publish prompt

Publish steps:

1. Resolve the target skill name:
   - Use the candidate target by default
   - If the user supplied `as <name>`, normalize it to `learned-<slug>` for new skills
   - In autonomous mode, low-risk `create_skill` candidates may publish as `learned-<slug>-canary`
2. Validate the target path stays under `./skills/`
3. If `./skills/<skill-name>/SKILL.md` already exists:
   - Read it
   - Verify `managed-by: skill-evolver`
   - Refuse if the marker is missing
4. Determine `managed-version`:
   - `1` for new skills
   - increment the existing managed version for updates
5. Back up the previous `SKILL.md` into `./.skill-evolver/backups/<skill-name>/`
6. Write the new `SKILL.md`
7. Update the registry record:
   - `status: "published"`
   - `target_skill: "<final-name>"`
   - `published_version: <n>`
   - `publish_effect: "<short outcome>"`
   - `promotion_channel: "main" | "canary"`
8. Write a `candidate_published` audit event with a concise `diff_summary`

For v0, publish only a single `SKILL.md` file per managed skill.

## Rollback Procedure

1. Read `./skills/<skill-name>/SKILL.md`
2. Verify `managed-by: skill-evolver`
3. Find the newest backup in `./.skill-evolver/backups/<skill-name>/`
4. Restore that backup into `./skills/<skill-name>/SKILL.md`
5. Update the latest published registry entry for that skill:
   - `status: "rolled_back"`
   - `rollback_of: "<backup-file>"`
   - `publish_effect: "rolled back to previous managed version"`
6. Write a `skill_rolled_back` audit event

If the skill is unmanaged, or there is no backup, refuse.
