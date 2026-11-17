# results-statistics-convention-checker 交付说明

> 成员 B 交付物说明：制作标准、文献来源与筛选说明、例句溯源总表、评测记录
> 日期：2026-08-22（初版提交期限：8 月 23 日）

---

## 一、交付物清单

| # | 交付物 | 路径 |
|---|--------|------|
| 1 | Skill 初版（已打包，通过官方校验） | `/mnt/agents/output/results-statistics-convention-checker.skill` |
| 2 | Skill 源文件夹（SKILL.md + rubric + checklist + examples + 测试文件） | `/mnt/agents/output/results-statistics-convention-checker/` |
| 3 | 8 篇论文 PDF（按"作者_年份_期刊简称"重命名） | `/mnt/agents/output/成员B_8篇论文PDF/*.pdf` |
| 4 | 统计报告 examples（含在 skill 内） | `results-statistics-convention-checker/references/examples/examples_memberB.md` |
| 5 | rubric.md（评分量规） | `results-statistics-convention-checker/references/rubric.md` |
| 6 | checklist.md（检查清单） | `results-statistics-convention-checker/references/checklist.md` |
| 7 | 测试输入 / 测试输出 | `results-statistics-convention-checker/tests/test_input.md`、`test_output.md` |
| 8 | 配对评测报告（baseline vs with_skill） | `/mnt/agents/output/eval1/report.md`、`report(1).md` |
| 9 | 本说明文档 | `/mnt/agents/output/交付说明_results-statistics-convention-checker.md` |

---

## 二、文献来源与筛选说明

### 文献来源
本模块 8 篇论文为小组统一收集的环境心理学 / 环境行为方向实证研究论文（窗景、光照、恢复性环境主题），由成员 B 逐篇核验后用于统计报告 examples 提取。

### 核验标准（4 条）
1. **体裁**：实证研究论文，含完整、独立的 Results 部分（P3 为会议论文集章节、P6 为会议论文，Results 与 Discussion 合写，保留作为问题例来源）；
2. **统计报告密度**：Results 中含足够密度的统计报告句（t / F / p / M / SD / r / β 等），可支撑正例与问题例双向提取；
3. **可得性**：全文 PDF 可合法获取，小组内可分发使用；
4. **时效性**：2020–2025 年发表，反映当前主流期刊统计报告实践（含不规范实践，问题例同样来自真实发表论文）。

### 最终入选 8 篇

| 编号 | 论文 | 期刊 | 年份 | 主要用途 |
|---|---|---|---|---|
| P1 | Xu, Liu, Li & Xia. Effects of environmental lighting on students' sleep, alertness and mood: A field study in a Chinese boarding school | Lighting Research & Technology, 56, 185–206 | 2024 | F/t 完整报告、阴性结果精确 p、± SEM 界定、边缘显著表述（正例 B-01～B-04） |
| P2 | Yoon, Lim, Kim & Joo. The relationship between perceived restorativeness and place attachment for hikers at Jeju Gotjawal Provincial Park | Frontiers in Psychology, 14, 1201112 | 2023 | SEM 拟合指数组合、β + 解释方差、Δχ² 不变性检验（正例 B-05、B-06） |
| P3 | Jain, Garg & Goel. Comparison of Indoor Air Quality for Air-Conditioned and Naturally Ventilated Office Spaces | Lecture Notes in Civil Engineering, Vol. 60 | 2020 | 无检验的百分比差异断言、± 未界定、结果与解释混杂（问题例 B-10） |
| P4 | Song et al. Is more vegetation always better? Evaluation of restorative benefits and preference for window views | Building and Environment, 272, 112660 | 2025 | t 检验规范表格（含 95% CI）、正文概括+表格承载、相关报告（正例 B-11、B-12） |
| P5 | Elsadek, Zhang & Liu. High-rise window views: Evaluating the physiological and psychological impacts of green, blue, and built environments | Building and Environment, 262, 111798 | 2024 | F 缺自由度、± 未界定（问题例 B-07） |
| P6 | Dong, Liu, Qi & Huang. Research on the Current Situation and Improvement Strategy of Light Environment in College Classroom | IOP Conf. Series: Earth and Environmental Science, 531, 012045 | 2020 | 纯描述统计、无推断统计、模糊表述（问题例 B-09） |
| P7 | Luo et al. Natural Dose of Blue Restoration: A Field Experiment on Mental Restoration of Urban Blue Spaces | Land, 12, 1834 | 2023 | F + 精确 p + partial η² 三件套、事后比较报 M、信度报告、p=0.000 提示（正例 B-13、B-14） |
| P8 | Yao, Lin, Bao & Zeng. Natural or balanced? The physiological and psychological benefits of window views with different proportions of sky, green space, and buildings | Sustainable Cities and Society, 104, 105293 | 2024 | p < 0.1 当显著、成串 p 值无统计量（问题例 B-08） |

