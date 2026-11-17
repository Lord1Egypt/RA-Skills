#!/usr/bin/env python3
"""
A voice as a measurable target: the fingerprint, and the distance to it.

Everything the voice band enforces today is a refusal: a banned word, a
punctuation rule, a paragraph cap. A document can clear all of them and sound
like nobody, which SKILL.md admits in prose and nothing measures. This module
is the measurement. It answers "how far is this document from how this person
writes" with a number whose calibrated range comes from the person's own
samples, so "in the voice" stops being a feeling and becomes a band.

The measure is Burrows' Delta, the standard authorship-attribution distance:
the document's function-word rates, z-scored against the author's baseline,
averaged. Function words carry the signal on purpose. Content words are about
the topic, and a voice has to survive a change of topic. "also" versus
"additionally", the contraction rate, and how often a sentence opens with
"but" are the connective tissue where a generic register creeps back in, and
they are exactly what no ban list reaches.

Two departures from textbook Delta, both forced by the data this runs on:

  A fixed marker list, not the corpus top-N. Delta classically takes the most
  frequent words of a large reference corpus. Three writing samples do not
  have a stable top-N: one essay about markets puts "market" in it. The list
  below is fixed, versioned, and English-only, like every other calibration
  in this engine.

  A floored standard deviation. Three samples give a noisy sd, and a marker
  the author uses at an identical rate in every sample gives sd 0, at which
  point any deviation divides to infinity. Each marker's sd is floored at a
  fraction of its mean and at an absolute minimum, so a marker the author
  never uses can still register a deviation without one "moreover" scoring as
  an infinite departure. The floors are stated as constants, not buried.

What a distance is, and is not. It is a signal about register, reported at P2
and never enforced: a writer is allowed to sound unlike themselves on purpose,
and a number that blocked a commit over it would be the humanizer-shaped
failure this plugin exists to avoid. It is also not an authorship verdict, for
every reason references/false-positives.md gives. The finding it feeds says
"further from the profile than any of the samples are from each other", quotes
the markers responsible, and stops there.

The per-marker contributors are the half that makes it actionable. A bare
distance tells a rewrite loop nothing. "additionally at 3.1 sd over the
profile, so at 2.4 sd under" tells it which words to trade.

Two blocks, not one. The markers answer "does this sound like them". The
`measures` block answers "is it built the same way", and it carries min and max
as well as a mean, because the writer's own envelope is what says a converted
document has overshot into caricature. The sentence shape is the distribution
behind `avg_sentence_words`, stored as deciles, and it is a rewrite target
rather than a threshold: nothing in scan.py raises a finding off it.

Neither of those is measured here. They come out of `scan.compute_stats`, and
scan.py imports this module, so the caller passes the numbers in. That is the
same inversion `distributions(..., split_sentences=None)` already uses.

**Callers pass prose with the markup already stripped.** `scan.strip_for_stats`
is that function, and both call sites in this plugin run it first. A fingerprint
built over raw markdown and compared against stripped prose would be measuring
two different things, and the difference would read as a register change: a
code fence has no function words in it at all.

Stdlib only, 3.9+.
"""

import json
import math
import os
import re
import statistics
import sys
from collections import Counter

try:
    from .voices import strip_rules_suffix
    from .markdown import CURLY_APOSTROPHE
except ImportError:
    # Run as a script, so there is no parent package and the relative imports
    # above cannot resolve. The fix is to put the directory *above* rwlib on
    # the path and import the package properly, not to put rwlib itself
    # there: a bare `import markdown` succeeds (rwlib/markdown.py, loaded as
    # a top-level module) and then that file's own `from .artifacts import`
    # fails one level down with the same error, exactly what happened to
    # rwlib/registers.py's CLI for two releases before this same fix.
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from rwlib.voices import strip_rules_suffix
    from rwlib.markdown import CURLY_APOSTROPHE

# Bumped for the sentences.py split fix (mark-then-closer, and a forced
# boundary at each list item): both change what sentence lengths a fingerprint
# was measured over, which is what this version exists to catch. A fingerprint
# stamped 2 was measured with the old splitter and distance() refuses it
# rather than silently comparing against numbers that no longer mean what they
# used to. voices/john.fingerprint.json and every voices/satoshi.*.fingerprint.json
# in this repo are stamped 2 as of this bump and need `measure_voice.py
# --write-fingerprint` rerun from their original samples before voice-distance
# reports for them again; scan.py's apply_voice_distance already degrades this
# to a stderr note rather than a crash.
SCHEMA_VERSION = 3

# The file that sits beside a profile's rules. scan.py looks for it there and
# runs without one, which is the only sane default: a fingerprint costs the
# writer three samples to make, and a profile that has none is still a profile.
FINGERPRINT_SUFFIX = ".fingerprint.json"

# Below this many words a document's marker rates are sampling noise, the same
# reasoning as scan.py's reliability tiers. Reported, never silently ignored.
RELIABLE_WORDS = 250

