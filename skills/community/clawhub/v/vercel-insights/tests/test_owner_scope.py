"""The Speed Insights scope, as the live API actually defines it.

The shape here is verified rather than inferred. A request carrying the earlier
guess, ``{"type": "project", "projectId": ...}``, was answered with HTTP 400
naming both real fields:

    path ["scope", "ownerId"]     expected string, received undefined
    path ["scope", "projectIds"]  expected array,  received undefined

So the scope is ``{"ownerId": <string>, "projectIds": [<string>, ...]}``. There
is no type discriminator and no team key: a team owned project is expressed by
making the team the owner. This module pins that, and pins how the owner is
found when nothing supplies it.
"""

from __future__ import annotations

import json

import pytest
from conftest import Cli
from helpers import OWNER, PROJECT, TOKEN, FakeResponse, FakeSession

from vercel_insights.cli import OWNER_PLACEHOLDER

WINDOW = ["--since", "2026-08-07", "--until", "2026-08-14"]
EMPTY = {"version": 1, "data": []}
PROJECT_PAYLOAD = {"id": PROJECT, "name": "demo", "accountId": "own_from_api"}


def _bodies(out: str) -> list[dict[str, object]]:
    """Every JSON body printed by a dry run."""
    bodies: list[dict[str, object]] = []
    depth = 0
    buffer: list[str] = []
    for line in out.splitlines():
        stripped = line.strip()
        if stripped.startswith("{"):
            depth += stripped.count("{") - stripped.count("}")
            buffer.append(stripped)
            if depth == 0:
                bodies.append(json.loads("".join(buffer)))
                buffer = []
            continue
        if buffer:
            depth += stripped.count("{") - stripped.count("}")
            buffer.append(stripped)
            if depth == 0:
                bodies.append(json.loads("".join(buffer)))
                buffer = []
    return bodies


# ---------------------------------------------------------------------------
# Where the owner comes from
# ---------------------------------------------------------------------------


def test_an_explicit_owner_id_is_used_without_any_lookup(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, EMPTY))
    code, _out, err = cli.run(
        ["slowest-pages", "--project", PROJECT, "--owner-id", "own_x", *WINDOW],
        env={"VERCEL_TOKEN": TOKEN},
        session=session,
    )
    assert code == 0, err
    assert len(session.calls) == 1, "an explicit owner must cost no extra request"
    assert session.calls[0]["json"]["scope"]["ownerId"] == "own_x"


def test_the_environment_supplies_the_owner_too(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, EMPTY))
    code, _out, err = cli.run(
        ["slowest-pages", *WINDOW],
        env={"VERCEL_TOKEN": TOKEN, "VERCEL_PROJECT_ID": PROJECT, "VERCEL_OWNER_ID": OWNER},
        session=session,
    )
    assert code == 0, err
    assert len(session.calls) == 1
    assert session.calls[0]["json"]["scope"]["ownerId"] == OWNER


def test_a_team_is_its_own_owner_and_needs_no_lookup(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, EMPTY))
    code, _out, err = cli.run(
        ["slowest-pages", "--project", PROJECT, "--team", "team_abc", *WINDOW],
        env={"VERCEL_TOKEN": TOKEN},
        session=session,
    )
    assert code == 0, err
    assert len(session.calls) == 1
    assert session.calls[0]["json"]["scope"]["ownerId"] == "team_abc"


def test_an_unspecified_owner_is_read_off_the_project_record(cli: Cli) -> None:
    # Two calls: the project lookup, then the query. The project record is the
    # right source because it answers the same way for a team owned and a
    # personal project, and the token must already be able to read it.
    session = FakeSession(FakeResponse(200, PROJECT_PAYLOAD), FakeResponse(200, EMPTY))
    code, _out, err = cli.run(
        ["slowest-pages", "--project", PROJECT, *WINDOW],
        env={"VERCEL_TOKEN": TOKEN},
        session=session,
    )
    assert code == 0, err
    assert len(session.calls) == 2
    assert session.calls[0]["method"] == "GET"
    assert session.calls[0]["url"].endswith(f"/v9/projects/{PROJECT}")
    assert session.calls[1]["json"]["scope"]["ownerId"] == "own_from_api"


def test_a_project_without_an_account_id_fails_with_the_flag_to_set(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, {"id": PROJECT, "name": "demo"}))
    code, _out, err = cli.run(
        ["slowest-pages", "--project", PROJECT, *WINDOW],
        env={"VERCEL_TOKEN": TOKEN},
        session=session,
    )
    assert code == 2
    assert "--owner-id" in err
    assert "Traceback" not in err
    # The refusal names the surface that could not be scoped, because the same
    # lookup now serves request logs and the two need telling apart.
    assert "Speed Insights query could not be scoped" in err


