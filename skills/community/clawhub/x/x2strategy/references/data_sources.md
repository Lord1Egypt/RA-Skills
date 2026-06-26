# Data Sources Reference

> Sources: ranaroussi.github.io/yfinance/ (official API reference & CHANGELOG),
> akshare.akfamily.xyz/data/stock/stock.md (official documentation).

Guide for generating data-fetching code. Covers yfinance and akshare APIs.

## yfinance (US/Global Markets)

### `yf.download()` — Full Signature (from official docs)

```python
yfinance.download(
    tickers,                  # str or list — "AAPL" or ["AAPL", "MSFT"]
    start=None,               # str/datetime — inclusive start date
    end=None,                 # str/datetime — EXCLUSIVE end date (!)
    actions=False,            # bool — include dividends/splits columns
    threads=True,             # bool/int — parallel downloads
    ignore_tz=None,           # bool — ignore timezone
    group_by='column',        # str — 'column' or 'ticker'
    auto_adjust=True,         # bool — adjust OHLC for splits/dividends (DEFAULT since v1.0)
    back_adjust=False,        # bool — back-adjusted data
    repair=False,             # bool — repair bad data
    keepna=False,             # bool — keep NaN rows
    progress=True,            # bool — show progress bar
    period=None,              # str — alternative to start/end (see values below)
    interval='1d',            # str — data frequency (see values below)
    prepost=False,            # bool — include pre/post market data
    rounding=False,           # bool — round to 2 decimal places
    timeout=10,               # int — request timeout in seconds
    session=None,             # requests.Session — custom session
    multi_level_index=True,   # bool — MultiIndex columns (EVEN for single ticker!)
)
```

**period values**: `1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max`
**interval values**: `1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo`
**Intraday limit**: Max 60 days of intraday data.

### Critical yfinance Behaviors

1. **`end` date is EXCLUSIVE**: `end='2024-01-01'` fetches up to 2023-12-31.
   To include Jan 1, use `end='2024-01-02'`.
2. **`multi_level_index=True` by default** (since v0.2.47): Returns MultiIndex
   columns `(Price, Ticker)` even for a SINGLE ticker. Set `multi_level_index=False`
   or flatten with `df.droplevel(1, axis=1)`.
3. **`auto_adjust=True` by default** (since v1.0): OHLC are already adjusted.
   The `Adj Close` column is redundant. Not specifying this explicitly may
   trigger deprecation warnings.
4. **Output columns** (with auto_adjust=True): `Open, High, Low, Close, Volume`
   (no `Adj Close`).

### Single Symbol — Correct Pattern
```python
import yfinance as yf

df = yf.download('AAPL', start='2020-01-01', end='2024-01-02',
                 auto_adjust=True, multi_level_index=False)
# Columns: Open, High, Low, Close, Volume
# Index: DatetimeIndex (timezone-aware)
```

### Multiple Symbols
```python
df = yf.download(['AAPL', 'MSFT', 'GOOGL'], start='2020-01-01', end='2024-01-02',
                 auto_adjust=True, multi_level_index=True)
# Returns MultiIndex columns: (Price, Symbol)
# Access single: df[('Close', 'AAPL')]  or  df['Close']['AAPL']

# For per-symbol DataFrames:
for sym in ['AAPL', 'MSFT', 'GOOGL']:
    sym_df = df.xs(sym, level=1, axis=1)  # Single-level columns
```

### Common Tickers
| Asset Class | Examples |
|-------------|----------|
| US Equities | AAPL, MSFT, GOOGL, AMZN, TSLA, JPM |
| ETFs | SPY, QQQ, IWM, TLT, GLD, XLF |
| Indices | ^GSPC (S&P500), ^DJI (Dow), ^IXIC (Nasdaq) |
| Forex | EURUSD=X, GBPUSD=X, JPYUSD=X |
| Crypto | BTC-USD, ETH-USD |

### `yf.Ticker` — Key Attributes
```python
ticker = yf.Ticker('AAPL')
ticker.info                # dict — P/E, market cap, sector, etc.
ticker.history(period='1y') # DataFrame — OHLCV + Dividends + Stock Splits
ticker.balance_sheet       # DataFrame
ticker.income_stmt         # DataFrame
ticker.cashflow            # DataFrame
ticker.earnings_dates      # DataFrame
ticker.dividends           # Series
ticker.splits              # Series
ticker.recommendations     # DataFrame
```

### Key Breaking Changes (from CHANGELOG)
| Version | Change |
|---------|--------|
| v0.2.47 | Added `multi_level_index` param; MultiIndex default for download() |
| v0.2.53 | Warns if download() called without specifying `auto_adjust` |
| v1.0 | Major version — `auto_adjust=True` default; `yf.config` class added |
| v1.1.0 | Pandas 3.0 upgrade; capital gains double-counting repair |
| v1.2.0 | Latest stable release |

## akshare (China A-Share, HK, US, Macro)

### `stock_zh_a_hist` — A股历史行情 (东方财富, 推荐)

This is the **primary interface** for A-share historical data.

```python
import akshare as ak

df = ak.stock_zh_a_hist(
    symbol="000001",           # 股票代码 (不带市场前缀)
    period="daily",            # choice of {'daily', 'weekly', 'monthly'}
    start_date="20200101",     # 格式 YYYYMMDD
    end_date="20240101",       # 格式 YYYYMMDD
    adjust="qfq"              # "qfq"=前复权, "hfq"=后复权, ""=不复权
)
```

**输出列**: `日期, 股票代码, 开盘, 收盘, 最高, 最低, 成交量(手), 成交额(元), 振幅(%), 涨跌幅(%), 涨跌额, 换手率(%)`

