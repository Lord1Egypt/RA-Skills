# Value and Momentum Everywhere

> **==> picture [361 x 35] intentionally omitted <==**
> 
> THE JOURNAL OF FINANCE[•] VOL. LXVIII, NO. 3[•] JUNE 2013 
> 
> ## **Value and Momentum Everywhere** 
> 
> CLIFFORD S. ASNESS, TOBIAS J. MOSKOWITZ, and LASSE HEJE PEDERSEN[∗] 
> 
> ## **ABSTRACT** 
> 
> We find consistent value and momentum return premia across eight diverse markets and asset classes, and a strong common factor structure among their returns. Value and momentum returns correlate more strongly across asset classes than passive exposures to the asset classes, but value and momentum are negatively correlated with each other, both within and across asset classes. Our results indicate the presence of common global risks that we characterize with a three-factor model. Global funding liquidity risk is a partial source of these patterns, which are identifiable only when examining value and momentum jointly across markets. Our findings present a challenge to existing behavioral, institutional, and rational asset pricing theories that largely focus on U.S. equities. 
> 
> TWO OF THE MOST studied capital market phenomena are the relation between an asset’s return and the ratio of its “long-run” (or book) value relative to its current market value, termed the “value” effect, and the relation between an asset’s return and its recent relative performance history, termed the “momentum” effect. The returns to value and momentum strategies have become central to the market efficiency debate and the focal points of asset pricing studies, genera

## Methodology

Based on the provided text, here is a structured synthesis of the trading strategy methodology.

**Core Trading Idea:** The paper implements **cross-sectional value and momentum factor strategies** across eight diverse asset classes. The core idea is to rank assets within each class based on standardized value and momentum signals, then go long the assets deemed "cheap" (high value) or "winners" (high momentum) and short those deemed "expensive" (low value) or "losers" (low momentum).

**Signal Generation and Portfolio Formation Process:** For each asset within an asset class at a given monthly rebalancing point, two signals are calculated:
1.  **Value Signal:** Defined uniformly as a measure of long-term cheapness.
    *   For **individual stocks**: Book-to-Market ratio (*BE/ME*), using book value lagged 6 months.
    *   For **country equity indices**: *BE/ME* of the MSCI country index.
    *   For **commodities**: Negative of the 5-year spot return. Specifically, `log(avg spot price 4.5-5.5 years ago / current spot price)`.
    *   For **currencies**: Negative of the 5-year real exchange rate return, adjusting for purchasing power parity (PPP).
    *   For **government bonds**: Negative of the 5-year return, approximated by the 5-year change in 10-year bond yields.
2.  **Momentum Signal:** Defined uniformly across all asset classes as the past 12-month cumulative return, skipping the most recent month (*MOM2–12*). This exclusion is to avoid short-term reversals.

**Portfolio Construction and Rebalancing:** Each month, assets within an asset class are ranked separately based on their value and momentum signals. The strategy constructs **zero-cost, dollar-neutral portfolios** by going long the top 30% (winners/cheap) and short the bottom 30% (losers/expensive) of the ranked assets. The paper uses **equal weighting** within the long and short sides. The portfolios are **rebalanced monthly**. This process is repeated independently for the value strategy and the momentum strategy within each of the eight asset classes.

**Strategy Type and Key Details:** This is fundamentally a **cross-sectional strategy**—assets are ranked relative to each other within their asset class at each point in time. The strategy is applied globally but implemented locally within each class. Key parameter values are: the **30th/70th percentile breakpoints** for portfolio formation, a **12-month formation period for momentum** (skipping month t-1), and a **5-year lookback for the value signal** in non-stock asset classes. The paper also combines the value and momentum portfolios into a single "combo" portfolio, which is a simple **equal-weighted average of the two strategy returns**, leveraging their negative correlation.

## Data Description

Based on a thorough extraction from the provided text, here are the precise data requirements and sample description for the paper "Value and Momentum Everywhere."

### 1. **Data Sources**
*   **CRSP**: For U.S. individual stock prices, returns, and share codes.
*   **Compustat**: For U.S. individual stock book values.
*   **Datastream**: For individual stock data (prices, returns) in the UK, Europe, and Japan, and for spot exchange rates for currencies.
*   **Worldscope**: For book values of individual stocks outside the U.S. (UK, Europe, Japan).
*   **MSCI**: For country equity index returns, price data, and book values. Also used for some currency spot price data.
*   **Bloomberg**: For country equity index futures data, government bond index returns, short rates, 10-year government bond yields, and some commodity futures data.
*   **Morgan Markets**: For government bond index returns.
*   **Consensus Economics**: For inflation forecasts (used in currency value measure).
*   **Futures Exchanges**: Specific commodity futures data from:
    *   London Metal Exchange (LME)
    *   Intercontinental Exchange (ICE)
    *   Chicago Mercantile Exchange (CME)
    *   Chicago Board of Trade (CBOT)
    *   New York Mercantile Exchange (NYMEX)
    *   New York Commodities Exchange (COMEX)
    *   New York Board of Trade (NYBOT)
    *   Tokyo Commodity Exchange (TOCOM)
