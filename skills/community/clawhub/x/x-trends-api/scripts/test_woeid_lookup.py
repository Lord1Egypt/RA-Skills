import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).with_name("woeid_lookup.py")
SPEC = importlib.util.spec_from_file_location("woeid_lookup", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


SAMPLE_PLACES = [
    {"name": "Worldwide", "woeid": 1, "country": "", "countryCode": None, "placeType": {"code": 19, "name": "Supername"}},
    {"name": "Tokyo", "woeid": 1118370, "country": "Japan", "countryCode": "JP", "placeType": {"code": 7, "name": "Town"}},
    {"name": "New York", "woeid": 2459115, "country": "United States", "countryCode": "US", "placeType": {"code": 7, "name": "Town"}},
    {"name": "Jakarta", "woeid": 1047378, "country": "Indonesia", "countryCode": "ID", "placeType": {"code": 7, "name": "Town"}},
    {"name": "Japan", "woeid": 23424856, "country": "Japan", "countryCode": "JP", "placeType": {"code": 12, "name": "Country"}},
]


class TestSearch:
    def test_exact_name(self):
        results = MODULE.search(SAMPLE_PLACES, "Tokyo")
        assert len(results) == 1
        assert results[0]["woeid"] == 1118370

    def test_case_insensitive(self):
        results = MODULE.search(SAMPLE_PLACES, "tokyo")
        assert len(results) == 1
        assert results[0]["woeid"] == 1118370

    def test_partial_match(self):
        results = MODULE.search(SAMPLE_PLACES, "New")
        assert any(r["woeid"] == 2459115 for r in results)

    def test_country_match(self):
        results = MODULE.search(SAMPLE_PLACES, "Japan")
        woeids = {r["woeid"] for r in results}
        assert 1118370 in woeids  # Tokyo (country=Japan)
        assert 23424856 in woeids  # Japan (name=Japan)

    def test_no_match(self):
        results = MODULE.search(SAMPLE_PLACES, "Atlantis")
        assert results == []

    def test_result_fields(self):
        results = MODULE.search(SAMPLE_PLACES, "Jakarta")
        assert len(results) == 1
        r = results[0]
        assert r["woeid"] == 1047378
        assert r["name"] == "Jakarta"
        assert r["country"] == "Indonesia"
        assert r["countryCode"] == "ID"
        assert r["placeType"] == "Town"

    def test_skips_non_dict(self):
        places = [None, "bad", {"name": "Tokyo", "woeid": 1118370, "country": "Japan", "countryCode": "JP", "placeType": {"code": 7, "name": "Town"}}]
        results = MODULE.search(places, "Tokyo")
        assert len(results) == 1


class TestMain:
    def test_no_args(self):
        with pytest.raises(SystemExit) as exc:
            MODULE.main(["prog"])
        assert exc.value.code == 1

    def test_help(self):
        with pytest.raises(SystemExit) as exc:
            MODULE.main(["prog", "--help"])
        assert exc.value.code == 0
