---
name: self-improving-marketing
description: "Injects marketing self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"📊","events":["agent:bootstrap"]}}
---

# Self-Improving Marketing Hook

Injects a reminder to evaluate marketing learnings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds a marketing-specific reminder block to check `.learnings/` for relevant entries
- Prompts the agent to log campaign issues, messaging problems, attribution gaps, brand inconsistencies, audience drift, and content decay

## Reminder Content

The hook injects reminders to log to the appropriate file based on what occurred:

| Trigger | Target File | Category |
|---------|-------------|----------|
| CTR or conversion drop detected | `CAMPAIGN_ISSUES.md` | performance trigger |
| Email deliverability problem | `CAMPAIGN_ISSUES.md` | deliverability trigger |
| Messaging missed target segment | `LEARNINGS.md` | `messaging_miss` |
| Channel underperforming benchmarks | `LEARNINGS.md` | `channel_underperformance` |
| Audience behavior shifted | `LEARNINGS.md` | `audience_drift` |
| Brand guideline violation found | `LEARNINGS.md` | `brand_inconsistency` |
| UTM or attribution broken | `LEARNINGS.md` | `attribution_gap` |
| Content performance declining | `LEARNINGS.md` | `content_decay` |

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable self-improving-marketing
```
