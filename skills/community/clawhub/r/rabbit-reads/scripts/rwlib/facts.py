#!/usr/bin/env python3
"""
The facts a paraphrase corrupts silently: numbers, dates, and quotations.

SKILL.md's first guardrail is "never invent facts", and until this module it was
prompt-only. `verify.py` proved a rewrite had not touched a code fence or a
table and said nothing about the sentence that turned 3,200 into 3,000. Numbers
and dates are exactly where a paraphrase goes wrong without looking wrong, and
they are the cheap half to check.

**Everything here canonicalizes before it compares.** That is the whole design.
A conversion under a `date_format: dmy` profile is *instructed* to rewrite
"September 12, 2025" as "12 September 2025", and a checker that reported it
would be failing the edit the skill asked for. So a date compares as its ISO
form, a percent compares the same whether it is spelled or signed, a range is
one token rather than two numbers, and a version is an identifier rather than
three. Each carve-out was sized against the 100-README corpus before it was
written, and the size is in the comment beside it.

Extraction is ordered and each pass eats its span, so nothing is counted twice.
Dates go first and are consumed without being emitted here, because `dates()`
owns them: left in, "September 12, 2025" would also contribute 12 and 2025 to
the number multiset, and reformatting the date would read as two numbers
changing.

The two directions are not symmetric, and that is a decision rather than an
oversight. A number in the source and missing from the rewrite is a fact that
left the document. A number in the rewrite and not in the source usually is not
an invention: a rewrite that turns "the last two years" into "2024 and 2025" is
deriving a number the source carried. Both are reported. Only the first fails,
and `verify.py` is where that is enforced.

Spelled numbers are not tracked at all. "three" against "3" is a style edit a
profile can legitimately require in either direction, and matching them would
turn this into a second lexicon. That is the known residual and it is
documented rather than papered over.

Named entities are here and are report-only, forever. A capitalized-run regex
cannot tell a product name from the first word of a sentence, and set-equality
on it would fail every rewrite that splits a sentence at a capital. What it is
good for is a list a person reads, which is why nothing in this plugin gates on
it.

The date patterns used to live in scan.py. They moved here because verify.py
needs them and must not import scan.py, which lazily imports verify. scan.py
keeps its own names as aliases onto these, the way it already aliases
`TABLE_RX` onto `rwlib.markdown.TABLE_ROW_RX`.

Every non-ASCII character in this file is written as an escape, never as a
literal. A curly apostrophe and an en dash both survive a copy and both are
silently rewritten by anything that normalizes the source, at which point the
alternative they sit in stops matching and the line still looks correct.

Stdlib only, 3.9+.
"""

import re

from .markdown import CURLY_APOSTROPHE

MONTH_NAMES = ("January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December")
MONTHS = {name.lower(): i for i, name in enumerate(MONTH_NAMES, 1)}

_MONTH_ALT = "|".join(MONTH_NAMES)

EN_DASH = "\u2013"
EM_DASH = "\u2014"

# Moved verbatim from scan.py, where `voice-date-format` still reads them
# through the aliases there. Changing one of these changes a voice rule, so
# they are one definition rather than two. The groups are new: scan.py only
# ever needed group(0), and this module needs the parts to build an ISO form.
DATE_US_RX = re.compile(r"\b(%s)\s+(\d{1,2}),?\s+(\d{4})\b" % _MONTH_ALT)
DATE_DMY_RX = re.compile(r"\b(\d{1,2})\s+(%s)\s+(\d{4})\b" % _MONTH_ALT)
DATE_ISO_RX = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")

# A version is an identifier that happens to be punctuated like arithmetic.
# Left to the bare-number pass, `v1.2.3` decomposes into 1.2 and 3, and a
# rewrite that writes it without the `v` reads as two facts changing. Largest
# single carve-out over the corpus: 789 of 5,780 prose numbers, 14%.
#
# The two lookbehinds guard the one shape that carve-out never covered: a bare
# `12.5` still reads as a version by default, calibrated behaviour this repo's
# own corpus measurement backs, but `$3,200.50` does not, and without a guard
# the version pass claims its `.50` tail as `200.50` before PERCENT_RX or the
# comma-grouped number pass ever sees it, splitting one fact ($3,200.50) into
# a fabricated version number plus a stray `3,`. `(?<!\$)` catches the
# no-comma case (`$12.5`), `(?<!,)` catches the tail of a comma-grouped one.
VERSION_RX = re.compile(r"(?<!\$)(?<!,)\bv?\d+\.\d+(?:\.\d+)*\b")

