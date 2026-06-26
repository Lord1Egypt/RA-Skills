from __future__ import annotations

import argparse
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ._version import __version__
from .cache import ResourceCache
from .common import dump_json, ensure_utf8_stdio, storage_root
from .core import ResourceHunterEngine, format_search_text, format_sources_text, parse_intent
from .errors import ResourceHunterError
from . import packaging_gate, packaging_report, packaging_verify
from . import packaging_smoke as packaging_tools
from .video_core import VideoManager, format_video_text


_PACKAGING_PYTHON_ENV = "RESOURCE_HUNTER_PACKAGING_PYTHON"
_AUTO_PACKAGING_PYTHON = "auto"
_PACKAGING_CAPTURE_SCHEMA_VERSION = 1
_PACKAGING_BASELINE_SCHEMA_VERSION = 1


def _resolve_kind(args: argparse.Namespace) -> str | None:
    if getattr(args, "kind", None):
        return args.kind
    for name in ("movie", "tv", "anime", "music", "software", "book", "general"):
        if getattr(args, name, False):
            return name
    return None


def _resolve_channel(args: argparse.Namespace) -> str:
    if getattr(args, "pan_only", False):
        return "pan"
    if getattr(args, "torrent_only", False):
        return "torrent"
    return getattr(args, "channel", "both")


def _module_available(module_name: str) -> bool:
    return packaging_tools.module_available(module_name)


def _packaging_blockers(*, has_pip: bool, has_build_backend: bool, has_wheel: bool) -> list[str]:
    return packaging_tools.packaging_blockers(
        has_pip=has_pip,
        has_build_backend=has_build_backend,
        has_wheel=has_wheel,
    )


def _console_script_strategy(*, has_venv: bool, console_smoke_ready: bool) -> str:
    return packaging_tools.console_script_strategy(
        has_venv=has_venv,
        console_smoke_ready=console_smoke_ready,
    )


def _packaging_status(python_executable: str | None = None) -> dict[str, Any]:
    return packaging_tools.packaging_status(python_executable=python_executable)


def _configured_packaging_python() -> str | None:
    configured = os.environ.get(_PACKAGING_PYTHON_ENV)
    if configured is None:
        return None
    configured = configured.strip()
    return configured or None


def _wants_auto_packaging_python(value: str | None) -> bool:
    return value is not None and value.strip().lower() == _AUTO_PACKAGING_PYTHON


def _effective_packaging_python(
    python_executable: str | None,
    *,
    bootstrap_build_deps: bool = False,
    project_root: str | None = None,
) -> tuple[str | None, str, list[dict[str, Any]] | None, bool]:
    if python_executable:
        if _wants_auto_packaging_python(python_executable):
            packaging_python, candidates = packaging_tools.select_packaging_python(
                project_root=project_root,
                allow_bootstrap_build_deps=bootstrap_build_deps,
            )
            return packaging_python or sys.executable, "auto", candidates, packaging_python is not None
        return python_executable, "argument", None, True
    configured = _configured_packaging_python()
    if configured:
        if _wants_auto_packaging_python(configured):
            packaging_python, candidates = packaging_tools.select_packaging_python(
                project_root=project_root,
                allow_bootstrap_build_deps=bootstrap_build_deps,
            )
            return packaging_python or sys.executable, "auto", candidates, packaging_python is not None
        return configured, "environment", None, True
    return None, "current", None, True


def _same_python(left: str, right: str) -> bool:
    return os.path.normcase(os.path.abspath(left)) == os.path.normcase(os.path.abspath(right))


def _packaging_python_subject(payload: dict[str, Any]) -> str:
    packaging_python = payload.get("packaging_python")
    runtime_python = payload.get("python")
    if packaging_python and runtime_python and not _same_python(packaging_python, runtime_python):
        return f"Selected packaging Python ({packaging_python})"
    return "Current Python"


def _packaging_python_label(payload: dict[str, Any]) -> str:
    packaging_python = payload.get("packaging_python") or payload.get("python")
    source = payload.get("packaging_python_source")
    if source == "argument":
        return f"{packaging_python} (via --python)"
    if source == "environment":
        return f"{packaging_python} (via {_PACKAGING_PYTHON_ENV})"
    if source == "auto":
        if payload.get("packaging_python_auto_selected"):
            return f"{packaging_python} (auto-selected)"
        return f"{packaging_python} (auto fallback to current interpreter)"
    return f"{packaging_python} (current interpreter)"


def _packaging_candidate_lines(payload: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for candidate in payload.get("packaging_python_candidates") or []:
        candidate_packaging = candidate.get("packaging", {})
        candidate_error = candidate_packaging.get("error")
        candidate_blockers = candidate_packaging.get("blockers") or []
        candidate_optional_gaps = candidate_packaging.get("optional_gaps") or []
        if candidate_error:
            detail = f"error: {candidate_error}"
        elif candidate.get("ready") and candidate.get("bootstrap_ready") and not candidate_packaging.get("full_packaging_smoke_ready"):
            strategy = candidate_packaging.get("bootstrap_console_script_strategy") or "unknown"
            detail = f"ready via bootstrap (strategy: {strategy})"
            if candidate_optional_gaps:
                detail += f"; optional gaps: {', '.join(candidate_optional_gaps)}"
        elif candidate.get("ready"):
            if candidate_optional_gaps:
                detail = f"ready (optional gaps: {', '.join(candidate_optional_gaps)})"
            else:
                detail = "ready"
        else:
            detail = f"blocked ({', '.join(candidate_blockers) if candidate_blockers else 'unknown'})"
        lines.append(f"- {candidate['python']} [{candidate['source']}]: {detail}")
    return lines


def _availability_text(value: Any) -> str:
    if value is None:
        return "unknown"
    return "ok" if value else "missing"


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


def _download_repo_text(download: dict[str, Any]) -> str:
    repo = download.get("repo")
    if repo is None:
        return "current gh context"
    repo_label = str(repo)
    repo_source = download.get("repo_source")
    if repo_source:
        repo_label = f"{repo_label} ({repo_source})"
    return repo_label


def _download_run_text(download: dict[str, Any]) -> str:
    run_label = str(download.get("run_id") or "unknown")
    requested_run_id = download.get("requested_run_id")
    if requested_run_id is None:
        return run_label
    requested_run_label = str(requested_run_id).strip()
    if requested_run_label and requested_run_label != run_label:
        return f"{run_label} (requested {requested_run_label})"
    return run_label


def _github_run_download_lines(download: dict[str, Any]) -> list[str]:
    if download.get("provider") != "github-actions":
        return []

    lines = [
        f"github_run: {_download_run_text(download)}",
        f"download_repo: {_download_repo_text(download)}",
        f"download_dir: {download.get('download_dir') or 'unknown'}",
    ]
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
    if isinstance(run_lookup, dict):
        selected_run = run_lookup.get("selected_run")
        if isinstance(selected_run, dict):
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


def _format_packaging_baseline_issue(issue: dict[str, Any]) -> str:
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
    report_payload: dict[str, Any],
    *,
    capture_name: str,
) -> Any:
    captures = report_payload.get("captures")
    if not isinstance(captures, list):
        return None
    for capture in captures:
        if not isinstance(capture, dict):
            continue
        if capture.get("name") == capture_name:
            return capture.get("matches_expectation")
    return None


def _format_packaging_baseline_capture_text(capture: dict[str, Any]) -> list[str]:
    label = capture.get("label") or f"{capture.get('name') or 'Unknown'}"
    expected_outcome = capture.get("expected_outcome")
    if not isinstance(expected_outcome, dict):
        expected_outcome = {}
    actual = capture.get("actual")
    if not isinstance(actual, dict):
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
            lines.append(f"- expectation_drift[{index}]: {_format_packaging_baseline_issue(issue)}")
    else:
        lines.append("- expectation_drift: none")
    return lines


