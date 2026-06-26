from __future__ import annotations

import base64
import html
import re
import urllib.parse
from dataclasses import dataclass, field
from typing import Any

from .adapters import AliasResolver, HTTPClient
from .common import clean_share_url, extract_password, infer_provider_from_url, normalize_title
from .models import SearchIntent, SearchResult


@dataclass(frozen=True)
class RetrievalLayerDefinition:
    name: str
    channel: str
    role: str
    sources: list[str] = field(default_factory=list)
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "channel": self.channel,
            "role": self.role,
            "sources": list(self.sources),
            "description": self.description,
        }


LAYERED_RETRIEVAL_DEFINITIONS: list[RetrievalLayerDefinition] = [
    RetrievalLayerDefinition(
        name="direct-structured-pan",
        channel="pan",
        role="direct",
        sources=["2fun", "dalipan", "hunhepan", "pansou.vip"],
        description="Structured pan aggregators and API-driven sources.",
    ),
    RetrievalLayerDefinition(
        name="direct-structured-torrent",
        channel="torrent",
        role="direct",
        sources=["nyaa", "animetosho", "dmhy", "eztv", "tpb", "torlock", "yts", "1337x"],
        description="Structured torrent, RSS, and index-style sources.",
    ),
    RetrievalLayerDefinition(
        name="community-clue",
        channel="pan",
        role="clue",
        sources=["tieba"],
        description="Community/forum clue mining for links, extraction codes, and follow-up hints.",
    ),
    RetrievalLayerDefinition(
        name="indexed-discovery",
        channel="mixed",
        role="discovery",
        sources=["search-index:ddg", "search-index:bing", "search-index:brave"],
        description="Search-engine indexed discovery for direct links and follow-up clues.",
    ),
    RetrievalLayerDefinition(
        name="authenticated-connector",
        channel="mixed",
        role="auth",
        sources=[],
        description="Reserved layer for future authenticated and private connectors.",
    ),
]


def layered_retrieval_summary() -> list[dict[str, Any]]:
    return [definition.to_dict() for definition in LAYERED_RETRIEVAL_DEFINITIONS]


def build_indexed_discovery_queries(intent: SearchIntent) -> list[str]:
    title_candidates = [
        intent.query,
        intent.title_core,
        intent.english_title_core or intent.english_alias,
        intent.chinese_title_core or intent.chinese_alias,
        *intent.resolved_titles,
    ]
    deduped_titles: list[str] = []
    seen: set[str] = set()
    for title in title_candidates:
        normalized = str(title or "").strip()
        if not normalized:
            continue
        lowered = normalized.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        deduped_titles.append(normalized)

    domain_hints = ["pan.quark.cn", "pan.baidu.com", "alipan", "aliyundrive", "115", "磁力", "网盘"]
    queries: list[str] = []
    for title in deduped_titles[:4]:
        if intent.year:
            queries.append(f"{title} {intent.year}")
        queries.append(title)
        for hint in domain_hints:
            queries.append(f"{title} {hint}")
    if intent.kind in {"tv", "anime"} and intent.season is not None and intent.episode is not None:
        episode_label = f"S{intent.season:02d}E{intent.episode:02d}"
        queries.append(f"{deduped_titles[0] if deduped_titles else intent.query} {episode_label}")
    if intent.wants_sub:
        queries.append(f"{deduped_titles[0] if deduped_titles else intent.query} subtitles")
    if intent.wants_4k:
        queries.append(f"{deduped_titles[0] if deduped_titles else intent.query} 2160p")

    final_queries: list[str] = []
    seen_final: set[str] = set()
    for query in queries:
        normalized = " ".join(str(query or "").split()).strip()
        if not normalized:
            continue
        lowered = normalized.lower()
        if lowered in seen_final:
            continue
        seen_final.add(lowered)
        final_queries.append(normalized)
    return final_queries[:12]


