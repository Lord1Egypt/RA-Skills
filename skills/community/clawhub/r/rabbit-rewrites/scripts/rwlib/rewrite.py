#!/usr/bin/env python3
"""
Model-backed rewriting, one finding at a time, behind the gate the engine
already owns.

**The unit of work is a finding, not a document.** A tell sits in a sentence.
Send that sentence, the rule it broke, and one line of context, and the request
is 150 tokens whatever the document's length. This is the whole reason a 1.7B
model on a Raspberry Pi is a plausible engine for this: there is no chunking
strategy here, no overlap window, no map-reduce, and no context limit to design
around, because the document is never sent. A 10,000-word draft with 40 findings
is 40 independent 150-token calls.

The one exception is shape. `uniformity` and the tier clusters are properties of
a passage rather than of a phrase, so those get the paragraph, sized against
`Endpoint.input_budget()` and skipped when it will not fit. A paragraph that
does not fit in the configured context is reported as such and left alone, which
is the honest outcome: silently truncating it produces a rewrite that drops the
end of somebody's paragraph and verifies clean, because everything it lost was
lost from both sides of the comparison.

**A small model is not trusted, it is gated.** Every candidate has to survive
the same `verify.validate` that `--apply-safe` runs, plus a rescan proving the
tell it was sent to remove is actually gone and that nothing new arrived. A
rejected candidate is retried with the reason attached, then abandoned, and the
original text stays. That gate is what makes the model choice a measurement
instead of an argument: the pass rate for a given model over a fixed battery is
a number, and `skills/rabbit-rewrites/scripts/bench.py` prints it.

`scan_fn` and `validate_fn` are injected. `rwlib` must not import `scan.py` or
`verify.py`: `scan.py` lazily imports `verify`, `verify` imports `rwlib.facts`,
and a module down here reaching back up closes that loop. Same inversion
`stylometry.fingerprint(..., sample_measures=)` uses for the numbers it reports
but does not measure.

Stdlib only, 3.9+.
"""

import json
import os
import re

from . import markdown, sentences
from .endpoint import EndpointError, Truncated
from .endpoint import estimate_tokens as endpoint_estimate_tokens

# Never sent to a model, each for its own reason.
#
#   safety      concealed text is evidence. It is quarantined and quoted, never
#               rewritten, and `run` refuses the whole document over a P0 rather
#               than rewriting around one. See injection.py.
#   structure   a README missing an Install section is not a sentence problem.
#   hidden-unicode, em-dash-rate
#               fixes.py already does these deterministically and correctly. A
#               model asked to remove an em dash sometimes rewrites the clause
#               around it, which is a worse edit than the character swap.
#   suppression-*
#               about the document's own `rabbit-allow` comments, not its prose.
SKIP_BANDS = frozenset(("safety", "structure"))
SKIP_IDS = frozenset((
    "hidden-unicode", "em-dash-rate",
    "suppression-invalid", "suppression-unused", "suppression-refused",
))

# Measured over the whole document and not fixable by editing any one span. A
# paragraph rewrite cannot move a document-wide type-token ratio, and a
# paragraph-length distribution is a property of where the blank lines are.
# Pretending otherwise produces a run that edits six paragraphs and still
# reports the finding, so these are listed as unaddressable rather than skipped
# silently.
DOCUMENT_IDS = frozenset(("low-diversity", "uniform-paragraphs"))

# Findings about a passage rather than a phrase. The unit is the paragraph, and
# it is anchored by the finding's *line* rather than by its match, because these
# do not carry a locatable one: `tier2-cluster` reports "empowers, leverage,
# transformation" (the words that formed the cluster, comma-joined, appearing
# nowhere in that order) and `uniformity` reports "sd/mean of sentence length",
# which is the name of a statistic. A match-first locator finds neither and
# reports both as missing, which is how the first version of this silently did
# nothing about shape at all.
BLOCK_IDS = frozenset(("tier2-cluster", "tier3-density"))

