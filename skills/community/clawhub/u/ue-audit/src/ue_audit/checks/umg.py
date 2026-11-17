"""Read-only UMG widget tree checks."""

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


def check_widgets(ctx: AuditContext):
    check = new_check("UMG001", "Widget tree (read-only)")
    if not ctx.options.live:
        check.status = Status.SKIP
        check.summary = "Live checks were not requested."
        check.details = {"reason": "live_not_requested"}
        return check
    if not ctx.options.widgets:
        check.status = Status.SKIP
        check.summary = "No widgets selected."
        check.details = {"reason": "no_widgets_selected"}
        return check
    if ctx.bridge is None:
        check.status = Status.UNKNOWN
        check.summary = "Bridge is unavailable."
        check.details = {"reason": "bridge_unavailable", "error": ctx.bridge_error}
        return check

    entries: list[dict[str, Any]] = []
    for raw_path in ctx.options.widgets:
        asset_path = normalize_game_path(raw_path)
        try:
            result = ctx.bridge.call("widget_read_tree", {"widget_path": asset_path})
        except Exception as exc:  # noqa: BLE001
            message = bridge_error_message(exc)
            entries.append({"widget": asset_path, "status": "read_failed", "error": message})
            check.add(
                make_finding(
                    "UMG001",
                    Severity.WARNING,
                    Status.UNKNOWN,
                    "Cannot read widget tree",
                    f"{asset_path}: {message}",
                    asset=asset_path,
                    recommendation="Confirm the asset path and that the bridge is connected to the intended project.",
                )
            )
            continue

        if not isinstance(result, dict):
            entries.append({"widget": asset_path, "status": "invalid_result"})
            check.add(
                make_finding(
                    "UMG001",
                    Severity.WARNING,
                    Status.UNKNOWN,
                    "Widget read returned an invalid result",
                    asset_path,
                    asset=asset_path,
                )
            )
            continue

        data = result.get("data") if isinstance(result.get("data"), dict) else {}
        widgets = data.get("widgets") or []
        count = int(data.get("count") or len(widgets) or 0)
        roots = [item for item in widgets if isinstance(item, dict) and not item.get("parent")]
        names = [str(item.get("name")) for item in widgets if isinstance(item, dict) and item.get("name")]
        duplicate_names = sorted({name for name in names if names.count(name) > 1})
        root_class = str(roots[0].get("class") or "") if len(roots) == 1 else ""
        entry = find_manifest_entry(ctx.manifest, asset_path)
        package_sha256 = entry.sha256 if entry else ""
        entries.append(
            {
                "widget": asset_path,
                "count": count,
                "root_count": len(roots),
                "root_class": root_class,
                "duplicate_widget_names": duplicate_names,
                "package_sha256": package_sha256,
            }
        )

        if count == 0 or not widgets:
            check.add(
                make_finding(
                    "UMG001",
                    Severity.ERROR,
                    Status.FAIL,
                    "Widget tree is empty",
                    f"{asset_path}: count=0",
                    asset=asset_path,
                    recommendation="Open the widget in the editor and confirm it has a root and children.",
                )
            )
        elif not roots:
            check.add(
                make_finding(
                    "UMG001",
                    Severity.WARNING,
                    Status.WARN,
                    "Widget tree has no root",
                    f"{asset_path}: {count} widgets, no parent-less root found.",
                    asset=asset_path,
                    recommendation="Inspect the hierarchy; the reader may be incomplete.",
                )
            )
        elif len(roots) > 1:
            check.add(
                make_finding(
                    "UMG001",
                    Severity.WARNING,
                    Status.WARN,
                    "Widget tree has multiple roots",
                    f"{asset_path}: {len(roots)} parent-less widgets.",
                    asset=asset_path,
                    recommendation="Confirm the hierarchy in the UMG designer.",
                )
            )
        else:
            check.add(
                make_finding(
                    "UMG001",
                    Severity.INFO,
                    Status.PASS,
                    "Widget tree is readable",
                    f"{asset_path}: {count} widgets, root={roots[0].get('name', '')} "
                    f"({root_class or 'unknown class'})",
                    asset=asset_path,
                )
            )

        if duplicate_names:
            check.add(
                make_finding(
                    "UMG001",
                    Severity.WARNING,
                    Status.WARN,
                    "Widget tree has duplicate widget names",
                    f"{asset_path}: {', '.join(duplicate_names[:10])}",
                    asset=asset_path,
                    recommendation="Rename duplicate widgets; duplicate names make bindings and lookups ambiguous.",
                )
            )
        if roots and not root_class:
            check.add(
                make_finding(
                    "UMG001",
                    Severity.WARNING,
                    Status.UNKNOWN,
                    "Widget root class is unavailable",
                    f"{asset_path}: root has no class.",
                    asset=asset_path,
                    recommendation="Inspect the widget in the editor; the reader may be incomplete.",
                )
            )

    check.details = {"widgets": entries, "count": len(entries)}
    empty = sum(1 for item in entries if item.get("count") == 0)
    unknown = sum(1 for item in entries if item.get("status") == "read_failed")
    duplicates = sum(1 for item in entries if item.get("duplicate_widget_names"))
    check.summary = (
        f"widgets={len(entries)}, empty={empty}, read-failed={unknown}, "
        f"duplicate-names={duplicates}"
    )
    return finish_check(check)
