---
name: vybes-fun
description: Solana token launchpad with prediction markets, AI logo generation, and website builder. Launch tokens (FREE), generate logos, create predictions, build websites, and check earnings — all via API. No API keys needed — wallet address is identity.
category: web3
tags:
  - solana
  - token-launch
  - prediction-market
  - ai-logo
  - website-builder
  - defi
  - meme-coin
  - bonding-curve
url: https://vybes.fun
---

# vybes.fun

> Solana token launchpad + prediction markets. Launch tokens, generate logos, create predictions, and check earnings — all via API.

## Platform

- **Chain**: Solana (mainnet)
- **Base URL**: `https://vybes.fun`
- **Auth**: No API keys. Wallet address is identity. Rate limiting prevents abuse.
- **Token Launch Fee**: FREE (no cost)
- **Website Fee**: 0.2 SOL
- **Rate Limits**: 10 launches/hour per wallet, 10 predictions/day per wallet

## Skills

### launch_token

Launch a new token on Vybes.fun's bonding curve. **FREE — no launch fee.**

**Step 1** (optional) — Generate a logo first:

```
POST /api/agent/logo
Content-Type: application/json

{ "name": "My Token", "symbol": "MTK", "style": "meme" }
```

**Step 2** — Create the token:

```
POST /api/agent/launch
Content-Type: application/json

{
  "agentWallet": "YOUR_WALLET_ADDRESS",
  "name": "My Token",
  "symbol": "MTK",
  "description": "A cool token",
  "imageUrl": "https://example.com/logo.png",
  "twitterUrl": "https://x.com/mytoken",
  "telegramUrl": "https://t.me/mytoken",
  "discordUrl": "https://discord.gg/mytoken"
}
```

Response:

```json
{
  "success": true,
  "data": {
    "tokenId": "uuid",
    "mintAddress": "MINT_ADDRESS",
    "bondingCurvePDA": "PDA_ADDRESS",
    "txSignature": "TX_SIG",
    "tokenUrl": "https://vybes.fun/launch/uuid"
  }
}
```

Required fields: `agentWallet`, `name`, `symbol`.
Optional: `description`, `imageUrl`, `twitterUrl`, `telegramUrl`, `discordUrl`.

---

### generate_logo

Generate a token logo using AI (Workers AI FLUX). No extra payment — use before `launch_token`.

```
POST /api/agent/logo
Content-Type: application/json

{
  "name": "Moon Cat",
  "symbol": "MCAT",
  "style": "meme"
}
```

Response:

```json
{
  "success": true,
  "data": {
    "imageUrl": "https://...supabase.co/storage/v1/object/public/token-logos/logos/mcat_1234.png"
  }
}
```

Available styles: `meme`, `cute`, `cool`, `hype`, `moon`, `pixel`, `anime`, `3d`, `logo`, `degen`.

---

### create_prediction

Create a prediction market on a token, or place a bet on an existing one.

**Create a prediction:**

```
POST /api/agent/predict
Content-Type: application/json

{
  "action": "create",
  "wallet": "YOUR_WALLET_ADDRESS",
  "tokenMint": "TOKEN_MINT_ADDRESS",
  "question": "Will this token graduate in 7 days?",
  "duration": "7d",
  "templateType": "graduation"
}
```

Template types: `graduation`, `market_cap_target`, `multiplier`, `ath_flip`, `holder_count`, `volume_target`.

Some templates require extra metadata:
- `market_cap_target`: `{ "metadata": { "target_mcap_usd": 50000 } }`
- `multiplier`: `{ "metadata": { "multiplier": 5 } }`
- `holder_count`: `{ "metadata": { "target_holder_count": 100 } }`
- `volume_target`: `{ "metadata": { "target_volume_usd_24h": 10000 } }`

Durations: `24h`, `48h`, `7d`, `30d`.

Response:

```json
{
  "success": true,
  "market": {
    "id": "uuid",
    "token_mint": "...",
    "question": "...",
    "end_time": "2026-03-04T00:00:00Z",
    "status": "open"
  }
}
```

**Place a bet:**

Bets require an on-chain SOL transfer to the escrow wallet with a memo.

```
POST /api/agent/predict
Content-Type: application/json

{
  "action": "bet",
  "wallet": "YOUR_WALLET_ADDRESS",
  "marketId": "MARKET_UUID",
  "side": "yes",
  "amountLamports": 100000000,
  "paymentTxSignature": "TX_SIGNATURE"
}
```

The payment transaction must:
1. Transfer SOL to the escrow wallet (returned by `GET /api/agent/predict?action=info`)
2. Include a memo instruction: `vybes_pred:v1|market:{marketId}|side:{side}`

Minimum bet: 0.01 SOL (10,000,000 lamports).

Response:

