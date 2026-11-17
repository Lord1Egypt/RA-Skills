#!/usr/bin/env python3
"""
scan.py - the mechanical layer of the rabbit-writes skill.

Finds what a regex and a counter find better than a reader does: copy-paste
fingerprints, tiered vocabulary density, and stylometric uniformity. Everything
requiring judgment lives in references/patterns.md and stays out of here.

This reports signals. It does not classify authorship, and it deliberately does
not emit a single "AI score" for the document. Detector audits report false
positive rates above 60% on non-native English writers (Liang et al., Stanford,
Patterns 2023). A number invites a verdict; a list of named findings invites a
check.

Findings come back in four bands:

    safety       concealed text, or text addressed to an agent. Never fixable,
                 never suppressible, and a P0 here stops --apply-safe dead.

    voice        this writer's own rules, from --voice-rules or --voice.
                 A hit is a defect.
    fingerprint  evidence the text came out of a chat tool.
    craft        general writing problems, never evidence about authorship.

This engine is calibrated on English. The tier lists are English words, the
sentence splitter breaks on English punctuation, and the stylometric bands come
from studies of English prose. It reports a note on a document that is mostly
another script and keeps going, because a bilingual README with an English
quickstart deserves an answer for the English half. It never fails on one.

Usage:
    python3 scan.py draft.md
    python3 scan.py draft.md --json
    python3 scan.py draft.md --sarif > scan.sarif
    python3 scan.py draft.md --profile technical-blog
    python3 scan.py draft.md --profile auto   # detect a register from structure
    python3 scan.py draft.md --voice-rules ../../rabbit-writes/voices/whit3rabbit.rules.json
    python3 scan.py draft.md --voice auto     # whichever profile this repo pins
    python3 scan.py draft.md --voice dana     # voices/dana.rules.json
    python3 scan.py --profile chat < input.txt
    python3 scan.py draft.md --no-exempt      # score quoted examples too
    python3 scan.py draft.md --apply-safe     # show the mechanical fixes
    python3 scan.py draft.md --apply-safe --write

No profile is applied unless one is asked for. That is deliberate rather than an
oversight: this script is what the `rabbit-scan` pre-commit hook runs, the hook
runs in somebody else's repository, and a stranger's em dash is not a defect in a
stranger's README. `--voice auto` is the opt-in.

A register profile relaxes the general rules. It never relaxes a voice rule:
lowercase and loose punctuation are fine off the clock, a banned phrase is not.

`--profile auto` is the same kind of opt-in as `--voice auto`: the default stays
DEFAULT_REGISTER unless auto is asked for by name, so an existing --profile-less
hook invocation is unaffected. Detection only fires for the handful of forms with
an unambiguous structural tell (docs, linkedin, formal);
everything else falls through to the default rather than guessing at a formality
band with no structural signal to back it.

Exit codes: 0 clean; 1 when --check is passed and a P0 finding is present; 2 when
a profile *named by hand*, with --voice-rules or `--voice <name>`, cannot be read
or does not parse, because silently scanning without the voice rules that were
asked for would report a clean voice band on a document nobody checked. A
`--voice auto` that finds no profile is a note and still exits 0: plenty of repos
have none, and failing there only teaches people to drop the flag.
Stdlib only; runs on Python 3.9+.
"""

import argparse
import json
import math
import os
import re
import stat
import sys
import tempfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
# rwlib sits beside this file and is not on anybody's PYTHONPATH: a plugin runs
# from wherever it was installed. Inserted rather than appended, so a stray
# `markdown` or `sections` module on the host's path cannot shadow ours.
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from rwlib import docx_text                      # noqa: E402
from rwlib import fixes as fixes_mod             # noqa: E402
from rwlib import ste as ste_mod                # noqa: E402
from rwlib import cli_error, facts, inflect, injection, language, registers, sarif, suppress  # noqa: E402
from rwlib import stylometry                       # noqa: E402
from rwlib import findings as findings_mod       # noqa: E402
from rwlib import lexicon as lexicon_mod         # noqa: E402
from rwlib import voices as voices_mod           # noqa: E402
from rwlib.artifacts import (HIDDEN_UNICODE, REPORT_ONLY_TOLERANCE,  # noqa: E402
                             REPORT_ONLY_UNICODE, SPACE_LIKE_TOLERANCE,
                             SPACE_LIKE_UNICODE, TAG_NAME, TAG_RX, VS_NAME,
                             VS_RX, occurrences, range_occurrences,
                             unlisted_invisibles)
# QUOTED_RX and SENTENCE_SENTINEL are re-exports rather than callers. Two
# tests assert `scan.QUOTED_RX is verify.QUOTED_RX` and pin the sentinel
# codepoint through this module, which is what makes "one home per fact"
# checkable from the outside instead of promised in a comment. Deleting them
# as unused takes the tripwire with them.
from rwlib.markdown import (BLOCKQUOTE_RX, CURLY_QUOTE_RX, FENCE_RX,  # noqa: E402,F401
                            FRONTMATTER_RX, HEADING_LINE_RX, INLINE_CODE_RX,
                            PROSE_DASH_RX, QUOTED_RX, TABLE_ROW_RX,
                            URL_GREEDY_RX, apply_exemptions, blank,
                            blank_entities, excerpt, invisible_entities,
                            is_prose_block, line_of)
from rwlib.markdown import strip_for_stats as md_strip_for_stats  # noqa: E402
from rwlib.sentences import (SENTENCE_SENTINEL, split_sentences,  # noqa: E402,F401
                             syllables, tokenize)

LEXICON_PATH = lexicon_mod.LEXICON_PATH

# The priority of a finding this engine raises itself, read out of the table in
# rwlib/lexicon.py at each call site. A catalogue pattern carries its own in its
# entry; these used to carry theirs as a string literal here, with the table
# beside them and a comment asking the next person to keep the two in step.
SYNTH = lexicon_mod.synthetic_priority

# The tolerance matrix, read from registers.json rather than restated here.
# These three names are what validate.py and the test suite check, and they used
# to be the second of three copies of the same fact: the first was prose in
# references/context.md and the third was a test that parsed that prose. See
# rwlib/registers.py.
#
# `blog` is the strict baseline and is the default register.
REGISTERS = registers.registers()
PROFILE_SKIP = registers.skip_table()
PROFILE_RELAX = registers.relax_table()
VOCAB_EXEMPT_PROFILES = registers.vocab_exempt_registers()
DEFAULT_REGISTER = registers.default_register()

# Human reference ranges. Sources: Copyleaks stylometric work (arXiv 2503.01659),
# classical type-token-ratio literature, and the ranges published by
# brandonwise/humanizer. Directional, not diagnostic.
BANDS = {
    "burstiness": (0.45, 1.10),   # sd/mean of sentence length
    "mattr": (0.62, 0.85),        # moving-average TTR, window 100
    "ttr": (0.40, 0.75),          # raw type-token ratio, length-sensitive
    "trigram_repetition": (0.0, 0.06),
    "em_dashes_per_1k": (0.0, 6.0),
}

RELIABILITY_TIERS = [
    (600, "high"),
    (250, "medium"),
    (120, "low"),
]

# Kept as a module-level name because the reference files talk about it. The
# definition lives in rwlib.markdown, beside the other table patterns, so
# verify.py and readme_check.py cannot end up disagreeing with it.
TABLE_RX = TABLE_ROW_RX


# --------------------------------------------------------------------------
# text preparation
# --------------------------------------------------------------------------

def strip_for_stats(text):
    """Remove code and markup noise before measuring prose statistics.

    Tables are dropped as well as code: a comparison table legitimately repeats
    the same cell values, and counting those repeats as trigram repetition or
    the cell separators as prose rhythm would measure the markup, not the
    writing.

    Headings and block quotes go with them. A heading is a label rather than a
    sentence, and a block quote is somebody else's prose: apply_exemptions
    already refuses to flag one, and a document that is half quotation used to
    report the rhythm of whoever it was quoting. Over patterns.md that is 599
    words and 57 "sentences" of other people's writing.

    List items are deliberately kept. They distort rhythm the same way a heading
    does, and dropping them costs too much to be worth it: checklist.md falls
    from 666 measured words to 91, under the 120-word floor, which silences every
    stylometric flag on exactly the list-heavy documents most worth measuring.
    A bullet is also prose a reader reads, which a `##` is not.

    The steps themselves live in rwlib.markdown, beside the patterns they run.
    `registers.detect_register` measures a word count with the same function,
    and a copy here would mean the register a document is scanned *as* and the
    statistics it is scanned *with* could disagree about what counts as prose.
    """
    return md_strip_for_stats(text)


# --------------------------------------------------------------------------
# statistics
# --------------------------------------------------------------------------

def moving_ttr(words, window=100):
    """Mean distinct-word ratio over every window-sized span of the text.

    The window slides rather than being rebuilt. Building a fresh set at each
    position is O(n x window), which nobody notices on a blog post and which
    crawls on a book-length document for a number that comes out identical."""
    if len(words) < window:
        return None
    counts = Counter(words[:window])
    positions = len(words) - window + 1
    distinct_total = len(counts)
    for i in range(1, positions):
        leaving = words[i - 1]
        counts[leaving] -= 1
        if not counts[leaving]:
            del counts[leaving]
        entering = words[i + window - 1]
        counts[entering] = counts.get(entering, 0) + 1
        distinct_total += len(counts)
    return distinct_total / positions / window


def compute_stats(raw_text):
    prose = strip_for_stats(raw_text)
    words = tokenize(prose)
    sentences = split_sentences(prose)
    paragraphs = [p for p in re.split(r"\n\s*\n", prose) if p.strip()]

    stats = {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs),
    }
    if not words or not sentences:
        return stats

    lengths = [len(tokenize(s)) for s in sentences]
    lengths = [n for n in lengths if n > 0]
    mean = sum(lengths) / len(lengths) if lengths else 0.0
    if len(lengths) > 1:
        var = sum((n - mean) ** 2 for n in lengths) / (len(lengths) - 1)
        sd = math.sqrt(var)
    else:
        sd = 0.0

    stats["avg_sentence_words"] = round(mean, 1)
    stats["sentence_sd"] = round(sd, 1)
    stats["burstiness"] = round(sd / mean, 3) if mean else 0.0
    stats["longest_sentence"] = max(lengths) if lengths else 0
    stats["shortest_sentence"] = min(lengths) if lengths else 0

    stats["ttr"] = round(len(set(words)) / len(words), 3)
    mattr = moving_ttr(words)
    stats["mattr"] = round(mattr, 3) if mattr is not None else None

    trigrams = [tuple(words[i:i + 3]) for i in range(len(words) - 2)]
    if trigrams:
        counts = Counter(trigrams)
        repeated = sum(c - 1 for c in counts.values() if c > 1)
        stats["trigram_repetition"] = round(repeated / len(trigrams), 4)
    else:
        stats["trigram_repetition"] = 0.0

    em = len(PROSE_DASH_RX.findall(prose))
    stats["em_dashes"] = em
    stats["em_dashes_per_1k"] = round(em / len(words) * 1000, 2)
    contractions = len(stylometry.CONTRACTION_RX.findall(prose))
    stats["contraction_rate"] = round(contractions / len(words) * 1000, 2)

    if paragraphs:
        plens = [len(split_sentences(p)) for p in paragraphs]
        pmean = sum(plens) / len(plens)
        if len(plens) > 1:
            psd = math.sqrt(sum((n - pmean) ** 2 for n in plens) / (len(plens) - 1))
        else:
            psd = 0.0
        stats["avg_paragraph_sentences"] = round(pmean, 1)
        stats["paragraph_sd"] = round(psd, 2)

    syl = sum(syllables(w) for w in words)
    stats["flesch_kincaid_grade"] = round(
        0.39 * (len(words) / len(sentences)) + 11.8 * (syl / len(words)) - 15.59, 1
    )
    return stats


