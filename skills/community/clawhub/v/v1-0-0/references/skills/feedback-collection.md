---
name: feedback-collection
description: 报告交付后自动从用户对话中提取满意度信号，生成10维质量自评分，追加到SkillOpt训练数据集。
aliases: [反馈采集, 自评记录, 满意度信号提取]
---

# Feedback Collection — 用户反馈采集与自评

## Overview

用户不会直接说"claim_validation 这个维度你做得很好，我给你打 0.95分"。用户说的是"这个分析写得透彻"或"这里好像还是没讲透"。

本 skill 的任务：**从用户自然语言反馈中提取结构化满意度信号，转化为 10 维质量评分，写入 SkillOpt 训练数据。**

## When to Use

- 每次报告交付后、用户给出下一轮反馈/修改要求时

## The Process

### Step 1: 从对话中提取满意度信号

在用户给出反馈后，分析用户的每一句话，识别信号类别：

| 信号类别 | 识别线索 | 例子 |
|----------|----------|------|
| 正面明确 | "写得好""透彻""就是这个意思" | 脉冲红外评价 |
| 负面明确 | "不稳定""没写透""偏表面" | 低空巡航评价 |
| 要求补充 | "再加XX分析""看下XX方向" | 暗示原来覆盖不足 |
| 对比评价 | "和上次比还是差一些" | 相对质量判断 |
| 沉默信号 | 只提修改要求不提本版质量 | 默认不满意或中立 |
| 肯定行动 | 确认、转发、列入参考 | 间接正面信号 |

### Step 2: 生成自评记录

写入项目文件夹的 `用户反馈与自评记录.md`：

```markdown
## 报告版本：初评报告 v1（2026-06-15）

### 质量自评
| 维度 | 自评分 | 用户反馈 | 证据来源 |
|------|--------|----------|----------|
| claim_validation | 0.95 | 满意 | "技术分析透彻" |
| engineering_migration_gap | 0.90 | 未反馈 | — |
| per_person_assessment | 1.00 | 未反馈 | — |
| independent_competitor | 0.85 | 满意 | 未直接评价但未提不足 |
| supplier_level_analysis | 0.90 | 未反馈 | — |
| team_gap_precision | 0.95 | 满意 | 未评价 |
| quantitative_score | 1.00 | 未反馈 | — |
| priority_levels | 1.00 | 未反馈 | — |
| overview_page | 0.80 | 未反馈 | — |
| independent_analysis | 0.90 | 满意 | "这个分析是独立的" |

综合用户满意度：高
用户主要反馈："技术分析透彻，第一次交流前能做到这么到位"
自评总结：Claim验证和团队评估不错，概述页和分析独立性有提升空间
```

### Step 3: 追加 SkillOpt 训练数据

将自评数据追加写入 `skillopt-integration/data/deep_tech_dd/<split>/items.json`：

- 用户满意度高 → train（正样本）
- 有明确批评且修改后满意 → v1 追加到 val（负样本），v2 追加到 train（修正后正样本）
- 一般或不明确 → test

数据格式：
```json
{
  "id": "proj-项目名-v1",
  "project_name": "项目名",
  "domain": "领域",
  "quality_score": 0.85,
  "quality_dimensions": {
    "claim_validation": 0.95,
    ...
  },
  "user_feedback": "原文引用",
  "feedback_signal": "正面明确"
}
```

### 规则

1. 每条数据必须源自真实用户反馈，不得虚构或推测
2. 未反馈的维度不要赋0分——在训练数据中该维度标记为 null，evaluator 中跳过
3. 负样本需要成对出现（v1 不满意 + 修改后 v2 满意）
4. 自评记录只在数据层面跨项目聚合，不跨项目分析具体内容

## Verification

- [ ] 从用户对话中提取了至少 3 个满意度信号
- [ ] 生成了 10 维自评分（含未反馈维度的 null 标记）
- [ ] 自评记录已写入项目文件夹的 `用户反馈与自评记录.md`
- [ ] 训练数据已追加到 `skillopt-integration/data/deep_tech_dd/`
- [ ] 已检查累计数据量是否 ≥ 20 条 → 提示触发重训练