---

## 三、Skill 制作标准

### 1. 检查范围（严格对齐小组分工表，成员 B）
六类统计报告检查点：
- **描述统计**：M、SD 是否成对、格式一致；"X ± Y" 是否界定 SD / SEM；
- **推断统计格式**：t(df)、F(df1, df2)、χ²(df) 是否完整；SEM 是否报告 χ²、df 与多个拟合指数（CFI、RMSEA、SRMR）；相关是否报 r（区分 Pearson r / Spearman rs）；回归是否报 β、R²；
- **p 值报告**：精确 p 值 vs 阈值报告；p = .000、前导零混用、p < .1 当显著等违规识别；阴性结果是否完整报告；
- **效应量**：Cohen's d、partial η²、r、β 是否报告并解读；
- **置信区间**：关键比较是否报告 95% CI；
- **一致性**：文中数值与图表、文字结论与统计方向是否一致；差异断言是否有检验支撑。

### 2. 边界控制
在 SKILL.md 中显式声明**不检查**的其他五个模块（结构、时态语法、词汇、衔接连贯、hedging），发现此类问题只在报告末尾"转介提示"，避免与成员 A/C/D/E/F 的技能重叠；同时声明**不替代统计计算本身**、不评价统计方法选择与实验设计。

### 3. 例句使用标准
- rubric / examples 中所有英文例句**逐字摘自 8 篇论文的 Results 部分**，每条保留溯源标注（Example ID + 作者年份 + 期刊 + Results 小节）；全文共精选 **14 条真实例句**（8 条正例、6 条问题例），8 篇论文全覆盖；
- 诊断输出中的 Before / After 改写句为构造句，缺失的数值（df、效应量等）一律以 X.XX 占位并注明"请据实补全"，**禁止编造统计数值**，与真实文献例句严格区分。

### 4. 输出标准
诊断报告按 SKILL.md 第 8 节统一格式输出：Dimension Score（1–5 分，对照 rubric 锚点与速查表）→ Key Problems（按严重程度排序）→ Evidence from Draft（原文引用定位）→ Example-based Comparison（引用 Example ID）→ Revision Suggestions（Before / After 示范改写）→ Priority Level（高/中/低 + 理由）。

### 5. 质量验证
- 结构通过官方校验脚本验证（`quick_validate.py` → "Skill is valid!"）；
- 完成一轮 with_skill vs baseline 配对评测（见下节）。

---

## 四、评测记录（skill 有效性验证）

| 项 | 内容 |
|---|---|
| 测试输入 | 一段构造的、含典型统计报告问题的英文 Results 片段（tests/test_input.md：t/F 缺自由度、p = .000、p < 0.1 当显著、± 未界定、只报 p 无统计量、无效应量、无检验的百分比断言、阴性结果只写 n.s. 等 10 类问题，共 13 句） |
| 对照设计 | with_skill（加载本技能）vs baseline（无技能），同一输入，独立诊断 |
| 评测产物 | baseline 输出：`eval1/report.md`；with_skill 输出：`eval1/report(1).md` |
| 评测结论 | **with_skill 胜**：(1) 给出五个子维度的量化评分与 2/5 总评（对照 rubric 锚点与速查表），baseline 无量化评分；(2) 逐句定位原文证据并标注 checklist 未通过项，baseline 仅定性描述；(3) 每个问题引用真实文献例句（Example ID + 溯源）作为诊断依据并给出 Before / After 规范改写，baseline 只给笼统建议；(4) 提供高/中/低修改优先级排序与对其他五个技能的转介机制，baseline 无优先级、无转介；(5) 漏诊控制：with_skill 检出全部 10 类植入问题，baseline 漏检"前导零混用"且未识别 S1 "better" 的概括无支撑问题 |
| 评测后修订 | 依据评测发现，在 checklist 中强化了 D3（前导零统一）、F2（方向性结论与统计表述对应）两项检查点的表述，并在 rubric 速查表中明确"格式瑕疵单项不降级、多项叠加降 1 级"的定级规则，重新打包 |

---

## 五、使用方式（小组集成说明）
- 本 skill 为单项诊断技能，可被成员 G 的汇总技能 `results-summary-report-generator` 调用；
- 调用入口：`SKILL.md`；按需加载 `references/`（examples / rubric / checklist）与 `tests/`（测试样例）；
- 输入：论文 Results 片段（建议同时提供研究假设与图表信息）；输出：结构化统计报告规范诊断报告（markdown，含评分、问题定位、examples 对照、Before/After 改写、优先级）；
- 默认以 APA 第 7 版为基准，目标期刊另有规定时从其规定。
