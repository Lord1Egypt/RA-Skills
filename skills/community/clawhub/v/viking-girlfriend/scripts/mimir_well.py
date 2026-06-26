"""
mimir_well.py — Mímisbrunnr: The Ground Truth Well
====================================================

The deep knowledge store of the Ørlög Architecture. Indexes all
knowledge_reference/ files plus identity anchor files (core_identity.md,
SOUL.md, values.json, AGENTS.md) into ChromaDB with a three-level hierarchy.

  Level 1 — Raw    : Individual document chunks (≤512 tokens / ~2 048 chars)
  Level 2 — Cluster: Domain thematic summaries (auto-generated at ingest)
  Level 3 — Axiom  : Core identity truths (identity files only)

Resilience layers:
  - ChromaDB reads/writes each protected by a named circuit breaker
  - Jittered exponential backoff RetryEngine on all ChromaDB calls
  - Fallback A: in-memory BM25-style keyword index (no ChromaDB required)
  - Fallback B: empty list  (caller handles gracefully — never crashes)
  - Self-healing: reindex() detects interrupted ingest via lock file and
    auto-triggers a clean rebuild. Called by MimirHealthMonitor on corruption.

Norse framing: Odin gave an eye to drink from this Well — wisdom
extracted at great cost becomes infallible Ground Truth. We give it
our knowledge files and drink back only verified fact.
"""

from __future__ import annotations

import asyncio
import json
import logging
import math
import random
import re
import threading
import time
import uuid
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum, IntEnum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import yaml

from scripts.state_bus import StateBus, StateEvent

logger = logging.getLogger(__name__)

# ─── Constants ────────────────────────────────────────────────────────────────

_CHARS_PER_TOKEN: int = 4          # rough approximation: 1 token ≈ 4 chars
_DEFAULT_CHUNK_SIZE_TOKENS: int = 512
_DEFAULT_OVERLAP_TOKENS: int = 64
_DEFAULT_COLLECTION: str = "mimir_well"
_DEFAULT_PERSIST_DIR: str = "data/chromadb_mimir"
_DEFAULT_N_RETRIEVE: int = 50
_DEFAULT_N_FINAL: int = 3
_LOCK_FILE_NAME: str = ".mimir_ingest_lock"
_MAX_JSONL_ITEMS_PER_FILE: int = 200   # cap on JSONL chunks to keep index manageable
_MAX_CSV_ROWS_PER_CHUNK: int = 20
_CLUSTER_MIN_CHUNKS: int = 5          # min chunks in a domain before cluster is created


# ─── Error Taxonomy ───────────────────────────────────────────────────────────


class MimirVordurError(Exception):
    """Base class for all Mímir-Vörðr system errors."""


class MimirWellError(MimirVordurError):
    """Base class for MimirWell-specific errors."""


class ChromaDBUnavailableError(MimirWellError):
    """ChromaDB is unreachable or failed to initialise."""


class ChromaDBCorruptionError(MimirWellError):
    """ChromaDB collection appears to be corrupt or unexpectedly empty."""


class IngestError(MimirWellError):
    """An unrecoverable error occurred during knowledge ingest."""


class RetrievalTimeoutError(MimirWellError):
    """A retrieval operation timed out."""


class CircuitBreakerOpenError(MimirVordurError):
    """Circuit breaker is open — fast-fail, never retry this exception."""

    def __init__(self, component: str, cooldown_remaining_s: float = 0.0) -> None:
        self.component = component
        self.cooldown_remaining_s = cooldown_remaining_s
        super().__init__(
            f"Circuit breaker '{component}' is OPEN "
            f"({cooldown_remaining_s:.1f}s remaining in cooldown)"
        )


# ─── Circuit Breaker ──────────────────────────────────────────────────────────


class _CBState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class DataRealm(Enum):
    """The Nine Worlds of Data classification."""

    ASGARD = "asgard"           # Core Axioms / Identity
    MIDGARD = "midgard"         # Historical / General Facts
    VANAHEIM = "vanaheim"       # Speculative / Vibe / Intuition
    SVARTALFHEIM = "svartalfheim"  # Code / Technical / Procedure
    JOTUNHEIM = "jotunheim"     # External / User Input / Unverified
    HEL = "hel"                 # Banned / Hallucination Patterns


class TruthTier(IntEnum):
    """The Roots of Yggdrasil hierarchy of authority."""

    DEEP_ROOT = 1    # Primary Sources (Eddas, Sagas, Core Laws)
    TRUNK = 2        # Secondary Sources (Hand-crafted Knowledge)
    BRANCH = 3       # Tertiary Sources (AI-generated, Scraped)


@dataclass
class CircuitBreakerConfig:
    """Configuration for a single _MimirCircuitBreaker instance."""

    failure_threshold: int = 3      # failures before tripping OPEN
    success_threshold: int = 2      # consecutive successes to re-CLOSE from HALF_OPEN
    cooldown_s: float = 30.0        # seconds to wait before HALF_OPEN probe


class _MimirCircuitBreaker:
    """Three-state circuit breaker. Thread-safe via threading.Lock.

    Usage:
        breaker.before_call()           # raises CircuitBreakerOpenError if OPEN
        try:
            result = risky_operation()
            breaker.on_success()
        except Exception as exc:
            breaker.on_failure(exc)
            raise
    """

    def __init__(
        self,
        name: str,
        config: Optional[CircuitBreakerConfig] = None,
    ) -> None:
        self._name = name
        self._cfg = config or CircuitBreakerConfig()
        self._state = _CBState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._opened_at: Optional[float] = None
        self._lock = threading.Lock()

    # ── State probes ──────────────────────────────────────────────────────────

    def _can_probe(self) -> bool:
        """True if cooldown has elapsed and a half-open probe is allowed."""
        if self._state != _CBState.OPEN or self._opened_at is None:
            return False
        return (time.monotonic() - self._opened_at) >= self._cfg.cooldown_s

    def before_call(self) -> None:
        """Call before every attempt. Raises CircuitBreakerOpenError when OPEN."""
        with self._lock:
            if self._state == _CBState.OPEN:
                if self._can_probe():
                    self._state = _CBState.HALF_OPEN
                    logger.debug(
                        "CircuitBreaker '%s': entering HALF_OPEN probe", self._name
                    )
                else:
                    elapsed = time.monotonic() - (self._opened_at or 0.0)
                    remaining = max(0.0, self._cfg.cooldown_s - elapsed)
                    raise CircuitBreakerOpenError(self._name, remaining)

    def on_success(self) -> None:
        """Record a successful call. May close an open breaker."""
        with self._lock:
            if self._state == _CBState.HALF_OPEN:
                self._success_count += 1
                if self._success_count >= self._cfg.success_threshold:
                    self._state = _CBState.CLOSED
                    self._failure_count = 0
                    self._success_count = 0
                    self._opened_at = None
                    logger.info(
                        "CircuitBreaker '%s': CLOSED — service recovered", self._name
                    )
            elif self._state == _CBState.CLOSED:
                self._failure_count = 0

    def on_failure(self, exc: Exception) -> None:
        """Record a failed call. May trip the breaker OPEN."""
        with self._lock:
            self._failure_count += 1
            self._success_count = 0
            if self._failure_count >= self._cfg.failure_threshold:
                if self._state != _CBState.OPEN:
                    self._state = _CBState.OPEN
                    self._opened_at = time.monotonic()
                    logger.warning(
                        "CircuitBreaker '%s': OPEN after %d failures — last: %s",
                        self._name,
                        self._failure_count,
                        exc,
                    )

    def reset(self) -> None:
        """Manually reset to CLOSED. Used by health monitor after reindex."""
        with self._lock:
            self._state = _CBState.CLOSED
            self._failure_count = 0
            self._success_count = 0
            self._opened_at = None
        logger.info("CircuitBreaker '%s': manually reset to CLOSED", self._name)

    def get_state_label(self) -> str:
        with self._lock:
            if self._state == _CBState.OPEN and self._can_probe():
                return "half_open"
            return self._state.value

    def to_dict(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "name": self._name,
                "state": self.get_state_label(),
                "failure_count": self._failure_count,
                "cooldown_s": self._cfg.cooldown_s,
            }


# ─── Retry Engine ─────────────────────────────────────────────────────────────


@dataclass
class RetryConfig:
    """Configuration for a _RetryEngine instance."""

    max_attempts: int = 3
    base_delay_s: float = 0.5
    backoff_factor: float = 2.0
    max_delay_s: float = 8.0
    jitter: bool = True             # adds random ±20% variation to delay


_NEVER_RETRY: Tuple[Type[Exception], ...] = (CircuitBreakerOpenError,)


class _RetryEngine:
    """Synchronous retry engine with jittered exponential backoff.

    Automatically skips retry for CircuitBreakerOpenError (and any
    caller-supplied non-retriable exceptions) since those are structural
    failures, not transient ones.
    """

    def __init__(
        self,
        config: Optional[RetryConfig] = None,
    ) -> None:
        self._cfg = config or RetryConfig()

    def run(
        self,
        fn: Callable[..., Any],
        *args: Any,
        non_retriable: Tuple[Type[Exception], ...] = (),
        **kwargs: Any,
    ) -> Any:
        """Run fn(*args, **kwargs) with retry. Returns result or re-raises."""
        no_retry = _NEVER_RETRY + tuple(non_retriable)
        last_exc: Optional[Exception] = None

        for attempt in range(1, self._cfg.max_attempts + 1):
            try:
                return fn(*args, **kwargs)
            except no_retry:
                raise
            except Exception as exc:
                last_exc = exc
                if attempt < self._cfg.max_attempts:
                    delay = min(
                        self._cfg.base_delay_s
                        * (self._cfg.backoff_factor ** (attempt - 1)),
                        self._cfg.max_delay_s,
                    )
                    if self._cfg.jitter:
                        delay *= 0.8 + random.random() * 0.4  # nosec B311 - jitter, not cryptographic
                    logger.debug(
                        "RetryEngine: attempt %d/%d failed (%s) — retrying in %.2fs",
                        attempt,
                        self._cfg.max_attempts,
                        exc,
                        delay,
                    )
                    time.sleep(delay)

        raise last_exc  # type: ignore[misc]


# ─── Data Structures ──────────────────────────────────────────────────────────


