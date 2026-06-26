from __future__ import annotations

import pytest

from zim.airports import normalize_airport


def test_normalize_city_names() -> None:
    assert normalize_airport("New York") == "JFK"
    assert normalize_airport("London") == "LHR"
    assert normalize_airport("Dubai") == "DXB"
    assert normalize_airport("Copenhagen") == "CPH"
    assert normalize_airport("Singapore") == "SIN"


def test_normalize_aliases_case_insensitive() -> None:
    assert normalize_airport("nyc") == "JFK"
    assert normalize_airport("los angeles") == "LAX"
    assert normalize_airport("washington dc") == "IAD"
    assert normalize_airport("bombay") == "BOM"
    assert normalize_airport("saigon") == "SGN"


def test_passes_through_iata_code() -> None:
    assert normalize_airport("jfk") == "JFK"
    assert normalize_airport("DXB") == "DXB"


def test_unknown_city_raises() -> None:
    with pytest.raises(ValueError):
        normalize_airport("Atlantis")
