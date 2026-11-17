"""scripts/academic.py - 学术源（arXiv API 取预印本元数据，D3 结构化引用）。

产品原生检索域：用户搜「论文 / 文献 / arXiv / DOI」时由 connector 路由到此，直接打
arXiv 公开 API（无需 key）取预印本元数据。

DOI 由调用方经 doi_resolver(arxiv_id)->str 回调注入（由调用方提供）：库内【不】内置任何书目源、
【不】读环境变量、【不】硬编码任何 API URL。调用方想拿真 DOI，就传自己的 resolver
（可以是 Semantic Scholar / Crossref / 自有库 / 任意）；未注入时 citation.doi 留空，
BibTeX 导出退化为 @misc（预印本本无 DOI，诚实退化，绝不伪造）。

注：arXiv API 不暴露 <arxiv:doi>，Crossref 对 arXiv 预印本 10.48550/arXiv.<id> 返回 404、
且其 bibliographic 模糊查会误命中无关文献（如 R 的 arxiv 包），故库不内置任何回填，全部交
由调用方 resolver 决定。

反爬：系统 curl 子进程（与 finance/github 一致，绕过 TLS 指纹封禁）；失败时若调用方
注入 `web_fetch` 则兜底抓 arXiv 网页，否则记 warning。
"""

import re
import xml.etree.ElementTree as ET
from typing import Any, Callable, Dict, List, Optional, Tuple
from urllib.parse import quote as _urlencode

import scrape

_ATOM_NS = "{http://www.w3.org/2005/Atom}"
_ARXIV_API = "http://export.arxiv.org/api/query"


def _arxiv_search(query: str, max_results: int = 10, timeout: int = 15) -> List[Dict[str, Any]]:
    """系统 curl 调 arXiv Atom API，解析 entry 为 source_type=academic 文档。"""
    url = f"{_ARXIV_API}?search_query=all:{_urlencode(query)}&start=0&max_results={max_results}"
    headers = scrape._coherent_headers()
    status, body, _ = scrape._fetch_system_curl(url, headers, None, timeout)
    if status != 200 or not body:
        return []
    try:
        root = ET.fromstring(body)
    except Exception:
        return []
    out: List[Dict[str, Any]] = []
    for entry in root.findall(f"{_ATOM_NS}entry"):
        title = (entry.findtext(f"{_ATOM_NS}title") or "").strip().replace("\n", " ")
        summary = (entry.findtext(f"{_ATOM_NS}summary") or "").strip()
        id_el = entry.find(f"{_ATOM_NS}id")
        link = (id_el.text or "").strip() if id_el is not None else ""
        authors = [
            a.findtext(f"{_ATOM_NS}name", "") or "" for a in entry.findall(f"{_ATOM_NS}author")
        ]
        published = entry.findtext(f"{_ATOM_NS}published") or ""
        year = published[:4] if published else "n.d."
        if not link:
            continue
        slug_key = re.sub(r"[^a-z0-9]", "", link.lower())[:14] or "arxiv"
        arxiv_id = _parse_arxiv_id(link)
        out.append(
            {
                "url": link,
                "title": title,
                "text": f"{title}\n\n{summary}",
                "snippet": summary[:200],
                "engine": "arxiv",
                "source_type": "academic",
                "landing_resolved": True,
                "arxiv_id": arxiv_id,
                "citation": {
                    "key": f"arxiv-{slug_key}",
                    "authors": ", ".join(a for a in authors if a) or "unknown",
                    "year": year,
                    "source": "arxiv",
                    "doi": "",
                },
            }
        )
    return out


def _parse_arxiv_id(link: str) -> str:
    """从 arXiv abs 链接提取 arXiv id（新格式 1706.03762 / 旧格式 math.GT/0309136）。"""
    m = re.search(r"arxiv\.org/abs/([0-9]{4}\.[0-9]{4,5})", link)
    if m:
        return m.group(1)
    m = re.search(r"arxiv\.org/abs/([a-z-]+/\d{7})", link)
    if m:
        return m.group(1)
    return ""


def search(
    query: str,
    cfg: Dict[str, Any] = None,
    web_fetch: Optional[Callable] = None,
    max_results: int = 10,
    doi_resolver: Optional[Callable[[str], str]] = None,
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """学术源检索。返回 (docs, warnings)。

    - arXiv API 取预印本；DOI 由调用方经 doi_resolver(arxiv_id)->str 注入（由调用方提供），
      命中即写入 citation.doi → BibTeX 升级 @article。未注入 / 返回空 → 退化为 @misc
      （预印本本无 DOI，绝不伪造）。
    - 主传输失败 → 若 web_fetch 注入则兜底抓 arXiv 搜索页；否则记 warning 返回空。
    """
    warnings: List[str] = []
    docs = _arxiv_search(query, max_results)

    # DOI 回填（由调用方提供）：仅当调用方注入 doi_resolver 才查；命中即写入 citation.doi。
    # 库内不内置任何书目源、不读环境变量、杜绝伪造 DOI（D3 DOI→@article 仅在真值时触发）。
    if docs and doi_resolver:
        for d in docs:
            aid = d.get("arxiv_id")
            if aid:
                try:
                    doi = doi_resolver(aid)
                    if doi:
                        d["citation"]["doi"] = doi
                except Exception:
                    pass

    if not docs:
        if web_fetch:
            try:
                page = f"https://arxiv.org/search/?searchtype=all&query={_urlencode(query)}"
                html = web_fetch(page)
                if html:
                    return [
                        {
                            "url": page,
                            "text": str(html),
                            "engine": "arxiv",
                            "source_type": "academic",
                            "landing_resolved": True,
                            "citation": {
                                "key": f"arxiv-{_urlencode(query)[:14]}",
                                "source": "arxiv-web",
                                "doi": "",
                            },
                        }
                    ], warnings
            except Exception:
                pass
        warnings.append("arXiv API 暂时不可用，且未注入 web_fetch 兜底，返回空结果")
    return docs, warnings
