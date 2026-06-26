from __future__ import annotations

import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

import resource_hunter.config as config
from resource_hunter import packaging_report, packaging_smoke
from resource_hunter.cache import ResourceCache
from resource_hunter.cli import _doctor_advice, _packaging_status
from resource_hunter.config import default_download_dir, storage_root
from resource_hunter.precision_core import AliasResolver


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def _runtime_cli_env() -> dict[str, str]:
    env = os.environ.copy()
    pythonpath = [str(SRC)]
    existing_pythonpath = env.get("PYTHONPATH")
    if existing_pythonpath:
        pythonpath.append(existing_pythonpath)
    env["PYTHONPATH"] = os.pathsep.join(pythonpath)
    env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def _run_runtime_cli(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "resource_hunter", *args],
        cwd=str(cwd or ROOT),
        env=_runtime_cli_env(),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
    )


def _run_source_checkout_script(script_name: str, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script_name), *args],
        cwd=str(cwd or ROOT),
        env=_runtime_cli_env(),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
    )


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


def test_resource_hunter_home_override(monkeypatch, tmp_path):
    home = tmp_path / "rh-home"
    monkeypatch.setenv("RESOURCE_HUNTER_HOME", str(home))
    monkeypatch.delenv("OPENCLAW_WORKSPACE", raising=False)
    assert storage_root() == home / "storage" / "resource-hunter"
    assert default_download_dir() == home / "downloads"


def test_openclaw_workspace_linked_storage_is_resolved(monkeypatch, tmp_path):
    workspace = tmp_path / "workspace"
    target = tmp_path / "external-storage"
    storage = workspace / "storage"
    workspace.mkdir()
    storage.mkdir()
    target.mkdir()

    original_resolve = Path.resolve

    def fake_resolve(self, strict=False):
        if self == storage:
            return target
        return original_resolve(self, strict=strict)

    monkeypatch.setattr(config, "_is_linked_storage_dir", lambda path: path == storage)
    monkeypatch.setattr(Path, "resolve", fake_resolve)
    monkeypatch.delenv("RESOURCE_HUNTER_HOME", raising=False)
    monkeypatch.setenv("OPENCLAW_WORKSPACE", str(workspace))

    assert storage_root() == target / "resource-hunter"
    assert default_download_dir() == target / "downloads"


def test_openclaw_workspace_storage_symlink_is_supported(monkeypatch, tmp_path):
    workspace = tmp_path / "workspace"
    target = tmp_path / "external-storage"
    storage = workspace / "storage"
    workspace.mkdir()
    target.mkdir()
    try:
        storage.symlink_to(target, target_is_directory=True)
    except (NotImplementedError, OSError, PermissionError) as exc:
        if os.name == "nt":
            pytest.skip(f"directory symlink privilege unavailable: {exc}")
        raise

    monkeypatch.delenv("RESOURCE_HUNTER_HOME", raising=False)
    monkeypatch.setenv("OPENCLAW_WORKSPACE", str(workspace))
    assert storage_root() == target / "resource-hunter"
    assert default_download_dir() == target / "downloads"


def test_cache_connection_enables_wal_and_busy_timeout(tmp_path):
    cache = ResourceCache(tmp_path / "cache.db")
    with cache._connect() as conn:
        journal_mode = conn.execute("pragma journal_mode").fetchone()[0]
        busy_timeout = conn.execute("pragma busy_timeout").fetchone()[0]
    assert str(journal_mode).lower() == "wal"
    assert int(busy_timeout) == 3000


def test_alias_extractor_recovers_non_chinese_title_from_metadata_text():
    resolver = AliasResolver()
    texts = [
        "赤橙黄绿青蓝紫（1982年姜树森执导的电影）_百度百科",
        "《赤橙黄绿青蓝紫》（Three-Dimensional People）是长春电影制片厂摄制的剧情片。",
    ]
    english, romanized, alternates = resolver._extract_aliases_from_texts(texts, "1982", original_title="赤橙黄绿青蓝紫")
    assert english == "Three-Dimensional People"
    assert romanized == ""
    assert "Three-Dimensional People" in alternates


def test_packaging_status_detects_missing_components(monkeypatch):
    def fake_find_spec(name):
        if name == "pip":
            return object()
        if name == "venv":
            return None
        if name == "setuptools.build_meta":
            raise ModuleNotFoundError(name)
        if name == "wheel":
            return None
        return None

    monkeypatch.setattr("resource_hunter.packaging_smoke.importlib.util.find_spec", fake_find_spec)

    status = _packaging_status()

    assert status == {
        "pip": True,
        "venv": False,
        "setuptools_build_meta": False,
        "wheel": False,
        "wheel_build_ready": False,
        "python_module_smoke_ready": False,
        "console_script_smoke_ready": False,
        "full_packaging_smoke_ready": False,
        "blockers": ["setuptools.build_meta", "wheel"],
        "optional_gaps": ["venv"],
        "console_script_strategy": "blocked",
    }


