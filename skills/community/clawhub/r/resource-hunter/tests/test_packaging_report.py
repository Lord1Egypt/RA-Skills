from __future__ import annotations

import json
import sys
import zipfile

import pytest

from resource_hunter.errors import ResourceHunterError
from resource_hunter.packaging_report import (
    PACKAGING_BASELINE_REPORT_SCHEMA_VERSION,
    build_packaging_baseline_report,
    format_packaging_baseline_report_text,
    load_packaging_baseline_payload,
    packaging_baseline_report_requirement_failures,
    read_packaging_baseline_report,
    read_packaging_baseline_reports,
    resolve_packaging_baseline_artifact_paths,
)


def _baseline_payload(tmp_path):
    return {
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
            "strategy": "missing-python",
            "strategy_family": "blocked",
            "reason": "Python executable was not found.",
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


def _apply_passing_capture_probe_error_drift(payload, *, packaging_error: str):
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
    return payload


def _apply_passing_capture_legacy_reason_probe_error_drift(payload, *, packaging_error: str):
    payload = _apply_passing_capture_probe_error_drift(payload, packaging_error=packaging_error)
    payload["passing_capture"]["reason"] = f"Packaging smoke is blocked: {packaging_error}"
    payload["passing_capture"].pop("doctor", None)
    payload["passing_capture"].pop("packaging_smoke", None)
    return payload


def _write_baseline_artifact(artifact_path, payload):
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(payload), encoding="utf-8")
    return artifact_path


def _write_baseline_archive(archive_path, members):
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path, "w") as archive:
        if hasattr(members, "rglob"):
            for artifact_path in sorted(members.rglob("packaging-baseline.json")):
                archive.write(artifact_path, arcname=artifact_path.relative_to(members).as_posix())
        else:
            for member_name, payload in members.items():
                archive.writestr(member_name, json.dumps(payload))
    return archive_path


def test_build_packaging_baseline_report_normalizes_artifact(tmp_path):
    payload = _baseline_payload(tmp_path)

    report = build_packaging_baseline_report(payload, artifact_path=tmp_path / "packaging-baseline.json")

    assert report["report_schema_version"] == PACKAGING_BASELINE_REPORT_SCHEMA_VERSION
    assert report["report_type"] == "single"
    assert report["artifact_name"] == tmp_path.name
    assert report["status"] == "ok"
    assert report["requirement_failure_count"] == 0
    assert report["capture_diagnostic_count"] == 0
    assert report["summary"]["baseline_contract_ok"] is True
    assert [capture["name"] for capture in report["captures"]] == ["passing", "blocked"]
    assert report["captures"][0]["actual"] == {
        "doctor_packaging_ready": True,
        "packaging_smoke_ok": True,
        "failed_step": None,
        "strategy_family": "usable",
        "strategy": "prefix-install",
        "reason": "Packaging smoke passed.",
    }
    assert report["captures"][1]["expected_outcome"]["strategy_family_any_of"] == ["blocked"]


def test_build_packaging_baseline_report_preserves_capture_diagnostics(tmp_path):
    payload = _apply_passing_capture_probe_error_drift(
        _baseline_payload(tmp_path),
        packaging_error=(
            "Unable to inspect packaging modules via /opt/python/3.10/bin/python: "
            "Traceback ...\nAssertionError: /opt/python/3.10/lib/python3.10/distutils/core.py"
        ),
    )

    report = build_packaging_baseline_report(payload, artifact_path=tmp_path / "packaging-baseline.json")

    assert report["status"] == "drift"
    assert report["requirement_failure_count"] == 1
    assert report["capture_diagnostic_count"] == 1
    assert report["capture_diagnostics"] == [
        {
            "artifact_path": str((tmp_path / "packaging-baseline.json").resolve()),
            "artifact_label": tmp_path.name,
            "artifact_display_label": tmp_path.name,
            "capture_name": "passing",
            "capture_label": "Passing",
            "packaging_python": sys.executable,
            "failed_step": "packaging-status",
            "strategy_family": "blocked",
            "strategy": "blocked",
            "reason": "Packaging smoke is blocked: Unable to inspect packaging modules.",
            "packaging_error": (
                "Unable to inspect packaging modules via /opt/python/3.10/bin/python: "
                "Traceback ...\nAssertionError: /opt/python/3.10/lib/python3.10/distutils/core.py"
            ),
            "bootstrap_build_requirements": ["setuptools>=69", "wheel"],
            "bootstrap_build_deps_ready": False,
            "packaging_smoke_ready_with_bootstrap": False,
        }
    ]
    assert report["captures"][0]["diagnostics"] == {
        "packaging_error": (
            "Unable to inspect packaging modules via /opt/python/3.10/bin/python: "
            "Traceback ...\nAssertionError: /opt/python/3.10/lib/python3.10/distutils/core.py"
        ),
        "bootstrap_build_requirements": ["setuptools>=69", "wheel"],
        "bootstrap_build_deps_ready": False,
        "packaging_smoke_ready_with_bootstrap": False,
    }


