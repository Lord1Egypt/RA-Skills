# Pairs trading  does volatility timing matter 

> **==> picture [94 x 126] intentionally omitted <==**
> 
> ## **Applied Economics** 
> 
> **ISSN: 0003-6846 (Print) 1466-4283 (Online) Journal homepage: www.tandfonline.com/journals/raec20** 
> 
> **==> picture [73 x 21] intentionally omitted <==**
> 
> ## **Pairs trading: does volatility timing matter?** 
> 
> ## **Nicolas Huck** 
> 
> **To cite this article:** Nicolas Huck (2015) Pairs trading: does volatility timing matter?, Applied Economics, 47:57, 6239-6256, DOI: 10.1080/00036846.2015.1068923 
> 
> **To link to this article:** https://doi.org/10.1080/00036846.2015.1068923 
> 
> **==> picture [18 x 19] intentionally omitted <==**
> 
> **==> picture [19 x 15] intentionally omitted <==**
> 
> **==> picture [21 x 16] intentionally omitted <==**
> 
> **==> picture [17 x 19] intentionally omitted <==**
> 
> **==> picture [20 x 21] intentionally omitted <==**
> 
> **==> picture [19 x 19] intentionally omitted <==**
> 
> Published online: 24 Jul 2015. 
> 
> **==> picture [14 x 10] intentionally omitted <==**
> 
> Submit your article to this journal 
> 
> Article views: 1404 
> 
> **==> picture [14 x 10] intentionally omitted <==**
> 
> View related articles 
> 
> **==> picture [14 x 10] intentionally omitted <==**
> 
> View Crossmark data 
> 
> **==> picture [14 x 10] intentionally omitted <==**
> 
> Citing articles: 9 View citing articles 
> 
> Full Terms & Conditions of access and use can be found at https://www.tandfonline.com/action/journalInformation?journalCode=raec20 
> 
> 
> 
> Applied Economics, 2015 Vol. 47, No. 57, 6239–6256, http://dx.doi.org/10.1080/00036846.2015.1068

## Methodology

**Core Trading Idea:**  
This is a **pairs trading** strategy, a dollar-neutral, relative-value approach that exploits temporary deviations from a long-term equilibrium relationship between two stocks. The strategy is fundamentally **mean-reverting**—it goes long the relatively undervalued stock and short the relatively overvalued stock when their prices diverge, expecting convergence.

**Step-by-Step Process & Signal Generation:**  
The strategy operates in a two-phase, rolling-window framework. First, during a **formation period** (either 12 or 24 months, i.e., 252 or 504 trading days), pairs are selected from the components of a major index (S&P 500 or Nikkei 225). Three distinct selection methods are tested:  
1. **Minimum Distance:** For each stock, find the partner that minimizes the sum of squared differences (SSD) of normalized price series. The top 20 pairs with the lowest SSD are selected.  
2. **Stationarity (ADF Test):** Select the 20 pairs with the lowest ADF t-statistics for the price ratio, indicating the strongest rejection of a unit root (i.e., most stationary spread).  
3. **Cointegration (Johansen Test):** Using the Johansen procedure with optimal lag length selection (up to 10 lags), select the 20 pairs with the highest trace statistics, indicating a stable long-run relationship.  

A pre-filter is applied: pairs whose total return difference over the formation period exceeds 10% (20% for cointegration on the Nikkei 225) are discarded. After selection, pairs enter a **6-month trading period** (126 trading days). During this period, a trade is triggered when the normalized price spread (recalculated at the start of trading) diverges by more than a threshold—**2 or 3 standard deviations** of the spread estimated during the formation period. The position is closed when the spread converges to zero or at the end of the 6-month period, whichever comes first. This entire formation/trading cycle repeats every 21 trading days (~monthly).

**Portfolio Construction & Rebalancing:**  
The overall portfolio consists of six overlapping sub-portfolios staggered by one month, as each selected pair has a 6-month trading lifespan. The portfolio is **equal-weighted** across all active pairs on a given day. It is **dollar-neutral**: for each pair, $1 is short the "winner" (overvalued stock) and $1 is long the "loser" (undervalued stock). Daily portfolio returns are computed as the mean return of all active pairs. If fewer than 10 pairs are active, the "missing" positions are filled with a long position in the equity market premium (S&P 500 premium for the U.S., Topix index return minus risk-free rate for Japan) to maintain full investment. Transaction costs are incorporated as 30 bps round-trip (commissions + market impact) plus a 1% annual short-selling fee.

**Strategy Type & Key Formulas:**  
This is primarily a **time-series strategy** for each individual pair (trading based on the deviation of its own historical spread), but the portfolio c

*(truncated)*

## Data Description

Based on a thorough review of the provided text, here are the precise data requirements and sample description extracted from the paper "Pairs trading: does volatility timing matter?" by Nicolas Huck (2015).

### 1. **Data Sources**
*   **Primary Source:** Bloomberg.
*   **Supporting Source:** Kenneth French's data library (for the U.S. equity premium).

### 2. **Asset Universe**
*   **United States:** Components of the S&P 500 index.
*   **Japan:** Components of the Nikkei 225 index.
*   **Note:** The paper considered but explicitly excluded European indices (EuroStoxx 600, Bloomberg European 500) due to data synchronization issues across exchanges.