def test_packaging_status_requires_pip_for_wheel_build(monkeypatch):
    def fake_find_spec(name):
        if name == "pip":
            return None
        if name == "venv":
            return object()
        if name == "setuptools.build_meta":
            return object()
        if name == "wheel":
            return object()
        return None

    monkeypatch.setattr("resource_hunter.packaging_smoke.importlib.util.find_spec", fake_find_spec)

    status = _packaging_status()

    assert status == {
        "pip": False,
        "venv": True,
        "setuptools_build_meta": True,
        "wheel": True,
        "wheel_build_ready": False,
        "python_module_smoke_ready": False,
        "console_script_smoke_ready": False,
        "full_packaging_smoke_ready": False,
        "blockers": ["pip"],
        "optional_gaps": [],
        "console_script_strategy": "blocked",
    }


def test_packaging_status_requires_wheel_for_wheel_build(monkeypatch):
    def fake_find_spec(name):
        if name == "pip":
            return object()
        if name == "venv":
            return object()
        if name == "setuptools.build_meta":
            return object()
        if name == "wheel":
            return None
        return None

    monkeypatch.setattr("resource_hunter.packaging_smoke.importlib.util.find_spec", fake_find_spec)

    status = _packaging_status()

    assert status == {
        "pip": True,
        "venv": True,
        "setuptools_build_meta": True,
        "wheel": False,
        "wheel_build_ready": False,
        "python_module_smoke_ready": False,
        "console_script_smoke_ready": False,
        "full_packaging_smoke_ready": False,
        "blockers": ["wheel"],
        "optional_gaps": [],
        "console_script_strategy": "blocked",
    }


def test_packaging_status_allows_console_smoke_without_venv(monkeypatch):
    def fake_find_spec(name):
        if name == "pip":
            return object()
        if name == "venv":
            return None
        if name == "setuptools.build_meta":
            return object()
        if name == "wheel":
            return object()
        return None

    monkeypatch.setattr("resource_hunter.packaging_smoke.importlib.util.find_spec", fake_find_spec)

    status = _packaging_status()

    assert status == {
        "pip": True,
        "venv": False,
        "setuptools_build_meta": True,
        "wheel": True,
        "wheel_build_ready": True,
        "python_module_smoke_ready": True,
        "console_script_smoke_ready": True,
        "full_packaging_smoke_ready": True,
        "blockers": [],
        "optional_gaps": ["venv"],
        "console_script_strategy": "prefix-install",
    }


def test_packaging_status_prefers_venv_strategy_when_available(monkeypatch):
    def fake_find_spec(name):
        if name in {"pip", "venv", "setuptools.build_meta", "wheel"}:
            return object()
        return None

    monkeypatch.setattr("resource_hunter.packaging_smoke.importlib.util.find_spec", fake_find_spec)

    status = _packaging_status()

    assert status == {
        "pip": True,
        "venv": True,
        "setuptools_build_meta": True,
        "wheel": True,
        "wheel_build_ready": True,
        "python_module_smoke_ready": True,
        "console_script_smoke_ready": True,
        "full_packaging_smoke_ready": True,
        "blockers": [],
        "optional_gaps": [],
        "console_script_strategy": "venv",
    }


def test_doctor_advice_includes_missing_binary_and_permission_guidance(tmp_path):
    payload = {
        "cache_db": str(tmp_path / "cache.db"),
        "storage_root": str(tmp_path),
        "binaries": {"yt_dlp": None, "ffmpeg": None},
        "packaging": {
            "pip": True,
            "venv": False,
            "setuptools_build_meta": False,
            "wheel": False,
            "wheel_build_ready": False,
            "python_module_smoke_ready": False,
            "console_script_smoke_ready": False,
            "full_packaging_smoke_ready": False,
            "blockers": ["setuptools.build_meta", "wheel"],
            "optional_gaps": ["venv"],
            "console_script_strategy": "blocked",
        },
        "recent_sources": {
            "sources": [
                {"recent_status": {"ok": False, "degraded": True}},
                {"recent_status": {"ok": False, "degraded": True}},
            ]
        },
    }
    advice = _doctor_advice(payload)
    assert any("yt-dlp" in item for item in advice)
    assert any("ffmpeg" in item for item in advice)
    assert any("setuptools.build_meta" in item for item in advice)
    assert any("wheel" in item for item in advice)
    assert any("bootstrap-build-deps" in item for item in advice)
    assert any("degraded" in item.lower() for item in advice)


def test_doctor_advice_mentions_prefix_fallback_when_venv_missing(tmp_path):
    payload = {
        "cache_db": str(tmp_path / "cache.db"),
        "storage_root": str(tmp_path),
        "binaries": {"yt_dlp": "/bin/yt-dlp", "ffmpeg": "/bin/ffmpeg"},
        "packaging": {
            "pip": True,
            "venv": False,
            "setuptools_build_meta": True,
            "wheel": True,
            "wheel_build_ready": True,
            "python_module_smoke_ready": True,
            "console_script_smoke_ready": True,
            "full_packaging_smoke_ready": True,
            "blockers": [],
            "optional_gaps": ["venv"],
            "console_script_strategy": "prefix-install",
        },
        "recent_sources": {"sources": []},
    }

    advice = _doctor_advice(payload)

    assert any("venv" in item and "prefix" in item for item in advice)


