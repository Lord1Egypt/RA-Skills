# 扫地僧藏经阁 · 文献提炼索引（sources/）

> 本目录收录从原始论文全文提炼的"一经一卡"方法论精华。
> 每张卡 = 一篇论文的核心方法论论点 + 适用边界 + 前提 + 坑 + 换招 + 与其他经文的关系。
> 被方法矩阵（method-matrix.md）路由引用，使取卡有据、诊断有源。

---

## 索引

| 编号 | 文件 | 论文 | 方法矩阵定位 | 核心论点（一句话） |
|------|------|------|-------------|-------------------|
| B1 | [B1-fwe-neuroimaging.md](B1-fwe-neuroimaging.md) | Nichols & Hayasaka 2003 (Stat Methods Med Res) | 比较/批判评价 × 自然理工 → `data-analysis` + `experiment-design` | 大规模多重检验必须控制 FWE；置换检验在低 df 下最优 |
| B2 | [B2-pnn-fear-learning.md](B2-pnn-fear-learning.md) | Banerjee et al. 2017 (Neuron) | 因果/解释机制 × 医学/自然 → `experiment-design` | 复杂系统因果推断需多层收敛证据（行为→分子→组织→可逆干预） |
| B3 | [B3-population-coding-normalization.md](B3-population-coding-normalization.md) | Busse, Wade & Carandini 2009 (Neuron) | 解释机制/建构理论 × 自然理工 → `computational` + `data-analysis` | 好模型用一个机制统一解释多种现象状态（归一化模型跨连续谱） |
| B4 | [B4-ioannidis-false-findings.md](B4-ioannidis-false-findings.md) | Ioannidis 2005 (PLoS Medicine) | 批判评价 × 全学科 → `research-playbook` | PPV = (1-β)R/(R-βR+α)；低功效+低先验+高偏倚=大多数发现是假的 |
| B5 | [B5-manifesto-reproducible.md](B5-manifesto-reproducible.md) | Munafò et al. 2017 (Nature Human Behaviour) | 批判评价/设计创制 × 全学科 → `research-playbook` | 可复现危机需五维协同改进：方法+报告+复现+评价+激励 |
| B6 | [B6-design-based-research.md](B6-design-based-research.md) | Design-Based Research Collective 2003 (Educational Researcher) | 设计创制/建构理论 × 社科教育 → `design-science` | 干预即结果；设计×情境联合产出可用干预与情境化理论 |
| B7 | [B7-contemporary-historiography.md](B7-contemporary-historiography.md) | Scott (ed.) 2023 (HISTOS Supplement 5) | 诠释理解/批判评价 × 人文 → `humanities` | 亲历者叙事≠历史真相；当代史学需批判性分析"在场"本身 |
| B8 | [B8-translation-hermeneutics.md](B8-translation-hermeneutics.md) | Frank 2016 (Open Theology) | 诠释理解 × 人文 → `humanities` | 文本意义≠作者意图；翻译起点是文本本身而非作者心中所想 |
| B9 | [B9-experimental-syntax.md](B9-experimental-syntax.md) | Sprouse 2015 (Linguistics Vanguard, DOI 10.1515/lingvan-2014-1012) | 解释机制/因果 × 语言学 → `cards/linguistics.md` + `cards/experiment-design.md` | 实验句法方法论：可接受性判断/句法岛/强制选择/多范式交叉/三个开放问题 |

---

## 提炼日期
2026-07-11 · 全文 PDF → PyPDF2 提取 → 逐篇精读 → 一经一卡产出

## 维护说明
- **10 本方法论书单**已汇入 `references/methodology-reading-list.md`（书不在本目录，避免与"论文提炼卡"混淆）。
- **B9（实验句法）**：2026-07-13 已补全引用——Sprouse (2015), *Linguistics Vanguard* 1(1):89–100, DOI 10.1515/lingvan-2014-1012（Open Access）。方法论内容已据论文框架对齐。
- B2/B3 实际论文与原 reading-list 预期不同（非 Poldrack 系列），已按实际内容提炼。
- B8 实际论文为 Frank 2016（翻译诠释学），**非** Sprouse 2014（实验句法）——原 Sprouse 位置由 **B9** 补上，两条线互不冲突。
