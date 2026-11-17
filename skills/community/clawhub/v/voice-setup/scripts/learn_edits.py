#!/usr/bin/env python3
"""
learn_edits.py - what the user's corrections say about their profile.

`voice-setup`'s adjust mode is three sentences of procedure and no tooling: ask
what read wrong, find the rule that produced it, change that rule. It works and
it runs on recall, which means it runs at the worst possible moment. A person
who has just rewritten your output can tell you the word they hated. A week
later they remember that something felt off.

This reads the diff instead. Given what the skill produced and what the person
turned it into, it proposes profile changes with the count behind each one:

    python3 learn_edits.py converted.md their-edit.md
    python3 learn_edits.py converted.md their-edit.md --voice whit3rabbit
    python3 learn_edits.py converted.md their-edit.md --json

**Nothing here is written.** Every line is a suggestion a person confirms, the
same contract measure_voice.py holds itself to, and for a stronger reason: a
profile is a claim about somebody, and one edit is one edit. A word they
replaced once because it was wrong in that sentence is not a ban. The threshold
below is what separates the two, and it is deliberately not 1.

What it looks for, in the order it is worth acting on:

  substitutions   a word consistently traded for another. The strongest signal
                  a diff carries, and it maps straight onto
                  `preferred_substitutions` and often onto `banned_words`.
  removals        a word or phrase they took out and never put back.
  openers         sentence openers that moved (added or cut), which is where a register lives
                  and what no ban list reaches.
  mechanics       punctuation the edit removed entirely, which is a `mechanics`
                  answer rather than a word.
  measures        how their edit moved the six stylometrics, against the
                  profile's own fingerprint when there is one. This is the half
                  that says the profile's *numbers* were wrong rather than its
                  word list.

Exit codes: 0 always when both files read, 2 on an IO error. This proposes and
never judges, so there is nothing for it to fail.

Stdlib only, 3.9+.
"""

import argparse
import difflib
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
from _bootstrap import cli_error, inflect, voice_check, voices_mod, load_scan, SKILLS_DIR
from rwlib import registers as registers_mod, stylometry

# How many times a change has to repeat before it is worth proposing. Two rather
# than one, and this is the whole difference between reading a diff and reading
# a person: a word replaced once was wrong in that sentence, and a word replaced
# three times is a preference. Three would be safer and would say nothing about
# most real edits, which are short.
MIN_REPEATS = 2

WORD_RX = re.compile(r"[A-Za-z][A-Za-z'\-]*")

# Function words move for a hundred reasons that are not taste, and proposing a
# ban on "the" because a rewrite tightened four sentences is how a profile
# acquires a rule nobody meant. The marker list is already the engine's
# definition of a word that carries register rather than content, so it is what
# gets excluded from the substitution and removal proposals.
STOP = set(stylometry.MARKER_WORDS)


def _words(text):
    return WORD_RX.findall(text.lower())


def substitutions(before, after):
    """{(from, to): n} for a word consistently traded for another.

    Read off difflib's opcodes rather than off two bags of words, because "they
    stopped using X" and "they replaced X with Y" are different proposals and
    only the second one can fill in `preferred_substitutions`. A replace block
    of one word for one word is the case this can be sure about; anything longer
    is a rewrite and is left to the removal pass.
    """
    out = Counter()
    a, b = _words(before), _words(after)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if tag != "replace" or (i2 - i1) != 1 or (j2 - j1) != 1:
            continue
        old, new = a[i1], b[j1]
        if old == new or old in STOP:
            continue
        out[(old, new)] += 1
    return out


def removals(before, after):
    """{word: n} for a content word the edit took out and did not put back."""
    a, b = Counter(_words(before)), Counter(_words(after))
    out = Counter()
    for word, n in a.items():
        if word in STOP or len(word) < 4:
            continue
        if b.get(word, 0) == 0:
            out[word] = n
    return out