# Shape measured over the whole document that *is* reachable one paragraph at a
# time, unlike DOCUMENT_IDS. Burstiness is the average over every sentence in
# the file, and the way to move it is to rewrite the paragraphs that are
# themselves uniform, so this fans out to those blocks instead of resolving to
# the one line the finding reports.
#
# The floor comes from the caller. `BANDS["burstiness"]` is calibrated and lives
# in scan.py, and a second copy here would be a second calibration constant that
# nothing keeps in step. Called without one, this reports unaddressable rather
# than guessing at a threshold.
SHAPE_IDS = frozenset(("uniformity",))

# Below this a paragraph has too few sentences for sd/mean to mean anything, and
# "vary your sentence lengths" is not advice you can act on with two of them.
MIN_SHAPE_SENTENCES = 3

# What to tell the model, for the findings where the label alone is not an
# instruction. "AI transition" names the problem and does not say what to do
# about it, and a 1.7B given only a name invents a fix.
#
# This lives here rather than in lexicon.json on purpose. The lexicon is the one
# home for *what a pattern is*, and this is advice to a rewriter about what to
# do instead, which is the rewriter's concern and changes without the detection
# changing. Adding a `guidance` key to fifty patterns would also bump the
# lexicon version, and every stored fingerprint and PROOF number quotes it.
GUIDANCE = {
    "negation-runway": "State the point once. Drop the \"not X, but Y\" build-up.",
    "transition-stack": "Delete the opening transition word. Start with the subject.",
    "clarity": "Cut the hedge and say the thing directly.",
    "uniformity": ("Every sentence here is about the same length, which is the "
                   "clearest sign of machine writing. Vary them: put a short "
                   "sentence next to a long one."),
    "tier2-cluster": "Replace the inflated words with ordinary ones.",
    "tier3-density": "Replace the inflated words with ordinary ones.",
    "trigram-repetition": "Vary the repeated phrasing.",
    "tier1": "Replace with an ordinary word that means the same thing.",
    "tier2": "Replace with an ordinary word that means the same thing.",
    "tier3": "Replace with an ordinary word that means the same thing.",
}

DEFAULT_GUIDANCE = "Rewrite so this no longer appears."

SYSTEM_PROMPT = """You are a copy editor. You rewrite one short passage at a time into clear, natural, and plain language.

Remove these machine-writing characteristics:
- Weird subject and verb combinations, and roundabout pseudo-epiphanies.
- Objects performing action verbs (keep actions for humans, groups, or agents; avoid phrases like "this file carries..." or "the module names...").
- Self-praise, AI hedges, and conversational padding.
- Distracting beats and unnecessary complexity.

Absolute rules:
- Keep every number, date, name, file path, URL, and quoted phrase exactly as written.
- Keep all markdown unchanged: code spans, links, list markers, headings, and emphasis.
- Leave fenced code blocks completely unchanged.
- Never use an em dash.
- Do not add facts, opinions, examples, or a closing summary sentence.
- Do not change the meaning. Say the same thing in plainer, everyday words.
- Reply ONLY with the rewritten passage and nothing else: no preamble, no commentary, no labels, no surrounding quotes, no code fence."""

# A wrapping code fence, and the preamble a small model adds however firmly the
# system prompt forbids it. Both are stripped rather than rejected, because the
# rewrite underneath is usually fine and a rejection here costs a whole retry.
_FENCE_WRAP_RX = re.compile(r"(?s)\A\s*```[a-zA-Z0-9_+-]*\n(.*?)\n?```\s*\Z")
_PREAMBLE_RX = re.compile(
    r"(?i)\A\s*(?:here(?:'s| is| are)[^\n:]{0,60}:|"
    r"(?:rewritten|revised|edited|plain[- ]english)(?: version| passage| text)?:|"
    r"sure[,!.][^\n]{0,60}:)\s*\n?")

# A reasoning model's scratchpad, inline. `endpoint.py` asks every server to
# turn thinking off and reads the dedicated `reasoning_content` field when it
# comes back separately, and neither helps on a server that leaves the block in
# `content`. An unterminated opener is stripped too: that is the shape a
# truncated thinking block has, and keeping it would hand the gate a candidate
# made entirely of deliberation.
_THINK_RX = re.compile(
    r"(?is)<(think|thinking|thoughts?|reasoning|analysis)\b[^>]*>"
    r".*?(?:</\1\s*>|\Z)")

