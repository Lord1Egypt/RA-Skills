#!/bin/bash
# scan_closure.sh - Check for task completion vs open items
# Returns: 3=mostly closed, 2=balanced, 1=accumulating, 0=overwhelmed

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_scan_helper.sh"

NEED="closure"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d 2>/dev/null)

time_sat=$(calc_time_satisfaction "$NEED")

POS_PATTERN="(completed|done|finished|resolved|closed|checked off|\[x\]|✅|✓)"
NEG_PATTERN="(TODO|PENDING|\[ \]|waiting for|need to|should do|to follow up|open question|unresolved|blocked)"

pos_signals=0
neg_signals=0
scan_lines_in_file "$MEMORY_DIR/$TODAY.md" "$POS_PATTERN" "$NEG_PATTERN"
scan_lines_in_file "$MEMORY_DIR/$YESTERDAY.md" "$POS_PATTERN" "$NEG_PATTERN"

# Git drift check — uncommitted TP changes count as open items
git_drift=$($SCRIPT_DIR/scan_git_drift.sh 2>/dev/null)
if [[ "$git_drift" == drift:* ]]; then
    drift_count=${git_drift#drift:}
    drift_count=${drift_count%% *}
    # Each drifted file = 1 neg signal (open work not committed)
    neg_signals=$((neg_signals + drift_count))
fi

# Deferred backlog pressure — accumulating dropped items add psychological weight
# Implements declared check: deferred_backlog_size
# _ASSETS_DIR is already set by _scan_helper.sh (respects SCAN_ASSETS_DIR / MINDSTATE_ASSETS_DIR)
PENDING_FILE="$_ASSETS_DIR/pending_actions.json"
if [[ -f "$PENDING_FILE" ]]; then
    deferred_count=$(jq -r '[.actions[]? | select(.status == "DEFERRED")] | length' "$PENDING_FILE" 2>/dev/null || echo 0)
    # Pressure bands calibrated to scan_closure cascade thresholds:
    # cascade: neg>5 → event_sat=0, neg>3 → event_sat=1
    # <5 deferred  → no boost (normal)
    # 5-10         → +2 neg (pushes to event_sat=1 territory)
    # 11-20        → +4 neg (event_sat=1, noticeable pressure)
    # >20          → +6 neg (event_sat=0, backlog paralysis)
    if (( deferred_count > 20 )); then
        neg_signals=$((neg_signals + 6))
    elif (( deferred_count > 10 )); then
        neg_signals=$((neg_signals + 4))
    elif (( deferred_count > 5 )); then
        neg_signals=$((neg_signals + 2))
    fi
fi

net=$((pos_signals - neg_signals))

if [[ $neg_signals -gt $pos_signals ]] && [[ $neg_signals -gt 5 ]]; then
    event_sat=0
elif [[ $net -ge 3 ]]; then
    event_sat=3
elif [[ $net -ge 0 ]]; then
    event_sat=2
elif [[ $neg_signals -gt 3 ]]; then
    event_sat=1
else
    event_sat=$time_sat
fi

smart_satisfaction "$NEED" "$event_sat"
