# Bridge HTTP Contract

Instance A POSTs extracted JSON to `bridge-service` on Instance B's machine. The bridge verifies auth, deduplicates, and invokes OpenClaw with `tally-skill`.

Base URL: `$BRIDGE_URL` (no trailing slash), e.g. `https://client-abc.ngrok.app`.

## Authentication

Every mutating request requires:

| Header | Value |
|---|---|
| `Authorization` | `Bearer $BRIDGE_BEARER` |
| `X-Signature` | `hmac-sha256=<hex>` |
| `Content-Type` | `application/json` |

`Idempotency-Key` header is required on `POST /v1/post-voucher` and must equal the body's `idempotency_key`.

### HMAC computation

Sign the **raw request body** (UTF-8, exact bytes sent):

```bash
# Linux / macOS
BODY='{"schema_version":"1.0",...}'
SIG=$(printf '%s' "$BODY" | openssl dgst -sha256 -hmac "$BRIDGE_HMAC_SECRET" -binary | xxd -p -c 256)
# Header: X-Signature: hmac-sha256=$SIG
```

```javascript
// Node.js
const crypto = require('node:crypto');
const sig = crypto.createHmac('sha256', process.env.BRIDGE_HMAC_SECRET)
  .update(bodyString, 'utf8')
  .digest('hex');
// Header: X-Signature: hmac-sha256=${sig}
```

Bridge rejects requests when signature missing, wrong, or body altered.

## Endpoints

### GET /v1/health

No body. Bearer required.

**Response 200**

```json
{
  "tally": "ok",
  "company_default": "ABC Company",
  "version": "1.0.0"
}
```

`tally: "down"` when `$TALLY_URL` is unreachable. Instance A must not call `/v1/post-voucher` until `tally` is `ok`.

### POST /v1/post-voucher

Posts one voucher to Tally via Instance B OpenClaw.

**Headers:** Bearer, `X-Signature`, `Idempotency-Key`, `Content-Type: application/json`

**Body:** Canonical JSON per `extraction-schema.md`.

**Response 200 — posted**

```json
{
  "status": "posted",
  "guid": "abc-purchase-ril2026-00123-20260115",
  "voucher_number": "00123",
  "company": "ABC Company",
  "summary": "Purchase voucher posted: Reliance Industries Ltd, ₹71,095.00",
  "masters_created": ["Reliance Industries Ltd"]
}
```

**Response 200 — duplicate (idempotent replay)**

Same body as original success; `status` may be `posted` with `"duplicate": true`.

**Response 422 — needs clarification**

```json
{
  "status": "needs_clarification",
  "missing_fields": ["voucher.voucher_class"],
  "message": "Please confirm the voucher class name (e.g., 'Purchase @ 18 %')."
}
```

Instance A forwards `message` to the user on Telegram.

**Response 4xx/5xx — error**

```json
{
  "status": "error",
  "error_code": "TALLY_UNREACHABLE",
  "message": "Could not connect to Tally at http://localhost:9000"
}
```

### POST /v1/generate-pdf

Optional. Forwards to Instance B to run `tallyca` (invoice/receipt PDF generation). Same auth headers as post-voucher.

**Body**

```json
{
  "mode": "from-text|invoice|generic",
  "company": "ABC Company",
  "text": "Party Name: ...",
  "output_filename": "invoice_186.pdf"
}
```

**Response 200**

```json
{
  "status": "ok",
  "file_path": "/tmp/invoice_186.pdf"
}
```

### GET /v1/report

Query params: `name`, `from` (`YYYY-MM-DD`), `to` (`YYYY-MM-DD`), optional `company`.

Proxies Tally report export via Instance B. Bearer required; HMAC not required on GET.

## Error codes

| Code | HTTP | Meaning |
|---|---|---|
| `UNAUTHORIZED` | 401 | Missing/invalid bearer |
| `INVALID_SIGNATURE` | 401 | HMAC mismatch |
| `INVALID_BODY` | 400 | JSON parse or schema failure |
| `MISSING_IDEMPOTENCY_KEY` | 400 | Header absent |
| `TALLY_UNREACHABLE` | 502 | Tally not running |
| `OPENCLAW_ERROR` | 502 | OpenClaw CLI/HTTP failed |
| `NEEDS_CLARIFICATION` | 422 | Missing/low-confidence fields |
| `INTERNAL_ERROR` | 500 | Unexpected bridge failure |

## Retry policy (Instance A)

| Condition | Action |
|---|---|
| Network timeout, connection reset | Retry up to 3 times |
| HTTP 5xx | Retry with exponential backoff: 2s, 4s, 8s |
| HTTP 422 `needs_clarification` | Do not retry — ask user |
| HTTP 401 | Do not retry — fix credentials |
| HTTP 200 `posted` | Do not retry |

Use the **same** `Idempotency-Key` on retries so duplicate posts are safe.

## Sample curl (post-voucher)

```bash
BODY=$(cat payload.json)
SIG=$(printf '%s' "$BODY" | openssl dgst -sha256 -hmac "$BRIDGE_HMAC_SECRET" -binary | xxd -p -c 256)

curl -s -X POST "$BRIDGE_URL/v1/post-voucher" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BRIDGE_BEARER" \
  -H "X-Signature: hmac-sha256=$SIG" \
  -H "Idempotency-Key: abc-sales-186-20260518" \
  -d "$BODY"
```

## Sample curl (health)

```bash
curl -s -H "Authorization: Bearer $BRIDGE_BEARER" "$BRIDGE_URL/v1/health"
```
