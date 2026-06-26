#!/usr/bin/env python3
"""SearXNG-lite: 轻量多引擎聚合搜索插件。

单文件，热加载 config.yml 分类配置，并发搜索，JSON 输出。
依赖：系统 Python + httpx + lxml（macOS 默认已有）。

用法:
    python3 search.py "query"                          # 默认引擎
    python3 search.py "query" -c dev                   # 按分类搜
    python3 search.py "query" -c dev,academic          # 多分类
    python3 search.py "query" -e github,arxiv          # 指定引擎
    python3 search.py "query" --all                    # 所有启用的引擎
    python3 search.py "query" --compact                # 紧凑输出
    python3 search.py --list                           # 列出所有引擎和分类
"""

import argparse
import base64
import json
import logging
import os
import random
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Any
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx
import lxml.html

log = logging.getLogger("sxng")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SKILL_DIR, "config.yml")

# ── User-Agent ─────────────────────────────────────────────────

_UA_TEMPLATES = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36",
]

def _ua() -> str:
    return random.choice(_UA_TEMPLATES).format(v=random.randint(120, 136))

def _headers(lang: str = "en") -> dict[str, str]:
    return {
        "User-Agent": _ua(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": f"{lang},{lang.split('-')[0]};q=0.9,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1", "Connection": "keep-alive", "Cache-Control": "no-cache",
    }

# ── 引擎实现 ───────────────────────────────────────────────────
#
# 每个引擎函数签名: (query, client, lang, page, **_) -> list[dict]
# 返回: [{"title": ..., "url": ..., "content": ..., "engine": ...}, ...]

# ── 通用搜索 ──

def _bing(query: str, client: httpx.Client, lang: str = "en", page: int = 1, **_) -> list[dict]:
    params = {"q": query}
    if page > 1:
        params["first"] = str((page - 1) * 10 + 1)
    resp = client.get("https://www.bing.com/search", params=params, headers=_headers(lang), follow_redirects=True, timeout=10)
    resp.raise_for_status()
    dom = lxml.html.fromstring(resp.text)
    results = []
    for item in dom.xpath('//ol[@id="b_results"]/li[contains(@class, "b_algo")]'):
        link = item.xpath(".//h2/a")
        if not link:
            continue
        href, title = link[0].get("href", ""), link[0].text_content().strip()
        if not href or not title:
            continue
        if href.startswith("https://www.bing.com/ck/a?"):
            qs = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
            u = qs.get("u", [""])[0]
            if u.startswith("a1"):
                try:
                    href = base64.urlsafe_b64decode(u[2:] + "=" * (-len(u[2:]) % 4)).decode("utf-8", errors="replace")
                except Exception:
                    pass
        for p in item.xpath(".//p"):
            for icon in p.xpath('.//span[@class="algoSlug_icon"]'):
                icon.getparent().remove(icon)
        content = item.xpath(".//p")[0].text_content().strip() if item.xpath(".//p") else ""
        results.append({"title": title, "url": href, "content": content, "engine": "bing"})
    return results

def _brave(query: str, client: httpx.Client, lang: str = "en", page: int = 1, **_) -> list[dict]:
    params = {"q": query, "source": "web"}
    if page > 1:
        params["offset"] = str((page - 1) * 10)
    resp = client.get("https://search.brave.com/search", params=params, headers=_headers(lang), follow_redirects=True, timeout=10)
    resp.raise_for_status()
    dom = lxml.html.fromstring(resp.text)
    results = []
    for item in dom.xpath("//div[contains(@class, 'snippet ')]"):
        a = item.xpath(".//a[contains(@class, 'heading')]") or item.xpath(".//a[@href]")
        if not a:
            continue
        url, title = a[0].get("href", ""), a[0].text_content().strip()
        desc = item.xpath(".//p")
        content = desc[0].text_content().strip() if desc else ""
        if url and title and url.startswith("http"):
            results.append({"title": title, "url": url, "content": content, "engine": "brave"})
    return results

def _duckduckgo(query: str, client: httpx.Client, lang: str = "en", **_) -> list[dict]:
    if len(query) >= 500:
        return []
    headers = _headers(lang)
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"
    headers["Referer"] = "https://html.duckduckgo.com/"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    resp = client.post("https://html.duckduckgo.com/html", data={"q": query, "b": "", "kl": "wt-wt"},
                        headers=headers, follow_redirects=True, timeout=10)
    resp.raise_for_status()
    doc = lxml.html.fromstring(resp.text)
    if doc.xpath("//form[@id='challenge-form']"):
        log.warning("DuckDuckGo: CAPTCHA")
        return []
    results = []
    for div in doc.xpath('//div[@id="links"]/div[contains(@class, "web-result")]'):
        a = div.xpath(".//h2/a")
        if not a:
            continue
        title, url = a[0].text_content().strip(), a[0].get("href", "")
        snip = div.xpath('.//a[contains(@class, "result__snippet")]')
        content = snip[0].text_content().strip() if snip else ""
        if url and title:
            results.append({"title": title, "url": url, "content": content, "engine": "duckduckgo"})
    return results

def _google(query: str, client: httpx.Client, lang: str = "en", page: int = 1, **_) -> list[dict]:
    start = (page - 1) * 10
    params = {"q": query, "hl": lang.split("-")[0], "start": str(start), "filter": "0", "ie": "utf8", "oe": "utf8"}
    resp = client.get("https://www.google.com/search", params=params, headers=_headers(lang), follow_redirects=True, timeout=10)
    resp.raise_for_status()
    dom = lxml.html.fromstring(resp.text)
    results = []
    for a in dom.xpath('//a[@data-ved and not(@class)]'):
        title_div = a.xpath('.//div[@style]') or a.xpath('.//h3')
        if not title_div:
            continue
        title = title_div[0].text_content().strip()
        raw_url = a.get("href", "")
        if raw_url.startswith("/url?q="):
            url = urllib.parse.unquote(raw_url[7:].split("&sa=U")[0])
        else:
            url = raw_url
        content_nodes = a.xpath('../..//div[contains(@class, "ilUpNd")]')
        content = content_nodes[0].text_content().strip() if content_nodes else ""
        if url.startswith("http"):
            results.append({"title": title, "url": url, "content": content, "engine": "google"})
    return results

def _startpage(query: str, client: httpx.Client, lang: str = "en", page: int = 1, **_) -> list[dict]:
    data = {"query": query, "cat": "web", "language": lang, "page": str(page)}
    headers = _headers(lang)
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    resp = client.post("https://www.startpage.com/sp/search", data=data, headers=headers, follow_redirects=True, timeout=10)
    resp.raise_for_status()
    dom = lxml.html.fromstring(resp.text)
    results = []
    for item in dom.xpath('//div[contains(@class, "w-gl__result")]'):
        a = item.xpath('.//a[contains(@class, "w-gl__result-url")]') or item.xpath(".//a[@href]")
        if not a:
            continue
        url = a[0].get("href", "")
        title_el = item.xpath('.//h2') or item.xpath('.//a[contains(@class, "w-gl__result-title")]')
        title = title_el[0].text_content().strip() if title_el else ""
        desc = item.xpath('.//p[contains(@class, "w-gl__description")]')
        content = desc[0].text_content().strip() if desc else ""
        if url and title and url.startswith("http"):
            results.append({"title": title, "url": url, "content": content, "engine": "startpage"})
    return results

def _yahoo(query: str, client: httpx.Client, lang: str = "en", page: int = 1, **_) -> list[dict]:
    params = {"p": query, "b": str((page - 1) * 10 + 1)}
    resp = client.get("https://search.yahoo.com/search", params=params, headers=_headers(lang), follow_redirects=True, timeout=10)
    resp.raise_for_status()
    dom = lxml.html.fromstring(resp.text)
    results = []
    for item in dom.xpath('//div[contains(@class, "algo")]'):
        a = item.xpath('.//h3/a') or item.xpath('.//a[@href]')
        if not a:
            continue
        url, title = a[0].get("href", ""), a[0].text_content().strip()
        desc = item.xpath('.//div[contains(@class, "compText")]//p')
        content = desc[0].text_content().strip() if desc else ""
        if url and title and url.startswith("http"):
            results.append({"title": title, "url": url, "content": content, "engine": "yahoo"})
    return results

# ── 百科/知识 ──

def _wikipedia(query: str, client: httpx.Client, lang: str = "en", **_) -> list[dict]:
    wl = lang.split("-")[0] if lang != "auto" else "en"
    resp = client.get(f"https://{wl}.wikipedia.org/w/api.php",
        params={"action": "opensearch", "search": query, "limit": "5", "format": "json"},
        headers={"User-Agent": _ua()}, follow_redirects=True, timeout=8)
    if resp.status_code != 200:
        return []
    data = resp.json()
    results = []
    if len(data) >= 4:
        for t, d, u in zip(data[1], data[2], data[3]):
            results.append({"title": t, "url": u, "content": d, "engine": "wikipedia"})
    return results

def _wikidata(query: str, client: httpx.Client, lang: str = "en", **_) -> list[dict]:
    wl = lang.split("-")[0] if lang != "auto" else "en"
    resp = client.get("https://www.wikidata.org/w/api.php",
        params={"action": "wbsearchentities", "search": query, "language": wl, "format": "json", "limit": "5"},
        headers={"User-Agent": _ua()}, follow_redirects=True, timeout=8)
    if resp.status_code != 200:
        return []
    results = []
    for item in resp.json().get("search", []):
        results.append({
            "title": item.get("label", ""),
            "url": item.get("concepturi", ""),
            "content": item.get("description", ""),
            "engine": "wikidata",
        })
    return results

# ── 开发/IT ──

def _github(query: str, client: httpx.Client, **_) -> list[dict]:
    resp = client.get("https://api.github.com/search/repositories",
        params={"q": query, "sort": "stars", "order": "desc"},
        headers={"Accept": "application/vnd.github.v3+json", "User-Agent": _ua()}, timeout=10)
    resp.raise_for_status()
    results = []
    for item in resp.json().get("items", [])[:10]:
        desc = " / ".join(p for p in [item.get("language", ""), item.get("description", "")] if p)
        results.append({"title": item.get("full_name", ""), "url": item.get("html_url", ""),
                         "content": desc, "engine": "github", "stars": item.get("stargazers_count", 0)})
    return results

def _stackoverflow(query: str, client: httpx.Client, page: int = 1, **_) -> list[dict]:
    resp = client.get("https://api.stackexchange.com/2.3/search/advanced",
        params={"q": query, "page": str(page), "pagesize": "10", "site": "stackoverflow", "sort": "relevance", "order": "desc"},
        headers={"User-Agent": _ua()}, follow_redirects=True, timeout=10)
    resp.raise_for_status()
    results = []
    for item in resp.json().get("items", []):
        tags = ", ".join(item.get("tags", [])[:5])
        answered = "✓" if item.get("is_answered") else ""
        content = f"[{tags}] score:{item.get('score', 0)} {answered}"
        import html as html_mod
        results.append({"title": html_mod.unescape(item.get("title", "")), "url": item.get("link", ""),
                         "content": content, "engine": "stackoverflow"})
    return results

def _hackernews(query: str, client: httpx.Client, page: int = 1, **_) -> list[dict]:
    resp = client.get("https://hn.algolia.com/api/v1/search",
        params={"query": query, "page": str(page - 1), "hitsPerPage": "10", "tags": "story"},
        headers={"User-Agent": _ua()}, timeout=10)
    resp.raise_for_status()
    results = []
    for hit in resp.json().get("hits", []):
        url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}"
        pts = hit.get("points", 0)
        comments = hit.get("num_comments", 0)
        content = f"⬆{pts} 💬{comments}"
        if hit.get("story_text"):
            import html as html_mod
            text = html_mod.unescape(re.sub(r'<[^>]+>', '', hit["story_text"]))[:200]
            content += f" — {text}"
        results.append({"title": hit.get("title", ""), "url": url, "content": content, "engine": "hackernews"})
    return results

