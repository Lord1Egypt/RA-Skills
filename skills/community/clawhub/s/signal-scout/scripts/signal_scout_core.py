"""Shared, deterministic pieces of signal-scout: dimension scoring, schema
validation, evidence matching, and verification-tier constants.

This is intentionally narrow. Classification (Individual/Segment/Company) and
the dimension ratings themselves (pain_strength, timing, etc.) are judgment
calls an LLM makes from evidence — that reasoning isn't extractable into code
and this module doesn't attempt it. What *is* deterministic, and previously
duplicated between generate_report.py and verify_sources.py, is: the weighted
formula that turns 0-5 dimension ratings into a 0-100 score, the schema rules
those dimensions must satisfy, the evidence/page matching used to assign a
verification tier, and the tier vocabulary itself. Other tools
(signal-outreach, a CI bot, a future integration) can import this module to
recompute or validate a score without re-reading research-framework.md.
"""

from __future__ import annotations

import re
from typing import Any

# ── Dimension weights, from references/research-framework.md ────────────────

DIMENSION_WEIGHTS: dict[str, dict[str, float]] = {
    "individual": {
        "pain_strength": 0.25,
        "product_fit": 0.25,
        "timing": 0.20,
        "reachability": 0.15,
        "evidence_quality": 0.15,
    },
    "segment": {
        "pain_strength": 0.30,
        "product_fit": 0.30,
        "timing": 0.25,
        "evidence_quality": 0.15,
    },
    "company": {
        "strategic_fit": 0.30,
        "timing": 0.25,
        "execution_ease": 0.25,
        "evidence_quality": 0.20,
    },
}

VALID_STAGES = {"High intent", "Problem aware", "Trigger present", "Potential fit"}


def compute_score(prospect_type: str, dimensions: dict[str, Any]) -> int:
    """Recompute the 0-100 score from 0-5 dimension ratings for the given type.
    Use this to check a self-graded `score` field for arithmetic drift, or to
    (re)score a prospect programmatically once dimensions are known."""
    weights = DIMENSION_WEIGHTS.get(prospect_type)
    if weights is None:
        raise ValueError(f"Unknown prospect_type: {prospect_type!r}")
    total = 0.0
    for key, weight in weights.items():
        try:
            rating = float(dimensions.get(key, 0))
        except (TypeError, ValueError):
            rating = 0.0
        rating = max(0.0, min(5.0, rating))
        total += rating / 5 * weight * 100
    return round(total)


def validate_prospect(prospect_type: str, item: dict[str, Any]) -> list[str]:
    """Return a list of schema violations (empty list = valid). Mirrors the
    validation rules in references/report-artifact.md."""
    errors: list[str] = []
    weights = DIMENSION_WEIGHTS.get(prospect_type)
    if weights is None:
        return [f"Unknown prospect_type: {prospect_type!r}"]

    if not str(item.get("name", "")).strip():
        errors.append("name must be non-empty")

    url = str(item.get("source_url", "")).strip()
    if not url.startswith(("http://", "https://")):
        errors.append("source_url must be a valid http(s) URL")

    stage = item.get("stage")
    if stage not in VALID_STAGES:
        errors.append(f"stage must be one of {sorted(VALID_STAGES)}, got {stage!r}")

    try:
        score = float(item.get("score"))
        if not (0 <= score <= 100):
            errors.append("score must be 0-100")
    except (TypeError, ValueError):
        errors.append("score must be a number 0-100")

    dimensions = item.get("dimensions")
    if not isinstance(dimensions, dict):
        errors.append("dimensions must be an object")
    else:
        missing = set(weights) - set(dimensions)
        if missing:
            errors.append(f"dimensions missing keys: {sorted(missing)}")
        for key in weights:
            if key not in dimensions:
                continue
            try:
                rating = float(dimensions[key])
                if not (0 <= rating <= 5):
                    errors.append(f"dimensions.{key} must be 0-5")
            except (TypeError, ValueError):
                errors.append(f"dimensions.{key} must be a number 0-5")

    if prospect_type == "segment" and not str(item.get("content_angle", "")).strip():
        errors.append("segment requires content_angle")
    if prospect_type == "company":
        if not str(item.get("execution_path", "")).strip():
            errors.append("company requires execution_path")
        if not str(item.get("contact_path", "")).strip():
            errors.append("company requires contact_path")
    if prospect_type == "individual":
        channel = str(item.get("suggested_channel", "")).strip()
        if item.get("opener") and channel == "No public reply/DM channel exists":
            errors.append("opener present but suggested_channel says no channel exists")

    return errors


