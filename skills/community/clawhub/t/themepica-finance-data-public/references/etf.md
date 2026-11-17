# ETF API (etf) — 公开版

共1个公开接口。

---

### 1. etf_narratives - ETF叙事数据

**描述**: 获取ETF的叙事数据

**请求**:
- 方法: GET
- 路径: /etf/narratives
- 参数:
  - `etfTicker` (string, 可选) - ETF代码 (如: 159994)

**示例**:
```javascript
const result = await call('etf_narratives', {
  etfTicker: '159994'
});
```

**返回字段**:
- ETF叙事相关数据，包括热度、情绪等时间序列信息