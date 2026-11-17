"""scripts/clean_sources.py - 干净源预灌注册表 + 供给器（v1）。

设计目标（见 clean-sources-plan.md）：替用户多做一步，把高质量、无 key 无 API 的国内外
干净源提前备好灌进库，使调用方**零配置**即得论文级/权威级干净答案，不必自己手写 web_fetch。

契约修正（重要）：既有 `web_fetch` 的真实语义是 `web_fetch(url: str) -> str(html)`（单 URL
兜底抓取器，被 finance/github/academic/searxng 调用），本模块**不替换**该契约。
`build_clean_fetch(cfg, ...)` 产出的是一个**「按 query 扇出、返回 docs 列表的干净源供给器」**
`Callable[[str], List[Dict]]`，由 orchestrate.retrieve 在 `web_fetch is None 且
clean_sources.enabled` 时把产出的 docs 并入质量层。显式 `web_fetch=` 仍最高优先（调用方注入）；
`clean_sources.enabled=false` 时行为与修改前完全一致。

设计红线：库而非产品、零 key、零成本开箱、不绑 LLM、不 spawn 新进程；CN 沙箱下国外/部分国内源
可能偏慢或被墙——每个源内置可达性探针，超时/不可达**静默跳过**，绝不拖垮整次检索。

源质量：`source_type` 驱动 SBA 打分（gov/academic/media…），`quality`(A/B) 作注册表元数据与
`describe_clean_sources()` 报告用，二者协同、`quality` 不强行改写 score.py。
"""

import json
import os
import re
import threading
import urllib.error
import urllib.parse
import urllib.request
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List, Optional

