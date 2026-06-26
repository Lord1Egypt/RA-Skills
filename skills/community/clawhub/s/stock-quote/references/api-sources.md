# Stock Data API Sources

## Free APIs (No Key Required)

### Stooq ⭐ RECOMMENDED
- **URL**: `https://stooq.com/q/l/?s=SYMBOL.us&f=sd2t2ohlc&h=&t=csv`
- **Rate Limit**: Unknown (generous)
- **Data**: EOD prices (Open, High, Low, Close, Date, Time)
- **Coverage**: US stocks (add `.us` suffix)
- **Reliability**: ⭐⭐⭐⭐⭐ (best for US stocks, no key needed)
- **Format**: CSV

```bash
# Example: Fetch UNH price
curl -sL "https://stooq.com/q/l/?s=unh.us&f=sd2t2ohlc&h=&t=csv"
# Returns: Symbol,Date,Time,Open,High,Low,Close
#          UNH.US,2026-03-31,22:00:25,262.75,271.865,262.61,270.49
```

### Yahoo Finance (via yfinance)
- **Library**: `pip install yfinance`
- **Rate Limit**: ~2000 requests/day (unofficial)
- **Data**: Price, fundamentals, historical, options
- **Coverage**: US, international markets
- **Reliability**: ⭐⭐⭐⭐ (best free option)

```python
import yfinance as yf
ticker = yf.Ticker("AAPL")
info = ticker.fast_info
```

### Yahoo Finance (Web Scrape)
- **URL**: `https://finance.yahoo.com/quote/{SYMBOL}`
- **Rate Limit**: Unknown (use sparingly)
- **Data**: Price, basic stats
- **Reliability**: ⭐⭐ (HTML changes may break parser)

## Free APIs (Key Required)

### Alpha Vantage
- **URL**: https://www.alphavantage.co
- **Free Tier**: 25 requests/day, 5 requests/min
- **Data**: Real-time, historical, fundamentals, FX, crypto
- **Key**: Free signup required

```python
import requests
url = "https://www.alphavantage.co/query"
params = {
    "function": "GLOBAL_QUOTE",
    "symbol": "AAPL",
    "apikey": "YOUR_KEY"
}
response = requests.get(url, params=params)
```

### Financial Modeling Prep
- **URL**: https://financialmodelingprep.com
- **Free Tier**: 250 requests/day
- **Data**: Price, financials, ratios, insider trading
- **Key**: Free signup required

### IEX Cloud
- **URL**: https://iexcloud.io
- **Free Tier**: Limited (sandbox available)
- **Data**: Real-time, fundamentals, news
- **Key**: Signup required

## Paid APIs (Production)

### Polygon.io
- **Pricing**: $29/month starter
- **Data**: Real-time, historical, options, forex, crypto
- **Best for**: Production applications

### Twelve Data
- **Pricing**: Free tier available, paid from $29/month
- **Data**: Real-time, historical, fundamentals
- **Best for**: Balanced price/features

## Recommendations

| Use Case | Recommended Source |
|----------|-------------------|
| US stocks (EOD prices) | **Stooq** (free, no key, reliable) |
| Personal/portfolio tracking | Stooq or yfinance |
| Intraday prices | yfinance (during market hours) |
| Fundamental data (PE, etc.) | yfinance or FMP (with key) |
| Production app | Polygon.io or Twelve Data |
| Historical data | Alpha Vantage or yfinance |

## Rate Limiting Best Practices

1. **Cache results**: Store prices for 15-30 minutes during market hours
2. **Batch requests**: Query multiple symbols in single call when possible
3. **Off-peak updates**: Run daily portfolio updates after market close
4. **Error backoff**: Exponential backoff on rate limit errors

## Market Hours (NYSE/NASDAQ)

- **Open**: 9:30 AM ET
- **Close**: 4:00 PM ET
- **Pre-market**: 4:00 AM - 9:30 AM ET
- **After-hours**: 4:00 PM - 8:00 PM ET
- **Closed**: Weekends, market holidays

Prices outside market hours reflect last traded price or after-hours trading.
