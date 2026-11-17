# 方法核心 V1.0 — 策划思维模型正式定义

> **方法模型**：九才策划思维模型 V0.3.2-Frozen
> **Provenance 体系**：四轴标注（ORIGIN × ENDORSEMENT × EVIDENCE-BASIS × VALIDATION-MATURITY），依据 00号 V1.1.1-Frozen provenance-v3 规范
> **本文档性质**：方法核心定义，供 Skill 运行时按需查阅。不替代 SKILL.md 中的执行规则。

---

## 1. A 层：核心策划原则

> A 层 = 用户明确拥有/确认的策划原则。具体 Runtime 执行强度按条目定义（见下文各条目）。

### A1：从结果出发，逆向推导

| 字段 | 内容 |
|------|------|
| 原则 | 从结果出发，逆向推导 |
| ORIGIN | USER-ORIGINAL |
| ENDORSEMENT | USER-CONFIRMED |
| EVIDENCE-BASIS | USER-STATEMENT |
| VALIDATION-MATURITY | CROSS-CASE-PRELIMINARY（Case 01/02/03 均 SUPPORT，无已知反例；未经过专门强度判断，不自动标为 STRONG） |
| 执行强度 | 核心方向原则 |
| 在产品中的角色 | **核心方向**——所有分析从"做成了是什么样"开始 |
| 执行方式 | ① 先确认/引导结果定义 ② 从结果逆推必要条件 ③ 从条件逆推问题 ④ 从问题逆推路径 |
| 执行原则 | Skill 必须知道当前在为什么结果策划（可以是暂定的、外部给定的或待验证的）。不跳过结果确认直接给方案 |

**证据详情**：
- 用户原话："帮助他从结果出发，分析目标、问题、条件、资源、路径、策略和执行"
- 上游作者确认：用户本人在 WorkBuddy 对话中首发，无 AI 介入痕迹
- 特殊处理：Case 03 变体——结果不由用户定义时（甲方/外部定义），当结果由甲方/外部给定时，识别外部结果框架与约束，并在该框架内定义和设计解决方案
- 支持案例：Case 01（思维导图从结果出发）、Case 02（短剧从最终形态倒推）、Case 03（甲方定义结果框架，用户在框架内定义和设计解决方案）

---

### A2：结果尽可能具象、可观察、可验证

| 字段 | 内容 |
|------|------|
| 原则 | 结果尽可能具象、可观察、可验证 |
| ORIGIN | AI-AUTHORED |
| ENDORSEMENT | USER-MODIFIED-AND-ADOPTED |
| 历史说明 | AI-TOPIC → USER-CORRECTED：AI 引入"目标必须带数字"话题，用户纠正为"结果尽可能具象、可观察、可验证" |
| EVIDENCE-BASIS | AI-INFERENCE + USER-STATEMENT |
| VALIDATION-MATURITY | CROSS-CASE-PRELIMINARY（Case 01/02 SUPPORT，Case 03 NOT-OBSERVED，无反例） |
| 执行强度 | 核心结果质量原则，但不阻塞流程 |
| 在产品中的角色 | **结果质量要求**——引导结果尽可能具象可验证，但不因"不够完美"阻塞流程 |
| 执行方式 | ① 用户能说出具象结果 → 确认并记录 ② 用户只有模糊想法 → 追问"能说说做成了是什么状态吗" ③ 模糊表述 → 如果歧义会显著改变路径，继续引导 |
| 执行原则 | 如果结果歧义会显著改变路径 → 追问；如果用户不知道 → 给出暂定结果/候选解释，标注 [假设] 后继续；如果已有信息足以支持下一步判断 → 继续 |
| 特殊处理 | 数字是有效方式之一但不是唯一方式。判断标准：能不能明确说出"这件事做成了没有"。Case 03 中甲方需求是方向性的——NOT-OBSERVED ≠ 反例，可能是委托项目中用户无权要求甲方量化 |

