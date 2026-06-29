---
name: 文献搜索工具
description: 基于FastMCP框架开发的专业文献搜索工具，支持多源文献搜索、文献详情获取、参考文献管理、文献关系分析、期刊质量评估和批量结果导出等功能，适用于学术研究和AI助手集成。
version: 1.0.0
---

# 文献搜索工具

基于FastMCP框架开发的专业文献搜索工具，支持多源文献搜索、文献详情获取、参考文献管理、文献关系分析、期刊质量评估和批量结果导出等功能，适用于学术研究和AI助手集成。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| 多源文献搜索工具。用于查找文献并获取 PMCID。

⚠️ 此工具只返回元数据（标题、作者、摘要、PMCID等），不包含全文内容。
   如需获取全文，请使用返回结果中的 pmcid 调用"文献全文"工具。

搜索策略：
- comprehensive: 全面搜索，使用所有可用数据源（并集）
- fast: 快速搜索，只使用主要数据源（Europe PMC、PubMed）
- precise: 精确搜索，只使用权威数据源（PubMed、Europe PMC，交集）
- preprint: 预印本搜索（arXiv）

主要参数：
- keyword: 搜索关键词（必填）
- sources: 数据源列表（可选，默认根据搜索策略自动选择）
- max_results: 每个源的最大结果数（默认10）
- search_type: 搜索策略（默认comprehensive）
- use_cache: 是否使用24小时缓存（默认true）

返回数据包含：标题、作者、期刊、摘要、PMCID、DOI等元数据（不含全文） | `scripts.tools.search_literature` |
| 获取文献全文工具。

前置条件：需要 PMCID 标识符
- 如果您有 PMCID（如 PMC1234567），直接使用此工具
- 如果您只有关键词或标题，请先使用"文献搜索"工具查找并获取 PMCID

主要参数：
- pmcid: PMCID 标识符（必填）：单个或列表[PMC1234567, PMC2345678, ...]
         批量模式最多支持20个 PMCID
- sections: 全文章节控制（可选，默认None获取全部章节）
            None → 获取全部章节（全文）
            ["conclusion", "discussion"] → 只获取指定章节
- format: 全文格式（可选，默认"markdown"）
            "markdown" → Markdown格式（推荐，适合AI处理）
            "xml" → 原始XML格式
            "text" → 纯文本格式

数据源：Europe PMC + PMC 全文数据库
返回数据包含标题、作者、摘要、期刊、发表日期和全文内容

全文功能：
- 按需获取指定格式（默认Markdown）
- 支持按章节提取（如方法、讨论、结论等）
- 优化性能，只转换请求的格式

批量返回结构：
{
    "total": 10,           # 总请求数
    "successful": 8,       # 成功获取数
    "failed": 2,           # 失败数
    "articles": [...],     # 成功的文章列表（含全文）
    "fulltext_stats": {    # 全文统计
        "has_pmcid": 8,    # 有 PMCID 数量
        "fulltext_fetched": 8  # 成功获取全文数量
    }
}

支持的章节名称：
- methods（方法）: methods, methodology, materials and methods
- introduction（引言）: introduction, intro, background
- results（结果）: results, findings
- discussion（讨论）: discussion
- conclusion（结论）: conclusion, conclusions
- abstract（摘要）: abstract, summary
- references（参考文献）: references, bibliography | `scripts.tools.get_article_details` |
| 获取参考文献工具。通过文献标识符获取其引用的参考文献列表，支持智能去重。

主要参数：
- identifier: 文献标识符（必填）：DOI、PMID、PMCID
- id_type: 标识符类型（默认doi）：auto/doi/pmid/pmcid
- sources: 数据源列表（默认["europe_pmc", "crossref"]）
- max_results: 最大参考文献数量（默认20，建议20-100）
- include_metadata: 是否包含详细元数据（默认true）

支持的数据源：Europe PMC、CrossRef、PubMed
去重规则：优先按DOI去重，其次按标题去重；按数据源优先级排序 | `scripts.tools.get_references` |
| 文献关系分析工具。分析文献间的引用关系、相似文献和引用网络。

