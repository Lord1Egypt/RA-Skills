活跃供血市场（高新品占比）

> **分类**：四、类目结构型 | **难度**：⭐⭐ | **适用阶段**：品类筛选 / 新品可行性评估

---

## 核心逻辑

头部 100 个产品中新品占比 > 5% = **市场持续洗牌，新品有机会挤进头部**。

## 触发场景

- "帮我找新品还能挤进头部的活跃市场"
- "我想评估某个类目新品进入的机会"
- "有没有市场持续洗牌、新品有机会的类目？"

## MCP 工具

`mcp__sellersprite__market_research`

## 参数配置

```json
{
  "marketplace": "US",
  "minNewProportion": 0.05,
  "minNewAvgUnits": 100,
  "newProduct": 6,
  "order": {"field": "total_units", "desc": true},
  "size": 20
}
```

## 参数说明

| 参数 | 含义 | 建议值 | 调节指南 |
|------|------|--------|----------|
| `minNewProportion` | 新品占比下限 | > 5% | 提高到 8% 可筛选更活跃的市场 |
| `minNewAvgUnits` | 新品平均月销量 | ≥ 100 | 确保新品不只是上架但不出单 |
| `newProduct` | 新品定义（月数） | ≤ 6 | 缩短到 3 可筛选更严格的新品 |

## 结果解读要点

1. **新品占比 > 8% 且新品均销 > 150**：市场活跃度极高，新品存活率好
2. **新品占比高但均销低**：市场虽开放但竞争激烈，需谨慎评估
3. **结合上架时间分布**：**并行调用** `mcp__sellersprite__market_listing_date_distribution` 和 `mcp__sellersprite__market_listing_trend_distribution`（这两个工具均仅支持单个 nodeIdPath 查询，不支持批量，需将所有候选节点的调用同时发起），一次性获取生命周期结构与新品趋势数据

## 风险提示

- 新品占比高可能意味着市场门槛低，大量跟卖者涌入导致利润快速下降
- 部分新品可能是变体拆分或老品翻新，需逐一确认
- 新品数据波动大，建议持续观察 2~3 个月确认趋势
- 新品平均销量可能被个别爆款拉高，需看中位数而非均值

## 组合打法

本 SKILL 筛出候选类目后，建议串联：
1. → **低品牌垄断类目**：叠加 = "白牌友好型活跃市场"
2. → **新品快速爆发**：在这些类目里精准搜索刚爆发的新品
3. → **ABA高增长趋势词**：确认类目对应的关键词需求是否在增长
---

## 参考文档

本 Skill 涉及的 API 详细参数说明：

- [`market_listing_date_distribution`](../../reference/market_listing_date_distribution.md)
- [`market_listing_trend_distribution`](../../reference/market_listing_trend_distribution.md)
- [`market_research`](../../reference/market_research.md)