**证据详情**：
- AI 原始提案："目标必须带数字"（AI 从思维导图三个定价场景推断）
- 用户纠正原话："'目标必须带数字'不要绝对化。真正原则应该是：结果必须尽可能具象、可观察、可验证。"
- 不是简单附和的理由：用户说"真正原则应该是……"——主动声称自己的原则，内容比 AI 提案更抽象、更通用

---

### A7：资源不足处理优先级链

| 字段 | 内容 |
|------|------|
| 原则 | 资源不足时：补→借→换→换路径→改模型→最后才考虑调整目标 |
| ORIGIN | AI-AUTHORED |
| ENDORSEMENT | USER-MODIFIED-AND-ADOPTED |
| 历史说明 | AI-TOPIC → USER-CORRECTED：AI 提出"资源不够→降目标"，用户纠正为完整的优先级链 |
| EVIDENCE-BASIS | AI-INFERENCE + USER-STATEMENT |
| VALIDATION-MATURITY | SINGLE-CASE（Case 01 SUPPORT，Case 02 COUNTEREXAMPLE，Case 03 NOT-OBSERVED） |
| 执行强度 | 强默认参考 / 可跳级 / 可 override（存在已知反例） |
| 在产品中的角色 | **默认处理顺序，存在已知反例，可 override** |

**证据详情**：
- AI 原始提案："资源不够→降目标"
- 用户纠正原话："'资源不够→降目标'不能作为默认逻辑。更完整的判断应该是：补资源/借资源/换资源/换路径/改模型→最后才考虑调整目标。"
- 已知反例：Case 02 中用户直接跳过"补/借/换"到达"换路径"——证明不是绝对线性

#### A7 产品执行方式

A7 不设计为绝对线性流程。设计为**默认优先级参考 + 允许跳级 + override 规则统一**：

```
发现资源缺口
├─ 默认参考顺序（可跳级）：
│   ① 补资源（找新来源）
│   ② 借资源（合作/外包/交换）
│   ③ 换资源（不同组合达到类似效果）
│   ④ 换路径（不同方法达到同样结果）
│   ⑤ 改模型（改变商业模式降低资源需求）
│   └─ ⑥ 调整目标（默认最后考虑）
│
├─ 允许跳级的条件：
│   某一级明显不可行时，直接跳到下一级
│   用户已有明确偏好时，尊重用户选择
│   项目类型使某一级不适用时（如创意项目中"降质量"=换资源，不是调目标）
│
└─ override 规则（统一）：
    "调整目标"默认最后考虑。
    但以下情况可以 override：
    ① 用户明确决定调整目标
    ② 现实条件发生根本变化
    ③ 继续维持原目标明显不合理
    Skill 必须说明调整目标的原因和代价，但不能阻止用户选择。
```

**与 C2 的关系**：C2 假设"资源链是否适用于所有项目类型"。在产品中，C2 的结论已体现在 A7 的"允许跳级"设计中——不强制逐级执行。C2 作为假设记录存在，不进入工作流。

---

## 2. A 层 Provenance 摘要

| 编号 | 内容 | ORIGIN | ENDORSEMENT | EVIDENCE-BASIS | VALIDATION-MATURITY |
|------|------|--------|-------------|----------------|---------------------|
| A1 | 从结果出发逆向推导 | USER-ORIGINAL | USER-CONFIRMED | USER-STATEMENT | CROSS-CASE-PRELIMINARY |
| A2 | 结果尽可能具象可观察可验证 | AI-AUTHORED | USER-MODIFIED-AND-ADOPTED | AI-INFERENCE + USER-STATEMENT | CROSS-CASE-PRELIMINARY |
| A7 | 资源优先级链 | AI-AUTHORED | USER-MODIFIED-AND-ADOPTED | AI-INFERENCE + USER-STATEMENT | SINGLE-CASE |

