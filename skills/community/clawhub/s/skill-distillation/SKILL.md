---
name: skill-distillation
displayName: skill-distillation
version: 1.0.0
description: Skill蒸馏 — 从大模型/人类专家/书本中提取可复用Agent技能的方法论与工具链
compatibility: opencode
trigger: user mentions skill distillation, skill extraction, knowledge distillation, skill alchemy, nuwa, cangjie
tags: [skill-distillation, agent-skills, knowledge-distillation, ai-agent]
---

# Skill蒸馏

将知识从大模型/人类专家/方法论/书本中提取为可复用的 Agent Skill。

## 核心结构

Skill = (C, π, T, R)
- **C** (Condition): 适用条件，语义匹配
- **π** (Policy): 执行策略，操作步骤
- **T** (Termination): 终止条件
- **R** (Reusable Interface): 可复用接口

## 蒸馏精度三级

| 层级 | 内容 | 可蒸馏性 |
|------|------|---------|
| **L1** | 精确规则 + 陈述性知识 | ✅ 完美蒸馏 |
| **L1.5** | 扩散激活 + 范例 | ⚠️ 方向正确但边界受限 |
| **L2** | Utility 判断权重系统 | ❌ 不可用语言编码 |

## 代表项目

### SkillAlchemy
- 蒸馏人/方法论/已有 Skill
- 3 种 depth: quick (~5min) / standard (~15min) / deep (~30min)
- GitHub: https://github.com/agentsope/SkillAlchemy

### Nuwa-Skill
- 蒸馏人物思维方式（13人物+1主题）
- 六路并行采集 → 三重验证提炼 → 质量验证
- GitHub: https://github.com/alchaincyf/nuwa-skill

### Cangjie-Skill
- 蒸馏书为可执行 Skill（RIA-TV++ 流水线）
- 支持巴菲特、毛泽东选集、黄帝内经等
- GitHub: https://github.com/kangarooking/cangjie-skill

## 使用方式

```bash
# 安装 SkillAlchemy 蒸馏的技能
npx skills add agentsope/SkillAlchemy/skills/<skill-name>

# 安装 Nuwa 蒸馏的人物技能
npx skills add alchaincyf/nuwa-skill

# 安装 Cangjie 蒸馏的书籍技能
npx skills add kangarooking/cangjie-skill
```

## 关键洞察

- Comprehensive skill（面面俱到）比 Detailed skill（聚焦具体）效果更差 (-2.9% vs +18.8%)
- 2-3 个 skill 协同效果最好 (+18.6%)，4 个以上降至 +5.9%
- 约 80% 的日常工作时间可被 skill 覆盖，但只创造 ~30-40% 的价值
- Skill 形式为自然语言，LLM 带宽有限 — L2 Utility 强行展开成语言只会造成混乱
