#!/usr/bin/env bash
# wip-license-hook — Pre-pull hook (hard gate)
# Blocks pull/merge if upstream license has changed.
#
# Install: cp hooks/pre-pull.sh .git/hooks/pre-merge-commit && chmod +x .git/hooks/pre-merge-commit
# Or: wip-license-hook install

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"

# Check if wip-license-hook is available
if command -v wip-license-hook &>/dev/null; then
  HOOK_CMD="wip-license-hook"
elif [ -f "$REPO_ROOT/node_modules/.bin/wip-license-hook" ]; then
  HOOK_CMD="$REPO_ROOT/node_modules/.bin/wip-license-hook"
elif command -v npx &>/dev/null; then
  HOOK_CMD="npx @wipcomputer/wip-license-hook"
else
  echo ""
  echo "╔══════════════════════════════════════════════════╗"
  echo "║  ⚠️  wip-license-hook not found                  ║"
  echo "║  Install: npm i -g @wipcomputer/wip-license-hook ║"
  echo "║  Pull proceeding WITHOUT license check.          ║"
  echo "╚══════════════════════════════════════════════════╝"
  echo ""
  exit 0
fi

echo ""
echo "🔒 wip-license-hook: Checking upstream licenses..."
echo ""

# Run the gate check — exits non-zero if license changed
cd "$REPO_ROOT"
$HOOK_CMD gate

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo ""
  echo "╔══════════════════════════════════════════════════╗"
  echo "║  🚫  MERGE BLOCKED — License change detected!   ║"
  echo "║                                                  ║"
  echo "║  Review the changes above. If you accept the     ║"
  echo "║  new license, update the ledger:                 ║"
  echo "║    wip-license-hook scan                         ║"
  echo "║                                                  ║"
  echo "║  Then retry the pull/merge.                      ║"
  echo "╚══════════════════════════════════════════════════╝"
  echo ""
  exit 1
fi

exit 0
