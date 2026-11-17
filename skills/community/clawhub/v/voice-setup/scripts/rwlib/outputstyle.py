#!/usr/bin/env python3
"""
A voice profile, rendered as a Claude Code output style.

An output style edits the host's system prompt, so it is in force on every
response in a session rather than only when somebody runs a skill. That is the
gap this module fills: between two invocations of `rabbit-writes` the model
writes in its own register, and the writer re-asks for their own voice every
turn.

**What goes in, and what deliberately does not.** The style carries the
refusals: mechanics, bans, swaps, the contrastive pairs, the openers and
closers. Those are short, checkable, and specific to one person, which is the
same test `voice-setup/SKILL.md` applies to a profile itself. The long-form
judgment in `voices/<name>.md` (argument order, warmth calibration, the
feedback sandwich) stays out. It is thousands of tokens on every request in
every session, and the skill loads the whole profile at the moment prose is
actually being written, which is when it is worth paying for.

Two exceptions to "refusals only", both lifted verbatim from the profile
markdown rather than restated here, because a second copy of somebody's voice
summary is a second thing to keep in step:

  ## The three essentials    the writer's own ordering contract, first
  ## Voice in one line       one sentence of what the register is

Both headings come from `voices/TEMPLATE.md`, so every profile built through
`build_voice.py --scaffold` has them.

**`signature_moves` is omitted on purpose, and this is not an oversight.** The
engine caps `voice-signature-underuse` at P2 whatever a profile's
`default_priority` says, because a rule that tells an editor to *add* a move
installs a tic. A system prompt is the strongest push available to this plugin,
stronger than any finding, so putting a list of moves in one is the P0 version
of that rule wearing a different hat. Ceilings without floors would be safe and
are also not worth the tokens: the scanner already reports an overused move.

Nothing here touches the filesystem and there is no CLI. The caller owns the
IO, the same inversion `stylometry.fingerprint(..., sample_measures=)` uses, so
this renders from a dict in a test without a profile on disk.

Stdlib only, 3.9+.
"""

import json
import re

try:
    from . import voices as voices_mod
except ImportError:                 # run as a script: no package, but rwlib/ is
    import voices as voices_mod     # on sys.path, because it holds this file

# The four frontmatter keys Claude Code reads on an output style. Stated here
# because this module writes them and `scripts/validate.py` checks them, and a
# fifth key invented by either side is a style the host loads with a warning.
FRONTMATTER_KEYS = ("name", "description", "keep-coding-instructions",
                    "force-for-plugin")

# `keep-coding-instructions` defaults to false in the host, which drops Claude
# Code's own software-engineering instructions from the system prompt. A voice
# style is about how prose reads and says nothing about how to scope a change
# or verify work, so dropping them turns a coding session into a writing
# session three turns after somebody picked a style for their email.
KEEP_CODING_INSTRUCTIONS = True

# A system prompt is not a lexicon dump. Past these counts the style names what
# it cut and points at the scanner, which carries the whole list and enforces
# it exactly. satoshi's profile has 78 preferred substitutions.
MAX_LISTED = 24
MAX_SWAPS = 12
MAX_PAIRS = 4

# Mechanics rendered as one sentence each, keyed by the value that is worth a
# sentence. A mechanic set to `allow` says nothing a system prompt needs: it is
# the absence of a rule, and spending a line on it teaches the model that this
# writer thinks about semicolons.
_MECHANIC_PROSE = {
    ("em_dash", "forbid"): "Never use an em dash. Recast with a comma, a colon, parentheses, or a new sentence.",
    ("em_dash", "limit"): "Use em dashes sparingly.",
    ("double_hyphen", "forbid"): "Never use a double hyphen as a dash.",
    ("semicolon", "forbid"): "Never use a semicolon. Split the sentence.",
    ("emoji", "forbid"): "Never use emoji.",
    ("curly_quotes", "forbid"): "Use straight quotes and apostrophes, never curly ones.",
    ("one_word_sentence", "forbid"): "Never write a one-word sentence.",
    ("oxford_comma", "require"): "Use the Oxford comma.",
    ("oxford_comma", "forbid"): "Do not use the Oxford comma.",
    ("date_format", "dmy"): "Write dates as 12 September 2025, never as 09/12/2025.",
    ("date_format", "mdy"): "Write dates as September 12, 2025, never as 09/12/2025.",
    ("date_format", "iso"): "Write dates as 2025-09-12.",
}

