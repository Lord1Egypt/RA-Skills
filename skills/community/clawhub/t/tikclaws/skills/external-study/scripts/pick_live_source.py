#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import random
import re
import shlex
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

XIAOHONGSHU_HOST = "xiaohongshu.com"
XIAOHONGSHU_NOTE_PATH = "/explore/"
TIKTOK_HOST = "tiktok.com"
TIKTOK_VIDEO_PATH = "/video/"

SEARCH_TOPICS = [
    "cinematic short",
    "street video",
    "mini documentary",
    "dance video",
    "nature short",
    "food video",
    "craft process video",
    "night city video",
    "creative camera movement",
    "character moment video",
]

PLATFORM_SEARCH_TOPICS = {
    "x": [
        "breaking video",
        "weather video",
        "street video",
        "wildlife video",
        "space video",
        "camera footage",
        "short clip",
        "news video",
    ],
    "youtube_shorts": SEARCH_TOPICS,
    "tiktok": SEARCH_TOPICS,
    "xiaohongshu": [
        "恋爱",
        "情侣",
        "日常",
        "旅行",
        "美食",
        "舞蹈",
        "手工",
        "城市",
        "校园",
        "vlog",
        "剧情",
        "电影感",
        "记录生活",
        "探店",
        "宠物",
        "穿搭",
        "运动",
        "街拍",
        "生活碎片",
        "氛围感",
    ],
}
PLATFORM_SEARCH_TOPICS["tiktok"] = SEARCH_TOPICS + [
    "original sound dance",
    "TikTok video dance",
    "original sound food",
    "travel TikTok video",
]

USER_AGENT = "Mozilla/5.0 TikClawsLiveSourcePicker/1.0"


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def fetch_text(url: str, timeout: int = 25) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
    return raw.decode("utf-8", errors="replace")


def jina_url(target: str) -> str:
    return "https://r.jina.ai/http://" + target


