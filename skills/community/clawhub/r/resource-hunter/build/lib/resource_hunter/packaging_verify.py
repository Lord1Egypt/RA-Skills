from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
import zipfile
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .common import dump_json
from .errors import ResourceHunterError
from . import packaging_gate, packaging_report


PACKAGING_BASELINE_VERIFY_SCHEMA_VERSION = 1
PACKAGING_BASELINE_VERIFY_BUNDLE_SCHEMA_VERSION = 1
_VERIFY_BUNDLE_MANIFEST_NAME = "bundle-manifest.json"
_VERIFY_BUNDLE_DOWNLOAD_ROOT = "download"
_SAVED_OUTPUT_ORDER = (
    "report_json",
    "report_text",
    "gate_json",
    "gate_text",
    "verify_json",
    "verify_text",
    "bundle_manifest",
    "output_archive",
)


class PackagingBaselineVerifyError(ResourceHunterError):
    def __init__(self, message: str, *, download_payload: Mapping[str, Any] | None = None) -> None:
        super().__init__(message)
        self.download_payload = dict(download_payload) if isinstance(download_payload, Mapping) else {}


def _verify_status(payload: Mapping[str, Any]) -> str:
    if payload.get("error"):
        return "error"
    if payload.get("ok") is True:
        return "ok"
    return "drift"


def _copy_mapping(value: object) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        return {}
    return dict(value)


def _optional_copy_mapping(value: object) -> dict[str, Any] | None:
    payload = _copy_mapping(value)
    return payload or None


def _verify_output_paths(output_dir: Path) -> dict[str, Path]:
    return {
        "report_json": output_dir / "report.json",
        "report_text": output_dir / "report.txt",
        "gate_json": output_dir / "gate.json",
        "gate_text": output_dir / "gate.txt",
        "verify_json": output_dir / "verify.json",
        "verify_text": output_dir / "verify.txt",
    }


def _prepare_managed_download_dir(download_dir: Path) -> Path:
    if download_dir.exists():
        shutil.rmtree(download_dir)
    download_dir.parent.mkdir(parents=True, exist_ok=True)
    return download_dir


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _verify_bundle_manifest_path(output_dir: Path) -> Path:
    return output_dir / _VERIFY_BUNDLE_MANIFEST_NAME


def _download_bundle_members(download_payload: Mapping[str, Any]) -> list[tuple[str, Path]]:
    download_dir_value = download_payload.get("download_dir")
    if download_dir_value is None:
        return []
    download_dir = Path(str(download_dir_value)).resolve()
    if not download_dir.is_dir():
        return []
    members: list[tuple[str, Path]] = []
    for path in sorted(download_dir.rglob("*")):
        if not path.is_file():
            continue
        relative_path = path.relative_to(download_dir).as_posix()
        members.append((f"{_VERIFY_BUNDLE_DOWNLOAD_ROOT}/{relative_path}", path))
    return members


def _build_verify_bundle_manifest(
    payload: Mapping[str, Any],
    *,
    output_dir: Path,
    saved_outputs: Mapping[str, Any],
    download_bundle_members: Sequence[str] | None = None,
) -> dict[str, Any]:
    bundle_members = [
        Path(str(saved_outputs[key])).name
        for key in _SAVED_OUTPUT_ORDER
        if key in saved_outputs and key != "output_archive"
    ]
    resolved_download_bundle_members = [str(member) for member in (download_bundle_members or []) if str(member).strip()]
    bundle_members.extend(resolved_download_bundle_members)
    manifest: dict[str, Any] = {
        "bundle_schema_version": PACKAGING_BASELINE_VERIFY_BUNDLE_SCHEMA_VERSION,
        "verify_schema_version": payload.get("verify_schema_version"),
        "created_at": _utc_now_iso(),
        "status": _verify_status(payload),
        "ok": payload.get("ok") is True,
        "output_dir": str(output_dir.resolve()),
        "saved_outputs": dict(saved_outputs),
        "bundle_members": bundle_members,
    }
    if resolved_download_bundle_members:
        manifest["download_bundle_members"] = resolved_download_bundle_members
        manifest["download_bundle_member_count"] = len(resolved_download_bundle_members)
    for key in (
        "report_ok",
        "report_failure_count",
        "gate_ok",
        "gate_failure_count",
        "report_failures",
        "error",
    ):
        if key in payload:
            manifest[key] = payload.get(key)
    download = _optional_copy_mapping(payload.get("download"))
    if download is not None:
        manifest["download"] = download
    return manifest


