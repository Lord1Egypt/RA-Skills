#!/usr/bin/env python3
"""
verify.py - preservation validator for a rewrite.

SKILL.md promises the editor will not touch code blocks, frontmatter, tables,
block quotes, inline code, URLs, file paths, or heading structure, and will not
add em dashes or leave a draft with more tells than it started with. Edit mode
writes to files, so a broken promise there is silent and destructive. This is
what checks them.

Two of those checks are narrower than the promise, and those narrowings are
measured rather than assumed. A file path is tracked only when it carries an
extension, for the reason spelled out at PATH_RX. Headings are ATX-only (`# Title`),
matching `rwlib.markdown.HEADING_RX`.

Image *sources* are checked, as of the pass that measured them. They used to be
covered only incidentally, by URL_RX when the src is absolute and by PATH_RX
when it is relative and carries an extension, so a relative extensionless src
was unprotected. See uncovered_image_srcs: over the 100-README corpus the gap
held 0 of 341 markdown images and 3 HTML ones, which is what made closing it
obviously worth doing.

Image *alt text* is still not covered, and that is now a decision with a number
under it rather than a note. Over the same corpus: 337 images carry alt text,
7,282 characters of it, containing 0 lexicon tells and 18 prose dashes. The 18
cost nothing today, because both counters compare a before to an after and an
editor that leaves alt text alone moves neither. What protecting it verbatim
*would* cost is the legitimate edit: alt text in this corpus is overwhelmingly
badge labels, and "PyPI" becoming "PyPI version" is a fix, not a violation.
SKILL.md's guardrails never promised alt text was untouchable, so requiring it
here would be this file inventing a promise the skill does not make. Everything
else on the list is checked in full.

Usage:
    python3 verify.py original.md rewritten.md
    python3 verify.py original.md rewritten.md --json
    python3 verify.py original.md converted.md --allow-structure

Exit codes: 0 clean, 1 a violation, 2 a usage or IO error.

Heading structure is inviolable by default, which is right for `deslop` and
wrong for `voice`: a conversion reorders sections and rewrites headings because
the profile told it to. `--allow-structure` moves those two checks into a
reported `structure_changes` list instead of failing. Nothing else moves with
them, and the default is unchanged.

Carve-outs, because the skill instructs these edits:
  - a heading whose text changed only in capitalization (Title Case fix)
  - a URL that lost only an AI tracking parameter
  - an en dash between digits, which is a numeric range and not a splice
  - a tell or a dash inside a span the skill already promises not to touch:
    code, tables, block quotes, frontmatter, and quoted examples
"""

import argparse
from collections import Counter
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# See scan.py: rwlib sits beside this file and is not on anybody's PYTHONPATH.
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from rwlib import cli_error                                      # noqa: E402
from rwlib import facts                                               # noqa: E402
from rwlib import lexicon as lexicon_mod                              # noqa: E402
from rwlib import registers as registers_mod                          # noqa: E402
from rwlib import voices as voices_mod                                # noqa: E402
from rwlib.artifacts import norm_url                                  # noqa: E402
# QUOTED_RX is a re-export, not a caller: test_verify.py asserts it is the
# same object scan.py holds. See the note in scan.py.
from rwlib.markdown import (BLOCKQUOTE_RX, FENCE_RX, FRONTMATTER_RX,  # noqa: E402,F401
                            HEADING_RX, HTML_IMG_RX,
                            HTML_TAG_RX, IMAGE_RX, INLINE_CODE_RX, PATH_RX,
                            PROSE_DASH_RX, QUOTED_RX, TABLE_ROW_RX, URL_RX,
                            apply_exemptions, blank, blank_entities, context)

LEXICON_PATH = lexicon_mod.LEXICON_PATH

