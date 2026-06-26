from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

import pytest

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


def test_evaluate_packaging_baseline_gate_aggregates_artifact_tree(tmp_path):
    artifact_root = tmp_path / "downloaded-artifacts"
    ok_path = _write_packaging_baseline_artifact(
        artifact_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        baseline_contract_ok=True,
    )
    drift_path = _write_packaging_baseline_artifact(
        artifact_root,
        "resource-hunter-packaging-baseline-windows-latest-py3.13",
        baseline_contract_ok=False,
    )

    payload = packaging_gate.evaluate_packaging_baseline_gate([artifact_root])

    assert payload == {
        "gate_schema_version": packaging_gate.PACKAGING_BASELINE_GATE_SCHEMA_VERSION,
        "ok": False,
        "failure_count": 1,
        "failures": [
            f"{drift_path.resolve()}: Packaging baseline requirement failed: Blocked capture did not report failed_step."
        ],
        "report_type": "aggregate",
        "summary": {
            "artifact_count": 2,
            "contract_ok_artifact_count": 1,
            "contract_drift_artifact_count": 1,
            "requirement_failed_artifact_count": 1,
            "warning_count": 1,
            "all_baseline_contracts_ok": False,
        },
        "artifacts_with_contract_drift": [str(drift_path.resolve())],
        "artifacts_with_requirement_failures": [str(drift_path.resolve())],
    }
    assert str(ok_path.resolve()) not in payload["failures"]


def test_packaging_baseline_gate_main_json_exits_2_on_drift(capsys, tmp_path):
    artifact_root = tmp_path / "downloaded-artifacts"
    _write_packaging_baseline_artifact(
        artifact_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        baseline_contract_ok=True,
    )
    drift_path = _write_packaging_baseline_artifact(
        artifact_root,
        "resource-hunter-packaging-baseline-windows-latest-py3.13",
        baseline_contract_ok=False,
    )

    rc = packaging_gate.main(["--json", str(artifact_root)])

    captured = capsys.readouterr()
    assert rc == 2
    payload = json.loads(captured.out)
    assert payload["gate_schema_version"] == packaging_gate.PACKAGING_BASELINE_GATE_SCHEMA_VERSION
    assert payload["ok"] is False
    assert payload["failure_count"] == 1
    assert payload["artifacts_with_contract_drift"] == [str(drift_path.resolve())]
    assert (
        f"{drift_path.resolve()}: Packaging baseline requirement failed: Blocked capture did not report failed_step."
        in captured.err
    )


def test_packaging_baseline_gate_main_text_reports_single_ok_artifact(capsys, tmp_path):
    artifact_path = _write_packaging_baseline_artifact(
        tmp_path,
        "resource-hunter-packaging-baseline-windows-latest-py3.13",
        baseline_contract_ok=True,
    )

    rc = packaging_gate.main([str(artifact_path)])

    captured = capsys.readouterr()
    assert rc == 0
    assert "Resource Hunter packaging baseline gate" in captured.out
    assert "Status: ok" in captured.out
    assert f"Artifact: {artifact_path.resolve()}" in captured.out
    assert "Failure count: 0" in captured.out
    assert captured.err == ""


def test_evaluate_packaging_baseline_gate_accepts_zip_archives(tmp_path):
    archive_path = tmp_path / "downloaded-artifacts.zip"
    ok_payload_path = _write_packaging_baseline_artifact(
        tmp_path / "scratch",
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        baseline_contract_ok=True,
    )
    ok_payload = json.loads(ok_payload_path.read_text(encoding="utf-8"))
    drift_payload_path = _write_packaging_baseline_artifact(
        tmp_path / "scratch",
        "resource-hunter-packaging-baseline-windows-latest-py3.13",
        baseline_contract_ok=False,
    )
    drift_payload = json.loads(drift_payload_path.read_text(encoding="utf-8"))
    _write_packaging_baseline_archive(
        archive_path,
        {
            "job-a/packaging-baseline.json": ok_payload,
            "job-b/packaging-baseline.json": drift_payload,
        },
    )

    payload = packaging_gate.evaluate_packaging_baseline_gate([archive_path])

    assert payload["gate_schema_version"] == packaging_gate.PACKAGING_BASELINE_GATE_SCHEMA_VERSION
    assert payload["ok"] is False
    assert payload["artifacts_with_contract_drift"] == [
        f"{archive_path.resolve()}!/job-b/packaging-baseline.json"
    ]


