#!/bin/bash
# Tests for action staleness feature
# Covers: recording, weight penalty, disabled mode, window expiry, min_weight,
# missing history, cleanup, and selectable all-stale actions.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$SKILL_DIR/scripts"
CONFIG_FILE="$SKILL_DIR/assets/needs-config.json"
STATE_FILE="$SKILL_DIR/assets/needs-state.json"

export WORKSPACE="${WORKSPACE:-$SKILL_DIR}"
export SKIP_SCANS="true"
export SKIP_SPONTANEITY="true"
export SKIP_GATE="true"

cp "$CONFIG_FILE" "$CONFIG_FILE.test_bak"
cp "$STATE_FILE" "$STATE_FILE.test_bak"
cleanup() {
    mv "$CONFIG_FILE.test_bak" "$CONFIG_FILE" 2>/dev/null || true
    mv "$STATE_FILE.test_bak" "$STATE_FILE" 2>/dev/null || true
}
trap cleanup EXIT

PASS=0
FAIL=0
TOTAL=0

assert_numeric() {
    local name="$1" op="$2" expected="$3" actual="$4"
    ((TOTAL++)) || true
    if [ "$actual" "$op" "$expected" ]; then
        echo "  ✅ $name (actual=$actual)"
        ((PASS++)) || true
    else
        echo "  ❌ $name"
        echo "     expected: $op $expected, got: $actual"
        ((FAIL++)) || true
    fi
}

assert_eq() {
    local name="$1" expected="$2" actual="$3"
    ((TOTAL++)) || true
    if [[ "$actual" == "$expected" ]]; then
        echo "  ✅ $name"
        ((PASS++)) || true
    else
        echo "  ❌ $name"
        echo "     expected: $expected"
        echo "     got: $actual"
        ((FAIL++)) || true
    fi
}

NOW=$(date +%s)
NOW_ISO=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
export TURING_PYRAMID_SOURCE_ONLY=true
# shellcheck source=/dev/null
source "$SCRIPTS_DIR/run-cycle.sh"

reset_expression() {
    local sat="${1:-0.00}"
    jq --argjson sat "$sat" --arg now "$NOW_ISO" '
      to_entries | map(
        if .key == "expression" then
          .value.satisfaction = $sat |
          .value.last_decay_check = $now |
          .value.last_action_at = $now |
          .value.action_history = {}
        elif .key == "_meta" then .
        else
          .value.satisfaction = 3.00 |
          .value.last_decay_check = $now |
          .value.last_action_at = $now
        end
      ) | from_entries
    ' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
}

configure_staleness() {
    local enabled="$1" penalty="${2:-0.2}" min_weight="${3:-5}"
    jq --argjson enabled "$enabled" --argjson penalty "$penalty" --argjson min_weight "$min_weight" '
      .settings.action_staleness = {
        "enabled": $enabled,
        "window_hours": 24,
        "penalty": $penalty,
        "min_weight": $min_weight
      } |
      .settings.starvation_guard.enabled = false
    ' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
}

select_many() {
    local iterations="$1" target="$2"
    local count=0
    for _ in $(seq 1 "$iterations"); do
        selected=$(select_weighted_action expression high)
        [[ "$selected" == "$target" ]] && ((count++)) || true
    done
    echo "$count"
}

TARGET="write substantial post or essay"

# Deterministic RANDOM sequence for stable statistical assertions.
RANDOM=42

echo "=== Action Staleness Tests ==="
echo ""

echo "Test 1: record_action_selection writes to state"
configure_staleness true
reset_expression 0.00
record_action_selection expression "$TARGET"
HISTORY=$(jq -r '.expression.action_history // {} | keys | length' "$STATE_FILE")
assert_numeric "action_history has entry after record" -ge 1 "$HISTORY"

echo ""
echo "Test 2: stale action receives reduced effective weight"
WEIGHT=$(get_effective_weight expression "$TARGET" 40)
assert_eq "stale weight = base*penalty" "8" "$WEIGHT"

echo ""
echo "Test 3: disabled staleness leaves weight unchanged"
configure_staleness false
WEIGHT_DISABLED=$(get_effective_weight expression "$TARGET" 40)
assert_eq "disabled weight unchanged" "40" "$WEIGHT_DISABLED"

echo ""
echo "Test 4: action outside window is fresh"
configure_staleness true
OLD_TIME=$(date -u -d "48 hours ago" +"%Y-%m-%dT%H:%M:%SZ")
jq --arg old "$OLD_TIME" --arg target "$TARGET" '.expression.action_history = {($target): $old}' \
  "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
WEIGHT_OLD=$(get_effective_weight expression "$TARGET" 40)
assert_eq "expired action weight unchanged" "40" "$WEIGHT_OLD"

echo ""
echo "Test 5: min_weight prevents total suppression"
configure_staleness true 0.01 5
jq --arg now "$NOW_ISO" --arg target "$TARGET" '.expression.action_history = {($target): $now}' \
  "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
WEIGHT_MIN=$(get_effective_weight expression "$TARGET" 40)
assert_eq "penalized weight floored to min_weight" "5" "$WEIGHT_MIN"

echo ""
echo "Test 6: missing action_history is treated as fresh"
configure_staleness true
jq 'del(.expression.action_history)' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
WEIGHT_MISSING=$(get_effective_weight expression "$TARGET" 40)
assert_eq "missing history weight unchanged" "40" "$WEIGHT_MISSING"

echo ""
echo "Test 7: cleanup removes expired entries and keeps recent ones"
OLD_TIME=$(date -u -d "48 hours ago" +"%Y-%m-%dT%H:%M:%SZ")
jq --arg old "$OLD_TIME" --arg now "$NOW_ISO" --arg target "$TARGET" '
  .expression.action_history = {
    "old expired action": $old,
    ($target): $now
  }
' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
record_action_selection expression "develop scratchpad idea into finished piece"
OLD_ENTRY=$(jq -r '.expression.action_history["old expired action"] // "GONE"' "$STATE_FILE")
REMAINING=$(jq -r '.expression.action_history | keys | length' "$STATE_FILE")
assert_eq "expired entry removed" "GONE" "$OLD_ENTRY"
assert_numeric "recent entries kept" -ge 2 "$REMAINING"

echo ""
echo "Test 8: stale action shifts weighted selection distribution"
configure_staleness true 0.2 5
jq --arg now "$NOW_ISO" --arg target "$TARGET" '.expression.action_history = {($target): $now}' \
  "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
RANDOM=42
stale_count=$(select_many 80 "$TARGET")
assert_numeric "stale action selected less often (< 25 of 80)" -lt 25 "$stale_count"

configure_staleness false
RANDOM=42
disabled_count=$(select_many 80 "$TARGET")
assert_numeric "disabled penalty selects target more often" -gt "$stale_count" "$disabled_count"

echo ""
echo "Test 9: all stale actions remain selectable via min_weight"
configure_staleness true 0.01 5
jq --arg now "$NOW_ISO" '
  .expression.action_history = {
    "write substantial post or essay": $now,
    "develop scratchpad idea into finished piece": $now,
    "create something new (script, tool, doc)": $now
  }
' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
selected=$(select_weighted_action expression high)
if [[ -n "$selected" ]]; then
    echo "  ✅ all stale still selected: $selected"
    ((PASS++)) || true
else
    echo "  ❌ all stale produced no selection"
    ((FAIL++)) || true
fi
((TOTAL++)) || true

echo ""
echo "=== Results: $PASS/$TOTAL passed, $FAIL failed ==="
exit "$FAIL"
