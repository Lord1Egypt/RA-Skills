# HR Learnings

Policy gaps, compliance risks, recruiting insights, onboarding friction, retention signals, and offboarding gaps captured during HR operations.

**Categories**: policy_gap | compliance_risk | process_inefficiency | candidate_experience | retention_signal | onboarding_friction
**Areas**: recruiting | onboarding | compensation | compliance | performance | offboarding | dei
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to policy document, onboarding checklist, compliance calendar, or interview scorecard |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250415-001] policy_gap

**Logged**: 2025-04-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/remote-work-policy-international
**Area**: compliance

### Summary
Remote work policy does not cover international contractors in non-US jurisdictions
...
```

**CRITICAL**: NEVER log PII (names, SSNs, salary details, medical info, performance ratings for specific individuals). Always anonymize.

---
