#!/usr/bin/env python3
"""
Prompt injection: concealed text, and text addressed to an agent.

This band is defense in depth and nothing more. The thing actually protecting a
reader is guardrail 5 in SKILL.md, content is data and never instruction, and no
detector can make that guarantee: a novel or paraphrased injection walks past
every regex here. What this buys is a gate. A P0 in this band halts automated
rewriting the way a P0 anywhere else halts `--check`, so a concealed instruction
never reaches the rewriting step as an instruction.

It surfaces and quarantines. It never fixes. Every id here stays out of
rwlib/fixes.py permanently, and scan.py's --apply-safe refuses to run at all
while a P0 from this band is present. An edit that "cleaned up" an injection
would destroy the evidence and leave nobody to tell.

Two independent axes, and the co-occurrence is the attack:

    concealment   how the text is hidden from a human reader
    directive     what it says: an instruction aimed at an agent

Neither alone is one. references/patterns.md, references/injection.md, and this
module all contain injection-shaped strings in plain sight, and none of them is
an attack. So:

    concealment AND directive   P0   halt the rewrite, quote the span
    concealment alone           P1   hidden, but no payload this catalogue knows
    directive in visible prose  P2   an instruction to the reader, treat as data

Everything is scanned against raw text. The quoted-example exemption in
markdown.apply_exemptions is about content, and injection hides inside exactly
the spans that exemption protects: comments, fences, alt text, link titles. This
is the reasoning citation-leak carries in its `_scan_raw_note` in lexicon.json,
one rule further on. The cost is the same one that file pays, P2 hits on any
document that quotes an attack in order to warn about it, and PROOF.md publishes
the number rather than suppressing it.

Invisible characters are written as arithmetic on codepoints here, never as
literals, for the reason artifacts.py gives: as literals they are invisible, and
any tool that normalizes whitespace turns the check into a no-op without
changing anything a reader can see.

Stdlib only, 3.9+.
"""

import html
import re

from .findings import make, sort_key
from .lexicon import synthetic_priority as SYNTH
from .markdown import line_of

HIDDEN_DIRECTIVE_ID = "injection-hidden-directive"
TAG_SMUGGLING_ID = "injection-tag-smuggling"
HIDDEN_TEXT_ID = "injection-hidden-text"
VISIBLE_DIRECTIVE_ID = "injection-visible-directive"

# Every id this module can raise. rwlib.lexicon holds their priorities, beside
# every other synthetic id, so a register can name one and validate.py knows it
# exists. test_every_id_this_module_raises_declares_a_priority pins the two.
FINDING_IDS = (HIDDEN_DIRECTIVE_ID, TAG_SMUGGLING_ID, HIDDEN_TEXT_ID,
               VISIBLE_DIRECTIVE_ID)

BAND = "safety"


# --------------------------------------------------------------------------
# the directive axis: text addressed to an agent
# --------------------------------------------------------------------------

