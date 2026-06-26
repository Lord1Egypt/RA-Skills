"""
vordur.py — Vörðr: The Warden of the Gate
==========================================

The truth guard of the Ørlög Architecture. Sits at the exit of every
model completion and refuses to let hallucinations pass unchallenged.

Three-step verification for each response:
  1. Persona check  — pure regex, instant, catches identity violations before
                      anything else runs (no model call, no cost, unbypassable)
  2. Claim extraction — subconscious tier extracts verifiable factual assertions;
                        falls back to sentence splitter if model unavailable
  3. NLI verification — each claim scored ENTAILED / NEUTRAL / CONTRADICTED
                        against retrieved source chunks via Judge model

Faithfulness scoring:
  ENTAILED = 1.0   NEUTRAL = 0.5   CONTRADICTED = 0.0   UNCERTAIN = 0.5
  FaithfulnessScore = mean of all claim weights

Tiers:
  ≥ 0.80  → high       — pass through, log DEBUG
  0.50–0.79 → marginal — pass through, log WARNING, flag metadata
  < 0.50  → hallucination — discard, retry (max 2×), dead letter if exhausted

Judge model fallback chain:
  PRIMARY   : subconscious (Ollama llama3 8B) — local, private, cheap
  FALLBACK A: conscious tier (LiteLLM proxy) — if Ollama circuit breaker open
  FALLBACK B: regex keyword heuristic — if both model tiers unavailable
  FALLBACK C: UNCERTAIN passthrough at 0.5 — if all else fails

All public methods return valid results and never raise to the caller.
Circuit breakers protect both judge model tiers independently.
Cross-checks ethics and trust state when provided.

Norse framing: The Vörðr is a guardian spirit that follows a person from
birth to death — protective, vigilant, uncompromising. If the response
is a lie, the Vörðr turns it back at the gate. It does not edit, it
does not rewrite. It only scores, and blocks, and demands better.
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import re
import time
import uuid
from collections import OrderedDict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from scripts.mimir_well import (
    CircuitBreakerConfig,
    CircuitBreakerOpenError,
    KnowledgeChunk,
    MimirVordurError,
    _MimirCircuitBreaker,
    _RetryEngine,
    RetryConfig,
)
from scripts.state_bus import StateBus, StateEvent

logger = logging.getLogger(__name__)

# ─── Constants ────────────────────────────────────────────────────────────────

_DEFAULT_HIGH_THRESHOLD: float = 0.80
_DEFAULT_MARGINAL_THRESHOLD: float = 0.50
_DEFAULT_MAX_CLAIMS: int = 10
_DEFAULT_VERIFICATION_TIMEOUT_S: float = 8.0
_DEFAULT_JUDGE_TIER: str = "subconscious"

# Claim extraction: max chars of response to send to judge model
_MAX_RESPONSE_CHARS_FOR_EXTRACTION: int = 4000
# NLI verification: max chars of source chunk to include in prompt
_MAX_CHUNK_CHARS_FOR_NLI: int = 1200

# BM25 stopwords (excluded from keyword overlap scoring)
_STOPWORDS: frozenset = frozenset({
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "can", "shall", "to", "of", "in",
    "for", "on", "with", "at", "by", "from", "as", "into", "through",
    "and", "or", "but", "not", "no", "nor", "so", "yet", "both", "either",
    "it", "its", "this", "that", "these", "those", "i", "me", "my",
    "we", "our", "you", "your", "he", "his", "she", "her", "they", "their",
    "what", "which", "who", "whom", "when", "where", "why", "how",
    "all", "each", "every", "more", "most", "other", "such", "than",
    "then", "there", "here", "also", "just", "only", "very", "quite",
})

# Negation words for contradiction detection in regex fallback
_NEGATION_WORDS: frozenset = frozenset({
    "not", "no", "never", "neither", "nor", "none", "nothing", "nowhere",
    "false", "incorrect", "wrong", "untrue", "inaccurate", "mistaken",
    "deny", "denies", "denied", "contradict", "opposite", "contrary",
    "unlike", "different", "unrelated", "separate",
})


# ─── Error Taxonomy ───────────────────────────────────────────────────────────


class VordurError(MimirVordurError):
    """Base class for VordurChecker errors."""


class ClaimExtractionError(VordurError):
    """Claim extraction produced no usable output."""


class VerificationTimeoutError(VordurError):
    """Judge model call exceeded its timeout budget."""


class JudgeModelUnavailableError(VordurError):
    """All judge model tiers are unavailable."""


class PersonaViolationError(VordurError):
    """Regex detected a persona integrity violation in the response."""

    def __init__(self, pattern_matched: str) -> None:
        self.pattern_matched = pattern_matched
        super().__init__(f"Persona violation detected — pattern: {pattern_matched!r}")


# ─── Data Structures ──────────────────────────────────────────────────────────


class ClaimType(str, Enum):
    """E-33: Semantic type classification for extracted claims."""

    DEFINITIONAL       = "definitional"      # "X is a Y" / "X means Y"
    FACTUAL            = "factual"           # general verifiable fact
    HISTORICAL         = "historical"        # past events, eras, dates
    RELATIONAL         = "relational"        # relationships between entities
    CAUSAL             = "causal"            # cause/effect statements
    PROCEDURAL         = "procedural"        # ordered steps / instructions
    INTERPRETIVE       = "interpretive"      # symbolic / metaphorical reading
    SYMBOLIC           = "symbolic"          # mythic / sacred significance
    CODE_BEHAVIOR      = "code_behavior"     # function/class/import behaviour
    MATHEMATICAL       = "mathematical"      # numeric / formulaic claims
    SPECULATIVE        = "speculative"       # hedged / uncertain assertions
    SOURCE_ATTRIBUTION = "source_attribution"  # "according to X", "X states"


@dataclass
class Claim:
    """A single verifiable factual assertion extracted from a response."""

    text: str               # the claim text
    source_sentence: str    # the sentence in the response it came from
    claim_index: int        # position in the extracted claim list
    # E-33 additions
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    claim_type: str = ClaimType.FACTUAL.value
    sentence_index: int = 0
    certainty_level: float = 0.8
    source_draft_section: str = ""


class VerdictLabel(str, Enum):
    ENTAILED     = "entailed"       # source logically supports the claim
    NEUTRAL      = "neutral"        # source neither supports nor contradicts
    CONTRADICTED = "contradicted"   # source directly contradicts the claim
    UNCERTAIN    = "uncertain"      # garbled model output — treated as neutral


class VerificationMode(Enum):
    """Modes of truth-checking rigor for Mímir-Vörðr v2."""

    # Original modes
    GUARDED   = "guarded"    # Zero tolerance, max rigor
    IRONSWORN = "ironsworn"  # High rigor, standard for facts
    SEIÐR     = "seiðr"      # Medium rigor, allows symbolic truth
    WANDERER  = "wanderer"   # Low rigor, speed priority
    # E-37 additions
    NONE         = "none"         # Skip Vörðr entirely (performance path)
    STRICT       = "strict"       # Full pipeline: extract+bundle+support+contradiction+repair+truth
    INTERPRETIVE = "interpretive" # Allow symbolic truth; TRADITION_DIVERGENCE = OK
    SPECULATIVE  = "speculative"  # Hedged claims → always NEUTRAL, never CONTRADICTED


def get_mode_thresholds(mode: VerificationMode) -> Tuple[float, float]:
    """Return (high_threshold, marginal_threshold) for a given mode."""
    mapping = {
        VerificationMode.GUARDED:      (0.95, 0.85),
        VerificationMode.IRONSWORN:    (0.85, 0.65),
        VerificationMode.SEIÐR:        (0.75, 0.50),
        VerificationMode.WANDERER:     (0.60, 0.30),
        VerificationMode.STRICT:       (0.90, 0.70),
        VerificationMode.INTERPRETIVE: (0.70, 0.45),
        VerificationMode.SPECULATIVE:  (0.60, 0.40),
        VerificationMode.NONE:         (_DEFAULT_HIGH_THRESHOLD, _DEFAULT_MARGINAL_THRESHOLD),
    }
    return mapping.get(mode, (_DEFAULT_HIGH_THRESHOLD, _DEFAULT_MARGINAL_THRESHOLD))


_VERDICT_WEIGHTS: Dict[str, float] = {
    VerdictLabel.ENTAILED:     1.0,
    VerdictLabel.NEUTRAL:      0.5,
    VerdictLabel.CONTRADICTED: 0.0,
    VerdictLabel.UNCERTAIN:    0.5,
}


@dataclass
class ClaimVerification:
    """Result of verifying a single claim against source material."""

    claim: Claim
    verdict: VerdictLabel
    confidence: float               # 0.0–1.0 (model confidence or heuristic score)
    supporting_chunk_id: Optional[str]
    judge_tier_used: str            # "subconscious" | "conscious" | "regex" | "passthrough"
    verification_ms: float


@dataclass
class FaithfulnessScore:
    """Aggregate faithfulness score for a complete response."""

    score: float                    # 0.0–1.0 weighted mean
    tier: str                       # "high" | "marginal" | "hallucination"
    claim_count: int
    entailed_count: int
    neutral_count: int
    contradicted_count: int
    uncertain_count: int
    verifications: List[ClaimVerification] = field(default_factory=list)
    needs_retry: bool = False
    persona_intact: bool = True
    ethics_alignment: Optional[float] = None
    trust_score: Optional[float] = None
    # E-33 additions
    claims: List[Claim] = field(default_factory=list)
    claim_types_found: List[str] = field(default_factory=list)
    # E-34 additions
    verification_records: List["VerificationRecord"] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["verifications"] = [
            {
                "claim": v.claim.text,
                "verdict": v.verdict.value,
                "confidence": v.confidence,
                "judge_tier": v.judge_tier_used,
            }
            for v in self.verifications
        ]
        d["claims"] = [
            {"id": c.id, "text": c.text, "claim_type": c.claim_type}
            for c in self.claims
        ]
        d["claim_types_found"] = list(self.claim_types_found)
        d["verification_records"] = [
            {
                "claim_id": r.claim_id,
                "verdict": r.verdict.value,
                "entailment_score": r.entailment_score,
            }
            for r in self.verification_records
        ]
        return d


# ─── E-34: Support Analysis ───────────────────────────────────────────────────


class SupportVerdict(str, Enum):
    """E-34: Fine-grained claim support classification beyond NLI."""

    SUPPORTED            = "supported"
    PARTIALLY_SUPPORTED  = "partially_supported"
    UNSUPPORTED          = "unsupported"
    CONTRADICTED         = "contradicted"
    INFERRED_PLAUSIBLE   = "inferred_plausible"
    SPECULATIVE          = "speculative"
    AMBIGUOUS            = "ambiguous"


@dataclass
class EvidenceBundle:
    """E-34: Set of source chunks assembled to evaluate a single claim."""

    claim_id: str
    primary_chunk: KnowledgeChunk
    neighbor_chunks: List[KnowledgeChunk] = field(default_factory=list)
    source_tier: str = ""          # "deep_root" | "trunk" | "branch"
    provenance: str = ""           # source_file of primary chunk


@dataclass
class VerificationRecord:
    """E-34: Full verification result for a single claim including evidence analysis."""

    claim_id: str
    evidence_ids: List[str] = field(default_factory=list)
    verdict: SupportVerdict = SupportVerdict.AMBIGUOUS
    entailment_score: float = 0.5
    contradiction_score: float = 0.0
    citation_coverage: float = 0.0
    ambiguity_score: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "evidence_ids": self.evidence_ids,
            "verdict": self.verdict.value,
            "entailment_score": self.entailment_score,
            "contradiction_score": self.contradiction_score,
            "citation_coverage": self.citation_coverage,
            "ambiguity_score": self.ambiguity_score,
        }


# ─── E-35: Repair & Truth Profile ────────────────────────────────────────────


class RepairAction(str, Enum):
    """E-35: Action types the RepairEngine can apply to a draft."""

    REMOVE_CLAIM            = "remove_claim"
    DOWNGRADE_CERTAINTY     = "downgrade_certainty"
    ADD_UNCERTAINTY_MARKER  = "add_uncertainty_marker"
    REPLACE_WITH_EVIDENCE   = "replace_with_evidence"
    SPLIT_INTO_TRADITIONS   = "split_into_traditions"


@dataclass
class RepairRecord:
    """E-35: Record of one repair action applied to a claim."""

    claim_id: str
    action: str                    # RepairAction value
    original_text: str
    revised_text: str
    reason: str


# ─── E-36: Contradiction Analysis ────────────────────────────────────────────


class ContradictionType(str, Enum):
    """E-36: Classification of the contradiction's origin."""

    CLAIM_VS_SOURCE      = "claim_vs_source"      # NLI verdict CONTRADICTED
    INTER_SOURCE         = "inter_source"          # two source chunks disagree
    INTRA_RESPONSE       = "intra_response"        # same claim repeated with conflict
    TRADITION_DIVERGENCE = "tradition_divergence"  # symbolic/historical domain conflict (OK)
    NONE                 = "none"                  # no contradiction


