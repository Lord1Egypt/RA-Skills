# Scoring Rubric — Results Claim & Hedging Checker

## 评分总则

每个维度按 **1—5 分** 评分。**5 分为最高（无问题 / 典范）**，**1 分为最低（严重问题 / 必须修改）**。如果某个维度没有问题，该维度应得 **5 分**。不得使用"2 分 / Pass"等含糊表述——直接给出 1—5 的数字分数。

| 分值 | 标签 | 含义 | 行动要求 |
|------|------|------|---------|
| 5 | 无问题 | 声称强度与证据匹配，hedging 恰当，因果语言与设计一致，无理论解释渗入，无主观评价词 | 无需修改 |
| 4 | 轻微 | 风格偏好层面的微小问题，不影响科学准确性 | 可选修改；低优先级 |
| 3 | 中度 | 声称略超出证据支持，或 hedging 缺失/过度 | 建议修改；说明原因 |
| 2 | 较严重 | 因果语言与设计不匹配，或相关数据写成因果断言，或 Results 中出现理论解释 | 推荐修改；解释误导风险 |
| 1 | 严重 | 绝对化断言（prove, definitely），因果跳跃严重，使用强动词且无对应证据 | 必须修改；解释误导风险 |

---

## D1 — Hedging（对冲表达）

评估句子在间接证据、观察性数据或机制推测上是否使用了恰当的 hedging 表达。既要检测**缺失 hedging**（过度声称），也要检测**过度 hedging**（削弱明确发现）。

| 分值 | 标准 | 典型特征 | 对应示例 |
|------|------|---------|---------|
| 5 | 无问题：hedging 精准匹配证据强度 | 双重限定（如 "It appears … at least in part"）；对间接证据用 "showed signs of"；对混淆变量主动声明 "this interpretation is not advanced because…" | F-01, F-05, F-07, F-09, F-16 |
| 4 | 轻微：hedging 略弱或略强，属风格偏好 | 实验设计下用了 "resulted in" 稍强但可接受；或对强实验数据过度 hedging（如随机对照实验中仍写 "may possibly suggest"） | — |
| 3 | 中度：缺失 hedging，涉及间接证据 | 对中介/机制/观察性数据直接断言，未用任何限定词。如 "the verb mediated the effect" 而非 "may be mediated by" | — |
| 2 | 较严重：相关数据上 hedging 严重不足 | 对相关/观察数据缺少 hedging，如 "X was associated with Y" 在横断面数据中未加任何限制 | — |
| 1 | 严重：对相关/观察数据零 hedging 的因果断言 | 基于横断面相关数据直接写 "X caused Y"，无任何限制声明 | F-11（正面对照） |

**触发词扫描清单**：
- 强动词（缺 hedging 信号）：prove, demonstrate, establish, confirm, cause, produce, determine
- 适度 hedging 词：appear, seem, suggest, indicate, may, might, could, partially, relatively
- 过度 hedging 词（在强实验设计下）：might possibly, could perhaps, seems to potentially

---

## D2 — Claim Strength vs. Evidence（声明强度与证据匹配）

评估句子所做的声明强度是否与统计证据的强度匹配。重点关注：作者是否使用了超出证据支持范围的强声称词（如 "strong evidence""clear evidence""robust finding""definitely"），以及是否从相关结果推断因果。

> **职责边界**：本维度**不负责统计报告格式的完整性检查**（如效应量、置信区间的具体报告格式和完整性），这些由 `results-statistics-convention-checker` 负责。如果结果本身未使用强声称词，单纯缺少效应量或置信区间**不作为本维度的扣分项**。

