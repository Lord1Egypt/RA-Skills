---
name: stock-tracker-pro
description: 股票监控技能。使用 Yahoo Finance 获取股票数据。支持添加股票到监控列表、删除股票、查询股票信息。触发场景：(1) 添加股票如"监控 AAPL"，(2) 删除股票如"删除 TSLA"，(3) 查询股票如"查看腾讯股票"、"AAPL 股价"。
---

# Stock Tracker Pro

管理股票监控列表并获取股票信息。

## 存储位置

股票列表：`/home/frank/.openclaw/workspace/skills/stock-tracker-pro/stocks.json`

## 操作

### 添加股票

```bash
python3 /home/frank/.openclaw/workspace/skills/stock-tracker-pro/scripts/stock_manager.py add <股票代码>
```

- 国际股票：AAPL、TSLA、MSFT、GOOGL、NVDA、AMZN、META 等
- 自动获取股票名称

### 删除股票

```bash
python3 /home/frank/.openclaw/workspace/skills/stock-tracker-pro/scripts/stock_manager.py remove <股票代码>
```

### 查看监控列表

```bash
python3 /home/frank/.openclaw/workspace/skills/stock-tracker-pro/scripts/stock_manager.py list
```

### 获取股票信息（含新闻）

```bash
python3 /home/frank/.openclaw/workspace/skills/stock-tracker-pro/scripts/get_stock_info.py <股票代码>
```

返回：当前价格、涨跌幅、市值、成交量、52周高低、PE、盈利、股息等财务数据，**同时显示 3 条热门新闻**。

## 示例

- 用户说"监控 AAPL" → 执行 add
- 用户说"删除 TSLA" → 执行 remove  
- 用户说"看看 NVDA 怎么样" → 执行 get_stock_info（含新闻）
- 用户说"查看监控列表" → 执行 list
