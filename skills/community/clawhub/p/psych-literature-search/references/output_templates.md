# 文献搜索整理 — 输出模板 (Output Templates)

## 核心输出：一体化文献整理表（主要需求）

将所有关键字段整合在一张大表中，适合直接呈现给用户查阅。
若单篇文献包含多个研究变量，采用多行分列展示（同一编号的文献信息在首行完整呈现，后续变量行只填写变量相关列）。

```markdown
| # | 标题（含链接） | 来源数据库 | 关键词 | 摘要（原文） | 摘要（中文翻译） | 研究变量 | 概念定义 | 操作性定义（测量工具） | 期刊 & 水平 | 被引次数 |
|---|-------------|----------|--------|------------|-----------------|---------|---------|-------------------|-----------|---------|
| 1 | [标题全文](https://doi.org/xxx) | Web of Science | cognitive empathy（认知共情）; emotion regulation（情绪调节）| [原文摘要150-300词] | [中文翻译] | 认知共情 (Cognitive Empathy) | 从认知层面理解他人心理状态的能力（Davis, 1983） | IRI 观点采择分量表（7题，5点计分，α=.81）| *Emotion* Q1 SSCI IF=3.5 | 142 |
|   |   |   |   |   |   | 情绪调节 (Emotion Regulation) | 个体对情绪体验和表达进行管理的过程（Gross, 1998）（推断） | ERQ 认知重评分量表（6题，7点计分）| — | — |
| 2 | [标题全文](https://doi.org/yyy) | Springer Nature [OA] | ... | ... | ... | ... | ... | ... | ... | ... |
```

**链接规则**：
- 优先使用 `https://doi.org/[DOI]` 作为标准链接
- DOI 不可用时，使用 Springer 原始 URL（`url` 字段）
- 两者均不可用时，标注 `[链接不可获取]`

---

## 辅助四表结构（适用于系统综述报告）

当用户需要完整的文献综述报告时，在一体化表格之外，按以下四表格式补充输出。

### 表一 — 文献概览

```markdown
| # | 标题 | 作者 | 年份 | 期刊 | 期刊水平 | 被引次数 | 链接 |
|---|------|------|------|------|----------|----------|------|
| 1 | Title... | Author A.; Author B. | 2022 | Emotion | Q1 SSCI IF≈3.5 | 142 | [DOI](https://doi.org/...) |
```

### 表二 — 关键词与摘要

```markdown
| # | 关键词（双语） | 摘要（原文） | 摘要（中文翻译） |
|---|-------------|------------|----------------|
| 1 | cognitive empathy（认知共情）; emotion regulation（情绪调节）; adolescents（青少年） | [Original abstract, 150–300 words] | [完整中文翻译，80–150字] |
```

**关键词规则：**
- 若文献显式列出关键词，直接使用；若未列出，从摘要和主题标签推断 3–6 个关键词，并标注 `(推断)`。
- 格式：英文原词（中文对应词），如 `mindfulness（正念）`
- 若摘要超过 300 词，先压缩至约 200 词再翻译。
- 无摘要时标注 `[摘要不可获取，请查阅原文]`

### 表三 — 研究变量定义表（核心增值）

```markdown
| # | 核心研究变量 | 概念定义 | 操作性定义（测量工具） |
|---|------------|---------|-------------------|
| 1 | 认知共情 (Cognitive Empathy) | 从认知层面理解他人情绪与心理状态的能力（Davis, 1983） | IRI 观点采择分量表；7题；5点Likert；α=.81 |
|   | 情绪调节 (Emotion Regulation) | 个体对情绪体验及表达进行有意识调控的过程（Gross, 1998）（推断） | ERQ 认知重评分量表；6题；7点Likert |
| 2 | 正念 (Mindfulness) | 对当下时刻的注意与觉察，不带评判（Kabat-Zinn, 1990） | FFMQ 五因素正念量表；39题；5点；α=.87 |
|   | 抑郁症状 (Depressive Symptoms) | 持续性低落情绪与快感缺乏等核心症状（DSM-5）（推断） | PHQ-9；9题；4点Likert |
```

**变量提取规则：**
- **实证研究**：列出所有被测量的核心变量（自变量 IV、因变量 DV、中介/调节变量）
  - 概念定义：研究中引用的理论定义，附原始文献作者和年份（如有）
  - 操作性定义：具体量表/工具名称 + 题目数量 + 计分方式 + 信度（Cronbach's α）
  - 若未显式给出概念定义，从摘要推断并标注 `(推断)`