| 分值 | 标准 | 典型特征 | 对应示例 |
|------|------|---------|---------|
| 5 | 无问题：所有声称都有充分的统计证据支持，声称强度与证据匹配，无过度声称或因果跳跃 | 报告均值 + 方向 + 显著性水平 + 统计量；显著但效应小时主动说明 "small in magnitude"；使用 "there was evidence of" 等适度 hedging | F-03, F-07, F-10 |
| 4 | 轻微：声称强度与证据基本匹配，仅有微小风格问题 | 报告了 p 值和方向，使用中性动词（showed, indicated），未使用强声称词 | — |
| 3 | 中度：部分声称强度略超出证据支持 | 例如使用 "strong evidence" 但未提供效应量或置信区间；或从相关结果推断因果；或使用 "clear effect" 但仅有边缘显著 | — |
| 2 | 较严重：声称明显超出证据支持 | 使用 "robust finding""strong effect" 但统计证据薄弱（如 p ≈ .05、小样本）；或相关数据写成因果断言 | — |
| 1 | 严重：大量声称缺乏证据支持，因果跳跃严重 | 使用 "prove""cause""definitely""leave no room for doubt" 等强动词且无对应证据；绝对化断言排除一切例外 | F-15 |

**子维度判定**：
- **强声称词检测**：出现 "strong evidence / clear evidence / robust finding / definitely / prove / conclusively" 等强声称词时，检查是否有相应的统计证据支撑。若强声称词与证据不匹配 → 按程度判 3—1 分
- **因果跳跃检测**：从相关/观察数据推断因果关系（无实验操纵或纵向证据）→ 至少 2 分
- **绝对化语言**：出现 "prove / definitely / conclusively / no room for doubt" → 直接 1 分
- **注意**：单纯缺少效应量或置信区间，且未使用强声称词时，不作为本维度扣分项

---

## D3 — Causal Language（因果语言适当性）

评估句子中因果动词的使用是否与研究设计匹配。**关键判定依据：研究设计是否支持因果推断**。若用户提供了研究设计信息，按设计类型判定；若未提供，采用保守策略（任何强因果动词均标记 ≤ 2 分）。

| 分值 | 标准 | 典型特征 | 对应示例 |
|------|------|---------|---------|
| 5 | 无问题：因果语言与设计完美匹配 | 真实验设计中用 "resulted in" / "showed significant differences"；观察性数据主动声明 "no causal inferences are implied" 并提供替代解释 | F-11 |
| 4 | 轻微：因果词稍强但设计可支持 | 真实验中用 "leads to" / "produced"——设计支持因果但 Results 惯例偏好中性词 | F-06 |
| 3 | 中度：准实验或观察数据用了因果词 | 准实验（无随机分配）中用 "caused" / "produced"；纵向观察数据用 "leads to" | F-13 |
| 2 | 较严重：横断面相关数据用了强因果词 | 横断面相关数据中用 "caused" / "produced" / "determined"；或用 "draw the conclusion: X produced Y" 将相关结果包装为因果结论 | F-13（若为相关数据） |
| 1 | 严重：观察性数据上绝对化因果断言且无任何限制声明 | 横断面相关数据中用 "caused" 并排除其他解释，无 hedging、无替代说明 | — |

**设计-语言匹配速查表**：

| 研究设计 | 可接受的措辞 | 应避免的措辞 |
|---------|-------------|-------------|
| 随机对照实验 (RCT) | resulted in, showed, was associated with | caused, produced, determines |
| 准实验 (无随机分配) | was associated with, showed differences | caused, produced, leads to |
| 纵向观察 | was related to, predicted | caused, produced, resulted in |
| 横断面相关 | was related to, correlated with | caused, produced, leads to, resulted in |

**触发词扫描清单**：
- 高风险因果词：cause, produce, determine, lead to, drive, result in（观察数据中）
- 中风险因果词：affect, influence, contribute to（需看设计）
- 低风险/中性词：associate with, relate to, correlate with, show, display

**行为用法豁免**：当触发词（如 "produced"）用于描述被试行为（如 "participants produced responses"）而非因果推断（如 "the prime produced the effect"）时，**不应视为问题**，该维度记 **5 分**。判定关键在于主语是否为实验操纵变量及其是否暗示因果关系。

---

## D4 — Interpretation in Results（Results 中的解释性内容）

评估 Results 部分是否包含了应属于 Discussion / Introduction / Method 的内容。Results 应**报告数据**，而非**解释原因、重述假设或讨论理论含义**。

