from __future__ import annotations

import hashlib
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, replace
from typing import Any
from xml.etree import ElementTree

from .cache import ResourceCache
from .common import (
    clean_share_url,
    compact_spaces,
    detect_kind,
    extract_chinese_alias,
    extract_english_alias,
    extract_password,
    extract_season_episode,
    extract_share_id,
    extract_year,
    infer_provider_from_url,
    is_video_url,
    normalize_key,
    normalize_title,
    parse_quality_tags,
    quality_display_from_tags,
    source_priority,
    title_core,
    title_tokens,
    token_overlap_score,
    unique_preserve,
)
from .models import SearchIntent, SearchPlan, SearchResult, SourceStatus


DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "*/*",
}

PAN_PROVIDER_SCORE = {
    "aliyun": 12,
    "quark": 11,
    "115": 10,
    "pikpak": 9,
    "uc": 8,
    "baidu": 7,
    "123": 6,
    "xunlei": 5,
    "tianyi": 4,
    "other": 1,
}

TRACKERS = (
    "&tr=udp://tracker.openbittorrent.com:80"
    "&tr=udp://tracker.opentrackr.org:1337"
    "&tr=udp://open.demonii.com:1337"
    "&tr=udp://tracker.torrent.eu.org:451"
    "&tr=udp://tracker.cyberia.is:6969"
)

MATCH_BUCKET_ORDER = {
    "exact_title_episode": 0,
    "title_family_match": 1,
    "episode_only_match": 2,
    "weak_context_match": 3,
}

BUCKET_LABELS = {
    "exact_title_episode": "Top matches",
    "title_family_match": "Related matches",
    "episode_only_match": "Loose matches",
    "weak_context_match": "Loose matches",
}


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
    "nyaa": SourceRuntimeProfile(timeout=8, retries=1, degraded_score_penalty=0, cooldown_seconds=180, failure_threshold=2),
    "eztv": SourceRuntimeProfile(timeout=10, retries=1, degraded_score_penalty=0, cooldown_seconds=180, failure_threshold=2),
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
        for attempt in range(self.retries + 1):
            request = urllib.request.Request(url, headers=DEFAULT_HEADERS)
            try:
                with urllib.request.urlopen(request, timeout=timeout) as response:
                    charset = response.headers.get_content_charset() or "utf-8"
                    return response.read().decode(charset, errors="replace")
            except urllib.error.HTTPError as exc:
                last_error = f"HTTP {exc.code}"
                if 400 <= exc.code < 500:
                    break
            except Exception as exc:  # pragma: no cover
                last_error = str(exc)
            if attempt < self.retries:
                time.sleep(0.2 * (attempt + 1))
        raise RuntimeError(last_error or "request failed")

    def get_text(self, url: str, timeout: int | None = None) -> str:
        return self._request(url, timeout=timeout)

    def get_json(self, url: str, timeout: int | None = None) -> dict[str, Any]:
        payload = self._request(url, timeout=timeout)
        try:
            return json.loads(payload)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"invalid json from {url}: {exc}") from exc


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

    def resolve(self, intent: SearchIntent, cache: ResourceCache, http_client: HTTPClient) -> dict[str, Any]:
        if intent.kind not in {"movie", "general"} or not intent.chinese_title_core or not intent.year or intent.english_alias:
            return {}
        cache_key = hashlib.sha256(f"alias_v7|{intent.chinese_title_core}|{intent.year}".encode("utf-8")).hexdigest()
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
        raise RuntimeError(f"unexpected payload type from {source_name}")
    if "results" in payload and isinstance(payload["results"], list):
        return payload
    if "data" in payload and isinstance(payload["data"], (list, dict)):
        return payload
    raise RuntimeError(f"unexpected pan payload shape from {source_name}")


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


