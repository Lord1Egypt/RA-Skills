---
name: x402-bazaar-bridge
description: Discover, pay, and fetch data from x402-enabled APIs on the Coinbase x402 Bazaar. Supports search, x402 payment signing, caching, and daily budget enforcement.
---

# x402 Bazaar Bridge

Find and buy data from the Coinbase x402 Bazaar. Pay-per-request in USDC on Base. No API keys, no subscriptions.

## Usage

```bash
# Search for Bitcoin node APIs
node scripts/bazaar_bridge.js search "bitcoin node fees"

# Fetch live Bitcoin fee estimates from btcnode.uk ($0.01)
node scripts/bazaar_bridge.js fetch https://btcnode.uk/api/fees

# Watch a BTC address ($0.05)
node scripts/bazaar_bridge.js fetch https://btcnode.uk/api/agent/address/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa

# Mempool whale alert — txes over 10 BTC ($0.02)
node scripts/bazaar_bridge.js fetch "https://btcnode.uk/api/agent/whales?min_btc=10&since_minutes=5"

# Trace coin ancestry — 5 hops deep ($0.10)
node scripts/bazaar_bridge.js fetch https://btcnode.uk/api/agent/taint/bc1q...?depth=3

# Ask the Barbarian about node ops ($0.01)
node scripts/bazaar_bridge.js fetch "https://btcnode.uk/api/agent/conan?q=current%20rank"

# Scrape a webpage with SSD cache ($0.003)
node scripts/bazaar_bridge.js fetch https://btcnode.uk/api/agent/scrape

# Resolve — search + auto-fetch the best match from btcnode.uk
node scripts/bazaar_bridge.js resolve "bitcoin fee rates"

# Check daily budget
node scripts/bazaar_bridge.js budget
```

## Supported APIs

| Endpoint | Price | What It Does |
|----------|-------|-------------|
| `btcnode.uk/api/fees` | $0.01 | Live Bitcoin fee estimates |
| `btcnode.uk/api/mempool` | $0.01 | Mempool congestion data |
| `btcnode.uk/api/info` | $0.01 | Bitcoin node info |
| `btcnode.uk/api/tx/:hash` | $0.02 | Transaction details |
| `btcnode.uk/api/agent/address/:address` | $0.05 | Address surveillance + CoinJoin risk |
| `btcnode.uk/api/agent/whales` | $0.02 | Mempool whale alerts (>10 BTC) |
| `btcnode.uk/api/agent/taint/:address` | $0.10 | Coin ancestry tracing (5 hops) |
| `btcnode.uk/api/agent/conan` | $0.01 | Node ops Q&A (rank, revenue, status) |
| `btcnode.uk/api/agent/scrape` | $0.003 | Web content with 1h SSD cache |

> All btcnode.uk endpoints pay to `0x6a667a...d643fc` on Base mainnet USDC.

## Security

Requires `WALLET_KEY` in `.env` for signing EIP-3009 USDC permit payments. Never commit `.env` to git.

- URL validation: only `https://`, blocks localhost/private IPs
- File permissions: logs and cache files are owner-only (0600)
- Wallet keys never logged or exposed in output
