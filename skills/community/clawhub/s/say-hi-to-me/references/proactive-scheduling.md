# Proactive Scheduling

This skill uses `scripts/proactive_scheduler.py` to decide whether a proactive message should be sent.

Important:

1. The script is a policy engine, not a delivery engine.
2. It does not wake up by itself.
3. True proactive delivery requires the host app to invoke this logic from OpenClaw Heartbeat or Cron.

## Defaults

1. Proactive mode default: `off`
2. Freshness window: `72h`
3. Frequency cooldown:
- `low`: 24h
- `mid`: 12h
- `high`: 6h

## Gating Order

1. `proactive.enabled` must be `true`
2. `pause_until` must be expired
3. Current time must be outside `quiet_hours`
4. `last_sent_at` cooldown must pass
5. Build candidate message (stale-context-safe when needed)

All time comparisons must be timezone-aware and interpreted in local runtime timezone.

## Input State

Read from `state/session.yaml`:

- `proactive.enabled`
- `proactive.frequency`
- `proactive.quiet_hours`
- `proactive.pause_until`
- `proactive.last_sent_at`
- `context.freshness_hours`
- `last_user_input_at`
- `role.active`

## Usage

```bash
python3 scripts/proactive_scheduler.py --json
python3 scripts/proactive_scheduler.py --json --mark-sent
python3 scripts/proactive_scheduler.py --now "2026-04-03T22:30:00" --json
```

## Integration Notes

1. Use this script for local tests, dry runs, and policy verification.
2. For real outbound greetings, wire the same gating logic into OpenClaw Heartbeat or Cron.
3. Heartbeat is a better fit for companionship-style check-ins.
4. Cron is a better fit for exact-time greetings such as fixed morning or evening messages.