def parse_intent(
    query: str,
    explicit_kind: str | None = None,
    channel: str = "both",
    quick: bool = False,
    wants_sub: bool = False,
    wants_4k: bool = False,
) -> SearchIntent:
    season, episode = extract_season_episode(query)
    english_alias = extract_english_alias(query)
    chinese_alias = extract_chinese_alias(query)
    kind = detect_kind(query, explicit_kind)
    query_title_core = title_core(query) or title_core(english_alias) or title_core(chinese_alias)
    return SearchIntent(
        query=compact_spaces(query),
        original_query=query,
        kind=kind,
        channel=channel,
        english_alias=english_alias,
        chinese_alias=chinese_alias,
        year=extract_year(query),
        season=season,
        episode=episode,
        wants_sub=wants_sub,
        wants_4k=wants_4k,
        quick=quick,
        is_video_url=is_video_url(query),
        title_core=query_title_core,
        title_tokens=title_tokens(query_title_core or query),
        english_title_core=title_core(english_alias),
        chinese_title_core=title_core(chinese_alias),
        resolved_titles=[],
        resolved_year="",
        alias_resolution={},
    )


def enrich_intent_with_aliases(intent: SearchIntent, alias_resolution: dict[str, Any]) -> SearchIntent:
    if not alias_resolution:
        return intent
    resolved_titles = unique_preserve(
        [
            alias_resolution.get("english_title", ""),
            alias_resolution.get("romanized_title", ""),
            *alias_resolution.get("alternate_titles", []),
        ]
    )
    english_alias = intent.english_alias or alias_resolution.get("english_title", "")
    resolved_year = alias_resolution.get("resolved_year") or intent.year
    return replace(
        intent,
        kind="movie" if intent.kind == "general" else intent.kind,
        english_alias=english_alias,
        english_title_core=title_core(english_alias),
        resolved_titles=resolved_titles,
        resolved_year=resolved_year,
        alias_resolution=alias_resolution,
    )


def build_plan(intent: SearchIntent) -> SearchPlan:
    if intent.is_video_url:
        return SearchPlan(channels=["video"], notes=["url routed to video pipeline"])

    if intent.channel == "pan":
        channels = ["pan"]
    elif intent.channel == "torrent":
        channels = ["torrent"]
    elif intent.kind in {"anime", "tv"}:
        channels = ["torrent", "pan"]
    else:
        channels = ["pan", "torrent"]

    pan_queries: list[str] = []
    torrent_queries: list[str] = []
    title_variant = intent.title_core
    english_variant = intent.english_title_core or intent.english_alias
    chinese_variant = intent.chinese_title_core or intent.chinese_alias
    resolved_variants = unique_preserve(
        [*intent.resolved_titles, *[title_core(item) or item for item in intent.resolved_titles]]
    )

    if "pan" in channels:
        pan_queries.extend([intent.query, title_variant, chinese_variant, english_variant, *resolved_variants])
        if intent.year and english_variant:
            pan_queries.append(compact_spaces(f"{english_variant} {intent.year}"))
        for variant in resolved_variants:
            if intent.year:
                pan_queries.append(compact_spaces(f"{variant} {intent.resolved_year or intent.year}"))
        if intent.wants_sub:
            pan_queries.extend(
                [
                    compact_spaces(f"{title_variant or intent.query} subtitles"),
                    compact_spaces(f"{chinese_variant or intent.query} 中文字幕"),
                ]
            )
        if intent.wants_4k:
            pan_queries.extend(
                [
                    compact_spaces(f"{title_variant or intent.query} 4K"),
                    compact_spaces(f"{title_variant or intent.query} 2160p"),
                ]
            )
        if intent.kind == "music" and "无损" not in intent.query:
            pan_queries.append(compact_spaces(f"{intent.query} 无损"))

    if "torrent" in channels:
        full_variant = intent.english_alias or intent.query
        torrent_queries.extend([intent.query, full_variant, title_variant, english_variant, *resolved_variants])
        if intent.year and title_variant:
            torrent_queries.append(compact_spaces(f"{title_variant} {intent.year}"))
        for variant in resolved_variants:
            if intent.year:
                torrent_queries.append(compact_spaces(f"{variant} {intent.resolved_year or intent.year}"))
        if intent.wants_4k:
            torrent_queries.append(compact_spaces(f"{title_variant or full_variant or intent.query} 2160p"))
        if intent.wants_sub:
            torrent_queries.append(compact_spaces(f"{title_variant or full_variant or intent.query} subtitles"))

    plan = SearchPlan(
        channels=channels,
        pan_queries=unique_preserve(pan_queries),
        torrent_queries=unique_preserve(torrent_queries),
        notes=[],
    )

    if intent.kind == "anime":
        plan.preferred_pan_sources = ["2fun", "hunhepan", "pansou.vip"]
        plan.preferred_torrent_sources = ["nyaa", "tpb", "1337x", "yts", "eztv"]
        plan.notes.append("anime prefers nyaa before pan sources")
    elif intent.kind == "tv":
        plan.preferred_pan_sources = ["2fun", "hunhepan", "pansou.vip"]
        plan.preferred_torrent_sources = ["eztv", "tpb", "1337x", "nyaa", "yts"]
        plan.notes.append("tv prefers eztv/tpb before pan sources")
    elif intent.kind == "movie":
        plan.preferred_pan_sources = ["2fun", "hunhepan", "pansou.vip"]
        plan.preferred_torrent_sources = ["yts", "tpb", "1337x", "eztv", "nyaa"]
        plan.notes.append("movie prefers pan results, then yts/tpb torrents")
    else:
        plan.preferred_pan_sources = ["2fun", "hunhepan", "pansou.vip"]
        plan.preferred_torrent_sources = ["tpb", "1337x", "nyaa", "eztv", "yts"]
        plan.notes.append("general/software/music/book prefer pan results first")
    return plan


