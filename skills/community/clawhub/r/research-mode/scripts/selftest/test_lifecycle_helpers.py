"""Unit tests for research_mode_lifecycle_helpers: confidence, quality scores, badges, notification, text composition."""
from __future__ import annotations

from pathlib import Path

from .helpers import assert_eq, assert_in, assert_true

from research_mode_adequacy import (
    build_adequacy_contract,
    build_adequacy_guidance,
)
from research_mode_lifecycle_helpers import (
    build_evidence_gaps,
    build_revision_diff,
    compose_failure_update_text,
    compose_finish_update_text,
    compute_confidence_score,
    compute_low_yield,
    compute_source_quality_score,
    detect_comparative_structure,
    enrich_findings_with_provenance,
    inspect_deliverable_requirements,
    render_confidence_badge,
    should_notify,
)


# --- compute_confidence_score ---

def test_adequacy_contract_carries_goal_constraints_and_open_questions(root: Path) -> None:
    state = {
        "id": "adequacy-contract",
        "goal": "Compare options for a user-facing recommendation.",
        "phase": "verify",
        "working_memory": {
            "constraints": ["Use primary sources where possible."],
            "deliverable": "short comparative memo",
            "open_questions": ["Reliability evidence is still weak."],
            "user_instructions": ["Answer in Russian."],
        },
    }

    contract = build_adequacy_contract(state)
    guidance = build_adequacy_guidance(state)

    assert_in("result.adequacy", contract["result_field"], "contract should name the result field")
    assert_in("goal_alignment", contract["required_checks"], "contract should require goal alignment")
    assert_in("source_diversity", contract["required_checks"], "contract should require source diversity")
    assert_in("Reliability evidence is still weak.", contract["current_open_questions"], "contract should carry open questions")
    assert_in("Use primary sources where possible.", contract["constraints"], "contract should carry constraints")
    assert_in("short comparative memo", " ".join(guidance), "guidance should mention requested deliverable")
    assert_in("Russian", " ".join(guidance), "guidance should include explicit user instructions")


def test_detect_comparative_structure_accepts_ranked_table(root: Path) -> None:
    report = """# Recommendation

| 甲 | 乙 | 丙 | 丁 |
| --- | --- | --- | --- |
| 1 | A | choose | supply |
| 2 | B | backup | price |
"""

    result = detect_comparative_structure(report)

    assert_eq(result["passed"], True, "table shape should be comparative")
    assert_in("table_shape", result["signals"], "table shape signal should be explicit")


def test_detect_comparative_structure_accepts_risk_matrix(root: Path) -> None:
    report = """# Decision Matrix

| 一 | 二 |
| --- | --- |
| A | supplier reserve |
| B | price cap |
"""

    result = detect_comparative_structure(report)

    assert_eq(result["passed"], True, "matrix shape should be comparative")
    assert_in("table_shape", result["signals"], "table shape signal should be explicit")


def test_comparative_deliverable_rejects_plain_bullets_without_criteria(root: Path) -> None:
    report = """# Options

- A is cheap.
- B is reliable.
"""

    validation = inspect_deliverable_requirements(
        "comparative memo",
        report,
        payload={},
        total_sources=2,
        total_findings=2,
        output_contract={
            "quality_checks": [
                {"kind": "comparative_matrix", "min_rows": 2, "min_columns": 2}
            ]
        },
    )
    comparative_check = next(
        check for check in validation["checks"] if check["kind"] == "comparative_matrix"
    )

    assert_eq(comparative_check["passed"], False, "plain bullets should not satisfy comparative shape")
    assert_in(
        "deliverable_comparative_shape_weak",
        validation["reasons"],
        "plain bullets should produce actionable comparative rejection",
    )

def test_confidence_no_sources(root: Path) -> None:
    finding = {"kind": "fact", "text": "Claim without refs"}
    result = compute_confidence_score(finding, [])
    assert_eq(result["tier"], "reserve", "no sources -> reserve tier")
    assert_eq(result["confidence"], 0.0, "no sources -> 0 confidence")
    assert_eq(result["reason"], "no_verifiable_source", "reason for zero confidence")