# ----------------------------------------------------------------------------
# 1) 干净源注册表
# ----------------------------------------------------------------------------
# 每条字段：
#   id, name         : 标识 / 展示名
#   category         : 分组（驱动档位与开关）
#   method           : serp（网页搜索 URL）/ rest（结构化 URL）/ rest_adapter（专用适配）
#   access           : keyless / keyless_meta（仅元数据，全文需 keyed 升级）/ keyed（opt-in）
#   source_type      : 驱动 SBA（gov/academic/media/vendor/unknown…）
#   quality          : A/B 元数据
#   url_template     : 含 {q} 的请求 URL（method=serp/rest 用）；rest_adapter 由适配器拼
#   engine_id        : 若源已在 config.engines 中，复用 search.fetch（method=serp_cfg）
#   response         : json / html
#   json_items       : JSON 中结果列表路径（rest + response=json 用）
#   item_map         : {doc字段: JSON字段} 简单映射（rest 用）
#   adapter          : 命名专用适配器（rest_adapter / 已知 API 精解）
#   key_env          : keyed 源的 env 名（opt-in）
#   gate             : 可选门控（如 searxng 需 config.searxng.url）
#   tags / tiers     : 标签 / 所属档位集合
#
# 说明：名单为「预灌」交付物，覆盖方案全部 v1 源。rest 类优先走 item_map 通用抽取，
# 已知 API 形状（OpenAlex/Crossref/SemanticScholar/EuropePMC/ClinicalTrials/CourtListener）
# 走精解适配器；其余 rest 走通用 JSON/HTML 抽取（best-effort，抓不到即静默跳过）。
CLEAN_SOURCES: List[Dict[str, Any]] = [
    # ---- 国际通用引擎（来自 multi-search-engine，已在 config.engines.global）----
    {
        "id": "Google",
        "name": "Google",
        "category": "intl_engines",
        "method": "serp_cfg",
        "engine_id": "Google",
        "access": "keyless",
        "source_type": "unknown",
        "quality": "B",
        "tags": ["通用", "英文"],
        "tiers": ["lite", "standard", "full"],
    },
    {
        "id": "GoogleHK",
        "name": "Google 香港",
        "category": "intl_engines",
        "method": "serp_cfg",
        "engine_id": "GoogleHK",
        "access": "keyless",
        "source_type": "unknown",
        "quality": "B",
        "tags": ["通用", "中文国际"],
        "tiers": ["lite", "standard", "full"],
    },
    {
        "id": "DuckDuckGo",
        "name": "DuckDuckGo",
        "category": "intl_engines",
        "method": "serp_cfg",
        "engine_id": "DuckDuckGo",
        "access": "keyless",
        "source_type": "unknown",
        "quality": "B",
        "tags": ["隐私", "通用"],
        "tiers": ["lite", "standard", "full"],
    },
    {
        "id": "Yahoo",
        "name": "Yahoo",
        "category": "intl_engines",
        "method": "serp_cfg",
        "engine_id": "Yahoo",
        "access": "keyless",
        "source_type": "unknown",
        "quality": "B",
        "tags": ["通用"],
        "tiers": ["lite", "standard", "full"],
    },
    {
        "id": "Startpage",
        "name": "Startpage",
        "category": "intl_engines",
        "method": "serp_cfg",
        "engine_id": "Startpage",
        "access": "keyless",
        "source_type": "unknown",
        "quality": "B",
        "tags": ["隐私", "Google结果"],
        "tiers": ["lite", "standard", "full"],
    },
    {
        "id": "Brave",
        "name": "Brave",
        "category": "intl_engines",
        "method": "serp_cfg",
        "engine_id": "Brave",
        "access": "keyless",
        "source_type": "unknown",
        "quality": "B",
        "tags": ["隐私", "通用"],
        "tiers": ["lite", "standard", "full"],
    },
    {
        "id": "Ecosia",
        "name": "Ecosia",
        "category": "intl_engines",
        "method": "serp_cfg",
        "engine_id": "Ecosia",
        "access": "keyless",
        "source_type": "unknown",
        "quality": "B",
        "tags": ["通用", "环保"],
        "tiers": ["lite", "standard", "full"],
    },
    {
        "id": "Qwant",
        "name": "Qwant",
        "category": "intl_engines",
        "method": "serp_cfg",
        "engine_id": "Qwant",
        "access": "keyless",
        "source_type": "unknown",
        "quality": "B",
        "tags": ["隐私", "欧洲"],
        "tiers": ["lite", "standard", "full"],
    },
    {
        "id": "WolframAlpha",
        "name": "WolframAlpha",
        "category": "intl_engines",
        "method": "serp_cfg",
        "engine_id": "WolframAlpha",
        "access": "keyless",
        "source_type": "unknown",
        "quality": "B",
        "tags": ["计算", "事实", "数据"],
        "tiers": ["lite", "standard", "full"],
    },
    # ---- 通用参考 ----
    {
        "id": "Wikipedia",
        "name": "Wikipedia",
        "category": "reference",
        "method": "serp_cfg",
        "engine_id": "Wikipedia",
        "access": "keyless",
        "source_type": "academic",
        "quality": "A",
        "tags": ["百科", "事实"],
        "tiers": ["lite", "standard", "full"],
    },
    {
        "id": "Wikidata",
        "name": "Wikidata",
        "category": "reference",
        "method": "serp_cfg",
        "engine_id": "Wikidata",
        "access": "keyless",
        "source_type": "academic",
        "quality": "A",
        "tags": ["结构化知识"],
        "tiers": ["lite", "standard", "full"],
    },
    {
        "id": "InternetArchive",
        "name": "Internet Archive",
        "category": "reference",
        "method": "rest",
        "url_template": (
            "https://archive.org/advancedsearch.php?q={q}&fl[]=identifier"
            "&fl[]=title&rows=5&output=json"
        ),
        "access": "keyless",
        "source_type": "academic",
        "quality": "A",
        "response": "json",
        "json_items": "response.docs",
        "item_map": {"url": "identifier", "title": "title"},
        "tags": ["存档", "书籍", "数据集"],
        "tiers": ["lite", "standard", "full"],
    },
    # ---- 学术 API（多 keyless REST）----
    {
        "id": "OpenAlex",
        "name": "OpenAlex",
        "category": "academic_api",
        "method": "rest",
        "url_template": (
            "https://api.openalex.org/works?search={q}&per-page=5"
            "&mailto=signal-search@example.com"
        ),
        "access": "keyless",
        "source_type": "academic",
        "quality": "A",
        "response": "json",
        "adapter": "_adapt_openalex",
        "tags": ["文献", "2.5亿", "CC0"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "Crossref",
        "name": "Crossref",
        "category": "academic_api",
        "method": "rest",
        "url_template": "https://api.crossref.org/works?query={q}&rows=5",
        "access": "keyless",
        "source_type": "academic",
        "quality": "A",
        "response": "json",
        "adapter": "_adapt_crossref",
        "tags": ["DOI", "1.67亿"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "SemanticScholar",
        "name": "Semantic Scholar",
        "category": "academic_api",
        "method": "rest",
        "url_template": (
            "https://api.semanticscholar.org/graph/v1/paper/search?query={q}"
            "&limit=5&fields=title,url,abstract,year"
        ),
        "access": "keyless",
        "source_type": "academic",
        "quality": "A",
        "response": "json",
        "adapter": "_adapt_semanticscholar",
        "tags": ["引用图", "2亿"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "PubMed",
        "name": "PubMed",
        "category": "academic_api",
        "method": "rest",
        "url_template": (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed"
            "&term={q}&retmode=json&retmax=5"
        ),
        "access": "keyless",
        "source_type": "academic",
        "quality": "A",
        "response": "json",
        "adapter": "_adapt_pubmed",
        "tags": ["生物医学"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "EuropePMC",
        "name": "Europe PMC",
        "category": "academic_api",
        "method": "rest",
        "url_template": (
            "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}"
            "&format=json&pageSize=5"
        ),
        "access": "keyless",
        "source_type": "academic",
        "quality": "A",
        "response": "json",
        "adapter": "_adapt_europepmc",
        "tags": ["4600万文献"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "bioRxiv",
        "name": "bioRxiv",
        "category": "academic_api",
        "method": "rest",
        "url_template": "https://api.biorxiv.org/details/{q}/0",
        "access": "keyless",
        "source_type": "academic",
        "quality": "A",
        "response": "json",
        "adapter": "_adapt_biorxiv",
        "tags": ["预印本"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "arXiv",
        "name": "arXiv",
        "category": "academic_api",
        "method": "serp_cfg",
        "engine_id": "arXiv",
        "access": "keyless",
        "source_type": "academic",
        "quality": "A",
        "tags": ["预印本"],
        "tiers": ["standard", "full"],
    },
    # ---- 权威 / 标准参考 ----
    {
        "id": "W3C",
        "name": "W3C",
        "category": "authoritative",
        "method": "serp",
        "url_template": "https://www.w3.org/Search/query.php?q={q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "html",
        "tags": ["Web标准"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "IETF",
        "name": "IETF RFC",
        "category": "authoritative",
        "method": "serp",
        "url_template": "https://www.rfc-editor.org/search?q={q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "html",
        "tags": ["互联网协议"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "WHATWG",
        "name": "WHATWG",
        "category": "authoritative",
        "method": "serp",
        "url_template": "https://html.spec.whatwg.org/multipage/#toc",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "html",
        "tags": ["HTML活标准"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "MDN",
        "name": "MDN",
        "category": "authoritative",
        "method": "serp",
        "url_template": "https://developer.mozilla.org/search?q={q}",
        "access": "keyless",
        "source_type": "vendor",
        "quality": "A",
        "response": "html",
        "tags": ["Web技术参考"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "Unicode",
        "name": "Unicode",
        "category": "authoritative",
        "method": "serp",
        "url_template": "https://home.unicode.org/?s={q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "html",
        "tags": ["字符集"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "TC39",
        "name": "TC39",
        "category": "authoritative",
        "method": "serp",
        "url_template": "https://github.com/tc39/proposals/search?q={q}",
        "access": "keyless",
        "source_type": "vendor",
        "quality": "A",
        "response": "html",
        "tags": ["JS语言标准"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "OpenAPI",
        "name": "OpenAPI",
        "category": "authoritative",
        "method": "serp",
        "url_template": "https://spec.openapis.org/search?q={q}",
        "access": "keyless",
        "source_type": "vendor",
        "quality": "A",
        "response": "html",
        "tags": ["API规范"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "GitHub",
        "name": "GitHub",
        "category": "authoritative",
        "method": "serp_cfg",
        "engine_id": "GitHub",
        "access": "keyless",
        "source_type": "vendor",
        "quality": "A",
        "tags": ["代码", "开源"],
        "tiers": ["standard", "full"],
    },
    # ---- 国外行业 keyless ----
    {
        "id": "SEC_EDGAR",
        "name": "SEC EDGAR",
        "category": "industry_keyless",
        "method": "rest",
        "url_template": "https://efts.sec.gov/LATEST/search-index?q={q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "json",
        "adapter": "_adapt_edgar",
        "tags": ["金融", "美股申报"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "WorldBank",
        "name": "World Bank Open Data",
        "category": "industry_keyless",
        "method": "rest",
        "url_template": "https://api.worldbank.org/v2/search/{q}?format=json",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "json",
        "adapter": "_adapt_worldbank",
        "tags": ["宏观", "发展"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "ClinicalTrials",
        "name": "ClinicalTrials.gov v2",
        "category": "industry_keyless",
        "method": "rest",
        "url_template": "https://clinicaltrials.gov/api/v2/studies?query.term={q}&pageSize=5",
        "access": "keyless",
        "source_type": "academic",
        "quality": "A",
        "response": "json",
        "adapter": "_adapt_clinicaltrials",
        "tags": ["医疗", "临床试验"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "openFDA",
        "name": "openFDA",
        "category": "industry_keyless",
        "method": "rest",
        "url_template": "https://api.fda.gov/drug/label.json?search={q}&limit=5",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "json",
        "adapter": "_adapt_openfda",
        "tags": ["药品", "不良事件"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "CourtListener",
        "name": "CourtListener",
        "category": "industry_keyless",
        "method": "rest",
        "url_template": (
            "https://www.courtlistener.com/api/rest/v4/search/?q={q}" "&type=o&format=json"
        ),
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "json",
        "adapter": "_adapt_courtlistener",
        "tags": ["法律", "判例"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "DataEuropa",
        "name": "data.europa.eu",
        "category": "industry_keyless",
        "method": "rest",
        "url_template": "https://data.europa.eu/api/hub/search/datasets?q={q}&limit=5",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "json",
        "adapter": "_adapt_dataeuropa",
        "tags": ["欧盟开放数据"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "NOAA",
        "name": "NOAA",
        "category": "industry_keyless",
        "method": "rest",
        "url_template": "https://api.weather.gov/alerts?q={q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "json",
        "adapter": "_adapt_noaa",
        "tags": ["气象", "海洋"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "USGS",
        "name": "USGS",
        "category": "industry_keyless",
        "method": "rest",
        "url_template": "https://api.water.usgs.gov/observations?q={q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "json",
        "tags": ["地质", "地球科学"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "NASA",
        "name": "NASA (data.nasa.gov)",
        "category": "industry_keyless",
        "method": "rest",
        "url_template": "https://data.nasa.gov/resource/gh9g-ax6g.json?q={q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "json",
        "adapter": "_adapt_nasa",
        "tags": ["航天", "地球科学"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "IMF",
        "name": "IMF DataMapper",
        "category": "industry_keyless",
        "method": "rest",
        "url_template": "https://www.imf.org/external/datamapper/api/v1/{q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "json",
        "tags": ["经济", "宏观"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "OECD",
        "name": "OECD SDMX",
        "category": "industry_keyless",
        "method": "rest",
        "url_template": "https://sdmx.oecd.org/public/rest/data/OECD.SDD.DSD_EO@DF_EO_ALL?q={q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "json",
        "tags": ["经济", "OECD"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "WHO",
        "name": "WHO GHO OData",
        "category": "industry_keyless",
        "method": "rest",
        "url_template": (
            "https://ghoapi.azureedge.net/api/Indicator?" "$filter=substringof('{q}',IndicatorName)"
        ),
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "json",
        "adapter": "_adapt_who",
        "tags": ["卫生", "指标"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "CDC",
        "name": "CDC Socrata",
        "category": "industry_keyless",
        "method": "rest",
        "url_template": "https://data.cdc.gov/resource.json?q={q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "json",
        "tags": ["公卫", "美国"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "ECDC",
        "name": "ECDC",
        "category": "industry_keyless",
        "method": "rest",
        "url_template": "https://opendata.ecdc.europa.eu/api/v1/{q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "json",
        "tags": ["欧洲疾控"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "UKDataGov",
        "name": "UK data.gov.uk",
        "category": "industry_keyless",
        "method": "rest",
        "url_template": "https://www.data.gov.uk/api/3/action/package_search?q={q}&rows=5",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "json",
        "adapter": "_adapt_ukdatagov",
        "tags": ["英国政府", "开放数据"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "RePEc",
        "name": "RePEc·IDEAS",
        "category": "industry_keyless",
        "method": "serp",
        "url_template": "https://ideas.repec.org/cgi-bin/htsearch?words={q}",
        "access": "keyless",
        "source_type": "academic",
        "quality": "A",
        "response": "html",
        "tags": ["经济", "文献"],
        "tiers": ["standard", "full"],
    },
    # ---- 隐私 / 独立引擎补充 ----
    {
        "id": "Mojeek",
        "name": "Mojeek",
        "category": "privacy_extra",
        "method": "serp_cfg",
        "engine_id": "Mojeek",
        "access": "keyless",
        "source_type": "unknown",
        "quality": "B",
        "tags": ["独立索引"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "MetaGer",
        "name": "MetaGer",
        "category": "privacy_extra",
        "method": "serp",
        "url_template": "https://metager.de/en/search?q={q}",
        "access": "keyless",
        "source_type": "unknown",
        "quality": "B",
        "response": "html",
        "tags": ["德国隐私", "元索引"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "SearxNG",
        "name": "SearxNG",
        "category": "privacy_extra",
        "method": "serp",
        "url_template": "{searxng_url}/search?q={q}",
        "access": "keyless",
        "source_type": "unknown",
        "quality": "A",
        "response": "html",
        "gate": "searxng",
        "tags": ["自托管", "聚合"],
        "tiers": ["standard", "full"],
    },
    # ---- 国内权威（free，本版即进 v1）----
    # ⑦a 标准
    {
        "id": "StdOpen",
        "name": "国家标准全文公开系统",
        "category": "cn_official",
        "method": "serp",
        "url_template": "https://openstd.samr.gov.cn/bzgk/gb/index?q={q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "html",
        "tags": ["标准", "全文"],
        "tiers": ["standard", "full"],
    },
    # ⑦b 法律 / 政府
    {
        "id": "FlkNPC",
        "name": "国家法律法规数据库",
        "category": "cn_official",
        "method": "serp",
        "url_template": "https://flk.npc.gov.cn/fl.html#/keyword/{q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "html",
        "tags": ["法律", "全文"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "Gsxt",
        "name": "国家企业信用信息公示系统",
        "category": "cn_official",
        "method": "serp",
        "url_template": "https://www.gsxt.gov.cn/corp-query-search-1.html?key={q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "html",
        "tags": ["企业", "信用"],
        "tiers": ["standard", "full"],
    },
    # ⑦c 政府 / 统计 / 科研主管
    {
        "id": "GovCN",
        "name": "中国政府网",
        "category": "cn_official",
        "method": "serp_cfg",
        "engine_id": "GovCN",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "tags": ["政策", "公报"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "NBS",
        "name": "国家统计局",
        "category": "cn_official",
        "method": "rest_adapter",
        "adapter": "_adapt_nbs",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "tags": ["统计", "宏观经济"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "NSFC",
        "name": "国家自然科学基金委",
        "category": "cn_official",
        "method": "serp",
        "url_template": "https://www.nsfc.gov.cn/search?q={q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "B",
        "response": "html",
        "tags": ["科研资助"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "CAS",
        "name": "中国科学院",
        "category": "cn_official",
        "method": "serp",
        "url_template": "https://www.cas.cn/search/?q={q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "B",
        "response": "html",
        "tags": ["科研", "成果"],
        "tiers": ["standard", "full"],
    },
    # ⑦d 社科 / 中文学术（元数据型 best-effort）
    {
        "id": "NCpssd",
        "name": "国家哲学社会科学文献中心",
        "category": "cn_official",
        "method": "serp",
        "url_template": "https://ncpssd.org/axSearch#gsc.tab=0&q={q}",
        "access": "keyless_meta",
        "source_type": "academic",
        "quality": "A",
        "response": "html",
        "tags": ["中文学术", "题录"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "CNKI",
        "name": "中国知网",
        "category": "cn_official",
        "method": "serp_cfg",
        "engine_id": "CNKI",
        "access": "keyless_meta",
        "source_type": "academic",
        "quality": "B",
        "tags": ["中文学术", "摘要题录"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "WanFang",
        "name": "万方数据",
        "category": "cn_official",
        "method": "serp_cfg",
        "engine_id": "WanFang",
        "access": "keyless_meta",
        "source_type": "academic",
        "quality": "B",
        "tags": ["中文学术", "摘要"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "NSTL",
        "name": "国家科技图书文献中心",
        "category": "cn_official",
        "method": "serp",
        "url_template": "https://www.nstl.gov.cn/search.html?q={q}",
        "access": "keyless_meta",
        "source_type": "academic",
        "quality": "A",
        "response": "html",
        "tags": ["科技文献", "题录"],
        "tiers": ["standard", "full"],
    },
    # ⑦e 医疗 / 公共卫生
    {
        "id": "NMPA",
        "name": "国家药监局",
        "category": "cn_official",
        "method": "serp",
        "url_template": "https://www.nmpa.gov.cn/WS04/CL2042/",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "html",
        "tags": ["药品", "医疗器械"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "ChiCTR",
        "name": "中国临床试验注册中心",
        "category": "cn_official",
        "method": "serp",
        "url_template": "http://www.chictr.org.cn/searchproj.html?searchType=all&keywords={q}",
        "access": "keyless",
        "source_type": "academic",
        "quality": "A",
        "response": "html",
        "tags": ["临床试验"],
        "tiers": ["standard", "full"],
    },
    {
        "id": "NHC",
        "name": "国家卫生健康委员会",
        "category": "cn_official",
        "method": "serp",
        "url_template": "http://www.nhc.gov.cn/search/{q}.html",
        "access": "keyless",
        "source_type": "gov",
        "quality": "B",
        "response": "html",
        "tags": ["卫生政策"],
        "tiers": ["standard", "full"],
    },
    # ⑦f 科学数据
    {
        "id": "NSIDC",
        "name": "国家科技基础条件平台",
        "category": "cn_official",
        "method": "serp",
        "url_template": "https://www.escience.org.cn/search?q={q}",
        "access": "keyless",
        "source_type": "gov",
        "quality": "A",
        "response": "html",
        "tags": ["科学数据"],
        "tiers": ["standard", "full"],
    },
    # ---- AI 原生搜索 API（keyed，opt-in 留门，默认关）----
    {
        "id": "Tavily",
        "name": "Tavily",
        "category": "ai_search",
        "method": "rest",
        "url_template": "https://api.tavily.com/search?query={q}",
        "access": "keyed",
        "key_env": "TAVILY_API_KEY",
        "source_type": "vendor",
        "quality": "A",
        "response": "json",
        "tags": ["Agent搜索", "引用富"],
        "tiers": [],
    },
    {
        "id": "Exa",
        "name": "Exa",
        "category": "ai_search",
        "method": "rest",
        "url_template": "https://api.exa.ai/search?q={q}",
        "access": "keyed",
        "key_env": "EXA_API_KEY",
        "source_type": "vendor",
        "quality": "A",
        "response": "json",
        "tags": ["神经语义检索"],
        "tiers": [],
    },
    {
        "id": "Perplexity",
        "name": "Perplexity",
        "category": "ai_search",
        "method": "rest",
        "url_template": "https://api.perplexity.ai/chat/completions",
        "access": "keyed",
        "key_env": "PERPLEXITY_API_KEY",
        "source_type": "vendor",
        "quality": "A",
        "response": "json",
        "tags": ["带引用答案"],
        "tiers": [],
    },
    {
        "id": "BraveAPI",
        "name": "Brave Search API",
        "category": "ai_search",
        "method": "rest",
        "url_template": "https://api.search.brave.com/res/v1/web/search?q={q}",
        "access": "keyed",
        "key_env": "BRAVE_API_KEY",
        "source_type": "unknown",
        "quality": "A",
        "response": "json",
        "tags": ["独立索引API"],
        "tiers": [],
    },
]

# 档位 → 包含的分组（full 在 privacy 已入 standard 后等价于 standard；保留扩展位）
CLEAN_TIERS_PRESET: Dict[str, List[str]] = {
    "lite": ["intl_engines", "reference"],
    "standard": [
        "intl_engines",
        "reference",
        "academic_api",
        "authoritative",
        "industry_keyless",
        "cn_official",
        "privacy_extra",
        "private_kb",
    ],
    "full": [
        "intl_engines",
        "reference",
        "academic_api",
        "authoritative",
        "industry_keyless",
        "cn_official",
        "privacy_extra",
        "private_kb",
    ],
}


# ----------------------------------------------------------------------------
# 2) 默认 HTTP 抓取器（可注入，供测试 monkeypatch / 调用方覆盖）
# ----------------------------------------------------------------------------
_DEFAULT_HEADERS = {
    "User-Agent": "Signal-Search/1.0 (+https://github.com/signal-search; clean-sources)",
    "Accept": "application/json, text/html, */*",
}


def _default_fetcher(url: str, timeout: float = 4.0) -> tuple:
    """返回 (content: bytes_or_str, content_type: str)；失败抛异常由调用方捕获跳过。"""
    req = urllib.request.Request(url, headers=_DEFAULT_HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        ctype = resp.headers.get("Content-Type", "") or ""
    try:
        text = data.decode("utf-8")
    except Exception:
        text = data
    return text, ctype


# ----------------------------------------------------------------------------
# 3) 解析适配器
# ----------------------------------------------------------------------------
def _inv_index_to_text(inv: Optional[dict]) -> str:
    """OpenAlex abstract_inverted_index → 文本（best-effort）。"""
    if not isinstance(inv, dict):
        return ""
    out = []
    for word, positions in inv.items():
        for p in positions or []:
            out.append((p, word))
    out.sort()
    return " ".join(w for _, w in out)


def _norm_url(u: Optional[str]) -> Optional[str]:
    if not u:
        return None
    u = str(u).strip()
    if u.startswith("//"):
        u = "https:" + u
    if u.startswith("/"):
        return None  # 相对路径，无 host，跳过
    if u.startswith("http://") or u.startswith("https://"):
        return u
    return "https://" + u


def _adapt_openalex(src, data, q):
    out = []
    for it in data.get("results") or []:
        url = it.get("doi") or it.get("id")
        url = _norm_url(url)
        if not url:
            continue
        abstract = _inv_index_to_text(it.get("abstract_inverted_index"))
        out.append(
            {
                "url": url,
                "title": it.get("display_name") or it.get("title") or "",
                "snippet": abstract[:300] or it.get("display_name", ""),
            }
        )
    return out


def _adapt_crossref(src, data, q):
    out = []
    for it in (data.get("message") or {}).get("items") or []:
        doi = it.get("DOI")
        url = _norm_url("https://doi.org/" + doi) if doi else None
        if not url:
            continue
        title = (it.get("title") or [""])[0] if it.get("title") else ""
        out.append({"url": url, "title": title, "snippet": (it.get("abstract") or "")[:300]})
    return out


def _adapt_semanticscholar(src, data, q):
    out = []
    for it in data.get("data") or []:
        url = _norm_url(
            it.get("url")
            or it.get("paperId")
            and "https://www.semanticscholar.org/paper/" + it["paperId"]
        )
        if not url:
            continue
        out.append(
            {
                "url": url,
                "title": it.get("title") or "",
                "snippet": (it.get("abstract") or "")[:300],
            }
        )
    return out


def _adapt_pubmed(src, data, q):
    out = []
    for pid in (data.get("esearchresult") or {}).get("idlist") or []:
        url = "https://pubmed.ncbi.nlm.nih.gov/" + str(pid)
        out.append({"url": url, "title": "PubMed:" + str(pid), "snippet": ""})
    return out


def _adapt_europepmc(src, data, q):
    out = []
    for it in (data.get("resultList") or {}).get("result") or []:
        doi = it.get("doi")
        url = _norm_url("https://doi.org/" + doi) if doi else _norm_url(it.get("id"))
        if not url:
            continue
        out.append(
            {
                "url": url,
                "title": it.get("title") or "",
                "snippet": (it.get("abstractText") or "")[:300],
            }
        )
    return out


def _adapt_biorxiv(src, data, q):
    out = []
    for it in data.get("collection") or []:
        doi = it.get("doi")
        url = _norm_url("https://doi.org/" + doi) if doi else None
        if not url:
            continue
        out.append(
            {"url": url, "title": it.get("title") or "", "snippet": it.get("abstract") or ""}
        )
    return out


def _adapt_edgar(src, data, q):
    out = []
    for it in (data.get("hits") or {}).get("hits") or []:
        url = _norm_url(it.get("url"))
        if not url:
            continue
        out.append(
            {
                "url": url,
                "title": it.get("display_names")
                or it.get("_source", {}).get("display_names")
                or "",
                "snippet": "",
            }
        )
    return out


def _adapt_worldbank(src, data, q):
    out = []
    for it in data or []:
        if not isinstance(it, dict):
            continue
        url = _norm_url(it.get("url"))
        if not url:
            continue
        out.append({"url": url, "title": it.get("name") or "", "snippet": ""})
    return out


def _adapt_clinicaltrials(src, data, q):
    out = []
    for it in data.get("studies") or []:
        ident = (it.get("protocolSection") or {}).get("identificationModule") or {}
        nct = ident.get("nctId")
        if not nct:
            continue
        out.append(
            {
                "url": "https://clinicaltrials.gov/study/" + nct,
                "title": ident.get("briefTitle") or "",
                "snippet": "",
            }
        )
    return out


def _adapt_openfda(src, data, q):
    out = []
    for it in data.get("results") or []:
        url = (
            _norm_url(it.get("openfda", {}).get("url") and it["openfda"]["url"][0])
            if isinstance(it, dict)
            else None
        )
        if not url:
            url = _norm_url("https://api.fda.gov/drug/label.json?search=" + q)
        if not url:
            continue
        out.append(
            {
                "url": url,
                "title": (
                    (it.get("openfda", {}).get("brand_name") or [""])[0]
                    if isinstance(it, dict)
                    else ""
                ),
                "snippet": "",
            }
        )
    return out


def _adapt_courtlistener(src, data, q):
    out = []
    for it in data.get("results") or []:
        url = _norm_url(it.get("absolute_url"))
        if not url:
            continue
        out.append({"url": url, "title": it.get("caseName") or "", "snippet": ""})
    return out


def _adapt_dataeuropa(src, data, q):
    out = []
    try:
        for it in data.get("result", {}).get("results", []):
            url = _norm_url(it.get("url"))
            if not url:
                continue
            out.append({"url": url, "title": it.get("title") or "", "snippet": ""})
    except Exception:
        pass
    return out


def _adapt_noaa(src, data, q):
    out = []
    for f in data.get("features") or []:
        props = f.get("properties") or {}
        url = _norm_url(props.get("id") and "https://api.weather.gov/alerts/" + props["id"])
        if not url:
            continue
        out.append(
            {"url": url, "title": props.get("event") or "", "snippet": props.get("headline") or ""}
        )
    return out


def _adapt_nasa(src, data, q):
    out = []
    for it in data or []:
        if not isinstance(it, dict):
            continue
        url = _norm_url(it.get("url") or it.get("id"))
        if not url:
            continue
        out.append({"url": url, "title": it.get("title") or "", "snippet": ""})
    return out


def _adapt_who(src, data, q):
    out = []
    for it in data.get("value") or []:
        url = _norm_url(
            it.get("IndicatorLink")
            or it.get("IndicatorCode")
            and "https://www.who.int/data/gho/data/indicators/" + it["IndicatorCode"]
        )
        if not url:
            continue
        out.append({"url": url, "title": it.get("IndicatorName") or "", "snippet": ""})
    return out


def _adapt_ukdatagov(src, data, q):
    out = []
    for it in (data.get("result") or {}).get("results") or []:
        url = _norm_url(
            it.get("url") or it.get("id") and "https://www.data.gov.uk/dataset/" + it["id"]
        )
        if not url:
            continue
        out.append({"url": url, "title": it.get("title") or "", "snippet": ""})
    return out


def _adapt_nbs(src, query, cfg, fetcher):
    """国家统计局 rest_adapter：仍免 key，走专用适配（best-effort，失败返回 []）。

    国家统计局是结构化查询 API（非搜索 URL），真实形状需按指标代码拼，这里做轻量探测：
    命中即返回结构化占位 doc，证明 rest_adapter 通路可用；实际指标查询由调用方经 web_fetch= 深化。
    """
    try:
        url = "https://data.stats.gov.cn/easyquery.htm?cn=C01&zb=A0101&sj=last"
        content, _ = fetcher(url, timeout=4.0)
        text = content.decode("utf-8") if isinstance(content, (bytes, bytearray)) else content
        if not (text or "").strip():
            return []  # 无内容即跳过，不产空占位 doc
        title = "国家统计局（结构化统计数据，需指标代码深化）"
        snippet = (text or "")[:200]
        return [{"url": "https://data.stats.gov.cn/", "title": title, "snippet": snippet}]
    except Exception:
        return []


# 命名适配器表
_NAMED_ADAPTERS = {
    "_adapt_openalex": _adapt_openalex,
    "_adapt_crossref": _adapt_crossref,
    "_adapt_semanticscholar": _adapt_semanticscholar,
    "_adapt_pubmed": _adapt_pubmed,
    "_adapt_europepmc": _adapt_europepmc,
    "_adapt_biorxiv": _adapt_biorxiv,
    "_adapt_edgar": _adapt_edgar,
    "_adapt_worldbank": _adapt_worldbank,
    "_adapt_clinicaltrials": _adapt_clinicaltrials,
    "_adapt_openfda": _adapt_openfda,
    "_adapt_courtlistener": _adapt_courtlistener,
    "_adapt_dataeuropa": _adapt_dataeuropa,
    "_adapt_noaa": _adapt_noaa,
    "_adapt_nasa": _adapt_nasa,
    "_adapt_who": _adapt_who,
    "_adapt_ukdatagov": _adapt_ukdatagov,
    "_adapt_nbs": _adapt_nbs,
}


# ----------------------------------------------------------------------------
# 4) 通用抽取（serp / 通用 JSON）
# ----------------------------------------------------------------------------
_URL_HREF = re.compile(r'href=["\'](https?://[^"\']+?)["\']', re.I)
_LINK_TITLE = re.compile(r'<a[^>]+href=["\'](https?://[^"\']+?)["\'][^>]*>(.*?)</a>', re.I | re.S)


def _extract_serp(html: str, base_url: str) -> List[Dict[str, str]]:
    """从 SERP HTML 轻量抽取结果链接 + 锚文本（best-effort）。"""
    out = []
    seen = set()
    for href, label in _LINK_TITLE.findall(html or ""):
        u = _norm_url(href)
        if not u or u in seen or u.rstrip("/") == base_url.rstrip("/"):
            continue
        seen.add(u)
        label = re.sub(r"<[^>]+>", "", label).strip()
        out.append({"url": u, "title": label[:120], "snippet": ""})
        if len(out) >= 5:
            break
    if not out:
        for href in _URL_HREF.findall(html or ""):
            u = _norm_url(href)
            if not u or u in seen:
                continue
            seen.add(u)
            out.append({"url": u, "title": "", "snippet": ""})
            if len(out) >= 5:
                break
    return out


def _get_path(data: dict, path: str):
    cur = data
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        elif isinstance(cur, list) and part.isdigit() and int(part) < len(cur):
            cur = cur[int(part)]
        else:
            return None
    return cur


def _extract_json_generic(src: dict, data: dict) -> List[Dict[str, str]]:
    """通用 JSON 抽取：优先 item_map，否则尽力从列表元素取 url/title/snippet。"""
    items = []
    if src.get("json_items"):
        items = _get_path(data, src["json_items"]) or []
    if not isinstance(items, list):
        items = []
    out = []
    for it in items[:5]:
        if not isinstance(it, dict):
            continue
        m = src.get("item_map") or {}
        url = _norm_url(it.get(m.get("url", "url")) or it.get("url"))
        if not url:
            # 退而求其次：任何含 http 的字段
            for k, v in it.items():
                if isinstance(v, str) and v.startswith("http"):
                    url = _norm_url(v)
                    break
        if not url:
            continue
        title = it.get(m.get("title", "title")) or it.get("title") or ""
        snippet = (
            it.get(m.get("snippet", "snippet")) or it.get("snippet") or it.get("abstract") or ""
        )
        if isinstance(snippet, (dict, list)):
            snippet = ""
        out.append({"url": url, "title": str(title)[:160], "snippet": str(snippet)[:300]})
    return out


# ----------------------------------------------------------------------------
# 4.5) 自定义（私有 / 内部）源：配置驱动接入，零 Python 代码
# ----------------------------------------------------------------------------
# 设计：调用方在 config.clean_sources.custom_sources 写一条源定义（URL 模板 + JSON 路径映射），
# 即可把自有知识库 / 公司内部资料库接进同一质量管线（SBA/M51/去重/token 预算），与 65 个
# 公开源平等打分。这是相对「纯网页搜索产品」的核心差异化：你的私有源不是外挂，而是
# 一等公民。详见 README「接入你自己的知识库」。
#
# 源定义字段（均为 config 内声明，无需改代码）：
#   id, name        : 标识 / 展示名（必填）
#   category        : 默认为 "private_kb"（已纳入 standard/full 档）
#   method          : "rest"（默认；通用 JSON/HTML 抽取）
#   url_template    : 请求 URL，含 {q}（查询，自动编码）；可选 {token}（来自 key_env 的鉴权值）
#   response        : "json"（默认）/ "html"
#   json_items      : JSON 中结果数组路径（如 "results" / "data.hits"）
#   item_map        : {doc字段: JSON字段}，支持 url/title/snippet（默认即同名）
#   key_env         : 设了即变 keyed opt-in（env 注入 key 才激活）；{token} 从此 env 取值
#   auth            : "bearer" 时把 {token} 作为 Bearer 值拼进 URL（常见 ?token= / &apikey=）
#   topics          : 主题词表（如 ["corp"]），命中即被路由选中；缺省仅靠 force_include 命中
#   force_include   : 默认 True（你主动接的源就该被打，非噪声）；设 False 则仅按 topics/档位命中
#   quality         : 默认 "B"；内部权威源可标 "A"
#   source_type     : 驱动 SBA，默认 "internal"
def _normalize_custom(src: dict, warnings: Optional[List[str]] = None) -> dict:
    """填充自定义源默认值；返回新 dict，不改动入参。

    warnings：可选收集器，用于记录配置边界问题（不抛、不误伤正常源）。
    """
    s = dict(src)
    s.setdefault("category", "private_kb")
    s.setdefault("method", "rest")
    s.setdefault("response", "json")
    s.setdefault("source_type", "internal")
    s.setdefault("quality", "B")
    s.setdefault("force_include", True)  # 私有源是用户主动接的，默认必打（非噪声源）
    if s.get("key_env") and s.get("access") is None:
        s["access"] = "keyed"
    s.setdefault("access", "keyless")
    if s.get("topics") is None:
        s["topics"] = []
    # 边界：rest 源 url_template 缺 {q} 且未声明 static → 所有查询抓同一静态地址，
    # 属典型配置错误（静默返回错误结果）。仅告警，不抛、不阻断正常 static 源。
    if (
        s.get("method") == "rest"
        and "{q}" not in (s.get("url_template") or "")
        and not s.get("static")
    ):
        if warnings is not None:
            warnings.append(
                f"自定义源 {s.get('id')!r} 的 url_template 缺 {{q}} 且未声明 static，"
                f"将始终抓取同一静态地址（所有查询返回相同结果）——通常配置有误。"
            )
    return s


def _custom_sources(cfg: dict, warnings: Optional[List[str]] = None) -> List[dict]:
    """从 config.clean_sources.custom_sources 取经归一化的自定义源列表。

    warnings：透传给 _normalize_custom，收集配置边界提示。
    """
    raw = (cfg.get("clean_sources") or {}).get("custom_sources") or []
    return [_normalize_custom(s, warnings) for s in raw if isinstance(s, dict) and s.get("id")]


def _safe_url_format(template: str, q: str, src: dict) -> str:
    """安全填充 url_template：{q}（必填，已编码）→ 查询；{token}（可选）→ key_env 的 env 值。
    用字符串替换而非 str.format，避免模板含其它 {} 占位符时抛 KeyError。"""
    out = template.replace("{q}", q)
    if "{token}" in out:
        tok = ""
        env = src.get("key_env")
        if env:
            tok = os.environ.get(env) or ""
        out = out.replace("{token}", tok)
    return out


# ----------------------------------------------------------------------------
# 5) 单源抓取
# ----------------------------------------------------------------------------
def _cfg_engines(cfg: dict) -> Dict[str, dict]:
    out = {}
    for grp in ("cn", "global", "academic"):
        for e in (cfg.get("engines") or {}).get(grp, []):
            out[e["id"]] = e
    for dom, lst in (cfg.get("engines") or {}).get("vertical", {}).items():
        for e in lst:
            out[e["id"]] = e
    return out


def _fetch_one(
    src: dict, query: str, cfg: dict, fetcher, timeout: float, engines_index: dict = None
) -> List[Dict[str, Any]]:
    """抓单源 → docs 列表（失败返回 []，不抛）。"""
    try:
        q = urllib.parse.quote(query)
        method = src.get("method")
        if method == "serp_cfg":
            eid = src.get("engine_id")
            from search import fetch as _search_fetch

            docs = _search_fetch(
                eid, query, cfg=cfg
            )  # cfg 作关键字传参：保留调用方注入、避免 search.fetch 内重读磁盘（D1）
            out = []
            engines = engines_index or _cfg_engines(cfg)
            e = engines.get(eid)
            for d in docs:
                u = d.get("url")
                if not u and e:
                    u = e["search_url"].format(q=query)
                if not u:
                    continue
                out.append(
                    {
                        "url": u,
                        "title": d.get("title") or src["name"],
                        "snippet": (d.get("raw_html") or "")[:300],
                    }
                )
            return out
        if method == "serp":
            url = src["url_template"].format(
                q=q, searxng_url=(cfg.get("searxng") or {}).get("url", "")
            )
            content, ctype = fetcher(url, timeout=timeout)
            html = content.decode("utf-8") if isinstance(content, (bytes, bytearray)) else content
            return _extract_serp(html, url)
        if method == "rest_adapter":
            adapter = _NAMED_ADAPTERS.get(src.get("adapter"))
            if not adapter:
                return []
            return adapter(src, query, cfg, fetcher)
        if method == "rest":
            url = _safe_url_format(src["url_template"], q, src)
            content, ctype = fetcher(url, timeout=timeout)
            is_json = ("json" in (ctype or "").lower()) or str(content).lstrip().startswith("{")
            if is_json:
                data = json.loads(
                    content.decode("utf-8") if isinstance(content, (bytes, bytearray)) else content
                )
                adapter = _NAMED_ADAPTERS.get(src.get("adapter"))
                if adapter:
                    return adapter(src, data, query)
                return _extract_json_generic(src, data)
            html = content.decode("utf-8") if isinstance(content, (bytes, bytearray)) else content
            return _extract_serp(html, url)
    except Exception:
        return []
    return []


def _source_active(src: dict, tier: str, cfg: dict, keys: Optional[dict]) -> bool:
    """判断单源是否应参与本次扇出。

    keyed 源走「纯 key 驱动」opt-in：只要 env / keys 中注入了对应 key 即激活，
    不受 tier 分组与 category.enabled 门控（category 仅对非 keyed 源起开关联动作用）。
    这保证「keyed AI 搜索 API 默认关、env 注入即活」的契约成立。
    """
    cat = src.get("category")
    access = src.get("access")
    if access == "keyed":
        # opt-in：纯 key 驱动，跳过 tier 分组检查（tiers=[] 也照常可激活）
        env = src.get("key_env")
        if not env:
            return False
        if keys and keys.get(env):
            return True
        if os.environ.get(env):
            return True
        return False
    groups = CLEAN_TIERS_PRESET.get(tier, CLEAN_TIERS_PRESET["standard"])
    if cat not in groups:
        return False
    cat_cfg = ((cfg.get("clean_sources") or {}).get("categories") or {}).get(cat) or {}
    # 非 keyed：受 category 开关联动门控
    if cat_cfg.get("enabled") is False:
        return False
    # 门控（如 SearxNG 需 config.searxng.url）
    if src.get("gate") == "searxng":
        if not ((cfg.get("searxng") or {}).get("url")):
            return False
    return True


# ----------------------------------------------------------------------------
# 5.5) 源路由层（按需选源，避免全扇出爆炸）
# ----------------------------------------------------------------------------
# 设计依据（联网调研，见 README「源路由」小节）：
#   - RAGRoute (arXiv:2502.19280)：over-selecting 稀释相关性、引入噪声；需轻量路由器选子集。
#   - Learning to Route (arXiv:2510.02388)：规则路由胜过静态全连；盲连多源反而降质。
#   - Agent-Level MoE（agentpatternscatalog / programmer.ie）：最朴素路由器即 Python 关键词
#     规则（零 key、零延迟、确定性），top-1 或 top-k + 通用兜底。
#   - 元搜索 DB 选择（CORI / ReDDE / GlOSS）：每查询仅选可能相关的子库，大量库对单查询无用。
# 默认启发式路由器（零 key、零 LLM）；调用方可通过 router_fn= 注入 LLM 路由器（调用方注入契约）。
#
# 主题词表：query 关键词 → 主题 token（与 _SOURCE_TOPICS 对齐）。权重越高，该主题越被选中。
TOPIC_KEYWORDS: Dict[str, List[tuple]] = {
    "academic": [
        ("论文", 2),
        ("文献", 2),
        ("doi", 2),
        ("引用", 1),
        ("研究", 1),
        ("预印本", 2),
        ("arxiv", 2),
        ("期刊", 2),
        ("综述", 2),
        ("学术", 2),
        ("书评", 1),
        ("paper", 1),
        ("article", 1),
        ("citation", 1),
        ("preprint", 2),
        ("journal", 1),
        ("research", 1),
        ("scholar", 1),
    ],
    "dev": [
        ("html", 2),
        ("css", 2),
        ("javascript", 2),
        ("js", 2),
        ("web标准", 2),
        ("web 标准", 2),
        ("规范", 1),
        ("rfc", 2),
        ("api规范", 2),
        ("unicode", 2),
        ("tc39", 2),
        ("mdn", 2),
        ("前端", 1),
        ("后端", 1),
        ("编程", 1),
        ("代码规范", 1),
        ("html5", 1),
        ("css3", 1),
        ("standard", 1),
        ("spec", 1),
        ("ecmascript", 2),
    ],
    "finance": [
        ("股价", 2),
        ("股票", 2),
        ("财报", 2),
        ("主力", 2),
        ("净流入", 2),
        ("市值", 2),
        ("市盈率", 2),
        ("营收", 2),
        ("净利润", 2),
        ("金融", 1),
        ("基金", 1),
        ("etf", 1),
        ("上市公司", 2),
        ("证券", 2),
        ("年报", 1),
        ("stock", 1),
        ("earnings", 1),
        ("revenue", 1),
        ("market cap", 1),
        ("pe ratio", 1),
        ("10-k", 2),
        ("sec", 1),
    ],
    "macro": [
        ("gdp", 2),
        ("通胀", 2),
        ("通货膨胀", 2),
        ("cpi", 2),
        ("宏观经济", 2),
        ("经济增长", 2),
        ("失业率", 2),
        ("世界经济", 1),
        ("imf", 2),
        ("oecd", 2),
        ("经济", 1),
        ("economy", 1),
        ("inflation", 1),
        ("unemployment", 1),
        ("货币政策", 1),
        ("gdp增长", 2),
    ],
    "health": [
        ("疾病", 2),
        ("临床", 2),
        ("药物", 2),
        ("疫苗", 2),
        ("流行病学", 2),
        ("who", 2),
        ("cdc", 2),
        ("医疗", 1),
        ("症状", 1),
        ("治疗", 1),
        ("临床试验", 2),
        ("药品", 1),
        ("公卫", 2),
        ("disease", 1),
        ("clinical", 1),
        ("drug", 1),
        ("vaccine", 1),
        ("trial", 1),
        ("epidemic", 1),
        ("health", 1),
        ("fda", 2),
        ("药监", 2),
    ],
    "legal": [
        ("法律", 2),
        ("法规", 2),
        ("法条", 2),
        ("判例", 2),
        ("法院", 2),
        ("立法", 2),
        ("合规", 2),
        ("司法解释", 2),
        ("法规数据库", 2),
        ("legal", 1),
        ("law", 1),
        ("statute", 1),
        ("case law", 1),
        ("regulation", 1),
        ("court", 1),
    ],
    "gov": [
        ("统计", 2),
        ("人口", 2),
        ("普查", 2),
        ("社融", 1),
        ("开放数据", 1),
        ("政府数据", 1),
        ("statistics", 1),
        ("population", 1),
        ("census", 1),
        ("government", 1),
        ("dataset", 1),
        ("欧盟数据", 1),
        ("英国政府", 1),
        ("美国政府", 1),
    ],
    "climate": [
        ("气候", 2),
        ("气象", 2),
        ("卫星", 2),
        ("气温", 2),
        ("碳排放", 2),
        ("海洋", 2),
        ("地质", 2),
        ("地球科学", 1),
        ("climate", 1),
        ("weather", 1),
        ("satellite", 1),
        ("carbon", 1),
        ("earth", 1),
        ("space", 1),
        ("nasa", 2),
        ("noaa", 2),
        ("usgs", 1),
    ],
    "privacy": [("隐私", 2), ("匿名", 1), ("privacy", 1), ("独立索引", 1)],
    "cn_official": [
        ("国标", 2),
        ("国家标准", 2),
        ("国家法律法规", 2),
        ("中国企业", 1),
        ("信用记录", 1),
        ("中文文献", 1),
        ("中文学术", 1),
        ("科技文献", 1),
        ("科学数据", 1),
        ("国家药监", 1),
        ("卫健委", 1),
        ("自然科学基金", 1),
        ("中科院", 1),
    ],
    "corp": [("公司信用", 2), ("企业信用", 2), ("工商", 1), ("企业信息", 1)],
}

# 源 → 意图主题（细粒度）。未列出的源回退到其 category 作为主题。
# 仅 industry_keyless / cn_official 需要细粒度（其余「分类即主题」）。
_SOURCE_TOPICS: Dict[str, List[str]] = {
    # industry_keyless
    "SEC_EDGAR": ["finance", "corp"],
    "WorldBank": ["macro", "gov"],
    "ClinicalTrials": ["health"],
    "openFDA": ["health"],
    "CourtListener": ["legal"],
    "DataEuropa": ["gov"],
    "NOAA": ["climate"],
    "USGS": ["climate"],
    "NASA": ["climate"],
    "IMF": ["macro"],
    "OECD": ["macro"],
    "WHO": ["health"],
    "CDC": ["health"],
    "ECDC": ["health"],
    "UKDataGov": ["gov"],
    "RePEc": ["academic", "macro"],
    # cn_official（细粒度）
    "StdOpen": ["cn_official"],
    "FlkNPC": ["legal", "cn_official"],
    "Gsxt": ["corp", "gov"],
    "GovCN": ["gov", "cn_official"],
    "NBS": ["gov", "macro", "cn_official"],
    "NSFC": ["academic", "cn_official"],
    "CAS": ["academic", "cn_official"],
    "NCpssd": ["academic", "cn_official"],
    "CNKI": ["academic", "cn_official"],
    "WanFang": ["academic", "cn_official"],
    "NSTL": ["academic", "cn_official"],
    "NMPA": ["health", "cn_official"],
    "ChiCTR": ["health", "academic", "cn_official"],
    "NHC": ["health", "gov", "cn_official"],
    "NSIDC": ["gov", "climate", "cn_official"],
}

_CORE_CATS = {"intl_engines", "reference"}

# category → 主题 token 归一（注册表未显式标注 topics 的源按此映射）
_CAT_TOPIC = {
    "academic_api": "academic",
    "authoritative": "dev",
    "privacy_extra": "privacy",
    "ai_search": "ai",
}


def _source_topics(src: dict) -> List[str]:
    """返回源覆盖的意图主题；显式标注优先，否则 category 归一，再否则回退 category。"""
    if src.get("topics"):  # 自定义源声明的主题优先
        return list(src["topics"])
    if src["id"] in _SOURCE_TOPICS:
        return _SOURCE_TOPICS[src["id"]]
    ct = _CAT_TOPIC.get(src["category"])
    if ct:
        return [ct]
    return [src["category"]]


def _detect_topics(query: str) -> Dict[str, float]:
    """关键词词典识别查询意图：{topic: score}（命中权重和）。"""
    q = (query or "").lower()
    scores: Dict[str, float] = {}
    for topic, kws in TOPIC_KEYWORDS.items():
        s = 0.0
        for kw, w in kws:
            if kw.lower() in q:
                s += w
        if s > 0:
            scores[topic] = s
    return scores


def select_sources(query: str, sources: List[dict], cfg: dict) -> List[dict]:
    """源路由：从候选源中按需选出本次查询应打的子集（默认 select 模式）。

    规则：
      - 通用保底：intl_engines + reference 始终纳入（召回地板，避免漏通用信息）；
        已激活的 keyed 源（用户显式注入 key）始终纳入（尊重 opt-in 意图）。
      - 主题专家源：按 query 命中主题 score 降序加入，受 max_sources 截断。
      - 未识别主题（detected 空）：默认仅返回保底集——通用查询不再打 PubMed/IMF 等噪声源
        （这是相对旧全扇出的核心改进）；fallback_to_tier=true 时才补满其余源保召回。
      - 永不空：保底集恒非空。
    mode="off" 或 routing.enabled=false → 返回全部候选（旧全扇出行为，向后兼容）。
    """
    rc = (cfg.get("clean_sources") or {}).get("routing") or {}
    if not rc.get("enabled", True) or rc.get("mode") == "off":
        return list(sources)
    max_sources = int(rc.get("max_sources") or 16)

    core = [
        s
        for s in sources
        if s.get("category") in _CORE_CATS or s.get("access") == "keyed" or s.get("force_include")
    ]
    core_ids = {id(s) for s in core}
    others = [s for s in sources if id(s) not in core_ids]
    detected = _detect_topics(query)

    scored = []
    for s in others:
        st = _source_topics(s)
        sc = max((detected.get(t, 0.0) for t in st), default=0.0)
        if sc > 0:
            scored.append((sc, s))
    scored.sort(key=lambda x: -x[0])

    result = list(core)
    seen = {id(s) for s in result}

    if detected:
        for sc, s in scored:
            if id(s) in seen:
                continue
            if len(result) >= max_sources:
                break
            result.append(s)
            seen.add(id(s))
    elif rc.get("fallback_to_tier"):
        # 未识别且开启回退：补满其余源（保召回，牺牲精准）
        for s in others:
            if id(s) in seen:
                continue
            if len(result) >= max_sources:
                break
            result.append(s)
            seen.add(id(s))
    return result


# ----------------------------------------------------------------------------
# 6) 供给器构建
# ----------------------------------------------------------------------------
# active_srcs 仅取决于 cfg + 档位 + 是否注入 keys；按 (id(cfg), 档位, 注入keys) 记忆化，
# 避免每次 retrieve() 重算 65 源 × 3 档位 × _source_active（P4）。
# active_srcs 仅取决于 cfg 子态 + 档位 + 是否注入 keys；按「内容指纹」记忆化，
# 不依赖 id(cfg)（id 复用会导致陈旧命中，且「每请求新 dict → 以 id 为键」会内存泄漏）。
# 有界 FIFO + 锁：长驻服务下条目数恒定、并发安全（上线 QA / P4 增强）。
_ACTIVE_SRCS_CACHE: "OrderedDict[Any, List[dict]]" = OrderedDict()
_ACTIVE_SRCS_LOCK = threading.Lock()
_ACTIVE_SRCS_MAX = 128
# keyed 源的 env 变量名集合（key 指纹用，使 env 注入 key 后缓存正确失效）
_KEY_ENV_NAMES: tuple = tuple(
    sorted(
        {s.get("key_env") for s in CLEAN_SOURCES if s.get("access") == "keyed" and s.get("key_env")}
    )
)


def _cfg_active_sig(cfg: dict) -> tuple:
    """提取决定 active_srcs 的 cfg 子态指纹（稳定、可哈希、与对象身份无关）。

    仅纳入 _source_active 实际读取的字段：categories 开关态、searxng.url 是否存在、
    自定义源的内容（id/key_env/access/force_include/topics）。
    """
    cs = cfg.get("clean_sources") or {}
    cats = cs.get("categories") or {}
    cat_sig = tuple(sorted((c, bool((cats.get(c) or {}).get("enabled", True))) for c in cats))
    searxng_url = bool((cfg.get("searxng") or {}).get("url"))
    custom = tuple(
        sorted(
            (
                s.get("id"),
                s.get("key_env"),
                s.get("access"),
                s.get("force_include"),
                tuple(s.get("topics") or []),
            )
            for s in _custom_sources(cfg)
        )
    )
    return (cat_sig, searxng_url, custom)


def build_clean_fetch(
    cfg: dict = None,
    tiers: Optional[List[str]] = None,
    keys: Optional[dict] = None,
    fetcher: Optional[Callable] = None,
    router_fn: Optional[Callable] = None,
) -> Callable[[str], List[Dict[str, Any]]]:
    """构建「按 query 扇出、返回 docs 列表」的干净源供给器。

    参数：
      cfg     : 配置（含 clean_sources 段）；None 时取默认配置（进程级缓存单例）。
      tiers   : 覆盖档位（单档字符串或列表）；默认取 cfg.clean_sources.default_tier。
      keys    : 调用方注入的 key 字典（opt-in keyed 源用）；也可走 env。
      fetcher : 注入式底层抓取器（测试用）；默认 urllib（含超时+UA）。
    返回：Callable[[query: str], List[doc]]，doc 含 url/title/snippet/source_type/
          quality/engine/category/clean_source=True/landing_resolved=False。
    """
    from common import load_config as _load_cfg

    cfg = cfg or _load_cfg()
    cs_cfg = cfg.get("clean_sources") or {}
    default_tier = cs_cfg.get("default_tier", "standard")
    if isinstance(tiers, str):
        tiers = [tiers]
    # 参与档位集合 = 从 default_tier 起向上（lite⊂standard⊂full 单调）
    if not tiers:
        tiers = [default_tier]
    active_tiers = set()
    for t in ("lite", "standard", "full"):
        active_tiers.add(t)
        if t in tiers:
            break
    timeout = float((cs_cfg.get("timeout")) or 4.0)
    max_workers = int((cs_cfg.get("max_workers")) or 8)
    budget = float((cs_cfg.get("overall_timeout")) or 12.0)
    _fetcher = fetcher or _default_fetcher

    # env key 指纹：keyed 源是否经 env 激活会随进程内 setenv 改变，
    # 必须纳入 cache key，否则注入 key 后命中旧缓存导致 opt-in 失效（P4 修正）
    _env_sig = tuple(
        (e, bool(os.environ.get(e)))
        for e in (
            set(_KEY_ENV_NAMES)
            | {s.get("key_env") for s in _custom_sources(cfg) if s.get("key_env")}
        )
    )
    # 内容指纹键（非 id(cfg)）：同内容不同对象 → 命中同一缓存，长驻服务不泄漏
    _cache_key = (_cfg_active_sig(cfg), tuple(sorted(active_tiers)), bool(keys), _env_sig)
    with _ACTIVE_SRCS_LOCK:
        active_srcs = _ACTIVE_SRCS_CACHE.get(_cache_key)
        if active_srcs is None:
            # 候选源 = 内置注册表 + 调用方自定义（私有/内部）源
            _all = CLEAN_SOURCES + _custom_sources(cfg)
            active_srcs = [
                s for s in _all if any(_source_active(s, t, cfg, keys) for t in active_tiers)
            ]
            _ACTIVE_SRCS_CACHE[_cache_key] = active_srcs
            _ACTIVE_SRCS_CACHE.move_to_end(_cache_key)
            while len(_ACTIVE_SRCS_CACHE) > _ACTIVE_SRCS_MAX:
                _ACTIVE_SRCS_CACHE.popitem(last=False)  # FIFO 淘汰最早条目

    def provider(query: str) -> List[Dict[str, Any]]:
        if not query or not active_srcs:
            return []
        # 源路由：按需选源（默认启发式；router_fn 注入则优先；均永不空打）
        if router_fn:
            selected = router_fn(query, active_srcs) or []
        else:
            selected = select_sources(query, active_srcs, cfg)
        if not selected:
            selected = active_srcs
        docs: List[Dict[str, Any]] = []
        seen_urls = set()
        ex = ThreadPoolExecutor(max_workers=max_workers)
        try:
            futs = {ex.submit(_fetch_one, s, query, cfg, _fetcher, timeout): s for s in selected}
            try:
                for fut in as_completed(futs, timeout=budget):
                    src = futs[fut]
                    try:
                        for d in fut.result() or []:
                            u = d.get("url")
                            if not u or u in seen_urls:
                                continue
                            seen_urls.add(u)
                            docs.append(
                                {
                                    "url": u,
                                    "title": d.get("title", ""),
                                    "snippet": d.get("snippet", ""),
                                    "source_type": src.get("source_type", "unknown"),
                                    "quality": src.get("quality", "B"),
                                    "engine": src["id"],
                                    "category": src.get("category"),
                                    "access": src.get("access"),
                                    "clean_source": True,
                                    "landing_resolved": False,
                                }
                            )
                    except Exception:
                        continue
            except Exception:
                pass  # 总预算超时：返回已收集的部分，不抛
        finally:
            # 总预算超时后不阻塞等待慢源：放弃未开始/已提交未运行的抓取（cancel_futures=Py3.9+）；
            # 运行中抓取后台跑完即被 GC，不拖慢本次返回（D2：修复 with 退出 shutdown(wait=True) 使预算形同虚设）
            ex.shutdown(wait=False, cancel_futures=True)
        return docs

    return provider


# ----------------------------------------------------------------------------
# 7) 注册表快照（供文档 / describe）
# ----------------------------------------------------------------------------
def describe_clean_sources() -> Dict[str, Any]:
    """返回注册表快照：按 category 分组的源计数与明细（含 access / quality / tiers），
    以及源路由层的主题词表与可路由主题。"""
    cats: Dict[str, List[dict]] = {}
    for s in CLEAN_SOURCES:
        cats.setdefault(s["category"], []).append(
            {
                "id": s["id"],
                "name": s["name"],
                "access": s["access"],
                "quality": s["quality"],
                "source_type": s["source_type"],
                "method": s["method"],
                "tiers": s["tiers"],
                "topics": _source_topics(s),
            }
        )
    from common import load_config as _describe_load

    _custom_warn: List[str] = []
    custom = [
        {
            "id": s["id"],
            "name": s["name"],
            "access": s["access"],
            "quality": s["quality"],
            "source_type": s["source_type"],
            "method": s["method"],
            "topics": _source_topics(s),
            "keyed": bool(s.get("key_env")),
        }
        for s in _custom_sources(_describe_load(), _custom_warn)
    ]
    return {
        "total": len(CLEAN_SOURCES),
        "by_category": cats,
        "custom_sources": custom,
        "custom_source_warnings": _custom_warn,
        "tiers_preset": CLEAN_TIERS_PRESET,
        "routing_topics": sorted(TOPIC_KEYWORDS.keys()),
        "routing_source_overrides": len(_SOURCE_TOPICS),
    }


if __name__ == "__main__":
    import pprint

    pprint.pprint(describe_clean_sources())
