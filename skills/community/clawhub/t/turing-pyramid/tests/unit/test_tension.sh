#!/usr/bin/env bash
# Test: Turing-exp tension formula
# tension = dep² + importance × max(0, dep - crisis_threshold)²
# Below threshold: all needs equal. Above: importance amplifies crisis.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
CONFIG_FILE="$SKILL_DIR/assets/needs-config.json"
STATE_FILE="$SKILL_DIR/assets/needs-state.json"
RUN_CYCLE="$SKILL_DIR/scripts/run-cycle.sh"

export WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
export SKIP_SCANS="true"

errors=0
THRESHOLD=$(jq -r '.settings.tension_formula.crisis_threshold // 1.0' "$CONFIG_FILE")

calc_expected() {
    local imp=$1 dep=$2
    local excess=$(echo "scale=4; $dep - $THRESHOLD" | bc -l)
    if (( $(echo "$excess < 0" | bc -l) )); then excess="0"; fi
    echo "scale=1; ($dep * $dep) + ($imp * $excess * $excess)" | bc -l
}

# Test 1: Security at sat=2.0 (dep=1.0 = threshold — crisis term = 0)
echo "Test 1: At threshold — importance should be silent"

cp "$STATE_FILE" "$STATE_FILE.tension_backup"
now_str=$(date -u +%Y-%m-%dT%H:%M:%SZ)
jq --arg t "$now_str" '.security.satisfaction = 2.0 | .security.last_decay_check = $t | .security.last_satisfied = $t' \
    "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

output=$("$RUN_CYCLE" 2>&1)
security_line=$(echo "$output" | grep -E "^\s+security: tension=" | head -1)
actual=$(echo "$security_line" | sed -E 's/.*tension=([0-9.]+).*/\1/')
# dep=1.0, threshold=1.0 → excess=0 → tension = 1² + 10×0 = 1.0
expected=$(calc_expected 10 1.0)

cp "$STATE_FILE.tension_backup" "$STATE_FILE"
rm "$STATE_FILE.tension_backup"

if (( $(echo "$actual == $expected" | bc -l) )); then
    echo "  security (sat=2.0, dep=1.0): tension=$actual — OK (importance silent at threshold)"
else
    echo "  security (sat=2.0, dep=1.0): tension=$actual (expected $expected) — FAIL"
    ((errors++))
fi

# Test 2: Crisis state (sat=0, dep=3.0 — importance fully active)
echo ""
echo "Test 2: Full crisis — importance amplifies"

cp "$STATE_FILE" "$STATE_FILE.tension_backup"
now_str=$(date -u +%Y-%m-%dT%H:%M:%SZ)
jq --arg t "$now_str" '.integrity.satisfaction = 0 | .integrity.last_decay_check = $t | .integrity.last_satisfied = $t' \
    "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

output=$("$RUN_CYCLE" 2>&1)
integrity_line=$(echo "$output" | grep -E "^\s+integrity: tension=" | head -1)
actual=$(echo "$integrity_line" | sed -E 's/.*tension=([0-9.]+).*/\1/')
# dep=3.0, imp=9, excess=2.0 → 9 + 9×4 = 45.0
expected=$(calc_expected 9 3.0)

cp "$STATE_FILE.tension_backup" "$STATE_FILE"
rm "$STATE_FILE.tension_backup"

if (( $(echo "$actual == $expected" | bc -l) )); then
    echo "  integrity (sat=0, dep=3.0): tension=$actual — OK"
else
    echo "  integrity (sat=0, dep=3.0): tension=$actual (expected $expected) — FAIL"
    ((errors++))
fi

# Test 3: Satisfied state (sat=3.0, dep=0 — tension=0)
echo ""
echo "Test 3: Fully satisfied — zero tension"

cp "$STATE_FILE" "$STATE_FILE.tension_backup"
now_str=$(date -u +%Y-%m-%dT%H:%M:%SZ)
jq --arg t "$now_str" '.expression.satisfaction = 3.0 | .expression.last_decay_check = $t | .expression.last_satisfied = $t' \
    "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

