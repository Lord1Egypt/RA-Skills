# Solana Wallet PnL Analyzer

Analyze any Solana wallet's trading history to decide if it's worth copy-trading.

## What it returns

- **Win Rate** — % of closed positions that were profitable
- **Realized PnL** — total SOL profit/loss from completed trades
- **Copy Rating** — FOLLOW / NEUTRAL / AVOID
- **Trader Type** — WHALE / DEGEN / TRADER / HOLDER / INACTIVE
- **Top Tokens** — most traded tokens with per-token PnL
- **Recent Trades** — last 10 swaps with side, token, SOL amount

## Quick Start

```bash
pip install -r api/requirements.txt
export HELIUS_API_KEY=your_key
python3 scripts/pnl.py <WALLET_ADDRESS>
```

## Paid API

`https://wallet-pnl-production.up.railway.app/pnl?wallet=<ADDRESS>`

$0.03 USDC per request via x402 on Base chain.

## License

MIT
