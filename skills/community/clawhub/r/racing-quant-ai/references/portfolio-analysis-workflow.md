# Portfolio Deep Analysis Workflow

> Reusable procedure for analyzing a user's full portfolio of A-share stocks and ETFs,
> producing a structured buy/sell recommendation report.

## 1. Data Collection (parallel where possible)

> 🔴 **数据校验铁律**：严禁编造任何具体数值。数据获取失败时必须如实标注"数据获取失败"。数据源优先级：Tushare MCP > new-akshare-stock > baostock > 东方财富API。

### 1a. Real-time Quotes
- **Primary: Tushare MCP** - `daily_basic` for latest price, PE/PB, turnover, market cap; `daily` for OHLCV
- **Fallback 1: akshare** - `fund_etf_spot_em()` for ETFs; `stock_zh_a_hist()` for stocks
- **Fallback 2: baostock** - `query_history_k_data_plus()` with `adjustflag="2"` (forward-adjusted), last 60+ trading days
  - Compute: latest price, pctChg, open/high/low, volume, turnover, PE(TTM), PB(MRQ).

### 1b. Financial Data
- **Primary: Tushare MCP** - `fina_indicator` for ROE, net margin, gross margin; `income` for revenue/profit
- **Fallback 1: akshare** - `stock_financial_abstract_ths(symbol, indicator="按年度")` - last 4 rows
- **Fallback 2: baostock** - `query_profit_data()` + `query_growth_data()`

### 1c. Fund Flow
- **Primary: Tushare MCP** - `moneyflow` for daily main capital flow
- **Fallback 1: akshare** - `stock_individual_fund_flow(stock=code, market="sz")` - last 10 days
- **Fallback 2: baostock** - not available; use akshare or web search

### 1d. News
- `akshare.stock_news_em(symbol=code)` — last 5 headlines.
  - Extract sentiment signals: earnings, orders, policy, concept rotation.

### 1e. Technical Indicators (compute from K-line)
- MA5 / MA10 / MA20 / MA60 — trend alignment.
- MACD (DIF, DEA, MACD histogram) — golden/death cross.
- Period returns: 5d, 1m, 3m, 1y.

## 2. Analysis Framework (per holding)

### For Individual Stocks (5 dimensions per racing-quant-ai skill):
1. **Core Trading Data** — price, change, volume, turnover, PE, PB, market cap.
2. **Price Trend Review** — multi-period returns (5d/1m/3m/1y).
3. **Fund Flow Analysis** — net inflow/outflow trend, price-flow divergence.
4. **Fundamental Analysis** — valuation vs peers, earnings growth, business drivers, risks.
5. **Comprehensive Assessment** — bullish/bearish verdict, support/resistance, investor-type advice.

### For ETFs (3 dimensions):
1. **Trend & Technical** — MA alignment, MACD, period returns.
2. **Underlying Driver** — what drives the index (e.g., AI capex for Nasdaq, geopolitics for Gold).
3. **Verdict** — hold / add / reduce with key level.

## 3. Report Structure

```
# Portfolio Deep Analysis Report
Date | Data cutoff

## Individual Stocks
[Per stock: data table → bull case → bear case → verdict with key levels]

## ETFs
[Per ETF: data table → analysis → verdict]

## Summary Table
| Ticker | Verdict | Action |
[All holdings in one view]

## Portfolio Diagnosis
- Concentration issues
- Style mismatch
- Defense/offense balance

## Optimization Suggestions
- Priority reductions / additions

## Disclaimers
- Data source annotation
- Investment risk disclaimer
```

## 4. Pitfalls

- **🔴 数据校验铁律**：严禁编造任何具体数值。数据获取失败时如实标注"数据获取失败"。Tushare MCP 不可用时降级至 akshare/baostock，但降级也失败时绝不用估算值替代。
- **Tushare MCP 工具未注册**：Gateway 重启后才能发现 MCP 工具。若当前会话无 `mcp_tushareMcp_*` 工具，说明 MCP 未连接，直接使用 akshare/baostock 降级数据源。
- **Tushare 日期格式差异**：Tushare 使用 `YYYYMMDD`，akshare/baostock 使用 `YYYY-MM-DD`，调用时注意转换。
- **Do NOT use `delegate_task` for web search** - sub-agents often fail to call web_fetch. Do searches in the main session.
- **akshare spot data may be empty for some ETFs** — always cross-check with baostock K-line.
- **Gold price APIs are unreliable** — use 黄金ETF (518880) K-line as proxy.
- **US index data (`index_us_stock_sina`) returns 20+ years** — always `.tail()` to avoid memory issues.
- **Write Python scripts to /tmp/ and run with venv python** — inline `-c` with complex code fails due to shell quoting.
