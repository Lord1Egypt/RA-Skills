# WORKING_STATE.md Format and Maintenance

WORKING_STATE.md is a structured file that captures the current state of
a long-running agent session. It serves as insurance against context
compaction and crashes — when the agent loses implicit context, it can
rebuild situational awareness from this file.

## Format

```markdown
# Working State

Last updated: [ISO timestamp]

## Current Task

- Slice/Task ID: [id]
- Description: [what we're doing]
- Phase: [RED/GREEN/DOMAIN/COMMIT/REVIEW/etc.]
- Status: [in-progress/blocked/waiting]

## Progress

- [x] Completed step 1
- [x] Completed step 2
- [ ] Current step 3
- [ ] Pending step 4

## Key Decisions

- [Decision and rationale]

## Files Modified This Session

- path/to/file.ext (what changed)

## Blocked On

- [What's blocking, who/what we're waiting for]
```

### Pipeline Controller Extension

When running as a pipeline controller, add:

```markdown
## Pipeline State

- Active slice: [slice-id]
- Gate: [current gate name]
- Gate checklist: [path to gate task list]
- Rework count: [N]
- Agents active: [list of agent names and their current tasks]
```

## Location

- **Pipeline mode:** `.factory/WORKING_STATE.md`
- **Standalone:** `WORKING_STATE.md` in project root

## Maintenance Rules

1. **Update after every significant state change.** Task start, phase
   change, decision made, blocker encountered, agent spawned/completed.
2. **Keep concise.** This is a reference document, not a journal. Current
   state only.
3. **Overwrite, don't append.** It represents current state, not history.
   Old state belongs in memory files or git history.
4. **Read FIRST after any interruption.** Context compaction, crash,
   session restart, or long idle period. Never guess state from memory.
5. **Never skip the read.** Even if you think you remember, read the file.
   Context compaction removes information you don't realize you've lost.

## Example: Pipeline Controller

```markdown
# Working State

Last updated: 2025-01-15T14:32:00Z

## Current Task

- Slice/Task ID: slice-003-user-authentication
- Description: Implementing user login with email/password
- Phase: REVIEW (code review before push)
- Status: waiting (review in progress)

## Progress

- [x] Slice decomposed into 4 leaf tasks
- [x] Pre-implementation context gathered
- [x] TDD pair dispatched (ping: kent-beck, pong: sandi-metz)
- [x] 3 TDD cycles completed, all tests passing
- [ ] Code review (3 reviewers activated)
- [ ] Mutation testing
- [ ] Push and CI
- [ ] Merge

## Key Decisions

- Used bcrypt for password hashing (ADR-007)
- Session tokens stored in Redis, not JWT (team consensus)

## Files Modified This Session

- src/auth/login.rs (login handler)
- src/auth/password.rs (bcrypt wrapper)
- tests/auth/login_test.rs (acceptance + 3 unit tests)

## Blocked On

- Waiting for code review results from 3 reviewers

## Pipeline State

- Active slice: slice-003-user-authentication
- Gate: review
- Gate checklist: .factory/audit-trail/slices/slice-003/gates.md
- Rework count: 0
- Agents active: reviewer-alice (stage 1), reviewer-bob (stage 2)
```

## Example: Standalone TDD

```markdown
# Working State

Last updated: 2025-01-15T10:15:00Z

## Current Task

- Task: Add drag-and-drop reordering to task list
- Phase: GREEN (making test pass)
- Status: in-progress

## Progress

- [x] Acceptance test written (drag task, verify new order persists)
- [x] Domain review: introduced Position value object
- [x] Unit test 1: Position.move_to (RED -> GREEN -> COMMIT)
- [ ] Unit test 2: TaskList.reorder (currently RED)
- [ ] Acceptance test GREEN
- [ ] Final domain review

## Key Decisions

- Position uses integer ordering with gap strategy (powers of 2)

## Files Modified This Session

- src/domain/position.rs (Position value object)
- tests/domain/position_test.rs (unit tests)
- tests/acceptance/reorder_test.rs (acceptance test, still failing)

## Blocked On

- Nothing — actively implementing
```
