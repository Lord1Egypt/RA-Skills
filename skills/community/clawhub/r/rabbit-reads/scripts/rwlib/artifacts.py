#!/usr/bin/env python3
"""
Paste artifacts and concealment channels: what survives a copy out of a chat
window, and what somebody puts in a file so a reader cannot see it.

These are facts about how a file was produced rather than about what it says,
which is why three different scripts need the same table. scan.py reports them,
fixes.py removes the ones it is allowed to remove, and verify.py grants the
removal a carve-out so a rewrite that strips one still passes preservation.

The concealment half is the difference between an accident and a payload. A
zero-width space is residue; a run of Unicode tag characters is a message
written to be read by a machine and missed by a person. Both live here because
both are invisible, but the tables keep them apart: what is safe to delete is
not the same question as what is worth reporting.

Written as escapes, never as the characters themselves. As literals these keys
are invisible: two that look identical in an editor merge into one and a check
disappears without a word, and any tool that normalizes whitespace can turn the
U+00A0 key into a plain space, at which point the counter reads every space in
every document as a paste artifact. The test suite pins the exact codepoints, so
a normalizing save fails the build instead of the scan.

Stdlib only, 3.9+.
"""

import re
import unicodedata

from .lexicon import pattern_source

HIDDEN_UNICODE = {
    "\u200b": "zero-width space",
    "\u200c": "zero-width non-joiner",
    "\u200d": "zero-width joiner",
    "\u2060": "word joiner",
    "\ufeff": "byte-order mark",
    "\u00ad": "soft hyphen",
    "\u00a0": "non-breaking space",
    "\u202f": "narrow no-break space",
    "\u180e": "mongolian vowel separator",
    "\u2061": "invisible function application",
    "\u2062": "invisible times",
    "\u2063": "invisible separator",
    "\u2064": "invisible plus",
}

# The invisible characters above have no honest use in prose, so one occurrence
# is a paste artifact and a P0. The two space-like ones are different: a
# non-breaking space is correct French typography, correct in front of a unit,
# and correct in a name that must not wrap. Calling those a credibility killer
# fails documents that were typeset properly, so they report at P2 and only once
# there are enough of them to look mechanical.
SPACE_LIKE_UNICODE = frozenset({"\u00a0", "\u202f"})
SPACE_LIKE_TOLERANCE = 3

# Everything safe to delete outright, because it carries no meaning at all.
ZERO_WIDTH = {ch: name for ch, name in HIDDEN_UNICODE.items()
              if ch not in SPACE_LIKE_UNICODE}

# One exception to "no honest use". A zero-width joiner between two pictographs
# is the emoji: U+1F468 ZWJ U+1F4BB is the man-technologist glyph, and family
# and profession emoji are all built this way. Deleting it does not clean the
# document, it silently replaces one emoji with two, and reporting it calls an
# ordinary README a paste artifact. One of the trending READMEs in the corpus
# tripped this. Written as an escape, like every key above, and for the same
# reason: as a literal it is invisible and a normalizing save deletes the check.
ZWJ = "\u200d"


def _pictographic(ch):
    # No unicodedata category covers "emoji", so this is the ranges that matter:
    # the pictograph blocks, the miscellaneous symbols, and the variation
    # selector and skin-tone modifiers that attach to them.
    point = ord(ch)
    return (0x1F000 <= point <= 0x1FAFF or 0x2600 <= point <= 0x27BF
            or 0xFE0E <= point <= 0xFE0F or 0x1F3FB <= point <= 0x1F3FF
            or point in (0x2640, 0x2642, 0x00A9, 0x00AE, 0x2122))


def load_bearing_zwj(text, index):
    """True when the character at `index` is a joiner inside an emoji sequence.

    Deliberately narrow: both neighbours have to be pictographic. A joiner
    between two letters is still the paste artifact it has always been, which is
    the case this table exists for.
    """
    if text[index] != ZWJ:
        return False
    if index == 0 or index + 1 >= len(text):
        return False
    return _pictographic(text[index - 1]) and _pictographic(text[index + 1])


def occurrences(text, ch):
    """Offsets of every `ch` that counts as a paste artifact.

    The one shared definition of "how many are in here". scan.py reports off it
    and fixes.py thresholds off it, because the two used to count differently:
    the scan saw the whole file and the fixer saw only the spans it was allowed
    to edit, so a document could be reported and then neither fixed nor
    explained. Emoji joiners are excluded here rather than at either caller.
    """
    if ch not in text:
        return []
    out, index = [], text.find(ch)
    while index != -1:
        if not load_bearing_zwj(text, index):
            out.append(index)
        index = text.find(ch, index + 1)
    return out

# The concealment tables. Everything below is reported and never auto-deleted,
# except where a comment says otherwise: these are the characters somebody uses
# on purpose, and the right response to a payload is showing it to the user,
# not quietly editing it away.

