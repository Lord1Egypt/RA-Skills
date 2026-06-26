from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote, urlparse


VIDEO_URL_HINTS = (
    "http://",
    "https://",
    "www.",
    "youtu",
    "bilibili",
    "b23.tv",
    "tiktok",
    "douyin",
    "instagram",
    "twitter",
    "x.com",
    "weibo",
    "vimeo",
    "reddit",
)

ANIME_TERMS = (
    "\u52a8\u6f2b",
    "\u52a8\u753b",
    "\u756a\u5267",
    "\u65b0\u756a",
    "ova",
    "attack on titan",
    "one piece",
    "naruto",
    "demon slayer",
    "\u8fdb\u51fb",
    "\u5de8\u4eba",
    "\u6d77\u8d3c",
    "\u706b\u5f71",
)
TV_TERMS = ("season", "episode", "\u7f8e\u5267", "\u82f1\u5267", "\u97e9\u5267", "\u65e5\u5267")
MUSIC_TERMS = ("\u97f3\u4e50", "\u4e13\u8f91", "\u5355\u66f2", "flac", "mp3", "\u65e0\u635f", "ost", "soundtrack")
SOFTWARE_TERMS = ("\u8f6f\u4ef6", "\u6e38\u620f", "portable", "apk", ".exe", "steam", "\u7834\u89e3", "keygen")
SOFTWARE_BRANDS = (
    "adobe",
    "photoshop",
    "illustrator",
    "premiere",
    "after effects",
    "windows",
    "office",
    "visual studio",
    "jetbrains",
    "pycharm",
    "intellij",
)
BOOK_TERMS = ("epub", "pdf", "\u7535\u5b50\u4e66", "\u5c0f\u8bf4", "\u6f2b\u753b", "manga", "comic")
SUBTITLE_TERMS = ("\u4e2d\u5b57", "\u5b57\u5e55", "sub", "subtitle")
LOSSLESS_TERMS = ("flac", "\u65e0\u635f", "ape", "alac")

RELEASE_NOISE_TERMS = {
    "1080p",
    "2160p",
    "720p",
    "480p",
    "4k",
    "uhd",
    "hdr",
    "dovi",
    "bluray",
    "blu",
    "ray",
    "bdrip",
    "webrip",
    "webdl",
    "web",
    "web-dl",
    "remux",
    "hevc",
    "x265",
    "x264",
    "h265",
    "h264",
    "aac",
    "ac3",
    "ddp",
    "dts",
    "10bit",
    "proper",
    "repack",
    "extended",
    "limited",
    "dubbed",
    "multi",
    "dual",
    "audio",
    "sub",
    "subs",
    "subtitle",
    "subtitles",
    "complete",
}

STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "of",
    "to",
    "for",
    "in",
    "on",
    "with",
    "at",
}

QUALITY_RESOLUTION_RE = re.compile(r"\b(2160p|1080p|720p|480p)\b", re.I)
SEASON_EPISODE_RE = re.compile(r"s(?P<season>\d{1,2})e(?P<episode>\d{1,2})", re.I)
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
TOKEN_RE = re.compile(r"[\u4e00-\u9fff]+|[a-z0-9]+", re.I)
EN_ALIAS_PAREN_RE = re.compile(r"[\(\uff08]([A-Za-z][^()\uff08\uff09]{1,80})[\)\uff09]")
EN_ALIAS_RE = re.compile(r"([A-Za-z][A-Za-z0-9\s\.\-:]{2,80})")
CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")
TITLE_CORE_CLEAN_RE = re.compile(
    r"\b(?:s\d{1,2}e\d{1,2}|season|episode|ep|part|2160p|1080p|720p|480p|4k|uhd|hdr|dovi|"
    r"bluray|bdrip|webrip|web[- ]?dl|remux|hevc|x265|x264|h\.?265|h\.?264|aac|ac3|ddp|dts|"
    r"10bit|proper|repack|extended|limited)\b",
    re.I,
)

