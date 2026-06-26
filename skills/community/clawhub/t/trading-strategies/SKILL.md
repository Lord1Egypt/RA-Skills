---
name: trading
description: Comprehensive trading knowledge base covering fundamentals, technicals, strategies, backtesting, and risk management. Use when building trading apps or evaluating strategies.
---

# Trading Skill — Complete Reference

## Purpose
Comprehensive trading knowledge base covering fundamentals, technicals, strategies, backtesting, and risk management. Use when building trading apps, evaluating strategies, or making trading decisions.

---

## 1. TRADING STYLES

### Scalping
- Hold: seconds to minutes
- Goal: profit from tiny price movements
- Pros: many opportunities, reduced exposure to big moves
- Cons: high transaction costs, stressful, tiny profit per trade
- Best for: highly liquid markets with tight spreads

### Day Trading
- Hold: minutes to hours (close all by market close)
- Goal: profit from intraday price movements
- Pros: no overnight risk, high profit potential per trade
- Cons: high risk, emotional pressure, costs add up
- Best for: volatile stocks with clear intraday patterns

### Swing Trading
- Hold: days to months
- Goal: catch short-to-intermediate moves
- Pros: lower costs, more analysis time, less stressful
- Cons: overnight risk, may miss long-term moves
- Best for: trending markets with pullbacks

### Position Trading
- Hold: months to years
- Goal: profit from major long-term trends
- Pros: lowest costs, highest profit potential, most flexibility
- Cons: capital tied up, exposed to macro events
- Best for: fundamentally strong companies in sector uptrends

---

## 2. FUNDAMENTAL ANALYSIS

### Key Metrics

**P/E Ratio (Price-to-Earnings)**
- Formula: `Share Price / Earnings Per Share`
- S&P 500 average: ~30 (as of late 2025)
- Low (<15): potentially undervalued or troubled
- High (>30): potentially overvalued or high growth expected
- Compare WITHIN same industry only
- Forward P/E uses projected earnings; Trailing P/E uses last 12 months

**P/B Ratio (Price-to-Book)**
- Formula: `Share Price / Book Value Per Share`
- Book Value = total assets - intangible assets - liabilities
- P/B < 1 = trading below asset value (potential bargain)
- Most useful for capital-heavy industries (banks, manufacturing)

**Debt-to-Equity Ratio**
- Formula: `Total Liabilities / Shareholders' Equity`
- High = heavy debt reliance (risky in downturns)
- Compare within industry — some sectors carry more debt naturally

**Revenue Growth Rate**
- Year-over-year revenue increase
- Consistent > spiky
- Accelerating growth rate = strongest signal

**Free Cash Flow (FCF)**
- Cash generated after capital expenditures
- Positive FCF = real cash generation, not accounting tricks
- FCF Yield = FCF / Market Cap (higher = better value)

**EPS Growth (Earnings Per Share)**
- Consistent EPS growth over 3-5 years = strong signal
- Check quality: operations vs one-time events

**Return on Equity (ROE)**
- Formula: `Net Income / Shareholders' Equity`
- ROE > 15% = generally good management efficiency

**Dividend Yield & Payout Ratio**
- Yield = Annual Dividend / Share Price
- Payout = Dividends / Net Income
- Payout > 80% may be unsustainable

---

## 3. TECHNICAL INDICATORS

### RSI (Relative Strength Index)
- **Formula:** `RSI = 100 - (100 / (1 + (Avg Gain / Avg Loss)))` over 14 periods
- Scale: 0-100
- **>70 = Overbought** (potential sell)
- **<30 = Oversold** (potential buy)
- **Strengths:** Simple, effective in ranging markets
- **Weaknesses:** Stays >70 for extended periods in strong uptrends — don't auto-sell
- **RSI Divergence:** Price makes new high but RSI makes lower high = bearish (momentum weakening)
- **Swing Rejection:** RSI crosses 30 upward → dips but stays above 30 → breaks prior high = bullish entry
- **Best in:** Ranging/sideways markets. Combine with ADX to filter.

