"""Load YAML/JSON calibration from ``setup/config`` or ``tai_alpha/config``."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from tai_alpha.runtime_paths import find_project_root

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


def _package_config_dir() -> Path:
    return Path(__file__).resolve().parent / "config"


def _setup_config_dir() -> Path:
    return find_project_root() / "setup" / "config"


def _first_existing(*candidates: Path) -> Path | None:
    for p in candidates:
        if p.is_file():
            return p
    return None


@lru_cache(maxsize=1)
def load_score_dimensions() -> dict[str, Any]:
    """
    Load score dimension weights and thresholds.

    Resolution order: ``<repo>/setup/config/score_dimensions.yaml``,
    then ``tai_alpha/config/score_dimensions.yaml``.
    """
    path = _first_existing(
        _setup_config_dir() / "score_dimensions.yaml",
        _package_config_dir() / "score_dimensions.yaml",
    )
    if path is None:
        raise FileNotFoundError(
            "score_dimensions.yaml not found under setup/config or tai_alpha/config"
        )
    text = path.read_text(encoding="utf-8")
    if yaml is None:
        raise RuntimeError("PyYAML is required to load score_dimensions.yaml")
    raw = yaml.safe_load(text)
    if not isinstance(raw, dict):
        raise ValueError("score_dimensions.yaml must parse to a mapping")
    return raw


@lru_cache(maxsize=1)
def load_risk_keywords() -> dict[str, list[str]]:
    """
    Load crisis / geopolitical keyword lists for ``risk_flags`` scanning.
    """
    path = _first_existing(
        _setup_config_dir() / "risk_keywords.json",
        _package_config_dir() / "risk_keywords.json",
    )
    if path is None:
        return {"crisis_keywords": [], "geopolitical_keywords": []}
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {"crisis_keywords": [], "geopolitical_keywords": []}
    out: dict[str, list[str]] = {}
    for key in ("crisis_keywords", "geopolitical_keywords"):
        v = raw.get(key, [])
        out[key] = [str(x) for x in v] if isinstance(v, list) else []
    return out


def clear_config_caches() -> None:
    """Test helper: invalidate memoized config loads."""
    load_score_dimensions.cache_clear()
    load_risk_keywords.cache_clear()
