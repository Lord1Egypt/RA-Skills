#!/bin/bash
# test_mindstate_daemon.sh — Unit tests for mindstate-daemon.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
DAEMON="$SKILL_DIR/scripts/mindstate-daemon.sh"
CONFIG_FILE="$SKILL_DIR/assets/needs-config.json"
FIXTURES="$(dirname "$SCRIPT_DIR")/fixtures"

errors=0
pass() { echo "  ✓ $1"; }
fail() { echo "  ✗ $1"; ((errors++)) || true; }

# Isolated test environment — never touches real state
TEST_WORKSPACE=$(mktemp -d /tmp/tp_mindstate_daemon_XXXXXX)
TEST_ASSETS=$(mktemp -d /tmp/tp_mindstate_assets_XXXXXX)
export WORKSPACE="$TEST_WORKSPACE"
export MINDSTATE_ASSETS_DIR="$TEST_ASSETS"

# Create minimal workspace
mkdir -p "$TEST_WORKSPACE/memory" "$TEST_WORKSPACE/research"
echo "# test" > "$TEST_WORKSPACE/INTENTIONS.md"

# Copy config + state to isolated assets
cp "$SKILL_DIR/assets/needs-config.json" "$TEST_ASSETS/"
cp "$SKILL_DIR/assets/decay-config.json" "$TEST_ASSETS/" 2>/dev/null || true
cp "$SKILL_DIR/assets/mindstate-config.json" "$TEST_ASSETS/" 2>/dev/null || true
cp "$FIXTURES/needs-state-healthy.json" "$TEST_ASSETS/needs-state.json"
touch "$TEST_ASSETS/audit.log"

STATE_FILE="$TEST_ASSETS/needs-state.json"

# Set all timestamps to now for predictable decay
now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
for need in security integrity coherence closure autonomy connection competence understanding recognition expression; do
    jq --arg n "$need" --arg t "$now" '
        .[$n].last_decay_check = $t |
        .[$n].last_satisfied = $t |
        .[$n].satisfaction = 2.5 |
        .[$n].surplus = 0 |
        .[$n].last_spontaneous_at = "1970-01-01T00:00:00Z"
    ' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
done

cleanup() {
    rm -rf "$TEST_WORKSPACE" "$TEST_ASSETS"
}
trap cleanup EXIT

echo "=== mindstate-daemon tests ==="

# ─── Test 1: Creates MINDSTATE on first run ───
echo "Test 1: Creates MINDSTATE on first run"
rm -f "$TEST_WORKSPACE/MINDSTATE.md"
rm -f "$TEST_ASSETS/mindstate.lock"
bash "$DAEMON" 2>/dev/null
if [[ -f "$TEST_WORKSPACE/MINDSTATE.md" ]]; then
    pass "MINDSTATE.md created"
else
    fail "MINDSTATE.md not created"
fi

# ─── Test 2: Contains all three sections ───
echo "Test 2: Contains all three sections"
grep -q "^## reality" "$TEST_WORKSPACE/MINDSTATE.md" && pass "## reality present" || fail "## reality missing"
grep -q "^## cognition" "$TEST_WORKSPACE/MINDSTATE.md" && pass "## cognition present" || fail "## cognition missing"
grep -q "^## forecast" "$TEST_WORKSPACE/MINDSTATE.md" && pass "## forecast present" || fail "## forecast missing"

# ─── Test 3: All 10 needs in pyramid_snapshot ───
echo "Test 3: All 10 needs in pyramid_snapshot"
for need in security integrity coherence closure autonomy connection competence understanding recognition expression; do
    grep -q "  $need:" "$TEST_WORKSPACE/MINDSTATE.md" && pass "$need present" || fail "$need missing"
done

# ─── Test 4: Trend arrows present ───
echo "Test 4: Trend arrows present"
trend_count=$(grep -cE "  [a-z]+: [0-9.]+ [↑↓→]" "$TEST_WORKSPACE/MINDSTATE.md" || true)
(( trend_count == 10 )) && pass "All 10 needs have trend arrows" || fail "Expected 10, got $trend_count"