def test_build_packaging_baseline_report_infers_traceback_diagnostics_from_reason_only(tmp_path):
    packaging_error = (
        "Unable to inspect packaging modules via /opt/python/3.10/bin/python: "
        "Traceback ...\nAssertionError: /opt/python/3.10/lib/python3.10/distutils/core.py"
    )
    payload = _apply_passing_capture_legacy_reason_probe_error_drift(
        _baseline_payload(tmp_path),
        packaging_error=packaging_error,
    )

    report = build_packaging_baseline_report(payload, artifact_path=tmp_path / "packaging-baseline.json")

    assert report["capture_diagnostics"] == [
        {
            "artifact_path": str((tmp_path / "packaging-baseline.json").resolve()),
            "artifact_label": tmp_path.name,
            "artifact_display_label": tmp_path.name,
            "capture_name": "passing",
            "capture_label": "Passing",
            "packaging_python": sys.executable,
            "failed_step": "packaging-status",
            "strategy_family": "blocked",
            "strategy": "blocked",
            "reason": "Packaging smoke is blocked: Unable to inspect packaging modules.",
            "packaging_error": packaging_error,
        }
    ]
    assert report["captures"][0]["diagnostics"] == {
        "packaging_error": packaging_error,
    }


def test_read_packaging_baseline_report_reads_archive_from_disk(tmp_path):
    artifact_path = tmp_path / "packaging-baseline.json"
    artifact_path.write_text(json.dumps(_baseline_payload(tmp_path)), encoding="utf-8")

    report = read_packaging_baseline_report(artifact_path)

    assert report["artifact_path"] == str(artifact_path.resolve())
    assert report["captures"][1]["matches_expectation"] is True
    assert report["requirements"] == {
        "require_expected_outcomes": True,
        "ok": True,
        "failures": [],
    }


def test_read_packaging_baseline_report_reads_single_zip_member(tmp_path):
    archive_path = _write_baseline_archive(
        tmp_path / "resource-hunter-packaging-baseline.zip",
        {"windows/job-a/packaging-baseline.json": _baseline_payload(tmp_path / "job-a")},
    )

    report = read_packaging_baseline_report(archive_path)

    assert report["artifact_path"] == (
        f"{archive_path.resolve()}!/windows/job-a/packaging-baseline.json"
    )
    assert report["summary"]["baseline_contract_ok"] is True


def test_read_packaging_baseline_report_rejects_multi_member_zip_for_single_report(tmp_path):
    archive_path = _write_baseline_archive(
        tmp_path / "resource-hunter-packaging-baseline.zip",
        {
            "job-a/packaging-baseline.json": _baseline_payload(tmp_path / "job-a"),
            "job-b/packaging-baseline.json": _baseline_payload(tmp_path / "job-b"),
        },
    )

    with pytest.raises(ResourceHunterError, match="contains 2 packaging-baseline.json artifacts"):
        read_packaging_baseline_report(archive_path)


def test_load_packaging_baseline_payload_rejects_missing_capture_entries(tmp_path):
    artifact_path = tmp_path / "packaging-baseline.json"
    artifact_path.write_text(json.dumps({"schema_version": 1, "passing_capture": {}}), encoding="utf-8")

    with pytest.raises(ResourceHunterError, match="does not contain passing_capture and blocked_capture entries"):
        load_packaging_baseline_payload(artifact_path)


