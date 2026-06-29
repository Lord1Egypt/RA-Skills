"""Delivery manifest: population, mark-delivered, primary file validation."""
from __future__ import annotations

import json
import zipfile
from pathlib import Path

from .helpers import (
    assert_eq,
    assert_in,
    assert_true,
    finish_to_awaiting_review,
    finish_preflight_if_needed,
    human_ready_adequacy,
    json_out,
    run,
)
from research_mode_reporting import refresh_task_playbook
from research_mode_task import ResearchTask


_HUMAN_READY_FINALIZATION = {
    "status": "passed",
    "inferred_user_need": "A readable result that can be reviewed without reconstructing it from internal artifacts.",
    "intended_recipient": "operator",
    "primary_deliverable_kind": "markdown_report",
    "internal_artifacts": [
        {"path": "iterations/001.md", "kind": "iteration_notes", "note": "Internal iteration notes."}
    ],
    "candidate_artifacts": [
        {"path": "final-report.md", "kind": "markdown_report", "note": "Human-readable final report."}
    ],
    "blocking_defects": [],
    "nonblocking_defects": [],
    "revisions": [
        {"summary": "Converted synthesis notes into a reader-facing final report."}
    ],
    "validation_evidence": [
        {"kind": "markdown_review", "summary": "Checked headings, summary, findings, and conclusion."}
    ],
}