def test_doctor_advice_mentions_selected_packaging_python(tmp_path):
    payload = {
        "python": "/usr/bin/current-python",
        "packaging_python": "/tmp/packaging-python",
        "packaging_python_source": "environment",
        "cache_db": str(tmp_path / "cache.db"),
        "storage_root": str(tmp_path),
        "binaries": {"yt_dlp": "/bin/yt-dlp", "ffmpeg": "/bin/ffmpeg"},
        "packaging": {
            "pip": True,
            "venv": True,
            "setuptools_build_meta": True,
            "wheel": False,
            "wheel_build_ready": False,
            "python_module_smoke_ready": False,
            "console_script_smoke_ready": False,
            "full_packaging_smoke_ready": False,
            "blockers": ["wheel"],
            "optional_gaps": [],
            "console_script_strategy": "blocked",
        },
        "recent_sources": {"sources": []},
    }

    advice = _doctor_advice(payload)

    assert any("Selected packaging Python (/tmp/packaging-python) lacks the `wheel` package" in item for item in advice)


def test_select_packaging_python_returns_first_ready_candidate(monkeypatch):
    candidates = [
        ("current", "/python/current"),
        ("path:python", "/python/ready"),
        ("py-launcher", "/python/other-ready"),
    ]
    statuses = {
        "/python/current": {
            "full_packaging_smoke_ready": False,
            "blockers": ["wheel"],
            "optional_gaps": [],
        },
        "/python/ready": {
            "full_packaging_smoke_ready": True,
            "blockers": [],
            "optional_gaps": ["venv"],
        },
        "/python/other-ready": {
            "full_packaging_smoke_ready": True,
            "blockers": [],
            "optional_gaps": [],
        },
    }

    monkeypatch.setattr(packaging_smoke, "_packaging_python_candidates", lambda: candidates)
    monkeypatch.setattr(packaging_smoke, "packaging_status", lambda python_executable=None: statuses[python_executable])

    selected, discovered = packaging_smoke.select_packaging_python()

    assert selected == "/python/ready"
    assert [candidate["python"] for candidate in discovered] == [candidate[1] for candidate in candidates]
    assert discovered[0]["ready"] is False
    assert discovered[1]["ready"] is True


def test_packaging_python_candidates_skip_windows_store_aliases(monkeypatch):
    current_python = r"E:\Python\python.exe"
    windows_store_alias = r"C:\Users\30582\AppData\Local\Microsoft\WindowsApps\python.EXE"
    other_windows_store_alias = r"C:\Users\30582\AppData\Local\Microsoft\WindowsApps\python3.EXE"
    path_python3 = r"E:\DevTools\bin\python3.CMD"
    launcher_python = r"E:\Python312\python.exe"

    def fake_which(command):
        return {
            "python": windows_store_alias,
            "python3": path_python3,
        }.get(command)

    monkeypatch.setattr(packaging_smoke.sys, "executable", current_python)
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    monkeypatch.delenv("CONDA_PREFIX", raising=False)
    monkeypatch.setattr(packaging_smoke.shutil, "which", fake_which)
    monkeypatch.setattr(packaging_smoke, "_py_launcher_candidates", lambda: [other_windows_store_alias, launcher_python])

    candidates = packaging_smoke._packaging_python_candidates()

    assert candidates == [
        ("current", current_python),
        ("path:python3", path_python3),
        ("py-launcher", launcher_python),
    ]


def test_packaging_status_probes_external_python_via_temp_script(monkeypatch, tmp_path):
    recorded = {}

    def fake_run_command(args, *, cwd, env=None, timeout=180):
        recorded["args"] = args
        recorded["cwd"] = cwd
        probe_script = Path(args[1])
        recorded["probe_script"] = probe_script
        recorded["probe_script_text"] = probe_script.read_text(encoding="utf-8")
        return {
            "command": args,
            "cwd": str(cwd),
            "returncode": 0,
            "stdout": json.dumps(
                {
                    "pip": True,
                    "venv": True,
                    "setuptools.build_meta": True,
                    "wheel": True,
                }
            ),
            "stderr": "",
        }

    monkeypatch.setattr(packaging_smoke, "_run_command", fake_run_command)

    status = packaging_smoke.packaging_status(python_executable=str(tmp_path / "python3.cmd"))

    assert recorded["args"][0] == str(tmp_path / "python3.cmd")
    assert recorded["args"][1] != "-c"
    assert recorded["probe_script"].name == "probe_packaging_modules.py"
    assert recorded["probe_script_text"] == packaging_smoke._MODULE_PROBE_SCRIPT
    assert status == {
        "pip": True,
        "venv": True,
        "setuptools_build_meta": True,
        "wheel": True,
        "wheel_build_ready": True,
        "python_module_smoke_ready": True,
        "console_script_smoke_ready": True,
        "full_packaging_smoke_ready": True,
        "blockers": [],
        "optional_gaps": [],
        "console_script_strategy": "venv",
    }


