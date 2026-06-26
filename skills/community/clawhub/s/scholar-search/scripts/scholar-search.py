#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path
import xml.etree.ElementTree as ET

import requests

ARXIV_BASE_URL = "https://export.arxiv.org/api/query"
SEMANTIC_SCHOLAR_BASE_URL = "https://api.semanticscholar.org/graph/v1"
MISSING_VALUE = "缺失"
SUPPORTED_SOURCES = {"arxiv", "semantic_scholar"}
ARXIV_XML_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
}

_LAST_CALL_TS: Dict[str, float] = {"arxiv": 0.0, "semantic_scholar": 0.0}
_THROTTLE_LOCK = threading.Lock()

# 节流
def _throttle(source: str) -> None:
    import random
    min_interval_base = 3.0 if source == "arxiv" else 2.0
    # 在多实例同时打同一接口时，轻微抖动可降低“同秒打点”导致的瞬时峰值。
    min_interval = min_interval_base * (1 + random.uniform(0, 0.2))
    while True:
        with _THROTTLE_LOCK:
            last_ts = _LAST_CALL_TS.get(source, 0.0)
            now = time.monotonic()
            wait_seconds = min_interval - (now - last_ts)
            if wait_seconds <= 0:
                _LAST_CALL_TS[source] = now
                return
        time.sleep(wait_seconds)


def _is_supported_semantic_endpoint(endpoint: str) -> bool:
    normalized = endpoint.strip().rstrip("/")
    if not normalized:
        return False
    if normalized in {
        "paper/search",
        "paper/search/match",
        "paper/autocomplete",
        "snippet/search",
        "author/search",
    }:
        return True
    if normalized.startswith("paper/"):
        return True
    if normalized.startswith("author/"):
        return True
    return False


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _validate_semantic_params(endpoint: str, params: Dict[str, Any]) -> Optional[str]:
    if not _is_supported_semantic_endpoint(endpoint):
        return f"参数错误: 不支持的 endpoint: {endpoint}"

    if endpoint in {"paper/search", "paper/search/match", "paper/autocomplete", "snippet/search"}:
        query = params.get("query")
        if not isinstance(query, str) or not query.strip():
            return f"参数错误: {endpoint} 需要非空 query。"

    limit = params.get("limit")
    offset = params.get("offset", 0)
    if limit is None:
        return None

    limit_i = _safe_int(limit, -1)
    offset_i = _safe_int(offset, 0)
    if limit_i < 0:
        return "参数错误: limit 必须为非负整数。"
    if offset_i < 0:
        return "参数错误: offset 必须为非负整数。"

    if endpoint == "paper/search":
        if limit_i > 100:
            return "参数错误: paper/search 的 limit 必须 <= 100。"
        if offset_i + limit_i >= 1000:
            return "参数错误: paper/search 的 offset + limit 必须 < 1000。"

    if endpoint == "author/search":
        if limit_i > 1000:
            return "参数错误: author/search 的 limit 必须 <= 1000。"
        if offset_i + limit_i >= 10000:
            return "参数错误: author/search 的 offset + limit 必须 < 10000。"

    if endpoint.endswith("/references") or endpoint.endswith("/citations") or endpoint.endswith("/papers"):
        if limit_i > 1000:
            return "参数错误: references/citations/author papers 的 limit 必须 <= 1000。"

    return None


def _xml_text_or_missing(element: Optional[ET.Element]) -> str:
    if element is None or element.text is None:
        return MISSING_VALUE
    text = element.text.strip()
    return text if text else MISSING_VALUE


def _extract_arxiv_id(raw_entry_id: str) -> str:
    if raw_entry_id == MISSING_VALUE:
        return MISSING_VALUE
    if "arxiv.org/abs/" in raw_entry_id:
        return raw_entry_id.split("arxiv.org/abs/")[-1].rstrip("/")
    return raw_entry_id


