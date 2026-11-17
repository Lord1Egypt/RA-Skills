#!/usr/bin/env python3
"""
attain.py - did the conversion land?

`verify.py` answers "did the rewrite break anything". Nothing answered "did it
arrive", and SKILL.md names the gap in prose three separate times: a pass that
cleared eleven mechanical hits, moved the punctuation, and left the register
alone. That is the commonest failure of a voice conversion and no rule-by-rule
report can see it, because every rule passed.

This reads the two documents, measures both against the profile's fingerprint,
and says which of the six measures moved toward it, which missed, and which
went the wrong way.

    python3 attain.py before.md after.md --voice whit3rabbit
    python3 attain.py after.md --voice auto            # no before column
    python3 attain.py before.md after.md --json --check
    python3 attain.py before.md --voice dana --plan    # the shape to write to

Why a script of its own, rather than a flag on one of the two that exist:

  Not `verify.py`. Its `ok` key gates whether `scan.py --apply-safe --write`
  writes at all. Putting a register measurement in there lets a distance stop
  the mechanical fixer, which is the humanizer-shaped failure the whole P2 rule
  exists to prevent.

  Not `scan.py`. Attainment is a two-document question, and that CLI is one
  document with many views. It already juggles stdin, --apply-safe, --write,
  --stdout and --sarif, and a second input path collides with all of them.

**Exit codes, and the rule behind them.** A number about a *document* never
blocks. A number about an *edit* may. `scan.py`'s `voice-distance` is P2 forever
and cannot fail `--check`, because the `rabbit-scan` hook runs it in a
stranger's repository over a document nobody asked to convert. This is
different: you ran it, on a pair, naming a profile, after asking for a
conversion. So:

    0   every verdict, with no flags. The opposite of verify.py's default.
    1   only with --check, and only on `regressed` and `flat`. Never on
        `partial` or `missed`, which mean the document cannot reach the target
        without inventing content, and guardrail 1 forbids that.
    2   an IO error, a profile named by hand that will not read, or a resolved
        profile with no fingerprint.

That last one diverges from scan.py deliberately. There, a missing fingerprint
is the common case and a note. Here you asked for an attainment check, and a
clean report over nothing measured is a false pass.

No pre-commit hook ships for this. `check_precommit_hooks` in scripts/validate.py
fails one that names this script unless it is opt-in and voice-scoped.

Stdlib only, 3.9+.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# See scan.py: rwlib sits beside this file and is not on anybody's PYTHONPATH.
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import scan as scan_mod                                          # noqa: E402
from rwlib import cli_error                                      # noqa: E402
from rwlib import registers as registers_mod                     # noqa: E402
from rwlib import stylometry                                     # noqa: E402
from rwlib import voices as voices_mod                           # noqa: E402

SCHEMA_VERSION = 1

# A measure has to move by more than this, in sample sd, before the gap growing
# counts as a regression. Without it, noise in a measure a pass never touched
# reads as the pass making things worse.
REGRESSION_EPSILON_SD = 0.25

# The same allowance for the document's Delta, as a fraction of the profile's
# own self-distance band rather than an absolute number. A raw Delta means
# nothing on its own, which is the argument stylometry.distance already makes:
# the band is what makes 0.9 readable, so it is also what says how much of a
# move is noise. Without this the per-measure comparison was careful and the
# document verdict was not, and a conversion that landed all six measures and
# drifted the Delta from 0.912 to 0.914 reported `regressed` and failed --check.
REGRESSION_EPSILON_DELTA_FRACTION = 0.05

# `flat` is the verdict this script exists for. A conversion is flat when it
# closed less than this fraction of the distance it had to close, and no single
# measure moved a full sample sd. That is "0.97 to 0.95 and eleven punctuation
# fixes" stated as a rule.
FLAT_DELTA_FRACTION = 0.1
FLAT_MEASURE_SD = 1.0

VERDICTS_THAT_FAIL_CHECK = ("regressed", "flat")


def _read(path, label, examples):
    try:
        with open(path, encoding="utf-8-sig") as fh:
            return fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        print(cli_error.format_file_error(
            "attain.py", path, label, expected_type="file path",
            details=str(exc), examples=examples), file=sys.stderr)
        raise SystemExit(2)


def measure(text, fingerprint):
    """Everything one document contributes: its stats and its distance.

    Both come off scan.py, so the numbers here are the numbers scan.py would
    print. A second measurement path would be the drift rwlib exists to end.
    """
    stats = scan_mod.compute_stats(text)
    prose = scan_mod.strip_for_stats(text)
    return {
        "stats": stats,
        "words": stats.get("word_count", 0),
        "distance": stylometry.distance(fingerprint, prose),
    }


def measure_verdict(before_gap, after_gap, within):
    """One measure's verdict, given both gaps in sample sd.

    `within` is measure_gaps' answer for the after document, and it is None when
    the profile does not carry the measure or the document does not have it.
    None is not a pass, and every caller has to say which it means: here it is
    `unmeasured`, and it stays out of the summary counts a verdict is built on.

    **Tolerance is tested before movement.** A regression is a measure that ends
    up somewhere the profile does not reach, so a measure sitting inside the
    tolerance band is `on_target` whichever way it moved to get there. The other
    order called -0.1 sd to +0.5 sd a regression, and one such row failed the
    whole document under --check, which is the opposite of what a tolerance is
    for.
    """
    if within is None:
        return "unmeasured"
    if within:
        return "on_target"
    if (before_gap is not None and after_gap is not None
            and after_gap > before_gap + REGRESSION_EPSILON_SD):
        return "regressed"
    return "missed"


def compare(before, after, fingerprint, tolerance):
    """The per-measure table, and the document verdict over it."""
    fp_measures = (fingerprint.get("measures") or {})
    after_gaps = stylometry.measure_gaps(fingerprint, after["stats"], tolerance)
    before_gaps = (stylometry.measure_gaps(fingerprint, before["stats"], tolerance)
                   if before else {})

    rows, summary = {}, {"on_target": 0, "missed": 0, "regressed": 0,
                         "unmeasured": 0}
    # A short `before` is exactly as unreliable as a short `after`: its
    # sd_off feeds `measure_verdict`, `_is_flat`, and `_delta_regressed`
    # the same way after's does, and a document that is already inside the
    # band because it is nine words long is sampling noise, not a landed
    # conversion. `before is None` (nothing to compare against) is not this
    # case and stays reliable on its own words alone.
    reliable = (after["words"] >= stylometry.RELIABLE_WORDS
               and (before is None or before["words"] >= stylometry.RELIABLE_WORDS))
    for name in stylometry.MEASURES:
        gap = after_gaps.get(name, {})
        prior = before_gaps.get(name, {})
        entry = fp_measures.get(name) or {}
        a_off = abs(gap["sd_off"]) if gap.get("sd_off") is not None else None
        b_off = abs(prior["sd_off"]) if prior.get("sd_off") is not None else None
        verdict = ("unmeasured" if not reliable
                   else measure_verdict(b_off, a_off, gap.get("within")))
        summary[verdict] += 1
        rows[name] = {
            "before": prior.get("value"),
            "after": gap.get("value"),
            "profile_mean": entry.get("mean"),
            "profile_sd": entry.get("sd"),
            "profile_min": entry.get("min"),
            "profile_max": entry.get("max"),
            "sd_off_before": prior.get("sd_off"),
            "sd_off_after": gap.get("sd_off"),
            "verdict": verdict,
        }

    band = (fingerprint.get("self_distance") or {}).get("max", 0.0)
    a_delta = after["distance"]["delta"]
    b_delta = before["distance"]["delta"] if before else None

    if not reliable or not fp_measures:
        verdict = "unmeasurable"
    elif before is None:
        # One path. There is no edit, so there is nothing to say landed or did
        # not, and every other verdict here is a claim about a pair. The table
        # is still the whole point of running it this way.
        verdict = "unpaired"
    elif summary["regressed"] or _delta_regressed(b_delta, a_delta, band):
        verdict = "regressed"
    elif _is_flat(b_delta, a_delta, band, rows):
        verdict = "flat"
    elif (after["distance"]["verdict"] in ("in_range", "near")
          and summary["missed"] <= 1):
        verdict = "landed"
    else:
        verdict = "partial"

    return {"measures": rows, "summary": summary, "verdict": verdict,
            "reliable": reliable}


def _delta_regressed(before_delta, after_delta, band):
    """The document's Delta moved away from the profile, and it matters.

    Two conditions, and the second is the one measure_verdict states in sd:
    a document that ends inside the writer's own band has not regressed, it has
    arrived, and how it got there is not a defect anybody can act on. The first
    is the noise floor, scaled to the band for the reason the constant gives.
    """
    if before_delta is None:
        return False
    return (after_delta > before_delta + REGRESSION_EPSILON_DELTA_FRACTION * band
            and after_delta > band)


def _is_flat(before_delta, after_delta, band, rows):
    """Punctuation moved and the register did not.

    Needs a before document: with one path there is nothing that could have
    failed to move. Both halves have to hold, because a document that started
    in range has no distance to close and is not flat for saying so.
    """
    if before_delta is None or before_delta <= band:
        return False
    closed = (before_delta - after_delta) / (before_delta - band)
    if closed >= FLAT_DELTA_FRACTION:
        return False
    for row in rows.values():
        a, b = row["sd_off_after"], row["sd_off_before"]
        if a is not None and b is not None and abs(b) - abs(a) >= FLAT_MEASURE_SD:
            return False
    return True


def report(result, voice, fingerprint, tolerance, plan_for=None,
           fingerprint_path=None, register=None):
    fp = fingerprint
    band_max = (fp.get("self_distance") or {}).get("max", 0.0)
    out = ["voice attainment: %s   (%d samples, %d measures, band max %.2f, "
           "tolerance %.1f sd)"
           % (voice, fp.get("n_samples", 0), len(fp.get("measures") or {}),
              band_max, tolerance)]
    # Which fingerprint, named rather than implied. Once a register can have its
    # own, "the profile's fingerprint" is no longer one file, and a reader
    # comparing two runs has no way to tell which target moved.
    if fingerprint_path:
        measured = fp.get("register")
        if register and not measured:
            how = ("no %s fingerprint for this profile, measured against the "
                   "general one" % register)
        elif measured:
            how = "the %s fingerprint" % measured
        else:
            how = "the general fingerprint"
        out.append("  against: %s (%s)"
                   % (os.path.basename(fingerprint_path), how))
    out.append("")

    d = result["distance"]
    out.append("  %-22s %-9s %-9s %-17s %-8s %s"
               % ("measure", "before", "after", "profile", "off", "verdict"))
    out.append("  %-22s %-9s %-9s %-17s %-8s %s"
               % ("distance", _num(d["before"]), _num(d["after"]),
                  "under %.2f" % fp["self_distance"]["max"], "",
                  d["verdict_after"].replace("_", " ")))
    for name in stylometry.MEASURES:
        row = result["measures"][name]
        if row["profile_mean"] is None:
            continue
        out.append("  %-22s %-9s %-9s %-17s %-8s %s"
                   % (name, _num(row["before"]), _num(row["after"]),
                      "%s +/- %s" % (_num(row["profile_mean"]),
                                     _num(row["profile_sd"])),
                      # Signed, because "10 sd under the profile" and "10 sd
                      # over it" call for opposite edits and a rewrite loop
                      # reads this column to decide which.
                      "-" if row["sd_off_after"] is None
                      else "%+.1f sd" % row["sd_off_after"],
                      row["verdict"].replace("_", " ")))

    shape = result.get("sentence_shape")
    if shape:
        out.append("  %-22s %-9s %-9s %-17s"
                   % ("sentence p10/p50/p90", _triple(shape["before"]),
                      _triple(shape["after"]), _triple(shape["profile"])))

    s = result["summary"]
    out.append("")
    missed = [n for n, r in result["measures"].items() if r["verdict"] == "missed"]
    regressed = [n for n, r in result["measures"].items()
                 if r["verdict"] == "regressed"]
    out.append("  %-11s %d of %d measures on target"
               % ("on target", s["on_target"],
                  sum(v for k, v in s.items() if k != "unmeasured")))
    out.append("  %-11s %s" % ("missed", ", ".join(missed) or "none"))
    out.append("  %-11s %s" % ("regressed", ", ".join(regressed) or "none"))
    out.append("  %-11s %s" % ("verdict", result["verdict"]))
    out.append("")
    out.append(VERDICT_NOTES[result["verdict"]])

    if plan_for:
        out.append("")
        out += plan_lines(fp, plan_for)
    return "\n".join(out)


VERDICT_NOTES = {
    "landed": "The register moved, not only the punctuation.",
    "partial": "Some of it landed. Read the missed measures: each one is a "
               "rewrite target, and none of them is worth inventing content to "
               "reach.",
    "flat": "The distance barely moved and no measure moved a full sd. This is "
            "the shallow conversion: mechanics fixed, register untouched. "
            "Guardrail 3 in SKILL.md is the rule it broke.",
    "regressed": "Something moved away from the profile and ended outside it. "
                 "Check the regressed rows before anything else.",
    "unmeasurable": "Under the reliability floor, or the fingerprint carries no "
                    "measures. Nothing here is a verdict about the writing.",
    "unpaired": "One document, so this says where it sits and not whether an "
                "edit landed. Pass the original as well for that.",
}


def plan_lines(fingerprint, paragraph_sentences):
    """Shape targets, one per paragraph, for a conversion about to be written.

    A band and never a script. "Five sentences, at least one under 9 words, at
    least one over 29" is a constraint a rewrite can hold and a later run of
    this script can check. A sampled list of exact per-sentence word counts is
    not: nobody hits it, and chasing it manufactures the cadence
    references/false-positives.md calls a new fingerprint rather than the
    absence of one.
    """
    shape = fingerprint.get("sentence_shape")
    if not shape:
        return ["shape targets: this profile has no sentence shape stored. "
                "Rebuild the fingerprint with measure_voice.py."]
    out = ["shape targets, drawn from %d of this writer's sentences"
           % shape["n_sentences"]]
    for i, n in enumerate(paragraph_sentences, 1):
        t = stylometry.shape_target(shape, n)
        wants = []
        if t["short_at_least"]:
            wants.append("at least %d under %dw"
                         % (t["short_at_least"], t["short_under"]))
        if t["long_at_least"]:
            wants.append("at least %d over %dw"
                         % (t["long_at_least"], t["long_over"]))
        wants.append("median around %dw" % t["median"])
        wants.append("spread about %.0f" % t["sd"])
        out.append("  para %-4d %d sentence%s   %s"
                   % (i, n, " " if n == 1 else "s", ", ".join(wants)))
    out.append("  These are bands. Hitting the median on every sentence is the "
               "uniformity the profile exists to avoid.")
    return out


def _num(value):
    return "-" if value is None else ("%g" % round(value, 3))


def _triple(values):
    return "-" if not values else "/".join(str(v) for v in values)


def paragraph_sentence_counts(text):
    """How many sentences each prose paragraph of a document has.

    What `--plan` writes its targets against. Blank-line separated, the same
    split compute_stats uses, so a bullet list is one paragraph here too and the
    target for it is meaningless in the same well-known way.
    """
    prose = scan_mod.strip_for_stats(text)
    out = []
    for block in re.split(r"\n\s*\n", prose):
        if block.strip():
            n = len(scan_mod.split_sentences(block))
            if n:
                out.append(n)
    return out


def resolve_profile(args, examples):
    """(rules_path, voice_name). Exits 2 rather than measuring against nothing.

    Same resolution order as scan.py and readme_check.py, through
    rwlib.voices.resolve, so the three cannot disagree about whose rules are in
    force. That order ends in nothing rather than in a profile nobody chose, and
    here that means exit 2 with the note attached: an attainment report measured
    against a stranger's fingerprint is worse than no report.

    The other difference is at the end: scan.py continues without a fingerprint
    and this refuses, because a clean attainment report over nothing measured is
    a false pass.
    """
    rules_path = args.voice_rules
    if args.voice == "auto":
        rules_path, _, note = voices_mod.resolve(args.after or args.before)
        if not rules_path:
            print(cli_error.format_file_error(
                "attain.py", args.after or args.before or "auto", "--voice auto",
                expected_type="voice profile (.rules.json)",
                details=note or "No voice profile resolved for document",
                examples=examples), file=sys.stderr)
            raise SystemExit(2)
    elif args.voice:
        rules_path = os.path.join(voices_mod.VOICES_DIR,
                                  args.voice + voices_mod.RULES_SUFFIX)
        if not os.path.exists(rules_path):
            installed_str = ", ".join(voices_mod.installed()) or "none"
            print(cli_error.format_file_error(
                "attain.py", args.voice, "--voice",
                expected_type="installed voice profile name",
                details="No profile named %r in %s. Installed: %s"
                        % (args.voice, voices_mod.VOICES_DIR, installed_str),
                examples=examples), file=sys.stderr)
            raise SystemExit(2)
    try:
        rules = voices_mod.load(rules_path)
    except voices_mod.VoiceError as exc:
        print(cli_error.format_file_error(
            "attain.py", rules_path, "--voice / --voice-rules",
            expected_type="voice rules file path (.rules.json)",
            details=str(exc), examples=examples), file=sys.stderr)
        raise SystemExit(2)
    return rules_path, rules.get("voice", os.path.basename(rules_path))


def main():
    examples = [
        "python3 attain.py before.md after.md --voice whit3rabbit",
        "python3 attain.py after.md --voice auto",
        "python3 attain.py before.md after.md --voice dana --json --check",
        "python3 attain.py draft.md --voice dana --plan",
    ]
    ap = cli_error.LLMArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        examples=examples)
    ap.add_argument("before", help="the document as it was, or the only "
                                   "document when no second path is given")
    ap.add_argument("after", nargs="?",
                    help="the converted document. Omit to measure one document "
                         "with no before column")
    ap.add_argument("--version", action="version",
                    version="attain.py (schema v%d, registers v%s)"
                            % (SCHEMA_VERSION, registers_mod.version()))
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--voice", metavar="NAME",
                       help="profile to measure against. `auto` runs the same "
                            "resolution order as scan.py")
    group.add_argument("--voice-rules", metavar="PATH",
                       help="spell the profile's rules path out")
    ap.add_argument("--profile", metavar="REGISTER",
                    choices=sorted(registers_mod.registers()),
                    help="the register the documents are in. Measures against "
                         "that register's own fingerprint when the profile has "
                         "one, and against the general fingerprint otherwise. A "
                         "chat message measured against an essay fingerprint "
                         "reports a change of form as a conversion that missed")
    ap.add_argument("--tolerance", type=float,
                    default=stylometry.ATTAIN_TOLERANCE, metavar="SD",
                    help="how far off the profile mean a measure may sit before "
                         "it is called missed, in sample sd")
    ap.add_argument("--plan", action="store_true",
                    help="print the per-paragraph shape targets for the first "
                         "document, for a conversion about to be written")
    ap.add_argument("--json", action="store_true",
                    help="machine-readable, for a rewrite loop")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 on `regressed` or `flat`. Never on `missed`: "
                         "a document that cannot reach the target without "
                         "inventing content is a legitimate outcome")
    args = ap.parse_args()

    if not args.voice and not args.voice_rules:
        args.voice = "auto"

    rules_path, voice_name = resolve_profile(args, examples)
    fingerprint_path = stylometry.path_for(rules_path, args.profile)
    if not fingerprint_path:
        # Resolved by walking up from this file rather than assembled from the
        # repository root, so the command in the error works from whatever
        # directory somebody ran this in. Same rule as every other sibling
        # lookup in the plugin.
        measure_script = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                                      "voice-setup", "scripts",
                                      "measure_voice.py")
        print(cli_error.format_file_error(
            "attain.py", rules_path, "fingerprint",
            expected_type="voice fingerprint file (.fingerprint.json)",
            details="%s has no fingerprint beside it. Build one with:\n  python3 %s sample1.md sample2.md sample3.md --name %s --write-fingerprint"
                    % (os.path.basename(rules_path), measure_script, voice_name),
            examples=examples), file=sys.stderr)
        return 2
    try:
        fingerprint = stylometry.load(fingerprint_path)
    except (OSError, ValueError) as exc:
        print(cli_error.format_file_error(
            "attain.py", fingerprint_path, "fingerprint",
            expected_type="voice fingerprint file (.fingerprint.json)",
            details=str(exc), examples=examples), file=sys.stderr)
        return 2
    fp_reg = fingerprint.get("register")
    if fp_reg and fp_reg != args.profile:
        print(cli_error.format_file_error(
            "attain.py", fingerprint_path, "fingerprint",
            expected_type="voice fingerprint file (.fingerprint.json)",
            details="Fingerprint register %r does not match target register %r"
                    % (fp_reg, args.profile),
            examples=examples), file=sys.stderr)
        return 2

    before_text = _read(args.before, "before", examples)
    after_text = _read(args.after, "after", examples) if args.after else None

    try:
        if after_text is None:
            before, after = None, measure(before_text, fingerprint)
        else:
            before, after = (measure(before_text, fingerprint),
                             measure(after_text, fingerprint))

        result = compare(before, after, fingerprint, args.tolerance)
    except ValueError as exc:
        print(cli_error.format_llm_error(
            "attain.py", str(exc), parser=ap, examples=examples), file=sys.stderr)
        return 2

    result["distance"] = {
        "before": before["distance"]["delta"] if before else None,
        "after": after["distance"]["delta"],
        "band_max": fingerprint["self_distance"]["max"],
        "verdict_before": before["distance"]["verdict"] if before else None,
        "verdict_after": after["distance"]["verdict"],
        "contributors_after": after["distance"]["contributors"],
    }
    shape = fingerprint.get("sentence_shape")
    if shape:
        # Keyed off `before`, the measure, not off `before_text`, the string.
        # With one path that path is the document being measured, and every
        # other block in the result reports it under `after`. Reading the text
        # instead put the same document under `before` here and left `after`
        # null, so the report's shape row sat in a different column from its
        # own distance row.
        result["sentence_shape"] = {
            "before": _percentiles(before_text) if before else None,
            "after": _percentiles(after_text if after_text is not None
                                  else before_text),
            "profile": [shape["quantiles"][1], shape["quantiles"][5],
                        shape["quantiles"][9]],
        }

    plan_for = paragraph_sentence_counts(before_text) if args.plan else None
    if args.json:
        payload = dict(result, schema_version=SCHEMA_VERSION, voice=voice_name,
                       fingerprint_schema=fingerprint.get("schema_version"),
                       tolerance_sd=args.tolerance)
        if plan_for:
            payload["shape_targets"] = [
                stylometry.shape_target(shape, n) for n in plan_for] if shape else []
        print(json.dumps(payload, indent=2))
    else:
        print(report(result, voice_name, fingerprint, args.tolerance, plan_for,
                     fingerprint_path, args.profile))

    if args.check and result["verdict"] in VERDICTS_THAT_FAIL_CHECK:
        return 1
    return 0


def _percentiles(text):
    """p10, p50, p90 of one document's sentence lengths, or None under three
    sentences, where a percentile is describing individual sentences."""
    prose = scan_mod.strip_for_stats(text)
    lengths = sorted(n for n in (len(scan_mod.tokenize(s))
                                 for s in scan_mod.split_sentences(prose)) if n)
    if len(lengths) < 3:
        return None
    def at(frac):
        return lengths[min(len(lengths) - 1, int(frac * len(lengths)))]
    return [at(0.1), at(0.5), at(0.9)]


if __name__ == "__main__":
    sys.exit(main())
