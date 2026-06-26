#!/bin/bash
# Security Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind about security finding capture
# Keep output minimal (~80-120 tokens) to minimize overhead

set -e

cat << 'EOF'
<security-improvement-reminder>
After completing this task, evaluate if any security findings should be captured:
- Vulnerability discovered (CVE, injection, broken auth)?
- Misconfiguration found (permissions, policies, open ports)?
- Access control issue (unauthorized access, privilege escalation)?
- Secrets or credentials in output? → REDACT IMMEDIATELY before logging
- Compliance gap identified (missing control, audit finding)?

CRITICAL: NEVER log actual secrets, credentials, tokens, private keys, or PII.
Always use REDACTED_* placeholders.

If yes: Log to .learnings/ using the security self-improvement format.
  - Vulnerabilities/incidents → SECURITY_INCIDENTS.md [SEC-YYYYMMDD-XXX]
  - Misconfigs/compliance/intel → LEARNINGS.md [LRN-YYYYMMDD-XXX]
If high-value (recurring, broadly applicable): Promote to hardening checklist or playbook.
</security-improvement-reminder>
EOF
