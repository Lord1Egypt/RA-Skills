#!/usr/bin/env python3
"""Retest the three previously failed live cases without printing secrets."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "scripts" / "qianlima_skill.py"


CASES: list[dict[str, Any]] = [
    {
        "id": "用例2",
        "text": "帮我找下近一周海淀学校里跟食堂有关的，中标的就行，金额别太小，50 万以上",
        "query": {'areaIds': [3320], 'beginTime': '2026-04-09', 'endTime': '2026-04-15', 'purchasingUnitTypes': [3], 'infoTypes': {'3': []}, 'beginAmount': 500000, 'numPerPage': 10, 'keywordGroups': [{'keywords': ['食堂'], 'matchScopes': [2, 8]}]},
    },
    {
        "id": "用例3",
        "text": "上海浦东最近有没有医院买设备的结果，预算或者中标金额 100 万到 1000 万",
        "query": {'areaIds': [3411], 'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [1], 'infoTypes': {'3': []}, 'beginAmount': 1000000, 'endAmount': 10000000, 'numPerPage': 10, 'keywordGroups': [{'keywords': ['设备'], 'matchScopes': [2, 8]}]},
    },
    {
        "id": "用例12",
        "text": "华东这边最近一个月医院设备采购，100 万以上，先看公告",
        "query": {'areaIds': [24, 15, 30, 1, 3, 16, 21], 'beginTime': '2026-03-15', 'endTime': '2026-04-15', 'purchasingUnitTypes': [1], 'infoTypes': {'0': []}, 'beginAmount': 1000000, 'numPerPage': 10, 'keywordGroups': [{'keywords': ['设备'], 'matchScopes': [2, 8]}]},
    },
]


def run_case(case: dict[str, Any]) -> dict[str, Any]:
    proc = subprocess.run(
        [
            sys.executable,
            str(RUNTIME),
            "search",
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
    return {
        "用例": case["id"],
        "传入的自然语言": case["text"],
        "解析后的结构化字段": case["query"],
        "实际传参": payload.get("request_query"),
        "是否成功": payload.get("ok"),
        "接口总数": payload.get("api_total_count"),
        "接口本页返回": payload.get("api_returned_count"),
        "Skill展示数量": payload.get("returned_count"),
        "提醒": payload.get("warnings"),
        "修正说明": payload.get("corrections"),
        "返回数据": payload.get("cards"),
        "用户可见输出": payload.get("user_message"),
    }


def main() -> int:
    if not os.environ.get("QIANLIMA_API_KEY"):
        print("未检测到接口密钥。", file=sys.stderr)
        return 2
    print(json.dumps([run_case(case) for case in CASES], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
