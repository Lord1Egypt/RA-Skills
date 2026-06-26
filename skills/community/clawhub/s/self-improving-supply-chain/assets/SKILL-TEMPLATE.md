# Supply Chain Skill Template

Template for creating skills extracted from supply chain learnings. Copy and customize.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Concise description of the supply chain pattern, risk mitigation, or operational improvement this skill addresses. Include trigger conditions."
---

# Skill Name

Brief introduction: what supply chain problem this skill solves, what operational areas it applies to, and its origin.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Supply chain trigger] | [Mitigation or process to apply] |
| [Related trigger] | [Alternative approach] |

## Background

Why this supply chain knowledge matters. What disruptions it prevents. What cost savings or service level improvements it provides.

## The Problem

### Scenario

Describe the supply chain situation: demand pattern, supplier behavior, logistics constraint, or inventory condition that leads to the issue.

### Impact

Quantify the impact: stockout duration, excess inventory cost, delayed shipments, customer order fill rate drop, production line downtime.

## Solution

### Corrective Action

Step-by-step process to resolve the immediate issue.

### Preventive Measures

1. Policy change to prevent recurrence
2. Monitoring threshold to detect early
3. Escalation path if threshold breached
4. Backup plan or contingency

## Key Metrics

| Metric | Target | Threshold |
|--------|--------|-----------|
| [Relevant KPI] | [Target value] | [Alert threshold] |

## Common Variations

- **Variation A**: Description and how to handle
- **Variation B**: Description and how to handle

## Areas Affected

| Area | Impact | Mitigation |
|------|--------|------------|
| Procurement | [How it affects sourcing] | [Sourcing mitigation] |
| Inventory | [How it affects stock levels] | [Stock mitigation] |
| Logistics | [How it affects transport] | [Routing mitigation] |

## Gotchas

- Warning or common mistake when applying the solution
- Edge case to watch for (seasonality, regional variation, supplier-specific)

## Related

- Link to related supplier scorecard
- Link to safety stock policy
- Link to demand planning model
- Link to related skill

## Source

Extracted from supply chain learning entry.
- **Learning ID**: LRN-YYYYMMDD-XXX or SCM-YYYYMMDD-XXX
- **Original Category**: forecast_error | supplier_risk | logistics_delay | inventory_mismatch | quality_deviation | demand_signal_shift
- **Area**: procurement | inventory | logistics | manufacturing | quality | demand_planning | warehousing
- **Extraction Date**: YYYY-MM-DD
```

---

## Minimal Template

For simple supply chain skills that don't need all sections:

```markdown
---
name: skill-name-here
description: "What supply chain pattern this addresses and when to apply it."
---

# Skill Name

[Problem statement in one sentence]

## Problem

Describe the supply chain disruption or inefficiency.

## Solution

Step-by-step mitigation and prevention.

## Key Metrics

| Metric | Target |
|--------|--------|
| [KPI] | [Value] |

## Source

- Learning ID: LRN-YYYYMMDD-XXX
```

---

## Naming Conventions

- **Skill name**: lowercase, hyphens for spaces
  - Good: `supplier-diversification`, `safety-stock-optimization`, `ocean-freight-contingency`
  - Bad: `SupplierDiv`, `safety_stock`, `fix1`

- **Description**: Start with action verb, mention the operational area
  - Good: "Prevents single-source supplier risk by maintaining qualified backup suppliers. Use when a critical component has fewer than two approved sources."
  - Bad: "Supplier stuff"

- **Files**:
  - `SKILL.md` — Required, main documentation
  - `scripts/` — Optional, executable tools (forecasting helper, stock calculator)
  - `references/` — Optional, detailed docs
  - `assets/` — Optional, templates

---

## Extraction Checklist

Before creating a skill from a supply chain learning:

- [ ] Issue is verified (status: resolved, corrective action taken)
- [ ] Solution is broadly applicable (not one-off anomaly)
- [ ] Impact is quantified (cost, service level, lead time)
- [ ] Area(s) affected are specified
- [ ] Preventive measures are documented (policy, threshold, escalation)
- [ ] Name follows conventions
- [ ] Description is concise but informative

After creating:

- [ ] Update original learning with `promoted_to_skill` status
- [ ] Add `Skill-Path: skills/skill-name` to learning metadata
- [ ] Test skill by reading it in a fresh session
- [ ] Verify metrics and thresholds are realistic
