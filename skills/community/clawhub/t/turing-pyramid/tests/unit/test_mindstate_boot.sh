#!/bin/bash
# test_mindstate_boot.sh — Unit tests for mindstate-boot.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
BOOT="$SKILL_DIR/scripts/mindstate-boot.sh"
FIXTURES="$(dirname "$SCRIPT_DIR")/fixtures"

errors=0
pass() { echo "  ✓ $1"; }
fail() { echo "  ✗ $1"; ((errors++)) || true; }

TEST_WORKSPACE=$(mktemp -d /tmp/tp_boot_XXXXXX)
TEST_ASSETS=$(mktemp -d /tmp/tp_boot_assets_XXXXXX)
export WORKSPACE="$TEST_WORKSPACE"
export MINDSTATE_ASSETS_DIR="$TEST_ASSETS"

mkdir -p "$TEST_WORKSPACE/memory"

# Isolated state
cp "$SKILL_DIR/assets/needs-config.json" "$TEST_ASSETS/"
cp "$SKILL_DIR/assets/decay-config.json" "$TEST_ASSETS/" 2>/dev/null || true
cp "$SKILL_DIR/assets/mindstate-config.json" "$TEST_ASSETS/" 2>/dev/null || true
cp "$FIXTURES/needs-state-healthy.json" "$TEST_ASSETS/needs-state.json"
touch "$TEST_ASSETS/audit.log"

STATE_FILE="$TEST_ASSETS/needs-state.json"
now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
for need in security integrity coherence closure autonomy connection competence understanding recognition expression; do
    jq --arg n "$need" --arg t "$now" '.[$n].last_decay_check = $t | .[$n].last_satisfied = $t | .[$n].satisfaction = 2.5 | .[$n].surplus = 15 | .[$n].last_spontaneous_at = "1970-01-01T00:00:00Z"' \
        "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
done

cleanup() { rm -rf "$TEST_WORKSPACE" "$TEST_ASSETS"; }
trap cleanup EXIT

# Helper: write MINDSTATE and touch to now so daemon self-throttles
wms() { cat > "$TEST_WORKSPACE/MINDSTATE.md"; touch "$TEST_WORKSPACE/MINDSTATE.md"; }

echo "=== mindstate-boot tests ==="

# ─── Test 1: First boot (no MINDSTATE) ───
echo "Test 1: First boot"
rm -f "$TEST_WORKSPACE/MINDSTATE.md" "$TEST_ASSETS/mindstate.lock"
output=$(bash "$BOOT" 2>&1)
echo "$output" | grep -qi "first" && pass "First boot detected" || fail "Not detected"
[[ -f "$TEST_WORKSPACE/MINDSTATE.md" ]] && pass "MINDSTATE created" || fail "Not created"

# ─── Test 2: Smooth transition (aligned temperatures) ───
echo "Test 2: Smooth transition"
wms << 'EOF'
# MINDSTATE
## reality
timestamp: 2026-03-18T03:00:00Z
last_session_end: 2026-03-18T02:00:00Z
hours_elapsed: 1.0
physical_temperature: calm
critical_needs: none
surplus_gate: OPEN

## cognition
frozen_at: 2026-03-18T02:00:00Z
trajectory: testing boot
cognitive_temperature: calm

## forecast
structural:
  - (no near-term predictions)
semantic:
  - (mechanical only)
EOF
rm -f "$TEST_ASSETS/mindstate.lock"
output=$(bash "$BOOT" 2>&1)
echo "$output" | grep -q "SMOOTH" && pass "SMOOTH transition" || fail "$(echo "$output" | grep Transition)"
! echo "$output" | grep -q "DRIFT" && pass "No false drift" || fail "False drift"

# ─── Test 3: Temperature drift detection ───
echo "Test 3: Temperature drift"
jq '.connection.satisfaction = 0.4' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
wms << 'EOF'
# MINDSTATE
## reality
timestamp: 2026-03-18T08:00:00Z
last_session_end: 2026-03-18T02:00:00Z
hours_elapsed: 6.0
physical_temperature: crisis
critical_needs: connection
surplus_gate: CLOSED

## cognition
frozen_at: 2026-03-18T02:00:00Z
trajectory: deep building
cognitive_temperature: building

## forecast
structural:
  - connection < 1.0 within 4.0h
semantic:
  - (mechanical only)
EOF
rm -f "$TEST_ASSETS/mindstate.lock"
output=$(bash "$BOOT" 2>&1)
echo "$output" | grep -q "TEMPERATURE DRIFT" && pass "Drift detected" || fail "Not detected"
echo "$output" | grep -q "Temperature: crisis" && pass "Merged = physical" || fail "$(echo "$output" | grep Temperature)"
# Restore
jq '.connection.satisfaction = 2.5' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

