#!/bin/bash
# test_mindstate_freeze.sh — Unit tests for mindstate-freeze.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
FREEZE="$SKILL_DIR/scripts/mindstate-freeze.sh"
DAEMON="$SKILL_DIR/scripts/mindstate-daemon.sh"
FIXTURES="$(dirname "$SCRIPT_DIR")/fixtures"

errors=0
pass() { echo "  ✓ $1"; }
fail() { echo "  ✗ $1"; ((errors++)) || true; }

TEST_WORKSPACE=$(mktemp -d /tmp/tp_freeze_XXXXXX)
TEST_ASSETS=$(mktemp -d /tmp/tp_freeze_assets_XXXXXX)
export WORKSPACE="$TEST_WORKSPACE"
export MINDSTATE_ASSETS_DIR="$TEST_ASSETS"

mkdir -p "$TEST_WORKSPACE/memory" "$TEST_WORKSPACE/research"
echo "# test" > "$TEST_WORKSPACE/INTENTIONS.md"

# Isolated state
cp "$SKILL_DIR/assets/needs-config.json" "$TEST_ASSETS/"
cp "$SKILL_DIR/assets/decay-config.json" "$TEST_ASSETS/" 2>/dev/null || true
cp "$SKILL_DIR/assets/mindstate-config.json" "$TEST_ASSETS/" 2>/dev/null || true
cp "$FIXTURES/needs-state-healthy.json" "$TEST_ASSETS/needs-state.json"
touch "$TEST_ASSETS/audit.log"

STATE_FILE="$TEST_ASSETS/needs-state.json"
AUDIT_LOG="$TEST_ASSETS/audit.log"
now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
for need in security integrity coherence closure autonomy connection competence understanding recognition expression; do
    jq --arg n "$need" --arg t "$now" '.[$n].last_decay_check = $t | .[$n].last_satisfied = $t | .[$n].satisfaction = 2.5 | .[$n].surplus = 15 | .[$n].last_spontaneous_at = "1970-01-01T00:00:00Z"' \
        "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
done

cleanup() { rm -rf "$TEST_WORKSPACE" "$TEST_ASSETS"; }
trap cleanup EXIT

# Create initial MINDSTATE via daemon
rm -f "$TEST_ASSETS/mindstate.lock"
bash "$DAEMON" 2>/dev/null

echo "=== mindstate-freeze tests ==="

# ─── Test 1: Skips non-substantive session ───
echo "Test 1: Skips non-substantive session"
session_start=$(($(date +%s) - 10))
echo "" > "$AUDIT_LOG"
output=$(bash "$FREEZE" "$session_start" 2>&1)
echo "$output" | grep -q "not substantive" && pass "Skipped" || fail "Not skipped"

# ─── Test 2: Processes substantive session (duration >120s) ───
echo "Test 2: Processes substantive session"
session_start=$(($(date +%s) - 300))
output=$(bash "$FREEZE" "$session_start" 2>&1)
echo "$output" | grep -q "Cognition frozen" && pass "Processed" || fail "Not processed"

# ─── Test 3: frozen_at updated ───
echo "Test 3: frozen_at updated"
frozen_at=$(grep "^frozen_at:" "$TEST_WORKSPACE/MINDSTATE.md" | head -1 | sed 's/frozen_at: *//')
[[ "$frozen_at" != "never" && -n "$frozen_at" ]] && pass "frozen_at='$frozen_at'" || fail "Not updated"

# ─── Test 4: Cognitive temperature valid ───
echo "Test 4: Cognitive temperature valid"
cog_temp=$(grep "^cognitive_temperature:" "$TEST_WORKSPACE/MINDSTATE.md" | head -1 | sed 's/cognitive_temperature: *//')
case "$cog_temp" in
    building|exploring|intensive|contemplation|brief|neutral) pass "'$cog_temp'" ;;
    *) fail "'$cog_temp' invalid" ;;
esac

# ─── Test 5: Reality preserved ───
echo "Test 5: Reality preserved after freeze"
grep -q "^## reality" "$TEST_WORKSPACE/MINDSTATE.md" && pass "Reality present" || fail "Missing"
grep -q "pyramid_snapshot:" "$TEST_WORKSPACE/MINDSTATE.md" && pass "Pyramid in reality" || fail "Missing"

# ─── Test 6: Trajectory from audit ───
echo "Test 6: Trajectory from audit"
session_start=$(($(date +%s) - 600))
cat >> "$AUDIT_LOG" << EOF
{"timestamp":"$now","need":"coherence","impact":1.5,"old_sat":"1.5","new_sat":"3.00","reason":"synced memory","caller":"manual"}
{"timestamp":"$now","need":"coherence","impact":1.0,"old_sat":"2.0","new_sat":"3.00","reason":"reviewed logs","caller":"manual"}
EOF
rm -f "$TEST_ASSETS/mindstate.lock"
touch -d "2026-01-01" "$TEST_WORKSPACE/MINDSTATE.md"
bash "$DAEMON" 2>/dev/null
bash "$FREEZE" "$session_start" 2>&1 >/dev/null
trajectory=$(grep "^trajectory:" "$TEST_WORKSPACE/MINDSTATE.md" | head -1 | sed 's/trajectory: *//')
echo "$trajectory" | grep -qi "coherence" && pass "coherence in trajectory" || fail "'$trajectory'"

# ─── Test 7: Open threads from INTENTIONS.md ───
echo "Test 7: Open threads extraction"
cat > "$TEST_WORKSPACE/INTENTIONS.md" << 'EOF'
## Active
- Build continuity layer
- Write mindstate tests
- Research paper revision
## Done
- Setup daemon cron
EOF
session_start=$(($(date +%s) - 300))
bash "$FREEZE" "$session_start" 2>&1 >/dev/null
grep -q "Build continuity layer" "$TEST_WORKSPACE/MINDSTATE.md" && pass "Thread extracted" || fail "Not extracted"

# ─── Test 8: Open threads capped at 3 ───
echo "Test 8: Open threads cap"
thread_count=$(sed -n '/^open_threads:/,/^[a-z]/p' "$TEST_WORKSPACE/MINDSTATE.md" | grep -c "^  -" || true)
(( thread_count <= 3 )) && pass "Capped at $thread_count" || fail "$thread_count threads"

# ─── Test 9: Structural predictions ───
echo "Test 9: Structural predictions"
grep -q "^structural:" "$TEST_WORKSPACE/MINDSTATE.md" && {
    pred_count=$(sed -n '/^structural:/,/^semantic:/p' "$TEST_WORKSPACE/MINDSTATE.md" | grep -c "^  -" || true)
    pass "$pred_count predictions"
} || fail "No structural section"

# ─── Test 10: Forecast section ───
echo "Test 10: Forecast section"
grep -q "^## forecast" "$TEST_WORKSPACE/MINDSTATE.md" && pass "Present" || fail "Missing"

echo ""
if [[ $errors -eq 0 ]]; then echo "All freeze tests PASSED"; exit 0
else echo "Freeze tests: $errors FAILED"; exit 1; fi
