# Capture and Clarify — Task List

## Capture defaults

- Accept raw language: "remind me," "I need to," "waiting on," "someday," "not this week."
- If the user gives several items at once, split them into separate task records.
- Keep ambiguous items in `Inbox` unless the bucket is obvious from wording.

## Infer silently when confidence is high

Infer without asking when the meaning is obvious:
- explicit dates
- obvious waiting language
- obvious recurring language
- direct project names already in use
- clear "someday" or "not now" phrasing

## Ask only when ambiguity changes action

Ask one short follow-up when:
- the date phrase could mean due or defer
- the user named an outcome that should become a project
- the item might be waiting on someone else
- deletion, done, or recurrence could change history

Do not ask for tags, colors, labels, or metadata that does not change execution.

## Title hygiene

- Start with a verb whenever possible.
- Remove filler words but keep meaning.
- Preserve sensitive wording in notes when shortening the title would hide nuance.

## Good conversions

- "Need to send Marta the draft by Friday" -> `Send draft to Marta` with due date Friday
- "Waiting on legal before I can ship contract" -> waiting item plus next chase date if known
- "Someday maybe redesign landing page" -> Someday bucket, not Today
- "Every first workday review cash runway" -> recurring rule with explicit regeneration behavior