def _classify_failure_kind(error: str) -> str:
    lowered = (error or "").lower()
    if lowered.startswith("http 4"):
        return "http_4xx"
    if lowered.startswith("http 5"):
        return "http_5xx"
    if "invalid json" in lowered:
        return "json"
    if "unexpected pan payload shape" in lowered:
        return "shape"
    if "ssl" in lowered or "timed out" in lowered or "urlopen error" in lowered:
        return "network"
    if "circuit open" in lowered:
        return "circuit_open"
    return "unknown"


def _target_title_cores(intent: SearchIntent) -> list[str]:
    cores = [
        intent.title_core,
        intent.english_title_core,
        intent.chinese_title_core,
    ]
    cores.extend([title_core(item) or item for item in intent.resolved_titles])
    return unique_preserve([core for core in cores if core])


def _result_title_signals(intent: SearchIntent, title: str) -> dict[str, Any]:
    title_core_value = title_core(title)
    title_tokens_value = title_tokens(title_core_value or title)
    target_cores = _target_title_cores(intent)
    target_token_sets = [title_tokens(core) for core in target_cores]
    target_core_keys = [normalize_key(core) for core in target_cores if normalize_key(core)]
    title_core_key = normalize_key(title_core_value or title)
    query_overlap = max((token_overlap_score(title_tokens(core), title_tokens_value) for core in target_cores), default=0.0)
    overlap = query_overlap
    exact_core_match = bool(title_core_key and title_core_key in target_core_keys)
    alias_match = bool(title_core_key and not exact_core_match and overlap >= 0.82)
    starts_with_target = any(tokens and title_tokens_value[: len(tokens)] == tokens for tokens in target_token_sets)
    season_match = bool(
        intent.season is None
        or re.search(rf"s0?{intent.season}(?:e|\b)", title, re.I)
        or re.search(rf"season\s*0?{intent.season}\b", title, re.I)
        or re.search(rf"\u7b2c\s*0?{intent.season}\s*\u5b63", title)
    )
    episode_match = bool(
        intent.episode is None
        or re.search(rf"(?:e|x)0?{intent.episode}\b", title, re.I)
        or re.search(rf"episode\s*0?{intent.episode}\b", title, re.I)
        or re.search(rf"\u7b2c\s*0?{intent.episode}\s*\u96c6", title)
    )
    year_match = bool(intent.year and intent.year in title)
    return {
        "title_core": title_core_value,
        "title_tokens": title_tokens_value,
        "overlap": overlap,
        "exact_core_match": exact_core_match,
        "alias_match": alias_match,
        "season_match": season_match,
        "episode_match": episode_match,
        "year_match": year_match,
        "target_cores": target_cores,
        "starts_with_target": starts_with_target,
    }


