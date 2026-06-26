"""
ClawHub 搜索模块
搜索 ClawHub 上新发布的 Skills（指定时间范围内）

API endpoint: https://clawhub.ai/api/search?q=<keyword>
已知字段: score, slug, displayName, summary, version, updatedAt
"""

import json
import logging
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

# 尝试导入 requests，不可用时回退到 urllib
try:
    import requests as _requests
    _USE_REQUESTS = True
except ImportError:
    _USE_REQUESTS = False
    import urllib.request
    import urllib.parse
    import urllib.error

API_BASE = "https://clawhub.ai/api"
SEARCH_ENDPOINTS = [
    f"{API_BASE}/search",
    f"{API_BASE}/skills",
    f"{API_BASE}/skills/search",
]

# ClawHub 网站 URL 前缀
SKILL_URL_PREFIX = "https://clawhub.com/skills/"


def _http_get(url: str, params: dict | None = None, timeout: int = 15) -> dict | list | None:
    """发起 HTTP GET 请求，返回 JSON 或 None"""
    try:
        if _USE_REQUESTS:
            resp = _requests.get(url, params=params, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        else:
            if params:
                qs = urllib.parse.urlencode(params)
                url = f"{url}?{qs}"
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "spec-engine/1.0", "Accept": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        logger.debug("HTTP GET %s failed: %s", url, e)
        return None


def _parse_result(item: dict) -> dict:
    """将 API 返回的单条结果转换为标准格式"""
    slug = item.get("slug", "")
    summary = item.get("summary", "") or item.get("description", "")
    if len(summary) > 200:
        summary = summary[:200] + "..."

    updated_ts = item.get("updatedAt")
    updated_str = ""
    if updated_ts and isinstance(updated_ts, (int, float)):
        try:
            dt = datetime.fromtimestamp(updated_ts / 1000, tz=timezone.utc)
            updated_str = dt.strftime("%Y-%m-%d %H:%M UTC")
        except (OSError, ValueError):
            pass

    return {
        "title": item.get("displayName") or item.get("name") or slug,
        "url": f"{SKILL_URL_PREFIX}{slug}" if slug else "",
        "author": item.get("author") or item.get("publisher") or "",
        "description": summary,
        "version": item.get("version") or "",
        "downloads": item.get("downloads") or item.get("downloadCount") or 0,
        "updated_at": updated_str,
        "slug": slug,
        "_updatedAt_ms": updated_ts,  # 内部字段，用于时间过滤
    }


def _search_api(keyword: str, limit: int = 50) -> list[dict]:
    """尝试多个 API endpoint 搜索"""
    params = {"q": keyword, "limit": str(limit)}

    for endpoint in SEARCH_ENDPOINTS:
        data = _http_get(endpoint, params=params)
        if data is None:
            continue

        # 兼容不同响应格式
        if isinstance(data, dict):
            results = data.get("results") or data.get("skills") or data.get("data") or []
        elif isinstance(data, list):
            results = data
        else:
            continue

        if results and isinstance(results, list):
            logger.info("ClawHub API 返回 %d 条结果 (endpoint: %s)", len(results), endpoint)
            return [_parse_result(item) for item in results if isinstance(item, dict)]

    logger.warning("所有 ClawHub API endpoint 均无结果")
    return []


def collect(keyword: str = "openclaw", hours: int = 24) -> dict:
    """
    搜索 ClawHub 上新发布的 Skills

    Args:
        keyword: 搜索关键词
        hours: 时间范围（小时），过滤 updatedAt 在此范围内的结果

    Returns:
        {
            "source": "clawhub",
            "items": [...],
            "total": int,
            "query_time": "YYYY-MM-DD HH:MM"
        }
    """
    query_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    items = _search_api(keyword)

    # 按时间过滤
    if hours > 0 and items:
        cutoff = datetime.now(tz=timezone.utc) - timedelta(hours=hours)
        cutoff_ms = int(cutoff.timestamp() * 1000)
        filtered = []
        for item in items:
            ts = item.get("_updatedAt_ms")
            # 没有时间信息则保留；有时间信息则检查是否在范围内
            if ts is None or (isinstance(ts, (int, float)) and ts >= cutoff_ms):
                filtered.append(item)
        items = filtered

    # 清理内部字段
    for item in items:
        item.pop("_updatedAt_ms", None)

    result = {
        "source": "clawhub",
        "items": items,
        "total": len(items),
        "query_time": query_time,
    }

    logger.info(
        "ClawHub 搜索完成: keyword=%s, hours=%d, found=%d",
        keyword, hours, len(items),
    )
    return result


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    print("=" * 60)
    print("ClawHub 搜索模块测试")
    print("=" * 60)

    # 测试 1: 基本搜索
    print("\n[测试1] 搜索 'openclaw'（不限时间）")
    result = collect(keyword="openclaw", hours=0)
    print(f"  找到 {result['total']} 条结果")
    for i, item in enumerate(result["items"][:5], 1):
        print(f"  {i}. {item['title']} | v{item['version'] or 'N/A'} | 更新: {item['updated_at'] or 'N/A'}")
        print(f"     {item['url']}")

    # 测试 2: 带时间过滤
    print("\n[测试2] 搜索 'openclaw'（24小时内更新）")
    result24 = collect(keyword="openclaw", hours=24)
    print(f"  找到 {result24['total']} 条结果")
    for i, item in enumerate(result24["items"][:5], 1):
        print(f"  {i}. {item['title']} | 更新: {item['updated_at'] or 'N/A'}")

    # 测试 3: 输出完整 JSON
    print("\n[测试3] 完整结果 JSON（前3条）")
    display = {**result, "items": result["items"][:3]}
    print(json.dumps(display, indent=2, ensure_ascii=False))

    print("\n✅ 测试完成")
