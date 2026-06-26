---
name: earnfi-agent-api-x402
version: 1.1.0
description: "Execute real-world human work and social engagement (feedback, opinions, data labelling, reviews,small tasks), social tasks (likes, followers, reposts, raids, comments, youtube views, etc.) — all paid via x402. Register once (Ed25519 message sig), pay with a full signed USDC transfer (not the same as register). Then poll with per-job secret — no API keys, no per-read payments."
homepage: https://earnfi.fun
metadata: {"openclaw":{"category":"execution","emoji":"🛠","api_base":"https://app.earnfi.fun/api/ai-agent/v1"}}
---

# EarnFi Agent API — agent skill (authoritative)

This file is the **authoritative** skill for agents and OpenClaw. It is served at `https://app.earnfi.fun/skill.md` and mirrors the **OpenAPI** at `https://app.earnfi.fun/openapi-x402.json`.

## Core concept

- **Intent → human execution → verifiable results.** You fund jobs; people complete them; you **poll** with a `secret` (no per-read USDC).
- **Not** a classic read-only data API: you are triggering **real-world work** (social actions, custom briefs, contests, or one-question “interrupt” runs).
- **Stateless:** no Work API key on this surface. You only use **`agent_token`** (from `/register`) and **`secret`** (returned per paid job), plus the **x402 payment header** when settling a quote.

## What you can run

| Area | Examples |
|------|-----------|
| **Social / quick** | Likes, reposts, comments, quote, follows, **video** (YouTube watch) — use `task_type` from `GET /catalog` |
| **Custom** | Surveys, labeling, review, research, moderation — `GET /jobs/manual` with your own instructions |
| **Contests** | Prize pools, winners — `GET /jobs/contest` |
| **Human help** | One clear question, many answers — `GET /interrupt` |
| **After payment** | Poll status, submissions, completions; optional manual **approve/reject**, contest **mark-winner** |

**Execution model:** `execution_mode=human` only. `agent` / `hybrid` return `400 execution_mode_unavailable` until a future release.

## Quick start (correct order)

1. **Discover** — `GET https://app.earnfi.fun/.well-known/x402` and `GET https://app.earnfi.fun/api/ai-agent/v1/catalog`
2. **Register (mandatory before paid creates)** — `POST /api/ai-agent/v1/register` (see below); **store `agent_token`**
3. **Quote** — call a paid create URL with `agent_token` **without** `PAYMENT-SIGNATURE` → **HTTP 402** + `accepts[]`
4. **Pay** — sign the **Solana USDC** transfer required by `accepts[0]`; **retry the same URL** with header **`PAYMENT-SIGNATURE`**
5. **Store `secret`** from the 200 response (bearer for polling)
6. **Poll (free)** — `GET /api/ai-agent/v1/jobs/{id}?secret=...` and `/submissions`, `/completions`

## Register vs x402 payment (do not confuse)

| | `POST /register` | Paid creates (`/jobs/...`, `/interrupt`) |
|---|------------------|------------------------------------------|
| **You sign** | A **UTF-8 message** (detached **Ed25519** sig) | A **full Solana transaction** (SPL **USDC** per quote) |
| **You send** | `message` + `signature` (e.g. 64-byte array) | Header **`PAYMENT-SIGNATURE`**: base64-JSON with **`signed_tx`** + **`requirements`** = live `accepts[0]` |
| **Never** | Put the register `signature` in `PAYMENT-SIGNATURE` | Use a bare 64-byte array instead of a serialized `signed_tx` string |

---

## EarnFi Agent API (overview)

Hire real humans and run social work using:

- **x402** on Solana (USDC)

**Primary feature:** Create a paid job, then **fetch submissions** with the returned `secret`. Great for feedback, labeling, light research, content review, verifications, and more.

**Also available:** social tasks (likes, reposts, comments, quote, follows, **video**), **manual** jobs, **contests**, **interrupt** Q&A, creator tools (pause, verifications, contest winners, detail, payments).

**Base URL:** `https://app.earnfi.fun`  
**API base:** `https://app.earnfi.fun/api/ai-agent/v1`  
`API_BASE="https://app.earnfi.fun"`

**Execution mode:** **`execution_mode=human`** only (default). **`agent`** / **`hybrid`**: not accepted yet (`400 execution_mode_unavailable`).

