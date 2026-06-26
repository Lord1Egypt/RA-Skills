# 🌍 Travel Morning Weather Forecast

OpenClaw skill that adjusts your morning weather briefing based on travel plans captured from conversation.

## How It Works

```
Conversation → Travel plan detected → Update travel-plan.json
                                                    ↓
Morning Briefing Cron → Read today's location → Query weather → Report
```

## Features

- **Auto-capture** travel plans from chat — no manual input needed
- **Dynamic location** — morning briefing uses the city you're in today
- **Auto-expiry** — past dates cleaned automatically each morning
- **Home fallback** — uses default location when not traveling

## Install

```bash
clawhub install travel-morning-weather
```

## Quick Start

1. **Set your home location** (required — the skill won't work without it):
   ```json
   { "default_location": "<Your City>, <Country>", "daily_locations": {} }
   ```
   Save as `memory/travel-plan.json`. Replace with your actual home city.
2. Tell your agent about a trip: "May 10-12 in Paris"
3. Done — tomorrow's morning briefing will report Paris weather

## File Structure

```
travel-morning-weather/
├── SKILL.md                          # Core instructions (OpenClaw)
├── README.md                         # This file
├── references/
│   ├── data-format.md                # JSON schema + update commands
│   ├── capture-triggers.md           # When/how to capture travel plans
│   └── morning-briefing.md           # Cron integration guide
├── scripts/
│   ├── travel-cleaner.py             # Auto-expiry cleanup
│   └── update-travel-plan.py         # Travel data update
└── examples/
    └── travel-plan.json              # Sample data
```

## Author

Initiated by Neo Shi, executed by 银月 (Silvermoon)

## License

MIT
