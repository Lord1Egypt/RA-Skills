#!/usr/bin/env python3
"""
preloaded_data.py
~~~~~~~~~~~~~~~~~
预加载所有 reference JSON 文件为内存常量，避免每次 import 重新读文件。

导出
----
CATEGORIES            : dict[str, dict]  — dictCode → 条目
CATEGORIES_BY_EXTATTR : dict[str, list[dict]]  — extAttrs(英文名) → 同名条目列表
REGIONS               : dict[str, dict]  — dictCode → 条目
LANGUAGES             : dict[str, dict]  — dictCode → 条目
LANGUAGE_ALIASES      : dict[str, str]   — 别名(如"简体中文") → dictCode
REGION_ALIASES        : dict[str, str]   — 别名(如"美国") → dictCode
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_CAT_JSON = ROOT / "references" / "category-source.json"
_REG_JSON = ROOT / "references" / "region-source.json"
_LANG_JSON = ROOT / "references" / "language-source.json"


# ── helpers ──────────────────────────────────────────────────────────────────

def _normalize_alias(text: str) -> str:
    return re.sub(r"[\s（）()\-_/]+", "", (text or "").strip().lower())


def _load_json(path: Path) -> list[dict]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []


# ── CATEGORIES ───────────────────────────────────────────────────────────────

_RAW_CATEGORIES: list[dict] = _load_json(_CAT_JSON)

CATEGORIES: dict[str, dict] = {item["dictCode"]: item for item in _RAW_CATEGORIES}

# extAttrs (英文名) → 同名条目列表（可能有重名）
CATEGORIES_BY_EXTATTR: dict[str, list[dict]] = {}
for item in _RAW_CATEGORIES:
    en = (item.get("extAttrs") or "").strip()
    if en:
        CATEGORIES_BY_EXTATTR.setdefault(en, []).append(item)
        CATEGORIES_BY_EXTATTR.setdefault(en.lower(), []).append(item)


# ── REGIONS ──────────────────────────────────────────────────────────────────

_RAW_REGIONS: list[dict] = _load_json(_REG_JSON)

REGIONS: dict[str, dict] = {item["dictCode"]: item for item in _RAW_REGIONS}

REGION_ALIASES: dict[str, str] = {}

for item in _RAW_REGIONS:
    code = (item.get("dictCode") or "").lower()
    zh = (item.get("dictValue") or "").strip()
    en = (item.get("extAttrs") or "").strip()
    if code:
        REGION_ALIASES[code] = code
    for alias in {zh, en, _normalize_alias(zh), _normalize_alias(en)}:
        if alias:
            REGION_ALIASES[alias] = code

# 常用硬编码别名兜底
_EXTRA_REGION_ALIASES: dict[str, str] = {
    "美国": "us", "us": "us", "united states": "us", "america": "us",
    "英国": "gb", "uk": "gb", "united kingdom": "gb",
    "德国": "de", "germany": "de",
    "法国": "fr", "france": "fr",
    "加拿大": "ca", "canada": "ca",
    "日本": "jp", "japan": "jp",
    "韩国": "kr", "korea": "kr",
    "澳大利亚": "au", "australia": "au",
    "美国站": "us",
}
REGION_ALIASES.update(_EXTRA_REGION_ALIASES)


# ── LANGUAGES ────────────────────────────────────────────────────────────────

_RAW_LANGUAGES: list[dict] = _load_json(_LANG_JSON)

LANGUAGES: dict[str, dict] = {item["dictCode"]: item for item in _RAW_LANGUAGES}

LANGUAGE_ALIASES: dict[str, str] = {}

for item in _RAW_LANGUAGES:
    code = (item.get("dictCode") or "").lower()
    zh = (item.get("dictValue") or "").strip()
    en = (item.get("extAttrs") or "").strip()
    if code:
        LANGUAGE_ALIASES[code] = code
    for alias in {zh, en, _normalize_alias(zh), _normalize_alias(en)}:
        if alias:
            LANGUAGE_ALIASES[alias] = code

_EXTRA_LANG_ALIASES: dict[str, str] = {
    "英语": "en", "english": "en",
    "简体中文": "zh-cn", "简中": "zh-cn",
    "繁体中文": "zh-tw", "繁中": "zh-tw",
    "西班牙语": "es", "spanish": "es",
    "日语": "ja", "jp": "ja",
    "韩语": "ko", "kr": "ko",
    "菲律宾语": "tl", "filipino": "tl", "tagalog": "tl",
    "法语": "fr", "french": "fr",
    "德语": "de", "german": "de",
    "葡萄牙语": "pt", "portuguese": "pt",
}
LANGUAGE_ALIASES.update(_EXTRA_LANG_ALIASES)
