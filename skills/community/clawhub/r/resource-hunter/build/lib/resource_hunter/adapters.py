from __future__ import annotations

import hashlib
import html
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any
from xml.etree import ElementTree

from .cache import ResourceCache
from .common import (
    clean_share_url,
    compact_spaces,
    extract_password,
    extract_share_id,
    infer_provider_from_url,
    normalize_key,
    normalize_title,
    parse_quality_tags,
    quality_display_from_tags,
    unique_preserve,
)
from .errors import NetworkError, SchemaError, UpstreamError
from .models import SearchIntent, SearchResult

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "*/*",
}

TRACKERS = (
    "&tr=udp://tracker.openbittorrent.com:80"
    "&tr=udp://tracker.opentrackr.org:1337"
    "&tr=udp://open.demonii.com:1337"
    "&tr=udp://tracker.torrent.eu.org:451"
    "&tr=udp://tracker.cyberia.is:6969"
)

RESOURCE_URL_RE = re.compile(r"(https?://[^\s\"'<>]+|magnet:\?[^\s\"'<>]+|ed2k://[^\s\"'<>]+)", re.I)
TIEBA_PAN_CLUE_RE = re.compile(
    r"(?:通过百度网盘分享的文件|百度网盘分享的文件|网盘分享的文件)[:：]\s*(?P<title>[^\n\r<]{1,120})",
    re.I,
)


@dataclass(frozen=True)
class SourceRuntimeProfile:
    timeout: int
    retries: int
    degraded_score_penalty: int
    cooldown_seconds: int
    failure_threshold: int
    default_degraded: bool = False


SOURCE_RUNTIME_PROFILES: dict[str, SourceRuntimeProfile] = {
    "2fun": SourceRuntimeProfile(timeout=10, retries=1, degraded_score_penalty=0, cooldown_seconds=180, failure_threshold=2),
    "hunhepan": SourceRuntimeProfile(timeout=5, retries=0, degraded_score_penalty=18, cooldown_seconds=90, failure_threshold=1, default_degraded=True),
    "pansou.vip": SourceRuntimeProfile(timeout=5, retries=0, degraded_score_penalty=20, cooldown_seconds=90, failure_threshold=1, default_degraded=True),
    "tieba": SourceRuntimeProfile(timeout=8, retries=0, degraded_score_penalty=10, cooldown_seconds=120, failure_threshold=1, default_degraded=True),
    "nyaa": SourceRuntimeProfile(timeout=8, retries=1, degraded_score_penalty=0, cooldown_seconds=180, failure_threshold=2),
    "eztv": SourceRuntimeProfile(timeout=10, retries=1, degraded_score_penalty=0, cooldown_seconds=180, failure_threshold=2),
    "animetosho": SourceRuntimeProfile(timeout=10, retries=1, degraded_score_penalty=0, cooldown_seconds=180, failure_threshold=2),
    "torlock": SourceRuntimeProfile(timeout=12, retries=1, degraded_score_penalty=2, cooldown_seconds=180, failure_threshold=2),
    "dalipan": SourceRuntimeProfile(timeout=12, retries=1, degraded_score_penalty=0, cooldown_seconds=180, failure_threshold=2),
    "dmhy": SourceRuntimeProfile(timeout=10, retries=1, degraded_score_penalty=0, cooldown_seconds=180, failure_threshold=2),
    "tpb": SourceRuntimeProfile(timeout=10, retries=1, degraded_score_penalty=0, cooldown_seconds=180, failure_threshold=2),
    "yts": SourceRuntimeProfile(timeout=5, retries=0, degraded_score_penalty=16, cooldown_seconds=90, failure_threshold=1, default_degraded=True),
    "1337x": SourceRuntimeProfile(timeout=8, retries=0, degraded_score_penalty=4, cooldown_seconds=180, failure_threshold=2),
}


class HTTPClient:
    def __init__(self, retries: int = 1, default_timeout: int = 10) -> None:
        self.retries = retries
        self.default_timeout = default_timeout

    def _request(self, url: str, timeout: int | None = None) -> str:
        timeout = timeout or self.default_timeout
        last_error = ""
        failure_kind = "network"
        for attempt in range(self.retries + 1):
            request = urllib.request.Request(url, headers=DEFAULT_HEADERS)
            try:
                with urllib.request.urlopen(request, timeout=timeout) as response:
                    charset = response.headers.get_content_charset() or "utf-8"
                    return response.read().decode(charset, errors="replace")
            except urllib.error.HTTPError as exc:
                last_error = f"HTTP {exc.code}"
                failure_kind = "http_4xx" if 400 <= exc.code < 500 else "http_5xx"
                if 400 <= exc.code < 500:
                    break
            except Exception as exc:  # pragma: no cover
                last_error = str(exc)
                failure_kind = "network"
            if attempt < self.retries:
                time.sleep(0.2 * (attempt + 1))
        if failure_kind.startswith("http_"):
            raise UpstreamError(last_error or "request failed", url=url, failure_kind=failure_kind)
        raise NetworkError(last_error or "request failed", url=url)

    def get_text(self, url: str, timeout: int | None = None) -> str:
        return self._request(url, timeout=timeout)

    def get_json(self, url: str, timeout: int | None = None) -> Any:
        payload = self._request(url, timeout=timeout)
        try:
            return json.loads(payload)
        except json.JSONDecodeError as exc:
            raise SchemaError(f"invalid json from {url}: {exc}", url=url) from exc


