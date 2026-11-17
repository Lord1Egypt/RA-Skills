# Boundary Guide — Results–Discussion 边界判定（D8）

## 判定目标

判断 Results 是否过早进入 Discussion。Results 应停留在**结果陈述 + 有限的贴附解释**，不越界进入机制、文献、理论或实践意义。

## 允许留在 Results 的内容

- 结果陈述与方向/显著性报告。
- 对结果的直接、贴附式说明（"suggesting a stronger effect for…"）。
- 有限的技术性解释（如 "this null effect may reflect low power" 之类简短说明）。
- 贴附式总结（B3 "These results demonstrate a feedback loop…"）。

## 越界信号（应移至 Discussion）

| 越界类型 | 典型表现 | 真实边界例 |
|---|---|---|
| 深层机制解释 | "This may be explained by…" / "…because…" 长篇机制推理 | C1-04 "suggesting that… interfered with efficient pruning"（有限，可保留） |
| 文献比较 | "consistent with prior work showing…" / 引用并对比他人结论 | （见 constructed EX-02） |
| 理论意义 | "These findings contribute to…" / 理论框架升华 | （见 constructed EX-03） |
| 实践启示 | "These results have implications for…" / 应用建议 | （见 constructed EX-03） |

## 词面形式不等于语篇功能（consistent with 的判定）

"consistent with …" 至少可能承担三种不同功能，必须结合宾语与语境判定，**不得单凭短语本身评分**，也不得将其规定为固定错误信号：

1. **假设映射**（归 D3）：宾语为假设/预测对象，如 "The result was consistent with H1."——可作为结果与预先假设对应的证据。
2. **文献比较**（归 D8 边界审查）：宾语为既有研究/文献，如 "This pattern was consistent with previous studies."——属于与文献比较，可能触发 Results–Discussion 边界审查。
3. **模型/数据一致性**（中性）：宾语为模型预测、操作检验或数据模式（如与拟合结果一致）——需结合上下文判断，不能自动归为假设映射或 Discussion 越界。

判定原则：
- 先识别 "consistent with" 的**宾语或指向对象**；
- 再判断其承担的是**假设回指、结果描述、模型检验还是文献解释**；
- D3 与 D8 若同时相关（如一句话既回指假设又对比文献），应**分别说明功能**，避免重复扣分；
- 证据核验：声称"全文无某短语/无假设回指"前必须核验完整输入（见 SKILL.md Evidence Verification）。

## 旧版组件 6–9 处理原则

旧版 academic-results-editor 的 Generic Results Model 组件 6–9（Comparison with Other Studies / Explanation via Known Facts / Problems-Issues / Implications）**不作为标准 Results 组件**，在本技能中一律视为 D8 边界风险触发项：出现即标记"可能过早进入 Discussion"，而非要求补充。

## 边界判定步骤

1. 定位疑似越界句/段。
2. 判定其为"有限贴附解释"（保留）还是"深层 Discussion"（转介/建议移除）。
3. 判定越界类型（机制/文献/理论/实践）；文献类先按"词面形式不等于语篇功能"确认指向对象。
4. 若为 Results and Discussion 融合节 → 放宽判定（不机械判越界），但仍标记明显过度解释与文献/理论越界。

## 判定输出

- 对每个越界句/段标注越界类型与位置。
- 区分"有限贴附解释"（保留）与"深层 Discussion"（转介 Discussion 或建议移除）。
- 仅结构重排建议：把越界句移出 Results 或降级为贴附句，不润色措辞。
- 融合节（Results and Discussion）放宽判定，但仍标记过度解释与文献/理论越界。