def _format_packaging_baseline_text(report_payload: dict[str, Any]) -> str:
    summary = report_payload.get("summary") if isinstance(report_payload.get("summary"), dict) else {}
    requirements = (
        report_payload.get("requirements") if isinstance(report_payload.get("requirements"), dict) else {}
    )
    download = report_payload.get("download") if isinstance(report_payload.get("download"), dict) else {}
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
        if not isinstance(capture, dict):
            continue
        lines.append("")
        lines.extend(_format_packaging_baseline_capture_text(capture))
    return "\n".join(lines)


def _format_packaging_baseline_aggregate_text(report_payload: dict[str, Any]) -> str:
    summary = report_payload.get("summary") if isinstance(report_payload.get("summary"), dict) else {}
    download = report_payload.get("download") if isinstance(report_payload.get("download"), dict) else {}
    lines = [
        "Resource Hunter packaging baseline aggregate report",
        f"artifact_count: {summary.get('artifact_count') or 0}",
        f"contract_ok_artifact_count: {summary.get('contract_ok_artifact_count') or 0}",
        f"contract_drift_artifact_count: {summary.get('contract_drift_artifact_count') or 0}",
        (
            "requirement_failed_artifact_count: "
            f"{summary.get('requirement_failed_artifact_count') or 0}"
        ),
        f"warning_count: {summary.get('warning_count') or 0}",
        (
            "all_baseline_contracts_ok: "
            f"{_artifact_value_text(summary.get('all_baseline_contracts_ok'))}"
        ),
    ]
    lines.extend(_github_run_download_lines(download))
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
        if not isinstance(artifact, dict):
            continue
        artifact_summary = artifact.get("summary") if isinstance(artifact.get("summary"), dict) else {}
        requirements = artifact.get("requirements") if isinstance(artifact.get("requirements"), dict) else {}
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
                (
                    "- baseline_contract_ok: "
                    f"{_artifact_value_text(artifact_summary.get('baseline_contract_ok'))}"
                ),
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


def _format_doctor_text(payload: dict[str, Any]) -> str:
    lines = [
        "Resource Hunter doctor",
        f"Version: {payload['version']}",
        f"Python: {payload['python']}",
        f"Packaging Python: {_packaging_python_label(payload)}",
        f"stdout_encoding: {payload['stdout_encoding']}",
        f"cache_db: {payload['cache_db']}",
        f"storage_root: {payload['storage_root']}",
        f"project_root: {payload.get('project_root') or 'unresolved'}",
        f"project_root_source: {payload.get('project_root_source') or 'unknown'}",
        f"yt-dlp: {payload['binaries'].get('yt_dlp') or 'missing'}",
        f"ffmpeg: {payload['binaries'].get('ffmpeg') or 'missing'}",
    ]
    requested_project_root = payload.get("requested_project_root")
    if requested_project_root and requested_project_root != payload.get("project_root"):
        lines.insert(7, f"requested_project_root: {requested_project_root}")
    packaging = payload.get("packaging")
    if packaging:
        blockers = packaging.get("blockers")
        if blockers is None:
            blockers = _packaging_blockers(
                has_pip=bool(packaging.get("pip")),
                has_build_backend=bool(packaging.get("setuptools_build_meta")),
                has_wheel=bool(packaging.get("wheel")),
            )
        optional_gaps = packaging.get("optional_gaps")
        if optional_gaps is None:
            optional_gaps = ["venv"] if not packaging.get("venv") else []
        strategy = packaging.get("console_script_strategy")
        if strategy is None:
            strategy = _console_script_strategy(
                has_venv=bool(packaging.get("venv")),
                console_smoke_ready=bool(packaging.get("console_script_smoke_ready")),
            )
        lines.append("")
        lines.append("Packaging readiness:")
        lines.append(f"- pip: {_availability_text(packaging.get('pip'))}")
        lines.append(f"- venv: {_availability_text(packaging.get('venv'))}")
        lines.append(
            f"- setuptools.build_meta: {_availability_text(packaging.get('setuptools_build_meta'))}"
        )
        lines.append(f"- wheel: {_availability_text(packaging.get('wheel'))}")
        lines.append(f"- wheel build: {'ready' if packaging['wheel_build_ready'] else 'blocked'}")
        lines.append(
            f"- python -m smoke: {'ready' if packaging['python_module_smoke_ready'] else 'blocked'}"
        )
        lines.append(
            f"- console script smoke: {'ready' if packaging['console_script_smoke_ready'] else 'blocked'}"
        )
        if packaging.get("bootstrap_build_deps_ready"):
            bootstrap_requirements = ", ".join(packaging.get("bootstrap_build_requirements") or [])
            bootstrap_strategy = packaging.get("bootstrap_console_script_strategy") or "unknown"
            lines.append(
                f"- bootstrap build deps: ready ({bootstrap_requirements}; strategy={bootstrap_strategy})"
            )
        if packaging.get("error"):
            lines.append(f"- error: {packaging['error']}")
        lines.append(f"- blockers: {', '.join(blockers) if blockers else 'none'}")
        if optional_gaps:
            lines.append(f"- optional gaps: {', '.join(optional_gaps)}")
        lines.append(
            f"- console script strategy: {'prefix fallback' if strategy == 'prefix-install' else strategy}"
        )
    candidate_lines = _packaging_candidate_lines(payload)
    if candidate_lines:
        lines.append("")
        lines.append("Auto-discovered packaging candidates:")
        lines.extend(candidate_lines)
    if payload.get("recent_sources"):
        lines.append("")
        lines.append("Recent source status:")
        for item in payload["recent_sources"]["sources"]:
            status = item["recent_status"]
            lines.append(
                f"- {item['source']} ({item['channel']}, p{item['priority']}): "
                f"ok={status['ok']} skipped={status['skipped']} degraded={status.get('degraded')} latency_ms={status.get('latency_ms')}"
            )
    if payload.get("recent_manifests"):
        lines.append("")
        lines.append("Recent video manifests:")
        for item in payload["recent_manifests"]:
            lines.append(f"- {item['url']} [{item.get('preset', '-')}]")
    if payload.get("advice"):
        lines.append("")
        lines.append("Advice:")
        for item in payload["advice"]:
            lines.append(f"- {item}")
    return "\n".join(lines)


