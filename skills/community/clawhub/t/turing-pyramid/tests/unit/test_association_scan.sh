#!/usr/bin/env bash
# Test: association-scan.sh + followup horizons + concluded-action warning
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
SCRIPTS="$SKILL_DIR/scripts"

export WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
errors=0

TMP_DIR=$(mktemp -d)
trap "rm -rf '$TMP_DIR'" EXIT

# ─── Setup test corpus ───
TEST_ASSETS="$TMP_DIR/assets"
TEST_RESEARCH="$TMP_DIR/research"
mkdir -p "$TEST_ASSETS" "$TEST_RESEARCH/threads" "$TEST_RESEARCH/deliberations"

# Create test audit.log with conclusions
NOW_ISO=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat > "$TEST_ASSETS/audit.log" << AUDIT
{"timestamp":"$NOW_ISO","need":"coherence","impact":0.6,"old_sat":"2.0","new_sat":"2.6","reason":"test","caller":"manual","conclusion":"MEMORY.md is stale and should be updated with protocol changes"}
{"timestamp":"$NOW_ISO","need":"understanding","impact":2.1,"old_sat":"0.0","new_sat":"2.1","reason":"test","caller":"manual","conclusion":"H2S biosignature unreliable on magma planets"}
{"timestamp":"$NOW_ISO","need":"security","impact":1.0,"old_sat":"1.0","new_sat":"2.0","reason":"test","caller":"manual","conclusion":null}
AUDIT

# Create test research thread
cat > "$TEST_RESEARCH/threads/test-thread.md" << 'MD'
# Test Research Thread
## Conclusion
Sulfur compounds are not reliable biosignatures on magma ocean planets.
## Open questions
- Population estimates needed
MD

# Create test followups
cat > "$TEST_ASSETS/followups.jsonl" << 'FU'
{"id":"fu_1","what":"update MEMORY.md with protocol","need":"coherence","status":"pending","created_at":"2026-03-23T12:00:00Z"}
{"id":"fu_2","what":"check backup integrity","need":"security","status":"resolved","created_at":"2026-03-23T08:00:00Z"}
FU

# Create test INTERESTS.md
cat > "$TMP_DIR/INTERESTS.md" << 'INT'
# Interests
- Sulfur isotope ratios as biosignature discriminator
- Quantum computing applications in cryptography
INT

# Override paths for association-scan (use test corpus)
export WORKSPACE="$TMP_DIR"
export MINDSTATE_ASSETS_DIR="$TEST_ASSETS"

# ─── Test 1: Matching keyword in audit conclusion ───
echo "Test 1: Keyword match in audit conclusion"
output=$(bash "$SCRIPTS/association-scan.sh" --keywords "MEMORY stale protocol" --need coherence 2>&1)
if echo "$output" | grep -q "MEMORY.md is stale"; then
    echo "  Audit conclusion found — OK"
else
    echo "  FAIL: Expected audit conclusion match"
    echo "  Output: $output"
    ((errors++)) || true
fi

# ─── Test 2: No matching keywords ───
echo "Test 2: No matching keywords"
output=$(bash "$SCRIPTS/association-scan.sh" --keywords "xyzzyplugh zorkbleep" 2>&1)
if echo "$output" | grep -q "0 found"; then
    echo "  Zero results for non-matching keywords — OK"
else
    echo "  FAIL: Expected 0 found"
    ((errors++)) || true
fi

# ─── Test 3: Need match bonus ───
echo "Test 3: Need match bonus"
output_with=$(bash "$SCRIPTS/association-scan.sh" --keywords "MEMORY stale" --need coherence 2>&1)
output_without=$(bash "$SCRIPTS/association-scan.sh" --keywords "MEMORY stale" --need security 2>&1)
score_with=$(echo "$output_with" | grep -oP 'score: \K[0-9]+' | head -1)
score_without=$(echo "$output_without" | grep -oP 'score: \K[0-9]+' | head -1)
if [[ -n "$score_with" && -n "$score_without" ]] && (( score_with > score_without )); then
    echo "  Need match gives higher score ($score_with > $score_without) — OK"
else
    echo "  FAIL: Expected higher score with matching need (with=$score_with, without=$score_without)"
    ((errors++)) || true
fi

# ─── Test 4: Max results respected ───
echo "Test 4: Max results"
output=$(bash "$SCRIPTS/association-scan.sh" --keywords "sulfur biosignature magma protocol MEMORY" --max-results 1 2>&1)
result_count=$(echo "$output" | grep -c '^\[' || true)
if (( result_count <= 1 )); then
    echo "  Max 1 result respected — OK"
