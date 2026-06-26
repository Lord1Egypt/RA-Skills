"""Locale-aware labels for reports (en / zh-CN / zh-HK)."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from tai_alpha.runtime_paths import find_project_root


def _glossary_path() -> Path:
    p = find_project_root() / "setup" / "config" / "i18n_glossary_zh.json"
    if p.is_file():
        return p
    return Path(__file__).resolve().parent / "config" / "i18n_glossary_zh.json"


@lru_cache(maxsize=1)
def load_glossary() -> dict[str, Any]:
    path = _glossary_path()
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def signal_label(signal: str, lang: str) -> str:
    """Translate signal for zh locales; passthrough for English."""
    if not lang.startswith("zh"):
        return signal
    g = load_glossary().get("signal", {})
    row = g.get(signal, {})
    return str(row.get(lang, signal))


def disclaimer_short(lang: str) -> str:
    if not lang.startswith("zh"):
        return "Informational only; not investment advice."
    labels = load_glossary().get("labels", {})
    d = labels.get("disclaimer", {})
    return str(d.get(lang, d.get("zh-CN", "")))


def clear_glossary_cache() -> None:
    load_glossary.cache_clear()
