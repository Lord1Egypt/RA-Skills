#!/usr/bin/env python3
"""
audit_voice.py - does a profile survive the prose it was built from.

`build_voice.py --check` proves a rule fires on a probe sentence written for
it. The other half of validation is the inverse: run the finished profile over
the writer's own corpus and see which rules fire on the prose they came from.
A ban that trips the writer's own sentences is one of two things, and only the
writer can say which: a rule that is too broad, or a variant register the
profile has not accounted for. Until now that half was a procedure in SKILL.md
and a hand-run scan. This is the script for it.

    python3 audit_voice.py john sample1.md sample2.md sample3.md
    python3 audit_voice.py voices/dana.rules.json docs/dana/*.md --register formal
    python3 audit_voice.py john samples/*.md --json

Exactly one `scan.scan()` call per sample supplies everything: the voice-band
findings (fire-backs), the engine's own P0 tells, the fingerprint distance in
`stats["voice_distance"]`, and the numbers the cap suggestions are measured
from. There is no second measurement path here, because a second one drifting
from the first is the bug `rwlib` exists to end.

What it judges, and what it merely reports:

  fire-backs       a profile rule firing on the writer's own prose. The only
                   judgment: exit 1. `voice-distance` is exempt because it is a
                   measurement, not a rule, and `voice-oxford-comma` is exempt
                   because the engine itself holds it at P2 on the ground that
                   no regex can settle a serial comma.
  distance         per-sample distance from the fingerprint band. A note. An
                   out-of-range sample is a different register, not a broken
                   rule, and the suggestion is a per-register fingerprint
                   rather than a wider band.
  shape            per-sample sentence medians. A note. A wide spread means
                   the corpus holds two registers and the fingerprint is the
                   average of two people, which is nobody.
  known tells      engine P0 patterns over the corpus, which over one writer
                   are usually false positives ("of course," flagged as a
                   chatbot artifact over a writer who leans on the phrase).
                   Reported as candidates for the profile's
                   `## Known contamination` section. Never exit-affecting, and
                   the `safety` band is excluded: that band is unsuppressible
                   by design, so a concealed injection is never a tell to
                   record as somebody's habit.
  caricature       where a sample out-writers the writer: measures past the
                   profile's own envelope in the profile's own direction.
                   `stylometry.caricature` is calibrated in `PROOF.md` and
                   this is its first caller. A note.

**Nothing here is written.** Every suggestion carries its count, the same
contract `learn_edits.py` holds, and for the same reason: a profile is a claim
about somebody, and their own prose disagreeing with it is the disagreement
surfacing, not a bug in the scan.

Two limits worth knowing before reading a report. Samples that built the
fingerprint read in-range by construction, because the band is calibrated off
those same samples: the distance half is really testing held-out corpus. And
pass whole documents, not chunks: `max_allowed`, paragraph caps, and rate caps
are per-document rules, and a corpus of split chunks dilutes every ceiling
while drifting under the 250-word reliability floor.

Exit codes: 0 no rule fired on the writer's own prose, 1 at least one did,
2 on a usage or IO error.

Stdlib only, 3.9+.
"""

import argparse
import json
import os
import re
import statistics
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
if "_bootstrap" in sys.modules and getattr(sys.modules["_bootstrap"], "__file__", None) != os.path.join(HERE, "_bootstrap.py"):
    del sys.modules["_bootstrap"]
import _bootstrap
from _bootstrap import cli_error, inflect, voices_mod, load_scan
from rwlib import registers as registers_mod, stylometry

# An engine P0 pattern becomes a Known contamination candidate at this many
# occurrences across this many samples. The floor is MIN_REPEATS in
# learn_edits.py plus one, because these are per-occurrence counts and one
# essay leaning on a phrase twice is that essay's business. Below the line the
# count is still printed, so the silence has a stated meaning rather than an
# implied one.
KNOWN_TELL_MIN_HITS = 3
KNOWN_TELL_MIN_SAMPLES = 2

# A per-sample sentence-median range this wide, over at least this many
# samples, means the corpus holds two sentence registers. Six words is under
# the width the engine's own short/long sentence bands (8 and 30 words) imply
# one register can vary by, and three samples is the floor the caricature
# envelope uses: two samples show a difference, not a spread.
SPREAD_WIDE_WORDS = 6
SPREAD_MIN_SAMPLES = 3

