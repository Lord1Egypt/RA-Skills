# 基金 API (fund) — 公开版

共1个公开接口。

---

### 1. fund_narratives - 基金叙事数据

**描述**: 获取基金的叙事数据

**请求**:
- 方法: GET
- 路径: /v2.1/fund/narratives
- 参数:
  - `fundTicker` (string, 必填) - 基金代码

**示例**:
```javascript
const result = await call('fund_narratives', {
  fundTicker: '516090'
});
```

**返回字段**:
- 基金叙事相关数据，包括热度、情绪等时间序列信息

**说明**:
- 基金叙事数据提供基金在市场中的关注度、情绪变化等叙事维度分析
- 可用于跟踪基金的市场表现和投资者情绪