#!/bin/bash
# gate-propose.sh — Register a pending action in the execution gate
# Usage: gate-propose.sh --need <need> --action <name> --impact <n> \
#            [--evidence-type <type>] [--evidence-hint <hint>] [--source <src>]
# Writes to pending_actions.json. Does NOT execute anything.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/mindstate-utils.sh"

GATE_FILE="$(_ms_assets)/pending_actions.json"
GATE_LOCK="$(_ms_assets)/gate.lock"

# Acquire gate lock (fd 203)
exec 203>"$GATE_LOCK"
flock -w 5 203 || { echo "gate-propose: lock timeout" >&2; exit 1; }

# Parse args
NEED="" ACTION="" IMPACT="" EVIDENCE_TYPE="auto" EVIDENCE_HINT="" SOURCE="run-cycle" DEFERRABLE=true
while [[ $# -gt 0 ]]; do
    case "$1" in
        --need) NEED="$2"; shift 2 ;;
        --action) ACTION="$2"; shift 2 ;;
        --impact) IMPACT="$2"; shift 2 ;;
        --evidence-type) EVIDENCE_TYPE="$2"; shift 2 ;;
        --evidence-hint) EVIDENCE_HINT="$2"; shift 2 ;;
        --source) SOURCE="$2"; shift 2 ;;
        --non-deferrable) DEFERRABLE=false; shift ;;
        *) shift ;;
    esac
done

[[ -z "$NEED" || -z "$ACTION" || -z "$IMPACT" ]] && {
    echo "Usage: gate-propose.sh --need <need> --action <name> --impact <n>" >&2
    exit 1
}

NOW_ISO=$(now_iso)
NOW_EPOCH=$(now_epoch)
ACTION_ID="act_${NOW_EPOCH}_${NEED}_$(printf '%03d' $((RANDOM % 1000)))"

# Initialize gate file if missing
if [[ ! -f "$GATE_FILE" ]]; then
    echo '{"actions":[],"gate_status":"CLEAR","pending_count":0,"completed_count":0,"deferred_count":0}' > "$GATE_FILE"
fi

# Read action mode (deliberative/operative) for gate metadata
CONFIG_FILE=$(mindstate_config_file)
ACTION_MODE=$(jq -r --arg n "$NEED" --arg a "$ACTION" \
    '(.needs[$n].actions[] | select(.name == $a) | .mode) // "operative"' \
    "$CONFIG_FILE" 2>/dev/null || echo "operative")

# Auto-detect evidence type if "auto"
if [[ "$EVIDENCE_TYPE" == "auto" ]]; then
    # Check needs-config.json for action evidence block
    declared_type=$(jq -r --arg n "$NEED" --arg a "$ACTION" \
        '.needs[$n].actions[] | select(.name == $a) | .evidence.type // "auto"' \
        "$CONFIG_FILE" 2>/dev/null || echo "auto")

    if [[ "$declared_type" != "auto" && -n "$declared_type" ]]; then
        EVIDENCE_TYPE="$declared_type"
    else
        # Default: require mark-satisfied as minimum evidence
        EVIDENCE_TYPE="mark_satisfied"
    fi
fi

# Append action to pending queue (atomic write)
jq --arg id "$ACTION_ID" \
    --arg ts "$NOW_ISO" \
    --arg src "$SOURCE" \
    --arg need "$NEED" \
    --arg action "$ACTION" \
    --argjson impact "$IMPACT" \
    --arg etype "$EVIDENCE_TYPE" \
    --arg ehint "$EVIDENCE_HINT" \
    --argjson deferrable "$DEFERRABLE" \
    --arg mode "$ACTION_MODE" \
    '.actions += [{
        id: $id,
        timestamp: $ts,
        source: $src,
        need: $need,
        action_name: $action,
        impact: $impact,
        evidence_type: $etype,
        evidence_hint: $ehint,
        deferrable: $deferrable,
        action_mode: $mode,
        status: "PENDING",
        resolved_at: null,
        resolution: null,
        defer_reason: null
    }] | .pending_count = ([.actions[] | select(.status == "PENDING")] | length) |
    .gate_status = (if .pending_count > 0 then "BLOCKED" else "CLEAR" end)' \
    "$GATE_FILE" > "$GATE_FILE.tmp.$$" && mv "$GATE_FILE.tmp.$$" "$GATE_FILE"

echo "[GATE] Proposed: $ACTION_ID ($NEED: $ACTION, evidence: $EVIDENCE_TYPE)"