# Voice-band findings that never count as fire-backs. `voice-distance` is a
# measurement rather than a rule, and `voice-oxford-comma` is held at hard P2
# by the engine on the ground that no regex can settle a serial comma: the
# house profile requires one and would fire the advisory on its own prose
# constantly, which would make this audit noise for exactly the profile that
# runs every day.
FIRE_BACK_EXEMPT_IDS = ("voice-distance", "voice-oxford-comma")

# The mechanics whose findings are a numeric cap, mapped to the rules key the
# suggestion would raise and the stats key the measured maximum comes from.
MECHANIC_CAPS = {
    "voice-sentence-length": ("max_avg_sentence_words", "avg_sentence_words"),
    "voice-paragraph-length": ("max_paragraph_sentences", None),
    "voice-em-dash-rate": ("max_em_dashes_per_1000w", "em_dashes_per_1k"),
}

BAN_IDS = ("voice-banned-word", "voice-banned-phrase")


def resolve_voice(target, voices_dir):
    """Rules path from a profile name or a path, the way build_voice does it.

    A suffix is stripped and `.rules.json` put back, so a name, a rules path,
    a markdown path, and a fingerprint path all land on the rules file.
    """
    stem = target
    for suffix in (voices_mod.RULES_SUFFIX, stylometry.FINGERPRINT_SUFFIX,
                   ".md"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    if os.sep in target or (os.altsep and os.altsep in target):
        return os.path.abspath(stem + voices_mod.RULES_SUFFIX)
    return os.path.join(voices_dir, os.path.basename(stem)
                        + voices_mod.RULES_SUFFIX)


def load_rules_pair(rules_path, voices_dir):
    """(merged rules, raw child json).

    `voices_mod.load` resolves `extends`, so the merged rules are what the
    scanner enforces. The raw child is re-read so a fired entry can be
    labelled inherited: a ban that came from the parent has to be narrowed in
    the parent, because the union merge does not let a child drop it.
    """
    rules = voices_mod.load(rules_path, voices_dir)
    with open(rules_path, encoding="utf-8") as fh:
        raw = json.load(fh)
    return rules, raw


def ban_term_map(rules, raw_child):
    """{lowercased term: (rules key, term as written, inherited)}.

    The voice findings for a ban carry the matched text, not the entry, so
    attribution runs backwards through `inflect.expand` over both the child's
    entries and the merged list. The child's terms go in first and `setdefault`
    keeps them, so anything the merged list adds on top came from a parent.
    That ordering is the whole test: the two lists come from two separate
    `json.load` calls, so no entry in one is the same *object* as its twin in
    the other and identity cannot tell them apart.
    """
    out = {}
    for key in ("banned_words", "banned_phrases"):
        for term in inflect.expand(raw_child.get(key) or []):
            out.setdefault(term.lower(), (key, term, False))
        for term in inflect.expand(rules.get(key) or []):
            out.setdefault(term.lower(), (key, term, True))
    return out


def entry_ids(rules, raw_child, key):
    """({entry ids in the child}, {entry ids only in the merged parent})."""
    child = {e.get("id") for e in (raw_child.get(key) or []) if isinstance(e, dict)}
    all_ids = {e.get("id") for e in (rules.get(key) or []) if isinstance(e, dict)}
    return child, all_ids - child


def scoped_out_count(rules, register):
    """Rules the register being scanned never ran, so silence is not misread.

    Entries scoped with `applies_to_registers` away from this register, plus
    `mechanics_by_register` overrides for other registers.
    """
    n = 0
    for key in ("banned_regex", "signature_moves", "required_when"):
        for entry in rules.get(key) or []:
            applies = entry.get("applies_to_registers") if isinstance(entry, dict) else None
            if applies and register not in applies:
                n += 1
    for other in (rules.get("mechanics_by_register") or {}):
        if other != register:
            n += 1
    return n


def audit_one(scan, path, text, rules, fingerprint, register):
    """One sample's whole contribution, off exactly one scan() call."""
    # ste="off": this measures one writer's own rules firing over their own
    # prose. A standards band in the same list conflates the two judgments.
    findings, stats = scan.scan(text, profile=register, exempt=True,
                                voice_rules=rules, suppressions=True,
                                voice_fingerprint=fingerprint, ste="off")
    live = [f for f in findings if "suppressed" not in f]
    prose = scan.strip_for_stats(text)
    # The same exempted copy `scan()` just measured over, so the numbers the
    # suggestions carry are the numbers the engine enforced against.
    scored = scan.apply_exemptions(text)
    lengths = [len(scan.tokenize(s)) for s in scan.split_sentences(prose)]
    caric = stylometry.caricature(fingerprint, stats) if fingerprint else None
    return {
        "basename": os.path.basename(path),
        "words": stats.get("word_count", 0),
        "reliable": stats.get("word_count", 0) >= stylometry.RELIABLE_WORDS,
        "stats": stats,
        "voice": [f for f in live if f.get("band") == "voice"],
        # The `safety` band is deliberately not in here. `## Known
        # contamination` is where a writer records an engine tell that is a
        # false positive *over them*, and a concealed prompt injection is
        # never that: the band is unsuppressible by design, so proposing one
        # as a habit to record is advice the engine would refuse to honour.
        "p0": [f for f in live if f.get("priority") == "P0"
               and f.get("band") not in ("voice", "safety")],
        "distance": stats.get("voice_distance"),
        "sentence_median": statistics.median(lengths) if lengths else None,
        "max_paragraph_sents": max_paragraph_sentences(scan, scored),
        "signature": signature_counts(scan, scored, stats, rules, register),
        "caricature": caric,
    }


def signature_counts(scan, scored, stats, rules, register):
    """{entry id: (hits, rate per 1k)} recomputed with each entry's own rx.

    Counting rather than reading findings back, because the suggestion needs
    the observed maximum even in a sample where the ceiling did not fire, and
    the scanner only reports the overage.

    The denominator is `stats["word_count"]`, which is what `apply_voice_rules`
    divides by. Counting the exempted copy's own tokens instead is a second
    measurement path: it keeps the headings and tables `strip_for_stats` drops,
    so it reads a lower rate than the engine did and "raise the cap to the
    measured maximum" lands under the rate that fired.
    """
    words = stats.get("word_count", 0)
    out = {}
    for entry in rules.get("signature_moves") or []:
        if not scan.in_register(entry, register):
            continue
        try:
            rx = re.compile(entry["rx"])
        except (KeyError, re.error):
            continue
        hits = len([m for m in rx.finditer(scored) if m.group(0).strip()])
        out[entry.get("id")] = (hits,
                                (hits / words * 1000.0) if words > 0 else 0.0)
    return out


def max_paragraph_sentences(scan, scored):
    """The observed maximum for `max_paragraph_sentences`, engine-parity.

    Same split and the same `is_prose_block` gate `apply_voice_rules` uses,
    over the same exempted copy. Measured any other way a six-item bullet list
    reads as one 24-sentence paragraph, which is the case `is_prose_block`
    exists for, and the suggestion becomes "raise the cap to 24" over a
    document where the engine counted four.
    """
    worst = 0
    for block in re.split(r"\n\s*\n", scored):
        body = block.strip()
        if body and scan.is_prose_block(body):
            worst = max(worst, len(scan.split_sentences(body)))
    return worst


def fire_backs(samples, rules, raw_child, term_map):
    """Aggregated rows, one per (finding id, term). Drives exit 1 alone."""
    regex_child, regex_parent = entry_ids(rules, raw_child, "banned_regex")
    sig_child, sig_parent = entry_ids(rules, raw_child, "signature_moves")
    req_child, req_parent = entry_ids(rules, raw_child, "required_when")
    rows = {}

    def parent_of(finding_id):
        if finding_id in regex_parent or finding_id in sig_parent \
                or finding_id in req_parent:
            return True
        return False

    for sample in samples:
        for f in sample["voice"]:
            if f["id"] in FIRE_BACK_EXEMPT_IDS:
                continue
            fid = f["id"]
            if fid in BAN_IDS:
                # Whitespace collapsed before the lookup, because
                # `phrase_regex` lets a banned phrase flex across a line break
                # and the matched text then comes back with the newline in it.
                # Left raw it misses `term_map` entirely, so the row is
                # attributed to the wrong list, loses its inherited flag, does
                # not aggregate with the same ban matched on one line, and
                # prints a newline through the middle of a fixed-width column.
                matched = re.sub(r"\s+", " ", f.get("match") or "").strip()
                key2, term, inherited = term_map.get(
                    matched.lower(),
                    ("banned_phrases" if fid == "voice-banned-phrase"
                     else "banned_words", matched, False))
                detail = '"%s"' % term
            elif fid in MECHANIC_CAPS:
                key2, term, inherited = MECHANIC_CAPS[fid][0], fid, False
                detail = f.get("label") or fid
            else:
                key2, term, inherited = "entry", fid, parent_of(fid)
                detail = f.get("label") or fid
            row_key = (fid, str(term).lower())
            row = rows.setdefault(row_key, {
                "id": fid, "term": term, "key": key2, "detail": detail,
                "inherited": inherited, "priority": f.get("priority"),
                "times": 0, "samples": []})
            if sample["basename"] not in row["samples"]:
                row["samples"].append(sample["basename"])
            row["times"] += 1
    return sorted(rows.values(),
                  key=lambda r: (-r["times"], r["id"], str(r["term"])))


def cap_suggestions(samples, rules, scan, register, backs):
    """Rows for numeric caps the writer's own prose broke, measured not argued.

    Each carries the cap the profile set and the maximum the corpus actually
    reached, because "raise the cap" without the number is an instruction
    nobody can act on.
    """
    mech = scan.voice_mechanics(rules, register)
    back_ids = {r["id"] for r in backs}
    out = []

    for fid, (rules_key, stats_key) in MECHANIC_CAPS.items():
        cap = mech.get(rules_key)
        if cap is None or fid not in back_ids:
            continue
        if stats_key:
            measured = max(s["stats"].get(stats_key) or 0 for s in samples)
        else:
            measured = max(s["max_paragraph_sents"] for s in samples)
        out.append({"id": fid, "key": rules_key, "cap": cap,
                    "measured_max": measured})

    per_entry = {}
    for sample in samples:
        for entry_id, (hits, rate) in sample["signature"].items():
            best = per_entry.setdefault(entry_id, [0, 0.0])
            best[0] = max(best[0], hits)
            best[1] = max(best[1], rate)
    for entry in rules.get("signature_moves") or []:
        entry_id = entry.get("id")
        if entry_id not in per_entry or entry_id not in back_ids:
            continue
        hits, rate = per_entry[entry_id]
        if entry.get("max_allowed") is not None:
            out.append({"id": entry_id, "key": "signature_moves.max_allowed",
                        "cap": entry["max_allowed"], "measured_max": hits})
        if entry.get("max_per_1000w") is not None:
            out.append({"id": entry_id,
                        "key": "signature_moves.max_per_1000w",
                        "cap": entry["max_per_1000w"],
                        "measured_max": round(rate, 2)})
    return out


def distance_summary(samples):
    counts = Counter()
    rows = []
    for sample in samples:
        d = sample["distance"]
        if not d:
            counts["unmeasured"] += 1
            continue
        if not d.get("reliable"):
            counts["unreliable"] += 1
            continue
        counts[d.get("verdict", "unmeasured")] += 1
        if d.get("verdict") != "in_range":
            rows.append(sample)
    return rows, counts


def shape_receipt(samples, fingerprint):
    medians = [s["sentence_median"] for s in samples
               if s["sentence_median"] is not None]
    receipt = {
        "per_sample_median": medians,
        "range": (max(medians) - min(medians)) if medians else None,
        "wide": bool(medians and len(medians) >= SPREAD_MIN_SAMPLES
                     and max(medians) - min(medians) >= SPREAD_WIDE_WORDS),
        "profile_per_sample_median": (((fingerprint or {})
                                       .get("sentence_shape") or {})
                                      .get("per_sample_median")),
    }
    return receipt


def known_tells(samples, rules):
    """Engine P0 patterns over the corpus, with the Known contamination bar."""
    agg = {}
    for sample in samples:
        seen = Counter()
        for f in sample["p0"]:
            seen[(f["id"], (f.get("match") or "").lower())] += 1
        for (fid, match), n in seen.items():
            row = agg.setdefault((fid, match), {
                "id": fid, "match": match,
                "label": next((g["label"] for g in sample["p0"]
                               if g["id"] == fid), fid),
                "times": 0, "samples": []})
            row["times"] += n
            if sample["basename"] not in row["samples"]:
                row["samples"].append(sample["basename"])
    sig_note = {}
    for entry in rules.get("signature_moves") or []:
        try:
            rx = re.compile(entry["rx"])
        except (KeyError, re.error):
            continue
        sig_note[entry.get("id")] = rx
    rows = []
    for row in agg.values():
        row["candidate"] = (row["times"] >= KNOWN_TELL_MIN_HITS
                            and len(row["samples"]) >= KNOWN_TELL_MIN_SAMPLES)
        row["signature_move"] = next(
            (sid for sid, rx in sig_note.items()
             if row["match"] and rx.search(row["match"])), None)
        rows.append(row)
    return sorted(rows, key=lambda r: (-r["times"], r["id"], r["match"]))


def contributor_line(distance, n=3):
    parts = ["%s %+.1fsd" % (c["marker"], c["z"])
             for c in (distance.get("contributors") or [])[:n]]
    return ", ".join(parts)


def scale_mismatch(out_samples, fingerprint):
    """(fingerprint sample words, out-of-range sample words), or None.

    An out-of-range verdict has two live explanations and they suggest
    different fixes. A different register wants a per-register fingerprint. A
    document half the size of the ones the band was calibrated on is just
    noisier in Delta terms, and wants the fingerprint rebuilt from documents
    the size of the ones that will actually be scanned. The fingerprint
    stores its own sample word counts, so the two are separable.
    """
    fp_words = (fingerprint or {}).get("sample_words") or []
    if not fp_words or not out_samples:
        return None
    fp_median = statistics.median(fp_words)
    out_median = statistics.median(s["words"] for s in out_samples)
    if fp_median and (out_median < 0.5 * fp_median
                      or out_median > 2.0 * fp_median):
        return fp_median, out_median
    return None


def report(voice, register, samples, fingerprint, fingerprint_path,
           scoped_out, backs, caps, dist_rows, dist_counts, shape, tells,
           caric_rows):
    total_words = sum(s["words"] for s in samples)
    out = ["what this corpus says about %s" % voice, ""]
    fp_note = "no fingerprint beside the rules file"
    # A hand-edited or truncated file can load as JSON and still carry no
    # band. Read once here and reported as missing rather than formatted, or
    # the whole audit ends in a traceback over an optional measurement.
    band = (fingerprint or {}).get("self_distance", {}).get("max")
    if fingerprint:
        scope = fingerprint.get("register") or "general"
        fp_note = "fingerprint %s (%s, %s)" % (
            os.path.basename(fingerprint_path), scope,
            "band max %.2f" % band if band is not None
            else "no self-distance band, so it cannot be read")
    out.append("%d sample(s), %s words, scanned as %s, %s"
               % (len(samples), format(total_words, ","),
                  register, fp_note))
    if scoped_out:
        out.append("  note  %d rule(s) scoped to registers other than %s "
                   "did not run" % (scoped_out, register))
    out.append("")

    if backs:
        out.append("rules that fired on this writer's own prose")
        for row in backs:
            out.append("  %-22s %-24s %d time(s) in %d sample(s)  [%s]"
                       % (row["id"], row["detail"][:24], row["times"],
                          len(row["samples"]), row["priority"] or ""))
            if row["inherited"]:
                out.append("    -> inherited from a parent profile: narrow it "
                           "there, a child cannot drop an inherited ban")
            elif row["id"] in BAN_IDS:
                out.append("    -> drop it, narrow it with "
                           "applies_to_registers, or accept the variant "
                           "register")
        out.append("")
    else:
        out.append("Nothing fired. Every rule in this profile stayed quiet "
                   "over %d sample(s), %s words."
                   % (len(samples), format(total_words, ",")))
        out.append("")

    for row in caps:
        out.append("  %-22s cap %-4s measured max %s"
                   % (row["key"], row["cap"], row["measured_max"]))
    if caps:
        out.append("    -> raise the cap to the measured maximum, or drop it: "
                   "a cap the writer's own prose breaks is not a tolerance")
        out.append("")

    if fingerprint:
        out.append("distance from the fingerprint (band max %.2f)"
                   % (band or 0))
        for sample in dist_rows:
            d = sample["distance"]
            out.append("  %-22s %.2f  %-13s %s"
                       % (sample["basename"][:22], d.get("delta", 0),
                          d.get("verdict", ""), contributor_line(d)))
        out.append("  %d in range, %d near, %d out of range, %d unreliable, "
                   "%d unmeasured"
                   % (dist_counts.get("in_range", 0),
                      dist_counts.get("near", 0),
                      dist_counts.get("out_of_range", 0),
                      dist_counts.get("unreliable", 0),
                      dist_counts.get("unmeasured", 0)))
        out_rows = [s for s in dist_rows
                    if s["distance"].get("verdict") == "out_of_range"]
        mismatch = scale_mismatch(out_rows, fingerprint)
        if mismatch:
            out.append("    -> the band was calibrated on samples of ~%s "
                       "words and these run ~%s: rebuild the fingerprint from "
                       "documents the size of the ones you will scan, because "
                       "a short document is noisier in Delta terms and reads "
                       "far whatever register it is in"
                       % (format(int(mismatch[0]), ","),
                          format(int(mismatch[1]), ",")))
        elif out_rows:
            out.append("    -> %s is a different register, not a broken "
                       "rule: measure it separately with measure_voice.py "
                       "--register <r> and keep a per-register fingerprint"
                       % out_rows[0]["basename"])
        out.append("")

    # Outside the fingerprint gate on purpose. The receipt is per-sample
    # sentence medians and nothing else: it answers "is this one writer or
    # two" from the corpus alone, and a profile with no fingerprint yet is
    # exactly the one that needs the answer before somebody builds one. The
    # `--json` payload has always carried it unconditionally, so gating the
    # text report was also the two output modes disagreeing.
    if shape["per_sample_median"]:
        medians = " ".join("%g" % m for m in shape["per_sample_median"])
        out.append("sentence shape, one register or two")
        if shape["wide"]:
            out.append("  per-sample medians %s (range %g)  the corpus holds "
                       "two sentence registers" % (medians, shape["range"]))
            out.append("    -> split the corpus and measure each half: the "
                       "average of two registers is nobody")
        else:
            out.append("  per-sample medians %s (range %g)  one register"
                       % (medians, shape["range"]))
        out.append("")

    if tells:
        out.append("engine P0 tells over this corpus, for ## Known "
                   "contamination")
        for row in tells:
            line = ("  %-22s %-24s %d time(s) in %d sample(s)"
                    % (row["id"], ('"%s"' % row["match"])[:24],
                       row["times"], len(row["samples"])))
            if row["candidate"]:
                line += "  -> record under ## Known contamination"
            if row["signature_move"]:
                line += ("  [also the subject of signature move %s]"
                         % row["signature_move"])
            out.append(line)
        out.append("")

    if caric_rows:
        out.append("more them than they are")
        for sample, exceeded in caric_rows:
            detail = ", ".join("%s %s %s (%+.1fsd)" % (
                e["measure"], e["direction"], e["value"], e["z"])
                for e in exceeded)
            out.append("  %-22s %s" % (sample["basename"][:22], detail))
        out.append("")

    out.append("Nothing above has been written. Each line is a question for "
               "the author, because a profile is a claim about them and their "
               "own prose disagreeing with it is the disagreement surfacing, "
               "not a bug in the scan. Confirm a line, then change the rules "
               "file by hand.")
    return "\n".join(out)


def main():
    examples = [
        "python3 audit_voice.py john sample1.md sample2.md sample3.md",
        "python3 audit_voice.py voices/dana.rules.json docs/dana/*.md --register formal",
        "python3 audit_voice.py john samples/*.md --json",
    ]
    ap = cli_error.LLMArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        examples=examples)
    ap.add_argument("voice", metavar="VOICE",
                    help="profile name, or a path to any of its files")
    ap.add_argument("samples", nargs="+", metavar="SAMPLE",
                    help="documents this writer actually wrote")
    ap.add_argument("--register", metavar="NAME",
                    choices=sorted(registers_mod.registers()),
                    help="register to scan the samples as (default: the "
                         "scanner's default)")
    ap.add_argument("--json", action="store_true", help="machine-readable")
    ap.add_argument("--voices-dir", default=voices_mod.VOICES_DIR,
                    help=argparse.SUPPRESS)
    args = ap.parse_args()

    rules_path = resolve_voice(args.voice, args.voices_dir)
    if not os.path.isfile(rules_path):
        print(cli_error.format_file_error(
            "audit_voice.py", rules_path, "voice",
            expected_type="voice profile name or rules file path",
            examples=examples), file=sys.stderr)
        return 2
    try:
        rules, raw_child = load_rules_pair(rules_path, args.voices_dir)
    except (voices_mod.VoiceError, OSError, ValueError) as exc:
        print(cli_error.format_llm_error(
            "audit_voice.py", "%s could not be loaded as a voice rules file: "
            "%s" % (rules_path, exc), parser=ap, examples=examples),
            file=sys.stderr)
        return 2

    # Resolved before the fingerprint lookup, and off the same default
    # `scan.py` uses. `path_for(rules_path, None)` skips the register-scoped
    # file, so a profile carrying only `<name>.blog.fingerprint.json` reported
    # "no fingerprint" here while scan.py, scanning the same document as blog,
    # measured against it: the two checkers disagreeing about which
    # fingerprint applies, which is what path_for exists to prevent.
    register = args.register or registers_mod.default_register()

    fingerprint = None
    fingerprint_path = stylometry.path_for(rules_path, register=register)
    if fingerprint_path:
        try:
            fingerprint = stylometry.load(fingerprint_path)
        except (OSError, ValueError) as exc:
            print("audit_voice: %s, so distance and caricature are "
                  "not reported" % exc, file=sys.stderr)
            fingerprint_path = None
    else:
        print("audit_voice: no fingerprint beside %s, so distance and "
              "caricature are not reported"
              % os.path.basename(rules_path), file=sys.stderr)

    texts = []
    for path in args.samples:
        try:
            with open(path, encoding="utf-8") as fh:
                texts.append((path, fh.read()))
        except OSError as exc:
            print(cli_error.format_file_error(
                "audit_voice.py", path, "samples",
                expected_type="readable document path",
                details=str(exc), examples=examples), file=sys.stderr)
            return 2

    scan = load_scan("audit_voice")
    samples = []
    for path, text in texts:
        sample = audit_one(scan, path, text, rules, fingerprint, register)
        sample["path"] = path
        samples.append(sample)

    term_map = ban_term_map(rules, raw_child)
    backs = fire_backs(samples, rules, raw_child, term_map)
    caps = cap_suggestions(samples, rules, scan, register, backs)
    dist_rows, dist_counts = distance_summary(samples)
    shape = shape_receipt(samples, fingerprint)
    tells = known_tells(samples, rules)
    scoped_out = scoped_out_count(rules, register)
    caric_rows = [(s, s["caricature"]["exceeded"]) for s in samples
                  if s["caricature"] and s["caricature"].get("exceeded")]
    exit_code = 1 if backs else 0
    voice_label = voices_mod.strip_rules_suffix(
        os.path.basename(rules_path))

    if args.json:
        payload = {
            "voice": voice_label,
            "rules_path": rules_path,
            "register": register,
            "fingerprint": ({"loaded": True, "path": fingerprint_path,
                             "register": fingerprint.get("register"),
                             "band_max": fingerprint.get("self_distance",
                                                         {}).get("max")}
                            if fingerprint else
                            {"loaded": False,
                             "note": "no fingerprint beside the rules file"}),
            "corpus": {"samples": len(samples),
                       "words": sum(s["words"] for s in samples),
                       "unreliable": sum(1 for s in samples if not s["reliable"])},
            "samples": [{
                "path": s["path"], "basename": s["basename"],
                "words": s["words"], "reliable": s["reliable"],
                "sentence_median": s["sentence_median"],
                "voice_findings": [{"id": f["id"], "label": f.get("label"),
                                    "line": f.get("line"),
                                    "match": f.get("match")}
                                   for f in s["voice"]],
                "p0_findings": [{"id": f["id"], "label": f.get("label"),
                                 "line": f.get("line")} for f in s["p0"]],
                "distance": ({"delta": s["distance"].get("delta"),
                              "verdict": s["distance"].get("verdict"),
                              "reliable": s["distance"].get("reliable"),
                              "contributors": (s["distance"]
                                               .get("contributors", [])[:3])}
                             if s["distance"] else None),
                "caricature": s["caricature"],
            } for s in samples],
            "fire_backs": backs,
            "cap_suggestions": caps,
            "distance_summary": dict(dist_counts),
            "shape": shape,
            "known_tells": tells,
            "exit_code": exit_code,
        }
        print(json.dumps(payload, indent=2, default=str))
    else:
        print(report(voice_label, register, samples, fingerprint,
                     fingerprint_path, scoped_out, backs, caps, dist_rows,
                     dist_counts, shape, tells, caric_rows))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
