# TPVL Skill - 台灣職業排球聯盟資訊查詢 🏐

OpenClaw skill for querying Taiwan Professional Volleyball League (TPVL) game results, schedules, standings, and player leaderboards.

## Features

- 🏐 Game results with set scores and winner
- 📅 Schedule query (upcoming / postponed / past)
- 🏆 Standings (W-L, win rate, points, sets)
- 📊 Player leaderboards (points / attack / block / serve / reception / dig / setting)

## Data Source

TPVL official website ([tpvl.tw](https://tpvl.tw/)). No API key required.

**2026 update:** the site moved to Next.js App Router. `__NEXT_DATA__` is gone; data now lives in the
RSC flight payload (`self.__next_f.push`). Scripts extract and parse that payload, including
resolving `"$L<id>"` lazy references.

| Page | Purpose |
|------|---------|
| `/matches` | results + schedule |
| `/standings` | standings |
| `/stats/players` | player leaderboards |

## Quick Start

```bash
# Game results
uv run scripts/tpvl_games.py --limit 10
uv run scripts/tpvl_games.py --team 台鋼 --output text

# Schedule
uv run scripts/tpvl_schedule.py --output text
uv run scripts/tpvl_schedule.py --team 新竹 --output text

# Standings
uv run scripts/tpvl_standings.py --output text

# Player stats
uv run scripts/tpvl_stats.py --output text --top 10
uv run scripts/tpvl_stats.py --category 攔網 --output text
```

## Installation

```bash
clawhub install tpvl
```

## Teams (2026-27, 5 teams)

| Team | Chinese | Slug |
|------|---------|------|
| Taichung Winstreak | 臺中連莊 | taichung-winstreak |
| TSG SkyHawks | 台鋼天鷹 | tsg-skyhawks |
| Taipei East Power | 臺北伊斯特 | taipei-east-power |
| Taoyuan Leopards | 桃園雲豹飛將 | taoyuan-leopards |
| Hsinchu Collie | 新竹可利工程師 | hsinchu-collie-engineers |

## License

For learning and personal use only. Data sourced from TPVL official website.
