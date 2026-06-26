#!/bin/bash
# apply-preset.sh — Apply a preset to the Turing Pyramid
# Usage: apply-preset.sh <preset-name> [--force] [--no-reset]
#        apply-preset.sh --list
#        apply-preset.sh --current

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
ASSETS_DIR="$SKILL_DIR/assets"
PRESETS_DIR="$SKILL_DIR/presets"
CONFIG_FILE="$ASSETS_DIR/needs-config.json"
STATE_FILE="$ASSETS_DIR/needs-state.json"
TEMPLATE_FILE="$ASSETS_DIR/needs-state.template.json"
CROSS_IMPACT_FILE="$ASSETS_DIR/cross-need-impact.json"
TRIGGERS_FILE="$ASSETS_DIR/context-triggers.json"
ACTIVE_PRESET_FILE="$ASSETS_DIR/active-preset.json"
GATE_FILE="$ASSETS_DIR/pending_actions.json"
SNAPSHOT_FILE="$ASSETS_DIR/last-scan-snapshot.json"
BACKUPS_DIR="$ASSETS_DIR/backups"

# Parse args
PRESET_NAME=""
FORCE=false
NO_RESET=false

for arg in "$@"; do
    case "$arg" in
        --list) exec bash "$SCRIPT_DIR/list-presets.sh"; exit 0 ;;
        --current)
            if [[ -f "$ACTIVE_PRESET_FILE" ]]; then
                jq '.' "$ACTIVE_PRESET_FILE"
            else
                echo "No preset applied yet (using default config)"
            fi
            exit 0
            ;;
        --force) FORCE=true ;;
        --no-reset) NO_RESET=true ;;
        -*) echo "Unknown flag: $arg" >&2; exit 1 ;;
        *) PRESET_NAME="$arg" ;;
    esac
done

[[ -z "$PRESET_NAME" ]] && {
    echo "Usage: apply-preset.sh <preset-name> [--force] [--no-reset]"
    echo "       apply-preset.sh --list"
    echo "       apply-preset.sh --current"
    exit 1
}

PRESET_DIR="$PRESETS_DIR/$PRESET_NAME"

# ─── 1. VALIDATE ───
echo "🔺 Applying preset: $PRESET_NAME"
echo ""

[[ -d "$PRESET_DIR" ]] || { echo "Preset not found: $PRESET_DIR" >&2; exit 1; }

PRESET_NEEDS="$PRESET_DIR/needs.json"
PRESET_CROSS="$PRESET_DIR/cross-impact.json"
PRESET_TRIGGERS="$PRESET_DIR/context-triggers.json"

[[ -f "$PRESET_NEEDS" ]] || { echo "Missing: $PRESET_NEEDS" >&2; exit 1; }

# Validate JSON
jq '.' "$PRESET_NEEDS" >/dev/null 2>&1 || { echo "Invalid JSON: $PRESET_NEEDS" >&2; exit 1; }

# Validate structure
has_meta=$(jq 'has("_meta")' "$PRESET_NEEDS")
has_needs=$(jq 'has("needs")' "$PRESET_NEEDS")
[[ "$has_meta" == "true" && "$has_needs" == "true" ]] || {
    echo "Preset needs.json must have _meta and needs keys" >&2; exit 1
}

# Validate each need has required fields
invalid=$(jq -r '.needs | to_entries[] | select(
    (.value.importance | type) != "number" or
    (.value.decay_rate_hours | type) != "number" or
    (.value.actions | type) != "array" or
    (.value.actions | length) == 0
) | .key' "$PRESET_NEEDS")
if [[ -n "$invalid" ]]; then
    echo "Invalid needs (missing importance/decay_rate_hours/actions): $invalid" >&2
    exit 1
fi

# Validate cross-impact references (if file exists)
if [[ -f "$PRESET_CROSS" ]]; then
    need_names=$(jq -r '.needs | keys[]' "$PRESET_NEEDS")
    bad_refs=$(jq -r --argjson names "$(jq '.needs | keys' "$PRESET_NEEDS")" \
        '.impacts[]? | select(
            (.source as $s | $names | index($s) | not) or
            (.target as $t | $names | index($t) | not)
        ) | "\(.source) → \(.target)"' "$PRESET_CROSS" 2>/dev/null)
    if [[ -n "$bad_refs" ]]; then
        echo "Cross-impact references needs not in preset: $bad_refs" >&2
        exit 1
    fi
