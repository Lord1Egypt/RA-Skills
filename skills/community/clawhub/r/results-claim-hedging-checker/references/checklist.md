# Diagnostic Checklist — Results Claim & Hedging Checker

本清单用于逐项扫描 Results 部分草稿，配合 `rubric.md` 的 1-5 分评分体系使用。**评分方向：5 分为最高（无问题），1 分为最低（严重问题 / 必须修改）**；某维度无问题即记 5 分。按顺序执行以下 6 个阶段，每个阶段的检查项标注了对应维度（D1-D5）和示例编号。

---

## 阶段 0：预扫描 — 确定设计类型

在逐句诊断前，先确认以下信息，以便 D3（因果语言）维度选择正确的判定基准。

- [ ] **C0-1** 研究设计类型是什么？
  - 随机对照实验 (RCT) → D3 可接受 "resulted in"
  - 准实验（无随机分配） → D3 仅接受 "was associated with"
  - 纵向观察 → D3 仅接受 "was related to / predicted"
  - 横断面相关 → D3 仅接受 "correlated with / was related to"
  - **未知** → D3 采用保守策略：任何强因果动词均标记 ≤ 2 分
- [ ] **C0-2** 全文语言是英文还是中文？（中文 Results 部分适用相关但不同的 hedging 惯例）

---

## 阶段 1：逐句扫描 — D1 Hedging

对每个句子检查以下项目。任一项目命中 → 按 `rubric.md` D1 评分。

### 1-A 检测缺失 hedging

- [ ] **D1-1** 句子是否对间接证据（中介、机制、观察性数据）直接断言而未加限定？
  - 命中 → 3 分（严重时降至 2 分）
  - 正面对照：F-05（"It appears to be the case … at least in part"）
- [ ] **D1-2** 句子是否使用了强动词描述非实验数据的结果？
  - 触发词：prove, demonstrate, establish, confirm
  - 命中 → ≤ 2 分
  - 正面对照：F-01（"showed signs of"）、F-07（"there was evidence of"）
- [ ] **D1-3** 句子是否在描述被试行为或情绪时用了因果性动词？
  - 如 "caused anxiety" / "proved that subjects were nervous"
  - 命中 → 2 分
  - 正面对照：F-01（"showed signs of nervousness"）

### 1-B 检测过度 hedging

- [ ] **D1-4** 句子是否在强实验设计（RCT）下仍使用多重 hedging？
  - 如 RCT 结果中写 "might possibly suggest a potential effect"
  - 命中 → 4 分（风格偏好，轻微）
- [ ] **D1-5** 句子是否对直接测量值（均值、频次）也加了不必要的 hedging？
  - 如 "the mean score appeared to be 3.45"
  - 命中 → 4 分（风格偏好，轻微）

### 1-C 检测混淆变量处理

- [ ] **D1-6** 当存在混淆变量时，是否主动声明不予采纳某解释？
  - 未声明 → 3 分
  - 正面对照：F-16（"this interpretation is not advanced because…"）

---

## 阶段 2：逐句扫描 — D2 Claim Strength vs. Evidence

> **职责边界**：本阶段不检查统计报告格式的完整性（如是否报告了均值、效应量、置信区间等），这些由 `results-statistics-convention-checker` 负责。本阶段仅关注**声称强度是否与证据匹配**。

### 2-A 强声称词检测

- [ ] **D2-1** 作者是否使用了强声称词？
  - 触发词：strong evidence, clear evidence, robust finding, strong effect, definite, prove, conclusively demonstrate, establish, confirm
  - 若命中：检查是否有对应的统计证据（如具体数值、效应量、置信区间）支撑该声称
  - 强声称词出现但无对应证据支撑 → 3 分（严重时降至 2 分，绝对化时 1 分）
  - **注意**：单纯缺少效应量或置信区间、且未使用强声称词时，不作为本阶段扣分项
  - 正面对照：F-07（"there was evidence of significant superiority"）、F-10（"the majority are small in magnitude"）
- [ ] **D2-2** 是否将单个研究的结果推广为普遍结论而未提限制？
  - 如 "this establishes that …" / "this conclusively shows …" / "the results prove that …"
  - 命中 → 2 分
  - 问题对照：F-15（"leave no room for doubt"）

### 2-B 绝对化语言

