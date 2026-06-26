# Workflow Steering

## When To Start A Spec

Prefer a spec workflow when any one of these is true:
- Estimated effort is greater than 20 minutes
- There is more than one deliverable
- The work needs multiple phases
- The work is likely to be interrupted
- The work needs research plus execution
- The work must survive across sessions
- The user asked for plan first, then execution

## Execution Loop
1. Open or create the spec.
2. Read `handoff.md`, `tasks.md`, and `meta.json`.
3. Work on one batch only.
4. Write a checkpoint after each batch or every 20-30 minutes.
5. Before leaving, update `handoff.md` and `meta.json`.

## Valid Checkpoints
- `done`
- `blocked`
- `failed`

## Recovery Order
1. `handoff.md`
2. `tasks.md`
3. `meta.json`
4. `requirements.md` and `design.md` if needed

## Archive Policy
1. Move the spec to `completed`.
2. Archive to `specs/archive/<spec-id>/`.
3. Mark `meta.json.archive.is_archived` as `true`.
