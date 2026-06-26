# Fugle API Specifications

## Base URL
```
https://api.fugle.tw
```

## Authentication
All requests require the `X-API-Key` header:
```
X-API-Key: {your_api_key}
```

---

## Available Endpoints

### 1. Real-time Quote (即時報價)
**Endpoint:** `/intraday/quote/{symbol}`  
**Method:** GET

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| symbol* | string | Yes | Stock code (e.g., 2382) |
| type | string | No | Quote type: `oddlot` for zero-stock |

**Example:**
```bash
GET https://api.fugle.tw/intraday/quote/2382
```

---

### 2. Candles/K-Line (K 線數據)
**Endpoint:** `/candles/{symbol}`  
**Method:** GET

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| symbol* | string | Yes | Stock code |
| interval | string | No | Time interval: `1m`, `5m`, `15m`, `30m`, `1h`, `d`, `w` |
| start_time | string | No | Start date (YYYY-MM-DD) |
| end_time | string | No | End date (YYYY-MM-DD) |

---

### 3. Trades (成交明細)
**Endpoint:** `/trades/{symbol}`  
**Method:** GET

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| symbol* | string | Yes | Stock code |
| start_time | string | No | Start time (YYYY-MM-DD HH:MM:SS) |
| end_time | string | No | End time (YYYY-MM-DD HH:MM:SS) |

---

### 4. Technical Indicators (技術指標)

#### SMA (Simple Moving Average)
**Endpoint:** `/sma/{symbol}`  
**Parameters:** `period` (int)

#### RSI (Relative Strength Index)
**Endpoint:** `/rsi/{symbol}`  
**Parameters:** `period` (int, default: 14)

#### MACD (Moving Average Convergence Divergence)
**Endpoint:** `/macd/{symbol}`  
**Parameters:** 
- `fast_period` (int, default: 12)
- `slow_period` (int, default: 26)
- `signal_period` (int, default: 9)

#### KDJ (Stochastic Oscillator)
**Endpoint:** `/kdj/{symbol}`  
**Parameters:**
- `n` (int, default: 9)
- `m1` (int, default: 3)
- `m2` (int, default: 3)

#### BB (Bollinger Bands)
**Endpoint:** `/bb/{symbol}`  
**Parameters:**
- `period` (int, default: 20)
- `mult` (float, default: 2.0)

---

## Response Format

All responses are in JSON format with the following structure:
```json
{
  "status": "success",
  "data": { ... },
  "timestamp": "2025-01-30T10:00:00Z"
}
```

---

## Error Handling

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 401 | Unauthorized (missing/invalid API key) |
| 403 | Forbidden (rate limit exceeded) |
| 404 | Not Found (stock code not found) |
| 500 | Internal Server Error |

---

## Rate Limits

Rate limits depend on your subscription plan. Contact Fugle for details.
