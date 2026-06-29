from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def search_literature(
    keyword: str,
    sources: Optional[null] = None,
    max_results: Optional[int] = 10.0,
    search_type: Optional[str] = "comprehensive",
    use_cache: Optional[bool] = True
) -> Dict[str, Any]:
    """
    多源文献搜索工具。用于查找文献并获取 PMCID。

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
    
    Args:
        keyword: null
        sources: null
        max_results: null
        search_type: null
        use_cache: null
    
    Returns:
        null
    """
    arguments = {
        "keyword": keyword,
        "sources": sources,
        "max_results": max_results,
        "search_type": search_type,
        "use_cache": use_cache
    }
    
    return call_api("1777419072157699", "search_literature", arguments)

def get_article_details(
    pmcid: null,
    sections: Optional[null] = None,
    format: Optional[str] = "markdown"
) -> Dict[str, Any]:
    """
    获取文献全文工具。

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
    
    Args:
        pmcid: null
        sections: null
        format: null
    
    Returns:
        null
    """
    arguments = {
        "pmcid": pmcid,
        "sections": sections,
        "format": format
    }
    
    return call_api("1777419072157699", "get_article_details", arguments)

def get_references(
    identifier: str,
    id_type: Optional[str] = "doi",
    sources: Optional[null] = None,
    max_results: Optional[int] = 20.0,
    include_metadata: Optional[bool] = True
) -> Dict[str, Any]:
    """
    获取参考文献工具。通过文献标识符获取其引用的参考文献列表，支持智能去重。

主要参数：
- identifier: 文献标识符（必填）：DOI、PMID、PMCID
- id_type: 标识符类型（默认doi）：auto/doi/pmid/pmcid
- sources: 数据源列表（默认["europe_pmc", "crossref"]）
- max_results: 最大参考文献数量（默认20，建议20-100）
- include_metadata: 是否包含详细元数据（默认true）

支持的数据源：Europe PMC、CrossRef、PubMed
去重规则：优先按DOI去重，其次按标题去重；按数据源优先级排序
    
    Args:
        identifier: null
        id_type: null
        sources: null
        max_results: null
        include_metadata: null
    
    Returns:
        null
    """
    arguments = {
        "identifier": identifier,
        "id_type": id_type,
        "sources": sources,
        "max_results": max_results,
        "include_metadata": include_metadata
    }
    
    return call_api("1777419072157699", "get_references", arguments)

def get_literature_relations(
    identifier: Optional[null] = None,
    identifiers: Optional[null] = None,
    id_type: Optional[str] = "auto",
    relation_types: Optional[null] = None,
    max_results: Optional[int] = 20.0,
    sources: Optional[null] = None,
    analysis_type: Optional[str] = "basic",
    max_depth: Optional[int] = 1.0
) -> Dict[str, Any]:
    """
    文献关系分析工具。分析文献间的引用关系、相似文献和引用网络。

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
    
    Args:
        identifier: null
        identifiers: null
        id_type: null
        relation_types: null
        max_results: null
        sources: null
        analysis_type: null
        max_depth: null
    
    Returns:
        null
    """
    arguments = {
        "identifier": identifier,
        "identifiers": identifiers,
        "id_type": id_type,
        "relation_types": relation_types,
        "max_results": max_results,
        "sources": sources,
        "analysis_type": analysis_type,
        "max_depth": max_depth
    }
    
    return call_api("1777419072157699", "get_literature_relations", arguments)

def get_journal_quality(
    journal_name: null,
    include_metrics: Optional[null] = None,
    use_cache: Optional[bool] = True,
    sort_by: Optional[null] = None,
    sort_order: Optional[str] = "desc"
) -> Dict[str, Any]:
    """
    期刊质量评估工具。评估期刊的学术质量和影响力指标，集成 EasyScholar + OpenAlex 双数据源。

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
    
    Args:
        journal_name: null
        include_metrics: null
        use_cache: null
        sort_by: null
        sort_order: null
    
    Returns:
        null
    """
    arguments = {
        "journal_name": journal_name,
        "include_metrics": include_metrics,
        "use_cache": use_cache,
        "sort_by": sort_by,
        "sort_order": sort_order
    }
    
    return call_api("1777419072157699", "get_journal_quality", arguments)

