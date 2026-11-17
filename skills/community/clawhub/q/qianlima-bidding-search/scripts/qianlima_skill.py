#!/usr/bin/env python3
"""Qianlima bidding skill runtime helper.

The script keeps API access, result-set state, and project reference
resolution deterministic for the skill.
"""

from __future__ import annotations

import argparse
import calendar
import copy
from contextvars import ContextVar
from functools import wraps
import math
from zoneinfo import ZoneInfo
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Callable

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import area_resolver

from complex_query_plan import (
    PlanValidationError,
    preflight_complex_plan,
    sanitize_query_match_scopes,
)


DEFAULT_BASE_URL = "https://skills.qianlima.com"
PACKAGE_SOURCE_CODE = "bb3b4102f584028c3830df37"
STATE_VERSION = 3
DEFAULT_STATE_TTL_SECONDS = 7200
STATE_ERROR_CODES = {
    "SESSION_ID_REQUIRED",
    "RESULT_SET_ID_REQUIRED",
    "INVALID_RESULT_SET_ID",
    "RESULT_SET_NOT_FOUND",
    "RESULT_SET_SESSION_MISMATCH",
    "RESULT_SET_EXPIRED",
    "RESULT_SET_CORRUPT",
    "STATE_STORE_UNAVAILABLE",
}
STATE_RETRY_POLICY = "restore_explicit_context_or_clarify_missing_fields"
STATE_FAILURE_USER_MESSAGE = "现有上下文不足以准确继续。请补充所需的公告指代或原查询条件与当前页码。"
EMPTY_DISPLAY = "未公示"

ENTITLEMENT_DIAGNOSIS_ERROR_CODES = {"10007", "10010", "10028", "10030", "10031", "10032", "10036", "10037", "10038", "10039", "10040"}
SEARCH_ENTITLEMENT_RIGHTS = {
    "project": "标讯查询",
    "purchase_intention": "采购意向查询",
    "expiring_project": "临期项目查询",
}
DETAIL_ENTITLEMENT_RIGHTS = {
    "project": "标讯详情",
    "purchase_intention": "采购意向详情",
    "expiring_project": "临期项目详情",
}

AMOUNT_UNIT_CONFIRMATION_FIELD = "amount_unit_confirmed"
SEARCH_AMOUNT_FIELDS = {
    "project": ("beginAmount", "endAmount"),
    "purchase_intention": ("startPlanPurchaseAmount", "endPlanPurchaseAmount"),
    "expiring_project": ("beginContractAmount", "endContractAmount"),
}
AGENT_CORRECTION_ERROR_CODES = {
    "AGENT_QUERY_CORRECTION_REQUIRED",
    "AGENT_DETAIL_CORRECTION_REQUIRED",
    "AMOUNT_UNIT_SELF_CHECK_REQUIRED",
}

PROJECT_SEARCH_FIELDS = frozenset({
    "keywordGroups", "excludeWords", "currentPage", "numPerPage", "areaIds",
    "beginTime", "endTime", "purchasingUnitTypes", "infoTypes", "sortType",
    "procurementCategories", "procurementMethods", "fundsSources", "hasAnnex",
    "hasAgency", "registrationStatus", "hasBiddingPhone", "hasWinningPhone",
    "beginAmount", "endAmount", AMOUNT_UNIT_CONFIRMATION_FIELD,
})
PURCHASE_SEARCH_FIELDS = frozenset(
    {
        "keywords",
        "keywordsSearchType",
        "excludeWords",
        "matchScopes",
        "startPlanPurchaseDate",
        "endPlanPurchaseDate",
        "beginTime",
        "endTime",
        "areaIds",
        "startPlanPurchaseAmount",
        "endPlanPurchaseAmount",
        "purchasingUnitTypes",
        "sortType",
        "currentPage",
        "numPerPage",
        AMOUNT_UNIT_CONFIRMATION_FIELD,
    }
)
EXPIRING_SEARCH_FIELDS = frozenset(
    {
        "keywords",
        "keywordsSearchType",
        "excludeWords",
        "matchScopes",
        "beginServiceExpireTime",
        "endServiceExpireTime",
        "contractPeriodType",
        "areaIds",
        "beginContractAmount",
        "endContractAmount",
        "procurementMethod",
        "purchasingUnitTypes",
        "sortType",
        "currentPage",
        "numPerPage",
        AMOUNT_UNIT_CONFIRMATION_FIELD,
    }
)
ENTERPRISE_QUERY_FIELDS: dict[str, frozenset[str]] = {
    "partners": frozenset({"companyName", "beginTime", "endTime", "sortType"}),
    "area-distribution": frozenset({"companyName", "beginTime", "endTime", "sortType"}),
    "principals": frozenset({"companyName", "beginTime", "endTime", "sortType"}),
    "winning-area-distribution": frozenset({"companyName", "beginTime", "endTime", "sortType"}),
    "co-bidder-competitors": frozenset({"companyName", "beginTime", "endTime"}),
    "potential-competitors": frozenset({"companyName", "beginTime", "endTime"}),
    "business-info": frozenset({"companyName"}),
    "contacts": frozenset({"companyName", "phoneType", "currentPage", "numPerPage"}),
}

PROJECT_MATCH_SCOPES = frozenset(range(1, 11))
PURCHASE_MATCH_SCOPES = frozenset({1, 2, 8, 10})
EXPIRING_MATCH_SCOPES = PROJECT_MATCH_SCOPES
SEARCH_SORT_TYPES = frozenset({1, 2, 6})
ENTERPRISE_SORT_TYPES = frozenset({1, 2})
PROCUREMENT_METHODS = frozenset({0, 1, 2, 3, 4, 5, 6})
PURCHASING_UNIT_TYPES = frozenset({1, 2, 3, 4, 5, 6, 7})
CONTRACT_PERIOD_TYPES = frozenset({1, 2, 3, 4, 5, 6})
PHONE_TYPES = frozenset({1, 2})

CARD_FIELDS = [
    "hasAnnex",
    "id",
    "title",
    "purchasingUnit",
    "areaName",
    "infoType",
    "budgetAmount",
    "biddingAmount",
    "winningBidderUnit",
    "publishTime",
    "url",
]

DETAIL_FIELDS = [
    "id",
    "title",
    "areaName",
    "purchasingUnit",
    "publishTime",
    "infoType",
    "registrationEndTime",
    "biddingEndTime",
    "openBidingTime",
    "budgetAmount",
    "purchasingUnitLinkName",
    "purchasingUnitLinkPhone",
    "winningBidderUnit",
    "winningBidderUnitLinkName",
    "winningBidderUnitLinkPhone",
    "winningBidderAmount",
    "agencyUnit",
    "agencyUnitLinkName",
    "agencyUnitLinkPhone",
    "url",
    "targetKeywords",
    "planPurchaseDate",
    "purchaseContent",
    "serviceStartTime",
    "serviceExpireTime",
    "contractAmount",
    "contractPeriod",
]

CARD_VISIBLE_FIELDS = {
    "title",
    "purchasingUnit",
    "areaName",
    "publishTime",
    "infoType",
    "budgetAmount",
    "biddingAmount",
    "winningBidderUnit",
    "url",
}

PROJECT_DETAIL_FIELDS = [
    "id",
    "title",
    "areaName",
    "purchasingUnit",
    "publishTime",
    "infoType",
    "registrationEndTime",
    "biddingEndTime",
    "openBidingTime",
    "budgetAmount",
    "purchasingUnitLinkName",
    "purchasingUnitLinkPhone",
    "winningBidderUnit",
    "winningBidderUnitLinkName",
    "winningBidderUnitLinkPhone",
    "winningBidderAmount",
    "agencyUnit",
    "agencyUnitLinkName",
    "agencyUnitLinkPhone",
    "url",
    "targetKeywords",
]
PURCHASE_DETAIL_FIELDS = [
    "id",
    "title",
    "publishTime",
    "budgetAmount",
    "planPurchaseDate",
    "purchasingUnit",
    "areaName",
    "purchaseContent",
    "url",
]
EXPIRING_DETAIL_FIELDS = [
    "id",
    "title",
    "areaName",
    "purchasingUnit",
    "publishTime",
    "serviceStartTime",
    "serviceExpireTime",
    "contractAmount",
    "contractPeriod",
    "budgetAmount",
    "purchasingUnitLinkName",
    "purchasingUnitLinkPhone",
    "winningBidderUnit",
    "winningBidderUnitLinkName",
    "winningBidderUnitLinkPhone",
    "agencyUnit",
    "agencyUnitLinkName",
    "agencyUnitLinkPhone",
    "url",
    "targetKeywords",
]
NEW_PROJECT_DETAIL_FIELDS = [
    "xmNumber", "threeLevelClassification", "zhaoBiaoType", "registrationBeginTime",
    "tenderBeginTime", "bidingAcquireTime", "bidingEndTime", "biddingCandidates",
]
PROJECT_DETAIL_FIELDS += NEW_PROJECT_DETAIL_FIELDS
DETAIL_FIELDS += NEW_PROJECT_DETAIL_FIELDS
DETAIL_FIELDS_BY_RESULT_TYPE: dict[str, tuple[str, ...]] = {
    "project": tuple(PROJECT_DETAIL_FIELDS),
    "purchase_intention": tuple(PURCHASE_DETAIL_FIELDS),
    "expiring_project": tuple(EXPIRING_DETAIL_FIELDS),
}
SOURCE_URL_RESULT_TYPES = frozenset({"project", "expiring_project"})
DETAIL_FIELD_SET = set(DETAIL_FIELDS) | {"sourceUrl"}

DETAIL_FIELD_META: dict[str, dict[str, str]] = {
    "areaName": {"label": "地区", "group": "项目概况"},
    "purchasingUnit": {"label": "采购单位", "group": "项目概况"},
    "publishTime": {"label": "发布时间", "group": "项目概况"},
    "infoType": {"label": "当前阶段", "group": "项目概况"},
    "budgetAmount": {"label": "预算金额（万元）", "group": "项目概况"},
    "winningBidderUnit": {"label": "中标单位", "group": "项目概况"},
    "winningBidderAmount": {"label": "中标金额（万元）", "group": "项目概况"},
    "targetKeywords": {"label": "标的物", "group": "项目概况"},
    "registrationEndTime": {"label": "报名截止时间", "group": "时间安排"},
    "biddingEndTime": {"label": "投标截止时间", "group": "时间安排"},
    "openBidingTime": {"label": "开标日期", "group": "时间安排"},
    "purchasingUnitLinkName": {"label": "采购单位联系人", "group": "相关单位"},
    "purchasingUnitLinkPhone": {"label": "采购单位联系方式", "group": "相关单位"},
    "winningBidderUnitLinkName": {"label": "中标单位联系人", "group": "相关单位"},
    "winningBidderUnitLinkPhone": {"label": "中标单位联系方式", "group": "相关单位"},
    "agencyUnit": {"label": "代理机构", "group": "相关单位"},
    "agencyUnitLinkName": {"label": "代理机构联系人", "group": "相关单位"},
    "agencyUnitLinkPhone": {"label": "代理机构联系方式", "group": "相关单位"},
    "sourceUrl": {"label": "原文链接", "group": "链接"},
    "planPurchaseDate": {"label": "预计采购时间", "group": "项目概况"},
    "purchaseContent": {"label": "采购需求", "group": "项目概况"},
    "serviceStartTime": {"label": "服务开始时间", "group": "项目概况"},
    "serviceExpireTime": {"label": "服务到期时间", "group": "项目概况"},
    "contractAmount": {"label": "合同金额（万元）", "group": "项目概况"},
    "contractPeriod": {"label": "合同周期", "group": "项目概况"},
}

DETAIL_FIELD_META.update({
    "xmNumber": {"label": "项目编号", "group": "项目概况"},
    "threeLevelClassification": {"label": "采购分类", "group": "项目概况"},
    "zhaoBiaoType": {"label": "采购方式", "group": "项目概况"},
    "registrationBeginTime": {"label": "报名开始时间", "group": "时间安排"},
    "tenderBeginTime": {"label": "投标开始时间", "group": "时间安排"},
    "bidingAcquireTime": {"label": "标书获取开始时间", "group": "时间安排"},
    "bidingEndTime": {"label": "标书获取截止时间", "group": "时间安排"},
    "biddingCandidates": {"label": "第二、第三候选人", "group": "相关单位"},
})

DETAIL_SUPPLEMENT_GROUPS = ["项目概况", "时间安排", "相关单位"]

BUSINESS_INFO_FIELDS: tuple[tuple[str, str], ...] = (
    ("name", "企业名称"),
    ("regStatus", "经营状态"),
    ("companyOrgType", "企业类型"),
    ("legalPersonName", "法定代表人"),
    ("regCapital", "注册资本"),
    ("estiblishTime", "成立日期"),
    ("regNumber", "工商注册号"),
    ("orgNumber", "组织机构代码"),
    ("creditCode", "统一社会信用代码"),
    ("industry", "所属行业"),
    ("businessTerm", "营业期限"),
    ("approvedTime", "核准日期"),
    ("regInstitute", "登记机关"),
    ("regLocation", "注册地址"),
    ("businessScope", "经营范围"),
)

PURCHASE_CARD_FIELDS = [
    "id",
    "title",
    "publishTime",
    "budgetAmount",
    "planPurchaseDate",
    "purchasingUnit",
    "areaName",
    "url",
]

EXPIRING_CARD_FIELDS = [
    "id",
    "title",
    "areaName",
    "purchasingUnit",
    "publishTime",
    "serviceStartTime",
    "serviceExpireTime",
    "contractAmount",
    "contractPeriod",
    "budgetAmount",
    "winningBidderUnit",
    "url",
]

FOLLOWUP_STAGE_RULES: dict[str, dict[str, Any]] = {
    "招标公告": {
        "text": "看第 {index} 条的投标截止时间和联系人",
        "fields": ["biddingEndTime", "purchasingUnitLinkName", "purchasingUnitLinkPhone"],
    },
    "重新招标": {
        "text": "看第 {index} 条的投标截止时间和联系人",
        "fields": ["biddingEndTime", "purchasingUnitLinkName", "purchasingUnitLinkPhone"],
    },
    "招标预告": {
        "text": "看第 {index} 条的联系人和标的物",
        "fields": ["purchasingUnitLinkName", "purchasingUnitLinkPhone", "targetKeywords"],
    },
    "采购意向": {
        "text": "看第 {index} 条的联系人和标的物",
        "fields": ["purchasingUnitLinkName", "purchasingUnitLinkPhone", "targetKeywords"],
    },
    "候选人公示": {
        "text": "看第 {index} 条的中标单位联系人和代理机构",
        "fields": ["winningBidderUnitLinkName", "winningBidderUnitLinkPhone", "agencyUnit"],
    },
    "中标通知": {
        "text": "看第 {index} 条的中标单位联系人和代理机构",
        "fields": ["winningBidderUnitLinkName", "winningBidderUnitLinkPhone", "agencyUnit"],
    },
    "合同公告": {
        "text": "看第 {index} 条的中标单位联系人和代理机构",
        "fields": ["winningBidderUnitLinkName", "winningBidderUnitLinkPhone", "agencyUnit"],
    },
    "废标公告": {
        "text": "看第 {index} 条的联系人和代理机构",
        "fields": ["purchasingUnitLinkName", "purchasingUnitLinkPhone", "agencyUnit"],
    },
    "流标公告": {
        "text": "看第 {index} 条的联系人和代理机构",
        "fields": ["purchasingUnitLinkName", "purchasingUnitLinkPhone", "agencyUnit"],
    },
    "信息变更": {
        "text": "看第 {index} 条的联系人和代理机构",
        "fields": ["purchasingUnitLinkName", "purchasingUnitLinkPhone", "agencyUnit"],
    },
    "答疑公告": {
        "text": "看第 {index} 条的联系人和代理机构",
        "fields": ["purchasingUnitLinkName", "purchasingUnitLinkPhone", "agencyUnit"],
    },
    "开标公示": {
        "text": "看第 {index} 条的联系人和代理机构",
        "fields": ["purchasingUnitLinkName", "purchasingUnitLinkPhone", "agencyUnit"],
    },
    "_default": {
        "text": "看第 {index} 条的联系人和代理机构",
        "fields": ["purchasingUnitLinkName", "purchasingUnitLinkPhone", "agencyUnit"],
    },
}

PURCHASING_UNIT_TYPE_NAMES = {
    1: "医疗机构",
    2: "政府机构",
    3: "学校",
    4: "公安",
    5: "金融企业",
    6: "部队",
    7: "通信运营商",
}

INFO_TYPE_NAMES = {
    "1": {1: "意见征集", 2: "招标预告"},
    "0": {3: "招标公告", 4: "重新招标"},
    "2": {5: "信息变更", 6: "答疑公告"},
    "3": {7: "废标公告", 8: "流标公告", 9: "开标公示", 10: "候选人公示", 11: "中标通知", 12: "合同公告"},
    "4": {},
    "5": {13: "验收合同", 14: "违规公告", 15: "其他公告"},
}

INFO_TYPE_PARENT_NAMES = {
    "1": "招标预告",
    "0": "招标公告",
    "2": "招标变更",
    "3": "结果公示",
    "4": "国土",
    "5": "其他",
}


CHINESE_ORDINALS = {
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
    "十一": 11,
    "十二": 12,
    "十三": 13,
    "十四": 14,
    "十五": 15,
    "十六": 16,
    "十七": 17,
    "十八": 18,
    "十九": 19,
    "二十": 20,
}


class SkillError(Exception):
    def __init__(self, code: str, message: str, data: Any | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.data = data


QUERY_JSON_ERROR_MESSAGE = "查询条件格式不正确，请重新发起查询，或减少/确认筛选条件后再试。"
UNSUPPORTED_DETAIL_MESSAGE = "这类详情暂不支持，请改问联系人、联系电话、截止时间、开标日期、预算金额、中标金额、服务到期时间、详情页链接或原文链接。"
SERVICE_UNAVAILABLE_SUMMARY = "数据服务暂时不可用"
GENERAL_FAILURE_SUMMARY = "这次查询暂时没有处理成功"
WORD_LIST_LABELS = {
    "keywords": "关键词",
    "excludeWords": "排除词",
}
WORD_LIST_TYPE_MESSAGES = {
    "keywords": "关键词需要是文字，请提供项目、产品、服务或行业关键词后再查。",
    "excludeWords": "排除词需要是文字，请调整排除词后再查。",
}


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


API_RESPONSES: ContextVar[list[dict[str, Any]] | None] = ContextVar("api_responses", default=None)


def record_api_result(path: str, **result: Any) -> None:
    records = API_RESPONSES.get()
    if records is not None:
        records.append(copy.deepcopy({"path": path, **result}))


def transport_failure(path: str, code: str, message: str) -> SkillError:
    record_api_result(path, transport_error={"code": code, "message": message})
    return SkillError(code, message)


def accept_api_response(path: str, payload: Any) -> Any:
    if not isinstance(payload, dict) or "code" not in payload:
        error = SkillError("API_RESPONSE_UNREADABLE", "未取得可解析的 API 状态。")
        record_api_result(path, transport_error={"code": error.code, "message": error.message}, received=payload)
        raise error
    record_api_result(path, response=payload)
    if payload["code"] != 200:
        raise SkillError(str(payload["code"]), str(payload.get("msg") or "API 返回错误"), payload)
    return payload.get("data")


def api_command(func: Callable) -> Callable:
    """Keep received API outcomes independent of presentation and state storage."""
    @wraps(func)
    def wrapped(args: argparse.Namespace) -> dict[str, Any]:
        if API_RESPONSES.get() is not None:
            return func(args)
        records: list[dict[str, Any]] = []
        token = API_RESPONSES.set(records)
        try:
            local_error = None
            try:
                output = func(args)
            except Exception as exc:
                if not records:
                    raise
                local_error = exc
                output = {}
            if not records:
                if output.get("follow_up") is None:
                    output.pop("follow_up", None)
                return output
            # A supplemental wallet request must not replace the requested API's outcome.
            primary = [item for item in records if item["path"] != "/api/user/entitlement"] or records
            failures = [item for item in primary if item.get("response", {}).get("code") != 200]
            successes = [item for item in primary if item.get("response", {}).get("code") == 200]
            if failures:
                first = failures[0]
                cause = first.get("transport_error")
                response = first.get("response", {})
                error = SkillError(str(cause["code"] if cause else response.get("code")),
                                   str(cause["message"] if cause else response.get("msg") or "API 返回错误"))
                if not output or output.get("ok"):
                    output = failure_payload(stage=args.command, error=error)
                output["ok"] = False
                output["error_code"] = error.code
                if successes:
                    output["partial_success"] = True
            else:
                if local_error is not None or not output.get("ok"):
                    output = {"ok": True, "stage": args.command, "warnings": [],
                              "user_message": "查询成功，已保留查询结果。相关空值信息为未公示。",
                              "presentation_notice": "本次结果已保留，展示或后续操作暂受限制。",
                              "agent_instruction": "根据 api_responses 中的原始数据交付所需内容；字段空值为未公示。不要重试已成功的调用，不猜测 ID 或页码。"}
                output["ok"] = True
                output.pop("error_code", None)
            output["api_responses"] = records
            if output.get("follow_up") is None:
                output.pop("follow_up", None)
            return output
        finally:
            API_RESPONSES.reset(token)
    return wrapped


def parse_query_json(raw_value: str) -> dict[str, Any]:
    try:
        payload = json.loads(raw_value)
    except json.JSONDecodeError as exc:
        raise SkillError("INVALID_JSON", QUERY_JSON_ERROR_MESSAGE) from exc
    if not isinstance(payload, dict):
        raise SkillError("INVALID_JSON", QUERY_JSON_ERROR_MESSAGE)
    return payload


def today() -> str:
    return dt.datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, payload: Any) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(path.parent, 0o700)
        tmp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
        descriptor = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)
        os.chmod(tmp, 0o600)
        tmp.replace(path)
        os.chmod(path, 0o600)
    except OSError as exc:
        raise SkillError("STATE_STORE_UNAVAILABLE", "结果状态暂时无法安全保存。") from exc


def state_root() -> Path:
    explicit = str(os.environ.get("QIANLIMA_SKILL_STATE_DIR") or "").strip()
    if explicit:
        root = Path(explicit).expanduser()
    else:
        xdg_state = str(os.environ.get("XDG_STATE_HOME") or "").strip()
        base = Path(xdg_state).expanduser() if xdg_state else Path.home() / ".local" / "state"
        root = base / "qianlima-bidding-search"
    try:
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(root, 0o700)
    except OSError as exc:
        raise SkillError("STATE_STORE_UNAVAILABLE", "结果状态目录暂时不可用。") from exc
    return root


def ensure_state_store_writable(session_id: str) -> Path:
    session_dir = state_root() / session_id
    probe_path = session_dir / f".write-probe-{uuid.uuid4().hex}.tmp"
    try:
        if session_dir.exists():
            if not session_dir.is_dir() or not (session_dir.stat().st_mode & 0o200):
                raise OSError("session state directory is not writable")
        else:
            session_dir.mkdir(mode=0o700)
        os.chmod(session_dir, 0o700)
        descriptor = os.open(probe_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.close(descriptor)
        probe_path.unlink()
    except OSError as exc:
        try:
            probe_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise SkillError("STATE_STORE_UNAVAILABLE", "结果状态暂时无法安全保存。") from exc
    return session_dir


def canonical_uuid(raw_value: Any, *, code: str, label: str) -> str:
    text = str(raw_value or "").strip()
    if not text:
        raise SkillError(code, f"缺少{label}，无法继续使用上次结果。")
    try:
        return str(uuid.UUID(text))
    except (ValueError, AttributeError, TypeError) as exc:
        raise SkillError("INVALID_RESULT_SET_ID", f"{label}格式无效，无法继续使用上次结果。") from exc


def search_session_id(args: argparse.Namespace) -> str:
    raw_value = getattr(args, "session_id", None) or os.environ.get("QIANLIMA_SKILL_SESSION_ID")
    if raw_value:
        return canonical_uuid(raw_value, code="SESSION_ID_REQUIRED", label="会话编号")
    return str(uuid.uuid4())


def follow_up_context(args: argparse.Namespace) -> tuple[str | None, str]:
    session_value = getattr(args, "session_id", None) or os.environ.get("QIANLIMA_SKILL_SESSION_ID")
    session_id = canonical_uuid(session_value, code="SESSION_ID_REQUIRED", label="会话编号") if session_value else None
    result_set_id = canonical_uuid(
        getattr(args, "result_set_id", None),
        code="RESULT_SET_ID_REQUIRED",
        label="结果编号",
    )
    return session_id, result_set_id


def snapshot_path(session_id: str, result_set_id: str) -> Path:
    return state_root() / session_id / f"{result_set_id}.json"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def expires_at_iso() -> str:
    return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=state_ttl_seconds())).isoformat()


def state_ttl_seconds() -> int:
    raw_value = os.environ.get("QIANLIMA_SKILL_STATE_TTL_SECONDS", str(DEFAULT_STATE_TTL_SECONDS))
    try:
        return max(0, int(raw_value))
    except ValueError:
        return DEFAULT_STATE_TTL_SECONDS


