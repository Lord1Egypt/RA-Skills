from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

import pytest

import resource_hunter.cli as cli
import resource_hunter.packaging_gate as packaging_gate
import resource_hunter.packaging_verify as packaging_verify


def _write_packaging_baseline_artifact(
    root: Path,
    artifact_name: str,
    *,
    baseline_contract_ok: bool,
) -> Path:
    artifact_dir = root / artifact_name
    artifact_dir.mkdir(parents=True)
    artifact_path = artifact_dir / "packaging-baseline.json"
    blocked_warning = "Blocked capture did not report failed_step."
    blocked_capture = {
        "path": str(artifact_dir / "blocked-packaging-capture.json"),
        "project_root": str(root),
        "project_root_source": "argument",
        "requested_project_root": str(root),
        "packaging_python": str(root / "__blocked_python__" / "missing-python"),
        "packaging_python_source": "argument",
        "doctor_packaging_ready": False,
        "packaging_smoke_ok": False,
        "strategy": "blocked" if baseline_contract_ok else "prefix-install",
        "strategy_family": "blocked" if baseline_contract_ok else "usable",
        "reason": "Packaging smoke blocked." if baseline_contract_ok else "Packaging smoke unexpectedly passed.",
        "failed_step": "packaging-status" if baseline_contract_ok else None,
        "expected_outcome": {
            "doctor_packaging_ready": False,
            "packaging_smoke_ok": False,
            "failed_step_present": True,
            "strategy_family_any_of": ["blocked"],
        },
        "matches_expectation": baseline_contract_ok,
        "expectation_drift": []
        if baseline_contract_ok
        else [
            {
                "capture": "blocked",
                "field": "failed_step",
                "kind": "missing_failed_step",
                "expected_present": True,
                "actual": None,
                "message": blocked_warning,
            }
        ],
    }
    payload = {
        "schema_version": 1,
        "captured_at": "2026-03-23T00:00:00Z",
        "output_dir": str(artifact_dir),
        "project_root": str(root),
        "project_root_source": "argument",
        "requested_project_root": str(root),
        "blocked_python": str(root / "__blocked_python__" / "missing-python"),
        "passing_capture": {
            "path": str(artifact_dir / "passing-packaging-capture.json"),
            "project_root": str(root),
            "project_root_source": "argument",
            "requested_project_root": str(root),
            "packaging_python": sys.executable,
            "packaging_python_source": "current",
            "doctor_packaging_ready": True,
            "packaging_smoke_ok": True,
            "strategy": "venv",
            "strategy_family": "usable",
            "reason": "Packaging smoke passed.",
            "failed_step": None,
            "expected_outcome": {
                "doctor_packaging_ready": True,
                "packaging_smoke_ok": True,
                "failed_step_present": False,
                "strategy_family_any_of": ["usable"],
            },
            "matches_expectation": True,
            "expectation_drift": [],
        },
        "blocked_capture": blocked_capture,
        "summary": {
            "passing_capture_matches_expectation": True,
            "blocked_capture_matches_expectation": baseline_contract_ok,
            "baseline_contract_ok": baseline_contract_ok,
        },
        "warnings": [] if baseline_contract_ok else [blocked_warning],
        "requirements": {
            "require_expected_outcomes": True,
            "ok": baseline_contract_ok,
            "failures": []
            if baseline_contract_ok
            else [f"Packaging baseline requirement failed: {blocked_warning}"],
        },
    }
    artifact_path.write_text(json.dumps(payload), encoding="utf-8")
    return artifact_path


def _write_packaging_baseline_artifact_with_passing_probe_error(
    root: Path,
    artifact_name: str,
    *,
    packaging_error: str,
) -> Path:
    artifact_path = _write_packaging_baseline_artifact(
        root,
        artifact_name,
        baseline_contract_ok=True,
    )
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    payload["passing_capture"].update(
        {
            "doctor_packaging_ready": False,
            "packaging_smoke_ok": False,
            "strategy": "blocked",
            "strategy_family": "blocked",
            "reason": "Packaging smoke is blocked: Unable to inspect packaging modules.",
            "failed_step": "packaging-status",
            "matches_expectation": False,
            "expectation_drift": [
                {
                    "capture": "passing",
                    "field": "doctor_packaging_ready",
                    "kind": "unexpected_false",
                    "expected": True,
                    "actual": False,
                    "message": "Passing capture did not report doctor_packaging_ready=true.",
                }
            ],
            "doctor": {
                "packaging": {
                    "error": packaging_error,
                    "blockers": [],
                    "bootstrap_build_deps_ready": False,
                    "bootstrap_build_requirements": ["setuptools>=69", "wheel"],
                    "packaging_smoke_ready_with_bootstrap": False,
                }
            },
        }
    )
    payload["summary"] = {
        "passing_capture_matches_expectation": False,
        "blocked_capture_matches_expectation": True,
        "baseline_contract_ok": False,
    }
    payload["warnings"] = ["Passing capture did not report doctor_packaging_ready=true."]
    payload["requirements"] = {
        "require_expected_outcomes": True,
        "ok": False,
        "failures": [
            "Packaging baseline requirement failed: Passing capture did not report doctor_packaging_ready=true."
        ],
    }
    artifact_path.write_text(json.dumps(payload), encoding="utf-8")
    return artifact_path


