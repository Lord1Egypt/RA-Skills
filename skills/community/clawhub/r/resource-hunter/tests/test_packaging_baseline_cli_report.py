from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

import pytest

import resource_hunter.cli as cli
import resource_hunter.packaging_gate as packaging_gate


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


def _write_packaging_baseline_archive(archive_path: Path, members: dict[str, dict[str, object]]) -> Path:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path, "w") as archive:
        for member_name, payload in members.items():
            archive.writestr(member_name, json.dumps(payload))
    return archive_path


def test_cli_packaging_baseline_report_single_artifact_can_require_contract_ok(capsys, tmp_path):
    artifact_path = _write_packaging_baseline_artifact(
        tmp_path,
        "resource-hunter-packaging-baseline-windows-py3.13",
        baseline_contract_ok=False,
    )

    rc = cli.main(["packaging-baseline-report", "--require-contract-ok", str(artifact_path)])

    captured = capsys.readouterr()
    assert rc == 2
    assert "Resource Hunter packaging baseline report" in captured.out
    assert str(artifact_path.resolve()) in captured.err
    assert "Packaging baseline requirement failed" in captured.err


def test_cli_packaging_baseline_report_directory_aggregates_json(capsys, tmp_path):
    artifacts_root = tmp_path / "downloaded-artifacts"
    ok_path = _write_packaging_baseline_artifact(
        artifacts_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        baseline_contract_ok=True,
    )
    drift_path = _write_packaging_baseline_artifact(
        artifacts_root,
        "resource-hunter-packaging-baseline-windows-latest-py3.13",
        baseline_contract_ok=False,
    )

    rc = cli.main(["packaging-baseline-report", "--json", str(artifacts_root)])

    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["report_type"] == "aggregate"
    assert report["summary"] == {
        "artifact_count": 2,
        "contract_ok_artifact_count": 1,
        "contract_drift_artifact_count": 1,
        "requirement_failed_artifact_count": 1,
        "warning_count": 1,
        "all_baseline_contracts_ok": False,
    }
    assert report["artifacts_with_contract_drift"] == [str(drift_path.resolve())]
    assert report["artifacts_with_requirement_failures"] == [str(drift_path.resolve())]
    assert report["warnings"] == [
        f"{drift_path.resolve()}: Blocked capture did not report failed_step."
    ]
    assert [artifact["artifact_path"] for artifact in report["artifacts"]] == [
        str(ok_path.resolve()),
        str(drift_path.resolve()),
    ]
    assert report["artifacts"][0]["report_type"] == "single"
    assert report["artifacts"][1]["summary"]["baseline_contract_ok"] is False


def test_cli_packaging_baseline_report_zip_archive_aggregates_json(capsys, tmp_path):
    scratch_root = tmp_path / "scratch"
    ok_path = _write_packaging_baseline_artifact(
        scratch_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        baseline_contract_ok=True,
    )
    drift_path = _write_packaging_baseline_artifact(
        scratch_root,
        "resource-hunter-packaging-baseline-windows-latest-py3.13",
        baseline_contract_ok=False,
    )
    archive_path = _write_packaging_baseline_archive(
        tmp_path / "downloaded-artifacts.zip",
        {
            "job-a/packaging-baseline.json": json.loads(ok_path.read_text(encoding="utf-8")),
            "job-b/packaging-baseline.json": json.loads(drift_path.read_text(encoding="utf-8")),
        },
    )

    rc = cli.main(["packaging-baseline-report", "--json", str(archive_path)])

    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["report_type"] == "aggregate"
    assert report["artifacts_with_contract_drift"] == [
        f"{archive_path.resolve()}!/job-b/packaging-baseline.json"
    ]


def test_cli_packaging_baseline_report_directory_discovers_nested_zip_archives(capsys, tmp_path):
    scratch_root = tmp_path / "scratch"
    ok_path = _write_packaging_baseline_artifact(
        scratch_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        baseline_contract_ok=True,
    )
    drift_path = _write_packaging_baseline_artifact(
        scratch_root,
        "resource-hunter-packaging-baseline-windows-latest-py3.13",
        baseline_contract_ok=False,
    )
    downloads_root = tmp_path / "downloaded-zips"
    archive_path = _write_packaging_baseline_archive(
        downloads_root / "nested" / "downloaded-artifacts.zip",
        {
            "job-a/packaging-baseline.json": json.loads(ok_path.read_text(encoding="utf-8")),
            "job-b/packaging-baseline.json": json.loads(drift_path.read_text(encoding="utf-8")),
        },
    )

    rc = cli.main(["packaging-baseline-report", "--json", str(downloads_root)])

    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["report_type"] == "aggregate"
    assert report["artifacts_with_contract_drift"] == [
        f"{archive_path.resolve()}!/job-b/packaging-baseline.json"
    ]


