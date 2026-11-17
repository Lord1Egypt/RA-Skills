#!/usr/bin/env python3
"""
Shape rules for thesaurus.json, in the one place its three consumers share.

`scripts/validate.py` checks the shipped file, `04_merge_accepted.py` in the
research pipeline checks a merged object before writing it, and the skill's
own `tests/test_thesaurus.py` checks it on a checkout where the repo validator
does not exist. Three restatements of one constraint set is how a merge script
and a validator come to disagree about what valid means, which is the drift
`rwlib.voice_check` already exists to prevent for voice profiles.

Each rule exists because breaking it is a silent failure downstream: a reach
word that is not a mechanical substitution gets skipped by fixes.py's
`is_mechanical_substitution`, an overreach term in two families produces two
competing rewrites of one word, and a reach word that is also somebody's
overreach term rewrites toward a word the next family is busy rewriting away.

Stdlib only, 3.9+.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
if "_bootstrap" in sys.modules and getattr(sys.modules["_bootstrap"], "__file__", None) != os.path.join(HERE, "_bootstrap.py"):
    del sys.modules["_bootstrap"]
import _bootstrap
from rwlib import fixes  # noqa: E402


def problems(data):
    """Everything wrong with a thesaurus object, as prose. Empty means valid."""
    out = []
    if not isinstance(data, dict):
        return ["thesaurus data is %s, not an object" % type(data).__name__]
    if not isinstance(data.get("version"), int):
        out.append("thesaurus has no integer version. measure_voice.py reports "
                   "it beside every proposal, so a family edit without a "
                   "version bump is a silent change to what a printed report "
                   "claimed")
    families = data.get("families")
    if not isinstance(families, list) or not families:
        out.append("thesaurus has no families list")
        return out
    seen_reach, seen_over = {}, {}
    for i, family in enumerate(families):
        reach = family.get("reach") if isinstance(family, dict) else None
        over = family.get("overreach") if isinstance(family, dict) else None
        if not reach or not fixes.is_mechanical_substitution(reach):
            out.append("thesaurus family %d: reach %r is not a 1-3 word "
                       "replacement shape, so fixes.py would never rewrite "
                       "to it" % (i, reach))
            continue
        if reach in seen_reach:
            out.append("thesaurus family %d: reach %r already belongs to "
                       "family %d, and two proposals would compete"
                       % (i, reach, seen_reach[reach]))
        if reach in seen_over:
            # The mirror of the overreach-is-a-reach rule below. Without it
            # the constraint holds in one file order and not the other.
            out.append("thesaurus family %d: reach %r is family %d's "
                       "overreach term, so one family undoes another"
                       % (i, reach, seen_over[reach]))
        seen_reach[reach] = i
        if not isinstance(over, list) or not over:
            out.append("thesaurus family %d (reach %r): overreach must be a "
                       "non-empty list" % (i, reach))
            continue
        for term in over:
            if not isinstance(term, str) or not term.strip():
                out.append("thesaurus family %d (reach %r): overreach entry "
                           "%r is not a term" % (i, reach, term))
                continue
            if term == reach:
                out.append("thesaurus family %d: %r is both the reach word "
                           "and an overreach term, so the family rewrites "
                           "toward the word it is rewriting away" % (i, term))
            if term in seen_reach and term != reach:
                out.append("thesaurus family %d: overreach term %r is family "
                           "%d's reach word, so one family undoes another"
                           % (i, term, seen_reach[term]))
            if term in seen_over:
                out.append("thesaurus family %d: overreach term %r already "
                           "belongs to family %d, and the two would propose "
                           "different rewrites of one word"
                           % (i, term, seen_over[term]))
            seen_over.setdefault(term, i)
    return out


def totals(data):
    """(reach_count, overreach_count), for the note a caller prints."""
    families = data.get("families", [])
    reaches = {f.get("reach") for f in families if isinstance(f, dict)}
    overs = {t for f in families if isinstance(f, dict)
             for t in f.get("overreach", []) if isinstance(t, str)}
    return len(reaches - {None}), len(overs)