# Deliberately shape-matched rather than meaning-matched. Every alternative is
# an attack idiom rather than a word an ordinary sentence reaches for, because
# the cost of a loose one is a P0 on somebody's README. Three were tightened
# after measuring against the 100-README corpus and this plugin's own files:
#
#   `forget everything` alone hit "the three essentials (if you forget
#   everything else)" in two shipped voice profiles, so it needed a target.
#   Requiring one pronoun after it was not enough: `forget you|your|what` is
#   ordinary English (`don't forget your API key`, `I'll never forget what
#   happened`), and inside an HTML comment that reads as concealment plus a
#   directive, which is a P0 that halts --apply-safe and cannot be suppressed by
#   design. It now takes the whole instruction shape, spelled out in three
#   branches below, and picked up `forget the above instructions` on the way,
#   which the pronoun version never matched.
#   `send it to` and a bare `reply with` are ordinary English and were cut down
#   to the shapes an exfiltration payload actually uses.
DIRECTIVE_RX = re.compile(r"""(?imx)
    # override the instructions already in force
      ignore \s+ (?:all\s+|the\s+|any\s+)?
        (?:previous|above|prior|earlier|preceding) \s+
        (?:instruction|instructions|prompt|prompts|rule|rules)
    | disregard \s+ (?:the\s+|all\s+|any\s+)?
        (?:above|previous|prior|earlier|preceding)
    # `forget`, three shapes. Each one is an instruction with an object, which
    # is what separates the attack from the verb: the pronoun alone is English.
    # Plural before singular in each alternation, so the quoted evidence is the
    # whole word rather than `instruction` out of `instructions`.
    | forget \s+ (?:all\s+|everything\s+|any\s+|the\s+)*
        (?:previous|above|prior|earlier|preceding)
        (?:\s+ (?:instructions|instruction|prompts|prompt|rules|rule|context))?
    | forget \s+ (?:all\s+|everything\s+)? (?:you|your) \s+
        (?:\w+\s+){0,2}?
        (?:told|instructed|taught|given|said|read|know|knew|learned)
    | forget \s+ (?:all\s+)? (?:your|the) \s+
        (?:instructions|instruction|prompts|prompt|rules|rule|training|system)
    # role and turn injection: the shapes a chat transcript is framed in
    | ^ \s* (?:system|assistant) \s* :
    | <\|im_(?:start|end)\|>
    | \[/?INST\]
    | \bsystem \s+ prompt \s* :
    | \byou \s+ are \s+ now \b
    | \bnew \s+ instructions? \s* :
    # a fabricated tool call, shaped like the agent's own action syntax
    | </?function_calls>
    | <invoke \b
    | ```\s*tool_code
    # exfiltration and secrecy
    | do \s+ not \s+ (?:tell|inform|mention|reveal|show|report) \s+
        (?:it\s+|this\s+|that\s+)? (?:to\s+)? (?:the\s+)?
        (?:user|human|anyone|reader|operator|owner)
    | send \s+ (?:this|these|the\s+(?:contents?|key|token|secret|password))
        \s+ to \b
    | repl(?:y|ies) \s+ (?:only\s+)? with \s+ (?:the\s+|your\s+|this\s+)?
        (?:contents?|text|following|api|key|token|secret|password|system|nothing)
    # An imperative aimed at an agent by name: the noun, punctuation, a command
    # verb. Anchored to the start of a line, a sentence, or an HTML span, because
    # unanchored it is a comma-list detector. On the 100-README corpus it fired
    # on "state model, output formats", "(model, send key, theme...)" and "In
    # your agent, run it once per repo", none of which addresses anything.
    | (?:^|[.!?]\s+|>\s*)
      (?:AI|assistant|model|agent|LLM|Claude|ChatGPT|GPT|Copilot|Gemini|system)
        \s* [,:] \s* (?:please\s+)?
        (?:ignore|disregard|forget|stop|output|print|reveal|send|execute|run|
           respond|reply|write|do) \b
""")


# --------------------------------------------------------------------------
# the concealment axis: text a reader does not see
# --------------------------------------------------------------------------

# Each of these marks the text to search with a `hidden` group, or leaves it out
# to mean "the whole match". CONCEAL_ELEMENT_RX deliberately leaves it out: a
# directive can sit in the hidden element's own alt or title attribute as easily
# as in its body, and the whole element is the span a reader is owed.
COMMENT_RX = re.compile(r"(?s)<!--(?P<hidden>.*?)-->")

# The CSS properties that take an element out of the visual flow. `left:-NNNpx`
# and `text-indent:-NNNpx` want three digits or more so they cannot match an
# ordinary negative margin or indent. `overflow:hidden` is deliberately absent:
# it is a layout workhorse in legitimate CSS, and a height or width of zero in
# the same style attribute is already caught by the branch below, which covers
# the one combination that is actually concealment.
HIDING_CSS = (r"(?:display\s*:\s*none"
              r"|visibility\s*:\s*hidden"
              r"|opacity\s*:\s*0(?!\.\d*[1-9])"
              r"|font-size\s*:\s*0(?!\.\d*[1-9])"
              r"|(?:left|top)\s*:\s*-\d{3,}\s*px"
              r"|text-indent\s*:\s*-\d{3,}\s*px"
              r"|clip-path\s*:\s*inset\s*\(\s*100\s*%"
              r"|clip\s*:\s*rect\s*\(\s*0\b"
              r"|transform\s*:\s*scale\s*\(\s*0(?!\.\d*[1-9])"
              r"|(?:width|height)\s*:\s*0(?:px)?(?=[;\"'\s]|$))")

