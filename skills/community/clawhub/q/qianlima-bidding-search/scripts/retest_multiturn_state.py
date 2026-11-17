#!/usr/bin/env python3
"""Live-test multi-turn query state preservation without printing secrets."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


from live_validate import normalized_expected_query, keyword_summary, structured_filter_summary, visible_keyword_match

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "scripts" / "qianlima_skill.py"


INITIAL_QUERY: dict[str, Any] = {'excludeWords': ['维修'], 'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [3], 'infoTypes': {'3': []}, 'beginAmount': 500000, 'numPerPage': 3, 'keywordGroups': [{'keywords': ['空调'], 'matchScopes': [2, 8]}]}


def run_skill(args: list[str]) -> dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, str(RUNTIME), *args],
        env=os.environ.copy(),
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


def follow_up_command(command: list[str], payload: dict[str, Any]) -> list[str]:
    follow_up = payload.get("follow_up") or {}
    return [
        command[0],
        "--session-id",
        str(follow_up.get("session_id") or ""),
        "--result-set-id",
        str(follow_up.get("result_set_id") or ""),
        *command[1:],
    ]


def expected_with(base: dict[str, Any], **updates: Any) -> dict[str, Any]:
    value = json.loads(json.dumps(base, ensure_ascii=False))
    value.update(updates)
    return normalized_expected_query(value)


def compact_query(query: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "keywordGroups",
        "excludeWords",
        "areaIds",
        "beginTime",
        "endTime",
        "purchasingUnitTypes",
        "infoTypes",
        "beginAmount",
        "endAmount",
        "currentPage",
        "numPerPage",
    ]
    return {key: query.get(key) for key in keys if key in query}


def summarize_step(name: str, text: str, payload: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    actual = payload.get("request_query") or payload.get("effective_query") or {}
    actual_compact = compact_query(actual)
    expected_compact = compact_query(expected)
    return {
        "步骤": name,
        "用户意图": text,
        "是否成功": payload.get("ok"),
        "期望传参": expected_compact,
        "实际传参": actual_compact,
        "传参是否完整匹配": actual_compact == expected_compact,
        "接口总数": payload.get("api_total_count", payload.get("total_count")),
        "本页返回": payload.get("api_returned_count", payload.get("returned_count")),
        "Skill展示": payload.get("returned_count"),
        "用户可见摘要": "\n".join((payload.get("user_message") or "").splitlines()[:12]),
    }


def main() -> int:
    if not os.environ.get("QIANLIMA_API_KEY"):
        print("未检测到接口密钥。", file=sys.stderr)
        return 2

    state_dir = tempfile.TemporaryDirectory(prefix="qianlima_multiturn_state_")
    previous_state_dir = os.environ.get("QIANLIMA_SKILL_STATE_DIR")
    os.environ["QIANLIMA_SKILL_STATE_DIR"] = state_dir.name
    results: list[dict[str, Any]] = []

    first = run_skill(
        [
            "search",
            "--query-json",
            json.dumps(INITIAL_QUERY, ensure_ascii=False),
            "--user-text",
            "近一个月学校空调中标，50 万以上，排除维修，每页 3 条",
        ]
    )
    expected_first = expected_with(INITIAL_QUERY)
    results.append(summarize_step("搜索一批", "近一个月学校空调中标，50 万以上，排除维修，每页 3 条", first, expected_first))

    next_page = run_skill(follow_up_command(["next"], first))
    expected_next = expected_with(INITIAL_QUERY, currentPage=2)
    results.append(summarize_step("继续下一批", "继续看下一批", next_page, expected_next))

    refine_amount = run_skill(
        follow_up_command(
            [
            "refine",
            "--query-json",
            json.dumps({"beginAmount": 1000000}, ensure_ascii=False),
            "--user-text",
            "只看 100 万以上的",
            ],
            next_page,
        )
    )
    expected_amount = expected_with(INITIAL_QUERY, beginAmount=1000000, currentPage=1)
    results.append(summarize_step("收缩金额", "只看 100 万以上的", refine_amount, expected_amount))

    next_after_refine = run_skill(follow_up_command(["next"], refine_amount))
    expected_next_after_refine = expected_with(INITIAL_QUERY, beginAmount=1000000, currentPage=2)
    results.append(summarize_step("收缩后翻页", "继续看下一批", next_after_refine, expected_next_after_refine))

    refine_exclude = run_skill(
        follow_up_command(
            [
            "refine",
            "--query-json",
            json.dumps({"excludeWords": ["维修", "维保"]}, ensure_ascii=False),
            "--user-text",
            "再排除维保",
            ],
            next_after_refine,
        )
    )
    expected_exclude = expected_with(INITIAL_QUERY, beginAmount=1000000, excludeWords=["维修", "维保"], currentPage=1)
    results.append(summarize_step("增加排除词", "再排除维保", refine_exclude, expected_exclude))

    refine_keyword = run_skill(
        follow_up_command(
            [
            "refine",
            "--query-json",
            json.dumps({'keywordGroups': [{'keywords': ['设备'], 'matchScopes': [2, 8]}]}, ensure_ascii=False),
            "--user-text",
            "换成设备",
            ],
            refine_exclude,
        )
    )
    expected_keyword = expected_with(INITIAL_QUERY, beginAmount=1000000, excludeWords=["维修", "维保"], keywordGroups=[{"keywords":["设备"],"matchScopes":[2,8]}], currentPage=1)
    results.append(summarize_step("更换关键词", "换成设备", refine_keyword, expected_keyword))

    print(
        json.dumps(
            {
                "总览": {
                    "步骤数": len(results),
                    "传参完整匹配": f"{sum(1 for item in results if item['传参是否完整匹配'])}/{len(results)}",
                    "成功步骤": f"{sum(1 for item in results if item['是否成功'])}/{len(results)}",
                },
                "明细": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    exit_code = 0 if all(item["传参是否完整匹配"] for item in results) else 1
    if previous_state_dir is None:
        os.environ.pop("QIANLIMA_SKILL_STATE_DIR", None)
    else:
        os.environ["QIANLIMA_SKILL_STATE_DIR"] = previous_state_dir
    state_dir.cleanup()
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