output=$("$RUN_CYCLE" 2>&1)

if echo "$output" | grep -qE "^\s+expression: tension="; then
    expression_line=$(echo "$output" | grep -E "^\s+expression: tension=" | head -1)
    actual=$(echo "$expression_line" | sed -E 's/.*tension=([0-9.]+).*/\1/')
    if [[ "$actual" == "0" || "$actual" == "0.0" || "$actual" == ".0" ]]; then
        echo "  expression (sat=3.0): tension=0 — OK"
    else
        echo "  expression (sat=3.0): tension=$actual (expected 0) — FAIL"
        ((errors++))
    fi
else
    echo "  expression (sat=3.0): not shown (tension=0) — OK"
fi

cp "$STATE_FILE.tension_backup" "$STATE_FILE"
rm "$STATE_FILE.tension_backup"

# Test 4: Homeostasis equality — all needs at sat=2.5 should have EQUAL tension
echo ""
echo "Test 4: Homeostasis equality (all sat=2.5, dep=0.5 < threshold)"

cp "$STATE_FILE" "$STATE_FILE.tension_backup"
now_str=$(date -u +%Y-%m-%dT%H:%M:%SZ)
for need in security integrity coherence closure autonomy connection competence understanding recognition expression; do
    jq --arg n "$need" --arg t "$now_str" '.[$n].satisfaction = 2.5 | .[$n].last_decay_check = $t | .[$n].last_satisfied = $t' \
        "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
done

output=$("$RUN_CYCLE" 2>&1)
# All should be 0.25 (0.5² + imp × 0² = 0.25)
expected=$(calc_expected 1 0.5) # importance doesn't matter below threshold

all_equal=true
for need in security integrity coherence closure autonomy connection competence understanding recognition expression; do
    need_line=$(echo "$output" | grep -E "^\s+$need: tension=" | head -1)
    actual=$(echo "$need_line" | sed -E 's/.*tension=([0-9.]+).*/\1/')
    diff=$(echo "scale=4; ($actual - $expected)" | bc -l)
    diff=${diff#-}
    if (( $(echo "$diff > 0.5" | bc -l) )); then
        echo "  $need: tension=$actual (expected ~$expected) — FAIL (not equal!)"
        all_equal=false
        ((errors++))
    fi
done
if $all_equal; then
    echo "  All needs tension ≈ $expected at homeostasis — OK (importance silent)"
fi

cp "$STATE_FILE.tension_backup" "$STATE_FILE"
rm "$STATE_FILE.tension_backup"

# Test 5: Expression crisis beats security homeostasis
echo ""
echo "Test 5: Crisis crossover — expression(dep=2.5) vs security(dep=0.5)"
expr_tension=$(calc_expected 1 2.5)
sec_tension=$(calc_expected 10 0.5)
if (( $(echo "$expr_tension > $sec_tension" | bc -l) )); then
    echo "  expression=$expr_tension > security=$sec_tension — OK (crisis wins)"
else
    echo "  expression=$expr_tension <= security=$sec_tension — FAIL (crisis should win!)"
    ((errors++))
fi

# Test 6: Both in crisis — hierarchy restored
echo ""
echo "Test 6: Dual crisis — security(dep=2.5) vs expression(dep=2.5)"
sec_crisis=$(calc_expected 10 2.5)
expr_crisis=$(calc_expected 1 2.5)
if (( $(echo "$sec_crisis > $expr_crisis" | bc -l) )); then
    echo "  security=$sec_crisis > expression=$expr_crisis — OK (hierarchy in crisis)"
else
    echo "  security=$sec_crisis <= expression=$expr_crisis — FAIL"
    ((errors++))
fi

if [[ $errors -eq 0 ]]; then
    echo ""
    echo "All Turing-exp tension tests passed"
    exit 0
else
    echo ""
    echo "Turing-exp tension tests FAILED: $errors errors"
    exit 1
fi
