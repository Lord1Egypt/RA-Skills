#!/usr/bin/env bash
# Test: Deliberation Protocol — tagging, template, validation, run-cycle output
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
SCRIPTS="$SKILL_DIR/scripts"
CONFIG_FILE="$SKILL_DIR/assets/needs-config.json"

export WORKSPACE="${WORKSPACE:-$SKILL_DIR}"
export SKIP_GATE=true
errors=0

TMP_DIR=$(mktemp -d)

# Save ALL state files at start — restore on exit regardless of outcome
STATE_FILE="$SKILL_DIR/assets/needs-state.json"
AUDIT_LOG="$SKILL_DIR/assets/audit.log"
GATE_FILE="$SKILL_DIR/assets/pending_actions.json"
cp "$STATE_FILE" "$TMP_DIR/orig-needs-state.json"
cp "$AUDIT_LOG" "$TMP_DIR/orig-audit.log" 2>/dev/null || true
cp "$GATE_FILE" "$TMP_DIR/orig-gate.json" 2>/dev/null || true

cleanup_all() {
    cp "$TMP_DIR/orig-needs-state.json" "$STATE_FILE" 2>/dev/null || true
    cp "$TMP_DIR/orig-audit.log" "$AUDIT_LOG" 2>/dev/null || true
    # Don't restore gate — just clean it
    rm -f "$GATE_FILE" "$GATE_FILE.tmp" "$GATE_FILE.tmp."* 2>/dev/null || true
    rm -rf "$TMP_DIR"
}
trap cleanup_all EXIT

# ─── Test 1: Deliberative actions are tagged in config ───
echo "Test 1: Deliberative actions tagged in needs-config.json"
delib_count=$(jq '[.needs[].actions[] | select(.mode == "deliberative")] | length' "$CONFIG_FILE")
if (( delib_count >= 15 )); then
    echo "  Found $delib_count deliberative actions — OK"
else
    echo "  FAIL: Expected ≥15 deliberative actions, found $delib_count"
    ((errors++)) || true
fi

# ─── Test 2: Operative actions have no mode field (or mode=operative) ───
echo "Test 2: Operative actions unaffected"
backup_mode=$(jq -r '.needs.security.actions[] | select(.name == "run full backup + integrity verification") | .mode // "operative"' "$CONFIG_FILE")
if [[ "$backup_mode" == "operative" ]]; then
    echo "  'run full backup' is operative — OK"
else
    echo "  FAIL: 'run full backup' should be operative, got $backup_mode"
    ((errors++)) || true
fi

# ─── Test 3: Known deliberative action is tagged ───
echo "Test 3: Known deliberative action is tagged"
reread_mode=$(jq -r '.needs.understanding.actions[] | select(.name == "re-read recent learning notes") | .mode // "operative"' "$CONFIG_FILE")
if [[ "$reread_mode" == "deliberative" ]]; then
    echo "  're-read recent learning notes' is deliberative — OK"
else
    echo "  FAIL: expected deliberative, got $reread_mode"
    ((errors++)) || true
fi

# ─── Test 4: deliberate.sh --template (full) ───
echo "Test 4: Template mode (full pipeline)"
output=$(bash "$SCRIPTS/deliberate.sh" --template --need understanding --action "explore one topic briefly — note insight" 2>&1)
if grep -q "DELIBERATION:.*understanding" <<< "$output" && \
   grep -q "Phase 1: REPRESENT" <<< "$output" && \
   grep -q "Phase 5: CONCLUDE" <<< "$output" && \
   grep -q "Phase 6: ROUTE" <<< "$output"; then
    echo "  Full template generated with all phases — OK"
else
    echo "  FAIL: Missing phases in template output"
    echo "  Output: $output"
    ((errors++)) || true
fi

