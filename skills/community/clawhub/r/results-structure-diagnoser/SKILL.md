---
name: "results-structure-diagnoser"
description: "Diagnose macro-structure & organization of English psychology Results sections (8 dimensions)."
---

# Results Structure Diagnoser

检查英文心理学/认知神经科学论文 Results 部分的**宏观结构与组织（macro-structure & organization）**。
输出八维评分 + 问题定位 + 仅结构重排建议 + 范围外问题转介（Referral Notes）。

## Scope

**本技能检查（八个结构维度）：**

1. **总体结果陈述**（D1 general statement）：是否存在，位置是否先于具体统计。
2. **结果呈现顺序**（D2 ordering）：小节/实验/分析的先后是否合理。
3. **假设/RQ 对应**（D3 hypothesis/RQ correspondence）：每个结果是否对应某个假设或研究问题。
4. **先概括后具体**（D4 general→specific）：是否先给总体模式再报具体统计结果。
5. **图表正文引入**（D5 figure/table invitation）：图表是否在正文被引入，且与结果陈述一一对应。
6. **结果层次**（D6 layering）：主要/次要/探索性结果是否清楚分层。
7. **多实验/多分析组织**（D7 multi-experiment organization）：多实验、多研究、多分析是否组织清晰。
8. **Results–Discussion 边界**（D8 boundary）：是否过早进入 Discussion。

## Out of Scope / Referral

以下内容**不检查、不评分**；发现时只在报告末尾 "Referral Notes" 一句话转介：

- 连接词、过渡语、句间衔接、段落内部连贯、given→new 信息流 → `results-cohesion-flow-checker`
- 统计格式、APA 规范、统计计算 → `results-statistics-convention-checker`
- 时态与语法 → `results-tense-grammar-checker`
- 学术词汇与搭配 → `results-vocabulary-lexis-advisor`
- Hedging、确定性与过度声称 → `results-claim-hedging-checker`

**边界提醒**：成员 E 的"段落连贯"属局部段落与句间层面；本技能只负责 Results 全文、小节、实验与分析之间的宏观结构。不把连接词、topic continuity、given→new 纳入评分。

## Hard Rules（禁止项）

- 不编造缺失的假设、结果、统计值、图表或研究设计。
- 不进行全文语言润色；只给"仅结构重排"的 Before–After。
- 范围外问题只转介，不评分。
- 结构判断与语言无关；反馈语言默认跟随用户输入语言。

## Evidence Verification（证据核验规则）

- 在声称"全文没有""从未出现""无任何 X""所有结果均……"等全称或绝对判断之前，必须检查**完整 Results 输入**，不能只依据局部段落。
- 对可通过文本定位的表述，应做全文查找或完整逐段核验。
- 无法确认全文范围时，改用有限表述："在已提供的相关段落中未发现……" / "未见明确的……" / "现有文本不足以确认……"。
- 词语出现不等于功能成立：必须结合语境判断其实际修辞功能。
- 不允许仅因出现 "consistent with" 就认定其建立了假设–结果映射；也不允许仅因未注意到某个短语，就声称该短语在全文完全不存在（见 `references/boundary_guide.md`）。
- 报告中的证据定位应引用句号编号、段落、小节、实验或原文短语。
- 信息不足时必须标记"信息不足"，不作绝对结论。

## Workflow

### Step 0 — 识别输入类型与可诊断范围

| 输入类型 | 处理 |
|---|---|
| 完整英文 Results | 跑全八维诊断 |
| Results 片段（单/多段落） | 诊断可见范围内的结构，缺失维度标记"信息不足" |
| 多实验/多研究稿件 | 额外启用 D7 跨实验组织诊断 |
| Results and Discussion 融合节 | 放宽 D8 边界但仍标记过度解释 |
| 仅统计结果/图表清单 | 不编造结果，给结构框架并标记"信息不足" |
| 中文/混合语言草稿 | 结构判断照常（语言无关），反馈语言跟随输入 |

### Step 0b — 建立研究设计画像（决定 D6/D7 是否适用）

