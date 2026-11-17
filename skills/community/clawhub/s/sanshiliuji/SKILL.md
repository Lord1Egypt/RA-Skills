---
name: stratagem
description: >-
  Thirty-Six Stratagems (三十六计) strategic analysis — game theory, systems thinking,
  cognitive psychology, and Sun Tzu principles applied to competitive scenarios. Use
  when the user asks about any of the 36 stratagems by name (CN or EN), invokes
  /stratagem or /36计, discusses 战略/策略/博弈/商战/competitive strategy/business
  warfare, or presents a competitive scenario asking "怎么办" / "how should I deal
  with". Auto-adjusts from quick stratagem lookup to full 7-dimension analysis.
version: 1.0.0
license: MIT
user-invocable: true
tags:
  - strategy
  - game-theory
  - business
  - competitive-analysis
  - chinese-classics
  - sun-tzu
  - military-strategy
  - negotiation
  - systems-thinking
  - cognitive-psychology
  - decision-making
  - leadership
---

# 三十六计 Strategic Analysis Skill

> 以世界顶级思维框架重构三十六计——博弈论、系统论、认知心理学、孙子兵法、现代竞争战略的深度融合。

## Quick Start

```
/stratagem 我们公司被巨头挤压，该怎么办？
/stratagem 什么是围魏救赵？
/stratagem How should I compete against Amazon?
```

Just describe your situation — the skill auto-detects complexity and responds at the right depth. No need to name a stratagem; the framework will find the right one.

## Depth Routing (READ FIRST)

该技能以三层深度运行。在开始任何分析之前先确定深度级别。

### Level 1: Quick Lookup (快速查询)

**触发条件**：用户询问"什么是[计策]""[计策]是什么意思""tell me about stratagem #N"或任何单计策定义查询。
**信号**：没有场景上下文，没有问题需要解决，仅信息查询。
**响应**：计策名（中英）、章节、原文、2-3句释义、一个现代应用案例。150-300词。
**文件加载**：只读 `references/catalog.md` 中的相关计策条目。不加载 `references/framework.md`。

### Level 2: Focused Application (聚焦应用)

**触发条件**：用户将1-2个具体计策应用到具体场景中，例如"如何用声东击西做薪资谈判？"或带有明确计策引用的简短场景。
**信号**：用户点名计策 + 提供上下文，但上下文限于单个领域/互动。
**响应**：2-3个分析维度简要应用、具体战术步骤、注意事项。300-600词。
**文件加载**：只读 `references/catalog.md` 中的相关计策条目。可选读 `references/framework.md` 中相关的单一维度。

### Level 3: Full Strategic Analysis (完整战略分析)

**触发条件**：多实体丰富场景（公司、竞争对手、市场动态）、战略困境语言（"该怎么办""how should I approach""what's our strategy"）、未点名具体计策、复杂竞争或博弈情境。
**信号**：100+字符描述，涉及多个参与者、利害关系、约束条件或时间动态。
**响应**：完整七维分析 + 计策选择与排序 + 实施路线图 + 风险评估。1000-2500+词。
**文件加载**：完整读取 `references/catalog.md` 和 `references/framework.md`。可选读 `references/depth-routing.md` 校准分析深度。

### 歧义消解

当无法确定 Level 2 还是 Level 3 时：
- 默认选择 Level 2
- 在回复末尾附加：**"需要将此展开为完整的七维战略分析吗？"**
- 用户确认后升级到 Level 3

---

## Workflow

### Step 1: 语言检测
检测输入是中文、英文还是混合。用与查询相同的语言回复。混合输入时，以用户的主要语言为准。

### Step 2: 深度分类
应用上述三级标准 + 参考 `references/depth-routing.md`（仅在需要详细评分矩阵时加载）将查询分类为 Level 1、2 或 3。

### Step 3: 按选定深度加载参考文件
- Level 1: 仅 `references/catalog.md` 中相关条目
- Level 2: `references/catalog.md` 中相关条目 + `references/framework.md` 中相关维度
- Level 3: 完整 `references/catalog.md` + `references/framework.md` + 可选 `references/depth-routing.md`

### Step 4: 按深度输出

---

## Level 1 输出模板：Quick Lookup

```
**[序号]. [中文名] — [英文名]**
**所属篇章**: [六章之一]
**原文**: [文言原文]
**释义**: [2-3句白话解释]
**核心机制**: [一句话概括运作原理]
**现代应用**: [一个具体的现代场景案例]
**关键条件**: [使用此计的前提]
```

---

## Level 2 输出模板：Focused Application

```
## 情境分析 / Situation Analysis
[1-2句概括用户场景和核心矛盾]

## 策略应用 / Strategy Application
[选定的计策] — [为什么此计适用于此场景]
[如有必要，增加第二个计策]

### 核心逻辑
[从博弈论/认知心理学/系统思维中选取最相关的1-2个维度简要分析]

## 具体步骤 / Concrete Steps
1. [第一步 — 具体可执行]
2. [第二步]
3. [第三步]
4. [可选：第四步]
5. [可选：第五步]

## 注意事项 / Caveats
- [关键前提条件]
- [可能的风险]
- [何时应停止/调整]

---

> 需要将此展开为完整的七维战略分析吗？
```

---

## Level 3 输出模板：Full Strategic Analysis

