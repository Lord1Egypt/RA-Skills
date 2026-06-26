---
name: x402-x-tweet-fetcher
description: Buy Xcatcher points via x402 on Solana USDC, obtain an API key, create X crawl tasks, poll status, and download XLSX results.
homepage: https://xcatcher.top/docs/
user-invocable: true
metadata: {"openclaw":{"emoji":"🐦","homepage":"https://xcatcher.top/docs/","requires":{"bins":["curl","jq","base64"]}}}
---

# Xcatcher (x402 + X Tasks)

Use this skill to:
- buy Xcatcher points via x402 on Solana (USDC),
- obtain an API key,
- create X crawl tasks,
- poll task status,
- download XLSX results.

Base URL: `https://xcatcher.top`  
REST base: `https://xcatcher.top/api/v1`  
Optional health: `https://xcatcher.top/mcp/health`

## What this skill does

This skill provides an end-to-end flow for paid X data collection:

1. request an x402 quote for points,
2. pay the quote in Solana USDC,
3. exchange the paid quote for an API key,
4. use the API key to create crawl tasks,
5. poll task status until the result is ready,
6. download the XLSX result file.

## Requirements

Local tools:
- `curl`
- `jq`
- `base64`

Optional:
- `python3` for simple JSON math examples

Authentication:
- You do **not** need `XCATCHER_API_KEY` before starting.
- You will obtain `XCATCHER_API_KEY` after a successful `buy_points` call.
- For later authenticated calls, set:
  - `export XCATCHER_API_KEY="your_api_key"`

## Pricing model

Task cost:
- `mode=normal`: 1 point per user
- `mode=deep`: 10 points per user

Estimated cost:
- `estimated_cost = users_count × (mode == normal ? 1 : 10)`

Supported payment chains:
- `solana`
- quote payload may also mention other supported networks if enabled by server configuration

> Never hardcode any USDC-to-points conversion rate. Always trust the live quote response.

---

## 0) Optional health check

```bash
BASE="https://xcatcher.top"
curl -sS "$BASE/mcp/health"
echo
```

---

## 1) Get an x402 quote

Notes:
- quotes expire quickly,
- pay immediately after quote creation,
- save `quote_id`.

```bash
BASE="https://xcatcher.top"
POINTS=1

curl -sS "$BASE/api/v1/x402/quote?points=$POINTS" | tee quote.json
echo

QUOTE_ID=$(jq -r '.quote_id' quote.json)
USDC_MINT=$(jq -r '.accepts.solana.asset' quote.json)
PAY_TO=$(jq -r '.accepts.solana.payTo' quote.json)
AMOUNT_ATOMIC=$(jq -r '.accepts.solana.maxAmountRequired' quote.json)

echo "QUOTE_ID=$QUOTE_ID"
echo "USDC_MINT=$USDC_MINT"
echo "PAY_TO=$PAY_TO"
echo "AMOUNT_ATOMIC=$AMOUNT_ATOMIC"
echo "USDC_AMOUNT=$(python3 - <<'PY'
import json
q=json.load(open('quote.json'))
amt=int(q['accepts']['solana']['maxAmountRequired'])
print(amt/1_000_000)
PY
)"
echo
```

Important:
- keep `QUOTE_ID`,
- use it in the next purchase step,
- if the quote expires, create a new one.

---

## 2) Pay USDC on Solana mainnet

Send USDC (SPL) to `PAY_TO` for at least `AMOUNT_ATOMIC`.

Then record the Solana transaction signature:

```bash
SOL_SIG="YOUR_SOLANA_TX_SIGNATURE"
```

---

## 3) Build the `PAYMENT-SIGNATURE` header

Rules:
- base64 encode once,
- do not double encode,
- do not wrap the header value in extra quotes.

