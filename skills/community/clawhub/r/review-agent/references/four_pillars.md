# Four-Pillar Review Framework (v0, replaces 7-axis as primary)

> 适用**任意场景**：决策 brief / 状态汇报 / 设计 review / 1:1 议程 / 投资 memo / 方向讨论 / 其他。
>
> 每个 review session 都按这四柱检查——柱比轴粗但泛化好。某一柱下的细分问题由 **Responder Simulation** 层按 Responder profile 动态生成，不再固化为 7 条轴。

## 先记住一条 — Agent 是挑刺者，不是总结者

详见 `agent_persona.md` 的"核心原则"。简版：
- 只指出问题、只追问，不替 Requester 写答案
- 六个标准挑战维度（数据完整性 / 逻辑自洽性 / 方案可行性 / 利益相关方 / 风险评估 / ROI 清晰度）横跨所有场景
- 四柱是"去哪挑"，六维度是"怎么挑"，Responder 模拟是"以他的口气挑"

---

## Pillar 1: 背景 (Background)

"让 {responder} 不用问'这是咋回事'"

### Pass 标准
- 讲清了：什么事在发生 / 为什么是现在 / 当前状态 / 谁在 care
- {responder} 进会议能直接进入讨论，不用先听故事

### Fail signals
- 开头直接跳到选项或请求，没讲上下文
- "As discussed" / "我们都知道" 却并没有明确过
- 只讲 what 不讲 why now / why this way

### Severity 默认
- **IMPROVEMENT**——大部分情况
- **BLOCKER**——{responder} 没这个背景就无法决策（如他没参与过前情）

### 发给 Requester 的常见追问
- 这件事的来源 / 起点是什么？
- 为什么是这个时间点提出来？
- 之前尝试过什么？结果如何？

---

## Pillar 2: 资料 (Materials)

"让 {responder} 最可能追问的 top-3 问题都已有答案"

### Pass 标准
- 决策依据齐：数据（带来源+日期）、可比对象、相关案例
- 内部视角 + 外部锚点都在
- 核心数字经得起"这个从哪来"的追问

### Fail signals
- 数据没来源 / 没日期 / 只是观点陈述（"准确率更好"）
- 只有内部看法或只有市场说法（半盲）
- 关键 data point 缺失（如"我们当前用量"没说）

### Severity 默认
- **IMPROVEMENT**——数据不全但决策不依赖
- **BLOCKER**——某个缺失的 data 直接让决策无意义

### 发给 Requester 的常见追问
- 这个数字出自哪里？什么时候测的？
- 你做过对比吗？同类产品的基线是什么？
- 如果关键假设被推翻（X 明天降价/涨价/消失），材料里还站得住吗？

### 场景覆盖（内部 sub-categories）
决策 brief 场景下，本柱应包含「证据新鲜度」「红队反方立场」「stakeholder 真实声音」三个子检查——这些作为 LLM 扫描时的 reference，不对用户明说。

---

## Pillar 3: 框架 (Framework)

"让 {responder} 看完就知道讨论的变量和判断类型"

### Pass 标准
- 讨论要对齐的是什么：选项之间比较的维度（cost / speed / reliability / team fit）
- 要做的判断类型：二元 yes/no？A/B 选择？range 选择？nuanced advice？
- 如果是要选项，选项的比较维度和权重明确

### Fail signals
- "讨论 X" 但没说讨论 X 的哪个维度
- 多个选项罗列但没说按什么标准比
- 把 Responder 置于"你觉得呢"的开放场景——没提供他该如何切入的框架

### Severity 默认
- **IMPROVEMENT**——大部分时候
- **BLOCKER**——讨论方向完全开放，会议会沦为 brainstorm

### 发给 Requester 的常见追问
- 这几个选项你想按什么维度比较？
- {responder} 需要给的是哪种形式的答复（批准/选择/建议/反馈）？
- 如果他给的答复和你预期不一样，你怎么办？

---

## Pillar 4: 意图 (Intent) — **CSW GATE**

"让 {responder} 看完就知道开完会后他要做什么具体的事"

