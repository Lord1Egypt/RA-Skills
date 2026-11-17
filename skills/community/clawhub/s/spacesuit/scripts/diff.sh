#!/usr/bin/env bash
#
# spacesuit diff.sh — Show what would change on upgrade
#
# Compares current SPACESUIT sections in workspace files against latest base content.
#
# Usage: ./scripts/diff.sh [--workspace /path/to/workspace]

set -euo pipefail
if (( BASH_VERSINFO[0] < 4 )); then
  echo "Spacesuit requires Bash 4 or newer; select that bash explicitly." >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SPACESUIT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BASE_DIR="$SPACESUIT_DIR/base"
VERSION_FILE="$SPACESUIT_DIR/VERSION"
[[ -f "$VERSION_FILE" ]] || VERSION_FILE="$SPACESUIT_DIR/version.txt"
VERSION="$(cat "$VERSION_FILE")"

if [[ "${1:-}" == "--workspace" ]]; then shift; fi
[[ $# -le 1 ]] || { echo "Usage: bash diff.sh [--workspace PATH | PATH]" >&2; exit 1; }
WORKSPACE="${1:-$(cd "$SPACESUIT_DIR/../.." && pwd)}"

echo "🔍 Spacesuit Diff — v${VERSION}"
echo "   Workspace: $WORKSPACE"

# Check installed version
if [[ -f "$WORKSPACE/.spacesuit-version" ]]; then
  INSTALLED="$(cat "$WORKSPACE/.spacesuit-version")"
  echo "   Installed:  v${INSTALLED}"
else
  echo "   Installed:  (not installed)"
fi
echo ""

declare -A SECTION_MAP=(
  ["AGENTS"]="AGENTS.md"
  ["SOUL"]="SOUL.md"
  ["TOOLS"]="TOOLS.md"
  ["HEARTBEAT"]="HEARTBEAT.md"
  ["SECURITY"]="SECURITY.md"
  ["MEMORY"]="MEMORY.md"
)

declare -A TARGET_MAP=(
  ["AGENTS"]="AGENTS.md"
  ["SOUL"]="SOUL.md"
  ["TOOLS"]="TOOLS.md"
  ["HEARTBEAT"]="HEARTBEAT.md"
  ["SECURITY"]="SECURITY.md"
  ["MEMORY"]="MEMORY.md"
)

DIFFS=0

for section in "${!SECTION_MAP[@]}"; do
  base_file="$BASE_DIR/${SECTION_MAP[$section]}"
  target_file="$WORKSPACE/${TARGET_MAP[$section]}"
  begin_marker="<!-- SPACESUIT:BEGIN ${section} -->"
  end_marker="<!-- SPACESUIT:END -->"

  if [[ ! -f "$target_file" ]]; then
    echo "  ⚠️  ${TARGET_MAP[$section]} — not found in workspace"
    continue
  fi

  if [[ ! -f "$base_file" ]]; then
    continue
  fi

  if ! grep -qF "$begin_marker" "$target_file"; then
    echo "  📌 ${TARGET_MAP[$section]} — no SPACESUIT markers (preserved unless --adopt-unmarked is selected)"
    DIFFS=$((DIFFS + 1))
    continue
  fi

  # Extract current spacesuit section from target
  current_section="$(awk -v begin="$begin_marker" -v end="$end_marker" '
    $0 == begin { capturing = 1; next }
    $0 == end { capturing = 0; next }
    capturing { print }
  ' "$target_file")"

  # Compare with base
  if diff <(echo "$current_section") "$base_file" > /dev/null 2>&1; then
    echo "  ✅ ${TARGET_MAP[$section]} — up to date"
  else
    echo ""
    echo "  📝 ${TARGET_MAP[$section]} — differences found:"
    diff --unified=3 <(echo "$current_section") "$base_file" | head -60 || true
    echo ""
    DIFFS=$((DIFFS + 1))
  fi
done

echo ""
if [[ $DIFFS -eq 0 ]]; then
  echo "✅ Everything up to date! No changes needed."
else
  echo "📊 $DIFFS file(s) have changes. Run upgrade.sh to apply."
fi