# The sd floors. RELATIVE_SD_FLOOR is the fraction of a marker's own mean rate
# its sd may not fall under: three samples that happen to agree exactly do not
# license infinite confidence. ABSOLUTE_SD_FLOOR (per 1,000 words) is the floor
# for markers the author never uses at all, chosen so that one occurrence of an
# unused marker in a 1,000-word document scores about 2 sd: notable, finite.
RELATIVE_SD_FLOOR = 0.25
ABSOLUTE_SD_FLOOR = 0.5

# Per-marker z is capped before averaging. A voice is a broad property and the
# distance has to measure breadth. Uncapped, one paragraph that leans on a
# marker the author never uses ("should" nine times in a policy list) scores z
# in the thirties and single-handedly outweighs a hundred markers that sit
# exactly on the profile. Capped, that spike counts as one strong deviation
# among many possible ones, and only a document deviating across many markers
# reads as a different register. The cap is generous enough that a real
# departure still registers at full weight on each marker it touches.
Z_CAP = 4.0

# The marker list, fixed and versioned. Function words, discourse connectors,
# hedges, and the common contractions, because a contraction is one token to
# this tokenizer and the contraction rate is one of the strongest register
# signals a person has. Content words stay out: the fingerprint has to survive
# a change of subject. Editing this list changes every stored fingerprint's
# meaning, which is what SCHEMA_VERSION is for.
MARKER_WORDS = (
    # articles, core prepositions, conjunctions
    "the", "a", "an", "of", "to", "in", "on", "at", "by", "for", "with",
    "from", "into", "over", "under", "about", "between", "through", "during",
    "against", "without", "within", "across", "after", "before", "and", "or",
    "but", "nor", "if", "then", "than", "when", "while", "where", "because",
    "since", "although", "though", "unless", "until", "whereas",
    # pronouns and determiners
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us",
    "them", "my", "your", "his", "its", "our", "their", "this", "that",
    "these", "those", "which", "who", "whom", "whose", "what", "any", "some",
    "all", "no", "none", "each", "every", "both", "either", "neither", "such",
    "same", "own", "other", "another",
    # copulas, auxiliaries, modals
    "is", "are", "was", "were", "be", "been", "being", "am", "do", "does",
    "did", "have", "has", "had", "will", "would", "can", "could", "should",
    "shall", "may", "might", "must",
    # quantity and degree
    "more", "most", "less", "least", "few", "many", "much", "very", "quite",
    "rather", "too", "enough", "only", "even", "still", "yet", "just",
    # discourse connectors, the additionally-versus-also axis
    "so", "also", "however", "additionally", "moreover", "furthermore",
    "therefore", "thus", "hence", "instead", "otherwise", "meanwhile",
    "indeed", "anyway", "besides",
    # hedges and stance adverbs
    "really", "actually", "honestly", "probably", "possibly", "perhaps",
    "maybe", "certainly", "clearly", "obviously", "arguably", "roughly",
    "basically", "essentially", "mostly", "usually", "often", "sometimes",
    "never", "always", "again", "now", "here", "there", "not",
    # contractions, one token each to WORD_RX
    "don't", "doesn't", "didn't", "isn't", "aren't", "wasn't", "weren't",
    "can't", "won't", "wouldn't", "couldn't", "shouldn't", "it's", "that's",
    "there's", "what's", "i'm", "i've", "i'd", "i'll", "you're", "you've",
    "we're", "we've", "they're", "let's",
)

MARKER_SET = frozenset(MARKER_WORDS)

# Lowercase on the way in, apostrophes kept, so "Don't" and "don't" are one
# marker and a contraction is one token. Curly apostrophes are normalized
# first: half the samples anybody pastes come out of an editor that curls
# them, and a fingerprint that reads the curled "don't" as two tokens is
# measuring the editor rather than the writer.
WORD_RX = re.compile(r"[a-z][a-z'\-]*")


def _straight(text):
    return text.lower().replace(CURLY_APOSTROPHE, "'")


def _tokens(text):
    return WORD_RX.findall(_straight(text))


def rates(text):
    """({marker: occurrences per 1,000 words}, word_count) for one document.

    Every marker appears in the dict, at 0.0 when absent, because a missing
    key and a rate of zero are the same fact and downstream arithmetic should
    not have to know two spellings of it.
    """
    tokens = _tokens(text)
    n = len(tokens)
    if n == 0:
        return {m: 0.0 for m in MARKER_WORDS}, 0
    counts = Counter(t for t in tokens if t in MARKER_SET)
    return {m: 1000.0 * counts[m] / n for m in MARKER_WORDS}, n


def _mean_sd(vectors):
    """Per-marker mean and sample sd across sample vectors."""
    n = len(vectors)
    mean = {m: sum(v[m] for v in vectors) / n for m in MARKER_WORDS}
    if n < 2:
        sd = {m: 0.0 for m in MARKER_WORDS}
    else:
        sd = {m: math.sqrt(sum((v[m] - mean[m]) ** 2 for v in vectors)
                           / (n - 1))
              for m in MARKER_WORDS}
    return mean, sd


def _floored(mean, sd):
    return {m: max(sd[m], RELATIVE_SD_FLOOR * mean[m], ABSOLUTE_SD_FLOOR)
            for m in MARKER_WORDS}


