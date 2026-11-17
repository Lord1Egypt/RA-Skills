#!/usr/bin/env python3
"""
Regular English suffixes, for a banned term that should catch its own forms.

A voice profile bans words, and English inflects them. The shipped profile lists
`synergy` and `synergies`, `thought leader` and `thought leaders` and `thought
leadership`, `bad actor` and `bad actors`, `circle back` and `circling back`.
Every one of those pairs is a line somebody had to think of, and the commonest
profile-authoring mistake is thinking of the singular and stopping. The ban then
reads as enforced and is not.

So a profile can opt one entry in:

    "banned_words": ["piggyback", {"word": "synergy", "inflect": true}]

Opt-in, per entry, and it stays that way. Expansion is a guess about a language
full of exceptions, and a deliberately narrow ban has to stay narrow: banning
`lowly` should not quietly ban `lowlying`, and an author who wrote one word meant
one word. The default is unchanged behaviour.

What it does not do, on purpose:

  Consonant doubling. `ship` does not become `shipping` here. The rule depends on
  stress, which is not recoverable from spelling, and guessing wrong produces
  `shiping`: a pattern that matches nothing and reads in the report as a rule
  that fired. A miss leaves the author exactly where they are today, which is
  the safer failure.

  Irregulars. `run`/`ran`, `child`/`children`. There is no rule to apply, only a
  dictionary, and shipping a dictionary to expand a ban list is more machinery
  than the problem is worth. List them by hand.

  Derivation. `leader` does not reach `leadership`. That is a different word, not
  a form of this one, and a profile that banned it by accident would be a profile
  the author cannot predict.

Multi-word entries inflect one word at a time, at every position, and the
results are unioned. `thought leader` reaches `thought leaders` that way, and
`circle back` reaches `circling back`, which inflecting only the head or only the
tail would each have missed. The junk that falls out alongside (`circle backing`,
`bads actor`) costs nothing: those are strings no document contains, so they
match nothing and report nothing.

Stdlib only, 3.9+.
"""

import re

VOWELS = "aeiou"
# Suffixes after which the plural or third-person form takes `es` rather than
# `s`, because the bare `s` would be unpronounceable: box/boxes, church/churches.
SIBILANT_ENDINGS = ("s", "x", "z", "ch", "sh")

WORD_SPLIT_RX = re.compile(r"(\s+)")


def _consonant_y(word):
    """True for `synergy` and `apply`, false for `day` and `key`.

    The distinction is the whole reason `y` needs its own branch: a consonant
    before it turns into `ies`, a vowel before it just takes `s`.
    """
    return len(word) > 1 and word[-1] == "y" and word[-2].lower() not in VOWELS


def plural(word):
    if _consonant_y(word):
        return word[:-1] + "ies"
    if word.lower().endswith(SIBILANT_ENDINGS):
        return word + "es"
    return word + "s"


def past(word):
    if _consonant_y(word):
        return word[:-1] + "ied"
    if word.lower().endswith("e"):
        return word + "d"
    return word + "ed"


def gerund(word):
    # `ee` keeps its second `e`: agree/agreeing, not agreing.
    if word.lower().endswith("e") and not word.lower().endswith("ee"):
        return word[:-1] + "ing"
    return word + "ing"


def word_forms(word):
    """One word and its regular s/es/ed/ing forms, deduplicated, order stable."""
    out = []
    for candidate in (word, plural(word), past(word), gerund(word)):
        if candidate and candidate not in out:
            out.append(candidate)
    return out


def forms(term):
    """Every form of a term, single word or phrase.

    A phrase varies one word at a time. Varying every word at once multiplies out
    to combinations no writer produces (`circling backing`) without reaching
    anything the one-at-a-time pass misses.
    """
    parts = WORD_SPLIT_RX.split(term.strip())
    words = [i for i, p in enumerate(parts) if p.strip()]
    if len(words) <= 1:
        return word_forms(term.strip())

    out = [term.strip()]
    for index in words:
        for variant in word_forms(parts[index])[1:]:
            swapped = list(parts)
            swapped[index] = variant
            candidate = "".join(swapped)
            if candidate not in out:
                out.append(candidate)
    return out


def expand(entries):
    """A voice's ban list, flattened to plain strings.

    Accepts the two spellings an entry can take, so a profile that never asks for
    expansion reads and behaves exactly as it did:

        "synergy"                              one term, as written
        {"word": "synergy", "inflect": true}   the term and its regular forms

    `phrase` is accepted as a spelling of `word`, because `banned_phrases` reads
    better with it and there is no reason to make the two lists take different
    keys. An entry with neither is dropped rather than crashing the scan: one
    malformed line in a hand-edited profile should cost that line, which is the
    same bargain compiled_patterns makes for the catalogue.
    """
    out = []
    for entry in entries or []:
        if isinstance(entry, str):
            candidates = [entry]
        elif isinstance(entry, dict):
            term = entry.get("word") or entry.get("phrase")
            if not term:
                continue
            candidates = forms(term) if entry.get("inflect") else [term]
        else:
            continue
        for candidate in candidates:
            if candidate not in out:
                out.append(candidate)
    return out


def term_of(entry):
    """The term an entry names, whichever spelling it uses. Used where a ban list
    has to be counted or merged rather than compiled."""
    if isinstance(entry, str):
        return entry
    if isinstance(entry, dict):
        return entry.get("word") or entry.get("phrase") or ""
    return ""


INVARIANT_OR_S_SINGULARS = {
    "alias", "status", "canvas", "basis", "lens", "series", "species",
    "corpus", "analysis", "hypothesis", "parenthesis", "focus", "virus",
    "census", "radius", "syllabus", "bus"
}

IE_SINGULAR_NOUNS = {
    "movie", "cookie", "brownie", "zombie", "rookie", "hippie", "sweetie",
    "pixie", "goalie", "junkie", "lassie", "tie", "pie", "lie", "die"
}


def singular(noun):
    """A grouping key for a countable noun, so a plural and its singular
    collapse together. Inverse of plural().

    Handles regular English noun shapes. Irregulars (children, people)
    are left alone.
    """
    n = noun.lower()
    if n in INVARIANT_OR_S_SINGULARS or n in IE_SINGULAR_NOUNS:
        return n
    if n.endswith("ies") and len(n) > 4:
        if n[:-1] in IE_SINGULAR_NOUNS:
            return n[:-1]
        return n[:-3] + "y"
    if n.endswith(("sses", "shes", "ches", "xes", "zes")):
        return n[:-2]
    if n.endswith("ses") and len(n) > 4 and n[:-2] in INVARIANT_OR_S_SINGULARS:
        return n[:-2]
    if n.endswith("s") and not n.endswith("ss"):
        return n[:-1]
    return n

