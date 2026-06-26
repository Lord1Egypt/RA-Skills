低品牌垄断大盘类目

> **分类**：四、类目结构型 | **难度**：⭐⭐ | **适用阶段**：品类筛选 / 大盘扫描

---

## 核心逻辑

品牌集中度低 + 亚马逊自营占比低 = **白牌卖家的天堂**。

## 触发场景

- "帮我找品牌集中度低的类目"
- "我想看哪些类目适合白牌卖家进入"
- "有没有没有被大品牌垄断的蓝海类目？"

## MCP 工具

`mcp__sellersprite__market_research`

## 参数配置

```json
{
  "marketplace": "US",
  "maxBrandCrn": 0.45,
  "maxAmazonSelfProportion": 0.1,
  "minAvgUnits": 200,
  "minAvgPrice": 15,
  "order": {"field": "total_units", "desc": true},
  "size": 20
}
```

## 参数说明

| 参数 | 含义 | 建议值 | 调节指南 |
|------|------|--------|----------|
| `maxBrandCrn` | 品牌集中度上限 | < 45% | 降到 35% 可筛选更分散的市场 |
| `maxAmazonSelfProportion` | 亚马逊自营占比上限 | < 10% | 确保自营不占据头部流量 |
| `minAvgUnits` | 平均月销量下限 | ≥ 200 | 确保市场有足够需求 |
| `minAvgPrice` | 平均售价下限 | > $15 | 排除低价低利润类目 |

## 结果解读要点

1. **品牌集中度 < 35%**：极度分散市场，白牌卖家进入壁垒低
2. **亚马逊自营占比 = 0%**：无自营竞争，最佳进入条件
3. **平均销量 > 300 且品牌数 > 20**：市场规模足够且竞争格局健康
4. **深度验证**：**并行调用** `mcp__sellersprite__market_brand_concentration` 和 `mcp__sellersprite__market_seller_concentration`（这两个工具均仅支持单个 nodeIdPath 查询，不支持批量，需将所有筛出节点的调用同时发起）做进一步确认

## 风险提示

- 低品牌集中度可能意味着品类门槛低，容易陷入同质化价格战
- 部分类目虽然品牌分散，但可能有隐性壁垒（如认证要求、特殊供应链）
- 市场数据反映的是当前状态，竞争格局可能快速变化
- 建议结合 `mcp__sellersprite__market_product_concentration` 确认商品集中度

## 组合打法

本 SKILL 筛出候选类目后，建议串联：
1. → **高新品占比市场**：在低垄断类目里找新品能存活的市场
2. → **高毛利轻小品**：在低垄断类目里找利润好的产品
3. → **流量分散关键词**：在目标类目中找到竞争未固化的关键词
---

## 参考文档

本 Skill 涉及的 API 详细参数说明：

- [`market_brand_concentration`](../../reference/market_brand_concentration.md)
- [`market_product_concentration`](../../reference/market_product_concentration.md)
- [`market_research`](../../reference/market_research.md)
- [`market_seller_concentration`](../../reference/market_seller_concentration.md)
