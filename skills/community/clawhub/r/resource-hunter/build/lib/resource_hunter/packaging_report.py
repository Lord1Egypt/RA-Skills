from __future__ import annotations

import json
import os
import sys
import tempfile
import zipfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import ResourceHunterError


PACKAGING_BASELINE_REPORT_SCHEMA_VERSION = 1
DEFAULT_PACKAGING_BASELINE_ARTIFACT = Path("artifacts") / "packaging-baseline" / "packaging-baseline.json"
_PACKAGING_BASELINE_ARTIFACT_NAME = DEFAULT_PACKAGING_BASELINE_ARTIFACT.name


class PackagingBaselineReportError(ResourceHunterError):
    def __init__(self, message: str, *, download_payload: Mapping[str, Any] | None = None) -> None:
        super().__init__(message)
        self.download_payload = _copy_mapping(download_payload)


@dataclass(frozen=True)
class _ArtifactRef:
    display_path: str
    filesystem_path: Path
    zip_member: str | None = None


def _artifact_display_path(path: str | Path, *, zip_member: str | None = None) -> str:
    if zip_member is None:
        archive_member_ref = _split_archive_member_path(path)
        if archive_member_ref is not None:
            archive_path, normalized_member = archive_member_ref
            return _artifact_display_path(archive_path, zip_member=normalized_member)
    resolved_path = Path(path).resolve()
    if zip_member is None:
        return str(resolved_path)
    normalized_member = zip_member.replace("\\", "/").lstrip("/")
    return f"{resolved_path}!/{normalized_member}"


def _copy_mapping(value: object) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        return {}
    return dict(value)


def _split_archive_member_path(path: str | Path) -> tuple[Path, str] | None:
    raw_path = str(path)
    marker_index = raw_path.find("!")
    if marker_index < 0:
        return None
    archive_path = raw_path[:marker_index]
    if not archive_path.lower().endswith(".zip"):
        return None
    member_path = raw_path[marker_index + 1 :].lstrip("/\\")
    resolved_archive_path = Path(archive_path).resolve()
    if not member_path:
        raise ResourceHunterError(
            f"Packaging baseline archive {resolved_archive_path} must include a member path after '!'."
        )
    return resolved_archive_path, member_path.replace("\\", "/")


def _artifact_key(display_path: str) -> str:
    archive_path, marker, member = display_path.partition("!/")
    if not marker:
        return os.path.normcase(display_path)
    return f"{os.path.normcase(archive_path)}!/{member.lower()}"


def _artifact_sort_key(artifact_ref: _ArtifactRef) -> str:
    return _artifact_key(artifact_ref.display_path)


def _zip_artifact_refs(archive_path: str | Path) -> list[_ArtifactRef]:
    resolved_archive_path = Path(archive_path).resolve()
    try:
        with zipfile.ZipFile(resolved_archive_path) as archive:
            member_names = sorted(
                member_name
                for member_name in archive.namelist()
                if not member_name.endswith("/") and Path(member_name).name == _PACKAGING_BASELINE_ARTIFACT_NAME
            )
    except (OSError, zipfile.BadZipFile) as exc:
        raise ResourceHunterError(f"Unable to read packaging baseline archive {resolved_archive_path}: {exc}") from exc

    return [
        _ArtifactRef(
            display_path=_artifact_display_path(resolved_archive_path, zip_member=member_name),
            filesystem_path=resolved_archive_path,
            zip_member=member_name,
        )
        for member_name in member_names
    ]


def _read_artifact_text(artifact_ref: _ArtifactRef) -> str:
    if artifact_ref.zip_member is None:
        try:
            return artifact_ref.filesystem_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ResourceHunterError(
                f"Unable to read packaging baseline artifact {artifact_ref.display_path}: {exc}"
            ) from exc

    try:
        with zipfile.ZipFile(artifact_ref.filesystem_path) as archive:
            with archive.open(artifact_ref.zip_member, "r") as handle:
                raw_bytes = handle.read()
    except (OSError, KeyError, RuntimeError, zipfile.BadZipFile) as exc:
        raise ResourceHunterError(
            f"Unable to read packaging baseline artifact {artifact_ref.display_path}: {exc}"
        ) from exc

    try:
        return raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ResourceHunterError(
            f"Packaging baseline artifact {artifact_ref.display_path} is not valid UTF-8: {exc}"
        ) from exc


def _load_packaging_baseline_payload_from_ref(artifact_ref: _ArtifactRef) -> dict[str, Any]:
    raw_text = _read_artifact_text(artifact_ref)
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ResourceHunterError(
            f"Packaging baseline artifact {artifact_ref.display_path} is not valid JSON: {exc}"
        ) from exc
    if not isinstance(payload, dict):
        raise ResourceHunterError(f"Packaging baseline artifact {artifact_ref.display_path} must contain a JSON object.")
    _baseline_captures(payload, artifact_path=artifact_ref.display_path)
    return payload


def _coerce_artifact_ref(path: str | Path) -> _ArtifactRef:
    archive_member_ref = _split_archive_member_path(path)
    if archive_member_ref is not None:
        archive_path, zip_member = archive_member_ref
        return _ArtifactRef(
            display_path=_artifact_display_path(archive_path, zip_member=zip_member),
            filesystem_path=archive_path,
            zip_member=zip_member,
        )
    display_path = _artifact_display_path(path)
    return _ArtifactRef(display_path=display_path, filesystem_path=Path(path).resolve())


def _directory_artifact_refs(directory_path: str | Path) -> list[_ArtifactRef]:
    resolved_directory = Path(directory_path).resolve()
    matches = [
        _ArtifactRef(display_path=_artifact_display_path(path), filesystem_path=path.resolve())
        for path in resolved_directory.rglob(_PACKAGING_BASELINE_ARTIFACT_NAME)
        if path.is_file()
    ]
    archive_paths = sorted(
        path.resolve()
        for path in resolved_directory.rglob("*")
        if path.is_file() and path.suffix.lower() == ".zip"
    )
    for archive_path in archive_paths:
        matches.extend(_zip_artifact_refs(archive_path))
    return sorted(matches, key=_artifact_sort_key)


def _resolve_packaging_baseline_artifact_refs(
    raw_paths: Sequence[str | Path] | None = None, *, allow_empty: bool = False
) -> list[_ArtifactRef]:
    requested_paths = list(raw_paths or [])
    if not requested_paths:
        requested_paths = [DEFAULT_PACKAGING_BASELINE_ARTIFACT]

    artifact_refs: list[_ArtifactRef] = []
    empty_directories: list[Path] = []
    empty_archives: list[Path] = []
    seen: set[str] = set()
    for raw_path in requested_paths:
        candidate = Path(raw_path).resolve()
        if candidate.is_dir():
            matches = _directory_artifact_refs(candidate)
            if not matches:
                empty_directories.append(candidate)
                continue
            for match in matches:
                key = _artifact_key(match.display_path)
                if key in seen:
                    continue
                seen.add(key)
                artifact_refs.append(match)
            continue
        if candidate.suffix.lower() == ".zip":
            matches = _zip_artifact_refs(candidate)
            if not matches:
                empty_archives.append(candidate)
                continue
            for match in matches:
                key = _artifact_key(match.display_path)
                if key in seen:
                    continue
                seen.add(key)
                artifact_refs.append(match)
            continue
        key = _artifact_key(_artifact_display_path(candidate))
        if key in seen:
            continue
        seen.add(key)
        artifact_refs.append(_ArtifactRef(display_path=_artifact_display_path(candidate), filesystem_path=candidate))

    if allow_empty and not artifact_refs and (empty_directories or empty_archives):
        return []
    if empty_directories:
        directories = ", ".join(str(path) for path in empty_directories)
        raise ResourceHunterError(f"No packaging-baseline.json artifacts found under {directories}.")
    if empty_archives:
        archives = ", ".join(str(path) for path in empty_archives)
        raise ResourceHunterError(f"No packaging-baseline.json artifacts found in archive(s) {archives}.")
    if not artifact_refs:
        raise ResourceHunterError("No packaging baseline artifacts were requested.")
    return artifact_refs


def _baseline_captures(
    payload: Mapping[str, Any],
    *,
    artifact_path: str,
) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    passing_capture = payload.get("passing_capture")
    blocked_capture = payload.get("blocked_capture")
    if not isinstance(passing_capture, Mapping) or not isinstance(blocked_capture, Mapping):
        raise ResourceHunterError(
            f"Packaging baseline artifact {artifact_path} does not contain passing_capture and blocked_capture entries."
        )
    return passing_capture, blocked_capture


