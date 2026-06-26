---
name: yahooclaw
description: Yahoo Finance API integration for OpenClaw. Use when users ask for stock prices, company financials, historical data, dividends, or market data. Supports real-time quotes, financial statements, and market analysis.
---

# YahooClaw - Yahoo Finance API Integration

## 功能说明

yahooclaw 是一个集成 Yahoo Finance API 的 OpenClaw 技能，提供实时股票数据查询、财务分析、历史股价等功能。

## 使用场景

### 1. 查询实时股价
```
查询 AAPL 的股价
特斯拉现在多少钱
NVDA 最新股价
```

### 2. 查询公司信息
```
苹果公司的市值是多少
微软的市盈率
谷歌的营收数据
```

### 3. 历史数据
```
显示 AAPL 过去 30 天股价
特斯拉上个月走势
```

### 4. 财务指标
```
苹果的资产负债表
腾讯的利润表
```

### 5. 股息分红
```
AAPL 分红是多少
哪些股票股息率高
```

## 使用示例

### 基础用法
```javascript
const YahooClaw = require('./src/yahoo-finance.js');

// 获取实时股价
const quote = await YahooClaw.getQuote('AAPL');
console.log(quote);

// 获取历史数据
const history = await YahooClaw.getHistory('TSLA', '1mo');
console.log(history);

// 获取公司信息
const info = await YahooClaw.getCompanyInfo('MSFT');
console.log(info);
```

### OpenClaw 集成
```javascript
// 在 OpenClaw agent 中调用
const result = await tools.yahooclaw.getQuote({symbol: 'AAPL'});
```

## API 参数说明

### getQuote(symbol)
- **symbol**: 股票代码（如 AAPL, TSLA, 0700.HK）
- **返回**: 实时股价、涨跌幅、成交量等

### getHistory(symbol, period)
- **symbol**: 股票代码
- **period**: 时间周期（1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max）
- **返回**: 历史股价数据

### getCompanyInfo(symbol)
- **symbol**: 股票代码
- **返回**: 公司信息、市值、市盈率、市净率等

### getDividends(symbol)
- **symbol**: 股票代码
- **返回**: 股息分红历史

## 环境变量

```bash
# Yahoo Finance API（可选，基础功能无需 API key）
YAHOO_FINANCE_API_KEY=your_api_key_here

# 代理设置（如果需要）
HTTP_PROXY=http://proxy.example.com:8080
HTTPS_PROXY=https://proxy.example.com:8080
```

## 注意事项

1. **数据延迟**：Yahoo Finance 实时数据可能有 15 分钟延迟
2. **请求限制**：建议控制请求频率，避免被限流
3. **港股/A 股**：支持港股（0700.HK）、A 股（600519.SS）等
4. **错误处理**：网络问题或无效代码会返回错误信息

## 故障排除

### 常见问题

1. **获取数据失败**
   - 检查网络连接
   - 验证股票代码格式
   - 查看 Yahoo Finance 服务状态

2. **数据延迟**
   - 这是正常现象，Yahoo Finance 实时数据有延迟
   - 考虑使用付费 API 获取真正实时数据

3. **A 股/港股代码格式**
   - A 股：600519.SS（茅台）
   - 港股：0700.HK（腾讯）
   - 美股：AAPL（苹果）

## 相关资源

- [Yahoo Finance API 文档](https://finance.yahoo.com/)
- [yfinance Python 库](https://pypi.org/project/yfinance/)
- [OpenClaw 文档](https://docs.openclaw.ai/)

## 更新日志

### v0.1.0 (2026-03-09)
- ✅ 初始版本发布
- ✅ 实时股价查询
- ✅ 历史数据查询
- ✅ 公司信息查询
- ✅ 股息分红查询
- ✅ OpenClaw 集成

## 许可证

MIT License

## 作者

PocketAI for Leo - OpenClaw Community
