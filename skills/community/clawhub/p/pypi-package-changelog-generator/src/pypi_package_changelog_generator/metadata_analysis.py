from __future__ import annotations

import ast
import configparser
import re
import tomllib
from dataclasses import dataclass, field
from email.parser import Parser
from pathlib import Path
from typing import Any

from packaging.requirements import InvalidRequirement, Requirement
from packaging.version import InvalidVersion, Version


@dataclass(slots=True)
class ParsedProjectMetadata:
    source: str | None = None
    dependencies: dict[str, str] = field(default_factory=dict)
    requires_python: str | None = None
    license: str | None = None
    classifiers: list[str] = field(default_factory=list)


def analyze_metadata(
    from_release: dict[str, Any],
    to_release: dict[str, Any],
    *,
    from_root: Path | None,
    to_root: Path | None,
    file_changes: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    from_source = (
        parse_project_metadata(from_root) if from_root else ParsedProjectMetadata()
    )
    to_source = parse_project_metadata(to_root) if to_root else ParsedProjectMetadata()

    metadata_changes: list[dict[str, Any]] = []
    dependency_changes = compare_dependencies(
        from_source.dependencies, to_source.dependencies
    )
    breaking_signals: list[dict[str, Any]] = []

    _append_change(
        metadata_changes,
        field="requires_python",
        before=(from_release.get("info", {}) or {}).get("requires_python"),
        after=(to_release.get("info", {}) or {}).get("requires_python"),
        source="pypi",
    )
    _append_change(
        metadata_changes,
        field="license",
        before=(from_release.get("info", {}) or {}).get("license"),
        after=(to_release.get("info", {}) or {}).get("license"),
        source="pypi",
    )
    _append_change(
        metadata_changes,
        field="requires_python",
        before=from_source.requires_python,
        after=to_source.requires_python,
        source=to_source.source or from_source.source,
    )
    _append_change(
        metadata_changes,
        field="license",
        before=from_source.license,
        after=to_source.license,
        source=to_source.source or from_source.source,
    )

    if from_source.classifiers != to_source.classifiers:
        metadata_changes.append(
            {
                "field": "classifiers",
                "before": from_source.classifiers,
                "after": to_source.classifiers,
                "source": to_source.source or from_source.source,
            }
        )

    python_floor_change = compare_python_floor(
        from_source.requires_python, to_source.requires_python
    )
    if python_floor_change:
        breaking_signals.append(python_floor_change)

    removed_runtime = [
        change for change in dependency_changes if change["kind"] == "removed"
    ]
    if removed_runtime:
        breaking_signals.append(
            {
                "kind": "dependency_removed",
                "severity": "medium",
                "message": "Runtime dependencies were removed.",
                "evidence": [change["name"] for change in removed_runtime],
            }
        )

    public_module_removals = []
    for change in file_changes:
        status = change.get("status")
        path = change.get("path")
        previous_path = change.get("previous_path")
        if status == "removed" and _looks_public_python_module(path):
            public_module_removals.append(path)
            continue
        if status != "renamed":
            continue
        old_module = _module_qualname(previous_path)
        new_module = _module_qualname(path)
        if old_module and new_module and old_module != new_module:
            public_module_removals.append(path)
    if public_module_removals:
        breaking_signals.append(
            {
                "kind": "public_module_removed",
                "severity": "high",
                "message": "Public Python modules were removed or renamed.",
                "evidence": public_module_removals,
            }
        )

    return {
        "metadata_changes": metadata_changes,
        "dependency_changes": dependency_changes,
        "breaking_signals": breaking_signals,
    }


def parse_project_metadata(root: Path | None) -> ParsedProjectMetadata:
    if root is None:
        return ParsedProjectMetadata()

    candidates = [
        ("pyproject.toml", _parse_pyproject),
        ("setup.cfg", _parse_setup_cfg),
        ("setup.py", _parse_setup_py),
        ("PKG-INFO", _parse_pkg_info),
    ]
    for filename, parser in candidates:
        target = _find_shallowest(root, filename)
        if target:
            metadata = parser(target)
            metadata.source = str(target.relative_to(root))
            return metadata
    return ParsedProjectMetadata()


def compare_dependencies(
    before: dict[str, str], after: dict[str, str]
) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    before_keys = set(before)
    after_keys = set(after)
    for name in sorted(before_keys - after_keys):
        changes.append(
            {"kind": "removed", "name": name, "before": before[name], "after": None}
        )
    for name in sorted(after_keys - before_keys):
        changes.append(
            {"kind": "added", "name": name, "before": None, "after": after[name]}
        )
    for name in sorted(before_keys & after_keys):
        if before[name] == after[name]:
            continue
        changes.append(
            {
                "kind": "changed",
                "name": name,
                "before": before[name],
                "after": after[name],
            }
        )
    return changes


def compare_python_floor(
    before: str | None, after: str | None
) -> dict[str, Any] | None:
    before_floor = _extract_min_python(before)
    after_floor = _extract_min_python(after)
    if before_floor is None or after_floor is None or after_floor <= before_floor:
        return None
    return {
        "kind": "python_floor_raised",
        "severity": "high",
        "message": f"Python requirement increased from {before_floor} to {after_floor}.",
        "evidence": {"before": before, "after": after},
    }


def _parse_pyproject(path: Path) -> ParsedProjectMetadata:
    payload = tomllib.loads(path.read_text(encoding="utf-8"))
    project = payload.get("project", {})
    dependencies = {
        dep_name: dep_value
        for dep_name, dep_value in _normalize_dependencies(
            project.get("dependencies", [])
        )
    }
    for extra, values in (project.get("optional-dependencies", {}) or {}).items():
        for dep_name, dep_value in _normalize_dependencies(values):
            dependencies[f"extra:{extra}:{dep_name}"] = dep_value
    license_value = project.get("license")
    if isinstance(license_value, dict):
        license_value = license_value.get("text") or license_value.get("file")
    classifiers = list(project.get("classifiers", []) or [])
    return ParsedProjectMetadata(
        dependencies=dependencies,
        requires_python=project.get("requires-python"),
        license=license_value,
        classifiers=classifiers,
    )


def _parse_setup_cfg(path: Path) -> ParsedProjectMetadata:
    parser = configparser.ConfigParser()
    parser.read(path, encoding="utf-8")
    raw_dependencies = _split_multiline(
        parser.get("options", "install_requires", fallback="")
    )
    dependencies = {
        dep_name: dep_value
        for dep_name, dep_value in _normalize_dependencies(raw_dependencies)
    }
    if parser.has_section("options.extras_require"):
        for extra, value in parser.items("options.extras_require"):
            for dep_name, dep_value in _normalize_dependencies(_split_multiline(value)):
                dependencies[f"extra:{extra}:{dep_name}"] = dep_value
    classifiers = _split_multiline(parser.get("metadata", "classifiers", fallback=""))
    return ParsedProjectMetadata(
        dependencies=dependencies,
        requires_python=parser.get("options", "python_requires", fallback=None),
        license=parser.get("metadata", "license", fallback=None),
        classifiers=classifiers,
    )


def _parse_setup_py(path: Path) -> ParsedProjectMetadata:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    setup_call = None
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id == "setup":
            setup_call = node
            break
        if isinstance(node.func, ast.Attribute) and node.func.attr == "setup":
            setup_call = node
            break
    if setup_call is None:
        return ParsedProjectMetadata()

    keyword_map = {
        keyword.arg: keyword.value for keyword in setup_call.keywords if keyword.arg
    }
    dependencies = {
        dep_name: dep_value
        for dep_name, dep_value in _normalize_dependencies(
            _literal_list(keyword_map.get("install_requires"))
        )
    }
    extras_value = (
        _literal_value(keyword_map.get("extras_require"))
        if keyword_map.get("extras_require")
        else {}
    )
    if isinstance(extras_value, dict):
        for extra, values in extras_value.items():
            for dep_name, dep_value in _normalize_dependencies(
                values if isinstance(values, list) else []
            ):
                dependencies[f"extra:{extra}:{dep_name}"] = dep_value
    classifiers = _literal_list(keyword_map.get("classifiers"))
    license_value = _literal_scalar(keyword_map.get("license"))
    requires_python = _literal_scalar(keyword_map.get("python_requires"))
    return ParsedProjectMetadata(
        dependencies=dependencies,
        requires_python=requires_python,
        license=license_value,
        classifiers=[value for value in classifiers if isinstance(value, str)],
    )


def _parse_pkg_info(path: Path) -> ParsedProjectMetadata:
    parser = Parser()
    message = parser.parsestr(path.read_text(encoding="utf-8", errors="replace"))
    dependencies = {
        dep_name: dep_value
        for dep_name, dep_value in _normalize_dependencies(
            message.get_all("Requires-Dist") or []
        )
    }
    return ParsedProjectMetadata(
        dependencies=dependencies,
        requires_python=message.get("Requires-Python"),
        license=message.get("License"),
        classifiers=message.get_all("Classifier") or [],
    )


def _normalize_dependencies(values: list[str]) -> list[tuple[str, str]]:
    normalized: list[tuple[str, str]] = []
    for value in values:
        text = value.strip()
        if not text:
            continue
        try:
            requirement = Requirement(text)
            normalized.append((requirement.name.lower(), text))
        except InvalidRequirement:
            normalized.append((text.lower(), text))
    return normalized


def _split_multiline(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


def _find_shallowest(root: Path, filename: str) -> Path | None:
    candidates = list(root.rglob(filename))
    if not candidates:
        return None
    return min(
        candidates, key=lambda path: (len(path.relative_to(root).parts), str(path))
    )


def _literal_list(node: ast.AST | None) -> list[Any]:
    value = _literal_value(node)
    return value if isinstance(value, list) else []


def _literal_scalar(node: ast.AST | None) -> str | None:
    value = _literal_value(node)
    return value if isinstance(value, str) else None


def _literal_value(node: ast.AST | None) -> Any:
    if node is None:
        return None
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def _append_change(
    changes: list[dict[str, Any]],
    *,
    field: str,
    before: Any,
    after: Any,
    source: str | None,
) -> None:
    if before == after or (before in {None, ""} and after in {None, ""}):
        return
    changes.append({"field": field, "before": before, "after": after, "source": source})


def _extract_min_python(specifier: str | None) -> Version | None:
    if not specifier:
        return None
    candidates: list[Version] = []
    for operator, version in re.findall(
        r"(>=|>|==)\s*([0-9][0-9A-Za-z.\-]*)", specifier
    ):
        try:
            parsed = Version(version)
        except InvalidVersion:
            continue
        candidates.append(parsed)
    return max(candidates) if candidates else None


def _looks_public_python_module(path: str | None) -> bool:
    return _module_qualname(path) is not None


def _module_qualname(path: str | None) -> str | None:
    if not path or not path.endswith(".py"):
        return None
    normalized = path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    if normalized.startswith("src/"):
        normalized = normalized[4:]
    lower = normalized.lower()
    if lower.startswith(("tests/", "test/", "docs/", "examples/")):
        return None
    module = normalized[:-3]
    if module.endswith("/__init__"):
        module = module[: -len("/__init__")]
    if not module:
        return None
    return module.replace("/", ".")
