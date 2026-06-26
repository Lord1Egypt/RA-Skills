---
name: stripe-webhook-replay-lab
description: Replay signed Stripe webhook payloads to a local or staging endpoint for idempotency and retry debugging.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","curl","openssl","python3"]}}}
---

# Stripe Webhook Replay Lab

Use this skill to replay the same signed Stripe webhook event multiple times against your endpoint and validate idempotency behavior.

## What this skill does
- Loads a Stripe event payload from a JSON file or inline env var
- Generates valid Stripe `Stripe-Signature` headers using your webhook secret (`whsec_...`)
- Replays the exact same payload N times to simulate duplicate deliveries/retries
- Prints per-attempt HTTP status and latency with a pass/fail summary

## Inputs
Required:
- `STRIPE_WEBHOOK_URL` (target endpoint)
- `STRIPE_WEBHOOK_SECRET` (Stripe endpoint secret used to verify signatures)

Payload source (choose one):
- `STRIPE_EVENT_PATH` (default: `fixtures/sample-checkout-session-completed.json`)
- `STRIPE_EVENT_JSON` (inline JSON payload; overrides `STRIPE_EVENT_PATH`)

Optional:
- `REPLAY_COUNT` (default: `2`)
- `REPLAY_DELAY_SECONDS` (default: `0`)
- `REQUEST_TIMEOUT_SECONDS` (default: `15`)
- `ACCEPT_HTTP_CODES` (comma-separated exact HTTP codes accepted as success; default empty = any 2xx)

## Run

```bash
STRIPE_WEBHOOK_URL=http://localhost:8000/webhooks/stripe \
STRIPE_WEBHOOK_SECRET=whsec_test_123 \
bash scripts/replay-stripe-webhook.sh
```

Force five duplicate deliveries with a small delay:

```bash
STRIPE_WEBHOOK_URL=http://localhost:8000/webhooks/stripe \
STRIPE_WEBHOOK_SECRET=whsec_test_123 \
REPLAY_COUNT=5 \
REPLAY_DELAY_SECONDS=0.2 \
bash scripts/replay-stripe-webhook.sh
```

Use inline payload JSON:

```bash
STRIPE_WEBHOOK_URL=http://localhost:8000/webhooks/stripe \
STRIPE_WEBHOOK_SECRET=whsec_test_123 \
STRIPE_EVENT_JSON='{"id":"evt_test","type":"checkout.session.completed","object":"event","data":{"object":{"id":"cs_test"}}}' \
bash scripts/replay-stripe-webhook.sh
```

## Output contract
- Prints payload event id/type when available
- Logs each replay attempt: status code + elapsed milliseconds
- Exit `0` if all attempts pass success criteria
- Exit `1` if any attempt fails or inputs are invalid
