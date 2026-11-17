#!/usr/bin/env python3
"""
STE: ASD-STE100 Issue 9 (2025-01-15) structural rules for scan.py.

This is a REPORT-ONLY layer. Unlike the lexicon tier system, which can
mechanically fix some violations (hidden characters, utm params, preferred
substitutions), STE violations almost always require judgment to rewrite.
The rewrite (re-splitting long sentences, reordering condition-before-command)
is a language model task. This module flags.

Two modes (from STE, not this module):
  - procedural   instructions: max 20 words/sentence
  - descriptive  explanations: max 25 words/sentence

**This module takes prose with the markup already stripped.** scan.py passes
the exempted copy it already built (`apply_exemptions`), so fenced code,
inline code spans, and quoted examples arrive blanked and are never flagged.
Called on raw markdown, every semicolon in a code fence reads as prose, which
is exactly the 1,069 false positives the first calibration run found. The
same contract `rwlib/stylometry.py` states for the same reason.

The lexicon (`scripts/ste_lexicon.json`) loads lazily, on the first check,
not at import: this module is imported by scan.py unconditionally, and an
eager load made every vendored copy of the engine unimportable when one
packaging list forgot the JSON. Lazy keeps `--help` and every import working
without it, but the mechanical band is default-on now and reads the file for
its caps, so a missing lexicon fails the *scan* rather than only `--ste`.
`scripts/package_skills.py` ships it in SHARED_ENGINE_FILES for that reason.

Synthetic finding IDs, raised by this engine only:
  ste-sentence-procedural    sentence over 20 words in procedural text
  ste-sentence-descriptive   sentence over 25 words in descriptive text
  ste-paragraph-sentences    paragraph over six sentences (Rule 6.6)
  ste-modal                  banned modal verb (should/would/may/might/could)
  ste-ing-verb               -ing form opening a clause after a comma
  ste-condition-order        condition clause after the command verb
  ste-banned-verb            banned verb (check/verify/confirm/ensure)
  ste-phrasal-verb           phrasal verb that should be one word
  ste-no-punctuation         semicolon (STE bans semicolons)
  ste-passive                passive voice where active is possible
  ste-vocab                  banned vocabulary item

The ids split into two bands, and the split is the point: what a script
counts exactly (sentence words, sentences per paragraph, semicolons,
condition order) runs in every plain scan, because counting is the one
thing a script does better than a model. What the lexicon suggests
(vocabulary, verb forms, modals) is advisory, P2, and only asked for.
`MECHANICAL_IDS` below is the one home for which is which.

The `suppression-*` ids are deliberately absent: rwlib/lexicon.py owns them,
and a second copy here is a drift surface. STE findings pass through the same
suppression pass as everything else because scan.py appends them before it
runs `suppress.apply`.

Stdlib only, 3.9+.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
STE_LEXICON_PATH = os.path.join(HERE, "..", "ste_lexicon.json")

# ---------------------------------------------------------------------------
# Finding IDs and priorities
# ---------------------------------------------------------------------------

STE_PRIORITIES = {
    # Mechanical: counted, default-on. P1 where the count is certain; the
    # semicolon is P2 because a ban on punctuation is a style stance.
    "ste-sentence-procedural": "P1",
    "ste-sentence-descriptive": "P1",
    "ste-paragraph-sentences": "P1",
    "ste-condition-order": "P1",
    "ste-no-punctuation": "P2",
    # Advisory: lexicon-suggested, behind --ste, P2 because a word list is
    # a judgment about vocabulary rather than a measurement.
    "ste-modal": "P2",
    "ste-ing-verb": "P2",
    "ste-banned-verb": "P2",
    "ste-phrasal-verb": "P2",
    "ste-passive": "P2",
    "ste-vocab": "P2",
}

# Derived, not restated: two collections that must agree and are written twice
# is how the engine's own SYNTHETIC_FINDING_IDS grew a raise-on-drift check.
STE_FINDING_IDS = frozenset(STE_PRIORITIES)

# The split the module docstring describes. Which band an id sits in decides
# whether scan.py runs it in every plain scan (mechanical) or only under
# --ste (advisory), so a third statement of this list anywhere is drift.
MECHANICAL_IDS = frozenset((
    "ste-sentence-procedural",
    "ste-sentence-descriptive",
    "ste-paragraph-sentences",
    "ste-condition-order",
    "ste-no-punctuation",
))
ADVISORY_IDS = STE_FINDING_IDS - MECHANICAL_IDS


def ste_priority(finding_id):
    """The priority this engine raises a finding at."""
    try:
        return STE_PRIORITIES[finding_id]
    except KeyError:
        raise KeyError(
            "no declared priority for STE finding %r. "
            "Add it to STE_PRIORITIES in rwlib/ste.py." % finding_id
        )


# ---------------------------------------------------------------------------
# Word / phrase counting helpers
# ---------------------------------------------------------------------------

# Words are: alphabetic tokens, numbers, numbers-with-units, abbreviations,
# alphanumeric identifiers, quoted text. Backtick-quoted identifiers count as
# one. Hyphenated words count as one.
WORD_RX = re.compile(r"[A-Za-z][A-Za-z'-]*")
# The unit is optional, so without the boundary guards this matches the digit
# inside an identifier: `item0` counted as `item` plus `0`, two words, and
# `sha256` the same. The docstring below already says an alphanumeric
# identifier is one word, and the caps are default-on now, so a technical
# sentence full of `v2` and `utf8` measured half again as long as it reads.
NUMBER_WITH_UNIT_RX = re.compile(
    r"(?<![A-Za-z0-9])\d+(?:\.\d+)?(?:px|ms|s|min|h|d|w|mb|kb|gb|tb|gbps|mbps|"
    r"hz|mhz|ghz|kw|hw|cc|ml|l|cm|mm|m|km|in|ft|yd|oz|g|kg|lb|%)?"
    r"(?![A-Za-z0-9])")


def count_words(text):
    """Count words in text per STE word-counting rules.

    Numbers, numbers with units, abbreviations, alphanumeric identifiers, and
    quoted text each count as one word. Hyphenated words count as one.
    """
    # Code spans count as one word each
    code_spans = re.findall(r"`[^`]+`", text)
    count = len(code_spans)

    # Strip code spans
    stripped = re.sub(r"`[^`]+`", "", text)

    # Strip markdown images whole (alt text is not visible body text a reader
    # counts), but keep a link's visible text and drop only the URL: "See
    # [the config file](path) for details" reads as five visible words, and
    # dropping the whole match undercounted every sentence that links to
    # something.
    stripped = re.sub(r"!\[[^\]]*\]\([^\)]*\)", "", stripped)
    stripped = re.sub(r"\[([^\]]*)\]\([^\)]*\)", r"\1", stripped)
    # Strip HTML tags
    stripped = re.sub(r"<[^>]+>", "", stripped)

    # Strip numbers-with-units before counting standalone numbers/words,
    # so "50mb" contributes 1 to the count, not 2
    no_units = NUMBER_WITH_UNIT_RX.sub("", stripped)
    no_units = re.sub(r"\s+", " ", no_units).strip()

    count += len(WORD_RX.findall(no_units))

    # Numbers with units, each one is one word
    count += len(NUMBER_WITH_UNIT_RX.findall(stripped))

    # Standalone numbers not already consumed by NUMBER_WITH_UNIT_RX
    count += len(re.findall(r"(?<![A-Za-z0-9])\d+(?![A-Za-z0-9])", no_units))

    return count


# ---------------------------------------------------------------------------
# Vocabulary: banned and approved terms
# ---------------------------------------------------------------------------

_CACHE = {}


def load_ste_lexicon(path=STE_LEXICON_PATH):
    if path not in _CACHE:
        try:
            with open(path, encoding="utf-8") as fh:
                _CACHE[path] = json.load(fh)
        except FileNotFoundError:
            raise FileNotFoundError(
                "STE lexicon not found at %s. Every scan reads it now: the "
                "mechanical checks (sentence caps, paragraph cap, condition "
                "order, semicolon) run by default and take their limits from "
                "this file. Restore it, or run with --no-ste. If this is a "
                "packaged copy, the archive was built without "
                "ste_lexicon.json." % path)
    return _CACHE[path]


def version(path=STE_LEXICON_PATH):
    lex = load_ste_lexicon(path)
    return lex.get("version")


def word_regex(entries):
    """Whole-word alternation, longest first. Same logic as rwlib.lexicon."""
    if not entries:
        return re.compile(r"(?!)")
    escaped = sorted((re.escape(e) for e in entries), key=len, reverse=True)
    return re.compile(r"(?i)(?<![\w-])(" + "|".join(escaped) + r")(?![\w-])")


def dictionary_vocab_regex(entries):
    """Whole-word/phrase alternation with word_regex's hyphen-aware boundary,
    for a list mixing single words and phrases.

    Not phrase_regex: that one's `\\b` boundary treats a hyphen as a break,
    so "cross" matches inside "cross-platform" and "mid" matches inside
    "mid-air". A short, common word from the ASD-STE100 dictionary is
    exactly the shape most likely to also be a hyphenated-compound prefix in
    software prose ("cross-", "mid-", "self-"), which is what
    02_corpus_evidence.py's own counting has to use too, or the corpus
    evidence measures a different regex than the one that ships.
    """
    if not entries:
        return re.compile(r"(?!)")
    escaped = sorted((re.escape(e).replace(r"\ ", r"\s+") for e in entries),
                     key=len, reverse=True)
    return re.compile(r"(?i)(?<![\w-])(" + "|".join(escaped) + r")(?![\w-])")


def phrase_regex(entries):
    """Same for multi-word entries."""
    if not entries:
        # (?!) never matches. The earlier fallback here was (?!x), which is a
        # lookahead that *succeeds* everywhere no "x" follows: an emptied
        # lexicon list would have turned finditer into a per-character loop.
        return re.compile(r"(?!)")
    escaped = sorted((re.escape(e).replace(r"\ ", r"\s+") for e in entries),
                     key=len, reverse=True)
    return re.compile(r"(?i)\b(" + "|".join(escaped) + r")\b")


# Compiled regexes, built lazily on first use (see module docstring).
_BANNED_VERBS_RX = None
_BANNED_MODALS_RX = None
_PHRASAL_VERBS_RX = None
_ING_VERB_AFTER_COMMA_RX = None
_CONDITION_ORDER_RX = None
_PASSIVE_RX = None
_AI_SLOP_RX = None
_DICTIONARY_VOCAB_RX = None
_REGEXES_BUILT = False


def _ensure_regexes():
    global _BANNED_VERBS_RX, _BANNED_MODALS_RX, _PHRASAL_VERBS_RX
    global _ING_VERB_AFTER_COMMA_RX, _CONDITION_ORDER_RX, _PASSIVE_RX
    global _AI_SLOP_RX, _DICTIONARY_VOCAB_RX, _REGEXES_BUILT
    if _REGEXES_BUILT:
        return

    lex = load_ste_lexicon()

    _BANNED_VERBS_RX = word_regex(lex.get("banned_verbs", []))

    _BANNED_MODALS_RX = phrase_regex(
        lex.get("banned_modals", ["should", "would", "may", "might", "could"]))

    _PHRASAL_VERBS_RX = phrase_regex(sorted(_phrasal_examples(lex)))

    # Match -ing form used as verb after a comma (gerund clause, not noun):
    # "..., making it easy to ...", which STE bans.
    #
    # The exclusion list is words that end in "-ing" by spelling accident
    # rather than by being a gerund: "something", "nothing", "morning" are
    # nouns, and "including" and "following" are prepositions in this exact
    # slot ("a list of items, including the config file"), not a verb opening
    # a clause. Unguarded, every one of them matched a comma-then-preposition
    # or comma-then-noun that has nothing to do with the rule this pattern
    # exists to catch.
    _ING_VERB_AFTER_COMMA_RX = re.compile(
        r",\s+(?!(?:including|following|according|something|nothing|"
        r"anything|everything|morning|evening)\b)"
        r"([A-Za-z]+ing)\b(?:\s+(?:that|you|we|they|the|this|these|a|an|"
        r"to|not|it|them|him|her|us|me|be|been|being|get|gets|got|make|makes|"
        r"made|have|has|had|do|does|did|will|would|can|could|should|may|"
        r"might|must))+(?:\s+[A-Za-z]+\b){0,6}",
        re.I)

    # Condition AFTER command: "Do X if Y" is flagged, "If Y, do X" is not.
    # Anchored to an imperative: the verb must open the sentence (line start,
    # list marker, or a sentence boundary), or "I do not know if it works"
    # and every other declarative carrying one of these verbs mid-sentence
    # reads as a command. The clause may not cross a sentence boundary either,
    # so a condition that opens the *next* sentence does not count against
    # this one.
    _CONDITION_ORDER_RX = re.compile(
        r"(?:(?<=^)|(?<=[.!?] )|(?<=[.!?]  )|(?<=: ))"
        r"(?:[-*]\s+|\d+\.\s+)?"
        r"((?:do|run|set|check|make|install|start|stop|open|close|"
        r"write|read|delete|remove|add|update|create|build|compile|deploy|"
        r"execute|launch|send|receive|fetch|pull|push|configure|"
        r"adjust|increase|decrease|connect|disconnect|log|login|logout|"
        r"authenticate|verify|confirm|ensure)\b[^.!?\n]*?"
        r"\b(?:if|when|unless)\b)",
        re.I | re.M)

    # Passive voice: auxiliary + past participle. Regular participles need at
    # least two characters before the -ed ("is red" is an adjective, not a
    # passive), -en covers written/taken/given/hidden and friends, and the
    # alternation carries the common irregulars that end neither way. The
    # earlier pattern here was (\w+ed|en): the second branch was the literal
    # word "en", so "was written" never fired and "is en route" did.
    _PASSIVE_RX = re.compile(
        r"\b(is|are|was|were|be|been|being)\s+"
        r"(\w{2,}ed|\w{2,}en|done|made|put|sent|found|thought|kept|built|set|"
        r"said|known|shown|drawn|thrown|grown|blown|flown|worn|torn|held|"
        r"left|lost|meant|met|paid|read|sold|spent|told|understood|won|"
        r"begun|brought|bought|caught|felt|heard|hung|struck|stuck|laid|"
        r"run|become)\b",
        re.I)

    _AI_SLOP_RX = _build_ai_slop_rx(lex)
    _DICTIONARY_VOCAB_RX = dictionary_vocab_regex(sorted(lex.get("dictionary_vocabulary", {})))
    _REGEXES_BUILT = True


def _build_ai_slop_rx(lex):
    """A regex matching every ai_slop vocabulary item."""
    # Keys starting with "_" are the file's own commentary, not phrases. The
    # first version compiled "_comment" into the pattern, whose decoded form
    # " comment" matched every "word comment" in anybody's prose.
    slop = [k for k in lex.get("ai_slop", {}) if not k.startswith("_")]
    if not slop:
        return re.compile(r"(?!)")
    # A trailing \b only means something after a word character: "e.g." ends
    # on a literal period, and \b there requires a word character next, which
    # the space or comma that follows it in real prose is not, so "e.g." (and
    # "i.e.") never matched at all. The period already stops an accidental
    # partial-word hit on its own, which is what \b is for, so an entry
    # ending in punctuation skips the trailing \b instead of silently never
    # firing.
    alternatives = []
    for k in slop:
        term = k.replace("_", " ")
        boundary = r"\b" if term[-1:].isalnum() else ""
        alternatives.append(re.escape(term) + boundary)
    alternatives.sort(key=len, reverse=True)
    # Case-insensitive like every other STE regex: "Simply run it." is the
    # sentence-initial position these fillers actually sit in.
    return re.compile(r"(?i)\b(" + "|".join(alternatives) + r")")


# ---------------------------------------------------------------------------
# Classification: procedural vs descriptive
# ---------------------------------------------------------------------------

# Signals that text is procedural (imperative, steps, instructions)
PROCEDURAL_INDICATORS = (
    r"\bdo\b", r"\brun\b", r"\binstall\b", r"\bconfigure\b",
    r"\bstart\b", r"\bstop\b", r"\bopen\b", r"\bclose\b",
    r"\bcreate\b", r"\bupdate\b", r"\bdelete\b", r"\bremove\b",
    r"\badd\b", r"\bset\b", r"\bcheck\b", r"\bmake sure\b",
    r"\bgo to\b", r"\bclick\b", r"\bpress\b", r"\benter\b",
    r"\bselect\b", r"\btype\b", r"\bcopy\b", r"\bpaste\b",
    r"\bthen\b", r"\bnext\b", r"\bstep\b", r"\bif\b.*\bdo\b",
    r"\bprerequisite\b", r"\bto install\b", r"\bto run\b",
    r"\bstep \d+\b", r"^\d+\.", r"^\-\s", r"^\*\s",
    # YAML/list-style steps
    r"^\s*-\s+\w",
    # Imperative: "Run the migration."
    r"^\s*(?:run|install|configure|start|stop|check|make|set|add|remove|"
    r"delete|update|create)\s+",
)
PROCEDURAL_RX = re.compile("|".join(PROCEDURAL_INDICATORS), re.I | re.M)

# Signals that text is descriptive (explains, defines, describes)
DESCRIPTIVE_INDICATORS = (
    r"\bis\b.*\bthat\b", r"\bcontains\b", r"\bprovides\b", r"\ballows\b",
    r"\benables\b", r"\bsupports\b", r"\bconsists\b", r"\bincludes\b",
    r"\bexplains\b", r"\bdescribes\b", r"\bdefines\b", r"\bdetails\b",
    r"\bThe \w+ is\b", r"\bThis \w+ provides\b", r"\bwhich is\b",
    r"\bused for\b", r"\bdesigned to\b", r"\baimed at\b",
    r"\bArchitecture\b", r"\bOverview\b", r"\bIntroduction\b",
    r"\bIn this section\b", r"\bAs follows\b",
    # Numeric / measurement descriptions
    r"\b\d+\s*(?:ms|s|min|h|d|mb|gb|gbps|mbps|hz|kw)\b",
    r"\btypically\b", r"\bgenerally\b", r"\busually\b",
    # Third-person explanations
    r"\bthe system\b.*\bdoes\b", r"\bthe component\b.*\bhandles\b",
)
DESCRIPTIVE_RX = re.compile("|".join(DESCRIPTIVE_INDICATORS), re.I | re.M)


def classify_passage(text):
    """Return 'procedural' or 'descriptive' for a passage of text.

    Checks headings, list items, and sentence-level indicators.
    """
    # Check for procedural heading keywords
    procedural_headings = (
        r"^#+\s*(?:install|setup|configure|run|build|deploy|start|stop|"
        r"usage|quickstart|getting started|prerequisites|steps?|"
        r"how to|troubleshoot|faq|known issues|limitations|"
        r"before you begin|procedure|commands?|options?|flags?)",
        r"^#+\s*\d+[\.\):]\s",  # "## 1. Install"
        r"^#+\s*step",           # "### Step 1"
    )
    for rx in procedural_headings:
        if re.search(rx, text, re.I | re.M):
            return "procedural"

    # Check for procedural list patterns
    if re.search(r"^\s*(?:[-*]|\d+\.)\s+\w", text, re.M):
        return "procedural"

    # Check first few sentences for imperative voice
    first_sentences = " ".join(text.split("\n")[:5])
    proc_hits = PROCEDURAL_RX.findall(first_sentences)
    desc_hits = DESCRIPTIVE_RX.findall(first_sentences)

    if len(proc_hits) > len(desc_hits):
        return "procedural"

    # Check for "you can" / "you should" / imperative structure
    if re.search(r"\byou\s+(?:can|should|must|will|need to|have to)\b",
                 text, re.I):
        return "procedural"

    # Default: descriptive
    return "descriptive"


# ---------------------------------------------------------------------------
# Sentence-level checks
# ---------------------------------------------------------------------------

from .markdown import blank_entities as _blank_entities
from .markdown import is_prose_block as _is_prose_block
from .sentences import split_sentences as _split_sentences


def _word_limits():
    """(procedural, descriptive) sentence caps, from the lexicon.

    Rules 5.1 and 6.3 carry the numbers, so the lexicon's
    `punctuation_and_word_count` block is their one home and the fallbacks
    here only cover a lexicon predating it.
    """
    counts = load_ste_lexicon().get("punctuation_and_word_count", {})

    def cap(key, default):
        entry = counts.get(key)
        return entry.get("max_words", default) if isinstance(entry, dict) \
            else default
    return (cap("max_words_procedural_sentence", 20),
            cap("max_words_descriptive_sentence", 25))


def _paragraph_cap():
    """Max sentences per paragraph (Rule 6.6), same block, same contract."""
    entry = load_ste_lexicon().get("punctuation_and_word_count", {}) \
        .get("max_sentences_per_paragraph")
    return entry.get("max_sentences", 6) if isinstance(entry, dict) else 6


def check_sentence_lengths(text, mode=None, word_cap=None):
    """Return findings for sentences over the word-count limit.

    mode: 'procedural' (20 words) or 'descriptive' (25 words).
    If None, classifies each paragraph.

    word_cap: a voice profile's per-sentence cap, replacing both mode caps
    when set. The finding id still follows classification (the register
    tells you *why* the sentence is long); only the number is the profile's.
    """
    findings = []
    procedural_cap, descriptive_cap = _word_limits()
    offset = 0
    for para in text.split("\n\n"):
        stripped = para.strip()
        if not stripped:
            offset += len(para) + 2
            continue
        effective_mode = mode or classify_passage(stripped)
        if word_cap is not None:
            # int(), not int(word_cap): voice_check.py's mechanic_problems
            # only requires the mechanic to parse as float() ("30.5" passes),
            # and build_voice.py's own cap probe already coerces the same
            # field this way. int() alone raised ValueError on that shape.
            word_limit = int(float(word_cap))
        else:
            word_limit = (procedural_cap if effective_mode == "procedural"
                          else descriptive_cap)
        finding_id = ("ste-sentence-procedural"
                      if effective_mode == "procedural"
                      else "ste-sentence-descriptive")

        for sent in _split_sentences(stripped):
            n_words = count_words(sent)
            if n_words <= word_limit:
                continue
            # Line of the sentence, from character offsets. The first version
            # searched text.split("\n") for the paragraph's stripped first
            # line with .index(), which raises ValueError the moment a
            # paragraph is indented: 11 of the 100 corpus READMEs crashed on
            # exactly that.
            at = para.find(sent[:60])
            line = text.count("\n", 0, offset + (at if at >= 0 else 0)) + 1
            findings.append({
                "id": finding_id,
                "label": "%s sentence: %d words (limit %d)"
                         % (effective_mode, n_words, word_limit),
                "band": "craft",
                "priority": ste_priority(finding_id),
                "line": line,
                "match": sent[:80],
                "excerpt": ("Split this sentence. Voice profile cap: max %d "
                            "words per sentence." % word_limit
                            if word_cap is not None else
                            "Split this sentence. STE rules: %s text uses "
                            "max %d words per sentence."
                            % (effective_mode, word_limit)),
                "mode": effective_mode,
            })
        offset += len(para) + 2
    return findings


def check_paragraph_sentences(text):
    """Return findings for prose paragraphs over the sentence cap (Rule 6.6).

    A block that is mostly list items is not a paragraph, and
    `is_prose_block` is the engine's one notion of that: a 10-item bullet
    list is a legitimate 10 "sentences" and 6.6's answer to it is already
    the vertical list, so flagging it here would report the fix as the
    problem. One finding per offending paragraph, at its first line.

    Blocks are split on `\\n\\s*\\n`, the pattern scan.py's own
    `voice-paragraph-length` uses, and not on a literal blank line. A voice
    profile carrying `max_paragraph_sentences` stands this check down on the
    stated ground that the two report the same block, and a separator line
    carrying a space broke exactly that: one seven-sentence paragraph here,
    two short ones there, and the block reported by neither.
    """
    findings = []
    cap = _paragraph_cap()
    offset = 0
    for para in re.split(r"(\n\s*\n)", text):
        stripped = para.strip()
        if stripped and _is_prose_block(stripped):
            n = len(_split_sentences(stripped))
            if n > cap:
                line = text.count("\n", 0, offset + para.find(stripped)) + 1
                findings.append({
                    "id": "ste-paragraph-sentences",
                    "label": "paragraph of %d sentences (limit %d)" % (n, cap),
                    "band": "craft",
                    "priority": ste_priority("ste-paragraph-sentences"),
                    "line": line,
                    "match": stripped[:80],
                    "excerpt": ("Split this paragraph. STE rule 6.6: at most "
                                "%d sentences before a break." % cap),
                })
        # The separators come back from the split too, so the offset is the
        # exact length and never a literal two.
        offset += len(para)
    return findings


# ---------------------------------------------------------------------------
# Modal verb checks
# ---------------------------------------------------------------------------

# "May" the month, which a case-insensitive modal ban otherwise flags in
# every changelog: "Released in May 2026." Capitalized, followed by a
# digit or an ordinal day, or preceded by a month-position word.
_MAY_DATE_AFTER_RX = re.compile(r"\s+\d")
_MAY_DATE_BEFORE_RX = re.compile(
    r"(?i)\b(in|of|by|until|since|before|after|during|late|early|mid)[- ]$")


def check_modals(text):
    """Check for banned modal verbs (should/would/may/might/could).

    STE allows: can, will, must
    STE bans:  should, would, may, might, could
    """
    _ensure_regexes()
    findings = []
    for i, line in enumerate(text.split("\n"), 1):
        for m in _BANNED_MODALS_RX.finditer(line):
            word = m.group(0)
            if word == "May" and (
                    _MAY_DATE_AFTER_RX.match(line[m.end():])
                    or _MAY_DATE_BEFORE_RX.search(line[:m.start()])):
                continue
            findings.append({
                "id": "ste-modal",
                "label": "banned modal: '%s'" % word,
                "band": "craft",
                "priority": ste_priority("ste-modal"),
                "line": i,
                "match": word,
                "excerpt": ("STE bans '%s'. Modals that STE approves: "
                            "can, will, must. Rewrite as a direct statement "
                            "or use an approved modal." % word),
            })
    return findings


# ---------------------------------------------------------------------------
# -ing verb form checks
# ---------------------------------------------------------------------------

def check_ing_verbs(text):
    """Flag -ing verb forms after commas (gerund clause pattern).

    STE bans: "... , making it easy to ..."
    """
    _ensure_regexes()
    findings = []
    for i, line in enumerate(text.split("\n"), 1):
        for m in _ING_VERB_AFTER_COMMA_RX.finditer(line):
            word = m.group(1)
            findings.append({
                "id": "ste-ing-verb",
                "label": "-ing verb after comma: '%s'" % word,
                "band": "craft",
                "priority": ste_priority("ste-ing-verb"),
                "line": i,
                "match": m.group(0)[:80],
                "excerpt": ("STE bans -ing verb forms as clause openers "
                            "after a comma. Rewrite as two separate "
                            "sentences or restructure."),
            })
    return findings


# ---------------------------------------------------------------------------
# Condition-before-command checks
# ---------------------------------------------------------------------------

def check_condition_order(text):
    """Flag 'command ... if/when/unless' instead of 'if ... command'.

    STE rule: required conditions must come BEFORE the command.
    """
    _ensure_regexes()
    findings = []
    for i, line in enumerate(text.split("\n"), 1):
        for m in _CONDITION_ORDER_RX.finditer(line):
            match_str = m.group(0)
            if re.search(r"\b(?:is|are|was|were|has been|have been|will be)\b", match_str, re.I):
                continue
            findings.append({
                "id": "ste-condition-order",
                "label": "condition after command verb",
                "band": "craft",
                "priority": ste_priority("ste-condition-order"),
                "line": i,
                "match": match_str[:80],
                "excerpt": ("STE requires conditions BEFORE the command. "
                            "Rewrite: move the 'if/when/unless' clause to "
                            "the start. Example: 'If the flag is set, do X' "
                            "not 'Do X if the flag is set.'"),
            })
    return findings


# ---------------------------------------------------------------------------
# Banned verb checks (check/verify/confirm/ensure as verbs)
# ---------------------------------------------------------------------------

def check_banned_verbs(text):
    """Flag banned verbs: check, verify, confirm, ensure used as verbs.

    STE approved replacements:
      - check/verify/confirm -> 'make sure that' (state verification)
                                  OR 'examine' (look for faults)
                                  OR 'measure' (get a value)
      - ensure -> 'make sure that'
    """
    _ensure_regexes()
    findings = []
    for i, line in enumerate(text.split("\n"), 1):
        for m in _BANNED_VERBS_RX.finditer(line):
            word = m.group(0)
            findings.append({
                "id": "ste-banned-verb",
                "label": "banned verb used as verb: '%s'" % word,
                "band": "craft",
                "priority": ste_priority("ste-banned-verb"),
                "line": i,
                "match": word,
                "excerpt": ("STE bans '%s' as a verb. "
                            "Replace with: 'make sure that' (verify state), "
                            "'examine' (look for faults), or 'measure' "
                            "(get a value)." % word),
            })
    return findings


# ---------------------------------------------------------------------------
# Phrasal verb checks
# ---------------------------------------------------------------------------

def _phrasal_examples(lex):
    """{phrase: one-word replacement} from Rule 9.3's own worked examples.

    Rule 9.3 is a productive-grammar constraint: any two approved words can
    combine into a phrasal verb whose meaning is not approved, so there is no
    lookup table to enforce and the standard says so outright ("You will not
    usually find phrasal verbs listed as 'not approved' in the dictionary").
    A previous version of the lexicon shipped ~555 generic English phrasal
    verbs anyway, none of which exist in the Issue 9 PDF. What a regex *can*
    check is the rule's own worked examples, minus its named approved
    exceptions (PUT ON, COME ON, GO OFF), and that is all this does. The
    general constraint is a judgment call the report leaves to the writer.
    """
    block = lex.get("phrasal_verbs", {})
    approved = {k.lower() for k in block.get("approved_exceptions", {})
                if not k.startswith("_")}
    out = {}
    for example in block.get("worked_examples", []):
        phrase = " ".join(example.get("non_ste", "").split()[:2]).lower()
        replacement = (example.get("ste", "").split() or [""])[0]
        if phrase and replacement and phrase not in approved:
            out[phrase] = replacement
    return out


def check_phrasal_verbs(text):
    """Flag the phrasal verbs Rule 9.3 itself names. See _phrasal_examples."""
    _ensure_regexes()
    findings = []
    phrasal_map = _phrasal_examples(load_ste_lexicon())

    for i, line in enumerate(text.split("\n"), 1):
        for m in _PHRASAL_VERBS_RX.finditer(line):
            phrase = m.group(0)
            alt = phrasal_map.get(re.sub(r"\s+", " ", phrase.lower()))
            if not alt:
                continue
            findings.append({
                "id": "ste-phrasal-verb",
                "label": "phrasal verb: '%s'" % phrase,
                "band": "craft",
                "priority": ste_priority("ste-phrasal-verb"),
                "line": i,
                "match": phrase,
                "excerpt": ("STE bans phrasal verbs whose meaning is not the "
                            "approved meaning of their parts (Rule 9.3). "
                            "Replace '%s' with '%s'." % (phrase, alt)),
            })
    return findings


# ---------------------------------------------------------------------------
# Passive voice checks
# ---------------------------------------------------------------------------

_PASSIVE_NON_PARTICIPLES = frozenset({
    "often", "green", "seven", "even", "open", "screen", "queen", "alien",
    "citizen", "kitchen", "garden", "sudden", "heaven", "listen", "happen",
    "chicken", "golden", "wooden", "rotten", "sacred", "wicked", "naked",
    "crooked", "ragged", "hundred", "speed", "seed", "need", "bleed",
    "breed", "creed", "greed", "deed", "proceed", "exceed", "succeed",
    "then", "when", "men", "women", "children", "eleven", "dozen", "bed"
})


def check_passive(text):
    """Flag passive voice constructions (auxiliary + past participle).

    STE rule: use active voice.
    No per-line code guard here: this module receives the exempted copy, so
    code spans and fences are already blanked. The first version skipped any
    line carrying a backtick pair, which silenced "The value `x` was
    updated." entirely.
    """
    _ensure_regexes()
    findings = []
    for i, line in enumerate(text.split("\n"), 1):
        for m in _PASSIVE_RX.finditer(line):
            participle = m.group(2).lower()
            if participle in _PASSIVE_NON_PARTICIPLES:
                continue
            findings.append({
                "id": "ste-passive",
                "label": "passive voice",
                "band": "craft",
                "priority": ste_priority("ste-passive"),
                "line": i,
                "match": m.group(0),
                "excerpt": ("STE prefers active voice. "
                            "Rewrite with 'you', 'we', or the actor as "
                            "subject."),
            })
    return findings


# ---------------------------------------------------------------------------
# Semicolon checks
# ---------------------------------------------------------------------------

def check_semicolons(text):
    """Flag semicolons (banned by STE). One finding per line.

    Entities are blanked first, the way the voice semicolon rule does it:
    the `;` closing `&amp;` is markup, not punctuation.
    """
    findings = []
    for i, line in enumerate(_blank_entities(text).split("\n"), 1):
        if ";" in line:
            findings.append({
                "id": "ste-no-punctuation",
                "label": "semicolon used",
                "band": "craft",
                "priority": ste_priority("ste-no-punctuation"),
                "line": i,
                "match": ";",
                "excerpt": "STE bans semicolons. Write two sentences instead.",
            })
    return findings


# ---------------------------------------------------------------------------
# AI slop vocabulary checks
# ---------------------------------------------------------------------------

def check_ai_slop(text):
    """Flag AI-overused words from the word-swaps list."""
    _ensure_regexes()
    slop = load_ste_lexicon().get("ai_slop", {})
    findings = []
    for i, line in enumerate(text.split("\n"), 1):
        for m in _AI_SLOP_RX.finditer(line):
            word = m.group(0)
            key = word.lower()
            alt = slop.get(key.replace(" ", "_")) or slop.get(key)
            if not alt:
                continue
            findings.append({
                "id": "ste-vocab",
                "label": "AI overused word: '%s'" % word,
                "band": "craft",
                "priority": ste_priority("ste-vocab"),
                "line": i,
                "match": word,
                "excerpt": ("AI overused word. STE replacement: %s" % alt),
            })
    return findings


def check_dictionary_vocabulary(text):
    """Flag words the ASD-STE100 Issue 9 dictionary does not approve.

    Same `ste-vocab` id and priority as check_ai_slop, a different source: the
    dictionary_vocabulary block is the corpus-calibrated bulk word list
    scripts/ste-research/ builds from ste_dictionary_full.json, not the
    hand-picked ai_slop phrases. Kept as its own check rather than folded into
    check_ai_slop because that function's tests pin exact counts against the
    ai_slop list specifically, and a merge would make every one of those
    counts depend on whether a probe sentence happens to also contain a
    dictionary word.
    """
    _ensure_regexes()
    vocab = load_ste_lexicon().get("dictionary_vocabulary", {})
    findings = []
    for i, line in enumerate(text.split("\n"), 1):
        for m in _DICTIONARY_VOCAB_RX.finditer(line):
            word = m.group(0)
            norm_word = re.sub(r"\s+", " ", word.lower())
            alt = vocab.get(norm_word)
            if not alt:
                continue
            findings.append({
                "id": "ste-vocab",
                "label": "Not approved in ASD-STE100: '%s'" % word,
                "band": "craft",
                "priority": ste_priority("ste-vocab"),
                "line": i,
                "match": word,
                "excerpt": ("Not an approved ASD-STE100 dictionary word. "
                           "Approved alternative: %s" % alt),
            })
    return findings


# ---------------------------------------------------------------------------
# Run all STE checks
# ---------------------------------------------------------------------------

def check(text, mode=None, scope="all", word_cap=None):
    """Run STE structural checks against text.

    mode: 'procedural', 'descriptive', or None (classify per paragraph).
    Only the sentence-length check reads it: the limits are the one rule the
    two STE modes actually disagree on, and everything else in the standard
    applies to both.

    scope: 'mechanical' runs only what a script counts exactly (the ids in
    MECHANICAL_IDS), which is what every plain scan does. 'all' adds the
    advisory vocabulary checks behind --ste. An unknown value raises, the
    same way scan.scan's `ste=` does and for the same reason: silently
    reading as 'not all' is how a caller asking for the advisory band gets
    the mechanical one and no error.
    """
    if scope not in ("mechanical", "all"):
        raise ValueError("scope= must be 'mechanical' or 'all', not %r"
                         % (scope,))
    findings = []
    findings.extend(check_sentence_lengths(text, mode=mode, word_cap=word_cap))
    mechanical = (
        check_paragraph_sentences,
        check_condition_order,
        check_semicolons,
    )
    advisory = (
        check_modals,
        check_ing_verbs,
        check_banned_verbs,
        check_phrasal_verbs,
        check_ai_slop,
        check_dictionary_vocabulary,
        check_passive,
    )
    for checker in mechanical + (advisory if scope == "all" else ()):
        findings.extend(checker(text))
    return sorted(findings, key=lambda f: (f["line"], f["id"]))


def check_for_scan(text, mode=None, scope="all", word_cap=None):
    """Run STE checks and return findings in scan.py's findings schema.

    Adds 'ste_version' to each finding so scan.py can echo the lexicon
    version.
    """
    raw = check(text, mode=mode, scope=scope, word_cap=word_cap)
    for f in raw:
        f["ste_version"] = version()
    return raw
