#!/usr/bin/env python3
"""把 AI 重写搜索结果编译为普通搜索接口请求参数。

输入可以是 aiSearchSubmitPolling 的完整响应，也可以直接是 data 对象。
示例：
  python compile_search_condition.py --input ai-result.json
  cat ai-result.json | python compile_search_condition.py --pretty
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


def parse_args() -> argparse.Namespace:
    """解析输入、分页和输出选项。"""
    parser = argparse.ArgumentParser(description="编译保标招标普通搜索条件")
    parser.add_argument("--input", help="AI 重写响应 JSON 文件；不指定时读取标准输入")
    parser.add_argument("--page-id", type=int, default=1)
    parser.add_argument("--page-number", type=int, default=20)
    parser.add_argument("--pretty", action="store_true", help="格式化输出 JSON")
    return parser.parse_args()


def read_json(path: str | None) -> dict[str, Any]:
    """读取完整 AI 响应或 data 对象。"""
    if path:
        with open(path, "r", encoding="utf-8") as file:
            raw = file.read()
    else:
        raw = sys.stdin.read()
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("输入 JSON 必须是对象")
    if isinstance(value.get("data"), dict):
        return value["data"]
    return value


def join_unique(values: list[Any]) -> list[str]:
    """合并字符串编码并保持首次出现顺序。"""
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, list):
            continue
        for item in value:
            text = str(item).strip()
            if text and text not in seen:
                seen.add(text)
                result.append(text)
    return result


def compile_condition(data: dict[str, Any], page_id: int, page_number: int) -> dict[str, Any]:
    """将 AI 条件映射为 searchProjectApi 请求体。"""
    if page_id < 1:
        raise ValueError("page-id 必须大于等于 1")
    if page_number < 0 or page_number > 50:
        raise ValueError("page-number 必须在 0 到 50 之间")

    condition = data.get("searchCondition") or {}
    area = data.get("areaCode") or {}
    industry_items = data.get("industryCodes") or []
    first_codes: list[Any] = []
    second_codes: list[Any] = []
    third_codes: list[Any] = []
    for item in industry_items:
        if isinstance(item, dict):
            first_codes.append(item.get("firstCodeList", []))
            second_codes.append(item.get("secondCodeList", []))
            third_codes.append(item.get("thirdCodeList", []))

    subjects = condition.get("subjects") or []
    if isinstance(subjects, str):
        subjects = [subjects]
    keyword = "|".join(str(item).strip() for item in subjects if str(item).strip())

    start_date = condition.get("searchStartTime")
    end_date = condition.get("searchEndTime")
    if not start_date or not end_date:
        raise ValueError("AI 重写结果缺少 searchStartTime 或 searchEndTime")

    project_class_ids = condition.get("projectClassIds") or "-100"
    purchase_type_id = condition.get("purchaseTypeId") or "-100"
    result = {
        "startDate": f"{start_date} 00:00:00",
        "endDate": f"{end_date} 23:59:59",
        "pageId": page_id,
        "pageNumber": page_number,
        "searchType": 1,
        "keyword": keyword,
        "excludeKW": "",
        "inCludeKW": "",
        "projectClassID": str(project_class_ids),
        "searchMode": 1,
        "areaCode": {
            "proviceCodeList": area.get("proviceCodeList", []),
            "cityCodeList": area.get("cityCodeList", []),
            "countyCodeList": area.get("countyCodeList", []),
        },
        "industryCode": {
            "firstCodeList": join_unique(first_codes),
            "secondCodeList": join_unique(second_codes),
            "thirdCodeList": join_unique(third_codes),
        },
        "contractEndMin": "",
        "contractEndMax": "",
        "purchaseTypeID": str(purchase_type_id),
        "partAName": "",
        "partBName": "",
        "agentName": "",
        "projectMoneyMin": condition.get("projectMoneyMin"),
        "projectMoneyMax": condition.get("projectMoneyMax"),
        "fileFlag": -1,
        "companyName": condition.get("enterpriseName") or "",
        "_unsupportedFields": [],
    }
    if condition.get("subcontractFlag") is not None:
        result["_unsupportedFields"].append("subcontractFlag")
    return result


def main() -> int:
    """读取 AI 结果、编译普通搜索请求并输出 JSON。"""
    args = parse_args()
    try:
        data = read_json(args.input)
        result = compile_condition(data, args.page_id, args.page_number)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    separators = None if args.pretty else (",", ":")
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, separators=separators))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