def test_resolve_packaging_baseline_artifact_paths_expands_directories(tmp_path):
    artifact_root = tmp_path / "downloaded-gh-artifacts"
    artifact_path = _write_baseline_artifact(
        artifact_root / "job-a" / "packaging-baseline.json",
        _baseline_payload(tmp_path / "job-a"),
    )
    nested_path = _write_baseline_artifact(
        artifact_root / "job-b" / "nested" / "packaging-baseline.json",
        _baseline_payload(tmp_path / "job-b"),
    )

    resolved = resolve_packaging_baseline_artifact_paths([artifact_path, artifact_root])

    assert resolved == [artifact_path.resolve(), nested_path.resolve()]


def test_resolve_packaging_baseline_artifact_paths_expands_zip_archives(tmp_path):
    artifact_root = tmp_path / "downloaded-gh-artifacts"
    _write_baseline_artifact(
        artifact_root / "job-a" / "packaging-baseline.json",
        _baseline_payload(tmp_path / "job-a"),
    )
    _write_baseline_artifact(
        artifact_root / "job-b" / "nested" / "packaging-baseline.json",
        _baseline_payload(tmp_path / "job-b"),
    )
    archive_path = _write_baseline_archive(tmp_path / "downloaded-gh-artifacts.zip", artifact_root)

    resolved = resolve_packaging_baseline_artifact_paths([archive_path])

    assert resolved == [
        f"{archive_path.resolve()}!/job-a/packaging-baseline.json",
        f"{archive_path.resolve()}!/job-b/nested/packaging-baseline.json",
    ]


def test_resolve_packaging_baseline_artifact_paths_expands_zip_archives_under_directories(tmp_path):
    downloads_root = tmp_path / "downloaded-gh-artifact-zips"
    archive_path = _write_baseline_archive(
        downloads_root / "nested" / "downloaded-gh-artifacts.zip",
        {
            "job-a/packaging-baseline.json": _baseline_payload(tmp_path / "job-a"),
            "job-b/nested/packaging-baseline.json": _baseline_payload(tmp_path / "job-b"),
        },
    )

    resolved = resolve_packaging_baseline_artifact_paths([downloads_root])

    assert resolved == [
        f"{archive_path.resolve()}!/job-a/packaging-baseline.json",
        f"{archive_path.resolve()}!/job-b/nested/packaging-baseline.json",
    ]


def test_read_packaging_baseline_report_reads_explicit_zip_member(tmp_path):
    artifact_root = tmp_path / "downloaded-gh-artifacts"
    nested_project_root = tmp_path / "job-b"
    _write_baseline_artifact(
        artifact_root / "job-a" / "packaging-baseline.json",
        _baseline_payload(tmp_path / "job-a"),
    )
    nested_path = _write_baseline_artifact(
        artifact_root / "job-b" / "nested" / "packaging-baseline.json",
        _baseline_payload(nested_project_root),
    )
    archive_path = _write_baseline_archive(tmp_path / "downloaded-gh-artifacts.zip", artifact_root)

    report = read_packaging_baseline_report(f"{archive_path.resolve()}!/job-b/nested/packaging-baseline.json")

    assert report["artifact_path"] == f"{archive_path.resolve()}!/job-b/nested/packaging-baseline.json"
    assert report["output_dir"] == str(nested_project_root)
    assert nested_path.parent.name == "nested"
    assert report["captures"][1]["matches_expectation"] is True