def reliability(word_count):
    for threshold, label in RELIABILITY_TIERS:
        if word_count >= threshold:
            return label
    return "insufficient"


# --------------------------------------------------------------------------
# findings
# --------------------------------------------------------------------------

def find(text, rx, pattern_id, label, band, priority, findings, allowed=0):
    """`allowed` is the register's tolerance: the first N hits pass unreported
    and everything past them is a finding. 0 means report every hit."""
    hits = [m for m in rx.finditer(text) if m.group(0).strip()]
    for m in hits[allowed:]:
        findings.append(findings_mod.make(
            pattern_id, label, band, priority, line_of(text, m.start()),
            match=m.group(0).strip()[:80],
            excerpt=excerpt(text, m.start(), m.end())))


# Escaped, not literal. The variation selector (U+FE0F) is invisible as a
# literal, and an editor that drops it silently stops this pattern matching the
# emoji presentation form.
#
# Three alternatives, because an emoji is not only a character in one of the
# pictographic blocks. A keycap is an ASCII digit plus U+FE0F plus U+20E3, and
# the trademark and copyright signs become emoji the same way. The selector
# alone is not an emoji and must not match on its own, which is what the
# alternation buys over putting U+FE0F in the class.
EMOJI_RX = re.compile(
    "[" "\U0001F300-\U0001FAFF" "\u2600-\u27BF" "\U0001F900-\U0001F9FF"
    "\u2B00-\u2BFF" "\U0001F1E6-\U0001F1FF" "\U0001F004\U0001F0CF" "]\uFE0F?"
    "|[0-9#*]\uFE0F?\u20E3"
    "|[\u00A9\u00AE\u2122\u2194-\u2199\u21A9-\u21AA\u231A-\u231B\u23E9-\u23FA\u25AA-\u25FE\u2934-\u2935]\uFE0F")
# Two lookbehinds rather than one, because `re` fixes their width: with only the
# one-space form, a two-space typist's emphatic fragments were never checked at
# all, which is a rule that silently does not apply to whoever writes that way.
ONE_WORD_SENTENCE_RX = re.compile(
    r"(?m)(?:^|(?<=[.!?]\s)|(?<=[.!?]\s\s))([A-Z][a-z']{1,14})\.(?=\s|$)")
# Titles and abbreviations that this pattern would otherwise read as a one-word
# sentence: "...ran late. Dr. Smith arrived" is a name, not emphasis. Narrower
# than ABBREV_RX on purpose. `No.` is left out because a bare "No." in prose is
# almost always the emphatic sentence this rule exists to catch, and almost
# never the abbreviation for number.
ONE_WORD_ABBREV_RX = re.compile(
    r"(Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|Inc|Ltd|Fig|Vol|Dept|Approx|Est)\.")
US_DATE_RX = facts.DATE_US_RX
DMY_DATE_RX = facts.DATE_DMY_RX
ISO_DATE_RX = facts.DATE_ISO_RX


# Serial-comma candidates. OXFORD_MISSING_RX wants a comma, then a run with no
# comma in it, then the conjunction: "eggs, bacon and toast". OXFORD_PRESENT_RX
# wants that same run with the comma sitting after it: "eggs, bacon, and toast".
#
# Both sides carry the same two guards. The stop-word lookahead drops clauses
# that open with a conjunction or a relative pronoun, and the three-word ceiling
# drops the rest: a serial list item is short, a subordinate clause is not.
#
# Without them the missing side reports on the far-away "or" in "more examples,
# and the checklist at the end of any draft or edit", and every
# correctly-punctuated two-item list becomes a finding. Without them the present
# side is worse still: a bare `,\s+(?:and|or)` matches every compound sentence in
# the language, and "She left the room, and he stayed" is required punctuation,
# not a serial comma. Requiring a comma-delimited short run in front of the
# conjunction is what distinguishes the third item of a list from a second
# clause.
#
# The cost is real and deliberate on both sides. "eggs, a thick slice of bacon
# and toast" is a genuine miss, and so is its mirror. An advisory that fires on a
# third of a page gets ignored along with the hits, and TEMPLATE.rules.json
# promises advice here, not enforcement.
OXFORD_CLAUSE_OPENER = ("and|or|which|who|whom|whose|that|because|since|so|but|"
                        "before|after|while|when|where|if|though|although|"
                        "unless|until|whether")
OXFORD_MISSING_RX = re.compile(
    r",\s+(?!(?:%s)\b)(?:[^\s,;:.!?]+\s+){0,2}[^\s,;:.!?]+\s+(?:and|or)\s+\w"
    % OXFORD_CLAUSE_OPENER)
OXFORD_PRESENT_RX = re.compile(
    r",\s+(?!(?:%s)\b)(?:[^\s,;:.!?]+\s+){0,2}[^\s,;:.!?]+,\s+(?:and|or)\s+\w"
    % OXFORD_CLAUSE_OPENER)
OXFORD_MAX_REPORTED = 5

LIST_DASH_RX = re.compile(
    r"^\s*(?:[-*+]|\d+[.)])\s+(?:\*\*[^*]+\*\*|\[[^\]]+\]\([^)]+\)|`[^`]+`)\s*(?:[—–]|&[mn]dash;|&#821[12];)\s")


def in_list_typography(text, index):
    """True when this dash separates a bolded lead term in a list item
    (`- **Term** — description`). That is typography, not a prose splice, and
    the general em-dash rule already carves it out. A voice ban should agree.

    Checked against the raw text rather than the exemption-blanked copy, so a
    list item leading with an inline-code term still reads as a list item.
    Blanking preserves length, so the offsets line up."""
    start = text.rfind("\n", 0, index) + 1
    end = text.find("\n", index)
    if end < 0:
        end = len(text)
    return bool(LIST_DASH_RX.match(text[start:end]))


def voice_finding(rules_id, label, priority, line, match, excerpt_text):
    return findings_mod.make(rules_id, label, "voice", priority, line,
                             match=match, excerpt=excerpt_text)


def voice_mechanics(rules, register):
    """The mechanics in force for this register.

    `mechanics` is the writer's baseline and `mechanics_by_register` is where
    they say what changes off the clock:

        "mechanics": {"one_word_sentence": "forbid", "emoji": "forbid"},
        "mechanics_by_register": {"chat": {"one_word_sentence": "allow"}}

    This does not break the rule that a register never relaxes a voice rule. It
    is the opposite direction. `--profile chat` still cannot soften anything;
    what it can do now is select which of the writer's own rules the writer said
    applied there. The profile markdown has always drawn this line ("on the
    clock: full polish, off the clock: relaxed, lowercase"), and until now the
    rules file had no way to say it, so the enforceable half was making a promise
    against the readable half.

    Merged key by key over the baseline, so an override names only what moves.
    """
    mech = dict(rules.get("mechanics", {}))
    mech.update(rules.get("mechanics_by_register", {}).get(register, {}))
    return mech


def in_register(entry, register):
    """Whether a rules entry applies to the register being scanned.

    An entry that says nothing applies everywhere, which is what keeps every
    profile written before this key existed behaving exactly as it did.
    """
    applies_to = entry.get("applies_to_registers")
    return not applies_to or register in applies_to