def test_confidence_single_source(root: Path) -> None:
    sources = [{"url": "https://example.com", "title": "Example"}]
    finding = {"kind": "fact", "text": "Fact", "source_urls": ["https://example.com"]}
    result = compute_confidence_score(finding, sources)
    assert_in(result["tier"], ["medium", "low"], "single source -> medium or low")
    assert_eq(result["source_count"], 1, "one source counted")
    assert_eq(result["reason"], "single_source", "reason should be single_source")


def test_confidence_multi_source(root: Path) -> None:
    sources = [
        {"url": "https://a.gov"},
        {"url": "https://b.edu"},
        {"url": "https://c.org"},
    ]
    finding = {
        "kind": "fact",
        "text": "Well-sourced fact",
        "source_urls": ["https://a.gov", "https://b.edu", "https://c.org"],
    }
    result = compute_confidence_score(finding, sources)
    assert_in(result["tier"], ["high", "medium"], "3 sources -> high or medium")
    assert_eq(result["source_count"], 3, "three sources counted")
    assert_eq(result["reason"], "multi_source_corroborated", "multi-source reason")


def test_confidence_softened_by_kind(root: Path) -> None:
    """Hypotheses and estimates should have confidence softened."""
    sources = [{"url": "https://a.com"}, {"url": "https://b.com"}, {"url": "https://c.com"}]
    finding = {
        "kind": "hypothesis",
        "text": "Hypothetical claim",
        "source_urls": ["https://a.com", "https://b.com", "https://c.com"],
    }
    result = compute_confidence_score(finding, sources)
    assert_in("softened_by_kind", result["reason"], "hypothesis should be softened")


def test_confidence_downgraded_to_reserve(root: Path) -> None:
    sources = [{"url": "https://a.com"}]
    finding = {
        "kind": "fact",
        "text": "Downgraded",
        "source_urls": ["https://a.com"],
        "downgraded_to_reserve": True,
    }
    result = compute_confidence_score(finding, sources)
    assert_eq(result["tier"], "reserve", "downgraded should be reserve")
    assert_eq(result["confidence"], 0.1, "downgraded confidence")


# --- compute_source_quality_score ---

def test_source_quality_ignores_domain_and_tags(root: Path) -> None:
    result = compute_source_quality_score({
        "url": "https://agency.gov/report",
        "tags": ["official_source", "primary_source", "user_generated", "stale"],
    })
    assert_eq(result["factors"], [], "source quality should not infer authority from tags or domains")
    assert_eq(result["quality_score"], 0.5, "domain and tag labels should not alter quality score")


def test_source_quality_uses_structured_fetch_timestamp(root: Path) -> None:
    fresh = compute_source_quality_score({
        "url": "https://example.com",
        "fetched_at": "2999-01-01T00:00:00Z",
    })
    old = compute_source_quality_score({
        "url": "https://example.com",
        "fetched_at": "2020-01-01T00:00:00Z",
    })
    assert_in("fresh_30d", fresh["factors"], "fresh timestamp should raise quality")
    assert_in("stale_over_1yr", old["factors"], "old timestamp should lower quality")
    assert_true(fresh["quality_score"] > old["quality_score"], "timestamp should be the only scoring signal here")


def test_source_quality_tier_mapping(root: Path) -> None:
    plain = compute_source_quality_score({"url": "https://example.com"})
    assert_eq(plain["quality_score"], 0.5, "plain URL -> base score 0.5")
    assert_eq(plain["tier"], "weak", "score 0.5 < 0.55 threshold -> weak tier")

    fresh = compute_source_quality_score({
        "url": "https://example.com",
        "fetched_at": "2999-01-01T00:00:00Z",
    })
    assert_eq(fresh["tier"], "standard", "fresh timestamp -> standard tier")


# --- enrich_findings_with_provenance ---

def test_enrich_findings_adds_provenance(root: Path) -> None:
    sources = [{"url": "https://a.com", "title": "Source A"}]
    findings = [
        {"kind": "fact", "text": "Finding 1", "source_urls": ["https://a.com"]},
        {"kind": "note", "text": "Finding 2"},
    ]
    enriched = enrich_findings_with_provenance(findings, sources)
    assert_eq(len(enriched), 2, "all findings should be returned")
    assert_in("provenance", enriched[0], "first finding should have provenance")
    assert_in("tier", enriched[0]["provenance"], "provenance should have tier")
    assert_eq(enriched[1]["provenance"]["tier"], "reserve", "no-source finding -> reserve")


def test_enrich_findings_empty(root: Path) -> None:
    result = enrich_findings_with_provenance([], [])
    assert_eq(result, [], "empty input -> empty output")


