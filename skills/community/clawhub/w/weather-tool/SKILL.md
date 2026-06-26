---
name: weather-tool
description: Get current weather and forecasts. Use when user needs to check current weather, get forecast for travel planning, or monitor weather conditions.
---

# Weather Tool

Get current weather and forecasts.

## Quick Start

```bash
# Current weather
python scripts/weather.py Beijing

# Forecast
python scripts/weather.py Beijing --forecast 3
```

## Usage

```bash
python scripts/weather.py [LOCATION] [OPTIONS]

Options:
  --forecast DAYS   Forecast days (1-7)
  --json            Output as JSON
  --celsius         Use Celsius (default)
  --fahrenheit      Use Fahrenheit
```

## Examples

```bash
# Current weather
python scripts/weather.py Beijing

# 3-day forecast
python scripts/weather.py Shanghai --forecast 3

# JSON output
python scripts/weather.py "New York" --json
```

## Features

- Current weather conditions
- Multi-day forecasts
- Temperature in C/F
- JSON output
- Multiple location support