# ---------------------------------------------------------------------------
# A slug is a name, not an account id
# ---------------------------------------------------------------------------


def test_a_team_slug_alone_is_refused_rather_than_answered_for_the_wrong_account(
    cli: Cli,
) -> None:
    # Falling back to the personal account here would answer confidently about
    # the wrong account, which is worse than failing.
    code, _out, err = cli.run(
        ["slowest-pages", "--project", PROJECT, "--team-slug", "acme", *WINDOW],
        env={"VERCEL_TOKEN": TOKEN},
        session=None,
    )
    assert code == 2
    assert "--team-slug" in err
    assert "--team" in err and "--owner-id" in err


def test_a_team_slug_is_still_fine_on_a_web_analytics_preset(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, {"version": 1, "query": {}, "data": []}))
    code, _out, err = cli.run(
        ["top-pages", "--project", PROJECT, "--team-slug", "acme", *WINDOW],
        env={"VERCEL_TOKEN": TOKEN},
        session=session,
    )
    assert code == 0, err
    assert session.calls[0]["params"] == [
        ("projectId", PROJECT),
        ("by", "requestPath"),
        ("since", "2026-08-07T00:00:00Z"),
        ("until", "2026-08-14T00:00:00Z"),
        ("limit", "10"),
        ("slug", "acme"),
    ]


# ---------------------------------------------------------------------------
# A dry run resolves nothing, and says so
# ---------------------------------------------------------------------------


def test_a_dry_run_shows_a_placeholder_owner_and_explains_it(cli: Cli) -> None:
    code, out, err = cli.run(
        ["slowest-pages", "--project", PROJECT, *WINDOW, "--dry-run"],
        env={},
        session=None,
    )
    assert code == 0, err
    body = _bodies(out)[0]
    scope = body["scope"]
    assert isinstance(scope, dict)
    assert scope["ownerId"] == OWNER_PLACEHOLDER
    assert scope["projectIds"] == [PROJECT]
    assert "accountId" in out or "project" in out
    assert "--owner-id" in out
    # This surface really does carry the owner inside a scope object, so the note
    # names it that way. The request logs surface sends a plain query parameter
    # and gets its own wording; tests/test_logs_cli.py holds that half.
    assert "scope.ownerId shows" in out


def test_a_dry_run_with_a_known_owner_prints_no_placeholder_note(cli: Cli) -> None:
    code, out, err = cli.run(
        ["slowest-pages", "--project", PROJECT, "--owner-id", "own_x", *WINDOW, "--dry-run"],
        env={},
        session=None,
    )
    assert code == 0, err
    assert OWNER_PLACEHOLDER not in out
    assert _bodies(out)[0]["scope"] == {
        "type": "project",
        "ownerId": "own_x",
        "projectIds": [PROJECT],
    }


# ---------------------------------------------------------------------------
# projectIds wants ids
# ---------------------------------------------------------------------------


def test_a_project_name_warns_because_this_surface_scopes_by_id(cli: Cli) -> None:
    # The Web Analytics endpoints accept a name or an id; this one takes
    # projectIds, so a name is likely to come back empty rather than error.
    code, _out, err = cli.run(
        ["slowest-pages", "--project", "my-site", "--owner-id", "own_x", *WINDOW, "--dry-run"],
        env={},
        session=None,
    )
    assert code == 0, err
    assert "prj_" in err
    assert "my-site" in err


def test_a_real_project_id_warns_about_nothing(cli: Cli) -> None:
    code, _out, err = cli.run(
        ["slowest-pages", "--project", PROJECT, "--owner-id", "own_x", *WINDOW, "--dry-run"],
        env={},
        session=None,
    )
    assert code == 0, err
    assert "prj_" not in err


# ---------------------------------------------------------------------------
# The scope shape itself
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("selection", "expected"),
    [
        (
            ["--project", PROJECT],
            {"type": "project", "ownerId": "own_x", "projectIds": [PROJECT]},
        ),
        (["--all"], {"type": "owner", "ownerId": "own_x"}),
    ],
    ids=["one-project", "all-projects"],
)
def test_the_scope_is_a_union_discriminated_on_type(
    cli: Cli, selection: list[str], expected: dict[str, object]
) -> None:
    code, out, err = cli.run(
        ["vitals-by-country", *selection, "--owner-id", "own_x", *WINDOW, "--dry-run"],
        env={},
        session=None,
    )
    assert code == 0, err
    # Two live 400s pinned this: the first named ownerId and projectIds as
    # required, the second refused a body with no "type" as having no matching
    # discriminator. Both halves are needed.
    assert _bodies(out)[0]["scope"] == expected