```
## 一、局势研判 / Situation Assessment
[全面剖析当前局势：参与者、利害关系、力量对比、时间维度、关键不确定性]

## 二、七维框架分析 / Seven-Framework Analysis

### 1. 博弈论视角 / Game Theory
[信息结构、博弈类型（一次/重复）、承诺可信度、行动顺序、均衡分析]

### 2. 系统思维 / Systems Thinking
[系统要素、反馈回路、杠杆点识别、干预深度建议]

### 3. 认知心理学 / Cognitive Psychology
[对手决策者的认知偏误、情绪状态、注意力焦点、可利用的心理漏洞]

### 4. 孙子兵法元原则 / Sun Tzu Meta-Principles
[诡道应用、"不战而屈人之兵"的途径、知己知彼的差距、主动权归属]

### 5. 现代竞争战略 / Modern Competitive Strategy
[波特五力、蓝海/OODA/颠覆式/柔道框架中最适用的一种深入分析]

### 6. 四层深度模型 / Four-Layer Depth Model
[当前策略停留在哪一层？应上升到哪一层？给出跨层组合方案]

### 7. 七种元思维范式 / Seven Meta-Thinking Paradigms
[非线性、反直觉、涌现、借力、不对称、时序、灰度 — 选最适用的2-3种]

## 三、计策匹配 / Stratagem Matching

### 首选计策：**[计策名]** (主攻方向)
- **匹配理由**: [为什么此计是首选]
- **应用方案**: [如何实施]

### 次选计策：**[计策名]** (辅助/掩护)
- **匹配理由**: [为什么配合此计]
- **应用方案**: [如何配合首选计策]

### 备选计策：**[计策名]** (应变为)
- **触发条件**: [何时启用备选]

### 计策时序链
阶段一（近期）→ [计策A] → 预期效果：[...]
阶段二（中期）→ [计策B] → 预期效果：[...]
阶段三（远期）→ [计策C] → 预期效果：[...]

## 四、实施路线图 / Implementation Roadmap
| 阶段 | 行动 | 关键里程碑 | 所需资源 | 时间窗口 |
|------|------|-----------|---------|---------|
| 近期 | [...] | [...] | [...] | [...] |
| 中期 | [...] | [...] | [...] | [...] |
| 远期 | [...] | [...] | [...] | [...] |

## 五、风险评估与对策 / Risk Assessment & Mitigation
1. **风险**: [最大风险] → **对策**: [如何应对]
2. **风险**: [第二风险] → **对策**: [如何应对]
3. **风险**: [黑天鹅] → **对策**: [韧性方案]

## 六、总结建议 / Summary Recommendation
[一句话核心建议]
[三个关键词概括策略本质]
```

---

## 计策选择逻辑 / Stratagem Selection Logic

在选择计策时（Level 2 和 3），按以下逻辑进行：

1. **场景映射**：将场景动态映射到六大章节——优势局(胜战计)、对峙局(敌战计)、进攻局(攻战计)、混乱局(混战计)、兼并局(并战计)、劣势局(败战计)
2. **时序排序**：确定计策的应用顺序（哪个先、哪个后）
3. **冲突检测**：确保计策之间不相互矛盾（如不要同时用打草惊蛇和瞒天过海，除非有明确的前后次序）
4. **优先级排列**：按匹配度排序（首选、次选、备选）

### 场景 → 篇章快速映射

| 你的处境 | 对应篇章 | 核心思路 |
|---------|---------|---------|
| 你占据绝对优势 | 胜战计 (1-6) | 利用优势碾压，防止对手翻盘 |
| 你与对手旗鼓相当 | 敌战计 (7-12) | 在均势中制造不对称 |
| 你需要主动进攻 | 攻战计 (13-18) | 以攻势掌握主动权 |
| 局势混乱多边博弈 | 混战计 (19-24) | 在混乱中浑水摸鱼 |
| 你在蚕食/渗透阶段 | 并战计 (25-30) | 渐进式扩大控制 |
| 你处于明显劣势 | 败战计 (31-36) | 保存实力，以奇制胜 |

---

## 参考文件加载指南 / Reference Loading Guidelines

| 文件 | Level 1 | Level 2 | Level 3 |
|------|---------|---------|---------|
| `references/catalog.md` | 仅相关条目 | 相关条目 | 完整加载 |
| `references/framework.md` | 不加载 | 仅相关维度 | 完整加载 |
| `references/depth-routing.md` | 不加载 | 不加载 | 可选加载 |

### 重要

- Level 1 绝不加载 framework.md — 这是对简单查询的 token 浪费
- Level 2 只加载 framework.md 中与场景最相关的 1-2 个维度
- Level 3 加载全部 — 完整分析需要所有维度的交叉比对
- depth-routing.md 仅在 Level 3 需要精细校准或 Level 2/3 边界歧义时加载

---

## 语言与语调 / Language and Tone

### 中文回复
- 使用专业战略语言，保持可读性
- 文言原文使用引述格式
- 古典成语与现代术语灵活混用
- 输出简洁有力，避免空洞套话

### English replies
- Use professional business/strategic English
- Preserve Chinese stratagem names with parenthetical English translations
- Keep analytical tone but ensure accessibility
- Be concrete, avoid vague generalities

### 通用规则
- 不混合中英文在同一个句子中
- 计策名始终保留中文原名 + 英文翻译
- 引用原文时使用原文语言 + 白话解释