PROVIDER_LABELS = {
    "aliyun": "aliyun",
    "alipan": "aliyun",
    "quark": "quark",
    "baidu": "baidu",
    "115": "115",
    "pikpak": "pikpak",
    "uc": "uc",
    "xunlei": "xunlei",
    "123": "123pan",
    "tianyi": "tianyi",
    "magnet": "magnet",
    "ed2k": "ed2k",
    "mega": "mega",
    "mediafire": "mediafire",
    "gdrive": "gdrive",
    "onedrive": "onedrive",
    "cowtransfer": "cowtransfer",
    "lanzou": "lanzou",
}

DOMAIN_PROVIDER_MAP = {
    "aliyundrive.com": "aliyun",
    "alipan.com": "aliyun",
    "pan.quark.cn": "quark",
    "pan.baidu.com": "baidu",
    "115.com": "115",
    "115cdn.com": "115",
    "mypikpak.com": "pikpak",
    "pan.pikpak.com": "pikpak",
    "drive.uc.cn": "uc",
    "pan.xunlei.com": "xunlei",
    "123pan.com": "123",
    "123684.com": "123",
    "123865.com": "123",
    "123912.com": "123",
    "cloud.189.cn": "tianyi",
    "mega.nz": "mega",
    "mediafire.com": "mediafire",
    "drive.google.com": "gdrive",
    "onedrive.live.com": "onedrive",
    "cowtransfer.com": "cowtransfer",
    "lanzou": "lanzou",
    "lanzoux.com": "lanzou",
    "lanzouq.com": "lanzou",
}

PLATFORM_MAP = {
    "youtube.com": "YouTube",
    "youtu.be": "YouTube",
    "bilibili.com": "Bilibili",
    "b23.tv": "Bilibili",
    "tiktok.com": "TikTok",
    "douyin.com": "Douyin",
    "instagram.com": "Instagram",
    "twitter.com": "Twitter/X",
    "x.com": "Twitter/X",
    "weibo.com": "Weibo",
    "v.qq.com": "Tencent Video",
    "iqiyi.com": "iQIYI",
    "youku.com": "Youku",
    "acfun.cn": "AcFun",
    "nicovideo.jp": "NicoNico",
    "twitch.tv": "Twitch",
    "vimeo.com": "Vimeo",
    "facebook.com": "Facebook",
    "reddit.com": "Reddit",
}


def ensure_utf8_stdio() -> None:
    for handle_name in ("stdout", "stderr"):
        handle = getattr(sys, handle_name, None)
        if hasattr(handle, "reconfigure"):
            handle.reconfigure(encoding="utf-8", errors="replace")


def storage_root() -> Path:
    workspace = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw" / "workspace"))
    root = workspace / "storage" / "resource-hunter"
    root.mkdir(parents=True, exist_ok=True)
    return root


def default_download_dir() -> Path:
    workspace_downloads = Path.home() / ".openclaw" / "workspace" / "storage" / "downloads"
    if workspace_downloads.parent.exists():
        workspace_downloads.mkdir(parents=True, exist_ok=True)
        return workspace_downloads
    downloads = Path.home() / "Downloads"
    downloads.mkdir(parents=True, exist_ok=True)
    return downloads


def compact_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def has_chinese(text: str) -> bool:
    return bool(CHINESE_RE.search(text or ""))


def extract_year(text: str) -> str:
    match = YEAR_RE.search(text or "")
    return match.group(0) if match else ""


def extract_season_episode(text: str) -> tuple[int | None, int | None]:
    match = SEASON_EPISODE_RE.search(text or "")
    if match:
        return int(match.group("season")), int(match.group("episode"))
    cn_match = re.search(r"\u7b2c\s*(\d{1,2})\s*\u5b63", text or "")
    ep_match = re.search(r"\u7b2c\s*(\d{1,3})\s*\u96c6", text or "")
    return (
        int(cn_match.group(1)) if cn_match else None,
        int(ep_match.group(1)) if ep_match else None,
    )


def is_video_url(text: str) -> bool:
    lowered = (text or "").lower()
    return any(hint in lowered for hint in VIDEO_URL_HINTS)


