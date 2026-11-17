"""scripts/searxng_client.py - SearXNG 元搜索连接器（B9，§5.8）。

消费自托管 SearXNG 实例的 /search?format=json 结构化结果，免去逐引擎 CSS 解析
（Baidu/Sogou/Bing/DDG 的 selector 维护由 SearXNG 服务端完成）。须由用户本地起实例
（README §4 Docker 命令）并在 config.searxng.url 填地址；本模块不假设 Docker/网络可达，
失败隔离（B5）由 connector.load 包裹。

注意：SearXNG 公共实例会被 Google/Bing 限流验证码，须用私有实例（selfhostedguides.com 实证
私有低频实例基本不被验证码）。
"""

import json
import urllib.parse
from typing import Any, Dict, List

from common import load_config as _load_cfg


def _classify(url: str) -> str:
    try:
        from search import classify_source_type

        return classify_source_type(url)
    except Exception:
        return "unknown"


def fetch(
    query: str, cfg: Dict[str, Any] = None, max_results: int = 8, web_fetch: Any = None
) -> List[Dict[str, Any]]:
    """向 SearXNG 实例查询并返回 SERP doc 列表（结构与 search.fetch 一致）。

    传输层走系统 curl 子进程（与 finance/github 一致，绕过 TLS 指纹封禁）；
    SearXNG 主传输失败时若 web_fetch 注入则兜底抓实例 JSON 页。
    """
    cfg = _load_cfg(cfg)
    sx = cfg.get("searxng", {})
    base = (sx.get("url") or "").rstrip("/")
    if not base:
        return []
    url = f"{base}/search?q={urllib.parse.quote(query)}&format=json"
    try:
        import scrape as _scrape

        status, body, _ = _scrape._fetch_system_curl(url, _scrape._coherent_headers(), None, 15)
        if status != 200 or not body:
            raise RuntimeError("searxng non-200/empty")
        data = json.loads(body)
    except Exception:
        if web_fetch:
            try:
                html = web_fetch(url)
                if html:
                    return [
                        {
                            "url": url,
                            "title": query,
                            "snippet": str(html)[:200],
                            "raw_html": None,
                            "engine": "SearXNG",
                            "source_type": "searxng-web",
                        }
                    ]
            except Exception:
                pass
        return []
    docs: List[Dict[str, Any]] = []
    for item in (data.get("results") or [])[:max_results]:
        link = (item.get("url") or item.get("link") or "").strip()
        if not link.startswith("http"):
            continue
        docs.append(
            {
                "url": link,
                "title": item.get("title", "") or "",
                "snippet": item.get("content") or item.get("snippet") or "",
                "raw_html": None,
                "engine": "SearXNG",
                "source_type": _classify(link),
            }
        )
    return docs
