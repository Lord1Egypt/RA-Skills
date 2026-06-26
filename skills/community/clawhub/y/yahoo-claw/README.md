# 🦞 YahooClaw - Yahoo Finance API for OpenClaw

> Empower OpenClaw with real-time stock quotes, financial data, and market analysis

[![Version](https://img.shields.io/github/v/tag/leohuang8688/yahooclaw?label=version&color=green)](https://github.com/leohuang8688/yahooclaw)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://github.com/openclaw/openclaw)

**[中文文档](README-CN.md)** | **[English Docs](README.md)**

---

## 📖 Introduction

**YahooClaw v0.0.3** is a production-ready Yahoo Finance API integration skill for OpenClaw, featuring:

- 📈 **Real-time Quotes** - US, HK, A-shares and global markets
- 📊 **Historical Data** - Multiple time periods (1d to max)
- 💰 **Dividends** - Complete dividend history
- 📉 **Financial Statements** - Balance sheet, income statement, cash flow
- 🔍 **Stock Search** - Quick stock code lookup
- 📰 **News Aggregation** - Multi-source news with sentiment analysis
- 📊 **Technical Indicators** - 7 major indicators (MA, RSI, MACD, BOLL, KDJ)
- 🔄 **Auto Failover** - Automatic switch to backup API on rate limits
- 💾 **Smart Caching** - 5-minute TTL for 30x speed improvement

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd /root/.openclaw/workspace/skills/yahooclaw
npm install
```

### 2. Configure Environment (Optional)

Create `.env` file for backup API:

```bash
# Alpha Vantage API Key (500 calls/day free)
ALPHA_VANTAGE_API_KEY=your_api_key_here

# API Manager Settings
API_TIMEOUT=10000          # Request timeout (ms)
API_CACHE_TTL=300000       # Cache duration (5 min)
API_CACHE_ENABLED=true     # Enable caching
```

### 3. Use in OpenClaw

```javascript
// Import in your OpenClaw agent
import yahooclaw from './skills/yahooclaw/src/index.js';

// Query stock price
const aapl = await yahooclaw.getQuote('AAPL');
console.log(`AAPL: $${aapl.data.price}`);

// Query historical data
const tsla = await yahooclaw.getHistory('TSLA', '1mo');
console.log(tsla.data.quotes);

// Technical analysis
const nvda = await yahooclaw.getTechnicalIndicators('NVDA', '1mo', ['MA', 'RSI', 'MACD']);
console.log(nvda.data.analysis.recommendation);

// News with sentiment
const msft = await yahooclaw.getNews('MSFT', { limit: 5, sentiment: true });
console.log(msft.data.overallSentiment);
```

### 4. Use via OpenClaw Conversation

```
User: Query Apple stock price
PocketAI: Sure, querying AAPL...
        Apple Inc. (AAPL) current price: $260.83
        Change: +$0.95 (+0.37%) 📈
        Market Cap: $2.73T
```

---

## 📚 API Documentation

### getQuote(symbol)

Get real-time stock quote

**Parameters:**
- `symbol` (string): Stock code, e.g., 'AAPL', 'TSLA', '0700.HK'

**Returns:**
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
  message: 'Successfully retrieved AAPL quote data'
}
```

**Example:**
```javascript
const quote = await yahooclaw.getQuote('AAPL');
console.log(`AAPL: $${quote.data.price}`);
```

---

### getHistory(symbol, period)

Get historical stock price data

**Parameters:**
- `symbol` (string): Stock code
- `period` (string): Time period
  - '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'

**Returns:**
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
  message: 'Successfully retrieved TSLA 1mo historical data, 30 records'
}
```

---

### getTechnicalIndicators(symbol, period, indicators)

Get technical analysis indicators 🎯

**Parameters:**
- `symbol` (string): Stock code
- `period` (string): Time period
- `indicators` (Array): Technical indicators list
  - 'MA' - Moving Average
  - 'EMA' - Exponential Moving Average
  - 'RSI' - Relative Strength Index
  - 'MACD' - Moving Average Convergence Divergence
  - 'BOLL' - Bollinger Bands
  - 'KDJ' - Stochastic Oscillator
  - 'Volume' - Volume analysis

**Returns:**
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
        'MA5: BULLISH',
        'RSI: BULLISH',
        'MACD: BULLISH',
        'MACD: GOLDEN CROSS'
      ],
      recommendation: 'BUY (Confidence: 75%) - Most technical indicators are bullish'
    }
  },
  message: 'Successfully retrieved AAPL technical indicators'
}
```

**Signal Levels:**
- `STRONG_BUY` - Strong buy (confidence ≥70%)
- `BUY` - Buy (confidence 60-69%)
- `NEUTRAL` - Hold (confidence 40-59%)
- `SELL` - Sell (confidence 60-69%)
- `STRONG_SELL` - Strong sell (confidence ≥70%)

---

### getNews(symbol, options)

Get news aggregation with sentiment analysis 🎯 NEW!

**Parameters:**
- `symbol` (string): Stock code
- `options` (Object): Options
  - `limit` (number): News limit (default 10)
  - `sources` (Array): News sources
    - 'yahoo' - Yahoo Finance
    - 'google' - Google News
    - 'seekingalpha' - Seeking Alpha
  - `sentiment` (boolean): Enable sentiment analysis (default true)

**Returns:**
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
  message: 'Successfully retrieved AAPL news, 10 articles'
}
```

**Sentiment Labels:**
- `POSITIVE` - Bullish (score ≥0.6)
- `NEGATIVE` - Bearish (score ≤0.4)
- `NEUTRAL` - Neutral (0.4-0.6)

**Overall Sentiment:**
- `BULLISH` - Bullish (positive news ≥60%)
- `SLIGHTLY_BULLISH` - Slightly bullish (40-60%)
- `NEUTRAL` - Neutral
- `SLIGHTLY_BEARISH` - Slightly bearish (40-60%)
- `BEARISH` - Bearish (negative news ≥60%)

---

## 🌍 Supported Markets

| Market | Code Format | Examples |
|--------|-------------|----------|
| **US Stocks** | SYMBOL | AAPL, TSLA, NVDA |
| **HK Stocks** | SYMBOL.HK | 0700.HK, 9988.HK |
| **A-Shares** | SYMBOL.SS / SYMBOL.SZ | 600519.SS, 000001.SZ |
| **Taiwan** | SYMBOL.TW | 2330.TW |
| **Japan** | SYMBOL.T | 7203.T |
| **UK** | SYMBOL.L | HSBA.L |

---

## 🏗️ Architecture

```
yahooclaw/
├── src/
│   ├── index.js                    # Main entry point
│   └── modules/                    # Modular architecture
│       ├── Quote.js               # Real-time quotes
│       ├── History.js             # Historical data
│       ├── Technical.js           # Technical indicators
│       └── News.js                # News aggregation
├── test/
│   └── test-modules.js            # Module tests
├── package.json
└── README.md
```

---

## ⚠️ Notes

1. **Data Delay**: Yahoo Finance real-time data may have 15-minute delay
2. **Rate Limits**: Control request frequency to avoid rate limiting (< 100 requests/hour)
3. **Non-commercial Use**: Yahoo Finance API for personal/research use only
4. **Error Handling**: Always check `success` field

---

## 🐛 Troubleshooting

### Common Issues

**Q: Failed to get data**
```javascript
// Check stock code format
await yahooclaw.getQuote('AAPL');      // ✅ Correct
await yahooclaw.getQuote('AAPL.US');   // ❌ Incorrect
```

**Q: A-Share/HK Stock code format**
```javascript
// A-Shares
await yahooclaw.getQuote('600519.SS');  // Kweichow Moutai
await yahooclaw.getQuote('000001.SZ');  // Ping An Bank