def _report_capture(
    *,
    capture_name: str,
    label: str,
    capture: Mapping[str, Any],
) -> dict[str, Any]:
    expected_outcome = capture.get("expected_outcome")
    if not isinstance(expected_outcome, Mapping):
        expected_outcome = {}
    expectation_drift = capture.get("expectation_drift")
    if not isinstance(expectation_drift, list):
        expectation_drift = []
    report_capture: dict[str, Any] = {
        "name": capture_name,
        "label": label,
        "path": capture.get("path"),
        "project_root": capture.get("project_root"),
        "project_root_source": capture.get("project_root_source"),
        "expected_outcome": dict(expected_outcome),
        "actual": {
            "doctor_packaging_ready": capture.get("doctor_packaging_ready"),
            "packaging_smoke_ok": capture.get("packaging_smoke_ok"),
            "failed_step": capture.get("failed_step"),
            "strategy_family": capture.get("strategy_family"),
            "strategy": capture.get("strategy"),
            "reason": capture.get("reason"),
        },
        "matches_expectation": capture.get("matches_expectation"),
        "expectation_drift": expectation_drift,
    }
    requested_project_root = capture.get("requested_project_root")
    if requested_project_root is not None:
        report_capture["requested_project_root"] = requested_project_root
    packaging_python = capture.get("packaging_python")
    if packaging_python is not None:
        report_capture["packaging_python"] = packaging_python
    packaging_python_source = capture.get("packaging_python_source")
    if packaging_python_source is not None:
        report_capture["packaging_python_source"] = packaging_python_source
    packaging_python_auto_selected = capture.get("packaging_python_auto_selected")
    if packaging_python_auto_selected is not None:
        report_capture["packaging_python_auto_selected"] = packaging_python_auto_selected
    diagnostics = _capture_diagnostics(capture)
    if diagnostics:
        report_capture["diagnostics"] = diagnostics
    return report_capture


def _copy_string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        text = str(item or "").strip()
        if text:
            result.append(text)
    return result


def _capture_diagnostics(capture: Mapping[str, Any]) -> dict[str, Any]:
    doctor = capture.get("doctor") if isinstance(capture.get("doctor"), Mapping) else {}
    doctor_packaging = doctor.get("packaging") if isinstance(doctor.get("packaging"), Mapping) else {}
    packaging_smoke = capture.get("packaging_smoke") if isinstance(capture.get("packaging_smoke"), Mapping) else {}
    packaging_smoke_packaging = (
        packaging_smoke.get("packaging") if isinstance(packaging_smoke.get("packaging"), Mapping) else {}
    )

    diagnostics: dict[str, Any] = {}
    packaging_error = doctor_packaging.get("error") or packaging_smoke_packaging.get("error")
    if not packaging_error:
        packaging_error = _infer_packaging_error_from_reason(capture.get("reason"))
    if packaging_error:
        diagnostics["packaging_error"] = str(packaging_error)

    blockers = _copy_string_list(doctor_packaging.get("blockers"))
    if not blockers:
        blockers = _copy_string_list(packaging_smoke_packaging.get("blockers"))
    if blockers:
        diagnostics["packaging_blockers"] = blockers

    bootstrap_build_requirements = _copy_string_list(doctor_packaging.get("bootstrap_build_requirements"))
    if bootstrap_build_requirements:
        diagnostics["bootstrap_build_requirements"] = bootstrap_build_requirements

    for key in ("bootstrap_build_deps_ready", "packaging_smoke_ready_with_bootstrap"):
        value = doctor_packaging.get(key)
        if value is not None:
            diagnostics[key] = value

    return diagnostics


def _infer_packaging_error_from_reason(reason: object) -> str | None:
    reason_text = str(reason or "").strip()
    if not reason_text or "Traceback" not in reason_text:
        return None
    prefix = "Packaging smoke is blocked: "
    if reason_text.startswith(prefix):
        return reason_text[len(prefix) :].strip() or None
    return reason_text


def _normalized_capture_reason(reason: object) -> str | None:
    reason_text = str(reason or "").strip()
    if not reason_text:
        return None
    if "Traceback" not in reason_text:
        return reason_text

    summary_prefix = reason_text.partition("Traceback")[0].rstrip(" :")
    if " via " in summary_prefix:
        summary_prefix = summary_prefix.partition(" via ")[0].rstrip(" :")
    if not summary_prefix:
        return reason_text
    if summary_prefix.endswith((".", "!", "?")):
        return summary_prefix
    return f"{summary_prefix}."


def build_packaging_baseline_report(payload: Mapping[str, Any], *, artifact_path: str | Path) -> dict[str, Any]:
    resolved_path = _artifact_display_path(artifact_path)
    if not isinstance(payload, Mapping):
        raise ResourceHunterError(f"Packaging baseline artifact {resolved_path} must contain a JSON object.")
    passing_capture, blocked_capture = _baseline_captures(payload, artifact_path=resolved_path)
    summary = payload.get("summary") if isinstance(payload.get("summary"), Mapping) else {}
    requirements = payload.get("requirements") if isinstance(payload.get("requirements"), Mapping) else {}
    warnings = payload.get("warnings")
    if not isinstance(warnings, list):
        warnings = []
    failures = requirements.get("failures")
    if not isinstance(failures, list):
        failures = []
    report_payload: dict[str, Any] = {
        "report_schema_version": PACKAGING_BASELINE_REPORT_SCHEMA_VERSION,
        "report_type": "single",
        "artifact_path": resolved_path,
        "artifact_schema_version": payload.get("schema_version"),
        "captured_at": payload.get("captured_at"),
        "output_dir": payload.get("output_dir"),
        "project_root": payload.get("project_root"),
        "project_root_source": payload.get("project_root_source"),
        "blocked_python": payload.get("blocked_python"),
        "summary": {
            "passing_capture_matches_expectation": summary.get("passing_capture_matches_expectation"),
            "blocked_capture_matches_expectation": summary.get("blocked_capture_matches_expectation"),
            "baseline_contract_ok": summary.get("baseline_contract_ok"),
        },
        "requirements": {
            "require_expected_outcomes": requirements.get("require_expected_outcomes"),
            "ok": requirements.get("ok"),
            "failures": failures,
        },
        "warnings": warnings,
        "captures": [
            _report_capture(
                capture_name="passing",
                label="Passing",
                capture=passing_capture,
            ),
            _report_capture(
                capture_name="blocked",
                label="Blocked",
                capture=blocked_capture,
            ),
        ],
    }
    report_payload.update(_artifact_summary_metadata(resolved_path))
    requested_project_root = payload.get("requested_project_root")
    if requested_project_root is not None:
        report_payload["requested_project_root"] = requested_project_root
    capture_diagnostics = _packaging_baseline_report_capture_diagnostics(report_payload)
    if capture_diagnostics:
        report_payload["capture_diagnostics"] = capture_diagnostics
    report_payload["status"] = _artifact_report_status(report_payload)
    report_payload["requirement_failure_count"] = len(failures)
    report_payload["capture_diagnostic_count"] = len(capture_diagnostics)
    return report_payload


def resolve_packaging_baseline_artifact_paths(raw_paths: Sequence[str | Path] | None = None) -> list[str | Path]:
    artifact_refs = _resolve_packaging_baseline_artifact_refs(raw_paths)
    return [
        artifact_ref.display_path if artifact_ref.zip_member is not None else artifact_ref.filesystem_path
        for artifact_ref in artifact_refs
    ]


def _resolved_download_artifact_paths(download_payload: Mapping[str, Any]) -> list[str | Path]:
    download_dir = download_payload.get("download_dir")
    if download_dir is None:
        return []
    artifact_refs = _resolve_packaging_baseline_artifact_refs([str(download_dir)], allow_empty=True)
    return [
        artifact_ref.display_path if artifact_ref.zip_member is not None else artifact_ref.filesystem_path
        for artifact_ref in artifact_refs
    ]


