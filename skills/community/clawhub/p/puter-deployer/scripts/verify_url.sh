#!/usr/bin/env bash
set -euo pipefail

URL="${1:?usage: verify_url.sh <url> [expected_snippet]}"
SNIPPET="${2:-}"

TMP="$(mktemp)"
CODE=$(curl -sSL -o "$TMP" -w "%{http_code}" "$URL" || true)

if [ "$CODE" != "200" ]; then
  echo "FAIL: HTTP $CODE from $URL"
  rm -f "$TMP"
  exit 10
fi

if [ -n "$SNIPPET" ]; then
  if ! grep -Fq "$SNIPPET" "$TMP"; then
    echo "FAIL: snippet not found: $SNIPPET"
    rm -f "$TMP"
    exit 11
  fi
fi

echo "OK: verified $URL (HTTP 200)"
rm -f "$TMP"
