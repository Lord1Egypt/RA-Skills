#!/usr/bin/env python3
"""
The tolerance matrix, read from registers.json.

One fact, one home. The matrix used to be stated three times: as prose in
references/context.md, as PROFILE_SKIP and PROFILE_RELAX in scan.py, and as a
test that parsed the markdown table to check the first two agreed. That test was
clever and it was a workaround. It broke on table formatting rather than on a
real disagreement, and it could not see a cell that claimed a tolerance nobody
had implemented, which is how `curly-quote` sat in every skip set unable to fire
in any register.

Now scan.py derives its tables from this module, and the markdown table is
rendered from the same data:

    python3 scripts/rwlib/registers.py            # print the table
    python3 scripts/rwlib/registers.py --write    # write it into context.md
    python3 scripts/rwlib/registers.py --check    # exit 1 if the doc has drifted

validate.py runs --check, so editing the table by hand fails the build with the
diff rather than shipping a document that describes a different engine.

Stdlib only, 3.9+.
"""

import json
import os
import re
import sys

try:
    from . import markdown as markdown_mod
    from . import sections as sections_mod
except ImportError:
    # Run as a script, so there is no parent package and the relative imports
    # above cannot resolve. The fix is to put the directory *above* rwlib on
    # the path and import the package properly, not to put rwlib itself there:
    # `import markdown` succeeds and then markdown.py's own `from .artifacts`
    # fails with the same error one level down, which is what --write and
    # --check did for two releases. Nothing caught it because validate.py calls
    # doc_table() through an import and never runs the CLI.
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from rwlib import markdown as markdown_mod
    from rwlib import sections as sections_mod

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
REGISTERS_PATH = os.path.join(SCRIPTS, "registers.json")
CONTEXT_MD = os.path.join(os.path.dirname(SCRIPTS), "references", "context.md")

MATRIX_HEADING = "## Tolerance matrix"
# Where the rendered block stops. The prose under the table explains the modes
# and is written by hand, so the renderer has to know where its own output ends.
MATRIX_END_MARKER = "**Extra strict** means"

MODES = ("strict", "skip", "relaxed", "partial", "extra-strict", "p0-only")

_CACHE = {}


def load(path=REGISTERS_PATH):
    if path not in _CACHE:
        with open(path, encoding="utf-8") as fh:
            _CACHE[path] = json.load(fh)
    return _CACHE[path]


def registers(path=REGISTERS_PATH):
    """The registers --profile accepts, in matrix order.

    Declared, never inferred from the skip table. Inferred, a register whose
    skip set emptied out disappeared from the CLI without a word, and with it
    from the coverage the tests get by iterating the register list. A register
    with nothing to skip and nothing to relax is a legitimate register.
    """
    return tuple(load(path)["registers"])


def spine(path=REGISTERS_PATH):
    """The formality ladder, loosest first. The rest are genre columns.

    A document form maps onto this axis and never onto a third one:
    references/forms/*.md each name one register, and the ones naming a genre
    column do it because that genre carries tolerances no formality band
    captures. Data rather than prose, so `problems` can check it and so the
    split is not a claim some document makes about the matrix.
    """
    return tuple(load(path).get("spine", ()))


def genre_registers(path=REGISTERS_PATH):
    """Every register that is not on the formality spine, in matrix order."""
    on_spine = set(spine(path))
    return tuple(r for r in registers(path) if r not in on_spine)


def default_register(path=REGISTERS_PATH):
    return load(path)["default_register"]


def version(path=REGISTERS_PATH):
    return load(path).get("version")


def _cells(path):
    for rule in load(path)["rules"]:
        for register, cell in rule["cells"].items():
            yield rule, register, cell


def skip_table(path=REGISTERS_PATH):
    """{register: {finding id}} for every cell that suppresses a rule outright.

    `p0-only` lands here with `skip`, because every id it names is P1 or P2 and
    a P0 fingerprint is never suppressed in any register.
    """
    out = {r: set() for r in registers(path)}
    for rule, register, cell in _cells(path):
        if rule["id"] and cell["mode"] in ("skip", "p0-only"):
            out.setdefault(register, set()).add(rule["id"])
    return {r: ids for r, ids in out.items() if ids}


