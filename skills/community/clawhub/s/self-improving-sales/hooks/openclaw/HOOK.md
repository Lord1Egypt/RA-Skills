---
name: self-improving-sales
description: "Injects sales self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"💼","events":["agent:bootstrap"]}}
---

# Self-Improving Sales Hook

Injects a reminder to evaluate sales learnings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds a sales-specific reminder block to check `.learnings/` for relevant entries
- Prompts the agent to log deal issues, objection patterns, pricing errors, forecast misses, competitor shifts, and deal velocity drops

## Reminder Content

The hook injects reminders to log to the appropriate file based on what occurred:

| Trigger | Target File | Category |
|---------|-------------|----------|
| Deal stuck in stage >30 days | `DEAL_ISSUES.md` | pipeline_leak |
| Objection you couldn't handle | `LEARNINGS.md` | `objection_pattern` |
| Pricing mistake discovered | `DEAL_ISSUES.md` | pricing_error |
| Forecast missed by >20% | `DEAL_ISSUES.md` | forecast_miss |
| Lost deal to competitor | `LEARNINGS.md` | `competitor_shift` |
| Deal velocity slowing | `LEARNINGS.md` | `deal_velocity_drop` |
| Sales tool or capability needed | `FEATURE_REQUESTS.md` | feature_request |

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable self-improving-sales
```
