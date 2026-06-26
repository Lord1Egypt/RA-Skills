#!/bin/bash
# list-presets.sh — Show available Turing Pyramid presets

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PRESETS_DIR="$SKILL_DIR/presets"
ACTIVE_FILE="$SKILL_DIR/assets/active-preset.json"

echo "🔺 Available Presets"
echo "─────────────────────"
echo ""

for preset_dir in "$PRESETS_DIR"/*/; do
    [[ -d "$preset_dir" ]] || continue
    needs_file="$preset_dir/needs.json"
    [[ -f "$needs_file" ]] || continue

    name=$(jq -r '._meta.preset // "unknown"' "$needs_file")
    display_name=$(jq -r '._meta.name // .meta.preset' "$needs_file")
    needs_count=$(jq '.needs | length' "$needs_file")
    actions_count=$(jq '[.needs[].actions | length] | add' "$needs_file")
    desc=$(jq -r '._meta.description // ""' "$needs_file" | head -c 80)

    printf "  %-22s %2d needs, %3d actions   %s\n" "$name" "$needs_count" "$actions_count" "$desc"
done

echo ""
if [[ -f "$ACTIVE_FILE" ]]; then
    active=$(jq -r '.preset // "none"' "$ACTIVE_FILE")
    applied=$(jq -r '.applied_at // "unknown"' "$ACTIVE_FILE")
    echo "  Active: $active (applied $applied)"
else
    echo "  Active: none (using default config)"
fi
echo ""
echo "  Apply: bash scripts/apply-preset.sh <name>"
