"""Live, read-only bridge checks."""

from __future__ import annotations

from typing import Any

from .base import (
    AuditContext,
    bridge_error_message,
    engine_family,
    finish_check,
    find_manifest_entry,
    make_finding,
    new_check,
    normalize_game_path,
)
from ..report.model import Severity, Status


def check_health(ctx: AuditContext):
    check = new_check("LIVE001", "Bridge and editor health")
    if not ctx.options.live:
        check.status = Status.SKIP
        check.summary = "Live checks were not requested."
        check.details = {"reason": "live_not_requested"}
        return check
    if ctx.bridge is None:
        check.status = Status.UNKNOWN
        check.summary = "Bridge is unavailable."
        check.details = {"reason": "bridge_unavailable", "error": ctx.bridge_error}
        check.add(
            make_finding(
                "LIVE001",
                Severity.WARNING,
                Status.UNKNOWN,
                "Bridge is unavailable",
                ctx.bridge_error or "Could not connect to the local UE bridge.",
                recommendation="Start the UE editor and the bridge, then rerun with --live.",
            )
        )
        return finish_check(check)

    try:
        health = ctx.bridge.health()
    except Exception as exc:  # noqa: BLE001 - report, do not crash the audit
        check.status = Status.UNKNOWN
        check.summary = "Health request failed."
        check.details = {"reason": "health_failed", "error": bridge_error_message(exc)}
        check.add(
            make_finding(
                "LIVE001",
                Severity.WARNING,
                Status.UNKNOWN,
                "Bridge health request failed",
                bridge_error_message(exc),
                recommendation="Check the editor/bridge connection and rerun.",
            )
        )
        return finish_check(check)

    check.details = {"health": health, "bridge_error": ctx.bridge_error}
    if not health.get("bridge_loaded"):
        check.add(
            make_finding(
                "LIVE001",
                Severity.WARNING,
                Status.WARN,
                "C++ bridge is not loaded",
                "The editor bridge is reachable, but bridge_loaded is false; L2 reads may be degraded.",
                recommendation="Install/enable the editor bridge plugin if this project needs node-level reads.",
            )
        )
    expected_project = ctx.project.name
    actual_project = str(health.get("project_name") or "")
    if actual_project and expected_project and actual_project != expected_project:
        check.add(
            make_finding(
                "LIVE001",
                Severity.WARNING,
                Status.WARN,
                "Bridge is connected to a different project",
                f"Expected {expected_project!r}, got {actual_project!r}.",
                recommendation="Open the intended project in the editor and rerun.",
            )
        )
    expected_engine = str(ctx.engine.get("engine_version") or "")
    actual_engine = str(health.get("engine_version") or "")
    if (
        expected_engine
        and actual_engine
        and engine_family(expected_engine)
        and engine_family(actual_engine)
        and engine_family(expected_engine) != engine_family(actual_engine)
    ):
        check.add(
            make_finding(
                "LIVE001",
                Severity.WARNING,
                Status.WARN,
                "Bridge engine version differs from project metadata",
                f"Project metadata says {expected_engine!r}, bridge reports {actual_engine!r}.",
                recommendation="Confirm the editor version; version skew can change asset behavior.",
            )
        )
    check.summary = (
        f"bridge_loaded={health.get('bridge_loaded')}, "
        f"project={actual_project or 'unknown'}, engine={actual_engine or 'unknown'}"
    )
    return finish_check(check)


