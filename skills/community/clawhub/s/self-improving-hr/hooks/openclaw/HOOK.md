---
name: self-improving-hr
description: "Injects HR self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"👥","events":["agent:bootstrap"]}}
---

# Self-Improving HR Hook

Injects a reminder to evaluate HR learnings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds an HR-specific reminder block to check `.learnings/` for relevant entries
- Prompts the agent to log policy gaps, compliance risks, onboarding friction, candidate experience issues, retention signals, and process inefficiencies
- Emphasizes PII anonymization in all logged entries

## Reminder Content

The hook injects reminders to log to the appropriate file based on what occurred:

| Trigger | Target File | Category |
|---------|-------------|----------|
| Compliance audit finding | `HR_PROCESS_ISSUES.md` | compliance_risk |
| Candidate drops off pipeline | `LEARNINGS.md` | `candidate_experience` |
| New hire leaves within 90 days | `LEARNINGS.md` | `retention_signal` |
| Policy gap discovered | `LEARNINGS.md` | `policy_gap` |
| Exit interview recurring theme | `LEARNINGS.md` | `retention_signal` |
| Benefits enrollment error | `HR_PROCESS_ISSUES.md` | process_inefficiency |
| I-9 verification issue | `HR_PROCESS_ISSUES.md` | compliance_risk |
| Onboarding step causing delays | `LEARNINGS.md` | `onboarding_friction` |

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable self-improving-hr
```
