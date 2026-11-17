#!/usr/bin/env python3
"""Which language the intake pages speak -- decided once, here, for every script that asks.

The profile collects `identity_and_language.preferred_response_language`, and until 2026-09-24
nothing downstream read it: the trip form received it and dropped it, 0 of 15 real intakes carried
it, and every page was Chinese. The order of sources is the spec's (decision 2): an explicit
`--language`, else the saved profile's preferred output language, else Chinese.

The profile stores the traveller's own words for that preference ("中文", "English",
"中文和 English", "其他"), so they are normalised here rather than compared anywhere else. A
bilingual or unrecognised answer names no single page language and resolves to the next source.

Two additions from a generality pass on 2026-09-24. A profile written in chat, by whichever
assistant, says "en_US", "English (UK)" or "Simplified Chinese" rather than the dropdown's words,
and each of those fell through to Chinese; locale tags and language names are now read too. And a
traveller who switched the profile page to English but left the preference blank -- or chose
"other" -- had every trip form open in Chinese, although the page they used was the answer; the
profile now records `identity_and_language.profile_form_language`, consulted after the preference.
"""

from __future__ import annotations

import re

LANGUAGES = ("zh", "en")
# Both forms send their CURRENT language with every submission (it follows the page's switch), so
# a server answers in the language on screen and the intake records the one actually used.
LANGUAGE_HEADER = "X-Travel-Buddy-Language"

_ALIASES = {
    "en": "en", "english": "en", "英文": "en", "英语": "en", "en-us": "en", "en-gb": "en",
    "zh": "zh", "chinese": "zh", "中文": "zh", "汉语": "zh", "简体中文": "zh", "zh-cn": "zh",
    "zh-hans": "zh",
}


_TAG = re.compile(r"^(en|zh)(?:[-_][a-z0-9]+)*$")
_BILINGUAL = re.compile(r"中英|英中|双语|雙語|bilingual")
_NAMES = {
    "en": ("english", "英文", "英语", "英語"),
    "zh": ("chinese", "mandarin", "cantonese", "中文", "汉语", "漢語", "华语", "華語", "普通话",
           "普通話", "国语", "國語", "粤语", "粵語", "广东话", "廣東話"),
}


def normalize_language(value: object) -> str | None:
    """"English"/"en_US"/"英文" -> "en"; "中文"/"zh-TW"/"Simplified Chinese" -> "zh"; a bilingual
    answer or any other language -> None."""
    if not isinstance(value, str):
        return None
    text = value.strip().lower()
    if not text:
        return None
    if text in _ALIASES:
        return _ALIASES[text]
    if match := _TAG.match(text):
        return match.group(1)
    # Bilingual in one word: 英文 sits inside 中英文, which read as English.
    if _BILINGUAL.search(text):
        return None
    named = [code for code, names in _NAMES.items() if any(name in text for name in names)]
    return named[0] if len(named) == 1 else None


def resolve_form_language(cli: str | None, profile: dict | None) -> str:
    """The page language: the flag, else the profile's preference, else the language the profile
    itself was filled in, else Chinese."""
    chosen = normalize_language(cli)
    if chosen:
        return chosen
    identity = profile.get("identity_and_language") if isinstance(profile, dict) else None
    if isinstance(identity, dict):
        for field in ("preferred_response_language", "profile_form_language"):
            found = normalize_language(identity.get(field))
            if found:
                return found
    return "zh"


def pick(lang: str, zh: str, en: str) -> str:
    """The message in `lang`. An unknown language is a caller bug, so it raises instead of
    quietly answering in Chinese."""
    if lang not in LANGUAGES:
        raise ValueError(f"unknown intake language {lang!r}; expected one of {LANGUAGES}")
    return en if lang == "en" else zh
