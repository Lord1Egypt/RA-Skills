---
name: supah-wallet-xray
description: "Instant wallet intelligence for any EVM address. Know who you're dealing with before you interact. Wallet age, transaction history, token holdings, DeFi activity, risk flags, ENS resolution, and a Trust Score (0-100). Works across 21+ EVM chains. x402 USDC micropayments on Base."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["curl", "node"], "env": ["SUPAH_API_BASE"] },
        "network": { "outbound": ["api.supah.ai"] },
        "x402": { "enabled": true, "currency": "USDC", "network": "base", "maxPerCall": "0.05", "payTo": "0xD3B2eCfe77780bFfDFA356B70DC190C914521761" }
      }
  }
---

# SUPAH Wallet X-Ray

**Know who you're dealing with. Instantly.**

Before you follow a trader, accept a payment, interact with a contract, or copy a trade — run their wallet through X-Ray. One address, full picture.

**$0.05 USDC per scan** — paid via x402 micropayment on Base. Your agent pays automatically per call. No API keys. Just USDC in your agent wallet on Base. [How x402 works](https://www.x402.org)

## What It Does

Wallet X-Ray builds a complete **intelligence profile** on any EVM address:

1. **Identity** — ENS name, labels (exchange, contract, whale, fresh wallet)
2. **Wallet Age & Activity** — First transaction, total txn count, activity frequency
3. **Holdings Snapshot** — Top token holdings, ETH/native balance, portfolio value
4. **DeFi Fingerprint** — Protocols used, LP positions, lending, staking activity
5. **Trading Track Record** — Win rate, biggest wins/losses, average hold time
6. **Risk Assessment** — Interaction with flagged contracts, mixer usage, dust attacks
7. **Network Analysis** — Top counterparties, funding source, cluster detection

Returns a **Trust Score (0-100)** with labels: TRUSTED / NEUTRAL / SUSPICIOUS / DANGEROUS

## Usage

Ask your agent naturally:

```
"Who is this wallet? 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
"X-Ray this address: 0x..."
"Is this wallet safe to interact with?"
"What does vitalik.eth hold?"
"Profile this trader before I copy their trades"
"Check if this wallet is a bot or a real person"
"Show me the track record for 0x..."
```

## Supported Chains

Base, Ethereum, BSC, Polygon, Arbitrum, Optimism, Avalanche, Fantom, Cronos, Gnosis, Celo, Moonbeam, zkSync Era, Linea, Scroll, Mantle, Blast, Mode, Manta, and more.

## Example Output

```
🔍 SUPAH WALLET X-RAY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Address: 0xd8dA...6045
ENS: vitalik.eth
Chain: Ethereum
Label: 🐋 WHALE | PUBLIC FIGURE

TRUST SCORE: 95/100 🟢 TRUSTED

┌──────────────────────────────────┐
│ Wallet Age        ████████ 100  │
│ Activity Level    ████████ 95   │
│ Portfolio Health  ███████░ 90   │
│ Trading Record    ███████░ 85   │
│ Risk Flags        ████████ 100  │
│ Network Quality   ████████ 95   │
└──────────────────────────────────┘

📊 PROFILE:
  • Age: 3,421 days (9.4 years)
  • Total transactions: 1,247
  • Active chains: ETH, Base, Optimism, Arbitrum
  • Last active: 2 hours ago

💰 HOLDINGS (Top 5):
  • 812.4 ETH ($1.52M)
  • 2.1M USDC ($2.1M)
  • 500K UNI ($3.8M)
  • 1.2M ENS ($15.6K)
  • Various NFTs (CryptoPunks, ENS domains)

🏦 DeFi ACTIVITY:
  • Uniswap (frequent swaps)
  • Aave (lending positions)
  • ENS (domain registrations)

⚠️ FLAGS: None
✅ CLEAN: No mixer interactions, no flagged contracts

VERDICT: Established whale with long history. Safe to interact.
```

## How It Works

The skill calls api.supah.ai via **x402 USDC micropayments** on Base. Your agent pays $0.05 per scan automatically — no API keys, no setup.

SUPAH's backend aggregates data from multiple sources:
- **Blockscout** — Transaction history, wallet age, token holdings
- **DexScreener** — Trading activity and token prices
- **GoPlusLabs** — Malicious address detection, approval risks
- **Moralis** — On-chain wallet indexing, token transfers, DeFi activity
- **ENS** — Name resolution

SUPAH is built on and utilizes **Moralis** for real-time wallet data indexing, adding proprietary trust scoring, cluster analysis, and smart money classification on top.

All data fetched in parallel for speed (typically <8 seconds).

## Requirements

- **`curl`** — HTTP client (pre-installed on most systems)
- **`node`** — Node.js v18+ runtime (for JSON parsing)
- **USDC on Base** — Your agent wallet must hold USDC on Base network for x402 micropayments ($0.05/scan)
- **x402-compatible HTTP client** — Payment happens automatically per call via the [x402 protocol](https://www.x402.org)

Optional: Set `SUPAH_API_BASE` environment variable to override the default API endpoint (default: `https://api.supah.ai`).

## Use Cases

- **Before copying a trader**: Check their actual win rate and track record
- **Before accepting payment**: Verify the sender isn't a flagged address
- **Before interacting with a contract**: Check if the deployer is trustworthy
- **Due diligence on partners**: Profile wallets before business deals
- **Whale watching**: Identify and classify large wallets
- **Bot detection**: Distinguish real traders from MEV bots

## Install

```bash
clawhub install supah-wallet-xray
```
