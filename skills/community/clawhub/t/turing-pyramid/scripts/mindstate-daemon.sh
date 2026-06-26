#!/bin/bash
# mindstate-daemon.sh — Continuity Layer: Reality updater ("The Body")
# Runs on cron every 5 min. Updates ## reality in MINDSTATE.md.
# NEVER modifies ## cognition or ## forecast.
# Safe to call at any frequency (self-throttles, locked, atomic writes).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Source shared utilities
source "$SCRIPT_DIR/mindstate-utils.sh"

# Validate environment
mindstate_validate_workspace || exit 1

# Parse --force flag (bypass throttle for boot-time freshness)
FORCE=false
[[ "${1:-}" == "--force" ]] && FORCE=true

MINDSTATE_FILE=$(mindstate_file)
STATE_FILE=$(mindstate_state_file)
CONFIG_FILE=$(mindstate_config_file)
DECAY_CONFIG=$(mindstate_decay_config)
MS_CONFIG=$(mindstate_ms_config)
PREV_SNAPSHOT=$(mindstate_prev_snapshot)
LOCK_FILE=$(mindstate_lock_file)
ASSETS_DIR="$(_ms_assets)"

NOW_EPOCH=$(now_epoch)
NOW_ISO=$(now_iso)

# ─── Trap: cleanup on unexpected termination ───
_daemon_cleanup() {
    # Remove any tmp files created by THIS process
    rm -f "$MINDSTATE_FILE.tmp.$$" "$PREV_SNAPSHOT.tmp.$$" 2>/dev/null
    # Release flock automatically (fd closed on exit)
}
trap _daemon_cleanup EXIT SIGTERM SIGINT SIGHUP

# ─── Orphaned .tmp cleanup (older than 10 min) ───
# Daemon only cleans its own process's tmp files via trap.
# Broader orphan cleanup is handled by watchdog when allow_cleanup=true.

# ─── Self-throttle: skip if last update too recent (—bypass with --force)───
if ! $FORCE; then
    MIN_INTERVAL=$(jq -r '.daemon.min_interval_seconds // 240' "$MS_CONFIG" 2>/dev/null || echo 240)
    if [[ -f "$MINDSTATE_FILE" ]]; then
        last_update=$(stat -c %Y "$MINDSTATE_FILE" 2>/dev/null || echo 0)
        seconds_since=$((NOW_EPOCH - last_update))
        if (( seconds_since < MIN_INTERVAL )); then
            exit 0
        fi
    fi
fi

# ─── Lock: prevent concurrent writes ───
exec 202>"$LOCK_FILE"
if ! flock -n 202; then
    exit 0  # freeze.sh has the lock, skip this tick
fi

# ─── 1. Temporal context ───
last_session_end=$(mindstate_get "frozen_at" 2>/dev/null || echo "$NOW_ISO")
if [[ -z "$last_session_end" || "$last_session_end" == "never" ]]; then
    last_session_end="$NOW_ISO"
fi
hours_elapsed=$(hours_since "$last_session_end" "$NOW_EPOCH")

# Day/night phase
day_start=$(jq -r '.day_start // "06:01"' "$DECAY_CONFIG" 2>/dev/null || echo "06:01")
day_end=$(jq -r '.day_end // "22:00"' "$DECAY_CONFIG" 2>/dev/null || echo "22:00")
current_time=$(date +%H:%M)
if [[ "$current_time" > "$day_start" && "$current_time" < "$day_end" ]]; then
    phase="day"
else
    phase="night"
fi
day_of_week=$(date +%u)
decay_mult=$(get_decay_multiplier)

# ─── 2. Pyramid snapshot with trends and projections ───
declare -A SAT TENSION TREND PROJECTION
needs_list=$(get_needs_list)
critical_needs=""
max_tension="0"
total_tension="0"
need_count=0

# Initialize previous snapshot if missing
if [[ ! -f "$PREV_SNAPSHOT" ]]; then
    echo "{}" > "$PREV_SNAPSHOT"