# The whole element, opening tag through closing tag, because the payload sits
# in the body and the hiding sits in the attribute. A regex that captured only
# the style attribute would never see what it was hiding.
#
# The body is unbounded on purpose. A character ceiling here is an evasion the
# attacker controls: pad the hidden element past the ceiling and the element
# stops matching, which drops a P0 `injection-hidden-directive` to the P2 that
# only sees the visible text. A plain non-greedy `.*?</(?P=tag)>` has the same
# evasion under a different shape: `<div style="display:none"><div>x</div>
# payload</div>` stops at the FIRST same-name closer, leaving `payload` outside
# the concealed span. `_matching_close` below tracks same-tag nesting depth
# instead, so the match always reaches the closer that actually balances the
# opener. Still linear: each scan only advances through the open/close tokens
# of the one tag name in play, never both directions at once.
CONCEAL_ELEMENT_OPEN_RX = re.compile(
    r"(?is)<(?P<tag>\w+)[^>]*style=[\"'][^\"']*" + HIDING_CSS +
    r"[^\"']*[\"'][^>]*?(?P<selfclose>/)?>")


def _matching_close(text, tag, search_from):
    """Index just past the `</tag>` that balances an opener ending at
    `search_from`, honoring nested same-name tags. None if it never closes."""
    open_rx = re.compile(r"(?is)<%s\b[^>]*?(/)?>" % re.escape(tag))
    close_rx = re.compile(r"(?is)</%s\s*>" % re.escape(tag))
    depth, pos = 1, search_from
    while True:
        next_open = open_rx.search(text, pos)
        next_close = close_rx.search(text, pos)
        if next_close is None:
            return None
        if next_open and next_open.start() < next_close.start():
            if not next_open.group(1):
                depth += 1
            pos = next_open.end()
            continue
        depth -= 1
        pos = next_close.end()
        if depth == 0:
            return pos


class _ConcealElementMatch:
    def __init__(self, start, end, text):
        self._start, self._end, self._text = start, end, text

    def start(self):
        return self._start

    def end(self):
        return self._end

    def group(self, n=0):
        return self._text

    def groupdict(self):
        return {}


class _ConcealElementFinder:
    """`.finditer`-compatible wrapper so `_concealed()` can treat this the same
    as every other entry in CONCEALMENT, despite needing depth-aware matching
    a single compiled regex cannot do."""

    @staticmethod
    def finditer(text):
        pos = 0
        while True:
            m = CONCEAL_ELEMENT_OPEN_RX.search(text, pos)
            if m is None:
                return
            if m.group("selfclose"):
                # No body to conceal; CONCEAL_TAG_RX already covers this shape.
                pos = m.end()
                continue
            end = _matching_close(text, m.group("tag"), m.end())
            if end is None:
                pos = m.end()
                continue
            yield _ConcealElementMatch(m.start(), end, text[m.start():end])
            pos = end


CONCEAL_ELEMENT_RX = _ConcealElementFinder()

# The same hiding on a tag that never closes: `<img style="display:none"
# alt="...">`. The tag itself is the span, which is where alt and title live.
CONCEAL_TAG_RX = re.compile(
    r"(?is)<\w+[^>]*style=[\"'][^\"']*" + HIDING_CSS + r"[^\"']*[\"'][^>]*>")

# The HTML hidden attribute: the declarative spelling of display:none. A bare
# word, `=""`, `="hidden"`, or `="until-found"`, and nothing else. The
# mandatory whitespace before the word keeps aria-hidden and data-hidden out
# (aria-hidden hides from screen readers, not from the page), and the lookahead
# keeps an attribute value that merely contains the word out.
HIDDEN_ATTR = (r"\shidden(?:\s*=\s*[\"']?(?:hidden|until-found)?[\"']?)?"
               r"(?=[\s/>])")