# ─── Test 5: Physical temperature valid ───
echo "Test 5: Physical temperature valid"
temp=$(grep "^physical_temperature:" "$TEST_WORKSPACE/MINDSTATE.md" | sed 's/physical_temperature: *//')
case "$temp" in
    crisis|pressure|focus|impulse|accumulation|calm) pass "temperature '$temp' is valid" ;;
    *) fail "temperature '$temp' is not in vocabulary" ;;
esac

# ─── Test 6: Self-throttle skips if recent ───
echo "Test 6: Self-throttle"
mtime_before=$(stat -c %Y "$TEST_WORKSPACE/MINDSTATE.md")
sleep 1
bash "$DAEMON" 2>/dev/null
mtime_after=$(stat -c %Y "$TEST_WORKSPACE/MINDSTATE.md")
[[ "$mtime_before" == "$mtime_after" ]] && pass "Throttled" || fail "Not throttled"

# ─── Test 7: Updates reality, preserves cognition ───
echo "Test 7: Updates reality, preserves cognition"
cat > "$TEST_WORKSPACE/MINDSTATE.md" << 'EOF'
# MINDSTATE
## reality
timestamp: old
physical_temperature: calm

## cognition
frozen_at: 2026-01-01T00:00:00Z
trajectory: TEST_TRAJECTORY_MARKER
cognitive_temperature: building

## forecast
structural:
  - test prediction
EOF
touch -d "2026-01-01" "$TEST_WORKSPACE/MINDSTATE.md"
rm -f "$TEST_ASSETS/mindstate.lock"
bash "$DAEMON" 2>/dev/null

grep -q "TEST_TRAJECTORY_MARKER" "$TEST_WORKSPACE/MINDSTATE.md" && pass "Cognition preserved" || fail "Cognition overwritten"
grep -q "test prediction" "$TEST_WORKSPACE/MINDSTATE.md" && pass "Forecast preserved" || fail "Forecast overwritten"
! grep -q "timestamp: old" "$TEST_WORKSPACE/MINDSTATE.md" && pass "Reality updated" || fail "Reality not updated"

# ─── Test 8: Critical needs detection ───
echo "Test 8: Critical needs detection"
jq '.connection.satisfaction = 0.5 | .connection.last_decay_check = "2026-03-18T00:00:00Z"' \
    "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
touch -d "2026-01-01" "$TEST_WORKSPACE/MINDSTATE.md"
rm -f "$TEST_ASSETS/mindstate.lock"
bash "$DAEMON" 2>/dev/null
grep -q "critical_needs:.*connection" "$TEST_WORKSPACE/MINDSTATE.md" && pass "Connection critical" || fail "Not detected"

# Restore
for need in security integrity coherence closure autonomy connection competence understanding recognition expression; do
    jq --arg n "$need" --arg t "$now" '.[$n].last_decay_check = $t | .[$n].last_satisfied = $t | .[$n].satisfaction = 2.5 | .[$n].surplus = 0 | .[$n].last_spontaneous_at = "1970-01-01T00:00:00Z"' \
        "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
done

# ─── Test 9: Temperature crisis priority ───
echo "Test 9: Temperature crisis priority"
jq '.connection.satisfaction = 0.3' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
touch -d "2026-01-01" "$TEST_WORKSPACE/MINDSTATE.md"
rm -f "$TEST_ASSETS/mindstate.lock"
bash "$DAEMON" 2>/dev/null
temp=$(grep "^physical_temperature:" "$TEST_WORKSPACE/MINDSTATE.md" | sed 's/physical_temperature: *//')
[[ "$temp" == "crisis" ]] && pass "crisis when critical" || fail "'$temp', expected crisis"

# Restore
for need in security integrity coherence closure autonomy connection competence understanding recognition expression; do
    jq --arg n "$need" --arg t "$now" '.[$n].last_decay_check = $t | .[$n].last_satisfied = $t | .[$n].satisfaction = 2.5 | .[$n].surplus = 0 | .[$n].last_spontaneous_at = "1970-01-01T00:00:00Z"' \
        "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
done

# ─── Test 10: Environment delta ───
echo "Test 10: Environment delta"
touch -d "2026-01-01" "$TEST_WORKSPACE/MINDSTATE.md"
touch "$TEST_WORKSPACE/memory/test-new.md"
touch "$TEST_WORKSPACE/research/test-new.txt"
rm -f "$TEST_ASSETS/mindstate.lock"
bash "$DAEMON" 2>/dev/null
grep -q "memory_activity: 1" "$TEST_WORKSPACE/MINDSTATE.md" && pass "Memory activity" || fail "Memory not detected"
grep -q "research_activity: 1" "$TEST_WORKSPACE/MINDSTATE.md" && pass "Research activity" || fail "Research not detected"

