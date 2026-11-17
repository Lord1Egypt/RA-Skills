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

Query TPVL game results, schedules, standings, and player leaderboards.

## Data Sources

| Source | URL | Description |
|--------|-----|-------------|
| 賽程 / 比分 | `https://tpvl.tw/matches` | 已完賽比分 + 未來賽程 |
| 戰績 | `https://tpvl.tw/standings` | 例行賽排名（官網已依規程排序） |
| 球員榜 | `https://tpvl.tw/stats/players` | 得分 / 攻擊 / 攔網 / 發球 / 接發 / 防守 / 舉球 |

**⚠️ 2026 官網改版（重要）：** 網站已從 Next.js Pages Router 改成 **App Router**，
`__NEXT_DATA__` 已消失，舊的 `/schedule/schedule`、`/record` 也改成 `/matches`、`/standings`。
資料現在藏在 **RSC flight payload**（`self.__next_f.push([...])`），
`_tpvl_api.py` 會自動抽出 payload、展開 `"$L<id>"` lazy 參照後解析。

## Teams (2026-27 Season, 5 隊)

| Team | English | Slug |
|------|---------|------|
| 臺中連莊 | Taichung Winstreak | `taichung-winstreak` |
| 台鋼天鷹 | TSG SkyHawks | `tsg-skyhawks` |
| 臺北伊斯特 | Taipei East Power | `taipei-east-power` |
| 桃園雲豹飛將 | Taoyuan Leopards | `taoyuan-leopards` |
| 新竹可利工程師 | Hsinchu Collie | `hsinchu-collie-engineers` |

2026-27 新增第 5 隊：**新竹可利工程師**（Hsinchu Collie）。

## Features

| Feature | Script | Source | Status |
|---------|--------|--------|--------|
| Game results | `tpvl_games.py` | `/matches` | ✅ |
| Schedule | `tpvl_schedule.py` | `/matches` | ✅ |
| Standings | `tpvl_standings.py` | `/standings` | ✅ |
| Player stats | `tpvl_stats.py` | `/stats/players` | ✅ |

## Quick Start

All scripts use `uv run`（依賴會自動安裝）。

### Game Results（已完賽）

```bash
uv run scripts/tpvl_games.py --limit 10
uv run scripts/tpvl_games.py --output text
uv run scripts/tpvl_games.py --date 2026-10-18
uv run scripts/tpvl_games.py --team 台鋼 --limit 5
uv run scripts/tpvl_games.py --season 2025-26 --limit 20
```

### Schedule（未開打）

```bash
uv run scripts/tpvl_schedule.py --output text
uv run scripts/tpvl_schedule.py --date 2026-11-01
uv run scripts/tpvl_schedule.py --team 新竹 --output text
uv run scripts/tpvl_schedule.py --all --limit 20   # 含已完賽/延賽
```

### Standings

```bash
uv run scripts/tpvl_standings.py --output text
uv run scripts/tpvl_standings.py --season 2025-26
```

### Player Stats

```bash
uv run scripts/tpvl_stats.py --output text --top 10
uv run scripts/tpvl_stats.py --category 攔網 --output text
uv run scripts/tpvl_stats.py --category 發球 --team 台鋼 --output text
uv run scripts/tpvl_stats.py --category 攻擊 --season 2026-27
```

可用類別：`得分`、`攻擊`、`攔網`、`發球`、`接發`、`防守`、`舉球`
（也接受英文 key：`points`、`attack_points`、`block_points`、`serve_points`、`reception`、`dig`、`setting`）

## Output Format

- 預設 `--output json`（給程式用）
- `--output text` 給人看的排版

## Team Filtering

支援中文別名：`台中`/`連莊`、`台鋼`/`天鷹`、`台北`/`伊斯特`、`桃園`/`雲豹`/`飛將`、`新竹`/`可利`/`工程師`，
以及英文（`skyhawks`、`collie`…）。

## Data Notes

- 快取 30 分鐘於 `/tmp/tpvl_cache/`
- 賽季參數：`--season 2026-27`（預設）或 `--season 2025-26`
- 狀態值：`COMPLETED`（已結束）、`SCHEDULED`（即將開打）、`POSTPONED`（延賽）
- 戰績排序依聯盟規程：勝場 → 積分 → 局數比 → 得失分率（官網已排好，脚本照抄順序）
- 官網 `/api/*` 需登入（401），所以一律從 SSR payload 取資料
- For learning and personal use only. Please follow TPVL terms of service.