# Used only when the lexicon cannot be read. Kept deliberately short: it is a
# floor, not a copy of the lexicon.
FALLBACK_TELL_RX = [
    re.compile(r"(?i)\b(delve|tapestry|nestled|showcasing|testament to|"
               r"meticulous|seamless|robust|cutting-edge|pivotal|"
               r"underscores|game-changer|vibrant|bustling|ever-evolving)\b"),
    re.compile(r"(?i)(i hope this helps|great question|let's dive in|"
               r"in conclusion|the future looks bright|it's worth noting|"
               r"experts believe|studies show)"),
    re.compile(r"(?i)(it'?s not (just )?[^.;!?\n]{2,50}[,;] it'?s)"),
]


def load_tell_regexes():
    """Count tells against lexicon.json rather than against a copy of it."""
    try:
        lex = lexicon_mod.load()
    except (OSError, ValueError):
        return [(rx, False) for rx in FALLBACK_TELL_RX]
    out = [(lexicon_mod.word_regex(lex["tier1"]), False),
           (lexicon_mod.phrase_regex(lex["tier1_phrases"]), False)]
    for p in lex["patterns"]:
        if p.get("band") != "fingerprint" or p.get("priority") == "P2":
            continue
        try:
            out.append((re.compile(p["rx"]), bool(p.get("scan_raw"))))
        except (re.error, KeyError):
            continue
    return out


TELL_RX = load_tell_regexes()


def _blank_group(match, group=1):
    """The whole match with one group blanked, same length as it started.

    `blank` takes out the whole span, which is wrong when only part of it is
    the thing to hide. Written against the match's own offsets so the rest of
    the span, whatever it holds, comes through byte for byte.
    """
    start, end = match.span(group)
    if start < 0:
        return match.group(0)
    base = match.start()
    whole = match.group(0)
    return (whole[:start - base] + " " * (end - start) + whole[end - base:])


