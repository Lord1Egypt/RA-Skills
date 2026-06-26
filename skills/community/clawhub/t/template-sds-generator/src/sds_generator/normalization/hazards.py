from __future__ import annotations

from functools import lru_cache

from sds_generator.config_loader import load_ghs_codes

from .text import normalize_text, split_list_text


@lru_cache(maxsize=1)
def _ghs_codes() -> dict[str, dict[str, str]]:
    return load_ghs_codes()


def normalize_signal_word(value: str | None) -> str | None:
    cleaned = normalize_text(value or "")
    if cleaned.casefold() == "warning":
        return "Warning"
    if cleaned.casefold() == "danger":
        return "Danger"
    return cleaned or None


def normalize_hazard_statements(values: str | list[str] | None) -> list[str]:
    return split_list_text(values, delimiters=r"[;\n]")


def expand_hazard_code(code: str) -> str | None:
    code = normalize_text(code).upper()
    return _ghs_codes().get("hazard_statements", {}).get(code)


def expand_precautionary_code(code: str) -> str | None:
    code = normalize_text(code).upper()
    return _ghs_codes().get("precautionary_statements", {}).get(code)


def normalize_pictograms(values: str | list[str] | None) -> list[str]:
    normalized = []
    for value in split_list_text(values):
        cleaned = normalize_text(value).upper()
        if cleaned in _ghs_codes().get("pictograms", {}):
            normalized.append(cleaned)
            continue
        for code, description in _ghs_codes().get("pictograms", {}).items():
            if cleaned == description.upper():
                normalized.append(code)
                break
    return normalized
