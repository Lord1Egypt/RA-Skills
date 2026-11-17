#!/usr/bin/env python3
"""
Is this English? A warning, never a gate.

Every calibrated number in this engine is calibrated on English. The tier lists
are English words, the contraction and abbreviation rules are English
orthography, the sentence splitter breaks on English terminal punctuation, and
the burstiness and type-token bands come from studies of English prose. Run it
over Japanese or Arabic and it will still print numbers. They will not mean
anything.

So the tool says so. It does not refuse: a bilingual README with an English
quickstart is a real document that deserves a real answer for the English half,
and a checker that hard-fails on a Chinese heading is a checker people delete
from CI. The rule this module implements is: flag, do not fail.

The measure is the share of letters that are ASCII. That is a coarse instrument
and it is chosen on purpose over anything cleverer. It cannot tell English from
French, it counts a transliterated name against you, and it has nothing to say
about a document that is mostly numbers. What it does reliably is notice a
non-Latin script, which is the case where the output is worthless rather than
merely imprecise, and being wrong about French costs a note nobody has to act
on.

Stdlib only, 3.9+.
"""

import re

from .markdown import (FENCE_RX, HEADING_LINE_RX, INLINE_CODE_RX, TABLE_ROW_RX,
                       URL_GREEDY_RX, blank_all)

# Below this share of ASCII letters, the calibration is being applied to a
# language it was not measured on. Set where a Latin-script European language
# lands comfortably above it: accented French and German prose runs about 0.95
# ASCII letters, and a document in a non-Latin script runs near zero. There is
# nothing in between worth splitting hairs over.
ASCII_LETTER_FLOOR = 0.85

# Fewer letters than this and the ratio is noise. A three-line fragment with one
# accented name in it is not a Portuguese document.
MIN_LETTERS = 200

ASCII_LETTER_RX = re.compile(r"[A-Za-z]")


def measure(text):
    """(ratio, letters) over the prose, or (None, letters) when there is too
    little of it to say anything.

    Code, inline code, tables, headings, and URLs come out first. An identifier
    is ASCII whatever language the document is written in, and a page of Python
    would drag any Japanese README over the floor and silence the warning on
    exactly the documents that need it.
    """
    prose = blank_all(text, FENCE_RX, INLINE_CODE_RX, TABLE_ROW_RX,
                      HEADING_LINE_RX, URL_GREEDY_RX)
    letters = [c for c in prose if c.isalpha()]
    if len(letters) < MIN_LETTERS:
        return None, len(letters)
    ascii_letters = sum(1 for c in letters if ASCII_LETTER_RX.match(c))
    return ascii_letters / len(letters), len(letters)


def note(text, floor=ASCII_LETTER_FLOOR):
    """A one-line warning, or None when the document reads as English.

    Returned as text rather than as a finding on purpose. A finding has a
    priority and a line number and belongs in a list somebody is expected to
    work through; this is a caveat on the whole report.
    """
    ratio, letters = measure(text)
    if ratio is None or ratio >= floor:
        return None
    return ("%.0f%% of the letters in this document are not ASCII. Every band, "
            "tier list, and sentence rule in this engine is calibrated on "
            "English, so the numbers below describe the English parts and "
            "guess at the rest. Nothing here is a verdict on non-English prose."
            % ((1 - ratio) * 100))