def test_read_packaging_baseline_reports_aggregates_multiple_artifacts(tmp_path):
    artifact_root = tmp_path / "downloaded-gh-artifacts"
    passing_path = _write_baseline_artifact(
        artifact_root / "job-a" / "packaging-baseline.json",
        _baseline_payload(tmp_path / "job-a"),
    )
    drift_payload = _baseline_payload(tmp_path / "job-b")
    drift_payload["blocked_capture"]["matches_expectation"] = False
    drift_payload["blocked_capture"]["expectation_drift"] = [
        {
            "capture": "blocked",
            "field": "failed_step",
            "kind": "missing_failed_step",
            "expected_present": True,
            "actual": None,
            "message": "Blocked capture did not report failed_step.",
        }
    ]
    drift_payload["summary"] = {
        "passing_capture_matches_expectation": True,
        "blocked_capture_matches_expectation": False,
        "baseline_contract_ok": False,
    }
    drift_payload["warnings"] = ["Blocked capture did not report failed_step."]
    drift_payload["requirements"] = {
        "require_expected_outcomes": True,
        "ok": False,
        "failures": [
            "Packaging baseline requirement failed: Blocked capture did not report failed_step."
        ],
    }
    drift_path = _write_baseline_artifact(
        artifact_root / "job-b" / "nested" / "packaging-baseline.json",
        drift_payload,
    )

    report = read_packaging_baseline_reports([artifact_root])

    assert report["report_schema_version"] == PACKAGING_BASELINE_REPORT_SCHEMA_VERSION
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
    assert report["artifact_statuses"] == [
        {
            "artifact_path": str(passing_path.resolve()),
            "artifact_name": "job-a",
            "status": "ok",
            "baseline_contract_ok": True,
            "requirement_failure_count": 0,
            "capture_diagnostic_count": 0,
        },
        {
            "artifact_path": str(drift_path.resolve()),
            "artifact_name": "nested",
            "status": "drift",
            "baseline_contract_ok": False,
            "requirement_failure_count": 1,
            "capture_diagnostic_count": 1,
        },
    ]
    assert report["requirement_failure_groups"] == [
        {
            "message": "Blocked capture did not report failed_step.",
            "artifact_count": 1,
            "artifact_labels": ["nested"],
            "artifact_display_labels": ["nested"],
            "artifact_paths": [str(drift_path.resolve())],
        }
    ]
    assert report["warnings"] == [f"{drift_path.resolve()}: Blocked capture did not report failed_step."]
    assert [artifact["artifact_path"] for artifact in report["artifacts"]] == [
        str(passing_path.resolve()),
        str(drift_path.resolve()),
    ]
    assert packaging_baseline_report_requirement_failures(report) == [
        (
            f"{drift_path.resolve()}: Packaging baseline requirement failed: "
            "Blocked capture did not report failed_step."
        )
    ]


def test_read_packaging_baseline_reports_aggregates_multiple_zip_artifacts(tmp_path):
    artifact_root = tmp_path / "downloaded-gh-artifacts"
    _write_baseline_artifact(
        artifact_root / "job-a" / "packaging-baseline.json",
        _baseline_payload(tmp_path / "job-a"),
    )
    drift_payload = _baseline_payload(tmp_path / "job-b")
    drift_payload["blocked_capture"]["matches_expectation"] = False
    drift_payload["blocked_capture"]["expectation_drift"] = [
        {
            "capture": "blocked",
            "field": "failed_step",
            "kind": "missing_failed_step",
            "expected_present": True,
            "actual": None,
            "message": "Blocked capture did not report failed_step.",
        }
    ]
    drift_payload["summary"] = {
        "passing_capture_matches_expectation": True,
        "blocked_capture_matches_expectation": False,
        "baseline_contract_ok": False,
    }
    drift_payload["warnings"] = ["Blocked capture did not report failed_step."]
    drift_payload["requirements"] = {
        "require_expected_outcomes": True,
        "ok": False,
        "failures": [
            "Packaging baseline requirement failed: Blocked capture did not report failed_step."
        ],
    }
    _write_baseline_artifact(
        artifact_root / "job-b" / "nested" / "packaging-baseline.json",
        drift_payload,
    )
    archive_path = _write_baseline_archive(tmp_path / "downloaded-gh-artifacts.zip", artifact_root)

    report = read_packaging_baseline_reports([archive_path])

    drift_ref = f"{archive_path.resolve()}!/job-b/nested/packaging-baseline.json"
    assert report["report_schema_version"] == PACKAGING_BASELINE_REPORT_SCHEMA_VERSION
    assert report["report_type"] == "aggregate"
    assert report["summary"] == {
        "artifact_count": 2,
        "contract_ok_artifact_count": 1,
        "contract_drift_artifact_count": 1,
        "requirement_failed_artifact_count": 1,
        "warning_count": 1,
        "all_baseline_contracts_ok": False,
    }
    assert report["artifacts_with_contract_drift"] == [drift_ref]
    assert report["artifacts_with_requirement_failures"] == [drift_ref]
    assert report["warnings"] == [f"{drift_ref}: Blocked capture did not report failed_step."]
    assert [artifact["artifact_path"] for artifact in report["artifacts"]] == [
        f"{archive_path.resolve()}!/job-a/packaging-baseline.json",
        drift_ref,
    ]