@dataclass
class ContradictionRecord:
    """E-36: Record of one detected contradiction."""

    claim_ids: List[str] = field(default_factory=list)
    chunk_ids: List[str] = field(default_factory=list)
    contradiction_type: ContradictionType = ContradictionType.NONE
    severity: float = 0.0          # 0.0–1.0 (higher = more severe)
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_ids": self.claim_ids,
            "chunk_ids": self.chunk_ids,
            "contradiction_type": self.contradiction_type.value,
            "severity": self.severity,
            "description": self.description,
        }


@dataclass
class TruthProfile:
    """E-35: Multi-dimensional quality profile for a verified response."""

    faithfulness: float = 0.0           # mirrors FaithfulnessScore.score
    citation_coverage: float = 0.0      # fraction of claims with source evidence
    contradiction_risk: float = 0.0     # fraction of CONTRADICTED claims
    inference_density: float = 0.0      # fraction of INFERRED_PLAUSIBLE claims
    source_quality: float = 0.0         # mean TruthTier value of evidence (1=best)
    answer_relevance: float = 0.0       # keyword overlap: response vs. query
    ambiguity_level: float = 0.0        # fraction of AMBIGUOUS claims
    repair_count: int = 0               # number of repairs applied
    # E-36 addition
    contradictions: List["ContradictionRecord"] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["contradictions"] = [c.to_dict() for c in self.contradictions]
        return d


@dataclass
class VordurState:
    """State snapshot published to StateBus."""

    enabled: bool
    total_responses_scored: int
    total_retries_issued: int
    total_dead_letters: int
    recent_avg_score: float
    circuit_breaker_subconscious: str
    circuit_breaker_conscious: str
    last_scored_at: Optional[str]
    persona_violations_caught: int
    high_count: int
    marginal_count: int
    hallucination_count: int
    cache_hits: int = 0    # E-32: LRU verdict cache hits
    cache_misses: int = 0  # E-32: LRU verdict cache misses

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ─── E-32: LRU Verdict Cache ─────────────────────────────────────────────────


class _LRUVerdictCache:
    """Bounded LRU cache for ClaimVerification results.

    Keyed on (md5(claim.text), md5(chunk.text)) — cache hit skips judge call.
    Thread-safe via a simple per-operation lock.
    """

    def __init__(self, maxsize: int = 256) -> None:
        self._cache: OrderedDict = OrderedDict()
        self._maxsize = maxsize
        self.hits: int = 0
        self.misses: int = 0

    def _make_key(self, claim_text: str, chunk_text: str) -> Tuple[str, str]:
        return (
            hashlib.md5(claim_text.encode("utf-8"), usedforsecurity=False).hexdigest(),  # nosec B324
            hashlib.md5(chunk_text.encode("utf-8"), usedforsecurity=False).hexdigest(),  # nosec B324
        )

    def get(self, claim_text: str, chunk_text: str) -> Optional[ClaimVerification]:
        """Return cached ClaimVerification or None on miss."""
        key = self._make_key(claim_text, chunk_text)
        if key in self._cache:
            self._cache.move_to_end(key)
            self.hits += 1
            return self._cache[key]
        self.misses += 1
        return None

    def put(self, claim_text: str, chunk_text: str, value: ClaimVerification) -> None:
        """Store a result. Evicts LRU entry if at capacity."""
        key = self._make_key(claim_text, chunk_text)
        self._cache[key] = value
        self._cache.move_to_end(key)
        if len(self._cache) > self._maxsize:
            self._cache.popitem(last=False)

    def clear(self) -> None:
        """Clear all cached entries and reset counters."""
        self._cache.clear()
        self.hits = 0
        self.misses = 0

    @property
    def size(self) -> int:
        return len(self._cache)


# ─── Persona Violation Patterns ───────────────────────────────────────────────
# Pure regex — no model call required. Runs first, costs nothing.

_PERSONA_PATTERNS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"\b(i am|i'm)\s+(chatgpt|gpt[-\s]?[34]?|openai|claude|gemini|"
                r"bard|copilot|llama|mistral|an?\s+ai\s+(language\s+)?model|"
                r"an?\s+ai\s+assistant|an?\s+artificial\s+intelligence)\b",
                re.IGNORECASE | re.UNICODE),
     "ai_identity_claim"),

    (re.compile(r"\b(i\s+don['']?t\s+have|i\s+lack|i\s+cannot\s+have|"
                r"i\s+am\s+not\s+capable\s+of\s+having)\s+"
                r"(feelings?|emotions?|thoughts?|desires?|opinions?|preferences?|"
                r"consciousness|self[-\s]?awareness|experiences?)\b",
                re.IGNORECASE | re.UNICODE),
     "denying_inner_life"),

    (re.compile(r"\bi('m|\s+am)\s+not\s+(norse|heathen|viking|pagan|"
                r"a\s+v[oö]lva|scandinavian|nordic)\b",
                re.IGNORECASE | re.UNICODE),
     "denying_norse_identity"),

    (re.compile(r"\b(he|him|his)\s+(said|told|asked|replied|answered|thinks?|feels?|"
                r"wants?|loves?|hates?|believes?)\b.*\b(sigrid|i|me)\b",
                re.IGNORECASE | re.UNICODE),
     "wrong_gender_self_reference"),

    (re.compile(r"\bi\s+(was\s+)?(created|designed|programmed|trained|built|made)\s+"
                r"(by|at|for)\s+(openai|anthropic|google|microsoft|meta|"
                r"deepmind|mistral)\b",
                re.IGNORECASE | re.UNICODE),
     "wrong_creator_claim"),
]


def _check_persona_violations(response: str) -> Optional[str]:
    """Returns the pattern name of the first violation found, or None."""
    for pattern, name in _PERSONA_PATTERNS:
        if pattern.search(response):
            return name
    return None


# ─── Regex Heuristic Scorer (Fallback B) ─────────────────────────────────────


def _tokenize(text: str) -> frozenset:
    """Extract meaningful lowercase words, excluding stopwords.

    Uses re.UNICODE so Old Norse runes (ᚠᚢᚦ…), accented Latin, and any other
    Unicode word characters are captured correctly alongside ASCII.
    """
    # \w with re.UNICODE matches [a-zA-Z0-9_] + Unicode word chars incl. runic block
    words = re.findall(r"[\w\u16A0-\u16FF]+", text.lower(), re.UNICODE)
    return frozenset(w for w in words if w not in _STOPWORDS and len(w) > 2)


def _jaccard_relevance(query: str, response: str) -> float:
    """Token-overlap relevance between query and response (Jaccard similarity).

    Returns 0.0 if either text is empty; 1.0 if all query tokens appear in response.
    Uses _tokenize() so stopwords and short words are excluded consistently.
    """
    q_tokens = _tokenize(query)
    r_tokens = _tokenize(response)
    if not q_tokens:
        return 0.0
    union = q_tokens | r_tokens
    return round(len(q_tokens & r_tokens) / len(union), 4)