// HK Stocks
await yahooclaw.getQuote('0700.HK');    // Tencent
await yahooclaw.getQuote('9988.HK');    // Alibaba
```

**Q: Data delay**
- This is normal
- Consider paid API for real-time data

---

## 📝 Changelog

### v0.0.3 (2026-03-11) 🆕

**Enhancements:**
- ✅ Enhanced error handling with detailed logging
- ✅ Robust data parsing with null-safe extraction
- ✅ Better error classification (rate limit, API limit, data errors)
- ✅ Improved API failover logic
- ✅ Added debug logging for troubleshooting
- ✅ Graceful degradation on API limits

**Bug Fixes:**
- ✅ Fixed historical data parsing errors
- ✅ Better rate limit handling
- ✅ Improved error messages for users

**Documentation:**
- ✅ Updated usage examples
- ✅ Added troubleshooting guide
- ✅ API limit warnings

### v0.0.2 (2026-03-11)

- ✅ Modular architecture (Quote, History, Technical, News modules)
- ✅ Alpha Vantage backup API integration
- ✅ API Manager with automatic failover
- ✅ Smart caching (5 min TTL)
- ✅ Comprehensive test suite
- ✅ English & Chinese documentation

### v0.0.1 (2026-03-10)

- ✅ Initial release
- ✅ Basic Yahoo Finance integration
- ✅ Real-time quotes
- ✅ Historical data

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 👨‍💻 Author

**PocketAI for Leo** - OpenClaw Community

- GitHub: [@leohuang8688](https://github.com/leohuang8688)
- Project: [yahooclaw](https://github.com/leohuang8688/yahooclaw)

---

## 🙏 Acknowledgments

- [Yahoo Finance](https://finance.yahoo.com/) - Financial data provider
- [yahoo-finance2](https://github.com/gadicc/node-yahoo-finance2) - Node.js client
- [Alpha Vantage](https://www.alphavantage.co/) - Backup API provider
- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent framework

---

## 📞 Support

For issues or suggestions:

- GitHub Issues: [yahooclaw/issues](https://github.com/leohuang8688/yahooclaw/issues)
- OpenClaw Discord: [discord.gg/clawd](https://discord.gg/clawd)

---

**Happy Trading! 📈**
