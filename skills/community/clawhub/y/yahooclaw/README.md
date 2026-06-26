# 🦞 YahooClaw - Yahoo Finance API for OpenClaw

> Empower OpenClaw with real-time stock quotes, financial data, and market analysis

[![Version](https://img.shields.io/github/v/tag/leohuang8688/yahooclaw?label=version&color=green)](https://github.com/leohuang8688/yahooclaw)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://github.com/openclaw/openclaw)

**[中文文档](README-CN.md)** | **[English Docs](README.md)**

---

## 🔒 Security

### Security Features
- ✅ No external API keys stored in code
- ✅ No sensitive data collection
- ✅ No shell command execution
- ✅ All API calls use HTTPS
- ✅ Rate limiting implemented
- ✅ Open source and auditable
- ⚠️ API keys via environment variables only

### Permissions Required
- **Network:** Yahoo Finance API (HTTPS only)
- **No Admin:** No root/admin privileges needed
- **No Shell:** No system command execution
- **No Database:** Uses in-memory caching only

---

## 📖 Introduction

**YahooClaw v1.0.0** is a production-ready Yahoo Finance API integration skill for OpenClaw.

### Features
- 📈 **Real-time Quotes** - US, HK, A-shares and global markets
- 📊 **Historical Data** - Multiple time periods
- 💰 **Dividends** - Complete dividend history
- 📰 **News Aggregation** - Multi-source news
- 📊 **Technical Indicators** - MA, RSI, MACD, BOLL, KDJ
- 🔄 **Auto Failover** - Backup API support

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd /root/.openclaw/workspace/skills/yahooclaw
npm install
```

### 2. Configure Environment (Optional)

```bash
# Alpha Vantage API Key (backup data source)
# Get from: https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

### 3. Use in OpenClaw

```javascript
// Import in your OpenClaw agent
import yahooclaw from './src/index.js';

// Query stock price
const quote = await yahooclaw.getQuote('AAPL');
console.log(`AAPL: $${quote.data.price}`);

// Query historical data
const history = await yahooclaw.getHistory('TSLA', '1mo');
console.log(history.data.quotes);
```

---

## 📚 API Reference

### getQuote(symbol)
- **symbol**: Stock code (e.g., AAPL, TSLA, 0700.HK)
- **Returns**: Real-time stock price, change, volume

### getHistory(symbol, period)
- **symbol**: Stock code
- **period**: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
- **Returns**: Historical stock price data

### getCompanyInfo(symbol)
- **symbol**: Stock code
- **Returns**: Company info, market cap, P/E ratio

### getDividends(symbol)
- **symbol**: Stock code
- **Returns**: Dividend history

---

## 🔧 Environment Variables

```bash
# Optional: Alpha Vantage API (backup)
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

**Note:** Yahoo Finance API works without API key. Alpha Vantage is optional backup.

---

## 📝 Notes

1. **Data Delay:** Yahoo Finance may have 15-minute delay
2. **Rate Limiting:** Built-in rate limiting
3. **Stock Codes:** 
   - US: AAPL, TSLA
   - HK: 0700.HK
   - A-Shares: 600519.SS

---

## 📝 Changelog

### v1.0.0 (2026-03-12)
- ✅ Production ready
- ✅ Security improvements
- ✅ Fixed documentation inconsistencies
- ✅ Clean dependencies

---

## 📄 License

MIT License

## 👨‍💻 Author

PocketAI for Leo - OpenClaw Community
