#!/usr/bin/env bash
# setup-wizard.sh — Scaffold First-Run Setup
#
# Personalizes your Scaffold workspace in under 2 minutes.
# Replaces all [YOUR_HUMAN] placeholders and configures core identity files.
#
# Run from your workspace root: bash setup-wizard.sh

set -euo pipefail

WORKSPACE="${WORKSPACE:-$(pwd)}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🏗  Scaffold Setup Wizard"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Personalizes your workspace in ~2 minutes."
echo "You can always re-run this or edit files manually."
echo ""

# ── Collect inputs ──────────────────────────────────────────────────────────

read -rp "1. What should your agent call you? (e.g. Aubs, Alex, J): " YOUR_HUMAN
if [[ -z "$YOUR_HUMAN" ]]; then
  echo "ERROR: Name is required." >&2; exit 1
fi

read -rp "2. Your timezone (e.g. America/New_York, Europe/London, Asia/Tokyo): " TIMEZONE
TIMEZONE="${TIMEZONE:-America/New_York}"

read -rp "3. What do you want to name your agent? (e.g. Vesper, Nova, Cipher — or press Enter to decide later): " AGENT_NAME
AGENT_NAME="${AGENT_NAME:-[NAME PENDING]}"

echo ""
echo "   Available model tiers:"
echo "   1) anthropic/claude-haiku-4-5-20251001  (fast, cheap — good for most things)"
echo "   2) anthropic/claude-sonnet-4-6          (balanced — recommended default)"
echo "   3) anthropic/claude-opus-4-6            (most capable — use for complex work)"
echo "   4) Enter custom model ID"
read -rp "4. Default model [1-4, default=2]: " MODEL_CHOICE
case "${MODEL_CHOICE:-2}" in
  1) DEFAULT_MODEL="anthropic/claude-haiku-4-5-20251001" ;;
  3) DEFAULT_MODEL="anthropic/claude-opus-4-6" ;;
  4) read -rp "   Enter model ID: " DEFAULT_MODEL ;;
  *) DEFAULT_MODEL="anthropic/claude-sonnet-4-6" ;;
esac

read -rp "5. What are you primarily working toward? (one sentence — e.g. 'building a passive income business'): " PRIMARY_GOAL
PRIMARY_GOAL="${PRIMARY_GOAL:-[To be filled in]}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Applying configuration..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── Sanitize user inputs for safe sed substitution ─────────────────────────
# Escapes /, \, & which are special characters in sed replacement strings

escape_sed() {
  printf '%s' "$1" | sed 's/[\/&]/\\&/g'
}

SAFE_HUMAN=$(escape_sed "$YOUR_HUMAN")
SAFE_AGENT=$(escape_sed "$AGENT_NAME")

# ── Replace [YOUR_HUMAN] in all markdown files ──────────────────────────────

REPLACED_FILES=()
while IFS= read -r -d '' file; do
  if grep -q "\[YOUR_HUMAN\]" "$file" 2>/dev/null; then
    sed -i "s/\[YOUR_HUMAN\]/${SAFE_HUMAN}/g" "$file"
    REPLACED_FILES+=("$(basename "$file")")
  fi
done < <(find "$WORKSPACE" -maxdepth 2 -name "*.md" -o -name "*.sh" | tr '\n' '\0')

if [[ ${#REPLACED_FILES[@]} -gt 0 ]]; then
  echo "✓ Replaced [YOUR_HUMAN] with '${YOUR_HUMAN}' in:"
  for f in "${REPLACED_FILES[@]}"; do
    echo "  - $f"
  done
else
  echo "• No [YOUR_HUMAN] placeholders found (already configured?)"
fi

# ── Update IDENTITY.md ───────────────────────────────────────────────────────

IDENTITY_FILE="$WORKSPACE/IDENTITY.md"
if [[ -f "$IDENTITY_FILE" ]]; then
  sed -i "s/\[NAME PENDING\]/${SAFE_AGENT}/g" "$IDENTITY_FILE"
  sed -i "s/\[not set yet\]/${SAFE_AGENT}/g" "$IDENTITY_FILE"
  echo "✓ IDENTITY.md — agent name set to '${AGENT_NAME}'"
fi

# ── Update TOOLS.md with timezone ───────────────────────────────────────────

TOOLS_FILE="$WORKSPACE/TOOLS.md"
if [[ -f "$TOOLS_FILE" ]]; then
  if ! grep -q "Timezone:" "$TOOLS_FILE"; then
    echo "" >> "$TOOLS_FILE"
    echo "## Environment" >> "$TOOLS_FILE"
    echo "- **Timezone:** ${TIMEZONE}" >> "$TOOLS_FILE"
    echo "- **Default model:** ${DEFAULT_MODEL}" >> "$TOOLS_FILE"
    echo "✓ TOOLS.md — timezone and model recorded"
  else
    echo "• TOOLS.md already has timezone entry (skipped)"
  fi
fi

# ── Seed MEMORY.md with primary goal ────────────────────────────────────────

MEMORY_FILE="$WORKSPACE/MEMORY.md"
if [[ -f "$MEMORY_FILE" ]] && ! grep -q "Primary Goal" "$MEMORY_FILE"; then
  echo "" >> "$MEMORY_FILE"
  echo "## Setup" >> "$MEMORY_FILE"
  echo "- **Name:** ${YOUR_HUMAN}" >> "$MEMORY_FILE"
  echo "- **Timezone:** ${TIMEZONE}" >> "$MEMORY_FILE"
  echo "- **Primary Goal:** ${PRIMARY_GOAL}" >> "$MEMORY_FILE"
  echo "- **Agent Name:** ${AGENT_NAME}" >> "$MEMORY_FILE"
  echo "✓ MEMORY.md — seeded with your profile"
fi

# ── Done ─────────────────────────────────────────────────────────────────────

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ Setup complete"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Name:    ${YOUR_HUMAN}"
echo "  Agent:   ${AGENT_NAME}"
echo "  Model:   ${DEFAULT_MODEL}"
echo "  TZ:      ${TIMEZONE}"
echo "  Goal:    ${PRIMARY_GOAL}"
echo ""
echo "  Next: open a new session and say 'I'm ready for the first session.'"
echo "  Your agent knows what to do from there."
echo ""
