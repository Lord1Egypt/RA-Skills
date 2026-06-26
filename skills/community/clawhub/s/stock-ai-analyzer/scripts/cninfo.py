#!/usr/bin/env python3
"""CNInfo (巨潮资讯网) utilities: constants, classification rules, and helpers."""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    requests = None


DEFAULT_CNINFO_TIMEOUT = 15
DEFAULT_CNINFO_PAGE_SIZE = 30
CNINFO_ALLOWED_HOSTS = {"static.cninfo.com.cn", "www.cninfo.com.cn"}
CNINFO_ALLOWED_TAB_TYPES = {"fulltext", "relation"}
CNINFO_REPORT_TYPES = {"annual", "q1", "half", "q3", "all"}
CNINFO_REPORT_TYPE_ORDER = {"annual": 4, "half": 3, "q3": 2, "q1": 1}
CNINFO_REPORT_TYPE_LABELS = {
    "annual": "年度报告",
    "q1": "一季度报告",
    "half": "半年度报告",
    "q3": "三季度报告",
}
CNINFO_REPORT_CATEGORIES = {
    "annual": "category_ndbg_szsh",
    "half": "category_bndbg_szsh",
    "q1": "category_yjdbg_szsh",
    "q3": "category_sjdbg_szsh",
}
REPORT_SUMMARY_PATTERNS = (
    "摘要",
    "英文版",
    "外文版",
    "提示性公告",
    "问询",
    "回复",
)
REPORT_CORRECTION_PATTERNS = ("更正", "修订", "更新", "补充")

INQUIRY_REPLY_PATTERNS = [
    r"问询.*回复",
    r"回复.*问询",
    r"问询函回复",
    r"审核问询.*回复",
    r"反馈意见.*回复",
]
ABNORMAL_VOLATILITY_PATTERNS = [r"股价异常波动", r"股票交易异常波动"]
REGULATORY_PATTERNS = [r"监管函", r"关注函", r"警示函", r"监管工作函", r"纪律处分"]
CAPITAL_EMPLOYEE_PATTERNS = [r"员工持股计划"]
CAPITAL_PRIVATE_OFFER_PATTERNS = [r"向特定对象发行", r"特定对象发行", r"定向增发"]
CAPITAL_EQUITY_INCENTIVE_PATTERNS = [r"股权激励", r"限制性股票", r"股票期权", r"激励计划"]
INCREASE_HOLD_PATTERNS = [r"增持", r"拟增持", r"增持计划"]
DECREASE_HOLD_PATTERNS = [r"减持", r"拟减持", r"减持计划", r"减持股份"]
DECREASE_PROGRESS_PATTERNS = [
    r"减持进展",
    r"减持进度",
    r"减持计划完成",
    r"减持时间过半",
    r"减持计划时间过半",
    r"减持数量过半",
    r"减持计划届满",
    r"实施进展",
]
BUYBACK_PATTERNS = [r"回购", r"股份回购"]
MAJOR_COOPERATION_PATTERNS = [r"重大合作", r"战略合作", r"合作框架", r"签署.*协议", r"投资.*项目", r"项目投资", r"中标", r"中选"]
QUICK_REPORT_PATTERNS = [r"业绩快报", r"季度业绩快报", r"半年度业绩快报", r"年度业绩快报"]
ORIGINAL_TEXT_REQUIRED_TAGS = {
    "问询回复",
    "监管函",
    "资本运作",
    "员工持股计划",
    "特定对象发行",
    "股权激励",
    "增持",
    "减持",
    "回购",
    "合作",
    "投资项目",
    "快报",
    "业绩快报",
}


def default_cninfo_date_range(days: int = 365) -> str:
    """Build a CNInfo date range ending today."""
    today = datetime.now()
    start = today - timedelta(days=days)
    return f"{start:%Y-%m-%d}~{today:%Y-%m-%d}"


def validate_cninfo_date_range(value: Optional[str]) -> str:
    """Validate or default CNInfo date range."""
    if not value:
        return default_cninfo_date_range()
    raw = str(value).strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}~\d{4}-\d{2}-\d{2}", raw):
        raise ValueError("CNInfo date range must be YYYY-MM-DD~YYYY-MM-DD.")
    return raw


def title_hits(title: str, patterns: List[str]) -> bool:
    """Return whether a title matches any regex pattern."""
    return any(re.search(pattern, title, flags=re.IGNORECASE) for pattern in patterns)


