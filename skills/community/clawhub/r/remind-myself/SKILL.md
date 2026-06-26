---
name: remind-myself
description: "Set a one-shot reminder delivered via Telegram at a specific time or after a duration. Use when the user asks to be reminded of something, set an alarm, or schedule a future notification. Always use this skill instead of the cron tool directly — it handles chat ID resolution and delivery."
metadata: {"openclaw":{"requires":{"bins":["openclaw"]}}}
---

# Reminder

Creates a one-shot cron job that delivers a reminder to Telegram at the specified time.

## Workflow

### 1. Parse the user's message

Extract:

| Field | Notes |
|-------|-------|
| `text` | What to remember (verbatim or paraphrased, concise) |
| `when` | When to deliver — relative or absolute |

If `when` is ambiguous, ask for clarification before proceeding.

### 2. Compute the `when` value

**Relative durations** → pass directly as `<n><unit>`:
- "in 20 minutes" → `20m`
- "in 2 hours" → `2h`
- "in 1 day" → `1d`

**Absolute times** → convert to ISO 8601 in **Europe/Paris** timezone:
```bash
TZ=Europe/Paris date -d "tomorrow 09:00" --iso-8601=seconds
# → 2026-03-03T09:00:00+01:00
```

### 3. Confirm with the user before scheduling

Show a summary and ask for confirmation:

```
Set this reminder?
- What: <text>
- When: <human-readable time>
```

Only proceed after the user confirms.

### 4. Run the reminder script

**This is the only way to create a reminder. Do not use any other method.**

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/remind.sh \"<when>\" \"<text>\""
}
```

The script handles everything: chat ID resolution, cron job creation, and verification.

### 5. Check the script output

The script prints the result. Look for:
- `OK: reminder-xxx is scheduled` → success
- `ERROR: ...` → report the exact error to the user

**Do not confirm success unless the script output says "OK".**

### 6. Confirm to the user

Only after seeing "OK" in the script output:

```
⏰ Reminder set!
📝 <text>
🕐 <human-readable time>
```

### 7. Error handling

- **Never assume failure without running the script.** Always execute it and report the actual output.
- **Never invent a diagnosis.** If something fails, show the raw error.
- **Never use sessions_spawn, sleep, or any other method.** Only use the script above.
- If the time is in the past → warn the user and ask for a new time
- If the reminder text is empty → ask what to remind them of

## Examples

| User says | `when` | `text` |
|-----------|--------|--------|
| "in 20 minutes, remind me to take out the laundry" | `20m` | `Take out the laundry` |
| "remind me to call Alice tomorrow at 14h" | `2026-03-03T14:00:00+01:00` | `Call Alice` |
| "in 2 hours: check the oven" | `2h` | `Check the oven` |
| "friday at 9am: team standup" | `2026-03-06T09:00:00+01:00` | `Team standup` |
