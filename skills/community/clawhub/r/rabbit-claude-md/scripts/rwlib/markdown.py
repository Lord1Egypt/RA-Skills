#!/usr/bin/env python3
"""
Markdown spans, one definition each.

Everything in this plugin that has to tell prose from markup reads its patterns
from here. Three scripts used to carry their own copies, with comments asking
the next reader to keep them in sync by hand, and the copies drifted anyway:
the badge host lists disagreed, LINK_RX blanked images in one file and not in
another, and two heading patterns matched different spans. A comment is not a
mechanism. This module is.

Blanking, never deleting. Every blank_* and strip_* function here replaces a
span with the same number of characters, so an offset taken from the blanked
copy still points at the same place in the original. Most callers report line
numbers out of a copy they blanked, and preserving length is what makes that
legal. tests/test_invariants.py checks the property rather than trusting the
comment.

Stdlib only, 3.9+.
"""

import html
import re

from .artifacts import HIDDEN_UNICODE, REPORT_ONLY_UNICODE, SPACE_LIKE_UNICODE
from .artifacts import TAG_RX as _TAG_RX
from .artifacts import VS_RX as _VS_RX

CURLY_APOSTROPHE = "\u2019"

# --------------------------------------------------------------------------
# code and literal spans
# --------------------------------------------------------------------------

# The fence as one span, for blanking. Non-greedy to the next line that opens
# with a run of the same fence character.
#
# Two self-contained alternatives rather than one alternation over both
# characters. Written as `(?:`{3,}|~{3,})` at each end, an unterminated `~~~`
# closes against the next ``` fence and everything between them -- ordinary
# prose -- is blanked out of every counter in the engine.
#
# The opening run is captured and backreferenced at the close, with `*` after
# it rather than nothing, because CommonMark requires the closing fence be at
# least as long as the opening one and not the same length: an opener of 4
# backticks may still close on a run of 5. Without the backreference a 3-tick
# closer inside a 4-tick fence's body (a nested fenced example, say) ended the
# span early and blanked the wrong text: everything from the real 4-tick
# closer onward stayed unblanked and reached every counter in the engine as
# prose.
FENCE_RX = re.compile(
    r"^[ \t]*(?:(`{3,}).*?(?:^[ \t]*\1`*|\Z)|(~{3,}).*?(?:^[ \t]*\2~*|\Z))", re.M | re.S)
OPEN_FENCE_RX = re.compile(r"^[ \t]*(?:`{3,}|~{3,})", re.M)
# The same fences taken apart, for the corpus study, which counts languages and
# body lines. Two patterns because they answer two questions, not because
# anybody forgot to merge them: this one does not anchor to the line start, so
# it must never be used for blanking.
FENCE_PARTS_RX = re.compile(r"```(\w*)\n(.*?)```", re.S)
# A code span in CommonMark's shape: a run of N backticks opens, the next run
# of exactly N closes, and shorter runs between them are content. The old
# single-backtick pattern paired the wrong marks inside a doubled span, so a
# ban entry quoted as (`` `word` ``) blanked two space fragments and left the
# word itself exposed to the rule it was illustrating. Content still may not
# cross a line break: an unpaired backtick must not blank a paragraph, the same
# containment the quote pairs above insist on.
INLINE_CODE_RX = re.compile(r"(?<!`)(`+)(?!`)(?:(?!\1)[^\n])+?\1(?!`)")
FRONTMATTER_RX = re.compile(r"\A---\n(.*?)\n---\n", re.S)
TABLE_ROW_RX = re.compile(r"(?m)^\s*\|.*\|\s*$")
TABLE_SEP_RX = re.compile(r"(?m)^\|?[\s:|-]+\|[\s:|-]+\|?\s*$")
BLOCKQUOTE_RX = re.compile(r"(?m)^\s*>.*$")

# Heading, with the marker and the text captured and the trailing whitespace
# eaten. The whole line, not just the hashes: stripping the marker alone leaves
# heading text carrying no terminal punctuation, so a sentence splitter glues it
# onto the first sentence of the section below and every section opener measures
# two or three words too long.
HEADING_RX = re.compile(r"(?m)^(#{1,6})\s+(.*?)\s*$")
# The same span with nothing captured, for callers that only want it gone.
HEADING_LINE_RX = re.compile(r"(?m)^#{1,6}\s+.*$")

LIST_ITEM_RX = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")

