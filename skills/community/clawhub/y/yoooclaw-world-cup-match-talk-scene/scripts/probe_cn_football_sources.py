#!/usr/bin/env python3
"""Probe Chinese football talk-source pages and emit normalized JSON.

This is an experimental, zero-dependency scraper. It tries public search pages
first, then falls back to known seed URLs so extractor quality can be tested even
when search engines hide result links or show verification pages.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import ssl
import sys
import time
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, unquote, urljoin, urlparse
from urllib.request import Request, urlopen


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)

SOURCES = [
    {
        "name": "dongqiudi",
        "label": "懂球帝",
        "site_query": "site:m.dongqiudi.com/article",
        "domains": ["m.dongqiudi.com", "dongqiudi.com"],
        "seeds": ["https://m.dongqiudi.com/article/5943378.html"],
    },
    {
        "name": "zhibo8",
        "label": "直播吧",
        "site_query": "site:news.zhibo8.com",
        "domains": ["news.zhibo8.com"],
        "seeds": [
            "https://news.zhibo8.com/zuqiu/2026-06-17/6a320bc0bff75native.htm"
        ],
    },
    {
        "name": "sina_sports",
        "label": "新浪体育",
        "site_query": "site:sports.sina.com.cn",
        "domains": ["sports.sina.com.cn", "sports.sina.cn"],
        "seeds": [
            "https://sports.sina.com.cn/g/2026-06-17/doc-inictaeq5705996.shtml"
        ],
    },
    {
        "name": "hupu",
        "label": "虎扑",
        "site_query": "site:m.hupu.com/bbs",
        "domains": ["m.hupu.com"],
        "seeds": ["https://m.hupu.com/bbs/640105131"],
    },
    {
        "name": "weibo_hot",
        "label": "微博热点",
        "site_query": "site:weibo.com/a/hot",
        "domains": ["weibo.com", "www.weibo.com"],
        "seeds": ["https://www.weibo.com/a/hot/79058da5eff5db61_0.html?type=grab"],
    },
    {
        "name": "cctv_sports",
        "label": "央视网体育",
        "site_query": "site:sports.cctv.com",
        "domains": ["sports.cctv.com", "tv.cctv.com"],
        "seeds": [
            "https://sports.cctv.com/2026/06/17/VIDEXr99I4FHNoCtSsO6arYx260617.shtml"
        ],
    },
    {
        "name": "thecfa",
        "label": "中国足协",
        "site_query": "site:thecfa.cn",
        "domains": ["thecfa.cn", "www.thecfa.cn"],
        "seeds": ["https://www.thecfa.cn/cppy/20260422/37586.html"],
    },
    {
        "name": "cfl_china",
        "label": "中足联/中超",
        "site_query": "site:cfl-china.cn",
        "domains": ["cfl-china.cn", "www.cfl-china.cn"],
        "seeds": ["https://www.cfl-china.cn/zh/fixtures/list.html?competition_code=CSL"],
    },
]


@dataclass
class ProbeResult:
    source: str
    query: str
    url: str
    status: str
    title: str = ""
    published_at: str = ""
    author_or_source: str = ""
    summary: str = ""
    sample_facts: list[str] | None = None
    raw_text_length: int = 0
    error: str = ""

    def __post_init__(self) -> None:
        if self.sample_facts is None:
            self.sample_facts = []


class TextExtractor(HTMLParser):
    """Small HTML text/link extractor using only stdlib."""

    SKIP_TAGS = {"script", "style", "noscript", "svg", "canvas"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.text_parts: list[str] = []
        self.links: list[str] = []
        self.meta: dict[str, str] = {}
        self.title_parts: list[str] = []
        self._skip_depth = 0
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {k.lower(): v or "" for k, v in attrs}
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
        if tag == "title":
            self._in_title = True
        if tag == "a" and attrs_dict.get("href"):
            self.links.append(html.unescape(attrs_dict["href"]))
        if tag == "meta":
            key = (
                attrs_dict.get("name")
                or attrs_dict.get("property")
                or attrs_dict.get("itemprop")
                or ""
            ).lower()
            if key and attrs_dict.get("content"):
                self.meta[key] = attrs_dict["content"].strip()

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1
        if tag == "title":
            self._in_title = False
        if tag in {"p", "div", "br", "li", "h1", "h2", "h3"}:
            self.text_parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        cleaned = collapse_ws(data)
        if not cleaned:
            return
        if self._in_title:
            self.title_parts.append(cleaned)
        self.text_parts.append(cleaned)

    @property
    def text(self) -> str:
        return normalize_text("\n".join(self.text_parts))

    @property
    def title(self) -> str:
        return collapse_ws(" ".join(self.title_parts))


def collapse_ws(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def normalize_text(value: str) -> str:
    lines = [collapse_ws(line) for line in re.split(r"[\r\n]+", value or "")]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def fetch_url(url: str, timeout: int = 10) -> tuple[int, str, str]:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.6",
        },
    )
    context = ssl._create_unverified_context()
    try:
        with urlopen(request, timeout=timeout, context=context) as response:
            raw = response.read()
            charset = response.headers.get_content_charset() or guess_charset(raw)
            return response.status, raw.decode(charset, "ignore"), ""
    except HTTPError as exc:
        raw = exc.read()
        return exc.code, raw.decode(guess_charset(raw), "ignore"), str(exc)
    except (URLError, TimeoutError, OSError) as exc:
        return 0, "", repr(exc)


def guess_charset(raw: bytes) -> str:
    sample = raw[:2000].decode("ascii", "ignore").lower()
    match = re.search(r"charset=[\"']?([a-z0-9_-]+)", sample)
    return match.group(1) if match else "utf-8"


def search_urls(query: str, source: dict, limit: int) -> list[str]:
    search_query = f"{source['site_query']} {query}"
    urls: list[str] = []
    for template in (
        "https://www.so.com/s?q={query}",
        "https://www.bing.com/search?q={query}",
    ):
        status, body, _ = fetch_url(template.format(query=quote_plus(search_query)))
        if status < 200 or status >= 400 or not body:
            continue
        urls.extend(extract_search_links(body, source["domains"]))
        if len(urls) >= limit:
            break
        time.sleep(0.2)
    return dedupe_urls(urls)[:limit]


def extract_search_links(body: str, domains: Iterable[str]) -> list[str]:
    extractor = TextExtractor()
    extractor.feed(body)
    candidates = extractor.links + re.findall(r"https?%3A%2F%2F[^\"'<>\\\s]+", body)
    urls: list[str] = []
    for candidate in candidates:
        candidate = html.unescape(unquote(candidate))
        if candidate.startswith("//"):
            candidate = "https:" + candidate
        if not candidate.startswith(("http://", "https://")):
            continue
        parsed = urlparse(candidate)
        if any(domain in parsed.netloc for domain in domains):
            urls.append(clean_tracking_url(candidate))
    return urls


def clean_tracking_url(url: str) -> str:
    url = re.sub(r"[?#](?:utm_|from=|spm=).*$", "", url)
    return url.rstrip()


def dedupe_urls(urls: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            deduped.append(url)
    return deduped


def article_urls_for_source(query: str, source: dict, limit: int) -> list[str]:
    urls = search_urls(query, source, limit)
    if len(urls) < limit:
        urls.extend(source["seeds"])
    return dedupe_urls(urls)[:limit]


def parse_page(source_name: str, url: str, body: str) -> dict:
    if source_name == "dongqiudi":
        dqd = parse_dongqiudi_state(body)
        if dqd:
            return dqd

    extractor = TextExtractor()
    extractor.feed(body)
    text = extractor.text
    title = (
        extractor.meta.get("og:title")
        or extractor.meta.get("twitter:title")
        or extractor.title
    )
    description = extractor.meta.get("description", "")

    return {
        "title": clean_title(title),
        "published_at": extract_date(text + "\n" + body),
        "author_or_source": extract_author_or_source(text, body),
        "text": text,
        "summary": make_summary(text or description),
        "sample_facts": extract_sample_facts(source_name, text),
    }


def parse_dongqiudi_state(body: str) -> dict | None:
    match = re.search(r'window\.__INITIAL_STATE__=(\{.*?\});\(function\(\)', body, re.S)
    if not match:
        return None
    try:
        state = json.loads(match.group(1))
    except json.JSONDecodeError:
        return None
    article_map = state.get("articleContent") or {}
    if not article_map:
        return None
    article = next(iter(article_map.values()))
    raw_body = article.get("body", "")
    text = html_to_text(raw_body)
    return {
        "title": article.get("title", ""),
        "published_at": article.get("time", ""),
        "author_or_source": article.get("writer", "") or article.get("source", "") or "懂球帝",
        "text": text,
        "summary": make_summary(text),
        "sample_facts": extract_sample_facts("dongqiudi", text),
    }


def html_to_text(fragment: str) -> str:
    parser = TextExtractor()
    parser.feed(fragment)
    return parser.text


def clean_title(title: str) -> str:
    title = collapse_ws(title)
    title = re.sub(r"[_|-].{0,20}(新浪体育|直播吧|虎扑社区|央视网体育|中国足球协会官方网站).*$", "", title)
    return title.strip(" _-|")


def extract_date(text: str) -> str:
    patterns = [
        r"\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?\s+\d{1,2}:\d{2}(?::\d{2})?",
        r"\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?",
        r"\d{1,2}月\d{1,2}日\s*\d{1,2}:\d{2}",
        r"\d{1,2}-\d{1,2}\s*\d{1,2}:\d{2}",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return collapse_ws(match.group(0))
    return ""


def extract_author_or_source(text: str, body: str) -> str:
    source_patterns = [
        r"来源\s*[:：]\s*([^\n<]{2,30})",
        r"作者\s*[:：]?\s*([^\n<]{2,30})",
        r"(新浪体育|直播吧|央视网|虎扑足球资讯|中国足球协会|新华社)",
    ]
    combined = text + "\n" + body[:5000]
    for pattern in source_patterns:
        match = re.search(pattern, combined)
        if match:
            return collapse_ws(match.group(1))
    return ""


def make_summary(text: str, max_chars: int = 260) -> str:
    text = normalize_text(text)
    boilerplate = (
        "首页",
        "打开APP",
        "下载客户端",
        "合作网站",
        "用户协议",
        "隐私政策",
        "正在加载",
    )
    sentences: list[str] = []
    for line in text.splitlines():
        if any(token in line for token in boilerplate) and len(line) < 80:
            continue
        if len(line) >= 12:
            sentences.append(line)
        if sum(len(s) for s in sentences) > max_chars:
            break
    return collapse_ws(" ".join(sentences))[:max_chars]


def extract_sample_facts(source_name: str, text: str) -> list[str]:
    facts: list[str] = []
    patterns = [
        r"[^。\n]*(?:\d+[-:：比]\d+|\d+分|\d+球|\d+次|\d+%|\d+\.\d+%|\d+岁)[^。\n]*[。]?",
        r"#[^#\n]{2,30}#",
        r"亮了\(\d+\)",
        r"阅读\s*\d+",
        r"ñ\s*\d+\s*\s*\d+\s*\s*\d+",
        r"判例[一二三四五六七八九十\d]+[^。\n]*[。]?",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            fact = collapse_ws(match.group(0))
            if 6 <= len(fact) <= 180 and fact not in facts:
                facts.append(fact)
            if len(facts) >= 8:
                return facts

    if source_name in {"weibo_hot", "hupu"}:
        for line in text.splitlines():
            line = collapse_ws(line)
            if len(line) >= 18 and line not in facts:
                facts.append(line[:180])
            if len(facts) >= 8:
                break
    return facts


def probe_source(query: str, source: dict, limit: int) -> list[ProbeResult]:
    results: list[ProbeResult] = []
    urls = article_urls_for_source(query, source, limit)
    if not urls:
        return [
            ProbeResult(
                source=source["label"],
                query=query,
                url="",
                status="search_failed",
                error="No URLs found from search or seeds.",
            )
        ]

    for url in urls:
        status_code, body, error = fetch_url(url)
        if status_code < 200 or status_code >= 400 or not body:
            results.append(
                ProbeResult(
                    source=source["label"],
                    query=query,
                    url=url,
                    status="fetch_failed",
                    raw_text_length=len(body),
                    error=f"HTTP {status_code}: {error}",
                )
            )
            continue

        parsed = parse_page(source["name"], url, body)
        raw_text_length = len(parsed.get("text", ""))
        blocked_reason = detect_blocked_or_low_signal(source["name"], parsed, body)
        if blocked_reason:
            results.append(
                ProbeResult(
                    source=source["label"],
                    query=query,
                    url=url,
                    status="blocked" if "blocked" in blocked_reason else "partial",
                    title=parsed.get("title", ""),
                    published_at=parsed.get("published_at", ""),
                    author_or_source=parsed.get("author_or_source", ""),
                    summary=parsed.get("summary", ""),
                    sample_facts=parsed.get("sample_facts", []),
                    raw_text_length=raw_text_length,
                    error=blocked_reason,
                )
            )
            continue

        ok = bool(parsed.get("title") and (parsed.get("summary") or parsed.get("sample_facts")))
        results.append(
            ProbeResult(
                source=source["label"],
                query=query,
                url=url,
                status="ok" if ok else "partial",
                title=parsed.get("title", ""),
                published_at=parsed.get("published_at", ""),
                author_or_source=parsed.get("author_or_source", ""),
                summary=parsed.get("summary", ""),
                sample_facts=parsed.get("sample_facts", []),
                raw_text_length=raw_text_length,
                error="",
            )
        )
        time.sleep(0.2)
    return results


def detect_blocked_or_low_signal(source_name: str, parsed: dict, body: str) -> str:
    title = parsed.get("title", "")
    text = parsed.get("text", "")
    summary = parsed.get("summary", "")
    combined = f"{title}\n{summary}\n{text}\n{body[:500]}".lower()

    if "sina visitor system" in combined or "sina visitor" in combined:
        return "blocked: Weibo returned Sina Visitor System instead of topic content."
    if "百度安全验证" in combined or "安全验证" in combined:
        return "blocked: search/detail page returned security verification."
    if source_name == "cfl_china" and not parsed.get("sample_facts"):
        return "partial: CFL fixture page is mostly dynamic shell; use search snippet, API, or Playwright for match rows."
    if len(text) < 80:
        return "partial: extracted text is too short for reliable talk-material generation."
    return ""


def build_report(results: list[ProbeResult]) -> dict:
    by_source: dict[str, list[ProbeResult]] = {}
    for result in results:
        by_source.setdefault(result.source, []).append(result)

    stable: list[str] = []
    partial: list[str] = []
    needs_work: list[str] = []
    for source, items in by_source.items():
        ok_count = sum(1 for item in items if item.status == "ok")
        text_ok = any(item.raw_text_length >= 120 for item in items)
        blocked_count = sum(1 for item in items if item.status == "blocked")
        if ok_count and text_ok:
            stable.append(source)
        elif blocked_count == len(items):
            needs_work.append(source)
        elif any(item.status in {"ok", "partial"} for item in items):
            partial.append(source)
        else:
            needs_work.append(source)

    return {
        "stable_sources": stable,
        "partial_sources": partial,
        "needs_follow_up": needs_work,
        "ok_count": sum(1 for result in results if result.status == "ok"),
        "total_count": len(results),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True, help="核心搜索词")
    parser.add_argument("--limit", type=int, default=2, help="每个渠道最多抓取数量")
    parser.add_argument("--out", default="probe_results.json", help="输出 JSON 文件路径")
    args = parser.parse_args(argv)

    if args.limit < 1:
        parser.error("--limit must be >= 1")

    all_results: list[ProbeResult] = []
    for source in SOURCES:
        print(f"Probing {source['label']}...", file=sys.stderr)
        all_results.extend(probe_source(args.query, source, args.limit))

    payload = {
        "query": args.query,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "results": [asdict(result) for result in all_results],
        "report": build_report(all_results),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    report = payload["report"]
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