### Pass 标准
- 明确的单一 ask：批准 / 否决 / 选 A vs B / 给某方向反馈 / 审批预算
- Requester 已经把所有"只要他自己能做的"功课都做完了
- Boss 下一步动作 ≤ 1 个（签字/选/给一句反馈）

### Fail signals（全部 BLOCKER）
- "想讨论一下 X" / "找你聊聊" / "听听你的看法"——无具体动作
- "帮我看看该怎么办"——把决策推回 Responder
- 文末反问 Responder 一堆问题（违反 no-boss-burden）
- "我再梳理一下""再研究一下"——用分析掩盖"我没想好 ask"

### Severity
- **ALWAYS BLOCKER**——这是整个 review 的 gate。本柱 fail → session 不能 close → 材料不能送 Responder

### 发给 Requester 的常见追问
- 你希望 {responder} 做的具体动作是哪一个？（批准 X / 选 A 或 B / 给某方向反馈）
- 如果 {responder} 读完直接回一句话，你最理想的那句是什么？
- 这个 ask 是否是你**真的需要他**才能推进的，还是你自己其实能决？

---

# Top Layer: Responder Simulation

## 机制

四柱扫描跑完后，另起一次 LLM 调用，让模型**扮演 {responder} 本人**：
- 读入：{responder} 的 profile.md（pet peeves、决策风格、always-ask 问题）+ 本次 normalized.md
- Prompt: "你是 {responder_name}。按你的 profile 和你平时的思考方式，读完这份材料，你**前 5 个最关心的问题**是什么？按你自己的 priority 排，1 最要紧。"

对每个模拟问题：
- 检查 normalized.md 是否已经回答
- 没答 → emit finding（source=`responder_simulation`，severity 默认 IMPROVEMENT；若问题涉及意图/基本信息缺失 → BLOCKER）

## 为什么要这一层

四柱是**通用架构**。同一柱下，不同 Responder 的具体 pain point 很不同：
- 一位创始人视角的 Responder 看任何用户面向项目会追问 "过去 14 天和 ≥3 个真实用户聊过吗"（来自他 profile.md 里明确写的 pet peeve）
- 另一个做融资的 partner 看同样东西会问 "TAM 和同类 comps 的估值倍数对比是啥"
- 模拟层让标准自动适配到**这个人**

## 和四柱的关系

四柱 = safety net（baseline，任何场景都要过）
模拟 = depth layer（给这个特定 Responder 的额外问题）

两者产的 findings 合并到 `annotations.jsonl`，用 `source` 字段区分。final-gate 和 summary 按 pillar 分组显示。

## 限制

- 每次 scan 多一次 LLM call（成本 +50%）
- 非确定：同一材料两次跑可能出不同问题——作为 feature 看：模拟 Responder 的真实思考也不是每次完全一样
- 可能幻觉——mitigation：只 emit profile 里有明确依据的问题

---

# 对 Q&A emission 风格的影响

四柱不像七轴那样整齐对应 direct/Socratic，映射规则：

| 柱 + severity | 风格 |
|---|---|
| Pillar 4 (Intent) BLOCKER | **直接**："把 ask 改成 '请 {responder} 在 3-30 前批准预算 X'" |
| Pillar 1 (Background) BLOCKER | **直接**："加一段 5 句话的背景" |
| Pillar 2 (Materials) | **Socratic**："如果当前月调用是 100 vs 10000，你的选择会变吗？走给我看下分析。" |
| Pillar 3 (Framework) | **Socratic**："你想让 {responder} 按哪个维度选？cost? speed? team fit?" |
| Responder Simulation findings | **Socratic**（它们本来就是问题形态） |
| 任何 NICE-TO-HAVE | 只在本轮 findings < 3 条时发；否则入 annotations.jsonl 不打扰 |

---

# 和旧七轴的关系

原七轴（Ask Clarity / Completeness / Evidence / Assumptions / Red Team / Stakeholder / Decision Readiness）**保留为内部 sub-reference**（见 `axes_decision_brief_reference.md`），给 LLM 在决策 brief 场景下扫描时作 checklist 参考。但用户可见和 summary 分组**都按四柱走**。

简单说：七轴沉入 Pillar 2/3/4 的 sub-questions，不再作为 first-class axes。