def _doctor_advice(payload: dict[str, Any]) -> list[str]:
    advice: list[str] = []
    binaries = payload.get("binaries", {})
    if not binaries.get("yt_dlp"):
        advice.append("Install yt-dlp to enable video info, download, and subtitle commands.")
    if not binaries.get("ffmpeg"):
        advice.append("Install ffmpeg to enable merged downloads and audio post-processing.")

    packaging = payload.get("packaging", {})
    packaging_subject = _packaging_python_subject(payload)
    bootstrap_requested = bool(payload.get("packaging_bootstrap_build_deps_requested"))
    auto_selected = payload.get("packaging_python_source") == "auto" and payload.get("packaging_python_auto_selected")
    auto_unresolved = payload.get("packaging_python_source") == "auto" and not payload.get("packaging_python_auto_selected")
    if auto_selected:
        if packaging and packaging.get("bootstrap_build_deps_ready") and not packaging.get("full_packaging_smoke_ready"):
            advice.append(
                f"Auto-selected bootstrap-capable packaging Python {payload.get('packaging_python')}. Export {_PACKAGING_PYTHON_ENV}="
                f"{payload.get('packaging_python')} in shared CI/ops if you want a fixed canonical interpreter."
            )
        else:
            advice.append(
                f"Auto-selected packaging Python {payload.get('packaging_python')}. Export {_PACKAGING_PYTHON_ENV}="
                f"{payload.get('packaging_python')} in shared CI/ops if you want a fixed canonical interpreter."
            )
    elif auto_unresolved:
        target = "packaging-ready or bootstrap-capable" if bootstrap_requested else "packaging-ready"
        advice.append(
            f"Auto-discovery did not find a {target} interpreter. Provision one with `pip`, "
            "`setuptools.build_meta`, and `wheel`, then set RESOURCE_HUNTER_PACKAGING_PYTHON to its path "
            "or keep using `auto` once the interpreter is discoverable on PATH. If you are validating from outside "
            "the checkout, pass `--project-root` so bootstrap-capable discovery can inspect the target project."
        )
    packaging_error = packaging.get("error") if packaging else None
    if packaging_error:
        advice.append(
            f"{packaging_subject} could not be inspected for packaging readiness: {packaging_error}. "
            "Check the interpreter path or pass a working Python via --python."
        )
    else:
        if packaging and not packaging.get("pip"):
            advice.append(f"{packaging_subject} lacks `pip`, so package installation smoke cannot run.")
        if packaging and not packaging.get("setuptools_build_meta"):
            advice.append(
                f"{packaging_subject} lacks `setuptools.build_meta`, so wheel-build smoke cannot run. "
                "Use a packaging-capable interpreter or install setuptools."
            )
        if packaging and not packaging.get("wheel"):
            advice.append(
                f"{packaging_subject} lacks the `wheel` package required by this project's declared build-system, "
                "so `python -m pip wheel --no-build-isolation` smoke cannot run here."
            )
        if packaging and packaging.get("pip") and (
            not packaging.get("setuptools_build_meta") or not packaging.get("wheel")
        ):
            advice.append(
                f"{packaging_subject} can still run `packaging-smoke --bootstrap-build-deps` to install the "
                "declared build requirements into a disposable overlay for this checkout."
            )
        if packaging and not packaging.get("venv") and packaging.get("console_script_smoke_ready"):
            advice.append(
                f"{packaging_subject} lacks stdlib `venv`, so packaging smoke will use a temporary "
                "`pip install --prefix` fallback instead of an isolated virtual environment."
            )

    cache_parent = os.path.dirname(payload["cache_db"])
    if not os.access(payload["storage_root"], os.W_OK):
        advice.append("Storage root is not writable. Set RESOURCE_HUNTER_HOME to a writable directory.")
    elif not os.access(cache_parent, os.W_OK):
        advice.append("Cache directory is not writable. Check RESOURCE_HUNTER_HOME or OPENCLAW_WORKSPACE permissions.")

    recent_sources = payload.get("recent_sources", {}).get("sources", [])
    degraded_count = sum(1 for item in recent_sources if item.get("recent_status", {}).get("degraded"))
    failed_count = sum(1 for item in recent_sources if item.get("recent_status", {}).get("ok") is False)
    if recent_sources and degraded_count >= max(2, len(recent_sources) // 2):
        advice.append("Several sources are degraded. Run `hunt.py sources --probe --json` to refresh health status.")
    if failed_count == len(recent_sources) and recent_sources:
        advice.append("All sources failed on the last run. Check network connectivity or upstream site availability.")
    return advice


def _doctor_payload(
    engine: ResourceHunterEngine,
    *,
    probe: bool,
    python_executable: str | None = None,
    bootstrap_build_deps: bool = False,
    project_root: str | None = None,
) -> dict[str, Any]:
    (
        packaging_python,
        packaging_python_source,
        packaging_python_candidates,
        packaging_python_auto_selected,
    ) = _effective_packaging_python(
        python_executable,
        bootstrap_build_deps=bootstrap_build_deps,
        project_root=project_root,
    )
    video_manager = VideoManager(engine.cache)
    video_doctor = video_manager.doctor()
    packaging = _packaging_status(python_executable=packaging_python)
    packaging = packaging_tools.annotate_project_packaging_status(
        packaging,
        project_root=project_root,
        include_bootstrap_metadata=bootstrap_build_deps,
    )
    payload = {
        "version": __version__,
        "python": sys.executable,
        "packaging_python": packaging_python or sys.executable,
        "packaging_python_source": packaging_python_source,
        "stdout_encoding": getattr(sys.stdout, "encoding", None),
        "cache_db": str(engine.cache.db_path),
        "storage_root": str(storage_root()),
        "project_root": packaging.get("project_root"),
        "project_root_source": packaging.get("project_root_source"),
        "binaries": video_doctor["binaries"],
        "packaging": packaging,
        "packaging_bootstrap_build_deps_requested": bootstrap_build_deps,
        "recent_sources": engine.source_catalog(probe=probe),
        "recent_manifests": video_doctor["recent_manifests"],
    }
    if packaging.get("requested_project_root") is not None:
        payload["requested_project_root"] = packaging["requested_project_root"]
    if packaging_python_candidates is not None:
        payload["packaging_python_candidates"] = packaging_python_candidates
    if packaging_python_source == "auto":
        payload["packaging_python_auto_selected"] = packaging_python_auto_selected
    payload["advice"] = _doctor_advice(payload)
    return payload


def _packaging_gate_failure(payload: dict[str, Any], *, allow_bootstrap_build_deps: bool = False) -> str | None:
    packaging = payload.get("packaging")
    auto_unresolved = payload.get("packaging_python_source") == "auto" and not payload.get("packaging_python_auto_selected")
    target = "packaging-ready or bootstrap-capable interpreter" if allow_bootstrap_build_deps else "packaging-ready interpreter"
    if not packaging:
        if auto_unresolved:
            return f"Packaging gate failed: auto-discovery found no {target}."
        return "Packaging gate failed: packaging status is unavailable in doctor output."

    packaging_error = packaging.get("error")
    blockers = packaging.get("blockers")
    if blockers is None:
        blockers = _packaging_blockers(
            has_pip=bool(packaging.get("pip")),
            has_build_backend=bool(packaging.get("setuptools_build_meta")),
            has_wheel=bool(packaging.get("wheel")),
        )
    if auto_unresolved:
        if packaging_error:
            return (
                f"Packaging gate failed: auto-discovery found no {target}; "
                f"fallback {payload.get('packaging_python')} could not be inspected: {packaging_error}"
            )
        if blockers:
            if allow_bootstrap_build_deps and packaging.get("packaging_smoke_ready_with_bootstrap"):
                return None
            return (
                f"Packaging gate failed: auto-discovery found no {target}; "
                f"fallback {payload.get('packaging_python')} blockers={', '.join(blockers)}"
            )
        if allow_bootstrap_build_deps and packaging.get("packaging_smoke_ready_with_bootstrap"):
            return None
        return f"Packaging gate failed: auto-discovery found no {target}."
    if packaging_error:
        return f"Packaging gate failed: {packaging_error}"

    if blockers:
        if allow_bootstrap_build_deps and packaging.get("packaging_smoke_ready_with_bootstrap"):
            return None
        return f"Packaging gate failed for {payload.get('packaging_python')}: blockers={', '.join(blockers)}"

    if packaging.get("full_packaging_smoke_ready"):
        return None

    if allow_bootstrap_build_deps and packaging.get("packaging_smoke_ready_with_bootstrap"):
        return None

    strategy = packaging.get("console_script_strategy")
    if strategy is None:
        strategy = _console_script_strategy(
            has_venv=bool(packaging.get("venv")),
            console_smoke_ready=bool(packaging.get("console_script_smoke_ready")),
        )
    return (
        f"Packaging gate failed for {payload.get('packaging_python')}: "
        f"full packaging smoke is blocked (strategy={strategy})."
    )


def _capture_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _emit_json_payload(payload: dict[str, Any], *, output_path: str | None = None) -> None:
    text = dump_json(payload)
    if output_path and output_path != "-":
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(f"{text}\n", encoding="utf-8")
    print(text)


def _packaging_capture_args(
    *,
    project_root: str | None,
    python_executable: str | None,
    bootstrap_build_deps: bool,
) -> argparse.Namespace:
    return argparse.Namespace(
        project_root=project_root,
        python=python_executable,
        bootstrap_build_deps=bootstrap_build_deps,
        output=None,
        json=True,
    )


def _packaging_capture_payload(engine: ResourceHunterEngine, args: argparse.Namespace) -> dict[str, Any]:
    doctor_payload = _doctor_payload(
        engine,
        probe=False,
        python_executable=args.python,
        bootstrap_build_deps=args.bootstrap_build_deps,
        project_root=args.project_root,
    )
    packaging_python_source = doctor_payload.get("packaging_python_source")
    smoke_payload = packaging_tools.run_packaging_smoke(
        project_root=args.project_root,
        python_executable=doctor_payload.get("packaging_python"),
        packaging_python_source=packaging_python_source,
        packaging_python_candidates=doctor_payload.get("packaging_python_candidates"),
        packaging_python_auto_selected=(
            doctor_payload.get("packaging_python_auto_selected") if packaging_python_source == "auto" else None
        ),
        bootstrap_build_deps=args.bootstrap_build_deps,
    )
    payload: dict[str, Any] = {
        "schema_version": _PACKAGING_CAPTURE_SCHEMA_VERSION,
        "captured_at": _capture_timestamp(),
        "project_root": smoke_payload.get("project_root") or doctor_payload.get("project_root"),
        "project_root_source": smoke_payload.get("project_root_source") or doctor_payload.get("project_root_source"),
        "packaging_python": smoke_payload.get("packaging_python") or doctor_payload.get("packaging_python"),
        "packaging_python_source": smoke_payload.get("packaging_python_source")
        or doctor_payload.get("packaging_python_source"),
        "bootstrap_build_deps_requested": args.bootstrap_build_deps,
        "failed_step": smoke_payload.get("failed_step"),
        "doctor": doctor_payload,
        "packaging_smoke": smoke_payload,
        "summary": {
            "doctor_packaging_ready": (
                _packaging_gate_failure(
                    doctor_payload,
                    allow_bootstrap_build_deps=args.bootstrap_build_deps,
                )
                is None
            ),
            "packaging_smoke_ok": bool(smoke_payload.get("ok")),
            "strategy": smoke_payload.get("strategy"),
            "strategy_family": smoke_payload.get("strategy_family"),
            "reason": smoke_payload.get("reason"),
        },
    }
    requested_project_root = smoke_payload.get("requested_project_root")
    if requested_project_root is None:
        requested_project_root = doctor_payload.get("requested_project_root")
    if requested_project_root is not None:
        payload["requested_project_root"] = requested_project_root
    packaging_python_candidates = smoke_payload.get("packaging_python_candidates")
    if packaging_python_candidates is None:
        packaging_python_candidates = doctor_payload.get("packaging_python_candidates")
    if packaging_python_candidates is not None:
        payload["packaging_python_candidates"] = packaging_python_candidates
    packaging_python_auto_selected = smoke_payload.get("packaging_python_auto_selected")
    if packaging_python_auto_selected is None:
        packaging_python_auto_selected = doctor_payload.get("packaging_python_auto_selected")
    if packaging_python_auto_selected is not None:
        payload["packaging_python_auto_selected"] = packaging_python_auto_selected
    require_packaging_ready = bool(getattr(args, "require_packaging_ready", False))
    require_smoke_ok = bool(getattr(args, "require_smoke_ok", False))
    requirement_failures = _packaging_capture_requirement_failures(
        payload,
        require_packaging_ready=require_packaging_ready,
        require_smoke_ok=require_smoke_ok,
    )
    payload["requirements"] = {
        "require_packaging_ready": require_packaging_ready,
        "require_smoke_ok": require_smoke_ok,
        "ok": len(requirement_failures) == 0,
        "failures": requirement_failures,
    }
    return payload


def _write_json_artifact(destination: Path, payload: dict[str, Any]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(f"{dump_json(payload)}\n", encoding="utf-8")


def _default_blocked_python(output_dir: Path) -> str:
    suffix = ".exe" if os.name == "nt" else ""
    blocked_root = output_dir / "__blocked_python__"
    candidate = blocked_root / f"missing-resource-hunter-python{suffix}"
    index = 1
    while candidate.exists():
        candidate = blocked_root / f"missing-resource-hunter-python-{index}{suffix}"
        index += 1
    return str(candidate.resolve())


def _packaging_baseline_capture_entry(capture_path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    capture_summary = payload.get("summary", {})
    entry: dict[str, Any] = {
        "path": str(capture_path),
        "project_root": payload.get("project_root"),
        "project_root_source": payload.get("project_root_source"),
        "packaging_python": payload.get("packaging_python"),
        "packaging_python_source": payload.get("packaging_python_source"),
        "doctor_packaging_ready": capture_summary.get("doctor_packaging_ready"),
        "packaging_smoke_ok": capture_summary.get("packaging_smoke_ok"),
        "strategy": capture_summary.get("strategy"),
        "strategy_family": capture_summary.get("strategy_family"),
        "reason": capture_summary.get("reason"),
        "failed_step": payload.get("failed_step"),
    }
    requested_project_root = payload.get("requested_project_root")
    if requested_project_root is not None:
        entry["requested_project_root"] = requested_project_root
    packaging_python_auto_selected = payload.get("packaging_python_auto_selected")
    if packaging_python_auto_selected is not None:
        entry["packaging_python_auto_selected"] = packaging_python_auto_selected
    return entry


def _packaging_baseline_expected_outcome(
    *,
    expect_ready: bool,
    expect_smoke_ok: bool,
    expect_failed_step: bool,
    expected_strategy_families: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    expected: dict[str, Any] = {
        "doctor_packaging_ready": expect_ready,
        "packaging_smoke_ok": expect_smoke_ok,
        "failed_step_present": expect_failed_step,
    }
    if expected_strategy_families is not None:
        expected["strategy_family_any_of"] = list(expected_strategy_families)
    return expected


def _packaging_baseline_expectation_issues(
    capture: dict[str, Any],
    *,
    capture_name: str,
    label: str,
    expected_outcome: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    expect_ready = expected_outcome["doctor_packaging_ready"]
    expect_smoke_ok = expected_outcome["packaging_smoke_ok"]
    expect_failed_step = expected_outcome["failed_step_present"]
    expected_strategy_families_raw = expected_outcome.get("strategy_family_any_of")
    expected_strategy_families = tuple(expected_strategy_families_raw) if expected_strategy_families_raw else None
    if capture.get("doctor_packaging_ready") is not expect_ready:
        issues.append(
            {
                "capture": capture_name,
                "field": "doctor_packaging_ready",
                "kind": "value_mismatch",
                "expected": expect_ready,
                "actual": capture.get("doctor_packaging_ready"),
                "message": (
                    f"{label} capture did not report doctor_packaging_ready={str(expect_ready).lower()}."
                ),
            }
        )
    if capture.get("packaging_smoke_ok") is not expect_smoke_ok:
        issues.append(
            {
                "capture": capture_name,
                "field": "packaging_smoke_ok",
                "kind": "value_mismatch",
                "expected": expect_smoke_ok,
                "actual": capture.get("packaging_smoke_ok"),
                "message": (
                    f"{label} capture did not report packaging_smoke_ok={str(expect_smoke_ok).lower()}."
                ),
            }
        )
    failed_step = capture.get("failed_step")
    if expect_failed_step and failed_step is None:
        issues.append(
            {
                "capture": capture_name,
                "field": "failed_step",
                "kind": "missing_failed_step",
                "expected_present": True,
                "actual": failed_step,
                "message": f"{label} capture did not report failed_step.",
            }
        )
    if not expect_failed_step and failed_step is not None:
        issues.append(
            {
                "capture": capture_name,
                "field": "failed_step",
                "kind": "unexpected_failed_step",
                "expected_present": False,
                "actual": failed_step,
                "message": f"{label} capture unexpectedly reported failed_step={failed_step}.",
            }
        )
    if expected_strategy_families is not None and capture.get("strategy_family") not in expected_strategy_families:
        formatted_families = ", ".join(expected_strategy_families)
        issues.append(
            {
                "capture": capture_name,
                "field": "strategy_family",
                "kind": "strategy_mismatch",
                "expected_any_of": list(expected_strategy_families),
                "actual": capture.get("strategy_family"),
                "message": f"{label} capture did not report strategy_family in [{formatted_families}].",
            }
        )
    return issues


def _packaging_capture_requirement_failures(
    payload: dict[str, Any],
    *,
    require_packaging_ready: bool,
    require_smoke_ok: bool,
) -> list[str]:
    failures: list[str] = []
    summary = payload.get("summary", {})
    if require_packaging_ready and not summary.get("doctor_packaging_ready"):
        doctor_payload = payload.get("doctor")
        gate_failure = None
        if isinstance(doctor_payload, dict):
            gate_failure = _packaging_gate_failure(
                doctor_payload,
                allow_bootstrap_build_deps=bool(payload.get("bootstrap_build_deps_requested")),
            )
        failures.append(gate_failure or "Packaging capture requirement failed: doctor did not report packaging-ready.")
    if require_smoke_ok and not summary.get("packaging_smoke_ok"):
        failed_step = payload.get("failed_step")
        reason = summary.get("reason")
        if failed_step and reason:
            failures.append(
                f"Packaging capture requirement failed: packaging smoke did not pass "
                f"(failed_step={failed_step}): {reason}"
            )
        elif failed_step:
            failures.append(
                f"Packaging capture requirement failed: packaging smoke did not pass "
                f"(failed_step={failed_step})."
            )
        elif reason:
            failures.append(f"Packaging capture requirement failed: packaging smoke did not pass: {reason}")
        else:
            failures.append("Packaging capture requirement failed: packaging smoke did not pass.")
    return failures


def _packaging_baseline_requirement_failures(
    payload: dict[str, Any],
    *,
    require_expected_outcomes: bool,
) -> list[str]:
    if not require_expected_outcomes:
        return []
    summary = payload.get("summary", {})
    if summary.get("baseline_contract_ok"):
        return []
    warnings = payload.get("warnings")
    if isinstance(warnings, list):
        warning_messages = [warning for warning in warnings if isinstance(warning, str) and warning.strip()]
        if warning_messages:
            return [f"Packaging baseline requirement failed: {warning}" for warning in warning_messages]
    return [
        "Packaging baseline requirement failed: expected passing and blocked capture outcomes were not met."
    ]


def _packaging_baseline(engine: ResourceHunterEngine, args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir or Path("artifacts") / "packaging-baseline").resolve()
    passing_payload = _packaging_capture_payload(
        engine,
        _packaging_capture_args(
            project_root=args.project_root,
            python_executable=args.python,
            bootstrap_build_deps=args.bootstrap_build_deps,
        ),
    )
    blocked_python = args.blocked_python or _default_blocked_python(output_dir)
    blocked_payload = _packaging_capture_payload(
        engine,
        _packaging_capture_args(
            project_root=args.project_root,
            python_executable=blocked_python,
            bootstrap_build_deps=args.bootstrap_build_deps,
        ),
    )

    passing_path = output_dir / "passing-packaging-capture.json"
    blocked_path = output_dir / "blocked-packaging-capture.json"
    baseline_path = output_dir / "packaging-baseline.json"

    _write_json_artifact(passing_path, passing_payload)
    _write_json_artifact(blocked_path, blocked_payload)

    passing_capture = _packaging_baseline_capture_entry(passing_path, passing_payload)
    blocked_capture = _packaging_baseline_capture_entry(blocked_path, blocked_payload)
    passing_expected_outcome = _packaging_baseline_expected_outcome(
        expect_ready=True,
        expect_smoke_ok=True,
        expect_failed_step=False,
        expected_strategy_families=("usable",),
    )
    blocked_expected_outcome = _packaging_baseline_expected_outcome(
        expect_ready=False,
        expect_smoke_ok=False,
        expect_failed_step=True,
        expected_strategy_families=("blocked",),
    )
    passing_capture["expected_outcome"] = passing_expected_outcome
    blocked_capture["expected_outcome"] = blocked_expected_outcome
    passing_issues = _packaging_baseline_expectation_issues(
        passing_capture,
        capture_name="passing",
        label="Passing",
        expected_outcome=passing_expected_outcome,
    )
    blocked_issues = _packaging_baseline_expectation_issues(
        blocked_capture,
        capture_name="blocked",
        label="Blocked",
        expected_outcome=blocked_expected_outcome,
    )
    passing_capture["matches_expectation"] = len(passing_issues) == 0
    passing_capture["expectation_drift"] = passing_issues
    blocked_capture["matches_expectation"] = len(blocked_issues) == 0
    blocked_capture["expectation_drift"] = blocked_issues
    warnings = [
        issue["message"]
        for issue in [
            *passing_issues,
            *blocked_issues,
        ]
    ]
    summary = {
        "passing_capture_matches_expectation": passing_capture["matches_expectation"],
        "blocked_capture_matches_expectation": blocked_capture["matches_expectation"],
    }
    summary["baseline_contract_ok"] = (
        summary["passing_capture_matches_expectation"] and summary["blocked_capture_matches_expectation"]
    )

    payload: dict[str, Any] = {
        "schema_version": _PACKAGING_BASELINE_SCHEMA_VERSION,
        "captured_at": _capture_timestamp(),
        "output_dir": str(output_dir),
        "bootstrap_build_deps_requested": args.bootstrap_build_deps,
        "project_root": passing_payload.get("project_root") or blocked_payload.get("project_root"),
        "project_root_source": passing_payload.get("project_root_source") or blocked_payload.get("project_root_source"),
        "blocked_python": blocked_python,
        "passing_capture": passing_capture,
        "blocked_capture": blocked_capture,
        "summary": summary,
        "warnings": warnings,
    }
    requested_project_root = passing_payload.get("requested_project_root")
    if requested_project_root is None:
        requested_project_root = blocked_payload.get("requested_project_root")
    if requested_project_root is not None:
        payload["requested_project_root"] = requested_project_root
    require_expected_outcomes = bool(getattr(args, "require_expected_outcomes", False))
    requirement_failures = _packaging_baseline_requirement_failures(
        payload,
        require_expected_outcomes=require_expected_outcomes,
    )
    payload["requirements"] = {
        "require_expected_outcomes": require_expected_outcomes,
        "ok": len(requirement_failures) == 0,
        "failures": requirement_failures,
    }

    _write_json_artifact(baseline_path, payload)
    print(dump_json(payload))
    requirements = payload.get("requirements")
    failures = requirements.get("failures") if isinstance(requirements, dict) else None
    if failures is None:
        failures = _packaging_baseline_requirement_failures(
            payload,
            require_expected_outcomes=require_expected_outcomes,
        )
    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 2
    return 0


def _packaging_baseline_report(args: argparse.Namespace) -> int:
    try:
        if getattr(args, "github_run", None):
            report_payload = packaging_report.read_packaging_baseline_reports_from_github_run(
                args.github_run,
                repo=args.repo,
                github_workflow=args.github_workflow,
                github_run_list_limit=args.github_run_list_limit,
                artifact_names=args.artifact_names,
                artifact_patterns=args.artifact_patterns,
                download_dir=args.download_dir,
                keep_download_dir=args.keep_download_dir,
            )
        else:
            report_payload = packaging_report.read_packaging_baseline_reports(getattr(args, "paths", None))
    except ResourceHunterError as exc:
        if getattr(args, "json", False):
            print(
                dump_json(
                    packaging_report.build_packaging_baseline_report_error_payload(
                        str(exc),
                        download_payload=getattr(exc, "download_payload", None),
                    )
                )
            )
        print(str(exc), file=sys.stderr)
        return 1
    if getattr(args, "json", False):
        print(dump_json(report_payload))
    else:
        print(packaging_report.format_packaging_baseline_report_text(report_payload))
    if getattr(args, "require_contract_ok", False):
        failures = packaging_report.packaging_baseline_report_requirement_failures(report_payload)
        if failures:
            for failure in failures:
                print(failure, file=sys.stderr)
            return 2
    return 0


def _packaging_baseline_verify(args: argparse.Namespace) -> int:
    try:
        if args.github_run:
            payload = packaging_verify.verify_packaging_baseline_github_run(
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
            payload = packaging_verify.verify_packaging_baseline_artifacts(
                args.paths,
                output_dir=args.output_dir,
                output_archive=args.output_archive,
                archive_downloads=args.archive_downloads,
                required_artifact_count=args.require_artifact_count,
            )
    except ResourceHunterError as exc:
        payload = packaging_verify.build_packaging_baseline_verify_error_payload(
            str(exc),
            download_payload=getattr(exc, "download_payload", None),
        )
        if args.output_dir:
            packaging_verify._persist_verify_outputs(
                payload,
                Path(args.output_dir),
                output_archive=args.output_archive,
                archive_downloads=args.archive_downloads,
            )
        if getattr(args, "json", False):
            print(dump_json(payload))
        else:
            print(packaging_verify.format_packaging_baseline_verify_text(payload))
        print(str(exc), file=sys.stderr)
        return 1

    if getattr(args, "json", False):
        print(dump_json(payload))
    else:
        print(packaging_verify.format_packaging_baseline_verify_text(payload))

    if payload.get("gate_ok") is False:
        if getattr(args, "json", False):
            gate = payload.get("gate") if isinstance(payload.get("gate"), dict) else {}
            failures = gate.get("failures") if isinstance(gate.get("failures"), list) else []
            for failure in failures:
                print(failure, file=sys.stderr)
        return 2
    return 0


def _search(engine: ResourceHunterEngine, args: argparse.Namespace) -> int:
    intent = parse_intent(
        query=args.query,
        explicit_kind=_resolve_kind(args),
        channel=_resolve_channel(args),
        quick=args.quick,
        wants_sub=args.sub,
        wants_4k=args.uhd,
    )
    if intent.is_video_url:
        video_manager = VideoManager(engine.cache)
        payload = video_manager.probe(intent.query)
        if args.json:
            print(dump_json(payload.to_dict()))
        else:
            print(format_video_text(payload, "probe"))
        return 0
    response = engine.search(intent, page=args.page, limit=args.limit, use_cache=not args.no_cache)
    effective_limit = min(args.limit, 4) if args.quick else args.limit
    response.setdefault("meta", {})
    response["meta"]["effective_limit"] = effective_limit
    response["meta"]["candidate_count"] = len(response.get("results", []))
    if args.json:
        print(dump_json(response))
    else:
        print(format_search_text(response, max_results=effective_limit))
    return 0


def _sources(engine: ResourceHunterEngine, args: argparse.Namespace) -> int:
    payload = engine.source_catalog(probe=args.probe)
    if args.json:
        print(dump_json(payload))
    else:
        print(format_sources_text(payload))
    return 0


def _doctor(engine: ResourceHunterEngine, args: argparse.Namespace) -> int:
    payload = _doctor_payload(
        engine,
        probe=args.probe,
        python_executable=args.python,
        bootstrap_build_deps=args.bootstrap_build_deps,
        project_root=args.project_root,
    )
    gate_failure = (
        _packaging_gate_failure(payload, allow_bootstrap_build_deps=args.bootstrap_build_deps)
        if args.require_packaging_ready
        else None
    )
    if args.json:
        print(dump_json(payload))
    else:
        print(_format_doctor_text(payload))
    if gate_failure:
        print(gate_failure, file=sys.stderr)
        return 2
    return 0


def _packaging_smoke(args: argparse.Namespace) -> int:
    (
        packaging_python,
        packaging_python_source,
        packaging_python_candidates,
        packaging_python_auto_selected,
    ) = _effective_packaging_python(
        args.python,
        bootstrap_build_deps=args.bootstrap_build_deps,
        project_root=args.project_root,
    )
    payload = packaging_tools.run_packaging_smoke(
        project_root=args.project_root,
        python_executable=packaging_python,
        packaging_python_source=packaging_python_source,
        packaging_python_candidates=packaging_python_candidates,
        packaging_python_auto_selected=packaging_python_auto_selected if packaging_python_source == "auto" else None,
        bootstrap_build_deps=args.bootstrap_build_deps,
    )
    if args.json:
        print(dump_json(payload))
    else:
        print(packaging_tools.format_packaging_smoke_text(payload))
    if payload.get("ok"):
        return 0
    print(payload.get("reason") or "Packaging smoke failed.", file=sys.stderr)
    return 2


def _packaging_capture(engine: ResourceHunterEngine, args: argparse.Namespace) -> int:
    payload = _packaging_capture_payload(engine, args)
    _emit_json_payload(payload, output_path=args.output)
    requirements = payload.get("requirements")
    failures = requirements.get("failures") if isinstance(requirements, dict) else None
    if failures is None:
        failures = _packaging_capture_requirement_failures(
            payload,
            require_packaging_ready=args.require_packaging_ready,
            require_smoke_ok=args.require_smoke_ok,
        )
    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 2
    return 0


def _video(engine: ResourceHunterEngine, args: argparse.Namespace) -> int:
    video_manager = VideoManager(engine.cache)
    if args.video_cmd == "info":
        payload = video_manager.info(args.url)
    elif args.video_cmd == "probe":
        payload = video_manager.probe(args.url)
    elif args.video_cmd == "download":
        payload = video_manager.download(args.url, preset=args.format, output_dir=args.dir)
    elif args.video_cmd == "subtitle":
        payload = video_manager.subtitle(args.url, lang=args.lang)
    else:
        raise ResourceHunterError(f"unsupported video command: {args.video_cmd}")
    if getattr(args, "json", False):
        print(dump_json(payload.to_dict()))
    else:
        print(format_video_text(payload, args.video_cmd))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resource Hunter v2")
    parser.add_argument("--version", action="version", version=f"resource-hunter {__version__}")
    parser.add_argument("--debug", action="store_true", help="show traceback on errors")
    sub = parser.add_subparsers(dest="command")

    p_search = sub.add_parser("search", help="Search public pan/torrent resources")
    p_search.add_argument("query", help="keyword or public video url")
    p_search.add_argument("--kind", choices=["movie", "tv", "anime", "music", "software", "book", "general"])
    p_search.add_argument("--channel", choices=["both", "pan", "torrent"], default="both")
    p_search.add_argument("--movie", action="store_true")
    p_search.add_argument("--tv", action="store_true")
    p_search.add_argument("--anime", action="store_true")
    p_search.add_argument("--music", action="store_true")
    p_search.add_argument("--software", action="store_true")
    p_search.add_argument("--book", action="store_true")
    p_search.add_argument("--general", action="store_true")
    p_search.add_argument("--pan-only", action="store_true")
    p_search.add_argument("--torrent-only", action="store_true")
    p_search.add_argument("--page", type=int, default=1)
    p_search.add_argument("--limit", type=int, default=8)
    p_search.add_argument("--quick", action="store_true")
    p_search.add_argument("--sub", action="store_true")
    p_search.add_argument("--4k", action="store_true", dest="uhd")
    p_search.add_argument("--json", action="store_true")
    p_search.add_argument("--no-cache", action="store_true")

    p_sources = sub.add_parser("sources", help="Show configured resource sources")
    p_sources.add_argument("--probe", action="store_true")
    p_sources.add_argument("--json", action="store_true")

    p_doctor = sub.add_parser("doctor", help="Check dependencies and cached health")
    p_doctor.add_argument("--probe", action="store_true")
    p_doctor.add_argument("--json", action="store_true")
    p_doctor.add_argument(
        "--project-root",
        help="project root used for bootstrap-aware packaging inspection; defaults to cwd or a detected parent",
    )
    p_doctor.add_argument(
        "--python",
        help=(
            "python interpreter to inspect for packaging readiness; defaults to "
            f"{_PACKAGING_PYTHON_ENV} or the current interpreter; pass `{_AUTO_PACKAGING_PYTHON}` "
            "to auto-select the first packaging-ready interpreter discovered on this machine"
        ),
    )
    p_doctor.add_argument(
        "--require-packaging-ready",
        action="store_true",
        help="exit with code 2 when packaging smoke is blocked",
    )
    p_doctor.add_argument(
        "--bootstrap-build-deps",
        action="store_true",
        help="treat disposable build-dependency bootstrapping as an acceptable packaging route for auto-selection and gating",
    )

    p_packaging_smoke = sub.add_parser("packaging-smoke", help="Build and smoke-test the installable package")
    p_packaging_smoke.add_argument(
        "--project-root",
        help="project root to package; defaults to cwd or a detected parent",
    )
    p_packaging_smoke.add_argument(
        "--python",
        help=(
            "python interpreter to build and smoke-test with; defaults to "
            f"{_PACKAGING_PYTHON_ENV} or the current interpreter; pass `{_AUTO_PACKAGING_PYTHON}` "
            "to auto-select the first packaging-ready interpreter discovered on this machine; combine with "
            "`--bootstrap-build-deps` to also accept bootstrap-capable interpreters"
        ),
    )
    p_packaging_smoke.add_argument(
        "--bootstrap-build-deps",
        action="store_true",
        help="temporarily install missing declared build requirements into a disposable overlay before building",
    )
    p_packaging_smoke.add_argument("--json", action="store_true")

    p_packaging_capture = sub.add_parser(
        "packaging-capture",
        help="Capture doctor + packaging-smoke JSON for CI or ops baseline artifacts",
    )
    p_packaging_capture.add_argument(
        "--project-root",
        help="project root to inspect and package; defaults to cwd or a detected parent",
    )
    p_packaging_capture.add_argument(
        "--python",
        help=(
            "python interpreter to inspect and smoke-test with; defaults to "
            f"{_PACKAGING_PYTHON_ENV} or the current interpreter; pass `{_AUTO_PACKAGING_PYTHON}` "
            "to auto-select the first packaging-ready interpreter discovered on this machine"
        ),
    )
    p_packaging_capture.add_argument(
        "--bootstrap-build-deps",
        action="store_true",
        help="treat disposable build-dependency bootstrapping as an acceptable packaging route for capture",
    )
    p_packaging_capture.add_argument(
        "--output",
        help="optional path to also write the bundled JSON capture artifact",
    )
    p_packaging_capture.add_argument(
        "--require-packaging-ready",
        action="store_true",
        help="exit with code 2 after writing the capture when doctor does not report packaging-ready",
    )
    p_packaging_capture.add_argument(
        "--require-smoke-ok",
        action="store_true",
        help="exit with code 2 after writing the capture when packaging-smoke does not pass",
    )
    p_packaging_capture.add_argument(
        "--json",
        action="store_true",
        help="reserved for consistency; packaging-capture always emits JSON",
    )

    p_packaging_baseline = sub.add_parser(
        "packaging-baseline",
        help="Write one passing and one intentionally blocked packaging capture bundle",
    )
    p_packaging_baseline.add_argument(
        "--project-root",
        help="project root to inspect and package; defaults to cwd or a detected parent",
    )
    p_packaging_baseline.add_argument(
        "--python",
        help=(
            "python interpreter to use for the passing capture; defaults to "
            f"{_PACKAGING_PYTHON_ENV} or the current interpreter; pass `{_AUTO_PACKAGING_PYTHON}` "
            "to auto-select the first packaging-ready interpreter discovered on this machine"
        ),
    )
    p_packaging_baseline.add_argument(
        "--blocked-python",
        help="optional interpreter path to use for the intentionally blocked capture; defaults to a generated missing path",
    )
    p_packaging_baseline.add_argument(
        "--bootstrap-build-deps",
        action="store_true",
        help="treat disposable build-dependency bootstrapping as an acceptable packaging route for the passing capture",
    )
    p_packaging_baseline.add_argument(
        "--output-dir",
        help="directory that receives passing-packaging-capture.json, blocked-packaging-capture.json, and packaging-baseline.json",
    )
    p_packaging_baseline.add_argument(
        "--require-expected-outcomes",
        action="store_true",
        help="exit with code 2 after writing artifacts when the passing capture does not pass or the blocked capture does not fail as expected",
    )
    p_packaging_baseline.add_argument(
        "--json",
        action="store_true",
        help="reserved for consistency; packaging-baseline always emits JSON",
    )

    p_packaging_baseline_report = sub.add_parser(
        "packaging-baseline-report",
        help="Render a normalized report from a packaging-baseline.json artifact",
    )
    p_packaging_baseline_report.add_argument(
        "paths",
        nargs="*",
        help=(
            "artifact file(s), .zip archive(s), or directories to scan recursively for packaging-baseline.json and nested .zip archives; "
            "defaults to artifacts/packaging-baseline/packaging-baseline.json"
        ),
    )
    p_packaging_baseline_report.add_argument(
        "--json",
        action="store_true",
        help="emit normalized JSON; when multiple artifacts are discovered the payload becomes an aggregate report",
    )
    p_packaging_baseline_report.add_argument(
        "--require-contract-ok",
        action="store_true",
        help="exit with code 2 after printing the report when any artifact shows packaging-baseline contract drift",
    )
    p_packaging_baseline_report.add_argument(
        "--github-run",
        help=(
            "download packaging-baseline artifacts from a GitHub Actions run with `gh run download` before reporting; "
            "pass `latest` to auto-select the most recent completed resource-hunter-ci run; "
            "defaults to the resource-hunter-packaging-baseline-* artifact pattern"
        ),
    )
    p_packaging_baseline_report.add_argument(
        "--github-workflow",
        help=(
            "workflow name passed to `gh run list --workflow` when --github-run latest is used; "
            f"defaults to {packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW}"
        ),
    )
    p_packaging_baseline_report.add_argument(
        "--github-run-list-limit",
        type=packaging_gate._positive_int,
        help=(
            "max completed runs to scan when --github-run latest resolves a workflow-filtered run or "
            f"artifact-discovery fallback; defaults to {packaging_gate._GITHUB_RUN_LIST_LIMIT}"
        ),
    )
    p_packaging_baseline_report.add_argument(
        "--repo",
        help=(
            "repository passed through to `gh run download --repo`; defaults to GITHUB_REPOSITORY, "
            "then the git origin remote, then the current gh repository context"
        ),
    )
    p_packaging_baseline_report.add_argument(
        "--artifact-name",
        action="append",
        dest="artifact_names",
        help="artifact name to download from --github-run; may be passed multiple times",
    )
    p_packaging_baseline_report.add_argument(
        "--artifact-pattern",
        action="append",
        dest="artifact_patterns",
        help="artifact glob pattern to download from --github-run; may be passed multiple times",
    )
    p_packaging_baseline_report.add_argument(
        "--download-dir",
        help="directory passed to `gh run download --dir`; defaults to a temporary directory when --github-run is used",
    )
    p_packaging_baseline_report.add_argument(
        "--keep-download-dir",
        action="store_true",
        help="retain the temporary download directory created for --github-run reporting",
    )

    p_packaging_baseline_verify = sub.add_parser(
        "packaging-baseline-verify",
        help="Verify matched report/gate outputs from retained artifacts or one GitHub Actions run",
    )
    p_packaging_baseline_verify.add_argument(
        "paths",
        nargs="*",
        help=(
            "artifact file(s), .zip archive(s), or directories to scan recursively for packaging-baseline.json and nested .zip archives; "
            "defaults to artifacts/packaging-baseline/packaging-baseline.json when --github-run is omitted"
        ),
    )
    p_packaging_baseline_verify.add_argument(
        "--github-run",
        help=(
            "download packaging-baseline artifacts from a GitHub Actions run with `gh run download`; "
            "pass `latest` to auto-select the most recent completed resource-hunter-ci run"
        ),
    )
    p_packaging_baseline_verify.add_argument(
        "--github-workflow",
        help=(
            "workflow name passed to `gh run list --workflow` when --github-run latest is used; "
            f"defaults to {packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW}"
        ),
    )
    p_packaging_baseline_verify.add_argument(
        "--github-run-list-limit",
        type=packaging_verify._positive_int,
        help=(
            "max completed runs to scan when --github-run latest resolves a workflow-filtered run or "
            f"artifact-discovery fallback; defaults to {packaging_gate._GITHUB_RUN_LIST_LIMIT}"
        ),
    )
    p_packaging_baseline_verify.add_argument(
        "--repo",
        help=(
            "repository passed through to `gh run download --repo`; defaults to GITHUB_REPOSITORY, "
            "then the git origin remote, then the current gh repository context"
        ),
    )
    p_packaging_baseline_verify.add_argument(
        "--artifact-name",
        action="append",
        dest="artifact_names",
        help="artifact name to download from --github-run; may be passed multiple times",
    )
    p_packaging_baseline_verify.add_argument(
        "--artifact-pattern",
        action="append",
        dest="artifact_patterns",
        help="artifact glob pattern to download from --github-run; may be passed multiple times",
    )
    p_packaging_baseline_verify.add_argument(
        "--download-dir",
        help=(
            "directory passed to `gh run download --dir`; defaults to <output-dir>/download when --output-dir is set, "
            "otherwise a temporary directory"
        ),
    )
    p_packaging_baseline_verify.add_argument(
        "--keep-download-dir",
        action="store_true",
        help="retain the temporary download directory created for verification when --download-dir is omitted",
    )
    p_packaging_baseline_verify.add_argument(
        "--output-dir",
        help="write report.json, report.txt, gate.json, gate.txt, verify.json, and verify.txt into this directory",
    )
    p_packaging_baseline_verify.add_argument(
        "--output-archive",
        help=(
            "write a zip bundle containing the saved report.*, gate.*, verify.*, and bundle-manifest.json outputs; "
            "requires --output-dir"
        ),
    )
    p_packaging_baseline_verify.add_argument(
        "--archive-downloads",
        action="store_true",
        help=(
            "include the retained downloaded artifact tree under download/ inside --output-archive; "
            "requires --output-archive"
        ),
    )
    p_packaging_baseline_verify.add_argument(
        "--json",
        action="store_true",
        help="emit the top-level verification payload as JSON",
    )
    p_packaging_baseline_verify.add_argument(
        "--require-artifact-count",
        type=packaging_verify._positive_int,
        help="require exactly N discovered packaging-baseline artifacts before verification passes",
    )

    p_video = sub.add_parser("video", help="Video workflow powered by yt-dlp")
    video_sub = p_video.add_subparsers(dest="video_cmd", required=True)

    p_info = video_sub.add_parser("info", help="Fetch video metadata")
    p_info.add_argument("url")
    p_info.add_argument("--json", action="store_true")

    p_probe = video_sub.add_parser("probe", help="Probe a video url without download")
    p_probe.add_argument("url")
    p_probe.add_argument("--json", action="store_true")

    p_download = video_sub.add_parser("download", help="Download a public video")
    p_download.add_argument("url")
    p_download.add_argument("format", nargs="?", default="best")
    p_download.add_argument("--dir")
    p_download.add_argument("--json", action="store_true")

    p_subtitle = video_sub.add_parser("subtitle", help="Extract subtitles")
    p_subtitle.add_argument("url")
    p_subtitle.add_argument("--lang", default="zh-Hans,zh,en")
    p_subtitle.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    ensure_utf8_stdio()
    argv = list(argv if argv is not None else sys.argv[1:])
    if argv and argv[0] not in {
        "search",
        "sources",
        "doctor",
        "packaging-smoke",
        "packaging-capture",
        "packaging-baseline",
        "packaging-baseline-report",
        "packaging-baseline-verify",
        "video",
    } and not argv[0].startswith("-"):
        argv = ["search"] + argv

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "packaging-baseline-report":
        if args.github_run and args.paths:
            parser.error("paths cannot be combined with --github-run")
        if not args.github_run and (
            args.github_workflow
            or args.github_run_list_limit
            or args.repo
            or args.artifact_names
            or args.artifact_patterns
            or args.download_dir
            or args.keep_download_dir
        ):
            parser.error(
                "--github-workflow, --github-run-list-limit, --repo, --artifact-name, --artifact-pattern, --download-dir, and --keep-download-dir require --github-run"
            )
    if args.command == "packaging-baseline-verify":
        packaging_verify.validate_packaging_baseline_verify_args(parser, args)
    if args.command == "packaging-baseline-verify" and args.output_archive and not args.output_dir:
        parser.error("--output-archive requires --output-dir")
    if args.command == "packaging-baseline-verify" and args.archive_downloads and not args.output_archive:
        parser.error("--archive-downloads requires --output-archive")

    try:
        if args.command == "packaging-smoke":
            return _packaging_smoke(args)
        if args.command == "packaging-baseline-report":
            return _packaging_baseline_report(args)
        if args.command == "packaging-baseline-verify":
            return _packaging_baseline_verify(args)
        cache = ResourceCache()
        engine = ResourceHunterEngine(cache=cache)
        if args.command == "search":
            return _search(engine, args)
        if args.command == "sources":
            return _sources(engine, args)
        if args.command == "doctor":
            return _doctor(engine, args)
        if args.command == "packaging-capture":
            return _packaging_capture(engine, args)
        if args.command == "packaging-baseline":
            return _packaging_baseline(engine, args)
        if args.command == "video":
            return _video(engine, args)
    except Exception as exc:
        if getattr(args, "debug", False):
            traceback.print_exc()
        else:
            print(f"error: {exc}", file=sys.stderr)
        return 1
    parser.print_help()
    return 0


def legacy_pansou_main(argv: list[str] | None = None) -> int:
    ensure_utf8_stdio()
    parser = argparse.ArgumentParser(description="Legacy pan search wrapper")
    parser.add_argument("keyword")
    parser.add_argument("--types", nargs="+")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=20)
    parser.add_argument("--max", type=int, default=5)
    parser.add_argument("--fallback", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])
    engine = ResourceHunterEngine()
    intent = parse_intent(args.keyword, channel="pan")
    response = engine.search(intent, page=args.page, limit=args.max)
    if args.types:
        allowed = {item.lower() for item in args.types}
        response["results"] = [item for item in response["results"] if item["provider"].lower() in allowed]
    if args.json_output:
        print(dump_json(response))
    else:
        print(format_search_text(response, max_results=args.max))
    return 0


def legacy_torrent_main(argv: list[str] | None = None) -> int:
    ensure_utf8_stdio()
    parser = argparse.ArgumentParser(description="Legacy torrent search wrapper")
    parser.add_argument("keyword")
    parser.add_argument("--engine", choices=["tpb", "nyaa", "yts", "eztv", "1337x", "all"], default="all")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--anime", action="store_true")
    parser.add_argument("--movie", action="store_true")
    parser.add_argument("--tv", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])
    explicit_kind = "anime" if args.anime else "movie" if args.movie else "tv" if args.tv else None
    engine = ResourceHunterEngine()
    intent = parse_intent(args.keyword, explicit_kind=explicit_kind, channel="torrent")
    response = engine.search(intent, limit=args.limit)
    if args.engine != "all":
        response["results"] = [item for item in response["results"] if item["source"] == args.engine]
    if args.json_output:
        print(dump_json(response))
    else:
        print(format_search_text(response, max_results=args.limit))
    return 0


def legacy_video_main(argv: list[str] | None = None) -> int:
    ensure_utf8_stdio()
    argv = list(argv if argv is not None else sys.argv[1:])
    return main(["video"] + argv)
