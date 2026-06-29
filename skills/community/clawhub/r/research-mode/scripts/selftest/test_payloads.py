"""Unit tests for research_mode_payloads: normalization of sources, findings, artifacts, summaries."""
from __future__ import annotations

from pathlib import Path

from .helpers import assert_eq, assert_true

from research_mode_payloads import (
    adequacy_defaults,
    normalize_analysis_artifacts,
    normalize_adequacy_review,
    normalize_database_summary,
    normalize_findings,
    normalize_sources,
    normalize_string_list,
    normalize_vision_summary,
    result_template,
)
from research_mode_utils import ValidationError


def test_normalize_string_list_basic(root: Path) -> None:
    assert_eq(normalize_string_list(None), [], "None -> empty list")
    assert_eq(normalize_string_list([]), [], "empty list -> empty list")
    assert_eq(normalize_string_list(["a", "b"]), ["a", "b"], "simple list preserved")


def test_normalize_string_list_strips_and_filters(root: Path) -> None:
    assert_eq(
        normalize_string_list(["  hello ", None, "", "  ", "world"]),
        ["hello", "world"],
        "should strip whitespace and filter blanks/None",
    )


def test_normalize_string_list_rejects_non_list(root: Path) -> None:
    try:
        normalize_string_list("not a list")
        raise AssertionError("should have raised ValidationError")
    except ValidationError:
        pass


def test_normalize_sources_none_and_empty(root: Path) -> None:
    assert_eq(normalize_sources(None), [], "None -> empty")
    assert_eq(normalize_sources([]), [], "empty -> empty")


def test_normalize_sources_string_items(root: Path) -> None:
    result = normalize_sources(["https://example.com", "  ", "https://other.com"])
    assert_eq(len(result), 2, "blank strings filtered out")
    assert_eq(result[0], {"url": "https://example.com"}, "string -> url object")


def test_normalize_sources_dict_items(root: Path) -> None:
    result = normalize_sources([
        {"url": "https://a.com", "title": "Title A", "extra_field": "ignored"},
        {"url": "  ", "title": "  "},
    ])
    assert_eq(len(result), 1, "empty-only dict should be filtered")
    assert_eq(result[0], {"url": "https://a.com", "title": "Title A"}, "known keys preserved")


def test_normalize_sources_rejects_non_list(root: Path) -> None:
    try:
        normalize_sources("not a list")
        raise AssertionError("should raise ValidationError")
    except ValidationError:
        pass


def test_normalize_sources_rejects_invalid_item(root: Path) -> None:
    try:
        normalize_sources([42])
        raise AssertionError("should raise ValidationError for non-str non-dict item")
    except ValidationError:
        pass


def test_normalize_findings_none_and_empty(root: Path) -> None:
    assert_eq(normalize_findings(None), [], "None -> empty")
    assert_eq(normalize_findings([]), [], "empty -> empty")


def test_normalize_findings_string_items(root: Path) -> None:
    result = normalize_findings(["Important fact", "  "])
    assert_eq(len(result), 1, "blank strings filtered")
    assert_eq(result[0], {"kind": "note", "text": "Important fact"}, "string -> note finding")


def test_normalize_findings_dict_with_source_urls(root: Path) -> None:
    result = normalize_findings([{
        "kind": "fact",
        "text": "Discovery",
        "source_urls": ["https://a.com", "", None, "https://b.com"],
    }])
    assert_eq(len(result), 1, "single valid finding")
    assert_eq(result[0]["source_urls"], ["https://a.com", "https://b.com"], "cleaned source_urls")


def test_normalize_findings_skips_no_text(root: Path) -> None:
    result = normalize_findings([{"kind": "fact"}, {"kind": "note", "text": ""}])
    assert_eq(result, [], "findings without text should be skipped")


def test_normalize_analysis_artifacts_dedup(root: Path) -> None:
    result = normalize_analysis_artifacts([
        "/path/a.py",
        "/path/a.py",
        {"path": "/path/b.py", "kind": "script"},
        {"path": "/path/b.py", "kind": "script"},
    ])
    assert_eq(len(result), 2, "duplicates should be removed")


def test_normalize_analysis_artifacts_string_and_dict(root: Path) -> None:
    result = normalize_analysis_artifacts([
        "/path/file.py",
        {"path": "/path/chart.png", "kind": "chart", "note": "Sales chart"},
    ])
    assert_eq(result[0], {"path": "/path/file.py", "kind": "artifact"}, "string -> artifact")
    assert_eq(result[1]["note"], "Sales chart", "note preserved")


def test_normalize_analysis_artifacts_empty_path_skipped(root: Path) -> None:
    result = normalize_analysis_artifacts(["", "  ", {"path": ""}])
    assert_eq(result, [], "empty paths should be skipped")


def test_normalize_database_summary_valid(root: Path) -> None:
    result = normalize_database_summary({
        "db_path": "/tmp/data.db",
        "purpose": "Analysis store",
        "tables": ["users", "orders"],
        "row_counts": {"users": 100, "orders": "250"},
    })
    assert_eq(result["db_path"], "/tmp/data.db", "db_path preserved")
    assert_eq(result["tables"], ["users", "orders"], "tables preserved")
    assert_eq(result["row_counts"]["orders"], 250, "string count should be cast to int")


def test_normalize_database_summary_none_and_empty(root: Path) -> None:
    assert_eq(normalize_database_summary(None), None, "None -> None")
    assert_eq(normalize_database_summary(""), None, "empty string -> None")
    assert_eq(normalize_database_summary({}), None, "empty dict -> None")


def test_normalize_database_summary_invalid_row_count(root: Path) -> None:
    try:
        normalize_database_summary({"row_counts": {"t": "not_a_number"}})
        raise AssertionError("should raise ValidationError for non-integer row count")
    except ValidationError:
        pass


