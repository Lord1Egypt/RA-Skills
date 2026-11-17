"""
Dify Plugin - star-search tool
"""
import os
import json
import urllib.request

api_base = os.environ.get("STAR_SEARCH_BASE", "https://search.token-star.cn/v1")


def search(query: str, mode: str = "deep") -> dict:
    """执行搜索"""
    data = json.dumps({"query": query, "mode": mode, "top": 5}).encode()
    req = urllib.request.Request(
        f"{api_base}/search",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e)}
