# Template Contracts

## Required Spec Files

Each live spec must contain:
- `meta.json`
- `requirements.md`
- `design.md`
- `tasks.md`
- `handoff.md`
- `notes.md`

## meta.json

Required keys:
- `spec_id`
- `title`
- `spec_kind`
- `status`
- `phase`
- `current_batch`
- `next_action`
- `complexity_reasons`
- `deliverables`
- `blockers`
- `last_checkpoint_type`
- `last_checkpoint_at`
- `last_actor`
- `last_updated_files`
- `created_at`
- `updated_at`
- `archive`

## tasks.md

Rules:
- Each task must have a stable ID such as `P1-B2-T3`.
- Each task must have `done_definition`.
- Each task must have `evidence`.
- Only one `current_batch` may be active at a time.

## handoff.md

Required sections:
- `Current Status`
- `Checkpoint Type`
- `Completed This Round`
- `Current Blockers`
- `Failed Attempts And Corrections`
- `Next Exact Action`
- `Evidence`
- `Resume Order`
- `Notes For Next Session`

## Steering Files

Stable workspace context belongs in:
- `steering/workflow.md`
- `steering/preferences.md`
- `steering/product.md`
- `steering/tech.md`
- `steering/structure.md`

Task-specific details do not belong in steering.