def csv_safe(value: Any) -> Any:
    """Prefix a text cell that a spreadsheet would run as a formula (leading
    = + - @) with an apostrophe. Fields are copied from web pages."""
    if isinstance(value, str) and value[:1] in ("=", "+", "-", "@"):
        return "'" + value
    return value


# ── Verification tiers, shared between verify_sources.py and generate_report.py ──

TIER_VERIFIED = "verified"          # source fetched, evidence is substantially quoted from the live page
TIER_SNIPPET_ONLY = "snippet_only"  # source blocked automated fetch (e.g. Reddit); snippet-sourced only
TIER_LOW_MATCH = "low_match"        # source fetched, evidence is a paraphrase with its specifics on the page, not quoted
TIER_UNSUPPORTED = "unsupported"    # source fetched and readable, but the claim is not on the page at all
TIER_UNVERIFIED = "unverified"      # not checked, or page yielded no extractable text to check against
TIER_BROKEN = "broken"              # source unreachable or invalid — should not reach a shipped report

TIER_LABELS = {
    TIER_VERIFIED: "Verified",
    TIER_SNIPPET_ONLY: "Snippet-only",
    TIER_LOW_MATCH: "Paraphrased",
    TIER_UNSUPPORTED: "Not on page",
    TIER_UNVERIFIED: "Unverified",
    TIER_BROKEN: "Broken source",
}

# Tiers that must never reach a shipped report or a downstream handoff.
# TIER_UNSUPPORTED is the fabrication signal — the source loaded fine and the
# claim simply isn't in it, which is strictly worse than a dead link.
TIER_DISQUALIFYING = frozenset({TIER_BROKEN, TIER_UNSUPPORTED})


# ── Evidence matching ──────────────────────────────────────────────────────
#
# Asks "is this claim contained in that page?", NOT "are these two strings
# similar?". The distinction is the whole ballgame: a 200-character quote and a
# 40,000-character page are never "similar" by any symmetric string metric —
# difflib's ratio family normalises by the combined length of both inputs, so a
# verbatim quote on a long page scores near zero while any claim at all on a
# short page scores high. That inverts the result on real pages. Containment
# divides by the *evidence* alone, so page length cannot move the score.

# Common words carry no evidential weight — "the" appearing on both sides tells
# us nothing about whether the claim came from the page.
_STOPWORDS = frozenset({
    "the", "and", "for", "that", "this", "with", "have", "has", "had", "been", "was", "were",
    "are", "its", "our", "their", "they", "them", "from", "into", "about", "would", "could",
    "should", "just", "very", "really", "some", "what", "when", "where", "which", "while",
    "than", "then", "there", "here", "will", "your", "you", "but", "not", "all", "can", "out",
})

# A quoted claim shares exact word sequences with the page; a paraphrase only
# shares vocabulary. Two signals, because they fail differently: n-grams prove
# quotation but miss rewording, rare words survive rewording but prove only
# topicality. A claim needs one of them to be considered supported at all.
QUOTED_THRESHOLD = 0.55      # >= this much n-gram overlap ⇒ substantially quoted
SUPPORTED_THRESHOLD = 0.10   # below this on *both* signals ⇒ the claim is not on the page

# Below this much extracted text we didn't really get the page (JS-rendered SPA,
# consent wall, paywall stub). That's a fetch failure, not a fabrication — the
# distinction matters because one is our problem and the other is a false
# accusation against the research.
MIN_PAGE_TEXT_CHARS = 200


# Scripts written without spaces between words. Each character is its own
# token, so a quote's character sequences can be found inside a longer line.
_UNSPACED = re.compile(r"([\u0e00-\u0e7f\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af])")


def _plain(text: Any) -> str:
    """Typographic apostrophes as "'": pages print Bruno\u2019s, evidence is typed Bruno's."""
    return re.sub("[\u2018\u2019\u02bc]", "'", str(text or ""))


