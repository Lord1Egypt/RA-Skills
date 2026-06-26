# 🍌 Ripe Scanner

Free, zero-cost momentum scanner for [OpenClaw](https://github.com/openclaw/openclaw) agents.

Scans **600+ stocks** (S&P 500 + Nasdaq 100) and **15 crypto** assets for momentum signals.
Combines technical analysis with social sentiment from StockTwits and Reddit.

**No API keys. No rate limits. Runs locally.**

![Ripe Scanner Demo](demo.png)

## Features

- 📊 **Technical Scoring** — RSI, EMA 20/50 alignment, Bollinger Squeeze, volume surge, 52-week proximity
- 💬 **Social Sentiment** — StockTwits bull/bear ratio + Reddit WSB mentions
- 📸 **Daily Snapshots** — Track score history and verify win rates over time
- 🔄 **Change Detection** — Spot newly ripe signals and big score jumps vs yesterday
- 🪙 **Crypto Support** — BTC, ETH, SOL, and 12 more
- 🏷️ **Badge System** — Ripe / Ripening / Overripe / Neutral / Rotten

## Quick Start

```bash
# Install dependencies
pip install yfinance pandas numpy

# Top momentum signals
python3 scripts/ripe-scan.py top --limit 10 --sentiment

# Look up individual tickers
python3 scripts/ripe-scan.py lookup TSLA NVDA BTC-USD

# Market overview
python3 scripts/ripe-scan.py pulse

# Score changes vs yesterday
python3 scripts/ripe-scan.py changes

# Save snapshot for history tracking
python3 scripts/ripe-scan.py snapshot --sentiment

# View historical win rate
python3 scripts/ripe-scan.py history
```

## Example Output

```
🏆 TOP 5 MOMENTUM SIGNALS
Symbol     Score Badge               Price       1d       5d   RSI  Sent
------------------------------------------------------------------------
 $MU          94 🍌 ripe         $  426.13   +5.1%   +9.4%    51   100
          ↳ EMA uptrend, Bollinger Squeeze, RSI 51 healthy zone
 $XOM         91 🍌 ripe         $  156.12   +1.7%   +3.8%    61   100
          ↳ Uptrend confirmed, Squeeze detected, Near 52-week high
₿$BTC-USD    66 🟡 ripening     $70831.62   -0.2%   +1.3%    59    60
          ↳ Squeeze detected, RSI 59 healthy, Reddit WSB active
```

## Scoring

| Component | Weight | Source |
|-----------|--------|--------|
| RSI (14) trend zone | 20% | yfinance |
| EMA 20/50 alignment | 20% | yfinance |
| Bollinger Squeeze | 15% | yfinance |
| Volume surge | 15% | yfinance |
| 52-week high proximity | 10% | yfinance |
| Social sentiment | 20% | StockTwits + Reddit |

## OpenClaw Installation

Copy to your skills directory:

```bash
cp -r ripe-scanner ~/.openclaw/workspace/skills/
```

Or clone directly:

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/NomadRex/ripe-scanner.git
```

## License

MIT
