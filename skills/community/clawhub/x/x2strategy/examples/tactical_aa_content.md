# A Quantitative Approach to Tactical Asset Allocation

> ## **A Quantitative Approach to Tactical Asset Allocation** 
> 
> ## Mebane T. Faber 
> 
> May 2006, Working Paper Spring 2007, _The Journal of Wealth Management_ February 2009, Update February 2013, Update 
> 
> ## **ABSTRACT** 
> 
> In this paper we update our 2006 white paper “A Quantitative Approach to Tactical Asset Allocation” with new data from the 2008-2012 period. How well did the purpose of the original paper - to present a simple quantitative method that improves the risk-adjusted returns across various asset classes – hold up since publication?  Overall, we find that the models have performed well in real-time, achieving equity like returns with bond like volatility and drawdowns. We also examine the effects of departures from the original system including adding more asset classes, introducing various portfolio allocations, and implementing alternative cash management strategies. 
> 
> _Mebane T. Faber Cambria Investment Management, LP 2321 Rosecrans Ave., Suite 3225 El Segundo, CA 90245 310-683-5500_ 
> 
> E-mail: mf@cambriainvestments.com www.cambriainvestments.com 
> 
> Copyright Mebane Faber Research 2013 
> 
> 1 
> 
> Electronic copy available at: https://ssrn.com/abstract=962461 Electronic copy available at: http://ssrn.com/abstract=962461 
> 
> 
> 
> Cambria Investment Management has been managing investments for individuals and institutions since 2007. To learn more about all of our investment offerings, please contact us for more information: 
> 
> Phone: 310-683-5500 Email: **info@cambriainvestments.

## Methodology

Based on the provided text, the core trading strategy is a **time-series trend-following (momentum) strategy** applied across multiple asset classes. It uses a simple moving average crossover rule to tactically allocate between risky assets and cash.

The strategy's signal generation and portfolio construction process is as follows:
1.  **Signal Generation (per asset class):** For each asset, at the end of every month, compare its monthly closing price (total return) to its 10-month simple moving average (SMA). The rules are purely mechanical:
    *   **Buy/Long Signal:** If the monthly price > 10-month SMA, take a long position in the asset.
    *   **Sell/Cash Signal:** If the monthly price < 10-month SMA, exit the asset and move the allocated capital to cash (simulated by 90-day Treasury bill returns).
2.  **Portfolio Construction:** The strategy is implemented as a **long-only, multi-asset portfolio** called Global Tactical Asset Allocation (GTAA). The base portfolio consists of five equally weighted (20% each) asset classes: US Large Cap (S&P 500), Foreign Developed Stocks (MSCI EAFE), US 10-Year Government Bonds, Commodities (GSCI), and Real Estate (NAREIT). Each asset class is treated independently; its 20% allocation is either fully invested in that asset or fully in cash based on its own signal. There is no shorting.
3.  **Rebalancing:** The portfolio is evaluated and signals are acted upon **monthly**, on the last day of the month. This results in low turnover, averaging less than one round-trip trade per asset class per year. The portfolio is typically 60%-100% invested in risky assets, with an average of 70% invested over time.

The strategy is explicitly a **time-series strategy**, as the trading signal for each asset is derived solely from its own price history relative to its own moving average, not from its performance relative to other assets. The key mathematical definition is the 10-month SMA, though the paper notes the strategy's robustness across a range of 3 to 12 months. The primary goal is risk management, aiming to participate in bull markets while avoiding major bear market drawdowns by switching to cash.

## Data Description

Based on a thorough review of the provided text, here are the precise data requirements and sample description extracted from Mebane Faber's "A Quantitative Approach to Tactical Asset Allocation" (2013 update).

### 1. **Data Sources**
*   **Global Financial Data (GFD)**: Primary source for total return series.
*   **Morningstar / Dimson Marsh Staunton**: Source for long-term historical return series for 16 countries (1900-2011).
*   **Cowles Commission and Standard & Poor's (S&P)**: Source for pre-1971 S&P Composite Price Index and dividend yields (used by GFD to construct the early total return series).
*   **DALBAR Studies**: Cited for data on average investor behavior and returns.

### 2. **Asset Universe**
The core analysis uses five specific asset classes, represented by the following total return indices:
*   **US Large Cap**: S&P 500 Total Return Index.
*   **Foreign Developed Stocks**: MSCI EAFE Total Return Index.
*   **US Bonds**: US 10-Year Government Bond Total Return Index.
*   **Commodities**: Goldman Sachs Commodity Index (GSCI) Total Return.
*   **Real Estate**: NAREIT Index (Real Estate Investment Trusts) Total Return.
*   **Additional Context**: The paper also references broader global asset classes (G-7 country stocks) and specific examples (German, Russian, Chinese assets) for illustrative, long-term perspective, but the core model is tested on the five above.

