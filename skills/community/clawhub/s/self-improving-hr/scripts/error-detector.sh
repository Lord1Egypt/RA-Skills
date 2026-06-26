#!/bin/bash
# HR Self-Improvement Error Detector Hook
# Triggers on PostToolUse for Bash to detect compliance issues, violations, and HR process errors
# Reads CLAUDE_TOOL_OUTPUT environment variable

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

ERROR_PATTERNS=(
    "compliance"
    "violation"
    "overdue"
    "terminated"
    "grievance"
    "EEOC"
    "FMLA"
    "ADA"
    "discrimination"
    "harassment"
    "expired"
    "deadline"
    "COBRA"
    "HIPAA"
    "FLSA"
    "WARN Act"
    "I-9"
    "OSHA"
    "audit"
    "misconduct"
    "retaliation"
    "wrongful"
    "severance"
    "unemployment"
    "workers comp"
    "leave of absence"
    "reasonable accommodation"
    "protected class"
    "hostile work environment"
    "wage and hour"
    "exempt status"
    "misclassification"
)

contains_error=false
for pattern in "${ERROR_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_error=true
        break
    fi
done

if [ "$contains_error" = true ]; then
    cat << 'EOF'
<hr-issue-detected>
An HR/compliance term was detected in command output. Consider logging to .learnings/ if:
- Compliance violation or regulatory risk found → HR_PROCESS_ISSUES.md [HRP-YYYYMMDD-XXX]
- Policy gap or missing procedure identified → LEARNINGS.md with policy_gap category
- Employee relations issue pattern emerging → LEARNINGS.md with retention_signal category
- Process failure or benefits error discovered → HR_PROCESS_ISSUES.md with process_inefficiency

NEVER log PII. Anonymize all details. Specify jurisdiction and regulation.
</hr-issue-detected>
EOF
fi
