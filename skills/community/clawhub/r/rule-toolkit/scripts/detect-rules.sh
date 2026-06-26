#!/usr/bin/env bash
# detect-rules.sh — Dry-run: scan constraint files and report auto-toolable rules
# Usage: bash scripts/detect-rules.sh [project-dir]

set -euo pipefail

DIR="${1:-.}"
cd "$DIR"

echo "=== Rule Toolkit: Dry Run ==="
echo "Scanning: $(pwd)"
echo ""

# --- Platform Detection ---
PLATFORMS=()
FILES=()

if [ -f "CLAUDE.md" ]; then
  PLATFORMS+=("Claude Code")
  FILES+=("CLAUDE.md")
fi

if [ -f "openclaw.json" ] || [ -d ".openclaw" ]; then
  PLATFORMS+=("OpenClaw")
  for f in agents.md soul.md identity.md user.md tools.md bootstrap.md memory.md; do
    [ -f "$f" ] && FILES+=("$f")
  done
fi

if [ -f ".cursorrules" ]; then
  PLATFORMS+=("Cursor")
  FILES+=(".cursorrules")
fi

if [ -f ".github/copilot-instructions.md" ]; then
  PLATFORMS+=("Copilot")
  FILES+=(".github/copilot-instructions.md")
fi

if [ ${#PLATFORMS[@]} -eq 0 ]; then
  echo "No constraint files found. Nothing to analyze."
  exit 0
fi

echo "Platforms: ${PLATFORMS[*]}"
echo "Files found: ${FILES[*]}"
echo ""

# --- Rule Extraction ---
TOTAL_RULES=0
TOOLABLE=0
PROMPT_ONLY=0

declare -A CATEGORIES

for file in "${FILES[@]}"; do
  echo "--- Scanning: $file ---"

  # Count bullet-point rules (lines starting with - or *)
  RULES=$(grep -cE '^\s*[-*]\s+' "$file" 2>/dev/null || echo 0)
  TOTAL_RULES=$((TOTAL_RULES + RULES))

  # Detect auto-toolable patterns
  while IFS= read -r line; do
    lower=$(echo "$line" | tr '[:upper:]' '[:lower:]')

    # Code style
    if echo "$lower" | grep -qE '(indent|semicolon|quote|prettier|format|spacing)'; then
      TOOLABLE=$((TOOLABLE + 1))
      CATEGORIES["code-style"]=$(( ${CATEGORIES["code-style"]:-0} + 1 ))
    fi

    # Naming
    if echo "$lower" | grep -qE '(kebab.case|pascal.case|camel.case|snake.case|naming|file.name)'; then
      TOOLABLE=$((TOOLABLE + 1))
      CATEGORIES["naming"]=$(( ${CATEGORIES["naming"]:-0} + 1 ))
    fi

    # Type safety
    if echo "$lower" | grep -qE '(no any|no as |strict|typescript|type.check)'; then
      TOOLABLE=$((TOOLABLE + 1))
      CATEGORIES["type-safety"]=$(( ${CATEGORIES["type-safety"]:-0} + 1 ))
    fi

    # Git
    if echo "$lower" | grep -qE '(conventional.commit|commitlint|commit.message|pre-commit|lint.before)'; then
      TOOLABLE=$((TOOLABLE + 1))
      CATEGORIES["git"]=$(( ${CATEGORIES["git"]:-0} + 1 ))
    fi

    # Security
    if echo "$lower" | grep -qE '(innerhtml|eval\(|sanitize|no.*dangerous)'; then
      TOOLABLE=$((TOOLABLE + 1))
      CATEGORIES["security"]=$(( ${CATEGORIES["security"]:-0} + 1 ))
    fi

    # Import rules
    if echo "$lower" | grep -qE '(no.default.export|import.*alias|no.*import.*from)'; then
      TOOLABLE=$((TOOLABLE + 1))
      CATEGORIES["import"]=$(( ${CATEGORIES["import"]:-0} + 1 ))
    fi

  done < <(grep -E '^\s*[-*]\s+' "$file" 2>/dev/null || true)

  echo "  Rules found: $RULES"
done

PROMPT_ONLY=$((TOTAL_RULES - TOOLABLE))
[ $PROMPT_ONLY -lt 0 ] && PROMPT_ONLY=0

echo ""
echo "=== Summary ==="
echo "Total rules found: $TOTAL_RULES"
echo "Auto-toolable:     $TOOLABLE"
echo "Prompt-only:       $PROMPT_ONLY"

if [ ${#CATEGORIES[@]} -gt 0 ]; then
  echo ""
  echo "Categories:"
  for cat in "${!CATEGORIES[@]}"; do
    echo "  $cat: ${CATEGORIES[$cat]}"
  done
fi

echo ""
echo "Run the skill to generate actual tool configs."