def _decode_bing_result_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.lower() != "www.bing.com":
        return url
    query = urllib.parse.parse_qs(parsed.query)
    target = query.get("u")
    if not target:
        return url
    encoded = target[0]
    if encoded.startswith("a1"):
        encoded = encoded[2:]
    padding = "=" * ((4 - len(encoded) % 4) % 4)
    try:
        return html.unescape(base64.b64decode(encoded + padding).decode("utf-8", "replace"))
    except Exception:
        return url


def _bing_search_results(query: str, http_client: HTTPClient) -> list[dict[str, str]]:
    url = "https://www.bing.com/search?" + urllib.parse.urlencode({"q": query})
    html_text = http_client.get_text(url, timeout=12)
    results: list[dict[str, str]] = []
    pattern = re.compile(r'<li class="b_algo".*?<h2><a[^>]+href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>', re.I | re.S)
    for match in pattern.finditer(html_text):
        href = _decode_bing_result_url(html.unescape(match.group("href")))
        title = normalize_title(re.sub(r"<[^>]+>", " ", html.unescape(match.group("title"))))
        if href.startswith("http"):
            results.append({"title": title, "url": href})
        if len(results) >= 8:
            break
    return results


def _brave_search_results(query: str, http_client: HTTPClient) -> list[dict[str, str]]:
    url = "https://search.brave.com/search?" + urllib.parse.urlencode({"q": query})
    html_text = http_client.get_text(url, timeout=12)
    results: list[dict[str, str]] = []
    pattern = re.compile(r'<a href="(?P<href>https?://[^"]+)" target="_self" class="svelte-14r20fy l1">.*?<div class="title .*?"[^>]*>(?P<title>.*?)</div>', re.I | re.S)
    for match in pattern.finditer(html_text):
        href = clean_share_url(html.unescape(match.group("href")))
        title = normalize_title(re.sub(r"<[^>]+>", " ", html.unescape(match.group("title"))))
        if href.startswith("http"):
            results.append({"title": title, "url": href})
        if len(results) >= 8:
            break
    return results


def search_indexed_discovery(
    intent: SearchIntent,
    http_client: HTTPClient,
    *,
    max_results: int = 8,
) -> list[SearchResult]:
    resolver = AliasResolver()
    providers = [
        ("search-index:ddg", resolver.search_results),
        ("search-index:bing", _bing_search_results),
        ("search-index:brave", _brave_search_results),
    ]
    discovery_results: list[SearchResult] = []
    seen_keys: set[str] = set()
    for query in build_indexed_discovery_queries(intent):
        for source_name, search_provider in providers:
            try:
                search_results = search_provider(query, http_client)
            except Exception:
                continue
            for item in search_results:
                url = clean_share_url(item.get("url", ""))
                if not url:
                    continue
                provider = infer_provider_from_url(url)
                if provider == "other" and "tieba.baidu.com/p/" not in url:
                    continue
                title = normalize_title(item.get("title") or intent.query)
                password = extract_password(item.get("url", "")) or extract_password(item.get("title", ""))
                if provider == "other" and "tieba.baidu.com/p/" in url:
                    provider = "tieba_thread"
                key = f"{provider}:{url}"
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                role = "direct" if provider not in {"tieba_thread"} else "clue"
                discovery_results.append(
                    SearchResult(
                        channel="torrent" if provider == "magnet" else "pan",
                        source=source_name,
                        provider=provider,
                        title=title or url,
                        link_or_magnet=url,
                        password=password,
                        share_id_or_info_hash=url,
                        raw={
                            "query": query,
                            "layer": "indexed-discovery",
                            "retrieval_role": role,
                            "indexed_title": item.get("title", ""),
                        },
                    )
                )
                if len(discovery_results) >= max_results:
                    return discovery_results
    return discovery_results


__all__ = [
    "LAYERED_RETRIEVAL_DEFINITIONS",
    "RetrievalLayerDefinition",
    "build_indexed_discovery_queries",
    "layered_retrieval_summary",
    "search_indexed_discovery",
]
