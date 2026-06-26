---
name: Sector Rotation Analyst
version: 1.0.2
description: "Identify sector rotation opportunities across all 11 GICS sectors using relative strength, momentum, and macro regime context from the Finskills API."
author: finskills
metadata:
  openclaw:
    requires:
      env:
        - FINSKILLS_API_KEY
    primaryEnv: FINSKILLS_API_KEY
  homepage: https://github.com/finskills/sector-rotation-analyst
---

# Sector Rotation Analyst

Identify which of the 11 GICS sectors are leading or lagging the market using
live sector performance data, ETF holdings, and index constituent analysis from
the Finskills API. Generates a sector rotation map with actionable over/underweight
recommendations aligned with the current macro regime.

---

## Setup

**API Key required** — [Register at https://finskills.net](https://finskills.net) to get your free key.  
Header: `X-API-Key: <your_api_key>`
> **Get your API key**: Register at **https://finskills.net** — free tier available, Pro plan unlocks real-time quotes, history, and financials.

---

## When to Activate This Skill

Activate when the user:
- Asks which sectors are leading or lagging the market
- Wants top stock picks within a specific sector
- Asks about sector rotation strategy based on the economic cycle
- Wants to understand which ETFs offer sector exposure
- Asks "where is smart money flowing?" or "which sectors are hot right now?"

---

## Data Retrieval — Finskills API Calls

### 1. Sector Performance Data
```
GET https://finskills.net/v1/market/sectors
```
Extract: All 11 GICS sectors with performance across timeframes: `1D`, `1W`, `1M`, `3M`, `YTD`, `1Y`

### 2. ETF Holdings (for sector leaders)
For each sector's representative ETF (XLK, XLF, XLV, etc.):
```
GET https://finskills.net/v1/free/etf/holdings/{SECTOR_ETF}
```
Extract: top 10 holdings (ticker, weight, company name)

### 3. S&P 500 Index Constituents (for sector weights)
```
GET https://finskills.net/v1/free/index/SP500/constituents
```
Extract: all constituents with sector classification — compute actual S&P 500 sector weights

### 4. Market Summary (Benchmark Context)
```
GET https://finskills.net/v1/market/summary
```
Extract: S&P 500, Nasdaq, Russell 2000 performance for relative comparison

---

## Sector ETF Reference Map

| Sector | ETF | Description |
|--------|-----|-------------|
| Technology | XLK | Software, hardware, semiconductors |
| Healthcare | XLV | Pharma, biotech, medical devices |
| Financials | XLF | Banks, insurance, asset managers |
| Consumer Discretionary | XLY | Retail, autos, restaurants |
| Industrials | XLI | Defense, aerospace, construction |
| Communication Services | XLC | Media, telecom, internet |
| Consumer Staples | XLP | Food, beverage, household products |
| Energy | XLE | Oil & gas, refiners |
| Real Estate | XLRE | REITs |
| Materials | XLB | Mining, chemicals, paper |
| Utilities | XLU | Power, water, gas utilities |

---

## Analysis Workflow

### Step 1 — Sector Performance Snapshot

Create a leaderboard for each performance period: 1D, 1W, 1M, 3M, YTD:

**Rank sectors** from best to worst performer for each timeframe.

Flag **divergences**:
- Sector outperforming YTD but recently lagging 1M: momentum fade, potential reversal
- Sector lagging YTD but recently leading 1M: early rotation, potential breakout

**Relative strength vs. S&P 500** for each sector:
```
Sector Relative Return = Sector Return − S&P 500 Return (same period)
```
- Positive = outperforming (overweight candidate)
- Negative = underperforming (underweight candidate)

### Step 2 — Sector Rotation Cycle Mapping

Map current sector performance to the classic economic cycle:

```
Economic Cycle → Sector Leadership Pattern:

Early Recovery (recession ending):
  Leaders: Consumer Discretionary, Financials, Industrials
  Laggards: Utilities, Consumer Staples, Healthcare

Middle Expansion (goldilocks):
  Leaders: Technology, Industrials, Basic Materials
  Laggards: Utilities, Consumer Staples

Late Expansion (overheating):
  Leaders: Energy, Materials, Healthcare
  Laggards: Financials, Consumer Discretionary

Contraction (recession):
  Leaders: Consumer Staples, Utilities, Healthcare
  Laggards: Energy, Financials, Consumer Discretionary
```

Cross reference actual sector performance to infer the **current cycle phase** and whether the market is rotating toward or away from the expected pattern.

### Step 3 — Top Stock Leaders Within Sectors

For the top 2–3 leading sectors, extract top ETF holdings:
- List top 5 companies by weight in the sector ETF
- Note weighting (stocks with > 10% weight dominate ETF returns)
- Flag the sector ETF's largest contributors to recent performance

### Step 4 — Sector Concentration in S&P 500

From the index constituents data:
- Show current S&P 500 sector weights
- Flag if any sector is > 30% weight (systemic concentration risk for index investors)
- Note sector weight trend (growing vs. shrinking weight)

### Step 5 — Recommendations

Provide:
- **Overweight** (OW): 2–3 sectors with strongest momentum + macro tailwinds
- **Neutral** (N): sectors with mixed signals or in transition
- **Underweight** (UW): sectors with weakening momentum + macro headwinds

---

## Output Format

```
╔══════════════════════════════════════════════════════╗
║    SECTOR ROTATION REPORT  —  {DATE}                ║
╚══════════════════════════════════════════════════════╝

📊 SECTOR PERFORMANCE LEADERBOARD
  Sector               ETF    1D      1W      1M      3M      YTD
  ─────────────────────────────────────────────────────────────────
  Technology          XLK    +1.8%   +3.2%   +8.1%   +15.2%  +22.4%
  Communication Svcs  XLC    +1.2%   +2.1%   +5.3%   +11.0%  +18.1%
  Consumer Disc.      XLY    +0.9%   +1.0%   +2.2%   +5.1%   +12.3%
  Industrials         XLI    +0.4%   +0.3%   +1.1%   +3.2%    +8.4%
  Financials          XLF    -0.1%   -0.5%   +0.8%   +2.1%    +6.2%
  Healthcare          XLV    -0.3%   +0.1%   -0.5%   +1.0%    +4.1%
  Materials           XLB    -0.5%   -1.2%   -1.0%   +0.2%    +2.1%
  Energy              XLE    -0.8%   -2.1%   -4.2%   -3.0%    -2.4%
  Real Estate         XLRE   -1.0%   -1.5%   -2.3%   -1.2%    -3.0%
  Consumer Staples    XLP    -1.1%   -1.0%   -1.8%   +0.5%    +2.0%
  Utilities           XLU    -1.4%   -2.0%   -3.1%   -2.5%    -1.5%
  ─────────────────────────────────────────────────────────────────
  S&P 500 (SPY)              +0.5%   +0.8%   +2.3%   +5.4%   +10.2%

🔄 ROTATION CYCLE SIGNAL: {Cycle Phase — e.g., "Mid-to-Late Expansion"}
   Market aligning with: {expected leaders for this cycle} ✅
   Anomalies: {any sectors not behaving as expected}

🏆 TOP SECTORS — EXPANDED VIEW

  #1 Technology (XLK) — YTD +22.4% vs SPY +10.2% (+12.2pp)
  Top Holdings: AAPL {weight}%, MSFT {weight}%, NVDA {weight}%, ...
  Catalyst: {AI capex cycle / Strong pricing power / etc.}

  #2 Communication Services (XLC) — YTD +18.1% vs SPY +10.2% (+7.9pp)
  Top Holdings: GOOG {weight}%, META {weight}%, ...
  Catalyst: {Digital advertising recovery / streaming growth}

  #3 {Next sector...}

📉 WEAKEST SECTORS
  Utilities (XLU) — YTD -1.5% | Headwind: Rising rates hurt dividend valuations
  Energy (XLE) — YTD -2.4% | Headwind: Oil supply increase, demand concerns

🏛️ S&P 500 SECTOR WEIGHTS
  Technology: {%} | Healthcare: {%} | Financials: {%} | ...
  [⚠️ Flag if Tech > 30%]

🎯 TACTICAL RECOMMENDATIONS
  OVERWEIGHT:  {Sector 1}, {Sector 2}  —  {rationale}
  NEUTRAL:     {Sector 3}, {Sector 4}
  UNDERWEIGHT: {Sector 5}, {Sector 6}  —  {rationale}
```

---

## Limitations

- Sector ETF performance may diverge from underlying sector due to size/weight concentration.
- Sector rotation is a medium-term (1–6 month) framework; it has low signal at daily resolution.
- ETF holdings data may lag actual portfolio composition by 1–3 months.
