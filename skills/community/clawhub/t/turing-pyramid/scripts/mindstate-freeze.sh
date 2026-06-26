#!/bin/bash
# mindstate-freeze.sh — Continuity Layer: Cognition snapshot
# Called at end of substantive sessions.
# Extracts cognition + forecast from observable artifacts. No self-report.
# Writes ## cognition + ## forecast. Does NOT touch ## reality.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$SCRIPT_DIR/mindstate-utils.sh"

mindstate_validate_workspace || exit 1

MINDSTATE_FILE=$(mindstate_file)
STATE_FILE=$(mindstate_state_file)
CONFIG_FILE=$(mindstate_config_file)
AUDIT_LOG=$(mindstate_audit_log)
LOCK_FILE=$(mindstate_lock_file)

SESSION_START_EPOCH="${1:?Usage: mindstate-freeze.sh <session_start_epoch>}"

NOW_EPOCH=$(now_epoch)
NOW_ISO=$(now_iso)

# ─── Trap: cleanup on unexpected termination ───
_freeze_cleanup() {
    rm -f "$MINDSTATE_FILE.tmp.$$" 2>/dev/null
}
trap _freeze_cleanup EXIT SIGTERM SIGINT SIGHUP

# ─── Substantive check ───
if ! is_session_substantive "$SESSION_START_EPOCH"; then
    echo "[MINDSTATE] Session not substantive — preserving previous cognition"
    exit 0
fi

# ─── Lock: blocking (freeze always completes) ───
exec 202>"$LOCK_FILE"
flock 202

# ═══════════════════════════════════════
# COGNITION EXTRACTION (all mechanical)
# ═══════════════════════════════════════

SINCE_ISO=$(date -u -d "@$SESSION_START_EPOCH" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || echo "1970-01-01T00:00:00Z")

# ─── 1. Trajectory: primary area of activity this session ───
trajectory=""

if [[ -f "$AUDIT_LOG" ]]; then
    # Get actions from this session
    session_actions=$(awk -v since="$SINCE_ISO" '
        {
            if (match($0, /"timestamp":"([^"]+)"/, ts)) {
                if (ts[1] >= since) {
                    if (match($0, /"need":"([^"]+)"/, nd)) {
                        print nd[1]
                    }
                }
            }
        }
    ' "$AUDIT_LOG" 2>/dev/null)
    
    if [[ -n "$session_actions" ]]; then
        # Most frequent need = primary trajectory
        primary_need=$(echo "$session_actions" | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')
        
        # Get the last action reason for that need
        last_reason=$(awk -v since="$SINCE_ISO" -v need="$primary_need" '
            {
                if (match($0, /"timestamp":"([^"]+)"/, ts) && ts[1] >= since) {
                    if (match($0, /"need":"([^"]+)"/, nd) && nd[1] == need) {
                        if (match($0, /"reason":"([^"]*)"/, rn)) {
                            reason = rn[1]
                        }
                    }
                }
            }
            END { if (reason) print reason }
        ' "$AUDIT_LOG" 2>/dev/null)
        
        trajectory="$primary_need — ${last_reason:-active}"
    fi
fi

