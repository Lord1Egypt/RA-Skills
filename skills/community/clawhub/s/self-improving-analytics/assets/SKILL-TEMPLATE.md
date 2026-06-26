# Analytics Skill Template

Template for creating skills extracted from analytics learnings. Copy and customize.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Concise description of the analytics pattern, data quality check, or pipeline reliability technique this skill addresses. Include trigger conditions."
---

# Skill Name

Brief introduction: what analytics problem this skill solves, what data stack components it applies to, and its origin.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Data quality trigger] | [Check or remediation to apply] |
| [Pipeline failure trigger] | [Recovery or prevention approach] |

## Background

Why this analytics knowledge matters. What data quality issues it prevents. What reporting accuracy or pipeline reliability improvements it provides.

## The Problem

### Problematic Pattern

\`\`\`sql
-- Query or config that demonstrates the issue
\`\`\`

### Why It Fails

Explanation of the root cause: data model assumption, timing issue, implicit type coercion, missing validation, etc.

## Solution

### Corrected Approach

\`\`\`sql
-- Fixed query, config, or pipeline step
\`\`\`

### Step-by-Step

1. Identify the pattern in existing pipelines or dashboards
2. Apply the fix
3. Add data quality test to prevent regression
4. Update data dictionary if definitions changed

## Prevention

### Data Quality Test

\`\`\`yaml
# dbt test or Great Expectations check
tests:
  - not_null:
      column_name: key_column
  - accepted_values:
      column_name: status
      values: ['active', 'inactive', 'pending']
\`\`\`

### Pipeline Alert

\`\`\`yaml
# Airflow or Dagster alert configuration
alert:
  condition: "null_rate > 0.05"
  severity: critical
  channel: "#data-quality"
\`\`\`

## Common Variations

- **Variation A**: Description and how to handle
- **Variation B**: Description and how to handle

## Data Stack Components Affected

| Component | Manifestation | Fix |
|-----------|---------------|-----|
| Snowflake | [How it appears] | [Stack-specific fix] |
| BigQuery | [How it appears] | [Stack-specific fix] |
| Redshift | [How it appears] | [Stack-specific fix] |

## Gotchas

- Warning or common mistake when applying the fix
- Edge case to watch for (timezone, DST, fiscal calendar)

## Related

- Link to related data quality documentation
- Link to warehouse-specific behavior documentation
- Link to related skill

## Source

Extracted from analytics learning entry.
- **Learning ID**: LRN-YYYYMMDD-XXX
- **Original Category**: data_quality | metric_drift | pipeline_failure | visualization_mislead | definition_mismatch | freshness_issue
- **Area**: ingestion | transformation | modeling | reporting | visualization | governance | data_catalog
- **Extraction Date**: YYYY-MM-DD
```

---

## Minimal Template

For simple analytics skills that don't need all sections:

```markdown
---
name: skill-name-here
description: "What analytics pattern this addresses and when to apply it."
---

# Skill Name

[Problem statement in one sentence]

## Problem

\`\`\`sql
-- problematic query or pipeline config
\`\`\`

## Solution

\`\`\`sql
-- corrected query or pipeline config
\`\`\`

## Prevention

[Data quality test, pipeline alert, or governance rule to prevent recurrence]

## Source

- Learning ID: LRN-YYYYMMDD-XXX
```

---

## Naming Conventions

- **Skill name**: lowercase, hyphens for spaces
  - Good: `null-rate-monitoring`, `metric-definition-governance`, `dashboard-axis-standards`
  - Bad: `NullRateMonitoring`, `metric_def`, `fix1`

- **Description**: Start with action verb, mention the data issue or pattern
  - Good: "Detects NULL rate spikes in key columns after source system changes. Use when ingestion pipelines process data from systems undergoing migration."
  - Bad: "Data stuff"

- **Files**:
  - `SKILL.md` — Required, main documentation
  - `scripts/` — Optional, executable checks (dbt test wrapper, freshness checker)
  - `references/` — Optional, detailed docs
  - `assets/` — Optional, templates

---

## Extraction Checklist

Before creating a skill from an analytics learning:

- [ ] Data issue is verified (status: resolved, root cause confirmed)
- [ ] Solution is broadly applicable (not one-off data fix)
- [ ] SQL or config examples are minimal and self-contained
- [ ] Data stack components affected are specified
- [ ] Prevention method is documented (data quality test, pipeline alert, governance rule)
- [ ] Name follows conventions
- [ ] Description is concise but informative

After creating:

- [ ] Update original learning with `promoted_to_skill` status
- [ ] Add `Skill-Path: skills/skill-name` to learning metadata
- [ ] Test skill by reading it in a fresh session
- [ ] Verify SQL examples run correctly against the target warehouse
