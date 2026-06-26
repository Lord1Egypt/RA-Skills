from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse

PLATFORM_URL_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("bilibili", re.compile(r"space\.bilibili\.com/(\d+)")),
    ("bilibili", re.compile(r"bilibili\.com/space/(\d+)")),
    ("youtube", re.compile(r"youtube\.com/(?:@|channel/|c/)([^/?&]+)")),
    ("douyin", re.compile(r"douyin\.com/user/([A-Za-z0-9_-]+)")),
    ("kuaishou", re.compile(r"kuaishou\.com/profile/([A-Za-z0-9_-]+)")),
    ("xiaohongshu", re.compile(r"xiaohongshu\.com/user/profile/([A-Za-z0-9]+)")),
    ("tiktok", re.compile(r"tiktok\.com/@([^/?&]+)")),
    ("instagram", re.compile(r"instagram\.com/([^/?&]+)")),
    ("toutiao", re.compile(r"toutiao\.com/c/user/token/([^/?&]+)")),
    ("baijiahao", re.compile(r"baijiahao\.baidu\.com/u\?app_id=(\d+)")),
    ("baijiahao", re.compile(r"author\.baidu\.com/home/(\d+)")),
    ("haokan", re.compile(r"haokan\.baidu\.com/author/(\d+)")),
    ("iqiyi", re.compile(r"iqiyi\.com/u/(\w+)")),
    ("iqiyi", re.compile(r"iqiyi\.com/creator/(\d+)")),
    ("wechat_video", re.compile(r"channels\.weixin\.qq\.com/([^/?&]+)")),
]


@dataclass
class ResolvedInput:
    platform: str
    uid: str | None = None
    url: str | None = None
    nickname: str | None = None


def resolve_input(input_str: str, platform_hint: str | None = None) -> ResolvedInput:
    """Resolve user input (URL or nickname) into a platform + identifier."""
    input_str = input_str.strip()

    if input_str.startswith("http://") or input_str.startswith("https://"):
        return _resolve_url(input_str)

    if "." in input_str and "/" in input_str:
        return _resolve_url("https://" + input_str)

    if platform_hint:
        return ResolvedInput(
            platform=platform_hint.lower().replace(" ", "_"),
            nickname=input_str,
        )

    raise ValueError(
        f"Cannot determine platform from input '{input_str}'. "
        "Please provide a URL or specify the platform name."
    )


def _resolve_url(url: str) -> ResolvedInput:
    for platform, pattern in PLATFORM_URL_PATTERNS:
        m = pattern.search(url)
        if m:
            return ResolvedInput(platform=platform, uid=m.group(1), url=url)

    parsed = urlparse(url)
    raise ValueError(
        f"Unsupported platform URL: {parsed.netloc}. "
        f"Supported platforms: bilibili, youtube, douyin, kuaishou, "
        f"xiaohongshu, tiktok, instagram, toutiao, baijiahao, haokan, iqiyi, wechat_video"
    )
