# API Reference

Base URL: `https://mpp-createos.nodeops.network`

## Auth Headers (all `/agent/*` endpoints)

| Header             | Value                                       |
| ------------------ | ------------------------------------------- |
| `X-Wallet-Address` | `0x...` wallet address                      |
| `X-Signature`      | Signature of `{wallet}:{timestamp}:{nonce}` |
| `X-Timestamp`      | Unix ms (within 60s of server)              |
| `X-Nonce`          | UUID, unique per request                    |

---

## `GET /health`

Response: `{ "status": "ok" }`

---

## `POST /agent/deploy`

Gateway dynamically prices deployments by querying CreateOS, then checks credits and active projects to decide whether to deploy free or require payment. Minimum charge is $0.50.

### Without `X-Payment-Tx` — credit + active project check

The gateway returns one of:

**Case A: Has credits, no active projects** → 200, deploys for free
**Case B: Has credits, active projects, opted in (`X-Use-Existing-Credits: true`)** → 200, deploys with warning
**Case C: Has credits, active projects, NOT opted in** → 402 with warning
**Case D: Not enough credits** → 402 standard

402 (no credits):
```json
{
  "error": "Payment required",
  "amount_usd": 0.5,
  "amount_token": "500000",
  "current_credit_balance_usd": 0,
  "active_projects": 0,
  "pay_to": "0x7EA5...",
  "payment_chain": "arbitrum",
  "token": "usdc",
  "decimals": 6,
  "supported_chains": [...]
}
```

402 (has credits + active projects):
```json
{
  "error": "Payment required",
  "warning": "You have 2 active project(s) sharing credits. Paying extends total runtime. To deploy using existing credits (will reduce other projects' runtime), retry with header X-Use-Existing-Credits: true",
  "amount_usd": 0.5,
  "current_credit_balance_usd": 1.20,
  "active_projects": 2,
  "pay_to": "0x7EA5...",
  ...
}
```

### With `X-Payment-Tx` — deploys

Additional headers:

| Header            | Required | Default  | Description            |
| ----------------- | -------- | -------- | ---------------------- |
| `X-Payment-Tx`    | yes      | —        | ERC20 transfer tx hash |
| `X-Payment-Chain` | no       | from 402 | Chain name             |
| `X-Payment-Token` | no       | `usdc`   | Token symbol           |
| `X-Use-Existing-Credits` | no | `false` | Opt in to share credits with active projects (no payment) |

Body:

```json
{
  "uniqueName": "my-app",
  "displayName": "My App",
  "upload": {
    "type": "files",
    "files": [{ "path": "index.js", "content": "base64" }]
  }
}
```

Or zip: `"upload": { "type": "zip", "data": "base64", "filename": "code.zip" }`

Optional: `months` (default 1), `description`, `settings`.

Response `200`:

```json
{ "projectId": "uuid", "deploymentId": "uuid", "status": "deploying" }
```

## Pricing

- Pricing is dynamic — fetched from CreateOS pricing API and converted to USD ($1 = 100 credits)
- Cached server-side for 5 minutes
- Minimum deploy price: **$0.50**
- Multiplied by `months` (default 1)

## Credit Sharing

CreateOS credits are pooled across active projects and consumed hourly. Deploying without paying when you have active projects will reduce their runtime — the gateway warns you in 402 responses and requires explicit opt-in.

---

## `GET /agent/deploy/:projectId/:deploymentId/status`

Only the deployer wallet can access.

```json
{ "status": "deploying", "deployment_status": "building" }
{ "status": "ready", "endpoint": "https://app.nodeops.network" }
{ "status": "failed", "reason": "build error" }
```

---

## `GET /agent/projects`

List all projects deployed by the authenticated wallet, with the live URL of the latest deployment. Requires auth headers.

Response:

```json
{
  "wallet": "0x5B6C...",
  "count": 2,
  "projects": [
    {
      "id": "uuid",
      "name": "demo-1234567890",
      "displayName": "Demo App",
      "status": "active",
      "url": "https://demo-1234567890.nodeops.network",
      "createdAt": "2026-04-07T10:00:00.000Z"
    }
  ]
}
```

`url` is `null` if the project has no deployment yet (e.g. building, failed, or no deployments). Project status values: `active`, `building`, `deploying`, `pending`, `queued`, `promoting`, `deleting`, `failed`.

---

## `GET /agent/balance/:address`

Returns all token balances for an address on a chain. No auth required.

Query params:

- `chain` — chain name (default: `arbitrum`)

Response:

```json
{
  "address": "0x5B6C...",
  "chain": "arbitrum",
  "chain_id": 42161,
  "balances": [
    {
      "token": "usdc",
      "symbol": "USDC",
      "address": "0xaf88d065...",
      "balance": "18.000000",
      "balance_raw": "18000000",
      "decimals": 6
    }
  ]
}
```

---

## `GET /agent/chains`

Returns all supported chains and accepted tokens. No auth required.

```json
{
  "chains": [
    { "chain": "arbitrum", "chain_id": 42161, "tokens": ["usdc", "usdt"] },
    { "chain": "base", "chain_id": 8453, "tokens": ["usdc", "usdt"] }
  ]
}
```

---

## Supported Chains & Tokens

| Chain      | ID    | Tokens     |
| ---------- | ----- | ---------- |
| `arbitrum` | 42161 | USDC, USDT |
| `base`     | 8453  | USDC, USDT |

---

## Error Codes

| Code | Meaning                              |
| ---- | ------------------------------------ |
| 400  | Invalid body                         |
| 401  | Bad signature, expired, nonce reused |
| 402  | No payment or verification failed    |
| 403  | Wrong wallet on status               |
| 409  | Tx hash already used                 |
| 429  | Rate limited (30/min)                |
