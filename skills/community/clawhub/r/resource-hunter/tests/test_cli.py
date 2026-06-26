from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from resource_hunter import __version__
from resource_hunter import cli


def _packaging_smoke_payload_with_provenance(
    payload: dict[str, object],
    *,
    python_executable: str | None = None,
    packaging_python_source: str | None = None,
    packaging_python_candidates: list[dict[str, object]] | None = None,
    packaging_python_auto_selected: bool | None = None,
) -> dict[str, object]:
    response = dict(payload)
    response["packaging_python"] = python_executable or payload.get("python") or sys.executable
    response["packaging_python_source"] = packaging_python_source or (
        "argument" if python_executable is not None else "current"
    )
    if packaging_python_candidates is not None:
        response["packaging_python_candidates"] = packaging_python_candidates
    if packaging_python_auto_selected is not None:
        response["packaging_python_auto_selected"] = packaging_python_auto_selected
    return response


def test_cli_search_json(monkeypatch, capsys):
    fake_response = {
        "query": "test query",
        "intent": {"kind": "general", "quick": False},
        "plan": {"channels": ["pan", "torrent"], "notes": ["demo"]},
        "results": [
            {
                "channel": "pan",
                "source": "2fun",
                "provider": "aliyun",
                "title": "Demo",
                "link_or_magnet": "https://example.com",
                "password": "1234",
                "share_id_or_info_hash": "abc",
                "size": "",
                "seeders": 0,
                "quality": "",
                "score": 77,
                "reasons": ["query match"],
                "raw": {},
            }
        ],
        "warnings": [],
        "source_status": [],
        "meta": {"cached": False},
    }

    def fake_search(self, intent, plan=None, page=1, limit=8, use_cache=True):
        return fake_response

    monkeypatch.setattr("resource_hunter.core.ResourceHunterEngine.search", fake_search)
    rc = cli.main(["search", "test query", "--json"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["query"] == "test query"
    assert payload["results"][0]["password"] == "1234"


def test_cli_sources_text(monkeypatch, capsys):
    def fake_catalog(self, probe=False):
        return {
            "sources": [
                {
                    "source": "2fun",
                    "channel": "pan",
                    "priority": 1,
                    "recent_status": {"ok": True, "skipped": False, "latency_ms": 42, "error": "", "checked_at": "now"},
                }
            ],
            "meta": {"probe": probe},
        }

    monkeypatch.setattr("resource_hunter.core.ResourceHunterEngine.source_catalog", fake_catalog)
    rc = cli.main(["sources"])
    assert rc == 0
    output = capsys.readouterr().out
    assert "2fun" in output
    assert "priority=1" in output


def test_cli_doctor_json_includes_packaging(monkeypatch, capsys, tmp_path):
    packaging = {
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

    def fake_catalog(self, probe=False):
        return {"sources": [], "meta": {"probe": probe}}

    def fake_video_doctor(self):
        return {"binaries": {"yt_dlp": None, "ffmpeg": None}, "recent_manifests": []}

    monkeypatch.setattr("resource_hunter.core.ResourceHunterEngine.source_catalog", fake_catalog)
    monkeypatch.setattr("resource_hunter.video_core.VideoManager.doctor", fake_video_doctor)
    monkeypatch.setattr(cli, "_packaging_status", lambda python_executable=None: packaging)
    monkeypatch.setattr(cli.packaging_tools, "find_project_root", lambda project_root=None: tmp_path)

    rc = cli.main(["doctor", "--json"])

    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["project_root"] == str(tmp_path)
    assert payload["project_root_source"] == "discovered"
    assert payload["packaging"] == {
        **packaging,
        "project_root": str(tmp_path),
        "project_root_source": "discovered",
    }
    assert any("setuptools" in item for item in payload["advice"])
    assert any("wheel" in item for item in payload["advice"])


def test_cli_doctor_text_reports_packaging_readiness(monkeypatch, capsys, tmp_path):
    def fake_catalog(self, probe=False):
        return {"sources": [], "meta": {"probe": probe}}

    def fake_video_doctor(self):
        return {"binaries": {"yt_dlp": "/bin/yt-dlp", "ffmpeg": "/bin/ffmpeg"}, "recent_manifests": []}

    monkeypatch.setattr("resource_hunter.core.ResourceHunterEngine.source_catalog", fake_catalog)
    monkeypatch.setattr("resource_hunter.video_core.VideoManager.doctor", fake_video_doctor)
    monkeypatch.setattr(cli.packaging_tools, "find_project_root", lambda project_root=None: tmp_path)
    monkeypatch.setattr(
        cli,
        "_packaging_status",
        lambda python_executable=None: {
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
    )

    rc = cli.main(["doctor"])

    assert rc == 0
    output = capsys.readouterr().out
    assert f"Packaging Python: {sys.executable} (current interpreter)" in output
    assert f"project_root: {tmp_path}" in output
    assert "project_root_source: discovered" in output
    assert "Packaging readiness:" in output
    assert "venv: missing" in output
    assert "setuptools.build_meta: ok" in output
    assert "wheel: ok" in output
    assert "console script smoke: ready" in output
    assert "blockers: none" in output
    assert "optional gaps: venv" in output
    assert "console script strategy: prefix fallback" in output


def test_cli_doctor_text_reports_requested_project_root_when_it_differs(monkeypatch, capsys, tmp_path):
    project_root = tmp_path / "repo"
    requested_root = project_root / "ops" / "workspace"
    (project_root / "src" / "resource_hunter").mkdir(parents=True)
    (project_root / "pyproject.toml").write_text("[project]\nname='resource-hunter'\n", encoding="utf-8")
    requested_root.mkdir(parents=True)

    def fake_catalog(self, probe=False):
        return {"sources": [], "meta": {"probe": probe}}

    def fake_video_doctor(self):
        return {"binaries": {"yt_dlp": "/bin/yt-dlp", "ffmpeg": "/bin/ffmpeg"}, "recent_manifests": []}

    monkeypatch.setattr("resource_hunter.core.ResourceHunterEngine.source_catalog", fake_catalog)
    monkeypatch.setattr("resource_hunter.video_core.VideoManager.doctor", fake_video_doctor)
    monkeypatch.setattr(
        cli,
        "_packaging_status",
        lambda python_executable=None: {
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
    )

    rc = cli.main(["doctor", "--project-root", str(requested_root)])

    assert rc == 0
    output = capsys.readouterr().out
    assert f"project_root: {project_root}" in output
    assert f"requested_project_root: {requested_root}" in output
    assert "project_root_source: argument" in output


def test_cli_doctor_text_reports_packaging_blockers(monkeypatch, capsys):
    def fake_catalog(self, probe=False):
        return {"sources": [], "meta": {"probe": probe}}

    def fake_video_doctor(self):
        return {"binaries": {"yt_dlp": "/bin/yt-dlp", "ffmpeg": "/bin/ffmpeg"}, "recent_manifests": []}

    monkeypatch.setattr("resource_hunter.core.ResourceHunterEngine.source_catalog", fake_catalog)
    monkeypatch.setattr("resource_hunter.video_core.VideoManager.doctor", fake_video_doctor)
    monkeypatch.setattr(
        cli,
        "_packaging_status",
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

    rc = cli.main(["doctor"])

    assert rc == 0
    output = capsys.readouterr().out
    assert "blockers: setuptools.build_meta, wheel" in output
    assert "console script strategy: blocked" in output


def test_cli_doctor_text_reports_packaging_probe_error(monkeypatch, capsys):
    packaging = {
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
    }

    def fake_catalog(self, probe=False):
        return {"sources": [], "meta": {"probe": probe}}

    def fake_video_doctor(self):
        return {"binaries": {"yt_dlp": "/bin/yt-dlp", "ffmpeg": "/bin/ffmpeg"}, "recent_manifests": []}

    monkeypatch.setattr("resource_hunter.core.ResourceHunterEngine.source_catalog", fake_catalog)
    monkeypatch.setattr("resource_hunter.video_core.VideoManager.doctor", fake_video_doctor)
    monkeypatch.setattr(cli, "_packaging_status", lambda python_executable=None: packaging)

    rc = cli.main(["doctor", "--python", "/tmp/missing-python"])

    assert rc == 0
    output = capsys.readouterr().out
    assert "Packaging Python: /tmp/missing-python (via --python)" in output
    assert "pip: unknown" in output
    assert "venv: unknown" in output
    assert "error: Unable to inspect packaging modules via /tmp/missing-python: launcher failed" in output
    assert "could not be inspected for packaging readiness" in output


def test_cli_doctor_require_packaging_ready_fails_on_blockers(monkeypatch, capsys):
    packaging = {
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

    def fake_catalog(self, probe=False):
        return {"sources": [], "meta": {"probe": probe}}

    def fake_video_doctor(self):
        return {"binaries": {"yt_dlp": None, "ffmpeg": None}, "recent_manifests": []}

    monkeypatch.setattr("resource_hunter.core.ResourceHunterEngine.source_catalog", fake_catalog)
    monkeypatch.setattr("resource_hunter.video_core.VideoManager.doctor", fake_video_doctor)
    monkeypatch.setattr(cli, "_packaging_status", lambda python_executable=None: packaging)

    rc = cli.main(["doctor", "--json", "--require-packaging-ready"])

    captured = capsys.readouterr()
    assert rc == 2
    payload = json.loads(captured.out)
    assert payload["packaging"] == {
        **packaging,
        "project_root": payload["project_root"],
        "project_root_source": payload["project_root_source"],
    }
    assert "Packaging gate failed" in captured.err
    assert "setuptools.build_meta" in captured.err
    assert "wheel" in captured.err


def test_cli_doctor_require_packaging_ready_fails_on_probe_error(monkeypatch, capsys):
    packaging = {
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
    }

    def fake_catalog(self, probe=False):
        return {"sources": [], "meta": {"probe": probe}}

    def fake_video_doctor(self):
        return {"binaries": {"yt_dlp": None, "ffmpeg": None}, "recent_manifests": []}

    monkeypatch.setattr("resource_hunter.core.ResourceHunterEngine.source_catalog", fake_catalog)
    monkeypatch.setattr("resource_hunter.video_core.VideoManager.doctor", fake_video_doctor)
    monkeypatch.setattr(cli, "_packaging_status", lambda python_executable=None: packaging)

    rc = cli.main(["doctor", "--json", "--python", "/tmp/missing-python", "--require-packaging-ready"])

    captured = capsys.readouterr()
    assert rc == 2
    payload = json.loads(captured.out)
    assert payload["packaging"] == {
        **packaging,
        "project_root": payload["project_root"],
        "project_root_source": payload["project_root_source"],
    }
    assert captured.err.strip() == "Packaging gate failed: Unable to inspect packaging modules via /tmp/missing-python: launcher failed"


def test_cli_doctor_require_packaging_ready_allows_prefix_fallback(monkeypatch, capsys):
    packaging = {
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

    def fake_catalog(self, probe=False):
        return {"sources": [], "meta": {"probe": probe}}

    def fake_video_doctor(self):
        return {"binaries": {"yt_dlp": "/bin/yt-dlp", "ffmpeg": "/bin/ffmpeg"}, "recent_manifests": []}

    monkeypatch.setattr("resource_hunter.core.ResourceHunterEngine.source_catalog", fake_catalog)
    monkeypatch.setattr("resource_hunter.video_core.VideoManager.doctor", fake_video_doctor)
    monkeypatch.setattr(cli, "_packaging_status", lambda python_executable=None: packaging)

    rc = cli.main(["doctor", "--json", "--require-packaging-ready"])

    captured = capsys.readouterr()
    assert rc == 0
    payload = json.loads(captured.out)
    assert payload["packaging"] == {
        **packaging,
        "project_root": payload["project_root"],
        "project_root_source": payload["project_root_source"],
    }
    assert captured.err == ""


def test_cli_packaging_smoke_json(monkeypatch, capsys, tmp_path):
    payload = {
        "ok": True,
        "reason": "Packaging smoke passed.",
        "python": "/usr/bin/python",
        "project_root": str(tmp_path),
        "project_root_source": "discovered",
        "packaging": {
            "blockers": [],
            "console_script_strategy": "venv",
            "project_root_source": "discovered",
        },
        "strategy": "venv",
        "workspace": str(tmp_path / "work"),
        "wheel": str(tmp_path / "dist" / "resource_hunter-1.0.0-py3-none-any.whl"),
        "console_script": str(tmp_path / "venv" / "bin" / "resource-hunter"),
        "steps": [],
    }

    monkeypatch.setattr(
        cli.packaging_tools,
        "run_packaging_smoke",
        lambda project_root=None, python_executable=None, packaging_python_source=None, packaging_python_candidates=None, packaging_python_auto_selected=None, bootstrap_build_deps=False: _packaging_smoke_payload_with_provenance(
            payload,
            python_executable=python_executable,
            packaging_python_source=packaging_python_source,
            packaging_python_candidates=packaging_python_candidates,
            packaging_python_auto_selected=packaging_python_auto_selected,
        ),
    )

    rc = cli.main(["packaging-smoke", "--json"])

    assert rc == 0
    assert json.loads(capsys.readouterr().out) == {
        **payload,
        "packaging_python": "/usr/bin/python",
        "packaging_python_source": "current",
    }


def test_cli_packaging_smoke_failure_returns_exit_2(monkeypatch, capsys, tmp_path):
    payload = {
        "ok": False,
        "reason": "Wheel build failed.",
        "python": "/usr/bin/python",
        "project_root": str(tmp_path),
        "project_root_source": "discovered",
        "packaging": {
            "blockers": [],
            "console_script_strategy": "venv",
            "project_root_source": "discovered",
        },
        "strategy": "venv",
        "workspace": str(tmp_path / "work"),
        "wheel": None,
        "console_script": None,
        "failed_step": "build-wheel",
        "steps": [{"name": "build-wheel", "returncode": 1, "ok": False}],
    }

    monkeypatch.setattr(
        cli.packaging_tools,
        "run_packaging_smoke",
        lambda project_root=None, python_executable=None, packaging_python_source=None, packaging_python_candidates=None, packaging_python_auto_selected=None, bootstrap_build_deps=False: _packaging_smoke_payload_with_provenance(
            payload,
            python_executable=python_executable,
            packaging_python_source=packaging_python_source,
            packaging_python_candidates=packaging_python_candidates,
            packaging_python_auto_selected=packaging_python_auto_selected,
        ),
    )

    rc = cli.main(["packaging-smoke"])

    captured = capsys.readouterr()
    assert rc == 2
    assert "Wheel build failed." in captured.out
    assert "Wheel build failed." in captured.err


def test_cli_doctor_forwards_python_override(monkeypatch, capsys):
    recorded: list[str | None] = []
    packaging = {
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

    def fake_catalog(self, probe=False):
        return {"sources": [], "meta": {"probe": probe}}

    def fake_video_doctor(self):
        return {"binaries": {"yt_dlp": "/bin/yt-dlp", "ffmpeg": "/bin/ffmpeg"}, "recent_manifests": []}

    def fake_packaging_status(python_executable=None):
        recorded.append(python_executable)
        return packaging

    monkeypatch.setattr("resource_hunter.core.ResourceHunterEngine.source_catalog", fake_catalog)
    monkeypatch.setattr("resource_hunter.video_core.VideoManager.doctor", fake_video_doctor)
    monkeypatch.setattr(cli, "_packaging_status", fake_packaging_status)
    monkeypatch.setenv("RESOURCE_HUNTER_PACKAGING_PYTHON", "/tmp/env-python")

    rc = cli.main(["doctor", "--json", "--python", "/tmp/alt-python"])

    assert rc == 0
    assert recorded == ["/tmp/alt-python"]
    payload = json.loads(capsys.readouterr().out)
    assert payload["packaging"] == {
        **packaging,
        "project_root": payload["project_root"],
        "project_root_source": payload["project_root_source"],
    }
    assert payload["packaging_python"] == "/tmp/alt-python"
    assert payload["packaging_python_source"] == "argument"


def test_cli_doctor_uses_env_python_override(monkeypatch, capsys):
    recorded: list[str | None] = []
    packaging = {
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

    def fake_catalog(self, probe=False):
        return {"sources": [], "meta": {"probe": probe}}

    def fake_video_doctor(self):
        return {"binaries": {"yt_dlp": "/bin/yt-dlp", "ffmpeg": "/bin/ffmpeg"}, "recent_manifests": []}

    def fake_packaging_status(python_executable=None):
        recorded.append(python_executable)
        return packaging

    monkeypatch.setattr("resource_hunter.core.ResourceHunterEngine.source_catalog", fake_catalog)
    monkeypatch.setattr("resource_hunter.video_core.VideoManager.doctor", fake_video_doctor)
    monkeypatch.setattr(cli, "_packaging_status", fake_packaging_status)
    monkeypatch.setenv("RESOURCE_HUNTER_PACKAGING_PYTHON", "/tmp/env-python")

    rc = cli.main(["doctor", "--json"])

    assert rc == 0
    assert recorded == ["/tmp/env-python"]
    payload = json.loads(capsys.readouterr().out)
    assert payload["packaging"] == {
        **packaging,
        "project_root": payload["project_root"],
        "project_root_source": payload["project_root_source"],
    }
    assert payload["packaging_python"] == "/tmp/env-python"
    assert payload["packaging_python_source"] == "environment"


def test_cli_doctor_auto_selects_packaging_python(monkeypatch, capsys):
    recorded: list[str | None] = []
    packaging = {
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
    candidates = [
        {
            "python": "/tmp/current-python",
            "source": "current",
            "ready": False,
            "packaging": {
                "blockers": ["wheel"],
                "optional_gaps": ["venv"],
            },
        },
        {
            "python": "/tmp/ready-python",
            "source": "path:python",
            "ready": True,
            "packaging": packaging,
        },
    ]

    def fake_catalog(self, probe=False):
        return {"sources": [], "meta": {"probe": probe}}

    def fake_video_doctor(self):
        return {"binaries": {"yt_dlp": "/bin/yt-dlp", "ffmpeg": "/bin/ffmpeg"}, "recent_manifests": []}

    def fake_packaging_status(python_executable=None):
        recorded.append(python_executable)
        return packaging

    monkeypatch.setattr("resource_hunter.core.ResourceHunterEngine.source_catalog", fake_catalog)
    monkeypatch.setattr("resource_hunter.video_core.VideoManager.doctor", fake_video_doctor)
    monkeypatch.setattr(cli, "_packaging_status", fake_packaging_status)
    monkeypatch.setattr(
        cli.packaging_tools,
        "select_packaging_python",
        lambda project_root=None, allow_bootstrap_build_deps=False: ("/tmp/ready-python", candidates),
    )

    rc = cli.main(["doctor", "--json", "--python", "auto"])

    assert rc == 0
    assert recorded == ["/tmp/ready-python"]
    payload = json.loads(capsys.readouterr().out)
    assert payload["packaging"] == {
        **packaging,
        "project_root": payload["project_root"],
        "project_root_source": payload["project_root_source"],
    }
    assert payload["packaging_python"] == "/tmp/ready-python"
    assert payload["packaging_python_source"] == "auto"
    assert payload["packaging_python_auto_selected"] is True
    assert payload["packaging_python_candidates"] == candidates
    assert any("Auto-selected packaging Python /tmp/ready-python" in item for item in payload["advice"])


def test_cli_doctor_auto_reports_gate_failure_when_no_candidate_ready(monkeypatch, capsys):
    packaging = {
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
    candidates = [
        {
            "python": "/tmp/current-python",
            "source": "current",
            "ready": False,
            "packaging": packaging,
        }
    ]

    def fake_catalog(self, probe=False):
        return {"sources": [], "meta": {"probe": probe}}

    def fake_video_doctor(self):
        return {"binaries": {"yt_dlp": "/bin/yt-dlp", "ffmpeg": "/bin/ffmpeg"}, "recent_manifests": []}

    monkeypatch.setattr("resource_hunter.core.ResourceHunterEngine.source_catalog", fake_catalog)
    monkeypatch.setattr("resource_hunter.video_core.VideoManager.doctor", fake_video_doctor)
    monkeypatch.setattr(cli, "_packaging_status", lambda python_executable=None: packaging)
    monkeypatch.setattr(
        cli.packaging_tools,
        "select_packaging_python",
        lambda project_root=None, allow_bootstrap_build_deps=False: (None, candidates),
    )

    rc = cli.main(["doctor", "--json", "--python", "auto", "--require-packaging-ready"])

    captured = capsys.readouterr()
    assert rc == 2
    payload = json.loads(captured.out)
    assert payload["packaging_python_source"] == "auto"
    assert payload["packaging_python_auto_selected"] is False
    assert payload["packaging_python_candidates"] == candidates
    assert "auto-discovery found no packaging-ready interpreter" in captured.err
    assert "setuptools.build_meta" in captured.err
    assert "wheel" in captured.err


def test_cli_doctor_auto_selects_bootstrap_capable_python_when_requested(monkeypatch, capsys, tmp_path):
    recorded: list[str | None] = []
    selected_roots: list[str | None] = []
    annotated_roots: list[tuple[str | None, bool]] = []
    packaging = {
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
    packaging_with_bootstrap = {
        **packaging,
        "bootstrap_build_deps_ready": True,
        "bootstrap_build_requirements": ["setuptools>=69", "wheel"],
        "bootstrap_console_script_strategy": "prefix-install",
        "packaging_smoke_ready_with_bootstrap": True,
    }
    candidates = [
        {
            "python": "/tmp/current-python",
            "source": "current",
            "ready": False,
            "bootstrap_ready": False,
            "packaging": packaging,
        },
        {
            "python": "/tmp/bootstrap-python",
            "source": "path:python",
            "ready": True,
            "bootstrap_ready": True,
            "packaging": packaging_with_bootstrap,
        },
    ]

    def fake_catalog(self, probe=False):
        return {"sources": [], "meta": {"probe": probe}}

    def fake_video_doctor(self):
        return {"binaries": {"yt_dlp": "/bin/yt-dlp", "ffmpeg": "/bin/ffmpeg"}, "recent_manifests": []}

    def fake_packaging_status(python_executable=None):
        recorded.append(python_executable)
        return packaging

    def fake_annotate(packaging_payload, *, project_root=None, include_bootstrap_metadata=True):
        annotated_roots.append((project_root, include_bootstrap_metadata))
        return {**packaging_payload, **packaging_with_bootstrap, "project_root": project_root}

    def fake_select(project_root=None, allow_bootstrap_build_deps=False):
        assert allow_bootstrap_build_deps is True
        selected_roots.append(project_root)
        return "/tmp/bootstrap-python", candidates

    monkeypatch.setattr("resource_hunter.core.ResourceHunterEngine.source_catalog", fake_catalog)
    monkeypatch.setattr("resource_hunter.video_core.VideoManager.doctor", fake_video_doctor)
    monkeypatch.setattr(cli, "_packaging_status", fake_packaging_status)
    monkeypatch.setattr(cli.packaging_tools, "annotate_project_packaging_status", fake_annotate)
    monkeypatch.setattr(cli.packaging_tools, "select_packaging_python", fake_select)

    rc = cli.main(
        [
            "doctor",
            "--json",
            "--project-root",
            str(tmp_path),
            "--python",
            "auto",
            "--bootstrap-build-deps",
            "--require-packaging-ready",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    assert captured.err == ""
    assert recorded == ["/tmp/bootstrap-python"]
    assert selected_roots == [str(tmp_path)]
    assert annotated_roots == [(str(tmp_path), True)]
    payload = json.loads(captured.out)
    assert payload["project_root"] == str(tmp_path)
    assert payload["packaging_python"] == "/tmp/bootstrap-python"
    assert payload["packaging_python_source"] == "auto"
    assert payload["packaging_python_auto_selected"] is True
    assert payload["packaging_python_candidates"] == candidates
    assert payload["packaging_bootstrap_build_deps_requested"] is True
    assert payload["packaging"]["project_root"] == str(tmp_path)
    assert payload["packaging"]["bootstrap_build_deps_ready"] is True
    assert payload["packaging"]["packaging_smoke_ready_with_bootstrap"] is True
    assert any(
        "Auto-selected bootstrap-capable packaging Python /tmp/bootstrap-python" in item
        for item in payload["advice"]
    )


def test_cli_packaging_smoke_forwards_python_override(monkeypatch, capsys, tmp_path):
    recorded: list[tuple[str | None, str | None]] = []
    payload = {
        "ok": True,
        "reason": "Packaging smoke passed.",
        "python": "/tmp/alt-python",
        "project_root": str(tmp_path),
        "project_root_source": "argument",
        "packaging": {
            "blockers": [],
            "console_script_strategy": "venv",
            "project_root_source": "argument",
        },
        "strategy": "venv",
        "workspace": str(tmp_path / "work"),
        "wheel": str(tmp_path / "dist" / "resource_hunter-1.0.0-py3-none-any.whl"),
        "console_script": str(tmp_path / "venv" / "bin" / "resource-hunter"),
        "steps": [],
    }

    def fake_run_packaging_smoke(
        project_root=None,
        python_executable=None,
        packaging_python_source=None,
        packaging_python_candidates=None,
        packaging_python_auto_selected=None,
        bootstrap_build_deps=False,
    ):
        recorded.append((project_root, python_executable))
        return _packaging_smoke_payload_with_provenance(
            payload,
            python_executable=python_executable,
            packaging_python_source=packaging_python_source,
            packaging_python_candidates=packaging_python_candidates,
            packaging_python_auto_selected=packaging_python_auto_selected,
        )

    monkeypatch.setattr(cli.packaging_tools, "run_packaging_smoke", fake_run_packaging_smoke)

    rc = cli.main(["packaging-smoke", "--json", "--project-root", str(tmp_path), "--python", "/tmp/alt-python"])

    assert rc == 0
    assert recorded == [(str(tmp_path), "/tmp/alt-python")]
    assert json.loads(capsys.readouterr().out) == {
        **payload,
        "packaging_python": "/tmp/alt-python",
        "packaging_python_source": "argument",
    }


def test_cli_packaging_smoke_uses_env_python_override(monkeypatch, capsys, tmp_path):
    recorded: list[tuple[str | None, str | None]] = []
    payload = {
        "ok": True,
        "reason": "Packaging smoke passed.",
        "python": "/tmp/env-python",
        "project_root": str(tmp_path),
        "project_root_source": "argument",
        "packaging": {
            "blockers": [],
            "console_script_strategy": "venv",
            "project_root_source": "argument",
        },
        "strategy": "venv",
        "workspace": str(tmp_path / "work"),
        "wheel": str(tmp_path / "dist" / "resource_hunter-1.0.0-py3-none-any.whl"),
        "console_script": str(tmp_path / "venv" / "bin" / "resource-hunter"),
        "steps": [],
    }

    def fake_run_packaging_smoke(
        project_root=None,
        python_executable=None,
        packaging_python_source=None,
        packaging_python_candidates=None,
        packaging_python_auto_selected=None,
        bootstrap_build_deps=False,
    ):
        recorded.append((project_root, python_executable))
        return _packaging_smoke_payload_with_provenance(
            payload,
            python_executable=python_executable,
            packaging_python_source=packaging_python_source,
            packaging_python_candidates=packaging_python_candidates,
            packaging_python_auto_selected=packaging_python_auto_selected,
        )

    monkeypatch.setattr(cli.packaging_tools, "run_packaging_smoke", fake_run_packaging_smoke)
    monkeypatch.setenv("RESOURCE_HUNTER_PACKAGING_PYTHON", "/tmp/env-python")

    rc = cli.main(["packaging-smoke", "--json", "--project-root", str(tmp_path)])

    assert rc == 0
    assert recorded == [(str(tmp_path), "/tmp/env-python")]
    assert json.loads(capsys.readouterr().out) == {
        **payload,
        "packaging_python": "/tmp/env-python",
        "packaging_python_source": "environment",
    }


def test_cli_packaging_smoke_forwards_bootstrap_flag(monkeypatch, capsys, tmp_path):
    recorded: list[tuple[str | None, str | None, bool]] = []
    payload = {
        "ok": True,
        "reason": "Packaging smoke passed.",
        "python": sys.executable,
        "project_root": str(tmp_path),
        "project_root_source": "argument",
        "packaging": {
            "blockers": [],
            "console_script_strategy": "venv",
            "project_root_source": "argument",
        },
        "strategy": "venv",
        "workspace": str(tmp_path / "work"),
        "wheel": str(tmp_path / "dist" / "resource_hunter-1.0.0-py3-none-any.whl"),
        "console_script": str(tmp_path / "venv" / "bin" / "resource-hunter"),
        "steps": [],
    }

    def fake_run_packaging_smoke(
        project_root=None,
        python_executable=None,
        packaging_python_source=None,
        packaging_python_candidates=None,
        packaging_python_auto_selected=None,
        bootstrap_build_deps=False,
    ):
        recorded.append((project_root, python_executable, bootstrap_build_deps))
        return _packaging_smoke_payload_with_provenance(
            payload,
            python_executable=python_executable,
            packaging_python_source=packaging_python_source,
            packaging_python_candidates=packaging_python_candidates,
            packaging_python_auto_selected=packaging_python_auto_selected,
        )

    monkeypatch.setattr(cli.packaging_tools, "run_packaging_smoke", fake_run_packaging_smoke)

    rc = cli.main(["packaging-smoke", "--json", "--project-root", str(tmp_path), "--bootstrap-build-deps"])

    assert rc == 0
    assert recorded == [(str(tmp_path), None, True)]
    payload = json.loads(capsys.readouterr().out)
    assert payload["packaging_python"] == sys.executable
    assert payload["packaging_python_source"] == "current"


def test_cli_packaging_smoke_auto_fallback_reports_candidates(monkeypatch, capsys, tmp_path):
    recorded: list[tuple[str | None, str | None]] = []
    payload = {
        "ok": False,
        "reason": "Packaging smoke is blocked: setuptools.build_meta, wheel",
        "python": sys.executable,
        "project_root": str(tmp_path),
        "project_root_source": "argument",
        "packaging": {
            "blockers": ["setuptools.build_meta", "wheel"],
            "optional_gaps": ["venv"],
            "console_script_strategy": "blocked",
            "project_root_source": "argument",
        },
        "strategy": "blocked",
        "workspace": None,
        "wheel": None,
        "console_script": None,
        "steps": [],
    }
    candidates = [
        {
            "python": sys.executable,
            "source": "current",
            "ready": False,
            "packaging": {
                "blockers": ["setuptools.build_meta", "wheel"],
                "optional_gaps": ["venv"],
            },
        }
    ]

    def fake_run_packaging_smoke(
        project_root=None,
        python_executable=None,
        packaging_python_source=None,
        packaging_python_candidates=None,
        packaging_python_auto_selected=None,
        bootstrap_build_deps=False,
    ):
        recorded.append((project_root, python_executable))
        return _packaging_smoke_payload_with_provenance(
            payload,
            python_executable=python_executable,
            packaging_python_source=packaging_python_source,
            packaging_python_candidates=packaging_python_candidates,
            packaging_python_auto_selected=packaging_python_auto_selected,
        )

    monkeypatch.setattr(cli.packaging_tools, "run_packaging_smoke", fake_run_packaging_smoke)
    monkeypatch.setattr(
        cli.packaging_tools,
        "select_packaging_python",
        lambda project_root=None, allow_bootstrap_build_deps=False: (None, candidates),
    )

    rc = cli.main(["packaging-smoke", "--json", "--project-root", str(tmp_path), "--python", "auto"])

    captured = capsys.readouterr()
    assert rc == 2
    assert recorded == [(str(tmp_path), sys.executable)]
    payload = json.loads(captured.out)
    assert payload["packaging_python"] == sys.executable
    assert payload["packaging_python_source"] == "auto"
    assert payload["packaging_python_auto_selected"] is False
    assert payload["packaging_python_candidates"] == candidates
    assert "Packaging smoke is blocked" in captured.err


def test_cli_packaging_smoke_auto_selects_bootstrap_capable_python_when_requested(monkeypatch, capsys, tmp_path):
    recorded: list[tuple[str | None, str | None, bool]] = []
    payload = {
        "ok": True,
        "reason": "Packaging smoke passed.",
        "python": "/tmp/bootstrap-python",
        "project_root": str(tmp_path),
        "project_root_source": "argument",
        "packaging": {
            "blockers": ["setuptools.build_meta", "wheel"],
            "optional_gaps": ["venv"],
            "console_script_strategy": "blocked",
            "project_root_source": "argument",
            "bootstrap_build_deps_ready": True,
            "bootstrap_build_requirements": ["setuptools>=69", "wheel"],
            "bootstrap_console_script_strategy": "prefix-install",
            "packaging_smoke_ready_with_bootstrap": True,
        },
        "strategy": "prefix-install",
        "workspace": str(tmp_path / "work"),
        "wheel": str(tmp_path / "dist" / "resource_hunter-1.0.0-py3-none-any.whl"),
        "console_script": str(tmp_path / "prefix" / "Scripts" / "resource-hunter.exe"),
        "bootstrapped_build_requirements": ["setuptools>=69", "wheel"],
        "steps": [],
    }
    candidates = [
        {
            "python": "/tmp/bootstrap-python",
            "source": "path:python",
            "ready": True,
            "bootstrap_ready": True,
            "packaging": payload["packaging"],
        }
    ]

    def fake_run_packaging_smoke(
        project_root=None,
        python_executable=None,
        packaging_python_source=None,
        packaging_python_candidates=None,
        packaging_python_auto_selected=None,
        bootstrap_build_deps=False,
    ):
        recorded.append((project_root, python_executable, bootstrap_build_deps))
        return _packaging_smoke_payload_with_provenance(
            payload,
            python_executable=python_executable,
            packaging_python_source=packaging_python_source,
            packaging_python_candidates=packaging_python_candidates,
            packaging_python_auto_selected=packaging_python_auto_selected,
        )

    def fake_select(project_root=None, allow_bootstrap_build_deps=False):
        assert allow_bootstrap_build_deps is True
        assert project_root == str(tmp_path)
        return "/tmp/bootstrap-python", candidates

    monkeypatch.setattr(cli.packaging_tools, "run_packaging_smoke", fake_run_packaging_smoke)
    monkeypatch.setattr(cli.packaging_tools, "select_packaging_python", fake_select)

    rc = cli.main(
        [
            "packaging-smoke",
            "--json",
            "--project-root",
            str(tmp_path),
            "--python",
            "auto",
            "--bootstrap-build-deps",
        ]
    )

    assert rc == 0
    assert recorded == [(str(tmp_path), "/tmp/bootstrap-python", True)]
    payload = json.loads(capsys.readouterr().out)
    assert payload["packaging_python"] == "/tmp/bootstrap-python"
    assert payload["packaging_python_source"] == "auto"
    assert payload["packaging_python_auto_selected"] is True
    assert payload["packaging_python_candidates"] == candidates


def test_cli_packaging_capture_json_bundles_doctor_and_smoke(monkeypatch, capsys, tmp_path):
    candidates = [
        {
            "python": "/tmp/bootstrap-python",
            "source": "path:python",
            "ready": True,
            "bootstrap_ready": True,
            "packaging": {
                "blockers": ["setuptools.build_meta", "wheel"],
                "optional_gaps": ["venv"],
                "console_script_strategy": "blocked",
                "project_root": str(tmp_path),
                "project_root_source": "argument",
                "requested_project_root": str(tmp_path),
                "bootstrap_build_deps_ready": True,
                "bootstrap_build_requirements": ["setuptools>=69", "wheel"],
                "bootstrap_console_script_strategy": "prefix-install",
                "packaging_smoke_ready_with_bootstrap": True,
            },
        }
    ]
    doctor_payload = {
        "version": "1.0.0",
        "python": sys.executable,
        "packaging_python": "/tmp/bootstrap-python",
        "packaging_python_source": "auto",
        "packaging_python_auto_selected": True,
        "packaging_python_candidates": candidates,
        "stdout_encoding": "utf-8",
        "cache_db": str(tmp_path / "cache.db"),
        "storage_root": str(tmp_path / "storage"),
        "project_root": str(tmp_path),
        "project_root_source": "argument",
        "requested_project_root": str(tmp_path),
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
            "project_root": str(tmp_path),
            "project_root_source": "argument",
            "requested_project_root": str(tmp_path),
            "bootstrap_build_deps_ready": True,
            "bootstrap_build_requirements": ["setuptools>=69", "wheel"],
            "bootstrap_console_script_strategy": "prefix-install",
            "packaging_smoke_ready_with_bootstrap": True,
        },
        "packaging_bootstrap_build_deps_requested": True,
        "recent_sources": {"sources": []},
        "recent_manifests": [],
        "advice": [],
    }
    smoke_payload = {
        "ok": False,
        "reason": "Console script smoke failed.",
        "python": "/tmp/bootstrap-python",
        "project_root": str(tmp_path),
        "project_root_source": "argument",
        "requested_project_root": str(tmp_path),
        "packaging": doctor_payload["packaging"],
        "strategy": "prefix-install",
        "strategy_family": "usable",
        "workspace": str(tmp_path / "work"),
        "wheel": str(tmp_path / "dist" / "resource_hunter-1.0.0-py3-none-any.whl"),
        "console_script": str(tmp_path / "prefix" / "Scripts" / "resource-hunter.exe"),
        "bootstrapped_build_requirements": ["setuptools>=69", "wheel"],
        "steps": [],
        "failed_step": "console-script",
    }
    recorded: list[tuple[str | None, str | None, str | None, list[dict[str, object]] | None, bool | None, bool]] = []

    def fake_doctor_payload(
        engine,
        *,
        probe=False,
        python_executable=None,
        bootstrap_build_deps=False,
        project_root=None,
    ):
        assert probe is False
        assert python_executable == "auto"
        assert bootstrap_build_deps is True
        assert project_root == str(tmp_path)
        return doctor_payload

    def fake_run_packaging_smoke(
        project_root=None,
        python_executable=None,
        packaging_python_source=None,
        packaging_python_candidates=None,
        packaging_python_auto_selected=None,
        bootstrap_build_deps=False,
    ):
        recorded.append(
            (
                project_root,
                python_executable,
                packaging_python_source,
                packaging_python_candidates,
                packaging_python_auto_selected,
                bootstrap_build_deps,
            )
        )
        return _packaging_smoke_payload_with_provenance(
            smoke_payload,
            python_executable=python_executable,
            packaging_python_source=packaging_python_source,
            packaging_python_candidates=packaging_python_candidates,
            packaging_python_auto_selected=packaging_python_auto_selected,
        )

    monkeypatch.setattr(cli, "_doctor_payload", fake_doctor_payload)
    monkeypatch.setattr(cli.packaging_tools, "run_packaging_smoke", fake_run_packaging_smoke)

    rc = cli.main(
        [
            "packaging-capture",
            "--json",
            "--project-root",
            str(tmp_path),
            "--python",
            "auto",
            "--bootstrap-build-deps",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    assert captured.err == ""
    assert recorded == [(str(tmp_path), "/tmp/bootstrap-python", "auto", candidates, True, True)]
    payload = json.loads(captured.out)
    assert payload["schema_version"] == 1
    assert payload["project_root"] == str(tmp_path)
    assert payload["project_root_source"] == "argument"
    assert payload["requested_project_root"] == str(tmp_path)
    assert payload["packaging_python"] == "/tmp/bootstrap-python"
    assert payload["packaging_python_source"] == "auto"
    assert payload["packaging_python_auto_selected"] is True
    assert payload["packaging_python_candidates"] == candidates
    assert payload["failed_step"] == "console-script"
    assert payload["summary"]["doctor_packaging_ready"] is True
    assert payload["summary"]["packaging_smoke_ok"] is False
    assert payload["summary"]["strategy"] == "prefix-install"
    assert payload["summary"]["strategy_family"] == "usable"
    assert payload["summary"]["reason"] == "Console script smoke failed."
    assert payload["requirements"] == {
        "require_packaging_ready": False,
        "require_smoke_ok": False,
        "ok": True,
        "failures": [],
    }
    assert payload["doctor"] == doctor_payload
    assert payload["packaging_smoke"]["failed_step"] == "console-script"


def test_cli_packaging_capture_writes_output_file(monkeypatch, capsys, tmp_path):
    doctor_payload = {
        "version": "1.0.0",
        "python": sys.executable,
        "packaging_python": sys.executable,
        "packaging_python_source": "current",
        "stdout_encoding": "utf-8",
        "cache_db": str(tmp_path / "cache.db"),
        "storage_root": str(tmp_path / "storage"),
        "project_root": str(tmp_path),
        "project_root_source": "argument",
        "requested_project_root": str(tmp_path),
        "binaries": {"yt_dlp": None, "ffmpeg": None},
        "packaging": {
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
            "project_root": str(tmp_path),
            "project_root_source": "argument",
            "requested_project_root": str(tmp_path),
        },
        "packaging_bootstrap_build_deps_requested": False,
        "recent_sources": {"sources": []},
        "recent_manifests": [],
        "advice": [],
    }
    smoke_payload = {
        "ok": True,
        "reason": "Packaging smoke passed.",
        "python": sys.executable,
        "project_root": str(tmp_path),
        "project_root_source": "argument",
        "requested_project_root": str(tmp_path),
        "packaging": doctor_payload["packaging"],
        "strategy": "venv",
        "workspace": str(tmp_path / "work"),
        "wheel": str(tmp_path / "dist" / "resource_hunter-1.0.0-py3-none-any.whl"),
        "console_script": str(tmp_path / "venv" / "bin" / "resource-hunter"),
        "steps": [],
    }
    output_path = tmp_path / "artifacts" / "packaging-capture.json"

    monkeypatch.setattr(cli, "_doctor_payload", lambda *args, **kwargs: doctor_payload)

    def fake_run_packaging_smoke(
        project_root=None,
        python_executable=None,
        packaging_python_source=None,
        packaging_python_candidates=None,
        packaging_python_auto_selected=None,
        bootstrap_build_deps=False,
    ):
        return _packaging_smoke_payload_with_provenance(
            smoke_payload,
            python_executable=python_executable,
            packaging_python_source=packaging_python_source,
            packaging_python_candidates=packaging_python_candidates,
            packaging_python_auto_selected=packaging_python_auto_selected,
        )

    monkeypatch.setattr(
        cli.packaging_tools,
        "run_packaging_smoke",
        fake_run_packaging_smoke,
    )

    rc = cli.main(["packaging-capture", "--project-root", str(tmp_path), "--output", str(output_path)])

    captured = capsys.readouterr()
    assert rc == 0
    stdout_payload = json.loads(captured.out)
    file_payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert file_payload == stdout_payload
    assert stdout_payload["summary"]["packaging_smoke_ok"] is True
    assert stdout_payload["requirements"] == {
        "require_packaging_ready": False,
        "require_smoke_ok": False,
        "ok": True,
        "failures": [],
    }


def test_cli_packaging_capture_records_requirement_failures_in_bundle(monkeypatch, capsys, tmp_path):
    doctor_payload = {
        "version": "1.0.0",
        "python": sys.executable,
        "packaging_python": sys.executable,
        "packaging_python_source": "current",
        "stdout_encoding": "utf-8",
        "cache_db": str(tmp_path / "cache.db"),
        "storage_root": str(tmp_path / "storage"),
        "project_root": str(tmp_path),
        "project_root_source": "argument",
        "requested_project_root": str(tmp_path),
        "binaries": {"yt_dlp": None, "ffmpeg": None},
        "packaging": {
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
        "packaging_bootstrap_build_deps_requested": False,
        "recent_sources": {"sources": []},
        "recent_manifests": [],
        "advice": [],
    }
    smoke_payload = {
        "ok": False,
        "reason": "Console script smoke failed.",
        "python": sys.executable,
        "project_root": str(tmp_path),
        "project_root_source": "argument",
        "requested_project_root": str(tmp_path),
        "packaging": doctor_payload["packaging"],
        "strategy": "venv",
        "workspace": str(tmp_path / "work"),
        "wheel": str(tmp_path / "dist" / "resource_hunter-1.0.0-py3-none-any.whl"),
        "console_script": str(tmp_path / "venv" / "bin" / "resource-hunter"),
        "steps": [],
        "failed_step": "console-script",
    }

    monkeypatch.setattr(cli, "_doctor_payload", lambda *args, **kwargs: doctor_payload)
    monkeypatch.setattr(
        cli.packaging_tools,
        "run_packaging_smoke",
        lambda project_root=None, python_executable=None, packaging_python_source=None, packaging_python_candidates=None, packaging_python_auto_selected=None, bootstrap_build_deps=False: _packaging_smoke_payload_with_provenance(
            smoke_payload,
            python_executable=python_executable,
            packaging_python_source=packaging_python_source,
            packaging_python_candidates=packaging_python_candidates,
            packaging_python_auto_selected=packaging_python_auto_selected,
        ),
    )

    rc = cli.main(["packaging-capture", "--project-root", str(tmp_path), "--require-smoke-ok"])

    captured = capsys.readouterr()
    assert rc == 2
    payload = json.loads(captured.out)
    assert payload["requirements"]["require_packaging_ready"] is False
    assert payload["requirements"]["require_smoke_ok"] is True
    assert payload["requirements"]["ok"] is False
    assert payload["requirements"]["failures"] == [
        "Packaging capture requirement failed: packaging smoke did not pass (failed_step=console-script): Console script smoke failed."
    ]
    assert payload["summary"]["packaging_smoke_ok"] is False
    assert "failed_step=console-script" in captured.err


def test_cli_packaging_capture_require_packaging_ready_fails_after_writing_output(monkeypatch, capsys, tmp_path):
    output_path = tmp_path / "artifacts" / "packaging-capture.json"
    payload = {
        "schema_version": 1,
        "captured_at": "2026-03-23T00:00:00Z",
        "project_root": str(tmp_path),
        "project_root_source": "argument",
        "requested_project_root": str(tmp_path),
        "packaging_python": "/missing/python",
        "packaging_python_source": "argument",
        "bootstrap_build_deps_requested": False,
        "failed_step": "packaging-status",
        "summary": {
            "doctor_packaging_ready": False,
            "packaging_smoke_ok": False,
            "strategy": "blocked",
            "reason": "Unable to inspect packaging modules.",
        },
        "doctor": {
            "packaging_python": "/missing/python",
            "packaging_python_source": "argument",
            "packaging": {
                "error": "Unable to inspect packaging modules via /missing/python: launcher error",
            },
        },
        "packaging_smoke": {
            "ok": False,
            "reason": "Unable to inspect packaging modules.",
            "failed_step": "packaging-status",
        },
    }

    monkeypatch.setattr(cli, "_packaging_capture_payload", lambda *args, **kwargs: payload)

    rc = cli.main(["packaging-capture", "--output", str(output_path), "--require-packaging-ready"])

    captured = capsys.readouterr()
    assert rc == 2
    stdout_payload = json.loads(captured.out)
    file_payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert stdout_payload == payload
    assert file_payload == payload
    assert "Packaging gate failed: Unable to inspect packaging modules via /missing/python: launcher error" in captured.err


def test_cli_packaging_capture_require_smoke_ok_fails_after_writing_output(monkeypatch, capsys, tmp_path):
    output_path = tmp_path / "artifacts" / "packaging-capture.json"
    payload = {
        "schema_version": 1,
        "captured_at": "2026-03-23T00:00:00Z",
        "project_root": str(tmp_path),
        "project_root_source": "argument",
        "requested_project_root": str(tmp_path),
        "packaging_python": sys.executable,
        "packaging_python_source": "current",
        "bootstrap_build_deps_requested": False,
        "failed_step": "console-script",
        "summary": {
            "doctor_packaging_ready": True,
            "packaging_smoke_ok": False,
            "strategy": "prefix-install",
            "reason": "Console script smoke failed.",
        },
        "doctor": {
            "packaging_python": sys.executable,
            "packaging_python_source": "current",
            "packaging": {
                "blockers": [],
                "full_packaging_smoke_ready": True,
            },
        },
        "packaging_smoke": {
            "ok": False,
            "reason": "Console script smoke failed.",
            "failed_step": "console-script",
        },
    }

    monkeypatch.setattr(cli, "_packaging_capture_payload", lambda *args, **kwargs: payload)

    rc = cli.main(["packaging-capture", "--output", str(output_path), "--require-smoke-ok"])

    captured = capsys.readouterr()
    assert rc == 2
    stdout_payload = json.loads(captured.out)
    file_payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert stdout_payload == payload
    assert file_payload == payload
    assert "Packaging capture requirement failed: packaging smoke did not pass" in captured.err
    assert "failed_step=console-script" in captured.err
    assert "Console script smoke failed." in captured.err


def test_cli_packaging_baseline_writes_passing_and_blocked_artifacts(monkeypatch, capsys, tmp_path):
    project_root = tmp_path / "checkout"
    project_root.mkdir()
    output_dir = tmp_path / "artifacts"
    captured_calls: list[tuple[str | None, str | None, bool]] = []

    def fake_packaging_capture_payload(_engine, args):
        captured_calls.append((args.project_root, args.python, args.bootstrap_build_deps))
        blocked = args.python is not None
        payload = {
            "schema_version": 1,
            "captured_at": "2026-03-23T00:00:00Z",
            "project_root": str(project_root),
            "project_root_source": "argument",
            "requested_project_root": str(project_root),
            "packaging_python": args.python or sys.executable,
            "packaging_python_source": "argument" if args.python else "current",
            "failed_step": "packaging-status" if blocked else None,
            "summary": {
                "doctor_packaging_ready": not blocked,
                "packaging_smoke_ok": not blocked,
                "strategy": "blocked" if blocked else "venv",
                "strategy_family": "blocked" if blocked else "usable",
                "reason": "Unable to inspect packaging modules." if blocked else "Packaging smoke passed.",
            },
        }
        return payload

    monkeypatch.setattr(cli, "_capture_timestamp", lambda: "2026-03-23T00:00:00Z")
    monkeypatch.setattr(cli, "_packaging_capture_payload", fake_packaging_capture_payload)

    rc = cli.main([
        "packaging-baseline",
        "--project-root",
        str(project_root),
        "--output-dir",
        str(output_dir),
    ])

    captured = capsys.readouterr()
    assert rc == 0
    stdout_payload = json.loads(captured.out)
    baseline_payload = json.loads((output_dir / "packaging-baseline.json").read_text(encoding="utf-8"))
    passing_payload = json.loads((output_dir / "passing-packaging-capture.json").read_text(encoding="utf-8"))
    blocked_payload = json.loads((output_dir / "blocked-packaging-capture.json").read_text(encoding="utf-8"))

    assert baseline_payload == stdout_payload
    assert passing_payload["summary"]["packaging_smoke_ok"] is True
    assert blocked_payload["summary"]["packaging_smoke_ok"] is False
    assert stdout_payload["passing_capture"]["path"] == str(output_dir / "passing-packaging-capture.json")
    assert stdout_payload["passing_capture"]["project_root"] == str(project_root)
    assert stdout_payload["passing_capture"]["project_root_source"] == "argument"
    assert stdout_payload["passing_capture"]["requested_project_root"] == str(project_root)
    assert stdout_payload["passing_capture"]["doctor_packaging_ready"] is True
    assert stdout_payload["passing_capture"]["packaging_smoke_ok"] is True
    assert stdout_payload["passing_capture"]["strategy"] == "venv"
    assert stdout_payload["passing_capture"]["strategy_family"] == "usable"
    assert stdout_payload["passing_capture"]["reason"] == "Packaging smoke passed."
    assert stdout_payload["passing_capture"]["expected_outcome"] == {
        "doctor_packaging_ready": True,
        "packaging_smoke_ok": True,
        "failed_step_present": False,
        "strategy_family_any_of": ["usable"],
    }
    assert stdout_payload["passing_capture"]["matches_expectation"] is True
    assert stdout_payload["passing_capture"]["expectation_drift"] == []
    assert stdout_payload["blocked_capture"]["path"] == str(output_dir / "blocked-packaging-capture.json")
    assert stdout_payload["blocked_capture"]["project_root"] == str(project_root)
    assert stdout_payload["blocked_capture"]["project_root_source"] == "argument"
    assert stdout_payload["blocked_capture"]["requested_project_root"] == str(project_root)
    assert stdout_payload["blocked_capture"]["doctor_packaging_ready"] is False
    assert stdout_payload["blocked_capture"]["packaging_smoke_ok"] is False
    assert stdout_payload["blocked_capture"]["strategy"] == "blocked"
    assert stdout_payload["blocked_capture"]["strategy_family"] == "blocked"
    assert stdout_payload["blocked_capture"]["reason"] == "Unable to inspect packaging modules."
    assert stdout_payload["blocked_capture"]["failed_step"] == "packaging-status"
    assert stdout_payload["blocked_capture"]["expected_outcome"] == {
        "doctor_packaging_ready": False,
        "packaging_smoke_ok": False,
        "failed_step_present": True,
        "strategy_family_any_of": ["blocked"],
    }
    assert stdout_payload["blocked_capture"]["matches_expectation"] is True
    assert stdout_payload["blocked_capture"]["expectation_drift"] == []
    assert stdout_payload["summary"] == {
        "passing_capture_matches_expectation": True,
        "blocked_capture_matches_expectation": True,
        "baseline_contract_ok": True,
    }
    assert stdout_payload["requirements"] == {
        "require_expected_outcomes": False,
        "ok": True,
        "failures": [],
    }
    assert stdout_payload["warnings"] == []
    assert stdout_payload["requested_project_root"] == str(project_root)
    assert stdout_payload["blocked_python"] == captured_calls[1][1]
    assert captured_calls[0] == (str(project_root), None, False)
    assert captured_calls[1][0] == str(project_root)
    assert captured_calls[1][2] is False
    assert Path(stdout_payload["blocked_python"]).name.startswith("missing-resource-hunter-python")


def test_cli_packaging_baseline_require_expected_outcomes_records_success(monkeypatch, capsys, tmp_path):
    def fake_packaging_capture_payload(_engine, args):
        blocked = args.python is not None
        return {
            "schema_version": 1,
            "captured_at": "2026-03-23T00:00:00Z",
            "project_root": str(tmp_path),
            "project_root_source": "discovered",
            "packaging_python": args.python or sys.executable,
            "packaging_python_source": "argument" if args.python else "current",
            "failed_step": "packaging-status" if blocked else None,
            "summary": {
                "doctor_packaging_ready": not blocked,
                "packaging_smoke_ok": not blocked,
                "strategy": "blocked" if blocked else "prefix-install",
                "strategy_family": "blocked" if blocked else "usable",
                "reason": "blocked" if blocked else "ok",
            },
        }

    monkeypatch.setattr(cli, "_capture_timestamp", lambda: "2026-03-23T00:00:00Z")
    monkeypatch.setattr(cli, "_packaging_capture_payload", fake_packaging_capture_payload)

    rc = cli.main([
        "packaging-baseline",
        "--output-dir",
        str(tmp_path / "artifacts"),
        "--require-expected-outcomes",
    ])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert rc == 0
    assert captured.err == ""
    assert payload["requirements"] == {
        "require_expected_outcomes": True,
        "ok": True,
        "failures": [],
    }
    assert payload["passing_capture"]["expected_outcome"] == {
        "doctor_packaging_ready": True,
        "packaging_smoke_ok": True,
        "failed_step_present": False,
        "strategy_family_any_of": ["usable"],
    }
    assert payload["passing_capture"]["matches_expectation"] is True
    assert payload["passing_capture"]["expectation_drift"] == []
    assert payload["blocked_capture"]["expected_outcome"] == {
        "doctor_packaging_ready": False,
        "packaging_smoke_ok": False,
        "failed_step_present": True,
        "strategy_family_any_of": ["blocked"],
    }
    assert payload["blocked_capture"]["matches_expectation"] is True
    assert payload["blocked_capture"]["expectation_drift"] == []


def test_cli_packaging_baseline_uses_explicit_blocked_python(monkeypatch, capsys, tmp_path):
    blocked_python = tmp_path / "missing-python.exe"
    seen: list[str | None] = []

    def fake_packaging_capture_payload(_engine, args):
        seen.append(args.python)
        blocked = args.python == str(blocked_python)
        return {
            "schema_version": 1,
            "captured_at": "2026-03-23T00:00:00Z",
            "project_root": str(tmp_path),
            "project_root_source": "argument",
            "packaging_python": args.python or sys.executable,
            "packaging_python_source": "argument" if args.python else "current",
            "failed_step": "packaging-status" if blocked else None,
            "summary": {
                "doctor_packaging_ready": not blocked,
                "packaging_smoke_ok": not blocked,
                "strategy": "blocked" if blocked else "venv",
                "strategy_family": "blocked" if blocked else "usable",
                "reason": "blocked" if blocked else "ok",
            },
        }

    monkeypatch.setattr(cli, "_capture_timestamp", lambda: "2026-03-23T00:00:00Z")
    monkeypatch.setattr(cli, "_packaging_capture_payload", fake_packaging_capture_payload)

    rc = cli.main([
        "packaging-baseline",
        "--output-dir",
        str(tmp_path / "artifacts"),
        "--blocked-python",
        str(blocked_python),
    ])

    captured = capsys.readouterr()
    assert rc == 0
    payload = json.loads(captured.out)
    assert payload["blocked_python"] == str(blocked_python)
    assert seen == [None, str(blocked_python)]


def test_cli_packaging_baseline_require_expected_outcomes_detects_contract_drift(monkeypatch, capsys, tmp_path):
    output_dir = tmp_path / "artifacts"

    def fake_packaging_capture_payload(_engine, args):
        blocked = args.python is not None
        if blocked:
            summary = {
                "doctor_packaging_ready": True,
                "packaging_smoke_ok": True,
                "strategy": "venv",
                "strategy_family": "usable",
                "reason": "Unexpected success.",
            }
            failed_step = None
        else:
            summary = {
                "doctor_packaging_ready": True,
                "packaging_smoke_ok": True,
                "strategy": "venv",
                "strategy_family": "usable",
                "reason": "Packaging smoke passed.",
            }
            failed_step = None
        return {
            "schema_version": 1,
            "captured_at": "2026-03-23T00:00:00Z",
            "project_root": str(tmp_path),
            "project_root_source": "discovered",
            "packaging_python": args.python or sys.executable,
            "packaging_python_source": "argument" if args.python else "current",
            "failed_step": failed_step,
            "summary": summary,
        }

    monkeypatch.setattr(cli, "_capture_timestamp", lambda: "2026-03-23T00:00:00Z")
    monkeypatch.setattr(cli, "_packaging_capture_payload", fake_packaging_capture_payload)

    rc = cli.main([
        "packaging-baseline",
        "--output-dir",
        str(output_dir),
        "--require-expected-outcomes",
    ])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert rc == 2
    assert payload["summary"] == {
        "passing_capture_matches_expectation": True,
        "blocked_capture_matches_expectation": False,
        "baseline_contract_ok": False,
    }
    assert payload["passing_capture"]["expected_outcome"] == {
        "doctor_packaging_ready": True,
        "packaging_smoke_ok": True,
        "failed_step_present": False,
        "strategy_family_any_of": ["usable"],
    }
    assert payload["passing_capture"]["matches_expectation"] is True
    assert payload["passing_capture"]["expectation_drift"] == []
    assert payload["blocked_capture"]["expected_outcome"] == {
        "doctor_packaging_ready": False,
        "packaging_smoke_ok": False,
        "failed_step_present": True,
        "strategy_family_any_of": ["blocked"],
    }
    assert payload["blocked_capture"]["matches_expectation"] is False
    assert payload["blocked_capture"]["expectation_drift"] == [
        {
            "capture": "blocked",
            "field": "doctor_packaging_ready",
            "kind": "value_mismatch",
            "expected": False,
            "actual": True,
            "message": "Blocked capture did not report doctor_packaging_ready=false.",
        },
        {
            "capture": "blocked",
            "field": "packaging_smoke_ok",
            "kind": "value_mismatch",
            "expected": False,
            "actual": True,
            "message": "Blocked capture did not report packaging_smoke_ok=false.",
        },
        {
            "capture": "blocked",
            "field": "failed_step",
            "kind": "missing_failed_step",
            "expected_present": True,
            "actual": None,
            "message": "Blocked capture did not report failed_step.",
        },
        {
            "capture": "blocked",
            "field": "strategy_family",
            "kind": "strategy_mismatch",
            "expected_any_of": ["blocked"],
            "actual": "usable",
            "message": "Blocked capture did not report strategy_family in [blocked].",
        },
    ]
    assert payload["requirements"] == {
        "require_expected_outcomes": True,
        "ok": False,
        "failures": [
            "Packaging baseline requirement failed: Blocked capture did not report doctor_packaging_ready=false.",
            "Packaging baseline requirement failed: Blocked capture did not report packaging_smoke_ok=false.",
            "Packaging baseline requirement failed: Blocked capture did not report failed_step.",
            "Packaging baseline requirement failed: Blocked capture did not report strategy_family in [blocked].",
        ],
    }
    assert payload["warnings"] == [
        "Blocked capture did not report doctor_packaging_ready=false.",
        "Blocked capture did not report packaging_smoke_ok=false.",
        "Blocked capture did not report failed_step.",
        "Blocked capture did not report strategy_family in [blocked].",
    ]
    assert "Packaging baseline requirement failed: Blocked capture did not report doctor_packaging_ready=false." in captured.err
    assert "Packaging baseline requirement failed: Blocked capture did not report packaging_smoke_ok=false." in captured.err
    assert "Packaging baseline requirement failed: Blocked capture did not report failed_step." in captured.err
    assert "Packaging baseline requirement failed: Blocked capture did not report strategy_family in [blocked]." in captured.err
    assert (output_dir / "packaging-baseline.json").exists()
    assert (output_dir / "passing-packaging-capture.json").exists()
    assert (output_dir / "blocked-packaging-capture.json").exists()


def test_cli_packaging_baseline_report_renders_expected_outcome_contract(capsys, tmp_path):
    artifact_path = tmp_path / "packaging-baseline.json"
    payload = {
        "schema_version": 1,
        "captured_at": "2026-03-23T00:00:00Z",
        "output_dir": str(tmp_path),
        "project_root": str(tmp_path),
        "project_root_source": "argument",
        "requested_project_root": str(tmp_path),
        "blocked_python": str(tmp_path / "__blocked_python__" / "missing-python"),
        "passing_capture": {
            "path": str(tmp_path / "passing-packaging-capture.json"),
            "project_root": str(tmp_path),
            "project_root_source": "argument",
            "requested_project_root": str(tmp_path),
            "packaging_python": sys.executable,
            "packaging_python_source": "current",
            "doctor_packaging_ready": True,
            "packaging_smoke_ok": True,
            "strategy": "prefix-install",
            "strategy_family": "usable",
            "reason": "Packaging smoke passed.",
            "failed_step": None,
            "expected_outcome": {
                "doctor_packaging_ready": True,
                "packaging_smoke_ok": True,
                "failed_step_present": False,
                "strategy_family_any_of": ["usable", "bootstrap"],
            },
            "matches_expectation": True,
            "expectation_drift": [],
        },
        "blocked_capture": {
            "path": str(tmp_path / "blocked-packaging-capture.json"),
            "project_root": str(tmp_path),
            "project_root_source": "argument",
            "requested_project_root": str(tmp_path),
            "packaging_python": str(tmp_path / "__blocked_python__" / "missing-python"),
            "packaging_python_source": "argument",
            "doctor_packaging_ready": False,
            "packaging_smoke_ok": False,
            "strategy": "prefix-install",
            "strategy_family": "usable",
            "reason": "Packaging smoke unexpectedly passed.",
            "failed_step": None,
            "expected_outcome": {
                "doctor_packaging_ready": False,
                "packaging_smoke_ok": False,
                "failed_step_present": True,
                "strategy_family_any_of": ["blocked"],
            },
            "matches_expectation": False,
            "expectation_drift": [
                {
                    "capture": "blocked",
                    "field": "failed_step",
                    "kind": "missing_failed_step",
                    "expected_present": True,
                    "actual": None,
                    "message": "Blocked capture did not report failed_step.",
                },
                {
                    "capture": "blocked",
                    "field": "strategy_family",
                    "kind": "strategy_mismatch",
                    "expected_any_of": ["blocked"],
                    "actual": "usable",
                    "message": "Blocked capture did not report strategy_family in [blocked].",
                },
            ],
        },
        "summary": {
            "passing_capture_matches_expectation": True,
            "blocked_capture_matches_expectation": False,
            "baseline_contract_ok": False,
        },
        "warnings": [
            "Blocked capture did not report failed_step.",
            "Blocked capture did not report strategy_family in [blocked].",
        ],
        "requirements": {
            "require_expected_outcomes": True,
            "ok": False,
            "failures": [
                "Packaging baseline requirement failed: Blocked capture did not report failed_step.",
                "Packaging baseline requirement failed: Blocked capture did not report strategy_family in [blocked].",
            ],
        },
    }
    artifact_path.write_text(json.dumps(payload), encoding="utf-8")

    rc = cli.main(["packaging-baseline-report", str(artifact_path)])

    assert rc == 0
    output = capsys.readouterr().out
    assert "Resource Hunter packaging baseline report" in output
    assert "- expected_outcome.strategy_family_any_of: usable, bootstrap" in output
    assert "- expected_outcome.failed_step_present: false" in output
    assert "- actual.failed_step: absent" in output
    assert "- matches_expectation: false" in output
    assert "- expectation_drift[1]: field=failed_step; kind=missing_failed_step; expected_present=true; actual=null; Blocked capture did not report failed_step." in output
    assert "- expectation_drift[2]: field=strategy_family; kind=strategy_mismatch; expected_any_of=blocked; actual=usable; Blocked capture did not report strategy_family in [blocked]." in output
    assert "- require_expected_outcomes: true" in output
    assert "- requirements.ok: false" in output


def test_cli_packaging_baseline_report_json_normalizes_captures(capsys, tmp_path):
    artifact_path = tmp_path / "packaging-baseline.json"
    payload = {
        "schema_version": 1,
        "captured_at": "2026-03-23T00:00:00Z",
        "output_dir": str(tmp_path),
        "project_root": str(tmp_path),
        "project_root_source": "argument",
        "requested_project_root": str(tmp_path),
        "blocked_python": str(tmp_path / "__blocked_python__" / "missing-python"),
        "passing_capture": {
            "path": str(tmp_path / "passing-packaging-capture.json"),
            "project_root": str(tmp_path),
            "project_root_source": "argument",
            "requested_project_root": str(tmp_path),
            "packaging_python": sys.executable,
            "packaging_python_source": "current",
            "doctor_packaging_ready": True,
            "packaging_smoke_ok": True,
            "strategy": "prefix-install",
            "strategy_family": "usable",
            "reason": "Packaging smoke passed.",
            "failed_step": None,
            "expected_outcome": {
                "doctor_packaging_ready": True,
                "packaging_smoke_ok": True,
                "failed_step_present": False,
                "strategy_family_any_of": ["usable", "bootstrap"],
            },
            "matches_expectation": True,
            "expectation_drift": [],
        },
        "blocked_capture": {
            "path": str(tmp_path / "blocked-packaging-capture.json"),
            "project_root": str(tmp_path),
            "project_root_source": "argument",
            "requested_project_root": str(tmp_path),
            "packaging_python": str(tmp_path / "__blocked_python__" / "missing-python"),
            "packaging_python_source": "argument",
            "doctor_packaging_ready": False,
            "packaging_smoke_ok": False,
            "strategy": "prefix-install",
            "strategy_family": "usable",
            "reason": "Packaging smoke unexpectedly passed.",
            "failed_step": None,
            "expected_outcome": {
                "doctor_packaging_ready": False,
                "packaging_smoke_ok": False,
                "failed_step_present": True,
                "strategy_family_any_of": ["blocked"],
            },
            "matches_expectation": False,
            "expectation_drift": [
                {
                    "capture": "blocked",
                    "field": "failed_step",
                    "kind": "missing_failed_step",
                    "expected_present": True,
                    "actual": None,
                    "message": "Blocked capture did not report failed_step.",
                }
            ],
        },
        "summary": {
            "passing_capture_matches_expectation": True,
            "blocked_capture_matches_expectation": False,
            "baseline_contract_ok": False,
        },
        "warnings": ["Blocked capture did not report failed_step."],
        "requirements": {
            "require_expected_outcomes": True,
            "ok": False,
            "failures": [
                "Packaging baseline requirement failed: Blocked capture did not report failed_step."
            ],
        },
    }
    artifact_path.write_text(json.dumps(payload), encoding="utf-8")

    rc = cli.main(["packaging-baseline-report", "--json", str(artifact_path)])

    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["report_schema_version"] == 1
    assert report["artifact_path"] == str(artifact_path.resolve())
    assert report["artifact_schema_version"] == 1
    assert report["summary"] == {
        "passing_capture_matches_expectation": True,
        "blocked_capture_matches_expectation": False,
        "baseline_contract_ok": False,
    }
    assert report["requirements"] == {
        "require_expected_outcomes": True,
        "ok": False,
        "failures": [
            "Packaging baseline requirement failed: Blocked capture did not report failed_step."
        ],
    }
    assert report["warnings"] == ["Blocked capture did not report failed_step."]
    assert [capture["name"] for capture in report["captures"]] == ["passing", "blocked"]
    assert report["captures"][0]["label"] == "Passing"
    assert report["captures"][0]["actual"] == {
        "doctor_packaging_ready": True,
        "packaging_smoke_ok": True,
        "failed_step": None,
        "strategy_family": "usable",
        "strategy": "prefix-install",
        "reason": "Packaging smoke passed.",
    }
    assert report["captures"][1]["expected_outcome"] == {
        "doctor_packaging_ready": False,
        "packaging_smoke_ok": False,
        "failed_step_present": True,
        "strategy_family_any_of": ["blocked"],
    }
    assert report["captures"][1]["matches_expectation"] is False
    assert report["captures"][1]["expectation_drift"] == [
        {
            "capture": "blocked",
            "field": "failed_step",
            "kind": "missing_failed_step",
            "expected_present": True,
            "actual": None,
            "message": "Blocked capture did not report failed_step.",
        }
    ]


def test_cli_packaging_baseline_report_defaults_to_local_artifact(monkeypatch, capsys, tmp_path):
    artifact_path = tmp_path / "artifacts" / "packaging-baseline" / "packaging-baseline.json"
    artifact_path.parent.mkdir(parents=True)
    artifact_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "captured_at": "2026-03-23T00:00:00Z",
                "output_dir": str(artifact_path.parent),
                "project_root": str(tmp_path),
                "project_root_source": "discovered",
                "blocked_python": str(tmp_path / "__blocked_python__" / "missing-python"),
                "passing_capture": {
                    "path": str(tmp_path / "passing-packaging-capture.json"),
                    "project_root": str(tmp_path),
                    "project_root_source": "discovered",
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
                    "path": str(tmp_path / "blocked-packaging-capture.json"),
                    "project_root": str(tmp_path),
                    "project_root_source": "discovered",
                    "doctor_packaging_ready": False,
                    "packaging_smoke_ok": False,
                    "strategy": "blocked",
                    "strategy_family": "blocked",
                    "reason": "Unable to inspect packaging modules.",
                    "failed_step": "packaging-status",
                    "expected_outcome": {
                        "doctor_packaging_ready": False,
                        "packaging_smoke_ok": False,
                        "failed_step_present": True,
                        "strategy_family_any_of": ["blocked"],
                    },
                    "matches_expectation": True,
                    "expectation_drift": [],
                },
                "summary": {
                    "passing_capture_matches_expectation": True,
                    "blocked_capture_matches_expectation": True,
                    "baseline_contract_ok": True,
                },
                "warnings": [],
                "requirements": {
                    "require_expected_outcomes": True,
                    "ok": True,
                    "failures": [],
                },
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    rc = cli.main(["packaging-baseline-report"])

    assert rc == 0
    output = capsys.readouterr().out
    assert f"artifact: {artifact_path.resolve()}" in output
    assert "- warning: none" in output
    assert "- expectation_drift: none" in output


def test_cli_packaging_baseline_report_aggregate_json_require_contract_ok(capsys, tmp_path):
    def baseline_payload(project_root: Path, *, baseline_contract_ok: bool, warnings: list[str], failures: list[str]):
        return {
            "schema_version": 1,
            "captured_at": "2026-03-23T00:00:00Z",
            "output_dir": str(project_root),
            "project_root": str(project_root),
            "project_root_source": "argument",
            "blocked_python": str(project_root / "__blocked_python__" / "missing-python"),
            "passing_capture": {
                "path": str(project_root / "passing-packaging-capture.json"),
                "project_root": str(project_root),
                "project_root_source": "argument",
                "packaging_python": sys.executable,
                "packaging_python_source": "current",
                "doctor_packaging_ready": True,
                "packaging_smoke_ok": True,
                "strategy": "prefix-install",
                "strategy_family": "usable",
                "reason": "Packaging smoke passed.",
                "failed_step": None,
                "expected_outcome": {
                    "doctor_packaging_ready": True,
                    "packaging_smoke_ok": True,
                    "failed_step_present": False,
                    "strategy_family_any_of": ["usable", "bootstrap"],
                },
                "matches_expectation": True,
                "expectation_drift": [],
            },
            "blocked_capture": {
                "path": str(project_root / "blocked-packaging-capture.json"),
                "project_root": str(project_root),
                "project_root_source": "argument",
                "packaging_python": str(project_root / "__blocked_python__" / "missing-python"),
                "packaging_python_source": "argument",
                "doctor_packaging_ready": False,
                "packaging_smoke_ok": False,
                "strategy": "missing-python",
                "strategy_family": "blocked" if baseline_contract_ok else "usable",
                "reason": "Python executable was not found.",
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
                        "message": "Blocked capture did not report failed_step.",
                    }
                ],
            },
            "summary": {
                "passing_capture_matches_expectation": True,
                "blocked_capture_matches_expectation": baseline_contract_ok,
                "baseline_contract_ok": baseline_contract_ok,
            },
            "warnings": warnings,
            "requirements": {
                "require_expected_outcomes": True,
                "ok": not failures,
                "failures": failures,
            },
        }

    artifact_root = tmp_path / "downloaded-gh-artifacts"
    passing_path = artifact_root / "job-a" / "packaging-baseline.json"
    passing_path.parent.mkdir(parents=True)
    passing_path.write_text(
        json.dumps(
            baseline_payload(
                tmp_path / "job-a",
                baseline_contract_ok=True,
                warnings=[],
                failures=[],
            )
        ),
        encoding="utf-8",
    )
    drift_path = artifact_root / "job-b" / "nested" / "packaging-baseline.json"
    drift_path.parent.mkdir(parents=True)
    drift_path.write_text(
        json.dumps(
            baseline_payload(
                tmp_path / "job-b",
                baseline_contract_ok=False,
                warnings=["Blocked capture did not report failed_step."],
                failures=[
                    "Packaging baseline requirement failed: Blocked capture did not report failed_step."
                ],
            )
        ),
        encoding="utf-8",
    )

    rc = cli.main(
        ["packaging-baseline-report", "--json", "--require-contract-ok", str(artifact_root)]
    )

    captured = capsys.readouterr()
    assert rc == 2
    report = json.loads(captured.out)
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
    assert report["warnings"] == [f"{drift_path.resolve()}: Blocked capture did not report failed_step."]
    assert [artifact["artifact_path"] for artifact in report["artifacts"]] == [
        str(passing_path.resolve()),
        str(drift_path.resolve()),
    ]
    assert (
        f"{drift_path.resolve()}: Packaging baseline requirement failed: "
        "Blocked capture did not report failed_step."
    ) in captured.err


def test_cli_version_flag(capsys):
    with pytest.raises(SystemExit) as excinfo:
        cli.main(["--version"])

    assert excinfo.value.code == 0
    assert capsys.readouterr().out.strip() == f"resource-hunter {__version__}"