def test_read_packaging_baseline_reports_aggregates_zip_members(tmp_path):
    archive_path = tmp_path / "downloaded-gh-artifacts.zip"
    drift_payload = _baseline_payload(tmp_path / "job-b")
    drift_payload["blocked_capture"]["matches_expectation"] = False
    drift_payload["blocked_capture"]["expectation_drift"] = [
        {
            "capture": "blocked",
            "field": "failed_step",
            "kind": "missing_failed_step",
            "expected_present": True,
            "actual": None,
            "message": "Blocked capture did not report failed_step.",
        }
    ]
    drift_payload["summary"] = {
        "passing_capture_matches_expectation": True,
        "blocked_capture_matches_expectation": False,
        "baseline_contract_ok": False,
    }
    drift_payload["warnings"] = ["Blocked capture did not report failed_step."]
    drift_payload["requirements"] = {
        "require_expected_outcomes": True,
        "ok": False,
        "failures": [
            "Packaging baseline requirement failed: Blocked capture did not report failed_step."
        ],
    }
    _write_baseline_archive(
        archive_path,
        {
            "job-a/packaging-baseline.json": _baseline_payload(tmp_path / "job-a"),
            "job-b/nested/packaging-baseline.json": drift_payload,
        },
    )

    report = read_packaging_baseline_reports([archive_path])

    assert report["report_type"] == "aggregate"
    assert report["summary"] == {
        "artifact_count": 2,
        "contract_ok_artifact_count": 1,
        "contract_drift_artifact_count": 1,
        "requirement_failed_artifact_count": 1,
        "warning_count": 1,
        "all_baseline_contracts_ok": False,
    }
    assert report["artifacts_with_contract_drift"] == [
        f"{archive_path.resolve()}!/job-b/nested/packaging-baseline.json"
    ]
    assert report["artifacts_with_requirement_failures"] == [
        f"{archive_path.resolve()}!/job-b/nested/packaging-baseline.json"
    ]


def test_format_packaging_baseline_report_text_groups_repeated_requirement_failures(tmp_path):
    artifact_root = tmp_path / "downloaded-gh-artifacts"
    for artifact_name in (
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.10",
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.11",
    ):
        drift_payload = _baseline_payload(tmp_path / artifact_name)
        drift_payload["blocked_capture"]["matches_expectation"] = False
        drift_payload["blocked_capture"]["expectation_drift"] = [
            {
                "capture": "blocked",
                "field": "failed_step",
                "kind": "missing_failed_step",
                "expected_present": True,
                "actual": None,
                "message": "Blocked capture did not report failed_step.",
            }
        ]
        drift_payload["summary"] = {
            "passing_capture_matches_expectation": True,
            "blocked_capture_matches_expectation": False,
            "baseline_contract_ok": False,
        }
        drift_payload["warnings"] = ["Blocked capture did not report failed_step."]
        drift_payload["requirements"] = {
            "require_expected_outcomes": True,
            "ok": False,
            "failures": [
                "Packaging baseline requirement failed: Blocked capture did not report failed_step."
            ],
        }
        _write_baseline_artifact(
            artifact_root / artifact_name / "packaging-baseline.json",
            drift_payload,
        )

    report = read_packaging_baseline_reports([artifact_root])

    assert report["requirement_failure_groups"][0]["artifact_display_labels"] == [
        "ubuntu-latest / py3.10",
        "ubuntu-latest / py3.11",
    ]

    text = format_packaging_baseline_report_text(report)

    assert "Requirement failure groups:" in text
    assert (
        "- Blocked capture did not report failed_step. "
        "(2 artifacts: ubuntu-latest / py3.10, ubuntu-latest / py3.11)" in text
    )