@dataclass(slots=True)
class KnowledgeChunk:
    """A single knowledge unit stored in MimirWell."""

    chunk_id: str               # uuid4
    text: str                   # raw chunk text (≤512 tokens / ~2048 chars)
    source_file: str            # relative path within data/
    domain: str                 # see _FILE_DOMAIN_MAP
    realm: DataRealm            # Nine Worlds classification
    tier: TruthTier             # Roots of Yggdrasil hierarchy
    level: int                  # 1=raw, 2=cluster, 3=axiom (Legacy)
    metadata: Dict[str, Any]    # position, heading, file_type, etc.

    def to_chroma_metadata(self) -> Dict[str, str]:
        """Convert metadata to ChromaDB-compatible string-only dict."""
        return {
            "source_file": self.source_file,
            "domain": self.domain,
            "realm": self.realm.value,
            "tier": str(self.tier.value),
            "level": str(self.level),
            "file_type": str(self.metadata.get("file_type", "unknown")),
            "heading": str(self.metadata.get("heading", "")),
            "position": str(self.metadata.get("position", 0)),
        }


@dataclass
class IngestReport:
    """Summary of a MimirWell ingest operation."""

    files_processed: int = 0
    chunks_created: int = 0
    chunks_skipped: int = 0
    errors: List[str] = field(default_factory=list)
    duration_s: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MimirState:
    """State snapshot published to StateBus."""

    collection_name: str
    document_count: int
    domain_counts: Dict[str, int]
    last_ingest_at: Optional[str]
    ingest_count: int
    is_healthy: bool
    chromadb_status: str        # "ok" | "degraded" | "down"
    fallback_mode: str          # "chromadb" | "bm25_fast" | "bm25" | "bm25_fallback" | "empty"
    circuit_breaker_read: str
    circuit_breaker_write: str
    bm25_shortcircuit_rate: float = 0.0  # E-26: fraction of queries served by BM25 fast-path
    rag_chunks_blocked: int = 0          # S-01: RAG chunks filtered by injection scan

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ─── Dead-Letter Store ────────────────────────────────────────────────────────


@dataclass
class DeadLetterEntry:
    """One failed-verification record written to the dead-letter log."""

    entry_id: str               # UUID
    timestamp: str              # ISO-8601
    component: str              # "vordur" | "cove" | "huginn" | "smart_complete_with_cove"
    query: str                  # original user query
    response: str               # response that failed verification
    faithfulness_score: float
    error_type: str             # e.g. "HallucinationExhausted"
    retry_count: int
    trace: str                  # full traceback or empty string
    context_chunks: List[str]   # chunk IDs that were retrieved

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class _DeadLetterStore:
    """
    Append-only JSONL log at session/dead_letters.jsonl.
    Thread-safe via a lock.  Never raises — failures are silently logged.
    Provides summary stats for the health monitor.
    """

    def __init__(self, path: Path) -> None:
        self._path = Path(path)
        self._lock = threading.Lock()
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            logger.warning("_DeadLetterStore: could not create directory %s: %s", self._path.parent, exc)

    def append(self, entry: DeadLetterEntry) -> None:
        """Write one entry to the JSONL log, thread-safely.  Never raises."""
        import json  # stdlib — safe local import
        try:
            with self._lock:
                with self._path.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(entry.to_dict()) + "\n")
        except Exception as exc:
            logger.warning("_DeadLetterStore.append failed: %s", exc)

    def count_recent(self, window_s: float = 300.0) -> int:
        """Return count of entries written within the last *window_s* seconds."""
        import json
        cutoff = datetime.now(timezone.utc).timestamp() - window_s
        count = 0
        try:
            with self._lock:
                if not self._path.exists():
                    return 0
                with self._path.open("r", encoding="utf-8") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            obj = json.loads(line)
                            ts = datetime.fromisoformat(obj.get("timestamp", "")).timestamp()
                            if ts >= cutoff:
                                count += 1
                        except Exception as exc:
                            logger.debug("_DeadLetterStore.count_recent: malformed entry skipped: %s", exc)
        except Exception as exc:
            logger.warning("_DeadLetterStore.count_recent failed: %s", exc)
        return count

    def get_last_n(self, n: int = 10) -> List[DeadLetterEntry]:
        """Return up to *n* most recent entries.  Skips corrupt lines silently."""
        import json
        entries: List[DeadLetterEntry] = []
        try:
            with self._lock:
                if not self._path.exists():
                    return []
                with self._path.open("r", encoding="utf-8") as fh:
                    lines = fh.readlines()
            for line in reversed(lines):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    entries.append(DeadLetterEntry(**obj))
                    if len(entries) >= n:
                        break
                except Exception as exc:
                    logger.debug("_DeadLetterStore.get_last_n: malformed entry skipped: %s", exc)
        except Exception as exc:
            logger.warning("_DeadLetterStore.get_last_n failed: %s", exc)
        return entries


# ─── Domain → File Map ────────────────────────────────────────────────────────

# Map of filename -> (domain, realm, tier)
_FILE_TIER_MAP: Dict[str, Tuple[str, DataRealm, TruthTier]] = {
    # Norse Spirituality
    "freyjas_aett_grimoire.md": ("norse_spirituality", DataRealm.ASGARD, TruthTier.DEEP_ROOT),
    "tyrs_aett_grimoire.md": ("norse_spirituality", DataRealm.ASGARD, TruthTier.DEEP_ROOT),
    "heimdalls_aett_grimoire.md": ("norse_spirituality", DataRealm.ASGARD, TruthTier.DEEP_ROOT),
    "yrsas_rune_poems.md": ("norse_spirituality", DataRealm.ASGARD, TruthTier.DEEP_ROOT),
    "galdrabok_reconstruction.json": ("norse_spirituality", DataRealm.ASGARD, TruthTier.DEEP_ROOT),
    "voluspa.json": ("norse_spirituality", DataRealm.ASGARD, TruthTier.DEEP_ROOT),
    "voluspa_the_seeresss_vision_the_ultimate_poetic_rendering.jsonl": ("norse_spirituality", DataRealm.ASGARD, TruthTier.DEEP_ROOT),
    "viking_trolldom_the_ancient_northern_ways.yaml": ("norse_spirituality", DataRealm.MIDGARD, TruthTier.TRUNK),
    "authentic_norse_religious_practices.json": ("norse_spirituality", DataRealm.MIDGARD, TruthTier.TRUNK),
    "9th_century_celtic_pagan_witches.md": ("norse_spirituality", DataRealm.MIDGARD, TruthTier.TRUNK),
    # Norse Mythology
    "norse_gods.json": ("norse_mythology", DataRealm.ASGARD, TruthTier.DEEP_ROOT),
    "poetic_edda_translation.json": ("norse_mythology", DataRealm.ASGARD, TruthTier.DEEP_ROOT),
    # Norse Culture
    "viking_culture_guide.md": ("norse_culture", DataRealm.MIDGARD, TruthTier.TRUNK),
    "viking_history_and_important_events_volume1.jsonl": ("norse_culture", DataRealm.MIDGARD, TruthTier.TRUNK),
    "viking_history.md": ("norse_culture", DataRealm.MIDGARD, TruthTier.TRUNK),
    "ancient_warfare.md": ("norse_culture", DataRealm.MIDGARD, TruthTier.TRUNK),
    # Coding
    "software_engineering.md": ("coding", DataRealm.SVARTALFHEIM, TruthTier.TRUNK),
    "artificial_intelligence.md": ("coding", DataRealm.SVARTALFHEIM, TruthTier.TRUNK),
    "cybersecurity.md": ("coding", DataRealm.SVARTALFHEIM, TruthTier.TRUNK),
}

# Files in data/ root (not knowledge_reference/) that get level=3 axiom status
_IDENTITY_FILES: Dict[str, str] = {
    "core_identity.md": "character",
    "SOUL.md": "character",
    "values.json": "character",
    "AGENTS.md": "character",
}

# Files to skip during ingest (meta/admin files)
_SKIP_FILES: frozenset = frozenset({
    "DOMAIN_PROGRESS.md",
    "KNOWLEDGE_DOMAINS.md",
    "MEMORY.md",
    "README_AI.md",
    "INTERFACE.md",
})


def _detect_domain_from_filename(filename: str) -> str:
    """Keyword-based fallback domain detection for unmapped files."""
    low = filename.lower()
    if any(k in low for k in ("rune", "aett", "gald", "trolld", "paganism", "heathen",
                               "witches", "voluspa", "eddic")):
        return "norse_spirituality"
    if any(k in low for k in ("gods", "goddess", "myth", "edda", "cosmol")):
        return "norse_mythology"
    if any(k in low for k in ("viking", "culture", "honor", "frith", "history",
                               "geography", "social", "city", "sailing", "bondmaid")):
        return "norse_culture"
    if any(k in low for k in ("python", "ai", "code", "software", "cyber",
                               "data_science", "system_admin", "artificial")):
        return "coding"
    if any(k in low for k in ("roleplay", "gm_mindset", "conversation", "flirty",
                               "erotic", "bondmaids")):
        return "roleplay"
    return "norse_culture"   # sensible default


# ─── In-Memory BM25-Style Flat Index ─────────────────────────────────────────


class _FlatIndex:
    """In-memory keyword index for ChromaDB-free fallback retrieval.

    Uses a simplified BM25-inspired scoring:
      score(query, chunk) = Σ_w (tf(w, chunk) / sqrt(len(chunk_words))
                                 * log(1 + N / df(w)))
    Built once at ingest time; rebuilt on reindex.
    Thread-safe reads via per-query immutable snapshot of _entries.
    """

    def __init__(self) -> None:
        self._entries: List[Tuple[str, str, Counter]] = []
        # Each entry: (chunk_id, text, word_counter)
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.Lock()

    def add(self, chunk: KnowledgeChunk) -> None:
        """Add a chunk to the flat index."""
        words = Counter(re.findall(r"[a-zA-Z0-9\u00C0-\u024F]+", chunk.text.lower()))
        with self._lock:
            self._entries.append((chunk.chunk_id, chunk.text, words))
            self._idf_cache.clear()   # invalidate cache on mutation

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()
            self._idf_cache.clear()

    def search(
        self,
        query: str,
        chunks_by_id: Dict[str, KnowledgeChunk],
        n: int = 50,
    ) -> List[KnowledgeChunk]:
        """Return top-n chunks by BM25-style keyword score."""
        results, _ = self.search_with_top_score(query, chunks_by_id, n)
        return results

    def search_with_top_score(
        self,
        query: str,
        chunks_by_id: Dict[str, KnowledgeChunk],
        n: int = 50,
    ) -> Tuple[List[KnowledgeChunk], float]:
        """E-26: Return (top-n chunks, top BM25 score) for shortcircuit detection.

        top_score of 0.0 means no results. Normalised to the first result's score
        — useful as a confidence signal but not a probability.
        """
        if not self._entries:
            return [], 0.0

        query_words = re.findall(r"[a-zA-Z0-9\u00C0-\u024F]+", query.lower())
        if not query_words:
            return [], 0.0

        with self._lock:
            entries = list(self._entries)
            n_docs = len(entries)

        # Compute IDF for each query word
        idfs: Dict[str, float] = {}
        for qw in set(query_words):
            if qw in self._idf_cache:
                idfs[qw] = self._idf_cache[qw]
            else:
                df = sum(1 for _, _, wc in entries if qw in wc)
                idf = math.log(1.0 + n_docs / (1 + df))
                idfs[qw] = idf

        scored: List[Tuple[float, str]] = []
        for chunk_id, _text, word_counter in entries:
            total_words = max(1, sum(word_counter.values()))
            score = sum(
                (word_counter.get(qw, 0) / total_words) * idfs.get(qw, 0.0)
                for qw in query_words
            )
            if score > 0.0:
                scored.append((score, chunk_id))

        if not scored:
            return [], 0.0

        scored.sort(key=lambda x: x[0], reverse=True)
        top_score = scored[0][0]

        result: List[KnowledgeChunk] = []
        for _, cid in scored[:n]:
            chunk = chunks_by_id.get(cid)
            if chunk is not None:
                result.append(chunk)
        return result, top_score

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._entries)


