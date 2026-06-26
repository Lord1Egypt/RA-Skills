新品快速爆发（基础版）

> **分类**：一、新品爆发型 | **难度**：⭐ | **适用阶段**：日常选品巡检 / 快速跟品

---

## 核心逻辑

上架时间极短但销量已经起飞的产品，往往把握住了新兴未被满足的需求。
Review 数还很少说明竞争壁垒尚未建立，**现在跟进是成本最低的窗口期**。

## 触发场景

- "我想找最近出来的爆款新品"
- "帮我筛一下上架2个月内销量超300的产品"

## MCP 工具

`mcp__sellersprite__product_research`

## 参数配置

```json
{
  "marketplace": "US",
  "availableMonth": 2,
  "minUnits": 300,
  "maxRatings": 100,
  "minRating": 4.2,
  "variation": "Y",
  "order": {"field": "total_units", "desc": true},
  "size": 20
}
```

## 参数说明

| 参数 | 含义 | 建议值 | 调节指南 |
|------|------|--------|----------|
| `availableMonth` | 上架月数上限 | ≤ 2 | 放宽到 3 可获得更多结果 |
| `minUnits` | 月最低销量 | ≥ 300 | 大类目可提高到 500 |
| `maxRatings` | 最大评论数 | ≤ 100 | 确保竞争壁垒未建立 |
| `minRating` | 最低评分 | ≥ 4.2 | 低于此值说明产品有缺陷 |
| `variation` | 排除变体 | Y | 避免同父体重复计算 |

## 结果解读要点

1. **优先看 FBA 且中国卖家**：说明供应链可复制
2. **关注 BSR 7天增长率**：`bsrCr` 为负值说明排名还在上升
3. **警惕品牌词**：如果标题含知名品牌名，跟进风险极大
4. **交叉验证**：对筛出的 ASIN 调用 `mcp__sellersprite__asin_prediction` 确认销量趋势是否真实（注意：`asin_prediction` 不支持批量查询，需对多个 ASIN **并行调用**以节省等待时间）

## 风险提示

- 新品销量可能是刷单或站外引流导致的虚假繁荣
- 务必用 `mcp__sellersprite__traffic_source` 检查流量结构是否健康（注意：`traffic_source` 不支持批量查询，需对多个 ASIN **并行调用**以节省等待时间）
- 季节性产品（如万圣节、圣诞节）需额外排除

## 组合打法

本 SKILL 筛出候选 ASIN 后，建议串联：
1. → **评论语义分析**：确认竞品痛点，找到改良方向
2. → **自然流量反查**：验证是否过度依赖广告
3. → **标题密度漏洞**：寻找 Listing 优化入口
---

## 参考文档

本 Skill 涉及的 API 详细参数说明：

- [`asin_prediction`](../../reference/asin_prediction.md)
- [`product_research`](../../reference/product_research.md)
- [`traffic_source`](../../reference/traffic_source.md)
