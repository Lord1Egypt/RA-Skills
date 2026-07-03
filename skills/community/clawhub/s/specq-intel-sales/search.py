"""
search.py — SpecQ v2.0 联网搜索模块
Brave Search API 为主，无 API Key 时降级为 requests + BeautifulSoup
"""
import os


async def web_search(query: str, limit: int = 5, source: str = "web") -> dict:
    """
    联网搜索，返回结构化结果。

    source 取值:
      - "web": 通用网页搜索
      - "news": 新闻搜索
      - "scholar": 学术搜索（使用 web endpoint + 关键词强化）

    Brave Search API:
      URL: https://api.search.brave.com/res/v1/{source}/search
      Header: Accept: application/json
              X-Subscription-Token: {SEARCH_API_KEY}

    Fallback: requests + BeautifulSoup Google 基础抓取（不返回结果，仅降级占位）
    """
    api_key = os.getenv("SEARCH_API_KEY", "")
    if not api_key:
        return _fallback_search(query, source)

    import httpx
    try:
        base = "https://api.search.brave.com/res/v1"
        endpoint = f"{base}/{source}/search" if source in ("web", "news") else f"{base}/web/search"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": api_key,
        }
        if source == "scholar":
            query = f"{query} (research OR paper OR scholar)"

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(endpoint, params={"q": query, "count": limit}, headers=headers)
            if resp.status_code != 200:
                return _fallback_search(query, source)

            data = resp.json()
            raw_results = data.get("web", {}).get("results", data.get("results", []))
            results = []
            for r in raw_results[:limit]:
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "snippet": r.get("description", r.get("snippet", "")),
                    "published": r.get("published", r.get("page_age", "")),
                })
            return {"results": results, "total": len(results), "source": source}
    except Exception as e:
        return {"results": [], "total": 0, "source": source, "error": str(e)}


def _fallback_search(query: str, source: str) -> dict:
    """降级搜索：返回空结果（不阻塞主流程）。"""
    return {
        "results": [],
        "total": 0,
        "source": source,
        "error": "SEARCH_API_KEY 未配置，联网搜索不可用。请设置 Brave Search API Key。",
    }
