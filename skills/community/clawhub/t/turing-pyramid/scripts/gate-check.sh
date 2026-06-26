#!/bin/bash
# gate-check.sh — Check if heartbeat can proceed
# Returns: exit 0 = CLEAR (heartbeat OK), exit 1 = BLOCKED (actions pending)
# Also handles timeout: auto-defers actions older than max_action_time
# Called by run-cycle.sh (structural enforcement, not advisory)

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/mindstate-utils.sh"

GATE_FILE="$(_ms_assets)/pending_actions.json"
GATE_LOCK="$(_ms_assets)/gate.lock"
MS_CONFIG=$(mindstate_ms_config)

# No gate file = nothing pending
[[ ! -f "$GATE_FILE" ]] && exit 0

# Check if execution gate is enabled
enabled=$(jq -r '.execution_gate.enabled // false' "$MS_CONFIG" 2>/dev/null || echo "false")
[[ "$enabled" != "true" ]] && exit 0

NOW_EPOCH=$(now_epoch)
NOW_ISO=$(now_iso)

# Max time an action can stay pending before auto-defer (seconds)
MAX_ACTION_TIME=$(jq -r '.execution_gate.max_action_time_seconds // 600' "$MS_CONFIG" 2>/dev/null || echo 600)

# Acquire gate lock for mutations (fd 203)
exec 203>"$GATE_LOCK"
flock -w 5 203 || { echo "gate-check: lock timeout" >&2; exit 1; }

# Check for timed-out pending actions → auto-defer
pending_ids=$(jq -r '.actions[] | select(.status == "PENDING") | .id' "$GATE_FILE" 2>/dev/null)

for action_id in $pending_ids; do
    action_ts=$(jq -r --arg id "$action_id" '.actions[] | select(.id == $id) | .timestamp' "$GATE_FILE")
    action_epoch=$(date -d "$action_ts" +%s 2>/dev/null || echo 0)
    age=$((NOW_EPOCH - action_epoch))

    if (( age > MAX_ACTION_TIME )); then
        action_name=$(jq -r --arg id "$action_id" '.actions[] | select(.id == $id) | .action_name' "$GATE_FILE")
        need=$(jq -r --arg id "$action_id" '.actions[] | select(.id == $id) | .need' "$GATE_FILE")

        # Auto-defer with timeout reason
        jq --arg id "$action_id" --arg ts "$NOW_ISO" --arg age "$age" \
            '(.actions[] | select(.id == $id and .status == "PENDING")) |=
            (.status = "DEFERRED" | .resolved_at = $ts | .defer_reason = ("timeout after " + $age + "s")) |
            .pending_count = ([.actions[] | select(.status == "PENDING")] | length) |
            .deferred_count = ([.actions[] | select(.status == "DEFERRED")] | length) |
            .gate_status = (if .pending_count > 0 then "BLOCKED" else "CLEAR" end)' \
            "$GATE_FILE" > "$GATE_FILE.tmp.$$" && mv "$GATE_FILE.tmp.$$" "$GATE_FILE"

        echo "⚠ [GATE] Auto-deferred: $need/$action_name (timeout: ${age}s)" >&2
    fi
done

# Final check
pending_count=$(jq -r '.pending_count // 0' "$GATE_FILE" 2>/dev/null)

if (( pending_count > 0 )); then
    echo "🚫 [GATE] BLOCKED — $pending_count action(s) still pending:" >&2
    jq -r '.actions[] | select(.status == "PENDING") | " • \(.need): \(.action_name)"' "$GATE_FILE" >&2
    echo "" >&2
    echo "Execute the actions, then:" >&2
    jq -r '.actions[] | select(.status == "PENDING") | "  gate-resolve.sh --need \(.need) --evidence \"what you did\""' "$GATE_FILE" >&2
    echo "Or defer:" >&2
    jq -r '.actions[] | select(.status == "PENDING") | "  gate-resolve.sh --defer \(.id) --reason \"why\""' "$GATE_FILE" >&2
    exit 1
else
    # Clear — clean up completed/deferred actions older than 24h
    CUTOFF_ISO=$(date -u -d '24 hours ago' +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || echo "1970-01-01T00:00:00Z")
    jq --arg cutoff "$CUTOFF_ISO" \
        '.actions |= [.[] | select(
            .status == "PENDING" or
            ((.resolved_at // "9999") > $cutoff)
        )]' "$GATE_FILE" > "$GATE_FILE.tmp.$$" 2>/dev/null && mv "$GATE_FILE.tmp.$$" "$GATE_FILE" || true

    echo "✅ [GATE] CLEAR — all actions resolved"
    exit 0
fi
