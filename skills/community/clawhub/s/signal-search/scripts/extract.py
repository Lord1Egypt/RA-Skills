"""scripts/extract.py - 正文抽取（§5.5 / D9 / M12）。trafilatura 优先，bs4/markdownify 兜底。"""

import re
from typing import Any, Dict, List

from common import load_config as _load_cfg

# 逐站点正文选择器（T4 校准）：命中则用 bs4 select 精准抽正文，回退通用抽取。
# 仅列"通用抽取（trafilatura）易失准/漏抓"的高价值站点；未列出的站点走通用链路。
SITE_SELECTORS = {
    "arxiv.org": "blockquote.abstract, div.abstract",
    "en.wikipedia.org": "div.mw-parser-output",
    "zh.wikipedia.org": "div.mw-parser-output",
    "github.com": "article.entry-content, div.Box-body",
    "stackoverflow.com": "div.s-prose",
    "news.ycombinator.com": "div.comment-tree",
    "pubmed.ncbi.nlm.nih.gov": "div.abstract-content",
    "docs.python.org": "div.body > div.section, div.document",
}


def _domain(url: str) -> str:
    m = re.search(r"https?://([^/]+)", url or "")
    return m.group(1).lower() if m else ""


def _extract_site(html: str, domain: str) -> str:
    """站点特定选择器优先抽正文；未命中或异常回退空串（交上层通用抽取）。"""
    sel = SITE_SELECTORS.get(domain)
    if not sel:
        return ""
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html or "", "lxml")
        parts = [t.get_text(" ", strip=True) for t in soup.select(sel)]
        text = "\n".join(p for p in parts if p).strip()
        return re.sub(r"[ \t]+", " ", re.sub(r"\n{3,}", "\n\n", text)).strip()
    except Exception:
        return ""


def _title(html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", html or "", re.S | re.I)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()[:120]
    return ""


def extract(doc: Dict[str, Any], cfg=None) -> Dict[str, Any]:
    """抽取 doc['raw_html'] → doc['text'/'title'/'snippet']；失败也不抛（B5）。"""
    html = doc.get("raw_html")
    if not html:
        doc.setdefault("snippet", "")
        doc.setdefault("title", "")
        doc.setdefault("text", "")
        return doc
    cfg = _load_cfg(cfg)
    truncate = (cfg.get("extract") or {}).get("truncate_chars", 800)

    text = ""
    # T4：站点特定选择器优先抽正文（精准），失败回退通用抽取
    dom = _domain(doc.get("url") or "")
    if dom:
        site_text = _extract_site(html, dom)
        if site_text:
            text = site_text
    if not text:
        try:
            import trafilatura

            ext = trafilatura.extract(html, include_comments=False, include_tables=False)
            if ext:
                text = ext
        except Exception:
            pass
    if not text:
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(html, "lxml")
            for t in soup(["script", "style", "noscript"]):
                t.decompose()
            text = soup.get_text("\n")
        except Exception:
            try:
                import markdownify

                text = markdownify.markdownify(html)
            except Exception:
                text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"[ \t]+", " ", re.sub(r"\n{3,}", "\n\n", text)).strip()
    doc["text"] = text
    doc["title"] = _title(html) or text[:40]
    doc["snippet"] = text[:truncate]
    return doc


# 搜索引擎自身域名（站内导航/相关搜索落在此类 host，属"非结果"链接，应剔除）
_SERP_HOSTS = {
    "baidu.com",
    "www.baidu.com",
    "cn.bing.com",
    "www.bing.com",
    "bing.com",
    "sogou.com",
    "www.sogou.com",
    "weixin.sogou.com",
    "duckduckgo.com",
    "html.duckduckgo.com",
    "google.com",
    "www.google.com",
    "google.com.hk",
    "so.com",
    "360.com",
    "so.toutiao.com",
    "jisilu.cn",
}

# 各引擎结果容器的专属 CSS 选择器（自然结果标题链接）。百度/搜狗结果走同域重定向器
# （/link?url=...）或协议相对链接（//host/...），故选择器不限定 href^='http'，由 _norm_href
# 统一归一化为绝对 URL；Bing/DuckDuckGo/Google 取跨域直链。无选择器或命中为空时回退通用过滤。
_ENGINE_RESULT_SELECTORS = {
    "Baidu": "div[class*='c-container'] h3 a",
    "BingCN": "li.b_algo h2 a",
    "BingINT": "li.b_algo h2 a",
    "DuckDuckGo": "a.result__a",
    "Sogou": "div.vrwrap h3 a, div.rb h3 a",
    "Google": "div.g a h3",
    "GoogleHK": "div.g a h3",
}


