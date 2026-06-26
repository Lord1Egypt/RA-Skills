import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).with_name("trends.py")
SPEC = importlib.util.spec_from_file_location("trends", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TestParseArgs:
    def test_woeid_basic(self):
        opts = MODULE.parse_args(["prog", "--woeid", "1"])
        assert opts["woeid"] == "1"
        assert opts["max_trends"] is None

    def test_woeid_with_max(self):
        opts = MODULE.parse_args(["prog", "--woeid", "23424977", "--max", "10"])
        assert opts["woeid"] == "23424977"
        assert opts["max_trends"] == "10"

    def test_equals_syntax(self):
        opts = MODULE.parse_args(["prog", "--woeid=2459115", "--max=5"])
        assert opts["woeid"] == "2459115"
        assert opts["max_trends"] == "5"

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
            MODULE.parse_args(["prog", "--verbose"])

    def test_unexpected_positional_rejected(self):
        with pytest.raises(SystemExit):
            MODULE.parse_args(["prog", "--woeid", "1", "extra"])

    def test_flag_missing_value(self):
        with pytest.raises(SystemExit):
            MODULE.parse_args(["prog", "--woeid"])

    def test_max_missing_value(self):
        with pytest.raises(SystemExit):
            MODULE.parse_args(["prog", "--woeid", "1", "--max"])


class TestValidate:
    def _opts(self, **kw):
        base = {"woeid": None, "max_trends": None}
        base.update(kw)
        return base

    def test_valid_woeid(self):
        MODULE.validate(self._opts(woeid="1"))

    def test_valid_woeid_with_max(self):
        MODULE.validate(self._opts(woeid="23424977", max_trends="10"))

    def test_missing_woeid(self):
        with pytest.raises(SystemExit):
            MODULE.validate(self._opts())

    def test_non_numeric_woeid_rejected(self):
        with pytest.raises(SystemExit):
            MODULE.validate(self._opts(woeid="abc"))

    def test_zero_woeid_rejected(self):
        with pytest.raises(SystemExit):
            MODULE.validate(self._opts(woeid="0"))

    def test_non_numeric_max_rejected(self):
        with pytest.raises(SystemExit):
            MODULE.validate(self._opts(woeid="1", max_trends="abc"))

    def test_max_below_min_rejected(self):
        with pytest.raises(SystemExit):
            MODULE.validate(self._opts(woeid="1", max_trends="0"))

    def test_max_above_max_rejected(self):
        with pytest.raises(SystemExit):
            MODULE.validate(self._opts(woeid="1", max_trends="51"))

    def test_max_boundary_min_accepted(self):
        MODULE.validate(self._opts(woeid="1", max_trends="1"))

    def test_max_boundary_max_accepted(self):
        MODULE.validate(self._opts(woeid="1", max_trends="50"))


class TestBuildUrl:
    def test_woeid_default(self):
        url = MODULE.build_url({"woeid": "1", "max_trends": None})
        assert url == "https://api.x.com/2/trends/by/woeid/1?trend.fields=trend_name,tweet_count"

    def test_woeid_with_max(self):
        url = MODULE.build_url({"woeid": "23424977", "max_trends": "10"})
        assert "max_trends=10" in url
        assert "trend.fields=trend_name,tweet_count" in url


class TestFormatResponse:
    def test_trends(self):
        data = {
            "data": [
                {"trend_name": "#AI", "tweet_count": 150000},
                {"trend_name": "Python", "tweet_count": 80000},
            ]
        }
        r = MODULE.format_response(data)
        assert r["count"] == 2
        assert r["trends"][0]["trend_name"] == "#AI"
        assert r["trends"][0]["tweet_count"] == 150000

    def test_empty_response(self):
        r = MODULE.format_response({})
        assert r["count"] == 0
        assert r["trends"] == []
        assert "errors" not in r

    def test_malformed_data_not_list(self):
        r = MODULE.format_response({"data": "not a list"})
        assert r["count"] == 0
        assert r["trends"] == []

    def test_malformed_trend_entries(self):
        data = {"data": ["not a dict", 42, None, {"trend_name": "valid"}]}
        r = MODULE.format_response(data)
        assert r["count"] == 1
        assert r["trends"][0]["trend_name"] == "valid"

    def test_errors_included(self):
        data = {
            "data": [],
            "errors": [{"title": "Not Found", "detail": "WOEID not found"}],
        }
        r = MODULE.format_response(data)
        assert r["errors"] == ["WOEID not found"]

    def test_errors_title_fallback(self):
        data = {"data": [], "errors": [{"title": "Forbidden"}]}
        r = MODULE.format_response(data)
        assert r["errors"] == ["Forbidden"]

    def test_malformed_errors_not_list(self):
        r = MODULE.format_response({"data": [], "errors": "bad"})
        assert "errors" not in r

    def test_trend_without_name_still_included(self):
        data = {"data": [{"tweet_count": 5000}]}
        r = MODULE.format_response(data)
        assert r["count"] == 1
        assert r["trends"][0] == {"tweet_count": 5000}

    def test_empty_trend_entry_skipped(self):
        data = {"data": [{}]}
        r = MODULE.format_response(data)
        assert r["count"] == 0
        assert r["trends"] == []
