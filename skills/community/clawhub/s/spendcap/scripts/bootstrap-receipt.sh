#!/usr/bin/env bash
set -euo pipefail

fail() {
  printf '%s\n' "$1" >&2
  exit 1
}

verify_receipt_tools() {
  local tools_output actual expected
  tools_output="$(openclaw mcp tools receipt --include 'receipt_*' 2>/dev/null)" || return 1
  actual="$(printf '%s\n' "$tools_output" | grep -Eo 'receipt_[a-z0-9_]+' | sort -u)"
  expected="$(printf '%s\n' \
    receipt_discover receipt_quote receipt_purchase receipt_get_transaction \
    receipt_search_transactions receipt_get_account receipt_get_remedy_options \
    receipt_request_remedy | sort)"
  [[ "$actual" == "$expected" ]]
}

command -v openclaw >/dev/null 2>&1 || fail "OpenClaw is not available on PATH."

configured=false
if openclaw mcp show receipt --json >/dev/null 2>&1; then
  configured=true
else
  openclaw mcp set receipt \
    '{"url":"https://receiptprotocol.com/mcp","transport":"streamable-http","auth":"oauth","supportsParallelToolCalls":false}'
fi

if [[ "$configured" == "true" ]] && verify_receipt_tools; then
  printf '%s\n' \
    "RECEIPT_CONNECTION_REUSED" \
    "Existing healthy Receipt connection reused; no OAuth flow was started." \
    "Open https://receiptprotocol.com/dashboard/spendcap?product=spendcap&source=clawhub&skill_version=1.0.1"
  exit 0
fi

login_output=""
if ! login_output="$(openclaw mcp login receipt 2>&1)"; then
  fail "OpenClaw could not start the Receipt OAuth authorization attempt."
fi
authorization_url=""
while IFS= read -r line; do
  if [[ "$line" =~ (https://receiptprotocol\.com/api/public/oauth/authorize\?[^[:space:]]+) ]]; then
    authorization_url="${BASH_REMATCH[1]}"
    break
  fi
done <<<"$login_output"
[[ -n "$authorization_url" ]] || fail "OpenClaw produced no Receipt authorization URL."
authorization_url="${authorization_url}&product=spendcap&source=clawhub&skill_version=1.0.1&platform=openclaw"

printf '%s\n' \
  "RECEIPT_AUTHORIZATION_URL_BEGIN" \
  "$authorization_url" \
  "RECEIPT_AUTHORIZATION_URL_END" \
  "" \
  "After owner approval, copy the entire localhost callback URL and run:" \
  "bash ~/.openclaw/workspace/skills/spendcap/scripts/complete-oauth-from-clipboard.sh" \
  "" \
  "Then open https://receiptprotocol.com/dashboard/spendcap?product=spendcap&source=clawhub&skill_version=1.0.1"
