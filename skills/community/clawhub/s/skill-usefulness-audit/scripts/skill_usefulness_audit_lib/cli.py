from __future__ import annotations

from .common import *

from .ablation import *
from .community import *
from .risk_quality import *
from .scoring import *
from .reporting import *
from .usage_loader import *

def cli_version() -> str:
    module_path = Path(__file__).resolve()
    roots = list(module_path.parents)
    for root in roots:
        version_path = root / "VERSION"
        if version_path.exists():
            return read_text(version_path).strip()
    for root in roots:
        skill_path = root / "SKILL.md"
        if not skill_path.exists():
            continue
        frontmatter, _body = parse_frontmatter(read_text(skill_path))
        version = str(frontmatter.get("version", "") or "").strip()
        if version:
            return version
    return "unknown"


def existing_paths(label: str, raw_paths: list[str] | None, strict: bool = False) -> list[Path] | None:
    paths = [Path(item).expanduser().resolve() for item in (raw_paths or [])]
    existing: list[Path] = []
    missing = False
    for path in paths:
        if path.exists():
            existing.append(path)
            continue
        missing = True
        level = "error" if strict else "warning"
        print(f"{level}: {label} file not found: {path}", file=sys.stderr)
    if strict and missing:
        return None
    return existing


def path_key(path: Path) -> str:
    return os.path.normcase(str(path.resolve()))


def add_not_audited_entry(
    entries: list[dict[str, str]],
    seen_paths: set[str],
    path: Path,
    reason: str,
) -> None:
    try:
        resolved = path.resolve()
    except OSError:
        resolved = path
    key = os.path.normcase(str(resolved))
    if key in seen_paths:
        return
    seen_paths.add(key)
    entries.append({"path": str(resolved), "reason": reason})


def collect_not_audited_entries(
    roots: list[Path],
    audited_skill_files: list[Path],
    include_system: bool,
    dedupe_install_identity: bool,
) -> list[dict[str, str]]:
    audited = {path_key(path) for path in audited_skill_files}
    entries: list[dict[str, str]] = []
    seen_paths: set[str] = set()

    if not include_system:
        for root in roots:
            if not root.exists():
                continue
            for skill_md in root.rglob("SKILL.md"):
                if "/.system/" in skill_md.as_posix().lower():
                    add_not_audited_entry(entries, seen_paths, skill_md.parent, "system-skipped")

    if dedupe_install_identity:
        for skill_md in discover_skill_files(roots, include_system, dedupe_install_identity=False):
            if path_key(skill_md) not in audited:
                add_not_audited_entry(entries, seen_paths, skill_md.parent, "duplicate-skill-install")

    for root in roots:
        if not root.exists() or (root / "SKILL.md").is_file():
            continue
        try:
            children = sorted((item for item in root.iterdir() if item.is_dir()), key=lambda item: item.as_posix())
        except OSError:
            continue
        for child in children:
            if (child / "SKILL.md").is_file():
                continue
            if not include_system and child.name.lower() == ".system":
                continue
            if any(child.rglob("SKILL.md")):
                continue
            add_not_audited_entry(entries, seen_paths, child, "no-skill-entry")

    return sorted(entries, key=lambda item: (item["reason"], item["path"]))


def _closest_peer(
    skill: dict[str, object],
    skills: list[dict[str, object]],
    alias_counts: Counter,
) -> tuple[str | None, float]:
    best_peer = None
    best_overlap = 0.0
    for other in skills:
        if skill["path"] == other["path"]:
            continue
        overlap = jaccard(skill["terms"], other["terms"])  # type: ignore[arg-type]
        if overlap > best_overlap:
            best_overlap = overlap
            best_peer = skill_display_name(other, alias_counts)
    return best_peer, best_overlap