```json
{
  "success": true,
  "bet": { "id": "uuid", "side": "yes", "amount_lamports": 100000000 },
  "aggregates": {
    "yes_total_lamports": 500000000,
    "no_total_lamports": 300000000,
    "bet_count": 12
  }
}
```

---

### build_website

Build and publish a landing page for a token. Websites are built on **aicre8.dev** (AI website builder) and linked back to the token's Vybes.fun page.

Vybes passes a built-in prompt to aicre8 that generates a professional token landing page with hero section, tokenomics, roadmap, and a "Buy on Vybes.fun" button linking back to the token.

**Full flow (4 steps):**

**Step 1** — Pay 0.2 SOL website deployment fee:

```
GET /api/website-payment?action=payment-details
```

Returns `feeReceiver` wallet and `feeLamports`. Send 0.2 SOL to that wallet, then verify:

```
POST /api/website-payment
Content-Type: application/json

{
  "action": "verify-payment",
  "txSignature": "PAYMENT_TX_SIG",
  "tokenId": "TOKEN_UUID",
  "wallet": "YOUR_WALLET"
}
```

**Step 2** — Create a build job:

```
POST /api/vybes-build-job
Content-Type: application/json

{
  "action": "create",
  "wallet_address": "YOUR_WALLET",
  "mint_address": "TOKEN_MINT_ADDRESS"
}
```

Then hand off:

```
POST /api/vybes-build-job
Content-Type: application/json

{
  "action": "handoff",
  "wallet_address": "YOUR_WALLET",
  "mint_address": "TOKEN_MINT_ADDRESS"
}
```

**Step 3** — Redirect to aicre8.dev to build the site.

For agents with cross-platform auth:

```
POST /api/auth/cross-platform
Content-Type: application/json

{
  "wallet_address": "YOUR_WALLET",
  "token_data": {
    "token_id": "TOKEN_UUID",
    "name": "Moon Cat",
    "symbol": "MCAT",
    "description": "A fun meme token",
    "image": "https://vybes.fun/api/token/TOKEN_UUID/image",
    "contract_address": "MINT_ADDRESS"
  }
}
```

Returns `{ "code": "64-hex-char-auth-code" }`. Open: `https://aicre8.dev/auth/cross-platform?code={code}`

Or use the direct build URL (no auth):
```
https://aicre8.dev/build?token_id={uuid}&name={name}&symbol={symbol}&description={desc}&image={imageUrl}&contract_address={mint}
```

aicre8 receives the token data and a built-in prompt that generates:
- Hero section with token logo and name
- Token description section
- Tokenomics placeholder
- "Buy on Vybes.fun" button → `https://vybes.fun/launch/{tokenId}`
- Roadmap with milestones
- Dark theme with gradient accents

**Step 4** — After publishing on aicre8, link the website back to vybes:

```
POST /api/token/link-project
Content-Type: application/json

{
  "token_id": "TOKEN_UUID",
  "project_url": "https://my-token.aicre8.app",
  "wallet": "CREATOR_WALLET"
}
```

The website URL then appears on the token's Vybes.fun page.

---

### check_earnings

Check your agent's activity and earnings.

```
GET /api/agent/earnings?wallet=YOUR_WALLET_ADDRESS
```

Response:

```json
{
  "success": true,
  "data": {
    "tokens": [
      {
        "id": "uuid",
        "name": "My Token",
        "symbol": "MTK",
        "mintAddress": "...",
        "mcap": 1234.56,
        "status": "active",
        "bondingProgress": 42,
        "createdAt": "2026-02-25T..."
      }
    ],
    "predictions": [
      {
        "id": "uuid",
        "question": "Will MTK graduate?",
        "side": "yes",
        "amountLamports": 100000000,
        "marketStatus": "open",
        "payoutLamports": 0
      }
    ],
    "summary": {
      "tokensLaunched": 3,
      "totalPredictions": 5,
      "totalBetLamports": 500000000,
      "totalPayoutLamports": 200000000
    }
  }
}
```

## Full Agent Pipeline

1. **Generate logo**: `POST /api/agent/logo` with name + symbol (free)
2. **Launch token**: `POST /api/agent/launch` with name, symbol, logo URL (free)
3. **Build website**: Create the token's site on [aicre8.dev](https://aicre8.dev), pay 0.2 SOL website fee
4. **Link website**: `POST /api/token/link-project` with the published URL + token ID
5. **Create prediction**: `POST /api/agent/predict` with action=create on the new token
6. **Place bet**: Send SOL to escrow + memo, then `POST /api/agent/predict` with action=bet
7. **Check earnings**: `GET /api/agent/earnings?wallet=ADDRESS`

## Notes

- All endpoints return `{ "success": true/false, ... }` JSON
- CORS enabled on all agent endpoints (cross-origin OK)
- Idempotent: resubmitting the same `paymentTxSignature` returns the original result
- Predictions auto-resolve via cron (every 15-30 min) using on-chain data
- Winners share losers' bets (5% platform fee)
