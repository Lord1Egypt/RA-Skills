---
name: "stock-price-query"
description: "Query current A/HK/US-share stock prices using natural language stock names. Invoke when user asks about stock prices, market data, or mentions Chinese stock names like '贵州茅台', '中国平安', etc."
---
# A股/港股/美股股票价格查询

## 功能描述

使用Python查询A股/港股/美股股票的当前价格，支持通过自然语言描述股票名称（如"贵州茅台"、"中国平安"等）。

## 使用方法

当用户询问股票价格时，直接运行以下命令：

```bash
uv run python ~/.openclaw/skills/stock-price-query/scripts/stock_price_query.py <股票名称或代码>
```

## 快速开始

### 在工作目录下执行

```bash
python3 scripts/stock_price_query.py "贵州茅台的股价"
```

## 注意事项

1. **数据源**：使用新浪财经
2. **错误处理**：网络异常或股票代码错误时会返回友好提示

## 触发条件

当用户询问以下类型问题时调用此skill：

- "XX股票现在多少钱？"
- "查询一下贵州茅台的股价"
- "中国平安今天涨了多少？"
- "比亚迪股票行情"
- "宁德时代最新价格"