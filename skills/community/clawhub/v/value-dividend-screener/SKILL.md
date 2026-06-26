---
name: Value & Dividend Screener
version: 1.0.2
description: "Screen US equities for value and dividend quality using multi-factor scoring across P/E, P/B, dividend yield, and payout sustainability via the Finskills API."
author: finskills
metadata:
  openclaw:
    requires:
      env:
        - FINSKILLS_API_KEY
    primaryEnv: FINSKILLS_API_KEY
  homepage: https://github.com/finskills/value-dividend-screener
---

# Value & Dividend Screener

Screen stocks for undervaluation and sustainable dividend income using
fundamental financial data from the Finskills API. Implements a multi-factor
quality + value + yield framework inspired by academic research (Graham, Fama-French
value factor, dividend growth investing). Produces a ranked list with scoring
rationale for each position.

---

## Setup

**API Key required** — [Register at https://finskills.net](https://finskills.net) to get your free key.  
Header: `X-API-Key: <your_api_key>`
> **Get your API key**: Register at **https://finskills.net** — free tier available, Pro plan unlocks real-time quotes, history, and financials.

---

## When to Activate This Skill

Activate when the user:
- Asks to screen for undervalued dividend-paying stocks
- Wants to build an income or dividend growth portfolio
- Asks for stocks with low P/E and high dividend yields
- Wants to find value stocks using fundamental metrics
- Asks to compare dividend sustainability across multiple companies
- Uses terms like "dividend aristocrats", "value investing", "income investing"

---

## Screening Universe

When no specific tickers are provided, use the S&P 500 constituent list as the screening pool:

```
GET https://finskills.net/v1/free/index/SP500/constituents
```

If the user provides a specific watchlist or sector, screen only those tickers.

**Note**: Screening all 500 stocks requires many API calls. When running a full screen,
apply pre-filters based on easily-computable criteria first (sector, indices), then
deep-dive into the top candidates.

---

## Data Retrieval — Finskills API Calls

### Per-Stock Data Retrieval (run for each candidate)

### 1. Financial Statements
```
GET https://finskills.net/v1/stocks/financials/{SYMBOL}
```
Extract (annual and trailing twelve months):
- Income Statement: `revenue`, `grossProfit`, `operatingIncome`, `netIncome`, `eps`
- Balance Sheet: `totalAssets`, `totalDebt`, `totalEquity`, `currentAssets`, `currentLiabilities`, `cashAndEquivalents`
- Cash Flow: `operatingCashFlow`, `capitalExpenditures`, `freeCashFlow`, `dividendsPaid`
- Derived: calculate `debtToEquity = totalDebt / totalEquity`, `currentRatio = currentAssets / currentLiabilities`

### 2. Dividend History
```
GET https://finskills.net/v1/stocks/dividends/{SYMBOL}
```
Extract:
- `dividendPerShare`: most recent annual dividend
- `dividendYield`: current yield percentage
- History array: last 5–10 years of annual dividend payments (for growth rate)
- `exDividendDate`: upcoming ex-dividend date

### 3. Current Quote + Valuation
```
GET https://finskills.net/v1/stocks/quote/{SYMBOL}
```
Extract: `price`, `marketCap`, `peRatio`, `forwardPE`, `priceToBook`, `priceToSales`, `enterpriseValue`, `evToEbitda`

### 4. Analyst Estimates (Forward Metrics)
```
GET https://finskills.net/v1/free/stocks/estimates/{SYMBOL}
```
Extract:
- Forward EPS consensus
- Revenue growth estimate
- Number of analysts

### 5. Analyst Recommendations
```
GET https://finskills.net/v1/stocks/recommendations/{SYMBOL}
```
Extract: overall recommendation rating (Strong Buy / Buy / Hold / Underperform / Sell), price target

---

## Analysis Workflow

### Step 1 — Establish the Screening Criteria

**Value Criteria (at least 3 of 5 must pass):**
- P/E Ratio (TTM) < 20 (or < sector average if sector is cyclical)
- Price/Book < 2.5
- EV/EBITDA < 12
- Price/FCF < 18
- Enterprise Value / Revenue < 2.0

**Dividend Quality Criteria (at least 3 of 4 must pass):**
- Dividend Yield ≥ 2.5%
- Payout Ratio (dividends / earnings) < 65% (< 80% for REITs/utilities)
- FCF Payout Ratio (dividends / free cash flow) < 75%
- 5-Year dividend growth rate > 3% per year

**Financial Health Criteria (must pass all):**
- Debt/Equity < 1.5 (exception: utilities, REITs can be up to 2.5)
- Current Ratio > 1.0
- Positive Free Cash Flow (FCF > 0 for 3 of last 3 years)

### Step 2 — Compute Dividend Growth Rate

From the dividend history, compute CAGR over 5 years:
```
Dividend CAGR 5Y = (divPS_latest / divPS_5y_ago)^(1/5) - 1
```
If data is only available for 3 years, use 3-year CAGR and note the shorter history.

### Step 3 — Score Each Stock (0–100)

**Value Score (30 points max):**
| Metric | Scoring |
|--------|---------|
| P/E vs. sector median | +10 if < 50th percentile, +5 if < 75th |
| P/B < 1.5 | +10 pts; P/B 1.5–2.5: +5 pts |
| EV/EBITDA < 8 | +10 pts; 8–12: +5 pts |

**Income Score (40 points max):**
| Metric | Scoring |
|--------|---------|
| Dividend Yield ≥ 4% | +15; 3–4%: +10; 2.5–3%: +5 |
| FCF Payout < 50% | +15; 50–65%: +10; 65–75%: +5 |
| Div. CAGR 5Y > 8% | +10; 3–8%: +5; < 3%: +0 |

**Financial Health Score (30 points max):**
| Metric | Scoring |
|--------|---------|
| D/E < 0.5 | +10; 0.5–1.0: +7; 1.0–1.5: +4 |
| Current Ratio > 2 | +10; 1.5–2: +7; 1–1.5: +4 |
| FCF Margin > 15% | +10; 10–15%: +7; 5–10%: +4 |

### Step 4 — Risk Flags

Auto-flag (remove from qualified list or flag prominently):
- ❌ Dividend yield > 8% with payout ratio > 90%: Dividend at severe risk
- ❌ FCF negative for 2+ consecutive years: Cannot fund dividend organically
- ❌ D/E > 3.0 (non-financial): Balance sheet stress → dividend at risk
- ⚠️ Dividend frozen (no growth) for > 3 years while yield is maintained by stock price decline

### Step 5 — Produce Ranking

Rank qualifying stocks by total score (0–100). Present top 10 with:
- Score breakdown
- Dividend yield + 5Y CAGR
- Key valuation metrics
- Main risk flag if any

---

## Output Format

```
╔══════════════════════════════════════════════════════════╗
║    VALUE & DIVIDEND SCREEN  —  {DATE}                   ║
║    Universe: {S&P 500 / User list}  |  Pass: {n}/{total}║
╚══════════════════════════════════════════════════════════╝

🏆 TOP QUALIFIED STOCKS (Ranked by Score)

Rank  Ticker  Score  Yield   DivCAGR  P/E    P/B  EV/EBITDA  Payout  D/E
────  ──────  ─────  ──────  ───────  ─────  ───  ─────────  ──────  ───
 #1   {TKR}   87/100  4.2%    6.8%   12.4x  1.8x   7.2x      45%    0.8
 #2   {TKR}   82/100  3.8%    9.1%   15.1x  2.1x   9.3x      52%    0.6
 #3   {TKR}   79/100  3.2%   11.5%   13.8x  1.5x   8.8x      38%    1.1
 ...

──────────────────────────────────────────────────────────────
HIGHLIGHTED PICK: {TICKER}

  Business:       {Company name, sector, brief description}
  Current Price:  ${price}  |  Market Cap: ${mktcap}

  VALUATION         DIVIDEND              FINANCIAL HEALTH
  P/E:   12.4x ✅   Yield:     4.2% ✅   D/E:         0.8 ✅
  P/B:    1.8x ✅   Payout:   45%   ✅   Current:    2.1x ✅
  EV/EB:  7.2x ✅   FCFPay:   52%   ✅   FCF Margin: 18% ✅
  P/FCF: 14.1x ✅   CAGR 5Y:  6.8% ✅   Debt/Cap:   36% ✅

  Dividend History: $1.20 → $1.40 → $1.55 → $1.68 → $1.80 → $1.92
  5-Year CAGR: 9.9%  |  Streak: {n} consecutive years of growth

  Analyst View: {Buy/Hold/Sell}  |  Price Target: ${target}  |  {n} analysts

  Score Breakdown:
    Value:  {28}/30  |  Income: {35}/40  |  Health: {24}/30  =  87/100

  Investment Thesis: {2-sentence summary of why this passes screening}
  Key Risk:  {1 sentence on main risk (e.g., "Cyclical revenue in automotive sector")}

──────────────────────────────────────────────────────────────
❌ FAILED SCREENER (Notable names that didn't qualify)
  {TICKER}: Fail — Payout ratio {95%} > 65%, dividend at risk
  {TICKER}: Fail — Negative FCF last 2 years

📊 SCREENING SUMMARY
  Passed all criteria:  {n} stocks
  Value + health only:  {n} stocks (no attractive yield)
  High yield only:      {n} stocks (value/health concerns)
  Failed all:           {n} stocks
```

---

## Limitations

- Screening 500 stocks requires many API calls; batch with Pro plan to avoid rate limiting.
- Financial data is trailing/annual; may not reflect recent quarterly deterioration.
- REITs, utilities, and MLPs have structurally higher payout ratios and debt — adjust thresholds.
- International ADRs may have variable withholding taxes on dividends (not modeled here).