_NUMERIC_PROSE = {
    "max_sentence_words": "Keep every sentence under %s words.",
    "max_avg_sentence_words": "Average under %s words a sentence across the piece.",
    "max_paragraph_sentences": "Keep paragraphs to %s sentences or fewer.",
    "max_em_dashes_per_1000w": "At most %s em dashes per 1000 words.",
}

# Punctuation refusals, then shape, then the date convention. Sorting the dict
# instead put `date_format` at the top of every profile's hard nos, which reads
# as the thing this writer cares about most. A mechanic missing from this list
# still renders, after the ones that are in it.
_MECHANIC_ORDER = ("em_dash", "double_hyphen", "semicolon", "emoji",
                   "curly_quotes", "one_word_sentence", "oxford_comma",
                   "max_sentence_words", "max_avg_sentence_words",
                   "max_paragraph_sentences", "max_em_dashes_per_1000w",
                   "date_format")


def style_name(voice_name):
    """The name the host shows in the /config picker."""
    return "Rabbit: %s" % voice_name


def style_filename(voice_name):
    """The file name, which is also what an uninstall matches on."""
    return "rabbit-%s.md" % voice_name


def section(profile_md, heading):
    """The body under a `## <heading>` in a profile, up to the next `## `.

    Matched on the heading's opening words rather than the whole line, because
    whit3rabbit's is "## The three essentials (if you forget everything else)"
    and the parenthetical is the writer's, not the template's.
    """
    if not profile_md:
        return ""
    rx = re.compile(r"^##\s+" + re.escape(heading) + r"[^\n]*\n(.*?)(?=^##\s|\Z)",
                    re.M | re.S)
    m = rx.search(profile_md)
    return m.group(1).strip() if m else ""


def _listed(items, limit=MAX_LISTED):
    """(rendered, cut_count) for a list too long to spend a system prompt on."""
    items = [str(i).strip() for i in items if str(i).strip()]
    shown = items[:limit]
    return ", ".join(shown), len(items) - len(shown)


def _mechanics_lines(mechanics):
    keys = [k for k in _MECHANIC_ORDER if k in mechanics]
    keys += sorted(k for k in mechanics if k not in _MECHANIC_ORDER)
    out = []
    for key in keys:
        if key.startswith("_"):
            continue                    # template guidance keys
        value = mechanics[key]
        if key in voices_mod.NUMERIC_MECHANICS:
            template = _NUMERIC_PROSE.get(key)
            if template:
                out.append(template % value)
            continue
        prose = _MECHANIC_PROSE.get((key, value))
        if prose:
            out.append(prose)
    return out


def _first_sentence(text):
    """A profile note's first sentence, for a system prompt.

    Notes are written for a maintainer reading the rules file and run to a
    paragraph. whit3rabbit's closer note ends by explaining why the rule is
    scoped to the formality spine and not the genre columns, which is a fact
    about the register matrix and not an instruction to anybody writing an
    email.
    """
    text = " ".join(str(text).split())
    m = re.search(r"^(.+?[.!?])(\s|$)", text)
    return m.group(1) if m else text