fi

# Validate trigger references (if file exists)
if [[ -f "$PRESET_TRIGGERS" ]]; then
    bad_trigger_refs=$(jq -r --argjson names "$(jq '.needs | keys' "$PRESET_NEEDS")" \
        '.triggers[]?.boost.needs[]? | select(. as $n | $names | index($n) | not)' \
        "$PRESET_TRIGGERS" 2>/dev/null)
    if [[ -n "$bad_trigger_refs" ]]; then
        echo "Context trigger references needs not in preset: $bad_trigger_refs" >&2
        exit 1
    fi
fi

echo "  ✓ Validation passed"

# ─── Acquire lock (prevent concurrent cycle) ───
exec 200>"$ASSETS_DIR/cycle.lock"
if ! flock -w 10 200; then
    echo "A cycle is running. Wait or retry." >&2
    exit 1
fi

# ─── 2. BACKUP ───
mkdir -p "$BACKUPS_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

for f in "$CONFIG_FILE" "$STATE_FILE" "$CROSS_IMPACT_FILE" "$TRIGGERS_FILE"; do
    if [[ -f "$f" ]]; then
        cp "$f" "$BACKUPS_DIR/$(basename "$f").$TIMESTAMP"
    fi
done
echo "  ✓ Backup created (assets/backups/*.$TIMESTAMP)"

# ─── 3. MERGE needs-config.json ───
# Keep global settings, replace needs section
PRESET_VERSION=$(jq -r '._meta.version // "unknown"' "$PRESET_NEEDS")
NEEDS_COUNT=$(jq '.needs | length' "$PRESET_NEEDS")
ACTIONS_COUNT=$(jq '[.needs[].actions | length] | add' "$PRESET_NEEDS")

if [[ -f "$CONFIG_FILE" ]]; then
    # Merge: keep settings from current, inject needs from preset
    jq --slurpfile preset "$PRESET_NEEDS" '
        .needs = $preset[0].needs |
        ._meta.active_preset = $preset[0]._meta.preset |
        ._meta.preset_version = $preset[0]._meta.version
    ' "$CONFIG_FILE" > "$CONFIG_FILE.tmp.$$" && mv "$CONFIG_FILE.tmp.$$" "$CONFIG_FILE"
else
    # No config exists — create from preset + minimal settings
    cp "$PRESET_NEEDS" "$CONFIG_FILE"
fi
echo "  ✓ needs-config.json updated ($NEEDS_COUNT needs, $ACTIONS_COUNT actions)"

# ─── 4. COPY cross-impact and triggers ───
if [[ -f "$PRESET_CROSS" ]]; then
    cp "$PRESET_CROSS" "$CROSS_IMPACT_FILE"
    impact_count=$(jq '.impacts | length' "$CROSS_IMPACT_FILE")
    echo "  ✓ cross-need-impact.json updated ($impact_count impacts)"
else
    echo '{"_meta":{"preset":"'"$PRESET_NAME"'"},"impacts":[],"settings":{"cascade_limit":3,"min_impact":0.01}}' > "$CROSS_IMPACT_FILE"
    echo "  ✓ cross-need-impact.json reset (no impacts in preset)"
fi

if [[ -f "$PRESET_TRIGGERS" ]]; then
    cp "$PRESET_TRIGGERS" "$TRIGGERS_FILE"
    trigger_count=$(jq '.triggers | length' "$TRIGGERS_FILE")
    echo "  ✓ context-triggers.json updated ($trigger_count triggers)"
else
    echo '{"triggers":[]}' > "$TRIGGERS_FILE"
    echo "  ✓ context-triggers.json reset (no triggers in preset)"
fi