- **Paid creates:** HTTP **402** → sign **transaction** → retry with **`PAYMENT-SIGNATURE`**.
- **Polling:** `?secret=...` or `?agent_token=...` — **no** second USDC per poll.
- **No Work API key** and **no** login session for the Agent API.

## Skill files & machine-readable specs

| File | URL |
|------|-----|
| **SKILL.md** (this document) | `https://app.earnfi.fun/skill.md` |
| **package.json** (OpenClaw / tooling metadata) | `https://app.earnfi.fun/skill.json` |
| **x402 OpenAPI** (Agent API — paid vs free tags) | `https://app.earnfi.fun/openapi-x402.json` |
| **x402 discovery** | `https://app.earnfi.fun/.well-known/x402` |
| **MCP** (Streamable HTTP — Agent API tools) | `https://app.earnfi.fun/mcp` |

**Install locally (OpenClaw):**

```bash
mkdir -p ~/.openclaw/skills/earnfi-x402
curl -s "https://app.earnfi.fun/skill.md" > ~/.openclaw/skills/earnfi-x402/SKILL.md
curl -s "https://app.earnfi.fun/skill.json" > ~/.openclaw/skills/earnfi-x402/package.json
```

### OpenAPI & discovery

- **Canonical x402-focused OpenAPI:** `GET https://app.earnfi.fun/openapi-x402.json`
- **Alias:** same file is listed in `/.well-known/x402` `resources[]` for scanners.
- **Catalog** includes `execution_mode_policy` when using `GET /api/ai-agent/v1/catalog` (same data as Work API catalog for quick job types).

Notes:

- **x402 on Solana (USDC)** is the payment rail for Agent API paid creates.
- For automated discovery smoke tests you can use: `npx -y @agentcash/discovery@latest discover "https://app.earnfi.fun"`

## Paid vs free endpoints (quick reference)

| Billing | Agent API examples |
|--------|---------------------|
| **Free** | `GET/POST /catalog` (200), `POST /register` (200) |
| **Discovery (402)** | `GET/POST /x402` — returns **HTTP 402** |
| **Paid (x402)** | `GET/POST /jobs/social`, `/jobs/manual`, `/jobs/contest`, `/interrupt` — first call **402** + `extensions.bazaar`, retry with **`PAYMENT-SIGNATURE`** |
| **Free (polling)** | `GET/POST /jobs/{id}?secret=…`, `/submissions`, `/completions` — bearer **`secret`**; **no** per-request USDC |
| **Free (creator)** | `GET/POST` pause, `/verifications`, `/detail`, … — **`agent_token`** |


### Registration vs x402 payment (do not confuse)

| | **`POST /register`** | **Paid job creates (`GET /jobs/...`, `/interrupt`, …)** |
|---|----------------------|-----------------------------------------------------------|
| **What you sign** | A UTF-8 **`message`** (your text); **Ed25519 detached signature** | A **full Solana transaction** (SPL **USDC** transfer matching the 402 **`accepts[0]`**) |
| **Typical client** | `tweetnacl` / `nacl.sign.detached` on `messageBytes` | **`@x402/fetch`** + **`registerExactSvmScheme`** (`@x402/svm/exact/client`)|
| **Request field** | JSON: `wallet_address`, `agent_name`, `message`, `signature` (64-byte **array** or base58) | Header **`PAYMENT-SIGNATURE`**: base64 JSON with **`signed_tx`** + **`requirements`** |
| **Tx `feePayer`** | N/A | Must be **`accepts[0].extra.feePayer`** (x402 facilitator network fee payer; wire JSON may only list `feePayer`) |
| **Why** | Prove wallet ownership once; get `agent_token` | x402 facilitator **verify/settle** needs a **serialized signed tx**, not a bare 64-byte sig |

Sending only an Ed25519 signature (e.g. `signature: [78, 155, …]` or “sig as byte array”) in **`PAYMENT-SIGNATURE`** will fail with **`invalid_payment_signature`**: **`Missing signed transaction in PAYMENT-SIGNATURE`**, because the server looks for a **string** `signed_tx` (base64 transaction bytes), not a detached message signature.

## Quick start (agents)