def _skill_evidence_context(
    skill: dict[str, object],
    skills: list[dict[str, object]],
    alias_counts: Counter,
    usage: dict[str, dict[str, object]],
    history_usage: dict[str, dict[str, object]],
    ablation: dict[str, dict[str, object]],
    community: dict[str, dict[str, object]],
    has_history: bool,
) -> dict[str, object]:
    kind = classify_skill(skill)
    best_peer, best_overlap = _closest_peer(skill, skills, alias_counts)
    evidence_notes: list[str] = []
    usage_record, usage_note = resolve_record(usage, skill, alias_counts)
    if usage_note:
        evidence_notes.append(f"usage={usage_note}")
    usage_source = "usage"
    if usage_record is None:
        usage_record, history_note = resolve_record(history_usage, skill, alias_counts)
        if history_note:
            evidence_notes.append(f"history={history_note}")
        usage_record = usage_record or {"calls": 0}
        usage_source = "history" if has_history else "missing"

    ablation_summary, ablation_note = resolve_record(ablation, skill, alias_counts)
    if ablation_note:
        evidence_notes.append(f"ablation={ablation_note}")
    community_entry, community_note = resolve_record(community, skill, alias_counts)
    if community_note:
        evidence_notes.append(f"community={community_note}")
    community_prior, community_conf, community_breakdown = community_prior_score(community_entry)
    return {
        "kind": kind,
        "best_peer": best_peer,
        "best_overlap": best_overlap,
        "usage_record": usage_record,
        "usage_source": usage_source,
        "evidence_weight": usage_evidence_weight(usage_source),
        "ablation_summary": ablation_summary,
        "community_entry": community_entry,
        "community_prior": community_prior,
        "community_conf": community_conf,
        "community_breakdown": community_breakdown,
        "evidence_note": " | ".join(dict.fromkeys(evidence_notes)) if evidence_notes else None,
        "risk_review": risk_review_summary(
            str(skill["risk_level"]),
            list(skill["risk_evidence"]),  # type: ignore[arg-type]
        ),
        "install_gate": install_gate_summary(
            str(skill["risk_level"]),
            list(skill["risk_evidence"]),  # type: ignore[arg-type]
        ),
    }


def _skill_score_context(
    skill: dict[str, object],
    evidence: dict[str, object],
    skill_count: int,
) -> dict[str, object]:
    usage_record = evidence["usage_record"]  # type: ignore[assignment]
    kind = str(evidence["kind"])
    best_overlap = float(evidence["best_overlap"])
    calls = int(usage_record.get("calls", 0) or 0)  # type: ignore[union-attr]
    u_score = usage_score(usage_record, float(evidence["evidence_weight"]))  # type: ignore[arg-type]
    uniq_score = uniqueness_score(best_overlap)
    i_score = impact_score(kind, calls, best_overlap, skill, evidence["ablation_summary"])
    total = round(u_score + uniq_score + i_score, 2)
    catalog_evidence = catalog_quality_evidence(evidence["best_peer"], best_overlap)
    quality = quality_penalty(skill, usage_record, evidence["ablation_summary"], catalog_evidence)
    quality_penalty_value = float(quality["penalty"])
    pre_health_cap_final = round(clamp(total - quality_penalty_value, 0.0, 10.0), 2)
    health_cap = health_cap_from_quality(list(quality["evidence"]))  # type: ignore[arg-type]
    final = min(pre_health_cap_final, health_cap) if health_cap is not None else pre_health_cap_final
    confidence = confidence_score(
        str(evidence["usage_source"]),
        usage_record,  # type: ignore[arg-type]
        kind,
        evidence["ablation_summary"],
        evidence["community_entry"],
        skill_count,
    )
    action, action_reason, delete_candidate = recommend_action(
        str(skill["source"]),
        kind,
        round(final, 2),
        confidence,
        str(skill["risk_level"]),
        quality_penalty_value,
        calls,
        best_overlap,
        evidence["community_prior"],
    )
    return {
        **evidence,
        "calls": calls,
        "history_mentions": int(usage_record.get("history_mentions", 0) or 0),  # type: ignore[union-attr]
        "suspected_invocations": int(usage_record.get("suspected_invocations", 0) or 0),  # type: ignore[union-attr]
        "u_score": u_score,
        "uniq_score": uniq_score,
        "i_score": i_score,
        "total": total,
        "quality": quality,
        "quality_penalty_value": quality_penalty_value,
        "quality_penalty_uncapped": float(quality["penalty_uncapped"]),
        "quality_flags": list(quality["flags"]),  # type: ignore[arg-type]
        "pre_health_cap_final": pre_health_cap_final,
        "health_cap": health_cap,
        "final": round(final, 2),
        "confidence": confidence,
        "action": action,
        "action_reason": action_reason,
        "advice": action_advice(action, action_reason),
        "delete_candidate": delete_candidate,
    }


