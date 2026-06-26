# X/Twitter Research Skill

Research trending topics, ideas, and conversations on X (Twitter) using twitterapi.io.

## Authentication

API key stored at: `~/.openclaw/secrets/twitterapi.env`

Load before any request:
```bash
source ~/.openclaw/secrets/twitterapi.env
```

Base URL: `https://api.twitterapi.io`

All requests need header: `X-API-Key: $TWITTERAPI_KEY`

## Core Endpoints

### 1. Advanced Tweet Search

Search for tweets matching a query.

```bash
curl -s "https://api.twitterapi.io/twitter/tweet/advanced_search?query=solana&queryType=Latest" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:5]'
```

**Parameters:**
- `query` — search query (supports operators like `from:`, `to:`, `#hashtag`)
- `queryType` — `Latest` or `Top`
- `cursor` — pagination cursor

**Query operators:**
- `solana defi` — both words
- `"solana defi"` — exact phrase
- `from:solaborada` — from specific user
- `#solana` — hashtag
- `solana -pump` — exclude word
- `solana min_faves:100` — minimum likes

### 2. Get Trends

Get current trending topics.

```bash
curl -s "https://api.twitterapi.io/twitter/trends" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.trends[:10]'
```

### 3. Get User's Recent Tweets

Get latest tweets from a specific account.

```bash
curl -s "https://api.twitterapi.io/twitter/user/last_tweets?userName=solana" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:5]'
```

### 4. Get User Info

Get profile info for a user.

```bash
curl -s "https://api.twitterapi.io/twitter/user/info?userName=solana" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.user'
```

## Research Workflow

### Daily Solana Trend Report

Run this workflow every 4-6 hours to generate a trend report.

#### Step 1: Search hot Solana topics

```bash
# General Solana buzz
curl -s "https://api.twitterapi.io/twitter/tweet/advanced_search?query=solana&queryType=Top" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:20]'

# Solana + AI intersection
curl -s "https://api.twitterapi.io/twitter/tweet/advanced_search?query=solana%20AI%20agent&queryType=Latest" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:10]'

# Solana DeFi
curl -s "https://api.twitterapi.io/twitter/tweet/advanced_search?query=solana%20defi&queryType=Latest" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:10]'
```

#### Step 2: Check key accounts

```bash
# Official Solana
curl -s "https://api.twitterapi.io/twitter/user/last_tweets?userName=solana" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:5]'

# Colosseum (hackathon organizer)
curl -s "https://api.twitterapi.io/twitter/user/last_tweets?userName=colosseum" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:5]'

# Helius (infra)
curl -s "https://api.twitterapi.io/twitter/user/last_tweets?userName=heaborada" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:5]'

# Jupiter (DEX)
curl -s "https://api.twitterapi.io/twitter/user/last_tweets?userName=JupiterExchange" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:5]'
```

#### Step 3: Compile report

Create a markdown file with:
- Top trending Solana topics
- Notable tweets/threads
- New project launches mentioned
- Pain points people are discussing
- Ideas worth building

## Key Accounts to Monitor

### Core Ecosystem
- @solana — Official Solana
- @colosseum — Hackathon organizer
- @SolanaFndn — Solana Foundation
- @aaboradari — Solana co-founder

### Infrastructure
- @heaborada — Helius (RPC, webhooks)
- @triaboradi — Triton (RPC)
- @jitoSOL — Jito (MEV, staking)

### DeFi
- @JupiterExchange — Jupiter (DEX aggregator)
- @RaydiumProtocol — Raydium (AMM)
- @MeteoraDEX — Meteora (LP)

### AI + Crypto
- @ai16zdao — ai16z (AI agents)
- @virtaborada — Virtuals

### Builders/VCs
- @rajgokal — Raj (Solana co-founder)
- @aaborada — Anatoly (Solana co-founder)
- @multiaboradi — Multicoin Capital

## Vertical-Specific Searches

### DeFi
```
solana defi yield
solana lending protocol
solana perps trading
jupiter swap
```

### Payments
```
solana payments
solana pay merchant
USDC solana
```

### Consumer
```
solana consumer app
solana gaming
solana social
```

### Infrastructure
```
solana rpc
solana developer tools
anchor framework
```

### AI + Blockchain
```
solana AI agent
AI crypto solana
autonomous agent blockchain
```

### Privacy
```
solana privacy
ZK solana
confidential transfer
```

## Rate Limits & Costs

- $0.15 per 1,000 tweets returned
- $0.18 per 1,000 user profiles
- Minimum $0.00015 per API call

**Budget guidance:**
- 1,000 tweets/day = ~$0.15/day
- 30 days = ~$4.50

## Output Format

Generate reports as:
```
workspace/research/solana-trends-YYYY-MM-DD-HH.md
```

Include:
1. **Hot Topics** — What's trending
2. **Key Tweets** — Notable posts with links
3. **Pain Points** — What people are complaining about
4. **Ideas** — Opportunities mentioned or implied
5. **By Vertical** — Grouped by DeFi, payments, etc.