| 分值 | 标准 | 典型特征 | 对应示例 |
|------|------|---------|---------|
| 5 | 无问题：纯数据报告，零解释 | 仅报告统计比较结果；即使有解释也明确标注 "this interpretation is not advanced because…" 并给出理由；混淆变量处主动声明限制 | F-16 |
| 4 | 轻微：单句内嵌一个理论性从句但不影响整体报告性质 | 如 "X was significantly higher than Y (p = .03), consistent with the hypothesis."——后半句可移至 Discussion | — |
| 3 | 中度：完整句子用理论解释数据 | "Because X was high, Y should also be high" 的推理句；"Since… should be related to…" 的假设重述；"Because… can introduce bias, we compared…" 的分析动机解释 | F-04, F-08, F-12 |
| 2 | 较严重：段落级别的理论讨论或假设重述 | 整段用理论机制解释结果趋势；或解释数据缺失原因（属 Method） | F-18 |
| 1 | 严重：Results 中出现结论性总结 + 理论解释，完全偏离结果报告 | "From the preceding analysis we draw the following conclusions: …" 的结论性段落 | F-13 |

**子类型判定**：
- **理论解释型**：用 "because / since / as … should be" 解释数据趋势 → 3 分
- **假设重述型**：在 Results 中重述 "we expected / X should be related to Y" → 3 分（参见 F-12）
- **分析动机型**：用 "Because… we compared / we conducted" 解释为什么做某分析 → 3 分（参见 F-08）
- **结论总结型**："we draw the following conclusions" / "the findings suggest that …" 的讨论级总结 → 1 分（参见 F-13）
- **方法解释型**：在 Results 中解释数据缺失、排除原因 → 2—1 分（参见 F-18，应移至 Method）

---

## D5 — Subjective / Evaluative Language（主观评价语言）

评估句子是否使用了主观评价词、主观引导语或绝对化表达，这些语言削弱 Results 部分的客观性。

| 分值 | 标准 | 典型特征 | 对应示例 |
|------|------|---------|---------|
| 5 | 无问题：完全客观，零评价词 | 纯数据描述，无形容词修饰，无主观引导 | F-01, F-03 |
| 4 | 轻微：偶有中性描述词 | 如 "notably" 仅做过渡而非评价；"marked" 修饰差异但附统计量 | — |
| 3 | 中度：单个评价性形容词 | 单独使用 "interesting" / "notable" / "striking" 修饰结果，但句子主体仍为数据 | — |
| 2 | 较严重：主观引导语 + 评价词 | "It is instructive to…" / "It is helpful to consider…" 等主观引导语；"conspicuous, instructive" 等评价形容词与统计结果混合 | F-02, F-14, F-17 |
| 1 | 严重：绝对化表达 + 主观框架 | "leave no room for doubt" / "prove" / "definitely" 等绝对化语言，且嵌入主观评价框架中 | F-15 |

**触发词扫描清单**：
- 主观引导语：It is instructive to, It is helpful to consider, Interestingly, Importantly, Notably, It is worth noting that
- 评价性形容词：conspicuous, instructive, remarkable, striking, impressive, surprising
- 绝对化表达：prove, definitely, conclusively, leave no room for doubt, beyond doubt, undoubtedly
- 中性替代词：showed, displayed, varied, ranged, differed, was associated with

---

## 跨维度综合评分

当句子触发多个维度时，取**最低分**作为该句的综合风险分（分数越低，问题越严重）。例如，一个句子同时在 D3 得 2 分、D5 得 3 分，则综合分为 2 分。

### 综合分与行动对应

| 综合分 | 行动 | 报告格式 |
|--------|------|---------|
| 5 | 无需修改 | 不列入报告（除非用户要求 full audit） |
| 4 | 可选修改（低优先级） | 列入，标注 "Optional" |
| 3 | 建议修改（中优先级） | 列入，标注 "Suggested" |
| 2 | 推荐修改（高优先级） | 列入，标注 "Recommended" |
| 1 | 必须修改（最高优先级） | 列入，标注 "Required" |