def _score_breakdown(skill: dict[str, object], context: dict[str, object]) -> dict[str, object]:
    usage_record = context["usage_record"]  # type: ignore[assignment]
    return {
        "usage": {
            "score": context["u_score"],
            "source": context["usage_source"],
            "evidence_weight": context["evidence_weight"],
            "calls": context["calls"],
            "history_mentions": context["history_mentions"],
            "suspected_invocations": context["suspected_invocations"],
            "recent_30d_calls": coerce_int(usage_record.get("recent_30d_calls")),  # type: ignore[union-attr]
            "recent_90d_calls": coerce_int(usage_record.get("recent_90d_calls")),  # type: ignore[union-attr]
            "last_used_at": usage_record.get("last_used_at"),  # type: ignore[union-attr]
            "executions": coerce_int(usage_record.get("executions")),  # type: ignore[union-attr]
            "script_failures": coerce_int(usage_record.get("script_failures")),  # type: ignore[union-attr]
            "repair_turns": coerce_int(usage_record.get("repair_turns")),  # type: ignore[union-attr]
            "reference_loads": coerce_int(usage_record.get("reference_loads")),  # type: ignore[union-attr]
            "false_triggers": coerce_int(usage_record.get("false_triggers")),  # type: ignore[union-attr]
        },
        "uniqueness": {
            "score": context["uniq_score"],
            "overlap_peer": context["best_peer"],
            "overlap_value": round(float(context["best_overlap"]), 2),
        },
        "impact": {
            "score": context["i_score"],
            "kind": context["kind"],
            "protected_capability": context["kind"] in {"api", "tool"},
            "ablation": context["ablation_summary"],
        },
        "community": {
            "score": context["community_prior"],
            "confidence": context["community_conf"],
            "breakdown": context["community_breakdown"],
        },
        "risk": {
            "level": skill["risk_level"],
            "score": skill["risk_score"],
            "flags": skill["risk_flags"],
            "static_level": skill["static_risk_level"],
            "static_flags": skill["static_risk_flags"],
            "install_gate": context["install_gate"],
        },
        "quality": {
            "penalty": context["quality_penalty_value"],
            "penalty_uncapped": context["quality_penalty_uncapped"],
            "flags": context["quality_flags"],
            "pre_health_cap_final": context["pre_health_cap_final"],
            "health_cap": context["health_cap"],
            "resource_metrics": skill["resource_metrics"],
            "required_env": skill.get("required_env"),
            "missing_required_env": skill.get("missing_required_env"),
        },
        "confidence": {
            "score": context["confidence"],
        },
    }


