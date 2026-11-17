# 扫地僧 · 全学科方法矩阵（method-matrix）

> 老衲的"藏经阁书目"。遇题先在此定位：**根本招式（行）× 学科轴（列）= 该取哪张卡**。
> 用法：辨明根因后，看用户要的是哪类"知识动作"（行），落在哪个学科（列），交叉格即方法 + 指向的卡。只读那一张卡，不翻全阁。
> "—" 表示该学科此招式非主干（非不能用，只是通常另有更贴的招式），可据语境灵活取用。

---

## 一、矩阵总览

**根本招式（行，不分学科）**：描述 · 比较 · 关联 · 因果 · 预测 · 解释/机制 · 建构/理论 · 设计/创制 · 批判/评价 · 诠释/理解

**学科轴（列）**：社科/教育 · 医学/临床 · 计算机/AI · 经济 · 人文 · 工程/设计 · 艺术 · 自然/理工 · 法学实证 · 语言学 · 心理/认知 · 生态/环境（含法学实证 / 语言学 / 心理认知 / 生态环科四轴）

| 根本招式 ＼ 学科 | 社科/教育 | 医学/临床 | 计算机/AI | 经济 | 人文 | 工程/设计 | 艺术 | 自然/理工 | 法学实证 | 语言学 | 心理/认知 | 生态/环境 |
|---|---|---|---|---|---|---|---|---|---|---|
| **描述** | 描述统计→survey-scale / data-analysis | 流行病学描述→data-analysis | 基线/数据画像→ml-eval / data-analysis | 数据画像→data-analysis / econometrics | 文本描述/综述→humanities | 需求/规格描述→design-science | 作品形式分析→humanities | 观测/表征→experiment-design | 法律/案例描述→data-analysis / empirical-legal | 语料/形式描述→data-analysis / linguistics | 行为/反应时描述→data-analysis / ml-eval | 群落/多样性描述→data-analysis |
| **比较** | 组间 t/ANOVA→data-analysis | RCT/队列比较→experiment-design | 基线 vs 方法→ml-eval | 组间/地区比较→econometrics / data-analysis | 比较研究→humanities | 方案 A-B→design-science | 风格比较→humanities | 条件对比→experiment-design | 法系/管辖比较→empirical-legal / humanities | 语言/方言比较→linguistics / humanities | 组间/条件比较→experiment-design | 生境/处理比较→experiment-design / data-analysis |
| **关联** | 相关/因子→data-analysis | 危险因素关联→data-analysis | 特征相关→data-analysis | 变量关联/协整→econometrics | 主题关联→humanities | 参数关联→design-science / data-analysis | 形式关联→humanities | 变量相关→experiment-design / data-analysis | 法律变量关联→econometrics / empirical-legal | 语言变量相关→data-analysis / linguistics | 相关/因子→data-analysis | 物种/环境关联→data-analysis |
| **因果** | 准实验/IV→experiment-design | RCT→experiment-design | 消融/A-B/因果推断→ml-eval / experiment-design | DID/IV/RDD/合成控制→econometrics | 因果叙事→humanities | 控制实验→experiment-design | — | 控制实验→experiment-design | 法律改革 DID/自然实验→econometrics / empirical-legal | 句法/语音因果→experiment-design / linguistics | RCT/准实验→experiment-design | 野外控制实验/自然实验→experiment-design |
| **预测** | 回归/ML 预测→data-analysis | 风险预测模型→data-analysis / ml-eval | 预测模型/benchmark→ml-eval | 预测/景气→econometrics | 趋势诠释→humanities | 性能预测→design-science | — | 模型预测→experiment-design | 判决/量刑预测→ml-eval / empirical-legal | 语言模型预测→ml-eval / linguistics | 行为/认知预测模型→ml-eval / data-analysis | 种群/气候预测→ml-eval / data-analysis |
| **解释/机制** | 中介/调节/质性机制→qualitative / data-analysis | 病理机制→experiment-design | 可解释 AI/归因→ml-eval | 机制分析→econometrics | 阐释→humanities | 原理机制→design-science | — | 机制实验→experiment-design | 法律规则作用机制→qualitative / empirical-legal | 语言加工机制→computational / linguistics | 认知机制/中介→qualitative / data-analysis / experiment-design | 生态机制→experiment-design |
| **建构/理论** | 扎根理论/量表→qualitative / survey-scale | 临床构念→survey-scale / qualitative | 框架/模型提出→ml-eval / design-science | 理论模型→econometrics | 理论建构/批判→humanities | 设计科学(artifact+理论)→design-science | 创作即理论(实践研究)→humanities | 理论/模型建构→experiment-design | 法律理论→humanities / empirical-legal | 语法理论→humanities / linguistics | 理论模型/量表→survey-scale / qualitative | 理论模型→experiment-design |
| **设计/创制** | 干预方案→experiment-design / design-science | 器械/疗法→experiment-design | 系统/算法→ml-eval / design-science | 政策设计→econometrics | — | DSRM 设计科学→design-science | 创作/实践研究→humanities | 装置/实验设计→experiment-design | 法律实验/田野实验→experiment-design / empirical-legal | 实验范式设计→experiment-design / linguistics | 实验范式/任务设计→experiment-design | 监测/实验设计→experiment-design |
| **批判/评价** | 批判话语/方案评价→qualitative / survey-scale | 疗效评价/RoB→experiment-design / data-analysis | benchmark/消融评价→ml-eval | 政策评估→econometrics | 文本批评/考据→humanities | artifact 评价→design-science | 作品评价→humanities | 结果评价→experiment-design / data-analysis | 法律政策评估→econometrics / empirical-legal | 语言学论证评价→humanities / linguistics | 效度评价→experiment-design / data-analysis | 评价→data-analysis / experiment-design |
| **诠释/理解** | 主题分析/患者体验→qualitative | 患者体验诠释→qualitative | — | — | 诠释学/文本理解→humanities | 使用体验诠释→design-science / qualitative | 意义诠释→humanities | — | 法律文本诠释→humanities | 语义/语用理解→humanities / linguistics | 体验诠释→qualitative | — |

