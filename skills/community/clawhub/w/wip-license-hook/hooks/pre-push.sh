#!/usr/bin/env bash
# wip-license-hook — Pre-push hook (advisory alert)
# Warns if upstream license has drifted. Does NOT block push.
#
# Install: cp hooks/pre-push.sh .git/hooks/pre-push && chmod +x .git/hooks/pre-push
# Or: wip-license-hook install

set -uo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"

# Check if wip-license-hook is available
if command -v wip-license-hook &>/dev/null; then
  HOOK_CMD="wip-license-hook"
elif [ -f "$REPO_ROOT/node_modules/.bin/wip-license-hook" ]; then
  HOOK_CMD="$REPO_ROOT/node_modules/.bin/wip-license-hook"
elif command -v npx &>/dev/null; then
  HOOK_CMD="npx @wipcomputer/wip-license-hook"
else
  # No tool available — push proceeds silently
  exit 0
fi

echo ""
echo "🔒 wip-license-hook: Checking license status before push..."
echo ""

cd "$REPO_ROOT"

# Run gate in advisory mode — capture output but NEVER block push
OUTPUT=$($HOOK_CMD gate 2>&1) || true
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo ""
  echo "╔══════════════════════════════════════════════════╗"
  echo "║  ⚠️  LICENSE DRIFT DETECTED                      ║"
  echo "║                                                  ║"
  echo "║  Upstream license may have changed.              ║"
  echo "║  Your push will proceed (it's your code).        ║"
  echo "║                                                  ║"
  echo "║  Run: wip-license-hook scan --verbose            ║"
  echo "║  to review the changes.                          ║"
  echo "╚══════════════════════════════════════════════════╝"
  echo ""
  echo "$OUTPUT"
  echo ""
fi

# ALWAYS exit 0 — pre-push is advisory only
exit 0
