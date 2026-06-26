from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import sysconfig
import zipfile
from pathlib import Path

import pytest

from resource_hunter import __version__
from resource_hunter import packaging_gate, packaging_report, packaging_smoke


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def _clean_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    return env


def _run_command(args: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd),
        env=env or _clean_env(),
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )


def _venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def _venv_console_script(venv_dir: Path, script_name: str) -> Path:
    scripts_dir = venv_dir / ("Scripts" if os.name == "nt" else "bin")
    candidates = [scripts_dir / script_name]
    if os.name == "nt":
        candidates.insert(0, scripts_dir / f"{script_name}.exe")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def _prefix_paths(prefix_dir: Path) -> tuple[Path, list[Path]]:
    vars_map = {
        "base": str(prefix_dir),
        "platbase": str(prefix_dir),
        "installed_base": str(prefix_dir),
        "installed_platbase": str(prefix_dir),
    }
    scripts_dir = Path(sysconfig.get_path("scripts", vars=vars_map))
    site_paths: list[Path] = []
    for key in ("purelib", "platlib"):
        site_path = Path(sysconfig.get_path(key, vars=vars_map))
        if site_path not in site_paths:
            site_paths.append(site_path)
    return scripts_dir, site_paths


def _prefix_console_script(prefix_dir: Path, script_name: str) -> Path:
    scripts_dir, _ = _prefix_paths(prefix_dir)
    candidates = [scripts_dir / script_name]
    if os.name == "nt":
        candidates.insert(0, scripts_dir / f"{script_name}.exe")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def _prefix_env(prefix_dir: Path) -> dict[str, str]:
    env = _clean_env()
    _, site_paths = _prefix_paths(prefix_dir)
    env["PYTHONPATH"] = os.pathsep.join(str(path) for path in site_paths)
    return env


def _supports_venv() -> bool:
    return importlib.util.find_spec("venv") is not None


def _supports_pip() -> bool:
    return importlib.util.find_spec("pip") is not None


def _supports_wheel_build() -> bool:
    return bool(packaging_smoke.packaging_status(python_executable=sys.executable).get("wheel_build_ready"))


