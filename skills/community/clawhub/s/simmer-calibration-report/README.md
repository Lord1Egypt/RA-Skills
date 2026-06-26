# 📊 Simmer Calibration Report

You've been trading for weeks. You have a feeling your BTC strategy kills it overnight. You think weather markets are your sweet spot. You're probably right — but you're guessing. This skill reads your trade journal and tells you exactly where your edge is concentrated, where it's thin, and where you're giving money back. No vibes. Just numbers.

## Live Demo

```
📊 Calibration Report — Last 30 days
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 287 trades | 68.3% WR | +$0.038 EV/trade
Journal: data/live/trade_journal.jsonl

BY STRATEGY
  btc_momentum         n=142  WR=72.5%  EV=+0.047  ██████████████
  eth_midcandle        n=67   WR=61.2%  EV=+0.021  ██████
  btc_midcandle_scalp  n=49   WR=65.3%  EV=+0.031  ████████
  eth_btc_lag          n=29   WR=58.6%  EV=+0.015  ████ (below min_n, informational)

BY HOUR (UTC)
  00-06                n=44   WR=75.0%  EV=+0.055  ██████████████████
  06-12                n=89   WR=70.8%  EV=+0.044  ████████████████
  12-18                n=97   WR=65.0%  EV=+0.031  ██████████
  18-24                n=57   WR=64.9%  EV=+0.028  █████████

BY PRICE BAND
  0.20–0.35            n=38   WR=73.7%  EV=+0.052  ██████████████████
  0.35–0.50            n=71   WR=70.4%  EV=+0.041  █████████████
  0.50–0.65            n=89   WR=66.3%  EV=+0.033  ██████████
  0.65–0.80            n=61   WR=63.9%  EV=+0.024  ████████
  0.80–0.95            n=28   WR=60.7%  EV=+0.018  ██████

Best segment: btc_momentum 00–06 UTC (WR=79.2%, n=21)
```

Every dimension. Every strategy. One command.

## Quick Start

1. **Install:** `pip install simmer-sdk`
2. **Set key:** `export SIMMER_API_KEY=your_key_here`
3. **Run:** `python calibration_report.py --live`

## What It Measures

The report breaks your performance across five dimensions. Each one answers a different question about your trading.

### Strategy

The obvious one. Is each strategy actually earning? A strategy can have a decent win rate and still lose money if the entry prices are wrong. EV per trade is the number that matters.

### Time of Day

Markets behave differently at different hours. Overnight crypto markets are thinner, weather markets get volatile near resolution. This breakdown shows you which hours are profitable and which are dead weight. If you're trading 24/7, you're probably leaving edge on the table — or worse, giving it back during your worst window.

### Price Band

Are you better at low-price NO bets or high-price YES bets? Most traders have a bias they don't realize. Buying at 0.25 and winning 70% of the time is very different from buying at 0.75 and winning 70% of the time — the EV math is completely different. This breakdown exposes that.

### Day of Week

Weekend markets are thinner. Fewer participants, wider spreads, sometimes easier money. Or maybe your edge disappears when liquidity drops. This tells you which days to push and which to sit out.

### Market Type

Crypto, weather, politics, sports — the report infers market type from question text and tags. You might think you're a generalist, but your numbers probably say otherwise. Find the category where your edge is real and concentrate there.

## Configuration

| Parameter | Env Var | Default | Description |
|-----------|---------|---------|-------------|
| `journal_path` | `CALIB_JOURNAL_PATH` | `""` | Path to trade journal JSONL. Empty = auto-detect. |
| `min_trades` | `CALIB_MIN_TRADES` | `10` | Minimum trades to display a segment. |
| `lookback_days` | `CALIB_LOOKBACK_DAYS` | `30` | How many days back to analyze. |
| `include_unresolved` | `CALIB_INCLUDE_UNRESOLVED` | `false` | Include unresolved trades in counts. |

## CLI Reference

```bash
# Report on sim journal (default)
python calibration_report.py

# Report on live journal
python calibration_report.py --live

# Show current config
python calibration_report.py --config

# Change lookback window
python calibration_report.py --set lookback_days=60

# Point at a specific journal file
CALIB_JOURNAL_PATH=/path/to/journal.jsonl python calibration_report.py

# Summary only (no breakdowns — good for cron)
python calibration_report.py --live --quiet
```

## Tips

- **Wait for sample size.** Run this after 30+ resolved trades per strategy. Before that, the numbers will mislead you. A 90% win rate on 8 trades means nothing.

- **Chase EV, not win rate.** EV matters more than WR. A 55% win rate on a 0.20-price market (EV ≈ +0.09) crushes a 70% win rate on a 0.70-price market (EV ≈ -0.01). The price band breakdown makes this obvious.

- **Concentrate on your best window.** If a time bucket shows 70%+ WR with n>20, that's signal. Shift your trading toward that window. Don't spread yourself evenly across hours where you break even.

- **Check after strategy changes.** Use `--set lookback_days=7` right after tweaking a strategy. You won't get statistical significance, but you'll see the direction fast.

- **Automate it.** Set the cron (default: daily at 08:00 UTC) and let it run with `--quiet`. When something changes, you'll see it in the summary line before you notice it in your balance.

## Troubleshooting

**"No journal found"**
The script looks for `data/live/trade_journal.jsonl` (or `data/sim/sim_trade_journal.jsonl` without `--live`). If your journal is elsewhere, set the path explicitly:
```bash
export CALIB_JOURNAL_PATH=/path/to/your/trade_journal.jsonl
```

**"0 resolved trades" or "No trades found"**
Your trades haven't resolved yet. Prediction markets take time. If you want to see pending trades anyway:
```bash
python calibration_report.py --set include_unresolved=true
```
Note: EV will be approximate since outcomes aren't final.

**Segment not showing up**
It's below the `min_trades` threshold (default: 10). If you have fewer trades and want to see everything:
```bash
python calibration_report.py --set min_trades=3
```
But take small-sample segments with a grain of salt.

**"SIMMER_API_KEY not set"**
```bash
export SIMMER_API_KEY=your_key_here
```

**"simmer-sdk not installed"**
```bash
pip install simmer-sdk
```