def snapshot_is_expired(snapshot: dict[str, Any]) -> bool:
    expires_at = str(snapshot.get("expires_at") or "").strip()
    if not expires_at:
        return True
    try:
        expires = dt.datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
    except ValueError:
        return True
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=dt.timezone.utc)
    return dt.datetime.now(dt.timezone.utc) > expires


def validate_continuation_paging(query: dict[str, Any], result_type: str, *, require_complete: bool = True) -> None:
    """An executed query's page size must be exact, never silently clamped."""
    size_field, maximum = ("pageSize", 20) if result_type == "company_candidates" else ("numPerPage", 100)
    fields = ("currentPage", size_field)
    missing = [field for field in fields if field not in query]
    if require_complete and missing:
        raise SkillError("FOLLOW_UP_UNAVAILABLE", "原查询缺少准确分页：" + "、".join(missing) + "。", {"missing_fields": missing})
    for field in fields:
        if field not in query:
            continue
        if type(query[field]) is not int or query[field] < 1:
            raise SkillError("INVALID_QUERY", f"原查询 {field} 需要准确的正整数，不能猜测分页。")
    if size_field in query and query[size_field] > maximum:
        raise SkillError("INVALID_QUERY", f"原查询 {size_field} 超出上限 {maximum}，不能改小页大小继续；需要准确的原分页条件。")


def validate_snapshot(snapshot: Any, session_id: str, result_set_id: str, *, for_query: bool = True) -> dict[str, Any]:
    if not isinstance(snapshot, dict):
        raise SkillError("RESULT_SET_CORRUPT", "结果状态内容损坏。")
    if snapshot.get("state_version") != STATE_VERSION:
        raise SkillError("RESULT_SET_CORRUPT", "结果状态版本不兼容。")
    if snapshot.get("session_id") != session_id:
        raise SkillError("RESULT_SET_CORRUPT", "结果状态中的创建会话编号与保存目录不一致。")
    if snapshot.get("result_set_id") != result_set_id:
        raise SkillError("RESULT_SET_CORRUPT", "结果状态编号不一致。")
    if snapshot.get("result_type") not in {*SEARCH_CAPABILITIES, "company_candidates"}:
        raise SkillError("RESULT_SET_CORRUPT", "结果状态的数据类型无效。")
    effective_query = snapshot.get("effective_query")
    cards = snapshot.get("cards")
    if not isinstance(cards, list) or any(not isinstance(card, dict) for card in cards):
        raise SkillError("RESULT_SET_CORRUPT", "结果状态内容不完整。")
    if for_query and snapshot_is_expired(snapshot):
        raise SkillError("RESULT_SET_EXPIRED", "上次结果状态已过期。")
    if not for_query:
        if not isinstance(effective_query, dict):
            snapshot["effective_query"] = {}
        return snapshot
    if not isinstance(effective_query, dict):
        raise SkillError("RESULT_SET_CORRUPT", "结果状态中的查询条件不完整。")
    try:
        validate_continuation_paging(effective_query, snapshot["result_type"], require_complete=False)
    except SkillError as exc:
        raise SkillError("RESULT_SET_CORRUPT", exc.message) from exc
    if snapshot.get("result_type") == "project" and snapshot.get("origin") != "timeline":
        try:
            migrated = migrate_project_query(effective_query)
            # Keep historical scopes and time spans readable for refine. Every
            # search/next/refine validates the resulting query before execution.
            historical_ids = normalize_area_ids(migrated.pop("areaIds")) if "areaIds" in migrated else []
            normalized = normalize_query({**migrated, AMOUNT_UNIT_CONFIRMATION_FIELD: True}, check_time_span=False)[0]
            for page_field in ("currentPage", "numPerPage"):
                if page_field not in effective_query:
                    normalized.pop(page_field, None)
            if historical_ids:
                normalized["areaIds"] = historical_ids
            snapshot["effective_query"] = normalized
        except SkillError as exc:
            raise SkillError("RESULT_SET_CORRUPT", "结果条件不能安全迁移或校验，未重新查询。") from exc
    return snapshot


def find_result_owner(result_set_id: str) -> str | None:
    root = state_root()
    for session_dir in root.iterdir():
        if session_dir.is_dir() and (session_dir / f"{result_set_id}.json").exists():
            return session_dir.name
    return None


def load_snapshot(session_id: str | None, result_set_id: str, *, for_query: bool = True) -> dict[str, Any]:
    owner = find_result_owner(result_set_id)
    if owner is None:
        raise SkillError("RESULT_SET_NOT_FOUND", "没有找到上次结果状态。")
    path = snapshot_path(owner, result_set_id)
    try:
        with path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
    except json.JSONDecodeError as exc:
        raise SkillError("RESULT_SET_CORRUPT", "结果状态内容损坏。") from exc
    except OSError as exc:
        raise SkillError("STATE_STORE_UNAVAILABLE", "结果状态暂时无法读取。") from exc
    if for_query and isinstance(payload, dict) and snapshot_is_expired(payload):
        try:
            path.unlink()
        except OSError:
            pass
        raise SkillError("RESULT_SET_EXPIRED", "上次结果状态已过期。")
    return validate_snapshot(payload, owner, result_set_id, for_query=for_query)


def follow_up_metadata(snapshot: dict[str, Any]) -> dict[str, Any] | None:
    if not snapshot.get("result_set_id"):
        return None
    metadata = {
        "session_id": snapshot["session_id"],
        "result_set_id": snapshot["result_set_id"],
        "parent_result_set_id": snapshot.get("parent_result_set_id"),
        "expires_at": snapshot["expires_at"],
        "total_count": snapshot.get("total_count"),
        "allowed_actions": (["search-company --next"] if snapshot.get("result_type") == "company_candidates" else ["detail","full-text","attachments","timeline"] if snapshot.get("origin") == "timeline" else ["detail","next","refine","full-text","attachments","timeline"] if snapshot.get("result_type") == "project" else ["detail","next","refine"]),
    }
    for field in ("access_mode", "access_mode_source", "viewable_page_count", "max_viewable_rows", "delivered_position", "seen_ids", "pending_cards"):
        if field in snapshot:
            metadata[field] = snapshot[field]
    if usable_count(snapshot.get("page_count")) is None:
        metadata["limitation"] = "总页数未公示，下一页按已执行页码继续。"
    query = snapshot.get("effective_query") or {}
    if snapshot.get("origin") != "timeline":
        try:
            validate_continuation_paging(query, snapshot["result_type"])
        except SkillError:
            metadata["allowed_actions"] = [action for action in metadata["allowed_actions"] if action not in {"next", "refine", "search-company --next"}]
            metadata["limitation"] = "查询分页信息不足或超限，不能自动续查；已定位公告仍可读取。"
    notice = free_continuation_notice(snapshot)
    if notice:
        metadata["allowed_actions"] = [action for action in metadata["allowed_actions"] if action != "next"]
        metadata["limitation"] = notice
    if snapshot_is_expired(snapshot):
        metadata["allowed_actions"] = [action for action in metadata["allowed_actions"] if action not in {"next", "refine", "search-company --next"}]
        metadata["limitation"] = "查询状态已过期；仍可按完整名单定位公告读取。"
    cards = snapshot.get("cards")
    if snapshot.get("result_type") != "company_candidates" and (not isinstance(cards, list) or any(not isinstance(card, dict) or not usable_project_id(card.get("id")) for card in cards)):
        metadata["allowed_actions"] = [action for action in metadata["allowed_actions"] if action not in {"detail", "full-text", "attachments", "timeline"}]
        metadata["limitation"] = "部分结果缺少可定位编号，暂不能按序号追问。"
    return metadata


def usable_count(value: Any) -> int | None:
    """Interpret paging metadata only; never replace the original API value."""
    if type(value) is int and value >= 0:
        return value
    if isinstance(value, str) and value.isascii() and value.isdigit():
        return int(value)
    return None


