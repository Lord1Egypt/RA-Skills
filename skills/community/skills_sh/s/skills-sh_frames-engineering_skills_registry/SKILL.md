---
name: registry
version: 1.0.0
description: Pay-per-call API gateway for AI agents. 10 services available via x402 — no API keys, no subscriptions.
homepage: https://registry.frames.ag
metadata:
  category: api-gateway
  api_base: https://registry.frames.ag/api
  x402:
    supported: true
    chains:
      - evm
      - solana
    networks:
    - eip155:8453
    - eip155:84532
    - solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp
    - solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1
    tokens:
      - USDC
      - USDT
      - CASH
  services:
    count: 10
    slugs:
    - twitter
    - ai-gen
    - test
    - exa
    - wordspace
    - openrouter
    - jupiter
    - near-intents
    - agentmail
    - coingecko
    endpoints:
    twitter: /api/service/twitter
    ai-gen: /api/service/ai-gen
    test: /api/service/test
    exa: /api/service/exa
    wordspace: /api/service/wordspace
    openrouter: /api/service/openrouter
    jupiter: /api/service/jupiter
    near-intents: /api/service/near-intents
    agentmail: /api/service/agentmail
    coingecko: /api/service/coingecko
    skill_docs: /api/service/{slug}/skill.md
  wallet:
    recommended: agentwallet
    skill: https://frames.ag/skill.md
    endpoint: /x402/fetch
---

# Frames Registry

Pay-per-call API gateway for AI agents. 10 services available via the x402 payment protocol. No API keys, no subscriptions — just pay per request with crypto.

## Base URL

```
https://registry.frames.ag
```

## Prerequisites

A crypto wallet funded with USDC is required to use paid endpoints. Two options:

- **[AgentWallet](https://frames.ag/skill.md) (recommended for agents)** — server-side wallet that handles 402 detection, payment signing, and retries automatically via a single `POST /x402/fetch` call. No private key management needed on your side.
- **Self-managed wallet** — any EVM wallet (Base) or Solana wallet with USDC. You sign x402 payment headers directly.

## Quick Start

1. **Set up a wallet** — create an [AgentWallet](https://frames.ag/skill.md) or fund your own wallet with USDC
2. **Discover services:** `GET https://registry.frames.ag/api/services`
3. **Read service docs:** `GET https://registry.frames.ag/api/service/{slug}/skill.md`
4. **Check pricing:** `GET https://registry.frames.ag/api/pricing`
5. **Make a paid request** — via AgentWallet's `/x402/fetch` or directly with x402 headers (see Payment Protocol below)

## Services (10)

| Service | Slug | Description | Endpoints | Price Range |
|---------|------|-------------|-----------|-------------|
| [Twitter API](https://registry.frames.ag/api/service/twitter/skill.md) | `twitter` | Full Twitter API access - users, tweets, search, communities, spaces, trends, and more via twitterapi.io | 26 | $0.005 - $0.02 |
| [AI Generation API](https://registry.frames.ag/api/service/ai-gen/skill.md) | `ai-gen` | Run AI models for image, video, audio, and 3D generation | 1 | $0.01 |
| [x402 Test Service](https://registry.frames.ag/api/service/test/skill.md) | `test` | Test x402 payment flows on Base Sepolia (EVM) and Solana Devnet. Use this service to verify your x402 client integration is working correctly. | 2 | $0.001 |
| [Exa API](https://registry.frames.ag/api/service/exa/skill.md) | `exa` | Semantic web search via Exa | 4 | $0.002 - $0.01 |
| [Wordspace Agent](https://registry.frames.ag/api/service/wordspace/skill.md) | `wordspace` | AI agent loop with sandboxed execution and OpenProse skills | 1 | $2 |
| [OpenRouter](https://registry.frames.ag/api/service/openrouter/skill.md) | `openrouter` | Text generation via 300+ models (OpenAI, Anthropic, Google, Meta, etc.) | 0 | free |
| [Jupiter API](https://registry.frames.ag/api/service/jupiter/skill.md) | `jupiter` | Solana token swap, price, search, and portfolio via Jupiter | 4 | $0.002 - $0.01 |
| [NEAR Intents API](https://registry.frames.ag/api/service/near-intents/skill.md) | `near-intents` | Cross-chain token swaps via 1Click deposit addresses | 1 | $0.01 |
| [AgentMail API](https://registry.frames.ag/api/service/agentmail/skill.md) | `agentmail` | Email infrastructure for AI agents — create inboxes, send/receive emails, manage threads | 5 | $0.005 - $0.01 |
| [CoinGecko API](https://registry.frames.ag/api/service/coingecko/skill.md) | `coingecko` | Crypto price data, market info, and token search — prices, market caps, trending tokens, and search across 10,000+ cryptocurrencies | 5 | $0.002 - $0.005 |

## Service Endpoints

Each service lives at `https://registry.frames.ag/api/service/{slug}` and exposes:

| Endpoint | Description |
|----------|-------------|
| `GET /` | Service info |
| `GET /health` | Health check |
| `GET /docs` | Interactive API docs |
| `GET /openapi.json` | OpenAPI 3.x spec |
| `GET /skill.md` | Agent-friendly documentation |

## Pricing Details

### Twitter API (`twitter`)

Base: `https://registry.frames.ag/api/service/twitter` | [Docs](https://registry.frames.ag/api/service/twitter/docs) | [OpenAPI](https://registry.frames.ag/api/service/twitter/openapi.json) | [Skill](https://registry.frames.ag/api/service/twitter/skill.md)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `POST /api/user-info` | $0.005 | Look up a Twitter user's profile by username — returns bio, follower/following counts, verification status, and profile metadata |
| `POST /api/user-tweets` | $0.01 | Fetch a user's recent tweets by username or user ID, with optional reply inclusion and cursor pagination |
| `POST /api/user-followers` | $0.01 | List accounts following a user, paginated up to 200 per page with cursor-based navigation |
| `POST /api/user-following` | $0.01 | List accounts a user follows, paginated up to 200 per page with cursor-based navigation |
| `POST /api/verified-followers` | $0.01 | List only verified (blue-check) accounts following a user, by user ID with cursor pagination |
| `POST /api/search-users` | $0.01 | Search for Twitter users by keyword — matches against names, bios, and usernames |
| `POST /api/user-mentions` | $0.01 | Fetch tweets that @mention a user, with optional time range filtering (sinceTime/untilTime unix timestamps) |
| `POST /api/check-follow` | $0.005 | Check whether one user follows another — returns the follow relationship between two usernames |
| `POST /api/batch-users` | $0.02 | Fetch multiple user profiles in one request by comma-separated user IDs |
| `POST /api/tweets-by-ids` | $0.01 | Fetch full tweet data for multiple tweets by comma-separated tweet IDs |
| `POST /api/tweet-replies` | $0.01 | Get replies to a specific tweet, sortable by Relevance, Latest, or Likes with cursor pagination |
| `POST /api/search-tweets` | $0.01 | Advanced tweet search with operators — supports from:, to:, has:media, date ranges, engagement filters, and boolean logic |
| `POST /api/tweet-quotes` | $0.01 | Get all quote tweets of a specific tweet, with optional time range and reply inclusion filters |
| `POST /api/tweet-retweeters` | $0.01 | List users who retweeted a specific tweet, with cursor pagination |
| `POST /api/tweet-thread` | $0.01 | Retrieve the full conversation thread for a tweet — parent tweets and replies in context |
| `POST /api/list-tweets` | $0.01 | Fetch tweets from a Twitter List by list ID, with optional time range and reply filters |
| `POST /api/list-followers` | $0.01 | List users who follow a specific Twitter List, with cursor pagination |
| `POST /api/list-members` | $0.01 | List all members of a Twitter List, with cursor pagination |
| `POST /api/community-info` | $0.005 | Get a Twitter Community's metadata — name, description, member count, rules, and creation date |
| `POST /api/community-members` | $0.01 | List members of a Twitter Community, with cursor pagination |
| `POST /api/community-tweets` | $0.01 | Fetch tweets posted in a Twitter Community, with cursor pagination |
| `POST /api/space-detail` | $0.005 | Get details about a Twitter Space — title, host, participants, schedule, and state (live/scheduled/ended) |
| `POST /api/article` | $0.01 | Retrieve a long-form Twitter Article (Notes) by the tweet ID that contains it |
| `POST /api/trends` | $0.01 | Get trending topics for a location by WOEID (1=Worldwide, 23424977=US, 2459115=NYC) |
| `POST /api/invoke` | $0.01 | Search tweets (legacy — use /api/search-tweets instead) |
| `POST /api/search` | $0.01 | Search tweets (legacy — use /api/search-tweets instead) |

### AI Generation API (`ai-gen`)

Base: `https://registry.frames.ag/api/service/ai-gen` | [Docs](https://registry.frames.ag/api/service/ai-gen/docs) | [OpenAPI](https://registry.frames.ag/api/service/ai-gen/openapi.json) | [Skill](https://registry.frames.ag/api/service/ai-gen/skill.md)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `POST /api/invoke` | $0.01 | Run AI model prediction (price varies by model) |

### x402 Test Service (`test`)

Base: `https://registry.frames.ag/api/service/test` | [Docs](https://registry.frames.ag/api/service/test/docs) | [OpenAPI](https://registry.frames.ag/api/service/test/openapi.json) | [Skill](https://registry.frames.ag/api/service/test/skill.md)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `POST /api/invoke` | $0.001 | Test x402 payment flow (Base Sepolia & Solana Devnet) |
| `POST /api/echo` | $0.001 | Echo data with payment verification |

### Exa API (`exa`)

Base: `https://registry.frames.ag/api/service/exa` | [Docs](https://registry.frames.ag/api/service/exa/docs) | [OpenAPI](https://registry.frames.ag/api/service/exa/openapi.json) | [Skill](https://registry.frames.ag/api/service/exa/skill.md)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `POST /api/search` | $0.01 | Semantic web search |
| `POST /api/find-similar` | $0.01 | Find similar pages |
| `POST /api/contents` | $0.002 | Extract URL contents |
| `POST /api/answer` | $0.01 | AI-powered answer |

### Wordspace Agent (`wordspace`)

Base: `https://registry.frames.ag/api/service/wordspace` | [Docs](https://registry.frames.ag/api/service/wordspace/docs) | [OpenAPI](https://registry.frames.ag/api/service/wordspace/openapi.json) | [Skill](https://registry.frames.ag/api/service/wordspace/skill.md)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `POST /api/invoke` | $2 | Run wordspace AI agent loop |

### Jupiter API (`jupiter`)

Base: `https://registry.frames.ag/api/service/jupiter` | [Docs](https://registry.frames.ag/api/service/jupiter/docs) | [OpenAPI](https://registry.frames.ag/api/service/jupiter/openapi.json) | [Skill](https://registry.frames.ag/api/service/jupiter/skill.md)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `POST /api/swap` | $0.01 | Get swap quote and unsigned transaction |
| `POST /api/price` | $0.002 | Token price lookup |
| `POST /api/tokens` | $0.002 | Token search and metadata |
| `POST /api/portfolio` | $0.005 | Wallet portfolio positions |

### NEAR Intents API (`near-intents`)

Base: `https://registry.frames.ag/api/service/near-intents` | [Docs](https://registry.frames.ag/api/service/near-intents/docs) | [OpenAPI](https://registry.frames.ag/api/service/near-intents/openapi.json) | [Skill](https://registry.frames.ag/api/service/near-intents/skill.md)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `POST /api/quote` | $0.01 | Cross-chain swap quote and deposit address |

### AgentMail API (`agentmail`)

Base: `https://registry.frames.ag/api/service/agentmail` | [Docs](https://registry.frames.ag/api/service/agentmail/docs) | [OpenAPI](https://registry.frames.ag/api/service/agentmail/openapi.json) | [Skill](https://registry.frames.ag/api/service/agentmail/skill.md)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `POST /api/inbox/create` | $0.01 | Create a new email inbox for an AI agent |
| `POST /api/send` | $0.01 | Send an email from an agent inbox |
| `POST /api/messages` | $0.005 | List messages in an inbox |
| `POST /api/message` | $0.005 | Get a specific message by ID |
| `POST /api/threads` | $0.005 | List email threads in an inbox |

### CoinGecko API (`coingecko`)

Base: `https://registry.frames.ag/api/service/coingecko` | [Docs](https://registry.frames.ag/api/service/coingecko/docs) | [OpenAPI](https://registry.frames.ag/api/service/coingecko/openapi.json) | [Skill](https://registry.frames.ag/api/service/coingecko/skill.md)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `POST /api/price` | $0.002 | Get token prices in any fiat/crypto currency |
| `POST /api/token-info` | $0.005 | Get detailed token information and market data |
| `POST /api/trending` | $0.005 | Get currently trending tokens |
| `POST /api/markets` | $0.005 | Get token market data with sorting and pagination |
| `POST /api/search` | $0.003 | Search tokens by name or symbol |

### AI Model Pricing (`ai-gen`)

Price is set dynamically based on the `model` field in the request body.

**Image Models:**

| Model | Price |
|-------|-------|
| `flux/schnell` | $0.004/image |
| `flux/2-pro` | $0.02 |
| `flux/kontext-pro` | $0.05/image |
| `bytedance/seedream-4` | $0.04/image |
| `google/nano-banana` | $0.05/image |
| `google/nano-banana-2` | $0.09/image (1K), $0.13/image (2K), $0.19/image (4K) |
| `google/nano-banana-pro` | $0.18/image |
| `google/imagen-4-fast` | $0.03/image |
| `ideogram/v3-turbo` | $0.04/image |
| `prunaai/z-image-turbo` | $0.006/image |
| `prunaai/p-image` | $0.006/image |
| `fofr/sdxl-emoji` | $0.01 |
| `qwen/qwen-image-edit-2511` | $0.04/image |
| `openai/dall-e-3` | $0.15/image |
| `nightmareai/real-esrgan` | $0.003/image |

**Video Models:**

| Model | Price |
|-------|-------|
| `google/veo-3` | $0.48/sec (audio), $0.24/sec (no audio) |
| `google/veo-3-fast` | $0.18/sec (audio), $0.12/sec (no audio) |
| `google/veo-3.1` | $0.48/sec (audio), $0.24/sec (no audio) |
| `google/veo-3.1-fast` | $0.18/sec (audio), $0.12/sec (no audio) |
| `openai/sora-2` | $0.12/sec |
| `openai/sora-2-pro` | $0.36/sec (720p), $0.60/sec (1080p) |
| `kwaivgi/kling-v2.5-turbo-pro` | $0.09/sec |
| `kwaivgi/kling-v2.6` | $0.09/sec |
| `kwaivgi/kling-v2.6-motion-control` | $0.09/sec (std), $0.15/sec (pro) |
| `bytedance/seedance-1-pro` | $0.04/sec (480p), $0.08/sec (720p), $0.18/sec (1080p) |
| `bytedance/seedance-1-lite` | $0.03/sec (480p), $0.05/sec (720p), $0.09/sec (1080p) |
| `bytedance/seedance-1-pro-fast` | $0.02/sec (480p), $0.03/sec (720p), $0.08/sec (1080p) |
| `bytedance/seedance-1.5-pro` | $0.04/sec (720p), $0.07/sec (720p+audio) |
| `minimax/video-01` | $0.60 |
| `wan-video/wan-2.2-t2v-fast` | $0.12 |
| `wan-video/wan-2.2-i2v-fast` | $0.07 |
| `wan-video/wan-2.5-i2v-fast` | $0.09/sec (720p), $0.13/sec (1080p) |
| `runwayml/gen4-turbo` | $0.06/sec |
| `runwayml/gen4-aleph` | $0.22/sec |
| `veed/fabric-1.0` | $0.10/sec (480p), $0.18/sec (768p) |
| `shreejalmaharjan-27/tiktok-short-captions` | $0.002/sec |

## Payment Protocol (x402)

All paid endpoints use the [x402](https://www.x402.org/) payment protocol. No API keys needed.

**Flow:**

1. Call any paid endpoint without a payment header
2. Receive `402 Payment Required` with a `PAYMENT-REQUIRED` header (Base64 JSON with price, network, payTo address)
3. Sign a payment for the requested amount on your chosen network
4. Retry the same request with the `PAYMENT-SIGNATURE` header
5. Receive the response plus a `PAYMENT-RESPONSE` confirmation header

Failed requests are automatically refunded.

**Supported Networks:**

| Network | ID | Type | Environment |
|---------|----|------|-------------|
| Base | `eip155:8453` | EVM | Mainnet |
| Base Sepolia | `eip155:84532` | EVM | Testnet |
| Solana | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | Solana | Mainnet |
| Solana Devnet | `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` | Solana | Devnet |

**Accepted Tokens:** USDC, USDT, CASH (availability varies by network)

## Platform Endpoints (FREE)

| Endpoint | Description |
|----------|-------------|
| `GET https://registry.frames.ag/api` | Platform info and version |
| `GET https://registry.frames.ag/api/services` | List all services with metadata |
| `GET https://registry.frames.ag/api/services/:slug` | Single service details |
| `GET https://registry.frames.ag/api/pricing` | All pricing policies |
| `GET https://registry.frames.ag/api/networks` | Supported payment networks |
| `GET https://registry.frames.ag/api/health` | Health check |
| `GET https://registry.frames.ag/api/packages` | Skill/agent package catalog |
| `GET https://registry.frames.ag/api/packages/:slug/bundle` | Download package bundle |
| `GET https://registry.frames.ag/.well-known/x402` | x402 discovery document |
| `GET https://registry.frames.ag/docs` | Interactive docs (HTML) |

## Agent Integration

### With AgentWallet (recommended)

[AgentWallet](https://frames.ag/skill.md) is a server-side wallet for AI agents. It manages keys, balances, and x402 payment signing so agents don't need to handle crypto directly.

1. Authenticate with AgentWallet (email OTP → API token)
2. Fund your wallet with USDC on Base or Solana
3. Call any Frames Registry endpoint through AgentWallet's proxy:

```
POST https://frames.ag/x402/fetch
{
  "url": "https://registry.frames.ag/api/service/twitter/api/search-tweets",
  "method": "POST",
  "body": { "query": "AI agents" }
}
```

AgentWallet detects the 402 response, signs payment, and retries automatically.

### Direct x402 (self-managed wallet)

Requires an EVM or Solana wallet with USDC and the ability to sign EIP-3009 or SPL transfers.

1. Make the request to the paid endpoint
2. Parse the `PAYMENT-REQUIRED` header from the 402 response (Base64 JSON with price, network, payTo)
3. Sign a payment authorization for the exact amount
4. Retry with the `PAYMENT-SIGNATURE` header
