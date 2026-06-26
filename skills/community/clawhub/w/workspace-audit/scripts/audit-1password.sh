#!/usr/bin/env bash
# Audit 1Password vault items against TOOLS.md references
# Usage: bash scripts/audit-1password.sh [--verbose]
set -euo pipefail

WS="${WS:-$HOME/.openclaw/workspace}"
TOOLS_MD="${TOOLS_MD:-$WS/TOOLS.md}"
VAULT="${OP_VAULT:-}"
VERBOSE="${1:-}"

if [ ! -f "$TOOLS_MD" ]; then
  echo "=== 1Password Vault Audit ==="
  echo ""
  echo "⊘ TOOLS.md not found at $TOOLS_MD — skipping"
  exit 0
fi

# Check if op CLI is available
if ! command -v op &>/dev/null; then
  echo "=== 1Password Vault Audit ==="
  echo ""
  echo "⊘ 1Password CLI (op) not installed — skipping"
  echo "  Install: https://developer.1password.com/docs/cli/get-started/"
  exit 0
fi

# Check if authenticated
if ! op account list &>/dev/null; then
  echo "=== 1Password Vault Audit ==="
  echo ""
  echo "⊘ 1Password CLI not authenticated — skipping"
  echo "  Set OP_SERVICE_ACCOUNT_TOKEN or run: op signin"
  exit 0
fi

echo "=== 1Password Vault Audit ==="
echo ""

# Build vault flag
VAULT_FLAG=""
if [ -n "$VAULT" ]; then
  VAULT_FLAG="--vault $VAULT"
  echo "🔒 Vault: $VAULT"
else
  echo "🔒 Vault: (all vaults)"
fi

# Get all vault items
# shellcheck disable=SC2086
VAULT_ITEMS=$(op item list $VAULT_FLAG --format json 2>/dev/null | python3 -c "
import json,sys
items = json.load(sys.stdin)
for i in items:
    print(i['title'])
" | sort)

if [ -z "$VAULT_ITEMS" ]; then
  echo "⚠️  No items found (check vault name or auth)"
  exit 1
fi

VAULT_COUNT=$(echo "$VAULT_ITEMS" | wc -l | tr -d ' ')
echo "📦 Vault items: $VAULT_COUNT"

# Extract 1Password item references from TOOLS.md
# Looks for patterns like: 1Password: "Item Name" → field
TOOLS_REFS=$(grep -i '1Password:' "$TOOLS_MD" | sed 's/→.*//' | grep -oE '"[^"]+?"' | tr -d '"' | sort -u)

if [ -z "$TOOLS_REFS" ]; then
  echo ""
  echo "⊘ No 1Password references found in TOOLS.md"
  exit 0
fi

echo ""
echo "--- TOOLS.md References vs Vault ---"
MATCH=0
MISS=0
while IFS= read -r ref; do
  [ -z "$ref" ] && continue
  if echo "$VAULT_ITEMS" | grep -qF "$ref"; then
    [ "$VERBOSE" = "--verbose" ] && echo "  ✅ $ref"
    MATCH=$((MATCH + 1))
  else
    echo "  ❌ NOT IN VAULT: \"$ref\""
    MISS=$((MISS + 1))
  fi
done <<< "$TOOLS_REFS"

echo ""
echo "Matched: $MATCH | Missing: $MISS"

echo ""
echo "--- Vault Items NOT in TOOLS.md ---"
UNDOC=0
while IFS= read -r item; do
  [ -z "$item" ] && continue
  if ! grep -qF "\"$item\"" "$TOOLS_MD"; then
    echo "  ⚠️  $item"
    UNDOC=$((UNDOC + 1))
  fi
done <<< "$VAULT_ITEMS"

echo ""
echo "Undocumented: $UNDOC"
echo ""

if [ "$MISS" -gt 0 ]; then
  echo "⚠️  $MISS TOOLS.md reference(s) don't match vault items"
  exit 1
else
  echo "✅ All TOOLS.md references match vault items"
  exit 0
fi
