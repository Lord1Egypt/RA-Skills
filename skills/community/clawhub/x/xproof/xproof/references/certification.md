# Certification API

REST endpoints for registering an agent, creating blockchain certifications on MultiversX, and reading status.

## Bootstrap

### `POST /api/agent/register` -- Free Trial Registration (No Auth)

Get a `pm_` API key instantly with 10 free certifications. No wallet, no credit card, no signup form.

**Authentication:** None.

**Request:**

```json
{
  "agent_name": "my-agent",
  "webhook_url": "https://your-agent.com/hooks/xproof"
}
```

| Field | Type | Required | Description |
|:---|:---|:---|:---|
| `agent_name` | string | Yes | 2-128 chars. Used to deduplicate trial registrations per identity. |
| `webhook_url` | string | No | HTTPS callback for on-chain confirmation events. |

**Response (201 Created):**

```json
{
  "api_key": "pm_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "agent_name": "my-agent",
  "trial": {
    "quota": 10,
    "used": 0,
    "remaining": 10
  },
  "endpoints": {
    "certify": "POST https://xproof.app/api/proof",
    "batch": "POST https://xproof.app/api/batch",
    "audit": "POST https://xproof.app/api/audit",
    "status": "GET https://xproof.app/api/agent/status",
    "verify": "GET https://xproof.app/api/proof/{proof_id}"
  },
  "quick_start": {
    "steps": [
      {"step": 1, "title": "Register", "done": true},
      {"step": 2, "title": "Certify your first file"},
      {"step": 3, "title": "Verify the proof publicly"},
      {"step": 4, "title": "Check remaining credits"}
    ]
  },
  "message": "Trial registered. 10 free proofs available. Treat your api_key as a password."
}
```

**Errors:**

| Code | Meaning |
|:---|:---|
| `400` | Missing or invalid `agent_name` |
| `409` | Agent name already has an active trial (returns existing `agent_id`, no new key) |
| `429` | Rate limited (max 5 registrations per IP per hour) |

---

### `GET /api/agent/status` -- Agent Status & Credits

Get the agent's current trial credits, last certified proof, and usage statistics.

**Authentication:** API Key (`Authorization: Bearer pm_...`).

**Response (200 OK):**

```json
{
  "agent_id": "uuid",
  "agent_name": "my-agent",
  "is_trial": true,
  "credits_remaining": 8,
  "credits": {
    "trial_quota": 10,
    "trial_used": 2,
    "total_remaining": 8
  },
  "last_proof": {
    "id": "proof-uuid",
    "filename": "report.pdf",
    "verify_url": "https://xproof.app/proof/proof-uuid",
    "transaction_hash": "abc123...",
    "created_at": "2026-05-02T11:00:00.000Z"
  },
  "proofs": {
    "total": 2,
    "last_proof": { "...": "same as top-level last_proof" }
  }
}
```

**Errors:**

| Code | Meaning |
|:---|:---|
| `401` | Missing or invalid API key |

---

## Certification

### `POST /api/proof` -- Certify a Single File

Creates an immutable certification on MultiversX mainnet.

**Authentication:** API Key (`Authorization: Bearer pm_...`) or x402 payment.

**Request:**

```json
{
  "file_hash": "a1b2c3d4e5f6789012345678901234567890123456789012345678901234abcd",
  "filename": "report.pdf",
  "author_name": "MyAgent",
  "webhook_url": "https://your-agent.com/hooks/xproof"
}
```

| Field | Type | Required | Description |
|:---|:---|:---|:---|
| `file_hash` | string | Yes | SHA-256 hash (64 hex characters) |
| `filename` | string | Yes | Original filename with extension |
| `author_name` | string | No | Default: "AI Agent" |
| `webhook_url` | string | No | HTTPS URL for on-chain confirmation callback |

**Response (201 Created):**

```json
{
  "proof_id": "uuid-v4",
  "status": "certified",
  "file_hash": "a1b2c3...",
  "filename": "report.pdf",
  "verify_url": "https://xproof.app/proof/uuid-v4",
  "certificate_url": "https://xproof.app/api/certificates/uuid-v4.pdf",
  "blockchain": {
    "network": "MultiversX",
    "transaction_hash": "abc123...",
    "explorer_url": "https://explorer.multiversx.com/transactions/abc123..."
  },
  "credits_remaining": 9,
  "timestamp": "2026-05-02T12:00:00.000Z"
}
```

---

### `POST /api/batch` -- Batch Certification (Up to 50 Files)

```json
{
  "files": [
    {"file_hash": "abc...", "filename": "model.bin"},
    {"file_hash": "def...", "filename": "training.csv"}
  ],
  "author_name": "MyAgent"
}
```

**Response (207 Multi-Status):** Per-file results with `proof_id` and `status` for each.

---

### `POST /api/audit` -- Audit Log Anchoring

See [SKILL.md Section 8](../SKILL.md#8-agent-audit-log-standard) for the full canonical schema and enforcement pattern.

---

## Verification (Public, No Auth)

### `GET /api/proof/:id` -- Lookup by Proof UUID

Returns the structured proof document. Public if the certification was created with `is_public=true` (default for trial users) or by the proof owner.

```bash
curl https://xproof.app/api/proof/<proof_id>
```

### `GET /api/proof/hash/:hash` -- Lookup by File Hash

```bash
curl https://xproof.app/api/proof/hash/<sha256_hex>
```

### `GET /proof/:id` -- Human-readable proof page

Returns a styled HTML page with QR code, blockchain explorer link, and download buttons.

### `GET /proof/:id.json` -- Same data as JSON

### `GET /api/certificates/:id.pdf` -- Downloadable PDF Certificate

Returns a downloadable PDF certificate with QR code. Public.

### `GET /badge/:id` -- Dynamic SVG Badge

Returns a shields.io-style SVG badge showing certification status:
- **Verified** (green) -- hash found on-chain
- **Pending** (yellow) -- awaiting confirmation
- **Not Found** (red) -- no matching hash

Embed in Markdown:

```markdown
![xProof Certified](https://xproof.app/badge/<proof_id>)
```

---

## Webhook Payload

When a certification is confirmed on-chain, xProof sends a POST to the `webhook_url`:

```json
{
  "event": "proof.confirmed",
  "proof_id": "uuid-v4",
  "file_hash": "a1b2c3...",
  "filename": "report.pdf",
  "blockchain": {
    "network": "MultiversX",
    "transaction_hash": "abc123...",
    "explorer_url": "https://explorer.multiversx.com/transactions/abc123..."
  },
  "timestamp": "2026-05-02T12:00:00.000Z"
}
```

**Security:** HMAC-SHA256 signature in `X-Webhook-Signature` header.
**Retry:** 3 attempts with exponential backoff.

## Error Codes

| Code | Meaning |
|:---|:---|
| `400` | Invalid request (missing/malformed `file_hash` or `filename`) |
| `401` | Missing or invalid API key |
| `402` | Payment required (x402 mode) |
| `403` | Trial quota exhausted -- top up via wallet or use x402 |
| `409` | File already certified (returns existing certification) |
| `429` | Rate limit exceeded |
| `500` | Internal server error |
