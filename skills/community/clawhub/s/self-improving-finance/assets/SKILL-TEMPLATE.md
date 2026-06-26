# Finance Skill Template

Template for creating skills extracted from finance learnings. Copy and customize.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Concise description of the finance procedure, control, or reconciliation pattern this skill addresses. Include trigger conditions."
---

# Skill Name

Brief introduction: what finance problem this skill solves, what areas it applies to, and its origin.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Reconciliation/control/close trigger] | [Procedure or remediation to apply] |
| [Related trigger] | [Alternative approach] |

## Background

Why this finance knowledge matters. What misstatements or control failures it prevents.
What regulatory requirements it satisfies. What process efficiencies it provides.

## The Problem

### Incorrect Treatment

Description of the incorrect accounting treatment, reconciliation approach,
or control procedure. Use anonymized examples only.

### Why It Fails

Explanation of the root cause: misapplied standard, system misconfiguration,
process gap, or control design deficiency.

## Solution

### Correct Treatment

Description of the correct treatment, procedure, or control.
Reference applicable standards (ASC, IFRS, SOX section).

### Step-by-Step

1. Identify the issue in current procedures
2. Apply the correct treatment
3. Update close checklist or control matrix
4. Document for audit trail

## Prevention

### Control Step

Description of the control to add: approval workflow, reconciliation step,
review checkpoint, or system configuration.

### Checklist Item

Concise checklist entry for close procedures or reconciliation guides.

## Common Variations

- **Variation A**: Description and how to handle
- **Variation B**: Description and how to handle

## Applicability

| Framework | Treatment | Reference |
|-----------|-----------|-----------|
| US GAAP | [How it applies] | [ASC reference] |
| IFRS | [How it applies] | [IAS/IFRS reference] |
| Local GAAP | [How it applies] | [Local standard reference] |

## Gotchas

- Warning or common mistake when applying the procedure
- Edge case to watch for (e.g., intercompany, multi-currency, consolidation)

## Related

- Link to applicable accounting standard
- Link to internal control framework section
- Link to related skill

## Source

Extracted from finance learning entry.
- **Learning ID**: LRN-YYYYMMDD-XXX
- **Original Category**: reconciliation_error | control_weakness | forecast_variance | regulatory_gap | valuation_error | cash_flow_anomaly
- **Area**: accounting | treasury | tax | audit | budgeting | reporting | accounts_payable | accounts_receivable
- **Extraction Date**: YYYY-MM-DD
```

---

## Minimal Template

For simple finance skills that don't need all sections:

```markdown
---
name: skill-name-here
description: "What finance procedure this addresses and when to apply it."
---

# Skill Name

[Problem statement in one sentence]

## Problem

Description of the incorrect treatment or process gap (anonymized).

## Solution

Description of the correct treatment, with standard reference.

## Prevention

[Close checklist item or control step to prevent recurrence]

## Source

- Learning ID: LRN-YYYYMMDD-XXX
```

---

## Naming Conventions

- **Skill name**: lowercase, hyphens for spaces
  - Good: `fx-translation-rates`, `je-approval-workflow`, `month-end-reconciliation`
  - Bad: `FXTranslation`, `je_approval`, `fix1`

- **Description**: Start with action verb, mention the finance issue or procedure
  - Good: "Prevents FX translation errors by enforcing average rate for P&L items during consolidation."
  - Bad: "Accounting stuff"

- **Files**:
  - `SKILL.md` — Required, main documentation
  - `scripts/` — Optional, executable helpers (reconciliation checks, variance alerts)
  - `references/` — Optional, detailed docs
  - `assets/` — Optional, templates

---

## Extraction Checklist

Before creating a skill from a finance learning:

- [ ] Issue is verified (status: resolved, remediation confirmed)
- [ ] Procedure is broadly applicable (not a one-off entity adjustment)
- [ ] Examples are anonymized (no real account numbers, amounts, or entity names)
- [ ] Applicable standards are referenced (ASC, IFRS, SOX)
- [ ] Prevention method is documented (control step, checklist item, system config)
- [ ] Name follows conventions
- [ ] Description is concise but informative

After creating:

- [ ] Update original learning with `promoted_to_skill` status
- [ ] Add `Skill-Path: skills/skill-name` to learning metadata
- [ ] Test skill by reading it in a fresh session
- [ ] Verify procedures are complete and self-contained
