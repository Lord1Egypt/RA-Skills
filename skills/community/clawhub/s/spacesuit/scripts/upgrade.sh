#!/usr/bin/env bash
#
# spacesuit upgrade.sh — Section-based merge
#
# Replaces content between <!-- SPACESUIT:BEGIN ... --> and <!-- SPACESUIT:END -->
# markers with the latest base content. Preserves everything outside markers.
#
# Unmarked files are preserved unless --adopt-unmarked is explicitly selected.
#
# Usage: ./scripts/upgrade.sh [--workspace /path/to/workspace] [--dry-run]

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

DRY_RUN=false
WORKSPACE=""
ADOPT_UNMARKED=false
BACKUP=""

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --workspace) [[ $# -ge 2 && -n "$2" ]] || { echo "--workspace needs a path" >&2; exit 1; }; WORKSPACE="$2"; shift 2 ;;
    --adopt-unmarked) ADOPT_UNMARKED=true; shift ;;
    --help|-h) echo "Usage: bash upgrade.sh [--workspace PATH | PATH] [--dry-run] [--adopt-unmarked]"; exit 0 ;;
    -*) echo "Unknown option: $1" >&2; exit 1 ;;
    *) [[ -z "$WORKSPACE" ]] || { echo "Only one workspace is supported" >&2; exit 1; }; WORKSPACE="$1"; shift ;;
  esac
done

# Default workspace is two levels up (skills/spacesuit/ → workspace root)
WORKSPACE="${WORKSPACE:-$(cd "$SPACESUIT_DIR/../.." && pwd)}"

echo "🔄 Spacesuit Upgrade v${VERSION}"
echo "   Workspace: $WORKSPACE"
if $DRY_RUN; then
  echo "   Mode: DRY RUN (no changes will be made)"
fi
echo ""

# Track changes
CHANGED=0
SKIPPED=0
ADDED=0

# Map: section name → base file
declare -A SECTION_MAP=(
  ["AGENTS"]="AGENTS.md"
  ["SOUL"]="SOUL.md"
  ["TOOLS"]="TOOLS.md"
  ["HEARTBEAT"]="HEARTBEAT.md"
  ["SECURITY"]="SECURITY.md"
  ["MEMORY"]="MEMORY.md"
)

# Map: section name → target file in workspace
declare -A TARGET_MAP=(
  ["AGENTS"]="AGENTS.md"
  ["SOUL"]="SOUL.md"
  ["TOOLS"]="TOOLS.md"
  ["HEARTBEAT"]="HEARTBEAT.md"
  ["SECURITY"]="SECURITY.md"
  ["MEMORY"]="MEMORY.md"
)

# Validate every target before writing any file. Malformed markers can otherwise
# swallow user content; symlinked instruction files must not escape the workspace.
for section in "${!SECTION_MAP[@]}"; do
  target="$WORKSPACE/${TARGET_MAP[$section]}"
  if [[ -L "$target" ]]; then echo "Refusing symlinked target: ${TARGET_MAP[$section]}" >&2; exit 1; fi
  [[ -f "$target" ]] || continue
  if ! awk -v expected="<!-- SPACESUIT:BEGIN $section -->" '
    /<!-- SPACESUIT:BEGIN/ { if ($0 != expected || seen || inside) bad=1; seen++; inside=1 }
    /<!-- SPACESUIT:END/ { if ($0 != "<!-- SPACESUIT:END -->" || !inside || ended) bad=1; ended++; inside=0 }
    END { exit (bad || inside || seen != ended) ? 1 : 0 }
  ' "$target"; then echo "Malformed managed markers: ${TARGET_MAP[$section]}" >&2; exit 1; fi
done
for target in "$WORKSPACE/.spacesuit-version" "$WORKSPACE/.spacesuit-backups"; do
  [[ ! -L "$target" ]] || { echo "Refusing symlinked version/backup path" >&2; exit 1; }
done
ensure_backup() {
  if [[ -z "$BACKUP" ]]; then
    mkdir -p "$WORKSPACE/.spacesuit-backups"
    BACKUP="$(mktemp -d "$WORKSPACE/.spacesuit-backups/upgrade.XXXXXXXX")"
    if [[ -f "$WORKSPACE/.spacesuit-version" ]]; then
      cp -p "$WORKSPACE/.spacesuit-version" "$BACKUP/.spacesuit-version"
    else
      touch "$BACKUP/.version-was-absent"
    fi
  fi
}
backup_target() {
  local target="$1"
  ensure_backup
  cp -p "$target" "$BACKUP/$(basename "$target")"
}