def test_cli_packaging_baseline_report_directory_without_artifacts_errors(capsys, tmp_path):
    empty_dir = tmp_path / "downloaded-artifacts"
    empty_dir.mkdir()

    rc = cli.main(["packaging-baseline-report", str(empty_dir)])

    captured = capsys.readouterr()
    assert rc == 1
    assert "No packaging-baseline.json artifacts found under" in captured.err
    assert str(empty_dir.resolve()) in captured.err


def test_cli_packaging_baseline_report_downloads_github_run_artifacts(capsys, monkeypatch, tmp_path):
    download_dir = tmp_path / "downloaded-gh-artifacts"
    seen: dict[str, object] = {}
    ubuntu_artifact = download_dir / "resource-hunter-packaging-baseline-ubuntu-latest-py3.12" / "packaging-baseline.json"
    windows_artifact = download_dir / "resource-hunter-packaging-baseline-windows-latest-py3.13" / "packaging-baseline.json"

    def fake_run_command(args, *, cwd, timeout=300):
        seen["args"] = list(args)
        seen["cwd"] = str(cwd)
        seen["timeout"] = timeout
        _write_packaging_baseline_artifact(
            download_dir,
            "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
            baseline_contract_ok=True,
        )
        _write_packaging_baseline_artifact(
            download_dir,
            "resource-hunter-packaging-baseline-windows-latest-py3.13",
            baseline_contract_ok=False,
        )
        return {
            "command": list(args),
            "cwd": str(cwd),
            "returncode": 0,
            "stdout": "downloaded",
            "stderr": "",
        }

    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(packaging_gate, "_run_command", fake_run_command)

    rc = cli.main(
        [
            "packaging-baseline-report",
            "--json",
            "--github-run",
            "123456",
            "--repo",
            "openclaw/resource-hunter",
            "--download-dir",
            str(download_dir),
        ]
    )

    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["report_type"] == "aggregate"
    assert report["summary"] == {
        "artifact_count": 2,
        "contract_ok_artifact_count": 1,
        "contract_drift_artifact_count": 1,
        "requirement_failed_artifact_count": 1,
        "warning_count": 1,
        "all_baseline_contracts_ok": False,
    }
    assert report["download"] == {
        "provider": "github-actions",
        "run_id": "123456",
        "repo": "openclaw/resource-hunter",
        "download_dir": str(download_dir.resolve()),
        "download_dir_source": "argument",
        "download_dir_retained": True,
        "artifact_names": [],
        "artifact_patterns": [packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN],
        "artifact_filter_source": "default",
        "resolved_artifact_count": 2,
        "resolved_artifact_paths": [str(ubuntu_artifact.resolve()), str(windows_artifact.resolve())],
        "resolved_archive_member_count": 0,
        "resolved_filesystem_artifact_count": 2,
        "download_command": [
            "/fake/bin/gh",
            "run",
            "download",
            "123456",
            "--repo",
            "openclaw/resource-hunter",
            "--dir",
            str(download_dir.resolve()),
            "--pattern",
            packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN,
        ],
    }
    assert seen == {
        "args": [
            "/fake/bin/gh",
            "run",
            "download",
            "123456",
            "--repo",
            "openclaw/resource-hunter",
            "--dir",
            str(download_dir.resolve()),
            "--pattern",
            packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN,
        ],
        "cwd": str(Path.cwd()),
        "timeout": 300,
    }


def test_cli_packaging_baseline_report_uses_environment_repo_when_repo_omitted(capsys, monkeypatch, tmp_path):
    download_dir = tmp_path / "downloaded-gh-artifacts"

    def fake_run_command(args, *, cwd, timeout=300):
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

    rc = cli.main(
        [
            "packaging-baseline-report",
            "--json",
            "--github-run",
            "123456",
            "--download-dir",
            str(download_dir),
        ]
    )

    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["download"]["repo"] == "openclaw/resource-hunter"
    assert report["download"]["repo_source"] == "environment"
    assert report["download"]["download_command"] == [
        "/fake/bin/gh",
        "run",
        "download",
        "123456",
        "--repo",
        "openclaw/resource-hunter",
        "--dir",
        str(download_dir.resolve()),
        "--pattern",
        packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN,
    ]


