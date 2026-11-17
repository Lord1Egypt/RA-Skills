"""Project structure and abnormal-file checks."""

from __future__ import annotations

import json
from pathlib import Path

from .base import AuditContext, finish_check, make_finding, new_check
from ..report.model import Severity, Status


def check_project_structure(ctx: AuditContext):
    check = new_check("PRJ001", "Project structure and engine association")
    project = ctx.project

    if not project.content_dir.is_dir():
        check.add(
            make_finding(
                "PRJ001",
                Severity.BLOCKER,
                Status.FAIL,
                "Content directory is missing",
                f"Expected {project.content_dir}",
                recommendation="Confirm this is a complete Unreal project.",
            )
        )
    if not project.config_dir.is_dir():
        check.add(
            make_finding(
                "PRJ001",
                Severity.ERROR,
                Status.FAIL,
                "Config directory is missing",
                f"Expected {project.config_dir}",
                recommendation="Restore the project Config directory before auditing.",
            )
        )

    default_engine = project.config_dir / "DefaultEngine.ini"
    default_game = project.config_dir / "DefaultGame.ini"
    if project.config_dir.is_dir() and not default_engine.is_file():
        check.add(
            make_finding(
                "PRJ001",
                Severity.WARNING,
                Status.WARN,
                "DefaultEngine.ini is missing",
                f"Expected {default_engine}",
                recommendation="Check whether this project is intentionally minimal.",
            )
        )
    if project.config_dir.is_dir() and not default_game.is_file():
        check.add(
            make_finding(
                "PRJ001",
                Severity.INFO,
                Status.PASS,
                "DefaultGame.ini is missing",
                f"Expected {default_game}",
                recommendation="Not always required, but worth confirming.",
            )
        )

    if not project.source_dir.is_dir():
        check.add(
            make_finding(
                "PRJ001",
                Severity.INFO,
                Status.PASS,
                "Source directory is absent",
                "This is normal for a Blueprint-only project.",
                recommendation="No action needed unless the project is expected to contain C++ modules.",
            )
        )

    if not project.engine_association:
        check.add(
            make_finding(
                "PRJ001",
                Severity.WARNING,
                Status.WARN,
                "EngineAssociation is empty",
                "The .uproject does not declare an engine association.",
                recommendation="Set EngineAssociation or pass --engine so the report can record the engine version.",
            )
        )

    plugin_findings = 0
    for plugin in project.plugins:
        name = str(plugin.get("Name") or "").strip()
        if not name:
            check.add(
                make_finding(
                    "PRJ001",
                    Severity.WARNING,
                    Status.WARN,
                    "Plugin entry has no name",
                    "A Plugins entry in the .uproject is missing Name.",
                    recommendation="Fix the .uproject plugin entry.",
                )
            )
            plugin_findings += 1
            continue
        enabled = plugin.get("Enabled", True)
        local_path = project.local_plugin_path(name)
        if local_path.is_file():
            try:
                json.loads(local_path.read_text(encoding="utf-8-sig"))
            except (OSError, ValueError):
                check.add(
                    make_finding(
                        "PRJ001",
                        Severity.WARNING,
                        Status.WARN,
                        "Plugin descriptor is not valid JSON",
                        str(local_path),
                        asset=str(local_path),
                        recommendation="Open the .uplugin file and fix the JSON.",
                    )
                )
                plugin_findings += 1
        elif enabled:
            check.add(
                make_finding(
                    "PRJ001",
                    Severity.INFO,
                    Status.PASS,
                    "Plugin is not present in the project Plugins directory",
                    f"{name} may be an engine or marketplace plugin.",
                    asset=name,
                    recommendation="No action needed if the plugin resolves at editor startup.",
                )
            )
            plugin_findings += 1

    check.details = {
        "project_root": str(project.root),
        "uproject": str(project.uproject),
        "engine_association": project.engine_association,
        "has_content": project.content_dir.is_dir(),
        "has_config": project.config_dir.is_dir(),
        "has_source": project.source_dir.is_dir(),
        "plugin_count": len(project.plugins),
        "plugin_findings": plugin_findings,
    }
    check.summary = (
        f"{project.name}: Content={project.content_dir.is_dir()}, "
        f"Config={project.config_dir.is_dir()}, Source={project.source_dir.is_dir()}, "
        f"plugins={len(project.plugins)}"
    )
    return finish_check(check)


def check_abnormal_files(ctx: AuditContext):
    check = new_check("PRJ003", "Abnormal file facts")
    threshold = int(ctx.options.max_file_mb * 1024 * 1024)
    zero_byte: list[dict[str, object]] = []
    large: list[dict[str, object]] = []
    hash_errors: list[dict[str, object]] = []
    duplicates: dict[str, list[str]] = {}

    for path, entry in sorted(ctx.manifest.files.items()):
        if entry.error:
            hash_errors.append({"path": path, "error": entry.error})
        if entry.size == 0:
            zero_byte.append({"path": path, "sha256": entry.sha256})
        if entry.size > threshold:
            large.append({"path": path, "size": entry.size})
        if entry.sha256:
            duplicates.setdefault(entry.sha256, []).append(path)

    for item in zero_byte[:50]:
        path = str(item["path"])
        severity = (
            Severity.WARNING
            if path.lower().endswith((".uasset", ".umap"))
            else Severity.INFO
        )
        check.add(
            make_finding(
                "PRJ003",
                severity,
                Status.WARN if severity == Severity.WARNING else Status.PASS,
                "Zero-byte file",
                path,
                asset=path,
                recommendation="Confirm whether this file is a placeholder or a broken asset.",
            )
        )
    if len(zero_byte) > 50:
        check.add(
            make_finding(
                "PRJ003",
                Severity.INFO,
                Status.PASS,
                "Additional zero-byte files omitted",
                f"{len(zero_byte) - 50} more zero-byte files were not listed.",
                evidence=[],
            )
        )

    for item in large[:50]:
        path = str(item["path"])
        check.add(
            make_finding(
                "PRJ003",
                Severity.INFO,
                Status.PASS,
                "Large file fact",
                f"{path} is {int(item['size'])} bytes (threshold {threshold}).",
                asset=path,
                recommendation="Review whether this file belongs in source control; no failure is implied.",
            )
        )

    duplicate_groups = [
        {"sha256": digest, "paths": paths}
        for digest, paths in duplicates.items()
        if len(paths) > 1
    ]
    duplicate_groups.sort(key=lambda item: (-len(item["paths"]), item["sha256"]))

    check.details = {
        "threshold_bytes": threshold,
        "zero_byte_count": len(zero_byte),
        "large_file_count": len(large),
        "hash_error_count": len(hash_errors),
        "duplicate_hash_group_count": len(duplicate_groups),
        "zero_byte_files": zero_byte[:50],
        "large_files": large[:50],
        "hash_errors": hash_errors[:50],
        "duplicate_hash_groups": duplicate_groups[:20],
    }
    check.summary = (
        f"zero-byte={len(zero_byte)}, large={len(large)}, "
        f"hash-errors={len(hash_errors)}, duplicate-groups={len(duplicate_groups)}"
    )
    return finish_check(check)