**注意**: 成交量单位是"手"(1手=100股), 成交额单位是"元"。研究中普遍采用后复权数据。

### Rename for Backtrader
```python
import pandas as pd

df = df.rename(columns={
    '日期': 'date', '开盘': 'open', '收盘': 'close',
    '最高': 'high', '最低': 'low', '成交量': 'volume'
})
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')
```

### Other A-Share Data Sources

```python
# 新浪-A股历史 (较老接口, 易被封IP, 建议用 stock_zh_a_hist)
df = ak.stock_zh_a_daily(symbol="sz000001", start_date="20200101",
                         end_date="20240101", adjust="qfq")
# 输出列: date, open, high, low, close, volume, outstanding_share, turnover

# 腾讯-A股历史
df = ak.stock_zh_a_hist_tx(symbol="sz000001", start_date="20200101",
                           end_date="20240101", adjust="qfq")
# 输出列: date, open, close, high, low, amount(手)

# 分时数据-东财 (近期, 1/5/15/30/60分钟)
df = ak.stock_zh_a_hist_min_em(symbol="000001", period='5', adjust='qfq',
                                start_date="2024-01-01 09:30:00",
                                end_date="2024-01-05 15:00:00")
# 注意: 1分钟数据只返回近5个交易日且不复权
```

### Index Data
```python
# 指数历史行情-东财 (推荐)
df = ak.stock_zh_index_daily_em(symbol="sh000300")  # 沪深300

# 指数历史行情-新浪
df = ak.stock_zh_index_daily(symbol="sh000001")  # 上证综指

# 指数实时行情
df = ak.stock_zh_index_spot_em()  # 全部指数
```

### HK Stocks (港股)
```python
# 东财-港股历史行情 (推荐)
df = ak.stock_hk_hist(
    symbol="00700",           # 腾讯
    period="daily",
    start_date="20200101",
    end_date="20240101",
    adjust="qfq"             # qfq/hfq/""
)
# 输出列: 日期, 开盘, 收盘, 最高, 最低, 成交量(股), 成交额(港元), 振幅(%), 涨跌幅(%), 涨跌额, 换手率(%)

# 新浪-港股历史
df = ak.stock_hk_daily(symbol="00700", adjust="qfq")
```

### US Stocks (美股)
```python
# 东财-美股历史行情
df = ak.stock_us_hist(
    symbol='106.TTE',         # 代码格式: 通过 ak.stock_us_spot_em() 获取
    period="daily",
    start_date="20200101",
    end_date="20240101",
    adjust="qfq"
)
# 输出列: 日期, 开盘, 收盘, 最高, 最低, 成交量, 成交额, 振幅(%), 涨跌幅(%), 涨跌额, 换手率(%)

# 新浪-美股历史 (更直接的 symbol)
df = ak.stock_us_daily(symbol="AAPL", adjust="qfq")
# 输出列: date, open, high, low, close, volume
```

### Macro Data
```python
cpi = ak.macro_china_cpi()          # 居民消费价格指数
gdp = ak.macro_china_gdp()          # 国内生产总值
pmi = ak.macro_china_pmi()          # 采购经理人指数
lpr = ak.macro_china_lpr()          # 贷款报价利率
```

### Real-time Data (实时行情)
```python
# 东财-全部A股实时
df = ak.stock_zh_a_spot_em()
# 输出: 序号, 代码, 名称, 最新价, 涨跌幅(%), 涨跌额, 成交量(手), 成交额(元), 振幅(%), 最高, 最低, 今开, 昨收, 量比, 换手率(%), 市盈率, 市净率, 总市值(元), 流通市值(元), 涨速, 5分钟涨跌(%), 60日涨跌幅(%), 年初至今涨跌幅(%)

# 沪A股 / 深A股 / 京A股 / 科创板
df = ak.stock_sh_a_spot_em()
df = ak.stock_sz_a_spot_em()
df = ak.stock_bj_a_spot_em()
df = ak.stock_kc_a_spot_em()

# 股票代码列表
df = ak.stock_info_a_code_name()    # 输出: code, name
```

## Data Quality Checklist

When generating data-fetching code, ensure:

1. **Date range**: start < end; yfinance end is EXCLUSIVE.
2. **NaN handling**: `df.dropna()` or `df.ffill()` (pandas 2.0+, `fillna(method='ffill')` deprecated).
3. **Column naming**: Backtrader expects `open, high, low, close, volume` (case-insensitive for PandasData, but consistent is safer).
4. **Timezone**: yfinance may return tz-aware index. Remove: `df.index = df.index.tz_localize(None)`.
5. **Sorting**: Ensure ascending date: `df.sort_index(inplace=True)`.
6. **MultiIndex**: yfinance single-ticker download returns MultiIndex since v0.2.47. Flatten it.
7. **akshare units**: 成交量=手(×100=股), 成交额=元, 涨跌幅/换手率/振幅=%.

## Backtrader Data Feed Creation

### From yfinance DataFrame
```python
import backtrader as bt
from datetime import datetime

# After download with multi_level_index=False and tz removal
data = bt.feeds.PandasData(
    dataname=df,
    fromdate=datetime(2020, 1, 1),
    todate=datetime(2024, 1, 1),
)
```

### From akshare DataFrame (after column rename)
```python
data = bt.feeds.PandasData(
    dataname=df,
    datetime=None,  # Use index
    open='open', high='high', low='low',
    close='close', volume='volume',
    openinterest=-1,
)
```

### From CSV
```python
data = bt.feeds.GenericCSVData(
    dataname='data.csv',
    dtformat='%Y-%m-%d',
    datetime=0, open=1, high=2, low=3, close=4, volume=5,
    openinterest=-1,
)
```