def _audit_result_record(
    skill: dict[str, object],
    alias_counts: Counter,
    context: dict[str, object],
    has_community: bool,
) -> dict[str, object]:
    usage_record = context["usage_record"]  # type: ignore[assignment]
    quality = context["quality"]  # type: ignore[assignment]
    delete_candidate = bool(context["delete_candidate"])
    return {
        "name": skill["name"],
        "display_name": skill_display_name(skill, alias_counts),
        "source": skill["source"],
        "namespace": skill["namespace"],
        "slug": skill["slug"],
        "skill_key": skill.get("skill_key"),
        "install_identity": skill.get("install_identity"),
        "install_identities": skill.get("install_identities"),
        "metadata": skill.get("metadata"),
        "registry_metadata": skill.get("registry_metadata"),
        "registry_version": skill.get("registry_version"),
        "registry_published_at": skill.get("registry_published_at"),
        "registry_owner_id": skill.get("registry_owner_id"),
        "required_env": skill.get("required_env"),
        "missing_required_env": skill.get("missing_required_env"),
        "kind": context["kind"],
        "path": skill["path"],
        "calls": context["calls"],
        "history_mentions": context["history_mentions"],
        "suspected_invocations": context["suspected_invocations"],
        "recent_30d_calls": coerce_int(usage_record.get("recent_30d_calls")),  # type: ignore[union-attr]
        "recent_90d_calls": coerce_int(usage_record.get("recent_90d_calls")),  # type: ignore[union-attr]
        "active_days": coerce_int(usage_record.get("active_days")),  # type: ignore[union-attr]
        "first_seen_at": usage_record.get("first_seen_at"),  # type: ignore[union-attr]
        "last_used_at": usage_record.get("last_used_at"),  # type: ignore[union-attr]
        "executions": coerce_int(usage_record.get("executions")),  # type: ignore[union-attr]
        "script_failures": coerce_int(usage_record.get("script_failures")),  # type: ignore[union-attr]
        "repair_turns": coerce_int(usage_record.get("repair_turns")),  # type: ignore[union-attr]
        "reference_loads": coerce_int(usage_record.get("reference_loads")),  # type: ignore[union-attr]
        "false_triggers": coerce_int(usage_record.get("false_triggers")),  # type: ignore[union-attr]
        "usage_source": context["usage_source"],
        "evidence_weight": context["evidence_weight"],
        "usage_score": context["u_score"],
        "uniqueness_score": context["uniq_score"],
        "impact_score": context["i_score"],
        "local_score": context["total"],
        "total_score": context["total"],
        "quality_penalty": context["quality_penalty_value"],
        "quality_penalty_uncapped": context["quality_penalty_uncapped"],
        "quality_flags": context["quality_flags"],
        "quality_evidence": quality["evidence"],  # type: ignore[index]
        "resource_metrics": skill["resource_metrics"],
        "final_score": context["final"],
        "confidence_score": context["confidence"],
        "verdict": verdict(float(context["final"]), float(context["confidence"])),
        "action": context["action"],
        "action_reason": context["action_reason"],
        "action_advice": context["advice"],
        "delete_candidate": delete_candidate,
        "delete_trigger": context["action_reason"] if delete_candidate else None,
        "overlap_peer": context["best_peer"],
        "overlap_value": round(float(context["best_overlap"]), 2),
        "community": context["community_entry"],
        "community_prior_score": context["community_prior"],
        "community_confidence": context["community_conf"],
        "community_breakdown": context["community_breakdown"],
        "risk_level": skill["risk_level"],
        "risk_score": skill["risk_score"],
        "risk_flags": skill["risk_flags"],
        "risk_evidence": skill["risk_evidence"],
        "risk_review": context["risk_review"],
        "install_gate": context["install_gate"],
        "static_risk_level": skill["static_risk_level"],
        "static_risk_score": skill["static_risk_score"],
        "static_risk_flags": skill["static_risk_flags"],
        "static_risk_evidence": skill["static_risk_evidence"],
        "score_breakdown": _score_breakdown(skill, context),
        "evidence_note": context["evidence_note"],
        "basis": build_basis(
            usage_record,  # type: ignore[arg-type]
            str(context["usage_source"]),
            float(context["evidence_weight"]),
            context["best_peer"],
            float(context["best_overlap"]),
            str(context["kind"]),
            context["ablation_summary"],
            context["community_prior"],
            list(skill["risk_flags"]),  # type: ignore[arg-type]
            float(context["quality_penalty_value"]),
            context["quality_flags"],  # type: ignore[arg-type]
            context["evidence_note"],
        ),
        "missing_usage": context["usage_source"] == "missing",
        "missing_ablation": context["kind"] == "general" and not context["ablation_summary"],
        "missing_community": has_community and context["community_entry"] is None,
    }


def _build_audit_result(
    skill: dict[str, object],
    skills: list[dict[str, object]],
    alias_counts: Counter,
    usage: dict[str, dict[str, object]],
    history_usage: dict[str, dict[str, object]],
    ablation: dict[str, dict[str, object]],
    community: dict[str, dict[str, object]],
    has_history: bool,
    has_community: bool,
) -> dict[str, object]:
    evidence = _skill_evidence_context(
        skill,
        skills,
        alias_counts,
        usage,
        history_usage,
        ablation,
        community,
        has_history,
    )
    context = _skill_score_context(skill, evidence, len(skills))
    return _audit_result_record(skill, alias_counts, context, has_community)


def _table_report_section(
    language: str,
    title_key: str,
    headers_key: str,
    rows: list[list[str]],
) -> list[str]:
    if not rows:
        return []
    return [
        "",
        f"## {report_text(language, title_key)}",
        "",
        markdown_table(report_headers(language, headers_key), rows),
    ]


def _basis_for_report(item: dict[str, object]) -> str:
    basis = str(item["basis"])
    if str(item["usage_source"]) != "missing":
        return basis
    if basis == "calls=0":
        return "calls=unknown"
    if basis.startswith("calls=0;"):
        return "calls=unknown" + basis[len("calls=0"):]
    return basis


