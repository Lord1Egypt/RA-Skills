#!/bin/bash
# Negotiation Self-Improvement Error Detector Hook
# Triggers on PostToolUse for Bash to detect high-signal negotiation patterns.
# Reminder-only behavior: no auto approvals or agreement actions.

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"
LOWER_OUTPUT="$(printf '%s' "$OUTPUT" | tr '[:upper:]' '[:lower:]')"

ERROR_PATTERNS=(
    "deadlock"
    "stalled"
    "no movement"
    "repeated objection"
    "scope creep"
    "concession"
    "discount exception"
    "threshold exceeded"
    "batna not defined"
    "no batna"
    "approval missing"
    "not approved"
    "term ambiguity"
    "ambiguous clause"
    "redline unresolved"
    "open redline"
    "walk-away undefined"
    "anchor drift"
    "best and final"
    "procurement blocked"
)

contains_signal=false
for pattern in "${ERROR_PATTERNS[@]}"; do
    if [[ "$LOWER_OUTPUT" == *"$pattern"* ]]; then
        contains_signal=true
        break
    fi
done

if [ "$contains_signal" = true ]; then
    cat << 'EOF'
<negotiation-signal-detected>
A negotiation risk signal was detected. Consider logging:
- Deadlock / repeated objection -> NEGOTIATION_ISSUES.md (framing_miss or escalation_misalignment)
- Scope creep or concession over threshold -> NEGOTIATION_ISSUES.md (concession_leak / agreement_risk)
- BATNA missing -> NEGOTIATION_ISSUES.md (batna_weakness)
- Approval missing -> NEGOTIATION_ISSUES.md (escalation_misalignment)
- Term ambiguity or unresolved redline -> NEGOTIATION_ISSUES.md (agreement_risk)
- Anchor drift / value framing miss -> LEARNINGS.md (anchor_error / value_articulation_gap)

Reminder-only: do not auto-accept terms, commit pricing, execute approvals, or finalize agreements.
Escalate to human approvers for high-impact concessions and final terms.
</negotiation-signal-detected>
EOF
fi
