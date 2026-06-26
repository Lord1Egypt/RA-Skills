# HR Skill Template

Template for creating HR skills extracted from learnings, process issues, and compliance findings. Copy and customize.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Concise description of the HR skill and when to use it. Include trigger conditions."
---

# Skill Name

Brief introduction explaining the HR problem this skill addresses and its origin.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [HR trigger 1] | [Remediation 1] |
| [HR trigger 2] | [Remediation 2] |

## Background

Why this HR knowledge matters. What compliance risks or process failures it prevents. Context from the original finding.

## Remediation

### Step-by-Step

1. First remediation step with process or policy change
2. Second step
3. Verification step (audit check, HRIS validation, or manager confirmation)

### Policy/Process Example

\`\`\`markdown
# Example showing the correct policy language or process documentation
\`\`\`

## Common Variations

- **Variation A**: Different jurisdiction or employment type specifics
- **Variation B**: Alternative remediation approach

## Gotchas

- Warning or common mistake during remediation #1
- Warning or common mistake during remediation #2
- **NEVER** log PII — always anonymize before documenting

## Related Standards

- Regulation: FMLA | ADA | EEOC | FLSA | COBRA | HIPAA | WARN
- Jurisdiction: Federal | State | Local | International
- Internal Policy: handbook section reference

## Source

Extracted from HR learning or process issue entry.
- **Entry ID**: LRN-YYYYMMDD-XXX or HRP-YYYYMMDD-XXX
- **Original Category**: policy_gap | compliance_risk | process_inefficiency | candidate_experience | retention_signal | onboarding_friction
- **Extraction Date**: YYYY-MM-DD
```

---

## Minimal Template

For simple HR skills:

```markdown
---
name: skill-name-here
description: "What this HR skill does and when to use it."
---

# Skill Name

[HR problem statement in one sentence]

## Remediation

[Direct fix with policy update or process change]

## Source

- Entry ID: LRN-YYYYMMDD-XXX or HRP-YYYYMMDD-XXX
```

---

## Template with Scripts

For HR skills that include compliance checkers or automation scripts:

```markdown
---
name: skill-name-here
description: "What this HR skill does and when to use it."
---

# Skill Name

[Introduction]

## Quick Reference

| Command | Purpose |
|---------|---------|
| `./scripts/check-compliance.sh` | [What it checks] |
| `./scripts/generate-report.sh` | [What it generates] |

## Usage

### Automated (Recommended)

\`\`\`bash
./skills/skill-name/scripts/check-compliance.sh [target]
\`\`\`

### Manual Steps

1. Step one
2. Step two

## Scripts

| Script | Description |
|--------|-------------|
| `scripts/check-compliance.sh` | Compliance deadline and requirement checker |
| `scripts/generate-report.sh` | Report generator for audit preparation |

## Source

- Entry ID: HRP-YYYYMMDD-XXX
```

---

## Naming Conventions

- **Skill name**: lowercase, hyphens for spaces
  - Good: `i9-reverification-tracker`, `onboarding-it-checklist`, `exit-interview-playbook`
  - Bad: `I9_ReVerification`, `OnboardingITChecklist`

- **Description**: Start with action verb, mention HR trigger
  - Good: "Tracks I-9 re-verification deadlines for visa holders. Use when work authorization expiry approaches."
  - Bad: "I-9 stuff"

- **Files**:
  - `SKILL.md` - Required, main documentation
  - `scripts/` - Optional, compliance checkers and automation
  - `references/` - Optional, regulatory references
  - `assets/` - Optional, templates and checklists

---

## Extraction Checklist

Before creating a skill from an HR finding:

- [ ] Finding is verified (status: resolved, remediation confirmed)
- [ ] Solution is broadly applicable (not department-specific one-off)
- [ ] **No PII in any content** (names, SSNs, salaries, medical info)
- [ ] Content is complete (has all needed remediation context)
- [ ] Jurisdiction is specified where applicable
- [ ] Name follows conventions
- [ ] Description is concise but includes HR triggers
- [ ] Quick Reference table maps situations to actions
- [ ] Regulatory references included where applicable
- [ ] Source entry ID is recorded

After creating:

- [ ] Update original entry with `promoted_to_skill` status
- [ ] Add `Skill-Path: skills/skill-name` to entry metadata
- [ ] Test skill by reading it in a fresh session
- [ ] Verify no PII leaked into the skill
