---
name: security-scanner-triage
description: Triage security/virus scanner findings for skills and automations. Use when scanner reports mixed-risk findings (defaults, credential handling, data routing, metadata mismatch, docs inconsistency). Do not use for live incident response requiring SOC tooling. Success = prioritized true issues, false positives called out, and concrete remediation patch plan.
---

# Security Scanner Triage

## Workflow

1. Normalize findings
- Convert scanner text into discrete claims.
- Group by category: data routing, credentials, defaults, docs mismatch, privilege/persistence.

2. Verify against code/docs
- Locate exact file/line evidence.
- Mark each claim as:
  - Confirmed
  - Partially confirmed
  - Not reproducible

3. Risk rate
- Critical / High / Medium / Low
- Include blast radius and exploitability notes.

4. Remediation plan
- Provide minimal patch order:
  1) safety first
  2) behavior/docs consistency
  3) version bump and publish notes

5. Verification
- Provide re-scan checklist and expected clean-state signals.

## Output format

Use `references/output-template.md`.

## Guardrails

- Never leak secrets from `.env`.
- Distinguish trust/disclosure issues from active vulnerabilities.
- Always separate "data-routing transparency" findings from "security-impact" findings.
