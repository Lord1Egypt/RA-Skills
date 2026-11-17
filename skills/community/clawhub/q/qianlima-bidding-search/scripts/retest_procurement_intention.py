#!/usr/bin/env python3
"""Verify procurement-intention validation uses the dedicated capability and API."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "scripts" / "qianlima_skill.py"


QUERY: dict[str, Any] = {
    "keywords": ["数字化"],
    "purchasingUnitTypes": [2],
    "startPlanPurchaseDate": "2026-05",
    "endPlanPurchaseDate": "2026-07",
    "endPlanPurchaseAmount": 2000000,
    "numPerPage": 10,
}

USER_TEXT = "政府未来三个月的数字化采购意向，预计采购金额 200 万以内，看 10 条"


def main() -> int:
    if not os.environ.get("QIANLIMA_API_KEY"):
        print("未检测到接口密钥。", file=sys.stderr)
        return 2

    proc = subprocess.run(
        [
            sys.executable,
            str(RUNTIME),
            "search-purchase",
            "--query-json",
            json.dumps(QUERY, ensure_ascii=False),
            "--user-text",
            USER_TEXT,
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

    cards = payload.get("cards") or []
    intention_cards = [
        {
            "序号": index,
            "项目名称": card.get("title"),
            "发布时间": card.get("publishTime"),
            "预计采购时间": card.get("planPurchaseDate"),
            "预计采购金额": card.get("budgetAmount"),
            "链接": card.get("url"),
        }
        for index, card in enumerate(cards, start=1)
    ]
    route_ok = (
        payload.get("capability") == "search-purchase-intentions"
        and payload.get("result_type") == "purchase_intention"
        and payload.get("request_api_path") == "/api/search/purchase"
    )
    card_shape_ok = bool(cards) and all(card.get("planPurchaseDate") for card in cards)

    output = {
        "传入自然语言": USER_TEXT,
        "结构化查询": QUERY,
        "实际传参": payload.get("request_query"),
        "实际能力": payload.get("capability"),
        "实际接口路径": payload.get("request_api_path"),
        "实际结果类型": payload.get("result_type"),
        "路由正确": route_ok,
        "接口调用成功": payload.get("ok"),
        "接口总数": payload.get("api_total_count"),
        "本页返回": payload.get("api_returned_count"),
        "Skill展示": payload.get("returned_count"),
        "采购意向卡片字段正确": card_shape_ok,
        "采购意向样例": intention_cards[:5],
        "用户可见输出前20行": "\n".join((payload.get("user_message") or "").splitlines()[:20]),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if payload.get("ok") and route_ok and card_shape_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