关系类型：
- references: 该文献引用的参考文献
- similar: 相似文献
- citing: 引用该文献的文献

主要参数：
- identifiers: 文献标识符（单个或列表）：DOI、PMID、PMCID
- id_type: 标识符类型（默认auto）：auto/doi/pmid/pmcid
- relation_types: 关系类型列表（默认全部）：["references", "similar", "citing"]
- max_results: 每种关系类型最大结果数（默认20）
- analysis_type: 分析类型（默认basic）：basic/comprehensive/network
- max_depth: 分析深度（默认1）

分析模式：
- 单个文献：传入单个标识符
- 批量分析：传入标识符列表 + analysis_type="basic"
- 网络分析：传入标识符列表 + analysis_type="network" | `scripts.tools.get_literature_relations` |
| 期刊质量评估工具。评估期刊的学术质量和影响力指标，集成 EasyScholar + OpenAlex 双数据源。

支持的指标：
EasyScholar 提供：impact_factor（影响因子）、quartile（SCI分区 Q1-Q4）、jci（JCI指数）、cas_zone（中科院分区）、cas_zone_top（TOP期刊标识）
OpenAlex 提供：h_index（h指数）、citation_rate（2年引用率）、cited_by_count（总引用数）、works_count（总文章数）、i10_index（i10指数）

主要参数：
- journal_name: 期刊名称（单个或列表）
- include_metrics: 返回的指标列表（默认["impact_factor", "quartile", "jci"]）
- use_cache: 是否使用24小时缓存（默认true）
- sort_by: 排序字段，仅批量查询有效（默认null）：impact_factor/quartile/jci
- sort_order: 排序顺序，仅批量查询有效（默认desc）：desc降序/asc升序

使用示例：单个期刊查询、批量期刊查询、批量查询并排序、指定返回指标 | `scripts.tools.get_journal_quality` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.search_literature
工具描述：多源文献搜索工具。用于查找文献并获取 PMCID。

⚠️ 此工具只返回元数据（标题、作者、摘要、PMCID等），不包含全文内容。
   如需获取全文，请使用返回结果中的 pmcid 调用"文献全文"工具。

搜索策略：
- comprehensive: 全面搜索，使用所有可用数据源（并集）
- fast: 快速搜索，只使用主要数据源（Europe PMC、PubMed）
- precise: 精确搜索，只使用权威数据源（PubMed、Europe PMC，交集）
- preprint: 预印本搜索（arXiv）

主要参数：
- keyword: 搜索关键词（必填）
- sources: 数据源列表（可选，默认根据搜索策略自动选择）
- max_results: 每个源的最大结果数（默认10）
- search_type: 搜索策略（默认comprehensive）
- use_cache: 是否使用24小时缓存（默认true）

返回数据包含：标题、作者、期刊、摘要、PMCID、DOI等元数据（不含全文）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|keyword|string|true| |null|
|sources|null|false| |null|
|max_results|integer|false|10.0|null|
|search_type|string|false|"comprehensive"|null|
|use_cache|boolean|false|true|null|

---

## scripts.tools.get_article_details
工具描述：获取文献全文工具。

前置条件：需要 PMCID 标识符
- 如果您有 PMCID（如 PMC1234567），直接使用此工具
- 如果您只有关键词或标题，请先使用"文献搜索"工具查找并获取 PMCID

主要参数：
- pmcid: PMCID 标识符（必填）：单个或列表[PMC1234567, PMC2345678, ...]
         批量模式最多支持20个 PMCID
- sections: 全文章节控制（可选，默认None获取全部章节）
            None → 获取全部章节（全文）
            ["conclusion", "discussion"] → 只获取指定章节
- format: 全文格式（可选，默认"markdown"）
            "markdown" → Markdown格式（推荐，适合AI处理）
            "xml" → 原始XML格式
            "text" → 纯文本格式

数据源：Europe PMC + PMC 全文数据库
返回数据包含标题、作者、摘要、期刊、发表日期和全文内容

全文功能：
- 按需获取指定格式（默认Markdown）
- 支持按章节提取（如方法、讨论、结论等）
- 优化性能，只转换请求的格式

