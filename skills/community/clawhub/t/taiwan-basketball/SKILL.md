---
name: taiwan-basketball
description: "Taiwan professional basketball stats, scores, schedules, player data, live scores, box scores, notifications, and transactions for PLG and TPBL."
tags: ["plg", "tpbl", "basketball", "taiwan", "sports", "scores", "standings"]
version: 1.3.6
metadata:
  openclaw:
    emoji: 🏀
    requires:
      bins:
        - uv
      anyBins:
        - python3
---

# Taiwan Basketball Skill - 台灣職籃資訊查詢 🏀

Query PLG (P. LEAGUE+) and TPBL (台灣職業籃球大聯盟) game results, schedules, standings, player stats, league leaders, live scores, box scores, notifications, and transactions.

## Data Sources

| Source | Description |
|--------|-------------|
| PLG official website | HTML scraping (server-side rendered) |
| TPBL official REST API | `api.tpbl.basketball` |
| 台灣籃球維基館 | Scrapling StealthyFetcher (bypasses Anubis protection) |
| Local SQLite DB | `~/.local/share/taiwan-basketball/basketball.db` |

## Features

| Feature | Script | Source |
|---------|--------|--------|
| Schedule (with countdown) | `basketball_schedule.py` | PLG website / TPBL API |
| Standings | `basketball_standings.py` | PLG website / TPBL API |
| Game results | `basketball_games.py` | PLG website / TPBL API |
| Player stats | `basketball_player.py` | PLG website / TPBL API |
| League leaders | `basketball_leaders.py` | PLG website / TPBL API |
| Player comparison | `basketball_compare.py` | PLG website / TPBL API |
| **Live scores** ✨ | `basketball_live.py` | TPBL API / PLG time-based |
| **Box Score** ✨ | `basketball_boxscore.py` | TPBL API / PLG website |
| **Notifications** ✨ | `basketball_notify.py` | PLG website / TPBL API |
| **Transactions** ✨ | `basketball_transactions.py` | PLG news / TPBL API |
| **Wiki (awards/history)** ✨ | `_wiki_api.py` | 台灣籃球維基館 (Scrapling StealthyFetcher) |

## Architecture

```
scripts/
  _cache.py            # 磁碟 TTL 快取模組
  _http.py             # HTTP 工具（重試 / 快取）
  _utils.py            # 共用工具（格式化、球隊別名、球員別名、並行擷取）
  _tpbl_api.py         # TPBL REST API 封裝
  _plg_api.py          # PLG HTML 爬蟲封裝
  _wiki_api.py         # 台灣籃球維基館（Scrapling StealthyFetcher 繞過 Anubis）
  _basketball_api.py   # 兼容性匯入層（維持所有腳本相容）
  _db.py               # SQLite 資料持久化模組
  basketball_*.py      # CLI 腳本
```

**並行擷取**：所有 `--league all` 查詢均使用 `ThreadPoolExecutor` 並行發送 PLG/TPBL 請求，大幅縮短等待時間。

## Quick Start

All scripts use `uv run` for dependency management.

### Schedule

```bash
uv run scripts/basketball_schedule.py --league plg
uv run scripts/basketball_schedule.py --league tpbl
uv run scripts/basketball_schedule.py --league all       # PLG + TPBL 合併查詢
uv run scripts/basketball_schedule.py -l plg --team 勇士
uv run scripts/basketball_schedule.py -l all --next      # 只顯示下一場比賽及倒數
uv run scripts/basketball_schedule.py -l all --format table
uv run scripts/basketball_schedule.py -l all --stage playoffs    # 只顯示季後賽賽程
uv run scripts/basketball_schedule.py -l tpbl --stage play-in   # 只顯示季後挑戰賽賽程
```

### Standings

```bash
uv run scripts/basketball_standings.py --league plg
uv run scripts/basketball_standings.py --league tpbl
uv run scripts/basketball_standings.py --league plg --format table
```

### Game Results

```bash
uv run scripts/basketball_games.py --league plg
uv run scripts/basketball_games.py --league tpbl
uv run scripts/basketball_games.py --league all            # PLG + TPBL 合併查詢
uv run scripts/basketball_games.py --league all --last 5   # 最近 5 場結果
uv run scripts/basketball_games.py -l tpbl --team 戰神
uv run scripts/basketball_games.py -l all --last 10 --format table
uv run scripts/basketball_games.py -l tpbl --stage play-in  # 只顯示季後挑戰賽結果
uv run scripts/basketball_games.py -l all --stage playoffs  # 只顯示季後賽結果
```

### Player Stats