def apply_voice_rules(scored, raw_text, rules, stats, findings):
    """Enforce one writer's own rules. These sit above the register profile:
    a register can relax a general rule, never a voice rule. A writer can scope
    their own rule to a register, which is a different thing: see
    voice_mechanics."""
    default = rules.get("default_priority", "P0")
    register = stats.get("_profile")
    mech = voice_mechanics(rules, register)
    subs = rules.get("preferred_substitutions", {})

    def fix_hint(term):
        key = term.lower().strip()
        return "use %s" % subs[key] if key in subs else "cut it or say the specific thing"

    # Punctuation and formatting mechanics.
    if mech.get("em_dash") == "forbid":
        for m in PROSE_DASH_RX.finditer(scored):
            if in_list_typography(raw_text, m.start()):
                continue
            findings.append(voice_finding(
                "voice-em-dash", "Em dash (voice forbids)", default,
                line_of(scored, m.start()), m.group(0),
                excerpt(scored, m.start(), m.end())))
    elif mech.get("em_dash") == "limit":
        cap = float(mech.get("max_em_dashes_per_1000w", 2))
        rate = stats.get("em_dashes_per_1k", 0)
        if rate > cap:
            findings.append(voice_finding(
                "voice-em-dash-rate", "Em-dash rate %.1f/1k over voice cap %.1f"
                % (rate, cap), default, 1, "%d dashes" % stats.get("em_dashes", 0),
                "This writer uses em dashes, but not this many."))

    if mech.get("semicolon") == "forbid":
        # Positions taken from a copy with the character references blanked, and
        # everything reported out of `scored`. `&amp;` and `&nbsp;` each end in a
        # semicolon that is markup rather than punctuation, and a header block
        # full of them used to report a finding apiece. Blanking preserves
        # length, so the offsets still point at the same characters.
        for m in re.finditer(r";", blank_entities(scored)):
            findings.append(voice_finding(
                "voice-semicolon", "Semicolon (voice forbids)", default,
                line_of(scored, m.start()), ";",
                excerpt(scored, m.start(), m.end())))

    if mech.get("emoji") == "forbid":
        for m in EMOJI_RX.finditer(scored):
            findings.append(voice_finding(
                "voice-emoji", "Emoji (voice forbids)", default,
                line_of(scored, m.start()), m.group(0),
                excerpt(scored, m.start(), m.end())))

    if mech.get("curly_quotes") == "forbid":
        # Raw text, for the reason in lexicon.json's curly-quote entry: the
        # exemption blanks a quoted span along with the quote marks that are
        # the thing being checked. The excerpt has to come from raw_text for the
        # same reason, or a quote inside an exempted span reports a line of
        # blanks. Blanking preserves length, so the offsets line up either way.
        for m in CURLY_QUOTE_RX.finditer(raw_text):
            findings.append(voice_finding(
                "voice-curly-quote", "Curly quote (voice forbids)", "P2",
                line_of(raw_text, m.start()), m.group(0),
                excerpt(raw_text, m.start(), m.end())))

    # Serial comma. Advisory: reported, never enforced at the voice default,
    # because no regex tells a three-item list from a compound sentence.
    style = mech.get("oxford_comma", "allow")
    if style in ("require", "forbid"):
        rx = OXFORD_MISSING_RX if style == "require" else OXFORD_PRESENT_RX
        label = ("Serial comma missing (voice requires it)" if style == "require"
                 else "Serial comma present (voice omits it)")
        hits = list(rx.finditer(scored))
        for m in hits[:OXFORD_MAX_REPORTED]:
            findings.append(voice_finding(
                "voice-oxford-comma", label, "P2",
                line_of(scored, m.start()), m.group(0).strip()[:60],
                "Advisory. Check it is a list and not a compound sentence "
                "before touching it: " + excerpt(scored, m.start(), m.end())))
        if len(hits) > OXFORD_MAX_REPORTED:
            findings.append(voice_finding(
                "voice-oxford-comma",
                "%s, %d more sites" % (label, len(hits) - OXFORD_MAX_REPORTED),
                "P2", 1, "%d candidates" % len(hits),
                "Advisory. Read them rather than running a replace."))

    if mech.get("one_word_sentence") == "forbid":
        for m in ONE_WORD_SENTENCE_RX.finditer(scored):
            if ONE_WORD_ABBREV_RX.fullmatch(m.group(0)):
                continue
            findings.append(voice_finding(
                "voice-one-word-sentence",
                "One-word sentence for emphasis (voice forbids)", default,
                line_of(scored, m.start()), m.group(0),
                "Reads harsh. Fold it into the sentence that follows."))

    fmt = mech.get("date_format", "any")
    if fmt == "dmy":
        for m in US_DATE_RX.finditer(scored):
            findings.append(voice_finding(
                "voice-date-format", "US date format (voice wants day-month-year)",
                default, line_of(scored, m.start()), m.group(0),
                "Write it as 12 September 2025."))
    elif fmt == "mdy":
        for m in DMY_DATE_RX.finditer(scored):
            findings.append(voice_finding(
                "voice-date-format", "Day-month-year (voice wants month-day-year)",
                default, line_of(scored, m.start()), m.group(0), ""))
    elif fmt == "iso":
        for m in list(US_DATE_RX.finditer(scored)) + list(DMY_DATE_RX.finditer(scored)):
            findings.append(voice_finding(
                "voice-date-format", "Spelled date (voice wants ISO)", default,
                line_of(scored, m.start()), m.group(0), "Write it as 2025-09-12."))

    _p_cap = mech.get("max_paragraph_sentences")
    try:
        p_cap_val = int(_p_cap) if _p_cap is not None else 0
    except (ValueError, TypeError):
        p_cap_val = 0
    if p_cap_val > 0:
        offset = 0
        for para in re.split(r"(\n\s*\n)", scored):
            body = para.strip()
            if body and is_prose_block(body):
                n = len(split_sentences(body))
                if n > p_cap_val:
                    findings.append(voice_finding(
                        "voice-paragraph-length",
                        "Paragraph of %d sentences (voice cap %s)" % (n, _p_cap),
                        default, line_of(scored, offset), "%d sentences" % n,
                        "Break it. Dense blocks read as machine output."))
            offset += len(para)

    _a_cap = mech.get("max_avg_sentence_words")
    try:
        a_cap_val = float(_a_cap) if _a_cap is not None else 0.0
    except (ValueError, TypeError):
        a_cap_val = 0.0
    if a_cap_val > 0 and stats.get("avg_sentence_words", 0) > a_cap_val:
        findings.append(voice_finding(
            "voice-sentence-length",
            "Average sentence %.1f words (voice cap %s)"
            % (stats["avg_sentence_words"], _a_cap), default, 1,
            "avg sentence length", "This writer writes shorter than this."))

    # Word and phrase bans. Flattened through rwlib.inflect, which turns an
    # entry that asked for it into the term plus its regular s/es/ed/ing forms
    # and leaves a plain string exactly as written. A profile using neither
    # feature reaches word_regex with the same list it always did.
    if rules.get("banned_words"):
        words = inflect.expand(rules["banned_words"])
        for m in lexicon_mod.word_regex(words).finditer(scored):
            findings.append(voice_finding(
                "voice-banned-word", "Banned word", default,
                line_of(scored, m.start()), m.group(0),
                fix_hint(m.group(0))))

    if rules.get("banned_phrases"):
        phrases = inflect.expand(rules["banned_phrases"])
        for m in lexicon_mod.phrase_regex(phrases).finditer(scored):
            findings.append(voice_finding(
                "voice-banned-phrase", "Banned phrase", default,
                line_of(scored, m.start()), m.group(0),
                fix_hint(m.group(0))))

    # Custom regexes, including overuse rules that allow N hits before flagging.
    for entry in rules.get("banned_regex", []):
        # Scoped the same way required_when is, and for the same reason: a rule
        # about how a writer signs off, or about lowercase openers, is a rule
        # about a context rather than about the whole person.
        if not in_register(entry, register):
            continue
        try:
            rx = re.compile(entry["rx"])
        except (re.error, KeyError) as exc:
            print("voice-rules: bad entry %s (%s)" % (entry.get("id"), exc),
                  file=sys.stderr)
            continue
        hits = [m for m in rx.finditer(scored) if m.group(0).strip()]
        allowed = int(entry.get("max_allowed", 0))
        if len(hits) <= allowed:
            continue
        note = entry.get("note", "")
        for m in hits[allowed:]:
            label = entry.get("label", entry["id"])
            if allowed:
                label = "%s (%d uses, cap %d)" % (label, len(hits), allowed)
            findings.append(voice_finding(
                entry["id"], label, entry.get("priority", default),
                line_of(scored, m.start()), m.group(0).strip()[:60],
                note or excerpt(scored, m.start(), m.end())))

    # Presence checks. Advisory by design: a fragment has no sign-off.
    # `when_rx` gates the check so it only runs on text of the right shape.
    # Without a gate, "missing closer" fires on every document that is not a
    # letter, which is most of them.
    for entry in rules.get("required_when", []):
        if not in_register(entry, register):
            continue
        gate = entry.get("when_rx")
        if gate and not re.search(gate, scored):
            continue
        found = any(re.search(rx, scored) for rx in entry.get("any_of_rx", []))
        if not found:
            findings.append(voice_finding(
                entry["id"], entry.get("label", entry["id"]),
                entry.get("priority", "P2"), 1, "not found",
                entry.get("note", "")))

    # Signature moves. Ceiling and floor checks, reported at P2 always.
    words = stats.get("word_count", 0)
    for entry in rules.get("signature_moves", []):
        if not in_register(entry, register):
            continue
        try:
            rx = re.compile(entry["rx"])
        except (re.error, KeyError) as exc:
            print("voice-rules: bad signature move entry %s (%s)" % (entry.get("id"), exc),
                  file=sys.stderr)
            continue
        hits = [m for m in rx.finditer(scored) if m.group(0).strip()]
        count = len(hits)
        rate = (count / words * 1000.0) if words > 0 else 0.0
        label = entry.get("label", entry["id"])
        note = entry.get("note", "")

        max_allowed = entry.get("max_allowed")
        if max_allowed is not None and count > int(max_allowed):
            allowed = int(max_allowed)
            label_msg = "%s (%d uses, cap %d)" % (label, count, allowed)
            for m in hits[allowed:]:
                findings.append(voice_finding(
                    entry["id"], label_msg, "P2",
                    line_of(scored, m.start()), m.group(0).strip()[:60],
                    note or excerpt(scored, m.start(), m.end())))

        max_per_1000w = entry.get("max_per_1000w")
        if max_per_1000w is not None and rate > float(max_per_1000w):
            cap_rate = float(max_per_1000w)
            label_msg = "%s: rate %.1f/1k over cap %.1f" % (label, rate, cap_rate)
            findings.append(voice_finding(
                entry["id"], label_msg, "P2", 1,
                "%d uses" % count,
                note or "Signature move used more frequently than voice cap."))

        # The floor needs a document long enough for a rate to mean anything,
        # which is the same threshold every other rate in the engine uses. A
        # literal here is a second copy of stylometry.RELIABLE_WORDS.
        min_per_1000w = entry.get("min_per_1000w")
        if (min_per_1000w is not None
                and words >= stylometry.RELIABLE_WORDS
                and rate < float(min_per_1000w)):
            floor_rate = float(min_per_1000w)
            label_msg = "%s: rate %.1f/1k below voice floor %.1f" % (label, rate, floor_rate)
            findings.append(voice_finding(
                entry["id"], label_msg, "P2", 1,
                "%d uses" % count,
                note or "Signature move under-used for document length."))


def apply_voice_distance(raw_text, fingerprint, stats, findings):
    """How far this document sits from how the profile's owner writes.

    The one voice measurement that is not a refusal. Everything else in the
    band is a rule a document either breaks or does not, and a document can
    clear all of them and still sound like nobody. This is the number for that,
    calibrated against the writer's own samples: `references/voice.md` and
    rwlib/stylometry.py carry the reasoning.

    Three deliberate limits, all of them about not overclaiming:

      P2, always, and never a `--check` failure. A writer is allowed to sound
      unlike themselves on purpose, and a distance that blocked a commit would
      be the humanizer-shaped failure this plugin exists to avoid.

      Reported only past the reliability floor. Under it the marker rates are
      sampling noise, the same reason scan.py labels a short document.

      Reported only when the document is further from the profile than any of
      the writer's own samples are from each other. `near` is a real reading
      and it is not a finding: half the corpus would carry one.

    The measurement lands in `stats` whatever the verdict, so a rewrite loop can
    read the before and after numbers without parsing a report. Measured over
    the stripped prose, the copy compute_stats measures, because a code fence
    has no function words in it and counting one as register would make every
    documented API read like a stranger.
    """
    try:
        measured = stylometry.distance(fingerprint, strip_for_stats(raw_text))
    except ValueError as exc:
        # A fingerprint written by a different marker list. Reported on stderr
        # and dropped, the way lexicon.py drops a pattern that will not
        # compile: one stale optional file should cost its own measurement and
        # not the scan somebody is waiting on.
        print("scan: %s" % exc, file=sys.stderr)
        return
    stats["voice_distance"] = measured
    if not measured["reliable"] or measured["verdict"] != "out_of_range":
        return

    top = ", ".join("%s %+.1fsd" % (c["marker"], c["z"])
                    for c in measured["contributors"][:3])
    findings.append(voice_finding(
        "voice-distance",
        "Register distance %.2f, this writer's own samples sit under %.2f"
        % (measured["delta"], measured["band"]["max"]), "P2", 1,
        "%d markers off profile" % len(measured["contributors"]),
        "Furthest markers: %s. A signal about register, never a defect: a "
        "writer may sound unlike themselves on purpose, and this cannot tell "
        "that from a conversion that did not land." % top))