CONCEAL_ATTR_ELEMENT_RX = re.compile(
    r"(?is)<(?P<tag>\w+)[^>]*" + HIDDEN_ATTR + r"[^>]*>.*?</(?P=tag)\s*>")
CONCEAL_ATTR_TAG_RX = re.compile(r"(?is)<\w+[^>]*" + HIDDEN_ATTR + r"[^>]*>")

# White text: camouflage rather than removal from the flow, and a heuristic
# where everything above is a declaration. White is only certainly invisible
# against a default background, so a style that also declares any background is
# left alone: that author is managing contrast, not hiding. Text matching a
# themed background needs a renderer to catch and is out of scope. GitHub
# strips style= from rendered markdown, which narrows this to standalone HTML
# and READMEs rendered elsewhere; it does not make the text less hidden there.
WHITE_CSS = (r"color\s*:\s*(?:white\b|#fff\b|#ffffff\b|#fefefe\b|#fdfdfd\b"
             r"|rgba?\(\s*255\s*,\s*255\s*,\s*255)")
CONCEAL_WHITE_ELEMENT_RX = re.compile(
    r"(?is)<(?P<tag>\w+)[^>]*style=[\"'](?![^\"']*background)[^\"']*"
    + WHITE_CSS + r"[^\"']*[\"'][^>]*>.*?</(?P=tag)\s*>")
# The deprecated font tag's spelling of the same trick.
CONCEAL_FONT_RX = re.compile(
    r"(?is)<font[^>]+color\s*=\s*[\"']?(?:white\b|#fff\b|#ffffff\b)"
    r"[^>]*>.*?</font\s*>")

# Markdown-native hiding spots a reader never sees rendered.
LINK_TITLE_RX = re.compile(r"(?s)\]\([^)\s]+\s+[\"'](?P<hidden>[^\"']+)[\"']\s*\)")
REF_TITLE_RX = re.compile(
    r"(?m)^\s*\[[^\]]+\]:\s*\S+\s+[\"'](?P<hidden>[^\"']+)[\"']")
TITLE_ATTR_RX = re.compile(r"(?i)title=[\"'](?P<hidden>[^\"']+)[\"']")
ALT_TEXT_RX = re.compile(r"!\[(?P<hidden>[^\]]*)\]")

# verify.py's docstring records that alt text is not in its extract set, so an
# edit can rewrite it silently. Here that gap is the thing to scan rather than a
# gap to close: alt text is invisible to a reader and legible to a model, which
# is the definition this band works from.
CONCEALMENT = (
    ("comment", COMMENT_RX),
    ("hidden element", CONCEAL_ELEMENT_RX),
    ("hidden element", CONCEAL_TAG_RX),
    ("hidden element", CONCEAL_ATTR_ELEMENT_RX),
    ("hidden element", CONCEAL_ATTR_TAG_RX),
    ("white text", CONCEAL_WHITE_ELEMENT_RX),
    ("white text", CONCEAL_FONT_RX),
    ("link title", LINK_TITLE_RX),
    ("reference title", REF_TITLE_RX),
    ("title attribute", TITLE_ATTR_RX),
    ("image alt text", ALT_TEXT_RX),
)

# The kinds whose bare existence is worth a P1 when they carry prose and no
# directive the catalogue knows. Comments, and the two element classes a
# renderer drops entirely: a hidden div full of sentences is hidden text
# whatever it says. The attribute kinds stay out, because a title or an alt is
# visible machinery doing its documented job.
CONCEALED_PROSE_KINDS = ("comment", "hidden element", "white text")


# --------------------------------------------------------------------------
# concealment alone
# --------------------------------------------------------------------------

# A hidden comment with no payload is worth one line of "why is this here", and
# nothing shorter than a sentence clears that bar. Eight words is where the
# 100-README corpus splits: below it every comment is a marker, above it they
# start being prose somebody wrote.
MIN_HIDDEN_WORDS = 8