def _attach_download_artifact_resolution(
    download_payload: Mapping[str, Any], artifact_paths: Sequence[str | Path]
) -> dict[str, Any]:
    payload = _copy_mapping(download_payload)
    resolved_paths = [str(artifact_path) for artifact_path in artifact_paths]
    archive_member_count = sum(1 for artifact_path in resolved_paths if "!/" in artifact_path)
    payload["resolved_artifact_count"] = len(resolved_paths)
    payload["resolved_artifact_paths"] = resolved_paths
    payload["resolved_archive_member_count"] = archive_member_count
    payload["resolved_filesystem_artifact_count"] = len(resolved_paths) - archive_member_count
    return payload


def build_packaging_baseline_aggregate_report(report_payloads: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    artifact_reports = [_annotated_artifact_report(report_payload) for report_payload in report_payloads]
    contract_ok_artifact_count = 0
    contract_drift_artifacts: list[str] = []
    requirement_failed_artifacts: list[str] = []
    warnings: list[str] = []
    for report_payload in artifact_reports:
        artifact_path = str(report_payload.get("artifact_path") or "unknown")
        summary = report_payload.get("summary") if isinstance(report_payload.get("summary"), Mapping) else {}
        requirements = (
            report_payload.get("requirements") if isinstance(report_payload.get("requirements"), Mapping) else {}
        )
        artifact_warnings = report_payload.get("warnings")
        if not isinstance(artifact_warnings, list):
            artifact_warnings = []
        if summary.get("baseline_contract_ok") is True:
            contract_ok_artifact_count += 1
        else:
            contract_drift_artifacts.append(artifact_path)
        if requirements.get("ok") is False:
            requirement_failed_artifacts.append(artifact_path)
        warnings.extend(f"{artifact_path}: {warning}" for warning in artifact_warnings)

    artifact_count = len(artifact_reports)
    aggregate_report = {
        "report_schema_version": PACKAGING_BASELINE_REPORT_SCHEMA_VERSION,
        "report_type": "aggregate",
        "summary": {
            "artifact_count": artifact_count,
            "contract_ok_artifact_count": contract_ok_artifact_count,
            "contract_drift_artifact_count": artifact_count - contract_ok_artifact_count,
            "requirement_failed_artifact_count": len(requirement_failed_artifacts),
            "warning_count": len(warnings),
            "all_baseline_contracts_ok": contract_ok_artifact_count == artifact_count,
        },
        "artifacts_with_contract_drift": contract_drift_artifacts,
        "artifacts_with_requirement_failures": requirement_failed_artifacts,
        "warnings": warnings,
        "artifacts": artifact_reports,
    }
    artifact_statuses = _aggregate_artifact_statuses(artifact_reports)
    if artifact_statuses:
        aggregate_report["artifact_statuses"] = artifact_statuses
    requirement_failure_groups = _aggregate_requirement_failure_groups(aggregate_report)
    if requirement_failure_groups:
        aggregate_report["requirement_failure_groups"] = requirement_failure_groups
    capture_diagnostics = _packaging_baseline_report_capture_diagnostics(aggregate_report)
    if capture_diagnostics:
        aggregate_report["capture_diagnostics"] = capture_diagnostics
    capture_diagnostic_groups = _aggregate_capture_diagnostic_groups(aggregate_report)
    if capture_diagnostic_groups:
        aggregate_report["capture_diagnostic_groups"] = capture_diagnostic_groups
    return aggregate_report


def load_packaging_baseline_payload(path: str | Path) -> dict[str, Any]:
    artifact_ref = _coerce_artifact_ref(path)
    if artifact_ref.zip_member is not None:
        return _load_packaging_baseline_payload_from_ref(artifact_ref)

    artifact_path = artifact_ref.filesystem_path
    if artifact_path.suffix.lower() == ".zip":
        artifact_refs = _zip_artifact_refs(artifact_path)
        if not artifact_refs:
            raise ResourceHunterError(f"No packaging-baseline.json artifacts found in archive(s) {artifact_path}.")
        if len(artifact_refs) != 1:
            raise ResourceHunterError(
                f"Packaging baseline archive {artifact_path} contains {len(artifact_refs)} packaging-baseline.json artifacts; "
                "use read_packaging_baseline_reports() when multiple archived artifacts must be aggregated."
            )
        return _load_packaging_baseline_payload_from_ref(artifact_refs[0])
    return _load_packaging_baseline_payload_from_ref(artifact_ref)


def read_packaging_baseline_report(path: str | Path) -> dict[str, Any]:
    artifact_ref = _coerce_artifact_ref(path)
    if artifact_ref.zip_member is not None:
        payload = _load_packaging_baseline_payload_from_ref(artifact_ref)
        return build_packaging_baseline_report(payload, artifact_path=artifact_ref.display_path)

    artifact_path = artifact_ref.filesystem_path
    if artifact_path.suffix.lower() == ".zip":
        artifact_refs = _zip_artifact_refs(artifact_path)
        if not artifact_refs:
            raise ResourceHunterError(f"No packaging-baseline.json artifacts found in archive(s) {artifact_path}.")
        if len(artifact_refs) != 1:
            raise ResourceHunterError(
                f"Packaging baseline archive {artifact_path} contains {len(artifact_refs)} packaging-baseline.json artifacts; "
                "use read_packaging_baseline_reports() when multiple archived artifacts must be aggregated."
            )
        payload = _load_packaging_baseline_payload_from_ref(artifact_refs[0])
        return build_packaging_baseline_report(payload, artifact_path=artifact_refs[0].display_path)
    payload = _load_packaging_baseline_payload_from_ref(artifact_ref)
    return build_packaging_baseline_report(payload, artifact_path=artifact_ref.display_path)


def read_packaging_baseline_reports(paths: Sequence[str | Path] | None = None) -> dict[str, Any]:
    artifact_refs = _resolve_packaging_baseline_artifact_refs(paths)
    report_payloads = [
        build_packaging_baseline_report(
            _load_packaging_baseline_payload_from_ref(artifact_ref),
            artifact_path=artifact_ref.display_path,
        )
        for artifact_ref in artifact_refs
    ]
    if len(report_payloads) == 1:
        return report_payloads[0]
    return build_packaging_baseline_aggregate_report(report_payloads)


def attach_packaging_baseline_download_payload(
    report_payload: Mapping[str, Any], *, download_payload: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    payload = dict(report_payload)
    if download_payload is not None:
        payload["download"] = _copy_mapping(download_payload)
    return payload


def build_packaging_baseline_report_error_payload(
    error: str, *, download_payload: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "report_schema_version": PACKAGING_BASELINE_REPORT_SCHEMA_VERSION,
        "report_type": "error",
        "summary": {},
        "warnings": [],
        "error": error,
    }
    if download_payload is not None:
        payload["download"] = _copy_mapping(download_payload)
    return payload


def _evaluate_downloaded_packaging_baseline_reports(download_payload: Mapping[str, Any]) -> dict[str, Any]:
    artifact_paths = _resolved_download_artifact_paths(download_payload)
    download_payload = _attach_download_artifact_resolution(download_payload, artifact_paths)
    if not artifact_paths:
        raise PackagingBaselineReportError(
            f"No packaging-baseline.json artifacts found under {download_payload['download_dir']}.",
            download_payload=download_payload,
        )
    try:
        report_payload = read_packaging_baseline_reports(artifact_paths)
    except ResourceHunterError as exc:
        raise PackagingBaselineReportError(str(exc), download_payload=download_payload) from exc
    return attach_packaging_baseline_download_payload(report_payload, download_payload=download_payload)


def read_packaging_baseline_reports_from_github_run(
    run_id: str,
    *,
    repo: str | None = None,
    github_workflow: str | None = None,
    github_run_list_limit: int | None = None,
    artifact_names: Sequence[str] | None = None,
    artifact_patterns: Sequence[str] | None = None,
    download_dir: str | Path | None = None,
    keep_download_dir: bool = False,
) -> dict[str, Any]:
    from . import packaging_gate

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
                download_dir_source="argument",
                download_dir_retained=True,
            )
        except ResourceHunterError as exc:
            raise PackagingBaselineReportError(
                str(exc),
                download_payload=getattr(exc, "download_payload", None),
            ) from exc
        return _evaluate_downloaded_packaging_baseline_reports(download_payload)

    if keep_download_dir:
        retained_dir = Path(tempfile.mkdtemp(prefix="resource-hunter-gh-run-download-"))
        try:
            download_payload = packaging_gate._download_packaging_baseline_github_run(
                run_id,
                repo=repo,
                github_workflow=github_workflow,
                github_run_list_limit=github_run_list_limit,
                artifact_names=artifact_names,
                artifact_patterns=artifact_patterns,
                download_dir=retained_dir,
                download_dir_source="temporary",
                download_dir_retained=True,
            )
        except ResourceHunterError as exc:
            raise PackagingBaselineReportError(
                str(exc),
                download_payload=getattr(exc, "download_payload", None),
            ) from exc
        return _evaluate_downloaded_packaging_baseline_reports(download_payload)

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
                download_dir_source="temporary",
                download_dir_retained=False,
            )
        except ResourceHunterError as exc:
            raise PackagingBaselineReportError(
                str(exc),
                download_payload=getattr(exc, "download_payload", None),
            ) from exc
        return _evaluate_downloaded_packaging_baseline_reports(download_payload)


