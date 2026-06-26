#!/bin/bash
# test_watchdog.sh — Unit tests for mindstate-watchdog.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
WATCHDOG="$SKILL_DIR/scripts/mindstate-watchdog.sh"
DAEMON="$SKILL_DIR/scripts/mindstate-daemon.sh"
FREEZE="$SKILL_DIR/scripts/mindstate-freeze.sh"
FIXTURES="$(dirname "$SCRIPT_DIR")/fixtures"

errors=0
pass() { echo "  ✓ $1"; }
fail() { echo "  ✗ $1"; ((errors++)) || true; }

# Isolated test environment
TEST_WORKSPACE=$(mktemp -d /tmp/tp_watchdog_XXXXXX)
TEST_ASSETS=$(mktemp -d /tmp/tp_watchdog_assets_XXXXXX)
export WORKSPACE="$TEST_WORKSPACE"
export MINDSTATE_ASSETS_DIR="$TEST_ASSETS"

mkdir -p "$TEST_WORKSPACE/memory" "$TEST_WORKSPACE/research"
echo "# test" > "$TEST_WORKSPACE/INTENTIONS.md"

# Copy configs to isolated assets
cp "$SKILL_DIR/assets/needs-config.json" "$TEST_ASSETS/"
cp "$SKILL_DIR/assets/decay-config.json" "$TEST_ASSETS/" 2>/dev/null || true
cp "$SKILL_DIR/assets/mindstate-config.json" "$TEST_ASSETS/" 2>/dev/null || true
cp "$FIXTURES/needs-state-healthy.json" "$TEST_ASSETS/needs-state.json"
touch "$TEST_ASSETS/audit.log"

STATE_FILE="$TEST_ASSETS/needs-state.json"
now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
for need in security integrity coherence closure autonomy connection competence understanding recognition expression; do
    jq --arg n "$need" --arg t "$now" \
        '.[$n].last_decay_check = $t | .[$n].last_satisfied = $t | .[$n].satisfaction = 2.5 | .[$n].surplus = 0 | .[$n].last_spontaneous_at = "1970-01-01T00:00:00Z"' \
        "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
done

cleanup() { rm -rf "$TEST_WORKSPACE" "$TEST_ASSETS"; }
trap cleanup EXIT

# Create initial MINDSTATE via daemon
rm -f "$TEST_ASSETS/mindstate.lock"
bash "$DAEMON" 2>/dev/null

# Ensure cognition has a fresh frozen_at (daemon creates "never" on first run)
fresh_ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
sed -i "s/^frozen_at:.*/frozen_at: $fresh_ts/" "$TEST_WORKSPACE/MINDSTATE.md"

echo "=== watchdog tests ==="

# ─── Test 1: Silent when healthy ───
echo "Test 1: Silent when healthy"
output=$(bash "$WATCHDOG" 2>&1)
[[ -z "$output" ]] && pass "Silent when all healthy" || fail "Unexpected output: $output"

# ─── Test 2: No watchdog.log when healthy ───
echo "Test 2: No log when healthy"
[[ ! -f "$TEST_ASSETS/watchdog.log" ]] && pass "No log file" || {
    lines=$(wc -l < "$TEST_ASSETS/watchdog.log")
    [[ "$lines" -eq 0 ]] && pass "Empty log" || fail "Log has $lines lines"
}

# ─── Test 3: Detects stale MINDSTATE (dry-run) ───
echo "Test 3: Detects stale MINDSTATE"
touch -d "2026-01-01" "$TEST_WORKSPACE/MINDSTATE.md"
output=$(bash "$WATCHDOG" --dry-run 2>&1)
echo "$output" | grep -q "MINDSTATE.md stale" && pass "Stale detected" || fail "Not detected: $output"
echo "$output" | grep -q "DRY-RUN.*daemon restart" && pass "Restart proposed" || fail "No restart proposed"
# Restore freshness
rm -f "$TEST_ASSETS/mindstate.lock"
bash "$DAEMON" 2>/dev/null

# ─── Test 4: Orphan detection (default: log only, no delete) ───
echo "Test 4: Orphan detection (allow_cleanup=false)"
# Force allow_cleanup=false for this test (real config may have it enabled)
jq '.watchdog.allow_cleanup = false' "$TEST_ASSETS/mindstate-config.json" > "$TEST_ASSETS/mindstate-config.json.tmp" \
    && mv "$TEST_ASSETS/mindstate-config.json.tmp" "$TEST_ASSETS/mindstate-config.json"
touch -d "2026-01-01" "$TEST_ASSETS/somefile.tmp.99999"
touch -d "2026-01-01" "$TEST_WORKSPACE/otherfile.tmp.88888"
rm -f "$TEST_ASSETS/watchdog.log"
bash "$WATCHDOG" 2>&1 >/dev/null
# Default: detect only, files should still exist
[[ -f "$TEST_ASSETS/somefile.tmp.99999" ]] && pass "Assets orphan preserved (detect only)" || fail "Deleted without allow_cleanup"
[[ -f "$TEST_WORKSPACE/otherfile.tmp.88888" ]] && pass "Workspace orphan preserved (detect only)" || fail "Deleted without allow_cleanup"
grep -q "DETECT.*orphaned" "$TEST_ASSETS/watchdog.log" && pass "Detection logged" || fail "Not logged"

# ─── Test 4b: Orphan cleanup (allow_cleanup=true) ───
echo "Test 4b: Orphan cleanup (allow_cleanup=true)"
jq '.watchdog.allow_cleanup = true' "$TEST_ASSETS/mindstate-config.json" > "$TEST_ASSETS/mindstate-config.json.tmp" \
    && mv "$TEST_ASSETS/mindstate-config.json.tmp" "$TEST_ASSETS/mindstate-config.json"
