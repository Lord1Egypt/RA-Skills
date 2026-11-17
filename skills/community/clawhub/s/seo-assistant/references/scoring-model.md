# SEO Score 计算模型

`seo_audit.py` 对每个维度打 0–100 分，再按权重加权得到整站 SEO Score（0–100，越高越好）。

## 维度权重

| 维度 | key | 权重 |
| --- | --- | --- |
| 关键词分析 | keyword | 10 |
| Title 分析 | title | 15 |
| Description 分析 | description | 10 |
| Heading 分析 | heading | 10 |
| URL 分析 | url | 10 |
| Internal Link 分析 | internal_link | 10 |
| Schema 分析 | schema | 10 |
| Indexability 分析 | indexability | 20 |
| 页面分析 | page | 5 |
| **合计** | | **100** |

## 计算流程

1. **逐页打分**：对每页计算 `title/description/heading/url/schema/indexability/page/keyword` 八个子分（逻辑见 `seo-metrics.md`）。
2. **维度聚合**：每个维度取**全站页面均值**（internal_link 为站点级图计算，不参与逐页均值）。
3. **总分加权**：
   - 九维度均有权重 → `SEO Score = Σ(维度分 × 权重) / 100`。
   - 单页模式（`page` 子命令）时 `internal_link` 无法评估（记为 `null`），其权重 10 摊分到其余维度：`SEO Score = Σ(有值维度分 × 权重) / 90`。
4. **跨页修正**：标题/描述重复、孤岛页、noindex 等跨页问题在聚合/建议阶段体现扣分。

## 等级参考（仅供参考，非硬性阈值）

| 分数 | 等级 | 含义 |
| --- | --- | --- |
| 90–100 | 优秀 | 基本无需改动 |
| 75–89 | 良好 | 少量低风险优化 |
| 60–74 | 中等 | 存在明确可优化项 |
| 40–59 | 偏弱 | 多项基础问题 |
| < 40 | 较差 | 需系统性重构 |

## 复检（重新检查）

执行优化后再次运行 `audit` 或 `score`，对比前后 SEO Score 与各维度分，确认低风险项已生效、高风险项经确认后落地。
