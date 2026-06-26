---
name: supah-token-guardian
description: "Pre-trade token safety scanner for 21+ EVM chains. 6-layer deep scan: contract safety, liquidity health, deployer profiling, holder distribution, trading patterns, social signals. Returns Guardian Score (0-100) with BUY/CAUTION/AVOID verdict. x402 USDC micropayments on Base."
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires": { "bins": ["curl", "node"], "env": ["SUPAH_API_BASE"] },
        "network": { "outbound": ["api.supah.ai"] },
        "x402": { "enabled": true, "currency": "USDC", "network": "base", "maxPerCall": "0.08", "payTo": "0xD3B2eCfe77780bFfDFA356B70DC190C914521761" }
      }
  }
---

# SUPAH Token Guardian

**The most comprehensive pre-trade token safety scanner on ClawHub.**

Before you buy ANY token — run it through the Guardian. One command, full picture.

**$0.08 USDC per scan** — paid via x402 micropayment on Base. Your agent pays automatically per call. No API keys. Just USDC in your agent wallet on Base. [How x402 works](https://www.x402.org)

## What It Does

Token Guardian performs a **6-layer deep scan** on any token across 21+ EVM chains:

1. **Contract Safety** — Honeypot detection, mint authority, proxy risk, ownership renounced
2. **Liquidity Analysis** — Pool depth, lock status, LP concentration, rugpull probability
3. **Deployer Profiling** — Wallet age, deployment history, serial rugger detection
4. **Holder Distribution** — Top 10 concentration, insider clustering, wash trading flags
5. **Trading Pattern** — Buy/sell ratio, volume authenticity, sandwich attack exposure
6. **Social Signals** — Community size, organic vs botted engagement, team doxxing

Returns a single **Guardian Score (0-100)** with a clear BUY / CAUTION / AVOID verdict.

## Usage

Ask your agent naturally:

```
"Is 0x28538b9e45d1f40b801375bf3e6a378ec80a8a52 safe to buy?"
"Run a safety check on $OTTIE on Base"
"Should I ape into this token? [paste address]"
"Guardian scan 0x... on Ethereum"
"Check if this contract is a honeypot: 0x..."
"Full security report on $PEPE"
```

## Supported Chains

Base, Ethereum, BSC, Polygon, Arbitrum, Optimism, Avalanche, Fantom, Cronos, Gnosis, Celo, Moonbeam, Harmony, zkSync Era, Linea, Scroll, Mantle, Blast, Mode, Manta, and more.

## Example Output

```
🛡️ SUPAH GUARDIAN REPORT
━━━━━━━━━━━━━━━━━━━━━━━

Token: Ottie ($OTTIE)
Chain: Base
Address: 0x2853...8a52

GUARDIAN SCORE: 72/100 ⚠️ CAUTION

┌─────────────────────────────────┐
│ Contract Safety     ██████░░ 78 │
│ Liquidity Health    █████░░░ 65 │
│ Deployer Trust      ███████░ 85 │
│ Holder Distribution █████░░░ 62 │
│ Trading Patterns    ██████░░ 74 │
│ Social Signals      ██████░░ 70 │
└─────────────────────────────────┘

⚠️ RISKS DETECTED:
• Top 10 holders control 45% of supply
• Liquidity not locked (LP tokens in deployer wallet)
• Buy tax: 0% | Sell tax: 0% (clean)
• Contract not renounced (owner can modify)

✅ POSITIVE SIGNALS:
• No honeypot detected
• Deployer has clean history (3 prior tokens, none rugged)
• Organic trading volume ($4.4M/24h)
• Active community (2.1K holders)

VERDICT: CAUTION — Tradeable but monitor LP lock status.
Small position only. Set stop-loss.

NFA / DYOR — Data from GoPlusLabs, DexScreener, on-chain.
```

## How It Works

The skill calls api.supah.ai via **x402 USDC micropayments** on Base. Your agent pays $0.08 per scan automatically — no API keys, no setup.

SUPAH's backend aggregates data from multiple sources:
- **GoPlusLabs** — Contract security analysis (honeypot, taxes, ownership)
- **DexScreener** — Price, liquidity, volume, trading pairs
- **Moralis** — On-chain data indexing, token transfers, wallet activity
- **Block Explorers** — Deployer history, contract verification, holder data

SUPAH is built on and utilizes **Moralis** for its foundational on-chain data layer, adding proprietary 5-gate scoring, ML predictions, and narrative analysis on top.

All data is fetched in parallel for speed (typically <5 seconds).

## Requirements

- **`curl`** — HTTP client (pre-installed on most systems)
- **`node`** — Node.js v18+ runtime (for JSON parsing)
- **USDC on Base** — Your agent wallet must hold USDC on Base network for x402 micropayments ($0.08/scan)
- **x402-compatible HTTP client** — Payment happens automatically per call via the [x402 protocol](https://www.x402.org)

Optional: Set `SUPAH_API_BASE` environment variable to override the default API endpoint (default: `https://api.supah.ai`).

## Install

```bash
clawhub install supah-token-guardian
```

Or manually:
```bash
cd ~/.openclaw/skills
git clone https://github.com/supah-based/supah-token-guardian.git
```
