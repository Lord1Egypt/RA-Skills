#!/bin/bash
# test_closure_backlog.sh — Deferred backlog pressure + ABANDONED close operation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
SCAN="$SKILL_DIR/scripts/scan_closure.sh"
RESOLVE="$SKILL_DIR/scripts/gate-resolve.sh"

errors=0
pass() { echo "  ✓ $1"; }
fail() { echo "  ✗ $1"; ((errors++)) || true; }

# Isolated environment
TEST_WORKSPACE=$(mktemp -d /tmp/tp_backlog_XXXXXX)
TEST_ASSETS=$(mktemp -d /tmp/tp_backlog_assets_XXXXXX)
export WORKSPACE="$TEST_WORKSPACE"
export SCAN_ASSETS_DIR="$TEST_ASSETS"
export MINDSTATE_ASSETS_DIR="$TEST_ASSETS"

cleanup() { rm -rf "$TEST_WORKSPACE" "$TEST_ASSETS"; }
trap cleanup EXIT

# Copy required assets
cp "$SKILL_DIR/assets/needs-config.json" "$TEST_ASSETS/"
cp "$SKILL_DIR/assets/needs-state.template.json" "$TEST_ASSETS/needs-state.json"
cp "$SKILL_DIR/assets/decay-config.json" "$TEST_ASSETS/" 2>/dev/null || true
mkdir -p "$TEST_WORKSPACE/memory"

# Set recent last_satisfied for closure so time_sat=3 in tests (baseline without pressure)
now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
jq --arg t "$now" --arg n "closure" '.[$n].last_satisfied = $t | .[$n].satisfaction = 3.0' \
    "$TEST_ASSETS/needs-state.json" > "$TEST_ASSETS/needs-state.json.tmp" && \
    mv "$TEST_ASSETS/needs-state.json.tmp" "$TEST_ASSETS/needs-state.json"

# Helper: write pending_actions.json with N deferred actions
write_deferred() {
    local count="$1"
    local actions="[]"
    for i in $(seq 1 "$count"); do
        actions=$(echo "$actions" | jq \
            --arg id "act_test_closure_$i" \
            --arg need "closure" \
            --arg name "test action $i" \
            '. += [{"id": $id, "status": "DEFERRED", "need": $need, "action_name": $name,
                    "timestamp": "2026-01-01T00:00:00Z", "impact": 1.5, "deferrable": true,
                    "action_mode": "operative", "evidence_type": "mark_satisfied",
                    "defer_reason": "timeout"}]')
    done
    echo "{\"actions\": $actions, \"gate_status\": \"CLEAR\", \"pending_count\": 0, \"deferred_count\": $count}" \
        > "$TEST_ASSETS/pending_actions.json"
}

echo "=== closure backlog tests ==="

# Helper to run scan with all env vars properly forwarded
run_scan() {
    WORKSPACE="$TEST_WORKSPACE" SCAN_ASSETS_DIR="$TEST_ASSETS" MINDSTATE_ASSETS_DIR="$TEST_ASSETS" \
        bash "$SCAN" 2>/dev/null
}

# Test 1: Low deferred (<5) — no pressure boost
echo "Test 1: Low deferred (3) — no pressure"
write_deferred 3
result=$(run_scan)
[[ -n "$result" ]] && pass "Scanner runs cleanly" || fail "Scanner crashed"
(( result >= 2 )) && pass "No pressure at 3 deferred (sat=$result)" || fail "Unexpected pressure at 3 deferred (sat=$result)"

# Test 2: Medium deferred (12) — pressure applied (+3 neg signals)
echo "Test 2: Medium deferred (12) — pressure applied"
write_deferred 12
result=$(run_scan)
(( result <= 1 )) && pass "Medium pressure at 12 deferred (sat=$result)" || fail "Expected sat≤1 at 12 deferred (got $result)"

# Test 3: Heavy deferred (22) — max pressure (+5 neg signals)
echo "Test 3: Heavy deferred (22) — max pressure"
write_deferred 22
result=$(run_scan)
(( result == 0 )) && pass "Max pressure at 22 deferred (sat=$result)" || fail "Expected sat=0 at 22 deferred (got $result)"

# Test 4: gate-resolve --close transitions DEFERRED → ABANDONED
echo "Test 4: gate-resolve --close"
write_deferred 3
# Add a pending action too (required for gate file structure)
jq '.actions += [{"id": "act_pending_1", "status": "PENDING", "need": "closure",
    "action_name": "active action", "timestamp": "2026-04-09T00:00:00Z", "impact": 2.0,
    "deferrable": true, "action_mode": "operative", "evidence_type": "mark_satisfied"}] |
    .pending_count = 1 | .gate_status = "BLOCKED"' \
    "$TEST_ASSETS/pending_actions.json" > "$TEST_ASSETS/pending_actions.json.tmp" && \
    mv "$TEST_ASSETS/pending_actions.json.tmp" "$TEST_ASSETS/pending_actions.json"

bash "$RESOLVE" --close act_test_closure_1 --close-reason "cleaned during backlog review" >/dev/null 2>&1
status=$(jq -r '.actions[] | select(.id == "act_test_closure_1") | .status' "$TEST_ASSETS/pending_actions.json")
[[ "$status" == "ABANDONED" ]] && pass "DEFERRED → ABANDONED" || fail "Expected ABANDONED, got $status"

# Test 5: --close on PENDING fails
echo "Test 5: --close on PENDING is rejected"
output=$(bash "$RESOLVE" --close act_pending_1 2>&1 || true)
echo "$output" | grep -q "only valid for DEFERRED" && pass "PENDING close rejected" || fail "Expected rejection: $output"

# Test 6: after close, deferred_count decreases
echo "Test 6: deferred_count updates after close"
count=$(jq -r '[.actions[] | select(.status == "DEFERRED")] | length' "$TEST_ASSETS/pending_actions.json")
(( count == 2 )) && pass "deferred_count decreased to $count" || fail "Expected 2, got $count"

# Test 7: pressure reduces after cleanup (3→1 deferred after closes)
echo "Test 7: pressure reduces after cleanup"
# Close 2 more so only 1 remains
bash "$RESOLVE" --close act_test_closure_2 >/dev/null 2>&1
bash "$RESOLVE" --close act_test_closure_3 >/dev/null 2>&1
result=$(run_scan)
(( result >= 2 )) && pass "Pressure reduced at 1 deferred (sat=$result)" || fail "Expected sat≥2 at 1 deferred (got $result)"

# Test 8: new action "review deferred backlog" in config
echo "Test 8: backlog review action present in config"
has_action=$(jq -r '.needs.closure.actions[] | select(.name | test("review deferred backlog")) | .name' \
    "$TEST_ASSETS/needs-config.json" 2>/dev/null)
[[ -n "$has_action" ]] && pass "backlog review action found" || fail "action not found in config"

# Test 9: deferred_backlog_size in scan checks
echo "Test 9: deferred_backlog_size in closure scan checks"
has_check=$(jq -r '.needs.closure.scan.checks[] | select(. == "deferred_backlog_size")' \
    "$TEST_ASSETS/needs-config.json" 2>/dev/null)
[[ -n "$has_check" ]] && pass "deferred_backlog_size check declared" || fail "check not in config"

echo ""
if [[ $errors -eq 0 ]]; then echo "All backlog tests PASSED"; exit 0
else echo "Backlog tests: $errors FAILED"; exit 1; fi
