# realtime-finance-data

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_finance_data.yaml

**Host:** `real-time-finance-data.p.rapidapi.com`
**Notes:** Returns all matching results in a single call. No pagination.

## Endpoints

### GET /search
Search

**Required:**
- `query` (string)

**Optional:**
- `language` (string, default: en) Example: `en`

**Pagination:** none
**Response path:** `data`
**Key fields:** symbol

---

### GET /market-trends
Market Trends

**Required:**
- `trend_type` (string) Example: `MARKET_INDEXES`

**Optional:**
- `country` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`

**Pagination:** none
**Response path:** `data`
**Key fields:** article_title

---

### GET /stock-quote
Stock Quote

**Required:**
- `symbol` (string)

**Optional:**
- `language` (string, default: en) Example: `en`

**Pagination:** none

---

### GET /stock-time-series
Stock Time Series

**Required:**
- `symbol` (string)

**Optional:**
- `period` (string) Example: `1D`
- `language` (string, default: en) Example: `en`

**Pagination:** none

---

### GET /stock-news
Stock News

**Required:**
- `symbol` (string)

**Optional:**
- `language` (string, default: en) Example: `en`

**Pagination:** none
**Response path:** `data`
**Key fields:** article_title

---

### GET /stock-overview
Stock / Company Overview

**Required:**
- `symbol` (string)

**Optional:**
- `language` (string, default: en) Example: `en`

**Pagination:** none

---

### GET /company-income-statement
Company Income Statement

**Required:**
- `symbol` (string)

**Optional:**
- `period` (string)
- `language` (string, default: en) Example: `en`

**Pagination:** none
**Response path:** `data`
**Key fields:** date

---

### GET /company-balance-sheet
Company Balance Sheet

**Required:**
- `symbol` (string)

**Optional:**
- `period` (string)
- `language` (string, default: en) Example: `en`

**Pagination:** none
**Response path:** `data`
**Key fields:** date

---

### GET /company-cash-flow
Company Cash Flow

**Required:**
- `symbol` (string)

**Optional:**
- `period` (string)
- `language` (string, default: en) Example: `en`

**Pagination:** none
**Response path:** `data`
**Key fields:** date

---

### GET /currency-exchange-rate
Currency Exchange Rate

**Required:**
- `from_symbol` (string) Example: `USD`
- `to_symbol` (string) Example: `EUR`

**Optional:**
- `language` (string, default: en) Example: `en`

**Pagination:** none

---

### GET /currency-time-series
Currency Time Series

**Required:**
- `from_symbol` (string) Example: `USD`
- `to_symbol` (string) Example: `EUR`

**Optional:**
- `period` (string) Example: `1D`
- `language` (string, default: en) Example: `en`

**Pagination:** none

---

### GET /currency-news
Currency News

**Required:**
- `from_symbol` (string) Example: `USD`
- `to_symbol` (string) Example: `EUR`

**Optional:**
- `language` (string, default: en) Example: `en`

**Pagination:** none
**Response path:** `data`
**Key fields:** article_title

---

### GET /stock-quote-yahoo-finance
Stock Quote (Yahu Finance)

**Required:**
- `symbol` (string) Example: `AAPL`

**Pagination:** none
**Response path:** `data`
**Key fields:** symbol

---

### GET /stock-time-series-yahoo-finance
Stock Time Series (Yahu Finance)

**Required:**
- `symbol` (string)

**Optional:**
- `period` (string) Example: `1D`

**Pagination:** none
**Response path:** `data`
**Key fields:** datetime

---
