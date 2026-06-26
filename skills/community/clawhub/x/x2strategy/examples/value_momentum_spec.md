# Value and Momentum Everywhere

> **2 independent strategies** detected in this paper.

---

## Strategy 1: Cross-Sectional Value Factor Strategy

**Type**: hybrid
**Asset Class**: equity, forex, bonds, commodities

Rank assets within each of eight asset classes based on a standardized value signal, then go long the top quintile (cheapest) and short the bottom quintile (most expensive). For stocks/indices, the signal is book-to-market ratio; for other asset classes, it is the negative of a 5-year past return.

### Data Requirements

- **Source**: ['CRSP', 'Compustat', 'Datastream', 'Worldscope', 'MSCI', 'Bloomberg', 'Morgan Markets', 'Consensus Economics', 'Futures Exchanges (LME, ICE, CME, CBOT, NYMEX, COMEX, NYBOT, TOCOM)']
- **Period**: 1972-07-2011
- **Frequency**: monthly
- **Universe**: U.S. Individual Stocks, U.K. Individual Stocks, European Individual Stocks, Japanese Individual Stocks, Global Equity Indices (18 developed markets), Currencies (10 currencies), Global Government Bonds (10 countries), Commodity Futures (27 commodities)
- **Filters**: For individual stocks: Exclude ADRs, REITs, financials, closed-end funds, foreign shares; exclude stocks with share price < $1 at month start; must have book value from Compustat/Worldscope in previous 6 months; must have ≥12 months of past return history; liquidity filter: include only stocks cumulatively accounting for 90% of total regional market capitalization. For other asset classes: Minimum securities available at sample start (e.g., min 8 equity indices, min 7 currencies, min 5 bonds, min 10 commodities).
- **Data fields**: Price, Book-to-Market, CPI inflation data, 10-year government bond yields
- **Lookback**: 1260 bars

### Indicators (5)

