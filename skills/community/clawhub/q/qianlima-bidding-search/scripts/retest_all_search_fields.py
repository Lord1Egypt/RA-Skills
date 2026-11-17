#!/usr/bin/env python3
"""Live-test every search input field with diverse cases.

This script prints no secrets and only reports summarized returned data.
"""

from __future__ import annotations

import datetime as dt
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import area_resolver


from live_validate import normalized_expected_query, keyword_summary, structured_filter_summary, visible_keyword_match

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "scripts" / "qianlima_skill.py"
AREA_FILE = ROOT / "references" / "area.json"

INFO_NAMES = {
    "0": {"_parent": "招标公告", 3: "招标公告", 4: "重新招标"},
    "1": {2: "招标预告"},
    "2": {5: "信息变更", 6: "答疑公告"},
    "3": {"_parent": "中标公告", 7: "废标公告", 8: "流标公告", 10: "候选人公示", 11: "中标通知", 12: "合同公告"},
}

CASE_GROUPS: list[dict[str, Any]] = [
    {
        "field": "keywordGroups.keywords",
        "cases": [
            {
                "id": "keywords_01",
                "text": "近一个月医院设备招标，预算 100 万以上，看 5 条",
                "query": {'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [1], 'infoTypes': {'0': []}, 'beginAmount': 1000000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['设备'], 'matchScopes': [2, 8]}]},
            },
            {
                "id": "keywords_02",
                "text": "近一个月学校空调中标，金额 50 万以上，看 5 条",
                "query": {'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [3], 'infoTypes': {'3': []}, 'beginAmount': 500000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['空调'], 'matchScopes': [2, 8]}]},
            },
        ],
    },
    {
        "field": "关键词逻辑（普通项目分组 / 采购意向单一关系）",
        "cases": [
            {
                "id": "keywords_search_type_01_or",
                "text": "北京学校空调或者新风项目，看公告",
                "query": {'areaIds': [2], 'purchasingUnitTypes': [3], 'infoTypes': {'0': []}, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['空调', '新风'], 'matchScopes': [2, 8]}]},
            },
            {
                "id": "keywords_search_type_02_and",
                "command": "search-purchase",
                "expected_capability": "search-purchase-intentions",
                "expected_api_path": "/api/search/purchase",
                "expected_result_type": "purchase_intention",
                "text": "广州政府项目同时包含数字化和平台，别带运维，看看采购意向",
                "query": {
                    "areaIds": [305],
                    "keywords": ["数字化", "平台"],
                    "keywordsSearchType": 2,
                    "excludeWords": ["运维"],
                    "purchasingUnitTypes": [2],
                    "numPerPage": 5,
                },
            },
        ],
    },
    {
        "field": "excludeWords",
        "cases": [
            {
                "id": "exclude_01",
                "text": "最近三天医院影像设备招标，100 万到 200 万，不要维保和耗材",
                "query": {'excludeWords': ['维保', '耗材'], 'beginTime': '2026-04-13', 'endTime': '2026-04-15', 'purchasingUnitTypes': [1], 'infoTypes': {'0': []}, 'beginAmount': 1000000, 'endAmount': 2000000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['影像设备'], 'matchScopes': [2, 8]}]},
            },
            {
                "id": "exclude_02",
                "text": "近一个月学校空调中标，50 万到 500 万，不要维修和维保",
                "query": {'excludeWords': ['维修', '维保'], 'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [3], 'infoTypes': {'3': []}, 'beginAmount': 500000, 'endAmount': 5000000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['空调'], 'matchScopes': [2, 8]}]},
            },
        ],
    },
    {
        "field": "areaIds",
        "cases": [
            {
                "id": "area_01_city",
                "text": "北京学校空调中标，50 万以上，看 5 条",
                "query": {'areaIds': [2], 'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [3], 'infoTypes': {'3': []}, 'beginAmount': 500000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['空调'], 'matchScopes': [2, 8]}]},
            },
            {
                "id": "area_02_district_exact",
                "text": "上海浦东医院设备中标，100 万到 1000 万，看 5 条",
                "query": {'areaIds': [3411], 'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [1], 'infoTypes': {'3': []}, 'beginAmount': 1000000, 'endAmount': 10000000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['设备'], 'matchScopes': [2, 8]}]},
            },
            {
                "id": "area_03_region_group",
                "text": "大湾区学校空调中标，最近一个月，看 5 条",
                "query": {'areaIds': [305, 316, 322, 304, 307, 303, 321, 308, 320], 'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [3], 'infoTypes': {'3': []}, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['空调'], 'matchScopes': [2, 8]}]},
            },
        ],
    },
    {
        "field": "beginTime/endTime",
        "cases": [
            {
                "id": "time_01_today",
                "text": "今天医院设备招标，100 万以上，看 5 条",
                "query": {'beginTime': '2026-04-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [1], 'infoTypes': {'0': []}, 'beginAmount': 1000000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['设备'], 'matchScopes': [2, 8]}]},
            },
            {
                "id": "time_02_two_days",
                "command": "search-purchase",
                "expected_capability": "search-purchase-intentions",
                "expected_api_path": "/api/search/purchase",
                "expected_result_type": "purchase_intention",
                "text": "这两天政府数字化采购意向，预算 200 万以内，看 5 条",
                "query": {
                    "keywords": ["数字化"],
                    "beginTime": "2026-04-14",
                    "endTime": "2026-04-15",
                    "purchasingUnitTypes": [2],
                    "endPlanPurchaseAmount": 2000000,
                    "numPerPage": 5,
                },
            },
            {
                "id": "time_03_three_months",
                "text": "近三个月部队食堂服务合同或中标，30 万到 100 万，看 5 条",
                "query": {'beginTime': '2026-01-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [6], 'infoTypes': {'3': []}, 'beginAmount': 300000, 'endAmount': 1000000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['食堂服务'], 'matchScopes': [2, 8]}]},
            },
        ],
    },
    {
        "field": "purchasingUnitTypes",
        "cases": [
            {
                "id": "unit_01_hospital",
                "text": "医院设备招标，近一个月，100 万以上，看 5 条",
                "query": {'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [1], 'infoTypes': {'0': []}, 'beginAmount': 1000000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['设备'], 'matchScopes': [2, 8]}]},
            },
            {
                "id": "unit_02_school",
                "text": "学校空调中标，近一个月，50 万以上，看 5 条",
                "query": {'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [3], 'infoTypes': {'3': []}, 'beginAmount': 500000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['空调'], 'matchScopes': [2, 8]}]},
            },
            {
                "id": "unit_03_government",
                "command": "search-purchase",
                "expected_capability": "search-purchase-intentions",
                "expected_api_path": "/api/search/purchase",
                "expected_result_type": "purchase_intention",
                "text": "政府数字化采购意向，两天内，200 万以内，看 5 条",
                "query": {
                    "keywords": ["数字化"],
                    "beginTime": "2026-04-14",
                    "endTime": "2026-04-15",
                    "purchasingUnitTypes": [2],
                    "endPlanPurchaseAmount": 2000000,
                    "numPerPage": 5,
                },
            },
        ],
    },
    {
        "field": "infoTypes",
        "cases": [
            {
                "id": "info_01_tender",
                "text": "医院设备，只看公告，近一个月，100 万以上，看 5 条",
                "query": {'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [1], 'infoTypes': {'0': []}, 'beginAmount': 1000000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['设备'], 'matchScopes': [2, 8]}]},
            },
            {
                "id": "info_02_tender_child",
                "text": "医院设备，只看普通招标公告，不含重新招标，近一个月，100 万以上，看 5 条",
                "query": {'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [1], 'infoTypes': {'0': [3]}, 'beginAmount': 1000000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['设备'], 'matchScopes': [2, 8]}]},
            },
            {
                "id": "info_02_win",
                "text": "学校空调，只看中标通知，近一个月，50 万以上，看 5 条",
                "query": {'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [3], 'infoTypes': {'3': [11]}, 'beginAmount': 500000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['空调'], 'matchScopes': [2, 8]}]},
            },
            {
                "id": "info_03_candidate_colloquial",
                "text": "学校空调，看候选人或者入围名单，近一个月，50 万以上，看 5 条",
                "query": {'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [3], 'infoTypes': {'3': [10]}, 'beginAmount': 500000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['空调'], 'matchScopes': [2, 8]}]},
            },
            {
                "id": "info_04_contract_colloquial",
                "text": "学校空调，看合同或者签合同的结果，近一个月，50 万以上，看 5 条",
                "query": {'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [3], 'infoTypes': {'3': [12]}, 'beginAmount': 500000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['空调'], 'matchScopes': [2, 8]}]},
            },
            {
                "id": "info_05_change_or_answer",
                "text": "公安安防监控变更或者答疑，近期，100 万左右，看 5 条",
                "query": {'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [4], 'infoTypes': {'2': [5, 6]}, 'beginAmount': 800000, 'endAmount': 1200000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['安防监控'], 'matchScopes': [2, 8]}]},
            },
        ],
    },
    {
        "field": "beginAmount/endAmount",
        "cases": [
            {
                "id": "amount_01_lower",
                "text": "医院设备招标，300 万以上，近一个月，看 5 条",
                "query": {'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [1], 'infoTypes': {'0': []}, 'beginAmount': 3000000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['设备'], 'matchScopes': [2, 8]}]},
            },
            {
                "id": "amount_02_upper",
                "command": "search-purchase",
                "expected_capability": "search-purchase-intentions",
                "expected_api_path": "/api/search/purchase",
                "expected_result_type": "purchase_intention",
                "text": "政府数字化采购意向，200 万以内，这两天，看 5 条",
                "query": {
                    "keywords": ["数字化"],
                    "beginTime": "2026-04-14",
                    "endTime": "2026-04-15",
                    "purchasingUnitTypes": [2],
                    "endPlanPurchaseAmount": 2000000,
                    "numPerPage": 5,
                },
            },
            {
                "id": "amount_03_range",
                "text": "学校空调中标，50 万到 500 万，近一个月，看 5 条",
                "query": {'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [3], 'infoTypes': {'3': []}, 'beginAmount': 500000, 'endAmount': 5000000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['空调'], 'matchScopes': [2, 8]}]},
            },
        ],
    },
    {
        "field": "currentPage/numPerPage",
        "cases": [
            {
                "id": "page_01_size_3",
                "text": "学校空调中标，近一个月，50 万以上，只看 3 条",
                "query": {'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [3], 'infoTypes': {'3': []}, 'beginAmount': 500000, 'numPerPage': 3, 'keywordGroups': [{'keywords': ['空调'], 'matchScopes': [2, 8]}]},
            },
            {
                "id": "page_02_second_page",
                "text": "学校空调中标，近一个月，50 万以上，直接看第 2 页，每页 3 条",
                "query": {'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [3], 'infoTypes': {'3': []}, 'beginAmount': 500000, 'currentPage': 2, 'numPerPage': 3, 'keywordGroups': [{'keywords': ['空调'], 'matchScopes': [2, 8]}]},
            },
        ],
    },
]


def area_path(area_id: int) -> str:
    return area_resolver.catalog().display_path(area_id)


def expected_request(query: dict[str, Any], command: str = "search") -> dict[str, Any]:
    return normalized_expected_query(query, command)


def compact_query(query: dict[str, Any]) -> str:
    parts: list[str] = []
    if keyword_summary(query):
        parts.append("关键词=" + keyword_summary(query))
    parts.extend(structured_filter_summary(query))
    if query.get("excludeWords"):
        parts.append("排除=" + "、".join(query["excludeWords"]))
    if query.get("areaIds"):
        parts.append("地区=" + "、".join(dict.fromkeys(area_path(int(value)) for value in query["areaIds"])))
    if query.get("beginTime") or query.get("endTime"):
        parts.append(f"时间={query.get('beginTime', '不限')} 至 {query.get('endTime', '不限')}")
    if query.get("purchasingUnitTypes"):
        parts.append("采购单位类型=" + "、".join(str(value) for value in query["purchasingUnitTypes"]))
    if query.get("infoTypes"):
        parts.append("信息类型=" + json.dumps(query["infoTypes"], ensure_ascii=False, sort_keys=True))
    if query.get("beginAmount") is not None:
        parts.append(f"金额下限={float(query['beginAmount']) / 10000:.2f} 万元")
    if query.get("endAmount") is not None:
        parts.append(f"金额上限={float(query['endAmount']) / 10000:.2f} 万元")
    parts.append(f"页码={query.get('currentPage', 1)}")
    parts.append(f"每页={query.get('numPerPage')}")
    return "；".join(parts)


def parse_amount(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(str(value).replace(",", "").strip())
    except ValueError:
        return None


def card_amounts(card: dict[str, Any]) -> list[float]:
    return [value for value in (parse_amount(card.get("budgetAmount")), parse_amount(card.get("biddingAmount"))) if value is not None]


def publication_time_match(query: dict[str, Any], value: Any) -> bool | None:
    def endpoint(text: Any, *, end: bool) -> dt.datetime:
        parsed = dt.datetime.fromisoformat(str(text))
        return parsed.replace(hour=23, minute=59, second=59) if end and len(str(text)) == 10 else parsed

    if not query.get("beginTime") and not query.get("endTime"):
        return True
    try:
        lower = endpoint(query["beginTime"], end=False) if query.get("beginTime") else dt.datetime.min
        upper = endpoint(query["endTime"], end=True) if query.get("endTime") else dt.datetime.max
        visible_lower = endpoint(value, end=False)
        visible_upper = endpoint(value, end=True)
    except (TypeError, ValueError):
        return None
    if visible_upper < lower or visible_lower > upper:
        return False
    if lower <= visible_lower and visible_upper <= upper:
        return True
    return None


def info_expected_names(query: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for parent, values in (query.get("infoTypes") or {}).items():
        for value in values:
            name = INFO_NAMES.get(parent, {}).get(int(value))
            if name:
                names.append(name)
    return names


def card_text(card: dict[str, Any]) -> str:
    return " ".join(str(card.get(field) or "") for field in ("title", "purchasingUnit", "areaName", "infoType"))


def ratio(ok: int, total: int) -> str:
    return f"{ok}/{total}"


def visible_accuracy(query: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    cards = payload.get("cards") or []
    total = len(cards)
    begin = query.get("beginAmount", query.get("startPlanPurchaseAmount"))
    end = query.get("endAmount", query.get("endPlanPurchaseAmount"))
    excludes = [str(value) for value in query.get("excludeWords") or []]
    info_names = info_expected_names(query)
    area_ids = [int(value) for value in query.get("areaIds") or []]
    area_names = [area_path(value).split("-")[-1] for value in area_ids]

    checks = {
        "关键词可见命中": [0, total],
        "排除词可见通过": [0, total],
        "地区可见匹配": [0, total],
        "发布时间匹配": [0, total],
        "信息类型可见匹配": [0, total],
        "金额可见匹配": [0, total],
    }
    keyword_unknown = 0
    amount_unknown = 0
    date_unknown = 0
    mismatches: list[str] = []

    for index, card in enumerate(cards, start=1):
        text = card_text(card)
        keyword_match = visible_keyword_match(query, card)
        if keyword_match is True:
            checks["关键词可见命中"][0] += 1
        elif keyword_match is None:
            keyword_unknown += 1
        else:
            mismatches.append(f"第{index}条关键词与限定位置不匹配")

        if not excludes or not any(word in text for word in excludes):
            checks["排除词可见通过"][0] += 1
        else:
            found = [word for word in excludes if word in text]
            mismatches.append(f"第{index}条包含排除词：{'、'.join(found)}")

        if not area_names or any(name and name in str(card.get("areaName") or "") for name in area_names):
            checks["地区可见匹配"][0] += 1
        else:
            mismatches.append(f"第{index}条地区不可见匹配")

        publish_match = publication_time_match(query, card.get("publishTime"))
        if publish_match is True:
            checks["发布时间匹配"][0] += 1
        elif publish_match is None:
            date_unknown += 1
        else:
            mismatches.append(f"第{index}条发布时间不匹配：{card.get('publishTime')}")

        if not info_names or any(name in str(card.get("infoType") or "") for name in info_names):
            checks["信息类型可见匹配"][0] += 1
        else:
            mismatches.append(f"第{index}条信息类型不匹配：{card.get('infoType')}")

        amounts = card_amounts(card)
        if begin is None and end is None:
            checks["金额可见匹配"][0] += 1
        elif not amounts:
            amount_unknown += 1
        elif any((begin is None or value >= float(begin)) and (end is None or value <= float(end)) for value in amounts):
            checks["金额可见匹配"][0] += 1
        else:
            mismatches.append(f"第{index}条金额不匹配")

    return {
        "计数": {
            "接口总数": payload.get("api_total_count"),
            "接口本页返回": payload.get("api_returned_count"),
            "Skill展示": payload.get("returned_count"),
        },
        "可见字段": {key: ratio(value[0], value[1]) for key, value in checks.items()},
        "关键词不可完整核验": keyword_unknown,
        "金额不可见": amount_unknown,
        "日期不可见": date_unknown,
        "前5个问题": mismatches[:5],
    }


def sample_cards(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "项目名称": card.get("title"),
            "招标单位": card.get("purchasingUnit"),
            "地区": card.get("areaName"),
            "发布时间": card.get("publishTime"),
            "阶段": card.get("infoType"),
            "预算": card.get("budgetAmount"),
            "中标金额": card.get("biddingAmount"),
        }
        for card in cards[:2]
    ]


def run_case(field: str, case: dict[str, Any]) -> dict[str, Any]:
    command = str(case.get("command") or "search")
    proc = subprocess.run(
        [
            sys.executable,
            str(RUNTIME),
            command,
            "--query-json",
            json.dumps(case["query"], ensure_ascii=False),
            "--user-text",
            case["text"],
        ],
        env=os.environ.copy(),
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        payload = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        payload = {"ok": False, "stdout": proc.stdout[:500], "stderr": proc.stderr[:500]}

    expected = expected_request(case["query"], command)
    sent = payload.get("request_query") or {}
    accuracy = visible_accuracy(sent, payload)
    returned = payload.get("api_returned_count")
    shown = payload.get("returned_count")
    expected_capability = case.get("expected_capability") or "search-projects"
    expected_api_path = case.get("expected_api_path") or "/api/search"
    expected_result_type = case.get("expected_result_type") or "project"
    route_ok = (
        payload.get("capability") == expected_capability
        and payload.get("request_api_path") == expected_api_path
        and payload.get("result_type") == expected_result_type
    )
    return {
        "字段": field,
        "用例": case["id"],
        "自然语言": case["text"],
        "期望传参": expected,
        "实际传参": sent,
        "传参匹配": sent == expected,
        "命令": command,
        "能力路由匹配": route_ok,
        "实际能力": payload.get("capability"),
        "实际接口路径": payload.get("request_api_path"),
        "实际结果类型": payload.get("result_type"),
        "接口调用成功": bool(payload.get("ok")),
        "返回展示匹配": returned == shown,
        "准确性观察": accuracy,
        "样例返回": sample_cards(payload.get("cards") or []),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="字段级真实接口验收")
    parser.add_argument("--summary-only", action="store_true", help="只输出汇总和问题，不输出每条返回样例")
    args = parser.parse_args()
    if not os.environ.get("QIANLIMA_API_KEY"):
        print("未检测到接口密钥。", file=sys.stderr)
        return 2
    results: list[dict[str, Any]] = []
    for group in CASE_GROUPS:
        for case in group["cases"]:
            results.append(run_case(group["field"], case))

    field_summary: dict[str, dict[str, Any]] = {}
    for item in results:
        summary = field_summary.setdefault(item["字段"], {"用例数": 0, "传参匹配": 0, "路由匹配": 0, "展示匹配": 0, "问题": []})
        summary["用例数"] += 1
        summary["传参匹配"] += 1 if item["传参匹配"] else 0
        summary["路由匹配"] += 1 if item["能力路由匹配"] else 0
        summary["展示匹配"] += 1 if item["返回展示匹配"] else 0
        issues = item["准确性观察"]["前5个问题"]
        if issues:
            summary["问题"].append({"用例": item["用例"], "问题": issues})

    output: dict[str, Any] = {
        "总览": {
            "用例数": len(results),
            "传参匹配": f"{sum(1 for item in results if item['传参匹配'])}/{len(results)}",
            "能力路由匹配": f"{sum(1 for item in results if item['能力路由匹配'])}/{len(results)}",
            "展示数量匹配接口本页返回": f"{sum(1 for item in results if item['返回展示匹配'])}/{len(results)}",
        },
        "字段汇总": field_summary,
    }
    if args.summary_only:
        output["未通过传参"] = [
            {
                "字段": item["字段"],
                "用例": item["用例"],
                "自然语言": item["自然语言"],
                "期望传参": item["期望传参"],
                "实际传参": item["实际传参"],
            }
            for item in results
            if not item["传参匹配"]
        ]
    else:
        output["明细"] = results
    print(json.dumps(output, ensure_ascii=False, indent=2))
    passed = all(
        item["接口调用成功"]
        and item["传参匹配"]
        and item["能力路由匹配"]
        and item["返回展示匹配"]
        and not item["准确性观察"]["前5个问题"]
        for item in results
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