def test_cli_packaging_baseline_report_json_emits_error_payload_when_github_run_has_no_artifacts(
    capsys, monkeypatch, tmp_path
):
    download_dir = tmp_path / "downloaded-gh-artifacts"
    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(
        packaging_gate,
        "_run_command",
        lambda args, *, cwd, timeout=300: {
            "command": list(args),
            "cwd": str(cwd),
            "returncode": 0,
            "stdout": "downloaded",
            "stderr": "",
        },
    )

    rc = cli.main(
        [
            "packaging-baseline-report",
            "--json",
            "--github-run",
            "123456",
            "--repo",
            "openclaw/resource-hunter",
            "--download-dir",
            str(download_dir),
        ]
    )

    error = f"No packaging-baseline.json artifacts found under {download_dir.resolve()}."
    captured = capsys.readouterr()
    assert rc == 1
    assert json.loads(captured.out) == {
        "report_schema_version": 1,
        "report_type": "error",
        "summary": {},
        "warnings": [],
        "error": error,
        "download": {
            "provider": "github-actions",
            "run_id": "123456",
            "repo": "openclaw/resource-hunter",
            "download_dir": str(download_dir.resolve()),
            "download_dir_source": "argument",
            "download_dir_retained": True,
            "artifact_names": [],
            "artifact_patterns": [packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN],
            "artifact_filter_source": "default",
            "resolved_artifact_count": 0,
            "resolved_artifact_paths": [],
            "resolved_archive_member_count": 0,
            "resolved_filesystem_artifact_count": 0,
            "download_command": [
                "/fake/bin/gh",
                "run",
                "download",
                "123456",
                "--repo",
                "openclaw/resource-hunter",
                "--dir",
                str(download_dir.resolve()),
                "--pattern",
                packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN,
            ],
        },
    }
    assert captured.err.strip() == error


def test_cli_packaging_baseline_report_rejects_paths_with_github_run():
    with pytest.raises(SystemExit) as excinfo:
        cli.main(["packaging-baseline-report", "--github-run", "123456", "artifacts/downloaded-gh-artifacts"])

    assert excinfo.value.code == 2


def test_cli_packaging_baseline_report_text_includes_latest_run_resolution(capsys, monkeypatch, tmp_path):
    download_dir = tmp_path / "downloaded-gh-artifacts"
    run_list_limit = 35
    commands: list[list[str]] = []
    artifact_path = download_dir / "resource-hunter-packaging-baseline-ubuntu-latest-py3.12" / "packaging-baseline.json"

    def fake_run_command(args, *, cwd, timeout=300):
        commands.append(list(args))
        if args[2] == "list":
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
                        },
                        {
                            "databaseId": 987653,
                            "status": "completed",
                            "conclusion": "failure",
                            "workflowName": packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW,
                            "headBranch": "main",
                            "event": "push",
                            "url": "https://github.com/openclaw/resource-hunter/actions/runs/987653",
                            "displayTitle": "Older packaging baseline",
                        },
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
        if args[:3] == ["/fake/bin/gh", "run", "download"]:
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
        pytest.fail(f"Unexpected command: {args}")

    monkeypatch.setenv("GITHUB_REPOSITORY", "openclaw/resource-hunter")
    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(packaging_gate, "_run_command", fake_run_command)

    rc = cli.main(
        [
            "packaging-baseline-report",
            "--github-run",
            "latest",
            "--github-run-list-limit",
            str(run_list_limit),
            "--download-dir",
            str(download_dir),
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    assert "github_run: 987654 (requested latest)" in captured.out
    assert "download_repo: openclaw/resource-hunter (environment)" in captured.out
    assert f"download_dir: {download_dir.resolve()}" in captured.out
    assert f"github_run_list_limit: {run_list_limit}" in captured.out
    assert "download_dir_retained: true" in captured.out
    assert "artifact_filter_source: default" in captured.out
    assert f"artifact_patterns: {packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN}" in captured.out
    assert "resolved_artifact_count: 1" in captured.out
    assert "resolved_filesystem_artifact_count: 1" in captured.out
    assert "resolved_archive_member_count: 0" in captured.out
    assert f"resolved_artifact[1]: {artifact_path.resolve()}" in captured.out
    assert f"selected_github_run_workflow: {packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW}" in captured.out
    assert "selected_github_run_status: completed" in captured.out
    assert "selected_github_run_conclusion: success" in captured.out
    assert "selected_github_run_head_branch: main" in captured.out
    assert "selected_github_run_event: push" in captured.out
    assert "selected_github_run_title: Packaging baseline" in captured.out
    assert "selected_github_run_url: https://github.com/openclaw/resource-hunter/actions/runs/987654" in captured.out
    assert commands == [
        [
            "/fake/bin/gh",
            "run",
            "list",
            "--workflow",
            packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW,
            "--limit",
            str(run_list_limit),
            "--json",
            "databaseId,status,conclusion,workflowName,headBranch,event,url,displayTitle",
            "--repo",
            "openclaw/resource-hunter",
        ],
        ["/fake/bin/gh", "api", "repos/openclaw/resource-hunter/actions/runs/987654/artifacts"],
        [
            "/fake/bin/gh",
            "run",
            "download",
            "987654",
            "--repo",
            "openclaw/resource-hunter",
            "--dir",
            str(download_dir.resolve()),
            "--pattern",
            packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN,
        ],
    ]