def packaging_baseline_report_requirement_failures(report_payload: Mapping[str, Any]) -> list[str]:
    report_type = report_payload.get("report_type")
    if report_type == "aggregate":
        artifacts = report_payload.get("artifacts")
        if not isinstance(artifacts, list):
            return ["Packaging baseline aggregate report did not contain artifacts."]
        failures: list[str] = []
        for artifact in artifacts:
            if not isinstance(artifact, Mapping):
                continue
            failures.extend(packaging_baseline_report_requirement_failures(artifact))
        return failures

    requirements = report_payload.get("requirements") if isinstance(report_payload.get("requirements"), Mapping) else {}
    requirement_failures = requirements.get("failures")
    if not isinstance(requirement_failures, list):
        requirement_failures = []
    artifact_path = report_payload.get("artifact_path") or "unknown artifact"
    if requirement_failures:
        return [f"{artifact_path}: {failure}" for failure in requirement_failures]

    summary = report_payload.get("summary") if isinstance(report_payload.get("summary"), Mapping) else {}
    if summary.get("baseline_contract_ok") is True:
        return []
    return [f"{artifact_path}: Packaging baseline contract drift detected."]


def _capture_diagnostic_entry(
    *,
    artifact_path: str,
    capture: Mapping[str, Any],
) -> dict[str, Any] | None:
    diagnostics = capture.get("diagnostics") if isinstance(capture.get("diagnostics"), Mapping) else {}
    actual = capture.get("actual") if isinstance(capture.get("actual"), Mapping) else {}

    failed_step = actual.get("failed_step")
    strategy_family = actual.get("strategy_family")
    strategy = actual.get("strategy")
    reason = _normalized_capture_reason(actual.get("reason"))
    packaging_error = diagnostics.get("packaging_error")
    packaging_blockers = _copy_string_list(diagnostics.get("packaging_blockers"))
    bootstrap_build_requirements = _copy_string_list(diagnostics.get("bootstrap_build_requirements"))
    bootstrap_build_deps_ready = diagnostics.get("bootstrap_build_deps_ready")
    packaging_smoke_ready_with_bootstrap = diagnostics.get("packaging_smoke_ready_with_bootstrap")

    if not any(
        (
            failed_step,
            strategy_family,
            strategy,
            reason,
            packaging_error,
            packaging_blockers,
            bootstrap_build_requirements,
            bootstrap_build_deps_ready is not None,
            packaging_smoke_ready_with_bootstrap is not None,
        )
    ):
        return None

    entry: dict[str, Any] = {
        "artifact_path": artifact_path,
        "artifact_label": _artifact_group_label(artifact_path),
        "artifact_display_label": _artifact_display_label(artifact_path),
        "capture_name": str(capture.get("name") or "unknown"),
        "capture_label": str(capture.get("label") or capture.get("name") or "unknown"),
    }
    packaging_python = capture.get("packaging_python")
    if packaging_python is not None:
        entry["packaging_python"] = packaging_python
    if failed_step is not None:
        entry["failed_step"] = failed_step
    if strategy_family is not None:
        entry["strategy_family"] = strategy_family
    if strategy is not None:
        entry["strategy"] = strategy
    if reason is not None:
        entry["reason"] = reason
    if packaging_error:
        entry["packaging_error"] = str(packaging_error)
    if packaging_blockers:
        entry["packaging_blockers"] = packaging_blockers
    if bootstrap_build_requirements:
        entry["bootstrap_build_requirements"] = bootstrap_build_requirements
    if bootstrap_build_deps_ready is not None:
        entry["bootstrap_build_deps_ready"] = bootstrap_build_deps_ready
    if packaging_smoke_ready_with_bootstrap is not None:
        entry["packaging_smoke_ready_with_bootstrap"] = packaging_smoke_ready_with_bootstrap
    return entry


