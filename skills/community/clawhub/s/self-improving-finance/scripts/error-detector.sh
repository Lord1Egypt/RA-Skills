#!/bin/bash
# Finance Self-Improvement Error Detector Hook
# Triggers on PostToolUse for Bash to detect reconciliation issues, variances, and control failures
# Reads CLAUDE_TOOL_OUTPUT environment variable

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

ERROR_PATTERNS=(
    "reconciliation"
    "variance"
    "imbalance"
    "overdue"
    "misstatement"
    "audit finding"
    "SOX"
    "material"
    "write-off"
    "accrual"
    "depreciation"
    "amortization"
    "unreconciled"
    "past due"
    "out of balance"
    "control failure"
    "control deficiency"
    "significant deficiency"
    "material weakness"
    "restatement"
    "adjusting entry"
    "journal entry"
    "intercompany"
    "elimination"
    "aging"
    "bad debt"
    "allowance"
    "impairment"
    "covenant"
    "liquidity"
    "cash shortfall"
    "budget overrun"
    "forecast miss"
    "late close"
    "cutoff"
    "deferred revenue"
    "prepaid"
    "unearned"
    "contingent liability"
    "subsequent event"
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
<finance-issue-detected>
A finance-related issue was detected in command output. Consider logging to .learnings/ if:
- Reconciliation break or imbalance found → FINANCE_ISSUES.md [FIN-YYYYMMDD-XXX]
- Control failure or SOX deficiency identified → FINANCE_ISSUES.md with control_test trigger
- Budget/forecast variance exceeds threshold → FINANCE_ISSUES.md with variance_analysis trigger
- Audit finding or misstatement risk → FINANCE_ISSUES.md with audit trigger
- Control weakness or regulatory gap → LEARNINGS.md with appropriate category

ALWAYS ANONYMIZE: No real account numbers, bank details, client names, or specific figures.
Include area tag (accounting, treasury, tax, audit, budgeting, reporting, AP, AR).
</finance-issue-detected>
EOF
fi
