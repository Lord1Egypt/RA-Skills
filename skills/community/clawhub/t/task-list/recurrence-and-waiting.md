# Recurrence and Waiting — Task List

## Date semantics

- `Due` means the task becomes painful or late after that date.
- `Start` or `defer` means the task should begin appearing on that date.
- `Completed` records when the user actually finished it.

Never overwrite one field just because another changed.

## Recurrence rules

- Preserve the user's wording if possible: every weekday, every Friday, first business day, every two weeks after completion.
- Regenerate from the correct anchor:
  - calendar-based rules use the calendar date
  - completion-based rules use the completion timestamp
- When a recurring item completes, create the next occurrence and log the regeneration.

## Waiting state

Use `Waiting` when progress depends on another person, team, or external event.

Each waiting item should keep:
- who or what it depends on
- when it entered waiting
- when to follow up next
- what action becomes possible once unblocked

## Rescheduling language

- "Move to Someday" changes bucket, not history.
- "Snooze two weeks" changes start or defer date, not due date unless the user says so.
- "Push deadline" changes due date and should be reflected explicitly.

When the user's phrasing is unclear, ask which field they want changed before editing.