def classify_cninfo_fulltext(title: Optional[str]) -> Dict[str, Any]:
    """Classify CNInfo announcement titles with local copied rules."""
    normalized = str(title or "").strip()

    if title_hits(normalized, INQUIRY_REPLY_PATTERNS):
        if title_hits(normalized, ABNORMAL_VOLATILITY_PATTERNS):
            return {
                "category": "上市公司公开信息",
                "subcategory": "其他",
                "rule_id": "cninfo.fulltext.excluded.abnormal_volatility_reply.v1",
                "excluded": True,
                "exclude_reason": "问询回复中的股价或股票交易异常波动公告",
                "tags": ["问询回复", "排除"],
            }
        return {
            "category": "上市公司公开信息",
            "subcategory": "问询回复",
            "rule_id": "cninfo.fulltext.inquiry_reply.v1",
            "excluded": False,
            "exclude_reason": "",
            "tags": ["问询回复"],
        }

    if title_hits(normalized, REGULATORY_PATTERNS):
        return {
            "category": "上市公司公开信息",
            "subcategory": "监管函",
            "rule_id": "cninfo.fulltext.regulatory_letter.v1",
            "excluded": False,
            "exclude_reason": "",
            "tags": ["监管函"],
        }

    if title_hits(normalized, CAPITAL_EMPLOYEE_PATTERNS):
        return {
            "category": "上市公司公开信息",
            "subcategory": "资本运作-员工持股计划",
            "rule_id": "cninfo.fulltext.capital.employee_stock_plan.v1",
            "excluded": False,
            "exclude_reason": "",
            "tags": ["资本运作", "员工持股计划"],
        }

    if title_hits(normalized, CAPITAL_PRIVATE_OFFER_PATTERNS):
        return {
            "category": "上市公司公开信息",
            "subcategory": "资本运作-特定对象发行",
            "rule_id": "cninfo.fulltext.capital.private_offering.v1",
            "excluded": False,
            "exclude_reason": "",
            "tags": ["资本运作", "特定对象发行"],
        }

    if title_hits(normalized, CAPITAL_EQUITY_INCENTIVE_PATTERNS):
        return {
            "category": "上市公司公开信息",
            "subcategory": "资本运作-股权激励",
            "rule_id": "cninfo.fulltext.capital.equity_incentive.v1",
            "excluded": False,
            "exclude_reason": "",
            "tags": ["资本运作", "股权激励"],
        }

    if title_hits(normalized, INCREASE_HOLD_PATTERNS):
        return {
            "category": "上市公司公开信息",
            "subcategory": "增持",
            "rule_id": "cninfo.fulltext.increase_hold.v1",
            "excluded": False,
            "exclude_reason": "",
            "tags": ["增持"],
        }

    if title_hits(normalized, DECREASE_HOLD_PATTERNS):
        if title_hits(normalized, DECREASE_PROGRESS_PATTERNS):
            return {
                "category": "上市公司公开信息",
                "subcategory": "其他",
                "rule_id": "cninfo.fulltext.excluded.decrease_progress.v1",
                "excluded": True,
                "exclude_reason": "减持进度或实施进展类公告",
                "tags": ["减持", "排除"],
            }
        return {
            "category": "上市公司公开信息",
            "subcategory": "减持",
            "rule_id": "cninfo.fulltext.decrease_hold.v1",
            "excluded": False,
            "exclude_reason": "",
            "tags": ["减持"],
        }

    if title_hits(normalized, BUYBACK_PATTERNS):
        return {
            "category": "上市公司公开信息",
            "subcategory": "回购",
            "rule_id": "cninfo.fulltext.buyback.v1",
            "excluded": False,
            "exclude_reason": "",
            "tags": ["回购"],
        }

    if title_hits(normalized, MAJOR_COOPERATION_PATTERNS):
        return {
            "category": "上市公司公开信息",
            "subcategory": "重大合作/投资项目",
            "rule_id": "cninfo.fulltext.major_cooperation_project.v1",
            "excluded": False,
            "exclude_reason": "",
            "tags": ["合作", "投资项目"],
        }

    if title_hits(normalized, QUICK_REPORT_PATTERNS):
        return {
            "category": "上市公司公开信息",
            "subcategory": "快报",
            "rule_id": "cninfo.fulltext.quick_report.v1",
            "excluded": False,
            "exclude_reason": "",
            "tags": ["快报", "业绩快报"],
        }

    return {
        "category": "上市公司公开信息",
        "subcategory": "其他",
        "rule_id": "cninfo.fulltext.other.v1",
        "excluded": False,
        "exclude_reason": "",
        "tags": ["其他"],
    }


