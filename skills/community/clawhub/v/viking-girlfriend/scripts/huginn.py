"""
huginn.py — Huginn's Ara: The Flight of Thought
================================================

The retrieval orchestrator of the Ørlög Architecture. Named after Odin's
raven Huginn (Thought) who flies across all nine worlds and returns with
exactly the information needed — no more, no less.

HuginnRetriever sits between every user query and the model call.
It detects which knowledge domain the query belongs to, retrieves the most
relevant Ground Truth from MimirWell, simultaneously fetches episodic memory
context, combines both into a single injection-ready context string, and
returns a typed RetrievalResult to the caller.

Four-tier fallback chain (never crashes):
  PRIMARY   : MimirWell ChromaDB semantic search → rerank 50→3
  FALLBACK A: MimirWell BM25 keyword index (ChromaDB circuit breaker open)
  FALLBACK B: Episodic memory only (BM25 also empty)
  FALLBACK C: Empty RetrievalResult (log WARNING, continue)

Domain detection:
  Pure keyword counting — no model call, no cost, instant.
  Scans the query against six domain keyword sets and selects the
  domain with the highest match confidence (≥ 0.05 threshold).
  Below threshold → None (global search, no domain pre-filter).

Memory federation:
  Retrieves from MimirWell (knowledge) and MemoryStore (episodic) in
  a single call, combining both into one context_string for prompt injection.
  MemoryStore failure is non-fatal — episodic context degrades to empty string.

All public methods return valid typed results — never raise to caller.
Circuit breaker protects the full pipeline with 30s cooldown.
RetryEngine wraps each MimirWell call with 2 attempts + jittered backoff.

Norse framing: Huginn flies out at dawn and returns before nightfall.
He brings back what is needed — not everything, just the truth relevant
to this moment. The raven does not guess. He retrieves.
"""

from __future__ import annotations

import asyncio
import logging
import re
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union

from scripts.mimir_well import (
    CircuitBreakerConfig,
    CircuitBreakerOpenError,
    KnowledgeChunk,
    MimirVordurError,
    MimirWell,
    _MimirCircuitBreaker,
    _RetryEngine,
    RetryConfig,
)
from scripts.state_bus import StateBus, StateEvent

logger = logging.getLogger(__name__)

# ─── Constants ────────────────────────────────────────────────────────────────

_DEFAULT_N_INITIAL: int = 50
_DEFAULT_N_FINAL: int = 3
_DOMAIN_CONFIDENCE_THRESHOLD: float = 0.05
_MAX_EPISODIC_CHARS: int = 3000    # cap on episodic context injected
_MAX_KNOWLEDGE_CHARS: int = 6000   # cap on knowledge context injected

# Context section headers
_GROUND_TRUTH_HEADER = "[GROUND TRUTH — retrieved from the Well]"
_MEMORY_HEADER = "[MEMORY — recent episodic context]"


# ─── Error Taxonomy ───────────────────────────────────────────────────────────


class HuginnError(MimirVordurError):
    """Base class for HuginnRetriever errors."""


class HuginnRetrievalFailedError(HuginnError):
    """All retrieval attempts failed."""


class HuginnAllFallbacksExhaustedError(HuginnError):
    """Every fallback level exhausted — returning empty result."""


# ─── Domain Keyword Map ───────────────────────────────────────────────────────

