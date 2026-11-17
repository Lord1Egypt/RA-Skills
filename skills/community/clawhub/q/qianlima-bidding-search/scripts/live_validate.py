#!/usr/bin/env python3
"""Run live validation cases for the Qianlima bidding skill.

This script intentionally does not accept an API key as an argument. Provide
QIANLIMA_API_KEY through the environment or current-session secret injection.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import area_resolver


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "scripts" / "qianlima_skill.py"
DEFAULT_CASES = ROOT / "tests" / "live_validation_cases.json"
AREA_FILE = ROOT / "references" / "area.json"
RESULT_CARD_FIELDS = {
    "project": {"id", "title", "purchasingUnit", "areaName", "infoType", "budgetAmount", "biddingAmount", "publishTime", "url"},
    "purchase_intention": {"id", "title", "publishTime", "budgetAmount", "planPurchaseDate", "purchasingUnit", "areaName", "url"},
    "expiring_project": {
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
    },
}
SEARCH_KEYS = {"total_count", "returned_count", "effective_query", "warnings", "cards"}
INTERNAL_WORDS = ["total_count", "returned_count", "warnings", "effective_query", "sourceUrl", "areaIds", "infoTypes", "request_query"]
SEARCH_CASE_COMMANDS = {
    "search": "search",
    "purchase_intention": "search-purchase",
    "expiring_project": "search-expiring",
}


SCENARIO_CATEGORY_NAMES = {
    "normal": "正常业务场景",
    "exception": "异常场景",
    "boundary": "边界场景",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def is_safe_follow_up_failure(payload: dict[str, Any]) -> bool:
    """Accept unresolved follow-ups only when no API request was made."""
    if payload.get("ok") or payload.get("api_responses"):
        return False
    resolution = payload.get("resolution")
    if isinstance(resolution, dict) and resolution.get("status") in {"ambiguous", "not_found"}:
        return True
    return (
        payload.get("retry_policy") == "restore_explicit_context_or_clarify_missing_fields"
        and payload.get("needs_clarification") is True
    )


def shift_dates_to_today(cases_payload: dict[str, Any]) -> dict[str, Any]:
    base_date = cases_payload.get("current_date")
    if not base_date:
        return cases_payload
    try:
        source_date = dt.date.fromisoformat(str(base_date))
    except ValueError:
        return cases_payload
    target_date = dt.date.today()
    delta = target_date - source_date
    month_delta = (target_date.year - source_date.year) * 12 + target_date.month - source_date.month
    if not delta.days:
        return cases_payload
    shifted = json.loads(json.dumps(cases_payload))
    shifted["current_date"] = target_date.isoformat()

    def shift_query_dates(query: dict[str, Any]) -> None:
        for key in ("beginTime", "endTime", "beginServiceExpireTime", "endServiceExpireTime"):
            value = query.get(key)
            if not isinstance(value, str):
                continue
            try:
                if len(value) == 19 and key in {"beginTime", "endTime"}:
                    query[key] = (dt.datetime.strptime(value, "%Y-%m-%d %H:%M:%S") + delta).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    query[key] = (dt.date.fromisoformat(value) + delta).isoformat()
            except ValueError:
                continue
        for key in ("startPlanPurchaseDate", "endPlanPurchaseDate"):
            value = query.get(key)
            if not isinstance(value, str):
                continue
            try:
                source_month = dt.datetime.strptime(value, "%Y-%m")
            except ValueError:
                continue
            month_index = source_month.year * 12 + source_month.month - 1 + month_delta
            query[key] = f"{month_index // 12:04d}-{month_index % 12 + 1:02d}"

    for case in shifted.get("cases") or []:
        if isinstance(case.get("expected_query"), dict):
            shift_query_dates(case["expected_query"])
        if isinstance(case.get("failed_query"), dict):
            shift_query_dates(case["failed_query"])
    return shifted


def generated_zero_result_query(case: dict[str, Any]) -> dict[str, Any]:
    if case.get("id") == "zero_28_too_narrow":
        current = dt.date.today()
        return {
            "keywordGroups": [{"keywords":["5G基站"],"matchScopes":[2,8]}],
            "excludeWords": ["监理"],
            "beginTime": (current - dt.timedelta(days=6)).isoformat(),
            "endTime": current.isoformat(),
            "beginAmount": 3000000,
            "infoTypes": {"0": [4]},
            "numPerPage": 10,
        }
    return {"numPerPage": 10}


def run_skill(args: list[str], env: dict[str, str]) -> tuple[int, dict[str, Any]]:
    proc = subprocess.run(
        [sys.executable, str(RUNTIME), *args],
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        payload = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        payload = {
            "ok": False,
            "message": "工具返回内容不是有效 JSON。",
            "stdout": proc.stdout[:500],
            "stderr": proc.stderr[:500],
        }
    return proc.returncode, payload


def area_names_for_query(query: dict[str, Any]) -> list[str]:
    if query.get("areaNames"):
        return list(dict.fromkeys(str(value) for value in query["areaNames"] if str(value).strip()))
    directory = area_resolver.catalog()
    ids = directory.validate_ids(query.get("areaIds") or [])
    return list(dict.fromkeys(directory.display_path(i) for i in ids))


def amount_wan(value: Any) -> str:
    try:
        return f"{float(value) / 10000:.2f} 万元"
    except (TypeError, ValueError):
        return str(value)


MATCH_SCOPE_LABELS = {1: "标题+正文+附件", 2: "标题", 3: "项目编号", 4: "采购单位", 5: "中标单位", 6: "代理机构", 7: "联系人", 8: "正文", 9: "标的物", 10: "附件"}


def keyword_summary(query: dict[str, Any]) -> str:
    if query.get("keywordGroups"):
        return " AND ".join(
            "(" + " OR ".join(group["keywords"]) + ")@" + "+".join(MATCH_SCOPE_LABELS.get(scope, str(scope)) for scope in group["matchScopes"])
            for group in query["keywordGroups"]
        )
    words = query.get("keywords") or []
    separator = " AND " if query.get("keywordsSearchType") == 2 else " OR "
    return separator.join(words)


def visible_keyword_match(query: dict[str, Any], card: dict[str, Any]) -> bool | None:
    """True/False only with visible evidence; None means hidden scopes matter."""
    groups = query.get("keywordGroups")
    if groups is None:
        words = query.get("keywords") or []
        scopes = query.get("matchScopes") or [2, 8]
        groups = ([{"keywords": [word], "matchScopes": scopes} for word in words]
                  if query.get("keywordsSearchType") == 2 else [{"keywords": words, "matchScopes": scopes}])
    scope_fields = {2: "title", 4: "purchasingUnit", 5: "winningBidderUnit"}
    results = []
    for group in groups:
        words = group.get("keywords") or []
        if not words:
            continue
        visible = []
        hidden = False
        for scope in group["matchScopes"]:
            field = scope_fields.get(scope)
            if scope == 1:
                visible.append(str(card.get("title") or ""))
                hidden = True
            elif field is not None and field in card and card[field] is not None:
                visible.append(str(card[field]))
            else:
                hidden = True
        if any(word in text for word in words for text in visible):
            results.append(True)
        else:
            results.append(None if hidden else False)
    if False in results:
        return False
    return None if None in results else True


def structured_filter_summary(query: dict[str, Any]) -> list[str]:
    parts = []
    for key, label in (("procurementCategories", "采购分类"), ("procurementMethods", "采购方式"), ("fundsSources", "资金来源")):
        if key in query:
            parts.append(label + "：" + "、".join(map(str, query[key])))
    for key, labels in {
        "hasAnnex": ("无附件", "有附件"), "hasAgency": ("无代理机构", "有代理机构"),
        "registrationStatus": ("报名未结束", "报名已结束"),
        "hasBiddingPhone": ("无招标电话", "有招标电话"), "hasWinningPhone": ("无中标电话", "有中标电话"),
    }.items():
        if key in query and query[key] in (0, 1):
            parts.append(labels[int(query[key])])
    return parts


def compact_query(query: dict[str, Any]) -> str:
    parts: list[str] = []
    if query.get("companyName"):
        parts.append("企业：" + str(query["companyName"]))
    if keyword_summary(query):
        parts.append("关键词：" + keyword_summary(query))
    parts.extend(structured_filter_summary(query))
    if query.get("excludeWords"):
        parts.append("排除：" + "、".join(query["excludeWords"]))
    area_names = area_names_for_query(query)
    if area_names:
        parts.append("地区：" + "、".join(area_names))
    if query.get("beginTime") or query.get("endTime"):
        parts.append(f"时间：{query.get('beginTime', '不限')} 至 {query.get('endTime', '不限')}")
    if query.get("startPlanPurchaseDate") or query.get("endPlanPurchaseDate"):
        parts.append(
            f"预计采购时间：{query.get('startPlanPurchaseDate', '不限')} 至 {query.get('endPlanPurchaseDate', '不限')}"
        )
    if query.get("beginServiceExpireTime") or query.get("endServiceExpireTime"):
        parts.append(
            f"服务到期时间：{query.get('beginServiceExpireTime', '不限')} 至 {query.get('endServiceExpireTime', '不限')}"
        )
    if query.get("beginAmount") is not None and query.get("endAmount") is not None:
        parts.append(f"金额：{amount_wan(query['beginAmount'])}至 {amount_wan(query['endAmount'])}")
    elif query.get("beginAmount") is not None:
        parts.append(f"金额：{amount_wan(query['beginAmount'])}以上")
    elif query.get("endAmount") is not None:
        parts.append(f"金额：{amount_wan(query['endAmount'])}以下")
    if query.get("startPlanPurchaseAmount") is not None or query.get("endPlanPurchaseAmount") is not None:
        parts.append(
            "预计采购金额："
            f"{amount_wan(query['startPlanPurchaseAmount']) if query.get('startPlanPurchaseAmount') is not None else '不限'}"
            " 至 "
            f"{amount_wan(query['endPlanPurchaseAmount']) if query.get('endPlanPurchaseAmount') is not None else '不限'}"
        )
    if query.get("beginContractAmount") is not None or query.get("endContractAmount") is not None:
        parts.append(
            "合同金额："
            f"{amount_wan(query['beginContractAmount']) if query.get('beginContractAmount') is not None else '不限'}"
            " 至 "
            f"{amount_wan(query['endContractAmount']) if query.get('endContractAmount') is not None else '不限'}"
        )
    return "；".join(parts) if parts else "未设置额外筛选条件"


def normalized_expected_query(query: dict[str, Any], case_type: str = "search") -> dict[str, Any]:
    # Request echoes contain normalized timestamps and API defaults. Use the
    # same pure normalizers; this does not create a client or call an API.
    if str(ROOT / "scripts") not in sys.path:
        sys.path.insert(0, str(ROOT / "scripts"))
    from qianlima_skill import normalize_project_search_query, normalize_purchase_search_query, normalize_expiring_search_query
    normalizer = {
        "search": normalize_project_search_query,
        "purchase_intention": normalize_purchase_search_query,
        "search-purchase": normalize_purchase_search_query,
        "expiring_project": normalize_expiring_search_query,
        "search-expiring": normalize_expiring_search_query,
    }.get(case_type)
    return normalizer(query)[0] if normalizer else json.loads(json.dumps(query))


def request_query(payload: dict[str, Any]) -> dict[str, Any]:
    query = payload.get("request_query")
    if isinstance(query, dict):
        return query
    query = payload.get("effective_query")
    return query if isinstance(query, dict) else {}


def request_matches_expected(case: dict[str, Any], payload: dict[str, Any]) -> tuple[bool, str]:
    expected = normalized_expected_query(case["expected_query"], str(case.get("type") or "search"))
    sent = request_query(payload)
    if not sent:
        return False, "未发起搜索请求。"
    labels = {
        "keywords": "关键词",
        "keywordsSearchType": "关键词关系",
        "keywordGroups": "关键词组及独立位置",
        "procurementCategories": "采购分类",
        "procurementMethods": "采购方式",
        "fundsSources": "资金来源",
        "hasAnnex": "附件要求",
        "excludeWords": "排除词",
        "areaIds": "地区",
        "beginTime": "开始时间",
        "endTime": "结束时间",
        "purchasingUnitTypes": "采购单位类型",
        "infoTypes": "信息类型",
        "beginAmount": "金额下限",
        "endAmount": "金额上限",
        "startPlanPurchaseDate": "预计采购开始月份",
        "endPlanPurchaseDate": "预计采购结束月份",
        "startPlanPurchaseAmount": "预计采购金额下限",
        "endPlanPurchaseAmount": "预计采购金额上限",
        "beginServiceExpireTime": "服务到期开始日期",
        "endServiceExpireTime": "服务到期结束日期",
        "beginContractAmount": "合同金额下限",
        "endContractAmount": "合同金额上限",
        "companyName": "企业名称",
        "currentPage": "页码",
        "numPerPage": "每页数量",
    }
    mismatches: list[str] = [labels.get(key, key) for key in sorted(set(sent) - set(expected))]
    for key, expected_value in expected.items():
        actual_value = sent.get(key)
        if key == "areaIds":
            try:
                matches = {int(value) for value in actual_value or []} == {int(value) for value in expected_value or []}
            except (TypeError, ValueError):
                matches = False
        else:
            matches = actual_value == expected_value
        if not matches:
            mismatches.append(labels.get(key, key))
    if mismatches:
        return False, f"实际请求条件与系统理解不一致，涉及：{', '.join(mismatches)}。实际请求：{compact_query(sent)}"
    return True, f"实际请求与系统理解一致：{compact_query(sent)}"


def search_case_args(case: dict[str, Any]) -> list[str]:
    command = SEARCH_CASE_COMMANDS.get(str(case.get("type") or ""))
    if not command:
        raise ValueError(f"不支持的搜索验收类型：{case.get('type')}")
    return [command, "--query-json", json.dumps(case["expected_query"], ensure_ascii=False)]


def enterprise_case_args(case: dict[str, Any]) -> list[str]:
    return [
        "enterprise",
        "--kind",
        str(case["enterprise_kind"]),
        "--query-json",
        json.dumps(case["expected_query"], ensure_ascii=False),
    ]


def route_matches_expected(
    case: dict[str, Any],
    *,
    actual_command: str,
    payload: dict[str, Any],
) -> tuple[bool, str]:
    checks = [
        ("命令", case.get("expected_command"), actual_command),
        ("能力", case.get("expected_capability"), payload.get("capability")),
        ("接口路径", case.get("expected_api_path"), payload.get("request_api_path")),
        ("结果类型", case.get("expected_result_type"), payload.get("result_type")),
    ]
    mismatches = [f"{label}期望 {expected}，实际 {actual}" for label, expected, actual in checks if expected != actual]
    if mismatches:
        return False, "路由不一致：" + "；".join(mismatches) + "。"
    return True, (
        f"路由一致：{actual_command} → {payload.get('capability')} → "
        f"{payload.get('request_api_path')} → {payload.get('result_type')}。"
    )


def search_count_note(payload: dict[str, Any]) -> str:
    api_total = int(payload.get("api_total_count", payload.get("total_count", 0)) or 0)
    api_returned = int(payload.get("api_returned_count", len(payload.get("cards") or [])) or 0)
    displayed = int(payload.get("returned_count", 0) or 0)
    return f"接口总数 {api_total} 条，接口本页返回 {api_returned} 条，Skill 展示 {displayed} 条。"


def result_consistency_check(payload: dict[str, Any]) -> tuple[bool, str]:
    api_returned = int(payload.get("api_returned_count", len(payload.get("cards") or [])) or 0)
    displayed = int(payload.get("returned_count", 0) or 0)
    if api_returned != displayed:
        return False, "未通过：Skill 展示数量与接口本页返回数量不一致。"
    return True, "通过：Skill 不拦截后端返回结果，本页项目已按接口返回原样展示。"


def recall_count_check(payload: dict[str, Any]) -> tuple[bool, str]:
    api_returned = int(payload.get("api_returned_count", len(payload.get("cards") or [])) or 0)
    displayed = int(payload.get("returned_count", 0) or 0)
    if api_returned != displayed:
        return False, search_count_note(payload)
    return True, search_count_note(payload)


def user_message_is_chinese_safe(payload: dict[str, Any]) -> bool:
    message = payload.get("user_message") or ""
    return bool(message) and not any(word in message for word in INTERNAL_WORDS)


def user_message_includes_returned_results(message: str, cards: list[dict[str, Any]]) -> bool:
    if not cards:
        return True
    titles = [str(card.get("title") or "").strip() for card in cards]
    return all(title and title in message for title in titles)


def search_passed(
    payload: dict[str, Any],
    case: dict[str, Any] | None = None,
    actual_command: str = "",
) -> bool:
    cards = payload.get("cards") or []
    message = payload.get("user_message") or ""
    returned_count = int(payload.get("returned_count", 0) or 0)
    warning_text = "；".join(payload.get("warnings") or [])
    request_ok = True
    route_ok = True
    if case is not None:
        request_ok, _ = request_matches_expected(case, payload)
        route_ok, _ = route_matches_expected(case, actual_command=actual_command, payload=payload)
    consistency_ok, _ = result_consistency_check(payload)
    recall_ok, _ = recall_count_check(payload)
    card_fields = RESULT_CARD_FIELDS.get(str(payload.get("result_type") or ""), RESULT_CARD_FIELDS["project"])
    return (
        bool(payload.get("ok"))
        and request_ok
        and route_ok
        and consistency_ok
        and recall_ok
        and SEARCH_KEYS.issubset(payload)
        and bool(card_fields)
        and all(card_fields.issubset(card) for card in cards)
        and returned_count == len(cards)
        and user_message_includes_returned_results(message, cards)
        and user_message_is_chinese_safe(payload)
    )


def print_case_header(index: int, text: str) -> None:
    print(f"\n{index}. 用户说：{text}")


def print_user_message(message: str, indent: str = "   ") -> None:
    for line in message.splitlines():
        print(indent + line)


def scenario_category(case: dict[str, Any]) -> str:
    if case.get("category"):
        return str(case["category"])
    case_type = case["type"]
    if case_type in {"ambiguous_area", "next_no_current", "next_after_failed_search", "detail_failure", "detail_no_current", "detail_safe"}:
        return "exception"
    if case_type in {"zero_result_reflection"}:
        return "boundary"
    if case["id"] in {
        "search_04_tianhe_gov_intention",
        "search_06_xihu_imaging_preview",
        "search_12_huadong_hospital_device",
        "search_13_gba_school_air",
    }:
        return "boundary"
    return "normal"


def case_label(case: dict[str, Any]) -> str:
    return SCENARIO_CATEGORY_NAMES.get(scenario_category(case), "正常业务场景")


def report_message(payload: dict[str, Any], fallback: str) -> str:
    message = payload.get("user_message")
    if message:
        return str(message)
    if payload.get("message"):
        return str(payload["message"])
    return fallback


def append_report_entry(
    entries: list[dict[str, Any]],
    *,
    case: dict[str, Any],
    interface_call: str,
    ok: bool,
    user_message: str,
    note: str = "",
    intent_check: str = "",
    request_check: str = "",
    result_check: str = "",
    recall_check: str = "",
    route_check: str = "",
) -> None:
    entries.append(
        {
            "category": case_label(case),
            "natural_language": case["natural_language"],
            "understanding": case["understanding"],
            "interface_call": interface_call,
            "ok": ok,
            "user_message": user_message,
            "note": note,
            "intent_check": intent_check,
            "request_check": request_check,
            "result_check": result_check,
            "recall_check": recall_check,
            "route_check": route_check,
        }
    )


def write_report(
    path: Path,
    *,
    cases_payload: dict[str, Any],
    entries: list[dict[str, Any]],
    passed: int,
    total: int,
    quota: dict[str, int | str] | None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 千里马 Skill 真实验收报告",
        "",
        f"- 样例日期基准：{cases_payload.get('current_date', '')}",
        "- 密钥处理：仅从当前会话环境读取，未写入报告。",
        "- 验收边界：本脚本核对已配置命令、实际能力、API 路径和结果类型；宿主 Agent 自主路由未验证。",
        "- 复杂查询完成率需使用答案隔离的三轮 Host Agent 新旧对照证明；本脚本只验证运行时契约，不能替代该证据。",
        f"- 验收结果：通过 {passed} / {total}",
    ]
    if quota:
        lines.append("- 本地额度计数：" + "；".join(f"{key}：{value}" for key, value in quota.items()))
    lines.append("")
    for index, entry in enumerate(entries, start=1):
        lines.extend(
            [
                f"## 用例 {index}：{entry['category']}",
                "",
                f"- 用户原话：{entry['natural_language']}",
                f"- 系统理解：{entry['understanding']}",
                f"- 接口调用：{entry['interface_call']}",
                f"- 验收结果：{'通过' if entry['ok'] else '未通过'}",
            ]
        )
        if entry.get("note"):
            lines.append(f"- 说明：{entry['note']}")
        if entry.get("intent_check"):
            lines.append(f"- 意图解析：{entry['intent_check']}")
        if entry.get("route_check"):
            lines.append(f"- 能力路由：{entry['route_check']}")
        if entry.get("request_check"):
            lines.append(f"- 实际传参：{entry['request_check']}")
        if entry.get("result_check"):
            lines.append(f"- 结果一致性：{entry['result_check']}")
        if entry.get("recall_check"):
            lines.append(f"- 召回数量：{entry['recall_check']}")
        lines.extend(["", "用户实际看到的数据：", "", "```markdown", entry["user_message"], "```", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def summarize_search(case: dict[str, Any], code: int, payload: dict[str, Any], actual_command: str) -> dict[str, Any]:
    request_ok, request_note = request_matches_expected(case, payload)
    route_ok, route_note = route_matches_expected(case, actual_command=actual_command, payload=payload)
    consistency_ok, consistency_note = result_consistency_check(payload)
    recall_ok, recall_note = recall_count_check(payload)
    ok = search_passed(payload, case, actual_command)
    print(f"   理解：{case['understanding']}")
    print(f"   查询条件：{compact_query(case['expected_query'])}")
    print(f"   请求检查：{request_note}")
    print(f"   路由检查：{route_note}")
    print(f"   结果一致性：{consistency_note}")
    print(f"   召回数量：{recall_note}")
    if payload.get("user_message"):
        print("   用户会看到：")
        print_user_message(payload["user_message"], "     ")
    elif payload.get("ok"):
        print(f"   结果：共找到 {payload.get('total_count', 0)} 条，本次展示 {payload.get('returned_count', 0)} 条。")
    else:
        print(f"   结果：查询未成功。{payload.get('message', '')}")
        print("   处理：没有使用其他网站或搜索引擎补结果。")
    print(f"   验收：{'通过' if ok else '未通过'}")
    return {
        "id": case["id"],
        "ok": ok,
        "returncode": code,
        "total_count": payload.get("total_count", 0),
        "returned_count": payload.get("returned_count", 0),
        "payload_ok": payload.get("ok"),
        "error_code": payload.get("error_code"),
        "message": payload.get("message"),
        "request_ok": request_ok,
        "request_note": request_note,
        "route_ok": route_ok,
        "route_note": route_note,
        "intent_note": f"已按用户原话理解为：{case['understanding']}",
        "consistency_ok": consistency_ok,
        "consistency_note": consistency_note,
        "recall_ok": recall_ok,
        "recall_note": recall_note,
    }


def follow_up_args(payload: dict[str, Any]) -> list[str]:
    follow_up = payload.get("follow_up") or {}
    return [
        "--session-id",
        str(follow_up.get("session_id") or ""),
        "--result-set-id",
        str(follow_up.get("result_set_id") or ""),
    ]


def snapshot_payload(state_dir: Path, payload: dict[str, Any]) -> dict[str, Any]:
    follow_up = payload.get("follow_up") or {}
    path = state_dir / str(follow_up.get("session_id") or "") / f"{follow_up.get('result_set_id')}.json"
    return load_json(path) if path.exists() else {}


def main() -> int:
    parser = argparse.ArgumentParser(description="千里马 Skill 线上验收脚本")
    parser.add_argument("--cases", default=str(DEFAULT_CASES))
    parser.add_argument("--state", default="", help="结果快照目录")
    parser.add_argument("--report-md", default="", help="输出 Markdown 验收报告路径")
    parser.add_argument("--skip-source-url", action="store_true", help="跳过原文链接验证，减少月度额度消耗")
    parser.add_argument("--use-today", action="store_true", help="将样例中的相对日期平移到今天，适合真实线上验收")
    args = parser.parse_args()

    if not os.environ.get("QIANLIMA_API_KEY"):
        print("未检测到接口密钥。请先在当前会话环境中配置 QIANLIMA_API_KEY。")
        return 2

    state_path = Path(args.state) if args.state else Path(tempfile.gettempdir()) / "qianlima_skill_live_validation_state"
    env = os.environ.copy()
    env["QIANLIMA_SKILL_STATE_DIR"] = str(state_path)
    env.pop("QIANLIMA_SKILL_STATE", None)

    cases_payload = load_json(Path(args.cases))
    if args.use_today:
        cases_payload = shift_dates_to_today(cases_payload)
    cases = cases_payload["cases"]

    print("千里马 Skill 白话混合查询线上验证")
    print(f"样例日期基准：{cases_payload.get('current_date')}")
    print("密钥处理：已从当前会话环境读取，不会打印或写入报告。")
    print("验收边界：核对已配置命令、实际能力、API 路径和结果类型；宿主 Agent 自主路由未验证。")
    print("复杂查询完成率需使用答案隔离的三轮 Host Agent 新旧对照证明；本脚本只验证运行时契约，不能替代该证据。")

    code, verify = run_skill(["verify"], env)
    if not verify.get("ok"):
        print("认证未通过，已停止。")
        print(f"原因：{verify.get('message', '未知错误')}")
        return 1
    print("认证：通过。")

    code, entitlement = run_skill(["entitlement"], env)
    if code != 0 or not entitlement.get("ok") or type(entitlement.get("availablePoints")) is not int:
        print("权益查询未通过，已停止。")
        print(f"原因：{entitlement.get('message', '权益数据结构不完整')}")
        return 1
    print("权益：通过。")

    results: list[dict[str, Any]] = []
    report_entries: list[dict[str, Any]] = []
    first_success: dict[str, Any] | None = None
    first_success_case: dict[str, Any] | None = None
    pageable_success: dict[str, Any] | None = None
    pageable_success_case: dict[str, Any] | None = None
    detail_success: dict[str, Any] | None = None
    detail_success_case: dict[str, Any] | None = None
    property_success: dict[str, Any] | None = None
    property_success_case: dict[str, Any] | None = None
    search_payloads: dict[str, dict[str, Any]] = {}

    search_cases = [case for case in cases if case["type"] in SEARCH_CASE_COMMANDS]
    for index, case in enumerate(search_cases, start=1):
        print_case_header(index, case["natural_language"])
        command = search_case_args(case)
        actual_command = command[0]
        code, payload = run_skill(
            [*command, "--user-text", case["natural_language"]],
            env,
        )
        result = summarize_search(case, code, payload, actual_command)
        results.append(result)
        if result["ok"]:
            search_payloads[case["id"]] = payload
        append_report_entry(
            report_entries,
            case=case,
            interface_call=f"{actual_command} → {payload.get('request_api_path') or case['expected_api_path']}",
            ok=bool(result["ok"]),
            user_message=report_message(payload, f"查询未成功。{payload.get('message', '')}"),
            intent_check=result.get("intent_note", ""),
            request_check=result.get("request_note", ""),
            result_check=result.get("consistency_note", ""),
            recall_check=result.get("recall_note", ""),
            route_check=result.get("route_note", ""),
        )
        if result["ok"] and payload.get("returned_count", 0) > 0 and first_success is None:
            first_success = payload
            first_success_case = case
        if (
            result["ok"]
            and payload.get("returned_count", 0) > 0
            and int(payload.get("total_count", 0) or 0) > int(payload.get("returned_count", 0) or 0)
            and pageable_success is None
        ):
            pageable_success = payload
            pageable_success_case = case
        if result["ok"] and payload.get("returned_count", 0) >= 2 and detail_success is None:
            detail_success = payload
            detail_success_case = case
        if case["id"] == "search_01_chaoyang_property" and result["ok"] and payload.get("returned_count", 0) > 0:
            property_success = payload
            property_success_case = case

    enterprise_cases = [case for case in cases if case["type"] == "enterprise"]
    for case in enterprise_cases:
        print_case_header(len(results) + 1, case["natural_language"])
        command = enterprise_case_args(case)
        code, payload = run_skill(command, env)
        request_ok, request_note = request_matches_expected(case, payload)
        route_ok, route_note = route_matches_expected(case, actual_command=command[0], payload=payload)
        rows = payload.get("rows") or []
        ok = (
            bool(payload.get("ok"))
            and request_ok
            and route_ok
            and isinstance(rows, list)
            and int(payload.get("returned_count", 0) or 0) == len(rows)
            and user_message_is_chinese_safe(payload)
        )
        print(f"   理解：{case['understanding']}")
        print(f"   请求检查：{request_note}")
        print(f"   路由检查：{route_note}")
        if payload.get("user_message"):
            print("   用户会看到：")
            print_user_message(payload["user_message"], "     ")
        print(f"   验收：{'通过' if ok else '未通过'}")
        results.append({"id": case["id"], "ok": ok, "returncode": code})
        append_report_entry(
            report_entries,
            case=case,
            interface_call=f"enterprise --kind {case['enterprise_kind']} → {payload.get('request_api_path') or case['expected_api_path']}",
            ok=ok,
            user_message=report_message(payload, "企业情报查询未成功。"),
            request_check=request_note,
            route_check=route_note,
        )

    ambiguous_cases = [case for case in cases if case["type"] == "ambiguous_area"]
    for case in ambiguous_cases:
        print_case_header(len(results) + 1, case["natural_language"])
        code, payload = run_skill(["area", "--name", case["area_phrase"], "--limit", "10"], env)
        candidates = payload.get("candidates") or []
        ok = (bool(payload.get("ok"))
               and payload.get("resolution_status") in {"ambiguous", "unmapped"}
               and "effective_query" not in payload)
        print(f"   理解：{case['understanding']}")
        print(f"   结果：返回 {len(candidates)} 个候选地区，{'未发起搜索' if ok else '需要检查'}。")
        if payload.get("user_message"):
            print("   提醒：" + payload["user_message"].replace("\n", " / "))
        print(f"   验收：{'通过' if ok else '未通过'}")
        results.append({"id": case["id"], "ok": ok, "returncode": code})
        append_report_entry(
            report_entries,
            case=case,
            interface_call="地区候选接口；未调用搜索接口",
            ok=ok,
            user_message=report_message(payload, "地区存在歧义，请先确认地区。"),
        )

    zero_reflection_cases = [case for case in cases if case["type"] == "zero_result_reflection"]
    if zero_reflection_cases:
        print("\n零结果反思验证")
    for case in zero_reflection_cases:
        print_case_header(len(results) + 1, case["natural_language"])
        query = generated_zero_result_query(case)
        code, payload = run_skill(
            ["search", "--query-json", json.dumps(query, ensure_ascii=False), "--user-text", case["natural_language"]],
            env,
        )
        reflections = payload.get("zero_result_reflection") or []
        ok = bool(payload.get("ok")) and int(payload.get("returned_count", 0) or 0) == int(payload.get("api_returned_count", 0) or 0)
        if int(payload.get("total_count", 0) or 0) == 0:
            ok = ok and bool(reflections) and len(reflections) <= 3
            result_note = "通过：0 结果时已基于实际参数给出放宽建议。"
        else:
            result_note = "接口返回了项目，未触发 0 结果反思；数量一致性仍已验证。"
        request_note = f"实际请求：{compact_query(request_query(payload))}"
        recall_note = recall_count_check(payload)[1]
        print(f"   理解：{case['understanding']}")
        print(f"   实际传参：{request_note}")
        if payload.get("user_message"):
            print("   用户会看到：")
            print_user_message(payload["user_message"], "     ")
        print(f"   结果检查：{result_note}")
        if recall_note:
            print(f"   召回数量：{recall_note}")
        print(f"   验收：{'通过' if ok else '未通过'}")
        results.append({"id": case["id"], "ok": ok, "returncode": code})
        append_report_entry(
            report_entries,
            case=case,
            interface_call="搜索接口",
            ok=ok,
            user_message=report_message(payload, "请补充更明确的查询条件后再查。"),
            request_check=request_note,
            result_check=result_note,
            recall_check=recall_note,
        )

    if pageable_success and pageable_success_case:
        print("\n下一批验证")
        code, next_payload = run_skill(["next", *follow_up_args(pageable_success)], env)
        before = pageable_success_case["expected_query"]
        after = next_payload.get("effective_query") or {}
        unchanged = {k: v for k, v in before.items() if k != "currentPage"} == {k: v for k, v in after.items() if k != "currentPage"}
        page_ok = after.get("currentPage") == 2
        next_ok = bool(next_payload.get("ok")) and unchanged and page_ok and search_passed(next_payload)
        print(f"   使用样例：{pageable_success_case['natural_language']}")
        if next_payload.get("user_message"):
            print("   用户会看到：")
            print_user_message(next_payload["user_message"], "     ")
        else:
            print(f"   结果：共找到 {next_payload.get('total_count', 0)} 条，本次展示 {next_payload.get('returned_count', 0)} 条。")
        print(f"   验收：{'通过' if next_ok else '未通过'}")
        results.append({"id": "follow_15_next", "ok": next_ok, "returncode": code})
        next_case = next((case for case in cases if case["type"] == "next_success"), None)
        if next_case:
            append_report_entry(
                report_entries,
                case=next_case,
                interface_call="翻页接口",
                ok=next_ok,
                user_message=report_message(next_payload, "继续下一批未成功。"),
            )

        next_failure_cases = [case for case in cases if case["type"] in {"next_no_current", "next_after_failed_search"}]
        for case in next_failure_cases:
            print(f"   用户说：{case['natural_language']}")
            failure_env = env.copy()
            failure_state = Path(tempfile.gettempdir()) / f"qianlima_skill_{case['id']}_state"
            failure_env["QIANLIMA_SKILL_STATE_DIR"] = str(failure_state)
            if case["type"] == "next_after_failed_search":
                run_skill(["search", "--query-json", json.dumps(case["failed_query"], ensure_ascii=False)], failure_env)
            code, payload = run_skill(["next"], failure_env)
            ok = is_safe_follow_up_failure(payload)
            print("   结果：" + ("上下文缺项，等待补全；未重新查询。" if ok else "行为需要检查。"))
            if payload.get("user_message"):
                print("   用户会看到：")
                print_user_message(payload["user_message"], "     ")
            print(f"   验收：{'通过' if ok else '未通过'}")
            results.append({"id": case["id"], "ok": ok, "returncode": code})
            append_report_entry(
                report_entries,
                case=case,
                interface_call="翻页接口；未调用搜索接口",
                ok=ok,
                user_message=report_message(payload, "还没有可继续展示的结果。请先查一批项目。"),
            )

        print("\n当前结果追问验证")
        follow_cases = [case for case in cases if case["type"] in {"detail", "detail_safe", "detail_failure", "detail_no_current", "source_url"}]
        for case in follow_cases:
            if case["type"] == "source_url" and args.skip_source_url:
                print(f"   跳过：{case['natural_language']}（已选择跳过原文链接验证）")
                continue
            if case["type"] == "detail_no_current":
                active_case = None
                active_payload = None
            elif case["id"] in {"follow_18_ordinal_detail", "follow_21_ordinal_out_of_range", "follow_22_ambiguous_project"}:
                active_case = detail_success_case or first_success_case
                active_payload = detail_success or first_success
            elif case["id"] in {"follow_19_property_source", "follow_20_chaoyang_budget"}:
                active_case = property_success_case
                active_payload = property_success
            elif case["id"] == "follow_19b_ordinal_source":
                active_case = detail_success_case or first_success_case
                active_payload = detail_success or first_success
            else:
                active_case = first_success_case
                active_payload = first_success
            if (not active_case or not active_payload) and case["type"] != "detail_no_current":
                print(f"   跳过：{case['natural_language']}（没有可用的当前结果集）")
                results.append({"id": case["id"], "ok": False, "returncode": 0})
                append_report_entry(
                    report_entries,
                    case=case,
                    interface_call="未调用详情或原文链接接口",
                    ok=False,
                    user_message="当前没有可用于追问的准确项目结果。请您先查到符合条件的项目，再用第几条或标题关键词追问。",
                    note="前置搜索没有产生可用的准确结果。",
                )
                continue
            command_env = env.copy()
            fields = ",".join(case.get("fields") or [])
            command = ["detail", "--project-ref", case["project_ref"]]
            if active_payload:
                command.extend(follow_up_args(active_payload))
            if fields:
                command.extend(["--fields", fields])
            if case["type"] == "source_url":
                command.append("--source-url")
            code, payload = run_skill(command, command_env)
            safe_failure = case["type"] in {"detail_safe", "detail_failure", "detail_no_current"} or case["id"] == "follow_19_property_source"
            ok = bool(payload.get("ok")) or (safe_failure and is_safe_follow_up_failure(payload))
            print(f"   用户说：{case['natural_language']}")
            if active_case:
                print(f"   当前结果来自：{active_case['natural_language']}")
            if payload.get("user_message"):
                print("   用户会看到：")
                print_user_message(payload["user_message"], "     ")
            elif payload.get("ok"):
                print(f"   结果：已定位当前结果并查询详情。")
            else:
                print(f"   结果：未直接猜测，已返回需要您确认的信息。")
            print(f"   验收：{'通过' if ok else '未通过'}")
            results.append({"id": case["id"], "ok": ok, "returncode": code, "payload_ok": payload.get("ok")})
            if case["type"] == "source_url":
                interface_call = "原文链接接口" if payload.get("ok") else "未调用原文链接接口"
            elif payload.get("ok"):
                interface_call = "详情接口"
            else:
                interface_call = "未调用详情接口"
            append_report_entry(
                report_entries,
                case=case,
                interface_call=interface_call,
                ok=ok,
                user_message=report_message(payload, "未直接猜测，请补充项目序号或标题关键词。"),
            )

            if case["type"] == "source_url" and payload.get("ok"):
                before_snapshot = snapshot_payload(state_path, payload)
                code2, payload2 = run_skill(command, command_env)
                after_snapshot = snapshot_payload(state_path, payload2)
                dedupe_ok = bool(payload2.get("ok")) and "quotas" not in before_snapshot and "quotas" not in after_snapshot
                print("   重复索要原文链接：" + ("未写入本地额度状态" if dedupe_ok else "状态需要检查"))
                results.append({"id": "source_url_dedupe", "ok": dedupe_ok, "returncode": code2})
                append_report_entry(
                    report_entries,
                    case={
                        "natural_language": "重复索要同一个项目的原文链接",
                        "understanding": "同一项目重复索要原文链接，不应写入本地额度状态。",
                        "type": "source_url",
                        "category": "boundary",
                    },
                    interface_call="原文链接接口；本地状态校验",
                    ok=dedupe_ok,
                    user_message=report_message(payload2, "重复索要原文链接已完成。"),
                    note="验证重复请求不会生成本地额度计数。",
                )
    else:
        print("\n没有任何搜索样例返回项目，已跳过下一批和详情追问验证。")

    passed = sum(1 for item in results if item.get("ok"))
    total = len(results)
    print("\n验证汇总")
    print(f"通过：{passed} / {total}")
    summary = None
    if summary:
        print("本地额度计数：" + "；".join(f"{key}：{value}" for key, value in summary.items()))
    failed = [item["id"] for item in results if not item.get("ok")]
    if args.report_md:
        write_report(
            Path(args.report_md),
            cases_payload=cases_payload,
            entries=report_entries,
            passed=passed,
            total=total,
            quota=summary,
        )
        print(f"验收报告：{Path(args.report_md).resolve()}")
    if failed:
        print("未通过样例：" + "、".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