class SourceAdapter:
    name = "base"
    channel = "both"
    priority = 9

    def search(
        self,
        query: str,
        intent: SearchIntent,
        limit: int,
        page: int,
        http_client: HTTPClient,
    ) -> list[SearchResult]:
        raise NotImplementedError

    def healthcheck(self, http_client: HTTPClient) -> tuple[bool, str]:
        probe_intent = SearchIntent(
            query="ubuntu",
            original_query="ubuntu",
            kind="general",
            channel=self.channel,
            title_core="ubuntu",
            title_tokens=["ubuntu"],
        )
        try:
            self.search("ubuntu", probe_intent, limit=1, page=1, http_client=http_client)
            return True, ""
        except Exception as exc:  # pragma: no cover
            return False, str(exc)


class AliasResolver:
    SEARCH_RESULT_RE = re.compile(
        r'<a[^>]+class="result__a"[^>]+href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>',
        re.I | re.S,
    )
    META_CONTENT_RE = re.compile(
        r'<meta[^>]+(?:property|name)=["\'](?:og:title|title|description|og:description|twitter:title)["\'][^>]+content=["\'](?P<content>[^"\']+)["\']',
        re.I,
    )
    HTML_TITLE_RE = re.compile(r"<title>(?P<title>.*?)</title>", re.I | re.S)
    JSON_LD_RE = re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(?P<json>.*?)</script>', re.I | re.S)
    ORIGINAL_TITLE_RE = re.compile(
        r"(?:Original title|AKA|Also known as|原名|别名|譯名|片名)[:：]?\s*([A-Za-z][A-Za-z0-9'&:\- ]{2,80})",
        re.I,
    )
    ENGLISH_TITLE_RE = re.compile(r"\b[A-Z][A-Za-z0-9'&:\-]+(?: [A-Z0-9][A-Za-z0-9'&:\-]+){0,8}\b")
    EXTRA_TITLE_RE = re.compile(r"(?:外文名|英文名)[:：]?\s*([A-Za-z][A-Za-z0-9'&:\- ]{2,80})", re.I)
    BLACKLIST = {"youtube", "bilibili", "douban", "baidu", "wikipedia", "letterboxd", "imdb", "sohu", "tencent", "video", "cast", "name", "rate", "full"}
    ID_LIKE_RE = re.compile(r"^(?:BV[0-9A-Za-z]+|[A-Za-z0-9_-]{8,})$")

    def search_results(self, query: str, http_client: HTTPClient) -> list[dict[str, str]]:
        url = "https://duckduckgo.com/html/?" + urllib.parse.urlencode({"q": query})
        html_text = http_client.get_text(url, timeout=12)
        results: list[dict[str, str]] = []
        for match in self.SEARCH_RESULT_RE.finditer(html_text):
            href = html.unescape(match.group("href"))
            parsed = urllib.parse.urlparse(href)
            if "duckduckgo.com" in parsed.netloc and "uddg=" in href:
                href = urllib.parse.parse_qs(parsed.query).get("uddg", [href])[0]
            title = normalize_title(re.sub(r"<[^>]+>", " ", html.unescape(match.group("title"))))
            if href.startswith("http"):
                results.append({"title": title, "url": href})
            if len(results) >= 5:
                break
        return results

    def fetch_metadata_texts(self, url: str, http_client: HTTPClient) -> list[str]:
        html_text = http_client.get_text(url, timeout=12)
        texts: list[str] = [url]
        title_match = self.HTML_TITLE_RE.search(html_text)
        if title_match:
            texts.append(html.unescape(re.sub(r"<[^>]+>", " ", title_match.group("title"))))
        for meta_match in self.META_CONTENT_RE.finditer(html_text):
            texts.append(html.unescape(meta_match.group("content")))
        for original in self.ORIGINAL_TITLE_RE.findall(html_text):
            texts.append(html.unescape(original))
        for original in self.EXTRA_TITLE_RE.findall(html_text):
            texts.append(html.unescape(original))
        for json_match in self.JSON_LD_RE.finditer(html_text):
            raw_json = html.unescape(json_match.group("json")).strip()
            try:
                payload = json.loads(raw_json)
            except Exception:
                continue
            candidates = payload if isinstance(payload, list) else [payload]
            for item in candidates:
                if not isinstance(item, dict):
                    continue
                for key in ("name", "alternateName", "alternateName", "headline"):
                    value = item.get(key)
                    if isinstance(value, str):
                        texts.append(value)
                    elif isinstance(value, list):
                        texts.extend([entry for entry in value if isinstance(entry, str)])
        return [compact_spaces(text) for text in texts if compact_spaces(text)]

    def _extract_aliases_from_texts(self, texts: list[str], year: str, original_title: str = "") -> tuple[str, str, list[str]]:
        english = ""
        romanized = ""
        alternates: list[str] = []
        explicit_hits: list[str] = []
        explicit_pattern = None
        if original_title:
            explicit_pattern = re.compile(
                rf"(?:《{re.escape(original_title)}》|{re.escape(original_title)})[（(]([A-Za-z][A-Za-z0-9'&:\- ]{{2,80}})[)）]"
            )
        for text in texts:
            if original_title and original_title in text:
                start = text.find(original_title)
                window = text[start : start + 140]
                nearby = re.search(r"[（(]([A-Za-z][A-Za-z0-9'&:\- ]{2,80})[)）]", window)
                if nearby:
                    candidate = compact_spaces(nearby.group(1))
                    lowered = candidate.lower()
                    if candidate and lowered not in self.BLACKLIST and not self.ID_LIKE_RE.match(candidate):
                        explicit_hits.append(candidate)
            if explicit_pattern:
                for match in explicit_pattern.findall(text):
                    candidate = compact_spaces(match)
                    lowered = candidate.lower()
                    if candidate and lowered not in self.BLACKLIST and not self.ID_LIKE_RE.match(candidate):
                        explicit_hits.append(candidate)
            for match in self.ORIGINAL_TITLE_RE.findall(text):
                candidate = compact_spaces(match)
                lowered = candidate.lower()
                if candidate and not any(ord(ch) > 127 for ch in candidate) and lowered not in self.BLACKLIST and not self.ID_LIKE_RE.match(candidate):
                    alternates.append(candidate)
            for match in self.EXTRA_TITLE_RE.findall(text):
                candidate = compact_spaces(match)
                lowered = candidate.lower()
                if candidate and lowered not in self.BLACKLIST and not self.ID_LIKE_RE.match(candidate):
                    alternates.append(candidate)
            for match in self.ENGLISH_TITLE_RE.findall(text):
                candidate = compact_spaces(match)
                lowered = candidate.lower()
                if not candidate or lowered in self.BLACKLIST | {"movie", "film"} or self.ID_LIKE_RE.match(candidate):
                    continue
                if year and year in candidate:
                    candidate = compact_spaces(candidate.replace(year, ""))
                if len(candidate) < 4:
                    continue
                alternates.append(candidate)
        ranked = sorted(
            unique_preserve(alternates),
            key=lambda candidate: (
                0 if len(candidate.split()) >= 2 else 1,
                0 if candidate.replace("-", " ").replace("'", "").replace("&", "").replace(":", "").replace(".", "").replace(" ", "").isalpha() else 1,
                len(candidate),
            ),
        )
        deduped = unique_preserve([*explicit_hits, *ranked])
        if explicit_hits:
            english = explicit_hits[0]
        for candidate in deduped:
            token_count = len(candidate.split())
            if not english and token_count >= 2 and any(ch.isupper() for ch in candidate):
                english = candidate
            if not romanized and token_count >= 3 and all(part.isalpha() for part in candidate.replace("-", " ").split()):
                romanized = candidate
        return english, romanized, deduped[:8]

    def resolve(self, intent: SearchIntent, cache: ResourceCache, http_client: HTTPClient | None) -> dict[str, Any]:
        if (
            http_client is None
            or intent.kind not in {"movie", "general"}
            or not intent.chinese_title_core
            or not intent.year
            or intent.english_alias
            or intent.season is not None
            or intent.episode is not None
        ):
            return {}
        cache_key = hashlib.sha256(f"alias_v8|{intent.chinese_title_core}|{intent.year}".encode("utf-8")).hexdigest()
        cached = cache.get_alias_resolution(cache_key)
        if cached:
            return cached

        resolver_sources: list[str] = []
        collected_texts: list[str] = []
        try:
            baike_url = "https://baike.baidu.com/item/" + urllib.parse.quote(intent.chinese_title_core)
            resolver_sources.append(baike_url)
            collected_texts.extend(self.fetch_metadata_texts(baike_url, http_client))
        except Exception:
            pass

        search_queries = [
            f"{intent.chinese_title_core} {intent.year} 百度百科",
            f"{intent.chinese_title_core} {intent.year} 豆瓣",
            f"{intent.chinese_title_core} {intent.year} 电影",
            f"{intent.chinese_title_core} {intent.year} IMDb",
            f"{intent.chinese_title_core} {intent.year} 英文名",
        ]
        result_items: list[dict[str, str]] = []
        for query in search_queries:
            try:
                result_items.extend(self.search_results(query, http_client))
            except Exception:
                continue

        domain_priority = {
            "imdb.com": 0,
            "letterboxd.com": 1,
            "movie.douban.com": 2,
            "wikipedia.org": 3,
            "baike.baidu.com": 4,
            "bilibili.com": 5,
            "v.qq.com": 6,
            "tv.sohu.com": 7,
            "youtube.com": 8,
        }
        result_items.sort(
            key=lambda item: min(
                (priority for domain, priority in domain_priority.items() if domain in item["url"]),
                default=99,
            )
        )

        for item in result_items[:4]:
            resolver_sources.append(item["url"])
            collected_texts.append(item["title"])
            try:
                collected_texts.extend(self.fetch_metadata_texts(item["url"], http_client))
            except Exception:
                continue

        english_title, romanized_title, alternates = self._extract_aliases_from_texts(
            collected_texts, intent.year, original_title=intent.chinese_title_core
        )
        follow_up_alias = english_title or (alternates[0] if alternates else "")
        if follow_up_alias:
            for query in (
                f"{follow_up_alias} {intent.year} site:imdb.com",
                f"{follow_up_alias} {intent.year} site:letterboxd.com",
                f"{follow_up_alias} {intent.year} site:wikipedia.org",
            ):
                try:
                    for item in self.search_results(query, http_client)[:2]:
                        resolver_sources.append(item["url"])
                        collected_texts.append(item["title"])
                        try:
                            collected_texts.extend(self.fetch_metadata_texts(item["url"], http_client))
                        except Exception:
                            continue
                except Exception:
                    continue
            english_title, romanized_title, alternates = self._extract_aliases_from_texts(
                collected_texts, intent.year, original_title=intent.chinese_title_core
            )
        payload = {
            "original_title": intent.chinese_title_core,
            "english_title": english_title,
            "romanized_title": romanized_title,
            "alternate_titles": alternates,
            "resolved_year": intent.year,
            "resolver_sources": unique_preserve(resolver_sources),
        }
        cache.set_alias_resolution(cache_key, payload, ttl_seconds=86400)
        return payload