def _normalize_published_date(published_str: str) -> str:
    if not published_str or published_str == MISSING_VALUE:
        return MISSING_VALUE
    try:
        dt = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return published_str[:10]


def _parse_arxiv_feed(feed_text: str) -> Dict[str, Any]:
    result: Dict[str, Any] = {"meta": {}, "entries": [], "error": None}
    try:
        root = ET.fromstring(feed_text)
    except ET.ParseError as exc:
        result["error"] = f"XML 解析失败: {exc}"
        return result

    result["meta"] = {
        "title": _xml_text_or_missing(root.find("atom:title", ARXIV_XML_NS)),
        "updated": _xml_text_or_missing(root.find("atom:updated", ARXIV_XML_NS)),
        "totalResults": _xml_text_or_missing(root.find("opensearch:totalResults", ARXIV_XML_NS)),
        "startIndex": _xml_text_or_missing(root.find("opensearch:startIndex", ARXIV_XML_NS)),
        "itemsPerPage": _xml_text_or_missing(root.find("opensearch:itemsPerPage", ARXIV_XML_NS)),
    }

    entries: List[Dict[str, Any]] = []
    for entry in root.findall("atom:entry", ARXIV_XML_NS):
        raw_entry_id = _xml_text_or_missing(entry.find("atom:id", ARXIV_XML_NS))
        arxiv_id = _extract_arxiv_id(raw_entry_id)
        primary_category = MISSING_VALUE
        primary_category_elem = entry.find("arxiv:primary_category", ARXIV_XML_NS)
        if primary_category_elem is not None:
            primary_category = (primary_category_elem.get("term") or "").strip() or MISSING_VALUE

        categories: List[str] = []
        for tag in entry.findall("atom:category", ARXIV_XML_NS):
            term = (tag.get("term") or "").strip()
            if term:
                categories.append(term)
        if primary_category == MISSING_VALUE and categories:
            primary_category = categories[0]

        pdf_url = MISSING_VALUE
        for link in entry.findall("atom:link", ARXIV_XML_NS):
            href = (link.get("href") or "").strip()
            if not href:
                continue
            link_type = (link.get("type") or "").strip()
            link_title = (link.get("title") or "").strip().lower()
            if link_type == "application/pdf" or link_title == "pdf":
                pdf_url = href
                break

        published_str = _xml_text_or_missing(entry.find("atom:published", ARXIV_XML_NS))
        published_date = _normalize_published_date(published_str)

        authors: List[str] = []
        for author in entry.findall("atom:author", ARXIV_XML_NS):
            author_name = _xml_text_or_missing(author.find("atom:name", ARXIV_XML_NS))
            if author_name != MISSING_VALUE:
                authors.append(author_name)

        entries.append({
            "arxiv_id": arxiv_id,
            "title": _xml_text_or_missing(entry.find("atom:title", ARXIV_XML_NS)),
            "authors": authors,
            "summary": _xml_text_or_missing(entry.find("atom:summary", ARXIV_XML_NS)),
            "published": published_date,
            "updated": _xml_text_or_missing(entry.find("atom:updated", ARXIV_XML_NS)),
            "primary_category": primary_category,
            "categories": categories,
            "pdf_url": pdf_url,
            "doi": _xml_text_or_missing(entry.find("arxiv:doi", ARXIV_XML_NS)),
            "journal_ref": _xml_text_or_missing(entry.find("arxiv:journal_ref", ARXIV_XML_NS)),
            "comment": _xml_text_or_missing(entry.find("arxiv:comment", ARXIV_XML_NS)),
            "raw_entry_id": raw_entry_id,
        })

    result["entries"] = entries
    result["meta"]["count_returned"] = len(entries)
    return result


