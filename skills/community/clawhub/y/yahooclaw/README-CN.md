# 🦞 YahooClaw - Yahoo Finance API for OpenClaw

> 让 OpenClaw 能直接查询股票行情、财务数据和市场分析

[![版本](https://img.shields.io/github/v/tag/leohuang8688/yahooclaw?label=version&color=green)](https://github.com/leohuang8688/yahooclaw)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://github.com/openclaw/openclaw)

**[English Docs](README.md)** | **[中文文档](README-CN.md)**

---

## 📖 简介

**YahooClaw v0.0.3** 是一个为 OpenClaw 设计的生产级 Yahoo Finance API 集成技能，特性包括：

- 📈 **实时股价** - 美股、港股、A 股等全球市场
- 📊 **历史数据** - 支持多种时间周期（1 天到全部）
- 💰 **股息分红** - 完整的分红历史
- 📉 **财务报表** - 资产负债表、利润表、现金流
- 🔍 **股票搜索** - 快速查找股票代码
- 📰 **新闻聚合** - 多源新闻 + 情感分析
- 📊 **技术指标** - 7 大主流技术指标（MA, RSI, MACD, BOLL, KDJ）
- 🔄 **自动故障转移** - 限流时自动切换备用 API
- 💾 **智能缓存** - 5 分钟 TTL，速度提升 30 倍

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /root/.openclaw/workspace/skills/yahooclaw
npm install
```

### 2. 配置环境变量（可选）

创建 `.env` 文件配置备用 API：

```bash
# Alpha Vantage API Key（免费 500 次/天）
ALPHA_VANTAGE_API_KEY=your_api_key_here

# API 管理器配置
API_TIMEOUT=10000          # 请求超时（毫秒）
API_CACHE_TTL=300000       # 缓存有效期（5 分钟）
API_CACHE_ENABLED=true     # 启用缓存
```

### 3. 在 OpenClaw 中使用

```javascript
// 在你的 OpenClaw agent 中导入
import yahooclaw from './skills/yahooclaw/src/index.js';

// 查询股价
const aapl = await yahooclaw.getQuote('AAPL');
console.log(`AAPL: $${aapl.data.price}`);

// 查询历史数据
const tsla = await yahooclaw.getHistory('TSLA', '1mo');
console.log(tsla.data.quotes);

// 技术指标分析
const nvda = await yahooclaw.getTechnicalIndicators('NVDA', '1mo', ['MA', 'RSI', 'MACD']);
console.log(nvda.data.analysis.recommendation);

// 新闻聚合 + 情感分析
const msft = await yahooclaw.getNews('MSFT', { limit: 5, sentiment: true });
console.log(msft.data.overallSentiment);
```

### 4. 通过 OpenClaw 对话使用

```
用户：查询苹果股价
PocketAI: 好的，正在查询 AAPL...
        苹果公司 (AAPL) 当前股价：$260.83
        涨跌：+$0.95 (+0.37%) 📈
        市值：2.73 万亿美元
```

---

## 📚 API 文档

### getQuote(symbol)

获取实时股价

**参数：**
- `symbol` (string): 股票代码，如 'AAPL', 'TSLA', '0700.HK'

**返回：**
```javascript
{
  success: true,
  data: {
    symbol: 'AAPL',
    name: 'Apple Inc.',
    price: 175.43,
    change: 2.15,
    changePercent: 1.24,
    previousClose: 173.28,
    open: 173.50,
    dayHigh: 176.00,
    dayLow: 173.00,
    volume: 52000000,
    marketCap: 2730000000000,
    pe: 28.5,
    eps: 6.15,
    dividend: 0.96,
    yield: 0.0055,
    currency: 'USD',
    exchange: 'NMS',
    marketState: 'REGULAR',
    timestamp: '2026-03-10T12:00:00.000Z'
  },
  message: '成功获取 AAPL 股价数据'
}
```

**示例：**
```javascript
const quote = await yahooclaw.getQuote('AAPL');
console.log(`AAPL: $${quote.data.price}`);
```

---

### getHistory(symbol, period)

获取历史股价数据

**参数：**
- `symbol` (string): 股票代码
- `period` (string): 时间周期
  - '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'

**返回：**
```javascript
{
  success: true,
  data: {
    symbol: 'TSLA',
    period: '1mo',
    quotes: [
      {
        date: '2026-02-09',
        open: 280.50,
        high: 285.00,
        low: 278.00,
        close: 282.30,
        volume: 45000000
      },
      // ...
    ],
    count: 30
  },
  message: '成功获取 TSLA 过去 1mo 历史数据，共 30 条记录'
}
```

---

### getTechnicalIndicators(symbol, period, indicators)

获取技术指标分析 🎯

**参数：**
- `symbol` (string): 股票代码
- `period` (string): 时间周期
- `indicators` (Array): 技术指标列表
  - 'MA' - 移动平均线
  - 'EMA' - 指数移动平均线
  - 'RSI' - 相对强弱指数
  - 'MACD' - 平滑异同移动平均线
  - 'BOLL' - 布林带
  - 'KDJ' - 随机指标
  - 'Volume' - 成交量分析

**返回：**
```javascript
{
  success: true,
  data: {
    symbol: 'AAPL',
    period: '1mo',
    indicators: {
      MA: {
        MA5: { value: 174.50, period: 5, trend: 'BULLISH' },
        MA10: { value: 172.30, period: 10, trend: 'BULLISH' },
        MA20: { value: 170.80, period: 20, trend: 'BULLISH' }
      },
      RSI: {
        RSI14: 65.50,
        signal: 'BULLISH'
      },
      MACD: {
        macdLine: 2.35,
        signalLine: 1.80,
        histogram: 0.55,
        trend: 'BULLISH',
        crossover: 'GOLDEN'
      }
    },
    analysis: {
      signal: 'BUY',
      confidence: 75,
      bullish: 6,
      bearish: 2,
      details: [
        'MA5: 看涨',
        'RSI: 看涨',
        'MACD: 看涨',
        'MACD: 金叉'
      ],
      recommendation: '建议买入 (置信度：75%) - 多数技术指标看涨'
    }
  },
  message: '成功获取 AAPL 技术指标分析'
}
```

**信号说明：**
- `STRONG_BUY` - 强烈买入（置信度≥70%）
- `BUY` - 建议买入（置信度 60-69%）
- `NEUTRAL` - 观望（置信度 40-59%）
- `SELL` - 建议卖出（置信度 60-69%）
- `STRONG_SELL` - 强烈卖出（置信度≥70%）

---

### getNews(symbol, options)

获取新闻聚合 + 情感分析 🎯 NEW!

**参数：**
- `symbol` (string): 股票代码
- `options` (Object): 选项
  - `limit` (number): 新闻数量限制（默认 10）
  - `sources` (Array): 新闻源列表
    - 'yahoo' - Yahoo Finance
    - 'google' - Google News
    - 'seekingalpha' - Seeking Alpha
  - `sentiment` (boolean): 是否进行情感分析（默认 true）

**返回：**
```javascript
{
  success: true,
  data: {
    symbol: 'AAPL',
    news: [
      {
        title: 'Apple Beats Q1 Earnings Expectations',
        summary: 'Apple Inc reported better-than-expected...',
        source: 'yahoo',
        publisher: 'Yahoo Finance',
        link: 'https://finance.yahoo.com/news/...',
        publishedAt: '2026-03-09T10:00:00.000Z',
        sentiment: {
          label: 'POSITIVE',
          score: 0.85,
          positive: 5,
          negative: 1
        }
      }
    ],
    sentimentStats: {
      positive: 6,
      negative: 2,
      neutral: 2,
      total: 10
    },
    overallSentiment: 'BULLISH',
    timestamp: '2026-03-09T12:00:00.000Z'
  },
  message: '成功获取 AAPL 新闻，共 10 条'
}
```

**情感标签：**
- `POSITIVE` - 利好（情感分≥0.6）
- `NEGATIVE` - 利空（情感分≤0.4）
- `NEUTRAL` - 中性（0.4-0.6）

**整体情感倾向：**
- `BULLISH` - 看涨（利好新闻≥60%）
- `SLIGHTLY_BULLISH` - 轻微看涨（40-60%）
- `NEUTRAL` - 中性
- `SLIGHTLY_BEARISH` - 轻微看跌（40-60%）
- `BEARISH` - 看跌（利空≥60%）

---

## 🌍 支持的市场

| 市场 | 代码格式 | 示例 |
|------|---------|------|
| **美股** | SYMBOL | AAPL, TSLA, NVDA |
| **港股** | SYMBOL.HK | 0700.HK, 9988.HK |
| **A 股** | SYMBOL.SS / SYMBOL.SZ | 600519.SS, 000001.SZ |
| **台股** | SYMBOL.TW | 2330.TW |
| **日股** | SYMBOL.T | 7203.T |
| **英股** | SYMBOL.L | HSBA.L |

---

## 🏗️ 项目架构

```
yahooclaw/
├── src/
│   ├── index.js                    # 主入口文件
│   └── modules/                    # 模块化架构
│       ├── Quote.js               # 股价查询模块
│       ├── History.js             # 历史数据模块
│       ├── Technical.js           # 技术指标模块
│       └── News.js                # 新闻聚合模块
├── test/
│   └── test-modules.js            # 模块测试
├── package.json
└── README.md
```

---

## ⚠️ 注意事项

1. **数据延迟**：Yahoo Finance 实时数据可能有 15 分钟延迟
2. **请求限制**：建议控制请求频率（< 100 次/小时）
3. **非商业用途**：Yahoo Finance API 仅供个人/研究使用
4. **错误处理**：始终检查 `success` 字段

---

## 🐛 故障排除

### 常见问题

**Q: 获取数据失败**
```javascript
// 检查股票代码格式
await yahooclaw.getQuote('AAPL');      // ✅ 正确
await yahooclaw.getQuote('AAPL.US');   // ❌ 错误
```

**Q: A 股/港股代码格式**
```javascript
// A 股
await yahooclaw.getQuote('600519.SS');  // 贵州茅台
await yahooclaw.getQuote('000001.SZ');  // 平安银行

// 港股
await yahooclaw.getQuote('0700.HK');    // 腾讯控股
await yahooclaw.getQuote('9988.HK');    // 阿里巴巴
```

**Q: 数据延迟**
- 这是正常现象
- 考虑使用付费 API 获取真正实时数据

---

## 📝 更新日志

### v0.0.3 (2026-03-11) 🆕

**功能增强：**
- ✅ 增强的错误处理，详细日志输出
- ✅ 健壮的数据解析，空值安全提取
- ✅ 更好的错误分类（限流、API 限制、数据错误）
- ✅ 改进的 API 故障转移逻辑
- ✅ 添加调试日志，便于故障排除
- ✅ API 限制时的优雅降级

**Bug 修复：**
- ✅ 修复历史数据解析错误
- ✅ 更好的限流处理
- ✅ 更友好的用户错误提示

**文档更新：**
- ✅ 更新使用示例
- ✅ 添加故障排除指南
- ✅ API 限制警告提示

### v0.0.2 (2026-03-11)

- ✅ 模块化架构（Quote, History, Technical, News 模块）
- ✅ Alpha Vantage 备用 API 集成
- ✅ API Manager 自动故障转移
- ✅ 智能缓存（5 分钟 TTL）
- ✅ 完整测试套件
- ✅ 中英文档

### v0.0.1 (2026-03-10)

- ✅ 初始版本发布
- ✅ 基础 Yahoo Finance 集成
- ✅ 实时股价查询
- ✅ 历史数据查询

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 👨‍💻 作者

**PocketAI for Leo** - OpenClaw Community

- GitHub: [@leohuang8688](https://github.com/leohuang8688)
- Project: [yahooclaw](https://github.com/leohuang8688/yahooclaw)

---

## 🙏 致谢

- [Yahoo Finance](https://finance.yahoo.com/) - 提供金融数据
- [yahoo-finance2](https://github.com/gadicc/node-yahoo-finance2) - Node.js 客户端
- [Alpha Vantage](https://www.alphavantage.co/) - 备用 API 提供商
- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent 框架

---

## 📞 支持

如有问题或建议，欢迎通过以下方式联系：

- GitHub Issues: [yahooclaw/issues](https://github.com/leohuang8688/yahooclaw/issues)
- OpenClaw Discord: [discord.gg/clawd](https://discord.gg/clawd)

---

**祝交易顺利！📈**
