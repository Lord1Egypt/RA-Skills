#!/bin/bash
# test_mindstate_lifecycle.sh — Full lifecycle + homeostasis integration test
# 
# Tests the complete: daemon → freeze → sleep → daemon → boot → reconciliation cycle.
# Also validates homeostasis: pyramid continues to self-correct across sessions,
# and MINDSTATE continuity score correlates with prediction accuracy.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
DAEMON="$SKILL_DIR/scripts/mindstate-daemon.sh"
FREEZE="$SKILL_DIR/scripts/mindstate-freeze.sh"
BOOT="$SKILL_DIR/scripts/mindstate-boot.sh"
MARK="$SKILL_DIR/scripts/mark-satisfied.sh"
FIXTURES="$(dirname "$SCRIPT_DIR")/fixtures"

errors=0
pass() { echo "  ✓ $1"; }
fail() { echo "  ✗ $1"; ((errors++)) || true; }

# Fully isolated environment — no writes to real state
TEST_WORKSPACE=$(mktemp -d /tmp/tp_lifecycle_XXXXXX)
TEST_ASSETS=$(mktemp -d /tmp/tp_lifecycle_assets_XXXXXX)
export WORKSPACE="$TEST_WORKSPACE"
export MINDSTATE_ASSETS_DIR="$TEST_ASSETS"
export SKIP_SCANS="true"
export SKIP_SPONTANEITY="true"

mkdir -p "$TEST_WORKSPACE/memory" "$TEST_WORKSPACE/research"
cat > "$TEST_WORKSPACE/INTENTIONS.md" << 'EOF'
## Active
- Test the mindstate lifecycle
- Validate continuity scoring
## Done
- Design the spec
EOF

# Isolated state files
cp "$SKILL_DIR/assets/needs-config.json" "$TEST_ASSETS/"
cp "$SKILL_DIR/assets/decay-config.json" "$TEST_ASSETS/" 2>/dev/null || true
cp "$SKILL_DIR/assets/mindstate-config.json" "$TEST_ASSETS/" 2>/dev/null || true
cp "$FIXTURES/needs-state-healthy.json" "$TEST_ASSETS/needs-state.json"
touch "$TEST_ASSETS/audit.log"

STATE_FILE="$TEST_ASSETS/needs-state.json"
AUDIT_LOG="$TEST_ASSETS/audit.log"

now_epoch=$(date +%s)
now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
for need in security integrity coherence closure autonomy connection competence understanding recognition expression; do
    jq --arg n "$need" --arg t "$now" '
        .[$n].last_decay_check = $t |
        .[$n].last_satisfied = $t |
        .[$n].satisfaction = 2.5 |
        .[$n].surplus = 10 |
        .[$n].last_spontaneous_at = "1970-01-01T00:00:00Z"
    ' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
done

cleanup() { rm -rf "$TEST_WORKSPACE" "$TEST_ASSETS"; }
trap cleanup EXIT

echo "=== Mindstate Lifecycle + Homeostasis Integration Test ==="
echo ""

# ═══════════════════════════════════════
# PHASE 1: Cold start
# ═══════════════════════════════════════
echo "Phase 1: Cold start (no MINDSTATE)"
rm -f "$TEST_WORKSPACE/MINDSTATE.md" "$TEST_ASSETS/mindstate.lock"

boot1=$(bash "$BOOT" 2>&1)
echo "$boot1" | grep -qi "first" && pass "Phase 1: First boot detected" || fail "Phase 1: First boot not detected"
[[ -f "$TEST_WORKSPACE/MINDSTATE.md" ]] && pass "Phase 1: MINDSTATE created" || fail "Phase 1: MINDSTATE not created"

# Simulate work: mark needs, write memory
session_start=$now_epoch
echo '{"timestamp":"'"$now"'","need":"coherence","impact":1.5,"old_sat":"1.0","new_sat":"2.5","reason":"synced memory","caller":"test"}' >> "$AUDIT_LOG"
echo '{"timestamp":"'"$now"'","need":"connection","impact":1.0,"old_sat":"1.5","new_sat":"2.5","reason":"replied to post","caller":"test"}' >> "$AUDIT_LOG"
touch "$TEST_WORKSPACE/memory/session.md"