def _delta(mean, floored_sd, doc_rates):
    """Burrows' Delta of one document against a baseline, with the receipts.

    Returns (distance, contributors). Contributors are every marker at 1.5 sd
    or more, worst first, each carrying the direction and both rates, because
    the number alone tells a rewrite loop nothing: "additionally at +3.1 sd,
    so at -2.4 sd" tells it which words to trade.

    The cap applies to the distance and not to the receipt. Averaging needs the
    cap so one spiky marker cannot impersonate a register change. The
    contributor list is there to say what happened, and "18 per 1,000 words
    against a profile of zero" is the size of the fact. Capping the report
    would also tie every large deviation at the cap, and a top-N slice of ties
    orders by accident of iteration.
    """
    raw = {m: (doc_rates[m] - mean[m]) / floored_sd[m] for m in MARKER_WORDS}
    distance = sum(min(abs(z), Z_CAP) for z in raw.values()) / len(MARKER_WORDS)
    contributors = [
        {"marker": m, "z": round(raw[m], 2),
         "doc_per_1k": round(doc_rates[m], 2),
         "profile_per_1k": round(mean[m], 2)}
        for m in sorted(raw, key=lambda k: -abs(raw[k]))
        if abs(raw[m]) >= 1.5
    ]
    return distance, contributors


# --------------------------------------------------------------------------
# exemplars
# --------------------------------------------------------------------------
#
# A profile describes and an exemplar demonstrates, and demonstration
# conditions a model harder than adjectives do. These live inside the
# fingerprint file rather than in a `voices/<name>/samples/` directory, so a
# profile stays three files that travel together and there is one path to
# resolve rather than two. The cost is that a fingerprint carrying exemplars
# has the writer's own prose in it, which is why writing them is opt-in and
# why measure_voice.py says so out loud before it writes one.

EXEMPLAR_MIN_WORDS = 25
EXEMPLAR_MAX_WORDS = 220
EXEMPLAR_MAX = 40


def paragraphs(text, min_words=EXEMPLAR_MIN_WORDS, max_words=EXEMPLAR_MAX_WORDS):
    """Prose paragraphs worth keeping as demonstrations.

    Bounded at both ends. Under the floor a paragraph demonstrates nothing, and
    over the ceiling it costs more context than it teaches. Lines that are
    bullets, headings or fences are dropped: an exemplar is there to show how
    this person writes a paragraph.
    """
    out = []
    for block in re.split(r"\n\s*\n", text):
        body = block.strip()
        if not body:
            continue
        lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
        if any(re.match(r"^(?:[-*+]\s|[>#]|\d+[.)]\s|```|\|)", ln) for ln in lines):
            continue
        n = len(_tokens(body))
        if min_words <= n <= max_words:
            out.append(" ".join(lines))
    return out


def nearest_exemplars(paragraph, sample_paragraphs, k=3):
    """The writer's own paragraphs most like the one being rewritten.

    For conditioning a conversion. Similarity is length plus marker profile,
    which is crude and is enough: the point is to hand the model a paragraph of
    theirs in the same register and rough shape, not to find a semantic twin.
    Content similarity would be the wrong axis anyway, since the exemplar is
    there for its voice and not for its subject.
    """
    target_rates, target_n = rates(paragraph)
    scored = []
    for i, sp in enumerate(sample_paragraphs):
        r, n = rates(sp)
        if n < 20:
            continue
        marker_gap = sum(abs(r[m] - target_rates[m])
                         for m in MARKER_WORDS) / len(MARKER_WORDS)
        length_gap = abs(n - target_n) / max(target_n, 1)
        # The index breaks ties, so two equally close paragraphs come back in
        # the order the samples were given rather than by whichever sorts first
        # as a string.
        scored.append((marker_gap + length_gap, i, sp))
    scored.sort(key=lambda row: (row[0], row[1]))
    return [sp for _, _, sp in scored[:k]]


# --------------------------------------------------------------------------
# distributions
# --------------------------------------------------------------------------
#
# The aggregate numbers a voice profile already carries are means: average
# sentence length, average paragraph size, one contraction rate. A mean hides
# the thing a reader actually recognizes. Two writers with the same 18-word
# average write nothing alike if one opens half her sentences with "But" and
# the other never does. These are the distributions behind the means, and they
# are rewrite targets rather than thresholds: nothing enforces them.

# Grouped so the report can say which axis moved rather than listing 30 words.
CONNECTOR_GROUPS = {
    "additive": ("also", "and", "besides", "additionally", "moreover",
                 "furthermore", "plus"),
    "adversative": ("but", "however", "though", "although", "yet", "still",
                    "whereas", "instead"),
    "causal": ("so", "because", "since", "therefore", "thus", "hence",
               "consequently", "accordingly"),
    "sequential": ("then", "next", "first", "finally", "meanwhile", "later",
                   "after", "before"),
}

HEDGES = ("probably", "possibly", "perhaps", "maybe", "roughly", "about",
          "around", "somewhat", "fairly", "pretty", "mostly", "usually",
          "often", "sometimes", "seems", "seem", "suggests", "suggest",
          "tends", "tend", "arguably", "i think", "i suspect", "i'd guess",
          "as far as i know", "in my experience")