def relax_table(path=REGISTERS_PATH):
    """{register: {finding id: allowance}} for cells that report past a count.

    A relaxed cell with no allowance is a documentation row for a rule with no
    mechanical form, and it is dropped here rather than defaulting to zero: an
    allowance of zero is indistinguishable from strict and would claim an
    implementation that does not exist.
    """
    out = {r: {} for r in registers(path)}
    for rule, register, cell in _cells(path):
        if rule["id"] and cell["mode"] == "relaxed" and "allowance" in cell:
            out.setdefault(register, {})[rule["id"]] = cell["allowance"]
    return {r: ids for r, ids in out.items() if ids}


def vocab_exempt_registers(path=REGISTERS_PATH):
    """{register: extra exemption list name or None} for every partial cell.

    This is what a `partial` cell means, and it is why those registers take no
    hit allowance on the vocabulary rows: an allowance would let a second
    `delve` through, and the named exemption list does not.

    `technical_exempt` is the base for every partial cell and always applies.
    A cell may name one further list with `exempt`, which is added to it, and
    that is how `academic` drops `paradigm` while `technical-blog` keeps
    flagging it. Adding those two words to `technical_exempt` instead would
    have exempted them in a tech blog, where a new paradigm for observability
    is precisely the tier-1 usage the list exists to catch.

    A dict rather than a set, and `scan.py` still asks `profile in ...`, which
    reads the keys. The membership test is the same question it always was.
    """
    out = {}
    for rule, register, cell in _cells(path):
        if cell["mode"] == "partial":
            out.setdefault(register, cell.get("exempt"))
    return out


def _lexicon_lists():
    """Top-level lexicon keys holding a word list, for the `exempt` check.

    Imported here rather than at module scope for the reason `priorities()`
    gives: this module is imported by the lexicon's own consumers and a
    top-level import would close the loop.
    """
    from . import lexicon
    data = lexicon.load(lexicon.LEXICON_PATH)
    return {k for k, v in data.items() if isinstance(v, list)}


def unimplemented_rules(path=REGISTERS_PATH):
    """Labels of rules with no pattern, applied by reading rather than by regex."""
    return [r["label"] for r in load(path)["rules"] if not r["id"]]


# --------------------------------------------------------------------------
# detection
# --------------------------------------------------------------------------

# One regex per structural signal named in references/forms/*.md. Deliberately
# narrow: a greeting or signoff line has to be the whole line, not a phrase
# that happens to appear inside a paragraph, or "Hi there, the incident
# started at 3pm" in the middle of a technical-blog post would read as a
# letter opener.
_GREETING_RX = re.compile(
    r"(?im)^\s*(hi|hello|hey|dear|greetings|good (morning|afternoon|evening))"
    r"(?:\s+[A-Z][\w.'-]*(?:\s+[A-Z][\w.'-]*)?|\s+there|\s+all|\s+team|\s+everyone)?"
    r"\s*[,:]\s*$")
_SIGNOFF_RX = re.compile(
    r"(?im)^\s*(sincerely|regards|best regards|best|thanks|thank you|cheers|"
    r"yours|yours truly|yours sincerely)[,]?\s*$"
)
_HASHTAG_LINE_RX = re.compile(r"(?m)^(?:\s*#\w+\s*){2,}$")
# Which classify_heading categories count as documentation shape. The keyword
# lists behind them live in rwlib.sections, which is the one home for what an
# "installation" heading is: a literal list here drifted from it once already.
_DOCS_CATEGORIES = frozenset({"installation", "usage", "api", "testing",
                              "configuration", "architecture"})

# The registers detect_register() will ever return other than the default.
# Chat and technical-blog were both tried and dropped: neither has a signal
# that is *present* rather than merely plausible-sounding. Chat's only
# candidate, "short, no headings, no greeting," fires on a plain blog blurb
# just as readily -- it is the absence of every other signal, not evidence
# for this one. Technical-blog's candidate, "fenced code plus a number with a
# unit," misfired on 62 of the 100 READMEs in docs/readme-analysis/repos
# (every project with a code block and an install size or version number,
# which is most of them); narrowing the unit list to actual latency/
# throughput units still misfired on 17. A README and a technical writeup
# both legitimately have code and numbers -- the form's real differentiator
# (references/forms/technical-blog.md: the problem stated from the reader's
# own system, a benchmark with methodology, a failed attempt included) is
# prose judgment, not a structural marker. Essay, substack, and generic
# long-form blog prose were never attempted, for the same underlying reason:
# formality is a judgment call. Every register below instead has a marker
# that has to be *present* to fire, verified against the same 100-README
# corpus at zero false positives, which is what keeps this list short.
#
# There is deliberately no DEFAULT_REGISTER constant here. registers.json
# owns that name and default_register() reads it; a literal beside these
# would be a second home for it, and the one that was here said
# "technical-blog" while the file said "blog".
DETECTABLE_REGISTERS = ("academic", "docs", "linkedin", "formal")