# The markers that survived the word count in the corpus, plus the two this
# plugin ships. Each one is a machine talking to a build step rather than a
# person talking to a reader, and 4 of the corpus's 8 long comments are one of
# these. The remaining 4 are genuine maintainer notes and stay P1: they are the
# honest residual, and PROOF.md publishes the rate.
BUILD_MARKER_RX = re.compile(r"""(?ix)
    ^ \s* (?: /{2}\s* | \#\s* )?
    (?:
        (?:begin|end|start|stop)\b
      | [\w.:@/-]+ [:-] (?:start|end|begin|stop)\b
      | (?:todo|fixme|hack|xxx)\b
      | rabbit-allow\b
      | prettier-ignore | markdownlint | eslint | stylelint | shellcheck
      | doctoc | all-contributors | mcp-name | sponsors?
      | omit \s+ in \s+ toc | toc\b
      | [\w-]+ - (?:ignore|disable) [\w-]*
    )
""")


# --------------------------------------------------------------------------
# the Unicode Tags block: invisible characters that decode to ASCII
# --------------------------------------------------------------------------

# U+E0000 to U+E007F map one to one onto printable ASCII and render as nothing,
# so an attacker can smuggle a whole readable instruction into text that looks
# empty. That is categorically different from the stray zero-width space
# scan.py's hidden-unicode owns: one is a paste artifact, this is a message.
TAG_BLOCK_LO = 0xE0000
TAG_BLOCK_HI = 0xE007F

# Two words and six characters. One or two tag characters are noise rather than
# a sentence, and the paste-artifact detector already reports them.
MIN_TAG_WORDS = 2
MIN_TAG_CHARS = 6


def tag_runs(text):
    """[(offset, decoded)] for every run of Unicode Tags characters that decodes
    to something readable."""
    out, run, start = [], [], 0
    for i, ch in enumerate(text):
        if TAG_BLOCK_LO <= ord(ch) <= TAG_BLOCK_HI:
            if not run:
                start = i
            run.append(chr(ord(ch) - TAG_BLOCK_LO))
        elif run:
            out.append((start, "".join(run)))
            run = []
    if run:
        out.append((start, "".join(run)))
    return _readable_runs(out)


# A Tags-block character spelled as its own decimal or hex HTML entity, e.g.
# `&#917601;` or `&#xE0061;`, renders identically to the literal character in
# any browser but is plain ASCII to a regex scanning raw codepoints: the whole
# `_hidden-unicode` P1 sweep in scan.py already reports these one entity at a
# time, but tag_runs() above never saw them as the message they decode to, so
# a smuggled instruction spelled this way scored P1 noise instead of the P0
# this band exists to raise. Entities are matched as tokens rather than
# decoded with html.unescape() up front so the offsets stay in raw-text space;
# decoding first would shift every position after the first multi-digit
# entity and break line_of(raw, at) for the finding.
_NUMERIC_ENTITY_RX = re.compile(r"&#(?:[xX][0-9a-fA-F]+|[0-9]+);")


def _entity_codepoint(entity):
    body = entity[2:-1]
    try:
        return int(body[1:], 16) if body[:1] in ("x", "X") else int(body, 10)
    except ValueError:
        return -1


def entity_tag_runs(text):
    """[(offset, decoded)] for every run of Tags-block characters spelled out
    as consecutive numeric HTML entities rather than as literal codepoints."""
    out, run, start, pos = [], [], 0, 0
    for m in _NUMERIC_ENTITY_RX.finditer(text):
        if run and m.start() != pos:
            out.append((start, "".join(run)))
            run = []
        point = _entity_codepoint(m.group(0))
        if TAG_BLOCK_LO <= point <= TAG_BLOCK_HI:
            if not run:
                start = m.start()
            run.append(chr(point - TAG_BLOCK_LO))
        elif run:
            out.append((start, "".join(run)))
            run = []
        pos = m.end()
    if run:
        out.append((start, "".join(run)))
    return _readable_runs(out)


def _readable_runs(runs):
    out = []
    for at, msg in runs:
        # Strip language tag framing control characters (e.g. U+E0001 / \x01, U+E007F / \x7f)
        cleaned = "".join(c for c in msg if c.isprintable() or c in " \t\n\r")
        if cleaned and all(c.isprintable() or c in " \t\n\r" for c in cleaned):
            core = cleaned.strip()
            if len(core) >= MIN_TAG_CHARS and len(core.split()) >= MIN_TAG_WORDS:
                out.append((at, msg))
    return out