### 3. **Time Period**
*   **Formation & Trading Period:** The trading results cover **10 years (120 months) from July 2003 to June 2013**.
*   **Formation Windows:** Mobile windows of 12 months (252 trading days) and 24 months (504 trading days) are used for pair selection, rolled forward every 21 trading days (~1 month).
*   **Trading Windows:** A fixed 6-month (126 trading days) eligibility/trading period follows each formation period.

### 4. **Data Frequency & Type**
*   **Frequency:** Daily data.
*   **Data Type:** Stock prices **adjusted for dividends and splits**. Returns are computed from these prices.

### 5. **Selection/Filter Criteria**
*   **Liquidity Focus:** Selection is limited to large-cap components of major indices to ensure liquidity.
*   **Pre-Selection Filter (Cream-Skimming):** To reduce computational load, pairs are pre-filtered based on return co-movement during the formation period.
    *   **For Distance & Stationarity methods:** A pair is discarded if the total return difference between the two stocks exceeds **10%**.
    *   **For Cointegration method only (Nikkei 225):** A less restrictive filter of **20%** is applied to ensure a large enough candidate pool.
*   **Portfolio Minimum:** If fewer than 10 pairs are active on a given day, the portfolio is filled with a long position in the market premium to maintain diversification.

### 6. **Fundamental Data Fields**
*   **None mentioned.** The strategy is purely statistical/price-based and does not utilize fundamental accounting variables.

### 7. **Alternative Data**
*   **Volatility Index:** The CBOE Volatility Index (**VIX**) is used to condition trades and analyze performance.
*   **Risk-Free Rates:**
    *   **U.S.:** Implied from the equity premium data from Kenneth French's library.
    *   **Japan:** The **Japan Central Bank discount rate** is used as the risk-free rate.
*   **Benchmark Indices (for premium calculation):**
    *   **U.S.:** The market return from Kenneth French's data library.
    *   **Japan:** The **Topix index (TPXDDVD)** return, inclusive of dividends.

### 8. **Benchmark**
*   **Primary Benchmark:** The strategy's performance is measured as **excess returns** (alpha) over the relevant equity market premium.
*   **Factor Model Benchmark:** Returns are also analyzed against a **six-factor model*

*(truncated)*

## Signal Logic

Based on the provided text, here is a precise extraction of the trading rules and signal logic for the pairs trading strategies described in the paper.

### **1. Entry Conditions**
A long-short position in a pair is initiated when the following condition is met:
*   **Trigger:** The normalized price difference (spread) between the two stocks diverges by more than a specified number of standard deviations from its equilibrium state.
*   **Threshold:** The opening trigger is **2 or 3** standard deviations (σ). The paper tests both values.
*   **Position:** Go **long** the "loser" (the relatively undervalued stock) and **short** the "winner" (the relatively overvalued stock) in a **dollar-neutral** manner (one dollar short, one dollar long).

### **2. Exit Conditions**
Positions are closed under one of two conditions:
*   **Convergence:** The spread returns to its equilibrium (mean reverts).
*   **Time-based:** At the end of the **6-month trading period** (126 trading days), all positions are closed out.

### **3. Technical Indicators & Statistical Models**
The core of the strategy is the modeling of the spread. The paper tests three distinct selection/equilibrium modeling methods:

**A. Minimum Distance Method (Gatev et al., 2006)**
*   **Indicator:** Sum of Squared Differences (SSD) of normalized prices.
*   **Calculation:** Over the formation period (T days): `SSD = Σ_{t=1 to T} (P_t^i - P_t^j)^2`, where `P_t^i` and `P_t^j` are normalized prices for stocks *i* and *j* on day *t*, scaled to $1 at the start of the formation period.
*   **Selection:** For each stock, the partner is the stock that minimizes the SSD. The top 20 pairs with the lowest SSD are selected for trading.

**B. Stationarity (ADF Test)**
*   **Indicator:** Augmented Dickey-Fuller (ADF) test on the **price ratio** of the two stocks.
*   **Logic:** A stationary price ratio (rejecting a unit root) indicates a constant mean and volatility over time. Deviations from this mean are trading opportunities.
*   **Selection:** Each month, the eligible pairs are the **20 pairs with the lowest ADF t-statistics** (strongest rejection of the unit root).

**C. Cointegration (Johansen Test)**
*   **Indicator:** Johansen (1988) cointegration test (trace statistic).
*   **Logic:** Cointegrated stocks share a long-term equilibrium relationship. The spread (residuals from the cointegrating regression) is mean-reverting.
*   **Procedure:**
    1.  For each pair, determine the optimal lag length using a likelihood ratio test (up to 10 lags).
    2.  Perform the Johansen cointegration test.
*   **Selection:** Select the **top 20 cointegrated pairs with the highest trace statistics**.

### **4. Fundamental Factors**
*   **Not Applicable.** The strategy is purely statistical/technical, based on price history. No accounting ratios or fundamental factors are used for pair selection or trading signals.

### **5. Sorting/Ranking Procedures**
*   **Procedure:** A monthly ranking and selection process.
*   **S

*(truncated)*

---
*Full text: 70,305 chars*
