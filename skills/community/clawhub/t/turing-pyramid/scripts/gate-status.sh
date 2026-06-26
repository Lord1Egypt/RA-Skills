#!/bin/bash
# gate-status.sh — Display execution gate status (human-readable)

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/mindstate-utils.sh"

GATE_FILE="$(_ms_assets)/pending_actions.json"

if [[ ! -f "$GATE_FILE" ]]; then
    echo "🚪 Execution Gate: No actions tracked"
    exit 0
fi

echo "🚪 Execution Gate Status"
echo "========================"
echo ""

gate_status=$(jq -r '.gate_status // "CLEAR"' "$GATE_FILE")
pending=$(jq -r '.pending_count // 0' "$GATE_FILE")
completed=$(jq -r '.completed_count // 0' "$GATE_FILE")
deferred=$(jq -r '.deferred_count // 0' "$GATE_FILE")

if [[ "$gate_status" == "BLOCKED" ]]; then
    echo "Status: 🚫 BLOCKED ($pending pending)"
else
    echo "Status: ✅ CLEAR"
fi
echo "Completed: $completed | Deferred: $deferred | Pending: $pending"
echo ""

# Show pending actions
if (( pending > 0 )); then
    echo "Pending actions:"
    jq -r '.actions[] | select(.status == "PENDING") |
        " ▶ \(.need): \(.action_name) (impact: \(.impact)) — \(.evidence_type)"' "$GATE_FILE"
    echo ""
fi

# Show recent completed
completed_recent=$(jq -r '[.actions[] | select(.status == "COMPLETED")] | length' "$GATE_FILE")
if (( completed_recent > 0 )); then
    echo "Recently completed:"
    jq -r '.actions[] | select(.status == "COMPLETED") |
        " ✓ \(.need): \(.action_name) — \(.resolution)"' "$GATE_FILE" | tail -5
    echo ""
fi

# Show deferred
deferred_count=$(jq -r '[.actions[] | select(.status == "DEFERRED")] | length' "$GATE_FILE")
if (( deferred_count > 0 )); then
    echo "Deferred:"
    jq -r '.actions[] | select(.status == "DEFERRED") |
        " ○ \(.need): \(.action_name) — \(.defer_reason)"' "$GATE_FILE"
    echo ""
fi

# Analytics: execution rate
total=$(jq '.actions | length' "$GATE_FILE")
if (( total > 0 )); then
    rate=$(echo "scale=0; $completed * 100 / $total" | bc -l 2>/dev/null || echo 0)
    echo "Execution rate: ${rate}% ($completed/$total)"

    self_reported=$(jq '[.actions[] | select(.resolution != null and (.resolution | startswith("self-reported")))] | length' "$GATE_FILE")
    if (( self_reported > 0 )); then
        echo "  ⚠ $self_reported self-reported (low-trust evidence)"
    fi
fi
