#!/usr/bin/env bash
set -euo pipefail

if ! command -v hdc >/dev/null 2>&1; then
  echo "[error] hdc not found. Install HarmonyOS SDK tools first."
  exit 1
fi

echo "[step] checking hdc targets"
hdc list targets || true

TARGETS=$(hdc list targets 2>/dev/null | awk 'NF{print $1}' | tail -n +2)
if [ -z "$TARGETS" ]; then
  echo "[error] no authorized HarmonyOS target found"
  echo "Fixes:"
  echo "  1. Enable Developer Options"
  echo "  2. Enable USB debugging"
  echo "  3. Accept the authorization prompt"
  echo "  4. If wireless, run hdc tconn <ip:port>"
  exit 1
fi

echo "[ok] target(s):"
echo "$TARGETS"

echo "[done] harmonyos readiness check finished"
