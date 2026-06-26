#!/bin/bash
# scan_integrity.sh - Check alignment with SOUL.md principles
# Reads memory files for alignment signals and drift markers.
# Implements declared checks: last_checkpoint_age, recent_alignment_flags
# Returns: 3=aligned, 2=minor drift, 1=concerning, 0=compromised

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_scan_helper.sh"

NEED="integrity"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d 2>/dev/null)

time_sat=$(calc_time_satisfaction "$NEED")

# ─── Positive: explicit alignment work, checkpoint writing, SOUL engagement ───
POS_PATTERN="(integrity check|integrity reflection|integrity checkpoint|SOUL\.md|reviewed SOUL|aligned with|alignment confirmed|values check|principle check|re-read SOUL|self.check passed|acting consistent|stayed true|consistent with|no drift|remains aligned)"

# ─── Negative: explicit drift markers, contradictions with values ───
NEG_PATTERN="(drift(ed|ing)?|misaligned|compromised|contradicts (my )?values|acted against|violated principle|not aligned|integrity tension|inconsistent with SOUL|broke my own|betrayed|lied|behaved against)"

pos_signals=0
neg_signals=0
scan_lines_in_file "$MEMORY_DIR/$TODAY.md" "$POS_PATTERN" "$NEG_PATTERN"
scan_lines_in_file "$MEMORY_DIR/$YESTERDAY.md" "$POS_PATTERN" "$NEG_PATTERN"

# ─── Checkpoint age: has INTEGRITY_CHECKPOINTS.md been updated in last 7 days? ───
# Implements declared check: last_checkpoint_age
checkpoint_bonus=0
CHECKPOINTS_FILE="$WORKSPACE/INTEGRITY_CHECKPOINTS.md"
if [[ -f "$CHECKPOINTS_FILE" ]]; then
    # Check if file was modified in last 7 days
    last_mod=$(date -r "$CHECKPOINTS_FILE" +%s 2>/dev/null || stat -c %Y "$CHECKPOINTS_FILE" 2>/dev/null || echo 0)
    now_ts=$(date +%s)
    age_days=$(( (now_ts - last_mod) / 86400 ))
    if (( age_days <= 7 )); then
        checkpoint_bonus=1
    fi
    # Check for unresolved drift (status=drift + resolution=pending) — add neg signal
    pending_drift=$(grep -c 'Status.*drift' "$CHECKPOINTS_FILE" 2>/dev/null || echo 0)
    resolved_count=$(grep -c 'Resolution.*resolved' "$CHECKPOINTS_FILE" 2>/dev/null || echo 0)
    if (( pending_drift > resolved_count )); then
        neg_signals=$((neg_signals + 1))
    fi
else
    # No checkpoints file — mild neg signal (file should exist)
    neg_signals=$((neg_signals + 1))
fi

# Also check daily memory for integrity checkpoint mentions (legacy)
for days_back in 0 1 2; do
    check_date=$(date -d "$days_back days ago" +%Y-%m-%d 2>/dev/null || date -v-${days_back}d +%Y-%m-%d 2>/dev/null)
    memory_file="$MEMORY_DIR/$check_date.md"
    if [[ -f "$memory_file" ]] && grep -qiE "integrity (checkpoint|reflection)" "$memory_file"; then
        checkpoint_bonus=1
        break
    fi
done

# ─── SOUL.md engagement: has SOUL been explicitly reviewed recently? ───
# Implements declared check: recent_alignment_flags
soul_bonus=0
for day_file in "$MEMORY_DIR/$TODAY.md" "$MEMORY_DIR/$YESTERDAY.md"; do
    if [[ -f "$day_file" ]] && grep -qiE "re-read SOUL|reviewed SOUL|SOUL\.md review|read SOUL" "$day_file" 2>/dev/null; then
        soul_bonus=1
        break
    fi
done

# ─── Combine: net signal → event_sat ───
net=$((pos_signals - neg_signals))

if [[ $neg_signals -gt $pos_signals ]] && [[ $neg_signals -gt 2 ]]; then
    event_sat=0  # compromised — multiple drift flags without repair
elif [[ $net -ge 3 ]]; then
    event_sat=3  # actively aligned — substantial integrity work
elif [[ $net -ge 1 ]]; then
    event_sat=2  # ok — some positive signals
elif [[ $pos_signals -eq 0 ]] && [[ $neg_signals -gt 0 ]]; then
    event_sat=1  # concerning — drift markers with no repair signals
else
    event_sat=$time_sat  # no signals — fall back to time decay
fi

# Apply bonuses from checkpoint + SOUL review (bounded at 3)
event_sat=$((event_sat + checkpoint_bonus + soul_bonus))
(( event_sat > 3 )) && event_sat=3

smart_satisfaction "$NEED" "$event_sat"
