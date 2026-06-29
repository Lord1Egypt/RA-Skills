from __future__ import annotations

import json
from pathlib import Path

from .helpers import assert_eq, assert_in, json_out, run


def test_deliverable_kind_cli_sets_output_contract(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "contract-kind-create",
            "--goal",
            "Prepare a report",
            "--deliverable",
            "自由文本，不用于判断格式",
            "--deliverable-kind",
            "pdf_report",
            "--skip-preflight",
        )
    )
    assert_eq(created["status"], "created", "create status")

    state = json.loads(
        (root / "contract-kind-create" / "state.json").read_text(encoding="utf-8")
    )
    working = state.get("working_memory") or {}
    contract = working.get("output_contract") or {}
    assert_eq(
        working.get("deliverable"),
        "自由文本，不用于判断格式",
        "deliverable remains display text",
    )
    assert_eq(contract.get("kind"), "pdf_report", "deliverable kind is structured")


def test_set_deliverable_kind_updates_contract_without_text(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "contract-kind-setter",
            "--goal",
            "Prepare a report",
            "--deliverable",
            "Keep this free-text hint",
            "--skip-preflight",
        )
    )

    updated = json_out(
        run(
            "set-deliverable",
            "--root",
            str(root),
            "--id",
            "contract-kind-setter",
            "--kind",
            "xlsx",
        )
    )
    assert_eq(updated["deliverable"], "Keep this free-text hint", "hint remains")
    assert_eq(
        updated["output_contract"]["kind"],
        "xlsx",
        "set-deliverable --kind should update output contract",
    )

    state = json.loads(
        (root / "contract-kind-setter" / "state.json").read_text(encoding="utf-8")
    )
    working = state.get("working_memory") or {}
    assert_eq(working.get("deliverable"), "Keep this free-text hint", "state hint remains")
    assert_eq(
        working.get("output_contract", {}).get("kind"),
        "xlsx",
        "state contract kind should be structured",
    )


def test_invalid_deliverable_kind_exits_nonzero(root: Path) -> None:
    result = run(
        "create",
        "--root",
        str(root),
        "--id",
        "invalid-contract-kind",
        "--goal",
        "Prepare a report",
        "--deliverable-kind",
        "spreadsheet",
        "--skip-preflight",
        check=False,
    )

    assert_eq(result.returncode, 2, "invalid deliverable kind should fail")
    assert_in("invalid choice", result.stderr, "argparse should explain invalid kind")
    assert_in("xlsx", result.stderr, "allowed enum values should be visible")


def test_free_text_remains_available_to_worker_and_surfaces(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "free-text-preserved",
            "--goal",
            "请分析供应商风险，并保留这些原始说明给执行代理。",
            "--deliverable",
            "Свободное описание результата: сравнительная записка для чтения человеком.",
            "--constraint",
            "Не терять пользовательские формулировки.",
            "--instruction",
            "Сохрани контекст для worker-а.",
            "--skip-preflight",
        )
    )

    lease = json_out(run("begin", "--root", str(root), "--id", "free-text-preserved"))
    guidance_blob = "\n".join(lease.get("execution_guidance") or [])
    input_layer = lease.get("input_layer") or {}

    assert_eq(
        input_layer.get("deliverable"),
        "Свободное описание результата: сравнительная записка для чтения человеком.",
        "begin payload should still carry free-text deliverable",
    )
    assert_in(
        "requested deliverable",
        guidance_blob.lower(),
        "guidance should still mention requested deliverable",
    )

    summary_text = run(
        "summary",
        "--root",
        str(root),
        "--id",
        "free-text-preserved",
        "--format",
        "text",
    ).stdout
    assert_in(
        "Свободное описание результата",
        summary_text,
        "summary should still render free-text deliverable",
    )


def test_deliverable_free_text_does_not_infer_format_from_language(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "free-text-no-format-inference",
            "--goal",
            "请准备一个详细报告并发送到聊天线程",
            "--deliverable",
            "请做一个适合阅读的报告",
            "--skip-preflight",
        )
    )
    assert_eq(created["status"], "created", "create status")

    from research_mode_finalization import build_deliverable_format_decision

    state = json.loads(
        (root / "free-text-no-format-inference" / "state.json").read_text(
            encoding="utf-8"
        )
    )
    decision = build_deliverable_format_decision(
        state=state,
        finalization=None,
        report_markdown="# Report\n\nA short Markdown candidate exists for feasibility only.",
        artifact_check=None,
    )

    assert_eq(
        decision.get("source"),
        "artifact",
        "free text must not become an explicit or inferred source",
    )
    assert_eq(
        decision.get("selected_kind"),
        "markdown_report",
        "selection should follow feasible artifact only",
    )


