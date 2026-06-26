---
name: tw-stock-info
description: Taiwan stock info using Fugle or FinMind APIs. Provides real-time quotes, historical data, financial statements, and technical indicators for Taiwan stocks.
---

# Taiwan Stock Info

## Overview

Complete Taiwan stock analysis tool using Fugle and FinMind APIs. Provides real-time quotes, historical data, financial statements, and technical indicators for Taiwan stocks.

---

## API Endpoints Summary

### Fugle API (Real-time & Technical)
- **Base URL:** `https://api.fugle.tw`
- **Authentication:** Header `X-API-Key: {your_api_key}`
- **Features:** Real-time quotes, candles, trades, technical indicators

### FinMind API (Historical & Financial Data)
- **Base URL:** `https://api.finmindtrade.com/api/v4/data`
- **Authentication:** Header `Authorization: Bearer {your_token}`
- **Features:** Historical prices, financial statements, revenue, EPS

---

## Usage Examples

See [examples.md](./examples.md) for detailed usage examples.

---

## File Structure

```
tw-stock-analysis/
├── SKILL.md          (This file - API overview)
├── api/
│   ├── fugle.md      (Fugle API specifications)
│   └── finmind.md    (FinMind API specifications)
└── examples.md       (Usage examples in cURL format)
```

---

## Rate Limits

| API | Unverified | Verified |
|-----|------------|----------|
| Fugle | Plan-dependent | Contact provider |
| FinMind | 300/hour | 600/hour |

