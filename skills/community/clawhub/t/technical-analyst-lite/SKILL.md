---
name: Technical Analyst Lite
slug: technical-analyst-lite
version: 1.0.0
description: >
  Basic technical analysis of price charts. Identifies trend direction, reads two
  key support/resistance levels, and gives a simple moving average assessment. Works
  on stocks, crypto, and indices. Free version — upgrade for pattern recognition,
  probability-weighted scenarios, and full indicator confluence analysis.
author: OpenClaw Skills
tags: [technical-analysis, charting, trading, stocks, crypto, free]
metadata:
  emoji: 📈
  requires:
    tools: []
    capabilities: [vision]
  os: [linux, darwin, win32]
---

# Technical Analyst Lite

> *"The tape tells all."* — Jesse Livermore

**📊 Want pattern recognition, probability scenarios, and full indicator analysis?**
**Full version → [agentofalpha.com](https://agentofalpha.com)**

---

## What This Skill Does

Systematic, objective technical analysis of price charts — without the noise. Give me a chart and I'll tell you the trend, where price is likely to find support or resistance, and what the moving averages are saying.

**Included in Lite:**
- ✅ Trend identification (uptrend / downtrend / sideways) with strength read
- ✅ 2 key support levels + 2 key resistance levels (specific prices)
- ✅ Moving average configuration (50-day vs 200-day read)
- ✅ Overall technical bias (bullish / bearish / neutral)

**Upgrade to Full for:**
- ❌ Chart pattern recognition (flags, H&S, wedges, cup & handle, etc.)
- ❌ Volume analysis and confirmation
- ❌ RSI, MACD, and indicator divergence signals
- ❌ 2-4 probability-weighted price scenarios
- ❌ Multi-timeframe alignment (monthly → weekly → daily)
- ❌ Measured move targets and pattern completion triggers

---

## How to Use

**Provide:**
- A chart image (weekly or daily timeframe — weekly preferred)
- The asset name or ticker
- Optional: what you're trying to decide (entry, exit, stop placement)

I'll give you a clean, objective read. No fundamentals, no news — pure price action.

---

## Analysis Workflow

### Step 1: Orient to the Chart

Before anything else, confirm:
- **Asset and timeframe** (weekly = more reliable signals)
- **Price scale** (linear vs. log)
- **Date range visible**
- **What's on the chart** (candles/bars, MAs, any indicators visible)

If the chart is unclear or cut off, ask for a better version.

---

### Step 2: Trend Identification

**Define the primary trend from the chart:**

| Signal | Uptrend | Downtrend | Sideways |
|--------|---------|-----------|----------|
| Price structure | Higher highs + higher lows | Lower highs + lower lows | Contained swing range |
| Moving averages | Price above rising MAs | Price below falling MAs | MAs flat and entangled |
| General feel | Staircase up | Staircase down | Horizontal chop |

**Trend strength:**
- **Strong**: Steep angle, minimal counter-trend swings, price closes consistently in the trend direction
- **Moderate**: Clear direction but regular pullbacks, average slope
- **Weak**: Shallow slope, large counter-trend moves eating into gains
- **Potentially reversing**: Sequence of higher highs / lower lows broken; momentum stalling

**State:** `[Uptrend / Downtrend / Sideways] — [Strong / Moderate / Weak]`

---

### Step 3: Support and Resistance (2 + 2)

Identify the **2 most important support levels** and **2 most important resistance levels** from the chart.

**How to spot them:**
- **Prior swing highs/lows** — Price turned multiple times at this level
- **Round numbers** — $100, $50, $500 act as psychological anchors
- **Role reversal zones** — Old resistance that was broken becomes support (and vice versa)
- **Prior consolidation areas** — Where price spent significant time before a move

**For each level, note:**
- The specific price
- Why it matters (how many tests, role reversal, round number, etc.)
- Whether it's currently being tested or is a distance away

**Format:**
```
Support 1: $XXX — [reason: prior low tested 3×, role reversal from resistance]
Support 2: $XXX — [reason: prior consolidation zone, round number]
Resistance 1: $XXX — [reason: prior swing high, untested breakout level]
Resistance 2: $XXX — [reason: all-time high region, multiple rejections]
```

**Proximity note:** Is price currently near support (favorable long entry risk/reward) or near resistance (unfavorable)?

---

### Step 4: Moving Average Read

If moving averages are visible on the chart, assess:

**The key levels:**
- **50-period MA**: Intermediate trend health. Price consistently above = intermediate uptrend.
- **200-period MA**: Long-term dividing line. Above = bull territory. Below = bear territory.

**Configuration signals:**
- **Golden Cross**: 50-MA crosses ABOVE 200-MA → long-term bullish signal
- **Death Cross**: 50-MA crosses BELOW 200-MA → long-term bearish signal
- **Bullish stack**: Price > 50-MA > 200-MA, both rising → strongest bull setup
- **Bearish stack**: Price < 50-MA < 200-MA, both falling → strongest bear setup
- **Mixed**: Transitioning or choppy — treat with caution

**MA as support/resistance:**
- Is price bouncing off a rising MA? (Healthy uptrend behavior)
- Is price getting rejected at a falling MA? (Bearish structure)
- How far is price stretched from the 200-MA? (Extreme distance = mean reversion risk)

**If MAs are not visible on the chart:** Note the limitation and work from price structure alone.

---

### Step 5: Overall Technical Bias

Synthesize the above into a single assessment:

- **Bias**: Bullish / Bearish / Neutral / Cautiously [Directional]
- **Conviction**: High / Medium / Low
- **Key level to watch**: The one price that, if broken, changes the whole picture

---

## Output Format

```markdown
## Technical Read: $[TICKER] — [Timeframe] Chart
**Date:** [Date]

---

### Trend
**Primary Trend:** [Uptrend / Downtrend / Sideways] — [Strong / Moderate / Weak]

[2-3 sentences describing what the price structure looks like — the sequence of highs
and lows, general direction, any signs of trend change or continuation]

---

### Key Levels

**Support:**
- S1: $XXX — [why: prior lows / role reversal / consolidation zone]
- S2: $XXX — [why]

**Resistance:**
- R1: $XXX — [why: prior swing high / untested breakout / round number]
- R2: $XXX — [why]

**Price Location:** Currently [near support / mid-range / near resistance]
→ Risk/reward for longs is [favorable / neutral / unfavorable] at this level

---

### Moving Averages
- **50-MA:** Price [above / below] by ~X% | Slope: [Rising / Flat / Falling]
- **200-MA:** Price [above / below] by ~X% | Slope: [Rising / Flat / Falling]
- **Configuration:** [Bullish stack / Bearish stack / Mixed / Golden Cross / Death Cross]
- **MA Read:** [1 sentence — are MAs confirming the trend or diverging from it?]

---

### Overall Assessment

**Technical Bias:** [Bullish / Bearish / Neutral]
**Conviction:** [High / Medium / Low]
**Key Level:** $XXX — [if price closes above/below this on a weekly basis, the picture changes]

[2-3 sentences honest synthesis of what the chart is showing overall]

---
*⚠️ Lite read — trend, levels, and MAs only.*
*For pattern recognition, volume analysis, and probability-weighted scenarios:*
*Full version → agentofalpha.com*
```

---

## What This Read Won't Tell You

This lite analysis gives you the essential framework — trend direction, where to watch for support and resistance, and whether the long-term moving average structure is constructive.

**What you won't get here:**
- Pattern identification (is that a bull flag, a head & shoulders, a cup and handle?)
- Volume confirmation (is the trend backed by conviction or is it thin?)
- Momentum indicators (RSI, MACD — are we overbought? Is there bullish divergence?)
- Probability-weighted scenarios ("60% chance it breaks out, 30% chance it retests support first")
- Multi-timeframe alignment (weekly trend vs. daily structure vs. monthly picture)
- Measured move targets (how far does the pattern project if it completes?)

The full version is used by swing traders and portfolio managers who need all of those layers before making a sizing decision.

**📊 Want pattern recognition, probability scenarios, and full indicator analysis?**
**Full version → [agentofalpha.com](https://agentofalpha.com)**

---

## Example Queries

- `"What's the trend on NVDA? [attaches chart]"`
- `"Give me key support and resistance on BTC [attaches chart]"`
- `"Quick technical read on SPY weekly [attaches chart]"`
- `"Is TSLA above or below its 200-day MA? [attaches chart]"`
- `"Where's the nearest support if AAPL keeps falling? [attaches chart]"`

---

*This analysis is based on chart data only and is for informational purposes only. Not investment advice. Past patterns do not guarantee future results.*
