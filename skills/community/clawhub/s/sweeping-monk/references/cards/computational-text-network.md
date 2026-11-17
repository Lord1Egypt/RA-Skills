# 计算文本与网络方法卡（computational text & network）

> 招式定位：描述 / 关联 / 比较。学科轴：人文 · 社科 · 计算社科 · 传播。
> 与 `cards/humanities.md`（诠释）、`cards/data-analysis.md`（统计）、`cards/bibliometrics.md`（引文网络）互补：本卡给"大规模文本/关系"的量化工具。

## 适用场景
- 大批量文本（论文/新闻/社媒/政策）要**系统性量化**，而非逐篇精读。
- 看"谁和谁连、结构什么样"（合作网/引文网/语义网/社交网）。
- 趋势/话语/框架/情绪随时间的演化。

## 核心方法
1. **文本作为数据（text-as-data）**：
   - 词频 / TF-IDF / 主题模型（LDA、BERTopic）→ 议题结构。
   - 词嵌入（word2vec / 上下文嵌入）→ 语义相似度、概念漂移。
   - 词典法（情感/意识形态）：快但依赖词典效度，别当金标准。
   - 监督分类（人工标注金标准→打标大库）：需交叉验证，防过拟合。
2. **网络分析**：
   - 中心性（度 / 介数 / 特征向量）→ 谁是关键节点。
   - 社群检测（Louvain / Infomap）→ 模块化结构。
   - 网络演化（新增边/节点趋势）→ 凝聚或分化。
3. **稳健性**：多方法交叉（主题模型 + 嵌入 + 人工抽样校验），别被单算法牵着走。

## 前提
- 文本需清洗（去噪/分词/语言匹配）；非英文需对应分词/嵌入模型。
- 标签/词典要有构念效度论证；纯黑箱模型结论要可解释。

## 常见坑
- **把频率当重要**：高词频≠高意义，要看相对/上下文。
- **算法当真理**：LDA 主题数 k 主观，结果敏感；需稳定性检验。
- **忽略采样偏差**：爬来的社媒≠总体；代表性要说清。
- **可复现缺失**：随机种子/语料版本不固定→别人重跑不出同结果。

## 何时换招
- 要"领域知识地图"快速了解 → `cards/bibliometrics.md` / `research-playbook.md` §八。
- 要深读少样本文本意义 → `cards/humanities.md` / `cards/qualitative.md`。
- 要"复现/公开" → `cards/replication-preregistration.md`。

## 经典出处
- Gentzkow, Kelly & Taddy. 2019. *Text as Data*. Journal of Economic Literature 57(3):535–574. DOI 10.1257/jel.20181020
- Lazer et al. 2009. *Computational Social Science*. Science 323(5915):721–723. DOI 10.1126/science.1167742
- Newman 2010. *Networks: An Introduction*. Oxford. ISBN 9780199206650
