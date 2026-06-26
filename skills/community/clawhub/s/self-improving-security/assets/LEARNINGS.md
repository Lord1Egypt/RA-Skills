# Security Learnings

Vulnerabilities, misconfigurations, compliance gaps, and security insights captured during development and operations.

**Categories**: vulnerability | misconfiguration | access_violation | compliance_gap | incident_response | threat_intelligence
**Areas**: authentication | authorization | encryption | network | endpoint | compliance | cloud
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being investigated or remediated |
| `resolved` | Issue fixed, control implemented, or knowledge integrated |
| `wont_fix` | Risk accepted (justification required in Resolution) |
| `promoted` | Elevated to hardening checklist, compliance matrix, or playbook |
| `promoted_to_skill` | Extracted as a reusable security skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250415-001] misconfiguration

**Logged**: 2025-04-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/s3-bucket-hardening
**Area**: cloud

### Summary
S3 bucket misconfigured with public read access exposing internal assets
...
```

## CRITICAL REMINDER

**NEVER log actual secrets, credentials, tokens, private keys, or PII.**
Always redact sensitive values. Describe the *type* and *location*, not the *content*.

---
