#!/bin/bash
# mindstate-boot.sh — Continuity Layer: Boot + reconciliation
# Called FIRST at session start, before SOUL.md or MEMORY.md.
# Reads MINDSTATE.md, reconciles forecast vs reality, outputs context block.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/mindstate-utils.sh"

mindstate_validate_workspace || exit 1

MINDSTATE_FILE=$(mindstate_file)
MS_CONFIG=$(mindstate_ms_config)
STATE_FILE=$(mindstate_state_file)
CONFIG_FILE=$(mindstate_config_file)
BOOT_LOG=$(mindstate_boot_log)

# ─── First boot: create initial MINDSTATE if missing ───
if [[ ! -f "$MINDSTATE_FILE" ]]; then
    echo "[MINDSTATE] First boot — creating initial state"
    bash "$SCRIPT_DIR/mindstate-daemon.sh" 2>/dev/null || true
    
    echo "═══════════════════════════════════════"
    echo "  CONTINUITY BOOT — FIRST START"
    echo "═══════════════════════════════════════"
    echo ""
    echo "No previous state. Clean initialization."
    echo "═══════════════════════════════════════"
    
    # Log first boot
    echo "{\"timestamp\":\"$(now_iso)\",\"hours_elapsed\":0,\"transition\":\"FIRST_BOOT\",\"continuity_score\":1.0,\"staleness\":\"FIRST_BOOT\",\"temp_drift\":\"N/A\"}" >> "$BOOT_LOG"
    exit 0
fi

# ─── Force fresh reality before reconciliation (--force bypasses throttle) ───
# SKIP_DAEMON_FORCE=true lets tests control MINDSTATE without interference
if [[ "${SKIP_DAEMON_FORCE:-false}" == "true" ]]; then
    bash "$SCRIPT_DIR/mindstate-daemon.sh" 2>/dev/null || true
else
    bash "$SCRIPT_DIR/mindstate-daemon.sh" --force 2>/dev/null || true
fi

NOW_EPOCH=$(now_epoch)

# ─── 1. Parse MINDSTATE ───
hours_elapsed=$(mindstate_get "hours_elapsed")
physical_temp=$(mindstate_get "physical_temperature")
cognitive_temp=$(mindstate_get "cognitive_temperature")
frozen_at=$(mindstate_get "frozen_at")
trajectory=$(mindstate_get "trajectory")
critical=$(mindstate_get "critical_needs")
momentum=$(mindstate_get "momentum")
surplus_gate=$(mindstate_get "surplus_gate")
exec_gate_status=$(mindstate_get "execution_gate")
pending_count=$(mindstate_get "pending_actions")
phase=$(grep "phase:" "$MINDSTATE_FILE" 2>/dev/null | head -1 | sed 's/.*phase: *//' || true)

# ─── 2. Staleness check ───
stale_threshold=$(jq -r '.boot.stale_threshold_hours // 24' "$MS_CONFIG" 2>/dev/null || echo 24)
very_stale_threshold=$(jq -r '.boot.very_stale_threshold_hours // 48' "$MS_CONFIG" 2>/dev/null || echo 48)

staleness="FRESH"
cognition_trust="FULL"

if [[ -z "$hours_elapsed" || "$frozen_at" == "never" ]]; then
    staleness="FIRST_BOOT"
    cognition_trust="NONE"
elif (( $(echo "${hours_elapsed:-0} > $very_stale_threshold" | bc -l) )); then
    staleness="VERY_STALE"
    cognition_trust="MINIMAL"  # trust only open_threads
elif (( $(echo "${hours_elapsed:-0} > $stale_threshold" | bc -l) )); then
    staleness="STALE"
    cognition_trust="PARTIAL"  # open_threads + momentum ok, trajectory may need revision
fi

# ─── 3. Temperature merge ───
temp_status="ALIGNED"
merged_temperature="${cognitive_temp:-neutral}"

if [[ -n "$physical_temp" && -n "$cognitive_temp" && "$physical_temp" != "$cognitive_temp" ]]; then
    temp_status="DRIFT_DETECTED"
    merged_temperature="$physical_temp"  # reality takes priority
fi