# A candidate this far off the original's length is not a rewrite of it. The
# bands are wide because a genuine de-slop *should* shorten ("in order to
# facilitate" -> "to help"), and tight enough that a model which answered the
# passage instead of rewriting it gets caught. Nothing here is calibrated
# against a corpus, because no paired corpus exists: these are guardrails on
# the shape of the failure, and the gate below is what checks correctness.
SPAN_LENGTH_BAND = (0.35, 1.9)
BLOCK_LENGTH_BAND = (0.5, 1.6)

DEFAULT_ATTEMPTS = 3

# Where the optional replacement palette lives, if somebody built one. Naming
# concrete alternatives is worth more to a 1.7B than any amount of instruction:
# told only to replace "delve into", small models reach for "dive deep into".
ALTERNATIVES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "thesaurus_alternatives.json")


class RewriteError(Exception):
    pass


def load_alternatives(path=None):
    """{phrase: [replacement, ...]}, or {} when no palette is installed.

    Optional by design. The palette improves what a small model reaches for and
    nothing depends on it, so a checkout without one rewrites slightly worse
    rather than failing.
    """
    path = path or ALTERNATIVES_PATH
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return {}
    alts = data.get("alternatives") if isinstance(data, dict) else None
    if not isinstance(alts, dict):
        return {}
    return {k.lower(): v for k, v in alts.items() if isinstance(v, list) and v}


def blocks(text):
    """[(start, end, block_text)] for every blank-line-separated block.

    Offsets into `text`, because everything downstream splices by offset. The
    line-based alternative loses the moment a finding's reported line is off by
    one, which is exactly what `_locate` exists to survive.
    """
    out = []
    pos = 0
    for chunk in re.split(r"(\n[ \t]*\n)", text):
        if not chunk:
            continue
        if not re.fullmatch(r"\n[ \t]*\n", chunk) and chunk.strip():
            out.append((pos, pos + len(chunk), chunk))
        pos += len(chunk)
    return out


def _locate(text, match, hint_line):
    """(start, end) of `match` in `text`, or None.

    Nearest occurrence to the finding's reported line wins, and the reported
    line is a hint rather than an index. It has to be: patterns anchored with a
    leading `(^|\\n)` report the line *before* the one the phrase is on, because
    the match starts at the newline that ends the previous line. A locator that
    trusted the number would rewrite the wrong sentence, or more often no
    sentence at all.
    """
    if not match:
        return None
    starts = [m.start() for m in re.finditer(re.escape(match), text)]
    if not starts:
        lowered = text.lower()
        starts = [m.start() for m in re.finditer(re.escape(match.lower()), lowered)]
    if not starts:
        return None
    hint = max(1, int(hint_line or 1))
    best = min(starts, key=lambda s: (abs(markdown.line_of(text, s) - hint), s))
    return best, best + len(match)


def sentence_span(block_text, index):
    """(start, end) of the sentence in `block_text` covering `index`.

    Built from `sentences.split_sentences` rather than from a second splitter,
    because that one is calibrated (abbreviations, initials, numbered lines) and
    every stored fingerprint was measured with it. It returns stripped strings
    with no offsets, so this walks them back onto the block with a cursor.
    """
    cursor = 0
    for sentence in sentences.split_sentences(block_text):
        found = block_text.find(sentence, cursor)
        if found < 0:
            continue
        cursor = found + len(sentence)
        if found <= index < cursor:
            return found, cursor
    return 0, len(block_text.rstrip())


def preceding_sentence(block_text, index):
    """The sentence immediately before the one covering `index`, or "".

    The one line of context `user_prompt` sends: the model sees what came
    right before the passage without being asked to rewrite it too. Same walk
    as `sentence_span`, kept separate because that one returns offsets and
    this one returns the previous sentence's text, and a caller after both
    would need to unpack a three-way return either way.
    """
    cursor = 0
    previous = ""
    for sentence in sentences.split_sentences(block_text):
        found = block_text.find(sentence, cursor)
        if found < 0:
            continue
        cursor = found + len(sentence)
        if found <= index < cursor:
            return previous
        previous = sentence
    return ""


