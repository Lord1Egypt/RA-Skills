# 🚌 臺北市公車定點車機 Skill

[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18-brightgreen)](https://nodejs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

整合**臺北市公車動態資料（TstBusEvent）**與**交通部 PTX 開放平台**，提供即時公車查詢、到站時間估算、路線站序、站牌座標與脫班異常偵測。

---

## ✨ 功能特色

| 功能 | 說明 |
|------|------|
| 🚍 **即時車機** | 每分鐘抓取 TstBusEvent.json，即時掌握公車動態 |
| 📍 **PTX 座標** | 全臺北市站牌座標離線快取，Haversine 精確估算 |
| ⏱ **站序 ETA** | 依站序計算剩餘站數，最精確的到站時間 |
| 🛣 **路線搜尋** | 以路名、幹線、顏色搜尋公車路線 |
| ⚠️ **脫班偵測** | 自動偵測勤務/車輛異常公車 |
| 🔥 **熱點分析** | 找出公車密度最高的站點 |

---

## 🚀 快速開始

### 需求

- **Node.js ≥ 18**
- **Python 3**（建置快取用）
- 網路連線（呼叫即時 API）

### 安裝

```bash
# 複製模組（推薦）
cp -r ~/.qclaw/skills/taipei-bus/lib ./taipei-bus-lib

# 或 npm 安裝
npm install taipei-bus-skill
```

### 首次使用：建置快取

```bash
cd ~/.qclaw/skills/taipei-bus
python3 scripts/build-cache.py
```

這會產生 `data/stop-coords.json` 與 `data/route-full-cache.json`，供離線查詢。

### 第一個查詢

```javascript
const {
  fetchAll,
  findByRoute,
  getStopCoords,
  formatBus
} = require('./taipei-bus-lib/bus-api.js');

async function main() {
  // 1. 抓全量即時公車
  const buses = await fetchAll();
  console.log(`目前 ${buses.length} 台公車在線`);

  // 2. 以路線代碼查
  const routeBuses = await findByRoute('158701');
  routeBuses.forEach(b => console.log(formatBus(b)));

  // 3. 查站牌座標
  const coords = getStopCoords('33210');
  console.log('站牌:', coords.name, coords.lat, coords.lon);
}

main().catch(console.error);
```

---

## 🔑 雙 ID 系統（重要）

| 系統 | 代碼範例 | 用途 |
|------|---------|------|
| **TstBusEvent（車機 ID）** | RouteID: `158701` / StopID: `179647` | 即時車機查詢 |
| **PTX（交通部統一 ID）** | RouteID: `10132` / StopID: `33210` | 路線站序查詢 |

> ⚠️ **兩套 ID 為獨立系統，不可直接互通。** 需透過站名搜尋建立橋接。

---

## API 參考

### 即時車機 API（bus-api.js）

#### `fetchAll()`
抓取全量即時公車資料（TstBusEvent.json）。按資料更新時間倒序排列。

```javascript
const buses = await fetchAll();
console.log(`共 ${buses.length} 台公車在線`);
```

#### `findByRoute(routeId)`
依 BusEvent 路線代碼，查詢所有在線公車。

```javascript
const buses = await findByRoute('158701');
```

#### `findByBus(busId)`
依車牌號碼查單台公車狀態。

```javascript
const bus = await findByBus('021-FW');
```

#### `findAtStation(stopId)`
查詢目前停在特定站位的公車。

```javascript
const atStation = await findAtStation('179647');
```

#### `detectAnomalies()`
偵測勤務異常或車輛異常的公車。

```javascript
const anomalies = await detectAnomalies();
// DutyStatus !== '1' 或 BusStatus !== '0'
```

#### `routeSummary()`
全系統路線概況摘要。

```javascript
const summary = await routeSummary();
const topRoutes = Object.entries(summary)
  .sort((a,b) => b[1].count - a[1].count)
  .slice(0, 5);
```

#### `fetchAllWithCoords()`
取得所有公車並附加站牌座標資訊（`_stopCoords` 欄位）。

```javascript
const enriched = await fetchAllWithCoords();
```

#### `etaEstimate(routeId, targetStopId, avgSpeedKmh?)`
依 Haversine 球面距離估算到站時間。

```javascript
const eta = await etaEstimate('158701', '185365', 25);
// { minutes: 8, bus: {...}, note: '依直線距離約 1.23 km（25km/h）估算' }
```

---

### PTX 座標 API（stop-coords.js）

#### `getStopCoords(stopId)`
依 PTX StopID 查站牌座標與名稱。

```javascript
const coords = getStopCoords('33210');
// { name: '歡仔園', lat: 25.0626, lon: 121.4573, stationId: '...' }
```

#### `searchStops(keyword, limit?)`
模糊搜尋站名。

```javascript
const found = searchStops('捷運', 5);
```

#### `getHotspots(topN?)`
取得公車密度最高的站點。

```javascript
const hotspots = await getHotspots(10);
```

---

### PTX 路線 API（route-api.js）

#### `searchRouteByName(name)`
以路名搜尋公車路線。

```javascript
const route = searchRouteByName('234');
// { routeId: '10132', routeName: '234', departure: '...', terminal: '...' }
```

#### `getRouteStopSequence(routeId, direction?)`
取得某路線的全部站序（`0`=去程，`1`=返程）。

```javascript
const stops = getRouteStopSequence('10132', 0);
stops.forEach((s, i) => console.log(`${i+1}. ${s.stopName}`));
```

#### `etaBySequence(routeId, targetStopId, direction?, avgSecPerStop?)`
依站序估算到站時間（最精確）。

```javascript
const eta = etaBySequence('10132', '33210', 0, 90);
// { minutes: 12, remaining: 8, total: 36, note: '依站序（第 10/36 站）...' }
```

#### `getRoutesByStop(stopId)`
查某站點在所有路線的經過情形。

```javascript
const passingRoutes = getRoutesByStop('33210');
```

---

## ⚙️ ETA 三種精度模式

| 模式 | 計算方式 | 精度 |
|------|---------|------|
| **站序（Precise）** | 剩餘站數 × 90s | ⭐⭐⭐⭐⭐ |
| **Haversine** | 直線距離 ÷ 時速 | ⭐⭐⭐ |
| **Fixed Fallback** | 固定 500m ÷ 時速 | ⭐ |

---

## 💬 使用情境對話

| 使用者提問 | 呼叫函式 | 回覆 |
|-----------|---------|------|
| 「忠孝幹線多久會到？」 | `searchRouteByName` → `etaBySequence` | 「預估約 8 分鐘到站，離終點尚有 6 站」 |
| 「藍 10 有幾台車在跑？」 | `searchRouteByName` → `findByRoute` | 「目前有 7 台公車在線」 |
| 「哪些站公車最多？」 | `getHotspots(10)` | 熱點站排名 |
| 「脫班偵測」 | `detectAnomalies()` | 「✅ 全系統正常」或異常列表 |
| 「設定早上 7:30 路線提醒」 | qclaw-cron-skill | Cron Job 設定完成 |

---

## ⚠️ 已知限制

1. **無 GPX 軌跡追蹤**：TstBusEvent 為定點車機，兩站之間無位置資料
2. **獨立 ID 未橋接**：BusEvent RouteID 與 PTX RouteID 無自動對照表
3. **無公車轉乘路由**：需串接地圖 API（如騰訊地圖）
4. **快取為靜態快照**：需手動執行 `build-cache.py` 更新
5. **僅支援臺北市公車**：新北、桃園等需另外串接

---

## 📁 檔案架構

```
taipei-bus/
├── lib/
│   ├── bus-api.js        ← 即時車機 + PTX 整合主模組
│   ├── route-api.js      ← PTX 路線 / 站序快取
│   └── stop-coords.js    ← PTX 站牌座標快取
├── data/                  ← 快取檔
│   ├── stop-coords.json
│   └── route-full-cache.json
├── examples/
│   ├── example-all-functions.js
│   ├── example-eta.js
│   ├── example-anomaly.js
│   ├── example-route-api.js
│   ├── example-cron.js
│   └── example-map.js
├── scripts/
│   └── build-cache.py    ← 建置快取腳本
└── docs/
    ├── index.html        ← 線上文檔
    └── README.md         ← 本檔案
```

---

## 🔄 更新快取

```bash
# 建置站牌座標快取
python3 scripts/build-cache.py
```

建議頻率：站牌座標每月一次，路線快取每季一次。

---

## 📜 授權

| 資料來源 | 授權 |
|---------|------|
| 臺北市政府公車動態資料 | [政府資料開放授權（OGDL）](https://data.taipei) |
| PTX 公共運輸整合資料 | [PTX MIT License](https://ptx.transportdata.tw) |
| taipei-bus Skill 本體 | MIT License |

> 💡 向使用者呈現資料時，請標示來源：「資料來源：臺北市政府開放資料 + 交通部 PTX」

---

*文件的最後更新：2026 年 8 月*
