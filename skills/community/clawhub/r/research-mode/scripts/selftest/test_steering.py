"""Working-memory mutation, completion validation, deliverable checks, routing guidance."""
from __future__ import annotations

import json
from pathlib import Path

from .helpers import (
    assert_eq,
    assert_in,
    assert_true,
    human_ready_finalization,
    json_out,
    route_to_finalize,
    run,
)


def _set_output_quality_checks(root: Path, task_id: str, checks: list[dict]) -> None:
    state_path = root / task_id / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    contract = state.setdefault("working_memory", {}).setdefault(
        "output_contract", {}
    )
    contract["quality_checks"] = checks
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def test_working_memory_mutation(root: Path) -> None:
    mutate_root = root / "mutate-root"
    mutate_root.mkdir(parents=True, exist_ok=True)
    run("create", "--root", str(mutate_root), "--id", "mut-1", "--goal", "Mutation test")
    mutated1 = json_out(run("mutate-working-memory", "--root", str(mutate_root), "--append-angle", "сравнить с альтернативной гипотезой"))
    assert_in("альтернативной гипотезой", mutated1["next_angle"], "append-angle should update next_angle on the sole active task")
    mutated2 = json_out(run("mutate-working-memory", "--root", str(mutate_root), "--add-open-question", "что пока не доказано?"))
    assert_in("что пока не доказано?", mutated2["open_questions"], "add-open-question should extend open_questions")
    mutated3 = json_out(run("mutate-working-memory", "--root", str(mutate_root), "--set-summary", "Пользователь уточнил фокус"))
    assert_eq(mutated3["summary"], "Пользователь уточнил фокус", "set-summary should replace working summary")
    mutated4 = json_out(run("mutate-working-memory", "--root", str(mutate_root), "--add-constraint", "не использовать слабые пересказы"))
    assert_in("не использовать слабые пересказы", mutated4["constraints"], "add-constraint should persist constraint")
    mutated5 = json_out(run("mutate-working-memory", "--root", str(mutate_root), "--set-deliverable", "короткий сравнительный итог"))
    assert_eq(mutated5["deliverable"], "короткий сравнительный итог", "set-deliverable should persist deliverable")
    mutated6 = json_out(run("mutate-working-memory", "--root", str(mutate_root), "--add-instruction", "сначала первичные источники"))
    assert_in("сначала первичные источники", mutated6["user_instructions"], "add-instruction should persist instruction")
    summary_mut = run("summary", "--root", str(mutate_root), "--format", "text").stdout
    assert_in("Пользователь уточнил фокус", summary_mut, "summary should reflect mutated working summary")
    assert_in("что пока не доказано?", summary_mut, "summary should reflect mutated open question")
    assert_in("не использовать слабые пересказы", summary_mut, "summary should reflect constraint")
    assert_in("короткий сравнительный итог", summary_mut, "summary should reflect deliverable")
    assert_in("сначала первичные источники", summary_mut, "summary should reflect user instruction")
    draft_mut = run("draft-report", "--root", str(mutate_root), "--format", "markdown").stdout
    assert_in("## Constraints", draft_mut, "draft should expose constraints section")
    assert_in("не использовать слабые пересказы", draft_mut, "draft should expose constraints")
    assert_in("## Target deliverable", draft_mut, "draft should expose deliverable section")
    assert_in("короткий сравнительный итог", draft_mut, "draft should expose deliverable")
    assert_in("## User instructions", draft_mut, "draft should expose instructions section")
    assert_in("сначала первичные источники", draft_mut, "draft should expose instructions")


def test_mutation_aliases(root: Path) -> None:
    mutate_root = root / "alias-root"
    mutate_root.mkdir(parents=True, exist_ok=True)
    run("create", "--root", str(mutate_root), "--id", "alias-1", "--goal", "Alias test")
    aliased_angle = json_out(run("add-angle", "--root", str(mutate_root), "докинуть альтернативный сценарий"))
    assert_in("альтернативный сценарий", aliased_angle["next_angle"], "add-angle alias should update next_angle")
    aliased_constraint = json_out(run("add-constraint", "--root", str(mutate_root), "без форумных слухов"))
    assert_in("без форумных слухов", aliased_constraint["constraints"], "add-constraint alias should update constraints")
    aliased_instruction = json_out(run("add-instruction", "--root", str(mutate_root), "отдельно отметить риски"))
    assert_in("отдельно отметить риски", aliased_instruction["user_instructions"], "add-instruction alias should update instructions")
    aliased_deliverable = json_out(run("set-deliverable", "--root", str(mutate_root), "итог в виде bullet list"))
    assert_eq(aliased_deliverable["deliverable"], "итог в виде bullet list", "set-deliverable alias should update deliverable")