# ─── Test 5: deliberate.sh --template (compressed for low-impact) ───
echo "Test 5: Template auto-compresses for impact < 1.0"
output=$(bash "$SCRIPTS/deliberate.sh" --template --need understanding --action "re-read recent learning notes" 2>&1)
if grep -q "\[compressed\]" <<< "$output" && \
   grep -q "REPRESENT" <<< "$output" && \
   grep -q "CONCLUDE" <<< "$output" && \
   ! grep -q "Phase 2: RELATE" <<< "$output"; then
    echo "  Compressed template (no RELATE/GENERATE/EVALUATE) — OK"
else
    echo "  FAIL: Expected compressed template for impact 0.2"
    echo "  Output: $output"
    ((errors++)) || true
fi

# ─── Test 6: deliberate.sh --template warns for non-deliberative ───
echo "Test 6: Template warns for non-deliberative action"
output=$(bash "$SCRIPTS/deliberate.sh" --template --need security --action "run full backup + integrity verification" 2>&1)
if grep -q "not tagged deliberative" <<< "$output"; then
    echo "  Warning emitted for operative action — OK"
else
    echo "  FAIL: Should warn about non-deliberative action"
    ((errors++)) || true
fi

# ─── Test 7: deliberate.sh --validate (passing file) ───
echo "Test 7: Validate mode — passing file"
cat > "$TMP_DIR/good-delib.md" << 'MDEOF'
# Research on Topic X

## Conclusion
H₂S is not a viable standalone biosignature. Multi-molecular context required.

Confidence: medium

## What I don't know / next questions
- Population estimates for molten-ocean planets needed
- Sulfur isotope ratios as discriminator?
MDEOF

output=$(bash "$SCRIPTS/deliberate.sh" --validate "$TMP_DIR/good-delib.md" 2>&1)
if grep -q "\[PASS\]" <<< "$output"; then
    echo "  File with conclusion + route + confidence passes — OK"
else
    echo "  FAIL: Expected PASS for good file"
    echo "  Output: $output"
    ((errors++)) || true
fi

# ─── Test 8: deliberate.sh --validate (failing file — no conclusion) ───
echo "Test 8: Validate mode — failing file (no conclusion)"
cat > "$TMP_DIR/bad-delib.md" << 'MDEOF'
# Some Notes
I read the article. It was interesting.
There were some good points about exoplanets.
MDEOF

if ! bash "$SCRIPTS/deliberate.sh" --validate "$TMP_DIR/bad-delib.md" >/dev/null 2>&1; then
    echo "  File without conclusion fails validation — OK"
else
    echo "  FAIL: Expected FAIL for file without conclusion"
    ((errors++)) || true
fi

# ─── Test 9: deliberate.sh --validate (Russian conclusion) ───
echo "Test 9: Validate mode — Russian conclusion"
cat > "$TMP_DIR/ru-delib.md" << 'MDEOF'
# Исследование

## Вывод
Сера как биомаркер не работает на магматических планетах.

Уверенность: средняя

## Дальше
- Проверить популяционные оценки
MDEOF

output=$(bash "$SCRIPTS/deliberate.sh" --validate "$TMP_DIR/ru-delib.md" 2>&1)
if grep -q "\[PASS\]" <<< "$output"; then
    echo "  Russian file passes validation — OK"
else
    echo "  FAIL: Russian file should pass"
    echo "  Output: $output"
    ((errors++)) || true
fi

# ─── Test 10: deliberate.sh --validate-inline (passing) ───
echo "Test 10: Validate-inline — passing"
output=$(bash "$SCRIPTS/deliberate.sh" --validate-inline \
    --conclusion "H2S is not a reliable biosignature" \
    --route "research_thread" 2>&1)
if grep -q "\[PASS\]" <<< "$output"; then
    echo "  Inline validation passes — OK"
else
    echo "  FAIL: Expected PASS for valid inline"
    echo "  Output: $output"
    ((errors++)) || true
fi

# ─── Test 11: deliberate.sh --validate-inline (no conclusion) ───
echo "Test 11: Validate-inline — no conclusion fails"
if ! bash "$SCRIPTS/deliberate.sh" --validate-inline --route "concluded" >/dev/null 2>&1; then
    echo "  Missing conclusion fails — OK"