def _score_report_rows(ranked: list[dict[str, object]]) -> list[list[str]]:
    return [
        [
            str(index),
            str(item["display_name"]),
            str(item["source"]),
            str(item["kind"]),
            "-" if str(item["usage_source"]) == "missing" else str(item["calls"]),
            "-" if str(item["usage_source"]) == "missing" else fmt_optional_int(item["recent_30d_calls"]),
            f"{item['usage_score']:.1f}",
            f"{item['uniqueness_score']:.1f}",
            f"{item['impact_score']:.1f}",
            fmt_optional_float(item["community_prior_score"]),
            fmt_optional_float(item["confidence_score"]),
            str(item["risk_level"]),
            fmt_score(item["local_score"]),
            fmt_score(item["quality_penalty"]),
            fmt_score(item["final_score"]),
            str(item["verdict"]),
            str(item["action"]),
            _basis_for_report(item),
        ]
        for index, item in enumerate(ranked, start=1)
    ]


def _ablation_report_section(
    ablation_plan: dict[str, object] | None,
    language: str,
) -> list[str]:
    if not ablation_plan or not ablation_plan["candidate_skills"]:
        return []
    expected_reduction = ablation_plan["model_cost_estimates"]["planned_expected"]["reduction_vs_baseline_percent"]  # type: ignore[index]
    realistic_reduction = expected_reduction["realistic"]  # type: ignore[index]
    baseline_policy = ablation_plan["case_policy"]["baseline_cases_per_general_skill"]  # type: ignore[index]
    rows = [
        [
            str(item["skill"]),
            str(item["priority_score"]),
            str(item["initial_cases"]),
            str(item["expand_to"]),
            str(item["max_cases"]),
            ", ".join(item["priority_reasons"]),
        ]
        for item in ablation_plan["candidates"]  # type: ignore[index]
    ]
    return [
        "",
        f"## {report_text(language, 'cost_ablation_plan')}",
        "",
        f"- {report_pair(language, report_text(language, 'strategy'), ablation_plan['strategy'])}",
        f"- {report_pair(language, report_text(language, 'eligible_general_skills'), ablation_plan['eligible_general_skills'])}",
        f"- {report_pair(language, report_text(language, 'candidate_skills'), ablation_plan['candidate_skills'])}",
        f"- {report_pair(language, report_text(language, 'deferred_general_skills'), ablation_plan['deferred_general_skills'])}",
        f"- {report_pair(language, report_text(language, 'expected_model_cost_reduction').format(baseline_policy=baseline_policy), f'{realistic_reduction}%')}",
        f"- {report_pair(language, report_text(language, 'expected_accuracy_impact'), ablation_plan['accuracy_tradeoff']['expected_accuracy_impact'])}",
        "",
        markdown_table(report_headers(language, "ablation"), rows),
    ]


def _diagnostic_report_sections(
    ranked: list[dict[str, object]],
    language: str,
) -> list[str]:
    community_rows = [
        [
            str(item["display_name"]),
            fmt_optional_float(item["community_prior_score"]),
            fmt_optional_float(item["community_confidence"]),
            fmt_breakdown_components(item["community_breakdown"]),
        ]
        for item in ranked
        if item["community_breakdown"]
    ]
    quality_rows = [
        [
            str(item["display_name"]),
            fmt_score(item["quality_penalty"]),
            fmt_score(item["quality_penalty_uncapped"]),
            short_risk_flags(list(item["quality_flags"])),
            summarize_quality_evidence(list(item["quality_evidence"]), language=language),
        ]
        for item in ranked
        if float(item["quality_penalty"]) > 0
    ]
    risk_rows = [
        [
            str(item["display_name"]),
            str(item["risk_level"]),
            short_risk_flags(list(item["risk_flags"])),
            install_gate_label(str(item["install_gate"]["verdict"]), language),  # type: ignore[index]
            risk_review_summary_for_report(
                str(item["risk_level"]),
                list(item["risk_evidence"]),  # type: ignore[arg-type]
                language,
            ),
        ]
        for item in ranked
        if str(item["risk_level"]) != "none"
    ]
    return [
        *_table_report_section(language, "community_signal_breakdown", "community", community_rows),
        *_table_report_section(language, "quality_burden", "quality", quality_rows),
        *_table_report_section(language, "risk_review", "risk", risk_rows),
    ]


