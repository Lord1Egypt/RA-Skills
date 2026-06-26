# Security Incidents Log

Vulnerability discoveries, access violations, secrets exposure, and active security incidents.

**Categories**: vulnerability | access_violation | secrets_exposure | active_incident
**Areas**: authentication | authorization | encryption | network | endpoint | compliance | cloud
**Statuses**: pending | in_progress | contained | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet triaged or investigated |
| `in_progress` | Actively being investigated or remediated |
| `contained` | Immediate threat neutralized, root cause analysis ongoing |
| `resolved` | Fully remediated and verified |
| `wont_fix` | Risk accepted with documented justification |
| `promoted` | Elevated to hardening checklist, runbook, or playbook |
| `promoted_to_skill` | Extracted as a reusable security skill |

## CRITICAL REMINDER

**NEVER log actual secrets, credentials, tokens, private keys, or PII in this file.**
Always use `REDACTED_*` placeholders. Describe the *type* of exposure, not the *content*.

## Severity Definitions

| Severity | Criteria |
|----------|----------|
| `critical` | Active exploitation, data breach confirmed, zero-day in production |
| `high` | Known CVE unpatched, secrets in CI logs, auth bypass on public endpoint |
| `medium` | Misconfiguration with compensating controls, limited blast radius |
| `low` | Informational finding, defense-in-depth improvement |

---