else
    echo "  FAIL: Expected FAIL for missing conclusion"
    ((errors++)) || true
fi

# ─── Test 12: deliberate.sh --validate-inline (low confidence + concluded warning) ───
echo "Test 12: Low-confidence + concluded warning"
output=$(bash "$SCRIPTS/deliberate.sh" --validate-inline \
    --conclusion "not sure about this" \
    --route "concluded" \
    --confidence "low" 2>&1)
if grep -q "Low-confidence conclusion with no followup" <<< "$output"; then
    echo "  Low-confidence warning emitted — OK"
else
    echo "  FAIL: Expected low-confidence warning"
    echo "  Output: $output"
    ((errors++)) || true
fi

# ─── Test 13: deliberate.sh --validate-inline (unknown route warning) ───
echo "Test 13: Unknown route warning"
output=$(bash "$SCRIPTS/deliberate.sh" --validate-inline \
    --conclusion "some conclusion" \
    --route "magic_portal" 2>&1)
if grep -q "Unknown route: magic_portal" <<< "$output"; then
    echo "  Unknown route warning emitted — OK"
else
    echo "  FAIL: Expected unknown route warning"
    echo "  Output: $output"
    ((errors++)) || true
fi

# ─── Test 14: run-cycle.sh outputs [DELIBERATIVE] tag ───
echo "Test 14: run-cycle.sh shows [DELIBERATIVE] for tagged actions"
# Run cycle up to 5 times to get a deliberative action (RNG dependent)
STATE_FILE="$SKILL_DIR/assets/needs-state.json"
cp "$STATE_FILE" "$TMP_DIR/needs-state-backup.json"

# Patch understanding satisfaction to 0 to force selection
jq '.understanding.satisfaction = 0 | .understanding.last_satisfied = "2026-01-01T00:00:00Z"' \
    "$STATE_FILE" > "$TMP_DIR/state-tmp.json" && cp "$TMP_DIR/state-tmp.json" "$STATE_FILE"

found_deliberative=false
found_protocol=false
found_operative_simple=false
combined_output=""
for attempt in 1 2 3 4 5; do
    output=$(WORKSPACE="$SKILL_DIR" SKIP_GATE=true bash "$SCRIPTS/run-cycle.sh" 2>&1 || true)
    combined_output="${combined_output}${output}"
    if grep -q "\[DELIBERATIVE\]" <<< "$output"; then
        found_deliberative=true
    fi
    if grep -q "deliberate.sh" <<< "$output"; then
        found_protocol=true
    fi
    # Check for operative action with simple "Then: mark-satisfied" (no --conclusion)
    if grep "Then: mark-satisfied.sh" <<< "$output" | grep -qv "\-\-conclusion"; then
        found_operative_simple=true
    fi
    if $found_deliberative && $found_protocol && $found_operative_simple; then
        break
    fi
done

# Restore state
cp "$TMP_DIR/needs-state-backup.json" "$STATE_FILE"

if $found_deliberative; then
    echo "  [DELIBERATIVE] tag appears in run-cycle output — OK"
else
    echo "  FAIL: No [DELIBERATIVE] tag in 5 attempts (statistically unlikely with 8/13 tagged)"
    ((errors++)) || true
fi

# ─── Test 15: run-cycle.sh shows deliberate.sh protocol for deliberative ───
echo "Test 15: run-cycle.sh shows protocol instructions for deliberative"
if $found_protocol; then
    echo "  Protocol instructions shown — OK"
else
    if $found_deliberative; then
        echo "  FAIL: DELIBERATIVE tag present but no protocol instructions"
        ((errors++)) || true
    else
        echo "  No deliberative action selected — skipping"
    fi
fi

# ─── Test 16: Operative actions still show simple "Then: mark-satisfied" ───
echo "Test 16: Operative actions have simple output (no --conclusion)"
if $found_operative_simple; then
    echo "  Operative action shows simple mark-satisfied — OK"
