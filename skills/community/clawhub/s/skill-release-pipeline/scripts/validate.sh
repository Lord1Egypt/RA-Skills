#!/usr/bin/env bash
# validate.sh — Validate a skill folder structure
# Usage: validate.sh <skill-folder>

set -euo pipefail

FOLDER="${1:-}"
if [[ -z "$FOLDER" ]]; then
  echo "Usage: $0 <skill-folder>"
  exit 1
fi

FOLDER="$(cd "$FOLDER" && pwd)"
ERRORS=0

echo "Validating: $FOLDER"
echo ""

# Check SKILL.md exists
if [[ ! -f "$FOLDER/SKILL.md" ]]; then
  echo "  ✗ SKILL.md not found"
  ERRORS=$((ERRORS + 1))
else
  echo "  ✓ SKILL.md exists"

  # Check frontmatter
  if head -1 "$FOLDER/SKILL.md" | grep -q "^---"; then
    echo "  ✓ YAML frontmatter present"
  else
    echo "  ✗ Missing YAML frontmatter (must start with ---)"
    ERRORS=$((ERRORS + 1))
  fi

  # Check required fields
  if grep -q "^name:" "$FOLDER/SKILL.md"; then
    NAME=$(grep "^name:" "$FOLDER/SKILL.md" | head -1 | sed 's/^name: *//')
    echo "  ✓ name: $NAME"
  else
    echo "  ✗ Missing 'name' in frontmatter"
    ERRORS=$((ERRORS + 1))
  fi

  if grep -q "^description:" "$FOLDER/SKILL.md"; then
    echo "  ✓ description present"
  else
    echo "  ✗ Missing 'description' in frontmatter"
    ERRORS=$((ERRORS + 1))
  fi

  # Check size
  LINES=$(wc -l < "$FOLDER/SKILL.md")
  if [[ $LINES -gt 500 ]]; then
    echo "  ⚠ SKILL.md is $LINES lines (recommended: <500)"
  else
    echo "  ✓ SKILL.md size OK ($LINES lines)"
  fi
fi

# Check LICENSE
if [[ -f "$FOLDER/LICENSE" ]]; then
  echo "  ✓ LICENSE present"
else
  echo "  ⚠ No LICENSE file (recommended: MIT)"
fi

# Check for symlinks
if find "$FOLDER" -type l | grep -q .; then
  echo "  ✗ Symlinks detected (not allowed by ClawHub)"
  ERRORS=$((ERRORS + 1))
else
  echo "  ✓ No symlinks"
fi

# List contents
echo ""
echo "Contents:"
ls -la "$FOLDER" | grep -v "^total" | grep -v "^\."

echo ""
if [[ $ERRORS -eq 0 ]]; then
  echo "✅ Validation passed"
else
  echo "❌ $ERRORS error(s) found"
  exit 1
fi