INTENSIFIERS = ("very", "really", "actually", "honestly", "clearly",
                "obviously", "certainly", "definitely", "absolutely",
                "completely", "entirely", "totally", "hugely", "massively")

CONTRACTION_RX = re.compile(
    "(?i)\\b[a-z]+['%s](?:t|s|re|ve|ll|d|m)\\b" % CURLY_APOSTROPHE)


def _rate(count, words):
    return round(1000.0 * count / words, 2) if words else 0.0


def distributions(text, top=8, split_sentences=None):
    """The shapes a mean hides, for one document.

    `split_sentences` is `rwlib.sentences.split_sentences` when the caller has
    it. It is a parameter rather than an import because this module is the one
    place a voice gets measured and it should stay usable on a bare string, and
    because the sentence splitter is the engine's and its behaviour is pinned by
    the engine's own tests. Without it, sentences are split on terminal
    punctuation and the openers are a little rougher.
    """
    if split_sentences is None:
        def split_sentences(body):
            return [s for s in re.split(r"(?<=[.!?])\s+", body) if s.strip()]

    tokens = _tokens(text)
    words = len(tokens)
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    sentences = [s.strip() for s in split_sentences(text) if s.strip()]

    def first_word(body):
        found = WORD_RX.search(_straight(body))
        return found.group(0) if found else ""

    sentence_openers = Counter(w for w in (first_word(s) for s in sentences) if w)
    paragraph_openers = Counter(w for w in (first_word(b) for b in blocks) if w)

    counts = Counter(tokens)
    connectors = {
        group: {"per_1k": _rate(sum(counts[w] for w in members), words),
                "n": sum(counts[w] for w in members),
                "used": sorted(w for w in members if counts[w])}
        for group, members in CONNECTOR_GROUPS.items()
    }

    lowered = _straight(text)
    contractions = Counter(_straight(m.group(0))
                           for m in CONTRACTION_RX.finditer(text))

    def phrase_count(entries):
        out = Counter()
        for entry in entries:
            if " " in entry:
                n = len(re.findall(r"\b%s\b" % re.escape(entry), lowered))
            else:
                n = counts[entry]
            if n:
                out[entry] = n
        return out

    hedges = phrase_count(HEDGES)
    intensifiers = phrase_count(INTENSIFIERS)

    # The last sentence of the document, verbatim. Nothing counts it. It is
    # here because "how do they sign off" is the question a voice profile most
    # often gets wrong, and no rate answers it: a person reads three of these
    # and knows. Whitespace collapsed, because a sentence that wrapped across
    # three source lines is one sentence and a report prints it on one row.
    closer = " ".join(sentences[-1].split()) if sentences else ""

    return {
        "words": words,
        "sentence_openers": [{"word": w, "n": n,
                              "share": round(n / len(sentences), 3)}
                             for w, n in sentence_openers.most_common(top)]
                            if sentences else [],
        "paragraph_openers": [{"word": w, "n": n} for w, n
                              in paragraph_openers.most_common(top)],
        "connectors": connectors,
        "contractions": {
            "per_1k": _rate(sum(contractions.values()), words),
            "inventory": [{"form": f, "n": n}
                          for f, n in contractions.most_common(top)],
        },
        "hedges": {"per_1k": _rate(sum(hedges.values()), words),
                   "used": [{"term": t, "n": n} for t, n in hedges.most_common(top)]},
        "intensifiers": {"per_1k": _rate(sum(intensifiers.values()), words),
                         "used": [{"term": t, "n": n}
                                  for t, n in intensifiers.most_common(top)]},
        "closer": closer[:200],
    }


# --------------------------------------------------------------------------
# the measures, and the shape behind the average
# --------------------------------------------------------------------------
#
# A fingerprint's marker block answers "does this sound like them". These
# answer "is it built the same way": the six stylometrics a profile's
# `## Measured from samples` block already carries, plus the sentence-length
# distribution the averages hide.
#
# **This module does not measure them.** Every one comes out of
# `scan.compute_stats`, and `scan.py` imports this module, so the reverse edge
# is a cycle. The caller passes the numbers in, which is the same inversion
# `distributions(..., split_sentences=None)` already uses and for the same
# reason: this is the one place a voice gets measured and it should stay usable
# on a bare string.

# Which measures a fingerprint carries, in the order a report prints them.
# Moved here from measure_voice.py, which now keeps only the spelling each one
# uses in voices/TEMPLATE.md. Editing this list changes what every stored
# fingerprint means, the same as MARKER_WORDS, which is what SCHEMA_VERSION is
# for.
MEASURES = ("avg_sentence_words", "sentence_sd", "burstiness", "mattr",
            "em_dashes_per_1k", "contraction_rate")

# Deciles. Eleven boundaries once the min and the max are on the ends.
#
# Not the raw sorted lengths, which are exact and resamplable and also ship the
# writer's prose shape verbatim in a file that travels with the plugin, which
# is the argument that made exemplars opt-in. Not fixed histogram buckets,
# which turn the bucket edges into a calibration constant and quantize
# anything sampled back out. Eleven numbers mean the same thing at three
# samples and at thirty.
SHAPE_QUANTILES = 10

