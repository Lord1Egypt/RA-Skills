---
name: weather-stable
description: Stable weather skill for OpenClaw. Designed for reliable same-day weather queries with predictable output, Chinese city support, and automation-friendly plain/json modes.
homepage: https://open-meteo.com/
author: advanceware-CEO
license: MIT
metadata: { "openclaw": { "emoji": "🌤️", "requires": { "bins": ["python3"] } } }
---

# Weather Stable

A lightweight, automation-first weather skill for OpenClaw.

It is built for one job: **return today's weather reliably, in a format agents and bots can actually use**.

## Why this is different

Many weather skills fall into one of these traps:

1. They are only usage notes for public services, not a stable tool
2. They scrape HTML pages and break when page structure changes
3. They return inconsistent text that is hard for bots to reuse
4. They are okay for humans reading a terminal, but weak for automation

**Weather Stable is different because it is designed around reliability, not novelty.**

### Core differences

- **Structured data first**  
  No HTML scraping, no title parsing hacks.

- **Predictable output**  
  Same city in → same output shape out.

- **Chinese-city friendly**  
  Chinese city names can be used directly.

- **Automation-first modes**  
  Plain text for messaging, JSON for workflows, pretty mode for terminals.

- **Built for agent use**  
  Better fit for Feishu bots, reporting flows, and automation scripts.

## What it returns

- weather condition
- current temperature
- today's min/max temperature
- wind speed
- source

## Usage

```bash
# plain text (default)
./weather-stable.sh Beijing
./weather-stable.sh 北京

# pretty terminal output
./weather-stable.sh --pretty 北京

# JSON output
./weather-stable.sh --json 北京
```

## Output example

### plain

```text
北京天气
日期: 2026-04-10
来源: open-meteo
天气: ☀️ 晴
当前温度: 16.2°C
温度范围: 8.0/26.9°C
风速: 3.6 km/h
```

### json

```json
{
  "city": "北京",
  "date": "2026-04-10",
  "source": "open-meteo",
  "weather": "晴",
  "icon": "☀️",
  "current_temperature": 16.2,
  "temperature_range": {
    "min": 8.0,
    "max": 26.9
  },
  "wind_kmh": 3.6
}
```

## Design goal

This project exists because weather is one of the easiest public data categories — and yet in many agent workflows it still fails too often.

The goal here is simple:

> turn weather from a fragile prompt-side trick into a dependable system capability.

## Best use cases

- "What's the weather in Beijing today?"
- daily summaries and digests
- chatbots and assistants
- structured automation workflows
- same-day city weather checks

## Notes

- Current focus is **same-day weather**, not multi-day forecasting
- Common Chinese cities use built-in coordinates first
- Other cities fall back to Open-Meteo geocoding

## Author

**advanceware-CEO**