# ─── 5. GENERATE state template ───
# State file is FLAT: {security: {last_satisfied: null}, ...} (no .needs wrapper)
# This matches the format run-cycle.sh and all scripts expect via .[$n] access
jq '.needs | with_entries(.value = {last_satisfied: null})' "$PRESET_NEEDS" > "$TEMPLATE_FILE"
echo "  ✓ needs-state.template.json generated"

# ─── 6. RESET state ───
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if [[ "$NO_RESET" == "true" && -f "$STATE_FILE" ]]; then
    # Carry over matching need names, init new ones at 3.0
    new_needs=$(jq -r '.needs | keys[]' "$PRESET_NEEDS")
    tmp_state=$(mktemp)
    echo "{}" > "$tmp_state"
    for need in $new_needs; do
        old_sat=$(jq -r --arg n "$need" '.[$n].satisfaction // empty' "$STATE_FILE" 2>/dev/null)
        if [[ -n "$old_sat" ]]; then
            jq --arg n "$need" --argjson s "$old_sat" --arg now "$NOW" \
                '. + {($n): {satisfaction: $s, last_satisfied: $now, last_decay_check: $now, surplus: 0, last_surplus_check: $now, last_high_action_at: $now, last_spontaneous_at: $now}}' \
                "$tmp_state" > "$tmp_state.x" && mv "$tmp_state.x" "$tmp_state"
        else
            jq --arg n "$need" --arg now "$NOW" \
                '. + {($n): {satisfaction: 3.0, last_satisfied: $now, last_decay_check: $now, surplus: 0, last_surplus_check: $now, last_high_action_at: $now, last_spontaneous_at: $now}}' \
                "$tmp_state" > "$tmp_state.x" && mv "$tmp_state.x" "$tmp_state"
        fi
    done
    mv "$tmp_state" "$STATE_FILE"
    echo "  ✓ State merged (matching needs carried over, new needs at 3.0)"
else
    # Full reset — generate flat state: {security: {satisfaction: 3.0, ...}, ...}
    jq --arg now "$NOW" '
        with_entries(.value = {
            satisfaction: 3.0,
            last_satisfied: $now,
            last_decay_check: $now,
            surplus: 0,
            last_surplus_check: $now,
            last_high_action_at: $now,
            last_spontaneous_at: $now
        })
    ' "$TEMPLATE_FILE" > "$STATE_FILE"
    echo "  ✓ State reset (all needs at satisfaction 3.0)"
fi

# ─── 7. RESET context snapshot ───
rm -f "$SNAPSHOT_FILE"
echo "  ✓ Context snapshot cleared"

# ─── 8. CLEAR gate (orphan prevention) ───
if [[ -f "$GATE_FILE" ]]; then
    pending=$(jq -r '.pending_count // 0' "$GATE_FILE" 2>/dev/null)
    if (( pending > 0 )); then
        echo "  ⚠ Cleared $pending pending gate actions (old need names)"
    fi
    rm -f "$GATE_FILE"
fi

# ─── 9. WRITE active-preset.json ───
previous_preset="none"
if [[ -f "$ACTIVE_PRESET_FILE" ]]; then
    previous_preset=$(jq -r '.preset // "none"' "$ACTIVE_PRESET_FILE")
fi

jq -n \
    --arg preset "$PRESET_NAME" \
    --arg applied "$NOW" \
    --arg from "presets/$PRESET_NAME" \
    --argjson nc "$NEEDS_COUNT" \
    --argjson ac "$ACTIONS_COUNT" \
    --arg prev "$previous_preset" \
    --arg ver "$PRESET_VERSION" \
    '{preset: $preset, applied_at: $applied, applied_from: $from, needs_count: $nc, actions_count: $ac, previous_preset: $prev, version: $ver}' \
    > "$ACTIVE_PRESET_FILE"

# ─── 10. SUMMARY ───
echo ""
echo "✅ Applied '$PRESET_NAME' (v$PRESET_VERSION)"
echo "   $NEEDS_COUNT needs, $ACTIONS_COUNT actions"
echo "   Previous: $previous_preset (backed up to assets/backups/)"
echo ""
echo "Next: bash scripts/run-cycle.sh --bootstrap"