# What counts as a short sentence and a long one. references/craft.md and
# patterns.md section 52 both talk in these terms ("mix 3-8 word sentences with
# 20+ word ones"), and the two shares are the facts deciles hide.
SHORT_SENTENCE_WORDS = 8
LONG_SENTENCE_WORDS = 30

# How far off the profile mean a measure may sit before a gate calls it missed,
# in sample sd. 1.5 rather than 2, because this compares a document against a
# writer's own spread and not against a population.
ATTAIN_TOLERANCE = 1.5

# The sd floor for that comparison, as a fraction of the measure's own mean.
# Relative only, with no absolute floor, because the six measures have six
# different units and one number cannot floor them all. Where mean and sd are
# both zero, the floor is zero too and the comparison says so rather than
# dividing.
ATTAIN_SD_FLOOR_FRACTION = 0.10


# --------------------------------------------------------------------------
# caricature
# --------------------------------------------------------------------------
#
# A converted document whose stats sit outside the range of the writer's own
# samples is more them than they are. That is the humanizer failure
# references/false-positives.md warns about, wearing this profile's clothes: an
# editor that applies every rule at maximum strictness installs a caricature.
#
# **The obvious rule does not work, and it was measured.** Leave-one-out over 13
# documents by this repository's writer, rule "any measure outside the sample
# min-max": it fires on 95.5% of held-out pairs at three samples and 90.7% at
# four. Min and max over three samples are two order statistics with enormous
# variance, and with three samples two of them define the envelope. That is a
# constant, not a detector.
#
# Four qualifications bring it to 0.2% at three samples and 0.0% at four, and
# each one is here because removing it puts the number back.

# Corpus medians, measured 2026-08-13 over the 100 READMEs in
# docs/readme-analysis. Hardcoded with the date rather than derived from
# corpus_summary.json, the way scan.BANDS is: a corpus regeneration silently
# flipping a detector's direction is worse than a stale constant.
#
# These pick a sign and nothing else. READMEs are not prose, their sentence
# counts are inflated by list items, and none of these numbers is used as a
# threshold. What they answer is "which side of normal does this writer sit on",
# so that only the tail *away* from normal counts as exaggeration.
CARICATURE_POPULATION = {
    "avg_sentence_words": 22.5,
    "burstiness": 1.14,
    "mattr": 0.734,
    "em_dashes_per_1k": 11.4,
    "contraction_rate": 0.42,
}

# `sentence_sd` is deliberately absent. It is sd and `burstiness` is sd/mean, so
# they are two spellings of one fact: over the 100-README corpus every single
# co-fire was that pair and nothing else, which made a two-measure rule fire on
# one. Keeping both would have meant the rule requiring two measures was
# satisfied by one.
CARICATURE_MEASURES = ("avg_sentence_words", "burstiness", "mattr",
                       "em_dashes_per_1k", "contraction_rate")

# A measure whose profile mean sits within this many sample sd of the population
# value does not participate, because the direction of exaggeration is
# undetermined. Direction alone takes the naive 95.5% to 65.6%.
CARICATURE_DIRECTION_MIN_SD = 0.25

# How far past the writer's own mean, in sample sd, before a measure counts.
CARICATURE_Z = 2.0

# How far past the envelope, as a multiple of the envelope's own width or one
# sample sd, whichever is larger. Distance past min-max alone is not enough: the
# envelope of three samples is two draws.
CARICATURE_PAD = 1.0

# How many measures have to fire together. `false-positives.md` says look for
# clusters and never isolated hits, and this is that rule applied to
# stylometrics.
CARICATURE_MIN_MEASURES = 2

# A two-sample envelope is one interval between two points, and the pad has
# nothing to scale against.
CARICATURE_MIN_SAMPLES = 3

# 20 of the 100 corpus READMEs have under 25 prose sentences and 11 have under
# 10. Burstiness over nine sentences is noise, so a word floor alone is not
# enough here even though it is elsewhere.
CARICATURE_MIN_SENTENCES = 25


