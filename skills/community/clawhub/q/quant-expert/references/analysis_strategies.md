# Quantitative Analysis Strategies

This document provides detailed analysis strategies and workflows for common quantitative analysis tasks using the Tushare Pro API.

The built-in helper scripts currently cover:

- value, dividend, growth, and momentum screening
- a structured single-stock diagnosis snapshot
- trading-day and holiday checks

More advanced combinations below can still be done with custom Tushare queries, but they are not all fully automated by the shipped scripts.

## Table of Contents

1. [Stock Selection Strategies](#1-stock-selection-strategies)
2. [Stock Diagnosis Workflow](#2-stock-diagnosis-workflow)
3. [Market Overview Analysis](#3-market-overview-analysis)
4. [Sector Rotation Analysis](#4-sector-rotation-analysis)
5. [Risk Assessment Framework](#5-risk-assessment-framework)
6. [ETF Analysis Workflow](#6-etf-analysis-workflow)
7. [Intraday & Real-time Analysis](#7-intraday--real-time-analysis)
8. [Options Analysis Workflow](#8-options-analysis-workflow)
9. [Margin Trading Analysis](#9-margin-trading-analysis)
10. [Data + Event Intelligence Fusion](#10-data--event-intelligence-fusion)

## 1. Stock Selection Strategies

### 1.1 Value Investing Screen

**Goal:** Find undervalued stocks with strong fundamentals.

**Step 1:** Get the latest trading date from `trade_cal` or use `holiday_helper.py` to check if today is a trading day.

**Step 2:** Query `daily_basic` with the latest `trade_date` to get PE, PB, and market cap for all stocks.

**Step 3:** Query `fina_indicator` for the latest reporting period to get `ROE`.

**Step 4:** Apply filters:
- PE_TTM < 20 (or user-specified)
- PB < 3
- ROE > 15%
- Total market cap > 10 billion CNY
- Exclude ST stocks (cross-reference with `stock_st`)

**Step 5:** Present results sorted by:
- lower `PE_TTM`
- lower `PB`
- higher `ROE`
- larger market cap as a secondary tie-breaker

### 1.2 Growth Stock Screen

**Goal:** Find high-growth companies.

**Step 1:** Query `fina_indicator` and keep the latest row for each stock.

**Step 2:** Use the latest YoY fields already returned by `fina_indicator`.

**Step 3:** Apply filters:
- Revenue growth > 20% YoY
- Net profit growth > 25% YoY
- ROE > 10%

**Step 4:** Join the latest valuation snapshot from `daily_basic`.

**Step 5:** Present results sorted by:
- higher net profit YoY
- higher revenue YoY
- higher `ROE`
- lower `PE_TTM` as a tie-breaker

### 1.3 Dividend Yield Screen

**Goal:** Find high-dividend stocks.

**Step 1:** Query `daily_basic` for `dv_ttm`.

**Step 2:** Query `dividend` for each shortlisted stock and count consecutive dividend years.

**Step 3:** Apply filters:
- Dividend yield > 3%
- Consistent dividend payments (at least 3 consecutive years)

**Step 4:** Present results sorted by dividend yield descending.

### 1.4 Technical Momentum Screen

**Goal:** Find stocks with strong daily momentum and liquidity confirmation.

**Step 1:** Query `daily` for the latest `pct_chg`, `close`, `vol`, and `amount`.

**Step 2:** Query `daily_basic` for `volume_ratio`, `turnover_rate`, `pe_ttm`, `pb`, and `total_mv`.

**Step 3:** Apply filters:
- Daily gain above threshold
- `volume_ratio` above threshold
- `turnover_rate` above threshold

**Step 4:** Present results sorted by:
- higher `pct_chg`
- higher `volume_ratio`
- higher `turnover_rate`
- higher trading amount

### 1.5 Hot Money / Momentum Screen

**Goal:** Find stocks with strong short-term momentum and institutional interest.

**Step 1:** Query `top_list` for recent dragon tiger list appearances.

**Step 2:** Query `limit_step` for consecutive limit-up stocks.

**Step 3:** Query `ths_hot` or `dc_hot` for trending stocks.

**Step 4:** Query `moneyflow` for net main force inflow.

**Step 5:** Present results with momentum indicators and risk warnings.

## 2. Stock Diagnosis Workflow

When a user asks for a diagnosis of a specific stock, the shipped script follows this structured snapshot workflow:

### Step 1: Basic Information

Query `stock_company` and `stock_basic` to get:
- Company name, industry, region
- Listing date, exchange
- Business scope, number of employees

### Step 2: Market Performance

Query `daily` (last year) and `daily_basic` to get:
- Recent price trend and returns
- PE, PB, PS ratios
- Market cap, turnover rate, volume ratio
- 52-week high/low

### Step 3: Financial Health

Query `income` and `fina_indicator` for the last 3 years:
- Revenue and net profit trends
- ROE trends
- Gross margin, net margin trends

### Step 4: Shareholder Analysis

Query `top10_holders` and `stk_holdernumber`:
- Major shareholders
- Shareholder count trend (decreasing = concentration)

### Step 5: Capital Flow

Query `moneyflow`:
- Main force net inflow trend
- Large order vs small order flow

### Step 6: Risk Assessment

Query `stock_st`, `pledge_stat`, `share_float`:
- ST risk status
- Pledge ratio (high pledge = risk)
- Upcoming restricted share unlocks

### Step 7: Summary

Combine the data into a structured snapshot with:
- key facts
- recent performance
- valuation
- financial trend notes
- shareholder and money-flow observations
- risk reminders

The shipped script does **not** produce an automatic buy/sell rating.

### Step 8: Event Intelligence Overlay (Mandatory for Judgment Tasks)

For any diagnosis that includes interpretation or recommendation, add external event intelligence:

- Stock-level events: company announcements, management changes, legal events, M&A, earnings guidance
- Industry-level events: policy, supply-demand, pricing, capacity, regulation, competition shifts
- Macro/global events: rates, liquidity, USD/yields, commodities, geopolitics, systemic risk

For each event, include: `title`, `published_time`, `source`, `url`, `impact_direction`, `confidence`.

Then classify the result as:

- **Resonance**: data and events point to the same direction
- **Divergence**: data and events conflict (must explain short-term vs medium-term implications)

## 3. Market Overview Analysis

### Daily Market Summary

**Step 1:** Query `index_daily` for major indices (000001.SH, 399001.SZ, 399006.SZ), or use `rt_k` for real-time snapshots (e.g., `pro.rt_k(ts_code='000001.SH,399001.SZ,399006.SZ')`).

**Step 2:** Query `moneyflow_mkt_dc` for overall market money flow.

**Step 3:** Query `moneyflow_hsgt` for northbound/southbound capital flow.

**Step 4:** Query `limit_list_d` for limit up/down counts.

**Step 5:** Query `limit_cpt_list` for strongest sectors.

**Step 6:** Present a comprehensive market summary.

### Macro Environment Check

**Step 1:** Query latest `cn_gdp`, `cn_cpi`, `cn_ppi` for economic indicators.

**Step 2:** Query `cn_m` for M1/M2 growth.

**Step 3:** Query `shibor` and `shibor_lpr` for interest rate environment.

**Step 4:** Assess overall macro environment (expansionary/contractionary).

## 4. Sector Rotation Analysis

**Step 1:** Query `ths_index` to get all sector/concept boards.

**Step 2:** Query `ths_daily` for sector index performance over different periods (1 week, 1 month, 3 months).

**Step 3:** Query `moneyflow_ind_ths` for sector money flow.

**Step 4:** Identify:
- Leading sectors (strong performance + net inflow)
- Lagging sectors (weak performance + net outflow)
- Rotation candidates (improving money flow but not yet reflected in price)

**Step 5:** For each interesting sector, query `ths_member` to get constituent stocks.

## 5. Risk Assessment Framework

### Individual Stock Risk Score

Calculate a composite risk score (0-100, higher = riskier) based on:

| Risk Factor | Weight | Data Source | High Risk Threshold |
|-------------|--------|-------------|---------------------|
| ST status | 20% | `stock_st` | Is ST = 100 |
| Pledge ratio | 15% | `pledge_stat` | > 50% = 100 |
| Debt ratio | 15% | `balancesheet` | > 70% = 100 |
| Audit opinion | 10% | `fina_audit` | Non-standard = 100 |
| Cash flow | 10% | `cashflow` | Negative OCF = 100 |
| Shareholder concentration | 10% | `stk_holdernumber` | Rapidly increasing = 80 |
| Restricted unlock | 10% | `share_float` | Large unlock within 3 months = 80 |
| Valuation | 10% | `daily_basic` | PE > 100 = 80 |

### Portfolio Risk Check

For a portfolio of stocks, run the individual risk assessment on each stock and flag any with a risk score above 60.

## 6. ETF Analysis Workflow

**Goal:** Analyze a specific ETF or screen for ETFs based on criteria.

### 6.1 ETF Diagnosis

**Step 1: Basic Information**
- Query `etf_basic` to get the ETF's name, tracking index, and management fee.
- Query `etf_index` to understand the composition of the underlying index.

**Step 2: Market Performance & Scale**
- Query `fund_daily` for historical price and volume trends.
- Query `etf_share_size` to analyze the trend of ETF share size and Net Asset Value (NAV). A growing share size indicates investor interest.
- Use `fund_adj` to calculate adjusted returns.

**Step 3: Liquidity Analysis**
- Analyze average daily volume from `fund_daily` to assess liquidity. Higher volume is generally better.

**Step 4: Tracking Error**
- Compare the ETF's daily returns (`fund_daily`) with the returns of its tracking index (query the index daily data) to estimate tracking error.

### 6.2 ETF Screener

**Goal:** Screen for ETFs based on sector, size, or performance.

**Step 1:** Get all ETFs using `etf_basic`.

**Step 2:** Filter by criteria:
- **Sector/Theme:** Filter by `track_index` name (e.g., 'CSI 300', 'ChiNext', 'Semiconductor').
- **Scale:** Filter by `total_mv` from `etf_share_size`.
- **Performance:** Calculate returns over a period using `fund_daily`.
- **Liquidity:** Filter by average daily `vol` or `amount` from `fund_daily`.

**Step 3:** Present a ranked list of ETFs that meet the criteria.

## 7. Intraday & Real-time Analysis

**Goal:** Monitor intraday market movements and real-time data.

**Step 1: Real-time Quotes**
- Use `rt_k` for real-time daily K-line snapshots. Supports wildcard batch fetching:
  - All Shanghai: `pro.rt_k(ts_code='6*.SH')`
  - All ChiNext: `pro.rt_k(ts_code='3*.SZ')`
  - Full market: `pro.rt_k(ts_code='3*.SZ,6*.SH,0*.SZ,9*.BJ')` (max 6000 per call)
  - Single stock: `pro.rt_k(ts_code='600000.SH')`
- Returns: open/high/low/close, volume, amount, trade count, bid/ask prices.
- Use `pro_bar` with `freq` parameter (e.g., `1min`, `5min`) for historical minute-level analysis.

**Step 2: Intraday Pattern Analysis**
- Use `rt_k` to monitor real-time price action and volume across the market.
- Compare current intraday volume profile with historical patterns from `pro_bar` minute data.

**Step 3: Intraday Money Flow**
- Use `moneyflow` with the current `trade_date` to track main force vs. retail flow throughout the day.

**Step 4: Limit Up/Down Monitoring**
- Use `limit_list_d` and `limit_list_ths` to monitor stocks hitting their price limits, which signals extreme momentum.

## 8. Options Analysis Workflow

**Goal:** Analyze options contracts for strategy building.

**Step 1: Find Contracts**
- Use `opt_basic` to find available option contracts for a specific underlying asset (e.g., 50 ETF), filtering by `call_put` (Call/Put) and expiration dates.

**Step 2: Analyze Option Chains**
- For a given expiration date, retrieve the full option chain using `opt_daily` for all relevant contracts.
- Analyze key metrics: Open Interest (`oi`), Volume (`vol`), and Implied Volatility (can be derived from Greeks).

**Step 3: Greeks Analysis**
- Use the Greeks (`delta`, `gamma`, `vega`, `theta`) from `opt_daily` to assess risk and potential profit/loss for different strategies (e.g., covered call, straddle).

## 9. Margin Trading Analysis

**Goal:** Analyze margin trading data to gauge market sentiment.

**Step 1: Market-level Sentiment**
- Query `margin` for the whole market (without `ts_code`) to get total financing balance (`rzye`) and financing purchase amount (`rzmre`).
- An increasing trend in total margin balance suggests rising bullish sentiment.

**Step 2: Individual Stock Sentiment**
- Query `margin_detail` for a specific stock.
- Analyze the trend of `rzye`. A rising balance coupled with a rising stock price is a bullish confirmation.
- A sharp increase in `rzmre` (margin buy amount) can signal strong short-term interest.

**Step 3: Identify Margin Targets**
- Use `margin_secs` to check which stocks are eligible for margin trading, as this can influence their liquidity and volatility.

## 10. Data + Event Intelligence Fusion

Use this workflow whenever the user asks for a conclusion, ranking, diagnosis, or actionable interpretation.

### 10.1 Two-Layer Pipeline

**Layer A: Quantitative Data (Tushare)**
- Pull core numeric evidence first (price, valuation, financials, money flow, risk flags).

**Layer B: Event Intelligence (Web)**
- Pull stock, industry, and macro/global events from credible online sources.

### 10.2 Minimum Evidence Requirement

- At least **2 stock-level** events
- At least **2 industry-level** events
- At least **2 macro/global** events

If evidence is insufficient, state this explicitly and lower confidence.

### 10.3 Source Quality Priority

1. Exchanges, regulators, official filings, company IR pages
2. Major financial media / primary institutional channels
3. Secondary aggregators and reposts (lower confidence)

### 10.4 Event Impact Scoring (Simple)

Assign each event:
- `impact_direction`: bullish / neutral / bearish
- `impact_strength`: 1 to 5
- `confidence`: high / medium / low

Create an event score by weighted aggregation, giving higher weights to higher-confidence sources.

### 10.5 Final Fusion Output

Final answer should follow this order:

1. One-sentence plain-language conclusion
2. Key quantitative findings
3. Key event findings (with source + URL)
4. Resonance/divergence judgment
5. Main risks and invalidation triggers
6. Investment disclaimer
