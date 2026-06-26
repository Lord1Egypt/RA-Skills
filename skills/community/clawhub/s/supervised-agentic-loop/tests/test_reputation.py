"""Tests for sal.reputation — EMA scoring + SQLite persistence."""

import os
import tempfile

import pytest

from sal.reputation import (
    DEFAULT_REPUTATION,
    SCORE_CRASH,
    SCORE_FIRST_PASS,
    SCORE_HALLUCINATION,
    SCORE_NO_CHANGE,
    ReputationDB,
)


@pytest.fixture
def rep_db():
    """Create a temp reputation DB."""
    d = tempfile.mkdtemp()
    db_path = os.path.join(d, "rep.db")
    db = ReputationDB(db_path)
    yield db
    db.close()


class TestReputationDB:
    def test_default_reputation(self, rep_db):
        """should start with default reputation for unknown agents."""
        assert rep_db.get_score("new-agent") == DEFAULT_REPUTATION

    def test_update_increases_on_success(self, rep_db):
        """should increase reputation on SCORE_FIRST_PASS."""
        result = rep_db.update("agent-a", 1, SCORE_FIRST_PASS, status="keep")
        assert result["reputation_after"] > result["reputation_before"]

    def test_update_decreases_on_hallucination(self, rep_db):
        """should decrease reputation on SCORE_HALLUCINATION."""
        result = rep_db.update("agent-b", 1, SCORE_HALLUCINATION, status="crash")
        assert result["reputation_after"] < result["reputation_before"]

    def test_ema_convergence(self, rep_db):
        """should converge to 1.0 with repeated successes."""
        for i in range(50):
            rep_db.update("converge-agent", i, SCORE_FIRST_PASS, status="keep")
        score = rep_db.get_score("converge-agent")
        assert score > 0.95

    def test_reputation_clamped(self, rep_db):
        """should clamp reputation to [-1.0, 1.0]."""
        for i in range(100):
            rep_db.update("clamp-agent", i, SCORE_HALLUCINATION, status="crash")
        score = rep_db.get_score("clamp-agent")
        assert score >= -1.0

    def test_get_level_autonomous(self, rep_db):
        """should be 'autonomous' above 0.8."""
        for i in range(20):
            rep_db.update("auto-agent", i, SCORE_FIRST_PASS, status="keep")
        level = rep_db.get_level("auto-agent")
        assert level["level"] == "autonomous"

    def test_get_level_suspended(self, rep_db):
        """should be 'suspended' at or below 0.2."""
        for i in range(50):
            rep_db.update("bad-agent", i, SCORE_HALLUCINATION, status="crash")
        level = rep_db.get_level("bad-agent")
        assert level["level"] == "suspended"

    def test_suspend_and_unsuspend(self, rep_db):
        """should suspend with reason and unsuspend with audit trail."""
        rep_db.update("sus-agent", 1, SCORE_CRASH, status="crash")
        rep_db.suspend("sus-agent", "too many failures")

        # Unsuspend
        result = rep_db.unsuspend("sus-agent", "human verified safe")
        assert result["reputation_after"] == 0.5
        assert result["reason"] == "human verified safe"

    def test_history(self, rep_db):
        """should return iteration history."""
        rep_db.update("hist-agent", 1, SCORE_FIRST_PASS, status="keep",
                      hypothesis="try X")
        rep_db.update("hist-agent", 2, SCORE_NO_CHANGE, status="discard",
                      hypothesis="try Y")

        history = rep_db.get_history("hist-agent")
        assert len(history) == 2
        assert history[0]["iteration"] == 2  # Most recent first