def _write_packaging_baseline_artifact_with_legacy_passing_probe_error_reason(
    root: Path,
    artifact_name: str,
    *,
    packaging_error: str,
) -> Path:
    artifact_path = _write_packaging_baseline_artifact_with_passing_probe_error(
        root,
        artifact_name,
        packaging_error=packaging_error,
    )
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    payload["passing_capture"]["reason"] = f"Packaging smoke is blocked: {packaging_error}"
    payload["passing_capture"].pop("doctor", None)
    payload["passing_capture"].pop("packaging_smoke", None)
    artifact_path.write_text(json.dumps(payload), encoding="utf-8")
    return artifact_path


def test_packaging_baseline_verify_main_saves_outputs_from_latest_run(capsys, monkeypatch, tmp_path):
    output_dir = tmp_path / "verify-output"
    output_archive = tmp_path / "verify-bundle.zip"
    workflow_name = "packaging-baseline-nightly"
    run_list_limit = 35
    commands: list[list[str]] = []

    def fake_run_command(args: list[str], *, cwd: Path) -> dict[str, object]:
        commands.append(list(args))
        if args[:3] == ["/fake/bin/gh", "run", "list"]:
            return {
                "command": list(args),
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": json.dumps(
                    [
                        {
                            "databaseId": 987654,
                            "status": "completed",
                            "conclusion": "success",
                            "workflowName": packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW,
                            "headBranch": "main",
                            "event": "push",
                            "url": "https://github.com/openclaw/resource-hunter/actions/runs/987654",
                            "displayTitle": "Packaging baseline",
                        }
                    ]
                ),
                "stderr": "",
            }
        download_dir = output_dir / "download"
        _write_packaging_baseline_artifact(
            download_dir,
            "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
            baseline_contract_ok=True,
        )
        return {
            "command": list(args),
            "cwd": str(cwd),
            "returncode": 0,
            "stdout": "downloaded",
            "stderr": "",
        }

    monkeypatch.setenv("GITHUB_REPOSITORY", "openclaw/resource-hunter")
    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(packaging_gate, "_run_command", fake_run_command)

    rc = packaging_verify.main(
        [
            "--github-run",
            "latest",
            "--github-workflow",
            workflow_name,
            "--github-run-list-limit",
            str(run_list_limit),
            "--output-dir",
            str(output_dir),
            "--output-archive",
            str(output_archive),
            "--archive-downloads",
            "--require-artifact-count",
            "1",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    assert "Status: ok" in captured.out
    assert "GitHub run: 987654 (requested latest)" in captured.out
    assert f"Latest run scan limit: {run_list_limit}" in captured.out
    assert "Report status: ok" in captured.out
    assert "Gate status: ok" in captured.out
    assert commands == [
        [
            "/fake/bin/gh",
            "run",
            "list",
            "--workflow",
            workflow_name,
            "--limit",
            str(run_list_limit),
            "--json",
            "databaseId,status,conclusion,workflowName,headBranch,event,url,displayTitle",
            "--repo",
            "openclaw/resource-hunter",
        ],
        [
            "/fake/bin/gh",
            "run",
            "download",
            "987654",
            "--repo",
            "openclaw/resource-hunter",
            "--dir",
            str((output_dir / "download").resolve()),
            "--pattern",
            packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN,
        ],
    ]
    verify_payload = json.loads((output_dir / "verify.json").read_text(encoding="utf-8"))
    assert verify_payload["ok"] is True
    assert verify_payload["report_ok"] is True
    assert verify_payload["gate_ok"] is True
    assert verify_payload["download"]["github_run_list_limit"] == run_list_limit
    assert verify_payload["download"]["resolved_artifact_count"] == 1
    assert verify_payload["saved_outputs"]["report_json"] == str((output_dir / "report.json").resolve())
    assert verify_payload["saved_outputs"]["bundle_manifest"] == str((output_dir / "bundle-manifest.json").resolve())
    assert verify_payload["saved_outputs"]["output_archive"] == str(output_archive.resolve())
    assert (output_dir / "report.txt").exists()
    assert (output_dir / "gate.json").exists()
    assert (output_dir / "gate.txt").exists()
    assert (output_dir / "verify.txt").exists()
    bundle_manifest = json.loads((output_dir / "bundle-manifest.json").read_text(encoding="utf-8"))
    assert bundle_manifest["ok"] is True
    assert bundle_manifest["download_bundle_member_count"] == 1
    assert bundle_manifest["download_bundle_members"] == [
        "download/resource-hunter-packaging-baseline-ubuntu-latest-py3.12/packaging-baseline.json"
    ]
    assert bundle_manifest["bundle_members"] == [
        "report.json",
        "report.txt",
        "gate.json",
        "gate.txt",
        "verify.json",
        "verify.txt",
        "bundle-manifest.json",
        "download/resource-hunter-packaging-baseline-ubuntu-latest-py3.12/packaging-baseline.json",
    ]
    with zipfile.ZipFile(output_archive) as archive:
        assert archive.namelist() == bundle_manifest["bundle_members"]


def test_packaging_baseline_verify_main_falls_back_to_next_inferred_repo_for_numeric_run(
    capsys, monkeypatch, tmp_path
):
    output_dir = tmp_path / "verify-output"
    commands: list[list[str]] = []

    def fake_git_run(args, *, cwd, check, capture_output, text, timeout):
        assert args == ["git", "remote", "get-url", "origin"]
        assert check is False
        assert capture_output is True
        assert text is True
        assert timeout == 10
        return packaging_gate.subprocess.CompletedProcess(
            args=args,
            returncode=0,
            stdout="https://github.com/openclaw/resource-hunter.git\n",
            stderr="",
        )

    def fake_run_command(args: list[str], *, cwd: Path) -> dict[str, object]:
        command = list(args)
        commands.append(command)
        if command[:3] != ["/fake/bin/gh", "run", "download"]:
            raise AssertionError(f"unexpected gh invocation: {command}")
        repo = command[command.index("--repo") + 1] if "--repo" in command else None
        if repo == "stale/resource-hunter":
            return {
                "command": command,
                "cwd": str(cwd),
                "returncode": 1,
                "stdout": "",
                "stderr": (
                    "failed to get run 123456: HTTP 404: Not Found "
                    "(https://api.github.com/repos/stale/resource-hunter/actions/runs/123456)\n"
                ),
            }
        if repo == "openclaw/resource-hunter":
            download_dir = output_dir / "download"
            _write_packaging_baseline_artifact(
                download_dir,
                "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
                baseline_contract_ok=True,
            )
            return {
                "command": command,
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": "downloaded",
                "stderr": "",
            }
        raise AssertionError(f"unexpected repo fallback target: {command}")

    monkeypatch.setenv("GITHUB_REPOSITORY", "stale/resource-hunter")
    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(packaging_gate.subprocess, "run", fake_git_run)
    monkeypatch.setattr(packaging_gate, "_run_command", fake_run_command)

    rc = packaging_verify.main(
        [
            "--github-run",
            "123456",
            "--output-dir",
            str(output_dir),
            "--require-artifact-count",
            "1",
            "--json",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    payload = json.loads(captured.out)
    assert payload["ok"] is True
    assert payload["download"]["repo"] == "openclaw/resource-hunter"
    assert payload["download"]["repo_source"] == "git-origin"
    attempts = payload["download"]["download_attempts"]
    assert len(attempts) == 2
    assert attempts[0]["repo"] == "stale/resource-hunter"
    assert attempts[1]["repo"] == "openclaw/resource-hunter"
    assert attempts[1]["selected"] is True
    assert commands == [
        [
            "/fake/bin/gh",
            "run",
            "download",
            "123456",
            "--repo",
            "stale/resource-hunter",
            "--dir",
            str((output_dir / "download").resolve()),
            "--pattern",
            packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN,
        ],
        [
            "/fake/bin/gh",
            "run",
            "download",
            "123456",
            "--repo",
            "openclaw/resource-hunter",
            "--dir",
            str((output_dir / "download").resolve()),
            "--pattern",
            packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN,
        ],
    ]


def test_packaging_baseline_verify_main_json_exits_2_on_gate_failure(capsys, monkeypatch, tmp_path):
    output_dir = tmp_path / "verify-output"
    output_archive = tmp_path / "verify-bundle.zip"

    def fake_run_command(args: list[str], *, cwd: Path) -> dict[str, object]:
        if args[:3] == ["/fake/bin/gh", "run", "list"]:
            return {
                "command": list(args),
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": json.dumps(
                    [
                        {
                            "databaseId": 987654,
                            "status": "completed",
                            "conclusion": "success",
                            "workflowName": packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW,
                            "headBranch": "main",
                            "event": "push",
                            "url": "https://github.com/openclaw/resource-hunter/actions/runs/987654",
                            "displayTitle": "Packaging baseline",
                        }
                    ]
                ),
                "stderr": "",
            }
        if args[:2] == ["/fake/bin/gh", "api"]:
            return {
                "command": list(args),
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": json.dumps(
                    {
                        "artifacts": [
                            {"name": "resource-hunter-packaging-baseline-ubuntu-latest-py3.12"}
                        ]
                    }
                ),
                "stderr": "",
            }
        if args[:2] == ["/fake/bin/gh", "api"]:
            return {
                "command": list(args),
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": json.dumps(
                    {
                        "artifacts": [
                            {"name": "resource-hunter-packaging-baseline-ubuntu-latest-py3.12"}
                        ]
                    }
                ),
                "stderr": "",
            }
        if args[:3] == ["/fake/bin/gh", "run", "download"]:
            download_dir = output_dir / "download"
            _write_packaging_baseline_artifact(
                download_dir,
                "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
                baseline_contract_ok=False,
            )
            return {
                "command": list(args),
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": "downloaded",
                "stderr": "",
            }
        raise AssertionError(f"unexpected gh invocation: {args}")

    monkeypatch.setenv("GITHUB_REPOSITORY", "openclaw/resource-hunter")
    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(packaging_gate, "_run_command", fake_run_command)

    rc = packaging_verify.main(
        [
            "--github-run",
            "latest",
            "--output-dir",
            str(output_dir),
            "--output-archive",
            str(output_archive),
            "--json",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 2
    payload = json.loads(captured.out)
    assert payload["ok"] is False
    assert payload["report_ok"] is False
    assert payload["gate_ok"] is False
    assert payload["gate_failure_count"] == 1
    assert "Blocked capture did not report failed_step" in payload["report_failures"][0]
    assert payload["saved_outputs"]["bundle_manifest"] == str((output_dir / "bundle-manifest.json").resolve())
    assert payload["saved_outputs"]["output_archive"] == str(output_archive.resolve())
    with zipfile.ZipFile(output_archive) as archive:
        assert archive.namelist() == [
            "report.json",
            "report.txt",
            "gate.json",
            "gate.txt",
            "verify.json",
            "verify.txt",
            "bundle-manifest.json",
        ]
    assert "Blocked capture did not report failed_step" in captured.err


def test_cli_packaging_baseline_verify_downloads_github_run_artifacts_and_writes_outputs(
    capsys, monkeypatch, tmp_path
):
    output_dir = tmp_path / "verify-output"
    output_archive = tmp_path / "verify-bundle.zip"
    workflow_name = "packaging-baseline-nightly"
    run_list_limit = 35
    commands: list[list[str]] = []

    def fake_run_command(args: list[str], *, cwd: Path) -> dict[str, object]:
        command = list(args)
        commands.append(command)
        if command[:3] == ["/fake/bin/gh", "run", "list"]:
            return {
                "command": command,
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": json.dumps(
                    [
                        {
                            "databaseId": 987654,
                            "status": "completed",
                            "conclusion": "success",
                            "workflowName": workflow_name,
                            "headBranch": "main",
                            "event": "push",
                            "url": "https://github.com/openclaw/resource-hunter/actions/runs/987654",
                            "displayTitle": "Packaging baseline",
                        }
                    ]
                ),
                "stderr": "",
            }
        if command[:3] == ["/fake/bin/gh", "run", "download"]:
            download_dir = output_dir / "download"
            _write_packaging_baseline_artifact(
                download_dir,
                "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
                baseline_contract_ok=True,
            )
            return {
                "command": command,
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": "downloaded",
                "stderr": "",
            }
        raise AssertionError(f"unexpected gh invocation: {command}")

    monkeypatch.setenv("GITHUB_REPOSITORY", "openclaw/resource-hunter")
    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(packaging_gate, "_run_command", fake_run_command)

    rc = cli.main(
        [
            "packaging-baseline-verify",
            "--github-run",
            "latest",
            "--github-workflow",
            workflow_name,
            "--github-run-list-limit",
            str(run_list_limit),
            "--output-dir",
            str(output_dir),
            "--output-archive",
            str(output_archive),
            "--archive-downloads",
            "--require-artifact-count",
            "1",
            "--json",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    payload = json.loads(captured.out)
    assert payload["ok"] is True
    assert payload["report_ok"] is True
    assert payload["gate_ok"] is True
    assert payload["download"]["github_run_list_limit"] == run_list_limit
    assert payload["saved_outputs"]["report_json"] == str((output_dir / "report.json").resolve())
    assert payload["saved_outputs"]["output_archive"] == str(output_archive.resolve())
    bundle_manifest = json.loads((output_dir / "bundle-manifest.json").read_text(encoding="utf-8"))
    assert bundle_manifest["download_bundle_member_count"] == 1
    assert bundle_manifest["download_bundle_members"] == [
        "download/resource-hunter-packaging-baseline-ubuntu-latest-py3.12/packaging-baseline.json"
    ]
    assert commands == [
        [
            "/fake/bin/gh",
            "run",
            "list",
            "--workflow",
            workflow_name,
            "--limit",
            str(run_list_limit),
            "--json",
            "databaseId,status,conclusion,workflowName,headBranch,event,url,displayTitle",
            "--repo",
            "openclaw/resource-hunter",
        ],
        [
            "/fake/bin/gh",
            "run",
            "download",
            "987654",
            "--repo",
            "openclaw/resource-hunter",
            "--dir",
            str((output_dir / "download").resolve()),
            "--pattern",
            packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN,
        ],
    ]


def test_packaging_baseline_verify_main_accepts_local_paths_and_saves_outputs(capsys, tmp_path):
    artifacts_root = tmp_path / "downloaded-artifacts"
    _write_packaging_baseline_artifact(
        artifacts_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        baseline_contract_ok=True,
    )
    output_dir = tmp_path / "verify-output"
    output_archive = tmp_path / "verify-bundle.zip"

    rc = packaging_verify.main(
        [
            str(artifacts_root),
            "--output-dir",
            str(output_dir),
            "--output-archive",
            str(output_archive),
            "--require-artifact-count",
            "1",
            "--json",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    payload = json.loads(captured.out)
    assert payload["status"] == "ok"
    assert payload["ok"] is True
    assert payload["report_ok"] is True
    assert payload["gate_ok"] is True
    assert "download" not in payload
    assert payload["saved_outputs"]["report_json"] == str((output_dir / "report.json").resolve())
    assert payload["saved_outputs"]["output_archive"] == str(output_archive.resolve())
    bundle_manifest = json.loads((output_dir / "bundle-manifest.json").read_text(encoding="utf-8"))
    assert bundle_manifest["status"] == "ok"
    assert "download_bundle_members" not in bundle_manifest
    with zipfile.ZipFile(output_archive) as archive:
        assert sorted(archive.namelist()) == [
            "bundle-manifest.json",
            "gate.json",
            "gate.txt",
            "report.json",
            "report.txt",
            "verify.json",
            "verify.txt",
        ]


def test_cli_packaging_baseline_verify_accepts_local_paths(capsys, tmp_path):
    artifacts_root = tmp_path / "downloaded-artifacts"
    _write_packaging_baseline_artifact(
        artifacts_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        baseline_contract_ok=True,
    )
    output_dir = tmp_path / "verify-output"

    rc = cli.main(
        [
            "packaging-baseline-verify",
            str(artifacts_root),
            "--output-dir",
            str(output_dir),
            "--require-artifact-count",
            "1",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    assert "Status: ok" in captured.out
    assert "Report status: ok" in captured.out
    assert "Gate status: ok" in captured.out
    assert (output_dir / "verify.json").is_file()


def test_cli_packaging_baseline_verify_text_mode_keeps_gate_failures_out_of_stderr(capsys, tmp_path):
    artifacts_root = tmp_path / "downloaded-artifacts"
    _write_packaging_baseline_artifact(
        artifacts_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        baseline_contract_ok=False,
    )

    rc = cli.main([
        "packaging-baseline-verify",
        str(artifacts_root),
    ])

    captured = capsys.readouterr()
    assert rc == 2
    assert "Failure overlap: shared=1; report_only=0; gate_only=0" in captured.out
    assert "Shared report/gate failures:" in captured.out
    assert captured.err == ""


def test_cli_packaging_baseline_verify_rejects_output_archive_without_output_dir():
    with pytest.raises(SystemExit) as excinfo:
        cli.main([
            "packaging-baseline-verify",
            "--github-run",
            "123456",
            "--output-archive",
            "artifacts/packaging-baseline-gh-verify.zip",
        ])

    assert excinfo.value.code == 2


def test_cli_packaging_baseline_verify_rejects_paths_with_github_run(tmp_path):
    artifacts_root = tmp_path / "downloaded-artifacts"
    artifacts_root.mkdir()

    with pytest.raises(SystemExit) as excinfo:
        cli.main(
            [
                "packaging-baseline-verify",
                str(artifacts_root),
                "--github-run",
                "123456",
            ]
        )

    assert excinfo.value.code == 2


def test_cli_packaging_baseline_verify_rejects_archive_downloads_without_output_archive():
    with pytest.raises(SystemExit) as excinfo:
        cli.main([
            "packaging-baseline-verify",
            "--github-run",
            "123456",
            "--output-dir",
            "artifacts/packaging-baseline-gh-verify",
            "--archive-downloads",
        ])

    assert excinfo.value.code == 2


def test_cli_packaging_baseline_verify_rejects_archive_downloads_without_github_run(tmp_path):
    artifacts_root = tmp_path / "downloaded-artifacts"
    artifacts_root.mkdir()

    with pytest.raises(SystemExit) as excinfo:
        cli.main(
            [
                "packaging-baseline-verify",
                str(artifacts_root),
                "--output-dir",
                str(tmp_path / "verify-output"),
                "--output-archive",
                str(tmp_path / "verify-bundle.zip"),
                "--archive-downloads",
            ]
        )

    assert excinfo.value.code == 2



def test_format_packaging_baseline_verify_text_includes_artifact_discovery_summary():
    payload = packaging_verify.build_packaging_baseline_verify_error_payload(
        "GitHub Actions run lookup failed for openclaw/resource-hunter latest resource-hunter-ci run",
        download_payload={
            "provider": "github-actions",
            "run_id": "222222",
            "requested_run_id": "latest",
            "download_dir": "/tmp/download",
            "artifact_names": [],
            "artifact_patterns": [packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN],
            "artifact_filter_source": "default",
            "run_lookup": {
                "strategy": "artifact-discovery",
                "selected_run": {"id": "222222", "workflow_name": "packaging-release"},
                "attempts": [
                    {
                        "workflow_filter_selected_run": {
                            "id": "111111",
                            "workflow_name": packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW,
                        },
                        "workflow_filter_selected_run_artifact_probe": {
                            "artifact_names": ["docs-preview"]
                        },
                        "artifact_discovery": {
                            "repo": "openclaw/resource-hunter",
                            "run_list": {"completed_run_count": 2},
                            "workflow_names": ["docs-ci", "packaging-release"],
                            "artifact_name_samples": ["docs-preview", "packaging-evidence"],
                        }
                    }
                ]
            },
        },
    )

    text = packaging_verify.format_packaging_baseline_verify_text(payload)

    assert "Artifact discovery repo: openclaw/resource-hunter" in text
    assert "Artifact discovery scanned runs: 2" in text
    assert "Artifact discovery workflows: docs-ci, packaging-release" in text
    assert "Artifact discovery artifact samples: docs-preview, packaging-evidence" in text
    assert (
        f"Workflow-filter candidate run: 111111 ({packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW})" in text
    )
    assert "Workflow-filter candidate artifacts: docs-preview" in text


def test_format_packaging_baseline_verify_text_groups_repeated_requirement_failures(tmp_path):
    artifact_root = tmp_path / "downloaded-artifacts"
    for artifact_name in (
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.10",
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.11",
    ):
        _write_packaging_baseline_artifact(
            artifact_root,
            artifact_name,
            baseline_contract_ok=False,
        )

    payload = packaging_verify.verify_packaging_baseline_artifacts([artifact_root])

    assert payload["report"]["artifact_statuses"] == [
        {
            "artifact_path": str(
                (artifact_root / "resource-hunter-packaging-baseline-ubuntu-latest-py3.10" / "packaging-baseline.json").resolve()
            ),
            "artifact_name": "resource-hunter-packaging-baseline-ubuntu-latest-py3.10",
            "artifact_matrix_os": "ubuntu-latest",
            "artifact_matrix_python": "py3.10",
            "artifact_matrix_label": "ubuntu-latest / py3.10",
            "status": "drift",
            "baseline_contract_ok": False,
            "requirement_failure_count": 1,
            "capture_diagnostic_count": 1,
        },
        {
            "artifact_path": str(
                (artifact_root / "resource-hunter-packaging-baseline-ubuntu-latest-py3.11" / "packaging-baseline.json").resolve()
            ),
            "artifact_name": "resource-hunter-packaging-baseline-ubuntu-latest-py3.11",
            "artifact_matrix_os": "ubuntu-latest",
            "artifact_matrix_python": "py3.11",
            "artifact_matrix_label": "ubuntu-latest / py3.11",
            "status": "drift",
            "baseline_contract_ok": False,
            "requirement_failure_count": 1,
            "capture_diagnostic_count": 1,
        },
    ]
    assert payload["report"]["requirement_failure_groups"] == [
        {
            "message": "Blocked capture did not report failed_step.",
            "artifact_count": 2,
            "artifact_labels": [
                "resource-hunter-packaging-baseline-ubuntu-latest-py3.10",
                "resource-hunter-packaging-baseline-ubuntu-latest-py3.11",
            ],
            "artifact_display_labels": [
                "ubuntu-latest / py3.10",
                "ubuntu-latest / py3.11",
            ],
            "artifact_paths": [
                str(
                    (artifact_root / "resource-hunter-packaging-baseline-ubuntu-latest-py3.10" / "packaging-baseline.json").resolve()
                ),
                str(
                    (artifact_root / "resource-hunter-packaging-baseline-ubuntu-latest-py3.11" / "packaging-baseline.json").resolve()
                ),
            ],
        }
    ]
    text = packaging_verify.format_packaging_baseline_verify_text(payload)

    assert "Artifact status summary:" in text
    assert (
        "- ubuntu-latest / py3.10: status=drift; baseline_contract_ok=false; "
        "requirement_failures=1; capture_diagnostics=1" in text
    )
    assert (
        "- ubuntu-latest / py3.11: status=drift; baseline_contract_ok=false; "
        "requirement_failures=1; capture_diagnostics=1" in text
    )
    assert "Requirement failure groups:" in text
    assert (
        "- Blocked capture did not report failed_step. "
        "(2 artifacts: ubuntu-latest / py3.10, ubuntu-latest / py3.11)" in text
    )
    assert payload["failure_overlap"]["shared_failure_count"] == 2
    assert payload["failure_overlap"]["report_only_failure_count"] == 0
    assert payload["failure_overlap"]["gate_only_failure_count"] == 0
    assert payload["failure_overlap"]["report_matches_gate"] is True
    assert payload["failure_overlap"]["shared_failure_groups"] == [
        {
            "message": "Blocked capture did not report failed_step.",
            "failure_count": 2,
            "raw_failures": [
                str(
                    (artifact_root / "resource-hunter-packaging-baseline-ubuntu-latest-py3.10" / "packaging-baseline.json").resolve()
                ) + ": Packaging baseline requirement failed: Blocked capture did not report failed_step.",
                str(
                    (artifact_root / "resource-hunter-packaging-baseline-ubuntu-latest-py3.11" / "packaging-baseline.json").resolve()
                ) + ": Packaging baseline requirement failed: Blocked capture did not report failed_step.",
            ],
            "artifact_count": 2,
            "artifact_labels": [
                "resource-hunter-packaging-baseline-ubuntu-latest-py3.10",
                "resource-hunter-packaging-baseline-ubuntu-latest-py3.11",
            ],
            "artifact_display_labels": ["ubuntu-latest / py3.10", "ubuntu-latest / py3.11"],
            "artifact_paths": [
                str(
                    (artifact_root / "resource-hunter-packaging-baseline-ubuntu-latest-py3.10" / "packaging-baseline.json").resolve()
                ),
                str(
                    (artifact_root / "resource-hunter-packaging-baseline-ubuntu-latest-py3.11" / "packaging-baseline.json").resolve()
                ),
            ],
        }
    ]
    assert "Failure overlap: shared=2; report_only=0; gate_only=0" in text
    assert "Shared report/gate failures:" in text
    assert (
        "- Blocked capture did not report failed_step. "
        "(2 artifacts: ubuntu-latest / py3.10, ubuntu-latest / py3.11)" in text
    )
    assert "Report failures:" not in text
    assert "Gate failures:" not in text


def test_build_packaging_baseline_verify_payload_tracks_failure_overlap():
    shared_failure = "/tmp/shared/packaging-baseline.json: Packaging baseline requirement failed: drift"
    report_only_failure = "/tmp/report-only/packaging-baseline.json: Packaging baseline requirement failed: drift"
    gate_only_failure = "Expected 6 packaging-baseline artifacts but found 5."
    payload = packaging_verify.build_packaging_baseline_verify_payload(
        {
            "report_type": "aggregate",
            "artifacts": [
                {
                    "artifact_path": "/tmp/shared/packaging-baseline.json",
                    "summary": {"baseline_contract_ok": False},
                    "requirements": {
                        "ok": False,
                        "failures": ["Packaging baseline requirement failed: drift"],
                    },
                },
                {
                    "artifact_path": "/tmp/report-only/packaging-baseline.json",
                    "summary": {"baseline_contract_ok": False},
                    "requirements": {
                        "ok": False,
                        "failures": ["Packaging baseline requirement failed: drift"],
                    },
                },
            ],
        },
        {
            "ok": False,
            "failure_count": 2,
            "failures": [shared_failure, gate_only_failure],
        },
    )

    assert payload["failure_overlap"]["shared_failure_count"] == 1
    assert payload["failure_overlap"]["shared_failures"] == [shared_failure]
    assert payload["failure_overlap"]["shared_failure_groups"] == [
        {
            "message": "drift",
            "failure_count": 1,
            "raw_failures": [shared_failure],
            "artifact_count": 1,
            "artifact_labels": ["shared"],
            "artifact_display_labels": ["shared"],
            "artifact_paths": ["/tmp/shared/packaging-baseline.json"],
        }
    ]
    assert payload["failure_overlap"]["report_only_failure_count"] == 1
    assert payload["failure_overlap"]["report_only_failures"] == [report_only_failure]
    assert payload["failure_overlap"]["report_only_failure_groups"] == [
        {
            "message": "drift",
            "failure_count": 1,
            "raw_failures": [report_only_failure],
            "artifact_count": 1,
            "artifact_labels": ["report-only"],
            "artifact_display_labels": ["report-only"],
            "artifact_paths": ["/tmp/report-only/packaging-baseline.json"],
        }
    ]
    assert payload["failure_overlap"]["gate_only_failure_count"] == 1
    assert payload["failure_overlap"]["gate_only_failures"] == [gate_only_failure]
    assert payload["failure_overlap"]["gate_only_failure_groups"] == [
        {
            "message": gate_only_failure,
            "failure_count": 1,
            "raw_failures": [gate_only_failure],
            "artifact_count": 0,
            "artifact_labels": [],
            "artifact_display_labels": [],
            "artifact_paths": [],
        }
    ]
    assert payload["failure_overlap"]["report_matches_gate"] is False

    text = packaging_verify.format_packaging_baseline_verify_text(payload)

    assert "Failure overlap: shared=1; report_only=1; gate_only=1" in text
    assert "Shared report/gate failures:" in text
    assert "- drift (1 artifact: shared)" in text
    assert "Report-only failures:" in text
    assert "- drift (1 artifact: report-only)" in text
    assert "Gate-only failures:" in text
    assert gate_only_failure in text
    assert "Report failures:" not in text
    assert "Gate failures:" not in text


def test_format_packaging_baseline_verify_text_includes_drift_diagnostics(tmp_path):
    artifact_root = tmp_path / "downloaded-artifacts"
    _write_packaging_baseline_artifact_with_passing_probe_error(
        artifact_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.10",
        packaging_error=(
            "Unable to inspect packaging modules via /opt/python/3.10/bin/python: "
            "Traceback ...\nAssertionError: /opt/python/3.10/lib/python3.10/distutils/core.py"
        ),
    )
    _write_packaging_baseline_artifact_with_passing_probe_error(
        artifact_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.11",
        packaging_error=(
            "Unable to inspect packaging modules via /opt/python/3.11/bin/python: "
            "Traceback ...\nAssertionError: /opt/python/3.11/lib/python3.11/distutils/core.py"
        ),
    )

    payload = packaging_verify.verify_packaging_baseline_artifacts([artifact_root])

    assert payload["report"]["artifact_statuses"] == [
        {
            "artifact_path": str(
                (artifact_root / "resource-hunter-packaging-baseline-ubuntu-latest-py3.10" / "packaging-baseline.json").resolve()
            ),
            "artifact_name": "resource-hunter-packaging-baseline-ubuntu-latest-py3.10",
            "artifact_matrix_os": "ubuntu-latest",
            "artifact_matrix_python": "py3.10",
            "artifact_matrix_label": "ubuntu-latest / py3.10",
            "status": "drift",
            "baseline_contract_ok": False,
            "requirement_failure_count": 1,
            "capture_diagnostic_count": 1,
        },
        {
            "artifact_path": str(
                (artifact_root / "resource-hunter-packaging-baseline-ubuntu-latest-py3.11" / "packaging-baseline.json").resolve()
            ),
            "artifact_name": "resource-hunter-packaging-baseline-ubuntu-latest-py3.11",
            "artifact_matrix_os": "ubuntu-latest",
            "artifact_matrix_python": "py3.11",
            "artifact_matrix_label": "ubuntu-latest / py3.11",
            "status": "drift",
            "baseline_contract_ok": False,
            "requirement_failure_count": 1,
            "capture_diagnostic_count": 1,
        },
    ]
    assert len(payload["report"]["capture_diagnostics"]) == 2
    assert len(payload["report"]["capture_diagnostic_groups"]) == 1
    assert payload["report"]["capture_diagnostic_groups"][0]["artifact_count"] == 2
    assert payload["report"]["capture_diagnostic_groups"][0]["artifact_labels"] == [
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.10",
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.11",
    ]
    assert payload["report"]["capture_diagnostic_groups"][0]["artifact_display_labels"] == [
        "ubuntu-latest / py3.10",
        "ubuntu-latest / py3.11",
    ]
    assert payload["report"]["capture_diagnostic_groups"][0]["packaging_error_signature"] == "AssertionError: */distutils/core.py"
    assert payload["report"]["capture_diagnostic_groups"][0]["packaging_error_summary_count"] == 2

    text = packaging_verify.format_packaging_baseline_verify_text(payload)

    assert "Artifact status summary:" in text
    assert (
        "- ubuntu-latest / py3.10: status=drift; baseline_contract_ok=false; "
        "requirement_failures=1; capture_diagnostics=1" in text
    )
    assert "Drift diagnostic groups:" in text
    assert (
        "- Passing: failed_step=packaging-status; strategy_family=blocked; strategy=blocked; "
        "reason=Packaging smoke is blocked: Unable to inspect packaging modules.; "
        "packaging_error=AssertionError: */distutils/core.py (2 variants); "
        "bootstrap_build_requirements=setuptools>=69, wheel; bootstrap_build_deps_ready=false; "
        "packaging_smoke_ready_with_bootstrap=false "
        "(2 artifacts: ubuntu-latest / py3.10, ubuntu-latest / py3.11)" in text
    )
    assert "Drift diagnostics:" in text
    assert "ubuntu-latest / py3.10 / Passing" in text
    assert "failed_step=packaging-status" in text
    assert "strategy_family=blocked" in text
    assert (
        "packaging_error=AssertionError: /opt/python/3.10/lib/python3.10/distutils/core.py" in text
    )
    assert "bootstrap_build_requirements=setuptools>=69, wheel" in text
    assert "bootstrap_build_deps_ready=false" in text
    assert "packaging_smoke_ready_with_bootstrap=false" in text


def test_format_packaging_baseline_verify_text_groups_legacy_reason_only_diagnostics(tmp_path):
    artifact_root = tmp_path / "downloaded-artifacts"
    _write_packaging_baseline_artifact_with_legacy_passing_probe_error_reason(
        artifact_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.10",
        packaging_error=(
            "Unable to inspect packaging modules via /opt/python/3.10/bin/python: "
            "Traceback ...\nAssertionError: /opt/python/3.10/lib/python3.10/distutils/core.py"
        ),
    )
    _write_packaging_baseline_artifact_with_legacy_passing_probe_error_reason(
        artifact_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.11",
        packaging_error=(
            "Unable to inspect packaging modules via /opt/python/3.11/bin/python: "
            "Traceback ...\nAssertionError: /opt/python/3.11/lib/python3.11/distutils/core.py"
        ),
    )

    payload = packaging_verify.verify_packaging_baseline_artifacts([artifact_root])

    assert len(payload["report"]["capture_diagnostic_groups"]) == 1
    assert payload["report"]["capture_diagnostic_groups"][0]["reason"] == (
        "Packaging smoke is blocked: Unable to inspect packaging modules."
    )
    assert payload["report"]["capture_diagnostic_groups"][0]["artifact_display_labels"] == [
        "ubuntu-latest / py3.10",
        "ubuntu-latest / py3.11",
    ]
    assert payload["report"]["capture_diagnostic_groups"][0]["packaging_error_signature"] == "AssertionError: */distutils/core.py"
    assert payload["report"]["capture_diagnostic_groups"][0]["packaging_error_summary_count"] == 2

    text = packaging_verify.format_packaging_baseline_verify_text(payload)

    assert "Drift diagnostic groups:" in text
    assert (
        "- Passing: failed_step=packaging-status; strategy_family=blocked; strategy=blocked; "
        "reason=Packaging smoke is blocked: Unable to inspect packaging modules.; "
        "packaging_error=AssertionError: */distutils/core.py (2 variants) "
        "(2 artifacts: ubuntu-latest / py3.10, ubuntu-latest / py3.11)" in text
    )
    assert (
        "packaging_error=AssertionError: /opt/python/3.10/lib/python3.10/distutils/core.py" in text
    )
