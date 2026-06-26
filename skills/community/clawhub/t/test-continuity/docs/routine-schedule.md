# Routine Schedule (V2)

This document describes the structured `routine_schedule` settings included in the V2 feature set.

It is part of the V2 public package and remains optional.

## Purpose

`routine_schedule` provides a stable, structured source for:

- `sleep`
- `wake_window`
- `active_day`

It exists so proactive follow-up behavior does not rely only on inferred memory or log clues.

## Settings

```json
"routine_schedule": {
  "enabled": false,
  "timezone": "UTC",
  "sleep_time": "05:30",
  "wake_time": "15:00",
  "wake_window_minutes": 90,
  "phases": {
    "sleep": {
      "proactive_enabled": false,
      "wake_seed_enabled": false
    },
    "wake_window": {
      "proactive_enabled": true,
      "wake_seed_enabled": true,
      "interval_hours": 0.5
    },
    "active_day": {
      "proactive_enabled": true,
      "wake_seed_enabled": false,
      "interval_hours": 3
    }
  }
}
```

## Phase precedence

Phase resolution follows this order:

1. structured `routine_schedule`
2. explicit current user state override, such as an early wake or early sleep request
3. memory/log/hook-derived wake fallback

Structured settings win over memory-derived guesses.

## Wake seed vs proactive chat

- `wake seed` is a wake-window-specific follow-up source
- it is intended for waking-up continuity, especially when a pending thread was explicitly left for after sleep
- normal `proactive_chat` is still separate and uses the recent conversation window
- wake seed uses structured `wake_time` / `wake_window_minutes` first, then falls back to memory-derived wake clues only when structured settings are unavailable

## What this does not claim

- it does not make V2 fully shipped
- it does not replace the rest of the continuity core
- it does not imply one specific delivery platform behavior
- it does not claim that rollout tuning is finished

## Operator note

If you are packaging this for a host/operator rather than a single live
instance, also read:

- `docs/host-operator-settings.md`

That document explains:

- how long staged/tracked records usually live
- which timing knobs are public settings
- how to use quiet-hours
- how to think about work-time vs rest-time behavior