# Fallback: check which directories had file modifications
if [[ -z "$trajectory" ]]; then
    modified_dir=$(find -P "$WORKSPACE" -maxdepth 2 -name "*.md" \
        -newermt "@$SESSION_START_EPOCH" 2>/dev/null \
        | xargs -I{} dirname {} 2>/dev/null | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')
    if [[ -n "$modified_dir" ]]; then
        trajectory="filesystem activity in $(basename "$modified_dir")"
    else
        trajectory="(minimal activity)"
    fi
fi

# ─── 2. Open threads: active incomplete items (max 3) ───
open_threads=()

# PRIORITY 1: Pending actions from execution gate (these block everything else)
GATE_FILE="$(_ms_assets)/pending_actions.json"
if [[ -f "$GATE_FILE" ]]; then
    while IFS= read -r pending_line; do
        [[ -z "$pending_line" ]] && continue
        open_threads+=("[PENDING GATE] $pending_line")
        (( ${#open_threads[@]} >= 3 )) && break
    done < <(jq -r '.actions[]? | select(.status == "PENDING") | "\(.need): \(.action_name)"' "$GATE_FILE" 2>/dev/null)
fi

# PRIORITY 2: From INTENTIONS.md: items under Active section
if (( ${#open_threads[@]} < 3 )) && [[ -f "$WORKSPACE/INTENTIONS.md" ]]; then
    in_active=false
    while IFS= read -r line; do
        # Detect Active section
        if [[ "$line" =~ ^##.*[Aa]ctive ]]; then
            in_active=true
            continue
        fi
        # Stop at next section
        if [[ "$line" =~ ^## ]] && $in_active; then
            break
        fi
        # Collect items (- [ ] or - [/] or just - item)
        if $in_active && [[ "$line" =~ ^[[:space:]]*-[[:space:]] ]]; then
            clean=$(echo "$line" | sed 's/^[[:space:]]*- *\(\[.\] *\)\?//')
            if [[ -n "$clean" ]]; then
                open_threads+=("$clean")
            fi
            if (( ${#open_threads[@]} >= 3 )); then break; fi
        fi
    done < "$WORKSPACE/INTENTIONS.md"
fi

# PRIORITY 3: Followups if we still have fewer than 3
if (( ${#open_threads[@]} < 3 )); then
    followups_file="$SKILL_DIR/assets/followups.jsonl"
    if [[ -f "$followups_file" ]]; then
        next_followup=$(jq -rs 'sort_by(.due_at) | .[0] | .what // empty' "$followups_file" 2>/dev/null)
        if [[ -n "$next_followup" ]]; then
            open_threads+=("followup: $next_followup")
        fi
    fi
fi

# ─── 3. Momentum: repeated activity pattern ───
momentum="mixed activity"

if [[ -f "$AUDIT_LOG" ]]; then
    recent_pattern=$(tail -10 "$AUDIT_LOG" | awk '
        { if (match($0, /"need":"([^"]+)"/, nd)) print nd[1] }
    ' 2>/dev/null | sort | uniq -c | sort -rn | head -1)
    
    if [[ -n "$recent_pattern" ]]; then
        momentum_count=$(echo "$recent_pattern" | awk '{print $1}')
        momentum_need=$(echo "$recent_pattern" | awk '{print $2}')
        if (( momentum_count >= 3 )); then
            momentum="$momentum_need ($momentum_count recent actions)"
        fi
    fi
fi

# ─── 4. Cognitive temperature: from session metrics ───
session_duration=$((NOW_EPOCH - SESSION_START_EPOCH))

# Count actions in this session
session_action_count=0
unique_needs=""
if [[ -f "$AUDIT_LOG" ]]; then
    session_action_count=$(awk -v since="$SINCE_ISO" '
        { if (match($0, /"timestamp":"([^"]+)"/, ts) && ts[1] >= since) count++ }
        END { print count+0 }
    ' "$AUDIT_LOG" 2>/dev/null)
    
    unique_needs=$(awk -v since="$SINCE_ISO" '
        { 
            if (match($0, /"timestamp":"([^"]+)"/, ts) && ts[1] >= since) {
                if (match($0, /"need":"([^"]+)"/, nd)) print nd[1]
            }
        }
    ' "$AUDIT_LOG" 2>/dev/null | sort -u | wc -l)
fi

cognitive_temperature="neutral"
if (( session_duration > 3600 && session_action_count > 3 )); then
    if (( unique_needs <= 2 )); then
        cognitive_temperature="building"
    else
        cognitive_temperature="exploring"
    fi
elif (( session_action_count > 5 )); then
    cognitive_temperature="intensive"
elif (( session_duration > 1800 && session_action_count <= 1 )); then
    cognitive_temperature="contemplation"
elif (( session_duration < 300 )); then
    cognitive_temperature="brief"
fi

# ═══════════════════════════════════════
# FORECAST GENERATION (mechanical)
# ═══════════════════════════════════════

structural_predictions=()

# Decay projections: which needs will hit crisis within 12h?
needs_list=$(get_needs_list)
for need in $needs_list; do
    sat=$(compute_current_satisfaction "$need")
    if (( $(echo "$sat > 1.0" | bc -l) )); then
        decay_rate=$(jq -r --arg n "$need" '.needs[$n].decay_rate_hours // 24' "$CONFIG_FILE")
        decay_mult=$(get_decay_multiplier)
        hours_to_crisis=$(echo "scale=1; ($sat - 1.0) * $decay_rate / $decay_mult" | bc -l)
        if (( $(echo "$hours_to_crisis < 12" | bc -l) )); then
            structural_predictions+=("$need < 1.0 within ${hours_to_crisis}h")
        fi
    fi
done

# Surplus projection
for need in $needs_list; do
    surplus=$(jq -r --arg n "$need" '.[$n].surplus // 0' "$STATE_FILE")
    has_spont=$(jq -r --arg n "$need" '.needs[$n].spontaneous // null' "$CONFIG_FILE" 2>/dev/null)
    if [[ "$has_spont" != "null" ]]; then
        threshold=$(jq -r --arg n "$need" '.needs[$n].spontaneous.threshold // 999' "$CONFIG_FILE" 2>/dev/null)
        if [[ "$threshold" != "999" ]] && (( $(echo "$surplus > $threshold * 0.7" | bc -l) )); then
            structural_predictions+=("$need surplus approaching threshold")
        fi
    fi
done

# Upcoming followups
followups_file="$SKILL_DIR/assets/followups.jsonl"
if [[ -f "$followups_file" ]]; then
    cutoff=$(date -u -d '+24 hours' +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null)
    if [[ -n "$cutoff" ]]; then
        upcoming=$(jq -rs --arg c "$cutoff" '[.[] | select(.due_at < $c)] | length' "$followups_file" 2>/dev/null || echo 0)
        if (( upcoming > 0 )); then
            structural_predictions+=("$upcoming followup(s) due within 24h")
        fi
    fi
fi

# ═══════════════════════════════════════
# WRITE COGNITION + FORECAST
# ═══════════════════════════════════════

# Build open_threads lines
OT_LINES=""
if (( ${#open_threads[@]} > 0 )); then
    for t in "${open_threads[@]}"; do
        OT_LINES+="  - $t"$'\n'
    done
else
    OT_LINES="  - (none detected)"$'\n'
fi

# Build structural prediction lines
SP_LINES=""
if (( ${#structural_predictions[@]} > 0 )); then
    for p in "${structural_predictions[@]}"; do
        SP_LINES+="  - $p"$'\n'
    done
else
    SP_LINES="  - (no near-term predictions)"$'\n'
fi

# ─── Extract deliberation residuals ───
# Scan recent audit conclusions for action language (implicit next steps)
DELIB_RESIDUALS=()
AUDIT_LOG="$(_ms_assets)/audit.log"
if [[ -f "$AUDIT_LOG" && -n "${SESSION_START:-}" ]]; then
    while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        ts=$(echo "$line" | grep -oP '"timestamp":"[^"]*"' | cut -d'"' -f4)
        [[ -z "$ts" ]] && continue
        ts_epoch=$(iso_to_epoch "$ts" 2>/dev/null || echo 0)
        (( ts_epoch < ${SESSION_START:-0} )) && continue

        conclusion=$(echo "$line" | grep -oP '"conclusion":"[^"]*"' | cut -d'"' -f4)
        [[ -z "$conclusion" || "$conclusion" == "null" ]] && continue

        if echo "$conclusion" | grep -qiE '(should|need to|update|revisit|demote|create|check|consider|fix|might want)'; then
            audit_need=$(echo "$line" | grep -oP '"need":"[^"]*"' | cut -d'"' -f4)
            DELIB_RESIDUALS+=("[$audit_need] $conclusion")
        fi
        (( ${#DELIB_RESIDUALS[@]} >= 5 )) && break
    done < <(tac "$AUDIT_LOG")
fi

DR_LINES=""
if (( ${#DELIB_RESIDUALS[@]} > 0 )); then
    for r in "${DELIB_RESIDUALS[@]}"; do
        DR_LINES+="  - $r"$'\n'
    done
fi

# ─── Deliberation discipline summary ───
delib_summary="no recent deliberations"
DELIB_LOG="$(_ms_assets)/deliberation.log"
if [[ -f "$DELIB_LOG" ]]; then
    recent=$(tail -50 "$DELIB_LOG" | grep '"event":"resolved"' | tail -10)
    if [[ -n "$recent" ]]; then
        _d_substantive=$(echo "$recent" | grep -c '"level":"substantive"' || echo 0)
        _d_deep=$(echo "$recent" | grep -c '"level":"deep"' || echo 0)
        _d_minimal=$(echo "$recent" | grep -c '"level":"minimal"' || echo 0)
        _d_absent=$(echo "$recent" | grep -c '"level":"absent"' || echo 0)
        delib_summary="$((_d_substantive + _d_deep)) substantive, $_d_minimal minimal, $_d_absent skipped (last 10)"
    fi
fi

COGNITION_BLOCK="## cognition
# [frozen by mindstate-freeze.sh — READ-ONLY until next freeze]
frozen_at: $NOW_ISO
trajectory: $trajectory
open_threads:
${OT_LINES}deliberation_residuals:
${DR_LINES:-  - (none)
}deliberation_discipline: $delib_summary
momentum: $momentum
cognitive_temperature: $cognitive_temperature"

FORECAST_BLOCK="## forecast
# [frozen with cognition — consumed by mindstate-boot.sh]
structural:
${SP_LINES}semantic:
  - (mechanical only)"

# ─── Atomic write: preserve reality, replace cognition+forecast ───
TMP_FILE="$MINDSTATE_FILE.tmp.$$"

# Extract reality section (everything before ## cognition)
if [[ -f "$MINDSTATE_FILE" ]]; then
    REALITY_SECTION=$(sed -n '1,/^## cognition/{/^## cognition/!p}' "$MINDSTATE_FILE")
else
    REALITY_SECTION="# MINDSTATE
# Auto-managed by continuity layer. Do not edit manually.

## reality
# [daemon has not run yet]
timestamp: $NOW_ISO"
fi

cat > "$TMP_FILE" <<EOF
$REALITY_SECTION

$COGNITION_BLOCK

$FORECAST_BLOCK
EOF

mv "$TMP_FILE" "$MINDSTATE_FILE"

echo "[MINDSTATE] Cognition frozen at $NOW_ISO"
echo "  trajectory: $trajectory"
echo "  temperature: $cognitive_temperature"
echo "  open_threads: ${#open_threads[@]}"
echo "  predictions: ${#structural_predictions[@]} structural"
