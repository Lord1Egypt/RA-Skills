---
name: simmer-calibration-report
displayName: "Simmer Calibration Report"
description: Run a calibration report on any Simmer trade journal. Win rate and EV broken down by strategy, time of day, price band, and market type. Know exactly where your edge lives — and where it doesn't.
version: "1.0.4"
authors:
  - name: "DjDyll"
difficulty: "beginner"
---

# 📊 Simmer Calibration Report

You think you know where your edge comes from. This skill tells you if you're right.

> **This is a template.** Point it at any Simmer JSONL trade journal — live, sim, or exported from anywhere — and get a full calibration breakdown. No strategy-specific logic baked in. Your journal, your numbers.

## Setup

1. Install dependencies:
   ```bash
   pip install simmer-sdk
   ```

2. Set your API key:
   ```bash
   export SIMMER_API_KEY=your_key_here
   ```

3. Run it:
   ```bash
   python calibration_report.py --live
   ```

That's it. If your journal exists at the default path, it just works.

## Configuration

| Parameter | Env Var | Default | Description |
|-----------|---------|---------|-------------|
| `journal_path` | `CALIB_JOURNAL_PATH` | `""` | Path to trade journal JSONL. Empty = auto-detect. |
| `min_trades` | `CALIB_MIN_TRADES` | `10` | Minimum trades to show a segment. Below this, the numbers lie. |
| `lookback_days` | `CALIB_LOOKBACK_DAYS` | `30` | How far back to analyze. |
| `include_unresolved` | `CALIB_INCLUDE_UNRESOLVED` | `false` | Include unresolved trades. EV becomes less meaningful. |

Set config inline:
```bash
python calibration_report.py --set lookback_days=60
python calibration_report.py --set min_trades=5
```

## Quick Commands

```bash
# Sim journal (dry run data)
python calibration_report.py

# Live journal
python calibration_report.py --live

# Custom journal path
CALIB_JOURNAL_PATH=/path/to/journal.jsonl python calibration_report.py

# Show config
python calibration_report.py --config

# Summary only (good for cron)
python calibration_report.py --live --quiet
```

## Example Output

```
📊 Calibration Report — Last 30 days
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 287 trades | 68.3% WR | +$0.038 EV/trade
Journal: data/live/trade_journal.jsonl

BY STRATEGY
  btc_momentum         n=142  WR=72.5%  EV=+0.047  ██████████████
  eth_midcandle        n=67   WR=61.2%  EV=+0.021  ██████
  btc_midcandle_scalp  n=49   WR=65.3%  EV=+0.031  ████████
  eth_btc_lag          n=29   WR=58.6%  EV=+0.015  ████

BY HOUR (UTC)
  00-06                n=44   WR=75.0%  EV=+0.055  ██████████████████
  06-12                n=89   WR=70.8%  EV=+0.044  ████████████████
  12-18                n=97   WR=65.0%  EV=+0.031  ██████████
  18-24                n=57   WR=64.9%  EV=+0.028  █████████

BY ENTRY PRICE
  0.20-0.35            n=38   WR=73.7%  EV=+0.052  ██████████████████
  0.35-0.50            n=71   WR=70.4%  EV=+0.041  █████████████
  0.50-0.65            n=89   WR=66.3%  EV=+0.033  ██████████
  0.65-0.80            n=61   WR=63.9%  EV=+0.024  ████████

🏆 Best segment: btc_momentum (EV=+0.047, WR=72.5%)
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "No journal found" | Set `CALIB_JOURNAL_PATH` explicitly, or ensure `data/live/trade_journal.jsonl` exists in your workspace. |
| 0 resolved trades | Trades haven't resolved yet. Set `CALIB_INCLUDE_UNRESOLVED=true` to see pending trades (EV will be approximate). |
| Segment not showing | Below `min_trades` threshold. Lower it: `python calibration_report.py --set min_trades=5` |
| "SIMMER_API_KEY not set" | `export SIMMER_API_KEY=your_key_here` |
| "simmer-sdk not installed" | `pip install simmer-sdk` |
