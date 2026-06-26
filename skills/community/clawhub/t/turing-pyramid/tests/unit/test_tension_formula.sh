#!/bin/bash
# test_tension_formula.sh — Verify Turing-exp formula math
# tension = dep² + importance × max(0, dep - threshold)²

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
CONFIG="$SKILL_DIR/assets/needs-config.json"

importance=$(jq -r '.needs.security.importance' "$CONFIG")
threshold=$(jq -r '.settings.tension_formula.crisis_threshold // 1.0' "$CONFIG")

# Test: security(imp=10) at sat=2.0 (dep=1.0 = threshold)
# excess = max(0, 1.0 - 1.0) = 0
# tension = 1² + 10 × 0² = 1.0
dep=1
excess=$(echo "scale=4; $dep - $threshold" | bc -l)
if (( $(echo "$excess < 0" | bc -l) )); then excess=0; fi
expected=$(echo "scale=1; ($dep * $dep) + ($importance * $excess * $excess)" | bc -l)

if (( $(echo "$expected == 1.0" | bc -l) )); then
    exit 0
else
    echo "Expected tension=1.0, got tension=$expected (imp=$importance, dep=$dep, threshold=$threshold)"
    exit 1
fi
