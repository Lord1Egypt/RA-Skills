---
name: warrior-trading
description: Ross Cameron's Warrior Trading methodology — Gap and Go, momentum day trading, low-float small-cap breakouts, and reversal strategies. Use when day trading US equities, scanning for gap setups, or executing momentum trades in the 9:30-11 AM ET window.
license: MIT
metadata:
  source: warriortrading.com, Ross Cameron
  category: day-trading
  market: us-small-cap
  session: pre-market + first 2 hours
---
# Warrior Trading — Ross Cameron Methodology

Small-cap momentum day trading. Target: stocks making 20-30% moves. Session: 9:30 AM–11 AM ET.

## Core Strategies

### 1. Gap and Go (9:30-10 AM ET)
Pre-market gappers >4% with a catalyst.

**Scanner Criteria:**
- Gap >4% from previous close
- Volume >100K pre-market
- Float <100M shares (ideal: <20M)
- News catalyst confirmed
- Price $2-20 range

**Entry:**
- Pre-market high breaks with volume
- Buy on first 1-min or 5-min candle to break pre-market high
- Ideal entry: flag pattern at pre-market high

**Exit:**
- Target 1: pre-market VWAP extension (1-2 ATR)
- Target 2: round number or prior resistance
- Stop: 10-20 cents below entry (tight)

**Risk Management:**
- Risk 10-20 cents per share
- Target 20-40 cents (2:1 reward/risk minimum)
- Max loss per trade: 1% of account
- Cut losers FAST — "Breakout or Bailout"

### 2. Momentum Trading (9:30-11 AM ET)
Stocks surging with volume right at the open, not necessarily gapping.

**Scanner Criteria:**
- Unusual volume spike (>5x average)
- Price surging on 1-min/5-min candles
- Float <20M ideal
- Relative volume >2
- Fresh news/catalyst

**Entry:**
- First pullback after surge (dip buy on momentum)
- Break of opening range high on second push
- Buy on 1-min candle close above prior 1-min high

**Exit:**
- Scale out: 1/2 at +20-30 cents, rest on trail
- Trailing stop: prior 1-min candle low
- HOD break with volume — hold for extension

### 3. Reversal Strategy (Late Morning)
Faded momentum stocks bouncing off support.

**Setup:**
- Stock that ran up 20-40% in first hour
- Pullback to VWAP or 9 EMA on 1-min
- Volume declining on pullback (not distribution)
- Support level holding (prior breakout, moving average)

**Entry:**
- Hammer/doji candle at support
- Buy on break of that candle's high
- Confirmation: volume increasing on the bounce

**Exit:**
- First target: VWAP or mid-point of morning range
- Stop: below the support candle low

## Scanner Setup (Trade Ideas / Finviz / DAS Trader)

```
Gap %: >4%
Volume: >100K pre-market
Float: <20M
Price: $2-$20
Relative Volume: >2
News: yes
```

## Key Rules

### Position Sizing
1 risk unit = 1% of account
Shares = (account × 0.01) / stop_distance
Example: $30K account, 10-cent stop = 30 shares
Hot key: BUY 100 shares with 10-cent stop

### The "Breakout or Bailout" Rule
If price doesn't move in your favor within 1-2 minutes, exit immediately.
Do NOT hold and hope. This is the single most important rule.

### Daily Routine
1. **8:00 AM**: Scan pre-market gappers (scanner + news)
2. **8:30 AM**: Build watchlist (3-5 names max)
3. **9:00 AM**: Mark support/resistance on daily + pre-market charts
4. **9:30 AM**: Execute Gap and Go setups
5. **10:00 AM**: Switch to momentum scans for new movers
6. **11:00 AM**: Done. Stop trading. Review P&L.

## Support/Resistance Mapping
- Daily moving averages: 9 EMA, 20 EMA, 50 SMA, 200 SMA
- Pre-market high/low
- Prior day high/low
- Round numbers ($5.00, $10.00, $15.00)
- Prior resistance (look left on daily chart)

## Anti-Patterns (Common Mistakes)
1. **Trading without a catalyst** — every gap needs a reason
2. **Holding losers** — "Breakout or Bailout" means cut immediately
3. **Overtrading** — max 3-5 trades per session
4. **Chasing** — never buy after 5+ green candles in a row
5. **Large caps** — avoid anything over $20 or float >100M
6. **After 11 AM** — win rate drops sharply, stop trading
7. **No stops** — hard stop ALWAYS set within seconds of entry