# Prove Before Act API Reference

> Prove Before Act is the current product name. `xproof` API/package labels are legacy compatibility identifiers. MX-8004 features are optional and available only when `/api/mx8004/status` reports `active`; production currently reports `not_configured`.

Base URL: `https://provebeforeact.com`

## Authentication

API key via Authorization header: `Authorization: Bearer pm_xxx`

Get your key at https://provebeforeact.com (connect wallet > API Keys section).

Alternative: x402 payment protocol (no API key needed). Send request without auth, receive 402 with payment requirements, sign USDC payment on Base, resend with `X-PAYMENT` header.

## Endpoints

### POST /api/proof

Certify a single file.

**Request:**
```json
{
  "file_hash": "64-char SHA-256 hex string",
  "filename": "document.pdf",
  "author_name": "optional",
  "webhook_url": "https://optional-webhook-url.com"
}
```

**Response (200):**
```json
{
  "proof_id": "uuid",
  "verify_url": "https://provebeforeact.com/proof/uuid",
  "blockchain": {
    "transaction_hash": "hex...",
    "explorer_url": "https://explorer.multiversx.com/transactions/hex..."
  }
}
```

### POST /api/batch

Certify up to 50 files in one call.

**Request:**
```json
{
  "files": [
    {"file_hash": "...", "filename": "file1.pdf"},
    {"file_hash": "...", "filename": "file2.zip"}
  ],
  "author_name": "optional",
  "webhook_url": "https://optional-webhook-url.com"
}
```

### GET /proof/{id}.json

Get proof details in JSON format.

### GET /proof/{id}.md

Get proof details in Markdown format (LLM-friendly).

### GET /badge/{id}

Dynamic SVG badge showing certification status.

### GET /api/acp/products

Discover available services and pricing. No auth required.

### POST /api/acp/checkout

Initiate an ACP checkout session (see ACP section below).

### POST /api/acp/confirm

Confirm an ACP payment and issue the certification (see ACP section below).

## ACP (Agent Commerce Protocol)

AI agents can certify files without an API key by using the ACP payment flow over MultiversX.

### Flow

1. `POST /api/acp/checkout` — create a checkout session and get the EGLD transaction to send
2. Broadcast the transaction on MultiversX
3. `POST /api/acp/confirm` — submit the tx_hash to verify payment and receive the certification

### POST /api/acp/confirm — Retry Contract

When the MultiversX network is slow or temporarily unavailable, the confirm endpoint returns `402` with `retry: true` and guidance on how long to wait:

```json
{
  "error": "PAYMENT_VERIFICATION_FAILED",
  "message": "Could not reach the MultiversX network to verify payment...",
  "retry": true,
  "retry_after_seconds": 15,
  "max_retries": 5
}
```

**Retry guidelines for agent developers:**

- `retry: true` means the payment status is unknown — the transaction may be valid but the network is unreachable. Do **not** treat this as a final failure.
- `retry_after_seconds` (default `15`) — wait at least this many seconds before retrying.
- `max_retries` (default `5`) — after this many consecutive retries without success, stop and alert the user to check the transaction manually on the MultiversX explorer.
- `retry: false` (or field absent) — the payment was verified and rejected for a specific reason (wrong receiver, insufficient value, etc.). Retrying will not help; a new checkout is needed.

**Idempotency:** `POST /api/acp/confirm` is idempotent. If the checkout is already confirmed, re-submitting the same `checkout_id` returns `200` with the existing certification data instead of an error. This allows agents to retry safely after a network timeout without risk of double-billing.

### POST /mcp

MCP server endpoint. JSON-RPC 2.0 over Streamable HTTP.

Available tools: `certify_file`, `verify_proof`, `get_proof`, `discover_services`.

## Pricing

The current flat per-certification price (served live at `/api/pricing`).
