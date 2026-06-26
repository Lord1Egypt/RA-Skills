#!/usr/bin/env python3

from __future__ import annotations

import csv
import json
import os
import urllib.request
from pathlib import Path

from runtime_config import load_runtime_env, require_em_api_key


MX_BASE_URL = "https://mkapi2.dfcfs.com/finskillshub/api/claw"
DEFAULT_HEADERS = {"Content-Type": "application/json"}


load_runtime_env()


def get_mx_api_key() -> str:
    return require_em_api_key(script_hint="python3 skill/uwillberich/scripts/runtime_config.py set-em-key --stdin")


def post_json(path: str, payload: dict, timeout: int = 30) -> dict:
    url = f"{MX_BASE_URL}/{path.lstrip('/')}"
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={**DEFAULT_HEADERS, "apikey": get_mx_api_key()},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def unwrap_response(payload: dict) -> dict:
    data = payload.get("data")
    while isinstance(data, dict) and "data" in data:
        next_data = data.get("data")
        if next_data is None:
            break
        data = next_data
    return data if isinstance(data, dict) else {}


def news_search(query: str, size: int | None = None) -> dict:
    payload = {"query": query}
    if size is not None:
        payload["size"] = size
    response = post_json("news-search", payload)
    data = unwrap_response(response)
    items = ((data.get("llmSearchResponse") or {}).get("data")) or []
    return {"query": query, "items": items, "raw": response}


def stock_screen(keyword: str, page_no: int = 1, page_size: int = 20) -> dict:
    payload = {"keyword": keyword, "pageNo": page_no, "pageSize": page_size}
    response = post_json("stock-screen", payload)
    data = unwrap_response(response)
    result = ((data.get("allResults") or {}).get("result")) or {}
    columns = result.get("columns") or []
    rows = result.get("dataList") or []
    return {
        "keyword": keyword,
        "title": data.get("title") or keyword,
        "response_code": data.get("responseCode"),
        "reflect_result": data.get("reflectResult"),
        "security_count": data.get("securityCount"),
        "conditions": data.get("responseConditionList") or [],
        "columns": columns,
        "rows": rows,
        "total": result.get("total") or len(rows),
        "raw": response,
    }


def data_query(tool_query: str) -> dict:
    response = post_json("query", {"toolQuery": tool_query})
    data = unwrap_response(response)
    result = data.get("searchDataResultDTO") or {}
    tables = result.get("dataTableDTOList") or []
    entities = result.get("entityTagDTOList") or []
    return {
        "tool_query": tool_query,
        "question_id": result.get("questionId"),
        "tables": tables,
        "entities": entities,
        "condition": result.get("condition") or {},
        "raw": response,
    }


def format_news_markdown(items: list[dict], limit: int = 5) -> str:
    lines = ["| Date | Source | Title | Type |", "| --- | --- | --- | --- |"]
    for item in items[:limit]:
        title = item.get("title") or ""
        url = item.get("jumpUrl") or ""
        linked_title = f"[{title}]({url})" if url else title
        lines.append(
            f"| {item.get('date', '')} | {item.get('source', '')} | {linked_title} | {item.get('informationType', '')} |"
        )
    return "\n".join(lines)


def csv_header(columns: list[dict]) -> list[str]:
    headers = []
    for column in columns:
        title = column.get("title") or column.get("key") or ""
        date_msg = column.get("dateMsg")
        if date_msg:
            title = f"{title}({date_msg})"
        headers.append(title)
    return headers


def csv_keys(columns: list[dict]) -> list[str]:
    return [column.get("key") or "" for column in columns]


def write_stock_screen_csv(columns: list[dict], rows: list[dict], path: str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    keys = csv_keys(columns)
    headers = csv_header(columns)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        for row in rows:
            writer.writerow([row.get(key, "") for key in keys])


def write_stock_screen_description(columns: list[dict], path: str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Stock Screen Columns", "", "| 标题 | 字段 key | 日期 | 单位 | 数据类型 |", "| --- | --- | --- | --- | --- |"]
    for column in columns:
        lines.append(
            f"| {column.get('title', '')} | {column.get('key', '')} | {column.get('dateMsg', '') or ''} | {column.get('unit', '') or ''} | {column.get('dataType', '') or ''} |"
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def format_stock_screen_markdown(columns: list[dict], rows: list[dict], limit: int = 10) -> str:
    keys = csv_keys(columns)
    header_map = dict(zip(keys, csv_header(columns)))
    preferred_matchers = [
        "SERIAL",
        "SECURITY_CODE",
        "SECURITY_SHORT_NAME",
        "MARKET_SHORT_NAME",
        "NEWEST_PRICE",
        "CHG",
        "PCHG",
        "010000_RPT_F10_ORG_BASICINFO_BOARD_NAME_TOTAL_BOARD_NAME_TOTAL_",
        "010000_TOAL_MARKET_VALUE",
        "010000_CIRCULATION_MARKET_VALUE",
    ]
    top_keys: list[str] = []
    for matcher in preferred_matchers:
        match = next((key for key in keys if key == matcher or key.startswith(matcher)), None)
        if match and match not in top_keys:
            top_keys.append(match)
    for key in keys:
        if key not in top_keys:
            top_keys.append(key)
        if len(top_keys) >= 8:
            break
    top_headers = [header_map[key] for key in top_keys]
    lines = ["| " + " | ".join(top_headers) + " |", "| " + " | ".join(["---"] * len(top_headers)) + " |"]
    for row in rows[:limit]:
        values = [str(row.get(key, "")) for key in top_keys]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def extract_latest_metrics(table: dict) -> list[dict]:
    metrics: list[dict] = []
    name_map = table.get("nameMap") or {}
    data_table = table.get("table") or {}
    dates = data_table.get("headName") or []
    as_of = dates[0] if dates else ""
    indicator_order = table.get("indicatorOrder") or []
    for key in indicator_order:
        if key == "headName":
            continue
        values = data_table.get(key) or []
        if not values:
            continue
        metrics.append(
            {
                "entity": table.get("entityName", ""),
                "metric": name_map.get(key, key),
                "latest": values[0],
                "as_of": as_of,
                "title": table.get("title", ""),
            }
        )
    return metrics


def format_data_query_markdown(tables: list[dict], limit: int = 12) -> str:
    metrics: list[dict] = []
    seen: set[tuple[str, str, str, str]] = set()
    for table in tables:
        for item in extract_latest_metrics(table):
            fingerprint = (item["entity"], item["metric"], str(item["latest"]), item["as_of"])
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            metrics.append(item)
    lines = ["| Entity | Metric | Latest | As Of |", "| --- | --- | --- | --- |"]
    for item in metrics[:limit]:
        lines.append(
            f"| {item['entity']} | {item['metric']} | {item['latest']} | {item['as_of']} |"
        )
    return "\n".join(lines)
