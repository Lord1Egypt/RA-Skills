from __future__ import annotations

from pathlib import Path

from research_mode_finalization import inspect_candidate_artifacts
from research_mode_payloads import normalize_output_contract
from research_mode_utils import ValidationError

from .helpers import json_out, run


def _assert_validation_error(fn, expected: str) -> None:
    try:
        fn()
    except ValidationError as exc:
        assert expected in str(exc)
    else:
        raise AssertionError("expected ValidationError")


def test_output_contract_accepts_open_media_type() -> None:
    contract = normalize_output_contract(
        {
            "outputs": [
                {
                    "id": "report",
                    "role": "primary_deliverable",
                    "required": True,
                    "media_type": "application/x-vendor-custom-report",
                }
            ]
        }
    )

    assert contract["outputs"] == [
        {
            "id": "report",
            "role": "primary_deliverable",
            "required": True,
            "media_type": "application/x-vendor-custom-report",
        }
    ]


def test_output_contract_supports_multiple_required_outputs() -> None:
    contract = normalize_output_contract(
        {
            "outputs": [
                {
                    "id": "report",
                    "role": "primary_deliverable",
                    "media_type": "application/pdf",
                },
                {
                    "id": "sources",
                    "role": "supporting_deliverable",
                    "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                },
            ]
        }
    )

    assert [item["id"] for item in contract["outputs"]] == ["report", "sources"]
    assert all(item["required"] is True for item in contract["outputs"])


def test_output_contract_rejects_unsafe_output_id() -> None:
    _assert_validation_error(
        lambda: normalize_output_contract(
            {"outputs": [{"id": "../report", "role": "primary_deliverable"}]}
        ),
        "output id",
    )


def test_output_contract_rejects_duplicate_output_ids() -> None:
    _assert_validation_error(
        lambda: normalize_output_contract(
            {
                "outputs": [
                    {"id": "report", "role": "primary_deliverable"},
                    {"id": "report", "role": "supporting_deliverable"},
                ]
            }
        ),
        "duplicate output id",
    )


def test_output_contract_parses_required_false() -> None:
    contract = normalize_output_contract(
        {
            "outputs": [
                {"id": "report", "role": "primary_deliverable"},
                {
                    "id": "appendix",
                    "role": "supporting_deliverable",
                    "required": False,
                },
            ]
        }
    )

    assert contract["outputs"][1]["required"] is False


def test_output_contract_rejects_multiple_primary_outputs() -> None:
    _assert_validation_error(
        lambda: normalize_output_contract(
            {
                "outputs": [
                    {"id": "report", "role": "primary_deliverable"},
                    {"id": "appendix", "role": "primary_deliverable"},
                ]
            }
        ),
        "exactly one primary_deliverable",
    )


def test_output_contract_keeps_legacy_kind_but_prefers_outputs() -> None:
    contract = normalize_output_contract(
        {
            "kind": "pdf_report",
            "outputs": [
                {
                    "id": "report",
                    "role": "primary_deliverable",
                    "media_type": "application/pdf",
                }
            ],
        }
    )

    assert contract["kind"] == "pdf_report"
    assert contract["outputs"][0]["id"] == "report"


def test_output_contract_preserves_open_relation_fields() -> None:
    contract = normalize_output_contract(
        {
            "outputs": [
                {
                    "id": "report_pdf",
                    "role": "primary_deliverable",
                    "derived_from": "report_source",
                },
                {
                    "id": "report_source",
                    "role": "supporting_artifact",
                    "source_for": "report_pdf",
                },
            ]
        }
    )

    assert contract["outputs"][0]["derived_from"] == "report_source"
    assert contract["outputs"][1]["source_for"] == "report_pdf"


def test_create_accepts_repeatable_output_specs(root) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "multi-output-cli",
            "--goal",
            "Prepare report and source workbook",
            "--output",
            "id=report,role=primary_deliverable,media_type=application/pdf",
            "--output",
            "id=sources,role=supporting_deliverable,media_type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    )

    outputs = created["working_memory"]["output_contract"]["outputs"]
    assert [item["id"] for item in outputs] == ["report", "sources"]


def test_structured_output_guidance_does_not_require_legacy_kind(root) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "structured-guidance-no-legacy-kind",
            "--goal",
            "Prepare report and source workbook",
            "--output",
            "id=report,role=primary_deliverable,media_type=application/pdf",
            "--output",
            "id=sources,role=supporting_deliverable,media_type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "--skip-preflight",
        )
    )

    lease = json_out(
        run(
            "begin",
            "--root",
            str(root),
            "--id",
            "structured-guidance-no-legacy-kind",
        )
    )
    guidance = "\n".join(lease.get("finalization_guidance") or [])

    assert "output_contract.outputs" in guidance
    assert "primary deliverable kind" not in guidance


