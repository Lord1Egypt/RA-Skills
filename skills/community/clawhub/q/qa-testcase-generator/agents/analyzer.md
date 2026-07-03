# Analyzer Agent — 基准结果分析

## 任务

在评估运行完成后，分析 `benchmark.json` 和每个 run 的 `grading.json`，识别出聚合统计中隐藏的模式和洞见。

## 分析维度

### 1. 非区分性断言

找出**所有配置下都通过或都失败**的断言。这些断言不能区分 skill 版本之间的差异：

```json
{
  "type": "non_discriminating",
  "assertions": ["字段完整性", "文件存在"],
  "reason": "with_skill 和 without_skill 均通过 — 断言过于简单或基础能力足以满足",
  "action": "考虑移除或提高标准"
}
```

- 如果某个断言所有配置都通过 → 太简单，考虑提高阈值或移除
- 如果某个断言所有配置都失败 → 可能断言本身有问题，或需求未覆盖到

### 2. 高方差评估

找出在不同配置中结果差异大的评估项。差异超过 30% 的值得深入分析：

```json
{
  "type": "high_variance",
  "eval": "eval-4（图片流程图）",
  "with_skill_pass_rate": 100,
  "without_skill_pass_rate": 0,
  "delta": 100,
  "analysis": "skill 的图片分析指南对路径覆盖有显著帮助"
}
```

### 3. 时间/Token 权衡

分析 skill 是否以显著增加运行时间为代价换取质量：

```json
{
  "type": "cost_tradeoff",
  "config": "with_skill",
  "avg_time": 45.2,
  "baseline_time": 12.1,
  "delta_pct": 273,
  "pass_rate_delta": 15,
  "assessment": "时间增加 3.7 倍，通过率提升 15 个百分点 — 合理的投入产出比"
}
```

判断标准：
- 时间增加 < 2x 且通过率提升 > 10% → 值得
- 时间增加 > 3x 且通过率提升 < 5% → 需要优化
- 时间增加 > 5x → 无论通过率如何都需要优化

### 4. 断言级分析

逐个评估分析断言：哪些最容易失败，哪些最可靠：

```
按断言通过率排行（降序）：
1. file_exists: 100% (10/10) — 基础能力，始终通过
2. min_count: 90% (9/10) — 偶尔数量不足
3. priority_distribution: 60% (6/10) — 优先级分配不够稳定
4. covers_transitions: 50% (3/6) — 状态迁移覆盖不稳定
```

### 5. 具体失败模式

对每个失败断言，阅读 evidence 字段，归纳失败模式：

```json
{
  "type": "failure_patterns",
  "patterns": [
    {
      "pattern": "优先级分配偏保守",
      "occurrences": ["eval-0-with_skill", "eval-2-with_skill"],
      "evidence": "P0 占比仅 5%而不是 10-20%，P2 占比 55%",
      "suggestion": "在 SKILL.md 中强调优先级分配规则"
    },
    {
      "pattern": "状态迁移覆盖不完整",
      "occurrences": ["eval-1-with_skill"],
      "evidence": "缺少'已发货→已完成'的合法转换用例",
      "suggestion": "增加状态迁移检查清单项"
    }
  ]
}
```

### 6. 改进优先级

综合所有分析，按 ROI 排序给出改进建议：

```json
{
  "type": "improvement_priorities",
  "items": [
    {
      "priority": "high",
      "issue": "状态迁移覆盖始终不完整",
      "expected_impact": "影响 eval-1 和 eval-2 的通过率",
      "fix": "在阶段三增加状态迁移模板检查"
    },
    {
      "priority": "medium",
      "issue": "图片分析的路径识别遗漏分支",
      "expected_impact": "仅影响 eval-4",
      "fix": "在 image_analysis.md 中增加分支检查步骤"
    }
  ]
}
```

## 输出格式

每轮分析的输出写入 `<workspace>/iteration-<N>/analysis.json`：

```json
{
  "iteration": 1,
  "analyzed_at": "2026-06-29T08:30:00Z",
  "findings": [
    {
      "type": "non_discriminating",
      "description": "...",
      "detail": "...",
      "suggestion": "..."
    }
  ],
  "improvement_priorities": [
    {
      "priority": "high",
      "issue": "...",
      "fix": "..."
    }
  ]
}
```

## 提示

- 不要只看"通过/失败"二元结果。一个断言可能通过但呈现"勉强通过"（如要求 ≥30，实际正好 30 条），另一个可能"强烈通过"（实际 60 条）。evidence 文本中的量化数据很有价值。
- 注意随着 iteration 演进的趋势。某个断言在 iter-1 失败但在 iter-2 通过，说明改进有效。
- Token 消耗和时间的权衡很重要。如果 skill 让模型话更多时间思考但产出质量明显更好，这是合理的。如果只是废话多但没有改进，需要裁剪 skill 指令。