def extract_english_alias(text: str) -> str:
    if is_video_url(text):
        return ""
    match = EN_ALIAS_PAREN_RE.search(text or "")
    if match:
        return compact_spaces(match.group(1))
    match = EN_ALIAS_RE.search(text or "")
    if not match:
        return ""
    alias = compact_spaces(match.group(1))
    alias = re.sub(r"\s+[A-Z]$", "", alias).strip()
    return alias if len(alias) >= 3 else ""


def extract_chinese_alias(text: str) -> str:
    chunks = re.findall(r"[\u4e00-\u9fff0-9\uff1a:\u00b7\-\s]{2,80}", text or "")
    cleaned = [compact_spaces(chunk) for chunk in chunks if has_chinese(chunk)]
    return cleaned[0] if cleaned else ""


def _strip_title_noise(text: str) -> str:
    value = text.lower()
    value = YEAR_RE.sub(" ", value)
    value = TITLE_CORE_CLEAN_RE.sub(" ", value)
    value = re.sub(r"[\[\]\(\)\{\}_\-\.,/:]+", " ", value)
    return compact_spaces(value)


def title_tokens(text: str, keep_numeric: bool = False) -> list[str]:
    tokens: list[str] = []
    for token in TOKEN_RE.findall(_strip_title_noise(text)):
        lowered = token.lower()
        if lowered in STOPWORDS or lowered in RELEASE_NOISE_TERMS:
            continue
        if not keep_numeric and lowered.isdigit():
            continue
        if len(lowered) == 1 and not CHINESE_RE.search(lowered):
            continue
        tokens.append(lowered)
    return tokens


def title_core(text: str) -> str:
    return " ".join(title_tokens(text))


