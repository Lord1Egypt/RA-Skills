#!/bin/bash
# Sales Self-Improvement Error Detector Hook
# Triggers on PostToolUse for Bash to detect deal-related signals
# Reads CLAUDE_TOOL_OUTPUT environment variable

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

ERROR_PATTERNS=(
    "lost deal"
    "churned"
    "discount"
    "competitor"
    "objection"
    "forecast"
    "pipeline"
    "quota"
    "slipped"
    "stalled"
    "no decision"
    "lost to"
    "deal lost"
    "churn"
    "pushed deal"
    "missed forecast"
    "over-forecast"
    "under-forecast"
    "pricing error"
    "wrong price"
    "deprecated tier"
    "budget freeze"
    "no budget"
    "went dark"
    "ghosted"
    "declined meeting"
    "champion left"
    "reorg"
    "procurement delay"
    "legal delay"
    "security review"
    "RFP"
    "competitive eval"
    "vendor switch"
    "free tier"
    "undercut"
    "win rate"
    "close rate"
    "conversion rate"
    "stage duration"
    "days in stage"
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
<sales-issue-detected>
A sales signal was detected in command output. Consider logging to .learnings/ if:
- Deal lost or churned → DEAL_ISSUES.md [DEAL-YYYYMMDD-XXX] with loss reason
- Competitor mentioned or undercut pricing → LEARNINGS.md with competitor_shift category
- Objection pattern surfaced → LEARNINGS.md with objection_pattern category
- Forecast or pipeline metric missed → DEAL_ISSUES.md with forecast_miss category
- Discount or pricing issue → DEAL_ISSUES.md with pricing_error category
- Deal stalled or slipped → DEAL_ISSUES.md with pipeline_leak category

Include deal context (anonymized), segment, and area tag.
</sales-issue-detected>
EOF
fi
