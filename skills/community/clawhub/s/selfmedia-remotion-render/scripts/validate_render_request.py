#!/usr/bin/env python3
"""Read-only validation of an explicit Remotion render request."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


class RequestError(ValueError):
    pass


def load_request(path: Path) -> tuple[dict[str, Any], Path]:
    try:
        request = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RequestError(f"cannot read render request: {exc}") from exc
    if not isinstance(request, dict):
        raise RequestError("render request must be a JSON object")
    workspace_raw = request.get("workspace")
    if not isinstance(workspace_raw, str) or not workspace_raw.strip():
        raise RequestError("workspace must be a non-empty path")
    request_dir = path.resolve().parent
    workspace_candidate = Path(workspace_raw)
    workspace = (request_dir / workspace_candidate).resolve() if not workspace_candidate.is_absolute() else workspace_candidate.resolve()
    if not workspace.is_dir():
        raise RequestError(f"workspace directory does not exist: {workspace}")

    entry = _relative_path(request.get("entry_point"), "entry_point")
    output = _relative_path(request.get("output_path"), "output_path")
    for field in ("composition_id", "codec"):
        _nonempty_string(request.get(field), field)
    for field in ("width", "height", "fps"):
        value = request.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
            raise RequestError(f"{field} must be a positive number")
    if not isinstance(request.get("input_files"), list) or not request["input_files"]:
        raise RequestError("input_files must be a non-empty list")
    inputs = [_relative_path(value, f"input_files[{i}]") for i, value in enumerate(request["input_files"])]

    package_json = workspace / "package.json"
    if not package_json.is_file():
        raise RequestError("workspace must include package.json with its existing Remotion project dependencies")
    try:
        package = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RequestError(f"invalid package.json: {exc}") from exc
    dependencies = {}
    for key in ("dependencies", "devDependencies", "optionalDependencies"):
        value = package.get(key, {}) if isinstance(package, dict) else {}
        if isinstance(value, dict):
            dependencies.update(value)
    if "remotion" not in dependencies:
        raise RequestError("package.json must declare the remotion dependency")

    entry_path = _resolve_inside(workspace, entry, "entry_point")
    if not entry_path.is_file():
        raise RequestError(f"entry_point does not exist: {entry}")
    for i, relative in enumerate(inputs):
        if not _resolve_inside(workspace, relative, f"input_files[{i}]").is_file():
            raise RequestError(f"input file does not exist: {relative}")
    output_path = _resolve_inside(workspace, output, "output_path")
    if output_path.exists():
        raise RequestError(f"output already exists; choose a new path to prevent overwrite: {output}")
    if not output_path.parent.is_dir():
        raise RequestError(f"output directory does not exist: {output.parent}")
    return request, workspace


def _nonempty_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RequestError(f"{name} must be a non-empty string")
    return value.strip()


def _relative_path(value: Any, name: str) -> Path:
    raw = _nonempty_string(value, name)
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts or "\\" in raw:
        raise RequestError(f"{name} must be a relative path inside the workspace")
    return path


def _resolve_inside(workspace: Path, relative: Path, name: str) -> Path:
    candidate = (workspace / relative).resolve()
    try:
        candidate.relative_to(workspace)
    except ValueError as exc:
        raise RequestError(f"{name} resolves outside the workspace") from exc
    return candidate


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_render_request.py REQUEST.json", file=sys.stderr)
        return 2
    try:
        request, workspace = load_request(Path(argv[1]))
    except RequestError as exc:
        print(f"invalid: {exc}", file=sys.stderr)
        return 1
    print("valid request (no render executed)")
    print(f"workspace={workspace}")
    print(f"composition={request['composition_id']} {request['width']}x{request['height']}@{request['fps']} codec={request['codec']}")
    print(f"output={request['output_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
