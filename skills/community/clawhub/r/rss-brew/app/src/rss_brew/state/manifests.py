from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    tmp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp_path, path)


def update_manifest(manifest_path: Path, mutate: Dict[str, Any]) -> Dict[str, Any]:
    current = read_json(manifest_path, {})
    if not isinstance(current, dict):
        current = {}
    current.update(mutate)
    write_json(manifest_path, current)
    return current


def list_committed_manifests(day_dir: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    if not day_dir.exists():
        return rows
    for p in sorted(day_dir.glob("*.json")):
        if p.name == "CURRENT.json":
            continue
        data = read_json(p, {})
        if not isinstance(data, dict):
            continue
        if data.get("status") == "committed":
            data["_path"] = str(p)
            rows.append(data)
    return rows