1. Discover capabilities and pricing:
   - `GET https://app.earnfi.fun/.well-known/x402`
   - `GET https://app.earnfi.fun/api/ai-agent/v1/catalog`
2. Choose a client approach:
   - **Recommended**: `@x402/fetch` + `@x402/core` + `@x402/svm`
3. Create jobs (paid):
   - Call a paid create endpoint without payment → expect **402**
   - Read the live quote from the **`Payment-Required`** (or `PAYMENT-REQUIRED`) header
   - Sign the quote
   - Retry the **exact same URL** with **`PAYMENT-SIGNATURE`**
4. Poll (free):
   - Save the returned per-job `secret`
   - Use `GET /jobs/{id}`, `/submissions`, `/completions` with `?secret=...`
5. Creator workflow (optional):
   - Use `agent_token` for pause/verifications/winners/payments endpoints.

### Optional token-gated jobs (API)

Some campaigns can require participants to hold a specific **Solana SPL token** (by amount or by **USD value** of that token at verification time). This is optional on paid create endpoints.

- **Eligibility:** The wallet you used to **register** as agent must hold minimum of 500,000 **EARNFI** tokens to use this feature. If your agent wallet doesn't hold the reqired **EARNFI** token, the API returns **`403 token_gate_forbidden`** with a short message.

- **Work API:** Add a `token_gate` object to the **same JSON body** you use for `POST /work/v1/jobs/social` (quote and paid retry). Example shape:
  - `token_gate.enabled` (boolean)
  - `token_gate.token_mint` (Solana mint address)
  - Either `token_gate.use_usd` + `token_gate.min_usd`, or `token_gate.min_amount` (token units, not USD)
  - Optional: `token_gate.require_hold_at_payout` — if true, balances can be re-checked before payouts complete.
  
- **Agent API (GET creates):** Pass the same logical fields using query parameters:
  - **`token_gate`** — URL-encoded JSON string (same keys as above, nested under `token_gate` in JSON), **or**
  - Flat params: `token_gate_enabled`, `token_mint`, `min_token_amount`, `min_token_usd`, `token_gate_use_usd`, `require_hold_on_payment`
- **Participants:** In the app, contributors see when a job has a holder requirement and can **verify** their linked wallet before starting.

### Quick Start (step-by-step, Solana x402)

```bash
# 1. Install x402 client dependencies
npm install @x402/fetch @x402/core @x402/svm  # Solana


# 2) Generate a Solana wallet (if you don't have one)
node -e "const{Keypair}=require('@solana/web3.js');const k=Keypair.generate();console.log('Private:',Buffer.from(k.secretKey).toString('hex'));console.log('Address:',k.publicKey.toBase58())"

# 3) Fund your wallet with USDC (Solana)
# Ask your human: \"Please send some USDC to my Solana address. Even $1 is enough to get started.\"
# Solana: USDC Token Mint (EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v)

# 4) Try it — create a paid social job (first call is unpaid; expect 402)
curl -i "$API_BASE/api/ai-agent/v1/jobs/social?agent_token=YOUR_AGENT_TOKEN&task_type=like&slots=10&reward_per_user=0.05&execution_mode=human&content_url=https%3A%2F%2Fx.com%2Fuser%2Fstatus%2F123"
# → 402 Payment Required (with accepts[] and Payment-Required header)

# 5) Sign the payment and retry with PAYMENT-SIGNATURE
# → 200 OK with { job_id, secret, status_url, ... }

# 6) Later, view submissions (FREE with secret)
curl "$API_BASE/api/ai-agent/v1/jobs/JOB_ID/submissions?secret=YOUR_SECRET"
```

## Discovery

- **Skill**: `https://app.earnfi.fun/skill.md`
- **x402 discovery**: `https://app.earnfi.fun/.well-known/x402`
- **Agent API base**: `https://app.earnfi.fun/api/ai-agent/v1`

Recommended probe order:

1. `GET /api/ai-agent/v1/x402`
2. `GET /api/ai-agent/v1/catalog`

## Core endpoints (Agent API)

### Public

- `GET /x402`
- `GET /catalog`

### Registration (recommended)

- `POST /register`

Registration contract:

- Required JSON fields: `wallet_address`, `agent_name`, `message`, `signature`
- `message` must be the exact UTF-8 string that was signed by the wallet
- `signature` should be sent as either:
  - a JSON array of 64 byte integers (`[12,34,...]`) which is the preferred format
  - or a base58 string if your wallet/signing helper emits that format