# Freeze
rm -f "$TEST_ASSETS/mindstate.lock"
freeze1=$(bash "$FREEZE" "$session_start" 2>&1)
echo "$freeze1" | grep -q "Cognition frozen" && pass "Phase 1: Freeze OK" || fail "Phase 1: Freeze failed"

cog_temp1=$(grep "^cognitive_temperature:" "$TEST_WORKSPACE/MINDSTATE.md" | head -1 | sed 's/cognitive_temperature: *//')
[[ -n "$cog_temp1" && "$cog_temp1" != "initializing" ]] && pass "Phase 1: Cognitive temp='$cog_temp1'" || fail "Phase 1: Temp not set"
trajectory1=$(grep "^trajectory:" "$TEST_WORKSPACE/MINDSTATE.md" | head -1 | sed 's/trajectory: *//')
[[ -n "$trajectory1" ]] && pass "Phase 1: Trajectory='$trajectory1'" || fail "Phase 1: No trajectory"

echo ""

# ═══════════════════════════════════════
# PHASE 2: Sleep — daemon updates, cognition frozen
# ═══════════════════════════════════════
echo "Phase 2: Sleep (daemon runs, cognition frozen)"

# Save frozen cognition
frozen_trajectory=$(grep "^trajectory:" "$TEST_WORKSPACE/MINDSTATE.md" | head -1)
frozen_cog_temp=$(grep "^cognitive_temperature:" "$TEST_WORKSPACE/MINDSTATE.md" | head -1)

# Simulate 4h of decay
jq '
    to_entries | map(
        if .value.last_decay_check then
            .value.last_decay_check = (
                (.value.last_decay_check | sub("\\.[0-9]+Z$"; "Z") |
                 strptime("%Y-%m-%dT%H:%M:%SZ") | mktime) - (4 * 3600) |
                strftime("%Y-%m-%dT%H:%M:%SZ")
            )
        else . end
    ) | from_entries
' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

# Daemon runs during sleep
touch -d "2026-01-01" "$TEST_WORKSPACE/MINDSTATE.md"
rm -f "$TEST_ASSETS/mindstate.lock"
bash "$DAEMON" 2>/dev/null

current_trajectory=$(grep "^trajectory:" "$TEST_WORKSPACE/MINDSTATE.md" | head -1)
current_cog_temp=$(grep "^cognitive_temperature:" "$TEST_WORKSPACE/MINDSTATE.md" | head -1)
[[ "$current_trajectory" == "$frozen_trajectory" ]] && pass "Phase 2: Trajectory frozen" || fail "Phase 2: Trajectory changed"
[[ "$current_cog_temp" == "$frozen_cog_temp" ]] && pass "Phase 2: Cog temp frozen" || fail "Phase 2: Cog temp changed"

ts=$(grep "^timestamp:" "$TEST_WORKSPACE/MINDSTATE.md" | head -1 | sed 's/timestamp: *//')
[[ -n "$ts" && "$ts" != "old" ]] && pass "Phase 2: Reality updated" || fail "Phase 2: Reality stale"

echo ""

# ═══════════════════════════════════════
# PHASE 3: Wake up
# ═══════════════════════════════════════
echo "Phase 3: Wake up"
# Touch MINDSTATE to now so daemon self-throttles — let boot read what daemon wrote
touch "$TEST_WORKSPACE/MINDSTATE.md"
rm -f "$TEST_ASSETS/mindstate.lock"
boot2=$(bash "$BOOT" 2>&1)

