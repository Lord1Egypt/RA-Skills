#!/usr/bin/env python3
"""
measure_voice.py - turn a pile of writing samples into a profile starting point.

The sample workflow in SKILL.md is the fastest way into a voice profile, and it
was described as a manual procedure: run scan.py on each sample, read five
numbers off each report, average them in your head, notice if any sample is
contaminated, and write the result into the profile. That is a script, and
asking a person to do it by hand is how the numbers end up approximate and the
contamination check ends up skipped.

    python3 measure_voice.py sample1.md sample2.md sample3.md
    python3 measure_voice.py samples/*.md --json
    python3 measure_voice.py samples/*.md --name dana --write-fingerprint
    python3 measure_voice.py samples/*.md --questions

What comes out:

  a per-sample table, so an outlier is visible rather than averaged away
  the aggregate, with a spread, because how *consistent* a writer is across
    pieces is itself a fact about them
  the `Measured from samples` block from voices/TEMPLATE.md, ready to paste
  a starter `mechanics` object, ready to paste
  the distributions behind the means, because a mean hides the thing a reader
    recognizes: two writers with the same 18-word average write nothing alike
    if one opens half her sentences with "But"
  a voice fingerprint, with the band of the writer's own samples around it,
    which is what turns "does this sound like them" into a number
  under --questions, an interview built out of all of the above

`--questions` is the samples-plus-interview route, and it prints instead of the
report rather than alongside it. Two blocks, in this order: the questions as
they should be asked, then the counts behind them. A count read out first is a
leading question, and the route exists because self-report and measurement are
two pieces of evidence that are allowed to disagree. Show the numbers after the
answers and the disagreement is visible; show them before and there is nothing
left to disagree with.

It asks only what the samples cannot settle. Every `forbid` suggestion below
rests on a silence rather than a refusal, which is a question. A writer who
used em dashes has already answered that one, so it is not asked again.

The fingerprint is the one output that is a file rather than a paste. It goes
beside the profile as `voices/<name>.fingerprint.json`, and `scan.py --voice`
measures a document against it and reports the distance at P2. Nothing enforces
it: see rwlib/stylometry.py on why a distance that could block a commit would be
the failure this plugin exists to avoid.

Everything in that last block is a **suggestion from three or four documents**,
and it is printed as one. A person who never used a semicolon in four blog posts
may still use them in email, and a profile that bans them because a script
counted zero is a profile that will be wrong in a way its owner did not choose.
Confirm each line with them. The script's job is to make the question specific.

Contamination is checked, not assumed away. A sample carrying a P0 fingerprint
is AI-assisted writing until the author says otherwise, and a tell that gets into
a profile is then reproduced on purpose, forever. Any P0 in any sample exits 1
so this cannot pass unnoticed in a pipeline.

Exit codes: 0 clean, 1 a sample carries a P0 fingerprint, 2 no readable sample.
Stdlib only, 3.9+.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
if "_bootstrap" in sys.modules and getattr(sys.modules["_bootstrap"], "__file__", None) != os.path.join(HERE, "_bootstrap.py"):
    del sys.modules["_bootstrap"]
import _bootstrap
from _bootstrap import cli_error, inflect, voice_check, voices_mod, load_scan, NAME_RX, SKILLS_DIR
from rwlib import registers as registers_mod, stylometry
scan = load_scan()


# The reach-for thesaurus: plain word a person actually writes, beside the
# dressed-up synonyms an inflated draft reaches for instead. Data rather than
# code because it is vocabulary somebody edits, and versioned for the same
# reason the lexicon is. The families drive `preferred_substitutions`
# proposals, which scan.py --apply-safe enforces, so a proposal here is not
# documentation: it is an edit a later conversion makes.
with open(os.path.join(HERE, "thesaurus.json"), encoding="utf-8") as _fh:
    THESAURUS = json.load(_fh)
THESAURUS_FAMILIES = THESAURUS["families"]
THESAURUS_TERMS = [t for f in THESAURUS_FAMILIES
                   for t in [f["reach"]] + f["overreach"]]

# Which measures exist, and in what order, is stylometry.MEASURES: they are the
# block a fingerprint stores and a later attainment check reads. What survives
# here is only the spelling each one uses in voices/TEMPLATE.md, which is not
# always scan.py's key. Two of them differ.
MEASURE_LABELS = {
    "avg_sentence_words": "avg_sentence_words",
    "sentence_sd": "sentence_length_sd",
    "burstiness": "burstiness",
    "mattr": "mattr",
    "em_dashes_per_1k": "em_dashes_per_1000w",
    "contraction_rate": "contraction_rate",
}

# --------------------------------------------------------------------------
# the interview, for the route that reads samples and then asks
# --------------------------------------------------------------------------

# The number SKILL.md commits to, and the reason it is a cap rather than a
# target: the person who quits at question 40 leaves a worse profile than the
# one who answered 10 and stayed engaged.
QUESTION_BUDGET = 10

# One question per mechanic the samples could not settle. None of these carries
# its own count, and that is the rule the whole mode turns on: the count goes in
# the block underneath, after the answer. Asked with the number attached, every
# one of them becomes a leading question and the answer stops being evidence.
MECHANIC_QUESTIONS = {
    "em_dash": "Em dashes. Do you use them, and where would one be wrong?",
    "semicolon": "Semicolons. Do you use them, and where never?",
    "emoji": "Emoji. Ever, and in which register?",
    "curly_quotes": "Curly quotes or straight ones. Do you care, and does the "
                    "answer change with where it gets published?",
    "one_word_sentence": "One-word sentences. A tool you reach for, or a tic "
                         "you cut?",
    "oxford_comma": "The comma before the final `and` in a list. Always, "
                    "never, or by ear?",
    "date_format": "How do you write a date?",
}

# The same, for the shapes a mean hides. These are the ones worth spending a
# question on because the answer and the count so often disagree: almost nobody
# can name the word they open sentences with.
SHAPE_QUESTIONS = {
    "closer": "How do you sign off? Give the exact words, and say which "
              "register each one belongs to.",
    "opener": "Which word do you catch yourself starting sentences with too "
              "often?",
    "hedges": "When you are not certain of something, what do you actually "
              "write?",
    "thesaurus": "When a draft offers the choice between a plain word and its "
                 "dressed-up synonym, which one is you?",
}

# Asked in this order, and trimmed from the end, so the order is a ranking by
# how likely the answer is to disagree with the count. The two marks people
# hold opinions about lead. Then the sign-off, which SKILL.md is right to call
# the line a profile most often gets wrong, and the opener, which almost nobody
# can name about themselves and which the samples can. `emoji` sits low on
# purpose: the count is nearly always zero, the answer is nearly always no, and
# a question whose answer is known is a question wasted out of ten.
DERIVED_ORDER = ("em_dash", "semicolon", "closer", "opener",
                 "one_word_sentence", "hedges", "thesaurus", "emoji",
                 "oxford_comma", "curly_quotes", "date_format")

# What no counter reaches, whatever the samples say. Samples are the record of
# what got written, and a voice is mostly what did not.
FIXED_QUESTIONS = (
    ("belief", "What do you believe about your subject that most people in "
               "your field do not?"),
    ("banned-words", "Which specific words make you close a tab? Which cliches "
                     "or corporate filler read as nails on a chalkboard?"),
    ("hard-no", "What would embarrass you to publish under your name? Give me "
                "one sentence you would refuse to write, and the one you would "
                "write instead."),
    ("red-flags", "What makes you spot an imitation of your writing straight "
                  "away?"),
    ("register-gap", "These samples are whichever registers you happened to "
                     "hand over. Name one you also write in that is not here, "
                     "and say what changes there."),
    ("top-three", "If you could keep only three rules: your one belief, your "
                  "one signature pattern, your one absolute refusal."),
)

# Never cut when the budget binds, implementing this skill's own rule: cut from
# Structure and Tone, never from Hard nos. `register-gap` is in here because a
# profile built from one register and silent about that is a profile that will
# be wrong the first time they write an email.
RESERVED = frozenset({"banned-words", "hard-no", "red-flags", "register-gap",
                      "top-three"})

# How dominant an opener has to be before it is worth a question. Below this it
# is the subject of the piece rather than a habit.
OPENER_SHARE = 0.12

# Openers that are never worth the question. An article is about the noun after
# it, so "opens 7 of 22 sentences with `the`" is a fact about English rather
# than about this writer, and a question that spends one of ten on it comes
# back with a shrug. The interesting openers are the ones a person could
# plausibly own: `But`, `So`, `I`, `This`.
OPENER_NOISE = frozenset({"the", "a", "an"})


def measure_one(scan, path, examples=None):
    """Everything one sample contributes, or None when it cannot be read."""
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        print(cli_error.format_file_error(
            "measure_voice.py", path, "samples", expected_type="file path",
            details=str(exc), examples=examples), file=sys.stderr)
        return None

    # `contraction_rate` arrives in `stats` now. It used to be computed here off
    # a local regex, which was a second counter for a fact scan.py also needed.
    # ste="off": sample statistics, not a defect report. Same reason as
    # audit_voice.py's call.
    findings, stats = scan.scan(text, ste="off")
    p0 = [f for f in findings if f["priority"] == "P0"]
    scored = scan.apply_exemptions(text)

    # The prose, with the markup gone. Everything stylometry measures runs off
    # this copy, because scan.py's own distance check does: a fingerprint built
    # over raw markdown and compared against stripped prose would be measuring
    # two different things, and a code fence has no function words in it at all.
    prose = scan.strip_for_stats(text)

    return {
        "path": path,
        "words": stats.get("word_count", 0),
        "reliability": scan.reliability(stats.get("word_count", 0)),
        "stats": stats,
        "prose": prose,
        # The two halves of the v2 fingerprint block. stylometry.py owns the
        # arithmetic and the stored shape, and this is where the numbers come
        # from, because this is the side of the wall that has scan.py loaded.
        "measures": {k: stats.get(k) for k in stylometry.MEASURES},
        "sentence_lengths": [n for n in (len(scan.tokenize(s))
                                         for s in scan.split_sentences(prose))
                             if n],
        "distributions": stylometry.distributions(
            prose, split_sentences=scan.split_sentences),
        "p0": [{"id": f["id"], "label": f["label"], "line": f["line"]} for f in p0],
        "marks": count_marks(scan, text, scored, stats),
        "thesaurus": count_thesaurus(scored),
    }


def count_marks(scan, raw_text, scored, stats):
    """The raw counts behind every mechanics suggestion.

    Reported alongside the suggestion rather than folded into it. "semicolon:
    forbid" is a claim about a person; "0 semicolons in 4,100 words" is what the
    samples actually said, and only the second is something they can check.
    """
    return {
        "em_dashes": stats.get("em_dashes", 0),
        "em_dashes_per_1k": stats.get("em_dashes_per_1k", 0.0),
        # Entities blanked first, the same as the voice check does: the `;`
        # closing `&nbsp;` is markup, and counting it would report semicolon
        # habits this writer does not have and then suggest allowing them.
        "semicolons": len(re.findall(r";", scan.blank_entities(scored))),
        "emoji": len(scan.EMOJI_RX.findall(scored)),
        "curly_quotes": len(scan.CURLY_QUOTE_RX.findall(scored)),
        "one_word_sentences": len([
            m for m in scan.ONE_WORD_SENTENCE_RX.finditer(scored)
            if not scan.ONE_WORD_ABBREV_RX.fullmatch(m.group(0))]),
        "oxford_missing": len(scan.OXFORD_MISSING_RX.findall(scored)),
        "oxford_present": len(scan.OXFORD_PRESENT_RX.findall(scored)),
        "date_us": len(scan.US_DATE_RX.findall(scored)),
        "date_dmy": len(scan.DMY_DATE_RX.findall(scored)),
        "date_iso": len(scan.ISO_DATE_RX.findall(scored)),
    }


def totals(samples, key):
    return sum(s["marks"].get(key, 0) or 0 for s in samples)


def term_rx(term):
    """Word-boundary regex for a thesaurus term, regular inflections included.

    `helped` is evidence of reaching for `help`, and `utilizes` of reaching
    for `utilize`. Multi-word phrases inflect non-article words (len > 2), joined by
    whitespace wildcards `\\s+`.
    """
    words = term.split()
    parts = [re.escape(w) + (r"(?:s|es|ed|d|ing)?" if len(w) > 2 else "") for w in words]
    return re.compile(r"(?i)\b%s\b" % r"\s+".join(parts))


def count_thesaurus(scored):
    """Every thesaurus term's count, over the exemption-scored text.

    Counted over `scored` rather than the raw text for the same reason the
    semicolon count blanks entities first: a term inside a quoted example is
    somebody else's word. Scripture quoting `require` is not this writer
    reaching for it, and counting it would turn an attributed quotation into
    an inverted-vocabulary note about the profile's owner.
    """
    return {term: len(term_rx(term).findall(scored))
            for term in THESAURUS_TERMS}


def suggest_substitutions(samples):
    """(proposals, notes, family_counts) for `preferred_substitutions`.

    A proposal needs both halves of its evidence: the plain word attested in
    these samples, and the dressed-up synonym at zero. Either half missing
    demotes the family to a note, because the two failure modes are the ones
    this exists to catch. Both halves used is the maybe/perhaps case, where a
    generic plain-English rule would ban a word the writer does use, and the
    inverted case is a writer whose register genuinely runs the other way.
    Nothing here is a refusal. `preferred_substitutions` rewrites one word to
    another under --apply-safe, which is a stronger power than a ban and gets
    treated like one.

    `family_counts` is every family's reach-word count, including the ones
    that produced no proposal, so the report's table can print the number
    behind a row without parsing it back out of the evidence strings.
    """
    words = sum(s["words"] for s in samples) or 1
    totals_map = Counter()
    for s in samples:
        for term, n in s["thesaurus"].items():
            totals_map[term] += n
    proposals, notes, family_counts = [], [], {}
    for family in THESAURUS_FAMILIES:
        reach, reach_n = family["reach"], totals_map[family["reach"]]
        used_over = [(t, totals_map[t]) for t in family["overreach"]
                     if totals_map[t] > 0]
        if reach_n == 0 and not used_over:
            # Neither side appears. Silence, not evidence, and the interview
            # can ask about it if it wants to spend a question.
            continue
        if reach_n == 0:
            notes.append({"kind": "inverted", "reach": reach, "reach_n": 0,
                          "overreach": used_over})
            continue
        if used_over:
            notes.append({"kind": "both", "reach": reach, "reach_n": reach_n,
                          "overreach": used_over})
            continue
        family_counts[reach] = reach_n
        for term in family["overreach"]:
            proposals.append(
                (term, reach, "%r %d times, %r 0 in %d words"
                 % (reach, reach_n, term, words)))
    return proposals, notes, family_counts


def substitutions_block(proposals):
    return json.dumps(
        {"preferred_substitutions":
         {term: reach for term, reach, _ in proposals}},
        indent=2)


def thesaurus_report(proposals, notes, family_counts):
    """The reach-for section of the report.

    Table first, paste block second, non-rules named as non-rules. A family
    the samples use both halves of is printed as a warning rather than folded
    into the block, because a substitution there would rewrite a word the
    writer chose.
    """
    out = ["words to reach for (a measured thesaurus, version %d)"
           % THESAURUS["version"]]
    if not proposals:
        out.append("  no family has its plain word attested and its dressed-up "
                   "synonyms at zero,")
        out.append("  so nothing here proposes a substitution. The samples are "
                   "short, or this")
        out.append("  writer genuinely runs formal. Either way, ask rather "
                   "than assume.")
    else:
        out.append("  %-22s %8s   never appears in these samples"
                   % ("reach for", "attested"))
        for reach in family_counts:
            fam = next(f for f in THESAURUS_FAMILIES if f["reach"] == reach)
            out.append("  %-22s %8d   %s"
                       % (reach, family_counts[reach],
                          ", ".join(fam["overreach"])))
        out.append("")
        out.append("  proposed for the rules file. scan.py --apply-safe "
                   "rewrites each key to its")
        out.append("  value, so this block converts an inflated draft rather "
                   "than just describing the")
        out.append("  problem:")
        for line in substitutions_block(proposals).splitlines():
            out.append("  " + line)
    if notes:
        out.append("")
        out.append("  not rules, printed so nobody paste-copies them:")
        for note in notes:
            if note["kind"] == "both":
                out.append("    both halves used: %r %d vs %s"
                           % (note["reach"], note["reach_n"],
                              ", ".join("%r %d" % (t, n)
                                        for t, n in note["overreach"])))
            else:
                out.append("    inverted: no %r at all, but %s did"
                           % (note["reach"],
                              ", ".join("%r %d" % (t, n)
                                        for t, n in note["overreach"])))
    return "\n".join(out)


def suggest_mechanics(samples):
    """A starter `mechanics` object, with the count behind each line.

    Silence in the samples is read as a ban only where a ban is the cheap
    direction. A writer who used no emoji in four pieces very likely does not use
    them, and being wrong costs one line they delete. A writer with no semicolons
    is a weaker signal, and it is still offered, because the alternative is
    offering nothing and the person then never being asked the question.

    Every value here is returned with its evidence so the caller can print both.
    Nothing in this function decides anything. It proposes, with the count.
    """
    words = sum(s["words"] for s in samples) or 1
    out = []

    def add(key, value, why):
        out.append((key, value, why))

    em = totals(samples, "em_dashes")
    rate = 1000.0 * em / words
    if em == 0:
        add("em_dash", "forbid", "0 in %d words" % words)
    elif rate <= 2.0:
        # Capped a little above what they actually do, not at it. A cap set to
        # the observed rate fails the next piece for being one dash busier than
        # the average of the last four, which is noise rather than a defect.
        cap = max(1.0, round(rate + 0.5, 1))
        add("em_dash", "limit", "%d in %d words (%.1f/1k), cap suggested %.1f"
            % (em, words, rate, cap))
        add("max_em_dashes_per_1000w", cap, "")
    else:
        add("em_dash", "allow", "%d in %d words (%.1f/1k): this writer uses them"
            % (em, words, rate))

    for key, mark, noun in (("semicolon", "semicolons", "semicolons"),
                            ("emoji", "emoji", "emoji"),
                            ("curly_quotes", "curly_quotes", "curly quotes"),
                            ("one_word_sentence", "one_word_sentences",
                             "one-word sentences")):
        n = totals(samples, mark)
        add(key, "forbid" if n == 0 else "allow",
            "%d %s in %d words" % (n, noun, words))

    missing, present = totals(samples, "oxford_missing"), totals(samples, "oxford_present")
    if present > missing * 2:
        add("oxford_comma", "require", "%d serial commas present, %d missing"
            % (present, missing))
    elif missing > present * 2:
        add("oxford_comma", "forbid", "%d serial commas missing, %d present"
            % (missing, present))
    else:
        add("oxford_comma", "allow", "%d present, %d missing: no clear habit"
            % (present, missing))

    dates = {"mdy": totals(samples, "date_us"),
             "dmy": totals(samples, "date_dmy"),
             "iso": totals(samples, "date_iso")}
    non_zero = {k: v for k, v in dates.items() if v > 0}
    if not non_zero:
        # "0 dates" rather than "no dates", so every line in this block carries a
        # count. A suggestion whose evidence is a sentence reads as a judgement,
        # and the point of the column is that the reader can check it.
        add("date_format", "any", "0 dates in %d words" % words)
    else:
        max_val = max(dates.values())
        max_keys = [k for k, v in dates.items() if v == max_val]
        if len(max_keys) > 1:
            add("date_format", "any", "%s: split sample evidence"
                % ", ".join("%d %s" % (v, k) for k, v in sorted(dates.items()) if v > 0))
        else:
            top = max_keys[0]
            add("date_format", top, "%s" % ", ".join("%d %s" % (v, k)
                                                     for k, v in sorted(dates.items()) if v > 0))
    return out


def aggregate(samples):
    """{measure: {"mean", "sd", "min", "max", "n"}} across the samples.

    One call, so the table this script prints and the block the fingerprint
    stores are the same computation. They used to be two, and the report had no
    min or max at all while claiming an outlier was visible rather than
    averaged away.
    """
    return stylometry.measure_stats([s["measures"] for s in samples])


def shown(value):
    """Two decimals for a human. The stored block keeps three, because
    `mattr` moves in the third and `avg_sentence_words` does not, and a table a
    person reads should not print 14.233 words per sentence."""
    return "-" if value is None else round(value, 2)


def measured_block(agg):
    """The `Measured from samples` block out of voices/TEMPLATE.md, filled in."""
    lines = ["```"]
    for key in stylometry.MEASURES:
        entry = agg.get(key)
        lines.append("%-22s %s" % (MEASURE_LABELS.get(key, key) + ":",
                                   "" if entry is None else shown(entry["mean"])))
    lines.append("```")
    return "\n".join(lines)


def mechanics_block(suggestions):
    body = {key: value for key, value, _ in suggestions}
    return json.dumps({"mechanics": body}, indent=2)


def build_fingerprint(samples, name, exemplars=False, register=None):
    """The stored fingerprint, or None when there are too few samples.

    Two is the floor and it is thin: with two samples the calibration band is a
    single number, and a single number cannot say how much a person varies. The
    caller prints that rather than hiding it.

    `register` is the answer to the `register-gap` question this script already
    asks. Samples are whichever registers somebody happened to keep, and a
    fingerprint built from two of them describes neither, so a run that knows
    which register it measured says so and writes to that register's own file.
    """
    if len(samples) < 2:
        return None
    return stylometry.fingerprint(
        [s["prose"] for s in samples], voice=name, exemplars=exemplars,
        sample_measures=[s["measures"] for s in samples],
        sentence_lengths=[s["sentence_lengths"] for s in samples],
        register=register)


# What the vocabulary line filters out beyond MARKER_WORDS. The marker list is
# function words by design ("content words stay out: the fingerprint has to
# survive a change of subject"), so the leftovers it never covered are the
# contractions it stores in uncontracted form and a handful of near-content
# words that rank high in any English prose whatever the subject.
VOCAB_NOISE = frozenset({
    "dont", "cant", "wont", "im", "ive", "youre", "thats", "were", "hes",
    "shes", "theyre", "weve", "lets", "didnt", "wasnt", "wouldnt", "couldnt",
    "doesnt", "isnt", "gonna", "wanna",
    "like", "just", "really", "very", "even", "also", "still", "back",
    "something", "anything", "everything", "nothing", "somebody",
    "everybody", "anybody", "yeah", "okay",
})


def vocabulary(samples):
    """The top content words, with counts, for the vocabulary line.

    The load-bearing nouns and adjectives a profile's reader should reach
    for, as opposed to the thesaurus section, which is about the words to
    avoid. Stopwording is `stylometry.MARKER_SET` plus VOCAB_NOISE, the same
    reuse learn_edits.py makes of it: one stopword list in the repo, and a
    second copy here would drift from it.
    """
    stop = set(stylometry.MARKER_WORDS) | VOCAB_NOISE
    counts = Counter()
    for s in samples:
        for tok in re.findall(r"[a-z']+", s["prose"].lower()):
            clean_tok = tok.replace("'", "")
            if len(clean_tok) >= 4 and clean_tok.isalpha() and clean_tok not in stop:
                counts[clean_tok] += 1
    return counts


def roll_up_distributions(samples):
    """Every per-sample distribution summed into one set of counters.

    One home for the summing. The report prints these and the interview asks
    questions off them, and two loops would be two answers to "which word does
    this person open sentences with", which is exactly the drift rwlib exists to
    prevent one directory over.
    """
    rolled = {key: Counter() for key in
              ("sentence_openers", "paragraph_openers", "connectors",
               "contractions", "hedges", "intensifiers")}
    for s in samples:
        d = s["distributions"]
        for entry in d["sentence_openers"]:
            rolled["sentence_openers"][entry["word"]] += entry["n"]
        for entry in d["paragraph_openers"]:
            rolled["paragraph_openers"][entry["word"]] += entry["n"]
        for group, body in d["connectors"].items():
            rolled["connectors"][group] += body.get("n", round(body.get("per_1k", 0) * d["words"] / 1000.0))
        for entry in d["contractions"]["inventory"]:
            rolled["contractions"][entry["form"]] += entry["n"]
        for entry in d["hedges"]["used"]:
            rolled["hedges"][entry["term"]] += entry["n"]
        for entry in d["intensifiers"]["used"]:
            rolled["intensifiers"][entry["term"]] += entry["n"]
    return rolled


def distribution_report(samples):
    """The shapes the aggregate table averages away.

    Openers, connectors, contractions, hedges and sign-offs. None of these is a
    threshold and none of them ends up in the rules file: they are what a person
    reads before writing the profile markdown, which is the half no counter
    reaches. The script's job here is the same as everywhere else in it, which
    is to make the question specific.
    """
    out = ["distributions (what the averages above hide)"]
    rolled = roll_up_distributions(samples)
    openers = rolled["sentence_openers"]
    para_openers = rolled["paragraph_openers"]
    connectors = rolled["connectors"]
    contractions = rolled["contractions"]
    hedges = rolled["hedges"]
    intensifiers = rolled["intensifiers"]

    def line(label, counter, note=""):
        if not counter:
            out.append("  %-22s %s" % (label, "none in these samples"))
            return
        body = ", ".join("%s %d" % (term, n) for term, n in counter.most_common(8))
        out.append("  %-22s %s%s" % (label, body, note))

    line("sentence openers", openers)
    line("paragraph openers", para_openers)
    line("connectors", connectors, "   (per group, whole sample set)")
    line("contractions used", contractions)
    line("hedges", hedges)
    line("intensifiers", intensifiers)
    line("load-bearing words", vocabulary(samples))
    # No rate here. Each row is the commonest forms per sample summed, so the
    # counts are a shape rather than a total, and the aggregate table above
    # already carries the one contraction number that is exact.
    out.append("")
    out.append("  how each sample ends, verbatim. No counter reaches this, and "
               "how a person signs off")
    out.append("  is the line a profile most often gets wrong:")
    for s in samples:
        closer = s["distributions"]["closer"].strip()
        if closer:
            out.append("    %-20s %s" % (os.path.basename(s["path"])[:20],
                                         closer if len(closer) <= 96
                                         else closer[:93] + "..."))
    return "\n".join(out)


def fingerprint_report(fp, written_to=None):
    band = fp["self_distance"]
    out = ["voice fingerprint (%d samples, %d markers)"
           % (fp["n_samples"], len(stylometry.MARKER_WORDS))]
    out.append("  self-distance          %.2f mean, %.2f max across the samples"
               % (band["mean"], band["max"]))
    out.append("  reading                a later document scoring under %.2f is "
               "indistinguishable" % band["max"])
    out.append("                         from another sample of theirs by this "
               "measure. Past 1.5x that,")
    out.append("                         it is a different register.")
    shape = fp.get("sentence_shape")
    if shape:
        q = shape["quantiles"]
        out.append("  sentence shape         %d sentences, p10 %d, median %d, "
                   "p90 %d, sd %.1f"
                   % (shape["n_sentences"], q[1], q[5], q[9], shape["sd"]))
        out.append("                         %d%% under %d words, %d%% over %d. "
                   "That is the rhythm a"
                   % (round(100 * shape["short_share"]),
                      stylometry.SHORT_SENTENCE_WORDS + 1,
                      round(100 * shape["long_share"]),
                      stylometry.LONG_SENTENCE_WORDS - 1))
        out.append("                         conversion aims at, and it is a "
                   "band rather than a script.")
    if fp.get("measures"):
        out.append("  measures               %d stored with their min and max, "
                   "which is what an" % len(fp["measures"]))
        out.append("                         attainment check compares a "
                   "converted document against.")
    if fp["thin_samples"]:
        out.append("  note                   %d sample(s) under %d words, so the "
                   "band is wider than it"
                   % (fp["thin_samples"], stylometry.RELIABLE_WORDS))
        out.append("                         should be. Add a longer piece "
                   "before trusting it.")
    if fp["n_samples"] < 3:
        out.append("  note                   2 samples means the band is one "
                   "number. It cannot say how")
        out.append("                         much this person varies, only that "
                   "these two differ by that much.")
    if written_to:
        out.append("  written to             %s" % written_to)
        out.append("  scan.py --voice now reports the distance from it, at P2. "
                   "Nothing enforces it:")
        out.append("  a writer is allowed to sound unlike themselves on purpose.")
    else:
        out.append("  not written. Pass --name <voice> --write-fingerprint to "
                   "save it beside the profile.")
    return "\n".join(out)


def derive_questions(samples, suggestions, sub_notes=None):
    """(questions, dropped) for the samples-plus-interview route.

    Only what these documents could not settle gets asked. A `forbid`
    suggestion is a silence rather than a refusal, so it is a question. An
    `allow` that came from observed use is not: a writer who put em dashes in
    four pieces has answered that one already, and asking anyway spends a
    question from a budget of ten and teaches them the interview is not
    listening.

    Every question carries its evidence in a separate key. The caller prints
    the two in two blocks, in that order, and `_no_counts_in_the_asking` is the
    test that keeps them apart.
    """
    mech = {key: (value, why) for key, value, why in suggestions}
    asks = {}

    def ask(qid, question, evidence):
        asks[qid] = {"id": qid, "question": question, "evidence": evidence,
                     "source": "measured"}

    value, why = mech.get("em_dash", (None, ""))
    if value in ("forbid", "limit"):
        # `limit` too. A cap this script chose from four documents is a number
        # nobody has agreed to, and it is about to start reporting findings.
        ask("em_dash", MECHANIC_QUESTIONS["em_dash"], why)
    for key in ("semicolon", "emoji", "curly_quotes", "one_word_sentence"):
        value, why = mech.get(key, (None, ""))
        if value == "forbid":
            ask(key, MECHANIC_QUESTIONS[key], why)
    value, why = mech.get("oxford_comma", (None, ""))
    if value == "allow":
        # "allow" here means the counts came out even, which is the one case
        # where the samples genuinely have no answer in them.
        ask("oxford_comma", MECHANIC_QUESTIONS["oxford_comma"], why)
    value, why = mech.get("date_format", (None, ""))
    if value == "any":
        ask("date_format", MECHANIC_QUESTIONS["date_format"], why)

    rolled = roll_up_distributions(samples)
    closers = [s["distributions"]["closer"].strip() for s in samples]
    closers = [c for c in closers if c]
    if closers:
        ask("closer", SHAPE_QUESTIONS["closer"],
            "; ".join(c if len(c) <= 60 else c[:57] + "..." for c in closers))
    openers = rolled["sentence_openers"]
    # The share is against every sentence, including the ones opening on a word
    # the question skips. Counting only the interesting openers would inflate
    # the share of whichever one survived and turn a habit nobody has into a
    # question asked with confidence.
    sentences = sum(openers.values())
    ranked = [(w, n) for w, n in openers.most_common()
              if w not in OPENER_NOISE]
    if sentences and ranked:
        word, n = ranked[0]
        if n / float(sentences) >= OPENER_SHARE:
            ask("opener", SHAPE_QUESTIONS["opener"],
                "opens %d of %d sentences with %r" % (n, sentences, word))
    if rolled["hedges"]:
        ask("hedges", SHAPE_QUESTIONS["hedges"],
            ", ".join("%s %d" % (term, n)
                      for term, n in rolled["hedges"].most_common(6)))
    # Only the both-used families. A family with one side at zero has already
    # been answered, and the count stays here in the evidence block: reading
    # "maybe 29, perhaps 7" before the question is the leading question this
    # whole mode exists to avoid.
    both = [n for n in (sub_notes or []) if n["kind"] == "both"]
    if both:
        ask("thesaurus", SHAPE_QUESTIONS["thesaurus"],
            "; ".join("%s %d vs %s" % (n["reach"], n["reach_n"],
                                       ", ".join("%s %d" % (t, c)
                                                 for t, c in n["overreach"]))
                      for n in both[:4]))

    derived = [asks[qid] for qid in DERIVED_ORDER if qid in asks]
    fixed = [{"id": qid, "question": question, "evidence": "",
              "source": "fixed"} for qid, question in FIXED_QUESTIONS]
    reserved = [q for q in fixed if q["id"] in RESERVED]
    optional = [q for q in fixed if q["id"] not in RESERVED]

    room = max(0, QUESTION_BUDGET - len(reserved))
    candidates = derived + optional
    # Named rather than silently truncated. A trim that reads as "these were
    # the questions" is the same lie as a rule that never fires.
    return candidates[:room] + reserved, candidates[room:]


def contamination_block(contaminated):
    """The STOP block, in one place, because both outputs end at it.

    The report prints it under the numbers and `--questions` prints it instead
    of an interview. Two copies would let one of them go stale, and the stale
    one would be the half somebody acts on.
    """
    out = ["STOP. %d sample(s) carry a P0 fingerprint, which is evidence of "
           "AI-assisted writing:" % len(contaminated)]
    for s in contaminated:
        for f in s["p0"]:
            out.append("  %s:%s  %s" % (os.path.basename(s["path"]),
                                        f["line"], f["label"]))
    out.append("")
    out.append("Ask the author before going further. A tell that reaches a "
               "profile is reproduced on purpose, forever. If they confirm a "
               "sample was assisted, drop it, rerun this, and record what you "
               "dropped under `## Known contamination`.")
    return "\n".join(out)


def questions_report(samples, questions, dropped, contaminated):
    """The interview, and then the counts, in that order and never the other.

    An interview is refused outright on a contaminated sample set. Every other
    output of this script is a suggestion somebody reads and corrects, and this
    one is a conversation: run it on writing that may not be theirs and the
    first ten answers are anchored to a register nobody chose before anyone has
    thought to check.
    """
    if contaminated:
        return "\n".join([
            contamination_block(contaminated), "",
            "No interview. Ask about the samples first: the answers to ten "
            "questions asked over somebody else's prose are ten answers about "
            "somebody else."])

    out = ["interview: %d question(s) from %d sample(s)"
           % (len(questions), len(samples)), ""]
    out.append("Ask these as written, in two batches. Do not read the block "
               "underneath until")
    out.append("they have answered: a count read out first is a leading "
               "question, and this route")
    out.append("exists because what a person says and what they wrote are two "
               "pieces of evidence")
    out.append("that are allowed to disagree.")
    out.append("Batch 1:")
    for i, q in enumerate(questions, 1):
        if i == 6:
            out.append("")
            out.append("Batch 2:")
        out.append("  %2d  %s" % (i, q["question"]))
    out.append("")

    measured = [q for q in questions if q["evidence"]]
    if measured:
        out.append("after they have answered, what the samples said")
        for q in measured:
            out.append("  %-20s %s" % (q["id"], q["evidence"]))
        out.append("")
        out.append("Where an answer and a count disagree, say so plainly and "
                   "let them settle it. \"I")
        out.append("write short\" against a 24-word average is not a "
                   "correction to make quietly: one of")
        out.append("the two is what they do and the other is what they want, "
                   "and the profile should")
        out.append("record which is which.")
        out.append("")

    if dropped:
        out.append("%d question(s) cut to keep this at %d: %s. Ask them if "
                   "they are still going."
                   % (len(dropped), QUESTION_BUDGET,
                      ", ".join(q["id"] for q in dropped)))
        out.append("")

    out.append("Keep the refusals verbatim, both halves. A sentence they would "
               "not write, beside the")
    out.append("one they would, goes in `contrastive_pairs` and is worth ten "
               "adjectives about tone.")
    out.append("Then: build_voice.py --scaffold, fill the markdown from these "
               "answers, --check, and")
    out.append("scan one of these samples against the finished profile. A "
               "stated rule that fires on")
    out.append("their own writing is the disagreement surfacing, not a bug in "
               "the scan.")
    return "\n".join(out)


def report(samples, agg, suggestions, contaminated, fingerprint=None,
           fingerprint_path=None, sub_proposals=None, sub_notes=None,
           sub_family_counts=None):
    out = ["voice measurement: %d sample(s)" % len(samples), ""]

    out.append("  %-34s %7s  %-12s %s" % ("sample", "words", "reliability", "P0"))
    for s in samples:
        name = os.path.basename(s["path"])
        if len(name) > 34:
            name = name[:31] + "..."
        out.append("  %-34s %7d  %-12s %s"
                   % (name, s["words"], s["reliability"],
                      "-" if not s["p0"] else
                      ", ".join(sorted({f["id"] for f in s["p0"]}))))
    out.append("")

    # The range column is the one the caricature guard reads later, and it is
    # the one a person should read now: a mean with a wide envelope under it is
    # a writer with two registers, and the mean is nobody.
    out.append("aggregate (mean across samples, spread between them, and the "
               "range they cover)")
    for key in stylometry.MEASURES:
        label = MEASURE_LABELS.get(key, key)
        entry = agg.get(key)
        if entry is None:
            out.append("  %-24s %-8s %s" % (label, "-", "not measurable here"))
            continue
        note = ""
        if entry["n"] < len(samples):
            note = "from %d of %d samples" % (entry["n"], len(samples))
        out.append("  %-24s %-8s +/- %-7s %-14s %s"
                   % (label, shown(entry["mean"]), shown(entry["sd"]),
                      "%s to %s" % (shown(entry["min"]), shown(entry["max"])),
                      note))
    out.append("")

    out.append("paste into the profile, under `## Measured from samples`")
    out.append(measured_block(agg))
    out.append("")

    out.append(distribution_report(samples))
    out.append("")

    if fingerprint:
        out.append(fingerprint_report(fingerprint, fingerprint_path))
        out.append("")

    out.append("a starting point for `mechanics`, one question each")
    for key, value, why in suggestions:
        if why:
            out.append("  %-28s %-10s %s" % (key, json.dumps(value), why))
    out.append("")
    out.append(mechanics_block(suggestions))
    out.append("")
    if sub_proposals is not None:
        out.append(thesaurus_report(sub_proposals, sub_notes or [],
                                    sub_family_counts or {}))
        out.append("")

    thin = [s for s in samples if s["words"] < stylometry.RELIABLE_WORDS]
    if thin:
        out.append("note: %d sample(s) under %d words. Stylometry on a short "
                   "piece is noise, and a profile built on it will describe the "
                   "piece rather than the person: %s"
                   % (len(thin), stylometry.RELIABLE_WORDS,
                      ", ".join(os.path.basename(s["path"]) for s in thin)))

    if len(samples) < 3:
        out.append("note: %d sample(s). The spread column above is what tells "
                   "you whether one profile can describe this writer at all, "
                   "and it means little under three." % len(samples))

    if contaminated:
        out.append("")
        out.append(contamination_block(contaminated))

    out.append("")
    out.append("Every suggestion above comes from these documents and nothing "
               "else. Read the samples yourself for what no counter sees: "
               "paragraph openings, how they transition, where they hedge, how "
               "they sign off, and what they refuse to write.")
    return "\n".join(out)


def main():
    examples = [
        "python3 measure_voice.py sample1.md sample2.md sample3.md",
        "python3 measure_voice.py samples/*.md --json",
        "python3 measure_voice.py samples/*.md --name dana --write-fingerprint",
        "python3 measure_voice.py samples/*.md --questions"
    ]
    ap = cli_error.LLMArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        examples=examples
    )
    ap.add_argument("samples", nargs="+", help="files this person wrote")
    out_group = ap.add_mutually_exclusive_group()
    out_group.add_argument("--json", action="store_true", help="machine-readable output")
    out_group.add_argument("--questions", action="store_true",
                           help="print an interview built from these samples instead "
                                "of the report. Asks only what the samples could not "
                                "settle, and holds every count back until after the "
                                "answer, because a count read out first is a leading "
                                "question")
    ap.add_argument("--name", metavar="VOICE",
                    help="the profile these samples belong to. Labels the "
                         "fingerprint, and names the file --write-fingerprint "
                         "writes")
    ap.add_argument("--write-fingerprint", action="store_true",
                    help="save the fingerprint to voices/<name>.fingerprint.json, "
                         "where scan.py --voice will find it. Needs --name")
    ap.add_argument("--register", metavar="NAME",
                    choices=sorted(registers_mod.registers()),
                    help="the register these samples are written in. Writes "
                         "voices/<name>.<register>.fingerprint.json, which "
                         "scan.py and attain.py prefer over the general one "
                         "when scanning that register. Omit it for a profile's "
                         "one general fingerprint")
    ap.add_argument("--with-exemplars", action="store_true",
                    help="embed the writer's own paragraphs in the fingerprint, "
                         "for conditioning a conversion. This copies their prose "
                         "into a file that travels with the plugin, so it is "
                         "opt-in and worth asking them about")
    ap.add_argument("--voices-dir", default=voices_mod.VOICES_DIR,
                    help=argparse.SUPPRESS)
    args = ap.parse_args()

    if args.name and not NAME_RX.match(args.name):
        print(cli_error.format_llm_error(
            "measure_voice.py",
            "--name %r is invalid: name must be a slug matching ^[A-Za-z0-9_-]+$" % args.name,
            parser=ap, examples=examples
        ), file=sys.stderr)
        return 2

    if args.write_fingerprint and not args.name:
        print(cli_error.format_llm_error(
            "measure_voice.py",
            "--write-fingerprint requires --name <voice> to specify the voice profile name and filename",
            parser=ap, examples=examples
        ), file=sys.stderr)
        return 2

    scan = load_scan("measure_voice")
    samples = [s for s in (measure_one(scan, p, examples) for p in args.samples) if s]
    if not samples:
        print(cli_error.format_file_error(
            "measure_voice.py", ", ".join(args.samples), "samples",
            expected_type="one or more readable markdown file paths",
            details="No readable sample files could be opened",
            examples=examples
        ), file=sys.stderr)
        return 2

    agg = aggregate(samples)
    suggestions = suggest_mechanics(samples)
    sub_proposals, sub_notes, sub_family_counts = suggest_substitutions(samples)
    thesaurus_totals = {term: sum(s["thesaurus"].get(term, 0) for s in samples)
                        for term in THESAURUS_TERMS}
    contaminated = [s for s in samples if s["p0"]]
    fingerprint = build_fingerprint(samples, args.name, args.with_exemplars,
                                    args.register)
    questions, dropped = derive_questions(samples, suggestions, sub_notes)

    # Never written from contaminated samples. Every other output of this script
    # is a suggestion a person reads and confirms, and this one is a file a
    # later scan measures against without asking: an assisted sample in it makes
    # the assisted register the target, which is the failure the P0 gate exists
    # to prevent, made permanent.
    written_to = None
    if args.write_fingerprint and fingerprint and not contaminated:
        stem = (args.name if not args.register
                else "%s.%s" % (args.name, args.register))
        written_to = os.path.join(args.voices_dir,
                                  stem + stylometry.FINGERPRINT_SUFFIX)
        try:
            stylometry.save(fingerprint, written_to)
        except OSError as exc:
            print(cli_error.format_file_error(
                "measure_voice.py", written_to, "--write-fingerprint",
                expected_type="writable fingerprint file path (.fingerprint.json)",
                details=str(exc), examples=examples), file=sys.stderr)
            return 2
    elif args.write_fingerprint and not fingerprint:
        print(cli_error.format_llm_error(
            "measure_voice.py",
            "A fingerprint needs at least 2 samples, and one sample has no self-distance to calibrate against",
            parser=ap, examples=examples), file=sys.stderr)
    elif args.write_fingerprint and contaminated:
        print(cli_error.format_llm_error(
            "measure_voice.py",
            "Refused to write a fingerprint from samples that carry a P0. See the report.",
            parser=ap, examples=examples), file=sys.stderr)

    if args.json:
        print(json.dumps({
            "samples": [{"path": s["path"], "words": s["words"],
                         "reliability": s["reliability"], "p0": s["p0"],
                         "marks": s["marks"], "measures": s["measures"],
                         "distributions": s["distributions"]} for s in samples],
            "aggregate": agg,
            "measured_block": measured_block(agg),
            "mechanics": {k: v for k, v, _ in suggestions},
            "mechanics_evidence": {k: w for k, _, w in suggestions if w},
            "thesaurus_version": THESAURUS["version"],
            "substitutions": {term: reach
                              for term, reach, _ in sub_proposals},
            "substitutions_evidence": {term: why
                                       for term, _, why in sub_proposals},
            "substitution_notes": sub_notes,
            "thesaurus_totals": thesaurus_totals,
            "contaminated": [s["path"] for s in contaminated],
            "fingerprint": None if contaminated else fingerprint,
            "fingerprint_written_to": written_to,
            # Both, unconditionally. A caller reading JSON is not choosing
            # between the two outputs the way a caller reading a terminal is,
            # and the anchoring rule is about what gets said to a person.
            "questions": [] if contaminated else questions,
            "questions_dropped": [] if contaminated else dropped,
        }, indent=2))
    elif args.questions:
        print(questions_report(samples, questions, dropped, contaminated))
    else:
        print(report(samples, agg, suggestions, contaminated, fingerprint,
                     written_to, sub_proposals, sub_notes,
                     sub_family_counts))

    return 1 if contaminated else 0


if __name__ == "__main__":
    sys.exit(main())

