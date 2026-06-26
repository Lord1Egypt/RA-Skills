---
name: scholar-search
description: Unified academic search across arXiv and Semantic Scholar. Supports topic search, latest preprints, paper/author lookup, citation analysis, and structured output from core endpoints.
metadata: {"openclaw":{"requires":{"anyBins":["python","python3"],"env":["S2_API_KEY"]},"primaryEnv":"S2_API_KEY"}}
---

# **scholar-search**

## **概述**

本 skill 通过统一的命令行脚本 `scripts/scholar-search.py` 封装 arXiv 和 Semantic Scholar API，支持学术论文检索、详情拉取、引用网络扩展与作者轨迹分析。

---

## **前置条件**
- Python
- 所需依赖：`requests`
  ```bash
  pip install requests
  ```
- 环境变量要求：
  - `S2_API_KEY` - Semantic Scholar API 密钥（必需；优先从进程环境变量读取）
- 当我在对话中直接提供 Semantic Scholar API Key 时，必须先写入：
  ```python
  python scripts/set_s2_api_key.py --api-key "<我提供的key>"
  ```
- 写入策略：`S2_API_KEY` 已存在则覆盖，不存在则自动追加到 `scripts/.env`。
- 读取策略：优先读进程环境变量 `S2_API_KEY`，若未设置则回退读取 `scripts/.env`。
- 命令占位符约定：
  - 技能目录根路径（`skills/scholar-search`）。
  - 统一脚本路径写法：、`scripts/scholar-search.py`。

---

## **可用工具**
- `scripts/scholar-search.py`：主检索脚本，执行 arXiv + Semantic Scholar 联合检索与结果整理。
- `scripts/set_s2_api_key.py`：写入或覆盖 `.env` 中的 `S2_API_KEY`，用于配置 Semantic Scholar API Key。

## **详细操作手册**
- `references/semantic-scholar-api-reference.md`：Semantic Scholar API 的端点、参数与字段参考，用于核对调用细节。
- `references/arxiv-api-reference.md`：arXiv API 的查询语法与参数说明，用于核对 arXiv 检索细节。

---

# **工作流**

---

## 1) **解读我的需求**
先提取并标准化以下约束：
1. 查询实体：关键词、paper_id、author_id、DOI、arXiv ID、作者姓名，学科等等。
2. 时间和过滤：year、venue、publicationTypes、fieldsOfStudy、cat 分类
3. 规模目标：目标条数
4. 输出语言：中文
5. 类型偏好：是否只要 conference/期刊、是否只要 2024 年后等硬条件

输出语言决策：
- 如果我的查询包含“中文”“用中文”“中文回答”“总结成中文”等词 -> 强制全部输出中文。
- 如果我的查询是纯英文或学术术语为主 -> 保持论文标题/作者/会议期刊原文，分析描述用中文。
- 其他情况默认中文，并在描述字段中保持中文表达。

---

## 2) **可用的搜索引擎与使用**

### **arxiv搜索引擎**
**功能概述**  
面向 arXiv 预印本的统一检索入口，支持关键词/作者/分类/时间过滤、ID 精确拉取、分页、排序。  
**典型用途**：  
- 追踪最新预印本（按提交时间倒序）  
- 按学科/作者做前沿扫描  
- 用 arXiv ID 快速获取单篇或多篇元数据（标题、摘要、作者、PDF链接等）

**核心参数速查**（建议优先掌握这6个，覆盖 95% 场景）

| 参数          | 作用                              | 常用值/格式示例                              | 必填 | 建议/约束                  |
|---------------|-----------------------------------|----------------------------------------------|------|----------------------------|
| `search_query` | 查询表达式（标题/作者/摘要/分类/全字段） | `cat:cs.CL AND all:multimodal`<br>`au:goodfellow AND ti:gan` | 否   | 支持 `ti:`, `au:`, `abs:`, `cat:`, `all:` 前缀；AND/OR/ANDNOT/短语"" |
| `id_list`     | 精确拉取 arXiv ID（逗号分隔，可带版本 vN） | `0704.0001,cond-mat/0207270v1`              | 否   | 与 search_query 可组合做过滤；优先用此拿单篇 |
| `start`       | 分页起点（0-based）               | `0`, `10`, `100`                             | 否   | 默认 0                     |
| `max_results` | 单次返回条数                      | `10`, `50`, `200`                            | 否   | 默认 10；上限 30000，建议 ≤2000/次 |
| `sortBy`      | 排序字段                          | `relevance`（默认，模糊搜推荐）<br>`submittedDate`（新论文优先）<br>`lastUpdatedDate` | 否   | 与最新预印本最常用         |
| `sortOrder`   | 排序方向                          | `descending`（新→旧）<br>`ascending`         | 否   | 默认 relevance 时无关      |