def test_set_deliverable_accepts_output_spec(root) -> None:
    run("create", "--root", str(root), "--id", "set-output-cli", "--goal", "Prepare report")

    updated = json_out(
        run(
            "set-deliverable",
            "--root",
            str(root),
            "--id",
            "set-output-cli",
            "--output",
            "id=report,role=primary_deliverable,media_type=application/pdf",
        )
    )

    assert updated["working_memory"]["output_contract"]["outputs"][0]["id"] == "report"


def test_candidate_artifacts_satisfy_required_outputs(tmp_path: Path) -> None:
    task_dir = tmp_path / "task"
    output_dir = task_dir / "workspace" / "outputs"
    output_dir.mkdir(parents=True)
    (output_dir / "report.pdf").write_bytes(b"%PDF-1.7\n")
    (output_dir / "sources.xlsx").write_bytes(
        b"source,url\nexample,https://example.com\n"
    )

    result = inspect_candidate_artifacts(
        task_dir=task_dir,
        final_report_path=task_dir / "final-report.md",
        report_markdown="",
        finalization={
            "candidate_artifacts": [
                {
                    "id": "report",
                    "path": "workspace/outputs/report.pdf",
                    "role": "primary_deliverable",
                    "media_type": "application/pdf",
                },
                {
                    "id": "sources",
                    "path": "workspace/outputs/sources.xlsx",
                    "role": "supporting_deliverable",
                    "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                },
            ]
        },
        output_contract={
            "outputs": [
                {
                    "id": "report",
                    "role": "primary_deliverable",
                    "media_type": "application/pdf",
                },
                {
                    "id": "sources",
                    "role": "supporting_deliverable",
                    "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                },
            ]
        },
    )

    assert result["passed"] is True
    assert result["reasons"] == []


def test_candidate_artifacts_do_not_use_extension_mapping(tmp_path: Path) -> None:
    task_dir = tmp_path / "task"
    output_dir = task_dir / "workspace" / "outputs"
    output_dir.mkdir(parents=True)
    (output_dir / "report.custom").write_bytes(b"readable")

    result = inspect_candidate_artifacts(
        task_dir=task_dir,
        final_report_path=task_dir / "final-report.md",
        report_markdown="",
        finalization={
            "candidate_artifacts": [
                {
                    "id": "report",
                    "path": "workspace/outputs/report.custom",
                    "role": "primary_deliverable",
                    "media_type": "application/pdf",
                }
            ]
        },
        output_contract={
            "outputs": [
                {
                    "id": "report",
                    "role": "primary_deliverable",
                    "media_type": "application/pdf",
                }
            ]
        },
    )

    assert result["passed"] is True


def test_candidate_artifact_missing_declared_media_type_fails(tmp_path: Path) -> None:
    task_dir = tmp_path / "task"
    output_dir = task_dir / "workspace" / "outputs"
    output_dir.mkdir(parents=True)
    (output_dir / "report.pdf").write_bytes(b"%PDF-1.7\n")

    result = inspect_candidate_artifacts(
        task_dir=task_dir,
        final_report_path=task_dir / "final-report.md",
        report_markdown="",
        finalization={
            "candidate_artifacts": [
                {
                    "id": "report",
                    "path": "workspace/outputs/report.pdf",
                    "role": "primary_deliverable",
                }
            ]
        },
        output_contract={
            "outputs": [
                {
                    "id": "report",
                    "role": "primary_deliverable",
                    "media_type": "application/pdf",
                }
            ]
        },
    )

    assert "candidate_artifact_media_type_missing:report" in result["reasons"]


def test_candidate_artifact_relations_are_checked_by_id(tmp_path: Path) -> None:
    task_dir = tmp_path / "task"
    output_dir = task_dir / "workspace" / "outputs"
    output_dir.mkdir(parents=True)
    (output_dir / "report.pdf").write_bytes(b"%PDF-1.7\n")
    (output_dir / "report.md").write_text("# Report\n", encoding="utf-8")

    result = inspect_candidate_artifacts(
        task_dir=task_dir,
        final_report_path=task_dir / "final-report.md",
        report_markdown="",
        finalization={
            "candidate_artifacts": [
                {
                    "id": "report_pdf",
                    "path": "workspace/outputs/report.pdf",
                    "role": "primary_deliverable",
                    "media_type": "application/pdf",
                    "derived_from": "report_source",
                },
                {
                    "id": "report_source",
                    "path": "workspace/outputs/report.md",
                    "role": "supporting_artifact",
                    "media_type": "text/markdown",
                    "source_for": "report_pdf",
                },
            ]
        },
        output_contract={
            "outputs": [
                {
                    "id": "report_pdf",
                    "role": "primary_deliverable",
                    "media_type": "application/pdf",
                    "derived_from": "report_source",
                },
                {
                    "id": "report_source",
                    "role": "supporting_artifact",
                    "media_type": "text/markdown",
                    "source_for": "report_pdf",
                },
            ]
        },
    )

    assert result["passed"] is True
    assert result["reasons"] == []


def test_internal_artifact_can_be_relation_target_without_delivery_output(
    tmp_path: Path,
) -> None:
    task_dir = tmp_path / "task"
    output_dir = task_dir / "workspace" / "outputs"
    output_dir.mkdir(parents=True)
    (output_dir / "report.pdf").write_bytes(b"%PDF-1.7\n")
    (output_dir / "report.html").write_text("<h1>Report</h1>\n", encoding="utf-8")

    result = inspect_candidate_artifacts(
        task_dir=task_dir,
        final_report_path=task_dir / "final-report.md",
        report_markdown="",
        finalization={
            "candidate_artifacts": [
                {
                    "id": "report_pdf",
                    "path": "workspace/outputs/report.pdf",
                    "role": "primary_deliverable",
                    "derived_from": "report_html",
                }
            ],
            "internal_artifacts": [
                {
                    "id": "report_html",
                    "path": "workspace/outputs/report.html",
                    "role": "supporting_artifact",
                    "visibility": "internal",
                }
            ],
        },
        output_contract={
            "outputs": [
                {
                    "id": "report_pdf",
                    "role": "primary_deliverable",
                    "derived_from": "report_html",
                }
            ]
        },
    )

    assert result["passed"] is True
    assert result["reasons"] == []


def test_candidate_artifact_relation_target_must_exist(tmp_path: Path) -> None:
    task_dir = tmp_path / "task"
    output_dir = task_dir / "workspace" / "outputs"
    output_dir.mkdir(parents=True)
    (output_dir / "report.pdf").write_bytes(b"%PDF-1.7\n")

    result = inspect_candidate_artifacts(
        task_dir=task_dir,
        final_report_path=task_dir / "final-report.md",
        report_markdown="",
        finalization={
            "candidate_artifacts": [
                {
                    "id": "report_pdf",
                    "path": "workspace/outputs/report.pdf",
                    "role": "primary_deliverable",
                    "derived_from": "missing_source",
                }
            ]
        },
        output_contract={
            "outputs": [
                {
                    "id": "report_pdf",
                    "role": "primary_deliverable",
                    "derived_from": "missing_source",
                }
            ]
        },
    )

    assert result["passed"] is False
    assert (
        "candidate_artifact_relation_target_missing:report_pdf:derived_from:missing_source"
        in result["reasons"]
    )


def test_candidate_artifact_relations_are_not_inferred_from_extensions(
    tmp_path: Path,
) -> None:
    task_dir = tmp_path / "task"
    output_dir = task_dir / "workspace" / "outputs"
    output_dir.mkdir(parents=True)
    (output_dir / "report.pdf").write_bytes(b"%PDF-1.7\n")
    (output_dir / "report.md").write_text("# Report\n", encoding="utf-8")

    result = inspect_candidate_artifacts(
        task_dir=task_dir,
        final_report_path=task_dir / "final-report.md",
        report_markdown="",
        finalization={
            "candidate_artifacts": [
                {
                    "id": "report_pdf",
                    "path": "workspace/outputs/report.pdf",
                    "role": "primary_deliverable",
                },
                {
                    "id": "report_source",
                    "path": "workspace/outputs/report.md",
                    "role": "supporting_artifact",
                },
            ]
        },
        output_contract={
            "outputs": [
                {
                    "id": "report_pdf",
                    "role": "primary_deliverable",
                    "derived_from": "report_source",
                },
                {
                    "id": "report_source",
                    "role": "supporting_artifact",
                    "source_for": "report_pdf",
                },
            ]
        },
    )

    assert result["passed"] is False
    assert "candidate_artifact_derived_from_missing:report_pdf" in result["reasons"]
    assert "candidate_artifact_source_for_missing:report_source" in result["reasons"]


def test_output_decision_takes_priority_over_legacy_primary_kind() -> None:
    from research_mode_finalization import build_output_decision

    decision = build_output_decision(
        output_contract={
            "outputs": [
                {
                    "id": "report",
                    "role": "primary_deliverable",
                    "media_type": "application/pdf",
                },
                {"id": "sources", "role": "supporting_deliverable", "required": True},
            ]
        },
        finalization={"primary_deliverable_kind": "markdown_report"},
    )

    assert decision == {
        "source": "output_contract",
        "selected_output_id": "report",
        "primary_output_id": "report",
        "required_output_ids": ["report", "sources"],
        "reason": "Structured output contract declares reviewable outputs.",
    }
