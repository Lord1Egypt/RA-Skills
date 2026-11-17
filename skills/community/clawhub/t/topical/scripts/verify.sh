#!/usr/bin/env bash
# Quick checks after Topical ↔ OpenClaw wiring.
set -euo pipefail

TRANSFORMS_DIR="${OPENCLAW_HOOKS_TRANSFORMS:-${HOME}/.openclaw/hooks/transforms}"
CONFIG="${HOME}/.openclaw/openclaw.json"
FAIL=0

check() {
  if "$@"; then
    echo "✓ $*"
  else
    echo "✗ $*"
    FAIL=1
  fi
}

[[ -f "${TRANSFORMS_DIR}/topical-inbound.mjs" ]] && echo "✓ transform installed" || { echo "✗ missing ${TRANSFORMS_DIR}/topical-inbound.mjs"; FAIL=1; }
[[ -f "${TRANSFORMS_DIR}/topical.config.json" ]] && echo "✓ topical.config.json present" || { echo "✗ missing ${TRANSFORMS_DIR}/topical.config.json"; FAIL=1; }
[[ -f "${CONFIG}" ]] && echo "✓ openclaw.json present" || { echo "✗ missing ${CONFIG}"; FAIL=1; }

if command -v openclaw >/dev/null 2>&1; then
  if openclaw mcp list 2>&1 | grep -qi topical; then
    echo "✓ openclaw mcp list shows topical"
  else
    echo "✗ topical MCP server not listed — run openclaw mcp set topical …"
    FAIL=1
  fi
else
  echo "⚠ openclaw CLI not in PATH — skipped mcp list"
fi

exit "${FAIL}"