upgrade_section() {
  local section="$1"
  local base_file="$BASE_DIR/${SECTION_MAP[$section]}"
  local target_file="$WORKSPACE/${TARGET_MAP[$section]}"

  if [[ ! -f "$base_file" ]]; then
    echo "  ⚠️  Base file for $section not found — skipping"
    SKIPPED=$((SKIPPED + 1))
    return 0
  fi

  if [[ ! -f "$target_file" ]]; then
    echo "  ⚠️  Target ${TARGET_MAP[$section]} not found — skipping (run install.sh first)"
    SKIPPED=$((SKIPPED + 1))
    return 0
  fi

  local begin_marker="<!-- SPACESUIT:BEGIN ${section} -->"
  local end_marker="<!-- SPACESUIT:END -->"
  local base_content
  base_content="$(cat "$base_file")"

  # Check if markers exist in target
  if grep -qF "$begin_marker" "$target_file"; then
    # Markers exist — replace content between them
    local tmp_file
    tmp_file="$(mktemp)"

    # Replace content between markers using a temp file for the replacement content
    local replacement_file
    replacement_file="$(mktemp)"
    echo "$base_content" > "$replacement_file"

    awk -v begin="$begin_marker" -v end="$end_marker" -v repfile="$replacement_file" '
      BEGIN { replacing = 0; printed_replacement = 0 }
      $0 == begin {
        print $0
        replacing = 1
        next
      }
      $0 == end {
        if (!printed_replacement) {
          while ((getline line < repfile) > 0) print line
          close(repfile)
          printed_replacement = 1
        }
        replacing = 0
        print $0
        next
      }
      !replacing { print $0 }
    ' "$target_file" > "$tmp_file"

    rm -f "$replacement_file"

    # Check if anything changed
    if diff -q "$target_file" "$tmp_file" > /dev/null 2>&1; then
      echo "  ✅ ${TARGET_MAP[$section]} — already up to date"
      rm -f "$tmp_file"
      return 0
    fi

    # Show diff
    echo "  📝 ${TARGET_MAP[$section]} — changes detected:"
    diff --unified=3 "$target_file" "$tmp_file" | head -40 || true
    echo ""

    if ! $DRY_RUN; then
      backup_target "$target_file"
      cp "$tmp_file" "$target_file"
      echo "  ✅ ${TARGET_MAP[$section]} — updated"
    else
      echo "  🔍 ${TARGET_MAP[$section]} — would update (dry run)"
    fi

    rm -f "$tmp_file"
    CHANGED=$((CHANGED + 1))
  else
    if ! $ADOPT_UNMARKED; then
      echo "  Unmarked ${TARGET_MAP[$section]} preserved; review --adopt-unmarked separately."
      SKIPPED=$((SKIPPED + 1))
      return 0
    fi
    # Explicit migration — prepend base content with markers at top
    echo "  📌 ${TARGET_MAP[$section]} — no markers found, prepending framework section"

    local tmp_file
    tmp_file="$(mktemp)"

    {
      echo "$begin_marker"
      echo "$base_content"
      echo "$end_marker"
      echo ""
      cat "$target_file"
    } > "$tmp_file"

    if ! $DRY_RUN; then
      backup_target "$target_file"
      cp "$tmp_file" "$target_file"
      echo "  ✅ ${TARGET_MAP[$section]} — markers added + content prepended"
    else
      echo "  🔍 ${TARGET_MAP[$section]} — would prepend (dry run)"
    fi

    rm -f "$tmp_file"
    ADDED=$((ADDED + 1))
  fi
}

echo "📄 Upgrading workspace files..."
echo ""

for section in "${!SECTION_MAP[@]}"; do
  upgrade_section "$section"
done

# Update version tracker
if ! $DRY_RUN && [[ "$SKIPPED" -eq 0 ]]; then
  if [[ ! -f "$WORKSPACE/.spacesuit-version" ]] || [[ "$(cat "$WORKSPACE/.spacesuit-version")" != "$VERSION" ]]; then
    ensure_backup
  fi
  echo "$VERSION" > "$WORKSPACE/.spacesuit-version"
fi
[[ -z "$BACKUP" ]] || echo "Rollback backup: $BACKUP (restore saved files to the workspace)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Changed: $CHANGED"
echo "  Added:   $ADDED"
echo "  Skipped: $SKIPPED"
echo "  Version: $VERSION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if $DRY_RUN; then
  echo ""
  echo "🔍 Dry run complete. No files were modified."
  echo "   Run without --dry-run to apply changes."
fi