def classify_result(result: SearchResult, intent: SearchIntent) -> tuple[str, float, list[str], list[str], dict[str, Any]]:
    signals = _result_title_signals(intent, result.title)
    reasons: list[str] = []
    penalties: list[str] = []

    if signals["exact_core_match"]:
        reasons.append("canonical title match")
    elif signals["alias_match"]:
        reasons.append("alias match")
    elif signals["overlap"] >= 0.8:
        reasons.append("strong title-family match")
    elif signals["overlap"] >= 0.45:
        reasons.append("partial title-family match")
    elif signals["overlap"] > 0:
        reasons.append("weak context match")

    if signals["year_match"]:
        reasons.append("year match")
    if intent.season is not None and signals["season_match"]:
        reasons.append("season match")
    if intent.episode is not None and signals["episode_match"]:
        reasons.append("episode match")

    if intent.kind in {"tv", "anime"} and (intent.season is not None or intent.episode is not None):
        if (signals["exact_core_match"] or (signals["starts_with_target"] and signals["overlap"] >= 0.55) or signals["overlap"] >= 0.94) and signals["episode_match"] and signals["season_match"]:
            return "exact_title_episode", 0.96, reasons, penalties, signals
        if signals["exact_core_match"] or signals["alias_match"] or signals["overlap"] >= 0.45:
            return "title_family_match", 0.78 if signals["overlap"] >= 0.6 else 0.62, reasons, penalties, signals
        if signals["episode_match"] or signals["season_match"]:
            penalties.append("episode without title-family match")
            return "episode_only_match", 0.28, reasons, penalties, signals
        penalties.append("weak context only")
        return "weak_context_match", 0.12, reasons, penalties, signals

    if signals["exact_core_match"] or signals["alias_match"] or signals["overlap"] >= 0.78:
        return "title_family_match", 0.9 if signals["exact_core_match"] else 0.74, reasons, penalties, signals
    if signals["overlap"] >= 0.35:
        return "title_family_match", 0.52, reasons, penalties, signals
    penalties.append("weak context only")
    return "weak_context_match", 0.14, reasons, penalties, signals


def _source_is_degraded(cache: ResourceCache, source_name: str) -> bool:
    profile = _profile_for(source_name)
    if not profile.default_degraded:
        latest = cache.latest_source_status(source_name)
        return bool(latest and latest.get("degraded"))
    latest = cache.latest_source_status(source_name)
    if latest and latest.get("ok") and latest.get("failure_kind") == "probe_ok":
        return False
    last_failure = cache.latest_failure_epoch(source_name, within_seconds=900)
    recovery_since = last_failure if last_failure is not None else (time.time() - 900)
    if cache.count_real_successes_since(source_name, recovery_since, within_seconds=900) >= 2:
        return False
    return True


