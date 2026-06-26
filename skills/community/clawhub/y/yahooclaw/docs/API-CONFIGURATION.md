# 🔌 API Configuration

YahooClaw supports multiple data sources with automatic failover for reliable data access.

---

## 📊 Available Data Sources

| API Provider | Free Tier | Rate Limit | Status |
|-------------|-----------|------------|--------|
| **Yahoo Finance** | Free | ~100 calls/hour | ✅ Primary |
| **Alpha Vantage** | 500 calls/day | 5 calls/min | ✅ Backup |

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Alpha Vantage API Key (Optional but recommended)
# Get your free API key at: https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_API_KEY=your_api_key_here

# API Manager Settings (Optional)
API_TIMEOUT=10000          # Request timeout in milliseconds
API_CACHE_TTL=300000       # Cache duration in milliseconds (5 min)
API_CACHE_ENABLED=true     # Enable/disable caching
```

### Default Behavior

- **Primary API:** Yahoo Finance
- **Fallback API:** Alpha Vantage
- **Auto-failover:** Automatic when primary API fails or rate-limited
- **Caching:** Enabled by default (5 minutes)

---

## 🔄 Automatic Failover

The API Manager automatically handles failover:

```javascript
import yahooclaw from './src/index.js';

// When Yahoo Finance is rate-limited, automatically falls back to Alpha Vantage
const quote = await yahooclaw.getQuote('AAPL');
console.log(`Data source: ${quote.source}`); // "YahooFinance" or "AlphaVantage"
```

**Failover Logic:**
1. Try Yahoo Finance first
2. If rate-limited or failed → Try Alpha Vantage
3. Return best available result
4. Cache successful response

---

## 💾 Caching

### How It Works

- **Cache Duration:** 5 minutes (configurable)
- **Cache Key:** `method:symbol:period`
- **Auto-clear:** Expired entries removed automatically

### Manual Cache Control

```javascript
import { APIManager } from './src/api/APIManager.js';

const apiManager = new APIManager();

// Clear cache
apiManager.clearCache();

// View cache statistics
const stats = apiManager.getStats();
console.log(stats);
// {
//   total: 100,
//   success: 95,
//   failed: 5,
//   successRate: '95.00%',
//   byAPI: {
//     YahooFinance: { total: 80, success: 75, failed: 5 },
//     AlphaVantage: { total: 20, success: 20, failed: 0 }
//   },
//   cacheSize: 15
// }
```

---

## 🎯 Custom API Configuration

### Use Only Alpha Vantage

```javascript
import { AlphaVantageAPI } from './src/api/AlphaVantage.js';

const alphaVantage = new AlphaVantageAPI({
  apiKey: 'your_api_key',
  timeout: 15000
});

const quote = await alphaVantage.getQuote('AAPL');
```

### Custom API Manager

```javascript
import { APIManager } from './src/api/APIManager.js';

const apiManager = new APIManager({
  primary: 'AlphaVantage',      // Use Alpha Vantage as primary
  fallback: ['YahooFinance'],   // Fallback to Yahoo Finance
  timeout: 15000,               // 15 second timeout
  cache: true,                  // Enable caching
  cacheTTL: 600000              // 10 minute cache
});

const quote = await apiManager.getQuote('AAPL');
```

---

## 📈 API Comparison

### Yahoo Finance

**Pros:**
- ✅ Real-time data
- ✅ Comprehensive data (quotes, history, news, fundamentals)
- ✅ Global market coverage
- ✅ No API key required

**Cons:**
- ❌ Rate limiting (~100 calls/hour)
- ❌ Unofficial API (may change)
- ❌ 15-minute delay on some data

**Best For:** Primary data source, comprehensive queries

---

### Alpha Vantage

**Pros:**
- ✅ Official API
- ✅ Stable and reliable
- ✅ Good for technical indicators
- ✅ 500 calls/day free

**Cons:**
- ❌ Lower rate limit (5 calls/min)
- ❌ Limited news data
- ❌ Requires API key for full access

**Best For:** Backup source, technical analysis, historical data

---

## 🐛 Troubleshooting

### Rate Limiting

**Symptom:** `Error: RATE_LIMIT`

**Solutions:**
1. Wait 5-10 minutes for limits to reset
2. Enable caching (reduces duplicate requests)
3. Use Alpha Vantage API key for higher limits
4. Reduce request frequency

### API Key Issues

**Symptom:** `Error: Invalid API key`

**Solutions:**
1. Check `.env` file exists
2. Verify API key is correct
3. Ensure Alpha Vantage account is active
4. Check API key permissions

### Timeout Errors

**Symptom:** `Error: Request timeout (10000ms)`

**Solutions:**
1. Increase timeout in configuration
2. Check network connection
3. Try alternative API source
4. Enable caching to reduce requests

---

## 📊 Performance Tips

### 1. Enable Caching

```javascript
const apiManager = new APIManager({
  cache: true,
  cacheTTL: 300000  // 5 minutes
});
```

### 2. Batch Requests

```javascript
// Instead of multiple individual requests
const [aapl, tsla, nvda] = await Promise.all([
  yahooclaw.getQuote('AAPL'),
  yahooclaw.getQuote('TSLA'),
  yahooclaw.getQuote('NVDA')
]);
```

### 3. Use Appropriate Periods

```javascript
// Use shorter periods for recent data
await yahooclaw.getHistory('AAPL', '5d');   // Fast
await yahooclaw.getHistory('AAPL', '5y');   // Slower
```

---

## 🔑 Getting Alpha Vantage API Key

1. Visit: https://www.alphavantage.co/support/#api-key
2. Fill in the form (free)
3. Receive API key via email instantly
4. Add to `.env` file:
   ```bash
   ALPHA_VANTAGE_API_KEY=your_api_key_here
   ```

**Free Tier Limits:**
- 500 requests/day
- 5 requests/minute
- Sufficient for most use cases

---

## 📈 Monitoring API Usage

```javascript
// Check API statistics
const stats = apiManager.getStats();

console.log(`Total Requests: ${stats.total}`);
console.log(`Success Rate: ${stats.successRate}`);
console.log(`Cache Size: ${stats.cacheSize}`);
console.log('By API:', stats.byAPI);
```

---

## 🚀 Best Practices

1. **Always use caching** - Reduces API calls by 60-80%
2. **Set reasonable timeouts** - 10-15 seconds recommended
3. **Monitor rate limits** - Check stats regularly
4. **Have backup plan** - API Manager handles this automatically
5. **Use environment variables** - Keep API keys secure
6. **Batch requests** - Use Promise.all for multiple queries
7. **Choose appropriate data sources** - Yahoo for real-time, Alpha Vantage for indicators

---

## 📞 Support

For API-related issues:

- **Yahoo Finance:** Unofficial API, no official support
- **Alpha Vantage:** https://www.alphavantage.co/support/
- **GitHub Issues:** https://github.com/leohuang8688/yahooclaw/issues

---

**Happy Coding! 📈**
