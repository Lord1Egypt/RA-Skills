# Weather Stable

Author: **advanceware-CEO**
License: **MIT**

A lightweight, automation-first weather skill for OpenClaw.

## Why this exists

Weather should be one of the easiest public data types to retrieve.
But in many agent workflows, it still breaks for avoidable reasons:

- HTML scraping is fragile
- some "weather skills" are only instructions, not stable tools
- output formats vary too much for bots and automations
- user-facing results often depend on model interpretation

**Weather Stable** was built to solve that.

It focuses on one outcome:

> return today's weather reliably, with predictable output, in a format that bots and agents can use directly.

---

## What makes it different

### 1. It is not just a note about public services
A lot of weather skills only tell the agent to call a site or API.
This project provides an actual runnable tool.

### 2. It does not depend on HTML scraping
No page-title guessing. No brittle CSS/regex parsing of weather websites.
It uses structured weather data.

### 3. It is built for automation first
Three output modes are supported:

- `plain` → for Feishu, chatbots, logs
- `pretty` → for local terminal viewing
- `json` → for programmatic workflows

### 4. It handles Chinese city names well
Chinese city names can be used directly, and common cities are optimized with preset coordinates.

### 5. It is designed as a system capability
The goal is not to answer weather questions once.
The goal is to make weather querying dependable inside agent workflows.

---

## Features

- same-day weather lookup
- Chinese and English city input
- current temperature
- daily min/max temperature
- wind speed
- stable output shape
- JSON mode for workflows

---

## Usage

```bash
# default plain text
./weather-stable.sh 北京
./weather-stable.sh Beijing

# pretty terminal mode
./weather-stable.sh --pretty 北京

# JSON mode
./weather-stable.sh --json 北京
```

---

## Example output

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

---

## Installation

Place this skill inside your OpenClaw skills directory, for example:

```bash
skills/weather-stable/
```

Required runtime:

- `python3`
- outbound access to Open-Meteo API

No API key required.

---

## Design choices

### Source strategy

- common Chinese cities → preset coordinates
- other cities → Open-Meteo geocoding
- weather data → Open-Meteo forecast endpoint

### Why this strategy

Because it is significantly more stable than scraping web pages, and easier to reuse in automation.

---

## Scope

Current scope is:

- today's weather
- single-city query
- stable automation-friendly output

Not yet included:

- multi-day forecast formatting
- AQI / pollen / alerts
- clothing or lifestyle recommendations

Those can be added later without changing the basic contract of the tool.

---

## License

MIT
