"""Load science and game-content JSON relative to the repository root."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
I18N = ROOT / "i18n"


def _load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def science() -> dict:
    return _load(DATA / "science.json")


@lru_cache(maxsize=1)
def references() -> dict:
    return _load(DATA / "references.json")


@lru_cache(maxsize=1)
def tech_tree() -> dict:
    return _load(DATA / "tech_tree.json")


@lru_cache(maxsize=1)
def factions() -> dict:
    return _load(DATA / "factions.json")


@lru_cache(maxsize=1)
def advisors() -> dict:
    return _load(DATA / "advisors.json")


@lru_cache(maxsize=1)
def organisms() -> dict:
    return _load(DATA / "organisms.json")


@lru_cache(maxsize=1)
def events() -> dict:
    return _load(DATA / "events.json")


@lru_cache(maxsize=None)
def i18n(language: str) -> dict:
    code = "zh" if language.startswith("zh") else "en"
    return _load(I18N / f"{code}.json")


def value(node: dict) -> float:
    """Return the numeric value of a science leaf {"value": ...}."""
    if not isinstance(node, dict) or "value" not in node:
        raise KeyError(f"not a science leaf: {node!r}")
    return node["value"]


def meta(node: dict) -> dict:
    return {
        "value": node["value"],
        "estimate": bool(node.get("estimate", False)),
        "source_id": node.get("source_id"),
        "unit": node.get("unit"),
        "note": node.get("note"),
        "uncertainty": node.get("uncertainty"),
    }


def sci(*path: str) -> dict:
    node: object = science()
    for part in path:
        if not isinstance(node, dict) or part not in node:
            raise KeyError(".".join(path))
        node = node[part]
    if not isinstance(node, dict):
        raise KeyError(".".join(path))
    return node


def V(*path: str) -> float:
    return float(value(sci(*path)))