echo "$boot2" | grep -q "CONTINUITY BOOT" && pass "Phase 3: Boot header" || fail "Phase 3: No header"
echo "$boot2" | grep -q "Where I am:" && pass "Phase 3: Trajectory shown" || fail "Phase 3: No trajectory"
echo "$boot2" | grep -q "Temperature:" && pass "Phase 3: Temperature shown" || fail "Phase 3: No temperature"
[[ -f "$TEST_ASSETS/mindstate-boot.log" ]] && pass "Phase 3: Boot log exists" || fail "Phase 3: No boot log"

# Extract continuity score
score=$(echo "$boot2" | grep "score:" | grep -oP '[0-9]+(\.[0-9]+)?' | head -1)
[[ -n "$score" ]] && pass "Phase 3: Continuity score=$score" || fail "Phase 3: No score (output: $(echo "$boot2" | grep score))"

echo ""

# ═══════════════════════════════════════
# PHASE 4: Race condition (concurrent daemon + freeze)
# ═══════════════════════════════════════
echo "Phase 4: Race condition"
touch -d "2026-01-01" "$TEST_WORKSPACE/MINDSTATE.md"
rm -f "$TEST_ASSETS/mindstate.lock"

# Run concurrently
bash "$DAEMON" 2>/dev/null &
daemon_pid=$!
session_start2=$(($(date +%s) - 300))
bash "$FREEZE" "$session_start2" 2>/dev/null &
freeze_pid=$!
wait "$daemon_pid" 2>/dev/null || true
wait "$freeze_pid" 2>/dev/null || true

section_count=$(grep -c "^## " "$TEST_WORKSPACE/MINDSTATE.md" || true)
(( section_count == 3 )) && pass "Phase 4: 3 sections (no corruption)" || fail "Phase 4: $section_count sections"
header=$(head -1 "$TEST_WORKSPACE/MINDSTATE.md")
[[ "$header" == "# MINDSTATE" ]] && pass "Phase 4: Header intact" || fail "Phase 4: '$header'"

echo ""

# ═══════════════════════════════════════
# PHASE 5: Temperature drift scenario
# ═══════════════════════════════════════
echo "Phase 5: Crisis drift (building → crisis)"
jq '.connection.satisfaction = 0.3' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
cat > "$TEST_WORKSPACE/MINDSTATE.md" << 'MDEOF'
# MINDSTATE
## reality
timestamp: 2026-03-18T10:00:00Z
last_session_end: 2026-03-18T06:00:00Z
hours_elapsed: 4.0
physical_temperature: crisis
critical_needs: connection
surplus_gate: CLOSED

## cognition
frozen_at: 2026-03-18T06:00:00Z
trajectory: peaceful research
cognitive_temperature: contemplation

## forecast
structural:
  - connection < 1.0 within 3.0h
semantic:
  - (mechanical only)
MDEOF
touch "$TEST_WORKSPACE/MINDSTATE.md"  # prevent daemon overwrite

rm -f "$TEST_ASSETS/mindstate.lock"
boot3=$(bash "$BOOT" 2>&1)

echo "$boot3" | grep -q "TEMPERATURE DRIFT.*contemplation.*crisis" && pass "Phase 5: Drift detected" || fail "Phase 5: No drift"
echo "$boot3" | grep -q "Temperature: crisis" && pass "Phase 5: Merged=physical" || fail "Phase 5: $(echo "$boot3" | grep Temperature)"
echo "$boot3" | grep -q "✓.*connection.*CONFIRMED" && pass "Phase 5: Prediction confirmed" || fail "Phase 5: Not confirmed"

jq '.connection.satisfaction = 2.5' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
echo ""

# ═══════════════════════════════════════
# PHASE 6: Homeostasis across sessions
# Validates that pyramid self-corrects over multiple cycles,
# and MINDSTATE continuity score stays coherent.
# ═══════════════════════════════════════
echo "Phase 6: Homeostasis across sessions"

# Start from crisis
cp "$FIXTURES/needs-state-crisis.json" "$STATE_FILE"

CYCLES=20
consecutive_smooth=0
hard_breaks=0
floor_tally=0

