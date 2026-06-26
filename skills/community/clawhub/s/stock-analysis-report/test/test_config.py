from __future__ import annotations

import pytest

from src.config import SkillConfig


class TestSkillConfig:
    def test_defaults_from_env(self, monkeypatch):
        monkeypatch.setenv("LLM_API_KEY", "test-key")
        monkeypatch.setenv("LLM_BASE_URL", "https://api.example.com/v1")
        monkeypatch.setenv("LLM_MODEL", "test-model")

        config = SkillConfig()
        assert config.llm_api_key == "test-key"
        assert config.llm_base_url == "https://api.example.com/v1"
        assert config.llm_model == "test-model"

    def test_validate_success(self, monkeypatch):
        monkeypatch.setenv("LLM_API_KEY", "test-key")
        monkeypatch.setenv("LLM_BASE_URL", "https://api.example.com/v1")
        monkeypatch.setenv("LLM_MODEL", "test-model")

        config = SkillConfig()
        errors = config.validate()
        assert errors == []

    def test_validate_missing_api_key(self, monkeypatch):
        monkeypatch.delenv("LLM_API_KEY", raising=False)
        monkeypatch.setenv("LLM_BASE_URL", "https://api.example.com/v1")
        monkeypatch.setenv("LLM_MODEL", "test-model")

        config = SkillConfig(llm_api_key="")
        errors = config.validate()
        assert len(errors) == 1
        assert "LLM_API_KEY" in errors[0]

    def test_validate_missing_base_url(self, monkeypatch):
        monkeypatch.setenv("LLM_API_KEY", "test-key")
        monkeypatch.delenv("LLM_BASE_URL", raising=False)
        monkeypatch.setenv("LLM_MODEL", "test-model")

        config = SkillConfig(llm_base_url="")
        errors = config.validate()
        assert len(errors) == 1
        assert "LLM_BASE_URL" in errors[0]

    def test_validate_missing_model(self, monkeypatch):
        monkeypatch.setenv("LLM_API_KEY", "test-key")
        monkeypatch.setenv("LLM_BASE_URL", "https://api.example.com/v1")
        monkeypatch.delenv("LLM_MODEL", raising=False)

        config = SkillConfig(llm_model="")
        errors = config.validate()
        assert len(errors) == 1
        assert "LLM_MODEL" in errors[0]

    def test_has_search_engine_true(self, monkeypatch):
        monkeypatch.setenv("SERPAPI_KEY", "some-key")

        config = SkillConfig(serpapi_key="some-key")
        assert config.has_search_engine is True

    def test_has_search_engine_false(self, monkeypatch):
        monkeypatch.delenv("SERPAPI_KEY", raising=False)
        monkeypatch.delenv("TAVILY_KEY", raising=False)
        monkeypatch.delenv("BRAVE_KEY", raising=False)
        monkeypatch.delenv("BOCHA_KEY", raising=False)

        config = SkillConfig(serpapi_key="", tavily_key="", brave_key="", bocha_key="")
        assert config.has_search_engine is False

    def test_optional_fields_defaults(self, monkeypatch):
        monkeypatch.delenv("MX_APIKEY", raising=False)
        monkeypatch.delenv("BIAS_THRESHOLD", raising=False)
        monkeypatch.delenv("NEWS_MAX_AGE_DAYS", raising=False)
        monkeypatch.delenv("ENABLE_CHIP", raising=False)

        config = SkillConfig()
        assert config.mx_apikey == ""
        assert config.bias_threshold == 5.0
        assert config.news_max_age_days == 3
        assert config.enable_chip is True
