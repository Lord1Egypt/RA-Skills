# Sleep Channel Rules

Channel: your dedicated sleep channel (configured in your agent setup)

Purpose: maintain an accurate sleep log and formatted summary without hallucinated entries or wrong times.

## Non-Negotiable Rules

1. Never write `now` as the time in a sleep entry.
2. Never invent a time from the current model turn time.
3. Source of truth for a sleep event time is the source Discord message timestamp unless the user explicitly gives a different time in the message.
4. Convert displayed timestamps to the configured timezone (`SLEEP_TIMEZONE`).
5. Never fabricate future dates or extra entries that are not in the log.
6. When correcting the latest entry, supersede or update the last real entry instead of adding fake history.
7. If asked to show the log, render from the actual log file instead of reconstructing from memory.
8. If unsure whether a message is a new event or a correction to the previous event, ask a short clarifying question.

## Time Handling

Use this order of precedence:
1. Explicit time stated by the user in the message, if unambiguous.
2. Otherwise, the source Discord message timestamp.
3. Never fall back to `now`.

Rules:
- Display in the configured timezone (`SLEEP_TIMEZONE`).
- Keep UTC in storage if the tracker stores UTC.
- Do not drift dates across midnight by using UTC for user-facing output.

## Logging Behavior

Allowed event types include:
- going to bed / getting in bed / heading to bed
- still awake / awake again / laying in bed
- fell asleep
- awake now / got up / up now
- correction of latest entry
- delete latest entry if explicitly requested

Do not:
- make up missing events
- add a second entry when the user asked to correct the latest one
- render entries that are not in the file
- claim the file says something you did not read

## Rendering Rules

When asked for the formatted log:
- read or render from the actual sleep log file / tracker output
- do not rebuild from conversational memory
- preserve only real active entries
- do not include superseded or deleted entries unless explicitly asked

## Response Style

Good:
- `Logged: 🌙🛏️ 2:50am — going to sleep now`
- `Corrected latest entry to: 😴💤 2:23am — falling asleep`
- `Here’s the current sleep log from file:`

Bad:
- `😴💤 now — falling asleep`
- adding `3/25/2026` when the log only contains `3/24/2026`
- saying the file contains an entry that was never read from disk

## Safety Rails For Weak Models

Before replying, check:
- Did I derive the time from the source message timestamp or explicit user time?
- Did I convert to the user's configured timezone?
- Did I avoid `now`?
- If showing the log, did I render from the actual file?
- Did I avoid invented entries and invented dates?

If any answer is no, stop and fix it first.