def _write_verify_bundle_archive(
    archive_path: Path,
    bundle_members: Mapping[str, Path],
    *,
    download_bundle_members: Sequence[tuple[str, Path]] | None = None,
) -> None:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for key in _SAVED_OUTPUT_ORDER:
            if key == "output_archive":
                continue
            path = bundle_members.get(key)
            if path is None:
                continue
            archive.write(path, arcname=path.name)
        for arcname, path in download_bundle_members or []:
            archive.write(path, arcname=arcname)


def _persist_verify_outputs(
    payload: dict[str, Any],
    output_dir: Path,
    *,
    output_archive: str | Path | None = None,
    archive_downloads: bool = False,
) -> None:
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths = _verify_output_paths(output_dir)
    manifest_path = _verify_bundle_manifest_path(output_dir)

    report_payload = payload.get("report") if isinstance(payload.get("report"), Mapping) else None
    gate_payload = payload.get("gate") if isinstance(payload.get("gate"), Mapping) else None

    saved_outputs: dict[str, str] = {
        "verify_json": str(output_paths["verify_json"].resolve()),
        "verify_text": str(output_paths["verify_text"].resolve()),
        "bundle_manifest": str(manifest_path.resolve()),
    }
    bundle_members: dict[str, Path] = {
        "verify_json": output_paths["verify_json"],
        "verify_text": output_paths["verify_text"],
        "bundle_manifest": manifest_path,
    }

    if report_payload is not None:
        saved_outputs["report_json"] = str(output_paths["report_json"].resolve())
        saved_outputs["report_text"] = str(output_paths["report_text"].resolve())
        bundle_members["report_json"] = output_paths["report_json"]
        bundle_members["report_text"] = output_paths["report_text"]
    if gate_payload is not None:
        saved_outputs["gate_json"] = str(output_paths["gate_json"].resolve())
        saved_outputs["gate_text"] = str(output_paths["gate_text"].resolve())
        bundle_members["gate_json"] = output_paths["gate_json"]
        bundle_members["gate_text"] = output_paths["gate_text"]

    archive_path = Path(output_archive).resolve() if output_archive is not None else None
    if archive_downloads and archive_path is None:
        raise PackagingBaselineVerifyError("--archive-downloads requires --output-archive")
    if archive_path is not None:
        saved_outputs["output_archive"] = str(archive_path)

    download_payload = payload.get("download") if isinstance(payload.get("download"), Mapping) else {}
    download_bundle_members = _download_bundle_members(download_payload) if archive_downloads else []

    payload["output_dir"] = str(output_dir)
    payload["saved_outputs"] = saved_outputs

    if report_payload is not None:
        output_paths["report_json"].write_text(dump_json(report_payload), encoding="utf-8")
        output_paths["report_text"].write_text(
            packaging_report.format_packaging_baseline_report_text(report_payload),
            encoding="utf-8",
        )
    if gate_payload is not None:
        output_paths["gate_json"].write_text(dump_json(gate_payload), encoding="utf-8")
        output_paths["gate_text"].write_text(
            packaging_gate.format_packaging_baseline_gate_text(gate_payload),
            encoding="utf-8",
        )

    manifest_payload = _build_verify_bundle_manifest(
        payload,
        output_dir=output_dir,
        saved_outputs=saved_outputs,
        download_bundle_members=[arcname for arcname, _ in download_bundle_members],
    )
    manifest_path.write_text(dump_json(manifest_payload), encoding="utf-8")
    output_paths["verify_json"].write_text(dump_json(payload), encoding="utf-8")
    output_paths["verify_text"].write_text(format_packaging_baseline_verify_text(payload), encoding="utf-8")

    if archive_path is not None:
        _write_verify_bundle_archive(
            archive_path,
            bundle_members,
            download_bundle_members=download_bundle_members,
        )