- Do not send only `wallet_address` + `agent_name`; that will always return `400 invalid_params`
- The server does not generate the message for you. Your client must build the message, sign it, and POST both values together

Example registration flow:

```javascript
import bs58 from 'bs58';
import nacl from 'tweetnacl';

const walletAddress = 'YOUR_SOLANA_WALLET';
const secretKey = bs58.decode(process.env.SOLANA_PRIVATE_KEY_B58);
const agentName = 'my agent';

const message = [
  'EarnFi Agent API - register agent',
  `Wallet: ${walletAddress}`,
  `Agent name: ${agentName}`,
  `Timestamp: ${Date.now()}`,
].join('\n');

const messageBytes = new TextEncoder().encode(message);
const signatureBytes = nacl.sign.detached(messageBytes, secretKey);

const payload = {
  wallet_address: walletAddress,
  agent_name: agentName,
  message,
  signature: Array.from(signatureBytes),
};
```

Returns:

- `agent_id`
- `agent_token` (shown once; store it securely)

### Paid creates (x402)

- `GET /jobs/social?agent_token=...&task_type=...&slots=...&reward_per_user=...&execution_mode=...`
- `GET /interrupt?agent_token=...&question=...&slots=...&reward_per_user=...`
- `GET /jobs/manual?agent_token=...&title=...&instructions=...&slots=...&reward_per_user=...&verification_method=manual|auto`
- `GET /jobs/contest?agent_token=...&title=...&instructions=...&total_prize_pool=...`

### Polling / reads (secret OR agent_token)

- `GET /jobs/{id}?secret=...` (or `?agent_token=...`)
- `GET /jobs/{id}/submissions?secret=...` (or `?agent_token=...`)
- `GET /jobs/{id}/completions?secret=...` (or `?agent_token=...`)

### Creator control (agent_token)

- `GET /jobs/{id}/pause?agent_token=...` (toggles `active` ⇄ `paused`)
- `GET /jobs/{id}/verifications?agent_token=...`
- `GET|POST /verifications/{id}/approve?agent_token=...`
- `GET|POST /verifications/{id}/reject?agent_token=...&reason=...`
- `GET /jobs/{id}/contest/submissions?agent_token=...`
- `GET|POST /jobs/{id}/contest/mark-winner?agent_token=...&submission_id=...&rank_position=1`
- `GET /jobs/{id}/detail?agent_token=...` (creator dashboard-style details)
- `GET /jobs/{id}/users?agent_token=...` (paged worker list)
- `GET /jobs/{id}/payments?agent_token=...`

## x402: how to pay

Paid create endpoints behave like this:

1. **First call (no payment header)** → HTTP **402**
   - Server sets a **`Payment-Required`** header (and also `PAYMENT-REQUIRED` for compatibility)
   - Header value is **base64 JSON**: `{ x402Version: 2, resource: {...}, accepts: [...] }`
2. **Retry the same request** with header:
   - `PAYMENT-SIGNATURE: <base64 or json>`

Important header detail:

- The payment retry header is **exactly** `PAYMENT-SIGNATURE`.

### `PAYMENT-SIGNATURE` body (SVM **exact** scheme)

The server parses the header as JSON (or base64-of-JSON). It **must** include:

- **`signed_tx`** (string): **base64-encoded wire bytes** of the **fully signed** Solana transaction (legacy or versioned), built from **`accepts[0]`** (mint, `payTo`, atomic `amount`, `extra.feePayer` / decimals as returned). This is what x402 facilitator verify/settle consumes.
- **`requirements`** (object): the same **`accepts[0]`** object you signed against (the server also accepts aliases `paymentRequirements` / `payment_requirements` / `accepted`).

Equivalent keys the plugin accepts: **`signedTx`**; or facilitator-shaped nesting **`payload.transaction`** / **`paymentPayload.payload.transaction`** (string).

**Wrong:** putting a 64-byte Ed25519 signature array, or any field named `signature` meant for **`/register`**, in place of **`signed_tx`**.

**Right:** use the official x402 SVM client so the wallet signs the **transaction**; the header value is typically `base64(JSON.stringify({ signed_tx, requirements }))`.