def _reddit(query: str, client: httpx.Client, **_) -> list[dict]:
    resp = client.get("https://www.reddit.com/search.json",
        params={"q": query, "limit": "10"},
        headers={"User-Agent": _ua()}, follow_redirects=True, timeout=10)
    resp.raise_for_status()
    results = []
    for post in resp.json().get("data", {}).get("children", []):
        d = post["data"]
        content = d.get("selftext", "")[:300]
        sub = d.get("subreddit_name_prefixed", "")
        score = d.get("score", 0)
        comments = d.get("num_comments", 0)
        meta = f"{sub} ⬆{score} 💬{comments}"
        if content:
            meta += f" — {content}"
        results.append({"title": d.get("title", ""), "url": f"https://www.reddit.com{d.get('permalink', '')}",
                         "content": meta, "engine": "reddit"})
    return results

def _huggingface(query: str, client: httpx.Client, **_) -> list[dict]:
    resp = client.get("https://huggingface.co/api/models",
        params={"search": query, "direction": "-1", "limit": "10"},
        headers={"User-Agent": _ua()}, follow_redirects=True, timeout=10)
    resp.raise_for_status()
    results = []
    for item in resp.json()[:10]:
        model_id = item.get("modelId") or item.get("id", "")
        downloads = item.get("downloads", 0)
        likes = item.get("likes", 0)
        pipeline = item.get("pipeline_tag", "")
        content = f"❤{likes} ⬇{downloads}"
        if pipeline:
            content += f" [{pipeline}]"
        results.append({"title": model_id, "url": f"https://huggingface.co/{model_id}",
                         "content": content, "engine": "huggingface"})
    return results

