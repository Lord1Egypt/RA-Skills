# A Quantitative Approach to Tactical Asset Allocation

## Global Tactical Asset Allocation (GTAA) with 10-Month Moving Average Timing

**Type**: technical
**Asset Class**: equity, bonds, commodities, real_estate

A time-series trend-following strategy that uses a simple 10-month moving average crossover rule to tactically allocate between risky assets and cash. For each of five asset classes, the strategy goes long when the month-end price exceeds its 10-month simple moving average, and moves to cash (T-bills) otherwise. The portfolio is equally weighted across assets, with each asset managed independently.

### Data Requirements

- **Source**: Global Financial Data (GFD), Morningstar/Dimson Marsh Staunton, Cowles Commission/S&P
- **Period**: 1973-2012
- **Frequency**: monthly
- **Universe**: S&P 500 Total Return Index, MSCI EAFE Total Return Index, US 10-Year Government Bond Total Return Index, Goldman Sachs Commodity Index (GSCI) Total Return, NAREIT Index Total Return
- **Filters**: Five specified total return indices representing major asset classes; no additional filters applied.
- **Data fields**: Price
- **Lookback**: 210 bars

### Expected Performance

- Sharpe: 0.63
- Annual Return: 9.9%
- Max Drawdown: -7.2%

### Indicators (2)

| ID | Name | Category | Formula | Scope |
|:---|:-----|:---------|:--------|:------|
| `sma_10_month` | 10-Month Simple Moving Average | technical | Calculate the simple moving average of monthly closing prices over the most rece… | time_series |
| `price_sma_crossover_signal` | Price vs. SMA Crossover Signal | technical | Compare the current month's closing price to the 10-month SMA. Generate a binary… | time_series |

### Logic Pipeline (4 steps)

step1. **arithmetic** (time_series): Calculate 10-month simple moving average for each asset — `SMA_10(t) = (P(t) + P(t-1) + ... + P(t-9)) / 10, where P is monthly closing price`  
   → output: `sma_10_month` (scalar)
step2. **condition** (time_series): Generate crossover signal by comparing current price to 10-month SMA — `IF price_monthly_close(t) > sma_10_month(t) THEN TRUE ELSE FALSE`  
   → output: `price_sma_crossover_signal` (boolean)
step3. **condition** (time_series): Convert boolean signal to asset allocation decision for each asset class — `IF price_sma_crossover_signal(t) = TRUE THEN allocate 20% to asset_class_i ELSE allocate 20% to cash (90-day T-bills)`  
   → output: `asset_allocation_signal` (label)
step4. **custom** (cross_sectional): Aggregate independent asset class signals into final portfolio allocation — `Portfolio(t) = Σ(asset_allocation_signal_i(t) for i=1 to 5), where each asset_class_i contributes either 20% to its risky asset or 20% to cash based on its individual signal`  
   → output: `final_portfolio_allocation` (scalar)

### Execution (1 plans)

**exec_1**: Monthly rebalancing of GTAA portfolio based on 10-month SMA crossover signals for each asset class
- Trigger: time_driven, end_of_month, delay=1 bar(s)
- Action: `WHEN price_sma_crossover_signal=True: LONG asset; WHEN price_sma_crossover_signal=False: EXIT asset to cash`
- Sizing: equal_weight, exposure=1.0, long_only

### Risk Management (5 rules)

- No explicit stop-loss rules
- Position limit per asset: 20% of portfolio (equal weight allocation)
- Maximum risky asset exposure: 100% (when all 5 assets are above SMA)
- Minimum risky asset exposure: 0% (when all 5 assets are below SMA)
- Cash position when asset signal is negative: 90-day Treasury bills