**时间过滤语法**（常用但非必备）  
在 `search_query` 中加：  
`submittedDate:[YYYYMMDDTTTT TO YYYYMMDDTTTT]`  
示例：`submittedDate:[202501010000 TO 202603082359]`（2025年1月1日到2026年3月8日）

**快速上手案例**
```bash
# 1. 最新10篇 cs.CL 多模态相关预印本（推荐默认用法）
python scripts/scholar-search.py --source arxiv --params '{"search_query":"cat:cs.CL AND all:multimodal","start":0,"max_results":10,"sortBy":"submittedDate","sortOrder":"descending"}'

# 2. 指定作者 + 近一年论文（时间区间过滤）
python scripts/scholar-search.py --source arxiv --params '{"search_query":"au:goodfellow AND submittedDate:[202503010000 TO 202603082359]","max_results":20}'

# 3. 精确拉取单篇或多篇（最快、最稳定）
python scripts/scholar-search.py --source arxiv --params '{"id_list":"2501.12345,2409.09876v2"}'

# 4. ID 列表 + 额外过滤（例如只看 cs.AI 中的）
python scripts/scholar-search.py --source arxiv --params '{"id_list":"2408.00001,2407.12345","search_query":"cat:cs.AI"}'
```

**高级/注意事项**（仅在需要时深入）  
- search_query + id_list 组合：id_list 为主，search_query 作二次过滤。   
- 限流：**每 3 秒 1 次请求**，单连接；
- 完整语法、错误码、返回字段详解 → `references/arxiv-api-reference.md`
**决策提示**
- 想最新/热门 → 用 `sortBy=submittedDate` / `lastUpdatedDate` + `descending`  
- 模糊主题搜 → `search_query` + `sortBy=relevance`  
- 已知 ID → 优先 `id_list`，速度最快、准确最高  
- 需要时间范围 → 加 `submittedDate:[...]`  
- 结果太多/太少 → 调整 max_results 或细化 search_query（如加 cat: / au:）
> 高级用法参考：`references/arxiv-api-reference.md`


### **semantic scholar 搜索引擎**
**功能概述**  
面向 Semantic Scholar Academic Graph 的检索入口，提供论文/作者元数据、引用网络、引用上下文等。  
**典型用途**：  
- 主题/关键词搜高影响力论文（带 citationCount 排序）  
- 论文详情 + PDF/开放获取判断  
- 沿引用链扩展（citations/references）  
- 作者轨迹分析（author/{id}/papers）  
- 标题精确匹配或术语上下文片段定位

**核心参数速查**（覆盖 90% 场景）
| 参数                  | 作用                               | 常用示例/格式                              | 必填/约束                          |
|-----------------------|------------------------------------|--------------------------------------------|------------------------------------|
| `endpoint`            | 目标 API 路径                      | `paper/search`, `paper/{paper_id}`, `citations` 等 | 必填                               |
| `query`               | 搜索词（plain text，无特殊语法）   | `"machine learning"`, `transformer`        | paper/search、match、author/search 必填 |
| `fields`              | 返回字段白名单（逗号分隔，支持点号嵌套） | `paperId,title,abstract,citationCount,openAccessPdf,url,authors` | 可选；不传返回最小数据             |
| `limit` / `offset`    | 分页（offset 从 0 开始）           | `limit:50`, `offset:0`                     | 大多端点 limit 默认 100，常见 max 100–1000（见下方关键约束） |
| `publicationDateOrYear` / `year` | 时间过滤                     | `2024:2026`, `year:2025`                   | 可选                               |
| `minCitationCount` / `venue` / `fieldsOfStudy` / `publicationTypes` | 过滤高引/特定会议/领域/类型 | `minCitationCount:50`, `venue:NeurIPS`     | 可选                               |

