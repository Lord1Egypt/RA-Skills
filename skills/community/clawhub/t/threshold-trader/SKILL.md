# Threshold Trader

A simple probability-threshold trading skill for prediction markets. Trades when market prices diverge from your configured probability threshold by a minimum edge amount.

> **This is a template.** The default signal is a fixed probability threshold — remix it with your own model predictions, external data feeds, or custom signals. The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## How It Works

1. **Monitor Markets**: Scans active markets on your configured venue (Polymarket or sim)
2. **Check Threshold**: Compares current market price against your configured probability
3. **Calculate Edge**: Only trades when edge exceeds minimum threshold (default 3%)
4. **Position Sizing**: Uses Kelly Criterion-based sizing for optimal stake amounts
5. **Safety Checks**: Reviews flip-flop warnings, slippage estimates, and edge analysis before executing
6. **Auto-Redeem**: Automatically collects payouts from resolved markets

## Configuration

Configure via environment variables:

- `THRESHOLD_PROBABILITY`: Your probability estimate (0.0-1.0). Default: 0.70
- `TRADE_SIDE`: Which side to trade ("YES" or "NO"). Default: "YES"
- `SIMMER_VENUE`: Trading venue ("sim" for paper, "polymarket" for real). Default: "sim"
- `SIMMER_MIN_EV`: Minimum edge to trade (0.0-1.0). Default: 0.03 (3%)
- `SIMMER_KELLY_MULTIPLIER`: Kelly fraction (0.0-1.0). Default: 0.25
- `MAX_POSITION_SIZE`: Maximum position size in USD. Default: 100.0

## Usage

Install the skill:

```bash
npx clawhub@latest install threshold-trader
```

Set your credentials and configuration:

```bash
export SIMMER_API_KEY="your-api-key-here"
export THRESHOLD_PROBABILITY="0.65"
export TRADE_SIDE="YES"
export SIMMER_VENUE="sim"  # or "polymarket" for real money
```

Run manually:

```bash
python threshold_trader.py
```

Or let the automaton run it every 15 minutes (configured in clawhub.json).

## Remixing

The core logic is in `should_trade()` — swap the fixed threshold for:

- **Your ML model**: Replace `THRESHOLD_PROBABILITY` with model predictions
- **External APIs**: Fetch signals from news feeds, social sentiment, or market data
- **Multi-market strategies**: Scan correlations across related markets
- **Event-driven**: React to external triggers (sports scores, election results)

The skill handles position sizing, safety checks, execution, and redemption. You focus on the signal.

## Safety Features

- **Flip-flop detection**: Skips trades if you've been reversing positions too frequently
- **Slippage protection**: Avoids illiquid markets with high slippage
- **Edge validation**: Only trades when expected value exceeds threshold
- **Dry-run default**: Paper trades unless you explicitly pass `--live`

## Examples

Paper trade YES when probability is above 70%:

```bash
export THRESHOLD_PROBABILITY="0.70"
export TRADE_SIDE="YES"
python threshold_trader.py
```

Real money trade NO when probability is below 30%:

```bash
export THRESHOLD_PROBABILITY="0.30"
export TRADE_SIDE="NO"
export SIMMER_VENUE="polymarket"
python threshold_trader.py --live
```

## Requirements

- `simmer-sdk` >= 1.0.0
- Python >= 3.8
- `SIMMER_API_KEY` from [simmer.markets/dashboard](https://simmer.markets/dashboard)

---
name: threshold-trader
description: Simple probability-threshold trading skill. Trades when market prices diverge from your configured threshold. Remixable template for custom signals.
metadata:
  author: "Simmer Community"
  version: "1.0.0"
  displayName: "Threshold Trader"
  difficulty: "beginner"
---