# ─── Chunker ─────────────────────────────────────────────────────────────────


class _Chunker:
    """Splits raw file content into KnowledgeChunk objects.

    Supports: .md, .txt, .json, .jsonl, .yaml/.yml, .csv
    Each chunk targets chunk_size_chars characters with overlap_chars overlap.
    """

    def __init__(
        self,
        chunk_size_tokens: int = _DEFAULT_CHUNK_SIZE_TOKENS,
        overlap_tokens: int = _DEFAULT_OVERLAP_TOKENS,
    ) -> None:
        self._max_chars = chunk_size_tokens * _CHARS_PER_TOKEN
        self._overlap_chars = overlap_tokens * _CHARS_PER_TOKEN

    def chunk_file(
        self,
        path: Path,
        source_rel: str,
        domain: str,
        realm: "DataRealm" = None,   # type: ignore[assignment]
        tier: "TruthTier" = None,    # type: ignore[assignment]
        level: int = 1,
    ) -> List[KnowledgeChunk]:
        """Dispatch to the correct chunking strategy based on extension."""
        # Provide safe defaults if realm/tier not supplied (legacy callers)
        if realm is None:
            realm = DataRealm.MIDGARD
        if tier is None:
            tier = TruthTier.BRANCH
        ext = path.suffix.lower()
        try:
            raw = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            try:
                raw = path.read_text(encoding="latin-1")
            except Exception as exc:
                logger.warning("_Chunker: cannot read %s: %s", path.name, exc)
                return []
        except Exception as exc:
            logger.warning("_Chunker: cannot read %s: %s", path.name, exc)
            return []

        if ext in (".md", ".txt"):
            return self._chunk_markdown(raw, source_rel, domain, realm, tier, level, path.name)
        if ext == ".json":
            return self._chunk_json(raw, source_rel, domain, realm, tier, level, path.name)
        if ext == ".jsonl":
            return self._chunk_jsonl(raw, source_rel, domain, realm, tier, level, path.name)
        if ext in (".yaml", ".yml"):
            return self._chunk_yaml(raw, source_rel, domain, realm, tier, level, path.name)
        if ext == ".csv":
            return self._chunk_csv(raw, source_rel, domain, realm, tier, level, path.name)
        # Unknown format — treat as plain text
        return self._chunk_text_blocks(raw, source_rel, domain, realm, tier, level, path.name, heading="")

    # ── Format-specific chunkers ──────────────────────────────────────────────

    def _chunk_markdown(
        self,
        raw: str,
        source_rel: str,
        domain: str,
        realm: DataRealm,
        tier: TruthTier,
        level: int,
        filename: str,
    ) -> List[KnowledgeChunk]:
        """Split by ## headings, then sub-chunk each section by char count."""
        chunks: List[KnowledgeChunk] = []
        sections = re.split(r"(?m)^(#{1,3}\s+.+)$", raw)
        current_heading = ""
        buffer = ""

        for part in sections:
            if re.match(r"^#{1,3}\s+", part):
                # Flush buffer before new heading
                if buffer.strip():
                    chunks.extend(
                        self._split_text(
                            buffer.strip(), source_rel, domain, realm, tier, level, filename, current_heading
                        )
                    )
                current_heading = part.strip().lstrip("#").strip()
                buffer = part + "\n"
            else:
                buffer += part

        if buffer.strip():
            chunks.extend(
                self._split_text(
                    buffer.strip(), source_rel, domain, realm, tier, level, filename, current_heading
                )
            )

        return chunks

    def _chunk_json(
        self,
        raw: str,
        source_rel: str,
        domain: str,
        realm: DataRealm,
        tier: TruthTier,
        level: int,
        filename: str,
    ) -> List[KnowledgeChunk]:
        """Split JSON by top-level keys (if dict) or items (if list)."""
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # Try BOM-stripped recovery
            try:
                data = json.loads(raw.lstrip("\ufeff"))
            except Exception:
                logger.warning("_Chunker: cannot parse JSON: %s", filename)
                return self._chunk_text_blocks(raw, source_rel, domain, realm, tier, level, filename, "")

        chunks: List[KnowledgeChunk] = []
        if isinstance(data, dict):
            items = [(k, json.dumps(v, ensure_ascii=False)) for k, v in data.items()]
        elif isinstance(data, list):
            items = [(str(i), json.dumps(item, ensure_ascii=False)) for i, item in enumerate(data)]
        else:
            items = [("root", json.dumps(data, ensure_ascii=False))]

        buffer = ""
        buffer_heading = ""
        pos = 0

        for key, val_str in items:
            entry = f'"{key}": {val_str}\n'
            if len(buffer) + len(entry) > self._max_chars and buffer:
                chunks.append(self._make_chunk(buffer.strip(), source_rel, domain, realm, tier,
                                               level, filename, buffer_heading, pos))
                pos += 1
                buffer = entry
                buffer_heading = key
            else:
                if not buffer:
                    buffer_heading = key
                buffer += entry

        if buffer.strip():
            chunks.append(self._make_chunk(buffer.strip(), source_rel, domain, realm, tier,
                                           level, filename, buffer_heading, pos))
        return chunks

    def _chunk_jsonl(
        self,
        raw: str,
        source_rel: str,
        domain: str,
        realm: DataRealm,
        tier: TruthTier,
        level: int,
        filename: str,
    ) -> List[KnowledgeChunk]:
        """Split JSONL by line groups, cap at _MAX_JSONL_ITEMS_PER_FILE chunks."""
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        chunks: List[KnowledgeChunk] = []
        buffer = ""
        pos = 0

        for i, line in enumerate(lines):
            if i >= _MAX_JSONL_ITEMS_PER_FILE * 5:
                # Hard cap: skip remainder of very large files
                logger.debug("_Chunker: capping JSONL at line %d for %s", i, filename)
                break

            if len(buffer) + len(line) + 1 > self._max_chars and buffer:
                chunks.append(self._make_chunk(buffer.strip(), source_rel, domain, realm, tier,
                                               level, filename, f"item_{pos}", pos))
                pos += 1
                buffer = line + "\n"
                if len(chunks) >= _MAX_JSONL_ITEMS_PER_FILE:
                    break
            else:
                buffer += line + "\n"

        if buffer.strip() and len(chunks) < _MAX_JSONL_ITEMS_PER_FILE:
            chunks.append(self._make_chunk(buffer.strip(), source_rel, domain, realm, tier,
                                           level, filename, f"item_{pos}", pos))
        return chunks

    def _chunk_yaml(
        self,
        raw: str,
        source_rel: str,
        domain: str,
        realm: DataRealm,
        tier: TruthTier,
        level: int,
        filename: str,
    ) -> List[KnowledgeChunk]:
        """Split YAML by top-level keys."""
        try:
            data = yaml.safe_load(raw)
        except yaml.YAMLError:
            return self._chunk_text_blocks(raw, source_rel, domain, realm, tier, level, filename, "")

        if not isinstance(data, dict):
            return self._chunk_text_blocks(str(data), source_rel, domain, realm, tier, level, filename, "")

        chunks: List[KnowledgeChunk] = []
        buffer = ""
        buffer_heading = ""
        pos = 0

        for key, val in data.items():
            entry = f"{key}:\n{yaml.dump(val, allow_unicode=True, default_flow_style=False)}\n"
            if len(buffer) + len(entry) > self._max_chars and buffer:
                chunks.append(self._make_chunk(buffer.strip(), source_rel, domain, realm, tier,
                                               level, filename, buffer_heading, pos))
                pos += 1
                buffer = entry
                buffer_heading = str(key)
            else:
                if not buffer:
                    buffer_heading = str(key)
                buffer += entry

        if buffer.strip():
            chunks.append(self._make_chunk(buffer.strip(), source_rel, domain, realm, tier,
                                           level, filename, buffer_heading, pos))
        return chunks

    def _chunk_csv(
        self,
        raw: str,
        source_rel: str,
        domain: str,
        realm: DataRealm,
        tier: TruthTier,
        level: int,
        filename: str,
    ) -> List[KnowledgeChunk]:
        """Split CSV into chunks of _MAX_CSV_ROWS_PER_CHUNK rows each."""
        lines = raw.splitlines()
        if not lines:
            return []
        header = lines[0]
        rows = lines[1:]
        chunks: List[KnowledgeChunk] = []
        pos = 0

        for i in range(0, len(rows), _MAX_CSV_ROWS_PER_CHUNK):
            batch = rows[i: i + _MAX_CSV_ROWS_PER_CHUNK]
            text = header + "\n" + "\n".join(batch)
            chunks.append(self._make_chunk(text.strip(), source_rel, domain, realm, tier,
                                           level, filename, f"rows_{i}", pos))
            pos += 1

        return chunks

    def _chunk_text_blocks(
        self,
        raw: str,
        source_rel: str,
        domain: str,
        realm: DataRealm,
        tier: TruthTier,
        level: int,
        filename: str,
        heading: str,
    ) -> List[KnowledgeChunk]:
        """Generic: split by blank lines (paragraphs), then by char limit."""
        paragraphs = re.split(r"\n\s*\n", raw.strip())
        buffer = ""
        pos = 0
        chunks: List[KnowledgeChunk] = []

        for para in paragraphs:
            if len(buffer) + len(para) + 2 > self._max_chars and buffer:
                chunks.extend(
                    self._split_text(buffer.strip(), source_rel, domain, realm, tier, level, filename, heading)
                )
                pos += len(chunks)
                buffer = para + "\n\n"
            else:
                buffer += para + "\n\n"

        if buffer.strip():
            chunks.extend(
                self._split_text(buffer.strip(), source_rel, domain, realm, tier, level, filename, heading)
            )

        return chunks

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _split_text(
        self,
        text: str,
        source_rel: str,
        domain: str,
        realm: DataRealm,
        tier: TruthTier,
        level: int,
        filename: str,
        heading: str,
    ) -> List[KnowledgeChunk]:
        """Hard-split a text block at max_chars with overlap."""
        if not text:
            return []

        if len(text) <= self._max_chars:
            return [self._make_chunk(text, source_rel, domain, realm, tier, level, filename, heading, 0)]

        chunks: List[KnowledgeChunk] = []
        start = 0
        pos = 0
        while start < len(text):
            end = min(start + self._max_chars, len(text))
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(
                    self._make_chunk(chunk_text, source_rel, domain, realm, tier, level, filename, heading, pos)
                )
                pos += 1
            start = end - self._overlap_chars if end < len(text) else end

        return chunks

    @staticmethod
    def _make_chunk(
        text: str,
        source_rel: str,
        domain: str,
        realm: DataRealm,
        tier: TruthTier,
        level: int,
        filename: str,
        heading: str,
        position: int,
    ) -> KnowledgeChunk:
        return KnowledgeChunk(
            chunk_id=str(uuid.uuid4()),
            text=text,
            source_file=source_rel,
            domain=domain,
            realm=realm,
            tier=tier,
            level=level,
            metadata={
                "file_type": Path(filename).suffix.lower().lstrip("."),
                "heading": heading,
                "position": position,
                "filename": filename,
            },
        )