# "10-20%", "10 to 20 percent". One fact with two numbers in it, and the two
# spellings are the same fact. 403 over the corpus, 7%.
#
# Three guards, and every one of them was put here by a false positive the
# 100-README corpus produced:
#
#   The dash form is spaceless and the word form is spaced. `verify.py`'s
#   existing carve-out is already "an en dash between digits", spaceless, and a
#   spaced dash between two numbers is prose far more often than it is a range.
#   `**2026 - 1,237 contributions**` is the case: read as a range it also
#   fragmented the 1,237.
#
#   No em dash, for the same reason. An em dash between numbers is a sentence.
#
#   Both endpoints carry comma groups and a boundary on each side, so a range
#   cannot begin or end in the middle of a number. Without the trailing guard,
#   `1,000-2,000` matched "000-2" and left a stray 1 and 000 behind.
RANGE_RX = re.compile(
    r"(?<![\w.,$-])(\d+(?:,\d{3})*(?:\.\d+)?)"
    r"(?:[-%s]|\s+to\s+)"
    r"(\d+(?:,\d{3})*(?:\.\d+)?)(?![\d,])\s*(%%|percent\b)?" % EN_DASH)

# A percent-encoded URL escape is not a percentage. A markdown link to a
# non-ASCII anchor, `(#%E5%AD%97%E5%B9%95)`, is not a URL by URL_RX and survives
# the blanking, and PERCENT_RX then reads `97%` out of `%AD%97%E5`. Consumed
# first and never emitted, the way dates are. Three corpus documents, all
# Chinese-language READMEs with anchor links.
PERCENT_ENCODED_RX = re.compile(r"(?:%[0-9A-Fa-f]{2})+")

# "20%", "20 %", "20 percent". 224 over the corpus.
PERCENT_RX = re.compile(r"\b(\d+(?:\.\d+)?)\s*(?:%|percent\b)")

# "1st" and "1" are one number wearing two hats. Needs its own pass: NUMBER_RX's
# trailing lookahead refuses a digit followed by a letter, so an ordinal would
# otherwise not be counted at all.
ORDINAL_RX = re.compile(r"\b(\d+)(?:st|nd|rd|th)\b")

# What is left once the passes above have eaten their spans. Thousands
# separators are matched so canonical_number can take them out: 62 comma-grouped
# numbers over the corpus.
#
# Both guards are narrower than the obvious spelling, and both were widened by a
# corpus false positive:
#
#   The lookbehind rejects a comma, so a rejected `1,000` cannot re-match as
#   `000`. It does *not* reject `$`: money is a fact a reader reads, and
#   excluding the symbol made `$1,000` match only its tail and report a 0.
#
#   The lookahead rejects a decimal point only when a digit follows it, because
#   the version and range passes have already eaten every real decimal and what
#   is left is the full stop at the end of a sentence. Rejecting a bare `.`
#   dropped every sentence-final number in the corpus.
NUMBER_RX = re.compile(
    r"(?:(?<=[\s(\[{])|^)-?(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)(?![\w,]|\.\d)"
    r"|(?<![\w.,-])(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)(?![\w,]|\.\d)")

# Quotations, straight or curly, at this many words or more. The floor is what
# separates a quotation from a scare-quoted term: `"robust"` is a word the
# rewrite may legitimately replace, and a four-word span is somebody's sentence.
# 337 qualifying spans over the corpus, median 1 per document, 32 documents with
# none.
try:
    from .markdown import QUOTED_RX
except ImportError:
    from markdown import QUOTED_RX

QUOTED_MIN_WORDS = 4

# A capitalized run, for the report-only entity list. Deliberately crude: it
# feeds a list somebody reads and never a comparison anything fails on, so
# precision buys nothing and a missing name costs one line in a report.
ENTITY_RX = re.compile(r"\b[A-Z][a-zA-Z0-9]*(?:[ -][A-Z][a-zA-Z0-9]*)*\b")

# What sits in front of a sentence-initial capital, which is most of what
# ENTITY_RX matches and none of what it is for. Read off a short window behind
# the match rather than by searching from the start of the document, which is
# quadratic and shows up the moment this runs over a corpus.
_LEAD_RX = re.compile(r"(?:^|[.!?:]\s+|\n\s*(?:[-*+>#]+\s*)?"
                      r"|\n\s*\d+[.)]\s*)$")
_LEAD_WINDOW = 12


def canonical_number(raw):
    """One spelling per numeric fact.

    "1,200", "1200" and "1200.0" are one number. A trailing zero goes because a
    rewrite that writes 1200 where the source wrote 1200.0 changed the
    formatting and not the fact, and this check exists for the one that changed
    the fact.
    """
    body = raw.replace(",", "").strip()
    try:
        value = float(body)
    except ValueError:
        return body
    if value == int(value) and abs(value) < 1e15:
        return str(int(value))
    return repr(value)


