"""Tests for session feedback metrics."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import metrics  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _event(skill_id: str, outcome: str, ts: str = "2026-04-05T10:00:00Z", dim: str | None = None):
    return {
        "event_id": f"{skill_id}-{outcome}-{ts}",
        "timestamp": ts,
        "session_id": "sess-1",
        "skill_id": skill_id,
        "outcome": outcome,
        "confidence": 0.9,
        "correction_type": "rejection" if outcome == "correction" else None,
        "dimension_hint": dim,
    }


# ---------------------------------------------------------------------------
# Tests: compute_correction_rate
# ---------------------------------------------------------------------------


class TestCorrectionRate:
    def test_basic(self):
        events = [
            _event("skill-a", "correction"),
            _event("skill-a", "correction"),
            _event("skill-a", "acceptance"),
            _event("skill-a", "acceptance"),
            _event("skill-a", "acceptance"),
        ]
        result = metrics.compute_correction_rate(events, "skill-a")
        assert result["correction_rate"] == 0.4  # 2/5
        assert result["sample_size"] == 5
        assert result["sufficient_data"] is True

    def test_with_partials(self):
        events = [
            _event("skill-a", "correction"),
            _event("skill-a", "partial"),
            _event("skill-a", "acceptance"),
            _event("skill-a", "acceptance"),
            _event("skill-a", "acceptance"),
        ]
        result = metrics.compute_correction_rate(events, "skill-a")
        # (1 + 0.5*1) / 5 = 0.3
        assert result["correction_rate"] == 0.3

    def test_all_acceptances(self):
        events = [_event("skill-a", "acceptance") for _ in range(6)]
        result = metrics.compute_correction_rate(events, "skill-a")
        assert result["correction_rate"] == 0.0

    def test_all_corrections(self):
        events = [_event("skill-a", "correction") for _ in range(5)]
        result = metrics.compute_correction_rate(events, "skill-a")
        assert result["correction_rate"] == 1.0

    def test_insufficient_data(self):
        events = [
            _event("skill-a", "correction"),
            _event("skill-a", "acceptance"),
        ]
        result = metrics.compute_correction_rate(events, "skill-a")
        assert result["sufficient_data"] is False

    def test_empty(self):
        result = metrics.compute_correction_rate([], "skill-a")
        assert result["correction_rate"] == 0.0
        assert result["sample_size"] == 0
        assert result["sufficient_data"] is False

    def test_filters_by_skill(self):
        events = [
            _event("skill-a", "correction"),
            _event("skill-b", "acceptance"),
            _event("skill-a", "acceptance"),
            _event("skill-a", "acceptance"),
            _event("skill-a", "acceptance"),
            _event("skill-a", "acceptance"),
        ]
        result = metrics.compute_correction_rate(events, "skill-a")
        assert result["correction_rate"] == 0.2  # 1/5
        assert result["sample_size"] == 5


# ---------------------------------------------------------------------------
# Tests: compute_correction_trend
# ---------------------------------------------------------------------------


class TestCorrectionTrend:
    def test_stable(self):
        events = [_event("s", "acceptance", ts="2026-04-04T10:00:00Z") for _ in range(5)]
        events += [_event("s", "acceptance", ts="2026-03-04T10:00:00Z") for _ in range(5)]
        result = metrics.compute_correction_trend(events, "s", window_days=30)
        assert result["direction"] == "stable"

    def test_no_events(self):
        result = metrics.compute_correction_trend([], "s")
        assert result["trend"] == 0.0


# ---------------------------------------------------------------------------
# Tests: compute_hotspot_dimensions
# ---------------------------------------------------------------------------


class TestHotspotDimensions:
    def test_groups_by_dimension(self):
        events = [
            _event("s", "correction", dim="accuracy"),
            _event("s", "correction", dim="accuracy"),
            _event("s", "correction", dim="coverage"),
            _event("s", "acceptance"),  # no dimension, not a correction
        ]
        result = metrics.compute_hotspot_dimensions(events, "s")
        assert result == {"accuracy": 2, "coverage": 1}

    def test_ignores_none_dimension(self):
        events = [
            _event("s", "correction", dim=None),
        ]
        result = metrics.compute_hotspot_dimensions(events, "s")
        assert result == {}

    def test_includes_partials(self):
        events = [
            _event("s", "partial", dim="efficiency"),
        ]
        result = metrics.compute_hotspot_dimensions(events, "s")
        assert result == {"efficiency": 1}


# ---------------------------------------------------------------------------
# Tests: format_metrics_report
# ---------------------------------------------------------------------------


class TestFormatReport:
    def test_basic_format(self):
        metrics_data = [{
            "skill_id": "cpp-expert",
            "correction_rate": 0.4,
            "sample_size": 10,
            "sufficient_data": True,
            "corrections": 3,
            "partials": 2,
            "acceptances": 5,
            "hotspot_dimensions": {"accuracy": 2, "coverage": 1},
        }]
        report = metrics.format_metrics_report(metrics_data)
        assert "cpp-expert" in report
        assert "0.40" in report
        assert "accuracy=2" in report
