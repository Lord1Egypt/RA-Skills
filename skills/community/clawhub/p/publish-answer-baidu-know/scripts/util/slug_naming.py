"""技能 slug 语义校验（verb-noun-platform 规范，见 development/NAMING.md）。"""

from __future__ import annotations

import os
import re

_KEBAB_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_MAX_SLUG_LENGTH = 48
_MIN_SEGMENTS = 3
_MAX_SEGMENTS = 5
_MAX_NOUN_SEGMENTS = 3

_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_NAMING_DIR = os.path.join(_SKILL_ROOT, "assets", "naming")

_BUILTIN_VERBS = frozenset(
    {
        "scrape",
        "receive",
        "download",
        "export",
        "add",
        "fill",
        "enter",
        "bind",
        "withdraw",
        "reconcile",
        "verify",
        "submit",
        "publish",
        "query",
        "process",
        "reply",
        "generate",
        "draft",
        "review",
        "confirm",
        "track",
        "upload",
        "match",
        "triage",
        "ship",
        "reprice",
    }
)
_BUILTIN_PLATFORMS = frozenset(
    {
        "amazon",
        "shopee",
        "xinghang",
        "alibaba",
        "kingdee",
        "icbc",
        "pingpong",
        "worldfirst",
        "paypal",
        "lianlian",
        "single-window",
        "export-rebate",
        "etax",
        "baidu-know",
        "baidu-zhidao",
    }
)
_BUILTIN_SCOPES = frozenset({"all", "batch", "multi", "default"})

LEGACY_EXEMPT_SLUGS: frozenset[str] = frozenset(
    {
        "account-manager",
        "skill-template",
        "your-skill-slug",
        "your_skill_slug",
    }
)


def load_wordlist(filename: str) -> frozenset[str]:
    """从 assets/naming/{filename} 加载词表；文件不存在时 fallback 内置集合。"""
    fallbacks = {
        "verbs.txt": _BUILTIN_VERBS,
        "platforms.txt": _BUILTIN_PLATFORMS,
        "scopes.txt": _BUILTIN_SCOPES,
    }
    fallback = fallbacks.get(filename, frozenset())
    path = os.path.join(_NAMING_DIR, filename)
    if not os.path.isfile(path):
        return fallback
    words: set[str] = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word and not word.startswith("#"):
                words.add(word)
    return frozenset(words) if words else fallback


def parse_slug_segments(slug: str) -> list[str]:
    """按 '-' 分割；非法字符由上层 kebab 校验处理。"""
    slug = slug.strip()
    if not slug:
        return []
    return slug.split("-")


def _match_platform_suffix(
    segments: list[str],
    platforms: frozenset[str],
) -> tuple[str, int] | None:
    """返回 (platform_name, platform_part_count) 或 None。"""
    for platform in sorted(platforms, key=lambda item: (-item.count("-"), item)):
        parts = platform.split("-")
        part_count = len(parts)
        if len(segments) < part_count + 2:
            continue
        if segments[-part_count:] == parts:
            return platform, part_count
    return None


def classify_slug_form(segments: list[str], *, slug: str = "") -> str:
    """
    返回: 'legacy_exempt' | 'standard' | 'scope' | 'invalid'

    - legacy_exempt: slug in LEGACY_EXEMPT_SLUGS
    - standard: 末段匹配 platforms, 首段 in verbs, 3<=len<=5
    - scope: 末段 in scopes, 首段 in verbs, 3<=len<=5
    - invalid: 其他
    """
    if slug in LEGACY_EXEMPT_SLUGS:
        return "legacy_exempt"

    if not segments or not (_MIN_SEGMENTS <= len(segments) <= _MAX_SEGMENTS):
        return "invalid"

    verbs = load_wordlist("verbs.txt")
    platforms = load_wordlist("platforms.txt")
    scopes = load_wordlist("scopes.txt")

    if segments[0] not in verbs:
        return "invalid"

    if segments[-1] in scopes:
        return "scope"

    if _match_platform_suffix(segments, platforms) is not None:
        return "standard"

    return "invalid"


def validate_slug_semantics(
    slug: str,
    *,
    strict: bool = True,
) -> tuple[list[str], list[str]]:
    """返回 (errors, warnings)。"""
    slug = slug.strip()
    if slug in LEGACY_EXEMPT_SLUGS:
        return [], []

    errors: list[str] = []
    warnings: list[str] = []

    if not _KEBAB_SLUG.fullmatch(slug):
        msg = f"slug 必须为 kebab-case（小写字母、数字、连字符）：{slug!r}"
        (errors if strict else warnings).append(msg)
        return errors, warnings

    if len(slug) > _MAX_SLUG_LENGTH:
        msg = f"slug 长度不得超过 {_MAX_SLUG_LENGTH} 字符（当前 {len(slug)}）：{slug!r}"
        (errors if strict else warnings).append(msg)

    segments = parse_slug_segments(slug)
    segment_count = len(segments)

    if segment_count < _MIN_SEGMENTS:
        msg = (
            f"slug 段数应为 {_MIN_SEGMENTS}～{_MAX_SEGMENTS}（verb-noun-platform），"
            f"当前为 {segment_count} 段：{slug!r}；新技能禁止 2 段无平台形态（如 reconcile-finance）"
        )
        (errors if strict else warnings).append(msg)
        return errors, warnings

    if segment_count > _MAX_SEGMENTS:
        msg = f"slug 段数不得超过 {_MAX_SEGMENTS}（当前 {segment_count}）：{slug!r}"
        (errors if strict else warnings).append(msg)

    verbs = load_wordlist("verbs.txt")
    platforms = load_wordlist("platforms.txt")
    scopes = load_wordlist("scopes.txt")

    if segments[0] in platforms and segments[0] not in verbs:
        msg = f"平台名不应放在 slug 最前：{slug!r}（应为 verb-noun-platform）"
        (errors if strict else warnings).append(msg)

    if segments[0] not in verbs:
        msg = f"slug 首段应为动词白名单中的词：{segments[0]!r}（slug={slug!r}）"
        (errors if strict else warnings).append(msg)

    form = classify_slug_form(segments, slug=slug)
    if form == "scope":
        if segments[-1] not in scopes:
            msg = f"slug 末段应为 scope 白名单中的词：{segments[-1]!r}（slug={slug!r}）"
            (errors if strict else warnings).append(msg)
        noun_count = segment_count - 2
    elif form == "standard":
        platform_match = _match_platform_suffix(segments, platforms)
        if platform_match is None:
            msg = f"slug 末段应匹配平台白名单：{slug!r}"
            (errors if strict else warnings).append(msg)
            noun_count = 0
        else:
            _platform_name, platform_part_count = platform_match
            noun_count = segment_count - 1 - platform_part_count
    else:
        if segment_count >= _MIN_SEGMENTS:
            if segments[-1] not in scopes:
                platform_match = _match_platform_suffix(segments, platforms)
                if platform_match is None:
                    msg = f"slug 末段应匹配平台或 scope 白名单：{slug!r}"
                    (errors if strict else warnings).append(msg)
        noun_count = 0

    if noun_count > _MAX_NOUN_SEGMENTS:
        warnings.append(
            f"slug 中间名词段建议不超过 {_MAX_NOUN_SEGMENTS} 个词（当前 {noun_count}）：{slug!r}"
        )

    return errors, warnings