# ─── 4. Forecast reconciliation ───
prediction_errors=()
confirmations=()

# Parse structural predictions from forecast section
in_structural=false
while IFS= read -r line; do
    if [[ "$line" == "structural:" ]]; then
        in_structural=true
        continue
    fi
    if [[ "$line" == "semantic:" ]]; then
        in_structural=false
        continue
    fi
    
    if $in_structural && [[ "$line" =~ ^[[:space:]]*-[[:space:]] ]]; then
        prediction=$(echo "$line" | sed 's/^[[:space:]]*- //')
        
        # Skip placeholder predictions
        [[ "$prediction" == "(no near-term predictions)" ]] && continue
        [[ "$prediction" == "[]" ]] && continue
        
        # Match "need < threshold within Xh"
        if [[ "$prediction" =~ ^([a-z]+)[[:space:]]*\<[[:space:]]*([0-9.]+) ]]; then
            pred_need="${BASH_REMATCH[1]}"
            pred_threshold="${BASH_REMATCH[2]}"
            
            # Compute actual current satisfaction
            actual_sat=$(compute_current_satisfaction "$pred_need" 2>/dev/null || echo "unknown")
            if [[ "$actual_sat" != "unknown" ]] && (( $(echo "$actual_sat < $pred_threshold" | bc -l 2>/dev/null) )); then
                confirmations+=("✓ $prediction → CONFIRMED (actual: $actual_sat)")
            else
                prediction_errors+=("✗ $prediction → NOT YET (actual: $actual_sat)")
            fi
        
        # Match "need surplus approaching threshold"
        elif [[ "$prediction" =~ ^([a-z]+)[[:space:]]surplus ]]; then
            pred_need="${BASH_REMATCH[1]}"
            surplus=$(jq -r --arg n "$pred_need" '.[$n].surplus // 0' "$STATE_FILE" 2>/dev/null || echo 0)
            threshold=$(jq -r --arg n "$pred_need" '.needs[$n].spontaneous.threshold // 999' "$CONFIG_FILE" 2>/dev/null || echo 999)
            if [[ "$threshold" != "999" ]] && (( $(echo "$surplus >= $threshold" | bc -l 2>/dev/null) )); then
                confirmations+=("✓ $prediction → CONFIRMED (surplus: $surplus)")
            else
                confirmations+=("⧖ $prediction → IN PROGRESS (surplus: $surplus)")
            fi
        
        # Match "N followup(s) due"
        elif [[ "$prediction" =~ followup ]]; then
            confirmations+=("⧖ $prediction → (check pending)")
        fi
    fi
done < "$MINDSTATE_FILE"

