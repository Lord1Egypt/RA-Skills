"""Layer 1b: Unit tests for QuorumConfig and config loading."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from quorum.config import VALID_CRITICS, VALID_DEPTHS, QuorumConfig, load_config


# ── QuorumConfig creation ────────────────────────────────────────────────────


class TestQuorumConfigCreation:
    def test_minimal_valid(self):
        cfg = QuorumConfig(
            critics=["correctness"],
            model_tier1="anthropic/claude-opus-4-6",
            model_tier2="anthropic/claude-sonnet-4-6",
        )
        assert cfg.depth_profile == "standard"
        assert cfg.temperature == 0.1
        assert cfg.max_tokens == 4096

    def test_full_config(self):
        cfg = QuorumConfig(
            critics=["correctness", "security", "completeness", "code_hygiene"],
            model_tier1="anthropic/claude-opus-4-6",
            model_tier2="anthropic/claude-sonnet-4-6",
            depth_profile="thorough",
            temperature=0.05,
            max_tokens=8192,
            enable_prescreen=True,
            max_fix_loops=2,
        )
        assert cfg.max_fix_loops == 2
        assert cfg.enable_prescreen is True


# ── Validators ───────────────────────────────────────────────────────────────


class TestQuorumConfigValidation:
    def test_invalid_critic_rejected(self):
        with pytest.raises(ValidationError, match="Unknown critics"):
            QuorumConfig(
                critics=["nonexistent_critic"],
                model_tier1="m1",
                model_tier2="m2",
            )

    def test_empty_critics_rejected(self):
        with pytest.raises(ValidationError, match="At least one critic"):
            QuorumConfig(critics=[], model_tier1="m1", model_tier2="m2")

    def test_invalid_depth_rejected(self):
        with pytest.raises(ValidationError, match="depth_profile"):
            QuorumConfig(
                critics=["correctness"],
                model_tier1="m1",
                model_tier2="m2",
                depth_profile="invalid",
            )

    def test_valid_depths(self):
        for depth in VALID_DEPTHS:
            cfg = QuorumConfig(
                critics=["correctness"],
                model_tier1="m1",
                model_tier2="m2",
                depth_profile=depth,
            )
            assert cfg.depth_profile == depth

    def test_temperature_bounds(self):
        with pytest.raises(ValidationError):
            QuorumConfig(
                critics=["correctness"],
                model_tier1="m1",
                model_tier2="m2",
                temperature=3.0,
            )
        with pytest.raises(ValidationError):
            QuorumConfig(
                critics=["correctness"],
                model_tier1="m1",
                model_tier2="m2",
                temperature=-0.1,
            )

    def test_max_tokens_minimum(self):
        with pytest.raises(ValidationError):
            QuorumConfig(
                critics=["correctness"],
                model_tier1="m1",
                model_tier2="m2",
                max_tokens=100,
            )

    def test_max_fix_loops_bounds(self):
        with pytest.raises(ValidationError):
            QuorumConfig(
                critics=["correctness"],
                model_tier1="m1",
                model_tier2="m2",
                max_fix_loops=5,
            )


# ── from_yaml ────────────────────────────────────────────────────────────────


class TestQuorumConfigFromYAML:
    def test_load_from_yaml(self, tmp_path):
        config_data = {
            "critics": ["correctness", "completeness"],
            "model_tier1": "anthropic/claude-opus-4-6",
            "model_tier2": "anthropic/claude-sonnet-4-6",
            "depth_profile": "quick",
        }
        path = tmp_path / "test-config.yaml"
        with open(path, "w") as f:
            yaml.dump(config_data, f)

        cfg = QuorumConfig.from_yaml(path)
        assert cfg.critics == ["correctness", "completeness"]
        assert cfg.depth_profile == "quick"

    def test_env_var_api_key_resolution(self, tmp_path, monkeypatch):
        monkeypatch.setenv("TEST_API_KEY", "sk-test-123")
        config_data = {
            "critics": ["correctness"],
            "model_tier1": "m1",
            "model_tier2": "m2",
            "api_keys": {"anthropic": "$TEST_API_KEY"},
        }
        path = tmp_path / "config.yaml"
        with open(path, "w") as f:
            yaml.dump(config_data, f)

        cfg = QuorumConfig.from_yaml(path)
        assert cfg.api_keys["anthropic"] == "sk-test-123"

    def test_env_var_missing_resolves_empty(self, tmp_path, monkeypatch):
        monkeypatch.delenv("MISSING_KEY", raising=False)
        config_data = {
            "critics": ["correctness"],
            "model_tier1": "m1",
            "model_tier2": "m2",
            "api_keys": {"key": "$MISSING_KEY"},
        }
        path = tmp_path / "config.yaml"
        with open(path, "w") as f:
            yaml.dump(config_data, f)

        cfg = QuorumConfig.from_yaml(path)
        assert cfg.api_keys["key"] == ""


# ── with_overrides ───────────────────────────────────────────────────────────


class TestQuorumConfigOverrides:
    def test_override_depth(self):
        cfg = QuorumConfig(
            critics=["correctness"],
            model_tier1="m1",
            model_tier2="m2",
            depth_profile="quick",
        )
        cfg2 = cfg.with_overrides(depth_profile="thorough")
        assert cfg2.depth_profile == "thorough"
        assert cfg.depth_profile == "quick"  # original unchanged

    def test_override_ignores_none(self):
        cfg = QuorumConfig(
            critics=["correctness"],
            model_tier1="m1",
            model_tier2="m2",
        )
        cfg2 = cfg.with_overrides(depth_profile=None)
        assert cfg2.depth_profile == cfg.depth_profile

    def test_override_temperature(self):
        cfg = QuorumConfig(
            critics=["correctness"],
            model_tier1="m1",
            model_tier2="m2",
        )
        cfg2 = cfg.with_overrides(temperature=0.5)
        assert cfg2.temperature == 0.5


# ── load_config ──────────────────────────────────────────────────────────────


class TestLoadConfig:
    def test_load_from_explicit_path(self, tmp_path):
        config_data = {
            "critics": ["correctness"],
            "model_tier1": "m1",
            "model_tier2": "m2",
            "depth_profile": "quick",
        }
        path = tmp_path / "cfg.yaml"
        with open(path, "w") as f:
            yaml.dump(config_data, f)

        cfg = load_config(config_path=path)
        assert cfg.critics == ["correctness"]

    def test_missing_config_raises(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        with pytest.raises(FileNotFoundError, match="No config found"):
            load_config(depth="nonexistent_depth_profile")


# ── EnvVar handling ──────────────────────────────────────────────────────────


class TestEnvVarHandling:
    def test_api_key_from_env(self, tmp_path, monkeypatch):
        monkeypatch.setenv("MY_KEY", "secret-value")
        config_data = {
            "critics": ["correctness"],
            "model_tier1": "m1",
            "model_tier2": "m2",
            "api_keys": {"provider": "$MY_KEY"},
        }
        path = tmp_path / "config.yaml"
        with open(path, "w") as f:
            yaml.dump(config_data, f)

        cfg = QuorumConfig.from_yaml(path)
        assert cfg.api_keys["provider"] == "secret-value"

    def test_literal_key_preserved(self, tmp_path):
        config_data = {
            "critics": ["correctness"],
            "model_tier1": "m1",
            "model_tier2": "m2",
            "api_keys": {"provider": "literal-key-value"},
        }
        path = tmp_path / "config.yaml"
        with open(path, "w") as f:
            yaml.dump(config_data, f)

        cfg = QuorumConfig.from_yaml(path)
        assert cfg.api_keys["provider"] == "literal-key-value"
