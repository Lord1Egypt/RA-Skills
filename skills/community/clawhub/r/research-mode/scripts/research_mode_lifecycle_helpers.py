from __future__ import annotations

import datetime as dt
import re
from pathlib import Path
from typing import Any

from research_mode_corpus import list_corpus_entries
from research_mode_adequacy import build_adequacy_contract, build_adequacy_guidance
from research_mode_finalization import (
    build_finalization_contract,
    build_output_decision,
    check_deliverable_format_decision,
    inspect_candidate_artifacts,
)
from research_mode_payloads import result_template
from research_mode_surfaces import build_synthesis_payload, compute_budget_phase
from research_mode_task import ResearchTask
from research_mode_utils import (
    effective_lock_stale_timeout_min,
    minutes_since,
    parse_ts,
    pending_result_path,
    read_jsonl,
)

RULES_PROFILE_MAX_CHARS = 20000
SKILL_DIR = Path(__file__).resolve().parent.parent
RULES_PROFILE_PATH = SKILL_DIR / "RULES.md"
USER_FACING_ARTIFACT_VISIBILITIES = {"user_facing", "external", "reviewable"}
INTERNAL_CANDIDATE_PATH_PREFIXES = (
    "iterations/",
    ".tmp/",
    "workspace/tmp/",
    "workspace/analysis/",
    "workspace/data/",
    "workspace/tools/",
    "workspace/vision/",
    "workspace/screenshots/",
)
SEARCH_SCOPES = {"local", "regional", "national", "global", "unknown"}
DISCOVERY_MODES = {"serp_first", "synthesis_first", "corpus_first", "unknown"}


def _structured_search_profile(state: dict[str, Any]) -> dict[str, Any]:
    working_memory = state.get("working_memory") or {}
    raw_profile = working_memory.get("search_profile")
    if not isinstance(raw_profile, dict):
        output_contract = working_memory.get("output_contract") or {}
        if isinstance(output_contract, dict):
            raw_profile = output_contract.get("search_profile")
    if not isinstance(raw_profile, dict):
        return {}

    scope = str(raw_profile.get("scope") or "unknown").strip().lower()
    discovery_mode = str(
        raw_profile.get("discovery_mode") or "unknown"
    ).strip().lower()
    if scope not in SEARCH_SCOPES:
        scope = "unknown"
    if discovery_mode not in DISCOVERY_MODES:
        discovery_mode = "unknown"

    profile: dict[str, Any] = {
        "scope": scope,
        "discovery_mode": discovery_mode,
    }
    for key in ("locale", "region_hint"):
        value = str(raw_profile.get(key) or "").strip()
        if value:
            profile[key] = value
    return profile


def _build_search_routing_guidance(state: dict[str, Any]) -> list[str]:
    guidance = [
        "Write user-facing summaries and final deliverables in the same language as the user's goal/instructions unless the user asks for another language.",
        "For discovery-heavy research, prefer tools that expose raw source lists / SERPs before relying on synthesis-first search.",
        "Use synthesis-first search after you already have candidate resources, or when the topic is clearly global/international rather than local/regional.",
    ]
    search_profile = _structured_search_profile(state)
    scope = search_profile.get("scope")
    discovery_mode = search_profile.get("discovery_mode")
    if scope in {"local", "regional", "national"}:
        scope_text = str(scope).replace("_", " ")
        region_hint = search_profile.get("region_hint")
        locale = search_profile.get("locale")
        guidance.extend(
            [
                f"Structured search_profile.scope={scope_text}: prefer matching geographic discovery tools before broad synthesis.",
            ]
        )
        if region_hint or locale:
            guidance.append(
                "Structured search profile hints: "
                + ", ".join(
                    item
                    for item in (
                        f"region_hint={region_hint}" if region_hint else "",
                        f"locale={locale}" if locale else "",
                    )
                    if item
                )
                + "."
            )
    if discovery_mode and discovery_mode != "unknown":
        guidance.append(
            f"Structured search_profile.discovery_mode={discovery_mode}: use that discovery mode as the first-pass search strategy."
        )
    return guidance


def _is_internal_candidate_path(path: str) -> bool:
    cleaned = str(path or "").strip()
    if not cleaned:
        return False
    return any(
        cleaned == prefix.rstrip("/") or cleaned.startswith(prefix)
        for prefix in INTERNAL_CANDIDATE_PATH_PREFIXES
    )


def _candidate_artifact_exposure_reasons(
    artifact: dict[str, Any],
    *,
    primary_kind: str,
) -> list[str]:
    path = str(artifact.get("path") or "").strip()
    kind = str(artifact.get("kind") or "").strip().lower()
    visibility = str(artifact.get("visibility") or "user_facing").strip().lower()
    package_candidate = (
        primary_kind == "package"
        and kind in {"package", "final_package"}
        and path.startswith("workspace/outputs/")
    )

    reasons: list[str] = []
    if visibility == "internal":
        reasons.append("raw_artifact_exposed_as_final")
    elif visibility and visibility not in USER_FACING_ARTIFACT_VISIBILITIES:
        reasons.append("candidate_artifact_visibility_unsupported")

    if not package_candidate and _is_internal_candidate_path(path):
        reasons.append("raw_artifact_exposed_as_final")
    return reasons


