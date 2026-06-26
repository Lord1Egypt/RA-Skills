---
name: gateway-resume
description: "Reliably resume work after `openclaw gateway restart` (or when you must restart the OpenClaw gateway mid-task). Uses durable one-shot cron `agentTurn` jobs (isolated session + explicit delivery) so the agent comes back after restart and replies to the same chat (Discord/Telegram/etc), usually with the same model/thinking as the requesting session. Use when: user asks for a gateway restart; you need to restart to apply config/updates; or you must ensure a post-restart follow-up message happens automatically."
---

# Gateway Resume

Gateway restarts kill the current agent process. If you need to restart mid-task, you must create a **durable wakeup** *before* restarting.

This skill uses **cron + isolated agentTurn + explicit delivery route** (not `systemEvent`) so it:

- survives restarts (cron is persisted to disk)
- replies back to the same place (Discord channel, Telegram DM/topic, etc)
- can pin the cron run to the **same model/thinking** that was active in the requesting session

## Procedure (recommended)

### 0) Tell the user you’re about to go down (own message)

Send a short message in the current chat **before** you schedule the restart:

- "Heads up — restarting the gateway for ~10–20s. I’ll be back momentarily and will resume automatically."

Keep this as its **own** message (don’t bundle it with other info).

**Common failure mode:** writing a plan but forgetting to actually schedule the cron + restart. If you don’t run Steps 3–4, the gateway won’t go down and you won’t come back.

**Do not require a user 'go' message.** Instead, schedule the restart to occur ~15s in the future (see Step 4) so this message has time to deliver before the gateway is killed.
### 1) Save resume context

Write `memory/post-restart-task.md`:

```md
# Post-restart: <brief description>
- Channel: <where to reply>
- Was doing: <what was in progress>
- Next step: <what to do next on resume>
- Status: pending
```

### 2) Resolve the return route + session model (Option B)

From the current chat/session, capture:

- `sessionKey` (e.g. `agent:main:discord:channel:<id>` or `agent:main:telegram:direct:<id>`)
- `deliveryChannel` (e.g. `discord`, `telegram`)
- `deliveryTo`:
  - Discord channel: `channel:<channelId>`
  - Discord DM: `user:<userId>`
  - Telegram DM/topic: use the chat id or `-100…:topic:<id>`
- `modelProvider` + `model` for the session (e.g. `openai-codex` + `gpt-5.2`)
- `thinkingLevel` for the session

Tip: `openclaw sessions --active 240 --json` includes these fields.

### 3) Schedule two one-shot cron jobs (back message + resume)

Use the bundled script (Option B: it infers route + model from the session store):

```bash
skills/gateway-resume/scripts/schedule-resume-cron.sh \
  --back-delay 75s \
  --delay 90s \
  --session-key "<sessionKey>"
```

The script will:
- infer the delivery route from the session key (Discord channel/DM, Telegram DM/group)
- read `openclaw sessions --json` to infer `modelProvider/model` and thinking level
- schedule **two** isolated agentTurn cron jobs with explicit delivery:
  1) a short, personable "I’m back" message (own message)
  2) a resume job that reads `memory/post-restart-task.md` and completes the next step

Notes:
- Use `--delay 90s` (or more) so the job fires well after the gateway finishes restarting.
- The cron job runs **isolated**, but delivers back to the captured route.
- The “back” job is a *separate* message to make the restart feel responsive, even if the resume step takes longer.

### 4) Restart (delayed)

Do **not** restart immediately (it can kill the process before the pre-restart message delivers). Instead schedule a restart a few seconds in the future using `systemd-run`:

```bash
skills/gateway-resume/scripts/delayed-gateway-restart.sh 15
```

This schedules a `systemctl --user restart openclaw-gateway.service` in a transient user unit.

### 5) On the cron wake

The scheduled jobs should:

1) Send a short, personable "I’m back" message (by itself).
2) Then resume:
   - read `memory/post-restart-task.md`
   - do `Next step`
   - append a handled marker (avoid needing deletes)
   - reply back to the captured destination with the result

Do **not** include raw markers like `BACK_FROM_RESTART` in user-facing text.

## Troubleshooting

- **Nothing happens after restart**: confirm the cron jobs exist *before* restarting:
  - `openclaw cron list`
- **Cron fires but no message is delivered**: route inference may be wrong for this `sessionKey` pattern.
  - Re-run the schedule script with the correct `--session-key`.
- **Model inference fails**: the session may have fallen outside the `--active` window.
  - Edit `schedule-resume-cron.sh` to use a larger `--active` range or no filter.

## Why not `systemEvent`?

`systemEvent` targets the **main** session, which may be a different model/provider and may fail (or respond in the wrong place). Isolated `agentTurn` + explicit `delivery` is deterministic.
