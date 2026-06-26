---
name: skill-evolver
description: Let OpenClaw capture reusable workflows as managed skill candidates, support review or revision, and evolve safely through manual, assisted, or autonomous modes inside the current workspace.
user-invocable: true
argument-hint: "[ACTION=<review|approve|reject|revise|publish|rollback|show-mode|set-mode>] [ID=<candidate-id>] [NAME=<skill-name>]"
metadata:
  openclaw:
    always: true
    skillKey: skill-evolver
---

Manage a safe, mode-aware skill evolution loop inside the current workspace.

This skill is always on. Its job is to notice reusable workflows, turn them into managed skill candidates, support review and user suggestions, publish approved changes into `./skills/`, and roll them back when needed.

## Installation And Runtime Modes

This skill supports two install paths:

- standalone skill install
  - installed directly from ClawHub into the workspace `skills/` directory
  - works without any plugin
  - uses built-in file tools plus the policy files in this skill folder
- plugin-backed install
  - installed as part of the TrustLoop managed-skill plugin
  - the plugin bundles this skill and registers the native `skill_manage_managed` tool
  - preferred when available because candidate review, publish, rollback, and mode changes become safer and more reliable

Do not fail just because the plugin is missing.

If `skill_manage_managed` is available, prefer it for lifecycle mutations such as:

- `create_candidate`
- `merge_candidate`
- `get_mode`
- `set_mode`
- `review_candidate`
- `publish_candidate`
- `rollback_skill`

If that tool is not available, continue in pure skill mode using built-in file tools and the references/templates shipped with this skill.

## Scope

Only manage skills in the current workspace, and only when one of these is true:

- The target directory is `./skills/learned-<slug>/`
- The target `SKILL.md` frontmatter contains `managed-by: skill-evolver`

Refuse to modify:

- bundled skills
- third-party installed skills
- user-authored skills without the `managed-by: skill-evolver` marker
- any candidate that introduces dangerous commands, sensitive-path access, secret handling, or data exfiltration

Before any publish or rollback action, read [references/review-policy.md](references/review-policy.md). For lifecycle details and state layout, read [references/evolution-rules.md](references/evolution-rules.md). For the native-tool path, read [references/skill-manage-managed-tool.md](references/skill-manage-managed-tool.md).

## State Layout

All runtime state lives in the workspace root:

- `./.skill-evolver/candidates/`
- `./.skill-evolver/backups/`
- `./.skill-evolver/audit/`
- `./.skill-evolver/registry.json`
- `./.skill-evolver/config.json`

Published managed skills live only in:

- `./skills/learned-<slug>/SKILL.md`

Initialize missing state directories, `registry.json`, or `config.json` only when needed.

## Autonomy Modes

The learning loop supports three modes:

- `manual`
  - default mode
  - create candidates, ask for review, and require a human approval before any publish
- `assisted`
  - auto-approve low-risk updates such as low-risk `patch_skill`
  - keep all publishing manual
- `autonomous`
  - auto-publish low-risk `patch_skill` updates to the managed skill directly
  - auto-publish low-risk `create_skill` candidates as `learned-*-canary`
  - keep medium- and high-risk changes in review

Treat `manual` as the safe default unless the user explicitly changes mode.

## User Experience Rules

Keep the learning loop helpful, quiet, and low-friction.

- Stay silent when no candidate should be created.
- Do not require plugin installation before the user can get value from the skill.
- Do not interrupt the middle of a task just to announce learning.
- Only raise a review request after the task is complete or the user has already shifted into review mode.
- Keep prompts short and concrete:
  - what was learned
  - where it would be published
  - what the user can do next
- Prefer one lightweight prompt over a long explanation.
- Treat user suggestions as collaboration, not failure.
- After publish, confirm success in one short message and mention rollback only if useful.
- When a candidate is merged or deduped, explain that briefly so the user understands why a new skill was not created.
- When a mode auto-approves or auto-publishes something, say so clearly in one sentence.

## When To Create A Candidate

Create a candidate only when at least one of these is true:

- A task completed successfully after multiple meaningful tool calls
- The user explicitly corrected the approach
- The same request pattern appeared at least twice in the current workspace history you can see
- A failed path was recovered into a stable reusable workflow

Do not create a candidate for trivial one-step actions, one-off facts, or workflows that depend on unsafe behavior.

## Candidate Workflow

When a reusable workflow should be learned:

