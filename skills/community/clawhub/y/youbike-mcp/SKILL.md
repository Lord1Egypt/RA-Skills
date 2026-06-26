---
name: youbike-mcp
description: 提供台北市、新北市及桃園市 YouBike 2.0 站點的即時狀態查詢，支援經緯度近鄰搜尋及關鍵字搜尋。
---

# YouBike MCP Server

本技能透過 MCP Server 提供北北桃地區 YouBike 2.0 的即時資訊。

## 功能列表

1. **近鄰搜尋 (`get_nearby_stations`)**:
   - 輸入：縣市名稱（台北市/新北市/桃園市）、緯度、經度。
   - 輸出：依距離排序的最近站點即時狀態。

2. **關鍵字搜尋 (`search_stations`)**:
   - 輸入：縣市名稱（台北市/新北市/桃園市）、關鍵字（如：捷運科技大樓站）。
   - 輸出：符合關鍵字的站點即時狀態。

## 資料來源

- **台北市**: `https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json`
- **新北市**: `https://data.ntpc.gov.tw/api/datasets/010e5b15-3823-4b20-b401-b1cf000550c5/json?size=2000`
- **桃園市**: `https://opendata.tycg.gov.tw/api/v1/dataset.api_access?rid=08274d61-edbe-419d-8fcc-7a643831283d&format=json`

## 本地開發

### 安裝依賴
```bash
npm install
```

### 啟動服務
```bash
npm start
```

### 執行整合測試
```bash
npm test
```
