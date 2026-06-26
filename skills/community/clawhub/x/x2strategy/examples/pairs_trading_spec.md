# Pairs trading  does volatility timing matter 

> **3 independent strategies** detected in this paper.

---

## Strategy 1: Minimum Distance Pairs Trading

**Type**: technical
**Asset Class**: equity

A pairs trading strategy that selects pairs by minimizing the sum of squared differences (SSD) of normalized price series during a formation period. Trades are triggered when the normalized spread diverges by more than 2 or 3 standard deviations from its mean, with positions held until convergence or a fixed 6-month horizon. The portfolio is dollar-neutral and equal-weighted across active pairs.

### Data Requirements

- **Source**: Bloomberg, Kenneth French's data library
- **Period**: July 2003 to June 2013
- **Frequency**: daily
- **Universe**: S&P 500 components, Nikkei 225 components
- **Filters**: Large-cap components of S&P 500 or Nikkei 225. Pre-filter: pairs with total return difference > 10% over formation period are discarded (for Minimum Distance method).
- **Data fields**: Price, VIX, market volatility index (Japan)
- **Lookback**: 252 bars

### Indicators (12)

| ID | Name | Category | Formula | Scope |
|:---|:-----|:---------|:--------|:------|
| `normalized_price` | Normalized Price Series | technical | For each stock, scale the price series to start at $1 at the beginning of the fo… | time_series |
| `sum_squared_differences` | Sum of Squared Differences | technical | For each candidate pair (i,j), compute the sum of squared differences between th… | time_series |
| `pair_selection_ranking` | Pair Selection Ranking by Minimum SSD | derived | For each stock, find the partner stock that minimizes the SSD. Rank all candidat… | cross_sectional |
| `pre_selection_filter` | Total Return Difference Filter | technical | Compute the total return difference between two stocks over the formation period… | time_series |
| `normalized_spread` | Normalized Price Spread | technical | During the trading period, compute the spread as the difference between the norm… | time_series |
| `spread_mean` | Spread Mean | technical | Calculate the mean of the normalized spread series during the formation period. … | time_series |
| `spread_std` | Spread Standard Deviation | technical | Calculate the standard deviation of the normalized spread series during the form… | time_series |
| `entry_signal` | Entry Signal Trigger | derived | Generate a trade entry signal when the absolute normalized spread exceeds a mult… | time_series |
| `exit_signal_convergence` | Exit Signal on Convergence | derived | Close the position when the spread returns to zero (converges). Exit = sign(init… | time_series |
| `exit_signal_time` | Time-based Exit Signal | derived | Close the position at the end of the 6-month trading period (126 trading days) r… | time_series |
| `position_direction` | Position Direction Assignment | derived | When entry signal triggers, go long the stock with lower normalized price (loser… | time_series |
| `portfolio_fill_signal` | Portfolio Fill Signal | derived | If fewer than 10 pairs are active on a given day, fill the portfolio with a long… | cross_sectional |

### Logic Pipeline (13 steps)

step1. **filter** (cross_sectional): Pre-filter pairs based on total return difference over formation period — `Keep pair if |total_return_i - total_return_j| ≤ 0.10 (0.20 for cointegration on Nikkei 225)`  
   → output: `filtered_pairs` (boolean)
step2. **arithmetic** (time_series): Calculate normalized price series for each stock over formation period — `P_t^i = price_t^i / price_0^i (scaled to $1 at start of formation period)`  
   → output: `normalized_price_series` (scalar)
step3. **arithmetic** (time_series): Compute sum of squared differences (SSD) for each candidate pair — `SSD = Σ_{t=1 to T} (P_t^i - P_t^j)^2 where T = 252 trading days (12-month formation)`  
   → output: `pair_ssd` (scalar)
step4. **rank** (cross_sectional): Rank filtered pairs by SSD (ascending) — `Rank all filtered pairs from lowest SSD (most similar) to highest SSD`  
   → output: `pair_selection_ranking` (ranking)
step5. **filter** (cross_sectional): Select top 20 pairs with minimum SSD — `Keep pairs where rank ≤ 20`  
   → output: `selected_pairs` (boolean)
step6. **arithmetic** (time_series): Calculate normalized spread for each selected pair at start of trading period — `spread_t = P_t^i - P_t^j (recalculated at start of 6-month trading period)`  
   → output: `current_spread` (scalar)
step7. **arithmetic** (time_series): Compute spread statistics from formation period — `μ_spread = mean(spread over formation period), σ_spread = std(spread over formation period)`  
   → output: `spread_stats` (scalar)
step8. **condition** (time_series): Generate entry signal when spread diverges beyond threshold — `IF |spread_t| > threshold_multiplier * σ_spread THEN entry_signal = TRUE`  
   → output: `entry_signal` (boolean)
step9. **condition** (time_series): Assign position direction based on spread sign — `IF spread_t > 0 THEN long stock j, short stock i (spread positive means P_i > P_j) ELSE long stock i, short stock j`  
   → output: `position_direction` (label)
step10. **condition** (time_series): Generate exit signal on convergence — `IF spread_t crosses 0 (changes sign) THEN exit_signal_convergence = TRUE`  
   → output: `exit_signal_convergence` (boolean)
step11. **condition** (time_series): Generate time-based exit signal after 126 trading days — `IF days_in_position ≥ 126 THEN exit_signal_time = TRUE`  
   → output: `exit_signal_time` (boolean)
step12. **condition** (time_series): Final trade signal combining entry and exit conditions — `IF entry_signal = TRUE AND no existing position THEN OPEN position with direction from position_direction; IF exit_signal_convergence = TRUE OR exit_signal_time = TRUE THEN CLOSE position`  
   → output: `final_trade_signal` (label)
step13. **condition** (cross_sectional): Portfolio fill signal when fewer than 10 active pairs — `IF count(active_pairs) < 10 THEN fill missing positions with long market premium (S&P 500/Topix)`  
   → output: `portfolio_fill_signal` (boolean)

### Execution (1 plans)

**exec_1**: Monthly rebalancing of pairs portfolio with staggered 6-month trading windows. Each month, a new formation period ends, top 20 pairs are selected, and they enter a 6-month trading period. The overall portfolio consists of six overlapping sub-portfolios staggered by one month.
- Trigger: time_driven, monthly, delay=1 bar(s)
- Action: `WHEN 'entry_long_short': OPEN PAIR POSITION (LONG 'loser', SHORT 'winner'); WHEN 'exit_convergence' OR 'exit_time': CLOSE PAIR POSITION`
- Sizing: equal_weight, exposure=1.0, long_short

### Risk Management (5 rules)

- Portfolio fill rule: If fewer than 10 pairs are active on a given day, fill the portfolio with a long position in the equity market premium (S&P 500 premium for U.S., Topix index return minus risk-free rate for Japan) to maintain full investment.
- Position sizing: Dollar-neutral within each pair ($1 long the 'loser' stock, $1 short the 'winner' stock).
- Maximum holding period: Fixed 6-month (126 trading days) horizon for each pair position.
- Pre-selection filter: Discard candidate pairs if the total return difference over the formation period exceeds 10%.
- Transaction costs: Incorporated as 30 bps round-trip (commissions + market impact) plus a 1% annual short-selling fee.

---

## Strategy 2: Stationarity-Based Pairs Trading (ADF Test)

**Type**: technical
**Asset Class**: equity

A pairs trading strategy that selects 20 pairs from S&P 500 or Nikkei 225 components based on the lowest ADF t-statistics of their price ratio, indicating strongest stationarity. Trades are triggered when the normalized price spread exceeds 2 or 3 standard deviations (estimated during formation). Positions are dollar-neutral ($1 long undervalued, $1 short overvalued) and held until spread reverts to zero or 6-month trading period ends.

### Data Requirements

- **Source**: Bloomberg, Kenneth French data library
- **Period**: July 2003 - June 2013
- **Frequency**: daily
- **Universe**: S&P 500 components, Nikkei 225 components
- **Filters**: Large-cap components of major indices (S&P 500 or Nikkei 225). Pre-filter: pairs with total return difference >10% during formation period are discarded. Daily adjusted prices (dividends and splits).
- **Data fields**: Price, VIX, market volatility indices
- **Lookback**: 252 bars

### Indicators (6)

| ID | Name | Category | Formula | Scope |
|:---|:-----|:---------|:--------|:------|
| `adf_t_statistic_price_ratio` | Augmented Dickey-Fuller t-statistic for price ratio | technical | Perform Augmented Dickey-Fuller test on the price ratio series of two stocks ove… | time_series |
| `normalized_price_spread` | Normalized price spread | technical | Calculate the spread between two normalized price series. First, normalize each … | time_series |
| `spread_standard_deviation` | Spread standard deviation | technical | Calculate the standard deviation of the price spread during the formation period… | time_series |
| `total_return_difference` | Total return difference filter | technical | Calculate the absolute difference in total returns between two stocks over the f… | time_series |
| `spread_deviation_signal` | Spread deviation trading signal | technical | Generate trading signal when the absolute value of the normalized spread exceeds… | time_series |
| `pair_selection_ranking` | Pair selection ranking by ADF t-statistic | technical | Rank all candidate pairs by their ADF t-statistics in ascending order (lowest t-… | cross_sectional |

### Logic Pipeline (5 steps)

step1. **filter** (cross_sectional): Pre-filter pairs based on total return difference to reduce computation — `IF ABS(total_return_difference) <= 0.1 THEN keep_pair ELSE discard_pair`  
   → output: `prefiltered_pairs` (boolean)
step2. **rank** (cross_sectional): Rank all pre-filtered pairs by ADF t-statistic of price ratio (lowest = most stationary) — `RANK(adf_t_statistic_price_ratio) WHERE ascending = True (lower t-statistic = better rank)`  
   → output: `pair_selection_ranking` (ranking)
step3. **filter** (cross_sectional): Select top 20 ranked pairs for trading portfolio — `IF pair_selection_ranking <= 20 THEN select_pair ELSE discard_pair`  
   → output: `selected_pairs_portfolio` (boolean)
step4. **condition** (time_series): Monitor normalized price spread for each selected pair during 6-month trading period — `ABS(normalized_price_spread) > (threshold_multiplier * spread_standard_deviation)`  
   → output: `spread_deviation_signal` (boolean)
step5. **custom** (time_series): Generate final trade signal: long undervalued stock, short overvalued stock when spread exceeds threshold — `IF spread_deviation_signal = True THEN: IF normalized_price_spread > 0 THEN SHORT stock_A $position_size, LONG stock_B $position_size ELSE IF normalized_price_spread < 0 THEN SHORT stock_B $position_size, LONG stock_A $position_size`  
   → output: `final_trade_signal` (label)

### Execution (2 plans)

**exec_1**: Monthly rolling formation and trading cycle with daily monitoring and signal-driven execution
- Trigger: signal_driven, daily, delay=1 bar(s)
- Action: `WHEN spread_zscore < -2: LONG undervalued_stock, SHORT overvalued_stock; WHEN spread_zscore > 2: SHORT overvalued_stock, LONG undervalued_stock; WHEN |spread_zscore| < 0.5 OR trading_period_end: CLOSE ALL`
- Sizing: equal_weight, exposure=1.0, long_short

**exec_2**: Monthly portfolio rebalancing - formation period analysis and pair selection
- Trigger: time_driven, monthly, delay=1 bar(s)
- Action: `WHEN new_formation_period: RUN prefilter (10% total return difference filter) → RANK by ADF t-statistic (lowest 20) → SELECT top 20 pairs → INITIALIZE 6-month trading period`
- Sizing: equal_weight, exposure=1.0, long_short

### Risk Management (6 rules)

- Dollar-neutral positions: $1 long and $1 short per pair
- Minimum portfolio size: If fewer than 10 pairs active, fill with long position in equity market premium
- Maximum trading period: 6 months (126 trading days) per pair
- Position closure: Close when spread converges to zero (|zscore| < 0.5) or at end of 6-month period
- Transaction costs: 30 bps round-trip + 1% annual short-selling fee incorporated
- Pre-filter: Discard pairs with total return difference > 10% during formation period

---

## Strategy 3: Johansen Cointegration Pairs Trading with Volatility Timing

**Type**: technical
**Asset Class**: equity

A pairs trading strategy that selects 20 pairs from S&P 500 or Nikkei 225 components using the Johansen cointegration test (highest trace statistics). Trades are initiated when the normalized price spread exceeds 2 or 3 standard deviations from its formation-period mean, with positions closed upon convergence or after 6 months. The strategy operates on rolling 12/24-month formation and 6-month trading windows, rebalanced monthly.

### Data Requirements

- **Source**: Bloomberg, Kenneth French data library
- **Period**: July 2003 - June 2013
- **Frequency**: daily
- **Universe**: S&P 500 components, Nikkei 225 components
- **Filters**: Large-cap index components; pre-filter: pairs with total return difference >10% (20% for cointegration on Nikkei) during formation period are discarded
- **Data fields**: Price, VIX, market volatility index (Japan)
- **Lookback**: 252 bars

### Indicators (8)

| ID | Name | Category | Formula | Scope |
|:---|:-----|:---------|:--------|:------|
| `johansen_trace_statistic` | Johansen Cointegration Trace Statistic | technical | For each candidate pair (i,j), perform the Johansen cointegration test on their … | time_series |
| `normalized_price_spread` | Normalized Price Spread | technical | For a selected pair (i,j), compute the spread as the difference between their no… | time_series |
| `spread_standard_deviation` | Spread Standard Deviation (Formation Period) | technical | The standard deviation of the normalized price spread calculated over the format… | time_series |
| `total_return_difference_filter` | Total Return Difference Filter | technical | Pre-selection filter: For each candidate pair, compute the absolute difference i… | time_series |
| `entry_signal_threshold` | Entry Signal Threshold | technical | Trading signal triggered when the absolute value of the normalized spread exceed… | time_series |
| `exit_signal_convergence` | Exit Signal (Convergence) | technical | Position is closed when the spread returns to zero (converges to its equilibrium… | time_series |
| `exit_signal_time_based` | Exit Signal (Time-Based) | technical | Position is automatically closed at the end of the 6-month (126 trading day) tra… | time_series |
| `pair_ranking_trace_statistic` | Pair Ranking by Trace Statistic | technical | After computing the Johansen trace statistic for all candidate pairs that pass t… | cross_sectional |

### Logic Pipeline (8 steps)

step1. **filter** (cross_sectional): Apply pre-selection filter to discard pairs with excessive total return difference — `Keep pair if total return difference over formation period ≤ 10% (20% for cointegration on Nikkei 225)`  
   → output: `filtered_pairs` (boolean)
step2. **rank** (cross_sectional): Rank filtered pairs by Johansen trace statistic — `Rank all pairs from highest to lowest trace statistic value`  
   → output: `pair_ranking_trace_statistic` (ranking)
step3. **filter** (cross_sectional): Select top 20 pairs for trading portfolio — `Select pairs with rank ≤ 20`  
   → output: `selected_pairs` (boolean)
step4. **condition** (time_series): Monitor normalized price spread for entry signals — `IF ABS(normalized_price_spread) > threshold_multiplier × spread_standard_deviation THEN entry_signal = TRUE`  
   → output: `entry_signal_threshold` (boolean)
step5. **condition** (time_series): Determine trade direction based on spread deviation — `IF normalized_price_spread > 0 THEN short stock A, long stock B ELSE long stock A, short stock B`  
   → output: `trade_direction` (label)
step6. **condition** (time_series): Monitor for convergence exit signal — `IF normalized_price_spread crosses through 0 THEN exit_signal = TRUE`  
   → output: `exit_signal_convergence` (boolean)
step7. **condition** (time_series): Apply time-based exit after 6 months — `IF days since trade entry ≥ 126 THEN exit_signal = TRUE`  
   → output: `exit_signal_time_based` (boolean)
step8. **condition** (time_series): Generate final trade execution signals — `IF entry_signal_threshold = TRUE AND no existing position THEN OPEN position with trade_direction; IF exit_signal_convergence = TRUE OR exit_signal_time_based = TRUE THEN CLOSE position`  
   → output: `trade_execution_signal` (label)

### Execution (1 plans)

**exec_1**: Monthly rolling formation and trading cycle with daily monitoring for entry/exit signals
- Trigger: time_driven, monthly, delay=1 bar(s)
- Action: `WHEN 'open_long_short': LONG undervalued stock, SHORT overvalued stock; WHEN 'close_convergence': CLOSE ALL positions for that pair; WHEN 'close_time_based': CLOSE ALL positions for that pair`
- Sizing: equal_weight, exposure=1.0, long_short

### Risk Management (4 rules)

- Portfolio minimum: If fewer than 10 pairs are active on a given day, fill remaining positions with a long position in the equity market premium (S&P 500 premium for U.S., Topix index return minus risk-free rate for Japan)
- Maximum holding period: 6 months (126 trading days) per pair
- Transaction costs: 30 bps round-trip (commissions + market impact) plus 1% annual short-selling fee
- Pre-selection filter: Discard pairs with total return difference > 20% during formation period (for cointegration method on Nikkei 225)