# --- render_confidence_badge ---

def test_render_confidence_badge_known_tiers(root: Path) -> None:
    assert_eq(render_confidence_badge("high"), "[●●●]", "high badge")
    assert_eq(render_confidence_badge("medium"), "[●●○]", "medium badge")
    assert_eq(render_confidence_badge("low"), "[●○○]", "low badge")
    assert_eq(render_confidence_badge("reserve"), "[○○○]", "reserve badge")


def test_render_confidence_badge_unknown(root: Path) -> None:
    assert_eq(render_confidence_badge("xyz"), "[???]", "unknown tier -> fallback badge")


# --- should_notify ---

def test_should_notify_silent(root: Path) -> None:
    state = {"progress": {"meaningful_iterations": 5}, "delivery": {"milestone_every_iterations": 2}}
    payload = {"notify_recommendation": "silent", "meaningful_progress": True}
    assert_eq(should_notify(state, payload, "idle"), False, "silent -> never notify")


def test_should_notify_blocker(root: Path) -> None:
    state = {"progress": {"meaningful_iterations": 1}, "delivery": {"milestone_every_iterations": 2}}
    payload = {"notify_recommendation": "blocker", "meaningful_progress": True}
    assert_eq(should_notify(state, payload, "idle"), True, "blocker -> always notify")


def test_should_notify_final_status(root: Path) -> None:
    state = {"progress": {"meaningful_iterations": 1}, "delivery": {"milestone_every_iterations": 2}}
    payload = {"notify_recommendation": "auto", "meaningful_progress": True}
    assert_eq(should_notify(state, payload, "complete"), True, "complete -> notify")
    assert_eq(should_notify(state, payload, "failed"), True, "failed -> notify")
    assert_eq(should_notify(state, payload, "cancelled"), True, "cancelled -> notify")


def test_should_notify_auto_milestone(root: Path) -> None:
    state = {"progress": {"meaningful_iterations": 4}, "delivery": {"milestone_every_iterations": 2}}
    payload = {"notify_recommendation": "auto", "meaningful_progress": True}
    assert_eq(should_notify(state, payload, "idle"), True, "4 % 2 == 0 -> milestone notify")


def test_should_notify_auto_no_progress(root: Path) -> None:
    state = {"progress": {"meaningful_iterations": 4}, "delivery": {"milestone_every_iterations": 2}}
    payload = {"notify_recommendation": "auto", "meaningful_progress": False}
    assert_eq(should_notify(state, payload, "idle"), False, "no progress -> skip")


# --- compose_finish_update_text ---

def test_compose_finish_complete(root: Path) -> None:
    state = {"title": "Test Research", "id": "t1"}
    payload = {
        "summary": "Done!",
        "next_angle": "",
        "open_questions": [],
        "findings": [{"text": "Key fact"}],
        "notify_recommendation": "final",
    }
    text = compose_finish_update_text(state, payload, "complete", iteration_count=5, final_report_path="/tmp/r.md")
    assert_true(text is not None, "should produce text for complete")
    assert_in("завершено", text, "should mention completion")
    assert_in("Test Research", text, "should include title")


def test_compose_finish_blocker(root: Path) -> None:
    state = {"title": "Blocked", "id": "t2"}
    payload = {
        "summary": "Stuck",
        "next_angle": "Need user input",
        "open_questions": ["What region?"],
        "findings": [],
        "notify_recommendation": "blocker",
    }
    text = compose_finish_update_text(state, payload, "idle", iteration_count=3, final_report_path=None)
    assert_true(text is not None, "should produce text for blocker")
    assert_in("нужен", text.lower(), "should mention user input needed")


def test_compose_finish_silent(root: Path) -> None:
    state = {"title": "Silent", "id": "t3"}
    payload = {
        "summary": "Progressing",
        "next_angle": "Next",
        "open_questions": [],
        "findings": [],
        "notify_recommendation": "silent",
    }
    text = compose_finish_update_text(state, payload, "idle", iteration_count=1, final_report_path=None)
    assert_eq(text, None, "silent notification -> None")


# --- compose_failure_update_text ---

def test_compose_failure_cancelled(root: Path) -> None:
    text = compose_failure_update_text({"title": "Failed Task"}, "Timeout", "cancelled")
    assert_true(text is not None, "should produce text for cancelled")
    assert_in("остановлено", text, "should mention stop")