def caricature(fp, stats):
    """Measures where this document out-writers the writer, or None.

    Returns a dict at every verdict, so a caller can publish the measurement
    whether or not it crossed: `{"exceeded": [...], "eligible": n, "skipped":
    reason}`. `exceeded` empty means the document is inside the envelope or the
    check did not apply, and `skipped` says which.

    None only when the fingerprint carries no measures at all.
    """
    measures = (fp or {}).get("measures") or {}
    if not measures:
        return None
    n_samples = fp.get("n_samples") or 0
    if n_samples < CARICATURE_MIN_SAMPLES:
        return {"exceeded": [], "eligible": 0,
                "skipped": "%d samples, and an envelope needs %d"
                           % (n_samples, CARICATURE_MIN_SAMPLES)}
    if stats.get("word_count", 0) < RELIABLE_WORDS:
        return {"exceeded": [], "eligible": 0,
                "skipped": "under %d words" % RELIABLE_WORDS}
    if stats.get("sentence_count", 0) < CARICATURE_MIN_SENTENCES:
        return {"exceeded": [], "eligible": 0,
                "skipped": "under %d sentences" % CARICATURE_MIN_SENTENCES}

    exceeded, eligible = [], 0
    for name in CARICATURE_MEASURES:
        entry = measures.get(name)
        value = stats.get(name)
        population = CARICATURE_POPULATION.get(name)
        if entry is None or value is None or population is None:
            continue
        sd = max(entry["sd"], ATTAIN_SD_FLOOR_FRACTION * abs(entry["mean"]))
        if sd == 0:
            # Mean and sd both zero. A writer who never uses an em dash makes
            # any dash infinitely exaggerated, and `voice-em-dash` already owns
            # that fact. Double-reporting it would be the two-checks-one-fact
            # bug uncovered_image_srcs argues against.
            continue
        offset = entry["mean"] - population
        if abs(offset) < CARICATURE_DIRECTION_MIN_SD * sd:
            continue                    # direction undetermined
        eligible += 1
        high = offset > 0
        edge = entry["max"] if high else entry["min"]
        width = max(entry["max"] - entry["min"], sd)
        past = (value - edge) if high else (edge - value)
        if past < CARICATURE_PAD * width:
            continue
        if abs(value - entry["mean"]) / sd < CARICATURE_Z:
            continue
        exceeded.append({"measure": name, "value": round(value, 3),
                         "sample_min": entry["min"], "sample_max": entry["max"],
                         "direction": "above" if high else "below",
                         "z": round((value - entry["mean"]) / sd, 2)})
    if len(exceeded) < CARICATURE_MIN_MEASURES:
        exceeded = []
    return {"exceeded": exceeded, "eligible": eligible, "skipped": None}


def _stdev(values):
    """Sample standard deviation, or 0.0 for a single value.

    Across samples, not within one. It answers "how consistent is this person
    from piece to piece", which is the number that says whether one profile can
    describe them at all or whether they have two registers somebody is about
    to average into a third that is nobody.
    """
    return statistics.stdev(values) if len(values) > 1 else 0.0


def measure_stats(sample_measures):
    """{measure: {"mean", "sd", "min", "max", "n"}} over the samples.

    `sample_measures` is one {measure: value or None} dict per sample, as
    `scan.compute_stats` returns them. A None is dropped and lowers that
    measure's n, which is why n is per measure rather than one number for the
    file: `mattr` is None on any sample under the 100-word window, and a
    fingerprint that reported n=4 for a measure taken from 3 samples would be
    overstating its own base.

    min and max are the point of this over a bare mean and sd. They are the
    writer's own envelope, and a document outside it is more characteristic
    than they are, which is the caricature this engine has to be able to see.
    """
    out = {}
    for m in MEASURES:
        values = [s.get(m) for s in sample_measures]
        values = [float(v) for v in values if v is not None]
        if not values:
            continue
        out[m] = {"mean": round(sum(values) / len(values), 3),
                  "sd": round(_stdev(values), 3),
                  "min": round(min(values), 3),
                  "max": round(max(values), 3),
                  "n": len(values)}
    return out


def sentence_shape(lengths_per_sample):
    """The stored sentence-length distribution, or None with nothing to store.

    `lengths_per_sample` is one list of per-sentence word counts per sample,
    measured over the same stripped prose the markers were measured over. A
    shape built over raw markdown and compared against stripped prose is
    measuring the fences.

    The quantile definition is pinned here on purpose: changing it moves every
    stored file, so which one it is matters less than writing it down.
    `statistics.quantiles(..., method="inclusive")` is available on the 3.9
    floor and does not extrapolate past the observed data, which matters when
    the data is three samples.
    """
    per_sample = [sorted(n for n in lengths if n > 0)
                  for lengths in lengths_per_sample]
    per_sample = [s for s in per_sample if s]
    flat = sorted(n for s in per_sample for n in s)
    if not flat:
        return None
    if len(flat) > 1:
        cuts = statistics.quantiles(flat, n=SHAPE_QUANTILES, method="inclusive")
    else:
        cuts = [flat[0]] * (SHAPE_QUANTILES - 1)
    return {
        "n_sentences": len(flat),
        # Integers, because word counts are. Never key a check off the first or
        # the last of these: with three samples they are single sentences.
        "quantiles": [flat[0]] + [int(round(c)) for c in cuts] + [flat[-1]],
        "mean": round(sum(flat) / len(flat), 2),
        "sd": round(_stdev(flat), 2),
        "short_share": round(sum(1 for n in flat
                                 if n <= SHORT_SENTENCE_WORDS) / len(flat), 3),
        "long_share": round(sum(1 for n in flat
                                if n >= LONG_SENTENCE_WORDS) / len(flat), 3),
        # The consistency receipt. It says whether this is one shape or the
        # average of two registers, which no aggregate can.
        "per_sample_median": [int(statistics.median(s)) for s in per_sample],
    }


def shape_target(shape, n_sentences):
    """What a paragraph of `n_sentences` should look like in this voice.

    A band, never a script. "Five sentences, at least one under 9 words, at
    least one over 29, median around 16" is a constraint a rewrite can hold and
    check. A sampled list of exact per-sentence word counts is not: nobody hits
    it, and chasing it manufactures the cadence references/false-positives.md
    calls a new fingerprint rather than the absence of one.

    Returns None when the fingerprint carries no shape.
    """
    if not shape or n_sentences < 1:
        return None
    q = shape["quantiles"]
    return {
        "sentences": n_sentences,
        "short_at_least": min(n_sentences,
                              int(round(shape["short_share"] * n_sentences))),
        "long_at_least": min(n_sentences,
                             int(round(shape["long_share"] * n_sentences))),
        "short_under": SHORT_SENTENCE_WORDS + 1,
        "long_over": LONG_SENTENCE_WORDS - 1,
        "median": q[5],
        "p10": q[1],
        "p90": q[9],
        "sd": shape["sd"],
    }