def _packaging_baseline_report_capture_diagnostics(report_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    report_type = report_payload.get("report_type")
    diagnostics: list[dict[str, Any]] = []

    if report_type == "single":
        artifact_path = str(report_payload.get("artifact_path") or "unknown artifact")
        captures = report_payload.get("captures") if isinstance(report_payload.get("captures"), list) else []
        for capture in captures:
            if not isinstance(capture, Mapping) or capture.get("matches_expectation") is True:
                continue
            entry = _capture_diagnostic_entry(artifact_path=artifact_path, capture=capture)
            if entry is not None:
                diagnostics.append(entry)
        return diagnostics

    if report_type != "aggregate":
        return diagnostics

    artifacts = report_payload.get("artifacts") if isinstance(report_payload.get("artifacts"), list) else []
    for artifact in artifacts:
        if not isinstance(artifact, Mapping):
            continue
        artifact_path = str(artifact.get("artifact_path") or "unknown artifact")
        captures = artifact.get("captures") if isinstance(artifact.get("captures"), list) else []
        for capture in captures:
            if not isinstance(capture, Mapping) or capture.get("matches_expectation") is True:
                continue
            entry = _capture_diagnostic_entry(artifact_path=artifact_path, capture=capture)
            if entry is not None:
                diagnostics.append(entry)
    return diagnostics


def _artifact_group_label(artifact_path: object) -> str:
    artifact_ref = str(artifact_path or "").strip()
    if not artifact_ref:
        return "unknown artifact"
    archive_member_ref = _split_archive_member_path(artifact_ref)
    if archive_member_ref is not None:
        _, archive_member = archive_member_ref
        member_path = Path(archive_member)
        return member_path.parent.name or member_path.name or artifact_ref
    artifact_path_obj = Path(artifact_ref)
    return artifact_path_obj.parent.name or artifact_path_obj.name or artifact_ref


def _artifact_display_label(artifact_path: object) -> str:
    metadata = _artifact_summary_metadata(artifact_path)
    display_label = metadata.get("artifact_matrix_label") or metadata.get("artifact_name")
    if display_label is not None and str(display_label).strip():
        return str(display_label)
    return _artifact_group_label(artifact_path)


def _artifact_summary_metadata(artifact_path: object) -> dict[str, Any]:
    artifact_name = _artifact_group_label(artifact_path)
    metadata: dict[str, Any] = {
        "artifact_name": artifact_name,
    }
    prefix = "resource-hunter-packaging-baseline-"
    if not artifact_name.startswith(prefix):
        return metadata
    remainder = artifact_name[len(prefix) :]
    matrix_os, separator, matrix_python_suffix = remainder.rpartition("-py")
    if not separator or not matrix_os or not matrix_python_suffix:
        return metadata
    matrix_python = f"py{matrix_python_suffix}"
    metadata.update(
        {
            "artifact_matrix_os": matrix_os,
            "artifact_matrix_python": matrix_python,
            "artifact_matrix_label": f"{matrix_os} / {matrix_python}",
        }
    )
    return metadata


def _artifact_report_status(report_payload: Mapping[str, Any]) -> str:
    summary = report_payload.get("summary") if isinstance(report_payload.get("summary"), Mapping) else {}
    requirements = report_payload.get("requirements") if isinstance(report_payload.get("requirements"), Mapping) else {}
    if summary.get("baseline_contract_ok") is True and requirements.get("ok") is not False:
        return "ok"
    return "drift"


def _annotated_artifact_report(report_payload: Mapping[str, Any]) -> dict[str, Any]:
    annotated = dict(report_payload)
    artifact_path = annotated.get("artifact_path") or "unknown artifact"
    for key, value in _artifact_summary_metadata(artifact_path).items():
        annotated.setdefault(key, value)
    capture_diagnostics = annotated.get("capture_diagnostics")
    if not isinstance(capture_diagnostics, list):
        capture_diagnostics = _packaging_baseline_report_capture_diagnostics(annotated)
        if capture_diagnostics:
            annotated["capture_diagnostics"] = capture_diagnostics
    requirements = annotated.get("requirements") if isinstance(annotated.get("requirements"), Mapping) else {}
    requirement_failures = requirements.get("failures") if isinstance(requirements.get("failures"), list) else []
    annotated["status"] = str(annotated.get("status") or _artifact_report_status(annotated))
    annotated["requirement_failure_count"] = int(
        annotated.get("requirement_failure_count")
        if annotated.get("requirement_failure_count") is not None
        else len(requirement_failures)
    )
    annotated["capture_diagnostic_count"] = int(
        annotated.get("capture_diagnostic_count")
        if annotated.get("capture_diagnostic_count") is not None
        else len(capture_diagnostics)
    )
    return annotated


def _requirement_failure_message(failure: object) -> str:
    message = str(failure or "").strip()
    prefix = "Packaging baseline requirement failed: "
    if message.startswith(prefix):
        return message[len(prefix) :]
    return message


def _aggregate_requirement_failure_groups(report_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    if report_payload.get("report_type") != "aggregate":
        return []
    artifacts = report_payload.get("artifacts")
    if not isinstance(artifacts, list):
        return []

    grouped_failures: dict[str, dict[str, Any]] = {}
    for artifact in artifacts:
        if not isinstance(artifact, Mapping):
            continue
        annotated_artifact = _annotated_artifact_report(artifact)
        requirements = (
            annotated_artifact.get("requirements")
            if isinstance(annotated_artifact.get("requirements"), Mapping)
            else {}
        )
        requirement_failures = requirements.get("failures")
        if not isinstance(requirement_failures, list):
            continue
        artifact_path = str(annotated_artifact.get("artifact_path") or "unknown artifact")
        artifact_label = _artifact_group_label(artifact_path)
        artifact_display_label = str(
            annotated_artifact.get("artifact_matrix_label")
            or annotated_artifact.get("artifact_name")
            or artifact_label
        )
        for failure in requirement_failures:
            message = _requirement_failure_message(failure)
            if not message:
                continue
            group = grouped_failures.setdefault(
                message,
                {
                    "message": message,
                    "artifact_labels": [],
                    "artifact_display_labels": [],
                    "artifact_paths": [],
                },
            )
            if artifact_label not in group["artifact_labels"]:
                group["artifact_labels"].append(artifact_label)
            if artifact_display_label not in group["artifact_display_labels"]:
                group["artifact_display_labels"].append(artifact_display_label)
            if artifact_path not in group["artifact_paths"]:
                group["artifact_paths"].append(artifact_path)

    summary: list[dict[str, Any]] = []
    for group in grouped_failures.values():
        summary.append(
            {
                "message": group["message"],
                "artifact_count": len(group["artifact_paths"]),
                "artifact_labels": list(group["artifact_labels"]),
                "artifact_display_labels": list(group["artifact_display_labels"]),
                "artifact_paths": list(group["artifact_paths"]),
            }
        )
    return summary


def _aggregate_artifact_statuses(report_payload_or_artifacts: Mapping[str, Any] | Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    if isinstance(report_payload_or_artifacts, Mapping):
        artifacts = report_payload_or_artifacts.get("artifacts")
        if not isinstance(artifacts, list):
            return []
    else:
        artifacts = report_payload_or_artifacts

    statuses: list[dict[str, Any]] = []
    for artifact in artifacts:
        if not isinstance(artifact, Mapping):
            continue
        annotated = _annotated_artifact_report(artifact)
        summary_entry: dict[str, Any] = {
            "artifact_path": str(annotated.get("artifact_path") or "unknown artifact"),
            "artifact_name": str(annotated.get("artifact_name") or _artifact_group_label(annotated.get("artifact_path"))),
            "status": str(annotated.get("status") or _artifact_report_status(annotated)),
            "baseline_contract_ok": _packaging_baseline_report_summary_value(
                annotated,
                "baseline_contract_ok",
            ),
            "requirement_failure_count": int(annotated.get("requirement_failure_count") or 0),
            "capture_diagnostic_count": int(annotated.get("capture_diagnostic_count") or 0),
        }
        for key in ("artifact_matrix_os", "artifact_matrix_python", "artifact_matrix_label"):
            value = annotated.get(key)
            if value is not None and str(value).strip():
                summary_entry[key] = value
        statuses.append(summary_entry)
    return statuses


def _append_requirement_failure_group_lines(lines: list[str], report_payload: Mapping[str, Any]) -> None:
    failure_groups = report_payload.get("requirement_failure_groups")
    if not isinstance(failure_groups, list):
        failure_groups = _aggregate_requirement_failure_groups(report_payload)
    if not failure_groups:
        return
    lines.append("Requirement failure groups:")
    for group in failure_groups:
        artifact_count = int(group.get("artifact_count") or 0)
        artifact_labels = (
            group.get("artifact_display_labels")
            if isinstance(group.get("artifact_display_labels"), list)
            else group.get("artifact_labels")
            if isinstance(group.get("artifact_labels"), list)
            else []
        )
        artifact_label_text = ", ".join(str(label) for label in artifact_labels if str(label).strip()) or "unknown"
        artifact_noun = "artifact" if artifact_count == 1 else "artifacts"
        lines.append(
            f"- {group.get('message')} ({artifact_count} {artifact_noun}: {artifact_label_text})"
        )


def _packaging_baseline_report_summary_value(report_payload: Mapping[str, Any], key: str) -> Any:
    summary = report_payload.get("summary") if isinstance(report_payload.get("summary"), Mapping) else {}
    return summary.get(key)


def _append_artifact_status_summary_lines(lines: list[str], report_payload: Mapping[str, Any]) -> None:
    artifact_statuses = report_payload.get("artifact_statuses")
    if not isinstance(artifact_statuses, list):
        artifact_statuses = _aggregate_artifact_statuses(report_payload)
    if not artifact_statuses:
        return

    lines.append("Artifact status summary:")
    for artifact in artifact_statuses:
        if not isinstance(artifact, Mapping):
            continue
        artifact_label = str(
            artifact.get("artifact_matrix_label")
            or artifact.get("artifact_name")
            or artifact.get("artifact_path")
            or "unknown artifact"
        )
        details = [
            f"status={artifact.get('status') or 'unknown'}",
            "baseline_contract_ok="
            f"{_artifact_value_text(artifact.get('baseline_contract_ok'))}",
            f"requirement_failures={int(artifact.get('requirement_failure_count') or 0)}",
            f"capture_diagnostics={int(artifact.get('capture_diagnostic_count') or 0)}",
        ]
        lines.append(f"- {artifact_label}: {'; '.join(details)}")


def _artifact_value_text(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    if isinstance(value, (list, tuple)):
        rendered = ", ".join(_artifact_value_text(item) for item in value)
        return rendered or "[]"
    return str(value)


def _diagnostic_summary_text(value: object) -> str | None:
    text = str(value or "").strip()
    if not text:
        return None
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return None
    return lines[-1]


def _diagnostic_path_signature(value: object) -> str | None:
    detail = str(value or "").strip().strip("\"'")
    if not detail:
        return None
    if not (
        detail.startswith(("/", "\\"))
        or (len(detail) >= 3 and detail[1] == ":" and detail[2] in ("/", "\\"))
    ):
        return None
    normalized = detail.replace("\\", "/")
    segments = [segment for segment in normalized.split("/") if segment and segment not in {".", ".."}]
    if not segments:
        return None
    tail = "/".join(segments[-2:])
    return f"*/{tail}"


def _diagnostic_error_signature(value: object) -> str | None:
    summary = _diagnostic_summary_text(value)
    if not summary:
        return None
    prefix, _, detail = summary.partition(":")
    normalized_prefix = prefix.strip()
    if normalized_prefix and " " not in normalized_prefix and normalized_prefix.endswith(("Error", "Exception")):
        path_signature = _diagnostic_path_signature(detail)
        if path_signature:
            return f"{normalized_prefix}: {path_signature}"
        return normalized_prefix
    return summary


def _aggregate_capture_diagnostic_groups(report_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    if report_payload.get("report_type") != "aggregate":
        return []

    capture_diagnostics = report_payload.get("capture_diagnostics")
    if not isinstance(capture_diagnostics, list):
        capture_diagnostics = _packaging_baseline_report_capture_diagnostics(report_payload)
    if not capture_diagnostics:
        return []

    grouped_diagnostics: dict[tuple[Any, ...], dict[str, Any]] = {}
    for diagnostic in capture_diagnostics:
        if not isinstance(diagnostic, Mapping):
            continue
        artifact_path = str(diagnostic.get("artifact_path") or "unknown artifact")
        artifact_label = str(diagnostic.get("artifact_label") or _artifact_group_label(artifact_path))
        artifact_display_label = str(
            diagnostic.get("artifact_display_label") or _artifact_display_label(artifact_path)
        )
        capture_name = str(diagnostic.get("capture_name") or "unknown")
        capture_label = str(diagnostic.get("capture_label") or capture_name or "unknown")
        reason = _diagnostic_summary_text(diagnostic.get("reason"))
        packaging_error_signature = _diagnostic_error_signature(diagnostic.get("packaging_error"))
        packaging_error_summary = _diagnostic_summary_text(diagnostic.get("packaging_error"))
        packaging_blockers = _copy_string_list(diagnostic.get("packaging_blockers"))
        bootstrap_build_requirements = _copy_string_list(diagnostic.get("bootstrap_build_requirements"))
        key = (
            capture_name,
            capture_label,
            diagnostic.get("failed_step"),
            diagnostic.get("strategy_family"),
            diagnostic.get("strategy"),
            reason,
            packaging_error_signature,
            tuple(packaging_blockers),
            tuple(bootstrap_build_requirements),
            diagnostic.get("bootstrap_build_deps_ready"),
            diagnostic.get("packaging_smoke_ready_with_bootstrap"),
        )
        group = grouped_diagnostics.setdefault(
            key,
            {
                "capture_name": capture_name,
                "capture_label": capture_label,
                "failed_step": diagnostic.get("failed_step"),
                "strategy_family": diagnostic.get("strategy_family"),
                "strategy": diagnostic.get("strategy"),
                "reason": reason,
                "packaging_error_signature": packaging_error_signature,
                "packaging_error_summaries": [],
                "packaging_blockers": packaging_blockers,
                "bootstrap_build_requirements": bootstrap_build_requirements,
                "bootstrap_build_deps_ready": diagnostic.get("bootstrap_build_deps_ready"),
                "packaging_smoke_ready_with_bootstrap": diagnostic.get("packaging_smoke_ready_with_bootstrap"),
                "artifact_labels": [],
                "artifact_display_labels": [],
                "artifact_paths": [],
            },
        )
        if packaging_error_summary and packaging_error_summary not in group["packaging_error_summaries"]:
            group["packaging_error_summaries"].append(packaging_error_summary)
        if artifact_label not in group["artifact_labels"]:
            group["artifact_labels"].append(artifact_label)
        if artifact_display_label not in group["artifact_display_labels"]:
            group["artifact_display_labels"].append(artifact_display_label)
        if artifact_path not in group["artifact_paths"]:
            group["artifact_paths"].append(artifact_path)

    return [
        {
            **group,
            "artifact_count": len(group["artifact_paths"]),
            "packaging_error_summary_count": len(group["packaging_error_summaries"]),
        }
        for group in grouped_diagnostics.values()
    ]


def _append_capture_diagnostic_group_lines(lines: list[str], report_payload: Mapping[str, Any]) -> None:
    capture_diagnostic_groups = report_payload.get("capture_diagnostic_groups")
    if not isinstance(capture_diagnostic_groups, list):
        capture_diagnostic_groups = _aggregate_capture_diagnostic_groups(report_payload)
    if not capture_diagnostic_groups:
        return

    lines.append("Drift diagnostic groups:")
    for group in capture_diagnostic_groups:
        if not isinstance(group, Mapping):
            continue

        details: list[str] = []
        failed_step = group.get("failed_step")
        if failed_step is not None:
            details.append(f"failed_step={failed_step}")

        strategy_family = group.get("strategy_family")
        if strategy_family is not None:
            details.append(f"strategy_family={strategy_family}")

        strategy = group.get("strategy")
        if strategy is not None:
            details.append(f"strategy={strategy}")

        reason = group.get("reason")
        if reason:
            details.append(f"reason={reason}")

        packaging_error_summaries = group.get("packaging_error_summaries")
        if not isinstance(packaging_error_summaries, list):
            packaging_error_summaries = []
        packaging_error_summaries = [str(summary) for summary in packaging_error_summaries if str(summary).strip()]
        packaging_error_signature = str(group.get("packaging_error_signature") or "").strip()
        if packaging_error_summaries:
            if len(packaging_error_summaries) == 1:
                details.append(f"packaging_error={packaging_error_summaries[0]}")
            elif packaging_error_signature:
                details.append(
                    f"packaging_error={packaging_error_signature} ({len(packaging_error_summaries)} variants)"
                )
            else:
                details.append(f"packaging_error_variants={len(packaging_error_summaries)}")

        packaging_blockers = group.get("packaging_blockers")
        if isinstance(packaging_blockers, list) and packaging_blockers:
            details.append(f"blockers={', '.join(str(blocker) for blocker in packaging_blockers)}")

        bootstrap_build_requirements = group.get("bootstrap_build_requirements")
        if isinstance(bootstrap_build_requirements, list) and bootstrap_build_requirements:
            details.append(
                "bootstrap_build_requirements="
                + ", ".join(str(requirement) for requirement in bootstrap_build_requirements)
            )

        if group.get("bootstrap_build_deps_ready") is not None:
            details.append(
                "bootstrap_build_deps_ready="
                f"{_artifact_value_text(group.get('bootstrap_build_deps_ready'))}"
            )
        if group.get("packaging_smoke_ready_with_bootstrap") is not None:
            details.append(
                "packaging_smoke_ready_with_bootstrap="
                f"{_artifact_value_text(group.get('packaging_smoke_ready_with_bootstrap'))}"
            )

        detail_text = "; ".join(details) if details else "diagnostic details unavailable"
        artifact_labels = (
            group.get("artifact_display_labels")
            if isinstance(group.get("artifact_display_labels"), list)
            else group.get("artifact_labels")
            if isinstance(group.get("artifact_labels"), list)
            else []
        )
        artifact_label_text = ", ".join(str(label) for label in artifact_labels if str(label).strip()) or "unknown"
        artifact_count = int(group.get("artifact_count") or 0)
        artifact_noun = "artifact" if artifact_count == 1 else "artifacts"
        lines.append(
            f"- {group.get('capture_label') or group.get('capture_name') or 'unknown'}: {detail_text} "
            f"({artifact_count} {artifact_noun}: {artifact_label_text})"
        )


def _append_capture_diagnostic_lines(lines: list[str], report_payload: Mapping[str, Any]) -> None:
    capture_diagnostics = _packaging_baseline_report_capture_diagnostics(report_payload)
    if not capture_diagnostics:
        return

    lines.append("Drift diagnostics:")
    for diagnostic in capture_diagnostics:
        details: list[str] = []

        failed_step = diagnostic.get("failed_step")
        if failed_step is not None:
            details.append(f"failed_step={failed_step}")

        strategy_family = diagnostic.get("strategy_family")
        if strategy_family is not None:
            details.append(f"strategy_family={strategy_family}")

        strategy = diagnostic.get("strategy")
        if strategy is not None:
            details.append(f"strategy={strategy}")

        packaging_error = _diagnostic_summary_text(diagnostic.get("packaging_error"))
        if packaging_error:
            details.append(f"packaging_error={packaging_error}")
        else:
            reason = _diagnostic_summary_text(diagnostic.get("reason"))
            if reason:
                details.append(f"reason={reason}")

        packaging_blockers = _copy_string_list(diagnostic.get("packaging_blockers"))
        if packaging_blockers:
            details.append(f"blockers={', '.join(packaging_blockers)}")

        bootstrap_build_requirements = _copy_string_list(diagnostic.get("bootstrap_build_requirements"))
        if bootstrap_build_requirements:
            details.append(f"bootstrap_build_requirements={', '.join(bootstrap_build_requirements)}")

        if diagnostic.get("bootstrap_build_deps_ready") is not None:
            details.append(
                "bootstrap_build_deps_ready="
                f"{_artifact_value_text(diagnostic.get('bootstrap_build_deps_ready'))}"
            )
        if diagnostic.get("packaging_smoke_ready_with_bootstrap") is not None:
            details.append(
                "packaging_smoke_ready_with_bootstrap="
                f"{_artifact_value_text(diagnostic.get('packaging_smoke_ready_with_bootstrap'))}"
            )

        summary = "; ".join(details) if details else "diagnostic details unavailable"
        lines.append(
            f"- {diagnostic.get('artifact_display_label') or diagnostic.get('artifact_label') or 'unknown'} / "
            f"{diagnostic.get('capture_label') or diagnostic.get('capture_name') or 'unknown'}: {summary}"
        )


def _download_repo_text(download: Mapping[str, Any]) -> str:
    repo = download.get("repo")
    if repo is None:
        return "current gh context"
    repo_label = str(repo)
    repo_source = download.get("repo_source")
    if repo_source:
        repo_label = f"{repo_label} ({repo_source})"
    return repo_label


def _download_run_text(download: Mapping[str, Any]) -> str:
    run_label = str(download.get("run_id") or "unknown")
    requested_run_id = download.get("requested_run_id")
    if requested_run_id is None:
        return run_label
    requested_run_label = str(requested_run_id).strip()
    if requested_run_label and requested_run_label != run_label:
        return f"{run_label} (requested {requested_run_label})"
    return run_label


def _github_run_download_lines(download: Mapping[str, Any]) -> list[str]:
    if download.get("provider") != "github-actions":
        return []

    lines = [
        f"github_run: {_download_run_text(download)}",
        f"download_repo: {_download_repo_text(download)}",
        f"download_dir: {download.get('download_dir') or 'unknown'}",
    ]
    if download.get("github_run_list_limit") is not None:
        lines.append(f"github_run_list_limit: {_artifact_value_text(download.get('github_run_list_limit'))}")
    if "download_dir_retained" in download:
        lines.append(f"download_dir_retained: {_artifact_value_text(download.get('download_dir_retained'))}")
    artifact_filter_source = download.get("artifact_filter_source")
    if artifact_filter_source is not None:
        lines.append(f"artifact_filter_source: {artifact_filter_source}")

    artifact_names = download.get("artifact_names")
    if isinstance(artifact_names, list) and artifact_names:
        lines.append(f"artifact_names: {', '.join(str(name) for name in artifact_names)}")

    artifact_patterns = download.get("artifact_patterns")
    if isinstance(artifact_patterns, list) and artifact_patterns:
        lines.append(f"artifact_patterns: {', '.join(str(pattern) for pattern in artifact_patterns)}")

    for key in (
        "resolved_artifact_count",
        "resolved_filesystem_artifact_count",
        "resolved_archive_member_count",
    ):
        if key in download:
            lines.append(f"{key}: {_artifact_value_text(download.get(key))}")

    run_lookup = download.get("run_lookup")
    if isinstance(run_lookup, Mapping):
        selected_run = run_lookup.get("selected_run")
        if isinstance(selected_run, Mapping):
            for source_key, target_key in (
                ("workflow_name", "selected_github_run_workflow"),
                ("status", "selected_github_run_status"),
                ("conclusion", "selected_github_run_conclusion"),
                ("head_branch", "selected_github_run_head_branch"),
                ("event", "selected_github_run_event"),
                ("display_title", "selected_github_run_title"),
                ("url", "selected_github_run_url"),
            ):
                value = selected_run.get(source_key)
                if value is not None and str(value):
                    lines.append(f"{target_key}: {value}")

    resolved_artifact_paths = download.get("resolved_artifact_paths")
    if isinstance(resolved_artifact_paths, list):
        for index, artifact_path in enumerate(resolved_artifact_paths, start=1):
            lines.append(f"resolved_artifact[{index}]: {artifact_path}")

    return lines


def _expected_strategy_families_text(value: Any) -> str:
    if isinstance(value, (list, tuple)):
        rendered = ", ".join(str(item) for item in value if item is not None and str(item))
        if rendered:
            return rendered
    return "any"


def _failed_step_text(failed_step: Any) -> str:
    if failed_step is None:
        return "absent"
    return f"present ({failed_step})"


def _format_packaging_baseline_issue(issue: Mapping[str, Any]) -> str:
    parts = [
        f"field={issue.get('field') or 'unknown'}",
        f"kind={issue.get('kind') or 'unknown'}",
    ]
    if "expected_any_of" in issue:
        parts.append(f"expected_any_of={_artifact_value_text(issue.get('expected_any_of'))}")
    elif "expected_present" in issue:
        parts.append(f"expected_present={_artifact_value_text(issue.get('expected_present'))}")
    elif "expected" in issue:
        parts.append(f"expected={_artifact_value_text(issue.get('expected'))}")
    if "actual" in issue:
        parts.append(f"actual={_artifact_value_text(issue.get('actual'))}")
    message = issue.get("message")
    if message:
        parts.append(str(message))
    return "; ".join(parts)


def _packaging_baseline_report_capture_match(
    report_payload: Mapping[str, Any],
    *,
    capture_name: str,
) -> Any:
    captures = report_payload.get("captures")
    if not isinstance(captures, list):
        return None
    for capture in captures:
        if not isinstance(capture, Mapping):
            continue
        if capture.get("name") == capture_name:
            return capture.get("matches_expectation")
    return None


def _format_packaging_baseline_capture_text(capture: Mapping[str, Any]) -> list[str]:
    label = capture.get("label") or f"{capture.get('name') or 'Unknown'}"
    expected_outcome = capture.get("expected_outcome")
    if not isinstance(expected_outcome, Mapping):
        expected_outcome = {}
    actual = capture.get("actual")
    if not isinstance(actual, Mapping):
        actual = {}
    lines = [
        f"{label} capture:",
        f"- path: {capture.get('path') or 'missing'}",
        f"- project_root: {capture.get('project_root') or 'missing'}",
        f"- project_root_source: {capture.get('project_root_source') or 'unknown'}",
    ]
    requested_project_root = capture.get("requested_project_root")
    if requested_project_root is not None:
        lines.append(f"- requested_project_root: {requested_project_root}")
    packaging_python = capture.get("packaging_python")
    if packaging_python is not None:
        lines.append(f"- packaging_python: {packaging_python}")
    packaging_python_source = capture.get("packaging_python_source")
    if packaging_python_source is not None:
        lines.append(f"- packaging_python_source: {packaging_python_source}")
    packaging_python_auto_selected = capture.get("packaging_python_auto_selected")
    if packaging_python_auto_selected is not None:
        lines.append(
            f"- packaging_python_auto_selected: {_artifact_value_text(packaging_python_auto_selected)}"
        )
    lines.extend(
        [
            (
                "- expected_outcome.doctor_packaging_ready: "
                f"{_artifact_value_text(expected_outcome.get('doctor_packaging_ready'))}"
            ),
            (
                "- actual.doctor_packaging_ready: "
                f"{_artifact_value_text(actual.get('doctor_packaging_ready'))}"
            ),
            (
                "- expected_outcome.packaging_smoke_ok: "
                f"{_artifact_value_text(expected_outcome.get('packaging_smoke_ok'))}"
            ),
            f"- actual.packaging_smoke_ok: {_artifact_value_text(actual.get('packaging_smoke_ok'))}",
            (
                "- expected_outcome.failed_step_present: "
                f"{_artifact_value_text(expected_outcome.get('failed_step_present'))}"
            ),
            f"- actual.failed_step: {_failed_step_text(actual.get('failed_step'))}",
            (
                "- expected_outcome.strategy_family_any_of: "
                f"{_expected_strategy_families_text(expected_outcome.get('strategy_family_any_of'))}"
            ),
            f"- actual.strategy_family: {actual.get('strategy_family') or 'unknown'}",
            f"- strategy: {actual.get('strategy') or 'unknown'}",
            f"- reason: {actual.get('reason') or 'n/a'}",
            f"- matches_expectation: {_artifact_value_text(capture.get('matches_expectation'))}",
        ]
    )
    expectation_drift = capture.get("expectation_drift")
    if isinstance(expectation_drift, list) and expectation_drift:
        for index, issue in enumerate(expectation_drift, start=1):
            if isinstance(issue, Mapping):
                lines.append(f"- expectation_drift[{index}]: {_format_packaging_baseline_issue(issue)}")
    else:
        lines.append("- expectation_drift: none")
    diagnostics = capture.get("diagnostics") if isinstance(capture.get("diagnostics"), Mapping) else {}
    packaging_error = _diagnostic_summary_text(diagnostics.get("packaging_error"))
    if packaging_error:
        lines.append(f"- diagnostics.packaging_error: {packaging_error}")
    packaging_blockers = _copy_string_list(diagnostics.get("packaging_blockers"))
    if packaging_blockers:
        lines.append(f"- diagnostics.packaging_blockers: {', '.join(packaging_blockers)}")
    bootstrap_build_requirements = _copy_string_list(diagnostics.get("bootstrap_build_requirements"))
    if bootstrap_build_requirements:
        lines.append(
            "- diagnostics.bootstrap_build_requirements: "
            f"{', '.join(bootstrap_build_requirements)}"
        )
    if diagnostics.get("bootstrap_build_deps_ready") is not None:
        lines.append(
            "- diagnostics.bootstrap_build_deps_ready: "
            f"{_artifact_value_text(diagnostics.get('bootstrap_build_deps_ready'))}"
        )
    if diagnostics.get("packaging_smoke_ready_with_bootstrap") is not None:
        lines.append(
            "- diagnostics.packaging_smoke_ready_with_bootstrap: "
            f"{_artifact_value_text(diagnostics.get('packaging_smoke_ready_with_bootstrap'))}"
        )
    return lines


def _format_single_packaging_baseline_text(report_payload: Mapping[str, Any]) -> str:
    summary = report_payload.get("summary") if isinstance(report_payload.get("summary"), Mapping) else {}
    requirements = report_payload.get("requirements") if isinstance(report_payload.get("requirements"), Mapping) else {}
    download = report_payload.get("download") if isinstance(report_payload.get("download"), Mapping) else {}
    lines = [
        "Resource Hunter packaging baseline report",
        f"artifact: {report_payload.get('artifact_path') or 'unknown'}",
        f"schema_version: {report_payload.get('artifact_schema_version')}",
        f"captured_at: {report_payload.get('captured_at') or 'unknown'}",
        f"output_dir: {report_payload.get('output_dir') or 'unknown'}",
        f"project_root: {report_payload.get('project_root') or 'unknown'}",
        f"project_root_source: {report_payload.get('project_root_source') or 'unknown'}",
        f"blocked_python: {report_payload.get('blocked_python') or 'unknown'}",
    ]
    requested_project_root = report_payload.get("requested_project_root")
    if requested_project_root is not None:
        lines.append(f"requested_project_root: {requested_project_root}")
    lines.extend(_github_run_download_lines(download))
    lines.extend(
        [
            "",
            "Summary:",
            (
                "- passing_capture_matches_expectation: "
                f"{_artifact_value_text(summary.get('passing_capture_matches_expectation'))}"
            ),
            (
                "- blocked_capture_matches_expectation: "
                f"{_artifact_value_text(summary.get('blocked_capture_matches_expectation'))}"
            ),
            f"- baseline_contract_ok: {_artifact_value_text(summary.get('baseline_contract_ok'))}",
            f"- require_expected_outcomes: {_artifact_value_text(requirements.get('require_expected_outcomes'))}",
            f"- requirements.ok: {_artifact_value_text(requirements.get('ok'))}",
        ]
    )
    failures = requirements.get("failures")
    if isinstance(failures, list) and failures:
        for index, failure in enumerate(failures, start=1):
            lines.append(f"- requirements.failure[{index}]: {failure}")
    else:
        lines.append("- requirements.failure: none")
    warnings = report_payload.get("warnings")
    if isinstance(warnings, list) and warnings:
        for index, warning in enumerate(warnings, start=1):
            lines.append(f"- warning[{index}]: {warning}")
    else:
        lines.append("- warning: none")

    captures = report_payload.get("captures")
    if not isinstance(captures, list):
        captures = []
    for capture in captures:
        if not isinstance(capture, Mapping):
            continue
        lines.append("")
        lines.extend(_format_packaging_baseline_capture_text(capture))
    _append_capture_diagnostic_lines(lines, report_payload)
    return "\n".join(lines)


def _format_aggregate_packaging_baseline_text(report_payload: Mapping[str, Any]) -> str:
    summary = report_payload.get("summary") if isinstance(report_payload.get("summary"), Mapping) else {}
    download = report_payload.get("download") if isinstance(report_payload.get("download"), Mapping) else {}
    lines = [
        "Resource Hunter packaging baseline aggregate report",
        f"artifact_count: {summary.get('artifact_count') or 0}",
        f"contract_ok_artifact_count: {summary.get('contract_ok_artifact_count') or 0}",
        f"contract_drift_artifact_count: {summary.get('contract_drift_artifact_count') or 0}",
        f"requirement_failed_artifact_count: {summary.get('requirement_failed_artifact_count') or 0}",
        f"warning_count: {summary.get('warning_count') or 0}",
        f"all_baseline_contracts_ok: {_artifact_value_text(summary.get('all_baseline_contracts_ok'))}",
    ]
    lines.extend(_github_run_download_lines(download))
    _append_artifact_status_summary_lines(lines, report_payload)
    _append_requirement_failure_group_lines(lines, report_payload)
    _append_capture_diagnostic_group_lines(lines, report_payload)
    _append_capture_diagnostic_lines(lines, report_payload)
    warnings = report_payload.get("warnings")
    if isinstance(warnings, list) and warnings:
        for index, warning in enumerate(warnings, start=1):
            lines.append(f"warning[{index}]: {warning}")
    else:
        lines.append("warning: none")

    artifacts = report_payload.get("artifacts")
    if not isinstance(artifacts, list):
        artifacts = []
    for index, artifact in enumerate(artifacts, start=1):
        if not isinstance(artifact, Mapping):
            continue
        artifact_summary = artifact.get("summary") if isinstance(artifact.get("summary"), Mapping) else {}
        requirements = artifact.get("requirements") if isinstance(artifact.get("requirements"), Mapping) else {}
        artifact_warnings = artifact.get("warnings")
        if not isinstance(artifact_warnings, list):
            artifact_warnings = []
        lines.extend(
            [
                "",
                f"Artifact {index}:",
                f"- path: {artifact.get('artifact_path') or 'unknown'}",
                f"- captured_at: {artifact.get('captured_at') or 'unknown'}",
                f"- project_root: {artifact.get('project_root') or 'unknown'}",
                f"- baseline_contract_ok: {_artifact_value_text(artifact_summary.get('baseline_contract_ok'))}",
                (
                    "- passing.matches_expectation: "
                    f"{_artifact_value_text(_packaging_baseline_report_capture_match(artifact, capture_name='passing'))}"
                ),
                (
                    "- blocked.matches_expectation: "
                    f"{_artifact_value_text(_packaging_baseline_report_capture_match(artifact, capture_name='blocked'))}"
                ),
                f"- requirements.ok: {_artifact_value_text(requirements.get('ok'))}",
            ]
        )
        if artifact_warnings:
            for warning_index, warning in enumerate(artifact_warnings, start=1):
                lines.append(f"- warning[{warning_index}]: {warning}")
        else:
            lines.append("- warning: none")
    return "\n".join(lines)


def format_packaging_baseline_report_text(report_payload: Mapping[str, Any]) -> str:
    if report_payload.get("report_type") == "aggregate":
        return _format_aggregate_packaging_baseline_text(report_payload)
    return _format_single_packaging_baseline_text(report_payload)


def main(argv: Sequence[str] | None = None) -> int:
    from .cli import main as cli_main

    forwarded_argv = list(argv) if argv is not None else list(sys.argv[1:])
    return cli_main(["packaging-baseline-report", *forwarded_argv])


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "DEFAULT_PACKAGING_BASELINE_ARTIFACT",
    "PACKAGING_BASELINE_REPORT_SCHEMA_VERSION",
    "PackagingBaselineReportError",
    "attach_packaging_baseline_download_payload",
    "build_packaging_baseline_report_error_payload",
    "build_packaging_baseline_aggregate_report",
    "build_packaging_baseline_report",
    "format_packaging_baseline_report_text",
    "load_packaging_baseline_payload",
    "main",
    "packaging_baseline_report_requirement_failures",
    "read_packaging_baseline_report",
    "read_packaging_baseline_reports",
    "read_packaging_baseline_reports_from_github_run",
    "resolve_packaging_baseline_artifact_paths",
]