def block_burstiness(block_text):
    """sd/mean of this block's own sentence lengths, or None below the floor.

    The same ratio `scan.compute_stats` reports for the document, over one
    paragraph. Measured here rather than imported because the *number* is
    trivial and it is the *threshold* that is calibrated, and the threshold is
    the caller's to supply.
    """
    lengths = [len(sentences.tokenize(s))
               for s in sentences.split_sentences(block_text)]
    lengths = [n for n in lengths if n]
    if len(lengths) < MIN_SHAPE_SENTENCES:
        return None
    mean = sum(lengths) / len(lengths)
    if not mean:
        return None
    var = sum((n - mean) ** 2 for n in lengths) / len(lengths)
    return (var ** 0.5) / mean


def _addressable(finding):
    if finding.get("suppressed"):
        return False
    if finding.get("band") in SKIP_BANDS:
        return False
    return finding.get("id") not in SKIP_IDS


def plan(text, findings, budget_tokens=None, estimate=None,
         burstiness_floor=None):
    """(units, unaddressable). What can be rewritten, and what cannot.

    A unit is a contiguous span of `text` plus the findings that live in it.
    Findings that land in the same sentence become one unit, because rewriting
    the sentence twice means the second call is working from text the first one
    already changed and the second gate is comparing against the wrong original.

    `burstiness_floor` is `scan.BANDS["burstiness"][0]`. Without it the shape
    findings in SHAPE_IDS come back unaddressable, which is the honest answer
    for a caller that did not say what uniform means.
    """
    estimate = estimate or endpoint_estimate_tokens
    block_list = blocks(text)
    units = {}
    unaddressable = []

    def block_for(start):
        for b_start, b_end, b_text in block_list:
            if b_start <= start < b_end:
                return b_start, b_end, b_text
        return None

    def block_at_line(line):
        for b_start, b_end, b_text in block_list:
            first = markdown.line_of(text, b_start)
            last = markdown.line_of(text, max(b_start, b_end - 1))
            if first <= (line or 1) <= last:
                return b_start, b_end, b_text
        return None

    def add(kind, start, end, finding, context=""):
        unit_text = text[start:end]
        if not unit_text.strip():
            unaddressable.append((finding, "resolved to an empty passage"))
            return
        if budget_tokens is not None and estimate(unit_text) > budget_tokens:
            unaddressable.append(
                (finding, "the %s is %d estimated tokens, past the %d this "
                          "endpoint has room for"
                 % (kind, estimate(unit_text), budget_tokens)))
            return
        key = (start, end)
        if key in units:
            units[key]["findings"].append(finding)
            # A block claim outranks a span claim on the same offsets. It cannot
            # happen with different offsets, and the dedupe pass below handles
            # a span that merely sits *inside* a claimed block.
            if kind == "block":
                units[key]["kind"] = "block"
        else:
            units[key] = {"kind": kind, "start": start, "end": end,
                          "text": unit_text, "findings": [finding],
                          "context": context}

    def prose_block(finding, block):
        if block is None:
            unaddressable.append((finding, "not inside a text block"))
            return None
        if not markdown.is_prose_block(block[2]):
            unaddressable.append((finding, "sits in a list, table, heading or "
                                           "code block, which this does not rewrite"))
            return None
        return block

    for finding in findings:
        fid = finding.get("id")
        if not _addressable(finding):
            continue

        if fid in DOCUMENT_IDS:
            unaddressable.append((finding, "measured over the whole document, "
                                           "so no single passage carries it"))
            continue

        if fid in SHAPE_IDS:
            if burstiness_floor is None:
                unaddressable.append(
                    (finding, "the caller supplied no burstiness floor, so "
                              "there is no threshold to select paragraphs by"))
                continue
            candidates = [(s, e, t) for s, e, t in block_list
                          if markdown.is_prose_block(t)]
            uniform = []
            for s, e, t in candidates:
                bb = block_burstiness(t)
                if bb is not None and bb < burstiness_floor:
                    uniform.append((s, e, t))
            if not uniform:
                unaddressable.append(
                    (finding, "no single paragraph is uniform on its own, so "
                              "the evenness is spread across the document"))
                continue
            for b_start, b_end, b_text in uniform:
                add("block", b_start, b_start + len(b_text.rstrip()), finding)
            continue

        if fid in BLOCK_IDS:
            block = prose_block(finding, block_at_line(finding.get("line")))
            if block is None:
                continue
            b_start, _b_end, b_text = block
            add("block", b_start, b_start + len(b_text.rstrip()), finding)
            continue

        located = _locate(text, finding.get("match", ""), finding.get("line"))
        if located is None:
            unaddressable.append((finding, "could not be located in the text"))
            continue
        block = prose_block(finding, block_for(located[0]))
        if block is None:
            continue
        b_start, _b_end, b_text = block
        b_index = located[0] - b_start
        s_start, s_end = sentence_span(b_text, b_index)
        context = preceding_sentence(b_text, b_index)
        add("span", b_start + s_start, b_start + s_end, finding, context)

    ordered = [units[k] for k in sorted(units)]
    # A span inside a block that is also being rewritten whole would be edited
    # twice from two different originals. The block wins: it is the wider fix
    # and its own gate sees the span's tell too.
    covered = [(u["start"], u["end"]) for u in ordered if u["kind"] == "block"]
    kept = []
    for unit in ordered:
        if unit["kind"] == "span" and any(max(s, unit["start"]) < min(e, unit["end"])
                                          for s, e in covered):
            continue
        kept.append(unit)
    return kept, unaddressable