def measure_gaps(fp, measured, tolerance=ATTAIN_TOLERANCE):
    """One document's stats against a fingerprint's measure block.

    The single definition of "off the profile", so the attainment gate and the
    caricature guard cannot disagree about what that means. Both directions of
    the comparison are reported and neither is judged here: a verdict needs the
    before document, which this does not have.

    A measure the profile does not carry, or the document does not have, comes
    back with `within: None`. That is not the same as passing, and every caller
    has to say which it means.
    """
    profile = (fp or {}).get("measures") or {}
    out = {}
    for m in MEASURES:
        entry = profile.get(m)
        value = measured.get(m)
        row = {"value": value, "profile": entry, "sd_used": None,
               "sd_off": None, "within": None}
        if entry is None or value is None:
            out[m] = row
            continue
        sd_used = max(entry["sd"], ATTAIN_SD_FLOOR_FRACTION * abs(entry["mean"]))
        row["sd_used"] = round(sd_used, 3)
        gap = value - entry["mean"]
        if row["sd_used"] == 0:
            # Mean and sd both zero: a writer who never does the thing at all,
            # em_dashes_per_1k being the case that actually happens. Any nonzero
            # value is off, and sd_off stays null rather than reporting an
            # infinity a report would have to special-case anyway.
            row["within"] = gap == 0
        else:
            row["sd_off"] = round(gap / row["sd_used"], 2)
            row["within"] = abs(row["sd_off"]) <= tolerance
        out[m] = row
    return out


# --------------------------------------------------------------------------
# the fingerprint
# --------------------------------------------------------------------------

def fingerprint(sample_texts, voice=None, exemplars=False,
                sample_measures=None, sentence_lengths=None, register=None):
    """The stored fingerprint for a set of the writer's samples.

    Carries the calibration with it: each sample's leave-one-out distance to
    a fingerprint built from the others. That self-distance band is what makes
    a later measurement readable. A raw Delta means nothing on its own, and
    "0.9, where this writer's own samples sit between 0.5 and 0.8 of each
    other" is a claim a person can act on. With two samples the band is one
    number and thin, and the fingerprint says so instead of hiding it.

    `exemplars=True` embeds the writer's own paragraphs, for conditioning a
    conversion. Opt-in, because it copies their prose into a file that then
    travels with the plugin.

    `sample_measures` and `sentence_lengths` are the v2 half, one entry per
    sample and in the same order. They come from the caller because they come
    from `scan.compute_stats` and this module does not import scan.py. Both are
    optional rather than required, so a caller with a bare string can still
    build a fingerprint to measure a distance against, which is what this
    module's own tests do. A missing block is not announced at all: the comment
    below the return value says why, and `rwlib/voice_check.py` is what fails a
    stored fingerprint that has one.

    `register` names the register these samples were written in, and it is the
    layer where document forms actually diverge. A person's chat register and
    their essay register are two different statistical objects, and averaging
    them produces a fingerprint of nobody, which is what `per_sample_median`
    already exists to make visible. Stored here as well as in the filename so
    the two can be checked against each other: a file renamed by hand is
    otherwise a fingerprint measuring one register while claiming another.
    None is the general fingerprint, used for any register with no measured one.
    """
    if len(sample_texts) < 2:
        raise ValueError("a fingerprint needs at least 2 samples: "
                         "one sample has no self-distance to calibrate against")
    vectors, words = [], []
    for text in sample_texts:
        v, n = rates(text)
        vectors.append(v)
        words.append(n)

    mean, sd = _mean_sd(vectors)

    # Leave-one-out mean, full-set sd. The mean has to exclude the held-out
    # sample or every self-distance is biased low by the sample's own presence
    # in its baseline. The sd deliberately does not: over the two or three
    # samples that remain it is noise, and a marker where the held-out sample
    # happens to be the spread collapses to a tiny sd and an inflated z. The
    # full-set sd is the one distance() will use later, so the band and the
    # measurement it calibrates are computed with the same yardstick.
    floors = _floored(mean, sd)
    self_distances = []
    for i in range(len(vectors)):
        rest = vectors[:i] + vectors[i + 1:]
        rest_mean, _ = _mean_sd(rest)
        d, _ = _delta(rest_mean, floors, vectors[i])
        self_distances.append(round(d, 3))

    thin = [n for n in words if n < RELIABLE_WORDS]
    out = {
        "schema_version": SCHEMA_VERSION,
        "voice": voice,
        # Additive, so no SCHEMA_VERSION bump: it changes nothing about what any
        # stored number means. A fingerprint written before this key existed is
        # the general one, which is exactly what `None` says here.
        "register": register,
        "n_samples": len(sample_texts),
        "sample_words": words,
        "thin_samples": len(thin),
        "markers": {m: {"mean": round(mean[m], 3), "sd": round(sd[m], 3)}
                    for m in MARKER_WORDS},
        "self_distance": {
            "per_sample": self_distances,
            "mean": round(sum(self_distances) / len(self_distances), 3),
            "max": round(max(self_distances), 3),
        },
        "measures": measure_stats(sample_measures) if sample_measures else {},
        "sentence_shape": (sentence_shape(sentence_lengths)
                           if sentence_lengths else None),
    }
    # An empty measure block is not reported here, deliberately. Building a
    # fingerprint without the numbers is the ordinary in-memory case: the
    # reconstruction eval does it to get a baseline out of one document, and
    # half the tests do it from bare strings. Warning on all of that trains a
    # reader to ignore this module's stderr. The case that actually costs
    # something is a *stored* fingerprint with no measures, because a later
    # attainment check reads it and silently answers nothing, and
    # rwlib/voice_check.py fails that outright.
    if exemplars:
        picked = []
        for text in sample_texts:
            picked.extend(paragraphs(text))
        out["exemplars"] = picked[:EXEMPLAR_MAX]
    return out


