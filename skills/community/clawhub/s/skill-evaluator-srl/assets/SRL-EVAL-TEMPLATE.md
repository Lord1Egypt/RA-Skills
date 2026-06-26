# [SKILL_NAME] — SRL 评估报告 / SRL Evaluation Report

**日期 / Date:** YYYY-MM-DD
**评估者 / Evaluator:** AI
**技能版本 / Skill Version:** [version or commit]
**Tier 分类 / Tier Classification:** [Tier 1 确定性 / Tier 2 半确定性 / Tier 3 非确定性]

---

## 总评 / Overall Summary

| 指标 / Metric | 结果 / Result |
|------|------|
| **最终得分 / Final Score** | /100 |
| **SRL 等级 / SRL Level** | SRL-? |
| **星级 / Rating** | ☆☆☆☆☆ |
| **使用建议 / Usage Recommendation** | |

> SRL 等级参考:
> - SRL-5 (90-100 ★★★★★): 全流程工程化，可进入自动化决策链路
> - SRL-4 (75-89 ★★★★): 关键步骤锚定可靠平台，结果基本可复现
> - SRL-3 (60-74 ★★★): 混入部分弱校验环节，适合在明确边界下使用
> - SRL-2 (40-59 ★★): 大量依赖互联网信息或 AI 推理，需人工复核
> - SRL-1 (<40 ★): 全链路 AI 推理，无工程锚点，不建议用于正式决策

---

## 五维评分明细 / 5-Dimension Scoring

| 维度 / Dimension | 权重 / Weight | 原始分 / Raw | 修正后 / Corrected | 加权 / Weighted |
|------|------|------|------|------|
| 工程锚点密度 / Anchor Density | 25% | | | |
| 幻觉暴露面 / Hallucination Exposure | 20% | | | |
| 失败语义清晰度 / Failure Transparency | 20% | | | |
| 溯源性 / Traceability | 20% | | | |
| 可重现性推断 / Reproducibility | 15% | | | |

---

## 子项评分 / Sub-Score Details

### 工程锚点密度 / Anchor Density

| 子项 / Sub-criterion | 满分 / Max | 得分 / Score | 评估依据 / Evidence |
|------|------|------|------|
| 锚点覆盖率 / anchor_coverage | 40 | | |
| 锚点密度 / anchor_intensity | 30 | | |
| 验证闭环 / verification_loop | 30 | | |
| **小计** | **100** | | |

### 幻觉暴露面 / Hallucination Exposure

| 子项 / Sub-criterion | 满分 / Max | 得分 / Score | 评估依据 / Evidence |
|------|------|------|------|
| 推测性步骤占比 / speculative_ratio | 40 | | |
| 外部验证覆盖率 / external_validation | 30 | | |
| 输出确定性 / output_determinism | 30 | | |
| **小计** | **100** | | |

### 失败语义清晰度 / Failure Transparency

| 子项 / Sub-criterion | 满分 / Max | 得分 / Score | 评估依据 / Evidence |
|------|------|------|------|
| 错误处理策略 / error_handling_strategy | 40 | | |
| 置信度降级机制 / confidence_degradation | 30 | | |
| "我不知道"能力 / idk_capability | 30 | | |
| **小计** | **100** | | |

### 溯源性 / Traceability

| 子项 / Sub-criterion | 满分 / Max | 得分 / Score | 评估依据 / Evidence |
|------|------|------|------|
| 数据来源分类 / source_classification | 40 | | |
| 引用标注 / citation_annotation | 30 | | |
| 可独立验证性 / independent_verifiability | 30 | | |
| **小计** | **100** | | |

### 可重现性推断 / Reproducibility

| 子项 / Sub-criterion | 满分 / Max | 得分 / Score | 评估依据 / Evidence |
|------|------|------|------|
| Tier 确定性 / tier_determinism | 40 | | |
| 状态管理 / state_management | 30 | | |
| 步骤确定性 / step_determinism | 30 | | |
| **小计** | **100** | | |

---

## 修正因子 / Correction Factors

| 因子 / Factor | 评分 / Score (0-100) | 是否触发 / Triggered | 影响 / Impact |
|------|------|------|------|
| 时效性 / Timeliness | | ☐ | 可重现性线性扣减，最大 20% |
| 鲁棒性 / Robustness | | ☐ | 幻觉暴露面线性扣减，最大 10% |
| 级联稳定性 / Cascade Stability | | ☐ | 可重现性线性扣减，最大 20% |

---

## 最终计算 / Final Calculation

```
final_score = anchor × 0.25 + hallucination × 0.20 + transparency × 0.20 + traceability × 0.20 + reproducibility × 0.15
            =   ?    × 0.25 +      ?       × 0.20 +      ?        × 0.20 +      ?       × 0.20 +       ?        × 0.15
            = ___/100
```

---

## 改进行动清单 / Improvement Actions

> 按维度得分从低到高排序，为得分最低的 3 个维度各生成 1-2 条具体可执行的建议。

### 🔧 [维度名] 当前得分 ?/100

1. **[具体行动]** — [预期效果]
2. **[具体行动]** — [预期效果]

### 🔧 [维度名] 当前得分 ?/100

1. **[具体行动]** — [预期效果]
2. **[具体行动]** — [预期效果]

### 🔧 [维度名] 当前得分 ?/100

1. **[具体行动]** — [预期效果]
2. **[具体行动]** — [预期效果]

---

## 优先级修复清单 / Priority Fixes

### P0 — 发布前必须修复
1.

### P1 — 应该修复
1.

### P2 — 可选优化
1.

---

## 修订历史 / Revision History

| 日期 / Date | 得分 / Score | SRL 等级 / Level | 备注 / Notes |
|------|------|------|------|
| | /100 | SRL-? | 基线评估 / Baseline |