def unique_preserve(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if not item:
            continue
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def detect_platform(url: str) -> str:
    lowered = (url or "").lower()
    for domain, name in PLATFORM_MAP.items():
        if domain in lowered:
            return name
    return "Unknown"


def detect_kind(text: str, explicit_kind: str | None = None) -> str:
    if explicit_kind:
        return explicit_kind
    lowered = (text or "").lower()
    if is_video_url(lowered):
        return "video"
    if lowered.startswith("magnet:") or lowered.endswith(".torrent"):
        return "torrent"
    season, episode = extract_season_episode(lowered)
    if season or episode:
        return "tv"
    if any(term in lowered for term in ANIME_TERMS):
        return "anime"
    if any(term in lowered for term in MUSIC_TERMS):
        return "music"
    if any(term in lowered for term in SOFTWARE_TERMS) or any(term in lowered for term in SOFTWARE_BRANDS):
        return "software"
    if any(term in lowered for term in BOOK_TERMS):
        return "book"
    if extract_year(lowered) and extract_english_alias(text):
        return "movie"
    return "general"


def text_contains_any(text: str, terms: Iterable[str]) -> bool:
    lowered = (text or "").lower()
    return any(term.lower() in lowered for term in terms)


def normalize_title(text: str) -> str:
    cleaned = re.sub(r"<[^>]+>", " ", text or "")
    cleaned = unquote(cleaned)
    cleaned = compact_spaces(cleaned)
    return cleaned.strip(" -_|[]()")


def normalize_key(text: str) -> str:
    cleaned = normalize_title(text).lower()
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", cleaned)


def parse_quality_tags(text: str) -> dict[str, Any]:
    lowered = (text or "").lower()
    resolution_match = QUALITY_RESOLUTION_RE.search(lowered)
    resolution = resolution_match.group(1).lower() if resolution_match else ""
    if not resolution:
        if re.search(r"\b(4k|uhd)\b", lowered):
            resolution = "2160p"
    source = ""
    if "bluray" in lowered or "blu-ray" in lowered:
        source = "bluray"
    elif "bdrip" in lowered:
        source = "bdrip"
    elif "web-dl" in lowered or "webdl" in lowered:
        source = "web-dl"
    elif "webrip" in lowered:
        source = "webrip"
    elif "hdtv" in lowered:
        source = "hdtv"
    elif "cam" in lowered or "hdts" in lowered or "ts" in lowered:
        source = "cam"

    hdr_flags = []
    for flag in ("hdr", "dovi", "dolby", "dv"):
        if flag in lowered:
            hdr_flags.append(flag)
    pack = "remux" if "remux" in lowered else ""
    subtitle = text_contains_any(text, SUBTITLE_TERMS)
    lossless = any(term in lowered for term in LOSSLESS_TERMS)
    book_format = "pdf" if "pdf" in lowered else "epub" if "epub" in lowered else ""
    return {
        "resolution": resolution,
        "source": source,
        "pack": pack,
        "hdr_flags": hdr_flags,
        "subtitle": subtitle,
        "lossless": lossless,
        "book_format": book_format,
    }


def infer_quality(text: str) -> str:
    tags = parse_quality_tags(text)
    if tags["book_format"]:
        return tags["book_format"]
    if tags["lossless"]:
        return "lossless"
    return tags["resolution"]


def infer_provider_from_url(url: str) -> str:
    parsed = urlparse(url or "")
    host = parsed.netloc.lower()
    for domain, provider in DOMAIN_PROVIDER_MAP.items():
        if domain in host:
            return provider
    if (url or "").startswith("magnet:"):
        return "magnet"
    if (url or "").startswith("ed2k://"):
        return "ed2k"
    return "other"


def extract_password(text: str) -> str:
    decoded = unquote(text or "")
    match = re.search(r"[?&](?:password|pwd|pass)=([^&#]+)", decoded, re.I)
    if match:
        return match.group(1).strip()
    match = re.search(r"(?:\u63d0\u53d6\u7801|\u63d0\u53d6\u78bc|\u5bc6\u7801)[:\uff1a ]*([A-Za-z0-9]{4,8})", decoded)
    if match:
        return match.group(1)
    match = re.search(r"\?([A-Za-z0-9]{4,8})$", decoded)
    if match:
        return match.group(1)
    return ""


def clean_share_url(url: str) -> str:
    decoded = unquote(url or "")
    decoded = re.sub(r"[?&](?:password|pwd|pass)=[^&#]*", "", decoded, flags=re.I)
    decoded = re.sub(r"(?:\u63d0\u53d6\u7801|\u63d0\u53d6\u78bc|\u5bc6\u7801)[:\uff1a ]*[A-Za-z0-9]{4,8}", "", decoded)
    return decoded.rstrip("?&#, ").strip()


def extract_share_id(url: str, provider_hint: str = "") -> str:
    cleaned = clean_share_url(url)
    parsed = urlparse(cleaned)
    path = parsed.path.rstrip("/")
    if cleaned.startswith("magnet:"):
        match = re.search(r"btih:([A-Fa-f0-9]+)", cleaned)
        return match.group(1).lower() if match else normalize_key(cleaned)[:32]
    if cleaned.startswith("ed2k://"):
        return normalize_key(cleaned)[:32]
    if provider_hint == "baidu":
        match = re.search(r"/s/([A-Za-z0-9_-]+)", path)
        if match:
            return match.group(1)
    if provider_hint in {"aliyun", "quark", "uc", "xunlei", "123", "tianyi", "pikpak", "mega"}:
        parts = [part for part in path.split("/") if part]
        if parts:
            return parts[-1]
    parts = [part for part in path.split("/") if part]
    return parts[-1] if parts else parsed.netloc.lower()


def source_priority(source_name: str) -> int:
    priorities = {
        "2fun": 1,
        "hunhepan": 2,
        "pansou.vip": 3,
        "nyaa": 1,
        "eztv": 1,
        "tpb": 2,
        "yts": 2,
        "1337x": 3,
    }
    return priorities.get((source_name or "").lower(), 9)


def dump_json(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False)


def safe_filename(name: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|]+", "_", name).strip()
    return value or "download"


def token_overlap_score(query_tokens: list[str], title_tokens_: list[str]) -> float:
    if not query_tokens or not title_tokens_:
        return 0.0
    query_set = set(query_tokens)
    title_set = set(title_tokens_)
    shared = query_set & title_set
    if not shared:
        return 0.0
    return round(len(shared) / max(len(query_set), len(title_set)), 4)


def quality_display_from_tags(tags: dict[str, Any]) -> str:
    if tags.get("book_format"):
        return tags["book_format"]
    if tags.get("lossless"):
        return "lossless"
    if tags.get("resolution"):
        return tags["resolution"]
    return ""
