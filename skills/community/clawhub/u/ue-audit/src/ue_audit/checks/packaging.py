"""Offline packaging-readiness checks."""

from __future__ import annotations

import re
from pathlib import Path

from .base import AuditContext, finish_check, game_path_to_content_rel, make_finding, new_check
from ..report.model import Severity, Status


MAP_KEYS = ("GameDefaultMap", "EditorStartupMap", "ServerDefaultMap")
MAP_PATH_RE = re.compile(r'FilePath\s*=\s*"([^"]+)"')


def _read_ini_entries(path: Path) -> list[tuple[str, str, str]]:
    if not path.is_file():
        return []
    entries: list[tuple[str, str, str]] = []
    section = ""
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith(";") or stripped.startswith("#"):
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            section = stripped[1:-1].strip()
            continue
        if "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        entries.append((section, key.strip(), value.strip().strip('"')))
    return entries


def _manifest_has_map(ctx: AuditContext, game_path: str, manifest_paths: set[str]) -> bool:
    for candidate in game_path_to_content_rel(game_path):
        if candidate.casefold() in manifest_paths:
            return True
    return False


def check_packaging(ctx: AuditContext):
    check = new_check("PKG001", "Packaging readiness (offline)")
    default_engine = ctx.project.config_dir / "DefaultEngine.ini"
    default_game = ctx.project.config_dir / "DefaultGame.ini"
    engine_entries = _read_ini_entries(default_engine)
    game_entries = _read_ini_entries(default_game)

    map_values: dict[str, list[str]] = {key: [] for key in MAP_KEYS}
    for _section, key, value in engine_entries:
        if key in map_values and value:
            map_values[key].append(value)
    maps_to_cook: list[str] = []
    for _section, key, value in game_entries:
        if key.lstrip("+").strip() == "MapsToCook":
            match = MAP_PATH_RE.search(value)
            if match:
                maps_to_cook.append(match.group(1))
            elif value.startswith("/Game/"):
                maps_to_cook.append(value)

    manifest_paths = {path.casefold() for path in ctx.manifest.files}
    missing: list[dict[str, str]] = []
    for key, values in map_values.items():
        for value in values:
            if value.startswith("/Game/") and not _manifest_has_map(ctx, value, manifest_paths):
                missing.append({"key": key, "path": value})
    for value in maps_to_cook:
        if value.startswith("/Game/") and not _manifest_has_map(ctx, value, manifest_paths):
            missing.append({"key": "MapsToCook", "path": value})

    check.details = {
        "default_engine_ini": str(default_engine),
        "default_game_ini": str(default_game),
        "maps": map_values,
        "maps_to_cook": maps_to_cook[:50],
        "missing_maps": missing[:50],
    }

    if not default_engine.is_file():
        check.add(
            make_finding(
                "PKG001",
                Severity.WARNING,
                Status.WARN,
                "DefaultEngine.ini is missing",
                "Packaging map settings cannot be evaluated.",
                recommendation="Restore Config/DefaultEngine.ini or confirm this is intentional.",
            )
        )
    if not map_values["GameDefaultMap"]:
        check.add(
            make_finding(
                "PKG001",
                Severity.WARNING,
                Status.WARN,
                "No GameDefaultMap configured",
                "DefaultEngine.ini does not define a /Game/ GameDefaultMap.",
                recommendation="Set GameDefaultMap before packaging.",
            )
        )
    for item in missing:
        check.add(
            make_finding(
                "PKG001",
                Severity.ERROR,
                Status.FAIL,
                "Configured map is missing from the project manifest",
                f"{item['key']}={item['path']}",
                asset=item["path"],
                recommendation="Fix the map path or add the missing map asset.",
            )
        )
    if not maps_to_cook:
        check.add(
            make_finding(
                "PKG001",
                Severity.INFO,
                Status.PASS,
                "No explicit MapsToCook entries",
                "ProjectPackagingSettings does not list maps to cook; UE may use defaults.",
                recommendation="Confirm packaging includes the intended maps.",
            )
        )
    if not missing and map_values["GameDefaultMap"] and default_engine.is_file():
        check.add(
            make_finding(
                "PKG001",
                Severity.INFO,
                Status.PASS,
                "Packaging map settings are readable",
                f"GameDefaultMap={map_values['GameDefaultMap'][0]}, "
                f"MapsToCook={len(maps_to_cook)}",
            )
        )

    check.summary = (
        f"GameDefaultMap={len(map_values['GameDefaultMap'])}, "
        f"MapsToCook={len(maps_to_cook)}, missing={len(missing)}"
    )
    return finish_check(check)