def test_packaging_status_probes_external_python_with_hosted_setuptools_assertion(monkeypatch, tmp_path):
    injected_modules = tmp_path / "injected-modules"
    setuptools_dir = injected_modules / "setuptools"
    setuptools_dir.mkdir(parents=True)
    (setuptools_dir / "__init__.py").write_text(
        "raise AssertionError('hosted setuptools distutils override failed')\n",
        encoding="utf-8",
    )
    (injected_modules / "wheel.py").write_text("# probe fallback\n", encoding="utf-8")
    setuptools_dist_info = injected_modules / "setuptools-999.dist-info"
    setuptools_dist_info.mkdir()
    (setuptools_dist_info / "METADATA").write_text(
        "Metadata-Version: 2.1\nName: setuptools\nVersion: 999\n",
        encoding="utf-8",
    )

    def fake_run_command(args, *, cwd, env=None, timeout=180):
        command_env = packaging_smoke._clean_env()
        command_env["PYTHONPATH"] = str(injected_modules)
        result = subprocess.run(
            args,
            cwd=str(cwd),
            env=command_env,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "command": args,
            "cwd": str(cwd),
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    monkeypatch.setattr(packaging_smoke, "_same_python", lambda _: False)
    monkeypatch.setattr(packaging_smoke, "_run_command", fake_run_command)

    status = packaging_smoke.packaging_status(python_executable=sys.executable)

    assert status["pip"] is True
    assert status["setuptools_build_meta"] is True
    assert status["wheel"] is True
    assert status["full_packaging_smoke_ready"] is True
    assert status["console_script_strategy"] in {"venv", "prefix-install"}
    assert "error" not in status


def test_doctor_advice_mentions_auto_discovery_failure(tmp_path):
    payload = {
        "python": "/usr/bin/current-python",
        "packaging_python": "/usr/bin/current-python",
        "packaging_python_source": "auto",
        "packaging_python_auto_selected": False,
        "packaging_python_candidates": [
            {
                "python": "/usr/bin/current-python",
                "source": "current",
                "ready": False,
                "packaging": {
                    "blockers": ["setuptools.build_meta", "wheel"],
                    "optional_gaps": ["venv"],
                },
            }
        ],
        "cache_db": str(tmp_path / "cache.db"),
        "storage_root": str(tmp_path),
        "binaries": {"yt_dlp": "/bin/yt-dlp", "ffmpeg": "/bin/ffmpeg"},
        "packaging": {
            "pip": True,
            "venv": False,
            "setuptools_build_meta": False,
            "wheel": False,
            "wheel_build_ready": False,
            "python_module_smoke_ready": False,
            "console_script_smoke_ready": False,
            "full_packaging_smoke_ready": False,
            "blockers": ["setuptools.build_meta", "wheel"],
            "optional_gaps": ["venv"],
            "console_script_strategy": "blocked",
        },
        "recent_sources": {"sources": []},
    }

    advice = _doctor_advice(payload)

    assert any("Auto-discovery did not find a packaging-ready interpreter" in item for item in advice)


def test_doctor_json_bad_packaging_python_reports_probe_error_subprocess(tmp_path):
    missing_python = tmp_path / "missing-python" / ("python.exe" if os.name == "nt" else "python")

    result = _run_runtime_cli("doctor", "--json", "--python", str(missing_python))

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["packaging_python"] == str(missing_python)
    assert payload["packaging_python_source"] == "argument"
    assert payload["project_root_source"] == "discovered"
    assert payload["packaging"]["console_script_strategy"] == "blocked"
    assert payload["packaging"]["error"].startswith(
        f"Unable to inspect packaging modules via {missing_python}:"
    )
    assert any("Check the interpreter path" in item for item in payload["advice"])


def test_packaging_smoke_json_bad_packaging_python_reports_failed_step_subprocess(tmp_path):
    missing_python = tmp_path / "missing-python" / ("python.exe" if os.name == "nt" else "python")

    result = _run_runtime_cli("packaging-smoke", "--json", "--python", str(missing_python))

    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["strategy"] == "blocked"
    assert payload["failed_step"] == "packaging-status"
    assert payload["packaging_python"] == str(missing_python)
    assert payload["packaging_python_source"] == "argument"
    assert payload["packaging"]["error"].startswith(
        f"Unable to inspect packaging modules via {missing_python}:"
    )
    assert payload["reason"].startswith("Packaging smoke is blocked: Unable to inspect packaging modules via")
    assert "Packaging smoke is blocked:" in result.stderr


def test_packaging_capture_json_bad_packaging_python_emits_bundle_subprocess(tmp_path):
    missing_python = tmp_path / "missing-python" / ("python.exe" if os.name == "nt" else "python")

    result = _run_runtime_cli("packaging-capture", "--json", "--python", str(missing_python))

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    payload = json.loads(result.stdout)
    assert payload["packaging_python"] == str(missing_python)
    assert payload["packaging_python_source"] == "argument"
    assert payload["project_root_source"] == "discovered"
    assert payload["failed_step"] == "packaging-status"
    assert payload["summary"]["packaging_smoke_ok"] is False
    assert payload["summary"]["reason"].startswith(
        "Packaging smoke is blocked: Unable to inspect packaging modules via"
    )
    assert payload["doctor"]["packaging"]["error"].startswith(
        f"Unable to inspect packaging modules via {missing_python}:"
    )
    assert payload["packaging_smoke"]["failed_step"] == "packaging-status"


def test_packaging_gate_script_reports_downloaded_artifact_drift_subprocess(tmp_path):
    artifact_root = tmp_path / "downloaded-gh-artifacts"
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

    result = _run_source_checkout_script("packaging_gate.py", "--json", str(artifact_root))

    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert payload == {
        "gate_schema_version": 1,
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
    assert (
        f"{drift_path.resolve()}: Packaging baseline requirement failed: Blocked capture did not report failed_step."
        in result.stderr
    )


def test_packaging_report_script_reports_downloaded_artifact_drift_subprocess(tmp_path):
    artifact_root = tmp_path / "downloaded-gh-artifacts"
    _write_packaging_baseline_artifact(
        artifact_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        baseline_contract_ok=True,
    )
    _write_packaging_baseline_artifact(
        artifact_root,
        "resource-hunter-packaging-baseline-windows-latest-py3.13",
        baseline_contract_ok=False,
    )

    result = _run_source_checkout_script("packaging_report.py", "--json", "--require-contract-ok", str(artifact_root))

    expected_payload = packaging_report.read_packaging_baseline_reports([artifact_root])
    expected_failures = packaging_report.packaging_baseline_report_requirement_failures(expected_payload)
    assert result.returncode == 2
    assert json.loads(result.stdout) == expected_payload
    for failure in expected_failures:
        assert failure in result.stderr


def test_packaging_gate_script_reports_downloaded_zip_directory_drift_subprocess(tmp_path):
    downloads_root = tmp_path / "downloaded-gh-artifact-zips"
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
    archive_path = downloads_root / "nested" / "downloaded-gh-artifacts.zip"
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr(
            "job-a/packaging-baseline.json",
            ok_path.read_text(encoding="utf-8"),
        )
        archive.writestr(
            "job-b/packaging-baseline.json",
            drift_path.read_text(encoding="utf-8"),
        )

    result = _run_source_checkout_script("packaging_gate.py", "--json", str(downloads_root))

    assert result.returncode == 2
    payload = json.loads(result.stdout)
    drift_ref = f"{archive_path.resolve()}!/job-b/packaging-baseline.json"
    assert payload == {
        "gate_schema_version": 1,
        "ok": False,
        "failure_count": 1,
        "failures": [
            f"{drift_ref}: Packaging baseline requirement failed: Blocked capture did not report failed_step."
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
        "artifacts_with_contract_drift": [drift_ref],
        "artifacts_with_requirement_failures": [drift_ref],
    }
    assert (
        f"{drift_ref}: Packaging baseline requirement failed: Blocked capture did not report failed_step."
        in result.stderr
    )


def test_packaging_gate_script_emits_json_error_payload_when_github_run_downloads_no_artifacts_subprocess(
    tmp_path, monkeypatch
):
    fake_bin = tmp_path / "fake-gh-bin"
    fake_bin.mkdir()
    invocation_log = tmp_path / "fake-gh-invocation.json"
    fake_gh_impl = fake_bin / "fake_gh.py"
    fake_gh_impl.write_text(
        "import json\n"
        "import sys\n"
        "from pathlib import Path\n\n"
        f"INVOCATION_LOG = Path(r'''{invocation_log}''')\n\n"
        "def main() -> int:\n"
        "    args = sys.argv[1:]\n"
        "    INVOCATION_LOG.write_text(json.dumps(args), encoding='utf-8')\n"
        "    if args[:2] != ['run', 'download']:\n"
        "        print(f'unexpected gh invocation: {args}', file=sys.stderr)\n"
        "        return 1\n"
        "    try:\n"
        "        download_dir = Path(args[args.index('--dir') + 1])\n"
        "    except (ValueError, IndexError):\n"
        "        print('--dir is required', file=sys.stderr)\n"
        "        return 1\n"
        "    download_dir.mkdir(parents=True, exist_ok=True)\n"
        "    return 0\n\n"
        "if __name__ == '__main__':\n"
        "    raise SystemExit(main())\n",
        encoding="utf-8",
    )
    if os.name == "nt":
        fake_gh = fake_bin / "gh.cmd"
        fake_gh.write_text(
            f'@echo off\r\n"{sys.executable}" "{fake_gh_impl}" %*\r\n',
            encoding="utf-8",
        )
    else:
        fake_gh = fake_bin / "gh"
        fake_gh.write_text(
            f'#!/bin/sh\n"{sys.executable}" "{fake_gh_impl}" "$@"\n',
            encoding="utf-8",
        )
        fake_gh.chmod(0o755)

    original_path = os.environ.get("PATH", "")
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{original_path}")

    download_dir = tmp_path / "downloaded-gh-artifacts"
    result = _run_source_checkout_script(
        "packaging_gate.py",
        "--json",
        "--github-run",
        "123456",
        "--repo",
        "openclaw/resource-hunter",
        "--download-dir",
        str(download_dir),
        "--require-artifact-count",
        "2",
    )

    error = f"No packaging-baseline.json artifacts found under {download_dir.resolve()}."
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload == {
        "gate_schema_version": 1,
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
            "artifact_patterns": ["resource-hunter-packaging-baseline-*"],
            "artifact_filter_source": "default",
            "resolved_artifact_count": 0,
            "resolved_artifact_paths": [],
            "resolved_archive_member_count": 0,
            "resolved_filesystem_artifact_count": 0,
            "download_command": payload["download"]["download_command"],
        },
    }
    assert [part.lower() if isinstance(part, str) else part for part in payload["download"]["download_command"]] == [
        str(fake_gh.resolve()).lower(),
        "run",
        "download",
        "123456",
        "--repo",
        "openclaw/resource-hunter",
        "--dir",
        str(download_dir.resolve()).lower(),
        "--pattern",
        "resource-hunter-packaging-baseline-*",
    ]
    assert result.stderr.strip() == error
    assert json.loads(invocation_log.read_text(encoding="utf-8")) == [
        "run",
        "download",
        "123456",
        "--repo",
        "openclaw/resource-hunter",
        "--dir",
        str(download_dir.resolve()),
        "--pattern",
        "resource-hunter-packaging-baseline-*",
    ]


def test_packaging_report_script_reports_downloaded_zip_directory_drift_subprocess(tmp_path):
    downloads_root = tmp_path / "downloaded-gh-artifact-zips"
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
    archive_path = downloads_root / "nested" / "downloaded-gh-artifacts.zip"
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr(
            "job-a/packaging-baseline.json",
            ok_path.read_text(encoding="utf-8"),
        )
        archive.writestr(
            "job-b/packaging-baseline.json",
            drift_path.read_text(encoding="utf-8"),
        )

    result = _run_source_checkout_script("packaging_report.py", "--json", "--require-contract-ok", str(downloads_root))

    expected_payload = packaging_report.read_packaging_baseline_reports([downloads_root])
    expected_failures = packaging_report.packaging_baseline_report_requirement_failures(expected_payload)
    assert result.returncode == 2
    assert json.loads(result.stdout) == expected_payload
    for failure in expected_failures:
        assert failure in result.stderr


def test_packaging_gate_script_downloads_github_run_artifacts_subprocess(tmp_path, monkeypatch):
    seed_root = tmp_path / "seed-gh-artifacts"
    _write_packaging_baseline_artifact(
        seed_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        baseline_contract_ok=True,
    )
    _write_packaging_baseline_artifact(
        seed_root,
        "resource-hunter-packaging-baseline-windows-latest-py3.13",
        baseline_contract_ok=True,
    )
    fake_bin = tmp_path / "fake-gh-bin"
    fake_bin.mkdir()
    invocation_log = tmp_path / "fake-gh-invocation.json"
    fake_gh_impl = fake_bin / "fake_gh.py"
    fake_gh_impl.write_text(
        "import json\n"
        "import shutil\n"
        "import sys\n"
        "from pathlib import Path\n\n"
        f"SEED_ROOT = Path(r'''{seed_root}''')\n"
        f"INVOCATION_LOG = Path(r'''{invocation_log}''')\n\n"
        "def main() -> int:\n"
        "    args = sys.argv[1:]\n"
        "    INVOCATION_LOG.write_text(json.dumps(args), encoding='utf-8')\n"
        "    if args[:2] != ['run', 'download']:\n"
        "        print(f'unexpected gh invocation: {args}', file=sys.stderr)\n"
        "        return 1\n"
        "    try:\n"
        "        download_dir = Path(args[args.index('--dir') + 1])\n"
        "    except (ValueError, IndexError):\n"
        "        print('--dir is required', file=sys.stderr)\n"
        "        return 1\n"
        "    download_dir.mkdir(parents=True, exist_ok=True)\n"
        "    for child in SEED_ROOT.iterdir():\n"
        "        target = download_dir / child.name\n"
        "        if target.exists():\n"
        "            shutil.rmtree(target)\n"
        "        shutil.copytree(child, target)\n"
        "    return 0\n\n"
        "if __name__ == '__main__':\n"
        "    raise SystemExit(main())\n",
        encoding="utf-8",
    )
    if os.name == "nt":
        fake_gh = fake_bin / "gh.cmd"
        fake_gh.write_text(
            f'@echo off\r\n"{sys.executable}" "{fake_gh_impl}" %*\r\n',
            encoding="utf-8",
        )
    else:
        fake_gh = fake_bin / "gh"
        fake_gh.write_text(
            f'#!/bin/sh\n"{sys.executable}" "{fake_gh_impl}" "$@"\n',
            encoding="utf-8",
        )
        fake_gh.chmod(0o755)

    original_path = os.environ.get("PATH", "")
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{original_path}")

    download_dir = tmp_path / "downloaded-gh-artifacts"
    result = _run_source_checkout_script(
        "packaging_gate.py",
        "--json",
        "--github-run",
        "123456",
        "--repo",
        "openclaw/resource-hunter",
        "--download-dir",
        str(download_dir),
        "--require-artifact-count",
        "2",
    )

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
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
        "artifact_patterns": ["resource-hunter-packaging-baseline-*"],
        "artifact_filter_source": "default",
        "resolved_artifact_count": 2,
        "resolved_artifact_paths": [
            str((download_dir / "resource-hunter-packaging-baseline-ubuntu-latest-py3.12" / "packaging-baseline.json").resolve()),
            str((download_dir / "resource-hunter-packaging-baseline-windows-latest-py3.13" / "packaging-baseline.json").resolve()),
        ],
        "resolved_archive_member_count": 0,
        "resolved_filesystem_artifact_count": 2,
        "download_command": payload["download"]["download_command"],
    }
    assert [part.lower() if isinstance(part, str) else part for part in payload["download"]["download_command"]] == [
        str(fake_gh.resolve()).lower(),
        "run",
        "download",
        "123456",
        "--repo",
        "openclaw/resource-hunter",
        "--dir",
        str(download_dir.resolve()).lower(),
        "--pattern",
        "resource-hunter-packaging-baseline-*",
    ]
    assert json.loads(invocation_log.read_text(encoding="utf-8")) == [
        "run",
        "download",
        "123456",
        "--repo",
        "openclaw/resource-hunter",
        "--dir",
        str(download_dir.resolve()),
        "--pattern",
        "resource-hunter-packaging-baseline-*",
    ]


def test_packaging_report_script_downloads_github_run_artifacts_subprocess(tmp_path, monkeypatch):
    seed_root = tmp_path / "seed-gh-artifacts"
    _write_packaging_baseline_artifact(
        seed_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        baseline_contract_ok=True,
    )
    _write_packaging_baseline_artifact(
        seed_root,
        "resource-hunter-packaging-baseline-windows-latest-py3.13",
        baseline_contract_ok=False,
    )
    fake_bin = tmp_path / "fake-gh-bin"
    fake_bin.mkdir()
    invocation_log = tmp_path / "fake-gh-invocation.json"
    fake_gh_impl = fake_bin / "fake_gh.py"
    fake_gh_impl.write_text(
        "import json\n"
        "import shutil\n"
        "import sys\n"
        "from pathlib import Path\n\n"
        f"SEED_ROOT = Path(r'''{seed_root}''')\n"
        f"INVOCATION_LOG = Path(r'''{invocation_log}''')\n\n"
        "def main() -> int:\n"
        "    args = sys.argv[1:]\n"
        "    INVOCATION_LOG.write_text(json.dumps(args), encoding='utf-8')\n"
        "    if args[:2] != ['run', 'download']:\n"
        "        print(f'unexpected gh invocation: {args}', file=sys.stderr)\n"
        "        return 1\n"
        "    try:\n"
        "        download_dir = Path(args[args.index('--dir') + 1])\n"
        "    except (ValueError, IndexError):\n"
        "        print('--dir is required', file=sys.stderr)\n"
        "        return 1\n"
        "    download_dir.mkdir(parents=True, exist_ok=True)\n"
        "    for child in SEED_ROOT.iterdir():\n"
        "        target = download_dir / child.name\n"
        "        if target.exists():\n"
        "            shutil.rmtree(target)\n"
        "        shutil.copytree(child, target)\n"
        "    return 0\n\n"
        "if __name__ == '__main__':\n"
        "    raise SystemExit(main())\n",
        encoding="utf-8",
    )
    if os.name == "nt":
        fake_gh = fake_bin / "gh.cmd"
        fake_gh.write_text(
            f'@echo off\r\n"{sys.executable}" "{fake_gh_impl}" %*\r\n',
            encoding="utf-8",
        )
    else:
        fake_gh = fake_bin / "gh"
        fake_gh.write_text(
            f'#!/bin/sh\n"{sys.executable}" "{fake_gh_impl}" "$@"\n',
            encoding="utf-8",
        )
        fake_gh.chmod(0o755)

    original_path = os.environ.get("PATH", "")
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{original_path}")

    download_dir = tmp_path / "downloaded-gh-artifacts"
    result = _run_source_checkout_script(
        "packaging_report.py",
        "--json",
        "--github-run",
        "123456",
        "--repo",
        "openclaw/resource-hunter",
        "--download-dir",
        str(download_dir),
        "--require-contract-ok",
    )

    expected_payload = packaging_report.attach_packaging_baseline_download_payload(
        packaging_report.read_packaging_baseline_reports([download_dir]),
        download_payload={
            "provider": "github-actions",
            "run_id": "123456",
            "repo": "openclaw/resource-hunter",
            "download_dir": str(download_dir.resolve()),
            "download_dir_source": "argument",
            "download_dir_retained": True,
            "artifact_names": [],
            "artifact_patterns": ["resource-hunter-packaging-baseline-*"],
            "artifact_filter_source": "default",
            "resolved_artifact_count": 2,
            "resolved_artifact_paths": [
                str((download_dir / "resource-hunter-packaging-baseline-ubuntu-latest-py3.12" / "packaging-baseline.json").resolve()),
                str((download_dir / "resource-hunter-packaging-baseline-windows-latest-py3.13" / "packaging-baseline.json").resolve()),
            ],
            "resolved_archive_member_count": 0,
            "resolved_filesystem_artifact_count": 2,
            "download_command": [],
        },
    )
    expected_failures = packaging_report.packaging_baseline_report_requirement_failures(expected_payload)

    assert result.returncode == 2, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    expected_payload["download"]["download_command"] = payload["download"]["download_command"]
    assert payload == expected_payload
    assert [part.lower() if isinstance(part, str) else part for part in payload["download"]["download_command"]] == [
        str(fake_gh.resolve()).lower(),
        "run",
        "download",
        "123456",
        "--repo",
        "openclaw/resource-hunter",
        "--dir",
        str(download_dir.resolve()).lower(),
        "--pattern",
        "resource-hunter-packaging-baseline-*",
    ]
    for failure in expected_failures:
        assert failure in result.stderr
    assert json.loads(invocation_log.read_text(encoding="utf-8")) == [
        "run",
        "download",
        "123456",
        "--repo",
        "openclaw/resource-hunter",
        "--dir",
        str(download_dir.resolve()),
        "--pattern",
        "resource-hunter-packaging-baseline-*",
    ]


@pytest.mark.parametrize(
    ("script_name", "script_args"),
    [
        ("packaging_verify.py", ()),
        ("hunt.py", ("packaging-baseline-verify",)),
    ],
)
def test_packaging_verify_entrypoints_download_github_run_artifacts_and_write_outputs_subprocess(
    tmp_path,
    monkeypatch,
    script_name,
    script_args,
):
    seed_root = tmp_path / "seed-gh-artifacts"
    _write_packaging_baseline_artifact(
        seed_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
        baseline_contract_ok=True,
    )
    _write_packaging_baseline_artifact(
        seed_root,
        "resource-hunter-packaging-baseline-windows-latest-py3.13",
        baseline_contract_ok=True,
    )
    fake_bin = tmp_path / "fake-gh-bin"
    fake_bin.mkdir()
    invocation_log = tmp_path / "fake-gh-invocation.json"
    fake_gh_impl = fake_bin / "fake_gh.py"
    fake_gh_impl.write_text(
        "import json\n"
        "import shutil\n"
        "import sys\n"
        "from pathlib import Path\n\n"
        f"SEED_ROOT = Path(r'''{seed_root}''')\n"
        f"INVOCATION_LOG = Path(r'''{invocation_log}''')\n\n"
        "def main() -> int:\n"
        "    args = sys.argv[1:]\n"
        "    INVOCATION_LOG.write_text(json.dumps(args), encoding='utf-8')\n"
        "    if args[:2] != ['run', 'download']:\n"
        "        print(f'unexpected gh invocation: {args}', file=sys.stderr)\n"
        "        return 1\n"
        "    try:\n"
        "        download_dir = Path(args[args.index('--dir') + 1])\n"
        "    except (ValueError, IndexError):\n"
        "        print('--dir is required', file=sys.stderr)\n"
        "        return 1\n"
        "    download_dir.mkdir(parents=True, exist_ok=True)\n"
        "    for child in SEED_ROOT.iterdir():\n"
        "        target = download_dir / child.name\n"
        "        if target.exists():\n"
        "            shutil.rmtree(target)\n"
        "        shutil.copytree(child, target)\n"
        "    return 0\n\n"
        "if __name__ == '__main__':\n"
        "    raise SystemExit(main())\n",
        encoding="utf-8",
    )
    if os.name == "nt":
        fake_gh = fake_bin / "gh.cmd"
        fake_gh.write_text(
            f'@echo off\r\n"{sys.executable}" "{fake_gh_impl}" %*\r\n',
            encoding="utf-8",
        )
    else:
        fake_gh = fake_bin / "gh"
        fake_gh.write_text(
            f'#!/bin/sh\n"{sys.executable}" "{fake_gh_impl}" "$@"\n',
            encoding="utf-8",
        )
        fake_gh.chmod(0o755)

    original_path = os.environ.get("PATH", "")
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{original_path}")

    output_dir = tmp_path / "verify-output"
    output_archive = tmp_path / "verify-bundle.zip"
    result = _run_source_checkout_script(
        script_name,
        *script_args,
        "--json",
        "--github-run",
        "123456",
        "--repo",
        "openclaw/resource-hunter",
        "--output-dir",
        str(output_dir),
        "--output-archive",
        str(output_archive),
        "--archive-downloads",
        "--require-artifact-count",
        "2",
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["report_ok"] is True
    assert payload["gate_ok"] is True
    assert payload["saved_outputs"] == {
        "report_json": str((output_dir / "report.json").resolve()),
        "report_text": str((output_dir / "report.txt").resolve()),
        "gate_json": str((output_dir / "gate.json").resolve()),
        "gate_text": str((output_dir / "gate.txt").resolve()),
        "verify_json": str((output_dir / "verify.json").resolve()),
        "verify_text": str((output_dir / "verify.txt").resolve()),
        "bundle_manifest": str((output_dir / "bundle-manifest.json").resolve()),
        "output_archive": str(output_archive.resolve()),
    }
    bundle_manifest = json.loads((output_dir / "bundle-manifest.json").read_text(encoding="utf-8"))
    assert bundle_manifest["download_bundle_member_count"] == 2
    assert bundle_manifest["download_bundle_members"] == [
        "download/resource-hunter-packaging-baseline-ubuntu-latest-py3.12/packaging-baseline.json",
        "download/resource-hunter-packaging-baseline-windows-latest-py3.13/packaging-baseline.json",
    ]
    with zipfile.ZipFile(output_archive) as archive:
        assert archive.namelist() == [
            "report.json",
            "report.txt",
            "gate.json",
            "gate.txt",
            "verify.json",
            "verify.txt",
            "bundle-manifest.json",
            "download/resource-hunter-packaging-baseline-ubuntu-latest-py3.12/packaging-baseline.json",
            "download/resource-hunter-packaging-baseline-windows-latest-py3.13/packaging-baseline.json",
        ]
    assert json.loads(invocation_log.read_text(encoding="utf-8")) == [
        "run",
        "download",
        "123456",
        "--repo",
        "openclaw/resource-hunter",
        "--dir",
        str((output_dir / "download").resolve()),
        "--pattern",
        "resource-hunter-packaging-baseline-*",
    ]