def extract(text):
    # Fences and inline code are compared verbatim and so are read from the raw
    # text. Everything structural is read from a copy with the fences blanked:
    # `# build the image` inside a bash fence is a shell comment, not a heading,
    # and a piped line inside a fence is not a table row. Without this, moving a
    # code block that contains shell comments changes the heading count and
    # fails a conversion that touched no headings at all.
    prose = FRONTMATTER_RX.sub(blank, text)
    prose = FENCE_RX.sub(blank, prose)
    # A URL carries slashes and a dotted final segment, so PATH_RX matches
    # inside one (.../main/README.md). Left in, an edited URL is reported twice,
    # and the utm-stripping carve-out norm_url grants does not reach the second
    # report.
    #
    # Inline code goes with it, for the same reason and with the same fix. Most
    # paths in a document are written as `scripts/scan.py`, and inline code is
    # compared verbatim two checks above, which is a stricter promise than the
    # path check makes. Left in, one edit to one span reported both "inline code
    # altered" and "file path altered", and a reader counting violations saw two
    # broken promises where there was one.
    #
    # Image alt text goes too, and the module docstring above says why with a
    # number. Blanked in place rather than rebuilt from the groups: an image
    # may carry a title (`![alt](src "title")`), and reconstructing the match
    # as `![](src)` silently drops it and shortens the string, which is the one
    # thing every blanking helper in rwlib.markdown promises not to do.
    no_alt = IMAGE_RX.sub(_blank_group, prose)
    unlinked = INLINE_CODE_RX.sub(blank, URL_RX.sub(blank, no_alt))
    # Tables, block quotes and frontmatter go the same way, and for the third
    # time the same argument: each is compared verbatim below, so a path inside
    # one is already a promise this function keeps. Left in, an edited path in a
    # table row reported "table row altered" and "file path altered", which is
    # one edit and two violations. Measured over the 100-README corpus, blanking
    # them takes 2,275 raw path tokens down to 1,617 prose ones, so 29% of every
    # path in a README sits somewhere this check does not have to look.
    #
    # HTML tags deliberately stay in for this pass, though the fact pass below
    # takes them out. uncovered_image_srcs skips any src PATH_RX matches, so
    # blanking tags here would open exactly the gap that function exists to
    # close: a relative `<img src="assets/logo.svg">` would be reported by
    # neither.
    #
    # Headings deliberately stay in, for the reason the argument above does not
    # reach: `--allow-structure` moves the heading comparison to a reported list
    # rather than a violation, so a heading is the one span here that is not
    # always compared verbatim. Blanked, `## 10x faster` becoming `## 100x
    # faster` under that flag was neither a structure failure nor a fact one.
    unquoted = TABLE_ROW_RX.sub(
        blank, BLOCKQUOTE_RX.sub(blank, FRONTMATTER_RX.sub(blank, unlinked)))
    # The facts are read from a copy with every span that is already compared
    # verbatim taken out of it, which is the argument extract() already makes
    # for keeping PATH_RX out of URLs: a number inside a table is one broken
    # promise, and reporting it twice shows a reader two problems where there
    # is one. Measured over the 100-README corpus, that blanking takes 13,098
    # raw numeric tokens down to 6,028 prose ones, so more than half of every
    # number in a README is somewhere this check does not have to look.
    #
    # Entities are blanked too, the same as the voice check's semicolon counter
    # does and for the same reason: `&#8203;` is markup, and the 8203 in it is
    # not a number a reader reads. Stripping a zero-width space is an instructed
    # fix, and without this the fixer's own output failed verification with "the
    # number 8203 was removed".
    #
    # HTML tags go with them, and that one came off the corpus. An attribute
    # value is double-quoted, so `alt="Claude Code running with Free Claude
    # Code"` read as somebody's quotation and `style="width: 60%"` read as a
    # percentage. 55 of the 100 corpus READMEs carried at least one. Alt text is
    # already documented above as prose an editor may legitimately improve, so
    # protecting it verbatim here would contradict the decision this file
    # already made.
    fact_text = blank_entities(HTML_TAG_RX.sub(blank, unquoted))
    fm_match = FRONTMATTER_RX.search(text)
    return {
        # finditer, not findall: both patterns capture their own delimiter for
        # a backreference (the closing fence has to be at least as long as the
        # opener, the closing backtick run has to match the opener's), and
        # findall would return that group instead of the whole span.
        "fences": [m.group(0) for m in FENCE_RX.finditer(text)],
        "inline_code": [m.group(0) for m in INLINE_CODE_RX.finditer(text)],
        "frontmatter": fm_match.group(1) if fm_match else None,
        "tables": TABLE_ROW_RX.findall(prose),
        "blockquotes": BLOCKQUOTE_RX.findall(prose),
        "headings": HEADING_RX.findall(prose),
        "urls": URL_RX.findall(text),
        "paths": PATH_RX.findall(unquoted),
        "image_srcs": uncovered_image_srcs(prose),
        "numbers": [canon for canon, _ in facts.numbers(fact_text)],
        "dates": [iso for iso, _ in facts.dates(fact_text)],
        "quotes": facts.quoted(fact_text),
        # Report-only, forever. See facts.entities: a capitalized-run regex
        # cannot tell a product name from the first word of a sentence, and
        # set-equality on it would fail every rewrite that splits a sentence at
        # a capital. It never reaches `ok`.
        "entities": facts.entities(fact_text),
    }


def uncovered_image_srcs(text):
    """Image sources that neither the URL check nor the path check would catch.

    An image's src was covered incidentally: by URL_RX when it is absolute, and
    by PATH_RX when it is relative and carries an extension. A relative
    extensionless src, `<img src="assets/logo">`, fell through both, and an edit
    could retarget it with nothing reported.

    Only the leftovers are returned, for the reason spelled out at PATH_RX's
    exclusion in extract(): a src reported by two checks is one broken promise
    counted twice, and a reader tallying violations sees two problems where
    there is one.

    Measured before it was closed, over the 100-README corpus in
    docs/readme-analysis: 341 markdown images, 300 absolute, 41 relative with an
    extension, and none in this bucket. The HTML `<img>` half held 3. So the fix
    is close to free, which is the argument for making it rather than the
    argument against: nothing legitimate is going to trip it.
    """
    out = []
    for src in ([m.group(2) for m in IMAGE_RX.finditer(text)]
                + HTML_IMG_RX.findall(text)):
        if URL_RX.match(src) or PATH_RX.search(src):
            continue
        out.append(src)
    return out