def test_evaluate_packaging_baseline_gate_records_required_artifact_count(tmp_path):
    artifact_root = tmp_path / "downloaded-artifacts"
    _write_packaging_baseline_artifact(
        artifact_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        baseline_contract_ok=True,
    )
    _write_packaging_baseline_artifact(
        artifact_root,
        "resource-hunter-packaging-baseline-windows-latest-py3.13",
        baseline_contract_ok=True,
    )

    payload = packaging_gate.evaluate_packaging_baseline_gate(
        [artifact_root],
        required_artifact_count=2,
    )

    assert payload["ok"] is True
    assert payload["failure_count"] == 0
    assert payload["expected_artifact_count"] == 2
    assert payload["actual_artifact_count"] == 2


def test_packaging_baseline_gate_main_json_exits_2_on_artifact_count_mismatch(capsys, tmp_path):
    artifact_root = tmp_path / "downloaded-artifacts"
    artifact_path = _write_packaging_baseline_artifact(
        artifact_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        baseline_contract_ok=True,
    )

    rc = packaging_gate.main(["--json", "--require-artifact-count", "2", str(artifact_root)])

    captured = capsys.readouterr()
    assert rc == 2
    payload = json.loads(captured.out)
    assert payload["gate_schema_version"] == packaging_gate.PACKAGING_BASELINE_GATE_SCHEMA_VERSION
    assert payload["ok"] is False
    assert payload["failure_count"] == 1
    assert payload["artifact_path"] == str(artifact_path.resolve())
    assert payload["expected_artifact_count"] == 2
    assert payload["actual_artifact_count"] == 1
    assert (
        "Packaging baseline gate expected 2 artifact(s) but found 1."
        in payload["failures"]
    )
    assert "Packaging baseline gate expected 2 artifact(s) but found 1." in captured.err


def test_packaging_baseline_gate_main_json_emits_error_payload_when_artifacts_missing(capsys, tmp_path):
    artifact_root = tmp_path / "downloaded-artifacts"
    artifact_root.mkdir()

    rc = packaging_gate.main(["--json", "--require-artifact-count", "2", str(artifact_root)])

    captured = capsys.readouterr()
    error = f"No packaging-baseline.json artifacts found under {artifact_root.resolve()}."
    assert rc == 1
    assert json.loads(captured.out) == {
        "gate_schema_version": packaging_gate.PACKAGING_BASELINE_GATE_SCHEMA_VERSION,
        "report_type": "error",
        "summary": {},
        "ok": False,
        "failure_count": 1,
        "failures": [error],
        "error": error,
        "expected_artifact_count": 2,
    }
    assert captured.err.strip() == error


def test_packaging_baseline_gate_main_json_exits_2_on_zip_drift(capsys, tmp_path):
    archive_path = tmp_path / "downloaded-artifacts.zip"
    ok_payload_path = _write_packaging_baseline_artifact(
        tmp_path / "scratch",
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        baseline_contract_ok=True,
    )
    ok_payload = json.loads(ok_payload_path.read_text(encoding="utf-8"))
    drift_payload_path = _write_packaging_baseline_artifact(
        tmp_path / "scratch",
        "resource-hunter-packaging-baseline-windows-latest-py3.13",
        baseline_contract_ok=False,
    )
    drift_payload = json.loads(drift_payload_path.read_text(encoding="utf-8"))
    _write_packaging_baseline_archive(
        archive_path,
        {
            "job-a/packaging-baseline.json": ok_payload,
            "job-b/packaging-baseline.json": drift_payload,
        },
    )

    rc = packaging_gate.main(["--json", str(archive_path)])

    captured = capsys.readouterr()
    drift_ref = f"{archive_path.resolve()}!/job-b/packaging-baseline.json"
    assert rc == 2
    payload = json.loads(captured.out)
    assert payload["gate_schema_version"] == packaging_gate.PACKAGING_BASELINE_GATE_SCHEMA_VERSION
    assert payload["ok"] is False
    assert payload["failure_count"] == 1
    assert payload["artifacts_with_contract_drift"] == [drift_ref]
    assert (
        f"{drift_ref}: Packaging baseline requirement failed: Blocked capture did not report failed_step."
        in captured.err
    )


