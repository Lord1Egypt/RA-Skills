---
name: self-improving-operations
description: "Injects operations self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"⚙️","events":["agent:bootstrap"]}}
---

# Operations Self-Improvement Hook

Injects a reminder to evaluate operational learnings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds an operations-specific reminder block to check `.learnings/` for relevant entries
- Prompts the agent to log incidents, process bottlenecks, automation gaps, capacity issues, SLA breaches, and toil patterns

## Reminder Content

The hook injects reminders to log to the appropriate file based on what occurred:

| Trigger | Target File | Category |
|---------|-------------|----------|
| Incident repeats within 30 days | `OPERATIONS_ISSUES.md` | `incident_pattern` |
| MTTR exceeds target threshold | `OPERATIONS_ISSUES.md` | severity-based |
| SLA/SLO breach detected | `OPERATIONS_ISSUES.md` | `sla_breach` |
| Capacity threshold exceeded | `OPERATIONS_ISSUES.md` | `capacity_issue` |
| Manual step in automated pipeline | `LEARNINGS.md` | `automation_gap` |
| Alert fatigue detected | `LEARNINGS.md` | `monitoring` area |
| Change failure rate spikes | `LEARNINGS.md` | `change_management` area |
| Toil exceeds 50% of on-call | `LEARNINGS.md` | `toil_accumulation` |

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable self-improving-operations
```
