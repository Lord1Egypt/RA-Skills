# Vantage — HL Autonomous Trading Agent

> Autonomous signal-to-execution trading agent for Hyperliquid perpetual futures.
> Runs on your machine. No cloud infra. No ongoing cost after purchase.

---

## Getting Started in 5 Steps

**Step 1 — Install dependencies**
```bash
npm install
```

**Step 2 — Configure your environment**
```bash
cp .env.example .env
```
Open `.env` and fill in at minimum:
- `HYPERLIQUID_PRIVATE_KEY` — your Hyperliquid account private key
- `HYPERLIQUID_WALLET_ADDRESS` — your wallet address
- `MAX_POSITION_SIZE_USD`, `MAX_OPEN_POSITIONS`, `MAX_ACCOUNT_RISK_PCT`

**Step 3 — Validate your setup**
```bash
node src/setup-check.js
```
Checks all required env vars, tests API connectivity, and verifies your private key
matches your wallet address. Fix any FAIL items before continuing.

**Step 4 — Run in paper mode first**
```bash
node src/index.js start --paper
```
Paper mode runs the full signal → decision → trade loop without placing real orders.
Watch at least one cycle complete before going live.

**Step 5 — Go live**
```bash
node src/index.js start
```
The agent now places real orders on your Hyperliquid account.

---

## How It Works

```
Every N minutes (CRON_INTERVAL_MINUTES, default: 60)
  Signal Engine  ->  funding rates + momentum + THORChain volume (public APIs)
    Decision Layer  ->  Qwen (local) | OpenAI (fallback) | rule-based
      Position Sizing  ->  Kelly criterion * live account balance
        Hyperliquid REST  ->  signed market order (your private key)
          Profit Sweep  ->  log if balance > threshold
```

All signal data uses **public APIs only** — no external API keys needed for market data.

---

## Configuration

All configuration lives in `.env`. Full annotated list in `.env.example`.

| Variable | Required | Default | Description |
|---|---|---|---|
| `HYPERLIQUID_PRIVATE_KEY` | Yes | — | Your HL account private key |
| `HYPERLIQUID_WALLET_ADDRESS` | Yes | — | Your wallet address |
| `MAX_POSITION_SIZE_USD` | Yes | 500 | Hard cap per position (USD) |
| `MAX_OPEN_POSITIONS` | Yes | 3 | Max concurrent open positions |
| `MAX_ACCOUNT_RISK_PCT` | Yes | 2 | Max % of balance at risk per trade |
| `KELLY_FRACTION` | Yes | 0.25 | Kelly multiplier (0.25 = quarter-Kelly) |
| `CRON_INTERVAL_MINUTES` | Yes | 60 | How often to run a cycle (minutes) |
| `SCAN_COINS` | No | BTC,ETH,RUNE,SOL,AVAX | Coins to scan |
| `OLLAMA_URL` | No | — | Local Ollama endpoint |
| `OLLAMA_MODEL` | No | qwen3.5:35b | Ollama model |
| `OPENAI_API_KEY` | No | — | OpenAI fallback |
| `PROFIT_SWEEP_ENABLED` | No | false | Enable profit sweep logging |
| `PROFIT_SWEEP_THRESHOLD_USD` | No | 100 | Sweep trigger (USD above baseline) |
| `PROFIT_SWEEP_ADDRESS` | No | — | Destination for profit sweep |
| `HYPERLIQUID_TESTNET` | No | false | Use testnet instead of mainnet |

---

## Signals

| Signal | Logic | Direction |
|---|---|---|
| Funding extreme | funding > +0.05%/hr (longs crowded) | Short |
| Funding extreme | funding < -0.05%/hr (shorts crowded) | Long |
| Price momentum | 24h change > +5% with positive OI | Long |
| Price momentum | 24h change < -5% with positive OI | Short |
| THORChain volume spike | ecosystem 24h vol > $100M | Long (RUNE) |
| Neutral | no threshold exceeded | Hold |

---

## Decision Layer

1. **Qwen (Ollama)** — if `OLLAMA_URL` is set and reachable (recommended)
2. **OpenAI** — if `OPENAI_API_KEY` is set (cloud fallback)
3. **Rule-based** — confidence >= 0.7 = trade, else hold (always available, no LLM needed)

---

## Position Sizing (Kelly Criterion)

```
Kelly %            = confidence  (edge proxy, odds ~1 for crypto perps)
Conservative Kelly = Kelly % * KELLY_FRACTION  (default: 0.25)
Size               = min(Conservative Kelly * balance, MAX_ACCOUNT_RISK_PCT%, MAX_POSITION_SIZE_USD)
```

Live account balance is fetched before every trade. If the fetch fails, the trade is
aborted — the agent never defaults to an arbitrary size.

---

## Commands

### Autonomous loop
```bash
node src/index.js start --paper   # paper mode (simulate only, no real orders)
node src/index.js start           # live trading (requires private key)
```

### Market data
```bash
node src/index.js hl-data RUNE    # prices + funding rate for RUNE
node src/index.js hl-data         # all active coins
```

### Positions
```bash
node src/index.js hl-positions 0xYourWalletAddress   # live positions
node src/index.js hl-positions --paper               # paper trade log
```

### Manual paper trade
```bash
node src/index.js hl-trade --coin RUNE --side long --size 10 --paper
node src/index.js hl-trade --coin ETH --side short --size 5 --price 2500 --paper
```

### Arb scanner
```bash
node src/index.js hl-arb               # default coin set
node src/index.js hl-arb BTC ETH RUNE  # specific coins
```
Compares THORChain spot prices (Midgard `assetPriceUSD`) vs Hyperliquid mark prices.

### THORChain routing
```bash
node src/index.js quote ETH.ETH BTC.BTC 100000000
node src/index.js inbound ETH
```

### Setup validator
```bash
node src/setup-check.js
```

---

## Moving Funds Cross-Chain

Need to bridge funds from another chain to fund your Hyperliquid account?

MoreBetter Studios has dedicated products for this:

- **Crypto Swap Agent** — [LINK TO BE UPDATED]
- **THORChain Swap Website** — [LINK TO BE UPDATED]

_(Links will be live shortly — check morebetterstudios.com/products)_

---

## Security

- Private key is **never logged** and never included in any error output
- Key format and cryptographic validity are checked before any API call
- `--paper` flag is enforced when `HYPERLIQUID_PRIVATE_KEY` is absent
- `.env` is gitignored — never commit it

---

## Project Structure

```
hyperliquid-agent/
├── src/
│   ├── index.js          # CLI entrypoint + autonomous loop
│   ├── signals.js        # Signal engine (public APIs, no keys required)
│   ├── sizing.js         # Kelly criterion position sizing
│   ├── trader.js         # Live order execution (EIP-712 signing)
│   ├── setup-check.js    # Pre-flight config validator
│   ├── hyperliquid.js    # Hyperliquid REST API module
│   ├── thorchain.js      # THORChain routing module
│   └── research.js       # Deprecated (replaced by signals.js)
├── data/
│   └── paper-trades.json # Paper trade store (gitignored)
├── .env.example
└── README.md
```

---

## Requirements

- Node.js 18+
- A Hyperliquid account with funds deposited
- Optional: [Ollama](https://ollama.com) running locally for LLM-powered decisions
