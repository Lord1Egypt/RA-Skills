# 🚌 臺北市公車定點車機 Skill（含 PTX 座標 +路線整合）

> 串接臺北市定點車機 OD 即時 API + PTX Bus Stop/Route 整合，
> 提供含 GPS 的公車動態查詢、**依站序精確 ETA**、地圖視覺化、脫班偵測、路線資訊等智慧化功能。

**語言：繁體中文（預設）**

---

## 📡 資料來源

### 1️⃣ 定點車機即時 API（公車位置）
| 項目 | 內容 |
|------|------|
| API | `https://tcgbusfs.blob.core.windows.net/blobbus/TstBusEvent.json` |
| 說明 | 每台公車即時一筆，含車牌、路綫、站點 |
| 更新頻率 | 不定期（約即時） |
| 授權 | 公開免費 |

### 2️⃣ PTX Bus Stop API（站牌座標）
| 項目 | 內容 |
|------|------|
| API | `https://ptx.transportdata.tw/MOTC/v2/Bus/Stop/City/Taipei` |
| 本地快取 | `data/stop-coords.json`（**28741 站**，離線可用） |

### 3️⃣ PTX Bus Route + StopOfRoute API（路線站序）🆕
| 項目 | 內容 |
|------|------|
| Route | `https://ptx.transportdata.tw/MOTC/v2/Bus/Route/City/Taipei` |
| StopOfRoute | `https://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/City/Taipei` |
| 本地快取 | `data/route-full-cache.json`（**415 條路線**，含 819 筆站序） |

---

## 🚀 快速開始

### Agent 觸發關鍵字
```
公車到哪了、公車快到了嗎、等公車
「234 這條線多久會到？」
「搜尋公車：藍」
「158701 這條線現在有幾台車」
「查 KKC-1100」
「哪裡有公車脫班？」
「公車地圖」
「搜尋站牌：捷運」
```

### Node.js 腳本
```bash
cd ~/.qclaw/skills/taipei-bus
node examples/example-all-functions.js   # 即時車機 + 座標
node examples/example-route-api.js       # 路線站序 + 精確 ETA 🆕
```

---

## 📋 欄位說明

### 公車車機（Vehicle API）
| 欄位 | 說明 |
|------|------|
| `BusID` | 車牌號碼 |
| `RouteID` | 公車路綫代碼（內部碼，非 PTX） |
| `StopID` | 目前所在站點代碼（內部碼，非 PTX） |
| `CarOnStop` | 是否停在站位（1=是, 0=否） |
| `DutyStatus` | 勤務狀態（1=上班） |
| `BusStatus` | 公車狀態（0=正常） |
| `DataTime` | 資料時間 |

### PTX 路線（Route API）
| 欄位 | 說明 |
|------|------|
| `RouteID` | PTX 路綫代碼（5-6位數，如 `10132`） |
| `routeName` | 路綫名（如 `234`、`南京幹線`） |
| `DepartureStopNameZh` | 起点站名 |
| `TerminalStopNameZh` | 訖點站名 |
| `Direction` | 0=去程, 1=返程 |

### PTX 站序（StopOfRoute）
| 欄位 | 說明 |
|------|------|
| `StopID` | PTX 站點代碼 |
| `StopSequence` | 站序（起點=1） |
| `StopPosition` | WGS84 經緯度 |

---

## 🔧 核心函式

### 即時車機
```javascript
fetchAll()              // 全量即時公車資料
findByRoute(routeId)    // 特定路綫所有公車
findByBus(busId)        // 以車牌查單台
findAtStation(stopId)   // 某站停靠公車
detectAnomalies()       // 脫班/異常偵測
routeSummary()          // 全系統路綫概況
```

### PTX 座標整合
```javascript
fetchAllWithCoords()     // 公車 + 站牌座標
getHotspots(topN)        // 公車密度最高的站點
getStopCoords(stopId)    // 依 StopID 查座標
searchStops(keyword)     // 站名模糊搜尋
```

### PTX 路名 / 站序整合 🆕
```javascript
searchRouteByName(name)         // 路名 → RouteID（"234"、"南京"）
getRouteInfo(routeId)          // 路線完整資訊（起訖、首末班、業者）
searchRoutes(keyword, limit?)   // 模糊搜尋所有匹配路綫
getRouteStopSequence(routeId, direction?) // 路綫全部站序
getRoutesByStop(stopId)         // 某站有哪些路綫經過
```

### 精確 ETA 🆕
```javascript
etaBySequence(routeId, targetStopId, direction?, avgSecPerStop?)
// → { minutes, remaining, total, stop, note }
// 依剩餘站數 × 平均站距秒數估算（預設 90s/站）
```

---

## 📁 檔案結構

```
taipei-bus/
├── SKILL.md
├── README.zh-TW.md             # 繁體中文（本檔）
├── README.en.md                # English
├── lib/
│   ├── bus-api.js              # 核心（含整合）
│   ├── stop-coords.js          # PTX 座標查詢
│   └── route-api.js            # PTX 路名/站序 🆕
├── data/
│   ├── stop-coords.json        # 28741 站座標
│   ├── stop-of-route-cache.json # 站序 raw
│   └── route-full-cache.json    # 415 條路綫 🆕
├── scripts/
│   └── build-cache.py          # 快取建置腳本
└── examples/
    ├── example-all-functions.js
    ├── example-route-api.js     # 路名/站序/ETA 🆕
    ├── example-eta.js
    ├── example-anomaly.js
    ├── example-cron.js
    └── example-map.js
```

---

## 🔄 更新快取

```bash
# 重建全部快取（需先執行 scripts/build-cache.py → 產生 stop-coords.json
# 和 stop-of-route-cache.json，再由 Python 重建 route-full-cache.json）
```

> 注意：快取靜態，TstBusEvent 的 `RouteID`/`StopID` 與 PTX 不同体系，
> 需透過**站名搜尋**建立對照。

---

## ⚠️ 限制

1. **TstBusEvent ID ≠ PTX ID**：兩套 ID 体系獨立，精確對照需站名比對
2. **ETA 精度**：站序版 ±1-2 站，快取靜態，建議每季重建
3. **路線覆蓋**：PTX 覆蓋臺北市主要公車，特定區間車/副綫可能缺漏

---

## 📄 授權

- 公車車機：臺北市政府交通局公運處，政府資料開放授權
- PTX 站牌/路綫：交通部 PTX 開放資料平臺