# Directional formatting. The overrides and embeds can make rendered text read
# differently from its logical order, which is the Trojan Source trick, and an
# override in an English document has no honest explanation. The two marks are
# different: LRM and RLM are correct typography in mixed-script text, so they
# get the same courtesy the non-breaking space gets above, a tolerance before
# anything is said. None of these are ever stripped. Removing them from a
# legitimate RTL document breaks its rendering, and the fixer cannot tell a
# legitimate document from an attack; a human can.
REPORT_ONLY_UNICODE = {
    "\u202a": "left-to-right embedding",
    "\u202b": "right-to-left embedding",
    "\u202c": "pop directional formatting",
    "\u202d": "left-to-right override",
    "\u202e": "right-to-left override",
    "\u2066": "left-to-right isolate",
    "\u2067": "right-to-left isolate",
    "\u2068": "first strong isolate",
    "\u2069": "pop directional isolate",
    "\u061c": "arabic letter mark",
    "\u200e": "left-to-right mark",
    "\u200f": "right-to-left mark",
    "\ufff9": "interlinear annotation anchor",
    "\ufffa": "interlinear annotation separator",
    "\ufffb": "interlinear annotation terminator",
    "\u115f": "hangul choseong filler",
    "\u1160": "hangul jungseong filler",
    "\u3164": "hangul filler",
    "\uffa0": "halfwidth hangul filler",
    "\u2800": "braille pattern blank",
}

# Per-character allowances, same shape as SPACE_LIKE_TOLERANCE: enough LRM or
# RLM for real mixed-script typography, enough braille blanks for the alignment
# art some READMEs draw with them. Past the allowance they report, softly. A
# character in REPORT_ONLY_UNICODE and not in this dict reports on the first
# occurrence.
REPORT_ONLY_TOLERANCE = {
    "\u200e": 3,
    "\u200f": 3,
    "\u2800": 3,
}

# The Unicode tag block, U+E0001 and U+E0020 through U+E007F: a full invisible
# copy of ASCII. This is the ASCII-smuggling channel, whole instructions
# written where only a tokenizer will read them, and there is no prose reason
# for even one. Safe to strip: deleting them changes nothing any renderer
# shows.
TAG_RX = re.compile("[\U000e0001-\U000e007f]")
TAG_NAME = "unicode tag character"

# Variation selectors, minus the two emoji presentation selectors. Each one
# encodes a selectable byte, which makes a run of them a data channel, and
# outside CJK ideograph variation sequences they do not occur in prose. FE0E
# and FE0F are deliberately not in the class: they are how ordinary text asks
# for text or emoji presentation, they follow half the emoji ever pasted, and
# flagging them would call every second emoji a payload. The cost is a
# two-character channel left open, which is too narrow to carry a prompt.
VS_RX = re.compile("[\ufe00-\ufe0d\U000e0100-\U000e01ef]")
VS_NAME = "variation selector"


def range_occurrences(text, rx):
    """Offsets of every match of a character-class regex. The range analogue of
    occurrences(): one finding per class, not one per distinct codepoint, so a
    smuggled sentence reports as one thing and not thirty."""
    return [m.start() for m in rx.finditer(text)]


# Everything named above, for the sweep below to skip.
_KNOWN_INVISIBLES = frozenset(HIDDEN_UNICODE) | frozenset(REPORT_ONLY_UNICODE)

# The controls a text file is allowed to contain. Form feed is not in the set:
# it is invisible in most renderers and has no place in markdown.
_ALLOWED_CONTROLS = frozenset("\t\n\r")


def unlisted_invisibles(text):
    """Format and control characters nothing above names, as {char: offsets}.

    The tables are a list of known channels, and a list is only as good as its
    last update. This is the backstop: one pass over the text flagging any
    Unicode format character (category Cf) or control (Cc) that is not already
    in a table, so the next smuggling trick surfaces as "unexpected format
    character" instead of passing clean until somebody adds a dict entry.
    Escape characters land here too, which covers ANSI terminal injection in a
    document an agent might cat.
    """
    out = {}
    for index, ch in enumerate(text):
        if " " <= ch <= "~" or ch in _ALLOWED_CONTROLS:
            continue
        if ch in _KNOWN_INVISIBLES or TAG_RX.match(ch) or VS_RX.match(ch):
            continue
        if unicodedata.category(ch) in ("Cf", "Cc"):
            out.setdefault(ch, []).append(index)
    return out


# Tracking parameters an AI tool appends to a link it hands out. Anchored, so
# only a whole query parameter matches and a URL that happens to contain the
# substring elsewhere is left alone.
#
# Built from lexicon.json's "ai-utm" pattern rather than typed out a second
# time: that entry is what scan.py reports a finding off, this is what
# norm_url actually rewrites, and the two used to carry the same provider
# list independently, which is exactly the drift this repo's own "one home
# per fact" convention exists to forbid. `\Z` is added here because this
# pattern's job is narrower than the detector's: it has to match nothing but
# a complete query parameter, never a substring inside one.
AI_PARAM_RX = re.compile(pattern_source("ai-utm") + r"\Z")


def norm_url(url):
    """The URL with AI tracking parameters dropped and the query rebuilt.

    Shared by the fixer, which produces this string, and the verifier, which has
    to accept it. One function, so a fixed URL cannot fail the verification the
    fixer runs on its own output.
    """
    if "?" not in url:
        return url
    base, _, rest = url.partition("?")
    query, hash_sep, fragment = rest.partition("#")
    kept = [p for p in query.split("&") if p and not AI_PARAM_RX.match(p)]
    out = base + ("?" + "&".join(kept) if kept else "")
    # A bare trailing "#" is kept. Dropping it makes a URL that ends in an empty
    # fragment compare unequal to the identical URL on the other side, which is
    # a violation nobody caused.
    return out + hash_sep + fragment