*   **Libor rates**: Used in computing currency returns.

### 2. **Asset Universe**
The study covers **eight distinct markets/asset classes**:
1.  **U.S. Individual Stocks**: All common equity (CRSP sharecodes 10 and 11) with Compustat book data.
2.  **U.K. Individual Stocks**: From Datastream.
3.  **European Individual Stocks**: All European stock markets (ex-UK) from Datastream.
4.  **Japanese Individual Stocks**: From Datastream.
5.  **Global Equity Indices**: Futures/swap on 18 developed market MSCI indices (Australia, Austria, Belgium, Canada, Denmark, France, Germany, Hong Kong, Italy, Japan, Netherlands, Norway, Portugal, Spain, Sweden, Switzerland, UK, US).
6.  **Currencies**: 10 currencies (Australia, Canada, Germany/Euro, Japan, New Zealand, Norway, Sweden, Switzerland, UK, US).
7.  **Global Government Bonds**: 10 countries (Australia, Canada, Denmark, Germany, Japan, Norway, Sweden, Switzerland, UK, US).
8.  **Commodity Futures**: 27 commodities from various exchanges (Aluminum, Copper, Nickel, Zinc, Lead, Tin, Brent Crude, Gas Oil, Live Cattle, Feeder Cattle, Lean Hogs, Corn, Soybeans, Soy Meal, Soy Oil, Wheat, WTI Crude, RBOB Gasoline, Heating Oil, Natural Gas, Gold, Silver, Cotton, Coffee, Cocoa, Sugar, Platinum).

### 3. **Time Period**
*   **Overall Sample End**: July 2011 for all series.
*   **Sample Start Dates by Asset Class**:
    *   **U.S. & U.K. Stocks**: January 1972
    *   **Europe & Japan Stocks**: January 1974
    *   **Global Equity Indices**: January 1978
    *   **Currencies**: January 1979
    *   **Global Government Bonds**: January 1982
    *   **Commodity F

*(truncated)*

## Signal Logic

Based on the paper "Value and Momentum Everywhere" by Asness, Moskowitz, and Pedersen (2013), here are the precise trading rules and signal logic extracted from the text.

### 1. **Entry Conditions**
*   **Value Strategy (Long Entry)**: Buy assets with the highest value signal (cheapest) within each asset class.
*   **Momentum Strategy (Long Entry)**: Buy assets with the highest momentum signal (highest past returns) within each asset class.
*   **Combined Strategy (Long Entry)**: A simple equal-weighted combination of the value and momentum strategies.

### 2. **Exit Conditions**
*   **Time-Based Exit**: Positions are held until the next scheduled monthly rebalancing. There is no explicit stop-loss, take-profit, or signal-reversal exit condition within the holding period.

### 3. **Technical Indicators**
*   **Momentum Signal (`MOM2-12`)**: The cumulative raw return over the past 12 months, skipping the most recent month. Calculation: `Cumulative Return from month t-12 to t-2`.
*   **Value Signal (for Commodities, Currencies, Bonds)**: Uses a long-term past return as a proxy.
    *   **Commodities**: Negative of the 5-year spot return. `Value = log(Avg_Spot_Price_{t-5.5y to t-4.5y}) - log(Spot_Price_t)`.
    *   **Currencies**: Negative of the 5-year exchange rate return, adjusted for purchasing power parity (PPP). `Value = [log(Avg_Spot_{t-5.5y to t-4.5y}) - log(Spot_t)] - Δlog(CPI_foreign/USA)_{5y}`.
    *   **Bonds**: 5-year change in the yields of 10-year government bonds (similar to negative past return).

### 4. **Fundamental Factors**
*   **Value Signal (for Stocks and Equity Indices)**: Book-to-Market ratio (`BE/ME`).
    *   **Individual Stocks**: Book value of equity divided by market value of equity. Book values are lagged 6 months to ensure availability.
    *   **Country Equity Indices**: Previous month's `BE/ME` ratio for the MSCI country index.

### 5. **Sorting/Ranking Procedures**
*   **Procedure**: Independent, cross-sectional sorts within each asset class.
*   **Number of Groups**: Assets are sorted into **quintile portfolios** (5 groups) based on the signal (value or momentum).
*   **Breakpoint Methodology**: Breakpoints are determined using all assets within the specific asset class at the time of formation.
*   **Portfolio Definition**:
    *   **Long Leg**: Quintile of assets with the highest signal (high `BE/ME` for value, high `MOM2-12` for momentum).
    *   **Short Leg**: Quintile of assets with the lowest signal (low `BE/ME` for value, low `MOM2-12` for momentum).
    *   **Zero-Cost Factor**: A long-short, value-weighted portfolio (High minus Low).

### 6. **Threshold Values**
*   **Ranking Cutoffs**: Top 20% (quintile) and bottom 20% (quintile) of the cross-sectional distribution within each asset class. No absolute numeric thresholds or z-score boundaries are used.

### 7. **Holding Period and Rebalancing**
*   **Holding Period**: **One month**.
*   **Rebalancing Frequency**: Portfolios are reformed **monthly**. Al

*(truncated)*

---
*Full text: 218,119 chars*