else
    echo "  (No operative actions in output — test inconclusive)"
fi

# ═══════════════════════════════════════════
# Phase 2 Tests (v1.31.0)
# ═══════════════════════════════════════════

GATE_FILE="$SKILL_DIR/assets/pending_actions.json"
AUDIT_LOG="$SKILL_DIR/assets/audit.log"
STATE_FILE="$SKILL_DIR/assets/needs-state.json"

# Clear any stale locks from Phase 1 tests (fd leak prevention)
rm -f "$SKILL_DIR/assets/"*.lock "$GATE_FILE" 2>/dev/null || true

# Backup state files before Phase 2 tests (they modify real state)
cp "$STATE_FILE" "$TMP_DIR/needs-state-phase2-backup.json"
cp "$AUDIT_LOG" "$TMP_DIR/audit-phase2-backup.log" 2>/dev/null || true

# Restore on exit (update trap)
trap 'cp "$TMP_DIR/needs-state-phase2-backup.json" "$STATE_FILE" 2>/dev/null; cp "$TMP_DIR/audit-phase2-backup.log" "$AUDIT_LOG" 2>/dev/null; rm -f "$SKILL_DIR/assets/"*.lock "$GATE_FILE" 2>/dev/null; rm -rf "$TMP_DIR"' EXIT

cleanup_gate() {
    rm -f "$GATE_FILE" "$GATE_FILE.tmp" "$GATE_FILE.tmp."* 2>/dev/null
}

# ─── Test 17: mark-satisfied with --conclusion → audit.log ───
echo "Test 17: mark-satisfied --conclusion appears in audit.log"
AUDIT_LINES_BEFORE=$(wc -l < "$AUDIT_LOG" 2>/dev/null || echo 0)
bash "$SCRIPTS/mark-satisfied.sh" coherence 0.2 --reason "test deliberation" --conclusion "H2S is not a reliable biosignature" >/dev/null 2>&1 || true
# Find the new entry (may not be last if other tests wrote too)
NEW_ENTRY=$(tail -n +$((AUDIT_LINES_BEFORE + 1)) "$AUDIT_LOG" | grep "test deliberation" | tail -1)
if echo "$NEW_ENTRY" | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['conclusion'] == 'H2S is not a reliable biosignature'" 2>/dev/null; then
    echo "  Conclusion field present in audit.log — OK"
else
    echo "  FAIL: Conclusion not found in audit entry"
    echo "  New entry: $NEW_ENTRY"
    ((errors++)) || true
fi

# ─── Test 18: mark-satisfied without --conclusion → conclusion: null ───
echo "Test 18: mark-satisfied without --conclusion → null"
AUDIT_LINES_BEFORE=$(wc -l < "$AUDIT_LOG" 2>/dev/null || echo 0)
bash "$SCRIPTS/mark-satisfied.sh" coherence 0.2 --reason "no conclusion test" >/dev/null 2>&1 || true
NEW_ENTRY=$(tail -n +$((AUDIT_LINES_BEFORE + 1)) "$AUDIT_LOG" | grep "no conclusion test" | tail -1)
if echo "$NEW_ENTRY" | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['conclusion'] is None" 2>/dev/null; then
    echo "  Conclusion is null when absent — OK"
else
    echo "  FAIL: Conclusion should be null"
    echo "  New entry: $NEW_ENTRY"
    ((errors++)) || true
fi

# ─── Test 19: gate-resolve deliberative action without --conclusion → warning ───
echo "Test 19: gate-resolve deliberative without --conclusion → warning"
cleanup_gate
bash "$SCRIPTS/gate-propose.sh" --need understanding --action "re-read recent learning notes" --impact 0.2 >/dev/null 2>&1
# Mark satisfied first so evidence verification passes
bash "$SCRIPTS/mark-satisfied.sh" understanding 0.2 --reason "test" >/dev/null 2>&1 || true
output=$(bash "$SCRIPTS/gate-resolve.sh" --need understanding --evidence "test resolve" 2>&1)
if grep -qE "(Deliberative action resolved without|marked as 'absent')" <<< "$output"; then
    echo "  Warning emitted for deliberative without conclusion — OK"
