#!/bin/bash
# gate-resolve.sh — Resolve a pending action with evidence
# Usage: gate-resolve.sh <action_id> [--evidence "description"] [--self-report]
#        gate-resolve.sh --need <need> [--evidence "..."] (resolves first pending for need)
#        gate-resolve.sh --defer <action_id> --reason "why"

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/mindstate-utils.sh"

GATE_FILE="$(_ms_assets)/pending_actions.json"
GATE_LOCK="$(_ms_assets)/gate.lock"
AUDIT_LOG="$(mindstate_audit_log)"

# Acquire gate lock (fd 203)
exec 203>"$GATE_LOCK"
flock -w 5 203 || { echo "gate-resolve: lock timeout" >&2; exit 1; }

[[ ! -f "$GATE_FILE" ]] && { echo "No pending actions file" >&2; exit 1; }

# Parse args
ACTION_ID="" NEED="" EVIDENCE="" SELF_REPORT=false DEFER=false DEFER_REASON="" CONCLUSION=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --need) NEED="$2"; shift 2 ;;
        --evidence) EVIDENCE="$2"; shift 2 ;;
        --conclusion) CONCLUSION="$2"; shift 2 ;;
        --conclusion=*) CONCLUSION="${1#*=}"; shift ;;
        --self-report) SELF_REPORT=true; shift ;;
        --defer) DEFER=true; ACTION_ID="$2"; shift 2 ;;
        --reason) DEFER_REASON="$2"; shift 2 ;;
        --close) CLOSE=true; ACTION_ID="$2"; shift 2 ;;
        --close-reason) CLOSE_REASON="$2"; shift 2 ;;
        *) [[ -z "$ACTION_ID" ]] && ACTION_ID="$1"; shift ;;
    esac
done

CLOSE=${CLOSE:-false}
CLOSE_REASON=${CLOSE_REASON:-}

NOW_ISO=$(now_iso)

# Scrub sensitive data early (before defer/resolve branch)
_scrub_sensitive() {
    echo "$1" | sed -E '
        s/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[IP]/g;
        s|/home/[a-z]+/|~/|g;
        s/[a-zA-Z0-9_-]{20,}/[REDACTED]/g;
        s/[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}/[CARD]/g;
        s/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/[EMAIL]/g;
        s/(password|secret|token|key|api_key|apikey)[=: ]+[^ ]+/\1=[REDACTED]/gi;
        s/Bearer [^ ]+/Bearer [REDACTED]/g;
    '
}
CONCLUSION_SCRUBBED=$(_scrub_sensitive "${CONCLUSION:-}")


# ─── Close path: formally abandon a deferred item (DEFERRED → ABANDONED) ───
if $CLOSE; then
    [[ -z "$ACTION_ID" ]] && { echo "--close requires action_id" >&2; exit 1; }

    current_status=$(jq -r --arg id "$ACTION_ID" \
        '.actions[] | select(.id == $id) | .status' "$GATE_FILE")
    if [[ "$current_status" != "DEFERRED" ]]; then
        echo "[GATE] --close only valid for DEFERRED actions (current: $current_status)" >&2
        exit 1
    fi

    REASON_SCRUBBED=$(_scrub_sensitive "${CLOSE_REASON:-abandoned during backlog cleanup}")

    jq --arg id "$ACTION_ID" --arg ts "$NOW_ISO" --arg reason "$REASON_SCRUBBED" \
        '(.actions[] | select(.id == $id and .status == "DEFERRED")) |=
        (.status = "ABANDONED" | .closed_at = $ts | .close_reason = $reason) |
        .deferred_count = ([.actions[] | select(.status == "DEFERRED")] | length)' \
        "$GATE_FILE" > "$GATE_FILE.tmp.$$" && mv "$GATE_FILE.tmp.$$" "$GATE_FILE"

    echo "[GATE] Closed: $ACTION_ID \u2192 ABANDONED ($REASON_SCRUBBED)"
    exit 0
fi