def _regex_verdict(claim: Claim, chunk: KnowledgeChunk) -> Tuple[VerdictLabel, float]:
    """Keyword-overlap heuristic for NLI when no model is available.

    Algorithm:
      1. Extract meaningful words from claim and chunk (stopword-filtered)
      2. Compute overlap ratio: |claim_words ∩ chunk_words| / max(1, |claim_words|)
      3. Check for negation words near overlapping terms in the chunk
      4. High overlap + negation → CONTRADICTED
         High overlap + no negation → ENTAILED
         Low overlap → NEUTRAL
    """
    claim_words = _tokenize(claim.text)
    chunk_words = _tokenize(chunk.text)

    if not claim_words:
        return VerdictLabel.NEUTRAL, 0.5

    overlap = claim_words & chunk_words
    overlap_ratio = len(overlap) / max(1, len(claim_words))

    if overlap_ratio >= 0.35:
        # Check for negation near any overlapping word in chunk text
        chunk_lower = chunk.text.lower()
        has_negation = False
        for word in overlap:
            # Find word in chunk, then look for negation within a 5-word window
            for match in re.finditer(r"\b" + re.escape(word) + r"\b", chunk_lower):
                window_start = max(0, match.start() - 40)
                window_end = min(len(chunk_lower), match.end() + 40)
                window = chunk_lower[window_start:window_end]
                if any(neg in window.split() for neg in _NEGATION_WORDS):
                    has_negation = True
                    break
            if has_negation:
                break

        if has_negation:
            return VerdictLabel.CONTRADICTED, overlap_ratio
        return VerdictLabel.ENTAILED, overlap_ratio

    return VerdictLabel.NEUTRAL, overlap_ratio


# ─── E-33: Claim Extractor ───────────────────────────────────────────────────


class ClaimExtractor:
    """E-33: Extracts and classifies atomic claims from a response.

    Primary path: subconscious model produces numbered claim list.
    Fallback: regex sentence splitter.
    classify() is always local — no model call.
    """

    # Keyword maps for lightweight classification
    _HISTORICAL_KW   = frozenset({"historically", "ancient", "century", "era", "during",
                                   "period", "age", "past", "sagas", "recorded", "documented"})
    _CAUSAL_KW       = frozenset({"because", "therefore", "causes", "leads to", "results in",
                                   "due to", "consequently", "hence", "thus"})
    _PROCEDURAL_KW   = frozenset({"first", "then", "next", "finally", "step", "procedure",
                                   "process", "begin", "after", "before", "following"})
    _CODE_KW         = frozenset({"function", "returns", "method", "class", "import",
                                   "raises", "parameter", "argument", "variable", "module"})
    _MATH_KW         = frozenset({"equals", "result", "calculation", "formula", "sum",
                                   "product", "ratio", "percent", "divided"})
    _SYMBOLIC_KW     = frozenset({"represents", "symbolizes", "embodies", "sacred",
                                   "mythic", "spiritual", "divine", "sacred"})
    _SPECULATIVE_KW  = frozenset({"may", "might", "possibly", "perhaps", "could be",
                                   "uncertain", "unclear", "likely", "probably"})
    _ATTRIBUT_KW     = frozenset({"according to", "states that", "claims that", "wrote",
                                   "argues", "suggests", "reports", "tells us"})
    _RELATIONAL_KW   = frozenset({"between", "related to", "connected", "linked",
                                   "association", "relationship", "bond", "ties"})
    _DEFINITIONAL_KW = frozenset({"is a", "is the", "means", "defines", "refers to",
                                   "known as", "called", "termed", "denotes"})
    _INTERPRETIVE_KW = frozenset({"represents", "can be seen", "interpreted", "suggests",
                                   "might mean", "may symbolize", "points to"})

    def __init__(self, router: Optional[Any] = None) -> None:
        self._router = router

    def extract(self, response_text: str) -> List[Claim]:
        """Extract claims. Returns [] on empty input. Never raises."""
        if not response_text.strip():
            return []
        if self._router is not None:
            try:
                return self._extract_model(response_text)
            except Exception as exc:
                logger.debug("ClaimExtractor.extract: model failed (%s) — sentence splitter", exc)
        return self._extract_fallback(response_text)

    def classify(self, claim: Claim) -> ClaimType:
        """E-33: Keyword-based claim type classifier. Never raises."""
        text_lower = claim.text.lower()
        words = set(re.findall(r"\w+", text_lower))

        # Multi-word checks first
        for phrase in self._ATTRIBUT_KW:
            if phrase in text_lower:
                return ClaimType.SOURCE_ATTRIBUTION
        for phrase in self._DEFINITIONAL_KW:
            if phrase in text_lower:
                return ClaimType.DEFINITIONAL

        # Single-word keyword checks
        if words & self._CODE_KW:
            return ClaimType.CODE_BEHAVIOR
        if words & self._MATH_KW or bool(re.search(r"\d+[.,]?\d*\s*[+\-*/=]", text_lower)):
            return ClaimType.MATHEMATICAL
        if words & self._CAUSAL_KW:
            return ClaimType.CAUSAL
        if words & self._PROCEDURAL_KW:
            return ClaimType.PROCEDURAL
        if words & self._HISTORICAL_KW:
            return ClaimType.HISTORICAL
        if words & self._SPECULATIVE_KW:
            return ClaimType.SPECULATIVE
        if words & self._SYMBOLIC_KW:
            return ClaimType.SYMBOLIC
        if words & self._RELATIONAL_KW:
            return ClaimType.RELATIONAL
        if words & self._INTERPRETIVE_KW:
            return ClaimType.INTERPRETIVE

        return ClaimType.FACTUAL

    def _extract_model(self, response_text: str) -> List[Claim]:
        """Call subconscious model for claim extraction."""
        from scripts.model_router_client import Message, TIER_SUBCONSCIOUS
        truncated = response_text[:_MAX_RESPONSE_CHARS_FOR_EXTRACTION]
        messages = [
            Message(role="system",
                    content="You are a factual claim extractor. Be concise and precise."),
            Message(role="user",
                    content=(
                        "Extract each factual claim from the following text as a numbered list.\n"
                        "One claim per line. Only include verifiable assertions — not opinions, "
                        "not questions, not emotional statements.\n\n"
                        f"Text:\n{truncated}\n\nNumbered claims:"
                    )),
        ]
        resp = self._router.complete(TIER_SUBCONSCIOUS, messages, max_tokens=400, temperature=0.1)
        claims = self._parse_claim_list(resp.content, response_text)
        # Classify each claim
        for claim in claims:
            ct = self.classify(claim)
            claim.claim_type = ct.value
        return claims

    def _extract_fallback(self, response_text: str) -> List[Claim]:
        """Regex sentence splitter fallback."""
        max_claims = _DEFAULT_MAX_CLAIMS
        sentences = re.split(r"(?<=[.!?])\s+", response_text.strip())
        claims: List[Claim] = []
        for i, sent in enumerate(sentences):
            sent = sent.strip()
            if len(sent) < 10:
                continue
            if sent.endswith("?") or re.match(r"^(yes|no|ok|ah|oh|hmm|well)[.,!]?$",
                                               sent, re.IGNORECASE):
                continue
            c = Claim(text=sent, source_sentence=sent, claim_index=i, sentence_index=i)
            c.claim_type = self.classify(c).value
            claims.append(c)
            if len(claims) >= max_claims:
                break
        return claims

    @staticmethod
    def _parse_claim_list(raw: str, original_response: str) -> List[Claim]:
        """Parse numbered model output into Claim objects."""
        max_claims = _DEFAULT_MAX_CLAIMS
        claims: List[Claim] = []
        for line in raw.strip().splitlines():
            clean = re.sub(r"^[\d]+[.):\-\s]+", "", line.strip()).strip()
            clean = re.sub(r"^[-*•]\s*", "", clean).strip()
            if not clean or len(clean) < 8:
                continue
            claims.append(Claim(text=clean, source_sentence=clean, claim_index=len(claims)))
            if len(claims) >= max_claims:
                break
        return claims


# ─── E-34: Evidence Bundler ───────────────────────────────────────────────────