def test_format_packaging_baseline_report_text_includes_drift_diagnostics(tmp_path):
    artifact_root = tmp_path / "downloaded-gh-artifacts"
    payload_310 = _apply_passing_capture_probe_error_drift(
        _baseline_payload(tmp_path / "resource-hunter-packaging-baseline-ubuntu-latest-py3.10"),
        packaging_error=(
            "Unable to inspect packaging modules via /opt/python/3.10/bin/python: "
            "Traceback ...\nAssertionError: /opt/python/3.10/lib/python3.10/distutils/core.py"
        ),
    )
    payload_311 = _apply_passing_capture_probe_error_drift(
        _baseline_payload(tmp_path / "resource-hunter-packaging-baseline-ubuntu-latest-py3.11"),
        packaging_error=(
            "Unable to inspect packaging modules via /opt/python/3.11/bin/python: "
            "Traceback ...\nAssertionError: /opt/python/3.11/lib/python3.11/distutils/core.py"
        ),
    )
    _write_baseline_artifact(
        artifact_root / "resource-hunter-packaging-baseline-ubuntu-latest-py3.10" / "packaging-baseline.json",
        payload_310,
    )
    _write_baseline_artifact(
        artifact_root / "resource-hunter-packaging-baseline-ubuntu-latest-py3.11" / "packaging-baseline.json",
        payload_311,
    )

    report = read_packaging_baseline_reports([artifact_root])

    assert len(report["capture_diagnostic_groups"]) == 1
    assert report["capture_diagnostic_groups"][0]["artifact_count"] == 2
    assert report["capture_diagnostic_groups"][0]["artifact_labels"] == [
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.10",
        "resource-hunter-packaging-baseline-ubuntu-latest-py3.11",
    ]
    assert report["capture_diagnostic_groups"][0]["artifact_display_labels"] == [
        "ubuntu-latest / py3.10",
        "ubuntu-latest / py3.11",
    ]
    assert report["capture_diagnostic_groups"][0]["packaging_error_signature"] == "AssertionError: */distutils/core.py"
    assert report["capture_diagnostic_groups"][0]["packaging_error_summary_count"] == 2

    text = format_packaging_baseline_report_text(report)

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


def test_format_packaging_baseline_report_text_groups_legacy_reason_only_drift_diagnostics(tmp_path):
    artifact_root = tmp_path / "downloaded-gh-artifacts"
    payload_310 = _apply_passing_capture_legacy_reason_probe_error_drift(
        _baseline_payload(tmp_path / "resource-hunter-packaging-baseline-ubuntu-latest-py3.10"),
        packaging_error=(
            "Unable to inspect packaging modules via /opt/python/3.10/bin/python: "
            "Traceback ...\nAssertionError: /opt/python/3.10/lib/python3.10/distutils/core.py"
        ),
    )
    payload_311 = _apply_passing_capture_legacy_reason_probe_error_drift(
        _baseline_payload(tmp_path / "resource-hunter-packaging-baseline-ubuntu-latest-py3.11"),
        packaging_error=(
            "Unable to inspect packaging modules via /opt/python/3.11/bin/python: "
            "Traceback ...\nAssertionError: /opt/python/3.11/lib/python3.11/distutils/core.py"
        ),
    )
    _write_baseline_artifact(
        artifact_root / "resource-hunter-packaging-baseline-ubuntu-latest-py3.10" / "packaging-baseline.json",
        payload_310,
    )
    _write_baseline_artifact(
        artifact_root / "resource-hunter-packaging-baseline-ubuntu-latest-py3.11" / "packaging-baseline.json",
        payload_311,
    )

    report = read_packaging_baseline_reports([artifact_root])

    assert len(report["capture_diagnostic_groups"]) == 1
    assert report["capture_diagnostic_groups"][0]["artifact_count"] == 2
    assert report["capture_diagnostic_groups"][0]["reason"] == (
        "Packaging smoke is blocked: Unable to inspect packaging modules."
    )
    assert report["capture_diagnostic_groups"][0]["artifact_display_labels"] == [
        "ubuntu-latest / py3.10",
        "ubuntu-latest / py3.11",
    ]
    assert report["capture_diagnostic_groups"][0]["packaging_error_signature"] == "AssertionError: */distutils/core.py"
    assert report["capture_diagnostic_groups"][0]["packaging_error_summary_count"] == 2

    text = format_packaging_baseline_report_text(report)

    assert "Drift diagnostic groups:" in text
    assert (
        "- Passing: failed_step=packaging-status; strategy_family=blocked; strategy=blocked; "
        "reason=Packaging smoke is blocked: Unable to inspect packaging modules.; "
        "packaging_error=AssertionError: */distutils/core.py (2 variants) "
        "(2 artifacts: ubuntu-latest / py3.10, ubuntu-latest / py3.11)" in text
    )