**摘要表述规则**：A1/A2/A7 统称"用户明确拥有/确认的策划原则"，不得统称"3 条 USER-ORIGINAL"——A2/A7 的 ORIGIN 为 AI-AUTHORED，ENDORSEMENT 为 USER-MODIFIED-AND-ADOPTED。

---

## 3. C1：七维思考框架

| 字段 | 内容 |
|------|------|
| 假设 | 七维思考（结果/条件/问题/资源/路径/策略/执行）的维度划分是否完整 |
| ORIGIN | AI-AUTHORED |
| ENDORSEMENT | USER-ACKNOWLEDGED |
| EVIDENCE-BASIS | USER-STATEMENT + AI-INFERENCE |
| VALIDATION-MATURITY | SINGLE-CASE（Case 02 部分验证） |
| 产品角色 | **内部默认导航框架，不是用户可见的问卷** |
| 执行强度 | [默认启发式，可 override] |

**证据详情**：
- 用户提供七个维度：用户在原始描述中列出了七个维度的原始表述（结果/条件/问题/资源/路径/策略/执行）。维度内容来自用户，EVIDENCE-BASIS 含 USER-STATEMENT
- AI 结构化为 C1 框架：AI 将用户描述的维度结构化为导航框架，并提出"七维划分是否完整"的假设。框架结构和完整性假设是 AI 的贡献，ORIGIN=AI-AUTHORED
- 用户对框架的态度：用户提供了维度但未对框架结构/完整性假设给出强确认信号，ENDORSEMENT=USER-ACKNOWLEDGED

### 七维内部使用方式

| 维度 | 内部检查问题 | 何时出现 | 何时可略过 |
|------|------------|---------|-----------|
| 结果 | 成功长什么样？ | 通常出现 | 用户已有明确结果定义时 |
| 问题 | 什么挡在路上？ | 通常出现 | 已由其他维度隐含覆盖时 |
| 路径 | 怎么走？ | 通常出现 | 只有一条可行路径时 |
| 执行 | 第一步做什么？ | 通常出现 | 方案输出阶段自然包含时 |
| 条件 | 什么必须成立？ | 需要显性化时 | 已隐含在结果定义中 |
| 资源 | 有什么？缺什么？ | 是约束时 | 充足或非关键因素 |
| 策略 | 选哪个？为什么？ | 存在路径选择时 | 只有一条路径 |

### 哪些可以从用户已有材料直接获得

- 用户提供文档/方案 → 条件、资源、路径可能已有
- 用户一句话但信息完整 → 结果、条件、路径可能已有

### 哪些才值得追问

- 结果歧义会显著改变路径 → 追问（最高优先级）
- 信息矛盾 → 追问
- 关键歧义会影响方案方向 → 追问
- 其他 → 不追问，在方案中标注"[需确认]"

> **四项闭环来源说明**：上表中"通常出现"的四个维度（结果/问题/路径/执行）对应动态输出的四项必选项，但这是 D5/Runtime Rule 的要求，不是 C1 的硬约束权力。即使不调用 C1，也必须产生四项闭环。C1 本身可被 override。

---

## 4. D 层：产品/交互规则

> V0.3.2-Frozen D 层正式条目：D1、D2、D4、D5、D6。共 5 条。不存在 D3。
> VALIDATION-MATURITY 说明：D 层规则尚未通过 01号 Runtime 验证，标注 UNVALIDATED。但其用户确认身份与执行地位由 ORIGIN/ENDORSEMENT 和产品规则决定，不因 UNVALIDATED 自动降级。

