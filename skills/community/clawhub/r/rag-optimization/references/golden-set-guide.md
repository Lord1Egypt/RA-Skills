# Golden Set 建设指南

> Golden Set（黄金测试集）是评估 RAG 系统的"标尺"——没有它，任何优化都无法量化。
> 本技能自带 `assets/test-cases-example.json`（58 例），本文说明如何为你的领域建设专属测试集。

## 一、为什么需要 Golden Set

RAG 优化的核心流程是 **诊断 → 选策略 → 实施 → 评估**，而"评估"必须有固定的测试集和标准答案，否则：

- 无法回答"这次改动到底提升了多少"（需要 Ablation 对比）
- 不同策略之间的效果没有可比性
- 回归问题（改 A 坏了 B）无法被及时发现

## 二、用例结构（与 evaluate.py 契约一致）

```json
{
  "query": "用户真实查询",
  "expected_answer": "标准答案（人工编写）",
  "expected_doc_ids": ["doc_001", "doc_002"],
  "category": "概念理解",
  "difficulty": "easy"
}
```

| 字段 | 说明 |
|------|------|
| query | 从真实查询日志中采样，不要凭空编造 |
| expected_answer | 人工编写的权威答案，作为生成质量对照 |
| expected_doc_ids | 应被检索到的文档 id（对应你的语料库 id） |
| category | 类别（概念理解/技术实现/架构对比/多跳推理/评估方法/参数调优/问题解决） |
| difficulty | 难度（easy/medium/hard） |

## 三、建设步骤

1. **采样**：从真实用户查询日志抽取 2-3 周的查询，去重、清洗。
2. **配额**：按类别与难度设置目标配额（参考本技能分布：概念理解 10、技术实现 12、架构对比 10、多跳推理 8、评估方法 7、参数调优 6、问题解决 5；难度 easy:medium:hard ≈ 1:3:1.5）。
3. **标注**：每个用例由一人编写 query + expected_answer + expected_doc_ids，**至少另一人交叉复核**，重点核对 expected_doc_ids 是否确实能回答该 query。
4. **落地**：expected_doc_ids 必须能映射到你实际语料库中的文档 id（本技能的 doc_XXX 是占位示例，接入真实系统时替换）。
5. **维护**：每季度审查一次——淘汰过时用例、补充新领域用例、修正标注错误。**测试集变更后，历史基准报告作废，需重新建立基准。**

## 四、规模建议

| 阶段 | 用例数 | 用途 |
|------|--------|------|
| 起步 | 30-50 | 建立基准、发现明显问题 |
| 稳定 | 100-200 | 支持策略间精细对比 |
| 成熟 | 500+ | 支撑发布级评估与回归 |

> 原则：**先小后大、宁精勿滥**。50 个高质量用例远胜 500 个随意编写的用例。

## 五、与 Ablation 配合

```bash
# 1. 优化前建立基准
python scripts/evaluate.py --test-data assets/test-cases-example.json --output baseline.json

# 2. 实施某项优化后
python scripts/evaluate.py --test-data assets/test-cases-example.json --output after.json --compare baseline.json
```

`--compare` 会输出新旧指标 diff，用数据决定策略去留。