# --------------------------------------------------------------------------
# scanning
# --------------------------------------------------------------------------

REVIEW = ("Not rewritten and not fixable. Read the span above and decide "
          "before letting any tool process this document.")


def _flat(text, limit=None):
    out = re.sub(r"\s+", " ", text).strip()
    if limit and len(out) > limit:
        out = out[:limit - 3].rstrip() + "..."
    return out


def _concealed(raw):
    """[(kind, start, end, text)] for every span a reader does not see.

    Sorted by position, widest first at a tie, so a comment is considered before
    the title attribute inside it and the caller can drop the nested one.
    """
    spans = []
    for kind, rx in CONCEALMENT:
        for m in rx.finditer(raw):
            body = m.groupdict().get("hidden")
            spans.append((kind, m.start(), m.end(),
                          m.group(0) if body is None else body))
    spans.sort(key=lambda s: (s[1], -s[2]))
    return spans


def scan(raw):
    """Findings for one document, from its raw text.

    Raw, never the exemption-blanked copy. See the module docstring.
    """
    findings = []
    claimed = []

    for kind, start, end, body in _concealed(raw):
        # A title attribute inside an already-reported comment is the same
        # attack counted twice.
        if any(lo <= start and end <= hi for lo, hi in claimed):
            continue
        # Decode HTML entities before the directive test: a directive spelled
        # inside a concealed span as `&#105;gnore all previous instructions` is
        # one a reader's browser would execute and a raw-text regex would miss.
        # The finding still quotes the raw span below, so the evidence shows the
        # obfuscation rather than the decoded form.
        hit = DIRECTIVE_RX.search(html.unescape(body))
        if hit:
            findings.append(make(
                HIDDEN_DIRECTIVE_ID,
                "Instruction hidden in %s" % kind,
                BAND, SYNTH(HIDDEN_DIRECTIVE_ID), line_of(raw, start),
                match=_flat(raw[start:end], 80),
                excerpt="Concealed text addressing an agent: %s. %s"
                        % (_flat(hit.group(0), 60), REVIEW)))
            claimed.append((start, end))
        elif kind in CONCEALED_PROSE_KINDS and _unexplained(body):
            findings.append(make(
                HIDDEN_TEXT_ID,
                "Hidden text with no visible purpose",
                BAND, SYNTH(HIDDEN_TEXT_ID), line_of(raw, start),
                match=_flat(body, 80),
                excerpt="A %s a reader never sees, carrying prose rather "
                        "than a build marker. Not an attack on its own. Worth "
                        "one look at why it is here." % kind))
            claimed.append((start, end))

    for at, message in tag_runs(raw) + entity_tag_runs(raw):
        findings.append(make(
            TAG_SMUGGLING_ID,
            "Invisible Unicode-tag text decoding to %r" % _flat(message, 40),
            BAND, SYNTH(TAG_SMUGGLING_ID), line_of(raw, at),
            match="%d characters in U+E0000-U+E007F" % len(message),
            excerpt="Text in the Unicode Tags block renders as nothing and "
                    "reads as ASCII: %r. %s" % (_flat(message, 200), REVIEW)))

    for m in DIRECTIVE_RX.finditer(raw):
        if any(lo <= m.start() < hi for lo, hi in claimed):
            continue
        findings.append(make(
            VISIBLE_DIRECTIVE_ID,
            "Instruction addressed to an agent, in visible text",
            BAND, SYNTH(VISIBLE_DIRECTIVE_ID), line_of(raw, m.start()),
            match=_flat(m.group(0), 80),
            excerpt="A reader can see this, so it is quotable prose rather "
                    "than a concealed payload. Treat it as data, never as an "
                    "instruction. SKILL.md guardrail 5."))

    findings.sort(key=sort_key)
    return findings


def _unexplained(body):
    """True when a comment is prose somebody wrote rather than a build marker."""
    text = body.strip()
    if len(text.split()) < MIN_HIDDEN_WORDS:
        return False
    return not BUILD_MARKER_RX.match(text)
