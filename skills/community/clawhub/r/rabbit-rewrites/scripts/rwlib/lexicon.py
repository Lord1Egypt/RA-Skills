#!/usr/bin/env python3
"""
The pattern catalogue, loaded once and shared.

scan.py scores against it, verify.py gates against it, and PROOF.md publishes
numbers measured against it. Those three only mean the same thing if they read
the same file, and "measured against lexicon 3" is only checkable if the file
says which version it is. `version` is that field, echoed into scan's --json
output and into PROOF.md's header.

Stdlib only, 3.9+.
"""

import functools
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEXICON_PATH = os.path.join(os.path.dirname(HERE), "lexicon.json")


# Findings the engine raises itself rather than from a catalogue pattern. A
# register may name any of these in its skip or relax set, so anything checking
# those ids has to know them.
SYNTHETIC_FINDING_IDS = frozenset({
    "hidden-unicode", "tier1", "clarity", "tier2-cluster", "tier3-density",
    "uniformity", "low-diversity", "trigram-repetition", "uniform-paragraphs",
    "em-dash-rate",
    # Findings about the suppression comments themselves. See rwlib/suppress.py.
    "suppression-invalid", "suppression-unused", "suppression-refused",
    # The safety band. See rwlib/injection.py.
    "injection-hidden-directive", "injection-tag-smuggling",
    "injection-hidden-text", "injection-visible-directive",
})

# The worst priority each of those can be raised at, which a catalogue pattern
# carries in its own entry and a synthetic finding has nowhere else to put. Only
# hidden-unicode reaches P0, and only for the zero-width half of its table.
#
# scan.py reads this table at each call site rather than repeating the string,
# so there is nothing left to keep in step. It used to be a hand-sync, with a
# test that pinned the two id sets equal and said nothing about whether the
# engine agreed on the priority: `registers.problems` could be told a finding was
# P1 while scan.py raised it at P2, and the p0-only check silently covered the
# wrong set. Add an id here and to SYNTHETIC_FINDING_IDS, and synthetic_priority
# raises on any id that is only in one.
SYNTHETIC_PRIORITIES = {
    "hidden-unicode": "P0",
    # Concealment and a directive in the same span. The co-occurrence is the
    # attack, and either one alone sits a band lower.
    "injection-hidden-directive": "P0",
    "injection-tag-smuggling": "P0",
    "injection-hidden-text": "P1",
    "injection-visible-directive": "P2",
    "suppression-refused": "P1",
    "tier1": "P1",
    "clarity": "P1",
    "tier2-cluster": "P1",
    "uniformity": "P1",
    "em-dash-rate": "P1",
    "suppression-invalid": "P1",
    "tier3-density": "P2",
    "low-diversity": "P2",
    "trigram-repetition": "P2",
    "uniform-paragraphs": "P2",
    "suppression-unused": "P2",
}


def synthetic_priority(finding_id):
    """The priority scan.py raises this synthetic finding at.

    Raises rather than defaulting. A default is how the table and the engine
    drifted apart in the first place: the miss has to be loud at the call site,
    at import-time-adjacent cost, rather than showing up months later as a
    register tolerance nobody is honouring.
    """
    try:
        return SYNTHETIC_PRIORITIES[finding_id]
    except KeyError:
        raise KeyError(
            "no declared priority for synthetic finding %r. Add it to "
            "SYNTHETIC_PRIORITIES and SYNTHETIC_FINDING_IDS in rwlib/lexicon.py."
            % finding_id)


# A regex that cannot match anything, for an empty word or phrase list. The
# alternation these functions build is `(a|b|c)`, and with nothing to join that
# collapses to `()`, which matches the empty string at every position in the
# document. Two of the callers do not filter zero-length matches, so an edited
# lexicon with an empty tier would have reported a cluster in every paragraph.
NEVER_RX = re.compile(r"(?!)")

_CACHE = {}


def load(path=LEXICON_PATH):
    """The parsed lexicon. Cached by path: scan.py reads it once per document
    and the corpus regression test runs it over a hundred of them."""
    if path not in _CACHE:
        with open(path, encoding="utf-8") as fh:
            _CACHE[path] = json.load(fh)
    return _CACHE[path]


def version(path=LEXICON_PATH):
    """The lexicon's declared version, or None on a file that predates the key.

    None rather than a guess: a report that invents a version number is worse
    than one that admits it does not know, because the whole point of the field
    is to make a published measurement reproducible.
    """
    return load(path).get("version")


def pattern_source(finding_id, path=LEXICON_PATH):
    """The raw `rx` string a catalogue entry carries, for a caller outside
    scan.py that needs the same alternation without a second hardcoded copy.

    artifacts.py's AI_PARAM_RX is the one caller today: the provider list
    inside `ai-utm`'s pattern used to be typed out a second time over there,
    and the two drifted apart from having no way to notice they should agree.
    Raises rather than returning None on a missing id, the same reasoning as
    synthetic_priority above: a caller reaching for a pattern that got
    renamed should fail at import time, not compile an empty alternation and
    match nothing forever.
    """
    for p in load(path).get("patterns", []):
        if p.get("id") == finding_id:
            return p["rx"]
    raise KeyError("no pattern named %r in %s" % (finding_id, path))


def word_regex(entries):
    """Whole-word alternation, longest first so `game-changer` wins over `game`.

    The boundary is `(?<![\\w-])` rather than `\\b`, because a hyphen is a word
    character to a reader and not to `re`: without it, "cutting-edge" matches
    the bare word "edge" as well.

    An empty list gives back NEVER_RX rather than an empty alternation.
    """
    escaped = sorted((re.escape(e) for e in entries), key=len, reverse=True)
    if not escaped:
        return NEVER_RX
    return re.compile(r"(?i)(?<![\w-])(" + "|".join(escaped) + r")(?![\w-])")


def phrase_regex(entries):
    """Same, for multi-word entries, with runs of whitespace made flexible so a
    phrase still matches across a line break. Empty in, NEVER_RX out."""
    escaped = sorted((re.escape(e).replace(r"\ ", r"\s+") for e in entries),
                     key=len, reverse=True)
    if not escaped:
        return NEVER_RX
    return re.compile(r"(?i)\b(" + "|".join(escaped) + r")\b")


# Everything scan.py reads off a catalogue entry. Checked here rather than at
# the point of use, because "drop the one bad rule" is only true if the entry is
# dropped before anybody indexes into it: an entry carrying `rx` but no `id`
# compiled fine and then raised KeyError out of scan.py's `relax.get(p["id"])`,
# which is the same whole-scan outage this function exists to prevent, moved one
# file along.
REQUIRED_PATTERN_KEYS = ("id", "label", "band", "priority", "rx")


@functools.lru_cache(maxsize=32)
def _compiled_patterns_cached(path, skip_set):
    out = []
    for p in load(path).get("patterns", []):
        if p.get("id") in skip_set:
            continue
        missing = [k for k in REQUIRED_PATTERN_KEYS if not p.get(k)]
        if missing:
            print("lexicon: unusable pattern %s (missing %s)"
                  % (p.get("id", "<no id>"), ", ".join(missing)), file=sys.stderr)
            continue
        try:
            out.append((p, re.compile(p["rx"])))
        except re.error as exc:
            print("lexicon: unusable pattern %s (%s)" % (p["id"], exc),
                  file=sys.stderr)
    return out


def compiled_patterns(path=LEXICON_PATH, skip=()):
    """[(entry, compiled_rx)] for every catalogue pattern that compiles."""
    return _compiled_patterns_cached(path, frozenset(skip))
