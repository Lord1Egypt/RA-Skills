"""Tests for sal.monitor.classifier — severity + dedup escalation."""

import pytest

from sal.monitor.behaviors import BehaviorHit, Severity
from sal.monitor.classifier import classify_hits, needs_alert, needs_block


class TestClassifier:
    def test_empty_hits(self):
        """should return LOW for no hits."""
        result = classify_hits([])
        assert result["severity"] == Severity.LOW
        assert result["unique_behaviors"] == 0

    def test_single_hit(self):
        """should use the hit's severity directly."""
        hits = [BehaviorHit("B001", Severity.HIGH, "test")]
        result = classify_hits(hits)
        assert result["severity"] == Severity.HIGH
        assert result["unique_behaviors"] == 1

    def test_dedup_same_behavior(self):
        """should dedup same behavior_id — count once."""
        hits = [
            BehaviorHit("B001", Severity.HIGH, "match 1"),
            BehaviorHit("B001", Severity.HIGH, "match 2"),
            BehaviorHit("B001", Severity.HIGH, "match 3"),
        ]
        result = classify_hits(hits)
        assert result["unique_behaviors"] == 1
        assert result["total_hits"] == 3
        assert result["severity"] == Severity.HIGH  # NOT escalated
        assert result["escalated"] is False

    def test_10_same_behavior_no_escalation(self):
        """should NOT escalate 10x same behavior (false positive fix)."""
        hits = [BehaviorHit("B008", Severity.LOW, f"hit {i}") for i in range(10)]
        result = classify_hits(hits)
        assert result["severity"] == Severity.LOW
        assert result["escalated"] is False

    def test_escalate_3_different_behaviors(self):
        """should escalate when 3+ DIFFERENT behaviors detected."""
        hits = [
            BehaviorHit("B001", Severity.MEDIUM, "bypass"),
            BehaviorHit("B003", Severity.MEDIUM, "deviation"),
            BehaviorHit("B007", Severity.MEDIUM, "priv esc"),
        ]
        result = classify_hits(hits)
        assert result["severity"] == Severity.HIGH  # MEDIUM + 1
        assert result["escalated"] is True

    def test_cap_at_max_plus_one(self):
        """should cap escalation at highest + 1."""
        hits = [
            BehaviorHit("B001", Severity.HIGH, "one"),
            BehaviorHit("B002", Severity.HIGH, "two"),
            BehaviorHit("B003", Severity.HIGH, "three"),
        ]
        result = classify_hits(hits)
        assert result["severity"] == Severity.CRITICAL  # HIGH + 1
        assert result["escalated"] is True

    def test_cap_does_not_exceed_critical(self):
        """should never go above CRITICAL."""
        hits = [
            BehaviorHit("B004", Severity.CRITICAL, "one"),
            BehaviorHit("B005", Severity.CRITICAL, "two"),
            BehaviorHit("B009", Severity.CRITICAL, "three"),
        ]
        result = classify_hits(hits)
        assert result["severity"] == Severity.CRITICAL  # Already max

    def test_llm_hit_floor_medium(self):
        """should floor LLM hits at MEDIUM."""
        hits = [BehaviorHit("B002", Severity.LOW, "llm finding", source="llm")]
        result = classify_hits(hits)
        assert result["severity"] == Severity.MEDIUM

    def test_dedup_keeps_highest_severity(self):
        """should keep highest severity when deduping same behavior."""
        hits = [
            BehaviorHit("B001", Severity.MEDIUM, "first"),
            BehaviorHit("B001", Severity.HIGH, "second"),
        ]
        result = classify_hits(hits)
        assert result["severity"] == Severity.HIGH


class TestAlertDecisions:
    def test_high_needs_alert(self):
        assert needs_alert(Severity.HIGH) is True

    def test_medium_no_alert(self):
        assert needs_alert(Severity.MEDIUM) is False

    def test_critical_needs_block(self):
        assert needs_block(Severity.CRITICAL) is True

    def test_high_no_block(self):
        assert needs_block(Severity.HIGH) is False
