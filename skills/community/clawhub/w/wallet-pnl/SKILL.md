---
name: wallet-pnl
description: |
  Analyze any Solana wallet's trading history: win rate, realized PnL, trader type,
  and copy-trade rating. Use when the user wants to check if a wallet is worth copying,
  analyze smart money performance, check a trader's win rate, evaluate a wallet's PnL,
  or decide whether to follow a wallet's trades.
  Keywords: copy trade, wallet analysis, win rate, PnL, smart money, trader stats.
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    env: ["HELIUS_API_KEY"]
    primaryEnv: "HELIUS_API_KEY"
---

# Solana Wallet PnL Analyzer

Analyze any Solana wallet's swap history to determine if it's worth copy-trading.
Returns win rate, realized PnL in SOL, trader classification, and top traded tokens.

## Paid API

$0.03 USDC per request via x402 on Base chain:

```bash
npx awal@latest x402 pay "https://wallet-pnl-production.up.railway.app/pnl?wallet=WALLET_ADDRESS"
```

## API Response

```json
{
  "wallet": "AbCd...XyZw",
  "summary": {
    "trader_type": "TRADER",
    "copy_rating": "FOLLOW",
    "total_trades": 87,
    "win_rate_pct": 64.3,
    "win_trades": 36,
    "loss_trades": 20,
    "realized_pnl_sol": 12.45,
    "avg_trade_size_sol": 0.85
  },
  "most_traded_tokens": [...],
  "recent_trades": [...]
}
```

## Copy Rating Guide

| Rating | Meaning |
|--------|---------|
| ✅ FOLLOW | Win rate ≥ 60% and positive PnL — worth copying |
| ⚠️ NEUTRAL | Mixed results — monitor before copying |
| 🚨 AVOID | Low win rate or negative PnL — do not copy |

## Trader Types

| Type | Meaning |
|------|---------|
| WHALE | Avg trade > 10 SOL |
| DEGEN | 50+ trades, high frequency |
| TRADER | Balanced buy/sell activity |
| HOLDER | Mostly buying, holding |
| INACTIVE | Fewer than 5 trades found |

## Self-Hosted

```bash
pip install -r {baseDir}/api/requirements.txt
python3 {baseDir}/scripts/pnl.py <WALLET_ADDRESS>
```

Requires `HELIUS_API_KEY` for transaction history (free at helius.xyz).
