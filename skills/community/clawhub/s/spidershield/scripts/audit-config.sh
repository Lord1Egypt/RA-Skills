#!/usr/bin/env bash
# /spidershield audit-config [--skills] [--verify] [--json] [--sarif]
# Scan your OpenClaw installation for security issues (10 config checks).
# Wraps: spidershield agent-check [--skills] [--verify]

set -euo pipefail

EXTRA_FLAGS=""

# Parse optional flags — warn on unknown
while [[ $# -gt 0 ]]; do
  case "$1" in
    --skills)  EXTRA_FLAGS="$EXTRA_FLAGS --skills"; shift ;;
    --verify)  EXTRA_FLAGS="$EXTRA_FLAGS --verify"; shift ;;
    --json)    EXTRA_FLAGS="$EXTRA_FLAGS --format json"; shift ;;
    --sarif)   EXTRA_FLAGS="$EXTRA_FLAGS --format sarif"; shift ;;
    -*)
      echo "Warning: unknown option '$1' (ignored)" >&2
      shift ;;
    *)
      echo "Warning: unexpected argument '$1' (ignored)" >&2
      shift ;;
  esac
done

echo ""
echo "SpiderShield — OpenClaw Config Audit"
echo ""

# Resolve CLI: prefer spidershield (open-source, pip install spidershield)
if command -v spidershield &>/dev/null; then
  # shellcheck disable=SC2086
  spidershield agent-check $EXTRA_FLAGS
elif python3 -c "import spidershield" 2>/dev/null; then
  # shellcheck disable=SC2086
  python3 -m spidershield agent-check $EXTRA_FLAGS
else
  echo "" >&2
  echo "spidershield not installed. To use this command:" >&2
  echo "" >&2
  echo "  pip install spidershield" >&2
  echo "" >&2
  echo "Or use /spidershield check <skill-name> (works without installation)." >&2
  exit 1
fi