- [ ] **D2-3** 是否出现以下绝对化表达？
  - "prove" / "definitely" / "conclusively" / "beyond doubt" / "leave no room for doubt" / "undoubtedly" / "unquestionably"
  - 命中 → 1 分
  - 问题对照：F-15（"leave no room for doubt"）

### 2-C 因果跳跃检测

- [ ] **D2-4** 是否从相关/观察数据推断因果关系而无实验操纵或纵向证据支持？
  - 如横断面相关数据中写 "X caused Y" / "X led to Y"
  - 命中 → ≤ 2 分
  - 正面对照：F-11（"no causal inferences are implied"）

---

## 阶段 3：逐句扫描 — D3 Causal Language

### 3-A 因果动词检测

- [ ] **D3-1** 是否使用了强因果动词？
  - 触发词：cause, produce, determine, lead to, drive, result in
  - 命中 → 按 C0-1 设计类型判定分数（真实验 4 分；准实验/观察 3 分；横断面 2 分；保守策略 ≤ 2 分）
  - 问题对照：F-06（"leads to"）、F-13（"produced"）
- [ ] **D3-2** 触发词是否用于描述被试行为而非因果推断？
  - 如 "participants produced responses" / "participants produced fewer DO responses"
  - 判定关键：主语是否为实验操纵变量（如 prime / manipulation）→ 因果推断；主语为被试 → 行为描述
  - 若为行为用法 → **不视为问题**，该维度记 **5 分**，不再按 D3-1 评分
  - 正面对照：F-01（"showed signs of" 描述被试行为）
- [ ] **D3-3** 是否使用了中风险因果词而设计不支持？
  - 触发词：affect, influence, contribute to（在观察性数据中）
  - 命中 → 3 分
- [ ] **D3-4** 因果方向是否明确且正确？
  - 如 "X caused Y" 而非 "Y was caused by X"——方向本身无误但措辞需检查
  - 方向不明确 → 3 分

### 3-B 设计-语言匹配

- [ ] **D3-5** 若为横断面相关数据，是否明确声明不可做因果推断？
  - 未声明 → 3 分（若同时使用强因果动词则 ≤ 2 分）
  - 正面对照：F-11（"no causal inferences are implied"）
- [ ] **D3-6** 若为观察性数据，是否提供了替代解释（反向因果 / 第三变量）？
  - 未提供 → 3 分
  - 正面对照：F-11（"it is possible that increased symptomatology caused increased stress"）
- [ ] **D3-7** 真实验设计中是否用中性词替代了强因果词？
  - 如用 "was associated with" 代替 "produced"
  - 未替代 → 4 分（风格偏好，非错误）
  - 正面对照：F-11

### 3-C 结论性因果断言

- [ ] **D3-8** 是否在 Results 中以因果结论形式总结结果？
  - 如 "we draw the conclusion: X produced Y" / "the findings establish that X causes Y"
  - 命中 → 1 分（结论应移至 Discussion）
  - 问题对照：F-13

---

## 阶段 4：逐句扫描 — D4 Interpretation in Results

### 4-A 理论解释

- [ ] **D4-1** 是否在 Results 中用理论机制解释数据趋势？
  - 触发句式："because X was high, Y should be high" / "since … therefore …"
  - 命中 → 3 分
  - 问题对照：F-04
- [ ] **D4-2** 是否在 Results 中用 "because …" 解释为什么做某项分析？
  - 如 "Because dropout can introduce bias, we compared …"
  - 命中 → 3 分（应移至 Method）
  - 问题对照：F-08
- [ ] **D4-3** 是否在 Results 中重述理论预期或假设？
  - 触发句式："we expected that …" / "X should be related to Y" / "these correlations should be higher"
  - 命中 → 3 分（应移至 Introduction 或 Discussion）
  - 问题对照：F-12

### 4-B 结论性总结

- [ ] **D4-4** 是否在 Results 中以结论性段落总结？
  - 触发句式："From the preceding analysis we draw the following conclusions: …" / "In summary, these findings suggest …"
  - 命中 → 1 分（应移至 Discussion）
  - 问题对照：F-13

### 4-C 方法性信息

- [ ] **D4-5** 是否在 Results 中解释数据缺失或排除的原因？
  - 如 "… because the mother had been instructed not to intervene … therefore episodes 2 and 3 are omitted"
  - 命中 → 2 分（应移至 Method 或脚注）
  - 问题对照：F-18
