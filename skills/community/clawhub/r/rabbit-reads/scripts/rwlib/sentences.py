#!/usr/bin/env python3
"""
Sentence and word segmentation.

English only, and deliberately so. The abbreviation list, the capital-letter
initial rule, the syllable heuristic, and the word pattern are all calibrated on
English orthography. rwlib.language.note exists so a caller can say that out
loud instead of silently reporting nonsense, and rwlib.language.measure is the
number it says it with.

Stdlib only, 3.9+.
"""

import re

# Stands in for a period that must not end a sentence, for the length of one
# split. A NUL cannot occur in a document a person edits, which is the whole
# requirement: the last step of split_sentences turns every sentinel back into a
# period, so a sentinel that a writer could legitimately have typed would be a
# silent rewrite of the copy being measured. It used to be U+2024 ONE DOT
# LEADER, which is a real character with real uses.
SENTENCE_SENTINEL = "\x00"

ABBREV_RX = re.compile(
    r"\b(Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|etc|vs|approx|dept|est|vol|Inc|Ltd|Fig|No)\.",
    re.I,
)

WORD_RX = re.compile(r"[A-Za-z][A-Za-z'\-]*")

# A closer allowed between the terminal mark and the split: `said "no." Then`
# and `(finally!) The` both end a sentence with a quote or paren after the
# mark, not before it. Python's lookbehind has to be fixed-width, so this is
# two lookbehinds of different widths joined by alternation rather than one
# variable-width assertion.
_CLOSER = "[\"'\u2019\u201d\\)\\]]"
SENTENCE_SPLIT_RX = re.compile(
    r"(?:(?<=[.!?])|(?<=[.!?]" + _CLOSER + r"))[\s\n]+")

# A forced boundary at the start of every list item, on the SENTENCE_SENTINEL-
# protected text below (so a numbered marker's own period, already turned into
# a sentinel by the substitution two lines down, is matched by its sentinel
# form rather than by a literal period). Without this, a bulleted list with no
# terminal punctuation on any item reads as one sentence spanning the whole
# list: nothing here ends in [.!?], so SENTENCE_SPLIT_RX never fires between
# items. The words themselves are still counted (markdown.strip_for_stats
# keeps list text on purpose), only the sentence-length shape was wrong.
_LIST_BOUNDARY_RX = re.compile(
    r"(?m)(?=^\s*(?:[-*+]\s|\d+\)\s|\d+" + SENTENCE_SENTINEL + r"))")


def split_sentences(text):
    """Sentences, with the periods that are not sentence ends held back."""
    text = text.replace(SENTENCE_SENTINEL, "")
    protected = ABBREV_RX.sub(
        lambda m: m.group(0).replace(".", SENTENCE_SENTINEL), text)
    # Every single-capital-and-period is protected, not only the ones followed
    # by another capital. Requiring a following capital splits "the U. of
    # Texas" into two sentences, and it does not buy the case it looks like it
    # would: "the grade was A. Then we left" is followed by a capital too, so
    # it stays glued either way. Sentence lengths feed every stored
    # fingerprint, so a change here is a fingerprint schema change.
    protected = re.sub(r"\b([A-Z])\.", r"\1" + SENTENCE_SENTINEL, protected)
    protected = re.sub(r"(?m)^\s*(\d+)\.", r"\1" + SENTENCE_SENTINEL, protected)
    parts = []
    for chunk in _LIST_BOUNDARY_RX.split(protected):
        if chunk:
            parts.extend(SENTENCE_SPLIT_RX.split(chunk))
    return [p.replace(SENTENCE_SENTINEL, ".").strip() for p in parts if p.strip()]


def tokenize(text):
    return WORD_RX.findall(text.lower())


def syllables(word):
    word = re.sub(r"[^a-z]", "", word.lower())
    if not word:
        return 0
    groups = re.findall(r"[aeiouy]+", word)
    n = len(groups)
    if word.endswith("e") and n > 1 and not word.endswith(("le", "ee", "ye")):
        n -= 1
    return max(n, 1)
