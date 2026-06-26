from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .common import dump_json, ensure_utf8_stdio
from .errors import ResourceHunterError
from .packaging_report import (
    _attach_download_artifact_resolution,
    _resolved_download_artifact_paths,
    packaging_baseline_report_requirement_failures,
    read_packaging_baseline_reports,
)


PACKAGING_BASELINE_GATE_SCHEMA_VERSION = 1
DEFAULT_GITHUB_ARTIFACT_PATTERN = "resource-hunter-packaging-baseline-*"
DEFAULT_GITHUB_RUN_WORKFLOW = "resource-hunter-ci"
_GITHUB_RUN_DOWNLOAD_TIMEOUT_SECONDS = 300
_GITHUB_RUN_LIST_LIMIT = 20
_GITHUB_RUN_LIST_JSON_FIELDS = "databaseId,status,conclusion,workflowName,headBranch,event,url,displayTitle"


class PackagingBaselineGateError(ResourceHunterError):
    def __init__(self, message: str, *, download_payload: Mapping[str, Any] | None = None) -> None:
        super().__init__(message)
        self.download_payload = _copy_mapping(download_payload)


def _copy_mapping(value: object) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        return {}
    return dict(value)


def _copy_mapping_list(value: object) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, Mapping)]


def _copy_string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _report_artifact_count(report_payload: Mapping[str, Any]) -> int:
    if report_payload.get("report_type") != "aggregate":
        return 1
    summary = report_payload.get("summary") if isinstance(report_payload.get("summary"), Mapping) else {}
    artifact_count = summary.get("artifact_count")
    if isinstance(artifact_count, int):
        return artifact_count
    artifacts = report_payload.get("artifacts")
    if isinstance(artifacts, list):
        return len(artifacts)
    return 0


def _artifact_count_failure(required_artifact_count: int, actual_artifact_count: int) -> str:
    return (
        "Packaging baseline gate expected "
        f"{required_artifact_count} artifact(s) but found {actual_artifact_count}."
    )


def _copy_string_sequence(values: Sequence[str] | None) -> list[str]:
    if values is None:
        return []
    return [str(value) for value in values if str(value).strip()]


