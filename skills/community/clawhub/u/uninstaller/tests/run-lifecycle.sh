#!/usr/bin/env bash
# run-lifecycle.sh — Full install → gateway run → uninstall lifecycle.
# Usage: ./tests/run-lifecycle.sh [--preserve-state]
#   --preserve-state  Use --preserve-state on uninstall, then reinstall and verify state inherited

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PRESERVE_STATE=false
[[ "${1:-}" == "--preserve-state" ]] && PRESERVE_STATE=true

echo "=== Step 1: Install OpenClaw ==="
pnpm add -g openclaw@latest

echo ""
echo "=== Step 2: Start Gateway (background, 10s) ==="
openclaw gateway run --bind loopback --port 18789 --force &
GWPID=$!
trap "kill $GWPID 2>/dev/null || true" EXIT
sleep 8
# Check if gateway is listening
if lsof -nP -iTCP:18789 -sTCP:LISTEN 2>/dev/null | head -1; then
  echo "Gateway listening on 18789"
else
  echo "Gateway may not be listening (continuing anyway)"
fi

echo ""
echo "=== Step 3: Run Uninstall ==="
if [[ "$PRESERVE_STATE" == "true" ]]; then
  ./scripts/uninstall-oneshot.sh --preserve-state
else
  ./scripts/uninstall-oneshot.sh --no-backup
fi

echo ""
echo "=== Step 4: Verify ==="
if command -v openclaw &>/dev/null; then
  echo "WARN: openclaw still in PATH"
else
  echo "OK: openclaw removed"
fi
if [[ -d "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}" ]]; then
  if [[ "$PRESERVE_STATE" == "true" ]]; then
    echo "OK: State dir preserved (as expected)"
  else
    echo "WARN: State dir still exists"
  fi
else
  if [[ "$PRESERVE_STATE" == "true" ]]; then
    echo "WARN: State dir missing (expected to be preserved)"
  else
    echo "OK: State dir removed"
  fi
fi

if [[ "$PRESERVE_STATE" == "true" ]]; then
  echo ""
  echo "=== Step 5: Reinstall and verify inheritance ==="
  pnpm add -g openclaw@latest
  if [[ -d "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}" ]]; then
    echo "OK: State inherited after reinstall"
  else
    echo "WARN: State dir missing after reinstall"
  fi
fi

echo ""
echo "=== Lifecycle complete ==="