# Each quote pair has to close with its own kind. A single alternation over both
# the opening and the closing marks lets one stray straight quote pair with a
# curly one up to 400 characters later, and every word between them stops being
# scored.
LEFT_DOUBLE = "“"
RIGHT_DOUBLE = "”"
LEFT_SINGLE = "‘"
RIGHT_SINGLE = "’"

_QUOTE_PAIRS = (('"', '"'), (LEFT_DOUBLE, RIGHT_DOUBLE), (LEFT_SINGLE, RIGHT_SINGLE))
# A line break inside a quotation is allowed and a blank line is not. Markdown
# prose is hard-wrapped as often as not, and a rewrite rewraps it: refusing any
# newline meant a quotation that moved across a line boundary vanished from
# facts.quoted's multiset and read as a quotation removed. A blank line still
# ends the span, because an unclosed quote mark would otherwise swallow the
# rest of the document up to the 400-character ceiling.
#
# There is no lower bound, and that is the load-bearing half. A straight quote
# closes with the same character it opens with, so pairing is positional: skip
# one well-formed pair and every quote after it on the paragraph pairs with the
# wrong neighbour. A `{4,400}` floor did exactly that. `("No.")` holds three
# characters, fell under the floor, and its *closing* quote then opened a
# 220-character span that ran to the opening quote of the next real quotation
# and ate it, which left `circle back"` scored as prose and raised a banned
# phrase against a document that was only naming the phrase as an example.
# Length is a judgement about a matched span, not about where one ends, so the
# callers that want a floor apply their own: facts.quoted has QUOTED_MIN_WORDS.
# The curly right-single mark closes a quotation and spells an apostrophe, and
# those are the same character. A genuine closing quote is never immediately
# followed by a letter and an apostrophe always is, which is the distinction
# both halves of this fix turn on. `_closer_guard` refuses a "closer" that
# looks like an apostrophe. `_content_class` is the half that also has to
# change: without it, the mark inside "It's" is excluded from content the
# same as a real closer, the greedy match cannot skip past it either way, and
# `'It's a test'` matched nothing at all rather than the whole quotation.
# Letting the mark back into content, but only when a letter follows, keeps
# the positional pairing the module docstring above describes: a mark that is
# NOT followed by a letter still ends the span, exactly as before. Neither
# guard applies to the other two pairs in _QUOTE_PAIRS, and there is no
# straight-single-quote pair here to carry the same problem: `'` is ASCII
# apostrophe and closing quote both, and _QUOTE_PAIRS never pairs it with
# itself for exactly that reason.
def _closer_guard(b):
    return r"(?![A-Za-z])" if b == RIGHT_SINGLE else ""


def _content_class(a, b):
    base = r"[^%s%s\n]" % (re.escape(a), re.escape(b))
    if b == RIGHT_SINGLE:
        return r"(?:%s|%s(?=[A-Za-z]))" % (base, re.escape(b))
    return base


QUOTED_RX = re.compile(
    "|".join("%s((?:%s|\\n(?![ \\t]*\\n)){0,400})%s%s"
             % (re.escape(a), _content_class(a, b), re.escape(b),
                _closer_guard(b))
             for a, b in _QUOTE_PAIRS))
CURLY_QUOTE_RX = re.compile("[“”‘’]")

# --------------------------------------------------------------------------
# HTML character references
# --------------------------------------------------------------------------

# Named, decimal, and hex character references. The lengths are bounded so a
# stray `&` in prose followed half a paragraph later by a semicolon is not read
# as one entity swallowing the sentence between them. 31 is HTML5's longest
# named reference (`CounterClockwiseContourIntegral`) plus room.
HTML_ENTITY_RX = re.compile(
    r"&(?:#\d{1,7}|#[xX][0-9a-fA-F]{1,6}|[A-Za-z][A-Za-z0-9]{1,31});")

# The dashes again, spelled as character references. A document written with
# `&mdash;` renders an em dash, reads as an em dash, and is an em dash to every
# reader, so it has to be one to the counter as well. Left out, a voice that
# forbids em dashes was a find-and-replace away from passing, and verify.py's
# "no em dashes added" gate let a rewrite add as many as it liked.
EM_DASH_ENTITY = r"&(?:mdash|#8212|#[xX]2014);"
EN_DASH_ENTITY = r"&(?:ndash|#8211|#[xX]2013);"

