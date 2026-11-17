#!/usr/bin/env python3
"""
One finding shape, for every checker in this plugin.

A finding is a dict with exactly these keys:

    id          stable slug. A lexicon pattern id, a voice rule id, or one of
                the synthetic ids in rwlib.lexicon.SYNTHETIC_FINDING_IDS.
    label       one line, for a human, already formatted with any counts.
    band        voice | fingerprint | craft | structure. See BANDS.
    priority    P0 | P1 | P2.
    line        1-indexed line in the file the finding was read from.
    match       the text that triggered it, truncated. Empty, or a short
                stand-in like "3 badges", when the finding is about the whole
                document and no single span caused it.
    excerpt     surrounding text, or the instruction for fixing it. This is the
                second line of a report, and it is where a structural finding
                puts its entire explanation.

Two optional keys, both set by rwlib.suppress and absent otherwise:

    suppressed     the reason an inline `rabbit-allow` comment gave for it.
    suppressed_at  the line that comment is on.

A finding carrying them is reported and does not count. See suppress.py for why
it stays in the list rather than being dropped.

readme_check.py used to spell the last one `detail` and drop `match` entirely,
so its reporter had to branch on the band to decide which key held the text and
no downstream consumer could read both checkers with one parser. That is why
SCHEMA_VERSION exists and why it is emitted in --json: a consumer that pins it
finds out at parse time when the shape moves, rather than by rendering blanks.

SCHEMA_VERSION goes up when a key is removed, renamed, or changes meaning.
Adding an optional key does not move it.

Stdlib only, 3.9+.
"""

SCHEMA_VERSION = 1

# Ordered worst-first, which is also the order every reporter prints them in.
PRIORITIES = ("P0", "P1", "P2")

# Ordered by how much the reader is expected to argue with the finding.
#
#   safety       concealed text, or text addressed to an agent. The one band
#                nobody is meant to argue with, and the only one that is never
#                fixable: it is quarantined and quoted, never rewritten.
#   structure    the shape of the document, measured against the corpus.
#   voice        this writer's own rules. A hit is a defect, not a suggestion.
#   fingerprint  evidence about how the text was produced.
#   craft        general writing problems, never evidence about authorship.
BANDS = ("safety", "structure", "voice", "fingerprint", "craft")

PRIORITY_RANK = {p: i for i, p in enumerate(PRIORITIES)}
BAND_RANK = {b: i for i, b in enumerate(BANDS)}

REQUIRED_KEYS = ("id", "label", "band", "priority", "line", "match", "excerpt")


def make(fid, label, band, priority, line, match="", excerpt=""):
    """A finding, with every key present. Callers that build the dict by hand
    are the ones that used to leave a key out."""
    return {"id": fid, "label": label, "band": band, "priority": priority,
            "line": line, "match": match, "excerpt": excerpt}


def sort_key(f):
    """Worst priority first, then band, then position in the file."""
    return (PRIORITY_RANK.get(f["priority"], len(PRIORITIES)),
            BAND_RANK.get(f["band"], len(BANDS)),
            f["line"])


def counts(findings):
    """The per-priority and per-band tallies both CLIs report.

    A suppressed finding is counted under `suppressed` and nowhere else. It has
    to come out of the priority tallies, because those are what `--check` and
    every summary line read, and leaving it in would make an allowed finding
    fail the build it was allowed for. It gets its own number rather than
    vanishing, because a report that says "0 P0" over a document with three
    allowed P0s in it is the silent suppression rwlib/suppress.py refuses to
    ship.
    """
    out = {p: 0 for p in PRIORITIES}
    out.update({b: 0 for b in BANDS})
    out["suppressed"] = 0
    for f in findings:
        if "suppressed" in f:
            out["suppressed"] += 1
            continue
        if f["priority"] in out:
            out[f["priority"]] += 1
        if f["band"] in out:
            out[f["band"]] += 1
    return out


def validate(findings):
    """[(index, problem)] for findings that do not match the schema.

    Used by the test suites rather than at runtime: a malformed finding should
    fail a build, not a scan a writer is waiting on.
    """
    problems = []
    for i, f in enumerate(findings):
        missing = [k for k in REQUIRED_KEYS if k not in f]
        if missing:
            problems.append((i, "missing keys: %s" % ", ".join(missing)))
            continue
        if f["band"] not in BANDS:
            problems.append((i, "unknown band %r" % f["band"]))
        if f["priority"] not in PRIORITIES:
            problems.append((i, "unknown priority %r" % f["priority"]))
        if not isinstance(f["line"], int) or f["line"] < 1:
            problems.append((i, "line %r is not a 1-indexed line number"
                             % f["line"]))
    return problems