def _mdn(query: str, client: httpx.Client, page: int = 1, **_) -> list[dict]:
    resp = client.get("https://developer.mozilla.org/api/v1/search",
        params={"q": query, "page": str(page)},
        headers={"User-Agent": _ua()}, follow_redirects=True, timeout=10)
    resp.raise_for_status()
    results = []
    for doc in resp.json().get("documents", []):
        results.append({"title": doc.get("title", ""), "url": f"https://developer.mozilla.org{doc.get('mdn_url', '')}",
                         "content": doc.get("summary", ""), "engine": "mdn"})
    return results

def _gitlab(query: str, client: httpx.Client, **_) -> list[dict]:
    resp = client.get("https://gitlab.com/api/v4/projects",
        params={"search": query, "order_by": "stars_count", "sort": "desc", "per_page": "10"},
        headers={"User-Agent": _ua()}, follow_redirects=True, timeout=10)
    resp.raise_for_status()
    results = []
    for item in resp.json():
        desc = item.get("description", "") or ""
        stars = item.get("star_count", 0)
        content = f"⭐{stars} — {desc[:200]}" if desc else f"⭐{stars}"
        results.append({"title": item.get("path_with_namespace", ""), "url": item.get("web_url", ""),
                         "content": content, "engine": "gitlab"})
    return results

