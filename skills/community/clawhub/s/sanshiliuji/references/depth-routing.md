# 深度分派决策表 / Depth Routing Decision Matrix

## 快速评分启发式 / Quick Scoring Heuristic

| 信号 / Signal | 权重 | Level 1 指向 | Level 2 指向 | Level 3 指向 |
|-------------|------|-------------|-------------|-------------|
| 查询长度 | 中 | <30 字 | 30-150 字 | >150 字 |
| 提及的实体数（公司/人/组织） | 高 | 0-1 | 1-2 | 3+ |
| 包含"怎么办"/"how should"/"strategy for" | 高 | 否 | 可能 | 是 |
| 具体计策名被提及 | 高 | 是（释义型） | 是（应用型） | 否 |
| 描述了竞争动态 | 高 | 否 | 否 | 是 |
| 包含时间压力/高利害标记 | 中 | 否 | 可能 | 是 |
| 请求"分析"/"analyze" | 中 | 否 | 是 | 是 |
| 是"what is"/"什么是"型问题 | 极高 | 是 | 否 | 否 |

---

## 评分规则 / Scoring Rules

### Level 1 加分条件
- +3：查询长度 < 30字 AND 以"什么是/what is"开头 AND 提及具体计策名
- +1：请求计策列举（"三十六计有哪些""list all stratagems"）
- +1：查询只含一个计策名，没有上下文、没有场景、没有问题

### Level 2 加分条件
- +2：提及具体计策名 AND 提供了应用上下文（实体、场景、领域）
- +1：提及多个计策名（在查询中）
- +1：包含"分析"/"analyze" 但场景简单（单实体、单领域）

### Level 3 加分条件
- +2：查询长度 > 150字 AND 包含2+动态/困境标记
- +2：查询长度 > 300字 AND 包含3+实体
- +2：描述多实体竞争关系 AND 没有提及任何具体计策
- +1：包含时间压力标记（"即将""危机""窗口期"）

---

## 决策逻辑 / Decision Logic

```
if Level1_score >= 3 → Level 1 (Quick Lookup)
if Level3_score >= 3 → Level 3 (Full Strategic Analysis)
if Level2_score >= 2 AND Level3_score < 2 → Level 2 (Focused Application)
if 歧义 (Level2_score ~= Level3_score, 差距 <= 1) → Level 2 with escalation offer
```

---

## 歧义消解 / Ambiguity Resolution

当评分处于 Level 2 和 Level 3 之间时：
- 默认选择 **Level 2**
- 在回复末尾附加升级提示：
  > "需要我将此展开为完整的七维战略分析吗？(Would you like me to expand this into a full 7-dimension strategic analysis?)"
- 如果用户确认 → 升级到 Level 3
- 如果用户说"不用"或继续对话 → 保持 Level 2

---

## 边界案例参考 / Edge Case Reference

| 查询 | 分析 | 结论 | 理由 |
|------|------|------|------|
| `什么是围魏救赵？` | 7字, 计策名, "什么是" | **Level 1** | 纯定义查询 |
| `围魏救赵怎么用在商业谈判中？` | 14字, 计策名, 应用域 | **Level 2** | 计策名 + 领域 |
| `Tell me about stratagem 18` | 计策编号查询 | **Level 1** | 编号查含义 |
| `三十六计有哪些？` | 列举请求 | **Level 1** | 枚举型 |
| `如何用声东击西和暗度陈仓做市场推广？` | 多计策 + 应用域 | **Level 2** | 多计策应用 |
| `I want to use 趁火打劫 in my negotiation with a supplier` | 计策名 + 具体场景 | **Level 2** | 有场景上下文 |
| `我们初创公司被字节和腾讯挤压，市场份额从15%降到5%，怎么办？` | 多实体 + 困境 + 数据 + "怎么办" | **Level 3** | 多实体竞争困境 |
| `How should I compete against Amazon entering my niche?` | 竞争动态 + 困境 + 实体 | **Level 2→3** | 有场景但不够丰富，先给 Level 2 再升级 |
| `分析一下诺基亚vs苹果的竞争案例` | "分析" + 历史案例 | **Level 3** | 明确分析请求 |
| `中国新能源汽车行业竞争格局，小公司如何突围？` | 行业 + 竞争 + 困境 | **Level 3** | 复杂多实体场景 |
| `瞒天过海` | 仅计策名 | **Level 1** | 无上下文，可能是想了解含义 |
| `瞒天过海 怎么用` | 计策名 + "怎么用" | **Level 2** | 有应用意图 |

---

## 动态标记词表 / Dynamic Marker Keywords

### 中文
- 困境/决策类：怎么办、该如何、怎样应对、对策、方案、出路、破局
- 竞争类：竞争、对手、压制、蚕食、威胁、危机、市场份额、围剿
- 战略类：战略、策略、布局、谋划、博弈、分析
- 时间类：即将、马上、迫在眉睫、窗口期、长期、短期
- 规模/不对称类：巨头、大公司、小公司、初创、弱势、强势

### English
- Dilemma/decision: how should I, what should I do, how to deal with, strategy for, approach to
- Competition: compete, rival, competitor, threat, dominate, squeeze, market share
- Strategy: strategy, tactic, analyze, analysis, game theory, competitive
- Temporal: upcoming, imminent, window, long-term, short-term, crisis
- Scale/Asymmetry: giant, big company, small company, startup, underdog, dominant