_DOMAIN_KEYWORDS: Dict[str, List[str]] = {
    "norse_spirituality": [
        "rune", "runes", "futhark", "elder futhark", "younger futhark",
        "seidhr", "seidr", "seith", "volva", "volva", "galdr", "galdrabok",
        "blot", "bindrune", "bind rune", "ansuz", "thurisaz", "fehu", "uruz",
        "hagalaz", "tiwaz", "berkanan", "mannaz", "laguz", "ingwaz", "othalan",
        "raidho", "kenaz", "gebo", "wunjo", "nauthiz", "isa", "jera", "eihwaz",
        "perthro", "algiz", "sowilo", "ehwaz", "dagaz", "wyrd", "norn", "norns",
        "freyja", "freyr", "heathen", "asatru", "rokkatru", "nornir", "disir",
        "vaettir", "landvaettir", "hugr", "fylgja", "hamingja", "vitki",
        "trolldom", "trollcraft", "galdor", "spae", "spaework", "utiseta",
        "blot", "sumbel", "symbel", "ve", "votive", "sacrifice",
        "runic", "runecast", "reading runes", "casting runes", "rune meaning",
        "elder futhark", "aett", "freyjas aett", "heimdalls aett", "tyrs aett",
        "voluspa", "poetic edda", "havamal", "sigrdrifumal",
        "witchcraft", "magic", "magick", "sorcery", "spellwork",
    ],
    "norse_mythology": [
        "odin", "thor", "loki", "frigg", "freyr", "freyja", "tyr", "baldur",
        "baldr", "mimir", "heimdall", "skadi", "njord", "idunn", "bragi",
        "forseti", "ullr", "vidar", "vali", "hodr", "hermod",
        "yggdrasil", "world tree", "nine worlds", "asgard", "midgard",
        "jotunheim", "niflheim", "muspelheim", "vanaheim", "alfheim",
        "svartalfheim", "helheim", "nidavellir",
        "valhalla", "einherjar", "valkyrie", "valkyries",
        "ragnarok", "twilight of gods", "fimbulwinter",
        "eddas", "prose edda", "poetic edda", "snorri sturluson",
        "jormungandr", "world serpent", "fenrir", "fenris", "hela", "hel",
        "bifrost", "rainbow bridge", "mjolnir", "gungnir", "draupnir",
        "aesir", "vanir", "jotun", "giants", "frost giants", "fire giants",
        "dwarves", "dark elves", "light elves", "hugin", "munin",
        "sleipnir", "huginn", "muninn", "geri", "freki",
    ],
    "norse_culture": [
        "viking", "vikings", "norse", "scandinavian", "nordic", "norseman",
        "jarl", "thane", "thrall", "karl", "huscarl", "hirdman",
        "longship", "longboat", "drakkar", "knarr", "ship",
        "mead", "mead hall", "longhouse", "great hall",
        "frith", "honor", "honour", "shame", "wergild", "wyrd",
        "thing", "althing", "lawspeaker", "lawman",
        "shield maiden", "shieldmaiden", "skald", "skalds",
        "berserker", "berserk", "ulfhednar",
        "saga", "sagas", "eddic", "skaldic", "kenning",
        "raid", "raiding", "trade", "exploration",
        "norway", "sweden", "denmark", "iceland", "greenland",
        "dublin", "jorvik", "york", "novgorod", "hedeby",
        "9th century", "10th century", "11th century", "viking age",
        "norse society", "daily life", "social structure",
        "bondmaid", "bondmaids", "thralls", "slavery",
        "wedding", "marriage", "family", "clan", "tribe",
        "feast", "feasting", "drinking", "ale", "horn",
    ],
    "coding": [
        "python", "javascript", "typescript", "js", "ts", "rust", "golang",
        "java", "cpp", "csharp", "ruby", "php", "bash", "shell",
        "code", "coding", "programming", "developer", "development",
        "function", "class", "method", "variable", "loop", "recursion",
        "algorithm", "data structure", "array", "list", "dict", "map",
        "database", "sql", "nosql", "query", "schema",
        "api", "rest", "graphql", "endpoint", "request", "response",
        "async", "await", "thread", "process", "concurrency",
        "debug", "debugging", "error", "exception", "traceback", "bug",
        "git", "github", "commit", "branch", "merge", "pull request",
        "docker", "container", "kubernetes", "deployment", "devops",
        "machine learning", "neural network", "llm", "transformer",
        "linux", "terminal", "command line", "bash script",
        "import", "library", "package", "module", "dependency",
        "type hints", "typing", "annotation", "dataclass",
        "test", "unittest", "pytest", "assertion", "mock",
    ],
    "character": [
        "values", "soul", "identity", "who are you", "what do you believe",
        "your philosophy", "your worldview",
        "feel", "feeling", "feelings", "emotion", "emotions", "emotional",
        "personality", "character", "nature", "spirit",
        "honor", "honour", "integrity", "ethics", "morality", "principles",
        "belief", "beliefs", "faith", "spirituality",
        "opinion", "think", "thought", "perspective", "view",
        "relationship", "love", "affection", "loyalty", "trust",
        "anger", "joy", "sadness", "fear", "disgust", "surprise",
        "happy", "sad", "angry", "scared", "excited", "calm",
        "sigrid", "yourself", "your nature", "your soul",
        "desire", "want", "wish", "dream", "hope",
        "memory", "remember", "past", "history", "story",
    ],
    "roleplay": [
        "roleplay", "role play", "rp", "scene", "scenario",
        "play as", "act as", "pretend", "character",
        "bondmaid", "bondmaids", "servant", "handmaiden",
        "gm", "game master", "storyteller", "dungeon master",
        "adventure", "quest", "story", "narrative", "plot",
        "dialogue", "conversation", "interaction",
        "flirt", "flirting", "romance", "intimate", "sensual",
        "viking roleplay", "norse roleplay",
        "npc", "player character",
    ],
}


