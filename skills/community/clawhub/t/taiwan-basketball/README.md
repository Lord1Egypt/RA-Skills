# 台灣職籃 🏀

OpenClaw Agent Skill — 台灣職業籃球資訊查詢，支援 PLG（P. LEAGUE+）與 TPBL（台灣職業籃球大聯盟）。

## 版本

v1.3.6

## 完整文件

詳見 [SKILL.md](SKILL.md)。

## 功能總覽

| 功能 | 說明 |
|------|------|
| 賽程查詢 | PLG / TPBL 賽程、倒數計時、球隊篩選 |
| 比賽結果 | 最近比賽結果、球隊篩選 |
| 戰績排行 | PLG / TPBL 排名 |
| 球員數據 | 歷年數據、每季效力球隊、別名搜尋 |
| 排行榜 | 得分王、籃板王、助攻王等 |
| 球員比較 | 兩位球員對比 |
| 即時比分 | 進行中的比賽分數 |
| Box Score ✨ | 單場詳細球員數據（TPBL 用 Scrapling StealthyFetcher 爬取） |
| 比賽提醒 | 訂閱球隊、自動通知 |
| 球員異動 | 交易、簽約、轉隊 |
| 賽制過濾 ✨ | 例行賽、季後賽、季後挑戰賽、總冠軍賽、熱身賽 |
| 維基館查詢 ✨ | 台灣籃球維基館歷史資料（跨聯盟經歷、獎項、T1 數據） |

## 快速開始

所有腳本使用 `uv run` 執行：

```bash
# 雙聯盟賽程（並行查詢）
uv run scripts/basketball_schedule.py --league all

# 戰績排行
uv run scripts/basketball_standings.py --league plg
uv run scripts/basketball_standings.py --league tpbl

# 最近比賽結果
uv run scripts/basketball_games.py --league all --last 5

# 球員數據（支援別名：高柏鎧↔吉爾貎克）
uv run scripts/basketball_player.py --league all --player 高柏鎧
uv run scripts/basketball_player.py --league plg --player 飛米

# 季後賽賽程
uv run scripts/basketball_schedule.py --league all --stage playoffs

# 即時比分
uv run scripts/basketball_live.py --league all

# Box Score
uv run scripts/basketball_boxscore.py --league tpbl --game-id 123

# 比賽提醒
uv run scripts/basketball_notify.py add --team 戰神 --league tpbl
uv run scripts/basketball_notify.py check --hours 24

# 球員異動
uv run scripts/basketball_transactions.py --league all
```

## 更新紀錄

### v1.3.6 (2026-06-12)

**Bug Fix**

- 🐛 PLG 總冠軍賽 G4 即時比分誤判為「completed」— 已修復
  - 根因：`_parse_schedule_page()` 看到 PLG 官網賽程頁的即時分數 > 0 就當作比賽結束
  - 修法：比分 > 0 時再檢查比賽時間是否落在 live window（3 小時）內，是的話標 `live` 而非 `completed`
  - 效果：`basketball_live.py` 現在能正確顯示 PLG 進行中比賽，`basketball_games.py` 不再誤報

### v1.3.3 (2026-05-11)

**重構**

- 🔄 Camoufox 全面替換為 Scrapling StealthyFetcher
  - `_wiki_api.py` 維基館爬蟲改用 `StealthyFetcher.fetch()` 一行搞定
  - `_tpbl_boxscore_scraper.py` Box Score 爬蟲同步改用 StealthyFetcher
  - `_tpbl_api.py` 註解與錯誤訊息同步更新
  - 文字提取改用 `page.css()[0].get_all_text()` 取代 Playwright API
  - 移除所有 camoufox 直接依賴，改用 scrapling（共用 CPBL skill venv）

### v1.3.2 (2026-05-10)

**新功能**

- 🐛 TPBL Box Score 改用 Scrapling StealthyFetcher 爬蟲！不再依賴不開放的 API 端點
  - `_tpbl_boxscore_scraper.py` 模組，用 StealthyFetcher 渲染 JS 頁面並爬取完整球員數據
  - `basketball_boxscore.py --league tpbl --game-id 6316` 現在可以正常顯示整場 Box Score
  - 自動 fallback：API 撈不到時自動切 StealthyFetcher 爬蟲

### v1.3.1 (2026-05-10)

**修復**

- 🐛 `basketball_games.py` 新增 `--date` 參數，支援指定日期查詢比賽結果
- 🐛 `basketball_games.py` 現在也會包含正在進行中的比賽（之前只回傳 COMPLETED 的比賽）
- 🐛 `basketball_live.py` 預設 `--no-cache`，即時比分不再使用快取資料

### v1.3.0 (2026-05-11)

**新功能**

- 🏀 **賽制過濾**：`--stage` 參數支援 `regular`/`playoffs`/`play-in`/`finals`/`preseason`
  - TPBL：`division_id` 判斷（8=熱身賽、9=例行賽、11=季後挑戰賽、12=季後賽）
  - PLG：從不同 URL 抓取各賽制頁面
  - 中文化顯示：例行賽、季後賽、季後挑戰賽、總冠軍賽、熱身賽

- 🏀 **球員每季效力球隊**：PLG 球員不再永遠顯示現役球隊
  - 三層判斷：Preciser API → 經歷區塊 → 頁面基本資料
  - 球隊名正規化：移除「籃球隊」後綴和英文名

- 🏀 **球員別名搜尋**：歸化改名、跨聯盟譯名雙向解析
  - 別名對照表：高柏鎧↔吉爾貝克、飛米↔Flymy/Ironmy 等
  - PLG 和 TPBL 雙向別名解析

- 🏀 **台灣籃球維基館整合**：Scrapling StealthyFetcher 繞過 Anubis 防護
  - 球員跨聯盟經歷（PLG/T1/TPBL/NBA/CBA 完整球隊歷史）
  - T1 聯盟歷史數據（已消失聯盟）
  - 球員獎項紀錄、歸化資訊、球隊更名歷史

**修復**

- PLG 球員頁面「球隊」欄位永遠顯示現役球隊 → 現在正確顯示每季效力球隊
- 經歷區塊支援年份格式（`2023` 只有年份沒有範圍，如林書豪的 `2023 PLG 高雄鋼鐵人`）
- 經歷推算只使用同聯盟條目（避免 CBA/NBA 經歷干擾 PLG 球隊判斷）
- 球員名字從頁面標題正確提取（移除「- 球隊名籃球隊」後綴）
- TPBL 每季數據補上 `team` 欄位

## 資料來源

| 來源 | 說明 |
|------|------|
| PLG 官網 | HTML 爬蟲 |
| TPBL 官方 API | REST API |
| 台灣籃球維基館 | Scrapling StealthyFetcher 繞過 Anubis |
| 本地 SQLite | `~/.local/share/taiwan-basketball/basketball.db` |

## 授權

MIT