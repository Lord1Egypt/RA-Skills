"""Read-only AnimBlueprint structure checks."""

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


def check_animbp(ctx: AuditContext):
    check = new_check("ANIM001", "AnimBlueprint structure (read-only)")
    if not ctx.options.live:
        check.status = Status.SKIP
        check.summary = "Live checks were not requested."
        check.details = {"reason": "live_not_requested"}
        return check
    if not ctx.options.animbps:
        check.status = Status.SKIP
        check.summary = "No AnimBlueprints selected."
        check.details = {"reason": "no_animbps_selected"}
        return check
    if ctx.bridge is None:
        check.status = Status.UNKNOWN
        check.summary = "Bridge is unavailable."
        check.details = {"reason": "bridge_unavailable", "error": ctx.bridge_error}
        return check

    entries: list[dict[str, Any]] = []
    for raw_path in ctx.options.animbps:
        asset_path = normalize_game_path(raw_path)
        try:
            probe = ctx.bridge.call("animbp_probe", {"asset_path": asset_path})
        except Exception as exc:  # noqa: BLE001
            message = bridge_error_message(exc)
            entries.append({"animbp": asset_path, "status": "probe_failed", "error": message})
            check.add(
                make_finding(
                    "ANIM001",
                    Severity.WARNING,
                    Status.UNKNOWN,
                    "Cannot probe AnimBlueprint",
                    f"{asset_path}: {message}",
                    asset=asset_path,
                    recommendation="Confirm the asset path and bridge connection.",
                )
            )
            continue

        probe_data = probe.get("data") if isinstance(probe, dict) and isinstance(probe.get("data"), dict) else {}
        is_animbp = bool(probe_data.get("is_animbp"))
        if not is_animbp:
            entries.append({"animbp": asset_path, "status": "not_animbp"})
            check.add(
                make_finding(
                    "ANIM001",
                    Severity.WARNING,
                    Status.UNKNOWN,
                    "Asset is not an AnimBlueprint",
                    f"{asset_path}: is_animbp=false",
                    asset=asset_path,
                    recommendation="Pass an AnimBlueprint asset path.",
                )
            )
            continue

        try:
            result = ctx.bridge.call(
                "animbp_read", {"asset_path": asset_path, "include_nodes": True, "limit": 500}
            )
        except Exception as exc:  # noqa: BLE001
            message = bridge_error_message(exc)
            entries.append({"animbp": asset_path, "status": "read_failed", "error": message})
            check.add(
                make_finding(
                    "ANIM001",
                    Severity.WARNING,
                    Status.UNKNOWN,
                    "Cannot read AnimBlueprint",
                    f"{asset_path}: {message}",
                    asset=asset_path,
                    recommendation="Confirm the bridge supports AnimBlueprint reads on this UE version.",
                )
            )
            continue

        if not isinstance(result, dict) or result.get("ok") is False:
            error = ""
            if isinstance(result, dict):
                error = str(result.get("error") or result.get("warning") or "")
            entries.append({"animbp": asset_path, "status": "read_failed", "error": error})
            check.add(
                make_finding(
                    "ANIM001",
                    Severity.WARNING,
                    Status.UNKNOWN,
                    "AnimBlueprint read was incomplete",
                    f"{asset_path}: {error or 'ok=false'}",
                    asset=asset_path,
                    recommendation="Inspect the AnimBlueprint in the editor; this audit only reads.",
                )
            )
            continue

        graphs = result.get("graphs") or []
        graph_count = int(result.get("graph_count") or len(graphs) or 0)
        node_count = sum(int(graph.get("node_count") or 0) for graph in graphs if isinstance(graph, dict))
        nodes_available = all(
            bool(graph.get("nodes_available", True)) for graph in graphs if isinstance(graph, dict)
        )
        entry = find_manifest_entry(ctx.manifest, asset_path)
        entries.append(
            {
                "animbp": asset_path,
                "graph_count": graph_count,
                "node_count": node_count,
                "nodes_available": nodes_available,
                "package_sha256": entry.sha256 if entry else "",
            }
        )

        if graph_count == 0:
            check.add(
                make_finding(
                    "ANIM001",
                    Severity.WARNING,
                    Status.WARN,
                    "AnimBlueprint has no graphs",
                    f"{asset_path}: graph_count=0",
                    asset=asset_path,
                    recommendation="Confirm the AnimBlueprint is intentionally empty.",
                )
            )
        elif not nodes_available:
            check.add(
                make_finding(
                    "ANIM001",
                    Severity.WARNING,
                    Status.UNKNOWN,
                    "AnimBlueprint node data is unavailable",
                    f"{asset_path}: {graph_count} graphs, node data incomplete.",
                    asset=asset_path,
                    recommendation="This can happen on older bridges; inspect the graph manually.",
                )
            )
        else:
            check.add(
                make_finding(
                    "ANIM001",
                    Severity.INFO,
                    Status.PASS,
                    "AnimBlueprint is readable",
                    f"{asset_path}: graphs={graph_count}, nodes={node_count}",
                    asset=asset_path,
                )
            )

    check.details = {"animbps": entries, "count": len(entries)}
    empty = sum(1 for item in entries if item.get("graph_count") == 0)
    unknown = sum(1 for item in entries if item.get("status") in {"read_failed", "probe_failed", "not_animbp"})
    check.summary = f"animbps={len(entries)}, empty={empty}, incomplete={unknown}"
    return finish_check(check)
