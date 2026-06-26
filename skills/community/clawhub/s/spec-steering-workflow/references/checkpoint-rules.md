# Checkpoint Rules

## Valid Checkpoints

Only these checkpoint types are valid:
- `done`
- `blocked`
- `failed`

Anything like "still working", "continuing", or "in progress" is invalid.

## When To Checkpoint

Write a checkpoint when:
- A batch finishes
- 20 to 30 minutes have passed
- You are about to stop
- You are changing sessions
- A failure happens
- A blocker is discovered

## Required Updates

Every checkpoint must update:
- `meta.json.last_checkpoint_type`
- `meta.json.last_checkpoint_at`
- `meta.json.current_batch`
- `meta.json.next_action`
- `meta.json.last_updated_files`
- `handoff.md`

If task completion changed, update `tasks.md` too.

## Required Handoff Content

Each checkpoint entry in `handoff.md` must contain:
- `Checkpoint Type`
- `Completed This Round`
- `Current Blockers`
- `Failed Attempts And Corrections`
- `Next Exact Action`
- `Evidence`

## Quality Bar

Checkpoint content must be factual and verifiable:
- Completed items should name exact tasks or deliverables.
- Blockers should state what is missing.
- Failed checkpoints should say what failed, why, and what changed next.
