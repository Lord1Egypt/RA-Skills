# Security Skill Template

Template for creating security skills extracted from learnings and incidents. Copy and customize.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Concise description of the security skill and when to use it. Include trigger conditions."
---

# Skill Name

Brief introduction explaining the security problem this skill addresses and its origin.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Security trigger 1] | [Remediation 1] |
| [Security trigger 2] | [Remediation 2] |

## Background

Why this security knowledge matters. What vulnerabilities or risks it prevents. Context from the original finding.

## Remediation

### Step-by-Step

1. First remediation step with command or configuration
2. Second step
3. Verification step (scan, test, or manual check)

### Code/Config Example

\`\`\`language
// Example showing the secure configuration or code pattern
\`\`\`

## Common Variations

- **Variation A**: Different environment or platform specifics
- **Variation B**: Alternative remediation approach

## Gotchas

- Warning or common mistake during remediation #1
- Warning or common mistake during remediation #2
- **NEVER** log actual secrets — always redact before documenting

## Related Standards

- CWE: CWE-XXX
- OWASP: Reference
- Compliance: SOC2 / GDPR / HIPAA / PCI-DSS control reference

## Source

Extracted from security learning or incident entry.
- **Entry ID**: LRN-YYYYMMDD-XXX or SEC-YYYYMMDD-XXX
- **Original Category**: vulnerability | misconfiguration | compliance_gap | incident_response
- **Extraction Date**: YYYY-MM-DD
```

---

## Minimal Template

For simple security skills:

```markdown
---
name: skill-name-here
description: "What this security skill does and when to use it."
---

# Skill Name

[Security problem statement in one sentence]

## Remediation

[Direct fix with commands/configuration]

## Source

- Entry ID: LRN-YYYYMMDD-XXX or SEC-YYYYMMDD-XXX
```

---

## Template with Scripts

For security skills that include scanner helpers or hardening scripts:

```markdown
---
name: skill-name-here
description: "What this security skill does and when to use it."
---

# Skill Name

[Introduction]

## Quick Reference

| Command | Purpose |
|---------|---------|
| `./scripts/scan.sh` | [What it scans] |
| `./scripts/harden.sh` | [What it hardens] |
| `./scripts/verify.sh` | [What it verifies] |

## Usage

### Automated (Recommended)

\`\`\`bash
./skills/skill-name/scripts/scan.sh [target]
\`\`\`

### Manual Steps

1. Step one
2. Step two

## Scripts

| Script | Description |
|--------|-------------|
| `scripts/scan.sh` | Vulnerability or misconfiguration scanner |
| `scripts/harden.sh` | Applies hardening configuration |
| `scripts/verify.sh` | Verifies remediation was effective |

## Source

- Entry ID: SEC-YYYYMMDD-XXX
```

---

## Naming Conventions

- **Skill name**: lowercase, hyphens for spaces
  - Good: `s3-bucket-hardening`, `jwt-validation-patterns`, `secret-rotation`
  - Bad: `S3_Bucket_Hardening`, `JWTValidation`

- **Description**: Start with action verb, mention security trigger
  - Good: "Hardens S3 bucket configurations against public access. Use when S3 buckets are created or audited."
  - Bad: "S3 stuff"

- **Files**:
  - `SKILL.md` - Required, main documentation
  - `scripts/` - Optional, scanners and hardening scripts
  - `references/` - Optional, compliance mappings
  - `assets/` - Optional, templates

---

## Extraction Checklist

Before creating a skill from a security finding:

- [ ] Finding is verified (status: resolved, remediation confirmed)
- [ ] Solution is broadly applicable (not environment-specific one-off)
- [ ] **No secrets, credentials, or PII in any content**
- [ ] Content is complete (has all needed remediation context)
- [ ] Name follows conventions
- [ ] Description is concise but includes security triggers
- [ ] Quick Reference table maps threats to actions
- [ ] Code/config examples are tested
- [ ] CWE/CVE references included where applicable
- [ ] Source entry ID is recorded

After creating:

- [ ] Update original entry with `promoted_to_skill` status
- [ ] Add `Skill-Path: skills/skill-name` to entry metadata
- [ ] Test skill by reading it in a fresh session
- [ ] Verify no sensitive data leaked into the skill
