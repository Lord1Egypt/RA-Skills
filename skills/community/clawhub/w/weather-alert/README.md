# Weather Alert Skill

Proactive weather monitoring and alerting for any location. Uses free APIs (Open-Meteo, wttr.in) — no API key required.

## Features

- **Current weather** — temperature, humidity, wind, UV, pressure
- **7-day forecast** — daily conditions with precipitation, wind, temperature
- **Smart alerts** — threshold-based notifications (rain, temp, wind, UV, frost)
- **Event planner** — check weather suitability for activities
- **Weather trends** — track conditions over time

## Quick Start

```bash
npx clawhub install weather-alert
"Check weather in Prague"
"Alert me if it will rain tomorrow"
"7-day weather briefing"
```

## Install Locally

```bash
# Clone and install
git clone https://github.com/openclaw/skills.git
cd skills/weather-alert
pip install pyyaml  # optional, for config.yaml support

# Test
python3 -m unittest discover -s test -v

# Run
python scripts/weather_alert.py --location Berlin --days 5
```

## Configuration

Edit `config.yaml` to set your default location and alert thresholds.

## API Data Source

Open-Meteo (free, 1000 req/hour, no key): https://open-meteo.com/
