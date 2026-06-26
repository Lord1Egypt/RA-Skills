---
name: Risk Manager
version: 1.0.2
description: "Compute portfolio risk metrics including VaR, Sharpe ratio, and Kelly criterion using historical and real-time data from the Finskills API."
author: finskills
metadata:
  openclaw:
    requires:
      env:
        - FINSKILLS_API_KEY
    primaryEnv: FINSKILLS_API_KEY
  homepage: https://github.com/finskills/risk-manager
---

# Risk Manager

Quantify and manage portfolio risk using historical volatility, drawdown analysis,
correlation metrics, position sizing frameworks, and macro risk factors sourced
from the Finskills API. Outputs a structured risk dashboard with actionable
hedging and position sizing recommendations.

---

## Setup

**API Key required** — [Register at https://finskills.net](https://finskills.net) to get your free key.  
Header: `X-API-Key: <your_api_key>`
> **Get your API key**: Register at **https://finskills.net** — free tier available, Pro plan unlocks real-time quotes, history, and financials.

---

## When to Activate This Skill

Activate when the user:
- Provides a portfolio and asks "how risky is this?"
- Wants to size a new position using Kelly Criterion or % risk rules
- Asks about maximum drawdown risk for their portfolio
- Wants Value at Risk (VaR) estimate
- Asks how to hedge a portfolio against a market downturn
- Looks for stop-loss levels or risk budgeting advice

---

## Required Information

1. **Portfolio holdings**: ticker + shares (or weights) for risk assessment
2. **New position sizing question**: ticker, account size, max loss tolerance — for position sizing
3. **Risk framework preference**: Kelly / Fixed % / VaR-based (default: Fixed %)
4. **Time horizon**: Daily / Weekly / Monthly risk measurement

---

## Data Retrieval — Finskills API Calls

### 1. Historical Daily Returns for Risk Calculation
For each portfolio holding:
```
GET https://finskills.net/v1/stocks/history/{SYMBOL}?period=1y&interval=1d
```
Extract: closing prices → compute daily log returns (ln(P_t/P_{t-1}))

### 2. Market Breadth (Systemic Risk Context)
```
GET https://finskills.net/v1/free/market/breadth
```
Extract: advance/decline ratio, % stocks above 200MA, new highs vs new lows → gauge market risk-on/off condition

### 3. Benchmark Performance
```
GET https://finskills.net/v1/stocks/history/SPY?period=1y&interval=1d
```
Extract: SPY daily returns for Beta and correlation calculation

### 4. US Treasury Risk-Free Rate
```
GET https://finskills.net/v1/free/macro/treasury-rates
```
Extract: 3-month and 10-year yield for risk-free rate in Sharpe Ratio calculation

### 5. Short Volume (Individual Stock Risk Signal)
For high-concentration positions:
```
GET https://finskills.net/v1/free/market/short-volume/{SYMBOL}
```
Extract: short volume ratio (short vol / total vol) — high short ratio = elevated downside risk

---

## Analysis Workflow

### Step 1 — Individual Position Risk Metrics

For each holding (using 252 trading days of daily returns):

```
Daily Volatility    = std(daily_returns)
Annual Volatility   = daily_vol × √252
Daily VaR (95%)     = -1.645 × daily_vol × position_value
Daily VaR (99%)     = -2.326 × daily_vol × position_value
Max Drawdown        = max(cummax(prices) - prices) / cummax(prices)
Sharpe Ratio        = (Ann.Return - risk_free_rate) / annual_vol
```

### Step 2 — Portfolio-Level Risk Metrics

```
Portfolio Variance  = Σ_i Σ_j (w_i × w_j × cov(r_i, r_j))
Portfolio Volatility = √(Portfolio Variance) × √252
Portfolio VaR(95%)  = -1.645 × daily_portfolio_vol × total_portfolio_value
Portfolio Beta      = Σ_i (w_i × cov(r_i, r_SPY) / var(r_SPY))
Portfolio Sharpe    = (Portfolio Annual Return - rf) / Portfolio Annual Volatility
```

**Correlation matrix** (simplified for 4 or fewer positions):
- Show pairwise correlations between holdings
- Flag highly correlated pairs (r > 0.75): diversification benefit is reduced

### Step 3 — Risk Classification

Assign each metric to a risk tier:

| Metric | Low Risk | Medium Risk | High Risk |
|--------|---------|------------|---------|
| Portfolio Annual Vol | < 12% | 12–25% | > 25% |
| Portfolio Beta | < 0.8 | 0.8–1.3 | > 1.3 |
| Max Drawdown | < 15% | 15–30% | > 30% |
| Largest Position | < 15% | 15–25% | > 25% |
| VaR (95%, 1D) | < 1% | 1–2% | > 2% |

### Step 4 — Position Sizing Recommendations

**For a new trade, calculate using Fixed Fractional method (default):**
```
Max Risk Per Trade:  user-specified % of account (common: 1–2%)
Stop Loss Distance:  entry_price - stop_price
Position Size:       (Account × Risk%) / Stop Loss Distance
Max Shares:          min(Position Size, account × 20%)  [never > 20% allocation]
```

**Kelly Criterion (advanced, use when win_rate and win/loss ratio are known):**
```
Kelly %  = win_rate - (1 - win_rate) / (avg_win / avg_loss)
F*       = Kelly % × 0.5  [half-Kelly for safety]
Position = F* × account_value / entry_price
```

**Rule of thumb safety caps:**
- Single stock: Max 20% of portfolio
- Single sector: Max 35% of portfolio
- High-beta stocks (β > 1.5): Reduce position by 20–30%

### Step 5 — Hedging Strategies

Based on portfolio Beta and market risk context (market breadth data):

| Portfolio Beta | Market Condition | Hedge Recommendation |
|---------------|-----------------|---------------------|
| > 1.3 | Market breadth weakening | Buy SPY puts (5–10% notional hedge) |
| > 1.3 | Normal market | Consider collar or reduce position in top beta names |
| 0.8–1.3 | Market breadth weakening | Add 5% cash or defensive rotation |
| < 0.8 | Any | Portfolio already defensive; monitor for opportunity |

**Common hedge instruments:**
- SPY puts (broad market hedge)
- QQQ puts (tech-heavy portfolio hedge)
- VXX or UVXY (volatility spike hedge — only for short-term, decay is severe)
- TLT (flight-to-quality hedge in recession scenarios)
- GLD (inflation/tail risk hedge)

---

## Output Format

```
╔══════════════════════════════════════════════════════╗
║      PORTFOLIO RISK DASHBOARD  —  {DATE}            ║
╚══════════════════════════════════════════════════════╝

📊 PORTFOLIO RISK SUMMARY
  Annual Volatility:  {%}    Risk Level: {Low/Medium/High}
  Portfolio Beta:     {x}    vs. S&P 500
  Sharpe Ratio:       {x}    ({Good/Adequate/Poor} risk-adjusted return)
  Max Drawdown (1Y):  -{%}
  VaR (95%, 1-Day):   -${amount} ({%} of portfolio)

📋 POSITION RISK BREAKDOWN
  Ticker  Weight  Ann.Vol  Beta  VaR(1D,95%)  MaxDD(1Y)
  AAPL    18.4%   22.1%    1.12  -$852        -28.3%
  MSFT    24.2%   19.8%    0.98  -$1,104      -24.1%
  ...

🔗 CORRELATION MATRIX
  [Pairwise correlations between holdings]
  High correlation pairs: {Ticker A & Ticker B: r={value}} ⚠️

⚠️ RISK FLAGS
  🚨 {Ticker} is {%} of portfolio — exceeds 20% concentration threshold
  ⚠️  {Sector} exposure at {%} — elevated sector risk
  ⚠️  Portfolio beta {x} — above 1.2 threshold in current market

📐 POSITION SIZING GUIDE (for new positions)
  Account Size:    ${value}
  Risk Per Trade:  {%} = ${dollar_amount}
  Example Entry:   {TICKER} at ${price}, Stop at ${stop}
  Suggested Size:  {shares} shares (${value} = {%} of account)

🛡️ HEDGING RECOMMENDATIONS
  Current Portfolio Beta: {x}
  Market Breadth Status:  {Risk-On / Neutral / Risk-Off}
  Recommendation:         {hedge action or "No hedge needed"}
  
  If hedging: {specific instrument, quantity, rationale}

📰 MARKET RISK CONTEXT
  Advance/Decline Ratio: {x}
  % Stocks > 200MA:      {%}
  Short Interest Signal:  {Low/Elevated for key positions}
```

---

## Limitations

- Historical volatility and correlation are backward-looking; future risk may differ.
- VaR assumes normally distributed returns; tail events (crashes) are underestimated.
- Correlation estimates become less reliable with fewer than 60 data points.
- This skill does not account for leverage, margin calls, or options gamma risk.
