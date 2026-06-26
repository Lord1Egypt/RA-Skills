# Analytics Learnings

Data quality patterns, metric drift insights, pipeline reliability findings, visualization best practices, and governance lessons captured during analytics work.

**Categories**: data_quality | metric_drift | pipeline_failure | visualization_mislead | definition_mismatch | freshness_issue
**Areas**: ingestion | transformation | modeling | reporting | visualization | governance | data_catalog
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to data dictionary, metric definition, pipeline runbook, or dashboard standard |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250415-001] data_quality

**Logged**: 2025-04-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/null-rate-monitoring
**Area**: ingestion

### Summary
NULL rate spike in user_id column after source system migration requires automated monitoring
...
```

---
