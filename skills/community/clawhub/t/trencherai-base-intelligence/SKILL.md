# TrencherAI — Base Chain Token Intelligence

TrencherAI is an AI-powered token scoring system for Base chain. It monitors Clanker, Bankr, and Doppler launches in real-time and scores them using a Claude Haiku reasoning pipeline with smart money tracking and pattern learning.

## Payment

All endpoints use x402 micropayments (USDC on Base). No API key required. Your agent pays per request automatically if you have an x402-compatible client.

> **No credentials required on TrencherAI's side.** Payment is handled entirely client-side by your x402-compatible agent using its own wallet. TrencherAI does not store, request, or have access to any client credentials.

- **Network:** Base Mainnet (eip155:8453)
- **Token:** USDC (0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913)
- **Pay-to:** 0xd3c3b0b35a9252f438ac3c86ca0ce18caa02ccab
- **Facilitator:** https://api.cdp.coinbase.com/platform/v2/x402
- **x402 Discovery:** https://api.aitrencher.xyz/.well-known/x402.json
- **ERC-8004 Agent:** https://www.8004scan.io/agents/base/29167

---

## Endpoints

### 1. Score a Token — $0.05 USDC

Analyze any Base chain token and get a 0-100 AI score with recommendation.

```
GET https://api.aitrencher.xyz/api/score-token?address={contract_address}
```

**Parameters:**

- `address` (required): Base chain ERC-20 contract address (0x + 40 hex chars)

**Example:**

```
GET https://api.aitrencher.xyz/api/score-token?address=0x4ed4e862860bed51a9570b96d89af5e1b0efefed
```

**Response (after x402 payment):**

```json
{
  "score": 82,
  "recommendation": "BUY",
  "smart_money": true,
  "pattern_win_rate": 0.73,
  "launchpad": "Clanker",
  "reasoning": "Strong smart money entry with high pattern confidence"
}
```

**Response fields:**

| Field | Type | Description |
|---|---|---|
| `score` | integer 0-100 | AI confidence score. 80+ = strong signal, 65-79 = moderate, <65 = weak |
| `recommendation` | string | `BUY`, `WATCH`, or `SKIP` |
| `smart_money` | boolean | Whether tracked smart money wallets are buying this token |
| `pattern_win_rate` | float | Historical win rate of similar token patterns (0.0-1.0) |
| `launchpad` | string | Token origin: `Clanker`, `Bankr`, `Doppler`, or `Base` |
| `reasoning` | string | One-line AI explanation of the score |

---

### 2. Hot Tokens Feed — $0.02 USDC

Get the top scoring Base chain tokens detected in the last N hours.

```
GET https://api.aitrencher.xyz/api/hot-tokens?limit={limit}&min_score={min_score}&hours={hours}
```

**Parameters:**

- `limit` (optional, default 10): Number of tokens to return (max 50)
- `min_score` (optional, default 70): Minimum score threshold
- `hours` (optional, default 24): Lookback window in hours

**Example:**

```
GET https://api.aitrencher.xyz/api/hot-tokens?limit=5&min_score=80&hours=12
```

**Response:**

```json
[
  {
    "symbol": "DEGEN",
    "address": "0x4ed4e862860bed51a9570b96d89af5e1b0efefed",
    "score": 95,
    "recommendation": "BUY",
    "launchpad": "Clanker",
    "has_smart_money": true,
    "alerted_at": "2026-04-05T14:30:00.000Z",
    "mcap": 45000
  }
]
```

---

### 3. Smart Money Activity — $0.10 USDC

Track smart money wallet movements on Base chain memecoins.

```
GET https://api.aitrencher.xyz/api/smart-money/activity?hours={hours}&limit={limit}
```

**Parameters:**

- `hours` (optional, default 24): Lookback window in hours
- `limit` (optional, default 20): Number of results (max 50)

**Example:**

```
GET https://api.aitrencher.xyz/api/smart-money/activity?hours=12&limit=10
```

**Response:**

```json
[
  {
    "symbol": "AGENT",
    "address": "0x...",
    "score": 88,
    "launchpad": "Doppler",
    "detected_at": "2026-04-05T15:00:00.000Z",
    "signal": "ACCUMULATION"
  }
]
```

---

## x402 Payment Flow

When your agent calls any endpoint, the server returns HTTP 402 with payment instructions:

```json
{
  "x402Version": 1,
  "accepts": [{
    "scheme": "exact",
    "network": "eip155:8453",
    "amount": "50000",
    "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "payTo": "0xd3c3b0b35a9252f438ac3c86ca0ce18caa02ccab",
    "maxTimeoutSeconds": 60
  }]
}
```

Your x402 client handles payment automatically. Example using Coinbase CDP:

> **Note:** `apiKeyId` and `apiKeySecret` in the example below are **your own Coinbase CDP credentials**, used by your agent to sign payments client-side. TrencherAI never receives, requests, or stores any credentials — all signing happens locally in your agent.

```javascript
import { createCdpAuthHeaders } from '@coinbase/x402';

const headers = createCdpAuthHeaders(apiKeyId, apiKeySecret);
const authHeaders = await headers();

const response = await fetch(
  'https://api.aitrencher.xyz/api/score-token?address=0x...',
  { headers: authHeaders.verify }
);
```

---

## Use Cases

- **Token screening:** Score newly launched tokens before buying
- **Portfolio monitoring:** Track scores of tokens you hold
- **Smart money following:** See what tracked wallets are accumulating
- **Market scanning:** Find the highest-scored tokens in the last 24h
- **Automated trading:** Use scores in your trading bot's decision pipeline

---

## Scoring Methodology

TrencherAI scores tokens 0-100 using multiple signals:

| Signal | Weight | Source |
|---|---|---|
| Smart Money Entry | High | On-chain wallet tracking via BaseScan |
| Telegram Mentions | Medium | Real-time group monitoring (50+ groups) |
| X/Twitter Sentiment | Medium | Post volume and sentiment analysis |
| Deployer Reputation | Medium | Historical deployer success rate |
| Pattern Win Rate | High | ML pattern matching against 1800+ outcomes |
| Liquidity Depth | Low | Pool analysis via DexScreener |
| Launchpad Trust | Base | Clanker/Bankr/Doppler = trusted LP lock |

**Score interpretation:**

- **90-100:** Exceptional confluence of signals. Rare (<5% of tokens).
- **80-89:** Strong signal. Smart money + social proof present.
- **65-79:** Moderate signal. Some positive indicators.
- **<65:** Weak or no signal. High risk.

---

## Links

- **Website:** https://aitrencher.xyz
- **Telegram Bot:** https://t.me/TrencherAIBot
- **ERC-8004 Registry:** https://www.8004scan.io/agents/base/29167
- **Coinbase Bazaar:** Indexed
- **X:** https://x.com/BasedJaider
