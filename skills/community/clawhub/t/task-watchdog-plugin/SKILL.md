# Task Watchdog

OpenClaw plugin that auto-notifies on subagent failures, exec errors, and stale tasks.

## Hooks

- **subagent_ended**: Detects abnormal outcomes (error/timeout/killed/reset/deleted) and notifies parent session
- **after_tool_call (exec)**: Watches for abnormal exec exits (non-zero, OOM, signals)
- **heartbeat_prompt_contribution**: Injects stale-task patrol instructions into heartbeat cycles
- **gateway_start**: Timer-based patrol that periodically triggers heartbeat checks

## Install

```bash
openclaw plugin install openclaw-task-watchdog
```

## Config

All optional — works with defaults:

```json
{
  "task-watchdog": {
    "subagentNotifyOn": ["error", "timeout", "killed"],
    "execNotifyOnAbnormal": true,
    "timerPatrol": true,
    "timerPatrolIntervalMs": 120000,
    "staleThresholdMs": 1800000
  }
}
```