def check_blueprint_status(ctx: AuditContext):
    check = new_check("BP001", "Blueprint compile status (read-only)")
    if not ctx.options.live:
        check.status = Status.SKIP
        check.summary = "Live checks were not requested."
        check.details = {"reason": "live_not_requested"}
        return check
    if not ctx.options.blueprints:
        check.status = Status.SKIP
        check.summary = "No blueprints selected."
        check.details = {"reason": "no_blueprints_selected"}
        return check
    if ctx.bridge is None:
        check.status = Status.UNKNOWN
        check.summary = "Bridge is unavailable."
        check.details = {"reason": "bridge_unavailable", "error": ctx.bridge_error}
        return check

    entries: list[dict[str, Any]] = []
    for blueprint_raw in ctx.options.blueprints:
        blueprint = normalize_game_path(blueprint_raw)
        l2_error = ""
        try:
            result = ctx.bridge.call(
                "read_blueprint",
                {
                    "bp_path": blueprint,
                    "level": "L2",
                    "include_cdo": False,
                    "include_conn": True,
                },
            )
        except Exception as exc:  # noqa: BLE001
            l2_error = bridge_error_message(exc)
            try:
                result = ctx.bridge.call("read_blueprint", {"bp_path": blueprint, "level": "L1"})
            except Exception as fallback_exc:  # noqa: BLE001
                message = bridge_error_message(fallback_exc)
                entries.append({"blueprint": blueprint, "status": "read_failed", "error": message})
                check.add(
                    make_finding(
                        "BP001",
                        Severity.WARNING,
                        Status.UNKNOWN,
                        "Cannot read blueprint",
                        f"{blueprint}: {message}",
                        asset=blueprint,
                        recommendation="Confirm the asset path and that the editor bridge is connected to the right project.",
                    )
                )
                continue

        if not isinstance(result, dict):
            entries.append({"blueprint": blueprint, "status": "invalid_result"})
            check.add(
                make_finding(
                    "BP001",
                    Severity.WARNING,
                    Status.UNKNOWN,
                    "Blueprint read returned an invalid result",
                    blueprint,
                    asset=blueprint,
                )
            )
            continue

        l1 = result.get("l1") if isinstance(result.get("l1"), dict) else {}
        l2 = result.get("l2") if isinstance(result.get("l2"), dict) else {}
        graphs = l2.get("graphs") if isinstance(l2.get("graphs"), list) else []
        compile_status = str(l1.get("compile_status") or result.get("compile_status") or "")
        compile_source = str(l1.get("compile_status_source") or "")
        asset_name = str(l1.get("asset_name") or blueprint)
        entry = find_manifest_entry(ctx.manifest, blueprint)
        package_sha256 = entry.sha256 if entry else ""
        graph_count = len(graphs)
        node_count = sum(
            int(graph.get("node_count") or 0) for graph in graphs if isinstance(graph, dict)
        )
        connection_count = sum(
            int(graph.get("connection_count") or 0) for graph in graphs if isinstance(graph, dict)
        )
        l2_available = bool(l2.get("available"))
        entries.append(
            {
                "blueprint": blueprint,
                "asset_name": asset_name,
                "compile_status": compile_status or "unknown",
                "compile_status_source": compile_source,
                "parent_class": l1.get("parent_class", ""),
                "l2_available": l2_available,
                "l2_error": l2_error or str(l2.get("error") or ""),
                "graph_count": graph_count,
                "node_count": node_count,
                "connection_count": connection_count,
                "package_sha256": package_sha256,
            }
        )
        if l2_available and graph_count == 0:
            check.add(
                make_finding(
                    "BP001",
                    Severity.WARNING,
                    Status.WARN,
                    "Blueprint has no graphs",
                    f"{blueprint}: l2.available=true, graph_count=0",
                    asset=blueprint,
                    recommendation="Confirm the Blueprint is intentionally empty.",
                )
            )
        elif not l2_available:
            check.add(
                make_finding(
                    "BP001",
                    Severity.INFO,
                    Status.PASS,
                    "Blueprint graph details are unavailable",
                    f"{blueprint}: {l2_error or l2.get('error') or 'l2.available=false'}",
                    asset=blueprint,
                    recommendation="Compile status is still reported when available; graph details need L2 reads.",
                )
            )
        normalized = compile_status.casefold()
        if not compile_status or normalized == "unknown":
            check.add(
                make_finding(
                    "BP001",
                    Severity.INFO,
                    Status.UNKNOWN,
                    "Blueprint compile status is unknown",
                    f"{blueprint}: compile_status={compile_status or 'missing'}"
                    + (f" ({compile_source})" if compile_source else ""),
                    asset=blueprint,
                    recommendation="This can happen on older UE versions; verify compile status manually.",
                )
            )
            continue
        if normalized in {"bs_uptodate", "uptodate", "up_to_date"}:
            check.add(
                make_finding(
                    "BP001",
                    Severity.INFO,
                    Status.PASS,
                    "Blueprint compile status is up to date",
                    f"{blueprint}: graphs={graph_count}, nodes={node_count}, "
                    f"connections={connection_count}",
                    asset=blueprint,
                )
            )
            continue
        severity = Severity.ERROR if "error" in normalized else Severity.WARNING
        status = Status.FAIL if severity == Severity.ERROR else Status.WARN
        check.add(
            make_finding(
                "BP001",
                severity,
                status,
                "Blueprint is not up to date",
                f"{blueprint}: compile_status={compile_status}",
                asset=blueprint,
                recommendation="Compile the blueprint and fix errors; this audit does not compile.",
            )
        )

    known_ok = {"bs_uptodate", "uptodate", "up_to_date"}
    not_up_to_date = sum(
        1
        for item in entries
        if item.get("compile_status", "").casefold()
        not in known_ok | {"", "unknown"}
    )
    unknown = sum(
        1 for item in entries if item.get("compile_status", "").casefold() in ("", "unknown")
    )
    check.details = {"blueprints": entries, "count": len(entries)}
    check.summary = (
        f"blueprints={len(entries)}, not-up-to-date={not_up_to_date}, unknown={unknown}"
    )
    return finish_check(check)
