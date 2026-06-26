# Stock Market Analyzer

A-share股票市场分析工具 - 支持实时行情查询、技术指标分析和投资组合管理。

## 功能特性

- **实时行情数据**: 查询最新价格、成交量和基本面数据
- **技术指标分析**: RSI、MACD、KDJ、布林带、移动平均线等
- **市场汇总**: 开盘和收盘市场摘要
- **投资组合跟踪**: 追踪多只股票并分析表现

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 查询实时价格

```python
from scripts.stock_analyzer import query_realtime_price

# 查询单只股票
result = query_realtime_price("600519.SH")
print(f"当前价格: {result['price']}")
```

### 查询技术指标

```python
from scripts.stock_analyzer import query_technical_indicators

# 获取技术分析
indicators = query_technical_indicators("000001.SZ")
print(f"RSI: {indicators['rsi']}")
print(f"MACD: {indicators['macd']}")
```

### 查询开盘/收盘汇总

```python
from scripts.stock_analyzer import query_open_summary, query_close_summary

# 开盘汇总
open_data = query_open_summary("600519.SH")

# 收盘汇总
close_data = query_close_summary("000001.SZ,600519.SH")
```

## 支持的股票交易所

- **SH**: 上海证券交易所 (如: 600519.SH)
- **SZ**: 深圳证券交易所 (如: 000001.SZ)

## 可用技术指标

- RSI (相对强弱指数)
- MACD (指数平滑异同平均线)
- KDJ (随机指标)
- BOLL (布林带)
- MA (移动平均线)
- 量比
- 换手率
- 振幅