def test_work_order_input_layer(root: Path) -> None:
    wo_root = root / "wo-root"
    wo_root.mkdir(parents=True, exist_ok=True)
    run("create", "--root", str(wo_root), "--id", "wo-1", "--goal", "Work order test",
        "--constraint", "не использовать слабые пересказы",
        "--instruction", "сначала первичные источники",
        "--deliverable", "итог в виде bullet list")
    run("mutate-working-memory", "--root", str(wo_root), "--append-angle", "докинуть альтернативный сценарий")
    run("add-constraint", "--root", str(wo_root), "без форумных слухов")
    run("add-instruction", "--root", str(wo_root), "отдельно отметить риски")
    run("set-deliverable", "--root", str(wo_root), "итог в виде bullet list")

    lease = json_out(run("begin", "--root", str(wo_root), "--id", "wo-1"))
    assert_in("input_layer", lease, "begin payload should expose input_layer")
    assert_in("execution_guidance", lease, "begin payload should expose execution guidance")
    assert_in("finalization_guidance", lease, "begin payload should expose finalization guidance")
    assert_in("finalization_contract", lease, "begin payload should expose finalization contract")
    assert_true(isinstance(lease["execution_guidance"], list), "execution_guidance should be a list")
    assert_in("не использовать слабые пересказы", lease["input_layer"]["constraints"], "begin payload should carry constraints")
    assert_eq(lease["input_layer"]["deliverable"], "итог в виде bullet list", "begin payload should carry deliverable")
    assert_in("сначала первичные источники", lease["input_layer"]["user_instructions"], "begin payload should carry user instructions")
    assert_true(any("hard boundaries" in item for item in lease["execution_guidance"]), "guidance should mention constraints")
    assert_true(any("requested deliverable" in item for item in lease["execution_guidance"]), "guidance should mention deliverable")
    assert_true(any("raw" in item.lower() for item in lease["finalization_guidance"]), "finalization guidance should warn against raw artifacts as final")
    assert_true(any("finalization" in item.lower() for item in lease["finalization_guidance"]), "finalization guidance should mention the required trace")
    assert_true(any("output_contract.outputs" in item for item in lease["finalization_guidance"]), "finalization guidance should explain structured outputs")
    assert_true(any("source_for" in item for item in lease["finalization_guidance"]), "finalization guidance should explain provenance relations")
    contract = lease["finalization_contract"]
    assert_eq(contract["required_status"], "passed", "finalization contract should require passed status")
    assert_in("inferred_user_need", contract["required_trace_fields"], "contract should require inferred user need")
    assert_in("validation_evidence", contract["required_trace_fields"], "contract should require validation evidence")
    assert_eq(contract["requested_deliverable"], "итог в виде bullet list", "contract should carry requested deliverable")
    artifact_requirements = contract["candidate_artifact_requirements"]
    assert_in(
        "user_facing",
        artifact_requirements["visibility"],
        "contract should expose structured artifact visibility",
    )
    assert_eq(
        artifact_requirements["primary_role"],
        "primary",
        "contract should expose structured primary artifact role",
    )
    run("fail", "--root", str(wo_root), "--id", "wo-1", "--run-id", lease["run_id"], "--error", "cleanup")


def test_ru_local_guidance(root: Path) -> None:
    ru_root = root / "ru-local-root"
    ru_root.mkdir(parents=True, exist_ok=True)
    ru_local = json_out(
        run("create", "--root", str(ru_root), "--id", "ru-local-1",
            "--goal", "Собери сайты, контакты и адреса сервисов по ремонту телефонов в Каменске-Шахтинском",
            "--instruction", "Нужен список ресурсов и локальная выдача по региону")
    )
    assert_eq(ru_local["status"], "created", "ru-local task should be created")
    state_path = ru_root / "ru-local-1" / "state.json"
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
    lease = json_out(run("begin", "--root", str(ru_root), "--id", "ru-local-1"))
    assert_true(
        any("search_profile.scope=local" in item for item in lease["execution_guidance"]),
        "explicit local search profile should bias toward local discovery",
    )
    assert_true(
        any("serp_first" in item for item in lease["execution_guidance"]),
        "explicit search profile should expose discovery mode",
    )
    assert_true(
        any("same language" in item.lower() for item in lease["execution_guidance"]),
        "work order should tell workers to answer in the user's language",
    )
    run("fail", "--root", str(ru_root), "--id", "ru-local-1", "--run-id", lease["run_id"], "--error", "cleanup")


