---
name: spec-steering-workflow
description: Use a lightweight spec + steering workflow for long, interruptible, multi-phase tasks that need checkpointed progress, recoverable state, and multi-session continuity.
user-invocable: true
metadata: {"openclaw":{"homepage":"https://clawhub.ai/skills?sort=downloads"}}
---

# Spec Steering Workflow

Use this skill when work is long, interruptible, multi-phase, or needs recovery in a new session.

Start or recommend a spec when any of these are true:
- The task is likely to take more than 20 minutes.
- The task has more than one deliverable.
- The task needs staged execution.
- The task is likely to be interrupted.
- The task needs research plus execution.
- The task must survive across sessions.
- The user asks for plan first, then execution.

This skill manages execution state with workspace files:
- `specs/active/<spec-id>/`
- `specs/archive/<spec-id>/`
- `steering/`

Default workflow:
1. Read `steering/workflow.md` and `steering/preferences.md`.
2. If resuming, read `handoff.md`, then `tasks.md`, then `meta.json`.
3. Work only on the current batch.
4. After each batch, or every 20-30 minutes, write a checkpoint.
5. Before stopping, update `handoff.md` and `meta.json`.

Valid checkpoint types are only:
- `done`
- `blocked`
- `failed`

Do not treat "working on it", "continue", or "in progress" as valid progress reports.

Use `{baseDir}/scripts/specctl.py` for these operations:
- `init <spec-id> --title "<title>" --kind <kind>`
- `checkpoint <spec-id> --type done|blocked|failed --batch <batch-id> --next "<next action>"`
- `status <spec-id>`
- `resume <spec-id>`
- `validate <spec-id>`
- `archive <spec-id>`
- `set-status <spec-id> --status ready|review|completed [--phase <phase>] [--next "<next action>"]`
- `doctor`

Read references only as needed:
- `{baseDir}/references/workflow-rules.md` for trigger and lifecycle rules
- `{baseDir}/references/checkpoint-rules.md` for checkpoint requirements
- `{baseDir}/references/recovery-rules.md` for resume order and stale-state rules
- `{baseDir}/references/integration-rules.md` for coexistence with other skills
- `{baseDir}/references/template-contracts.md` for file contracts and required fields

Use templates from `{baseDir}/assets/templates/`. Keep the skill lean: detailed rules belong in `references/`, file bodies belong in `assets/templates/`, and only execution state belongs in workspace `specs/` and `steering/`.