def _words(text: str) -> list[str]:
    return re.findall(r"(?:[^\W_]|')+", _UNSPACED.sub(r" \1 ", _plain(text).lower()))


def _ngrams(words: list[str], size: int) -> set[tuple[str, ...]]:
    if len(words) < size:
        return set()
    return {tuple(words[i:i + size]) for i in range(len(words) - size + 1)}


def evidence_signals(evidence: str, page_text: str) -> tuple[float, float]:
    """Return (quoted, topical), each 0-1, measuring how much of `evidence` is
    present in `page_text`.

    `quoted` is n-gram containment — the fraction of the evidence's word
    sequences found on the page. High only for real quotation.
    `topical` is the fraction of the evidence's distinctive (non-stopword)
    terms found on the page. Survives rewording, but proves only that the claim
    talks about what the page talks about.

    Both denominators are the evidence, so neither is affected by page length.
    """
    evidence_words, page_words = _words(evidence), _words(page_text)
    if not evidence_words or not page_words:
        return 0.0, 0.0

    def containment(size: int) -> float:
        wanted = _ngrams(evidence_words, size)
        if not wanted:
            return 0.0
        return len(wanted & _ngrams(page_words, size)) / len(wanted)

    # Trigrams are the cleanest quotation proof; bigrams are discounted because
    # they collide by chance far more often on a large page.
    quoted = max(containment(3), 0.8 * containment(2))

    distinctive = {w for w in evidence_words if len(w) > 3 and w not in _STOPWORDS}
    topical = len(distinctive & set(page_words)) / len(distinctive) if distinctive else 0.0
    return quoted, topical


def _normalize_number(number: str) -> str:
    """ "1,000" and "1000" are one number, as are "15.0" and "15". """
    return re.sub(r"\.0+$", "", number.replace(",", ""))


def _numbers(text: str) -> set[str]:
    return {_normalize_number(n) for n in re.findall(r"\d+(?:[.,]\d+)*", str(text or ""))}


_SCALE_WORDS = {
    "k": "thousand", "thousand": "thousand",
    "m": "million", "mn": "million", "mm": "million", "million": "million",
    "b": "billion", "bn": "billion", "billion": "billion",
    "t": "trillion", "tn": "trillion", "trillion": "trillion",
    "%": "percent", "percent": "percent",
}


def _quantities(text: str) -> set[str]:
    """Numbers carrying a scale word, normalized: "$40M" and "40 million" both
    become "40 million". A bare number check can't tell $40 million from
    $40 billion; this can."""
    found = set()
    pattern = r"(\d+(?:[.,]\d+)*)\s*(%|[A-Za-z]+)\b|(\d+(?:[.,]\d+)*)\s*(%)"
    for m in re.finditer(pattern, str(text or "")):
        num, unit = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        scale = _SCALE_WORDS.get(unit.lower())
        if scale:
            found.add(f"{_normalize_number(num)} {scale}")
    return found


def _letter_identifiers(text: str) -> set[str]:
    """Capitalized word followed by a single capital letter: "Series B",
    "Class A". The one-letter part is the fact, and it's too short to pass
    the name check on its own."""
    return {f"{w} {letter}" for w, letter in re.findall(r"\b([A-Z][a-z]+) ([A-Z])\b", str(text or ""))
            if letter != "I"}  # the pronoun, as in "Yesterday I"


# Sentence ends, except after a title or an initial ("Dr. Lee", "J. Lee"), whose
# next word is a name and not capitalized by position.
_SENTENCE_BREAK = re.compile(
    r"(?<=[.!?])(?<!\bMr\.)(?<!\bMs\.)(?<!\bDr\.)(?<!\bSt\.)(?<!\bMrs\.)(?<!\bProf\.)(?<!\b[A-Z]\.)"
    r"[\"')\]]*\s+(?=[\"'(\[]*[A-Z])"
)


# Ordinary words that open a later sentence. Anything else capitalized there may be a name.
_SENTENCE_OPENERS = frozenset({
    "moreover", "however", "furthermore", "additionally", "also", "meanwhile", "still", "yet",
    "then", "next", "finally", "first", "second", "third", "instead", "overall", "today",
    "recently", "later", "previously", "currently", "thus", "therefore", "similarly", "likewise",
    "nevertheless", "otherwise", "besides", "both", "many", "most", "some", "several", "after",
    "before", "since", "while", "when", "although", "because", "if", "in", "on", "at", "by",
    "for", "from", "with", "as", "to", "of",
})