# Em dashes, and en dashes that are not a numeric range. "2010-2023" written
# with an en dash and "pp. 14-18" are correct typography and the one en dash a
# rewrite legitimately produces; counting them fails a rewrite for getting the
# punctuation right. Only a spaceless en dash flanked by digits is a range,
# because a spaced one is standing in for an em dash. The entity spellings carry
# the same two guards, so `2010&ndash;2023` is a range on both sides of the
# alternation and neither form is stricter than the other.
#
# scan.py scores against this and verify.py gates against it. They were two
# byte-identical copies with a test pinning them together, which is the drift
# this module exists to make impossible: one object, imported twice.
PROSE_DASH_RX = re.compile(
    r"—|%s|–(?!\d)|(?<!\d)–|%s(?!\d)|(?<!\d)%s"
    % (EM_DASH_ENTITY, EN_DASH_ENTITY, EN_DASH_ENTITY))

def invisible_entities(text):
    """Every character reference that renders as a concealment character, as
    (match, decoded character) pairs.

    The principle is PROSE_DASH_RX's, pointed the other way: a document written
    with `&#8203;` renders a zero-width space, so it is one to the counter as
    well. Decoded with html.unescape rather than a hand-kept alternation,
    because HTML5 gives U+200B four named spellings beyond ZeroWidthSpace and a
    list here would drift from the tables in artifacts.py.

    The two space-like characters are deliberately excluded. `&nbsp;` is
    ubiquitous, visible in the source, and the reason blank_entities exists;
    nothing about it is concealed from anybody. The zero-widths and the
    directional controls are different: their entity forms exist to put an
    invisible character into the rendered page, and the number in the source
    tells a reader nothing about what it does.
    """
    out = []
    for m in HTML_ENTITY_RX.finditer(text):
        decoded = html.unescape(m.group(0))
        if len(decoded) != 1 or decoded == m.group(0):
            continue
        if decoded in SPACE_LIKE_UNICODE:
            continue
        if (decoded in HIDDEN_UNICODE or decoded in REPORT_ONLY_UNICODE
                or _TAG_RX.match(decoded) or _VS_RX.match(decoded)):
            out.append((m, decoded))
    return out


# --------------------------------------------------------------------------
# links, images, URLs
# --------------------------------------------------------------------------

IMAGE_RX = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
LINK_RX = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
REF_LINK_RX = re.compile(r"(?<!!)\[([^\]]+)\]\[([^\]]*)\]")
# The label is captured so a `[a][b]` match can be required to resolve against a
# definition before it is reported. Without that, adjacent brackets in ordinary
# prose read as reference links: `matrix[i][j]` outside a code span is the common
# case, and the finding told the writer to convert a link that does not exist.
REF_DEF_RX = re.compile(r"(?m)^\s*\[([^\]]+)\]:\s*(\S+)")
AUTOLINK_RX = re.compile(r"<https?://[^>]+>")

# Two URL patterns, for two jobs.
#
# URL_RX stops at the first character that closes a wrapper, which is what an
# extractor wants: the URL in `(see https://x.dev/p)` is not the closing paren.
# URL_GREEDY_RX runs to the next whitespace, which is what a *stripper* wants:
# scan.py deletes URLs before measuring prose rhythm, and leaving a stray `)`
# or `"` behind puts markup back into the word counts. Narrowing the greedy one
# to match the other would quietly change every stylometric number this engine
# publishes.
URL_RX = re.compile(r"https?://[^\s)>\]\"']+")
URL_GREEDY_RX = re.compile(r"https?://\S+")
# The same pattern under the name the README checker reports it by. A URL only
# counts as bare once strip_wrapped_urls has blanked every one that already sits
# inside a link, an attribute, an autolink, a reference definition, or a code
# span, which is what makes an extractor pattern the right one here.
BARE_URL_RX = URL_RX

HTML_TAG_RX = re.compile(r"</?[a-zA-Z][^>]*>")
HTML_ATTR_URL_RX = re.compile(r"(?:src|href)\s*=\s*[\"'][^\"']*[\"']", re.I)
HTML_IMG_RX = re.compile(r"<img[^>]+src\s*=\s*[\"']([^\"']+)[\"']", re.I)
HTML_IMG_ALT_RX = re.compile(r"""<img\b[^>]*?\balt\s*=\s*(["'])(.*?)\1""", re.I)
HTML_LINK_RX = re.compile(r"<a[^>]+href\s*=\s*[\"']([^\"']+)[\"']", re.I)
# Anchor text, for the vague-link-text check. Non-greedy and DOTALL because a
# centered header routinely puts the badge image and the anchor text on separate
# lines. Nested <a> is not valid HTML, so there is nothing to balance.
HTML_ANCHOR_RX = re.compile(r"<a\b[^>]*>(.*?)</a>", re.I | re.S)
# Any line opening with a tag is markup, not the project description. Kept broad
# on purpose: <details>, <picture>, and <p align=center> all show up in header
# blocks, and listing tags by hand guarantees missing one.
HTML_TAG_LINE_RX = re.compile(r"^\s*</?[a-zA-Z][a-zA-Z0-9]*(?:\s|>|/>)")
HTML_CENTER_RX = re.compile(r"<(p|div|h[1-6])\s+align=[\"']center[\"']", re.I)

