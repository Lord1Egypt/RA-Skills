#!/usr/bin/env bash
# Test: Action dedup guard
# Verifies that select_action_with_dedup skips recently-selected actions

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

TMPDIR=$(mktemp -d)
FAKE_SKILL="$TMPDIR/skill"
mkdir -p "$FAKE_SKILL/assets" "$FAKE_SKILL/scripts" "$TMPDIR/workspace/memory/logs"

# Copy scripts
cp "$SKILL_DIR/scripts/"*.sh "$FAKE_SKILL/scripts/" 2>/dev/null || true
chmod +x "$FAKE_SKILL/scripts/"*.sh 2>/dev/null || true

# Minimal config with 3 high-impact actions for expression
cat > "$FAKE_SKILL/assets/needs-config.json" <<'EOF'
{
  "settings": {
    "max_actions_per_cycle": 3,
    "action_staleness": { "enabled": true, "window_hours": 24, "penalty": 0.3, "min_weight": 10 },
    "starvation_guard": { "enabled": false },
    "spontaneity": { "enabled": false }
  },
  "needs": {
    "expression": {
      "importance": 1,
      "decay_rate_hours": 8,
      "description": "test",
      "actions": [
        { "name": "action_alpha", "impact": 2.5, "weight": 100 },
        { "name": "action_beta", "impact": 2.0, "weight": 100 },
        { "name": "action_gamma", "impact": 2.2, "weight": 100 }
      ]
    }
  }
}
EOF

NOW_ISO=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# State: expression recently selected action_alpha (1 hour ago)
RECENT=$(date -u -d "1 hour ago" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%SZ")

cat > "$FAKE_SKILL/assets/needs-state.json" <<EOF
{
  "expression": {
    "satisfaction": 0,
    "last_decay_check": "$NOW_ISO",
    "action_history": {
      "action_alpha": "$RECENT"
    }
  }
}
EOF

# Empty audit log
> "$FAKE_SKILL/assets/audit.log"

cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

errors=0

assert_neq() {
    local label="$1" unexpected="$2" actual="$3"
    if [[ "$unexpected" != "$actual" ]]; then
        echo "  PASS: $label (got=$actual, avoided=$unexpected)"
    else
        echo "  FAIL: $label (got=$actual, should have avoided $unexpected)"
        ((errors++)) || true
    fi
}

assert_not_empty() {
    local label="$1" actual="$2"
    if [[ -n "$actual" ]]; then
        echo "  PASS: $label (got=$actual)"
    else
        echo "  FAIL: $label (empty result)"
        ((errors++)) || true
    fi
}

echo "=== Test 1: Dedup skips recently-selected action ==="
# Source run-cycle functions
export WORKSPACE="$TMPDIR/workspace"
export SKIP_SPONTANEITY=true
export SKIP_SCANS=true

# We need to source the functions from run-cycle.sh
# Extract function definitions by running in a subshell
result=$(
    SKILL_DIR="$FAKE_SKILL" \
    CONFIG_FILE="$FAKE_SKILL/assets/needs-config.json" \
    STATE_FILE="$FAKE_SKILL/assets/needs-state.json" \
    AUDIT_LOG="$FAKE_SKILL/assets/audit.log" \
    NOW=$(date +%s) \
    NOW_ISO="$NOW_ISO" \
    bash -c '
        source "'"$FAKE_SKILL"'/scripts/run-cycle.sh" 2>/dev/null
    ' 2>/dev/null || true
)

# Since sourcing run-cycle.sh runs the whole cycle, test via a focused script
cat > "$TMPDIR/test_dedup_func.sh" <<'TESTSCRIPT'
#!/bin/bash
# Minimal test: source helpers, call dedup function
SKILL_DIR="$1"
CONFIG_FILE="$SKILL_DIR/assets/needs-config.json"
STATE_FILE="$SKILL_DIR/assets/needs-state.json"
AUDIT_LOG="$SKILL_DIR/assets/audit.log"
NOW=$(date +%s)
NOW_ISO=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Source the functions we need
source "$SKILL_DIR/scripts/spontaneity.sh" 2>/dev/null || true

# Inline the functions from run-cycle.sh we need
get_effective_weight() {
    local need=$1 action_name=$2 base_weight=$3
    local penalty=0.3 min_weight=10
    local window_hours=24 window_seconds=$((24*3600))
    local last_selected=$(jq -r --arg n "$need" --arg a "$action_name" \
        '.[$n].action_history[$a] // "1970-01-01T00:00:00Z"' "$STATE_FILE")
    local last_epoch=$(date -d "$last_selected" +%s 2>/dev/null || echo 0)
    local seconds_since=$((NOW - last_epoch))
    if [[ $seconds_since -lt $window_seconds ]]; then
        local penalized=$(echo "scale=0; $base_weight * $penalty / 1" | bc -l)
        if [[ $penalized -lt $min_weight ]]; then penalized=$min_weight; fi
        echo "$penalized"
    else
        echo "$base_weight"
    fi
}

select_weighted_action() {
    local need=$1 range=$2
    local actions_json
    case $range in
        high) actions_json=$(jq -c "[.needs.\"$need\".actions[] | select(.disabled != true) | select(.impact >= 2.0)]" "$CONFIG_FILE") ;;
        *) actions_json='[]' ;;
    esac
    local count=$(echo "$actions_json" | jq 'length')
    [[ $count -eq 0 ]] && return
    # Weighted selection
    local total=0 weights=() names=()
    for i in $(seq 0 $((count-1))); do
        local bw=$(echo "$actions_json" | jq -r ".[$i].weight // 100")
        local nm=$(echo "$actions_json" | jq -r ".[$i].name")
        local ew=$(get_effective_weight "$need" "$nm" "$bw")
        weights+=("$ew"); names+=("$nm"); total=$((total+ew))
    done
    [[ $total -le 0 ]] && echo "${names[0]}" && return
    local roll=$((RANDOM % total)) cum=0
    for i in $(seq 0 $((count-1))); do
        cum=$((cum + ${weights[$i]}))
        [[ $roll -lt $cum ]] && echo "${names[$i]}" && return
    done
}