```bash
PAYMENT_SIGNATURE_B64=$(jq -nc --arg sig "$SOL_SIG" \
  '{"x402Version":1,"scheme":"exact","network":"solana:mainnet","payload":{"signature":$sig}}' \
  | base64 | tr -d '\n')

echo "PAYMENT_SIGNATURE_B64=$PAYMENT_SIGNATURE_B64"
echo
```

---

## 4) Buy points and obtain an API key

```bash
BASE="https://xcatcher.top"

curl -sS -X POST "$BASE/api/v1/x402/buy_points" \
  -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: $PAYMENT_SIGNATURE_B64" \
  -d "$(jq -nc --arg q "$QUOTE_ID" '{quote_id:$q}')" \
  | tee buy.json
echo

API_KEY=$(jq -r '.api_key' buy.json)
echo "API_KEY=$API_KEY"

export XCATCHER_API_KEY="$API_KEY"
echo "XCATCHER_API_KEY exported."
echo
```

---

## 5) Verify balance

```bash
BASE="https://xcatcher.top"

curl -sS "$BASE/api/v1/me" \
  -H "Authorization: Bearer $XCATCHER_API_KEY" \
  | jq .
echo
```

If you get `402`:
- quote may have expired,
- payment proof may be invalid,
- redo steps 1 to 4 with a new quote and a new payment proof.

---

## 6) Create a crawl task

Rules:
- `users` are X usernames without `@`,
- always provide `idempotency_key`,
- if retrying the same logical request, reuse the same `idempotency_key`.

```bash
BASE="https://xcatcher.top"
MODE="normal"
IDEM="test-idem-001"
USERS_JSON='["user1","user2"]'

export MODE USERS_JSON

echo "ESTIMATED_COST_POINTS=$(python3 - <<'PY'
import json, os
users=json.loads(os.environ.get('USERS_JSON', '[]'))
mode=os.environ.get('MODE', 'normal')
per=1 if mode == 'normal' else 10
print(len(users) * per)
PY
)"
echo

curl -sS -X POST "$BASE/api/v1/tasks" \
  -H "Authorization: Bearer $XCATCHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -nc --arg mode "$MODE" --arg idem "$IDEM" --argjson users "$USERS_JSON" \
        '{mode:$mode, users:$users, idempotency_key:$idem}')" \
  | tee task.json | jq .
echo

TASK_ID=$(jq -r '.task_id' task.json)
echo "TASK_ID=$TASK_ID"
echo
```

---

## 7) Poll task status until ready

Stop when `download_url` or `result_path` appears.

```bash
BASE="https://xcatcher.top"

while true; do
  J=$(curl -sS "$BASE/api/v1/tasks/$TASK_ID" \
      -H "Authorization: Bearer $XCATCHER_API_KEY")

  echo "$J" | jq '{task_id,status,status_code,updated_time,error_message,result_path,download_url}'

  HAS=$(echo "$J" | jq -r '(.download_url // .result_path // "") | length')
  if [ "$HAS" -gt 0 ]; then
    echo "DONE"
    break
  fi

  sleep 5
done
echo
```

---

## 8) Download the XLSX result

```bash
BASE="https://xcatcher.top"

curl -sS -L -o "task_${TASK_ID}.xlsx" \
  -H "Authorization: Bearer $XCATCHER_API_KEY" \
  "$BASE/api/v1/tasks/$TASK_ID/download"

echo "Saved: task_${TASK_ID}.xlsx"
echo
```

---

## Failure handling

- `401`: Bearer token missing or invalid  
  → obtain API key again or set `XCATCHER_API_KEY` correctly

- `402`: quote invalid, payment proof invalid, or quote expired  
  → redo quote + pay + buy_points with a fresh quote

- `429`: rate limited  
  → back off and respect `Retry-After` if present

- task delayed or upstream unavailable  
  → keep polling with a longer interval and surface the error clearly

## Notes for agents

- Prefer live quote responses over any cached assumptions.
- Prefer explicit `idempotency_key` values for retries.
- Treat task results as private and always download with the same Bearer token.
- Do not assume result files are public URLs.