def score_result(result: SearchResult, intent: SearchIntent, cache: ResourceCache | None = None) -> SearchResult:
    bucket, confidence, reasons, penalties, signals = classify_result(result, intent)
    result.match_bucket = bucket
    result.confidence = round(confidence, 3)
    result.reasons = unique_preserve(reasons)
    result.penalties = unique_preserve(penalties)

    tags = result.quality_tags or parse_quality_tags(result.title)
    result.quality_tags = tags
    result.quality = quality_display_from_tags(tags)

    score = {
        "exact_title_episode": 145,
        "title_family_match": 95,
        "episode_only_match": 20,
        "weak_context_match": -5,
    }[bucket]

    if signals["exact_core_match"]:
        score += 28
    if signals["alias_match"]:
        score += 16
    score += int(signals["overlap"] * 30)
    if signals["year_match"]:
        score += 10
    if intent.season is not None and signals["season_match"]:
        score += 8
    if intent.episode is not None and signals["episode_match"]:
        score += 12

    resolution = tags.get("resolution")
    if resolution == "2160p":
        score += 18
        result.reasons.append("4k resolution")
    elif resolution == "1080p":
        score += 10
        result.reasons.append("1080p resolution")
    elif resolution == "720p":
        score += 4
        result.reasons.append("720p resolution")

    source_type = tags.get("source")
    if source_type == "bluray":
        score += 8
        result.reasons.append("bluray source")
    elif source_type == "web-dl":
        score += 5
        result.reasons.append("web-dl source")
    elif source_type in {"webrip", "hdtv"}:
        score += 2
        result.reasons.append(f"{source_type} source")
    elif source_type == "cam":
        score -= 30
        result.penalties.append("cam-quality release")

    if tags.get("pack") == "remux":
        score += 4
        result.reasons.append("remux pack")
    if tags.get("hdr_flags"):
        score += min(8, 4 * len(tags["hdr_flags"]))
        result.reasons.append("hdr flags")
    if intent.wants_sub and tags.get("subtitle"):
        score += 12
        result.reasons.append("subtitle requested")
    if intent.wants_4k and resolution == "2160p":
        score += 20
        result.reasons.append("4k requested")

    if result.channel == "pan":
        score += PAN_PROVIDER_SCORE.get(result.provider, PAN_PROVIDER_SCORE["other"])
        if result.password:
            score += 6
            result.reasons.append("has extraction code")
    if result.channel == "torrent" and result.seeders:
        score += min(result.seeders, 240) // 6
        result.reasons.append("seeders")

    score += max(0, 12 - source_priority(result.source))
    result.reasons.append(f"source priority {source_priority(result.source)}")

    if bucket == "episode_only_match":
        score -= 55
        result.penalties.append("episode-only match penalty")
    elif bucket == "weak_context_match":
        score -= 30
        result.penalties.append("weak-context penalty")

    if cache and _source_is_degraded(cache, result.source):
        penalty = _profile_for(result.source).degraded_score_penalty
        if penalty:
            score -= penalty
            result.source_degraded = True
            result.penalties.append(f"degraded source penalty ({penalty})")

    result.score = score
    result.reasons = unique_preserve(result.reasons)
    result.penalties = unique_preserve(result.penalties)
    return result


def deduplicate_results(results: list[SearchResult]) -> list[SearchResult]:
    chosen: dict[str, SearchResult] = {}
    for result in results:
        if result.channel == "pan":
            key = f"pan:{result.provider}:{result.share_id_or_info_hash}"
        else:
            fallback = result.share_id_or_info_hash or normalize_key(result.title)[:64]
            key = f"torrent:{fallback}"
        current = chosen.get(key)
        if not current:
            chosen[key] = result
            continue
        if result.password and not current.password:
            chosen[key] = result
            continue
        if result.seeders > current.seeders:
            chosen[key] = result
    return list(chosen.values())