def _iso(year, month, day):
    return "%04d-%02d-%02d" % (int(year), int(month), int(day))


def _date_matches(text):
    """(start, end, iso, raw) for every date, in all three spellings."""
    out = []
    for m in DATE_US_RX.finditer(text):
        out.append((m.start(), m.end(),
                    _iso(m.group(3), MONTHS[m.group(1).lower()], m.group(2)),
                    m.group(0)))
    for m in DATE_DMY_RX.finditer(text):
        out.append((m.start(), m.end(),
                    _iso(m.group(3), MONTHS[m.group(2).lower()], m.group(1)),
                    m.group(0)))
    for m in DATE_ISO_RX.finditer(text):
        out.append((m.start(), m.end(), m.group(0), m.group(0)))
    return out


def dates(text):
    """[(iso, raw)] for every date in any of the three formats.

    Compared as ISO on purpose. A `date_format` profile instructs the rewrite to
    move a date between spellings, and a checker that failed that would be
    failing the edit the skill asked for. A date whose *value* moved still
    fails, which is the case worth catching.
    """
    return [(iso, raw) for _, _, iso, raw in _date_matches(text)]


def _blank_spans(text, spans):
    """`text` with `spans` replaced by spaces, so offsets do not move.

    The device rwlib.markdown.blank uses, and for the same reason: a later pass
    has to see a hole where an earlier pass took its span, at the same offset,
    or every position downstream moves.
    """
    if not spans:
        return text
    out = list(text)
    for start, end in spans:
        for i in range(start, min(end, len(out))):
            if out[i] != "\n":
                out[i] = " "
    return "".join(out)


def numbers(text):
    """[(canonical, raw)] for every numeric fact a reader reads.

    Ordered passes, each consuming its span so a later one never sees it. The
    order carries the argument: dates are eaten first and never emitted, because
    `dates()` owns them and a reformatted date must not read as two numbers
    moving. A range is claimed before its two endpoints, and a percent before
    the version pass, because VERSION_RX's own decimal shape is a strict
    subset of both: unclaimed, `10-20%` fragments into a range plus a stray
    `20` read as a version, and `12.5%` (or `12.5 percent`) loses its percent
    sign entirely to a version number that was never there. A version still
    has to be claimed before the bare-decimal pass beneath it.
    """
    out = []
    # Consumed and never emitted: a date is dates()' fact, and a percent-encoded
    # escape is not a number at all.
    spans = [(s, e) for s, e, _, _ in _date_matches(text)]
    spans.extend((m.start(), m.end())
                 for m in PERCENT_ENCODED_RX.finditer(text))

    def take(rx, canon):
        blanked = _blank_spans(text, spans)
        found = list(rx.finditer(blanked))
        for m in found:
            out.append((canon(m), m.group(0).strip()))
        spans.extend((m.start(), m.end()) for m in found)

    take(RANGE_RX, lambda m: "range:%s-%s%s"
         % (canonical_number(m.group(1)), canonical_number(m.group(2)),
            "%" if m.group(3) else ""))
    take(PERCENT_RX, lambda m: canonical_number(m.group(1)) + "%")
    take(VERSION_RX, lambda m: "version:" + m.group(0).lstrip("vV"))
    take(ORDINAL_RX, lambda m: canonical_number(m.group(1)))
    take(NUMBER_RX, lambda m: canonical_number(m.group(0)))
    return out


def quoted(text):
    """[normalized] for every quoted span of QUOTED_MIN_WORDS or more.

    Whitespace collapsed and curly apostrophes straightened, because a rewrite
    that reflowed a paragraph, or ran through an editor that curls typography,
    did not change the quotation. Curling has its own P2 elsewhere and does not
    need a second reporter.
    """
    out = []
    for m in QUOTED_RX.finditer(text):
        body = next((g for g in m.groups() if g is not None), "")
        body = " ".join(body.replace(CURLY_APOSTROPHE, "'").split())
        if len(body.split()) >= QUOTED_MIN_WORDS:
            out.append(body)
    return out


def entities(text):
    """Capitalized runs, minus the ones a sentence boundary explains.

    Report-only, forever. This cannot tell a product name from the first word of
    a sentence, and nothing in this plugin gates on it. It is a list a person
    reads when a rewrite looks like it dropped a name, and the cost of a wrong
    entry is that they ignore one line.
    """
    out = []
    for m in ENTITY_RX.finditer(text):
        if _LEAD_RX.search(text[max(0, m.start() - _LEAD_WINDOW):m.start()]):
            continue
        token = m.group(0)
        if len(token) < 2:
            continue
        out.append(token)
    return out