# ─── LocalOllamaEmbeddingFunction ─────────────────────────────────────────────


class LocalOllamaEmbeddingFunction:
    """Odin's Eye at Mímir's Well — purely local embedding via Ollama.

    Replaces ChromaDB's default embedding (ONNX + potential cloud fallbacks)
    with a local Ollama model (default: nomic-embed-text), ensuring zero
    external API calls in the knowledge retrieval path.

    This closes the Voyage AI privacy leak: OpenClaw's host framework may call
    Voyage AI for its internal memory, but Sigrid's knowledge store is fully
    sovereign when this function is active.

    Graceful degradation: if Ollama is unavailable at construction time,
    `available` is False and MimirWell falls back to ChromaDB's default.
    """

    _ZERO_DIM: int = 768  # nomic-embed-text output dimension

    def __init__(
        self,
        model_name: str = "nomic-embed-text",
        ollama_base_url: str = "http://localhost:11434",
    ) -> None:
        self._model_name = model_name
        self._ollama_base_url = ollama_base_url
        self._available: bool = False
        self._check_availability()

    def _check_availability(self) -> None:
        """Probe Ollama with a minimal call to confirm it is reachable."""
        try:
            import ollama as _ollama  # type: ignore
            _ollama.list()
            self._available = True
            logger.info(
                "LocalOllamaEmbeddingFunction: Ollama reachable — "
                "using %s for local embeddings.",
                self._model_name,
            )
        except Exception as exc:
            logger.warning(
                "LocalOllamaEmbeddingFunction: Ollama unavailable (%s) — "
                "ChromaDB default embedding will be used instead.",
                exc,
            )

    @property
    def available(self) -> bool:
        return self._available

    def __call__(self, input: List[str]) -> List[List[float]]:  # type: ignore[override]
        """Embed a batch of texts via Ollama. Never raises — returns zero-vectors on failure."""
        import ollama as _ollama  # type: ignore
        embeddings: List[List[float]] = []
        for text in input:
            try:
                response = _ollama.embeddings(model=self._model_name, prompt=text)
                embeddings.append(response["embedding"])
            except Exception as exc:
                logger.error(
                    "LocalOllamaEmbeddingFunction: embed failed for segment (%.40s…): %s",
                    text,
                    exc,
                )
                embeddings.append([0.0] * self._ZERO_DIM)
        return embeddings


# ─── MimirWell ────────────────────────────────────────────────────────────────


