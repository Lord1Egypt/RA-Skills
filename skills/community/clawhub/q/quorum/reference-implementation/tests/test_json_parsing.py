# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Tests for JSON parsing utilities and provider JSON handling.
Ensures robust parsing of LLM responses that may have markdown fences.
"""

import json
import pytest

from quorum.utils import extract_json_from_response
from quorum.providers.litellm_provider import LiteLLMProvider


class TestExtractJsonFromResponse:
    """Test the utility function for extracting JSON from various response formats."""

    def test_plain_json_object(self):
        """Plain JSON object should pass through unchanged."""
        json_str = '{"findings": [], "confidence": 0.5}'
        result = extract_json_from_response(json_str)
        assert result == json_str

    def test_plain_json_array(self):
        """Plain JSON array should pass through unchanged."""
        json_str = '[{"id": 1}, {"id": 2}]'
        result = extract_json_from_response(json_str)
        assert result == json_str

    def test_json_with_whitespace(self):
        """JSON with leading/trailing whitespace should be trimmed."""
        json_str = '   {"key": "value"}   '
        result = extract_json_from_response(json_str)
        assert result == '{"key": "value"}'

    def test_json_fences_basic(self):
        """Basic ```json fences should be stripped."""
        fenced = '```json\n{"findings": [], "confidence": 0.5}\n```'
        result = extract_json_from_response(fenced)
        assert result == '{"findings": [], "confidence": 0.5}'

    def test_json_fences_uppercase(self):
        """```JSON fences should be stripped."""
        fenced = '```JSON\n{"findings": [], "confidence": 0.5}\n```'
        result = extract_json_from_response(fenced)
        assert result == '{"findings": [], "confidence": 0.5}'

    def test_plain_fences(self):
        """Plain ``` fences should be stripped."""
        fenced = '```\n{"findings": [], "confidence": 0.5}\n```'
        result = extract_json_from_response(fenced)
        assert result == '{"findings": [], "confidence": 0.5}'

    def test_fences_with_trailing_newlines(self):
        """Fences with multiple trailing newlines should be handled."""
        fenced = '```json\n{"findings": []}\n\n\n```'
        result = extract_json_from_response(fenced)
        assert result == '{"findings": []}'

    def test_compact_fences(self):
        """Compact fences without newlines should be handled."""
        fenced = '```json{"findings": []}```'
        result = extract_json_from_response(fenced)
        assert result == '{"findings": []}'

    def test_nested_json_in_fences(self):
        """Complex nested JSON in fences should be extracted correctly."""
        nested = {
            "findings": [
                {
                    "severity": "HIGH",
                    "description": "Test finding",
                    "evidence": {"tool": "grep", "result": "match"}
                }
            ]
        }
        json_str = json.dumps(nested)
        fenced = f'```json\n{json_str}\n```'
        result = extract_json_from_response(fenced)
        assert result == json_str

    def test_json_with_nested_backticks_in_strings(self):
        """JSON containing backticks in string values should be handled."""
        json_with_backticks = '{"code": "```bash\\necho hello\\n```", "findings": []}'
        fenced = f'```json\n{json_with_backticks}\n```'
        result = extract_json_from_response(fenced)
        assert result == json_with_backticks

    def test_malformed_fences_fallback(self):
        """Malformed fences should fall back to original text."""
        malformed = '```json\n{"incomplete": true'
        result = extract_json_from_response(malformed)
        # Should try to extract, but in this case would fall back
        assert '{"incomplete": true' in result

    def test_empty_fences(self):
        """Empty fences should return empty string."""
        empty_fenced = '```json\n\n```'
        result = extract_json_from_response(empty_fenced)
        assert result == ''

    def test_whitespace_only_fences(self):
        """Fences with only whitespace should return empty string."""
        whitespace_fenced = '```json\n   \n  \n```'
        result = extract_json_from_response(whitespace_fenced)
        assert result == ''


class TestLiteLLMProviderJsonParsing:
    """Test the provider's JSON parsing with various response formats."""

    @pytest.fixture
    def provider(self):
        """Create a provider instance for testing."""
        return LiteLLMProvider()

    def test_parse_plain_json(self, provider):
        """Plain JSON should parse correctly."""
        json_str = '{"findings": [], "confidence": 0.5}'
        result = provider._parse_json(json_str, "test-model")
        assert result == {"findings": [], "confidence": 0.5}

    def test_parse_fenced_json(self, provider):
        """JSON wrapped in fences should parse correctly."""
        fenced = '```json\n{"findings": [], "confidence": 0.5}\n```'
        result = provider._parse_json(fenced, "test-model")
        assert result == {"findings": [], "confidence": 0.5}

    def test_parse_uppercase_fences(self, provider):
        """JSON with uppercase fence markers should parse correctly."""
        fenced = '```JSON\n{"findings": [], "confidence": 0.5}\n```'
        result = provider._parse_json(fenced, "test-model")
        assert result == {"findings": [], "confidence": 0.5}

    def test_parse_plain_fences(self, provider):
        """JSON with plain ``` fences should parse correctly."""
        fenced = '```\n{"findings": [], "confidence": 0.5}\n```'
        result = provider._parse_json(fenced, "test-model")
        assert result == {"findings": [], "confidence": 0.5}

    def test_parse_complex_findings(self, provider):
        """Complex findings structure should parse correctly."""
        findings_data = {
            "findings": [
                {
                    "severity": "CRITICAL",
                    "description": "SQL injection vulnerability",
                    "evidence_tool": "static-analysis",
                    "evidence_result": "Detected unsanitized user input",
                    "location": "line 42"
                }
            ]
        }
        json_str = json.dumps(findings_data)
        fenced = f'```json\n{json_str}\n```'
        result = provider._parse_json(fenced, "test-model")
        assert result == findings_data

    def test_parse_json_array(self, provider):
        """JSON arrays should be parsed correctly."""
        array_str = '[{"id": 1, "name": "test"}]'
        fenced = f'```json\n{array_str}\n```'
        result = provider._parse_json(fenced, "test-model")
        assert result == [{"id": 1, "name": "test"}]

    def test_parse_json_with_nested_backticks(self, provider):
        """JSON containing backticks in strings should parse correctly."""
        json_with_backticks = {
            "findings": [{
                "description": "Code snippet: ```python\nprint('hello')\n```",
                "evidence_result": "Found in function `get_data()`"
            }]
        }
        json_str = json.dumps(json_with_backticks)
        fenced = f'```json\n{json_str}\n```'
        result = provider._parse_json(fenced, "test-model")
        assert result == json_with_backticks

    def test_parse_multiline_json(self, provider):
        """Multiline JSON should parse correctly."""
        multiline = '''```json
{
  "findings": [
    {
      "severity": "HIGH",
      "description": "This is a long description that spans multiple lines and contains various details about the security issue found"
    }
  ],
  "confidence": 0.85
}
```'''
        result = provider._parse_json(multiline, "test-model")
        assert result["findings"][0]["severity"] == "HIGH"
        assert result["confidence"] == 0.85

    def test_parse_json_with_extra_text_before_fences(self, provider):
        """JSON with explanatory text before fences should extract correctly."""
        response_with_text = '''Here is the analysis result:

```json
{"findings": [{"severity": "MEDIUM", "description": "Issue found"}]}
```

The analysis is complete.'''
        result = provider._parse_json(response_with_text, "test-model")
        assert result["findings"][0]["severity"] == "MEDIUM"

    def test_parse_invalid_json_raises_error(self, provider):
        """Invalid JSON should raise ValueError with helpful message."""
        invalid_json = '```json\n{"invalid": json, missing quotes}\n```'
        with pytest.raises(ValueError) as exc_info:
            provider._parse_json(invalid_json, "test-model")

        error_msg = str(exc_info.value)
        assert "Could not parse JSON" in error_msg
        assert "test-model" in error_msg

    def test_parse_completely_invalid_response(self, provider):
        """Completely invalid response should raise ValueError."""
        invalid_response = "This is not JSON at all, just plain text."
        with pytest.raises(ValueError) as exc_info:
            provider._parse_json(invalid_response, "test-model")

        error_msg = str(exc_info.value)
        assert "Could not parse JSON" in error_msg
        assert "test-model" in error_msg

    def test_backward_compatibility_unfenced_json(self, provider):
        """Unfenced JSON should still work (backward compatibility)."""
        unfenced_json = '{"findings": [], "confidence": 1.0}'
        result = provider._parse_json(unfenced_json, "test-model")
        assert result == {"findings": [], "confidence": 1.0}