def _build_finalization_guidance(state: dict[str, Any]) -> list[str]:
    working_memory = state.get("working_memory") or {}
    deliverable = working_memory.get("deliverable")
    has_structured_outputs = bool(
        (working_memory.get("output_contract") or {}).get("outputs")
    )
    opening_guidance = (
        "Before setting should_complete=true, run a human-ready finalization loop: infer the user need, map the reviewable files to working_memory.output_contract.outputs, inspect them as the recipient, fix blocking defects, and record the trace in result.finalization."
        if has_structured_outputs
        else "Before setting should_complete=true, run a human-ready finalization loop: infer the user need, choose the recipient and primary deliverable kind, draft the deliverable, inspect it as the recipient, fix blocking defects, and record the trace in result.finalization."
    )
    guidance = [
        opening_guidance,
        "Synthesis notes, raw JSON/CSV/XLSX, SQLite dumps, iteration logs, and workspace files are internal artifacts until they are turned into a user-facing deliverable.",
        "List internal work in result.finalization.internal_artifacts; list only reviewable outputs in result.finalization.candidate_artifacts.",
        "For each candidate artifact, set id, path, role, visibility, and media_type when known. Use role='primary_deliverable' for the main reviewable output when output_contract.outputs is present; legacy single-kind tasks may still use role='primary'.",
        "Set result.finalization.status='passed' only when blocking_defects is empty and validation_evidence records what was actually checked.",
        "Keep delivery.review_ready separate from delivery.ready: worker finalization can reach review, but approval or mark-delivered makes it delivery-ready.",
        "For multiple reviewable outputs, list each required user-facing output in working_memory.output_contract.outputs with id, role, required, media_type, and optional relation fields; then list produced files in result.finalization.candidate_artifacts with matching id, role, media_type, path, visibility, and optional relation fields.",
        "Use source_for and derived_from to declare artifact provenance by id when one artifact is the editable/provenance source for another or was generated from another. Do not call a lifecycle summary an editable source unless it is actually the declared source artifact for that output.",
        "Directory/package outputs are still allowed when explicitly useful, but they are one possible container shape, not the default substitute for multiple reviewable outputs.",
    ]
    if deliverable:
        hint_action = (
            "Use it to shape the declared outputs"
            if has_structured_outputs
            else "Use it to choose the primary deliverable"
        )
        guidance.append(
            f"Requested deliverable hint: {deliverable}. {hint_action}, but adapt the final shape to the real user need."
        )
    return guidance


def _load_rules_profile() -> dict[str, Any]:
    candidate = RULES_PROFILE_PATH
    if candidate.is_file():
        content = candidate.read_text(encoding="utf-8")
        truncated = len(content) > RULES_PROFILE_MAX_CHARS
        if truncated:
            content = content[:RULES_PROFILE_MAX_CHARS].rstrip() + "\n"
        return {
            "exists": True,
            "path": str(candidate),
            "content": content,
            "truncated": truncated,
            "max_chars": RULES_PROFILE_MAX_CHARS,
        }

    return {
        "exists": False,
        "path": str(candidate),
        "content": "",
        "truncated": False,
        "max_chars": RULES_PROFILE_MAX_CHARS,
    }


def stale_lock(state: dict[str, Any]) -> bool:
    lock = state["lock"]
    if lock.get("status") != "held" or not lock.get("started_at"):
        return False
    started = parse_ts(lock.get("started_at"))
    if not started:
        return False
    now = dt.datetime.now(dt.timezone.utc)
    timeout_min = effective_lock_stale_timeout_min(state)
    return (now - started).total_seconds() > timeout_min * 60


def clear_reviewable_candidate(state: dict[str, Any]) -> None:
    state.setdefault("artifacts", {})["final_report_path"] = None
    delivery = state.setdefault("delivery", {})
    delivery["primary_file"] = None
    delivery["review_ready"] = False
    delivery["ready"] = False


