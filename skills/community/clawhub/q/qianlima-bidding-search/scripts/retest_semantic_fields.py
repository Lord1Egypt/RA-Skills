#!/usr/bin/env python3
"""Live-test non-area semantic mapping without printing secrets."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


from live_validate import normalized_expected_query, keyword_summary, structured_filter_summary, visible_keyword_match

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "scripts" / "qianlima_skill.py"

INFO_NAMES = {
    "0": {"_parent": "招标公告", 3: "招标公告", 4: "重新招标"},
    "2": {5: "信息变更", 6: "答疑公告"},
    "3": {"_parent": "中标公告", 10: "候选人公示", 11: "中标通知", 12: "合同公告"},
}

CASES: list[dict[str, Any]] = [
    {
        "id": "语义字段-01",
        "text": "最近三天医院买影像设备的招标，预算刚好 100 万到 200 万之间，不要维保和耗材，给我 5 条",
        "understanding": "最近三天；医疗机构；影像设备；“招标”按招标公告一级类型；金额 100 万到 200 万；排除维保、耗材；每页 5 条。",
        "query": {'beginTime': '2026-04-13', 'endTime': '2026-04-15', 'excludeWords': ['维保', '耗材'], 'purchasingUnitTypes': [1], 'infoTypes': {'0': []}, 'beginAmount': 1000000, 'endAmount': 2000000, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['影像设备'], 'matchScopes': [2, 8]}]},
    },
    {
        "id": "语义字段-02",
        "text": "近一个月学校空调，中标或者候选都行，金额不低于 50 万但别超过 500 万，排除维修和维保",
        "understanding": "近一个月；学校；空调；“中标或者候选”按中标公告一级类型；金额 50 万到 500 万；排除维修、维保。",
        "query": {'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'excludeWords': ['维修', '维保'], 'purchasingUnitTypes': [3], 'infoTypes': {'3': []}, 'beginAmount': 500000, 'endAmount': 5000000, 'numPerPage': 10, 'keywordGroups': [{'keywords': ['空调'], 'matchScopes': [2, 8]}]},
    },
    {
        "id": "语义字段-03",
        "command": "search-purchase",
        "expected_capability": "search-purchase-intentions",
        "expected_api_path": "/api/search/purchase",
        "expected_result_type": "purchase_intention",
        "text": "政府未来三个月的数字化采购意向，预计采购金额 200 万以内，别带运维，最多看 5 个",
        "understanding": "政府机构；数字化；采购意向；预计采购时间为未来三个月；预计采购金额 200 万以内；排除运维；每页 5 条。",
        "query": {
            "keywords": ["数字化"],
            "excludeWords": ["运维"],
            "purchasingUnitTypes": [2],
            "startPlanPurchaseDate": "2026-05",
            "endPlanPurchaseDate": "2026-07",
            "endPlanPurchaseAmount": 2000000,
            "numPerPage": 5,
        },
    },
    {
        "id": "语义字段-04",
        "text": "近期公安安防监控变更或者答疑，金额 100 万左右，不要监理",
        "understanding": "近期按近一个月；公安；安防监控；信息变更或答疑公告；100 万左右按 80 万到 120 万；排除监理。",
        "query": {'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'excludeWords': ['监理'], 'purchasingUnitTypes': [4], 'infoTypes': {'2': [5, 6]}, 'beginAmount': 800000, 'endAmount': 1200000, 'numPerPage': 10, 'keywordGroups': [{'keywords': ['安防监控'], 'matchScopes': [2, 8]}]},
    },
    {
        "id": "语义字段-05",
        "text": "最近一周通信运营商 5G 基站重新招，预算 300 万以上，不要设计、监理和施工",
        "understanding": "最近一周；通信运营商；5G 基站；重新招标；金额 300 万以上；排除设计、监理、施工。",
        "query": {'beginTime': '2026-04-09', 'endTime': '2026-04-15', 'excludeWords': ['设计', '监理', '施工'], 'purchasingUnitTypes': [7], 'infoTypes': {'0': [4]}, 'beginAmount': 3000000, 'numPerPage': 10, 'keywordGroups': [{'keywords': ['5G基站'], 'matchScopes': [2, 8]}]},
    },
    {
        "id": "语义字段-06",
        "text": "近三个月部队食堂服务合同或者中标，金额 30 万到 100 万，别要装修",
        "understanding": "近三个月；部队；食堂服务；“合同或者中标”按中标公告一级类型；金额 30 万到 100 万；排除装修。",
        "query": {'beginTime': '2026-01-15', 'endTime': '2026-04-15', 'excludeWords': ['装修'], 'purchasingUnitTypes': [6], 'infoTypes': {'3': []}, 'beginAmount': 300000, 'endAmount': 1000000, 'numPerPage': 10, 'keywordGroups': [{'keywords': ['食堂服务'], 'matchScopes': [2, 8]}]},
    },
]


def amount_values(card: dict[str, Any]) -> list[float]:
    values: list[float] = []
    for field in ("budgetAmount", "biddingAmount"):
        value = card.get(field)
        if value in (None, ""):
            continue
        try:
            values.append(float(str(value).replace(",", "").strip()))
        except ValueError:
            pass
    return values


def visible_checks(query: dict[str, Any], cards: list[dict[str, Any]]) -> dict[str, Any]:
    begin = query.get("beginAmount", query.get("startPlanPurchaseAmount"))
    end = query.get("endAmount", query.get("endPlanPurchaseAmount"))
    info_names = [
        INFO_NAMES.get(parent, {}).get(int(value), "")
        for parent, values in (query.get("infoTypes") or {}).items()
        for value in values
    ]
    info_names = [name for name in info_names if name]
    excludes = [str(value) for value in query.get("excludeWords") or []]
    amount_ok = 0
    amount_unknown = 0
    info_ok = 0
    exclude_ok = 0
    keyword_visible = 0
    keyword_unknown = 0
    keyword_mismatch = 0
    for card in cards:
        text = " ".join(str(card.get(field) or "") for field in ("title", "purchasingUnit", "areaName", "infoType"))
        if not info_names or any(name in str(card.get("infoType") or "") for name in info_names):
            info_ok += 1
        if not excludes or not any(word in text for word in excludes):
            exclude_ok += 1
        keyword_match = visible_keyword_match(query, card)
        if keyword_match is True:
            keyword_visible += 1
        elif keyword_match is None:
            keyword_unknown += 1
        else:
            keyword_mismatch += 1
        values = amount_values(card)
        if not values:
            amount_unknown += 1
            continue
        if any((begin is None or value >= float(begin)) and (end is None or value <= float(end)) for value in values):
            amount_ok += 1
    total = len(cards)
    has_amount_filter = begin is not None or end is not None
    visible_ok = (
        total > 0
        and info_ok == total
        and exclude_ok == total
        and keyword_mismatch == 0
        and (not has_amount_filter or amount_ok == total)
    )
    return {
        "通过": visible_ok,
        "核验口径": "只判断可见冲突；隐藏字段不计作已命中或后端错误。",
        "完整可见核验": keyword_unknown == 0 and amount_unknown == 0,
        "关键词不可完整核验": keyword_unknown,
        "阶段可见匹配": f"{info_ok}/{total}",
        "排除词可见匹配": f"{exclude_ok}/{total}",
        "关键词可见命中": f"{keyword_visible}/{total}",
        "金额可见匹配": f"{amount_ok}/{total}",
        "金额不可见": amount_unknown,
        "采购单位类型": "接口字段未直接返回该类型，只核对传参。",
    }


def normalized(query: dict[str, Any], command: str = "search") -> dict[str, Any]:
    return normalized_expected_query(query, command)


def run_case(case: dict[str, Any]) -> dict[str, Any]:
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
    sent = payload.get("request_query") or {}
    expected = normalized(case["query"], command)
    cards = payload.get("cards") or []
    visible_result = visible_checks(case["query"], cards)
    expected_capability = case.get("expected_capability") or "search-projects"
    expected_api_path = case.get("expected_api_path") or "/api/search"
    expected_result_type = case.get("expected_result_type") or "project"
    route_ok = (
        payload.get("capability") == expected_capability
        and payload.get("request_api_path") == expected_api_path
        and payload.get("result_type") == expected_result_type
    )
    return {
        "用例": case["id"],
        "传入的自然语言": case["text"],
        "语义理解": case["understanding"],
        "解析后的结构化字段": case["query"],
        "实际传参": sent,
        "传参是否匹配语义": sent == expected,
        "命令": command,
        "能力路由是否匹配": route_ok,
        "实际能力": payload.get("capability"),
        "实际接口路径": payload.get("request_api_path"),
        "实际结果类型": payload.get("result_type"),
        "接口调用成功": bool(payload.get("ok")),
        "接口总数": payload.get("api_total_count"),
        "接口本页返回": payload.get("api_returned_count"),
        "Skill展示数量": payload.get("returned_count"),
        "可见字段匹配": visible_result["通过"],
        "可见字段匹配观察": visible_result,
        "返回数据前3条": cards[:3],
        "用户可见输出": payload.get("user_message"),
    }


def main() -> int:
    if not os.environ.get("QIANLIMA_API_KEY"):
        print("未检测到接口密钥。", file=sys.stderr)
        return 2
    results = [run_case(case) for case in CASES]
    summary = {
        "传参匹配": f"{sum(1 for item in results if item['传参是否匹配语义'])}/{len(results)}",
        "能力路由匹配": f"{sum(1 for item in results if item['能力路由是否匹配'])}/{len(results)}",
        "可见字段匹配": f"{sum(1 for item in results if item['可见字段匹配'])}/{len(results)}",
        "展示数量匹配接口本页返回": f"{sum(1 for item in results if item['接口本页返回'] == item['Skill展示数量'])}/{len(results)}",
    }
    print(json.dumps({"汇总": summary, "明细": results}, ensure_ascii=False, indent=2))
    passed = all(
        item["接口调用成功"]
        and item["传参是否匹配语义"]
        and item["能力路由是否匹配"]
        and item["可见字段匹配"]
        and item["接口本页返回"] == item["Skill展示数量"]
        for item in results
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