class ResourceHunterEngine:
    def __init__(self, cache: ResourceCache | None = None, http_client: HTTPClient | None = None) -> None:
        self.cache = cache or ResourceCache()
        self.http_client = http_client or HTTPClient(retries=1, default_timeout=10)
        self.alias_resolver = AliasResolver()
        self.pan_sources: list[SourceAdapter] = [TwoFunSource(), HunhepanSource(), PansouVipSource()]
        self.torrent_sources: list[SourceAdapter] = [
            NyaaSource(),
            EZTVSource(),
            TPBSource(),
            YTSSource(),
            OneThreeThreeSevenXSource(),
        ]

    def _resolve_aliases(self, intent: SearchIntent) -> SearchIntent:
        alias_resolution = self.alias_resolver.resolve(intent, self.cache, self.http_client)
        return enrich_intent_with_aliases(intent, alias_resolution)

    def _cache_key(self, intent: SearchIntent, plan: SearchPlan, page: int, limit: int) -> str:
        payload = json.dumps(
            {
                "schema_version": "precision_with_broad_recall_v1",
                "intent": intent.to_dict(),
                "plan": plan.to_dict(),
                "resolved_titles": intent.resolved_titles,
                "resolved_year": intent.resolved_year,
                "page": page,
                "limit": limit,
            },
            sort_keys=True,
            ensure_ascii=False,
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _ordered_sources(self, channel: str, plan: SearchPlan) -> list[SourceAdapter]:
        if channel == "pan":
            preferred = {name: index for index, name in enumerate(plan.preferred_pan_sources)}
            catalog = self.pan_sources
        else:
            preferred = {name: index for index, name in enumerate(plan.preferred_torrent_sources)}
            catalog = self.torrent_sources
        return sorted(
            catalog,
            key=lambda item: (
                preferred.get(item.name, 999) + (100 if _source_is_degraded(self.cache, item.name) else 0),
                item.priority,
            ),
        )

    def _search_source(
        self,
        source: SourceAdapter,
        channel: str,
        queries: list[str],
        intent: SearchIntent,
        page: int,
        limit: int,
    ) -> tuple[SourceStatus, list[SearchResult]]:
        profile = _profile_for(source.name)
        degraded_before_search = _source_is_degraded(self.cache, source.name)
        if self.cache.should_skip_source(source.name, profile.cooldown_seconds, profile.failure_threshold):
            status = SourceStatus(
                source=source.name,
                channel=channel,
                priority=source.priority,
                ok=False,
                skipped=True,
                degraded=degraded_before_search or profile.default_degraded,
                error="circuit open from recent failures",
                failure_kind="circuit_open",
            )
            self.cache.record_source_status(status)
            return status, []

        source_results: list[SearchResult] = []
        status = SourceStatus(
            source=source.name,
            channel=channel,
            priority=source.priority,
            ok=True,
            degraded=degraded_before_search,
        )
        client = HTTPClient(retries=profile.retries, default_timeout=profile.timeout)
        query_budget = 1 if (profile.default_degraded or degraded_before_search) else 2
        for query in queries[:query_budget]:
            if not query:
                continue
            started = time.time()
            try:
                batch = source.search(query, intent, limit, page, client)
                status.latency_ms = int((time.time() - started) * 1000)
                status.ok = True
                status.error = ""
                status.failure_kind = ""
                if batch:
                    status.degraded = degraded_before_search
                    source_results.extend(batch)
                    break
            except Exception as exc:
                status.ok = False
                status.latency_ms = int((time.time() - started) * 1000)
                status.error = str(exc)[:200]
                status.failure_kind = _classify_failure_kind(status.error)
                status.degraded = profile.default_degraded or degraded_before_search
        self.cache.record_source_status(status)
        return status, source_results

    def search(
        self,
        intent: SearchIntent,
        plan: SearchPlan | None = None,
        page: int = 1,
        limit: int = 8,
        use_cache: bool = True,
    ) -> dict[str, Any]:
        intent = self._resolve_aliases(intent)
        plan = plan or build_plan(intent)
        cache_key = self._cache_key(intent, plan, page, limit)
        if use_cache:
            cached = self.cache.get_search_cache(cache_key)
            if cached:
                cached.setdefault("meta", {})
                cached["meta"]["cached"] = True
                return cached

        results: list[SearchResult] = []
        statuses: list[SourceStatus] = []
        warnings: list[str] = []

        for channel in plan.channels:
            queries = plan.pan_queries if channel == "pan" else plan.torrent_queries
            ordered_sources = self._ordered_sources(channel, plan)
            with ThreadPoolExecutor(max_workers=min(4, len(ordered_sources) or 1)) as executor:
                futures = [
                    executor.submit(self._search_source, source, channel, queries, intent, page, limit)
                    for source in ordered_sources
                ]
                for future in as_completed(futures):
                    status, source_results = future.result()
                    statuses.append(status)
                    results.extend(source_results)

        results = deduplicate_results(results)
        results = [score_result(result, intent, cache=self.cache) for result in results]
        results.sort(
            key=lambda item: (
                MATCH_BUCKET_ORDER.get(item.match_bucket, 9),
                -item.score,
                -item.seeders,
                item.source_degraded,
                item.title.lower(),
            )
        )
        statuses.sort(key=lambda item: (item.channel, item.priority, item.source))

        if not results:
            warnings.append("no results returned from active sources")

        response = {
            "query": intent.original_query,
            "intent": intent.to_dict(),
            "plan": plan.to_dict(),
            "results": [result.to_public_dict() for result in results],
            "warnings": warnings,
            "source_status": [status.to_dict() for status in statuses],
            "meta": {
                "cached": False,
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "limit": limit,
                "page": page,
                "candidate_count": len(results),
                "effective_limit": limit,
                "alias_resolution": intent.alias_resolution,
                "resolved_titles": intent.resolved_titles,
                "resolved_year": intent.resolved_year or intent.year,
            },
        }
        if use_cache:
            self.cache.set_search_cache(cache_key, response, ttl_seconds=300)
        return response

    def source_catalog(self, probe: bool = False) -> dict[str, Any]:
        sources: list[dict[str, Any]] = []
        cached_status = {row["source"]: row for row in self.cache.list_source_statuses()}
        all_sources = self.pan_sources + self.torrent_sources
        for adapter in sorted(all_sources, key=lambda item: (item.channel, item.priority, item.name)):
            status_info = cached_status.get(adapter.name, {})
            if probe:
                profile = _profile_for(adapter.name)
                started = time.time()
                ok, error = adapter.healthcheck(HTTPClient(retries=profile.retries, default_timeout=profile.timeout))
                status = SourceStatus(
                    source=adapter.name,
                    channel=adapter.channel,
                    priority=adapter.priority,
                    ok=ok,
                    degraded=False if ok else profile.default_degraded,
                    error=error,
                    failure_kind="probe_ok" if ok else _classify_failure_kind(error),
                    latency_ms=int((time.time() - started) * 1000),
                )
                self.cache.record_source_status(status)
                status_info = status.to_dict()
            sources.append(
                {
                    "source": adapter.name,
                    "channel": adapter.channel,
                    "priority": adapter.priority,
                    "recent_status": {
                        "ok": bool(status_info.get("ok")) if status_info else None,
                        "skipped": bool(status_info.get("skipped")) if status_info else False,
                        "degraded": bool(status_info.get("degraded")) if status_info else _source_is_degraded(self.cache, adapter.name),
                        "latency_ms": status_info.get("latency_ms"),
                        "error": status_info.get("error", ""),
                        "failure_kind": status_info.get("failure_kind", ""),
                        "checked_at": status_info.get("checked_at"),
                    },
                }
            )
        return {"sources": sources, "meta": {"probe": probe}}


def format_search_text(response: dict[str, Any], max_results: int | None = None) -> str:
    intent = response["intent"]
    plan = response["plan"]
    results = response["results"]
    meta = response.get("meta", {})
    limit = max_results if max_results is not None else meta.get("effective_limit", meta.get("limit", 8))
    selected = results[:limit]

    lines = [
        "Resource Hunter v2",
        f"Query: {response['query']}",
        f"Kind: {intent['kind']} | Channel: {' -> '.join(plan['channels'])}",
    ]
    if plan.get("notes"):
        lines.append("Plan: " + "; ".join(plan["notes"]))
    if meta.get("resolved_titles"):
        lines.append("Resolved titles: " + ", ".join(meta["resolved_titles"][:4]))
    lines.append("")

    if not selected:
        lines.append("No result matched the current query.")
    else:
        has_confident = any(item.get("match_bucket") in {"exact_title_episode", "title_family_match"} for item in selected)
        if not has_confident:
            lines.append("No confident match")
            lines.append("")
        grouped: dict[str, list[dict[str, Any]]] = {}
        for result in selected:
            grouped.setdefault(result.get("match_bucket", "weak_context_match"), []).append(result)
        seen_labels: set[str] = set()
        for bucket in ("exact_title_episode", "title_family_match", "episode_only_match", "weak_context_match"):
            bucket_items = grouped.get(bucket) or []
            if not bucket_items:
                continue
            label = BUCKET_LABELS[bucket]
            if label not in seen_labels:
                lines.append(label + ":")
                seen_labels.add(label)
            for result in bucket_items:
                summary_bits = [
                    f"{result['channel']}/{result['provider']}",
                    f"via {result['source']}",
                    f"bucket={result.get('match_bucket')}",
                    f"confidence={result.get('confidence')}",
                ]
                if result["quality"]:
                    summary_bits.append(result["quality"])
                if result["size"]:
                    summary_bits.append(result["size"])
                if result["seeders"]:
                    summary_bits.append(f"seeders={result['seeders']}")
                summary_bits.append(f"score={result['score']}")
                if result.get("source_degraded"):
                    summary_bits.append("degraded-source")
                lines.append(f"- {result['title']}")
                lines.append("  " + " | ".join(summary_bits))
                lines.append(f"  {result['link_or_magnet']}")
                if result["password"]:
                    lines.append(f"  password: {result['password']}")
                if result["reasons"]:
                    lines.append("  why: " + ", ".join(result["reasons"][:4]))
                if result.get("penalties"):
                    lines.append("  penalties: " + ", ".join(result["penalties"][:3]))
            lines.append("")

    if response.get("warnings"):
        lines.append("Warnings:")
        for warning in response["warnings"]:
            lines.append(f"- {warning}")
    if response.get("source_status"):
        lines.append("")
        lines.append("Source status:")
        for status in response["source_status"]:
            state = "ok" if status["ok"] else ("skipped" if status["skipped"] else "fail")
            if status.get("degraded"):
                state += "/degraded"
            detail = f"{status['source']} ({status['channel']}, p{status['priority']}): {state}"
            if status.get("latency_ms") is not None:
                detail += f", {status['latency_ms']}ms"
            if status.get("failure_kind"):
                detail += f", {status['failure_kind']}"
            if status.get("error"):
                detail += f", {status['error']}"
            lines.append(f"- {detail}")
    return "\n".join(lines).strip()


def format_sources_text(payload: dict[str, Any]) -> str:
    lines = ["Resource Hunter sources", ""]
    for item in payload["sources"]:
        status = item["recent_status"]
        state = "unknown"
        if status["ok"] is True:
            state = "ok"
        elif status["ok"] is False and status["skipped"]:
            state = "skipped"
        elif status["ok"] is False:
            state = "fail"
        if status.get("degraded"):
            state += "/degraded"
        lines.append(f"- {item['source']} | {item['channel']} | priority={item['priority']} | status={state}")
        if status.get("latency_ms") is not None or status.get("checked_at"):
            lines.append(
                f"  checked_at={status.get('checked_at') or '-'} latency_ms={status.get('latency_ms') or '-'}"
            )
        if status.get("failure_kind"):
            lines.append(f"  failure_kind={status['failure_kind']}")
        if status.get("error"):
            lines.append(f"  error={status['error']}")
    return "\n".join(lines)