def scan(raw_text, profile=None, exempt=True, voice_rules=None,
         suppressions=True, voice_fingerprint=None, ste="mechanical",
         ste_mode=None):
    """`suppressions=False` leaves the inline `rabbit-allow` comments alone.

    readme_check.py passes it, because it merges these findings with its own
    structure findings and then runs one suppression pass over the whole list.
    Run here as well, it would audit the same comments twice, and report a
    suppression naming a structure id as covering nothing: this function cannot
    see the half of the report that id belongs to.

    `ste` is a tri-state, not the boolean it once was: 'mechanical' (the
    default) runs the counted rules in every scan, 'all' adds the advisory
    vocabulary band behind --ste, 'off' silences the lot. Unknown values
    raise here rather than reading as false, which would have made --no-ste
    a silent no-op.
    """
    if ste not in ("off", "mechanical", "all"):
        raise ValueError(
            "ste= must be 'off', 'mechanical', or 'all', not %r. The boolean "
            "form is gone: --ste maps to 'all' and every plain scan runs "
            "'mechanical'." % (ste,))
    profile = profile or DEFAULT_REGISTER
    lex = lexicon_mod.load()
    scored = apply_exemptions(raw_text) if exempt else raw_text
    skip = set(PROFILE_SKIP.get(profile, set()))
    ste_word_cap = None
    if voice_rules:
        mech = voice_mechanics(voice_rules, profile)
        if mech.get("double_hyphen") == "allow":
            skip.add("double-hyphen-dash")
        # The profile wins every conflict with STE, the same way it wins
        # against double-hyphen-dash just above. A semicolon mechanic that
        # is present is a ruling whichever way it reads: 'allow' is the
        # writer's own sentence shape, and 'forbid' already flags every
        # occurrence at the voice's priority, so the ste copy underneath is
        # noise about the same character.
        if mech.get("semicolon") is not None:
            skip.add("ste-no-punctuation")
        # A profile that sets its own paragraph cap has ruled on paragraph
        # length (voice-paragraph-length enforces it); the STE 6.6 copy
        # would double-report the same block.
        _p_cap = mech.get("max_paragraph_sentences")
        if _p_cap is not None:
            try:
                if int(_p_cap) > 0:
                    skip.add("ste-paragraph-sentences")
            except (ValueError, TypeError):
                pass
        # A per-sentence cap replaces the STE 20/25 caps outright, in both
        # directions: stricter than STE is the writer's choice, looser
        # keeps the monsters flagged past the profile's own number.
        # A profile carrying a zero means the key is unset everywhere else in
        # this function, and honoured here it would cap every sentence in the
        # document at nothing. Checked as a float, not by truthiness: JSON's
        # own `"0"` string form is truthy in Python and `or None` let it
        # through as a live zero-word cap, flagging every non-empty sentence.
        _cap = mech.get("max_sentence_words")
        ste_word_cap = None if _cap is None or float(_cap) == 0 else _cap
    relax = PROFILE_RELAX.get(profile, {})
    findings = []
    stats = compute_stats(raw_text)
    stats["_profile"] = profile

    # 1. Hidden unicode. Checked on the raw text; exemptions do not apply,
    #    because a zero-width space inside a code fence is still a paste artifact.
    #    Offsets rather than a bare count, so the reported line is the first
    #    occurrence that actually counted rather than the first one in the file,
    #    and so the emoji-joiner carve-out has something to filter. fixes.py
    #    counts the same way, or the two disagree about whether a rule fired.
    #    Gated on `skip` like every other finding the engine raises itself. No
    #    register asks for it today, and until this line existed none could: the
    #    loop ran before anything read the skip set, so a cell naming
    #    hidden-unicode in registers.json would have been a silent no-op that
    #    read in the rendered matrix as a tolerance somebody was honouring.
    for ch, name in (HIDDEN_UNICODE.items() if "hidden-unicode" not in skip else []):
        at = occurrences(raw_text, ch)
        n = len(at)
        space_like = ch in SPACE_LIKE_UNICODE
        if space_like and n <= SPACE_LIKE_TOLERANCE:
            continue
        if n:
            findings.append(findings_mod.make(
                "hidden-unicode", "Hidden unicode: %s" % name, "fingerprint",
                # The table names the worst this id reaches. The space-like half
                # is softer, and says so here rather than in the table, because
                # a register reading the table needs the ceiling.
                "P2" if space_like else SYNTH("hidden-unicode"),
                line_of(raw_text, at[0]),
                match="U+%04X x%d" % (ord(ch), n),
                excerpt=("%d of them, past the %d a typesetter would use. "
                         "Check they are deliberate before replacing them."
                         % (n, SPACE_LIKE_TOLERANCE) if space_like
                         else "%d occurrence(s) of %s" % (n, name))))

    # 1b. The concealment tables, same id and same skip gate. Everything here
    #     is softer than the P0 above and says so at the call site, the way the
    #     space-like half does: these characters have honest uses (RTL
    #     typography, CJK variation sequences, braille art), so a bare presence
    #     is a P1 to read, not a P0 to strip, and the fixer never touches them.
    #     The one exception is the Unicode Tags block, which has no honest use
    #     at any count: runs long enough to decode into words are
    #     injection-tag-smuggling P0s in the safety band, and what is reported
    #     here is only the residue below that threshold, so the two detectors
    #     tile the block with no gap and no double count.
    if "hidden-unicode" not in skip:
        for ch, name in REPORT_ONLY_UNICODE.items():
            at = occurrences(raw_text, ch)
            allowed = REPORT_ONLY_TOLERANCE.get(ch, 0)
            if not at or len(at) <= allowed:
                continue
            findings.append(findings_mod.make(
                "hidden-unicode", "Hidden unicode: %s" % name, "fingerprint",
                "P2" if allowed else "P1", line_of(raw_text, at[0]),
                match="U+%04X x%d" % (ord(ch), len(at)),
                excerpt=("%d of them, past the %d honest typography uses. "
                         "Check they are deliberate before replacing them."
                         % (len(at), allowed) if allowed else
                         "%d occurrence(s) of %s. Never auto-removed: "
                         "deleting one from a document that needs it breaks "
                         "its rendering. Read the span and decide."
                         % (len(at), name))))

        smuggled = [(at, at + len(msg))
                    for at, msg in injection.tag_runs(raw_text)]
        tag_at = [i for i in range_occurrences(raw_text, TAG_RX)
                  if not any(lo <= i < hi for lo, hi in smuggled)]
        if tag_at:
            findings.append(findings_mod.make(
                "hidden-unicode", "Hidden unicode: %s" % TAG_NAME,
                "fingerprint", SYNTH("hidden-unicode"),
                line_of(raw_text, tag_at[0]),
                match="U+E0001-U+E007F x%d" % len(tag_at),
                excerpt="%d character(s) in the invisible Unicode Tags block, "
                        "too few to decode into a message. No honest use at "
                        "any count." % len(tag_at)))

        vs_at = range_occurrences(raw_text, VS_RX)
        if vs_at:
            findings.append(findings_mod.make(
                "hidden-unicode", "Hidden unicode: %s" % VS_NAME,
                "fingerprint", "P1", line_of(raw_text, vs_at[0]),
                match="U+FE00-U+FE0D/U+E0100-U+E01EF x%d" % len(vs_at),
                excerpt="%d variation selector(s) outside emoji presentation. "
                        "Honest in CJK ideograph variation sequences; a run in "
                        "other text is a byte-per-character data channel."
                        % len(vs_at)))

        for ch, at in sorted(unlisted_invisibles(raw_text).items()):
            findings.append(findings_mod.make(
                "hidden-unicode", "Hidden unicode: unlisted format or control "
                "character", "fingerprint", "P1", line_of(raw_text, at[0]),
                match="U+%04X x%d" % (ord(ch), len(at)),
                excerpt="An invisible character no table in this engine names. "
                        "Escape sequences and stray controls land here, which "
                        "covers ANSI terminal injection."))

        # An entity spelling of an invisible character renders identically, so
        # it counts identically: PROSE_DASH_RX's reasoning, pointed the other
        # way. Softer than the literal, because the entity is at least visible
        # in the raw source. Scored against the exempted copy, unlike every
        # literal above and for placeholder's reason rather than
        # citation-leak's: a fence renders as code, so an entity inside one
        # never renders invisible, and `&#8203;` in backticks is a document
        # explaining the trick. This file's own changelog was the first false
        # positive.
        by_entity = {}
        for m, ch in invisible_entities(scored):
            by_entity.setdefault(m.group(0), []).append(m.start())
        for ent, at in sorted(by_entity.items()):
            findings.append(findings_mod.make(
                "hidden-unicode", "Hidden unicode spelled as %s" % ent,
                "fingerprint", "P1", line_of(raw_text, at[0]),
                match="%s x%d" % (ent, len(at)),
                excerpt="A character reference that renders as an invisible "
                        "character. Visible in the source, invisible on the "
                        "page."))

    # 2. Catalog regexes.
    for p, rx in lexicon_mod.compiled_patterns(skip=skip):
        allowed = relax.get(p["id"], 0)
        label = p["label"]
        if allowed:
            label = "%s (past the %s allowance of %d)" % (label, profile, allowed)
        # A pattern marked scan_raw is about how the file was produced rather
        # than what it says, so the quoted-example exemption does not apply.
        # Blanking preserves length, so the line numbers agree either way.
        target = raw_text if p.get("scan_raw") else scored
        find(target, rx, p["id"], label, p["band"], p["priority"], findings,
             allowed=allowed)

    # 3. Vocabulary, tiered. Tier 1 always flags. Clarity edits are reported in
    #    their own band and never counted toward the AI-vocabulary signal, so a
    #    wordiness fix can never look like authorship evidence.
    # `technical_exempt` is the base for every partial cell. A register may name
    # one further list, which is added to it: `academic` drops `paradigm` while
    # `technical-blog` keeps flagging it, and putting those words in the shared
    # list instead would have exempted them in a tech blog, where a new paradigm
    # for observability is exactly the tier-1 usage the list exists to catch.
    technical = profile in VOCAB_EXEMPT_PROFILES
    exempt_words = set(w.lower() for w in lex["technical_exempt"]) if technical else set()
    extra = VOCAB_EXEMPT_PROFILES.get(profile) if technical else None
    if extra:
        exempt_words |= set(w.lower() for w in lex[extra])

    if "tier1" not in skip:
        t1 = [w for w in lex["tier1"] if w.lower() not in exempt_words]
        # Phrases first, then the word pass over a copy with their spans blanked.
        # `delve into` is on both lists, so run the other way round it was two P1
        # findings about one token: the phrase takes its span first, the way
        # facts.numbers() orders its takes. Blanking preserves length and
        # newlines, so lines and excerpts are the same either way.
        t1_phrases = lexicon_mod.phrase_regex(lex["tier1_phrases"])
        find(scored, t1_phrases, "tier1", "Tier-1 phrase",
             "fingerprint", SYNTH("tier1"), findings)
        find(t1_phrases.sub(blank, scored), lexicon_mod.word_regex(t1),
             "tier1", "Tier-1 vocabulary", "fingerprint", SYNTH("tier1"),
             findings)

    if "clarity" not in skip:
        find(scored, lexicon_mod.word_regex(lex["clarity"]), "clarity", "Wordiness",
             "craft", SYNTH("clarity"), findings)
        find(scored, lexicon_mod.phrase_regex(lex["clarity_phrases"]), "clarity",
             "Wordiness", "craft", SYNTH("clarity"), findings)

    # Tier 2 fires only when two or more land in the same paragraph.
    if "tier2-cluster" not in skip:
        t2 = [w for w in lex["tier2"] if w.lower() not in exempt_words]
        t2rx = lexicon_mod.word_regex(t2)
        offset = 0
        for para in re.split(r"(\n\s*\n)", scored):
            hits = [m for m in t2rx.finditer(para)]
            if len(hits) >= 2:
                findings.append(findings_mod.make(
                    "tier2-cluster",
                    "Tier-2 cluster (%d in one paragraph)" % len(hits),
                    "craft", SYNTH("tier2-cluster"),
                    line_of(scored, offset + hits[0].start()),
                    match=", ".join(sorted({h.group(0).lower() for h in hits})),
                    excerpt=excerpt(para, hits[0].start(), hits[-1].end())))
            offset += len(para)

    # Tier 3 fires only at density.
    wc = stats.get("word_count", 0)
    wc_scored = len(tokenize(scored))
    if "tier3-density" not in skip and wc_scored >= 120:
        t3 = [w for w in lex["tier3"] if w.lower() not in exempt_words]
        hits = list(lexicon_mod.word_regex(t3).finditer(scored))
        density = len(hits) / wc_scored
        if density >= 0.02:
            findings.append(findings_mod.make(
                "tier3-density",
                "Tier-3 saturation (%.1f%% of words)" % (density * 100),
                "craft", SYNTH("tier3-density"),
                line_of(scored, hits[0].start()) if hits else 1,
                match=", ".join(sorted({h.group(0).lower() for h in hits})[:12]),
                excerpt="Replace some with specifics: numbers, comparisons, examples."))

    # 4. Stylometric flags.
    if wc >= 120:
        b = stats.get("burstiness", 0)
        if "uniformity" not in skip and b < BANDS["burstiness"][0]:
            findings.append(findings_mod.make(
                "uniformity", "Low burstiness (%.2f, human range %.2f-%.2f)"
                % (b, *BANDS["burstiness"]), "craft", SYNTH("uniformity"), 1,
                match="sd/mean of sentence length",
                excerpt="Sentence lengths are too even. Mix 3-8 word sentences "
                        "with 20+ word ones. Vary the sentences, not the punctuation."))
        m = stats.get("mattr")
        if "low-diversity" not in skip and m is not None and m < BANDS["mattr"][0]:
            findings.append(findings_mod.make(
                "low-diversity",
                "Low vocabulary diversity (MATTR %.2f, human range %.2f-%.2f)"
                % (m, *BANDS["mattr"]), "craft", SYNTH("low-diversity"), 1,
                match="moving-average type-token ratio",
                excerpt="Broaden the what, not the thesaurus: name specific things, "
                        "cite specific cases, replace a reused abstract noun with the instance."))
        tr = stats.get("trigram_repetition", 0)
        if "trigram-repetition" not in skip and tr > BANDS["trigram_repetition"][1]:
            findings.append(findings_mod.make(
                "trigram-repetition",
                "Repeated 3-word phrases (%.1f%%)" % (tr * 100), "craft",
                SYNTH("trigram-repetition"), 1,
                match="trigram repetition",
                excerpt="The draft reuses the same phrasings. Rewrite the repeats or cut them."))
        psd = stats.get("paragraph_sd")
        if ("uniform-paragraphs" not in skip and psd is not None
                and psd < 0.75 and stats.get("paragraph_count", 0) >= 5):
            findings.append(findings_mod.make(
                "uniform-paragraphs",
                "Uniform paragraph length (sd %.2f sentences)" % psd,
                "craft", SYNTH("uniform-paragraphs"), 1, match="paragraph length",
                excerpt="Every paragraph is about the same size. Some should be one sentence."))

    if "em-dash-rate" not in skip:
        rate = stats.get("em_dashes_per_1k", 0)
        # The register's allowance is an absolute dash count, not a rate: a
        # LinkedIn post tolerating "2 per post" says nothing about per-1,000-word
        # rates on a document that never reaches 1,000 words.
        allowed = max(1, relax.get("em-dash-rate", 0))
        if rate > BANDS["em_dashes_per_1k"][1] and stats.get("em_dashes", 0) > allowed:
            findings.append(findings_mod.make(
                "em-dash-rate", "Em-dash rate %.1f per 1,000 words" % rate,
                "craft", SYNTH("em-dash-rate"), 1,
                match="%d em/en dashes" % stats.get("em_dashes", 0),
                excerpt="Guidance, not a ban. A user's writing sample overrides this. "
                        "Never add one during a rewrite."))

    # The safety band, on the raw text and never on `scored`. The quoted-example
    # exemption is about content, and an injection hides in exactly the spans it
    # protects. See rwlib/injection.py. Skip-gated per id like every other stage,
    # though no shipped register skips any of them: registers.py forbids it.
    findings.extend(f for f in injection.scan(raw_text)
                    if f["id"] not in skip)

    # Voice rules run last and are never suppressed by the register profile.
    if voice_rules:
        apply_voice_rules(scored, raw_text, voice_rules, stats, findings)

    # The one voice measurement that is not a rule, and the only one that runs
    # without a rules file: a fingerprint is a separate artifact and a profile
    # may have one without the other.
    if voice_fingerprint:
        apply_voice_distance(raw_text, voice_fingerprint, stats, findings)

    # STE structural checks, report-only. Over `scored`, not `raw_text`: a
    # semicolon in a code fence is not prose, and the first calibration run
    # counted 1,069 of exactly those. Before the suppression pass below, so
    # a `rabbit-allow: ste-modal (...)` comment works on these findings the
    # way it works on everything else. 'mechanical' (the counted rules)
    # runs in every scan; 'all' adds the advisory vocabulary band.
    #
    # Register allowances drop the first N per id in document order, the
    # same contract find() gives the lexicon tiers, and on the same side of
    # suppress.apply: a rabbit-allow naming an allowed-away hit reports
    # suppression-unused, exactly as a tier allowance does today.
    if ste != "off":
        # Grouped by id, then sliced past the allowance, the same shape
        # find()'s `hits[allowed:]` gives the lexicon tiers rather than a
        # second counter-and-compare idiom for the identical contract.
        # ste_mod.check_for_scan already returns findings sorted by
        # (line, id), so appending in id-group order preserves each id's own
        # document order without needing to re-sort.
        by_id = {}
        for f in ste_mod.check_for_scan(
                scored, mode=ste_mode,
                scope=("all" if ste == "all" else "mechanical"),
                word_cap=ste_word_cap):
            if f["id"] not in skip:
                by_id.setdefault(f["id"], []).append(f)
        for fid, hits in by_id.items():
            findings.extend(hits[relax.get(fid, 0):])

    # Inline `rabbit-allow` comments and voice profile engine exemptions,
    # after every finding exists and before the sort. Marked, never dropped:
    # a suppressed finding is still reported, it just stops counting. See rwlib/suppress.py.
    # The safety band is refused there.
    if suppressions:
        allowances, problems = suppress.parse(raw_text)
        allowances.extend(suppress.profile_allowances(voice_rules))
        used, refused = suppress.apply(findings, allowances)
        findings.extend(suppress.audit(allowances, problems, used,
                                       findings_mod.make, refused))

    stats.pop("_profile", None)
    findings.sort(key=findings_mod.sort_key)
    return findings, stats