| ID | Name | Category | Formula | Scope |
|:---|:-----|:---------|:--------|:------|
| `book_to_market` | Book-to-Market Ratio | fundamental | Book value of equity divided by market value of equity. For individual stocks, b… | cross_sectional |
| `negative_5y_spot_return` | Negative 5-Year Spot Return | technical | Negative of the 5-year spot return. Calculated as the log of the average spot pr… | time_series |
| `negative_5y_real_fx_return` | Negative 5-Year Real Exchange Rate Return | derived | Negative of the 5-year exchange rate return, adjusted for purchasing power parit… | time_series |
| `negative_5y_bond_return_proxy` | Negative 5-Year Bond Return Proxy | technical | Proxy for the negative 5-year return on government bonds, approximated by the 5-… | time_series |
| `value_signal_standardized` | Standardized Value Signal | derived | The raw value indicator (BE/ME for stocks/indices, negative 5-year return for ot… | cross_sectional |

### Logic Pipeline (4 steps)

step1. **custom** (time_series): Calculate asset-specific value signal based on asset class — `IF asset_class IN ('individual_stocks', 'country_equity_indices') THEN value_raw = book_to_market ELSE IF asset_class = 'commodities' THEN value_raw = negative_5y_spot_return ELSE IF asset_class = 'currencies' THEN value_raw = negative_5y_real_fx_return ELSE IF asset_class = 'bonds' THEN value_raw = negative_5y_bond_return_proxy`  
   → output: `value_raw_signal` (scalar)
step2. **z_score** (cross_sectional): Standardize raw value signal cross-sectionally within each asset class — `value_signal_standardized = (value_raw_signal - mean(value_raw_signal_within_asset_class)) / std(value_raw_signal_within_asset_class)`  
   → output: `value_signal_standardized` (scalar)
step3. **quantile_sort** (cross_sectional): Sort assets into quintiles based on standardized value signal within each asset class — `value_quintile = assign_quantile(value_signal_standardized, n=5) where Q1=lowest_signal (most expensive), Q5=highest_signal (cheapest)`  
   → output: `value_quintile` (label)
step4. **condition** (cross_sectional): Generate final trade signal based on value quintile ranking — `IF value_quintile = 'Q5' THEN signal = 'long' ELSE IF value_quintile = 'Q1' THEN signal = 'short' ELSE signal = 'neutral'`  
   → output: `trade_signal` (label)

### Execution (1 plans)

**exec_1**: Monthly rebalancing of cross-sectional value factor portfolios within each asset class
- Trigger: time_driven, monthly, delay=1 bar(s)
- Action: `WHEN 'Q1': LONG; WHEN 'Q5': SHORT`
- Sizing: equal_weight, exposure=1.0, long_short

---

## Strategy 2: Cross-Sectional Momentum Factor Strategy (MOM2-12)

**Type**: technical
**Asset Class**: equity, forex, bonds, commodities

Rank assets within each of eight asset classes based on past 12-month return (skipping the most recent month), then go long the top quintile (winners) and short the bottom quintile (losers). The strategy uses a pure price momentum signal applied uniformly across all asset classes.

### Data Requirements

- **Source**: ['CRSP', 'Datastream', 'Worldscope', 'MSCI', 'Bloomberg', 'Morgan Markets', 'Futures Exchanges (LME, ICE, CME, CBOT, NYMEX, COMEX, NYBOT, TOCOM)']
- **Period**: 1972-07-2011-07
- **Frequency**: monthly
- **Universe**: U.S. Individual Stocks, U.K. Individual Stocks, European Individual Stocks, Japanese Individual Stocks, Global Equity Indices (18 developed markets), Currencies (10 currencies), Global Government Bonds (10 countries), Commodity Futures (27 commodities)
- **Filters**: For individual stocks: Exclude ADRs, REITs, financials, closed-end funds, foreign shares; price ≥ $1 at month start; must have book value in previous 6 months; must have ≥12 months return history; liquidity filter: include only stocks cumulatively accounting for 90% of total regional market cap. For other asset classes: Minimum securities available at sample start (e.g., min 8 equity indices, min 7 currencies, min 5 bonds, min 10 commodities).
- **Data fields**: Price
- **Lookback**: 252 bars

### Indicators (2)

| ID | Name | Category | Formula | Scope |
|:---|:-----|:---------|:--------|:------|
| `mom2_12` | 12-Month Momentum (Skipping Most Recent Month) | technical | Cumulative raw return over the past 12 months, excluding the most recent month (… | time_series |
| `cross_sectional_rank_mom2_12` | Cross-Sectional Rank by MOM2-12 | derived | Within each asset class at time t, rank all assets based on their MOM2-12 signal… | cross_sectional |

### Logic Pipeline (4 steps)

step1. **arithmetic** (time_series): Calculate the 12-month momentum signal for each asset, skipping the most recent month — `MOM2-12 = cumulative return from month t-12 to month t-2 (inclusive)`  
   → output: `mom2_12` (scalar)
step2. **rank** (cross_sectional): Rank all assets within each asset class based on their MOM2-12 signal — `For each asset class at time t: assign rank = 1 to highest MOM2-12 value, rank = N to lowest MOM2-12 value`  
   → output: `cross_sectional_rank_mom2_12` (ranking)
step3. **quantile_sort** (cross_sectional): Sort assets within each asset class into quintiles based on MOM2-12 ranking — `Within each asset class: assign quintile labels (Q1, Q2, Q3, Q4, Q5) where Q1 = top 20% (highest MOM2-12), Q5 = bottom 20% (lowest MOM2-12)`  
   → output: `momentum_quintile` (label)
step4. **condition** (cross_sectional): Generate final trade signals based on momentum quintile assignment — `IF momentum_quintile = 'Q1' THEN 'long_signal' ELSE IF momentum_quintile = 'Q5' THEN 'short_signal' ELSE 'no_trade'`  
   → output: `trade_signal` (label)

### Execution (1 plans)

**exec_1**: Monthly rebalancing of cross-sectional momentum strategy based on MOM2-12 ranking within each asset class
- Trigger: time_driven, monthly, delay=1 bar(s)
- Action: `WHEN 'top_quintile': LONG; WHEN 'bottom_quintile': SHORT`
- Sizing: equal_weight, exposure=1.0, long_short

### Risk Management (5 rules)

- Liquidity filter: For individual stocks, restrict universe to stocks cumulatively accounting for 90% of total market capitalization in each region
- Price filter: Exclude stocks with share price < $1 at beginning of each month
- Minimum history: Assets must have at least 12 months of past return history
- Asset class constraints: Portfolio constructed separately within each of eight asset classes
- No explicit stop-loss or position limits mentioned in paper