def _instruction(finding, alternatives):
    fid = finding.get("id") or ""
    match = (finding.get("match") or "").strip()
    guidance = GUIDANCE.get(fid, DEFAULT_GUIDANCE)
    options = alternatives.get(match.lower()) if match else None
    if options:
        guidance = "%s Use one of: %s." % (guidance, ", ".join(options[:5]))
    if match:
        return "- %r (%s). %s" % (match, finding.get("label", fid), guidance)
    return "- %s. %s" % (finding.get("label", fid), guidance)


def user_prompt(unit, alternatives=None, context="", reason=None):
    """The one message sent per attempt. Short on purpose.

    A small model's instruction-following degrades fast with prompt length, and
    every token here competes with the passage for the same 4k window.
    """
    alternatives = alternatives or {}
    noun = "paragraph" if unit["kind"] == "block" else "sentence"
    lines = ["Rewrite this %s in plain, direct English." % noun, ""]
    lines.append("Problems to remove:")
    seen = set()
    for finding in unit["findings"]:
        line = _instruction(finding, alternatives)
        if line not in seen:
            seen.add(line)
            lines.append(line)
    if context:
        lines += ["", "The %s before it, for context only. Do not rewrite it:"
                  % noun, context]
    if reason:
        # The previous attempt, named. A 1.7B corrects a specific complaint far
        # more reliably than it obeys a general rule it already ignored once.
        lines += ["", "Your previous attempt was rejected: %s. Fix that." % reason]
    lines += ["", "%s to rewrite:" % noun.capitalize(), unit["text"]]
    return "\n".join(lines)


def clean_completion(raw):
    """The rewrite, with the wrapper a small model puts around it removed."""
    text = _THINK_RX.sub("", raw or "").strip()
    fence = _FENCE_WRAP_RX.match(text)
    if fence:
        text = fence.group(1).strip()
    text = _PREAMBLE_RX.sub("", text).strip()
    # A model that quoted the whole passage back. Stripped only when the pair is
    # the *only* pair in the passage: `"Ship it," she said, "before Friday."`
    # opens and closes with a quote mark and is not a quoted rewrite, and taking
    # its outer marks off changes what somebody said.
    for mark in ('"', "'"):
        if (len(text) > 2 and text.startswith(mark) and text.endswith(mark)
                and text.count(mark) == 2):
            text = text[1:-1].strip()
            break
    return text


def _fence_count(text):
    return len(re.findall(r"(?m)^\s*```", text))