def make_work_order(state: dict[str, Any], task: ResearchTask) -> dict[str, Any]:
    lock = state["lock"]
    run_id = lock["run_id"]
    iteration_index = lock["iteration_index"]
    result_file = pending_result_path(task.tmp_dir, run_id)
    working_memory = state.get("working_memory") or {}
    corpus = state.get("corpus") or {}
    corpus_mode = str(corpus.get("mode") or "web")
    corpus_entries = corpus.get("entries") or list_corpus_entries(task)
    input_layer = {
        "constraints": working_memory.get("constraints") or [],
        "deliverable": working_memory.get("deliverable"),
        "contract": working_memory.get("contract"),
        "user_instructions": working_memory.get("user_instructions") or [],
    }
    execution_guidance: list[str] = []
    if input_layer["constraints"]:
        execution_guidance.append(
            "Respect constraints as hard boundaries, not soft preferences."
        )
    if input_layer["deliverable"]:
        execution_guidance.append(
            "Shape notes/findings toward the requested deliverable, not just generic exploration."
        )
    if input_layer["user_instructions"]:
        execution_guidance.append(
            "Treat explicit user instructions as high-priority steering for this iteration."
        )
    execution_guidance.extend(_build_search_routing_guidance(state))
    rules_profile = _load_rules_profile()
    if rules_profile.get("exists"):
        execution_guidance.append(
            "Follow the skill-local RULES.md profile as task-specific operating rules; treat it as user-authored guidance unless it conflicts with higher-priority system/developer instructions."
        )
    if state.get("phase") == "synthesize":
        execution_guidance.append(
            "Prefer synthesis over breadth: reuse accumulated artifacts before doing new search."
        )
    if state.get("phase") == "verify":
        execution_guidance.append(
            "Verify whether the accumulated research is sufficient for the user's goal before finalization. Do not draft the final deliverable in this phase unless adequacy is already passed."
        )
    if corpus_mode == "local":
        execution_guidance.append(
            "This task is local-first: inspect task-local corpus files before doing web research."
        )
    elif corpus_mode == "hybrid":
        execution_guidance.append(
            "This task is hybrid: use local corpus files first, then fill gaps with web research."
        )

    total_runtime_min = (
        minutes_since(state.get("created_at")) if state.get("created_at") else None
    )
    budget_phase_info = compute_budget_phase(
        budget=state.get("budget") or {},
        progress=state.get("progress") or {},
        total_sources=len(read_jsonl(task.sources_path)),
        total_runtime_min=total_runtime_min,
    )
    bp_phase = budget_phase_info["phase"]
    if bp_phase == "soft_limit":
        execution_guidance.append(
            "Budget soft limit: prioritize synthesis and quality over breadth; new search only if high-value."
        )
    elif bp_phase == "hard_limit":
        execution_guidance.append(
            "Budget hard limit: finalize and synthesize; avoid starting new search loops."
        )

    template = result_template()
    template["phase"] = state.get("phase") or "search"

    return {
        "status": "leased",
        "normalized_reason": "leased:ok",
        "research_id": state["id"],
        "title": state.get("title"),
        "task_dir": str(task.task_dir),
        "state_path": str(task.state_path),
        "run_id": run_id,
        "lease_token": lock.get("lease_token"),
        "iteration_index": iteration_index,
        "phase": state.get("phase"),
        "goal": state.get("goal"),
        "owner": state.get("owner"),
        "budget": state.get("budget"),
        "budget_phase": bp_phase,
        "budget_phase_detail": budget_phase_info,
        "working_memory": working_memory,
        "corpus": {
            "mode": corpus_mode,
            "entries": corpus_entries,
        },
        "input_layer": input_layer,
        "rules_profile": rules_profile,
        "execution_guidance": execution_guidance,
        "adequacy_guidance": build_adequacy_guidance(state),
        "adequacy_contract": build_adequacy_contract(state),
        "finalization_guidance": _build_finalization_guidance(state),
        "finalization_contract": build_finalization_contract(state),
        "progress": state.get("progress"),
        "paths": {
            "result_file": str(result_file),
            "sources_path": str(task.sources_path),
            "findings_path": str(task.findings_path),
            "iteration_path": str(task.iterations_dir / f"{iteration_index:03d}.md"),
            "final_report_path": str(task.final_report_path),
            "input_dir": str(task.input_dir),
            "corpus_dir": str(task.corpus_dir),
            "corpus_manifest_path": str(task.corpus_manifest_path),
            "workspace_dir": str(task.workspace_dir),
            "workspace_analysis_dir": str(task.workspace_analysis_dir),
            "workspace_tools_dir": str(task.workspace_tools_dir),
            "workspace_data_dir": str(task.workspace_data_dir),
            "workspace_outputs_dir": str(task.workspace_outputs_dir),
            "workspace_tmp_dir": str(task.workspace_tmp_dir),
            "workspace_screenshots_dir": str(task.workspace_screenshots_dir),
            "workspace_vision_dir": str(task.workspace_vision_dir),
            "sqlite_db_path": str(task.sqlite_db_path),
            "sqlite_schema_path": str(task.sqlite_schema_path),
            "sqlite_queries_dir": str(task.sqlite_queries_dir),
            "sqlite_imports_dir": str(task.sqlite_imports_dir),
            "runtime_dir": str(task.runtime_dir),
            "venv_dir": str(task.venv_dir),
            "runtime_meta_path": str(task.runtime_meta_path),
        },
        "result_template": template,
    }


