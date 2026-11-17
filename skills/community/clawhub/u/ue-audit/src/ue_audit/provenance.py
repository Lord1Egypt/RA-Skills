"""Task-manifest parsing and simple change provenance classification."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .checks.base import game_path_to_content_rel, normalize_game_path
from .report.model import Provenance


TOOLCHAIN_PREFIXES = (
    "Saved/",
    "Intermediate/",
    "Binaries/",
    "DerivedDataCache/",
    "Content/Python/",
    ".git/",
)


def load_task_manifest(path: str | Path) -> dict[str, Any]:
    candidate = Path(path).expanduser().resolve()
    data = json.loads(candidate.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{candidate} is not a task manifest object")
    return data


def _normalize_expected_path(raw: str) -> list[str]:
    value = normalize_game_path(str(raw or "").strip())
    if not value:
        return []
    if value.startswith("/Game/"):
        return game_path_to_content_rel(value)
    if value.startswith("Content/"):
        if Path(value).suffix:
            return [value]
        return [value + ".uasset", value + ".umap"]
    return [value]


def expected_paths_from_task(task: dict[str, Any]) -> set[str]:
    raw_values: list[str] = []
    for key in ("expected_write_set", "allowed_assets", "allowed_write_set", "write_set"):
        value = task.get(key)
        if isinstance(value, list):
            raw_values.extend(str(item) for item in value)
    for step in task.get("steps") or []:
        if not isinstance(step, dict):
            continue
        asset = step.get("asset")
        if asset:
            raw_values.append(str(asset))
        save = step.get("save")
        if isinstance(save, list):
            raw_values.extend(str(item) for item in save)
        target = step.get("target")
        if isinstance(target, dict) and target.get("package"):
            raw_values.append(str(target["package"]))
    paths: set[str] = set()
    for raw in raw_values:
        for normalized in _normalize_expected_path(raw):
            paths.add(normalized.casefold())
    return paths


def classify_path(path: str, expected_paths: set[str]) -> Provenance:
    normalized = str(path or "").replace("\\", "/")
    if normalized.casefold() in expected_paths:
        return Provenance.AI
    if any(normalized.startswith(prefix) for prefix in TOOLCHAIN_PREFIXES):
        return Provenance.TOOLCHAIN
    return Provenance.UNKNOWN


def classify_diff(diff: dict[str, Any], expected_paths: set[str]) -> dict[str, Any]:
    annotated: dict[str, list[dict[str, Any]]] = {}
    for bucket in ("added", "removed", "changed"):
        annotated[bucket] = []
        for item in diff.get(bucket, []):
            path = str(item.get("path") or "")
            copy = dict(item)
            copy["provenance"] = classify_path(path, expected_paths).value
            annotated[bucket].append(copy)
    return annotated