def opener_changes(scan, before, after):
    """{opener: (before, after)} for sentence openers whose count moved (added or cut).

    Where a register lives, and the half no ban list reaches: two writers with
    the same average sentence length sound nothing alike if one opens on "But".
    """
    def openers(text):
        found = Counter()
        for sentence in scan.split_sentences(scan.strip_for_stats(text)):
            words = WORD_RX.findall(sentence)
            if words:
                found[words[0].lower()] += 1
        return found

    a, b = openers(before), openers(after)
    return {word: (a.get(word, 0), b.get(word, 0))
            for word in set(a) | set(b)
            if abs(a.get(word, 0) - b.get(word, 0)) >= MIN_REPEATS}


MECHANIC_MARKS = (
    ("em_dash", "em dashes", lambda scan, t: len(scan.PROSE_DASH_RX.findall(t))),
    ("semicolon", "semicolons",
     lambda scan, t: len(re.findall(r";", scan.blank_entities(t)))),
    ("emoji", "emoji", lambda scan, t: len(scan.EMOJI_RX.findall(t))),
    ("one_word_sentence", "one-word sentences",
     lambda scan, t: len([m for m in scan.ONE_WORD_SENTENCE_RX.finditer(t)
                          if not scan.ONE_WORD_ABBREV_RX.fullmatch(m.group(0))])),
)


def mechanic_changes(scan, before, after):
    """[(key, label, before, after)] for punctuation the edit cleared out.

    Only the direction that becomes a rule. A mark the edit *added* is a mark
    the profile should probably stop forbidding, and that is a question for the
    person rather than a proposal, because a rules file is mostly refusals and
    loosening one on a single edit is how a ban quietly disappears.
    """
    out = []
    sb = scan.apply_exemptions(before)
    sa = scan.apply_exemptions(after)
    for key, label, count in MECHANIC_MARKS:
        a, b = count(scan, sb), count(scan, sa)
        if a >= MIN_REPEATS and b == 0:
            out.append((key, label, a, b))
    return out


def measure_moves(scan, before, after, fingerprint):
    """How the edit moved the six stylometrics, and toward what.

    The half that says the profile's numbers were wrong rather than its word
    list. Without a fingerprint it still reports the before and after, because
    "your edit doubled the contraction rate" is a fact about them either way.
    """
    a = scan.compute_stats(scan.strip_for_stats(before))
    b = scan.compute_stats(scan.strip_for_stats(after))
    out = {}
    profile = (fingerprint or {}).get("measures") or {}
    for name in stylometry.MEASURES:
        if a.get(name) is None or b.get(name) is None:
            continue
        entry = profile.get(name)
        row = {"before": a[name], "after": b[name], "profile_mean": None,
               "toward_profile": None}
        if entry:
            row["profile_mean"] = entry["mean"]
            row["toward_profile"] = (abs(b[name] - entry["mean"])
                                     < abs(a[name] - entry["mean"]))
        out[name] = row
    return out


def proposals(scan, before, after, fingerprint):
    subs = substitutions(before, after)
    return {
        "substitutions": [{"from": k[0], "to": k[1], "n": n}
                          for k, n in subs.most_common()
                          if n >= MIN_REPEATS],
        "removals": [{"word": w, "n": n}
                     for w, n in removals(before, after).most_common()
                     if n >= MIN_REPEATS],
        "openers": [{"opener": w, "before": a, "after": b}
                    for w, (a, b) in sorted(opener_changes(scan, before,
                                                           after).items())],
        "mechanics": [{"key": k, "label": label, "before": a, "after": b}
                      for k, label, a, b in mechanic_changes(scan, before, after)],
        "measures": measure_moves(scan, before, after, fingerprint),
        # Every proposal above needed MIN_REPEATS to appear. Published so a
        # reader knows what the silence means: a one-off correction is not
        # absent from the diff, it is below the line this script draws.
        "min_repeats": MIN_REPEATS,
    }


