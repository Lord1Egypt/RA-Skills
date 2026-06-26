#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

"$BASE_DIR/session-manifest.sh" list --root "$TMP_DIR" >/dev/null
"$BASE_DIR/session-manifest.sh" write \
  --root "$TMP_DIR" \
  --origin "https://example.com" \
  --session-key "acct-a-main" \
  --account-hint "acct-a" \
  --state ready \
  --browser-pid 123 >/dev/null
"$BASE_DIR/session-manifest.sh" write \
  --root "$TMP_DIR" \
  --origin "https://example.com" \
  --session-key "acct-b-main" \
  --account-hint "acct-b" \
  --state ready \
  --browser-pid 456 >/dev/null
test -f "$TMP_DIR/sessions/https___example_com/acct-a-main.json"
"$BASE_DIR/session-manifest.sh" index-show --root "$TMP_DIR" --origin "https://example.com" | grep -q "acct-a-main"
"$BASE_DIR/session-manifest.sh" select --root "$TMP_DIR" --origin "https://example.com" --account-hint "acct-a" | grep -q "acct-a-main"
if "$BASE_DIR/session-manifest.sh" select --root "$TMP_DIR" --origin "https://example.com" >/dev/null 2>&1; then
  echo "expected ambiguous selection to fail"
  exit 1
fi
