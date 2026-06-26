# Operations Learnings

Process bottlenecks, incident patterns, capacity insights, automation gaps, toil patterns, and SRE best practices captured during operations work.

**Categories**: process_bottleneck | incident_pattern | capacity_issue | automation_gap | sla_breach | toil_accumulation
**Areas**: incident_management | change_management | capacity_planning | automation | monitoring | runbooks | on_call
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Accepted risk (reason documented in Resolution) |
| `promoted` | Elevated to runbook, postmortem, capacity model, or SLO definition |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250415-001] incident_pattern

**Logged**: 2025-04-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/database-connection-pool-exhaustion
**Area**: incident_management

### Summary
Database connection pool exhaustion recurring monthly during batch ETL jobs
...
```

---