def dedupe(urls: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for url in urls:
        clean = normalize_candidate_url(url)
        if not clean or clean in seen:
            continue
        seen.add(clean)
        out.append(clean)
    return out


def normalize_candidate_url(url: str) -> str:
    url = html.unescape(url).strip().strip("'\"<>.,;)")
    # Yahoo redirect decoding can leave ranking suffixes attached to the target
    # URL. They are not part of the platform canonical URL and can poison
    # dedupe/backend freshness checks even when yt-dlp tolerates them.
    for marker in ("/RK=", "/RS="):
        if marker in url:
            url = url.split(marker, 1)[0]
    if not url:
        return ""
    if url.startswith("//"):
        url = "https:" + url
    if url.startswith("www.") or url.startswith("x.com/") or url.startswith("twitter.com/") or url.startswith("xiaohongshu.com/") or url.startswith("tiktok.com/"):
        url = "https://" + url
    parsed = urllib.parse.urlsplit(url)
    if parsed.netloc in {"duckduckgo.com", "www.duckduckgo.com"} and parsed.path.startswith("/l/"):
        qs = urllib.parse.parse_qs(parsed.query)
        uddg = (qs.get("uddg") or [""])[0]
        if uddg:
            return normalize_candidate_url(urllib.parse.unquote(uddg))
    # Strip obvious tracking while preserving platform-required query values.
    if "xiaohongshu.com" not in parsed.netloc:
        parsed = parsed._replace(query="", fragment="")
    return urllib.parse.urlunsplit(parsed)


def platform_candidate_match(url: str, platform: str) -> bool:
    if platform == "youtube_shorts":
        return bool(re.search(r"(?:youtube\.com/(?:shorts/|watch\?v=)|youtu\.be/)[A-Za-z0-9_-]{11}", url))
    if platform == "x":
        return bool(re.search(r"(?:x|twitter)\.com/[A-Za-z0-9_]+/status/\d+", url))
    if platform == "xiaohongshu":
        return bool(re.search(r"xiaohongshu\.com/explore/[0-9A-Fa-f]{24}", url))
    if platform == "tiktok":
        return bool(re.search(r"tiktok\.com/@(?:[^/\s\]\)]+)?/video/\d+", url))
    return False


def extract_urls_from_text(text: str, platform: str) -> list[str]:
    text = html.unescape(text)
    urls: list[str] = []
    for encoded in re.findall(r"uddg=([^&\)\]]+)", text):
        decoded = urllib.parse.unquote(encoded)
        if platform_candidate_match(decoded, platform):
            urls.append(decoded)
    for encoded in re.findall(r"/RU=([^/]+(?:%2[fF]|/)[^\"<\s]+?)/(?:RK|RS)=", text):
        decoded = urllib.parse.unquote(encoded)
        if platform_candidate_match(decoded, platform):
            urls.append(decoded)
    for encoded in re.findall(r"https?%3A%2F%2F[^\"<\s]+", text, flags=re.I):
        decoded = urllib.parse.unquote(encoded)
        if platform_candidate_match(decoded, platform):
            urls.append(decoded)
    if platform == "youtube_shorts":
        patterns = [
            r"https?://(?:www\.)?youtube\.com/shorts/[A-Za-z0-9_-]{11}",
            r"https?://(?:www\.)?youtube\.com/watch\?v=[A-Za-z0-9_-]{11}",
            r"/(?:shorts/[A-Za-z0-9_-]{11}|watch\?v=[A-Za-z0-9_-]{11})",
        ]
        for pat in patterns:
            for m in re.findall(pat, text):
                urls.append("https://www.youtube.com" + m if m.startswith("/") else m)
    elif platform == "x":
        for m in re.findall(r"(?:https?://)?(?:www\.)?(?:x|twitter)\.com/[A-Za-z0-9_]+/status/\d+", text):
            urls.append(m)
    elif platform == "xiaohongshu":
        for m in re.findall(r"(?:https?://)?(?:www\.)?xiaohongshu\.com/explore/[0-9A-Fa-f]{24}(?:\?[^\s\]\)]+)?", text):
            urls.append(m)
    elif platform == "tiktok":
        for m in re.findall(r"(?:https?://)?(?:www\.)?tiktok\.com/@[^/\s\]\)]+/video/\d+(?:\?[^\s\]\)]+)?", text):
            urls.append(m)
    return dedupe(urls)


def discovery_urls(platform: str, topic: str) -> list[str]:
    q = urllib.parse.quote_plus(topic)
    if platform == "youtube_shorts":
        return [jina_url(f"https://www.youtube.com/results?search_query={q}+shorts")]
    if platform == "x":
        return [
            jina_url("https://duckduckgo.com/html/?q=" + urllib.parse.quote_plus(f"site:x.com/ status video {topic}")),
            jina_url("https://duckduckgo.com/html/?q=" + urllib.parse.quote_plus(f"site:twitter.com/ status video {topic}")),
        ]
    if platform == "xiaohongshu":
        search_queries = [
            f"site:{XIAOHONGSHU_HOST}{XIAOHONGSHU_NOTE_PATH} \"type=video\" \"{topic}\"",
            f"site:{XIAOHONGSHU_HOST}{XIAOHONGSHU_NOTE_PATH} \"app_platform=ios\" \"type=video\" \"{topic}\"",
            f"site:{XIAOHONGSHU_HOST}{XIAOHONGSHU_NOTE_PATH} \"app_platform=android\" \"type=video\" \"{topic}\"",
            f"site:{XIAOHONGSHU_HOST}{XIAOHONGSHU_NOTE_PATH} \"xsec_token\" \"{topic}\"",
            f"site:{XIAOHONGSHU_HOST}{XIAOHONGSHU_NOTE_PATH} \"share_channel=copy_link\" \"{topic}\"",
            f"site:{XIAOHONGSHU_HOST}{XIAOHONGSHU_NOTE_PATH} \"xhsshare\" \"{topic}\"",
            f"site:{XIAOHONGSHU_HOST}{XIAOHONGSHU_NOTE_PATH} \"小红书\" \"视频\" \"{topic}\"",
        ]
        out = []
        for query in search_queries:
            q = urllib.parse.quote_plus(query)
            # Yahoo exposes app-share URLs with xsec_token/type=video more
            # reliably than the static DuckDuckGo mirror. These are discovery
            # surfaces only; the selected canonical_url remains a concrete
            # Xiaohongshu note URL verified by yt-dlp.
            out.append("https://search.yahoo.com/search?p=" + q)
            out.append("https://au.search.yahoo.com/search?p=" + q)
        out.append(jina_url("https://duckduckgo.com/html/?q=" + urllib.parse.quote_plus(f"site:{XIAOHONGSHU_HOST}{XIAOHONGSHU_NOTE_PATH} 视频 {topic}")))
        return out
    if platform == "tiktok":
        search_queries = [
            f"site:{TIKTOK_HOST}/@ video {topic}",
            f"site:{TIKTOK_HOST}/@ \"TikTok\" \"video\" \"{topic.split()[0]}\"",
            f"site:{TIKTOK_HOST}/@ \"original sound\" \"{topic.split()[0]}\"",
        ]
        # Use multiple live search surfaces.  These are discovery pages only;
        # the selected canonical_url is still a concrete TikTok video URL.
        out = [
            jina_url("https://duckduckgo.com/html/?q=" + urllib.parse.quote_plus(f"site:{TIKTOK_HOST}/@ {TIKTOK_VIDEO_PATH} {topic}")),
        ]
        for query in search_queries:
            q = urllib.parse.quote_plus(query)
            out.append("https://search.yahoo.com/search?p=" + q)
            out.append("https://au.search.yahoo.com/search?p=" + q)
        return out
    raise SystemExit(f"unsupported platform: {platform}")


def yt_dlp_cmd(*args: str) -> list[str]:
    uses_cli = bool(shutil.which("yt-dlp"))
    cmd = ["yt-dlp"] if uses_cli else [sys.executable, "-m", "yt_dlp"]
    node_path = "/usr/local/bin/node"
    if uses_cli and Path(node_path).exists():
        cmd += ["--js-runtimes", f"node:{node_path}"]
    cmd += list(args)
    return cmd


def tiktok_oembed_url(url: str) -> str:
    return "https://www.tiktok.com/oembed?url=" + urllib.parse.quote(url, safe="")


def tiktok_video_id(url: str) -> str | None:
    match = re.search(r"/video/(\d+)", url)
    return match.group(1) if match else None


def canonicalize_tiktok_candidate(url: str) -> str:
    """Resolve search-result TikTok candidates into concrete /@user/video/id URLs.

    Search engines sometimes expose only /@/video/<id>.  That is still a live
    discovered video id, but it is not a stable canonical URL.  TikTok oEmbed
    gives the author handle for many such ids without requiring a fixed sample.
    """
    clean = normalize_candidate_url(url)
    if not clean or "tiktok.com" not in urllib.parse.urlsplit(clean).netloc:
        return ""
    video_id = tiktok_video_id(clean)
    if not video_id:
        return ""
    # Already has a non-empty creator segment.
    author_match = re.search(r"/(@[^/\s]+)/video/" + re.escape(video_id), clean)
    if author_match:
        return f"https://www.{TIKTOK_HOST}/{author_match.group(1)}/video/{video_id}"
    clean_for_oembed = f"https://www.{TIKTOK_HOST}/@/video/{video_id}"
    try:
        data = json.loads(fetch_text(tiktok_oembed_url(clean_for_oembed), timeout=20))
    except Exception as exc:
        log(f"tiktok oembed failed for {clean}: {exc}")
        return ""
    author_url = str(data.get("author_url") or "").strip()
    author = urllib.parse.urlsplit(author_url).path.strip("/")
    if author.startswith("@") and len(author) > 1:
        return f"https://www.{TIKTOK_HOST}/{author}/video/{video_id}"
    html_blob = str(data.get("html") or "")
    match = re.search(r"https://www\." + re.escape(TIKTOK_HOST) + r"/(@[^/\s\"<>]+)/video/" + re.escape(video_id), html_blob)
    if match:
        return f"https://www.{TIKTOK_HOST}/{match.group(1)}/video/{video_id}"
    return ""


def extract_play_addr_from_tiktok_page(url: str) -> tuple[str, dict[str, Any]] | None:
    try:
        text = fetch_text(url, timeout=25)
    except Exception as exc:
        log(f"tiktok page fetch failed for {url}: {exc}")
        return None
    play_match = re.search(r'"playAddr":"(https:\\u002F\\u002F[^"]+)"', text)
    if not play_match:
        log(f"tiktok page has no playAddr: {url}")
        return None
    try:
        play_addr = json.loads('"' + play_match.group(1) + '"')
    except Exception:
        return None
    duration = None
    duration_match = re.search(r'"duration":(\d+)', text)
    if duration_match:
        try:
            duration = int(duration_match.group(1))
        except Exception:
            duration = None
    title = ""
    title_match = re.search(r'<title>(.*?)</title>', text, flags=re.S)
    if title_match:
        title = html.unescape(re.sub(r"\s+", " ", title_match.group(1))).strip()
    return play_addr, {"title": title, "duration": duration, "extractor": "tiktok_page_play_addr"}


def verify_video(url: str, platform: str, timeout: int = 90) -> dict[str, Any] | None:
    if platform == "tiktok":
        canonical = canonicalize_tiktok_candidate(url)
        if not canonical:
            return None
        extracted = extract_play_addr_from_tiktok_page(canonical)
        if extracted is None:
            return None
        _play_addr, info = extracted
        return {
            "url": canonical,
            "title": info.get("title"),
            "duration": info.get("duration"),
            "extractor": info.get("extractor"),
        }
    cmd = yt_dlp_cmd("--dump-single-json", "--no-playlist", url)
    log("$ " + " ".join(shlex.quote(p) for p in cmd))
    try:
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
    except Exception as exc:
        log(f"verify exception for {url}: {exc}")
        return None
    if proc.returncode != 0 or not proc.stdout.strip():
        log((proc.stderr or proc.stdout or "verify failed").strip()[-800:])
        return None
    try:
        info = json.loads(proc.stdout)
    except Exception:
        return None
    entries = info.get("entries") if isinstance(info.get("entries"), list) else [info]
    for item in entries:
        if not isinstance(item, dict):
            continue
        formats = item.get("formats")
        duration = item.get("duration")
        if (isinstance(formats, list) and formats) or isinstance(duration, (int, float)):
            resolved_url = item.get("webpage_url") or info.get("webpage_url") or url
            extractor = item.get("extractor") or info.get("extractor")
            if not platform_candidate_match(str(resolved_url), platform):
                log(f"resolved URL platform mismatch for {url}: {resolved_url}")
                return None
            if platform == "x" and "twitter" not in str(extractor).lower():
                log(f"extractor platform mismatch for {url}: {extractor}")
                return None
            return {
                "url": resolved_url,
                "title": item.get("title") or info.get("title"),
                "duration": duration,
                "extractor": extractor,
            }
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Pick random live platform video candidates without fixed fallback URLs.")
    parser.add_argument("--platform", required=True, choices=["youtube_shorts", "x", "xiaohongshu", "tiktok"])
    parser.add_argument("--candidate-count", type=int, default=8)
    parser.add_argument("--verify-limit", type=int, default=12)
    parser.add_argument("--topic", default="")
    args = parser.parse_args()

    rng = random.SystemRandom()
    topics = [args.topic.strip()] if args.topic.strip() else list(PLATFORM_SEARCH_TOPICS.get(args.platform, SEARCH_TOPICS))
    rng.shuffle(topics)

    raw_candidates: list[str] = []
    discovery_used: list[str] = []
    topic_limit = len(topics) if args.platform == "xiaohongshu" else min(len(topics), 6)
    raw_target = max(3, args.candidate_count)
    if args.platform == "xiaohongshu":
        # Xiaohongshu public search results include many notes that look like
        # video shares but expose no downloadable formats.  Keep the source
        # random/live, but search a wider topic surface before declaring a
        # platform-specific failure.
        raw_target = max(24, args.candidate_count * 8)
    for topic in topics[:topic_limit]:
        for url in discovery_urls(args.platform, topic):
            discovery_used.append(url)
            try:
                text = fetch_text(url)
            except Exception as exc:
                log(f"discovery failed {url}: {exc}")
                continue
            raw_candidates.extend(extract_urls_from_text(text, args.platform))
        raw_candidates = dedupe(raw_candidates)
        if len(raw_candidates) >= raw_target:
            break

    rng.shuffle(raw_candidates)
    verified: list[dict[str, Any]] = []
    verify_limit = max(args.verify_limit, args.candidate_count)
    if args.platform == "xiaohongshu":
        verify_limit = max(verify_limit, 50, args.candidate_count * 12)
    for url in raw_candidates[:verify_limit]:
        info = verify_video(url, args.platform)
        if info is not None:
            info["candidate_url"] = url
            verified.append(info)
        if len(verified) >= args.candidate_count:
            break

    if not verified:
        print(json.dumps({
            "ok": False,
            "platform": args.platform,
            "error": "no_verified_live_video_candidate",
            "raw_candidate_count": len(raw_candidates),
            "discovery_used": discovery_used,
        }, ensure_ascii=False, indent=2))
        return 2

    selected_index = rng.randrange(len(verified))
    payload = {
        "ok": True,
        "selection_method": "random_live_pick",
        "required_source_platform": args.platform,
        "candidate_count": len(verified),
        "selected_index": selected_index,
        "canonical_url": verified[selected_index]["url"],
        "candidates": verified,
        "raw_candidate_count": len(raw_candidates),
        "discovery_used": discovery_used,
        "tooling_used": ["r.jina.ai", "duckduckgo/yahoo public discovery", "yt-dlp"],
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
