"""Tests for vercel_insights/odata.py."""

from __future__ import annotations

import re

import pytest

from vercel_insights import ConfigError
from vercel_insights import odata as od
from vercel_insights.webanalytics import PLAIN_DIMENSIONS


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("US", "'US'"),
        ("O'Brien", "'O''Brien'"),
        ("it's a 'test'", "'it''s a ''test'''"),
        ("", "''"),
        ("/blog/[slug]", "'/blog/[slug]'"),
    ],
)
def test_quote_odata_doubles_embedded_single_quotes(value: str, expected: str) -> None:
    assert od.quote_odata(value) == expected


@pytest.mark.parametrize(
    ("dimension", "value", "expected"),
    [
        ("country", "US", "country eq 'US'"),
        ("requestPath", "/pricing", "requestPath eq '/pricing'"),
        ("requestPath", "O'Brien", "requestPath eq 'O''Brien'"),
        ("country", "US,DE", "country in ('US', 'DE')"),
        ("country", " US , DE ", "country in ('US', 'DE')"),
        ("country", "US,DE,FR", "country in ('US', 'DE', 'FR')"),
        ("country", "US,,DE", "country in ('US', 'DE')"),
        ("country", "US,", "country eq 'US'"),
        ("browserName", "O'Neill,Safari", "browserName in ('O''Neill', 'Safari')"),
    ],
)
def test_build_clause_uses_eq_for_one_value_and_in_for_a_list(
    dimension: str, value: str, expected: str
) -> None:
    assert od.build_clause(dimension, value) == expected


@pytest.mark.parametrize("value", ["", "   ", ",", ",,", " , "])
def test_build_clause_rejects_an_empty_filter_value(value: str) -> None:
    with pytest.raises(ConfigError) as excinfo:
        od.build_clause("country", value)
    assert "is empty" in str(excinfo.value)


@pytest.mark.parametrize(
    ("clauses", "expected"),
    [
        ([], None),
        ([""], None),
        (["   "], None),
        (["country eq 'US'"], "country eq 'US'"),
        (
            ["country eq 'US'", "requestPath eq '/pricing'"],
            "country eq 'US' and requestPath eq '/pricing'",
        ),
        (
            ["country eq 'US' or country eq 'DE'", "requestPath eq '/pricing'"],
            "(country eq 'US' or country eq 'DE') and requestPath eq '/pricing'",
        ),
        (
            ["country eq 'US'", "not (deviceType eq 'bot' or deviceType eq 'crawler')"],
            "country eq 'US' and not (deviceType eq 'bot' or deviceType eq 'crawler')",
        ),
        (["country eq 'or'"], "country eq 'or'"),
        (
            ["referrerHostname eq 'editor.example'"],
            "referrerHostname eq 'editor.example'",
        ),
    ],
)
def test_combine_filters_joins_with_and_and_parenthesizes_top_level_or(
    clauses: list[str], expected: str | None
) -> None:
    assert od.combine_filters(clauses) == expected


def test_combine_filters_only_parenthesizes_the_clause_that_needs_it() -> None:
    combined = od.combine_filters(
        ["a eq 'x' or a eq 'y'", "b eq 'z'", "c eq 'w' or c eq 'v'"]
    )
    assert combined == "(a eq 'x' or a eq 'y') and b eq 'z' and (c eq 'w' or c eq 'v')"


@pytest.mark.parametrize(
    "value", ["US", "US,DE", "O'Brien", "12", "true", "/a/b", "a or b"]
)
def test_no_comparison_operator_is_ever_emitted(value: str) -> None:
    for dimension in PLAIN_DIMENSIONS:
        clause = od.build_clause(dimension, value)
        assert re.search(r"(^|\s)(gt|lt|ge|le)\s", clause) is None
        assert " eq " in clause or " in (" in clause


def test_json_dimension_quotes_keys_with_punctuation_and_leaves_bare_keys_alone() -> (
    None
):
    assert od.json_dimension("eventData", "plan") == "eventData/plan"
    assert od.json_dimension("flags", "beta_banner") == "flags/beta_banner"
    assert od.json_dimension("flags", "my-flag") == "flags/'my-flag'"
    assert (
        od.json_dimension("eventData", "'signup-source'") == "eventData/'signup-source'"
    )


def test_json_dimension_rejects_an_empty_key() -> None:
    with pytest.raises(ConfigError) as excinfo:
        od.json_dimension("eventData", "  ")
    assert "eventData/plan" in str(excinfo.value)
