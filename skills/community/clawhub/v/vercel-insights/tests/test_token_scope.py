"""Token scope: what a project scoped token can and cannot reach.

Vercel has two kinds of endpoint behind this tool. Web Analytics takes a
``projectId`` and is project-level, so a token scoped to one project reads it
fine. The observability API that serves Speed Insights takes ``scope.ownerId``
and is account-level, so the same token has no account to resolve and Vercel
answers ``404 Observability Data not found.``

That message reads as "your project has no data" when it means "this token
cannot ask", which is a genuinely expensive confusion: the API is not lying, it
is answering a different question than the one the reader thinks they asked.
These tests pin the explanation that turns it into something actionable.
"""

from __future__ import annotations

import pytest
from conftest import Cli
from helpers import OWNER, PROJECT, TOKEN, FakeResponse, FakeSession

NOT_FOUND = {"error": {"code": "not_found", "message": "Observability Data not found."}}
ENV = {"VERCEL_TOKEN": TOKEN, "VERCEL_PROJECT_ID": PROJECT, "VERCEL_OWNER_ID": OWNER}
WINDOW = ["--since", "2026-08-07", "--until", "2026-08-14"]


@pytest.mark.parametrize(
    "argv",
    [
        ["--list-metrics"],
        ["slowest-pages", *WINDOW],
        ["vitals", *WINDOW],
    ],
    ids=["schema", "grouped-query", "vitals"],
)
def test_an_observability_404_explains_token_scope(cli: Cli, argv: list[str]) -> None:
    session = FakeSession(*[FakeResponse(404, NOT_FOUND) for _ in range(6)])
    code, _out, err = cli.run(argv, env=dict(ENV), session=session)
    assert code == 1
    # Vercel's own wording is kept, then explained rather than replaced.
    assert "Observability Data not found." in err
    assert "scoped to a single project" in err
    assert "account" in err
    assert "https://vercel.com/account/tokens" in err


def test_the_explanation_says_web_analytics_still_works(cli: Cli) -> None:
    # The useful half of the news: a project scoped token is not useless here.
    session = FakeSession(FakeResponse(404, NOT_FOUND))
    code, _out, err = cli.run(["--list-metrics"], env=dict(ENV), session=session)
    assert code == 1
    assert "Web Analytics presets keep working" in err


def test_a_web_analytics_404_is_left_alone(cli: Cli) -> None:
    # The hint is about one surface. Attaching it to every 404 would be noise,
    # and wrong: Web Analytics does not scope by account.
    session = FakeSession(FakeResponse(404, NOT_FOUND))
    code, _out, err = cli.run(
        ["top-pages", *WINDOW], env=dict(ENV), session=session
    )
    assert code == 1
    assert "Observability Data not found." in err
    assert "scoped to a single project" not in err


@pytest.mark.parametrize("status", [401, 403, 429, 500])
def test_only_a_404_gets_the_scope_explanation(cli: Cli, status: int) -> None:
    # A 403 is a different problem with a different fix, and guessing "your
    # token is project scoped" at one would send the reader the wrong way.
    body = {"error": {"code": "forbidden", "message": "Not authorized"}}
    session = FakeSession(*[FakeResponse(status, body) for _ in range(6)])
    code, _out, err = cli.run(
        ["--list-metrics", "--max-retries", "0"], env=dict(ENV), session=session
    )
    assert code == 1
    assert "scoped to a single project" not in err


# ---------------------------------------------------------------------------
# VERCEL_ORG_ID, which is Vercel's own name for the owning account
# ---------------------------------------------------------------------------


def test_vercel_org_id_supplies_the_owner(cli: Cli) -> None:
    # `vercel link` writes VERCEL_ORG_ID, so anyone with a standard Vercel setup
    # already has the owner in their environment under that name.
    session = FakeSession(FakeResponse(200, {"version": 1, "data": []}))
    code, _out, err = cli.run(
        ["slowest-pages", *WINDOW],
        env={
            "VERCEL_TOKEN": TOKEN,
            "VERCEL_PROJECT_ID": PROJECT,
            "VERCEL_ORG_ID": "team_from_org_id",
        },
        session=session,
    )
    assert code == 0, err
    # One request: no owner lookup was needed.
    assert len(session.calls) == 1
    assert session.calls[0]["json"]["scope"]["ownerId"] == "team_from_org_id"


def test_vercel_owner_id_wins_over_vercel_org_id(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, {"version": 1, "data": []}))
    code, _out, err = cli.run(
        ["slowest-pages", *WINDOW],
        env={
            "VERCEL_TOKEN": TOKEN,
            "VERCEL_PROJECT_ID": PROJECT,
            "VERCEL_ORG_ID": "team_from_org_id",
            "VERCEL_OWNER_ID": "own_explicit",
        },
        session=session,
    )
    assert code == 0, err
    assert session.calls[0]["json"]["scope"]["ownerId"] == "own_explicit"


def test_an_explicit_flag_still_wins_over_both(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, {"version": 1, "data": []}))
    code, _out, err = cli.run(
        ["slowest-pages", "--owner-id", "own_flag", *WINDOW],
        env={
            "VERCEL_TOKEN": TOKEN,
            "VERCEL_PROJECT_ID": PROJECT,
            "VERCEL_ORG_ID": "team_from_org_id",
            "VERCEL_OWNER_ID": "own_env",
        },
        session=session,
    )
    assert code == 0, err
    assert session.calls[0]["json"]["scope"]["ownerId"] == "own_flag"


# ---------------------------------------------------------------------------
# A team owned project needs its team named on every request
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("status", [403, 404])
def test_a_web_analytics_refusal_suggests_the_team_when_none_was_given(
    cli: Cli, status: int
) -> None:
    # Vercel: "For team projects, find the team's teamId or slug and include one
    # in each request." Omitting it looks exactly like not having access, and
    # the API says nothing about which of the two it is.
    body = {"error": {"code": "forbidden", "message": "Not authorized"}}
    session = FakeSession(*[FakeResponse(status, body) for _ in range(4)])
    code, _out, err = cli.run(
        ["top-pages", *WINDOW],
        env={"VERCEL_TOKEN": TOKEN, "VERCEL_PROJECT_ID": PROJECT},
        session=session,
    )
    assert code == 1
    assert "VERCEL_TEAM_ID" in err
    assert "--team" in err


def test_no_team_hint_when_a_team_was_already_configured(cli: Cli) -> None:
    # Suggesting the fix they already applied would send them the wrong way.
    body = {"error": {"code": "forbidden", "message": "Not authorized"}}
    session = FakeSession(*[FakeResponse(403, body) for _ in range(4)])
    code, _out, err = cli.run(
        ["top-pages", *WINDOW],
        env={"VERCEL_TOKEN": TOKEN, "VERCEL_PROJECT_ID": PROJECT, "VERCEL_TEAM_ID": "team_x"},
        session=session,
    )
    assert code == 1
    assert "VERCEL_TEAM_ID" not in err


def test_no_team_hint_on_an_unrelated_failure(cli: Cli) -> None:
    body = {"error": {"code": "bad_request", "message": "bad value"}}
    session = FakeSession(FakeResponse(400, body))
    code, _out, err = cli.run(
        ["top-pages", *WINDOW],
        env={"VERCEL_TOKEN": TOKEN, "VERCEL_PROJECT_ID": PROJECT},
        session=session,
    )
    assert code == 1
    assert "VERCEL_TEAM_ID" not in err
