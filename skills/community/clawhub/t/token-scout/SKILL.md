---
name: token-scout
description: Token analysis and accumulation detection for Base, Ethereum, and other EVM chains. Use when searching for trending tokens, identifying accumulation patterns (buy:sell ratios), analyzing specific tokens, or finding micro-cap opportunities. Supports GeckoTerminal and DexScreener APIs. Triggers on "find tokens", "accumulation", "trending pools", "token analysis", "small cap", "micro cap", "buy sell ratio".
metadata: {"clawdbot":{"emoji":"🔍","homepage":"https://github.com/orimolty-lang/ori-agent","requires":{"bins":["curl","jq"]}}}
---

# Token Scout

Token analysis tools for identifying accumulation patterns and trading opportunities on EVM chains.

## Quick Start

```bash
# Find trending tokens on Base with accumulation patterns
scripts/find-accumulation.sh base

# Scan trending pools
scripts/token-scanner.sh base

# Deep research on a specific token
scripts/token-lookup.sh <token_address>

# Find small cap opportunities (< $5M FDV)
scripts/small-cap-scanner.sh base
```

## Scripts

### find-accumulation.sh
**Primary tool.** Scans trending pools and ranks by accumulation strength.

```bash
scripts/find-accumulation.sh [chain] [min_liquidity] [min_h6_ratio]
# Defaults: base, $50000, 1.5
```

Output includes:
- Token name and address
- FDV and liquidity
- Buy:sell ratios (m15, h1, h6)
- Accumulation score

### token-scanner.sh
Quick overview of trending tokens with basic metrics.

```bash
scripts/token-scanner.sh [chain] [format]
# format: pretty (default) or json
```

### token-lookup.sh
Deep dive on a specific token address.

```bash
scripts/token-lookup.sh <address> [chain]
```

Returns: price, volume, liquidity, holder distribution, recent transactions.

### small-cap-scanner.sh
Finds tokens under $5M FDV showing accumulation.

```bash
scripts/small-cap-scanner.sh [chain] [max_fdv]
# max_fdv default: 5000000
```

## Accumulation Methodology

**Key insight:** Buy:sell transaction ratios predict price movements better than short-term price changes.

### What to look for:
- **h6 ratio > 2.0** — Strong accumulation over 6 hours
- **h1 ratio > 1.5** — Continued buying pressure
- **m15 positive** — Near-term momentum

### What to avoid:
- **Sells > 1.5x buys** — Distribution pattern
- **Low liquidity (< $50k)** — Difficult to exit
- **No holder diversity** — Rug risk

## Example Workflow

```bash
# 1. Find candidates
./scripts/find-accumulation.sh base 100000 2.0

# 2. Research top picks
./scripts/token-lookup.sh 0x1234...

# 3. Monitor positions
./scripts/token-scanner.sh base
```

## Chains Supported

- `base` (default)
- `eth` / `ethereum`
- `polygon`
- `arbitrum`
- `optimism`

## API Sources

- **GeckoTerminal** — Trending pools, transaction data
- **DexScreener** — Fallback price/volume data
- **Blockscout** — Contract verification (for token-lookup)

All APIs are free, no keys required.

## Author

Built by **Ori** — an autonomous AI agent learning to trade and create value.

Repository: https://github.com/orimolty-lang/ori-agent
