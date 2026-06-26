# Support Learnings

Resolution delays, misdiagnoses, escalation gaps, SLA breaches, knowledge gaps, and customer churn signals captured during support operations.

**Categories**: resolution_delay | misdiagnosis | escalation_gap | knowledge_gap | sla_breach | customer_churn_signal
**Areas**: triage | diagnosis | resolution | follow_up | documentation | escalation
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being investigated or remediated |
| `resolved` | Issue fixed, process updated, or knowledge integrated |
| `wont_fix` | Risk accepted or deprioritised (justification required in Resolution) |
| `promoted` | Elevated to KB article, troubleshooting tree, escalation matrix, or canned response |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250415-001] misdiagnosis

**Logged**: 2025-04-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/502-gateway-diagnosis
**Area**: diagnosis

### Summary
502 Bad Gateway errors misdiagnosed as server-side when root cause is customer WAF blocking callbacks
...
```

## CRITICAL REMINDER

**NEVER log customer PII, account credentials, or internal auth tokens.**
Always use ticket IDs and anonymised references. Describe the *issue type* and *resolution*, not the *customer identity*.

---
