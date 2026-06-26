# Support Skill Template

Template for creating support skills extracted from learnings and ticket issues. Copy and customize.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Concise description of the support skill and when to use it. Include trigger conditions."
---

# Skill Name

Brief introduction explaining the support problem this skill addresses and its origin.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Support trigger 1] | [Resolution 1] |
| [Support trigger 2] | [Resolution 2] |

## Background

Why this support knowledge matters. What ticket patterns or customer impact it prevents. Context from the original finding.

## Resolution

### Step-by-Step

1. First triage or diagnostic step
2. Resolution or workaround step
3. Verification step (confirm with customer, check monitoring)

### Example Response

\`\`\`
Hi [Customer],

Thank you for reaching out. I've identified the issue and here's what we need to do:

[Resolution steps tailored to the customer's situation]

Please let me know if this resolves the issue. I'll follow up in 24 hours to confirm.

Best regards,
[Agent]
\`\`\`

## Common Variations

- **Variation A**: Different product tier or channel specifics
- **Variation B**: Alternative resolution for edge cases

## Gotchas

- Warning or common misdiagnosis #1
- Warning or common misdiagnosis #2
- **NEVER** include customer PII in any documentation

## Related Resources

- KB Article: link-to-article
- Escalation Path: team or on-call contact
- Product Documentation: link-to-docs

## Source

Extracted from support learning or ticket issue entry.
- **Entry ID**: LRN-YYYYMMDD-XXX or TKT-YYYYMMDD-XXX
- **Original Category**: resolution_delay | misdiagnosis | escalation_gap | knowledge_gap
- **Extraction Date**: YYYY-MM-DD
```

---

## Minimal Template

For simple support skills:

```markdown
---
name: skill-name-here
description: "What this support skill does and when to use it."
---

# Skill Name

[Support problem statement in one sentence]

## Resolution

[Direct resolution steps]

## Source

- Entry ID: LRN-YYYYMMDD-XXX or TKT-YYYYMMDD-XXX
```

---

## Template with Scripts

For support skills that include diagnostic helpers or automation scripts:

```markdown
---
name: skill-name-here
description: "What this support skill does and when to use it."
---

# Skill Name

[Introduction]

## Quick Reference

| Command | Purpose |
|---------|---------|
| `./scripts/diagnose.sh` | [What it checks] |
| `./scripts/resolve.sh` | [What it fixes] |
| `./scripts/verify.sh` | [What it verifies] |

## Usage

### Automated (Recommended)

\`\`\`bash
./skills/skill-name/scripts/diagnose.sh [customer-env]
\`\`\`

### Manual Steps

1. Step one
2. Step two

## Scripts

| Script | Description |
|--------|-------------|
| `scripts/diagnose.sh` | Diagnostic checks for the issue |
| `scripts/resolve.sh` | Applies the resolution |
| `scripts/verify.sh` | Verifies the fix with the customer |

## Source

- Entry ID: TKT-YYYYMMDD-XXX
```

---

## Naming Conventions

- **Skill name**: lowercase, hyphens for spaces
  - Good: `502-gateway-diagnosis`, `sso-login-failures`, `sla-breach-prevention`
  - Bad: `502_Gateway_Diagnosis`, `SSOLoginFailures`

- **Description**: Start with action verb, mention support trigger
  - Good: "Diagnoses 502 Bad Gateway errors caused by customer WAF misconfiguration. Use when customer reports intermittent 502s on API callbacks."
  - Bad: "502 stuff"

- **Files**:
  - `SKILL.md` - Required, main documentation
  - `scripts/` - Optional, diagnostic and resolution scripts
  - `references/` - Optional, related KB articles and escalation paths
  - `assets/` - Optional, response templates

---

## Extraction Checklist

Before creating a skill from a support finding:

- [ ] Finding is verified (status: resolved, resolution confirmed with customer)
- [ ] Solution is broadly applicable (not customer-specific one-off)
- [ ] **No customer PII, credentials, or internal tokens in any content**
- [ ] Content is complete (has all needed diagnostic and resolution context)
- [ ] Name follows conventions
- [ ] Description is concise but includes support triggers
- [ ] Quick Reference table maps symptoms to actions
- [ ] Resolution steps are tested and verified
- [ ] Related KB articles and escalation paths are referenced
- [ ] Source entry ID is recorded

After creating:

- [ ] Update original entry with `promoted_to_skill` status
- [ ] Add `Skill-Path: skills/skill-name` to entry metadata
- [ ] Test skill by reading it in a fresh session
- [ ] Verify no customer data leaked into the skill
