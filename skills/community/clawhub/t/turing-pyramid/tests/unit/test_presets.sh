#!/usr/bin/env bash
# Test: Preset system — apply, validate, switch, edge cases
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
SCRIPTS="$SKILL_DIR/scripts"
ASSETS="$SKILL_DIR/assets"

export WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
export SKIP_GATE=true
export SKIP_SCANS=true
errors=0

# Backup current state
cp "$ASSETS/needs-config.json" "/tmp/tp-preset-test-config-backup.json"
cp "$ASSETS/needs-state.json" "/tmp/tp-preset-test-state-backup.json" 2>/dev/null || true
cp "$ASSETS/cross-need-impact.json" "/tmp/tp-preset-test-cross-backup.json"
cp "$ASSETS/context-triggers.json" "/tmp/tp-preset-test-triggers-backup.json"
cp "$ASSETS/active-preset.json" "/tmp/tp-preset-test-active-backup.json" 2>/dev/null || true

restore() {
    cp "/tmp/tp-preset-test-config-backup.json" "$ASSETS/needs-config.json"
    cp "/tmp/tp-preset-test-state-backup.json" "$ASSETS/needs-state.json" 2>/dev/null || true
    cp "/tmp/tp-preset-test-cross-backup.json" "$ASSETS/cross-need-impact.json"
    cp "/tmp/tp-preset-test-triggers-backup.json" "$ASSETS/context-triggers.json"
    cp "/tmp/tp-preset-test-active-backup.json" "$ASSETS/active-preset.json" 2>/dev/null || true
    rm -f "$ASSETS/pending_actions.json" "$ASSETS"/*.lock
    rm -f /tmp/tp-preset-test-*.json
}
trap restore EXIT

# ─── Test 1: list-presets shows available presets ───
echo "Test 1: list-presets"
output=$(bash "$SCRIPTS/list-presets.sh" 2>&1)
if echo "$output" | grep -q "default" && echo "$output" | grep -q "personal-assistant"; then
    echo "  Both presets listed — OK"
else
    echo "  FAIL: missing presets in list"
    ((errors++))
fi

# ─── Test 2: apply default preset ───
echo "Test 2: apply default"
output=$(bash "$SCRIPTS/apply-preset.sh" default --force 2>&1)
if echo "$output" | grep -q "Applied 'default'" && [[ -f "$ASSETS/active-preset.json" ]]; then
    active=$(jq -r '.preset' "$ASSETS/active-preset.json")
    if [[ "$active" == "default" ]]; then
        echo "  Default applied, active-preset correct — OK"
    else
        echo "  FAIL: active preset = $active"
        ((errors++))
    fi
else
    echo "  FAIL: apply-preset output: $output"
    ((errors++))
fi

# ─── Test 3: default has 10 needs ───
echo "Test 3: default needs count"
count=$(jq '.needs | length' "$ASSETS/needs-config.json")
if [[ "$count" == "10" ]]; then
    echo "  10 needs — OK"
else
    echo "  FAIL: $count needs (expected 10)"
    ((errors++))
fi

# ─── Test 4: apply personal-assistant ───
echo "Test 4: apply personal-assistant"
output=$(bash "$SCRIPTS/apply-preset.sh" personal-assistant --force 2>&1)
if echo "$output" | grep -q "Applied 'personal-assistant'"; then
    count=$(jq '.needs | length' "$ASSETS/needs-config.json")
    if [[ "$count" == "5" ]]; then
        echo "  5 needs — OK"
    else
        echo "  FAIL: $count needs (expected 5)"
        ((errors++))
    fi
else
    echo "  FAIL: $output"
    ((errors++))
fi

# ─── Test 5: PA needs are correct names ───
echo "Test 5: PA need names"
needs=$(jq -r '.needs | keys[]' "$ASSETS/needs-config.json" | sort | tr '\n' ',')
expected="accuracy,context_awareness,organization,proactivity,task_completion,"
if [[ "$needs" == "$expected" ]]; then
    echo "  Correct PA needs — OK"
else
    echo "  FAIL: needs=$needs expected=$expected"
    ((errors++))
fi

# ─── Test 6: state was reset with PA needs ───
# State is FLAT format: {task_completion: {...}, accuracy: {...}, ...} (no .needs wrapper)
echo "Test 6: state has PA needs"
state_needs=$(jq -r 'keys[] | select(. != "_meta" and . != "history")' "$ASSETS/needs-state.json" 2>/dev/null | sort | tr '\n' ',')
if [[ "$state_needs" == "$expected" ]]; then
    echo "  State matches PA needs — OK"
else
    echo "  FAIL: state needs=$state_needs"
    ((errors++))
fi

# ─── Test 7: PA preset config persists ───
echo "Test 7: PA preset config persists"
needs=$(jq -r '.needs | keys[]' "$ASSETS/needs-config.json" | sort | tr '\n' ',')
if [[ "$needs" == "$expected" ]]; then
    echo "  PA needs still in config — OK"
else
    echo "  FAIL: needs=$needs (expected $expected)"
    ((errors++))
fi

# ─── Test 8: global settings preserved across preset switch ───
echo "Test 8: settings preserved"
bash "$SCRIPTS/apply-preset.sh" default --force >/dev/null 2>&1
settings_before=$(jq '.settings.tension_formula.crisis_threshold' "$ASSETS/needs-config.json")
bash "$SCRIPTS/apply-preset.sh" personal-assistant --force >/dev/null 2>&1
settings_after=$(jq '.settings.tension_formula.crisis_threshold' "$ASSETS/needs-config.json")
if [[ "$settings_before" == "$settings_after" ]]; then
    echo "  Settings preserved — OK"
else
    echo "  FAIL: before=$settings_before after=$settings_after"
    ((errors++))
fi

# ─── Test 9: cross-impact updated on preset switch ───
echo "Test 9: cross-impact per preset"
bash "$SCRIPTS/apply-preset.sh" personal-assistant --force >/dev/null 2>&1
pa_sources=$(jq -r '.impacts[].source' "$ASSETS/cross-need-impact.json" | sort -u | tr '\n' ',')
if echo "$pa_sources" | grep -q "task_completion"; then
    echo "  PA cross-impacts present — OK"
else
    echo "  FAIL: sources=$pa_sources"
    ((errors++))
fi

# ─── Test 10: invalid preset rejected ───
echo "Test 10: invalid preset"
output=$(bash "$SCRIPTS/apply-preset.sh" nonexistent --force 2>&1 || true)
if echo "$output" | grep -q "not found"; then
    echo "  Invalid preset rejected — OK"
else
    echo "  FAIL: should have rejected"
    ((errors++))
fi

# ─── Test 11: backup created ───
echo "Test 11: backups exist"
backup_count=$(ls "$ASSETS/backups/" 2>/dev/null | wc -l)
if (( backup_count > 0 )); then
    echo "  Backups created ($backup_count files) — OK"
else
    echo "  FAIL: no backups found"
    ((errors++))
fi

# ─── Test 12: idempotent apply ───
echo "Test 12: idempotent apply"
bash "$SCRIPTS/apply-preset.sh" default --force >/dev/null 2>&1
hash1=$(jq -Sc '.needs' "$ASSETS/needs-config.json" | md5sum | cut -d' ' -f1)
bash "$SCRIPTS/apply-preset.sh" default --force >/dev/null 2>&1
hash2=$(jq -Sc '.needs' "$ASSETS/needs-config.json" | md5sum | cut -d' ' -f1)
if [[ "$hash1" == "$hash2" ]]; then
    echo "  Idempotent — OK"
else
    echo "  FAIL: hashes differ"
    ((errors++))
fi

# ─── Summary ───
echo ""
if [[ $errors -eq 0 ]]; then
    echo "All preset tests passed (12/12)"
    exit 0
else
    echo "Preset tests FAILED: $errors errors"
    exit 1
fi
