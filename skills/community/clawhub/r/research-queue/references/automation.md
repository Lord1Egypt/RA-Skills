# Automation

Prefer **OpenClaw cron** for autonomous research runs.

Do **not** use system `crontab`, shell sleep loops, launchd timers, or ad-hoc heartbeat polling when the goal is scheduled queue processing.

## Recommended mode

Use an **isolated OpenClaw cron job** that runs an agent turn.

Why:
- keeps research work out of the main session
- avoids polluting the active conversation
- gives bounded, repeatable runs
- uses OpenClaw-native scheduling instead of OS-level timers

## Cron requirements

- Explicitly create the schedule with the **OpenClaw `cron` tool**.
- If a model/user seems to confuse `cron` with Unix `crontab`, restate that this means **OpenClaw cron jobs**, not host `crontab`.
- Default to cron, not HEARTBEAT.
- Use HEARTBEAT only when the user specifically wants drift-tolerant, batched background attention in the main session.

## Minimal cron run prompt

Use a short prompt and rely on the skill + `QUESTIONS.md` structure:

```text
Run one bounded research-queue pass. Read `skills/research-queue/SKILL.md` and `QUESTIONS.md`. If the queue is missing, initialize it per the skill. Select at most one `open` question, investigate with allowed tools only, update the question in place, and write durable findings to `memory/YYYY-MM-DD.md` when warranted. Prefer OpenClaw-native tools and keep the run bounded.
```

## Session target

Prefer:
- `sessionTarget: "isolated"`
- `payload.kind: "agentTurn"`

This keeps autonomous research separate from the live chat session.

## Example schedule choices

- Every 4 hours during active experimentation
- Daily in the morning for slow-burn research
- Manually triggered cron for on-demand queue processing