**关键约束（精简版）**
- `paper/search`：`limit <= 100` 且 `offset + limit < 1000`。
- `author/search`：`limit <= 1000` 且 `offset + limit < 10000`。
- `paper/{id}/references`、`paper/{id}/citations`、`author/{id}/papers`：`limit <= 1000`。
- `paper/autocomplete`：必须有 `query`，不要依赖 `limit`。
- `snippet/search`：必须有 `query`；建议不传 `fields`；`limit <= 1000`；`offset` 不稳定不建议依赖。
- 以上规则在脚本参数校验中会优先拦截；完整细则与返回字段定义见 `references/semantic-scholar-api-reference.md`。

**快速上手案例**
```bash
# 1. 主题检索（推荐默认入口，带关键字段）
python scripts/scholar-search.py --source semantic_scholar --endpoint paper/search --params '{"query":"large language model reasoning","limit":15,"offset":0,"fields":"paperId,title,year,authors,abstract,citationCount,venue,openAccessPdf,url,externalIds"}'

# 2. 标题精确匹配（单条最准）
python scripts/scholar-search.py --source semantic_scholar --endpoint paper/search/match --params '{"query":"Attention Is All You Need","fields":"paperId,title,authors,year,abstract,url,venue"}'

# 3. 论文详情（已知任意 ID）
python scripts/scholar-search.py --source semantic_scholar --endpoint paper/arXiv:2312.17485 --params '{"fields":"title,abstract,authors,citationCount,openAccessPdf,url"}'

# 4. 引用扩展（看谁引用了这篇）
python scripts/scholar-search.py --source semantic_scholar --endpoint paper/PMID:12345678/citations --params '{"limit":20,"offset":0,"fields":"citingPaper.paperId,citingPaper.title,citingPaper.year,citingPaper.citationCount"}'

# 5. 作者轨迹（某作者所有论文，按时间过滤）
python scripts/scholar-search.py --source semantic_scholar --endpoint author/1741101/papers --params '{"limit":30,"offset":0,"publicationDateOrYear":"2023:2026","fields":"title,year,venue,citationCount"}'
```

---

## 3) **结果质量检查与继续检索条件**
满足任一条件时，继续检索 1 轮：
1. 数量不足（例如 `< 3`）
2. 与我的主题偏离明显
3. 关键字段缺失较多（标题、ID、来源链接、摘要）

结束检索条件：
1. 数量达到目标或可接受范围
2. 主题匹配度高
3. 继续检索收益低

补充策略：先在同一数据源内改写查询重试 1 次；仍不足再切到另一源补充 1 次。

### **相关性分层**（输出前必须执行）
基于 query 与论文标题/摘要/TL;DR 的语义匹配程度分层：
- **高相关**：直接研究 query 主题本身，或以 DeepSeek 作为核心对象/核心方法（优先详细输出）。
- **中相关**：将 DeepSeek 作为主要对比基线、实验对象或关键组成部分。
- **弱相关**：仅在实验、附录或背景中提及 DeepSeek。

排序优先级：
1. 相关性（高 > 中 > 弱）
2. 时间（新到旧）
3. 引用数（高到低，未知置后）

必须停止并输出结果的条件（任一满足即终止）：
1. 已获取 >= 目标数量的合格论文（合格 = 有标题 + paperId + year + abstract/TL;DR 至少一项）。
2. 本轮与上一轮相比，新论文重复率 > 70% 或没有明显新信息。
3. 已连续执行 3 轮检索（含 query 改写重试）。
4. 当前结果平均 citationCount < 3 且 year 均在近 3 年内（领域过新或 query 过窄）。
5. 我明确表示“够了”“停止搜索”。

---

