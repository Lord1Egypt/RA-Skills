#!/usr/bin/env bash
set -euo pipefail

STRIPE_WEBHOOK_URL="${STRIPE_WEBHOOK_URL:-}"
STRIPE_WEBHOOK_SECRET="${STRIPE_WEBHOOK_SECRET:-}"
STRIPE_EVENT_PATH="${STRIPE_EVENT_PATH:-fixtures/sample-checkout-session-completed.json}"
STRIPE_EVENT_JSON="${STRIPE_EVENT_JSON:-}"
REPLAY_COUNT="${REPLAY_COUNT:-2}"
REPLAY_DELAY_SECONDS="${REPLAY_DELAY_SECONDS:-0}"
REQUEST_TIMEOUT_SECONDS="${REQUEST_TIMEOUT_SECONDS:-15}"
ACCEPT_HTTP_CODES="${ACCEPT_HTTP_CODES:-}"

require_bin() {
  local bin="$1"
  command -v "$bin" >/dev/null 2>&1 || {
    echo "FAIL: required binary not found: ${bin}" >&2
    exit 1
  }
}

for b in bash curl openssl python3; do
  require_bin "$b"
done

if [[ -z "$STRIPE_WEBHOOK_URL" ]]; then
  echo "FAIL: STRIPE_WEBHOOK_URL is required"
  exit 1
fi

if [[ -z "$STRIPE_WEBHOOK_SECRET" ]]; then
  echo "FAIL: STRIPE_WEBHOOK_SECRET is required"
  exit 1
fi

if ! [[ "$REPLAY_COUNT" =~ ^[1-9][0-9]*$ ]]; then
  echo "FAIL: REPLAY_COUNT must be a positive integer"
  exit 1
fi

if ! [[ "$REQUEST_TIMEOUT_SECONDS" =~ ^[1-9][0-9]*$ ]]; then
  echo "FAIL: REQUEST_TIMEOUT_SECONDS must be a positive integer"
  exit 1
fi

if ! python3 - <<'PY' "$REPLAY_DELAY_SECONDS"
import sys
try:
    v = float(sys.argv[1])
except Exception:
    raise SystemExit(1)
raise SystemExit(0 if v >= 0 else 1)
PY
then
  echo "FAIL: REPLAY_DELAY_SECONDS must be a non-negative number"
  exit 1
fi

load_payload() {
  if [[ -n "$STRIPE_EVENT_JSON" ]]; then
    printf '%s' "$STRIPE_EVENT_JSON"
    return
  fi

  if [[ ! -f "$STRIPE_EVENT_PATH" ]]; then
    echo "FAIL: STRIPE_EVENT_PATH does not exist: $STRIPE_EVENT_PATH" >&2
    exit 1
  fi

  cat "$STRIPE_EVENT_PATH"
}

payload="$(load_payload)"

if ! python3 - <<'PY' "$payload"
import json, sys
json.loads(sys.argv[1])
PY
then
  echo "FAIL: payload is not valid JSON"
  exit 1
fi

read -r event_id event_type < <(python3 - <<'PY' "$payload"
import json, sys
obj = json.loads(sys.argv[1])
print((obj.get("id") or "<unknown>").replace(" ", "_"), (obj.get("type") or "<unknown>").replace(" ", "_"))
PY
)

echo "Target URL: ${STRIPE_WEBHOOK_URL}"
echo "Event id: ${event_id}"
echo "Event type: ${event_type}"
echo "Replay count: ${REPLAY_COUNT}"

is_success_code() {
  local code="$1"

  if [[ -n "$ACCEPT_HTTP_CODES" ]]; then
    python3 - <<'PY' "$ACCEPT_HTTP_CODES" "$code"
import sys
allowed = {c.strip() for c in sys.argv[1].split(',') if c.strip()}
code = sys.argv[2].strip()
raise SystemExit(0 if code in allowed else 1)
PY
    return
  fi

  [[ "$code" =~ ^2[0-9][0-9]$ ]]
}

ok=0
failed=0

for ((i=1; i<=REPLAY_COUNT; i++)); do
  ts="$(date +%s)"
  signed_payload="${ts}.${payload}"
  signature="$(printf '%s' "$signed_payload" | openssl dgst -sha256 -hmac "$STRIPE_WEBHOOK_SECRET" | sed 's/^.*= //')"
  stripe_sig_header="t=${ts},v1=${signature}"

  start_ns="$(date +%s%N)"
  http_code="$(curl -sS -o /tmp/stripe-webhook-replay-response.$$ \
    -w "%{http_code}" \
    --max-time "$REQUEST_TIMEOUT_SECONDS" \
    -X POST "$STRIPE_WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -H "Stripe-Signature: ${stripe_sig_header}" \
    --data "$payload" || true)"
  end_ns="$(date +%s%N)"
  elapsed_ms=$(( (end_ns - start_ns) / 1000000 ))

  if is_success_code "$http_code"; then
    ok=$((ok + 1))
    echo "attempt ${i}/${REPLAY_COUNT}: HTTP ${http_code} (${elapsed_ms} ms) PASS"
  else
    failed=$((failed + 1))
    echo "attempt ${i}/${REPLAY_COUNT}: HTTP ${http_code} (${elapsed_ms} ms) FAIL"
    if [[ -s /tmp/stripe-webhook-replay-response.$$ ]]; then
      echo "  response body:"
      sed 's/^/    /' /tmp/stripe-webhook-replay-response.$$ | head -n 5
    fi
  fi

  if (( i < REPLAY_COUNT )) && [[ "$REPLAY_DELAY_SECONDS" != "0" && "$REPLAY_DELAY_SECONDS" != "0.0" ]]; then
    sleep "$REPLAY_DELAY_SECONDS"
  fi
done

rm -f /tmp/stripe-webhook-replay-response.$$ || true

echo ""
echo "Summary: ${ok} passed, ${failed} failed"

if [[ "$failed" -gt 0 ]]; then
  echo "Result: FAIL"
  exit 1
fi

echo "Result: PASS"