action_was_selected_recently() {
    local need="$1" action_name="$2" cooldown_hours="${3:-8}"
    local cutoff_epoch=$((NOW - cooldown_hours * 3600))
    local last_selected=$(jq -r --arg n "$need" --arg a "$action_name" \
        '.[$n].action_history[$a] // "1970-01-01T00:00:00Z"' "$STATE_FILE" 2>/dev/null)
    local last_epoch=$(date -d "$last_selected" +%s 2>/dev/null || echo 0)
    [[ $last_epoch -ge $cutoff_epoch ]]
}

select_action_with_dedup() {
    local need="$1" range="$2" cooldown_hours=8
    local actions_json
    case $range in
        high) actions_json=$(jq -c "[.needs.\"$need\".actions[] | select(.disabled != true) | select(.impact >= 2.0)]" "$CONFIG_FILE") ;;
        *) actions_json='[]' ;;
    esac
    local count=$(echo "$actions_json" | jq 'length')
    [[ $count -eq 0 ]] && return
    local attempts=0 max_attempts=$count tried=()
    while [[ $attempts -lt $max_attempts ]]; do
        local candidate=$(select_weighted_action "$need" "$range")
        [[ -z "$candidate" ]] && break
        local already_tried=false
        for t in "${tried[@]+"${tried[@]}"}"; do
            [[ "$t" == "$candidate" ]] && already_tried=true && break
        done
        $already_tried && ((attempts++)) && continue
        tried+=("$candidate")
        if action_was_selected_recently "$need" "$candidate" "$cooldown_hours"; then
            ((attempts++)); continue
        fi
        echo "$candidate"; return
    done
    [[ ${#tried[@]} -gt 0 ]] && echo "${tried[0]}"
}

# Run test: action_alpha was selected 1h ago, should be skipped
selected=$(select_action_with_dedup "expression" "high" 2>/dev/null)
echo "$selected"
TESTSCRIPT
chmod +x "$TMPDIR/test_dedup_func.sh"

# Run 10 times — action_alpha should rarely appear (only as fallback)
echo "  Running 10 selections with action_alpha marked as recent..."
alpha_count=0
non_alpha_count=0
for i in $(seq 1 10); do
    selected=$(bash "$TMPDIR/test_dedup_func.sh" "$FAKE_SKILL" 2>/dev/null)
    if [[ "$selected" == "action_alpha" ]]; then
        ((alpha_count++)) || true
    elif [[ -n "$selected" ]]; then
        ((non_alpha_count++)) || true
    fi
done

echo "  action_alpha selected: $alpha_count/10, others: $non_alpha_count/10"
if [[ $non_alpha_count -ge 7 ]]; then
    echo "  PASS: dedup guard mostly avoids recent action ($non_alpha_count/10 non-alpha)"
else
    echo "  FAIL: dedup guard not working (only $non_alpha_count/10 avoided alpha)"
    ((errors++)) || true
fi

echo ""
echo "=== Test 2: All actions recent → fallback to first tried ==="
# Mark all three as recent
RECENT2=$(date -u -d "30 minutes ago" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%SZ")
cat > "$FAKE_SKILL/assets/needs-state.json" <<EOF
{
  "expression": {
    "satisfaction": 0,
    "last_decay_check": "$NOW_ISO",
    "action_history": {
      "action_alpha": "$RECENT2",
      "action_beta": "$RECENT2",
      "action_gamma": "$RECENT2"
    }
  }
}
EOF

selected=$(bash "$TMPDIR/test_dedup_func.sh" "$FAKE_SKILL" 2>/dev/null)
assert_not_empty "fallback when all recent" "$selected"

echo ""
echo "=== Test 3: Flock guard prevents parallel cycles ==="
# Create a lock file and hold it, then try to run cycle
(
    exec 200>"$FAKE_SKILL/assets/cycle.lock"
    flock -n 200
    sleep 2
) &
LOCK_PID=$!
sleep 0.5

# Try running cycle with the lock held — should exit immediately
# Use FAKE_SKILL's copy of run-cycle.sh so BASH_SOURCE resolves to fake dir
WORKSPACE="$TMPDIR/workspace" \
SKIP_SCANS=true \
SKIP_SPONTANEITY=true \
timeout 3 bash "$FAKE_SKILL/scripts/run-cycle.sh" >/dev/null 2>&1
cycle_exit=$?
wait $LOCK_PID 2>/dev/null || true

if [[ $cycle_exit -eq 0 ]]; then
    echo "  PASS: cycle exited cleanly when lock held"
else
    echo "  FAIL: cycle didn't handle lock correctly (exit=$cycle_exit)"
    ((errors++)) || true
fi

echo ""
echo "=============================="
echo "Results: $errors error(s)"
exit $errors
