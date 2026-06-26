# Memory Template — Task List

Create `~/task-list/memory.md` only if the user wants continuity across sessions.

```markdown
# Task List Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Context
- Activation preference:
- Default buckets:
- Date semantics:
- Review rhythm:
- Project style:
- Area vocabulary:
- Typical overload signals:

## Notes
- Current planning horizon:
- Recurring commitments worth keeping visible:
- Waiting patterns or follow-up rules:
- Durable corrections about sorting, naming, or prioritization:

---
*Updated: YYYY-MM-DD*
```

## Optional Support Files

If the user wants full continuity, create these files too:

- `~/task-list/inbox.md` — unclarified captures
- `~/task-list/tasks.md` — active tasks across Today, Upcoming, Anytime, Someday
- `~/task-list/projects.md` — finite outcomes and next actions
- `~/task-list/areas.md` — ongoing responsibilities
- `~/task-list/recurring.md` — recurrence rules and last completion
- `~/task-list/waiting.md` — delegated or blocked items
- `~/task-list/log.md` — recently completed, dropped, or major changes

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | preferences still evolving | keep learning from normal task-list use |
| `complete` | working model is stable | apply defaults with minimal follow-up |
| `paused` | setup or updates paused | use stored context without pushing for more |
| `never_ask` | user declined setup questions | do not reopen setup unless they ask |

## Integration Values

| Value | Meaning |
|-------|---------|
| `pending` | activation boundary not decided yet |
| `done` | activation preference saved in main memory |
| `declined` | user wants manual invocation only |

## Key Principles

- Keep memory short enough to scan before acting.
- Save user-stated rules and durable patterns, not every daily task.
- Update `last` whenever the local task-list workspace changes.
- Ask before widening storage from lightweight memory into the full task workspace.
