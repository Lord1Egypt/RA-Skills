#!/usr/bin/env bash
set -euo pipefail

NS="${1:-steve}"
LIMIT="${2:-5}"

echo "Checking Telegram namespace: $NS"
if tdl chat ls -n "$NS" --limit "$LIMIT"; then
  echo
  echo "OK: reusable namespace '$NS' is alive"
  exit 0
fi

echo "Namespace '$NS' is not usable. Only then consider re-login or session copy." >&2
exit 1