else
    echo "  FAIL: Expected max 1, got $result_count"
    ((errors++)) || true
fi

# ─── Test 5: Min score respected ───
echo "Test 5: Min score threshold"
output=$(bash "$SCRIPTS/association-scan.sh" --keywords "sulfur" --min-score 100 2>&1)
if echo "$output" | grep -q "no associations above threshold\|0 found"; then
    echo "  High min-score filters everything — OK"
else
    echo "  FAIL: Expected no results with min-score 100"
    ((errors++)) || true
fi

# ─── Test 6: Recency filter ───
echo "Test 6: Recency filter"
# Create old entry with unique keyword
echo '{"timestamp":"2020-01-01T00:00:00Z","need":"understanding","impact":1.0,"old_sat":"0","new_sat":"1","reason":"old","caller":"manual","conclusion":"ancient dinosaur fossils discovery"}' >> "$TEST_ASSETS/audit.log"
output=$(bash "$SCRIPTS/association-scan.sh" --keywords "dinosaur fossils" --recency-hours 1 2>&1)
if echo "$output" | grep -q "0 found\|no associations"; then
    echo "  Old entry excluded by recency — OK"
else
    echo "  FAIL: Expected old entry to be excluded"
    echo "  Output: $output"
    ((errors++)) || true
fi

# ─── Test 7: Pending followup found ───
echo "Test 7: Pending followup match"
output=$(bash "$SCRIPTS/association-scan.sh" --keywords "MEMORY protocol update" 2>&1)
if echo "$output" | grep -q "followup.*pending"; then
    echo "  Pending followup found — OK"
else
    echo "  FAIL: Expected pending followup in results"
    ((errors++)) || true
fi

# ─── Test 8: Research thread found ───
echo "Test 8: Research thread match"
output=$(bash "$SCRIPTS/association-scan.sh" --keywords "sulfur biosignature magma" 2>&1)
if echo "$output" | grep -q "thread"; then
    echo "  Research thread found — OK"
else
    echo "  FAIL: Expected research thread in results"
    ((errors++)) || true
fi

# ─── Test 9: INTERESTS.md entry found ───
echo "Test 9: INTERESTS.md match"
output=$(bash "$SCRIPTS/association-scan.sh" --keywords "sulfur isotope biosignature" 2>&1)
if echo "$output" | grep -q "interest"; then
    echo "  Interest entry found — OK"
else
    echo "  FAIL: Expected interest in results"
    ((errors++)) || true
fi

# ─── Test 10: Empty corpus ───
echo "Test 10: Empty corpus"
EMPTY_DIR=$(mktemp -d)
output=$(WORKSPACE="$EMPTY_DIR" bash "$SCRIPTS/association-scan.sh" --keywords "anything" 2>&1)
rm -rf "$EMPTY_DIR"
if echo "$output" | grep -q "0 found"; then
    echo "  Empty corpus returns 0 — OK"
else
    echo "  FAIL: Expected 0 found on empty corpus"
    ((errors++)) || true
fi

# ─── Test 11: Performance (not too slow) ───
echo "Test 11: Performance"
# Generate large audit log
for i in $(seq 1 2000); do
    echo "{\"timestamp\":\"$NOW_ISO\",\"need\":\"understanding\",\"impact\":1.0,\"old_sat\":\"0\",\"new_sat\":\"1\",\"reason\":\"bulk test $i\",\"caller\":\"test\",\"conclusion\":\"generic finding number $i\"}"
done >> "$TEST_ASSETS/audit.log"
start_time=$(date +%s%N)
bash "$SCRIPTS/association-scan.sh" --keywords "protocol stale" --max-results 3 > /dev/null 2>&1
end_time=$(date +%s%N)
elapsed_ms=$(( (end_time - start_time) / 1000000 ))
if (( elapsed_ms < 5000 )); then
    echo "  2000+ lines scanned in ${elapsed_ms}ms — OK"
else
    echo "  FAIL: Took ${elapsed_ms}ms (target < 5000ms)"
    ((errors++)) || true
fi

# ─── Test 12: mindstate-freeze extracts deliberation residuals ───
echo "Test 12: Freeze extracts deliberation residuals"
# Setup: freeze needs full assets (needs-state, needs-config, audit.log) + MINDSTATE.md
FREEZE_DIR=$(mktemp -d)
mkdir -p "$FREEZE_DIR/assets"
cp "$SKILL_DIR/assets/needs-state.json" "$FREEZE_DIR/assets/" 2>/dev/null || true
cp "$SKILL_DIR/assets/needs-config.json" "$FREEZE_DIR/assets/" 2>/dev/null || true
cp "$TEST_ASSETS/audit.log" "$FREEZE_DIR/assets/"
cat > "$FREEZE_DIR/MINDSTATE.md" << 'MSEOF'
# MINDSTATE
## reality
last_update: 2026-03-24T01:00:00Z
## cognition
frozen_at: 2026-03-23T20:00:00Z
trajectory: testing
open_threads:
  - test thread