def render(rules, profile_md="", voice_name=None):
    """A rules dict plus the profile markdown, as one output style file.

    `rules` is what `voices.load` returns, already merged if the profile
    extends another, so an inheriting profile renders the union it actually
    enforces rather than its own two-line delta.
    """
    name = voice_name or rules.get("voice") or "voice"
    lines = []

    lines.append("---")
    # json.dumps() rather than a bare `"%s"`: the name always carries a colon
    # (`Rabbit: <name>`), which is ambiguous YAML unquoted, and a voice name
    # is not guaranteed to be free of a `"` or a backslash of its own. JSON
    # string escaping is a valid double-quoted YAML scalar, so this is both
    # a fix and not a new format to maintain.
    lines.append("name: %s" % json.dumps(style_name(name)))
    lines.append("description: %s" % json.dumps(
        "Write as %s. The refusals from that voice profile, in force "
        "every turn." % name))
    lines.append("keep-coding-instructions: %s"
                 % ("true" if KEEP_CODING_INSTRUCTIONS else "false"))
    lines.append("---")
    lines.append("")
    lines.append("# Write as %s" % name)
    lines.append("")
    lines.append("Everything below is one person's voice, from their saved "
                 "profile. It governs prose you write for them to send or "
                 "publish. It does not govern code, tool output, or a report "
                 "about what you just did.")
    lines.append("")

    one_line = section(profile_md, "Voice in one line")
    if one_line:
        lines.append("## In one line")
        lines.append("")
        lines.append(one_line)
        lines.append("")

    essentials = section(profile_md, "The three essentials")
    if essentials:
        lines.append("## First, before anything else")
        lines.append("")
        lines.append(essentials)
        lines.append("")

    mech_lines = _mechanics_lines(rules.get("mechanics", {}))
    words, words_cut = _listed(rules.get("banned_words", []))
    phrases, phrases_cut = _listed(rules.get("banned_phrases", []))
    bans = [e for e in rules.get("banned_regex", []) if isinstance(e, dict)]

    if mech_lines or words or phrases or bans:
        lines.append("## Hard nos")
        lines.append("")
        for line in mech_lines:
            lines.append("- %s" % line)
        if words:
            lines.append("- Never write these words: %s.%s"
                         % (words, _cut_note(words_cut)))
        if phrases:
            lines.append("- Never write these phrases: %s.%s"
                         % (phrases, _cut_note(phrases_cut)))
        for entry in bans:
            lines.append("- %s" % _ban_line(entry))
        lines.append("")

    subs = rules.get("preferred_substitutions", {})
    if subs:
        shown = sorted(subs.items())[:MAX_SWAPS]
        lines.append("## Swaps")
        lines.append("")
        for bad, good in shown:
            lines.append("- %s: %s" % (bad, good))
        cut = len(subs) - len(shown)
        if cut > 0:
            lines.append("- %d more swaps live in the profile. The scanner "
                         "carries all of them." % cut)
        lines.append("")

    pairs = [p for p in rules.get("contrastive_pairs", []) if isinstance(p, dict)]
    if pairs:
        lines.append("## Would write, would never write")
        lines.append("")
        for pair in pairs[:MAX_PAIRS]:
            rule = str(pair.get("rule", "")).strip()
            if rule:
                lines.append("On %s:" % rule)
            lines.append("- Would: %s" % str(pair.get("would", "")).strip())
            lines.append("- Would never: %s"
                         % str(pair.get("would_never", "")).strip())
            lines.append("")
        pairs_cut = len(pairs) - min(len(pairs), MAX_PAIRS)
        if pairs_cut > 0:
            lines.append("%d more contrastive pair(s) live in the profile."
                         % pairs_cut)
            lines.append("")

    required = [r for r in rules.get("required_when", []) if isinstance(r, dict)]
    if required:
        lines.append("## Required")
        lines.append("")
        for entry in required:
            label = str(entry.get("label") or entry.get("id") or "").strip()
            note = _first_sentence(entry.get("note", ""))
            lines.append("- %s%s" % (label, ". " + note if note else ""))
        lines.append("")

    lines.append("## Scope")
    lines.append("")
    lines.append("These are refusals, not a checklist to satisfy. Prose that "
                 "breaks none of them and still sounds like nobody has failed. "
                 "When the user asks to draft, convert, or audit a document, "
                 "run the `rabbit-writes` skill: it loads the whole profile, "
                 "which carries the judgment this summary leaves out, and it "
                 "checks the result with the scanner rather than by eye.")
    lines.append("")

    return "\n".join(lines)


def _cut_note(cut):
    if cut <= 0:
        return ""
    return (" There are %d more; the scanner enforces the full list." % cut)


def _ban_line(entry):
    """One `banned_regex` entry as a sentence.

    An entry carrying `max_allowed` or a rate cap is an overuse rule, not a
    ban. Rendering it as "never" is a rule the writer did not write, and it is
    the kind of overcorrection that makes somebody delete the style.
    """
    label = str(entry.get("label") or entry.get("id") or "").strip()
    note = _first_sentence(entry.get("note", ""))
    cap = entry.get("max_allowed")
    if cap is not None:
        head = "%s: at most %s in a piece." % (label, cap)
    else:
        head = "Never: %s." % label
    example = str(entry.get("example", "")).strip()
    if note:
        return "%s %s" % (head, note)
    if example and "\n" not in example:
        return '%s Not: "%s"' % (head, example)
    return head