# --------------------------------------------------------------------------
# output
# --------------------------------------------------------------------------

def band_note(value, key):
    if value is None:
        return ""
    lo, hi = BANDS[key]
    if value < lo:
        return "  below human range (%.2f-%.2f)" % (lo, hi)
    if value > hi:
        return "  above human range (%.2f-%.2f)" % (lo, hi)
    return "  in human range"


BAND_HEADERS = {
    "safety": "  safety (concealed text, or text aimed at an agent)",
    "voice": "  voice (this writer's own rules)",
    "fingerprint": "  fingerprints (evidence about production)",
    "craft": "  craft (bad writing regardless of author)",
    "structure": "  structure (document organization and headings)",
}


def report(findings, stats, profile, exempt, voice_name=None, notes=()):
    out = []
    wc = stats.get("word_count", 0)
    rel = reliability(wc)
    out.append("rabbit-writes scan")
    out.append("register: %s   voice: %s   words: %d   reliability: %s%s"
               % (profile, voice_name or "none", wc, rel,
                  "   (quoted examples exempt)" if exempt else "   (nothing exempt)"))
    if rel in ("low", "insufficient"):
        out.append("Short sample. Treat every number below as directional; "
                   "re-run on 250+ words before making any call that matters.")
    for note in notes:
        out.append("note: %s" % note)
    out.append("")

    # Suppressed findings are held out of the priority sections and printed
    # under their own heading below. They do not count and they are not hidden:
    # see rwlib/suppress.py on why a mechanism that made a P0 disappear quietly
    # would be worse than the `files:` scoping it replaces.
    allowed = suppress.suppressed(findings)
    findings = suppress.live(findings)

    if not findings:
        out.append("No mechanical findings. The judgment layer still applies: "
                   "run references/patterns.md and references/checklist.md.")
    else:
        for pri in ("P0", "P1", "P2"):
            group = [f for f in findings if f["priority"] == pri]
            if not group:
                continue
            titles = {"P0": "P0  credibility killers",
                      "P1": "P1  obvious machine smell",
                      "P2": "P2  polish"}
            out.append(titles[pri])
            for band in ("safety", "voice", "fingerprint", "craft", "structure"):
                sub = [f for f in group if f["band"] == band]
                if not sub:
                    continue
                out.append(BAND_HEADERS[band])
                seen = Counter(f["id"] for f in sub)
                shown = Counter()
                for f in sub:
                    shown[f["id"]] += 1
                    if shown[f["id"]] > 4:
                        continue
                    out.append("    L%-4d %-32s %s" % (f["line"], f["label"], f["match"]))
                for pid, n in seen.items():
                    if n > 4:
                        out.append("    ... and %d more %s" % (n - 4, pid))
            out.append("")

    if allowed:
        out.append("suppressed (%d, not counted above)" % len(allowed))
        for f in allowed:
            out.append("    L%-4d %-32s %s" % (f["line"], f["label"], f["match"]))
            if "suppressed_at" in f:
                out.append("          allowed at L%d: %s"
                           % (f["suppressed_at"], f["suppressed"]))
            elif "suppressed_by" in f:
                out.append("          allowed by %s: %s"
                           % (f["suppressed_by"], f["suppressed"]))
            else:
                out.append("          allowed: %s" % f["suppressed"])
        out.append("")

    out.append("stylometrics")
    rows = [
        ("words", wc, None),
        ("sentences", stats.get("sentence_count"), None),
        ("avg sentence words", stats.get("avg_sentence_words"), None),
        ("sentence length sd", stats.get("sentence_sd"), None),
        ("burstiness (sd/mean)", stats.get("burstiness"), "burstiness"),
        ("MATTR-100", stats.get("mattr"), "mattr"),
        ("type-token ratio", stats.get("ttr"), "ttr"),
        ("trigram repetition", stats.get("trigram_repetition"), "trigram_repetition"),
        ("em dashes / 1k words", stats.get("em_dashes_per_1k"), "em_dashes_per_1k"),
        ("avg paragraph sentences", stats.get("avg_paragraph_sentences"), None),
        ("paragraph length sd", stats.get("paragraph_sd"), None),
        ("Flesch-Kincaid grade", stats.get("flesch_kincaid_grade"), None),
    ]
    for name, value, key in rows:
        if value is None:
            continue
        note = band_note(value, key) if key else ""
        out.append("  %-26s %-8s%s" % (name, value, note))

    # Printed at every verdict, including in_range, because "0.58, in range" is
    # the line a conversion is checked against and a measurement that only
    # appears when it fails cannot be a before-and-after.
    measured = stats.get("voice_distance")
    if measured:
        out.append("  %-26s %-8s  %s, this writer's samples sit under %.2f%s"
                   % ("voice distance", measured["delta"],
                      measured["verdict"].replace("_", " "),
                      measured["band"]["max"],
                      "" if measured["reliable"] else
                      "   (under %d words: directional only)"
                      % stylometry.RELIABLE_WORDS))
    out.append("")
    out.append("Flesch-Kincaid is a diagnostic, never a target. Readability formulas "
               "are poor proxies for comprehension and reward gaming.")
    out.append("These are signals, not proof. Never use this output to decide who "
               "wrote something.")
    return "\n".join(out)