# Rendered-invisible HTML (hiding CSS, the hidden attribute, white text,
# comments) is rwlib/injection.py's fact, not this module's: concealment is a
# safety judgement, and the two copies that briefly existed here had already
# drifted from its corpus-calibrated thresholds by the time they merged.

# File paths, and only the ones carrying an extension. An extensionless path
# like `voices/ACTIVE` is not tracked, and that is a deliberate ceiling rather
# than an oversight: dropping the extension requirement makes this match every
# slash-separated pair in English prose. Over this repo's own documents that is
# "and/or", "read/write", "TCP/IP", "human/AI", and every `owner/repo` slug.
PATH_RX = re.compile(r"(?<![\w/])(?:\.{0,2}/)?(?:[\w.-]+/)+[\w.-]+\.\w{1,6}\b")

# Substrings, not patterns: is_badge does `h in url`, so a regex written here is
# a literal that never matches. GitHub Actions badges are covered by
# "actions/workflows".
#
# BADGE_HOSTS_CORPUS is what the study counted, and it is frozen: the corpus
# medians in corpus_summary.json were measured with exactly this list, and
# widening it without regenerating the corpus compares a README against a number
# that means something else.
BADGE_HOSTS_CORPUS = (
    "shields.io", "badge.fury.io", "img.shields", "badgen.net", "travis-ci",
    "circleci.com/gh", "codecov.io", "coveralls.io", "actions/workflows",
    "sonarcloud.io", "snyk.io", "discord.com/api/guilds", "opencollective.com",
    "npmjs.com/package", "pypi.org/project", "crates.io/v", "gitpod.io/button",
    "deepwiki.com/badge", "img.badgesize.io", "visitor-badge",
)
# What the checker counts: the study's list plus one catch-all. "/badge" picks up
# the long tail the named hosts miss (trendshift, star-history, repology,
# awesome.re, scorecard): 625 badges against 568 over the committed snapshot, and
# no non-badge image caught by it in that sample. The divergence is deliberate
# and one-directional. The checker is broader than the study, never narrower, so
# a badge-wall finding stays conservative against a corpus median of 5.
BADGE_HOSTS = BADGE_HOSTS_CORPUS + ("/badge",)


def is_badge(url, hosts=BADGE_HOSTS):
    lu = url.lower()
    return any(h in lu for h in hosts)


# --------------------------------------------------------------------------
# blanking
# --------------------------------------------------------------------------

def blank(match):
    """Replace a span with same-length whitespace, so offsets stay stable.

    Written as a re.sub replacement function. Newlines survive, because a
    blanked block that loses its line breaks moves every line number below it.
    """
    return re.sub(r"\S", " ", match.group(0))


def blank_all(text, *patterns):
    for rx in patterns:
        text = rx.sub(blank, text)
    return text


def strip_images(text):
    """Blank every markdown image, so LINK_RX sees links and not badge wrappers.

    A badge-wrapped link is `[![alt](badge.svg)](target)`, and it is one of the
    most common shapes in a README. LINK_RX's outer `[` stops at the first `]`,
    which is the one closing the alt text, so left alone it captures `![alt` as
    the link text and the *badge image URL* as the destination: a pseudo-link
    that is not in the file, counted as a link and averaged into link text
    length. Blanking the image first leaves `[     ](target)`, which matches
    with the real destination and with whitespace for text, and whitespace text
    is already dropped from the average.
    """
    return IMAGE_RX.sub(blank, text)


def blank_entities(text):
    """Blank every HTML character reference, so the `;` that closes one is not
    read as prose punctuation.

    `&amp;`, `&nbsp;`, and `&#39;` are ordinary in a README, and each one ends in
    a semicolon that belongs to the markup rather than to the sentence. A voice
    that forbids semicolons reported one finding per entity, which on a header
    block full of `&nbsp;` is a wall of findings about punctuation the writer
    never typed.

    Deliberately not folded into apply_exemptions. The dash counters want to see
    `&mdash;`, and a blanket blank here would hide it from them.
    """
    return HTML_ENTITY_RX.sub(blank, text)


