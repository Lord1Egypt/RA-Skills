---
name: self-improving-support
description: "Injects support self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🎧","events":["agent:bootstrap"]}}
---

# Self-Improving Support Hook

Injects a reminder to evaluate support learnings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds a support-specific reminder block to check `.learnings/` for relevant entries
- Prompts the agent to log resolution delays, misdiagnoses, SLA breaches, escalation gaps, knowledge gaps, and customer churn signals

## Reminder Content

The hook injects reminders to log to the appropriate file based on what occurred:

| Trigger | Target File | Category |
|---------|-------------|----------|
| Repeat ticket detected | `TICKET_ISSUES.md` | repeat_ticket trigger |
| SLA breach occurred | `TICKET_ISSUES.md` | sla_breach trigger |
| Misdiagnosis identified | `TICKET_ISSUES.md` | misdiagnosis |
| Ticket reopened by customer | `TICKET_ISSUES.md` | ticket_reopen trigger |
| Knowledge base gap found | `LEARNINGS.md` | `knowledge_gap` |
| Escalation path unclear | `LEARNINGS.md` | `escalation_gap` |
| Customer churn signal | `LEARNINGS.md` | `customer_churn_signal` |
| Resolution delayed | `LEARNINGS.md` | `resolution_delay` |

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable self-improving-support
```