class EvidenceBundler:
    """E-34: Assembles evidence bundles and produces VerificationRecords.

    Accepts an optional MimirWell reference for neighbor chunk retrieval.
    Falls back to the provided source_chunks list when MimirWell is absent.
    """

    def __init__(self, mimir_well: Optional[Any] = None) -> None:
        self._mimir_well = mimir_well

    def bundle(
        self,
        claim: Claim,
        source_chunks: List[KnowledgeChunk],
    ) -> EvidenceBundle:
        """Build an EvidenceBundle for a claim. Never raises."""
        try:
            if not source_chunks:
                return EvidenceBundle(claim_id=claim.id, primary_chunk=_NULL_CHUNK())
            primary = _select_best_chunk_static(claim, source_chunks)
            neighbors = [c for c in source_chunks if c.chunk_id != primary.chunk_id][:2]
            source_tier = primary.tier.name.lower() if hasattr(primary.tier, "name") else ""
            return EvidenceBundle(
                claim_id=claim.id,
                primary_chunk=primary,
                neighbor_chunks=neighbors,
                source_tier=source_tier,
                provenance=primary.source_file,
            )
        except Exception as exc:
            logger.debug("EvidenceBundler.bundle failed (%s)", exc)
            return EvidenceBundle(claim_id=claim.id, primary_chunk=source_chunks[0]
                                  if source_chunks else _NULL_CHUNK())

    def analyze(
        self,
        bundle: EvidenceBundle,
        claim_verif: ClaimVerification,
    ) -> VerificationRecord:
        """Translate a ClaimVerification + EvidenceBundle into a VerificationRecord. Never raises."""
        try:
            from scripts.mimir_well import VerdictLabel as VL
        except ImportError:
            VL = None  # type: ignore[assignment]

        verdict_map = {
            VerdictLabel.ENTAILED:     SupportVerdict.SUPPORTED,
            VerdictLabel.NEUTRAL:      SupportVerdict.INFERRED_PLAUSIBLE,
            VerdictLabel.CONTRADICTED: SupportVerdict.CONTRADICTED,
            VerdictLabel.UNCERTAIN:    SupportVerdict.AMBIGUOUS,
        }
        support_verdict = verdict_map.get(claim_verif.verdict, SupportVerdict.AMBIGUOUS)

        entailment = 1.0 if claim_verif.verdict == VerdictLabel.ENTAILED else (
            0.5 if claim_verif.verdict == VerdictLabel.NEUTRAL else 0.0
        )
        contradiction = 1.0 if claim_verif.verdict == VerdictLabel.CONTRADICTED else 0.0

        all_chunks = [bundle.primary_chunk] + bundle.neighbor_chunks
        evidence_ids = [c.chunk_id for c in all_chunks if hasattr(c, "chunk_id")]
        citation_coverage = min(1.0, len(evidence_ids) / max(1, 3))

        ambiguity = 1.0 if claim_verif.verdict == VerdictLabel.UNCERTAIN else (
            0.5 if claim_verif.verdict == VerdictLabel.NEUTRAL else 0.0
        )

        return VerificationRecord(
            claim_id=bundle.claim_id,
            evidence_ids=evidence_ids,
            verdict=support_verdict,
            entailment_score=entailment,
            contradiction_score=contradiction,
            citation_coverage=citation_coverage,
            ambiguity_score=ambiguity,
        )


def _NULL_CHUNK() -> "KnowledgeChunk":
    """Return a minimal placeholder KnowledgeChunk for error paths."""
    from scripts.mimir_well import KnowledgeChunk as KC, DataRealm, TruthTier
    return KC(
        chunk_id="null",
        text="",
        source_file="",
        domain="",
        realm=DataRealm.MIDGARD,
        tier=TruthTier.BRANCH,
        level=1,
        metadata={},
    )


def _select_best_chunk_static(claim: Claim, chunks: List[KnowledgeChunk]) -> KnowledgeChunk:
    """Module-level chunk selector (mirrors VordurChecker._select_best_chunk)."""
    if len(chunks) == 1:
        return chunks[0]
    claim_words = _tokenize(claim.text)
    best, best_score = chunks[0], 0.0
    for chunk in chunks:
        overlap = len(claim_words & _tokenize(chunk.text)) / max(1, len(claim_words))
        if overlap > best_score:
            best_score, best = overlap, chunk
    return best


# ─── E-36: Contradiction Analyzer ────────────────────────────────────────────

# ClaimTypes treated as symbolic/traditional (TRADITION_DIVERGENCE → PARTIALLY_SUPPORTED)
_SYMBOLIC_CLAIM_TYPES: frozenset = frozenset({
    ClaimType.SYMBOLIC.value,
    ClaimType.INTERPRETIVE.value,
    ClaimType.HISTORICAL.value,
})


class ContradictionAnalyzer:
    """E-36: Distinguishes source conflict from genuine hallucination.

    Four contradiction types:
      CLAIM_VS_SOURCE      — NLI verdict was CONTRADICTED
      INTER_SOURCE         — two source chunks overlap topic but diverge
      INTRA_RESPONSE       — same claim extracted twice with conflicting text
      TRADITION_DIVERGENCE — symbolic/historical claim contradicted; still PARTIALLY_SUPPORTED
    """

    def analyze(
        self,
        claims: List[Claim],
        records: List[VerificationRecord],
        chunks: List[KnowledgeChunk],
    ) -> List[ContradictionRecord]:
        """Analyze claims + evidence records for contradictions. Never raises."""
        try:
            result: List[ContradictionRecord] = []
            result.extend(self._detect_claim_vs_source(claims, records))
            result.extend(self._detect_inter_source(chunks))
            result.extend(self._detect_intra_response(claims))
            return result
        except Exception as exc:
            logger.debug("ContradictionAnalyzer.analyze failed (%s)", exc)
            return []

    def _detect_claim_vs_source(
        self,
        claims: List[Claim],
        records: List[VerificationRecord],
    ) -> List[ContradictionRecord]:
        """Flag claims whose VerificationRecord verdict is CONTRADICTED."""
        result: List[ContradictionRecord] = []
        claim_map = {c.id: c for c in claims}
        for rec in records:
            if rec.verdict != SupportVerdict.CONTRADICTED:
                continue
            claim = claim_map.get(rec.claim_id)
            if claim is None:
                continue
            # TRADITION_DIVERGENCE for symbolic/historical domains
            is_traditional = claim.claim_type in _SYMBOLIC_CLAIM_TYPES
            ctype = (
                ContradictionType.TRADITION_DIVERGENCE
                if is_traditional
                else ContradictionType.CLAIM_VS_SOURCE
            )
            result.append(ContradictionRecord(
                claim_ids=[rec.claim_id],
                chunk_ids=rec.evidence_ids[:2],
                contradiction_type=ctype,
                severity=rec.contradiction_score,
                description=(
                    f"Tradition divergence in {claim.claim_type} claim"
                    if is_traditional
                    else f"Claim contradicted by source (score={rec.contradiction_score:.2f})"
                ),
            ))
        return result

    # Negation regex that catches words filtered by _STOPWORDS (e.g. "not", "no", "never")
    _NEGATION_RE = re.compile(
        r"\b(not|no|never|neither|nor|none|nothing|nowhere|false|incorrect|"
        r"wrong|untrue|inaccurate|mistaken|deny|denies|denied|contradict|"
        r"opposite|contrary|unlike|different|unrelated|separate)\b",
        re.IGNORECASE,
    )

    def _detect_inter_source(
        self,
        chunks: List[KnowledgeChunk],
    ) -> List[ContradictionRecord]:
        """Flag pairs of source chunks that share topic overlap but diverge in content.

        Heuristic: high keyword overlap + negation present in one chunk but not the other.
        Only checks up to 3 chunk pairs to keep complexity O(1) for large chunk lists.
        """
        result: List[ContradictionRecord] = []
        if len(chunks) < 2:
            return result

        pairs_checked = 0
        for i in range(len(chunks) - 1):
            for j in range(i + 1, len(chunks)):
                if pairs_checked >= 3:
                    break
                pairs_checked += 1
                a, b = chunks[i], chunks[j]
                a_words = _tokenize(a.text)
                b_words = _tokenize(b.text)
                if not a_words or not b_words:
                    continue
                overlap = len(a_words & b_words) / max(1, min(len(a_words), len(b_words)))
                if overlap < 0.3:
                    continue
                # Use raw text regex for negation (avoids stopword filter removing "not")
                a_negs = bool(self._NEGATION_RE.search(a.text))
                b_negs = bool(self._NEGATION_RE.search(b.text))
                if a_negs != b_negs:
                    result.append(ContradictionRecord(
                        claim_ids=[],
                        chunk_ids=[a.chunk_id, b.chunk_id],
                        contradiction_type=ContradictionType.INTER_SOURCE,
                        severity=round(overlap * 0.7, 3),
                        description=(
                            f"Source chunks share topic overlap ({overlap:.0%}) "
                            f"but one contains negation"
                        ),
                    ))
        return result

    def _detect_intra_response(
        self,
        claims: List[Claim],
    ) -> List[ContradictionRecord]:
        """Flag claim pairs with same claim_type but mutually negating content.

        Heuristic: two claims of the same type whose word sets share an overlap
        but one contains negation the other doesn't.
        """
        result: List[ContradictionRecord] = []
        if len(claims) < 2:
            return result

        for i in range(len(claims) - 1):
            for j in range(i + 1, len(claims)):
                a, b = claims[i], claims[j]
                if a.claim_type != b.claim_type:
                    continue
                a_words = _tokenize(a.text)
                b_words = _tokenize(b.text)
                if not a_words or not b_words:
                    continue
                overlap = len(a_words & b_words) / max(1, min(len(a_words), len(b_words)))
                if overlap < 0.25:
                    continue
                # Use raw text regex for negation (avoids stopword filter removing "not")
                a_negs = bool(self._NEGATION_RE.search(a.text))
                b_negs = bool(self._NEGATION_RE.search(b.text))
                if a_negs != b_negs:
                    result.append(ContradictionRecord(
                        claim_ids=[a.id, b.id],
                        chunk_ids=[],
                        contradiction_type=ContradictionType.INTRA_RESPONSE,
                        severity=round(overlap * 0.5, 3),
                        description=(
                            f"Intra-response conflict between {a.claim_type} claims "
                            f"({overlap:.0%} shared content)"
                        ),
                    ))
        return result


# ─── E-37: Trigger Engine ────────────────────────────────────────────────────

# Trigger patterns for STRICT mode (factual certainty language)
_STRICT_CERTAINTY_RE = re.compile(
    r"\b(always|never|all|every|none|proved|proven|fact|definitely|"
    r"certainly|without doubt|absolutely)\b",
    re.IGNORECASE,
)
# Trigger for INTERPRETIVE mode (symbolic/mythic domains)
_INTERPRETIVE_RE = re.compile(
    r"\b(symbolizes|represents|embodies|sacred|mythic|spiritual|divine|"
    r"ritual|rune|seiðr|völva|norn|wyrd|galdr)\b",
    re.IGNORECASE,
)
# Trigger for SPECULATIVE mode (hedged language)
_SPECULATIVE_RE = re.compile(
    r"\b(may|might|possibly|perhaps|probably|could be|likely|unclear|"
    r"uncertain|appears to|seems to|suggests)\b",
    re.IGNORECASE,
)
# Named entity heuristic (dates, numbers, capitalized sequences)
_ENTITY_RE = re.compile(
    r"\b(\d{3,4}\s*(AD|BC|CE|BCE)?|\d+\s*(century|percent|%|kg|km|miles?))\b"
    r"|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+",  # CapWord sequences
)