def test_explicit_output_contract_kind_controls_format(root: Path) -> None:
    from research_mode_finalization import check_deliverable_format_decision

    state = {
        "working_memory": {
            "deliverable": "任意文本",
            "output_contract": {"kind": "pdf_report", "quality_checks": []},
        }
    }
    artifact_check = {
        "check": "candidate_artifact_inspection",
        "passed": True,
        "reasons": [],
        "artifacts": [
            {"path": "final-report.md", "format": "markdown", "reasons": []}
        ],
    }

    result = check_deliverable_format_decision(
        state=state,
        finalization={
            "status": "passed",
            "primary_deliverable_kind": "markdown_report",
        },
        report_markdown="# Report\n\nMarkdown candidate.",
        artifact_check=artifact_check,
    )

    assert_eq(result.get("passed"), False, "contract PDF with Markdown artifact should fail")
    assert_in(
        "output_contract_format_mismatch",
        result.get("reasons") or [],
        "contract mismatch reason",
    )
    assert_eq(result.get("desired_kind"), "pdf_report", "contract kind is desired")
    assert_eq(
        result.get("feasible_kind"),
        "markdown_report",
        "artifact kind is feasible",
    )


def test_quality_checks_are_activated_only_by_contract(root: Path) -> None:
    from research_mode_lifecycle_helpers import inspect_deliverable_requirements

    report = "# Informe\n\nTexto breve sin lista."

    without_contract = inspect_deliverable_requirements(
        "bullet list",
        report,
        payload={},
        total_sources=1,
        total_findings=1,
        output_contract={"quality_checks": []},
    )
    assert_eq(
        without_contract.get("checks"),
        [],
        "free text should not activate quality checks",
    )

    with_contract = inspect_deliverable_requirements(
        "",
        report,
        payload={},
        total_sources=1,
        total_findings=1,
        output_contract={"quality_checks": [{"kind": "bullet_list", "min_items": 2}]},
    )
    bullet_check = next(
        check for check in with_contract["checks"] if check["kind"] == "bullet_list"
    )
    assert_eq(bullet_check["passed"], False, "contract bullet_list should be enforced")
    assert_in(
        "deliverable_bullet_list_unstructured",
        with_contract["reasons"],
        "bullet list reason",
    )


def test_comparative_matrix_check_uses_shape_not_header_language(root: Path) -> None:
    from research_mode_lifecycle_helpers import inspect_deliverable_requirements

    report = """# 比较

| 甲 | 乙 | 丙 |
| --- | --- | --- |
| A | 1 | x |
| B | 2 | y |
"""
    validation = inspect_deliverable_requirements(
        "",
        report,
        payload={},
        total_sources=2,
        total_findings=2,
        output_contract={
            "quality_checks": [
                {"kind": "comparative_matrix", "min_rows": 2, "min_columns": 3}
            ]
        },
    )
    check = next(
        item for item in validation["checks"] if item["kind"] == "comparative_matrix"
    )
    assert_eq(
        check["passed"],
        True,
        "matrix shape should pass regardless of header language",
    )


def test_free_text_deliverable_does_not_activate_comparative_check(root: Path) -> None:
    from research_mode_lifecycle_helpers import inspect_deliverable_requirements

    validation = inspect_deliverable_requirements(
        "сравнительная записка",
        "# Note\n\n- A\n- B\n",
        payload={},
        total_sources=2,
        total_findings=2,
        output_contract={"quality_checks": []},
    )
    assert_eq(
        validation["checks"],
        [],
        "free-text deliverable must not activate comparative validation",
    )
    assert_eq(
        validation["reasons"],
        [],
        "no contract means no comparative rejection",
    )


def test_ru_text_does_not_auto_enable_local_routing(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "ru-text-no-local-routing",
            "--goal",
            "Найти контакты магазинов в Ростове",
            "--skip-preflight",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "ru-text-no-local-routing"))
    guidance = "\n".join(lease.get("execution_guidance") or [])

    assert_eq(
        "RU/local/regional research" in guidance,
        False,
        "Russian free text alone must not activate local routing guidance",
    )


def test_explicit_search_profile_controls_routing_guidance(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "explicit-local-routing",
            "--goal",
            "Find local businesses",
            "--skip-preflight",
        )
    )
    state_path = root / "explicit-local-routing" / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.setdefault("working_memory", {})["search_profile"] = {
        "scope": "local",
        "locale": "ru-RU",
        "region_hint": "RU-ROS",
        "discovery_mode": "serp_first",
    }
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lease = json_out(run("begin", "--root", str(root), "--id", "explicit-local-routing"))
    guidance = "\n".join(lease.get("execution_guidance") or [])

    assert_in("local", guidance.lower(), "explicit local profile should affect guidance")
    assert_in("serp", guidance.lower(), "explicit serp_first profile should affect guidance")