def _finish_with_payload(root: Path, task_id: str, lease: dict, payload: dict) -> dict:
    lease = finish_preflight_if_needed(root, task_id, lease)
    result_file = Path(lease["paths"]["result_file"])
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    finished = json_out(
        run(
            "finish",
            "--root",
            str(root),
            "--id",
            task_id,
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result_file),
        )
    )
    if finished.get("status") != "idle":
        return finished

    verify_lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    if verify_lease.get("phase") != "verify":
        return finished
    verify_result = Path(verify_lease["paths"]["result_file"])
    verify_result.write_text(
        json.dumps(
            {
                "summary": "Research adequacy passed.",
                "next_angle": "Prepare the final deliverable.",
                "meaningful_progress": True,
                "phase": "verify",
                "open_questions": [],
                "sources": [],
                "findings": [],
                "notify_recommendation": "silent",
                "should_complete": False,
                "final_report_markdown": None,
                "adequacy": human_ready_adequacy(),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    routed = json_out(
        run(
            "finish",
            "--root",
            str(root),
            "--id",
            task_id,
            "--run-id",
            verify_lease["run_id"],
            "--result-file",
            str(verify_result),
        )
    )
    if routed.get("status") != "idle":
        return routed

    finalize_lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    final_payload = dict(payload)
    final_payload["phase"] = "finalize"
    finalize_result = Path(finalize_lease["paths"]["result_file"])
    finalize_result.write_text(
        json.dumps(final_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return json_out(
        run(
            "finish",
            "--root",
            str(root),
            "--id",
            task_id,
            "--run-id",
            finalize_lease["run_id"],
            "--result-file",
            str(finalize_result),
        )
    )


def _final_payload(finalization: dict | None = None) -> dict:
    payload = {
        "summary": "Research completed.",
        "next_angle": "",
        "meaningful_progress": True,
        "phase": "synthesize",
        "open_questions": [],
        "sources": [{"title": "src"}],
        "findings": [{"kind": "fact", "text": "finding"}],
        "notify_recommendation": "final",
        "should_complete": True,
        "final_report_markdown": (
            "# Final Report\n\n"
            "## Summary\n\n"
            "This is a comprehensive final report prepared as a readable deliverable. "
            "It summarizes the result, explains the evidence, and avoids exposing raw internal fields.\n\n"
            "## Key Findings\n\n"
            "- Finding 1: Important discovery supported by evidence.\n"
            "- Finding 2: Another key insight from the research.\n\n"
            "## Conclusion\n\n"
            "The result is ready for operator review."
        ),
    }
    if finalization is not None:
        payload["finalization"] = finalization
    return payload


def _write_minimal_xlsx(path: Path, *, sheet_name: str = "Сводка") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as workbook:
        workbook.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>
""",
        )
        workbook.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
""",
        )
        workbook.writestr(
            "xl/workbook.xml",
            f"""<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="{sheet_name}" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>
""",
        )
        workbook.writestr(
            "xl/_rels/workbook.xml.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>
""",
        )
        workbook.writestr(
            "xl/worksheets/sheet1.xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    <row r="1"><c r="A1" t="inlineStr"><is><t>Итог</t></is></c></row>
  </sheetData>
</worksheet>
""",
        )


def _write_conflicting_filter_xlsx(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as workbook:
        workbook.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/tables/table1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.table+xml"/>
</Types>
""",
        )
        workbook.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
""",
        )
        workbook.writestr(
            "xl/workbook.xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets><sheet name="Data" sheetId="1" r:id="rId1"/></sheets>
</workbook>
""",
        )
        workbook.writestr(
            "xl/_rels/workbook.xml.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>
""",
        )
        workbook.writestr(
            "xl/worksheets/sheet1.xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheetData>
    <row r="1"><c r="A1" t="inlineStr"><is><t>Name</t></is></c><c r="B1" t="inlineStr"><is><t>Value</t></is></c></row>
    <row r="2"><c r="A2" t="inlineStr"><is><t>A</t></is></c><c r="B2"><v>1</v></c></row>
  </sheetData>
  <autoFilter ref="A1:B2"/>
  <tableParts count="1"><tablePart r:id="rId1"/></tableParts>
</worksheet>
""",
        )
        workbook.writestr(
            "xl/worksheets/_rels/sheet1.xml.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/table" Target="../tables/table1.xml"/>
</Relationships>
""",
        )
        workbook.writestr(
            "xl/tables/table1.xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<table xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" id="1" name="Table1" displayName="Table1" ref="A1:B2">
  <autoFilter ref="A1:B2"/>
  <tableColumns count="2"><tableColumn id="1" name="Name"/><tableColumn id="2" name="Value"/></tableColumns>
</table>
""",
        )


def test_initial_state_has_explicit_finalization_defaults(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "finalization-defaults",
            "--goal",
            "Finalization defaults test",
        )
    )
    state = json.loads((root / "finalization-defaults" / "state.json").read_text(encoding="utf-8"))
    finalization = state.get("finalization") or {}
    assert_eq(
        finalization.get("status"),
        "not_started",
        "new tasks should start with explicit finalization.not_started",
    )
    assert_eq(
        finalization.get("max_attempts"),
        3,
        "new tasks should preserve the bounded finalization loop default",
    )
    assert_true(
        isinstance(finalization.get("validation_evidence"), list),
        "new tasks should expose validation_evidence as a list",
    )


def test_worker_final_without_finalization_trace_enters_finalize(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "finalization-missing-trace",
            "--goal",
            "Missing finalization trace test",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "finalization-missing-trace"))
    finished = _finish_with_payload(root, "finalization-missing-trace", lease, _final_payload())

    assert_eq(
        finished.get("status"),
        "finalize",
        "worker final without finalization trace should enter finalize rather than awaiting_review",
    )
    reasons = finished.get("finalization_validation", {}).get("reasons") or []
    assert_in(
        "finalization_not_started",
        reasons,
        "validation should explain that finalization trace was missing",
    )


def test_worker_final_rejects_raw_artifact_exposed_as_final(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "raw-artifact-final",
            "--goal",
            "Check client base and prepare the final spreadsheet",
            "--deliverable",
            "usable spreadsheet for a manager",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "raw-artifact-final"))
    raw_finalization = {
        **_HUMAN_READY_FINALIZATION,
        "primary_deliverable_kind": "xlsx",
        "candidate_artifacts": [
            {
                "path": "workspace/outputs/client_check_raw.xlsx",
                "kind": "xlsx",
                "visibility": "internal",
                "role": "primary",
                "note": "Working workbook is not ready for review.",
            }
        ],
        "validation_evidence": [
            {"kind": "manifest_review", "summary": "Only confirmed that the raw workbook exists."}
        ],
    }
    finished = _finish_with_payload(
        root,
        "raw-artifact-final",
        lease,
        _final_payload(raw_finalization),
    )

    assert_eq(
        finished.get("status"),
        "finalize",
        "raw working artifact should not pass as a review-ready deliverable",
    )
    reasons = finished.get("finalization_validation", {}).get("reasons") or []
    assert_in(
        "raw_artifact_exposed_as_final",
        reasons,
        "validation should identify raw artifact exposure",
    )


def test_candidate_note_with_word_draft_does_not_fail_when_artifact_is_valid(root: Path) -> None:
    from research_mode_lifecycle_helpers import _check_finalization_trace

    finalization = {
        "status": "passed",
        "inferred_user_need": "Readable result for review.",
        "intended_recipient": "operator",
        "primary_deliverable_kind": "markdown_report",
        "internal_artifacts": [],
        "candidate_artifacts": [
            {
                "path": "final-report.md",
                "kind": "markdown_report",
                "visibility": "user_facing",
                "role": "primary",
                "note": "Earlier draft wording was reviewed and removed.",
            }
        ],
        "blocking_defects": [],
        "validation_evidence": [
            {"kind": "manual_review", "summary": "Reviewed final artifact."}
        ],
    }

    result = _check_finalization_trace(
        finalization, "# Report\n\nFinal readable report text."
    )

    assert_eq(
        result.get("passed"),
        True,
        "word draft in note must not fail structural validation",
    )
    assert_true(
        "raw_artifact_exposed_as_final" not in (result.get("reasons") or []),
        "raw/final decision must not scan note text",
    )


def test_internal_visibility_candidate_is_rejected_as_final(root: Path) -> None:
    from research_mode_lifecycle_helpers import _check_finalization_trace

    finalization = {
        "status": "passed",
        "inferred_user_need": "Readable result for review.",
        "intended_recipient": "operator",
        "primary_deliverable_kind": "markdown_report",
        "internal_artifacts": [],
        "candidate_artifacts": [
            {
                "path": "final-report.md",
                "kind": "markdown_report",
                "visibility": "internal",
                "role": "primary",
                "note": "No forbidden words needed.",
            }
        ],
        "blocking_defects": [],
        "validation_evidence": [
            {"kind": "manual_review", "summary": "Reviewed final artifact."}
        ],
    }

    result = _check_finalization_trace(
        finalization, "# Report\n\nFinal readable report text."
    )

    assert_eq(result.get("passed"), False, "internal candidate cannot be final")
    assert_in(
        "raw_artifact_exposed_as_final",
        result.get("reasons") or [],
        "internal visibility reason",
    )


def test_worker_final_with_human_ready_finalization_trace_reaches_review(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "human-ready-trace",
            "--goal",
            "Human-ready finalization trace test",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "human-ready-trace"))
    finished = _finish_with_payload(
        root,
        "human-ready-trace",
        lease,
        _final_payload(_HUMAN_READY_FINALIZATION),
    )
    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "human-ready finalization trace should allow awaiting_review",
    )
    state = json.loads((root / "human-ready-trace" / "state.json").read_text(encoding="utf-8"))
    assert_eq(
        (state.get("finalization") or {}).get("status"),
        "passed",
        "state should persist passed finalization trace",
    )
    summary = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            "human-ready-trace",
            "--format",
            "json",
        )
    )
    fin = summary.get("finalization") or {}
    assert_eq(
        fin.get("inferred_user_need"),
        _HUMAN_READY_FINALIZATION["inferred_user_need"],
        "summary should expose inferred user need",
    )
    assert_eq(
        fin.get("primary_deliverable_kind"),
        "markdown_report",
        "summary should expose primary deliverable kind",
    )
    assert_eq(
        fin.get("candidate_artifacts_count"),
        1,
        "summary should count candidate artifacts",
    )
    assert_eq(
        fin.get("validation_evidence_count"),
        1,
        "summary should count validation evidence",
    )
    summary_text = run(
        "summary",
        "--root",
        str(root),
        "--id",
        "human-ready-trace",
        "--format",
        "text",
    ).stdout
    assert_in(
        "Finalization need:",
        summary_text,
        "summary text should expose finalization need",
    )
    assert_in(
        "Primary deliverable: markdown_report",
        summary_text,
        "summary text should expose primary deliverable kind",
    )
    playbook = (root / "human-ready-trace" / "task-playbook.md").read_text(encoding="utf-8")
    assert_in(
        "Inferred user need",
        playbook,
        "playbook should expose inferred user need",
    )
    assert_in(
        "Validation evidence",
        playbook,
        "playbook should expose validation evidence",
    )


def test_worker_final_rejects_missing_candidate_artifact(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "missing-candidate-artifact",
            "--goal",
            "Missing candidate artifact test",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "missing-candidate-artifact"))
    finalization = {
        **_HUMAN_READY_FINALIZATION,
        "primary_deliverable_kind": "markdown_report",
        "candidate_artifacts": [
            {
                "path": "reports/missing-final.md",
                "kind": "markdown_report",
                "note": "Expected review-ready report.",
            }
        ],
    }
    finished = _finish_with_payload(
        root,
        "missing-candidate-artifact",
        lease,
        _final_payload(finalization),
    )
    assert_eq(
        finished.get("status"),
        "finalize",
        "missing candidate artifact should route to finalize",
    )
    reasons = finished.get("finalization_validation", {}).get("reasons") or []
    assert_in(
        "candidate_artifact_missing",
        reasons,
        "missing candidate artifact should be explicit",
    )


def test_worker_final_inspects_existing_markdown_candidate_artifact(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "markdown-candidate-artifact",
            "--goal",
            "Markdown candidate artifact test",
        )
    )
    task_dir = root / "markdown-candidate-artifact"
    reports_dir = task_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "final.md").write_text(
        "# Final Report\n\n"
        "## Summary\n\n"
        "This markdown report is a human-facing deliverable with enough content to be inspected. "
        "It is not an internal iteration log and it gives the reviewer a clear summary.\n",
        encoding="utf-8",
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "markdown-candidate-artifact"))
    finalization = {
        **_HUMAN_READY_FINALIZATION,
        "primary_deliverable_kind": "markdown_report",
        "candidate_artifacts": [
            {
                "path": "reports/final.md",
                "kind": "markdown_report",
                "note": "Review-ready Markdown report.",
            }
        ],
    }
    finished = _finish_with_payload(
        root,
        "markdown-candidate-artifact",
        lease,
        _final_payload(finalization),
    )
    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "existing markdown candidate artifact should pass inspection",
    )
    findings = finished.get("finalization_validation", {}).get("findings") or []
    artifact_finding = next(
        (item for item in findings if item.get("check") == "candidate_artifact_inspection"),
        {},
    )
    assert_true(
        artifact_finding.get("passed"),
        "candidate artifact inspection should pass for readable markdown",
    )
    inspected = artifact_finding.get("artifacts") or []
    assert_true(
        any(item.get("path") == "reports/final.md" for item in inspected),
        "inspection finding should list the checked markdown artifact",
    )


def test_worker_final_rejects_pdf_kind_with_markdown_candidate(root: Path) -> None:
    task_id = "pdf-kind-markdown-candidate"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "PDF deliverable should not silently hand off Markdown.",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    finalization = {
        **_HUMAN_READY_FINALIZATION,
        "primary_deliverable_kind": "pdf_report",
        "candidate_artifacts": [
            {
                "path": "final-report.md",
                "kind": "markdown_report",
                "note": "Markdown source, not the requested PDF.",
            }
        ],
    }

    finished = _finish_with_payload(root, task_id, lease, _final_payload(finalization))

    assert_eq(
        finished.get("status"),
        "finalize",
        "PDF finalization should not reach review with only Markdown candidate",
    )
    reasons = finished.get("finalization_validation", {}).get("reasons") or []
    assert_in(
        "primary_deliverable_format_mismatch",
        reasons,
        "format mismatch should be explicit",
    )
    decision_finding = next(
        (
            item
            for item in finished.get("finalization_validation", {}).get("findings") or []
            if item.get("check") == "deliverable_format_decision"
        ),
        {},
    )
    assert_true(
        not decision_finding.get("passed"),
        "format decision should not pass when declared PDF only has Markdown",
    )
    assert_eq(
        decision_finding.get("desired_kind"),
        "pdf_report",
        "declared PDF should remain the desired deliverable kind",
    )
    assert_eq(
        decision_finding.get("feasible_kind"),
        "markdown_report",
        "actual Markdown candidate should be the feasible worker output",
    )
    assert_eq(
        decision_finding.get("source"),
        "declared",
        "declared primary kind should be distinguished from inferred defaults",
    )
    assert_in(
        "declared_deliverable_format_mismatch",
        decision_finding.get("reasons") or [],
        "format decision should carry the declared/actual mismatch reason",
    )


def test_worker_final_accepts_pdf_primary_with_supporting_markdown(root: Path) -> None:
    task_id = "pdf-primary-with-markdown-support"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "PDF deliverable with editable Markdown companion.",
            "--deliverable",
            "PDF report with supporting Markdown",
            "--skip-preflight",
        )
    )
    task_dir = root / task_id
    report_dir = task_dir / "workspace" / "outputs"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "final.pdf").write_bytes(b"%PDF-1.7\n% test pdf\n")
    (report_dir / "final.md").write_text(
        "# Final Report\n\n"
        "## Summary\n\n"
        "This readable Markdown companion mirrors the primary PDF report and is "
        "kept only as an editable supporting artifact for reviewers.\n",
        encoding="utf-8",
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    finalization = {
        **_HUMAN_READY_FINALIZATION,
        "primary_deliverable_kind": "pdf_report",
        "candidate_artifacts": [
            {
                "path": "workspace/outputs/final.pdf",
                "kind": "final_pdf_report",
                "note": "Primary human-facing PDF report.",
            },
            {
                "path": "workspace/outputs/final.md",
                "kind": "final_markdown_report",
                "note": "Editable Markdown companion.",
            },
        ],
    }

    finished = _finish_with_payload(root, task_id, lease, _final_payload(finalization))

    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "primary PDF candidate should pass even when Markdown companion is present",
    )
    findings = finished.get("finalization_validation", {}).get("findings") or []
    artifact_finding = next(
        (item for item in findings if item.get("check") == "candidate_artifact_inspection"),
        {},
    )
    assert_true(
        artifact_finding.get("passed"),
        "candidate inspection should accept at least one matching primary PDF",
    )
    decision_finding = next(
        (
            item
            for item in findings
            if item.get("check") == "deliverable_format_decision"
        ),
        {},
    )
    assert_eq(
        decision_finding.get("feasible_kind"),
        "pdf_report",
        "format decision should prefer the matching primary PDF over companions",
    )
    reasons = finished.get("finalization_validation", {}).get("reasons") or []
    assert_true(
        "raw_artifact_exposed_as_final" not in reasons,
        "final report artifacts under workspace/outputs should not be treated as raw",
    )
    state = json.loads((root / task_id / "state.json").read_text(encoding="utf-8"))
    delivery = state.get("delivery") or {}
    assert_eq(
        delivery.get("primary_file"),
        str(report_dir / "final.pdf"),
        "delivery.primary_file should hand off the validated primary PDF candidate",
    )


def test_worker_final_tolerates_string_deliverable_decision_note(root: Path) -> None:
    task_id = "string-deliverable-decision-note"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "PDF finalization should tolerate worker notes in optional decision field.",
            "--deliverable",
            "PDF report",
            "--skip-preflight",
        )
    )
    task_dir = root / task_id
    report_dir = task_dir / "workspace" / "outputs"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "final.pdf").write_bytes(b"%PDF-1.7\n% test pdf\n")
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    finalization = {
        **_HUMAN_READY_FINALIZATION,
        "primary_deliverable_kind": "pdf_report",
        "deliverable_decision": "Use the generated PDF as the primary artifact.",
        "candidate_artifacts": [
            {
                "path": "workspace/outputs/final.pdf",
                "kind": "final_pdf_report",
                "note": "Primary human-facing PDF report.",
            }
        ],
    }

    finished = _finish_with_payload(root, task_id, lease, _final_payload(finalization))

    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "string worker note in deliverable_decision should not make finish fail",
    )
    state = json.loads((root / task_id / "state.json").read_text(encoding="utf-8"))
    decision = (state.get("finalization") or {}).get("deliverable_decision") or {}
    assert_eq(
        decision.get("selected_kind"),
        "pdf_report",
        "validator-computed deliverable decision should replace worker note",
    )


def test_worker_final_does_not_infer_pdf_for_long_chat_report(root: Path) -> None:
    task_id = "no-inferred-pdf-chat-report"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Prepare a long narrative report for a Mattermost thread.",
            "--skip-preflight",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    finalization = {
        **_HUMAN_READY_FINALIZATION,
        "inferred_user_need": "Long narrative report delivered in a chat thread.",
        "intended_recipient": "Mattermost thread",
        "primary_deliverable_kind": "markdown_report",
        "candidate_artifacts": [
            {
                "path": "final-report.md",
                "kind": "markdown_report",
                "note": "Markdown source prepared by the worker.",
            }
        ],
    }

    finished = _finish_with_payload(root, task_id, lease, _final_payload(finalization))

    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "free text alone should not force a PDF artifact before review",
    )
    decision_finding = next(
        (
            item
            for item in finished.get("finalization_validation", {}).get("findings") or []
            if item.get("check") == "deliverable_format_decision"
        ),
        {},
    )
    assert_eq(
        decision_finding.get("desired_kind"),
        "markdown_report",
        "declared Markdown should remain the desired kind",
    )
    assert_eq(
        decision_finding.get("feasible_kind"),
        "markdown_report",
        "Markdown remains the feasible worker output",
    )
    assert_eq(
        decision_finding.get("source"),
        "declared",
        "free text should not be recorded as an inferred format source",
    )


def test_worker_final_preserves_explicit_markdown_format(root: Path) -> None:
    task_id = "explicit-markdown-chat-report"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Prepare a report in the requested format.",
            "--deliverable",
            "Markdown report for a Mattermost thread",
            "--skip-preflight",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    finalization = {
        **_HUMAN_READY_FINALIZATION,
        "inferred_user_need": "Markdown report delivered in a chat thread.",
        "intended_recipient": "Mattermost thread",
        "primary_deliverable_kind": "markdown_report",
        "candidate_artifacts": [
            {
                "path": "final-report.md",
                "kind": "markdown_report",
                "note": "Explicitly requested Markdown report.",
            }
        ],
    }

    finished = _finish_with_payload(root, task_id, lease, _final_payload(finalization))

    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "explicit Markdown request should preserve Markdown as user-facing output",
    )
    state = json.loads((root / task_id / "state.json").read_text(encoding="utf-8"))
    decision = (state.get("finalization") or {}).get("deliverable_decision") or {}
    assert_eq(
        decision.get("source"),
        "declared",
        "format decision should come from structured finalization kind",
    )
    assert_eq(
        decision.get("selected_kind"),
        "markdown_report",
        "explicit Markdown should remain the selected deliverable kind",
    )


def test_worker_final_inspects_xlsx_candidate_sheet_names(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "xlsx-candidate-artifact",
            "--goal",
            "XLSX candidate artifact test",
            "--deliverable-kind",
            "xlsx",
            "--deliverable",
            "review-ready spreadsheet",
        )
    )
    task_dir = root / "xlsx-candidate-artifact"
    _write_minimal_xlsx(task_dir / "reports" / "final.xlsx", sheet_name="Сводка")
    lease = json_out(run("begin", "--root", str(root), "--id", "xlsx-candidate-artifact"))
    finalization = {
        **_HUMAN_READY_FINALIZATION,
        "primary_deliverable_kind": "xlsx",
        "candidate_artifacts": [
            {
                "path": "reports/final.xlsx",
                "kind": "xlsx",
                "note": "Review-ready workbook.",
            }
        ],
    }
    finished = _finish_with_payload(
        root,
        "xlsx-candidate-artifact",
        lease,
        _final_payload(finalization),
    )
    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "valid XLSX candidate artifact should pass inspection",
    )
    findings = finished.get("finalization_validation", {}).get("findings") or []
    artifact_finding = next(
        (item for item in findings if item.get("check") == "candidate_artifact_inspection"),
        {},
    )
    inspected = artifact_finding.get("artifacts") or []
    xlsx_artifact = next(
        (item for item in inspected if item.get("path") == "reports/final.xlsx"),
        {},
    )
    assert_eq(xlsx_artifact.get("format"), "xlsx", "XLSX inspection should expose format")
    assert_eq(xlsx_artifact.get("sheet_count"), 1, "XLSX inspection should count sheets")
    assert_eq(
        xlsx_artifact.get("sheet_names"),
        ["Сводка"],
        "XLSX inspection should expose sheet names",
    )


def test_worker_final_structured_outputs_handoff_without_legacy_format_mismatch(root: Path) -> None:
    task_id = "structured-output-finish-handoff"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Prepare a PDF report and source workbook.",
            "--output",
            "id=report,role=primary_deliverable,media_type=application/pdf",
            "--output",
            "id=sources,role=supporting_deliverable,media_type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "--skip-preflight",
        )
    )
    task_dir = root / task_id
    outputs_dir = task_dir / "workspace" / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    (outputs_dir / "report.pdf").write_bytes(b"%PDF-1.7\nstructured report\n")
    _write_minimal_xlsx(outputs_dir / "sources.xlsx")

    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    finalization = {
        **_HUMAN_READY_FINALIZATION,
        "primary_deliverable_kind": "pdf_report",
        "candidate_artifacts": [
            {
                "id": "report",
                "path": "workspace/outputs/report.pdf",
                "role": "primary_deliverable",
                "media_type": "application/pdf",
                "visibility": "user_facing",
            },
            {
                "id": "sources",
                "path": "workspace/outputs/sources.xlsx",
                "role": "supporting_deliverable",
                "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "visibility": "user_facing",
            },
        ],
    }

    finished = _finish_with_payload(root, task_id, lease, _final_payload(finalization))

    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "structured outputs should pass finalization and enter review",
    )
    findings = finished.get("finalization_validation", {}).get("findings") or []
    format_decision = next(
        (
            item
            for item in findings
            if item.get("check") == "deliverable_format_decision"
        ),
        {},
    )
    assert_eq(
        format_decision.get("reasons"),
        [],
        "structured outputs should not fail legacy format decision",
    )
    state = json.loads((task_dir / "state.json").read_text(encoding="utf-8"))
    delivery = state.get("delivery") or {}
    assert_eq(
        delivery.get("primary_file"),
        str(outputs_dir / "report.pdf"),
        "primary_file should point at the primary structured output",
    )
    assert_eq(
        [item.get("id") for item in delivery.get("outputs") or []],
        ["report", "sources"],
        "delivery.outputs should retain structured outputs",
    )
    assert_eq(
        delivery.get("attachments"),
        [str(outputs_dir / "sources.xlsx")],
        "supporting output should become an attachment",
    )


def test_worker_final_xlsx_output_does_not_require_legacy_kind_or_long_wrapper(root: Path) -> None:
    task_id = "structured-xlsx-finish-handoff"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Prepare a formatted Excel company profile.",
            "--output",
            "id=company_workbook,role=primary_deliverable,media_type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "--skip-preflight",
        )
    )
    task_dir = root / task_id
    outputs_dir = task_dir / "workspace" / "outputs"
    workbook_path = outputs_dir / "company-profile.xlsx"
    _write_minimal_xlsx(workbook_path)

    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    finalization = {
        **_HUMAN_READY_FINALIZATION,
        "primary_deliverable_kind": "Excel workbook (.xlsx)",
        "candidate_artifacts": [
            {
                "id": "company_workbook",
                "path": "workspace/outputs/company-profile.xlsx",
                "role": "primary",
                "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "visibility": "user_facing",
            }
        ],
    }
    payload = _final_payload(finalization)
    payload["final_report_markdown"] = (
        "# Workbook wrapper\n\n"
        "The review-ready Excel workbook is the primary deliverable for this task. "
        "This wrapper only records the handoff context; workbook content, source "
        "provenance, formatting, and validation evidence live in the XLSX artifact."
    )

    finished = _finish_with_payload(root, task_id, lease, payload)

    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "valid structured XLSX output should not be blocked by legacy kind or wrapper length",
    )
    findings = finished.get("finalization_validation", {}).get("findings") or []
    failed = [item for item in findings if not item.get("passed")]
    assert_eq(failed, [], "structured XLSX finalization should have no failed checks")
    state = json.loads((task_dir / "state.json").read_text(encoding="utf-8"))
    assert_eq(
        state.get("delivery", {}).get("primary_file"),
        str(workbook_path),
        "delivery.primary_file should point at the XLSX workbook",
    )


def test_structured_outputs_do_not_require_legacy_primary_kind(root: Path) -> None:
    task_id = "structured-output-no-legacy-kind"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Prepare a PDF report and source workbook.",
            "--output",
            "id=report,role=primary_deliverable,media_type=application/pdf",
            "--output",
            "id=sources,role=supporting_deliverable,media_type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "--skip-preflight",
        )
    )
    task_dir = root / task_id
    outputs_dir = task_dir / "workspace" / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    (outputs_dir / "report.pdf").write_bytes(b"%PDF-1.7\nstructured report\n")
    _write_minimal_xlsx(outputs_dir / "sources.xlsx")

    finalization = {
        key: value
        for key, value in _HUMAN_READY_FINALIZATION.items()
        if key not in {"primary_deliverable_kind", "deliverable_decision"}
    }
    finalization["candidate_artifacts"] = [
        {
            "id": "report",
            "path": "workspace/outputs/report.pdf",
            "role": "primary_deliverable",
            "media_type": "application/pdf",
            "visibility": "user_facing",
        },
        {
            "id": "sources",
            "path": "workspace/outputs/sources.xlsx",
            "role": "supporting_deliverable",
            "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "visibility": "user_facing",
        },
    ]

    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    finished = _finish_with_payload(root, task_id, lease, _final_payload(finalization))

    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "structured outputs should not need legacy primary_deliverable_kind",
    )
    finalization_trace = next(
        (
            item
            for item in finished.get("finalization_validation", {}).get("findings") or []
            if item.get("check") == "finalization_trace"
        ),
        {},
    )
    assert_eq(
        finalization_trace.get("reasons"),
        [],
        "structured output contract should satisfy finalization trace without legacy kind",
    )


def test_approve_defaults_to_delivery_primary_file_for_structured_outputs(root: Path) -> None:
    task_id = "structured-output-approve-primary"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Prepare a formatted Excel company profile.",
            "--output",
            "id=company_workbook,role=primary_deliverable,media_type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "--skip-preflight",
        )
    )
    task_dir = root / task_id
    workbook_path = task_dir / "workspace" / "outputs" / "company-profile.xlsx"
    _write_minimal_xlsx(workbook_path)

    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    finalization = {
        **_HUMAN_READY_FINALIZATION,
        "candidate_artifacts": [
            {
                "id": "company_workbook",
                "path": "workspace/outputs/company-profile.xlsx",
                "role": "primary_deliverable",
                "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "visibility": "user_facing",
            }
        ],
    }
    payload = _final_payload(finalization)
    payload["final_report_markdown"] = (
        "# Workbook wrapper\n\n"
        "The XLSX file is the reviewable deliverable; this markdown is only handoff context."
    )
    finished = _finish_with_payload(root, task_id, lease, payload)
    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "structured workbook task should wait for review",
    )

    approved = json_out(
        run(
            "approve",
            "--root",
            str(root),
            "--id",
            task_id,
            "--feedback",
            "Workbook approved.",
        )
    )

    assert_eq(
        approved.get("approved_artifact_path"),
        str(workbook_path),
        "approve should default to delivery.primary_file for structured outputs",
    )
    state = json.loads((task_dir / "state.json").read_text(encoding="utf-8"))
    assert_eq(
        state.get("review", {}).get("approved_artifact_path"),
        str(workbook_path),
        "review state should record the actual workbook as approved artifact",
    )


def test_delivery_ready_missing_primary_file_sets_operator_attention(root: Path) -> None:
    task_id = "delivery-ready-missing-primary"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Delivery ready state should surface missing primary file.",
            "--skip-preflight",
        )
    )
    state_path = root / task_id / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["delivery"] = {
        "ready": True,
        "review_ready": True,
        "primary_file": "reports/missing.pdf",
    }
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = json_out(run("summary", "--root", str(root), "--id", task_id, "--format", "json"))
    attention = summary.get("operator_attention") or {}
    assert_eq(
        attention.get("status"),
        "manual_review_needed",
        "missing delivery primary file should require operator attention",
    )
    assert_true(
        any(
            item.get("code") == "delivery_artifact_handoff_failed"
            for item in attention.get("conditions") or []
        ),
        "operator attention should expose delivery_artifact_handoff_failed",
    )


def test_delivery_ready_relative_primary_file_resolves_under_task(root: Path) -> None:
    task_id = "delivery-ready-relative-primary"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Legacy relative primary file should still be valid.",
            "--skip-preflight",
        )
    )
    task_dir = root / task_id
    reports_dir = task_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "final.pdf").write_bytes(b"%PDF-1.7\n% test pdf\n")
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {"status": "pending", "review_gated": True}
    state["delivery"] = {
        "review_ready": True,
        "ready": True,
        "primary_file": "reports/final.pdf",
    }
    state["artifacts"]["final_report_path"] = None
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    health = json_out(run("health", "--root", str(root), "--id", task_id, "--format", "json"))
    codes = [item.get("code") for item in health.get("findings") or []]
    assert_true(
        "missing_reviewable_artifact" not in codes,
        "relative primary_file should satisfy awaiting_review artifact check",
    )
    assert_true(
        "delivery_ready_but_missing_primary" not in codes,
        "relative primary_file should satisfy delivery.ready artifact check",
    )


def test_awaiting_review_candidate_without_primary_file_sets_handoff_attention(root: Path) -> None:
    task_id = "review-candidate-no-primary"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Review-ready candidate should have a delivery primary file.",
            "--skip-preflight",
        )
    )
    task_dir = root / task_id
    reports_dir = task_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "final.pdf").write_text("dummy pdf", encoding="utf-8")
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {"status": "pending", "review_gated": True}
    state["finalization"] = {
        **_HUMAN_READY_FINALIZATION,
        "status": "passed",
        "primary_deliverable_kind": "pdf_report",
        "candidate_artifacts": [
            {
                "path": "reports/final.pdf",
                "kind": "pdf_report",
                "note": "Review-ready PDF candidate.",
            }
        ],
        "last_validation_findings": [
            {
                "check": "candidate_artifact_inspection",
                "passed": True,
                "reasons": [],
                "artifacts": [
                    {
                        "path": "reports/final.pdf",
                        "kind": "pdf_report",
                        "exists": True,
                        "inside_task": True,
                        "is_file": True,
                        "format": "pdf",
                        "reasons": [],
                    },
                    {
                        "path": "final-report.md",
                        "kind": "markdown_report",
                        "exists": True,
                        "inside_task": True,
                        "is_file": True,
                        "format": "markdown",
                        "reasons": [],
                    },
                ],
            }
        ],
    }
    state["delivery"] = {
        "review_ready": True,
        "ready": False,
        "primary_file": None,
    }
    state["artifacts"]["final_report_path"] = None
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = json_out(run("summary", "--root", str(root), "--id", task_id, "--format", "json"))
    attention = summary.get("operator_attention") or {}
    assert_true(
        any(
            item.get("code") == "delivery_artifact_handoff_failed"
            for item in attention.get("conditions") or []
        ),
        "awaiting_review without delivery primary should surface handoff failure",
    )

    task = ResearchTask(task_dir)
    refresh_task_playbook(task)
    playbook = (task_dir / "task-playbook.md").read_text(encoding="utf-8")
    assert_in(
        "delivery_artifact_handoff_failed",
        playbook,
        "task playbook should show delivery handoff warning",
    )


def test_awaiting_review_primary_file_mismatch_sets_handoff_attention(root: Path) -> None:
    task_id = "review-primary-file-mismatch"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Review-ready PDF task should not hand off Markdown as primary.",
            "--skip-preflight",
        )
    )
    task_dir = root / task_id
    reports_dir = task_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = reports_dir / "final.pdf"
    markdown_path = task_dir / "final-report.md"
    pdf_path.write_bytes(b"%PDF-1.7\n% test pdf\n")
    markdown_path.write_text("# Final Report\n\nSupporting source.\n", encoding="utf-8")
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {"status": "pending", "review_gated": True}
    state["finalization"] = {
        **_HUMAN_READY_FINALIZATION,
        "status": "passed",
        "primary_deliverable_kind": "pdf_report",
        "candidate_artifacts": [
            {
                "path": "reports/final.pdf",
                "kind": "pdf_report",
                "note": "Review-ready PDF candidate.",
            }
        ],
        "last_validation_findings": [
            {
                "check": "candidate_artifact_inspection",
                "passed": True,
                "reasons": [],
                "artifacts": [
                    {
                        "path": "reports/final.pdf",
                        "kind": "pdf_report",
                        "exists": True,
                        "inside_task": True,
                        "is_file": True,
                        "format": "pdf",
                        "reasons": [],
                    },
                    {
                        "path": "final-report.md",
                        "kind": "markdown_report",
                        "exists": True,
                        "inside_task": True,
                        "is_file": True,
                        "format": "markdown",
                        "reasons": [],
                    },
                ],
            }
        ],
    }
    state["delivery"] = {
        "review_ready": True,
        "ready": False,
        "primary_file": str(markdown_path),
    }
    state["artifacts"]["final_report_path"] = str(markdown_path)
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = json_out(run("summary", "--root", str(root), "--id", task_id, "--format", "json"))
    attention = summary.get("operator_attention") or {}
    assert_true(
        any(
            item.get("code") == "delivery_artifact_handoff_failed"
            for item in attention.get("conditions") or []
        ),
        "awaiting_review PDF task with Markdown primary_file should surface handoff failure",
    )


def test_awaiting_review_primary_file_mismatch_requires_artifact_inspection(
    root: Path,
) -> None:
    task_id = "review-primary-file-mismatch-no-inspection"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Legacy review-ready state should not invent handoff mismatch evidence.",
            "--skip-preflight",
        )
    )
    task_dir = root / task_id
    reports_dir = task_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = reports_dir / "final.pdf"
    markdown_path = task_dir / "final-report.md"
    pdf_path.write_bytes(b"%PDF-1.7\n% test pdf\n")
    markdown_path.write_text("# Final Report\n\nSupporting source.\n", encoding="utf-8")
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {"status": "pending", "review_gated": True}
    state["finalization"] = {
        **_HUMAN_READY_FINALIZATION,
        "status": "passed",
        "primary_deliverable_kind": "pdf_report",
        "candidate_artifacts": [
            {
                "path": "reports/final.pdf",
                "kind": "pdf_report",
                "note": "Review-ready PDF candidate.",
            }
        ],
        "last_validation_findings": [],
    }
    state["delivery"] = {
        "review_ready": True,
        "ready": False,
        "primary_file": str(markdown_path),
    }
    state["artifacts"]["final_report_path"] = str(markdown_path)
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = json_out(run("summary", "--root", str(root), "--id", task_id, "--format", "json"))
    attention = summary.get("operator_attention") or {}
    assert_true(
        not any(
            item.get("code") == "delivery_artifact_handoff_failed"
            for item in attention.get("conditions") or []
        ),
        "handoff mismatch warning should require validated candidate_artifact_inspection evidence",
    )


def test_worker_final_rejects_xlsx_table_autofilter_conflict(root: Path) -> None:
    task_id = "xlsx-filter-conflict"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "XLSX filter conflict test",
            "--deliverable",
            "review-ready spreadsheet",
        )
    )
    task_dir = root / task_id
    _write_conflicting_filter_xlsx(task_dir / "reports" / "final.xlsx")
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    finalization = {
        **_HUMAN_READY_FINALIZATION,
        "primary_deliverable_kind": "xlsx",
        "candidate_artifacts": [
            {
                "path": "reports/final.xlsx",
                "kind": "xlsx",
                "note": "Review-ready workbook.",
            }
        ],
    }
    finished = _finish_with_payload(root, task_id, lease, _final_payload(finalization))
    assert_eq(finished.get("status"), "finalize", "conflicting XLSX should rework")
    reasons = (finished.get("finalization_validation") or {}).get("reasons") or []
    assert_in(
        "xlsx_conflicting_table_autofilter",
        reasons,
        "conflicting worksheet/table filters should be rejected",
    )


def test_worker_final_accepts_review_ready_output_package(root: Path) -> None:
    task_id = "package-finalization"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Prepare a multi-file deliverable package.",
            "--title",
            "Package Finalization",
            "--stale-timeout-min",
            "1",
        )
    )
    package_dir = root / task_id / "workspace" / "outputs" / "repository-example"
    package_dir.mkdir(parents=True)
    (package_dir / "README.md").write_text(
        "# Repository Example\n\nThis package is the final deliverable.\n",
        encoding="utf-8",
    )
    (package_dir / "app.py").write_text("print('ready')\n", encoding="utf-8")
    (package_dir / "manifest.json").write_text(
        json.dumps({"entrypoint": "README.md", "files": ["README.md", "app.py"]})
        + "\n",
        encoding="utf-8",
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    payload = _final_payload(
        {
            **_HUMAN_READY_FINALIZATION,
            "primary_deliverable_kind": "package",
            "candidate_artifacts": [
                {
                    "path": "workspace/outputs/repository-example",
                    "kind": "final_package",
                    "entrypoint": "README.md",
                    "note": "Review-ready package directory.",
                }
            ],
            "validation_evidence": [
                {
                    "kind": "package_review",
                    "summary": "Checked README entrypoint and package files.",
                }
            ],
        }
    )
    payload["final_report_markdown"] = ""

    finished = _finish_with_payload(root, task_id, lease, payload)
    assert_eq(finished["status"], "awaiting_review", "package should reach review")
    state = json.loads((root / task_id / "state.json").read_text(encoding="utf-8"))
    delivery = state.get("delivery") or {}
    assert_true(delivery.get("review_ready"), "package should be review-ready")
    assert_true(not delivery.get("ready"), "package should still require approval")
    assert_eq(delivery.get("package_path"), str(package_dir), "delivery should track package path")
    assert_eq(delivery.get("primary_file"), str(package_dir / "README.md"), "package README should be primary file")
    assert_true(delivery.get("attachments"), "package should expose attachments")
    reasons = [
        reason
        for finding in (state.get("finalization") or {}).get("last_validation_findings", [])
        for reason in (finding.get("reasons") or [])
    ]
    assert_true(
        "raw_artifact_exposed_as_final" not in reasons,
        "package should not be treated as raw workspace",
    )


def test_worker_final_rejects_package_symlink_escape(root: Path) -> None:
    task_id = "package-symlink-escape"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Reject unsafe package.",
            "--title",
            "Package Escape",
            "--stale-timeout-min",
            "1",
        )
    )
    package_dir = root / task_id / "workspace" / "outputs" / "unsafe-package"
    package_dir.mkdir(parents=True)
    (package_dir / "README.md").write_text("# Unsafe\n\nEscaping package.\n", encoding="utf-8")
    (package_dir / "escape").symlink_to(root)
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    payload = _final_payload(
        {
            **_HUMAN_READY_FINALIZATION,
            "primary_deliverable_kind": "package",
            "candidate_artifacts": [
                {
                    "path": "workspace/outputs/unsafe-package",
                    "kind": "final_package",
                    "entrypoint": "README.md",
                }
            ],
            "validation_evidence": [
                {"kind": "package_review", "summary": "Package was inspected."}
            ],
        }
    )
    payload["final_report_markdown"] = ""

    finished = _finish_with_payload(root, task_id, lease, payload)
    assert_eq(finished["status"], "finalize", "unsafe package should stay in finalize")
    reasons = (finished.get("finalization_validation") or {}).get("reasons") or []
    assert_in("candidate_package_symlink_escape", reasons, "symlink escape should be rejected")


def test_delivery_manifest_populated_on_completion(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "delivery-test",
            "--goal",
            "Delivery manifest test",
        )
    )
    task_dir = root / "delivery-test"
    state_path = task_dir / "state.json"

    lease = json_out(run("begin", "--root", str(root), "--id", "delivery-test"))
    finished = finish_to_awaiting_review(root, "delivery-test", lease)
    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "worker-initiated final should go to awaiting_review",
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    delivery = state.get("delivery") or {}
    assert_true(
        bool(delivery.get("primary_file")),
        "delivery.primary_file should be set after awaiting_review",
    )
    assert_true(
        delivery.get("review_ready"),
        "delivery.review_ready should be True after awaiting_review",
    )
    assert_true(
        not delivery.get("ready"),
        "delivery.ready should remain False until explicit delivery approval",
    )


def test_mark_delivered_command(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "mark-delivered-test",
            "--goal",
            "Mark delivered test",
        )
    )
    task_dir = root / "mark-delivered-test"
    reports_dir = task_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "final.pdf").write_text("dummy pdf", encoding="utf-8")
    (reports_dir / "leads.xlsx").write_text("dummy xlsx", encoding="utf-8")

    result = json_out(
        run(
            "mark-delivered",
            "--root",
            str(root),
            "--id",
            "mark-delivered-test",
            "--primary-file",
            "reports/final.pdf",
            "--summary-text",
            "Analysis complete. PDF attached.",
            "--channel-strategy",
            "attach",
            "--attachment",
            "reports/leads.xlsx",
            "--ready",
        )
    )
    assert_true(
        result.get("delivery_ready"),
        "mark-delivered should set delivery_ready=True",
    )
    assert_true(
        result.get("primary_file"),
        "primary_file should be set (resolved to absolute path)",
    )
    assert_eq(
        result.get("primary_file"),
        str(reports_dir / "final.pdf"),
        "relative primary_file should be stored as a task-local absolute path",
    )
    assert_eq(
        result.get("summary_text"),
        "Analysis complete. PDF attached.",
        "summary_text should be set",
    )
    assert_eq(
        result.get("channel_strategy"),
        "attach",
        "channel_strategy should be set",
    )
    attachments = result.get("attachments") or []
    assert_true(
        any("leads.xlsx" in att for att in attachments),
        "attachment should be in attachments list",
    )


def test_mark_delivered_accepts_structured_outputs(root: Path) -> None:
    task_id = "delivery-output-files"
    run("create", "--root", str(root), "--id", task_id, "--goal", "Prepare outputs")
    task_dir = root / task_id
    out_dir = task_dir / "workspace" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "report.pdf").write_bytes(b"%PDF-1.7\n")
    (out_dir / "sources.xlsx").write_bytes(b"readable")

    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text())
    state["working_memory"]["output_contract"] = {
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
        ],
        "quality_checks": [],
        "search_profile": None,
    }
    state["finalization"] = {
        **state["finalization"],
        "status": "passed",
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
        ],
    }
    state["status"] = "awaiting_review"
    state["delivery"]["review_ready"] = True
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))

    delivered = json_out(
        run(
            "mark-delivered",
            "--root",
            str(root),
            "--id",
            task_id,
            "--output",
            "id=report,path=workspace/outputs/report.pdf,role=primary_deliverable,media_type=application/pdf",
            "--output",
            "id=sources,path=workspace/outputs/sources.xlsx,role=supporting_deliverable,media_type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "--ready",
        )
    )

    assert_eq(
        delivered["primary_file"],
        str(out_dir / "report.pdf"),
        "primary_file should mirror the primary structured output",
    )
    assert_eq(
        delivered["attachments"],
        [str(out_dir / "sources.xlsx")],
        "attachments should mirror supporting structured outputs",
    )
    status = json_out(run("status", "--root", str(root), "--id", task_id))
    assert_eq(
        [item["id"] for item in status["delivery"]["outputs"]],
        ["report", "sources"],
        "status should expose structured delivery outputs",
    )


def test_mark_delivered_succeeds_with_valid_relative_primary_file(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "delivery-relative-success",
            "--goal",
            "Test mark-delivered with relative path",
        )
    )
    task_dir = root / "delivery-relative-success"
    reports_dir = task_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    final_pdf = reports_dir / "final.pdf"
    final_pdf.write_text("dummy pdf content", encoding="utf-8")

    result = json_out(
        run(
            "mark-delivered",
            "--root",
            str(root),
            "--id",
            "delivery-relative-success",
            "--primary-file",
            "reports/final.pdf",
            "--ready",
        )
    )
    assert_true(
        result.get("delivery_ready"),
        "mark-delivered should set delivery_ready=True with valid relative path",
    )
    assert_true(
        result.get("primary_file"),
        "primary_file should be set with resolved absolute path",
    )
    assert_eq(
        result.get("primary_file"),
        str(final_pdf),
        "relative primary_file should be persisted as an absolute path",
    )
    health = json_out(
        run(
            "health",
            "--root",
            str(root),
            "--id",
            "delivery-relative-success",
            "--format",
            "json",
        )
    )
    assert_true(
        not any(
            item.get("code") == "delivery_ready_but_missing_primary"
            for item in health.get("findings") or []
        ),
        "health should resolve stored primary_file after mark-delivered",
    )


def test_mark_delivered_fails_with_missing_primary_file_when_ready(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "delivery-missing-file",
            "--goal",
            "Test mark-delivered with missing file",
        )
    )
    fail_result = run(
        "mark-delivered",
        "--root",
        str(root),
        "--id",
        "delivery-missing-file",
        "--primary-file",
        "reports/nonexistent.pdf",
        "--ready",
        check=False,
    )
    assert_true(
        fail_result.returncode != 0,
        "mark-delivered should fail with missing primary_file and --ready",
    )
    assert_in(
        "does not exist", fail_result.stderr.lower(),
        "error message should indicate file does not exist",
    )


def test_mark_delivered_rejects_external_primary_file(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "delivery-external-file",
            "--goal",
            "Test mark-delivered rejects external file",
        )
    )
    outside_file = root.parent / "outside-delivery.txt"
    outside_file.write_text("outside\n", encoding="utf-8")

    fail_result = run(
        "mark-delivered",
        "--root",
        str(root),
        "--id",
        "delivery-external-file",
        "--primary-file",
        str(outside_file),
        "--ready",
        check=False,
    )

    assert_true(
        fail_result.returncode != 0,
        "mark-delivered should reject primary_file outside the task directory",
    )
    assert_in(
        "outside task directory",
        fail_result.stderr.lower(),
        "error should mention task directory containment",
    )


def test_mark_delivered_fails_when_primary_file_points_to_directory(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "delivery-directory-test",
            "--goal",
            "Test mark-delivered with directory path",
        )
    )
    task_dir = root / "delivery-directory-test"
    reports_dir = task_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    fail_result = run(
        "mark-delivered",
        "--root",
        str(root),
        "--id",
        "delivery-directory-test",
        "--primary-file",
        "reports",
        "--ready",
        check=False,
    )
    assert_true(
        fail_result.returncode != 0,
        "mark-delivered should fail when primary_file is a directory",
    )
    assert_in(
        "not a file", fail_result.stderr.lower(),
        "error message should indicate path is not a file",
    )


def test_mark_delivered_fails_ready_without_primary_file(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "delivery-no-primary",
            "--goal",
            "Test mark-delivered --ready without primary_file",
        )
    )
    fail_result = run(
        "mark-delivered",
        "--root",
        str(root),
        "--id",
        "delivery-no-primary",
        "--ready",
        check=False,
    )
    assert_true(
        fail_result.returncode != 0,
        "mark-delivered should fail when --ready without primary_file",
    )
    assert_in(
        "primary_file", fail_result.stderr.lower(),
        "error message should mention primary_file requirement",
    )


def test_mark_delivered_validates_existing_primary_on_ready(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "delivery-existing-invalid",
            "--goal",
            "Test mark-delivered validates existing primary_file",
        )
    )
    task_dir = root / "delivery-existing-invalid"
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["delivery"] = {"primary_file": "reports/missing.pdf"}
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    fail_result = run(
        "mark-delivered",
        "--root",
        str(root),
        "--id",
        "delivery-existing-invalid",
        "--ready",
        check=False,
    )
    assert_true(
        fail_result.returncode != 0,
        "mark-delivered should fail when existing primary_file is invalid",
    )
    assert_in(
        "does not exist", fail_result.stderr.lower(),
        "error message should indicate file does not exist",
    )
