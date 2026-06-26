---
name: simmer-weather-trader
description: Automated weather prediction market trading skill for Simmer/Polymarket. Cross-references 4 weather sources (NOAA, Open-Meteo, Wunderground, NVIDIA FourcastNet) and only trades when all forecasts agree within ±1°F. Remixable — add your own data sources or adjust the confidence thresholds.
author: "Joe"
version: "1.0.0"
displayName: "Simmer Weather Trader"
difficulty: "advanced"
---

# Simmer Weather Trader

An automated trading bot for Simmer weather prediction markets. Fetches active weather markets, cross-references temperature forecasts from **4 independent sources**, and only trades when the consensus is strong.

## How it works

1. **Market Discovery** — fetches active weather markets from Simmer via the SDK
2. **Multi-Source Forecast** — gets high temperature predictions from:
   - **NOAA** (US government weather API)
   - **Open-Meteo** (free global weather API)
   - **Wunderground** (scraped via Playwright for broader coverage)
   - **NVIDIA FourcastNet** (physics-based atmospheric model)
3. **Confidence Scoring** — computes a 0–100 score based on:
   - Source agreement (all within ±1°F)
   - Market bucket fit
   - Simmer edge recommendation
   - Time to resolution
4. **Execution** — only trades when score reaches 100 (maximum confidence)

## Default signal

The default strategy is **conservative multi-source consensus**:
- All 3 weather sources must agree within ±1°F
- FourcastNet must confirm the bucket
- Simmer edge must recommend TRADE
- Only YES trades (betting the temp falls within the market bucket)

> **This is a template.** The default signal uses 4 weather models. Remix it by:
> - Adding more weather sources (AccuWeather, Weather.com, etc.)
> - Adjusting the agreement threshold (currently strict ±1°F)
> - Adding NO trades (betting the temp falls outside the bucket)
> - Using ML models trained on historical forecast accuracy per source

## Setup

### Environment variables

```bash
SIMMER_API_KEY=your_key        # Required — from simmer.markets
NVIDIA_API_KEY=your_key        # Required — for FourcastNet
TELEGRAM_BOT_TOKEN=your_token  # Optional — for Telegram UI
TRADE_AMOUNT=10.0              # Optional — default $10
CONFIDENCE_THRESHOLD=100       # Optional — default max confidence only
SIMMER_BASE_URL=https://api.simmer.markets  # Optional
SIMMER_VENUE=sim               # Optional — default "sim"
```

### Dependencies

```bash
pip install httpx python-telegram-bot python-dotenv numpy
pip install netCDF4              # For FourcastNet output parsing
pip install playwright           # For Wunderground scraping
playwright install chromium      # Required for Wunderground
```

## Supported cities

New York, Los Angeles, Chicago, Miami, Houston, Phoenix, Philadelphia, San Francisco, Seattle, Denver, Boston, Atlanta, Dallas, Minneapolis, Las Vegas, Detroit, Portland, San Antonio, San Diego, Milan, Madrid, Tel Aviv, London, Paris, Berlin, Tokyo.

Add more in `city_map.py`.

## Remix guide

Swap in your own signals:

- **Different weather sources**: Replace or add forecast functions in the `simmer_weather_bot/` folder
- **Different scoring**: Modify `compute_confidence()` in `strategy.py`
- **Add NO trades**: Extend the strategy to also bet against consensus
- **ML-based**: Train a model on historical forecast accuracy and replace the simple agreement check

The plumbing (market discovery, trade execution, Telegram UI, health checks) stays the same.

## Hard rules

- Always defaults to dry-run. Pass `--live` for real trades.
- Always tags trades with source and skill_slug for tracking.
- Always includes reasoning with the weather data used.
- Reads API keys from env — never hardcodes credentials.
