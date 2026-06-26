from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from sds_generator.models.common import SourceProfileName
from sds_generator.models.template_contract import TemplateContract
from sds_generator.models.source import SourceProfile


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_ROOT = PROJECT_ROOT / "config"


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise TypeError(f"Expected a mapping in {path}")
    return payload


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise TypeError(f"Expected a mapping in {path}")
    return payload


@lru_cache(maxsize=1)
def load_defaults() -> dict[str, Any]:
    return _load_yaml(CONFIG_ROOT / "defaults.yml")


@lru_cache(maxsize=1)
def load_template_contract() -> TemplateContract:
    return TemplateContract.model_validate(_load_yaml(CONFIG_ROOT / "template_contract.yml"))


@lru_cache(maxsize=1)
def load_business_rules() -> dict[str, Any]:
    return _load_yaml(CONFIG_ROOT / "business_rules.yml")


@lru_cache(maxsize=1)
def load_field_registry() -> dict[str, Any]:
    return _load_yaml(CONFIG_ROOT / "field_registry.yml")


@lru_cache(maxsize=1)
def load_content_policy() -> dict[str, Any]:
    return _load_yaml(CONFIG_ROOT / "content_policy.yml")


@lru_cache(maxsize=1)
def load_fixed_company() -> dict[str, str]:
    data = _load_yaml(CONFIG_ROOT / "fixed_company.yml")
    return {str(key): str(value) for key, value in data.items()}


@lru_cache(maxsize=1)
def load_section_aliases() -> dict[int, list[str]]:
    raw = _load_yaml(CONFIG_ROOT / "section_aliases.yml")
    return {int(key): [str(item) for item in value] for key, value in raw.items()}


@lru_cache(maxsize=1)
def load_field_aliases() -> dict[str, list[str]]:
    raw = _load_yaml(CONFIG_ROOT / "field_aliases.yml")
    return {str(key): [str(item) for item in value] for key, value in raw.items()}


@lru_cache(maxsize=1)
def load_reconciliation_policy() -> dict[str, Any]:
    return _load_yaml(CONFIG_ROOT / "reconciliation.yml")


def _coerce_source_profile_name(value: str) -> SourceProfileName:
    try:
        return SourceProfileName(value)
    except ValueError:
        return SourceProfileName.UNCLASSIFIED


@lru_cache(maxsize=1)
def load_source_profiles() -> list[SourceProfile]:
    raw = _load_yaml(CONFIG_ROOT / "source_profiles.yml")
    profiles: list[SourceProfile] = []
    for profile in raw.get("profiles", []):
        profiles.append(
            SourceProfile(
                name=_coerce_source_profile_name(str(profile.get("name", "unclassified"))),
                authority=int(profile.get("authority", 0)),
                description=str(profile.get("label")) if profile.get("label") else None,
            )
        )
    return profiles


@lru_cache(maxsize=1)
def load_units() -> dict[str, Any]:
    return _load_yaml(CONFIG_ROOT / "units.yml")


@lru_cache(maxsize=1)
def load_ghs_codes() -> dict[str, Any]:
    return _load_json(CONFIG_ROOT / "ghs_codes.json")


def resolve_source_profile(file_path: str | Path, hint_text: str = "") -> SourceProfile:
    path = Path(file_path)
    haystacks = [path.name.lower(), hint_text.lower()]
    raw_profiles = _load_yaml(CONFIG_ROOT / "source_profiles.yml").get("profiles", [])
    default_profile = SourceProfile(
        name=SourceProfileName.UNCLASSIFIED,
        authority=0,
        description="Unclassified source",
    )
    for profile, raw_profile in zip(load_source_profiles(), raw_profiles, strict=False):
        needles = [str(item).lower() for item in raw_profile.get("match_any", [])]
        if any(needle in haystack for haystack in haystacks for needle in needles):
            return profile
    return default_profile
