# `skill_manage_managed` Minimal Tool Interface

This file describes the recommended minimal native tool for upgrading `skill-evolver` from a pure-skill workflow into a safer, more reliable managed-skill system.

## Why Add A Tool

The current v0 skill can work using OpenClaw's built-in file tools such as `read`, `write`, `edit`, and `apply_patch`, plus workflow rules in `SKILL.md`.

That is enough for:

- candidate drafting
- registry updates
- approval-gated publishing
- rollback with backups
- basic dedupe and merge guidance

But it is not ideal for:

- reliable dedupe and merge decisions
- atomic registry plus file updates
- structured auditing
- mode-aware auto-promotion
- preventing accidental writes outside managed scope
- making publish and rollback idempotent

For that, a dedicated tool is the better next step.

## Can OpenClaw Use This Directly

Yes, but not as a built-in tool today.

OpenClaw skills can define tool schemas or instruct the agent to use existing system tools, and plugins can register additional native tools. OpenClaw's docs say tools are typed functions the agent can invoke, plugins can register additional ones, and native plugins can register tools, hooks, and services in-process.

Implication:

- pure skill v0: works today with built-in file tools
- `skill_manage_managed` tool: requires a small custom OpenClaw plugin or another tool-providing extension

## Minimal Tool Surface

Prefer one narrow tool with explicit operations rather than many loosely scoped tools.

Tool name:

- `skill_manage_managed`

Operations:

- `create_candidate`
- `merge_candidate`
- `get_mode`
- `set_mode`
- `review_candidate`
- `publish_candidate`
- `rollback_skill`

## Input Schema

### Common fields

- `workspace_root`: absolute or session-resolved workspace root
- `operation`: one of the supported operations
- `candidate_id`: optional depending on operation
- `skill_name`: optional depending on operation
- `reason`: short human-readable reason

### `create_candidate`

- `source_summary`
- `signal_type`
- `signal_count`
- `proposed_skill_content`
- `target_skill`
- `change_type`
- `risk_level`
- `matched_rules`
- `source_tools`
- `diff_summary`
- `dedupe_basis`
- optional `autonomy_mode`

### `merge_candidate`

- `candidate_id`
- `merge_into_candidate_id`
- `reason`
- optional `replacement_skill_content`
- optional `diff_summary`

### `get_mode`

- `workspace_root`

### `set_mode`

- `autonomy_mode`: `manual`, `assisted`, or `autonomous`

### `review_candidate`

- `candidate_id`
- `decision`: `approve`, `reject`, or `revise`
- `failure_reason`: required when rejected
- `suggestions`: optional for approve, recommended for revise
- `replacement_skill_content`: optional revised draft content

### `publish_candidate`

- `candidate_id`
- optional `publish_as`

### `rollback_skill`

- `skill_name`

## Output Schema

Return a structured result:

```json
{
  "ok": true,
  "operation": "publish_candidate",
  "candidate_id": "candidate-20260409-120101-review-loop",
  "skill_name": "learned-review-loop",
  "status_before": "approved",
  "status_after": "published",
  "published_version": 2,
  "autonomy_mode": "autonomous",
  "promotion_channel": "main",
  "backup_path": "./.skill-evolver/backups/learned-review-loop/20260409-120100-v1-SKILL.md",
  "audit_path": "./.skill-evolver/audit/20260409-120101-candidate_published-candidate-20260409-120101-review-loop.json",
  "message": "Published learned-review-loop v2"
}
```

Return `ok: false` with:

- `error_code`
- `message`
- optional `blocking_record`

## Mode Semantics

### `manual`

- create candidates
- keep them in review
- require explicit human approval before publish

### `assisted`

- auto-approve low-risk updates
- keep publishing manual
- leave medium- and high-risk changes in review

### `autonomous`

- auto-publish low-risk `patch_skill` candidates to `main`
- auto-publish low-risk `create_skill` candidates only as `canary`
- auto-approve low-risk non-patch updates when safe
- leave medium- and high-risk changes in review

## Required Safety Guarantees

The tool should enforce these rules itself, not rely on prompt wording:

- only read and write inside the active workspace root
- only publish to `./skills/learned-*`
- only patch skills with `managed-by: skill-evolver`
- perform backup and publish atomically
- update registry and audit together
- reject unmanaged targets
- reject duplicate creates when patch or merge is the correct action
- store structured review suggestions and revision counts
- store the current `autonomy_mode` and `promotion_channel`
- never auto-publish outside the mode's low-risk policy

## Recommended Implementation Shape

Use a tiny OpenClaw plugin that registers exactly one tool plus optional helper hooks.

Suggested follow-up plugin responsibilities:

- validate paths
- normalize skill names
- read and write `registry.json`
- read and write `config.json`
- read and write candidate files
- write audit events
- compute dedupe decisions from managed skills and open candidates
- apply mode-aware auto-promotion

Keep the policy in the skill and the mutation logic in the tool.

That split gives you:

- better safety than pure prompt orchestration
- lower token cost for repetitive lifecycle operations
- behavior closer to Hermes `skill_manage`, but still scoped to managed workspace skills only
