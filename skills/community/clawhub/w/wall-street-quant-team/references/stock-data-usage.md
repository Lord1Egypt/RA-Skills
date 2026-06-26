# 股票数据获取使用指南

## 目录
- 功能概述
- 安装依赖
- 支持的市场和代码格式
- 使用方法
- 数据类型说明
- 集成到代理系统
- 常见问题

## 功能概述

股票数据获取脚本（`scripts/stock-data-fetcher.py`）提供以下功能：
- 实时报价获取
- 历史数据查询
- 股票基本信息
- 财务报表数据
- 技术指标计算（MA、MACD、RSI等）
- 批量获取多个股票数据

基于yfinance库，支持A股、港股、美股等全球主要市场。

## 安装依赖

```bash
pip install yfinance>=0.2.28 pandas>=2.0.0
```

## 支持的市场和代码格式

### A股市场
- 上海证券交易所：股票代码 + `.SS`
  - 茅台：`600519.SS`
  - 工商银行：`601398.SS`
- 深圳证券交易所：股票代码 + `.SZ`
  - 平安银行：`000001.SZ`
  - 宁德时代：`300750.SZ`

### 港股市场
- 股票代码 + `.HK`
  - 腾讯控股：`0700.HK`
  - 阿里巴巴：`9988.HK`
  - 美团：`3690.HK`

### 美股市场
- 直接使用股票代码
  - 苹果：`AAPL`
  - 特斯拉：`TSLA`
  - 微软：`MSFT`
  - 英伟达：`NVDA`

## 使用方法

### 命令行使用

#### 1. 获取实时报价
```bash
python scripts/stock-data-fetcher.py AAPL --type quote
```

输出示例：
```json
{
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "current_price": 178.72,
  "change": 2.34,
  "change_percent": 1.33,
  "open": 176.50,
  "high": 179.20,
  "low": 176.10,
  "volume": 52340000,
  "previous_close": 176.38,
  "market_cap": 2800000000000,
  "pe_ratio": 28.5,
  "52_week_high": 198.23,
  "52_week_low": 124.17
}
```

#### 2. 获取股票基本信息
```bash
python scripts/stock-data-fetcher.py AAPL --type info
```

输出包含：公司名称、行业、市值、PE比率、ROE等基本面数据。

#### 3. 获取技术指标
```bash
python scripts/stock-data-fetcher.py AAPL --type technical --period 3mo
```

输出示例：
```json
{
  "symbol": "AAPL",
  "price": 178.72,
  "ma5": 176.45,
  "ma10": 175.20,
  "ma20": 172.30,
  "ma60": 165.80,
  "macd": 1.2345,
  "macd_signal": 0.9876,
  "macd_histogram": 0.2469,
  "rsi": 58.5,
  "volume": 52340000
}
```

#### 4. 获取历史数据
```bash
python scripts/stock-data-fetcher.py AAPL --type history --period 1y --interval 1d
```

参数说明：
- `--period`: 时间周期（1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max）
- `--interval`: 数据间隔（1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo）

#### 5. 获取财务报表
```bash
python scripts/stock-data-fetcher.py AAPL --type financial
```

输出包含：利润表、资产负债表、现金流量表。

#### 6. 输出到文件
```bash
python scripts/stock-data-fetcher.py AAPL --type quote --output quote.json
```

## 数据类型说明

### 实时报价字段
- `current_price`: 当前价格
- `change`: 涨跌额
- `change_percent`: 涨跌幅（%）
- `open`: 开盘价
- `high`: 最高价
- `low`: 最低价
- `volume`: 成交量
- `market_cap`: 市值
- `pe_ratio`: 市盈率
- `52_week_high`: 52周最高
- `52_week_low`: 52周最低

### 技术指标字段
- `ma5/10/20/60`: 5/10/20/60日均线
- `macd`: MACD指标
- `macd_signal`: MACD信号线
- `macd_histogram`: MACD柱状图
- `rsi`: RSI相对强弱指标

## 集成到代理系统

### Python API调用

```python
from scripts.stock_data_fetcher import StockDataFetcher

# 初始化
fetcher = StockDataFetcher()

# 获取实时报价
quote = fetcher.get_realtime_quote('AAPL')
print(f"当前价格: {quote['current_price']}")

# 获取技术指标
indicators = fetcher.get_technical_indicators('AAPL')
print(f"RSI: {indicators['rsi']}, MACD: {indicators['macd']}")

# 批量获取
quotes = fetcher.batch_get_quotes(['AAPL', 'TSLA', 'MSFT'])
```

### 基本面分析师集成

基本面分析师代理在分析股票时：
1. 调用 `get_stock_info()` 获取公司基本信息
2. 调用 `get_financial_statements()` 获取财务报表
3. 基于数据进行分析和估值

### 技术分析师集成

技术分析师代理在分析K线时：
1. 调用 `get_technical_indicators()` 获取技术指标
2. 调用 `get_historical_data()` 获取历史K线数据
3. 基于指标判断趋势和买卖点

### 行业研究员集成

行业研究员代理在分析行业时：
1. 批量获取行业内多个股票的基本面数据
2. 对比分析行业整体表现
3. 识别行业龙头和优质标的

## 常见问题

### Q: API限流怎么办？
A: yfinance有请求频率限制，建议：
- 批量获取时增加请求间隔
- 缓存已获取的数据
- 使用多个数据源备份

### Q: A股数据准确性如何？
A: yfinance对A股支持有限，建议：
- 优先使用港股和美股数据
- A股可考虑使用tushare或akshare作为补充

### Q: 实时数据延迟多久？
A:
- 美股：约15分钟延迟（免费版）
- 港股：约15-20分钟延迟
- A股：延迟较大，建议使用其他数据源

### Q: 支持哪些时间周期？
A:
- 分钟级：1m, 2m, 5m, 15m, 30m, 60m, 90m
- 日级：1d, 5d
- 周月级：1wk, 1mo, 3mo

### Q: 如何获取更多历史数据？
A: 使用 `--period max` 参数获取全部可用历史数据

## 扩展建议

如需更高频或更精准的数据，可考虑：
1. **付费API**：
   - Alpha Vantage
   - IEX Cloud
   - Polygon.io
   - Finnhub

2. **A股专用**：
   - Tushare Pro
   - AKShare
   - TuShare

3. **专业数据**：
   - Bloomberg Terminal
   - Wind（万得）
   - Choice（东方财富）
