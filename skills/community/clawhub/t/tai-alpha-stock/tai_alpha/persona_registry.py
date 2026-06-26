"""Load and validate persona YAML from setup/config/personas (bundled fallback)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from tai_alpha.runtime_paths import find_project_root

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


def _personas_dir() -> Path:
    root = find_project_root()
    p = root / "setup" / "config" / "personas"
    if p.is_dir():
        return p
    return Path(__file__).resolve().parent / "config" / "personas"


def _load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required for persona configs")
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Invalid YAML (not a mapping): {path}")
    return raw


@lru_cache(maxsize=1)
def load_persona_registry() -> dict[str, Any]:
    """Load ``PERSONA_REGISTRY.yaml``."""
    base = _personas_dir() / "PERSONA_REGISTRY.yaml"
    if not base.is_file():
        raise FileNotFoundError(f"Missing {base}")
    return _load_yaml(base)


def list_persona_ids(enabled_only: bool = True) -> list[str]:
    """Return persona ids from registry."""
    reg = load_persona_registry()
    out: list[str] = []
    for row in reg.get("personas", []):
        if not isinstance(row, dict):
            continue
        pid = row.get("id")
        if not pid:
            continue
        fn = row.get("file")
        if fn:
            data = load_persona_by_id(str(pid))
            if enabled_only and not data.get("enabled", True):
                continue
        out.append(str(pid))
    return out


@lru_cache(maxsize=32)
def load_persona_by_id(persona_id: str) -> dict[str, Any]:
    """Load one persona file and validate minimal schema."""
    reg = load_persona_registry()
    pid = persona_id.strip().lower()
    target_file: str | None = None
    for row in reg.get("personas", []):
        if isinstance(row, dict) and str(row.get("id", "")).lower() == pid:
            target_file = str(row.get("file", ""))
            break
    if not target_file:
        raise KeyError(f"Unknown persona id: {persona_id}")
    path = _personas_dir() / target_file
    if not path.is_file():
        raise FileNotFoundError(f"Persona file missing: {path}")
    data = _load_yaml(path)
    if str(data.get("id", "")).lower() != pid:
        raise ValueError(f"Persona id mismatch in {path}")
    if "overlay" not in data:
        data["overlay"] = {}
    return data


def clear_persona_cache() -> None:
    """Test helper."""
    load_persona_registry.cache_clear()
    load_persona_by_id.cache_clear()


def validate_persona_config(data: dict[str, Any]) -> list[str]:
    """Return list of validation errors (empty if ok)."""
    errors: list[str] = []
    if not data.get("id"):
        errors.append("missing id")
    ov = data.get("overlay", {})
    if not isinstance(ov, dict):
        errors.append("overlay must be a mapping")
        return errors
    for key in ("conviction_scale", "conviction_bias"):
        if key in ov:
            try:
                float(ov[key]) if key == "conviction_scale" else int(ov[key])
            except (TypeError, ValueError):
                errors.append(f"invalid {key}")
    return errors
