# SKILL.md — 臺北市公車定點車機 Skill

> 版本：1.2.0 | 更新：2026-08-10

---

## 觸發關鍵字

```
公車、公車動態、等公車、公車到站、公車多久、公車地圖、公車追蹤
公車來了、公車怎麼還沒到、公車即時、公車站牌、公車路線、公車搜尋
公車首班、公車末班、公車熱點、公車脫班
bus dynamic、bus ETA、台北公車、臺北市公車
```

---

## 簡介

串接三個資料來源：
1. **臺北市定點車機 OD** 即時 API — 公車即時位置
2. **PTX Bus Stop API** — 站牌座標（28,741 站）
3. **PTX Bus Route/StopOfRoute API** — 公車路線含站序（415 條）

提供：即時車位查詢、**依站序精確 ETA**、路線資訊、地圖視覺化、脫班偵測等功能。

---

## ⚠️ 重要：兩套 ID 體系

| 系統 | 說明 | ID 範例 |
|------|------|---------|
| **TstBusEvent**（即時車機）| 車位資料，內部碼 | RouteID=`158701`, StopID=`179647` |
| **PTX Route/Stop** | 路線時刻表+站序，開放碼 | RouteID=`10132`（=234線），StopID=`33210` |

> 兩套 ID **不相通**，需透過**站名/路線名搜尋**建立對照。

---

## 資料來源

| 來源 | URL | 內容 | 快取 |
|------|-----|------|------|
| 車機即時 | `tcgbusfs.blob.core.windows.net/blobbus/TstBusEvent.json` | 即時車位 | 無（每次即時抓） |
| PTX 站牌 | `ptx.transportdata.tw/MOTC/v2/Bus/Stop/City/Taipei` | 28,741 站座標 | `data/stop-coords.json` |
| PTX 路線 | `ptx.transportdata.tw/MOTC/v2/Bus/Route/City/Taipei` | 415 條路名/起訖 | `data/route-full-cache.json` |
| PTX 站序 | `ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/City/Taipei` | 站點順序/方向 | `data/route-full-cache.json` |

---

## 模組架構

```
lib/
├── bus-api.js         — 核心整合（車機 + PTX）
├── route-api.js       — PTX 路名/站序（快取查詢）
└── stop-coords.js    — PTX 座標查詢（快取查詢）
```

---

## 核心函式速查

### 即時車機（fetchAll, findByRoute...）
```javascript
const { fetchAll, findByRoute, findByBus, findAtStation,
        detectAnomalies, routeSummary } = require('./lib/bus-api.js');

await fetchAll()              // → [{BusID, RouteID, StopID, CarOnStop, DataTime...}]
await findByRoute('158701')  // → [BusRecord]
await findByBus('KKC-1100')  // → BusRecord | null
await findAtStation('179647') // → [BusRecord]
await detectAnomalies()       // → [BusRecord] DutyStatus!=='1' or BusStatus!=='0'
await routeSummary()          // → { [routeId]: { count, buses } }
```

### PTX 座標整合
```javascript
const { getStopCoords, searchStops, batchGetStopCoords,
        fetchAllWithCoords, getHotspots } = require('./lib/bus-api.js');

getStopCoords('33210')        // → { name, lat, lon, stationId }
searchStops('捷運', 5)        // → [{stopId, name, lat, lon...}]
batchGetStopCoords(['33210','33211'])
await fetchAllWithCoords()    // → [BusRecord + _stopCoords]
await getHotspots(10)         // → [{stopId, stopName, lat, lon, count}]
```

### PTX 路名 / 站序整合
```javascript
const { searchRouteByName, getRouteInfo, searchRoutes,
        getRouteStopSequence, getRoutesByStop,
        etaBySequence } = require('./lib/bus-api.js');

searchRouteByName('234')      // → { routeId:'10132', routeName:'234', departure, terminal... }
searchRoutes('藍', 5)          // → [RouteInfo]
getRouteInfo('10132')         // → RouteInfo（完整資訊）
getRouteStopSequence('10132', 0) // → [StopEntry] 去程全部站序
getRoutesByStop('33210')      // → [{routeId, routeName, direction, index...}]
etaBySequence('10132', '33210', 0)  // → { minutes, remaining, total, note }
```

### 格式化輸出
```javascript
const { formatBus, routeApi } = require('./lib/bus-api.js');

formatBus(busRecord, true)              // 人類可讀（含座標）
routeApi.formatRoute(routeInfo)        // 路線完整資訊
routeApi.formatStopSequence(seq, rid, dir) // 站序 + 周邊站
```

