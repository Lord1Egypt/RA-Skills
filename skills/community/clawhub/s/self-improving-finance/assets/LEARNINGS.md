# Finance Learnings

Reconciliation errors, control weaknesses, forecast variances, regulatory gaps, valuation errors, and cash flow anomalies captured during finance operations.

**Categories**: reconciliation_error | forecast_variance | control_weakness | regulatory_gap | valuation_error | cash_flow_anomaly
**Areas**: accounting | treasury | tax | audit | budgeting | reporting | accounts_payable | accounts_receivable
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue remediated or knowledge integrated |
| `wont_fix` | Determined immaterial or accepted risk (reason in Resolution) |
| `promoted` | Elevated to close checklist, control matrix, reconciliation procedure, or tax calendar |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250415-001] reconciliation_error

**Logged**: 2025-04-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/month-end-reconciliation-checklist
**Area**: accounting

### Summary
FX conversion using spot rate instead of average rate for P&L items causes translation variance at consolidation
...
```

---