def _write_packaging_baseline_artifact(
    root: Path,
    artifact_name: str,
    *,
    baseline_contract_ok: bool = True,
) -> Path:
    artifact_dir = root / artifact_name
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = artifact_dir / "packaging-baseline.json"
    blocked_python_name = "python.exe" if os.name == "nt" else "python"
    blocked_python = artifact_dir / "__blocked_python__" / blocked_python_name
    blocked_warning = "Blocked capture did not report failed_step."
    payload = {
        "schema_version": 1,
        "captured_at": "2026-03-23T00:00:00Z",
        "output_dir": str(artifact_dir),
        "project_root": str(ROOT),
        "project_root_source": "argument",
        "requested_project_root": str(ROOT),
        "blocked_python": str(blocked_python),
        "passing_capture": {
            "path": str(artifact_dir / "passing-packaging-capture.json"),
            "project_root": str(ROOT),
            "project_root_source": "argument",
            "requested_project_root": str(ROOT),
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
        "blocked_capture": {
            "path": str(artifact_dir / "blocked-packaging-capture.json"),
            "project_root": str(ROOT),
            "project_root_source": "argument",
            "requested_project_root": str(ROOT),
            "packaging_python": str(blocked_python),
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
        },
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


def _write_fake_gh_download_command(fake_bin: Path, *, seed_root: Path, invocation_log: Path) -> Path:
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
    return fake_gh


def test_find_project_root_walks_up(tmp_path):
    project_root = tmp_path / "repo"
    nested = project_root / "scripts" / "nested"
    (project_root / "src" / "resource_hunter").mkdir(parents=True)
    (project_root / "pyproject.toml").write_text("[project]\nname='resource-hunter'\n", encoding="utf-8")
    nested.mkdir(parents=True)

    assert packaging_smoke.find_project_root(nested) == project_root


def test_run_packaging_smoke_reports_missing_project_root(tmp_path):
    payload = packaging_smoke.run_packaging_smoke(project_root=tmp_path)

    assert payload["ok"] is False
    assert payload["packaging_python"] == sys.executable
    assert payload["packaging_python_source"] == "current"
    assert payload["project_root"] is None
    assert payload["project_root_source"] == "argument"
    assert payload["requested_project_root"] == str(tmp_path.resolve())
    assert payload["packaging"]["project_root"] is None
    assert payload["packaging"]["project_root_source"] == "argument"
    assert payload["packaging"]["requested_project_root"] == str(tmp_path.resolve())
    assert payload["steps"] == []
    assert "project root" in payload["reason"].lower()


def test_run_packaging_smoke_short_circuits_on_packaging_blockers(monkeypatch, tmp_path):
    project_root = tmp_path / "repo"
    (project_root / "src" / "resource_hunter").mkdir(parents=True)
    (project_root / "pyproject.toml").write_text("[project]\nname='resource-hunter'\n", encoding="utf-8")
    monkeypatch.setattr(
        packaging_smoke,
        "packaging_status",
        lambda python_executable=None: {
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
    )

    payload = packaging_smoke.run_packaging_smoke(project_root=project_root)

    assert payload["ok"] is False
    assert payload["strategy"] == "blocked"
    assert payload["strategy_family"] == "blocked"
    assert payload["failed_step"] == "packaging-gate"
    assert payload["steps"] == []
    assert payload["project_root_source"] == "argument"
    assert payload["requested_project_root"] == str(project_root)
    assert payload["packaging"]["project_root"] == str(project_root)
    assert payload["packaging"]["project_root_source"] == "argument"
    assert payload["packaging"]["requested_project_root"] == str(project_root)
    assert payload["packaging"]["blockers"] == ["setuptools.build_meta", "wheel"]
    assert "setuptools.build_meta" in payload["reason"]
    assert "wheel" in payload["reason"]


def test_annotate_project_packaging_status_records_project_root_without_bootstrap_metadata(tmp_path):
    project_root = tmp_path / "repo"
    (project_root / "src" / "resource_hunter").mkdir(parents=True)
    (project_root / "pyproject.toml").write_text("[project]\nname='resource-hunter'\n", encoding="utf-8")

    annotated = packaging_smoke.annotate_project_packaging_status(
        {
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
        project_root=project_root,
        include_bootstrap_metadata=False,
    )

    assert annotated["project_root"] == str(project_root)
    assert annotated["project_root_source"] == "argument"
    assert annotated["requested_project_root"] == str(project_root)
    assert "bootstrap_build_deps_ready" not in annotated
    assert "bootstrap_build_requirements" not in annotated
    assert "bootstrap_console_script_strategy" not in annotated
    assert "packaging_smoke_ready_with_bootstrap" not in annotated


def test_annotate_project_packaging_status_distinguishes_requested_and_resolved_project_root(tmp_path):
    project_root = tmp_path / "repo"
    nested = project_root / "ops" / "workspace"
    (project_root / "src" / "resource_hunter").mkdir(parents=True)
    (project_root / "pyproject.toml").write_text("[project]\nname='resource-hunter'\n", encoding="utf-8")
    nested.mkdir(parents=True)

    annotated = packaging_smoke.annotate_project_packaging_status(
        {
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
        },
        project_root=nested,
        include_bootstrap_metadata=False,
    )

    assert annotated["requested_project_root"] == str(nested)
    assert annotated["project_root"] == str(project_root)
    assert annotated["project_root_source"] == "argument"


def test_annotate_project_packaging_status_marks_discovered_root_source_when_project_root_omitted(tmp_path):
    project_root = tmp_path / "repo"
    (project_root / "src" / "resource_hunter").mkdir(parents=True)
    (project_root / "pyproject.toml").write_text("[project]\nname='resource-hunter'\n", encoding="utf-8")

    annotated = packaging_smoke.annotate_project_packaging_status(
        {
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
        },
        resolved_project_root=project_root,
        include_bootstrap_metadata=False,
    )

    assert annotated["project_root"] == str(project_root)
    assert annotated["project_root_source"] == "discovered"
    assert "requested_project_root" not in annotated


def test_run_packaging_smoke_bootstraps_missing_build_deps(monkeypatch, tmp_path):
    project_root = tmp_path / "repo"
    (project_root / "src" / "resource_hunter").mkdir(parents=True)
    (project_root / "pyproject.toml").write_text(
        "[build-system]\n"
        "requires=['setuptools>=69','wheel']\n"
        "build-backend='setuptools.build_meta'\n"
        "[project]\n"
        "name='resource-hunter'\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        packaging_smoke,
        "packaging_status",
        lambda python_executable=None: {
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
    )

    recorded: list[dict[str, object]] = []

    def fake_run_command(args, *, cwd, env=None, timeout=180):
        recorded.append({"args": args, "cwd": str(cwd), "env": env})
        if args[1:4] == ["-m", "pip", "install"] and "--target" in args:
            return {
                "command": args,
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": "bootstrapped",
                "stderr": "",
            }
        if args[1:4] == ["-m", "pip", "wheel"]:
            dist_dir = Path(args[args.index("--wheel-dir") + 1])
            (dist_dir / f"resource_hunter-{__version__}-py3-none-any.whl").write_text("wheel", encoding="utf-8")
            return {
                "command": args,
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": "built",
                "stderr": "",
            }
        if args[1:4] == ["-m", "pip", "install"] and "--prefix" in args:
            install_root = Path(args[args.index("--prefix") + 1])
            console_script = packaging_smoke._prefix_console_script(install_root, "resource-hunter")
            console_script.parent.mkdir(parents=True, exist_ok=True)
            console_script.write_text("", encoding="utf-8")
            return {
                "command": args,
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": "installed",
                "stderr": "",
            }
        if args[1:3] == ["-m", "resource_hunter"] and args[-1] == "--help":
            return {
                "command": args,
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": "usage: resource-hunter [-h]\n",
                "stderr": "",
            }
        if args[1:3] == ["-m", "resource_hunter"] and args[-1] == "--version":
            return {
                "command": args,
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": f"resource-hunter {__version__}",
                "stderr": "",
            }
        if args[-1] == "--help":
            return {
                "command": args,
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": "usage: resource-hunter [-h]\n",
                "stderr": "",
            }
        if args[-1] == "--version":
            return {
                "command": args,
                "cwd": str(cwd),
                "returncode": 0,
                "stdout": f"resource-hunter {__version__}",
                "stderr": "",
            }
        raise AssertionError(f"Unexpected command: {args}")

    monkeypatch.setattr(packaging_smoke, "_run_command", fake_run_command)

    payload = packaging_smoke.run_packaging_smoke(project_root=project_root, bootstrap_build_deps=True)

    assert payload["ok"] is True
    assert payload["strategy"] == "prefix-install"
    assert payload["strategy_family"] == "usable"
    assert payload["bootstrapped_build_requirements"] == ["setuptools>=69", "wheel"]
    assert payload["steps"][0]["name"] == "bootstrap-build-deps"
    build_step = next(step for step in payload["steps"] if step["name"] == "build-wheel")
    assert build_step["ok"] is True
    assert payload["bootstrap_overlay"] is not None
    build_call = next(item for item in recorded if item["args"][1:4] == ["-m", "pip", "wheel"])
    assert build_call["env"]["PYTHONPATH"] == payload["bootstrap_overlay"]


def test_packaging_status_probes_target_python(monkeypatch):
    recorded: list[list[str]] = []

    def fake_run_command(args, *, cwd, env=None, timeout=180):
        recorded.append(args)
        return {
            "command": args,
            "cwd": str(cwd),
            "returncode": 0,
            "stdout": json.dumps(
                {
                    "pip": True,
                    "venv": False,
                    "setuptools.build_meta": True,
                    "wheel": True,
                }
            ),
            "stderr": "",
        }

    monkeypatch.setattr(packaging_smoke, "_run_command", fake_run_command)

    status = packaging_smoke.packaging_status(python_executable="/tmp/alt-python")

    assert recorded and recorded[0][0] == "/tmp/alt-python"
    assert recorded[0][1] != "-c"
    assert Path(recorded[0][1]).name == "probe_packaging_modules.py"
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


def test_packaging_status_falls_back_to_subprocess_for_current_python_distutils_assertion(monkeypatch):
    recorded: list[list[str]] = []

    def fake_module_available(module_name: str) -> bool:
        if module_name == "setuptools.build_meta":
            raise AssertionError("stdlib distutils leaked into setuptools probe")
        return module_name != "venv"

    def fake_run_command(args, *, cwd, env=None, timeout=180):
        recorded.append(args)
        return {
            "command": args,
            "cwd": str(cwd),
            "returncode": 0,
            "stdout": json.dumps(
                {
                    "pip": True,
                    "venv": False,
                    "setuptools.build_meta": True,
                    "wheel": True,
                }
            ),
            "stderr": "",
        }

    monkeypatch.setattr(packaging_smoke, "module_available", fake_module_available)
    monkeypatch.setattr(packaging_smoke, "_run_command", fake_run_command)

    status = packaging_smoke.packaging_status()

    assert recorded and recorded[0][0] == sys.executable
    assert recorded[0][1] != "-c"
    assert Path(recorded[0][1]).name == "probe_packaging_modules.py"
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


def test_packaging_status_reports_probe_errors(monkeypatch):
    def fake_run_command(args, *, cwd, env=None, timeout=180):
        return {
            "command": args,
            "cwd": str(cwd),
            "returncode": 1,
            "stdout": "",
            "stderr": "python launcher failed",
        }

    monkeypatch.setattr(packaging_smoke, "_run_command", fake_run_command)

    status = packaging_smoke.packaging_status(python_executable="/tmp/missing-python")

    assert status == {
        "pip": None,
        "venv": None,
        "setuptools_build_meta": None,
        "wheel": None,
        "wheel_build_ready": False,
        "python_module_smoke_ready": False,
        "console_script_smoke_ready": False,
        "full_packaging_smoke_ready": False,
        "blockers": [],
        "optional_gaps": [],
        "console_script_strategy": "blocked",
        "error": "Unable to inspect packaging modules via /tmp/missing-python: python launcher failed",
    }


def test_select_packaging_python_accepts_bootstrap_capable_candidates(monkeypatch, tmp_path):
    project_root = tmp_path / "repo"
    (project_root / "src" / "resource_hunter").mkdir(parents=True)
    (project_root / "pyproject.toml").write_text(
        "[build-system]\nrequires=['setuptools>=69','wheel']\nbuild-backend='setuptools.build_meta'\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        packaging_smoke,
        "_packaging_python_candidates",
        lambda: [("current", "/tmp/current-python"), ("path:python", "/tmp/bootstrap-python")],
    )

    def fake_packaging_status(*, python_executable=None):
        if python_executable == "/tmp/bootstrap-python":
            return {
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
        return {
            "pip": False,
            "venv": False,
            "setuptools_build_meta": False,
            "wheel": False,
            "wheel_build_ready": False,
            "python_module_smoke_ready": False,
            "console_script_smoke_ready": False,
            "full_packaging_smoke_ready": False,
            "blockers": ["pip", "setuptools.build_meta", "wheel"],
            "optional_gaps": ["venv"],
            "console_script_strategy": "blocked",
        }

    monkeypatch.setattr(packaging_smoke, "packaging_status", fake_packaging_status)

    python_executable, candidates = packaging_smoke.select_packaging_python(
        project_root=project_root,
        allow_bootstrap_build_deps=True,
    )

    assert python_executable == "/tmp/bootstrap-python"
    assert candidates[0]["ready"] is False
    assert candidates[1]["ready"] is True
    assert candidates[1]["bootstrap_ready"] is True
    assert candidates[1]["packaging"]["project_root"] == str(project_root)
    assert candidates[1]["packaging"]["project_root_source"] == "argument"
    assert candidates[1]["packaging"]["bootstrap_build_deps_ready"] is True
    assert candidates[1]["packaging"]["bootstrap_build_requirements"] == ["setuptools>=69", "wheel"]
    assert candidates[1]["packaging"]["packaging_smoke_ready_with_bootstrap"] is True


def test_run_packaging_smoke_checks_target_python_status(monkeypatch, tmp_path):
    project_root = tmp_path / "repo"
    (project_root / "src" / "resource_hunter").mkdir(parents=True)
    (project_root / "pyproject.toml").write_text("[project]\nname='resource-hunter'\n", encoding="utf-8")
    recorded: list[str | None] = []

    def fake_packaging_status(*, python_executable=None):
        recorded.append(python_executable)
        return {
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

    monkeypatch.setattr(packaging_smoke, "packaging_status", fake_packaging_status)

    payload = packaging_smoke.run_packaging_smoke(project_root=project_root, python_executable="/tmp/alt-python")

    assert recorded == ["/tmp/alt-python"]
    assert payload["ok"] is False
    assert payload["packaging_python"] == "/tmp/alt-python"
    assert payload["packaging_python_source"] == "argument"
    assert payload["project_root_source"] == "argument"
    assert payload["strategy"] == "blocked"


def test_run_packaging_smoke_accepts_packaging_python_provenance(monkeypatch, tmp_path):
    project_root = tmp_path / "repo"
    (project_root / "src" / "resource_hunter").mkdir(parents=True)
    (project_root / "pyproject.toml").write_text("[project]\nname='resource-hunter'\n", encoding="utf-8")
    candidates = [
        {
            "python": "/tmp/ready-python",
            "source": "path:python",
            "ready": True,
            "packaging": {
                "blockers": [],
                "optional_gaps": [],
                "console_script_strategy": "venv",
            },
        }
    ]
    monkeypatch.setattr(
        packaging_smoke,
        "packaging_status",
        lambda python_executable=None: {
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
    )

    payload = packaging_smoke.run_packaging_smoke(
        project_root=project_root,
        python_executable="/tmp/ready-python",
        packaging_python_source="auto",
        packaging_python_candidates=candidates,
        packaging_python_auto_selected=True,
    )

    assert payload["ok"] is False
    assert payload["packaging_python"] == "/tmp/ready-python"
    assert payload["packaging_python_source"] == "auto"
    assert payload["project_root_source"] == "argument"
    assert payload["packaging_python_candidates"] == candidates
    assert payload["packaging_python_auto_selected"] is True


def test_run_packaging_smoke_short_circuits_on_packaging_probe_error(monkeypatch, tmp_path):
    project_root = tmp_path / "repo"
    (project_root / "src" / "resource_hunter").mkdir(parents=True)
    (project_root / "pyproject.toml").write_text("[project]\nname='resource-hunter'\n", encoding="utf-8")
    monkeypatch.setattr(
        packaging_smoke,
        "packaging_status",
        lambda python_executable=None: {
            "pip": None,
            "venv": None,
            "setuptools_build_meta": None,
            "wheel": None,
            "wheel_build_ready": False,
            "python_module_smoke_ready": False,
            "console_script_smoke_ready": False,
            "full_packaging_smoke_ready": False,
            "blockers": [],
            "optional_gaps": [],
            "console_script_strategy": "blocked",
            "error": "Unable to inspect packaging modules via /tmp/missing-python: launcher failed",
        },
    )

    payload = packaging_smoke.run_packaging_smoke(project_root=project_root, python_executable="/tmp/missing-python")

    assert payload["ok"] is False
    assert payload["strategy"] == "blocked"
    assert payload["strategy_family"] == "blocked"
    assert payload["steps"] == []
    assert payload["failed_step"] == "packaging-status"
    assert payload["packaging"]["error"] == "Unable to inspect packaging modules via /tmp/missing-python: launcher failed"
    assert payload["reason"] == "Packaging smoke is blocked: Unable to inspect packaging modules via /tmp/missing-python: launcher failed"


def test_format_packaging_smoke_text_reports_python_source():
    payload = {
        "ok": True,
        "reason": "Packaging smoke passed.",
        "python": "/tmp/env-python",
        "packaging_python": "/tmp/env-python",
        "packaging_python_source": "environment",
        "project_root": "/tmp/repo",
        "packaging": {"blockers": [], "console_script_strategy": "venv"},
        "strategy": "venv",
        "strategy_family": "usable",
        "workspace": "/tmp/work",
        "wheel": "/tmp/dist/resource_hunter-1.0.0-py3-none-any.whl",
        "console_script": "/tmp/venv/bin/resource-hunter",
        "steps": [],
    }

    text = packaging_smoke.format_packaging_smoke_text(payload)

    assert "Python: /tmp/env-python (via RESOURCE_HUNTER_PACKAGING_PYTHON)" in text
    assert "strategy_family: usable" in text


def test_format_packaging_smoke_text_reports_bootstrap_details():
    payload = {
        "ok": True,
        "reason": "Packaging smoke passed.",
        "python": "/tmp/env-python",
        "packaging_python": "/tmp/env-python",
        "packaging_python_source": "current",
        "project_root": "/tmp/repo",
        "packaging": {"blockers": [], "console_script_strategy": "prefix-install"},
        "strategy": "prefix-install",
        "strategy_family": "usable",
        "workspace": "/tmp/work",
        "wheel": "/tmp/dist/resource_hunter-1.0.0-py3-none-any.whl",
        "console_script": "/tmp/prefix/bin/resource-hunter",
        "bootstrapped_build_requirements": ["setuptools>=69", "wheel"],
        "steps": [],
    }

    text = packaging_smoke.format_packaging_smoke_text(payload)

    assert "build_dependency_bootstrap: setuptools>=69, wheel" in text


def test_format_packaging_smoke_text_reports_requested_project_root_when_it_differs():
    payload = {
        "ok": False,
        "reason": "Packaging smoke requires a project root containing pyproject.toml and src/resource_hunter.",
        "python": sys.executable,
        "project_root": None,
        "project_root_source": "argument",
        "requested_project_root": "/tmp/repo/scripts",
        "packaging_python": sys.executable,
        "packaging_python_source": "current",
        "packaging": {
            "blockers": [],
            "console_script_strategy": "blocked",
            "project_root": None,
            "project_root_source": "argument",
        },
        "strategy": "blocked",
        "strategy_family": "blocked",
        "steps": [],
    }

    text = packaging_smoke.format_packaging_smoke_text(payload)

    assert "requested_project_root: /tmp/repo/scripts" in text
    assert "project_root_source: argument" in text


@pytest.mark.parametrize(
    ("script_name", "args", "expected_text"),
    [
        ("hunt.py", ["--help"], "usage:"),
        ("pansou.py", ["--help"], "Legacy pan search wrapper"),
        ("torrent.py", ["--help"], "Legacy torrent search wrapper"),
        ("video.py", ["--help"], "usage:"),
    ],
)
def test_legacy_wrapper_help_smoke(tmp_path, script_name, args, expected_text):
    result = _run_command([sys.executable, str(SCRIPTS / script_name), *args], cwd=tmp_path)
    assert result.returncode == 0, result.stderr or result.stdout
    assert expected_text in result.stdout


def test_venv_console_script_prefers_generated_entrypoint(tmp_path):
    scripts_dir = tmp_path / ("Scripts" if os.name == "nt" else "bin")
    scripts_dir.mkdir()
    expected = scripts_dir / ("resource-hunter.exe" if os.name == "nt" else "resource-hunter")
    expected.write_text("", encoding="utf-8")
    if os.name == "nt":
        (scripts_dir / "resource-hunter").write_text("", encoding="utf-8")

    assert _venv_console_script(tmp_path, "resource-hunter") == expected


def test_prefix_console_script_prefers_generated_entrypoint(tmp_path):
    scripts_dir, _ = _prefix_paths(tmp_path)
    scripts_dir.mkdir(parents=True)
    expected = scripts_dir / ("resource-hunter.exe" if os.name == "nt" else "resource-hunter")
    expected.write_text("", encoding="utf-8")
    if os.name == "nt":
        (scripts_dir / "resource-hunter").write_text("", encoding="utf-8")

    assert _prefix_console_script(tmp_path, "resource-hunter") == expected


def test_resource_hunter_entrypoints_after_wheel_install(tmp_path):
    if not _supports_wheel_build():
        pytest.skip("pip, wheel, or setuptools build backend unavailable in this interpreter")

    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()

    build_result = _run_command(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--no-deps",
            "--no-build-isolation",
            "--wheel-dir",
            str(dist_dir),
            str(ROOT),
        ],
        cwd=ROOT,
    )
    assert build_result.returncode == 0, build_result.stderr or build_result.stdout

    wheels = sorted(dist_dir.glob("resource_hunter-*.whl"))
    assert len(wheels) == 1

    artifact_root = tmp_path / "downloaded-gh-artifacts"
    artifact_path = _write_packaging_baseline_artifact(
        artifact_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
    )
    gh_seed_root = tmp_path / "github-run-seed"
    _write_packaging_baseline_artifact(
        gh_seed_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
    )
    _write_packaging_baseline_artifact(
        gh_seed_root,
        "resource-hunter-packaging-baseline-windows-latest-py3.12",
    )
    fake_bin = tmp_path / "fake-gh-bin"
    fake_bin.mkdir()
    invocation_log = tmp_path / "fake-gh-invocation.json"
    fake_gh = _write_fake_gh_download_command(fake_bin, seed_root=gh_seed_root, invocation_log=invocation_log)
    gh_download_dir = tmp_path / "downloaded-gh-artifacts-via-gh"
    scratch_root = tmp_path / "scratch"
    ok_path = _write_packaging_baseline_artifact(
        scratch_root,
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.12",
    )
    drift_path = _write_packaging_baseline_artifact(
        scratch_root,
        "resource-hunter-packaging-baseline-windows-latest-py3.13",
        baseline_contract_ok=False,
    )
    downloads_root = tmp_path / "downloaded-gh-artifact-zips"
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

    if _supports_venv():
        import venv

        venv_dir = tmp_path / "venv"
        venv.EnvBuilder(with_pip=True, clear=True).create(venv_dir)
        venv_python = _venv_python(venv_dir)
        install_result = _run_command(
            [str(venv_python), "-m", "pip", "install", "--no-index", str(wheels[0])],
            cwd=tmp_path,
        )
        assert install_result.returncode == 0, install_result.stderr or install_result.stdout
        help_result = _run_command([str(venv_python), "-m", "resource_hunter", "--help"], cwd=tmp_path)
        version_result = _run_command([str(venv_python), "-m", "resource_hunter", "--version"], cwd=tmp_path)
        console_script = _venv_console_script(venv_dir, "resource-hunter")
        assert console_script.exists(), f"console script not generated: {console_script}"
        console_help_result = _run_command([str(console_script), "--help"], cwd=tmp_path)
        console_version_result = _run_command([str(console_script), "--version"], cwd=tmp_path)
        report_console_script = _venv_console_script(venv_dir, "resource-hunter-packaging-baseline-report")
        assert report_console_script.exists(), f"packaging report console script not generated: {report_console_script}"
        report_help_result = _run_command([str(report_console_script), "--help"], cwd=tmp_path)
        report_json_result = _run_command([str(report_console_script), "--json", str(artifact_root)], cwd=tmp_path)
        report_zip_json_result = _run_command(
            [str(report_console_script), "--json", "--require-contract-ok", str(downloads_root)],
            cwd=tmp_path,
        )
        gate_console_script = _venv_console_script(venv_dir, "resource-hunter-packaging-baseline-gate")
        assert gate_console_script.exists(), f"packaging gate console script not generated: {gate_console_script}"
        gate_help_result = _run_command([str(gate_console_script), "--help"], cwd=tmp_path)
        gate_json_result = _run_command(
            [str(gate_console_script), "--json", "--require-artifact-count", "1", str(artifact_root)],
            cwd=tmp_path,
        )
        gate_zip_json_result = _run_command(
            [str(gate_console_script), "--json", "--require-artifact-count", "2", str(downloads_root)],
            cwd=tmp_path,
        )
        gate_github_env = _clean_env()
        gate_github_env["PATH"] = f"{fake_bin}{os.pathsep}{gate_github_env.get('PATH', '')}"
        gate_github_json_result = _run_command(
            [
                str(gate_console_script),
                "--json",
                "--github-run",
                "123456",
                "--repo",
                "openclaw/resource-hunter",
                "--download-dir",
                str(gh_download_dir),
                "--require-artifact-count",
                "2",
            ],
            cwd=tmp_path,
            env=gate_github_env,
        )
    else:
        install_root = tmp_path / "wheel-install"
        install_result = _run_command(
            [sys.executable, "-m", "pip", "install", "--no-index", "--prefix", str(install_root), str(wheels[0])],
            cwd=tmp_path,
        )
        assert install_result.returncode == 0, install_result.stderr or install_result.stdout
        env = _prefix_env(install_root)
        help_result = _run_command([sys.executable, "-m", "resource_hunter", "--help"], cwd=tmp_path, env=env)
        version_result = _run_command([sys.executable, "-m", "resource_hunter", "--version"], cwd=tmp_path, env=env)
        console_script = _prefix_console_script(install_root, "resource-hunter")
        assert console_script.exists(), f"console script not generated: {console_script}"
        console_help_result = _run_command([str(console_script), "--help"], cwd=tmp_path, env=env)
        console_version_result = _run_command([str(console_script), "--version"], cwd=tmp_path, env=env)
        report_console_script = _prefix_console_script(install_root, "resource-hunter-packaging-baseline-report")
        assert report_console_script.exists(), f"packaging report console script not generated: {report_console_script}"
        report_help_result = _run_command([str(report_console_script), "--help"], cwd=tmp_path, env=env)
        report_json_result = _run_command(
            [str(report_console_script), "--json", str(artifact_root)],
            cwd=tmp_path,
            env=env,
        )
        report_zip_json_result = _run_command(
            [str(report_console_script), "--json", "--require-contract-ok", str(downloads_root)],
            cwd=tmp_path,
            env=env,
        )
        gate_console_script = _prefix_console_script(install_root, "resource-hunter-packaging-baseline-gate")
        assert gate_console_script.exists(), f"packaging gate console script not generated: {gate_console_script}"
        gate_help_result = _run_command([str(gate_console_script), "--help"], cwd=tmp_path, env=env)
        gate_json_result = _run_command(
            [str(gate_console_script), "--json", "--require-artifact-count", "1", str(artifact_root)],
            cwd=tmp_path,
            env=env,
        )
        gate_zip_json_result = _run_command(
            [str(gate_console_script), "--json", "--require-artifact-count", "2", str(downloads_root)],
            cwd=tmp_path,
            env=env,
        )
        gate_github_env = dict(env)
        gate_github_env["PATH"] = f"{fake_bin}{os.pathsep}{gate_github_env.get('PATH', '')}"
        gate_github_json_result = _run_command(
            [
                str(gate_console_script),
                "--json",
                "--github-run",
                "123456",
                "--repo",
                "openclaw/resource-hunter",
                "--download-dir",
                str(gh_download_dir),
                "--require-artifact-count",
                "2",
            ],
            cwd=tmp_path,
            env=gate_github_env,
        )

    assert help_result.returncode == 0, help_result.stderr or help_result.stdout
    assert "usage:" in help_result.stdout
    assert "search" in help_result.stdout
    assert version_result.returncode == 0, version_result.stderr or version_result.stdout
    assert version_result.stdout.strip() == f"resource-hunter {__version__}"
    if console_help_result is not None:
        assert console_help_result.returncode == 0, console_help_result.stderr or console_help_result.stdout
        assert "usage:" in console_help_result.stdout
        assert "search" in console_help_result.stdout
    if console_version_result is not None:
        assert console_version_result.returncode == 0, console_version_result.stderr or console_version_result.stdout
        assert console_version_result.stdout.strip() == f"resource-hunter {__version__}"
    assert report_help_result.returncode == 0, report_help_result.stderr or report_help_result.stdout
    assert "usage:" in report_help_result.stdout
    assert "artifact file(s)" in report_help_result.stdout
    expected_report_payload = packaging_report.read_packaging_baseline_reports([artifact_root])
    assert report_json_result.returncode == 0, report_json_result.stderr or report_json_result.stdout
    assert json.loads(report_json_result.stdout) == expected_report_payload
    expected_zip_report_payload = packaging_report.read_packaging_baseline_reports([downloads_root])
    expected_zip_report_failures = packaging_report.packaging_baseline_report_requirement_failures(
        expected_zip_report_payload
    )
    assert report_zip_json_result.returncode == 2, report_zip_json_result.stderr or report_zip_json_result.stdout
    assert json.loads(report_zip_json_result.stdout) == expected_zip_report_payload
    for failure in expected_zip_report_failures:
        assert failure in report_zip_json_result.stderr
    assert gate_help_result.returncode == 0, gate_help_result.stderr or gate_help_result.stdout
    assert "usage:" in gate_help_result.stdout
    assert gate_json_result.returncode == 0, gate_json_result.stderr or gate_json_result.stdout
    assert json.loads(gate_json_result.stdout) == {
        "gate_schema_version": 1,
        "ok": True,
        "failure_count": 0,
        "failures": [],
        "report_type": "single",
        "summary": {
            "passing_capture_matches_expectation": True,
            "blocked_capture_matches_expectation": True,
            "baseline_contract_ok": True,
        },
        "artifact_path": str(artifact_path.resolve()),
        "expected_artifact_count": 1,
        "actual_artifact_count": 1,
    }
    drift_ref = f"{archive_path.resolve()}!/job-b/packaging-baseline.json"
    assert gate_zip_json_result.returncode == 2, gate_zip_json_result.stderr or gate_zip_json_result.stdout
    assert json.loads(gate_zip_json_result.stdout) == {
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
        "expected_artifact_count": 2,
        "actual_artifact_count": 2,
    }
    assert (
        f"{drift_ref}: Packaging baseline requirement failed: Blocked capture did not report failed_step."
        in gate_zip_json_result.stderr
    )
    assert gate_github_json_result.returncode == 0, gate_github_json_result.stderr or gate_github_json_result.stdout
    assert gate_github_json_result.stderr == ""
    gate_github_payload = json.loads(gate_github_json_result.stdout)
    expected_gh_download_paths = [
        str(
            (
                gh_download_dir
                / "resource-hunter-packaging-baseline-ubuntu-latest-py3.12"
                / "packaging-baseline.json"
            ).resolve()
        ),
        str(
            (
                gh_download_dir
                / "resource-hunter-packaging-baseline-windows-latest-py3.12"
                / "packaging-baseline.json"
            ).resolve()
        ),
    ]
    assert gate_github_payload == packaging_gate.build_packaging_baseline_gate_payload(
        packaging_report.read_packaging_baseline_reports([gh_download_dir]),
        required_artifact_count=2,
        download_payload={
            "provider": "github-actions",
            "run_id": "123456",
            "repo": "openclaw/resource-hunter",
            "download_dir": str(gh_download_dir.resolve()),
            "download_dir_source": "argument",
            "download_dir_retained": True,
            "artifact_names": [],
            "artifact_patterns": [packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN],
            "artifact_filter_source": "default",
            "resolved_artifact_count": 2,
            "resolved_artifact_paths": expected_gh_download_paths,
            "resolved_archive_member_count": 0,
            "resolved_filesystem_artifact_count": 2,
            "download_command": gate_github_payload["download"]["download_command"],
        },
    )
    assert [part.lower() if isinstance(part, str) else part for part in gate_github_payload["download"]["download_command"]] == [
        str(fake_gh.resolve()).lower(),
        "run",
        "download",
        "123456",
        "--repo",
        "openclaw/resource-hunter",
        "--dir",
        str(gh_download_dir.resolve()).lower(),
        "--pattern",
        packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN,
    ]
    assert json.loads(invocation_log.read_text(encoding="utf-8")) == [
        "run",
        "download",
        "123456",
        "--repo",
        "openclaw/resource-hunter",
        "--dir",
        str(gh_download_dir.resolve()),
        "--pattern",
        packaging_gate.DEFAULT_GITHUB_ARTIFACT_PATTERN,
    ]
