# 指数 API (index) — 公开版

共2个公开接口。

---

### 1. index_detail - 指数详情

**描述**: 获取指数的详细信息

**请求**:
- 方法: GET
- 路径: /index/detail
- 参数:
  - `indexTicker` (string, 可选) - 指数代码 (如: HSTECH.HK)

**示例**:
```javascript
const result = await call('index_detail', {
  indexTicker: 'HSTECH.HK'
});
```

**返回字段**:
- 指数基本信息、编制方案、成分股等详细信息

---

### 2. index_daily - 指数历史日行情

**描述**: 获取指数的历史日行情数据

**请求**:
- 方法: GET
- 路径: /index/daily
- 参数:
  - `indexTickers` (string, 可选) - 指数代码列表，逗号分隔 (如: 000001.SH,000300.SH)
  - `startDate` (string, 可选) - 开始日期 (YYYY-MM-DD)
  - `endDate` (string, 可选) - 结束日期 (YYYY-MM-DD)

**示例**:
```javascript
const result = await call('index_daily', {
  indexTickers: '000001.SH,000300.SH',
  startDate: '2026-06-01',
  endDate: '2026-06-05'
});
```

**返回字段**:
- 日期、开盘价、收盘价、最高价、最低价、成交量、涨跌幅等行情数据