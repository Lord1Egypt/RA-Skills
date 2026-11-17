# 主题 API (themes) — 公开版

共7个公开接口。

---

### 1. themes - 主题列表

**描述**: 获取主题列表

**请求**:
- 方法: GET
- 路径: /themes
- 参数:
  - `pageNum` (int, 必填) - 页编号
  - `pageSize` (int, 必填) - 页大小
  - `returnTotalNum` (boolean, 可选) - 是否返回总数

**返回字段**:
- `themeId` (int) - 主题ID
- `themeName` (string) - 主题名称
- `themeCreateDate` (string) - 主题创建日期
- `themeDescription` (string) - 主题描述
- `hasSecPool` (boolean) - 是否有股票池
- `secPoolCreateDate` (string) - 股票池创建日期
- `isQuarterlyTheme` (boolean) - 是否季度重点主题
- `themeUpdateDate` (string) - 主题更新日期
- `latestHeat` (float) - 主题最新热度
- `hotwords` (array) - 主题相关热词

**示例**:
```javascript
const result = await call('themes', { pageNum: 1, pageSize: 10 });
```

---

### 2. theme_indices - 主题关联指数

**描述**: 获取主题关联的指数列表

**请求**:
- 方法: GET
- 路径: /theme/indices
- 参数:
  - `themeId` (string, 必填) - 主题ID

**返回字段**:
- `themeId` (int) - 主题ID
- `themeName` (string) - 主题名称
- `indexName` (string) - 指数名称
- `tickerSymbol` (string) - 指数代码
- `market` (string) - 市场
- `introduce` (string) - 指数介绍
- `secFullName` (string) - 证券全称

**示例**:
```javascript
const result = await call('theme_indices', { themeId: '3' });
```

---

### 3. theme_etfs - 主题关联ETF

**描述**: 获取主题关联的ETF列表

**请求**:
- 方法: GET
- 路径: /theme/etfs
- 参数:
  - `themeId` (string, 必填) - 主题ID

**示例**:
```javascript
const result = await call('theme_etfs', { themeId: '3' });
```

---

### 4. theme_diagnose - 主题诊断信息

**描述**: 获取主题的诊断信息，包括热度、情绪、象限、信号等

**请求**:
- 方法: GET
- 路径: /theme/diagnose
- 参数:
  - `themeId` (string, 必填) - 主题ID

**返回字段**:
- `themeId` (int) - 主题ID
- `themeName` (string) - 主题名称
- `heat` (float) - 热度
- `heatLevel` (string) - 热度等级（高热/热/温/冷）
- `sentiment` (float) - 情绪
- `sentimentLevel` (string) - 情绪等级（积极/中性/消极）
- `consensus` (float) - 共识度
- `consensusLevel` (string) - 共识度等级（高度/中度/低度）
- `quadrant` (string) - 象限（蓄力/明星/分歧/沉寂）
- `signal` (string) - 信号（机会/风险/观察）

**示例**:
```javascript
const result = await call('theme_diagnose', { themeId: '1477062244' });
```

---

### 5. theme_subs_diagnose - 主题诊断_子主题

**描述**: 获取主题及其子主题的诊断信息

**请求**:
- 方法: GET
- 路径: /theme/subs/diagnose
- 参数:
  - `themeId` (string, 必填) - 主题ID

**示例**:
```javascript
const result = await call('theme_subs_diagnose', { themeId: '3' });
```

---

### 6. theme_narratives - 主题叙事数据

**描述**: 获取主题的叙事数据，包括热度、情绪的时间序列

**请求**:
- 方法: GET
- 路径: /theme/narratives
- 参数:
  - `themeId` (string, 必填) - 主题ID
  - `startDate` (string, 可选) - 开始日期 (YYYY-MM-DD)
  - `endDate` (string, 可选) - 结束日期 (YYYY-MM-DD)

**示例**:
```javascript
const result = await call('theme_narratives', { 
  themeId: '5900',
  startDate: '2026-08-01',
  endDate: '2026-08-13'
});
```

---

### 7. theme_contents - 主题相关资讯

**描述**: 获取主题相关的资讯列表

**请求**:
- 方法: GET
- 路径: /theme/contents
- 参数:
  - `themeId` (int, 必填) - 主题ID
  - `pageNum` (int, 可选) - 页编号（默认1）
  - `pageSize` (int, 可选) - 页大小（默认10）
  - `startDate` (string, 必填) - 开始日期 (YYYY-MM-DD)
  - `endDate` (string, 必填) - 结束日期 (YYYY-MM-DD)
  - `newsCategory` (string, 必填) - 资讯分类（如：事件）

**示例**:
```javascript
const result = await call('theme_contents', { 
  themeId: 8,
  pageSize: 10,
  pageNum: 1,
  startDate: '2026-08-17',
  endDate: '2026-08-17',
  newsCategory: '事件'
});
```