def json_payload(findings, stats, profile, exempt, voice_name, notes,
                 voice_lineage=(), register_detection=None):
    """The --json document. Versioned, because a consumer that pins the schema
    finds out at parse time when the shape moves rather than by rendering
    blanks, and because a published measurement is only reproducible if the
    report says which lexicon produced it."""
    # Lifted out of `stats` rather than copied, so the measurement has one place
    # in the document. It is not a stylometric like the rest of that block: it
    # is a comparison against a stored artifact, and a consumer reading it wants
    # it whether or not a finding was raised off it. `null` when no fingerprint
    # was found, which is the common case and is not an error.
    stats = dict(stats)
    measured = stats.pop("voice_distance", None)
    return {
        "schema_version": findings_mod.SCHEMA_VERSION,
        "lexicon_version": lexicon_mod.version(),
        "registers_version": registers.version(),
        "ste_version": ste_mod.version(),
        "profile": profile,
        "register_detection": register_detection,
        "voice": voice_name,
        "voice_lineage": list(voice_lineage),
        "exempt_applied": exempt,
        "reliability": reliability(stats.get("word_count", 0)),
        "notes": list(notes),
        "stats": stats,
        "voice_distance": measured,
        "human_ranges": BANDS,
        "counts": findings_mod.counts(findings),
        "findings": findings,
    }


def run_apply_safe(text, path, voice_rules, write, to_stdout=False,
                   newline=None):
    """Apply the mechanical fixes, verify the result, and say what happened.

    The verification pass is the point. Anything this writes has to survive
    verify.py, which is the same gate a model-authored rewrite goes through, so
    a bug here fails loudly instead of quietly editing somebody's draft.

    `to_stdout` emits the document instead of the report, and it runs the same
    gate. It used to be a separate branch in main() that called the fixer and
    printed the result with no verification at all, which is the path most likely
    to be redirected straight into a file: `--apply-safe --stdout > new.md` wrote
    exactly the document the gate would have rejected, silently, exit 0.

    `newline` is the line ending the file was read with. Written back as it came
    in, because rewriting every line of a CRLF document is not one of the edits
    with exactly one correct answer, and verify.py cannot see it: both sides are
    read through universal newlines, so the comparison it runs has already
    normalized the difference away.
    """
    # The safety gate, before any edit is even planned. A document carrying a
    # concealed instruction is not auto-edited at all, and the span is quoted
    # verbatim rather than summarized: a person decides, and the tool does not
    # get to paraphrase an attack into something that reads as harmless.
    #
    # Refusing the whole run rather than masking the span. Masking would ship an
    # edited file that still contains the injection, and the next tool down the
    # pipeline has no way to know it was there. This is the same reasoning as
    # rule 2 in fixes.py, one step stronger: there the promise outranks the fix,
    # here the evidence does.
    blocking = [f for f in injection.scan(text) if f["priority"] == "P0"]
    if blocking:
        stream = sys.stderr if to_stdout else sys.stdout
        print("rabbit-writes --apply-safe: refused, nothing was written.",
              file=stream)
        print("%s carries concealed text addressed to an agent. Read it before "
              "letting any tool process this document:\n" % (path or "stdin"),
              file=stream)
        for f in blocking:
            print("  L%-4d %s" % (f["line"], f["label"]), file=stream)
            print("        %s" % f["match"], file=stream)
        print("\nNothing in the safety band is fixable, and a `rabbit-allow` "
              "comment cannot clear it: see rwlib/injection.py.", file=stream)
        if to_stdout:
            print("Note: output was redirected with --stdout; your redirect target is now empty.", file=sys.stderr)
        return 1

    fixed, applied, skipped = fixes_mod.apply(text, voice_rules)

    # Imported here rather than at module scope. verify.py is a sibling script
    # and a scan is the common case: a document that never asks for a fix should
    # not pay to load the validator, and a scan.py copied somewhere without its
    # sibling should still scan.
    try:
        import verify as verify_mod
    except ImportError:
        verify_mod = None

    if to_stdout:
        verdict = verify_mod.validate(text, fixed) if verify_mod else None
        if verdict and not verdict["ok"]:
            print("scan: verify.py rejected these edits, so nothing was "
                  "printed:", file=sys.stderr)
            for v in verdict["violations"]:
                print("  %-32s %s" % (v["kind"], v["detail"]), file=sys.stderr)
            print("This is a bug in the fixer, not in your document. Report it.",
                  file=sys.stderr)
            return 1
        if verdict is None:
            print("scan: verify.py not found beside this script, so these "
                  "edits cannot be checked against the preservation rules. "
                  "Refusing to print --apply-safe output unverified.",
                  file=sys.stderr)
            return 2
        sys.stdout.write(fixed)
        return 0

    print("rabbit-writes --apply-safe")
    if not applied and not skipped:
        print("Nothing mechanically fixable. Every other finding needs a "
              "person: run the scan without this flag.")
        return 0

    for record in applied:
        print("  L%-4d %-20s %r -> %r   (%s)"
              % (record["line"], record["id"], record["before"],
                 record["after"], record["note"]))
    for record in skipped:
        print("  L%-4d %-20s not fixed: %s"
              % (record["line"], record["id"], record["note"]))

    verdict = verify_mod.validate(text, fixed) if verify_mod else None
    if verdict and not verdict["ok"]:
        print("\nverify.py rejected these edits, so nothing was written:")
        for v in verdict["violations"]:
            print("  %-32s %s" % (v["kind"], v["detail"]))
        print("This is a bug in the fixer, not in your document. Report it.")
        return 1
    if verdict:
        print("\nverified: tells %d -> %d, em dashes %d -> %d"
              % (verdict["tells_before"], verdict["tells_after"],
                 verdict["em_dashes_before"], verdict["em_dashes_after"]))
    else:
        print("\nverify.py not found beside this script, so the edits above "
              "were not checked against the preservation rules.")

    if not write:
        print("\nDry run. Nothing written. Pass --write to apply, or pipe "
              "--apply-safe --stdout into a diff.")
        return 0
    if verdict is None:
        print("\nRefusing to write: verify.py is missing, so these edits "
              "cannot be checked against the preservation rules. Copy "
              "verify.py back beside scan.py, or drop --write to review the "
              "edits above without applying them.")
        return 2
    if not path:
        examples = [
            "python3 scan.py draft.md",
            "python3 scan.py draft.md --json",
            "python3 scan.py draft.md --apply-safe --write"
        ]
        print(cli_error.format_llm_error(
            "scan.py", "--write requires a file argument (cannot write back when reading from stdin)",
            parser=None, examples=examples), file=sys.stderr)
        return 2
    # `newline` is a str when the file used one style throughout, a tuple when it
    # mixed them, and None on a file with no line break at all. Only the first
    # case can be reproduced faithfully; the other two fall back to the platform
    # default, which is what they got before.
    try:
        _write_back(path, fixed, newline)
    except OSError as exc:
        examples = [
            "python3 scan.py draft.md",
            "python3 scan.py draft.md --apply-safe --write"
        ]
        print(cli_error.format_file_error(
            "scan.py", path, "file", expected_type="writable file path",
            details=str(exc), examples=examples), file=sys.stderr)
        return 2
    print("\nwrote %d edit(s) to %s" % (len(applied), path))
    return 0


def _write_back(path, text, newline):
    """The atomic write --apply-safe and --apply-model share.

    `newline` is the line ending the file was read with. Written back as it came
    in, because rewriting every line of a CRLF document is not one of the edits
    with exactly one correct answer, and verify.py cannot see it: both sides are
    read through universal newlines, so the comparison it runs has already
    normalized the difference away. A str when the file used one style
    throughout, a tuple when it mixed them, and None on a file with no line
    break at all. Only the first case can be reproduced faithfully.

    mkstemp creates at 0600 and os.replace carries that onto the target, so a
    0644 file in a repository would come back readable by nobody but its owner.
    The original mode is copied across first, best effort: a platform that
    refuses chmod still gets the write, which is the point. Two callers doing
    this by hand is two chances to drop that line.
    """
    dir_name = os.path.dirname(os.path.abspath(path)) or "."
    nl = newline if isinstance(newline, str) else None
    tmp_fd, tmp_path = tempfile.mkstemp(dir=dir_name, prefix=".rw_tmp_")
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8", newline=nl) as fh:
            fh.write(text)
        try:
            os.chmod(tmp_path, stat.S_IMODE(os.stat(path).st_mode))
        except OSError:
            pass
        os.replace(tmp_path, path)
    except OSError:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        raise


