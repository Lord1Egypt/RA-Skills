# Operations Skill Template

Template for creating skills extracted from operations learnings. Copy and customize.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Concise description of the operational pattern, incident response procedure, or automation this skill addresses. Include trigger conditions."
---

# Skill Name

Brief introduction: what operational problem this skill solves, what systems it applies to, and its origin.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Incident/operational trigger] | [Response procedure or automation] |
| [Related trigger] | [Alternative approach] |

## Background

Why this operational knowledge matters. What incidents it prevents. What reliability or efficiency improvements it provides.

## The Problem

### Symptoms

- Observable indicators (alerts, metrics, user reports)
- How the problem manifests in production

### Impact

- Blast radius (users affected, revenue impact, SLA consumption)
- Duration and MTTR of past occurrences

## Solution

### Immediate Response

1. Triage and assess blast radius
2. Mitigate user impact
3. Communicate to stakeholders
4. Apply known fix or workaround

### Permanent Fix

1. Root cause analysis
2. Systemic remediation
3. Automation to prevent recurrence
4. Monitoring to detect recurrence early

### Runbook Steps

\`\`\`bash
# Step-by-step commands for incident response
# Include verification commands after each step
\`\`\`

## Prevention

### Monitoring

- Alert conditions to detect early
- Dashboard queries for proactive monitoring
- SLI/SLO thresholds

### Automation

- Automated remediation scripts
- Capacity auto-scaling rules
- Circuit breakers and failsafes

## Common Variations

- **Variation A**: Description and how to handle
- **Variation B**: Description and how to handle

## Systems Affected

| System | Manifestation | Response |
|--------|---------------|----------|
| Database | [How it appears] | [System-specific response] |
| Load Balancer | [How it appears] | [System-specific response] |
| Message Queue | [How it appears] | [System-specific response] |

## Gotchas

- Warning or common mistake during incident response
- Edge case to watch for during remediation

## Related

- Link to related runbook
- Link to incident postmortem
- Link to related SLO definition

## Source

Extracted from operations learning entry.
- **Learning ID**: LRN-YYYYMMDD-XXX or OPS-YYYYMMDD-XXX
- **Original Category**: incident_pattern | process_bottleneck | capacity_issue | automation_gap
- **Area**: incident_management | change_management | capacity_planning | automation | monitoring
- **Extraction Date**: YYYY-MM-DD
```

---

## Minimal Template

For simple operational skills that don't need all sections:

```markdown
---
name: skill-name-here
description: "What operational pattern this addresses and when to apply it."
---

# Skill Name

[Problem statement in one sentence]

## Symptoms

- [Observable indicator 1]
- [Observable indicator 2]

## Response

1. [Step 1]
2. [Step 2]
3. [Verification]

## Prevention

[Monitoring, automation, or process change to prevent recurrence]

## Source

- Learning ID: LRN-YYYYMMDD-XXX
```

---

## Naming Conventions

- **Skill name**: lowercase, hyphens for spaces
  - Good: `database-connection-pool-exhaustion`, `certificate-renewal-automation`, `deployment-rollback-procedure`
  - Bad: `DBConnPoolExhaust`, `cert_renewal`, `fix1`

- **Description**: Start with action verb, mention the operational pattern
  - Good: "Diagnoses and resolves database connection pool exhaustion during batch jobs. Use when connection timeouts spike during ETL windows."
  - Bad: "Database stuff"

- **Files**:
  - `SKILL.md` — Required, main documentation
  - `scripts/` — Optional, runbook automation scripts
  - `references/` — Optional, detailed docs and postmortems
  - `assets/` — Optional, templates and dashboards

---

## Extraction Checklist

Before creating a skill from an operations learning:

- [ ] Incident/issue is verified (status: resolved, root cause confirmed)
- [ ] Solution is broadly applicable (not a one-off infrastructure quirk)
- [ ] Runbook steps are tested and include verification commands
- [ ] Systems affected are specified
- [ ] Monitoring/prevention is documented (alerts, SLOs, automation)
- [ ] Name follows conventions
- [ ] Description is concise but informative

After creating:

- [ ] Update original learning with `promoted_to_skill` status
- [ ] Add `Skill-Path: skills/skill-name` to learning metadata
- [ ] Test runbook steps in staging environment
- [ ] Verify monitoring queries return expected results
