ABA 高增长趋势词（持续爬升）

> **分类**：二、关键词趋势型 | **难度**：⭐⭐ | **适用阶段**：趋势选品 / 品类机会发现

---

## 核心逻辑

ABA 搜索排名数据反映真实买家搜索行为。
**连续 3 个月搜索量持续上升 + 头部点击未固化** = 新兴需求正在形成。

## 触发场景

- "我想看哪些关键词的搜索量在持续上升"
- "帮我找买家需求正在增长但竞争还没固化的词"
- "有没有最近搜索量一直在涨的品类机会词？"

## MCP 工具

`mcp__sellersprite__keyword_research`

## 参数配置

```json
{
  "marketplace": "US",
  "minSearchNearlyCr": 0.05,
  "maxAraClickRate": 0.6,
  "minSearches": 3000,
  "order": {"field": "searches", "desc": true},
  "size": 20
}
```

## 参数说明

| 参数 | 含义 | 建议值 | 调节指南 |
|------|------|--------|----------|
| `minSearchNearlyCr` | 近3月搜索增长率下限 | > 5% | 提高到 10% 可筛选更强势的增长词 |
| `maxAraClickRate` | 点击集中度上限 | < 60% | 降到 50% 可排除头部已固化的词 |
| `minSearches` | 月搜索量下限 | ≥ 3000 | 降到 1000 可发现小众增长词 |

## 结果解读要点

1. **连续 3 月增长率均 > 5%**：趋势确立，非短期波动
2. **点击集中度 < 40%**：新卖家有机会获取流量
3. **搜索量 + 增长率双高**：优先关注的核心机会词
4. **交叉验证**：调用 `mcp__sellersprite__google_trend` 做外部趋势确认（该工具支持 `keywords` 数组参数，可一次批量查询多个关键词）

## 风险提示

- 增长趋势可能由短期事件（如社交媒体热门话题）驱动，需判断持续性
- 高增长词会快速吸引竞争者跟进，窗口期可能较短
- 部分增长词可能与现有产品不匹配，需结合供应链能力判断
- 务必用 `mcp__sellersprite__keyword_miner` 确认实际竞争格局（提示：`keyword_miner` 支持 `keywordList` 数组参数，可一次批量查询多个关键词）

## 组合打法

本 SKILL 筛出候选关键词后，建议串联：
1. → **流量分散关键词**：确认是否存在未被垄断的关键词
2. → **标题密度漏洞**：在增长词中发现 SEO 优化机会
3. → **新品快速爆发**：在增长词对应的品类中寻找已爆发的竞品
---

## 参考文档

本 Skill 涉及的 API 详细参数说明：

- [`google_trend`](../../reference/google_trend.md)
- [`keyword_miner`](../../reference/keyword_miner.md)
- [`keyword_research`](../../reference/keyword_research.md)