def distance(fp, text):
    """One document against a stored fingerprint.

    Returns a dict rather than a float, because the float is the least useful
    part: the verdict compares it to the writer's own band, the contributors
    say what moved it, and the reliability says whether to believe any of it.

    verdict values:
        in_range      at or under the max self-distance: indistinguishable
                      from another sample by this measure
        near          under 1.5x the band: drifting, read the contributors
        out_of_range  past that: this does not sound like the profile's owner
    """
    if fp.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("fingerprint schema %r, this module reads %d: "
                         "regenerate it with measure_voice.py"
                         % (fp.get("schema_version"), SCHEMA_VERSION))
    doc_rates, n = rates(text)
    try:
        mean = {m: fp["markers"][m]["mean"] for m in MARKER_WORDS}
        sd = {m: fp["markers"][m]["sd"] for m in MARKER_WORDS}
    except (KeyError, TypeError) as exc:
        raise ValueError("fingerprint is missing marker %s. It was written by a "
                         "different marker list: regenerate it with "
                         "measure_voice.py" % exc)
    d, contributors = _delta(mean, _floored(mean, sd), doc_rates)

    try:
        band_max = fp["self_distance"]["max"]
        band = dict(fp["self_distance"])
    except (KeyError, TypeError) as exc:
        raise ValueError("fingerprint is missing self_distance. It was written by a "
                         "different version: regenerate it with measure_voice.py")

    if d <= band_max:
        verdict = "in_range"
    elif d <= 1.5 * band_max:
        verdict = "near"
    else:
        verdict = "out_of_range"

    return {
        # Echoed for the reason scan.py echoes the lexicon and register
        # versions: a published measurement is only reproducible if the report
        # says which marker list produced it.
        "schema_version": SCHEMA_VERSION,
        "voice": fp.get("voice"),
        "delta": round(d, 3),
        "band": band,
        "verdict": verdict,
        "words": n,
        "reliable": n >= RELIABLE_WORDS,
        "contributors": contributors[:10],
    }


def register_fingerprint_path(rules_path, register):
    """Where a register's own fingerprint would live, whether or not it does."""
    return "%s.%s%s" % (strip_rules_suffix(rules_path), register,
                        FINGERPRINT_SUFFIX)


def path_for(rules_path, register=None):
    """The fingerprint that belongs to a voice's rules file, if it exists.

    Beside the rules rather than named separately, so whichever profile
    `rwlib.voices.resolve` picked is the one measured against. A profile
    resolved by `.rabbit-voice` and a fingerprint found by some other rule
    would be the two-checkers-disagreeing bug resolve() was written to end.

    `register` asks for that register's own fingerprint first and falls back to
    the general one, which is the whole of the per-form support: the refusals in
    a profile carry across forms unchanged, the mechanics carry with the
    per-register overrides the writer authored, and the statistical target
    switches wholesale, because that is the layer where forms diverge most.
    The fallback is silent and has to be, since almost no profile will ever
    carry more than one.
    """
    if not rules_path:
        return None
    if register:
        scoped = register_fingerprint_path(rules_path, register)
        if os.path.exists(scoped):
            return scoped
    candidate = strip_rules_suffix(rules_path) + FINGERPRINT_SUFFIX
    return candidate if os.path.exists(candidate) else None


def register_of(path):
    """The register a fingerprint filename claims, or None for the general one.

    Read off the filename rather than out of the file, because this is what
    decides which file gets loaded and the two are checked against each other
    afterwards. A middle segment that is not a register is not a register-scoped
    fingerprint at all, and the caller has to say so rather than treating a typo
    as a profile whose name happens to contain a dot.
    """
    base = os.path.basename(path)
    if not base.endswith(FINGERPRINT_SUFFIX):
        return None
    stem = base[:-len(FINGERPRINT_SUFFIX)]
    return stem.rsplit(".", 1)[1] if "." in stem else None


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save(fp, path):
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as fh:
        json.dump(fp, fh, indent=2, sort_keys=False)
        fh.write("\n")
    os.replace(tmp_path, path)
