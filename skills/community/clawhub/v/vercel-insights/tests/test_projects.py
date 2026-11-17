"""Choosing among many projects, which is the first thing any query needs.

One Vercel account holds many projects and a query names exactly one, so
finding the right one is not a convenience feature: it is step one. These tests
cover the three parts of that.

They also pin a real inconsistency this fixed. Web Analytics accepts "the
project identifier or the project name", but Speed Insights scopes by
``projectIds`` and wants identifiers, so `--project my-site` worked for traffic
and silently returned nothing for speed. A name is now resolved to its id before
that surface sees it.
"""

from __future__ import annotations

import json

import pytest
from conftest import Cli
from helpers import TOKEN, FakeResponse, FakeSession

from vercel_insights import projects as vp

ENV = {"VERCEL_TOKEN": TOKEN}
WINDOW = ["--since", "2026-08-07", "--until", "2026-08-14"]

PROJECT_LIST = {
    "projects": [
        {
            "id": "prj_aaa",
            "name": "my-site",
            "accountId": "team_x",
            "webAnalytics": {"enabledAt": 1, "hasData": True},
            "speedInsights": {"enabledAt": 1, "hasData": True},
        },
        {
            "id": "prj_bbb",
            "name": "marketing",
            "accountId": "team_x",
            "webAnalytics": {"enabledAt": 1, "hasData": True},
            "speedInsights": {"enabledAt": 1, "hasData": False},
        },
        {"id": "prj_ccc", "name": "internal-tools", "accountId": "team_x"},
    ]
}
ONE_PROJECT = {"id": "prj_aaa", "name": "my-site", "accountId": "team_resolved"}
SPEED_OK = {
    "data": [{"vercel_speed_insights_lcp_ms_p75": 2400}],
    "summary": [{"vercel_speed_insights_lcp_ms_p75": 2400}],
}


# ---------------------------------------------------------------------------
# Listing
# ---------------------------------------------------------------------------


def test_every_project_is_listed_including_the_empty_ones(cli: Cli) -> None:
    # A project missing from the list would read as "does not exist" when it may
    # only have analytics switched off, which is a different problem.
    session = FakeSession(FakeResponse(200, PROJECT_LIST))
    code, out, err = cli.run(["--list-projects"], env=dict(ENV), session=session)
    assert code == 0, err
    for name in ("my-site", "marketing", "internal-tools"):
        assert name in out
    for identifier in ("prj_aaa", "prj_bbb", "prj_ccc"):
        assert identifier in out


def test_each_project_says_whether_it_has_data(cli: Cli) -> None:
    # "enabled but empty" and "not enabled" both produce an empty query and need
    # different fixes, so they are shown differently.
    session = FakeSession(FakeResponse(200, PROJECT_LIST))
    code, out, err = cli.run(["--list-projects"], env=dict(ENV), session=session)
    assert code == 0, err
    lines = {line.split()[0]: line for line in out.splitlines() if line.startswith("prj")
             or line.startswith(("my-site", "marketing", "internal-tools"))}
    assert "data" in lines["my-site"]
    assert "empty" in lines["marketing"]
    assert "off" in lines["internal-tools"]


def test_listing_needs_no_project_of_its_own(cli: Cli) -> None:
    # It is the thing you run precisely because you do not know which to name.
    session = FakeSession(FakeResponse(200, PROJECT_LIST))
    code, _out, err = cli.run(["--list-projects"], env={"VERCEL_TOKEN": TOKEN}, session=session)
    assert code == 0, err


def test_listing_uses_one_read_only_get(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, PROJECT_LIST))
    code, _out, err = cli.run(["--list-projects"], env=dict(ENV), session=session)
    assert code == 0, err
    assert len(session.calls) == 1
    assert session.calls[0]["method"] == "GET"
    assert session.calls[0]["url"] == "https://api.vercel.com/v10/projects"


def test_an_empty_account_says_so_and_mentions_token_scope(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, {"projects": []}))
    code, out, err = cli.run(["--list-projects"], env=dict(ENV), session=session)
    assert code == 0, err
    assert "no projects found" in out
    assert "scoped to a single project" in out