fi

for need in $needs_list; do
    # Current satisfaction (with decay applied)
    sat=$(compute_current_satisfaction "$need")
    SAT[$need]="$sat"
    
    # Tension
    tension=$(compute_tension "$need" "$sat")
    TENSION[$need]="$tension"
    
    # Track max/total tension
    if (( $(echo "$tension > $max_tension" | bc -l) )); then
        max_tension="$tension"
    fi
    total_tension=$(echo "scale=2; $total_tension + $tension" | bc -l)
    need_count=$((need_count + 1))
    
    # Trend: compare with previous daemon snapshot
    prev_sat=$(jq -r --arg n "$need" '.[$n] // "'"$sat"'"' "$PREV_SNAPSHOT" 2>/dev/null || echo "$sat")
    if (( $(echo "$sat < $prev_sat - 0.1" | bc -l) )); then
        TREND[$need]="↓"
    elif (( $(echo "$sat > $prev_sat + 0.1" | bc -l) )); then
        TREND[$need]="↑"
    else
        TREND[$need]="→"
    fi
    
    # Projection: hours until crisis (sat < 1.0)
    if (( $(echo "$sat <= 0.5" | bc -l) )); then
        PROJECTION[$need]="(IN_CRISIS)"
        critical_needs="${critical_needs:+$critical_needs, }$need"
    elif (( $(echo "$sat <= 1.0" | bc -l) )); then
        PROJECTION[$need]="(critical)"
        critical_needs="${critical_needs:+$critical_needs, }$need"
    elif (( $(echo "$sat > 1.0" | bc -l) )); then
        decay_rate=$(jq -r --arg n "$need" '.needs[$n].decay_rate_hours // 24' "$CONFIG_FILE")
        # steps of 1 sat = decay_rate hours
        hours_to_crisis=$(echo "scale=1; ($sat - 1.0) * $decay_rate / $decay_mult" | bc -l)
        if (( $(echo "$hours_to_crisis < 12" | bc -l) )); then
            PROJECTION[$need]="(crisis in ${hours_to_crisis}h)"
        else
            PROJECTION[$need]="(stable)"
        fi
    fi
done

avg_tension=$(echo "scale=2; $total_tension / $need_count" | bc -l)

# ─── 3. Surplus gate status ───
gate_min=$(jq -r '.settings.spontaneity.gate_min_satisfaction // 1.0' "$CONFIG_FILE" 2>/dev/null || echo "1.0")
surplus_gate="OPEN"
for need in $needs_list; do
    if (( $(echo "${SAT[$need]} < $gate_min" | bc -l) )); then
        surplus_gate="CLOSED"
        break
    fi
done

# Execution Gate Status
GATE_FILE="$(_ms_assets)/pending_actions.json"
exec_gate_status="CLEAR"
pending_count=0
if [[ -f "$GATE_FILE" ]]; then
    pending_count=$(jq -r '[.actions[]? | select(.status == "PENDING")] | length' "$GATE_FILE" 2>/dev/null || echo 0)
    if [[ -z "$pending_count" || "$pending_count" == "null" ]]; then
        pending_count=0
    fi
    if (( pending_count > 0 )); then
        exec_gate_status="BLOCKED"
    fi
fi

# ─── 4. Environment delta (filesystem only — zero API calls) ───
files_changed=0
memory_activity=0
research_activity=0
stale_files=""

if [[ -f "$MINDSTATE_FILE" ]]; then
    files_changed=$(find -P "$WORKSPACE" -maxdepth 2 -newer "$MINDSTATE_FILE" -name "*.md" 2>/dev/null | wc -l)
fi

if [[ -d "$WORKSPACE/memory" && -f "$MINDSTATE_FILE" ]]; then
    memory_activity=$(find -P "$WORKSPACE/memory" -name "*.md" -newer "$MINDSTATE_FILE" 2>/dev/null | wc -l)
fi

