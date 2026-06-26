# Webhooks and Payment Genuineness Verification

Use this reference when the user asks to configure seller webhooks, inspect events, debug delivery failures, or verify payment authenticity.

## Setup

Configure a webhook for an endpoint:

```bash
python {baseDir}/scripts/manage_webhook.py set <slug> <https_webhook_url>
```

Inspect/remove:

```bash
python {baseDir}/scripts/manage_webhook.py info <slug>
python {baseDir}/scripts/manage_webhook.py remove <slug>
```

Important: when a webhook is set or rotated, save the returned `signing_secret` immediately.

## Seller Webhook Headers

x402 Studio seller webhooks are HMAC-signed. Expect these headers on current deliveries:

- `X-X402-Signature`
- `X-X402-Timestamp`
- `X-X402-Event`
- `X-X402-Event-Id`

Event types currently include:

- `payment.succeeded`
- `credits.depleted`
- `credits.low`
- `credits.recharged`

## Signature Verification Model

Verification model:

- payload to sign: `<timestamp>.<raw_request_body>`
- algorithm: `HMAC-SHA256`
- secret: the webhook `signing_secret`

Python snippet:

```python
import hashlib
import hmac

def verify(secret: str, timestamp: str, raw_body: bytes, received_sig: str) -> bool:
    payload = timestamp.encode() + b"." + raw_body
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, received_sig)
```

Do not parse and re-serialize JSON before hashing. Use the raw request body bytes.

## Backward Compatibility Warning

Some older receivers may still accept legacy raw-secret headers such as:

- `x-x402layer-secret`
- `x-x402-secret`
- `Authorization: Bearer <secret>`

That legacy model is not enough for current Studio seller webhook deliveries. Use signed webhook verification first and keep raw-secret-header fallback only if older clients still depend on it.

## Two Secret Hops

Do not confuse these two different secrets:

### 1) Studio → seller webhook receiver

- sender: x402 Studio
- secret: webhook `signing_secret`
- auth model: HMAC verification using the signed headers above

### 2) Seller webhook receiver → app settlement route

- sender: your own receiver / worker
- secret: your app-internal shared secret
- repo-specific example: worker sends `x-x402-secret`, app verifies with `X402_WEBHOOK_SECRET`

The Studio webhook signing secret is not the same thing as the app settlement secret.

## Secret Rotation Runbook

If webhook deliveries suddenly return `401` after previously working:

1. verify whether the Studio webhook `signing_secret` was rotated or drifted
2. rotate the webhook secret in Studio if needed
3. copy the newly returned `signing_secret` immediately
4. update the receiving worker/server to the exact new value
5. test again with one small payment

## Log Expectations

For debugging, it is safe and useful to log the presence or parsed values of:

- `x-x402-signature`
- `x-x402-timestamp`
- `x-x402-event`
- `x-x402-event-id`

Do not:

- log the signing secret itself
- log full signed payloads if they contain sensitive metadata unless that is absolutely necessary for a short-lived debug session

## Common Failure Mode

If Studio shows webhook delivery `401`, and a direct manual POST with the stored secret succeeds against the receiver, the receiver likely supports only legacy raw-secret auth while Studio is sending signed webhooks.

That mismatch is the first thing to check before blaming network or payload shape issues.

## Receipt Verification (PyJWT/JWKS)

For stronger authenticity checks, verify the receipt JWT (RS256/JWKS):

```bash
python {baseDir}/scripts/verify_webhook_payment.py \
  --body-file ./webhook.json \
  --signature 't=1700000000,v1=<hex>' \
  --secret '<YOUR_SIGNING_SECRET>' \
  --required-source-slug my-api \
  --require-receipt
```

Dependencies (already in `requirements.txt`):

```bash
pip install pyjwt[crypto] cryptography
```

## Webhook Payload Schema

A `payment.succeeded` webhook body looks like:

```json
{
  "id": "event-uuid",
  "type": "payment.succeeded",
  "created_at": "2026-05-20T12:00:00.000Z",
  "data": {
    "source": "endpoint",
    "source_id": "endpoint-uuid",
    "source_slug": "my-api",
    "amount": 0.01,
    "currency": "USDC",
    "tx_hash": "0xabc...",
    "payer_wallet": "0x123...",
    "network": "base",
    "status": "confirmed",
    "client_reference_id": "order-456",
    "metadata": {
      "factory_payment_id": "f1ee6b40-...",
      "plan": "pro"
    },
    "receipt_token": "eyJ...",
    "jwks_url": "https://api.x402layer.cc/.well-known/jwks.json"
  }
}
```

Fields:

| Field | Type | Description |
|---|---|---|
| `source` | `"endpoint"` or `"product"` | What was paid for |
| `source_id` | uuid | Endpoint or product ID |
| `source_slug` | string | URL slug |
| `amount` | number | Amount paid in `currency` |
| `currency` | string | Always `"USDC"` today |
| `tx_hash` | string | On-chain transaction hash |
| `payer_wallet` | string | Buyer wallet address |
| `network` | string | Chain used (`base`, `solana`, etc.) |
| `status` | string | Always `"confirmed"` on success |
| `client_reference_id` | string or null | From `?client_reference_id=` query param |
| `metadata` | object | All custom query params from the payment URL (see below) |
| `receipt_token` | string or null | Signed JWT for receipt verification |
| `jwks_url` | string or null | JWKS endpoint for verifying receipt |

## Payment Metadata Passthrough

Any query parameter on a payment URL that is not a Singularity-internal parameter is automatically captured in the webhook `metadata` field. This works like Stripe metadata passthrough.

### Supported patterns

| URL pattern | Result in webhook `metadata` |
|---|---|
| `?factory_payment_id=abc` | `{"factory_payment_id": "abc"}` |
| `?order_id=123&user_email=a@b.com` | `{"order_id": "123", "user_email": "a@b.com"}` |
| `?client_reference_id=ref-99` | Populates `client_reference_id` field (top-level, not in metadata) |
| `?metadata={"key":"val"}` | Parsed JSON merged into metadata |
| `?metadata.plan=pro` | `{"plan": "pro"}` |
| `?meta_source=ios` | `{"source": "ios"}` |

### Reserved parameters (not forwarded)

These are consumed by the payment engine and excluded from metadata:
`client_reference_id`, `clientReferenceId`, `purchaseId`, `purchase_id`, `reference`, `metadata`, `credits`, `wallet`, `action`, `useCredits`, `amount`, `subscription_coupon_token`, `subscription_holder_token`

### Limits

- Max 24 metadata entries
- Max 64 characters per key
- Values must be scalar (string, number, boolean, null)
- Total metadata JSON must be under 2048 bytes
- Keys `__proto__`, `constructor`, `prototype` are blocked

### Example: correlating a webhook to an internal record

Build the payment URL with your internal ID:

```
https://api.x402layer.cc/e/my-api?order_id=abc-123
```

When payment succeeds, the webhook arrives with:

```json
{
  "data": {
    "metadata": { "order_id": "abc-123" },
    ...
  }
}
```

Your server matches `metadata.order_id` to your internal record.

## Cross-check Rules

When a receipt is present, compare:

- payload `data.tx_hash` == receipt `tx_hash`
- payload `data.source_slug` == receipt `source_slug`
- payload `data.amount` == receipt `amount`

Reject the request when:

- signature verification fails
- receipt is invalid or missing when required
- event fields and receipt fields do not match

## Minimal Test Flow

When integrating seller webhooks:

1. confirm whether the sender is Studio-signed or legacy raw-secret only
2. implement HMAC verification if Studio is the sender
3. keep legacy raw-secret fallback only if an older client still needs it
4. verify the exact secret source:
   - Studio webhook `signing_secret`
   - app settlement secret
5. test with:
   - one direct manual POST
   - one real Studio payment delivery
6. confirm the purchase row transitions from `pending` to `settled`