```bash
uv run scripts/basketball_player.py --league plg --player 林書豪
uv run scripts/basketball_player.py --league tpbl --player 林書豪
uv run scripts/basketball_player.py --league all --player 林書豪
uv run scripts/basketball_player.py -l plg -p 林書豪 --season 2023-24
uv run scripts/basketball_player.py -l tpbl -p 夢想家           # 球隊搜尋
```

Player names support aliases (e.g. `高柏鎧` finds `吉爾貝克` in PLG, `吉爾貝克` finds `高柏鎧` in TPBL).

### League Leaders（排行榜）

```bash
uv run scripts/basketball_leaders.py --league plg --stat pts          # PLG 得分王
uv run scripts/basketball_leaders.py --league tpbl --stat reb --top 5 # TPBL 籃板前5名
uv run scripts/basketball_leaders.py -l tpbl -s ast --format table    # 表格輸出
uv run scripts/basketball_leaders.py -l all -s pts --top 10           # 雙聯盟得分榜
```

Supported `--stat` values: `pts`（得分）、`reb`（籃板）、`ast`（助攻）、`stl`（抄截）、`blk`（阻攻）、`tov`（失誤）、`pf`（犯規）、`eff`（效率值，TPBL 限定）

### Player Comparison（球員比較）

```bash
uv run scripts/basketball_compare.py --league plg --player1 林書豪 --player2 戴維斯
uv run scripts/basketball_compare.py -l tpbl -p1 林志傑 -p2 陳盈駿
uv run scripts/basketball_compare.py -l plg -p1 林書豪 -p2 戴維斯 --season 2023-24
uv run scripts/basketball_compare.py -l plg -p1 林書豪 -p2 戴維斯 --format table
```

Supports fuzzy search by player name or team name. Returns per-season stats (GP, avg minutes/pts/reb/ast/stl/blk, FG/3P/FT splits, efficiency, PIR) plus career totals.

- **PLG**: Scrapes `/stat-player` + `/all-players` for player index, then `/player/{ID}` for detailed per-season stats.
- **TPBL**: Queries `/games/stats/players?division_id={id}` for all divisions across all seasons. Recalculates FG%/3P%/FT% from accumulated makes/attempts for cross-division accuracy.

### Live Scores（即時比分）✨

```bash
uv run scripts/basketball_live.py --league all
uv run scripts/basketball_live.py --league tpbl --format table
uv run scripts/basketball_live.py --league plg
```

- **TPBL**: Returns games with `status=IN_PROGRESS` from official API.
- **PLG**: Estimates live games based on scheduled time ±3 hours (no real-time API). Recommend visiting `pleagueofficial.com` for exact scores.

### Box Score（單場詳情）✨

```bash
# 先取得 game_id
uv run scripts/basketball_games.py --league tpbl --last 5 --format table

# 查詢 box score（TPBL 用數字 ID，PLG 用如 G101 格式）
uv run scripts/basketball_boxscore.py --league tpbl --game-id 123
uv run scripts/basketball_boxscore.py --league plg --game-id G101
uv run scripts/basketball_boxscore.py --league tpbl --game-id 123 --format table
```

Returns game summary (score, venue, date) and per-player stats (pts/reb/ast/stl/blk/tov/pf/min/FG splits+/-).

### Notifications（比賽提醒）✨

```bash
# 訂閱管理
uv run scripts/basketball_notify.py add --team 戰神 --league tpbl
uv run scripts/basketball_notify.py add --team 勇士 --league plg
uv run scripts/basketball_notify.py list
uv run scripts/basketball_notify.py remove --team 戰神 --league tpbl

# 檢查提醒（訂閱的球隊，未來 24 小時）
uv run scripts/basketball_notify.py check
uv run scripts/basketball_notify.py check --hours 48 --format table

# 臨時查詢（不需要先訂閱）
uv run scripts/basketball_notify.py check --team 戰神 --league tpbl --hours 72
```

Subscriptions are stored in the local SQLite database. Can be used with cron for automated alerts.

### Transactions（球員異動 / 交易）✨

```bash
uv run scripts/basketball_transactions.py --league tpbl
uv run scripts/basketball_transactions.py --league plg --format table
uv run scripts/basketball_transactions.py --league all

# 從本地 DB 讀取已儲存資料
uv run scripts/basketball_transactions.py --league all --from-db
```

- **TPBL**: Tries official API endpoints for transaction data.
- **PLG**: Parses news page for player movement reports (transfers, signings, etc.).
- Results are auto-saved to local SQLite DB for offline access.

## CLI Parameters