# ── 学术/科研 ──

def _arxiv(query: str, client: httpx.Client, **_) -> list[dict]:
    resp = client.get("https://export.arxiv.org/api/query",
        params={"search_query": f"all:{query}", "start": "0", "max_results": "10", "sortBy": "relevance"},
        headers={"User-Agent": _ua()}, follow_redirects=True, timeout=10)
    resp.raise_for_status()
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(resp.text)
    results = []
    for entry in root.findall("atom:entry", ns):
        title = (entry.findtext("atom:title", "", ns) or "").strip().replace("\n", " ")
        summary = (entry.findtext("atom:summary", "", ns) or "").strip().replace("\n", " ")[:300]
        link = ""
        for l in entry.findall("atom:link", ns):
            if l.get("type") == "text/html" or l.get("rel") == "alternate":
                link = l.get("href", "")
                break
        if not link:
            link = entry.findtext("atom:id", "", ns)
        results.append({"title": title, "url": link, "content": summary, "engine": "arxiv"})
    return results

def _semantic_scholar(query: str, client: httpx.Client, page: int = 1, **_) -> list[dict]:
    offset = (page - 1) * 10
    resp = client.get("https://api.semanticscholar.org/graph/v1/paper/search",
        params={"query": query, "offset": str(offset), "limit": "10",
                "fields": "title,url,abstract,year,citationCount,authors"},
        headers={"User-Agent": _ua()}, follow_redirects=True, timeout=10)
    resp.raise_for_status()
    results = []
    for paper in resp.json().get("data", []):
        authors = ", ".join(a.get("name", "") for a in (paper.get("authors") or [])[:3])
        year = paper.get("year", "")
        cites = paper.get("citationCount", 0)
        abstract = (paper.get("abstract") or "")[:200]
        content = f"({year}) [{authors}] 📎{cites}"
        if abstract:
            content += f" — {abstract}"
        results.append({"title": paper.get("title", ""), "url": paper.get("url", ""),
                         "content": content, "engine": "semantic_scholar"})
    return results

def _google_scholar(query: str, client: httpx.Client, lang: str = "en", page: int = 1, **_) -> list[dict]:
    start = (page - 1) * 10
    params = {"q": query, "hl": lang.split("-")[0], "start": str(start), "as_sdt": "2007"}
    resp = client.get("https://scholar.google.com/scholar", params=params, headers=_headers(lang), follow_redirects=True, timeout=10)
    resp.raise_for_status()
    dom = lxml.html.fromstring(resp.text)
    results = []
    for item in dom.xpath('//div[@data-rp]'):
        a = item.xpath('.//h3//a')
        if not a:
            continue
        title, url = a[0].text_content().strip(), a[0].get("href", "")
        desc = item.xpath('.//div[@class="gs_rs"]')
        content = desc[0].text_content().strip()[:200] if desc else ""
        meta = item.xpath('.//div[@class="gs_a"]')
        if meta:
            content = meta[0].text_content().strip() + " — " + content
        if url and title:
            results.append({"title": title, "url": url, "content": content, "engine": "google_scholar"})
    return results

def _crossref(query: str, client: httpx.Client, page: int = 1, **_) -> list[dict]:
    resp = client.get("https://api.crossref.org/works",
        params={"query": query, "offset": str((page - 1) * 10), "rows": "10"},
        headers={"User-Agent": _ua()}, follow_redirects=True, timeout=10)
    resp.raise_for_status()
    results = []
    for item in resp.json().get("message", {}).get("items", []):
        titles = item.get("title", [])
        title = titles[0] if titles else ""
        url = item.get("URL", "")
        authors = ", ".join(f"{a.get('given', '')} {a.get('family', '')}" for a in (item.get("author") or [])[:3])
        year = ""
        for dp in ["published-print", "published-online", "created"]:
            parts = (item.get(dp) or {}).get("date-parts", [[]])
            if parts and parts[0]:
                year = str(parts[0][0])
                break
        container = item.get("container-title", [""])
        journal = container[0] if container else ""
        content = f"({year}) [{authors}]"
        if journal:
            content += f" {journal}"
        results.append({"title": title, "url": url, "content": content, "engine": "crossref"})
    return results

# ── 新闻 ──

