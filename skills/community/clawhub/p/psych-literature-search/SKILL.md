---
name: psych-literature-search
description: "Searches and organizes academic literature on a given topic or research question. Queries PubMed (NCBI E-utilities, no API key required) and Semantic Scholar (free REST API, no key required). Produces structured tables including: title, keywords (bilingual), DOI/URL link, full abstract (with Chinese translation), research variable conceptual definitions, and operational definitions (measurement instruments/scales). Also includes citation counts and publication types. This skill should be used when the user wants to find and organize academic papers on any topic, conduct a systematic literature review, extract research variable definitions and measurement instruments, or compile references for a study."
agent_created: true
---

# 文献自动搜索与整理 Skill

## 功能目的

针对用户给定的研究主题，自动搜索 PubMed（NCBI E-utilities，无需 API Key）与 Semantic Scholar（免费 REST API，无需 Key）两大数据库，提取每篇文献的核心信息，并整理为结构化表格，包含：文献标题、关键词、链接、摘要、研究变量的概念定义、操作性定义（测量工具）等。

---

## 触发条件（Trigger Conditions）

当用户出现以下任一意图时，立即启用此 Skill：

**中文触发词：**
- 帮我搜索 / 查找 / 找 XX 主题的文献
- 做一个文献综述 / 文献检索
- 整理 XX 相关的研究论文
- 文献搜索，主题是 XX
- 帮我找关于 XX 的学术文章
- XX 的研究变量是什么 / 操作性定义是什么
- 搜索 PubMed / Semantic Scholar 文献
- 搜索心理学 / 医学 / 生命科学文献

**English trigger phrases:**
- "search literature on [topic]"
- "find papers / articles about [topic]"
- "literature review on [topic]"
- "search PubMed / Semantic Scholar for [topic]"
- "organize papers into a table"
- "what are the research variables / operational definitions in studies on [topic]"

---

## 执行工作流（Workflow）

### Step 1 — 确认搜索参数

If the query is unclear, ask the user:
- **研究主题**（必填）：具体关键词或研究问题
- **时间范围**（默认近 10 年）
- **文献数量**（默认每个数据库 10–15 篇）
- **API 密钥**（可选）：WoS / Springer 密钥；无密钥则使用 Semantic Scholar 免费备用通道

建议澄清提示（中文）：
> "请告诉我：① 具体研究主题或关键词；② 时间范围（默认近10年）；③ 需要多少篇？如有 Web of Science 或 Springer API 密钥请提供，没有也可以用免费通道搜索。"

---

### Step 2 — 搜索文献

PubMed 和 Semantic Scholar 均**无需 API Key**，直接运行附带脚本即可。

#### 并行搜索：PubMed + Semantic Scholar（推荐）

使用托管 Python 运行时并行运行两个脚本：

**PubMed（NCBI E-utilities，无需 Key）：**
```bash
"C:\Users\refresh\.workbuddy\binaries\python\versions\3.13.12\python.exe" \
  "C:/Users/refresh/.workbuddy/skills/psych-literature-search/scripts/search_pubmed.py" \
  --query "[TOPIC]" --max 30
```

**Semantic Scholar（免费 REST API，无需 Key）：**
```bash
"C:\Users\refresh\.workbuddy\binaries\python\versions\3.13.12\python.exe" \
  "C:/Users/refresh/.workbuddy/skills/psych-literature-search/scripts/search_semantic.py" \
  --query "[TOPIC]" --max 30
```

两个脚本并行运行；解析 JSON 输出，每个返回 `hits` 数组，包含 title, authors, year, journal, doi, abstract, keywords, url, database 字段。

**PubMed 参数说明：**
- `--mindate 2015` / `--maxdate 2024`：时间范围过滤
- `--email you@example.com`：可选，填写你的邮箱以符合 NCBI 礼仪要求

**Semantic Scholar 参数说明：**
- `--year 2015-2024`：年份过滤
- `--venue "Journal Name"`：按期刊/会议过滤
- 速率限制：无需 Key 时 100 次/5 分钟，脚本已内置限速（每次请求间隔 6 秒）

#### 方案 B：WebFetch 补充（可选）

若脚本执行失败，使用 WebFetch 工具直接调用 API：

**PubMed E-utilities（WebFetch）：**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=[URL-ENCODED TOPIC]&retmax=20&sort=relevance&retmode=xml
```
然后对返回的每个 PMID 调用：
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=[PMIDs]&retmode=xml
```

**Semantic Scholar（WebFetch）：**
```
https://api.semanticscholar.org/graph/v1/paper/search?query=[URL-ENCODED TOPIC]&fields=title,authors,year,venue,doi,abstract,citationCount,fieldsOfStudy&limit=20
```

#### 方案 C：WebSearch 兜底

如脚本和 WebFetch 均失败，使用 WebSearch：
- `"[topic]" pubmed abstract`
- `"[topic]" site:semanticscholar.org`
- `"[topic]" (site:pubmed.ncbi.nlm.nih.gov OR site:semanticscholar.org)`

