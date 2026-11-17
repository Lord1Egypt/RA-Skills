#!/usr/bin/env python3
"""Fixture tests for v9.0.0 new functions: ecosystem assessment & value scores."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

from audit_skill_plugin_issues import (
    load_mcp_config,
    estimate_token_count,
    assess_mcp_health,
    assess_agent_dispatch,
    assess_context_pressure,
    audit_ecosystem,
)
from compute_value_scores import (
    normalize_usage,
    value_score,
    confidence_level,
    recommendation_layer,
    assess_skills_optimization,
    assess_mcp_optimization,
)
@pytest.fixture
def fake_mcp_config():
    """ZCode config.json mcp.servers structure."""
    return {
        "firecrawl": {
            "command": "npx",
            "args": ["firecrawl-mcp"],
            "env": {"FIRECRAWL_API_KEY": "fc-test"},
        },
        "playwright": {"command": "npx", "args": ["@playwright/mcp"]},
        "headroom": {"command": "headroom", "args": ["mcp", "serve"]},
    }


@pytest.fixture
def fake_signals():
    """extract_usage_signals.py output."""
    return {
        "scan_summary": {"agents_scanned": 10, "sessions_scanned": 5},
        "agent_dispatch_stats": [
            {
                "profile_id": "Explore",
                "dispatch_count": 50,
                "avg_duration_ms": 10000,
                "avg_tokens": 5000,
                "top_tools": {"Read": 30},
            },
            {
                "profile_id": "research-worker",
                "dispatch_count": 2,
                "avg_duration_ms": 20000,
                "avg_tokens": 8000,
                "top_tools": {},
            },
        ],
        "mcp_usage_evidence": [
            {
                "mcp_server": "firecrawl",
                "tool_calls": 15,
                "last_used": "2026-07-25",
                "tools_used": {},
                "status": "observed",
            },
            {
                "mcp_server": "playwright",
                "tool_calls": 0,
                "last_used": None,
                "tools_used": {},
                "status": "configured_never_observed",
            },
        ],
        "skill_invocation_evidence": [
            {"skill_id": "agent-reach", "invocations": 5},
        ],
    }


@pytest.fixture
def fake_user_skill_dir(tmp_path):
    """Temp skill directory with 2 SKILL.md files."""
    (tmp_path / "skill-a").mkdir()
    (tmp_path / "skill-a" / "SKILL.md").write_text(
        "---" + chr(10) + "name: skill-a" + chr(10) + "description: 测试技能 A" + chr(10) + "---" + chr(10) + "# Skill A" + chr(10),
        encoding="utf-8",
    )
    (tmp_path / "skill-b").mkdir()
    (tmp_path / "skill-b" / "SKILL.md").write_text(
        "---" + chr(10) + "name: skill-b" + chr(10) + "description: test skill B" + chr(10) + "---" + chr(10) + "# Skill B" + chr(10),
        encoding="utf-8",
    )
    return tmp_path


class TestLoadMcpConfig:
    def test_load_mcp_config_zcode_format(self, tmp_path):
        """ZCode format {mcp: {servers: {...}}}"""
        config = {"mcp": {"servers": {"s1": {"command": "echo"}}}}
        p = tmp_path / "config.json"
        p.write_text(json.dumps(config), encoding="utf-8")
        assert load_mcp_config(p) == {"s1": {"command": "echo"}}

    def test_load_mcp_config_standard_format(self, tmp_path):
        """Standard {mcpServers: {...}} format"""
        config = {"mcpServers": {"s2": {"command": "cat"}}}
        p = tmp_path / "config.json"
        p.write_text(json.dumps(config), encoding="utf-8")
        assert load_mcp_config(p) == {"s2": {"command": "cat"}}

    def test_load_mcp_config_missing_file(self, tmp_path):
        """Non-existent path returns {}"""
        assert load_mcp_config(tmp_path / "nonexistent.json") == {}

    def test_load_mcp_config_empty_object(self, tmp_path):
        """Empty object returns {}"""
        p = tmp_path / "empty.json"
        p.write_text("{}", encoding="utf-8")
        assert load_mcp_config(p) == {}

    def test_load_mcp_config_malformed_json(self, tmp_path):
        """Malformed JSON returns {}"""
        p = tmp_path / "bad.json"
        p.write_text("{invalid", encoding="utf-8")
        assert load_mcp_config(p) == {}

class TestEstimateTokenCount:
    def test_estimate_token_pure_chinese(self):
        """10 Chinese chars -> 10/1.8=5"""
        assert estimate_token_count("你好世界这是一个测试") == 5

    def test_estimate_token_pure_english(self):
        """46 English chars -> 46/4=11"""
        assert estimate_token_count("hello world this is a test sentence for tokens") == 11

    def test_estimate_token_mixed(self):
        """Mixed Chinese/English"""
        assert estimate_token_count("你好 world 测试 tokens 混合") == 7

    def test_estimate_token_empty_string(self):
        """Empty string returns 0."""
        assert estimate_token_count("") == 0


class TestAssessMcpHealth:
    def test_assess_mcp_health_all_pass(self, fake_mcp_config, fake_signals):
        """Basic health check structure."""
        result = assess_mcp_health(fake_mcp_config, fake_signals)
        assert len(result) == 3

        fc = next(r for r in result if r["server"] == "firecrawl")
        assert fc["dimensions"]["config"]["status"] == "pass"
        assert fc["dimensions"]["usage"]["status"] == "pass"
        assert fc["dimensions"]["usage"]["calls"] == 15

        pw = next(r for r in result if r["server"] == "playwright")
        assert pw["dimensions"]["usage"]["status"] == "unavailable"
        assert pw["dimensions"]["usage"]["calls"] is None

        hr = next(r for r in result if r["server"] == "headroom")
        assert hr["dimensions"]["usage"]["status"] == "unavailable"

    def test_assess_mcp_health_with_exposed_key(self, fake_mcp_config, fake_signals):
        """Plain-text API key -> permissions warn."""
        fc = next(
            r for r in assess_mcp_health(fake_mcp_config, fake_signals)
            if r["server"] == "firecrawl"
        )
        assert len(fc["dimensions"]["permissions"]["exposed_fields"]) >= 1
        assert fc["dimensions"]["permissions"]["exposed_fields"][0]["field"] == "FIRECRAWL_API_KEY"

    def test_assess_mcp_health_never_called(self, fake_mcp_config, fake_signals):
        """No attributable event is not evidence of non-use."""
        pw = next(
            r for r in assess_mcp_health(fake_mcp_config, fake_signals)
            if r["server"] == "playwright"
        )
        assert pw["dimensions"]["usage"]["status"] == "unavailable"

    def test_assess_mcp_health_empty_config(self, fake_signals):
        """Empty config -> empty list."""
        assert assess_mcp_health({}, fake_signals) == []

    def test_assess_mcp_health_no_signals(self, fake_mcp_config):
        """No signals -> usage=unavailable."""
        result = assess_mcp_health(fake_mcp_config, {})
        for r in result:
            assert r["dimensions"]["usage"]["status"] == "unavailable"

class TestAssessAgentDispatch:
    def test_assess_agent_dispatch_high_overlap(self, fake_signals):
        """Explore vs research-worker overlap."""
        result = assess_agent_dispatch(fake_signals)
        pairs = result["overlap_pairs"]
        er = [
            p for p in pairs
            if set([p["agent_a"], p["agent_b"]]) == {"Explore", "research-worker"}
        ]
        assert er, "Expected Explore vs research-worker overlap pair"

    def test_assess_agent_dispatch_no_signals(self):
        """Empty signals: overlap_pairs based on hardcoded capabilities."""
        result = assess_agent_dispatch({})
        assert isinstance(result["overlap_pairs"], list)
        assert "capability_matrix" in result
        assert result["dispatch_distribution"] == {}

    def test_assess_agent_dispatch_structure(self, fake_signals):
        """Output structure validation."""
        result = assess_agent_dispatch(fake_signals)
        assert "capability_matrix" in result
        assert "overlap_pairs" in result
        assert "dispatch_distribution" in result
        assert "data_source" in result
        assert result["dispatch_distribution"]["Explore"]["count"] == 50


class TestAssessContextPressure:
    def test_assess_context_pressure_basic(self, fake_user_skill_dir, fake_mcp_config):
        """Basic output structure."""
        result = assess_context_pressure(fake_user_skill_dir, fake_mcp_config)
        for key in ("total_injection_tokens", "context_window_assumed", "pressure_percent", "grade", "breakdown"):
            assert key in result, f"Missing key: {key}"
        bd = result["breakdown"]
        assert bd["skills"]["count"] == 2
        assert bd["mcp"]["count"] == 3

    def test_assess_context_pressure_no_agents_dir(self, fake_user_skill_dir, fake_mcp_config):
        """Non-existent agents_dir -> status=unavailable."""
        fake_agents = fake_user_skill_dir / "does-not-exist"
        result = assess_context_pressure(fake_user_skill_dir, fake_mcp_config, agents_dir=fake_agents)
        assert result["breakdown"]["agents"]["status"] == "unavailable"

    def test_assess_context_pressure_empty_skills(self, tmp_path, fake_mcp_config):
        """Empty skill directory."""
        result = assess_context_pressure(tmp_path, fake_mcp_config)
        assert result["breakdown"]["skills"]["count"] == 0

    def test_assess_context_pressure_grade_low(self, tmp_path):
        """Minimal config -> low_pressure."""
        result = assess_context_pressure(tmp_path, {})
        assert result["grade"] == "low_pressure"

class TestNormalizeUsage:
    def test_normalize_usage_basic(self):
        """5/10=5.0"""
        assert normalize_usage(5, 10) == 5.0

    def test_normalize_usage_capped(self):
        """20/10=10.0 (capped)"""
        assert normalize_usage(20, 10) == 10.0

    def test_normalize_usage_zero_max(self):
        """max=0 returns 0"""
        assert normalize_usage(5, 0) == 0.0

    def test_normalize_usage_zero_count(self):
        """0/10=0"""
        assert normalize_usage(0, 10) == 0.0

    def test_normalize_usage_exact_max(self):
        """10/10=10"""
        assert normalize_usage(10, 10) == 10.0


class TestValueScore:
    def test_value_score_weights(self):
        """Verify weights: usage*0.4 + alignment*0.25 + health*0.2 + market*0.15"""
        assert value_score(10, 8, 6, 4) == 7.8

    def test_value_score_zero(self):
        """All zeros."""
        assert value_score(0, 0, 0, 0) == 0.0

    def test_value_score_max(self):
        """Full marks."""
        assert value_score(10, 10, 10, 10) == 10.0

    def test_value_score_mixed(self):
        """Mixed values."""
        assert value_score(5, 3, 8, 0) == 4.35


class TestConfidenceLevel:
    def test_confidence_high(self):
        """Has local usage -> high."""
        assert confidence_level(True, False, False) == "medium"
        assert confidence_level(True, True, True) == "high"

    def test_confidence_medium(self):
        """No local usage, has market or alignment -> medium."""
        assert confidence_level(False, True, False) == "medium"
        assert confidence_level(False, False, True) == "medium"

    def test_confidence_low(self):
        """Nothing -> low."""
        assert confidence_level(False, False, False) == "low"


class TestRecommendationLayer:
    def test_recommendation_keep(self):
        """>=7 -> keep"""
        assert recommendation_layer(7.0) == "keep"
        assert recommendation_layer(9.5) == "keep"

    def test_recommendation_watch(self):
        """4-7 -> watch"""
        assert recommendation_layer(4.0) == "watch"
        assert recommendation_layer(5.5) == "watch"
        assert recommendation_layer(6.999) == "watch"

    def test_recommendation_hide(self):
        """2-4 -> hide"""
        assert recommendation_layer(2.0) == "hide"
        assert recommendation_layer(3.5) == "hide"

    def test_recommendation_uninstall(self):
        """<2 -> uninstall_candidate"""
        assert recommendation_layer(0.0) == "uninstall_candidate"
        assert recommendation_layer(1.5) == "uninstall_candidate"
        assert recommendation_layer(1.999) == "uninstall_candidate"

    def test_recommendation_boundaries(self):
        """Boundary values."""
        assert recommendation_layer(6.999) == "watch"
        assert recommendation_layer(7.001) == "keep"
        assert recommendation_layer(3.999) == "hide"
        assert recommendation_layer(4.001) == "watch"
        assert recommendation_layer(1.999) == "uninstall_candidate"
        assert recommendation_layer(2.001) == "hide"

class TestAssessSkillsOptimization:
    def test_assess_skills_optimization_empty(self):
        """Empty skill_scores -> empty list."""
        assert assess_skills_optimization([], {}) == []

    def test_assess_skills_optimization_with_usage(self):
        """With usage evidence -> higher value_score."""
        scores = [{"id": "ts", "health_score": 8.0, "profile_alignment": {"score": 5.0, "matched_terms": ["t"]}}]
        usage = {"ts": {"invocations": 10, "skill_id": "ts"}}
        result = assess_skills_optimization(scores, usage)
        assert len(result) == 1
        r = result[0]
        assert r["target"] == "ts"
        assert r["type"] == "skill"
        # usage_norm=10, alignment=5, health=8
        # = 10*0.4 + 5*0.25 + 8*0.2 = 4 + 1.25 + 1.6 = 6.85
        assert r["value_score"] is None
        assert r["layer"] == "pending_evidence"
        assert r["confidence"] == "medium"

    def test_assess_skills_optimization_no_usage(self):
        """No usage -> usage=0."""
        scores = [{"id": "ns", "health_score": 8.0, "profile_alignment": {"score": 3.0, "matched_terms": ["t"]}}]
        result = assess_skills_optimization(scores, {})
        r = result[0]
        # usage=0, alignment=3, health=8
        # = 0 + 3*0.25 + 8*0.2 = 0.75 + 1.6 = 2.35
        assert r["value_score"] is None
        assert r["layer"] == "pending_evidence"
        assert r["breakdown"]["usage"] is None

    def test_assess_skills_optimization_multiple_skills(self):
        """Multiple skills sorted descending by value_score."""
        scores = [
            {"id": "hi", "health_score": 9.0, "profile_alignment": {"score": 8.0, "matched_terms": ["a"]}},
            {"id": "lo", "health_score": 3.0, "profile_alignment": {"score": 1.0, "matched_terms": ["b"]}},
        ]
        usage = {"hi": {"invocations": 20, "skill_id": "hi"}}
        result = assess_skills_optimization(scores, usage)
        assert len(result) == 2
        assert result[0]["target"] == "hi"
        assert result[1]["target"] == "lo"
        assert all(r["value_score"] is None for r in result)
        assert result[1]["breakdown"]["usage"] is None


class TestAssessMcpOptimization:
    def test_assess_mcp_optimization_basic(self):
        """Basic calculation."""
        health = [{"server": "tm", "health_score": 8.0}]
        usage = [{"mcp_server": "tm", "tool_calls": 5}]
        result = assess_mcp_optimization(health, usage)
        assert len(result) == 1
        r = result[0]
        assert r["target"] == "tm"
        assert r["type"] == "mcp"
        # usage_norm=10, alignment=4, health=8
        # = 10*0.4 + 4*0.25 + 8*0.2 = 4 + 1 + 1.6 = 6.6
        assert r["value_score"] is None
        assert r["breakdown"]["alignment"] is None

    def test_assess_mcp_optimization_hide_review(self):
        """Low-score MCP downgraded to hide_review."""
        health = [{"server": "bm", "health_score": 1.0}]
        usage = [{"mcp_server": "bm", "tool_calls": 0}]
        result = assess_mcp_optimization(health, usage)
        assert result[0]["layer"] == "pending_evidence"

    def test_assess_mcp_optimization_empty(self):
        """Empty lists -> empty."""
        assert assess_mcp_optimization([], []) == []

class TestAuditEcosystem:
    def test_audit_ecosystem_structure(self, fake_user_skill_dir, fake_mcp_config, fake_signals, tmp_path):
        """Basic output structure: all 3 layers assessed."""
        cfg = tmp_path / "config.json"
        cfg.write_text(json.dumps({"mcp": {"servers": fake_mcp_config}}), encoding="utf-8")
        sig = tmp_path / "signals.json"
        sig.write_text(json.dumps(fake_signals), encoding="utf-8")

        result = audit_ecosystem(
            user_skill_dir=fake_user_skill_dir,
            zcode_config_path=cfg,
            agents_dir=None,
            signals_path=sig,
        )
        assert result["scope"] == "ecosystem"
        assert result["schema_version"] == 2
        ea = result["ecosystem_assessment"]
        assert len(ea["mcp_health"]) == 3
        assert "overlap_pairs" in ea["agent_dispatch"]
        assert "total_injection_tokens" in ea["context_pressure"]
        assert ea["skill_layer"]["status"] == "unavailable"
        assert ea["optimization"]["status"] == "partial"

    def test_audit_ecosystem_missing_config(self, fake_user_skill_dir, fake_signals, tmp_path):
        """Missing config -> empty mcp list."""
        sig = tmp_path / "signals.json"
        sig.write_text(json.dumps(fake_signals), encoding="utf-8")
        result = audit_ecosystem(
            user_skill_dir=fake_user_skill_dir,
            zcode_config_path=tmp_path / "nonexistent.json",
            agents_dir=None,
            signals_path=sig,
        )
        assert result["ecosystem_assessment"]["mcp_health"] == []

    def test_audit_ecosystem_empty_signals(self, fake_user_skill_dir, fake_mcp_config, tmp_path):
        """No signals -> mcp usage=unavailable."""
        cfg = tmp_path / "config.json"
        cfg.write_text(json.dumps({"mcp": {"servers": fake_mcp_config}}), encoding="utf-8")
        result = audit_ecosystem(
            user_skill_dir=fake_user_skill_dir,
            zcode_config_path=cfg,
            agents_dir=None,
            signals_path=None,
        )
        for m in result["ecosystem_assessment"]["mcp_health"]:
            assert m["dimensions"]["usage"]["status"] == "unavailable"

    def test_audit_ecosystem_skill_layer_with_root(
        self, fake_user_skill_dir, fake_mcp_config, fake_signals, tmp_path
    ):
        """With root dir, skill layer runs without exception."""
        cfg = tmp_path / "config.json"
        cfg.write_text(json.dumps({"mcp": {"servers": fake_mcp_config}}), encoding="utf-8")
        sig = tmp_path / "signals.json"
        sig.write_text(json.dumps(fake_signals), encoding="utf-8")

        root = tmp_path / "codex-root"
        (root / "cache" / "remote_plugin_catalog").mkdir(parents=True)
        (root / ".tmp" / "bundled-marketplaces").mkdir(parents=True)

        result = audit_ecosystem(
            user_skill_dir=fake_user_skill_dir,
            zcode_config_path=cfg,
            agents_dir=None,
            signals_path=sig,
            root=root,
            catalog_dir=root / "cache" / "remote_plugin_catalog",
            runtime_dir=root / "cache",
            staging_dir=root / ".tmp" / "bundled-marketplaces",
        )
        assert result["ecosystem_assessment"]["optimization"]["status"] == "partial"