def classify_cninfo_relation() -> Dict[str, Any]:
    """Classify CNInfo relation-tab items."""
    return {
        "category": "互动易/调研",
        "subcategory": "未定义",
        "rule_id": "cninfo.relation.unclassified.v1",
        "excluded": False,
        "exclude_reason": "",
        "tags": ["relation"],
    }


def announcement_needs_original_text(item: Dict[str, Any]) -> bool:
    """Flag events where title metadata should usually be upgraded to PDF text."""
    tags = set(item.get("tags") or [])
    return bool(tags & ORIGINAL_TEXT_REQUIRED_TAGS)


def require_requests() -> Any:
    """Ensure requests is installed before using CNInfo-based features."""
    if requests is None:
        raise RuntimeError("Missing dependency: install requests before using CNInfo report retrieval.")
    return requests


def cninfo_headers() -> Dict[str, str]:
    """Headers for CNInfo announcement endpoints."""
    return {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "www.cninfo.com.cn",
        "Origin": "http://www.cninfo.com.cn",
        "Referer": "http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        ),
        "X-Requested-With": "XMLHttpRequest",
    }


def build_cninfo_url(path_or_url: str) -> str:
    """Normalize a CNInfo announcement path or URL to a full URL."""
    raw = str(path_or_url or "").strip()
    if not raw:
        raise ValueError("CNInfo report URL cannot be empty.")
    if raw.startswith("http://") or raw.startswith("https://"):
        parsed = urlparse(raw)
        if parsed.hostname not in CNINFO_ALLOWED_HOSTS:
            raise ValueError(f"Unsupported CNInfo host: {parsed.hostname}")
        return raw

    normalized = raw.lstrip("/")
    return f"http://static.cninfo.com.cn/{normalized}"


def build_report_date_range(report_year: Optional[int]) -> str:
    """Build a CNInfo date range that covers report disclosures."""
    today = datetime.now()
    if report_year:
        start = datetime(report_year, 1, 1)
        end = datetime(report_year + 1, 12, 31)
    else:
        start = datetime(today.year - 5, 1, 1)
        end = today
    return f"{start:%Y-%m-%d}~{end:%Y-%m-%d}"


def classify_report_title(title: str) -> Dict[str, Any]:
    """Parse report title metadata from a CNInfo announcement title."""
    normalized = str(title or "").strip()
    report_type = ""
    if "第一季度报告" in normalized or "一季度报告" in normalized:
        report_type = "q1"
    elif "半年度报告" in normalized:
        report_type = "half"
    elif "第三季度报告" in normalized or "三季度报告" in normalized:
        report_type = "q3"
    elif "年度报告" in normalized and "半年度报告" not in normalized:
        report_type = "annual"

    year_match = re.search(r"(20\d{2})\s*年", normalized)
    report_year = int(year_match.group(1)) if year_match else None
    is_summary = any(token in normalized for token in REPORT_SUMMARY_PATTERNS)
    is_correction = any(token in normalized for token in REPORT_CORRECTION_PATTERNS)
    is_full_report = bool(report_type) and not is_summary

    return {
        "report_type": report_type,
        "report_type_label": CNINFO_REPORT_TYPE_LABELS.get(report_type, ""),
        "report_year": report_year,
        "is_summary": is_summary,
        "is_correction": is_correction,
        "is_full_report": is_full_report,
    }


def report_sort_key(item: Dict[str, Any]) -> Any:
    """Sort reports by fiscal period, disclosure date, and preferred variant."""
    report_year = int(item.get("report_year") or 0)
    report_type = str(item.get("report_type") or "")
    report_type_order = CNINFO_REPORT_TYPE_ORDER.get(report_type, 0)
    announcement_time = str(item.get("announcement_time") or "")
    full_report_order = 1 if item.get("is_full_report") else 0
    correction_order = 1 if item.get("is_correction") else 0
    return (
        report_year,
        report_type_order,
        announcement_time,
        full_report_order,
        correction_order,
    )