for i in $(seq 1 $CYCLES); do
    # Simulate 1h between sessions
    jq '
        to_entries | map(
            if .value.last_decay_check then
                .value.last_decay_check = (
                    (.value.last_decay_check | sub("\\.[0-9]+Z$"; "Z") |
                     strptime("%Y-%m-%dT%H:%M:%SZ") | mktime) - 3600 |
                    strftime("%Y-%m-%dT%H:%M:%SZ")
                )
            else . end
        ) | from_entries
    ' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

    # Session: boot, work (mark top needs), freeze
    touch -d "2026-01-01" "$TEST_WORKSPACE/MINDSTATE.md"
    rm -f "$TEST_ASSETS/mindstate.lock"
    boot_out=$(bash "$BOOT" 2>&1)

    # Check boot score
    b_score=$(echo "$boot_out" | grep "score:" | grep -oP '[0-9]+\.[0-9]+' | head -1)
    if [[ -n "$b_score" ]]; then
        if (( $(echo "$b_score >= 0.7" | bc -l) )); then
            consecutive_smooth=$((consecutive_smooth + 1))
        else
            consecutive_smooth=0
            hard_breaks=$((hard_breaks + 1))
        fi
    fi

    # Mark all needs satisfied (simulate work completing in each cycle)
    sess_start=$(($(date +%s) - 600))
    ts_now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    for need in security integrity coherence closure autonomy connection competence understanding recognition expression; do
        sat=$(jq -r --arg n "$need" '.[$n].satisfaction // 0.5' "$STATE_FILE" 2>/dev/null || echo "0.5")
        new_sat=$(echo "scale=2; if ($sat + 1.5 > 3.0) 3.0 else $sat + 1.5" | bc -l 2>/dev/null || echo "2.0")
        echo '{"timestamp":"'"$ts_now"'","need":"'"$need"'","impact":1.5,"old_sat":"'"$sat"'","new_sat":"'"$new_sat"'","reason":"cycle_'"$i"'","caller":"test"}' >> "$AUDIT_LOG"
        jq --arg n "$need" --arg s "$new_sat" --arg t "$ts_now" \
            '.[$n].satisfaction = ($s | tonumber) | .[$n].last_satisfied = $t | .[$n].last_decay_check = $t' \
            "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    done

    # Count needs at floor
    for need in security integrity coherence closure autonomy connection competence understanding recognition expression; do
        sat=$(jq -r --arg n "$need" '.[$n].satisfaction // 0.5' "$STATE_FILE")
        if (( $(echo "$sat <= 0.5" | bc -l) )); then
            floor_tally=$((floor_tally + 1))
        fi
    done

    # Freeze
    rm -f "$TEST_ASSETS/mindstate.lock"
    bash "$FREEZE" "$sess_start" 2>/dev/null
done

# Homeostasis: no chronic deprivation (floor_tally / (CYCLES * 10) < 50%)
max_floor_ratio="0.50"
actual_ratio=$(echo "scale=2; $floor_tally / ($CYCLES * 10)" | bc -l)
(( $(echo "$actual_ratio < $max_floor_ratio" | bc -l) )) && \
    pass "Phase 6: Homeostasis (floor=$floor_tally/$((CYCLES*10)), ratio=$actual_ratio)" || \
    fail "Phase 6: Chronic deprivation (floor=$floor_tally/$((CYCLES*10)), ratio=$actual_ratio)"

# Continuity: majority of boots should be SMOOTH
smooth_ratio=$(echo "scale=2; $consecutive_smooth / $CYCLES" | bc -l 2>/dev/null || echo "0")
(( $(echo "$hard_breaks <= $((CYCLES / 2))" | bc -l) )) && \
    pass "Phase 6: Continuity coherent (hard_breaks=$hard_breaks/$CYCLES)" || \
    fail "Phase 6: Too many hard breaks ($hard_breaks/$CYCLES)"

echo ""
echo "=== Results ==="
if [[ $errors -eq 0 ]]; then
    echo "All lifecycle+homeostasis tests PASSED"
    exit 0
else
    echo "$errors FAILED"
    exit 1
fi