- [ ] **D4-6** 是否在 Results 中解释实验程序或指导语？
  - 命中 → 2 分（应移至 Method）

### 4-D 图表解释

- [ ] **D4-7** 是否在 Results 中解释图表的理论含义而非描述数据构成？
  - 如 "It is helpful to consider that the area represents the majority effect"
  - 命中 → 3 分（理论含义应在 Discussion）
  - 问题对照：F-14
- [ ] **D4-8** 描述图表时是否使用了主观引导语？
  - 如 "It is helpful to consider …" / "This figure illustrates the effect of …"
  - 命中 → 3 分（D4 + D5 双维度）
  - 问题对照：F-14

---

## 阶段 5：逐句扫描 — D5 Subjective / Evaluative Language

### 5-A 主观引导语

- [ ] **D5-1** 是否出现以下主观引导语？
  - "It is instructive to …" / "It is helpful to consider …" / "Interestingly," / "Importantly," / "It is worth noting that …" / "Notably,"
  - 命中 → 3 分
  - 问题对照：F-02、F-14

### 5-B 评价性形容词

- [ ] **D5-2** 是否使用评价性形容词修饰结果？
  - 触发词：conspicuous, instructive, remarkable, striking, impressive, surprising, noteworthy
  - 命中 → 4 分（单个）或 2 分（多个且与统计结果混合）
  - 问题对照：F-17（"conspicuous, instructive"）

### 5-C 绝对化表达

- [ ] **D5-3** 是否出现绝对化表达？
  - 触发词：prove, definitely, conclusively, leave no room for doubt, beyond doubt, undoubtedly, unquestionably
  - 命中 → 1 分（D5 + D2 双维度）
  - 问题对照：F-15

### 5-D 中性替代检查

- [ ] **D5-4** 评价性形容词是否可替换为中性描述？
  - "conspicuous" → "varied widely" / "ranged from X to Y"
  - "instructive" → 删除或改为 "are presented below"
  - "remarkable" → "statistically significant (p = .xx)"
  - 可替换 → 标注建议替换
  - 问题对照：F-17

---

## 阶段 6：全文复核

完成逐句扫描后，对全文进行以下整体检查。

- [ ] **C6-1** 是否存在连续多个句子缺失 hedging？（系统性问题，非个别疏忽）
  - 若连续 3+ 句无 hedging → 在报告中标注为系统性问题
- [ ] **C6-2** 是否存在系统性使用强声称词（如 strong evidence, robust finding）但缺乏对应证据的问题？
  - 系统性强声称无证据支撑 → 在报告中标注为系统性问题
- [ ] **C6-3** Results 部分是否以纯报告结尾，未以讨论性段落收尾？
  - 若以讨论性段落收尾 → 标注 D4 系统性问题
- [ ] **C6-4** 是否存在段落级别的理论讨论（连续 2+ 句解释机制或含义）？
  - 命中 → 标注 D4 系统性问题（2 分）
- [ ] **C6-5** 所有图表引用是否仅描述数据构成，未附加理论解释？
  - 附加了理论解释 → 标注 D4 + D5
- [ ] **C6-6** 是否存在将单个研究的结果推广为普遍结论的段落？
  - 命中 → 标注 D2 系统性问题

---

## 使用说明

1. **优先级**：阶段 0 → 1 → 2 → 3 → 4 → 5 → 6，按序执行。
2. **多维度命中**：同一句子可同时命中多个维度的检查项，分别记分，最终**取最低分**作为该句的综合风险分（分数越低，问题越严重）。
3. **示例引用**：报告中每个 flagged sentence 应引用对应的正面/问题示例 ID（F-01 ~ F-18），为修改建议提供权威依据。
4. **false positive 处理**：若某句在 D4 被标记为"理论解释"但实际是合理的 Results 段末小结（1-2 句），可放宽为 4 分或豁免，在报告中注明理由。
5. **评分方向**：全清单遵循 **5 分为最高（无问题）、1 分为最低（严重问题）**，与 `rubric.md` 和 SKILL.md 保持一致；无问题的维度直接记 5 分，不得使用"2 分 / Pass"等含糊表述。
6. **与 rubric.md 的关系**：本清单是 rubric.md 的操作化版本——清单负责"查什么"，rubric 负责"怎么评分"。