- **综述/元分析**：列出所综述的主要构念 + 所报告的各类测量工具范围
- **理论文章/社论**：列出主要理论构念 + 其理论定义（若有）
- 信度信息：尽量提取，格式如 `α=.85` 或 `ICC=.92`

### 表四 — 研究设计摘要

```markdown
| # | 研究类型 | 样本量 | 研究方法 | 主要研究工具 | 统计方法 |
|---|---------|-------|---------|------------|---------|
| 1 | 横断面调查 | N=412（大学生） | 问卷法 | IRI, ERQ, PHQ-9 | 层次回归分析 |
| 2 | 元分析 | k=38篇研究, N=12,450 | 文献检索+元分析 | Hedges' g, 调节分析 | 随机效应模型 |
```

**研究类型标准化标签（中英对照）：**
| English | 中文 |
|---------|------|
| Cross-sectional study | 横断面调查 |
| Longitudinal study | 纵向追踪研究 |
| Experimental study | 实验研究 |
| Randomized controlled trial | 随机对照试验 |
| Quasi-experimental | 准实验研究 |
| Systematic review | 系统综述 |
| Meta-analysis | 元分析 |
| Theoretical review | 理论综述 |
| Editorial / commentary | 社论/评论 |
| Scale development / validation | 量表编制/验证 |
| Neuroimaging study | 神经影像研究 |
| Mixed methods | 混合方法研究 |
| Case study | 个案研究 |

---

## 综合分析部分（可选，系统综述时使用）

```markdown
## 五、主题综合分析

### 1. 核心发现
（归纳 3–5 个跨文献的共同发现，每点 1–2 句，引用具体文献编号）

### 2. 研究方法趋势
| 方法类型 | 出现频次 | 代表性工具 |
|---------|---------|----------|
| 问卷调查 | 8篇 | IRI, PHQ-9, FFMQ |
| 实验研究 | 3篇 | Go/NoGo 任务, 情绪启动 |

### 3. 研究空白与未来方向
（指出文献中未被充分研究的方向，5条以内）
```

---

## APA 7 参考文献格式

```markdown
## 六、APA 7 参考文献

1. Author, A. A., & Author, B. B. (Year). Title of article. *Journal Name*, *Vol*(Issue), pp–pp. https://doi.org/xxxxx
```

---

## 输出规范（Output Guidelines）

1. **链接必填**：每篇文献必须提供可点击链接，优先 DOI，其次原始 URL。
2. **关键词必填**：未显式列出时从摘要推断并标注 `(推断)`。双语格式：英文（中文）。
3. **研究变量必提取**：这是本 Skill 的核心增值，每篇文献必须尝试提取研究变量及其定义。
4. **概念定义来源标注**：尽量注明定义的原始引用（作者年份），无明确来源时标注 `(推断)`。
5. **操作性定义格式**：量表名称 + 题目数 + 计分方式 + 信度（如有），如 `PHQ-9; 9题; 4点; α=.87`。
6. **期刊水平必填**：使用 `journal_level.py` 查询，未命中时注明"详见 JCR"。
7. **摘要翻译**：英文摘要必须提供中文翻译。
8. **数据库标注**：每篇明确标注来源（Web of Science / Springer Nature / Semantic Scholar）。
9. **OA 标注**：Springer 开放获取文献标注 `[OA]`。
10. **去重标注**：多库重复收录时只保留一条，标注 `[多库收录]`。
11. **多变量展示**：一篇文献有多个研究变量时，在变量定义列中逐行列出，不省略。

---

## Semantic Scholar 备用查询

当 WoS 和 Springer API 密钥均不可用时，使用 WebFetch 调用：

```
https://api.semanticscholar.org/graph/v1/paper/search?query=[ENCODED_QUERY]&fields=title,abstract,year,venue,authors,citationCount,externalIds&limit=20
```

无需 API 密钥；匿名限速 100 次/5分钟。

遭遇 429 限速时，使用 WebSearch 兜底：
- `"[topic]" journal abstract [year]`
- `"[topic]" site:link.springer.com OR site:frontiersin.org OR site:pmc.ncbi.nlm.nih.gov`
- `"[topic]" "[measurement tool]" psychology study`
