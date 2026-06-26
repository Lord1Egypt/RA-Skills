自然流量主导型竞品反查

> **分类**：五、流量防伪型 | **难度**：⭐⭐⭐ | **适用阶段**：竞品验真 / 广告策略制定

---

## 核心逻辑

找真正靠自然搜索排名卖断货的产品，避开全靠亏本广告推上去的虚假繁荣品。

## 触发场景

- "我想验证竞品的流量结构是否健康"
- "帮我反查自然流量占比高的竞品"
- "这个产品的销量是真实的还是靠广告堆出来的？"

## MCP 工具（两步法）

### Step 1 & Step 2：并行调用（同时获取流量结构与流量来源）

> **并行调用** `mcp__sellersprite__traffic_keyword_stat`、`mcp__sellersprite__traffic_source` 和 `mcp__sellersprite__keepa_info`（这三个工具均仅支持单个 ASIN 查询，不支持批量，但对同一 ASIN 应将三个调用同时发起，避免串行等待）

#### traffic_keyword_stat
```json
{
  "marketplace": "US",
  "asin": "B0XXXXXXXXX",
  "month": "202604"
}
```

#### traffic_source
```json
{
  "marketplace": "US",
  "q": "B0XXXXXXXXX"
}
```

#### keepa_info（交叉验证）
```json
{
  "marketplace": "US",
  "asin": "B0XXXXXXXXX"
}
```

## 参数说明

| 参数 | 含义 | 建议值 | 调节指南 |
|------|------|--------|----------|
| `asin` | 目标竞品 ASIN | 必填 | 选择销量较高的竞品 |
| `q` | 查询关键词 | 目标ASIN | traffic_source 使用此参数 |

## 判断标准

| 指标 | 健康 | 危险 |
|------|------|------|
| 自然搜索词占比 | > 60% | < 30% |
| SP广告词占比 | < 30% | > 50% |
| AC推荐词 | 有 | 无 |

## 结果解读要点

1. **自然流量占比 > 60%**：产品有真实的市场认可度，值得研究学习
2. **广告词占比 > 50%**：高度依赖广告，销量可能随广告停投而骤降
3. **AC推荐词存在**：说明产品被亚马逊算法认可，转化率较高
4. **交叉验证**：`mcp__sellersprite__keepa_info` 已在上方与 traffic_keyword_stat、traffic_source **并行调用**，直接使用返回的价格和排名历史趋势数据

## 风险提示

- 自然流量高可能部分来自品牌词搜索，而非品类词，需拆分查看
- 广告占比较高不一定是坏事，新品期广告投放是正常策略
- 流量结构会随时间变化，建议定期复查
- 数据为快照，不同时间点的流量结构可能差异较大

## 组合打法

本 SKILL 验真完成后，建议串联：
1. → **标题密度漏洞**：从健康竞品流量词里找 SEO 优化机会
2. → **评论语义分析**：对验真竞品做痛点拆解
3. → **新品快速爆发**：验证该竞品是否属于新品爆发型
---

## 参考文档

本 Skill 涉及的 API 详细参数说明：

- [`keepa_info`](../../reference/keepa_info.md)
- [`traffic_keyword_stat`](../../reference/traffic_keyword_stat.md)
- [`traffic_source`](../../reference/traffic_source.md)