# Continuity score
total_predictions=$(( ${#confirmations[@]} + ${#prediction_errors[@]} ))
if (( total_predictions > 0 )); then
    confirmed_count=0
    for c in "${confirmations[@]}"; do
        [[ "$c" == ✓* ]] && confirmed_count=$((confirmed_count + 1))
    done
    continuity_score=$(echo "scale=2; $confirmed_count / $total_predictions" | bc -l)
else
    continuity_score="1.00"  # no predictions = smooth by default
fi

# Transition quality
smooth_thresh=$(jq -r '.boot.smooth_transition_threshold // 0.7' "$MS_CONFIG" 2>/dev/null || echo "0.7")
partial_thresh=$(jq -r '.boot.partial_transition_threshold // 0.4' "$MS_CONFIG" 2>/dev/null || echo "0.4")

if (( $(echo "$continuity_score > $smooth_thresh" | bc -l) )); then
    transition="SMOOTH"
elif (( $(echo "$continuity_score > $partial_thresh" | bc -l) )); then
    transition="PARTIAL_DISCONTINUITY"
else
    transition="HARD_BREAK"
fi

# ─── 5. Output boot context ───
echo "═══════════════════════════════════════"
echo "  CONTINUITY BOOT — $(date '+%Y-%m-%d %H:%M')"
echo "═══════════════════════════════════════"
echo ""
echo "Boot after ${hours_elapsed}h offline"
echo "Cognition trust: $cognition_trust"
echo "Transition: $transition (score: $continuity_score)"
echo ""

if [[ "$temp_status" == "DRIFT_DETECTED" ]]; then
    echo "⚠ TEMPERATURE DRIFT: cognitive=$cognitive_temp → physical=$physical_temp"
    echo "  (reality shifted while cognition was frozen)"
    echo ""
fi

if [[ "$staleness" == "STALE" || "$staleness" == "VERY_STALE" ]]; then
    echo "⚠ STALE COGNITION: frozen ${hours_elapsed}h ago"
    if [[ "$staleness" == "VERY_STALE" ]]; then
        echo "  Trust only open_threads. Trajectory and momentum likely stale."
    else
        echo "  Trajectory may need revision."
    fi
    echo ""
fi

echo "Where I am: ${trajectory:-(unknown)}"
echo "Momentum: ${momentum:-(none)}"
echo "Temperature: $merged_temperature"
echo "Critical: ${critical:-none}"
echo "Surplus gate: ${surplus_gate:-unknown}"
echo "Execution gate: ${exec_gate_status:-unknown} (${pending_count:-0} pending)"
echo "Phase: ${phase:-unknown}"
echo ""

if [[ "${exec_gate_status:-unknown}" == "BLOCKED" ]]; then
    echo "⚠ EXECUTION GATE BLOCKED: ${pending_count:-0} pending action(s) — resolve before new proposals"
    echo ""
fi

if (( ${#confirmations[@]} > 0 || ${#prediction_errors[@]} > 0 )); then
    echo "Forecast reconciliation:"
    for c in "${confirmations[@]}"; do echo "  $c"; done
    for e in "${prediction_errors[@]}"; do echo "  $e"; done
    echo ""
fi

# Open threads (from cognition)
echo "Open threads:"
in_threads=false
while IFS= read -r line; do
    if [[ "$line" == "open_threads:" ]]; then
        in_threads=true
        continue
    fi
    if $in_threads && [[ "$line" =~ ^[[:space:]]*-[[:space:]] ]]; then
        echo "  $line"
    elif $in_threads && [[ ! "$line" =~ ^[[:space:]] ]]; then
        break
    fi
done < "$MINDSTATE_FILE"
echo ""

# ─── 5b. Contextual recall (association scan) ───
ASSOC_SCRIPT="$SCRIPT_DIR/association-scan.sh"
if [[ -x "$ASSOC_SCRIPT" ]]; then
    # Build keywords from open threads + high-level context
    boot_keywords=""

    # Extract open thread words (>4 chars)
    in_threads=false
    while IFS= read -r line; do
        if [[ "$line" == "open_threads:" ]]; then
            in_threads=true; continue
        fi
        if $in_threads && [[ "$line" =~ ^[[:space:]]*-[[:space:]] ]]; then
            thread_text=$(echo "$line" | sed 's/^[[:space:]]*-[[:space:]]*//')
            thread_words=$(echo "$thread_text" | tr ' ' '\n' | awk 'length > 4' | head -3 | tr '\n' ' ')
            boot_keywords="$boot_keywords $thread_words"
        elif $in_threads && [[ ! "$line" =~ ^[[:space:]] ]]; then
            break
        fi
    done < "$MINDSTATE_FILE"

    # Add trajectory words if available
    if [[ -n "${trajectory:-}" ]]; then
        traj_words=$(echo "$trajectory" | tr ' ' '\n' | awk 'length > 4' | head -3 | tr '\n' ' ')
        boot_keywords="$boot_keywords $traj_words"
    fi

    boot_keywords=$(echo "$boot_keywords" | xargs) # trim

    if [[ -n "$boot_keywords" ]]; then
        echo "Contextual recall:"
        bash "$ASSOC_SCRIPT" --keywords "$boot_keywords" --max-results 5 \
            --recency-hours 336 --exclude-source mindstate_residuals 2>/dev/null || true
        echo ""
    fi
fi

echo "═══════════════════════════════════════"

# ─── 6. Log boot event ───
echo "{\"timestamp\":\"$(now_iso)\",\"hours_elapsed\":${hours_elapsed:-0},\"transition\":\"$transition\",\"continuity_score\":$continuity_score,\"staleness\":\"$staleness\",\"temp_drift\":\"$temp_status\"}" >> "$BOOT_LOG"
