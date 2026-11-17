# 榜单 API (board) — 公开版

共4个公开接口。

---

### 1. board_hotspots - 热点榜单(周度)

**描述**: 获取周度热点榜单列表

**请求**:
- 方法: GET
- 路径: /board/hotspots
- 参数:
  - `pageNum` (string, 可选) - 页编号
  - `pageSize` (string, 可选) - 页大小
  - `returnTotalNum` (boolean, 可选) - 是否返回总数

**示例**:
```javascript
const result = await call('board_hotspots', { pageNum: '1', pageSize: '10' });
```

---

### 2. board_hotspots_detail - 热点榜单详情

**描述**: 获取指定日期的热点榜单详情

**请求**:
- 方法: POST
- 路径: /board/hotspots/detail
- Body参数:
  - `startTime` (string, 必填) - 开始时间 (YYYY-MM-DD)
  - `endTime` (string, 必填) - 结束时间 (YYYY-MM-DD)

**示例**:
```javascript
const result = await call('board_hotspots_detail', {
  startTime: '2026-08-18',
  endTime: '2026-08-18'
});
```

---

### 3. board_hotspots_latest_detail - 最新热点榜单详情

**描述**: 获取最新的热点榜单详情

**请求**:
- 方法: GET
- 路径: /board/hotspots/latest/detail

**示例**:
```javascript
const result = await call('board_hotspots_latest_detail');
```

---

### 4. board_indices - 指数机会榜单

**描述**: 获取指数机会榜单

**请求**:
- 方法: GET
- 路径: /board/indices
- 参数:
  - `startDate` (string, 可选) - 开始日期
  - `endDate` (string, 可选) - 结束日期

**示例**:
```javascript
const result = await call('board_indices', {
  startDate: '2026-08-03',
  endDate: '2026-08-03'
});
```