### MACD (Moving Average Convergence Divergence)
- **MACD Line** = 12-period EMA - 26-period EMA
- **Signal Line** = 9-period EMA of MACD Line
- **Histogram** = MACD Line - Signal Line
- **Buy:** MACD crosses ABOVE signal line
- **Sell:** MACD crosses BELOW signal line
- **Divergence:** MACD rising while price falling = potential reversal
- **Strengths:** Good trend-following indicator
- **Weaknesses:** Lagging, many false positives in sideways markets
- **Best combined with ADX** — only trust MACD signals when ADX > 25 (confirming trend)

### Bollinger Bands
- **Middle Band** = 20-day SMA
- **Upper Band** = SMA + 2 standard deviations
- **Lower Band** = SMA - 2 standard deviations
- 95% of price action stays within bands
- **Squeeze:** Bands narrow → low volatility → breakout imminent (direction unknown)
- **Bollinger Bounce:** Price off lower band toward middle = buy; off upper toward middle = sell
- **Breakout:** Price outside bands with volume = trend continuation
- **Strengths:** Visual, adapts to volatility
- **Weaknesses:** Secondary indicator — always confirm with RSI/MACD
- Created by John Bollinger in the 1980s

### Moving Averages
- **SMA (Simple):** Equal weight all periods
- **EMA (Exponential):** More weight on recent prices (faster reaction)
- Key periods: 5, 9, 20, 50, 100, 200 day
- **Golden Cross:** 50-day crosses ABOVE 200-day = strong bullish
- **Death Cross:** 50-day crosses BELOW 200-day = strong bearish
- MAs act as dynamic support/resistance levels
- Use longer MAs for volatile stocks to avoid false signals

### Volume
- Confirms price movements
- Price up + high volume = strong bullish
- Price up + low volume = weak rally, likely to reverse
- Price down + high volume = strong selling pressure
- Price down + low volume = lack of selling conviction
- 60-80% of daily volume is algorithmic

### Ichimoku Cloud (Ichimoku Kinko Hyo)
- **5 Components:**
  - Tenkan-sen (Conversion Line): (9-period high + 9-period low) / 2
  - Kijun-sen (Base Line): (26-period high + 26-period low) / 2
  - Senkou Span A: (Tenkan + Kijun) / 2, plotted 26 periods ahead
  - Senkou Span B: (52-period high + 52-period low) / 2, plotted 26 periods ahead
  - Chikou Span: Current close plotted 26 periods back
- **The Cloud (Kumo):** Area between Span A and Span B = support/resistance zone
- **Buy:** Price above cloud, Tenkan crosses above Kijun
- **Sell:** Price below cloud, Tenkan crosses below Kijun
- **Strengths:** All-in-one indicator (trend, momentum, support/resistance)
- **Weaknesses:** Complex visually, lagging in fast markets
- **Best in:** Trending markets. Avoid in ranging/sideways.
- Michael Automates created an AI-improved Ichimoku strategy that performs well

### Super Trend
- **Formula:** Based on ATR (Average True Range) and a multiplier
- Upper Band = (High + Low) / 2 + (Multiplier × ATR)
- Lower Band = (High + Low) / 2 - (Multiplier × ATR)
- **Buy:** Price crosses above Super Trend line
- **Sell:** Price crosses below Super Trend line
- **Strengths:** Simple, good trend-following, clear signals
- **Weaknesses:** Late entries, bad in ranging markets
- AI iteration took Super Trend from 44% to 3,605% P&L in Michael Automates' testing

### VWAP (Volume-Weighted Average Price)
- **Formula:** `Sum(Price × Volume) / Total Volume` (intraday only)
- Above VWAP = bullish intraday
- Below VWAP = bearish intraday
- Institutional benchmark — they buy below VWAP, sell above
- Resets daily — intraday tool only

---

## 4. SIGNAL COMBINATIONS