# ─── Defer path ───
if $DEFER; then
    [[ -z "$ACTION_ID" ]] && { echo "--defer requires action_id" >&2; exit 1; }

    # Check if action is non-deferrable (starvation guard)
    # Note: jq `// true` treats false as falsey, so use if/then/else
    is_deferrable=$(jq -r --arg id "$ACTION_ID" \
        '.actions[] | select(.id == $id) | if has("deferrable") then .deferrable else true end' "$GATE_FILE")
    if [[ "$is_deferrable" == "false" ]]; then
        echo "[GATE] BLOCKED: action $ACTION_ID is non-deferrable (starvation guard)" >&2
        exit 1
    fi

    jq --arg id "$ACTION_ID" --arg ts "$NOW_ISO" --arg reason "${DEFER_REASON:-no reason}" --arg conclusion "$CONCLUSION_SCRUBBED" \
        '(.actions[] | select(.id == $id and .status == "PENDING")) |=
        (.status = "DEFERRED" | .resolved_at = $ts | .defer_reason = $reason | .partial_conclusion = (if $conclusion == "" then null else $conclusion end)) |
        .pending_count = ([.actions[] | select(.status == "PENDING")] | length) |
        .deferred_count = ([.actions[] | select(.status == "DEFERRED")] | length) |
        .gate_status = (if .pending_count > 0 then "BLOCKED" else "CLEAR" end)' \
        "$GATE_FILE" > "$GATE_FILE.tmp.$$" && mv "$GATE_FILE.tmp.$$" "$GATE_FILE"

    echo "[GATE] Deferred: $ACTION_ID (reason: ${DEFER_REASON:-none})"
    exit 0
fi

# ─── Resolve by need (find first pending for this need) ───
if [[ -z "$ACTION_ID" && -n "$NEED" ]]; then
    ACTION_ID=$(jq -r --arg n "$NEED" \
        '[.actions[] | select(.need == $n and .status == "PENDING")][0].id // empty' \
        "$GATE_FILE")
    [[ -z "$ACTION_ID" ]] && { echo "No pending actions for need: $NEED" >&2; exit 0; }
fi

[[ -z "$ACTION_ID" ]] && { echo "Need action_id or --need" >&2; exit 1; }

# ─── Verify evidence ───
evidence_type=$(jq -r --arg id "$ACTION_ID" '.actions[] | select(.id == $id) | .evidence_type' "$GATE_FILE")
need=$(jq -r --arg id "$ACTION_ID" '.actions[] | select(.id == $id) | .need' "$GATE_FILE")
action_ts=$(jq -r --arg id "$ACTION_ID" '.actions[] | select(.id == $id) | .timestamp' "$GATE_FILE")

# Validate action exists
if [[ -z "$evidence_type" || -z "$need" ]]; then
    echo "Action not found: $ACTION_ID" >&2
    exit 1
fi

verification_result="unverified"

case "$evidence_type" in
    mark_satisfied)
        # Check audit.log for mark-satisfied call since action was proposed
        # audit.log is JSON lines — compare ISO timestamps lexicographically
        if [[ -f "$AUDIT_LOG" ]]; then
            recent_mark=$(awk -v since="$action_ts" -v need="$need" '
                { if (match($0, /"timestamp":"([^"]+)"/, ts) && ts[1] >= since) {
                    if (match($0, /"need":"([^"]+)"/, nd) && nd[1] == need) {
                        found=1
                    }
                }}
                END { print found+0 }
            ' "$AUDIT_LOG" 2>/dev/null)

            if (( recent_mark > 0 )); then
                verification_result="verified: mark-satisfied found in audit.log"
            else
                verification_result="UNVERIFIED: no mark-satisfied call found for $need since $action_ts"
            fi
        fi
        ;;

    file_created|file_modified)
        hint=$(jq -r --arg id "$ACTION_ID" '.actions[] | select(.id == $id) | .evidence_hint // ""' "$GATE_FILE")
        if [[ -n "$hint" && -n "${WORKSPACE:-}" ]]; then
            found=$(find -P "$WORKSPACE" -path "*${hint}*" -newer "$GATE_FILE" 2>/dev/null | head -1)
            if [[ -n "$found" ]]; then
                verification_result="verified: $found modified"
            else
                verification_result="UNVERIFIED: no matching file changes for pattern '$hint'"
            fi
        fi
        ;;

    self_report)
        if $SELF_REPORT || [[ -n "$EVIDENCE" ]]; then
            verification_result="self-reported: ${EVIDENCE:-no details}"
        else
            verification_result="UNVERIFIED: self_report type requires --self-report or --evidence"
        fi
        ;;