def missing_specifics(evidence: str, page_text: str) -> list[str]:
    """Numbers (with their scale word), capitalized names and one-letter
    identifiers like "Series B" in the evidence that do not appear on the page.
    Copied from cited's tiering_core.py.

    A fabricated claim about a real entity (a funding round, an investor, a
    date) shares the entity's name with the page, so it clears the topical
    signal. Its specifics are what give it away. Lexical and English-centric:
    capitalized tokens stand in for names. The claim's first token is skipped
    because it is capitalized by position, and so is a later sentence's first
    token when it is an ordinary opener.
    """
    missing = sorted(_numbers(evidence) - _numbers(page_text))
    missing += sorted(_quantities(evidence) - _quantities(page_text))
    page_lower = " " + " ".join(_words(page_text)) + " "
    missing += sorted(i for i in _letter_identifiers(evidence)
                      if " " + " ".join(_words(i)) + " " not in page_lower)
    page_words = set(_words(page_text))
    for i, sentence in enumerate(_SENTENCE_BREAK.split(_plain(evidence))):
        tokens = re.findall(r"[^\W\d_](?:[^\W\d_]|')*", sentence)
        skip_first = i == 0 or (tokens and (tokens[0].lower() in _STOPWORDS or tokens[0].lower() in _SENTENCE_OPENERS))
        for token in tokens[1:] if skip_first else tokens:
            if len(token) >= 2 and token[0].isupper() and token.lower() not in page_words:
                if token not in missing:
                    missing.append(token)
    return missing


def opener_grounding_note(opener: str, evidence: str) -> str:
    """Return a warning if an individual's outreach opener references specifics
    absent from its own checked evidence, else "".

    This is a different axis than tier_for_evidence: that asks "is the evidence
    on the page"; this asks "does the opener stick to what the evidence says."
    Openers legitimately paraphrase and add conversational framing, so this
    checks topical overlap only (SUPPORTED_THRESHOLD) — the stricter
    QUOTED_THRESHOLD would flag ordinary rewording as a problem.
    """
    if not str(opener or "").strip() or not str(evidence or "").strip():
        return ""
    _quoted, topical = evidence_signals(opener, evidence)
    if topical < SUPPORTED_THRESHOLD:
        return (
            f"Opener references specifics not found in the checked evidence (topical {topical:.2f}) "
            "— ground the message in the evidence text before sending"
        )
    return ""


def tier_for_evidence(evidence: str, page_text: str) -> tuple[str, str, float, float]:
    """Classify one prospect's evidence against its fetched page.

    Returns (tier, note, quoted, topical). Callers that couldn't fetch the page
    at all should assign TIER_BROKEN / TIER_SNIPPET_ONLY themselves rather than
    passing empty text here — an empty page is not evidence of fabrication.
    """
    if len(str(page_text or "").strip()) < MIN_PAGE_TEXT_CHARS:
        return (
            TIER_UNVERIFIED,
            "Page returned too little text to verify against (JS-rendered or gated)",
            0.0,
            0.0,
        )

    quoted, topical = evidence_signals(evidence, page_text)
    if not str(evidence or "").strip():
        return TIER_UNVERIFIED, "No evidence text to verify", quoted, topical
    missing = missing_specifics(evidence, page_text)
    if missing:
        return (
            TIER_UNSUPPORTED,
            "Evidence's specifics are not on the live page: " + ", ".join(missing),
            quoted,
            topical,
        )
    if quoted >= QUOTED_THRESHOLD:
        return TIER_VERIFIED, "", quoted, topical
    if quoted >= SUPPORTED_THRESHOLD or topical >= SUPPORTED_THRESHOLD:
        return (
            TIER_LOW_MATCH,
            f"Evidence paraphrases the page rather than quoting it "
            f"(quoted {quoted:.2f}, topical {topical:.2f}) — tighten the quote or note it in limits",
            quoted,
            topical,
        )
    return (
        TIER_UNSUPPORTED,
        "Claim not found on the live page — the source loaded but does not contain this evidence",
        quoted,
        topical,
    )