def _profile_for(source_name: str) -> SourceRuntimeProfile:
    return SOURCE_RUNTIME_PROFILES.get(
        source_name,
        SourceRuntimeProfile(timeout=10, retries=1, degraded_score_penalty=0, cooldown_seconds=180, failure_threshold=2),
    )


def _clean_magnet(text: str) -> str:
    return html.unescape(text or "").strip()


def _make_magnet(info_hash: str, name: str) -> str:
    return f"magnet:?xt=urn:btih:{info_hash}&dn={urllib.parse.quote(name)}{TRACKERS}"


def _format_size(size_bytes: int | str | None) -> str:
    if size_bytes in (None, "", 0, "0"):
        return ""
    try:
        numeric = float(size_bytes)
    except Exception:
        return str(size_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if numeric < 1024:
            return f"{numeric:.1f}{unit}"
        numeric /= 1024
    return f"{numeric:.1f}PB"


def _validate_pan_payload(payload: Any, source_name: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise SchemaError(f"unexpected payload type from {source_name}", source=source_name)
    if "results" in payload and isinstance(payload["results"], list):
        return payload
    if "data" in payload and isinstance(payload["data"], (list, dict)):
        return payload
    raise SchemaError(f"unexpected pan payload shape from {source_name}", source=source_name)


def _flatten_pan_payload(payload: dict[str, Any], source_name: str) -> list[SearchResult]:
    payload = _validate_pan_payload(payload, source_name)
    items: list[dict[str, Any]] = []
    if isinstance(payload.get("results"), list):
        items = payload["results"]
    elif isinstance(payload.get("data"), list):
        items = payload["data"]
    elif isinstance(payload.get("data"), dict):
        for provider, values in payload["data"].items():
            for value in values if isinstance(values, list) else []:
                entry = dict(value) if isinstance(value, dict) else {"url": value}
                entry.setdefault("cloud", provider)
                items.append(entry)

    results: list[SearchResult] = []
    for item in items:
        raw_url = item.get("url") or item.get("link") or item.get("shareUrl") or ""
        cleaned_url = clean_share_url(raw_url)
        if not cleaned_url:
            continue
        provider = item.get("netdiskType") or item.get("cloud") or item.get("type") or infer_provider_from_url(cleaned_url)
        title = normalize_title(item.get("title") or item.get("name") or "")
        password = item.get("pwd") or item.get("password") or extract_password(raw_url) or extract_password(title)
        quality_tags = parse_quality_tags(title)
        normalized_channel = "torrent" if (provider or "").lower() in {"magnet", "ed2k"} else "pan"
        results.append(
            SearchResult(
                channel=normalized_channel,
                source=source_name,
                provider=provider or infer_provider_from_url(cleaned_url),
                title=title or cleaned_url,
                link_or_magnet=cleaned_url,
                password=password,
                share_id_or_info_hash=extract_share_id(cleaned_url, provider_hint=provider),
                size=str(item.get("size") or ""),
                quality=quality_display_from_tags(quality_tags),
                quality_tags=quality_tags,
                raw=item,
            )
        )
    return results


class TwoFunSource(SourceAdapter):
    name = "2fun"
    channel = "pan"
    priority = 1

    def search(self, query: str, intent: SearchIntent, limit: int, page: int, http_client: HTTPClient) -> list[SearchResult]:
        url = "https://s.2fun.live/api/search?" + urllib.parse.urlencode(
            {"q": query, "page": page, "pageSize": max(limit * 3, 20)}
        )
        payload = http_client.get_json(url)
        return _flatten_pan_payload(payload, self.name)


class HunhepanSource(SourceAdapter):
    name = "hunhepan"
    channel = "pan"
    priority = 2

    def search(self, query: str, intent: SearchIntent, limit: int, page: int, http_client: HTTPClient) -> list[SearchResult]:
        url = "https://www.hunhepan.com/api/search?" + urllib.parse.urlencode({"q": query, "page": page})
        payload = http_client.get_json(url)
        return _flatten_pan_payload(payload, self.name)


class PansouVipSource(SourceAdapter):
    name = "pansou.vip"
    channel = "pan"
    priority = 3

    def search(self, query: str, intent: SearchIntent, limit: int, page: int, http_client: HTTPClient) -> list[SearchResult]:
        candidates = [
            "https://pansou.vip/api/search?" + urllib.parse.urlencode({"q": query, "page": page}),
            "https://pansou.vip/api/search?" + urllib.parse.urlencode({"keyword": query, "page": page}),
            "https://pansou.vip/api?" + urllib.parse.urlencode({"q": query, "page": page}),
        ]
        last_error = "no valid endpoint"
        for url in candidates:
            try:
                payload = http_client.get_json(url)
                results = _flatten_pan_payload(payload, self.name)
                if results:
                    return results
            except Exception as exc:  # pragma: no cover
                last_error = str(exc)
        raise RuntimeError(last_error)


def _extract_embedded_resource_results(
    html_text: str,
    *,
    source_name: str,
    title_hint: str,
    thread_url: str,
) -> list[SearchResult]:
    results: list[SearchResult] = []
    seen: set[str] = set()
    decoded_text = html.unescape(html_text)
    for match in RESOURCE_URL_RE.finditer(decoded_text):
        raw_url = match.group(1).rstrip(".,);]>\"'")
        cleaned_url = clean_share_url(raw_url)
        if not cleaned_url:
            continue
        provider = infer_provider_from_url(cleaned_url)
        if provider == "other":
            continue
        share_key = extract_share_id(cleaned_url, provider_hint=provider)
        if share_key in seen:
            continue
        seen.add(share_key)
        start = max(0, match.start() - 120)
        end = min(len(decoded_text), match.end() + 120)
        context = decoded_text[start:end]
        password = extract_password(context) or extract_password(raw_url) or extract_password(title_hint)
        quality_tags = parse_quality_tags(title_hint)
        normalized_channel = "torrent" if provider in {"magnet", "ed2k"} else "pan"
        results.append(
            SearchResult(
                channel=normalized_channel,
                source=source_name,
                provider=provider,
                title=normalize_title(title_hint) or cleaned_url,
                link_or_magnet=cleaned_url,
                password=password,
                share_id_or_info_hash=share_key,
                quality=quality_display_from_tags(quality_tags),
                quality_tags=quality_tags,
                raw={"thread_url": thread_url},
            )
        )
    return results


def _extract_tieba_clue_results(
    html_text: str,
    *,
    source_name: str,
    title_hint: str,
    thread_url: str,
) -> list[SearchResult]:
    decoded_text = html.unescape(html_text)
    title_match = TIEBA_PAN_CLUE_RE.search(decoded_text)
    password = extract_password(decoded_text)
    if not title_match or not password:
        return []

    clue_title = normalize_title(title_match.group("title")) or normalize_title(title_hint)
    quality_tags = parse_quality_tags(clue_title)
    return [
        SearchResult(
            channel="pan",
            source=source_name,
            provider="baidu_clue",
            title=clue_title,
            link_or_magnet=thread_url,
            password=password,
            share_id_or_info_hash=normalize_key(thread_url)[:32],
            quality=quality_display_from_tags(quality_tags),
            quality_tags=quality_tags,
            raw={"thread_url": thread_url, "manual_follow_up": True},
        )
    ]


class TiebaSource(SourceAdapter):
    name = "tieba"
    channel = "pan"
    priority = 4

    def search(self, query: str, intent: SearchIntent, limit: int, page: int, http_client: HTTPClient) -> list[SearchResult]:
        resolver = AliasResolver()
        search_queries = unique_preserve(
            [
                f"site:tieba.baidu.com/p/ {query}",
                f"site:tieba.baidu.com/p/ {query} 网盘",
                f"site:tieba.baidu.com/p/ {query} 磁力",
            ]
        )
        thread_results: list[dict[str, str]] = []
        for search_query in search_queries:
            try:
                items = resolver.search_results(search_query, http_client)
            except Exception:
                continue
            for item in items:
                if "tieba.baidu.com/p/" not in item["url"]:
                    continue
                thread_results.append(item)
            if len(thread_results) >= max(limit * 2, 6):
                break

        all_results: list[SearchResult] = []
        seen_threads: set[str] = set()
        for item in thread_results:
            thread_url = item["url"]
            if thread_url in seen_threads:
                continue
            seen_threads.add(thread_url)
            try:
                html_text = http_client.get_text(thread_url, timeout=12)
            except Exception:
                continue
            title_hint = item["title"] or query
            all_results.extend(
                _extract_embedded_resource_results(
                    html_text,
                    source_name=self.name,
                    title_hint=title_hint,
                    thread_url=thread_url,
                )
            )
            if not all_results:
                all_results.extend(
                    _extract_tieba_clue_results(
                        html_text,
                        source_name=self.name,
                        title_hint=title_hint,
                        thread_url=thread_url,
                    )
                )
            if len(all_results) >= max(limit * 2, 8):
                break
        return all_results


class AnimeToshoSource(SourceAdapter):
    name = "animetosho"
    channel = "torrent"
    priority = 2

    SIZE_RE = re.compile(r"Total Size</strong>:\s*([^<]+)<", re.I)

    def search(self, query: str, intent: SearchIntent, limit: int, page: int, http_client: HTTPClient) -> list[SearchResult]:
        url = "https://feed.animetosho.org/rss2?" + urllib.parse.urlencode({"q": query})
        payload = http_client.get_text(url)
        root = ElementTree.fromstring(payload)
        results: list[SearchResult] = []
        for item in root.findall("./channel/item")[: max(limit * 3, 12)]:
            title = normalize_title(item.findtext("title", ""))
            description = html.unescape(item.findtext("description", ""))
            enclosure = item.find("enclosure")
            torrent_url = clean_share_url(enclosure.get("url", "")) if enclosure is not None else ""
            magnet = ""
            for match in RESOURCE_URL_RE.finditer(description):
                candidate = clean_share_url(match.group(1))
                if candidate.startswith("magnet:"):
                    magnet = candidate
                    break
                if not torrent_url and candidate.startswith("http"):
                    torrent_url = candidate
            link_or_magnet = magnet or torrent_url or clean_share_url(item.findtext("link", ""))
            if not title or not link_or_magnet:
                continue
            info_hash = extract_share_id(link_or_magnet, provider_hint="magnet" if link_or_magnet.startswith("magnet:") else "")
            size_match = self.SIZE_RE.search(description)
            quality_tags = parse_quality_tags(title)
            results.append(
                SearchResult(
                    channel="torrent",
                    source=self.name,
                    provider="magnet" if link_or_magnet.startswith("magnet:") else "torrent",
                    title=title,
                    link_or_magnet=link_or_magnet,
                    share_id_or_info_hash=info_hash,
                    size=size_match.group(1).strip() if size_match else "",
                    quality=quality_display_from_tags(quality_tags),
                    quality_tags=quality_tags,
                    raw={"link": item.findtext("link", ""), "description": description[:500]},
                )
            )
        return results


class DMHYSource(SourceAdapter):
    name = "dmhy"
    channel = "torrent"
    priority = 2

    ROW_RE = re.compile(
        r'<tr[^>]*>.*?<td class="title">.*?<a href="(?P<detail>/topics/view/[^"]+)"[^>]*>(?P<title>.*?)</a>.*?'
        r'class="download-arrow arrow-magnet"[^>]+href="(?P<magnet>magnet:[^"]+)".*?'
        r'<td nowrap="nowrap" align="center">(?P<size>[^<]+)</td>',
        re.S,
    )

    def search(self, query: str, intent: SearchIntent, limit: int, page: int, http_client: HTTPClient) -> list[SearchResult]:
        url = "https://dmhy.org/topics/list?" + urllib.parse.urlencode({"keyword": query})
        payload = http_client.get_text(url)
        results: list[SearchResult] = []
        for match in self.ROW_RE.finditer(payload):
            title = normalize_title(re.sub(r"<[^>]+>", " ", html.unescape(match.group("title"))))
            magnet = _clean_magnet(html.unescape(match.group("magnet")))
            if not title or not magnet:
                continue
            quality_tags = parse_quality_tags(title)
            detail_url = "https://dmhy.org" + html.unescape(match.group("detail"))
            results.append(
                SearchResult(
                    channel="torrent",
                    source=self.name,
                    provider="magnet",
                    title=title,
                    link_or_magnet=magnet,
                    share_id_or_info_hash=extract_share_id(magnet, provider_hint="magnet"),
                    size=normalize_title(html.unescape(match.group("size"))),
                    quality=quality_display_from_tags(quality_tags),
                    quality_tags=quality_tags,
                    raw={"detail_url": detail_url},
                )
            )
            if len(results) >= max(limit * 2, 8):
                break
        return results


class DaliPanSource(SourceAdapter):
    name = "dalipan"
    channel = "pan"
    priority = 2

    def search(self, query: str, intent: SearchIntent, limit: int, page: int, http_client: HTTPClient) -> list[SearchResult]:
        def _load_payload() -> dict[str, Any]:
            try:
                payload = http_client.get_json(url, timeout=12)
                if isinstance(payload, dict):
                    return payload
                raise SchemaError(f"invalid dalipan payload type: {type(payload).__name__}", source=self.name, url=url)
            except Exception as primary_error:
                request = urllib.request.Request(url, headers=DEFAULT_HEADERS | {"Accept": "application/json"})
                try:
                    with urllib.request.urlopen(request, timeout=12, context=ssl._create_unverified_context()) as response:
                        payload = json.loads(
                            response.read().decode(response.headers.get_content_charset() or "utf-8", errors="replace")
                        )
                except json.JSONDecodeError as exc:
                    raise SchemaError(f"invalid json from {url}: {exc}", source=self.name, url=url) from exc
                except Exception as insecure_error:
                    message = str(insecure_error) or str(primary_error) or "request failed"
                    raise NetworkError(message, source=self.name, url=url) from insecure_error
                if not isinstance(payload, dict):
                    raise SchemaError(
                        f"invalid dalipan payload type: {type(payload).__name__}", source=self.name, url=url
                    )
                return payload

        params = {
            "kw": query,
            "page": page or 1,
            "line": max(limit * 2, 10),
            "site": "dalipan",
        }
        url = "https://api.dalipan.com/api/v1/pan/search?" + urllib.parse.urlencode(params)
        resources = (_load_payload().get("resources") or [])
        results: list[SearchResult] = []
        for item in resources[: max(limit * 3, 18)]:
            res = item.get("res") or {}
            raw_title = html.unescape(res.get("filename") or "")
            title = normalize_title(raw_title)
            if not title:
                continue
            provider = str(res.get("type") or "")
            if provider not in {"baidu", "aliyun", "quark", "xunlei"}:
                continue
            access_token = str(res.get("eu") or "")
            if not access_token:
                continue
            quality_tags = parse_quality_tags(title)
            results.append(
                SearchResult(
                    channel="pan",
                    source=self.name,
                    provider=provider,
                    title=title,
                    link_or_magnet=f"dalipan://{provider}/{access_token}",
                    share_id_or_info_hash=str(res.get("id") or access_token),
                    size=_format_size(res.get("size", 0)),
                    quality=quality_display_from_tags(quality_tags),
                    quality_tags=quality_tags,
                    raw={
                        "dalipan_id": res.get("id", ""),
                        "dalipan_eu": access_token,
                        "ctime": res.get("ctime", ""),
                        "updatetime": res.get("updatetime", ""),
                        "filelist": res.get("filelist", []),
                        "delivery": "token_only",
                        "retrieval_role": "clue",
                        "requires_follow_up": True,
                    },
                )
            )
        return results


class TorlockSource(SourceAdapter):
    name = "torlock"
    channel = "torrent"
    priority = 2

    ROW_RE = re.compile(
        r'<tr>.*?<a href=(?P<detail>[^\s>]+)[^>]*>(?P<title>.*?)</a>.*?'
        r'<td class=td[^>]*>(?P<added>[^<]+)</td>.*?<td class=ts[^>]*>(?P<size>[^<]+)</td>.*?'
        r'<td class=tul[^>]*>(?P<seeds>\d+)</td>.*?<td class=tdl[^>]*>(?P<peers>\d+)</td>',
        re.S,
    )
    DETAIL_MAGNET_RE = re.compile(r'href="(magnet:[^"]+)"', re.I)

    def search(self, query: str, intent: SearchIntent, limit: int, page: int, http_client: HTTPClient) -> list[SearchResult]:
        url = f"https://www.torlock2.com/all/torrents/{urllib.parse.quote(query)}.html"
        payload = http_client.get_text(url)
        results: list[SearchResult] = []
        for match in self.ROW_RE.finditer(payload):
            detail_url = html.unescape(match.group("detail")).strip().strip('"\'')
            if detail_url.startswith("/"):
                detail_url = "https://www.torlock2.com" + detail_url
            elif not detail_url.startswith("http"):
                detail_url = "https://www.torlock2.com/" + detail_url.lstrip("/")
            try:
                detail_payload = http_client.get_text(detail_url)
                magnet_match = self.DETAIL_MAGNET_RE.search(detail_payload)
            except Exception:
                continue
            if not magnet_match:
                continue
            title = normalize_title(re.sub(r"<[^>]+>", " ", html.unescape(match.group("title"))))
            magnet = _clean_magnet(html.unescape(magnet_match.group(1)))
            quality_tags = parse_quality_tags(title)
            results.append(
                SearchResult(
                    channel="torrent",
                    source=self.name,
                    provider="magnet",
                    title=title,
                    link_or_magnet=magnet,
                    share_id_or_info_hash=extract_share_id(magnet, provider_hint="magnet"),
                    size=normalize_title(html.unescape(match.group("size"))),
                    seeders=int(match.group("seeds")),
                    quality=quality_display_from_tags(quality_tags),
                    quality_tags=quality_tags,
                    raw={"detail_url": detail_url, "added": normalize_title(match.group("added")), "peers": int(match.group("peers"))},
                )
            )
            if len(results) >= max(limit * 2, 8):
                break
        return results


class TPBSource(SourceAdapter):
    name = "tpb"
    channel = "torrent"
    priority = 2

    def search(self, query: str, intent: SearchIntent, limit: int, page: int, http_client: HTTPClient) -> list[SearchResult]:
        url = f"https://apibay.org/q.php?q={urllib.parse.quote(query)}&cat=0"
        payload = http_client.get_json(url)
        if not isinstance(payload, list):
            return []
        results: list[SearchResult] = []
        for item in payload[: max(limit * 3, 12)]:
            name = normalize_title(item.get("name", ""))
            if not name or name == "No results returned":
                continue
            info_hash = (item.get("info_hash") or "").lower()
            quality_tags = parse_quality_tags(name)
            results.append(
                SearchResult(
                    channel="torrent",
                    source=self.name,
                    provider="magnet",
                    title=name,
                    link_or_magnet=_make_magnet(info_hash, name),
                    share_id_or_info_hash=info_hash,
                    size=_format_size(item.get("size", 0)),
                    seeders=int(item.get("seeders", 0)),
                    quality=quality_display_from_tags(quality_tags),
                    quality_tags=quality_tags,
                    raw=item,
                )
            )
        return results


class NyaaSource(SourceAdapter):
    name = "nyaa"
    channel = "torrent"
    priority = 1

    def search(self, query: str, intent: SearchIntent, limit: int, page: int, http_client: HTTPClient) -> list[SearchResult]:
        category = "1_2" if intent.kind == "anime" else "0_0"
        url = f"https://nyaa.si/?f=0&c={category}&q={urllib.parse.quote(query)}&page=rss"
        payload = http_client.get_text(url)
        root = ElementTree.fromstring(payload)
        results: list[SearchResult] = []
        for item in root.findall("./channel/item")[: max(limit * 3, 12)]:
            title = normalize_title(item.findtext("title", ""))
            magnet = item.findtext("{https://nyaa.si/xmlns/nyaa}magnetUri", "")
            info_hash = extract_share_id(magnet, provider_hint="magnet")
            seeders = int(item.findtext("{https://nyaa.si/xmlns/nyaa}seeders", "0"))
            quality_tags = parse_quality_tags(title)
            results.append(
                SearchResult(
                    channel="torrent",
                    source=self.name,
                    provider="magnet",
                    title=title,
                    link_or_magnet=_clean_magnet(magnet),
                    share_id_or_info_hash=info_hash,
                    size=item.findtext("{https://nyaa.si/xmlns/nyaa}size", ""),
                    seeders=seeders,
                    quality=quality_display_from_tags(quality_tags),
                    quality_tags=quality_tags,
                    raw={"title": title, "seeders": seeders},
                )
            )
        return results


class EZTVSource(SourceAdapter):
    name = "eztv"
    channel = "torrent"
    priority = 1

    def search(self, query: str, intent: SearchIntent, limit: int, page: int, http_client: HTTPClient) -> list[SearchResult]:
        url = "https://eztv.re/api/get-torrents?" + urllib.parse.urlencode(
            {"imdb_id": 0, "limit": max(limit * 3, 20), "page": page, "keywords": query}
        )
        payload = http_client.get_json(url)
        items = payload.get("torrents") or []
        results: list[SearchResult] = []
        for item in items[: max(limit * 3, 12)]:
            title = normalize_title(item.get("title", ""))
            magnet = item.get("magnet_url") or ""
            info_hash = (item.get("hash") or "").lower()
            if not magnet and info_hash:
                magnet = _make_magnet(info_hash, title)
            if not title or not magnet:
                continue
            quality_tags = parse_quality_tags(title)
            results.append(
                SearchResult(
                    channel="torrent",
                    source=self.name,
                    provider="magnet",
                    title=title,
                    link_or_magnet=magnet,
                    share_id_or_info_hash=info_hash or extract_share_id(magnet, "magnet"),
                    size=_format_size(item.get("size_bytes", 0)),
                    seeders=int(item.get("seeds", 0)),
                    quality=quality_display_from_tags(quality_tags),
                    quality_tags=quality_tags,
                    raw=item,
                )
            )
        return results


class YTSSource(SourceAdapter):
    name = "yts"
    channel = "torrent"
    priority = 2

    def search(self, query: str, intent: SearchIntent, limit: int, page: int, http_client: HTTPClient) -> list[SearchResult]:
        url = "https://yts.mx/api/v2/list_movies.json?" + urllib.parse.urlencode(
            {"query_term": query, "limit": max(limit * 3, 20), "sort_by": "seeds"}
        )
        payload = http_client.get_json(url)
        movies = payload.get("data", {}).get("movies") or []
        results: list[SearchResult] = []
        for movie in movies[: max(limit * 2, 10)]:
            title = normalize_title(movie.get("title_long") or movie.get("title") or "")
            for torrent in movie.get("torrents", []):
                info_hash = (torrent.get("hash") or "").lower()
                full_title = compact_spaces(f"{title} {torrent.get('quality', '')} {torrent.get('video_codec', '')}")
                quality_tags = parse_quality_tags(full_title)
                results.append(
                    SearchResult(
                        channel="torrent",
                        source=self.name,
                        provider="magnet",
                        title=full_title,
                        link_or_magnet=_make_magnet(info_hash, full_title),
                        share_id_or_info_hash=info_hash,
                        size=torrent.get("size", ""),
                        seeders=int(torrent.get("seeds", 0)),
                        quality=quality_display_from_tags(quality_tags),
                        quality_tags=quality_tags,
                        raw=torrent,
                    )
                )
        return results


class OneThreeThreeSevenXSource(SourceAdapter):
    name = "1337x"
    channel = "torrent"
    priority = 3

    SEARCH_ROW_RE = re.compile(
        r'<a href="(?P<detail>/torrent/[^"]+)"[^>]*>(?P<title>[^<]+)</a>.*?'
        r'class="coll-4[^"]*">(?P<size>.*?)</td>.*?'
        r'class="coll-2[^"]*">(?P<seeds>\d+)</td>.*?'
        r'class="coll-3[^"]*">(?P<leeches>\d+)</td>',
        re.S,
    )

    def search(self, query: str, intent: SearchIntent, limit: int, page: int, http_client: HTTPClient) -> list[SearchResult]:
        url = f"https://www.1377x.to/search/{urllib.parse.quote(query)}/{page}/"
        payload = http_client.get_text(url)
        results: list[SearchResult] = []
        for match in self.SEARCH_ROW_RE.finditer(payload):
            detail_path = html.unescape(match.group("detail"))
            detail_url = "https://www.1377x.to" + detail_path
            detail_payload = http_client.get_text(detail_url)
            magnet_match = re.search(r'href="(magnet:[^"]+)"', detail_payload)
            if not magnet_match:
                continue
            title = normalize_title(html.unescape(match.group("title")))
            magnet = _clean_magnet(magnet_match.group(1))
            info_hash = extract_share_id(magnet, provider_hint="magnet")
            quality_tags = parse_quality_tags(title)
            results.append(
                SearchResult(
                    channel="torrent",
                    source=self.name,
                    provider="magnet",
                    title=title,
                    link_or_magnet=magnet,
                    share_id_or_info_hash=info_hash,
                    size=normalize_title(html.unescape(match.group("size"))),
                    seeders=int(match.group("seeds")),
                    quality=quality_display_from_tags(quality_tags),
                    quality_tags=quality_tags,
                    raw={"detail_url": detail_url},
                )
            )
            if len(results) >= max(limit * 2, 8):
                break
        return results


__all__ = [
    "AliasResolver",
    "DEFAULT_HEADERS",
    "AnimeToshoSource",
    "DaliPanSource",
    "DMHYSource",
    "EZTVSource",
    "HTTPClient",
    "HunhepanSource",
    "NyaaSource",
    "OneThreeThreeSevenXSource",
    "PansouVipSource",
    "TorlockSource",
    "RESOURCE_URL_RE",
    "SOURCE_RUNTIME_PROFILES",
    "SourceAdapter",
    "SourceRuntimeProfile",
    "TIEBA_PAN_CLUE_RE",
    "TPBSource",
    "TRACKERS",
    "TiebaSource",
    "TwoFunSource",
    "YTSSource",
    "_clean_magnet",
    "_extract_embedded_resource_results",
    "_extract_tieba_clue_results",
    "_flatten_pan_payload",
    "_format_size",
    "_make_magnet",
    "_profile_for",
    "_validate_pan_payload",
]
