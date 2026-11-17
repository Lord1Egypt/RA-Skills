#!/usr/bin/env python3
"""Direct runtime CLI for pt-agent.

This script gives agent hosts a concrete executable surface when they do not
provide native tools yet. It intentionally supports only safe secret references
that can be resolved locally, currently env://NAME. Other providers should be
implemented by the host and passed through the same command shapes.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

try:
    import pt_store
except ImportError as exc:  # pragma: no cover
    raise SystemExit(f"Cannot import pt_store.py: {exc}") from exc


ROOT = Path(__file__).resolve().parents[1]
SITE_CATALOG = ROOT / "references" / "site-preset-catalog.json"
ADAPTER_CATALOG = ROOT / "references" / "adapter-catalog.json"
DEFAULT_TIMEOUT = 20
USER_AGENT = "pt-agent-runtime/0.1"
_JSON_CACHE: dict[Path, dict[str, Any]] = {}
_ADAPTER_INDEX: dict[str, dict[str, Any]] | None = None

SCHEMA_DEFAULTS: dict[str, dict[str, Any]] = {
    "nexusphp": {
        "searchPath": "/torrents.php",
        "keywordParam": "search",
        "extraParams": {"notnewword": "1"},
        "statsPaths": ["/index.php", "/userdetails.php", "/mybonus.php"],
        "downloadTemplate": "/download.php?id={id}",
        "detailPattern": "details.php",
        "downloadPattern": "download.php",
    },
    "unit3d": {
        "searchPath": "/torrents",
        "keywordParam": "name",
        "extraParams": {},
        "statsPaths": ["/users/me", "/profile", "/dashboard"],
        "detailPattern": "/torrents/",
    },
    "gazelle": {
        "searchPath": "/torrents.php",
        "keywordParam": "searchstr",
        "extraParams": {},
        "statsPaths": ["/index.php", "/user.php"],
        "detailPattern": "torrents.php",
    },
    "selector": {
        "searchPath": "/",
        "keywordParam": "q",
        "extraParams": {},
        "statsPaths": ["/"],
    },
}

NO_LOGIN_URL_RE = re.compile(r"(login|doLogin|verify|checkpoint|returnto)", re.I)
NO_LOGIN_TEXT_RE = re.compile(r"(auth_form|not authorized|please log in|login|password|\u767b\u5f55|\u767b\u5165)", re.I)
NO_RESULTS_TEXT_RE = re.compile(r"(\u6ca1\u6709\u79cd\u5b50|no [Tt]orrents?|Your search did not match anything|\u7528\u51c6\u786e\u7684\u5173\u952e\u5b57\u91cd\u8bd5)", re.I)
ROW_CLASS_HINTS = (
    "torrent-table-sub-info",
    "torrent-row",
    "torrent-item",
    "torrent-list-item",
)
VOID_HTML_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


class RuntimeErrorJson(Exception):
    def __init__(self, code: str, message: str, **extra: Any) -> None:
        self.payload = {"code": code, "message": message, **extra}
        super().__init__(message)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict[str, str]] = []
        self._active: dict[str, str] | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            data = {k.lower(): v or "" for k, v in attrs}
            self._active = data
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._active is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._active is not None:
            text = normalize_space("".join(self._text))
            item = dict(self._active)
            item["text"] = text
            self.links.append(item)
            self._active = None
            self._text = []


class SearchRowParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[str] = []
        self._depth = 0
        self._current: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag_name = tag.lower()
        class_value = " ".join(value or "" for key, value in attrs if key.lower() == "class").lower()
        is_row = tag_name == "tr" or any(hint in class_value for hint in ROW_CLASS_HINTS)
        if self._depth == 0 and is_row:
            self._depth = 1
            self._current = [self.get_starttag_text() or f"<{tag}>"]
        elif self._depth:
            self._current.append(self.get_starttag_text() or f"<{tag}>")
            if tag_name not in VOID_HTML_TAGS:
                self._depth += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self._depth:
            self._current.append(self.get_starttag_text() or f"<{tag}/>")

    def handle_endtag(self, tag: str) -> None:
        if self._depth:
            self._current.append(f"</{tag}>")
            self._depth -= 1
            if self._depth == 0:
                self.rows.append("".join(self._current))
                self._current = []

    def handle_data(self, data: str) -> None:
        if self._depth:
            self._current.append(data)


def emit(data: dict[str, Any]) -> int:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def fail(exc: RuntimeErrorJson) -> int:
    return emit({"ok": False, "error": exc.payload})


def load_json(path: Path) -> dict[str, Any]:
    cached = _JSON_CACHE.get(path)
    if cached is not None:
        return cached
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    _JSON_CACHE[path] = data
    return data


def adapter_index() -> dict[str, dict[str, Any]]:
    global _ADAPTER_INDEX
    if _ADAPTER_INDEX is None:
        _ADAPTER_INDEX = {item["id"]: item for item in load_json(ADAPTER_CATALOG).get("adapters", [])}
    return _ADAPTER_INDEX


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(value)).strip()


def normalize_id(value: str) -> str:
    return pt_store.normalize_id(value)


def resolve_ref(ref: str | None, purpose: str) -> str | None:
    if not ref:
        return None
    if not ref.startswith(("env://", "secret://", "profile://", "proxy://")):
        raise RuntimeErrorJson("unsafe_secret_ref", f"{purpose} must use env://, secret://, profile://, or proxy://.")
    if ref.startswith("env://"):
        name = ref.removeprefix("env://")
        value = os.environ.get(name)
        if not value:
            raise RuntimeErrorJson("secret_unavailable", f"Environment variable is not set for {purpose}.", ref=ref)
        return value
    if ref.startswith(("secret://", "profile://", "proxy://")):
        raise RuntimeErrorJson(
            "provider_unavailable",
            f"Current environment cannot resolve {ref.split('://', 1)[0]} references directly; use a supported secret/profile provider.",
            ref=ref,
        )
    raise RuntimeErrorJson("unsafe_secret_ref", f"{purpose} must be a reference such as env://NAME or secret://path.")


def request(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, str, bytes, dict[str, str]]:
    import urllib.error
    import urllib.request

    req = urllib.request.Request(url, method=method.upper(), data=data)
    req.add_header("User-Agent", USER_AGENT)
    for key, value in (headers or {}).items():
        req.add_header(key, value)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.geturl(), resp.read(), dict(resp.headers.items())
    except urllib.error.HTTPError as exc:
        body = exc.read()
        return exc.code, exc.geturl(), body, dict(exc.headers.items())
    except urllib.error.URLError as exc:
        raise RuntimeErrorJson("network_error", str(exc.reason)) from exc
    except TimeoutError as exc:
        raise RuntimeErrorJson("network_timeout", "The remote service did not respond before the timeout.") from exc


def assert_logged(status: int, final_url: str, body: bytes, headers: dict[str, str]) -> None:
    import urllib.parse

    if status in {401, 403, 502, 504}:
        raise RuntimeErrorJson("auth_required", "Tracker returned a login-like HTTP status.", statusCode=status)
    if NO_LOGIN_URL_RE.search(final_url):
        raise RuntimeErrorJson("auth_required", "Tracker redirected to a login-like URL.", finalUrlHost=urllib.parse.urlparse(final_url).netloc)
    refresh = headers.get("refresh") or headers.get("Refresh") or ""
    if refresh and NO_LOGIN_URL_RE.search(refresh):
        raise RuntimeErrorJson("auth_required", "Tracker returned a refresh-to-login header.")
    text = body[:1200].decode("utf-8", errors="ignore")
    if len(text) < 900 and NO_LOGIN_TEXT_RE.search(text):
        raise RuntimeErrorJson("auth_required", "Tracker response looks like a login page.")


def base_url_join(base_url: str, path: str) -> str:
    import urllib.parse

    return urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def schema_default(adapter_id: str | None) -> dict[str, Any]:
    return SCHEMA_DEFAULTS.get(str(adapter_id or ""), SCHEMA_DEFAULTS["selector"])


def get_secret_ref(secret_refs: dict[str, Any], *names: str) -> str | None:
    aliases = {
        "apiToken": ["apiToken", "api_token", "token"],
        "apiKey": ["apiKey", "api_key", "apikey", "api_token"],
        "cookie": ["cookie", "cookieRef"],
        "rssKey": ["rssKey", "rss_key", "passkey"],
    }
    for name in names:
        for key in aliases.get(name, [name]):
            value = secret_refs.get(key)
            if value:
                return str(value)
    return None


def tracker_headers(tracker: dict[str, Any]) -> dict[str, str]:
    headers: dict[str, str] = {}
    secret_refs = tracker.get("secretRefs") if isinstance(tracker.get("secretRefs"), dict) else {}
    cookie_ref = get_secret_ref(secret_refs, "cookie") or tracker.get("cookieRef")
    if tracker.get("authMode") == "cookie" or cookie_ref:
        cookie = resolve_ref(cookie_ref, "tracker cookie")
        headers["Cookie"] = cookie or ""
    token_ref = get_secret_ref(secret_refs, "apiToken", "apiKey") or tracker.get("apiKeyRef")
    if token_ref and tracker.get("adapterId") in {"unit3d-api", "gazelle-json"}:
        token = resolve_ref(token_ref, "tracker API token")
        headers["Authorization"] = f"Bearer {token}"
    return headers


def load_store(path: str | None) -> tuple[dict[str, Any], Path, str]:
    store_path, source = pt_store.resolve_store_path(path)
    try:
        return pt_store.load_store(store_path), store_path, source
    except pt_store.StoreError as exc:
        raise RuntimeErrorJson(exc.payload["code"], exc.payload["message"], store=str(store_path), storeSource=source) from exc


def find_tracker_record(store: dict[str, Any], tracker_id: str) -> dict[str, Any]:
    tracker_id = normalize_id(tracker_id)
    for bucket in ("trackers", "trackerDrafts"):
        record = store.get(bucket, {}).get(tracker_id)
        if record:
            return dict(record)
    record = pt_store.find_tracker(store, tracker_id)
    if record:
        return dict(record)
    query = normalize_id(tracker_id)
    matches: list[dict[str, Any]] = []
    for bucket in (store.get("trackers", {}), store.get("trackerDrafts", {})):
        for candidate in bucket.values():
            if not isinstance(candidate, dict):
                continue
            names = [
                candidate.get("id"),
                candidate.get("name"),
                candidate.get("displayName"),
                candidate.get("sitePresetId"),
                *(candidate.get("aka") if isinstance(candidate.get("aka"), list) else []),
            ]
            normalized = [normalize_id(str(name)) for name in names if name]
            if query and any(name.startswith(query) or query.startswith(name) for name in normalized):
                matches.append(candidate)
    unique = {str(item.get("id")): item for item in matches if item.get("id")}
    if len(unique) == 1:
        return dict(next(iter(unique.values())))
    if len(unique) > 1:
        raise RuntimeErrorJson("ambiguous_tracker", "Tracker alias matches more than one configured tracker.", matches=sorted(unique))
    raise RuntimeErrorJson("not_found", "Tracker is not configured.", trackerId=tracker_id)


def find_downloader_record(store: dict[str, Any], downloader_id: str) -> dict[str, Any]:
    downloader_id = normalize_id(downloader_id)
    record = store.get("downloaders", {}).get(downloader_id)
    if not record:
        raise RuntimeErrorJson("not_found", "Downloader is not configured.", downloaderId=downloader_id)
    return dict(record)


def tracker_is_enabled_config(tracker: dict[str, Any]) -> bool:
    if tracker.get("enabled") is False:
        return False
    status = tracker.get("status")
    if status not in {None, "active", "configured", "enabled"}:
        return False
    try:
        validate_tracker(tracker)
    except RuntimeErrorJson:
        return False
    return True


def site_presets(query: str) -> dict[str, Any]:
    catalog = load_json(SITE_CATALOG)
    q = query.strip().lower()
    matches = []
    for site in catalog.get("sites", []):
        candidates = [site.get("id"), site.get("displayName"), *(site.get("aka") or [])]
        if any(str(candidate or "").lower() == q for candidate in candidates):
            matches.append(site)
    if not matches:
        for site in catalog.get("sites", []):
            candidates = [site.get("id"), site.get("displayName"), *(site.get("aka") or [])]
            if any(q in str(candidate or "").lower() for candidate in candidates):
                matches.append(site)
    return {"ok": True, "sites": matches[:20], "total": len(matches)}


def adapter_presets(adapter_ids: list[str]) -> dict[str, Any]:
    catalog = load_json(ADAPTER_CATALOG)
    wanted = set(adapter_ids)
    adapters = [
        adapter
        for adapter in catalog.get("adapters", [])
        if not wanted or adapter.get("id") in wanted
    ]
    return {"ok": True, "adapters": adapters}


def validate_tracker(tracker: dict[str, Any]) -> dict[str, Any]:
    adapter_id = tracker.get("adapterId")
    if not adapter_id:
        raise RuntimeErrorJson("credential_validation_failed", "adapterId is required.")
    adapter = adapter_index().get(adapter_id)
    if not adapter:
        raise RuntimeErrorJson("adapter_not_available", "Unknown adapterId.", adapterId=adapter_id)
    auth_mode = tracker.get("authMode")
    allowed = adapter.get("authModes", [])
    if auth_mode not in allowed:
        raise RuntimeErrorJson(
            "auth_material_mismatch",
            "Credential type is not accepted by this adapter.",
            adapterId=adapter_id,
            providedAuthMode=auth_mode,
            supportedAuthModes=allowed,
        )
    secret_refs = tracker.get("secretRefs") if isinstance(tracker.get("secretRefs"), dict) else {}
    missing: list[str] = []
    if auth_mode == "browser_profile" and not tracker.get("profileRef"):
        missing.append("profileRef")
    if auth_mode == "cookie" and not (get_secret_ref(secret_refs, "cookie") or tracker.get("cookieRef")):
        missing.append("secretRefs.cookie")
    if auth_mode == "api_token" and not (
        get_secret_ref(secret_refs, "apiToken", "apiKey") or tracker.get("apiKeyRef")
    ):
        missing.append("secretRefs.apiToken")
    if auth_mode == "rss_token" and not (get_secret_ref(secret_refs, "rssKey") or tracker.get("feedUrl") or tracker.get("feedUrlRef")):
        missing.append("feedUrl or secretRefs.rssKey")
    if missing:
        raise RuntimeErrorJson(
            "credential_validation_failed",
            "Required credential reference fields are missing.",
            adapterId=adapter_id,
            authMode=auth_mode,
            missing=missing,
        )
    return {
        "ok": True,
        "status": "statically_valid",
        "adapterId": adapter_id,
        "authMode": auth_mode,
        "capabilities": adapter.get("capabilities", []),
    }


def health_check(tracker: dict[str, Any]) -> dict[str, Any]:
    import urllib.parse

    validate_tracker(tracker)
    if tracker.get("authMode") == "browser_profile":
        raise RuntimeErrorJson(
            "provider_unavailable",
            "Current environment cannot use browser profiles directly; use cookie/env or a supported browser profile provider.",
        )
    base_url = tracker.get("baseUrl")
    if not base_url:
        raise RuntimeErrorJson("validation_failed", "baseUrl is required.")
    status, final_url, body, _headers = request("GET", base_url, headers=tracker_headers(tracker))
    assert_logged(status, final_url, body, _headers)
    return {"ok": True, "status": "authenticated_or_public", "statusCode": status, "finalUrlHost": urllib.parse.urlparse(final_url).netloc}


def parse_size(value: str | None, *, allow_plain_bytes: bool = True) -> int | None:
    if not value:
        return None
    text = value.replace(",", "").strip()
    if allow_plain_bytes and text.isdigit():
        return int(text)
    match = re.search(r"([\d.]+)\s*([kmgt]i?b|pib|pb|[kmgt])\b", text, flags=re.I)
    if not match:
        return None
    number = float(match.group(1))
    unit = match.group(2).lower().rstrip("b")
    powers = {"": 0, "k": 1, "ki": 1, "m": 2, "mi": 2, "g": 3, "gi": 3, "t": 4, "ti": 4, "p": 5, "pi": 5}
    return int(number * (1024 ** powers.get(unit, 0)))


def format_bytes(value: Any) -> str | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    units = ("B", "KB", "MB", "GB", "TB", "PB")
    unit = units[0]
    for unit in units:
        if abs(number) < 1024 or unit == units[-1]:
            break
        number /= 1024
    return f"{number:.2f} {unit}" if unit != "B" else f"{int(number)} B"


def stats_display(stats: dict[str, Any]) -> dict[str, Any]:
    return {
        "uploaded": format_bytes(stats.get("uploadedBytes")),
        "downloaded": format_bytes(stats.get("downloadedBytes")),
        "ratio": stats.get("ratio"),
        "bonus": stats.get("bonus"),
        "seeding": stats.get("seeding"),
    }


def parse_torznab_xml(data: bytes, tracker_id: str) -> list[dict[str, Any]]:
    import xml.etree.ElementTree as ET

    root = ET.fromstring(data)
    ns_torznab = "{http://torznab.com/schemas/2015/feed}"
    results: list[dict[str, Any]] = []
    for index, item in enumerate(root.findall(".//item"), start=1):
        attrs: dict[str, str] = {}
        for attr in item.findall(f"{ns_torznab}attr"):
            name = attr.attrib.get("name")
            value = attr.attrib.get("value")
            if name and value:
                attrs[name] = value
        title = item.findtext("title") or attrs.get("title") or "Untitled"
        link = item.findtext("link") or item.findtext("guid") or ""
        size = item.findtext("size") or attrs.get("size")
        results.append({
            "resultId": f"{tracker_id}:{index}",
            "trackerId": tracker_id,
            "title": normalize_space(title),
            "sizeBytes": parse_size(size),
            "seeders": to_int(attrs.get("seeders")),
            "leechers": to_int(attrs.get("peers")),
            "publishTime": item.findtext("pubDate"),
            "downloadRef": opaque_ref(link),
        })
    return results


def to_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def opaque_ref(value: str) -> str | None:
    import hashlib

    if not value:
        return None
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return f"opaque:{digest[:32]}"


def search_torznab(tracker: dict[str, Any], keyword: str, limit: int) -> list[dict[str, Any]]:
    import xml.etree.ElementTree as ET
    import urllib.parse

    base_url = tracker.get("baseUrl")
    if not base_url:
        raise RuntimeErrorJson("validation_failed", "baseUrl is required for Torznab/Prowlarr/Jackett search.")
    secret_refs = tracker.get("secretRefs") if isinstance(tracker.get("secretRefs"), dict) else {}
    api_key_ref = secret_refs.get("apiKey") or secret_refs.get("apiToken") or tracker.get("apiKeyRef")
    api_key = resolve_ref(api_key_ref, "Torznab API key")
    params = {"t": "search", "q": keyword, "apikey": api_key}
    url = base_url + ("&" if "?" in base_url else "?") + urllib.parse.urlencode(params)
    status, _final_url, body, _headers = request("GET", url, timeout=int(tracker.get("_searchTimeout") or DEFAULT_TIMEOUT))
    if status in {401, 403}:
        raise RuntimeErrorJson("auth_required", "Torznab endpoint rejected the API key.", statusCode=status)
    if status >= 400:
        raise RuntimeErrorJson("endpoint_mismatch", "Torznab endpoint returned an error.", statusCode=status)
    try:
        return parse_torznab_xml(body, tracker["id"])[:limit]
    except ET.ParseError as exc:
        raise RuntimeErrorJson("parse_failed", f"Torznab XML could not be parsed: {exc}") from exc


def search_rss(tracker: dict[str, Any], keyword: str, limit: int) -> list[dict[str, Any]]:
    import xml.etree.ElementTree as ET

    feed_url = tracker.get("feedUrl")
    if tracker.get("feedUrlRef"):
        feed_url = resolve_ref(tracker.get("feedUrlRef"), "RSS feed URL")
    if not feed_url:
        raise RuntimeErrorJson("validation_failed", "feedUrl or feedUrlRef is required for RSS search.")
    status, _final_url, body, _headers = request(
        "GET", feed_url, headers=tracker_headers(tracker), timeout=int(tracker.get("_searchTimeout") or DEFAULT_TIMEOUT)
    )
    if status >= 400:
        raise RuntimeErrorJson("endpoint_mismatch", "RSS endpoint returned an error.", statusCode=status)
    root = ET.fromstring(body)
    results: list[dict[str, Any]] = []
    q = keyword.lower()
    for index, item in enumerate(root.findall(".//item"), start=1):
        title = normalize_space(item.findtext("title") or "Untitled")
        if q and q not in title.lower():
            continue
        link = item.findtext("link") or item.findtext("enclosure") or ""
        results.append({
            "resultId": f"{tracker['id']}:{index}",
            "trackerId": tracker["id"],
            "title": title,
            "publishTime": item.findtext("pubDate"),
            "downloadRef": opaque_ref(link),
        })
        if len(results) >= limit:
            break
    return results


def html_attr(tag: str, attr: str) -> str | None:
    match = re.search(rf"""{attr}\s*=\s*["']([^"']+)["']""", tag, flags=re.I)
    return unescape(match.group(1)) if match else None


def strip_tags(html: str) -> str:
    return normalize_space(re.sub(r"<[^>]+>", " ", html))


def split_cells(row_html: str) -> list[str]:
    return re.findall(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", row_html, flags=re.I | re.S)


def extract_links(row_html: str) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    pattern = re.compile(r"(<a\b[^>]*href\s*=\s*['\"]([^'\"]+)['\"][^>]*>)(.*?)</a>", re.I | re.S)
    for match in pattern.finditer(row_html):
        tag, href, inner = match.groups()
        links.append({
            "tag": tag,
            "href": unescape(href),
            "title": html_attr(tag, "title") or "",
            "class": html_attr(tag, "class") or "",
            "text": strip_tags(inner),
        })
    return links


def extract_first_class_text(html: str, class_fragment: str) -> str | None:
    pattern = re.compile(
        rf"<(?P<tag>[a-z0-9]+)\b[^>]*class\s*=\s*['\"][^'\"]*{re.escape(class_fragment)}[^'\"]*['\"][^>]*>(?P<body>.*?)</(?P=tag)>",
        re.I | re.S,
    )
    match = pattern.search(html)
    if not match:
        return None
    return strip_tags(match.group("body"))


def extract_time_text(html: str) -> str | None:
    match = re.search(r"<(?:span|time)\b[^>]*title\s*=\s*['\"]([^'\"]+)['\"][^>]*>", html, flags=re.I)
    if match:
        return normalize_space(match.group(1))
    return strip_tags(html) or None


def marker_for_header_cell(cell_html: str) -> str | None:
    text = strip_tags(cell_html).lower()
    raw = cell_html.lower()
    def has_class_token(token: str) -> bool:
        return re.search(rf"class\s*=\s*['\"][^'\"]*\b{re.escape(token)}\b", raw) is not None

    if "comments" in raw:
        return "comments"
    if has_class_token("time") or has_class_token("date") or any(token in raw for token in ("icons time", "icons.time", "alt=\"time", "alt='time")) or any(
        token in text for token in ("time", "date", "added", "\u65f6\u95f4", "\u53d1\u5e03")
    ):
        return "time"
    if has_class_token("size") or any(token in raw for token in ("icons size", "icons.size", "alt=\"size", "alt='size")) or any(
        token in text for token in ("size", "\u5927\u5c0f")
    ):
        return "size"
    if has_class_token("seeders") or any(token in raw for token in ("icons seeders", "icons.seeders", "alt=\"seeders", "alt='seeders")) or any(
        token in text for token in ("seeders", "\u505a\u79cd", "\u7a2e\u5b50")
    ):
        return "seeders"
    if has_class_token("leechers") or any(token in raw for token in ("icons leechers", "icons.leechers", "alt=\"leechers", "alt='leechers")) or any(
        token in text for token in ("leechers", "\u4e0b\u8f7d\u6570")
    ):
        return "leechers"
    if any(has_class_token(token) for token in ("snatched", "finished", "completed")) or any(token in raw for token in ("snatched", "finished", "completed")) or any(
        token in text for token in ("completed", "snatched", "\u5b8c\u6210")
    ):
        return "completed"
    if re.search(r"(cat|\u7c7b\u578b|\u5206\u7c7b|\u5206\u985e)", text, flags=re.I):
        return "category"
    return None


def infer_table_fields(rows: list[str]) -> tuple[dict[str, int], int]:
    if not rows:
        return {}, 0
    first_cells = split_cells(rows[0])
    if not first_cells:
        return {}, 0
    markers = [marker_for_header_cell(cell) for cell in first_cells]
    is_header = "<th" in rows[0].lower() or not extract_links(rows[0]) or len([x for x in markers if x]) >= 2
    field_index: dict[str, int] = {}
    if is_header:
        for index, field in enumerate(markers):
            if field and field not in field_index:
                field_index[field] = index
        return field_index, 1
    return field_index, 0


def cell_value(cells: list[str], field_index: dict[str, int], field: str) -> str | None:
    index = field_index.get(field)
    if index is None or index >= len(cells):
        return None
    return strip_tags(cells[index])


def cell_html(cells: list[str], field_index: dict[str, int], field: str) -> str | None:
    index = field_index.get(field)
    if index is None or index >= len(cells):
        return None
    return cells[index]


def first_img_title(html: str | None) -> str | None:
    if not html:
        return None
    match = re.search(r"<img\b[^>]*>", html, flags=re.I)
    if not match:
        return None
    tag = match.group(0)
    return html_attr(tag, "title") or html_attr(tag, "alt")


def first_int_text(value: str | None) -> int | None:
    if not value:
        return None
    match = re.search(r"\d+", value.replace(",", ""))
    return to_int(match.group(0)) if match else None



def strip_style_and_script(html: str) -> str:
    cleaned = re.sub(r"<style\b[^>]*>.*?</style>", " ", html, flags=re.I | re.S)
    cleaned = re.sub(r"<script\b[^>]*>.*?</script>", " ", cleaned, flags=re.I | re.S)
    return cleaned


def parse_promotion_state(row_html: str, row_text: str | None = None) -> dict[str, Any]:
    """Extract freeleech/discount tags without matching CSS class definitions.

    HHClub embeds CSS such as `.promotion-tag-free { ... }` inside result cards.
    Matching the bare word `free` on raw HTML therefore marks every torrent free.
    Only inspect content markup, class attributes, and explicit badge text.
    """
    content_html = strip_style_and_script(row_html)
    content_text = row_text if row_text is not None else strip_tags(content_html)
    lower_html = content_html.lower()
    lower_text = content_text.lower()
    tags: list[str] = []
    discount = "unknown"

    class_tokens: list[str] = []
    for raw in re.findall(r"""class\s*=\s*['"]([^'"]+)['"]""", content_html, flags=re.I):
        class_tokens.extend(token for token in re.split(r"\s+", raw.strip().lower()) if token)
    class_set = set(class_tokens)

    badge_texts = [
        strip_tags(match).lower()
        for match in re.findall(
            r"""<(?:span|font|b|strong|em|i|label)\b[^>]*>(.*?)</(?:span|font|b|strong|em|i|label)>""",
            content_html,
            flags=re.I | re.S,
        )
    ]
    badge_texts = [text for text in badge_texts if text]
    title_alts = [
        value.lower()
        for value in re.findall(r"""(?:title|alt)\s*=\s*['"]([^'"]+)['"]""", content_html, flags=re.I)
    ]

    def has_class(*tokens: str) -> bool:
        for token in tokens:
            token = token.lower()
            if token in class_set:
                return True
            # Allow known promotion class fragments inside compound class names.
            for item in class_set:
                if item == token or item.startswith(f"{token}-") or item.endswith(f"-{token}") or f"-{token}-" in item:
                    return True
                if token.startswith("pro_") and token in item:
                    return True
                if token.startswith("promotion-tag-") and token in item:
                    return True
        return False

    def has_badge(*tokens: str) -> bool:
        for token in tokens:
            token_l = token.lower()
            for source in (*badge_texts, *title_alts):
                if source == token_l or token_l in source:
                    return True
        return False

    free = (
        has_class(
            "pro_free",
            "pro_free2up",
            "promotion-tag-free",
            "promotion-tag-2xfree",
            "freeleech",
            "free_bg",
        )
        or has_badge("2x免费", "2x free", "freeleech", "免费")
        or bool(re.search(r"\b(pro_free2up|pro_free|freeleech)\b", lower_html))
        or bool(re.search(r"(2x\s*免费|免费种|限时免费)", content_text))
        or any(re.fullmatch(r"free", text) for text in badge_texts)
    )
    half = (
        has_class("pro_50", "pro_50pctdown", "promotion-tag-50", "halfdown", "percent_50")
        or has_badge("50%", "半价", "50pct")
        or bool(re.search(r"\b(pro_50|halfdown)\b", lower_html))
    )
    thirty = has_class("pro_30", "promotion-tag-30", "percent_30") or has_badge("30%")
    two_x = (
        has_class("pro_2up", "pro_free2up", "promotion-tag-2x", "promotion-tag-2xfree", "twoup")
        or has_badge("2x", "2x免费", "2x free", "双倍", "2x 50%")
        or bool(re.search(r"\b(pro_2up|pro_free2up|twoup)\b", lower_html))
    )

    if free and two_x:
        discount = "2xfree"
        tags.extend(["2xFree", "Free"])
    elif free:
        discount = "free"
        tags.append("Free")
    elif two_x and half:
        discount = "2x50%"
        tags.append("2x50%")
    elif half:
        discount = "50%"
        tags.append("50%")
    elif thirty:
        discount = "30%"
        tags.append("30%")
    elif two_x:
        discount = "2x"
        tags.append("2x")

    if (
        "hitandrun" in lower_html
        or "h&r" in lower_text
        or "hit and run" in lower_text
        or any("h&r" in text or "hitandrun" in text for text in badge_texts)
    ):
        tags.append("H&R")

    deduped: list[str] = []
    for tag in tags:
        if tag not in deduped:
            deduped.append(tag)
    return {"discount": discount, "tags": deduped}


def parse_html_row(row_html: str, tracker: dict[str, Any], index: int, field_index: dict[str, int] | None = None) -> dict[str, Any] | None:
    schema = schema_default(tracker.get("adapterId"))
    links = extract_links(row_html)
    detail_href = ""
    download_href = ""
    title = ""
    for link in links:
        href = link["href"]
        title_attr = link.get("title") or ""
        text = link.get("text") or ""
        if schema.get("downloadPattern") and schema["downloadPattern"] in href:
            download_href = download_href or href
        if schema.get("detailPattern") and schema["detailPattern"] in href:
            detail_href = detail_href or href
            if title_attr or text:
                title = title or title_attr or text
        elif re.search(r"(details|torrent|view)", href, re.I):
            detail_href = detail_href or href
            title = title or title_attr or text
    if not title or not (detail_href or download_href):
        return None
    id_match = re.search(r"[?&]id=(\d+)", detail_href or download_href)
    if not download_href and id_match and schema.get("downloadTemplate"):
        download_href = str(schema["downloadTemplate"]).format(id=id_match.group(1))
    row_text = strip_tags(row_html)
    raw_cells = split_cells(row_html)
    cells = [strip_tags(cell) for cell in raw_cells]
    field_index = field_index or {}
    subtitle = extract_first_class_text(row_html, "torrent-info-text-small_name")
    size = parse_size(extract_first_class_text(row_html, "torrent-info-text-size") or cell_value(cells, field_index, "size"))
    if size is None:
        for cell in cells:
            size = parse_size(cell, allow_plain_bytes=False)
            if size:
                break
    seeders = first_int_text(extract_first_class_text(row_html, "torrent-info-text-seeders") or cell_value(cells, field_index, "seeders"))
    leechers = first_int_text(extract_first_class_text(row_html, "torrent-info-text-leechers") or cell_value(cells, field_index, "leechers"))
    completed = first_int_text(extract_first_class_text(row_html, "torrent-info-text-finished") or cell_value(cells, field_index, "completed"))
    time_source = extract_first_class_text(row_html, "torrent-info-text-added") or cell_html(raw_cells, field_index, "time") or ""
    publish_time = extract_time_text(time_source)
    category_html = cell_html(raw_cells, field_index, "category")
    category = first_img_title(category_html) or cell_value(cells, field_index, "category")
    promotion = parse_promotion_state(row_html, row_text)
    tags = list(promotion["tags"])
    return {
        "resultId": f"{tracker['id']}:{id_match.group(1) if id_match else index}",
        "trackerId": tracker["id"],
        "sitePresetId": tracker.get("sitePresetId"),
        "adapterId": tracker.get("adapterId"),
        "title": normalize_space(title),
        "subtitle": subtitle,
        "category": category,
        "sizeBytes": size,
        "seeders": seeders,
        "leechers": leechers,
        "completed": completed,
        "publishTime": publish_time,
        "tags": tags,
        "discount": promotion["discount"],
        "detailRef": opaque_ref(base_url_join(tracker.get("baseUrl", ""), detail_href)) if detail_href else None,
        "downloadRef": opaque_ref(base_url_join(tracker.get("baseUrl", ""), download_href)) if download_href else None,
    }


def search_html(tracker: dict[str, Any], keyword: str, limit: int) -> list[dict[str, Any]]:
    import urllib.parse

    schema = schema_default(tracker.get("adapterId"))
    path, param = schema["searchPath"], schema["keywordParam"]
    search_cfg = tracker.get("search") if isinstance(tracker.get("search"), dict) else {}
    path = search_cfg.get("path") or path
    param = search_cfg.get("keywordParam") or param
    url = base_url_join(tracker.get("baseUrl", ""), path)
    params = {**schema.get("extraParams", {}), param: keyword}
    # NexusPHP freeleech filter. Keep local filtering as a safety net.
    if tracker.get("_freeOnly") and tracker.get("adapterId") == "nexusphp" and "spstate" not in params:
        params["spstate"] = "2"
    url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    status, final_url, body, _headers = request(
        "GET", url, headers=tracker_headers(tracker), timeout=int(tracker.get("_searchTimeout") or DEFAULT_TIMEOUT)
    )
    text = body.decode("utf-8", errors="ignore")
    assert_logged(status, final_url, body, _headers)
    if status >= 400:
        raise RuntimeErrorJson("endpoint_mismatch", "HTML search returned an error.", statusCode=status)
    row_parser = SearchRowParser()
    row_parser.feed(text)
    field_index, start_index = infer_table_fields(row_parser.rows)
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in row_parser.rows[start_index:]:
        parsed = parse_html_row(row, tracker, len(results) + 1, field_index)
        if not parsed:
            continue
        title = parsed.get("title") or ""
        if keyword and keyword.lower() not in title.lower() and keyword.lower() not in strip_tags(row).lower():
            continue
        key = str(parsed.get("detailRef") or parsed.get("downloadRef") or title)
        if key in seen:
            continue
        seen.add(key)
        results.append(parsed)
        if len(results) >= limit:
            break
    if not results and row_parser.rows and not NO_RESULTS_TEXT_RE.search(text):
        raise RuntimeErrorJson(
            "selector_drift",
            "Authenticated HTML loaded, but the search result rows could not be normalized.",
            rowCount=len(row_parser.rows),
        )
    return results


def search_tracker(tracker: dict[str, Any], keyword: str, limit: int) -> dict[str, Any]:
    validate_tracker(tracker)
    adapter_id = tracker.get("adapterId")
    if adapter_id in {"torznab", "prowlarr", "jackett"}:
        results = search_torznab(tracker, keyword, limit)
    elif adapter_id == "rss":
        results = search_rss(tracker, keyword, limit)
    elif adapter_id in {"nexusphp", "unit3d", "gazelle", "selector"}:
        results = search_html(tracker, keyword, limit)
    else:
        raise RuntimeErrorJson("capability_unavailable", "Direct search is unavailable for this adapter in the current environment.", adapterId=adapter_id)
    return {"ok": True, "trackerId": tracker["id"], "results": results, "total": len(results)}


MEDIA_SUFFIXES = (
    "的电影资源",
    "的电视剧资源",
    "电影资源",
    "电视剧资源",
    "的电影",
    "的电视剧",
    "电影",
    "电视剧",
    "剧集",
    "资源",
)


def normalize_media_query(query: str) -> str:
    normalized = normalize_space(query)
    for suffix in MEDIA_SUFFIXES:
        if normalized.endswith(suffix) and len(normalized) > len(suffix):
            normalized = normalized[: -len(suffix)].strip()
            break
    normalized = re.sub(r"^(?:搜一下|搜索一下|搜|搜索|找一下|找)\s*", "", normalized).strip()
    return normalized or normalize_space(query)


def strip_tracker_phrase(query: str, aliases: list[str]) -> str:
    normalized = normalize_space(query)
    verbs = r"(?:搜一下|搜索一下|搜|搜索|找一下|找)"
    for alias in aliases:
        if not alias:
            continue
        pattern = rf"^(?:用\s*)?{re.escape(alias)}\s*{verbs}?\s*"
        stripped = re.sub(pattern, "", normalized, count=1, flags=re.I)
        if stripped != normalized:
            return stripped
    return normalized


def media_kind_matches(result: dict[str, Any], kind: str) -> bool:
    if kind == "any":
        return True
    category = str(result.get("category") or "").lower()
    title = str(result.get("title") or "").lower()
    subtitle = str(result.get("subtitle") or "").lower()
    combined = f"{category} {title} {subtitle}"
    movie_markers = ("movie", "电影", "movies")
    tv_markers = ("tv", "电视剧", "剧集", "series", "episode", "season", "真人秀", "综艺")
    episodic = any(marker in combined for marker in tv_markers) or bool(
        re.search(r"\bs\d{1,2}\b|第\s*\d+\s*[集期]|全\s*\d+\s*[集期]", combined, flags=re.I)
    )
    if kind == "movie":
        return any(marker in category for marker in movie_markers) or not episodic
    if kind == "tv":
        return episodic
    return True


def media_result_score(result: dict[str, Any], query: str, kind: str) -> tuple[int, int, int]:
    haystack = f"{result.get('title') or ''} {result.get('subtitle') or ''}".lower()
    relevance = 100 if query.lower() in haystack else 0
    kind_score = 20 if media_kind_matches(result, kind) else 0
    free_score = 10 if str(result.get("discount") or "").lower() in {"free", "2xfree"} else 0
    return relevance + kind_score + free_score, int(result.get("seeders") or 0), int(result.get("completed") or 0)


def media_search_display_text(
    results: list[dict[str, Any]],
    total: int,
    trackers: list[dict[str, Any]],
    *,
    free_only: bool,
    resolution: str | None,
    sort: str,
) -> str:
    active_filters = []
    if free_only:
        active_filters.append("免费筛选")
    if resolution:
        active_filters.append(resolution)
    if total == 0:
        if active_filters:
            return f"没有找到符合筛选条件的结果。\n可以继续：取消{'、'.join(active_filters)}、换关键词、换站点搜索。"
        return "没有找到匹配结果。\n可以继续：换关键词、换站点搜索。"

    tracker_names = {
        str(tracker.get("id")): str(tracker.get("displayName") or tracker.get("name") or tracker.get("id"))
        for tracker in trackers
    }
    ordering = {"seeders": "做种人数", "size": "大小", "relevance": "相关性"}.get(sort, "相关性")
    visible = results[:5]
    lines = [f"找到 {total} 个结果，按{ordering}展示前 {len(visible)} 个："]
    for index, item in enumerate(visible, start=1):
        fields = [tracker_names.get(str(item.get("trackerId")), str(item.get("trackerId") or ""))]
        if item.get("size"):
            fields.append(str(item["size"]))
        seeders = item.get("seeders")
        leechers = item.get("leechers")
        if seeders is not None or leechers is not None:
            fields.append(f"{seeders or 0}/{leechers or 0}")
        discount = str(item.get("discount") or "").lower()
        if discount and discount != "unknown":
            fields.append(str(item.get("discount")))
        if item.get("publishTime"):
            fields.append(str(item["publishTime"]))
        lines.extend(["", f"{index}. {item.get('title') or '未命名资源'}", f"   {' · '.join(field for field in fields if field)}"])
    lines.extend(["", "回复：下载第 1 个、只看免费、按做种排序。"])
    return "\n".join(lines)


def media_search(
    store: dict[str, Any],
    query: str,
    tracker_aliases: list[str],
    kind: str,
    limit: int,
    timeout: int,
    free_only: bool = False,
    resolution: str | None = None,
    sort: str = "relevance",
) -> dict[str, Any]:
    started = time.monotonic()
    if resolution == "4k":
        resolution = "2160p"
    aliases = [alias for alias in tracker_aliases if alias]
    keyword = normalize_media_query(strip_tracker_phrase(query, aliases))
    if not aliases:
        default_id = store.get("defaultSearchSolutionId")
        if default_id:
            aliases = [str(default_id)]
        else:
            aliases = [
                str(record.get("id"))
                for record in store.get("trackers", {}).values()
                if isinstance(record, dict) and tracker_is_enabled_config(record)
            ]
    if not aliases:
        raise RuntimeErrorJson("configuration_required", "No enabled tracker is available for search.")

    trackers: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for alias in aliases:
        tracker = find_tracker_record(store, alias)
        tracker_id = str(tracker.get("id"))
        if tracker_id not in seen_ids:
            tracker["_searchTimeout"] = max(1, min(timeout, 10))
            tracker["_freeOnly"] = bool(free_only)
            trackers.append(tracker)
            seen_ids.add(tracker_id)

    def run(tracker: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        tracker_id = str(tracker.get("id"))
        try:
            return tracker_id, search_tracker(tracker, keyword, min(max(limit * 3, 20), 50))
        except RuntimeErrorJson as exc:
            return tracker_id, {"ok": False, "error": exc.payload}

    reports: dict[str, dict[str, Any]] = {}
    if len(trackers) == 1:
        tracker_id, report = run(trackers[0])
        reports[tracker_id] = report
    else:
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=min(4, len(trackers))) as executor:
            for tracker_id, report in executor.map(run, trackers):
                reports[tracker_id] = report

    results = [
        result
        for report in reports.values()
        if report.get("ok")
        for result in report.get("results", [])
        if media_kind_matches(result, kind)
    ]
    if free_only:
        free_discounts = {"free", "2xfree"}
        results = [
            result
            for result in results
            if str(result.get("discount") or "").lower() in free_discounts
            or any(tag in (result.get("tags") or []) for tag in ("Free", "2xFree"))
        ]
    if resolution:
        markers = {"2160p": ("2160p", "4k"), "1080p": ("1080p",), "720p": ("720p",)}[resolution]
        results = [
            result
            for result in results
            if any(marker in f"{result.get('title') or ''} {result.get('subtitle') or ''}".lower() for marker in markers)
        ]
    if sort == "seeders":
        results.sort(key=lambda item: int(item.get("seeders") or 0), reverse=True)
    elif sort == "size":
        results.sort(key=lambda item: int(item.get("sizeBytes") or 0), reverse=True)
    else:
        results.sort(key=lambda item: media_result_score(item, keyword, kind), reverse=True)
    failures = [
        {"trackerId": tracker_id, "error": report.get("error")}
        for tracker_id, report in reports.items()
        if not report.get("ok")
    ]
    elapsed_ms = round((time.monotonic() - started) * 1000)
    visible_results = [{**result, "size": format_bytes(result.get("sizeBytes"))} for result in results[:limit]]
    return {
        "ok": bool(results) or not failures,
        "query": query,
        "normalizedQuery": keyword,
        "kind": kind,
        "filters": {"freeOnly": free_only, "resolution": resolution, "sort": sort},
        "trackerIds": [str(tracker.get("id")) for tracker in trackers],
        "results": visible_results,
        "total": len(results),
        "failures": failures,
        "elapsedMs": elapsed_ms,
        "display": {
            "text": media_search_display_text(
                visible_results,
                len(results),
                trackers,
                free_only=free_only,
                resolution=resolution,
                sort=sort,
            )
        },
    }


def parse_stats_text(text: str) -> dict[str, Any]:
    plain = normalize_space(re.sub(r"<[^>]+>", " ", text))
    stats: dict[str, Any] = {"status": "ok"}
    invite_badge = re.search(r"\[\s*\u9080\u8bf7\s*\]\s*:\s*\d+\s+([\d,]+(?:\.\d+)?)\s*\[\s*\u52cb\u7ae0\s*\]", plain)
    if invite_badge:
        stats["bonus"] = float(invite_badge.group(1).replace(",", ""))
    badge_transfer = re.search(
        r"\[\s*\u52cb\u7ae0\s*\]\s*([\d.]+\s*[KMGTPE]?i?B)\s+\d+\s+([\d.]+\s*[KMGTPE]?i?B)",
        plain,
        flags=re.I,
    )
    if badge_transfer:
        stats["uploadedBytes"] = parse_size(badge_transfer.group(1))
        stats["downloadedBytes"] = parse_size(badge_transfer.group(2))
    label_patterns = {
        "uploadedBytes": [r"(?:uploaded|upload|\u4e0a\u4f20\u91cf?)[^\d]{0,20}([\d.,]+\s*[KMGTPE]?i?B?)"],
        "downloadedBytes": [r"(?:downloaded|download|\u4e0b\u8f7d\u91cf?)[^\d]{0,20}([\d.,]+\s*[KMGTPE]?i?B?)"],
        "ratio": [r"(?:ratio|\u5206\u4eab\u7387)[^\d]{0,20}([\d.]+)"],
        "bonus": [
            r"(?:bonus\s*(?:points?)?|\u9b54\u529b\u503c|\u79ef\u5206)\s*(?:\[[^\]]*\]\s*)?[:\uff1a]\s*([\d.,]+)",
            r"(?:bonus\s*(?:points?)?|\u79ef\u5206)[^\d]{0,12}([\d.,]+)",
        ],
    }
    for key, patterns in label_patterns.items():
        if key in stats:
            continue
        for pattern in patterns:
            match = re.search(pattern, plain, flags=re.I)
            if not match:
                continue
            value = match.group(1)
            if key.endswith("Bytes"):
                stats[key] = parse_size(value)
            elif key == "ratio":
                try:
                    stats[key] = float(value.replace(",", ""))
                except ValueError:
                    continue
            else:
                try:
                    stats[key] = float(value.replace(",", ""))
                except ValueError:
                    continue
            break
    if len(stats) == 1:
        raise RuntimeErrorJson("parse_failed", "Authenticated page loaded, but account stats could not be normalized.")
    return stats


def user_stats(tracker: dict[str, Any]) -> dict[str, Any]:
    validate_tracker(tracker)
    if tracker.get("authMode") == "browser_profile":
        raise RuntimeErrorJson("provider_unavailable", "Current environment cannot read browser profile account stats directly.")
    candidates: list[str] = []
    if tracker.get("statsPath"):
        candidates.append(tracker["statsPath"])
    candidates.extend(["/index.php", "/usercp.php", "/my.php"])
    candidates = list(dict.fromkeys(candidates))
    last_error: RuntimeErrorJson | None = None
    for path in candidates:
        try:
            status, final_url, body, _headers = request("GET", base_url_join(tracker.get("baseUrl", ""), path), headers=tracker_headers(tracker))
            text = body.decode("utf-8", errors="ignore")
            if status in {401, 403} or "login" in final_url.lower():
                raise RuntimeErrorJson("auth_required", "Tracker did not return an authenticated stats page.")
            stats = parse_stats_text(text)
            stats["trackerId"] = tracker["id"]
            return {"ok": True, "stats": stats, "display": stats_display(stats)}
        except RuntimeErrorJson as exc:
            last_error = exc
            if exc.payload["code"] == "auth_required":
                raise
    raise last_error or RuntimeErrorJson("parse_failed", "Account stats could not be read.")


def qb_headers(downloader: dict[str, Any]) -> dict[str, str]:
    credential = resolve_ref(downloader.get("credentialRef"), "downloader credential") if downloader.get("credentialRef") else None
    if credential and credential.startswith("qbt_"):
        return {"Authorization": f"Bearer {credential}"}
    return {}


def parse_qb_credential(downloader: dict[str, Any]) -> tuple[str | None, str | None, str | None]:
    credential = resolve_ref(downloader.get("credentialRef"), "downloader credential") if downloader.get("credentialRef") else None
    if not credential:
        return None, None, None
    if credential.startswith("qbt_"):
        return None, None, credential
    try:
        data = json.loads(credential)
        if isinstance(data, dict):
            return str(data.get("username") or ""), str(data.get("password") or ""), None
    except json.JSONDecodeError:
        pass
    if ":" in credential:
        username, password = credential.split(":", 1)
        return username, password, None
    raise RuntimeErrorJson("credential_validation_failed", "qBittorrent credential env must be API key, user:pass, or JSON with username/password.")


def qb_session_headers(downloader: dict[str, Any]) -> dict[str, str]:
    import urllib.parse

    username, password, api_key = parse_qb_credential(downloader)
    if api_key:
        return {"Authorization": f"Bearer {api_key}"}
    if username is None and password is None:
        return {}
    data = urllib.parse.urlencode({"username": username or "", "password": password or ""}).encode("utf-8")
    status, _final_url, body, headers = request(
        "POST",
        base_url_join(downloader["baseUrl"], "/api/v2/auth/login"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=data,
    )
    body_text = body.decode("utf-8", errors="ignore")
    if status not in {200, 204} or (body_text and body_text not in {"Ok.", ""}):
        raise RuntimeErrorJson("downloader_auth_failed", "qBittorrent login failed.", statusCode=status)
    cookie = headers.get("Set-Cookie") or headers.get("set-cookie") or ""
    sid_match = re.search(r"(SID=[^;]+)", cookie)
    if not sid_match:
        raise RuntimeErrorJson("downloader_auth_failed", "qBittorrent login did not return SID cookie.")
    return {"Cookie": sid_match.group(1)}


def normalize_qb_counts(torrents: dict[str, Any]) -> dict[str, int]:
    counts = {"active": 0, "downloading": 0, "uploading": 0, "paused": 0, "checking": 0, "errored": 0, "completed": 0}
    for torrent in torrents.values():
        state = str(torrent.get("state") or "")
        progress = float(torrent.get("progress") or 0)
        if progress >= 1:
            counts["completed"] += 1
        if "error" in state or "missing" in state:
            counts["errored"] += 1
        elif "pause" in state:
            counts["paused"] += 1
        elif "check" in state:
            counts["checking"] += 1
        elif "up" in state or state in {"uploading", "stalledUP", "forcedUP"}:
            counts["uploading"] += 1
        elif "dl" in state.lower() or state in {"downloading", "metaDL", "forcedDL"}:
            counts["downloading"] += 1
        if int(torrent.get("dlspeed") or 0) > 0 or int(torrent.get("upspeed") or 0) > 0:
            counts["active"] += 1
    return counts


def downloader_status(downloader: dict[str, Any]) -> dict[str, Any]:
    dtype = downloader.get("type")
    if dtype != "qbittorrent":
        raise RuntimeErrorJson("capability_unavailable", "Downloader status is available only for qBittorrent in the current environment.", downloaderType=dtype)
    base = downloader.get("baseUrl")
    if not base:
        raise RuntimeErrorJson("validation_failed", "Downloader baseUrl is required.")
    headers = qb_session_headers(downloader)
    status, _final_url, body, _headers = request("GET", base_url_join(base, "/api/v2/app/version"), headers=headers)
    if status in {401, 403}:
        raise RuntimeErrorJson("downloader_auth_failed", "qBittorrent rejected credentials.", statusCode=status)
    if status >= 400:
        raise RuntimeErrorJson("downloader_unreachable", "qBittorrent status endpoint returned an error.", statusCode=status)
    version = body.decode("utf-8", errors="ignore").strip()
    sync_status, _sync_url, sync_body, _sync_headers = request(
        "GET",
        base_url_join(base, "/api/v2/sync/maindata?rid=0"),
        headers=headers,
    )
    if sync_status >= 400:
        return {
            "ok": True,
            "downloaderId": downloader["id"],
            "healthy": True,
            "type": dtype,
            "version": version,
            "display": {"version": version},
        }
    sync_data = json.loads(sync_body.decode("utf-8", errors="ignore") or "{}")
    server_state = sync_data.get("server_state") or {}
    torrents = sync_data.get("torrents") or {}
    result = {
        "ok": True,
        "downloaderId": downloader["id"],
        "healthy": True,
        "type": dtype,
        "version": version,
        "freeSpaceBytes": server_state.get("free_space_on_disk"),
        "downloadRateBytesPerSec": server_state.get("dl_info_speed"),
        "uploadRateBytesPerSec": server_state.get("up_info_speed"),
        "counts": normalize_qb_counts(torrents),
    }
    download_rate = format_bytes(result.get("downloadRateBytesPerSec"))
    upload_rate = format_bytes(result.get("uploadRateBytesPerSec"))
    result["display"] = {
        "version": version,
        "freeSpace": format_bytes(result.get("freeSpaceBytes")),
        "downloadRate": f"{download_rate}/s" if download_rate else None,
        "uploadRate": f"{upload_rate}/s" if upload_rate else None,
        "counts": result["counts"],
    }
    return result




def torrent_info_hash(torrent_data: bytes) -> str | None:
    """Return lowercase SHA1 infohash for a .torrent payload without third-party deps."""
    import hashlib

    marker = b"4:info"
    start = torrent_data.find(marker)
    if start < 0:
        return None
    index = start + len(marker)

    def parse_value(data: bytes, i: int) -> tuple[object, int]:
        if i >= len(data):
            raise ValueError("truncated bencode")
        ch = data[i:i+1]
        if ch == b"i":
            end = data.find(b"e", i)
            if end < 0:
                raise ValueError("bad int")
            return int(data[i+1:end] or b"0"), end + 1
        if ch == b"l":
            i += 1
            items = []
            while data[i:i+1] != b"e":
                item, i = parse_value(data, i)
                items.append(item)
            return items, i + 1
        if ch == b"d":
            i += 1
            mapping = {}
            while data[i:i+1] != b"e":
                key, i = parse_value(data, i)
                value, i = parse_value(data, i)
                mapping[key] = value
            return mapping, i + 1
        if ch.isdigit():
            colon = data.find(b":", i)
            if colon < 0:
                raise ValueError("bad string")
            length = int(data[i:colon])
            begin = colon + 1
            end = begin + length
            return data[begin:end], end
        raise ValueError(f"unknown bencode token {ch!r}")

    try:
        _info, end = parse_value(torrent_data, index)
    except Exception:
        return None
    return hashlib.sha1(torrent_data[index:end]).hexdigest()


def normalize_torrent_name(value: str | None) -> str:
    text = normalize_space(value or "").lower()
    text = re.sub(r"[\[\](){}_.-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def qb_find_torrent(downloader: dict[str, Any], *, info_hash: str | None = None, name_hint: str | None = None) -> dict[str, Any] | None:
    listing = qb_list_torrents(downloader, None, 200)
    torrents = listing.get("torrents") or []
    if info_hash:
        target = info_hash.lower()
        for item in torrents:
            if str(item.get("hash") or "").lower() == target:
                return item
    if name_hint:
        hint = normalize_torrent_name(name_hint)
        if hint:
            for item in torrents:
                name = normalize_torrent_name(str(item.get("name") or ""))
                if hint in name or name in hint:
                    return item
            # token overlap fallback
            hint_tokens = set(hint.split())
            best = None
            best_score = 0
            for item in torrents:
                name = normalize_torrent_name(str(item.get("name") or ""))
                tokens = set(name.split())
                score = len(hint_tokens & tokens)
                if score > best_score and score >= max(2, len(hint_tokens) // 3):
                    best = item
                    best_score = score
            if best is not None:
                return best
    return None


def summarize_torrent(item: dict[str, Any] | None) -> dict[str, Any] | None:
    if not item:
        return None
    progress = item.get("progress")
    try:
        progress_pct = round(float(progress) * 100, 1) if progress is not None else None
    except (TypeError, ValueError):
        progress_pct = None
    state = str(item.get("state") or "")
    return {
        "hash": item.get("hash"),
        "name": item.get("name"),
        "state": state,
        "progress": progress,
        "progressPercent": progress_pct,
        "sizeBytes": item.get("sizeBytes"),
        "downloadRateBytesPerSec": item.get("downloadRateBytesPerSec"),
        "uploadRateBytesPerSec": item.get("uploadRateBytesPerSec"),
        "category": item.get("category"),
        "tags": item.get("tags"),
        "display": {
            "name": item.get("name"),
            "state": state,
            "progress": f"{progress_pct}%" if progress_pct is not None else None,
            "size": format_bytes(item.get("sizeBytes")),
            "downloadRate": (
                f"{format_bytes(item.get('downloadRateBytesPerSec'))}/s"
                if item.get("downloadRateBytesPerSec") is not None
                else None
            ),
        },
    }


def qb_add_torrent_file(downloader: dict[str, Any], torrent_data: bytes, filename: str, options: dict[str, Any]) -> dict[str, Any]:
    if downloader.get("type") != "qbittorrent":
        raise RuntimeErrorJson("capability_unavailable", "Adding downloads is available only for qBittorrent in the current environment.", downloaderType=downloader.get("type"))
    info_hash = torrent_info_hash(torrent_data)
    name_hint = Path(filename).stem if filename else None
    existing = qb_find_torrent(downloader, info_hash=info_hash, name_hint=name_hint)
    if existing:
        summary = summarize_torrent(existing)
        return {
            "ok": True,
            "downloaderId": downloader["id"],
            "status": "already_present",
            "infoHash": info_hash,
            "torrent": summary,
            "display": summary.get("display") if summary else None,
        }

    headers = qb_session_headers(downloader)
    boundary = "----FormBoundary7MA4YWxkTrZu0gW"
    body_parts: list[bytes] = []
    fields = {}
    if options.get("savePath"):
        fields["savepath"] = str(options["savePath"])
    if options.get("categoryOrLabel"):
        fields["category"] = str(options["categoryOrLabel"])
    if options.get("tags"):
        fields["tags"] = ",".join(options["tags"]) if isinstance(options["tags"], list) else str(options["tags"])
    # Default to start immediately when the caller does not specify paused/start.
    paused = "true" if options.get("addPaused") else "false"
    fields["paused"] = paused
    fields["stopped"] = paused
    for key, value in fields.items():
        body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n{value}\r\n".encode())
    safe_name = filename.replace('"', "")
    body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"torrents\"; filename=\"{safe_name}\"\r\nContent-Type: application/x-bittorrent\r\n\r\n".encode())
    body_parts.append(torrent_data)
    body_parts.append(f"\r\n--{boundary}--\r\n".encode())
    body = b"".join(body_parts)
    status, _final_url, resp_body, _headers = request(
        "POST",
        base_url_join(downloader["baseUrl"], "/api/v2/torrents/add"),
        headers={**headers, "Content-Type": f"multipart/form-data; boundary={boundary}"},
        data=body,
    )
    response_text = resp_body.decode("utf-8", errors="ignore").strip()
    if status in {401, 403}:
        raise RuntimeErrorJson("downloader_auth_failed", "qBittorrent rejected credentials.", statusCode=status)

    matched = qb_find_torrent(downloader, info_hash=info_hash, name_hint=name_hint)
    if status >= 400 or response_text in {"Fails.", "Fail."}:
        if matched:
            summary = summarize_torrent(matched)
            return {
                "ok": True,
                "downloaderId": downloader["id"],
                "status": "already_present",
                "infoHash": info_hash,
                "response": response_text or None,
                "torrent": summary,
                "display": summary.get("display") if summary else None,
            }
        raise RuntimeErrorJson(
            "downloader_add_failed",
            "qBittorrent rejected the torrent file.",
            statusCode=status,
            response=response_text or None,
            infoHash=info_hash,
        )

    # Prefer matching by infohash; fall back to the newest torrent when qB needs a moment.
    if not matched and info_hash:
        for _ in range(3):
            time.sleep(0.35)
            matched = qb_find_torrent(downloader, info_hash=info_hash, name_hint=name_hint)
            if matched:
                break
    summary = summarize_torrent(matched)
    result = {
        "ok": True,
        "downloaderId": downloader["id"],
        "status": "added",
        "infoHash": info_hash,
        "response": response_text or "Ok.",
        "torrent": summary,
        "display": summary.get("display") if summary else {
            "name": filename,
            "state": "queued" if options.get("addPaused") else "downloading",
        },
    }
    return result


def download_torrent(tracker: dict[str, Any], torrent_id: str, downloader: dict[str, Any], options: dict[str, Any]) -> dict[str, Any]:
    import urllib.parse

    validate_tracker(tracker)
    base_url = tracker.get("baseUrl")
    if not base_url:
        raise RuntimeErrorJson("validation_failed", "baseUrl is required.")
    # Allow resultId form like hhanclub:18262
    if ":" in torrent_id and torrent_id.split(":", 1)[0].lower() in {
        str(tracker.get("id") or "").lower(),
        str(tracker.get("sitePresetId") or "").lower(),
        "hh",
        "hhanclub",
    }:
        torrent_id = torrent_id.split(":", 1)[1]
    schema = schema_default(tracker.get("adapterId"))
    download_path = schema.get("downloadTemplate", "/download.php?id={id}").format(id=torrent_id)
    download_url = base_url_join(base_url, download_path)
    status, final_url, body, headers = request("GET", download_url, headers=tracker_headers(tracker))
    if status in {401, 403}:
        raise RuntimeErrorJson("auth_required", "Tracker rejected the download request.", statusCode=status)
    if status >= 400:
        raise RuntimeErrorJson("download_failed", "Tracker returned an error for the download.", statusCode=status)
    content_type = headers.get("Content-Type", headers.get("content-type", ""))
    if "text/html" in content_type and len(body) < 5000:
        page = body.decode("utf-8", errors="ignore")
        if NO_LOGIN_TEXT_RE.search(page):
            raise RuntimeErrorJson("auth_required", "Tracker returned a login page instead of the torrent file.")
    if not body or not (body.startswith(b"d") or b"4:info" in body[:200]):
        # Some trackers still return HTML with a high content length.
        if b"<html" in body[:500].lower() or b"login" in body[:500].lower():
            raise RuntimeErrorJson("auth_required", "Tracker did not return a torrent file.")
    filename = f"{tracker['id']}_{torrent_id}.torrent"
    cd = headers.get("Content-Disposition", headers.get("content-Disposition", ""))
    fn_match = re.search(r"filename\*\s*=\s*UTF-8''([^;]+)|filename\*?\s*=\s*\"?([^\";]+)\"?", cd, flags=re.I)
    if fn_match:
        raw_name = fn_match.group(1) or fn_match.group(2) or ""
        filename = urllib.parse.unquote(raw_name.strip().strip('"')) or filename
    # Default start-immediately unless caller asked for paused.
    options = dict(options or {})
    if "addPaused" not in options:
        options["addPaused"] = False
    result = qb_add_torrent_file(downloader, body, filename, options)
    result["torrentId"] = torrent_id
    result["trackerId"] = tracker["id"]
    result["filename"] = filename
    if result.get("status") == "already_present" and not options.get("addPaused"):
        # If user asked to download/start and it exists paused, resume it.
        torrent = result.get("torrent") or {}
        state = str(torrent.get("state") or "")
        torrent_hash = torrent.get("hash")
        if torrent_hash and ("pause" in state.lower() or "stop" in state.lower()):
            resumed = qb_resume_torrents(downloader, [str(torrent_hash)])
            refreshed = qb_find_torrent(downloader, info_hash=str(torrent_hash))
            summary = summarize_torrent(refreshed) or torrent
            result["status"] = "resumed"
            result["resume"] = resumed
            result["torrent"] = summary
            result["display"] = summary.get("display") if isinstance(summary, dict) else result.get("display")
    return result


def qb_add_magnet(downloader: dict[str, Any], magnet: str, options: dict[str, Any]) -> dict[str, Any]:
    import urllib.parse

    if downloader.get("type") != "qbittorrent":
        raise RuntimeErrorJson("capability_unavailable", "Adding downloads is available only for qBittorrent in the current environment.", downloaderType=downloader.get("type"))
    if not magnet.startswith("magnet:"):
        raise RuntimeErrorJson("validation_failed", "Only magnet URLs are accepted by this direct command.")
    headers = qb_session_headers(downloader)
    fields = {"urls": magnet}
    if options.get("savePath"):
        fields["savepath"] = str(options["savePath"])
    if options.get("categoryOrLabel"):
        fields["category"] = str(options["categoryOrLabel"])
    if options.get("tags"):
        fields["tags"] = ",".join(options["tags"]) if isinstance(options["tags"], list) else str(options["tags"])
    if "addPaused" in options:
        paused = "true" if options.get("addPaused") else "false"
        fields["paused"] = paused
        fields["stopped"] = paused
    data = urllib.parse.urlencode(fields).encode("utf-8")
    status, _final_url, body, _headers = request(
        "POST",
        base_url_join(downloader["baseUrl"], "/api/v2/torrents/add"),
        headers={**headers, "Content-Type": "application/x-www-form-urlencoded"},
        data=data,
    )
    text = body.decode("utf-8", errors="ignore")
    if status in {401, 403}:
        raise RuntimeErrorJson("downloader_auth_failed", "qBittorrent rejected credentials.", statusCode=status)
    if status >= 400 or text == "Fails.":
        raise RuntimeErrorJson("downloader_add_failed", "qBittorrent rejected the magnet.", statusCode=status)
    return {"ok": True, "downloaderId": downloader["id"], "status": "added", "response": text or "Ok."}


def first_run_status(store: dict[str, Any], store_path: Path | None = None, store_source: str | None = None) -> dict[str, Any]:
    trackers = list(store.get("trackers", {}).values())
    drafts = list(store.get("trackerDrafts", {}).values())
    downloaders = list(store.get("downloaders", {}).values())
    stats = list(store.get("trackerStats", {}).values())

    enabled_trackers = [t for t in trackers if tracker_is_enabled_config(t)]
    usable_downloaders = [d for d in downloaders if d.get("enabled") is not False]

    next_steps: list[dict[str, Any]] = []
    if not enabled_trackers:
        if trackers or drafts:
            next_steps.append({
                "id": "repair_tracker",
                "label": "修复已有站点配置",
                "prompt": "我发现已有站点配置，但还没有静态校验通过的可用站点。请补齐缺失凭据引用或改用兼容认证方式。",
            })
        else:
            next_steps.append({
                "id": "add_tracker",
                "label": "添加第一个 PT 站点",
                "prompt": "请发送站点名和接入方式，例如：添加 {站点名}，使用 cookieRef=env://SITE_COOKIE。",
            })
    if not usable_downloaders:
        next_steps.append({
            "id": "add_downloader",
            "label": "添加下载器",
            "prompt": "请发送下载器信息，例如：type=qbittorrent baseUrl=http://nas:8080 credentialRef=env://QB_CREDENTIALS。",
        })
    if enabled_trackers and usable_downloaders:
        next_steps.append({
            "id": "ready_to_search",
            "label": "开始搜索",
            "prompt": "你可以直接说：搜索 沙丘 2160p。",
        })

    payload = {
        "ok": True,
        "firstRun": not trackers and not drafts and not downloaders,
        "summary": {
            "trackers": len(trackers),
            "trackerDrafts": len(drafts),
            "enabledTrackers": len(enabled_trackers),
            "downloaders": len(downloaders),
            "usableDownloaders": len(usable_downloaders),
            "trackerStats": len(stats),
        },
        "trackers": [{"id": t.get("id"), "displayName": t.get("displayName"), "status": t.get("status")} for t in trackers],
        "trackerDrafts": [{"id": t.get("id"), "displayName": t.get("displayName"), "status": t.get("status"), "missing": t.get("missing"), "credentialIssue": t.get("credentialIssue")} for t in drafts],
        "downloaders": [{"id": d.get("id"), "displayName": d.get("displayName"), "type": d.get("type")} for d in downloaders],
        "trackerStats": [{"trackerId": s.get("trackerId"), "status": s.get("status"), "message": s.get("message"), "updatedAt": s.get("updatedAt")} for s in stats],
        "nextSteps": next_steps,
    }
    if store_path is not None:
        payload["storage"] = {
            "store": str(store_path),
            "storeSource": store_source,
            "exists": store_path.exists(),
        }
    return payload




def qb_resume_torrents(downloader: dict[str, Any], hashes: list[str] | None = None) -> dict[str, Any]:
    if downloader.get("type") != "qbittorrent":
        raise RuntimeErrorJson(
            "capability_unavailable",
            "Resume is available only for qBittorrent in the current environment.",
            downloaderType=downloader.get("type"),
        )
    base = downloader.get("baseUrl")
    if not base:
        raise RuntimeErrorJson("validation_failed", "Downloader baseUrl is required.")
    headers = qb_session_headers(downloader)
    target = "|".join(hashes) if hashes else "all"
    import urllib.parse

    data = urllib.parse.urlencode({"hashes": target}).encode("utf-8")
    status, _final_url, body, _headers = request(
        "POST",
        base_url_join(base, "/api/v2/torrents/resume"),
        headers={**headers, "Content-Type": "application/x-www-form-urlencoded"},
        data=data,
    )
    # Newer qBittorrent versions renamed resume -> start.
    if status >= 400:
        status, _final_url, body, _headers = request(
            "POST",
            base_url_join(base, "/api/v2/torrents/start"),
            headers={**headers, "Content-Type": "application/x-www-form-urlencoded"},
            data=data,
        )
    if status in {401, 403}:
        raise RuntimeErrorJson("downloader_auth_failed", "qBittorrent rejected credentials.", statusCode=status)
    if status >= 400:
        raise RuntimeErrorJson("downloader_resume_failed", "qBittorrent rejected the resume request.", statusCode=status)
    return {
        "ok": True,
        "downloaderId": downloader["id"],
        "action": "resume",
        "hashes": hashes or ["all"],
        "response": body.decode("utf-8", errors="ignore") or "Ok.",
    }


def qb_list_torrents(downloader: dict[str, Any], filter_name: str | None = None, limit: int = 20) -> dict[str, Any]:
    if downloader.get("type") != "qbittorrent":
        raise RuntimeErrorJson(
            "capability_unavailable",
            "Torrent listing is available only for qBittorrent in the current environment.",
            downloaderType=downloader.get("type"),
        )
    base = downloader.get("baseUrl")
    if not base:
        raise RuntimeErrorJson("validation_failed", "Downloader baseUrl is required.")
    headers = qb_session_headers(downloader)
    path = "/api/v2/torrents/info"
    if filter_name:
        import urllib.parse

        path = path + "?" + urllib.parse.urlencode({"filter": filter_name})
    status, _final_url, body, _headers = request("GET", base_url_join(base, path), headers=headers)
    if status in {401, 403}:
        raise RuntimeErrorJson("downloader_auth_failed", "qBittorrent rejected credentials.", statusCode=status)
    if status >= 400:
        raise RuntimeErrorJson("downloader_unreachable", "qBittorrent torrent list returned an error.", statusCode=status)
    items = json.loads(body.decode("utf-8", errors="ignore") or "[]")
    if not isinstance(items, list):
        raise RuntimeErrorJson("parse_failed", "qBittorrent torrent list response was not a list.")
    items = sorted(items, key=lambda item: float(item.get("added_on") or 0), reverse=True)
    selected = items[: max(1, min(limit, 100))]
    torrents = []
    for item in selected:
        torrents.append({
            "hash": item.get("hash"),
            "name": item.get("name"),
            "state": item.get("state"),
            "progress": item.get("progress"),
            "sizeBytes": item.get("size"),
            "downloadRateBytesPerSec": item.get("dlspeed"),
            "uploadRateBytesPerSec": item.get("upspeed"),
            "category": item.get("category"),
            "tags": item.get("tags"),
            "addedOn": item.get("added_on"),
        })
    filter_labels = {
        "paused": "暂停",
        "downloading": "下载中",
        "completed": "已完成",
        "active": "活跃",
        "inactive": "不活跃",
        "stalled": "停滞",
        "errored": "出错",
        "all": "",
    }
    filter_label = filter_labels.get(filter_name or "all", filter_name or "")
    if not torrents:
        prefix = f"没有{filter_label}的任务。" if filter_label else "下载器里还没有任务。"
        display_text = f"{prefix}可以继续：查看全部任务、搜索新资源。"
    else:
        lines = [f"共 {len(items)} 个任务，显示最近 {len(torrents)} 个："]
        for index, item in enumerate(torrents[:5], start=1):
            progress = item.get("progress")
            try:
                progress_text = f"{float(progress) * 100:.1f}%" if progress is not None else None
            except (TypeError, ValueError):
                progress_text = None
            fields = [str(item.get("state") or "未知状态")]
            if progress_text:
                fields.append(progress_text)
            down_rate = format_bytes(item.get("downloadRateBytesPerSec"))
            if down_rate and item.get("downloadRateBytesPerSec"):
                fields.append(f"↓ {down_rate}/s")
            lines.append(f"{index}. {item.get('name') or '未命名任务'} · {' · '.join(fields)}")
        lines.extend(["", "可以继续：查看全部任务、查看暂停任务、恢复暂停任务。"])
        display_text = "\n".join(lines)
    return {
        "ok": True,
        "downloaderId": downloader["id"],
        "filter": filter_name or "all",
        "total": len(items),
        "torrents": torrents,
        "display": {
            "total": len(items),
            "showing": len(torrents),
            "filter": filter_name or "all",
            "text": display_text,
        },
    }

def overview(store: dict[str, Any], refresh: bool) -> dict[str, Any]:
    started = time.monotonic()
    trackers = [
        dict(record)
        for record in store.get("trackers", {}).values()
        if isinstance(record, dict) and tracker_is_enabled_config(record)
    ]
    downloaders = [dict(record) for record in store.get("downloaders", {}).values() if isinstance(record, dict)]
    cached_stats = {
        str(record.get("trackerId")): dict(record)
        for record in store.get("trackerStats", {}).values()
        if isinstance(record, dict) and record.get("trackerId")
    }

    if not refresh:
        return {
            "ok": True,
            "refreshed": False,
            "trackers": [
                {
                    "trackerId": tracker.get("id"),
                    "displayName": tracker.get("displayName") or tracker.get("name") or tracker.get("id"),
                    "status": tracker.get("status"),
                    "stats": cached_stats.get(str(tracker.get("id"))),
                }
                for tracker in trackers
            ],
            "downloaders": [
                {"downloaderId": item.get("id"), "type": item.get("type"), "status": item.get("status")}
                for item in downloaders
            ],
            "elapsedMs": round((time.monotonic() - started) * 1000),
        }

    def refresh_tracker(tracker: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        tracker_id = str(tracker.get("id"))
        try:
            return tracker_id, user_stats(tracker)
        except RuntimeErrorJson as exc:
            return tracker_id, {"ok": False, "error": exc.payload}

    def refresh_downloader(item: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        downloader_id = str(item.get("id"))
        try:
            return downloader_id, downloader_status(item)
        except RuntimeErrorJson as exc:
            return downloader_id, {"ok": False, "error": exc.payload}

    tracker_reports: dict[str, dict[str, Any]] = {}
    downloader_reports: dict[str, dict[str, Any]] = {}
    jobs: list[tuple[str, str, dict[str, Any]]] = [
        ("tracker", str(item.get("id")), item) for item in trackers
    ] + [("downloader", str(item.get("id")), item) for item in downloaders]
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=min(6, max(1, len(jobs)))) as executor:
        future_map = {
            executor.submit(refresh_tracker if kind == "tracker" else refresh_downloader, item): (kind, item_id)
            for kind, item_id, item in jobs
        }
        for future in concurrent.futures.as_completed(future_map):
            kind, item_id = future_map[future]
            _resolved_id, report = future.result()
            if kind == "tracker":
                tracker_reports[item_id] = report
            else:
                downloader_reports[item_id] = report

    failures = [
        {"kind": kind, "id": item_id, "error": report.get("error")}
        for kind, reports in (("tracker", tracker_reports), ("downloader", downloader_reports))
        for item_id, report in reports.items()
        if not report.get("ok")
    ]
    return {
        "ok": not failures,
        "refreshed": True,
        "trackers": [
            {
                "trackerId": tracker.get("id"),
                "displayName": tracker.get("displayName") or tracker.get("name") or tracker.get("id"),
                **tracker_reports.get(str(tracker.get("id")), {"ok": False}),
            }
            for tracker in trackers
        ],
        "downloaders": [
            {"downloaderId": item.get("id"), **downloader_reports.get(str(item.get("id")), {"ok": False})}
            for item in downloaders
        ],
        "failures": failures,
        "elapsedMs": round((time.monotonic() - started) * 1000),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="pt-agent direct runtime CLI")
    parser.add_argument(
        "--store",
        help=(
            "store path; defaults to PT_AGENT_STORE, PT_AGENT_HOME/store.json, "
            "host home, installed skill home, or XDG state"
        ),
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("first-run")

    p_overview = sub.add_parser("overview")
    p_overview.add_argument("--refresh", action="store_true")

    p_site = sub.add_parser("site-presets")
    p_site.add_argument("query")

    p_adapter = sub.add_parser("adapter-presets")
    p_adapter.add_argument("adapterIds", nargs="*")

    p_validate = sub.add_parser("validate-tracker")
    p_validate.add_argument("--tracker", required=True)

    p_health = sub.add_parser("health-check")
    p_health.add_argument("--tracker", required=True)

    p_stats = sub.add_parser("user-stats")
    p_stats.add_argument("--tracker", required=True)
    p_stats.add_argument("--persist", action="store_true")

    p_search = sub.add_parser("search")
    p_search.add_argument("keyword")
    p_search.add_argument("--tracker", "--site", dest="tracker")
    p_search.add_argument("--limit", type=int, default=20)

    p_media = sub.add_parser("media-search")
    p_media.add_argument("query")
    p_media.add_argument("--tracker", "--site", dest="trackers", action="append", default=[])
    p_media.add_argument("--all-trackers", action="store_true")
    p_media.add_argument("--kind", choices=("movie", "tv", "any"), default="any")
    p_media.add_argument("--limit", type=int, default=10)
    p_media.add_argument("--timeout", type=int, default=10)
    p_media.add_argument("--free-only", action="store_true")
    p_media.add_argument("--resolution", choices=("4k", "2160p", "1080p", "720p"))
    p_media.add_argument("--sort", choices=("relevance", "seeders", "size"), default="relevance")

    p_downloader = sub.add_parser("downloader-status")
    p_downloader.add_argument("--downloader")

    p_add_magnet = sub.add_parser("add-magnet")
    p_add_magnet.add_argument("--downloader")
    p_add_magnet.add_argument("--magnet", required=True)
    p_add_magnet.add_argument("--save-path")
    p_add_magnet.add_argument("--category")
    p_add_magnet.add_argument("--tags")
    p_add_magnet.add_argument("--paused", action="store_true")
    p_add_magnet.add_argument("--dry-run", action="store_true")

    p_dl_torrent = sub.add_parser("download-torrent")
    p_dl_torrent.add_argument("--tracker", required=True)
    p_dl_torrent.add_argument("--torrent-id", required=True)
    p_dl_torrent.add_argument("--downloader")
    p_dl_torrent.add_argument("--save-path")
    p_dl_torrent.add_argument("--category")
    p_dl_torrent.add_argument("--tags")
    p_dl_torrent.add_argument("--paused", action="store_true", help="Add torrent in paused/stopped state")
    p_dl_torrent.add_argument("--start", action="store_true", help="Add torrent and start downloading immediately")
    p_dl_torrent.add_argument("--dry-run", action="store_true")

    p_resume = sub.add_parser("resume-torrents")
    p_resume.add_argument("--downloader")
    p_resume.add_argument("--hash", dest="hashes", action="append", default=[])
    p_resume.add_argument("--all", action="store_true")
    p_resume.add_argument("--dry-run", action="store_true")

    p_list = sub.add_parser("list-torrents")
    p_list.add_argument("--downloader")
    p_list.add_argument("--filter", dest="torrent_filter", choices=("all", "downloading", "completed", "paused", "active", "inactive", "resumed", "stalled", "errored"))
    p_list.add_argument("--limit", type=int, default=20)

    args = parser.parse_args()
    try:
        if args.cmd == "site-presets":
            return emit(site_presets(args.query))
        if args.cmd == "adapter-presets":
            return emit(adapter_presets(args.adapterIds))

        store, store_path, store_source = load_store(args.store)
        if args.cmd == "first-run":
            return emit(first_run_status(store, store_path, store_source))
        if args.cmd == "overview":
            result = overview(store, args.refresh)
            if args.refresh:
                try:
                    for item in result.get("trackers", []):
                        tracker_id = item.get("trackerId")
                        if not tracker_id:
                            continue
                        if item.get("ok") and isinstance(item.get("stats"), dict):
                            pt_store.upsert_tracker_stats(store, str(tracker_id), item["stats"])
                        elif isinstance(item.get("error"), dict):
                            pt_store.upsert_tracker_stats(store, str(tracker_id), {
                                "status": item["error"].get("code", "failed"),
                                "message": item["error"].get("message", "Tracker refresh failed."),
                            })
                    pt_store.atomic_write(store_path, store)
                    result["persisted"] = True
                except pt_store.StoreError as exc:
                    raise RuntimeErrorJson(exc.payload["code"], exc.payload["message"], store=str(store_path)) from exc
            return emit(result)
        if args.cmd == "media-search":
            media_trackers = args.trackers
            if args.all_trackers:
                media_trackers = [
                    str(record.get("id"))
                    for record in store.get("trackers", {}).values()
                    if isinstance(record, dict) and record.get("id") and tracker_is_enabled_config(record)
                ]
            return emit(media_search(
                store,
                args.query,
                media_trackers,
                args.kind,
                max(1, min(args.limit, 50)),
                args.timeout,
                args.free_only,
                args.resolution,
                args.sort,
            ))
        if args.cmd in {"validate-tracker", "health-check", "user-stats", "search"}:
            tracker_alias = args.tracker
            if args.cmd == "search" and not tracker_alias:
                tracker_alias = store.get("defaultSearchSolutionId")
            if not tracker_alias:
                raise RuntimeErrorJson("configuration_required", "No tracker was selected and no default search tracker is configured.")
            tracker = find_tracker_record(store, str(tracker_alias))
            if args.cmd == "validate-tracker":
                return emit(validate_tracker(tracker))
            if args.cmd == "health-check":
                return emit(health_check(tracker))
            if args.cmd == "user-stats":
                store_path, _source = pt_store.resolve_store_path(args.store)
                try:
                    result = user_stats(tracker)
                    if args.persist:
                        try:
                            current = pt_store.load_store(store_path)
                            pt_store.upsert_tracker_stats(current, tracker["id"], result["stats"])
                            pt_store.atomic_write(store_path, current)
                        except pt_store.StoreError as exc:
                            raise RuntimeErrorJson(exc.payload["code"], exc.payload["message"], store=str(store_path), storeSource=store_source) from exc
                    return emit(result)
                except RuntimeErrorJson as exc:
                    if args.persist:
                        try:
                            current = pt_store.load_store(store_path)
                            pt_store.upsert_tracker_stats(current, tracker["id"], {
                                "status": exc.payload.get("code", "failed"),
                                "message": exc.payload.get("message", "Tracker stats failed."),
                            })
                            pt_store.atomic_write(store_path, current)
                        except pt_store.StoreError as store_exc:
                            raise RuntimeErrorJson(store_exc.payload["code"], store_exc.payload["message"], store=str(store_path), storeSource=store_source) from store_exc
                    raise
            if args.cmd == "search":
                return emit(search_tracker(tracker, args.keyword, args.limit))
        if args.cmd == "downloader-status":
            downloader_id = args.downloader or store.get("defaultDownloaderId")
            if not downloader_id:
                raise RuntimeErrorJson("configuration_required", "No downloader was selected and no default downloader is configured.")
            downloader = find_downloader_record(store, str(downloader_id))
            return emit(downloader_status(downloader))
        if args.cmd == "add-magnet":
            downloader_id = args.downloader or store.get("defaultDownloaderId")
            if not downloader_id:
                raise RuntimeErrorJson("configuration_required", "No downloader was selected and no default downloader is configured.")
            downloader = find_downloader_record(store, str(downloader_id))
            options = {
                "savePath": args.save_path,
                "categoryOrLabel": args.category,
                "tags": [x.strip() for x in args.tags.split(",")] if args.tags else None,
                "addPaused": True if args.paused else False,
            }
            sanitized_options = {k: v for k, v in options.items() if v is not None}
            if args.dry_run:
                if not args.magnet.startswith("magnet:"):
                    raise RuntimeErrorJson("validation_failed", "Only magnet URLs are accepted by this command.")
                return emit({
                    "ok": True,
                    "dryRun": True,
                    "action": "add_magnet",
                    "downloaderId": downloader.get("id"),
                    "magnetRef": opaque_ref(args.magnet),
                    "options": sanitized_options,
                })
            return emit(qb_add_magnet(downloader, args.magnet, sanitized_options))
        if args.cmd == "download-torrent":
            tracker = find_tracker_record(store, args.tracker)
            downloader_id = args.downloader or store.get("defaultDownloaderId")
            if not downloader_id:
                raise RuntimeErrorJson("configuration_required", "No downloader was selected and no default downloader is configured.")
            downloader = find_downloader_record(store, str(downloader_id))
            if args.paused and args.start:
                raise RuntimeErrorJson("validation_failed", "Use only one of --paused or --start.")
            options = {
                "savePath": args.save_path,
                "categoryOrLabel": args.category,
                "tags": [x.strip() for x in args.tags.split(",")] if args.tags else None,
                # Default path is start-immediately. --paused is the only opt-out.
                "addPaused": True if args.paused else False,
            }
            sanitized_options = {k: v for k, v in options.items() if v is not None}
            if args.dry_run:
                validate_tracker(tracker)
                return emit({
                    "ok": True,
                    "dryRun": True,
                    "action": "download_torrent",
                    "trackerId": tracker.get("id"),
                    "torrentId": args.torrent_id,
                    "downloaderId": downloader.get("id"),
                    "options": sanitized_options,
                })
            return emit(download_torrent(tracker, args.torrent_id, downloader, sanitized_options))
        if args.cmd == "resume-torrents":
            downloader_id = args.downloader or store.get("defaultDownloaderId")
            if not downloader_id:
                raise RuntimeErrorJson("configuration_required", "No downloader was selected and no default downloader is configured.")
            downloader = find_downloader_record(store, str(downloader_id))
            hashes = [item for item in (args.hashes or []) if item]
            if not hashes and not args.all:
                raise RuntimeErrorJson("validation_failed", "Provide --hash at least once, or pass --all to resume everything.")
            if args.dry_run:
                return emit({
                    "ok": True,
                    "dryRun": True,
                    "action": "resume_torrents",
                    "downloaderId": downloader.get("id"),
                    "hashes": hashes or ["all"],
                })
            return emit(qb_resume_torrents(downloader, None if args.all else hashes))
        if args.cmd == "list-torrents":
            downloader_id = args.downloader or store.get("defaultDownloaderId")
            if not downloader_id:
                raise RuntimeErrorJson("configuration_required", "No downloader was selected and no default downloader is configured.")
            downloader = find_downloader_record(store, str(downloader_id))
            return emit(qb_list_torrents(downloader, args.torrent_filter, args.limit))
    except RuntimeErrorJson as exc:
        return fail(exc)
    return emit({"ok": False, "error": {"code": "unhandled_command", "message": args.cmd}})


if __name__ == "__main__":
    raise SystemExit(main())
