"""Command-line interface for ue-audit."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

from .baseline import BaselineError, baseline_info, load_baseline, write_baseline
from .bridge import BridgeClient, read_token
from .checks import (
    check_abnormal_files,
    check_animbp,
    check_baseline_diff,
    check_blueprint_status,
    check_datatables,
    check_git,
    check_health,
    check_logs,
    check_materials,
    check_packaging,
    check_pie,
    check_project_structure,
    check_readonly_proof,
    check_write_monitor,
    check_task_changes,
    check_widgets,
)
from .checks.base import AuditContext, AuditOptions
from .manifest import (
    build_manifest,
    diff_manifests,
    manifest_summary,
    save_manifest,
)
from .project import ProjectError, find_project, resolve_engine_version
from .provenance import load_task_manifest
from .readonly import ReadOnlyBridge, build_readonly_proof
from .report import Report, write_reports
from .report.render_json import write_json
from .util import TOOL_VERSION, new_run_id, utc_now
from .watcher import DirectoryWatcher


DEFAULT_FORMATS = "json,md,html,junit"
DEFAULT_LIMITATIONS = [
    "This is an assessment report, not a certification.",
    "The audit is read-only in intent, but it cannot prove that no write occurred; see readonly_proof.",
    "Offline checks do not parse .uasset binaries.",
    "The report does not judge gameplay, design intent, art quality, or balance.",
]


def _default_bridge_port() -> int:
    try:
        return int(os.environ.get("UE_AUDIT_BRIDGE_PORT", "8889") or 8889)
    except ValueError:
        return 8889


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ue-audit",
        description="Read-only Unreal Engine project audit and report tool.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  ue-audit audit C:/Projects/MyGame\n"
            "  ue-audit audit C:/Projects/MyGame --baseline audit-baseline.json --live --blueprint /Game/BP_Player\n"
            "  ue-audit verify C:/Projects/MyGame --task task.json --baseline before.json\n"
            "  ue-audit doctor C:/Projects/MyGame --live\n"
        ),
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {TOOL_VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)

    audit = sub.add_parser("audit", help="Audit a project without a task manifest.")
    _add_common(audit)
    _add_live(audit)
    audit.set_defaults(func=run_audit)

    verify = sub.add_parser("verify", help="Verify an AI task against an expected write set.")
    _add_common(verify)
    _add_live(verify)
    verify.add_argument("--task", required=True, help="Task manifest JSON.")
    verify.set_defaults(func=run_verify)

    doctor = sub.add_parser("doctor", help="Check project discovery and optional bridge health.")
    doctor.add_argument("project", help="Project directory or .uproject file.")
    doctor.add_argument("--engine", default="", help="Optional engine root.")
    doctor.add_argument("--live", action="store_true", help="Also check the local bridge.")
    doctor.add_argument("--bridge-host", default="127.0.0.1")
    doctor.add_argument("--bridge-port", type=int, default=_default_bridge_port())
    doctor.add_argument("--token", default="")
    doctor.add_argument("--json", action="store_true", help="Print JSON.")
    doctor.set_defaults(func=run_doctor)
    return parser


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("project", help="Project directory or .uproject file.")
    parser.add_argument("--out", default="", help="Output directory outside the project.")
    parser.add_argument("--baseline", default="", help="Baseline manifest JSON.")
    parser.add_argument("--save-baseline", default="", help="Write the current manifest here.")
    parser.add_argument("--engine", default="", help="Optional engine root.")
    parser.add_argument(
        "--format",
        default=DEFAULT_FORMATS,
        help="Comma-separated formats: json,md,html,junit.",
    )
    parser.add_argument("--max-file-mb", type=float, default=100.0)
    parser.add_argument("--max-hash-mb", type=float, default=512.0)
    parser.add_argument(
        "--no-git",
        action="store_false",
        dest="include_git",
        help="Disable the Git working-tree check.",
    )
    parser.add_argument("--git-large-mb", type=float, default=50.0)
    parser.add_argument(
        "--no-watch",
        action="store_false",
        dest="watch_files",
        help="Disable the best-effort during-write directory monitor.",
    )
    parser.add_argument(
        "--ignore-mtime",
        action="store_true",
        help="Ignore mtime-only differences in the baseline diff (PRJ002).",
    )
    parser.add_argument("--quiet", action="store_true", help="Only print the output directory.")
    parser.add_argument("--json", action="store_true", help="Print the report JSON to stdout.")
    parser.add_argument(
        "--fail-on",
        choices=("warning", "error", "blocker"),
        default="warning",
        help="Lowest severity that makes the command exit nonzero (default: warning).",
    )


def _add_live(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--live", action="store_true", help="Enable optional bridge checks.")
    parser.add_argument("--bridge-host", default="127.0.0.1")
    parser.add_argument("--bridge-port", type=int, default=_default_bridge_port())
    parser.add_argument("--token", default="", help="Bridge token; defaults to env/APPDATA.")
    parser.add_argument(
        "--blueprint",
        action="append",
        default=[],
        help="Blueprint /Game path to read compile status for; repeatable.",
    )
    parser.add_argument(
        "--datatable",
        action="append",
        default=[],
        help="DataTable /Game path to read structure for; repeatable.",
    )
    parser.add_argument(
        "--widget",
        action="append",
        default=[],
        help="WidgetBlueprint /Game path to read the tree for; repeatable.",
    )
    parser.add_argument(
        "--material",
        action="append",
        default=[],
        help="Material /Game path to read expressions for; repeatable.",
    )
    parser.add_argument(
        "--animbp",
        action="append",
        default=[],
        help="AnimBlueprint /Game path to read graphs for; repeatable.",
    )
    parser.add_argument("--max-logs", type=int, default=3)
    parser.add_argument("--log-since-hours", type=int, default=0)
    parser.add_argument(
        "--pie",
        action="store_true",
        help="Opt in to a short stateful PIE smoke test. Does not save assets.",
    )
    parser.add_argument("--pie-seconds", type=float, default=3.0)
    parser.add_argument("--pie-mode", choices=("pie", "simulate"), default="pie")


def _default_out_dir(project_root: Path, project_name: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_name = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in project_name)
    return project_root.parent / "ue-audit-reports" / f"{safe_name}-{stamp}"


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _resolve_out_dir(args: argparse.Namespace, project_root: Path, project_name: str) -> Path:
    if args.out:
        out = Path(args.out).expanduser().resolve()
    else:
        out = _default_out_dir(project_root, project_name).resolve()
    if _is_relative_to(out, project_root):
        raise ValueError(
            "output directory must be outside the project so the audit does not write into it: "
            f"{out}"
        )
    out.mkdir(parents=True, exist_ok=True)
    return out


def _make_context(
    args: argparse.Namespace,
    project,
    engine: dict[str, Any],
    manifest,
    baseline,
    diff,
    out_dir: Path,
    live_bridge,
    bridge_error: str,
) -> AuditContext:
    options = AuditOptions(
        live=bool(getattr(args, "live", False)),
        blueprints=list(getattr(args, "blueprint", []) or []),
        datatables=list(getattr(args, "datatable", []) or []),
        widgets=list(getattr(args, "widget", []) or []),
        materials=list(getattr(args, "material", []) or []),
        animbps=list(getattr(args, "animbp", []) or []),
        max_file_mb=float(args.max_file_mb),
        max_logs=int(getattr(args, "max_logs", 3)),
        log_since_hours=int(getattr(args, "log_since_hours", 0)),
        include_git=bool(getattr(args, "include_git", True)),
        git_large_mb=float(getattr(args, "git_large_mb", 50.0)),
        watch_files=bool(getattr(args, "watch_files", True)),
        pie=bool(getattr(args, "pie", False)),
        pie_seconds=float(getattr(args, "pie_seconds", 3.0)),
        pie_mode=str(getattr(args, "pie_mode", "pie")),
        max_hash_bytes=int(args.max_hash_mb * 1024 * 1024),
    )
    evidence_dir = out_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    return AuditContext(
        project=project,
        engine=engine,
        manifest=manifest,
        baseline=baseline,
        diff=diff,
        options=options,
        output_dir=out_dir,
        evidence_dir=evidence_dir,
        bridge=live_bridge,
        bridge_error=bridge_error,
    )


def _connect_live(args: argparse.Namespace):
    if not getattr(args, "live", False):
        return None, ""
    token = read_token(getattr(args, "token", "") or None)
    client = BridgeClient(
        host=getattr(args, "bridge_host", "127.0.0.1"),
        port=int(getattr(args, "bridge_port", 8889)),
        token=token,
    )
    wrapper = ReadOnlyBridge(client)
    try:
        wrapper.health()
    except Exception as exc:  # noqa: BLE001 - live checks are optional
        return None, str(exc)
    return wrapper, ""


def _write_evidence(
    ctx: AuditContext,
    manifest_before,
    manifest_after,
    diff,
    proof,
    checks_data,
    write_monitor,
) -> dict[str, str]:
    from .util import sha256_file

    paths: dict[str, str] = {}
    before_path = ctx.evidence_dir / "manifest-before.json"
    save_manifest(manifest_before, before_path)
    paths["manifest_before"] = "evidence/manifest-before.json"
    after_path = ctx.evidence_dir / "manifest-after.json"
    save_manifest(manifest_after, after_path)
    paths["manifest_after"] = "evidence/manifest-after.json"
    diff_path = ctx.evidence_dir / "manifest-diff.json"
    write_json(diff, diff_path)
    paths["manifest_diff"] = "evidence/manifest-diff.json"
    proof_path = ctx.evidence_dir / "readonly-proof.json"
    write_json(proof, proof_path)
    paths["readonly_proof"] = "evidence/readonly-proof.json"
    checks_path = ctx.evidence_dir / "checks.json"
    write_json(checks_data, checks_path)
    paths["checks"] = "evidence/checks.json"
    write_events_path = ctx.evidence_dir / "write-events.json"
    write_json(write_monitor or {}, write_events_path)
    paths["write_events"] = "evidence/write-events.json"
    index_path = ctx.evidence_dir / "index.json"
    write_json(
        {
            "schema_version": 1,
            "files": {
                name: {
                    "path": relative,
                    "size": (ctx.output_dir / relative).stat().st_size,
                    "sha256": sha256_file(ctx.output_dir / relative),
                }
                for name, relative in paths.items()
                if (ctx.output_dir / relative).is_file()
            },
        },
        index_path,
    )
    paths["index"] = "evidence/index.json"
    return paths


def _run_common(
    args: argparse.Namespace,
    mode: str,
    task: dict[str, Any] | None = None,
) -> int:
    try:
        project = find_project(args.project)
    except ProjectError as exc:
        print(f"ue-audit: {exc}", file=sys.stderr)
        return 3

    try:
        out_dir = _resolve_out_dir(args, project.root, project.name)
    except (OSError, ValueError) as exc:
        print(f"ue-audit: {exc}", file=sys.stderr)
        return 3

    engine = resolve_engine_version(project, args.engine or None)
    try:
        manifest_before = build_manifest(
            project,
            max_hash_bytes=int(args.max_hash_mb * 1024 * 1024),
        )
    except OSError as exc:
        print(f"ue-audit: cannot build project manifest: {exc}", file=sys.stderr)
        return 4

    baseline = None
    diff = None
    if args.baseline:
        try:
            baseline = load_baseline(args.baseline)
            diff = diff_manifests(
                baseline, manifest_before, include_metadata=not args.ignore_mtime
            )
        except (BaselineError, OSError, ValueError) as exc:
            print(f"ue-audit: {exc}", file=sys.stderr)
            return 3

    if args.save_baseline:
        try:
            saved = write_baseline(args.save_baseline, manifest_before)
            if not args.quiet:
                print(f"baseline written: {saved}")
        except OSError as exc:
            print(f"ue-audit: cannot write baseline: {exc}", file=sys.stderr)
            return 4

    live_bridge, bridge_error = _connect_live(args)
    ctx = _make_context(
        args, project, engine, manifest_before, baseline, diff, out_dir, live_bridge, bridge_error
    )

    watch_roots = [
        project.root / name
        for name in ("Content", "Config", "Source", "Plugins")
        if (project.root / name).is_dir()
    ]
    watcher = None
    watch_snapshot: dict[str, Any] | None = None
    if ctx.options.watch_files:
        watcher = DirectoryWatcher(watch_roots).start()
        time.sleep(0.15)

    try:
        checks = [
            check_project_structure(ctx),
            check_baseline_diff(ctx),
            check_abnormal_files(ctx),
            check_git(ctx),
            check_packaging(ctx),
            check_logs(ctx),
            check_health(ctx),
            check_blueprint_status(ctx),
            check_datatables(ctx),
            check_widgets(ctx),
            check_materials(ctx),
            check_animbp(ctx),
            check_pie(ctx),
        ]
        if mode == "verify":
            checks.append(check_task_changes(ctx, task))

        try:
            manifest_after = build_manifest(
                project,
                max_hash_bytes=int(args.max_hash_mb * 1024 * 1024),
            )
        except OSError as exc:
            print(f"ue-audit: cannot build post-audit manifest: {exc}", file=sys.stderr)
            return 4
    finally:
        if watcher is not None:
            watcher.stop()
            watch_snapshot = watcher.snapshot()
        else:
            watch_snapshot = {"available": False, "reason": "disabled"}

    proof = build_readonly_proof(manifest_before, manifest_after, watch_snapshot)
    checks.append(check_readonly_proof(ctx, proof))
    checks.append(check_write_monitor(ctx, proof))

    report = Report(
        mode=mode,
        project=project.to_dict(),
        engine=engine,
        baseline=baseline_info(args.baseline, baseline) if baseline is not None else None,
        checks=checks,
        readonly_proof=proof,
        limitations=list(DEFAULT_LIMITATIONS),
        fail_on=args.fail_on,
        run_id=new_run_id(),
        generated_at=utc_now(),
    )
    checks_data = [check.to_dict() for check in checks]
    evidence = _write_evidence(
        ctx,
        manifest_before,
        manifest_after,
        diff if diff is not None else {"reason": "no_baseline"},
        proof,
        checks_data,
        watch_snapshot,
    )
    report.evidence = evidence
    report_data = report.to_dict()

    # Render after evidence paths are known so report.json includes them.
    report_paths = write_reports(report, out_dir, args.format.split(","))

    if args.json:
        print(json.dumps(report_data, ensure_ascii=False, indent=2))
    elif args.quiet:
        print(out_dir)
    else:
        summary = report_data["summary"]
        print(f"ue-audit {mode}: {project.name}")
        print(
            "  blockers={blocker} errors={error} warnings={warning} infos={info}".format(
                **summary["severity"]
            )
        )
        print(f"  checks: " + ", ".join(f"{check.check_id}={check.status.value}" for check in checks))
        print(f"  output: {out_dir}")
        for name, path in report_paths.items():
            print(f"  {name}: {path}")

    return report.exit_code()


def run_audit(args: argparse.Namespace) -> int:
    return _run_common(args, mode="audit")


def run_verify(args: argparse.Namespace) -> int:
    try:
        task = load_task_manifest(args.task)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ue-audit: cannot read task manifest: {exc}", file=sys.stderr)
        return 3
    if not args.baseline:
        print(
            "ue-audit: verify requires --baseline so the task can be compared to a before-change manifest.",
            file=sys.stderr,
        )
        return 3
    return _run_common(args, mode="verify", task=task)


def run_doctor(args: argparse.Namespace) -> int:
    try:
        project = find_project(args.project)
    except ProjectError as exc:
        print(f"ue-audit: {exc}", file=sys.stderr)
        return 3
    engine = resolve_engine_version(project, args.engine or None)
    try:
        manifest = build_manifest(project)
    except OSError as exc:
        print(f"ue-audit: cannot build manifest: {exc}", file=sys.stderr)
        return 4

    result: dict[str, Any] = {
        "ok": True,
        "project": project.to_dict(),
        "engine": engine,
        "manifest": manifest_summary(manifest),
        "bridge": None,
    }
    if args.live:
        token = read_token(args.token or None)
        wrapper = ReadOnlyBridge(
            BridgeClient(host=args.bridge_host, port=args.bridge_port, token=token)
        )
        try:
            health = wrapper.health()
            result["bridge"] = {"ok": True, "health": health}
            if not health.get("bridge_loaded"):
                result["ok"] = False
        except Exception as exc:  # noqa: BLE001
            result["bridge"] = {"ok": False, "error": str(exc)}
            result["ok"] = False

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"project: {project.name}")
        print(f"root: {project.root}")
        print(f"engine: {engine.get('engine_version') or 'unknown'}")
        print(
            f"manifest: {result['manifest']['file_count']} files, "
            f"{result['manifest']['total_human']}, sha256={result['manifest']['manifest_sha256'][:16]}"
        )
        if result["bridge"] is not None:
            print(f"bridge: {result['bridge']}")
    return 0 if result["ok"] else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        return int(args.func(args))
    except KeyboardInterrupt:
        print("ue-audit: interrupted", file=sys.stderr)
        return 130
    except Exception as exc:  # noqa: BLE001 - CLI boundary
        print(f"ue-audit: unexpected error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 4


def version() -> str:
    return TOOL_VERSION