def tell_hits(text):
    """Every lexicon tell in the prose, as matched strings. Returned rather than
    counted so a failure can name what got added instead of only how many."""
    prose = apply_exemptions(text)
    hits = []
    for rx, scan_raw in TELL_RX:
        target = text if scan_raw else prose
        hits.extend(m.group(0).strip() for m in rx.finditer(target))
    return hits


def dash_hits(text):
    """Prose em and en dashes, each with its surrounding text."""
    prose = apply_exemptions(text)
    return [context(prose, m.start(), m.end())
            for m in PROSE_DASH_RX.finditer(prose)]


def count_tells(text):
    return len(tell_hits(text))


def multiset_lost(before, after):
    """Items present in `before` that are missing from `after`, counting duplicates."""
    counts = Counter(after)
    lost = []
    for item in before:
        if counts[item] > 0:
            counts[item] -= 1
        else:
            lost.append(item)
    return lost


def fact_delta(a, b):
    """Both directions, per fact class, plus the report-only entity list.

    Both directions because a number that changed *value* is one lost and one
    added, and printing the pair is what turns "a number went missing" into
    "3200 became 3000". A reader given only the loss has to go find the other
    half themselves.

    Only the loss is a violation, and the asymmetry is a decision rather than an
    oversight. Guardrail 1 forbids inventing facts, which makes an added number
    look like one, and in practice a rewrite that turns "the last two years"
    into "2024 and 2025" is deriving a number the source already carried.
    Reported, never failed.
    """
    out = {}
    for key in ("numbers", "dates", "quotes", "entities"):
        out["%s_before" % key] = len(a[key])
        out["%s_after" % key] = len(b[key])
        out["%s_lost" % key] = multiset_lost(a[key], b[key])
        out["%s_added" % key] = multiset_lost(b[key], a[key])
    return out


