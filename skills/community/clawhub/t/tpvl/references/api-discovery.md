# TPVL API 調查報告

## 調查日期: 2026-03-23

## 官網資訊
- URL: https://tpvl.tw/
- 技術棧: Next.js (Pages Router) + i18n
- 託管: 可能在 Vercel 或自建
- 開發商: VNEMEX（從 meta author 欄位）

## API 調查結果

### 1. `/api/*` 端點
- `/api`, `/api/schedule`, `/api/match`, `/api/ranking` 均回傳 **401 Unauthorized**
- API 存在但需要認證 token（可能是 Bearer token）
- 目前無法取得公開 API 存取權

### 2. `__NEXT_DATA__` 伺服器端渲染資料（主要資料來源）
Next.js 將初始資料嵌入 HTML 的 `<script id="__NEXT_DATA__">` 標籤中，格式為 JSON。

#### 首頁 (`/`)
| Key | 說明 | 資料筆數 |
|-----|------|---------|
| `scheduleMatches` | 即將進行的比賽 | 5 場 |
| `completedMatches` | 最近完成的比賽 | 5 場 |
| `rankingsData` | 球隊戰績排名 | 4 隊 |
| `announcements` | 聯盟公告 | 5 則 |
| `liveMatches` | 正在進行的比賽 | 動態 |

#### 戰績頁 (`/record`)
| Key | 說明 |
|-----|------|
| `resRankingsData.teams_record[]` | 完整戰績：勝敗、勝率、局數、得分、得失分率等 |

#### 賽程頁 (`/schedule/schedule`)
| Key | 說明 |
|-----|------|
| `resultMatchData.data[]` | 所有已完成比賽（82 場） |
| `resultMatchData.total` | 總場次 |
| `liveMatches` | 即時比賽 |
| `squads` | 球隊基本資料 |

### 3. 比賽資料結構 (squadMatchResults)
每場比賽包含：
- `id`, `status` (COMPLETED / NOT_STARTED / LIVE)
- `matchedAt` (UTC ISO 8601)
- `venue` (場館)
- `homeSquadId`, `awaySquadId`
- `squadMatchResults[]` → `wonRounds`, `lostRounds`, `wonScore`, `lostScore`

### 4. 戰績資料結構 (teams_record)
每隊包含：
- `name`, `matchesPlayed`, `wins`, `losses`
- `winRate`, `points`
- `score_3_0`, `score_3_1`, `score_3_2`, `score_0_3`, `score_1_3`, `score_2_3`
- `setsWon`, `setsLost`, `setWinRate`
- `pointsFor`, `pointsAgainst`, `pointsRatio`

## 球隊資訊 (2025-26 賽季)

| ID | 中文名 | 英文名 |
|----|--------|--------|
| 11380 | 臺中連莊 | Taichung Winstreak |
| 11382 | 台鋼天鷹 | TSG SkyHawks |
| 11383 | 臺北伊斯特 | Taipei East Power |
| 11381 | 桃園雲豹飛將 | Taoyuan Leopards |

## 賽季資訊
- 2025-26 賽季：約 2025/10 - 2026/05
- leagueId: 23, seasonId: 171, eventId: 419

## 結論
- **無公開 API**，需認證才能存取
- **主要資料來源**: 從頁面 HTML 中提取 `__NEXT_DATA__` JSON
- 首頁提供最新 5 場已完賽 + 5 場未來賽程 + 戰績
- 賽程頁提供所有已完成比賽
- 未來賽程的完整列表可能需要透過頁面滾動載入（分頁 API，需要進一步調查）
