---
name: createos-deploy
description: Deploy projects to CreateOS infrastructure via the MPP Gateway. Use when the user wants to deploy code, ship an app, or deploy to CreateOS. No auth session or OAuth required — uses HTTP 402 payment flow only.
argument-hint: "[service] [plan]"
---

# Deploy to CreateOS

**No auth session, no OAuth, no browser login required.** This skill uses the HTTP 402 payment flow — the on-chain payment itself is the access control. Just call the API, pay with USDC/USDT, and deploy.

## Prerequisites

You need an EVM wallet with gas (ETH) and USDC on a supported chain. Generate one if needed:

```ts
import { generatePrivateKey, privateKeyToAccount } from "viem/accounts";
const privateKey = generatePrivateKey();
const account = privateKeyToAccount(privateKey);
// Save privateKey securely
```

Only dependency: `npm install viem`

## Flow

1. `POST /agent/deploy` (no payment) — gateway checks credits AND active projects
   - **Has credits, no active projects** → deploys directly, returns 200. Skip to step 5.
   - **Has credits, has active projects** → returns 402 with a warning. The agent must either:
     - **Pay** to extend total runtime (recommended), OR
     - **Retry with header `X-Use-Existing-Credits: true`** to deploy using existing credits (this will reduce runtime of the other active projects)
   - **No credits** → returns 402 with `pay_to`, `amount_token`, `payment_chain`, `supported_chains`
2. `GET /agent/balance/:address?chain=...` — check token balance on each supported chain
3. If no chain has enough balance, **stop and tell the user**:
   > "Your wallet `0x...` doesn't have enough funds to deploy. Please add **{amount_usd} {token}** on **{chain}** to address `0x...`."
   >
   > Show all supported chains so the user can pick one to fund.
4. Send ERC20 transfer to `pay_to` using viem → get `txHash`
   `POST /agent/deploy` with `X-Payment-Tx: txHash` → verifies payment, topups credits, deploys
5. `GET /agent/deploy/:projectId/:deploymentId/status` → poll until ready

## Credit Sharing & Active Projects

NodeOps credits are pooled across all your active projects and consumed hourly. When you have **multiple active deployments**, they share the same credit balance.

- If you have **0 active projects** and credits: deploys for free, no impact.
- If you have **1+ active projects** and you deploy without paying, the new project will share the credit pool — **reducing runtime of the other projects**.
- The gateway prevents this by default: if you have active projects, you must either pay (to add fresh credits) or explicitly opt in via `X-Use-Existing-Credits: true`.

**Always tell the user** when their deploy will affect other active projects, and recommend paying instead.

## Utility Endpoints (no auth required)

**Check balance** — all tokens on a chain:

```
GET /agent/balance/0xYourWallet?chain=arbitrum
```

```json
{
  "address": "0x...",
  "chain": "arbitrum",
  "balances": [
    { "token": "usdc", "symbol": "USDC", "balance": "18.000000", "decimals": 6 }
  ]
}
```

**List supported chains**:

```
GET /agent/chains
```

```json
{
  "chains": [
    { "chain": "arbitrum", "chain_id": 42161, "tokens": ["usdc", "usdt"] },
    { "chain": "base", "chain_id": 8453, "tokens": ["usdc", "usdt"] }
  ]
}
```

## Auth Headers (all requests)

Sign `{wallet}:{timestamp}:{nonce}` with your private key.

```
X-Wallet-Address: 0xYourWallet
X-Signature: 0xSignedMessage
X-Timestamp: 1711500000000
X-Nonce: unique-uuid
```

## List Your Projects (auth required)

```
GET /agent/projects
```

Returns all projects deployed by the wallet, with the live URL of the latest deployment for each.

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

`url` will be `null` if the project has no successful deployment yet. Status values: `active`, `building`, `deploying`, `pending`, `queued`, `promoting`, `deleting`, `failed`.

## Delete a Project (auth required)

```
DELETE /agent/projects/{projectId}
```

Permanently deletes a project from NodeOps. Only the wallet that originally deployed the project can delete it.

```json
{ "projectId": "uuid", "status": "deleted" }
```

Errors: `403` if the wallet is not the deployer.

## Step 1: Get Quote

```
POST /agent/deploy
Content-Type: application/json

{
  "uniqueName": "my-app",
  "displayName": "My App",
  "upload": { "type": "files", "files": [{ "path": "index.js", "content": "base64..." }] }
}
```

Response `402` (no credits):

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

Response `402` (has credits but active projects exist):

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

## Step 2: Pay

Send ERC20 transfer with viem:

```ts
import { createWalletClient, createPublicClient, http } from "viem";
import { arbitrum } from "viem/chains";

const txHash = await walletClient.writeContract({
  address: "0xaf88d065e77c8cC2239327C5EDb3A432268e5831", // USDC on arbitrum
  abi: [
    {
      name: "transfer",
      type: "function",
      stateMutability: "nonpayable",
      inputs: [
        { name: "to", type: "address" },
        { name: "value", type: "uint256" },
      ],
      outputs: [{ name: "", type: "bool" }],
    },
  ],
  functionName: "transfer",
  args: [quote.pay_to, BigInt(quote.amount_token)],
});
await publicClient.waitForTransactionReceipt({ hash: txHash });
```

## Step 3: Deploy

Same request body, add payment header:

```
POST /agent/deploy
X-Payment-Tx: 0xTransactionHash
X-Payment-Chain: arbitrum
X-Payment-Token: usdc
```

Response `200`:

```json
{ "projectId": "uuid", "deploymentId": "uuid", "status": "deploying" }
```

## Step 4: Poll

```
GET /agent/deploy/{projectId}/{deploymentId}/status
```

- `{ "status": "deploying" }` — keep polling every 5s
- `{ "status": "ready", "endpoint": "https://..." }` — done
- `{ "status": "failed", "reason": "..." }` — stop

## Upload Types

Files: `{ "type": "files", "files": [{ "path": "...", "content": "base64" }] }`
Zip: `{ "type": "zip", "data": "base64-zip", "filename": "code.zip" }`

**Important:** When uploading files, exclude build artifacts and dependencies:

- `node_modules/`, `dist/`, `build/`, `.next/`
- `.env`, `.env.*`, keys, secrets
- `.git/`, `.DS_Store`
- `__pycache__/`, `venv/`, `.venv/`

Only upload source code and config files needed to build and run the project.

## Error Codes

| Code | Meaning                                 |
| ---- | --------------------------------------- |
| 400  | Invalid body                            |
| 401  | Bad signature / expired / nonce reused  |
| 402  | Payment required or verification failed |
| 403  | Wrong wallet on status endpoint         |
| 409  | Tx hash already used                    |
| 429  | Rate limited (30/min)                   |

## Reference

- [api-reference.md](api-reference.md) — full endpoint specs
- [example.md](example.md) — complete working example
