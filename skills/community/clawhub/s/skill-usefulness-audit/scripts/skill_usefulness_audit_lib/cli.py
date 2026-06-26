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


def run_audit(args: argparse.Namespace) -> int:
    roots = [Path(item).expanduser().resolve() for item in (args.skills_root or [])]
    if not roots:
        roots = [root.resolve() for root in default_roots()]
    skill_files = discover_skill_files(roots, args.include_system)
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

    results: list[dict[str, object]] = []
    for skill in skills:
        kind = classify_skill(skill)
        best_peer = None
        best_overlap = 0.0
        for other in skills:
            if skill["path"] == other["path"]:
                continue
            overlap = jaccard(skill["terms"], other["terms"])
            if overlap > best_overlap:
                best_overlap = overlap
                best_peer = skill_display_name(other, alias_counts)

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
            usage_source = "history" if history_paths else "missing"

        evidence_weight = usage_evidence_weight(usage_source)
        calls = int(usage_record.get("calls", 0) or 0)
        history_mentions = int(usage_record.get("history_mentions", 0) or 0)
        suspected_invocations = int(usage_record.get("suspected_invocations", 0) or 0)
        ablation_summary, ablation_note = resolve_record(ablation, skill, alias_counts)
        if ablation_note:
            evidence_notes.append(f"ablation={ablation_note}")
        community_entry, community_note = resolve_record(community, skill, alias_counts)
        if community_note:
            evidence_notes.append(f"community={community_note}")
        community_prior, community_conf, community_breakdown = community_prior_score(community_entry)
        evidence_note = " | ".join(dict.fromkeys(evidence_notes)) if evidence_notes else None
        risk_review = risk_review_summary(str(skill["risk_level"]), list(skill["risk_evidence"]))  # type: ignore[arg-type]
        install_gate = install_gate_summary(str(skill["risk_level"]), list(skill["risk_evidence"]))  # type: ignore[arg-type]

        u_score = usage_score(usage_record, evidence_weight)
        uniq_score = uniqueness_score(best_overlap)
        i_score = impact_score(kind, calls, best_overlap, skill, ablation_summary)
        total = round(u_score + uniq_score + i_score, 2)
        catalog_evidence = catalog_quality_evidence(best_peer, best_overlap)
        quality = quality_penalty(skill, usage_record, ablation_summary, catalog_evidence)
        quality_penalty_value = float(quality["penalty"])
        quality_penalty_uncapped = float(quality["penalty_uncapped"])
        quality_flags = list(quality["flags"])  # type: ignore[arg-type]
        pre_health_cap_final = round(clamp(total - quality_penalty_value, 0.0, 10.0), 2)
        health_cap = health_cap_from_quality(list(quality["evidence"]))  # type: ignore[arg-type]
        final = min(pre_health_cap_final, health_cap) if health_cap is not None else pre_health_cap_final
        final = round(final, 2)
        confidence = confidence_score(
            usage_source,
            usage_record,
            kind,
            ablation_summary,
            community_entry,
            len(skills),
        )
        action, action_reason, delete_candidate = recommend_action(
            str(skill["source"]),
            kind,
            final,
            confidence,
            str(skill["risk_level"]),
            quality_penalty_value,
            calls,
            best_overlap,
            community_prior,
        )
        advice = action_advice(action, action_reason)
        score_breakdown = {
            "usage": {
                "score": u_score,
                "source": usage_source,
                "evidence_weight": evidence_weight,
                "calls": calls,
                "history_mentions": history_mentions,
                "suspected_invocations": suspected_invocations,
                "recent_30d_calls": coerce_int(usage_record.get("recent_30d_calls")),
                "recent_90d_calls": coerce_int(usage_record.get("recent_90d_calls")),
                "last_used_at": usage_record.get("last_used_at"),
                "executions": coerce_int(usage_record.get("executions")),
                "script_failures": coerce_int(usage_record.get("script_failures")),
                "repair_turns": coerce_int(usage_record.get("repair_turns")),
                "reference_loads": coerce_int(usage_record.get("reference_loads")),
                "false_triggers": coerce_int(usage_record.get("false_triggers")),
            },
            "uniqueness": {
                "score": uniq_score,
                "overlap_peer": best_peer,
                "overlap_value": round(best_overlap, 2),
            },
            "impact": {
                "score": i_score,
                "kind": kind,
                "protected_capability": kind in {"api", "tool"},
                "ablation": ablation_summary,
            },
            "community": {
                "score": community_prior,
                "confidence": community_conf,
                "breakdown": community_breakdown,
            },
            "risk": {
                "level": skill["risk_level"],
                "score": skill["risk_score"],
                "flags": skill["risk_flags"],
                "static_level": skill["static_risk_level"],
                "static_flags": skill["static_risk_flags"],
                "install_gate": install_gate,
            },
            "quality": {
                "penalty": quality_penalty_value,
                "penalty_uncapped": quality_penalty_uncapped,
                "flags": quality_flags,
                "pre_health_cap_final": pre_health_cap_final,
                "health_cap": health_cap,
                "resource_metrics": skill["resource_metrics"],
                "required_env": skill.get("required_env"),
                "missing_required_env": skill.get("missing_required_env"),
            },
            "confidence": {
                "score": confidence,
            },
        }

        results.append(
            {
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
                "kind": kind,
                "path": skill["path"],
                "calls": calls,
                "history_mentions": history_mentions,
                "suspected_invocations": suspected_invocations,
                "recent_30d_calls": coerce_int(usage_record.get("recent_30d_calls")),
                "recent_90d_calls": coerce_int(usage_record.get("recent_90d_calls")),
                "active_days": coerce_int(usage_record.get("active_days")),
                "first_seen_at": usage_record.get("first_seen_at"),
                "last_used_at": usage_record.get("last_used_at"),
                "executions": coerce_int(usage_record.get("executions")),
                "script_failures": coerce_int(usage_record.get("script_failures")),
                "repair_turns": coerce_int(usage_record.get("repair_turns")),
                "reference_loads": coerce_int(usage_record.get("reference_loads")),
                "false_triggers": coerce_int(usage_record.get("false_triggers")),
                "usage_source": usage_source,
                "evidence_weight": evidence_weight,
                "usage_score": u_score,
                "uniqueness_score": uniq_score,
                "impact_score": i_score,
                "local_score": total,
                "total_score": total,
                "quality_penalty": quality_penalty_value,
                "quality_penalty_uncapped": quality_penalty_uncapped,
                "quality_flags": quality_flags,
                "quality_evidence": quality["evidence"],
                "resource_metrics": skill["resource_metrics"],
                "final_score": final,
                "confidence_score": confidence,
                "verdict": verdict(final, confidence),
                "action": action,
                "action_reason": action_reason,
                "action_advice": advice,
                "delete_candidate": delete_candidate,
                "delete_trigger": action_reason if delete_candidate else None,
                "overlap_peer": best_peer,
                "overlap_value": round(best_overlap, 2),
                "community": community_entry,
                "community_prior_score": community_prior,
                "community_confidence": community_conf,
                "community_breakdown": community_breakdown,
                "risk_level": skill["risk_level"],
                "risk_score": skill["risk_score"],
                "risk_flags": skill["risk_flags"],
                "risk_evidence": skill["risk_evidence"],
                "risk_review": risk_review,
                "install_gate": install_gate,
                "static_risk_level": skill["static_risk_level"],
                "static_risk_score": skill["static_risk_score"],
                "static_risk_flags": skill["static_risk_flags"],
                "static_risk_evidence": skill["static_risk_evidence"],
                "score_breakdown": score_breakdown,
                "evidence_note": evidence_note,
                "basis": build_basis(
                    usage_record,
                    usage_source,
                    evidence_weight,
                    best_peer,
                    best_overlap,
                    kind,
                    ablation_summary,
                    community_prior,
                    list(skill["risk_flags"]),
                    quality_penalty_value,
                    quality_flags,
                    evidence_note,
                ),
                "missing_usage": usage_source == "missing",
                "missing_ablation": kind == "general" and not ablation_summary,
                "missing_community": bool(community_paths) and community_entry is None,
            }
        )

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

    score_rows = []
    for index, item in enumerate(ranked, start=1):
        score_rows.append(
            [
                str(index),
                str(item["display_name"]),
                str(item["source"]),
                str(item["kind"]),
                str(item["calls"]),
                fmt_optional_int(item["recent_30d_calls"]),
                f"{item['usage_score']:.1f}",
                f"{item['uniqueness_score']:.1f}",
                f"{item['impact_score']:.1f}",
                fmt_optional_float(item["community_prior_score"]),
                fmt_optional_float(item["confidence_score"]),
                str(item["risk_level"]),
                f"{item['local_score']:.1f}",
                f"{item['quality_penalty']:.1f}",
                f"{item['final_score']:.1f}",
                str(item["verdict"]),
                str(item["action"]),
                str(item["basis"]),
            ]
        )

    report_parts = [
        f"# {report_text(report_language, 'title')}",
        "",
        f"- {report_text(report_language, 'skills_audited')}: {len(ranked)}",
        f"- {report_text(report_language, 'usage_files')}: {len(usage_paths)}",
        f"- {report_text(report_language, 'history_files')}: {len(history_paths)}",
        f"- {report_text(report_language, 'ablation_files')}: {len(ablation_paths)}",
        f"- {report_text(report_language, 'community_files')}: {len(community_paths)}",
        f"- {report_text(report_language, 'report_mode')}: {report_mode}",
        f"- {report_text(report_language, 'recommended_actions')}: {len(recommended_actions)}",
        f"- {report_text(report_language, 'delete_candidates')}: {len(delete_candidates)}",
        "",
        *decision_summary(ranked, language=report_language),
        "",
        f"## {report_text(report_language, 'score_table')}",
        "",
        markdown_table(
            report_headers(report_language, "score"),
            score_rows,
        ),
    ]

    if ablation_plan and ablation_plan["candidate_skills"]:
        expected_reduction = ablation_plan["model_cost_estimates"]["planned_expected"]["reduction_vs_baseline_percent"]  # type: ignore[index]
        realistic_reduction = expected_reduction["realistic"]  # type: ignore[index]
        baseline_policy = ablation_plan["case_policy"]["baseline_cases_per_general_skill"]  # type: ignore[index]
        report_parts.extend(
            [
                "",
                f"## {report_text(report_language, 'cost_ablation_plan')}",
                "",
                f"- {report_text(report_language, 'strategy')}: {ablation_plan['strategy']}",
                f"- {report_text(report_language, 'eligible_general_skills')}: {ablation_plan['eligible_general_skills']}",
                f"- {report_text(report_language, 'candidate_skills')}: {ablation_plan['candidate_skills']}",
                f"- {report_text(report_language, 'deferred_general_skills')}: {ablation_plan['deferred_general_skills']}",
                f"- {report_text(report_language, 'expected_model_cost_reduction').format(baseline_policy=baseline_policy)}: {realistic_reduction}%",
                f"- {report_text(report_language, 'expected_accuracy_impact')}: {ablation_plan['accuracy_tradeoff']['expected_accuracy_impact']}",
                "",
                markdown_table(
                    report_headers(report_language, "ablation"),
                    [
                        [
                            str(item["skill"]),
                            str(item["priority_score"]),
                            str(item["initial_cases"]),
                            str(item["expand_to"]),
                            str(item["max_cases"]),
                            ", ".join(item["priority_reasons"]),
                        ]
                        for item in ablation_plan["candidates"]  # type: ignore[index]
                    ],
                ),
            ]
        )

    community_rows = []
    for item in ranked:
        community_breakdown = item["community_breakdown"]
        if community_breakdown:
            community_rows.append(
                [
                    str(item["display_name"]),
                    fmt_optional_float(item["community_prior_score"]),
                    fmt_optional_float(item["community_confidence"]),
                    fmt_breakdown_components(community_breakdown),
                ]
            )

    if community_rows:
        report_parts.extend(
            [
                "",
                f"## {report_text(report_language, 'community_signal_breakdown')}",
                "",
                markdown_table(report_headers(report_language, "community"), community_rows),
            ]
        )

    quality_rows = []
    for item in ranked:
        if float(item["quality_penalty"]) <= 0:
            continue
        quality_rows.append(
            [
                str(item["display_name"]),
                f"{item['quality_penalty']:.1f}",
                f"{item['quality_penalty_uncapped']:.1f}",
                short_risk_flags(list(item["quality_flags"])),
                summarize_quality_evidence(list(item["quality_evidence"])),
            ]
        )

    if quality_rows:
        report_parts.extend(
            [
                "",
                f"## {report_text(report_language, 'quality_burden')}",
                "",
                markdown_table(report_headers(report_language, "quality"), quality_rows),
            ]
        )

    risk_rows = []
    for item in ranked:
        if str(item["risk_level"]) == "none":
            continue
        risk_rows.append(
            [
                str(item["display_name"]),
                str(item["risk_level"]),
                short_risk_flags(list(item["risk_flags"])),
                str(item["install_gate"]["verdict"]),  # type: ignore[index]
                risk_review_summary_for_report(
                    str(item["risk_level"]),
                    list(item["risk_evidence"]),  # type: ignore[arg-type]
                    report_language,
                ),
            ]
        )

    if risk_rows:
        report_parts.extend(
            [
                "",
                f"## {report_text(report_language, 'risk_review')}",
                "",
                markdown_table(report_headers(report_language, "risk"), risk_rows),
            ]
        )

    if recommended_actions:
        action_rows = [
            [
                str(item["display_name"]),
                f"{item['local_score']:.1f}",
                f"{item['quality_penalty']:.1f}",
                f"{item['final_score']:.1f}",
                fmt_optional_float(item["confidence_score"]),
                str(item["risk_level"]),
                str(item["action"]),
                action_advice_for_report(str(item["action"]), str(item["action_reason"]), report_language),
            ]
            for item in recommended_actions
        ]
        report_parts.extend(
            [
                "",
                f"## {report_text(report_language, 'recommended_actions_heading')}",
                "",
                markdown_table(report_headers(report_language, "actions"), action_rows),
            ]
        )

    if delete_candidates:
        delete_rows = [
            [
                str(item["display_name"]),
                f"{item['local_score']:.1f}",
                f"{item['quality_penalty']:.1f}",
                f"{item['final_score']:.1f}",
                str(item["kind"]),
                str(item["action"]),
                str(item["delete_trigger"]),
                action_advice_for_report(str(item["action"]), str(item["action_reason"]), report_language),
            ]
            for item in delete_candidates
        ]
        report_parts.extend(
            [
                "",
                f"## {report_text(report_language, 'delete_candidates_heading')}",
                "",
                markdown_table(report_headers(report_language, "delete"), delete_rows),
            ]
        )

    if missing:
        missing_rows = []
        for item in missing:
            gaps = []
            if item["missing_usage"]:
                gaps.append(missing_evidence_label("usage", report_language))
            if item["missing_ablation"]:
                gaps.append(missing_evidence_label("ablation", report_language))
            if item["missing_community"]:
                gaps.append(missing_evidence_label("community", report_language))
            missing_rows.append([str(item["display_name"]), str(item["kind"]), ", ".join(gaps)])
        report_parts.extend(
            [
                "",
                f"## {report_text(report_language, 'missing_evidence')}",
                "",
                markdown_table(report_headers(report_language, "missing"), missing_rows),
            ]
        )

    report = "\n".join(report_parts) + "\n"

    if args.markdown_out:
        markdown_path = Path(args.markdown_out).expanduser().resolve()
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(report, encoding="utf-8")
    else:
        print(report)

    if args.json_out:
        payload = {
            "skills_audited": len(ranked),
            "usage_files": len(usage_paths),
            "history_files": len(history_paths),
            "ablation_files": len(ablation_paths),
            "community_files": len(community_paths),
            "report_mode": report_mode,
            "recommended_actions": len(recommended_actions),
            "delete_candidates": len(delete_candidates),
            "results": ranked,
        }
        if ablation_plan is not None:
            payload["ablation_plan"] = ablation_plan
        json_path = Path(args.json_out).expanduser().resolve()
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    if args.ablation_plan_out:
        assert ablation_plan is not None
        plan_path = Path(args.ablation_plan_out).expanduser().resolve()
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        plan_path.write_text(
            json.dumps(ablation_plan, ensure_ascii=False, indent=2),
            encoding="utf-8",
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
    audit_parser.add_argument("--markdown-out", help="Write the Markdown report to this file.")
    audit_parser.add_argument(
        "--report-language",
        default="auto",
        help="Markdown report language: auto, en, or zh-CN. Unsupported or unclear values fall back to English.",
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
    audit_parser.set_defaults(func=run_audit)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