---

## 實用範例

### 1. 查公車到站時間
```javascript
const { findByRoute, etaEstimate } = require('./lib/bus-api.js');

const buses = await findByRoute('158701');
if (buses.length) {
  const eta = await etaEstimate('158701', '179647');
  console.log(`約 ${eta.minutes} 分鐘，${eta.note}`);
}
```

### 2. 以站序估算（最精確）
```javascript
const { searchRouteByName, etaBySequence, getRouteStopSequence } = require('./lib/bus-api.js');

// 搜尋「234」→ RouteID=10132 → 查站序
const route = searchRouteByName('234');
const stops = getRouteStopSequence(route.routeId, 0);
// 找「歡仔園」的 StopID → 估算
const stopEntry = stops.find(s => s.stopName.includes('歡仔園'));
if (stopEntry) {
  const eta = etaBySequence(route.routeId, stopEntry.stopId, 0);
  console.log(`預估 ${eta.minutes} 分鐘（${eta.note}）`);
}
```

### 3. 脫班異常偵測
```javascript
const { detectAnomalies, formatBus } = require('./lib/bus-api.js');

const anomalies = await detectAnomalies();
if (anomalies.length === 0) {
  console.log('✅ 全系統正常');
} else {
  anomalies.forEach(b => console.log(formatBus(b)));
}
```

### 4. 站名搜尋 + 經過路線
```javascript
const { searchStops, getRoutesByStop } = require('./lib/bus-api.js');

const hits = searchStops('捷運', 3);
for (const stop of hits) {
  const routes = getRoutesByStop(stop.stopId);
  console.log(`${stop.name} 有 ${routes.length} 條路線`);
}
```

### 5. 公車熱點站位
```javascript
const { getHotspots } = require('./lib/bus-api.js');

const hotspots = await getHotspots(5);
hotspots.forEach((h, i) =>
  console.log(`${i+1}. ${h.stopName} — ${h.count} 台公車`)
);
```

---

## 對話式使用情境

| 使用者問題 | 呼叫函式 | 回覆格式 |
|-----------|---------|---------|
| 「234 多久會到？」 | `searchRouteByName('234')` + `etaEstimate()` | 約 N 分鐘 |
| 「XX 站有幾台公車？」 | `findAtStation(stopId)` | N 台停在站位 |
| 「查 KKC-1100」 | `findByBus('KKC-1100')` | 車牌/路線/站點 |
| 「哪裡公車最多？」 | `getHotspots()` | TOP N 站 |
| 「路線藍10的站序」 | `searchRouteByName('藍10')` + `getRouteStopSequence()` | 完整站名列表 |
| 「公車都正常嗎？」 | `detectAnomalies()` | ✅ 或 ⚠️ + 明細 |
| 「234 的首末班？」 | `searchRouteByName('234')` + `getRouteInfo()` | 首班/末班時間 |

> ⚠️ 「我在 XX 站，要去 OO 地址」的轉乘推薦需地址 geocoding + 轉乘演算法，**目前尚未實作**（需要騰訊地圖 geocoding 或大眾運輸轉乘 API）。

---

## 快取檔案

| 檔案 | 大小 | 內容 | 更新頻率 |
|------|------|------|---------|
| `data/stop-coords.json` | ~2 MB | PTX 站牌座標 28,741 站 | 每季重建 |
| `data/route-full-cache.json` | ~11 MB | PTX 路線+站序 415 條 | 每季重建 |
| `data/stop-of-route-cache.json` | ~12 MB | StopOfRoute raw | 每季重建 |

重建：`python3 scripts/build-cache.py`

---

## 依賴

- **Node.js 18+**（原生 `fetch` API）
- `qclaw-cron-skill`（定時監控）
- `tencentmap-jsapi-gl-skill`（地圖視覺化）

---

## 限制

1. **ID 體系不相通**：TstBusEvent 與 PTX 的 RouteID/StopID 為獨立系統，需站名/路線名搜尋建立對照
2. **ETA 精度**：站序版 ±1-2 站，快取為靜態snapshot
3. **即時資料覆蓋**：TstBusEvent 僅含部分在線車機車輛，非全部公車
4. **無轉乘推薦**：需 geocoding + 轉乘 API，目前未實作
5. **無擁擠度資料**：目前 API 不含乘客人數

---

## 參考文件

- `README.zh-TW.md` — 繁體中文使用說明
- `README.en.md` — English documentation
- `examples/` — 各功能範例腳本
- `docs/index.html` — 完整文件網站