def _bing_news(query: str, client: httpx.Client, lang: str = "en", **_) -> list[dict]:
    resp = client.get("https://www.bing.com/news/search", params={"q": query},
                       headers=_headers(lang), follow_redirects=True, timeout=10)
    resp.raise_for_status()
    dom = lxml.html.fromstring(resp.text)
    results = []
    for item in dom.xpath('//div[contains(@class, "news-card")]'):
        a = item.xpath('.//a[contains(@class, "title")]') or item.xpath('.//a[@href]')
        if not a:
            continue
        url, title = a[0].get("href", ""), a[0].text_content().strip()
        desc = item.xpath('.//div[contains(@class, "snippet")]')
        content = desc[0].text_content().strip() if desc else ""
        if url and title and url.startswith("http"):
            results.append({"title": title, "url": url, "content": content, "engine": "bing_news"})
    return results

def _reuters(query: str, client: httpx.Client, **_) -> list[dict]:
    resp = client.get("https://www.reuters.com/site-search/", params={"query": query},
                       headers=_headers("en"), follow_redirects=True, timeout=10)
    resp.raise_for_status()
    dom = lxml.html.fromstring(resp.text)
    results = []
    for item in dom.xpath('//li[contains(@class, "search-results__item")]'):
        a = item.xpath('.//a')
        if not a:
            continue
        href = a[0].get("href", "")
        if href.startswith("/"):
            href = "https://www.reuters.com" + href
        title = a[0].text_content().strip()
        desc = item.xpath('.//p')
        content = desc[0].text_content().strip() if desc else ""
        if href and title:
            results.append({"title": title, "url": href, "content": content, "engine": "reuters"})
    return results

# ── 视频 ──

def _youtube(query: str, client: httpx.Client, **_) -> list[dict]:
    resp = client.get(f"https://www.youtube.com/results",
        params={"search_query": query, "sp": "EgIQAQ=="},
        headers=_headers("en"), cookies={"CONSENT": "YES+"}, follow_redirects=True, timeout=10)
    resp.raise_for_status()
    results = []
    # 从 ytInitialData JSON 中提取
    match = re.search(r'var ytInitialData\s*=\s*(\{.+?\});</script>', resp.text)
    if not match:
        return results
    try:
        data = json.loads(match.group(1))
        contents = (data.get("contents", {}).get("twoColumnSearchResultsRenderer", {})
                    .get("primaryContents", {}).get("sectionListRenderer", {}).get("contents", []))
        for section in contents:
            for item in section.get("itemSectionRenderer", {}).get("contents", []):
                video = item.get("videoRenderer", {})
                if not video:
                    continue
                vid = video.get("videoId", "")
                title_runs = video.get("title", {}).get("runs", [])
                title = title_runs[0].get("text", "") if title_runs else ""
                desc_runs = video.get("detailedMetadataSnippets", [{}])[0].get("snippetText", {}).get("runs", []) if video.get("detailedMetadataSnippets") else []
                content = "".join(r.get("text", "") for r in desc_runs)[:200]
                length = video.get("lengthText", {}).get("simpleText", "")
                views = video.get("viewCountText", {}).get("simpleText", "")
                meta = f"[{length}] {views}" if length else ""
                if meta:
                    content = meta + " — " + content if content else meta
                if vid and title:
                    results.append({"title": title, "url": f"https://www.youtube.com/watch?v={vid}",
                                     "content": content, "engine": "youtube"})
    except (json.JSONDecodeError, KeyError):
        pass
    return results[:10]

# ── 图片 ──

def _unsplash(query: str, client: httpx.Client, **_) -> list[dict]:
    resp = client.get("https://unsplash.com/napi/search/photos",
        params={"query": query, "per_page": "10"},
        headers={"User-Agent": _ua()}, follow_redirects=True, timeout=10)
    resp.raise_for_status()
    results = []
    for item in resp.json().get("results", []):
        desc = item.get("description") or item.get("alt_description") or ""
        urls = item.get("urls", {})
        results.append({"title": desc[:100] or query, "url": item.get("links", {}).get("html", ""),
                         "content": desc, "engine": "unsplash", "img_src": urls.get("regular", ""),
                         "thumbnail": urls.get("thumb", "")})
    return results

# ── 社交 ──

def _lemmy(query: str, client: httpx.Client, **_) -> list[dict]:
    resp = client.get("https://lemmy.ml/api/v3/search",
        params={"q": query, "type_": "Posts", "sort": "TopAll", "limit": "10"},
        headers={"User-Agent": _ua()}, follow_redirects=True, timeout=10)
    resp.raise_for_status()
    results = []
    for post in resp.json().get("posts", []):
        p = post.get("post", {})
        community = post.get("community", {}).get("name", "")
        counts = post.get("counts", {})
        score = counts.get("score", 0)
        comments = counts.get("comments", 0)
        content = f"c/{community} ⬆{score} 💬{comments}"
        body = (p.get("body") or "")[:200]
        if body:
            content += f" — {body}"
        url = p.get("url") or p.get("ap_id", "")
        results.append({"title": p.get("name", ""), "url": url, "content": content, "engine": "lemmy"})
    return results