def _unique_string_values(values: Sequence[object]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        normalized = str(value).strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
    return result


def _preview_text(values: Sequence[str], *, limit: int = 5) -> str:
    if not values:
        return ""
    preview = ", ".join(str(value) for value in values[:limit])
    if len(values) > limit:
        preview = f"{preview}, +{len(values) - limit} more"
    return preview


def _normalize_repo_value(repo: str | None) -> str | None:
    if repo is None:
        return None
    normalized = str(repo).strip().strip("/")
    return normalized or None


def _repo_from_github_remote_url(remote_url: str | None) -> str | None:
    normalized = str(remote_url or "").strip()
    if not normalized:
        return None
    match = re.match(
        r"^(?:git@github\.com:|ssh://git@github\.com/|https?://github\.com/|git://github\.com/)(?P<repo>[^\s]+?)(?:\.git)?/?$",
        normalized,
    )
    if match is None:
        return None
    repo = match.group("repo").strip("/")
    if repo.count("/") != 1:
        return None
    owner, name = repo.split("/", 1)
    if not owner or not name:
        return None
    return f"{owner}/{name}"


def _repo_from_git_remote(*, cwd: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=str(cwd),
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return _repo_from_github_remote_url(result.stdout)


def _append_repo_candidate(
    candidates: list[tuple[str | None, str | None]],
    repo: str | None,
    repo_source: str | None,
) -> None:
    normalized_repo = _normalize_repo_value(repo)
    if normalized_repo is None and repo_source != "gh-context":
        return
    candidate = (normalized_repo, repo_source)
    if candidate not in candidates:
        candidates.append(candidate)


def _resolve_github_repo_contexts(repo: str | None, *, cwd: Path) -> list[tuple[str | None, str | None]]:
    explicit_repo = _normalize_repo_value(repo)
    if explicit_repo is not None:
        return [(explicit_repo, None)]

    candidates: list[tuple[str | None, str | None]] = []
    _append_repo_candidate(candidates, os.environ.get("GITHUB_REPOSITORY"), "environment")
    _append_repo_candidate(candidates, _repo_from_git_remote(cwd=cwd), "git-origin")
    _append_repo_candidate(candidates, None, "gh-context")
    return candidates


def _resolve_github_repo_context(repo: str | None, *, cwd: Path) -> tuple[str | None, str | None]:
    return _resolve_github_repo_contexts(repo, cwd=cwd)[0]


def _build_github_run_download_payload(
    run_id: str,
    *,
    requested_run_id: str | None = None,
    repo: str | None,
    repo_source: str | None,
    github_run_list_limit: int | None = None,
    artifact_names: Sequence[str] | None,
    artifact_patterns: Sequence[str] | None,
    download_dir: str | Path,
    download_dir_source: str,
    download_dir_retained: bool,
    run_lookup: Mapping[str, Any] | None = None,
    download_attempts: Sequence[Mapping[str, Any]] | None = None,
    download_command: Sequence[str] | None = None,
    download_returncode: int | None = None,
    download_stdout: str | None = None,
    download_stderr: str | None = None,
) -> dict[str, Any]:
    names, patterns, filter_source = _resolve_download_filters(
        artifact_names=artifact_names,
        artifact_patterns=artifact_patterns,
    )
    payload: dict[str, Any] = {
        "provider": "github-actions",
        "run_id": str(run_id),
        "repo": repo,
        "download_dir": str(Path(download_dir).resolve()),
        "download_dir_source": download_dir_source,
        "download_dir_retained": download_dir_retained,
        "artifact_names": names,
        "artifact_patterns": patterns,
        "artifact_filter_source": filter_source,
    }
    if requested_run_id is not None:
        payload["requested_run_id"] = str(requested_run_id)
    if repo_source is not None:
        payload["repo_source"] = repo_source
    if github_run_list_limit is not None:
        payload["github_run_list_limit"] = int(github_run_list_limit)
    if isinstance(run_lookup, Mapping) and run_lookup:
        payload["run_lookup"] = dict(run_lookup)
    if download_attempts:
        payload["download_attempts"] = _copy_mapping_list(list(download_attempts))
    if download_command is not None:
        payload["download_command"] = [str(part) for part in download_command]
    if download_returncode is not None:
        payload["download_returncode"] = int(download_returncode)
    if download_stdout:
        payload["download_stdout"] = str(download_stdout)
    if download_stderr:
        payload["download_stderr"] = str(download_stderr)
    return payload


def _run_command(
    args: Sequence[str],
    *,
    cwd: Path,
    timeout: int = _GITHUB_RUN_DOWNLOAD_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    result = subprocess.run(
        list(args),
        cwd=str(cwd),
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return {
        "command": list(args),
        "cwd": str(cwd),
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def _resolve_download_filters(
    *,
    artifact_names: Sequence[str] | None = None,
    artifact_patterns: Sequence[str] | None = None,
) -> tuple[list[str], list[str], str]:
    names = _copy_string_sequence(artifact_names)
    patterns = _copy_string_sequence(artifact_patterns)
    if names or patterns:
        return names, patterns, "argument"
    return [], [DEFAULT_GITHUB_ARTIFACT_PATTERN], "default"


def _is_latest_github_run_selector(run_id: str) -> bool:
    return str(run_id).strip().lower() == "latest"


def _resolve_github_run_workflow(workflow: str | None) -> str:
    if workflow is None:
        return DEFAULT_GITHUB_RUN_WORKFLOW
    normalized = str(workflow).strip()
    return normalized or DEFAULT_GITHUB_RUN_WORKFLOW


def _has_explicit_github_run_workflow(workflow: str | None) -> bool:
    return workflow is not None and bool(str(workflow).strip())


def _resolve_github_run_list_limit(limit: int | None) -> int:
    if limit is None:
        return _GITHUB_RUN_LIST_LIMIT
    parsed = int(limit)
    if parsed < 1:
        raise PackagingBaselineGateError("GitHub run list limit must be >= 1.")
    return parsed


def _latest_run_lookup_hint(
    *,
    repo: str | None,
    resolved_repo: str | None,
    repo_source: str | None,
    workflow: str,
    detail: str,
) -> str | None:
    detail_lower = detail.lower()
    if "404" in detail_lower and resolved_repo:
        if repo is not None:
            return (
                "The explicit --repo value may be stale or inaccessible; omit --repo to fall back to "
                "GITHUB_REPOSITORY, the git origin remote, or the current gh repository context."
            )
        if repo_source == "environment":
            return "GITHUB_REPOSITORY may be stale or inaccessible; unset it or pass --repo <owner>/<repo> to override it."
        if repo_source == "git-origin":
            return "The git origin remote may point at a different repository; pass --repo <owner>/<repo> to override it."
    if "could not find any workflows named" in detail_lower:
        return (
            f"Pass --github-workflow <workflow-name> if the packaging workflow was renamed from {workflow}, "
            "or use --github-run <numeric-run-id> to skip the latest-run lookup."
        )
    return None


def _latest_run_artifact_miss_hint(*, workflow: str) -> str:
    return (
        "Pass --artifact-name <artifact-name> or --artifact-pattern <pattern> if the packaging artifact name drifted, "
        f"pass --github-workflow <workflow-name> if {workflow} is no longer the publishing workflow, "
        "or use --github-run <numeric-run-id> to pin the expected run."
    )


def _can_retry_latest_run_lookup_with_next_repo(*, repo_source: str | None, detail: str) -> bool:
    if repo_source not in {"environment", "git-origin"}:
        return False
    detail_lower = detail.lower()
    return "404" in detail_lower or "could not find any workflows named" in detail_lower


def _github_run_download_hint(
    *,
    repo: str | None,
    resolved_repo: str | None,
    repo_source: str | None,
    run_id: str,
    detail: str,
) -> str | None:
    detail_lower = detail.lower()
    if ("404" in detail_lower or "not found" in detail_lower) and resolved_repo:
        if repo is not None:
            return (
                "The explicit --repo value may be stale or inaccessible; omit --repo to fall back to "
                "GITHUB_REPOSITORY, the git origin remote, or the current gh repository context."
            )
        if repo_source == "environment":
            return (
                "GITHUB_REPOSITORY may be stale or inaccessible; unset it or pass "
                f"--repo <owner>/<repo> to override it for run {run_id}."
            )
        if repo_source == "git-origin":
            return (
                "The git origin remote may point at a different repository; pass "
                f"--repo <owner>/<repo> to override it for run {run_id}."
            )
    return None


def _can_retry_github_run_download_with_next_repo(*, repo_source: str | None, detail: str) -> bool:
    if repo_source not in {"environment", "git-origin"}:
        return False
    detail_lower = detail.lower()
    return "404" in detail_lower or "not found" in detail_lower


def _summarize_download_attempt_targets(download_attempts: Sequence[Mapping[str, Any]]) -> str:
    targets: list[str] = []
    for attempt in download_attempts:
        target = str(attempt.get("repo") or "").strip() or "the current gh context"
        if target not in targets:
            targets.append(target)
    return ", ".join(targets)


def _selected_github_run_summary(run: Mapping[str, Any]) -> dict[str, Any]:
    summary = {"id": str(run.get("databaseId") or "")}
    for source_key, target_key in (
        ("status", "status"),
        ("conclusion", "conclusion"),
        ("workflowName", "workflow_name"),
        ("headBranch", "head_branch"),
        ("event", "event"),
        ("url", "url"),
        ("displayTitle", "display_title"),
    ):
        value = run.get(source_key)
        if value is not None and str(value):
            summary[target_key] = str(value)
    return summary


def _select_latest_completed_github_run(runs: object) -> tuple[dict[str, Any] | None, int]:
    if not isinstance(runs, list):
        return None, 0
    normalized_runs = [dict(run) for run in runs if isinstance(run, Mapping)]
    for run in normalized_runs:
        if str(run.get("status") or "").lower() == "completed" and run.get("databaseId") is not None:
            return run, len(normalized_runs)
    return None, len(normalized_runs)


def _artifact_name_matches_download_filters(
    artifact_name: str,
    *,
    artifact_names: Sequence[str] | None,
    artifact_patterns: Sequence[str] | None,
) -> bool:
    exact_names, glob_patterns, _ = _resolve_download_filters(
        artifact_names=artifact_names,
        artifact_patterns=artifact_patterns,
    )
    if artifact_name in exact_names:
        return True
    return any(fnmatch.fnmatchcase(artifact_name, pattern) for pattern in glob_patterns)


def _repo_from_gh_context(*, gh_binary: str, cwd: Path) -> tuple[str | None, dict[str, Any]]:
    command = [gh_binary, "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"]
    result = _run_command(command, cwd=cwd)
    attempt: dict[str, Any] = {"command": [str(part) for part in result.get("command", [])]}
    if result["returncode"] != 0:
        attempt["returncode"] = int(result["returncode"])
        if result.get("stderr"):
            attempt["stderr"] = str(result["stderr"])
        if result.get("stdout"):
            attempt["stdout"] = str(result["stdout"])
        return None, attempt
    resolved_repo = _normalize_repo_value(str(result.get("stdout") or ""))
    if resolved_repo is not None:
        attempt["repo"] = resolved_repo
    return resolved_repo, attempt


def _probe_github_run_artifacts(
    *,
    gh_binary: str,
    repo: str,
    run_id: str,
    artifact_names: Sequence[str] | None,
    artifact_patterns: Sequence[str] | None,
    cwd: Path,
    selected_run: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    artifact_command = [gh_binary, "api", f"repos/{repo}/actions/runs/{run_id}/artifacts"]
    artifact_result = _run_command(artifact_command, cwd=cwd)
    probe: dict[str, Any] = {
        "command": [str(part) for part in artifact_result.get("command", [])],
        "repo": repo,
        "run_id": run_id,
    }
    if isinstance(selected_run, Mapping):
        workflow_name = str(selected_run.get("workflow_name") or "").strip()
        if workflow_name:
            probe["workflow_name"] = workflow_name
        display_title = str(selected_run.get("display_title") or "").strip()
        if display_title:
            probe["display_title"] = display_title

    if artifact_result["returncode"] != 0:
        probe["returncode"] = int(artifact_result["returncode"])
        if artifact_result.get("stderr"):
            probe["stderr"] = str(artifact_result["stderr"])
        if artifact_result.get("stdout"):
            probe["stdout"] = str(artifact_result.get("stdout"))
        return probe

    try:
        artifact_payload = json.loads(artifact_result.get("stdout") or "{}")
    except json.JSONDecodeError as exc:
        probe["stdout"] = str(artifact_result.get("stdout") or "")
        probe["json_error"] = str(exc)
        return probe

    artifacts = artifact_payload.get("artifacts") if isinstance(artifact_payload, Mapping) else None
    artifact_entries = artifacts if isinstance(artifacts, list) else []
    artifact_name_list = [
        str(artifact.get("name"))
        for artifact in artifact_entries
        if isinstance(artifact, Mapping) and artifact.get("name") is not None
    ]
    matched_artifact_names = [
        artifact_name
        for artifact_name in artifact_name_list
        if _artifact_name_matches_download_filters(
            artifact_name,
            artifact_names=artifact_names,
            artifact_patterns=artifact_patterns,
        )
    ]
    probe["artifact_names"] = artifact_name_list
    probe["matched_artifact_names"] = matched_artifact_names
    return probe


def _discover_latest_github_run_with_matching_artifacts(
    *,
    gh_binary: str,
    repo: str | None,
    github_run_list_limit: int | None,
    artifact_names: Sequence[str] | None,
    artifact_patterns: Sequence[str] | None,
    cwd: Path,
) -> tuple[str | None, str | None, dict[str, Any] | None, dict[str, Any]]:
    resolved_run_list_limit = _resolve_github_run_list_limit(github_run_list_limit)
    resolved_names, resolved_patterns, filter_source = _resolve_download_filters(
        artifact_names=artifact_names,
        artifact_patterns=artifact_patterns,
    )
    discovery: dict[str, Any] = {
        "strategy": "artifact-discovery",
        "run_list_limit": resolved_run_list_limit,
        "artifact_names": resolved_names,
        "artifact_patterns": resolved_patterns,
        "artifact_filter_source": filter_source,
    }
    resolved_repo = repo
    if resolved_repo is None:
        resolved_repo, repo_resolution = _repo_from_gh_context(gh_binary=gh_binary, cwd=cwd)
        discovery["repo_resolution"] = repo_resolution
    if resolved_repo is None:
        discovery["error"] = "Unable to resolve a GitHub repository from the current gh context."
        return None, None, None, discovery

    discovery["repo"] = resolved_repo
    list_command: list[str] = [
        gh_binary,
        "run",
        "list",
        "--status",
        "completed",
        "--limit",
        str(resolved_run_list_limit),
        "--json",
        _GITHUB_RUN_LIST_JSON_FIELDS,
        "--repo",
        resolved_repo,
    ]
    list_result = _run_command(list_command, cwd=cwd)
    list_attempt: dict[str, Any] = {
        "command": [str(part) for part in list_result.get("command", [])],
        "repo": resolved_repo,
    }
    if list_result["returncode"] != 0:
        list_attempt["returncode"] = int(list_result["returncode"])
        if list_result.get("stderr"):
            list_attempt["stderr"] = str(list_result["stderr"])
        if list_result.get("stdout"):
            list_attempt["stdout"] = str(list_result["stdout"])
        discovery["run_list"] = list_attempt
        return None, resolved_repo, None, discovery

    try:
        run_candidates = json.loads(list_result.get("stdout") or "[]")
    except json.JSONDecodeError as exc:
        list_attempt["stdout"] = str(list_result.get("stdout") or "")
        list_attempt["json_error"] = str(exc)
        discovery["run_list"] = list_attempt
        return None, resolved_repo, None, discovery

    normalized_runs = [dict(run) for run in run_candidates if isinstance(run, Mapping)]
    workflow_names = _unique_string_values(
        [run.get("workflowName") for run in normalized_runs if run.get("workflowName") is not None]
    )
    list_attempt["matched_run_count"] = len(normalized_runs)
    list_attempt["completed_run_count"] = len(normalized_runs)
    discovery["run_list"] = list_attempt
    if workflow_names:
        discovery["workflow_names"] = workflow_names

    artifact_name_samples: list[str] = []
    probes: list[dict[str, Any]] = []
    for run in normalized_runs:
        run_id = str(run.get("databaseId") or "").strip()
        if not run_id:
            continue

        selected_run = _selected_github_run_summary(run)
        probe = _probe_github_run_artifacts(
            gh_binary=gh_binary,
            repo=resolved_repo,
            run_id=run_id,
            artifact_names=artifact_names,
            artifact_patterns=artifact_patterns,
            cwd=cwd,
            selected_run=selected_run,
        )
        artifact_name_list = _copy_string_list(probe.get("artifact_names"))
        artifact_name_samples = _unique_string_values([*artifact_name_samples, *artifact_name_list])
        matched_artifact_names = _copy_string_list(probe.get("matched_artifact_names"))
        if matched_artifact_names:
            if artifact_name_samples:
                discovery["artifact_name_samples"] = artifact_name_samples
            discovery["artifact_probes"] = probes + [probe]
            discovery["selected_run"] = selected_run
            discovery["selected_artifact_names"] = matched_artifact_names
            return run_id, resolved_repo, selected_run, discovery
        probes.append(probe)

    if artifact_name_samples:
        discovery["artifact_name_samples"] = artifact_name_samples
    discovery["artifact_probes"] = probes
    return None, resolved_repo, None, discovery


def _artifact_discovery_scanned_run_count(discovery: Mapping[str, Any]) -> int | None:
    run_list = discovery.get("run_list") if isinstance(discovery.get("run_list"), Mapping) else {}
    for key in ("completed_run_count", "matched_run_count"):
        value = run_list.get(key)
        if isinstance(value, int):
            return value
    return None


def _artifact_discovery_detail_text(discovery: Mapping[str, Any]) -> str | None:
    if not isinstance(discovery, Mapping) or not discovery:
        return None

    repo = _normalize_repo_value(str(discovery.get("repo") or ""))
    scanned_run_count = _artifact_discovery_scanned_run_count(discovery)
    workflow_names = _copy_string_list(discovery.get("workflow_names"))
    artifact_name_samples = _copy_string_list(discovery.get("artifact_name_samples"))

    parts: list[str] = []
    if scanned_run_count == 0:
        if repo:
            parts.append(f"Artifact discovery found no completed runs in {repo}.")
        else:
            parts.append("Artifact discovery found no completed runs.")
    elif scanned_run_count is not None:
        scanned_text = f"Artifact discovery scanned {scanned_run_count} completed run(s)"
        if repo:
            scanned_text = f"{scanned_text} in {repo}"
        workflow_preview = _preview_text(workflow_names)
        if workflow_preview:
            scanned_text = f"{scanned_text} and saw workflows: {workflow_preview}."
        else:
            scanned_text = f"{scanned_text}."
        parts.append(scanned_text)

    artifact_preview = _preview_text(artifact_name_samples)
    if artifact_preview:
        parts.append(f"Recent artifact names: {artifact_preview}.")

    if not parts:
        error = str(discovery.get("error") or "").strip()
        if error:
            parts.append(f"Artifact discovery error: {error}")

    return " ".join(parts) if parts else None


def _download_packaging_baseline_github_run(
    run_id: str,
    *,
    repo: str | None = None,
    github_workflow: str | None = None,
    github_run_list_limit: int | None = None,
    artifact_names: Sequence[str] | None = None,
    artifact_patterns: Sequence[str] | None = None,
    download_dir: str | Path,
    download_dir_source: str,
    download_dir_retained: bool,
) -> dict[str, Any]:
    requested_run_id = str(run_id)
    gh_binary = shutil.which("gh")
    repo_candidates = _resolve_github_repo_contexts(repo, cwd=Path.cwd())
    resolved_repo, repo_source = repo_candidates[0]
    resolved_run_list_limit = (
        _resolve_github_run_list_limit(github_run_list_limit)
        if _is_latest_github_run_selector(requested_run_id)
        else None
    )
    download_payload = _build_github_run_download_payload(
        requested_run_id,
        repo=resolved_repo,
        repo_source=repo_source,
        github_run_list_limit=resolved_run_list_limit,
        artifact_names=artifact_names,
        artifact_patterns=artifact_patterns,
        download_dir=download_dir,
        download_dir_source=download_dir_source,
        download_dir_retained=download_dir_retained,
    )
    if gh_binary is None:
        raise PackagingBaselineGateError(
            "GitHub CLI (gh) is required for --github-run. Install gh or provide downloaded artifact paths instead.",
            download_payload=download_payload,
        )
    resolved_run_id = requested_run_id
    run_lookup: dict[str, Any] | None = None
    if _is_latest_github_run_selector(requested_run_id):
        lookup_workflow = _resolve_github_run_workflow(github_workflow)
        explicit_workflow = _has_explicit_github_run_workflow(github_workflow)
        run_lookup = {
            "selector": requested_run_id,
            "workflow": lookup_workflow,
            "list_limit": resolved_run_list_limit,
            "attempts": [],
            "strategy": "workflow-filter",
        }
        for candidate_repo, candidate_source in repo_candidates:
            list_command: list[str] = [
                gh_binary,
                "run",
                "list",
                "--workflow",
                lookup_workflow,
                "--limit",
                str(resolved_run_list_limit),
                "--json",
                _GITHUB_RUN_LIST_JSON_FIELDS,
            ]
            if candidate_repo:
                list_command.extend(["--repo", candidate_repo])
            list_result = _run_command(list_command, cwd=Path.cwd())

            attempt: dict[str, Any] = {
                "command": [str(part) for part in list_result.get("command", [])],
                "repo_source": candidate_source,
            }
            if candidate_repo is not None:
                attempt["repo"] = candidate_repo

            if list_result["returncode"] != 0:
                attempt["returncode"] = int(list_result["returncode"])
                if list_result.get("stderr"):
                    attempt["stderr"] = str(list_result["stderr"])
                if list_result.get("stdout"):
                    attempt["stdout"] = str(list_result["stdout"])
                detail = (
                    list_result.get("stderr")
                    or list_result.get("stdout")
                    or f"exit code {list_result['returncode']}"
                ).strip()
                hint = _latest_run_lookup_hint(
                    repo=repo,
                    resolved_repo=candidate_repo,
                    repo_source=candidate_source,
                    workflow=lookup_workflow,
                    detail=detail,
                )
                if hint:
                    attempt["hint"] = hint
                if repo is None and _can_retry_latest_run_lookup_with_next_repo(
                    repo_source=candidate_source,
                    detail=detail,
                ):
                    run_lookup["attempts"].append(attempt)
                    continue
                if not explicit_workflow and "could not find any workflows named" in detail.lower():
                    discovered_run_id, discovered_repo, discovered_run, discovery = (
                        _discover_latest_github_run_with_matching_artifacts(
                            gh_binary=gh_binary,
                            repo=candidate_repo,
                            github_run_list_limit=resolved_run_list_limit,
                            artifact_names=artifact_names,
                            artifact_patterns=artifact_patterns,
                            cwd=Path.cwd(),
                        )
                    )
                    attempt["artifact_discovery"] = discovery
                    if discovered_run_id is not None and discovered_run is not None:
                        attempt["selected_run"] = discovered_run
                        run_lookup["attempts"].append(attempt)
                        run_lookup["selected_run"] = discovered_run
                        run_lookup["strategy"] = str(discovery.get("strategy") or "artifact-discovery")
                        resolved_repo = discovered_repo
                        repo_source = candidate_source
                        resolved_run_id = discovered_run_id
                        break
                run_lookup["attempts"].append(attempt)
                target = candidate_repo or "current gh context"
                message = (
                    "GitHub Actions run lookup failed for "
                    f"{target} latest {lookup_workflow} run: {detail}"
                )
                if (
                    not explicit_workflow
                    and isinstance(attempt.get("artifact_discovery"), Mapping)
                    and isinstance(attempt["artifact_discovery"].get("run_list"), Mapping)
                    and attempt["artifact_discovery"]["run_list"].get("matched_run_count") == resolved_run_list_limit
                ):
                    message = (
                        f"{message} Artifact discovery already scanned {resolved_run_list_limit} completed runs; "
                        "increase --github-run-list-limit to search deeper."
                    )
                discovery_detail = _artifact_discovery_detail_text(
                    attempt.get("artifact_discovery") if isinstance(attempt.get("artifact_discovery"), Mapping) else {}
                )
                if discovery_detail:
                    message = f"{message} {discovery_detail}"
                if hint:
                    message = f"{message} {hint}"
                raise PackagingBaselineGateError(
                    message,
                    download_payload=_build_github_run_download_payload(
                        requested_run_id,
                        requested_run_id=requested_run_id,
                        repo=candidate_repo,
                        repo_source=candidate_source,
                        github_run_list_limit=resolved_run_list_limit,
                        artifact_names=artifact_names,
                        artifact_patterns=artifact_patterns,
                        download_dir=download_dir,
                        download_dir_source=download_dir_source,
                        download_dir_retained=download_dir_retained,
                        run_lookup=run_lookup,
                    ),
                )

            try:
                run_candidates = json.loads(list_result.get("stdout") or "[]")
            except json.JSONDecodeError as exc:
                attempt["stdout"] = str(list_result.get("stdout") or "")
                run_lookup["attempts"].append(attempt)
                raise PackagingBaselineGateError(
                    (
                        "GitHub Actions run lookup returned invalid JSON for "
                        f"latest {lookup_workflow} run: {exc}"
                    ),
                    download_payload=_build_github_run_download_payload(
                        requested_run_id,
                        requested_run_id=requested_run_id,
                        repo=candidate_repo,
                        repo_source=candidate_source,
                        github_run_list_limit=resolved_run_list_limit,
                        artifact_names=artifact_names,
                        artifact_patterns=artifact_patterns,
                        download_dir=download_dir,
                        download_dir_source=download_dir_source,
                        download_dir_retained=download_dir_retained,
                        run_lookup=run_lookup,
                    ),
                ) from exc

            selected_run, matched_run_count = _select_latest_completed_github_run(run_candidates)
            attempt["matched_run_count"] = matched_run_count
            if selected_run is None:
                discovery: Mapping[str, Any] | None = None
                if not explicit_workflow:
                    discovered_run_id, discovered_repo, discovered_run, discovery = (
                        _discover_latest_github_run_with_matching_artifacts(
                            gh_binary=gh_binary,
                            repo=candidate_repo,
                            github_run_list_limit=resolved_run_list_limit,
                            artifact_names=artifact_names,
                            artifact_patterns=artifact_patterns,
                            cwd=Path.cwd(),
                        )
                    )
                    attempt["artifact_discovery"] = discovery
                    if discovered_run_id is not None and discovered_run is not None:
                        attempt["selected_run"] = discovered_run
                        run_lookup["attempts"].append(attempt)
                        run_lookup["selected_run"] = discovered_run
                        run_lookup["strategy"] = str(discovery.get("strategy") or "artifact-discovery")
                        resolved_repo = discovered_repo
                        repo_source = candidate_source
                        resolved_run_id = discovered_run_id
                        break
                run_lookup["attempts"].append(attempt)
                raise PackagingBaselineGateError(
                    (
                        "No completed GitHub Actions runs matched "
                        f"latest {lookup_workflow} for {candidate_repo or 'the current gh context'}."
                        + (
                            f" Artifact discovery already scanned {resolved_run_list_limit} completed runs; "
                            "increase --github-run-list-limit to search deeper."
                            if isinstance(discovery, Mapping)
                            and isinstance(discovery.get("run_list"), Mapping)
                            and discovery["run_list"].get("matched_run_count") == resolved_run_list_limit
                            else ""
                        )
                        + (
                            f" {_artifact_discovery_detail_text(discovery)}"
                            if isinstance(discovery, Mapping) and _artifact_discovery_detail_text(discovery)
                            else ""
                        )
                    ),
                    download_payload=_build_github_run_download_payload(
                        requested_run_id,
                        requested_run_id=requested_run_id,
                        repo=candidate_repo,
                        repo_source=candidate_source,
                        github_run_list_limit=resolved_run_list_limit,
                        artifact_names=artifact_names,
                        artifact_patterns=artifact_patterns,
                        download_dir=download_dir,
                        download_dir_source=download_dir_source,
                        download_dir_retained=download_dir_retained,
                        run_lookup=run_lookup,
                    ),
                )

            selected_run_summary = _selected_github_run_summary(selected_run)
            if not explicit_workflow:
                selected_run_artifact_probe = _probe_github_run_artifacts(
                    gh_binary=gh_binary,
                    repo=candidate_repo,
                    run_id=str(selected_run["databaseId"]),
                    artifact_names=artifact_names,
                    artifact_patterns=artifact_patterns,
                    cwd=Path.cwd(),
                    selected_run=selected_run_summary,
                )
                attempt["workflow_filter_selected_run_artifact_probe"] = selected_run_artifact_probe
                selected_run_matched_artifacts = _copy_string_list(
                    selected_run_artifact_probe.get("matched_artifact_names")
                )
                if selected_run_artifact_probe.get("returncode") is None and not selected_run_matched_artifacts:
                    attempt["workflow_filter_selected_run"] = selected_run_summary
                    discovered_run_id, discovered_repo, discovered_run, discovery = (
                        _discover_latest_github_run_with_matching_artifacts(
                            gh_binary=gh_binary,
                            repo=candidate_repo,
                            github_run_list_limit=resolved_run_list_limit,
                            artifact_names=artifact_names,
                            artifact_patterns=artifact_patterns,
                            cwd=Path.cwd(),
                        )
                    )
                    attempt["artifact_discovery"] = discovery
                    if discovered_run_id is not None and discovered_run is not None:
                        attempt["selected_run"] = discovered_run
                        run_lookup["attempts"].append(attempt)
                        run_lookup["selected_run"] = discovered_run
                        run_lookup["strategy"] = str(discovery.get("strategy") or "artifact-discovery")
                        resolved_repo = discovered_repo
                        repo_source = candidate_source
                        resolved_run_id = discovered_run_id
                        break
                    run_lookup["attempts"].append(attempt)
                    if repo is None and candidate_source in {"environment", "git-origin"}:
                        continue
                    selected_run_id = str(selected_run_summary.get("id") or selected_run["databaseId"])
                    target = candidate_repo or "the current gh context"
                    message = (
                        f"Latest {lookup_workflow} run {selected_run_id} for {target} had no artifacts matching the requested filters."
                    )
                    selected_run_artifact_names = _copy_string_list(
                        selected_run_artifact_probe.get("artifact_names")
                    )
                    if selected_run_artifact_names:
                        message = f"{message} Latest run artifacts: {_preview_text(selected_run_artifact_names)}."
                    else:
                        message = f"{message} Latest run reported no artifacts."
                    if (
                        isinstance(discovery, Mapping)
                        and isinstance(discovery.get("run_list"), Mapping)
                        and discovery["run_list"].get("matched_run_count") == resolved_run_list_limit
                    ):
                        message = (
                            f"{message} Artifact discovery already scanned {resolved_run_list_limit} completed runs; "
                            "increase --github-run-list-limit to search deeper."
                        )
                    discovery_detail = _artifact_discovery_detail_text(discovery)
                    if discovery_detail:
                        message = f"{message} {discovery_detail}"
                    message = f"{message} {_latest_run_artifact_miss_hint(workflow=lookup_workflow)}"
                    raise PackagingBaselineGateError(
                        message,
                        download_payload=_build_github_run_download_payload(
                            requested_run_id,
                            requested_run_id=requested_run_id,
                            repo=candidate_repo,
                            repo_source=candidate_source,
                            github_run_list_limit=resolved_run_list_limit,
                            artifact_names=artifact_names,
                            artifact_patterns=artifact_patterns,
                            download_dir=download_dir,
                            download_dir_source=download_dir_source,
                            download_dir_retained=download_dir_retained,
                            run_lookup=run_lookup,
                        ),
                    )
            attempt["selected_run"] = selected_run_summary
            run_lookup["attempts"].append(attempt)
            run_lookup["selected_run"] = selected_run_summary
            resolved_repo, repo_source = candidate_repo, candidate_source
            resolved_run_id = str(selected_run["databaseId"])
            break
    resolved_download_dir = Path(download_dir).resolve()
    resolved_download_dir.mkdir(parents=True, exist_ok=True)
    allow_download_repo_fallback = not _is_latest_github_run_selector(requested_run_id) and repo is None
    download_candidates = repo_candidates if allow_download_repo_fallback else [(resolved_repo, repo_source)]
    download_attempts: list[dict[str, Any]] = []
    result: dict[str, Any] | None = None
    last_failed_attempt: dict[str, Any] | None = None
    last_failed_detail: str | None = None
    last_failed_hint: str | None = None
    for candidate_repo, candidate_source in download_candidates:
        command: list[str] = [gh_binary, "run", "download", str(resolved_run_id)]
        if candidate_repo:
            command.extend(["--repo", candidate_repo])
        command.extend(["--dir", str(resolved_download_dir)])
        for name in download_payload["artifact_names"]:
            command.extend(["--name", name])
        for pattern in download_payload["artifact_patterns"]:
            command.extend(["--pattern", pattern])
        candidate_result = _run_command(command, cwd=Path.cwd())
        attempt: dict[str, Any] = {
            "command": [str(part) for part in candidate_result.get("command", [])],
            "repo_source": candidate_source,
        }
        if candidate_repo is not None:
            attempt["repo"] = candidate_repo
        if candidate_result["returncode"] == 0:
            if allow_download_repo_fallback:
                attempt["selected"] = True
                download_attempts.append(attempt)
            result = candidate_result
            resolved_repo, repo_source = candidate_repo, candidate_source
            break

        attempt["returncode"] = int(candidate_result["returncode"])
        if candidate_result.get("stderr"):
            attempt["stderr"] = str(candidate_result["stderr"])
        if candidate_result.get("stdout"):
            attempt["stdout"] = str(candidate_result["stdout"])
        detail = (
            candidate_result.get("stderr")
            or candidate_result.get("stdout")
            or f"exit code {candidate_result['returncode']}"
        ).strip()
        hint = _github_run_download_hint(
            repo=repo,
            resolved_repo=candidate_repo,
            repo_source=candidate_source,
            run_id=resolved_run_id,
            detail=detail,
        )
        if hint:
            attempt["hint"] = hint
        if allow_download_repo_fallback:
            download_attempts.append(attempt)
        last_failed_attempt = attempt
        last_failed_detail = detail
        last_failed_hint = hint
        if allow_download_repo_fallback and _can_retry_github_run_download_with_next_repo(
            repo_source=candidate_source,
            detail=detail,
        ):
            continue
        if allow_download_repo_fallback and len(download_attempts) > 1:
            attempted_targets = _summarize_download_attempt_targets(download_attempts)
            message = (
                "GitHub Actions artifact download failed for "
                f"run {resolved_run_id} after trying {attempted_targets}: {detail}"
            )
        else:
            target = f"{candidate_repo} run {resolved_run_id}" if candidate_repo else f"run {resolved_run_id}"
            message = f"GitHub Actions artifact download failed for {target}: {detail}"
        if hint:
            message = f"{message} {hint}"
        raise PackagingBaselineGateError(
            message,
            download_payload=_build_github_run_download_payload(
                resolved_run_id,
                requested_run_id=requested_run_id if requested_run_id != resolved_run_id else None,
                repo=candidate_repo,
                repo_source=candidate_source,
                github_run_list_limit=resolved_run_list_limit,
                artifact_names=artifact_names,
                artifact_patterns=artifact_patterns,
                download_dir=resolved_download_dir,
                download_dir_source=download_dir_source,
                download_dir_retained=download_dir_retained,
                run_lookup=run_lookup,
                download_attempts=download_attempts,
                download_command=candidate_result.get("command"),
                download_returncode=candidate_result.get("returncode"),
                download_stdout=candidate_result.get("stdout"),
                download_stderr=candidate_result.get("stderr"),
            ),
        )
    if result is None:
        if last_failed_attempt is None or last_failed_detail is None:
            raise PackagingBaselineGateError(
                f"GitHub Actions artifact download failed for run {resolved_run_id}.",
                download_payload=_build_github_run_download_payload(
                    resolved_run_id,
                    requested_run_id=requested_run_id if requested_run_id != resolved_run_id else None,
                    repo=resolved_repo,
                    repo_source=repo_source,
                    github_run_list_limit=resolved_run_list_limit,
                    artifact_names=artifact_names,
                    artifact_patterns=artifact_patterns,
                    download_dir=resolved_download_dir,
                    download_dir_source=download_dir_source,
                    download_dir_retained=download_dir_retained,
                    run_lookup=run_lookup,
                    download_attempts=download_attempts,
                ),
            )
        attempted_targets = _summarize_download_attempt_targets(download_attempts)
        message = (
            "GitHub Actions artifact download failed for "
            f"run {resolved_run_id} after trying {attempted_targets}: {last_failed_detail}"
        )
        if last_failed_hint:
            message = f"{message} {last_failed_hint}"
        raise PackagingBaselineGateError(
            message,
            download_payload=_build_github_run_download_payload(
                resolved_run_id,
                requested_run_id=requested_run_id if requested_run_id != resolved_run_id else None,
                repo=str(last_failed_attempt.get("repo") or "").strip() or None,
                repo_source=str(last_failed_attempt.get("repo_source") or "").strip() or None,
                github_run_list_limit=resolved_run_list_limit,
                artifact_names=artifact_names,
                artifact_patterns=artifact_patterns,
                download_dir=resolved_download_dir,
                download_dir_source=download_dir_source,
                download_dir_retained=download_dir_retained,
                run_lookup=run_lookup,
                download_attempts=download_attempts,
                download_command=last_failed_attempt.get("command"),
                download_returncode=last_failed_attempt.get("returncode"),
                download_stdout=last_failed_attempt.get("stdout"),
                download_stderr=last_failed_attempt.get("stderr"),
            ),
        )
    return _build_github_run_download_payload(
        resolved_run_id,
        requested_run_id=requested_run_id if requested_run_id != resolved_run_id else None,
        repo=resolved_repo,
        repo_source=repo_source,
        github_run_list_limit=resolved_run_list_limit,
        artifact_names=artifact_names,
        artifact_patterns=artifact_patterns,
        download_dir=resolved_download_dir,
        download_dir_source=download_dir_source,
        download_dir_retained=download_dir_retained,
        run_lookup=run_lookup,
        download_attempts=download_attempts,
        download_command=result["command"],
    )


def build_packaging_baseline_gate_payload(
    report_payload: Mapping[str, Any],
    *,
    required_artifact_count: int | None = None,
    download_payload: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    failures = list(packaging_baseline_report_requirement_failures(report_payload))
    payload: dict[str, Any] = {
        "gate_schema_version": PACKAGING_BASELINE_GATE_SCHEMA_VERSION,
        "report_type": report_payload.get("report_type"),
        "summary": _copy_mapping(report_payload.get("summary")),
    }
    if download_payload is not None:
        payload["download"] = _copy_mapping(download_payload)
    if report_payload.get("report_type") == "aggregate":
        payload["artifacts_with_contract_drift"] = _copy_string_list(
            report_payload.get("artifacts_with_contract_drift")
        )
        payload["artifacts_with_requirement_failures"] = _copy_string_list(
            report_payload.get("artifacts_with_requirement_failures")
        )
    else:
        artifact_path = report_payload.get("artifact_path")
        if artifact_path is not None:
            payload["artifact_path"] = str(artifact_path)
    if required_artifact_count is not None:
        actual_artifact_count = _report_artifact_count(report_payload)
        payload["expected_artifact_count"] = required_artifact_count
        payload["actual_artifact_count"] = actual_artifact_count
        if actual_artifact_count != required_artifact_count:
            failures.append(_artifact_count_failure(required_artifact_count, actual_artifact_count))
    payload["ok"] = len(failures) == 0
    payload["failure_count"] = len(failures)
    payload["failures"] = failures
    return payload


def build_packaging_baseline_gate_error_payload(
    error: str,
    *,
    required_artifact_count: int | None = None,
    download_payload: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "gate_schema_version": PACKAGING_BASELINE_GATE_SCHEMA_VERSION,
        "report_type": "error",
        "summary": {},
        "ok": False,
        "failure_count": 1,
        "failures": [error],
        "error": error,
    }
    if required_artifact_count is not None:
        payload["expected_artifact_count"] = required_artifact_count
    if download_payload is not None:
        payload["download"] = _copy_mapping(download_payload)
    return payload


def evaluate_packaging_baseline_gate(
    paths: Sequence[str | Path] | None = None, *, required_artifact_count: int | None = None
) -> dict[str, Any]:
    report_payload = read_packaging_baseline_reports(paths)
    return build_packaging_baseline_gate_payload(
        report_payload,
        required_artifact_count=required_artifact_count,
    )


def _evaluate_downloaded_packaging_baseline_gate(
    download_payload: Mapping[str, Any],
    *,
    required_artifact_count: int | None = None,
) -> dict[str, Any]:
    artifact_paths = _resolved_download_artifact_paths(download_payload)
    download_payload = _attach_download_artifact_resolution(download_payload, artifact_paths)
    if not artifact_paths:
        raise PackagingBaselineGateError(
            f"No packaging-baseline.json artifacts found under {download_payload['download_dir']}.",
            download_payload=download_payload,
        )
    try:
        report_payload = read_packaging_baseline_reports(artifact_paths)
    except ResourceHunterError as exc:
        raise PackagingBaselineGateError(str(exc), download_payload=download_payload) from exc
    return build_packaging_baseline_gate_payload(
        report_payload,
        required_artifact_count=required_artifact_count,
        download_payload=download_payload,
    )


def evaluate_packaging_baseline_gate_from_github_run(
    run_id: str,
    *,
    repo: str | None = None,
    github_workflow: str | None = None,
    github_run_list_limit: int | None = None,
    artifact_names: Sequence[str] | None = None,
    artifact_patterns: Sequence[str] | None = None,
    download_dir: str | Path | None = None,
    keep_download_dir: bool = False,
    required_artifact_count: int | None = None,
) -> dict[str, Any]:
    if download_dir is not None:
        download_payload = _download_packaging_baseline_github_run(
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
        return _evaluate_downloaded_packaging_baseline_gate(
            download_payload,
            required_artifact_count=required_artifact_count,
        )

    if keep_download_dir:
        retained_dir = Path(tempfile.mkdtemp(prefix="resource-hunter-gh-run-download-"))
        download_payload = _download_packaging_baseline_github_run(
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
        return _evaluate_downloaded_packaging_baseline_gate(
            download_payload,
            required_artifact_count=required_artifact_count,
        )

    with tempfile.TemporaryDirectory(prefix="resource-hunter-gh-run-download-") as temp_dir:
        download_payload = _download_packaging_baseline_github_run(
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
        return _evaluate_downloaded_packaging_baseline_gate(
            download_payload,
            required_artifact_count=required_artifact_count,
        )


def _text_value(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "unknown"
    return str(value)


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

    lines = [f"GitHub run: {_download_run_text(download)}"]
    if download.get("repo") is not None:
        repo_label = str(download.get("repo"))
        if download.get("repo_source"):
            repo_label = f"{repo_label} ({download.get('repo_source')})"
        lines.append(f"Repository: {repo_label}")
    elif download.get("repo_source") == "gh-context":
        lines.append("Repository: current gh context")
    if download.get("github_run_list_limit") is not None:
        lines.append(f"Latest run scan limit: {download.get('github_run_list_limit')}")

    lines.append(f"Downloaded artifacts: {download.get('download_dir')}")
    if "download_dir_retained" in download:
        lines.append(f"Download dir retained: {_text_value(download.get('download_dir_retained'))}")

    filter_parts: list[str] = []
    artifact_names = download.get("artifact_names")
    if isinstance(artifact_names, list) and artifact_names:
        filter_parts.append(f"names {', '.join(str(name) for name in artifact_names)}")
    artifact_patterns = download.get("artifact_patterns")
    if isinstance(artifact_patterns, list) and artifact_patterns:
        filter_parts.append(f"patterns {', '.join(str(pattern) for pattern in artifact_patterns)}")
    artifact_filter_source = download.get("artifact_filter_source")
    if filter_parts:
        details = "; ".join(filter_parts)
        if artifact_filter_source:
            details = f"{details} ({artifact_filter_source})"
        lines.append(f"Download filters: {details}")
    elif artifact_filter_source:
        lines.append(f"Download filters: {artifact_filter_source}")

    resolved_artifact_count = download.get("resolved_artifact_count")
    resolved_filesystem_artifact_count = download.get("resolved_filesystem_artifact_count")
    resolved_archive_member_count = download.get("resolved_archive_member_count")
    if (
        resolved_artifact_count is not None
        or resolved_filesystem_artifact_count is not None
        or resolved_archive_member_count is not None
    ):
        lines.append(
            "Resolved artifacts: "
            f"{_text_value(resolved_artifact_count)} total, "
            f"{_text_value(resolved_filesystem_artifact_count)} filesystem, "
            f"{_text_value(resolved_archive_member_count)} archive members"
        )

    run_lookup = download.get("run_lookup")
    if isinstance(run_lookup, Mapping):
        lookup_strategy = run_lookup.get("strategy")
        if lookup_strategy and str(lookup_strategy) != "workflow-filter":
            lines.append(f"Selected run lookup strategy: {lookup_strategy}")
        selected_run = run_lookup.get("selected_run")
        if isinstance(selected_run, Mapping):
            workflow_name = selected_run.get("workflow_name")
            if workflow_name:
                lines.append(f"Selected run workflow: {workflow_name}")
            status = selected_run.get("status")
            conclusion = selected_run.get("conclusion")
            if status or conclusion:
                selected_status = " / ".join(str(part) for part in (status, conclusion) if part)
                lines.append(f"Selected run status: {selected_status}")
            head_branch = selected_run.get("head_branch")
            if head_branch:
                lines.append(f"Selected run branch: {head_branch}")
            event = selected_run.get("event")
            if event:
                lines.append(f"Selected run event: {event}")
            display_title = selected_run.get("display_title")
            if display_title:
                lines.append(f"Selected run title: {display_title}")
            url = selected_run.get("url")
            if url:
                lines.append(f"Selected run URL: {url}")

        attempts = run_lookup.get("attempts") if isinstance(run_lookup.get("attempts"), list) else []
        artifact_discovery = next(
            (
                attempt.get("artifact_discovery")
                for attempt in reversed(attempts)
                if isinstance(attempt, Mapping) and isinstance(attempt.get("artifact_discovery"), Mapping)
            ),
            None,
        )
        if isinstance(artifact_discovery, Mapping) and (
            str(lookup_strategy) == "artifact-discovery" or not isinstance(selected_run, Mapping)
        ):
            discovery_repo = _normalize_repo_value(str(artifact_discovery.get("repo") or ""))
            if discovery_repo:
                lines.append(f"Artifact discovery repo: {discovery_repo}")
            scanned_run_count = _artifact_discovery_scanned_run_count(artifact_discovery)
            if scanned_run_count is not None:
                lines.append(f"Artifact discovery scanned runs: {scanned_run_count}")
            workflow_names = _copy_string_list(artifact_discovery.get("workflow_names"))
            if workflow_names:
                lines.append(f"Artifact discovery workflows: {_preview_text(workflow_names)}")
            artifact_name_samples = _copy_string_list(artifact_discovery.get("artifact_name_samples"))
            if artifact_name_samples:
                lines.append(f"Artifact discovery artifact samples: {_preview_text(artifact_name_samples)}")

        workflow_filter_selected_run = next(
            (
                attempt.get("workflow_filter_selected_run")
                for attempt in reversed(attempts)
                if isinstance(attempt, Mapping) and isinstance(attempt.get("workflow_filter_selected_run"), Mapping)
            ),
            None,
        )
        workflow_filter_selected_run_artifact_probe = next(
            (
                attempt.get("workflow_filter_selected_run_artifact_probe")
                for attempt in reversed(attempts)
                if isinstance(attempt, Mapping)
                and isinstance(attempt.get("workflow_filter_selected_run_artifact_probe"), Mapping)
            ),
            None,
        )
        if str(lookup_strategy) == "artifact-discovery" and isinstance(workflow_filter_selected_run, Mapping):
            candidate_run_id = str(workflow_filter_selected_run.get("id") or "").strip()
            candidate_workflow = str(workflow_filter_selected_run.get("workflow_name") or "").strip()
            if candidate_run_id and candidate_workflow:
                lines.append(f"Workflow-filter candidate run: {candidate_run_id} ({candidate_workflow})")
            elif candidate_run_id:
                lines.append(f"Workflow-filter candidate run: {candidate_run_id}")
            elif candidate_workflow:
                lines.append(f"Workflow-filter candidate workflow: {candidate_workflow}")
            if isinstance(workflow_filter_selected_run_artifact_probe, Mapping):
                candidate_artifact_names = _copy_string_list(
                    workflow_filter_selected_run_artifact_probe.get("artifact_names")
                )
                if candidate_artifact_names:
                    lines.append(
                        f"Workflow-filter candidate artifacts: {_preview_text(candidate_artifact_names)}"
                    )
                elif workflow_filter_selected_run_artifact_probe.get("returncode") is None:
                    lines.append("Workflow-filter candidate artifacts: none")

    download_attempts = download.get("download_attempts")
    if isinstance(download_attempts, list) and len(download_attempts) > 1:
        lines.append(f"Download repo attempts: {len(download_attempts)}")

    resolved_artifact_paths = download.get("resolved_artifact_paths")
    if isinstance(resolved_artifact_paths, list):
        for index, artifact_path in enumerate(resolved_artifact_paths, start=1):
            lines.append(f"Resolved artifact {index}: {artifact_path}")

    return lines


def format_packaging_baseline_gate_text(payload: Mapping[str, Any]) -> str:
    lines = [
        "Resource Hunter packaging baseline gate",
        f"Status: {'ok' if payload.get('ok') else 'drift'}",
        f"Report type: {payload.get('report_type') or 'unknown'}",
    ]
    download = payload.get("download") if isinstance(payload.get("download"), Mapping) else {}
    lines.extend(_github_run_download_lines(download))
    summary = payload.get("summary") if isinstance(payload.get("summary"), Mapping) else {}
    if payload.get("report_type") == "aggregate":
        lines.extend(
            [
                f"Artifacts: {summary.get('artifact_count')}",
                f"Contract drift artifacts: {summary.get('contract_drift_artifact_count')}",
                f"Requirement failure artifacts: {summary.get('requirement_failed_artifact_count')}",
            ]
        )
    else:
        artifact_path = payload.get("artifact_path")
        if artifact_path is not None:
            lines.append(f"Artifact: {artifact_path}")
        lines.append(f"Baseline contract ok: {summary.get('baseline_contract_ok')}")
    if payload.get("expected_artifact_count") is not None:
        lines.append(f"Expected artifacts: {payload.get('expected_artifact_count')}")
        lines.append(f"Discovered artifacts: {payload.get('actual_artifact_count')}")
    lines.append(f"Failure count: {payload.get('failure_count')}")
    failures = payload.get("failures")
    if isinstance(failures, list) and failures:
        lines.append("Failures:")
        lines.extend(f"- {failure}" for failure in failures)
    return "\n".join(lines)


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
        prog="resource-hunter-packaging-baseline-gate",
        description=(
            "Evaluate archived packaging-baseline.json artifacts through the shared Python API and "
            "exit with code 2 when contract drift is detected."
        ),
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help=(
            "artifact file(s), .zip archive(s), or directories to scan recursively for packaging-baseline.json and nested .zip archives; "
            "defaults to artifacts/packaging-baseline/packaging-baseline.json"
        ),
    )
    parser.add_argument("--json", action="store_true", help="emit a compact gate summary as JSON")
    parser.add_argument(
        "--require-artifact-count",
        type=_positive_int,
        help=(
            "require exactly N discovered packaging-baseline artifacts before evaluating drift; "
            "useful when gating downloaded CI matrix artifacts"
        ),
    )
    parser.add_argument(
        "--github-run",
        help=(
            "download packaging-baseline artifacts from a GitHub Actions run with `gh run download` before gating; "
            "pass `latest` to auto-select the most recent completed resource-hunter-ci run; "
            "defaults to the resource-hunter-packaging-baseline-* artifact pattern"
        ),
    )
    parser.add_argument(
        "--github-workflow",
        help=(
            "workflow name passed to `gh run list --workflow` when --github-run latest is used; "
            f"defaults to {DEFAULT_GITHUB_RUN_WORKFLOW}"
        ),
    )
    parser.add_argument(
        "--github-run-list-limit",
        type=_positive_int,
        help=(
            "max completed runs to scan when --github-run latest resolves a workflow-filtered run or "
            f"artifact-discovery fallback; defaults to {_GITHUB_RUN_LIST_LIMIT}"
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
        help="directory passed to `gh run download --dir`; defaults to a temporary directory when --github-run is used",
    )
    parser.add_argument(
        "--keep-download-dir",
        action="store_true",
        help="retain the temporary download directory created for --github-run evaluation",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    ensure_utf8_stdio()
    parser = _build_parser()
    args = parser.parse_args(argv)
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
    try:
        if args.github_run:
            payload = evaluate_packaging_baseline_gate_from_github_run(
                args.github_run,
                repo=args.repo,
                github_workflow=args.github_workflow,
                github_run_list_limit=args.github_run_list_limit,
                artifact_names=args.artifact_names,
                artifact_patterns=args.artifact_patterns,
                download_dir=args.download_dir,
                keep_download_dir=args.keep_download_dir,
                required_artifact_count=args.require_artifact_count,
            )
        else:
            payload = evaluate_packaging_baseline_gate(
                args.paths,
                required_artifact_count=args.require_artifact_count,
            )
    except ResourceHunterError as exc:
        if args.json:
            download_payload = getattr(exc, "download_payload", None)
            print(
                dump_json(
                    build_packaging_baseline_gate_error_payload(
                        str(exc),
                        required_artifact_count=args.require_artifact_count,
                        download_payload=download_payload,
                    )
                )
            )
        print(str(exc), file=sys.stderr)
        return 1
    if args.json:
        print(dump_json(payload))
    else:
        print(format_packaging_baseline_gate_text(payload))
    failures = payload.get("failures")
    if isinstance(failures, list) and failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "DEFAULT_GITHUB_ARTIFACT_PATTERN",
    "PACKAGING_BASELINE_GATE_SCHEMA_VERSION",
    "PackagingBaselineGateError",
    "build_packaging_baseline_gate_error_payload",
    "build_packaging_baseline_gate_payload",
    "evaluate_packaging_baseline_gate",
    "evaluate_packaging_baseline_gate_from_github_run",
    "format_packaging_baseline_gate_text",
    "main",
]
