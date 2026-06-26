# Tasks

## Rules
- Every task must be verifiable.
- Do not use placeholders like "continue optimizing" or "keep working".
- Only one current batch may be active at a time.

## Current Batch
- batch_id: B1
- objective: <clear batch objective>
- done_definition: <what makes this batch done>
- next_action: <single next action>

## Phase 1

### Batch B1
- [ ] P1-B1-T1 Capture current state and boundaries
  - done_definition: The current state is summarized with concrete constraints.
  - evidence: <path or artifact>
- [ ] P1-B1-T2 Draft requirements
  - done_definition: `requirements.md` has Goal, Scope, Deliverables, and Acceptance Criteria filled in.
  - evidence: specs/active/<spec-id>/requirements.md

### Batch B2
- [ ] P1-B2-T1 Draft design
  - done_definition: `design.md` contains summary, approach, key decisions, and risks.
  - evidence: specs/active/<spec-id>/design.md
- [ ] P1-B2-T2 Break work into executable tasks
  - done_definition: `tasks.md` has task IDs, done definitions, and evidence fields for each task.
  - evidence: specs/active/<spec-id>/tasks.md

## Completed Batches
- [ ] B1
- [ ] B2

## Blocked Tasks
- None