---

### Step 3 — 补充被引次数与文献类型

PubMed 结果已包含 `publication_types`（如 "Journal Article", "Review", "Meta-Analysis"）。
Semantic Scholar 结果已包含 `citations`（被引次数）和 `influential_citations`（高影响力被引次数）。

无需额外脚本调用，直接使用 Step 2 返回的数据即可。

**可选**：如需补充期刊水平信息（JCR 分区、影响因子），可运行（需要相应 API 访问权限）：
```bash
"C:\Users\refresh\.workbuddy\binaries\python\versions\3.13.12\python.exe" \
  "C:/Users/refresh/.workbuddy/skills/psych-literature-search/scripts/journal_level.py" \
  --journal "[JOURNAL NAME]"
```

未查询到分区信息时，注明"详见 JCR/Scimago"并附链接：
- https://jcr.clarivate.com/jcr/browse-journals
- https://www.scimagojr.com/

---

### Step 4 — 去重与排序

1. 按 DOI 合并 PubMed 与 Semantic Scholar 重复记录（标注 `[双库收录]`）
2. 排序：① 被引次数降序 ② 发表年份降序
3. 保留用户要求数量（默认 15 篇）

---

### Step 5 — 生成结构化表格

按照 `references/output_templates.md` 中的格式，输出以下内容：

**主输出：一体化文献整理表（核心需求）**

输出一张包含所有字段的综合表格，列包括：

| 编号 | 标题（含链接） | 关键词 | 摘要（原文） | 摘要（中文） | 研究变量 | 概念定义 | 操作性定义 | 期刊水平 | 被引次数 |
|------|-------------|--------|-------------|------------|---------|---------|----------|---------|---------|

若一篇文献有多个研究变量，将同一编号的行合并或拆分多行分别描述每个变量。

**辅助四表结构（用于系统化综述报告）：**

- **表一** — 文献概览：标题、作者、年份、期刊、期刊水平、被引、DOI/链接
- **表二** — 关键词与摘要：关键词（双语）、摘要原文、摘要中文翻译
- **表三** — 研究变量定义表：研究变量、概念定义、操作性定义（测量工具/量表）
- **表四** — 研究设计摘要：研究类型、样本量、方法、主要工具、统计方法

**综合分析部分**（可选，系统综述时使用）：
- 核心发现（3-5 条，注明文献编号）
- 研究方法趋势
- 研究空白与未来方向

**APA 7 参考文献列表**

详见 `references/output_templates.md` 中的完整模板。

---

### Step 6 — 交付报告

- 在对话中以 Markdown 形式展示表格
- 如用户需要文件，写入 `[主题]_文献整理_[日期].md` 到工作区
- 可按需提供 Word 兼容格式

---

## 关键参考文件

- `references/api_reference.md` — PubMed E-utilities 与 Semantic Scholar API 端点、字段映射、速率限制
- `references/output_templates.md` — 报告模板与输出格式规则（含所有表格示例）
- `scripts/search_pubmed.py` — PubMed 搜索脚本（无需 API Key）
- `scripts/search_semantic.py` — Semantic Scholar 搜索脚本（无需 API Key）
- `scripts/journal_level.py` — 期刊影响因子/分区查询脚本（可选）

---

## 重要注意事项

- **链接格式**：对每篇文献，优先使用 `https://doi.org/[DOI]` 作为标准链接；无 DOI 时使用 PubMed 链接或 Semantic Scholar 链接。
- **关键词处理**：若文献未显式列出关键词，从摘要和主题标签中推断 3–6 个关键词，用 `(推断)` 标注。双语格式：英文原词 + 中文翻译，如 `cognitive empathy（认知共情）`。
- **研究变量定义提取规则**：
  - 实证研究：列出所有被测量的核心变量（自变量、因变量、中间变量），分别给出概念定义（理论定义）和操作性定义（具体测量工具、量表名称、题目数量、计分方式）。
  - 综述/元分析：列出所综述的主要构念及其测量方式的范围。
  - 若文献未显式给出概念定义，从摘要和背景中推断，标注 `(推断)`。
  - 尽量包含信度信息（如 Cronbach's α）。
- **摘要翻译**：英文摘要提供完整中文翻译（非摘要摘要）；超过 300 词时先压缩至约 200 词再翻译。
- **研究领域范围**：默认搜索覆盖所有学科，若用户明确心理学主题，在 PubMed 中可加 MeSH 限定词，在 Semantic Scholar 中加 `fieldsOfStudy:Psychology` 过滤。
- **摘要缺失处理**：标注 `[摘要不可获取，请查阅原文]`。
- **中文主题**：若主题为中文，先翻译为英文再检索，并在报告中注明翻译。
- **伦理约束**：不尝试下载或访问全文 PDF；仅通过官方 API 获取元数据和摘要。
- **API 密钥安全**：不在最终报告中打印或记录 API 密钥。