---

## 二、方法卡索引

| 卡名 | 一句话 | 文件 |
|------|--------|------|
| 实验方法卡 | RCT/准实验/组内组间/随机/盲法/效度威胁 | `cards/experiment-design.md` |
| 数据分析卡 | 目的→数据→变量 决策树选统计法，含前提与坑 | `cards/data-analysis.md` |
| 问卷量表卡 | 构念→题项→EFA/CFA→α/CR/AVE→共同方法偏差 | `cards/survey-scale.md` |
| 质性方法卡 | 访谈/焦点小组/民族志/扎根理论/主题分析/话语分析/现象学/内容分析/CQR | `cards/qualitative.md` |
| 计算模拟卡 | 数值/ABM/形式化证明/算法基准 + 敏感性/收敛/消融 | `cards/computational.md` |
| 人文方法卡 | 考据校勘/史纂/诠释学/比较文学/档案/语文学 | `cards/humanities.md` |
| 设计科学卡 | DSRM 循环 + 案例法 Yin（协议/证据三角/跨案例） | `cards/design-science.md` |
| 计量经济卡 | DID/IV/RDD/匹配/面板 FE/合成控制 + 识别假设 | `cards/econometrics.md` |
| ML/AI 评估卡 | benchmark/消融/人工评测/可复现（贴 SmartLib 对话评估） | `cards/ml-eval.md` |
| 文献计量卡 | 引文网络/共被引/突现词/h 指数/合作网络 + 引用偏见 | `cards/bibliometrics.md` |
| 系统综述卡 | PRISMA/偏倚风险/I²/效应量/GRADE + 发表偏倚 | `cards/systematic-review.md` |
| 混合方法卡 | 并行收敛/解释序列/探索序列 + 整合(legitimation) | `cards/mixed-methods.md` |
| 法学实证卡 | 案例统计/审计研究/自然实验(DID)/判决建模 | `cards/empirical-legal.md` |
| 语言学方法卡 | 实验句法/语音/心理语言学/社会语言学/语料 | `cards/linguistics.md` |
| 复现与预注册卡 | 预注册/注册报告/复现设计/可复现闸门 | `cards/replication-preregistration.md` |
| 纵向生存卡 | 混合效应/交叉滞后/Cox/竞争风险 + 删失 | `cards/longitudinal-survival.md` |
| 计算文本网络卡 | text-as-data/主题模型/网络中心性/社群检测 | `cards/computational-text-network.md` |

---

## 三、取卡心法（老衲的提醒）

- **先辨根因，再落矩阵**：用户说"我要做问卷"，根因可能是构念未操作化——取 `survey-scale` 前先点破"你的构念是什么"。
- **一招不够就组合**：真实研究常跨多招式（如"因果+解释"→ 实验 + 质性机制）。矩阵可同时命中多张卡，按需都取。
- **矩阵空白处即缺口**：若某格暂无对应卡，老衲据内功底座（research-playbook）现场给心法，并记下落点待补卡。
- **不抢检索活**：卡只讲"方法怎么选、怎么用、坑在哪"，不替用户跑文献——检索交还 literature-search 等技能。
