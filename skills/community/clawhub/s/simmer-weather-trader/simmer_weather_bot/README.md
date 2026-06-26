# Simmer Weather Trading Bot

A production-grade Python Telegram bot that discovers weather prediction markets on Simmer Markets, fetches real temperature forecasts from three independent live APIs, uses DeepSeek AI to reason over the data, and executes trades exclusively through the Simmer SDK.

## Features

- **Startup health checks** — verifies all 6 APIs before the bot activates
- **Real forecasts** from NOAA, Open-Meteo, and Wunderground (Playwright)
- **DeepSeek-V3.1 AI reasoning** via NVIDIA NIM
- **Confidence scoring** — trades only when score == 100%
- **Simmer SDK trading** — all trades via `venue="sim"` (virtual $SIM)
- **Zero mock data** — every number comes from a live API

## File Structure

```
simmer_weather_bot/
├── main.py             # Entry point — health checks first, then bot
├── health_check.py     # Startup API health checker for all 6 services
├── telegram_ui.py      # Inline keyboard + formatted message output
├── simmer_client.py    # Simmer API wrapper (markets, context, trade, positions)
├── noaa.py             # NOAA National Weather Service live forecast
├── openmeteo.py        # Open-Meteo live forecast
├── wunderground.py     # Wunderground live forecast (Playwright headless)
├── ai_analyzer.py      # DeepSeek AI reasoning via NVIDIA NIM
├── strategy.py         # Confidence scoring (0–100, trade only at 100)
├── city_map.py         # City name → lat/lon + Wunderground slug resolver
├── config.py           # All env vars loaded from environment/dotenv
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 2. Configure secrets

Copy `.env.example` to `.env` and fill in:

```
TELEGRAM_BOT_TOKEN=   # from @BotFather on Telegram
SIMMER_API_KEY=       # your Simmer Markets sk_live_... key
NVIDIA_API_KEY=       # your NVIDIA NIM nvapi-... key
```

All other values have defaults and are pre-configured.

### 3. Run the bot

```bash
python main.py
```

### Startup output (if all APIs pass)

```
============================================================
🔍 SIMMER WEATHER BOT — STARTUP HEALTH CHECK
============================================================
  ✅ Simmer API Auth           PASS | Agent: abc123 | Balance: ...
  ✅ Simmer Markets            PASS | 8 markets found
  ✅ NOAA Weather API          PASS | Grid: OKX
  ✅ Open-Meteo API            PASS | Sample: 42°F
  ✅ NVIDIA AI API             PASS | Response: READY
  ✅ Wunderground Scraper      PASS | Sample: 43°F
============================================================
🟢 ALL SYSTEMS GO — Bot is starting...
============================================================
🚀 Starting Telegram bot...
```

If any check fails, the bot exits immediately and reports exactly which API failed and why.

## Telegram Commands

- `/start` — Fetches live markets, shows 4 prediction buttons
- `/status` — Shows agent balance and open positions
- **Predict & Bet buttons** — Runs full pipeline: 3 forecasts → AI → trade/skip

## Trade Logic

A trade only executes when **ALL** of these are true simultaneously:

1. All three forecasts (NOAA, Open-Meteo, Wunderground) within ±1°F of each other
2. Consensus temperature falls inside the market's temperature bucket
3. Simmer edge recommendation is "TRADE"
4. DeepSeek AI verdict is "TRADE" with all conditions confirmed
5. Confidence score == 100%

## City Map

Add new cities to `city_map.py` as new markets appear. Each entry needs:
- `lat`, `lon` — coordinates for NOAA and Open-Meteo
- `wunderground` — URL path segment (e.g. `"ny/new-york"`)
- `timezone` — IANA timezone string

## Logs

All activity is logged to `bot.log` with timestamps and to stdout.