if [[ -d "$WORKSPACE/research" && -f "$MINDSTATE_FILE" ]]; then
    research_activity=$(find -P "$WORKSPACE/research" -type f -newer "$MINDSTATE_FILE" 2>/dev/null | wc -l)
fi

# Stale files
stale_threshold_hours=$(jq -r '.environment_delta.stale_file_threshold_hours // 72' "$MS_CONFIG" 2>/dev/null || echo 72)
watched_files=$(jq -r '.environment_delta.watched_files[]? // empty' "$MS_CONFIG" 2>/dev/null || echo "INTENTIONS.md")
for wf in $watched_files; do
    fpath="$WORKSPACE/$wf"
    if [[ -f "$fpath" ]]; then
        file_age_hours=$(echo "scale=0; ($NOW_EPOCH - $(stat -c %Y "$fpath")) / 3600" | bc -l)
        if (( file_age_hours > stale_threshold_hours )); then
            stale_files="${stale_files:+$stale_files, }$wf (${file_age_hours}h)"
        fi
    fi
done

# ─── 5. System health ───
gateway_alive="unknown"
check_gw=$(jq -r '.system_health.check_gateway // true' "$MS_CONFIG" 2>/dev/null || echo "true")
if [[ "$check_gw" == "true" ]]; then
    gw_name=$(jq -r '.system_health.gateway_process_name // "openclaw"' "$MS_CONFIG" 2>/dev/null || echo "openclaw")
    if pgrep -f "$gw_name" &>/dev/null; then
        gateway_alive="yes"
    else
        gateway_alive="no"
    fi
fi

disk_warning=""
disk_thresh=$(jq -r '.system_health.disk_warning_threshold_pct // 90' "$MS_CONFIG" 2>/dev/null || echo 90)
disk_pct=$(df "$WORKSPACE" 2>/dev/null | tail -1 | awk '{print $5}' | tr -d '%')
if [[ -n "$disk_pct" ]] && (( disk_pct > disk_thresh )); then
    disk_warning="  disk_usage: ${disk_pct}% (WARNING)"
fi

# ─── 6. Stale cognition detection ───
cognition_stale=""
cognition_stale_hours=0
if [[ -f "$MINDSTATE_FILE" ]]; then
    frozen_at=$(grep "^frozen_at:" "$MINDSTATE_FILE" 2>/dev/null | head -1 | sed 's/^frozen_at: *//')
    if [[ -n "$frozen_at" && "$frozen_at" != "never" ]]; then
        frozen_epoch=$(iso_to_epoch "$frozen_at")
        cognition_stale_hours=$(echo "scale=1; ($NOW_EPOCH - $frozen_epoch) / 3600" | bc -l)
        stale_cog_thresh=$(jq -r '.freeze.stale_cognition_hours // 24' "$MS_CONFIG" 2>/dev/null || echo 24)
        if (( $(echo "$cognition_stale_hours > $stale_cog_thresh" | bc -l) )); then
            cognition_stale="stale (${cognition_stale_hours}h since last freeze)"
        fi
    elif [[ "$frozen_at" == "never" ]]; then
        cognition_stale="never frozen"
    fi
fi

# ─── 7. Physical temperature ───
# 6-word deterministic vocabulary, first-match wins

# Check recent spontaneous (within 6h)
recent_spontaneous=false
for need in $needs_list; do
    last_spont=$(jq -r --arg n "$need" '.[$n].last_spontaneous_at // "1970-01-01T00:00:00Z"' "$STATE_FILE")
    hours_since_spont=$(hours_since "$last_spont" "$NOW_EPOCH")
    if (( $(echo "$hours_since_spont < 6" | bc -l) )); then
        recent_spontaneous=true
        break
    fi
done

