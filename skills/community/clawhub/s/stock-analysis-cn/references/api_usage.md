# API Usage Guide for Stock Analysis

This skill uses multiple free APIs to fetch financial data. This document documents usage patterns, rate limits, and error handling.

---

## 1. Tencent Finance API (腾讯财经)

### Base URL Patterns

#### Daily K-line (price + volume + PE/PB)
```
https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param={code},day,,,{count},qfq
```
- `{code}`: Stock/ETF code with market prefix (sh/sz)
- `{count}`: Number of trading days (max ~320)
- Example: `sh000001,day,,,250,qfq` → 上证指数250日数据

#### Real-time Quote (single ticker)
```
https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=now&param={code}
```
Returns latest price, change, volume, turnover.

#### Response Format
- JavaScript variable assignment: `kline_dayqfq={...}`
- JSON inside: `{ "code": 0, "data": { "sh000001": { "qfqday": [...], "qt": [...] } } }`
- `qt` array fields (important ones):
  - `[3]`: Latest price
  - `[22]`: Change amount (¥)
  - `[23]`: Change percent (%) with % sign
  - More: `[0]` name, `[2]` code, `[4]` turnover, etc.

### Parsing Example (Bash)
```bash
curl -s "$URL" | grep -o '"qt":\[[^]]*\]' | head -1 | tr -d '[]"' | awk -F, '{print $3, $23}'
# prints: price change_percent
```

### Rate Limits
- No official limit, but be reasonable: **≤ 10 requests/second**
- Use batch query when possible (some endpoints support multiple codes)

---

## 2. Eastmoney API (东方财富)

### Fund NAV and Info
Fund detail page data can be scraped from:
```
https://fund.eastmoney.com/pingzhongdata/{code}.js
```
Returns JavaScript with `Data_netWorthTrend` array containing:
- `fsRQ`: Date
- `jz`: Net asset value
- `ljjz`: Accumulated value
- `dwjz`: Daily growth (%)

**Note**: Requires parsing JS; better to use structured APIs if available.

### ETF List
```
https://fund.eastmoney.com/etf/
```
HTML page containing all ETF codes, names, tracking indices, AUM, management fees.

Parsing: use `grep`/`awk` or HTML parser to extract table rows.

### Rate Limits
- Standard web scraping: **1 request / 2 seconds** to avoid IP block
- Use retry with increasing delays

---

## 3. Jisilu API (集思录)

### ETF Data Export
Jisilu provides downloadable CSV via:
```
https://www.jisilu.cn/data/etf/#index
```
Export button → CSV with fields:
- 基金代码, 基金名称, 现价, 涨幅, 成交额(万元), 净值, 溢价率, 指数, ...

**Authenticated**: Requires login. Session cookie needed.

For automated access:
- Use Selenium/Playwright to login and fetch page
- Or ask user to provide session cookie (not recommended for security)

---

## 4. Index Constituents

### CSI (中证指数公司)
Constituent list and weights:
```
http://www.csindex.com.cn/#/indices/family/detail?code={index_code}
```
- `index_code`: e.g., 000300 (沪深300)
- Data in JSON within HTML; may require reverse engineering

### SSE (上海证券交易所)
```
http://www.sse.com.cn/indexconst/excel/{index_code}.xls
```
Direct Excel download for some indices (上证50, 上证180)

---

## 5. Error Handling & Best Practices

### Retry Strategy
- Network errors: exponential backoff (2s, 4s, 8s)
- HTTP 429: honor `Retry-After` header or wait 10s
- HTTP 5xx: retry after 30s, then give up

### Caching
- Cache static data (index constituents, ETF lists) for 24 hours
- Cache daily prices to avoid re-fetching same day data
- Use file-based cache: `cache/{ticker}_{date}.json`

### Data Validation
- Check for null/NaN values
- Verify price continuity (no gaps > 10% unless suspension)
- Cross-validate volume from multiple sources if possible

---

## 6. Example: Fetch PE via Tencent API

```bash
#!/bin/bash
# Get PE for a single index
ticker="sh000300"
url="https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=${ticker},day,,,1,qfq"
response=$(curl -s "$url")
# Extract pe field
pe=$(echo "$response" | grep -o '"pe":"[^"]*"' | head -1 | cut -d: -f2 | tr -d '"')
echo "PE: $pe"
```

---

## 7. Limitations

- **Data freshness**: Free APIs may have 15-min delay for real-time quotes
- **History depth**: Tencent provides ~320 days only; longer history requires alternate sources or premium APIs (Wind, iFinD)
- **Fundamental data**: Quarterly financials may be delayed 1-2 days after release
- **Rate limits**: May be throttled during heavy usage

---

## 8. Future Enhancements

- **Wind/iFinD integration** (with user-provided credentials if permitted)
- **JoinQuant/聚宽 API** for factor data
- **Tushare** (though now requiring token)
- **CSIndex official API** (if available)

---

## 9. Security Notes

- Never hardcode API keys in scripts; use environment variables or config files
- Protect user credentials; this skill does not require personal login
- All external requests should be logged (for debugging)

---

For questions or to add new data sources, consult the skill maintainer.