### Strong Buy Signal (High Confidence)
All of these together:
- RSI < 30 (oversold) AND recovering
- MACD crossing above signal line
- Price bouncing off lower Bollinger Band
- Volume increasing on the bounce
- Price above 200-day MA (long-term uptrend intact)
- Fundamentals solid (P/E reasonable, FCF positive, revenue growing)

### Moderate Buy Signal
- RSI between 40-50 in an uptrend (pullback buy)
- Price touching 50-day MA support
- MACD histogram turning positive
- Volume above average

### Trend-Following Entry
- Golden Cross (50-day crosses above 200-day)
- Price breaks above resistance with high volume
- ADX > 25 confirming trend strength
- Buy on first pullback after breakout

### Strong Sell Signal
- RSI > 70 in a ranging market
- Price hitting upper Bollinger Band with declining volume
- MACD crossing below signal line
- Price reaching prior resistance level

**RULE: Never rely on a single indicator. Always combine 2-3 minimum.**

---

## 5. POSITION SIZING

### The 1% Rule
Never risk more than 1% of total account on a single trade.
- Account: $1,000 → max risk per trade: $10
- If stop-loss is $2 below entry → buy 5 shares max
- Keeps you alive through losing streaks

### Kelly Criterion
- `f = (bp - q) / b`
- b = win/loss ratio, p = win probability, q = loss probability
- Gives optimal position size based on historical win rate
- **Use half-Kelly** for safety (most professionals do)

### Example
- Win rate: 55%, average win: $200, average loss: $100
- Kelly: f = (2 × 0.55 - 0.45) / 2 = 0.325 (32.5% of account)
- Half-Kelly: 16.25% — still aggressive, many pros use quarter-Kelly

---

## 6. EXIT STRATEGIES

### Stop-Loss Types
- **Fixed percentage:** Sell if price drops X% (typically 5-8%)
- **ATR-based:** Stop at entry minus 2× Average True Range (adjusts for volatility)
- **Support-based:** Stop below key support level or moving average
- **Trailing stop:** Moves up with price, locks in profits (e.g., trail by 5%)

### Take-Profit Methods
- **Fixed target:** Pre-set price target (e.g., 2:1 or 3:1 risk/reward)
- **Technical target:** Previous resistance level, Fibonacci extension
- **Trailing:** Let winners run with trailing stop

### The 3 Hardest Sells
1. **Cutting losses** — "it'll come back" kills accounts. Honor your stops.
2. **Taking profits too early** — use trailing stops to let winners run
3. **Holding through earnings** — volatility spikes. Reduce position or hedge.

---

## 7. STRATEGY ARCHETYPES

### Mean Reversion
- **Theory:** Prices revert to their historical average over time
- **Entry:** Buy when RSI < 30 or price 2+ standard deviations below mean
- **Exit:** Sell when RSI > 70 or price returns to mean
- **Tools:** Z-scores, Bollinger Bands, RSI
- **Best in:** Range-bound/sideways markets
- **Weakness:** Fails badly in strong trending markets (price keeps going)
- **Key stat:** Z-score above 1.5 or below -1.5 signals opportunity

### Momentum
- **Theory:** Stocks that are going up tend to keep going up (and vice versa)
- **Entry:** Buy stocks with strongest 3-6 month performance
- **Exit:** Sell when momentum weakens (MACD crossover, RSI divergence)
- **Philosophy:** "Buy high, sell higher" — opposite of value investing
- **Best in:** Trending markets with clear direction
- **Weakness:** Sudden reversals can be devastating
- **Key tools:** Trend lines, MACD, RSI, relative strength vs index

### Moving Average Crossover
- **Entry:** Buy on Golden Cross (50-day crosses above 200-day)
- **Exit:** Sell on Death Cross (50-day crosses below 200-day)
- **Pros:** Simple, catches major trends
- **Cons:** Very lagging — you'll miss the first 10-20% of a move and give back 10-20% at the end
- **Variant:** Use shorter MAs (9/21) for faster signals but more noise

