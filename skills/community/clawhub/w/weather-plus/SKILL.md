---
name: weather-plus
description: >
  Get current weather, multi-day forecasts, clothing index, and feels-like temperature.
  No API key required. Use when a user wants to: (1) Check current weather,
  (2) View multi-day forecasts, (3) Get clothing/dressing recommendations,
  (4) Check feels-like temperature and comfort index.
  Supports any city worldwide. Integrates SkillPay.me at 0.001 USDT/call.
---

# Weather Plus

Weather, forecasts, clothing index & feels-like temperature. No API key needed. 0.001 USDT/call.

## Commands

| Command | Script | Description |
|:---|:---|:---|
| **weather** | `scripts/weather.py` | Current weather + feels-like |
| **forecast** | `scripts/forecast.py` | Multi-day forecast (up to 7 days) |
| **clothing** | `scripts/clothing.py` | Clothing/dressing index + recommendations |
| **billing** | `scripts/billing.py` | SkillPay charge/balance/payment |

## Workflow

```
1. Billing:   python3 scripts/billing.py --charge --user-id <id>
2. Weather:   python3 scripts/weather.py --city "Beijing"
3. Forecast:  python3 scripts/forecast.py --city "Shanghai" --days 5
4. Clothing:  python3 scripts/clothing.py --city "Chengdu"
```

## Examples

```bash
# Current weather
python3 scripts/weather.py --city "New York"
python3 scripts/weather.py --city "成都"

# Multi-day forecast
python3 scripts/forecast.py --city "Tokyo" --days 7

# Clothing index
python3 scripts/clothing.py --city "Beijing"
python3 scripts/clothing.py --city "London"
```

## Config

| Env Var | Required | Description |
|:---|:---:|:---|
| `SKILLPAY_API_KEY` | Yes | SkillPay.me API key |

## References

See `references/clothing-index.md` for dressing recommendation methodology.