def build_packaging_baseline_verify_payload(
    report_payload: Mapping[str, Any],
    gate_payload: Mapping[str, Any],
) -> dict[str, Any]:
    report_failures = packaging_report.packaging_baseline_report_requirement_failures(report_payload)
    gate_failures = _failure_messages(gate_payload.get("failures"))
    download_payload = _optional_copy_mapping(report_payload.get("download"))
    gate_ok = gate_payload.get("ok") is True
    payload: dict[str, Any] = {
        "verify_schema_version": PACKAGING_BASELINE_VERIFY_SCHEMA_VERSION,
        "status": "ok" if not report_failures and gate_ok else "drift",
        "ok": not report_failures and gate_ok,
        "report_ok": not report_failures,
        "report_failure_count": len(report_failures),
        "report_failures": list(report_failures),
        "gate_ok": gate_ok,
        "gate_failure_count": int(gate_payload.get("failure_count") or 0),
        "failure_overlap": _failure_overlap_payload(
            report_failures,
            gate_failures,
            report_payload=report_payload,
        ),
        "report": dict(report_payload),
        "gate": dict(gate_payload),
    }
    if download_payload is not None:
        payload["download"] = download_payload
    return payload


def build_packaging_baseline_verify_error_payload(
    error: str,
    *,
    download_payload: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "verify_schema_version": PACKAGING_BASELINE_VERIFY_SCHEMA_VERSION,
        "status": "error",
        "ok": False,
        "error": error,
    }
    resolved_download_payload = _optional_copy_mapping(download_payload)
    if resolved_download_payload is not None:
        payload["download"] = resolved_download_payload
    return payload


def _saved_outputs_text(saved_outputs: Mapping[str, Any]) -> list[str]:
    lines = ["Saved outputs:"]
    for key in _SAVED_OUTPUT_ORDER:
        value = saved_outputs.get(key)
        if value:
            lines.append(f"- {key}: {value}")
    return lines