### 3. **Time Period**
*   **Long-Term Illustrative Charts (Cash, Bills, Bonds, Stocks)**: 1900 to 2011.
*   **S&P 500 Timing Model Test**: **January 1901 to December 2012**.
*   **Core Portfolio Analysis (GTAA Model)**: **1973 to 2012**.
*   **Out-of-Sample Test Period**: **2006 to 2012** (post-original 2005 publication).
*   **Specific CAPE Analysis**: Shiller's Cyclically Adjusted P/E Ratio (CAPE) from 1881 to 2011/2012.

### 4. **Data Frequency**
*   **Primary Model Frequency**: **Monthly**.
    *   The model is updated only on the last day of each month.
    *   All entry and exit signals are generated using month-end closing prices.
*   **Return Calculation**: All data series are **total return series** (including dividends and income).
*   **Drawdown Calculation**: Calculated on a **monthly basis**.

### 5. **Selection/Filter Criteria**
*   **Price-Based Only**: The model uses only price data (via the moving average) for signals. No fundamental filters (e.g., market cap, price) are applied to the indices themselves.
*   **Asset Class Independence**: Each of the five asset classes in the portfolio is treated independently; the model is either long the asset or in cash with its allocated portion of funds.

### 6. **Fundamental Data Fields**
*   **Cyclically Adjusted Price-to-Earnings Ratio (CAPE)**: The 10-year version is referenced and used for valuation context (Figure 1, Figure 2), but it is **not an input** to the core tactical asset allocation model.

### 7. **Alternative Data**
*   **Macro Indicators**: 90-day Treasury Bill rates (for cash returns), broker c

*(truncated)*

## Signal Logic

Based on the provided text from Mebane Faber's "A Quantitative Approach to Tactical Asset Allocation," here is a precise extraction of the trading rules and signal logic. The paper primarily describes a single, core tactical asset allocation model with several extensions and variants.

### **Core Strategy: Global Tactical Asset Allocation (GTAA) - 10-Month Moving Average Timing Model**

**1. Entry Conditions**
*   **Buy/Go Long Rule:** For each asset, at the monthly rebalance, **buy** (or remain long) if the **monthly closing price** is **greater than** the **10-month simple moving average (SMA)**.
*   **Condition:** `Monthly_Price(t) > 10-Month_SMA(t)`

**2. Exit Conditions**
*   **Sell/Close Rule:** For each asset, at the monthly rebalance, **sell** (or move to cash) if the **monthly closing price** is **less than or equal to** the **10-month simple moving average (SMA)**.
*   **Condition:** `Monthly_Price(t) <= 10-Month_SMA(t)`
*   **Note:** There are **no explicit stop-loss, take-profit, or time-based exit rules**. The only exit condition is the signal reversal from above to below the SMA.

**3. Technical Indicators**
*   **Indicator Name:** Simple Moving Average (SMA)
*   **Calculation Period:** **10 months**
*   **Parameters:** `SMA(10)` calculated on the monthly closing price series.
*   **Reference:** The paper tests parameter stability for periods from 3 to 12 months (Figure 15) but establishes `SMA(10)` as the core, non-optimized parameter.

**4. Fundamental Factors**
*   **None.** The model is explicitly **price-based only**. The paper discusses valuation (e.g., CAPE) as market context but does not incorporate it into the trading signal logic.

**5. Sorting/Ranking Procedures**
*   **Not Applicable.** The strategy does not involve cross-sectional ranking or sorting of securities. It applies the same timing rule independently to each asset class.

**6. Threshold Values**
*   **Crossover Threshold:** The exact threshold is **zero**. The rule triggers on the binary condition of price being above or below the SMA. There is no additional percentage filter (e.g., 1% above/below as mentioned in Siegel's work).

**7. Holding Period and Rebalancing**
*   **Rebalancing Frequency:** **Monthly**, on the **last day of the month**.
*   **Signal Evaluation:** The model is only updated once per month at the rebalance point. Intra-month price fluctuations are ignored.
*   **Holding Period:** Indefinite, until the exit condition is met at a monthly check. The paper notes the system is invested approximately **70% of the time** on average and makes **less than one round-trip trade per asset class per year**.

**8. Data Requirements**
*   **Price Fields:** **Monthly closing price** (total return series, including dividends).
*   **Fundamental Fields:** None.
*   **Frequency:** **Monthly**.
*   **Cash Proxy:** 90-day Treasury bill returns.
*   **Asset Classes (Core Test):**
    1.  US Large Cap: S&P 500 Total Return
    2.  Foreign Developed: MSCI EAFE Tot

*(truncated)*

---
*Full text: 48,045 chars*