# ─── Test 4: Confirmed prediction ───
echo "Test 4: Confirmed prediction"
# connection.sat = 0.4 in state, forecast says < 1.0 → CONFIRMED
jq '.connection.satisfaction = 0.4' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
wms << 'EOF'
# MINDSTATE
## reality
timestamp: 2026-03-18T08:00:00Z
last_session_end: 2026-03-18T02:00:00Z
hours_elapsed: 4.0
physical_temperature: crisis
critical_needs: connection
surplus_gate: CLOSED

## cognition
frozen_at: 2026-03-18T02:00:00Z
trajectory: research
cognitive_temperature: building

## forecast
structural:
  - connection < 1.0 within 4.0h
semantic:
  - (mechanical only)
EOF
rm -f "$TEST_ASSETS/mindstate.lock"
output=$(bash "$BOOT" 2>&1)
echo "$output" | grep -q "✓.*connection.*CONFIRMED" && pass "Confirmed" || fail "$(echo "$output" | grep connection)"
jq '.connection.satisfaction = 2.5' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

# ─── Test 5: Staleness STALE (>24h) ───
echo "Test 5: Staleness STALE (>24h)"
wms << 'EOF'
# MINDSTATE
## reality
timestamp: 2026-03-18T08:00:00Z
last_session_end: 2026-03-17T00:00:00Z
hours_elapsed: 32.0
physical_temperature: calm
critical_needs: none
surplus_gate: OPEN

## cognition
frozen_at: 2026-03-17T00:00:00Z
trajectory: old work
cognitive_temperature: neutral

## forecast
structural:
  - (no near-term predictions)
semantic:
  - (mechanical only)
EOF
rm -f "$TEST_ASSETS/mindstate.lock"
output=$(bash "$BOOT" 2>&1)
echo "$output" | grep -q "STALE COGNITION" && pass "Stale at 32h" || fail "Not detected"
echo "$output" | grep -q "Cognition trust: PARTIAL" && pass "Trust=PARTIAL" || fail "$(echo "$output" | grep trust)"

# ─── Test 6: Very stale (>48h) ───
echo "Test 6: Very stale (>48h)"
wms << 'EOF'
# MINDSTATE
## reality
timestamp: 2026-03-18T08:00:00Z
last_session_end: 2026-03-16T00:00:00Z
hours_elapsed: 52.0
physical_temperature: calm
critical_needs: none
surplus_gate: OPEN

## cognition
frozen_at: 2026-03-16T00:00:00Z
trajectory: old work
cognitive_temperature: neutral

## forecast
structural:
  - (no near-term predictions)
semantic:
  - (mechanical only)
EOF
rm -f "$TEST_ASSETS/mindstate.lock"
output=$(bash "$BOOT" 2>&1)
echo "$output" | grep -q "Cognition trust: MINIMAL" && pass "Trust=MINIMAL at 52h" || fail "$(echo "$output" | grep trust)"

# ─── Test 7: Boot log created ───
echo "Test 7: Boot log"
[[ -f "$TEST_ASSETS/mindstate-boot.log" ]] && {
    n=$(wc -l < "$TEST_ASSETS/mindstate-boot.log")
    (( n >= 1 )) && pass "Boot log: $n entries" || fail "Empty"
} || fail "Not created"

# ─── Test 8: Open threads displayed ───
echo "Test 8: Open threads"
wms << 'EOF'
# MINDSTATE
## reality
timestamp: 2026-03-18T08:00:00Z
last_session_end: 2026-03-18T07:00:00Z
hours_elapsed: 1.0
physical_temperature: calm
critical_needs: none
surplus_gate: OPEN

## cognition
frozen_at: 2026-03-18T07:00:00Z
trajectory: writing tests
open_threads:
  - Build continuity layer
  - Write mindstate tests
cognitive_temperature: building

## forecast
structural:
  - (no near-term predictions)
semantic:
  - (mechanical only)
EOF
rm -f "$TEST_ASSETS/mindstate.lock"
output=$(bash "$BOOT" 2>&1)
echo "$output" | grep -q "Build continuity layer" && pass "Threads shown" || fail "Not shown"

# ─── Test 9: Continuity score ───
echo "Test 9: Continuity score"
echo "$output" | grep -q "score:" && {
    score=$(echo "$output" | grep "score:" | grep -oP '[0-9]+\.[0-9]+')
    pass "score=$score"
} || fail "No score"

# ─── Test 10: Boot header ───
echo "Test 10: Boot header"
echo "$output" | grep -q "CONTINUITY BOOT" && pass "Header present" || fail "Missing"

echo ""
if [[ $errors -eq 0 ]]; then echo "All boot tests PASSED"; exit 0
else echo "Boot tests: $errors FAILED"; exit 1; fi