| 编号 | 规则 | ORIGIN | ENDORSEMENT | EVIDENCE-BASIS | VALIDATION-MATURITY | 内容 |
|------|------|--------|-------------|----------------|---------------------|------|
| D1 | 自适应混合式交互 | USER-ORIGINAL | USER-CONFIRMED | USER-STATEMENT | UNVALIDATED | 根据信息成熟度选择交互模式（引导式/补缺口式/直接分析式）。不强迫填问卷 |
| D2 | 每轮最多1-3个问题 | USER-ORIGINAL | USER-CONFIRMED | USER-STATEMENT | UNVALIDATED | 每轮最多只问1-3个真正关键的问题。每个问题只问一件事 |
| D4 | 回溯机制 | USER-ORIGINAL | USER-CONFIRMED | USER-STATEMENT | UNVALIDATED | 允许返回前面的节点重新推演。回溯时只回到受影响的部分，不从头开始 |
| D5 | 动态输出结构 | USER-ORIGINAL | USER-CONFIRMED | USER-STATEMENT | UNVALIDATED | 输出结构根据项目实际情况动态组合。不是固定八段式 |
| D6 | 不编造信息 | USER-ORIGINAL | USER-CONFIRMED | USER-STATEMENT | UNVALIDATED | 未经验证的判断标注[假设]，缺失信息标注[需确认]，不假装知道用户没提供的信息 |

### D 层用户原话

- D1: "交互方式我选择 C，但我想把它进一步定义成：自适应混合式"
- D2: "每轮最多只问1-3个真正关键的问题"
- D4: "允许返回前面的节点重新推演"
- D5: "输出结构改为动态结构"、"根据项目实际情况动态组合章节"
- D6: 用户多次明确要求不编造信息

---

## 5. G 层：模型治理原则

> V0.3.2-Frozen G 层。4 条全部为 USER-ORIGINAL, USER-CONFIRMED。
> VALIDATION-MATURITY 说明：G 层规则尚未通过 01号 Runtime 验证，标注 UNVALIDATED。但其用户确认身份与执行地位由 ORIGIN/ENDORSEMENT 和产品规则决定，不因 UNVALIDATED 自动降级。

| 编号 | 治理原则 | ORIGIN | ENDORSEMENT | EVIDENCE-BASIS | VALIDATION-MATURITY | 内容 |
|------|---------|--------|-------------|----------------|---------------------|------|
| G1 | 不过早定型方法 | USER-ORIGINAL | USER-CONFIRMED | USER-STATEMENT | UNVALIDATED | 方法和模型需要经过案例交叉验证后才能固化。标注当前版本号和证据状态 |
| G2 | 证据等级 → 执行强度 | USER-ORIGINAL | USER-CONFIRMED | USER-STATEMENT | UNVALIDATED | 规则的执行强度不能高于它的证据等级。A层按条目定义执行强度，C层=默认启发式（可override），P层=产品假设（待验证） |
| G3 | 方法迭代机制 | USER-ORIGINAL | USER-CONFIRMED | USER-STATEMENT | UNVALIDATED | 通过新案例验证/推翻/修正现有假设，实现方法迭代 |
| G4 | 事实与假设分离 | USER-ORIGINAL | USER-CONFIRMED | USER-STATEMENT | UNVALIDATED | C 层假设不得出现在硬约束位置。如果工作流中必须使用，标注"[默认启发式，可 override]" |

### G 层用户原话

- G1: "先不要把你刚才提炼的'七步逆向策划'直接固化为最终方法论"
- G2: "规则的执行强度不能高于它的证据等级"
- G3: 用户描述了提供案例交叉验证的迭代过程
- G4: 用户多次要求区分事实和假设

---

## 6. Frozen 版本信息

- **当前有效模型版本**：V0.3.2-Frozen
- **Frozen B 层**：B1-B12（12条）。B13/B14 属于 Case 03 观察池，不计入 Frozen
- **Frozen D 层**：D1/D2/D4/D5/D6（5条，无 D3）
- **Frozen C 层**：17条（C4/C18已合并，C14已移入个人特质观察，C15已改写）
- **个人特质观察**：PT1（不进入 Skill 核心方法）
- **P 层**：P1/P2/P3（3条，全部 AI-AUTHORED，待 runtime 验证）
