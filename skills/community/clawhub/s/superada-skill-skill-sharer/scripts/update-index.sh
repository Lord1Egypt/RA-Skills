#!/bin/bash
# update-index.sh — Update the root README.md skill index
# Usage: update-index.sh <repo-dir> <skill-name> <description>
set -euo pipefail

REPO_DIR="$1"
SKILL_NAME="$2"
DESCRIPTION="$3"
README="$REPO_DIR/README.md"

if [[ ! -f "$README" ]]; then
  echo "❌ No README.md found in $REPO_DIR"
  exit 1
fi

NEW_LINE="| [${SKILL_NAME}](./${SKILL_NAME}/) | ${DESCRIPTION} |"

# Check if skill already in the table
if grep -qF "| [${SKILL_NAME}]" "$README"; then
  # Remove old entry, then re-add
  grep -vF "| [${SKILL_NAME}]" "$README" > "$README.tmp"
  mv "$README.tmp" "$README"
  
  # Find last table line and insert after it
  LAST_TABLE_LINE=$(grep -n "^|" "$README" | tail -1 | cut -d: -f1)
  if [[ -n "$LAST_TABLE_LINE" ]]; then
    head -n "$LAST_TABLE_LINE" "$README" > "$README.tmp"
    echo "$NEW_LINE" >> "$README.tmp"
    tail -n +"$((LAST_TABLE_LINE + 1))" "$README" >> "$README.tmp"
    mv "$README.tmp" "$README"
  else
    echo "$NEW_LINE" >> "$README"
  fi
  echo "✅ Updated existing entry for $SKILL_NAME in README"
else
  # Find last table line and append after it
  LAST_TABLE_LINE=$(grep -n "^|" "$README" | tail -1 | cut -d: -f1)
  
  if [[ -n "$LAST_TABLE_LINE" ]]; then
    head -n "$LAST_TABLE_LINE" "$README" > "$README.tmp"
    echo "$NEW_LINE" >> "$README.tmp"
    tail -n +"$((LAST_TABLE_LINE + 1))" "$README" >> "$README.tmp"
    mv "$README.tmp" "$README"
    echo "✅ Added $SKILL_NAME to README index"
  else
    echo "⚠️  Could not find table in README — appending"
    echo "$NEW_LINE" >> "$README"
  fi
fi