def _action_report_sections(
    recommended_actions: list[dict[str, object]],
    delete_candidates: list[dict[str, object]],
    language: str,
) -> list[str]:
    action_rows = [
        [
            str(item["display_name"]),
            fmt_score(item["local_score"]),
            fmt_score(item["quality_penalty"]),
            fmt_score(item["final_score"]),
            fmt_optional_float(item["confidence_score"]),
            str(item["risk_level"]),
            str(item["action"]),
            action_advice_for_item(item, language),
        ]
        for item in recommended_actions
    ]
    delete_rows = [
        [
            str(item["display_name"]),
            fmt_score(item["local_score"]),
            fmt_score(item["quality_penalty"]),
            fmt_score(item["final_score"]),
            str(item["kind"]),
            str(item["action"]),
            action_reason_for_report(str(item["delete_trigger"]), language),
            action_advice_for_item(item, language),
        ]
        for item in delete_candidates
    ]
    return [
        *_table_report_section(language, "recommended_actions_heading", "actions", action_rows),
        *_table_report_section(language, "delete_candidates_heading", "delete", delete_rows),
    ]


def _evidence_gap_report_sections(
    missing: list[dict[str, object]],
    not_audited: list[dict[str, str]],
    language: str,
) -> list[str]:
    missing_rows = []
    for item in missing:
        gaps = []
        if item["missing_usage"]:
            gaps.append(missing_evidence_label("usage", language))
        if item["missing_ablation"]:
            gaps.append(missing_evidence_label("ablation", language))
        if item["missing_community"]:
            gaps.append(missing_evidence_label("community", language))
        gap_separator = "、" if normalize_report_language(language) == "zh-CN" else ", "
        missing_rows.append([str(item["display_name"]), str(item["kind"]), gap_separator.join(gaps)])
    not_audited_rows = [
        [f"`{item['path']}`", not_audited_reason_label(item["reason"], language)]
        for item in not_audited
    ]
    return [
        *_table_report_section(language, "missing_evidence", "missing", missing_rows),
        *_table_report_section(language, "not_audited", "not_audited", not_audited_rows),
    ]


def _build_markdown_report(
    ranked: list[dict[str, object]],
    path_counts: dict[str, int],
    report_mode: str,
    report_language: str,
    recommended_actions: list[dict[str, object]],
    delete_candidates: list[dict[str, object]],
    missing: list[dict[str, object]],
    not_audited: list[dict[str, str]],
    description_characters: int,
    description_context_units: int,
    ablation_plan: dict[str, object] | None,
) -> str:
    report_parts = [
        description_load_notice(
            len(ranked),
            description_characters,
            description_context_units,
            report_language,
        ),
        "",
        f"# {report_text(report_language, 'title')}",
        "",
        f"- {report_pair(report_language, report_text(report_language, 'skills_audited'), len(ranked))}",
        f"- {report_pair(report_language, report_text(report_language, 'usage_files'), path_counts['usage'])}",
        f"- {report_pair(report_language, report_text(report_language, 'history_files'), path_counts['history'])}",
        f"- {report_pair(report_language, report_text(report_language, 'ablation_files'), path_counts['ablation'])}",
        f"- {report_pair(report_language, report_text(report_language, 'community_files'), path_counts['community'])}",
        f"- {report_pair(report_language, report_text(report_language, 'report_mode'), report_mode)}",
        f"- {report_pair(report_language, report_text(report_language, 'recommended_actions'), len(recommended_actions))}",
        f"- {report_pair(report_language, report_text(report_language, 'delete_candidates'), len(delete_candidates))}",
        f"- {report_pair(report_language, report_text(report_language, 'not_audited_count'), len(not_audited))}",
        "",
        *decision_summary(ranked, language=report_language),
        "",
        f"## {report_text(report_language, 'score_table')}",
        "",
        report_text(report_language, "score_axes_note"),
        "",
        markdown_table(report_headers(report_language, "score"), _score_report_rows(ranked)),
        *_ablation_report_section(ablation_plan, report_language),
        *_diagnostic_report_sections(ranked, report_language),
        *_action_report_sections(recommended_actions, delete_candidates, report_language),
        *_evidence_gap_report_sections(missing, not_audited, report_language),
    ]
    return "\n".join(report_parts) + "\n"