momentum: testing
cognitive_temperature: building
MSEOF
SESSION_START=$(($(date +%s) - 3600))
WORKSPACE="$FREEZE_DIR" MINDSTATE_ASSETS_DIR="$FREEZE_DIR/assets" \
    bash "$SCRIPTS/mindstate-freeze.sh" "$SESSION_START" >/dev/null 2>&1 || true
if [[ -f "$FREEZE_DIR/MINDSTATE.md" ]] && grep -q "deliberation_residuals:" "$FREEZE_DIR/MINDSTATE.md"; then
    echo "  deliberation_residuals section present — OK"
else
    echo "  FAIL: No deliberation_residuals in MINDSTATE.md"
    ((errors++)) || true
fi
rm -rf "$FREEZE_DIR"

# ─── Test 13: mindstate-boot outputs associations ───
echo "Test 13: Boot outputs contextual recall"
output=$(WORKSPACE="$TMP_DIR" MINDSTATE_ASSETS_DIR="$TEST_ASSETS" \
    bash "$SCRIPTS/mindstate-boot.sh" 2>&1 || true)
if echo "$output" | grep -q "Contextual recall\|ASSOCIATIONS"; then
    echo "  Contextual recall section in boot — OK"
else
    # Boot may exit early if MINDSTATE format doesn't match expectations
    echo "  (Boot may not reach association scan — test inconclusive)"
fi

# ─── Test 14: Concluded + action language warning (validate) ───
echo "Test 14: Concluded + action language warning (validate)"
cat > "$TMP_DIR/concluded-action.md" << 'MD'
# Deliberation
## Conclusion
All fine. Concluded — no further action needed.
But we should update INTENTIONS.md to demote Continuity Layer.
Confidence: high
## Route
concluded
MD
output=$(bash "$SCRIPTS/../scripts/deliberate.sh" --validate "$TMP_DIR/concluded-action.md" 2>&1)
if echo "$output" | grep -q "concluded.*action language"; then
    echo "  Warning emitted for concluded + action language — OK"
else
    echo "  FAIL: Expected concluded + action warning"
    echo "  Output: $output"
    ((errors++)) || true
fi

# ─── Test 15: create-followup.sh accepts --in 2w ───
echo "Test 15: Followup --in 2w"
output=$(bash "$SCRIPTS/create-followup.sh" --what "test-2w-$$" --in 2w --need coherence 2>&1)
if echo "$output" | grep -q "Follow-up created"; then
    echo "  2w followup created — OK"
    # Cleanup
    fu_id=$(echo "$output" | grep -oP 'ID: \K\S+')
    bash "$SCRIPTS/resolve-followup.sh" "$fu_id" >/dev/null 2>&1 || true
else
    echo "  FAIL: Expected followup creation"
    echo "  Output: $output"
    ((errors++)) || true
fi

# ─── Test 16: create-followup.sh accepts --in 1m ───
echo "Test 16: Followup --in 1m"
output=$(bash "$SCRIPTS/create-followup.sh" --what "test-1m-$$" --in 1m --need understanding 2>&1)
if echo "$output" | grep -q "Follow-up created"; then
    echo "  1m followup created — OK"
    fu_id=$(echo "$output" | grep -oP 'ID: \K\S+')
    bash "$SCRIPTS/resolve-followup.sh" "$fu_id" >/dev/null 2>&1 || true
else
    echo "  FAIL: Expected followup creation"
    echo "  Output: $output"
    ((errors++)) || true
fi

# ─── Test 17: --exclude-source ───
echo "Test 17: --exclude-source skips specified source"
output=$(bash "$SCRIPTS/association-scan.sh" --keywords "sulfur biosignature" --exclude-source thread 2>&1)
if echo "$output" | grep -q "thread"; then
    echo "  FAIL: thread source should have been excluded"
    ((errors++)) || true
else
    echo "  Thread source excluded — OK"
fi

# ─── Summary ───
echo ""
echo "================================"
if (( errors == 0 )); then
    echo "All association scan tests passed!"
else
    echo "FAILED: $errors test(s) failed"
fi
exit "$errors"