def gate(unit, candidate, scan_fn, validate_fn, injection_fn=None):
    """[] when the candidate may be used, otherwise the reasons it may not.

    Four checks, and the order is cheapest-first so a nonsense candidate costs
    one regex rather than a full scan.

    The rescan is the half that `verify.validate` cannot do. Validation proves
    the rewrite kept every fact, and it says nothing about whether the tell it
    was sent to remove is gone. Without this, a model that answers "In today's
    fast-paced world, we should not delve into this" passes every preservation
    rule in the engine.
    """
    reasons = []
    original = unit["text"]
    if not candidate.strip():
        return ["the model returned nothing"]
    if candidate.strip() == original.strip():
        return ["the model returned the passage unchanged"]

    low, high = (BLOCK_LENGTH_BAND if unit["kind"] == "block"
                 else SPAN_LENGTH_BAND)
    before_words = max(1, markdown.word_count(original))
    ratio = markdown.word_count(candidate) / before_words
    if not (low <= ratio <= high):
        reasons.append("length went to %.0f%% of the original, outside %d-%d%%"
                       % (ratio * 100, low * 100, high * 100))

    # Added structure. verify.validate checks what was *lost*, which is the
    # right question for a human rewrite and the wrong one here: the failure a
    # small model actually produces is a code fence or a heading it invented
    # around its own answer.
    if _fence_count(candidate) > _fence_count(original):
        reasons.append("the rewrite added a code fence")
    # An HTML comment the model invented, most dangerously a `rabbit-allow`
    # suppression: the rescan below runs with suppressions honored, so a
    # candidate that plants one gets its own remaining tells excluded from
    # `_countable` and can pass the count check while genuinely making
    # nothing better. Reject the shape outright rather than trying to count
    # suppressed findings, which would also block the legitimate case of a
    # rewrite that keeps a comment already present in the original.
    if "<!--" in candidate and "<!--" not in original:
        reasons.append("the rewrite added an HTML comment")
    if reasons:
        return reasons

    verdict = validate_fn(original, candidate)
    if not verdict.get("ok"):
        for violation in verdict.get("violations", [])[:4]:
            reasons.append("%s: %s" % (violation["kind"], violation["detail"]))
        return reasons

    if injection_fn:
        planted = [f for f in injection_fn(candidate) if f["priority"] == "P0"]
        if planted:
            return ["the rewrite contains concealed text addressed to an agent"]

    before_ids = _countable(scan_fn(original))
    after_ids = _countable(scan_fn(candidate))

    # Two questions, and an id-set comparison only answers the first one badly.
    #
    # The phrase the unit was sent to remove has to be gone. Checking the id
    # instead would accept "we should build a robust architecture" as a fix for
    # "we should delve into the architecture", because `robust` is a tier-1 word
    # too and the id is present before and after either way.
    #
    # And the total has to come down. Checking only the phrase accepts that same
    # swap from the other direction: `delve into` is gone, one tier-1 word
    # replaced by another, count unchanged, nothing improved. An edit that does
    # not reduce the count is not worth the risk of making it, which is the
    # stronger form of verify.py's own "never end with more tells than you
    # started with".
    lowered = candidate.lower()
    survivors = sorted({(f.get("match") or "").strip()
                        for f in unit["findings"]
                        if (f.get("match") or "").strip()
                        and (f["match"]).strip().lower() in lowered})
    if survivors:
        reasons.append("still contains %s"
                       % ", ".join(repr(s) for s in survivors))

    before_total, after_total = sum(before_ids.values()), sum(after_ids.values())
    if after_total >= before_total:
        arrived = sorted(i for i in after_ids
                         if after_ids[i] > before_ids.get(i, 0))
        detail = (": introduced %s" % ", ".join(arrived)) if arrived else ""
        reasons.append("findings went %d -> %d, so nothing improved%s"
                       % (before_total, after_total, detail))
    return reasons


def _countable(findings):
    counts = {}
    for finding in findings:
        if finding.get("suppressed") or finding.get("band") in SKIP_BANDS:
            continue
        counts[finding["id"]] = counts.get(finding["id"], 0) + 1
    return counts