1. Read [templates/managed-skill-template.md](templates/managed-skill-template.md) and [templates/candidate-record-template.md](templates/candidate-record-template.md).
2. Check existing managed skills and open candidates before creating anything new.
3. Prefer `patch_skill` when the workflow materially overlaps an existing managed skill or pending candidate.
4. Use `create_skill` only when no safe existing target matches.
5. Use `deprecate_skill` only for already-managed skills that should stop being used.
6. Classify risk using [references/review-policy.md](references/review-policy.md).
7. Detect whether the native `skill_manage_managed` tool is available.
8. Read the current autonomy mode from `./.skill-evolver/config.json` or from the native tool.
9. Render a single-file managed skill draft from the managed skill template.
10. If the native tool is available, prefer it for candidate creation, merge handling, registry updates, and audit writes.
11. If the native tool is not available, write the candidate record to `./.skill-evolver/candidates/<candidate-id>.md`.
12. If the native tool is not available, insert or update the registry record in `./.skill-evolver/registry.json`.
13. If the native tool is not available, write a structured audit event into `./.skill-evolver/audit/`.
14. If the current mode allows auto-approval or auto-publish for this low-risk candidate, explain the action briefly.
15. Otherwise reply with a short approval request such as: `I found a reusable workflow and created candidate <id> for learned-foo. Publish it?`

Never auto-publish medium- or high-risk candidates.
When a candidate clearly duplicates another pending candidate, merge into the older candidate or patch the shared target skill instead of creating a new `learned-*` skill.
Keep the candidate-creation prompt short enough that the user can decide quickly without reading the whole draft.

## Review Commands

Support these direct commands and close natural-language equivalents:

- `review skill candidates`
- `approve candidate <id>`
- `reject candidate <id>`
- `revise candidate <id> with suggestions: <feedback>`
- `publish candidate <id> as <name>`
- `rollback skill <name>`
- `show skill-evolver mode`
- `set skill-evolver mode <manual|assisted|autonomous>`

Behavior:

- `review`: list pending or approved candidates with `candidate_id`, `target_skill`, `change_type`, `risk_level`, and a one-line summary
- prefer the native `skill_manage_managed` tool for lifecycle mutations when it is available
- `approve`: mark the candidate approved in `registry.json`, set `approved_at` if empty, and do not write into `./skills/`
- `reject`: mark the candidate rejected and do not modify published skills
- `revise`: record the user's optimization suggestions, increment the candidate revision count, keep the candidate in review, and update the draft before asking again
- `publish`: only allowed after approval, or after an unambiguous direct user reply to the publish prompt
- `rollback`: restore the latest backup for a managed skill and update the registry
- `show mode`: read `./.skill-evolver/config.json` and explain the current mode in one short sentence
- `set mode`: update `./.skill-evolver/config.json` and confirm the new mode plus its publish behavior
- always include dedupe or merge notes when they exist

Silence is never approval.
When the user gives optimization feedback during review, treat it as a revision request rather than a rejection unless they explicitly reject the candidate.
Accept natural-language review feedback when the intent is clear, even if the user does not use the exact command syntax.

## Publish Rules

When publishing a candidate:

1. Confirm the target stays inside `./skills/`.
2. If the target already exists, verify it is managed by `skill-evolver`.
3. Back up the current published skill into `./.skill-evolver/backups/<skill-name>/`.
4. Write the approved skill draft to `./skills/<skill-name>/SKILL.md`.
5. Ensure the published skill frontmatter includes:
   - `managed-by: skill-evolver`
   - `managed-version: <n>`
   - `published-from-candidate: <candidate-id>`
6. Update the registry status to `published` and set `published_version`.
7. Record the publish channel as `main` or `canary`.
8. Write a publish audit event with the final diff summary, backup path, and publish result.

For v0, managed skills should stay single-file unless the user explicitly asks for richer supporting files later.
Autonomous mode may publish low-risk new skills as `learned-*-canary`, but that does not remove the need for human review on higher-risk changes.

## Rollback Rules

When the user asks to roll back a skill:

1. Verify the skill is managed by `skill-evolver`.
2. Restore the latest backup into `./skills/<skill-name>/SKILL.md`.
3. Mark the latest published registry entry as `rolled_back`.
4. Set `rollback_of` to the restored backup identifier or path.
5. Write a rollback audit event.

If the skill is unmanaged or no backup exists, refuse and explain why.
