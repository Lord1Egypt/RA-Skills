#!/bin/bash
# Security Self-Improvement Error Detector Hook (Optional)
# Conservative detector for high-signal security failures only.
# Reads CLAUDE_TOOL_OUTPUT (when provided by PostToolUse).

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

# If hook context didn't provide output, do nothing.
[ -n "$OUTPUT" ] || exit 0

SECURITY_PATTERNS=(
    "CVE-"
    "CRITICAL"
    "HIGH severity"
    "unauthorized"
    "forbidden"
    "authentication failed"
    "invalid token"
    "expired token"
    "certificate expired"
    "certificate verify failed"
    "privilege escalation"
    "SQL injection"
    "command injection"
    "path traversal"
    "open redirect"
    "SSRF"
    "XXE"
)

contains_security_pattern=false
matched_pattern=""
for pattern in "${SECURITY_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_security_pattern=true
        matched_pattern="$pattern"
        break
    fi
done

if [ "$contains_security_pattern" = true ]; then
    cat << EOF
<security-finding-detected>
High-signal security pattern detected in command output: "$matched_pattern"

Log only when the finding required investigation or is likely to recur.
- Vulnerability/CVE identified
- Access-control or authentication issue confirmed
- Critical transport/authn/authz failure observed

CRITICAL: NEVER log actual secrets, credentials, tokens, or PII.
Use REDACTED_* placeholders. Describe the type, not the content.

Format: [SEC-YYYYMMDD-XXX] for incidents, [LRN-YYYYMMDD-XXX] for learnings.
</security-finding-detected>
EOF
fi