@pytest.mark.parametrize(
    "payload",
    [PROJECT_LIST, PROJECT_LIST["projects"], {"data": PROJECT_LIST["projects"]}],
    ids=["projects-key", "bare-list", "data-key"],
)
def test_the_plausible_response_shapes_are_read(payload: object) -> None:
    assert [p["id"] for p in vp.extract_projects(payload)] == [
        "prj_aaa",
        "prj_bbb",
        "prj_ccc",
    ]


def test_json_prints_the_untouched_payload(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, PROJECT_LIST))
    code, out, err = cli.run(["--list-projects", "--json"], env=dict(ENV), session=session)
    assert code == 0, err
    assert json.loads(out) == PROJECT_LIST


# ---------------------------------------------------------------------------
# A name works on both surfaces
# ---------------------------------------------------------------------------


def test_a_name_is_resolved_to_an_id_before_the_speed_query(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, ONE_PROJECT), FakeResponse(200, SPEED_OK))
    code, _out, err = cli.run(
        ["slowest-pages", "--project", "my-site", *WINDOW], env=dict(ENV), session=session
    )
    assert code == 0, err
    assert session.calls[0]["url"].endswith("/v9/projects/my-site")
    # The query scopes by the resolved id, not the name it was given.
    assert session.calls[1]["json"]["scope"]["projectIds"] == ["prj_aaa"]


def test_the_owner_comes_from_the_same_lookup(cli: Cli) -> None:
    # One request answers both questions, so a name costs nothing extra.
    session = FakeSession(FakeResponse(200, ONE_PROJECT), FakeResponse(200, SPEED_OK))
    code, _out, err = cli.run(
        ["slowest-pages", "--project", "my-site", *WINDOW], env=dict(ENV), session=session
    )
    assert code == 0, err
    assert len(session.calls) == 2
    assert session.calls[1]["json"]["scope"]["ownerId"] == "team_resolved"


def test_an_identifier_with_a_known_owner_skips_the_lookup(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, SPEED_OK))
    code, _out, err = cli.run(
        ["slowest-pages", "--project", "prj_aaa", "--owner-id", "own_1", *WINDOW],
        env=dict(ENV),
        session=session,
    )
    assert code == 0, err
    assert len(session.calls) == 1, "an id plus an owner needs no lookup at all"


def test_web_analytics_takes_a_name_with_no_lookup(cli: Cli) -> None:
    # That API accepts a name natively, so resolving one there would be a
    # request spent for nothing.
    session = FakeSession(FakeResponse(200, {"version": 1, "query": {}, "data": []}))
    code, _out, err = cli.run(
        ["top-pages", "--project", "my-site", *WINDOW], env=dict(ENV), session=session
    )
    assert code == 0, err
    assert len(session.calls) == 1
    assert dict(session.calls[0]["params"])["projectId"] == "my-site"


@pytest.mark.parametrize(
    ("value", "expected"),
    [("prj_aaa", True), ("my-site", False), ("", False), (None, False)],
)
def test_identifiers_are_told_apart_from_names(value: str | None, expected: bool) -> None:
    assert vp.looks_like_project_id(value) is expected


# ---------------------------------------------------------------------------
# Naming no project
# ---------------------------------------------------------------------------


def test_naming_no_project_lists_the_choices(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, PROJECT_LIST))
    code, _out, err = cli.run(["vitals", *WINDOW], env=dict(ENV), session=session)
    assert code == 2
    assert "no project configured" in err
    # The answer to the question behind the error, not just the error.
    assert "my-site" in err and "prj_aaa" in err


def test_a_failed_listing_leaves_the_original_message_intact(cli: Cli) -> None:
    # An error path is the worst place to raise a second error.
    session = FakeSession(FakeResponse(403, {"error": {"code": "forbidden", "message": "no"}}))
    code, _out, err = cli.run(["vitals", *WINDOW], env=dict(ENV), session=session)
    assert code == 2
    assert "no project configured" in err
    assert "Traceback" not in err


def test_a_dry_run_never_spends_a_request_to_be_helpful(cli: Cli) -> None:
    code, _out, err = cli.run(["vitals", *WINDOW, "--dry-run"], env={}, session=None)
    assert code == 2
    assert "no project configured" in err