esac

# Allow completion when explicit evidence is provided even if auto-check failed
if [[ "$verification_result" == UNVERIFIED* && -n "$EVIDENCE" ]]; then
    verification_result="agent-provided: $EVIDENCE"
fi

# ─── Deliberation level classification + logging ───
# Read action_mode and proposed_at from gate file
action_mode=$(jq -r --arg id "$ACTION_ID" \
    '.actions[] | select(.id == $id) | .action_mode // "operative"' "$GATE_FILE" 2>/dev/null || echo "operative")
proposed_at=$(jq -r --arg id "$ACTION_ID" \
    '.actions[] | select(.id == $id) | .timestamp // ""' "$GATE_FILE" 2>/dev/null || echo "")

# Classify deliberation level (uses classify_deliberation_level from mindstate-utils.sh)
delib_level=$(classify_deliberation_level "${CONCLUSION:-}" "${ROUTE:-}" "$action_mode" "$proposed_at")

# Record to deliberation.log
if [[ "$action_mode" == "deliberative" ]]; then
    DELIB_LOG="$(_ms_assets)/deliberation.log"
    jq -cn --arg ts "$NOW_ISO" --arg aid "$ACTION_ID" --arg need "$need" \
        --arg level "$delib_level" --argjson clen "${#CONCLUSION}" \
        --arg route "${ROUTE:-}" \
        '{timestamp: $ts, event: "resolved", action_id: $aid, need: $need,
          level: $level, conclusion_length: $clen,
          route: (if $route == "" then null else $route end)}' \
        >> "$DELIB_LOG" 2>/dev/null || true
fi

# Scrub conclusion if provided
if [[ -n "$CONCLUSION" ]]; then
    verification_result="${verification_result} | conclusion: ${CONCLUSION_SCRUBBED}"
fi

# Append deliberation level to verification_result for audit visibility
if [[ "$action_mode" == "deliberative" ]]; then
    verification_result="${verification_result} | deliberation: ${delib_level}"
fi

# User-facing feedback, scaled by level (warn never block)
case "$delib_level" in
    absent)
        echo "⚠️  Deliberative action resolved without conclusion — marked as 'absent'."
        echo "   Pattern visible at next boot. Consider: deliberate.sh --template next time."
        ;;
    minimal)
        echo "ℹ️  Minimal deliberation recorded (short conclusion or no route)."
        ;;
    substantive|deep|n/a)
        # No noise for good path
        ;;
esac

# ─── Update status ───
final_status="COMPLETED"
if [[ "$verification_result" == UNVERIFIED* ]]; then
    final_status="FAILED"
fi

jq --arg id "$ACTION_ID" --arg ts "$NOW_ISO" --arg res "$verification_result" --arg st "$final_status" \
    '(.actions[] | select(.id == $id and .status == "PENDING")) |=
    (.status = $st | .resolved_at = $ts | .resolution = $res) |
    .pending_count = ([.actions[] | select(.status == "PENDING")] | length) |
    .completed_count = ([.actions[] | select(.status == "COMPLETED")] | length) |
    .gate_status = (if .pending_count > 0 then "BLOCKED" else "CLEAR" end)' \
    "$GATE_FILE" > "$GATE_FILE.tmp.$$" && mv "$GATE_FILE.tmp.$$" "$GATE_FILE"

echo "[GATE] Resolved: $ACTION_ID → $final_status ($verification_result)"