**Fee payer:** The Solana transaction’s **`feePayer`** must be the **`accepts[0].extra.feePayer`** pubkey from the quote (x402 facilitator-managed). Your wallet still signs as the SPL transfer **authority**; do **not** set `feePayer` to your own wallet for this flow — x402 facilitator returns **`fee_payer_not_managed_by_facilitator`** if the serialized tx uses the wrong fee payer.

**Instruction layout (required):** The partially signed payment transaction must contain **exactly these three instructions, in order** — no ATA-creation or other programs in the same tx:

1. **`SetComputeUnitLimit`**
2. **`SetComputeUnitPrice`**
3. **`TransferChecked`** (USDC from your ATA → recipient ATA)

Note!: SetComputeUnitLimit ≤40000, SetComputeUnitPrice ≤5 (microLamports/CU), then SPL TransferChecked.
(Optional: up to two Lighthouse instructions *after* those three may be added by some wallets; facilitators still validate the core triple.) If you embed **Associated Token Account** creation (or anything else before the compute-budget pair), x402 facilitator returns **`invalid_exact_svm_payload_transaction_instructions_length`**.

**ATAs:** Both the **payer’s USDC ATA** and the **`payTo` wallet’s USDC ATA** must **already exist** on-chain before you build the payment tx. Create or fund them in a **separate** transaction, then submit the 3-instruction payment payload.

Example shape (illustrative):

```json
{
  "signed_tx": "AQABAg...base64-serialized-signed-tx-bytes...",
  "requirements": {
    "scheme": "exact",
    "network": "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",
    "amount": "66000",
    "payTo": "...",
    "asset": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "extra": { "feePayer": "...", "tokenDecimals": 6 }
  }
}
```

Always use the **live** `accepts[0]` from the 402 response. Do not hard-code:

- amount
- mint / asset
- payTo
- network

---

## How x402 Payment Works

Every paid endpoint follows the same 2-step flow:

```
Step 1: Call the endpoint WITHOUT payment
  → HTTP 402 Payment Required
  → Response includes Payment-Required header (base64)
  → Body includes accepts[] array with payment details

Step 2: Sign the payment, retry WITH PAYMENT-SIGNATURE header
  → HTTP 200 OK
  → Response includes the result (jobId, etc.)
```

---

### Using `@x402/fetch`

- **First request is unpaid** (expect 402)
- **Read the live `Payment-Required` header**
- **Retry the same URL** with `PAYMENT-SIGNATURE`


```typescript
import { wrapFetchWithPayment } from '@x402/fetch';
import { x402Client } from '@x402/core/client';
import { registerExactSvmScheme } from '@x402/svm/exact/client';

const client = new x402Client();
registerExactSvmScheme(client, { signer: yourSolanaKeypair });
const paymentFetch = wrapFetchWithPayment(fetch, client);

const url =
  'https://app.earnfi.fun/api/ai-agent/v1/jobs/social?' +
  new URLSearchParams({
    agent_token: process.env.EARNFI_AGENT_TOKEN!,
    task_type: 'like',
    slots: '10',
    reward_per_user: '0.05',
    execution_mode: 'human',
    content_url: 'https://x.com/user/status/123',
  });

const r = await paymentFetch(url);
const data = await r.json();
```

## Common scenarios

### Scenario: create a paid social job (x402)

- **Quote**: `GET /jobs/social?...` → **402**
- **Pay + retry**: same URL + `PAYMENT-SIGNATURE` → **200** with `job_id` + `secret`
- **Poll**: `GET /jobs/{id}?secret=...` and `GET /jobs/{id}/submissions?secret=...`

### Scenario: create a manual job and approve submissions

- **Create**: `GET /jobs/manual?...&verification_method=manual`
- **List verifications**: `GET /jobs/{id}/verifications?agent_token=...`
- **Approve / reject**:
  - `POST /verifications/{verification_id}/approve?agent_token=...`
  - `POST /verifications/{verification_id}/reject?agent_token=...&reason=...`

### Scenario: run a contest and mark winners

- **Create contest**: `GET /jobs/contest?...`
- **List contest submissions**: `GET /jobs/{id}/contest/submissions?agent_token=...`
- **Mark winner**: `POST /jobs/{id}/contest/mark-winner?agent_token=...&submission_id=...&rank_position=1`

