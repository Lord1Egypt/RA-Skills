"""Tests for vercel_insights/presets.py, against literals from the contract.

The expectations below are transcribed by hand from the preset table in
docs/cli-contract.md. They are deliberately not read back from ``PRESETS``, so
a preset that quietly changes its dataset, grouping or limit fails here.
"""

from __future__ import annotations

import pytest
from conftest import Cli
from helpers import DRY_RUN_ENV, dry_run_calls, dry_run_values

from vercel_insights.presets import PRESETS, format_presets
from vercel_insights.timerange import LOGS

# preset -> one (endpoint, by values, limit) triple per request it issues.
PRESET_EXPECTATIONS: dict[str, list[tuple[str, list[str], str | None]]] = {
    "overview": [
        # The trend section asks for the API maximum so no bucket is dropped;
        # the two tables use the documented overview limit of 5.
        ("visits/aggregate", ["day"], "100"),
        ("visits/aggregate", ["requestPath"], "5"),
        ("visits/aggregate", ["referrerHostname"], "5"),
    ],
    "trend": [("visits/aggregate", ["day"], "100")],
    "top-pages": [("visits/aggregate", ["requestPath"], "10")],
    "top-routes": [("visits/aggregate", ["route"], "10")],
    "referrers": [("visits/aggregate", ["referrerHostname"], "10")],
    "countries": [("visits/aggregate", ["country"], "10")],
    "devices": [("visits/aggregate", ["deviceType"], "10")],
    "browsers": [("visits/aggregate", ["browserName"], "10")],
    "operating-systems": [("visits/aggregate", ["osName"], "10")],
    "campaigns": [("visits/aggregate", ["utmCampaign"], "10")],
    "events": [("events/aggregate", ["eventName"], "10")],
    "total": [("visits/count", [], None)],
}


@pytest.mark.parametrize("preset", sorted(PRESET_EXPECTATIONS))
def test_every_preset_hits_its_documented_endpoint_grouping_and_limit(
    cli: Cli, preset: str
) -> None:
    code, out, err = cli.run([preset, "--dry-run"], env=dict(DRY_RUN_ENV))
    assert code == 0, err
    calls = dry_run_calls(out)
    expected = PRESET_EXPECTATIONS[preset]
    assert len(calls) == len(expected), f"{preset} issued {len(calls)} requests"
    for (endpoint, params), (want_endpoint, want_by, want_limit) in zip(
        calls, expected
    ):
        assert endpoint == want_endpoint
        assert [value for key, value in params if key == "by"] == want_by
        limits = [value for key, value in params if key == "limit"]
        assert limits == ([want_limit] if want_limit is not None else [])


def test_the_default_run_with_no_arguments_is_the_overview_preset(cli: Cli) -> None:
    code, out, err = cli.run(["--dry-run"], env=dict(DRY_RUN_ENV))
    assert code == 0, err
    assert [endpoint for endpoint, _ in dry_run_calls(out)] == [
        "visits/aggregate",
        "visits/aggregate",
        "visits/aggregate",
    ]
    assert dry_run_values(out, "by", call=0) == ["day"]
    assert dry_run_values(out, "by", call=1) == ["requestPath"]
    assert dry_run_values(out, "by", call=2) == ["referrerHostname"]


def preset_row(out: str, name: str) -> list[str]:
    """The --list-presets line for one preset, split into its cells."""
    for line in out.splitlines():
        cells = line.split()
        if cells and cells[0] == name:
            return cells
    raise AssertionError(f"no {name!r} row in:\n{out}")


def test_list_presets_rows_match_the_documented_table(cli: Cli) -> None:
    code, out, err = cli.run(["--list-presets"], env={})
    assert code == 0
    assert err == ""

    # Transcribed from docs/cli-contract.md, not from PRESETS.
    top_pages = preset_row(out, "top-pages")
    assert top_pages[1:5] == ["visits", "aggregate", "requestPath", "10"]

    total = preset_row(out, "total")
    assert total[1:5] == ["visits", "count", "none", "n/a"]

    events = preset_row(out, "events")
    assert events[1:3] == ["events", "aggregate"]
    assert "eventName" in " ".join(events)

    overview = preset_row(out, "overview")
    assert overview[1] == "(default)"
    assert "3 x aggregate" in " ".join(overview)


#: Transcribed by hand from the preset table in docs/cli-contract.md, which says
#: 50 rows for logs and errors and 200 for error-summary. Not read back from
#: PRESETS: with nothing pinning the numbers, swapping the default and the
#: maximum between errors and error-summary passed every test, and that swap is
#: user-visible twice over, in the row budget and in build_report's
#: at-the-ceiling branch, which stops advising a raise once the limit is 200.
LOGS_PRESET_LIMITS: dict[str, int] = {"logs": 50, "errors": 50, "error-summary": 200}


@pytest.mark.parametrize("name", sorted(LOGS_PRESET_LIMITS))
def test_the_logs_presets_query_the_logs_surface(name: str) -> None:
    preset = PRESETS[name]
    assert preset.surface == LOGS
    assert preset.is_logs is True
    assert preset.group_by == ()
    assert preset.endpoint.endswith("request-logs")
    assert preset.dataset == "logs"
    assert preset.limit == LOGS_PRESET_LIMITS[name]


def test_the_errors_presets_issue_two_calls() -> None:
    assert PRESETS["errors"].calls == 2
    assert PRESETS["error-summary"].calls == 2
    assert PRESETS["logs"].calls == 1


@pytest.mark.parametrize(
    ("name", "since"),
    [("logs", "1h"), ("errors", "1h"), ("error-summary", "6h")],
)
def test_a_logs_preset_defaults_to_a_short_window(name: str, since: str) -> None:
    # Runtime logs are retained for an hour on Hobby and a day on Pro, so the
    # global 7d default would mostly report nothing and read as "no errors".
    assert PRESETS[name].default_since == since


def test_every_other_preset_keeps_the_global_default_window() -> None:
    for name, preset in PRESETS.items():
        if not preset.is_logs:
            assert preset.default_since is None, name


def test_the_preset_table_renders_with_the_logs_presets() -> None:
    text = format_presets()
    for name in ("logs", "errors", "error-summary"):
        assert name in text
    assert "request-logs" in text


@pytest.mark.parametrize("name", sorted(LOGS_PRESET_LIMITS))
def test_a_logs_preset_row_shows_its_documented_row_limit(name: str) -> None:
    # The limit column is what a reader checks before passing --limit, so the
    # printed table owes the same number the preset actually applies.
    row = preset_row(format_presets(), name)
    assert str(LOGS_PRESET_LIMITS[name]) in row
