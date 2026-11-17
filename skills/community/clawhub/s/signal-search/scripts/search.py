"""scripts/search.py - 引擎抓取层（§5.3 / D11）。拼 URL + 调 scrape；不裸发 HTTP。"""

import urllib.parse
from typing import Any, Dict, List

from common import load_config as _load_config


def _all_engines(cfg: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    out = {}
    for grp in ("cn", "global", "academic"):
        for e in cfg["engines"].get(grp, []):
            out[e["id"]] = e
    for dom, lst in cfg["engines"].get("vertical", {}).items():
        for e in lst:
            out[e["id"]] = e
    return out


# 学术源白名单：即便挂在 .gov / 通用域下，也应判为 academic（先专后泛，避免被裸 "gov" 误吞）。
# 匹配针对 URL 的 host（netloc）做精确子串判定，降低路径误命中。
ACADEMIC_HOSTS = (
    "arxiv",
    "scholar.google.",
    "cnki",
    "wanfang",
    "pubmed",
    "ncbi.nlm.nih.gov",
    "nlm.nih.gov",
    "doi.org",
    "crossref.org",
    "semanticscholar.org",
    "researchgate.net",
    "ieee.org",
    "acm.org",
    "springer.com",
    "wiley.com",
    "sciencedirect.com",
    "nature.com",
    "biorxiv.org",
    "medrxiv.org",
    "ssrn.com",
    "jstor.org",
)


def _host_of(url: str) -> str:
    try:
        return (urllib.parse.urlparse(url).netloc or url).lower()
    except Exception:
        return url.lower()


def _map_type(url: str) -> str:
    host = _host_of(url)
    low = url.lower()
    # 先专：已知学术库（含挂在 .gov 下的 NCBI / NLM / PubMed）按 host 精确白名单优先判 academic
    if any(h in host for h in ACADEMIC_HOSTS):
        return "academic"
    # 泛化 gov / 官媒：学术白名单已先判定，故不会吞掉学术 .gov 站
    if "gov" in low or "people.com" in low or "news.cn" in low:
        return "gov"
    if "weibo" in low or "zhihu" in low or "toutiao" in low or "mp.weixin" in low:
        return "selfmedia"
    if "stackoverflow" in low or "tieba" in low or "forum" in low:
        return "forum"
    return "unknown"


def classify_source_type(url: str) -> str:
    """公开封装：落地页域名 → source_type（供 deepfetch 复算 credibility）。"""
    return _map_type(url)


def fetch(
    engine_id: str, query: str, freshness: str = "中", cfg: Dict[str, Any] = None
) -> List[Dict[str, Any]]:
    """拼引擎 URL 并委托 scrape.scrape 拉取；失败返回 [] 不抛（B5）。"""
    cfg = cfg or _load_config()
    engines = _all_engines(cfg)
    e = engines.get(engine_id)
    if not e:
        return []
    url = e["search_url"].format(q=urllib.parse.quote(query))
    try:
        from scrape import scrape

        html, meta = scrape(url, {"engine": engine_id, "freshness": freshness, "cfg": cfg})
    except Exception:
        return []
    if html is None:
        return []
    src_type = _map_type(url)
    return [
        {
            "url": url,
            "raw_html": html,
            "title": "",
            "fetched_at": "",
            "engine": engine_id,
            "source_type": src_type,
        }
    ]
