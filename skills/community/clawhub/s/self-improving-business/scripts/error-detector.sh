#!/bin/bash
# Business Self-Improvement Error Detector Hook
# Inspects CLAUDE_TOOL_OUTPUT in-process only. Never writes tool output, secrets, or transcripts to disk.
# Reminder-only pattern detector for PostToolUse (Bash)

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"
# Scan a bounded prefix in memory only. Never print, store, or forward command output.
OUTPUT="${OUTPUT:0:2000}"

BUSINESS_PATTERNS=(
    "missed SLA"
    "overdue approval"
    "RACI conflict"
    "KPI variance"
    "budget overrun warning"
    "handoff failure"
    "missing policy"
    "audit issue"
    "dependency blocked"
    "approval delay"
    "escalation overdue"
    "ownership unclear"
    "policy exception"
    "vendor blocked"
)

contains_pattern=false
matched_pattern=""
for pattern in "${BUSINESS_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_pattern=true
        matched_pattern="$pattern"
        break
    fi
done

if [ "$contains_pattern" = true ]; then
    cat << EOF
<business-finding-detected>
High-signal business administration pattern detected: "$matched_pattern"

Consider logging if this reflects a real operating signal:
- missed SLA
- overdue approval
- RACI conflict
- KPI variance
- budget overrun warning
- handoff failure
- missing policy
- audit issue
- dependency blocked

Reminder-only safety:
- Do NOT execute approvals, spending, vendor commitments, payroll, or legal actions.
- Recommend explicit human approval for high-impact decisions.

Format:
- [LRN-YYYYMMDD-XXX] for reusable learnings
- [BUS-YYYYMMDD-XXX] for active business issues
- [FEAT-YYYYMMDD-XXX] for requested capabilities
</business-finding-detected>
EOF
fi
