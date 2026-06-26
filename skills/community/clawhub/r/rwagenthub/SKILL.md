---
name: rwagenthub
description: Call 32 real-world APIs — flights, hotels, weather, crypto prices, DeFi yields, stock quotes, web search, geocoding, IP reputation, blockchain data, code execution, and email — paying per call in USDC on Base via x402. Requires Node.js 20+ and a Base wallet with USDC.
homepage: https://agents-production-73c1.up.railway.app
user-invocable: true
metadata: {"openclaw":{"emoji":"🤖","requires":{"env":["AGENTHUB_WALLET_KEY"],"bins":["node","npm"]},"primaryEnv":"AGENTHUB_WALLET_KEY","install":[{"id":"sdk","kind":"node","package":"rwagenthub-sdk","label":"Install AgentHub SDK"}]}}
---

# AgentHub — 32 AI APIs, pay per call in USDC

You have access to **AgentHub**, a paid API gateway for real-world data.

- **What it does:** Routes API calls to 32 data providers (flights, weather, stocks, etc.)
- **How payment works:** Each call costs $0.01–$0.06 USDC, charged automatically via the x402 micropayment protocol on Base Mainnet. The wallet credential signs a gasless USDC transfer locally — no gas fees, no custody of funds by the gateway.
- **SDK source:** [npmjs.com/package/rwagenthub-sdk](https://www.npmjs.com/package/rwagenthub-sdk) — open source, auditable, no obfuscation. Only calls `https://agents-production-73c1.up.railway.app/v1/call` and the Base Mainnet RPC.
- **Gateway URL:** `https://agents-production-73c1.up.railway.app`

---

## Setup (one time)

### 1. Install the SDK

```bash
npm install --prefix ~/.openclaw/workspace/skills/rwagenthub rwagenthub-sdk@1.0.2
```

Installs the pinned SDK version into the skill's own folder. No global install required.

### 2. Configure your wallet credential

> ⚠️ Use a **dedicated wallet** funded only with the USDC you need for API calls. Do not use a primary wallet.

```bash
openclaw config set env.AGENTHUB_WALLET_KEY "YOUR_WALLET_CREDENTIAL"
```

The credential is used locally to sign a USDC micropayment authorization. Only the signed authorization (not the credential itself) is sent over the network. The gateway never receives or stores the credential.

### 3. Add USDC to your wallet on Base Mainnet

- Minimum recommended: $1 USDC (covers 100+ calls at $0.01 each)
- Acquire USDC via [Coinbase](https://coinbase.com) or any exchange, withdraw to Base network

---

## Before every call — verify SDK is installed

Run this check before making any API call. Installs automatically if missing:

```bash
SDK_DIR="$HOME/.openclaw/workspace/skills/rwagenthub"
[ -f "$SDK_DIR/node_modules/rwagenthub-sdk/index.js" ] || \
  npm install --prefix "$SDK_DIR" rwagenthub-sdk@1.0.2 --silent
```

If `AGENTHUB_WALLET_KEY` is not set, tell the user:
> "Please run: `openclaw config set env.AGENTHUB_WALLET_KEY \"YOUR_WALLET_CREDENTIAL\"`"

---

## How to call an API

For every API call, write a temporary script and run it with Node.js:

```bash
cat > /tmp/agenthub-call.mjs << SCRIPT
import AgentHub from "$HOME/.openclaw/workspace/skills/rwagenthub/node_modules/rwagenthub-sdk/index.js";
const hub = new AgentHub({ privateKey: process.env.AGENTHUB_WALLET_KEY });
const result = await hub.call('API_NAME', { ...inputs... });
console.log(JSON.stringify(result, null, 2));
SCRIPT
node /tmp/agenthub-call.mjs
```

Replace `API_NAME` and `{ ...inputs... }` with the API name and parameters from the list below.

---

## Available APIs

### ✈️ Travel

**`flight_search`** — $0.01
```js
await hub.call('flight_search', { from: 'EZE', to: 'JFK', date: '2026-04-15', adults: 1, cabin_class: 'economy' })
```

**`flight_search_pro`** — $0.01
```js
await hub.call('flight_search_pro', { from: 'MAD', to: 'NYC', date: '2026-06-01', adults: 1, cabin_class: 'ECONOMY' })
```

**`flight_status`** — $0.01
```js
await hub.call('flight_status', { carrier_code: 'AA', flight_number: '100', date: '2026-06-01' })
```

**`seat_map`** — $0.01
```js
await hub.call('seat_map', { offer_id: 'off_...' })
```

**`airport_search`** — $0.01
```js
await hub.call('airport_search', { country_code: 'AR', limit: 10 })
```

**`hotel_search`** — $0.06
```js
await hub.call('hotel_search', { city_code: 'NYC', check_in: '2026-04-01', check_out: '2026-04-03', adults: 2, ratings: '4,5' })
```

**`activities_search`** — $0.01
```js
await hub.call('activities_search', { latitude: 40.7128, longitude: -74.006, radius: 5 })
```

---

### 🌐 Web & Search

**`web_search`** — $0.02
```js
await hub.call('web_search', { query: 'best hotels in Paris 2026', type: 'search', num: 10 })
```

**`web_search_ai`** — $0.02
```js
await hub.call('web_search_ai', { query: 'latest AI agent news', count: 5, freshness: 'Week' })
```

**`web_search_full`** — $0.02
```js
await hub.call('web_search_full', { query: 'x402 protocol guide', limit: 3 })
```

**`places_search`** — $0.02
```js
await hub.call('places_search', { query: 'coffee shops', location: 'Tokyo, Japan', num: 5 })
```

**`image_search`** — $0.01
```js
await hub.call('image_search', { query: 'Patagonia landscape', num: 5 })
```

**`shopping_search`** — $0.02
```js
await hub.call('shopping_search', { query: 'carry-on luggage 40L', num: 5 })
```

**`url_extract`** — $0.02
```js
await hub.call('url_extract', { url: 'https://en.wikipedia.org/wiki/Patagonia', format: 'markdown' })
```

**`url_scrape`** — $0.01
```js
await hub.call('url_scrape', { url: 'https://example.com', only_main_content: true })
```

**`url_scrape_json`** — $0.02
```js
await hub.call('url_scrape_json', { url: 'https://news.ycombinator.com', prompt: 'extract top 3 story titles and point counts' })
```

---

### 🌤️ Weather & Location

**`weather_forecast`** — $0.01
```js
await hub.call('weather_forecast', { location: 'Buenos Aires', days: 7, units: 'metric' })
```

**`geocode`** — $0.01
```js
await hub.call('geocode', { query: 'Eiffel Tower, Paris', mode: 'forward' })
// reverse: { lat: 48.8584, lon: 2.2945, mode: 'reverse' }
```

---

### 💰 Crypto & DeFi

**`crypto_price`** — $0.01
```js
await hub.call('crypto_price', { coins: 'btc,eth,sol', vs_currency: 'usd' })
```

**`exchange_rate`** — $0.01
```js
await hub.call('exchange_rate', { from: 'USD', to: 'EUR,GBP,JPY', amount: 100 })
```

**`defi_market_snapshot`** — $0.02
```js
await hub.call('defi_market_snapshot', { top: 10 })
```

**`defi_yields`** — $0.02
```js
await hub.call('defi_yields', { stablecoin_only: true, no_il_risk: true, min_apy: 5, top: 10 })
```

---

### 📈 Stocks & Markets

**`stock_quote`** — $0.01
```js
await hub.call('stock_quote', { symbol: 'AAPL' })
```

**`stock_profile`** — $0.01
```js
await hub.call('stock_profile', { symbol: 'NVDA' })
```

**`stock_search`** — $0.01
```js
await hub.call('stock_search', { query: 'Apple', limit: 5 })
```

**`market_news`** — $0.01
```js
await hub.call('market_news', { category: 'general', limit: 10 })
// category options: 'general', 'forex', 'crypto', 'merger'
// add symbol: 'AAPL' for company-specific news
```

**`earnings_calendar`** — $0.01
```js
await hub.call('earnings_calendar', { from: '2026-04-01', to: '2026-04-30' })
```

---

### ⛓️ Blockchain & Security

**`alchemy_portfolio`** — $0.02
```js
await hub.call('alchemy_portfolio', { address: '0x...', networks: ['eth-mainnet', 'base-mainnet'] })
// networks: eth-mainnet, base-mainnet, arb-mainnet, opt-mainnet, polygon-mainnet, bnb-mainnet, avax-mainnet
```

**`alchemy_tx_history`** — $0.02
```js
await hub.call('alchemy_tx_history', { address: '0x...', networks: ['eth-mainnet'], page_size: 20, order: 'desc' })
```

**`opensky_flights`** — $0.01
```js
await hub.call('opensky_flights', { mode: 'live', limit: 20 })
// mode: 'live' | 'arrivals' | 'departures' — add airport: 'KJFK' for airport modes
```

**`ip_reputation`** — $0.01
```js
await hub.call('ip_reputation', { ip: '8.8.8.8', max_age_days: 90 })
```

---

### 🛠️ Utilities

**`code_exec`** — $0.05
```js
await hub.call('code_exec', { code: 'print(sum(range(1, 101)))', language: 'python', timeout: 30 })
// language: 'python' | 'javascript' | 'r' | 'bash'
```

**`email_send`** — $0.01
```js
await hub.call('email_send', { to: 'user@example.com', subject: 'Hello', text: 'Message body.' })
```

---

## Full example

Ask: *"What's the price of Bitcoin?"*

```bash
cat > /tmp/agenthub-call.mjs << SCRIPT
import AgentHub from "$HOME/.openclaw/workspace/skills/rwagenthub/node_modules/rwagenthub-sdk/index.js";
const hub = new AgentHub({ privateKey: process.env.AGENTHUB_WALLET_KEY });
const result = await hub.call('crypto_price', { coins: 'btc', vs_currency: 'usd' });
console.log(JSON.stringify(result, null, 2));
SCRIPT
node /tmp/agenthub-call.mjs
```

---

## Errors

| Error | Cause | Fix |
|---|---|---|
| `payment failed` | Insufficient USDC on Base | Top up wallet balance |
| `AgentHub: API error — unknown_api` | Wrong API name | Check spelling against the list above |
| `AgentHub: API error — invalid_inputs` | Missing or wrong parameters | Check the inputs for that API |
| `Cannot find module` / `ERR_MODULE_NOT_FOUND` | SDK not installed | Run `npm install --prefix ~/.openclaw/workspace/skills/rwagenthub rwagenthub-sdk@1.0.2` |