# Check surplus accumulation
surplus_accumulating=false
if [[ "$surplus_gate" == "OPEN" ]]; then
    for need in $needs_list; do
        surplus=$(jq -r --arg n "$need" '.[$n].surplus // 0' "$STATE_FILE")
        has_spont=$(jq -r --arg n "$need" '.needs[$n].spontaneous // null' "$CONFIG_FILE" 2>/dev/null)
        if [[ "$has_spont" != "null" ]]; then
            threshold=$(jq -r --arg n "$need" '.needs[$n].spontaneous.threshold // 999' "$CONFIG_FILE" 2>/dev/null)
            if [[ "$threshold" != "999" ]] && (( $(echo "$surplus > $threshold * 0.5" | bc -l) )); then
                surplus_accumulating=true
                break
            fi
        fi
    done
fi

# Temperature mapping (order matters: first match wins)
# Temperature thresholds calibrated for Turing-exp formula:
# Homeostasis avg ≈ 0.25, moderate stress avg ≈ 2-3, crisis avg ≈ 5+
physical_temperature="calm"
if [[ -n "$critical_needs" ]]; then
    physical_temperature="crisis"
elif (( $(echo "$avg_tension > 3" | bc -l) )); then
    physical_temperature="pressure"
elif (( $(echo "$max_tension > 2" | bc -l) )) && (( $(echo "$avg_tension <= 3" | bc -l) )); then
    physical_temperature="focus"
elif $recent_spontaneous; then
    physical_temperature="impulse"
elif $surplus_accumulating; then
    physical_temperature="accumulation"
fi

# ─── 8. Assemble ## reality ───
# Build pyramid snapshot lines
PYRAMID_BLOCK=""
for need in $(echo "$needs_list" | sort); do
    sat="${SAT[$need]}"
    trend="${TREND[$need]}"
    proj="${PROJECTION[$need]}"
    PYRAMID_BLOCK+="  $need: $sat $trend $proj"$'\n'
done

REALITY_BLOCK="## reality
# [updated by mindstate-daemon.sh]
timestamp: $NOW_ISO
last_session_end: $last_session_end
hours_elapsed: $hours_elapsed
temporal:
  phase: $phase
  day_of_week: $day_of_week
  decay_multiplier: $decay_mult
pyramid_snapshot:
${PYRAMID_BLOCK}critical_needs: ${critical_needs:-none}
surplus_gate: $surplus_gate
execution_gate: $exec_gate_status
pending_actions: $pending_count
environment_delta:
  files_changed: $files_changed
  memory_activity: $memory_activity
  research_activity: $research_activity
  stale_files: ${stale_files:-none}
system:
  gateway: $gateway_alive
${disk_warning}${cognition_stale:+
  cognition: $cognition_stale}
physical_temperature: $physical_temperature"

# ─── 9. Atomic write: replace reality, preserve cognition+forecast ───
TMP_FILE="$MINDSTATE_FILE.tmp.$$"

if [[ -f "$MINDSTATE_FILE" ]]; then
    FROZEN_SECTIONS=$(sed -n '/^## cognition/,$p' "$MINDSTATE_FILE")
else
    # First run: create initial frozen sections
    FROZEN_SECTIONS="## cognition
# [not yet initialized — first session has not ended]
frozen_at: never
trajectory: (awaiting first session)
open_threads: []
momentum: (none)
cognitive_temperature: initializing

## forecast
structural: []
semantic: []"
fi

cat > "$TMP_FILE" <<EOF
# MINDSTATE
# Auto-managed by continuity layer. Do not edit manually.
# daemon → reality | agent session end → cognition + forecast

$REALITY_BLOCK

$FROZEN_SECTIONS
EOF

mv "$TMP_FILE" "$MINDSTATE_FILE"

# ─── 10. Save snapshot for trend comparison ───
TMP_PREV="$PREV_SNAPSHOT.tmp.$$"
echo "{" > "$TMP_PREV"
first=true
for need in $needs_list; do
    if $first; then first=false; else echo "," >> "$TMP_PREV"; fi
    printf '  "%s": %s' "$need" "${SAT[$need]}" >> "$TMP_PREV"
done
echo "" >> "$TMP_PREV"
echo "}" >> "$TMP_PREV"
mv "$TMP_PREV" "$PREV_SNAPSHOT"
