---
name: tpvl
description: "TPVL (Taiwan Professional Volleyball League) stats, scores, schedules, and standings for Taiwan's pro volleyball."
tags: ["tpvl", "volleyball", "taiwan", "sports", "scores"]
metadata:
  openclaw:
    clawhub:
      link: https://clawhub.ai/ichendong/tpvl
---

# TPVL Skill - 台灣職業排球聯盟資訊查詢 🏐

Query TPVL game results, schedules, and standings for the Taiwan Professional Volleyball League.

## Data Sources

| Source | Description |
|--------|-------------|
| TPVL official website | Game results, schedule, standings via `__NEXT_DATA__` SSR JSON |

**Note:** TPVL's `/api/*` endpoints require authentication (401). All data is extracted from server-side rendered `__NEXT_DATA__` JSON embedded in page HTML.

- Homepage (`/`): Recent 5 completed + 5 upcoming matches + rankings
- Schedule page (`/schedule/schedule`): All completed match data (82+ games)
- Record page (`/record`): Full team standings with detailed stats

## Teams (2025-26 Season)

| Team | English |
|------|---------|
| 臺中連莊 | Taichung Winstreak |
| 台鋼天鷹 | TSG SkyHawks |
| 臺北伊斯特 | Taipei East Power |
| 桃園雲豹飛將 | Taoyuan Leopards |

## Features

| Feature | Script | Source | Status |
|---------|--------|--------|--------|
| Game results | `tpvl_games.py` | TPVL `/schedule/schedule` page | ✅ |
| Schedule | `tpvl_schedule.py` | TPVL homepage + schedule page | ✅ |
| Standings | `tpvl_standings.py` | TPVL `/record` page | ✅ |
| Player stats | `tpvl_stats.py` | Auto-detects TPVL pages | 🔄 Auto-detect |

## Game Type Codes

目前 TPVL 官網僅有單一賽事類型（例行賽），資料結構中只有一組 `seasonId`/`divisionId`/`poolId`：
- **seasonId**: 171
- **divisionId**: 272
- **poolId**: 443
- **round**: 3 ~ 5（巡迴賽輪次）

沒有明確的例行賽/季後賽/總冠軍賽區分。官網也沒有對應的篩選 UI。若未來球季加入季後賽，將新增 `--kind` 參數支援。

## Player Stats

`tpvl_stats.py` 會自動偵測 TPVL 官網球員數據頁面是否可用（路由 `/results/player-introduction`、`/results/competition-data`）。若頁面已開放，將自動取得實際數據；若仍為 404 則回傳空資料。

## Quick Start

All scripts use `uv run` for dependency management.

### Game Results

```bash
uv run scripts/tpvl_games.py --limit 10
uv run scripts/tpvl_games.py --date 2026-03-22
uv run scripts/tpvl_games.py --team 台鋼 --limit 5
uv run scripts/tpvl_games.py --year 2025
```

### Schedule

```bash
uv run scripts/tpvl_schedule.py
uv run scripts/tpvl_schedule.py --date 2026-03-28
uv run scripts/tpvl_schedule.py --team 連莊
uv run scripts/tpvl_schedule.py --all --limit 20
```

### Standings

```bash
uv run scripts/tpvl_standings.py
uv run scripts/tpvl_standings.py --output text
```

### Player Stats (⚠️ Coming Soon)

```bash
uv run scripts/tpvl_stats.py --category 得分 --top 20 --output text
uv run scripts/tpvl_stats.py --team 台鋼 --category 攔網
```

## Dependencies

Auto-installed via `uv`:
- `requests` — HTTP requests
- `beautifulsoup4` — HTML parsing (reserved for future scraping needs)
- `lxml` — Fast parser

## Notes

- Data source: TPVL official website (tpvl.tw)
- Data cached for 30 minutes in `/tmp/tpvl_cache/`
- Team name filtering supports aliases (e.g., `台鋼`, `連莊`, `伊斯特`, `桃園`)
- For learning and personal use only. Please follow TPVL terms of service.