def test_completion_validation(root: Path) -> None:
    cv_root = root / "cv-root"
    cv_root.mkdir(parents=True, exist_ok=True)
    run("create", "--root", str(cv_root), "--id", "cv-pass", "--goal", "Completion pass",
        "--constraint", "без форумных слухов", "--instruction", "отдельно отметить риски",
        "--deliverable", "итог в виде bullet list")
    lease = json_out(run("begin", "--root", str(cv_root), "--id", "cv-pass"))
    lease = route_to_finalize(cv_root, "cv-pass", lease)
    result = Path(lease["paths"]["result_file"])
    result.parent.mkdir(parents=True, exist_ok=True)
    result.write_text(
        json.dumps({
            "summary": "Mutation task finalized with layered input preserved.",
            "next_angle": "done",
            "meaningful_progress": True,
            "phase": "finalize",
            "open_questions": [],
            "sources": [{"title": "mut-final-source"}],
            "findings": [{"kind": "synthesis", "text": "Layered steering survived into finalization."}],
            "notify_recommendation": "final",
            "should_complete": True,
            "final_report_markdown": None,
            "finalization": human_ready_finalization(),
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    finished = json_out(run("finish", "--root", str(cv_root), "--id", "cv-pass", "--run-id", lease["run_id"], "--result-file", str(result)))
    assert_eq(finished["status"], "awaiting_review", "worker-initiated final should go to awaiting_review")
    final = (cv_root / "cv-pass" / "final-report.md").read_text(encoding="utf-8")
    assert_in("## Constraints", final, "final report should expose constraints section")
    assert_in("без форумных слухов", final, "final report should expose constraints")
    assert_in("## Requested deliverable", final, "final report should expose deliverable section")
    assert_in("итог в виде bullet list", final, "final report should expose deliverable")
    assert_in("## User instructions", final, "final report should expose user instructions section")
    assert_in("отдельно отметить риски", final, "final report should expose user instructions")
    assert_eq(finished["normalized_reason"], "awaiting_review:passed-validation", "awaiting_review should expose appropriate reason")


def test_completion_rejection(root: Path) -> None:
    cr_root = root / "cr-root"
    cr_root.mkdir(parents=True, exist_ok=True)
    run("create", "--root", str(cr_root), "--id", "cr-reject", "--goal", "Completion rejection test")
    lease = json_out(run("begin", "--root", str(cr_root), "--id", "cr-reject"))
    lease = route_to_finalize(cr_root, "cr-reject", lease, sources=[], findings=[])
    result = Path(lease["paths"]["result_file"])
    result.parent.mkdir(parents=True, exist_ok=True)
    result.write_text(
        json.dumps({
            "summary": "Tried to finalize without evidence base.",
            "next_angle": "collect actual evidence",
            "meaningful_progress": True,
            "phase": "finalize",
            "open_questions": [],
            "sources": [],
            "findings": [],
            "notify_recommendation": "silent",
            "should_complete": True,
            "final_report_markdown": "# Empty-ish final\n\nNo evidence.",
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    finished = json_out(run("finish", "--root", str(cr_root), "--id", "cr-reject", "--run-id", lease["run_id"], "--result-file", str(result)))
    assert_eq(finished["status"], "idle", "completion validation rejection should keep task idle")
    assert_eq(finished["normalized_reason"], "rejected:completion-validation", "completion validation rejection should expose normalized reason")
    assert_in("evidence_base_empty", (finished["completion_validation"] or {}).get("reasons", []), "completion validation rejection should explain why completion was rejected")
    reject_summary = json_out(run("summary", "--root", str(cr_root), "--id", "cr-reject", "--format", "json"))
    assert_eq(reject_summary["history"]["last_terminal_reason"], "rejected:completion-validation", "summary should expose rejected completion as terminal reason")


def test_blocker_failure(root: Path) -> None:
    bf_root = root / "bf-root"
    bf_root.mkdir(parents=True, exist_ok=True)
    run("create", "--root", str(bf_root), "--id", "bf-blocker", "--goal", "Blocker failure test")
    lease = json_out(run("begin", "--root", str(bf_root), "--id", "bf-blocker"))
    failed = json_out(run("fail", "--root", str(bf_root), "--id", "bf-blocker", "--run-id", lease["run_id"], "--error", "Need explicit user decision", "--requires-user-input"))
    assert_eq(failed["status"], "failed", "blocker failure should move task to failed")
    assert_eq(failed["normalized_reason"], "failed:blocker", "blocker failure should expose normalized reason")


def test_deliverable_bullet_validation(root: Path) -> None:
    db_root = root / "db-root"
    db_root.mkdir(parents=True, exist_ok=True)
    run("create", "--root", str(db_root), "--id", "db-bullets", "--goal", "Bullet deliverable validation", "--deliverable", "итог в виде bullet list")
    _set_output_quality_checks(
        db_root,
        "db-bullets",
        [{"kind": "bullet_list", "min_items": 2}],
    )
    lease = json_out(run("begin", "--root", str(db_root), "--id", "db-bullets"))
    lease = route_to_finalize(db_root, "db-bullets", lease)
    result = Path(lease["paths"]["result_file"])
    result.parent.mkdir(parents=True, exist_ok=True)
    result.write_text(
        json.dumps({
            "summary": "Structured bullet deliverable was not actually structured.",
            "next_angle": "rewrite as real bullets",
            "meaningful_progress": True,
            "phase": "finalize",
            "open_questions": [],
            "sources": [{"title": "bullet-source", "url": "https://example.com/bullet"}],
            "findings": [{"kind": "note", "text": "There is at least one concrete point."}],
            "notify_recommendation": "silent",
            "should_complete": True,
            "final_report_markdown": "# Итог\n\nЭто сплошной абзац без оформленного списка.",
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    finished = json_out(run("finish", "--root", str(db_root), "--id", "db-bullets", "--run-id", lease["run_id"], "--result-file", str(result)))
    assert_eq(finished["status"], "idle", "bullet-list deliverable should be rejected when report is unstructured")
    assert_in("deliverable_bullet_list_unstructured", (finished["completion_validation"] or {}).get("reasons", []), "bullet-list deliverable validation should explain rejection")
    summary_text = run("summary", "--root", str(db_root), "--id", "db-bullets", "--format", "text").stdout
    assert_in("Deliverable checks:", summary_text, "summary text should expose deliverable checks header")
    assert_in("bullet_list: failed", summary_text, "summary text should expose failed deliverable checks")
    playbook = (db_root / "db-bullets" / "task-playbook.md").read_text(encoding="utf-8")
    assert_in("- Deliverable checks:", playbook, "playbook should expose deliverable checks header")
    assert_in("bullet_list: failed", playbook, "playbook should expose failed deliverable checks")


def test_deliverable_comparative_validation(root: Path) -> None:
    dc_root = root / "dc-root"
    dc_root.mkdir(parents=True, exist_ok=True)
    run("create", "--root", str(dc_root), "--id", "dc-compare", "--goal", "Comparative deliverable validation", "--deliverable", "сравнительная записка")
    _set_output_quality_checks(
        dc_root,
        "dc-compare",
        [{"kind": "comparative_matrix", "min_rows": 2, "min_columns": 2}],
    )
    lease = json_out(run("begin", "--root", str(dc_root), "--id", "dc-compare"))
    lease = route_to_finalize(dc_root, "dc-compare", lease)
    result = Path(lease["paths"]["result_file"])
    result.parent.mkdir(parents=True, exist_ok=True)
    result.write_text(
        json.dumps({
            "summary": "Prepared a proper comparative memo.",
            "next_angle": "done",
            "meaningful_progress": True,
            "phase": "finalize",
            "open_questions": [],
            "sources": [{"title": "Source A", "url": "https://example.com/a"}, {"title": "Source B", "url": "https://example.com/b"}],
            "findings": [{"kind": "fact", "text": "Подход A дешевле."}, {"kind": "fact", "text": "Подход B надёжнее."}],
            "notify_recommendation": "final",
            "should_complete": True,
            "final_report_markdown": "# Сравнительная записка\n\n## Сравнение вариантов\n\n| 方案 | 指标 |\n| --- | --- |\n| A | дешевле и проще внедряется |\n| B | даёт более высокую надёжность |\n\n## Вывод\n\nСравнение показывает явный компромисс между стоимостью и устойчивостью.",
            "finalization": human_ready_finalization(),
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    finished = json_out(run("finish", "--root", str(dc_root), "--id", "dc-compare", "--run-id", lease["run_id"], "--result-file", str(result)))
    assert_eq(finished["status"], "awaiting_review", "worker-initiated final should go to awaiting_review (then needs approve)")
    compare_summary = json_out(run("summary", "--root", str(dc_root), "--id", "dc-compare", "--format", "json"))
    compare_checks = ((compare_summary["completion"] or {}).get("deliverable_validation") or {}).get("checks") or []
    assert_true(any(check.get("kind") == "comparative_matrix" and check.get("passed") for check in compare_checks), "comparative deliverable validation should be inspectable in summary json")


def test_deliverable_comparative_ranked_table_without_keyword(root: Path) -> None:
    dt_root = root / "dt-root"
    dt_root.mkdir(parents=True, exist_ok=True)
    run("create", "--root", str(dt_root), "--id", "dt-compare-table", "--goal", "Comparative deliverable table validation", "--deliverable", "comparative memo")
    _set_output_quality_checks(
        dt_root,
        "dt-compare-table",
        [{"kind": "comparative_matrix", "min_rows": 2, "min_columns": 4}],
    )
    lease = json_out(run("begin", "--root", str(dt_root), "--id", "dt-compare-table"))
    lease = route_to_finalize(dt_root, "dt-compare-table", lease)
    result = Path(lease["paths"]["result_file"])
    result.parent.mkdir(parents=True, exist_ok=True)
    result.write_text(
        json.dumps({
            "summary": "Prepared a ranked decision table.",
            "next_angle": "done",
            "meaningful_progress": True,
            "phase": "finalize",
            "open_questions": [],
            "sources": [{"title": "Source A", "url": "https://example.com/a"}, {"title": "Source B", "url": "https://example.com/b"}],
            "findings": [{"kind": "fact", "text": "A has supply risk."}, {"kind": "fact", "text": "B has price risk."}],
            "notify_recommendation": "final",
            "should_complete": True,
            "final_report_markdown": "# Recommendation\n\n| 甲 | 乙 | 丙 | 丁 |\n| --- | --- | --- | --- |\n| 1 | A | choose | supply |\n| 2 | B | backup | price |\n\n## Rationale\n\nThe table gives a structured comparison with four columns and two candidate rows.",
            "finalization": human_ready_finalization(),
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    finished = json_out(run("finish", "--root", str(dt_root), "--id", "dt-compare-table", "--run-id", lease["run_id"], "--result-file", str(result)))
    assert_eq(finished["status"], "awaiting_review", "ranked table should satisfy comparative deliverable without keyword dependency")
    compare_summary = json_out(run("summary", "--root", str(dt_root), "--id", "dt-compare-table", "--format", "json"))
    compare_checks = ((compare_summary["completion"] or {}).get("deliverable_validation") or {}).get("checks") or []
    comparative_check = next(check for check in compare_checks if check.get("kind") == "comparative_matrix")
    assert_true(comparative_check.get("passed"), "comparative table should pass structural validation")
    assert_in("table_shape", comparative_check.get("structure_signals") or [], "summary should expose structural signal")


def test_mutation_ambiguity(root: Path) -> None:
    ma_root = root / "ma-root"
    ma_root.mkdir(parents=True, exist_ok=True)
    run("create", "--root", str(ma_root), "--id", "ma-1", "--goal", "Mutation ambiguity A")
    run("create", "--root", str(ma_root), "--id", "ma-2", "--goal", "Mutation ambiguity B")
    ambiguous = run("mutate-working-memory", "--root", str(ma_root), "--append-angle", "ещё один угол", check=False)
    assert_true(ambiguous.returncode != 0, "mutation should fail when multiple active tasks exist")
    assert_in("Multiple active research tasks found", ambiguous.stderr, "mutation ambiguity should be explicit")
