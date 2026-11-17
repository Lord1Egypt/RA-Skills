#!/usr/bin/env bash
set -euo pipefail

fail() {
  printf '%s\n' "$1" >&2
  exit 1
}

command -v openclaw >/dev/null 2>&1 || fail "OpenClaw is not available on PATH."
command -v pbpaste >/dev/null 2>&1 || fail "pbpaste is required for the callback helper."
callback_url="$(pbpaste)" || fail "Could not read the clipboard."
case "$callback_url" in
  http://127.0.0.1:8989/oauth/callback\?* | http://localhost:8989/oauth/callback\?*) ;;
  *) fail "Clipboard does not contain the expected OpenClaw localhost callback URL." ;;
esac
query="${callback_url#*\?}"
query="${query%%\#*}"
code=""
IFS='&' read -r -a parameters <<<"$query"
for parameter in "${parameters[@]}"; do
  if [[ "$parameter" == code=* ]]; then
    code="${parameter#code=}"
    break
  fi
done
[[ -n "$code" ]] || fail "Clipboard callback URL has no authorization code."
case "$code" in
  *[!A-Za-z0-9._~-]*) fail "Clipboard callback contains a malformed authorization code." ;;
esac

openclaw mcp login receipt --code "$code"
tools_output="$(openclaw mcp tools receipt --include 'receipt_*' 2>/dev/null)" ||
  fail "Receipt connected, but its tool boundary could not be inspected."
actual="$(printf '%s\n' "$tools_output" | grep -Eo 'receipt_[a-z0-9_]+' | sort -u)"
expected="$(printf '%s\n' \
  receipt_discover receipt_quote receipt_purchase receipt_get_transaction \
  receipt_search_transactions receipt_get_account receipt_get_remedy_options \
  receipt_request_remedy | sort)"
[[ "$actual" == "$expected" ]] ||
  fail "Receipt connected, but the exact eight-tool boundary was not present."
printf '%s\n' \
  "Receipt connection saved and exactly eight universal tools verified. Open:" \
  "https://receiptprotocol.com/dashboard/spendcap?product=spendcap&source=clawhub&skill_version=1.0.1"