## 4) **输出要求（最终向我输出的内容格式要求）**
1. 每篇论文必须按以下结构输出，缺一项即判失败。
2. 每篇开头必须是独立一行（前后空一行）：`-----------`
3. 标题必须是一级标题：`# {序号}. **论文完整标题**`
4. 若有 TL;DR，标题下一行输出：`TL;DR: {文本} — 来自 {来源}`；无则整行删除。
5. 元数据固定三行、固定顺序、字段名必须加粗：
   **论文信息**：
   **来源**：{venue/journal/arXiv} | **发表/更新日期**：{日期} | **引用数**：{数字或未知} | **影响力引用**：{数字或未知} | **开放获取**：是/否/未知

   **链接**：[Semantic Scholar]({url}) | **PDF**：[PDF]({pdf_url})
   （无 PDF 时删除 `| **PDF**...` 整项，不得写"无/未知"）

6. 作者行：`**作者**（前3位 + et al.）：{A, B, C et al.}`
7. 领域行：`**领域**：{领域1, 领域2}`（无则整行删除）
8. 必须包含：
   `### 研究内容`（1–2句，仅基于 abstract/tldr/summary，禁止推断）
   `### 摘要关键点`（2–4条；若不足2条，补"原始信息有限。"）
9. 可选字段只能放在：
   **可选额外信息**：
   - **被引趋势**：...
   - **出版类型**：...
   - **外部ID**：...
   （此块可整体省略）

### **输出限制**
1. 严禁任何开场白、总结、结尾、过渡语。
2. 严禁改字段名、改顺序、压缩结构、合并段落。
3. 输出必须直接从第一篇 `-----------` 开始。
4. 不可将原本单篇信息详细的论文只输出少部分信息。

### **示例输出（仅供参考）**
```markdown

-----------

# 1. **Hierarchical Token Pruning for Efficient Vision-Language Reasoning**
TL;DR: 通过分层裁剪视觉与文本 token，在保持精度的同时显著降低推理开销 — 来自 Semantic TL;DR

**论文信息**：
**来源**：arXiv | **发表/更新日期**：2026-01-09 | **引用数**：未知 | **影响力引用**：未知 | **开放获取**：是

**链接**：[Semantic Scholar](https://www.semanticscholar.org/paper/Hierarchical-Token-Pruning-Example/abcdef123456) | **PDF**：[PDF](https://arxiv.org/pdf/2601.00999)

**作者**（前3位 + et al.）：Mina Park, David Lin, Q. Herrera et al.
**领域**：Computer Science, Vision-Language Models

### 研究内容
该研究提出分层 token pruning 框架，在不同网络深度动态移除低贡献 token。实验显示该方法在多项视觉问答与检索任务上实现更优的效率-性能折中。

### 摘要关键点
- 设计了跨层一致性的 token 重要性评分机制。
- 在多个基准上显著减少 FLOPs 与延迟，同时维持接近基线的准确率。
- 提供消融实验，验证不同裁剪率与层级策略的影响。
```

---

## 5) 失败处理
1. API 失败：回显脚本返回的 `error` 字段（含 HTTP 状态码、错误信息、已尝试参数）
2. 无结果：给出可执行的 query 改写建议（同义词、上位词、放宽过滤）
3. 参数错误：明确指出错误参数并给出修正后的完整调用命令
4. 字段缺失：标注"未知/缺失"，不得补写未返回信息
5. 429/配额处理顺序：
   - 若返回 429 -> 当前脚本直接返回错误并停止，不自动重试。
   - 建议：重试 1 次（间隔 2-5 秒）或减小 `limit` 后重试。
   - 若错误包含 `quota` 或 `rate limit` -> 直接告知我的配额已用尽，建议稍后重试或切换 arXiv。
6. 结果过少模板：
   - “当前结果较少（仅 X 篇），建议：① 去掉 venue 限制；② 用上位词替换关键词；③ 切换到 arXiv 获取最新预印本。”。

---

## 6) 执行硬约束
1. **每轮检索只做最小必要请求，优先复用已获取结果**
2. **输出前必须完成字段真实性校验**
3. 不使用未验证端点，不引用未在响应中出现的数据
4. 若我给出硬过滤（如 `year>=2024`、`conference only`），必须优先编码到参数中再发起请求
