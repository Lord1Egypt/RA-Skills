"""Layer 1b: Unit tests for rubric loading, schema validation, and parsing."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from quorum.models import Rubric, RubricCriterion, Severity
from quorum.rubrics.loader import BUILTIN_DIR, RubricLoader

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def loader() -> RubricLoader:
    return RubricLoader()


# ── RubricLoader basics ──────────────────────────────────────────────────────


class TestRubricLoader:
    def test_list_builtin_returns_names(self, loader):
        names = loader.list_builtin()
        assert isinstance(names, list)
        # We know at least these exist from the codebase
        assert "research-synthesis" in names
        assert "agent-config" in names

    def test_load_builtin_research_synthesis(self, loader):
        rubric = loader.load("research-synthesis")
        assert rubric.name is not None
        assert rubric.domain is not None
        assert len(rubric.criteria) > 0

    def test_load_builtin_agent_config(self, loader):
        rubric = loader.load("agent-config")
        assert len(rubric.criteria) > 0

    def test_load_builtin_python_code(self, loader):
        rubric = loader.load("python-code")
        assert len(rubric.criteria) > 0

    def test_load_from_path(self, loader):
        rubric = loader.load(FIXTURES / "rubrics" / "custom-research.json")
        assert rubric.name == "custom-research"
        assert rubric.domain == "research"
        assert len(rubric.criteria) == 2

    def test_load_not_found_raises(self, loader):
        with pytest.raises(FileNotFoundError, match="Rubric not found"):
            loader.load("nonexistent-rubric")

    def test_load_invalid_json_raises(self, loader, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text("{invalid json}")
        with pytest.raises(ValueError, match="Invalid JSON"):
            loader.load(bad)


# ── Rubric schema validation ─────────────────────────────────────────────────


class TestRubricSchema:
    def test_valid_rubric_parses(self, loader):
        rubric = loader.load("research-synthesis")
        assert isinstance(rubric, Rubric)
        for c in rubric.criteria:
            assert isinstance(c, RubricCriterion)

    def test_required_fields_present(self, loader):
        rubric = loader.load("research-synthesis")
        for c in rubric.criteria:
            assert c.id
            assert c.criterion
            assert c.severity in Severity
            assert c.evidence_required is not None

    def test_severity_enum_valid(self, loader):
        rubric = loader.load("research-synthesis")
        valid_severities = set(Severity)
        for c in rubric.criteria:
            assert c.severity in valid_severities

    def test_custom_rubric_fields(self, loader):
        rubric = loader.load(FIXTURES / "rubrics" / "custom-research.json")
        c = rubric.criteria[0]
        assert c.id == "CR-001"
        assert c.severity == Severity.HIGH
        assert "abstract" in c.criterion.lower()


# ── Duplicate IDs ────────────────────────────────────────────────────────────


class TestRubricDuplicateIDs:
    def test_duplicate_ids_detectable(self, loader):
        """Rubrics should not have duplicate criterion IDs."""
        for name in loader.list_builtin():
            rubric = loader.load(name)
            ids = [c.id for c in rubric.criteria]
            assert len(ids) == len(set(ids)), f"Duplicate IDs in rubric '{name}'"


# ── Unicode handling ─────────────────────────────────────────────────────────


class TestRubricUnicode:
    def test_unicode_in_criterion(self, tmp_path):
        rubric_data = {
            "name": "unicode-test",
            "domain": "test",
            "criteria": [
                {
                    "id": "U-001",
                    "criterion": "Must handle UTF-8: cafe\u0301, \u00fc\u00e4\u00f6",
                    "severity": "MEDIUM",
                    "evidence_required": "Unicode preserved",
                    "why": "Internationalization",
                },
            ],
        }
        path = tmp_path / "unicode.json"
        path.write_text(json.dumps(rubric_data, ensure_ascii=False))

        loader = RubricLoader()
        rubric = loader.load(path)
        assert "\u00e4" in rubric.criteria[0].criterion or "cafe" in rubric.criteria[0].criterion


# ── Custom rubric loading ────────────────────────────────────────────────────


class TestCustomRubricLoading:
    def test_load_rubric_from_file(self, loader):
        rubric = loader.load(FIXTURES / "rubrics" / "custom-research.json")
        assert rubric.name == "custom-research"

    def test_rubric_not_found_helpful_message(self, loader):
        with pytest.raises(FileNotFoundError) as exc_info:
            loader.load("definitely-missing")
        msg = str(exc_info.value)
        assert "Built-in rubrics" in msg

    def test_builtin_rubric_by_name(self, loader):
        names = loader.list_builtin()
        if names:
            rubric = loader.load(names[0])
            assert isinstance(rubric, Rubric)

    def test_severity_fallback_for_unknown(self, tmp_path):
        rubric_data = {
            "name": "fallback-test",
            "domain": "test",
            "criteria": [
                {
                    "id": "F-001",
                    "criterion": "Test",
                    "severity": "UNKNOWN_SEVERITY",
                    "evidence_required": "x",
                    "why": "y",
                },
            ],
        }
        path = tmp_path / "fallback.json"
        path.write_text(json.dumps(rubric_data))

        loader = RubricLoader()
        rubric = loader.load(path)
        # Should fall back to MEDIUM per loader logic
        assert rubric.criteria[0].severity == Severity.MEDIUM

    def test_alternative_field_names(self, tmp_path):
        rubric_data = {
            "name": "alt-fields",
            "domain": "test",
            "criteria": [
                {
                    "id": "A-001",
                    "criterion": "Test",
                    "severity": "HIGH",
                    "evidence_instruction": "Alternative field name for evidence",
                    "rationale": "Alternative field name for why",
                },
            ],
        }
        path = tmp_path / "alt.json"
        path.write_text(json.dumps(rubric_data))

        loader = RubricLoader()
        rubric = loader.load(path)
        assert rubric.criteria[0].evidence_required == "Alternative field name for evidence"
        assert rubric.criteria[0].why == "Alternative field name for why"