def report(found, voice):
    out = ["what this edit says about %s" % (voice or "the profile"), ""]
    if found["substitutions"]:
        out.append("substitutions, for `preferred_substitutions` and maybe "
                   "`banned_words`")
        for s in found["substitutions"]:
            out.append("  %-22s -> %-22s %d times"
                       % (s["from"], s["to"], s["n"]))
        out.append("")
    if found["removals"]:
        out.append("words the edit took out and never put back")
        for r in found["removals"]:
            out.append("  %-22s %d times" % (r["word"], r["n"]))
        out.append("")
    if found["openers"]:
        out.append("sentence openers that moved, which is where a register "
                   "lives")
        for o in found["openers"]:
            out.append("  %-22s %d -> %d" % (o["opener"], o["before"],
                                             o["after"]))
        out.append("")
    if found["mechanics"]:
        out.append("punctuation the edit cleared out, for `mechanics`")
        for m in found["mechanics"]:
            out.append("  %-22s %d -> 0   consider \"%s\": \"forbid\""
                       % (m["label"], m["before"], m["key"]))
        out.append("")
    if found["measures"]:
        out.append("how the numbers moved")
        for name, row in found["measures"].items():
            toward = ""
            if row["toward_profile"] is True:
                toward = "   toward the profile (%.3g)" % row["profile_mean"]
            elif row["toward_profile"] is False:
                toward = "   away from the profile (%.3g)" % row["profile_mean"]
            out.append("  %-22s %-9s -> %-9s%s"
                       % (name, row["before"], row["after"], toward))
        out.append("")

    if not any(found[k] for k in ("substitutions", "removals", "openers",
                                  "mechanics")):
        out.append("Nothing repeated %d or more times. Either the edit was "
                   "small, or the corrections were one-offs, and a one-off is "
                   "not a rule about a person." % found["min_repeats"])
        out.append("")

    out.append("Nothing above has been written. Each line is a question for the "
               "author, because a profile is a claim about them and one edit is "
               "one edit. Confirm a line, then put it in the rules file by "
               "hand.")
    out.append("A repeated substitution is also worth keeping verbatim under "
               "`contrastive_pairs`: the sentence they wrote against the one "
               "they replaced is worth more than any adjective about their "
               "style.")
    return "\n".join(out)


def main():
    examples = [
        "python3 learn_edits.py converted.md their-edit.md",
        "python3 learn_edits.py converted.md their-edit.md --voice whit3rabbit",
        "python3 learn_edits.py converted.md their-edit.md --voice-rules path/to/dana.rules.json --register blog",
        "python3 learn_edits.py converted.md their-edit.md --json",
    ]
    ap = cli_error.LLMArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        examples=examples)
    ap.add_argument("converted", help="what the skill produced")
    ap.add_argument("edited", help="what the author turned it into")
    ap.add_argument("--voice", metavar="NAME",
                    help="the profile these corrections are about. Only used to "
                         "find its fingerprint, so the measures can be reported "
                         "against the writer's own numbers")
    ap.add_argument("--voice-rules", metavar="PATH",
                    help="path to a voice rules file. Used to find its fingerprint")
    ap.add_argument("--register", metavar="NAME",
                    choices=sorted(registers_mod.registers()),
                    help="the register these texts are written in")
    ap.add_argument("--json", action="store_true", help="machine-readable")
    args = ap.parse_args()

    texts = []
    for path, label in ((args.converted, "converted"), (args.edited, "edited")):
        try:
            with open(path, encoding="utf-8") as fh:
                texts.append(fh.read())
        except OSError as exc:
            print(cli_error.format_file_error(
                "learn_edits.py", path, label, expected_type="file path",
                details=str(exc), examples=examples), file=sys.stderr)
            return 2

    rules_path = None
    if args.voice_rules:
        rules_path = os.path.abspath(args.voice_rules)
    elif args.voice:
        rules_path = os.path.join(voices_mod.VOICES_DIR,
                                  args.voice + voices_mod.RULES_SUFFIX)

    fingerprint = None
    if rules_path:
        path = stylometry.path_for(rules_path, register=args.register)
        if path:
            try:
                fingerprint = stylometry.load(path)
            except (OSError, ValueError) as exc:
                print("learn_edits: %s, so the measures are reported without a "
                      "profile to compare against" % exc, file=sys.stderr)

    scan = load_scan("learn_edits")
    found = proposals(scan, texts[0], texts[1], fingerprint)
    voice_label = args.voice or (voices_mod.strip_rules_suffix(os.path.basename(args.voice_rules))
                                 if args.voice_rules else None)
    if args.json:
        print(json.dumps(dict(found, voice=voice_label), indent=2))
    else:
        print(report(found, voice_label))
    return 0


if __name__ == "__main__":
    sys.exit(main())