def validate(original, rewritten, allow_structure=False, allow_facts=False,
             allow_dashes=False):
    a, b = extract(original), extract(rewritten)
    violations = []
    structure_changes = []
    fact_changes = []

    def check(key, name):
        lost = multiset_lost(a[key], b[key])
        for item in lost[:5]:
            snippet = re.sub(r"\s+", " ", str(item))[:110]
            violations.append({"kind": name, "detail": snippet})
        if len(lost) > 5:
            violations.append({"kind": name,
                               "detail": "... and %d more" % (len(lost) - 5)})

    check("fences", "code block altered or removed")
    check("inline_code", "inline code altered or removed")
    check("tables", "table row altered or removed")
    check("blockquotes", "block quote altered or removed")
    check("paths", "file path altered or removed")
    check("image_srcs", "image source altered or removed")

    if a["frontmatter"] != b["frontmatter"]:
        violations.append({"kind": "frontmatter altered", "detail": ""})

    # URLs: losing an AI tracking parameter is instructed; anything else is not.
    a_urls = [norm_url(u) for u in a["urls"]]
    b_urls = [norm_url(u) for u in b["urls"]]
    for u in multiset_lost(a_urls, b_urls)[:5]:
        violations.append({"kind": "URL altered or removed", "detail": u[:110]})

    # Headings: a case-only change is the instructed Title Case fix.
    #
    # Compared as a multiset, like every other preservation check. Membership
    # alone hides the duplicate case: a document with two `## Notes` that loses
    # one of them and gains a different heading keeps both the membership test
    # and the count test happy, and a section disappears with nothing reported.
    #
    # A voice conversion reorders sections and rewrites headings on purpose, so
    # --allow-structure downgrades these two to a reported list. It scopes to
    # headings and nothing else: code, tables, quotes, URLs, and the em-dash and
    # tell counters stay hard in both modes. Without the flag a conversion fails
    # its own verification, which is how "restructure freely" turns back into a
    # word swap.
    heading_bucket = structure_changes if allow_structure else violations
    unmatched = [(lvl, txt.lower()) for lvl, txt in b["headings"]]
    for lvl, txt in a["headings"]:
        key = (lvl, txt.lower())
        if key in unmatched:
            unmatched.remove(key)
        else:
            heading_bucket.append({"kind": "heading changed or removed",
                                   "detail": "%s %s" % (lvl, txt)})
    if len(a["headings"]) != len(b["headings"]):
        heading_bucket.append({
            "kind": "heading count changed",
            "detail": "%d -> %d" % (len(a["headings"]), len(b["headings"])),
        })

    # Em dashes must not be added, unless explicitly allowed by the active voice
    # profile or --allow-dashes. Both counters diff the actual hits rather than
    # the totals, so a report names the span that moved the number.
    dash_bucket = structure_changes if allow_dashes else violations
    a_dash, b_dash = dash_hits(original), dash_hits(rewritten)
    a_em, b_em = len(a_dash), len(b_dash)
    if b_em > a_em:
        added = multiset_lost(b_dash, a_dash)
        dash_bucket.append({"kind": "em dashes added",
                            "detail": "%d -> %d: %s"
                                      % (a_em, b_em, " | ".join(added[:3]))})

    # A rewrite must not end with more tells than it started with.
    a_tells, b_tells = tell_hits(original), tell_hits(rewritten)
    a_t, b_t = len(a_tells), len(b_tells)
    if b_t > a_t:
        added = multiset_lost(b_tells, a_tells)
        violations.append({"kind": "more tells after rewrite",
                           "detail": "%d -> %d: %s"
                                     % (a_t, b_t, ", ".join(added[:5]))})

    # Facts. Guardrail 1 says never invent a number, a date or a quote, and
    # until this it was prose in SKILL.md with nothing behind it: every check
    # above proves the rewrite did not touch a code fence, and none of them
    # noticed the sentence that turned 3,200 into 3,000.
    #
    # `--allow-facts` is the mirror of `--allow-structure`, and it exists for
    # the same kind of profile: rwlib/facts.py canonicalizes a date so a
    # `date_format` conversion passes, and it deliberately does not match a
    # spelled number against a digit, so a profile that requires one or the
    # other has an edit this cannot model. Default is hard, like everything
    # else here.
    facts_report = fact_delta(a, b)
    fact_bucket = fact_changes if allow_facts else violations
    for key, noun in (("numbers", "number"), ("dates", "date"),
                      ("quotes", "quotation")):
        lost = facts_report["%s_lost" % key]
        added = facts_report["%s_added" % key]
        for i, item in enumerate(lost[:5]):
            # The other half of the pair, positionally, when there is one. A
            # number that changed value shows up as one lost and one added, and
            # naming both is the difference between "a number went missing" and
            # "3200 became 3000".
            became = (" (%s appeared)" % added[i]) if i < len(added) else ""
            fact_bucket.append({
                "kind": "%s altered or removed" % noun,
                "detail": (re.sub(r"\s+", " ", str(item))[:90] + became)})
        if len(lost) > 5:
            fact_bucket.append({"kind": "%s altered or removed" % noun,
                                "detail": "... and %d more" % (len(lost) - 5)})

    return {
        "ok": not violations,
        "violations": violations,
        "structure_changes": structure_changes,
        "fact_changes": fact_changes,
        "facts": facts_report,
        "tells_before": a_t,
        "tells_after": b_t,
        "em_dashes_before": a_em,
        "em_dashes_after": b_em,
    }