| Script | Param | Description |
|--------|-------|-------------|
| All | `--league`, `-l` | `plg`, `tpbl`, or `all` |
| All | `--format`, `-f` | `json` (預設) or `table` (ASCII 表格) |
| All | `--no-cache` | 停用磁碟快取 |
| All | `--debug` | 輸出 debug 訊息（或設 `BASKETBALL_DEBUG=1`）|
| schedule, games | `--team`, `-t` | Team name filter (supports aliases) |
| `basketball_schedule.py` | `--next` | 只顯示下一場比賽及倒數計時 |
| `basketball_games.py` | `--last`, `-n` | Show only last N results (default: all) |
| `basketball_player.py` | `--player`, `-p` | Player name to search |
| `basketball_player.py` | `--season`, `-s` | Filter by season (e.g., `2023-24`) |
| `basketball_leaders.py` | `--stat`, `-s` | Stat category (pts/reb/ast/stl/blk/tov/pf/eff) |
| `basketball_leaders.py` | `--top`, `-n` | Show top N players (default: 10) |
| `basketball_compare.py` | `--player1`, `-p1` | First player name |
| `basketball_compare.py` | `--player2`, `-p2` | Second player name |
| `basketball_compare.py` | `--season`, `-s` | Compare a specific season (default: career) |
| `basketball_boxscore.py` | `--game-id`, `-g` | 比賽 ID（TPBL 數字，PLG 如 G101） |
| schedule, games | `--stage`, `-s` | 賽制過濾：`regular`, `playoffs`, `play-in`, `finals`, `preseason` |
| `basketball_notify.py check` | `--team`, `-t` | 指定球隊（不指定則用訂閱清單） |
| `basketball_transactions.py` | `--from-db` | 從本地 DB 讀取（不發送 API 請求） |
| `basketball_notify.py check` | `--hours` | 查詢未來幾小時內的比賽（預設 24） |
| `basketball_transactions.py` | `--limit`, `-n` | 最多顯示筆數（預設 30） |

Output JSON includes a `league` field per game when using `--league all`.
Output JSON includes a `stage` field per game indicating the competition stage:

| Stage | 說明 |
|-------|------|
| `regular` | 例行賽 |
| `play-in` | 季後挑戰賽（TPBL）|
| `playoffs` | 季後賽（四強）|
| `finals` | 總冠軍賽 |
| `preseason` | 熱身賽 |

## Per-Season Team Attribution

PLG player pages always show the **current** team, not the team the player played for in each season. We use a three-layer mechanism to correctly determine per-season teams:

1. **Preciser API** (primary) — Scrapes per-game "效力球隊" column from the player page's AJAX data
2. **Experience section** (fallback) — Parses the "經歷" block (e.g. `2022-24 PLG 高雄17直播鋼鐵人`) and maps periods to seasons
3. **Page basic info** (last resort) — Always shows current team, least accurate

**Example**: 飛米 (Ironmy) played for 高雄17直播鋼鐵人 in 22-23/23-24, but the PLG player page always shows 臺北富邦勇士. The three-layer mechanism correctly resolves this.

**Team name normalization**: All team names are normalized to remove "籃球隊" suffixes and English names (e.g. `臺北富邦勇士Taipei Fubon Braves` → `臺北富邦勇士`).

## Player Aliases

Cross-league name resolution for naturalized/foreign players:

| Alias | League | Resolved To |
|-------|--------|-------------|
| 高柏鎧 | PLG | 吉爾貝克 |
| 吉爾貝克 | TPBL | 高柏鎧 |
| Gilbeck | PLG/TPBL | Respective official name |
| 飛米 | PLG | 飛米 |
| 魔獸 | PLG | 魔獸 (Dwight Howard) |
| 霍華德 | PLG | 魔獸 |

## 台灣籃球維基館 (Wiki)

