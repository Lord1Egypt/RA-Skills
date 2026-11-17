"""Baseline loading and metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .manifest import Manifest, load_manifest, save_manifest


class BaselineError(RuntimeError):
    pass


def load_baseline(path: str | Path) -> Manifest:
    candidate = Path(path).expanduser().resolve()
    if not candidate.is_file():
        raise BaselineError(f"baseline manifest not found: {candidate}")
    try:
        return load_manifest(candidate)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise BaselineError(f"cannot read baseline manifest {candidate}: {exc}") from exc


def baseline_info(path: str | Path, manifest: Manifest) -> dict[str, Any]:
    candidate = Path(path).expanduser().resolve()
    return {
        "source": "manifest",
        "path": str(candidate),
        "generated_at": manifest.generated_at,
        "manifest_sha256": manifest.manifest_sha256,
        "file_count": manifest.file_count,
    }


def write_baseline(path: str | Path, manifest: Manifest) -> Path:
    candidate = Path(path).expanduser().resolve()
    save_manifest(manifest, candidate)
    return candidate