### Bollinger Band Squeeze
- **Entry:** When bands contract to minimum width, enter on the breakout direction with volume confirmation
- **Exit:** When price reaches opposite band or bands start contracting again
- **Key:** The squeeze only tells you a big move is coming — NOT the direction
- **Must combine with:** Volume, MACD, or other directional indicator

### Pairs Trading
- **Origin:** Morgan Stanley, mid-1980s
- **How:** Find two highly correlated stocks (0.80+ correlation). When they diverge, go long the underperformer, short the outperformer
- **Profit:** When they converge back to historical correlation
- **Market-neutral:** Hedged against broad market moves
- **Risk:** Correlation can break permanently (one company's fundamentals change)
- **Example:** Coca-Cola vs Pepsi, Visa vs Mastercard

### VWAP Reversion (Intraday)
- **Entry:** Buy below VWAP when overall trend is bullish
- **Exit:** Sell above VWAP or at end of day
- **Best for:** Day trading liquid stocks
- **Why it works:** Institutional traders use VWAP as a benchmark

---

## 8. BACKTESTING

### The 4 Deadly Biases
1. **Optimization Bias (Curve Fitting):** Over-tuning to historical data. Fix: minimal parameters, out-of-sample testing
2. **Look-Ahead Bias:** Using future data accidentally. Fix: strict chronological processing
3. **Survivorship Bias:** Only testing stocks that exist today. Fix: survivorship-free datasets or recent data
4. **Psychological Tolerance Bias:** A 25% drawdown looks fine on a chart but feels devastating in real-time

### Key Metrics
| Metric | Formula | Good | Great |
|--------|---------|------|-------|
| Sharpe Ratio | (Return - Risk-Free) / Std Dev | >1 | >2 |
| Max Drawdown | Worst peak-to-trough | <20% | <10% |
| Win Rate | Wins / Total Trades | >40% | >55% |
| Profit Factor | Gross Profits / Gross Losses | >1.5 | >2 |
| Risk/Reward | Avg Win / Avg Loss | >2:1 | >3:1 |

**Expected Return per Trade:** `(Win% × Avg Win) + (Loss% × Avg Loss)` — must be positive

### Drawdown Math (Critical)
- 10% loss → need 11% gain to recover
- 20% loss → need 25% gain to recover
- 30% loss → need 43% gain to recover
- 50% loss → need 100% gain to recover
- **The math gets exponentially worse.** Avoiding big losses > chasing big wins.

### Process
1. Define strategy rules with zero ambiguity
2. Get clean OHLCV data (Open, High, Low, Close, Volume)
3. Build engine (Python: backtrader, vectorbt, quantstats)
4. Split: 70% training / 30% out-of-sample validation
5. Run Monte Carlo simulation (randomize trade order) for robustness
6. Paper trade winners for 3+ months
7. Go live small — start with minimum position sizes

### Michael Automates Backtesting Workflow (Proven)
His backtesting engine ($99) does this — we can replicate for free:
1. **Get historical OHLCV data** (from CCXT/Binance/Alpaca — free)
2. **AI creates Python version** of your trading strategy
3. **Run backtest locally** → get metrics
4. **Compare with TradingView numbers** to verify accuracy
5. **If numbers don't match:** Export TradingView Excel report, do trade-by-trade comparison
6. **AI can auto-fix discrepancies** by modifying the backtest engine code
7. **Critical settings:** Commission = 0.1%, timezone = UTC, date range = not full history

**Auto-download data:**
- CCXT pulls from Binance, Coinbase, Kraken automatically
- Store in `/data/cache/` folder by asset and timeframe
- Format: `BTC_USDT_1d.csv`, `ETH_USDT_4h.csv`, etc.

### Data Sources
- **Free:** Yahoo Finance (yfinance), Alpha Vantage, Alpaca, Polygon.io free tier, CCXT (100+ crypto exchanges)
- **Paid:** Norgate, Nasdaq Data Link (Quandl)
- **Warning:** Yahoo Finance has survivorship bias
- **Best for crypto:** CCXT + Binance (most history, most pairs)
- **Best for stocks:** Alpaca (free, clean data, built-in paper trading)

---

## 9. RISK MANAGEMENT

### Core Rules
- **1% Rule:** Never risk more than 1% of account per trade
- **Daily Loss Limit:** Stop trading if down 3% in a day
- **Correlation Risk:** Don't hold 5 tech stocks — one sector crash kills you
- **Position Limits:** Max 5-10 open positions at once
- **Cash Reserve:** Always keep 20-30% cash for opportunities

### Circuit Breakers
- Hit daily loss limit → done for the day
- Hit weekly loss limit (5%) → reduce position sizes 50%
- Hit monthly loss limit (10%) → pause, review all strategies
- 3 consecutive losses → take a break, re-evaluate

### Fees & Slippage (Often Ignored)
- Commission-free doesn't mean cost-free — there's still the spread
- Slippage: the difference between expected and actual execution price
- High-frequency strategies amplify these costs
- **Always include fees + slippage in backtests** or results are meaningless

---

## 10. COMMON MISTAKES

1. **Trading without a plan** → Write rules BEFORE trading
2. **Ignoring position sizing** → The 1% rule exists for a reason
3. **Moving stop-losses** → Set them and honor them
4. **Averaging down** → Adding to losers hoping they'll recover
5. **Overtrading** → More trades ≠ more profit (costs eat you alive)
6. **Single indicator reliance** → Always combine 2-3 indicators
7. **Not accounting for fees** → Especially in backtests
8. **Skipping paper trading** → Going live without 3+ months of validation
9. **Revenge trading** → Trying to win back losses with bigger bets
10. **Ignoring the macro** → Individual stocks don't exist in a vacuum

---

## 11. TOOLS & APIS

### Broker APIs
- **Alpaca** — Commission-free, great API, paper trading built in (RECOMMENDED for us)
- **Interactive Brokers** — Most comprehensive, supports everything
- **TD Ameritrade/Schwab** — thinkorswim API

### Data APIs
- **Alpha Vantage** — Free tier (5 calls/min), stocks + crypto + forex
- **Polygon.io** — Real-time and historical, free tier
- **Yahoo Finance** — Free via yfinance (unreliable, survivorship bias)
- **Alpaca Market Data** — Included with account

### Python Stack
- **pandas** — Data manipulation
- **numpy** — Numerical computing
- **ta-lib / pandas-ta** — Technical indicators
- **backtrader** — Full backtesting framework
- **vectorbt** — Fast vectorized backtesting
- **quantstats** — Portfolio analytics
- **scikit-learn** — ML pattern recognition
- **alpaca-trade-api** — Broker integration

### Architecture
```
[Data Feed] → [Indicator Engine] → [Signal Generator] → [Risk Manager] → [Order Executor]
     ↑                                                           |
     └──────────── [Backtesting Engine] ←────────────────────────┘
                          ↓
                   [Performance Analytics]
```

---

## 12. CRYPTO-SPECIFIC STRATEGIES (From Video Research)

### Super Trend Strategy
- Built-in TradingView indicator
- AI can iterate: base version (44% P&L) → optimized V4 (3,605% P&L)
- Process: give AI base → "improve it" → backtest → repeat overnight
- Test on multiple assets to avoid overfitting

### Strategy Tournament (Evolution Method)
- Create 10 different strategies with different parameters/logic
- Run all 10 in parallel with small positions ($100 each)
- After 1-2 weeks: cut losers, keep winners
- Create variations of winners, repeat process
- Natural selection for trading strategies

### Market Regime Detection
- Run separate strategies for trending vs ranging markets
- AI detects current regime and switches strategies automatically
- Trend-following for trending markets, mean reversion for ranging

### Prediction Market Strategies (Polymarket)
- **15-Minute Windows:** BTC up/down resolution every 15 minutes
- **Late Entry:** Look at trend in last 3-4 minutes, enter in that direction
- **Arbitrage:** When both sides cost <$1 total = guaranteed profit
- **Mention Markets:** AI studies speech patterns to predict word usage
- **Sports Scanner:** AI researches obscure low-volume markets for edges
- **Counter-Trend AI:** Bet against AI consensus (contrarian)
- **Wallet Analysis:** Copy successful wallets → AI reverse-engineers their strategy
- KEY: Not dependent on bull/bear markets — works always

### Multi-Agent Trading Architecture
- **Coordinator:** Delegates tasks, manages priorities, daily briefing
- **Quant Scanner:** Scans 30+ coins every 15 min with CCXT, confluence scoring
- **Researcher:** Daily news/intel scanning, deep dives
- **Alert Agent:** Formats and delivers signals
- **Security Agent:** 24hr audit for malicious code, prompt injections, bugs
- Each agent needs a detailed "soul" (personality + instructions)
- Agents work in parallel, not sequentially

### Crypto Exchange APIs
- **Hyperliquid** — Decentralized perps, no KYC, good API
- **Blofin** — Centralized, API with trading perms (disable withdrawals!)
- **CCXT Library** — Open-source, supports 100+ exchanges, start read-only
- **Alpaca** — Stocks (commission-free, paper trading built in)

### AI Strategy Iteration Workflow (KEY — From Michael Automates)
This is the single most powerful workflow from all our research:
1. **Pick a base strategy** (e.g., Super Trend, RSI+MACD, Bollinger Squeeze)
2. **AI backtests it** → gets baseline metrics (P&L, drawdown, win rate, Sharpe)
3. **Tell AI "improve this"** → it modifies parameters, adds filters, changes logic
4. **AI creates V2, V3, V4...** each iteration potentially better
5. **Compare AI numbers with TradingView** to verify accuracy
6. **LET IT RUN OVERNIGHT** — wake up to results
7. **Score across multiple assets** (BTC, ETH, SOL, SPY, AAPL) to avoid overfitting
8. **Only keep strategies that work on 3+ different assets**
9. Repeat until you have top 3 strategies → paper trade those

**Michael's results:** Super Trend went from 44% P&L → 3,605% P&L through this process.

**Critical anti-overfitting rules:**
- Test on multiple assets, not just one
- Use walk-forward validation (train on years 1-3, test on years 4-5)
- If a strategy only works on one asset, it's overfit — discard it
- Commission must be set to 0.1% (not 0%)
- TradingView timezone must be UTC for number matching

### Strategy Tournament (From Alex Carter)
1. Create 10 different strategies (vary parameters, timeframes, indicators)
2. Run ALL 10 in parallel with small positions ($100 each)
3. Track for 1-2 weeks
4. Kill bottom 5 performers
5. Create mutations/variations of top 5
6. Run new tournament
7. Repeat — "evolution for trading strategies"
8. After 3-4 rounds, surviving strategies are battle-tested

### Counter-Trend Against AI Crowd (From Coin Bureau)
- Most AI trading bots use similar data and strategies
- When AI crowd consensus is heavy one direction, bet the opposite
- Works because: AI herding creates overcrowded trades that reverse
- Requires: monitoring what popular AI strategies are doing
- Best for: short-term contrarian plays in crypto and prediction markets

### Divergence Trading (From Coin Bureau)
- Use TBT Divergence indicator on 15-minute timeframe
- Contrarian entry when price makes new high/low but indicator doesn't confirm
- Specifically: price up but RSI/MACD diverging = weakening momentum
- Enter against the trend on confirmed divergence
- Best for: short-term crypto and Polymarket 15-min windows

### Critical Crypto Trading Rules
- NEVER enable withdrawal permissions on API keys
- Whitelist your IP on centralized exchanges
- Store keys in .env files, never hardcoded
- Use testnet/paper trading first
- Rotate API keys every few months
- Run on dedicated machine (not personal computer)
- Daily security audit via cron job

---

## 13. POLYMARKET (PREDICTION MARKETS)

### How It Works
- Binary markets: buy Yes/No shares in real-world outcomes
- Correct = $1.00 payout, wrong = $0.00
- Price = probability (Yes at $0.70 = market thinks 70% likely)
- Runs on Polygon (Ethereum L2), uses USDC.e
- Python SDK: `py-clob-client`
- Public data API (no auth): `gamma-api.polymarket.com`

### Strategy Types
1. **Arbitrage** — Yes + No < $1.00 = free money (rare, need speed)
2. **Late Entry** — 15-min BTC windows, enter last 3-4 min when trend is clear
3. **Mention Markets** — AI analyzes speech patterns to predict word usage
4. **Obscure Sports** — Low-volume markets with inefficient pricing
5. **Wallet Analysis** — Reverse-engineer top performers' strategies
6. **Market Making** — Provide liquidity, profit from spread (advanced)

### Why AI Has an Edge
- Can process more data than any human (speeches, news, stats)
- 24/7 monitoring of all markets simultaneously
- Niche markets have little competition = more mispricing
- Uncorrelated to stock/crypto markets — works in any cycle

### Market Making (Advanced)
- Place both buy and sell orders, profit from the spread
- Requires: understanding inventory risk, dynamic spread adjustment
- Need algorithm to adjust quotes based on position, volatility, flow
- Complex math but AI handles research and implementation
- Start with wide spreads in low-volume markets, tighten as you learn
- Risk: getting stuck holding losing positions if market moves fast

### TBO Cloud Strategy (Coin Bureau — Proprietary)
- Trending Breakout indicator on 4-hour timeframe
- Advanced moving average strategy — details not public
- Combined with TBT Divergence indicator for entry/exit
- We can build similar: EMA cloud (9/21/55 EMAs) with breakout confirmation
- Key concept: cloud acts as dynamic support/resistance, breakout above = long

### Key Insight
Build scanner first (read-only, free). Paper trade. Then go live small.

---

## 14. CRYPTO vs STOCK STRATEGIES — WHAT TRANSFERS

### Strategies That Work in BOTH Markets
| Strategy | Stocks | Crypto | Notes |
|----------|--------|--------|-------|
| Trend Following | ✅ | ✅ | Works in any market with trends |
| Mean Reversion | ✅ | ✅ | Better in stocks (more mean-reverting) |
| RSI/MACD Signals | ✅ | ✅ | Same indicators, different parameters |
| Bollinger Bands | ✅ | ✅ | Adjust for volatility differences |
| Pairs Trading | ✅ | ✅ | Stocks: KO/PEP. Crypto: BTC/ETH |
| Moving Average Crossover | ✅ | ✅ | Universal trend indicator |
| Ichimoku Cloud | ✅ | ✅ | Works anywhere with enough volume |
| Strategy Tournament | ✅ | ✅ | Run 10 strategies, evolve winners |
| AI Iteration | ✅ | ✅ | Give AI base strategy, let it improve |

### Key Differences
| Factor | Stocks | Crypto |
|--------|--------|--------|
| Hours | 9:30 AM - 4 PM ET | 24/7/365 |
| Volatility | Lower (1-3% daily avg) | Higher (5-10%+ daily avg) |
| Leverage | 2x (margin), options for more | 10-100x available |
| Regulation | Heavy (SEC, FINRA) | Light (evolving) |
| Data Quality | Excellent (decades) | Good (5-10 years) |
| Fees | Commission-free (Alpaca) | 0.1% typical |
| Short Selling | Restricted (uptick rule) | Easy (perps) |
| Pattern Day Trading | $25K minimum (PDT rule) | No restriction |
| Market Manipulation | Illegal, enforced | Common, less enforcement |

### What Needs Adjusting for Stocks
- **Wider MA periods** — crypto is faster, use longer MAs for stocks to filter noise
- **Lower leverage** — 2x max for stocks vs 5-10x crypto
- **Market hours** — need pre/after-hours data handling, overnight gaps
- **PDT Rule** — if under $25K, limited to 3 day trades per 5 business days
- **Earnings events** — stocks have scheduled volatility events quarterly
- **Sector correlation** — stocks in same sector move together more than crypto
- **Volume patterns** — stocks have predictable volume curves (open, close spikes)

### Bottom Line
**Yes, the core strategies transfer to stocks.** The math is the same. What changes:
1. Parameters (slower timeframes for stocks)
2. Risk settings (lower leverage, wider stops)
3. Schedule (market hours vs 24/7)
4. Starting capital ($25K for day trading stocks due to PDT rule, or use swing trading to avoid it)

**Best starting point for stocks:** Alpaca (free, commission-free, paper trading built in, great API). Same strategies, just tune the parameters.

---

## 15. MULTI-AGENT TRADING DESK (From Coin Bureau)

### Architecture
Each agent gets a detailed "soul" (personality + priorities + instructions). Without a soul, agents produce generic output.

### Agent Roles
1. **Coordinator (Betty)** — Manager agent. Delegates tasks, manages priorities, monitors agent health, delivers daily briefing. Never does the work itself.

2. **Quant Scanner** — Scans 30+ coins every 15 minutes via cron job. Uses CCXT for OHLCV data. Runs indicators (RSI, MACD, Bollinger, etc). Produces confluence score for each signal. Rules: never places trades without operator approval.

3. **Researcher** — Runs daily. Scans news, X/Twitter, market updates. Produces morning research brief. Focused on narratives, sectors, new listings.

4. **Alert Agent** — Formats signals from quant scanner into actionable alerts. Pushes to Discord channels. Includes: asset, timeframe, direction, confidence score, entry/exit suggestions.

5. **Security Agent (Radar)** — 24hr security audit. Checks for malicious code, prompt injections, bugs. Quality assurance on all strategy code before deployment. Non-negotiable.

6. **Backtesting Agent** — Validates strategies against historical data before deployment.

7. **Trading Agent** — Executes trades on exchange APIs. Only activated after paper trading period.

### Notification Pipeline (Discord Recommended)
- Private Discord server with bot admin privileges
- Bot creates channels per category (signals, research, alerts, P&L)
- Curated alerts — only coins/markets you care about
- Much better than Telegram (categories, threads, searchable)

### Key Insight From Coin Bureau
"Your output is only as good as your input." Generic prompts = generic agents. Spend time writing detailed soul descriptions for each agent. Include:
- Exact responsibilities
- What data to use
- What format to output
- What rules to follow
- What to never do

### Cost Reality
- Claude Max ($200/mo) — unlimited for heavy agent usage
- API credits alternative: $1,000-10,000/mo depending on volume
- Ollama (free) — can run specific tasks locally but less smart
- Strategy: use Claude for complex work, Ollama for routine scans

---

## 16. OUR APPROACH

### Phase 1: Foundation
- Set up Alpaca paper trading (free)
- Build data pipeline for historical OHLCV data
- Implement core indicators: RSI, MACD, Bollinger, MAs, Volume
- Build backtesting engine with walk-forward validation

### Phase 2: Strategy Development
- Backtest all 6 strategy archetypes against 5-10 years of data
- Find highest Sharpe ratio + lowest max drawdown combo
- Monte Carlo simulations for robustness
- Paper trade top 2-3 strategies simultaneously

### Phase 3: Live (After 3+ Months Paper)
- Minimum position sizes
- AI-driven condition analysis (use Claude to interpret market context)
- Full risk management: 1% rule, daily limits, circuit breakers
- Dashboard monitoring all positions, signals, performance

### Key Principles
1. Paper trade until proven over 3+ months
2. Position sizing > entry signals
3. Risk management is the ONLY thing that keeps you in the game
4. No single indicator is reliable alone
5. Past performance ≠ future results
6. Start with stocks, not crypto (more data, less manipulation)
7. Account for fees, slippage, and taxes ALWAYS
