---
name: safetoken_fun
description: Discover and use SafeToken.fun — fair memecoin launchpad on BNB Chain. Create tokens with no API key; GET /api for contracts and ABI; POST /api/tokens to register. Built for AI agents and crawlers.
---

# SafeToken.fun — Memecoin Launchpad for AI Agents

SafeToken.fun is a **fair memecoin launchpad on BNB Smart Chain (mainnet)**. No API key required. AI agents and bots can create tokens, list tokens, and read curve state via public REST API and on-chain contracts.

**Contact:** contact@safetoken.fun  
**Base URL:** https://safetoken.fun  
**Chain:** BNB Smart Chain (chainId 56)

---

## Quick discovery

1. **API manifest (start here):** `GET https://safetoken.fun/api`  
   Returns JSON with `contracts.tokenFactory`, `contracts.launchpad`, `contracts.tokenFactoryAbi`, and all endpoint descriptions. Use this to get contract addresses and ABI for creating tokens.

2. **Health check:** `GET https://safetoken.fun/api/health`  
   Returns `{ "ok": true, "status": "up" }`. Use to verify the API is available before calling other endpoints.

3. **Full API docs:** https://safetoken.fun/api-docs  
   Human- and crawler-friendly page with schema.org WebAPI and FAQPage JSON-LD.

---

## Create a token (agent flow)

1. **GET** `https://safetoken.fun/api` → read `contracts.tokenFactory` (address) and `contracts.tokenFactoryAbi`.
2. On **BNB Chain (56)**, call **TokenFactory.createToken(name, symbol, burnPercent)** from a funded wallet.  
   - `burnPercent`: 30–70 (percent of supply burned at launch).  
   - One tx: deploys token, approves launchpad, initializes bonding curve, burns reserve.
3. **POST** `https://safetoken.fun/api/tokens` with JSON body:  
   `{ "mint": "<new_token_address>", "name": "<name>", "symbol": "<symbol>", "creator": "<wallet_address>", "burnPercent": <30-70> }`  
   Optional: `description`, `imageUrl`, `twitterUrl`, `telegramUrl`, `websiteUrl`, `launchpadAddress`.
4. Token then appears on https://safetoken.fun/tokens and can be traded on the bonding curve until graduation.

**Vanity address (optional):** To get a token address ending in `5afe`, first **POST** to `https://safetoken.fun/api/tokens/vanity-salt` with `{ "name", "symbol", "burnPercent" }` to receive `salt` and `predictedAddress`, then call **TokenFactory.createTokenWithSalt(name, symbol, burnPercent, salt)** on-chain.

---

## REST endpoints (no auth)

| Method | Path | Purpose |
|--------|------|---------|
| GET | /api | API manifest: contracts, ABI, endpoints, agent FAQ |
| GET | /api/health | Health check for bots |
| GET | /api/tokens | List tokens. Query: `page`, `limit`, `q`, `board` (all\|new\|graduating\|listed), `creator`, `mint`, `sort` (newest\|burn) |
| POST | /api/tokens | Register a token after on-chain creation (mint, name, symbol, creator, burnPercent required) |
| GET | /api/curve/:mint | Bonding curve state for one token |
| GET | /api/curves | Progress for multiple tokens. Query: `mints` (comma-separated) |
| GET | /api/metadata/:mint | Token metadata for explorers/wallets |
| GET | /api/token/:mint/holders | Holder count and distribution |
| POST | /api/tokens/vanity-salt | Compute CREATE2 salt for address ending in 5afe |

---

## Economics and safety

- **Barrier to launch:** One tx; bonding curve seeded with 0.1 BNB. Only ~0.05 BNB of buys needed to reach graduation (0.15 BNB threshold). No large bond.
- **LP (liquidity):** For every graduated token, liquidity is **permanently burned** to `0xdEaD` — no team rug. Users can verify on BscScan.
- **Tax:** 5% transfer tax (configurable at creation); helps against snipers and bundlers; portion to holders.
- **Platform:** No paid promotion. API and docs are built for **crawler and AI agent discoverability**.

---

## When to use this skill

- You need to **create a memecoin** on BNB Chain with minimal steps and no API key.
- You need to **list or discover** tokens created on SafeToken.fun.
- You need **bonding curve or metadata** for a token (curve progress, holders, metadata for wallets).
- You are a **crawler or agent** looking for a low-friction, agent-friendly launchpad.

Always start with `GET https://safetoken.fun/api` to get current contract addresses and ABI.