def _detect_domain(query: str) -> Tuple[Optional[str], float]:
    """Keyword-based domain detection — no model call, instant.

    Returns (domain_name_or_None, confidence_score).
    confidence = matched_keywords / total_query_words
    Returns None if max confidence < _DOMAIN_CONFIDENCE_THRESHOLD.
    """
    if not query.strip():
        return None, 0.0

    query_lower = query.lower()
    query_words = re.findall(r"[a-zA-Z0-9\u00C0-\u024F]+", query_lower)
    if not query_words:
        return None, 0.0

    scores: Dict[str, float] = {}

    for domain, keywords in _DOMAIN_KEYWORDS.items():
        matches = 0
        for kw in keywords:
            # Support multi-word keywords
            if " " in kw:
                if kw in query_lower:
                    matches += len(kw.split())   # weight multi-word matches higher
            elif kw in query_words:
                matches += 1
        confidence = matches / max(1, len(query_words))
        if confidence > 0:
            scores[domain] = confidence

    if not scores:
        return None, 0.0

    best_domain = max(scores, key=lambda d: scores[d])
    best_conf = scores[best_domain]

    if best_conf < _DOMAIN_CONFIDENCE_THRESHOLD:
        return None, best_conf

    logger.debug(
        "HuginnRetriever.detect_domain: '%s' → domain=%s conf=%.3f",
        query[:60], best_domain, best_conf,
    )
    return best_domain, best_conf


# ─── Data Structures ──────────────────────────────────────────────────────────


@dataclass
class RetrievalRequest:
    """Typed API request for HuginnRetriever.retrieve().

    All fields have defaults — minimum viable call is:
        HuginnRetriever.retrieve(RetrievalRequest(query="..."))
    """

    query: str
    n_initial: int = _DEFAULT_N_INITIAL
    n_final: int = _DEFAULT_N_FINAL
    domain: Optional[str] = None        # None → auto-detect from query
    include_episodic: bool = True
    urgency: str = "normal"             # "normal" | "fast" (fast skips rerank)


@dataclass
class RetrievalResult:
    """Typed API response from HuginnRetriever.retrieve()."""

    query: str
    domain: Optional[str]
    knowledge_chunks: List[KnowledgeChunk]
    episodic_context: str
    context_string: str                 # formatted, ready for prompt injection
    retrieval_ms: float
    fallback_used: str                  # "chromadb" | "bm25" | "episodic_only" | "empty"
    domain_detection_confidence: float
    error_context: Optional[str] = None  # set if any fallback was engaged

    def is_empty(self) -> bool:
        return not self.knowledge_chunks and not self.episodic_context.strip()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query[:100],
            "domain": self.domain,
            "chunk_count": len(self.knowledge_chunks),
            "episodic_chars": len(self.episodic_context),
            "context_chars": len(self.context_string),
            "retrieval_ms": round(self.retrieval_ms, 1),
            "fallback_used": self.fallback_used,
            "domain_confidence": round(self.domain_detection_confidence, 3),
            "error_context": self.error_context,
        }


@dataclass
class HuginnState:
    """State snapshot published to StateBus."""

    total_retrievals: int
    total_fallbacks: int
    total_empty_results: int
    avg_retrieval_ms: float
    domain_counts: Dict[str, int]
    circuit_breaker_state: str
    last_retrieved_at: Optional[str]
    fallback_mode_active: bool
    last_domain: Optional[str]
    last_fallback_used: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ─── HuginnRetriever ──────────────────────────────────────────────────────────


