#!/usr/bin/env bash
# /spidershield fix [--dry-run]
# Scan OpenClaw config and auto-fix insecure settings.
# Wraps: spidershield agent-check --fix | --dry-run

set -euo pipefail

MODE="fix"
if [[ "${1:-}" == "--dry-run" ]]; then
  MODE="dry-run"
fi

if [[ "$MODE" == "dry-run" ]]; then
  echo ""
  echo "SpiderShield — Config Fix (DRY RUN — no changes will be made)"
  echo ""
else
  echo ""
  echo "SpiderShield — Config Auto-Fix"
  echo ""
  echo "This will modify your OpenClaw configuration files in ~/.openclaw/"
  echo -n "Continue? [y/N] "
  read -r CONFIRM
  if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
    echo "Cancelled."
    exit 0
  fi
  echo ""
fi

# Resolve CLI: prefer spidershield (open-source, pip install spidershield)
if command -v spidershield &>/dev/null; then
  if [[ "$MODE" == "dry-run" ]]; then
    spidershield agent-check --dry-run
  else
    spidershield agent-check --fix
  fi
elif python3 -c "import spidershield" 2>/dev/null; then
  if [[ "$MODE" == "dry-run" ]]; then
    python3 -m spidershield agent-check --dry-run
  else
    python3 -m spidershield agent-check --fix
  fi
else
  echo "" >&2
  echo "spidershield not installed. To use this command:" >&2
  echo "" >&2
  echo "  pip install spidershield" >&2
  echo "" >&2
  echo "Or use /spidershield check <skill-name> (works without installation)." >&2
  exit 1
fi
