#!/bin/bash
# SPM Parallel Task Switcher
# Switches between multiple WBS ledgers using .active_ledger pointer
# Usage: bash scripts/switch-ledger.sh <ledger-name>
#        bash scripts/switch-ledger.sh list

set -e
LEDGER_DIR="docs/spm/ledgers"

if [ "$1" = "list" ]; then
  echo "📋 Available ledgers:"
  if [ -d "$LEDGER_DIR" ]; then
    ls -1 "$LEDGER_DIR" 2>/dev/null | while read name; do
      if [ -f "$LEDGER_DIR/$name/ledger.md" ]; then
        active=""
        [ "$(readlink docs/spm/ledger.md 2>/dev/null)" = "ledgers/$name/ledger.md" ] && active=" ← ACTIVE"
        echo "  📁 $name$active"
      fi
    done
  else
    echo "  (no ledgers yet — create with: mkdir -p $LEDGER_DIR/<name>)"
  fi
  exit 0
fi

if [ -z "$1" ]; then
  echo "Usage: bash scripts/switch-ledger.sh <name>"
  echo "       bash scripts/switch-ledger.sh list"
  exit 1
fi

TARGET="$LEDGER_DIR/$1/ledger.md"

if [ ! -f "$TARGET" ]; then
  echo "❌ Ledger not found: $TARGET"
  echo ""
  echo "Create one:"
  echo "  mkdir -p $LEDGER_DIR/$1"
  echo "  cp docs/spm/ledger.md $TARGET"
  exit 1
fi

# If existing ledger.md is a regular file, move it into ledgers/
if [ -f docs/spm/ledger.md ] && [ ! -L docs/spm/ledger.md ]; then
  OLDNAME=$(date +%Y%m%d-%H%M%S)
  mkdir -p "$LEDGER_DIR/$OLDNAME"
  mv docs/spm/ledger.md "$LEDGER_DIR/$OLDNAME/ledger.md"
  echo "📦 Archived current ledger → ledgers/$OLDNAME/"
fi

# Create symlink
rm -f docs/spm/ledger.md
ln -sf "ledgers/$1/ledger.md" docs/spm/ledger.md

echo "✅ Switched to: $1"
echo "   Ledger: $TARGET"
echo ""
echo "   Run 'bash scripts/attest-wbs.sh' to secure this ledger."
echo "   Run 'bash scripts/switch-ledger.sh list' to see all."
