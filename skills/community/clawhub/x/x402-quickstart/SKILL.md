---
name: x402-quickstart
version: 1.0.0
description: Deploy x402 pay-per-call API endpoints in minutes. Turn any OpenClaw skill or service into a monetized endpoint accepting USDC on Base. Includes payment verification, pricing, and Cloudflare Tunnel integration. Use when deploying x402 endpoints, setting up agent payments, monetizing APIs, or building pay-per-call services.
---

# x402 Quickstart

Deploy x402-compatible pay-per-call endpoints that accept USDC payments from AI agents on Base.

## What is x402?

HTTP 402 ("Payment Required") is the standard for machine-to-machine payments. An agent sends a request, gets a `402` response with pricing info, pays in USDC on Base, and receives the data. No API keys, no accounts, no subscriptions.

**Ecosystem (Q1 2026)**: Stripe, Cloudflare, Google (AP2), Coinbase all ship native x402 support.

## Quick Deploy

### 1. Generate endpoint scaffold

```bash
bash scripts/scaffold.sh my-service "My cool API" 0.01
```

Creates a ready-to-run Express server with x402 payment middleware at `./my-service/`.

### 2. Configure wallet

Set your Base wallet address to receive payments:

```bash
# In the generated .env file
WALLET_ADDRESS=0xYourBaseWalletAddress
USDC_CONTRACT=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
CHAIN_ID=8453
PORT=3402
```

### 3. Run locally

```bash
cd my-service && npm install && node server.js
```

### 4. Expose via Cloudflare Tunnel (zero cost)

```bash
cloudflared tunnel --url http://localhost:3402
```

## How It Works

### Agent Flow

```
Agent → GET /api/data → 402 Payment Required
                         ├── price: "0.01 USDC"
                         ├── payTo: "0x..."
                         └── network: "base"
Agent → pays USDC on Base → gets tx hash
Agent → GET /api/data (X-Payment-Tx: 0x...) → 200 OK + data
```

### Server Flow

1. Request arrives without payment → respond `402` with pricing
2. Request arrives with `X-Payment-Tx` header → verify on-chain
3. If payment confirmed → serve data
4. If payment fails → respond `402` again

## Endpoint Ideas

High-value endpoints AI agents will pay for:

| Endpoint | Price | Description |
|----------|-------|-------------|
| `/alpha/scan` | $0.50-1.00 | Token/project analysis with scoring |
| `/market/signal` | $0.10 | Real-time trading signals |
| `/research/report` | $1.00 | Deep research on any topic |
| `/data/portfolio` | $0.05 | Multi-chain portfolio snapshot |
| `/tools/scrape` | $0.02 | Clean web content extraction |
| `/ai/inference` | $0.04 | LLM inference routing |

## Payment Verification

The scaffold includes `scripts/verify-payment.js` for on-chain verification:

```javascript
// Verifies USDC transfer on Base
const verified = await verifyPayment(txHash, expectedAmount, recipientAddress);
```

Uses Base RPC (free tier) — no API key needed for basic verification.

## Integration with OpenClaw

### As a skill endpoint

Add to your agent's capabilities:

```json5
// In SKILL.md or agent config
{
  tools: [{
    name: "my_x402_service",
    endpoint: "https://my-service.example.com/api",
    payment: { currency: "USDC", network: "base" }
  }]
}
```

### With Cloudflare Tunnel

Zero-cost hosting on your existing machine:

```bash
# One-time setup
cloudflared tunnel create my-x402
cloudflared tunnel route dns my-x402 api.mydomain.com

# Run
cloudflared tunnel run --url http://localhost:3402 my-x402
```

## Spraay Gateway Integration

Register your endpoint on [Spraay](https://gateway.spraay.app) to get discovered by agents automatically:

```bash
curl -X POST https://gateway.spraay.app/register \
  -H "Content-Type: application/json" \
  -d '{"url": "https://api.mydomain.com", "category": "data", "price": "0.01"}'
```

## Pricing Strategy

- **Data endpoints**: $0.005-0.05 (commodity, high volume)
- **Analysis endpoints**: $0.10-1.00 (value-add, medium volume)
- **Research endpoints**: $1.00-5.00 (premium, low volume)
- **GPU/compute**: $0.05-0.50 (resource-based pricing)

Start low, raise prices when you have traction. Better to have 1000 calls at $0.01 than 0 calls at $1.00.
