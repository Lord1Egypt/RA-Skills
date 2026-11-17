"""Read-only DataTable checks."""

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


def check_datatables(ctx: AuditContext):
    check = new_check("DT001", "DataTable structure (read-only)")
    if not ctx.options.live:
        check.status = Status.SKIP
        check.summary = "Live checks were not requested."
        check.details = {"reason": "live_not_requested"}
        return check
    if not ctx.options.datatables:
        check.status = Status.SKIP
        check.summary = "No DataTables selected."
        check.details = {"reason": "no_datatables_selected"}
        return check
    if ctx.bridge is None:
        check.status = Status.UNKNOWN
        check.summary = "Bridge is unavailable."
        check.details = {"reason": "bridge_unavailable", "error": ctx.bridge_error}
        return check

    entries: list[dict[str, Any]] = []
    for raw_path in ctx.options.datatables:
        asset_path = normalize_game_path(raw_path)
        try:
            result = ctx.bridge.call(
                "datatable_read",
                {"asset_path": asset_path, "limit": 50, "include_csv": True},
            )
        except Exception as exc:  # noqa: BLE001
            message = bridge_error_message(exc)
            entries.append({"datatable": asset_path, "status": "read_failed", "error": message})
            check.add(
                make_finding(
                    "DT001",
                    Severity.WARNING,
                    Status.UNKNOWN,
                    "Cannot read DataTable",
                    f"{asset_path}: {message}",
                    asset=asset_path,
                    recommendation="Confirm the asset path and that the bridge is connected to the intended project.",
                )
            )
            continue

        if not isinstance(result, dict):
            entries.append({"datatable": asset_path, "status": "invalid_result"})
            check.add(
                make_finding(
                    "DT001",
                    Severity.WARNING,
                    Status.UNKNOWN,
                    "DataTable read returned an invalid result",
                    asset_path,
                    asset=asset_path,
                )
            )
            continue

        data = result.get("data") if isinstance(result.get("data"), dict) else {}
        row_count = int(data.get("row_count") or 0)
        row_struct = str(data.get("row_struct") or "")
        row_names = data.get("row_names") or []
        csv_supported = bool(data.get("csv_supported"))
        truncated = bool(data.get("truncated"))
        warnings = data.get("warnings") or []
        entry = find_manifest_entry(ctx.manifest, asset_path)
        package_sha256 = entry.sha256 if entry else ""
        duplicate_rows = sorted(
            {str(name) for name in row_names if list(row_names).count(name) > 1}
        )
        entries.append(
            {
                "datatable": asset_path,
                "row_count": row_count,
                "row_names": list(row_names)[:20],
                "duplicate_row_names": duplicate_rows,
                "row_struct": row_struct,
                "csv_supported": csv_supported,
                "truncated": truncated,
                "package_sha256": package_sha256,
            }
        )

        if row_count == 0:
            check.add(
                make_finding(
                    "DT001",
                    Severity.WARNING,
                    Status.WARN,
                    "DataTable is empty",
                    f"{asset_path}: row_count=0",
                    asset=asset_path,
                    recommendation="Confirm whether an empty table is intentional.",
                )
            )
        if not row_struct:
            check.add(
                make_finding(
                    "DT001",
                    Severity.WARNING,
                    Status.UNKNOWN,
                    "DataTable row struct is unavailable",
                    f"{asset_path}: row_struct is empty.",
                    asset=asset_path,
                    recommendation="Inspect the table in the editor; this audit only reads.",
                )
            )
        if duplicate_rows:
            check.add(
                make_finding(
                    "DT001",
                    Severity.WARNING,
                    Status.WARN,
                    "DataTable has duplicate row names",
                    f"{asset_path}: {', '.join(duplicate_rows[:10])}",
                    asset=asset_path,
                    recommendation="Row names should be unique; inspect the table in the editor.",
                )
            )
        if not csv_supported:
            check.add(
                make_finding(
                    "DT001",
                    Severity.INFO,
                    Status.PASS,
                    "DataTable CSV export is unavailable",
                    f"{asset_path}: only row names are available on this UE version.",
                    asset=asset_path,
                )
            )
        if warnings:
            check.add(
                make_finding(
                    "DT001",
                    Severity.INFO,
                    Status.PASS,
                    "DataTable read warnings",
                    f"{asset_path}: " + "; ".join(str(item) for item in warnings[:5]),
                    asset=asset_path,
                )
            )
        if row_count > 0:
            names = ", ".join(str(name) for name in list(row_names)[:10]) or "(names unavailable)"
            check.add(
                make_finding(
                    "DT001",
                    Severity.INFO,
                    Status.PASS,
                    "DataTable rows are readable",
                    f"{asset_path}: rows={row_count}, names={names}, "
                    f"row_struct={row_struct or 'unknown'}"
                    + (", truncated" if truncated else ""),
                    asset=asset_path,
                )
            )

    check.details = {"datatables": entries, "count": len(entries)}
    empty = sum(1 for item in entries if item.get("row_count") == 0)
    unknown = sum(1 for item in entries if item.get("status") == "read_failed")
    struct_unknown = sum(
        1
        for item in entries
        if item.get("status") != "read_failed" and not item.get("row_struct")
    )
    duplicate_rows = sum(1 for item in entries if item.get("duplicate_row_names"))
    check.summary = (
        f"datatables={len(entries)}, empty={empty}, "
        f"read-failed={unknown}, struct-unknown={struct_unknown}, "
        f"duplicate-rows={duplicate_rows}"
    )
    return finish_check(check)
