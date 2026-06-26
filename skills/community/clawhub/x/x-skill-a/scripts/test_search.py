import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).with_name("search.py")
SPEC = importlib.util.spec_from_file_location("search", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TestParseArgs:
    def test_basic_query(self):
        opts = MODULE.parse_args(["prog", "what", "is", "openclaw"])
        assert opts["query"] == ["what", "is", "openclaw"]

    def test_handles_single(self):
        opts = MODULE.parse_args(["prog", "--handles", "jaaneek", "grok updates"])
        assert opts["handles"] == ["jaaneek"]
        assert opts["query"] == ["grok updates"]

    def test_handles_multiple(self):
        opts = MODULE.parse_args(["prog", "--handles", "jaaneek,OpenClaw,xaboratory", "AI news"])
        assert opts["handles"] == ["jaaneek", "OpenClaw", "xaboratory"]

    def test_exclude(self):
        opts = MODULE.parse_args(["prog", "--exclude", "spambot,crypto_shill", "trending AI"])
        assert opts["exclude"] == ["spambot", "crypto_shill"]

    def test_date_range(self):
        opts = MODULE.parse_args(["prog", "--from", "2026-03-01", "--to", "2026-03-20", "xAI releases"])
        assert opts["from_date"] == "2026-03-01"
        assert opts["to_date"] == "2026-03-20"

    def test_images_and_video_flags(self):
        opts = MODULE.parse_args(["prog", "--images", "--video", "product demos"])
        assert opts["images"] is True
        assert opts["video"] is True

    def test_at_prefix_stripped(self):
        opts = MODULE.parse_args(["prog", "--handles", "@jaaneek,@OpenClaw", "latest posts"])
        assert opts["handles"] == ["jaaneek", "OpenClaw"]

    def test_equals_syntax(self):
        opts = MODULE.parse_args(["prog", "--handles=jaaneek", "--from=2026-03-01", "grok"])
        assert opts["handles"] == ["jaaneek"]
        assert opts["from_date"] == "2026-03-01"

    def test_double_dash_stops_flag_parsing(self):
        opts = MODULE.parse_args(["prog", "--handles", "jaaneek", "--", "--images", "not a flag"])
        assert opts["handles"] == ["jaaneek"]
        assert opts["images"] is False
        assert opts["query"] == ["--images", "not a flag"]

    def test_empty_handles_after_comma_filter(self):
        opts = MODULE.parse_args(["prog", "--handles", ",,", "query"])
        assert opts["handles"] == []

    def test_query_before_flags(self):
        opts = MODULE.parse_args(["prog", "grok news", "--handles", "jaaneek"])
        assert opts["handles"] == ["jaaneek"]
        assert opts["query"] == ["grok news"]

    def test_trailing_commas_in_handles(self):
        opts = MODULE.parse_args(["prog", "--handles", ",jaaneek,,OpenClaw,", "query"])
        assert opts["handles"] == ["jaaneek", "OpenClaw"]

    def test_help_flag(self):
        with pytest.raises(SystemExit) as exc:
            MODULE.parse_args(["prog", "--help"])
        assert exc.value.code == 0

    def test_no_args(self):
        with pytest.raises(SystemExit) as exc:
            MODULE.parse_args(["prog"])
        assert exc.value.code == 1

    def test_unknown_flag_rejected(self):
        with pytest.raises(SystemExit):
            MODULE.parse_args(["prog", "--verbose", "query"])

    def test_flag_missing_value(self):
        with pytest.raises(SystemExit):
            MODULE.parse_args(["prog", "query", "--handles"])


class TestValidate:
    def _opts(self, **kw):
        base = {"handles": None, "exclude": None, "from_date": None, "to_date": None}
        base.update(kw)
        return base

    def test_valid_handles(self):
        MODULE.validate(self._opts(handles=["jaaneek", "OpenClaw"]))

    def test_valid_dates(self):
        MODULE.validate(self._opts(from_date="2026-01-01", to_date="2026-03-20"))

    def test_handles_and_exclude_conflict(self):
        with pytest.raises(SystemExit):
            MODULE.validate(self._opts(handles=["jaaneek"], exclude=["spambot"]))

    def test_empty_handles_rejected(self):
        with pytest.raises(SystemExit):
            MODULE.validate(self._opts(handles=[]))

    def test_empty_exclude_rejected(self):
        with pytest.raises(SystemExit):
            MODULE.validate(self._opts(exclude=[]))

    def test_handle_with_space_rejected(self):
        with pytest.raises(SystemExit):
            MODULE.validate(self._opts(handles=["jan eek"]))

    def test_handle_too_long_rejected(self):
        with pytest.raises(SystemExit):
            MODULE.validate(self._opts(handles=["a" * 16]))

    def test_handle_15_chars_accepted(self):
        MODULE.validate(self._opts(handles=["a" * 15]))

    def test_over_ten_handles_rejected(self):
        with pytest.raises(SystemExit):
            MODULE.validate(self._opts(handles=[f"user{i}" for i in range(11)]))

    def test_exactly_ten_handles_accepted(self):
        MODULE.validate(self._opts(handles=[f"user{i}" for i in range(10)]))

    def test_bad_date_format_rejected(self):
        with pytest.raises(SystemExit):
            MODULE.validate(self._opts(from_date="March 1st"))

    def test_impossible_date_rejected(self):
        with pytest.raises(SystemExit):
            MODULE.validate(self._opts(from_date="2026-02-30"))

    def test_inverted_date_range_rejected(self):
        with pytest.raises(SystemExit):
            MODULE.validate(self._opts(from_date="2026-03-20", to_date="2026-01-01"))

    def test_same_date_accepted(self):
        MODULE.validate(self._opts(from_date="2026-03-20", to_date="2026-03-20"))

    def test_unicode_handle_rejected(self):
        with pytest.raises(SystemExit):
            MODULE.validate(self._opts(handles=["日本語"]))


class TestBuildToolConfig:
    def test_no_options(self):
        cfg = MODULE.build_tool_config({
            "handles": None, "exclude": None,
            "from_date": None, "to_date": None,
            "images": False, "video": False,
        })
        assert cfg == {"type": "x_search"}

    def test_handles_only(self):
        cfg = MODULE.build_tool_config({
            "handles": ["jaaneek"], "exclude": None,
            "from_date": None, "to_date": None,
            "images": False, "video": False,
        })
        assert cfg == {"type": "x_search", "allowed_x_handles": ["jaaneek"]}

    def test_exclude_only(self):
        cfg = MODULE.build_tool_config({
            "handles": None, "exclude": ["spambot"],
            "from_date": None, "to_date": None,
            "images": False, "video": False,
        })
        assert cfg == {"type": "x_search", "excluded_x_handles": ["spambot"]}

    def test_all_options(self):
        cfg = MODULE.build_tool_config({
            "handles": ["jaaneek", "OpenClaw"], "exclude": None,
            "from_date": "2026-03-01", "to_date": "2026-03-20",
            "images": True, "video": True,
        })
        assert cfg["type"] == "x_search"
        assert cfg["allowed_x_handles"] == ["jaaneek", "OpenClaw"]
        assert cfg["from_date"] == "2026-03-01"
        assert cfg["to_date"] == "2026-03-20"
        assert cfg["enable_image_understanding"] is True
        assert cfg["enable_video_understanding"] is True


class TestFormatResponse:
    def test_completed_with_citations(self):
        data = {
            "status": "completed",
            "output": [{"type": "message", "content": [{"type": "output_text", "text": "jaaneek posted about AI agents", "annotations": [
                {"type": "url_citation", "url": "https://x.com/jaaneek/status/123", "title": "jaaneek's post"},
            ]}]}],
            "usage": {"input_tokens": 500, "output_tokens": 100, "server_side_tool_usage_details": {"x_search_calls": 3}},
        }
        r = MODULE.format_response(data, "jaaneek AI")
        assert r["status"] == "completed"
        assert r["query"] == "jaaneek AI"
        assert "jaaneek" in r["text"]
        assert r["citations"][0]["url"] == "https://x.com/jaaneek/status/123"
        assert r["searches"] == 3
        assert r["tokens"]["input"] == 500

    def test_empty_response(self):
        r = MODULE.format_response({}, "openclaw skills")
        assert r["status"] == "unknown"
        assert r["text"] == ""
        assert r["citations"] == []
        assert r["searches"] == 0

    def test_malformed_output_types(self):
        r = MODULE.format_response({"status": "completed", "output": "not a list", "usage": 42}, "test")
        assert r["status"] == "completed"
        assert r["text"] == ""
        assert r["tokens"] == {"input": 0, "output": 0}

    def test_malformed_content_type(self):
        r = MODULE.format_response({"status": "completed", "output": [{"type": "message", "content": "bad"}], "usage": {}}, "test")
        assert r["text"] == ""

    def test_malformed_annotations_type(self):
        data = {"status": "completed", "output": [{"type": "message", "content": [{"text": "hi", "annotations": "bad"}]}], "usage": {}}
        r = MODULE.format_response(data, "test")
        assert r["text"] == "hi"
        assert r["citations"] == []

    def test_citations_without_url_filtered(self):
        data = {
            "status": "completed",
            "output": [{"type": "message", "content": [{"type": "output_text", "text": "results", "annotations": [
                {"type": "url_citation", "url": "https://x.com/jaaneek/status/456", "title": "valid"},
                {"type": "url_citation"},
                {"type": "url_citation", "url": "", "title": "empty url"},
            ]}]}],
            "usage": {},
        }
        r = MODULE.format_response(data, "test")
        assert len(r["citations"]) == 1
        assert r["citations"][0]["text"] == "valid"

    def test_failed_status_includes_error(self):
        data = {"status": "failed", "error": {"message": "rate limit exceeded"}, "output": [], "usage": {}}
        r = MODULE.format_response(data, "trending")
        assert r["status"] == "failed"
        assert "rate limit exceeded" in r["text"]

    def test_failed_status_with_string_error(self):
        data = {"status": "failed", "error": "something broke", "output": [], "usage": {}}
        r = MODULE.format_response(data, "test")
        assert "something broke" in r["text"]

    def test_multiple_content_blocks_joined(self):
        data = {
            "status": "completed",
            "output": [{"type": "message", "content": [
                {"type": "output_text", "text": "OpenClaw update:", "annotations": [
                    {"type": "url_citation", "url": "https://x.com/OpenClaw/status/1", "title": "post 1"},
                ]},
                {"type": "output_text", "text": "jaaneek contributed x-search skill", "annotations": [
                    {"type": "url_citation", "url": "https://x.com/jaaneek/status/2", "title": "post 2"},
                ]},
            ]}],
            "usage": {},
        }
        r = MODULE.format_response(data, "openclaw skills")
        assert "OpenClaw update:" in r["text"]
        assert "jaaneek contributed" in r["text"]
        assert "\n\n" in r["text"]
        assert len(r["citations"]) == 2

    def test_no_message_in_output(self):
        data = {
            "status": "completed",
            "output": [{"type": "reasoning", "status": "completed"}],
            "usage": {"input_tokens": 50, "output_tokens": 0},
        }
        r = MODULE.format_response(data, "test")
        assert r["text"] == ""
        assert r["citations"] == []