批量返回结构：
{
    "total": 10,           # 总请求数
    "successful": 8,       # 成功获取数
    "failed": 2,           # 失败数
    "articles": [...],     # 成功的文章列表（含全文）
    "fulltext_stats": {    # 全文统计
        "has_pmcid": 8,    # 有 PMCID 数量
        "fulltext_fetched": 8  # 成功获取全文数量
    }
}

支持的章节名称：
- methods（方法）: methods, methodology, materials and methods
- introduction（引言）: introduction, intro, background
- results（结果）: results, findings
- discussion（讨论）: discussion
- conclusion（结论）: conclusion, conclusions
- abstract（摘要）: abstract, summary
- references（参考文献）: references, bibliography
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|pmcid|null|true| |null|
|sections|null|false| |null|
|format|string|false|"markdown"|null|

---

## scripts.tools.get_references
工具描述：获取参考文献工具。通过文献标识符获取其引用的参考文献列表，支持智能去重。

主要参数：
- identifier: 文献标识符（必填）：DOI、PMID、PMCID
- id_type: 标识符类型（默认doi）：auto/doi/pmid/pmcid
- sources: 数据源列表（默认["europe_pmc", "crossref"]）
- max_results: 最大参考文献数量（默认20，建议20-100）
- include_metadata: 是否包含详细元数据（默认true）

支持的数据源：Europe PMC、CrossRef、PubMed
去重规则：优先按DOI去重，其次按标题去重；按数据源优先级排序
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|identifier|string|true| |null|
|id_type|string|false|"doi"|null|
|sources|null|false| |null|
|max_results|integer|false|20.0|null|
|include_metadata|boolean|false|true|null|

---

## scripts.tools.get_literature_relations
工具描述：文献关系分析工具。分析文献间的引用关系、相似文献和引用网络。

关系类型：
- references: 该文献引用的参考文献
- similar: 相似文献
- citing: 引用该文献的文献

主要参数：
- identifiers: 文献标识符（单个或列表）：DOI、PMID、PMCID
- id_type: 标识符类型（默认auto）：auto/doi/pmid/pmcid
- relation_types: 关系类型列表（默认全部）：["references", "similar", "citing"]
- max_results: 每种关系类型最大结果数（默认20）
- analysis_type: 分析类型（默认basic）：basic/comprehensive/network
- max_depth: 分析深度（默认1）

分析模式：
- 单个文献：传入单个标识符
- 批量分析：传入标识符列表 + analysis_type="basic"
- 网络分析：传入标识符列表 + analysis_type="network"
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|identifier|null|false| |null|
|identifiers|null|false| |null|
|id_type|string|false|"auto"|null|
|relation_types|null|false| |null|
|max_results|integer|false|20.0|null|
|sources|null|false| |null|
|analysis_type|string|false|"basic"|null|
|max_depth|integer|false|1.0|null|

---

## scripts.tools.get_journal_quality
工具描述：期刊质量评估工具。评估期刊的学术质量和影响力指标，集成 EasyScholar + OpenAlex 双数据源。

支持的指标：
EasyScholar 提供：impact_factor（影响因子）、quartile（SCI分区 Q1-Q4）、jci（JCI指数）、cas_zone（中科院分区）、cas_zone_top（TOP期刊标识）
OpenAlex 提供：h_index（h指数）、citation_rate（2年引用率）、cited_by_count（总引用数）、works_count（总文章数）、i10_index（i10指数）

主要参数：
- journal_name: 期刊名称（单个或列表）
- include_metrics: 返回的指标列表（默认["impact_factor", "quartile", "jci"]）
- use_cache: 是否使用24小时缓存（默认true）
- sort_by: 排序字段，仅批量查询有效（默认null）：impact_factor/quartile/jci
- sort_order: 排序顺序，仅批量查询有效（默认desc）：desc降序/asc升序

使用示例：单个期刊查询、批量期刊查询、批量查询并排序、指定返回指标
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|journal_name|null|true| |null|
|include_metrics|null|false| |null|
|use_cache|boolean|false|true|null|
|sort_by|null|false| |null|
|sort_order|string|false|"desc"|null|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据