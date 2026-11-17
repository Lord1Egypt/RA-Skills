#!/usr/bin/env python3
"""Live-test detail follow-up intent mapping and backend detail accuracy."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "scripts" / "qianlima_skill.py"


DETAIL_LABELS = {
    "registrationEndTime": "报名截止时间",
    "biddingEndTime": "投标截止时间",
    "budgetAmount": "预算金额",
    "purchasingUnitLinkName": "采购单位联系人",
    "purchasingUnitLinkPhone": "采购单位联系方式",
    "winningBidderUnitLinkName": "中标单位联系人",
    "winningBidderUnitLinkPhone": "中标单位联系方式",
    "agencyUnit": "代理单位",
    "targetKeywords": "标的物",
    "sourceUrl": "原文链接",
}


CONTEXTS: dict[str, dict[str, Any]] = {
    "tender": {
        "command": "search",
        "expected_capability": "search-projects",
        "expected_api_path": "/api/search",
        "expected_result_type": "project",
        "text": "近三个月设备采购公告，先给我 5 条",
        "query": {'beginTime': '2026-01-16', 'endTime': '2026-04-16', 'infoTypes': {'0': []}, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['设备'], 'matchScopes': [2, 8]}]},
    },
    "intention": {
        "command": "search-purchase",
        "expected_capability": "search-purchase-intentions",
        "expected_api_path": "/api/search/purchase",
        "expected_result_type": "purchase_intention",
        "text": "未来三个月设备采购意向，先看 5 条",
        "query": {
            "keywords": ["设备"],
            "startPlanPurchaseDate": "2026-05",
            "endPlanPurchaseDate": "2026-07",
            "numPerPage": 5,
        },
    },
    "award": {
        "command": "search",
        "expected_capability": "search-projects",
        "expected_api_path": "/api/search",
        "expected_result_type": "project",
        "text": "近三个月服务类中标结果，先给我 5 条",
        "query": {'beginTime': '2026-01-16', 'endTime': '2026-04-16', 'infoTypes': {'3': []}, 'numPerPage': 5, 'keywordGroups': [{'keywords': ['服务'], 'matchScopes': [2, 8]}]},
    },
}


CASES: list[dict[str, Any]] = [
    {
        "id": "详情追问-01",
        "context": "tender",
        "user_text": "第 1 条什么时候投标截止，联系人电话有吗",
        "project_ref": "第1条",
        "fields": ["biddingEndTime", "purchasingUnitLinkName", "purchasingUnitLinkPhone"],
        "expected": "应定位当前结果第 1 条，调用详情接口，返回投标截止时间、采购单位联系人、采购单位联系方式。",
    },
    {
        "id": "详情追问-02",
        "context": "tender",
        "user_text": "第一条报名截止时间也给我看一下",
        "project_ref": "第一条",
        "fields": ["registrationEndTime"],
        "expected": "应识别中文序号“第一条”，定位当前结果第 1 条，调用详情接口，返回报名截止时间。",
    },
    {
        "id": "详情追问-03",
        "context": "intention",
        "user_text": "第 1 条联系人是谁，主要买什么",
        "project_ref": "第1条",
        "fields": ["purchasingUnitLinkName", "purchasingUnitLinkPhone", "targetKeywords"],
        "expected": "应定位当前结果第 1 条，调用详情接口，返回联系人、联系方式和标的物。",
    },
    {
        "id": "详情追问-04",
        "context": "award",
        "user_text": "第 1 条中标方联系人和代理机构是哪家",
        "project_ref": "第1条",
        "fields": ["winningBidderUnitLinkName", "winningBidderUnitLinkPhone", "agencyUnit"],
        "expected": "应定位当前结果第 1 条，调用详情接口，返回中标单位联系人、联系方式和代理单位。",
    },
    {
        "id": "详情追问-05",
        "context": "tender",
        "user_text": "刚才那个标题里带指定片段的项目，联系人是谁",
        "project_ref_from_first_title": True,
        "fields": ["purchasingUnitLinkName", "purchasingUnitLinkPhone"],
        "expected": "应从当前结果标题片段唯一定位项目，调用详情接口，返回采购单位联系人和联系方式。",
    },
    {
        "id": "详情追问-06",
        "context": "tender",
        "user_text": "第 1 条原文链接给我",
        "project_ref": "第1条",
        "fields": ["sourceUrl"],
        "source_url": True,
        "expected": "应定位当前结果第 1 条，仅调用原文链接接口返回来源链接。",
    },
    {
        "id": "详情追问-07",
        "context": "tender",
        "user_text": "那个实验室项目预算多少",
        "project_ref": "实验室",
        "fields": ["budgetAmount"],
        "expected_failure": "ambiguous",
        "expected": "“实验室”命中多条当前结果，应返回候选项目，不调用详情接口，不硬猜预算。",
    },
    {
        "id": "详情追问-08",
        "context": "tender",
        "user_text": "第 99 条联系人是谁",
        "project_ref": "第99条",
        "fields": ["purchasingUnitLinkName", "purchasingUnitLinkPhone"],
        "expected_failure": "not_found",
        "expected": "当前结果不足 99 条时应提示换成当前结果里的序号，不调用详情接口。",
    },
]


def run_skill(args: list[str], state_path: Path) -> dict[str, Any]:
    env = os.environ.copy()
    env["QIANLIMA_SKILL_STATE_DIR"] = str(state_path)
    env.pop("QIANLIMA_SKILL_STATE", None)
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
        payload = {"ok": False, "stdout": proc.stdout[:500], "stderr": proc.stderr[:500]}
    payload["_returncode"] = proc.returncode
    return payload


def search_context(context: dict[str, Any], state_path: Path) -> dict[str, Any]:
    return run_skill(
        [
            str(context["command"]),
            "--query-json",
            json.dumps(context["query"], ensure_ascii=False),
            "--user-text",
            context["text"],
        ],
        state_path,
    )


def pick_title_fragment(cards: list[dict[str, Any]]) -> str:
    if not cards:
        return ""
    title = str(cards[0].get("title") or "")
    for length in range(min(14, len(title)), 1, -1):
        fragment = title[:length]
        if sum(1 for card in cards if fragment in str(card.get("title") or "")) == 1:
            return fragment
    return title


def expected_project(case: dict[str, Any], cards: list[dict[str, Any]], project_ref: str) -> dict[str, Any] | None:
    if case.get("expected_failure") or not cards:
        return None
    if project_ref.startswith("第1") or project_ref.startswith("第一"):
        return cards[0]
    for card in cards:
        if project_ref and project_ref in str(card.get("title") or ""):
            return card
    return None


def field_labels(fields: list[str]) -> list[str]:
    return [DETAIL_LABELS.get(field, field) for field in fields]


def detail_command(case: dict[str, Any], project_ref: str) -> list[str]:
    command = ["detail", "--project-ref", project_ref]
    if case.get("fields"):
        command.extend(["--fields", ",".join(case["fields"])])
    if case.get("source_url"):
        command.append("--source-url")
    return command


def follow_up_args(payload: dict[str, Any]) -> list[str]:
    follow_up = payload.get("follow_up") or {}
    return [
        "--session-id",
        str(follow_up.get("session_id") or ""),
        "--result-set-id",
        str(follow_up.get("result_set_id") or ""),
    ]


def backend_accuracy(case: dict[str, Any], payload: dict[str, Any], selected: dict[str, Any] | None) -> dict[str, Any]:
    fields = case.get("fields") or []
    if case.get("expected_failure"):
        return {
            "符合预期": not payload.get("ok") and payload.get("resolution", {}).get("status") == case["expected_failure"],
            "项目定位": payload.get("resolution", {}),
            "详情接口是否应调用": "否",
            "说明": "失败场景只验证不硬猜、不调用详情。",
        }
    detail = payload.get("detail") or {}
    selected_id = str((selected or {}).get("id") or "")
    detail_id = str(detail.get("id") or "")
    missing_fields = [field for field in fields if field not in detail]
    title_match = not selected or detail.get("title") == selected.get("title")
    id_match = not selected_id or detail_id == selected_id
    return {
        "符合预期": bool(payload.get("ok")) and not missing_fields and title_match and id_match,
        "项目定位": payload.get("resolution", {}),
        "详情项目与当前结果一致": id_match and title_match,
        "缺失字段": missing_fields,
        "详情接口是否应调用": "否，仅调用原文链接接口" if fields == ["sourceUrl"] else "是",
    }


def summarize_case(case: dict[str, Any], search_payload: dict[str, Any], state_path: Path) -> dict[str, Any]:
    cards = search_payload.get("cards") or []
    project_ref = case.get("project_ref") or ""
    if case.get("project_ref_from_first_title"):
        project_ref = pick_title_fragment(cards)
    selected = expected_project(case, cards, project_ref)
    command = detail_command(case, project_ref)
    command[1:1] = follow_up_args(search_payload)
    payload = run_skill(command, state_path)
    actual_project_id = (payload.get("detail") or {}).get("id") or (selected or {}).get("id")
    return {
        "用例": case["id"],
        "前置查询": CONTEXTS[case["context"]]["text"],
        "前置能力": search_payload.get("capability"),
        "前置接口路径": search_payload.get("request_api_path"),
        "前置结果类型": search_payload.get("result_type"),
        "前置查询传参": search_payload.get("request_query") or search_payload.get("effective_query"),
        "前置接口总数": search_payload.get("api_total_count", search_payload.get("total_count")),
        "前置本页返回": search_payload.get("api_returned_count", search_payload.get("returned_count")),
        "传入的自然语言": case["user_text"].replace("指定片段", f"“{project_ref}”"),
        "预期返回结果": case["expected"],
        "解析后的结构化字段": {
            "项目指代": project_ref,
            "详情字段": field_labels(case.get("fields") or []),
            "字段入参": case.get("fields") or [],
            "是否索要原文链接": bool(case.get("source_url")),
        },
        "实际传参": {
            "命令": command,
            "定位后项目": {
                "id": actual_project_id,
                "名称": (payload.get("detail") or {}).get("title") or (selected or {}).get("title"),
            },
            "接口动作": "仅原文链接接口" if case.get("fields") == ["sourceUrl"] else ("详情接口 + 原文链接接口" if case.get("source_url") else "详情接口或安全失败"),
        },
        "后端返回数据": payload.get("detail") or {},
        "后端返回准确性": backend_accuracy(case, payload, selected),
        "用户看到的结果": payload.get("user_message"),
    }


def validation_exit_code(results: list[dict[str, Any]], *, expected_count: int) -> int:
    executed = sum(1 for item in results if "后端返回准确性" in item)
    passed = sum(1 for item in results if item.get("后端返回准确性", {}).get("符合预期"))
    return 0 if executed == expected_count and passed == expected_count else 1


def main() -> int:
    if not os.environ.get("QIANLIMA_API_KEY"):
        print("未检测到接口密钥。", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="qianlima_detail_followups_") as tmp:
        tmp_dir = Path(tmp)
        search_payloads: dict[str, dict[str, Any]] = {}
        for name, context in CONTEXTS.items():
            state = tmp_dir / f"{name}.json"
            search_payloads[name] = search_context(context, state)

        results: list[dict[str, Any]] = []
        for case in CASES:
            state = tmp_dir / f"{case['context']}.json"
            search_payload = search_payloads[case["context"]]
            context = CONTEXTS[case["context"]]
            route_ok = (
                search_payload.get("capability") == context["expected_capability"]
                and search_payload.get("request_api_path") == context["expected_api_path"]
                and search_payload.get("result_type") == context["expected_result_type"]
            )
            if not search_payload.get("ok") or not search_payload.get("cards") or not route_ok:
                results.append(
                    {
                        "用例": case["id"],
                        "前置查询": CONTEXTS[case["context"]]["text"],
                        "传入的自然语言": case["user_text"],
                        "预期返回结果": case["expected"],
                        "未执行原因": "前置查询没有可追问的当前结果，或前置能力路由不正确。",
                        "前置查询返回": {
                            "是否成功": search_payload.get("ok"),
                            "接口总数": search_payload.get("api_total_count", search_payload.get("total_count")),
                            "本页返回": search_payload.get("api_returned_count", search_payload.get("returned_count")),
                            "能力": search_payload.get("capability"),
                            "接口路径": search_payload.get("request_api_path"),
                            "结果类型": search_payload.get("result_type"),
                            "用户看到的结果": search_payload.get("user_message"),
                        },
                    }
                )
                continue
            results.append(summarize_case(case, search_payload, state))

    pass_count = sum(1 for item in results if item.get("后端返回准确性", {}).get("符合预期"))
    executed = sum(1 for item in results if "后端返回准确性" in item)
    print(
        json.dumps(
            {
                "测试目标": "详情追问白话意图理解、传参准确性、后端详情返回准确性",
                "汇总": {
                    "用例数": len(CASES),
                    "已执行": executed,
                    "符合预期": f"{pass_count}/{executed}" if executed else "0/0",
                },
                "用例": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return validation_exit_code(results, expected_count=len(CASES))


if __name__ == "__main__":
    raise SystemExit(main())