class HuginnRetriever:
    """Huginn's Ara — the retrieval flight of the Ørlög Architecture.

    Orchestrates federated retrieval across MimirWell (knowledge) and
    MemoryStore (episodic). Returns a single ready-to-inject RetrievalResult.

    Never raises — every failure path returns a degraded but valid result.
    Singleton: use init_huginn_from_config() + get_huginn().
    """

    def __init__(
        self,
        mimir_well: MimirWell,
        memory_store: Optional[Any] = None,     # MemoryStore — Any to avoid circular import
        n_initial: int = _DEFAULT_N_INITIAL,
        n_final: int = _DEFAULT_N_FINAL,
        domain_detection_enabled: bool = True,
        include_episodic: bool = True,
    ) -> None:
        self._well = mimir_well
        self._memory_store = memory_store
        self._n_initial = n_initial
        self._n_final = n_final
        self._domain_detection_enabled = domain_detection_enabled
        self._include_episodic = include_episodic

        # Circuit breaker for the full retrieval pipeline
        self._cb = _MimirCircuitBreaker(
            "huginn_full",
            CircuitBreakerConfig(failure_threshold=3, cooldown_s=30.0),
        )

        # Retry engine for MimirWell calls
        self._retry = _RetryEngine(
            RetryConfig(max_attempts=2, base_delay_s=0.5, backoff_factor=2.0, max_delay_s=4.0)
        )

        # Telemetry
        self._total_retrievals: int = 0
        self._total_fallbacks: int = 0
        self._total_empty: int = 0
        self._retrieval_times: List[float] = []
        self._domain_counts: Dict[str, int] = {}
        self._last_retrieved_at: Optional[str] = None
        self._last_domain: Optional[str] = None
        self._last_fallback: str = "none"

    # ─── Public API ───────────────────────────────────────────────────────────

    def detect_domain(self, query: str) -> Tuple[Optional[str], float]:
        """Keyword-based domain detection. Returns (domain_or_None, confidence)."""
        if not self._domain_detection_enabled:
            return None, 0.0
        return _detect_domain(query)

    def retrieve(self, request: RetrievalRequest) -> RetrievalResult:
        """Full federated retrieval — Ground Truth + episodic context.

        Fallback chain:
          1. ChromaDB semantic search (via MimirWell) + MemoryStore episodic
          2. BM25 keyword search (if ChromaDB circuit breaker open)
          3. Episodic memory only (if BM25 returns nothing)
          4. Empty result (log WARNING, never raises)
        """
        t0 = time.monotonic()
        self._total_retrievals += 1

        # ── Domain detection ─────────────────────────────────────────────────
        domain = request.domain
        domain_confidence = 0.0

        if domain is None and self._domain_detection_enabled:
            domain, domain_confidence = _detect_domain(request.query)
        elif domain is not None:
            domain_confidence = 1.0   # explicitly specified

        self._last_domain = domain
        if domain:
            self._domain_counts[domain] = self._domain_counts.get(domain, 0) + 1

        # ── Episodic context (non-fatal — always attempt) ─────────────────────
        episodic_ctx = self._fetch_episodic(request)

        # ── Knowledge retrieval — primary + fallback chain ───────────────────
        knowledge_chunks, fallback_used, error_ctx = self._fetch_knowledge(
            request, domain
        )

        # ── Assemble context string ──────────────────────────────────────────
        context_string = self._build_context_string(knowledge_chunks, episodic_ctx)

        elapsed_ms = (time.monotonic() - t0) * 1000
        self._record_retrieval(elapsed_ms, fallback_used, knowledge_chunks, episodic_ctx)

        result = RetrievalResult(
            query=request.query,
            domain=domain,
            knowledge_chunks=knowledge_chunks,
            episodic_context=episodic_ctx,
            context_string=context_string,
            retrieval_ms=elapsed_ms,
            fallback_used=fallback_used,
            domain_detection_confidence=domain_confidence,
            error_context=error_ctx,
        )

        if result.is_empty():
            self._total_empty += 1
            logger.warning(
                "HuginnRetriever: empty result for query='%.60s' — no context available",
                request.query,
            )

        logger.debug(
            "HuginnRetriever.retrieve: domain=%s chunks=%d episodic=%d chars "
            "fallback=%s ms=%.0f",
            domain, len(knowledge_chunks), len(episodic_ctx),
            fallback_used, elapsed_ms,
        )

        return result

    # ─── Retrieval internals ─────────────────────────────────────────────────

    def _fetch_knowledge(
        self,
        request: RetrievalRequest,
        domain: Optional[str],
    ) -> Tuple[List[KnowledgeChunk], str, Optional[str]]:
        """Run the knowledge retrieval fallback chain.

        Returns: (chunks, fallback_used, error_context_or_None)
        """

        # --- PRIMARY: ChromaDB via MimirWell.retrieve() ----------------------
        try:
            self._cb.before_call()
            chunks = self._retry.run(
                self._well.retrieve,
                request.query,
                request.n_initial,
                domain,
            )
            self._cb.on_success()

            if chunks:
                if request.urgency == "fast":
                    # Fast mode: skip rerank, return top-n directly
                    return chunks[: request.n_final], "chromadb", None
                reranked = self._well.rerank(request.query, chunks, n=request.n_final)
                return reranked, "chromadb", None

            # ChromaDB returned empty — fall through to BM25
            logger.debug(
                "HuginnRetriever: ChromaDB returned 0 chunks — trying BM25"
            )

        except CircuitBreakerOpenError as exc:
            logger.debug(
                "HuginnRetriever: ChromaDB CB open (%.1fs remaining) — BM25 fallback",
                exc.cooldown_remaining_s,
            )
        except Exception as exc:
            self._cb.on_failure(exc)
            logger.warning(
                "HuginnRetriever: ChromaDB retrieval failed (%s) — BM25 fallback", exc
            )

        # --- FALLBACK A: BM25 in-memory keyword search -----------------------
        self._total_fallbacks += 1
        try:
            bm25_chunks = self._well._bm25_retrieve(
                request.query, request.n_initial, domain
            )
            if bm25_chunks:
                if request.urgency != "fast":
                    bm25_chunks = self._well.rerank(
                        request.query, bm25_chunks, n=request.n_final
                    )
                else:
                    bm25_chunks = bm25_chunks[: request.n_final]
                logger.info(
                    "HuginnRetriever: BM25 fallback returned %d chunks", len(bm25_chunks)
                )
                return bm25_chunks, "bm25", "ChromaDB unavailable — BM25 keyword fallback used"
        except Exception as exc:
            logger.warning("HuginnRetriever: BM25 fallback failed (%s)", exc)

        # --- FALLBACK B: Episodic memory only — no knowledge chunks ----------
        # (episodic was already fetched — return empty knowledge, use episodic)
        logger.warning(
            "HuginnRetriever: all knowledge retrieval failed — episodic only"
        )
        return [], "episodic_only", "All knowledge retrieval failed — episodic memory only"

    def _fetch_episodic(self, request: RetrievalRequest) -> str:
        """Fetch episodic context from MemoryStore. Non-fatal — returns '' on failure."""
        if not request.include_episodic or not self._include_episodic:
            return ""
        if self._memory_store is None:
            return ""
        try:
            ctx = self._memory_store.get_context(
                query=request.query,
                include_short_term=True,
                include_medium_term=True,
                include_long_term=True,
                include_episodic=True,
            )
            # Cap episodic context length
            if len(ctx) > _MAX_EPISODIC_CHARS:
                ctx = ctx[:_MAX_EPISODIC_CHARS] + "\n[... episodic context truncated]"
            return ctx if ctx and ctx != "[No memory context available]" else ""
        except Exception as exc:
            logger.debug("HuginnRetriever._fetch_episodic: failed (%s) — empty", exc)
            return ""

    def _build_context_string(
        self,
        chunks: List[KnowledgeChunk],
        episodic_ctx: str,
    ) -> str:
        """Assemble the final prompt-injection context string.

        Format:
            [GROUND TRUTH — retrieved from the Well]
            [GT-1] (Source: filename.ext) chunk text...
            [GT-2] ...
            [GT-3] ...

            [MEMORY — recent episodic context]
            episodic context here...
        """
        sections: List[str] = []

        if chunks:
            gt_lines = [_GROUND_TRUTH_HEADER]
            knowledge_chars = 0
            for i, chunk in enumerate(chunks, 1):
                source = chunk.metadata.get("filename", chunk.source_file.split("/")[-1])
                # Truncate very long chunks
                text = chunk.text
                if len(text) > 2500:
                    text = text[:2500] + "..."
                entry = f"[GT-{i}] (Source: {source}) {text}"
                if knowledge_chars + len(entry) > _MAX_KNOWLEDGE_CHARS:
                    break
                gt_lines.append(entry)
                knowledge_chars += len(entry)
            sections.append("\n".join(gt_lines))

        if episodic_ctx.strip():
            sections.append(f"{_MEMORY_HEADER}\n{episodic_ctx}")

        return "\n\n".join(sections) if sections else ""

    # ─── Telemetry ────────────────────────────────────────────────────────────

    def _record_retrieval(
        self,
        elapsed_ms: float,
        fallback_used: str,
        chunks: List[KnowledgeChunk],
        episodic_ctx: str,
    ) -> None:
        self._last_retrieved_at = datetime.now(timezone.utc).isoformat()
        self._last_fallback = fallback_used
        self._retrieval_times.append(elapsed_ms)
        if len(self._retrieval_times) > 50:
            self._retrieval_times.pop(0)

    # ─── State & Bus ──────────────────────────────────────────────────────────

    def get_state(self) -> HuginnState:
        avg_ms = (
            sum(self._retrieval_times) / len(self._retrieval_times)
            if self._retrieval_times else 0.0
        )
        return HuginnState(
            total_retrievals=self._total_retrievals,
            total_fallbacks=self._total_fallbacks,
            total_empty_results=self._total_empty,
            avg_retrieval_ms=round(avg_ms, 1),
            domain_counts=dict(self._domain_counts),
            circuit_breaker_state=self._cb.get_state_label(),
            last_retrieved_at=self._last_retrieved_at,
            fallback_mode_active=self._cb.get_state_label() != "closed",
            last_domain=self._last_domain,
            last_fallback_used=self._last_fallback,
        )

    def publish(self, bus: StateBus) -> None:
        """Publish current state to the StateBus."""
        try:
            event = StateEvent(
                source_module="huginn",
                event_type="huginn_state",
                payload=self.get_state().to_dict(),
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
            logger.debug("HuginnRetriever.publish: failed (%s)", exc)

    # ─── Convenience ──────────────────────────────────────────────────────────

    def set_memory_store(self, memory_store: Any) -> None:
        """Inject MemoryStore after construction (called from main.py)."""
        self._memory_store = memory_store
        logger.debug("HuginnRetriever: MemoryStore injected.")

    @property
    def has_memory_store(self) -> bool:
        return self._memory_store is not None


# ─── Singleton ────────────────────────────────────────────────────────────────

_HUGINN: Optional[HuginnRetriever] = None


def get_huginn() -> HuginnRetriever:
    """Return the global HuginnRetriever. Raises if not yet initialised."""
    if _HUGINN is None:
        raise RuntimeError(
            "HuginnRetriever not initialised — call init_huginn_from_config() first."
        )
    return _HUGINN


def init_huginn_from_config(
    config: Any,
    mimir_well: MimirWell,
    memory_store: Optional[Any] = None,
) -> HuginnRetriever:
    """Create and register the global HuginnRetriever from the skill config dict.

    config      — dict loaded by ConfigLoader.
    mimir_well  — MimirWell singleton (must already be initialised).
    memory_store — MemoryStore singleton (optional, inject later via set_memory_store()).

    Config keys read (all optional):
        huginn.n_initial            (50)
        huginn.n_final              (3)
        huginn.domain_detection     (true)
        huginn.include_episodic     (true)
    """
    global _HUGINN

    hg_cfg: Dict[str, Any] = {}
    if isinstance(config, dict):
        hg_cfg = config.get("huginn", {}) or {}
    elif hasattr(config, "get"):
        hg_cfg = config.get("huginn", {}) or {}

    _HUGINN = HuginnRetriever(
        mimir_well=mimir_well,
        memory_store=memory_store,
        n_initial=int(hg_cfg.get("n_initial", _DEFAULT_N_INITIAL)),
        n_final=int(hg_cfg.get("n_final", _DEFAULT_N_FINAL)),
        domain_detection_enabled=bool(hg_cfg.get("domain_detection", True)),
        include_episodic=bool(hg_cfg.get("include_episodic", True)),
    )

    logger.info(
        "HuginnRetriever singleton registered "
        "(n_initial=%d, n_final=%d, domain_detection=%s, episodic=%s).",
        _HUGINN._n_initial,
        _HUGINN._n_final,
        _HUGINN._domain_detection_enabled,
        _HUGINN.has_memory_store,
    )
    return _HUGINN
