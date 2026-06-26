#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
InfoX-Med 高级搜索接口 — 支持关键词检索、指南搜索、系统评价/Meta分析、RCT 搜索。
通过命令行参数调用，输出 JSON 格式结果。
"""

import asyncio
import argparse
import json
import logging
import os
import re
import sys
from enum import Enum
from itertools import combinations
from typing import List, Dict, Any, Union

try:
    import aiohttp
except ImportError:  # optional dependency
    aiohttp = None

# ---------------------------------------------------------------------------
# 日志配置
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
API_URL = "https://api.infox-med.com/search/home/keywords"
API_TOKEN = os.environ.get("INFOX_MED_TOKEN", "e3f62087e126439aa12ad4637cf4f12b|1106970")
DEFAULT_PAGE_SIZE = 20
REQUEST_TIMEOUT = 20


# ---------------------------------------------------------------------------
# 枚举
# ---------------------------------------------------------------------------
class SearchField(Enum):
    """keywords 搜索支持的字段标签"""
    TITLE = "Title"
    ABSTRACT = "Abstract"
    TITLE_ABSTRACT = "Title/Abstract"
    MESH_TERMS = "MeSH Terms"
    JOURNAL = "Journal"
    AUTHOR = "Author"
    FIRST_AUTHOR = "First Author"
    LAST_AUTHOR = "Last Author"
    AFFILIATION = "Affiliation"
    FIRST_AUTHOR_AFFILIATION = "First Author Affiliation"
    LAST_AUTHOR_AFFILIATION = "Last Author Affiliation"
    CORPORATE_AUTHOR = "Corporate Author"


class LogicOp(Enum):
    """逻辑运算符"""
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


class SortType(Enum):
    """排序规则"""
    IF = "docIf"
    PUBLISH_TIME = "docPublishTime"
    CITED_BY = "citedBy"
    RELEVANT = "relevant"


# ---------------------------------------------------------------------------
# 查询构造器
# ---------------------------------------------------------------------------
class QueryBuilder:
    """构建 InfoX-Med keywords 查询字符串"""

    @staticmethod
    def term(value: str, field: Union[SearchField, str] = None) -> str:
        """创建带字段标签的术语，如 Lung Cancer[Title]"""
        clean_val = str(value).replace('"', '\\"')
        field_str = field.value if isinstance(field, SearchField) else field
        if field_str:
            return f"{clean_val}[{field_str}]"
        return clean_val

    @staticmethod
    def combine(items: List[str], operator: LogicOp = LogicOp.AND) -> str:
        """用逻辑运算符连接多个查询片段，每个子条件用括号包裹"""
        valid = []
        for item in items:
            if not item:
                continue
            s = item.strip()
            if s.startswith("(") and s.endswith(")"):
                valid.append(s)
            else:
                valid.append(f"({s})")
        if not valid:
            return ""
        if len(valid) == 1:
            return valid[0]
        return f" {operator.value} ".join(valid)


def build_pairwise_combination_query(keywords: List[str], field: SearchField) -> str:
    """
    构建两两组合查询：((K1 AND K2) OR (K1 AND K3) OR (K2 AND K3))
    若仅 1 个关键词则直接返回该词的带字段形式。
    """
    terms = [QueryBuilder.term(k, field) for k in keywords]

    if len(terms) <= 1:
        return QueryBuilder.combine(terms, LogicOp.OR)

    and_groups = []
    for t1, t2 in combinations(terms, 2):
        group = QueryBuilder.combine([t1, t2], LogicOp.AND)
        if group:
            and_groups.append(f"({group})")

    combined = QueryBuilder.combine(and_groups, LogicOp.OR)
    return f"({combined})" if combined else ""


# ---------------------------------------------------------------------------
# 筛选构造器
# ---------------------------------------------------------------------------
class FilterBuilder:
    """构建 filter 字符串，格式: $$key$$val..."""

    def __init__(self):
        self.filters: List[str] = []

    def add_range(self, key: str, start: Any, end: Any) -> "FilterBuilder":
        self.filters.append(f"{key}$${start}$${end}")
        return self

    def add_value(self, key: str, value: Any) -> "FilterBuilder":
        self.filters.append(f"{key}$${value}")
        return self

    def add_options(self, key: str, values: List[Any]) -> "FilterBuilder":
        if values:
            joined = "$OR$".join(str(v) for v in values)
            self.filters.append(f"{key}$${joined}")
        return self

    def add_publish_time(self, start_date: str, end_date: str) -> "FilterBuilder":
        return self.add_range("doc_publish_time", start_date, end_date)

    def build(self) -> str:
        if not self.filters:
            return ""
        return "@@AND$$" + "@@AND$$".join(self.filters)


# ---------------------------------------------------------------------------
# 参数校验
# ---------------------------------------------------------------------------
VALID_FIELD_TAGS = {
    "Title", "Abstract", "Title/Abstract", "MeSH Terms",
    "Author", "Affiliation", "Journal", "First Author", "Last Author",
    "First Author Affiliation", "Last Author Affiliation", "Corporate Author",
}


def validate_search_params(query_string: str, filter_string: str = "") -> str | None:
    """校验搜索参数。返回错误信息字符串，或 None 表示通过。"""
    if not query_string or not query_string.strip():
        return "query_string 不能为空。"

    # 括号匹配
    if query_string.count("(") != query_string.count(")"):
        return (
            f"query_string 中括号不匹配 "
            f"(左 {query_string.count('(')} / 右 {query_string.count(')')})。"
        )

    # 字段标签校验
    tags = re.findall(r"\[(.*?)\]", query_string)
    if not tags:
        return "缺少字段限定符，例如 [Title]。"
    for tag in tags:
        if tag not in VALID_FIELD_TAGS:
            return (
                f"无效字段限定符 '[{tag}]'。"
                f"方括号内只能放字段名（如 [Title]），不要把关键词放进方括号。"
            )

    # 多条件间需要逻辑运算符
    if re.search(r"\]\s+[\"(]", query_string):
        logic_ops = (" AND ", " OR ", " NOT ")
        if not any(op in query_string for op in logic_ops):
            return "多个搜索条件之间缺少逻辑运算符 (AND/OR/NOT)。"

    # filter 校验
    if filter_string:
        if "$$" not in filter_string:
            return "filter_string 分隔符错误，请使用 '$$' 分隔键和值。"
        if "doc_publish_time" in filter_string:
            if not re.findall(r"\d{4}-\d{2}-\d{2}", filter_string):
                return "doc_publish_time 日期格式错误，请使用 YYYY-MM-DD。"

    return None


# ---------------------------------------------------------------------------
# 结果清洗
# ---------------------------------------------------------------------------
def _simplify_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """保留核心字段并标准化命名"""
    return {
        "id": record.get("id"),
        "title": record.get("docTitle"),
        "abstract": record.get("docAbstract"),
        "authors": record.get("docAuthor"),
        "journal": record.get("docSourceJournal") or record.get("docSimpleJournal"),
        "publish_date": record.get("docPublishTime"),
        "impact_factor": record.get("docIf"),
        "publication_type": record.get("docPublishType"),
        "link": (
            f"https://www.infox-med.com/#/articleDetails?id={record['id']}"
            if record.get("id") else None
        ),
    }


# ---------------------------------------------------------------------------
# 核心搜索函数
# ---------------------------------------------------------------------------
async def search_infox_advanced(
    query_string: str,
    filter_string: str = "",
    sort_field: str = "relevant",
    page_size: int = DEFAULT_PAGE_SIZE,
) -> Dict[str, Any]:
    """
    调用 InfoX-Med API 执行高级搜索。

    参数:
        query_string:  检索表达式，如 (Lung Cancer[Title]) AND (Immunotherapy[Title/Abstract])
        filter_string: 筛选条件，如 $$doc_publish_type$$Review
        sort_field:    排序字段 (relevant / docPublishTime / docIf / citedBy)
        page_size:     每页结果数

    返回:
        {"code": 200, "msg": "success", "records": [...]}
    """
    logger.info(f"搜索请求: query='{query_string}', filter='{filter_string}', sort='{sort_field}'")

    # 参数校验
    error = validate_search_params(query_string, filter_string)
    if error:
        logger.warning(f"参数校验失败: {error}")
        return {"code": 400, "msg": f"INPUT_VALIDATION_ERROR: {error}", "records": []}

    sort_val = sort_field.value if isinstance(sort_field, SortType) else sort_field
    if sort_val == "relevant":
        sort_val = ""

    payload = {
        "type": "doc",
        "pageNum": 1,
        "pageSize": page_size,
        "keywords": query_string,
        "filter": filter_string,
        "sort": sort_val,
    }
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://infox-med.com",
        "token": API_TOKEN,
    }

    try:
        if aiohttp is not None:
            timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(API_URL, json=payload, headers=headers) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
        else:
            import urllib.request
            body = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(API_URL, data=body, headers=headers, method="POST")
            loop = asyncio.get_running_loop()
            def _do_request():
                with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                    return json.loads(resp.read().decode("utf-8", errors="replace"))
            data = await loop.run_in_executor(None, _do_request)
        records_raw = (data.get("data") or {}).get("records") or []
        records = [_simplify_record(r) for r in records_raw]
        return {"code": 200, "msg": "success", "records": records}
    except Exception as e:
        logger.error(f"请求异常: {e}")
        return {"code": 500, "msg": str(e), "records": []}


# ---------------------------------------------------------------------------
# 高层搜索函数
# ---------------------------------------------------------------------------
async def search_chinese_guideline(keywords: List[str]) -> List[Dict[str, Any]]:
    """搜索中文指南（仅限中华系列期刊）"""
    keyword_query = build_pairwise_combination_query(keywords, SearchField.TITLE_ABSTRACT)
    query_string = f'{keyword_query} AND ("Zhonghua"[Journal])'
    filter_string = "$$doc_publish_type$$Guideline$OR$Practice Guideline"
    result = await search_infox_advanced(query_string=query_string, filter_string=filter_string)
    return result.get("records", [])


async def search_english_guideline(keywords: List[str]) -> List[Dict[str, Any]]:
    """搜索英文指南（排除中华系列期刊）"""
    keyword_query = build_pairwise_combination_query(keywords, SearchField.TITLE_ABSTRACT)
    query_string = f'{keyword_query} NOT ("Zhonghua"[Journal])'
    filter_string = "$$doc_publish_type$$Guideline$OR$Practice Guideline"
    result = await search_infox_advanced(query_string=query_string, filter_string=filter_string)
    return result.get("records", [])


async def search_systematic_meta(keywords: List[str]) -> List[Dict[str, Any]]:
    """搜索系统评价和 Meta 分析"""
    query_string = build_pairwise_combination_query(keywords, SearchField.TITLE_ABSTRACT)
    filter_string = "$$doc_publish_type$$Meta-Analysis$OR$Systematic Review"
    result = await search_infox_advanced(query_string=query_string, filter_string=filter_string)
    records = result.get("records", [])
    # 二次过滤：标题必须包含 meta-analysis 或 systematic review
    return [
        r for r in records
        if r.get("title") and (
            "meta-analysis" in r["title"].lower()
            or "systematic review" in r["title"].lower()
        )
    ]


async def search_rct(keywords: List[str]) -> List[Dict[str, Any]]:
    """搜索随机对照试验 (RCT)"""
    query_string = build_pairwise_combination_query(keywords, SearchField.TITLE_ABSTRACT)
    filter_string = "$$doc_publish_type$$Randomized Controlled Trial"
    result = await search_infox_advanced(query_string=query_string, filter_string=filter_string)
    return result.get("records", [])


# ---------------------------------------------------------------------------
# 综合搜索：并行执行 4 类搜索
# ---------------------------------------------------------------------------
async def search_all(keywords: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    """并行搜索中文指南、英文指南、系统评价/Meta分析、RCT，返回分类结果。"""
    cn_guide, en_guide, sys_meta, rct = await asyncio.gather(
        search_chinese_guideline(keywords),
        search_english_guideline(keywords),
        search_systematic_meta(keywords),
        search_rct(keywords),
    )
    return {
        "chinese_guideline": cn_guide,
        "english_guideline": en_guide,
        "systematic_meta": sys_meta,
        "rct": rct,
    }


# ---------------------------------------------------------------------------
# 自由搜索（直接传 query_string + filter_string）
# ---------------------------------------------------------------------------
async def search_free(
    query_string: str,
    filter_string: str = "",
    sort_field: str = "relevant",
) -> List[Dict[str, Any]]:
    """自由搜索：直接使用检索表达式和筛选条件。"""
    result = await search_infox_advanced(
        query_string=query_string,
        filter_string=filter_string,
        sort_field=sort_field,
    )
    return result.get("records", [])


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------
def build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="InfoX-Med 医学文献搜索")
    sub = parser.add_subparsers(dest="command", help="搜索模式")

    # 模式 1：按关键词并行搜 4 类库
    p_all = sub.add_parser("all", help="并行搜索 4 类文献库 (中文指南/英文指南/系统评价/RCT)")
    p_all.add_argument("keywords", nargs="+", help="搜索关键词列表")

    # 模式 2：仅搜指定类别
    for name, desc in [
        ("chinese-guideline", "搜索中文指南"),
        ("english-guideline", "搜索英文指南"),
        ("systematic-meta", "搜索系统评价/Meta分析"),
        ("rct", "搜索随机对照试验 (RCT)"),
    ]:
        p = sub.add_parser(name, help=desc)
        p.add_argument("keywords", nargs="+", help="搜索关键词列表")

    # 模式 3：自由搜索
    p_free = sub.add_parser("free", help="自由搜索（直接传检索表达式）")
    p_free.add_argument("--query", required=True, help="检索表达式 (query_string)")
    p_free.add_argument("--filter", default="", help="筛选条件 (filter_string)")
    p_free.add_argument(
        "--sort", default="relevant",
        choices=["relevant", "docPublishTime", "docIf", "citedBy"],
        help="排序方式",
    )

    # 通用参数
    parser.add_argument("--output", "-o", help="结果输出到 JSON 文件（不指定则输出到 stdout）")

    return parser


async def async_main(args: argparse.Namespace):
    cmd = args.command
    if not cmd:
        print("请指定搜索模式。使用 --help 查看帮助。", file=sys.stderr)
        sys.exit(1)

    dispatch = {
        "all": lambda: search_all(args.keywords),
        "chinese-guideline": lambda: search_chinese_guideline(args.keywords),
        "english-guideline": lambda: search_english_guideline(args.keywords),
        "systematic-meta": lambda: search_systematic_meta(args.keywords),
        "rct": lambda: search_rct(args.keywords),
        "free": lambda: search_free(args.query, args.filter, args.sort),
    }

    result = await dispatch[cmd]()
    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        logger.info(f"结果已写入 {args.output}")
    else:
        print(output)


def main():
    parser = build_cli_parser()
    args = parser.parse_args()
    asyncio.run(async_main(args))


if __name__ == "__main__":
    main()
