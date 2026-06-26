---
name: xtdata
description: XtQuant行情数据模块 - 为QMT/miniQMT提供实时行情、K线、Tick、Level2和财务数据。
version: 1.2.0
homepage: http://dict.thinktrader.net/nativeApi/xtdata.html
metadata: {"clawdbot":{"emoji":"📡","requires":{"bins":["python3"]}}}
---

# XtData（XtQuant行情数据模块）

`xtdata` is the market data module of [XtQuant](http://dict.thinktrader.net/nativeApi/start_now.html), providing real-time and historical market data through the local miniQMT client.

> ⚠️ **Requires miniQMT running locally**. xtdata communicates with miniQMT via TCP to retrieve data.

## 安装

```bash
pip install xtquant
```

## 连接

```python
from xtquant import xtdata

# Connect to the local miniQMT market data service
xtdata.connect()
```

Optionally specify a data directory:

```python
# Manually specify the miniQMT data directory path
xtdata.data_dir = r'D:\QMT\userdata_mini'
```

## API分类

The xtdata API is divided into three main categories:

- **Subscription** — `subscribe_quote`, `subscribe_whole_quote`: Register real-time data callbacks; data is continuously pushed until unsubscribed
- **Retrieval** — `get_market_data_ex`, `get_local_data`, `get_full_tick`, `get_financial_data`: Read data from local cache; returns immediately
- **Download** — `download_history_data`, `download_financial_data`: Download data from the server to local cache; blocks synchronously until complete

> **Key Pattern**: When retrieving historical data, you must first `download` to local cache, then `get` from cache. For real-time data, use `subscribe`.

## 通用类型约定

- **stock_code**: `'SecurityCode.MarketCode'` format, e.g. `'600000.SH'`, `'000001.SZ'`
- **period**: `'tick'`, `'1m'`, `'5m'`, `'15m'`, `'30m'`, `'1h'`, `'1d'`, `'1w'`, `'1mon'`
- **start_time / end_time**: `'YYYYMMDDHHmmss'` or `'YYYYMMDD'` format strings
- **dividend_type**: `'none'` (no adjustment), `'front'` (forward adjustment), `'back'` (backward adjustment), `'front_ratio'` (proportional forward adjustment), `'back_ratio'` (proportional backward adjustment)

## 请求限制

- Historical data download requests are rate-limited; avoid excessive concurrent downloads.
- Batch queries (multiple stocks) are more efficient than looping one by one; batch mode is recommended.
- Full-market subscription (`subscribe_whole_quote`) may require Level2 data permissions for some data types.

---

## 下载历史数据

You must download data before retrieving it locally:

```python
# Download daily K-line data
xtdata.download_history_data('000001.SZ', '1d', start_time='20240101', end_time='20240630')

# Download 1-minute K-line data
xtdata.download_history_data('000001.SZ', '1m', start_time='20240101', end_time='20240630')

# Download Tick data
xtdata.download_history_data('000001.SZ', 'tick', start_time='20240601', end_time='20240630')
```

### 下载退市/到期合约数据

```python
# Use download_history_data2 to download data for delisted or expired contracts
xtdata.download_history_data2(['IC2312.IF'], '1d', start_time='20230101', end_time='20231231')
```

## 获取K线数据

```python
# Retrieve market data (returns a dict of DataFrames keyed by stock code)
data = xtdata.get_market_data_ex(
    [],                    # field_list, empty list means all fields
    ['000001.SZ'],         # stock_list, list of stock codes
    period='1d',           # period: tick, 1m, 5m, 15m, 30m, 1h, 1d, 1w, 1mon
    start_time='20240101',
    end_time='20240630',
    count=-1,              # -1 means retrieve all data
    dividend_type='front',  # adjustment type: none, front, back, front_ratio, back_ratio
    fill_data=True         # whether to fill suspended trading data
)
df = data['000001.SZ']
# Returned fields: open, high, low, close, volume, amount, settelementPrice, openInterest, preClose, suspendFlag
```

### 获取最新交易日K线

```python
# count=1 retrieves the latest single K-line bar
data = xtdata.get_market_data_ex([], ['000001.SZ'], period='1d', count=1)
```

## 获取本地缓存数据

```python
# If data is already cached, read directly from local storage (no need to download again)
data = xtdata.get_local_data(
    field_list=[],
    stock_list=['000001.SZ'],
    period='1d',
    start_time='20240101',
    end_time='20240630'
)
```

## 实时行情订阅

### 订阅单只股票

```python
def on_data(datas):
    """Quote callback function, receives pushed real-time data"""
    for stock_code, data in datas.items():
        print(stock_code, data)

# subscribe_quote(stock_code, period, start_time, end_time, count, callback)
xtdata.subscribe_quote('000001.SZ', period='tick', callback=on_data)
xtdata.run()  # Block the current thread, continuously receiving callback data
```

### 订阅全市场行情（全推）

```python
# Subscribe to full-market quote push
xtdata.subscribe_whole_quote(['SH', 'SZ'], callback=on_data)
# Market codes: 'SH' (Shanghai), 'SZ' (Shenzhen), 'BJ' (Beijing)
xtdata.run()
```

### 取消订阅

```python
# Unsubscribe using the sequence number returned by subscribe_quote
seq = xtdata.subscribe_quote('000001.SZ', period='tick', callback=on_data)
xtdata.unsubscribe_quote(seq)
```

## 获取全市场快照

```python
# Retrieve the latest Tick snapshot for the entire market
data = xtdata.get_full_tick(['SH', 'SZ'])
# 收益率 a dict: {stock_code: tick_data, ...}
```

---

## 财务数据

```python
# First download financial data to local cache
xtdata.download_financial_data(['000001.SZ'])

# Then retrieve financial data from local cache
data = xtdata.get_financial_data(['000001.SZ'])
```

### 可用财务报表

| Statement | Description |
|---|---|
| `Balance` | Balance Sheet |
| `Income` | Income Statement |
| `CashFlow` | Cash Flow Statement |
| `PershareIndex` | Per-Share Indicators |
| `CapitalStructure` | Capital Structure |
| `TOP10HOLDER` | Top 10 Shareholders |
| `TOP10FLOWHOLDER` | Top 10 Tradable Shareholders |
| `SHAREHOLDER` | Shareholder Count |

### 资产负债表关键字段

```python
'cash_equivalents'          # Cash and cash equivalents
'tradable_fin_assets'       # Trading financial assets
'account_receivable'        # Accounts receivable
'inventories'               # Inventories
'total_current_assets'      # Total current assets
'fix_assets'                # Fixed assets
'intang_assets'             # Intangible assets
'tot_assets'                # 总资产
'shortterm_loan'            # Short-term borrowings
'total_current_liability'   # Total current liabilities
'tot_liab'                  # Total liabilities
'cap_stk'                   # Paid-in capital (or share capital)
'undistributed_profit'      # Retained earnings
'total_equity'              # Total owners' equity
'tot_liab_shrhldr_eqy'      # Total liabilities and shareholders' equity
```

### 利润表关键字段

```python
'revenue'                              # Total operating revenue
'revenue_inc'                          # Operating revenue
'total_expense'                        # Operating costs
'sale_expense'                         # Selling expenses
'less_gerl_admin_exp'                  # Administrative expenses
'financial_expense'                    # Financial expenses
'oper_profit'                          # Operating profit
'tot_profit'                           # Total profit
'net_profit_incl_min_int_inc'          # 净利润
'net_profit_excl_min_int_inc'          # 净利润 attributable to parent company
's_fa_eps_basic'                       # Basic earnings per share
's_fa_eps_diluted'                     # Diluted earnings per share
```

### 现金流量表关键字段

```python
'goods_sale_and_service_render_cash'   # Cash received from sales of goods and services
'net_cash_flows_oper_act'              # Net cash flows from operating activities
'net_cash_flows_inv_act'               # Net cash flows from investing activities
'net_cash_flows_fnc_act'               # Net cash flows from financing activities
'net_incr_cash_cash_equ'               # Net increase in cash and cash equivalents
```

### 每股指标关键字段

```python
's_fa_eps_basic'                       # Basic earnings per share
's_fa_bps'                             # Book value per share
's_fa_ocfps'                           # Operating cash flow per share
'du_return_on_equity'                  # 净资产收益率（ROE）
'sales_gross_profit'                   # Gross profit margin
'inc_revenue_rate'                     # Year-over-year revenue growth rate
'du_profit_rate'                       # Year-over-year net profit growth rate
'gear_ratio'                          # Debt-to-asset ratio
'inventory_turnover'                   # Inventory turnover ratio
```

### 股本结构字段

```python
'total_capital'                        # Total share capital
'circulating_capital'                  # Listed tradable A-shares
'restrict_circulating_capital'         # Restricted tradable shares
```

### 前十大股东字段

```python
'declareDate'     # Announcement date
'endDate'         # Reporting period end date
'name'            # Shareholder name
'quantity'        # Number of shares held
'ratio'           # Shareholding ratio
'nature'          # Share type
'rank'            # Shareholding rank
```

---

## 除权除息数据

```python
# Retrieve ex-dividend adjustment factor data
data = xtdata.get_divid_factors('000001.SZ')
# Returned fields: interest (dividend per share), stockBonus (bonus shares per share), stockGift (capitalization shares per share),
#         allotNum (rights issue shares per share), allotPrice (rights issue price), gugai (share reform flag), dr (ex-dividend factor)
```

## 合约信息

```python
# Retrieve detailed instrument information
info = xtdata.get_instrument_detail('000001.SZ')
# 收益率 a dict containing: InstrumentName (instrument name), ExchangeID (market code), ProductID (product code),
#   UpStopPrice (upper price limit), DownStopPrice (lower price limit), PreClose (previous close),
#   FloatVolume (tradable shares), TotalVolume (total shares), PriceTick (minimum price increment),
#   VolumeMultiple (contract multiplier), CreateDate (creation date), OpenDate (listing date),
#   ExpireDate (expiration date), MainContract (main contract flag), IsTrading (whether tradable), etc.

# Retrieve security type
itype = xtdata.get_instrument_type('000001.SZ')  # 收益率 'stock', 'index', 'fund', 'bond', etc.

# Retrieve trading day list
days = xtdata.get_trading_dates('SH', start_time='20240101', end_time='20240630')

# Retrieve trading calendar
calendar = xtdata.get_trading_calendar('SH')

# Download and retrieve holiday data
xtdata.download_holiday_data()
holidays = xtdata.get_holidays()
```

## 板块管理

```python
# Retrieve sector list
sectors = xtdata.get_sector_list()

# Retrieve stock list within a sector
stocks = xtdata.get_stock_list_in_sector('沪深A股')

# Download sector classification data
xtdata.download_sector_data()

# Custom sector management
xtdata.create_sector_folder('', 'MyFolder')          # Create a folder at root level
xtdata.create_sector('MyFolder', 'MyBlock')           # Create a sector under the folder
xtdata.add_sector('MyBlock', ['000001.SZ', '600000.SH'])  # Add stocks to the sector
xtdata.remove_stock_from_sector('MyBlock', ['000001.SZ']) # Remove stocks from the sector
xtdata.reset_sector('MyBlock', ['600000.SH'])         # Reset sector contents
xtdata.remove_sector('MyBlock')                       # Delete the sector
```

## 指数成分股

```python
# First download index weight data
xtdata.download_index_weight()

# Retrieve index constituent weights
weights = xtdata.get_index_weight('000300.SH')
# 收益率: {stock_code: weight, ...}
```

## 可转债信息

```python
# Download and retrieve convertible bond data
xtdata.download_cb_data()
data = xtdata.get_cb_data()
```

## 新股申购信息

```python
# Retrieve IPO subscription information
data = xtdata.get_ipo_info()
```

## ETF申赎清单

```python
# Download and retrieve ETF creation/redemption information
xtdata.download_etf_info()
data = xtdata.get_etf_info()
```

## 可用数据周期

`tick`, `1m`, `5m`, `15m`, `30m`, `1h`, `1d`, `1w`, `1mon`

---

## 数据字段参考

### Tick数据字段

```python
'time'                  # Timestamp
'lastPrice'             # Latest price
'open'                  # Opening price
'high'                  # Highest price
'low'                   # Lowest price
'lastClose'             # Previous close price
'amount'                # Total turnover
'volume'                # Total volume
'pvolume'               # Raw total volume
'stockStatus'           # Security status
'openInt'               # Open interest
'lastSettlementPrice'   # Previous settlement price
'askPrice'              # Ask prices (list, 5 levels)
'bidPrice'              # Bid prices (list, 5 levels)
'askVol'                # Ask volumes (list, 5 levels)
'bidVol'                # Bid volumes (list, 5 levels)
'transactionNum'        # Number of transactions
```

### K线数据字段（1m / 5m / 1d等）

```python
'time'                  # Timestamp
'open'                  # Opening price
'high'                  # Highest price
'low'                   # Lowest price
'close'                 # Closing price
'volume'                # Volume
'amount'                # Turnover
'settelementPrice'      # Settlement price
'openInterest'          # Open interest
'preClose'              # Previous close price
'suspendFlag'           # Suspension flag: 0 - normal, 1 - suspended, -1 - resumed from today
```

### 证券状态码

```
0,10 - Unknown           11 - Pre-open S          12 - Call auction C
13 - Continuous trading T 14 - Break B             15 - Closed E
16 - Volatility interrupt V  17 - Temporary halt P  18 - Closing call auction U
19 - Intraday call auction M  20 - Halted until close N  21 - Field retrieval error
22 - After-hours fixed price trading  23 - After-hours fixed price trading ended
```

---

## Level2数据

If your broker supports Level2 data:

### l2quote — Level2实时行情快照

```python
'time'                  # Timestamp
'lastPrice'             # Latest price
'open' / 'high' / 'low' # Opening / Highest / Lowest price
'amount' / 'volume'     # Turnover / Volume
'transactionNum'        # Number of transactions
'pe'                    # 市盈率
'askPrice' / 'bidPrice' # Multi-level ask / bid prices
'askVol' / 'bidVol'     # Multi-level ask / bid volumes
```

### l2order — Level2逐笔委托

```python
'time'              # Timestamp
'price'             # Order price
'volume'            # Order quantity
'entrustNo'         # Order number
'entrustType'       # Order type (0 - unknown, 1 - normal, 2 - fill-or-kill remainder cancel, 4 - best five levels, 5 - fill-or-cancel, 6 - best own side, 7 - best counterparty)
'entrustDirection'  # Order direction (1 - buy, 2 - sell, 3 - cancel buy (SSE), 4 - cancel sell (SSE))
```

### l2transaction — Level2逐笔成交

```python
'time'          # Timestamp
'price'         # Trade price
'volume'        # Trade quantity
'amount'        # Trade amount
'tradeIndex'    # Trade record number
'buyNo'         # Buyer order number
'sellNo'        # Seller order number
'tradeType'     # Trade type
'tradeFlag'     # Trade flag (0 - unknown, 1 - active buy, 2 - active sell, 3 - cancellation (SZSE))
```

### l2quoteaux — 买卖汇总

```python
'avgBidPrice'           # Average bid price
'totalBidQuantity'      # Total bid quantity
'avgOffPrice'           # Average ask price
'totalOffQuantity'      # Total ask quantity
'withdrawBidQuantity'   # Total bid cancellation quantity
'withdrawOffQuantity'   # Total ask cancellation quantity
```

### l2orderqueue — 最优买卖委托队列

```python
'bidLevelPrice' / 'offerLevelPrice'    # Bid / Ask price
'bidLevelVolume' / 'offerLevelVolume'  # Bid / Ask volume
'bidLevelNumber' / 'offLevelNumber'    # Bid / Ask order count
```

### l2transactioncount — 逐笔成交统计

Includes ddx/ddy/ddz indicators, net order/cancellation volumes, and buy/sell statistics categorized by order size (extra-large / large / medium / small orders).

### l2thousand — 千档盘口

Up to 1000 levels of bid/ask prices and volumes.

### limitupperformance — 涨停连板数据

```python
'startUp' / 'endUp'   # Limit-up start / end time
'breakUp'              # Number of limit-up breaks
'sealCount'            # Consecutive limit-up days
'sealVolRatio'         # Seal-to-volume ratio
'direct'               # Direction: 0 - none, 1 - limit up, 2 - limit down
```

### snapshotindex — 快照指标

```python
'volRatio'          # Volume ratio
'speed1' / 'speed5' # 1-minute / 5-minute price change speed
'gainRate3/5/10'    # 3/5/10-day price change percentage
'turnoverRate3/5/10' # 3/5/10-day turnover rate
```

### announcement — 公告与新闻

```python
'headline'  # Headline
'summary'   # Summary
'content'   # Content
'type'      # Type: 0 - other, 1 - financial report
```

### hfiopv — 高频IOPV（100ms推送频率）

ETF IOPV data, including dynamic IOPV, limit-up/down IOPV, and premium/discount estimates.

### fullspeedorderbook — 全速盘口（20档）

```python
'bidPrice' / 'askPrice'    # Multi-level bid / ask price list (levels 1-20)
'bidVolume' / 'askVolume'  # Multi-level bid / ask volume list (levels 1-20)
```

---

## 合约信息 Fields

```python
'InstrumentName'        # Instrument name
'ExchangeID'            # Market code
'PreClose'              # Previous close price
'UpStopPrice'           # Daily upper price limit
'DownStopPrice'         # Daily lower price limit
'FloatVolume'           # Tradable shares
'TotalVolume'           # Total shares
'PriceTick'             # Minimum price increment
'VolumeMultiple'        # Contract multiplier
'MainContract'          # Main contract flag (1 - primary, 2 - secondary, 3 - tertiary)
'OpenDate'              # IPO date / Listing date
'ExpireDate'            # Delisting date or expiration date
'IsTrading'             # Whether the instrument is tradable
'OptExercisePrice'      # Option exercise price / Convertible bond conversion price
'OptionType'            # Option type (-1 not an option, 0 call, 1 put)
'MaxLimitOrderVolume'   # Maximum limit order volume
'MinLimitOrderVolume'   # Minimum limit order volume
```

## ETF现金替代标志

```
0 - Cash substitution prohibited (stock required)
1 - Cash substitution allowed (use stock first, cash for shortfall)
2 - Cash substitution mandatory
3 - Non-SSE cash substitution with settlement
4 - Non-SSE mandatory cash substitution
```

## 时间戳转换工具

```python
import time

def conv_time(ct):
    '''Convert millisecond timestamp to string format: conv_time(1476374400000) --> "20161014000000.000"'''
    local_time = time.localtime(ct / 1000)
    data_head = time.strftime('%Y%m%d%H%M%S', local_time)
    data_secs = (ct - int(ct)) * 1000
    return '%s.%03d' % (data_head, data_secs)
```

## 使用技巧

- Before retrieving data for the first time, always call `xtdata.download_history_data()` to download to local cache.
- Downloaded data is cached locally — subsequent reads are extremely fast.
- `xtdata.run()` blocks the current thread — if you need to trade simultaneously, run it in a separate thread.
- Prefer `get_market_data_ex` (recommended) over `get_local_data` — the former supports more features like dividend adjustment.
- For delisted/expired contract data, use `download_history_data2`.
- Financial data timestamp notes: `m_anntime` = disclosure date, `m_timetag` = reporting period end date.
- Documentation: http://dict.thinktrader.net/nativeApi/xtdata.html

---

## 进阶示例

### 批量下载多只股票历史数据

```python
from xtquant import xtdata
import time

# Connect to miniQMT market data service
xtdata.connect()

# Define the stock list to download (common A-share stocks)
stock_list = [
    '600519.SH',  # Kweichow Moutai
    '000001.SZ',  # Ping An Bank
    '300750.SZ',  # CATL
    '601318.SH',  # Ping An Insurance
    '000858.SZ',  # Wuliangye
    '600036.SH',  # China Merchants Bank
    '002594.SZ',  # BYD
]

# Batch download daily K-line data (forward adjusted)
for stock in stock_list:
    print(f"Downloading daily K-line data for {stock}...")
    xtdata.download_history_data(stock, '1d', start_time='20230101', end_time='20241231')
    time.sleep(0.5)  # Add delay to avoid triggering rate limits

# Batch retrieve data and merge for analysis
all_data = {}
for stock in stock_list:
    data = xtdata.get_market_data_ex(
        [],                     # Empty list means all fields
        [stock],                # 股票代码 list
        period='1d',            # Daily K-line
        start_time='20230101',
        end_time='20241231',
        dividend_type='front',  # Forward adjusted
        fill_data=True          # Fill suspended trading data
    )
    df = data[stock]
    all_data[stock] = df
    print(f"{stock} retrieved {len(df)} records")

# Compare closing price trends across multiple stocks
import pandas as pd
close_df = pd.DataFrame({stock: all_data[stock]['close'] for stock in stock_list})
print("Latest closing prices:")
print(close_df.tail(5))
```

### 实时行情监控 + 条件预警

```python
from xtquant import xtdata
import datetime

# Connect to market data service
xtdata.connect()

# Define watchlist and alert conditions
watch_list = ['600519.SH', '000001.SZ', '300750.SZ']
alert_config = {
    '600519.SH': {'upper': 1900.0, 'lower': 1700.0},  # Moutai: alert at 1900 or 1700
    '000001.SZ': {'upper': 15.0, 'lower': 10.0},       # Ping An Bank: alert at 15 or 10
    '300750.SZ': {'upper': 250.0, 'lower': 180.0},     # CATL: alert at 250 or 180
}

def on_realtime_data(datas):
    """Real-time quote callback — checks alert conditions on each push"""
    now = datetime.datetime.now().strftime('%H:%M:%S')
    for stock_code, tick_data in datas.items():
        # Get latest price
        last_price = tick_data['lastPrice']
        pre_close = tick_data['lastClose']
        # Calculate price change percentage
        change_pct = (last_price - pre_close) / pre_close * 100 if pre_close > 0 else 0

        print(f"[{now}] {stock_code}: Latest={last_price:.2f}, Change={change_pct:.2f}%")

        # Check alert conditions
        if stock_code in alert_config:
            config = alert_config[stock_code]
            if last_price >= config['upper']:
                print(f"  ⚠️ Alert: {stock_code} price {last_price:.2f} breached upper limit {config['upper']}")
            elif last_price <= config['lower']:
                print(f"  ⚠️ Alert: {stock_code} price {last_price:.2f} breached lower limit {config['lower']}")

# Subscribe to Tick data for multiple stocks
for stock in watch_list:
    xtdata.subscribe_quote(stock, period='tick', callback=on_realtime_data)

print("Real-time monitoring started, press Ctrl+C to exit...")
xtdata.run()  # Block main thread, continuously receiving data
```

### Level2逐笔成交分析（大单跟踪）

```python
from xtquant import xtdata
import pandas as pd

# Connect to market data service
xtdata.connect()

stock = '600519.SH'

# Download Level2 trade-by-trade data (requires L2 data permissions)
xtdata.download_history_data(stock, 'l2transaction', start_time='20240601', end_time='20240601')

# Retrieve trade-by-trade data
data = xtdata.get_market_data_ex([], [stock], period='l2transaction',
                                  start_time='20240601', end_time='20240601')
df = data[stock]

if len(df) > 0:
    # Convert trade amount to 10-thousands (wan yuan)
    df['amount_wan'] = df['amount'] / 10000

    # Categorize by trade amount (Extra-large >1M, Large >200K, Medium >50K, Small <50K)
    df['order_size'] = pd.cut(
        df['amount_wan'],
        bins=[0, 5, 20, 100, float('inf')],
        labels=['小单(<5万)', '中单(5-20万)', '大单(20-100万)', '特大单(>100万)']
    )

    # Statistics by trade direction and order size
    # tradeFlag: 1=active buy, 2=active sell
    buy_stats = df[df['tradeFlag'] == 1].groupby('order_size')['amount_wan'].sum()
    sell_stats = df[df['tradeFlag'] == 2].groupby('order_size')['amount_wan'].sum()

    print(f"\n{stock} Trade-by-Trade Statistics (unit: 10K yuan)")
    print("=" * 50)
    print("[Active Buy]")
    print(buy_stats)
    print("\n[Active Sell]")
    print(sell_stats)
    print(f"\nNet buy amount: {buy_stats.sum() - sell_stats.sum():.2f} (10K yuan)")
```

### 财务数据筛选 — 低估值高成长选股

```python
from xtquant import xtdata
import pandas as pd

# Connect to market data service
xtdata.connect()

# Retrieve A-share stock list
stock_list = xtdata.get_stock_list_in_sector('沪深A股')
print(f"Total A-shares: {len(stock_list)}")

# Download financial data
xtdata.download_financial_data(stock_list)

# Retrieve financial data
fin_data = xtdata.get_financial_data(stock_list)

# Build screening DataFrame
results = []
for stock, data_list in fin_data.items():
    if not data_list:
        continue
    # Take the latest financial report
    latest = data_list[-1] if isinstance(data_list, list) else data_list

    # Extract key indicators
    try:
        roe = latest.get('du_return_on_equity', None)          # 净资产收益率（ROE）
        revenue_growth = latest.get('inc_revenue_rate', None)   # Year-over-year revenue growth
        profit_growth = latest.get('du_profit_rate', None)      # Year-over-year net profit growth
        eps = latest.get('s_fa_eps_basic', None)                # Basic earnings per share
        bps = latest.get('s_fa_bps', None)                      # Book value per share
        gear = latest.get('gear_ratio', None)                   # Debt-to-asset ratio

        if all(v is not None for v in [roe, revenue_growth, eps, bps]):
            results.append({
                '股票代码': stock,
                'ROE(%)': roe,
                '营收增长率(%)': revenue_growth,
                '净利润增长率(%)': profit_growth,
                '每股收益': eps,
                '每股净资产': bps,
                '资产负债率(%)': gear
            })
    except:
        continue

df = pd.DataFrame(results)

# Screening criteria: ROE>15%, revenue growth>10%, net profit growth>10%, debt-to-asset ratio<70%
filtered = df[
    (df['ROE(%)'] > 15) &
    (df['营收增长率(%)'] > 10) &
    (df['净利润增长率(%)'] > 10) &
    (df['资产负债率(%)'] < 70)
].sort_values('ROE(%)', ascending=False)

print(f"\nScreened {len(filtered)} high-growth low-valuation stocks:")
print(filtered.head(20).to_string(index=False))
```

### 板块管理 — Custom Stock Pools

```python
from xtquant import xtdata

# Connect to market data service
xtdata.connect()

# Download sector classification data
xtdata.download_sector_data()

# View system sector list
sectors = xtdata.get_sector_list()
print("System sector list (first 20):")
for s in sectors[:20]:
    print(f"  {s}")

# Retrieve CSI 300 constituents
xtdata.download_index_weight()
hs300_weights = xtdata.get_index_weight('000300.SH')
print(f"\nCSI 300 has {len(hs300_weights)} constituents")
# Sort by weight, show top 10
sorted_weights = sorted(hs300_weights.items(), key=lambda x: x[1], reverse=True)
print("Top 10 by weight:")
for stock, weight in sorted_weights[:10]:
    print(f"  {stock}: {weight:.4f}")

# Create custom sector — save screened stocks as a watchlist
xtdata.create_sector_folder('', '我的策略')                    # Create folder
xtdata.create_sector('我的策略', '高ROE成长股')                 # Create sector
my_stocks = ['600519.SH', '000858.SZ', '601318.SH', '300750.SZ']
xtdata.add_sector('高ROE成长股', my_stocks)                    # Add stocks

# Verify sector contents
stocks_in_sector = xtdata.get_stock_list_in_sector('高ROE成长股')
print(f"\nCustom sector '高ROE成长股' contains {len(stocks_in_sector)} stocks:")
for s in stocks_in_sector:
    print(f"  {s}")
```

### 多周期K线数据对比分析

```python
from xtquant import xtdata
import pandas as pd

# Connect to market data service
xtdata.connect()

stock = '600519.SH'

# Download data for multiple periods
periods = ['1m', '5m', '15m', '30m', '1h', '1d']
for period in periods:
    xtdata.download_history_data(stock, period, start_time='20240601', end_time='20240630')

# Retrieve data for each period and compute statistics
print(f"\n{stock} Multi-Period Data Statistics (June 2024)")
print("=" * 60)
for period in periods:
    data = xtdata.get_market_data_ex([], [stock], period=period,
                                      start_time='20240601', end_time='20240630',
                                      dividend_type='front')
    df = data[stock]
    if len(df) > 0:
        print(f"\n[{period} period] {len(df)} K-line bars")
        print(f"  Highest: {df['high'].max():.2f}")
        print(f"  Lowest: {df['low'].min():.2f}")
        print(f"  Average volume: {df['volume'].mean():.0f}")
        print(f"  Total turnover: {df['amount'].sum() / 1e8:.2f} (100M yuan)")
```

### 可转债数据分析

```python
from xtquant import xtdata
import pandas as pd

# Connect to market data service
xtdata.connect()

# Download convertible bond data
xtdata.download_cb_data()
cb_data = xtdata.get_cb_data()

print(f"Retrieved {len(cb_data)} convertible bonds")

# Download convertible bond market data (using a subset as example)
cb_codes = list(cb_data.keys())[:20]  # Take the first 20
for code in cb_codes:
    xtdata.download_history_data(code, '1d', start_time='20240101', end_time='20241231')

# Retrieve market data and analyze
results = []
for code in cb_codes:
    data = xtdata.get_market_data_ex([], [code], period='1d', count=1)
    if code in data and len(data[code]) > 0:
        last = data[code].iloc[-1]
        info = xtdata.get_instrument_detail(code)
        results.append({
            '转债代码': code,
            '转债名称': info.get('InstrumentName', ''),
            '最新价': last['close'],
            '成交额(万)': last['amount'] / 10000,
        })

df = pd.DataFrame(results)
print("\nConvertible bond market overview:")
print(df.to_string(index=False))
```

### ETF申赎清单与套利分析

```python
from xtquant import xtdata

# Connect to market data service
xtdata.connect()

# Download ETF creation/redemption information
xtdata.download_etf_info()
etf_info = xtdata.get_etf_info()

print(f"Retrieved {len(etf_info)} ETF creation/redemption records")

# Compare ETF real-time quotes with IOPV (requires real-time data)
etf_list = ['510300.SH', '510050.SH', '510500.SH', '159919.SZ']  # Common broad-based ETFs
for etf in etf_list:
    xtdata.download_history_data(etf, '1d', start_time='20240101', end_time='20241231')
    data = xtdata.get_market_data_ex([], [etf], period='1d', count=5, dividend_type='none')
    if etf in data and len(data[etf]) > 0:
        df = data[etf]
        info = xtdata.get_instrument_detail(etf)
        print(f"\n{info.get('InstrumentName', etf)} ({etf}):")
        print(f"  Latest close: {df['close'].iloc[-1]:.4f}")
        print(f"  5-day avg turnover: {df['amount'].mean() / 1e8:.2f} (100M yuan)")
        print(f"  5-day change: {(df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100:.2f}%")
```

---

---

## 🤖 AI Agent 高阶使用指南

对于 AI Agent，在使用该量化/数据工具时应遵循以下高阶策略和最佳实践，以确保任务的高效完成：

### 1. 数据校验与错误处理
在获取数据或执行操作后，AI 应当主动检查返回的结果格式是否符合预期，以及是否存在缺失值（NaN）或空数据。
* **示例策略**：在通过 API 获取数据框（DataFrame）后，使用 `if df.empty:` 进行校验；捕获 `Exception` 以防网络或接口错误导致进程崩溃。

### 2. 多步组合分析
AI 经常需要进行宏观经济分析或跨市场对比。应善于将当前接口与其他数据源或工具组合使用。
* **示例策略**：先获取板块或指数的宏观数据，再筛选成分股，最后对具体标的进行深入的财务或技术面分析，形成完整的决策链条。

### 3. 构建动态监控与日志
对于交易和策略类任务，AI 可以定期拉取数据并建立监控机制。
* **示例策略**：使用循环或定时任务检查特定标的的异动（如涨跌停、放量），并在发现满足条件的信号时输出结构化日志或触发预警。

---

## 社区与支持

由 **大佬量化** 维护 — 量化交易教学与策略研发团队。

微信客服: **bossquant1** · [Bilibili](https://space.bilibili.com/48693330) · 搜索 **大佬量化** — 微信公众号 / Bilibili / 抖音