# ── 翻译 ──

def _lingva(query: str, client: httpx.Client, lang: str = "en", **_) -> list[dict]:
    target = lang.split("-")[0] if lang != "auto" else "zh"
    resp = client.get(f"https://lingva.ml/api/v1/auto/{target}/{urllib.parse.quote(query)}",
        headers={"User-Agent": _ua()}, follow_redirects=True, timeout=10)
    if resp.status_code != 200:
        return []
    data = resp.json()
    translation = data.get("translation", "")
    if translation:
        return [{"title": f"翻译: {query}", "url": f"https://lingva.ml/auto/{target}/{urllib.parse.quote(query)}",
                 "content": translation, "engine": "lingva"}]
    return []

# ── 实用工具 ──

def _wolframalpha(query: str, client: httpx.Client, **_) -> list[dict]:
    resp = client.get("https://api.wolframalpha.com/v1/result",
        params={"i": query, "appid": "DEMO"},
        headers={"User-Agent": _ua()}, follow_redirects=True, timeout=10)
    if resp.status_code == 200 and resp.text:
        return [{"title": f"Wolfram|Alpha: {query}", "url": f"https://www.wolframalpha.com/input?i={urllib.parse.quote(query)}",
                 "content": resp.text, "engine": "wolframalpha"}]
    return []

# ── 引擎注册表 ─────────────────────────────────────────────────

ENGINES: dict[str, dict[str, Any]] = {
    # 通用搜索
    "bing":              {"fn": _bing,             "cat": "general",   "proxy": False, "desc": "Bing Web 搜索"},
    "brave":             {"fn": _brave,            "cat": "general",   "proxy": False, "desc": "Brave 搜索"},
    "duckduckgo":        {"fn": _duckduckgo,       "cat": "general",   "proxy": False, "desc": "DuckDuckGo (偶有验证码)"},
    "google":            {"fn": _google,           "cat": "general",   "proxy": True,  "desc": "Google 搜索 (需代理, 反爬严格)"},
    "startpage":         {"fn": _startpage,        "cat": "general",   "proxy": False, "desc": "Startpage (Google 代理)"},
    "yahoo":             {"fn": _yahoo,            "cat": "general",   "proxy": False, "desc": "Yahoo 搜索"},
    # 百科/知识
    "wikipedia":         {"fn": _wikipedia,        "cat": "knowledge", "proxy": False, "desc": "维基百科"},
    "wikidata":          {"fn": _wikidata,         "cat": "knowledge", "proxy": False, "desc": "维基数据 (结构化)"},
    "wolframalpha":      {"fn": _wolframalpha,     "cat": "knowledge", "proxy": True,  "desc": "Wolfram|Alpha 计算"},
    # 开发/IT
    "github":            {"fn": _github,           "cat": "dev",       "proxy": False, "desc": "GitHub 仓库"},
    "gitlab":            {"fn": _gitlab,           "cat": "dev",       "proxy": False, "desc": "GitLab 仓库"},
    "stackoverflow":     {"fn": _stackoverflow,    "cat": "dev",       "proxy": False, "desc": "StackOverflow 问答"},
    "hackernews":        {"fn": _hackernews,       "cat": "dev",       "proxy": False, "desc": "Hacker News"},
    "reddit":            {"fn": _reddit,           "cat": "dev",       "proxy": True,  "desc": "Reddit 社区 (需代理)"},
    "huggingface":       {"fn": _huggingface,      "cat": "dev",       "proxy": True,  "desc": "HuggingFace 模型 (需代理)"},
    "mdn":               {"fn": _mdn,             "cat": "dev",       "proxy": False, "desc": "MDN Web 文档"},
    # 学术
    "arxiv":             {"fn": _arxiv,            "cat": "academic",  "proxy": False, "desc": "arXiv 论文"},
    "semantic_scholar":  {"fn": _semantic_scholar,  "cat": "academic",  "proxy": False, "desc": "Semantic Scholar"},
    "google_scholar":    {"fn": _google_scholar,    "cat": "academic",  "proxy": True,  "desc": "Google Scholar (需代理)"},
    "crossref":          {"fn": _crossref,          "cat": "academic",  "proxy": False, "desc": "Crossref 学术"},
    # 新闻
    "bing_news":         {"fn": _bing_news,        "cat": "news",      "proxy": False, "desc": "Bing 新闻"},
    "reuters":           {"fn": _reuters,          "cat": "news",      "proxy": False, "desc": "路透社"},
    # 视频
    "youtube":           {"fn": _youtube,          "cat": "video",     "proxy": True,  "desc": "YouTube 视频"},
    # 图片
    "unsplash":          {"fn": _unsplash,         "cat": "images",    "proxy": False, "desc": "Unsplash 免费图片"},
    # 社交
    "lemmy":             {"fn": _lemmy,            "cat": "social",    "proxy": True,  "desc": "Lemmy 社区 (需代理)"},
    # 翻译
    "lingva":            {"fn": _lingva,           "cat": "translate", "proxy": True,  "desc": "Lingva 翻译 (需代理)"},
}