# How many distinct IMRaD categories a document's headings must cover before it
# reads as a research paper. Three, and the number is measured rather than
# chosen: against the 100-README corpus, three produces 0 false positives and
# two produces one, a README carrying "Test Results" and "Limitations". Against
# the 19-paper corpus's real JATS section titles (not the extracted files, whose
# headings this repository's own pipeline wrote), three catches 17 and two
# catches 18.
#
# So one paper in ten is missed, and the two it misses are worth naming: a CS
# paper using Method and Experiments, and a humanities paper whose middle
# sections are named after its argument. Both fall through to the default
# register, which is what an unclassified document has always done. Trading
# them for a stranger's README misclassified as a paper is the trade every
# other entry in this list already made.
IMRAD_HEADINGS_REQUIRED = 3


def detect_register(text, path=None, registers_path=REGISTERS_PATH):
    """Guess a register from structural signals, or fall back to the default.

    references/forms/*.md already documents, for a human, which structural
    shape routes to which register. This reads the same short list of strong,
    unambiguous signals mechanically: a run of docs-shaped headings, as
    rwlib.sections classifies them, for docs (skipped for a file named
    README.*, which routes to the separate rabbit-readme-improver skill instead), a
    trailing hashtag line for linkedin, and a greeting-then-signoff shape for
    formal (covers both the email and letter forms, which route to the same
    register).

    Every other form -- chat, technical-blog, essay, substack, plain
    long-form prose -- has no structural tell that survives contact with a
    false positive (see DETECTABLE_REGISTERS for what was tried and why it
    was dropped), so it is left undetected on purpose and falls through to
    the default register, exactly as an unclassified document does today.

    Returns (register, confidence, signals). confidence is "detected" when a
    register-specific rule fired and "default" when nothing did; signals is
    the list of checks that matched, for a caller to report as a note.
    """
    known = set(registers(registers_path))
    stripped_lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    prose_words = len(markdown_mod.strip_for_stats(text).split())
    has_fence = bool(markdown_mod.FENCE_RX.search(text))
    headings = [m.group(2).strip()
                for m in markdown_mod.HEADING_RX.finditer(text)]

    # Academic first, because its bar is the highest of the four: three distinct
    # IMRaD categories present, against two docs-shaped headings. A paper that
    # also happens to carry an Installation section is still a paper.
    if "academic" in known:
        imrad = sections_mod.imrad_categories(headings)
        if len(imrad) >= IMRAD_HEADINGS_REQUIRED:
            return ("academic", "detected",
                    ["IMRaD sections: %s" % ", ".join(sorted(imrad))])

    if "docs" in known:
        doc_hits = sum(1 for h in headings
                       if sections_mod.classify_heading(h) in _DOCS_CATEGORIES)
        is_readme = path is not None and os.path.basename(path).lower().startswith("readme.")
        if doc_hits >= 2 and not is_readme:
            return ("docs", "detected", ["%d docs-shaped headings" % doc_hits])

    if "linkedin" in known and 50 <= prose_words <= 350:
        tail = "\n".join(stripped_lines[-2:])
        if _HASHTAG_LINE_RX.search(tail):
            return ("linkedin", "detected",
                    ["%d words" % prose_words, "hashtag line near the end"])

    if "formal" in known:
        greeting = any(_GREETING_RX.match(ln) for ln in stripped_lines[:5])
        signoff = any(_SIGNOFF_RX.match(ln) for ln in stripped_lines[-3:])
        if greeting and signoff and not has_fence and not headings:
            return ("formal", "detected",
                    ["greeting near the top", "signoff near the end"])

    return (default_register(registers_path), "default", [])


def priorities(lexicon_path=None):
    """{finding id: worst priority it can be raised at}.

    Catalogue patterns carry their own, the engine's own findings are listed in
    lexicon.SYNTHETIC_PRIORITIES, and the two id spaces do not overlap.

    The argument names the *lexicon*, unlike every other `path` in this module.
    Spelled out, because it read as the registers path and would have loaded
    registers.json as a catalogue: no `patterns` key, no error, and every
    catalogue priority silently missing from the answer.
    """
    from . import lexicon
    out = dict(lexicon.SYNTHETIC_PRIORITIES)
    for pattern in lexicon.load(lexicon_path or lexicon.LEXICON_PATH).get("patterns", []):
        if pattern.get("id") and pattern.get("priority"):
            out[pattern["id"]] = pattern["priority"]
    # The ste ids join the same answer, lazily for the same import-shape
    # reason as the lexicon import above. Without them the p0-only cell
    # check in problems() has no priority for an ste id and a p0-only cell
    # on one (all P1/P2, so a disguised full skip) read as fine.
    from . import ste
    out.update(ste.STE_PRIORITIES)
    return out