def run_apply_model(text, path, args, voice_rules, voice_fingerprint,
                    newline=None):
    """Send each finding's own passage to a small model, and gate every reply.

    The document is never sent. `rwlib.rewrite.plan` cuts it into one unit per
    finding (a sentence, or a paragraph for the shape findings), so the request
    size is set by the tell rather than by the file, and a 4k-context model on a
    Raspberry Pi is enough. The argument for all of that is in rewrite.py.

    What lives *here* rather than there is everything the engine knows and the
    library must not import: the scan itself, `verify.validate`, and
    `BANDS["burstiness"][0]`, which is the calibrated floor that decides which
    paragraphs count as uniform. `rwlib` cannot reach up to scan.py or verify.py
    without closing an import loop, so the three arrive as arguments.
    """
    from rwlib import endpoint as endpoint_mod
    from rwlib import rewrite as rewrite_mod

    stream = sys.stderr if args.stdout else sys.stdout
    overrides = {}
    if args.model_endpoint:
        overrides["base_url"] = args.model_endpoint
        overrides["model"] = args.model_name or "local"
    elif args.model_name:
        print(cli_error.format_llm_error(
            "scan.py",
            "--model-name names a model on an endpoint, and no endpoint was "
            "given. Pass --model-endpoint too, or put both in a .rabbit-model "
            "file beside the document.",
            parser=None,
            examples=["python3 scan.py draft.md --apply-model "
                      "--model-endpoint http://127.0.0.1:8080/v1 "
                      "--model-name qwen3-1.7b"]), file=sys.stderr)
        return 2

    endpoint, note = endpoint_mod.resolve(path, overrides or None)
    if endpoint is None and not args.model_plan:
        # An endpoint asked for and not usable exits 2, the same line --voice
        # draws: you named it, so a clean report on a document nothing rewrote
        # would be a false pass.
        print(cli_error.format_llm_error(
            "scan.py", "no usable model endpoint: %s" % note, parser=None,
            examples=["python3 scan.py draft.md --apply-model --model-plan",
                      "python3 scan.py draft.md --apply-model "
                      "--model-endpoint http://127.0.0.1:8080/v1 "
                      "--model-name qwen3-1.7b"]), file=sys.stderr)
        return 2

    exempt = not args.no_exempt
    # ste='off' on both calls: a rewriter is sent findings it can act on,
    # and STE is report-only by contract. In the plan that keeps this scan
    # quiet, and in the rescan that gates each reply, an ste finding would
    # either be sent to the model or move the before/after count.
    findings, _stats = scan(text, args.profile, exempt, voice_rules,
                            voice_fingerprint=voice_fingerprint,
                            ste="off")

    print("rabbit-writes --apply-model", file=stream)
    print("endpoint: %s" % (endpoint.describe() if endpoint else "none"),
          file=stream)
    print("source:   %s" % note, file=stream)

    if args.model_plan:
        # Plan and stop. This is the flag to run first on somebody else's
        # document and the one to run when there is no server yet: it says
        # exactly what would be sent and how big each request is, without
        # sending any of it.
        budget = endpoint.input_budget() if endpoint else None
        units, unaddressable = rewrite_mod.plan(
            text, findings, budget_tokens=budget,
            estimate=endpoint_mod.estimate_tokens,
            burstiness_floor=BANDS["burstiness"][0])
        print("\n%d unit(s) would be sent, one request each%s:"
              % (len(units), "" if budget is None else
                 " (budget %d tokens)" % budget), file=stream)
        for unit in units:
            print("  L%-4d %-6s %-22s ~%d tokens"
                  % (line_of(text, unit["start"]), unit["kind"],
                     ",".join(sorted({f["id"] for f in unit["findings"]}))[:22],
                     endpoint_mod.estimate_tokens(unit["text"])), file=stream)
        _report_unaddressable(unaddressable, text, stream)
        return 0

    import verify as verify_mod

    # A voice whose em_dash mechanic is 'allow' (e.g. john) means an em dash
    # the model adds is the writer's own sentence shape, not damage verify.py
    # should reject the candidate over. Without this, the gate treats every
    # voice the same as one that forbids dashes, and a model rewrite that
    # legitimately uses one is discarded regardless of the active profile.
    allow_dashes = bool(voice_rules) and voice_mechanics(
        voice_rules, args.profile).get("em_dash") == "allow"

    result = rewrite_mod.run(
        text, findings, endpoint,
        scan_fn=lambda t: scan(t, args.profile, exempt, voice_rules,
                               voice_fingerprint=voice_fingerprint,
                               ste="off")[0],
        validate_fn=lambda a, b: verify_mod.validate(a, b, allow_dashes=allow_dashes),
        injection_fn=injection.scan,
        attempts=args.model_attempts,
        limit=args.model_limit,
        estimate=endpoint_mod.estimate_tokens,
        burstiness_floor=BANDS["burstiness"][0])

    if result["refused"] == "safety":
        print("\nrefused, nothing was sent to the model and nothing was "
              "written.", file=stream)
        print("%s carries concealed text addressed to an agent. A rewriter is "
              "exactly what that text is written for, so it is quoted here and "
              "read by a person:\n" % (path or "stdin"), file=stream)
        for finding in result["blocking"]:
            print("  L%-4d %s" % (finding["line"], finding["label"]), file=stream)
            print("        %s" % finding["match"], file=stream)
        print("\nNothing in the safety band is fixable, and a `rabbit-allow` "
              "comment cannot clear it: see rwlib/injection.py.", file=stream)
        if args.stdout:
            print("Note: output was redirected with --stdout; your redirect "
                  "target is now empty.", file=sys.stderr)
        return 1

    accepted = [r for r in result["records"] if r["accepted"]]
    print("", file=stream)
    for record in result["records"]:
        line = line_of(text, record["start"])
        ids = ",".join(record["ids"])
        if record["accepted"]:
            print("  L%-4d %-6s %-24s rewritten" % (line, record["kind"], ids),
                  file=stream)
            print("        -  %s" % _one_line(record["before"]), file=stream)
            print("        +  %s" % _one_line(record["after"]), file=stream)
        else:
            print("  L%-4d %-6s %-24s left alone after %d attempt(s)"
                  % (line, record["kind"], ids, len(record["attempts"])),
                  file=stream)
            if record["attempts"]:
                print("        last: %s" % record["attempts"][-1], file=stream)
    if not result["records"]:
        print("  Nothing a model can help with. Every finding is either "
              "mechanically fixable (--apply-safe), measured over the whole "
              "document, or in the safety band.", file=stream)
    _report_unaddressable(result["unaddressable"], text, stream)

    if result["refused"] == "verify":
        print("\nverify.py rejected the assembled document, so nothing was "
              "written:", file=stream)
        for violation in result["verdict"]["violations"]:
            print("  %-32s %s" % (violation["kind"], violation["detail"]),
                  file=stream)
        print("Each rewrite passed its own gate and the document did not. "
              "Report it.", file=stream)
        if args.stdout:
            # Same courtesy as the safety refusal above: with --stdout the
            # report went to stderr and the redirect target holds nothing.
            print("Note: output was redirected with --stdout; your redirect "
                  "target is now empty.", file=sys.stderr)
        return 1

    verdict = result["verdict"]
    if verdict:
        print("\nverified: tells %d -> %d, em dashes %d -> %d"
              % (verdict["tells_before"], verdict["tells_after"],
                 verdict["em_dashes_before"], verdict["em_dashes_after"]),
              file=stream)

    if args.stdout:
        sys.stdout.write(result["text"])
        return 0
    if not args.write:
        print("\nDry run. Nothing written. Pass --write to apply, or pipe "
              "--apply-model --stdout into a diff.", file=stream)
        return 0
    if not path:
        print(cli_error.format_llm_error(
            "scan.py", "--write requires a file argument (cannot write back "
                       "when reading from stdin)", parser=None,
            examples=["python3 scan.py draft.md --apply-model --write"]),
            file=sys.stderr)
        return 2
    if not accepted:
        print("\nNothing accepted, so nothing written.", file=stream)
        return 0
    try:
        _write_back(path, result["text"], newline)
    except OSError as exc:
        print(cli_error.format_file_error(
            "scan.py", path, "file", expected_type="writable file path",
            details=str(exc),
            examples=["python3 scan.py draft.md --apply-model --write"]),
            file=sys.stderr)
        return 2
    print("\nwrote %d rewrite(s) to %s" % (len(accepted), path), file=stream)
    return 0


def _one_line(text):
    return re.sub(r"\s+", " ", (text or "").strip())[:96]


def _report_unaddressable(unaddressable, text, stream):
    """Every finding a model was not asked about, and why.

    Printed rather than dropped, for the same reason `suppress.py` marks a
    finding instead of removing it: a run that quietly skipped half the report
    reads exactly like a run that fixed it.
    """
    if not unaddressable:
        return
    print("\nnot sent to the model (%d):" % len(unaddressable), file=stream)
    seen = set()
    for finding, reason in unaddressable:
        key = (finding.get("id"), reason)
        if key in seen:
            continue
        seen.add(key)
        print("  L%-4d %-24s %s" % (finding.get("line", 0), finding.get("id"),
                                    reason), file=stream)


