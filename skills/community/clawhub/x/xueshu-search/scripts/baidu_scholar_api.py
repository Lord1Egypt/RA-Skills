#!/usr/bin/env python3
"""
Baidu Scholar (百度学术) API wrapper via Qianfan (千帆) platform.
Docs: https://cloud.baidu.com/doc/qianfan/s/Amkw9qpzd
Free tier: 50 calls/day.

Setup:
  1. Register at https://console.bce.baidu.com/qianfan/ais/console/apiKey
  2. Create API Key (bce-v3/ALTAK-xxx format, permanent)
  3. Set env var: export BAIDU_QIANFAN_API_KEY="bce-v3/ALTAK-xxx"

Without API Key: skip this source, use other sources instead.
"""

import os
import urllib.request
import urllib.parse
import json
import time
from typing import Optional

BAIDU_SCHOLAR_API = "https://qianfan.baidubce.com/v2/tools/baidu_scholar/search"
API_KEY = os.environ.get("BAIDU_QIANFAN_API_KEY", "")


def _is_available() -> bool:
    """Check if Baidu Scholar API is configured."""
    return bool(API_KEY)


def _make_request(url: str) -> dict:
    if not _is_available():
        return {"error": "no_key", "message": "BAIDU_QIANFAN_API_KEY not set. Get one at https://console.bce.baidu.com/qianfan/ais/console/apiKey"}

    time.sleep(0.5)
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"error": str(e.code), "message": body[:300]}
    except Exception as e:
        return {"error": "exception", "message": str(e)}


def _parse_item(item: dict) -> dict:
    pub_info = item.get("publishInfo", {}) or {}
    return {
        "source": "baidu_scholar",
        "id": item.get("paperId", ""),
        "title": item.get("title", ""),
        "authors": [],
        "abstract": item.get("aiAbstract", "") or item.get("abstract", ""),
        "year": item.get("publishYear"),
        "published": str(item.get("publishYear", "")),
        "doi": item.get("doi", ""),
        "url": item.get("url", ""),
        "pdf_url": "",
        "citation_count": None,
        "venue": pub_info.get("journalName", ""),
        "categories": [],
    }


def search(
    query: str,
    max_results: int = 10,
    page: int = 0,
    enable_ai_abstract: bool = True,
) -> list[dict]:
    """Search Baidu Scholar for papers (primarily Chinese literature).

    Args:
        query: Search keyword (supports Chinese and English).
        max_results: Max results (default 10). Note: the API returns a fixed page size.
        page: Page number, starting from 0.
        enable_ai_abstract: Use AI to generate smart summaries (default True).

    Returns:
        List of paper dicts. Returns empty list if API key not configured.
    """
    if not _is_available():
        return []

    params = {
        "wd": query,
        "pageNum": str(page),
    }
    if enable_ai_abstract:
        params["enable_ai_abstract"] = "true"

    url = f"{BAIDU_SCHOLAR_API}?{urllib.parse.urlencode(params)}"
    data = _make_request(url)

    if data.get("code") != "0" and "error" not in data:
        return []

    items = data.get("data", [])
    results = [_parse_item(item) for item in items]

    return results[:max_results]


def search_all_pages(query: str, max_results: int = 20) -> list[dict]:
    """Search multiple pages and aggregate results."""
    all_results = []
    page = 0
    while len(all_results) < max_results:
        batch = search(query, max_results=max_results - len(all_results), page=page)
        if not batch:
            break
        all_results.extend(batch)
        page += 1
        if len(batch) < 10:
            break
    return all_results[:max_results]