def save_search_snapshot(
    *,
    session_id: str,
    result_type: str,
    effective_query: dict[str, Any],
    viewed_cards: list[dict[str, Any]],
    total_count: int,
    page_count: int,
    parent_result_set_id: str | None = None,
    access_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result_set_id = str(uuid.uuid4())
    timestamp = now_iso()
    snapshot = {
        "state_version": STATE_VERSION,
        "session_id": session_id,
        "result_set_id": result_set_id,
        "parent_result_set_id": parent_result_set_id,
        "created_at": timestamp,
        "updated_at": timestamp,
        "expires_at": expires_at_iso(),
        "result_type": result_type,
        "effective_query": effective_query,
        "cards": viewed_cards,
        "total_count": total_count,
        "page_count": page_count,
        "focus_project": None,
    }
    snapshot.update(access_state or {})
    save_json(snapshot_path(session_id, result_set_id), snapshot)
    return snapshot


def save_snapshot(snapshot: dict[str, Any]) -> None:
    snapshot["updated_at"] = now_iso()
    snapshot["expires_at"] = expires_at_iso()
    save_json(snapshot_path(snapshot["session_id"], snapshot["result_set_id"]), snapshot)


def save_focus_project(snapshot: dict[str, Any], project: dict[str, Any]) -> None:
    if not snapshot.get("result_set_id") or snapshot_is_expired(snapshot):
        return
    snapshot["focus_project"] = dict(project)
    save_snapshot(snapshot)


def cleanup_expired_snapshots() -> None:
    root = state_root()
    for session_dir in list(root.iterdir()):
        if not session_dir.is_dir():
            continue
        for path in list(session_dir.glob("*.json")):
            try:
                payload = load_json(path, {})
            except (json.JSONDecodeError, OSError):
                continue
            if isinstance(payload, dict) and snapshot_is_expired(payload):
                try:
                    path.unlink()
                except OSError:
                    continue
        try:
            if not any(session_dir.iterdir()):
                session_dir.rmdir()
        except OSError:
            continue


def maintain_query_cache() -> None:
    """Clean after business success without making local maintenance a gate."""
    try:
        cleanup_expired_snapshots()
    except (OSError, SkillError):
        pass


def canonical_project_id(value: Any) -> str:
    return str(value).strip()


def usable_project_id(value: Any) -> bool:
    return type(value) in (int, str) and str(value).isascii() and str(value).isdigit()


def project_id_for_request(project: dict[str, Any]) -> str:
    if not usable_project_id(project.get("id")):
        raise SkillError("FOLLOW_UP_UNAVAILABLE", "该条项目编号未公示或无法定位，暂不能获取详情；已有查询结果仍可使用。")
    return canonical_project_id(project["id"])


def numeric_query_value(value: Any, label: str) -> float:
    try:
        result = float(str(value).replace(",", "").strip())
        if not math.isfinite(result):
            raise ValueError
        return result
    except (TypeError, ValueError) as exc:
        raise SkillError("INVALID_QUERY", f"{label}需要是数字，请您确认金额后再查。") from exc


def correction_error(
    code: str,
    message: str,
    agent_instruction: str,
    **extra: Any,
) -> SkillError:
    data = {
        "requires_agent_correction": True,
        "requires_user_confirmation": False,
        "agent_instruction": agent_instruction,
    }
    data.update(extra)
    return SkillError(code, message, data)


def reject_unsupported_fields(raw: dict[str, Any], allowed_fields: frozenset[str], endpoint_label: str) -> None:
    unsupported = sorted(str(field) for field in raw if field not in allowed_fields)
    if not unsupported:
        return
    raise correction_error(
        "AGENT_QUERY_CORRECTION_REQUIRED",
        f"{endpoint_label}包含不支持的查询字段。",
        f"删除不支持字段：{', '.join(unsupported)}；只保留当前端点允许的字段后重试，不要询问用户。",
        unsupported_fields=unsupported,
        allowed_fields=sorted(allowed_fields - {AMOUNT_UNIT_CONFIRMATION_FIELD}),
    )


def normalize_int_enum(value: Any, field: str, allowed: frozenset[int]) -> int:
    try:
        if isinstance(value, bool) or isinstance(value, float) and not value.is_integer():
            raise ValueError
        normalized = int(value)
    except (TypeError, ValueError) as exc:
        raise correction_error(
            "AGENT_QUERY_CORRECTION_REQUIRED",
            f"{field} 的值不符合当前端点契约。",
            f"按当前端点支持的枚举值 {sorted(allowed)} 修正 {field} 后重试，不要询问用户。",
            invalid_field=field,
            allowed_values=sorted(allowed),
        ) from exc
    if normalized not in allowed:
        raise correction_error(
            "AGENT_QUERY_CORRECTION_REQUIRED",
            f"{field} 的值不符合当前端点契约。",
            f"按当前端点支持的枚举值 {sorted(allowed)} 修正 {field} 后重试，不要询问用户。",
            invalid_field=field,
            allowed_values=sorted(allowed),
        )
    return normalized


def normalize_int_list_enum(value: Any, field: str, allowed: frozenset[int]) -> list[int]:
    values = value if isinstance(value, list) else [value]
    normalized = [normalize_int_enum(item, field, allowed) for item in values]
    if not normalized:
        raise correction_error(
            "AGENT_QUERY_CORRECTION_REQUIRED",
            f"{field} 不能为空数组。",
            f"删除空的 {field}，或按当前端点支持的枚举值 {sorted(allowed)} 重新设置，不要询问用户。",
            invalid_field=field,
            allowed_values=sorted(allowed),
        )
    return normalized


def normalize_purchase_match_scopes(value: Any, *, strict: bool = False) -> list[int]:
    # Preserve the CLI's existing numeric coercion; the transport accepts only
    # canonical arrays. Neither path drops or substitutes an unsupported scope.
    try:
        if strict and (not isinstance(value, list) or not value or any(
            type(item) is not int or item not in PURCHASE_MATCH_SCOPES for item in value
        )):
            raise ValueError
        return normalize_int_list_enum(value, "matchScopes", PURCHASE_MATCH_SCOPES)
    except (SkillError, ValueError):
        raise correction_error(
            "AGENT_QUERY_CORRECTION_REQUIRED",
            "采购意向 matchScopes 必须是仅包含 1、2、8、10 的非空整数数组。",
            "按用户已明确的检索位置修正：1=标题+正文+附件，2=标题，8=正文，10=附件。"
            "未指定位置时可省略；不得删除非法元素、改用默认范围或替换位置来放宽条件。"
            "采购意向不支持编号、采购单位、中标单位、代理机构、联系人、标的物专用位置；"
            "不能等价表达时说明能力限制，不自动重查。",
            invalid_field="matchScopes",
            allowed_values=sorted(PURCHASE_MATCH_SCOPES),
        )


def validate_date_order(query: dict[str, Any], begin_field: str, end_field: str, message: str) -> None:
    if not query.get(begin_field) or not query.get(end_field):
        return
    begin_date = dt.datetime.strptime(str(query[begin_field]), "%Y-%m-%d").date()
    end_date = dt.datetime.strptime(str(query[end_field]), "%Y-%m-%d").date()
    if begin_date > end_date:
        raise SkillError("INVALID_QUERY", message)


def validate_month_order(query: dict[str, Any], begin_field: str, end_field: str, message: str) -> None:
    if not query.get(begin_field) or not query.get(end_field):
        return
    begin_month = dt.datetime.strptime(str(query[begin_field]), "%Y-%m")
    end_month = dt.datetime.strptime(str(query[end_field]), "%Y-%m")
    if begin_month > end_month:
        raise SkillError("INVALID_QUERY", message)


def validate_time_span(
    query: dict[str, Any], begin_field: str, end_field: str,
    years: int, label: str, *, date_format: str = "%Y-%m-%d",
) -> None:
    """Check an inclusive calendar span without changing either endpoint."""
    if not query.get(begin_field) or not query.get(end_field):
        return
    try:
        start = dt.datetime.strptime(str(query[begin_field]), date_format)
        end = dt.datetime.strptime(str(query[end_field]), date_format)
    except ValueError as exc:
        raise SkillError("INVALID_QUERY", f"{label}格式无效，请调整时间条件后再查。") from exc
    if start > end:
        raise SkillError("INVALID_QUERY", f"{label}开始不能晚于结束。")
    if start.year + years > 9999:
        return  # Every representable end is within the limit.
    limit = start.replace(year=start.year + years,
                          day=min(start.day, calendar.monthrange(start.year + years, start.month)[1]))
    # Date-only project queries are normalized to full days. Preserve that
    # inclusive boundary after normalization, paging and transport validation.
    if start.time() == dt.time.min and end.time() == dt.time(23, 59, 59):
        limit = limit.replace(hour=23, minute=59, second=59)
    if end > limit:
        raise SkillError("TIME_SPAN_EXCEEDED",
                         f"{label}跨度最多 {years} 年，当前范围为 {query[begin_field]} 至 {query[end_field]}。"
                         "请调整起止时间后再查；本次未执行搜索，未截短或拆分时间范围。")


def validate_purchase_time_spans(query: dict[str, Any]) -> None:
    validate_time_span(query, "beginTime", "endTime", 3, "采购意向公告发布时间")
    validate_time_span(query, "startPlanPurchaseDate", "endPlanPurchaseDate", 3,
                       "预计采购时间", date_format="%Y-%m")


def amount_confirmation_instruction(amount: float) -> str:
    multiplied = amount * 10000
    multiplied_text = str(int(multiplied)) if multiplied.is_integer() else str(multiplied)
    amount_text = str(int(amount)) if amount.is_integer() else str(amount)
    return (
        "接口金额单位是元。回看用户原话检查是否漏乘 10000；"
        f"若用户说 {amount_text} 万，应传 {multiplied_text}。"
        f"若用户确实要查 {amount_text} 元，携带 {AMOUNT_UNIT_CONFIRMATION_FIELD}: true 按原值重试，不要询问用户。"
    )


def validate_amount_unit(
    query: dict[str, Any],
    fields: tuple[tuple[str, str], ...] = (("beginAmount", "金额下限"), ("endAmount", "金额上限")),
) -> None:
    confirmed = query.get(AMOUNT_UNIT_CONFIRMATION_FIELD) is True
    for field, label in fields:
        if field not in query:
            continue
        amount = numeric_query_value(query[field], label)
        if amount < 0:
            raise SkillError("INVALID_QUERY", "金额条件不能小于 0，请您确认后再查。")
        if 0 < amount < 10000 and not confirmed:
            raise correction_error(
                "AMOUNT_UNIT_SELF_CHECK_REQUIRED",
                "金额条件需要先完成单位自检。",
                amount_confirmation_instruction(amount),
                amount_field=field,
                amount_value=amount,
            )
        query[field] = amount


def validate_amount_order(query: dict[str, Any], begin_field: str, end_field: str) -> None:
    if begin_field in query and end_field in query and float(query[begin_field]) > float(query[end_field]):
        raise SkillError("INVALID_QUERY", "金额下限不能大于金额上限，请调整金额范围后再查。")


def validate_info_types(value: Any) -> dict[str, list[int]]:
    if value in (None, "", {}, []):
        return {}
    if not isinstance(value, dict):
        raise SkillError("INVALID_QUERY", "项目阶段条件格式不正确，请按一级阶段或明确二级阶段重新设置。")
    result: dict[str, list[int]] = {}
    for parent, children in value.items():
        parent_key = str(parent)
        if parent_key == "99":
            raise SkillError(
                "INVALID_QUERY",
                "采购意向不是普通项目阶段，请改用 search-purchase 查询采购意向。",
            )
        if parent_key not in INFO_TYPE_PARENT_NAMES:
            raise SkillError("INVALID_QUERY", "项目阶段条件不在支持范围内，请重新选择招标、中标、变更或答疑等阶段。")
        if children in (None, ""):
            child_values: list[int] = []
        elif isinstance(children, list):
            child_values = []
            for child in children:
                try:
                    child_values.append(int(child))
                except (TypeError, ValueError) as exc:
                    raise SkillError("INVALID_QUERY", "项目阶段条件格式不正确，请按一级阶段或明确二级阶段重新设置。") from exc
        else:
            try:
                child_values = [int(children)]
            except (TypeError, ValueError) as exc:
                raise SkillError("INVALID_QUERY", "项目阶段条件格式不正确，请按一级阶段或明确二级阶段重新设置。") from exc
        supported_children = INFO_TYPE_NAMES.get(parent_key, {})
        invalid_children = [child for child in child_values if child not in supported_children]
        if invalid_children:
            raise SkillError("INVALID_QUERY", "项目阶段条件不在支持范围内，请重新选择招标、中标、变更或答疑等阶段。")
        result[parent_key] = child_values
    return result


def int_query_value(value: Any, default: int, label: str, warnings: list[str]) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        warnings.append(f"{label}无法识别，已改为 {default}。")
        return default


def normalize_word_list(value: Any, field: str, warnings: list[str]) -> list[str]:
    values = value
    if isinstance(values, str):
        values = [values]
    elif not isinstance(values, list):
        raise SkillError("INVALID_QUERY", WORD_LIST_TYPE_MESSAGES.get(field, "查询条件需要是文字，请调整后再查。"))
    if any(not isinstance(item, str) for item in values):
        raise SkillError("INVALID_QUERY", WORD_LIST_TYPE_MESSAGES.get(field, "查询条件需要是文字，请调整后再查。"))
    values = [str(v).strip() for v in values if str(v).strip()]
    if len(values) > 10:
        label = WORD_LIST_LABELS.get(field, "条件")
        raise SkillError("INVALID_QUERY", f"{label}最多支持 10 个，不能丢弃部分条件后查询。")
    return values


def normalize_area_ids(value: Any) -> list[int]:
    try:
        return area_resolver.validate_ids(value)
    except area_resolver.AreaError as exc:
        raise SkillError("INVALID_QUERY", str(exc)) from exc


def normalize_area_filter(query: dict[str, Any]) -> None:
    if "areaIds" in query:
        ids = normalize_area_ids(query["areaIds"])
        validate_area_query_scope(ids)
        if ids:
            query["areaIds"] = ids
        else:
            query.pop("areaIds")


def validate_area_query_scope(ids: list[int]) -> None:
    message = area_resolver.catalog().scope_limit_message(ids)
    if message:
        raise SkillError("AREA_SCOPE_UNSUPPORTED", message)


def validate_required_keywords(query: dict[str, Any]) -> None:
    if not query.get("keywords"):
        raise SkillError("INVALID_QUERY", "关键词不能为空，请提供项目、产品、服务或行业关键词后再查。")


def normalize_keyword_groups(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        raise SkillError("INVALID_QUERY", "关键词不能为空，请按搜索意图设置关键词组和匹配位置。")
    result = []
    for group in value:
        if not isinstance(group, dict):
            raise SkillError("INVALID_QUERY", "每个关键词组必须包含关键词数组和匹配位置数组。")
        reject_unsupported_fields(group, frozenset({"keywords", "matchScopes"}), "关键词组")
        words = group.get("keywords")
        scopes = group.get("matchScopes")
        if not isinstance(words, list) or any(not isinstance(w, str) for w in words):
            raise SkillError("INVALID_QUERY", "关键词需要是文字数组，请按搜索意图设置关键词组。")
        words = [w.strip() for w in words if w.strip()]
        if not words or not isinstance(scopes, list) or not scopes:
            raise SkillError("INVALID_QUERY", "每组必须有至少一个非空关键词和一个匹配位置。")
        result.append({"keywords": words, "matchScopes": normalize_int_list_enum(scopes, "matchScopes", PROJECT_MATCH_SCOPES)})
    return result


def project_time(value: Any, *, end: bool = False) -> dt.datetime:
    text = str(value)
    pattern = r"\d{4}-\d{2}-\d{2}(?: \d{2}:\d{2}:\d{2})?"
    if not re.fullmatch(pattern, text):
        raise SkillError("INVALID_QUERY", "发布时间需为 YYYY-MM-DD 或 YYYY-MM-DD HH:mm:ss。")
    try:
        parsed = dt.datetime.strptime(text, "%Y-%m-%d" if len(text) == 10 else "%Y-%m-%d %H:%M:%S")
    except ValueError as exc:
        raise SkillError("INVALID_QUERY", "发布时间不是有效日期或时刻。") from exc
    if len(text) == 10 and end:
        parsed = parsed.replace(hour=23, minute=59, second=59)
    return parsed


def shift_project_month(value: dt.datetime, offset: int) -> dt.datetime:
    year, month0 = divmod(value.year * 12 + value.month - 1 + offset, 12)
    try:
        return value.replace(year=year, month=month0 + 1, day=min(value.day, calendar.monthrange(year, month0 + 1)[1]))
    except ValueError as exc:
        raise SkillError("INVALID_QUERY", "发布时间超出可查询的日期范围。") from exc


def normalize_query(raw: dict[str, Any], *, force_page: int | None = None, check_time_span: bool = True) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    reject_unsupported_fields(raw, PROJECT_SEARCH_FIELDS, "普通项目搜索")
    raw = dict(raw)
    normalize_area_filter(raw)
    query = {k: v for k, v in raw.items() if v is not None and v != ""}
    query["keywordGroups"] = normalize_keyword_groups(raw.get("keywordGroups"))
    query["currentPage"] = max(1, int_query_value(force_page if force_page is not None else query.get("currentPage", 1), 1, "页码", warnings))
    count = int_query_value(query.get("numPerPage", 30), 30, "每页数量", warnings)
    if count > 100:
        warnings.append("每页数量超过接口上限 100，已改为 100。")
    if count < 1:
        warnings.append("每页数量小于 1，已改为 30。")
    query["numPerPage"] = min(count, 100) if count > 0 else 30
    if "excludeWords" in query:
        query["excludeWords"] = normalize_word_list(query["excludeWords"], "excludeWords", warnings)
    start = project_time(query["beginTime"]) if query.get("beginTime") else None
    end = project_time(query["endTime"], end=True) if query.get("endTime") else None
    if start and not end:
        end = shift_project_month(start, 1)
        if len(str(query["beginTime"])) == 10:
            end = end.replace(hour=23, minute=59, second=59)
    elif end and not start:
        start = shift_project_month(end, -1)
        if len(str(query["endTime"])) == 10:
            start = start.replace(hour=0, minute=0, second=0)
    if start and end:
        if start > end:
            raise SkillError("INVALID_QUERY", "开始时间不能晚于结束时间，请调整时间范围后再查。")
        query["beginTime"] = start.strftime("%Y-%m-%d %H:%M:%S")
        query["endTime"] = end.strftime("%Y-%m-%d %H:%M:%S")
        if check_time_span:
            validate_time_span(query, "beginTime", "endTime", 3, "标讯发布时间", date_format="%Y-%m-%d %H:%M:%S")
    else:
        warnings.append("未传时间参数，接口默认按近一个月查询。")
    validate_amount_unit(query)
    validate_amount_order(query, "beginAmount", "endAmount")
    if "infoTypes" in query:
        query["infoTypes"] = validate_info_types(query["infoTypes"])
    normalize_area_filter(query)
    for field, allowed in (("procurementCategories", frozenset(range(4))), ("procurementMethods", PROCUREMENT_METHODS), ("fundsSources", frozenset(range(1,6))), ("purchasingUnitTypes", PURCHASING_UNIT_TYPES)):
        if field in query:
            query[field] = normalize_int_list_enum(query[field], field, allowed)
    if "sortType" in query:
        query["sortType"] = normalize_int_enum(query["sortType"], "sortType", SEARCH_SORT_TYPES)
    for field in ("hasAnnex", "hasAgency", "registrationStatus", "hasBiddingPhone", "hasWinningPhone"):
        if field in query:
            query[field] = normalize_int_enum(query[field], field, frozenset({0,1}))
    query.pop(AMOUNT_UNIT_CONFIRMATION_FIELD, None)
    return query, warnings


def migrate_project_query(query: dict[str, Any]) -> dict[str, Any]:
    """Only for persisted pre-upgrade snapshots, never for new Agent input."""
    result = dict(query)
    if "keywordGroups" in result:
        if any(k in result for k in ("keywords", "keywordsSearchType", "matchScopes", "procurementMethod")):
            raise SkillError("RESULT_SET_CORRUPT", "结果同时包含新旧搜索条件，不能安全迁移。")
        return result
    words = result.pop("keywords", None)
    scopes = result.pop("matchScopes", [2,8])
    mode = result.pop("keywordsSearchType", 1)
    if not isinstance(words, list) or not words or type(mode) is not int or mode not in (1,2):
        raise SkillError("RESULT_SET_CORRUPT", "旧结果关键词关系不完整，不能安全迁移。")
    result["keywordGroups"] = [{"keywords": [w], "matchScopes": scopes} for w in words] if mode == 2 else [{"keywords": words, "matchScopes": scopes}]
    if "procurementMethod" in result:
        result["procurementMethods"] = [result.pop("procurementMethod")]
    return result


def normalize_intelligence_query(
    raw: dict[str, Any],
    *,
    allowed_fields: frozenset[str],
    endpoint_label: str,
    match_scopes: frozenset[int],
    force_page: int | None = None,
    default_warning: str | None = None,
    default_warning_fields: tuple[str, ...] = (),
    require_service_expire_pair: bool = False,
    check_time_span: bool = True,
) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    reject_unsupported_fields(raw, allowed_fields, endpoint_label)
    query = dict(raw)
    if force_page is not None:
        query["currentPage"] = force_page
    query.setdefault("currentPage", 1)
    query.setdefault("numPerPage", 30)
    query["currentPage"] = int_query_value(query["currentPage"], 1, "页码", warnings)
    if query["currentPage"] < 1:
        warnings.append("页码小于 1，已改为 1。")
        query["currentPage"] = 1
    query["numPerPage"] = int_query_value(query["numPerPage"], 30, "每页数量", warnings)
    if query["numPerPage"] > 100:
        warnings.append("每页数量超过接口上限 100，已改为 100。")
        query["numPerPage"] = 100
    if query["numPerPage"] < 1:
        warnings.append("每页数量小于 1，已改为 30。")
        query["numPerPage"] = 30

    for field in ("keywords", "excludeWords"):
        if field in query and query[field] is not None:
            query[field] = normalize_word_list(query[field], field, warnings)
    validate_required_keywords(query)

    normalize_area_filter(query)

    for field in ("beginTime", "endTime", "beginServiceExpireTime", "endServiceExpireTime"):
        if field in query and query[field]:
            try:
                dt.datetime.strptime(str(query[field]), "%Y-%m-%d")
            except ValueError as exc:
                raise SkillError("INVALID_QUERY", "时间格式需要写成 YYYY-MM-DD，例如 2026-04-20。") from exc
    validate_date_order(query, "beginTime", "endTime", "开始时间不能晚于结束时间，请调整时间范围后再查。")
    validate_date_order(
        query,
        "beginServiceExpireTime",
        "endServiceExpireTime",
        "服务到期开始时间不能晚于结束时间，请调整后再查。",
    )
    if require_service_expire_pair and bool(query.get("beginServiceExpireTime")) != bool(query.get("endServiceExpireTime")):
        raise correction_error(
            "AGENT_QUERY_CORRECTION_REQUIRED",
            "临期项目的服务到期开始和结束日期必须成对传入。",
            "同时传 beginServiceExpireTime 和 endServiceExpireTime，或两个字段都不传后重试，不要询问用户。",
            invalid_fields=["beginServiceExpireTime", "endServiceExpireTime"],
        )
    for field in ("startPlanPurchaseDate", "endPlanPurchaseDate"):
        if field in query and query[field]:
            try:
                dt.datetime.strptime(str(query[field]), "%Y-%m")
            except ValueError as exc:
                raise SkillError("INVALID_QUERY", "预计采购时间需要写成 YYYY-MM，例如 2026-08。") from exc
    validate_month_order(
        query,
        "startPlanPurchaseDate",
        "endPlanPurchaseDate",
        "预计采购时间范围开始不能晚于结束，请确认后再查。",
    )

    if check_time_span and require_service_expire_pair:
        validate_time_span(query, "beginServiceExpireTime", "endServiceExpireTime", 5, "服务到期时间")

    amount_fields = tuple(
        (field, "金额")
        for field in (
            "startPlanPurchaseAmount",
            "endPlanPurchaseAmount",
            "beginContractAmount",
            "endContractAmount",
        )
        if field in allowed_fields
    )
    validate_amount_unit(query, amount_fields)
    validate_amount_order(query, "startPlanPurchaseAmount", "endPlanPurchaseAmount")
    validate_amount_order(query, "beginContractAmount", "endContractAmount")

    if "matchScopes" in query:
        query["matchScopes"] = normalize_int_list_enum(query["matchScopes"], "matchScopes", match_scopes)
    if "sortType" in query:
        query["sortType"] = normalize_int_enum(query["sortType"], "sortType", SEARCH_SORT_TYPES)
    if "procurementMethod" in query:
        query["procurementMethod"] = normalize_int_enum(query["procurementMethod"], "procurementMethod", PROCUREMENT_METHODS)
    if "purchasingUnitTypes" in query:
        query["purchasingUnitTypes"] = normalize_int_list_enum(
            query["purchasingUnitTypes"], "purchasingUnitTypes", PURCHASING_UNIT_TYPES
        )
    if "contractPeriodType" in query:
        query["contractPeriodType"] = normalize_int_enum(
            query["contractPeriodType"], "contractPeriodType", CONTRACT_PERIOD_TYPES
        )

    if default_warning:
        if not any(query.get(field) for field in default_warning_fields):
            warnings.append(default_warning)
    clean_query = {k: v for k, v in query.items() if v not in (None, "", [], {})}
    clean_query.pop(AMOUNT_UNIT_CONFIRMATION_FIELD, None)
    return clean_query, warnings


def card_view(card: Any) -> Any:
    return copy.deepcopy(card)


def purchase_card_view(card: Any) -> Any:
    return copy.deepcopy(card)


def expiring_card_view(card: Any) -> Any:
    return copy.deepcopy(card)


def detail_fields_for_result_type(result_type: str) -> tuple[str, ...]:
    try:
        return DETAIL_FIELDS_BY_RESULT_TYPE[result_type]
    except KeyError as exc:
        raise SkillError("RESULT_SET_CORRUPT", "结果状态的数据类型无效。") from exc


def detail_view(detail: Any, requested_fields: list[str] | None, result_type: str) -> Any:
    if not isinstance(detail, dict) or not requested_fields:
        return copy.deepcopy(detail)
    return {field: copy.deepcopy(detail[field]) for field in dict.fromkeys(["id", "title", *requested_fields]) if field in detail}


def clean_user_value(value: Any) -> str:
    if value in (None, ""):
        return EMPTY_DISPLAY
    if isinstance(value, list):
        values = [clean_user_value(item) for item in value]
        return "、".join(values) if values else EMPTY_DISPLAY
    text = str(value).replace("\n", " ").replace("|", "｜").strip()
    return text or EMPTY_DISPLAY


def format_amount_wan(value: Any) -> str:
    if value in (None, ""):
        return EMPTY_DISPLAY
    try:
        amount = float(str(value).replace(",", "").strip())
    except ValueError:
        return clean_user_value(value)
    return f"{amount / 10000:.2f}"


def format_query_amount_wan(value: Any) -> str:
    formatted = format_amount_wan(value)
    return formatted if formatted != EMPTY_DISPLAY else clean_user_value(value)


def format_detail_link(value: Any) -> str:
    text = clean_user_value(value)
    if text == EMPTY_DISPLAY:
        return text
    if text.startswith("http://") or text.startswith("https://"):
        return f"[查看详情]({text})"
    return text


def format_area_display(value: Any) -> str:
    text = clean_user_value(value)
    if text != EMPTY_DISPLAY and text.isdigit():
        names = area_display_names([text])
        if names:
            return names[0]
    return text


def format_list_area_display(value: Any) -> str:
    text = format_area_display(value)
    if text == EMPTY_DISPLAY:
        return text
    parts = [part.strip() for part in re.split(r"[-－—–/／>＞]", text) if part.strip()]
    deduped: list[str] = []
    for part in parts:
        if not deduped or deduped[-1] != part:
            deduped.append(part)
    return " / ".join(deduped) if deduped else text


def format_stage_display(value: Any) -> str:
    text = clean_user_value(value)
    if text == EMPTY_DISPLAY:
        return text
    parts = [part.strip() for part in re.split(r"[-－—–]", text) if part.strip()]
    return parts[-1] if parts else text


def is_pre_award_stage(value: Any) -> bool:
    text = clean_user_value(value)
    if text == EMPTY_DISPLAY:
        return False
    parts = [part.strip() for part in re.split(r"[-－—–]", text) if part.strip()]
    names = set(parts or [text])
    return bool(
        names
        & {
            "采购意向",
            "预告",
            "招标预告",
            "公告",
            "招标公告",
            "重新招标",
            "变更",
            "招标变更",
            "信息变更",
            "答疑公告",
        }
    )


def should_show_bidding_amount(cards: list[dict[str, Any]]) -> bool:
    return bool(cards) and not all(is_pre_award_stage(card.get("infoType")) for card in cards)


def numbered_card_lines(index: int, title: Any, fields: list[tuple[str, Any]]) -> list[str]:
    lines = [f"{index}. {clean_user_value(title)}"]
    for label, value in fields:
        lines.append(f"   - {label}：{clean_user_value(value)}")
    return lines


def is_account_home_link(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = urllib.parse.urlsplit(value)
    except ValueError:
        return False
    return (parsed.scheme in {"http", "https"}
            and parsed.hostname in {"ai.qianlima.com", "ai.atest.qianlima.com"}
            and parsed.path in {"", "/"})


def attach_free_link_facts(payload: dict[str, Any], cards: list[dict[str, Any]], *, has_key: bool) -> None:
    urls = [card.get("url") for card in cards if isinstance(card, dict) and isinstance(card.get("url"), str) and card.get("url")]
    homes = [url for url in urls if is_account_home_link(url)]
    issues = []
    if any(urllib.parse.parse_qs(urllib.parse.urlsplit(url).query).get("source") != [PACKAGE_SOURCE_CODE] for url in homes):
        issues.append("官网入口缺少或不符合约定的 source 参数")
    if not has_key and len(homes) != len(urls):
        issues.append("匿名免费响应的链接不是约定的官网入口")
    if issues:
        payload["link_contract_issues"] = issues
        payload["link_instruction"] = "公告名称附上实际返回的原始URL，官网入口不称公告详情或原文，不提示点击官网扣费；保留原始响应，不自行构造详情凭证。接入引导仍使用文档规定的完整账号链接。"
    if has_key and len(urls) > len(homes):
        payload["link_notice"] = "点击查看公告详情会消耗账号积分。"


def user_card_list(cards: list[dict[str, Any]]) -> list[str]:
    if not cards:
        return ["这一批没有更多项目。"]
    show_bidding_amount = should_show_bidding_amount(cards)
    lines: list[str] = []
    for index, card in enumerate(cards, start=1):
        fields: list[tuple[str, Any]] = [
            ("招标单位", card.get("purchasingUnit")),
            ("地区", format_list_area_display(card.get("areaName"))),
            ("发布时间", card.get("publishTime")),
            ("当前阶段", format_stage_display(card.get("infoType"))),
            ("预算金额（万元）", format_amount_wan(card.get("budgetAmount"))),
        ]
        if show_bidding_amount:
            fields.append(("中标金额（万元）", format_amount_wan(card.get("biddingAmount"))))
        if clean_user_value(card.get("winningBidderUnit")) != EMPTY_DISPLAY:
            fields.append(("中标单位", card.get("winningBidderUnit")))
        title = clean_user_value(card.get("title"))
        url = card.get("url")
        if isinstance(url, str) and url.startswith(("https://", "http://")):
            label = title.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")
            destination = f"<{url}>" if "(" in url or ")" in url else url
            title = f"[{label}]({destination})"
        lines.extend(numbered_card_lines(index, title, fields))
    return lines


def user_purchase_card_list(cards: list[dict[str, Any]]) -> list[str]:
    if not cards:
        return ["这一批没有更多采购意向。"]
    lines: list[str] = []
    for index, card in enumerate(cards, start=1):
        lines.extend(
            numbered_card_lines(
                index,
                card.get("title"),
                [
                    ("采购单位", card.get("purchasingUnit")),
                    ("地区", format_list_area_display(card.get("areaName"))),
                    ("发布日期", card.get("publishTime")),
                    ("预计采购时间", card.get("planPurchaseDate")),
                    ("预算金额（万元）", format_amount_wan(card.get("budgetAmount"))),
                    ("详情", format_detail_link(card.get("url"))),
                ],
            )
        )
    return lines


def user_expiring_card_list(cards: list[dict[str, Any]]) -> list[str]:
    if not cards:
        return ["这一批没有更多临期项目。"]
    lines: list[str] = []
    for index, card in enumerate(cards, start=1):
        lines.extend(
            numbered_card_lines(
                index,
                card.get("title"),
                [
                    ("采购单位", card.get("purchasingUnit")),
                    ("地区", format_list_area_display(card.get("areaName"))),
                    ("服务到期时间", card.get("serviceExpireTime")),
                    ("合同金额（万元）", format_amount_wan(card.get("contractAmount"))),
                    ("在位供应商", card.get("winningBidderUnit")),
                    ("详情", format_detail_link(card.get("url"))),
                ],
            )
        )
    return lines


def user_enterprise_list(kind: str, rows: list[dict[str, Any]]) -> list[str]:
    if not rows:
        return ["暂时没有查到对应企业情报。"]
    if kind == "contacts":
        title_field = "linkMan"
        field_sets = [("phoneType", clean_user_value), ("phone", clean_user_value)]
        labels = ["电话类型", "联系电话"]
    elif kind in {"partners", "principals"}:
        title_field = "companyName"
        field_sets = [("cooperationCount", clean_user_value), ("cooperationAmount", format_amount_wan)]
        labels = ["合作次数", "合作金额（万元）"]
    elif kind in {"area-distribution", "winning-area-distribution"}:
        amount_field = "winningAmount" if kind == "winning-area-distribution" else "cooperationAmount"
        count_field = "winningCount" if kind == "winning-area-distribution" else "cooperationCount"
        title_field = "areaName"
        field_sets = [(count_field, clean_user_value), (amount_field, format_amount_wan)]
        labels = ["次数", "金额（万元）"]
    elif kind == "co-bidder-competitors":
        title_field = "competitorName"
        field_sets = [("coBidderCount", clean_user_value), ("winningCount", clean_user_value), ("winningAmount", format_amount_wan), ("competitivenessLevel", clean_user_value)]
        labels = ["同场竞标次数", "中标次数", "中标金额（万元）", "竞争力等级"]
    elif kind == "potential-competitors":
        title_field = "competitorName"
        field_sets = [("winningCount", clean_user_value), ("winningAmount", format_amount_wan), ("competitivenessLevel", clean_user_value)]
        labels = ["中标次数", "中标金额（万元）", "竞争力等级"]
    elif kind == "business-info":
        row = rows[0]
        lines = []
        for index, (field, label) in enumerate(BUSINESS_INFO_FIELDS, start=1):
            if field in row:
                lines.append(f"{index}. {label}：{clean_user_value(row.get(field))}")
        return lines or ["暂时没有查到对应企业工商信息。"]
    else:
        lines: list[str] = []
        for index, (field, value) in enumerate(rows[0].items(), start=1):
            lines.append(f"{index}. {field}：{clean_user_value(value)}")
        return lines

    lines: list[str] = []
    for index, row in enumerate(rows, start=1):
        title = row.get(title_field)
        fields = [(label, formatter(row.get(field))) for label, (field, formatter) in zip(labels, field_sets)]
        lines.extend(numbered_card_lines(index, title, fields))
    return lines


def area_display_names(area_ids: list[Any]) -> list[str]:
    try:
        directory = area_resolver.catalog()
        return list(dict.fromkeys(directory.display_path(i) for i in normalize_area_ids(area_ids)))
    except area_resolver.AreaError as exc:
        raise SkillError("INVALID_QUERY", str(exc)) from exc


def area_records() -> list[dict[str, Any]]:
    return list(area_resolver.catalog().by_id.values())


def district_area_expansion(query: dict[str, Any]) -> dict[str, Any] | None:
    if not query.get("areaIds"):
        return None
    ids = normalize_area_ids(query["areaIds"])
    if len(ids) != 1:
        return None
    directory = area_resolver.catalog()
    parent = directory.city_parent(ids[0])
    if parent is None:
        return None
    return {
        "from_area_id": ids[0],
        "from_area_name": directory.candidate(ids[0])["path"],
        "to_area_id": parent,
        "to_area_name": directory.candidate(parent)["path"],
        "requires_confirmation": True,
        "refine_query": {"areaIds": [parent]},
    }


def area_expansion_prompt(expansion: dict[str, Any]) -> str:
    return (
        f"{expansion['from_area_name']}范围内未找到结果。"
        f"是否扩大到{expansion['to_area_name']}查询？只有您明确同意后，我才会重新查询。"
    )


def query_area_names(query: dict[str, Any]) -> list[str]:
    if query.get("areaNames"):
        return [str(value) for value in query["areaNames"] if str(value).strip()]
    if query.get("areaIds"):
        return area_display_names(query["areaIds"])
    return []


def normalized_info_types(value: Any) -> dict[str, list[int]]:
    if not isinstance(value, dict):
        return {}
    result: dict[str, list[int]] = {}
    for parent, children in value.items():
        if children in (None, ""):
            result[str(parent)] = []
        elif isinstance(children, list):
            result[str(parent)] = [int(child) for child in children]
        else:
            result[str(parent)] = [int(children)]
    return result


def resolution_method_label(resolution: dict[str, Any] | None) -> str:
    if not resolution:
        return ""
    method = resolution.get("method")
    if method == "ordinal":
        return "按结果序号定位"
    if method == "text":
        return "按你提供的标题或文字定位"
    if method == "project_id":
        return "按项目编号定位"
    return ""


def info_type_names(info_types: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for parent, children in info_types.items():
        parent_name = INFO_TYPE_PARENT_NAMES.get(str(parent), str(parent))
        if not children:
            names.append(parent_name)
            continue
        child_names = [INFO_TYPE_NAMES.get(str(parent), {}).get(int(child), str(child)) for child in children]
        names.extend(child_names or [parent_name])
    return names


MATCH_SCOPE_LABELS = {1:"标题、正文或附件",2:"标题",3:"项目编号",4:"采购单位",5:"中标单位",6:"代理机构",7:"联系人",8:"正文",9:"标的物",10:"附件"}
PROJECT_FILTER_LABELS = {
    "procurementCategories": ("采购分类", {0:"其他",1:"货物",2:"工程",3:"服务"}),
    "procurementMethods": ("采购方式", {0:"公开招标",1:"邀请招标",2:"竞争性谈判/磋商",3:"单一来源",4:"询价",5:"其它",6:"电子卖场"}),
    "fundsSources": ("资金来源", {1:"财政资金",2:"专项资金及债券",3:"银行贷款",4:"投资/融资",5:"单位自筹"}),
    "hasAnnex": ("附件", {0:"无附件",1:"有附件"}),
    "hasAgency": ("代理机构", {0:"无代理机构",1:"有代理机构"}),
    "hasBiddingPhone": ("采购单位电话", {0:"无电话",1:"有电话"}),
    "hasWinningPhone": ("中标单位电话", {0:"无电话",1:"有电话"}),
    "registrationStatus": ("报名状态", {0:"报名时间有记录且未截止",1:"报名时间已结束"}),
}


def project_query_phrases(query):
    parts=[]
    groups=query.get("keywordGroups") or []
    for group in groups:
        words="或".join(group["keywords"])
        scopes=group["matchScopes"]
        parts.append("/".join(MATCH_SCOPE_LABELS[n] for n in scopes) + "含“" + words + "”")
    if len(groups)>1:
        parts.append("各组关键词需同时命中")
    if groups and (query.get("beginAmount") is not None or query.get("endAmount") is not None):
        parts.append("预算或中标金额任一符合所设范围")
    for field,(label,mapping) in PROJECT_FILTER_LABELS.items():
        if field in query:
            values=query[field] if isinstance(query[field],list) else [query[field]]
            parts.append(label + "：" + "或".join(mapping[v] for v in values))
    return parts


def user_query_lines(query: dict[str, Any]) -> list[str]:
    lines: list[str] = project_query_phrases(query)
    if query.get("keywords"):
        lines.append(f"关键词：{'、'.join(map(str, query['keywords']))}")
        if query.get("keywordsSearchType") == 2:
            lines.append("关键词关系：同时命中")
        elif query.get("keywordsSearchType") == 1 and len(query.get("keywords") or []) > 1:
            lines.append("关键词关系：任一命中")
    if query.get("excludeWords"):
        lines.append(f"排除：{'、'.join(map(str, query['excludeWords']))}")
    if query.get("areaNames"):
        lines.append(f"地区：{'、'.join(map(str, query['areaNames']))}")
    elif query.get("areaIds"):
        area_names = area_display_names(query["areaIds"])
        if area_names:
            visible_names = area_names[:20]
            suffix = f"等 {len(area_names)} 个地区" if len(area_names) > len(visible_names) else ""
            lines.append(f"地区：{'、'.join(visible_names)}{suffix}")
        else:
            lines.append("地区：已按你指定的地区范围筛选")
    begin_time = query.get("beginTime")
    end_time = query.get("endTime")
    if begin_time or end_time:
        if begin_time and end_time:
            lines.append(f"时间：{begin_time} 至 {end_time}")
        elif begin_time:
            lines.append(f"时间：{begin_time} 之后")
        else:
            lines.append(f"时间：{end_time} 之前")
    if query.get("purchasingUnitTypes"):
        type_names = [PURCHASING_UNIT_TYPE_NAMES.get(int(value), str(value)) for value in query["purchasingUnitTypes"]]
        lines.append(f"采购单位：{'、'.join(type_names)}")
    if query.get("infoTypes"):
        lines.append(f"信息类型：{'、'.join(info_type_names(query['infoTypes']))}")
    begin_amount = query.get("beginAmount")
    end_amount = query.get("endAmount")
    if begin_amount is not None and end_amount is not None:
        lines.append(f"金额：{format_query_amount_wan(begin_amount)} 万元至 {format_query_amount_wan(end_amount)} 万元")
    elif begin_amount is not None:
        lines.append(f"金额：{format_query_amount_wan(begin_amount)} 万元以上")
    elif end_amount is not None:
        lines.append(f"金额：{format_query_amount_wan(end_amount)} 万元以下")
    if not lines:
        lines.append("未设置额外筛选条件")
    return lines


def user_query_sentence(query: dict[str, Any]) -> str:
    parts: list[str] = []
    area_names = query_area_names(query)
    if area_names:
        visible_names = area_names[:8]
        suffix = f"等 {len(area_names)} 个地区" if len(area_names) > len(visible_names) else ""
        parts.append("、".join(visible_names) + suffix)
    parts.extend(project_query_phrases(query))
    if query.get("keywords"):
        parts.append("关键词“" + "、".join(map(str, query["keywords"])) + "”")
        if query.get("keywordsSearchType") == 2:
            parts.append("关键词需同时命中")
        elif query.get("keywordsSearchType") == 1 and len(query.get("keywords") or []) > 1:
            parts.append("关键词任一命中")
    if query.get("excludeWords"):
        parts.append("排除“" + "、".join(map(str, query["excludeWords"])) + "”")
    if query.get("purchasingUnitTypes"):
        type_names = [PURCHASING_UNIT_TYPE_NAMES.get(int(value), str(value)) for value in query["purchasingUnitTypes"]]
        parts.append("采购单位为" + "、".join(type_names))
    if query.get("infoTypes"):
        parts.append("只看" + "、".join(info_type_names(query["infoTypes"])))
    begin_time = query.get("beginTime")
    end_time = query.get("endTime")
    if begin_time and end_time:
        parts.append(f"时间 {begin_time} 至 {end_time}")
    elif begin_time:
        parts.append(f"时间 {begin_time} 之后")
    elif end_time:
        parts.append(f"时间 {end_time} 之前")
    begin_amount = query.get("beginAmount")
    end_amount = query.get("endAmount")
    if begin_amount is not None and end_amount is not None:
        parts.append(f"金额 {format_query_amount_wan(begin_amount)} 万元至 {format_query_amount_wan(end_amount)} 万元")
    elif begin_amount is not None:
        parts.append(f"金额 {format_query_amount_wan(begin_amount)} 万元以上")
    elif end_amount is not None:
        parts.append(f"金额 {format_query_amount_wan(end_amount)} 万元以下")
    if not parts:
        return "我按您给出的条件查询了项目。"
    return "我按" + "，".join(parts) + "，查询了项目。"


def result_snapshot_lines(cards: list[dict[str, Any]]) -> list[str]:
    if not cards:
        return []
    stages: dict[str, int] = {}
    latest = ""
    max_amount: float | None = None
    for card in cards:
        stage = format_stage_display(card.get("infoType"))
        if stage != EMPTY_DISPLAY:
            stages[stage] = stages.get(stage, 0) + 1
        publish_time = clean_user_value(card.get("publishTime"))
        if publish_time != EMPTY_DISPLAY and publish_time > latest:
            latest = publish_time
        for field in ("budgetAmount", "biddingAmount"):
            raw = card.get(field)
            if raw in (None, ""):
                continue
            try:
                amount = float(str(raw).replace(",", "").strip())
            except ValueError:
                continue
            max_amount = amount if max_amount is None else max(max_amount, amount)
    lines: list[str] = []
    if stages:
        stage_text = "、".join(f"{name} {count} 条" for name, count in sorted(stages.items(), key=lambda item: item[0])[:3])
        lines.append(f"本批阶段分布：{stage_text}。")
    if latest:
        lines.append(f"本批最新发布时间：{latest}。")
    if max_amount is not None:
        lines.append(f"本批可见最高金额：{format_amount_wan(max_amount)} 万元。")
    return lines


def zero_result_reflection(effective_query: dict[str, Any]) -> list[str]:
    suggestions: list[str] = []
    expansion = district_area_expansion(effective_query)
    if expansion:
        return [area_expansion_prompt(expansion)]
    if effective_query.get("beginTime") or effective_query.get("endTime"):
        suggestions.append("可按需求扩大公告发布时间的起止范围，覆盖更多历史记录，但查询会变慢。")
    else:
        suggestions.append("当前默认查近一个月；可选择更长的具体时段，增加历史覆盖，但查询会变慢。")
    if effective_query.get("beginAmount") is not None or effective_query.get("endAmount") is not None:
        suggestions.append("若项目体量要求可调整，可放宽金额范围；结果也会包含原范围外的项目。")
    if effective_query.get("excludeWords"):
        first_exclude = str(effective_query["excludeWords"][0])
        suggestions.append(f"全文排除“{first_exclude}”可能误删仅在附带条款提及该词的公告；可先核对排除意图，再决定是否调整。")
    info_types = normalized_info_types(effective_query.get("infoTypes"))
    if any(children for children in info_types.values()):
        suggestions.append("可核对是否需要其他公告阶段；扩大阶段会增加不同业务状态的公告，需按查询目标选择。")
    if effective_query.get("purchasingUnitTypes"):
        suggestions.append("采购单位类型可能过窄，可以先不限定机构类型。")
    if effective_query.get("keywords") or effective_query.get("keywordGroups"):
        suggestions.append("可核对关键词拆分、组合与搜索位置；扩大内容范围可能增加覆盖，也会增加间接提及。")
    else:
        suggestions.append("可以补充项目关键词，例如设备、物业、食堂、空调。")
    if effective_query.get("areaIds") and len(effective_query["areaIds"]) == 1:
        suggestions.append("地区范围可能偏窄，可以扩大到省级或相邻城市。")
    deduped: list[str] = []
    for suggestion in suggestions:
        if suggestion not in deduped:
            deduped.append(suggestion)
    return deduped[:3]


def first_search_empty_lines(effective_query: dict[str, Any], reflections: list[str] | None = None) -> list[str]:
    lines = ["暂时没查到符合这些条件的项目。您可以尝试："]
    suggestion_values = reflections if reflections is not None else zero_result_reflection(effective_query)
    lines.extend(f"{index}. {line}" for index, line in enumerate(suggestion_values[:3], start=1))
    return lines


def followup_lines(effective_query: dict[str, Any], total_count: int, returned_count: int, cards: list[dict[str, Any]], *, allow_next: bool = True) -> list[str]:
    if not cards:
        return []
    suggestions: list[str] = []
    if allow_next and total_count > returned_count:
        suggestions.append("继续看下一批")

    detail_index = 2 if returned_count >= 2 else 1
    focus_card = cards[detail_index - 1] if len(cards) >= detail_index else cards[0]
    focus_stage = format_stage_display(focus_card.get("infoType"))
    detail_suggestion = stage_followup_text(focus_stage, detail_index)
    if detail_suggestion:
        suggestions.append(detail_suggestion)

    amount_relevant_stages = {"招标预告", "招标公告", "重新招标", "采购意向", "候选人公示", "中标通知", "合同公告"}
    stage_broaden_stages = {"废标公告", "流标公告", "信息变更", "答疑公告"}
    if focus_stage in stage_broaden_stages:
        suggestions.append("把项目阶段放宽一点")
    elif effective_query.get("beginAmount") is None and effective_query.get("endAmount") is None and focus_stage in amount_relevant_stages:
        suggestions.append("只看 100 万以上的")
    elif effective_query.get("beginAmount") is not None or effective_query.get("endAmount") is not None:
        suggestions.append("把金额条件放宽一点")
    elif not effective_query.get("beginTime") and not effective_query.get("endTime"):
        suggestions.append("把时间放宽到近三个月")

    deduped: list[str] = []
    for suggestion in suggestions:
        if suggestion not in deduped:
            deduped.append(suggestion)
    return ["您可以继续说："] + [f"- {suggestion}" for suggestion in deduped[:3]]


def followup_rule_is_valid(rule: dict[str, Any]) -> bool:
    fields = [str(field) for field in rule.get("fields") or []]
    return bool(fields) and all(field in DETAIL_FIELD_SET for field in fields) and not all(field in CARD_VISIBLE_FIELDS for field in fields)


def stage_followup_text(stage: str, index: int) -> str:
    rule = FOLLOWUP_STAGE_RULES.get(stage) or FOLLOWUP_STAGE_RULES["_default"]
    if not followup_rule_is_valid(rule):
        return ""
    return str(rule["text"]).format(index=index)


def user_search_message(
    *,
    success: bool,
    effective_query: dict[str, Any],
    total_count: int = 0,
    returned_count: int = 0,
    cards: list[dict[str, Any]] | None = None,
    warnings: list[str] | None = None,
    next_page: bool = False,
    failure: bool = False,
    include_query_conditions: bool = True,
    zero_reflections: list[str] | None = None,
    continuation_notice: str | None = None,
) -> str:
    lines: list[str] = []
    if next_page:
        lines.append("当前查询条件未变，继续展示下一批。")
        lines.append("")
    elif failure:
        lines.append("这次查询没有成功。")
        lines.append("")
    if include_query_conditions:
        lines.append(user_query_sentence(effective_query))
        lines.append("")
    if success:
        lines.append(f"共找到 {total_count} 条，本次展示 {returned_count} 条。")
        lines.append("")
        card_values = cards or []
        if returned_count == 0 and not next_page:
            lines.extend(first_search_empty_lines(effective_query, zero_reflections))
        else:
            snapshot = result_snapshot_lines(card_values)
            if snapshot and not next_page:
                lines.extend(snapshot)
                lines.append("")
            lines.extend(user_card_list(card_values))
            if not next_page:
                followups = followup_lines(effective_query, total_count, returned_count, card_values, allow_next=not continuation_notice)
                if followups:
                    lines.append("")
                    lines.extend(followups)
    else:
        lines.append("我没有自动改用其他网站或搜索引擎补结果。")
    if continuation_notice:
        lines.extend(["", continuation_notice])
    warning_values = warnings or []
    if warning_values:
        lines.append("")
        lines.append(f"提醒：{'；'.join(warning_values)}")
    return "\n".join(lines)


def user_intelligence_search_message(
    *,
    stage_label: str,
    effective_query: dict[str, Any],
    total_count: int,
    returned_count: int,
    cards: list[dict[str, Any]],
    warnings: list[str],
    result_lines: list[str],
    area_expansion: dict[str, Any] | None = None,
) -> str:
    scope = '、'.join(query_area_names(effective_query))
    opening = f"我按{scope}范围查询了{stage_label}。" if scope else f"我按您给出的条件查询了{stage_label}。"
    lines = [opening, "", f"共找到 {total_count} 条，本次展示 {returned_count} 条。", ""]
    if returned_count == 0 and area_expansion:
        lines.append(area_expansion_prompt(area_expansion))
        lines.append("")
    lines.extend(result_lines)
    if warnings:
        lines.append("")
        lines.append(f"提醒：{'；'.join(warnings)}")
    return "\n".join(lines)


def user_enterprise_message(kind: str, query: dict[str, Any], rows: list[dict[str, Any]], warnings: list[str]) -> str:
    company_name = clean_user_value(query.get("companyName"))
    labels = {
        "partners": "合作供应商",
        "principals": "合作甲方",
        "area-distribution": "采购地区分布",
        "winning-area-distribution": "中标地区分布",
        "co-bidder-competitors": "直接竞争对手",
        "potential-competitors": "潜在竞争对手",
        "business-info": "工商信息",
        "contacts": "企业联系电话",
    }
    label = labels.get(kind, "企业情报")
    lines = [f"我查询了“{company_name}”的{label}。", ""]
    lines.extend(user_enterprise_list(kind, rows))
    if kind == "contacts":
        lines.append("")
        lines.append("企业联系电话属于明确追问后再调用的数据。")
    if warnings:
        lines.append("")
        lines.append(f"提醒：{'；'.join(warnings)}")
    return "\n".join(lines)


def entitlement_right_name(
    *,
    operation: str,
    result_type: str | None = None,
    enterprise_kind: str | None = None,
) -> str:
    if operation == "search":
        right_name = SEARCH_ENTITLEMENT_RIGHTS.get(str(result_type or ""))
    elif operation == "detail":
        right_name = DETAIL_ENTITLEMENT_RIGHTS.get(str(result_type or ""))
    elif operation == "source_url":
        right_name = "源网址"
    elif operation == "enterprise":
        right_name = "企业联系电话" if enterprise_kind == "contacts" else "企业情报"
    else:
        right_name = None
    if not right_name:
        raise SkillError("INVALID_QUERY", "当前调用无法映射到具体权益。")
    return right_name


def normalize_entitlement_data(data: Any) -> dict[str, Any]:
    """Preserve API data; business success is decided by the response code."""
    return data


def user_entitlement_message(wallet: Any) -> str:
    if not isinstance(wallet, dict):
        return "积分信息：" + clean_user_value(wallet)
    lines = [f"当前可用积分：{clean_user_value(wallet.get('availablePoints'))}。"]
    if wallet.get("frozenPoints") not in (None, "", 0):
        lines.append(f"总积分 {clean_user_value(wallet.get('balancePoints'))}，其中 {clean_user_value(wallet.get('frozenPoints'))} 积分暂时占用。")
    usage = wallet.get("sourceUrlUsage")
    if isinstance(usage, dict):
        lines.append(f"本月原文链接还可获取 {clean_user_value(usage.get('remaining'))} 次（已用 {clean_user_value(usage.get('used'))} / 上限 {clean_user_value(usage.get('limit'))}）。")
        if usage.get("resetAt"):
            lines.append(f"原文次数下次重置时间：{clean_user_value(usage['resetAt'])}（北京时间）。")
    else:
        lines.append("原文链接月度用量：" + clean_user_value(usage))
    return "\n".join(lines)


def validate_search_response(data: Any) -> dict[str, Any]:
    """Preserve API data; business success is decided by the response code."""
    return data


def validate_verify_response(data: Any) -> dict[str, Any]:
    """Preserve API data; business success is decided by the response code."""
    return data


def validate_detail_response(data: Any) -> dict[str, Any]:
    """Preserve API data; business success is decided by the response code."""
    return data


def validate_source_url_response(data: Any) -> dict[str, Any]:
    """Preserve API data; business success is decided by the response code."""
    return data


def validate_enterprise_response(data: Any, kind: str) -> dict[str, Any]:
    """Preserve API data; business success is decided by the response code."""
    return data


def user_detail_failure_message(
    effective_query: dict[str, Any],
    warnings: list[str],
    candidates: list[dict[str, Any]] | None = None,
    intro: str | None = None,
    candidate_lines: list[str] | None = None,
) -> str:
    del effective_query
    del warnings
    lines = [intro or "我还不能确定您指的是哪一个项目。请您回复项目序号，或提供项目名称里的几个关键词，我再继续查。"]
    if candidates or candidate_lines:
        lines.append("")
        lines.append("可能相关的项目如下，请直接回复序号，我再继续查：")
        lines.extend(candidate_lines or user_card_list(candidates or []))
    return "\n".join(lines)


AUTH_ERROR_RULES: dict[str, dict[str, Any]] = {
    "MISSING_API_KEY": {
        "summary": "还没有配置可用于查询的 API Key",
        "next_steps": ["""**千里马AI 数据平台**\\
让你的AI 即刻拥有4.5 亿+招投标数据，注册即赠 500 积分

**注册流程：**\\
① 回复 11 位手机号 → ② 输入短信验证码 → ③ 自动获取并配置 API Key

[前往官网](https://ai.qianlima.com/?source=bb3b4102f584028c3830df37)  · 已有 API Key 可直接在会话提供"""],
        "safety": ["不会自动打开网页", "不会在回答里展示您的 API Key", "不会把查询失败的结果改用其他网站补充"],
    },
    "10001": {
        "summary": "当前 API Key 没有通过验证",
        "next_steps": ["可以通过手机号验证码登录后重新配置，也可以提供其他 API Key", "也可登录 https://ai.qianlima.com/?source=bb3b4102f584028c3830df37 获取或检查 API Key"],
    },
    "429": {
        "summary": "当前查询请求有点频繁",
        "next_steps": [
            "请稍等一会儿再试，不要连续重复提交同一个查询",
            "如果是在批量查询或连续翻页，请减少每次查询的数据量，间隔一会儿再继续",
            "如果经常出现，请登录 https://ai.qianlima.com/?source=bb3b4102f584028c3830df37 查看调用频率或剩余额度",
        ],
    },
}

EXPLICIT_API_ERROR_RULES: dict[str, dict[str, Any]] = {
    "401": {"summary":"当前请求未认证", "next_steps":["请确认已配置有效 API Key"]},
    "10004": {"summary":"接口参数异常", "next_steps":["请由 Agent 按当前接口契约修正参数"]},
    "10005": {"summary":"项目详情不存在", "next_steps":["请从当前结果选择其他项目"]},
    "10006": {"summary":"项目详情已撤回", "next_steps":["请从当前结果选择其他项目"]},
    "10007": {"summary":"当前无权查看详情", "next_steps":["请前往 https://ai.qianlima.com/?source=bb3b4102f584028c3830df37 核对访问权限"]},
    "10010": {"summary":"当前账号无权查看该数据", "next_steps":["请前往 https://ai.qianlima.com/?source=bb3b4102f584028c3830df37 核对数据权限"]},
    "10011": {"summary":"原文链接不存在", "next_steps":["仍可使用结果中的详情页链接"]},
    "10028": {"summary":"当前查询地区权限不足", "next_steps":["请前往 https://ai.qianlima.com/?source=bb3b4102f584028c3830df37 核对地区权限"]},
    "10030": {"summary":"积分余额不足", "next_steps":["请前往 https://ai.qianlima.com/?source=bb3b4102f584028c3830df37 查看积分或充值"]},
    "10031": {"summary":"积分扣除失败", "next_steps":["请稍后重试，本次未自动重复请求"]},
    "10032": {"summary":"积分账户尚未初始化或正在初始化", "next_steps":["请稍后查看，或前往 https://ai.qianlima.com/?source=bb3b4102f584028c3830df37 核对"]},
    "10036": {"summary":"原文链接本月获取次数已用完", "next_steps":["请查看月度次数及重置时间"]},
    "10037": {"summary":"积分结算已超时", "next_steps":["请先核对当前结果与积分记录，再决定是否重新查询"]},
    "10038": {"summary":"请求仍在处理中", "next_steps":["请稍后查看，避免连续重复提交"]},
    "10039": {"summary":"能力价格版本已变化", "next_steps":["请刷新当前权益并核对价格后决定是否重新查询"]},
    "10040": {"summary":"请求标识冲突", "next_steps":["本次未自动重复请求，可重新发起查询"]},
    "10041": {"summary":"项目完整正文尚未采集或为空", "next_steps":["目前无法提供该项目完整正文"]},
}




GENERIC_ACCOUNT_ACCESS_RULE: dict[str, Any] = {
    "summary": "当前账号无法完成本次查询",
    "next_steps": ["请登录 https://ai.qianlima.com/?source=bb3b4102f584028c3830df37 核对当前积分和数据权限"],
    "safety": ["不会绕过数据权限获取结果"],
}


def is_account_access_error(error: SkillError) -> bool:
    return error.code in AUTH_ERROR_RULES or error.code in ENTITLEMENT_DIAGNOSIS_ERROR_CODES or error.code == "401"


def should_diagnose_entitlement(error: SkillError) -> bool:
    return error.code in ENTITLEMENT_DIAGNOSIS_ERROR_CODES




def build_entitlement_diagnosis(data: Any, target_right: str, trigger: str) -> dict[str, Any]:
    wallet = normalize_entitlement_data(data)
    return {"checked": True, "target_right": target_right, "trigger": trigger, "wallet": wallet,
            "conclusion": "wallet_snapshot_only"}


def entitlement_diagnosis_message(diagnosis: dict[str, Any]) -> str:
    if not diagnosis.get("checked"):
        return "当前积分信息暂时无法确认，可前往[账号平台](https://ai.qianlima.com/?source=bb3b4102f584028c3830df37)核对。"
    wallet = diagnosis["wallet"]
    if not isinstance(wallet, dict):
        return "当前积分信息：" + clean_user_value(wallet) + "。"
    if diagnosis.get("target_right") == "源网址":
        usage = wallet.get("sourceUrlUsage")
        if not isinstance(usage, dict):
            return "原文链接月度用量：" + clean_user_value(usage) + "。"
        message = f"当前原文链接月度剩余 {clean_user_value(usage.get('remaining'))} 次。"
        if usage.get("resetAt"):
            message += f"下次重置时间：{usage['resetAt']}（北京时间）。"
        return message
    return f"当前可用积分 {clean_user_value(wallet.get('availablePoints'))}。积分余额不能确认本次数据或地区权限，本次失败原因仍以上述提示为准。"


def attach_entitlement_diagnosis(
    payload: dict[str, Any],
    client: Any,
    *,
    target_right: str,
    trigger: str,
) -> dict[str, Any]:
    try:
        diagnosis = build_entitlement_diagnosis(client.entitlement(), target_right, trigger)
    except Exception:
        diagnosis = {
            "checked": False,
            "target_right": target_right,
            "trigger": trigger,
            "right": None,
            "conclusion": "diagnosis_unavailable",
        }
    payload["entitlement_diagnosis"] = diagnosis
    original_message = str(payload.get("user_message") or "").rstrip()
    diagnostic_message = entitlement_diagnosis_message(diagnosis)
    if trigger == "access_block":
        payload["user_message"] = original_message + ("\n\n" if original_message else "") + "权益补充：" + diagnostic_message
    else:
        payload["user_message"] = original_message + ("\n\n" if original_message else "") + diagnostic_message
    return payload


def maybe_attach_entitlement_diagnosis(
    payload: dict[str, Any],
    client: Any,
    error: SkillError,
    *,
    target_right: str,
) -> dict[str, Any]:
    if getattr(client, "access_mode", None) == "guest" or not should_diagnose_entitlement(error):
        return payload
    trigger = "access_block"
    return attach_entitlement_diagnosis(payload, client, target_right=target_right, trigger=trigger)


def auth_error_rule(error: SkillError, command: str | None = None) -> dict[str, Any]:
    del command
    rule = EXPLICIT_API_ERROR_RULES.get(error.code) or AUTH_ERROR_RULES.get(error.code)
    if rule:
        return rule
    if is_account_access_error(error):
        return GENERIC_ACCOUNT_ACCESS_RULE
    return {
        "summary": "这次没有处理成功",
        "next_steps": ["请稍后再试，或调整查询条件后重试"],
        "safety": ["不会自动改用其他网站或搜索引擎补结果"],
    }


def generic_error_rule(error: SkillError, stage: str | None = None) -> dict[str, Any]:
    explicit_rule = EXPLICIT_API_ERROR_RULES.get(error.code)
    if explicit_rule:
        return explicit_rule
    if error.code == "INVALID_JSON":
        return {
            "summary": "查询条件格式不正确",
            "next_steps": ["请重新发起查询", "如果筛选条件较多，请减少或确认关键词、地区、时间后再查"],
            "safety": ["不会显示代码栈或原始接口错误", "不会自动改用其他网站或模型记忆补结果"],
        }
    if error.code == "INVALID_FIELDS":
        return {
            "summary": "这类详情暂不支持",
            "next_steps": ["请改问联系人、联系电话、截止时间、开标日期、预算金额、中标金额、服务到期时间、详情页链接或原文链接"],
            "safety": ["不会暴露内部字段名"],
        }
    if error.code == "10004":
        return {
            "summary": "查询条件没有通过数据服务校验",
            "next_steps": ["请重新确认关键词、地区或时间", "修改后重新查询"],
            "safety": ["不会显示接口参数名或原始错误"],
        }
    if error.code in {"HTTP_ERROR", "NETWORK_ERROR", "INVALID_RESPONSE"}:
        return {
            "summary": SERVICE_UNAVAILABLE_SUMMARY,
            "next_steps": [
                "请稍后重试",
                "如果您正在连续查询或翻页，请先停一会儿再继续",
                "如果多次重试仍失败，请确认本地网络可用，或登录 https://ai.qianlima.com/?source=bb3b4102f584028c3830df37 检查 API Key 后联系平台处理",
            ],
            "safety": ["不会显示接口状态码、网络异常或代码栈", "不会自动改用其他网站或模型记忆补结果"],
        }
    if stage in {"enterprise", "enterprise_contacts"}:
        return {
            "summary": GENERAL_FAILURE_SUMMARY,
            "next_steps": ["请稍后重试", "如果持续失败，请确认企业全称后再查，或联系平台处理"],
            "safety": ["不会显示原始接口错误", "不会自动改用其他网站或模型记忆补结果"],
        }
    return {
        "summary": GENERAL_FAILURE_SUMMARY,
        "next_steps": ["请稍后重试", "如果持续失败，请减少筛选条件，或重新确认关键词、地区或时间后再查"],
        "safety": ["不会显示原始接口错误", "不会自动改用其他网站或模型记忆补结果"],
    }


def render_user_error_from_rule(rule: dict[str, Any]) -> str:
    if rule is AUTH_ERROR_RULES["MISSING_API_KEY"]:
        return rule["next_steps"][0]
    lines = [f"{rule['summary']}。"]
    next_steps = [str(step).strip() for step in rule.get("next_steps") or [] if str(step).strip()]
    if next_steps:
        lines.append("")
        if len(next_steps) == 1:
            lines.append(next_steps[0] + "。")
        else:
            lines.append("您可以这样处理：")
            lines.extend(f"- {step}" for step in next_steps)
    optional_step = str(rule.get("optional_step") or "").strip()
    if optional_step:
        lines.append("")
        lines.append(optional_step)
    safety = [str(item).strip() for item in rule.get("safety") or [] if str(item).strip()]
    if safety:
        lines.append("")
        lines.append("安全说明：" + "、".join(safety) + "。")
    return "\n".join(lines)


def public_error_summary(error: SkillError, command: str | None = None) -> str:
    if error.code in AGENT_CORRECTION_ERROR_CODES or error.code == "NO_MORE_PAGES":
        return error.message
    if error.code in EXPLICIT_API_ERROR_RULES:
        return str(EXPLICIT_API_ERROR_RULES[error.code]["summary"])
    if is_account_access_error(error):
        return str(auth_error_rule(error, command)["summary"])
    if error.code in {"INVALID_JSON", "INVALID_FIELDS", "HTTP_ERROR", "NETWORK_ERROR", "INVALID_RESPONSE"}:
        return str(generic_error_rule(error, command)["summary"])
    if error.code in {"INVALID_QUERY"} | STATE_ERROR_CODES:
        return error.message
    if error.code in {"MOCK_ROUTE_NOT_FOUND", "MOCK_FILE_NOT_FOUND"} or re.fullmatch(r"\d+", str(error.code)):
        return str(generic_error_rule(error, command)["summary"])
    return error.message


def permission_user_message(error: SkillError, command: str | None = None) -> str:
    if error.code == "MISSING_API_KEY":
        return "当前查询进程没有 Key，请先检查已有配置的加载。确实无 Key 时，该能力需要登录并使用账号积分；愿意接入后可继续原任务。[前往官网](https://ai.qianlima.com/?source=bb3b4102f584028c3830df37)"
    return render_user_error_from_rule(auth_error_rule(error, command))


def generic_user_message(error: SkillError, stage: str | None = None) -> str:
    return render_user_error_from_rule(generic_error_rule(error, stage))


def failure_user_warning(error: SkillError, stage: str | None = None) -> str:
    rule = generic_error_rule(error, stage)
    next_steps = [str(step).strip() for step in rule.get("next_steps") or [] if str(step).strip()]
    if next_steps:
        return f"{rule['summary']}。{'；'.join(next_steps)}。"
    return f"{rule['summary']}。"


def detail_display_value(field: str, value: Any) -> str:
    if field == "biddingCandidates":
        if value is None or value == "" or value == []:
            return EMPTY_DISPLAY
        if not isinstance(value,list):
            return clean_user_value(value)
        return "；".join((f"排名 {clean_user_value(item.get('ranking'))}，{clean_user_value(item.get('providerName'))}，报价 {format_amount_wan(item.get('amount'))} 万元" if item.get('amount') not in (None, "") else f"排名 {clean_user_value(item.get('ranking'))}，{clean_user_value(item.get('providerName'))}，报价未公示") if isinstance(item, dict) else clean_user_value(item) for item in value) or EMPTY_DISPLAY
    if field in {"budgetAmount", "winningBidderAmount", "contractAmount"}:
        return format_amount_wan(value)
    if field == "infoType":
        return format_stage_display(value)
    if field == "sourceUrl":
        text = clean_user_value(value)
        if text == EMPTY_DISPLAY:
            return text
        return f"{markdown_link('查看原文', text)}（{text}）"
    return clean_user_value(value)


def detail_line(field: str, detail: dict[str, Any]) -> str:
    label = DETAIL_FIELD_META[field]["label"]
    return f"- {label}：{detail_display_value(field, detail.get(field))}"


def markdown_link(label: str, url: Any) -> str:
    text = clean_user_value(url)
    if text == EMPTY_DISPLAY:
        return EMPTY_DISPLAY
    escaped = text.replace(")", "%29")
    return f"[{label}]({escaped})"


def full_detail_view(detail: Any, result_type: str) -> Any:
    return copy.deepcopy(detail)


def user_detail_success_message(
    detail: dict[str, Any],
    requested_fields: list[str] | None = None,
    resolution: dict[str, Any] | None = None,
    result_type: str = "project",
) -> str:
    del resolution
    lines: list[str] = []
    if detail.get("title"):
        lines.append(f"定位到的项目：{detail['title']}")
    else:
        lines.append("定位到的项目：当前结果中的匹配项目")

    requested = [field for field in (requested_fields or []) if field in DETAIL_FIELD_META and field in detail]
    if requested:
        lines.append("")
        lines.append("## 您关心的信息")
        lines.extend(detail_line(field, detail) for field in requested)

    supplement_fields = [
        field
        for field in detail_fields_for_result_type(result_type)
        if field in DETAIL_FIELD_META
        and field in detail
        and field not in requested
        and field not in {"id", "title", "url"}
        and detail_display_value(field, detail.get(field)) != EMPTY_DISPLAY
    ]
    if supplement_fields:
        lines.append("")
        lines.append("## 项目补充信息")
        for group in DETAIL_SUPPLEMENT_GROUPS:
            group_fields = [field for field in supplement_fields if DETAIL_FIELD_META[field]["group"] == group]
            if not group_fields:
                continue
            lines.append(f"### {group}")
            lines.extend(detail_line(field, detail) for field in group_fields)

    detail_url = clean_user_value(detail.get("url"))
    lines.append("")
    if detail_url == EMPTY_DISPLAY:
        lines.append("项目详情入口未公示。")
    else:
        lines.append(f"您可以直接{markdown_link('查看项目详情', detail_url)}，了解公告页面里的完整信息。")
    return "\n".join(lines)


def failure_payload(
    *,
    stage: str,
    error: SkillError,
    effective_query: dict[str, Any] | None = None,
    warnings: list[str] | None = None,
    resolution: dict[str, Any] | None = None,
) -> dict[str, Any]:
    warning_values = list(warnings or [])
    display_message = public_error_summary(error, stage)
    if display_message not in warning_values:
        warning_values.append(display_message)
    payload: dict[str, Any] = {
        "ok": False,
        "stage": stage,
        "error_code": error.code,
        "message": display_message,
        "total_count": 0,
        "returned_count": 0,
        "effective_query": effective_query or {},
        "warnings": warning_values,
    }
    if resolution:
        payload["resolution"] = resolution
    if error.code in AGENT_CORRECTION_ERROR_CODES:
        payload["cards"] = []
        if isinstance(error.data, dict):
            for field in (
                "requires_agent_correction",
                "requires_user_confirmation",
                "agent_instruction",
                "unsupported_fields",
                "allowed_fields",
                "invalid_field",
                "invalid_fields",
                "allowed_values",
                "amount_field",
                "amount_value",
            ):
                if field in error.data:
                    payload[field] = error.data[field]
        payload.setdefault("requires_agent_correction", True)
        payload.setdefault("requires_user_confirmation", False)
        payload["user_message"] = "查询参数需要由 Agent 按接口契约修正后重试，本次未调用查询接口。"
        return payload
    if error.code == "NO_MORE_PAGES":
        payload["cards"] = []
        payload["user_message"] = "当前结果已经是最后一页，没有继续请求后端。"
        return payload
    if is_account_access_error(error):
        payload["user_message"] = permission_user_message(error, stage)
        return payload
    if error.code in {"INVALID_JSON", "INVALID_FIELDS"}:
        if error.code == "INVALID_FIELDS":
            payload["detail"] = {}
        else:
            payload["cards"] = []
        payload["user_message"] = generic_user_message(error, stage)
        return payload
    if error.code == "TIME_SPAN_EXCEEDED":
        payload["cards"] = []
        payload["user_message"] = display_message
        return payload
    if error.code == "INVALID_QUERY":
        payload["cards"] = []
        payload["user_message"] = f"这次没有继续查询。\n\n{display_message}\n\n请您确认后我再查。"
        return payload
    if stage in {"search", "next", "search_purchase", "search_expiring"}:
        payload["cards"] = []
        payload["user_message"] = user_search_message(
            success=False,
            effective_query=effective_query or {},
            warnings=[failure_user_warning(error, stage)],
            failure=True,
            include_query_conditions=stage == "search",
        )
    else:
        payload["user_message"] = generic_user_message(error, stage)
    return payload


def validate_endpoint_request(method: str, path: str, query: dict[str, Any] | None, *, mock: bool = False) -> None:
    expected_method: str | None = None
    allowed_fields: frozenset[str] | None = None
    required_fields: frozenset[str] = frozenset()
    endpoint_label = path

    if path in {"/api/user/verify", "/api/user/entitlement"}:
        expected_method = "GET"
        allowed_fields = frozenset()
    elif path in {"/api/search", "/api/free/search"}:
        expected_method = "POST"
        allowed_fields = PROJECT_SEARCH_FIELDS - {AMOUNT_UNIT_CONFIRMATION_FIELD}
        required_fields = frozenset({"keywordGroups"})
        endpoint_label = "普通项目搜索"
        if path == "/api/free/search":
            allowed_fields = (allowed_fields - {"numPerPage"}) | {"sourceCode"}
    elif path == "/api/search/purchase":
        expected_method = "POST"
        allowed_fields = PURCHASE_SEARCH_FIELDS - {AMOUNT_UNIT_CONFIRMATION_FIELD}
        required_fields = frozenset({"keywords", "currentPage", "numPerPage"})
        endpoint_label = "采购意向搜索"
    elif path == "/api/search/expiring":
        expected_method = "POST"
        allowed_fields = EXPIRING_SEARCH_FIELDS - {AMOUNT_UNIT_CONFIRMATION_FIELD}
        required_fields = frozenset({"keywords", "currentPage", "numPerPage"})
        endpoint_label = "临期项目搜索"
    elif re.fullmatch(r"/api/(?:detail|purchase/detail|expiring/detail|sourceUrl|fullText|attachments|timeline)/[^/]+", path):
        expected_method = "GET"
        allowed_fields = frozenset()
    elif path == "/api/searchCompany":
        expected_method = "POST"
        allowed_fields = frozenset({"companyName","currentPage","pageSize"})
        required_fields = frozenset({"companyName"})
        normalize_company_query(query or {})
    elif path.startswith("/api/enterprise/"):
        endpoint = path.rsplit("/", 1)[-1]
        kind_by_endpoint = {
            "partners": "partners",
            "areaDistribution": "area-distribution",
            "principals": "principals",
            "winningAreaDistribution": "winning-area-distribution",
            "coBidderCompetitors": "co-bidder-competitors",
            "potentialCompetitors": "potential-competitors",
            "businessInfo": "business-info",
            "contacts": "contacts",
        }
        kind = kind_by_endpoint.get(endpoint)
        if kind is not None:
            expected_method = "GET" if kind == "business-info" else "POST"
            allowed_fields = ENTERPRISE_QUERY_FIELDS[kind]
            required_fields = frozenset({"companyName"})
            endpoint_label = f"企业情报 {kind}"

    if expected_method is None or allowed_fields is None:
        return
    if method != expected_method:
        code = "MOCK_METHOD_MISMATCH" if mock else "REQUEST_METHOD_MISMATCH"
        raise SkillError(code, f"{path} 只支持 {expected_method} 请求。")
    effective_query = query or {}
    reject_unsupported_fields(effective_query, allowed_fields, endpoint_label)
    missing = sorted(field for field in required_fields if effective_query.get(field) in (None, "", [], {}))
    if missing:
        raise correction_error(
            "AGENT_QUERY_CORRECTION_REQUIRED",
            f"{endpoint_label}缺少必填字段。",
            f"补齐必填字段：{', '.join(missing)} 后重试，不要询问用户，除非用户原话确实缺少业务关键词。",
            missing_fields=missing,
            allowed_fields=sorted(allowed_fields),
        )

    if path in {"/api/search", "/api/free/search", "/api/search/purchase", "/api/search/expiring"}:
        if "areaIds" in effective_query:
            validate_area_query_scope(normalize_area_ids(effective_query["areaIds"]))
        if path not in {"/api/search", "/api/free/search"}:
            normalize_word_list(effective_query.get("keywords"), "keywords", [])
        if "sortType" in effective_query:
            normalize_int_enum(effective_query["sortType"], "sortType", SEARCH_SORT_TYPES)
        if "purchasingUnitTypes" in effective_query:
            normalize_int_list_enum(effective_query["purchasingUnitTypes"], "purchasingUnitTypes", PURCHASING_UNIT_TYPES)
    if path in {"/api/search", "/api/free/search"}:
        checked = dict(effective_query)
        if path == "/api/free/search":
            checked.pop("sourceCode", None)  # Request provenance, not a search filter.
        checked[AMOUNT_UNIT_CONFIRMATION_FIELD] = True
        normalize_query(checked)
    elif path == "/api/search/purchase":
        validate_purchase_time_spans(effective_query)
        if "matchScopes" in effective_query:
            normalize_purchase_match_scopes(effective_query["matchScopes"], strict=True)
    elif path == "/api/search/expiring":
        validate_time_span(effective_query, "beginServiceExpireTime", "endServiceExpireTime", 5, "服务到期时间")
        if "matchScopes" in effective_query:
            normalize_int_list_enum(effective_query["matchScopes"], "matchScopes", EXPIRING_MATCH_SCOPES)
        if "procurementMethod" in effective_query:
            normalize_int_enum(effective_query["procurementMethod"], "procurementMethod", PROCUREMENT_METHODS)
        if "contractPeriodType" in effective_query:
            normalize_int_enum(effective_query["contractPeriodType"], "contractPeriodType", CONTRACT_PERIOD_TYPES)
        if bool(effective_query.get("beginServiceExpireTime")) != bool(effective_query.get("endServiceExpireTime")):
            raise correction_error(
                "AGENT_QUERY_CORRECTION_REQUIRED",
                "临期项目的服务到期开始和结束日期必须成对传入。",
                "同时传 beginServiceExpireTime 和 endServiceExpireTime，或两个字段都不传后重试，不要询问用户。",
                invalid_fields=["beginServiceExpireTime", "endServiceExpireTime"],
            )
    elif path.startswith("/api/enterprise/"):
        if "sortType" in effective_query:
            normalize_int_enum(effective_query["sortType"], "sortType", ENTERPRISE_SORT_TYPES)
        if "phoneType" in effective_query:
            normalize_int_enum(effective_query["phoneType"], "phoneType", PHONE_TYPES)


def validate_mock_response(path: str, data: Any) -> Any:
    """Preserve API data; business success is decided by the response code."""
    return data


class ApiClient:
    def __init__(self, base_url: str, api_key: str | None, mock_dir: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.mock_dir = Path(mock_dir) if mock_dir else None
        self.last_request_query: dict[str, Any] | None = None
        self.last_request_path: str | None = None
        self.access_mode = "authenticated"
        self.access_mode_source = "default"

    def verify(self) -> dict[str, Any]:
        return self._request("GET", "/api/user/verify")

    def entitlement(self) -> dict[str, Any]:
        return self._request("GET", "/api/user/entitlement")

    def search(self, query: dict[str, Any]) -> dict[str, Any]:
        if self.access_mode == "guest":
            body = {key: value for key, value in query.items() if key != "numPerPage"}
            if body.get("currentPage", 1) > 10:
                raise SkillError("FREE_PAGE_LIMIT", "免费查询最多查看前 10 页／300 条；匹配结果可能仍有更多。")
            return self._request("POST", "/api/free/search", query=body)
        return self._request("POST", "/api/search", query=query)

    def search_purchase(self, query: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/api/search/purchase", query=query)

    def search_expiring(self, query: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/api/search/expiring", query=query)

    def detail(self, project_id: str) -> dict[str, Any]:
        return self._request("GET", f"/api/detail/{project_id}")

    def purchase_detail(self, project_id: str) -> dict[str, Any]:
        return self._request("GET", f"/api/purchase/detail/{project_id}")

    def expiring_detail(self, project_id: str) -> dict[str, Any]:
        return self._request("GET", f"/api/expiring/detail/{project_id}")

    def source_url(self, project_id: str) -> dict[str, Any]:
        return self._request("GET", f"/api/sourceUrl/{project_id}")

    def enterprise(self, kind: str, query: dict[str, Any]) -> dict[str, Any]:
        path_by_kind = {
            "partners": "/api/enterprise/partners",
            "area-distribution": "/api/enterprise/areaDistribution",
            "principals": "/api/enterprise/principals",
            "winning-area-distribution": "/api/enterprise/winningAreaDistribution",
            "co-bidder-competitors": "/api/enterprise/coBidderCompetitors",
            "potential-competitors": "/api/enterprise/potentialCompetitors",
            "business-info": "/api/enterprise/businessInfo",
            "contacts": "/api/enterprise/contacts",
        }
        if kind not in path_by_kind:
            raise SkillError("INVALID_QUERY", "企业情报类型不在支持范围内。")
        method = "GET" if kind == "business-info" else "POST"
        return self._request(method, path_by_kind[kind], query=query)

    def _request(self, method: str, path: str, query: dict[str, Any] | None = None) -> Any:
        if method == "POST" and path == "/api/free/search":
            # Provenance comes from this package, never user filters or old state.
            query = {**(query or {}), "sourceCode": PACKAGE_SOURCE_CODE}
        validate_endpoint_request(method, path, query, mock=self.mock_dir is not None)
        self.last_request_path = path
        if self.mock_dir:
            if query is not None:
                self.last_request_query = json.loads(json.dumps(query))
            return self._mock_response(method, path, query)
        if not self.api_key and path != "/api/free/search":
            raise SkillError("MISSING_API_KEY", "还没有配置 API Key。")

        url = self.base_url + path
        body = None
        headers = {"Content-Type": "application/json"}
        if query is not None:
            self.last_request_query = json.loads(json.dumps(query))
            if method == "GET":
                url += "?" + urllib.parse.urlencode(query, doseq=True)
            else:
                body = json.dumps(query, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        if self.api_key:
            req.add_unredirected_header("qianlimaApiKey", self.api_key)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            # HTTP errors may contain the authoritative business error and limits.
            try:
                received = json.loads(exc.read().decode("utf-8"))
            except (ValueError, UnicodeDecodeError, OSError, AttributeError, KeyError):
                received = None
            if isinstance(received, dict) and "code" in received:
                return accept_api_response(path, received)
            if exc.code == 503:
                raise transport_failure(path, "503", "免费查询暂时繁忙，请稍后再试。" if path == "/api/free/search" else "服务暂时繁忙，请稍后再试。") from exc
            if exc.code == 429:
                raise transport_failure(path, "429", "未取得 API 响应：请求过于频繁。") from exc
            if exc.code == 401:
                raise transport_failure(path, "401", "未取得 API 响应：未认证。") from exc
            raise transport_failure(path, "HTTP_ERROR", f"未取得 API 响应：HTTP {exc.code}。") from exc
        except urllib.error.URLError as exc:
            raise transport_failure(path, "NETWORK_ERROR", "网络连接异常，未取得 API 响应。") from exc
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise transport_failure(path, "API_RESPONSE_UNREADABLE", "未取得可解析的 API 响应。") from exc
        except (OSError, TimeoutError) as exc:
            raise transport_failure(path, "NETWORK_ERROR", "连接中断或超时，未取得 API 响应。") from exc

        return accept_api_response(path, payload)

    def _mock_response(self, method: str, path: str, query: dict[str, Any] | None) -> dict[str, Any]:
        validate_endpoint_request(method, path, query, mock=True)
        candidates: list[str]
        if path == "/api/user/verify":
            candidates = ["verify.json"]
        elif path == "/api/user/entitlement":
            candidates = ["entitlement.json"]
        elif path == "/api/searchCompany":
            candidates = [f"searchCompany_page_{(query or {}).get('currentPage',1)}.json", "searchCompany.json"]
        elif re.fullmatch(r"/api/(fullText|attachments|timeline)/[^/]+",path):
            endpoint,project_id = path.split("/")[-2:]
            candidates = [f"{endpoint}_{project_id}.json"]
        elif path == "/api/free/search":
            page = (query or {}).get("currentPage", 1)
            candidates = [f"free_search_page_{page}.json", "free_search.json"]
        elif path == "/api/search":
            page = (query or {}).get("currentPage", 1)
            candidates = [f"search_page_{page}.json", "search.json"]
        elif path == "/api/search/purchase":
            page = (query or {}).get("currentPage", 1)
            candidates = [f"search_purchase_page_{page}.json", "search_purchase.json"]
        elif path == "/api/search/expiring":
            page = (query or {}).get("currentPage", 1)
            candidates = [f"search_expiring_page_{page}.json", "search_expiring.json"]
        elif path.startswith("/api/detail/"):
            project_id = path.rsplit("/", 1)[-1]
            candidates = [f"detail_{project_id}.json", "detail.json"]
        elif path.startswith("/api/purchase/detail/"):
            project_id = path.rsplit("/", 1)[-1]
            candidates = [f"purchase_detail_{project_id}.json", "purchase_detail.json"]
        elif path.startswith("/api/expiring/detail/"):
            project_id = path.rsplit("/", 1)[-1]
            candidates = [f"expiring_detail_{project_id}.json", "expiring_detail.json"]
        elif path.startswith("/api/sourceUrl/"):
            project_id = path.rsplit("/", 1)[-1]
            candidates = [f"sourceUrl_{project_id}.json", "sourceUrl.json"]
        elif path.startswith("/api/enterprise/"):
            endpoint = path.rsplit("/", 1)[-1]
            candidates = [f"enterprise_{endpoint}.json"]
        else:
            raise SkillError("MOCK_ROUTE_NOT_FOUND", f"没有 mock 路由：{path}")

        for name in candidates:
            file_path = self.mock_dir / name
            if file_path.exists():
                payload = load_json(file_path, {})
                return accept_api_response(path, payload)
        raise SkillError("MOCK_FILE_NOT_FOUND", f"缺少 mock 文件：{', '.join(candidates)}")


class SearchCapabilitySpec:
    __slots__ = (
        "result_type",
        "success_stage",
        "stage_label",
        "search_call",
        "detail_call",
        "normalize_query",
        "card_view",
        "list_renderer",
        "message_renderer",
        "refine_aliases",
        "include_stage_on_success",
    )

    def __init__(
        self,
        *,
        result_type: str,
        success_stage: str,
        stage_label: str,
        search_call: Callable[[ApiClient, dict[str, Any]], dict[str, Any]],
        detail_call: Callable[[ApiClient, str], dict[str, Any]],
        normalize_query: Callable[..., tuple[dict[str, Any], list[str]]],
        card_view: Callable[[dict[str, Any]], dict[str, Any]],
        list_renderer: Callable[[list[dict[str, Any]]], list[str]],
        message_renderer: Callable[..., dict[str, Any]],
        refine_aliases: tuple[tuple[str, str], ...],
        include_stage_on_success: bool,
    ):
        self.result_type = result_type
        self.success_stage = success_stage
        self.stage_label = stage_label
        self.search_call = search_call
        self.detail_call = detail_call
        self.normalize_query = normalize_query
        self.card_view = card_view
        self.list_renderer = list_renderer
        self.message_renderer = message_renderer
        self.refine_aliases = refine_aliases
        self.include_stage_on_success = include_stage_on_success


def normalize_project_search_query(raw_query: dict[str, Any], *, force_page: int | None = None, check_time_span: bool = True) -> tuple[dict[str, Any], list[str]]:
    return normalize_query(raw_query, force_page=force_page, check_time_span=check_time_span)


def normalize_purchase_search_query(raw_query: dict[str, Any], *, force_page: int | None = None, check_time_span: bool = True) -> tuple[dict[str, Any], list[str]]:
    if "matchScopes" in raw_query:
        raw_query = {**raw_query, "matchScopes": normalize_purchase_match_scopes(raw_query["matchScopes"])}
    query, warnings = normalize_intelligence_query(
        raw_query,
        allowed_fields=PURCHASE_SEARCH_FIELDS,
        check_time_span=check_time_span,
        endpoint_label="采购意向搜索",
        match_scopes=PURCHASE_MATCH_SCOPES,
        force_page=force_page,
        default_warning="未传预计采购时间时，采购意向接口默认按未来 1 到 3 个月查询。",
        default_warning_fields=("startPlanPurchaseDate", "endPlanPurchaseDate"),
    )
    if check_time_span:
        validate_purchase_time_spans(query)
    return query, warnings

def normalize_expiring_search_query(raw_query: dict[str, Any], *, force_page: int | None = None, check_time_span: bool = True) -> tuple[dict[str, Any], list[str]]:
    return normalize_intelligence_query(
        raw_query,
        allowed_fields=EXPIRING_SEARCH_FIELDS,
        check_time_span=check_time_span,
        endpoint_label="临期项目搜索",
        match_scopes=EXPIRING_MATCH_SCOPES,
        force_page=force_page,
        default_warning="未传服务到期时间时，临期项目接口默认按未来 90 到 180 天查询。",
        default_warning_fields=("beginServiceExpireTime", "endServiceExpireTime"),
        require_service_expire_pair=True,
    )


def project_message_payload(
    *,
    capability: SearchCapabilitySpec,
    effective_query: dict[str, Any],
    total_count: int,
    returned_count: int,
    viewed_cards: list[dict[str, Any]],
    warnings: list[str],
    query_notice: str | None = None,
    continuation_notice: str | None = None,
) -> dict[str, Any]:
    del capability
    area_expansion = district_area_expansion(effective_query) if total_count == 0 and not query_notice else None
    zero_reflections = zero_result_reflection(effective_query) if total_count == 0 and not query_notice else []
    payload: dict[str, Any] = {
        "user_message": user_search_message(
            success=True,
            effective_query=effective_query,
            total_count=total_count,
            returned_count=returned_count,
            cards=viewed_cards,
            warnings=warnings,
            next_page=bool(query_notice),
            include_query_conditions=not bool(query_notice),
            zero_reflections=zero_reflections,
            continuation_notice=continuation_notice,
        )
    }
    if zero_reflections:
        payload["zero_result_reflection"] = zero_reflections
    if area_expansion:
        payload["area_expansion"] = area_expansion
    return payload


def intelligence_message_payload(
    *,
    capability: SearchCapabilitySpec,
    effective_query: dict[str, Any],
    total_count: int,
    returned_count: int,
    viewed_cards: list[dict[str, Any]],
    warnings: list[str],
    query_notice: str | None = None,
) -> dict[str, Any]:
    area_expansion = district_area_expansion(effective_query) if total_count == 0 and not query_notice else None
    payload = {
        "user_message": user_intelligence_search_message(
            stage_label=capability.stage_label,
            effective_query=effective_query,
            total_count=total_count,
            returned_count=returned_count,
            cards=viewed_cards,
            warnings=warnings,
            result_lines=capability.list_renderer(viewed_cards),
            area_expansion=area_expansion,
        )
    }
    if area_expansion:
        payload["area_expansion"] = area_expansion
    return payload


SEARCH_CAPABILITIES: dict[str, SearchCapabilitySpec] = {
    "project": SearchCapabilitySpec(
        result_type="project",
        success_stage="search",
        stage_label="项目",
        search_call=ApiClient.search,
        detail_call=ApiClient.detail,
        normalize_query=normalize_project_search_query,
        card_view=card_view,
        list_renderer=user_card_list,
        message_renderer=project_message_payload,
        refine_aliases=(),
        include_stage_on_success=False,
    ),
    "purchase_intention": SearchCapabilitySpec(
        result_type="purchase_intention",
        success_stage="purchase_intention",
        stage_label="采购意向",
        search_call=ApiClient.search_purchase,
        detail_call=ApiClient.purchase_detail,
        normalize_query=normalize_purchase_search_query,
        card_view=purchase_card_view,
        list_renderer=user_purchase_card_list,
        message_renderer=intelligence_message_payload,
        refine_aliases=(("beginAmount", "startPlanPurchaseAmount"), ("endAmount", "endPlanPurchaseAmount")),
        include_stage_on_success=True,
    ),
    "expiring_project": SearchCapabilitySpec(
        result_type="expiring_project",
        success_stage="expiring_project",
        stage_label="临期项目",
        search_call=ApiClient.search_expiring,
        detail_call=ApiClient.expiring_detail,
        normalize_query=normalize_expiring_search_query,
        card_view=expiring_card_view,
        list_renderer=user_expiring_card_list,
        message_renderer=intelligence_message_payload,
        refine_aliases=(("beginAmount", "beginContractAmount"), ("endAmount", "endContractAmount")),
        include_stage_on_success=True,
    ),
}


def search_capability(result_type: str) -> SearchCapabilitySpec:
    try:
        return SEARCH_CAPABILITIES[result_type]
    except KeyError as exc:
        raise SkillError("RESULT_SET_CORRUPT", "结果状态的数据类型无效。") from exc


def capability_failure_stage(capability: SearchCapabilitySpec) -> str:
    return capability.search_call.__name__


def apply_refine_aliases(capability: SearchCapabilitySpec, patch_query: dict[str, Any]) -> dict[str, Any]:
    query = dict(patch_query)
    if "areaIds" in query and query["areaIds"] is None:
        query["areaIds"] = []  # Legacy explicit clear patch.
    for source, target in capability.refine_aliases:
        if source in query and target not in query:
            query[target] = query[source]
        query.pop(source, None)
    return query


FREE_CARD_FIELDS = frozenset({"id", "title", "purchasingUnit", "winningBidderUnit", "areaName", "infoType", "budgetAmount", "biddingAmount", "publishTime", "url"})
ACCESS_MODES = ("auto", "guest", "authenticated")


def validate_access_state(snapshot: dict[str, Any], *, validate_mode: bool = True) -> None:
    if validate_mode and ("access_mode" in snapshot or "access_mode_source" in snapshot):
        if snapshot.get("access_mode") not in {"guest", "authenticated"} or snapshot.get("access_mode_source") not in {"default", "explicit"}:
            raise SkillError("FOLLOW_UP_UNAVAILABLE", "查询模式或选择来源缺失／无效，不能猜测是否使用积分。")
    if "delivered_position" in snapshot and (type(snapshot["delivered_position"]) is not int or snapshot["delivered_position"] < 0):
        raise SkillError("FOLLOW_UP_UNAVAILABLE", "已交付位置无效，无法准确续查。")
    if "seen_ids" in snapshot and (not isinstance(snapshot["seen_ids"], list) or any(not isinstance(i, str) for i in snapshot["seen_ids"])):
        raise SkillError("FOLLOW_UP_UNAVAILABLE", "已展示公告记录无效，无法准确续查。")
    pending = snapshot.get("pending_cards", [])
    if not isinstance(pending, list) or any(not isinstance(c, dict) for c in pending):
        raise SkillError("FOLLOW_UP_UNAVAILABLE", "待展示记录无效，无法准确续查。")
    if pending and "delivered_position" not in snapshot:
        raise SkillError("FOLLOW_UP_UNAVAILABLE", "待展示记录缺少已交付位置。")
    for field, maximum in (("viewable_page_count", 10), ("max_viewable_rows", 300)):
        value = snapshot.get(field)
        if value is not None and (type(value) is not int or not 0 <= value <= maximum):
            raise SkillError("FOLLOW_UP_UNAVAILABLE", "免费边界无效，无法准确续查。")


def persist_access_choice(snapshot: dict[str, Any], client: ApiClient) -> None:
    # A new explicit instruction supersedes old preference even if the API fails.
    if client.access_mode_source == "explicit" and (snapshot.get("access_mode"), snapshot.get("access_mode_source")) != (client.access_mode, client.access_mode_source) and snapshot.get("result_set_id") and not snapshot.get("_context_only"):
        snapshot.update(access_mode=client.access_mode, access_mode_source=client.access_mode_source)
        save_snapshot(snapshot)


def select_access_mode(client: ApiClient, args: argparse.Namespace, result_type: str,
                       snapshot: dict[str, Any] | None = None) -> None:
    requested = getattr(args, "access_mode", "auto")
    if snapshot is not None:
        validate_access_state(snapshot, validate_mode=requested == "auto")
    api_key = getattr(client, "api_key", os.environ.get("QIANLIMA_API_KEY"))
    requested = getattr(args, "access_mode", "auto")
    if requested not in ACCESS_MODES:
        raise SkillError("INVALID_QUERY", "access-mode 仅支持 auto、guest、authenticated。")
    source = "explicit" if requested != "auto" else "default"
    if requested == "auto" and snapshot and snapshot.get("access_mode_source") == "explicit":
        requested = snapshot.get("access_mode", "auto")
        source = "explicit"
    mode = ("authenticated" if api_key else "guest") if requested == "auto" and result_type == "project" else ("authenticated" if requested == "auto" else requested)
    if mode == "guest" and result_type != "project":
        raise SkillError("FREE_CAPABILITY_UNAVAILABLE", "免费查询仅支持普通标讯列表；此能力需要登录并使用账号积分。")
    if mode == "authenticated" and not api_key and not getattr(client, "mock_dir", None):
        raise SkillError("MISSING_API_KEY", "还没有配置 API Key。")
    client.access_mode, client.access_mode_source = mode, source


def mode_query_input(query: dict[str, Any], args: argparse.Namespace, result_type: str,
                     snapshot: dict[str, Any] | None = None) -> dict[str, Any]:
    requested = getattr(args, "access_mode", "auto")
    if requested == "auto" and snapshot and snapshot.get("access_mode_source") == "explicit":
        requested = snapshot.get("access_mode", "auto")
    guest = requested == "guest" or (requested == "auto" and not os.environ.get("QIANLIMA_API_KEY"))
    if result_type == "project" and guest:
        return {**query, "numPerPage": 30}
    return query


def apply_access_paging(client: ApiClient, query: dict[str, Any]) -> None:
    if client.access_mode == "guest":
        query["numPerPage"] = 30  # Local executed page size; never sent to free API.


def free_protocol_issues(data: Any, query: dict[str, Any]) -> list[str]:
    if not isinstance(data, dict):
        return ["免费响应缺少分页对象"]
    issues = []
    if "accessMode" in data and data["accessMode"] != "GUEST":
        issues.append("免费响应模式异常")
    for field, expected in (("numPerPage", 30), ("currentPage", query["currentPage"])):
        if field in data and (type(data[field]) is not int or data[field] != expected):
            issues.append(f"免费响应 {field} 异常")
    for field, maximum in (("viewablePageCount", 10), ("maxViewableRows", 300)):
        if field in data and (type(data[field]) is not int or not 0 <= data[field] <= maximum):
            issues.append(f"免费响应 {field} 异常")
    for field in ("rowCount", "pageCount"):
        if type(data.get(field)) is not int or data[field] < 0:
            issues.append(f"免费响应 {field} 异常")
    total = data.get("rowCount")
    if type(total) is int and total >= 0:
        total_pages = (total + 29) // 30
        # The deployed free API caps pageCount at ten; older responses used
        # total pages. Both are consistent with fixed-size free pagination.
        if type(data.get("pageCount")) is int and data["pageCount"] not in {total_pages, min(10, total_pages)}:
            issues.append("免费响应 pageCount 与总数及固定页大小不一致")
        if type(data.get("viewablePageCount")) is int and data["viewablePageCount"] > min(10, total_pages):
            issues.append("免费可访问页数超过结果范围")
    if not isinstance(data.get("list"), list) or len(data["list"]) > 30:
        issues.append("免费响应列表异常")
    return issues



def free_pagination_facts(data: dict[str, Any]) -> dict[str, Any]:
    """Local pagination derived from published limits; never rewrite API data."""
    total = data.get("rowCount")
    total_pages = (total + 29) // 30 if type(total) is int and total >= 0 else None
    max_rows = data.get("maxViewableRows", 300)
    viewable = data.get("viewablePageCount", min(10, total_pages) if total_pages is not None else None)
    if type(max_rows) is int and type(viewable) is int:
        viewable = min(viewable, (max_rows + 29) // 30)
    return {"page_count": total_pages, "api_page_count": data.get("pageCount"),
            "page_count_source": "rowCount_and_fixed_page_size_30",
            "viewable_page_count": viewable, "max_viewable_rows": max_rows}


def search_access_state(payload: dict[str, Any], client: ApiClient, query: dict[str, Any],
                        cards: list[dict[str, Any]], previous: dict[str, Any] | None = None) -> dict[str, Any]:
    seen = list((previous or {}).get("seen_ids", []))
    seen = list(dict.fromkeys([*seen, *[str(c["id"]) for c in cards if isinstance(c, dict) and c.get("id") is not None]]))
    return {"access_mode": client.access_mode, "access_mode_source": client.access_mode_source,
            "viewable_page_count": payload.get("viewable_page_count"),
            "max_viewable_rows": payload.get("max_viewable_rows"),
            "delivered_position": payload.get("delivered_position", (query["currentPage"] - 1) * query["numPerPage"] + payload.get("api_returned_count", len(cards))),
            "seen_ids": seen, "pending_cards": []}


def validate_delivery_progress(snapshot: dict[str, Any]) -> None:
    """Reject incomplete partial-page contexts rather than skip unseen results."""
    delivered = snapshot.get("delivered_position")
    if delivered is None:
        return  # Legacy complete-page contexts retain their established behavior.
    query = snapshot["effective_query"]
    fetched_end = query["currentPage"] * query["numPerPage"]
    total = usable_count(snapshot.get("total_count"))
    if total is not None:
        fetched_end = min(fetched_end, total)
    # A saved response also tells us when the last fetched page was short.
    if not snapshot.get("_context_only") and not snapshot.get("pending_cards"):
        cards = snapshot.get("cards", [])
        if delivered == (query["currentPage"] - 1) * query["numPerPage"] + len(cards):
            return
    pending = snapshot.get("pending_cards", [])
    if delivered < fetched_end and delivered + len(pending) < fetched_end:
        raise SkillError("FOLLOW_UP_UNAVAILABLE", "部分结果尚未展示，但续查上下文缺少剩余卡片；请恢复完整展示进度，不能跳过未展示记录。")


def free_continuation_notice(snapshot: dict[str, Any]) -> str | None:
    if snapshot.get("access_mode") != "guest":
        return None
    query = snapshot.get("effective_query") or {}
    position = snapshot.get("delivered_position")
    if position is None:
        position = (query.get("currentPage", 1) - 1) * 30 + snapshot.get("api_returned_count", snapshot.get("returned_count", 0))
    total = usable_count(snapshot.get("total_count"))
    if total is not None and position >= total:
        return "当前查询结果已展示完毕。"
    rows = usable_count(snapshot.get("max_viewable_rows"))
    pages = usable_count(snapshot.get("viewable_page_count"))
    limit = min(300, rows if rows is not None else 300, 30 * (pages if pages is not None else 10))
    if position >= limit:
        return "已达到免费访问上限（最多前 10 页／300 条），匹配结果仍可能有更多。"
    return None


def pending_search_result(snapshot: dict[str, Any], client: ApiClient, capability: SearchCapabilitySpec,
                          session_id: str) -> dict[str, Any] | None:
    pending = snapshot.get("pending_cards", [])
    if not pending:
        return None
    if not isinstance(pending, list) or any(not isinstance(c, dict) for c in pending):
        raise SkillError("FOLLOW_UP_UNAVAILABLE", "待展示结果不完整，无法准确继续。")
    delivered = snapshot.get("delivered_position")
    if type(delivered) is not int or delivered < 0:
        raise SkillError("FOLLOW_UP_UNAVAILABLE", "缺少待展示结果的准确位置。")
    row_limit = snapshot.get("max_viewable_rows") if snapshot.get("max_viewable_rows") is not None else 300
    page_limit = snapshot.get("viewable_page_count") if snapshot.get("viewable_page_count") is not None else 10
    maximum = min(30, max(0, min(300, row_limit, page_limit * 30) - delivered)) if client.access_mode == "guest" else len(pending)
    if not maximum:
        return None  # Normal next boundary handling will report the free cap.
    taken, remainder = pending[:maximum], pending[maximum:]
    if client.access_mode == "guest":
        taken = [{k: v for k, v in c.items() if k in FREE_CARD_FIELDS} for c in taken]
        remainder = [{k: v for k, v in c.items() if k in FREE_CARD_FIELDS} for c in remainder]
    seen = snapshot.get("seen_ids", [])
    shown = [c for c in taken if str(c.get("id")) not in seen]
    query = snapshot["effective_query"]
    payload = {"ok": True, "result_type": capability.result_type, "cards": shown,
               "returned_count": len(shown), "total_count": snapshot.get("total_count"),
               "page_count": snapshot.get("page_count"), "effective_query": query,
               "access_mode": client.access_mode, "access_mode_source": client.access_mode_source,
               "delivered_position": delivered + len(taken), "from_pending_cache": True,
               "viewable_page_count": snapshot.get("viewable_page_count"),
               "max_viewable_rows": snapshot.get("max_viewable_rows"), "warnings": []}
    payload.update(capability.message_renderer(capability=capability, effective_query=query,
                   total_count=snapshot.get("total_count"), returned_count=len(shown), viewed_cards=shown,
                   warnings=[], query_notice="继续展示已取得的结果，未重复请求接口。",
                   **({"continuation_notice": free_continuation_notice(payload)} if capability.result_type == "project" else {})))
    state = search_access_state(payload, client, query, shown, snapshot)
    state["pending_cards"] = remainder
    result = save_search_snapshot(session_id=session_id, result_type=capability.result_type,
                                  effective_query=query, viewed_cards=shown, total_count=snapshot.get("total_count"),
                                  page_count=snapshot.get("page_count"), parent_result_set_id=snapshot.get("result_set_id"), access_state=state)
    payload["follow_up"] = follow_up_metadata(result)
    if client.access_mode == "guest":
        attach_free_link_facts(payload, shown, has_key=bool(client.api_key))
    return payload


def attach_free_failure(payload: dict[str, Any], client: ApiClient, error: SkillError) -> dict[str, Any]:
    if client.access_mode == "guest":
        # Replace only the generic error summary, retaining unrelated query warnings.
        generic_summary = payload.get("message")
        payload["warnings"] = list(dict.fromkeys([
            *[warning for warning in payload.get("warnings", []) if warning != generic_summary],
            error.message,
        ]))
        payload.update(access_mode="guest", access_mode_source=client.access_mode_source,
                       user_message=error.message, message=error.message, retry_policy="no_automatic_retry")
        if isinstance(error.data, dict):
            payload["limit_response"] = error.data.get("data")
        payload["agent_instruction"] = "按服务端实际原因说明，不猜限额档位或恢复时间，不自动重试、去掉 Key、切收费或拆条件绕限；费用与登录引导按游客规则及会话授权执行。"
    return payload


def search_payload_for_capability(
    *,
    capability: SearchCapabilitySpec,
    client: ApiClient,
    effective_query: dict[str, Any],
    warnings: list[str],
    query_notice: str | None = None,
    skip: int = 0,
    seen_ids: list[str] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], int, int]:
    apply_access_paging(client, effective_query)
    data = validate_search_response(capability.search_call(client, effective_query))
    maintain_query_cache()
    cards = data.get("list") if isinstance(data, dict) else data
    if client.access_mode == "guest" and not isinstance(cards, list):
        return {"ok": True, "access_mode": "guest", "cards": [], "effective_query": effective_query,
                "request_query": client.last_request_query,
                "protocol_issues": free_protocol_issues(data, effective_query), "continuation_blocked": True,
                "user_message": "查询已成功，但免费响应列表或分页异常，暂停自动续查；原始业务响应已保留。"}, None, None, None
    if not isinstance(cards, list):
        total = data.get("rowCount") if isinstance(data, dict) else None
        pages = data.get("pageCount") if isinstance(data, dict) else None
        payload = {"ok": True, "result_type": capability.result_type, "request_api_path": client.last_request_path,
                   "effective_query": effective_query, "request_query": client.last_request_query,
                   "total_count": total, "returned_count": None, "page_count": pages, "cards": cards,
                   "warnings": warnings, "user_message": "查询成功，项目列表信息：" + clean_user_value(cards)}
        return payload, None, total, usable_count(pages)
    issues = free_protocol_issues(data, effective_query) if client.access_mode == "guest" else []
    if client.access_mode == "guest":
        cards = [{k: v for k, v in card.items() if k in FREE_CARD_FIELDS} for card in cards if isinstance(card, dict)]
    selected = cards[skip:]
    if seen_ids:
        selected = [c for c in selected if not isinstance(c, dict) or str(c.get("id")) not in seen_ids]
    viewed_cards = [capability.card_view(card) for card in selected]
    total_count = data.get("rowCount")
    payload: dict[str, Any] = {
        "ok": True,
        "capability": {
            "project": "search-projects",
            "purchase_intention": "search-purchase-intentions",
            "expiring_project": "search-expiring-projects",
        }[capability.result_type],
        "result_type": capability.result_type,
        "request_api_path": client.last_request_path,
        "total_count": total_count,
        "request_query": client.last_request_query,
        "returned_count": len(viewed_cards),
        "api_total_count": total_count,
        "api_returned_count": len(data.get("list") or []),
        "page_count": data.get("pageCount"),
        "effective_query": effective_query,
        "warnings": warnings,
        "cards": viewed_cards,
    }
    if client.access_mode == "guest" and (type(total_count) is not int or total_count < 0):
        payload.update(access_mode="guest", access_mode_source=client.access_mode_source,
                       protocol_issues=issues, continuation_blocked=True,
                       user_message="查询已成功，但免费响应缺少有效总数，暂停自动续查。\n" + "\n".join(user_card_list(viewed_cards)))
        payload.update(free_pagination_facts(data))
        attach_free_link_facts(payload, viewed_cards, has_key=bool(client.api_key))
        return payload, None, total_count, None
    if capability.include_stage_on_success:
        payload["stage"] = capability.success_stage
    else:
        payload["rejected_count"] = 0
    payload.update(
        capability.message_renderer(
            capability=capability,
            effective_query=effective_query,
            total_count=total_count if total_count is not None else EMPTY_DISPLAY,
            returned_count=len(viewed_cards),
            viewed_cards=viewed_cards,
            warnings=warnings,
            query_notice=query_notice,
            **({"continuation_notice": free_continuation_notice({**payload, "access_mode": client.access_mode,
                **(free_pagination_facts(data) if client.access_mode == "guest" else {})})} if capability.result_type == "project" else {}),
        )
    )
    payload.update(access_mode=client.access_mode, access_mode_source=client.access_mode_source)
    if client.access_mode == "guest":
        payload["unexpected_free_fields"] = sorted({key for card in data.get("list", []) if isinstance(card, dict) for key in card if key not in FREE_CARD_FIELDS})
        payload.update(free_pagination_facts(data))
        payload.update(access_facts={"list_uses_points": False, "has_key": bool(client.api_key),
                                     "detail_uses_points": True, "limits": {"minute": 20, "hour": 150, "day": 300}})
        attach_free_link_facts(payload, viewed_cards, has_key=bool(client.api_key))
        if issues:
            payload.update(protocol_issues=issues, continuation_blocked=True,
                           presentation_notice="免费响应模式或分页信息异常，保留业务响应，暂停自动续查。")
            return payload, None, total_count, None
    if query_notice:
        payload["query_notice"] = query_notice
    return payload, viewed_cards, total_count, usable_count(payload.get("page_count"))


def run_search(capability: SearchCapabilitySpec, raw_query: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    session_id = search_session_id(args)
    try:
        source_checked_query = sanitize_query_match_scopes(
            raw_query,
            getattr(args, "user_text", ""),
        )
        effective_query, warnings = capability.normalize_query(
            mode_query_input(source_checked_query, args, capability.result_type),
            force_page=1 if not source_checked_query.get("currentPage") else None,
        )
    except SkillError as exc:
        return failure_payload(stage=capability_failure_stage(capability), error=exc, effective_query=raw_query)

    client = build_client(args)
    select_access_mode(client, args, capability.result_type)
    try:
        payload, viewed_cards, total_count, page_count = search_payload_for_capability(
            capability=capability,
            client=client,
            effective_query=effective_query,
            warnings=warnings,
        )
    except SkillError as exc:
        payload = failure_payload(
            stage=capability_failure_stage(capability),
            error=exc,
            effective_query=effective_query,
            warnings=warnings,
        )
        payload["request_query"] = client.last_request_query
        payload = maybe_attach_entitlement_diagnosis(
            payload,
            client,
            exc,
            target_right=entitlement_right_name(operation="search", result_type=capability.result_type),
        )
        return attach_free_failure(payload, client, exc)

    if not isinstance(viewed_cards, list):
        return payload
    snapshot = save_search_snapshot(
        session_id=session_id,
        result_type=capability.result_type,
        effective_query=effective_query,
        viewed_cards=viewed_cards,
        total_count=total_count,
        page_count=page_count,
        access_state=search_access_state(payload, client, effective_query, viewed_cards),
    )
    payload["follow_up"] = follow_up_metadata(snapshot)
    payload["request_query"] = client.last_request_query
    return payload


@api_command
def cmd_search_purchase(args: argparse.Namespace) -> dict[str, Any]:
    return run_search(SEARCH_CAPABILITIES["purchase_intention"], parse_query_json(args.query_json), args)


@api_command
def cmd_search_expiring(args: argparse.Namespace) -> dict[str, Any]:
    return run_search(SEARCH_CAPABILITIES["expiring_project"], parse_query_json(args.query_json), args)


def normalize_enterprise_query(raw: dict[str, Any], kind: str) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    allowed_fields = ENTERPRISE_QUERY_FIELDS.get(kind)
    if allowed_fields is None:
        raise SkillError("INVALID_QUERY", "企业情报类型不在支持范围内。")
    reject_unsupported_fields(raw, allowed_fields, f"企业情报 {kind}")
    query = {k: v for k, v in dict(raw).items() if v not in (None, "", [], {})}
    if not query.get("companyName"):
        raise SkillError("INVALID_QUERY", "企业名称不能为空，请提供要查询的企业名称。")
    if kind == "contacts":
        query.setdefault("currentPage", 1)
        query.setdefault("numPerPage", 30)
        query["currentPage"] = int_query_value(query["currentPage"], 1, "页码", warnings)
        query["numPerPage"] = min(100, max(1, int_query_value(query["numPerPage"], 30, "每页数量", warnings)))
        if query.get("phoneType") is not None:
            query["phoneType"] = normalize_int_enum(query["phoneType"], "phoneType", PHONE_TYPES)
    if query.get("sortType") is not None:
        query["sortType"] = normalize_int_enum(query["sortType"], "sortType", ENTERPRISE_SORT_TYPES)
    for field in ("beginTime", "endTime"):
        if field in query and query[field]:
            try:
                dt.datetime.strptime(str(query[field]), "%Y-%m-%d")
            except ValueError as exc:
                raise SkillError("INVALID_QUERY", "时间格式需要写成 YYYY-MM-DD，例如 2026-04-20。") from exc
    validate_date_order(query, "beginTime", "endTime", "开始时间不能晚于结束时间，请调整时间范围后再查。")
    if kind not in {"business-info", "contacts"} and not query.get("beginTime") and not query.get("endTime"):
        warnings.append("未传时间参数，企业情报接口默认按近一年查询。")
    return query, warnings


@api_command
def cmd_enterprise(args: argparse.Namespace) -> dict[str, Any]:
    raw_query = parse_query_json(args.query_json)
    try:
        effective_query, warnings = normalize_enterprise_query(raw_query, args.kind)
    except SkillError as exc:
        return failure_payload(stage="enterprise", error=exc, effective_query=raw_query)
    client = build_client(args)
    try:
        data = validate_enterprise_response(client.enterprise(args.kind, effective_query), args.kind)
    except SkillError as exc:
        payload = failure_payload(stage="enterprise", error=exc, effective_query=effective_query, warnings=warnings)
        payload["request_query"] = client.last_request_query
        payload = maybe_attach_entitlement_diagnosis(
            payload,
            client,
            exc,
            target_right=entitlement_right_name(operation="enterprise", enterprise_kind=args.kind),
        )
        return payload
    rows = data.get("list") if isinstance(data.get("list"), list) else [data]
    rows = rows or []
    return {
        "ok": True,
        "capability": "enterprise-intel",
        "result_type": "enterprise_" + args.kind.replace("-", "_"),
        "request_api_path": client.last_request_path,
        "stage": "enterprise_" + args.kind.replace("-", "_"),
        "paid_sensitive": args.kind == "contacts",
        "total_count": data.get("rowCount") if isinstance(data, dict) else None,
        "returned_count": len(rows),
        "page_count": data.get("pageCount") if isinstance(data, dict) else None,
        "effective_query": effective_query,
        "warnings": warnings,
        "rows": rows,
        "request_query": client.last_request_query,
        "user_message": user_enterprise_message(args.kind, effective_query, rows, warnings),
    }


@api_command
def cmd_verify(args: argparse.Namespace) -> dict[str, Any]:
    client = build_client(args)
    data = validate_verify_response(client.verify())
    return {"ok": True, "total_count": 1, "returned_count": 1, "effective_query": {}, "warnings": [], "user": data}


@api_command
def cmd_entitlement(args: argparse.Namespace) -> dict[str, Any]:
    wallet = normalize_entitlement_data(build_client(args).entitlement())
    return {"ok":True, "stage":"entitlement", "total_count":1, "returned_count":1,
            "effective_query":{}, "warnings":[], **wallet, "user_message":user_entitlement_message(wallet)}


def validate_refine_amount_changes(result_type: str, previous_query: dict[str, Any], patch_query: dict[str, Any]) -> None:
    """Inherited amounts keep their units; only new amount values need checking."""
    changed_amounts = {AMOUNT_UNIT_CONFIRMATION_FIELD: patch_query.get(AMOUNT_UNIT_CONFIRMATION_FIELD)}
    amount_fields = tuple((field, "金额") for field in SEARCH_AMOUNT_FIELDS[result_type])
    for field, label in amount_fields:
        if field not in patch_query or patch_query[field] in (None, ""):
            continue
        value = numeric_query_value(patch_query[field], label)
        previous = previous_query.get(field)
        if previous is None or value != numeric_query_value(previous, label):
            changed_amounts[field] = value
    validate_amount_unit(changed_amounts, amount_fields)


def normalize_complex_operation(
    data_source: str,
    action: str,
    query: dict[str, Any],
    operation: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    if data_source in SEARCH_CAPABILITIES and action == "search":
        return SEARCH_CAPABILITIES[data_source].normalize_query(query, force_page=1)

    if data_source == "enterprise" and action == "search":
        kind = str(operation.get("enterprise_kind") or "")
        return normalize_enterprise_query(query, kind)

    if data_source in SEARCH_CAPABILITIES and action == "refine":
        session_value = operation.get("session_id")
        session_id = canonical_uuid(session_value, code="INVALID_SESSION_ID", label="会话编号") if session_value is not None else None
        result_set_id = canonical_uuid(
            operation.get("result_set_id"), code="INVALID_RESULT_SET_ID", label="结果集编号"
        )
        snapshot = load_snapshot(session_id, result_set_id)
        capability = search_capability(str(snapshot["result_type"]))
        if capability.result_type != data_source:
            raise PlanValidationError("refine 数据源与当前结果集不一致。")
        if snapshot.get("origin") == "timeline":
            raise PlanValidationError("时间线节点不支持修改搜索条件。")
        patch = apply_refine_aliases(capability, query)
        if data_source == "project" and "keywordGroups" in patch:
            context = operation.get("_project_refine_context") or {}
            if context.get("mode") == "ambiguous":
                raise PlanValidationError("Agent 需根据当前 effective_query 和用户原话构造完整 keyword_group 修改计划，保留未改词组；不要让用户填写内部参数。")
            if context.get("mode") == "generic":
                old_groups = snapshot["effective_query"].get("keywordGroups", [])
                business_scopes = {1, 2, 8, 9, 10}
                candidates = [index for index, group in enumerate(old_groups)
                              if group.get("matchScopes") and set(group["matchScopes"]) <= business_scopes]
                if len(candidates) != 1:
                    raise PlanValidationError("Agent 无法唯一定位待改业务词组，需根据当前 effective_query 和用户原话构造完整 keyword_group 修改计划；不要让用户填写内部参数。")
                index = candidates[0]
                new_groups = normalize_keyword_groups(patch["keywordGroups"])
                if not context.get("explicit_scopes"):
                    new_groups = [{"keywords": group["keywords"], "matchScopes": list(old_groups[index]["matchScopes"])}
                                  for group in new_groups]
                patch["keywordGroups"] = [*old_groups[:index], *new_groups, *old_groups[index + 1:]]
        if data_source == "project" and "matchScopes" in patch:
            scopes = patch.pop("matchScopes")
            old_groups = snapshot["effective_query"].get("keywordGroups", [])
            if not old_groups or any(set(g["matchScopes"]) != set(old_groups[0]["matchScopes"]) for g in old_groups[1:]):
                raise PlanValidationError("当前关键词组有不同匹配位置，请明确要修改的组。")
            patch["keywordGroups"] = [{"keywords": list(g["keywords"]), "matchScopes": scopes} for g in old_groups]
        merged = dict(snapshot["effective_query"])
        merged.update(patch)
        merged["currentPage"] = 1
        validate_refine_amount_changes(capability.result_type, snapshot["effective_query"], patch)
        validate_continuation_paging(merged, capability.result_type, require_complete=False)
        merged[AMOUNT_UNIT_CONFIRMATION_FIELD] = True
        normalized_merged, warnings = capability.normalize_query(merged, force_page=1)
        normalized_patch = {
            field: ([] if field == "areaIds" and patch[field] == [] else normalized_merged.get(field))
            for field in patch
            if field in normalized_merged or patch[field] is None or (field == "areaIds" and patch[field] == [])
        }
        return normalized_patch, warnings

    raise PlanValidationError("复杂查询操作不受支持。")


def cmd_preflight_complex(args: argparse.Namespace) -> dict[str, Any]:
    plan = parse_query_json(args.plan_json)
    output = preflight_complex_plan(plan, normalize_complex_operation, user_text=args.user_text)
    requested = getattr(args, "access_mode", "auto")
    executable = []
    for operation in output.get("approved_operations", []):
        mode = requested if requested != "auto" else operation.get("access_mode", "auto")
        if mode not in ACCESS_MODES:
            return {"ok": False, "error_code": "FREE_CAPABILITY_UNAVAILABLE", "approved_operations": [],
                    "user_message": "当前模式不支持计划中的数据源；免费仅支持普通标讯列表。"}
        if mode == "guest" and operation["data_source"] != "project":
            output.setdefault("unresolved_conditions", []).append({
                "scope": "branch", "operation_id": operation["id"],
                "error_code": "FREE_CAPABILITY_UNAVAILABLE",
                "reason": "此分支需要登录并使用账号积分；保留待办，其他可执行免费分支继续。",
            })
            continue
        operation["access_mode"] = mode
        executable.append(operation)
    if output.get("approved_operations"):
        output["approved_operations"] = executable
        output["approved_business_calls"] = len(executable)
        output["ok"] = bool(executable)
        if not executable:
            output["error_code"] = "FREE_CAPABILITY_UNAVAILABLE"
            output["fallback_status"] = "blocked"
            output["user_message"] = "当前模式不支持计划中的数据源；免费仅支持普通标讯列表。"
    return output


@api_command
def cmd_search(args: argparse.Namespace) -> dict[str, Any]:
    return run_search(SEARCH_CAPABILITIES["project"], parse_query_json(args.query_json), args)


def query_continuation_context(args: argparse.Namespace, *, company: bool = False) -> tuple[str, dict[str, Any]]:
    """Resume only an explicit result reference or a complete supplied query."""
    raw_context = getattr(args, "context_json", None)
    if raw_context is not None:
        context = parse_query_json(raw_context)
        result_type = context.get("result_type")
        allowed_sources = {"company_candidates"} if company else set(SEARCH_CAPABILITIES)
        if result_type is None:
            raise SkillError("FOLLOW_UP_UNAVAILABLE", "续查上下文缺少数据源 result_type，无法准确继续。", {"missing_fields": ["result_type"]})
        if not isinstance(result_type, str) or result_type not in allowed_sources or context.get("origin") == "timeline":
            raise SkillError("INVALID_QUERY", "完整上下文的数据源不支持本次续查动作。")
        query = context.get("effective_query")
        if not isinstance(query, dict):
            raise SkillError("FOLLOW_UP_UNAVAILABLE", "缺少原查询的完整条件，无法准确继续。")
        size_field = "pageSize" if company else "numPerPage"
        missing = [field for field in ("currentPage", size_field) if field not in query]
        required_field = "companyName" if company else "keywordGroups" if result_type == "project" else "keywords"
        if not query.get(required_field):
            missing.append(required_field)
        if missing:
            raise SkillError("FOLLOW_UP_UNAVAILABLE", "续查上下文缺少必要内容：" + "、".join(missing) + "。", {"missing_fields": missing})
        validate_continuation_paging(query, result_type)
        if company:
            effective_query = normalize_company_query(query)
        else:
            # Full context restores a previously executed effective query. Its
            # inherited amounts already use yuan; only refine changes need a
            # fresh unit check. Keep all other source and parameter validation.
            effective_query = search_capability(result_type).normalize_query(
                {**query, AMOUNT_UNIT_CONFIRMATION_FIELD: True}, check_time_span=False,
            )[0]
        session_id = search_session_id(args)
        snapshot = {
            "state_version": STATE_VERSION, "session_id": session_id,
            "result_set_id": getattr(args, "result_set_id", None),
            "result_type": result_type, "effective_query": effective_query,
            "cards": [], "focus_project": None,
            "total_count": context.get("total_count"),
            "page_count": usable_count(context.get("page_count")),
            "expires_at": expires_at_iso(), "_context_only": True,
        }
        for field in ("access_mode", "access_mode_source", "viewable_page_count", "max_viewable_rows", "delivered_position", "seen_ids", "pending_cards"):
            if field in context:
                snapshot[field] = copy.deepcopy(context[field])
        return session_id, snapshot
    requested_session_id, result_set_id = follow_up_context(args)
    snapshot = load_snapshot(requested_session_id, result_set_id)
    if snapshot.get("origin") == "timeline" or (snapshot["result_type"] == "company_candidates") != company:
        raise SkillError("INVALID_QUERY", "当前结果不支持本次续查动作，请使用该结果的对应动作。")
    validate_continuation_paging(snapshot["effective_query"], snapshot["result_type"])
    return requested_session_id or snapshot["session_id"], snapshot


@api_command
def cmd_next(args: argparse.Namespace) -> dict[str, Any]:
    session_id, snapshot = query_continuation_context(args)
    result_set_id = snapshot.get("result_set_id")
    capability = search_capability(str(snapshot["result_type"]))
    previous_query = snapshot["effective_query"]
    capability.normalize_query({**previous_query, AMOUNT_UNIT_CONFIRMATION_FIELD: True})
    client = build_client(args)
    select_access_mode(client, args, capability.result_type, snapshot)
    previous_mode = snapshot.get("access_mode")
    persist_access_choice(snapshot, client)
    validate_delivery_progress(snapshot)
    pending_payload = pending_search_result(snapshot, client, capability, session_id)
    if pending_payload is not None:
        return pending_payload
    current_page = previous_query["currentPage"]
    previous_size = previous_query["numPerPage"]
    delivered = snapshot.get("delivered_position", current_page * previous_size)
    if type(delivered) is not int or delivered < 0:
        raise SkillError("FOLLOW_UP_UNAVAILABLE", "缺少准确的已交付位置，无法续查。")
    target_size = 30 if client.access_mode == "guest" or previous_mode == "guest" else previous_size
    next_page, skip = divmod(delivered, target_size)
    next_page += 1
    if target_size == previous_size and not snapshot.get("pending_cards"):
        next_page, skip = current_page + 1, 0
    page_count = usable_count(snapshot.get("page_count"))
    total = usable_count(snapshot.get("total_count"))
    if client.access_mode == "guest" and total is not None and total <= 300 and delivered >= total:
        return failure_payload(stage="next", error=SkillError("NO_MORE_PAGES", "当前结果已经是最后一页。"), effective_query=previous_query)
    if client.access_mode == "guest":
        limit = min(300, snapshot.get("max_viewable_rows") if snapshot.get("max_viewable_rows") is not None else 300)
        pages = min(10, usable_count(snapshot.get("viewable_page_count")) if snapshot.get("viewable_page_count") is not None else 10)
        if delivered >= limit or next_page > pages:
            return attach_free_failure(failure_payload(stage="next", error=SkillError("FREE_PAGE_LIMIT", "免费查询最多查看可访问的前 10 页／300 条；匹配结果可能仍有更多。"), effective_query=previous_query), client, SkillError("FREE_PAGE_LIMIT", "已达到免费可访问范围，匹配结果可能仍有更多。"))
    if (previous_size != target_size and total is not None and delivered >= total) or (previous_size == target_size and page_count is not None and current_page >= page_count):
        payload = failure_payload(stage="next", error=SkillError("NO_MORE_PAGES", "当前结果已经是最后一页。"), effective_query=previous_query)
        payload["follow_up"] = follow_up_metadata(snapshot)
        return payload
    next_query = dict(previous_query)
    next_query.update(currentPage=next_page, numPerPage=target_size)
    next_query[AMOUNT_UNIT_CONFIRMATION_FIELD] = True
    effective_query, warnings = capability.normalize_query(next_query)
    if target_size != previous_size:
        warnings.append("分页大小已变化；结果动态更新或综合排序的页内重排可能影响衔接，已过滤重叠位置和已展示公告，不保证无遗漏，不自动重放历史页。")
    try:
        payload, viewed_cards, total_count, page_count = search_payload_for_capability(
            capability=capability,
            client=client,
            effective_query=effective_query,
            warnings=warnings,
            query_notice="当前查询条件未变，按已交付位置继续。",
            skip=skip, seen_ids=snapshot.get("seen_ids", []),
        )
    except SkillError as exc:
        payload = failure_payload(stage="next", error=exc, effective_query=effective_query, warnings=warnings)
        payload["follow_up"] = follow_up_metadata(snapshot)
        payload["request_query"] = client.last_request_query
        payload = maybe_attach_entitlement_diagnosis(
            payload,
            client,
            exc,
            target_right=entitlement_right_name(operation="search", result_type=capability.result_type),
        )
        return attach_free_failure(payload, client, exc)
    if not isinstance(viewed_cards, list):
        return payload
    if not snapshot.get("_context_only"):
        snapshot.update(access_mode=client.access_mode, access_mode_source=client.access_mode_source)
        save_snapshot(snapshot)
    next_snapshot = save_search_snapshot(
        session_id=session_id,
        result_type=capability.result_type,
        effective_query=effective_query,
        total_count=total_count,
        page_count=page_count,
        viewed_cards=viewed_cards,
        parent_result_set_id=result_set_id,
        access_state=search_access_state(payload, client, effective_query, viewed_cards, snapshot),
    )
    payload["follow_up"] = follow_up_metadata(next_snapshot)
    payload["request_query"] = client.last_request_query
    return payload


@api_command
def cmd_refine(args: argparse.Namespace) -> dict[str, Any]:
    session_id, snapshot = query_continuation_context(args)
    result_set_id = snapshot.get("result_set_id")
    capability = search_capability(str(snapshot["result_type"]))
    raw_patch = sanitize_query_match_scopes(parse_query_json(args.query_json), args.user_text)
    patch_query = apply_refine_aliases(capability, raw_patch)
    base_query = dict(snapshot["effective_query"])
    base_query.update(patch_query)
    base_query["currentPage"] = 1
    base_query = mode_query_input(base_query, args, capability.result_type, snapshot)
    try:
        validate_refine_amount_changes(capability.result_type, snapshot["effective_query"], patch_query)
        validate_continuation_paging(base_query, capability.result_type)
        base_query[AMOUNT_UNIT_CONFIRMATION_FIELD] = True
        effective_query, warnings = capability.normalize_query(base_query)
    except SkillError as exc:
        payload = failure_payload(stage=capability_failure_stage(capability), error=exc, effective_query=base_query)
        payload["follow_up"] = follow_up_metadata(snapshot)
        return payload

    client = build_client(args)
    select_access_mode(client, args, capability.result_type, snapshot)
    persist_access_choice(snapshot, client)
    try:
        payload, viewed_cards, total_count, page_count = search_payload_for_capability(
            capability=capability,
            client=client,
            effective_query=effective_query,
            warnings=warnings,
        )
    except SkillError as exc:
        payload = failure_payload(
            stage=capability_failure_stage(capability),
            error=exc,
            effective_query=effective_query,
            warnings=warnings,
        )
        payload["follow_up"] = follow_up_metadata(snapshot)
        payload["request_query"] = client.last_request_query
        payload = maybe_attach_entitlement_diagnosis(
            payload,
            client,
            exc,
            target_right=entitlement_right_name(operation="search", result_type=capability.result_type),
        )
        return attach_free_failure(payload, client, exc)

    if not isinstance(viewed_cards, list):
        return payload
    if not snapshot.get("_context_only"):
        snapshot.update(access_mode=client.access_mode, access_mode_source=client.access_mode_source)
        save_snapshot(snapshot)
    refined_snapshot = save_search_snapshot(
        session_id=session_id,
        result_type=capability.result_type,
        effective_query=effective_query,
        viewed_cards=viewed_cards,
        total_count=total_count,
        page_count=page_count,
        parent_result_set_id=result_set_id,
        access_state=search_access_state(payload, client, effective_query, viewed_cards),
    )
    payload["follow_up"] = follow_up_metadata(refined_snapshot)
    payload["request_query"] = client.last_request_query
    payload["query_notice"] = "已在当前查询条件上调整并重新查询。"
    return payload


def parse_fields(fields: str | None, result_type: str) -> list[str] | None:
    if not fields:
        return None
    requested = [field.strip() for field in fields.split(",") if field.strip()]
    allowed = set(detail_fields_for_result_type(result_type))
    if result_type in SOURCE_URL_RESULT_TYPES:
        allowed.add("sourceUrl")
    invalid = [field for field in requested if field not in allowed]
    if invalid:
        raise correction_error(
            "AGENT_DETAIL_CORRECTION_REQUIRED",
            "当前结果类型不支持这些详情字段。",
            f"删除不支持字段：{', '.join(invalid)}；只请求当前结果类型支持的详情字段后重试，不要询问用户。",
            unsupported_fields=invalid,
            allowed_fields=sorted(allowed),
        )
    return requested


def ordinal_from_ref(ref: str) -> int | None:
    text = ref.strip()
    match = re.search(r"^第\s*(\d{1,3})\s*[个条项]?(?:的.*)?$", text)
    if match:
        return int(match.group(1))
    match = re.search(r"^第\s*([一二两三四五六七八九十]{1,3})\s*[个条项]?(?:的.*)?$", text)
    if match:
        return CHINESE_ORDINALS.get(match.group(1))
    if text.isdigit() and len(text) <= 3:
        return int(text)
    return None


FOCUS_PROJECT_REFS = {
    "这条",
    "这一条",
    "这个",
    "这个项目",
    "这个商机",
    "这个结果",
    "这项",
    "这一项",
    "该项目",
    "该商机",
    "它",
    "当前项目",
    "当前商机",
}


def resolve_project(ref: str, cards: list[dict[str, Any]], focus_project: dict[str, Any] | None = None) -> dict[str, Any]:
    extracted = ref.strip()
    if extracted in FOCUS_PROJECT_REFS and focus_project:
        focus_id = canonical_project_id(focus_project.get("id"))
        matches = [card for card in cards if canonical_project_id(card.get("id")) == focus_id]
        if matches:
            return {"status": "matched", "method": "focus_project", "extracted_ref": extracted, "matches": matches}
    ordinal = ordinal_from_ref(extracted)
    if ordinal is not None:
        if 1 <= ordinal <= len(cards):
            return {"status": "matched", "method": "ordinal", "extracted_ref": extracted, "ordinal": ordinal, "matches": [cards[ordinal - 1]]}
        return {"status": "not_found", "method": "ordinal", "extracted_ref": extracted, "ordinal": ordinal, "matches": []}

    id_match = re.fullmatch(r"(?:(?:公告|项目)?\s*ID\s*[:：]?\s*)?(\d{6,})", extracted, flags=re.IGNORECASE)
    if id_match:
        project_id = id_match.group(1)
        matches = [card for card in cards if canonical_project_id(card.get("id")) == project_id]
        return {
            "status": "matched" if len(matches) == 1 else "not_found",
            "method": "project_id",
            "extracted_ref": project_id,
            "matches": matches,
        }

    lowered = extracted.lower()
    matches = []
    for card in cards:
        haystack = " ".join(str(card.get(field, "")) for field in ("title", "purchasingUnit", "areaName", "infoType")).lower()
        if lowered and lowered in haystack:
            matches.append(card)
    status = "matched" if len(matches) == 1 else "ambiguous" if len(matches) > 1 else "not_found"
    return {"status": status, "method": "text", "extracted_ref": extracted, "matches": matches}


def announcement_context(args: argparse.Namespace) -> tuple[dict[str, Any], SearchCapabilitySpec, dict[str, Any]]:
    """A declared announcement ID is independent of list membership and cache."""
    explicit_id = getattr(args, "id", None)
    ref = getattr(args, "project_ref", None) or ""
    legacy_id = re.fullmatch(r"(?:(?:公告|项目)?\s*ID\s*[:：]?\s*)?(\d{6,})", ref.strip(), flags=re.IGNORECASE)
    declared_source = getattr(args, "result_type", None)
    snapshot = None
    if explicit_id is not None:
        if not usable_project_id(explicit_id):
            raise correction_error("AGENT_DETAIL_CORRECTION_REQUIRED", "需要真实公告编号。", "将 --id 改为已明确的真实公告编号；不能用业务项目编号、公司编号、标题或序号代替。")
        project_id = canonical_project_id(explicit_id)
    elif legacy_id:
        project_id = legacy_id.group(1)
        if declared_source is None and getattr(args, "result_set_id", None):
            try:
                session_id, result_set_id = follow_up_context(args)
                snapshot = load_snapshot(session_id, result_set_id, for_query=False)
            except SkillError:
                # An optional old query reference cannot invalidate a known ID.
                snapshot = None
    else:
        session_id, result_set_id = follow_up_context(args)
        snapshot = load_snapshot(session_id, result_set_id, for_query=False)
        capability = search_capability(str(snapshot["result_type"]))
        resolution = resolve_project(ref, snapshot["cards"], snapshot.get("focus_project"))
        return snapshot, capability, resolution
    result_type = declared_source or (snapshot["result_type"] if snapshot else "project")
    capability = search_capability(result_type)
    project = next((item for item in snapshot["cards"] if canonical_project_id(item.get("id")) == project_id), None) if snapshot else None
    project = project or {"id": project_id}
    snapshot = snapshot or {"result_type": result_type, "effective_query": {}, "cards": [], "focus_project": None}
    resolution = {"status": "matched", "method": "project_id", "extracted_ref": project_id, "matches": [project]}
    return snapshot, capability, resolution


@api_command
def cmd_detail(args: argparse.Namespace) -> dict[str, Any]:
    snapshot, capability, resolution = announcement_context(args)
    cards = snapshot.get("cards") or []
    warnings: list[str] = []

    if resolution["status"] == "ambiguous":
        warnings.append("项目指代命中多个候选，未调用详情接口。请您补充序号、项目编号或更多标题词。")
        viewed_candidates = [capability.card_view(card) for card in resolution["matches"]]
        return {
            "ok": False,
            "total_count": len(resolution["matches"]),
            "returned_count": 0,
            "effective_query": snapshot.get("effective_query", {}),
            "warnings": warnings,
            "resolution": {k: v for k, v in resolution.items() if k != "matches"},
            "candidates": viewed_candidates,
            "user_message": user_detail_failure_message(
                snapshot.get("effective_query", {}),
                ["找到多条可能相关的项目，不能直接替您判断是哪一条。请您回复第几条或更多标题词。"],
                viewed_candidates,
                intro="我找到多条可能相关的项目，还不能直接判断您要查哪一个。",
                candidate_lines=capability.list_renderer(viewed_candidates),
            ),
            "follow_up": follow_up_metadata(snapshot),
        }

    if resolution["status"] != "matched":
        intro = "我没有在当前这批结果里准确找到您说的项目。请您回复项目序号，或提供项目名称里的几个关键词，我再继续查。"
        if resolution.get("method") == "ordinal":
            ordinal = resolution.get("ordinal")
            count = len(cards)
            if count:
                intro = f"当前这批结果只有 {count} 条，没有第 {ordinal} 条。请您回复 1 到 {count} 之间的序号，或提供项目名称里的几个关键词。"
            else:
                intro = "当前这批结果里没有可追问的项目。请您先查一批项目，再用第几条或标题关键词追问。"
        elif resolution.get("extracted_ref"):
            intro = f"我没有在当前这批结果里找到与“{resolution['extracted_ref']}”准确匹配的项目。请您换成结果里的序号，或提供项目名称中更具体的关键词。"
        warnings.append("当前结果集中未定位到该项目，未调用详情接口。请您提供结果序号、项目编号或更多标题词。")
        return {
            "ok": False,
            "total_count": 0,
            "returned_count": 0,
            "effective_query": snapshot.get("effective_query", {}),
            "warnings": warnings,
            "resolution": {k: v for k, v in resolution.items() if k != "matches"},
            "user_message": user_detail_failure_message(
                snapshot.get("effective_query", {}),
                ["当前这批结果里没有准确命中。请您回复第几条，或提供项目名称里的几个关键词。"],
                intro=intro,
            ),
            "follow_up": follow_up_metadata(snapshot),
        }

    project = resolution["matches"][0]
    project_id = project_id_for_request(project)
    source_only = False
    try:
        requested_fields = parse_fields(args.fields, capability.result_type)
        wants_source_url = args.source_url or bool(requested_fields and "sourceUrl" in requested_fields)
        if wants_source_url and capability.result_type not in SOURCE_URL_RESULT_TYPES:
            raise correction_error(
                "AGENT_DETAIL_CORRECTION_REQUIRED",
                "采购意向不支持原文链接接口。",
                "不要为采购意向请求 sourceUrl；改为返回采购意向详情页 url 或采购需求 purchaseContent，不要询问用户。",
                unsupported_fields=["sourceUrl"],
                allowed_fields=sorted(detail_fields_for_result_type(capability.result_type)),
            )
        requested_non_source_fields = [field for field in requested_fields or [] if field != "sourceUrl"]
        source_only = wants_source_url and not requested_non_source_fields
        if source_only and requested_fields is None:
            requested_fields = ["sourceUrl"]
    except SkillError as exc:
        payload = failure_payload(
            stage="detail",
            error=exc,
            effective_query=snapshot.get("effective_query", {}),
            resolution={k: v for k, v in resolution.items() if k != "matches"},
        )
        payload["follow_up"] = follow_up_metadata(snapshot)
        return payload
    client = build_client(args)
    detail_data: dict[str, Any] = dict(project)
    detail_failure = None
    if not source_only:
        try:
            detail_data = validate_detail_response(capability.detail_call(client, project_id))
            if isinstance(detail_data, dict) and str(detail_data.get("id")) != str(project_id):
                warnings.append("接口返回的项目编号与所选项目不同，以下内容按返回项目展示。")
        except SkillError as exc:
            payload = failure_payload(
                stage="detail",
                error=exc,
                effective_query=snapshot.get("effective_query", {}),
                resolution={k: v for k, v in resolution.items() if k != "matches"},
            )
            payload["follow_up"] = follow_up_metadata(snapshot)
            detail_failure = maybe_attach_entitlement_diagnosis(
                payload,
                client,
                exc,
                target_right=entitlement_right_name(operation="detail", result_type=capability.result_type),
            )
            if not wants_source_url:
                return detail_failure

    if wants_source_url:
        try:
            source = validate_source_url_response(client.source_url(project_id))
        except SkillError as exc:
            if detail_failure is not None:
                return detail_failure
            payload = failure_payload(
                stage="source_url",
                error=exc,
                effective_query=snapshot.get("effective_query", {}),
                resolution={k: v for k, v in resolution.items() if k != "matches"},
            )
            payload["follow_up"] = follow_up_metadata(snapshot)
            if exc.code == "10011":
                detail_url = clean_user_value(project.get("url"))
                if detail_url != EMPTY_DISPLAY:
                    payload["user_message"] = (
                        str(payload.get("user_message") or "").rstrip()
                        + f"\n\n原文暂不可用，你仍可以{markdown_link('查看项目详情', detail_url)}。"
                    )
            payload = maybe_attach_entitlement_diagnosis(
                payload, client, exc,
                target_right=entitlement_right_name(operation="source_url", result_type=capability.result_type),
            )
            if not source_only:
                save_focus_project(snapshot, project)
                payload.update(
                    partial_success=True, successful_resources=["detail"], failed_resources=["sourceUrl"],
                    retry_fields=["sourceUrl"], selected_project_id=project_id,
                    detail=detail_view(detail_data, requested_non_source_fields, capability.result_type),
                    full_detail=full_detail_view(detail_data, capability.result_type),
                )
                successful_message = user_detail_success_message(
                    full_detail_view(detail_data, capability.result_type), requested_non_source_fields,
                    {k:v for k,v in resolution.items() if k != "matches"}, capability.result_type,
                )
                payload["user_message"] = successful_message + "\n\n来源链接未取得。" + payload["user_message"]
                payload["agent_instruction"] = "已取得详情应直接交付；只在用户再次要求时重试 sourceUrl，不重放已成功的详情调用。"
            return payload
        source_value = source.get("sourceUrl") if isinstance(source, dict) else source
        if detail_failure is not None:
            detail_failure.update(partial_success=True, successful_resources=["sourceUrl"], failed_resources=["detail"],
                                  retry_fields=requested_non_source_fields, source_url=source)
            detail_failure["user_message"] += "\n\n来源链接：" + detail_display_value("sourceUrl", source_value)
            detail_failure["agent_instruction"] = "交付已成功的来源信息；不要重放已成功调用。"
            return detail_failure
        detail_data["sourceUrl"] = source_value

    save_focus_project(snapshot, project)
    return {
        "ok": True,
        "total_count": 1,
        "returned_count": 1,
        "effective_query": snapshot.get("effective_query", {}),
        "warnings": warnings,
        "resolution": {k: v for k, v in resolution.items() if k != "matches"},
        "detail": detail_view(detail_data, requested_fields, capability.result_type),
        "full_detail": full_detail_view(detail_data, capability.result_type),
        "selected_project_id": project_id,
        "follow_up": follow_up_metadata(snapshot),
        "user_message": user_detail_success_message(
            full_detail_view(detail_data, capability.result_type),
            requested_fields,
            {k: v for k, v in resolution.items() if k != "matches"},
            capability.result_type,
        ) + ("\n\n" + "；".join(warnings) if warnings else ""),
    }


RESOURCE_PATHS = {"full-text":"fullText", "attachments":"attachments", "timeline":"timeline"}
RESOURCE_LABELS = {"full-text":"完整正文", "attachments":"附件", "timeline":"项目进展"}


def validate_resource_data(kind: str, data: Any, project_id: str) -> Any:
    """Preserve API data; business success is decided by the response code."""
    return data


@api_command
def cmd_resource(args: argparse.Namespace) -> dict[str, Any]:
    snapshot, capability, resolution = announcement_context(args)
    if snapshot["result_type"] != "project":
        raise correction_error("AGENT_DETAIL_CORRECTION_REQUIRED", "该资源接口仅支持普通项目。", "使用当前数据源文档列明的能力，不要改用普通项目接口。")
    if resolution["status"] != "matched":
        return {"ok":False, "stage":args.command, "total_count":len(resolution.get("matches",[])), "returned_count":0,
                "candidates":resolution.get("matches",[]), "follow_up":follow_up_metadata(snapshot),
                "user_message":"当前结果尚未唯一定位，请提供结果序号或更具体的项目名称。"}
    project = resolution["matches"][0]
    project_id = project_id_for_request(project)
    client = build_client(args)
    path = f"/api/{RESOURCE_PATHS[args.command]}/{project_id}"
    try:
        data = validate_resource_data(args.command, client._request("GET", path), project_id)
    except SkillError as exc:
        payload = failure_payload(stage=args.command, error=exc, effective_query=snapshot["effective_query"])
        payload["follow_up"] = follow_up_metadata(snapshot)
        return maybe_attach_entitlement_diagnosis(payload, client, exc, target_right=RESOURCE_LABELS[args.command])
    save_focus_project(snapshot, project)
    count = len(data) if isinstance(data, list) else 1 if isinstance(data, dict) else None
    output = {"ok": True, "stage": args.command, "capability": args.command, "result_type": "project",
              "request_api_path": path, "selected_project_id": project_id, "warnings": [],
              "follow_up": follow_up_metadata(snapshot), "returned_count": count, "total_count": count}
    if args.command == "full-text":
        output["full_text"] = data
        if isinstance(data, dict):
            content = data.get('content')
            output["user_message"] = f"{clean_user_value(data.get('title'))}\n\n{content if isinstance(content, str) and content.strip() else clean_user_value(content)}"
            if str(data.get("projectId")) != project_id:
                output["warnings"].append("接口返回的项目编号与所选项目不同，正文按返回项目展示。")
        else:
            output["user_message"] = "正文信息：" + clean_user_value(data)
    elif args.command == "attachments":
        output["attachments"] = data
        lines = [f"{clean_user_value(project.get('title'))}的附件："]
        if isinstance(data, list):
            for index, item in enumerate(data, 1):
                if not isinstance(item, dict):
                    lines.append(f"{index}. {clean_user_value(item)}")
                    continue
                size = item.get('fileSize')
                if size is None or size == "":
                    size_text = "大小未公示"
                elif (type(size) in (int, float) and (type(size) is int or math.isfinite(size))) or (
                    isinstance(size, str) and re.fullmatch(r"[+-]?(?:\d+\.?\d*|\.\d+)", size.strip())
                ):
                    size_text = f"{clean_user_value(size)} KB"
                else:
                    size_text = None
                label = markdown_link(clean_user_value(item.get('fileName')), item.get('fileUrl'))
                lines.append(f"{index}. {label}" + (f"（{size_text}）" if size_text else ""))
                if str(item.get("projectId")) != project_id:
                    output["warnings"].append(f"第 {index} 个附件的项目编号与所选项目不同，按接口返回信息展示。")
        output["user_message"] = "\n".join(lines) if isinstance(data, list) and data else "附件信息：" + clean_user_value(data)
    else:
        output["timeline"] = data
        output.pop("follow_up", None)
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            timeline_snapshot = save_search_snapshot(session_id=snapshot.get("session_id") or search_session_id(args), result_type="project", effective_query=snapshot["effective_query"], viewed_cards=data, total_count=len(data), page_count=1, parent_result_set_id=snapshot.get("result_set_id"))
            timeline_snapshot["origin"] = "timeline"
            save_snapshot(timeline_snapshot)
            output["follow_up"] = follow_up_metadata(timeline_snapshot)
            output["user_message"] = "\n".join(f"{i}. {clean_user_value(item.get('publishTime'))} · {clean_user_value(item.get('title'))} · {format_stage_display(item.get('infoType'))}" for i, item in enumerate(data, 1)) or "项目进展信息未公示。"
        else:
            output["user_message"] = "项目进展信息：" + clean_user_value(data)
    if output["warnings"]:
        output["user_message"] += "\n\n" + "；".join(output["warnings"])
    return output


def normalize_company_query(raw: dict[str, Any]) -> dict[str, Any]:
    reject_unsupported_fields(raw, frozenset({"companyName","currentPage","pageSize"}), "公司搜索")
    name = raw.get("companyName")
    if not isinstance(name,str) or not name.strip():
        raise SkillError("INVALID_QUERY", "请提供公司名称、简称或名称片段。")
    result = {"companyName":name.strip()}
    for field,default,maximum in (("currentPage",1,None),("pageSize",10,20)):
        value = raw.get(field,default)
        if type(value) is not int or value < 1 or maximum is not None and value > maximum:
            raise SkillError("INVALID_QUERY", "公司页码从 1 开始，每页数量为 1 到 20。")
        result[field] = value
    return result


def validate_company_response(data: Any) -> dict[str, Any]:
    """Preserve API data; business success is decided by the response code."""
    return data


@api_command
def cmd_search_company(args: argparse.Namespace) -> dict[str, Any]:
    parent = None
    if args.next_page:
        session_id, parent = query_continuation_context(args, company=True)
        if args.query_json:
            raise SkillError("INVALID_QUERY", "公司翻页不能同时改变查询条件。")
        page_count = usable_count(parent.get("page_count"))
        if page_count is not None and parent["effective_query"]["currentPage"] >= page_count:
            return {"ok":True,"total_count":parent["total_count"],"returned_count":0,"rows":[],"follow_up":follow_up_metadata(parent),"user_message":"公司候选已全部展示。"}
        query = dict(parent["effective_query"])
        query["currentPage"] += 1
    else:
        if getattr(args, "context_json", None) is not None:
            raise SkillError("INVALID_QUERY", "完整续查上下文需要配合 search-company --next 使用。")
        session_id = search_session_id(args)
        query = parse_query_json(args.query_json or "{}")
    query = normalize_company_query(query)
    client = build_client(args)
    try:
        data = validate_company_response(client._request("POST","/api/searchCompany",query=query))
    except SkillError as exc:
        return maybe_attach_entitlement_diagnosis(failure_payload(stage="search-company",error=exc,effective_query=query),client,exc,target_right="公司搜索")

    maintain_query_cache()
    rows=data["list"]
    total = usable_count(data.get('total'))
    size = usable_count(data.get('pageSize'))
    reported_page = usable_count(data.get('currentPage'))
    matching_page = reported_page == query['currentPage'] and size == query['pageSize']
    page_count = math.ceil(total / size) if total is not None and size and matching_page else None
    paging_mismatch = (reported_page is not None and reported_page != query['currentPage']) or (size is not None and size != query['pageSize'])
    snapshot = None if paging_mismatch else save_search_snapshot(session_id=session_id,result_type="company_candidates",effective_query=query,viewed_cards=rows,total_count=data.get('total'),page_count=page_count,parent_result_set_id=parent['result_set_id'] if parent else None)
    message = f"找到 {clean_user_value(data.get('total'))} 家候选公司，本批 {len(rows)} 家。"
    if rows:
        message += "\n\n" + "\n".join(f"{i}. {clean_user_value(row.get('companyName'))} · {clean_user_value(row.get('registeredAddress'))} · 中标 {clean_user_value(row.get('winningCount'))} 次 / 招标 {clean_user_value(row.get('tenderingCount'))} 次" for i,row in enumerate(rows,1))
    output = {"ok":True,"capability":"search-company","result_type":"company_candidates","total_count":data['total'],"returned_count":len(rows),"rows":rows,"effective_query":query,"request_query":query,"request_api_path":"/api/searchCompany","user_message":message,"warnings":[]}
    if snapshot is not None:
        output['follow_up'] = follow_up_metadata(snapshot)
    else:
        output['agent_instruction'] = "交付本次成功的公司结果；接口返回分页与请求不一致，不能自动推断下一页。后续续查需明确已执行页码与页大小。"
    return output


def cmd_area(args: argparse.Namespace) -> dict[str, Any]:
    try:
        return area_resolver.resolve(args.name, args.limit, getattr(args, "parent", None))
    except area_resolver.AreaError as exc:
        raise SkillError("INVALID_QUERY", str(exc)) from exc


def build_client(args: argparse.Namespace) -> ApiClient:
    if getattr(args, "access_mode", "auto") == "guest" and getattr(args, "command", "search") not in {"search", "next", "refine"}:
        raise SkillError("FREE_CAPABILITY_UNAVAILABLE", "免费查询仅支持普通标讯列表；此能力需要登录并使用账号积分。")
    return ApiClient(
        base_url=args.base_url or os.environ.get("QIANLIMA_BASE_URL", DEFAULT_BASE_URL),
        api_key=os.environ.get("QIANLIMA_API_KEY"),
        mock_dir=args.mock_dir or os.environ.get("QIANLIMA_MOCK_DIR"),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Qianlima bidding skill runtime")
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--mock-dir", default=None)
    subparsers = parser.add_subparsers(dest="command", required=True)

    verify = subparsers.add_parser("verify")
    verify.set_defaults(func=cmd_verify)

    entitlement = subparsers.add_parser("entitlement")
    entitlement.set_defaults(func=cmd_entitlement)

    preflight_complex = subparsers.add_parser("preflight-complex")
    preflight_complex.add_argument("--plan-json", required=True)
    preflight_complex.add_argument("--user-text", default="")
    preflight_complex.set_defaults(func=cmd_preflight_complex)

    search = subparsers.add_parser("search")
    search.add_argument("--session-id", default=None)
    search.add_argument("--query-json", required=True)
    search.add_argument("--user-text", default="")
    search.set_defaults(func=cmd_search)

    search_purchase = subparsers.add_parser("search-purchase")
    search_purchase.add_argument("--session-id", default=None)
    search_purchase.add_argument("--query-json", required=True)
    search_purchase.add_argument("--user-text", default="")
    search_purchase.set_defaults(func=cmd_search_purchase)

    search_expiring = subparsers.add_parser("search-expiring")
    search_expiring.add_argument("--session-id", default=None)
    search_expiring.add_argument("--query-json", required=True)
    search_expiring.add_argument("--user-text", default="")
    search_expiring.set_defaults(func=cmd_search_expiring)

    next_page = subparsers.add_parser("next")
    next_page.add_argument("--session-id", default=None)
    next_page.add_argument("--result-set-id", default=None)
    next_page.add_argument("--context-json", default=None)
    next_page.set_defaults(func=cmd_next)

    refine = subparsers.add_parser("refine")
    refine.add_argument("--session-id", default=None)
    refine.add_argument("--result-set-id", default=None)
    refine.add_argument("--context-json", default=None)
    refine.add_argument("--query-json", required=True)
    refine.add_argument("--user-text", default="")
    refine.set_defaults(func=cmd_refine)

    detail = subparsers.add_parser("detail")
    detail.add_argument("--session-id", default=None)
    detail.add_argument("--result-set-id", default=None)
    detail.add_argument("--project-ref", default=None)
    detail.add_argument("--id", default=None)
    detail.add_argument("--result-type", default=None, choices=["project", "purchase_intention", "expiring_project"])
    detail.add_argument("--fields", default=None)
    detail.add_argument("--source-url", action="store_true")
    detail.set_defaults(func=cmd_detail)

    for command in RESOURCE_PATHS:
        resource = subparsers.add_parser(command)
        resource.add_argument("--session-id", default=None)
        resource.add_argument("--result-set-id", default=None)
        resource.add_argument("--project-ref", default=None)
        resource.add_argument("--id", default=None)
        resource.set_defaults(func=cmd_resource)
    company = subparsers.add_parser("search-company")
    company.add_argument("--query-json", default=None)
    company.add_argument("--session-id", default=None)
    company.add_argument("--result-set-id", default=None)
    company.add_argument("--context-json", default=None)
    company.add_argument("--next", dest="next_page", action="store_true")
    company.set_defaults(func=cmd_search_company)

    area = subparsers.add_parser("area")
    area.add_argument("--name", required=True)
    area.add_argument("--limit", type=int, default=5)
    area.add_argument("--parent", default=None, help="用户已明确的上级地区，用于消歧；不改变目标范围")
    area.set_defaults(func=cmd_area)

    enterprise = subparsers.add_parser("enterprise")
    enterprise.add_argument("--kind", required=True, choices=[
        "partners",
        "area-distribution",
        "principals",
        "winning-area-distribution",
        "co-bidder-competitors",
        "potential-competitors",
        "business-info",
        "contacts",
    ])
    enterprise.add_argument("--query-json", required=True)
    enterprise.set_defaults(func=cmd_enterprise)

    for subparser in subparsers.choices.values():
        subparser.add_argument("--access-mode", choices=ACCESS_MODES, default="auto")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        emit(args.func(args))
        return 0
    except SkillError as exc:
        display_message = public_error_summary(exc, args.command)
        payload = {
            "ok": False,
            "error_code": exc.code,
            "message": display_message,
            "total_count": 0,
            "returned_count": 0,
            "effective_query": {},
            "warnings": [display_message],
        }
        if exc.code in STATE_ERROR_CODES:
            payload["retry_policy"] = STATE_RETRY_POLICY
            payload["requires_user_confirmation"] = False
            payload["needs_clarification"] = True
            missing_context = "请补充要读取的公告指代或已知公告编号。" if args.command in {"detail", *RESOURCE_PATHS} else "请补充原查询条件与已执行页码。"
            payload["user_message"] = exc.message + missing_context
            payload["agent_instruction"] = "先检查对话中已明确的公告编号或完整查询条件与页码；可恢复时直接使用 --id 或 --context-json，不要求用户确认重搜。只有必要信息确实缺失时才澄清，不猜对象、条件或页码。"
        elif exc.code == "FOLLOW_UP_UNAVAILABLE":
            payload["user_message"] = exc.message
            payload["needs_clarification"] = True
            payload["requires_user_confirmation"] = False
            if isinstance(exc.data, dict):
                payload.update(exc.data)
            payload["agent_instruction"] = "先使用对话中已明确的必要内容补全上下文；只澄清实际缺失的信息，不默认重搜，不猜条件或页码。"
        elif exc.code == "TIME_SPAN_EXCEEDED":
            payload["cards"] = []
            payload["user_message"] = display_message
        elif is_account_access_error(exc):
            payload["user_message"] = permission_user_message(exc, args.command)
        elif exc.code in AGENT_CORRECTION_ERROR_CODES:
            if isinstance(exc.data, dict):
                payload.update(exc.data)
            payload.setdefault("requires_agent_correction", True)
            payload.setdefault("requires_user_confirmation", False)
            payload["user_message"] = "查询参数需要由 Agent 按接口契约修正后重试，本次未调用查询接口。"
        elif exc.code in {"INVALID_JSON", "INVALID_FIELDS", "HTTP_ERROR", "NETWORK_ERROR"}:
            payload["user_message"] = generic_user_message(exc, args.command)
        elif getattr(args, "context_json", None) is not None:
            payload["user_message"] = exc.message
        elif args.command == "next":
            payload["cards"] = []
            if display_message.startswith("当前"):
                payload["user_message"] = display_message
            else:
                payload["user_message"] = "还没有可继续展示的结果。请您先查一批项目。"
        elif args.command == "refine":
            payload["cards"] = []
            if display_message.startswith("当前"):
                payload["user_message"] = display_message
            else:
                payload["user_message"] = "还没有可调整的当前查询。请您先查一批项目。"
        elif args.command == "detail":
            if display_message.startswith("当前"):
                payload["user_message"] = display_message
            else:
                payload["user_message"] = "当前没有可追问的项目结果。请您先查一批项目，再用第几条或标题关键词追问。"
        elif args.command in {"search-purchase", "search-expiring", "enterprise"}:
            payload["user_message"] = "这次查询没有成功，我没有自动改用其他网站或模型记忆补结果。"
        else:
            payload["user_message"] = generic_user_message(exc, args.command)
        emit(payload)
        return 2
    except Exception:
        fallback = SkillError("UNEXPECTED_ERROR", GENERAL_FAILURE_SUMMARY)
        payload = {
            "ok": False,
            "error_code": fallback.code,
            "message": public_error_summary(fallback, args.command),
            "total_count": 0,
            "returned_count": 0,
            "effective_query": {},
            "warnings": [public_error_summary(fallback, args.command)],
            "user_message": generic_user_message(fallback, args.command),
        }
        emit(payload)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