def test_normalize_vision_summary_valid(root: Path) -> None:
    result = normalize_vision_summary({
        "purpose": "OCR receipts",
        "images_reviewed": "5",
        "confidence": "high",
    })
    assert_eq(result["purpose"], "OCR receipts", "purpose preserved")
    assert_eq(result["images_reviewed"], 5, "string count cast to int")
    assert_eq(result["confidence"], "high", "confidence preserved")


def test_normalize_vision_summary_none(root: Path) -> None:
    assert_eq(normalize_vision_summary(None), None, "None -> None")
    assert_eq(normalize_vision_summary(""), None, "empty -> None")


def test_normalize_vision_summary_invalid_images_count(root: Path) -> None:
    try:
        normalize_vision_summary({"images_reviewed": "abc"})
        raise AssertionError("should raise ValidationError")
    except ValidationError:
        pass


def test_result_template_shape(root: Path) -> None:
    tmpl = result_template()
    assert_eq(tmpl["phase"], "search", "default phase should be search")
    assert_eq(tmpl["meaningful_progress"], True, "default meaningful_progress")
    assert_eq(tmpl["should_complete"], False, "default should_complete")
    assert_true(isinstance(tmpl["sources"], list), "sources should be a list")
    assert_true(isinstance(tmpl["findings"], list), "findings should be a list")
    assert_eq(
        tmpl["finalization"]["status"],
        "not_started",
        "result template should expose finalization trace defaults",
    )
    assert_true(
        isinstance(tmpl["finalization"]["validation_evidence"], list),
        "result template finalization evidence should be a list",
    )
    assert_eq(
        tmpl["adequacy"]["status"],
        "not_started",
        "result template should expose adequacy review defaults",
    )
    assert_eq(
        tmpl["preflight"]["decision"],
        "go",
        "result template should expose preflight decision defaults",
    )
    assert_true(
        isinstance(tmpl["adequacy"]["coverage_gaps"], list),
        "result template adequacy coverage_gaps should be a list",
    )


def test_result_template_independent_copies(root: Path) -> None:
    """Each call should return an independent copy."""
    t1 = result_template()
    t2 = result_template()
    t1["sources"].append({"url": "test"})
    t1["finalization"]["validation_evidence"].append({"kind": "manual_review"})
    t1["adequacy"]["coverage_gaps"].append({"gap": "missing forum evidence"})
    t1["preflight"]["warnings"].append("network fallback needed")
    assert_eq(len(t2["sources"]), 0, "templates should be independent")
    assert_eq(
        len(t2["finalization"]["validation_evidence"]),
        0,
        "finalization template lists should be independent",
    )
    assert_eq(
        len(t2["adequacy"]["coverage_gaps"]),
        0,
        "adequacy template lists should be independent",
    )
    assert_eq(
        len(t2["preflight"]["warnings"]),
        0,
        "preflight template lists should be independent",
    )


def test_adequacy_defaults_shape(root: Path) -> None:
    defaults = adequacy_defaults()
    assert_eq(defaults["status"], "not_started", "default adequacy status")
    assert_eq(defaults["max_attempts"], 2, "default max attempts")
    assert_eq(defaults["attempt_count"], 0, "default attempt count")
    assert_true(isinstance(defaults["covered_requirements"], list), "requirements list")
    assert_true(isinstance(defaults["coverage_gaps"], list), "coverage gaps list")
    assert_true(isinstance(defaults["validation_evidence"], list), "evidence list")


def test_normalize_adequacy_review_valid(root: Path) -> None:
    review = normalize_adequacy_review(
        {
            "status": "needs_research",
            "goal_alignment": "Reliability evidence is incomplete.",
            "coverage_summary": "Only marketplace reviews checked.",
            "covered_requirements": ["price range covered"],
            "coverage_gaps": [
                {"gap": "repair forums missing", "severity": "blocking"}
            ],
            "evidence_risks": ["recent-review bias"],
            "contradictions": [],
            "recommended_next_phase": "search",
            "recommended_next_angle": "Search repair forums.",
            "blocking_reasons": ["insufficient reliability evidence"],
            "validation_evidence": [
                {"check": "coverage", "result": "failed"}
            ],
            "max_attempts": "4",
            "attempt_count": "1",
            "last_checked_at": "2026-06-15T16:00:00Z",
            "last_checked_by": "worker",
            "operator_next_action": {"kind": "worker_rework"},
        }
    )

    assert_eq(review["status"], "needs_research", "status preserved")
    assert_eq(review["recommended_next_phase"], "search", "next phase preserved")
    assert_eq(review["max_attempts"], 4, "max attempts cast to int")
    assert_eq(review["attempt_count"], 1, "attempt count cast to int")
    assert_eq(
        review["covered_requirements"],
        [{"summary": "price range covered"}],
        "string requirement should normalize to summary object",
    )
    assert_eq(
        review["evidence_risks"],
        [{"summary": "recent-review bias"}],
        "string risk should normalize to summary object",
    )
    assert_eq(
        review["operator_next_action"],
        {"kind": "worker_rework"},
        "operator_next_action trace is normalized but not trusted by lifecycle",
    )


def test_normalize_adequacy_review_rejects_invalid_status(root: Path) -> None:
    try:
        normalize_adequacy_review({"status": "approved"})
        raise AssertionError("should raise ValidationError")
    except ValidationError:
        pass


def test_normalize_adequacy_review_rejects_invalid_next_phase(root: Path) -> None:
    try:
        normalize_adequacy_review(
            {"status": "needs_research", "recommended_next_phase": "review"}
        )
        raise AssertionError("should raise ValidationError")
    except ValidationError:
        pass
