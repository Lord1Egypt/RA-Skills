"""Read-only material structure checks."""

from __future__ import annotations

from typing import Any

from .base import (
    AuditContext,
    bridge_error_message,
    finish_check,
    find_manifest_entry,
    make_finding,
    new_check,
    normalize_game_path,
)
from ..report.model import Severity, Status


def check_materials(ctx: AuditContext):
    check = new_check("MAT001", "Material structure (read-only)")
    if not ctx.options.live:
        check.status = Status.SKIP
        check.summary = "Live checks were not requested."
        check.details = {"reason": "live_not_requested"}
        return check
    if not ctx.options.materials:
        check.status = Status.SKIP
        check.summary = "No materials selected."
        check.details = {"reason": "no_materials_selected"}
        return check
    if ctx.bridge is None:
        check.status = Status.UNKNOWN
        check.summary = "Bridge is unavailable."
        check.details = {"reason": "bridge_unavailable", "error": ctx.bridge_error}
        return check

    entries: list[dict[str, Any]] = []
    for raw_path in ctx.options.materials:
        asset_path = normalize_game_path(raw_path)
        try:
            result = ctx.bridge.call("material_read", {"material_path": asset_path})
        except Exception as exc:  # noqa: BLE001
            message = bridge_error_message(exc)
            entries.append({"material": asset_path, "status": "read_failed", "error": message})
            check.add(
                make_finding(
                    "MAT001",
                    Severity.WARNING,
                    Status.UNKNOWN,
                    "Cannot read material",
                    f"{asset_path}: {message}",
                    asset=asset_path,
                    recommendation="Confirm the asset path and that the bridge is connected to the intended project.",
                )
            )
            continue

        data = result.get("data") if isinstance(result, dict) and isinstance(result.get("data"), dict) else {}
        expressions = data.get("expressions") or []
        count = int(data.get("count") or len(expressions) or 0)
        entry = find_manifest_entry(ctx.manifest, asset_path)
        entries.append(
            {
                "material": asset_path,
                "expression_count": count,
                "package_sha256": entry.sha256 if entry else "",
            }
        )
        if count == 0:
            check.add(
                make_finding(
                    "MAT001",
                    Severity.WARNING,
                    Status.WARN,
                    "Material has no expressions",
                    f"{asset_path}: expression_count=0",
                    asset=asset_path,
                    recommendation="Confirm the material is intentionally empty.",
                )
            )
        else:
            check.add(
                make_finding(
                    "MAT001",
                    Severity.INFO,
                    Status.PASS,
                    "Material is readable",
                    f"{asset_path}: expressions={count}",
                    asset=asset_path,
                )
            )

    check.details = {"materials": entries, "count": len(entries)}
    empty = sum(1 for item in entries if item.get("expression_count") == 0)
    unknown = sum(1 for item in entries if item.get("status") == "read_failed")
    check.summary = f"materials={len(entries)}, empty={empty}, read-failed={unknown}"
    return finish_check(check)
