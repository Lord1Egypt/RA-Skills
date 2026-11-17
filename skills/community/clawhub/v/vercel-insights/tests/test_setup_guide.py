"""The documentation set has to keep describing this tool, not a past version of it.

Two kinds of drift are guarded here, and both have actually happened.

The setup guide quotes messages a user might see in its troubleshooting table. A
quoted message that no longer matches what the code emits is worse than no table,
because it teaches someone to search for a string that will never appear.

And every document that describes the operation allowlist has to describe the
allowlist the code actually has. The endpoint count sat at "five" through several
releases after a sixth entry was added, in three files at once, because nothing
read them: the security claim a reader is asked to trust was checkable only by
hand. The expectations below are derived from ``OPERATIONS`` rather than written
out, so a seventh operation fails loudly in every file that owes the reader a
mention of it.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from vercel_insights import BASE_URL
from vercel_insights.http import OPERATIONS

ROOT = Path(__file__).resolve().parent.parent
GUIDE = (ROOT / "docs" / "openclaw-setup.md").read_text()
CLI = (ROOT / "vercel_insights" / "cli.py").read_text()
HTTP = (ROOT / "vercel_insights" / "http.py").read_text()
MAIN = (ROOT / "vercel_insights" / "__main__.py").read_text()
SOURCE = CLI + HTTP + MAIN

#: Documents that enumerate the endpoints one by one, and must therefore name
#: every one of them. ``full_url`` says how that file writes an entry on the API
#: host: ``True`` for the whole URL, ``False`` for the path alone. The second
#: host is always written out in full, because the host is the notable part.
ENUMERATING_DOCS: tuple[tuple[str, bool], ...] = (
    ("README.md", False),
    ("docs/cli-contract.md", True),
    ("docs/openclaw-setup.md", False),
)

#: Documents that state how many entries the allowlist has. ``CONTRIBUTING.md``
#: is here and not above on purpose: it tells a contributor what the ceiling is
#: rather than listing the endpoints, so the count is the whole of its claim.
COUNTING_DOCS: tuple[str, ...] = (
    "README.md",
    "docs/cli-contract.md",
    "docs/openclaw-setup.md",
    "CONTRIBUTING.md",
)

#: The prose spells small numbers out; the setup guide writes a digit. Either is
#: accepted, and the count itself comes from ``OPERATIONS``.
NUMBER_WORDS: dict[int, str] = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
}

#: What these documents call one allowlist entry.
ENTRY_NOUNS: tuple[str, ...] = ("entries", "endpoints", "operations")


def _read(name: str) -> str:
    return (ROOT / name).read_text()


def _flat(text: str) -> str:
    """One line, without the markdown emphasis and code ticks around a number.

    A claim can be wrapped across lines or bolded ("exactly **six** entries"),
    neither of which changes what it says, so neither should decide whether this
    test passes.
    """
    return re.sub(r"[*`]", "", " ".join(text.split()))


def _documented_url(url: str, full_url: bool) -> str:
    """The URL as the file under test writes it."""
    if full_url or not url.startswith(BASE_URL):
        return url
    return url[len(BASE_URL) :]


def _count_phrases(number: int) -> list[str]:
    """Every way these files write "the allowlist has this many entries".

    Both the digit and the spelled-out word, against each noun they use for an
    entry, plus the hyphenated adjective form ("six-endpoint allowlist"), which
    is the exact phrase that went stale in two files. Lower case, because the
    text is lowered before matching: a claim is no less a claim for starting a
    sentence.
    """
    forms = (str(number), NUMBER_WORDS[number])
    phrases = [f"{form} {noun}" for form in forms for noun in ENTRY_NOUNS]
    phrases.extend(f"{form}-endpoint" for form in forms)
    return phrases


def _stale_phrases(number: int) -> list[str]:
    """The shapes a stale count took, rather than every shape of a number.

    Narrower than :func:`_count_phrases` on purpose. The real drift was
    "exactly three entries" and "five-endpoint allowlist" a few lines apart in
    one file, and those two shapes only ever describe the whole allowlist. A
    bare "five entries" does not: `docs/cli-contract.md` correctly says "Five
    entries are on `api.vercel.com`", which is a true statement about a subset,
    and matching that as a stale claim would report a correct file as wrong.
    Narrowing is what lets this run case-insensitively, which a bare form could
    not.
    """
    forms = (str(number), NUMBER_WORDS[number])
    phrases = [f"exactly {form} {noun}" for form in forms for noun in ENTRY_NOUNS]
    phrases.extend(f"{form}-endpoint" for form in forms)
    return phrases


def _names_host(text: str, host: str) -> bool:
    """Whether ``text`` names this host rather than merely containing its tail.

    ``"vercel.com" in text`` is true of every mention of ``api.vercel.com``,
    since one is a substring of the other, so asserting it did no work at all:
    a file could enumerate the API host alone and still pass. A host counts as
    named only where the character before it cannot itself be part of a
    hostname, which is what tells the dashboard host apart from the API one.
    """
    return re.search(rf"(?<![A-Za-z0-9.-]){re.escape(host)}", text) is not None


def test_the_guide_exists_and_is_linked_from_both_entry_points() -> None:
    assert "docs/openclaw-setup.md" in (ROOT / "README.md").read_text()
    assert "openclaw-setup.md" in (ROOT / "SKILL.md").read_text()


@pytest.mark.parametrize(
    "phrase",
    [
        # Each of these is quoted in the troubleshooting table and must still be
        # something the code can actually produce.
        "is not importable by this interpreter",
        "scoped to a single project",
        "VERCEL_TEAM_ID",
    ],
)
def test_quoted_messages_still_exist_in_the_code(phrase: str) -> None:
    assert phrase in GUIDE, f"the guide no longer mentions {phrase!r}"
    assert phrase in SOURCE, f"the code no longer emits {phrase!r}"


def test_the_documented_exit_codes_match_the_code() -> None:
    from vercel_insights.budgets import BUDGET_EXCEEDED

    # The number alone is not enough: a row that says "3" and describes the
    # wrong thing is worse than a missing row.
    for code, meaning in ((0, "success"), (1, "API"), (2, "configured"), (3, "budget")):
        row = next((ln for ln in GUIDE.splitlines() if ln.startswith(f"| {code} |")), None)
        assert row is not None, f"exit code {code} is undocumented"
        assert meaning.lower() in row.lower(), f"exit code {code} describes the wrong thing"
    assert BUDGET_EXCEEDED == 3, "the documented budget exit code drifted"


@pytest.mark.parametrize("document,full_url", ENUMERATING_DOCS, ids=lambda item: str(item))
@pytest.mark.parametrize("operation", sorted(OPERATIONS))
def test_every_allowlisted_endpoint_is_documented_with_its_method(
    operation: str, document: str, full_url: bool
) -> None:
    # Derived from OPERATIONS rather than from a list written out here, so an
    # operation added to the code is missing from these files until someone adds
    # it, and the failure says which file and which URL.
    method, url = OPERATIONS[operation]
    text = _read(document)
    written = _documented_url(url, full_url)
    assert written in text, (
        f"{document} does not mention {written}, which the {operation} operation "
        "can send this user's token to"
    )
    rows = [line for line in text.splitlines() if written in line and "|" in line]
    assert rows, f"{document} mentions {written} but not in a table row"
    assert any(method in row for row in rows), (
        f"{document} documents {written} without its method ({method})"
    )


@pytest.mark.parametrize("document", [name for name, _full in ENUMERATING_DOCS])
def test_every_host_the_allowlist_can_reach_is_named(document: str) -> None:
    # The second host is the surprising part of this allowlist, so a file that
    # enumerates endpoints has to name every host, not only the API one.
    text = _read(document)
    for host in sorted({url.split("/")[2] for _method, url in OPERATIONS.values()}):
        assert _names_host(text, host), f"{document} never names the {host} host"


@pytest.mark.parametrize("document", COUNTING_DOCS)
def test_the_documented_endpoint_count_matches_the_allowlist(document: str) -> None:
    # The count is a security claim, and it is the part that drifted: it said
    # five for several releases after the sixth entry landed. Both spellings are
    # accepted because the prose spells the number and the setup guide digits it;
    # what is not accepted is a number that is no longer the real one.
    flat = _flat(_read(document)).lower()
    count = len(OPERATIONS)
    assert any(phrase in flat for phrase in _count_phrases(count)), (
        f"{document} does not say the allowlist has {count} "
        f"{ENTRY_NOUNS[0]}; it must, or its security claim is stale"
    )
    # A stale count next to a correct one is the shape the real drift took:
    # docs/cli-contract.md said "exactly three entries" and "five-endpoint
    # allowlist" a few lines apart, and both were wrong.
    stale = [
        phrase
        for number in NUMBER_WORDS
        if number != count
        for phrase in _stale_phrases(number)
        if phrase in flat
    ]
    assert not stale, f"{document} still claims {stale[0]!r}"


def test_the_guide_does_not_recommend_the_route_that_does_not_prompt() -> None:
    # `openclaw configure --section skills` reports status and exits. It may
    # only appear here as the warning that it is not the way in.
    for line in GUIDE.splitlines():
        if "openclaw configure --section skills" in line:
            assert "not" in line.lower(), (
                "configure is mentioned without saying it does not prompt"
            )