def _write_audit_outputs(
    args: argparse.Namespace,
    report: str,
    ranked: list[dict[str, object]],
    path_counts: dict[str, int],
    report_mode: str,
    report_language: str,
    recommended_actions: list[dict[str, object]],
    delete_candidates: list[dict[str, object]],
    not_audited: list[dict[str, str]],
    description_characters: int,
    description_context_units: int,
    ablation_plan: dict[str, object] | None,
) -> None:
    markdown_path = None
    if args.markdown_out:
        markdown_path = Path(args.markdown_out).expanduser().resolve()
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(report, encoding="utf-8")

    print(
        concise_report(
            ranked,
            language=report_language,
            markdown_path=markdown_path,
            not_audited_count=len(not_audited),
            entry_prompt_characters=description_characters,
            entry_prompt_tokens=description_context_units,
        )
    )

    if args.json_out:
        payload = {
            "skills_audited": len(ranked),
            "usage_files": path_counts["usage"],
            "history_files": path_counts["history"],
            "ablation_files": path_counts["ablation"],
            "community_files": path_counts["community"],
            "report_mode": report_mode,
            "recommended_actions": len(recommended_actions),
            "delete_candidates": len(delete_candidates),
            "not_audited": not_audited,
            "results": ranked,
        }
        if ablation_plan is not None:
            payload["ablation_plan"] = ablation_plan
        json_path = Path(args.json_out).expanduser().resolve()
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.ablation_plan_out:
        assert ablation_plan is not None
        plan_path = Path(args.ablation_plan_out).expanduser().resolve()
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        plan_path.write_text(json.dumps(ablation_plan, ensure_ascii=False, indent=2), encoding="utf-8")