def main():
    examples = [
        "python3 verify.py original.md rewritten.md",
        "python3 verify.py original.md rewritten.md --json",
        "python3 verify.py original.md converted.md --allow-structure",
        "python3 verify.py original.md converted.md --voice john"
    ]
    ap = cli_error.LLMArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        examples=examples
    )
    ap.add_argument("original", help="path to original unedited markdown file")
    ap.add_argument("rewritten", help="path to rewritten markdown file to verify against original")
    ap.add_argument("--version", action="version",
                    version="verify.py (lexicon v%s, registers v%s)"
                            % (lexicon_mod.version(), registers_mod.version()))
    ap.add_argument("--json", action="store_true", help="output machine-readable JSON result")
    ap.add_argument("--allow-structure", action="store_true",
                    help="report heading changes instead of failing on them. For a "
                         "voice conversion, which reorders sections by design. Every "
                         "other preservation check still applies")
    ap.add_argument("--allow-facts", action="store_true",
                    help="report a lost number, date or quotation instead of failing "
                         "on it. Dates already compare as their ISO form and a range "
                         "as one token, so a reformat passes without this. It is for "
                         "a profile that spells numbers out, which no regex can model")
    ap.add_argument("--allow-dashes", action="store_true",
                    help="report added em dashes under structure changes instead of "
                         "failing on them. For a voice profile (like john) that uses "
                         "em dashes authentically")
    vg = ap.add_mutually_exclusive_group()
    vg.add_argument("--voice", help="voice profile name (e.g. john). If the profile allows em dashes, enables dash allowance")
    vg.add_argument("--voice-rules", help="path to custom voice rules JSON file")
    args = ap.parse_args()

    try:
        with open(args.original, encoding="utf-8-sig") as fh:
            original = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        print(cli_error.format_file_error(
            "verify.py", args.original, "original", expected_type="file path",
            details=str(exc), examples=examples
        ), file=sys.stderr)
        return 2

    try:
        with open(args.rewritten, encoding="utf-8-sig") as fh:
            rewritten = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        print(cli_error.format_file_error(
            "verify.py", args.rewritten, "rewritten", expected_type="file path",
            details=str(exc), examples=examples
        ), file=sys.stderr)
        return 2

    allow_dashes = args.allow_dashes
    if not allow_dashes and (args.voice or args.voice_rules):
        # Named explicitly (there is no --voice auto here), so a bad path or
        # unparseable rules file exits 2 rather than silently leaving em
        # dashes disallowed: the repo's convention (see scan.py's own
        # --voice-rules handling) is that a profile asked for by name and
        # not readable is a false pass, not a clean report.
        rules_path = (args.voice_rules if args.voice_rules else
                     os.path.join(voices_mod.VOICES_DIR,
                                  args.voice + voices_mod.RULES_SUFFIX))
        try:
            vr = voices_mod.load(rules_path)
        except voices_mod.VoiceError as exc:
            print(cli_error.format_file_error(
                "verify.py", rules_path, "--voice-rules / --voice",
                expected_type="voice rules file path (.rules.json)",
                details=str(exc), examples=examples), file=sys.stderr)
            return 2
        if vr.get("mechanics", {}).get("em_dash") == "allow":
            allow_dashes = True

    result = validate(original, rewritten, allow_structure=args.allow_structure,
                      allow_facts=args.allow_facts, allow_dashes=allow_dashes)

    if args.json:
        print(json.dumps(result, indent=2))
    elif result["ok"]:
        f = result["facts"]
        print("preservation OK  |  tells %d -> %d  |  em dashes %d -> %d\n"
              "                 |  %d numbers, %d dates, %d quotations preserved"
              % (result["tells_before"], result["tells_after"],
                 result["em_dashes_before"], result["em_dashes_after"],
                 f["numbers_after"], f["dates_after"], f["quotes_after"]))
        for c in result["fact_changes"]:
            print("  fact       %-28s %s" % (c["kind"], c["detail"]))
        # Never a violation, and printed only when it moved. A capitalized-run
        # regex cannot tell a product name from the first word of a sentence,
        # so this is a list a person reads and not a verdict.
        for direction in ("lost", "added"):
            names = f["entities_%s" % direction]
            if names:
                print("  entities %-5s %s" % (direction, ", ".join(names[:8])))
        for c in result["structure_changes"]:
            print("  structure  %-28s %s" % (c["kind"], c["detail"]))
    else:
        print("preservation FAILED (%d violation(s))" % len(result["violations"]))
        for v in result["violations"]:
            print("  %-32s %s" % (v["kind"], v["detail"]))
        print("\nThe rewrite touched something SKILL.md promises to leave alone, "
              "or moved a counter the wrong way. Restore those spans and re-run.")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
