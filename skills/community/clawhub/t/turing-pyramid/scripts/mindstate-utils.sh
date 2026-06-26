#!/bin/bash
# mindstate-utils.sh — Continuity Layer: Shared utilities
# Sourced by daemon, freeze, and boot scripts.

# ─── Resolve paths ───
_MINDSTATE_UTILS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_MINDSTATE_SKILL_DIR="$(cd "$_MINDSTATE_UTILS_DIR/.." && pwd)"

# Validate WORKSPACE
mindstate_validate_workspace() {
    if [[ -z "$WORKSPACE" ]]; then
        echo "❌ ERROR: WORKSPACE not set" >&2
        return 1
    fi
    if [[ ! -d "$WORKSPACE" ]]; then
        echo "❌ ERROR: WORKSPACE directory not found: $WORKSPACE" >&2
        return 1
    fi
    return 0
}

# Get skill directory
mindstate_skill_dir() {
    echo "$_MINDSTATE_SKILL_DIR"
}

# Standard file paths
mindstate_file() { echo "$WORKSPACE/MINDSTATE.md"; }
# Override with MINDSTATE_ASSETS_DIR for testing isolation
_ms_assets() { echo "${MINDSTATE_ASSETS_DIR:-$_MINDSTATE_SKILL_DIR/assets}"; }

mindstate_state_file() { echo "$(_ms_assets)/needs-state.json"; }
mindstate_config_file() { local d="$(_ms_assets)"; [[ -f "$d/needs-config.json" ]] && echo "$d/needs-config.json" || echo "$_MINDSTATE_SKILL_DIR/assets/needs-config.json"; }
mindstate_decay_config() { local d="$(_ms_assets)"; [[ -f "$d/decay-config.json" ]] && echo "$d/decay-config.json" || echo "$_MINDSTATE_SKILL_DIR/assets/decay-config.json"; }
mindstate_ms_config() { local d="$(_ms_assets)"; [[ -f "$d/mindstate-config.json" ]] && echo "$d/mindstate-config.json" || echo "$_MINDSTATE_SKILL_DIR/assets/mindstate-config.json"; }
mindstate_audit_log() { echo "$(_ms_assets)/audit.log"; }
mindstate_lock_file() { echo "$(_ms_assets)/mindstate.lock"; }
mindstate_prev_snapshot() { echo "$(_ms_assets)/mindstate-prev-snapshot.json"; }
mindstate_boot_log() { echo "$(_ms_assets)/mindstate-boot.log"; }

# ─── Epoch helpers ───
now_epoch() { date +%s; }
now_iso() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

iso_to_epoch() {
    local iso="$1"
    date -d "$iso" +%s 2>/dev/null || echo 0
}

# ─── Deliberation log path ───
mindstate_deliberation_log() { echo "$(_ms_assets)/deliberation.log"; }