class MimirWell:
    """Mímisbrunnr — the Ground Truth Well.

    Indexes knowledge files into ChromaDB with in-memory BM25 fallback.
    All public methods are safe to call even when ChromaDB is unavailable.
    Never raises to the caller — all errors are logged and fallbacks engaged.

    Ingest is idempotent: calling ingest_all() on an already-populated
    collection is a no-op unless force=True.

    Singleton: use init_mimir_well_from_config() + get_mimir_well().
    """

    def __init__(
        self,
        collection_name: str = _DEFAULT_COLLECTION,
        persist_dir: Union[str, Path] = _DEFAULT_PERSIST_DIR,
        chunk_size_tokens: int = _DEFAULT_CHUNK_SIZE_TOKENS,
        chunk_overlap_tokens: int = _DEFAULT_OVERLAP_TOKENS,
        n_retrieve: int = _DEFAULT_N_RETRIEVE,
        n_final: int = _DEFAULT_N_FINAL,
        bm25_shortcircuit_threshold: float = 0.75,   # E-26
        session_dir: str = "session",                # E-27
        rag_injection_scan_enabled: bool = True,     # S-01
        use_ollama_embeddings: bool = True,          # S-07: local embedding sovereignty
        ollama_embed_model: str = "nomic-embed-text",  # S-07
        ollama_base_url: str = "http://localhost:11434",  # S-07
    ) -> None:
        self._collection_name = collection_name
        self._persist_dir = Path(persist_dir).resolve()
        self._n_retrieve = n_retrieve
        self._n_final = n_final

        # E-26: BM25 shortcircuit settings + counters
        self._bm25_shortcircuit_threshold: float = bm25_shortcircuit_threshold
        self._bm25_shortcircuit_hits: int = 0
        self._bm25_total_queries: int = 0

        # S-01: RAG injection scan
        self._rag_injection_scan_enabled: bool = rag_injection_scan_enabled
        self._rag_chunks_blocked: int = 0
        self._rag_scanner: Optional[Any] = None  # lazily initialised

        # E-27: axiom integrity
        self._session_dir: Path = Path(session_dir)
        self._axiom_hashes_file: Path = self._session_dir / "axiom_hashes.json"
        self._axiom_hashes: Dict[str, str] = {}
        self._load_axiom_hashes()

        # Infrastructure
        self._chunker = _Chunker(chunk_size_tokens, chunk_overlap_tokens)
        self._flat_index = _FlatIndex()
        self._chunks_by_id: Dict[str, KnowledgeChunk] = {}

        # Circuit breakers
        self._cb_read = _MimirCircuitBreaker(
            "mimir_chromadb_read",
            CircuitBreakerConfig(failure_threshold=3, cooldown_s=30.0),
        )
        self._cb_write = _MimirCircuitBreaker(
            "mimir_chromadb_write",
            CircuitBreakerConfig(failure_threshold=3, cooldown_s=60.0),
        )

        # Retry engines
        self._retry_read = _RetryEngine(
            RetryConfig(max_attempts=3, base_delay_s=0.5, backoff_factor=2.0, max_delay_s=4.0)
        )
        self._retry_write = _RetryEngine(
            RetryConfig(max_attempts=3, base_delay_s=1.0, backoff_factor=2.0, max_delay_s=8.0)
        )

        # State tracking
        self._domain_counts: Dict[str, int] = {}
        self._last_ingest_at: Optional[str] = None
        self._ingest_count: int = 0
        self._fallback_mode: str = "chromadb"

        # S-07: local embedding sovereignty settings
        self._use_ollama_embeddings: bool = use_ollama_embeddings
        self._ollama_embed_model: str = ollama_embed_model
        self._ollama_base_url: str = ollama_base_url

        # ChromaDB
        self._chromadb_available: bool = False
        self._collection = None
        self._init_chromadb()

    # ─── ChromaDB Initialisation ──────────────────────────────────────────────

    def _init_chromadb(self) -> None:
        """Attempt to connect to ChromaDB. Degrades gracefully on failure.

        S-07: If use_ollama_embeddings is True, tries to wire in
        LocalOllamaEmbeddingFunction (nomic-embed-text) for fully local,
        sovereign embeddings. Falls back to ChromaDB's default ONNX embedding
        if Ollama is unreachable — never blocks startup.
        """
        try:
            import chromadb  # type: ignore

            self._persist_dir.mkdir(parents=True, exist_ok=True)
            client = chromadb.PersistentClient(path=str(self._persist_dir))

            # S-07: try local Ollama embedding first
            embedding_fn = None
            if self._use_ollama_embeddings:
                ollama_ef = LocalOllamaEmbeddingFunction(
                    model_name=self._ollama_embed_model,
                    ollama_base_url=self._ollama_base_url,
                )
                if ollama_ef.available:
                    embedding_fn = ollama_ef
                    logger.info(
                        "MimirWell: using local Ollama embedding (%s) — "
                        "zero external API calls for embeddings.",
                        self._ollama_embed_model,
                    )
                else:
                    logger.warning(
                        "MimirWell: Ollama embedding unavailable — "
                        "falling back to ChromaDB default ONNX embedding."
                    )

            self._collection = client.get_or_create_collection(
                name=self._collection_name,
                embedding_function=embedding_fn,  # None = ChromaDB default ONNX
                metadata={"hnsw:space": "cosine"},
            )
            self._chromadb_available = True
            logger.info(
                "MimirWell: ChromaDB collection '%s' ready at '%s'.",
                self._collection_name,
                self._persist_dir,
            )
        except ImportError:
            logger.warning(
                "MimirWell: chromadb not installed — using BM25 keyword fallback only. "
                "Install with: pip install chromadb"
            )
            self._fallback_mode = "bm25"
        except Exception as exc:
            logger.warning(
                "MimirWell: ChromaDB init failed (%s) — BM25 fallback active.", exc
            )
            self._fallback_mode = "bm25"

    # ─── Lock File Management ─────────────────────────────────────────────────

    def _lock_path(self, data_root: Path) -> Path:
        return data_root / _LOCK_FILE_NAME

    def _set_lock(self, data_root: Path) -> None:
        try:
            self._lock_path(data_root).write_text(
                datetime.now(timezone.utc).isoformat(), encoding="utf-8"
            )
        except Exception as exc:
            logger.debug("MimirWell: could not write lock file: %s", exc)

    def _clear_lock(self, data_root: Path) -> None:
        try:
            lp = self._lock_path(data_root)
            if lp.exists():
                lp.unlink()
        except Exception as exc:
            logger.debug("MimirWell: could not remove lock file: %s", exc)

    def _check_interrupted_ingest(self, data_root: Path) -> bool:
        """Returns True if a previous ingest was interrupted (lock file present)."""
        return self._lock_path(data_root).exists()

    # ─── Ingest ───────────────────────────────────────────────────────────────

    def ingest_all(self, data_root: Path, force: bool = False) -> IngestReport:
        """Index all knowledge files under data_root.

        Idempotent: if ChromaDB already has documents and force=False, returns
        a quick report with 0 chunks ingested.

        force=True: drops and rebuilds the collection from scratch.
        If a lock file is found (interrupted previous ingest), forces a rebuild.
        """
        t0 = time.monotonic()
        report = IngestReport()

        # Detect interrupted previous ingest
        if self._check_interrupted_ingest(data_root):
            logger.warning(
                "MimirWell: previous ingest was interrupted (lock file found) — forcing rebuild."
            )
            force = True

        # Early exit if already populated and not forced
        if not force and self._chromadb_available and self._collection is not None:
            try:
                count = self._collection.count()
                if count > 0:
                    logger.info(
                        "MimirWell: collection already has %d documents — skipping ingest "
                        "(pass force=True to rebuild).",
                        count,
                    )
                    self._last_ingest_at = datetime.now(timezone.utc).isoformat()
                    report.duration_s = time.monotonic() - t0
                    return report
            except Exception as exc:
                logger.debug("MimirWell.ingest: count check failed, proceeding: %s", exc)

        # Force rebuild: drop collection
        if force and self._chromadb_available and self._collection is not None:
            try:
                import chromadb  # type: ignore

                self._collection.delete(where={"domain": {"$ne": "___never___"}})
                logger.info("MimirWell: cleared existing collection for rebuild.")
            except Exception as exc:
                logger.warning("MimirWell: could not clear collection: %s", exc)

        self._flat_index.clear()
        self._chunks_by_id.clear()
        self._domain_counts.clear()

        # Set lock file before starting work
        self._set_lock(data_root)

        try:
            # ── Ingest identity files (level=3, axiom) ────────────────────────
            for fname, domain in _IDENTITY_FILES.items():
                fpath = data_root / fname
                if not fpath.exists():
                    continue
                # Identity files are always ASGARD realm and DEEP_ROOT tier
                chunks = self._chunker.chunk_file(
                    fpath, fname, domain, DataRealm.ASGARD, TruthTier.DEEP_ROOT, level=3
                )
                ingested, errors = self._upsert_chunks(chunks)
                report.files_processed += 1
                report.chunks_created += ingested
                report.errors.extend(errors)

            # ── Ingest knowledge_reference/ files (level=1, raw) ─────────────
            kr_dir = data_root / "knowledge_reference"
            if kr_dir.is_dir():
                for fpath in sorted(kr_dir.iterdir()):
                    if fpath.is_dir():
                        continue  # skip subdirs
                    if fpath.name in _SKIP_FILES:
                        continue
                    if fpath.suffix.lower() not in {
                        ".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".csv"
                    }:
                        continue

                    # Lookup domain, realm, tier from map or fallback
                    mapping = _FILE_TIER_MAP.get(
                        fpath.name.lower(),
                        _FILE_TIER_MAP.get(fpath.name)
                    )
                    
                    if mapping:
                        domain, realm, tier = mapping
                    else:
                        domain = _detect_domain_from_filename(fpath.name)
                        realm = DataRealm.MIDGARD
                        tier = TruthTier.BRANCH  # Default for unmapped/external data

                    source_rel = f"knowledge_reference/{fpath.name}"

                    try:
                        chunks = self._chunker.chunk_file(fpath, source_rel, domain, realm, tier, level=1)
                        ingested, errors = self._upsert_chunks(chunks)
                        report.files_processed += 1
                        report.chunks_created += ingested
                        report.errors.extend(errors)
                        if errors:
                            logger.warning(
                                "MimirWell: %d errors ingesting %s", len(errors), fpath.name
                            )
                    except Exception as exc:
                        err_msg = f"{fpath.name}: {exc}"
                        report.errors.append(err_msg)
                        logger.warning("MimirWell: failed to ingest %s: %s", fpath.name, exc)

        finally:
            # Always clear the lock file — even if ingest partially failed
            self._clear_lock(data_root)

        self._last_ingest_at = datetime.now(timezone.utc).isoformat()
        self._ingest_count += 1
        report.duration_s = time.monotonic() - t0

        # E-27: compute and persist axiom hashes after ingest
        self._axiom_hashes = self._compute_axiom_hashes()
        self._save_axiom_hashes()
        logger.debug(
            "MimirWell: axiom hashes computed (%d DEEP_ROOT/ASGARD chunks).",
            len(self._axiom_hashes),
        )

        logger.info(
            "MimirWell: ingest complete — %d files, %d chunks, %d errors in %.1fs.",
            report.files_processed,
            report.chunks_created,
            len(report.errors),
            report.duration_s,
        )
        return report

    def reindex(self) -> IngestReport:
        """Force a full drop-and-rebuild. Called by MimirHealthMonitor on corruption."""
        logger.info("MimirWell: triggering full reindex...")
        # Find the data root from an existing chunk's source_file (if available)
        # or fall back to the known persist_dir sibling path
        data_root = self._persist_dir.parent
        report = self.ingest_all(data_root, force=True)
        self._cb_read.reset()
        self._cb_write.reset()
        logger.info("MimirWell: reindex complete. Circuit breakers reset.")
        return report

    def _upsert_chunks(
        self, chunks: List[KnowledgeChunk]
    ) -> Tuple[int, List[str]]:
        """Upsert a list of chunks into ChromaDB + flat index. Returns (ingested, errors)."""
        ingested = 0
        errors: List[str] = []

        for chunk in chunks:
            # Always add to flat index (no dependencies, never fails)
            try:
                self._flat_index.add(chunk)
                self._chunks_by_id[chunk.chunk_id] = chunk
                self._domain_counts[chunk.domain] = (
                    self._domain_counts.get(chunk.domain, 0) + 1
                )
            except Exception as exc:
                errors.append(f"flat_index add {chunk.chunk_id}: {exc}")
                continue

            # Upsert to ChromaDB (optional — fallback already has the data)
            if self._chromadb_available and self._collection is not None:
                try:
                    self._cb_write.before_call()

                    def _do_upsert(c: KnowledgeChunk) -> None:
                        self._collection.upsert(  # type: ignore[union-attr]
                            ids=[c.chunk_id],
                            documents=[c.text],
                            metadatas=[c.to_chroma_metadata()],
                        )

                    self._retry_write.run(_do_upsert, chunk)
                    self._cb_write.on_success()
                    ingested += 1
                except CircuitBreakerOpenError:
                    # Breaker is open — count as "ingested" since flat index has it
                    ingested += 1
                except Exception as exc:
                    self._cb_write.on_failure(exc)
                    errors.append(f"chromadb upsert {chunk.source_file}: {exc}")
                    ingested += 1  # flat index is the fallback — still "ingested"
            else:
                ingested += 1

        return ingested, errors

    # ─── S-01: RAG injection scan ─────────────────────────────────────────────

    def _get_rag_scanner(self) -> Optional[Any]:
        """Lazily initialise InjectionScanner for RAG chunk scanning.

        Uses a lazy import to avoid circular-import issues at module load.
        Returns None if the scanner cannot be initialised (graceful degrade).
        """
        if self._rag_scanner is None and self._rag_injection_scan_enabled:
            try:
                from scripts.security import InjectionScanner  # type: ignore
                self._rag_scanner = InjectionScanner()
            except Exception as exc:
                logger.warning(
                    "MimirWell: could not initialise RAG injection scanner: %s — "
                    "RAG scan disabled.", exc,
                )
                self._rag_injection_scan_enabled = False
        return self._rag_scanner

    def _scan_and_filter_chunks(
        self, chunks: List["KnowledgeChunk"]
    ) -> List["KnowledgeChunk"]:
        """S-01: Filter retrieved chunks through InjectionScanner.

        Any chunk whose text triggers a 'block'-severity injection pattern is
        dropped. Warns are logged but the chunk is kept (lower risk).
        Counters are updated; never raises.

        Thurisaz guard at the Well's mouth — no hostile rune-form shall pass
        from the knowledge base into Sigrid's voice.
        """
        if not self._rag_injection_scan_enabled:
            return chunks

        scanner = self._get_rag_scanner()
        if scanner is None:
            return chunks

        clean: List["KnowledgeChunk"] = []
        for chunk in chunks:
            try:
                result = scanner.scan(chunk.text)
                if result.detected:
                    if result.severity == "block":
                        self._rag_chunks_blocked += 1
                        logger.warning(
                            "MimirWell: RAG chunk blocked (id=%s pattern=%r severity=block) "
                            "— injection pattern detected in knowledge source.",
                            chunk.chunk_id, result.pattern_name,
                        )
                        continue  # drop this chunk
                    else:
                        logger.debug(
                            "MimirWell: RAG chunk warn-flagged (id=%s pattern=%r) — kept.",
                            chunk.chunk_id, result.pattern_name,
                        )
            except Exception as exc:
                logger.debug("MimirWell: RAG scan error for chunk %s: %s — chunk kept.", chunk.chunk_id, exc)
            clean.append(chunk)
        return clean

    # ─── Retrieval ────────────────────────────────────────────────────────────

    def retrieve(
        self,
        query: str,
        n: int = _DEFAULT_N_RETRIEVE,
        domain: Optional[str] = None,
        min_tier: TruthTier = TruthTier.BRANCH,
    ) -> List[KnowledgeChunk]:
        """Semantic search over the Well. Never raises — always returns a list.

        E-26: BM25 pre-filter runs first. If top BM25 score exceeds
        bm25_shortcircuit_threshold, returns BM25 results immediately without
        hitting ChromaDB (path="bm25_fast"). Otherwise falls through to ChromaDB
        then BM25 fallback as before.

        Primary: BM25 pre-check → ChromaDB semantic search.
        Fallback A: in-memory BM25 keyword search.
        Fallback B: empty list (logged as warning).
        """
        if not query.strip():
            return []

        self._bm25_total_queries += 1

        # E-26: BM25 pre-filter — compute score first, shortcircuit if confident
        bm25_results, bm25_top = self._bm25_retrieve_with_score(query, n, domain, min_tier)

        if bm25_top > self._bm25_shortcircuit_threshold and bm25_results:
            self._bm25_shortcircuit_hits += 1
            self._fallback_mode = "bm25_fast"
            logger.debug(
                "MimirWell: BM25 shortcircuit (score=%.4f > threshold=%.2f) — "
                "skipping ChromaDB for query=%.60s",
                bm25_top, self._bm25_shortcircuit_threshold, query,
            )
            return self._scan_and_filter_chunks(
                self._tag_retrieval_path(bm25_results, "bm25_fast")
            )

        # Try ChromaDB primary path
        if self._chromadb_available and self._collection is not None:
            try:
                self._cb_read.before_call()
                results = self._retry_read.run(
                    self._chromadb_retrieve, query, n, domain, min_tier
                )
                self._cb_read.on_success()
                self._fallback_mode = "chromadb"
                return self._scan_and_filter_chunks(
                    self._tag_retrieval_path(results, "chromadb")
                )
            except CircuitBreakerOpenError as exc:
                logger.debug(
                    "MimirWell: ChromaDB read circuit breaker open (%s) — using BM25 fallback.",
                    exc.cooldown_remaining_s,
                )
            except Exception as exc:
                self._cb_read.on_failure(exc)
                logger.warning(
                    "MimirWell: ChromaDB retrieve failed (%s) — using BM25 fallback.", exc
                )

        # Fallback A: BM25 keyword search (already computed above)
        if bm25_results:
            self._fallback_mode = "bm25"
            logger.debug(
                "MimirWell: BM25 fallback returned %d results for query=%.60s",
                len(bm25_results), query,
            )
            return self._scan_and_filter_chunks(
                self._tag_retrieval_path(bm25_results, "bm25_fallback")
            )

        # Fallback B: empty
        self._fallback_mode = "empty"
        logger.warning(
            "MimirWell: all retrieval fallbacks exhausted — returning empty context."
        )
        return []

    def _chromadb_retrieve(
        self,
        query: str,
        n: int,
        domain: Optional[str],
        min_tier: TruthTier,
    ) -> List[KnowledgeChunk]:
        """Raw ChromaDB query. Raises on any error (RetryEngine handles retry)."""
        where: Dict[str, Any] = {}
        if domain:
            where["domain"] = domain
        
        # Enforce tier hierarchy: tier <= min_tier (1 is strongest, 3 is weakest)
        # In Chroma where clause, we can filter by multiple conditions if needed.
        # However, simple min_tier logic:
        where["tier"] = {"$lte": str(min_tier.value)}

        query_kwargs: Dict[str, Any] = {
            "query_texts": [query],
            "n_results": min(n, self._collection.count() or 1),  # type: ignore
            "where": where,
        }

        results = self._collection.query(**query_kwargs)  # type: ignore

        chunks: List[KnowledgeChunk] = []
        for doc, meta, cid in zip(
            results.get("documents", [[]])[0],
            results.get("metadatas", [[]])[0],
            results.get("ids", [[]])[0],
        ):
            # Prefer in-memory version (has full Python dict metadata)
            chunk = self._chunks_by_id.get(cid)
            if chunk is None:
                # Reconstruct from ChromaDB result
                chunk = KnowledgeChunk(
                    chunk_id=cid,
                    text=doc or "",
                    source_file=meta.get("source_file", ""),
                    domain=meta.get("domain", ""),
                    level=int(meta.get("level", 1)),
                    realm=DataRealm.MIDGARD,
                    tier=TruthTier.BRANCH,
                    metadata={
                        "file_type": meta.get("file_type", ""),
                        "heading": meta.get("heading", ""),
                        "position": int(meta.get("position", 0)),
                    },
                )
            chunks.append(chunk)

        return chunks

    def _bm25_retrieve(
        self,
        query: str,
        n: int = _DEFAULT_N_RETRIEVE,
        domain: Optional[str] = None,
        min_tier: TruthTier = TruthTier.BRANCH,
    ) -> List[KnowledgeChunk]:
        """BM25-style keyword search over the in-memory flat index.

        Fallback A — no ChromaDB required. Always safe to call.
        Returns up to n results (domain and tier filtered).
        """
        results, _ = self._bm25_retrieve_with_score(query, n, domain, min_tier)
        return results

    def _bm25_retrieve_with_score(
        self,
        query: str,
        n: int = _DEFAULT_N_RETRIEVE,
        domain: Optional[str] = None,
        min_tier: TruthTier = TruthTier.BRANCH,
    ) -> Tuple[List[KnowledgeChunk], float]:
        """E-26: BM25 search returning (results, top_score) for shortcircuit decisions."""
        if self._flat_index.size == 0:
            return [], 0.0

        results, top_score = self._flat_index.search_with_top_score(
            query, self._chunks_by_id, n=n * 5
        )

        # Apply filters
        if domain:
            results = [c for c in results if c.domain == domain]

        # Enforce tier hierarchy
        results = [c for c in results if c.tier <= min_tier]

        return results[:n], top_score

    def _tag_retrieval_path(
        self, chunks: List[KnowledgeChunk], path: str
    ) -> List[KnowledgeChunk]:
        """E-26: Return copies of chunks with retrieval_path set in metadata.

        Uses dataclasses.replace() to avoid mutating the cached chunk objects.
        path values: "bm25_fast" | "chromadb" | "bm25_fallback"
        """
        from dataclasses import replace as dc_replace
        return [
            dc_replace(c, metadata={**c.metadata, "retrieval_path": path})
            for c in chunks
        ]

    # ─── Reranking ────────────────────────────────────────────────────────────

    def rerank(
        self,
        query: str,
        chunks: List[KnowledgeChunk],
        n: int = _DEFAULT_N_FINAL,
    ) -> List[KnowledgeChunk]:
        """Hybrid rerank: 0.7 * keyword_overlap + 0.3 * original_order_bonus.

        Pure Python — never raises. Returns up to n best chunks.
        When ChromaDB is the source, original order already reflects semantic
        similarity, so we boost keyword overlap to refine rather than replace.
        """
        if not chunks:
            return []
        if len(chunks) <= n:
            return chunks

        query_words = frozenset(
            re.findall(r"[a-zA-Z0-9\u00C0-\u024F]+", query.lower())
        )

        scored: List[Tuple[float, int, KnowledgeChunk]] = []
        for idx, chunk in enumerate(chunks):
            chunk_words = frozenset(
                re.findall(r"[a-zA-Z0-9\u00C0-\u024F]+", chunk.text.lower())
            )
            overlap = len(query_words & chunk_words) / max(1, len(query_words))
            order_bonus = 1.0 - (idx / len(chunks))   # earlier = higher
            score = 0.7 * overlap + 0.3 * order_bonus
            scored.append((score, idx, chunk))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, _, c in scored[:n]]

    # ─── Axioms ───────────────────────────────────────────────────────────────

    def get_axioms(self) -> List[KnowledgeChunk]:
        """Return all level=3 (axiom) chunks — Sigrid's non-negotiable core truths.

        Used by VordurChecker for persona consistency validation.
        In V2, axioms are primarily Tier 1 (DEEP_ROOT) in the ASGARD realm.
        """
        # Check in-memory first (fastest)
        axioms = [
            c for c in self._chunks_by_id.values() 
            if c.realm == DataRealm.ASGARD and c.tier == TruthTier.DEEP_ROOT
        ]
        if axioms:
            return axioms

        # ChromaDB query for Asgardian Deep Roots
        if self._chromadb_available and self._collection is not None:
            try:
                self._cb_read.before_call()

                def _query_axioms() -> List[KnowledgeChunk]:
                    count = self._collection.count()  # type: ignore
                    if count == 0:
                        return []
                    return self._chromadb_retrieve(
                        query="core identity values soul Sigrid",
                        n=25,
                        domain=None,
                        min_tier=TruthTier.DEEP_ROOT
                    )

                ax = self._retry_read.run(_query_axioms)
                self._cb_read.on_success()
                return [c for c in ax if c.realm == DataRealm.ASGARD]
            except Exception as exc:
                self._cb_read.on_failure(exc)
                logger.debug("MimirWell.get_axioms: ChromaDB failed (%s) — using BM25.", exc)

        # BM25 fallback
        return self._bm25_retrieve(
            "core identity values soul Sigrid character", 
            n=25, 
            min_tier=TruthTier.DEEP_ROOT
        )

    # ─── Soul Search (S-07 Layer 2) ───────────────────────────────────────────

    def soul_search(self, query: str, n_results: int = 3) -> str:
        """S-07 Layer 2: Retrieve the most relevant soul/identity fragments for this query.

        Used by prompt_synthesizer to inject targeted soul context per turn,
        instead of loading all identity files into the context window every time.
        This keeps context lean while ensuring the right soul fragments are present.

        Searches the ASGARD realm (identity/soul/values axioms) using the query
        for semantic or keyword relevance. Returns a formatted string ready for
        prompt injection — or empty string if nothing is found.

        Yggdrasil's roots drink only what is needed. The Allfather did not carry
        all knowledge of the well — he drew only what the moment required.
        """
        results = self.retrieve(
            query=query,
            n=max(n_results, 5),  # retrieve a few extra, we filter below
            domain=None,
            min_tier=TruthTier.DEEP_ROOT,
        )
        # Filter to ASGARD realm (soul/identity/values) and take top n
        soul_chunks = [c for c in results if c.realm == DataRealm.ASGARD][:n_results]

        if not soul_chunks:
            # Fallback: try get_axioms() which always returns something
            soul_chunks = self.get_axioms()[:n_results]

        if not soul_chunks:
            return ""

        fragments = [
            f"[Soul/{c.domain}] {c.text[:400].strip()}"
            for c in soul_chunks
        ]
        return "\n".join(fragments)

    # ─── Context String ───────────────────────────────────────────────────────

    def get_context_string(self, chunks: List[KnowledgeChunk]) -> str:
        """Format chunks as numbered Ground Truth citations for prompt injection.

        Output format:
            [GROUND TRUTH — retrieved from the Well]
            [GT-1] (Source: freyjas_aett_grimoire.md) ...chunk text...
            [GT-2] ...
        """
        if not chunks:
            return ""

        lines = ["[GROUND TRUTH — retrieved from the Well]"]
        for i, chunk in enumerate(chunks, 1):
            source = chunk.metadata.get("filename", chunk.source_file)
            # Truncate very long chunks for prompt efficiency
            text = chunk.text[:1200] + "..." if len(chunk.text) > 1200 else chunk.text
            lines.append(f"[GT-{i}] (Source: {source}) {text}")

        return "\n".join(lines)

    # ─── Dream Tick Integration ───────────────────────────────────────────────

    def associative_link_pass(
        self,
        session_dir: Optional[Union[str, Path]] = None,
    ) -> List[Tuple[str, str]]:
        """E-15: Find nearest semantic neighbour pairs in the flat index.

        Walks every chunk in the in-memory BM25 flat index and, for each
        chunk, retrieves its single closest neighbour by keyword overlap.
        Unique (a, b) pairs (where a < b by chunk_id) are collected and
        optionally written to ``<session_dir>/association_cache.json``.

        This is a lightweight associative pass — the Well dreams of its own
        contents, drawing threads between distantly related knowledge.  It
        runs once per deep_night entry and is best-effort throughout: any
        exception is caught and logged as WARN so the scheduler is never
        blocked.

        Args:
            session_dir: Optional path to the session directory.  When
                provided the pairs list is persisted as JSON.

        Returns:
            List of ``(chunk_id_a, chunk_id_b)`` string tuples — at most
            one pair per source chunk.  Empty list on failure or empty index.
        """
        try:
            all_ids = list(self._chunks_by_id.keys())
            if not all_ids:
                logger.debug("MimirWell.associative_link_pass: flat index empty — skipping.")
                return []

            pairs: List[Tuple[str, str]] = []
            seen: set = set()

            for chunk_id in all_ids:
                chunk = self._chunks_by_id.get(chunk_id)
                if chunk is None:
                    continue
                # Use a short excerpt as the query to avoid re-chunking costs
                query_text = chunk.text[:200]
                neighbours = self._bm25_retrieve(query_text, n=2, domain=None)
                for neighbour in neighbours:
                    if neighbour.chunk_id == chunk_id:
                        continue
                    # Canonical ordering so (a,b) == (b,a)
                    pair_key = (
                        min(chunk_id, neighbour.chunk_id),
                        max(chunk_id, neighbour.chunk_id),
                    )
                    if pair_key not in seen:
                        seen.add(pair_key)
                        pairs.append(pair_key)
                    break  # one neighbour per source chunk

            logger.info(
                "MimirWell: associative link pass found %d pairs from %d chunks.",
                len(pairs),
                len(all_ids),
            )

            if session_dir is not None and pairs:
                try:
                    cache_path = Path(session_dir) / "association_cache.json"
                    cache_path.parent.mkdir(parents=True, exist_ok=True)
                    payload = {
                        "ts": datetime.now(timezone.utc).isoformat(),
                        "pairs": [[a, b] for a, b in pairs],
                    }
                    cache_path.write_text(
                        json.dumps(payload, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )
                    logger.debug("MimirWell: association_cache written to %s", cache_path)
                except Exception as write_exc:
                    logger.warning(
                        "MimirWell: failed to write association_cache.json: %s", write_exc
                    )

            return pairs
        except Exception as exc:
            logger.warning("MimirWell.associative_link_pass failed: %s", exc)
            return []

    # ─── State & Bus ──────────────────────────────────────────────────────────

    def get_state(self) -> MimirState:
        """Build a current state snapshot."""
        doc_count = 0
        chroma_status = "down"

        if self._chromadb_available and self._collection is not None:
            try:
                doc_count = self._collection.count()
                chroma_status = "ok"
            except Exception:
                chroma_status = "degraded"
        elif self._flat_index.size > 0:
            doc_count = self._flat_index.size
            chroma_status = "down"

        sc_rate = (
            self._bm25_shortcircuit_hits / self._bm25_total_queries
            if self._bm25_total_queries > 0 else 0.0
        )
        return MimirState(
            collection_name=self._collection_name,
            document_count=doc_count,
            domain_counts=dict(self._domain_counts),
            last_ingest_at=self._last_ingest_at,
            ingest_count=self._ingest_count,
            is_healthy=chroma_status != "down" or self._flat_index.size > 0,
            chromadb_status=chroma_status,
            fallback_mode=self._fallback_mode,
            circuit_breaker_read=self._cb_read.get_state_label(),
            circuit_breaker_write=self._cb_write.get_state_label(),
            bm25_shortcircuit_rate=round(sc_rate, 4),  # E-26
            rag_chunks_blocked=self._rag_chunks_blocked,  # S-01
        )

    def publish(self, bus: StateBus) -> None:
        """Publish current state to the StateBus."""
        try:
            state = self.get_state()
            event = StateEvent(
                source_module="mimir_well",
                event_type="mimir_state",
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
            logger.debug("MimirWell.publish: failed to publish state: %s", exc)

    # ─── E-27: Axiom Integrity ────────────────────────────────────────────────

    def check_axiom_integrity(self) -> bool:
        """E-27: Verify that all DEEP_ROOT/ASGARD chunks match their stored hashes.

        Returns True if all hashes match (or if no hashes are stored yet).
        Logs CRITICAL and returns False on any mismatch or missing chunk.
        Never raises.
        """
        if not self._axiom_hashes:
            return True  # no baseline yet — integrity trivially holds
        try:
            current = self._compute_axiom_hashes()
            for cid, expected in self._axiom_hashes.items():
                actual = current.get(cid)
                if actual is None:
                    logger.critical(
                        "MimirWell: Axiom integrity violation — chunk '%s' is missing!", cid
                    )
                    return False
                if actual != expected:
                    logger.critical(
                        "MimirWell: Axiom integrity violation — chunk '%s' hash mismatch "
                        "(expected=%s, got=%s)!",
                        cid, expected[:16], actual[:16],
                    )
                    return False
            return True
        except Exception as exc:
            logger.warning("MimirWell.check_axiom_integrity failed: %s", exc)
            return False

    def _compute_axiom_hashes(self) -> Dict[str, str]:
        """Compute sha256 hashes for all DEEP_ROOT + ASGARD chunks."""
        import hashlib
        result: Dict[str, str] = {}
        for cid, chunk in self._chunks_by_id.items():
            if chunk.tier == TruthTier.DEEP_ROOT and chunk.realm == DataRealm.ASGARD:
                result[cid] = hashlib.sha256(
                    chunk.text.encode("utf-8")
                ).hexdigest()
        return result

    def _save_axiom_hashes(self) -> None:
        """Persist axiom hashes to session/axiom_hashes.json."""
        try:
            self._axiom_hashes_file.parent.mkdir(parents=True, exist_ok=True)
            self._axiom_hashes_file.write_text(
                json.dumps(self._axiom_hashes, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            logger.debug(
                "MimirWell: saved %d axiom hashes to %s.",
                len(self._axiom_hashes), self._axiom_hashes_file,
            )
        except Exception as exc:
            logger.warning("MimirWell._save_axiom_hashes failed: %s", exc)

    def _load_axiom_hashes(self) -> None:
        """Load axiom hashes from session/axiom_hashes.json if present."""
        if not self._axiom_hashes_file.exists():
            return
        try:
            raw = json.loads(self._axiom_hashes_file.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                self._axiom_hashes = raw
            logger.debug(
                "MimirWell: loaded %d axiom hashes from %s.",
                len(self._axiom_hashes), self._axiom_hashes_file,
            )
        except Exception as exc:
            logger.warning("MimirWell._load_axiom_hashes failed: %s", exc)

    # ─── Convenience properties ───────────────────────────────────────────────

    @property
    def chromadb_available(self) -> bool:
        return self._chromadb_available

    @property
    def flat_index_size(self) -> int:
        return self._flat_index.size

    @property
    def collection_name(self) -> str:
        return self._collection_name


# ─── Mímir Health Monitor ─────────────────────────────────────────────────────


@dataclass
class ComponentHealth:
    """Health snapshot for one Mímir-Vörðr component."""

    name: str
    status: str                  # "healthy" | "degraded" | "down"
    circuit_breaker_state: str
    last_success_at: Optional[str]
    last_failure_at: Optional[str]
    failure_rate_5m: float       # failures/minute over last 5 min
    dead_letters_5m: int         # dead-letter entries in last 5 min


@dataclass
class MimirHealthState:
    """Overall health snapshot published to StateBus."""

    overall: str                             # "healthy" | "degraded" | "critical"
    components: Dict[str, ComponentHealth]
    dead_letters_total: int
    last_reindex_at: Optional[str]
    reindex_count: int
    checked_at: str                          # ISO-8601
    axiom_integrity: bool = True             # E-27: False if any axiom hash mismatch

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall": self.overall,
            "dead_letters_total": self.dead_letters_total,
            "last_reindex_at": self.last_reindex_at,
            "reindex_count": self.reindex_count,
            "checked_at": self.checked_at,
            "axiom_integrity": self.axiom_integrity,  # E-27
            "components": {
                k: {
                    "name": v.name,
                    "status": v.status,
                    "circuit_breaker_state": v.circuit_breaker_state,
                    "last_success_at": v.last_success_at,
                    "last_failure_at": v.last_failure_at,
                    "failure_rate_5m": v.failure_rate_5m,
                    "dead_letters_5m": v.dead_letters_5m,
                }
                for k, v in self.components.items()
            },
        }


class MimirHealthMonitor:
    """
    Daemon-thread background watchdog for all Mímir-Vörðr subsystems.

    Runs _health_check() every check_interval_s (default 60 s).
    Runs _full_diagnostics() every diagnostics_interval_s (default 600 s).

    Health checks:
      - MimirWell:  attempt get_state() to confirm singleton alive
      - HuginnRetriever: get_state() alive check
      - VordurChecker:   get_state() alive check
      - CovePipeline:    get_state() alive check
      - Dead-letter rate: if >dead_letter_alert_threshold in 5 min -> WARNING
      - Collection integrity: if doc_count == 0 and auto_reindex -> trigger reindex

    Self-healing:
      - If doc_count == 0: trigger MimirWell.reindex()
      - If dead_letters_5m > 10: CRITICAL log + StateBus alert
    Never raises. All exceptions are caught and logged.
    """

    def __init__(
        self,
        mimir_well: MimirWell,
        vordur: Any,
        huginn: Any,
        cove: Any,
        dead_letter_store: Optional["_DeadLetterStore"],
        bus: Any,
        scheduler: Any = None,
        check_interval_s: float = 60.0,
        diagnostics_interval_s: float = 600.0,
        dead_letter_alert_threshold: int = 5,
        auto_reindex_on_corruption: bool = True,
    ) -> None:
        self._mimir_well = mimir_well
        self._vordur = vordur
        self._huginn = huginn
        self._cove = cove
        self._dead_letters = dead_letter_store
        self._bus = bus
        self._check_interval_s = check_interval_s
        self._diagnostics_interval_s = diagnostics_interval_s
        self._dead_letter_alert_threshold = dead_letter_alert_threshold
        self._auto_reindex = auto_reindex_on_corruption
        self._reindex_count: int = 0
        self._last_reindex_at: Optional[str] = None
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._axiom_integrity: bool = True  # E-27: tracks last axiom check result
        self._state = MimirHealthState(
            overall="healthy",
            components={},
            dead_letters_total=0,
            last_reindex_at=None,
            reindex_count=0,
            checked_at=datetime.now(timezone.utc).isoformat(),
            axiom_integrity=True,  # E-27
        )

    # ── Lifecycle ──────────────────────────────────────────────────────────────

    def start(self) -> None:
        """Start the background daemon thread. Idempotent."""
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run_loop, daemon=True, name="MimirHealthMonitor"
        )
        self._thread.start()
        logger.info("MimirHealthMonitor started (interval=%.0fs).", self._check_interval_s)

    def stop(self) -> None:
        """Signal the daemon thread to stop and join it (up to 5 s)."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5.0)
        logger.info("MimirHealthMonitor stopped.")

    # ── Internal loop ─────────────────────────────────────────────────────────

    def _run_loop(self) -> None:
        diagnostics_ticks = 0
        ticks_per_diagnostics = max(
            1, int(self._diagnostics_interval_s / max(1, self._check_interval_s))
        )
        while not self._stop_event.wait(self._check_interval_s):
            self._health_check()
            diagnostics_ticks += 1
            if diagnostics_ticks >= ticks_per_diagnostics:
                self._full_diagnostics()
                diagnostics_ticks = 0

    def _health_check(self) -> None:
        """Run one health check pass over all components."""
        components: Dict[str, ComponentHealth] = {}

        components["mimir_well"] = self._check_component(
            "mimir_well", self._mimir_well, "_read_cb", "_write_cb"
        )
        components["huginn"] = self._check_component("huginn", self._huginn)
        components["vordur"] = self._check_component("vordur", self._vordur)
        components["cove"] = self._check_component("cove", self._cove)

        # Dead-letter rate
        dl_5m = 0
        try:
            if self._dead_letters is not None:
                dl_5m = self._dead_letters.count_recent(300.0)
        except Exception as exc:
            logger.warning("MimirHealthMonitor: dead letter count failed: %s", exc)

        if dl_5m > self._dead_letter_alert_threshold:
            logger.warning(
                "MimirHealthMonitor: dead-letter rate HIGH (%d entries in last 5 min).", dl_5m
            )
        if dl_5m > 10:
            logger.critical(
                "MimirHealthMonitor: CRITICAL — %d dead letters in 5 min. "
                "Hallucination storm possible.",
                dl_5m,
            )
            self._publish_alert("HEALTH_CRITICAL", {"dead_letters_5m": dl_5m})

        # MimirWell collection integrity check
        if self._auto_reindex:
            try:
                mw_state = self._mimir_well.get_state()
                if mw_state.document_count == 0:
                    logger.warning(
                        "MimirHealthMonitor: collection empty — triggering auto-reindex."
                    )
                    self.trigger_reindex()
            except Exception as exc:
                logger.warning("MimirHealthMonitor: collection check failed: %s", exc)

        # E-27: axiom integrity check
        axiom_ok = True
        try:
            axiom_ok = self._mimir_well.check_axiom_integrity()
            if not axiom_ok:
                logger.critical(
                    "MimirHealthMonitor: Axiom integrity violation detected — "
                    "triggering emergency reindex!"
                )
                self.trigger_reindex()
        except Exception as exc:
            logger.warning("MimirHealthMonitor: axiom integrity check error: %s", exc)
        self._axiom_integrity = axiom_ok

        # Overall status
        statuses = [c.status for c in components.values()]
        if "down" in statuses or dl_5m > 10:
            overall = "critical"
        elif "degraded" in statuses or dl_5m > self._dead_letter_alert_threshold:
            overall = "degraded"
        else:
            overall = "healthy"

        with self._lock:
            self._state = MimirHealthState(
                overall=overall,
                components=components,
                dead_letters_total=self._reindex_count,
                last_reindex_at=self._last_reindex_at,
                reindex_count=self._reindex_count,
                checked_at=datetime.now(timezone.utc).isoformat(),
                axiom_integrity=self._axiom_integrity,  # E-27
            )

        logger.debug("MimirHealthMonitor: check complete — overall=%s.", overall)

    def _check_component(
        self, name: str, obj: Any, *cb_attrs: str
    ) -> ComponentHealth:
        """Generic component health check — call get_state() to verify alive."""
        status = "healthy"
        cb_state = "unknown"
        try:
            if obj is None:
                status = "down"
            else:
                # Attempt a cheap state snapshot
                if hasattr(obj, "get_state"):
                    obj.get_state()
                status = "healthy"
                # Try to read circuit breaker state from known attribute names
                for attr in cb_attrs:
                    if hasattr(obj, attr):
                        cb = getattr(obj, attr, None)
                        if cb is not None and hasattr(cb, "state"):
                            cb_state = cb.state.value
                        break
        except Exception as exc:
            status = "degraded"
            logger.debug("MimirHealthMonitor: %s check failed: %s", name, exc)

        return ComponentHealth(
            name=name,
            status=status,
            circuit_breaker_state=cb_state,
            last_success_at=None,
            last_failure_at=None,
            failure_rate_5m=0.0,
            dead_letters_5m=0,
        )

    def _full_diagnostics(self) -> None:
        """Deeper diagnostics pass (runs every ~10 min)."""
        try:
            mw_state = self._mimir_well.get_state()
            logger.info(
                "MimirHealthMonitor diagnostics: docs=%d, chroma=%s, fallback=%s",
                mw_state.document_count,
                mw_state.chromadb_status,
                mw_state.fallback_mode,
            )
        except Exception as exc:
            logger.debug("MimirHealthMonitor full_diagnostics failed: %s", exc)

    def _publish_alert(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Publish a health alert to StateBus, sync-safe."""
        try:
            from scripts.state_bus import StateEvent
            event = StateEvent(
                source_module="mimir_health_monitor",
                event_type=event_type,
                payload=payload,
            )
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self._bus.publish_state(event, nowait=True))
            else:
                loop.run_until_complete(self._bus.publish_state(event, nowait=True))
        except Exception as exc:
            logger.debug("MimirWell: state bus publish failed: %s", exc)

    # ── Public API ────────────────────────────────────────────────────────────

    def get_state(self) -> MimirHealthState:
        """Return the most recent health state snapshot. Thread-safe."""
        with self._lock:
            return self._state

    def publish(self, bus: Any) -> None:
        """Publish the current health state to StateBus. Never raises."""
        try:
            from scripts.state_bus import StateEvent
            state = self.get_state()
            event = StateEvent(
                source_module="mimir_health_monitor",
                event_type="mimir_health_state",
                payload=state.to_dict(),
            )
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(bus.publish_state(event, nowait=True))
            else:
                loop.run_until_complete(bus.publish_state(event, nowait=True))
        except Exception as exc:
            logger.debug("MimirHealthMonitor.publish: failed: %s", exc)

    def trigger_reindex(self) -> None:
        """Manually trigger a MimirWell reindex. Thread-safe. Never raises."""
        try:
            logger.info("MimirHealthMonitor: triggering MimirWell reindex.")
            self._mimir_well.reindex()
            self._reindex_count += 1
            self._last_reindex_at = datetime.now(timezone.utc).isoformat()
            logger.info(
                "MimirHealthMonitor: reindex complete (#%d).", self._reindex_count
            )
        except Exception as exc:
            logger.warning("MimirHealthMonitor.trigger_reindex failed: %s", exc)


# ─── Singleton ────────────────────────────────────────────────────────────────

_MIMIR_WELL: Optional[MimirWell] = None


def get_mimir_well() -> MimirWell:
    """Return the global MimirWell instance. Raises if not yet initialised."""
    if _MIMIR_WELL is None:
        raise RuntimeError(
            "MimirWell not initialised — call init_mimir_well_from_config() first."
        )
    return _MIMIR_WELL


def init_mimir_well_from_config(
    config: Any,
    data_root: Optional[Union[str, Path]] = None,
    auto_ingest: bool = True,
) -> MimirWell:
    """Create and register the global MimirWell from the skill config dict.

    config  — the dict loaded by ConfigLoader (may be a nested dict or Any).
    data_root — override for the data directory root. If None, derived from config.
    auto_ingest — if True (default), triggers ingest_all() when the collection
                  is empty. Set to False in tests.

    Config keys read (all optional, have defaults):
        mimir_well.collection_name
        mimir_well.persist_dir
        mimir_well.chunk_size_tokens
        mimir_well.chunk_overlap_tokens
        mimir_well.n_retrieve
        mimir_well.n_final
        mimir_well.auto_ingest
        mimir_well.force_reindex
    """
    global _MIMIR_WELL

    mw_cfg: Dict[str, Any] = {}
    if isinstance(config, dict):
        mw_cfg = config.get("mimir_well", {}) or {}
    elif hasattr(config, "get"):
        mw_cfg = config.get("mimir_well", {}) or {}

    well = MimirWell(
        collection_name=mw_cfg.get("collection_name", _DEFAULT_COLLECTION),
        persist_dir=mw_cfg.get("persist_dir", _DEFAULT_PERSIST_DIR),
        chunk_size_tokens=int(mw_cfg.get("chunk_size_tokens", _DEFAULT_CHUNK_SIZE_TOKENS)),
        chunk_overlap_tokens=int(mw_cfg.get("chunk_overlap_tokens", _DEFAULT_OVERLAP_TOKENS)),
        n_retrieve=int(mw_cfg.get("n_retrieve", _DEFAULT_N_RETRIEVE)),
        n_final=int(mw_cfg.get("n_final", _DEFAULT_N_FINAL)),
        bm25_shortcircuit_threshold=float(mw_cfg.get("bm25_shortcircuit_threshold", 0.75)),  # E-26
        session_dir=str(mw_cfg.get("session_dir", "session")),  # E-27
        use_ollama_embeddings=bool(mw_cfg.get("use_ollama_embeddings", True)),    # S-07
        ollama_embed_model=str(mw_cfg.get("ollama_embed_model", "nomic-embed-text")),  # S-07
        ollama_base_url=str(mw_cfg.get("ollama_base_url", "http://localhost:11434")),  # S-07
    )

    do_auto_ingest = auto_ingest and bool(mw_cfg.get("auto_ingest", True))
    force_reindex = bool(mw_cfg.get("force_reindex", False))

    if do_auto_ingest and data_root is not None:
        dr = Path(data_root)
        try:
            report = well.ingest_all(dr, force=force_reindex)
            if report.errors:
                logger.warning(
                    "MimirWell init: ingest completed with %d errors.", len(report.errors)
                )
        except Exception as exc:
            logger.error("MimirWell init: ingest failed: %s", exc)

    _MIMIR_WELL = well
    logger.info(
        "MimirWell singleton registered (collection='%s', chromadb=%s, flat_index=%d).",
        well.collection_name,
        well.chromadb_available,
        well.flat_index_size,
    )
    return _MIMIR_WELL