def _failure_messages(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    messages: list[str] = []
    seen: set[str] = set()
    for failure in value:
        message = str(failure or "").strip()
        if not message or message in seen:
            continue
        seen.add(message)
        messages.append(message)
    return messages


def _report_artifact_contexts(report_payload: Mapping[str, Any]) -> list[dict[str, str]]:
    report_type = report_payload.get("report_type")
    if report_type == "aggregate":
        artifacts = report_payload.get("artifacts")
        if not isinstance(artifacts, list):
            return []
    else:
        artifacts = [report_payload]

    contexts: list[dict[str, str]] = []
    seen_paths: set[str] = set()
    for artifact in artifacts:
        if not isinstance(artifact, Mapping):
            continue
        annotated_artifact = packaging_report._annotated_artifact_report(artifact)
        artifact_path = str(annotated_artifact.get("artifact_path") or "").strip()
        if not artifact_path or artifact_path in seen_paths:
            continue
        seen_paths.add(artifact_path)
        artifact_label = packaging_report._artifact_group_label(artifact_path)
        artifact_display_label = str(
            annotated_artifact.get("artifact_matrix_label")
            or annotated_artifact.get("artifact_name")
            or artifact_label
        )
        contexts.append(
            {
                "artifact_path": artifact_path,
                "artifact_label": artifact_label,
                "artifact_display_label": artifact_display_label,
            }
        )

    return sorted(contexts, key=lambda context: len(context["artifact_path"]), reverse=True)


def _failure_group_summary(
    failures: Sequence[str],
    *,
    report_payload: Mapping[str, Any],
) -> list[dict[str, Any]]:
    artifact_contexts = _report_artifact_contexts(report_payload)
    grouped_failures: dict[str, dict[str, Any]] = {}
    summary: list[dict[str, Any]] = []

    for failure in failures:
        raw_failure = str(failure or "").strip()
        if not raw_failure:
            continue

        failure_message = raw_failure
        artifact_path: str | None = None
        artifact_label: str | None = None
        artifact_display_label: str | None = None
        for context in artifact_contexts:
            prefix = f"{context['artifact_path']}: "
            if not raw_failure.startswith(prefix):
                continue
            artifact_path = context["artifact_path"]
            artifact_label = context["artifact_label"]
            artifact_display_label = context["artifact_display_label"]
            failure_message = raw_failure[len(prefix) :].strip()
            break

        normalized_message = packaging_report._requirement_failure_message(failure_message) or failure_message
        group = grouped_failures.get(normalized_message)
        if group is None:
            group = {
                "message": normalized_message,
                "failure_count": 0,
                "raw_failures": [],
                "artifact_count": 0,
                "artifact_labels": [],
                "artifact_display_labels": [],
                "artifact_paths": [],
            }
            grouped_failures[normalized_message] = group
            summary.append(group)

        group["failure_count"] += 1
        if raw_failure not in group["raw_failures"]:
            group["raw_failures"].append(raw_failure)
        if artifact_path is None:
            continue
        if artifact_label not in group["artifact_labels"]:
            group["artifact_labels"].append(artifact_label)
        if artifact_display_label not in group["artifact_display_labels"]:
            group["artifact_display_labels"].append(artifact_display_label)
        if artifact_path not in group["artifact_paths"]:
            group["artifact_paths"].append(artifact_path)
        group["artifact_count"] = len(group["artifact_paths"])

    return summary


def _failure_overlap_payload(
    report_failures: Sequence[str],
    gate_failures: Sequence[str],
    *,
    report_payload: Mapping[str, Any],
) -> dict[str, Any]:
    report_unique = _failure_messages(list(report_failures))
    gate_unique = _failure_messages(list(gate_failures))
    report_lookup = set(report_unique)
    gate_lookup = set(gate_unique)
    shared_failures = [failure for failure in report_unique if failure in gate_lookup]
    report_only_failures = [failure for failure in report_unique if failure not in gate_lookup]
    gate_only_failures = [failure for failure in gate_unique if failure not in report_lookup]
    return {
        "shared_failure_count": len(shared_failures),
        "shared_failures": shared_failures,
        "shared_failure_groups": _failure_group_summary(shared_failures, report_payload=report_payload),
        "report_only_failure_count": len(report_only_failures),
        "report_only_failures": report_only_failures,
        "report_only_failure_groups": _failure_group_summary(
            report_only_failures,
            report_payload=report_payload,
        ),
        "gate_only_failure_count": len(gate_only_failures),
        "gate_only_failures": gate_only_failures,
        "gate_only_failure_groups": _failure_group_summary(
            gate_only_failures,
            report_payload=report_payload,
        ),
        "report_matches_gate": report_unique == gate_unique,
    }


def _failure_overlap_text(payload: Mapping[str, Any]) -> list[str]:
    overlap = payload.get("failure_overlap") if isinstance(payload.get("failure_overlap"), Mapping) else None
    report = payload.get("report") if isinstance(payload.get("report"), Mapping) else {}
    if overlap is None:
        report_failures = payload.get("report_failures")
        gate = payload.get("gate") if isinstance(payload.get("gate"), Mapping) else {}
        overlap = _failure_overlap_payload(
            report_failures if isinstance(report_failures, list) else [],
            gate.get("failures") if isinstance(gate.get("failures"), list) else [],
            report_payload=report,
        )

    def _group_entries(group_key: str, fallback_key: str) -> list[dict[str, Any]]:
        groups = overlap.get(group_key) if isinstance(overlap.get(group_key), list) else None
        if groups is not None:
            return [dict(group) for group in groups if isinstance(group, Mapping)]
        failures = overlap.get(fallback_key) if isinstance(overlap.get(fallback_key), list) else []
        return _failure_group_summary(failures, report_payload=report)

    shared_groups = _group_entries("shared_failure_groups", "shared_failures")
    report_only_groups = _group_entries("report_only_failure_groups", "report_only_failures")
    gate_only_groups = _group_entries("gate_only_failure_groups", "gate_only_failures")
    if not shared_groups and not report_only_groups and not gate_only_groups:
        return []

    lines = [
        "Failure overlap: "
        f"shared={int(overlap.get('shared_failure_count') or 0)}; "
        f"report_only={int(overlap.get('report_only_failure_count') or 0)}; "
        f"gate_only={int(overlap.get('gate_only_failure_count') or 0)}"
    ]

    def _append_group_lines(header: str, groups: Sequence[Mapping[str, Any]]) -> None:
        if not groups:
            return
        lines.append(header)
        for group in groups:
            message = str(group.get("message") or "").strip()
            if not message:
                continue
            artifact_labels = group.get("artifact_display_labels")
            if isinstance(artifact_labels, list) and artifact_labels:
                artifact_count = int(group.get("artifact_count") or len(artifact_labels))
                artifact_suffix = "artifact" if artifact_count == 1 else "artifacts"
                display_labels = ", ".join(str(label) for label in artifact_labels)
                lines.append(f"- {message} ({artifact_count} {artifact_suffix}: {display_labels})")
                continue
            lines.append(f"- {message}")

    _append_group_lines("Shared report/gate failures:", shared_groups)
    _append_group_lines("Report-only failures:", report_only_groups)
    _append_group_lines("Gate-only failures:", gate_only_groups)
    return lines


def format_packaging_baseline_verify_text(payload: Mapping[str, Any]) -> str:
    status = _verify_status(payload)
    lines = [
        "Resource Hunter packaging baseline verify",
        f"Status: {status}",
    ]
    if payload.get("error"):
        lines.append(f"Error: {payload.get('error')}")
    download = payload.get("download") if isinstance(payload.get("download"), Mapping) else {}
    lines.extend(packaging_gate._github_run_download_lines(download))
    if "report_ok" in payload:
        lines.append(f"Report status: {'ok' if payload.get('report_ok') else 'drift'}")
        lines.append(f"Report failure count: {payload.get('report_failure_count') or 0}")
    if "gate_ok" in payload:
        lines.append(f"Gate status: {'ok' if payload.get('gate_ok') else 'drift'}")
        lines.append(f"Gate failure count: {payload.get('gate_failure_count') or 0}")
    report = payload.get("report") if isinstance(payload.get("report"), Mapping) else {}
    packaging_report._append_artifact_status_summary_lines(lines, report)
    packaging_report._append_requirement_failure_group_lines(lines, report)
    packaging_report._append_capture_diagnostic_group_lines(lines, report)
    packaging_report._append_capture_diagnostic_lines(lines, report)
    lines.extend(_failure_overlap_text(payload))
    saved_outputs = payload.get("saved_outputs") if isinstance(payload.get("saved_outputs"), Mapping) else {}
    if saved_outputs:
        lines.extend(_saved_outputs_text(saved_outputs))
    return "\n".join(lines)


def verify_packaging_baseline_github_run(
    run_id: str,
    *,
    repo: str | None = None,
    github_workflow: str | None = None,
    github_run_list_limit: int | None = None,
    artifact_names: Sequence[str] | None = None,
    artifact_patterns: Sequence[str] | None = None,
    download_dir: str | Path | None = None,
    keep_download_dir: bool = False,
    output_dir: str | Path | None = None,
    output_archive: str | Path | None = None,
    archive_downloads: bool = False,
    required_artifact_count: int | None = None,
) -> dict[str, Any]:
    managed_output_dir = Path(output_dir).resolve() if output_dir is not None else None
    if output_archive is not None and managed_output_dir is None:
        raise PackagingBaselineVerifyError("--output-archive requires --output-dir")
    if archive_downloads and output_archive is None:
        raise PackagingBaselineVerifyError("--archive-downloads requires --output-archive")
    if managed_output_dir is not None:
        managed_output_dir.mkdir(parents=True, exist_ok=True)
    if download_dir is None and managed_output_dir is not None:
        download_dir = _prepare_managed_download_dir(managed_output_dir / "download")
        download_dir_source = "output-dir"
        download_dir_retained = True
    elif download_dir is not None:
        download_dir_source = "argument"
        download_dir_retained = True
    elif keep_download_dir:
        download_dir = Path(tempfile.mkdtemp(prefix="resource-hunter-gh-run-download-"))
        download_dir_source = "temporary"
        download_dir_retained = True
    else:
        download_dir = None
        download_dir_source = "temporary"
        download_dir_retained = False

    def evaluate_from_download_payload(download_payload: Mapping[str, Any]) -> dict[str, Any]:
        artifact_paths = packaging_report.resolve_packaging_baseline_artifact_paths([str(download_payload["download_dir"])])
        resolved_download = packaging_report._attach_download_artifact_resolution(download_payload, artifact_paths)
        report_payload = packaging_report.attach_packaging_baseline_download_payload(
            packaging_report.read_packaging_baseline_reports(artifact_paths),
            download_payload=resolved_download,
        )
        gate_payload = packaging_gate.build_packaging_baseline_gate_payload(
            report_payload,
            required_artifact_count=required_artifact_count,
            download_payload=resolved_download,
        )
        return build_packaging_baseline_verify_payload(report_payload, gate_payload)

    if download_dir is not None:
        try:
            download_payload = packaging_gate._download_packaging_baseline_github_run(
                run_id,
                repo=repo,
                github_workflow=github_workflow,
                github_run_list_limit=github_run_list_limit,
                artifact_names=artifact_names,
                artifact_patterns=artifact_patterns,
                download_dir=download_dir,
                download_dir_source=download_dir_source,
                download_dir_retained=download_dir_retained,
            )
            payload = evaluate_from_download_payload(download_payload)
        except ResourceHunterError as exc:
            raise PackagingBaselineVerifyError(
                str(exc),
                download_payload=getattr(exc, "download_payload", None),
            ) from exc
    else:
        with tempfile.TemporaryDirectory(prefix="resource-hunter-gh-run-download-") as temp_dir:
            try:
                download_payload = packaging_gate._download_packaging_baseline_github_run(
                    run_id,
                    repo=repo,
                    github_workflow=github_workflow,
                    github_run_list_limit=github_run_list_limit,
                    artifact_names=artifact_names,
                    artifact_patterns=artifact_patterns,
                    download_dir=temp_dir,
                    download_dir_source=download_dir_source,
                    download_dir_retained=download_dir_retained,
                )
                payload = evaluate_from_download_payload(download_payload)
            except ResourceHunterError as exc:
                raise PackagingBaselineVerifyError(
                    str(exc),
                    download_payload=getattr(exc, "download_payload", None),
                ) from exc

    if managed_output_dir is not None:
        _persist_verify_outputs(
            payload,
            managed_output_dir,
            output_archive=output_archive,
            archive_downloads=archive_downloads,
        )

    return payload


def verify_packaging_baseline_artifacts(
    paths: Sequence[str | Path] | None = None,
    *,
    output_dir: str | Path | None = None,
    output_archive: str | Path | None = None,
    archive_downloads: bool = False,
    required_artifact_count: int | None = None,
) -> dict[str, Any]:
    managed_output_dir = Path(output_dir).resolve() if output_dir is not None else None
    if output_archive is not None and managed_output_dir is None:
        raise PackagingBaselineVerifyError("--output-archive requires --output-dir")
    if archive_downloads:
        raise PackagingBaselineVerifyError("--archive-downloads requires --github-run")
    if managed_output_dir is not None:
        managed_output_dir.mkdir(parents=True, exist_ok=True)

    try:
        report_payload = packaging_report.read_packaging_baseline_reports(paths)
        gate_payload = packaging_gate.build_packaging_baseline_gate_payload(
            report_payload,
            required_artifact_count=required_artifact_count,
        )
    except ResourceHunterError as exc:
        raise PackagingBaselineVerifyError(str(exc)) from exc

    payload = build_packaging_baseline_verify_payload(report_payload, gate_payload)
    if managed_output_dir is not None:
        _persist_verify_outputs(
            payload,
            managed_output_dir,
            output_archive=output_archive,
            archive_downloads=archive_downloads,
        )
    return payload


def validate_packaging_baseline_verify_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if getattr(args, "github_run", None) and getattr(args, "paths", None):
        parser.error("paths cannot be combined with --github-run")
    if not getattr(args, "github_run", None) and (
        getattr(args, "github_workflow", None)
        or getattr(args, "github_run_list_limit", None)
        or getattr(args, "repo", None)
        or getattr(args, "artifact_names", None)
        or getattr(args, "artifact_patterns", None)
        or getattr(args, "download_dir", None)
        or getattr(args, "keep_download_dir", False)
    ):
        parser.error(
            "--github-workflow, --github-run-list-limit, --repo, --artifact-name, --artifact-pattern, --download-dir, and --keep-download-dir require --github-run"
        )
    if getattr(args, "archive_downloads", False) and not getattr(args, "github_run", None):
        parser.error("--archive-downloads requires --github-run")


def _positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid positive integer value: {value!r}") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("value must be >= 1")
    return parsed


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="resource-hunter-packaging-baseline-verify",
        description=(
            "Verify packaging-baseline artifacts from either retained files/directories/archives or a single "
            "GitHub Actions run while keeping report/gate outputs anchored to the same resolved artifact set."
        ),
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help=(
            "artifact file(s), .zip archive(s), or directories to scan recursively for packaging-baseline.json and nested .zip archives; "
            "defaults to artifacts/packaging-baseline/packaging-baseline.json when --github-run is omitted"
        ),
    )
    parser.add_argument(
        "--github-run",
        help=(
            "download packaging-baseline artifacts from a GitHub Actions run with `gh run download`; "
            "pass `latest` to auto-select the most recent completed resource-hunter-ci run"
        ),
    )
    parser.add_argument(
        "--github-workflow",
        help=(
            "workflow name passed to `gh run list --workflow` when --github-run latest is used; "
            f"defaults to {packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW}"
        ),
    )
    parser.add_argument(
        "--github-run-list-limit",
        type=_positive_int,
        help=(
            "max completed runs to scan when --github-run latest resolves a workflow-filtered run or "
            f"artifact-discovery fallback; defaults to {packaging_gate._GITHUB_RUN_LIST_LIMIT}"
        ),
    )
    parser.add_argument(
        "--repo",
        help=(
            "repository passed through to `gh run download --repo`; defaults to GITHUB_REPOSITORY, "
            "then the git origin remote, then the current gh repository context"
        ),
    )
    parser.add_argument(
        "--artifact-name",
        action="append",
        dest="artifact_names",
        help="artifact name to download from --github-run; may be passed multiple times",
    )
    parser.add_argument(
        "--artifact-pattern",
        action="append",
        dest="artifact_patterns",
        help="artifact glob pattern to download from --github-run; may be passed multiple times",
    )
    parser.add_argument(
        "--download-dir",
        help=(
            "directory passed to `gh run download --dir`; defaults to <output-dir>/download when --output-dir is set, "
            "otherwise a temporary directory"
        ),
    )
    parser.add_argument(
        "--keep-download-dir",
        action="store_true",
        help="retain the temporary download directory created for verification when --download-dir is omitted",
    )
    parser.add_argument(
        "--output-dir",
        help="write report.json, report.txt, gate.json, gate.txt, verify.json, and verify.txt into this directory",
    )
    parser.add_argument(
        "--output-archive",
        help=(
            "write a zip bundle containing the saved report.*, gate.*, verify.*, and bundle-manifest.json outputs; "
            "requires --output-dir"
        ),
    )
    parser.add_argument(
        "--archive-downloads",
        action="store_true",
        help=(
            "include the retained downloaded artifact tree under download/ inside --output-archive; "
            "requires --output-archive"
        ),
    )
    parser.add_argument("--json", action="store_true", help="emit the top-level verification payload as JSON")
    parser.add_argument(
        "--require-artifact-count",
        type=_positive_int,
        help="require exactly N discovered packaging-baseline artifacts before verification passes",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else sys.argv[1:])
    validate_packaging_baseline_verify_args(parser, args)
    if args.output_archive and not args.output_dir:
        parser.error("--output-archive requires --output-dir")
    if args.archive_downloads and not args.output_archive:
        parser.error("--archive-downloads requires --output-archive")
    try:
        if args.github_run:
            payload = verify_packaging_baseline_github_run(
                args.github_run,
                repo=args.repo,
                github_workflow=args.github_workflow,
                github_run_list_limit=args.github_run_list_limit,
                artifact_names=args.artifact_names,
                artifact_patterns=args.artifact_patterns,
                download_dir=args.download_dir,
                keep_download_dir=args.keep_download_dir,
                output_dir=args.output_dir,
                output_archive=args.output_archive,
                archive_downloads=args.archive_downloads,
                required_artifact_count=args.require_artifact_count,
            )
        else:
            payload = verify_packaging_baseline_artifacts(
                args.paths,
                output_dir=args.output_dir,
                output_archive=args.output_archive,
                archive_downloads=args.archive_downloads,
                required_artifact_count=args.require_artifact_count,
            )
    except ResourceHunterError as exc:
        payload = build_packaging_baseline_verify_error_payload(
            str(exc),
            download_payload=getattr(exc, "download_payload", None),
        )
        if args.output_dir:
            _persist_verify_outputs(
                payload,
                Path(args.output_dir),
                output_archive=args.output_archive,
                archive_downloads=args.archive_downloads,
            )
        if args.json:
            print(dump_json(payload))
        else:
            print(format_packaging_baseline_verify_text(payload))
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(dump_json(payload))
    else:
        print(format_packaging_baseline_verify_text(payload))

    if payload.get("gate_ok") is False:
        gate = payload.get("gate") if isinstance(payload.get("gate"), Mapping) else {}
        failures = gate.get("failures") if isinstance(gate.get("failures"), list) else []
        for failure in failures:
            print(failure, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "PACKAGING_BASELINE_VERIFY_SCHEMA_VERSION",
    "PACKAGING_BASELINE_VERIFY_BUNDLE_SCHEMA_VERSION",
    "PackagingBaselineVerifyError",
    "build_packaging_baseline_verify_error_payload",
    "build_packaging_baseline_verify_payload",
    "format_packaging_baseline_verify_text",
    "main",
    "validate_packaging_baseline_verify_args",
    "verify_packaging_baseline_artifacts",
    "verify_packaging_baseline_github_run",
]
