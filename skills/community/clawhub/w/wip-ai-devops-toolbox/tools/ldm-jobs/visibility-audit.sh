#!/bin/bash
# visibility-audit.sh ... audit all public repos for missing -private counterparts
# Runs via LDMDevTools.app cron job
# Same pattern as branch-protect.sh

echo "=== Visibility audit: $(date) ==="

ORG="wipcomputer"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HOOK_DIR="$SCRIPT_DIR/../wip-repo-permissions-hook"

if [[ ! -f "$HOOK_DIR/cli.js" ]]; then
  echo "Error: wip-repo-permissions-hook not found at $HOOK_DIR"
  exit 1
fi

node "$HOOK_DIR/cli.js" audit "$ORG"
EXIT_CODE=$?

if [[ $EXIT_CODE -ne 0 ]]; then
  echo ""
  echo "VIOLATIONS FOUND. Some public repos lack -private counterparts."
  echo "Run: node $HOOK_DIR/cli.js audit $ORG"
fi

echo "=== Done ==="
exit $EXIT_CODE