def _norm_href(href: str, serp_url: str = "") -> str:
    """结果链接归一化为绝对 URL：
    - 绝对 http(s) 原样保留；
    - 协议相对 //host/... → https://host/...；
    - 同域相对 /link?... 或 /path → 拼 SERP host（serp_url 提供），使搜索引擎重定向器
      可被跟进到真实落地页（_is_redirector 据此继承 SERP 豁免）。
    返回 None 表示无法归一化（如 javascript:/#/mailto:）。
    """
    href = (href or "").strip()
    if not href:
        return None
    if href.startswith("http"):
        return href
    if href.startswith("//"):
        return "https:" + href
    if href.startswith("/"):
        try:
            from urllib.parse import urlparse

            host = urlparse(serp_url or "").netloc
            if host:
                return f"https://{host}{href}"
        except Exception:
            pass
    return None


def is_serp_host(url: str) -> bool:
    """落地页若仍落在搜索引擎自身域名，说明 /link 重定向进了其门户/新闻页，非真实答案源。"""
    try:
        from urllib.parse import urlparse

        return urlparse(url or "").netloc.lower() in _SERP_HOSTS
    except Exception:
        return False


def parse_serp_links(
    html: str, engine: str = "", cfg=None, max_links: int = 8, serp_url: str = ""
) -> List[str]:
    """从 SERP HTML 解析结果落地页链接（两跳第一跳→第二跳的候选）。

    优先用引擎专属 CSS 选择器定位自然结果标题链接（百度/搜狗为 /link 重定向器，Bing/DDG 为跨域直链）；
    无专属选择器或命中为空时回退通用跨域过滤。返回前 max_links 个、去重保序。
    """
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html or "", "lxml")
        cand: List[str] = []
        sel = _ENGINE_RESULT_SELECTORS.get(engine)
        if sel:
            for a in soup.select(sel):
                u = _norm_href(a.get("href"), serp_url)
                if u:
                    cand.append(u)
        if not cand:
            cand = _generic_result_links(soup, serp_url)
        out, seen = [], set()
        for u in cand:
            if u in seen:
                continue
            seen.add(u)
            out.append(u)
            if len(out) >= max_links:
                break
        return out
    except Exception:
        return []


def _generic_result_links(soup, serp_url: str) -> List[str]:
    """无专属选择器时的兜底：剔搜索引擎同域导航/站内链接，保留重定向器与跨域直链。"""
    from urllib.parse import urlparse

    serp_hosts = set(_SERP_HOSTS)
    if serp_url:
        try:
            serp_hosts.add(urlparse(serp_url).netloc.lower())
        except Exception:
            pass
    REDIRECT = ("/link?", "/url?", "/link/", "/url/", "/jump?", "/redirect?", "/ck/")
    out = []
    for a in soup.find_all("a", href=True):
        u = _norm_href(a["href"], serp_url)
        if not u:
            continue
        try:
            host = urlparse(u).netloc.lower()
        except Exception:
            continue
        low = u.lower()
        if host in serp_hosts and not any(r in low for r in REDIRECT):
            continue
        if any(
            j in low
            for j in ("/s?", "/search?", "/web?", "robots.txt", "javascript:", "mailto:", "#")
        ):
            continue
        out.append(u)
    return out


def clean_links(html: str) -> List[str]:
    """抽取外链并剔除蜜罐（父链含 display:none / visibility:hidden / hidden 的 <a>，M16）。"""
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html or "", "lxml")
        out = []
        for a in soup.find_all("a", href=True):
            el = a
            hidden = False
            for _ in range(4):
                if el is None:
                    break
                style = (el.get("style") or "").lower()
                # 精确蜜罐判定：仅 display:none / visibility:hidden 样式，或 [hidden] 属性（D3）。
                # 排除 overflow:hidden 等极常见的正常 CSS，避免误杀合法外链。
                if (
                    "display:none" in style
                    or "visibility:hidden" in style
                    or el.get("hidden") is not None
                ):
                    hidden = True
                    break
                el = el.parent
            if hidden:
                continue  # 蜜罐不跟
            href = a["href"].strip()
            if href.startswith("http"):
                out.append(href)
        # 去重保序
        seen, uniq = set(), []
        for h in out:
            if h not in seen:
                seen.add(h)
                uniq.append(h)
        return uniq
    except Exception:
        return []