台灣籃球維基館 (`wikibasketball.dils.tku.edu.tw`) uses Anubis protection that blocks `web_fetch` and Playwright.
**Use Scrapling StealthyFetcher (shared with CPBL skill's venv) to access it.**

### When to query the wiki

- ✅ Player **cross-league experience** (PLG → T1 → TPBL full team history)
- ✅ **T1 league** historical data (defunct league, not in official APIs)
- ✅ Player **awards** (MVP, Defensive Player of the Year, All-League teams, etc.)
- ✅ **Naturalization** info, career team changes
- ❌ Foreign/naturalized players may not have wiki pages (focus on domestic players)

### Setup (首次使用前)

維基館爬蟲依賴 CPBL skill venv 裡的 Scrapling stealth browser，需先安裝：

```bash
# 1. 建立 CPBL venv（如果不存在）
cd skills/cpbl && uv venv && uv pip install -e .
# 2. 安裝 stealth browser（Scrapling StealthyFetcher 需要）
cd ../.. && skills/cpbl/.venv/bin/scrapling install --force
```

### How to query

Use the CPBL venv's Scrapling (`skills/cpbl/.venv`). Do NOT use `web_fetch` or Playwright for wiki pages.

```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch(
    'https://wikibasketball.dils.tku.edu.tw/wiki/index.php?title=林書豪',
    headless=True,
    wait=10000,
)
text = page.css('#mw-content-text')[0].get_all_text()
```

### Limitations

- StealthyFetcher startup is slow (10-15 seconds), not suitable for frequent queries
- Player page names may differ from common names (e.g. 飛米 has no wiki page)
- Experience parsing is still being improved (wiki link syntax handling)

## Caching

Results are cached on disk at `~/.cache/taiwan-basketball/` with the following TTLs:

| Data type | TTL |
|-----------|-----|
| Schedule | 5 minutes |
| Game results | 10 minutes |
| Standings | 10 minutes |
| Player stats | 1 hour |
| League leaders | 10 minutes |
| Live scores | 1 minute |
| Box Score | 5 minutes |
| Transactions | 1 hour |

Use `--no-cache` to bypass cache, or set `BASKETBALL_DEBUG=1` to see cache hits/misses.

## League Codes

| Code | League |
|------|--------|
| `plg` | P. LEAGUE+ (4 teams) |
| `tpbl` | 台灣職業籃球大聯盟 (7 teams) |

## Team Aliases

### PLG
| Alias | Full Name |
|-------|-----------|
| 富邦, 勇士 | 臺北富邦勇士 |
| 璞園, 領航猿 | 桃園璞園領航猿 |
| 台鋼, 獵鷹 | 台鋼獵鷹 |
| 洋基, 洋基工程 | 洋基工程 |
| 國王 | 新北國王 (已轉至 TPBL) |
| 攻城獅 | 新竹街口攻城獅 (已轉至 TPBL) |
| 夢想家 | 福爾摩沙台新夢想家 (已轉至 TPBL) |
| 鋼鐵人 | 高雄鋼鐵人 (已解散) |

### TPBL
| Alias | Full Name |
|-------|-----------|
| 台新, 戰神 | 臺北台新戰神 |
| 中信, 特攻 | 新北中信特攻 |
| 國王 | 新北國王 |
| 雲豹 | 桃園台啤永豐雲豹 |
| 夢想家 | 福爾摩沙夢想家 |
| 攻城獅 | 新竹御嵿攻城獅 |
| 海神 | 高雄全家海神 |

## Dependencies

Auto-installed via `uv`:
- `beautifulsoup4` — HTML parsing
- `lxml` — Fast parser
- `sqlite3` — 內建 Python 模組，無需安裝

## Notes

- **PLG**: Server-side rendered HTML, no JS needed. Player pages use Preciser API for per-season team data. Experience section provides fallback team attribution.
- **TPBL**: Official REST API at `api.tpbl.basketball`. Player stats via `/games/stats/players?division_id={id}` across all seasons.
- **Team name normalization**: All PLG team names are normalized to remove "籃球隊" suffixes and English names for consistency.
- **Player aliases**: Supports naturalized name changes (高柏鎧↔吉爾貝克) and cross-league translation names.
- **Stage filter**: TPBL now has separate `playoffs` (semifinals, div=12) and `finals` (championship, div=35). PLG has both `playoffs` and `finals`.
- **Experience period formats**: PLG experience blocks support both `YYYY-YY` ranges and `YYYY` single-year formats (e.g. 林書豪's `2023 PLG 高雄17直播鋼鐵人`).
- **Experience league filter**: Only PLG experience entries are used when determining PLG per-season teams (CBA/NBA entries are ignored).
- **Retry**: All HTTP requests retry up to 3 times with exponential backoff on network errors.
- **FG% accuracy**: TPBL percentage stats (FG%/3P%/FT%) are recalculated from cumulative makes/attempts for cross-division accuracy.
- **Season format**: TPBL seasons display as `YY/YY` (e.g., `24/25`); PLG seasons as `YYYY-YY` (e.g., `2023-24`).
- **Live scores**: TPBL API natively supports `IN_PROGRESS` status. PLG uses time-window estimation (±3h from scheduled time).
- **Box Score**: TPBL tries multiple API endpoints; PLG scrapes individual game pages. If data is unavailable, a `note` field explains.
- **SQLite DB**: Data is stored at `~/.local/share/taiwan-basketball/basketball.db`. Schema is auto-created on first use.
- **Parallel fetch**: `--league all` queries run PLG and TPBL requests concurrently using `ThreadPoolExecutor`.
- SBL (超級籃球聯賽) is not supported — official site (sleague.tw) is a Vue SPA with authenticated GraphQL API.
- `avg_minutes` output is unified to `MM:SS` format for both leagues.