def problems(known_ids, path=REGISTERS_PATH, id_priorities=None):
    """Everything wrong with the matrix, as messages. Run by validate.py.

    `known_ids` is every finding id the engine can raise. A cell naming an id
    outside it is a silent no-op: the register quietly stops honouring a
    tolerance it claims in the docs, and the only symptom is a finding somebody
    eventually learns to ignore.

    `id_priorities` defaults to reading the lexicon, and exists as an argument
    so a test can hand in a matrix that does not match the shipped catalogue.
    """
    data = load(path)
    if id_priorities is None:
        id_priorities = priorities()
    known_registers = set(data["registers"])
    out = []
    if data["default_register"] not in known_registers:
        out.append("default_register %r is not in registers"
                   % data["default_register"])
    # A spine entry naming nothing is the same silent no-op as a cell naming an
    # id the engine cannot raise: the docs describe a formality ladder, a form
    # file routes onto it, and the rung is not there.
    for name in data.get("spine", ()):
        if name not in known_registers:
            out.append("spine names %r, which is not a register in %r"
                       % (name, data["registers"]))
    seen_labels = set()
    for rule in data["rules"]:
        label = rule["label"]
        if label in seen_labels:
            out.append("duplicate rule label %r" % label)
        seen_labels.add(label)
        if rule["id"] and rule["id"] not in known_ids:
            out.append("rule %r names id %r, which is not a lexicon pattern id "
                       "or a built-in finding id" % (label, rule["id"]))
        for register, cell in rule["cells"].items():
            where = "%s x %s" % (register, label)
            if register not in known_registers:
                out.append("%s is not a register in %r"
                           % (where, data["registers"]))
            mode = cell.get("mode")
            if mode not in MODES:
                out.append("%s has unknown mode %r" % (where, mode))
                continue
            if mode == "strict":
                out.append("%s says strict, which is the default. Delete the "
                           "cell rather than restating it" % where)
            if mode == "relaxed" and "allowance" in cell and not rule["id"]:
                out.append("%s carries an allowance but the rule has no id, so "
                           "nothing can honour it" % where)
            if mode == "relaxed" and "allowance" not in cell and rule["id"]:
                out.append("%s says relaxed and the rule has an id, but no "
                           "allowance implements it" % where)
            if mode == "partial" and rule["id"] not in data["vocabulary_rules"]:
                out.append("%s says partial, which only means something for a "
                           "vocabulary rule (%s)"
                           % (where, ", ".join(data["vocabulary_rules"])))
            if mode != "partial" and "exempt" in cell:
                out.append("%s names an exempt list but is not partial, so "
                           "nothing reads it" % where)
            if mode == "partial" and cell.get("exempt"):
                # A named list nothing defines is a register that silently
                # keeps flagging the words its cell claims to exempt.
                if cell["exempt"] not in _lexicon_lists():
                    out.append("%s names exempt list %r, which lexicon.json "
                               "does not carry" % (where, cell["exempt"]))
                elif cell["exempt"] == "technical_exempt":
                    out.append("%s names technical_exempt, which every partial "
                               "cell already gets. Drop the key rather than "
                               "restating the default" % where)
            # skip_table folds p0-only in with skip, on the stated grounds that
            # every id it names is P1 or P2. Nothing used to check that, so a
            # p0-only cell on a P0 id would have read in the docs as "the P0s
            # still fire here" and behaved as a full suppression of a
            # credibility killer.
            if mode == "p0-only" and id_priorities.get(rule["id"]) == "P0":
                out.append("%s says p0-only, but %r is itself a P0. That cell "
                           "suppresses the finding outright, which is the "
                           "opposite of what it says" % (where, rule["id"]))

    # One register cannot want two different exemption lists: scan.py resolves
    # one per profile, so a second would apply to some vocabulary rules and not
    # others with nothing saying which. Outside the cell loop on purpose: it is
    # a fact about a register rather than about a cell.
    per_register = {}
    for rule, register, cell in _cells(path):
        if cell["mode"] == "partial":
            per_register.setdefault(register, set()).add(cell.get("exempt"))
    for register, names in sorted(per_register.items()):
        if len(names) > 1:
            out.append("register %r names %d different exempt lists across its "
                       "partial cells (%s). scan.py resolves one per profile"
                       % (register, len(names),
                          ", ".join(sorted(str(n) for n in names))))

    relaxed = relax_table(path)
    for register, ids in skip_table(path).items():
        overlap = sorted(ids & set(relaxed.get(register, {})))
        if overlap:
            out.append("register %r both skips and relaxes %s; skip wins, so "
                       "the allowance never applies" % (register, ", ".join(overlap)))
    return out


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------