# ─── Test 11: Stale files detection ───
echo "Test 11: Stale files detection"
touch -d "2026-03-01" "$TEST_WORKSPACE/INTENTIONS.md"
touch -d "2026-01-01" "$TEST_WORKSPACE/MINDSTATE.md"
rm -f "$TEST_ASSETS/mindstate.lock"
bash "$DAEMON" 2>/dev/null
grep -q "stale_files:.*INTENTIONS.md" "$TEST_WORKSPACE/MINDSTATE.md" && pass "Stale detected" || fail "Not detected"

# ─── Test 12: Temporal phase ───
echo "Test 12: Temporal phase present"
grep -q "phase:" "$TEST_WORKSPACE/MINDSTATE.md" && pass "Phase present" || fail "Phase missing"

# ─── Test 13: Atomic write ───
echo "Test 13: Atomic write"
header=$(head -1 "$TEST_WORKSPACE/MINDSTATE.md")
[[ "$header" == "# MINDSTATE" ]] && pass "Header intact" || fail "Header corrupted"
section_count=$(grep -c "^## " "$TEST_WORKSPACE/MINDSTATE.md" || true)
(( section_count == 3 )) && pass "3 sections" || fail "$section_count sections"

# ─── Test 14: Daemon does NOT clean orphans (watchdog's job) ───
echo "Test 14: Daemon leaves orphans for watchdog"
touch -d "2026-01-01" "$TEST_ASSETS/stale.tmp.12345"
touch -d "2026-01-01" "$TEST_WORKSPACE/stale.tmp.67890"
touch -d "2026-01-01" "$TEST_WORKSPACE/MINDSTATE.md"
rm -f "$TEST_ASSETS/mindstate.lock"
bash "$DAEMON" 2>/dev/null
# Daemon should NOT delete orphans — that's the watchdog's responsibility
[[ -f "$TEST_ASSETS/stale.tmp.12345" ]] && pass "Assets orphan preserved (watchdog's job)" || fail "Daemon deleted orphan"
[[ -f "$TEST_WORKSPACE/stale.tmp.67890" ]] && pass "Workspace orphan preserved (watchdog's job)" || fail "Daemon deleted orphan"
# Clean up for remaining tests
rm -f "$TEST_ASSETS/stale.tmp.12345" "$TEST_WORKSPACE/stale.tmp.67890"

# ─── Test 15: Stale cognition detection ───
echo "Test 15: Stale cognition detection"
# Set frozen_at to 48 hours ago
old_frozen=$(date -u -d "48 hours ago" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null)
cat > "$TEST_WORKSPACE/MINDSTATE.md" << EOF
# MINDSTATE
## reality
timestamp: old

## cognition
frozen_at: $old_frozen
trajectory: test

## forecast
structural: []
EOF
touch -d "2026-01-01" "$TEST_WORKSPACE/MINDSTATE.md"
rm -f "$TEST_ASSETS/mindstate.lock"
bash "$DAEMON" 2>/dev/null
grep -q "cognition:.*stale" "$TEST_WORKSPACE/MINDSTATE.md" && pass "Stale cognition flagged" || fail "Not flagged"

# ─── Test 16: No stale flag when cognition fresh ───
echo "Test 16: No stale flag when fresh"
fresh_frozen=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat > "$TEST_WORKSPACE/MINDSTATE.md" << EOF
# MINDSTATE
## reality
timestamp: old

## cognition
frozen_at: $fresh_frozen
trajectory: test

## forecast
structural: []
EOF
touch -d "2026-01-01" "$TEST_WORKSPACE/MINDSTATE.md"
rm -f "$TEST_ASSETS/mindstate.lock"
bash "$DAEMON" 2>/dev/null
grep -q "cognition:.*stale" "$TEST_WORKSPACE/MINDSTATE.md" && fail "False stale flag" || pass "No stale flag"

echo ""
if [[ $errors -eq 0 ]]; then echo "All daemon tests PASSED"; exit 0
else echo "Daemon tests: $errors FAILED"; exit 1; fi
