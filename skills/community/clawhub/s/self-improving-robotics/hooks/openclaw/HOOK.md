---
name: self-improving-robotics
description: "Injects robotics self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🤖","events":["agent:bootstrap"]}}
---

# Self-Improving Robotics Hook

Injects a reminder to evaluate robotics autonomy learnings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds a robotics-specific reminder block to check `.learnings/` for relevant entries
- Prompts the agent to log localization, planning, control, sensor fusion, hardware interface, safety, sim-to-real, and power/thermal issues
- Skips subagent sessions in the TypeScript implementation

## Reminder Content

The hook injects reminders to log to the appropriate file based on what occurred:

| Trigger | Target File | Category |
|---------|-------------|----------|
| Dynamic scene causes localization drop | `ROBOTICS_ISSUES.md` | localization incident |
| Planner fails in narrow passage | `ROBOTICS_ISSUES.md` | planning incident |
| Oscillatory control behavior observed | `ROBOTICS_ISSUES.md` | control incident |
| Sensor timestamp mismatch detected | `ROBOTICS_ISSUES.md` | sensor fusion incident |
| Driver timeout or disconnect | `ROBOTICS_ISSUES.md` | hardware interface incident |
| Safety stop triggers unexpectedly | `ROBOTICS_ISSUES.md` | safety incident |
| Sim works but real robot fails | `LEARNINGS.md` | `sim_to_real_gap` |
| Thermal throttling or brownout | `LEARNINGS.md` | `power_thermal_constraint` |
| New capability needed | `FEATURE_REQUESTS.md` | feature request |

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable self-improving-robotics
```
