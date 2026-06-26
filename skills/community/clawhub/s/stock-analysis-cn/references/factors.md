# Factor Investing Reference

## What Are Factors?

Factors are systematic sources of return that explain stock performance across markets. Common factors include value, momentum, quality, low volatility, and size.

## Major Factor Categories

### 1. Value
**Hypothesis**: Cheap stocks outperform expensive ones over the long term.

**Metrics**:
- **PE (Price/Earnings)**: Lower = better
- **PB (Price/Book)**: Lower = better
- **PS (Price/Sales)**: Lower = better
- **Dividend Yield**: Higher = better
- **EV/EBITDA**: Lower = better

**Construction**:
- Rank stocks by each metric (ascending)
- Combine ranks into composite value score
- Top quintile = "value" portfolio, bottom = "growth"

**Caveats**:
- Value traps: cheap for a reason (fundamental deterioration)
- Value underperforms during growth-led bull markets

---

### 2. Quality
**Hypothesis**: High-quality companies deliver superior risk-adjusted returns.

**Metrics**:
- **ROE (Return on Equity)**: Higher = better (>15% typically)
- **ROA (Return on Assets)**: Higher = better
- **Debt/Equity**: Lower = better (<50% ideal)
- **Operating CF / Net Income**: >1 = high quality earnings
- **Earnings stability** (low volatility of profits)

**Construction**:
- Focus on profitability + low leverage + stable earnings
- Quality tends to be defensive (lower beta, lower drawdown)

---

### 3. Momentum
**Hypothesis**: Stocks that have performed well recently continue to perform well.

**Metrics**:
- **Price momentum**: 12-month return (skip most recent month)
- **Earnings momentum**: Latest EPS surprise vs prior quarters
- **Relative strength**: Rank by performance vs market

**Construction**:
- Rank by 12-month total return (excluding most recent month)
- Hold for 3-6 months then rebalance
- Transaction costs can eat profits

**Caveats**:
- Momentum crashes: reverses sharply during market stress
- Combine with quality/value to mitigate risk

---

### 4. Low Volatility
**Hypothesis**: Lower risk stocks have higher risk-adjusted returns.

**Metrics**:
- **Historical volatility**: Std dev of daily returns (past 1-3 years)
- **Beta**: Covariance with market index
- **Max drawdown**: Large historical declines

**Construction**:
- Rank stocks by volatility (ascending) or beta (ascending)
- Low-vol portfolio often has lower returns but much better Sharpe ratio

**Note**: Contradicts CAPM (higher risk should be compensated)

---

### 5. Size
**Hypothesis**: Small-cap stocks outperform large-cap over the long term.

**Metric**: Market cap (free float)
- Small: bottom 20% by market cap
- Large: top 20%

**Caveats**:
- Higher transaction costs for small caps
- Higher failure rate
- Size premium has diminished since 1990s

---

### 6. Dividend
**Hypothesis**: High-dividend stocks provide income and capital preservation.

**Metrics**:
- **Dividend yield**: Annual dividend / price
- **Payout ratio**: Dividends / earnings (<60% sustainable)
- **Dividend growth**: Consistent dividend increases

**Risk**: Dividend cuts can cause sharp declines

---

## Multi-Factor Models

### Combining Factors

**Approaches**:
1. **Top-N by each factor, then intersection** (strict, small universe)
2. **Composite scoring** (weighted sum of factor ranks)
3. **Tilt**: Start with market cap weighted, tilt toward factors

**Factor Timing**:
- Factors cycle; no factor wins forever
- Use long-term averages or valuation signals to tilt exposures
- Example: Value cheap relative to growth → overweight value

---

## Factor Data Sources

- **A-shares**: CSI (中证指数公司) publishes factor indices (300 Value, 300 Quality, etc.)
- ** ETFs**: Many factor ETFs available (e.g., 519310 股息ETF, 562500 消费50ETF)
- **Wind / iFinD**: Comprehensive factor data (paid)
- **Free**: Eastmoney, JoinQuant (聚宽) provide some factor metrics

---

## Practical Application for ETF Selection

When selecting ETFs for factor exposure:

1. **Identify target factor** (e.g., value, low vol)
2. **Find tracking index**: Does CSI/S&P/MSCI have a factor index? → Yes = good
3. **Check ETF replication method**: Full sampling vs optimized
4. **Liquidity**: Daily volume > 1000万元, AUM > 5亿元
5. **Tracking error**: Should be < 3% annually
6. **Fees**: Management fee < 0.50% preferable

**Example**:
- Want value exposure → CSI 300 Value Index (000919) → ETFs tracking it
- Want low volatility → CSI 300 Low Volatility Index (000960) → ETFs

---

## Common Factor ETFs in A-share Market

| Factor | Index Code | Example ETF | Characteristics |
|--------|------------|-------------|-----------------|
| 价值 | 000919 (300 Value) | 禁止 (需要查找) | Low PE, PB |
| 质量 | 930707 (300 Quality) | 禁止 | High ROE, low debt |
| 红利 | 000922 (红利指数) | 510880 (红利ETF) | High dividend |
| 低波 | H30365 (300LowVol) | 512890 (红利低波) | Low volatility |
| 成长 | 000949 (300Growth) | 159915 (创业板) | High growth |

---

## Factor Performance Cycles

| Period | Leading Factors |
|--------|-----------------|
| Bull market (growth-driven) | Momentum, Growth |
| Bull market (value-driven) | Value, Dividend |
| Bear market / recession | Quality, Low Volatility, Dividend |
| Recovery | Value, Small Size |
| Stagflation | Commodities, Value |

**Current cycle判断 (需结合市场环境)**:
- 2024-2025: Quality + Low Volatility leadership in early cycle, shifting to Value/Growth in expansion

---

## Portfolio Construction with Factors

**Core-Satellite Approach**:
- **Core (60%)**: Broad market ETF (沪深300, 中证500)
- **Satellite (40%)**: Factor tilts based on outlook
  - Example: 20% Quality, 10% Value, 10% Low Volatility

**Rebalancing**:
- Annual factor review (valuation and performance)
- Rebalance to target allocations if drift > 5%

---

## References

- Fama, K. (1992). "The Cross-Section of Expected Stock Returns"
- Asness, S. (2012). "Factor Investing"
- CSI Factor Index Methodology (中证指数公司因子编制手册)