# 默认启用的引擎（config.yml 不存在时）
DEFAULT_ENABLED = {"bing", "brave", "duckduckgo", "wikipedia"}

# ── 配置热加载 ─────────────────────────────────────────────────

def _load_config() -> dict:
    """加载 config.yml，每次搜索都重新读取（热插拔）。"""
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        import yaml
        with open(CONFIG_PATH) as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        # 没有 pyyaml，用简单解析
        return _parse_simple_yaml(CONFIG_PATH)

def _parse_simple_yaml(path: str) -> dict:
    """极简 YAML 解析器（只处理 config.yml 需要的结构）。"""
    config: dict[str, Any] = {}
    current_section = None
    current_list: list | None = None

    with open(path) as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            # 顶层 key
            if not line.startswith(" ") and ":" in stripped:
                key, _, val = stripped.partition(":")
                key, val = key.strip(), val.strip()
                if val == "" or val == "[]":
                    config[key] = [] if val == "[]" else {}
                    current_section = key
                    current_list = config[key] if isinstance(config[key], list) else None
                else:
                    config[key] = val.strip('"').strip("'")
                    current_section = None
                    current_list = None
            elif stripped.startswith("- ") and current_list is not None:
                current_list.append(stripped[2:].strip().strip('"').strip("'"))
            elif ":" in stripped and current_section and isinstance(config.get(current_section), dict):
                key, _, val = stripped.partition(":")
                config[current_section][key.strip()] = val.strip().strip('"').strip("'")
    return config

def get_enabled_engines(config: dict) -> set[str]:
    """从 config 确定启用的引擎。"""
    categories_cfg = config.get("categories", {})
    if not categories_cfg:
        # 没有 config 或 categories 为空：使用默认
        return DEFAULT_ENABLED

    enabled = set()
    for cat, status in categories_cfg.items():
        if str(status).lower() in ("true", "on", "yes", "enabled", "1"):
            # 启用该分类下所有引擎
            for name, eng in ENGINES.items():
                if eng["cat"] == cat:
                    enabled.add(name)
    return enabled or DEFAULT_ENABLED

# ── 聚合搜索 ───────────────────────────────────────────────────

def search(
    query: str,
    engines: list[str] | None = None,
    categories: list[str] | None = None,
    lang: str = "en",
    page: int = 1,
    max_results: int = 10,
    proxy: str | None = None,
    timeout: float = 12,
    use_all: bool = False,
) -> dict:
    """并发调用多引擎，聚合去重返回结果。"""

    config = _load_config()
    proxy_url = proxy or config.get("proxy", "") or os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or None

    # 确定使用哪些引擎
    if engines:
        # 指定引擎
        engine_names = [e.strip() for e in engines if e.strip() in ENGINES]
    elif categories:
        # 按分类
        engine_names = [n for n, e in ENGINES.items() if e["cat"] in categories]
    elif use_all:
        engine_names = [n for n in get_enabled_engines(config)]
    else:
        # 默认：config 中启用的，或 DEFAULT_ENABLED
        enabled = get_enabled_engines(config)
        # 只用 general + knowledge 分类的（默认搜索行为）
        engine_names = [n for n in enabled if ENGINES[n]["cat"] in ("general", "knowledge")]
        if not engine_names:
            engine_names = list(DEFAULT_ENABLED)

    if not engine_names:
        return {"error": True, "message": f"无有效引擎。可选: {', '.join(ENGINES)}"}

    all_results: list[dict] = []
    errors: list[dict] = []

    def _run(name: str):
        eng = ENGINES[name]
        client_kwargs: dict[str, Any] = {"verify": True}
        if eng["proxy"] and proxy_url:
            client_kwargs["proxy"] = proxy_url
        else:
            # 显式禁止读取环境变量代理，避免 HTTPS_PROXY 干扰
            client_kwargs["trust_env"] = False
        try:
            with httpx.Client(**client_kwargs) as c:
                return name, eng["fn"](query=query, client=c, lang=lang, page=page)
        except Exception as e:
            log.warning("%s: %s", name, e)
            return name, e

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=min(len(engine_names), 5)) as pool:
        futures = {pool.submit(_run, n): n for n in engine_names}
        try:
            for fut in as_completed(futures, timeout=timeout):
                name = futures[fut]
                try:
                    ename, result = fut.result()
                    if isinstance(result, Exception):
                        errors.append({"engine": ename, "error": str(result)[:200]})
                    else:
                        all_results.extend(result)
                except Exception as e:
                    errors.append({"engine": name, "error": str(e)[:200]})
        except TimeoutError:
            # 部分引擎超时，继续处理已有结果
            for fut, name in futures.items():
                if not fut.done():
                    errors.append({"engine": name, "error": "timeout"})

    elapsed = round(time.time() - t0, 3)

    # 去重 + 聚合引擎
    seen: dict[str, dict] = {}
    for r in all_results:
        url = r.get("url", "")
        norm = re.sub(r'[?#].*$', '', url).rstrip("/").lower()
        if not norm:
            continue
        if norm in seen:
            eng = r.get("engine", "")
            if eng and eng not in seen[norm].get("engines", []):
                seen[norm]["engines"].append(eng)
                seen[norm]["score"] = len(seen[norm]["engines"])
        else:
            r["engines"] = [r.get("engine", "")]
            r["score"] = 1
            seen[norm] = r

    unique = sorted(seen.values(), key=lambda x: -x.get("score", 0))

    return {
        "query": query,
        "results": unique[:max_results],
        "result_count": len(unique),
        "elapsed": elapsed,
        "engines_used": engine_names,
        "errors": errors,
    }

