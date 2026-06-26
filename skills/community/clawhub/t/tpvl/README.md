# TPVL Skill - 台灣職業排球聯盟資訊查詢 🏐

OpenClaw skill for querying Taiwan Professional Volleyball League (TPVL) game results, schedules, standings, and player data.

## Features

- 🏐 Game results with scores and set counts
- 📅 Schedule query (upcoming and past)
- 🏆 Standings (wins, losses, win rate, set records)
- 📊 Player stats (placeholder - TPVL website not yet available)

## Data Source

TPVL official website ([tpvl.tw](https://tpvl.tw/)) via `__NEXT_DATA__` SSR JSON.
No API key required.

## Quick Start

```bash
# Game results
uv run scripts/tpvl_games.py --limit 10
uv run scripts/tpvl_games.py --team 台中 --output text

# Schedule
uv run scripts/tpvl_schedule.py --limit 5
uv run scripts/tpvl_schedule.py --team 桃園 --output text

# Standings
uv run scripts/tpvl_standings.py
uv run scripts/tpvl_standings.py --output text

# Player stats (placeholder)
uv run scripts/tpvl_stats.py --top 10
```

## Installation

```bash
clawhub install tpvl
```

## Teams

| Team | Chinese | Home City |
|------|---------|-----------|
| Taichung WinStreak | 臺中連莊 | 臺中市 |
| TSG SkyHawks | 台鋼天鷹 | 臺南市/高雄市 |
| Taipei East Power | 臺北伊斯特 | 臺北市 |
| Taoyuan Leopards | 桃園雲豹飛將 | 桃園市 |

## License

For learning and personal use only. Data sourced from TPVL official website.
