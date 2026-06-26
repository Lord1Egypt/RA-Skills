#!/usr/bin/env bash
# Test: Execution Gate — propose, resolve, check, defer, edge cases
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
SCRIPTS="$SKILL_DIR/scripts"
GATE_FILE="$SKILL_DIR/assets/pending_actions.json"
AUDIT_LOG="$SKILL_DIR/assets/audit.log"

export WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
errors=0

cleanup() {
    rm -f "$GATE_FILE" "$GATE_FILE.tmp"
}
cleanup

# ─── Test 1: Propose creates pending action ───
echo "Test 1: gate-propose creates pending action"
bash "$SCRIPTS/gate-propose.sh" --need expression --action "test post" --impact 1.6 >/dev/null 2>&1
status=$(jq -r '.gate_status' "$GATE_FILE")
pending=$(jq -r '.pending_count' "$GATE_FILE")
action_need=$(jq -r '.actions[0].need' "$GATE_FILE")
action_status=$(jq -r '.actions[0].status' "$GATE_FILE")

if [[ "$status" == "BLOCKED" && "$pending" == "1" && "$action_need" == "expression" && "$action_status" == "PENDING" ]]; then
    echo "  Pending action created, gate BLOCKED — OK"
else
    echo "  FAIL: status=$status pending=$pending need=$action_need action_status=$action_status"
    ((errors++))
fi
cleanup

# ─── Test 2: gate-check blocks when pending ───
echo "Test 2: gate-check blocks when pending"
bash "$SCRIPTS/gate-propose.sh" --need understanding --action "read docs" --impact 1.0 >/dev/null 2>&1
if bash "$SCRIPTS/gate-check.sh" >/dev/null 2>&1; then
    echo "  FAIL: gate-check should have returned exit 1"
    ((errors++))
else
    echo "  gate-check returned exit 1 (BLOCKED) — OK"
fi
cleanup

# ─── Test 3: gate-check clears when no pending ───
echo "Test 3: gate-check clears when empty"
if bash "$SCRIPTS/gate-check.sh" >/dev/null 2>&1; then
    echo "  gate-check returned exit 0 (CLEAR) — OK"
else
    echo "  FAIL: gate-check should have returned exit 0"
    ((errors++))
fi

# ─── Test 4: Resolve by need with evidence ───
echo "Test 4: gate-resolve by need"
bash "$SCRIPTS/gate-propose.sh" --need connection --action "reply to post" --impact 1.3 >/dev/null 2>&1
bash "$SCRIPTS/gate-resolve.sh" --need connection --evidence "replied to SandyBlake post" >/dev/null 2>&1
resolved_status=$(jq -r '.actions[0].status' "$GATE_FILE")
gate=$(jq -r '.gate_status' "$GATE_FILE")
resolution=$(jq -r '.actions[0].resolution' "$GATE_FILE")

if [[ "$resolved_status" == "COMPLETED" && "$gate" == "CLEAR" && "$resolution" == *"replied"* ]]; then
    echo "  Resolved with evidence, gate CLEAR — OK"
else
    echo "  FAIL: status=$resolved_status gate=$gate resolution=$resolution"
    ((errors++))
fi
cleanup

# ─── Test 5: Defer with reason ───
echo "Test 5: gate-resolve --defer"
bash "$SCRIPTS/gate-propose.sh" --need expression --action "write essay" --impact 3.0 >/dev/null 2>&1
action_id=$(jq -r '.actions[0].id' "$GATE_FILE")
bash "$SCRIPTS/gate-resolve.sh" --defer "$action_id" --reason "quiet hours" >/dev/null 2>&1
deferred_status=$(jq -r '.actions[0].status' "$GATE_FILE")
gate=$(jq -r '.gate_status' "$GATE_FILE")
reason=$(jq -r '.actions[0].defer_reason' "$GATE_FILE")

if [[ "$deferred_status" == "DEFERRED" && "$gate" == "CLEAR" && "$reason" == "quiet hours" ]]; then
    echo "  Deferred with reason, gate CLEAR — OK"
else
    echo "  FAIL: status=$deferred_status gate=$gate reason=$reason"
    ((errors++))
fi
cleanup

# ─── Test 6: Multiple actions — gate blocks until ALL resolved ───
echo "Test 6: Multiple actions — partial resolution keeps gate blocked"
bash "$SCRIPTS/gate-propose.sh" --need expression --action "post A" --impact 1.0 >/dev/null 2>&1
bash "$SCRIPTS/gate-propose.sh" --need understanding --action "research B" --impact 1.5 >/dev/null 2>&1
pending=$(jq -r '.pending_count' "$GATE_FILE")
[[ "$pending" == "2" ]] || { echo "  FAIL: expected 2 pending, got $pending"; ((errors++)); }

# Resolve first only
bash "$SCRIPTS/gate-resolve.sh" --need expression --evidence "posted" >/dev/null 2>&1
gate=$(jq -r '.gate_status' "$GATE_FILE")
pending=$(jq -r '.pending_count' "$GATE_FILE")
if [[ "$gate" == "BLOCKED" && "$pending" == "1" ]]; then
    echo "  Partial resolution: still BLOCKED — OK"