def _cell_text(cell):
    mode = cell["mode"]
    if mode == "strict":
        return "strict"
    if mode == "skip":
        return "skip"
    if mode == "p0-only":
        return "P0 only"
    if mode == "extra-strict":
        return "**extra strict**"
    if mode == "partial":
        return "**partial**, see below"
    note = cell.get("note")
    return "relaxed (%s)" % note if note else "relaxed"


def render_table(path=REGISTERS_PATH):
    """The markdown table, exactly as it appears in references/context.md."""
    regs = registers(path)
    lines = ["| Rule | %s |" % " | ".join(regs),
             "|---|%s" % ("---|" * len(regs))]
    for rule in load(path)["rules"]:
        cells = [_cell_text(rule["cells"].get(r, {"mode": "strict"}))
                 for r in regs]
        lines.append("| %s | %s |" % (rule["label"], " | ".join(cells)))
    return "\n".join(lines)


def _split_doc(text):
    """(head, body, tail, table) around the rendered table in context.md."""
    head, sep, rest = text.partition(MATRIX_HEADING)
    if not sep:
        raise ValueError("%s has no %r section" % (CONTEXT_MD, MATRIX_HEADING))
    body, end_sep, tail = rest.partition(MATRIX_END_MARKER)
    if not end_sep:
        raise ValueError("%s: no %r line to stop at" % (CONTEXT_MD, MATRIX_END_MARKER))
    table_lines = [ln for ln in body.splitlines() if ln.startswith("|")]
    if not table_lines:
        raise ValueError("%s: no table under %r" % (CONTEXT_MD, MATRIX_HEADING))
    return head + sep, body, end_sep + tail, "\n".join(table_lines)


def doc_table(doc_path=CONTEXT_MD):
    with open(doc_path, encoding="utf-8") as fh:
        return _split_doc(fh.read())[3]


def write_doc(doc_path=CONTEXT_MD, path=REGISTERS_PATH):
    with open(doc_path, encoding="utf-8") as fh:
        text = fh.read()
    head, body, tail, current = _split_doc(text)
    new = render_table(path)
    if current == new:
        return False
    lines = body.splitlines(True)
    table_indices = [i for i, ln in enumerate(lines) if ln.lstrip().startswith("|")]
    if table_indices:
        start_idx = table_indices[0]
        end_idx = table_indices[-1] + 1
        new_body = "".join(lines[:start_idx]) + new + "\n" + "".join(lines[end_idx:])
    else:
        new_body = body.replace(current, new)
    with open(doc_path, "w", encoding="utf-8") as fh:
        fh.write(head + new_body + tail)
    return True


def main(argv):
    examples = [
        "python3 rwlib/registers.py",
        "python3 rwlib/registers.py --check",
        "python3 rwlib/registers.py --write"
    ]
    try:
        from .cli_error import LLMArgumentParser
    except ImportError:
        from cli_error import LLMArgumentParser

    ap = LLMArgumentParser(
        prog="registers.py",
        description="Tolerance matrix inspector and references/context.md documentation updater.",
        examples=examples
    )
    ap.add_argument("--write", action="store_true", help="update references/context.md table from registers.json")
    ap.add_argument("--check", action="store_true", help="verify references/context.md table matches registers.json")
    args = ap.parse_args(argv)

    if args.write and args.check:
        print("error: --write and --check are mutually exclusive", file=sys.stderr)
        return 2

    if args.write:
        changed = write_doc()
        print("context.md updated" if changed else "context.md already current")
        return 0
    if args.check:
        if doc_table() == render_table():
            print("tolerance matrix in context.md matches registers.json")
            return 0
        print("references/context.md's tolerance matrix has drifted from "
              "registers.json. Run: python3 %s --write"
              % os.path.relpath(__file__), file=sys.stderr)
        return 1
    print(render_table())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