def render_default_final_report(
    task: ResearchTask,
    state: dict[str, Any],
    payload: dict[str, Any],
    iteration_index: int,
) -> str:
    synthesis = build_synthesis_payload(
        task, state, findings_limit=20, sources_limit=20
    )
    lines = [
        f"# {state.get('title') or state['id']}",
        "",
        "## Goal",
        "",
        state.get("goal") or "",
        "",
        "## Final summary",
        "",
        payload["summary"],
        "",
    ]

    working_summary = synthesis.get("working_summary")
    if (
        working_summary
        and working_summary.strip()
        and working_summary.strip() != payload["summary"].strip()
    ):
        lines.extend(["## Working synthesis context", "", working_summary, ""])

    constraints = synthesis.get("constraints") or []
    if constraints:
        lines.extend(["## Constraints", ""])
        for item in constraints:
            lines.append(f"- {item}")
        lines.append("")

    deliverable = synthesis.get("deliverable")
    if deliverable:
        lines.extend(["## Requested deliverable", "", deliverable, ""])

    user_instructions = synthesis.get("user_instructions") or []
    if user_instructions:
        lines.extend(["## User instructions", ""])
        for item in user_instructions:
            lines.append(f"- {item}")
        lines.append("")

    findings = synthesis.get("findings") or payload.get("findings") or []
    sources = synthesis.get("sources") or payload.get("sources") or []
    enriched_findings = enrich_findings_with_provenance(findings, sources)
    if enriched_findings:
        lines.extend(["## Key findings", ""])
        for finding in enriched_findings:
            kind = finding.get("kind") or "note"
            text = finding.get("text") or ""
            provenance = finding.get("provenance") or {}
            badge = render_confidence_badge(provenance.get("tier", "unknown"))
            refs = finding.get("source_urls") or []
            bullet = f"- **{kind}** {badge}: {text}"
            if refs:
                bullet += f" (refs: {', '.join(refs)})"
            conf_note_parts = []
            tier = provenance.get("tier")
            src_count = provenance.get("source_count", 0)
            if tier and tier != "unknown":
                conf_note_parts.append(f"confidence={tier}")
            if src_count:
                conf_note_parts.append(f"sources={src_count}")
            if conf_note_parts:
                bullet += f" [{', '.join(conf_note_parts)}]"
            lines.append(bullet)
        lines.append("")

    open_questions = (
        synthesis.get("open_questions") or payload.get("open_questions") or []
    )
    if open_questions:
        lines.extend(["## Remaining open questions", ""])
        for question in open_questions:
            lines.append(f"- {question}")
        lines.append("")

    next_angle = payload.get("next_angle") or synthesis.get("next_angle")
    if next_angle:
        lines.extend(["## Next angle / follow-up", "", next_angle, ""])

    sources = synthesis.get("sources") or payload.get("sources") or []
    if sources:
        lines.extend(["## Evidence base", ""])
        for source in sources:
            title = source.get("title") or source.get("url") or "untitled source"
            url = source.get("url")
            note = source.get("note")
            quality = compute_source_quality_score(source)
            qbadge = (
                {"strong": "●●", "standard": "●○", "weak": "○○", "poor": "··"}
            ).get(quality["tier"], "??")
            bullet = f"- [{qbadge}] " + (f"[{title}]({url})" if url else title)
            if quality["factors"]:
                bullet += f" (quality: {', '.join(quality['factors'])})"
            if note:
                bullet += f" — {note}"
            lines.append(bullet)
        lines.append("")

    saturation = synthesis.get("saturation") or {}
    lines.extend(
        [
            "## Metadata",
            "",
            f"- Finalized on iteration {iteration_index}",
            f"- Total findings accumulated: {synthesis.get('totals', {}).get('findings', 0)}",
            f"- Total sources accumulated: {synthesis.get('totals', {}).get('sources', 0)}",
            f"- Topic saturated: {'yes' if saturation.get('topic_saturated') else 'no'}",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def compute_low_yield(metrics: dict[str, int], payload: dict[str, Any]) -> bool:
    return (
        metrics.get("new_sources", 0) == 0
        and metrics.get("new_findings", 0) == 0
        and not payload.get("meaningful_progress", True)
    )


def _markdown_table_cells(line: str) -> list[str]:
    return [cell.strip().lower() for cell in line.strip().strip("|").split("|")]


def _is_markdown_table_separator(line: str) -> bool:
    cells = _markdown_table_cells(line)
    return bool(cells) and all(re.match(r"^:?-{3,}:?$", cell or "") for cell in cells)


def _markdown_table_shapes(report_text: str) -> list[dict[str, Any]]:
    lines = [line.rstrip() for line in str(report_text or "").splitlines()]
    tables: list[dict[str, Any]] = []
    for index, line in enumerate(lines[:-1]):
        if "|" not in line or not _is_markdown_table_separator(lines[index + 1]):
            continue

        headers = _markdown_table_cells(line)
        column_count = len(headers)
        data_rows = 0
        for data_line in lines[index + 2 :]:
            if "|" not in data_line or _is_markdown_table_separator(data_line):
                break
            cells = _markdown_table_cells(data_line)
            if any(cell for cell in cells):
                data_rows += 1

        tables.append(
            {
                "columns": column_count,
                "data_rows": data_rows,
                "start_line": index + 1,
            }
        )
    return tables


def detect_comparative_structure(
    report_text: str,
    *,
    min_rows: int = 2,
    min_columns: int = 2,
) -> dict[str, Any]:
    tables = _markdown_table_shapes(report_text)
    matched_tables = [
        table
        for table in tables
        if table["data_rows"] >= min_rows and table["columns"] >= min_columns
    ]
    return {
        "passed": bool(matched_tables),
        "signals": ["table_shape"] if matched_tables else [],
        "table_count": len(tables),
        "matched_tables": matched_tables,
    }


def inspect_deliverable_requirements(
    deliverable: str,
    report_markdown: str,
    *,
    payload: dict[str, Any],
    total_sources: int,
    total_findings: int,
    output_contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    report = str(report_markdown or "")
    lines = [line.rstrip() for line in report.splitlines()]
    bullet_count = sum(
        1 for line in lines if re.match(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)", line)
    )
    pre_metadata_lines: list[str] = []
    for line in lines:
        if line.strip() == "## Metadata":
            break
        pre_metadata_lines.append(line)
    pre_metadata_bullet_count = sum(
        1
        for line in pre_metadata_lines
        if re.match(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)", line)
    )
    non_heading_lines = sum(
        1
        for line in lines
        if line.strip() and not line.lstrip().startswith("#")
    )

    checks: list[dict[str, Any]] = []
    reasons: list[str] = []
    quality_checks = []
    if isinstance(output_contract, dict):
        quality_checks = output_contract.get("quality_checks") or []
    if not isinstance(quality_checks, list):
        quality_checks = []

    for raw_check in quality_checks:
        if not isinstance(raw_check, dict):
            continue
        check_kind = str(raw_check.get("kind") or "").strip().lower()
        if check_kind == "minimum_length":
            min_chars = int(raw_check.get("min_chars") or 0)
            min_non_heading_lines = int(raw_check.get("min_non_heading_lines") or 0)
            passed = len(report) >= min_chars and non_heading_lines >= min_non_heading_lines
            checks.append(
                {
                    "kind": "minimum_length",
                    "passed": passed,
                    "char_count": len(report),
                    "minimum_chars": min_chars,
                    "non_heading_lines": non_heading_lines,
                    "minimum_non_heading_lines": min_non_heading_lines,
                }
            )
            if not passed:
                reasons.append("deliverable_minimum_length_unmet")
        elif check_kind == "bullet_list":
            min_items = int(raw_check.get("min_items") or 2)
            passed = pre_metadata_bullet_count >= min_items
            checks.append(
                {
                    "kind": "bullet_list",
                    "passed": passed,
                    "bullet_count": bullet_count,
                    "pre_metadata_bullet_count": pre_metadata_bullet_count,
                    "minimum_bullets": min_items,
                }
            )
            if not passed:
                reasons.append("deliverable_bullet_list_unstructured")
        elif check_kind == "comparative_matrix":
            min_rows = int(raw_check.get("min_rows") or 2)
            min_columns = int(raw_check.get("min_columns") or 2)
            comparative_structure = detect_comparative_structure(
                report,
                min_rows=min_rows,
                min_columns=min_columns,
            )
            passed = bool(comparative_structure.get("passed"))
            checks.append(
                {
                    "kind": "comparative_matrix",
                    "passed": passed,
                    "structure_signals": comparative_structure.get("signals") or [],
                    "structure_table_count": comparative_structure.get("table_count") or 0,
                    "matched_structures": comparative_structure.get("matched_tables") or [],
                    "minimum_rows": min_rows,
                    "minimum_columns": min_columns,
                }
            )
            if not passed:
                reasons.append("deliverable_comparative_shape_weak")

    return {
        "checks": checks,
        "reasons": reasons,
        "report_metrics": {
            "bullet_count": bullet_count,
            "pre_metadata_bullet_count": pre_metadata_bullet_count,
            "non_heading_lines": non_heading_lines,
        },
    }


def inspect_deliverable_contract(
    report_markdown: str,
    contract: dict[str, Any] | None,
) -> dict[str, Any]:
    if not contract:
        return {
            "check": "deliverable_contract",
            "passed": True,
            "reasons": [],
            "skipped": True,
        }

    reasons: list[str] = []
    required_sections: list[str] = contract.get("required_sections") or []
    required_sheets: list[str] = contract.get("required_sheets") or []

    lines = report_markdown.splitlines()
    heading_lines = {}
    for line in lines:
        m = re.match(r"^#+\s+(.+?)\s*$", line)
        if m:
            heading_lines[m.group(1).strip().lower()] = m.group(1).strip()

    missing_sections: list[str] = []
    for section in required_sections:
        section_lower = str(section).strip().lower()
        if section_lower not in heading_lines:
            missing_sections.append(str(section).strip())
            reasons.append(f"required_section_missing:{section_lower}")

    sheet_missing: list[str] = []
    for sheet in required_sheets:
        sheet_lower = str(sheet).strip().lower()
        if sheet_lower not in {s.lower() for s in heading_lines.values()}:
            sheet_missing.append(str(sheet).strip())
            reasons.append(f"required_sheet_missing:{sheet_lower}")

    passed = not missing_sections and not sheet_missing

    return {
        "check": "deliverable_contract",
        "passed": passed,
        "reasons": reasons,
        "skipped": False,
        "required_sections": required_sections,
        "present_sections": list(heading_lines.keys()),
        "missing_sections": missing_sections,
        "required_sheets": required_sheets,
        "sheet_missing": sheet_missing,
    }


def validate_completion(
    task: ResearchTask,
    state: dict[str, Any],
    payload: dict[str, Any],
    *,
    phase: str,
    report_markdown: str,
    triggered_by: str,
) -> dict[str, Any]:
    reasons: list[str] = []
    report_text = str(report_markdown or "").strip()
    working_memory = state.get("working_memory") or {}
    deliverable = str(working_memory.get("deliverable") or "").strip()
    total_sources = len(read_jsonl(task.sources_path))
    total_findings = len(read_jsonl(task.findings_path))

    if not report_text:
        reasons.append("final_report_empty")
    if working_memory.get("deliverable") is not None and not deliverable:
        reasons.append("deliverable_lost")
    if (
        total_sources <= 0
        and total_findings <= 0
        and triggered_by not in {"topic_saturated", "budget"}
    ):
        reasons.append("evidence_base_empty")
    budget_triggered = triggered_by == "budget"
    if (
        phase != "synthesize"
        and not bool(payload.get("should_complete"))
        and not budget_triggered
    ):
        reasons.append("phase_not_ready_for_completion")

    deliverable_validation = inspect_deliverable_requirements(
        deliverable,
        report_text,
        payload=payload,
        total_sources=total_sources,
        total_findings=total_findings,
        output_contract=working_memory.get("output_contract"),
    )
    reasons.extend(
        item
        for item in deliverable_validation.get("reasons", [])
        if item not in reasons
    )

    return {
        "passed": not reasons,
        "reasons": reasons,
        "triggered_by": triggered_by,
        "phase": phase,
        "report_bytes": len(report_text.encode("utf-8")) if report_text else 0,
        "deliverable_present": bool(deliverable),
        "deliverable_validation": deliverable_validation,
        "total_sources": total_sources,
        "total_findings": total_findings,
    }


def compose_finish_update_text(
    state: dict[str, Any],
    payload: dict[str, Any],
    next_status: str,
    *,
    iteration_count: int,
    final_report_path: str | None,
) -> str | None:
    title = state.get("title") or state.get("id") or "исследование"
    summary = payload.get("summary") or ""
    next_angle = payload.get("next_angle") or ""
    open_questions = payload.get("open_questions") or []
    findings = payload.get("findings") or []
    findings_block: list[str] = []
    for finding in findings[:3]:
        text = (finding.get("text") or "").strip()
        if text:
            findings_block.append(f"- {text}")

    if next_status == "complete":
        lines = [
            f"Исследование «{title}» завершено.",
            f"Итог: {summary}",
        ]
        if findings_block:
            lines.append("Ключевое:")
            lines.extend(findings_block)
        if final_report_path:
            lines.append("Финальный отчёт готов.")
        return "\n".join(lines)

    if next_status == "awaiting_review":
        lines = [
            f"Исследование «{title}» готово к ревью.",
            f"Итог: {summary}",
        ]
        if findings_block:
            lines.append("Ключевое:")
            lines.extend(findings_block)
        if final_report_path:
            lines.append("Финальный отчёт подготовлен и ждёт проверки.")
        return "\n".join(lines)

    notify = payload.get("notify_recommendation")
    if notify == "blocker":
        lines = [
            f"По исследованию «{title}» нужен твой ввод.",
            f"Сейчас: {summary}",
        ]
        if open_questions:
            lines.append("Что нужно уточнить:")
            lines.extend(f"- {question}" for question in open_questions[:3])
        elif next_angle:
            lines.append(f"Подвисший следующий шаг: {next_angle}")
        return "\n".join(lines)

    if notify in {"milestone", "auto"}:
        lines = [
            f"Апдейт по исследованию «{title}».",
            f"Прогресс: {summary}",
            f"Итераций: {iteration_count}",
        ]
        if findings_block:
            lines.append("Что уже нашлось:")
            lines.extend(findings_block)
        if next_angle:
            lines.append(f"Дальше копаю: {next_angle}")
        return "\n".join(lines)

    return None


def compose_failure_update_text(
    state: dict[str, Any], error_message: str, next_status: str
) -> str | None:
    title = state.get("title") or state.get("id") or "исследование"
    if next_status == "cancelled":
        return (
            f"Исследование «{title}» остановлено. Последний контекст: {error_message}"
        )
    if next_status == "failed":
        return f"Исследование «{title}» упёрлось в блокер и остановилось. Ошибка: {error_message}"
    return None


def should_notify(
    state: dict[str, Any], payload: dict[str, Any], next_status: str
) -> bool:
    policy = payload["notify_recommendation"]
    if policy == "silent":
        return False
    if policy == "final":
        return next_status in {"awaiting_review", "complete"}
    if policy in {"blocker", "milestone"}:
        return True
    if next_status in {"complete", "failed", "cancelled"}:
        return True
    if not payload["meaningful_progress"]:
        return False
    meaningful_iterations = int(state["progress"].get("meaningful_iterations") or 0)
    milestone_every = int(state["delivery"].get("milestone_every_iterations") or 2)
    if milestone_every <= 0:
        milestone_every = 2
    return meaningful_iterations > 0 and meaningful_iterations % milestone_every == 0


def validate_candidate_final(
    task: ResearchTask,
    state: dict[str, Any],
    payload: dict[str, Any],
    *,
    report_markdown: str | None = None,
) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    all_passed = True
    if report_markdown is None:
        report_markdown = str(payload.get("final_report_markdown") or "")
    working_memory = state.get("working_memory") or {}

    output_contract = working_memory.get("output_contract") or {}
    finalization_check = _check_finalization_trace(
        payload.get("finalization"),
        report_markdown,
        output_contract=output_contract,
    )
    findings.append(finalization_check)
    if not finalization_check["passed"]:
        all_passed = False

    artifact_check = inspect_candidate_artifacts(
        task_dir=task.task_dir,
        final_report_path=task.final_report_path,
        finalization=payload.get("finalization"),
        report_markdown=report_markdown,
        output_contract=output_contract,
    )
    findings.append(artifact_check)
    if not artifact_check["passed"]:
        all_passed = False

    format_decision_check = check_deliverable_format_decision(
        state=state,
        finalization=payload.get("finalization"),
        report_markdown=report_markdown,
        artifact_check=artifact_check,
    )
    findings.append(format_decision_check)
    if not format_decision_check["passed"]:
        all_passed = False
    output_decision = build_output_decision(
        output_contract=working_memory.get("output_contract") or {},
        finalization=payload.get("finalization"),
    )
    structured_output_final = (
        artifact_check.get("mode") == "output_contract"
        and artifact_check.get("passed")
        and bool(output_decision)
    )

    primary_kind = str(
        (payload.get("finalization") or {}).get("primary_deliverable_kind") or ""
    ).strip().lower()
    package_final = (
        primary_kind == "package"
        and artifact_check["passed"]
        and any(
            item.get("format") == "package"
            for item in artifact_check.get("artifacts") or []
        )
    )

    if package_final:
        findings.append(
            {
                "check": "package_deliverable_quality",
                "passed": True,
                "reasons": [],
            }
        )
    elif structured_output_final:
        findings.append(
            {
                "check": "deliverable_quality",
                "passed": True,
                "reasons": [],
                "skipped": True,
                "reason": "Structured output artifact inspection is authoritative for reviewable output quality.",
            }
        )
    else:
        deliverable_check = _check_deliverable_quality(report_markdown)
        findings.append(deliverable_check)
        if not deliverable_check["passed"]:
            all_passed = False

    if structured_output_final:
        findings.append(
            {
                "check": "human_readiness",
                "passed": True,
                "reasons": [],
                "skipped": True,
                "reason": "Structured output artifact inspection confirmed the reviewable deliverable.",
            }
        )
    else:
        human_readiness_check = _check_human_readiness(report_markdown)
        findings.append(human_readiness_check)
        if not human_readiness_check["passed"]:
            all_passed = False

    manifest_check = _check_delivery_manifest(state)
    findings.append(manifest_check)
    if not manifest_check["passed"]:
        all_passed = False

    contract_check = inspect_deliverable_contract(
        report_markdown, working_memory.get("contract")
    )
    findings.append(contract_check)
    if not contract_check["passed"]:
        all_passed = False

    reasons: list[str] = []
    for finding in findings:
        for reason in finding.get("reasons") or []:
            if reason not in reasons:
                reasons.append(reason)

    return {
        "passed": all_passed,
        "findings": findings,
        "reasons": reasons,
        "status": "passed" if all_passed else "rejected",
        "deliverable_decision": {
            key: format_decision_check.get(key)
            for key in (
                "selected_kind",
                "desired_kind",
                "feasible_kind",
                "reason",
                "source",
                "alternatives_considered",
            )
            if key in format_decision_check
        },
        "output_decision": output_decision,
    }


def _check_finalization_trace(
    finalization: dict[str, Any] | None,
    report_markdown: str,
    *,
    output_contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    reasons: list[str] = []
    trace = finalization or {}
    status = trace.get("status")
    if status in (None, "", "not_started"):
        reasons.append("finalization_not_started")
    elif status != "passed":
        reasons.append("finalization_not_passed")

    blocking_defects = trace.get("blocking_defects") or []
    if blocking_defects:
        reasons.append("finalization_blocking_defects")

    validation_evidence = trace.get("validation_evidence") or []
    if status == "passed" and not validation_evidence:
        reasons.append("primary_deliverable_unvalidated")

    candidate_artifacts = trace.get("candidate_artifacts") or []
    primary_kind = str(trace.get("primary_deliverable_kind") or "").strip().lower()
    has_structured_outputs = bool((output_contract or {}).get("outputs"))
    report_text = str(report_markdown or "").strip()
    if status == "passed" and not candidate_artifacts and not report_text:
        reasons.append("primary_deliverable_missing")

    if status == "passed":
        for artifact in candidate_artifacts:
            if isinstance(artifact, dict):
                for reason in _candidate_artifact_exposure_reasons(
                    artifact,
                    primary_kind=primary_kind,
                ):
                    if reason not in reasons:
                        reasons.append(reason)

    if status == "passed":
        if not str(trace.get("inferred_user_need") or "").strip():
            reasons.append("user_facing_quality_weak")
        if not primary_kind and not has_structured_outputs:
            reasons.append("primary_deliverable_missing")

    return {
        "check": "finalization_trace",
        "passed": not reasons,
        "reasons": reasons,
        "status": status,
        "primary_deliverable_kind": primary_kind or None,
        "candidate_artifacts_count": len(candidate_artifacts),
        "validation_evidence_count": len(validation_evidence),
        "blocking_defects_count": len(blocking_defects),
    }


def _check_delivery_manifest(state: dict[str, Any]) -> dict[str, Any]:
    from pathlib import Path

    delivery = state.get("delivery") or {}
    primary_file = delivery.get("primary_file")
    if not primary_file:
        return {
            "check": "delivery_manifest",
            "passed": True,
            "reasons": [],
        }

    path = Path(primary_file)
    if not path.is_absolute():
        task_dir = Path(state.get("artifacts", {}).get("task_dir", "."))
        path = task_dir / path

    passed = path.exists()
    reasons = [] if passed else ["primary_file_not_found"]

    return {
        "check": "delivery_manifest",
        "passed": passed,
        "reasons": reasons,
        "primary_file": primary_file,
    }


def _check_deliverable_quality(report_markdown: str) -> dict[str, Any]:
    report_lines = [
        line.strip() for line in report_markdown.splitlines() if line.strip()
    ]

    passed = True
    reasons: list[str] = []

    if not report_markdown.strip():
        passed = False
        reasons.append("final_report_empty")
    else:
        meaningful_lines = [
            line
            for line in report_lines
            if not line.startswith("#") and not line.startswith("```")
        ]
        if len(meaningful_lines) < 3:
            passed = False
            reasons.append("final_report_too_short")
        if len(report_markdown) < 200:
            passed = False
            reasons.append("final_report_truncated")

    return {
        "check": "deliverable_quality",
        "passed": passed,
        "reasons": reasons,
    }


def _check_human_readiness(report_markdown: str) -> dict[str, Any]:
    passed = True
    reasons: list[str] = []

    if len(report_markdown) < 200:
        passed = False
        reasons.append("report_too_short_for_human")
    else:
        words = report_markdown.split()
        if len(words) < 30:
            passed = False
            reasons.append("report_insufficient_content")

    return {
        "check": "human_readiness",
        "passed": passed,
        "reasons": reasons,
    }

CONFIDENCE_TIERS = {"high", "medium", "low", "reserve"}


def compute_confidence_score(
    finding: dict[str, Any],
    all_sources: list[dict[str, Any]],
    source_scores: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    source_urls = finding.get("source_urls") or []
    source_count = len(source_urls)
    kind = str(finding.get("kind") or "note").lower()

    if source_scores is None:
        source_scores = {}

    contributing_sources: list[dict[str, Any]] = []
    total_source_quality = 0.0
    for url in source_urls:
        src = next((s for s in all_sources if s.get("url") == url), None)
        if src:
            contributing_sources.append(src)
            score = source_scores.get(url, {})
            total_source_quality += float(score.get("quality_score", 0.5))

    if not contributing_sources:
        tier = "reserve"
        confidence = 0.0
        reason = "no_verifiable_source"
    elif source_count >= 3:
        avg_quality = total_source_quality / len(contributing_sources)
        tier = "high" if avg_quality >= 0.7 else "medium"
        confidence = min(0.95, 0.5 + avg_quality * 0.45)
        reason = "multi_source_corroborated"
    elif source_count == 2:
        avg_quality = total_source_quality / len(contributing_sources)
        tier = "high" if avg_quality >= 0.8 else "medium"
        confidence = min(0.85, 0.45 + avg_quality * 0.40)
        reason = "dual_source"
    else:
        single_score = total_source_quality if contributing_sources else 0.5
        tier = "medium" if single_score >= 0.6 else "low"
        confidence = min(0.7, 0.3 + single_score * 0.4)
        reason = "single_source"

    if kind in ("estimate", "hypothesis", "note"):
        if tier == "high":
            tier = "medium"
            confidence = round(confidence * 0.8, 3)
            reason = f"{reason};softened_by_kind"
        elif tier == "medium":
            tier = "low"
            confidence = round(confidence * 0.7, 3)
            reason = f"{reason};softened_by_kind"

    if finding.get("downgraded_to_reserve"):
        tier = "reserve"
        confidence = 0.1
        reason = "downgraded_to_reserve"

    return {
        "tier": tier,
        "confidence": round(confidence, 3),
        "source_count": source_count,
        "reason": reason,
        "provenance_refs": [
            {
                "url": src.get("url"),
                "title": src.get("title"),
            }
            for src in contributing_sources
        ],
    }


def compute_source_quality_score(source: dict[str, Any]) -> dict[str, Any]:
    url = str(source.get("url") or "")
    fetched_at = source.get("fetched_at") or source.get("recorded_at")
    score = 0.5
    factors: list[str] = []

    if fetched_at:
        try:
            fetched_ts = parse_ts(fetched_at)
            if fetched_ts:
                age_days = (dt.datetime.now(dt.timezone.utc) - fetched_ts).days
                if age_days <= 30:
                    score += 0.1
                    factors.append("fresh_30d")
                elif age_days <= 90:
                    score += 0.05
                    factors.append("fresh_90d")
                elif age_days >= 365:
                    score -= 0.1
                    factors.append("stale_over_1yr")
        except (TypeError, ValueError, OverflowError):
            fetched_ts = None

    quality_score = max(0.0, min(1.0, score))

    tier: str
    if quality_score >= 0.75:
        tier = "strong"
    elif quality_score >= 0.55:
        tier = "standard"
    elif quality_score >= 0.35:
        tier = "weak"
    else:
        tier = "poor"

    return {
        "quality_score": round(quality_score, 3),
        "tier": tier,
        "factors": factors,
        "url": url,
        "title": source.get("title"),
    }


def enrich_findings_with_provenance(
    findings: list[dict[str, Any]],
    sources: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_scores: dict[str, dict[str, Any]] = {}
    for src in sources:
        url = src.get("url")
        if url:
            source_scores[str(url)] = compute_source_quality_score(src)

    enriched: list[dict[str, Any]] = []
    for finding in findings:
        confidence_info = compute_confidence_score(finding, sources, source_scores)
        enriched_finding = {**finding, "provenance": confidence_info}
        enriched.append(enriched_finding)
    return enriched


def render_confidence_badge(tier: str) -> str:
    symbols = {
        "high": "[●●●]",
        "medium": "[●●○]",
        "low": "[●○○]",
        "reserve": "[○○○]",
    }
    return symbols.get(tier, "[???]")


def build_revision_diff(
    old_state: dict[str, Any] | None,
    new_state: dict[str, Any],
) -> dict[str, Any]:
    old_review = (old_state or {}).get("review") or {}
    new_review = new_state.get("review") or {}
    old_revision = int(old_review.get("revision_count") or 0)
    new_revision = int(new_review.get("revision_count") or 0)

    old_final_path = (old_state or {}).get("artifacts", {}).get("final_report_path")
    new_final_path = new_state.get("artifacts", {}).get("final_report_path")
    final_report_changed = (
        old_final_path != new_final_path and new_final_path is not None
    )

    changes: list[str] = []
    if new_revision > old_revision:
        changes.append(f"revision_count:{old_revision}->{new_revision}")
    if final_report_changed:
        changes.append("final_report_updated")
    if new_review.get("status") != old_review.get("status") and new_review.get(
        "status"
    ):
        changes.append(
            f"review_status:{old_review.get('status')}->{new_review.get('status')}"
        )

    return {
        "revision_from": old_revision,
        "revision_to": new_revision,
        "changes": changes,
        "final_report_updated": final_report_changed,
    }


def build_evidence_gaps(state: dict[str, Any]) -> dict[str, Any]:
    working_memory = state.get("working_memory") or {}
    open_questions = working_memory.get("open_questions") or []
    finalization = state.get("finalization") or {}
    validation_findings = finalization.get("last_validation_findings") or []
    failed_checks = [f.get("check") for f in validation_findings if not f.get("passed")]
    saturation = state.get("saturation") or {}
    low_yield_streak = int(saturation.get("consecutive_low_yield") or 0)
    budget = state.get("budget") or {}
    max_iter = int(budget.get("max_iterations") or 0)
    progress = state.get("progress") or {}
    iter_count = int(progress.get("iteration_count") or 0)
    budget_headroom = max(0, max_iter - iter_count) if max_iter > 0 else None

    evidence_gaps: list[str] = []
    for q in open_questions:
        evidence_gaps.append(f"open_question:{q}")
    for check in failed_checks:
        evidence_gaps.append(f"failed_validation:{check}")
    if low_yield_streak >= 1:
        evidence_gaps.append(f"low_yield_streak:{low_yield_streak}")
    if budget_headroom is not None and budget_headroom <= 1:
        evidence_gaps.append("budget_almost_exhausted")

    high_risk_assumptions: list[str] = []
    if low_yield_streak >= 2:
        high_risk_assumptions.append("topic_saturation_heuristic_may_be_wrong")
    if failed_checks:
        high_risk_assumptions.append(
            f"deliverable_validation_has_failures:{','.join(failed_checks)}"
        )
    if budget_headroom == 0 and iter_count > 0:
        high_risk_assumptions.append("hard_budget_limit_reached_mid_research")

    recommended_next_checks: list[str] = []
    if failed_checks:
        recommended_next_checks.append(
            f"address_failed_validations:{','.join(failed_checks)}"
        )
    if open_questions:
        recommended_next_checks.append("resolve_open_questions_before_finalizing")
    if evidence_gaps:
        recommended_next_checks.append("review_evidence_gaps_before_presenting_to_user")

    return {
        "evidence_gaps": evidence_gaps,
        "high_risk_assumptions": high_risk_assumptions,
        "recommended_next_checks": recommended_next_checks,
        "has_open_gaps": len(evidence_gaps) > 0,
    }