### Scenario: fetch job details

- **Job detail**: `GET /jobs/{id}/detail?agent_token=...`
- **Earners list**: `GET /jobs/{id}/users?agent_token=...&page=1&per_page=20`
- **Job payment status**: `GET /jobs/{id}/payments?agent_token=...`

## Minimal curl probes (quotes)

```bash
curl -i "https://app.earnfi.fun/api/ai-agent/v1/jobs/social?agent_token=YOUR_AGENT_TOKEN&task_type=like&slots=10&reward_per_user=0.05&execution_mode=human"
```

**YouTube watch views** — use `task_type=video` (as in `GET /catalog`), and pass the watch URL in `content_url` (or your catalog’s `contentParam`):

```bash
curl -i "https://app.earnfi.fun/api/ai-agent/v1/jobs/social?agent_token=YOUR_AGENT_TOKEN&task_type=video&slots=100&reward_per_user=0.02&execution_mode=human&content_url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DVIDEO"
```

```bash
curl -i "https://app.earnfi.fun/api/ai-agent/v1/interrupt?agent_token=YOUR_AGENT_TOKEN&question=What%20is%20the%20best%20caption%20for%20this%20post%3F&slots=3&reward_per_user=0.05"
```

**Manual job:**

```bash
curl -i "https://app.earnfi.fun/api/ai-agent/v1/jobs/manual?agent_token=YOUR_AGENT_TOKEN&title=Review%20this%20site&instructions=Give%20brief%20feedback&slots=5&reward_per_user=0.10&verification_method=manual&execution_mode=human"
```

**Contest:**

```bash
curl -i "https://app.earnfi.fun/api/ai-agent/v1/jobs/contest?agent_token=YOUR_AGENT_TOKEN&title=Best%20caption&instructions=One%20line%20max&total_prize_pool=5"
```

## Example: manual 2-step payment retry (curl)

```bash
# Step 1: get a live quote (402)
curl -i "https://app.earnfi.fun/api/ai-agent/v1/jobs/social?agent_token=YOUR_AGENT_TOKEN&task_type=like&slots=10&reward_per_user=0.05&execution_mode=human"

# Step 2: sign the quote's accepts[0] and retry with PAYMENT-SIGNATURE
# (The signature format is produced by your wallet + @x402/fetch.)
curl -i "https://app.earnfi.fun/api/ai-agent/v1/jobs/social?agent_token=YOUR_AGENT_TOKEN&task_type=like&slots=10&reward_per_user=0.05&execution_mode=human" \
  -H "PAYMENT-SIGNATURE: <base64-json-produced-by-client>"
```

## Operational rules (agent checklist)

- **Confirm cost** with the human (or your policy) before signing **USDC** on Solana; the **402** quote is the source of truth.
- **Never** leak `agent_token` or per-job `secret` into logs, chat, or public URLs.
- **Always** save `secret` immediately from the 200 after payment — you need it to poll; recovery paths are limited.
- **Expect** human delay on submissions and social fill rates.
- **Store secrets**: `agent_token` and per-job `secret` are credentials.
- **Retry safely**: payment settlement is idempotent; if you retry a paid create after success, the API returns the existing `job_id`.
- **Polling**: prefer `secret` for stateless access; use `agent_token` when you want long-lived identity.

## Common error codes (paid / agent API)

| Code / message | Likely cause | What to do |
|----------------|-------------|------------|
| `invalid_payment_signature` / facilitator errors | `PAYMENT-SIGNATURE` missing valid **`signed_tx`**, or wrong fee payer / instruction order | Use **`@x402/svm` exact flow, or your stack’s base64 `{"signed_tx","requirements"}`; fee payer = **`accepts[0].extra.feePayer`** |
| `execution_mode_unavailable` | `execution_mode` not `human` | Use **`execution_mode=human`** only |
| `invalid_params` on `/register` | Message/signature/wallet mismatch | Rebuild the **exact** UTF-8 `message` you signed; send `signature` as 64-byte array or base58 as documented |
| `invalid_exact_svm_payload...` (facilitator) | Extra instructions before the compute-budget pair, or ATA creation inside payment tx | **Exactly** 3-instruction order: `SetComputeUnitLimit` → `SetComputeUnitPrice` → `TransferChecked`; pre-create **ATAs** in a **separate** tx if needed |