# ── 列出引擎 ───────────────────────────────────────────────────

def list_engines():
    """列出所有引擎和分类。"""
    config = _load_config()
    enabled = get_enabled_engines(config)

    cats: dict[str, list] = {}
    for name, eng in ENGINES.items():
        cats.setdefault(eng["cat"], []).append((name, eng))

    cat_labels = {
        "general": "🔍 通用搜索", "knowledge": "📖 百科/知识", "dev": "💻 开发/IT",
        "academic": "📚 学术", "news": "📰 新闻", "video": "🎬 视频",
        "images": "🖼️ 图片", "social": "📋 社交", "translate": "🔧 翻译",
    }

    for cat in ["general", "knowledge", "dev", "academic", "news", "video", "images", "social", "translate"]:
        items = cats.get(cat, [])
        if not items:
            continue
        label = cat_labels.get(cat, cat)
        # 检查分类是否在 config 中启用
        cat_status = "?"
        if config.get("categories"):
            cs = config["categories"].get(cat, "")
            cat_status = "✅" if str(cs).lower() in ("true", "on", "yes", "enabled", "1") else "❌"
        print(f"\n{label} (category: {cat}) [{cat_status}]")
        for name, eng in sorted(items, key=lambda x: x[0]):
            status = "✅" if name in enabled else "  "
            proxy_tag = " 🌐proxy" if eng["proxy"] else ""
            print(f"  {status} {name:20s} {eng['desc']}{proxy_tag}")

    print(f"\n共 {len(ENGINES)} 个引擎，{len(enabled)} 个已启用")
    print(f"配置文件: {CONFIG_PATH}")

# ── CLI ────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="SearXNG-lite 聚合搜索插件")
    p.add_argument("query", nargs="?", help="搜索词")
    p.add_argument("-e", "--engines", help="指定引擎（逗号分隔）")
    p.add_argument("-c", "--categories", help="按分类搜索（逗号分隔）: general,dev,academic,news,video,images,social,knowledge,translate")
    p.add_argument("-n", "--max-results", type=int, default=10, help="最大结果数")
    p.add_argument("-l", "--lang", default="en", help="语言代码")
    p.add_argument("-p", "--page", type=int, default=1, help="页码")
    p.add_argument("--proxy", help="代理地址")
    p.add_argument("--timeout", type=float, default=12, help="超时秒数")
    p.add_argument("--all", action="store_true", help="使用所有启用的引擎")
    p.add_argument("--compact", action="store_true", help="紧凑输出")
    p.add_argument("--list", action="store_true", help="列出所有引擎")
    p.add_argument("--debug", action="store_true", help="调试日志")
    args = p.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)-7s %(name)s: %(message)s")
    else:
        logging.basicConfig(level=logging.WARNING)

    if args.list:
        list_engines()
        return

    if not args.query:
        p.print_help()
        return

    eng_list = args.engines.split(",") if args.engines else None
    cat_list = args.categories.split(",") if args.categories else None

    result = search(
        query=args.query, engines=eng_list, categories=cat_list,
        lang=args.lang, page=args.page, max_results=args.max_results,
        proxy=args.proxy, timeout=args.timeout, use_all=args.all,
    )

    if args.compact:
        for i, r in enumerate(result.get("results", []), 1):
            eng = ",".join(r.get("engines", []))
            print(f"{i}. {r['title']}")
            print(f"   {r['url']}")
            if r.get("content"):
                print(f"   {r['content'][:160]}")
            if eng:
                print(f"   [{eng}]")
            print()
        if result.get("errors"):
            for e in result["errors"]:
                print(f"⚠ {e['engine']}: {e['error'][:100]}", file=sys.stderr)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