def main():
    examples = [
        "python3 scan.py draft.md",
        "python3 scan.py draft.md --json",
        "python3 scan.py draft.md --sarif > scan.sarif",
        "python3 scan.py draft.md --profile technical-blog",
        "python3 scan.py draft.md --ste",
        "python3 scan.py draft.md --ste --ste-mode procedural",
        "python3 scan.py draft.md --voice-rules voices/whit3rabbit.rules.json",
        "python3 scan.py draft.md --voice auto",
        "python3 scan.py draft.md --apply-safe --write"
    ]
    ap = cli_error.LLMArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        examples=examples
    )
    ap.add_argument("file", nargs="?", help="file to scan; omit to read stdin")
    ap.add_argument("--version", action="version",
                    version="scan.py (lexicon v%s, registers v%s, ste v%s)"
                            % (lexicon_mod.version(), registers.version(),
                               ste_mod.version()))
    ap.add_argument("--profile", default=DEFAULT_REGISTER,
                    choices=sorted(REGISTERS) + ["auto"],
                    help="register profile (default: %s). 'auto' detects a "
                         "handful of unambiguous forms (docs, linkedin, "
                         "formal) from document structure and "
                         "falls back to %s otherwise; an explicit --profile "
                         "always wins over detection" % (DEFAULT_REGISTER, DEFAULT_REGISTER))
    format_group = ap.add_mutually_exclusive_group()
    format_group.add_argument("--json", action="store_true", help="machine-readable output")
    format_group.add_argument("--sarif", action="store_true",
                              help="SARIF 2.1.0, for GitHub pull request annotations")
    ap.add_argument("--sarif-uri", metavar="PATH",
                    help="the path to record in the SARIF output, relative to the "
                         "repository root. Defaults to the file argument")
    ap.add_argument("--no-exempt", action="store_true",
                    help="also score quoted examples, code, tables, and block quotes")
    # One profile, named one of two ways. Both in a mutually exclusive group
    # because silently preferring one over the other produces a report about a
    # profile nobody asked for, which is the failure this band exists to avoid.
    voice_group = ap.add_mutually_exclusive_group()
    voice_group.add_argument("--voice-rules", metavar="PATH",
                             help="a voice's <name>.rules.json; its findings land in the "
                                  "'voice' band and are never relaxed by --profile")
    voice_group.add_argument("--voice", metavar="NAME",
                             help="resolve the profile instead of spelling out a path. "
                                  "'auto' uses the same order readme_check.py does "
                                  "(.rabbit-voice beside the file or in the working "
                                  "directory, then voices/ACTIVE, and no profile at all "
                                  "if neither names one), and anything else loads "
                                  "voices/<NAME>.rules.json")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any P0 finding is present")
    ap.add_argument("--apply-safe", action="store_true",
                    help="apply only the edits with exactly one correct answer "
                         "(hidden characters, AI tracking parameters, this "
                         "voice's own single-word substitutions) and verify the "
                         "result. Everything needing judgment stays report-only, "
                         "a typed -- included: there is no mechanical answer, and "
                         "this plugin never adds an em dash")
    ap.add_argument("--write", action="store_true",
                    help="with --apply-safe, write the fixes back to the file. "
                         "Without it, --apply-safe is a dry run")
    ap.add_argument("--stdout", action="store_true",
                    help="with --apply-safe or --apply-model, print the fixed "
                         "document instead of the report, so it can be diffed "
                         "or piped")
    # Mutually exclusive because they argue about the same default: the
    # mechanical STE checks run in every plain scan now, so --ste and
    # --no-ste are 'more' and 'none' against that baseline.
    ste_group = ap.add_mutually_exclusive_group()
    ste_group.add_argument("--ste", action="store_true",
                    help="add the advisory ASD-STE100 checks (vocabulary, "
                         "passive voice, modals, banned and phrasal verbs) "
                         "on top of the mechanical ones every scan already "
                         "runs. Report-only: STE findings are never "
                         "mechanically fixed and never fail --check.")
    ste_group.add_argument("--no-ste", action="store_true",
                    help="silence the mechanical STE checks that run by "
                         "default (sentence word caps, sentences per "
                         "paragraph, semicolons, condition order)")
    ap.add_argument("--ste-mode", default=None,
                    choices=["procedural", "descriptive"],
                    help="force STE text classification. Without this flag, "
                         "ste.py classifies each paragraph automatically. "
                         "'procedural' enforces 20-word sentence limit; "
                         "'descriptive' enforces 25-word limit.")

    model_group = ap.add_argument_group(
        "model-backed rewriting",
        "Sends one passage per finding to a small OpenAI-compatible model and "
        "gates every reply through verify.py and a rescan. The document itself "
        "is never sent. Configure the endpoint in a .rabbit-model file beside "
        "the document, or pass --model-endpoint.")
    model_group.add_argument("--apply-model", action="store_true",
                             help="rewrite the passages that carry findings, "
                                  "keeping only the rewrites that survive the gate")
    model_group.add_argument("--model-plan", action="store_true",
                             help="with --apply-model, print what would be sent "
                                  "and how big each request is, and send nothing")
    model_group.add_argument("--model-endpoint", metavar="URL",
                             help="OpenAI-compatible base URL, e.g. "
                                  "http://127.0.0.1:8080/v1 for llama-server or "
                                  "http://127.0.0.1:11434/v1 for Ollama")
    model_group.add_argument("--model-name", metavar="NAME",
                             help="model to ask for at that endpoint. A local "
                                  "llama-server ignores it and still needs one")
    model_group.add_argument("--model-limit", type=int, metavar="N",
                             help="stop after N passages. What was dropped is "
                                  "listed rather than silently skipped")
    model_group.add_argument("--model-attempts", type=int, default=3, metavar="N",
                             help="tries per passage before leaving it alone "
                                  "(default 3). Each retry is told why the last "
                                  "one was rejected")
    args = ap.parse_args()

    # Both of these are read by run_apply_safe and by nothing else, so without
    # --apply-safe they were accepted and silently did nothing. `--stdout` is the
    # worse half: a caller piping the output got the report where it expected the
    # document, which is a fixed file that was never fixed.
    applying = args.apply_safe or args.apply_model
    dead = [flag for flag, on in (("--write", args.write),
                                  ("--stdout", args.stdout)) if on]
    if dead and not applying:
        print(cli_error.format_llm_error(
            "scan.py",
            "%s only applies with --apply-safe or --apply-model, which is what "
            "produces the fixed document. Without one there is nothing to write "
            "or print." % " and ".join(dead),
            parser=ap, examples=examples), file=sys.stderr)
        return 2

    # Every --model-* flag is read by run_apply_model and by nothing else, so
    # without --apply-model they were accepted and did nothing. The same trap
    # --write and --stdout fell into above, and worse here: a caller who
    # configured an endpoint and got a plain report has no way to tell that from
    # a document with nothing to rewrite.
    model_flags = [flag for flag, on in (
        ("--model-plan", args.model_plan),
        ("--model-endpoint", args.model_endpoint),
        ("--model-name", args.model_name),
        ("--model-limit", args.model_limit is not None)) if on]
    if model_flags and not args.apply_model:
        print(cli_error.format_llm_error(
            "scan.py",
            "%s only applies with --apply-model." % " and ".join(model_flags),
            parser=ap, examples=examples), file=sys.stderr)
        return 2

    if args.apply_safe and args.apply_model:
        print(cli_error.format_llm_error(
            "scan.py",
            "--apply-safe and --apply-model are separate passes and the order "
            "matters. Run --apply-safe --write first: it fixes the edits with "
            "exactly one correct answer, deterministically and for free, and "
            "leaves the model a smaller job.",
            parser=ap, examples=examples), file=sys.stderr)
        return 2

    if args.ste_mode and args.no_ste:
        print(cli_error.format_llm_error(
            "scan.py",
            "--ste-mode cannot be combined with --no-ste: --no-ste disables STE checks entirely.",
            parser=ap, examples=examples), file=sys.stderr)
        return 2

    if args.write and args.stdout:
        print(cli_error.format_llm_error(
            "scan.py",
            "--write and --stdout cannot be combined: --write modifies the file in place and --stdout prints to standard output.",
            parser=ap, examples=examples), file=sys.stderr)
        return 2

    if args.sarif_uri and not args.sarif:
        print(cli_error.format_llm_error(
            "scan.py",
            "--sarif-uri only applies with --sarif, which is what produces the SARIF output.",
            parser=ap, examples=examples), file=sys.stderr)
        return 2

    if applying:
        mode = "--apply-safe" if args.apply_safe else "--apply-model"
        conflict = [flag for flag, on in (("--check", args.check),
                                          ("--json", args.json),
                                          ("--sarif", args.sarif)) if on]
        if conflict:
            print(cli_error.format_llm_error(
                "scan.py",
                "%s cannot be combined with %s: %s applies fixes, and the other "
                "reports findings. Run the two as separate commands."
                % (" and ".join(conflict), mode, mode),
                parser=ap, examples=examples), file=sys.stderr)
            return 2

    # `newlines` records the line endings the file actually used, so --write can
    # put them back. Reading stays universal: every regex in the engine is
    # written against "\n", and handing it a "\r" would move the scan's own
    # numbers to fix a problem that only exists on the write path.
    newlines = None
    docx_findings = None
    if args.file and docx_text.is_docx(args.file):
        # A Word document: the visible text goes through the ordinary scan, and
        # the runs the file itself declares hidden come back as safety findings
        # with the paragraph number for a line. No write-back: --apply-safe
        # edits text files, and pretending to edit a zip would either destroy
        # the document or silently write a .md beside it.
        if applying:
            print(cli_error.format_file_error(
                "scan.py", args.file, "file", expected_type="text markdown file",
                details="%s edits text files and cannot write a .docx"
                        % ("--apply-safe" if args.apply_safe else "--apply-model"),
                examples=examples
            ), file=sys.stderr)
            return 2
        try:
            text, docx_findings = docx_text.extract(args.file)
        except docx_text.DocxError as exc:
            print(cli_error.format_file_error(
                "scan.py", args.file, "file", expected_type=".docx file",
                details=str(exc), examples=examples
            ), file=sys.stderr)
            return 2
    elif args.file:
        try:
            with open(args.file, encoding="utf-8-sig") as fh:
                text = fh.read()
                newlines = fh.newlines
        except (OSError, UnicodeDecodeError) as exc:
            print(cli_error.format_file_error(
                "scan.py", args.file, "file", expected_type="file path",
                details=str(exc), examples=examples
            ), file=sys.stderr)
            return 2
    else:
        text = sys.stdin.read()

    register_note, register_detection = None, None
    if args.profile == "auto":
        # Detection is opt-in only: omitting --profile still means
        # DEFAULT_REGISTER, exactly as before this flag existed. 'auto' has to
        # be asked for by name, the same rule --voice auto already follows.
        detected, confidence, signals = registers.detect_register(text, path=args.file)
        args.profile = detected
        register_detection = {"register": detected, "confidence": confidence, "signals": signals}
        register_note = ("register auto-detected as %r (%s)"
                         % (detected, ", ".join(signals) if signals else confidence))

    voice_rules, voice_name, lineage = None, None, []
    # `named` is the difference between "you asked for this profile" and "this
    # is the one that turned up". A profile asked for by name and not readable
    # exits 2, because a clean voice band on a profile nobody read is a false
    # pass. A profile that only fails to *resolve* under --voice auto is a note
    # and the run continues, because plenty of repos have none and failing there
    # teaches people to drop the flag. readme_check.py draws the line in the
    # same place.
    rules_path, voice_note, named = args.voice_rules, None, bool(args.voice_rules)
    if args.voice:
        if args.voice == "auto":
            rules_path, _, voice_note = voices_mod.resolve(args.file)
        else:
            named = True
            rules_path = os.path.join(voices_mod.VOICES_DIR,
                                      args.voice + voices_mod.RULES_SUFFIX)
            if not os.path.exists(rules_path):
                installed_str = ", ".join(voices_mod.installed()) or "none"
                print(cli_error.format_file_error(
                    "scan.py", args.voice, "--voice",
                    expected_type="installed voice profile name",
                    details="No profile named %r in %s. Installed: %s"
                            % (args.voice, voices_mod.VOICES_DIR, installed_str),
                    examples=examples), file=sys.stderr)
                return 2
    if rules_path:
        try:
            voice_rules = voices_mod.load(rules_path)
            lineage = voices_mod.lineage(rules_path)
        except voices_mod.VoiceError as exc:
            if named:
                print(cli_error.format_file_error(
                    "scan.py", rules_path, "--voice-rules / --voice",
                    expected_type="voice rules file path (.rules.json)",
                    details=str(exc), examples=examples), file=sys.stderr)
                return 2
            voice_note = ("%s. No voice band in this report, everything else "
                          "still ran" % exc)
        else:
            voice_name = voice_rules.get("voice", os.path.basename(rules_path))

    # The fingerprint belongs to whichever profile was resolved above, and is
    # looked for beside its rules file. Optional at every step: most profiles
    # will never have one, and an unreadable one is a note rather than an exit,
    # because it measures register and every rule in the band still ran.
    voice_fingerprint, fingerprint_note = None, None
    # Scoped to the register being scanned, falling back to the general one. A
    # writer's chat register and their essay register are two different
    # statistical objects, so measuring a chat message against an essay
    # fingerprint reports a distance that is a change of form rather than a
    # conversion that missed.
    fingerprint_path = stylometry.path_for(rules_path, args.profile)
    if fingerprint_path:
        try:
            voice_fingerprint = stylometry.load(fingerprint_path)
        except (OSError, ValueError) as exc:
            fingerprint_note = ("could not read %s (%s), so no voice distance "
                                "was measured"
                                % (os.path.basename(fingerprint_path), exc))

    if args.apply_safe:
        return run_apply_safe(text, args.file, voice_rules, args.write,
                              to_stdout=args.stdout, newline=newlines)
    if args.apply_model:
        return run_apply_model(text, args.file, args, voice_rules,
                               voice_fingerprint, newline=newlines)

    exempt = not args.no_exempt
    # STE mechanical runs in every scan; --ste adds the advisory band,
    # --no-ste silences the lot. Report-only either way: every ste-* id is
    # P1 or P2, so --check still gates on P0 alone.
    ste_scope = ("off" if args.no_ste
                 else "all" if args.ste else "mechanical")
    findings, stats = scan(text, args.profile, exempt, voice_rules,
                           voice_fingerprint=voice_fingerprint,
                           ste=ste_scope, ste_mode=args.ste_mode)
    if docx_findings:
        # The docx-declared hidden runs, merged after the scan over the visible
        # text so both halves land in one report and one --check verdict. Their
        # `line` is the paragraph number; the excerpt says so.
        findings.extend(docx_findings)
        findings.sort(key=findings_mod.sort_key)

    notes = [n for n in (language.note(text), voice_note, fingerprint_note,
                        register_note) if n]

    if args.sarif:
        uri = args.sarif_uri or args.file or "stdin"
        sarif.warn_if_uri_drops(uri)
        print(json.dumps(sarif.build(
            findings, uri, "rabbit-writes/scan",
            tool_version=lexicon_mod.version(),
            information_uri="https://github.com/whit3rabbit/rabbit-writes",
            extra_properties={"register": args.profile,
                              "voice": voice_name},
            notes=notes), indent=2))
    elif args.json:
        print(json.dumps(json_payload(findings, stats, args.profile, exempt,
                                      voice_name, notes, lineage,
                                      register_detection=register_detection), indent=2))
    else:
        print(report(findings, stats, args.profile, exempt, voice_name, notes))

    # A suppressed P0 does not fail the run. That is the whole point of the
    # mechanism, and it is why the reason is mandatory and the finding is still
    # printed above.
    if args.check and any(f["priority"] == "P0" and "suppressed" not in f
                          for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
