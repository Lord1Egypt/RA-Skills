#!/bin/bash
# Support Self-Improvement Issue Detector Hook
# Triggers on PostToolUse for Bash to detect SLA breaches, escalation failures, and churn signals
# Reads CLAUDE_TOOL_OUTPUT environment variable

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

ISSUE_PATTERNS=(
    "SLA"
    "sla"
    "breach"
    "breached"
    "escalat"
    "reopen"
    "reopened"
    "unsatisfied"
    "complaint"
    "churn"
    "cancel"
    "cancellation"
    "refund"
    "unacceptable"
    "frustrated"
    "disappointed"
    "downgrade"
    "alternative"
    "competitor"
    "misdiagnos"
    "misroute"
    "wrong team"
    "overdue"
    "expired"
    "timed out"
    "no results found"
    "article not found"
    "knowledge base"
    "CSAT"
    "csat"
    "NPS"
    "detractor"
    "priority 1"
    "P1"
    "outage"
    "incident"
)

contains_issue=false
for pattern in "${ISSUE_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_issue=true
        break
    fi
done

if [ "$contains_issue" = true ]; then
    cat << 'EOF'
<support-issue-detected>
A support issue signal was detected in command output. Consider logging to .learnings/ if:
- SLA breach or approaching breach → TICKET_ISSUES.md [TKT-YYYYMMDD-XXX]
- Misdiagnosis or wrong escalation path → TICKET_ISSUES.md with root cause analysis
- Customer churn signal (cancellation, frustration) → LEARNINGS.md (customer_churn_signal)
- Knowledge base gap (no article found) → LEARNINGS.md (knowledge_gap)
- Escalation failure (wrong team, delayed routing) → LEARNINGS.md (escalation_gap)

Include ticket timeline, customer impact, and prevention steps.
Anonymise all customer data — use ticket IDs only.
</support-issue-detected>
EOF
fi