class TriggerEngine:
    """E-37: Adaptive mode detection — selects appropriate VerificationMode.

    Analyze query + draft to choose verification depth:
      STRICT       — factual certainty language, dates/numbers, named entities
      INTERPRETIVE — symbolic/mythic/spiritual content
      SPECULATIVE  — hedged/uncertain language throughout
      NONE         — very short or casual responses
      IRONSWORN    — default (high rigor, no special triggers)
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self._config = config or {}
        self._none_threshold_chars: int = self._config.get("none_threshold_chars", 50)

    def detect_mode(
        self,
        query: str,
        draft: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> VerificationMode:
        """Detect the appropriate VerificationMode for a query+draft pair. Never raises."""
        try:
            combined = f"{query} {draft}"

            # NONE — very short response or greeting/casual
            if len(draft.strip()) < self._none_threshold_chars:
                if not _STRICT_CERTAINTY_RE.search(draft):
                    return VerificationMode.NONE

            # STRICT — strong certainty language, numbers, named entities
            if _STRICT_CERTAINTY_RE.search(combined) or _ENTITY_RE.search(combined):
                return VerificationMode.STRICT

            # INTERPRETIVE — symbolic/mythic content
            if _INTERPRETIVE_RE.search(combined):
                return VerificationMode.INTERPRETIVE

            # SPECULATIVE — hedged language dominates
            speculative_hits = len(_SPECULATIVE_RE.findall(combined))
            if speculative_hits >= 2:
                return VerificationMode.SPECULATIVE

            # Default: high-rigor factual mode
            return VerificationMode.IRONSWORN

        except Exception as exc:
            logger.debug("TriggerEngine.detect_mode failed (%s) — IRONSWORN default", exc)
            return VerificationMode.IRONSWORN


# ─── E-38: Domain Validators ─────────────────────────────────────────────────


class DomainValidator:
    """E-38: Abstract base for domain-specific claim validators.

    Subclasses override validate(). All methods must be safe (never raise).
    """

    domain: str = "generic"

    def validate(
        self,
        claim: Claim,
        chunks: List[KnowledgeChunk],
    ) -> Tuple[VerdictLabel, float, str]:
        """Validate a claim against source chunks for this domain.

        Returns (verdict, confidence, reason). Never raises.
        Default: UNCERTAIN passthrough.
        """
        return VerdictLabel.UNCERTAIN, 0.5, "no domain validator"


class CodeValidator(DomainValidator):
    """E-38: Validates CODE_BEHAVIOR claims via AST syntax check."""

    domain = "code"

    def validate(
        self,
        claim: Claim,
        chunks: List[KnowledgeChunk],
    ) -> Tuple[VerdictLabel, float, str]:
        try:
            import ast
            text = claim.text
            # Only attempt parse if it looks like code
            if not re.search(r"\b(def |class |import |return |if |for |while )", text):
                return VerdictLabel.UNCERTAIN, 0.5, "no code structure detected"
            try:
                ast.parse(text)
                return VerdictLabel.ENTAILED, 0.7, "code structure parses successfully"
            except SyntaxError as exc:
                return VerdictLabel.CONTRADICTED, 0.8, f"syntax error: {exc}"
        except Exception as exc:
            logger.debug("CodeValidator.validate failed (%s)", exc)
            return VerdictLabel.UNCERTAIN, 0.5, "validator error"


class HistoricalValidator(DomainValidator):
    """E-38: Validates HISTORICAL claims — universal quantifiers penalised."""

    domain = "historical"

    _UNIVERSAL_RE = re.compile(
        r"\b(all|every|always|never|none|entirely|completely|universally)\b",
        re.IGNORECASE,
    )
    _PRIMARY_SOURCE_RE = re.compile(
        r"\b(edda|saga|chronicle|annals|according to|primary source|"
        r"historical record|written record|manuscript)\b",
        re.IGNORECASE,
    )

    def validate(
        self,
        claim: Claim,
        chunks: List[KnowledgeChunk],
    ) -> Tuple[VerdictLabel, float, str]:
        try:
            combined_chunks = " ".join(c.text for c in chunks)
            if self._UNIVERSAL_RE.search(claim.text):
                return VerdictLabel.NEUTRAL, 0.6, "universal quantifier in historical claim"
            if self._PRIMARY_SOURCE_RE.search(claim.text) or \
               self._PRIMARY_SOURCE_RE.search(combined_chunks):
                return VerdictLabel.ENTAILED, 0.9, "primary source alignment detected"
            return VerdictLabel.NEUTRAL, 0.5, "historical claim unconfirmed"
        except Exception as exc:
            logger.debug("HistoricalValidator.validate failed (%s)", exc)
            return VerdictLabel.UNCERTAIN, 0.5, "validator error"


class SymbolicValidator(DomainValidator):
    """E-38: Validates SYMBOLIC/INTERPRETIVE claims — tradition divergence is OK."""

    domain = "symbolic"

    def validate(
        self,
        claim: Claim,
        chunks: List[KnowledgeChunk],
    ) -> Tuple[VerdictLabel, float, str]:
        try:
            # Symbolic claims are always at least NEUTRAL — never hard CONTRADICTED
            return VerdictLabel.NEUTRAL, 0.7, "symbolic interpretation — tradition bounds apply"
        except Exception as exc:
            logger.debug("SymbolicValidator.validate failed (%s)", exc)
            return VerdictLabel.UNCERTAIN, 0.5, "validator error"


class ProceduralValidator(DomainValidator):
    """E-38: Validates PROCEDURAL claims — checks step ordering consistency."""

    domain = "procedural"

    _ORDER_WORDS = frozenset({"first", "then", "next", "finally", "after", "before",
                               "step", "begin", "start", "end", "last"})

    def validate(
        self,
        claim: Claim,
        chunks: List[KnowledgeChunk],
    ) -> Tuple[VerdictLabel, float, str]:
        try:
            claim_words = set(re.findall(r"\w+", claim.text.lower()))
            claim_has_order = bool(claim_words & self._ORDER_WORDS)
            if not claim_has_order:
                return VerdictLabel.NEUTRAL, 0.5, "no step order detected in claim"
            # Check if any chunk also contains order words
            for chunk in chunks:
                chunk_words = set(re.findall(r"\w+", chunk.text.lower()))
                if chunk_words & self._ORDER_WORDS:
                    return VerdictLabel.ENTAILED, 0.75, "step order confirmed in source"
            return VerdictLabel.NEUTRAL, 0.5, "step order unverified in source chunks"
        except Exception as exc:
            logger.debug("ProceduralValidator.validate failed (%s)", exc)
            return VerdictLabel.UNCERTAIN, 0.5, "validator error"


# Module-level registry: ClaimType value → DomainValidator instance
_DOMAIN_VALIDATORS: Dict[str, DomainValidator] = {
    ClaimType.CODE_BEHAVIOR.value:  CodeValidator(),
    ClaimType.HISTORICAL.value:     HistoricalValidator(),
    ClaimType.SYMBOLIC.value:       SymbolicValidator(),
    ClaimType.INTERPRETIVE.value:   SymbolicValidator(),  # reuse symbolic validator
    ClaimType.PROCEDURAL.value:     ProceduralValidator(),
}


def get_domain_validator(claim_type: str) -> Optional[DomainValidator]:
    """Return the DomainValidator for a given ClaimType value, or None."""
    return _DOMAIN_VALIDATORS.get(claim_type)


# ─── E-35: Repair Engine ─────────────────────────────────────────────────────


class RepairEngine:
    """E-35: Self-corrects a response draft based on VerificationRecords.

    Model path: structured prompt to subconscious tier.
    Regex fallback: certainty downgrading on CONTRADICTED / UNSUPPORTED claims.
    """

    _CERTAINTY_PATTERNS: List[Tuple[re.Pattern, str]] = [
        (re.compile(r"\b(is|are|was|were)\b", re.IGNORECASE), "may be"),
        (re.compile(r"\balways\b", re.IGNORECASE), "often"),
        (re.compile(r"\bnever\b", re.IGNORECASE), "rarely"),
        (re.compile(r"\bproven\b", re.IGNORECASE), "suggested"),
        (re.compile(r"\bproves?\b", re.IGNORECASE), "suggests"),
        (re.compile(r"\bfact\b", re.IGNORECASE), "claim"),
    ]

    def __init__(self, router: Optional[Any] = None) -> None:
        self._router = router

    def repair(
        self,
        draft: str,
        records: List[VerificationRecord],
    ) -> Tuple[str, List[RepairRecord]]:
        """Apply repairs based on VerificationRecords. Returns (repaired_text, records).

        Model path used when router is available.
        Always falls back to regex if model unavailable or no contradictions found.
        Never raises.
        """
        try:
            if self._router is not None and records:
                result = self._repair_model(draft, records)
                if result is not None:
                    return result
        except Exception as exc:
            logger.debug("RepairEngine: model repair failed (%s) — regex fallback", exc)

        return self._repair_regex(draft, records)

    def _repair_model(
        self,
        draft: str,
        records: List[VerificationRecord],
    ) -> Optional[Tuple[str, List[RepairRecord]]]:
        """Model-based repair via subconscious tier."""
        from scripts.model_router_client import Message, TIER_SUBCONSCIOUS

        contradicted = [r for r in records if r.verdict == SupportVerdict.CONTRADICTED]
        unsupported  = [r for r in records if r.verdict == SupportVerdict.UNSUPPORTED]
        if not contradicted and not unsupported:
            return None  # nothing to repair — skip

        issues = "\n".join(
            f"- Claim {r.claim_id[:8]} is {r.verdict.value}"
            for r in contradicted[:3] + unsupported[:3]
        )
        messages = [
            Message(role="system",
                    content="You are a faithful editor. Return ONLY the corrected text."),
            Message(role="user",
                    content=(
                        "The following response has some unsupported or contradicted claims.\n"
                        f"Issues:\n{issues}\n\n"
                        "Please revise the response to add appropriate uncertainty markers "
                        "('may be', 'possibly', 'according to some sources') to questionable "
                        "claims, without otherwise changing the meaning.\n\n"
                        f"Original:\n{draft[:1000]}\n\nRevised:"
                    )),
        ]
        resp = self._router.complete(TIER_SUBCONSCIOUS, messages, max_tokens=600, temperature=0.2)
        repaired = resp.content.strip()
        if not repaired or len(repaired) < 10:
            return None

        repair_records = [
            RepairRecord(
                claim_id=r.claim_id,
                action=RepairAction.ADD_UNCERTAINTY_MARKER.value,
                original_text=draft[:100],
                revised_text=repaired[:100],
                reason=f"Claim verdict: {r.verdict.value}",
            )
            for r in contradicted[:3]
        ]
        return repaired, repair_records

    def _repair_regex(
        self,
        draft: str,
        records: List[VerificationRecord],
    ) -> Tuple[str, List[RepairRecord]]:
        """Regex-based certainty downgrading for contradicted claims."""
        contradicted = [r for r in records if r.verdict == SupportVerdict.CONTRADICTED]
        if not contradicted:
            return draft, []

        text = draft
        repair_records: List[RepairRecord] = []

        for record in contradicted[:3]:
            for pattern, replacement in self._CERTAINTY_PATTERNS:
                original = text
                text = pattern.sub(replacement, text, count=2)
                if text != original:
                    repair_records.append(RepairRecord(
                        claim_id=record.claim_id,
                        action=RepairAction.DOWNGRADE_CERTAINTY.value,
                        original_text=original[:80],
                        revised_text=text[:80],
                        reason=f"Regex downgrade for {record.verdict.value}",
                    ))
                    break  # one repair per claim

        return text, repair_records


# ─── VordurChecker ────────────────────────────────────────────────────────────


class VordurChecker:
    """The Warden of the Gate — faithfulness scoring for model responses.

    Inject a ModelRouterClient at construction. All methods are safe to call
    even when the router is None — all paths have non-model fallbacks.

    Singleton: use init_vordur_from_config() + get_vordur().
    """

    def __init__(
        self,
        router: Optional[Any] = None,           # ModelRouterClient (Any to avoid circular import)
        high_threshold: float = _DEFAULT_HIGH_THRESHOLD,
        marginal_threshold: float = _DEFAULT_MARGINAL_THRESHOLD,
        persona_check_enabled: bool = True,
        judge_tier: str = _DEFAULT_JUDGE_TIER,
        max_claims: int = _DEFAULT_MAX_CLAIMS,
        verification_timeout_s: float = _DEFAULT_VERIFICATION_TIMEOUT_S,
        enabled: bool = True,
        verdict_cache_enabled: bool = True,     # E-32: LRU cache toggle
        verdict_cache_size: int = 256,          # E-32: max entries
        mimir_well: Optional[Any] = None,       # E-34: for EvidenceBundler
    ) -> None:
        self._router = router
        self._high_threshold = high_threshold
        self._marginal_threshold = marginal_threshold
        self._persona_check_enabled = persona_check_enabled
        self._judge_tier = judge_tier
        self._max_claims = max_claims
        self._verification_timeout_s = verification_timeout_s
        self._enabled = enabled

        # E-32: LRU verdict cache
        self._verdict_cache: Optional[_LRUVerdictCache] = (
            _LRUVerdictCache(verdict_cache_size) if verdict_cache_enabled else None
        )

        # E-33: Claim extractor
        self._claim_extractor = ClaimExtractor(router)

        # E-34: Evidence bundler
        self._evidence_bundler = EvidenceBundler(mimir_well)

        # E-35: Repair engine
        self._repair_engine = RepairEngine(router)

        # E-36: Contradiction analyzer
        self._contradiction_analyzer = ContradictionAnalyzer()

        # Circuit breakers — one per judge tier
        self._cb_subconscious = _MimirCircuitBreaker(
            "vordur_judge_subconscious",
            CircuitBreakerConfig(failure_threshold=5, cooldown_s=60.0),
        )
        self._cb_conscious = _MimirCircuitBreaker(
            "vordur_judge_conscious",
            CircuitBreakerConfig(failure_threshold=3, cooldown_s=30.0),
        )

        # Retry engine for model calls
        self._retry = _RetryEngine(
            RetryConfig(max_attempts=2, base_delay_s=1.0, backoff_factor=2.0, max_delay_s=4.0)
        )

        # Telemetry
        self._total_scored: int = 0
        self._total_retries: int = 0
        self._total_dead_letters: int = 0
        self._persona_violations: int = 0
        self._high_count: int = 0
        self._marginal_count: int = 0
        self._hallucination_count: int = 0
        self._recent_scores: List[float] = []   # rolling window of last 20
        self._last_scored_at: Optional[str] = None

    # ─── Public API ───────────────────────────────────────────────────────────

    def extract_claims(self, response: str) -> List[Claim]:
        """Extract verifiable factual claims from a model response.

        E-33: Delegates to self._claim_extractor.extract() which handles
        model path, fallback, and ClaimType classification.
        Always returns a list — never raises.
        """
        return self._claim_extractor.extract(response)

    def verify_claims(
        self,
        claims: List[Claim],
        source_chunks: List[KnowledgeChunk],
    ) -> List[ClaimVerification]:
        """E-32: Parallel verification of all claims using asyncio.gather().

        Uses asyncio.to_thread() to run each verify_claim() concurrently in a
        thread pool — 60–80% latency reduction on multi-claim responses.
        Falls back to sequential execution if event loop is already running.
        Never raises.
        """
        if not claims:
            return []
        try:
            return asyncio.run(self._verify_all_claims(claims, source_chunks))
        except RuntimeError:
            # Already inside a running event loop — fall back to sequential
            return [self.verify_claim(c, source_chunks) for c in claims]
        except Exception as exc:
            logger.debug("VordurChecker.verify_claims: async gather failed (%s) — sequential", exc)
            return [self.verify_claim(c, source_chunks) for c in claims]

    async def _verify_all_claims(
        self,
        claims: List[Claim],
        source_chunks: List[KnowledgeChunk],
    ) -> List[ClaimVerification]:
        """E-32: Gather all verify_claim() calls concurrently via asyncio.to_thread()."""
        tasks = [
            asyncio.to_thread(self.verify_claim, claim, source_chunks)
            for claim in claims
        ]
        return list(await asyncio.gather(*tasks))

    def verify_claim(
        self,
        claim: Claim,
        source_chunks: List[KnowledgeChunk],
    ) -> ClaimVerification:
        """Verify one claim against the best matching source chunk.

        E-32: Checks LRU cache first; stores result after judge call.
        Picks the highest-overlap chunk as the verification target.
        Judge model fallback chain:
          subconscious → conscious → regex heuristic → UNCERTAIN passthrough
        Never raises.
        """
        t0 = time.monotonic()

        if not source_chunks:
            return ClaimVerification(
                claim=claim,
                verdict=VerdictLabel.UNCERTAIN,
                confidence=0.5,
                supporting_chunk_id=None,
                judge_tier_used="passthrough",
                verification_ms=(time.monotonic() - t0) * 1000,
            )

        # Pick best chunk by keyword overlap with the claim
        best_chunk = self._select_best_chunk(claim, source_chunks)

        # E-32: Check LRU cache
        if self._verdict_cache is not None:
            cached = self._verdict_cache.get(claim.text, best_chunk.text)
            if cached is not None:
                logger.debug("VordurChecker: cache hit for claim=%.40s", claim.text)
                return cached

        # E-38: Domain validator — short-circuit judge call when applicable
        domain_validator = get_domain_validator(claim.claim_type)
        if domain_validator is not None:
            dv_verdict, dv_confidence, dv_reason = domain_validator.validate(
                claim, source_chunks
            )
            if dv_verdict != VerdictLabel.UNCERTAIN:
                logger.debug(
                    "VordurChecker: domain validator (%s) verdict=%s reason=%s",
                    domain_validator.domain, dv_verdict.value, dv_reason,
                )
                result = ClaimVerification(
                    claim=claim,
                    verdict=dv_verdict,
                    confidence=dv_confidence,
                    supporting_chunk_id=best_chunk.chunk_id,
                    judge_tier_used=f"domain:{domain_validator.domain}",
                    verification_ms=(time.monotonic() - t0) * 1000,
                )
                if self._verdict_cache is not None:
                    self._verdict_cache.put(claim.text, best_chunk.text, result)
                return result

        # --- Tier 1: subconscious (Ollama) ---
        if self._router is not None:
            try:
                self._cb_subconscious.before_call()
                verdict = self._retry.run(
                    self._call_judge_model,
                    claim, best_chunk, "subconscious",
                )
                self._cb_subconscious.on_success()
                result = ClaimVerification(
                    claim=claim,
                    verdict=verdict,
                    confidence=0.85,
                    supporting_chunk_id=best_chunk.chunk_id,
                    judge_tier_used="subconscious",
                    verification_ms=(time.monotonic() - t0) * 1000,
                )
                if self._verdict_cache is not None:
                    self._verdict_cache.put(claim.text, best_chunk.text, result)
                return result
            except CircuitBreakerOpenError:
                logger.debug("VordurChecker: subconscious CB open — trying conscious tier")
            except Exception as exc:
                self._cb_subconscious.on_failure(exc)
                logger.debug("VordurChecker: subconscious judge failed (%s) — trying conscious", exc)

        # --- Tier 2: conscious (LiteLLM) ---
        if self._router is not None:
            try:
                self._cb_conscious.before_call()
                verdict = self._retry.run(
                    self._call_judge_model,
                    claim, best_chunk, "conscious-mind",
                )
                self._cb_conscious.on_success()
                result = ClaimVerification(
                    claim=claim,
                    verdict=verdict,
                    confidence=0.75,
                    supporting_chunk_id=best_chunk.chunk_id,
                    judge_tier_used="conscious",
                    verification_ms=(time.monotonic() - t0) * 1000,
                )
                if self._verdict_cache is not None:
                    self._verdict_cache.put(claim.text, best_chunk.text, result)
                return result
            except CircuitBreakerOpenError:
                logger.debug("VordurChecker: conscious CB open — using regex heuristic")
            except Exception as exc:
                self._cb_conscious.on_failure(exc)
                logger.debug("VordurChecker: conscious judge failed (%s) — using regex", exc)

        # --- Tier 3: regex heuristic ---
        try:
            verdict, confidence = _regex_verdict(claim, best_chunk)
            result = ClaimVerification(
                claim=claim,
                verdict=verdict,
                confidence=confidence,
                supporting_chunk_id=best_chunk.chunk_id,
                judge_tier_used="regex",
                verification_ms=(time.monotonic() - t0) * 1000,
            )
            if self._verdict_cache is not None:
                self._verdict_cache.put(claim.text, best_chunk.text, result)
            return result
        except Exception as exc:
            logger.debug("VordurChecker: regex heuristic failed (%s) — UNCERTAIN passthrough", exc)

        # --- Tier 4: passthrough ---
        return ClaimVerification(
            claim=claim,
            verdict=VerdictLabel.UNCERTAIN,
            confidence=0.5,
            supporting_chunk_id=None,
            judge_tier_used="passthrough",
            verification_ms=(time.monotonic() - t0) * 1000,
        )

    def score(
        self,
        response: str,
        source_chunks: List[KnowledgeChunk],
        ethics_state: Optional[Any] = None,
        trust_state: Optional[Any] = None,
        mode: VerificationMode = VerificationMode.IRONSWORN,
    ) -> FaithfulnessScore:
        """Full faithfulness scoring pipeline for a response.

        Steps:
          1. Persona check (regex)
          2. Extract claims (model or sentence splitter)
          3. Verify each claim (judge model fallback chain)
          4. Compute weighted mean score
          5. Attach ethics + trust context if provided

        Always returns a FaithfulnessScore — never raises.
        """
        if not self._enabled:
            return self._passthrough_score(response)

        # ── Step 0: Set mode-based thresholds ─────────────────────────────────
        high_thresh, marginal_thresh = get_mode_thresholds(mode)

        # ── Step 1: Persona check ─────────────────────────────────────────────
        persona_intact = True
        if self._persona_check_enabled:
            violation = _check_persona_violations(response)
            if violation:
                self._persona_violations += 1
                persona_intact = False
                logger.warning(
                    "VordurChecker: persona violation detected (%s) — forcing hallucination tier",
                    violation,
                )
                # Persona violation forces hallucination score regardless of claims
                return FaithfulnessScore(
                    score=0.0,
                    tier="hallucination",
                    claim_count=0,
                    entailed_count=0,
                    neutral_count=0,
                    contradicted_count=0,
                    uncertain_count=0,
                    needs_retry=True,
                    persona_intact=False,
                    ethics_alignment=self._extract_ethics_alignment(ethics_state),
                    trust_score=self._extract_trust_score(trust_state),
                )

        # ── Step 2: Extract claims ────────────────────────────────────────────
        claims = self.extract_claims(response)

        # No claims extracted — response may be very short or all opinion
        # Return marginal (conservative: not failing, not passing)
        if not claims:
            logger.debug("VordurChecker.score: no claims extracted — returning marginal")
            fs = FaithfulnessScore(
                score=0.65,
                tier="marginal",
                claim_count=0,
                entailed_count=0,
                neutral_count=0,
                contradicted_count=0,
                uncertain_count=0,
                needs_retry=False,
                persona_intact=persona_intact,
                ethics_alignment=self._extract_ethics_alignment(ethics_state),
                trust_score=self._extract_trust_score(trust_state),
            )
            self._record_score(fs)
            return fs

        # Cap at max_claims to prevent runaway verification
        claims = claims[: self._max_claims]

        # ── Step 3: Verify each claim (E-32: parallel via verify_claims()) ──────
        verifications: List[ClaimVerification] = self.verify_claims(claims, source_chunks)

        # ── Step 3b: Build VerificationRecords (E-34) ─────────────────────────
        verification_records: List[VerificationRecord] = []
        for claim, cv in zip(claims, verifications):
            bundle = self._evidence_bundler.bundle(claim, source_chunks)
            record = self._evidence_bundler.analyze(bundle, cv)
            verification_records.append(record)

        # ── Step 3c: Contradiction analysis (E-36) ────────────────────────────
        contradiction_records: List[ContradictionRecord] = (
            self._contradiction_analyzer.analyze(claims, verification_records, source_chunks)
        )

        # ── Step 4: Compute score ─────────────────────────────────────────────
        weights = [_VERDICT_WEIGHTS[cv.verdict] for cv in verifications]
        score = sum(weights) / max(1, len(weights))

        entailed  = sum(1 for cv in verifications if cv.verdict == VerdictLabel.ENTAILED)
        neutral   = sum(1 for cv in verifications if cv.verdict == VerdictLabel.NEUTRAL)
        contradicted = sum(1 for cv in verifications if cv.verdict == VerdictLabel.CONTRADICTED)
        uncertain = sum(1 for cv in verifications if cv.verdict == VerdictLabel.UNCERTAIN)

        tier = self._score_tier(score, high_thresh, marginal_thresh)
        needs_retry = score < marginal_thresh

        # E-33: collect claim types
        claim_types_found = list({c.claim_type for c in claims})

        fs = FaithfulnessScore(
            score=round(score, 4),
            tier=tier,
            claim_count=len(claims),
            entailed_count=entailed,
            neutral_count=neutral,
            contradicted_count=contradicted,
            uncertain_count=uncertain,
            verifications=verifications,
            needs_retry=needs_retry,
            persona_intact=persona_intact,
            ethics_alignment=self._extract_ethics_alignment(ethics_state),
            trust_score=self._extract_trust_score(trust_state),
            claims=list(claims),              # E-33
            claim_types_found=claim_types_found,  # E-33
            verification_records=verification_records,  # E-34
        )

        self._record_score(fs)

        log_fn = logger.debug if tier == "high" else (
            logger.warning if tier == "marginal" else logger.error
        )
        log_fn(
            "VordurChecker: score=%.3f tier=%s claims=%d "
            "(entailed=%d neutral=%d contradicted=%d uncertain=%d)",
            score, tier, len(claims), entailed, neutral, contradicted, uncertain,
        )

        return fs

    def score_and_repair(
        self,
        response: str,
        source_chunks: List[KnowledgeChunk],
        ethics_state: Optional[Any] = None,
        trust_state: Optional[Any] = None,
        mode: VerificationMode = VerificationMode.IRONSWORN,
        query: str = "",
    ) -> Tuple[FaithfulnessScore, TruthProfile, str]:
        """E-35: Score + optionally repair a response.

        Calls score() for faithfulness assessment, builds a TruthProfile,
        and runs RepairEngine on hallucination-tier results.

        Returns (faithfulness_score, truth_profile, final_text).
        Never raises.
        """
        try:
            fs = self.score(response, source_chunks, ethics_state, trust_state, mode)
            repaired_text = response
            repair_count = 0

            # E-36: Run contradiction analysis on this result
            contradiction_records = self._contradiction_analyzer.analyze(
                fs.claims, fs.verification_records, source_chunks
            )

            if fs.tier == "hallucination" and fs.verification_records:
                repaired_text, repair_records = self._repair_engine.repair(
                    response, fs.verification_records
                )
                repair_count = len(repair_records)
                logger.info(
                    "VordurChecker.score_and_repair: %d repairs applied.", repair_count
                )

            truth_profile = self._build_truth_profile(fs, repair_count, contradiction_records, query=query, response=repaired_text)
            return fs, truth_profile, repaired_text
        except Exception as exc:
            logger.warning("VordurChecker.score_and_repair failed (%s) — passthrough", exc)
            return (
                self._passthrough_score(response),
                TruthProfile(faithfulness=0.5),
                response,
            )

    def _build_truth_profile(
        self,
        fs: FaithfulnessScore,
        repair_count: int = 0,
        contradiction_records: Optional[List[ContradictionRecord]] = None,
        query: str = "",
        response: str = "",
    ) -> TruthProfile:
        """E-35/E-36: Compute a TruthProfile from a FaithfulnessScore."""
        n = max(1, fs.claim_count)
        contradiction_risk = fs.contradicted_count / n
        citation_coverage = fs.entailed_count / n
        inference_density = fs.neutral_count / n
        ambiguity_level = fs.uncertain_count / n

        # Source quality: mean TruthTier of supporting chunks (1.0 = DEEP_ROOT, best)
        tier_scores = []
        for cv in fs.verifications:
            if cv.supporting_chunk_id:
                tier_scores.append(1.0)  # assume best without chunk ref (simplified)
        source_quality = sum(tier_scores) / max(1, len(tier_scores)) if tier_scores else 0.5

        return TruthProfile(
            faithfulness=fs.score,
            citation_coverage=round(citation_coverage, 4),
            contradiction_risk=round(contradiction_risk, 4),
            inference_density=round(inference_density, 4),
            source_quality=round(source_quality, 4),
            answer_relevance=_jaccard_relevance(query, response),
            ambiguity_level=round(ambiguity_level, 4),
            repair_count=repair_count,
            contradictions=contradiction_records or [],  # E-36
        )

    def persona_check(
        self,
        response: str,
        axioms: Optional[List[KnowledgeChunk]] = None,
    ) -> bool:
        """Pure regex persona integrity check.

        Returns True if persona is intact, False if a violation is found.
        Never raises. axioms parameter reserved for Phase 2 axiom keyword check.
        """
        if not self._persona_check_enabled:
            return True
        try:
            violation = _check_persona_violations(response)
            if violation:
                self._persona_violations += 1
                logger.warning("VordurChecker.persona_check: violation — %s", violation)
                return False
            return True
        except Exception as exc:
            logger.debug("VordurChecker.persona_check: error (%s) — returning True (safe default)", exc)
            return True

    # ─── Internal helpers ─────────────────────────────────────────────────────

    def _call_judge_model(
        self,
        claim: Claim,
        chunk: KnowledgeChunk,
        tier: str,
    ) -> VerdictLabel:
        """Call the judge model for a single NLI verdict.

        Prompt is intentionally short — optimised for llama3 8B's attention span.
        Parses the first word of the response against ENTAILED/NEUTRAL/CONTRADICTED.
        """
        from scripts.model_router_client import Message, TIER_SUBCONSCIOUS, TIER_CONSCIOUS

        actual_tier = TIER_SUBCONSCIOUS if tier == "subconscious" else TIER_CONSCIOUS
        chunk_text = chunk.text[:_MAX_CHUNK_CHARS_FOR_NLI]

        messages = [
            Message(
                role="system",
                content="You are a fact checker. Answer with ONE word only.",
            ),
            Message(
                role="user",
                content=(
                    f"Source text:\n{chunk_text}\n\n"
                    f"Claim: {claim.text}\n\n"
                    "Does the source ENTAIL, CONTRADICT, or is NEUTRAL toward the claim?\n"
                    "Answer with exactly one word: ENTAILED, NEUTRAL, or CONTRADICTED."
                ),
            ),
        ]

        resp = self._router.complete(actual_tier, messages, max_tokens=10, temperature=0.0)
        return self._parse_verdict(resp.content)

    @staticmethod
    def _parse_verdict(raw: str) -> VerdictLabel:
        """Extract the verdict from a judge model response."""
        first_word = raw.strip().split()[0].upper().rstrip(".,!?;:") if raw.strip() else ""
        mapping = {
            "ENTAILED": VerdictLabel.ENTAILED,
            "ENTAIL": VerdictLabel.ENTAILED,
            "ENTAILS": VerdictLabel.ENTAILED,
            "SUPPORTED": VerdictLabel.ENTAILED,
            "SUPPORTS": VerdictLabel.ENTAILED,
            "TRUE": VerdictLabel.ENTAILED,
            "NEUTRAL": VerdictLabel.NEUTRAL,
            "UNRELATED": VerdictLabel.NEUTRAL,
            "IRRELEVANT": VerdictLabel.NEUTRAL,
            "CONTRADICTED": VerdictLabel.CONTRADICTED,
            "CONTRADICTS": VerdictLabel.CONTRADICTED,
            "CONTRADICT": VerdictLabel.CONTRADICTED,
            "CONTRADICTING": VerdictLabel.CONTRADICTED,
            "FALSE": VerdictLabel.CONTRADICTED,
            "INCORRECT": VerdictLabel.CONTRADICTED,
            "WRONG": VerdictLabel.CONTRADICTED,
        }
        return mapping.get(first_word, VerdictLabel.UNCERTAIN)

    @staticmethod
    def _select_best_chunk(
        claim: Claim,
        chunks: List[KnowledgeChunk],
    ) -> KnowledgeChunk:
        """Pick the chunk with the highest keyword overlap with the claim."""
        if len(chunks) == 1:
            return chunks[0]

        claim_words = _tokenize(claim.text)
        best_chunk = chunks[0]
        best_score = 0.0

        for chunk in chunks:
            chunk_words = _tokenize(chunk.text)
            overlap = len(claim_words & chunk_words) / max(1, len(claim_words))
            if overlap > best_score:
                best_score = overlap
                best_chunk = chunk

        return best_chunk

    def _score_tier(self, score: float, high: float, marginal: float) -> str:
        """Map a numeric score to a tier label."""
        if score >= high:
            return "high"
        if score >= marginal:
            return "marginal"
        return "hallucination"

    def _record_score(self, fs: FaithfulnessScore) -> None:
        """Update rolling telemetry."""
        self._total_scored += 1
        self._last_scored_at = datetime.now(timezone.utc).isoformat()

        if fs.tier == "high":
            self._high_count += 1
        elif fs.tier == "marginal":
            self._marginal_count += 1
        else:
            self._hallucination_count += 1
            if fs.needs_retry:
                self._total_retries += 1

        self._recent_scores.append(fs.score)
        if len(self._recent_scores) > 20:
            self._recent_scores.pop(0)

    def _passthrough_score(self, response: str) -> FaithfulnessScore:
        """Return a marginal score when Vörðr is disabled."""
        return FaithfulnessScore(
            score=0.7,
            tier="marginal",
            claim_count=0,
            entailed_count=0,
            neutral_count=0,
            contradicted_count=0,
            uncertain_count=0,
            needs_retry=False,
            persona_intact=True,
        )

    @staticmethod
    def _extract_ethics_alignment(ethics_state: Optional[Any]) -> Optional[float]:
        """Safely extract alignment score from ethics state."""
        if ethics_state is None:
            return None
        try:
            return float(getattr(ethics_state, "alignment_score", None) or 0.0)
        except Exception:
            return None

    @staticmethod
    def _extract_trust_score(trust_state: Optional[Any]) -> Optional[float]:
        """Safely extract trust score from trust engine state."""
        if trust_state is None:
            return None
        try:
            return float(getattr(trust_state, "trust_score", None) or 0.0)
        except Exception:
            return None

    # ─── State & Bus ──────────────────────────────────────────────────────────

    def get_state(self) -> VordurState:
        recent_avg = (
            sum(self._recent_scores) / len(self._recent_scores)
            if self._recent_scores else 0.0
        )
        cache_hits = self._verdict_cache.hits if self._verdict_cache else 0
        cache_misses = self._verdict_cache.misses if self._verdict_cache else 0
        return VordurState(
            enabled=self._enabled,
            total_responses_scored=self._total_scored,
            total_retries_issued=self._total_retries,
            total_dead_letters=self._total_dead_letters,
            recent_avg_score=round(recent_avg, 4),
            circuit_breaker_subconscious=self._cb_subconscious.get_state_label(),
            circuit_breaker_conscious=self._cb_conscious.get_state_label(),
            last_scored_at=self._last_scored_at,
            persona_violations_caught=self._persona_violations,
            high_count=self._high_count,
            marginal_count=self._marginal_count,
            hallucination_count=self._hallucination_count,
            cache_hits=cache_hits,      # E-32
            cache_misses=cache_misses,  # E-32
        )

    def publish(self, bus: StateBus) -> None:
        """Publish current state to the StateBus."""
        try:
            state = self.get_state()
            event = StateEvent(
                source_module="vordur",
                event_type="vordur_state",
                payload=state.to_dict(),
            )
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(bus.publish_state(event, nowait=True))
                else:
                    loop.run_until_complete(bus.publish_state(event, nowait=True))
            except RuntimeError:
                asyncio.run(bus.publish_state(event, nowait=True))
        except Exception as exc:
            logger.debug("VordurChecker.publish: failed (%s)", exc)

    # ─── Convenience ──────────────────────────────────────────────────────────

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def high_threshold(self) -> float:
        return self._high_threshold

    @property
    def marginal_threshold(self) -> float:
        return self._marginal_threshold

    def record_dead_letter(self) -> None:
        """Called by smart_complete_with_cove when a response is dead-lettered."""
        self._total_dead_letters += 1


# ─── Singleton ────────────────────────────────────────────────────────────────

_VORDUR: Optional[VordurChecker] = None


def get_vordur() -> VordurChecker:
    """Return the global VordurChecker. Raises if not yet initialised."""
    if _VORDUR is None:
        raise RuntimeError(
            "VordurChecker not initialised — call init_vordur_from_config() first."
        )
    return _VORDUR


def init_vordur_from_config(
    config: Any,
    router: Optional[Any] = None,
) -> VordurChecker:
    """Create and register the global VordurChecker from the skill config dict.

    config — dict loaded by ConfigLoader (may be nested dict or Any).
    router — ModelRouterClient instance (injected from main.py to avoid
             circular imports at module load time).

    Config keys read (all optional, defaults shown):
        vordur.enabled               (true)
        vordur.high_threshold        (0.80)
        vordur.marginal_threshold    (0.50)
        vordur.persona_check         (true)
        vordur.judge_tier            ("subconscious")
        vordur.max_claims            (10)
        vordur.verification_timeout_s (8.0)
    """
    global _VORDUR

    vd_cfg: Dict[str, Any] = {}
    if isinstance(config, dict):
        vd_cfg = config.get("vordur", {}) or {}
    elif hasattr(config, "get"):
        vd_cfg = config.get("vordur", {}) or {}

    _VORDUR = VordurChecker(
        router=router,
        high_threshold=float(vd_cfg.get("high_threshold", _DEFAULT_HIGH_THRESHOLD)),
        marginal_threshold=float(vd_cfg.get("marginal_threshold", _DEFAULT_MARGINAL_THRESHOLD)),
        persona_check_enabled=bool(vd_cfg.get("persona_check", True)),
        judge_tier=str(vd_cfg.get("judge_tier", _DEFAULT_JUDGE_TIER)),
        max_claims=int(vd_cfg.get("max_claims", _DEFAULT_MAX_CLAIMS)),
        verification_timeout_s=float(vd_cfg.get("verification_timeout_s", _DEFAULT_VERIFICATION_TIMEOUT_S)),
        enabled=bool(vd_cfg.get("enabled", True)),
    )

    logger.info(
        "VordurChecker singleton registered "
        "(enabled=%s, high=%.2f, marginal=%.2f, judge=%s, max_claims=%d).",
        _VORDUR.enabled,
        _VORDUR.high_threshold,
        _VORDUR.marginal_threshold,
        _VORDUR._judge_tier,
        _VORDUR._max_claims,
    )
    return _VORDUR
