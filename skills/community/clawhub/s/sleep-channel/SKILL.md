---
name: sleep-channel
version: 1.1.0
description: Handle messages in a Discord sleep-tracking channel by grounding all sleep logging and summaries on the real sleep tracker and source Discord metadata. Use when working in a dedicated sleep channel, especially for adding sleep entries, correcting the latest entry, deleting the latest entry, or rendering the current sleep log without hallucinating timestamps, dates, or entries.
env:
  SLEEP_TIMEZONE:
    required: true
    description: "IANA timezone string (e.g. America/Los_Angeles, Europe/Berlin)"
  WORKSPACE:
    required: false
    description: "Workspace root path. Defaults to ~/.openclaw/workspace"
---

# Sleep Channel

Deterministic sleep tracker for Discord channel-based sleep logging.

## Configuration

Set the following environment variables before use:

| Variable | Required | Description |
|----------|----------|-------------|
| `SLEEP_TIMEZONE` | Yes | IANA timezone string (e.g. `America/Los_Angeles`, `Europe/Berlin`) |
| `WORKSPACE` | No | Workspace root path. Defaults to `$HOME/.openclaw/workspace` |

## Core Rules

- Treat the configured channel as the dedicated sleep channel.
- Prefer `scripts/tracker.py` for all log mutations and rendering.
- Never write `now` as a logged time.
- Never derive event time from the model turn time.
- Use the source Discord message timestamp unless the user explicitly gives a different time.
- Convert displayed times to the user's local timezone (`SLEEP_TIMEZONE`).
- Never invent entries, dates, or file contents.
- If showing the sleep log, render from the real tracker/file output.

## Commands

### Add a new sleep event

For messages like: going to bed, still awake, fell asleep, awake now, resting, nap, back to sleep.

```bash
python3 scripts/tracker.py add \
  "$MESSAGE_TEXT" \
  "$CHANNEL_ID" \
  "$MESSAGE_ID" \
  "$AUTHOR_ID" \
  "$TIMESTAMP_UTC"
```

### Correct the latest entry

When the user is clearly correcting the previous sleep event.

```bash
python3 scripts/tracker.py correct-latest \
  "$MESSAGE_TEXT" \
  "$CHANNEL_ID" \
  "$MESSAGE_ID" \
  "$AUTHOR_ID" \
  "$TIMESTAMP_UTC"
```

### Delete the latest entry

When the user explicitly wants the latest sleep entry removed.

```bash
python3 scripts/tracker.py delete-latest
```

### Render the sleep log

Display the current sleep log/summary.

```bash
python3 scripts/tracker.py render
```

## Classification Hints

The tracker handles common phrases: `fell asleep`, `awake now`, `got up`, `still awake`, `laying in bed`, `going to bed`, `trying to sleep`, `going back to sleep`. Pass raw text to the tracker instead of re-parsing.

## If Uncertain

Ask a short clarifying question only when intent is ambiguous:
- Correction vs new event?
- Delete the latest entry?
- Explicit time override?

## Files

| File | Purpose |
|------|---------|
| `scripts/tracker.py` | Canonical sleep tracker (self-contained, stdlib only) |
| `references/CHANNEL_RULES.md` | Channel setup guide (optional) |
| `references/README.md` | System documentation (optional) |
