"""SKILL.md is the contract an agent reads, so it has to stay true.

Two claims in it are the kind people rely on and that drift silently: the list
of endpoints this skill may call, and the environment variables it reads.
ClawHub's own analysis checks the second against what the code does. Both have
gone stale during development, once by a blanket find-and-replace that updated a
sentence and left the table beneath it wrong, which is exactly the failure a test
catches and a careful reader does not.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from vercel_insights.http import OPERATIONS

SKILL = Path(__file__).resolve().parent.parent / "SKILL.md"
TEXT = SKILL.read_text()
FRONTMATTER = TEXT.split("---")[1] if TEXT.startswith("---") else ""

#: Every environment variable the package actually reads.
CODE_ENV = {
    "VERCEL_TOKEN",
    "VERCEL_PROJECT_ID",
    "VERCEL_TEAM_ID",
    "VERCEL_TEAM_SLUG",
    "VERCEL_OWNER_ID",
    "VERCEL_ORG_ID",
    "NO_COLOR",
}


def test_the_frontmatter_declares_every_environment_variable_the_code_reads() -> None:
    # ClawHub flags a mismatch between declared metadata and real behaviour, so
    # an undeclared variable is a publishing problem, not only a docs one.
    for name in sorted(CODE_ENV):
        assert name in FRONTMATTER, f"{name} is read by the code but not declared"


def test_the_code_reads_every_environment_variable_the_frontmatter_declares() -> None:
    # The other direction: declaring one the code ignores is a promise it cannot
    # keep, and it would send a user to set something with no effect.
    declared = set(re.findall(r"\b(VERCEL_[A-Z_]+|NO_COLOR)\b", FRONTMATTER))
    assert declared <= CODE_ENV, f"declared but unread: {sorted(declared - CODE_ENV)}"


def test_the_documented_endpoint_count_matches_the_allowlist() -> None:
    words = {3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}
    expected = words[len(OPERATIONS)]
    assert f"exactly {expected} entries" in TEXT
    assert f"{expected}-endpoint allowlist" in TEXT


@pytest.mark.parametrize("operation", sorted(OPERATIONS))
def test_every_allowlisted_operation_is_documented(operation: str) -> None:
    method, url = OPERATIONS[operation]
    path = url.replace("https://api.vercel.com", "")
    assert f"`{operation}`" in TEXT, f"{operation} is callable but undocumented"
    assert path in TEXT, f"{path} is callable but undocumented"
    row = next(
        (line for line in TEXT.splitlines() if f"`{operation}`" in line and "|" in line),
        None,
    )
    assert row is not None and method in row, f"{operation} documents the wrong method"


def test_no_endpoint_is_documented_that_the_code_cannot_call() -> None:
    # A documented endpoint that does not exist would overstate the surface,
    # which is as misleading as understating it.
    documented = set(re.findall(r"^\| `([a-z_]+)` \| (?:GET|POST) \|", TEXT, re.M))
    assert documented <= set(OPERATIONS), (
        f"documented but not callable: {sorted(documented - set(OPERATIONS))}"
    )


def test_the_declared_version_matches_the_package() -> None:
    from vercel_insights import VERSION

    assert re.search(rf"^version:\s*{re.escape(VERSION)}\s*$", FRONTMATTER, re.M)


def test_the_launcher_is_executable_and_documented() -> None:
    # An agent invoking this skill has its own working directory and no reason
    # to change it, so the entry point it is told to use must not depend on one.
    launcher = SKILL.parent / "bin" / "vercel-insights"
    assert launcher.exists(), "the documented launcher is missing"
    assert launcher.stat().st_mode & 0o111, "the launcher is not executable"
    assert "bin/vercel-insights" in TEXT


def test_the_launcher_runs_from_an_unrelated_directory() -> None:
    import subprocess

    from vercel_insights import VERSION

    launcher = SKILL.parent / "bin" / "vercel-insights"
    result = subprocess.run(
        [str(launcher), "--version"],
        capture_output=True,
        text=True,
        cwd="/",
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert VERSION in result.stdout


def test_only_the_token_gates_the_skill() -> None:
    # requires.env is a hard gate: a skill missing one of these is reported as
    # "needs setup" and stays there. Only the token qualifies, because the
    # project is discoverable through --list-projects and asking the user, so
    # gating on it would leave the skill permanently unready for no reason.
    gate = re.search(r"^\s*env:\s*\[([^\]]*)\]", FRONTMATTER, re.M)
    assert gate is not None, "requires.env is missing"
    names = {n.strip() for n in gate.group(1).split(",") if n.strip()}
    assert names == {"VERCEL_TOKEN"}, f"only the token should gate, found {names}"


def test_the_description_stays_short_enough_to_read_in_a_list() -> None:
    # `openclaw skills list` renders the description in a narrow column. A
    # keyword-stuffed paragraph wraps over many lines and reads as noise, which
    # costs more discoverability than the extra words buy.
    match = re.search(r"^description: >-\n((?:  .*\n)+)", FRONTMATTER, re.M)
    assert match is not None, "description is missing or not a folded block"
    text = " ".join(line.strip() for line in match.group(1).splitlines())
    assert len(text) <= 400, f"description is {len(text)} characters, trim it"


def test_the_setup_section_documents_the_real_config_mechanism() -> None:
    # Credentials belong in openclaw.json under skills.entries, not in a shell
    # profile, and apiKey is what primaryEnv maps to.
    assert "skills.entries" in TEXT or '"entries"' in TEXT
    assert "apiKey" in TEXT
    assert "primaryEnv" in TEXT


def test_setup_leads_with_the_supported_route() -> None:
    # `openclaw skills info` names two routes for saving the key: the Control UI
    # and `openclaw config set ...apiKey`. Both were checked against a real
    # install. `openclaw configure --section skills` reports status and does not
    # prompt, so documenting it as the way in sent people to a dead end.
    setup = TEXT[TEXT.find("## Setting it up") :]
    supported = setup.find("openclaw config set skills.entries")
    by_hand = setup.find('"skills": {')
    assert supported != -1, "the supported CLI route is missing"
    assert supported < by_hand, "the supported route should come before hand editing"
    assert "Control UI" in setup


def test_the_secret_reference_form_is_documented() -> None:
    # apiKey accepts a reference as well as a literal, so the token can stay in
    # the environment or a secrets provider rather than in openclaw.json.
    assert "--ref-provider" in TEXT and "--ref-id VERCEL_TOKEN" in TEXT