def test_compose_failure_failed(root: Path) -> None:
    text = compose_failure_update_text({"title": "Error Task"}, "Network error", "failed")
    assert_true(text is not None, "should produce text for failed")
    assert_in("блокер", text.lower(), "should mention blocker")


def test_compose_failure_other_status(root: Path) -> None:
    text = compose_failure_update_text({"title": "X"}, "err", "idle")
    assert_eq(text, None, "idle status -> no failure text")


# --- build_revision_diff ---

def test_build_revision_diff_new_revision(root: Path) -> None:
    old = {"review": {"revision_count": 1, "status": "pending"}, "artifacts": {"final_report_path": None}}
    new = {"review": {"revision_count": 2, "status": "approved"}, "artifacts": {"final_report_path": "/tmp/report.md"}}
    diff = build_revision_diff(old, new)
    assert_eq(diff["revision_from"], 1, "old revision")
    assert_eq(diff["revision_to"], 2, "new revision")
    assert_in("revision_count:1->2", diff["changes"], "revision change recorded")
    assert_in("final_report_updated", diff["changes"], "report update recorded")
    assert_in("review_status:pending->approved", diff["changes"], "status change recorded")


def test_build_revision_diff_no_change(root: Path) -> None:
    state = {"review": {"revision_count": 0, "status": "pending"}, "artifacts": {"final_report_path": None}}
    diff = build_revision_diff(state, state)
    assert_eq(diff["changes"], [], "no changes detected")


def test_build_revision_diff_none_old(root: Path) -> None:
    new = {"review": {"revision_count": 1, "status": "pending"}, "artifacts": {"final_report_path": "/tmp/r.md"}}
    diff = build_revision_diff(None, new)
    assert_eq(diff["revision_from"], 0, "None old -> 0")
    assert_in("final_report_updated", diff["changes"], "new report is a change from None")


# --- build_evidence_gaps ---

def test_build_evidence_gaps_with_open_questions(root: Path) -> None:
    state = {
        "working_memory": {"open_questions": ["Q1", "Q2"]},
        "finalization": {"last_validation_findings": []},
        "saturation": {"consecutive_low_yield": 0},
        "budget": {"max_iterations": 10},
        "progress": {"iteration_count": 3},
    }
    result = build_evidence_gaps(state)
    assert_eq(result["has_open_gaps"], True, "open questions -> gaps exist")
    assert_in("open_question:Q1", result["evidence_gaps"], "Q1 should be listed")


def test_build_evidence_gaps_budget_exhausted(root: Path) -> None:
    state = {
        "working_memory": {"open_questions": []},
        "finalization": {"last_validation_findings": []},
        "saturation": {"consecutive_low_yield": 0},
        "budget": {"max_iterations": 5},
        "progress": {"iteration_count": 5},
    }
    result = build_evidence_gaps(state)
    assert_in("budget_almost_exhausted", result["evidence_gaps"], "budget at limit")
    assert_in("hard_budget_limit_reached_mid_research", result["high_risk_assumptions"], "budget risk")


def test_build_evidence_gaps_clean(root: Path) -> None:
    state = {
        "working_memory": {"open_questions": []},
        "finalization": {"last_validation_findings": []},
        "saturation": {"consecutive_low_yield": 0},
        "budget": {"max_iterations": 10},
        "progress": {"iteration_count": 3},
    }
    result = build_evidence_gaps(state)
    assert_eq(result["has_open_gaps"], False, "no gaps")
    assert_eq(result["evidence_gaps"], [], "empty gaps list")


# --- compute_low_yield ---

def test_compute_low_yield_true(root: Path) -> None:
    assert_eq(
        compute_low_yield(
            {"new_sources": 0, "new_findings": 0},
            {"meaningful_progress": False},
        ),
        True,
        "zero new + no progress -> low yield",
    )


def test_compute_low_yield_false(root: Path) -> None:
    assert_eq(
        compute_low_yield(
            {"new_sources": 1, "new_findings": 0},
            {"meaningful_progress": False},
        ),
        False,
        "new sources present -> not low yield",
    )
    assert_eq(
        compute_low_yield(
            {"new_sources": 0, "new_findings": 0},
            {"meaningful_progress": True},
        ),
        False,
        "meaningful progress -> not low yield",
    )
