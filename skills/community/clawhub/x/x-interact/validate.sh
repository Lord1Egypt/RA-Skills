#!/bin/bash
# validate.sh — sanity check for SKILL.md

set -e

SKILL="SKILL.md"
if [ ! -f "$SKILL" ]; then
  echo "FAIL: $SKILL not found"
  exit 1
fi

# Check required frontmatter fields
if ! grep -q "^name:" "$SKILL"; then
  echo "FAIL: missing 'name:' field"
  exit 1
fi

if ! grep -q "^description:" "$SKILL"; then
  echo "FAIL: missing 'description:' field"
  exit 1
fi

# Check no TODOs
if grep -qi "TODO\|FIXME\|stub" "$SKILL"; then
  echo "FAIL: found TODO/FIXME/stub content"
  exit 1
fi

# Check line count under 200
LINES=$(wc -l < "$SKILL")
if [ "$LINES" -gt 200 ]; then
  echo "FAIL: SKILL.md is $LINES lines (max 200)"
  exit 1
fi

echo "PASS: SKILL.md validates ($LINES lines)"
exit 0