def test_evaluate_packaging_baseline_gate_from_github_run_downloads_artifacts(monkeypatch, tmp_path):
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
            baseline_contract_ok=True,
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

    payload = packaging_gate.evaluate_packaging_baseline_gate_from_github_run(
        "123456",
        repo="openclaw/resource-hunter",
        download_dir=download_dir,
        required_artifact_count=2,
    )

    assert payload["ok"] is True
    assert payload["failure_count"] == 0
    assert payload["expected_artifact_count"] == 2
    assert payload["actual_artifact_count"] == 2
    assert payload["download"] == {
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


def test_evaluate_packaging_baseline_gate_from_github_run_uses_environment_repo_when_repo_omitted(
    monkeypatch, tmp_path
):
    download_dir = tmp_path / "downloaded-gh-artifacts"
    seen: dict[str, object] = {}

    def fake_run_command(args, *, cwd, timeout=300):
        seen["args"] = list(args)
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

    payload = packaging_gate.evaluate_packaging_baseline_gate_from_github_run(
        "123456",
        download_dir=download_dir,
        required_artifact_count=1,
    )

    assert payload["download"]["repo"] == "openclaw/resource-hunter"
    assert payload["download"]["repo_source"] == "environment"
    assert seen["args"] == [
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


def test_evaluate_packaging_baseline_gate_from_github_run_uses_git_origin_repo_when_repo_omitted(
    monkeypatch, tmp_path
):
    download_dir = tmp_path / "downloaded-gh-artifacts"
    seen: dict[str, object] = {}

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

    def fake_run_command(args, *, cwd, timeout=300):
        seen["args"] = list(args)
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

    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(packaging_gate.subprocess, "run", fake_git_run)
    monkeypatch.setattr(packaging_gate, "_run_command", fake_run_command)

    payload = packaging_gate.evaluate_packaging_baseline_gate_from_github_run(
        "123456",
        download_dir=download_dir,
        required_artifact_count=1,
    )

    assert payload["download"]["repo"] == "openclaw/resource-hunter"
    assert payload["download"]["repo_source"] == "git-origin"
    assert seen["args"] == [
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


def test_evaluate_packaging_baseline_gate_from_numeric_run_falls_back_to_next_inferred_repo(
    monkeypatch, tmp_path
):
    download_dir = tmp_path / "downloaded-gh-artifacts"
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

    def fake_run_command(args, *, cwd, timeout=300):
        command = list(args)
        commands.append(command)
        if command[:3] != ["/fake/bin/gh", "run", "download"]:
            pytest.fail(f"Unexpected command: {command}")
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
        pytest.fail(f"Unexpected repo fallback target: {command}")

    monkeypatch.setenv("GITHUB_REPOSITORY", "stale/resource-hunter")
    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(packaging_gate.subprocess, "run", fake_git_run)
    monkeypatch.setattr(packaging_gate, "_run_command", fake_run_command)

    payload = packaging_gate.evaluate_packaging_baseline_gate_from_github_run(
        "123456",
        download_dir=download_dir,
        required_artifact_count=1,
    )

    assert payload["download"]["repo"] == "openclaw/resource-hunter"
    assert payload["download"]["repo_source"] == "git-origin"
    attempts = payload["download"]["download_attempts"]
    assert len(attempts) == 2
    assert attempts[0]["repo"] == "stale/resource-hunter"
    assert attempts[0]["repo_source"] == "environment"
    assert attempts[0]["returncode"] == 1
    assert "GITHUB_REPOSITORY may be stale or inaccessible" in attempts[0]["hint"]
    assert attempts[1]["repo"] == "openclaw/resource-hunter"
    assert attempts[1]["repo_source"] == "git-origin"
    assert attempts[1]["selected"] is True

    text = packaging_gate.format_packaging_baseline_gate_text(payload)
    assert "Download repo attempts: 2" in text

    assert commands == [
        [
            "/fake/bin/gh",
            "run",
            "download",
            "123456",
            "--repo",
            "stale/resource-hunter",
            "--dir",
            str(download_dir.resolve()),
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
            str(download_dir.resolve()),
            "--pattern",
            packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN,
        ],
    ]


def test_evaluate_packaging_baseline_gate_from_numeric_run_reports_attempted_repo_contexts_on_failure(
    monkeypatch, tmp_path
):
    download_dir = tmp_path / "downloaded-gh-artifacts"

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

    def fake_run_command(args, *, cwd, timeout=300):
        command = list(args)
        repo = command[command.index("--repo") + 1] if "--repo" in command else None
        target = repo or "gh-context"
        return {
            "command": command,
            "cwd": str(cwd),
            "returncode": 1,
            "stdout": "",
            "stderr": (
                f"failed to get run 123456 from {target}: HTTP 404: Not Found "
                "(https://api.github.com/repos/example/actions/runs/123456)\n"
            ),
        }

    monkeypatch.setenv("GITHUB_REPOSITORY", "stale/resource-hunter")
    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(packaging_gate.subprocess, "run", fake_git_run)
    monkeypatch.setattr(packaging_gate, "_run_command", fake_run_command)

    with pytest.raises(packaging_gate.PackagingBaselineGateError) as excinfo:
        packaging_gate.evaluate_packaging_baseline_gate_from_github_run(
            "123456",
            download_dir=download_dir,
            required_artifact_count=1,
        )

    message = str(excinfo.value)
    assert "GitHub Actions artifact download failed for run 123456 after trying" in message
    assert "stale/resource-hunter, openclaw/resource-hunter, the current gh context" in message
    download_payload = excinfo.value.download_payload
    assert download_payload["repo_source"] == "gh-context"
    attempts = download_payload["download_attempts"]
    assert len(attempts) == 3
    assert attempts[0]["repo"] == "stale/resource-hunter"
    assert attempts[1]["repo"] == "openclaw/resource-hunter"
    assert attempts[2]["repo_source"] == "gh-context"


def test_packaging_baseline_gate_main_errors_when_gh_download_fails(capsys, monkeypatch):
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(
        packaging_gate.subprocess,
        "run",
        lambda *args, **kwargs: packaging_gate.subprocess.CompletedProcess(args=args[0], returncode=1),
    )
    monkeypatch.setattr(
        packaging_gate,
        "_run_command",
        lambda args, *, cwd, timeout=300: {
            "command": list(args),
            "cwd": str(cwd),
            "returncode": 1,
            "stdout": "",
            "stderr": "artifact download failed",
        },
    )

    rc = packaging_gate.main(["--github-run", "987654"])

    captured = capsys.readouterr()
    assert rc == 1
    assert captured.out == ""
    assert (
        captured.err.strip()
        == "GitHub Actions artifact download failed for run 987654: artifact download failed"
    )


def test_packaging_baseline_gate_main_json_emits_error_payload_when_gh_download_fails(capsys, monkeypatch, tmp_path):
    download_dir = tmp_path / "downloaded-gh-artifacts"
    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(
        packaging_gate,
        "_run_command",
        lambda args, *, cwd, timeout=300: {
            "command": list(args),
            "cwd": str(cwd),
            "returncode": 1,
            "stdout": "",
            "stderr": "artifact download failed",
        },
    )

    rc = packaging_gate.main(
        [
            "--json",
            "--github-run",
            "987654",
            "--repo",
            "openclaw/resource-hunter",
            "--download-dir",
            str(download_dir),
        ]
    )

    captured = capsys.readouterr()
    error = "GitHub Actions artifact download failed for openclaw/resource-hunter run 987654: artifact download failed"
    assert rc == 1
    assert json.loads(captured.out) == {
        "gate_schema_version": packaging_gate.PACKAGING_BASELINE_GATE_SCHEMA_VERSION,
        "report_type": "error",
        "summary": {},
        "ok": False,
        "failure_count": 1,
        "failures": [error],
        "error": error,
        "download": {
            "provider": "github-actions",
            "run_id": "987654",
            "repo": "openclaw/resource-hunter",
            "download_dir": str(download_dir.resolve()),
            "download_dir_source": "argument",
            "download_dir_retained": True,
            "artifact_names": [],
            "artifact_patterns": [packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN],
            "artifact_filter_source": "default",
            "download_command": [
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
            "download_returncode": 1,
            "download_stderr": "artifact download failed",
        },
    }
    assert captured.err.strip() == error


def test_packaging_baseline_gate_main_json_emits_error_payload_when_github_run_has_no_artifacts(
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

    rc = packaging_gate.main(
        [
            "--json",
            "--github-run",
            "123456",
            "--repo",
            "openclaw/resource-hunter",
            "--download-dir",
            str(download_dir),
            "--require-artifact-count",
            "2",
        ]
    )

    captured = capsys.readouterr()
    error = f"No packaging-baseline.json artifacts found under {download_dir.resolve()}."
    assert rc == 1
    assert json.loads(captured.out) == {
        "gate_schema_version": packaging_gate.PACKAGING_BASELINE_GATE_SCHEMA_VERSION,
        "report_type": "error",
        "summary": {},
        "ok": False,
        "failure_count": 1,
        "failures": [error],
        "error": error,
        "expected_artifact_count": 2,
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


def test_packaging_baseline_gate_main_rejects_paths_with_github_run():
    with pytest.raises(SystemExit) as excinfo:
        packaging_gate.main(["--github-run", "123456", "artifacts/downloaded-gh-artifacts"])

    assert excinfo.value.code == 2


def test_packaging_baseline_gate_main_text_includes_latest_run_resolution(capsys, monkeypatch, tmp_path):
    download_dir = tmp_path / "downloaded-gh-artifacts"
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

    rc = packaging_gate.main(
        ["--github-run", "latest", "--download-dir", str(download_dir), "--require-artifact-count", "1"]
    )

    captured = capsys.readouterr()
    assert rc == 0
    assert "Status: ok" in captured.out
    assert "GitHub run: 987654 (requested latest)" in captured.out
    assert "Repository: openclaw/resource-hunter (environment)" in captured.out
    assert f"Downloaded artifacts: {download_dir.resolve()}" in captured.out
    assert "Download dir retained: true" in captured.out
    assert f"Download filters: patterns {packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN} (default)" in captured.out
    assert "Resolved artifacts: 1 total, 1 filesystem, 0 archive members" in captured.out
    assert f"Resolved artifact 1: {artifact_path.resolve()}" in captured.out
    assert f"Selected run workflow: {packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW}" in captured.out
    assert "Selected run status: completed / success" in captured.out
    assert "Selected run branch: main" in captured.out
    assert "Selected run event: push" in captured.out
    assert "Selected run title: Packaging baseline" in captured.out
    assert "Selected run URL: https://github.com/openclaw/resource-hunter/actions/runs/987654" in captured.out
    assert commands == [
        [
            "/fake/bin/gh",
            "run",
            "list",
            "--workflow",
            packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW,
            "--limit",
            "20",
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


def test_evaluate_packaging_baseline_gate_from_latest_run_404_suggests_repo_fallback(monkeypatch, tmp_path):
    download_dir = tmp_path / "downloaded-gh-artifacts"

    def fake_run_command(args, *, cwd, timeout=300):
        return {
            "command": list(args),
            "cwd": str(cwd),
            "returncode": 1,
            "stdout": "",
            "stderr": (
                "couldn't fetch workflows for openclaw/resource-hunter: HTTP 404: Not Found "
                "(https://api.github.com/repos/openclaw/resource-hunter/actions/workflows?per_page=100&page=1)\n"
            ),
        }

    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(packaging_gate, "_run_command", fake_run_command)

    with pytest.raises(packaging_gate.PackagingBaselineGateError) as excinfo:
        packaging_gate.evaluate_packaging_baseline_gate_from_github_run(
            "latest",
            repo="openclaw/resource-hunter",
            download_dir=download_dir,
        )

    message = str(excinfo.value)
    assert "GitHub Actions run lookup failed for openclaw/resource-hunter latest resource-hunter-ci run" in message
    assert "The explicit --repo value may be stale or inaccessible" in message
    assert "omit --repo to fall back to GITHUB_REPOSITORY" in message


def test_evaluate_packaging_baseline_gate_from_latest_run_falls_back_to_next_inferred_repo(
    monkeypatch, tmp_path
):
    download_dir = tmp_path / "downloaded-gh-artifacts"
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

    def fake_run_command(args, *, cwd, timeout=300):
        command = list(args)
        commands.append(command)
        if command[:3] == ["/fake/bin/gh", "run", "list"]:
            repo = command[command.index("--repo") + 1]
            if repo == "stale/resource-hunter":
                return {
                    "command": command,
                    "cwd": str(cwd),
                    "returncode": 1,
                    "stdout": "",
                    "stderr": (
                        "couldn't fetch workflows for stale/resource-hunter: HTTP 404: Not Found "
                        "(https://api.github.com/repos/stale/resource-hunter/actions/workflows?per_page=100&page=1)\n"
                    ),
                }
            if repo == "openclaw/resource-hunter":
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
        if command[:2] == ["/fake/bin/gh", "api"]:
            return {
                "command": command,
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
        if command[:3] == ["/fake/bin/gh", "run", "download"]:
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
        pytest.fail(f"Unexpected command: {command}")

    monkeypatch.setenv("GITHUB_REPOSITORY", "stale/resource-hunter")
    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(packaging_gate.subprocess, "run", fake_git_run)
    monkeypatch.setattr(packaging_gate, "_run_command", fake_run_command)

    payload = packaging_gate.evaluate_packaging_baseline_gate_from_github_run(
        "latest",
        download_dir=download_dir,
        required_artifact_count=1,
    )

    assert payload["download"]["repo"] == "openclaw/resource-hunter"
    assert payload["download"]["repo_source"] == "git-origin"
    attempts = payload["download"]["run_lookup"]["attempts"]
    assert len(attempts) == 2
    assert attempts[0]["repo"] == "stale/resource-hunter"
    assert attempts[0]["repo_source"] == "environment"
    assert attempts[0]["returncode"] == 1
    assert "GITHUB_REPOSITORY may be stale or inaccessible" in attempts[0]["hint"]
    assert attempts[1]["repo"] == "openclaw/resource-hunter"
    assert attempts[1]["repo_source"] == "git-origin"
    assert attempts[1]["matched_run_count"] == 1
    assert attempts[1]["selected_run"]["id"] == "987654"
    assert attempts[1]["workflow_filter_selected_run_artifact_probe"]["matched_artifact_names"] == [
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12"
    ]
    assert commands == [
        [
            "/fake/bin/gh",
            "run",
            "list",
            "--workflow",
            packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW,
            "--limit",
            "20",
            "--json",
            "databaseId,status,conclusion,workflowName,headBranch,event,url,displayTitle",
            "--repo",
            "stale/resource-hunter",
        ],
        [
            "/fake/bin/gh",
            "run",
            "list",
            "--workflow",
            packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW,
            "--limit",
            "20",
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


def test_evaluate_packaging_baseline_gate_from_latest_run_discovers_matching_artifacts_when_default_workflow_missing(
    monkeypatch, tmp_path
):
    download_dir = tmp_path / "downloaded-gh-artifacts"
    commands: list[list[str]] = []

    def fake_run_command(args, *, cwd, timeout=300):
        command = list(args)
        commands.append(command)
        if command[:3] == ["/fake/bin/gh", "run", "list"]:
            if "--workflow" in command:
                return {
                    "command": command,
                    "cwd": str(cwd),
                    "returncode": 1,
                    "stdout": "",
                    "stderr": (
                        "could not find any workflows named resource-hunter-ci in openclaw/resource-hunter\n"
                    ),
                }
            return {
                "command": command,
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": json.dumps(
                    [
                        {
                            "databaseId": 111111,
                            "status": "completed",
                            "conclusion": "success",
                            "workflowName": "docs-ci",
                            "headBranch": "main",
                            "event": "push",
                            "url": "https://github.com/openclaw/resource-hunter/actions/runs/111111",
                            "displayTitle": "Docs",
                        },
                        {
                            "databaseId": 222222,
                            "status": "completed",
                            "conclusion": "success",
                            "workflowName": "packaging-release",
                            "headBranch": "main",
                            "event": "workflow_dispatch",
                            "url": "https://github.com/openclaw/resource-hunter/actions/runs/222222",
                            "displayTitle": "Packaging baseline",
                        },
                    ]
                ),
                "stderr": "",
            }
        if command[:2] == ["/fake/bin/gh", "api"]:
            if command[2] == "repos/openclaw/resource-hunter/actions/runs/111111/artifacts":
                return {
                    "command": command,
                    "cwd": str(cwd),
                    "returncode": 0,
                    "stdout": json.dumps({"artifacts": [{"name": "docs-preview"}]}),
                    "stderr": "",
                }
            if command[2] == "repos/openclaw/resource-hunter/actions/runs/222222/artifacts":
                return {
                    "command": command,
                    "cwd": str(cwd),
                    "returncode": 0,
                    "stdout": json.dumps(
                        {
                            "artifacts": [
                                {"name": "resource-hunter-packaging-baseline-ubuntu-latest-py3.12"},
                                {"name": "resource-hunter-packaging-baseline-windows-latest-py3.13"},
                            ]
                        }
                    ),
                    "stderr": "",
                }
        if command[:3] == ["/fake/bin/gh", "run", "download"]:
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
        pytest.fail(f"Unexpected command: {command}")

    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(packaging_gate, "_run_command", fake_run_command)

    payload = packaging_gate.evaluate_packaging_baseline_gate_from_github_run(
        "latest",
        repo="openclaw/resource-hunter",
        download_dir=download_dir,
        required_artifact_count=1,
    )

    assert payload["ok"] is True
    assert payload["download"]["run_id"] == "222222"
    assert payload["download"]["requested_run_id"] == "latest"
    assert payload["download"]["run_lookup"]["strategy"] == "artifact-discovery"
    attempts = payload["download"]["run_lookup"]["attempts"]
    assert len(attempts) == 1
    assert attempts[0]["artifact_discovery"]["repo"] == "openclaw/resource-hunter"
    assert attempts[0]["artifact_discovery"]["selected_artifact_names"] == [
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        "resource-hunter-packaging-baseline-windows-latest-py3.13",
    ]
    assert attempts[0]["selected_run"]["id"] == "222222"
    assert attempts[0]["selected_run"]["workflow_name"] == "packaging-release"

    text = packaging_gate.format_packaging_baseline_gate_text(payload)
    assert "Selected run lookup strategy: artifact-discovery" in text
    assert "Selected run workflow: packaging-release" in text

    assert commands == [
        [
            "/fake/bin/gh",
            "run",
            "list",
            "--workflow",
            packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW,
            "--limit",
            "20",
            "--json",
            "databaseId,status,conclusion,workflowName,headBranch,event,url,displayTitle",
            "--repo",
            "openclaw/resource-hunter",
        ],
        [
            "/fake/bin/gh",
            "run",
            "list",
            "--status",
            "completed",
            "--limit",
            "20",
            "--json",
            "databaseId,status,conclusion,workflowName,headBranch,event,url,displayTitle",
            "--repo",
            "openclaw/resource-hunter",
        ],
        ["/fake/bin/gh", "api", "repos/openclaw/resource-hunter/actions/runs/111111/artifacts"],
        ["/fake/bin/gh", "api", "repos/openclaw/resource-hunter/actions/runs/222222/artifacts"],
        [
            "/fake/bin/gh",
            "run",
            "download",
            "222222",
            "--repo",
            "openclaw/resource-hunter",
            "--dir",
            str(download_dir.resolve()),
            "--pattern",
            packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN,
        ],
    ]


def test_evaluate_packaging_baseline_gate_from_latest_run_falls_back_when_selected_workflow_run_has_no_matching_artifacts(
    monkeypatch, tmp_path
):
    download_dir = tmp_path / "downloaded-gh-artifacts"
    commands: list[list[str]] = []

    def fake_run_command(args, *, cwd, timeout=300):
        command = list(args)
        commands.append(command)
        if command[:3] == ["/fake/bin/gh", "run", "list"]:
            if "--workflow" in command:
                return {
                    "command": command,
                    "cwd": str(cwd),
                    "returncode": 0,
                    "stdout": json.dumps(
                        [
                            {
                                "databaseId": 111111,
                                "status": "completed",
                                "conclusion": "success",
                                "workflowName": packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW,
                                "headBranch": "main",
                                "event": "push",
                                "url": "https://github.com/openclaw/resource-hunter/actions/runs/111111",
                                "displayTitle": "Default workflow latest",
                            }
                        ]
                    ),
                    "stderr": "",
                }
            return {
                "command": command,
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": json.dumps(
                    [
                        {
                            "databaseId": 111111,
                            "status": "completed",
                            "conclusion": "success",
                            "workflowName": packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW,
                            "headBranch": "main",
                            "event": "push",
                            "url": "https://github.com/openclaw/resource-hunter/actions/runs/111111",
                            "displayTitle": "Default workflow latest",
                        },
                        {
                            "databaseId": 222222,
                            "status": "completed",
                            "conclusion": "success",
                            "workflowName": "packaging-release",
                            "headBranch": "main",
                            "event": "workflow_dispatch",
                            "url": "https://github.com/openclaw/resource-hunter/actions/runs/222222",
                            "displayTitle": "Packaging baseline",
                        },
                    ]
                ),
                "stderr": "",
            }
        if command[:2] == ["/fake/bin/gh", "api"]:
            if command[2] == "repos/openclaw/resource-hunter/actions/runs/111111/artifacts":
                return {
                    "command": command,
                    "cwd": str(cwd),
                    "returncode": 0,
                    "stdout": json.dumps({"artifacts": [{"name": "docs-preview"}]}),
                    "stderr": "",
                }
            if command[2] == "repos/openclaw/resource-hunter/actions/runs/222222/artifacts":
                return {
                    "command": command,
                    "cwd": str(cwd),
                    "returncode": 0,
                    "stdout": json.dumps(
                        {
                            "artifacts": [
                                {"name": "resource-hunter-packaging-baseline-ubuntu-latest-py3.12"},
                                {"name": "resource-hunter-packaging-baseline-windows-latest-py3.13"},
                            ]
                        }
                    ),
                    "stderr": "",
                }
        if command[:2] == ["/fake/bin/gh", "api"]:
            return {
                "command": command,
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
        if command[:3] == ["/fake/bin/gh", "run", "download"]:
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
        pytest.fail(f"Unexpected command: {command}")

    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(packaging_gate, "_run_command", fake_run_command)

    payload = packaging_gate.evaluate_packaging_baseline_gate_from_github_run(
        "latest",
        repo="openclaw/resource-hunter",
        download_dir=download_dir,
        required_artifact_count=1,
    )

    assert payload["ok"] is True
    assert payload["download"]["run_id"] == "222222"
    assert payload["download"]["requested_run_id"] == "latest"
    assert payload["download"]["run_lookup"]["strategy"] == "artifact-discovery"
    attempts = payload["download"]["run_lookup"]["attempts"]
    assert len(attempts) == 1
    assert attempts[0]["workflow_filter_selected_run"]["id"] == "111111"
    assert attempts[0]["workflow_filter_selected_run"]["workflow_name"] == packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW
    assert attempts[0]["workflow_filter_selected_run_artifact_probe"]["artifact_names"] == ["docs-preview"]
    assert attempts[0]["artifact_discovery"]["selected_artifact_names"] == [
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        "resource-hunter-packaging-baseline-windows-latest-py3.13",
    ]
    assert attempts[0]["selected_run"]["id"] == "222222"
    assert attempts[0]["selected_run"]["workflow_name"] == "packaging-release"

    text = packaging_gate.format_packaging_baseline_gate_text(payload)
    assert "Selected run lookup strategy: artifact-discovery" in text
    assert "Selected run workflow: packaging-release" in text
    assert (
        f"Workflow-filter candidate run: 111111 ({packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW})" in text
    )
    assert "Workflow-filter candidate artifacts: docs-preview" in text

    assert commands == [
        [
            "/fake/bin/gh",
            "run",
            "list",
            "--workflow",
            packaging_gate.DEFAULT_GITHUB_RUN_WORKFLOW,
            "--limit",
            "20",
            "--json",
            "databaseId,status,conclusion,workflowName,headBranch,event,url,displayTitle",
            "--repo",
            "openclaw/resource-hunter",
        ],
        ["/fake/bin/gh", "api", "repos/openclaw/resource-hunter/actions/runs/111111/artifacts"],
        [
            "/fake/bin/gh",
            "run",
            "list",
            "--status",
            "completed",
            "--limit",
            "20",
            "--json",
            "databaseId,status,conclusion,workflowName,headBranch,event,url,displayTitle",
            "--repo",
            "openclaw/resource-hunter",
        ],
        ["/fake/bin/gh", "api", "repos/openclaw/resource-hunter/actions/runs/111111/artifacts"],
        ["/fake/bin/gh", "api", "repos/openclaw/resource-hunter/actions/runs/222222/artifacts"],
        [
            "/fake/bin/gh",
            "run",
            "download",
            "222222",
            "--repo",
            "openclaw/resource-hunter",
            "--dir",
            str(download_dir.resolve()),
            "--pattern",
            packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN,
        ],
    ]


def test_evaluate_packaging_baseline_gate_from_latest_run_missing_default_workflow_reports_discovery_summary(
    monkeypatch, tmp_path
):
    download_dir = tmp_path / "downloaded-gh-artifacts"

    def fake_run_command(args, *, cwd, timeout=300):
        command = list(args)
        if command[:3] == ["/fake/bin/gh", "run", "list"]:
            if "--workflow" in command:
                return {
                    "command": command,
                    "cwd": str(cwd),
                    "returncode": 1,
                    "stdout": "",
                    "stderr": "could not find any workflows named resource-hunter-ci in openclaw/resource-hunter\n",
                }
            return {
                "command": command,
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": json.dumps(
                    [
                        {
                            "databaseId": 111111,
                            "status": "completed",
                            "conclusion": "success",
                            "workflowName": "docs-ci",
                            "headBranch": "main",
                            "event": "push",
                            "url": "https://github.com/openclaw/resource-hunter/actions/runs/111111",
                            "displayTitle": "Docs",
                        },
                        {
                            "databaseId": 222222,
                            "status": "completed",
                            "conclusion": "success",
                            "workflowName": "packaging-release",
                            "headBranch": "main",
                            "event": "workflow_dispatch",
                            "url": "https://github.com/openclaw/resource-hunter/actions/runs/222222",
                            "displayTitle": "Packaging baseline",
                        },
                    ]
                ),
                "stderr": "",
            }
        if command[:2] == ["/fake/bin/gh", "api"]:
            if command[2] == "repos/openclaw/resource-hunter/actions/runs/111111/artifacts":
                return {
                    "command": command,
                    "cwd": str(cwd),
                    "returncode": 0,
                    "stdout": json.dumps({"artifacts": [{"name": "docs-preview"}]}),
                    "stderr": "",
                }
            if command[2] == "repos/openclaw/resource-hunter/actions/runs/222222/artifacts":
                return {
                    "command": command,
                    "cwd": str(cwd),
                    "returncode": 0,
                    "stdout": json.dumps({"artifacts": [{"name": "packaging-evidence"}]}),
                    "stderr": "",
                }
        pytest.fail(f"Unexpected command: {command}")

    monkeypatch.setattr(packaging_gate.shutil, "which", lambda name: "/fake/bin/gh" if name == "gh" else None)
    monkeypatch.setattr(packaging_gate, "_run_command", fake_run_command)

    with pytest.raises(packaging_gate.PackagingBaselineGateError) as excinfo:
        packaging_gate.evaluate_packaging_baseline_gate_from_github_run(
            "latest",
            repo="openclaw/resource-hunter",
            download_dir=download_dir,
        )

    message = str(excinfo.value)
    assert "GitHub Actions run lookup failed for openclaw/resource-hunter latest resource-hunter-ci run" in message
    assert (
        "Artifact discovery scanned 2 completed run(s) in openclaw/resource-hunter and saw workflows: "
        "docs-ci, packaging-release."
    ) in message
    assert "Recent artifact names: docs-preview, packaging-evidence." in message

    download_payload = excinfo.value.download_payload
    artifact_discovery = download_payload["run_lookup"]["attempts"][0]["artifact_discovery"]
    assert artifact_discovery["workflow_names"] == ["docs-ci", "packaging-release"]
    assert artifact_discovery["artifact_name_samples"] == ["docs-preview", "packaging-evidence"]

    error_payload = packaging_gate.build_packaging_baseline_gate_error_payload(
        message,
        download_payload=download_payload,
    )
    text = packaging_gate.format_packaging_baseline_gate_text(error_payload)
    assert "Artifact discovery repo: openclaw/resource-hunter" in text
    assert "Artifact discovery scanned runs: 2" in text
    assert "Artifact discovery workflows: docs-ci, packaging-release" in text
    assert "Artifact discovery artifact samples: docs-preview, packaging-evidence" in text
