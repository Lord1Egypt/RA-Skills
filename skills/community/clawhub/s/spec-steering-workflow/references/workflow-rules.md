# Workflow Rules

## Purpose

This skill is an execution protocol for long tasks. It is not a memory system, not a self-improvement system, and not a project manager.

## Trigger Rules

Recommend creating a spec when any one of these is true:
- Estimated effort is greater than 20 minutes.
- There is more than one deliverable.
- The work must be split into phases or batches.
- The work is likely to be interrupted.
- The work needs research plus execution.
- The work must resume in a future session.
- The user explicitly asks for plan first, then execution.

## Directory Rules

Use:
- `specs/active/<spec-id>/` for live work
- `specs/archive/<spec-id>/` for completed work
- `steering/` for stable workspace context

The skill directory stores rules, templates, and scripts only. It does not store live task state.

## Lifecycle

Allowed spec statuses:
- `draft`
- `ready`
- `in_progress`
- `blocked`
- `review`
- `completed`
- `archived`

Allowed phases:
- `requirements`
- `design`
- `execution`
- `review`
- `done`

Transitions:
- `draft -> ready`: requirements, design, and tasks exist and at least one batch is actionable.
- `ready -> in_progress`: `current_batch` and `next_action` are both set.
- `in_progress -> blocked`: blockers exist and the current batch cannot move.
- `in_progress -> review`: deliverables are ready for acceptance.
- `review -> completed`: acceptance criteria are satisfied.
- `completed -> archived`: the spec directory has been moved to `specs/archive/`.

## Source of Truth

Execution truth lives in:
1. `meta.json` for structured state
2. `tasks.md` for executable checklist state
3. `handoff.md` for resume summary

If these conflict:
- Prefer `tasks.md` task completion and `meta.json.current_batch`.
- Fix the inconsistency in the next checkpoint.
