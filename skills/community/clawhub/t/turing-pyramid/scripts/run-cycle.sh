#!/bin/bash
# Turing Pyramid — Main Cycle Runner
# WORKSPACE is REQUIRED - no silent fallback
if [[ -z "$WORKSPACE" ]]; then
    echo "❌ ERROR: WORKSPACE environment variable not set" >&2
    echo "   Set it explicitly: export WORKSPACE=/path/to/workspace" >&2
    exit 1
fi

# Called on each heartbeat to evaluate and act on needs

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$SKILL_DIR/assets/needs-config.json"
STATE_FILE="$SKILL_DIR/assets/needs-state.json"
TEMPLATE_FILE="$SKILL_DIR/assets/needs-state.template.json"
SCRIPTS_DIR="$SKILL_DIR/scripts"

require_command() {
    local cmd="$1"
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "❌ ERROR: required command not found: $cmd" >&2
        exit 1
    fi
}

initialize_state_if_missing() {
    if [[ -f "$STATE_FILE" ]]; then
        return 0
    fi
    if [[ ! -f "$TEMPLATE_FILE" ]]; then
        echo "❌ ERROR: state file missing and template not found: $TEMPLATE_FILE" >&2
        exit 1
    fi

    local now
    now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    mkdir -p "$(dirname "$STATE_FILE")"
    jq --arg now "$now" '
      ._meta.initialized = $now |
      ._meta.last_cycle = $now |
      to_entries
      | map(
          if .key == "_meta" then .
          elif (.value | type) == "object" then
            .value.satisfaction = (.value.satisfaction // 3.0) |
            .value.last_satisfied = (.value.last_satisfied // $now) |
            .value.last_decay_check = (.value.last_decay_check // $now) |
            .value.surplus = (.value.surplus // 0) |
            .value.last_surplus_check = (.value.last_surplus_check // $now) |
            .value.last_high_action_at = (.value.last_high_action_at // $now) |
            .value.last_spontaneous_at = (.value.last_spontaneous_at // $now) |
            .
          else . end
        )
      | from_entries
    ' "$TEMPLATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    echo "ℹ️  Initialized missing state from template: $STATE_FILE" >&2
}

require_command jq
require_command bc
require_command flock
initialize_state_if_missing

# Turing-exp formula: tension = dep² + importance × max(0, dep - crisis_threshold)²
# At homeostasis (dep < threshold): all needs equal (dep² only)
# In crisis (dep > threshold): importance amplifies — hierarchy emerges
MAX_IMPORTANCE=$(jq '[.needs[].importance] | max' "$CONFIG_FILE")
CRISIS_THRESHOLD=$(jq -r '.settings.tension_formula.crisis_threshold // 1.0' "$CONFIG_FILE")
# MAX_TENSION = 3² + max_imp × (3 - threshold)² [dep=3 worst case]
MAX_CRISIS_EXCESS=$(echo "scale=2; 3 - $CRISIS_THRESHOLD" | bc -l)
MAX_TENSION=$(echo "scale=1; 9 + ($MAX_IMPORTANCE * $MAX_CRISIS_EXCESS * $MAX_CRISIS_EXCESS)" | bc -l)
source "$SCRIPTS_DIR/spontaneity.sh"
WORKSPACE="$WORKSPACE"
MEMORY_DIR="$WORKSPACE/memory"
LOGS_DIR="$WORKSPACE/memory/logs"

# State is initialized before calculations so fresh installs can run safely.

# Acquire exclusive lock — skip if another cycle is already running
LOCK_FILE="$SKILL_DIR/assets/cycle.lock"
exec 200>"$LOCK_FILE"
if ! flock -n 200; then
    echo "⏳ Another cycle is already running — skipping this one." >&2
    exit 0
fi

NOW=$(date +%s)
NOW_ISO=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TODAY=$(date +%Y-%m-%d)

# Bootstrap mode: process ALL needs (also skips gate — clean slate)
if [[ "${1:-}" == "--bootstrap" ]]; then
    MAX_ACTIONS=10
    SKIP_GATE=true
    echo "🚀 BOOTSTRAP MODE — processing all needs"
else
    MAX_ACTIONS=$(jq -r '.settings.max_actions_per_cycle // 3' "$CONFIG_FILE")
fi

# ─── Execution Gate: block new proposals if pending actions exist ───
if [[ "${SKIP_GATE:-}" != "true" ]]; then
    GATE_CHECK="$SCRIPTS_DIR/gate-check.sh"
    if [[ -x "$GATE_CHECK" ]]; then
        if ! bash "$GATE_CHECK" 2>&1; then
            echo ""
            bash "$SCRIPTS_DIR/gate-status.sh" 2>/dev/null || true
            echo ""
            echo "Resolve: gate-resolve.sh --need <need> --evidence \"what you did\""
            echo "Or defer: gate-resolve.sh --defer <id> --reason \"why\""
            exit 0
        fi
    fi
fi

# No-scans mode for testing (env or arg)
SKIP_SCANS="${SKIP_SCANS:-false}"
if [[ "${1:-}" == "--no-scans" || "${2:-}" == "--no-scans" ]]; then
    SKIP_SCANS=true
fi
if [[ "$SKIP_SCANS" == "true" ]]; then
    echo "⚠️  TEST MODE — skipping event scans"
fi

# Calculate tension for all needs
declare -A TENSIONS
declare -A SATISFACTIONS
declare -A DEPRIVATIONS

calculate_tensions() {
    local needs=$(jq -r '.needs | keys[]' "$CONFIG_FILE")
    
    for need in $needs; do
        local importance=$(jq -r ".needs.\"$need\".importance" "$CONFIG_FILE")
        local decay_rate=$(jq -r ".needs.\"$need\".decay_rate_hours" "$CONFIG_FILE")
        
        # Read current satisfaction from state (float, default 2.0)
        local current_sat=$(jq -r --arg n "$need" '.[$n].satisfaction // 2.0' "$STATE_FILE")
        
        # Read last decay check time (when we last applied decay)
        local last_decay=$(jq -r --arg n "$need" '.[$n].last_decay_check // "1970-01-01T00:00:00Z"' "$STATE_FILE")
        local last_decay_epoch=$(date -d "$last_decay" +%s 2>/dev/null || echo 0)
        
        # Calculate hours since last decay check
        local hours_since_decay=$(echo "scale=4; ($NOW - $last_decay_epoch) / 3600" | bc -l)
        
        # Calculate decay delta: lose 1 satisfaction per decay_rate hours
        # Apply day/night multiplier if enabled
        local decay_multiplier=$("$SCRIPTS_DIR/get-decay-multiplier.sh" 2>/dev/null || echo "1.0")
        local decay_delta=$(echo "scale=4; ($hours_since_decay / $decay_rate) * $decay_multiplier" | bc -l)
        
        # Apply decay to current satisfaction
        local decayed_sat=$(echo "scale=2; $current_sat - $decay_delta" | bc -l)
        
        # Clamp to 0-3 range
        if (( $(echo "$decayed_sat < 0" | bc -l) )); then
            decayed_sat="0.00"
        fi
        if (( $(echo "$decayed_sat > 3" | bc -l) )); then
            decayed_sat="3.00"
        fi
        
        # Run event scan if exists (can only worsen)
        local scan_script="$SCRIPTS_DIR/scan_${need}.sh"
        local event_satisfaction=""
        if [[ "$SKIP_SCANS" != "true" && -x "$scan_script" ]]; then
            event_satisfaction=$("$scan_script" 2>/dev/null)
        fi
        
        # Event scan can override (take worst)
        local satisfaction=$decayed_sat
        if [[ -n "$event_satisfaction" && "$event_satisfaction" =~ ^[0-3]$ ]]; then
            if (( $(echo "$event_satisfaction < $satisfaction" | bc -l) )); then
                satisfaction=$event_satisfaction
            fi
        fi
        
        # Float deprivation for smooth tension curves (v1.15.0)
        local deprivation=$(echo "scale=2; 3 - $satisfaction" | bc -l)
        # Clamp to 0-3
        if (( $(echo "$deprivation < 0" | bc -l) )); then deprivation="0.00"; fi
        if (( $(echo "$deprivation > 3" | bc -l) )); then deprivation="3.00"; fi
        # Turing-exp: tension = dep² + importance × max(0, dep - crisis_threshold)²
        # Below threshold: all needs compete equally (pure deprivation)
        # Above threshold: importance amplifies crisis signal (priority hierarchy emerges)
        local crisis_excess=$(echo "scale=4; $deprivation - $CRISIS_THRESHOLD" | bc -l)
        if (( $(echo "$crisis_excess < 0" | bc -l) )); then crisis_excess="0"; fi
        local tension=$(echo "scale=1; ($deprivation * $deprivation) + ($importance * $crisis_excess * $crisis_excess)" | bc -l)
        
        TENSIONS[$need]=$tension
        SATISFACTIONS[$need]=$satisfaction  # Keep float for display
        DEPRIVATIONS[$need]=$deprivation
        
        # Update state with decayed satisfaction and decay check time
        jq --arg need "$need" --argjson sat "$satisfaction" --arg now "$NOW_ISO" '
            .[$need].satisfaction = $sat |
            .[$need].last_decay_check = $now
        ' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    done
}

# Get top N needs by tension
get_top_needs() {
    local n=$1
    for need in "${!TENSIONS[@]}"; do
        echo "${TENSIONS[$need]} $need"
    done | sort -rn | head -n "$n" | awk '{print $2}'
}

# Probability-based action decision
# Returns 0 (true) if should take action, 1 (false) for non-action
# v1.13.0: 6-level action probability with tension bonus
roll_action() {
    local sat=$1
    local tension=$2
    
    # Round float satisfaction to nearest 0.5 for lookup
    # Formula: round(sat * 2) / 2
    local doubled=$(echo "$sat * 2" | bc -l)
    local rounded_int=$(printf "%.0f" "$doubled")
    local sat_rounded=$(echo "scale=1; $rounded_int / 2" | bc -l)
    # Normalize format (.5 → 0.5)
    [[ "$sat_rounded" == .* ]] && sat_rounded="0$sat_rounded"
    # Clamp to valid range [0.5, 3.0]
    if (( $(echo "$sat_rounded < 0.5" | bc -l) )); then sat_rounded="0.5"; fi
    if (( $(echo "$sat_rounded > 3.0" | bc -l) )); then sat_rounded="3.0"; fi
    
    # Base chance by satisfaction level — read from config
    local config_key="sat_$sat_rounded"
    local base_chance=$(jq -r ".action_probability.\"$config_key\" // 50" "$CONFIG_FILE")
    # Validate it's a number, fallback to 50
    [[ ! "$base_chance" =~ ^[0-9]+$ ]] && base_chance=50
    
    # sat=3.0 always skip (no action needed)
    if [[ "$base_chance" -eq 0 ]]; then
        return 1
    fi
    
    # Tension bonus: scales 0-50% based on tension
    # MAX_TENSION = max_importance × max_deprivation(3), calculated from config
    # This preserves importance weighting: higher importance = bigger bonus at same sat
    local max_bonus=50
    local bonus=$(echo "scale=0; ($tension * $max_bonus) / $MAX_TENSION" | bc -l)
    
    # Final chance (capped at 100)
    local final_chance=$((base_chance + bonus))
    [[ $final_chance -gt 100 ]] && final_chance=100
    
    local roll=$((RANDOM % 100))
    [[ $roll -lt $final_chance ]]
}

# Roll for impact range based on satisfaction
# Returns: "low|mid|high|skip [rolled_spend]"
# If spontaneity shifted the matrix, appends rolled_spend for later deduction
roll_impact_range() {
    local need=$1
    local sat=$2
    local roll=$((RANDOM % 100))
    
    # Round float satisfaction to nearest 0.5 for matrix lookup
    local doubled=$(echo "$sat * 2" | bc -l)
    local rounded_int=$(printf "%.0f" "$doubled")
    local sat_rounded=$(echo "scale=1; $rounded_int / 2" | bc -l)
    [[ "$sat_rounded" == .* ]] && sat_rounded="0$sat_rounded"
    if (( $(echo "$sat_rounded < 0.5" | bc -l) )); then sat_rounded="0.5"; fi
    if (( $(echo "$sat_rounded > 3.0" | bc -l) )); then sat_rounded="3.0"; fi
    
    # Get normal impact matrix probabilities
    local matrix_key="sat_$sat_rounded"
    local p_low p_mid p_high
    
    p_low=$(jq -r ".impact_matrix_default.\"$matrix_key\".low // 25" "$CONFIG_FILE")
    p_mid=$(jq -r ".impact_matrix_default.\"$matrix_key\".mid // 50" "$CONFIG_FILE")
    p_high=$(jq -r ".impact_matrix_default.\"$matrix_key\".high // 25" "$CONFIG_FILE")
    
    # If all zeros (sat=3.0), skip action
    if [[ $p_low -eq 0 && $p_mid -eq 0 && $p_high -eq 0 ]]; then
        echo "skip"
        return
    fi
    
    # --- Spontaneity: try to shift matrix ---
    local shift_result
    shift_result=$(get_shifted_matrix "$need" "$p_low" "$p_mid" "$p_high" "$STATE_FILE" "$CONFIG_FILE")
    
    local rolled_spend=0
    if [[ "$shift_result" != "none" ]]; then
        # Parse: "shifted_low shifted_mid shifted_high rolled_spend t"
        p_low=$(echo "$shift_result" | awk '{print $1}')
        p_mid=$(echo "$shift_result" | awk '{print $2}')
        p_high=$(echo "$shift_result" | awk '{print $3}')
        rolled_spend=$(echo "$shift_result" | awk '{print $4}')
        local t_val=$(echo "$shift_result" | awk '{print $5}')
        echo "  [SURPLUS] $need: surplus=$(jq -r --arg n "$need" '.[$n].surplus // 0' "$STATE_FILE"), rolled_spend=$rolled_spend, t=$t_val, matrix={low:$p_low, mid:$p_mid, high:$p_high}" >&2
    fi
    
    # Roll: 0-p_low = low, p_low-(p_low+p_mid) = mid, rest = high
    local impact_range
    if [[ $roll -lt $p_low ]]; then
        impact_range="low"
    elif [[ $roll -lt $((p_low + p_mid)) ]]; then
        impact_range="mid"
    else
        impact_range="high"
    fi
    
    # Spend surplus if spontaneity was active
    if [[ "$shift_result" != "none" ]]; then
        spend_surplus "$need" "$impact_range" "$rolled_spend" "$STATE_FILE" "$CONFIG_FILE"
    fi
    
    echo "$impact_range"
}

# ─── Action Dedup Guard ──────────────────────────────────────────────────────
# Check if an action was already executed recently (across sessions).
# Uses audit.log (written by mark-satisfied.sh) as source of truth.
# Args: $1=action_name, $2=cooldown_hours (default: 8)
# Returns: 0=OK (not recent), 1=duplicate (was done recently)
AUDIT_LOG="$SKILL_DIR/assets/audit.log"

action_was_recent() {
    local action_name="$1"
    local cooldown_hours="${2:-8}"

    if [[ ! -f "$AUDIT_LOG" ]]; then
        return 1  # no log = no duplicates
    fi

    local cutoff_epoch=$((NOW - cooldown_hours * 3600))

    # Search audit.log for this action's reason field within cooldown window
    # Audit format: {"timestamp":"...","need":"...","reason":"..."}
    while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        local ts=$(echo "$line" | jq -r '.timestamp // empty' 2>/dev/null)
        [[ -z "$ts" ]] && continue
        local ts_epoch=$(date -d "$ts" +%s 2>/dev/null || echo 0)
        [[ $ts_epoch -lt $cutoff_epoch ]] && continue
        local reason=$(echo "$line" | jq -r '.reason // empty' 2>/dev/null)
        [[ -z "$reason" ]] && continue
        # Match if the reason contains the action name (mark-satisfied logs the action as reason)
        if [[ "$reason" == *"$action_name"* ]]; then
            return 0  # found recent execution
        fi
    done < "$AUDIT_LOG"

    return 1  # not found
}

# Check action_history in state file (written by record_action_selection)
# More precise: checks if this exact action was SELECTED (not just satisfied)
# Args: $1=need, $2=action_name, $3=cooldown_hours (default: 8)
action_was_selected_recently() {
    local need="$1"
    local action_name="$2"
    local cooldown_hours="${3:-8}"
    local cutoff_epoch=$((NOW - cooldown_hours * 3600))

    local last_selected=$(jq -r --arg n "$need" --arg a "$action_name" \
        '.[$n].action_history[$a] // "1970-01-01T00:00:00Z"' "$STATE_FILE" 2>/dev/null)
    local last_epoch=$(date -d "$last_selected" +%s 2>/dev/null || echo 0)

    [[ $last_epoch -ge $cutoff_epoch ]]
}

# Select action with dedup: try weighted selection, if duplicate, try alternatives
# Args: $1=need, $2=range
# Returns: action name (empty if all depleted)
select_action_with_dedup() {
    local need="$1"
    local range="$2"
    local cooldown_hours=8  # configurable

    # Get all available actions for this range
    local actions_json
    case $range in
        low)  actions_json=$(jq -c "[.needs.\"$need\".actions[] | select(.disabled != true) | select(.impact < 1.0)]" "$CONFIG_FILE") ;;
        mid)  actions_json=$(jq -c "[.needs.\"$need\".actions[] | select(.disabled != true) | select(.impact >= 1.0 and .impact < 2.0)]" "$CONFIG_FILE") ;;
        high) actions_json=$(jq -c "[.needs.\"$need\".actions[] | select(.disabled != true) | select(.impact >= 2.0)]" "$CONFIG_FILE") ;;
    esac

    local count=$(echo "$actions_json" | jq 'length')
    [[ $count -eq 0 ]] && return

    # Try up to $count times to find a non-duplicate action
    local attempts=0
    local max_attempts=$count
    local tried=()

    while [[ $attempts -lt $max_attempts ]]; do
        local candidate=$(select_weighted_action "$need" "$range")
        [[ -z "$candidate" ]] && break

        # Check if we already tried this one
        local already_tried=false
        for t in "${tried[@]}"; do
            [[ "$t" == "$candidate" ]] && already_tried=true && break
        done
        if $already_tried; then
            ((attempts++))
            continue
        fi
        tried+=("$candidate")

        # Check dedup: was this action selected or executed recently?
        if action_was_selected_recently "$need" "$candidate" "$cooldown_hours"; then
            echo "  ↩ Skipping \"$candidate\" (selected ${cooldown_hours}h ago)" >&2
            ((attempts++))
            continue
        fi

        # Passed dedup check
        echo "$candidate"
        return
    done

    # All actions were recent — fall through to the first one with a warning
    if [[ ${#tried[@]} -gt 0 ]]; then
        echo "  ⚠️ All $range actions for $need were recent — repeating least-stale" >&2
        echo "${tried[0]}"
    fi
}

# Get actions filtered by impact range (low/mid/high)
get_actions_by_range() {
    local need=$1
    local range=$2
    
    case $range in
        low)  jq -r ".needs.\"$need\".actions[] | select(.disabled != true) | select(.impact < 1.0) | .name" "$CONFIG_FILE" ;;
        mid)  jq -r ".needs.\"$need\".actions[] | select(.disabled != true) | select(.impact >= 1.0 and .impact < 2.0) | .name" "$CONFIG_FILE" ;;
        high) jq -r ".needs.\"$need\".actions[] | select(.disabled != true) | select(.impact >= 2.0) | .name" "$CONFIG_FILE" ;;
    esac
}

# Get effective weight for an action (applies staleness penalty if recently used)
get_effective_weight() {
    local need=$1
    local action_name=$2
    local base_weight=$3

    local staleness_enabled=$(jq -r '.settings.action_staleness.enabled // false' "$CONFIG_FILE")
    if [[ "$staleness_enabled" != "true" ]]; then
        echo "$base_weight"
        return
    fi

    local window_hours=$(jq -r '.settings.action_staleness.window_hours // 24' "$CONFIG_FILE")
    local penalty=$(jq -r '.settings.action_staleness.penalty // 0.2' "$CONFIG_FILE")
    local min_weight=$(jq -r '.settings.action_staleness.min_weight // 5' "$CONFIG_FILE")
    local window_seconds=$(echo "$window_hours * 3600" | bc -l | cut -d. -f1)

    # Check last time this action was selected
    local last_selected=$(jq -r --arg n "$need" --arg a "$action_name" \
        '.[$n].action_history[$a] // "1970-01-01T00:00:00Z"' "$STATE_FILE")
    local last_epoch=$(date -d "$last_selected" +%s 2>/dev/null || echo 0)
    local seconds_since=$((NOW - last_epoch))

    if [[ $seconds_since -lt $window_seconds ]]; then
        # Within staleness window — apply penalty
        local penalized=$(echo "scale=0; $base_weight * $penalty / 1" | bc -l)
        # Enforce minimum weight (never fully zero out)
        if [[ $penalized -lt $min_weight ]]; then
            penalized=$min_weight
        fi
        echo "$penalized"
    else
        echo "$base_weight"
    fi
}

# Record selected action in state file (with cleanup of expired entries)
record_action_selection() {
    local need=$1
    local action_name=$2

    local window_hours=$(jq -r '.settings.action_staleness.window_hours // 24' "$CONFIG_FILE")
    local cutoff_epoch=$((NOW - window_hours * 3600))
    local cutoff_iso=$(date -u -d "@$cutoff_epoch" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%SZ")

    jq --arg n "$need" --arg a "$action_name" --arg now "$NOW_ISO" --arg cutoff "$cutoff_iso" '
        .[$n].action_history //= {} |
        .[$n].action_history[$a] = $now |
        .[$n].action_history = (.[$n].action_history | to_entries | map(select(.value >= $cutoff)) | from_entries)
    ' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
}

# Weighted random selection of action by impact range (with staleness)
select_weighted_action() {
    local need=$1
    local range=$2
    
    # Get actions with weights for this impact range
    local actions_json
    case $range in
        low)  actions_json=$(jq -c "[.needs.\"$need\".actions[] | select(.disabled != true) | select(.impact < 1.0)]" "$CONFIG_FILE") ;;
        mid)  actions_json=$(jq -c "[.needs.\"$need\".actions[] | select(.disabled != true) | select(.impact >= 1.0 and .impact < 2.0)]" "$CONFIG_FILE") ;;
        high) actions_json=$(jq -c "[.needs.\"$need\".actions[] | select(.disabled != true) | select(.impact >= 2.0)]" "$CONFIG_FILE") ;;
    esac
    
    local count=$(echo "$actions_json" | jq 'length')
    
    if [[ $count -eq 0 ]]; then
        echo ""
        return
    fi
    
    if [[ $count -eq 1 ]]; then
        echo "$actions_json" | jq -r '.[0].name'
        return
    fi
    
    # Build effective weights (applying staleness penalties)
    local effective_weights=()
    local names=()
    local total_weight=0
    
    for i in $(seq 0 $((count - 1))); do
        local base_weight=$(echo "$actions_json" | jq -r ".[$i].weight // 100")
        local name=$(echo "$actions_json" | jq -r ".[$i].name")
        local eff_weight=$(get_effective_weight "$need" "$name" "$base_weight")
        
        effective_weights+=("$eff_weight")
        names+=("$name")
        total_weight=$((total_weight + eff_weight))
    done
    
    if [[ $total_weight -le 0 ]]; then
        # Shouldn't happen with min_weight, but safety
        echo "${names[0]}"
        return
    fi
    
    local roll=$((RANDOM % total_weight))
    
    # Select based on cumulative effective weights
    local cumulative=0
    local selected=""
    
    for i in $(seq 0 $((count - 1))); do
        cumulative=$((cumulative + ${effective_weights[$i]}))
        
        if [[ $roll -lt $cumulative ]]; then
            selected="${names[$i]}"
            break
        fi
    done
    
    echo "$selected"
}

# Log non-action (noticed but deferred)
log_noticed() {
    local need=$1
    local sat=$2
    local tension=$3
    local timestamp=$(date +"%H:%M")
    
    # Append to today's memory with timestamp
    if [[ -d "$MEMORY_DIR" ]]; then
        echo "- [$timestamp] ○ noticed: $need (sat=$sat, tension=$tension) — non-action" >> "$LOGS_DIR/$TODAY-cycles.log"
    fi
}

# Log action taken
log_action() {
    local need=$1
    local sat=$2
    local tension=$3
    local timestamp=$(date +"%H:%M")
    
    # Append to today's memory with timestamp
    if [[ -d "$MEMORY_DIR" ]]; then
        echo "- [$timestamp] ▶ action: $need (sat=$sat, tension=$tension) — requires action" >> "$LOGS_DIR/$TODAY-cycles.log"
    fi
}

# Starvation guard: detect needs stuck at floor without action
# Returns space-separated list of starving need names (longest-starved first)
detect_starving_needs() {
    local sg_enabled=$(jq -r '.settings.starvation_guard.enabled // false' "$CONFIG_FILE")
    if [[ "$sg_enabled" != "true" ]]; then
        return
    fi

    local threshold_hours=$(jq -r '.settings.starvation_guard.threshold_hours // 48' "$CONFIG_FILE")
    local sat_threshold=$(jq -r '.settings.starvation_guard.sat_threshold // 0.5' "$CONFIG_FILE")
    local threshold_seconds=$(echo "$threshold_hours * 3600" | bc -l | cut -d. -f1)

    local needs=$(jq -r '.needs | keys[]' "$CONFIG_FILE")
    local starving=()

    for need in $needs; do
        # Skip disabled needs (importance=0)
        local importance=$(jq -r ".needs.\"$need\".importance // 1" "$CONFIG_FILE")
        if [[ "$importance" == "0" ]]; then
            continue
        fi

        local sat=$(jq -r --arg n "$need" '.[$n].satisfaction // 2.0' "$STATE_FILE")

        # Check if at or below threshold
        if (( $(echo "$sat > $sat_threshold" | bc -l) )); then
            continue
        fi

        # Check last_action_at — if missing, use epoch 0 (never acted)
        local last_action=$(jq -r --arg n "$need" '.[$n].last_action_at // "1970-01-01T00:00:00Z"' "$STATE_FILE")
        local last_action_epoch=$(date -d "$last_action" +%s 2>/dev/null || echo 0)
        local seconds_since=$((NOW - last_action_epoch))

        if [[ $seconds_since -ge $threshold_seconds ]]; then
            # Store as "seconds_since:need" for sorting
            starving+=("$seconds_since:$need")
        fi
    done

    # Sort by starvation duration (longest first) and output need names
    if [[ ${#starving[@]} -gt 0 ]]; then
        printf '%s\n' "${starving[@]}" | sort -t: -k1 -rn | cut -d: -f2
    fi
}

# ─── Follow-up System ────────────────────────────────────────────────────────
FOLLOWUPS_FILE="$SKILL_DIR/assets/followups.jsonl"
FOLLOWUP_MAX_DISPLAY=5
FOLLOWUP_TTL_SECONDS=604800  # 1 week
FOLLOWUP_FLOOD_THRESHOLD=10

check_followups() {
    if [[ ! -f "$FOLLOWUPS_FILE" ]]; then
        return
    fi
    
    local ripe_count=0
    local ripe_entries=""
    local steward_overdue=""
    
    # Collect ripe follow-ups (status=pending, check_at_epoch <= now)
    while IFS= read -r line; do
        local status=$(echo "$line" | jq -r '.status')
        [[ "$status" != "pending" ]] && continue
        
        local check_epoch=$(echo "$line" | jq -r '.check_at_epoch // 0')
        [[ "$check_epoch" -gt "$NOW" ]] && continue
        
        local age=$((NOW - check_epoch))
        local source=$(echo "$line" | jq -r '.source')
        local what=$(echo "$line" | jq -r '.what')
        local need=$(echo "$line" | jq -r '.need')
        local id=$(echo "$line" | jq -r '.id')
        local parent=$(echo "$line" | jq -r '.parent_action // ""')
        
        # TTL check
        if [[ $age -ge $FOLLOWUP_TTL_SECONDS ]]; then
            if [[ "$source" == "steward" ]]; then
                local days=$((age / 86400))
                steward_overdue="${steward_overdue}  🔴 OVERDUE (${days}d): [$need] $what (id: $id)\n"
                ((ripe_count++))
            else
                # Auto-expire self/auto follow-ups past TTL
                local tmp_file=$(mktemp)
                while IFS= read -r fline; do
                    local fid=$(echo "$fline" | jq -r '.id')
                    if [[ "$fid" == "$id" ]]; then
                        echo "$fline" | jq -c ".status = \"expired\" | .expired_at = \"$NOW_ISO\"" >> "$tmp_file"
                    else
                        echo "$fline" >> "$tmp_file"
                    fi
                done < "$FOLLOWUPS_FILE"
                mv "$tmp_file" "$FOLLOWUPS_FILE"
                echo "  ⏰ Auto-expired follow-up (>7d): $what" >> "$LOGS_DIR/$TODAY-cycles.log" 2>/dev/null
                continue
            fi
        else
            ripe_entries="${ripe_entries}${line}\n"
            ((ripe_count++))
        fi
    done < "$FOLLOWUPS_FILE"
    
    if [[ $ripe_count -eq 0 ]]; then
        return
    fi
    
    echo ""
    
    # Flood check
    if [[ $ripe_count -gt $FOLLOWUP_FLOOD_THRESHOLD ]]; then
        echo "⚠️  $ripe_count follow-ups overdue! Consider: resolve-followup.sh --bulk-expire"
        echo ""
    fi
    
    echo "📌 Follow-ups due ($ripe_count total, showing up to $FOLLOWUP_MAX_DISPLAY):"
    
    # Show steward overdue first (always)
    if [[ -n "$steward_overdue" ]]; then
        echo -e "$steward_overdue"
    fi
    
    # Show ripe entries (oldest first, limited)
    local shown=0
    echo -e "$ripe_entries" | while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        [[ $shown -ge $FOLLOWUP_MAX_DISPLAY ]] && break
        
        local what=$(echo "$line" | jq -r '.what')
        local need=$(echo "$line" | jq -r '.need')
        local id=$(echo "$line" | jq -r '.id')
        local parent=$(echo "$line" | jq -r '.parent_action // ""')
        local source=$(echo "$line" | jq -r '.source')
        local check_at=$(echo "$line" | jq -r '.check_at')
        local age_hours=$(( (NOW - $(echo "$line" | jq -r '.check_at_epoch // 0')) / 3600 ))
        
        local parent_str=""
        [[ -n "$parent" && "$parent" != "null" ]] && parent_str=" (from: $parent)"
        local source_str=""
        [[ "$source" == "steward" ]] && source_str=" [steward]"
        
        echo "  → [$need] $what${parent_str}${source_str}"
        echo "    Due: ${age_hours}h ago | resolve-followup.sh $id [--impact N]"
        
        # Apply satisfaction penalty for ripe follow-up (gentle nudge: -0.3)
        local current_sat=$(jq -r --arg n "$need" '.[$n].satisfaction // 2.0' "$STATE_FILE")
        local nudge_sat=$(echo "scale=2; $current_sat - 0.3" | bc -l)
        if (( $(echo "$nudge_sat < 0.5" | bc -l) )); then
            nudge_sat="0.50"
        fi
        jq --arg n "$need" --argjson sat "$nudge_sat" '.[$n].satisfaction = $sat' \
            "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
        
        ((shown++))
    done
    
    echo ""
}

# Cleanup done/expired follow-ups older than 7 days
cleanup_followups() {
    if [[ ! -f "$FOLLOWUPS_FILE" ]]; then
        return
    fi
    
    local cleanup_cutoff=$((NOW - 604800))
    local tmp_file=$(mktemp)
    local cleaned=0
    
    exec 201>"$FOLLOWUPS_FILE.lock"
    flock 201
    
    while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        local status=$(echo "$line" | jq -r '.status')
        if [[ "$status" == "done" || "$status" == "expired" ]]; then
            local resolved_at=$(echo "$line" | jq -r '.resolved_at // .expired_at // .created')
            local resolved_epoch=$(date -d "$resolved_at" +%s 2>/dev/null || echo "$NOW")
            if [[ $resolved_epoch -lt $cleanup_cutoff ]]; then
                ((cleaned++))
                continue  # skip = remove
            fi
        fi
        echo "$line" >> "$tmp_file"
    done < "$FOLLOWUPS_FILE"
    
    mv "$tmp_file" "$FOLLOWUPS_FILE"
    
    if [[ $cleaned -gt 0 ]]; then
        echo "🧹 Cleaned $cleaned old follow-ups" >> "$LOGS_DIR/$TODAY-cycles.log" 2>/dev/null
    fi
}

# Check for auto-followup in selected action config
create_auto_followup() {
    local need=$1
    local action_name=$2
    
    local auto_followup=$(jq -r --arg n "$need" --arg a "$action_name" '
        .needs[$n].actions[] | select(.name == $a) | .auto_followup // empty
    ' "$CONFIG_FILE")
    
    if [[ -n "$auto_followup" ]]; then
        local template=$(echo "$auto_followup" | jq -r '.template')
        local delay=$(echo "$auto_followup" | jq -r '.delay_hours')
        local fu_need=$(echo "$auto_followup" | jq -r '.need // "'"$need"'"')
        
        bash "$SKILL_DIR/scripts/create-followup.sh" \
            --what "$template" \
            --in "${delay}h" \
            --need "$fu_need" \
            --source auto \
            --parent "$action_name" 2>/dev/null
        
        echo "  📌 Auto follow-up: \"$template\" in ${delay}h"
    fi
}

if [[ "${TURING_PYRAMID_SOURCE_ONLY:-false}" == "true" ]]; then
    return 0 2>/dev/null || exit 0
fi

# Main execution
echo "🔺 Turing Pyramid — Cycle at $(date)"
echo "======================================"

# Phase 0: Follow-up check (pre-scan, affects satisfaction)
check_followups
cleanup_followups

# Periodic housekeeping (every ~20 cycles via audit.log line count mod)
if [[ -x "$SCRIPTS_DIR/housekeep.sh" ]]; then
    audit_lines=$(wc -l < "$SKILL_DIR/assets/audit.log" 2>/dev/null || echo 0)
    if (( audit_lines % 20 == 0 && audit_lines > 0 )); then
        "$SCRIPTS_DIR/housekeep.sh" >> "$SKILL_DIR/assets/audit.log" 2>/dev/null
    fi
fi

# Apply cross-need deprivation effects first
if [[ -x "$SCRIPTS_DIR/apply-deprivation.sh" ]]; then
    "$SCRIPTS_DIR/apply-deprivation.sh"
fi

calculate_tensions

# Check if all satisfied
all_satisfied=true
for need in "${!TENSIONS[@]}"; do
    if (( $(echo "${TENSIONS[$need]} > 0" | bc -l) )); then
        all_satisfied=false
        break
    fi
done

if $all_satisfied; then
    echo "✅ All needs satisfied. HEARTBEAT_OK"
    exit 0
fi

# Show current tensions
echo ""
echo "Current tensions:"
for need in "${!TENSIONS[@]}"; do
    if (( $(echo "${TENSIONS[$need]} > 0" | bc -l) )); then
        echo "  $need: tension=${TENSIONS[$need]} (sat=${SATISFACTIONS[$need]}, dep=${DEPRIVATIONS[$need]})"
    fi
done | sort -t'=' -k2 -rn

# Select top needs (with starvation guard)
echo ""

# Phase 1: Detect starving needs
forced_needs=()
starving_list=$(detect_starving_needs)
if [[ -n "$starving_list" ]]; then
    local_max_forced=$(jq -r '.settings.starvation_guard.max_forced_per_cycle // 1' "$CONFIG_FILE")
    forced_count=0
    while IFS= read -r starving_need; do
        if [[ $forced_count -ge $local_max_forced ]]; then
            break
        fi
        forced_needs+=("$starving_need")
        ((forced_count++))
    done <<< "$starving_list"

    echo "🚨 Starvation guard: ${forced_needs[*]} forced into cycle"
fi

# Spontaneity: accumulate surplus AFTER starvation detection
if [[ "${SKIP_SPONTANEITY:-false}" != "true" ]]; then
    starvation_active=false
    if [[ ${#forced_needs[@]} -gt 0 ]]; then
        starvation_active=true
    fi
    accumulate_surplus "$STATE_FILE" "$CONFIG_FILE" "$starvation_active"

    # Layer C: Context scan — detect environmental triggers
    run_context_scan "$SCRIPTS_DIR"
fi

# Phase 2: Fill remaining slots with top-N (excluding forced)
remaining_slots=$((MAX_ACTIONS - ${#forced_needs[@]}))
if [[ $remaining_slots -gt 0 ]]; then
    # Get top needs, filter out forced ones
    all_top=$(get_top_needs $((MAX_ACTIONS + ${#forced_needs[@]})))
    regular_needs=()
    for candidate in $all_top; do
        # Skip if already forced
        is_forced=false
        for fn in "${forced_needs[@]}"; do
            if [[ "$candidate" == "$fn" ]]; then
                is_forced=true
                break
            fi
        done
        if ! $is_forced; then
            regular_needs+=("$candidate")
        fi
        if [[ ${#regular_needs[@]} -ge $remaining_slots ]]; then
            break
        fi
    done
else
    regular_needs=()
fi

# Combine: forced first, then regular
top_needs_array=("${forced_needs[@]}" "${regular_needs[@]}")
echo "Selecting ${#top_needs_array[@]} needs (${#forced_needs[@]} forced + ${#regular_needs[@]} regular)..."

echo ""
echo "📋 Decisions:"

action_count=0
noticed_count=0

for need in "${top_needs_array[@]}"; do
    if (( $(echo "${TENSIONS[$need]} > 0" | bc -l) )); then
        sat=${SATISFACTIONS[$need]}
        tension=${TENSIONS[$need]}
        
        # Check if this need was forced by starvation guard
        is_forced_need=false
        for fn in "${forced_needs[@]}"; do
            if [[ "$need" == "$fn" ]]; then
                is_forced_need=true
                break
            fi
        done
        
        if $is_forced_need || roll_action $sat $tension; then
            # Roll for impact range (with spontaneity shift if eligible)
            tp_roll_file=$(mktemp /tmp/tp_roll_XXXXXX)
            tp_spont_file=$(mktemp /tmp/tp_spont_XXXXXX)
            roll_impact_range "$need" "$sat" > "$tp_roll_file" 2>"$tp_spont_file"
            impact_range=$(cat "$tp_roll_file")
            
            # Print surplus logs and detect [SPONTANEOUS]
            local_spont_label=""
            if [[ -s "$tp_spont_file" ]]; then
                cat "$tp_spont_file"
                if grep -q "\[SPONTANEOUS\]" "$tp_spont_file"; then
                    local_spont_label=" [SPONTANEOUS]"
                fi
            fi
            rm -f "$tp_roll_file" "$tp_spont_file"
            
            # Record spontaneous for echo tracking (Layer B3)
            if [[ -n "$local_spont_label" && "$impact_range" == "high" ]]; then
                record_spontaneous "$need" "$STATE_FILE"
            fi
            
            # If sat=3.0, skip action (fully satisfied)
            if [[ "$impact_range" == "skip" ]]; then
                ((noticed_count++))
                echo ""
                echo "○ SATISFIED: $need (sat=$sat) — no action needed"
                continue
            fi
            
            # Layer B — Noise upgrade (boredom + echo)
            local_noise_label=""
            tp_noise_file=$(mktemp /tmp/tp_noise_XXXXXX)
            noise_result=$(try_noise_upgrade "$need" "$impact_range" "$STATE_FILE" "$CONFIG_FILE" 2>"$tp_noise_file")
            if [[ -s "$tp_noise_file" ]]; then
                cat "$tp_noise_file"
            fi
            rm -f "$tp_noise_file"
            # Parse: "range [LABEL]" or just "range"
            noise_range=$(echo "$noise_result" | awk '{print $1}')
            noise_tag=$(echo "$noise_result" | sed 's/^[a-z]* *//')
            if [[ "$noise_range" != "$impact_range" ]]; then
                local_noise_label=" $noise_tag"
                impact_range="$noise_range"
            fi
            
            # ACTION - weighted action selection
            ((action_count++))
            
            # Mark forced actions
            local_forced_label=""
            if $is_forced_need; then
                local_forced_label=" [STARVATION GUARD]"
            fi
            
            # Select specific action using weights within range (with dedup guard)
            selected_action=$(select_action_with_dedup "$need" "$impact_range")
            
            # Get actual impact value of selected action
            actual_impact=""
            if [[ -n "$selected_action" ]]; then
                actual_impact=$(jq -r ".needs.\"$need\".actions[] | select(.name == \"$selected_action\") | .impact" "$CONFIG_FILE")
            fi
            
            echo ""
            echo "▶ ACTION: $need (tension=$tension, sat=$sat)$local_forced_label$local_spont_label$local_noise_label"
            echo "  Range $impact_range rolled → selected:"
            
            if [[ -n "$selected_action" ]]; then
                # Check if action is deliberative
                action_mode=$(jq -r --arg n "$need" --arg a "$selected_action" \
                    '(.needs[$n].actions[] | select(.name == $a) | .mode) // "operative"' \
                    "$CONFIG_FILE" 2>/dev/null || echo "operative")
                
                delib_label=""
                if [[ "$action_mode" == "deliberative" ]]; then
                    delib_label=" [DELIBERATIVE]"
                fi
                
                echo "    ★ $selected_action (impact: $actual_impact)$delib_label"
                # Record selection for staleness tracking
                record_action_selection "$need" "$selected_action"
                # Register in execution gate (skip in test mode)
                if [[ "${SKIP_GATE:-}" != "true" ]]; then
                    gate_args=(--need "$need" --action "$selected_action" --impact "$actual_impact" --source "run-cycle")
                    if $is_forced_need; then
                        gate_args+=(--non-deferrable)
                    fi
                    bash "$SCRIPTS_DIR/gate-propose.sh" "${gate_args[@]}" 2>/dev/null || true
                fi
                # Check for auto-followup
                create_auto_followup "$need" "$selected_action"
            else
                # Fallback: show all actions if no weighted selection
                echo "  (no $impact_range actions, showing all):"
                jq -r ".needs.\"$need\".actions[] | \"    • \" + .name + \" (impact \" + (.impact|tostring) + \")\"" "$CONFIG_FILE"
            fi
            
            # Output execution instructions based on action mode
            if [[ "${action_mode:-operative}" == "deliberative" ]]; then
                # Show recent deliberation discipline (rolling window, last 10)
                DELIB_LOG="$SCRIPTS_DIR/../assets/deliberation.log"
                if [[ -f "$DELIB_LOG" ]]; then
                    recent_resolved=$(tail -30 "$DELIB_LOG" 2>/dev/null | grep '"event":"resolved"' | tail -10)
                    if [[ -n "$recent_resolved" ]]; then
                        recent_skipped=$(echo "$recent_resolved" | grep -c '"level":"absent"' || echo 0)
                        recent_total=$(echo "$recent_resolved" | wc -l | tr -d ' ')
                        if (( recent_skipped >= 2 && recent_total > 0 )); then
                            echo "  ⚠  recent discipline: $recent_skipped/$recent_total deliberations skipped"
                        fi
                    fi
                fi
                echo "  Protocol: Think → conclude → route. Options:"
                echo "    deliberate.sh --template --need $need --action \"$selected_action\""
                echo "    deliberate.sh --validate <your-file>"
                echo "    deliberate.sh --validate-inline --conclusion \"...\" --route \"...\""
                echo "  Then: mark-satisfied.sh $need $actual_impact --conclusion \"your conclusion\""
            else
                echo "  Then: mark-satisfied.sh $need $actual_impact"
            fi
            
            # Log to memory with selected action
            if $is_forced_need; then
                log_action "$need" "$sat" "$tension [FORCED]"
            else
                log_action "$need" "$sat" "$tension"
            fi
        else
            # NON-ACTION - noticed but deferred
            ((noticed_count++))
            echo ""
            echo "○ NOTICED: $need (tension=$tension, sat=$sat) — deferred"
            log_noticed "$need" "$sat" "$tension"
        fi
    fi
done

echo ""
echo "======================================"
echo "Summary: $action_count action(s), $noticed_count noticed"

if [[ $action_count -gt 0 ]]; then
    echo ""
    echo "📋 EXECUTE these actions, then resolve:"
    bash "$SCRIPTS_DIR/gate-status.sh" 2>/dev/null || true
    echo ""
    echo "After each action:"
    echo "  mark-satisfied.sh <need> <impact> --reason \"what you did\""
    echo "  gate-resolve.sh --need <need> --evidence \"what you did\""
    echo "Or defer:"
    echo "  gate-resolve.sh --defer <id> --reason \"why\""
fi