def execute_scholar_search(
    source: str,
    endpoint: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None,
    timeout: int = 20,
) -> Dict[str, Any]:
    if source not in SUPPORTED_SOURCES:
        return {"error": "无效源: 只支持 arxiv 或 semantic_scholar"}
    params = params or {}

    # arXiv -----------------
    if source == "arxiv":
        _throttle("arxiv")
        try:
            response = requests.get(ARXIV_BASE_URL, params=params, timeout=timeout)
            if response.status_code == 429:
                return {"error": "请求过于频繁: arXiv 返回 429，请稍后重试。", "tried_params": params}
            response.raise_for_status()
            result = _parse_arxiv_feed(response.text)
            if result["error"]:
                return {"error": result["error"], "tried_params": params}
            return result
        except requests.exceptions.RequestException as exc:
            status_code = exc.response.status_code if exc.response is not None else "未知"
            return {"error": f"HTTP 错误: {status_code}, 消息: {exc}", "tried_params": params}
    
    # semantic scholar -----------------
    if endpoint is None:
        return {"error": "Semantic Scholar 需要 endpoint"}

    validation_error = _validate_semantic_params(endpoint, params)
    if validation_error:
        return {"error": validation_error, "tried_params": params}

    url = f"{SEMANTIC_SCHOLAR_BASE_URL}/{endpoint}"
    headers = {"Accept": "application/json"}
    if api_key:
        headers["x-api-key"] = api_key

    _throttle("semantic_scholar")
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        if response.status_code == 429:
            return {"error": "请求过于频繁: Semantic Scholar 返回 429，请稍后重试。", "tried_params": params}
        response.raise_for_status()
        try:
            data = response.json()
        except ValueError:
            return {"error": "响应解析失败: 不是合法 JSON", "raw_text": response.text[:500]}
        # 直接透传 S2 官方返回，避免额外格式化引入结构偏差。
        return data
    except requests.exceptions.RequestException as exc:
        status_code = exc.response.status_code if exc.response is not None else "未知"
        return {"error": f"HTTP 错误: {status_code}, 消息: {exc}", "tried_params": params}

def _parse_json_arg(raw: Optional[str], arg_name: str) -> Dict[str, Any]:
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{arg_name} 不是合法 JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{arg_name} 必须是 JSON 对象")
    return value


def _read_s2_api_key_from_dotenv(env_path: Path) -> Optional[str]:
    if not env_path.is_file():
        return None

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key != "S2_API_KEY":
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        return value or None
    return None


def _resolve_s2_api_key(env_path: Path) -> Optional[str]:
    # 优先读取进程环境变量，便于在 CI/平台侧通过注入环境变量使用。
    env_value = (os.getenv("S2_API_KEY") or "").strip()
    if env_value:
        return env_value
    return _read_s2_api_key_from_dotenv(env_path)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified scholar search for arXiv and Semantic Scholar")
    parser.add_argument("--source", choices=["arxiv", "semantic_scholar"], required=True)
    parser.add_argument("--endpoint", help="Semantic Scholar endpoint, e.g. paper/search")
    parser.add_argument("--params", help="JSON object string for query params", default="{}")
    parser.add_argument("--timeout", type=int, default=20, help="HTTP timeout in seconds")
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    try:
        params = _parse_json_arg(args.params, "--params")
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1

    api_key: Optional[str] = None
    if args.source == "semantic_scholar":
        api_key = _resolve_s2_api_key(Path(__file__).resolve().parent / ".env")
        if api_key is None:
            print(json.dumps({"error": "S2_API_KEY 未设置（semantic_scholar搜索可能会被限速或限流）"}, ensure_ascii=False))
            
    result = execute_scholar_search(
        source=args.source,
        endpoint=args.endpoint,
        params=params,
        api_key=api_key,
        timeout=args.timeout,
    )

    try:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except UnicodeEncodeError:
    # Windows 某些终端默认 GBK，无法编码部分 Unicode 字符时回退为转义输出。
        print(json.dumps(result, indent=2, ensure_ascii=True))
    return 1 if result.get("error") else 0


if __name__ == "__main__":
    raise SystemExit(main())