else
    echo "  FAIL: Expected deliberative warning"
    echo "  Output: $output"
    ((errors++)) || true
fi
cleanup_gate

# ─── Test 20: gate-resolve deliberative with --conclusion → in resolution ───
echo "Test 20: gate-resolve deliberative with --conclusion → resolution"
cleanup_gate
bash "$SCRIPTS/gate-propose.sh" --need understanding --action "re-read recent learning notes" --impact 0.2 >/dev/null 2>&1
bash "$SCRIPTS/mark-satisfied.sh" understanding 0.2 --reason "test" >/dev/null 2>&1 || true
output=$(bash "$SCRIPTS/gate-resolve.sh" --need understanding --evidence "test" --conclusion "found tension between X and Y" 2>&1)
resolution=$(jq -r '.actions[0].resolution' "$GATE_FILE")
if grep -q "conclusion: found tension between X and Y" <<< "$resolution"; then
    echo "  Conclusion in resolution field — OK"
else
    echo "  FAIL: Conclusion not in resolution"
    echo "  Resolution: $resolution"
    ((errors++)) || true
fi
# Also verify no warning was emitted
if grep -q "Deliberative action resolved without" <<< "$output"; then
    echo "  FAIL: Warning should NOT appear when conclusion provided"
    ((errors++)) || true
fi
cleanup_gate

# ─── Test 21: gate-resolve operative without --conclusion → no warning ───
echo "Test 21: gate-resolve operative without --conclusion → no warning"
cleanup_gate
bash "$SCRIPTS/gate-propose.sh" --need security --action "run full backup + integrity verification" --impact 3.0 >/dev/null 2>&1
bash "$SCRIPTS/mark-satisfied.sh" security 3.0 --reason "backup done" >/dev/null 2>&1 || true
output=$(bash "$SCRIPTS/gate-resolve.sh" --need security --evidence "backup completed" 2>&1)
if grep -q "Deliberative action resolved without" <<< "$output"; then
    echo "  FAIL: Should NOT warn for operative actions"
    ((errors++)) || true
else
    echo "  No warning for operative action — OK"
fi
cleanup_gate

# ─── Test 22: gate-resolve legacy action (no action_mode) → no crash ───
echo "Test 22: Legacy action without action_mode → no crash"
cleanup_gate
# Manually create a legacy pending action without action_mode field
echo '{"actions":[{"id":"legacy_001","timestamp":"2026-03-23T00:00:00Z","source":"test","need":"coherence","action_name":"test","impact":0.5,"evidence_type":"mark_satisfied","status":"PENDING","resolved_at":null,"resolution":null,"defer_reason":null}],"gate_status":"BLOCKED","pending_count":1,"completed_count":0,"deferred_count":0}' > "$GATE_FILE"
bash "$SCRIPTS/mark-satisfied.sh" coherence 0.5 --reason "test" >/dev/null 2>&1 || true
output=$(bash "$SCRIPTS/gate-resolve.sh" legacy_001 --evidence "test legacy" 2>&1)
if grep -q "COMPLETED" <<< "$output"; then
    echo "  Legacy action resolves without crash — OK"
else
    echo "  FAIL: Legacy action should resolve normally"
    echo "  Output: $output"
    ((errors++)) || true
fi
# Verify no deliberative warning
if grep -q "Deliberative" <<< "$output"; then
    echo "  FAIL: Legacy action should not trigger deliberative warning"
    ((errors++)) || true
fi
cleanup_gate