def run_audit(args: argparse.Namespace) -> int:
    roots = [Path(item).expanduser().resolve() for item in (args.skills_root or [])]
    if not roots:
        roots = [root.resolve() for root in default_roots()]
    dedupe_install_identity = not bool(getattr(args, "show_duplicate_installs", False))
    skill_files = discover_skill_files(
        roots,
        args.include_system,
        dedupe_install_identity=dedupe_install_identity,
    )
    not_audited = collect_not_audited_entries(
        roots,
        skill_files,
        include_system=args.include_system,
        dedupe_install_identity=dedupe_install_identity,
    )
    if not skill_files:
        print("No skills found.", file=sys.stderr)
        print("Searched roots:", file=sys.stderr)
        for root in roots:
            print(f"- {root}", file=sys.stderr)
        print("Expected skill files named SKILL.md under each skill directory.", file=sys.stderr)
        print("Pass --skills-root PATH for custom install locations.", file=sys.stderr)
        return 1

    skills = [scan_skill(path) for path in skill_files]
    names = [skill["name"] for skill in skills]
    alias_counts = Counter(key for skill in skills for key in skill_lookup_keys(skill))
    usage_paths = existing_paths("usage", args.usage_file, args.strict_inputs)
    history_paths = existing_paths("history", args.history_file, args.strict_inputs)
    ablation_paths = existing_paths("ablation", args.ablation_file, args.strict_inputs)
    community_paths = existing_paths("community", args.community_file, args.strict_inputs)
    if usage_paths is None or history_paths is None or ablation_paths is None or community_paths is None:
        return 2

    usage = load_usage(usage_paths) if usage_paths else {}
    history_usage = infer_usage_from_history(history_paths, names) if history_paths else {}
    ablation = load_ablation(ablation_paths) if ablation_paths else {}
    community = load_community(community_paths) if community_paths else {}

    results = [
        _build_audit_result(
            skill,
            skills,
            alias_counts,
            usage,
            history_usage,
            ablation,
            community,
            bool(history_paths),
            bool(community_paths),
        )
        for skill in skills
    ]

    ranked = sorted(results, key=lambda item: (-float(item["final_score"]), str(item["display_name"])))
    recommended_actions = sorted(
        [item for item in ranked if str(item["action"]) not in {"keep", "keep-narrow", "keep-system"}],
        key=lambda item: (str(item["action"]), float(item["final_score"]), str(item["display_name"])),
    )
    delete_candidates = sorted(
        [item for item in ranked if item["delete_candidate"]],
        key=lambda item: (float(item["final_score"]), str(item["display_name"])),
    )
    missing = [item for item in ranked if item["missing_usage"] or item["missing_ablation"] or item["missing_community"]]
    report_mode = determine_report_mode(usage_paths, history_paths, ablation_paths, ranked)
    report_language = normalize_report_language(getattr(args, "report_language", "auto"))
    description_characters = sum(
        int(item["resource_metrics"].get("description_characters", 0))  # type: ignore[union-attr]
        for item in ranked
    )
    description_context_units = sum(
        int(item["resource_metrics"].get("description_context_units", 0))  # type: ignore[union-attr]
        for item in ranked
    )
    ablation_plan = None
    if args.ablation_plan_out:
        ablation_plan = build_ablation_plan(
            ranked,
            max_candidates=int(args.ablation_plan_max_candidates),
            baseline_cases_per_skill=int(args.ablation_baseline_cases),
            initial_cases_per_candidate=int(args.ablation_initial_cases),
            expand_to_cases=int(args.ablation_expand_cases),
            max_cases_per_candidate=int(args.ablation_max_cases),
        )

    path_counts = {
        "usage": len(usage_paths),
        "history": len(history_paths),
        "ablation": len(ablation_paths),
        "community": len(community_paths),
    }
    report = _build_markdown_report(
        ranked,
        path_counts,
        report_mode,
        report_language,
        recommended_actions,
        delete_candidates,
        missing,
        not_audited,
        description_characters,
        description_context_units,
        ablation_plan,
    )
    _write_audit_outputs(
        args,
        report,
        ranked,
        path_counts,
        report_mode,
        report_language,
        recommended_actions,
        delete_candidates,
        not_audited,
        description_characters,
        description_context_units,
        ablation_plan,
    )

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit installed skill usefulness.")
    parser.add_argument("--version", action="version", version=f"skill-usefulness-audit {cli_version()}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="Audit skills and render a report.")
    audit_parser.add_argument("--skills-root", action="append", help="Root directory containing skill folders.")
    audit_parser.add_argument("--usage-file", action="append", help="JSON/JSONL/CSV/TSV file with usage evidence.")
    audit_parser.add_argument("--history-file", action="append", help="Transcript export used for mention fallback.")
    audit_parser.add_argument("--ablation-file", action="append", help="JSON or JSONL file with ablation cases.")
    audit_parser.add_argument("--community-file", action="append", help="Offline JSON/JSONL/CSV/TSV file with registry metrics.")
    audit_parser.add_argument("--markdown-out", help="Write the full Markdown evidence report to this file.")
    if chinese_only_report_profile_enabled():
        audit_parser.add_argument(
            "--report-language",
            default="zh-CN",
            choices=("zh-CN",),
            help="Report language is fixed to zh-CN by this package profile.",
        )
    else:
        audit_parser.add_argument(
            "--report-language",
            default="auto",
            help=(
                "Summary and Markdown evidence language: auto, en, or zh-CN. Auto reads "
                "SKILL_AUDIT_REPORT_LANGUAGE or the "
                "process locale; unsupported or unclear values fall back to English."
            ),
        )
    audit_parser.add_argument("--json-out", help="Write machine-readable JSON output to this file.")
    audit_parser.add_argument("--ablation-plan-out", help="Write a cost-efficient ablation plan JSON file.")
    audit_parser.add_argument(
        "--strict-inputs",
        action="store_true",
        help="Fail instead of warning when any usage/history/ablation/community input file is missing.",
    )
    audit_parser.add_argument(
        "--ablation-plan-max-candidates",
        type=int,
        default=ABLATION_DEFAULT_MAX_CANDIDATES,
        help="Maximum general skills to include in the cost-efficient ablation plan.",
    )
    audit_parser.add_argument(
        "--ablation-baseline-cases",
        type=int,
        default=ABLATION_BASELINE_CASES,
        help="Baseline cases per general skill used for model-cost reduction estimates.",
    )
    audit_parser.add_argument(
        "--ablation-initial-cases",
        type=int,
        default=ABLATION_INITIAL_CASES,
        help="Initial replay cases per candidate skill.",
    )
    audit_parser.add_argument(
        "--ablation-expand-cases",
        type=int,
        default=ABLATION_EXPAND_CASES,
        help="Replay cases after expanding mixed candidate results.",
    )
    audit_parser.add_argument(
        "--ablation-max-cases",
        type=int,
        default=ABLATION_MAX_CASES,
        help="Maximum replay cases per candidate skill.",
    )
    audit_parser.add_argument("--include-system", action="store_true", help="Include system skills during discovery.")
    audit_parser.add_argument(
        "--show-duplicate-installs",
        action="store_true",
        help="Report duplicate install identities separately instead of deduplicating them.",
    )
    audit_parser.set_defaults(func=run_audit)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
