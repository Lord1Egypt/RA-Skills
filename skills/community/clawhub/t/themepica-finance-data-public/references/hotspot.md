# 热点 API (hotspot) — 公开版

共10个公开接口。

---

### 1. hotspot_heats - 热点热度

**描述**: 获取热点的热度数据

**请求**:
- 方法: POST
- 路径: /hotspot/heats
- Body参数:
  - `keywords` (array, 必填) - 关键词列表
  - `startTime` (string, 必填) - 开始时间 (YYYY-MM-DD HH:mm:ss)
  - `endTime` (string, 必填) - 结束时间 (YYYY-MM-DD HH:mm:ss)

**热度分段**:
- 热度 > 200: 高热
- 20 < 热度 ≤ 200: 热
- 热度 ≤ 20: 低热

**示例**:
```javascript
const result = await call('hotspot_heats', {
  keywords: ['英伟达'],
  startTime: '2026-08-03 00:00:00',
  endTime: '2026-08-12 12:34:32'
});
```

---

### 2. hotspot_emotions - 热点情绪

**描述**: 获取热点的情绪数据

**请求**:
- 方法: POST
- 路径: /hotspot/emotions
- Body参数:
  - `keywords` (array, 必填) - 关键词列表
  - `startTime` (string, 必填) - 开始时间
  - `endTime` (string, 必填) - 结束时间

**情绪分段**:
- 情绪 > 0.2: 积极
- 情绪 < -0.05: 消极
- 其他: 中性

**示例**:
```javascript
const result = await call('hotspot_emotions', {
  keywords: ['牛来'],
  startTime: '2026-08-13 00:00:00',
  endTime: '2026-08-17 13:34:32'
});
```

---

### 3. hotspot_news - 热点关联资讯

**描述**: 获取热点关联的资讯列表

**请求**:
- 方法: GET
- 路径: /hotspot/news
- 参数:
  - `startTime` (string, 可选) - 开始时间
  - `endTime` (string, 可选) - 结束时间
  - `keywords` (string, 可选) - 关键词
  - `category` (string, 可选) - 分组

**示例**:
```javascript
const result = await call('hotspot_news', {
  startTime: '2026-08-21',
  endTime: '2026-08-21',
  keywords: '消费贷',
  category: '事件'
});
```

---

### 4. hotspot_viewpoints - 热点关联观点

**描述**: 获取热点关联的观点

**请求**:
- 方法: GET
- 路径: /hotspot/viewpoints
- 参数:
  - `startTime` (string, 可选) - 开始时间
  - `endTime` (string, 可选) - 结束时间
  - `keywords` (string, 可选) - 关键词

**示例**:
```javascript
const result = await call('hotspot_viewpoints', {
  startTime: '2026-07-09',
  endTime: '2026-07-14',
  keywords: '石油'
});
```

---

### 5. hotspot_securities - 热点关联证券

**描述**: 获取热点关联的证券

**请求**:
- 方法: GET
- 路径: /hotspot/securities
- 参数:
  - `startTime` (string, 可选) - 开始时间
  - `endTime` (string, 可选) - 结束时间
  - `keywords` (string, 可选) - 关键词
  - `start` (string, 可选) - 起始位置
  - `end` (string, 可选) - 结束位置

**示例**:
```javascript
const result = await call('hotspot_securities', {
  startTime: '2026-08-17',
  endTime: '2026-08-17',
  keywords: 'AI',
  start: '0',
  end: '10'
});
```

---

### 6. hotspot_indices - 热点关联指数

**描述**: 获取热点关联的指数

**请求**:
- 方法: GET
- 路径: /hotspot/indices
- 参数:
  - `startTime` (string, 可选) - 开始时间
  - `endTime` (string, 可选) - 结束时间
  - `keywords` (string, 可选) - 关键词

**示例**:
```javascript
const result = await call('hotspot_indices', {
  startTime: '2026-07-17',
  endTime: '2026-07-23',
  keywords: '标普石油'
});
```

---

### 7. hotspot_themes - 热点相关主题

**描述**: 获取热点相关的主题

**请求**:
- 方法: GET
- 路径: /hotspot/themes
- 参数:
  - `startTime` (string, 可选) - 开始时间
  - `endTime` (string, 可选) - 结束时间
  - `keywords` (string, 可选) - 关键词

**示例**:
```javascript
const result = await call('hotspot_themes', {
  startTime: '2025-05-09',
  endTime: '2025-05-21',
  keywords: '华为'
});
```

---

### 8. hotspot_etfs - 热点关联ETF

**描述**: 获取热点关联的ETF

**请求**:
- 方法: GET
- 路径: /hotspot/etfs
- 参数:
  - `startTime` (string, 可选) - 开始时间
  - `endTime` (string, 可选) - 结束时间
  - `keywords` (string, 可选) - 关键词

**示例**:
```javascript
const result = await call('hotspot_etfs', {
  startTime: '2026-08-19',
  endTime: '2026-08-19',
  keywords: '眼镜'
});
```

---

### 9. hotspot_policies - 热点关联政策

**描述**: 获取热点关联的政策

**请求**:
- 方法: GET
- 路径: /hotspot/policies
- 参数:
  - `startTime` (string, 可选) - 开始时间
  - `endTime` (string, 可选) - 结束时间
  - `keywords` (string, 可选) - 关键词
  - `start` (string, 可选) - 起始位置
  - `end` (string, 可选) - 结束位置
  - `category` (string, 可选) - 分类

**示例**:
```javascript
const result = await call('hotspot_policies', {
  startTime: '2026-01-17',
  endTime: '2026-01-21',
  keywords: 'AI'
});
```

---

### 10. hotspot_funds - 热点关联基金

**描述**: 获取热点关联的基金

**请求**:
- 方法: GET
- 路径: /hotspot/funds
- 参数:
  - `startTime` (string, 可选) - 开始时间
  - `endTime` (string, 可选) - 结束时间
  - `keywords` (string, 可选) - 关键词

**示例**:
```javascript
const result = await call('hotspot_funds', {
  startTime: '2026-08-17',
  endTime: '2026-08-17',
  keywords: '智能机器人'
});
```