# ─── Test 23: mark-satisfied --conclusion with sensitive data → scrubbed ───
echo "Test 23: Conclusion with sensitive data is scrubbed"
AUDIT_LINES_BEFORE=$(wc -l < "$AUDIT_LOG" 2>/dev/null || echo 0)
bash "$SCRIPTS/mark-satisfied.sh" security 0.3 --reason "test scrub" --conclusion "found open port on 192.168.1.100 at /home/user/.ssh/key" >/dev/null 2>&1 || true
NEW_ENTRY=$(tail -n +$((AUDIT_LINES_BEFORE + 1)) "$AUDIT_LOG" | grep "test scrub" | tail -1)
if echo "$NEW_ENTRY" | grep -q "192.168.1.100"; then
    echo "  FAIL: IP address should be scrubbed"
    ((errors++)) || true
else
    echo "  Sensitive data scrubbed from conclusion — OK"
fi

# ─── Test 24: gate-propose deliberative → action_mode stored ───
echo "Test 24: gate-propose stores action_mode for deliberative"
cleanup_gate
bash "$SCRIPTS/gate-propose.sh" --need understanding --action "re-read recent learning notes" --impact 0.2 >/dev/null 2>&1
stored_mode=$(jq -r '.actions[0].action_mode' "$GATE_FILE")
if [[ "$stored_mode" == "deliberative" ]]; then
    echo "  action_mode: deliberative stored in gate — OK"
else
    echo "  FAIL: Expected deliberative, got $stored_mode"
    ((errors++)) || true
fi
cleanup_gate

# ─── Test 25: gate-propose unknown action → operative fallback ───
echo "Test 25: gate-propose unknown action → operative fallback"
cleanup_gate
bash "$SCRIPTS/gate-propose.sh" --need security --action "nonexistent action" --impact 1.0 >/dev/null 2>&1
stored_mode=$(jq -r '.actions[0].action_mode' "$GATE_FILE")
if [[ "$stored_mode" == "operative" ]]; then
    echo "  Fallback to operative for unknown action — OK"
else
    echo "  FAIL: Expected operative fallback, got $stored_mode"
    ((errors++)) || true
fi
cleanup_gate

# ─── Test 26: gate-resolve --conclusion with --defer ───
echo "Test 26: --conclusion preserved with --defer"
cleanup_gate
bash "$SCRIPTS/gate-propose.sh" --need understanding --action "explore one topic briefly — note insight" --impact 1.1 >/dev/null 2>&1
action_id=$(jq -r '.actions[0].id' "$GATE_FILE")
output=$(bash "$SCRIPTS/gate-resolve.sh" --defer "$action_id" --reason "night time" --conclusion "partial: found interesting lead on X" 2>&1)
partial=$(jq -r '.actions[0].partial_conclusion' "$GATE_FILE")
if [[ "$partial" == "partial: found interesting lead on X" ]]; then
    echo "  Partial conclusion preserved in defer — OK"
else
    echo "  FAIL: Partial conclusion not stored"
    echo "  Got: $partial"
    ((errors++)) || true
fi
cleanup_gate

# ─── Test 27: gate-resolve --conclusion "" (empty) → treated as absent ───
echo "Test 27: Empty --conclusion treated as absent"
cleanup_gate
bash "$SCRIPTS/gate-propose.sh" --need understanding --action "re-read recent learning notes" --impact 0.2 >/dev/null 2>&1
bash "$SCRIPTS/mark-satisfied.sh" understanding 0.2 --reason "test" >/dev/null 2>&1 || true
output=$(bash "$SCRIPTS/gate-resolve.sh" --need understanding --evidence "test" --conclusion "" 2>&1)
if grep -qE "(Deliberative action resolved without|marked as 'absent')" <<< "$output"; then
    echo "  Empty conclusion triggers warning — OK"
else
    echo "  FAIL: Empty conclusion should trigger warning for deliberative"
    echo "  Output: $output"
    ((errors++)) || true
fi
cleanup_gate

# ─── Summary ───
echo ""
echo "================================"
if (( errors == 0 )); then
    echo "All deliberation tests passed! (Phase 1 + Phase 2)"
else
    echo "FAILED: $errors test(s) failed"
fi
exit "$errors"
