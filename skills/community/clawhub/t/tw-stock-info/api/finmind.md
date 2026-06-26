# FinMind API Specifications

## Base URL
```
https://api.finmindtrade.com/api/v4/data
```

## Authentication
All requests can include the `Authorization` header to increase rate limit:
```
Authorization: Bearer {your_token}
```

---

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| dataset* | string | Yes | Dataset name (see list below) |
| data_id | string | No | Stock code/target ID (e.g., 2382) |
| start_date | string | Partial | Start date (YYYY-MM-DD) |
| end_date | string | Partial | End date (YYYY-MM-DD) |

**Note:** At least one of `start_date` or `end_date` must be provided.

---

## Available Datasets

### Taiwan Stock: General & Technical (台股總覽與技術面)

| Dataset Name | Description |
|--------------|-------------|
| `TaiwanStockInfo` | Taiwan Stock Info / 股票代號清單 |
| `TaiwanStockPrice` | Daily Price / 股價日線 |
| `TaiwanStockTick` | Tick Data / 逐筆交易資料 |
| `TaiwanStockPER` | PER, PBR & Dividend Yield / 本益比、股價淨值比及殖利率 |

### Taiwan Stock: Fundamental (台股基本面)

| Dataset Name | Description |
|--------------|-------------|
| `TaiwanStockFinancialStatements` | Financial Statements / 綜合損益表 |
| `TaiwanStockBalanceSheet` | Balance Sheet / 資產負債表 |
| `TaiwanStockCashFlowsStatement` | Cash Flows Statement / 現金流量表 |
| `TaiwanStockMonthRevenue` | Monthly Revenue / 月營收 |
| `TaiwanStockDividend` | Dividend Policy / 股利政策表 |
| `TaiwanStockDividendResult` | Dividend Result / 除權除息結果表 |

### Taiwan Stock: Institutional & Margin (台股籌碼面)

| Dataset Name | Description |
|--------------|-------------|
| `TaiwanStockInstitutionalInvestorsBuySell` | Institutional Investors Buy/Sell / 三大法人買賣超 |
| `TaiwanStockMarginPurchaseShortSale` | Margin Purchase & Short Sale / 融資融券餘額 |
| `TaiwanStockShareholding` | Shareholding Distribution / 股權分散表 |
| `TaiwanStockHoldingSharesPer` | Foreign Investor Holding Percentage / 外資持股比例 |
| `TaiwanStockSecuritiesLending` | Securities Lending / 借券成交明細 |

### Global & Macroeconomics (國際市場與總經)

| Dataset Name | Description |
|--------------|-------------|
| `USStockPrice` | US Stock Daily Price / 美股日線 |
| `TaiwanFuturesDaily` | Taiwan Futures Daily Data / 期貨日線 |
| `TaiwanOptionDaily` | Taiwan Options Daily Data / 選擇權日線 |
| `ExchangeRate` | Exchange Rates / 各國貨幣匯率 |
| `GoldPrice` | Gold Price / 黃金價格 |

---

## Example Requests

### Get Stock Price (股價查詢)
```bash
GET https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockPrice&data_id=2382&start_date=2025-01-01&end_date=2025-01-31

Headers:
Authorization: Bearer {your_token}
```

### Get Monthly Revenue (月營收查詢)
```bash
GET https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockMonthRevenue&data_id=2382&start_date=2025-01-01&end_date=2025-01-31

Headers:
Authorization: Bearer {your_token}
```

### Get EPS (EPS 查詢)
```bash
GET https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockPER&data_id=2382&start_date=2025-01-01&end_date=2025-01-31

Headers:
Authorization: Bearer {your_token}
```

---

## Response Format

All responses are in JSON format with the following structure:
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
    }
  ]
}
```

---

## Error Handling

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 401 | Unauthorized (missing/invalid token) |
| 429 | Too Many Requests (rate limit exceeded) |
| 500 | Internal Server Error |

---

## Rate Limits

| Type | Limit |
|------|-------|
| Unverified (no token) | 300/hour |
| Verified (with token) | 600/hour |
