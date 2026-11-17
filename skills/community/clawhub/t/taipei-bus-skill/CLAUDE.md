# CLAUDE.md — AI Agent 引用指南

本檔案給 AI Agent（Claude / QClaw）使用此 Skill 時參考。

---

## 快速入口

```javascript
// 只需要一行 require，即可使用全部功能
const bus = require('~/.qclaw/skills/taipei-bus/lib/bus-api.js');
```

---

## 呼叫流程（標準模式）

當使用者詢問公車相關資訊時：

```
1. 理解使用者問題
   ↓
2. 呼叫對應函式
   ↓
3. 格式化輸出（用 formatBus() / routeApi.formatRoute()）
   ↓
4. 附加說明與操作建議
```

---

## 常用呼叫模式

### 模式 A：使用者已知路線名（如「234」、「藍10」）

```javascript
// Step 1: 以路名找 RouteID
const route = bus.searchRouteByName('234');
// → { routeId: '10132', routeName: '234', departure: '板橋', terminal: '...' }

// Step 2: 取得站序
const stops = bus.getRouteStopSequence(route.routeId, 0);

// Step 3: 查 ETA（取第一台車 + 目標站）
const buses = await bus.findByRoute(route.routeId); // 注意：這是 TstBusEvent 的 internal RouteID，需對照
```

### 模式 B：使用者已知站名（如「捷運市政府站」）

```javascript
// Step 1: 以站名搜尋 StopID
const hits = bus.searchStops('捷運市政府', 5);
// → [{stopId: '...', name: '捷運市政府站(松高)', lat: ..., lon: ...}]

// Step 2: 查該站有哪些路線
const passingRoutes = bus.getRoutesByStop(hits[0].stopId);
// → [{routeId: '...', routeName: '藍5', direction: 0, index: 3}]

// Step 3: 估算到站
const eta = bus.etaBySequence(route.routeId, hits[0].stopId, direction);
```

### 模式 C：使用者已知車牌（如「KKC-1100」）

```javascript
const record = await bus.findByBus('KKC-1100');
console.log(bus.formatBus(record, true));
```

---

## ID 對照速查表

| 使用者輸入 | 轉換方式 | 對應 PTX StopID |
|-----------|---------|----------------|
| 「234 線」 | `searchRouteByName('234')` | RouteID=`10132` |
| 「藍10」 | `searchRouteByName('藍10')` | RouteID=`10792` |
| 「捷運市政府站」| `searchStops('捷運市政府')` | StopID=`...` |
| 「歡仔園」| `searchStops('歡仔園')` | StopID=`33210` |

> ⚠️ `findByRoute()` / `findAtStation()` 傳入的是 **TstBusEvent 內部 RouteID/StopID**（如 `158701`、`179647`），需先以 PTX 站名搜尋轉換。

---

## 輸出格式化規範

```
✅ 成功：明確數字 + 具體資訊 + 操作建議
❌ 無資料：說明原因 + 提供替代方案
⚠️ 異常：清楚標示異常項目 + 影響程度
```

**good:** `🚌 路線 234 預估 5 分鐘到站（亞東科技大學），第 10/37 站`
**bad:** `查到一個結果`

---

## 限制提醒（主動說明）

向使用者說明時，主動提及：
1. ETA 為估算值，實際可能誤差 ±1-2 站
2. 即時資料僅含在線車機車輛，非全部公車
3. 轉乘推薦需地址 geocoding（尚未實作）

---

## 範例回覆模板

### 查 ETA
```
🚌 路線 234（板橋 → 漢口街）最新一台公車
   📍 亞東科技大學（第 10/37 站，行駛中）
   ⏱️  預估到站：約 27 分鐘（依站序估算，±2站）
   🔄 去程方向
```

### 無車在線
```
⚠️ 路線 234 目前無公車在線回報
💡 可能原因：非尖峰時段班次少，或該路線非全線皆有車機
📌 建議查詢 234 的首班/末班時間，或稍後再查
```

### 脫班偵測
```
✅ 目前全系統公車正常行駛
   共 2 台在線，分別在路線 158701
```

---

## 與其他 Skill 的整合

- **地圖**：`tencentmap-jsapi-gl-skill` — 將 `fetchAllWithCoords()` / `getHotspots()` 產出的座標標注在騰訊地圖
- **定時監控**：`qclaw-cron-skill` — 用 `detectAnomalies()` / `routeSummary()` 設定 Cron Job
- **推播**：`message` tool — Cron Job 發現異常時主動推播到 LINE/Telegram

---

## 資料欄位對照（供 Agent 理解）

### TstBusEvent（車機）
| 欄位 | 意義 |
|------|------|
| `BusID` | 車牌 |
| `RouteID` | **內部**路線碼（非 PTX）|
| `StopID` | **內部**站點碼（非 PTX）|
| `CarOnStop='1'` | 停在站位 |
| `DutyStatus='1'` | 上班勤務 |
| `BusStatus='0'` | 正常行駛 |

### PTX Route / StopOfRoute
| 欄位 | 意義 |
|------|------|
| `RouteID` | PTX 路線碼（5位，如 `10132`）|
| `Direction=0` | 去程 |
| `Direction=1` | 返程 |
| `StopSequence` | 站序（起點=1）|
| `PositionLat/Lon` | WGS84 座標 |

---

*最後更新：2026-08-10*
