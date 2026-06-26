# Usage Examples (cURL Format)

This file provides practical examples using cURL format for both APIs.

---

## Fugle API Examples

### 1. Get Real-time Quote (即時報價)

```bash
curl -X GET "https://api.fugle.tw/intraday/quote/2382" \
  -H "X-API-Key: {your_fugle_api_key}"
```

**Response Example:**
```json
{
  "status": "success",
  "data": {
    "symbol": "2382",
    "last_price": 378.0,
    "change": 5.0,
    "pct_change": 1.34,
    "open": 375.0,
    "high": 382.0,
    "low": 373.0,
    "volume": 12456
  }
}
```

---

### 2. Get K-Line Data (K 線數據)

```bash
curl -X GET "https://api.fugle.tw/candles/2382?interval=d&start_time=2025-01-01&end_time=2025-01-31" \
  -H "X-API-Key: {your_fugle_api_key}"
```

---

### 3. Get Technical Indicators (技術指標)

#### RSI (Relative Strength Index)
```bash
curl -X GET "https://api.fugle.tw/rsi/2382?period=14" \
  -H "X-API-Key: {your_fugle_api_key}"
```

#### MACD
```bash
curl -X GET "https://api.fugle.tw/macd/2382?fast_period=12&slow_period=26&signal_period=9" \
  -H "X-API-Key: {your_fugle_api_key}"
```

#### SMA (Simple Moving Average)
```bash
curl -X GET "https://api.fugle.tw/sma/2382?period=20" \
  -H "X-API-Key: {your_fugle_api_key}"
```

---

## FinMind API Examples

### 1. Get Stock Price (股價查詢)

```bash
curl -X GET "https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockPrice&data_id=2382&start_date=2025-01-01&end_date=2025-01-31" \
  -H "Authorization: Bearer {your_finmind_token}"
```

**Response Example:**
```json
{
  "msg": "success",
  "data": [
    {
      "date": "2025-01-02",
      "open": 346.5,
      "high": 352.0,
      "low": 343.0,
      "close": 347.5,
      "volume": 4586
    },
    {
      "date": "2025-01-03",
      "open": 348.0,
      "high": 355.0,
      "low": 345.0,
      "close": 352.0,
      "volume": 5234
    }
  ]
}
```

---

### 2. Get Monthly Revenue (月營收查詢)

```bash
curl -X GET "https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockMonthRevenue&data_id=2382&start_date=2025-01-01&end_date=2025-06-30" \
  -H "Authorization: Bearer {your_finmind_token}"
```

---

### 3. Get EPS & PER (EPS 與本益比查詢)

```bash
curl -X GET "https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockPER&data_id=2382" \
  -H "Authorization: Bearer {your_finmind_token}"
```

---

### 4. Get Financial Statements (財報查詢)

```bash
curl -X GET "https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockFinancialStatements&data_id=2382&start_date=2025-01-01" \
  -H "Authorization: Bearer {your_finmind_token}"
```

---

### 5. Get Institutional Investors Buy/Sell (三大法人買賣超)

```bash
curl -X GET "https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockInstitutionalInvestorsBuySell&data_id=2382&start_date=2025-01-01&end_date=2025-01-31" \
  -H "Authorization: Bearer {your_finmind_token}"
```

---

### 6. Get Margin Purchase & Short Sale (融資融券餘額)

```bash
curl -X GET "https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockMarginPurchaseShortSale&data_id=2382&start_date=2025-01-01&end_date=2025-01-31" \
  -H "Authorization: Bearer {your_finmind_token}"
```

---

## Combined Analysis Example (綜合分析範例)

To get a complete analysis of a stock, you can combine multiple API calls:

**Step 1:** Get real-time quote from Fugle
```bash
curl -X GET "https://api.fugle.tw/intraday/quote/2382" \
  -H "X-API-Key: {your_fugle_api_key}"
```

**Step 2:** Get historical price from FinMind
```bash
curl -X GET "https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockPrice&data_id=2382&start_date=2025-01-01&end_date=2025-01-31" \
  -H "Authorization: Bearer {your_finmind_token}"
```

**Step 3:** Get technical indicators from Fugle
```bash
curl -X GET "https://api.fugle.tw/rsi/2382?period=14" \
  -H "X-API-Key: {your_fugle_api_key}"
```

**Step 4:** Get financial data from FinMind
```bash
curl -X GET "https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockMonthRevenue&data_id=2382" \
  -H "Authorization: Bearer {your_finmind_token}"
```

---

## Notes

1. Replace `{your_fugle_api_key}` with your actual Fugle API key.
2. Replace `{your_finmind_token}` with your actual FinMind token.
3. Date format for FinMind is `YYYY-MM-DD`.
4. Rate limits apply - see individual API documentation for details.
