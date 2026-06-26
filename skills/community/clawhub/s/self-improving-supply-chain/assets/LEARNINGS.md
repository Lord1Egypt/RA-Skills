# Supply Chain Learnings

Forecast errors, supplier risks, logistics delays, inventory mismatches, quality deviations, and demand signal shifts captured during supply chain operations.

**Categories**: forecast_error | supplier_risk | logistics_delay | inventory_mismatch | quality_deviation | demand_signal_shift
**Areas**: procurement | inventory | logistics | manufacturing | quality | demand_planning | warehousing
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being investigated or mitigated |
| `resolved` | Issue resolved, corrective action taken |
| `wont_fix` | Accepted risk or not actionable (reason in Resolution) |
| `promoted` | Elevated to supplier scorecard, safety stock policy, routing playbook, or demand model |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250415-001] forecast_error

**Logged**: 2025-04-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/seasonal-demand-model
**Area**: demand_planning

### Summary
Q4 seasonal demand spike not captured in baseline forecast model, caused 30% understock
...
```

---