def strip_wrapped_urls(text):
    """Blank every URL that already lives inside a link, an HTML attribute, an
    autolink, a reference definition, or inline code. What survives is bare.

    A URL inside backticks is part of a command or a config value, not a link
    the reader is meant to click. Telling someone to wrap `curl https://...` in
    markdown would break the thing they are supposed to paste.
    """
    out = strip_images(text)
    return blank_all(out, LINK_RX, HTML_ATTR_URL_RX, AUTOLINK_RX, REF_DEF_RX,
                     INLINE_CODE_RX)


def apply_exemptions(text):
    """Blank the spans this plugin promises never to rewrite, so a document that
    quotes AI patterns in order to warn about them does not score as one.

    Every span blanked here is one verify.py separately checks for verbatim
    preservation, so hiding it from the counters cannot hide a regression: an
    edit to a fence, a table, a block quote, or inline code is already a
    violation by the time the counters run. Leaving them in is what makes a
    document that quotes a flagged phrase fail the tell gate, which is the false
    positive the exemption exists to prevent.
    """
    return blank_all(text, FRONTMATTER_RX, FENCE_RX, INLINE_CODE_RX,
                     TABLE_ROW_RX, BLOCKQUOTE_RX, QUOTED_RX)


# --------------------------------------------------------------------------
# offsets and shapes
# --------------------------------------------------------------------------

def line_of(text, index):
    return text.count("\n", 0, index) + 1


def excerpt(text, start, end, pad=34):
    lo = max(0, start - pad)
    hi = min(len(text), end + pad)
    frag = text[lo:hi].replace("\n", " ")
    return re.sub(r"\s+", " ", frag).strip()


def context(text, start, end, pad=30):
    """excerpt() with the narrower window verify.py reports violations in."""
    return excerpt(text, start, end, pad=pad)


def word_count(text):
    return len(re.findall(r"\b[\w'-]+\b", text))


def is_prose_block(block):
    """True when a block is prose rather than a list, a table, or a heading.

    Two rules, because the same block was read wrong from both directions.

    A block that *opens* with a bullet is a list, whatever the ratio says. Items
    that wrap over several lines each drive the bullet share below half, so a
    six-item list with three-line items scored as one long paragraph and the
    voice paragraph-length cap fired on it. `CHANGELOG.md` reported five of
    those and every one was a bullet list. Nothing that starts with a bullet is a
    paragraph, so the ratio never needed a vote here.

    Past the first line, the majority rule stands. One sentence of lead-in
    followed by eight bullets has a first line that is prose, and matching only
    the first line let the whole thing score as a single 90-word paragraph. A
    lead-in plus one or two bullets is still a paragraph with a list under it,
    which is why that half is a majority rather than any bullet at all.
    """
    lines = [ln for ln in block.split("\n") if ln.strip()]
    if not lines:
        return False
    if lines[0].startswith(("    ", "\t")):
        return False
    first = lines[0].lstrip()
    if first.startswith(("#", ">", "|", "```")):
        return False
    if LIST_ITEM_RX.match(lines[0]):
        return False
    listish = sum(1 for ln in lines if LIST_ITEM_RX.match(ln))
    return listish * 2 < len(lines)


def strip_for_stats(text):
    """Remove code and markup noise before measuring prose statistics.

    Deleting rather than blanking, because nothing downstream of this takes an
    offset from the result: it is counted, not located. `scan.strip_for_stats`
    is the name the reference files use and it delegates here; the argument for
    each line (why tables and headings go, why list items stay) is in its
    docstring. `registers.detect_register` calls this directly, which is the
    point of one copy: the word count that picks a register and the word count
    the register is applied to are the same measurement.
    """
    out = FRONTMATTER_RX.sub("", text)
    out = FENCE_RX.sub("", out)
    out = INLINE_CODE_RX.sub("", out)
    out = TABLE_ROW_RX.sub("", out)
    out = URL_GREEDY_RX.sub("", out)
    out = HEADING_LINE_RX.sub("", out)
    out = BLOCKQUOTE_RX.sub("", out)
    out = re.sub(r"[*_`]", "", out)
    out = re.sub(r"(?m)^\s*>\s*", "", out)
    return out