def rewrite_unit(unit, endpoint, scan_fn, validate_fn, alternatives=None,
                 attempts=DEFAULT_ATTEMPTS, injection_fn=None, complete=None):
    """(text_or_None, record). One unit, retried up to `attempts` times.

    Temperature climbs across attempts. At 0.2 a model that produced a bad
    rewrite produces nearly the same bad rewrite again, so a retry at the same
    setting is a wasted call rather than a second chance.
    """
    complete = complete or endpoint.complete
    record = {"kind": unit["kind"], "start": unit["start"], "end": unit["end"],
              "ids": sorted({f["id"] for f in unit["findings"]}),
              "before": unit["text"], "after": None, "attempts": [],
              "accepted": False}
    reason = None
    for attempt in range(attempts):
        prompt = user_prompt(unit, alternatives,
                             context=unit.get("context", ""), reason=reason)
        try:
            raw = complete(SYSTEM_PROMPT, prompt,
                           temperature=endpoint.temperature + 0.15 * attempt)
        except Truncated as exc:
            # A higher temperature does not buy more output tokens, so the same
            # oversized unit would run into the same ceiling next attempt. Stop
            # here instead of spending two more calls confirming that.
            record["attempts"].append(str(exc))
            break
        except EndpointError as exc:
            # Narrow on purpose: a TypeError from a bad `complete` injection is
            # a programming error and must surface, not become an "attempt".
            # And a transport failure is not feedback about the prose, so it
            # does not overwrite `reason`: telling the model "could not reach
            # the server. Fix that." is an instruction it cannot follow.
            record["attempts"].append(str(exc))
            continue
        candidate = clean_completion(raw)
        reasons = gate(unit, candidate, scan_fn, validate_fn, injection_fn)
        if not reasons:
            record["after"] = candidate
            record["accepted"] = True
            return candidate, record
        record["attempts"].append("; ".join(reasons))
        reason = reasons[0]
    return None, record


def splice(text, records):
    """The document with every accepted rewrite applied.

    Back to front, so an earlier edit never moves a later one's offsets.
    """
    out = text
    accepted = sorted((r for r in records if r["accepted"]),
                      key=lambda r: r["start"], reverse=True)
    last_start = len(text) + 1
    for record in accepted:
        if record["end"] > last_start:
            # Overlaps with an edit that occurs later in text
            continue
        out = out[:record["start"]] + record["after"] + out[record["end"]:]
        last_start = record["start"]
    return out


def run(text, findings, endpoint, scan_fn, validate_fn, injection_fn=None,
        alternatives=None, attempts=DEFAULT_ATTEMPTS, limit=None,
        estimate=None, complete=None, burstiness_floor=None):
    """Rewrite what can be rewritten, and report everything else.

    The final `validate_fn(text, spliced)` is not redundant with the per-unit
    gates. Each unit was verified against its own span, and a document is not
    the sum of its spans: two accepted rewrites can each keep every number in
    their own sentence and still leave the document with a heading count that
    moved, or with an em dash one of them added where the other removed one.
    `--apply-safe` runs the same belt-and-braces pass for the same reason.
    """
    # Before any request. A document carrying a concealed instruction is not
    # sent to a model at all: the model is the thing the instruction is
    # addressed to, and "rewrite this" is exactly the call that would execute
    # it. The same refusal as run_apply_safe, one step earlier, because there
    # the cost of proceeding is a bad edit and here it is a bad edit made by
    # something that read the attacker's text as an instruction.
    blocking = []
    if injection_fn:
        blocking = [f for f in injection_fn(text) if f["priority"] == "P0"]
    if blocking:
        return {"ok": False, "refused": "safety", "blocking": blocking,
                "text": text, "records": [], "unaddressable": [], "verdict": None}

    alternatives = load_alternatives() if alternatives is None else alternatives
    units, unaddressable = plan(
        text, findings,
        budget_tokens=endpoint.input_budget() if endpoint else None,
        estimate=estimate, burstiness_floor=burstiness_floor)
    if limit:
        for unit in units[limit:]:
            for finding in unit["findings"]:
                unaddressable.append((finding,
                                      "past the --model-limit of %d units" % limit))
        units = units[:limit]

    records = []
    for unit in units:
        _, record = rewrite_unit(unit, endpoint, scan_fn, validate_fn,
                                 alternatives, attempts, injection_fn, complete)
        records.append(record)

    spliced = splice(text, records)
    verdict = validate_fn(text, spliced) if spliced != text else None
    if verdict is not None and not verdict.get("ok"):
        return {"ok": False, "refused": "verify", "blocking": [], "text": text,
                "records": records, "unaddressable": unaddressable,
                "verdict": verdict}
    return {"ok": True, "refused": None, "blocking": [], "text": spliced,
                "records": records, "unaddressable": unaddressable,
                "verdict": verdict}