bash "$WATCHDOG" 2>&1 >/dev/null
[[ ! -f "$TEST_ASSETS/somefile.tmp.99999" ]] && pass "Assets orphan cleaned" || fail "Not cleaned"
[[ ! -f "$TEST_WORKSPACE/otherfile.tmp.88888" ]] && pass "Workspace orphan cleaned" || fail "Not cleaned"
# Restore
jq '.watchdog.allow_cleanup = false' "$TEST_ASSETS/mindstate-config.json" > "$TEST_ASSETS/mindstate-config.json.tmp" \
    && mv "$TEST_ASSETS/mindstate-config.json.tmp" "$TEST_ASSETS/mindstate-config.json"

# ─── Test 5: Auto-freeze stale cognition (dry-run) ───
echo "Test 5: Auto-freeze stale cognition (dry-run)"
# Set frozen_at to 12 hours ago (threshold is 6h)
old_frozen=$(date -u -d "12 hours ago" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%SZ")
sed -i "s/^frozen_at:.*/frozen_at: $old_frozen/" "$TEST_WORKSPACE/MINDSTATE.md"
output=$(bash "$WATCHDOG" --dry-run 2>&1)
echo "$output" | grep -q "auto-freeze" && pass "Auto-freeze proposed" || fail "Not proposed: $output"

# ─── Test 6: Auto-freeze actually runs ───
echo "Test 6: Auto-freeze executes"
# Set frozen_at to 12 hours ago
sed -i "s/^frozen_at:.*/frozen_at: $old_frozen/" "$TEST_WORKSPACE/MINDSTATE.md"
rm -f "$TEST_ASSETS/watchdog.log"
bash "$WATCHDOG" 2>&1 >/dev/null
frozen_now=$(grep "^frozen_at:" "$TEST_WORKSPACE/MINDSTATE.md" | head -1 | sed 's/frozen_at: *//')
[[ "$frozen_now" != "$old_frozen" ]] && pass "Cognition re-frozen (now: $frozen_now)" || fail "Still stale: $frozen_now"

# ─── Test 7: No auto-freeze when fresh ───
echo "Test 7: No auto-freeze when cognition fresh"
rm -f "$TEST_ASSETS/watchdog.log"
output=$(bash "$WATCHDOG" 2>&1)
[[ -z "$output" ]] && pass "Silent (cognition fresh)" || fail "Unexpected: $output"

# ─── Test 8: Auto-freeze respects config ───
echo "Test 8: Auto-freeze disabled by config"
# Disable auto_freeze in config
jq '.watchdog.auto_freeze = false' "$TEST_ASSETS/mindstate-config.json" > "$TEST_ASSETS/mindstate-config.json.tmp" \
    && mv "$TEST_ASSETS/mindstate-config.json.tmp" "$TEST_ASSETS/mindstate-config.json"
sed -i "s/^frozen_at:.*/frozen_at: $old_frozen/" "$TEST_WORKSPACE/MINDSTATE.md"
rm -f "$TEST_ASSETS/watchdog.log"
output=$(bash "$WATCHDOG" --dry-run 2>&1)
echo "$output" | grep -q "auto-freeze" && fail "Should be disabled" || pass "Auto-freeze disabled"
# Re-enable
jq '.watchdog.auto_freeze = true' "$TEST_ASSETS/mindstate-config.json" > "$TEST_ASSETS/mindstate-config.json.tmp" \
    && mv "$TEST_ASSETS/mindstate-config.json.tmp" "$TEST_ASSETS/mindstate-config.json"

# ─── Test 9: Watchdog log rotation ───
echo "Test 9: Log rotation"
# Create oversized log
for i in $(seq 1 210); do
    echo "[test] line $i" >> "$TEST_ASSETS/watchdog.log"
done
lines_before=$(wc -l < "$TEST_ASSETS/watchdog.log")
(( lines_before > 200 )) && pass "Log oversized ($lines_before lines)" || fail "Not oversized"
# Trigger watchdog (needs something to log for rotation to matter)
touch -d "2026-01-01" "$TEST_WORKSPACE/MINDSTATE.md"
bash "$WATCHDOG" 2>&1 >/dev/null
lines_after=$(wc -l < "$TEST_ASSETS/watchdog.log")
(( lines_after < lines_before )) && pass "Rotated (now $lines_after lines)" || fail "Not rotated ($lines_after)"
# Restore
rm -f "$TEST_ASSETS/mindstate.lock"
bash "$DAEMON" 2>/dev/null

# ─── Test 10: Dry-run never modifies state ───
echo "Test 10: Dry-run is read-only"
frozen_before=$(grep "^frozen_at:" "$TEST_WORKSPACE/MINDSTATE.md" | head -1 | sed 's/frozen_at: *//')
sed -i "s/^frozen_at:.*/frozen_at: $old_frozen/" "$TEST_WORKSPACE/MINDSTATE.md"
rm -f "$TEST_ASSETS/watchdog.log"
bash "$WATCHDOG" --dry-run 2>&1 >/dev/null
frozen_after=$(grep "^frozen_at:" "$TEST_WORKSPACE/MINDSTATE.md" | head -1 | sed 's/frozen_at: *//')
[[ "$frozen_after" == "$old_frozen" ]] && pass "Dry-run didn't modify frozen_at" || fail "Modified!"
# Restore
sed -i "s/^frozen_at:.*/frozen_at: $frozen_before/" "$TEST_WORKSPACE/MINDSTATE.md"

echo ""
if [[ $errors -eq 0 ]]; then echo "All watchdog tests PASSED"; exit 0
else echo "Watchdog tests: $errors FAILED"; exit 1; fi