# ─── classify_deliberation_level <conclusion> <route> <mode> <action_proposed_at> ───
# Returns: absent / minimal / substantive / deep / n/a
classify_deliberation_level() {
    local conclusion="${1:-}" route="${2:-}" mode="${3:-operative}" proposed_at="${4:-}"

    # Non-deliberative actions — not tracked
    if [[ "$mode" != "deliberative" ]]; then
        echo "n/a"
        return
    fi

    local conc_len=${#conclusion}

    # Check for deep tier: deliberation file with phase markers created after action was proposed
    if [[ -n "$proposed_at" && -d "${WORKSPACE:-}/research/deliberations" ]]; then
        local proposed_epoch
        proposed_epoch=$(iso_to_epoch "$proposed_at" 2>/dev/null || echo 0)
        if (( proposed_epoch > 0 )); then
            local recent_delib_file
            recent_delib_file=$(find -P "${WORKSPACE}/research/deliberations" -name "*.md" -type f \
                -newermt "@$proposed_epoch" 2>/dev/null | head -1)
            if [[ -n "$recent_delib_file" ]]; then
                local phase_count
                phase_count=$(grep -ciE '^(##|###)\s*(REPRESENT|RELATE|GENERATE|EVALUATE|CONCLUDE|ROUTE)' \
                    "$recent_delib_file" 2>/dev/null || echo 0)
                if (( phase_count >= 3 )); then
                    echo "deep"
                    return
                fi
            fi
        fi
    fi

    # Tier by conclusion length + route
    if (( conc_len < 10 )); then
        echo "absent"
    elif (( conc_len < 50 )) || [[ -z "$route" ]]; then
        echo "minimal"
    else
        echo "substantive"
    fi
}

hours_since() {
    local past_iso="$1"
    local now=${2:-$(now_epoch)}
    local past_epoch
    past_epoch=$(iso_to_epoch "$past_iso")
    echo "scale=1; ($now - $past_epoch) / 3600" | bc -l
}

# ─── Decay multiplier ───
get_decay_multiplier() {
    local decay_config
    decay_config=$(mindstate_decay_config)
    
    if [[ ! -f "$decay_config" ]]; then
        echo "1.0"
        return
    fi
    
    local day_night_mode
    day_night_mode=$(jq -r '.day_night_mode // false' "$decay_config")
    
    if [[ "$day_night_mode" != "true" ]]; then
        echo "1.0"
        return
    fi
    
    local day_start day_end current_time
    day_start=$(jq -r '.day_start // "06:01"' "$decay_config")
    day_end=$(jq -r '.day_end // "22:00"' "$decay_config")
    current_time=$(date +%H:%M)
    
    if [[ "$current_time" > "$day_start" && "$current_time" < "$day_end" ]]; then
        jq -r '.day_decay_multiplier // 1.0' "$decay_config"
    else
        jq -r '.night_decay_multiplier // 0.5' "$decay_config"
    fi
}

# ─── Compute current satisfaction for a need ───
# Reads stored satisfaction + applies CONTINUOUS decay since last_decay_check.
# NOTE: This is an approximation. run-cycle.sh uses DISCRETE floor() steps.
# Daemon values may differ slightly from run-cycle — by design.
# Daemon = thermometer (continuous, approximate). Run-cycle = authoritative.
compute_current_satisfaction() {
    local need="$1"
    local state_file config_file now_epoch
    state_file=$(mindstate_state_file)
    config_file=$(mindstate_config_file)
    now_epoch=$(now_epoch)
    
    # Read stored values (top-level need key from state file)
    local stored_sat last_decay_check decay_rate
    stored_sat=$(jq -r --arg n "$need" '.[$n].satisfaction // 3.0' "$state_file")
    last_decay_check=$(jq -r --arg n "$need" '.[$n].last_decay_check // "1970-01-01T00:00:00Z"' "$state_file")
    decay_rate=$(jq -r --arg n "$need" '.needs[$n].decay_rate_hours // 24' "$config_file")
    
    # Compute additional decay since last check
    local last_epoch hours_since decay_mult decay_delta current_sat
    last_epoch=$(iso_to_epoch "$last_decay_check")
    hours_since=$(echo "scale=4; ($now_epoch - $last_epoch) / 3600" | bc -l)
    decay_mult=$(get_decay_multiplier)
    decay_delta=$(echo "scale=4; ($hours_since / $decay_rate) * $decay_mult" | bc -l)
    
    current_sat=$(echo "scale=2; $stored_sat - $decay_delta" | bc -l)
    
    # Clamp to [0.50, 3.00] (floor from config, default 0.5)
    local floor
    floor=$(jq -r --arg n "$need" '.needs[$n].floor // 0.5' "$config_file")
    if (( $(echo "$current_sat < $floor" | bc -l) )); then
        current_sat="$floor"
    fi
    if (( $(echo "$current_sat > 3.00" | bc -l) )); then
        current_sat="3.00"
    fi
    
    echo "$current_sat"
}

# ─── Compute tension for a need ───
compute_tension() {
    local need="$1"
    local satisfaction="$2"
    local config_file
    config_file=$(mindstate_config_file)
    
    local importance deprivation tension
    importance=$(jq -r --arg n "$need" '.needs[$n].importance // 1' "$config_file")
    deprivation=$(echo "scale=2; 3 - $satisfaction" | bc -l)
    if (( $(echo "$deprivation < 0" | bc -l) )); then deprivation="0.00"; fi
    # Turing-exp: dep² + importance × max(0, dep - threshold)²
    local crisis_threshold
    crisis_threshold=$(jq -r '.settings.tension_formula.crisis_threshold // 1.0' "$config_file")
    local crisis_excess=$(echo "scale=4; $deprivation - $crisis_threshold" | bc -l)
    if (( $(echo "$crisis_excess < 0" | bc -l) )); then crisis_excess="0"; fi
    tension=$(echo "scale=1; ($deprivation * $deprivation) + ($importance * $crisis_excess * $crisis_excess)" | bc -l)
    echo "$tension"
}

# ─── Get need list ───
get_needs_list() {
    local config_file
    config_file=$(mindstate_config_file)
    jq -r '.needs | keys[]' "$config_file" | sort
}

# ─── Substantive session check ───
is_session_substantive() {
    local session_start_epoch="$1"
    local now_epoch
    now_epoch=$(now_epoch)
    
    local state_file audit_log ms_config
    state_file=$(mindstate_state_file)
    audit_log=$(mindstate_audit_log)
    ms_config=$(mindstate_ms_config)
    
    local threshold_seconds min_file_changes
    threshold_seconds=$(jq -r '.freeze.substantive_threshold_seconds // 120' "$ms_config" 2>/dev/null || echo 120)
    min_file_changes=$(jq -r '.freeze.substantive_min_file_changes // 2' "$ms_config" 2>/dev/null || echo 2)
    
    # Criterion 1: pyramid action executed during session
    if [[ -f "$audit_log" ]]; then
        local since_iso
        since_iso=$(date -u -d "@$session_start_epoch" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null)
        local action_count
        action_count=$(awk -v since="$since_iso" '
            BEGIN { count=0 }
            { 
                if (match($0, /"timestamp":"([^"]+)"/, m)) {
                    if (m[1] > since) count++
                }
            }
            END { print count }
        ' "$audit_log" 2>/dev/null || echo 0)
        if (( action_count > 0 )); then
            return 0
        fi
    fi
    
    # Criterion 2: session duration > threshold
    local duration=$((now_epoch - session_start_epoch))
    if (( duration > threshold_seconds )); then
        return 0
    fi
    
    # Criterion 3: workspace files modified
    if [[ -n "$WORKSPACE" ]]; then
        local modified_files
        modified_files=$(find -P "$WORKSPACE" -maxdepth 2 -name "*.md" \
            -newermt "@$session_start_epoch" 2>/dev/null | wc -l)
        if (( modified_files > min_file_changes )); then
            return 0
        fi
    fi
    
    return 1
}

# ─── Extract section from MINDSTATE.md ───
# Usage: extract_mindstate_section "reality" < MINDSTATE.md
extract_mindstate_section() {
    local section="$1"
    local file="$2"
    [[ -z "$file" ]] && file=$(mindstate_file)
    sed -n "/^## $section/,/^## [a-z]/{ /^## [a-z]/!p; /^## $section/p }" "$file" 2>/dev/null
}

# ─── Parse key from MINDSTATE section ───
mindstate_get() {
    local key="$1"
    local file
    file=$(mindstate_file)
    local val
    val=$(grep "^${key}:" "$file" 2>/dev/null | head -1 | sed "s/^${key}: *//" || true)
    echo "$val"
}
