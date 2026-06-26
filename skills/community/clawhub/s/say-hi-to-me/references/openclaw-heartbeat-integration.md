# OpenClaw Heartbeat Integration

This project is designed so that companion logic and proactive delivery are separated.

## Responsibility Split

1. `say-hi-to-me` skill:
   owns role logic, greeting style, freshness rules, quiet hours, pause, cooldown, and safety boundaries
2. OpenClaw host automation:
   owns wake-up timing and actual outbound delivery

## Recommended Setup

For companionship-style proactive greetings:

1. Use OpenClaw `Heartbeat` for periodic wake-ups.
2. Keep a delivery target configured in the host app.
3. Use `scripts/sync_heartbeat_md.py` to write `HEARTBEAT.md` into the resolved workspace.
4. Let `HEARTBEAT.md` call `scripts/heartbeat_bridge.py`.
5. If the bridge returns `HEARTBEAT_OK`, exit quietly.
6. If the bridge returns a real greeting, send it and update `last_sent_at`.

For exact-time greetings such as a fixed morning message:

1. Use OpenClaw `Cron` instead of Heartbeat.

## Why This Split Exists

1. A skill does not wake itself up.
2. A skill does not guarantee outbound delivery by itself.
3. The host app is the correct place for schedules, channels, and delivery targets.

## Official References

1. Heartbeat: <https://docs.openclaw.ai/heartbeat>
2. Cron: <https://docs.openclaw.ai/cron/>
3. Message sending: <https://docs.openclaw.ai/message/>

## Repository Assets

1. Sample config: `examples/openclaw-heartbeat-config.md`
2. Sample heartbeat instructions: `examples/HEARTBEAT.md`
3. Bridge script: `scripts/heartbeat_bridge.py`

## Practical Flow

1. Heartbeat wakes the agent inside the host app.
2. `HEARTBEAT.md` tells the model to run `python3 scripts/heartbeat_bridge.py --json --mark-sent`.
3. If the script returns `HEARTBEAT_OK`, the run exits with no outbound greeting.
4. If the script returns a real `response_text`, the heartbeat sends that text to the configured target.