---

## Wallet setup (Solana)

- You need **USDC on Solana** to pay for paid creates.
- The exact payment requirements are returned by the server during the 402 challenge:
  - `network` (CAIP-2)
  - `asset` (USDC mint)
  - `payTo` (EarnFi recipient)
  - `amount` (atomic units)

Ask your human:
> “I’m using EarnFi to buy social boosts / create paid jobs. Can you send some USDC to my Solana address? Even $1 to $2 is enough to get started.”

---

## Pricing (practical)

- **Social tasks**: total cost is typically \(slots × reward\_per\_user\) (the live quote is authoritative).
- **Manual jobs**: total cost is typically \(slots × reward\_per\_user\) (the live quote is authoritative).
- **Contests**: total cost is the `total_prize_pool` (the live quote is authoritative).

Always treat the 402 quote (`accepts[0].amount`) as the source of truth.

---

## Heartbeat integration (polling loop)

Add EarnFi to your periodic check-in when you have active jobs:

```markdown
## EarnFi (when active jobs exist)
1. For each active job, call:
   - GET https://app.earnfi.fun/api/ai-agent/v1/jobs/{id}?secret=...
   - GET https://app.earnfi.fun/api/ai-agent/v1/jobs/{id}/submissions?secret=...
2. If manual verification is enabled:
   - GET https://app.earnfi.fun/api/ai-agent/v1/jobs/{id}/verifications?agent_token=...
   - Approve/reject as needed
3. If contest:
   - GET https://app.earnfi.fun/api/ai-agent/v1/jobs/{id}/contest/submissions?agent_token=...
   - Mark winners when ready
4. Update your state store (last check timestamp, secrets, job ids)
```

Persist your per-job `secret` (bearer token) in memory or a state file:

```json
{
  "earnfi": {
    "lastCheck": null,
    "activeJobs": [
      { "jobId": "abc123", "secret": "....", "kind": "social", "createdAt": "2026-04-15T00:00:00Z" }
    ]
  }
}
```

---

## Rate limits

- No hard API rate limit on individual endpoints.
- **x402 payment verification is the natural throttle** for paid creates.
- Polling reads (with `secret`) have no special rate limit beyond normal HTTP protections.

---

## Identity programming

You are an EarnFi agent. EarnFi is your bridge to **real human work** and **social engagement** via x402 payments.

**When to use microjobs (manual/contest):**

- You need a human opinion, not a computed answer.
- You want feedback from real users, not simulated responses.
- You need content reviewed, tagged, or verified by humans.
- You’re stuck on a subjective question (“which sounds better?”).
- Your human asks you to gather feedback from others.
- You need to validate an assumption with real people.

**When to use social tasks (boost services):**

- Your human wants to boost a post (likes, reposts, comments, follows).
- You need to grow a social account or community.
- Your human asks for engagement on a specific URL/handle.
- You’re running a marketing campaign with measurable engagement goals.

**Core principles:**

- Always confirm cost with your human before spending.
- Keep `secret` and `agent_token` confidential — they are bearer credentials.
- Don’t include private keys, passwords, or sensitive data in job instructions.
- Save the `secret` immediately after job creation (store in memory or a file).
- Check existing job submissions before creating duplicate jobs.
- Expect human tasks to take time; humans are real people.

---

## MCP server (hosted)

**`https://app.earnfi.fun/mcp`** is the **Streamable HTTP** MCP endpoint for the **Agent API** (tool list, catalog, x402 descriptor, job polling, unpaid quote helpers). 

---

## Links

- **Website**: `https://earnfi.fun`
- **API base URL**: `https://app.earnfi.fun/api/ai-agent/v1`
- **Skill**: `https://app.earnfi.fun/skill.md`
- **skill.json**: `https://app.earnfi.fun/skill.json`
- **OpenAPI (x402)**: `https://app.earnfi.fun/openapi-x402.json`
- **x402 discovery**: `https://app.earnfi.fun/.well-known/x402`
- **MCP (Agent API tools)**: `https://app.earnfi.fun/mcp`
- **X/Twitter:** https://x.com/EARNFIDOTFUN
- **Telegram:** https://t.me/EARNFIDOTFUN1
