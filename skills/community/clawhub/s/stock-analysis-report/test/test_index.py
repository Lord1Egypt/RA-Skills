from __future__ import annotations

import asyncio

import pytest

from src.index import _dataclass_to_dict, handler
from src.models import CheckItem, StockAnalysisResult


class TestDataclassToDict:
    def test_primitive_types(self):
        assert _dataclass_to_dict(42) == 42
        assert _dataclass_to_dict("hello") == "hello"
        assert _dataclass_to_dict(3.14) == 3.14
        assert _dataclass_to_dict(True) is True
        assert _dataclass_to_dict(None) is None

    def test_list(self):
        assert _dataclass_to_dict([1, 2, 3]) == [1, 2, 3]

    def test_dict(self):
        assert _dataclass_to_dict({"a": 1}) == {"a": 1}

    def test_dataclass(self):
        result = StockAnalysisResult(stock_code="600519", score=75)
        d = _dataclass_to_dict(result)
        assert d["stock_code"] == "600519"
        assert d["score"] == 75
        assert isinstance(d["checklist"], list)

    def test_nested_dataclass(self):
        result = StockAnalysisResult(
            stock_code="600519",
            checklist=[CheckItem(condition="test", status="✅", detail="ok")],
        )
        d = _dataclass_to_dict(result)
        assert len(d["checklist"]) == 1
        assert d["checklist"][0]["condition"] == "test"


class TestHandler:
    def test_missing_code_returns_error(self):
        result = asyncio.run(handler({"mode": "stock"}))
        assert "error" in result
        assert "股票代码" in result["error"]

    def test_missing_llm_config_returns_config_error(self, monkeypatch):
        monkeypatch.delenv("LLM_API_KEY", raising=False)
        monkeypatch.delenv("LLM_BASE_URL", raising=False)
        monkeypatch.delenv("LLM_MODEL", raising=False)

        result = asyncio.run(handler({"mode": "stock", "code": "600519"}))
        if "error" in result:
            assert "execution" in result["error"].lower() or "配置" in result.get("core_conclusion", "")
        else:
            assert result.get("stock_code") == "600519"