- 单研究 vs 多研究/多实验 vs 多分析；纵向/横断；实验/观察/问卷/干预/神经科学。
- 记录主要/次要结局与预注册 vs 探索性分析（据此判定 D6 层次、D7 组织、D3 假设映射）。
- 单研究且无多分析 → D7 标记 N/A；无先验假设（探索性）→ D3 以 RQ/分析目的替代并标注。

### Step 1 — 定位并切分 Results

- 定位 Results（含融合节）起止。
- 按 小节标题 → 段落 → 句子 三级切分并编号（P1, P2, …；S1, S2, …）。
- 记录每个图表编号及其首次在正文被提及的位置（段落/句号）。

### Step 2 — 建立 Hypothesis/RQ → Result mapping

- 从 Introduction、文末假设或用户说明提取假设/RQ 列表（H1, H2… / RQ1, RQ2…）。
- 把每个结果段落/小节映射到对应假设/RQ。
- 标记两类缺口：① 有结果但无对应假设/RQ（孤儿结果）；② 有假设/RQ 但无对应结果（空假设）。
- 假设锚定判定：只有指向假设/预测对象的 "consistent with"（如 "consistent with H1"）才计入假设映射；指向文献或数据的同类短语分别归 D8 或中性描述（见 `references/boundary_guide.md`）。

### Step 3 — 逐项执行八维诊断（D1–D8）

判定依据与 1/3/5 分锚点见 `references/rubric.md`。逐项对照 `references/checklist.md` 打勾（通过/不通过/不适用/信息不足），并记录逐项状态以便复核。

### Step 4 — 检查结果层次（D6）

判定主要/次要/探索性结果的标注与排列，依据 `references/hierarchy_rules.md`。

### Step 5 — 检查多实验/多分析组织（D7）

判定跨实验/研究的组织方式与信号，依据 `references/multi_experiment_guide.md`。

### Step 6 — 检查 Results–Discussion 边界（D8）

判定是否过早进入机制解释/文献比较/理论意义/实践启示，依据 `references/boundary_guide.md`。

### Step 7 — 分配 P0/P1/P2 优先级（仅结构问题）

每项优先级须标注对应维度与 checklist 条目或 rubric 判据（见下节与 `assets/report_template.md`）。

### Step 8 — 输出诊断报告

按 `assets/report_template.md`：输入范围说明 → 研究设计画像 → 总体评分表 → Hypothesis/RQ 映射表 → 八维诊断（紧凑表格，仅低分/关键/信息不足维度展开）→ Checklist 可复核摘要 → Referral Notes → P0/P1/P2（含维度与判据追溯）→ 信息不足与不适用项。

## P0/P1/P2 结构问题优先级

| 级别 | 含义 | 结构类典型问题 |
|---|---|---|
| P0 | 影响结构主干/假设对应/层次/边界 | 缺总体结果陈述、结果与假设无法对应、主次不分、多实验组织混乱、大段过早进入 Discussion |
| P1 | 影响局部组织/图表引入/层次 | 图表未在正文引入、图表与正文结果不对应、个别小节缺先概括后具体、局部顺序颠倒 |
| P2 | 轻微结构优化 | 开场策略可更明确、小节排序可微调 |

## When to load reference files

| 文件 | 加载时机 |
|---|---|
| `references/rubric.md` | Step 3 诊断打分前必读 |
| `references/checklist.md` | Step 3 逐项核对时加载（记录逐项状态） |
| `references/hierarchy_rules.md` | Step 4（D6）时加载 |
| `references/multi_experiment_guide.md` | Step 5（D7）时加载 |
| `references/boundary_guide.md` | Step 6（D8）时加载（含 consistent with 功能判定） |
| `references/examples.md` | 撰写结构重排建议时按需检索正例（真实例句带溯源，已填充 8 篇论文案例） |
| `assets/report_template.md` | Step 8 输出报告时加载 |

## Notes

- 真实例句须来自 `references/examples.md` 且逐字取自论文（带溯源）；禁止编造文献例句。
- 仅结构重排示例：只移动/合并/拆分/补充结构性句子（如补概括句、把结论句移出 Results），不润色措辞。
- 构造的问题句用于教学对照时标注 "constructed example"。
