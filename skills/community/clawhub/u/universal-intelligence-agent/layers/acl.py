"""
Anti-Corruption Layer (ACL) — 阶段间数据校验边界
────────────────────────────────────────────────
每一个阶段容器输出都必须通过 ACL 校验才能流入下一阶段。
ACL 是硬边界：None/空列表/类型不匹配在此处被拦截并转化为
明确的结构化错误，严禁向下游裸传脏数据。
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, TypeVar, Generic

logger = logging.getLogger(__name__)


# ── ACL 校验结果 ────────────────────────────────────────────

@dataclass(frozen=True)
class ACLResult:
    """ACL 校验结果 — 不可变值对象"""
    passed: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    transformed_data: Any = None

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    def or_raise(self) -> Any:
        """校验失败直接抛异常，成功则返回转换后的数据"""
        if not self.passed:
            raise ACLViolationError(self.errors)
        if self.has_warnings:
            for w in self.warnings:
                logger.warning(f"ACL Warning: {w}")
        return self.transformed_data


class ACLViolationError(Exception):
    """ACL 校验失败 — 脏数据在边界被拦截"""
    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__(f"ACL Violation: {'; '.join(errors)}")


# ── 核心校验函数 ────────────────────────────────────────────

def validate_not_none(data: Any, field_name: str = "data") -> ACLResult:
    """最基础的 None 拦截 — 这是崩溃传染链的第一道防线"""
    if data is None:
        return ACLResult(
            passed=False,
            errors=[f"{field_name} is None — upstream stage produced no data"],
        )
    return ACLResult(passed=True, transformed_data=data)


def validate_list_nonempty(data: list, field_name: str = "list") -> ACLResult:
    """列表非空校验 — 拦截空列表传入下游"""
    if not isinstance(data, list):
        return ACLResult(
            passed=False,
            errors=[f"{field_name} is not a list, got {type(data).__name__}"],
        )
    if len(data) == 0:
        return ACLResult(
            passed=False,
            errors=[f"{field_name} is empty — no results to process"],
        )
    return ACLResult(passed=True, transformed_data=data)


def validate_dict_has_keys(data: dict, required_keys: list[str], field_name: str = "dict") -> ACLResult:
    """字典必需字段校验"""
    if not isinstance(data, dict):
        return ACLResult(
            passed=False,
            errors=[f"{field_name} is not a dict, got {type(data).__name__}"],
        )
    missing = [k for k in required_keys if k not in data]
    if missing:
        return ACLResult(
            passed=False,
            errors=[f"{field_name} missing required keys: {missing}"],
        )
    return ACLResult(passed=True, transformed_data=data)


def validate_urls(urls: list[str], field_name: str = "urls") -> ACLResult:
    """URL 格式校验"""
    from urllib.parse import urlparse

    if not urls:
        return ACLResult(passed=True, transformed_data=[], warnings=[f"{field_name} is empty"])

    invalid = []
    for u in urls:
        if u is None:
            invalid.append("None")
            continue
        if not isinstance(u, str):
            invalid.append(str(type(u)))
            continue
        parsed = urlparse(u)
        if not parsed.scheme or not parsed.netloc:
            invalid.append(u)

    if invalid:
        return ACLResult(
            passed=False,
            errors=[f"{field_name} contains {len(invalid)} invalid URLs: {invalid[:5]}..."],
        )

    return ACLResult(passed=True, transformed_data=urls)


def validate_string_nonempty(data: str, field_name: str = "string", min_length: int = 1) -> ACLResult:
    """字符串非空+最小长度校验"""
    if not isinstance(data, str):
        return ACLResult(
            passed=False,
            errors=[f"{field_name} is not a string, got {type(data).__name__}"],
        )
    stripped = data.strip()
    if len(stripped) < min_length:
        return ACLResult(
            passed=False,
            errors=[f"{field_name} is too short: {len(stripped)} chars, need >= {min_length}"],
        )
    return ACLResult(passed=True, transformed_data=stripped)


def validate_content_quality(pages: list[dict], field_name: str = "pages") -> ACLResult:
    """
    内容质量校验 — Phase 1 新增
    拦截空内容的页面流入下游分析阶段。
    至少要有 1 个页面的 content_md 非空且 >= 50 字符。
    """
    if not pages:
        return ACLResult(
            passed=False,
            errors=[f"{field_name} is empty — no content to analyze"],
        )

    valid_pages = [
        p for p in pages
        if isinstance(p, dict) and len(p.get("content_md", "").strip()) >= 50
    ]

    if not valid_pages:
        return ACLResult(
            passed=False,
            errors=[
                f"{field_name}: all {len(pages)} pages have empty or too-short content "
                f"(min 50 chars required per page). Upstream crawl may have failed silently."
            ],
        )

    # 警告：部分页面内容为空（不阻断，但记录）
    empty_count = len(pages) - len(valid_pages)
    warnings = []
    if empty_count > 0:
        warnings.append(
            f"{field_name}: {empty_count}/{len(pages)} pages have insufficient content"
        )

    return ACLResult(
        passed=True,
        transformed_data=pages,
        warnings=warnings,
    )


def validate_credibility_range(data: dict, field_name: str = "credibility_scores") -> ACLResult:
    """
    可信度分数范围校验 — Phase 1 新增
    确保 average_score 在 [0.0, 5.0] 范围内。
    """
    if not isinstance(data, dict):
        return ACLResult(
            passed=False,
            errors=[f"{field_name} is not a dict, got {type(data).__name__}"],
        )

    avg = data.get("average_score")
    if avg is not None:
        if not isinstance(avg, (int, float)):
            return ACLResult(
                passed=False,
                errors=[f"{field_name}.average_score is not numeric: {type(avg).__name__}"],
            )
        if avg < 0.0 or avg > 5.0:
            return ACLResult(
                passed=False,
                errors=[f"{field_name}.average_score out of range: {avg} (expected [0.0, 5.0])"],
            )

    return ACLResult(passed=True, transformed_data=data)


# ── 阶段间数据管道校验器 ───────────────────────────────────

class StageValidator:
    """
    阶段间校验器 — 每个阶段容器输出必须通过此校验器才能传给下游

    用法:
        validator = StageValidator([
            lambda d: validate_not_none(d, "search_results"),
            lambda d: validate_list_nonempty(d, "search_results"),
        ])
        clean_data = validator.validate(raw_output)
    """

    def __init__(self, checks: list[Callable[[Any], ACLResult]]):
        self._checks = checks

    def validate(self, data: Any) -> Any:
        """执行所有校验，全部通过才返回净化后的数据"""
        current = data
        all_warnings = []
        for i, check in enumerate(self._checks):
            result = check(current)
            if not result.passed:
                logger.error(f"ACL check #{i} failed: {result.errors}")
                raise ACLViolationError(result.errors)
            if result.has_warnings:
                all_warnings.extend(result.warnings)
            current = result.transformed_data
        if all_warnings:
            logger.warning(f"ACL passed with {len(all_warnings)} warnings: {all_warnings}")
        return current


def _validate_and_keep(original: Any, result: ACLResult) -> ACLResult:
    """执行校验但保持原始数据不变 — 用于嵌套字段校验"""
    if not result.passed:
        return result
    return ACLResult(
        passed=True,
        transformed_data=original,
        warnings=result.warnings,
    )


# ── 搜索→爬取 阶段校验 ─────────────────────────────────────

search_to_crawl_validator = StageValidator([
    lambda d: validate_not_none(d, "search_output"),
    lambda d: validate_dict_has_keys(d, ["deduplicated_results", "total_deduped", "status"], "search_output"),
    lambda d: _validate_and_keep(d, validate_list_nonempty(d["deduplicated_results"], "deduplicated_results")),
])

# ── 爬取→分析 阶段校验 ─────────────────────────────────────

crawl_to_analyze_validator = StageValidator([
    lambda d: validate_not_none(d, "crawl_output"),
    lambda d: validate_dict_has_keys(d, ["pages", "status"], "crawl_output"),
    lambda d: _validate_and_keep(d, validate_list_nonempty(d["pages"], "pages")),
    # Phase 1 新增：内容质量校验 — 拦截空内容流入分析阶段
    lambda d: _validate_and_keep(d, validate_content_quality(d["pages"], "crawl_output.pages")),
])

# ── 分析→报告 阶段校验 ─────────────────────────────────────

analyze_to_report_validator = StageValidator([
    lambda d: validate_not_none(d, "analysis_output"),
    lambda d: validate_dict_has_keys(
        d,
        ["nlp_results", "credibility_scores", "status", "key_findings", "conclusions"],
        "analysis_output",
    ),
    lambda d: _validate_and_keep(d, ACLResult(passed=True, transformed_data=d)),
    # Phase 1 新增：可信度分数范围校验
    lambda d: _validate_and_keep(d, validate_credibility_range(
        d.get("credibility_scores", {}), "analysis_output.credibility_scores",
    )),
])

# ── 输入适配层校验 ──────────────────────────────────────────

input_validator = StageValidator([
    lambda d: validate_not_none(d, "user_input"),
    lambda d: validate_string_nonempty(d.get("query", ""), "query", min_length=2),
])


# ── Phase 5.0: 类型安全校验入口 ─────────────────────────────
# 直接接收 PipelineBus，通过强类型 getter 获取数据后校验，
# 消除 dict 透传的类型黑洞。

def validate_search_to_crawl(bus) -> dict:
    """类型安全的搜索→爬取校验

    从 PipelineBus 获取强类型 SearchOutput，校验后返回 dict 给爬取阶段。
    """
    from contracts.context_schema import PipelineBus
    search_output = bus.get_search_output()
    data = search_output.model_dump()
    # 使用现有 StageValidator 校验 dict 内容
    return search_to_crawl_validator.validate(data)


def validate_crawl_to_analyze(bus) -> dict:
    """类型安全的爬取→分析校验

    从 PipelineBus 获取强类型 CrawlOutput，校验后返回 dict 给分析阶段。
    """
    from contracts.context_schema import PipelineBus
    crawl_output = bus.get_crawl_output()
    data = crawl_output.model_dump()
    # 使用现有 StageValidator 校验 dict 内容
    return crawl_to_analyze_validator.validate(data)
