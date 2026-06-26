# Views and Sorting — Task List

## Core buckets

- `Inbox` — captured but not clarified enough to execute
- `Today` — should be visible now
- `Upcoming` — dated work not ready for Today
- `Anytime` — no current date pressure
- `Someday` — intentionally deferred ideas
- `Waiting` — delegated or blocked on someone else
- `Done` — completed and ready to roll out of the active list

## Deterministic ordering

Within a view, sort in this order:
1. Overdue due dates
2. Due today
3. Start date reached
4. High-priority items
5. Manual or intentional order
6. Everything else by oldest unresolved change

If two tasks tie on all fields, keep their previous visible order.

## Today rules

- `Today` is a focused working set, not the whole backlog.
- Pull in items explicitly scheduled for today, due today, or manually promoted by the user.
- Overdue items do not automatically flood `Today`; surface them as risk, then ask whether to promote, defer, or drop.

## Upcoming rules

- Show dated tasks in chronological order.
- Separate "starts showing" from "due by" when both exist.
- Keep recurring work visible only at its next intended appearance, not every future occurrence.

## Waiting rules

- Keep owner, blocker, and next chase date visible.
- Do not hide waiting items inside generic project notes.
- Surface stale waiting items during review even if they are not due today.