else
    echo "  FAIL: gate=$gate pending=$pending (expected BLOCKED/1)"
    ((errors++))
fi

# Resolve second
bash "$SCRIPTS/gate-resolve.sh" --need understanding --evidence "wrote research note" >/dev/null 2>&1
gate=$(jq -r '.gate_status' "$GATE_FILE")
if [[ "$gate" == "CLEAR" ]]; then
    echo "  Full resolution: CLEAR — OK"
else
    echo "  FAIL: gate=$gate (expected CLEAR)"
    ((errors++))
fi
cleanup

# ─── Test 7: Self-report (low trust) ───
echo "Test 7: Self-report evidence"
bash "$SCRIPTS/gate-propose.sh" --need integrity --action "reflect on values" --impact 0.4 \
    --evidence-type self_report >/dev/null 2>&1
bash "$SCRIPTS/gate-resolve.sh" --need integrity --self-report --evidence "reflected on alignment with SOUL.md" >/dev/null 2>&1
resolution=$(jq -r '.actions[0].resolution' "$GATE_FILE")
status=$(jq -r '.actions[0].status' "$GATE_FILE")

if [[ "$status" == "COMPLETED" && "$resolution" == *"self-reported"* ]]; then
    echo "  Self-report accepted (low trust) — OK"
else
    echo "  FAIL: status=$status resolution=$resolution"
    ((errors++))
fi
cleanup

# ─── Test 8: Resolve without evidence (FAILED) ───
echo "Test 8: Resolve without evidence fails"
bash "$SCRIPTS/gate-propose.sh" --need expression --action "write post" --impact 1.6 >/dev/null 2>&1
# mark_satisfied evidence type — no audit.log entry, no --evidence flag
bash "$SCRIPTS/gate-resolve.sh" --need expression >/dev/null 2>&1
status=$(jq -r '.actions[0].status' "$GATE_FILE")

if [[ "$status" == "FAILED" ]]; then
    echo "  No evidence → FAILED — OK"
else
    echo "  FAIL: status=$status (expected FAILED)"
    ((errors++))
fi
cleanup

# ─── Test 9: Auto-detect evidence type from config ───
echo "Test 9: Evidence type auto-detection"
bash "$SCRIPTS/gate-propose.sh" --need security --action "run full backup + integrity verification" --impact 3.0 >/dev/null 2>&1
etype=$(jq -r '.actions[0].evidence_type' "$GATE_FILE")
# Should default to mark_satisfied
if [[ "$etype" == "mark_satisfied" ]]; then
    echo "  Auto-detected: mark_satisfied — OK"
else
    echo "  FAIL: evidence_type=$etype (expected mark_satisfied)"
    ((errors++))
fi
cleanup

# ─── Test 10: run-cycle.sh blocks on pending gate ───
echo "Test 10: run-cycle.sh refuses when gate blocked"
bash "$SCRIPTS/gate-propose.sh" --need expression --action "blocked action" --impact 1.0 >/dev/null 2>&1
# Explicitly unset SKIP_GATE so gate-check runs (it may be set in suite env)
output=$(WORKSPACE="$WORKSPACE" SKIP_GATE="" SKIP_SCANS=true bash "$SCRIPTS/run-cycle.sh" 2>&1)
if echo "$output" | grep -q "BLOCKED"; then
    echo "  run-cycle.sh detected gate block — OK"
else
    echo "  FAIL: run-cycle.sh did not detect gate block"
    ((errors++))
fi
cleanup

# ─── Test 11: Non-deferrable action (starvation guard) ───
echo "Test 11: Non-deferrable action cannot be deferred"
echo '{"actions":[{"id":"guard_001","timestamp":"2026-01-01T00:00:00Z","source":"starvation_guard","need":"expression","action_name":"forced expression","impact":1.0,"evidence_type":"mark_satisfied","evidence_hint":"","status":"PENDING","resolved_at":null,"resolution":null,"defer_reason":null,"deferrable":false}],"gate_status":"BLOCKED","pending_count":1,"completed_count":0,"deferred_count":0}' > "$GATE_FILE"
output=$(bash "$SCRIPTS/gate-resolve.sh" --defer guard_001 --reason "dont wanna" 2>&1 || true)
# Action should still be PENDING (defer rejected)
action_status=$(jq -r '.actions[0].status' "$GATE_FILE")
if echo "$output" | grep -q "non-deferrable" && [[ "$action_status" == "PENDING" ]]; then
    echo "  Non-deferrable blocked defer — OK"
else
    echo "  FAIL: action_status=$action_status output=$output"
    ((errors++))
fi
cleanup

# ─── Summary ───
echo ""
if [[ $errors -eq 0 ]]; then
    echo "All gate tests passed (11/11)"
    exit 0
else
    echo "Gate tests FAILED: $errors errors"
    exit 1
fi
