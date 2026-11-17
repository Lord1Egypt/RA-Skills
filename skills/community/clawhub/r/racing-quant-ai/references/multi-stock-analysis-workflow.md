# Multi-Stock Deep Analysis Workflow

Proven workflow for analyzing 5-10 stocks in a single session, combining baostock + akshare for maximum reliability.

## Step 1: K-Line + Technical Indicators (baostock)

Write a Python script to `/tmp/fetch_kline.py` that:
- Logs in with `bs.login()`
- Loops over stock codes, calls `bs.query_history_k_data_plus()` with `adjustflag="2"` (forward adjusted)
- Calculates: MA5/MA10/MA20/MA60, MACD (DIF/DEA/MACD), RSI(14)
- Calculates period returns: 5d, 1m, 3m, 6m, 1y
- Prints structured output per stock

**Stock code format:** `sh.600021` (沪市), `sz.300274` (创业板/深市), `sh.688525` (科创板)

**Reliable fields:** `date,code,open,high,low,close,volume,amount,pctChg,turn,peTTM,pbMRQ`

## Step 2: Financial Data (akshare)

Write to `/tmp/fetch_financial.py`:
- `ak.stock_financial_abstract_ths(symbol=code, indicator="按报告期")` — use `.tail(4)` for latest 4 quarters
- Key columns: 报告期, 净利润, 净利润同比增长率, 营业总收入, 营业总收入同比增长率, 基本每股收益, 销售净利率, 销售毛利率, 净资产收益率, 每股经营现金流

**Pitfall:** `indicator="按年度"` gives yearly data. `"按报告期"` gives quarterly but from earliest date — always use `.tail()` not `.head()`.

## Step 3: Fund Flow (akshare)

Write to `/tmp/fetch_fund.py`:
- `ak.stock_individual_fund_flow(stock=code, market="sh"/"sz")` — most reliable akshare interface
- Key columns: 日期, 收盘价, 涨跌幅, 主力净流入-净额, 主力净流入-净占比
- Use `.tail(10)` for last 10 trading days

**Pitfall:** This interface may timeout on first call after a period of inactivity. Retry once if it fails.

**Market prefix:** sh for codes starting with 6 or 68, sz for codes starting with 0 or 3.

## Step 4: News (akshare)

- `ak.stock_news_em(symbol=code)` — returns top 8 news items with timestamps
- Use `.head(8)` per stock

## Step 5: Synthesize Analysis

For each stock, output:
1. **核心数据表**: 最新价, PE, PB, 各周期涨跌幅
2. **业绩**: 净利润增速, 营收增速, 毛利率趋势, 现金流
3. **资金面**: 近10日主力净流入/流出, 大额异动标注
4. **技术面**: MA排列, MACD金叉/死叉, RSI, 关键支撑/压力位
5. **风险**: 估值泡沫, 业绩拐头, 概念退潮, 游资主导
6. **判定**: 看多/偏多/中性/偏空/看空 + 关键价位

## Common Patterns

- **PE > 100 + 净利率为负** = 极度泡沫, 偏空判定
- **Q1业绩负增长 + 放量暴跌 + 主力出逃** = 三重利空, 看空
- **PE 25-40 + 业绩正增长 + 资金持续流入** = 偏多
- **RSI > 75 + 连续涨停 + 游资龙虎榜** = 超买警告

## Feishu Doc Export

After analysis, user may request saving to Feishu cloud doc. Use `feishu-docs` skill.
- Get fresh token immediately before writing blocks (token expires ~2hrs)
- Batch 5 blocks per request, use index=-1
- Replace Unicode arrows/special chars with ASCII equivalents in Python source
- Use single quotes for strings containing Chinese double quotes
