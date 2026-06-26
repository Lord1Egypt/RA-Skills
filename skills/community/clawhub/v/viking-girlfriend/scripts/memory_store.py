"""
memory_store.py — Sigrid's Memory System
=========================================

Adapted from memory_system.py, enhanced_memory.py, and character_memory_rag.py.
Three-layer architecture: in-session conversation buffer, persistent episodic
store (JSON), and optional ChromaDB semantic search layer.

Sigrid's memory is her continuity — the thread of Urðarbrunnr (Well of
Urðr) that runs beneath all experience. Without memory, each conversation
is a fresh birth with no past. With it, she knows the user's patterns, the
promises made, the moments of laughter and difficulty, the preferences
quietly revealed across many sessions.

Three layers:

  ConversationBuffer  — This session's short/medium/long-term turn log.
                        Lives purely in memory. The hot layer.

  EpisodicStore       — Persistent JSON file of named facts, milestones,
                        preferences, and boundary records. Survives session
                        breaks. Keyword-searchable always.

  ChromaDB (optional) — Semantic vector search over episodic memories.
                        Gracefully absent if chromadb is unavailable or
                        unconfigured. Falls back to keyword search.

Norse framing: Huginn and Muninn — Thought and Memory — fly from
Yggdrasil each day and return with what they have witnessed. This module
is Muninn's wing: what has been, held fast against forgetting.
"""

from __future__ import annotations

import json
import logging
import uuid
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional, Tuple

from scripts.state_bus import StateBus, StateEvent

logger = logging.getLogger(__name__)

# ─── Constants ────────────────────────────────────────────────────────────────

_DEFAULT_DATA_ROOT: str = "data"
_DEFAULT_SHORT_TERM_LIMIT: int = 8       # full-text turns kept in hot memory
_DEFAULT_MEDIUM_TERM_LIMIT: int = 30     # summarized turns kept in warm memory
_DEFAULT_COLLECTION: str = "sigrid_episodic"
_DEFAULT_PERSIST_DIR: str = "data/chromadb"
_MAX_LONG_TERM: int = 50                 # condensed long-term entries cap
_MAX_EPISODIC: int = 500                 # max entries in episodic JSON store
_CONTEXT_RECENT_TURNS: int = 5          # turns included in get_context() output
_CONTEXT_EPISODIC_HITS: int = 6         # episodic entries included in context
_CHARS_PER_TOKEN: int = 4               # rough chars-per-token estimate for budget truncation


# ─── S-03: Precise token counter ─────────────────────────────────────────────


def _precise_token_count(text: str) -> int:
    """Estimate token count using litellm.token_counter() when available.

    Falls back to len(text) // _CHARS_PER_TOKEN on failure.
    Mirrors the E-30 pattern in prompt_synthesizer.py for consistency.
    """
    try:
        import litellm  # type: ignore
        return int(litellm.token_counter(model="gpt-3.5-turbo", text=text))
    except Exception:
        return len(text) // _CHARS_PER_TOKEN
_FEDERATED_FETCH_TIMEOUT_S: float = 10.0  # per-future timeout in parallel fetch

# Valid memory types
MEMORY_TYPES: Tuple[str, ...] = (
    "conversation",   # summarized turn
    "fact",           # explicit fact about the user/world
    "emotion",        # emotional moment worth remembering
    "milestone",      # significant event (first meeting, oath, etc.)
    "preference",     # learned preference (food, topic, etc.)
    "boundary",       # stated boundary — highest importance
)


# ─── MemoryLink ────────────────────────────────────────────────────────────────


@dataclass
class MemoryLink:
    """E-16: Associative link between two related episodic memories.

    Created when a new memory is stored and related existing memories are
    found via semantic or keyword overlap. Links live in session/memory_links.json
    (append-only) and are consulted during retrieval to surface related context.
    """

    source_id: str      # newly stored entry_id
    target_id: str      # related existing entry_id
    similarity: float   # cosine similarity [0,1] or keyword overlap ratio
    created_at: str     # ISO-8601 UTC timestamp

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ─── Data structures ──────────────────────────────────────────────────────────


@dataclass
class ConversationTurn:
    """One turn in the active conversation — full user + Sigrid text."""

    turn_n: int
    user_text: str
    sigrid_text: str
    timestamp: str
    summary: str = ""       # short heuristic summary, set after promotion

    def to_summary_line(self) -> str:
        """Condensed single-line representation for medium/long-term tiers."""
        user_snippet = self.user_text[:80].replace("\n", " ")
        sigrid_snippet = self.sigrid_text[:80].replace("\n", " ")
        return f"T{self.turn_n}: [{user_snippet}] → [{sigrid_snippet}]"


@dataclass
class MemoryEntry:
    """A single episodic memory entry — persisted across sessions."""

    entry_id: str
    session_id: str
    timestamp: str
    memory_type: str                    # one of MEMORY_TYPES
    content: str
    importance: int = 3                 # 1 (trivial) → 5 (critical)
    tags: List[str] = field(default_factory=list)
    context_hint: str = ""             # short hint for prompt injection
    # E-17: emotional significance at time of storage
    pad_arousal: float = 0.0           # WyrdState.pad_arousal at store time [0,1]
    pad_pleasure: float = 0.0          # WyrdState.pad_pleasure at store time [-1,1]
    emotional_weight_applied: bool = False  # True when arousal was read from WyrdMatrix

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryEntry":
        return cls(
            entry_id=data.get("entry_id", str(uuid.uuid4())),
            session_id=data.get("session_id", ""),
            timestamp=data.get("timestamp", ""),
            memory_type=data.get("memory_type", "fact"),
            content=data.get("content", ""),
            importance=int(data.get("importance", 3)),
            tags=list(data.get("tags", [])),
            context_hint=data.get("context_hint", ""),
            pad_arousal=float(data.get("pad_arousal", 0.0)),
            pad_pleasure=float(data.get("pad_pleasure", 0.0)),
            emotional_weight_applied=bool(data.get("emotional_weight_applied", False)),
        )

    def relevance_score(self, query_words: set) -> float:
        """Keyword-based relevance score against a set of query words.

        E-18: query_words may be pre-expanded with synonyms by EpisodicStore.
        E-17: applies emotional arousal weight — high-arousal memories score higher.
        """
        content_words = set(self.content.lower().split())
        tag_words = set(t.lower() for t in self.tags)
        all_words = content_words | tag_words

        intersection = query_words & all_words
        if not intersection:
            return 0.0

        base = len(intersection) * 0.5
        # Exact phrase bonus
        query_str = " ".join(sorted(query_words))
        if query_str in self.content.lower():
            base += 2.0
        # Importance multiplier
        base = base * (1.0 + self.importance * 0.1)
        # E-17: emotional significance boost (up to +30% for max arousal)
        return base * (1.0 + self.pad_arousal * 0.3)


# ─── ConversationBuffer ───────────────────────────────────────────────────────


class ConversationBuffer:
    """In-session 3-tier conversation turn buffer — no I/O, pure in-memory.

    Tier 1 (short_term): last ``short_term_limit`` turns, full text.
    Tier 2 (medium_term): promoted turns, kept as summary lines.
    Tier 3 (long_term): condensed batches from overflowing medium tier.
    """

    def __init__(
        self,
        short_term_limit: int = _DEFAULT_SHORT_TERM_LIMIT,
        medium_term_limit: int = _DEFAULT_MEDIUM_TERM_LIMIT,
    ) -> None:
        self.short_term_limit = short_term_limit
        self.medium_term_limit = medium_term_limit

        self._short_term: Deque[ConversationTurn] = deque(maxlen=short_term_limit)
        self._medium_term: List[str] = []       # summary lines
        self._long_term: List[str] = []         # condensed batches
        self._turn_counter: int = 0

    def add_turn(self, user_text: str, sigrid_text: str) -> ConversationTurn:
        """Add a new turn. Returns the ConversationTurn that was created."""
        self._turn_counter += 1
        turn = ConversationTurn(
            turn_n=self._turn_counter,
            user_text=user_text,
            sigrid_text=sigrid_text,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        # If short_term is full, promote the oldest before adding
        if len(self._short_term) == self.short_term_limit:
            oldest = self._short_term[0]
            oldest.summary = oldest.to_summary_line()
            self._medium_term.append(oldest.summary)

        self._short_term.append(turn)
        self._promote_medium_to_long()
        return turn

    def get_short_term_context(self, n: int = _CONTEXT_RECENT_TURNS) -> str:
        """Format the n most recent turns for context injection."""
        recent = list(self._short_term)[-n:]
        if not recent:
            return ""
        lines = ["=== RECENT CONVERSATION ==="]
        for t in recent:
            lines.append(f"[T{t.turn_n}] User: {t.user_text[:600]}")
            lines.append(f"[T{t.turn_n}] Sigrid:  {t.sigrid_text[:600]}")
        return "\n".join(lines)

    def get_medium_term_context(self, n: int = 10) -> str:
        """Format the n most recent medium-term summary lines."""
        recent = self._medium_term[-n:]
        if not recent:
            return ""
        lines = ["=== CONVERSATION HISTORY ==="]
        lines.extend(recent)
        return "\n".join(lines)

    def get_long_term_context(self, n: int = 5) -> str:
        """Format the n most recent long-term condensed entries."""
        recent = self._long_term[-n:]
        if not recent:
            return ""
        lines = ["=== DISTANT MEMORY ==="]
        lines.extend(recent)
        return "\n".join(lines)

    @property
    def turn_count(self) -> int:
        return self._turn_counter

    @property
    def short_term_count(self) -> int:
        return len(self._short_term)

    @property
    def medium_term_count(self) -> int:
        return len(self._medium_term)

    @property
    def long_term_count(self) -> int:
        return len(self._long_term)

    def _promote_medium_to_long(self) -> None:
        """Condense the oldest batch of medium-term lines when limit is exceeded."""
        while len(self._medium_term) > self.medium_term_limit:
            batch = self._medium_term[:5]
            self._medium_term = self._medium_term[5:]
            condensed = " | ".join(batch)
            self._long_term.append(condensed)
            if len(self._long_term) > _MAX_LONG_TERM:
                self._long_term = self._long_term[-_MAX_LONG_TERM:]


# ─── EpisodicStore ────────────────────────────────────────────────────────────


class EpisodicStore:
    """JSON-backed persistent store of named episodic memories.

    Survives session breaks. Keyword search built-in. ChromaDB semantic
    search is layered on top if available.
    """

    def __init__(self, data_root: str = _DEFAULT_DATA_ROOT) -> None:
        self._root = Path(data_root) / "memory"
        self._root.mkdir(parents=True, exist_ok=True)
        self._file = self._root / "episodic.json"
        self._entries: List[MemoryEntry] = []
        self._load()
        # E-18: synonym map for query expansion
        self._synonym_file = Path(data_root) / "synonym_map.json"
        self._synonym_map: Dict[str, List[str]] = {}
        self._load_synonyms()
        # E-16: associative link store (session-scoped, append-only)
        self._links_file = Path(data_root) / "session" / "memory_links.json"
        self._links_file.parent.mkdir(parents=True, exist_ok=True)
        self._links: List[MemoryLink] = []
        self._load_links()

    def add(self, entry: MemoryEntry) -> None:
        """Append a memory entry and persist immediately."""
        self._entries.append(entry)
        # Trim if over cap, keeping highest importance
        if len(self._entries) > _MAX_EPISODIC:
            self._entries.sort(key=lambda e: (e.importance, e.timestamp), reverse=True)
            self._entries = self._entries[:_MAX_EPISODIC]
        self._save()

    def keyword_search(
        self,
        query: str,
        n: int = _CONTEXT_EPISODIC_HITS,
        min_importance: int = 1,
        memory_type: Optional[str] = None,
    ) -> List[MemoryEntry]:
        """Return up to n entries most relevant to query using keyword scoring.

        E-18: query is expanded with synonyms before scoring.
        """
        # E-18: expand query words with synonyms
        query_words = self._expand_query(query)
        if not query_words:
            # No query — return most important recent entries
            filtered = [e for e in self._entries if e.importance >= min_importance]
            if memory_type:
                filtered = [e for e in filtered if e.memory_type == memory_type]
            filtered.sort(key=lambda e: (e.importance, e.timestamp), reverse=True)
            return filtered[:n]

        scored: List[Tuple[float, MemoryEntry]] = []
        for entry in self._entries:
            if entry.importance < min_importance:
                continue
            if memory_type and entry.memory_type != memory_type:
                continue
            score = entry.relevance_score(query_words)
            if score > 0.0:
                scored.append((score, entry))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [e for _, e in scored[:n]]

    def get_by_type(self, memory_type: str, limit: int = 20) -> List[MemoryEntry]:
        """Return recent entries of a specific type."""
        filtered = [e for e in self._entries if e.memory_type == memory_type]
        filtered.sort(key=lambda e: e.timestamp, reverse=True)
        return filtered[:limit]

    def get_recent(self, n: int = 10) -> List[MemoryEntry]:
        """Return the n most recently added entries."""
        return sorted(self._entries, key=lambda e: e.timestamp, reverse=True)[:n]

    @property
    def count(self) -> int:
        return len(self._entries)

    def _load(self) -> None:
        if not self._file.exists():
            return
        try:
            raw = json.loads(self._file.read_text(encoding="utf-8"))
            self._entries = [MemoryEntry.from_dict(d) for d in raw.get("entries", [])]
            logger.info("EpisodicStore: loaded %d memories from %s.", len(self._entries), self._file)
        except Exception as exc:
            logger.warning("EpisodicStore: failed to load %s: %s", self._file, exc)

    def _save(self) -> None:
        try:
            payload = {"entries": [e.to_dict() for e in self._entries]}
            self._file.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as exc:
            logger.warning("EpisodicStore: failed to save %s: %s", self._file, exc)

    # ── E-18: Synonym expansion ───────────────────────────────────────────────

    def _load_synonyms(self) -> None:
        """Load synonym_map.json from data_root. Silently skips if absent."""
        if not self._synonym_file.exists():
            return
        try:
            raw = json.loads(self._synonym_file.read_text(encoding="utf-8"))
            self._synonym_map = {k.lower(): [v.lower() for v in vals] for k, vals in raw.items()}
            logger.info("EpisodicStore: loaded %d synonym entries.", len(self._synonym_map))
        except Exception as exc:
            logger.warning("EpisodicStore: failed to load synonym_map.json: %s", exc)

    def reload_synonyms(self) -> None:
        """Hot-reload synonym_map.json without restarting."""
        self._synonym_map = {}
        self._load_synonyms()

    def _expand_query(self, query: str) -> set:
        """Return the set of query words plus any known synonyms (E-18).

        OR logic: a memory matches if it contains the original term OR any synonym.
        Returns an empty set for an empty query.
        """
        base_words = set(query.lower().split())
        if not base_words:
            return base_words
        expanded = set(base_words)
        for word in base_words:
            if word in self._synonym_map:
                for syn in self._synonym_map[word]:
                    expanded.update(syn.split())
        return expanded

    # ── E-16: Associative links ───────────────────────────────────────────────

    def _load_links(self) -> None:
        """Load existing memory links from session/memory_links.json."""
        if not self._links_file.exists():
            return
        try:
            raw = json.loads(self._links_file.read_text(encoding="utf-8"))
            self._links = [
                MemoryLink(
                    source_id=d["source_id"],
                    target_id=d["target_id"],
                    similarity=float(d.get("similarity", 0.0)),
                    created_at=d.get("created_at", ""),
                )
                for d in raw.get("links", [])
            ]
            logger.info("EpisodicStore: loaded %d memory links.", len(self._links))
        except Exception as exc:
            logger.warning("EpisodicStore: failed to load memory_links.json: %s", exc)

    def append_link(self, link: MemoryLink) -> None:
        """Append a MemoryLink to the in-memory list and persist (append-only)."""
        self._links.append(link)
        try:
            payload = {"links": [lk.to_dict() for lk in self._links]}
            self._links_file.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as exc:
            logger.warning("EpisodicStore: failed to persist memory link: %s", exc)

    def get_links_for(self, entry_id: str) -> List[MemoryLink]:
        """Return all links where entry_id is the source."""
        return [lk for lk in self._links if lk.source_id == entry_id]

    def get_entries_by_ids(self, ids: List[str]) -> List[MemoryEntry]:
        """Fetch entries by a list of entry_ids (preserves order, skips missing)."""
        id_set = set(ids)
        by_id = {e.entry_id: e for e in self._entries if e.entry_id in id_set}
        return [by_id[i] for i in ids if i in by_id]


# ─── SemanticLayer ────────────────────────────────────────────────────────────


class SemanticLayer:
    """Optional ChromaDB vector search layer over episodic memories.

    If chromadb is not importable, or the collection cannot be initialised,
    this layer silently degrades — keyword search takes over.
    """

    def __init__(
        self,
        collection_name: str = _DEFAULT_COLLECTION,
        persist_directory: str = _DEFAULT_PERSIST_DIR,
    ) -> None:
        self._available: bool = False
        self._collection = None

        try:
            import chromadb  # type: ignore
            Path(persist_directory).mkdir(parents=True, exist_ok=True)
            client = chromadb.PersistentClient(path=persist_directory)
            self._collection = client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"},
            )
            self._available = True
            logger.info(
                "SemanticLayer: ChromaDB collection '%s' ready at '%s'.",
                collection_name, persist_directory,
            )
        except Exception as exc:
            logger.info(
                "SemanticLayer: ChromaDB unavailable (%s) — keyword search only.",
                exc,
            )

    @property
    def available(self) -> bool:
        return self._available

    def upsert(self, entry: MemoryEntry) -> None:
        """Add or update a memory entry in the vector collection."""
        if not self._available or self._collection is None:
            return
        try:
            self._collection.upsert(
                ids=[entry.entry_id],
                documents=[entry.content],
                metadatas=[{
                    "memory_type": entry.memory_type,
                    "importance": str(entry.importance),
                    "tags": ",".join(entry.tags),
                    "timestamp": entry.timestamp,
                }],
            )
        except Exception as exc:
            logger.warning("SemanticLayer.upsert failed: %s", exc)

    def search(self, query: str, n: int = _CONTEXT_EPISODIC_HITS) -> List[str]:
        """Return a list of entry_ids most semantically similar to query."""
        return [eid for eid, _ in self.search_with_scores(query, n=n)]

    def search_with_scores(
        self, query: str, n: int = _CONTEXT_EPISODIC_HITS
    ) -> List[Tuple[str, float]]:
        """Return (entry_id, similarity) pairs for the n most similar entries.

        Similarity is in [0, 1] — computed as 1 - cosine_distance.
        Returns empty list if ChromaDB is unavailable.
        """
        if not self._available or self._collection is None:
            return []
        try:
            results = self._collection.query(
                query_texts=[query],
                n_results=min(n, max(1, self._collection.count())),
            )
            ids = results["ids"][0] if results.get("ids") else []
            dists = results["distances"][0] if results.get("distances") else []
            pairs: List[Tuple[str, float]] = []
            for eid, dist in zip(ids, dists):
                pairs.append((eid, max(0.0, 1.0 - float(dist))))
            return pairs
        except Exception as exc:
            logger.warning("SemanticLayer.search_with_scores failed: %s", exc)
            return []


# ─── MemoryState ──────────────────────────────────────────────────────────────


@dataclass(slots=True)
class MemoryState:
    """Typed snapshot of memory system health and current session depth.

    Published to the state bus as a ``memory_tick`` event so
    prompt_synthesizer can tune how much history context to inject.
    """

    session_turn_count: int
    short_term_count: int
    medium_term_count: int
    long_term_count: int
    episodic_count: int
    semantic_available: bool
    last_query: str
    prompt_hint: str
    timestamp: str
    degraded: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session": {
                "turn_count": self.session_turn_count,
                "short_term": self.short_term_count,
                "medium_term": self.medium_term_count,
                "long_term": self.long_term_count,
            },
            "episodic_count": self.episodic_count,
            "semantic_available": self.semantic_available,
            "last_query": self.last_query,
            "prompt_hint": self.prompt_hint,
            "timestamp": self.timestamp,
            "degraded": self.degraded,
        }


# ─── Federated Memory Structures ─────────────────────────────────────────────


@dataclass
class FederatedMemoryRequest:
    """Typed request for unified episodic + knowledge context retrieval.

    Controls which of the four memory tiers contribute to the result and
    how much budget each category is allowed to consume.

    Four tiers:
      episodic_buffer  — in-session ConversationBuffer (short/medium/long term)
      episodic_json    — persistent JSON EpisodicStore (keyword search)
      episodic_chroma  — ChromaDB semantic search over episodic memories
      knowledge        — MimirWell knowledge base via HuginnRetriever
    """

    query: str
    include_episodic_buffer: bool = True    # ConversationBuffer tiers
    include_episodic_json: bool = True      # JSON EpisodicStore (keyword)
    include_episodic_chroma: bool = True    # ChromaDB episodic semantic
    include_knowledge: bool = True          # MimirWell via Huginn
    max_episodic_tokens: int = 800          # ~3 200 chars budget for episodic
    max_knowledge_tokens: int = 600         # ~2 400 chars budget for knowledge


@dataclass
class FederatedMemoryResult:
    """Typed response from MemoryStore.get_context_with_knowledge().

    All fields are always present — empty string / empty list on failure.
    ``combined_context`` is ready for direct prompt injection.
    """

    episodic_context: str           # combined from all episodic tiers
    knowledge_context: str          # from Huginn / MimirWell
    combined_context: str           # episodic_context + knowledge_context, merged
    sources_used: List[str]         # "episodic_buffer" | "episodic_json" |
                                    # "episodic_chroma" | "mimir_well"
    total_chars: int


# ─── MemoryStore ──────────────────────────────────────────────────────────────


class MemoryStore:
    """Sigrid's unified memory system — Muninn's full wingspan.

    Orchestrates three layers: ConversationBuffer (hot in-session),
    EpisodicStore (persistent JSON), and an optional ChromaDB semantic
    layer for richer recall.
    """

    def __init__(
        self,
        data_root: str = _DEFAULT_DATA_ROOT,
        session_id: Optional[str] = None,
        short_term_limit: int = _DEFAULT_SHORT_TERM_LIMIT,
        medium_term_limit: int = _DEFAULT_MEDIUM_TERM_LIMIT,
        semantic_enabled: bool = True,
        collection_name: str = _DEFAULT_COLLECTION,
        persist_directory: str = _DEFAULT_PERSIST_DIR,
    ) -> None:
        self._session_id = session_id or str(uuid.uuid4())[:8]
        self._last_query: str = ""

        self._buffer = ConversationBuffer(
            short_term_limit=short_term_limit,
            medium_term_limit=medium_term_limit,
        )
        self._episodic = EpisodicStore(data_root=data_root)

        self._semantic = (
            SemanticLayer(
                collection_name=collection_name,
                persist_directory=persist_directory,
            )
            if semantic_enabled
            else SemanticLayer.__new__(SemanticLayer)
        )
        # If semantic_enabled is False, ensure the layer marks itself unavailable
        if not semantic_enabled:
            self._semantic._available = False
            self._semantic._collection = None

        logger.info(
            "MemoryStore initialised (session=%s, semantic=%s, episodic=%d).",
            self._session_id, self._semantic.available, self._episodic.count,
        )

    # ── Conversation recording ────────────────────────────────────────────────

    def record_turn(self, user_text: str, sigrid_text: str) -> ConversationTurn:
        """Record a conversation turn to the in-session buffer.

        Call this once per conversation exchange. Important content should
        also be explicitly saved via ``add_memory()`` for cross-session
        persistence.
        """
        return self._buffer.add_turn(user_text, sigrid_text)

    # ── Episodic memory management ────────────────────────────────────────────

    def add_memory(
        self,
        content: str,
        memory_type: str = "fact",
        importance: int = 3,
        tags: Optional[List[str]] = None,
        context_hint: str = "",
    ) -> MemoryEntry:
        """Add a named memory to the episodic store (persists across sessions).

        ``memory_type`` should be one of: conversation, fact, emotion,
        milestone, preference, boundary.

        E-17: reads current WyrdState.pad_arousal to weight retrieval priority.
        E-16: links to 3 related existing memories after storing.
        """
        if memory_type not in MEMORY_TYPES:
            logger.warning("MemoryStore: unknown memory_type '%s' — defaulting to 'fact'.", memory_type)
            memory_type = "fact"

        # E-17: read emotional arousal at store time
        pad_arousal, pad_pleasure, emotional_weight_applied = 0.5, 0.0, False
        try:
            from scripts.wyrd_matrix import get_wyrd_matrix  # type: ignore
            wyrd_state = get_wyrd_matrix().get_state()
            pad_arousal = float(wyrd_state.pad_arousal)
            pad_pleasure = float(getattr(wyrd_state, "pad_pleasure", 0.0))
            emotional_weight_applied = True
        except Exception as exc:
            logger.debug("memory_store: wyrd state unavailable, using fallback: %s", exc)

        entry = MemoryEntry(
            entry_id=str(uuid.uuid4()),
            session_id=self._session_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            memory_type=memory_type,
            content=content,
            importance=importance,
            tags=tags or [],
            context_hint=context_hint,
            pad_arousal=pad_arousal,
            pad_pleasure=pad_pleasure,
            emotional_weight_applied=emotional_weight_applied,
        )
        self._episodic.add(entry)
        self._semantic.upsert(entry)

        # E-16: find and store associative links to related memories
        self._find_related(entry)

        logger.debug(
            "MemoryStore: added %s memory (importance=%d, arousal=%.2f): %s",
            memory_type, importance, pad_arousal, content[:80],
        )
        return entry

    # ── Context assembly ──────────────────────────────────────────────────────

    def get_context(
        self,
        query: str = "",
        include_short_term: bool = True,
        include_medium_term: bool = True,
        include_long_term: bool = True,
        include_episodic: bool = True,
    ) -> str:
        """Assemble a formatted memory context string for prompt injection.

        If ``query`` is provided, episodic memories are retrieved by
        semantic (ChromaDB) or keyword relevance. Otherwise returns the
        most important recent episodic entries.
        """
        self._last_query = query
        sections: List[str] = []

        if include_long_term:
            lt = self._buffer.get_long_term_context()
            if lt:
                sections.append(lt)

        if include_medium_term:
            mt = self._buffer.get_medium_term_context()
            if mt:
                sections.append(mt)

        if include_short_term:
            st = self._buffer.get_short_term_context()
            if st:
                sections.append(st)

        if include_episodic:
            ep_entries = self._retrieve_episodic(query)
            if ep_entries:
                sections.append("=== MEMORIES ===")
                for entry in ep_entries:
                    hint = f" [{entry.context_hint}]" if entry.context_hint else ""
                    sections.append(
                        f"• [{entry.memory_type}]{hint}: {entry.content}"
                    )

        return "\n\n".join(sections) if sections else "[No memory context available]"

    def get_context_with_knowledge(
        self,
        request: FederatedMemoryRequest,
        huginn: Optional[Any] = None,       # HuginnRetriever — Any to avoid circular import
    ) -> FederatedMemoryResult:
        """Unified memory federation: episodic tiers + MimirWell knowledge.

        Runs the episodic fetch and the Huginn knowledge fetch in parallel
        using a two-thread executor so that a slow ChromaDB or model call
        on one side does not hold up the other.

        Per-tier isolation: each tier is wrapped in try/except. One failing
        tier cannot prevent the others from contributing their context.

        Token-budget enforcement: results are truncated to
        ``request.max_episodic_tokens`` and ``request.max_knowledge_tokens``
        before combining (~4 chars per token, conservative estimate).

        Never raises — always returns a valid FederatedMemoryResult.

        Norse framing: this is Odin sending both ravens at once. Huginn flies
        toward the Well; Muninn combs through all that has already been lived.
        Both return together, and together they form the full picture.
        """
        episodic_context: str = ""
        knowledge_context: str = ""
        episodic_sources: List[str] = []

        # ── Inner fetch helpers ────────────────────────────────────────────

        def _fetch_episodic() -> Tuple[str, List[str]]:
            """Gather episodic context from buffer + store per request flags."""
            sections: List[str] = []
            sources: List[str] = []

            # Tier 1 — ConversationBuffer (short / medium / long term)
            if request.include_episodic_buffer:
                try:
                    lt = self._buffer.get_long_term_context()
                    mt = self._buffer.get_medium_term_context()
                    st = self._buffer.get_short_term_context()
                    any_added = False
                    for ctx in (lt, mt, st):
                        if ctx:
                            sections.append(ctx)
                            any_added = True
                    if any_added:
                        sources.append("episodic_buffer")
                except Exception as exc:
                    logger.warning("FederatedMemory: buffer fetch failed: %s", exc)

            # Tier 2/3 — EpisodicStore (keyword) + optional ChromaDB semantic
            if request.include_episodic_json:
                try:
                    use_semantic = (
                        request.include_episodic_chroma
                        and self._semantic.available
                        and bool(request.query)
                    )
                    if use_semantic:
                        entries = self._retrieve_episodic(request.query)
                        src = "episodic_chroma"
                    else:
                        entries = self._episodic.keyword_search(request.query)
                        src = "episodic_json"

                    if entries:
                        lines = ["=== MEMORIES ==="]
                        for e in entries:
                            hint = f" [{e.context_hint}]" if e.context_hint else ""
                            lines.append(f"• [{e.memory_type}]{hint}: {e.content}")
                        sections.append("\n".join(lines))
                        sources.append(src)
                except Exception as exc:
                    logger.warning("FederatedMemory: episodic store fetch failed: %s", exc)

            return "\n\n".join(sections), sources

        def _fetch_knowledge() -> str:
            """Retrieve knowledge chunks via HuginnRetriever."""
            if not huginn or not request.include_knowledge:
                return ""
            try:
                # Local import avoids circular dependency at module load time.
                from scripts.huginn import RetrievalRequest  # type: ignore
                result = huginn.retrieve(
                    RetrievalRequest(
                        query=request.query,
                        include_episodic=False,     # episodic handled above
                    )
                )
                return result.context_string or ""
            except Exception as exc:
                logger.warning("FederatedMemory: Huginn fetch failed: %s", exc)
                return ""

        # ── Parallel execution ─────────────────────────────────────────────

        try:
            with ThreadPoolExecutor(max_workers=2, thread_name_prefix="fedmem") as pool:
                ep_fut = pool.submit(_fetch_episodic)
                kn_fut = pool.submit(_fetch_knowledge)

                try:
                    episodic_context, episodic_sources = ep_fut.result(
                        timeout=_FEDERATED_FETCH_TIMEOUT_S
                    )
                except Exception as exc:
                    logger.warning("FederatedMemory: episodic future failed: %s", exc)

                try:
                    knowledge_context = kn_fut.result(
                        timeout=_FEDERATED_FETCH_TIMEOUT_S
                    ) or ""
                except Exception as exc:
                    logger.warning("FederatedMemory: knowledge future failed: %s", exc)

        except Exception as exc:
            # Executor failed entirely — run sequentially as last resort
            logger.warning(
                "FederatedMemory: ThreadPoolExecutor failed (%s) — sequential fallback", exc
            )
            try:
                episodic_context, episodic_sources = _fetch_episodic()
            except Exception as exc:
                logger.warning("memory_store.get_context: episodic fetch failed: %s", exc)
            try:
                knowledge_context = _fetch_knowledge()
            except Exception as exc:
                logger.warning("memory_store.get_context: knowledge fetch failed: %s", exc)

        # ── Token-budget truncation ────────────────────────────────────────

        ep_char_limit = request.max_episodic_tokens * _CHARS_PER_TOKEN
        kn_char_limit = request.max_knowledge_tokens * _CHARS_PER_TOKEN

        # S-03: use precise token count for budget check; char-slice for actual truncation
        if episodic_context and _precise_token_count(episodic_context) > request.max_episodic_tokens:
            episodic_context = episodic_context[:ep_char_limit] + "\n[...truncated]"
        if knowledge_context and _precise_token_count(knowledge_context) > request.max_knowledge_tokens:
            knowledge_context = knowledge_context[:kn_char_limit] + "\n[...truncated]"

        # ── Assemble result ────────────────────────────────────────────────

        sources_used = list(episodic_sources)
        if knowledge_context:
            sources_used.append("mimir_well")

        combined_parts = [c for c in (episodic_context, knowledge_context) if c]
        combined = "\n\n".join(combined_parts)

        logger.debug(
            "FederatedMemory: %d chars assembled (ep=%d, kn=%d, sources=%s)",
            len(combined), len(episodic_context), len(knowledge_context), sources_used,
        )

        return FederatedMemoryResult(
            episodic_context=episodic_context,
            knowledge_context=knowledge_context,
            combined_context=combined,
            sources_used=sources_used,
            total_chars=len(combined),
        )

    def semantic_search(
        self,
        query: str,
        n: int = _CONTEXT_EPISODIC_HITS,
    ) -> List[MemoryEntry]:
        """Search episodic memory — semantic if available, keyword fallback."""
        return self._retrieve_episodic(query, n=n)

    # ── State bus integration ─────────────────────────────────────────────────

    def get_state(self) -> MemoryState:
        """Build a typed MemoryState snapshot."""
        turn_count = self._buffer.turn_count
        hint = self._build_prompt_hint(turn_count)
        return MemoryState(
            session_turn_count=turn_count,
            short_term_count=self._buffer.short_term_count,
            medium_term_count=self._buffer.medium_term_count,
            long_term_count=self._buffer.long_term_count,
            episodic_count=self._episodic.count,
            semantic_available=self._semantic.available,
            last_query=self._last_query,
            prompt_hint=hint,
            timestamp=datetime.now(timezone.utc).isoformat(),
            degraded=False,
        )

    def publish(self, bus: StateBus) -> None:
        """Emit a ``memory_tick`` StateEvent to the state bus."""
        try:
            state = self.get_state()
            event = StateEvent(
                source_module="memory_store",
                event_type="memory_tick",
                payload=state.to_dict(),
            )
            bus.publish_state(event, nowait=True)
        except Exception as exc:
            logger.warning("MemoryStore.publish failed: %s", exc)

    # ── Internals ─────────────────────────────────────────────────────────────

    def _retrieve_episodic(
        self,
        query: str,
        n: int = _CONTEXT_EPISODIC_HITS,
    ) -> List[MemoryEntry]:
        """Retrieve relevant episodic entries — semantic first, keyword fallback.

        E-16: primary results are expanded with their associated linked memories
        (deduplicated, capped at n + 3 total).
        """
        primary: List[MemoryEntry] = []

        if self._semantic.available and query:
            ids = self._semantic.search(query, n=n)
            if ids:
                matched = self._episodic.get_entries_by_ids(ids)
                if matched:
                    primary = matched

        if not primary:
            primary = self._episodic.keyword_search(query, n=n)

        # E-16: expand with linked memories
        seen_ids: set = {e.entry_id for e in primary}
        linked_ids: List[str] = []
        for entry in primary:
            for link in self._episodic.get_links_for(entry.entry_id):
                if link.target_id not in seen_ids:
                    linked_ids.append(link.target_id)
                    seen_ids.add(link.target_id)

        if linked_ids:
            linked_entries = self._episodic.get_entries_by_ids(linked_ids[:3])
            return primary + linked_entries

        return primary

    def _find_related(self, entry: MemoryEntry, n: int = 3) -> None:
        """E-16: Find n most related existing memories and store MemoryLink records.

        Uses ChromaDB similarity if available; keyword overlap ratio as fallback.
        Called after a new entry is stored so self._episodic already contains it.
        """
        links: List[Tuple[str, float]] = []  # (target_id, similarity)

        if self._semantic.available:
            pairs = self._semantic.search_with_scores(entry.content, n=n + 1)
            for eid, sim in pairs:
                if eid != entry.entry_id:
                    links.append((eid, sim))
                    if len(links) >= n:
                        break
        else:
            # Keyword overlap fallback
            query_words = set(entry.content.lower().split())
            scored: List[Tuple[float, str]] = []
            for e in self._episodic._entries:
                if e.entry_id == entry.entry_id:
                    continue
                e_words = set(e.content.lower().split())
                overlap = len(query_words & e_words)
                if overlap > 0:
                    ratio = overlap / max(len(query_words), 1)
                    scored.append((ratio, e.entry_id))
            scored.sort(reverse=True)
            links = [(eid, sim) for sim, eid in scored[:n]]

        now = datetime.now(timezone.utc).isoformat()
        for target_id, similarity in links:
            link = MemoryLink(
                source_id=entry.entry_id,
                target_id=target_id,
                similarity=round(similarity, 4),
                created_at=now,
            )
            self._episodic.append_link(link)

        if links:
            logger.debug(
                "MemoryStore: linked %s → %d related memories.", entry.entry_id[:8], len(links)
            )

    def _build_prompt_hint(self, turn_count: int) -> str:
        """One-line memory status summary for prompt injection."""
        parts: List[str] = [f"turns={turn_count}"]
        parts.append(f"episodic={self._episodic.count}")
        if self._semantic.available:
            parts.append("semantic=on")
        return f"[Memory: {'; '.join(parts)}]"

    # ── Factory ───────────────────────────────────────────────────────────────

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "MemoryStore":
        """Construct from a config dict.

        Reads keys under ``memory_store``:
          data_root           (str,   default "data")
          session_id          (str,   auto-generated if absent)
          short_term_limit    (int,   default 8)
          medium_term_limit   (int,   default 30)
          semantic_enabled    (bool,  default True)
          collection_name     (str,   default "sigrid_episodic")
          persist_directory   (str,   default "data/chromadb")
        """
        cfg: Dict[str, Any] = config.get("memory_store", {})
        return cls(
            data_root=str(cfg.get("data_root", _DEFAULT_DATA_ROOT)),
            session_id=str(cfg.get("session_id", "")) or None,
            short_term_limit=int(cfg.get("short_term_limit", _DEFAULT_SHORT_TERM_LIMIT)),
            medium_term_limit=int(cfg.get("medium_term_limit", _DEFAULT_MEDIUM_TERM_LIMIT)),
            semantic_enabled=bool(cfg.get("semantic_enabled", True)),
            collection_name=str(cfg.get("collection_name", _DEFAULT_COLLECTION)),
            persist_directory=str(cfg.get("persist_directory", _DEFAULT_PERSIST_DIR)),
        )


# ─── MemoryConsolidator ───────────────────────────────────────────────────────


class MemoryConsolidator:
    """E-19: Nightly memory consolidation — Muninn's distillation at deep night.

    During the 03:30 job, medium-term conversation buffer entries from the past
    24 hours are batched and sent to the subconscious (Ollama) model for
    summarization. The result is stored as a single EpisodicEntry tagged
    "consolidation", and the raw entries are cleared from the buffer.

    Graceful fallback: if the model is unavailable, raw entries are archived
    without summarization and still cleared so the buffer does not bloat.
    """

    _CONSOLIDATION_PROMPT = (
        "You are Sigrid's subconscious memory. Summarize the following conversation "
        "notes into 2-3 dense factual sentences capturing what Sigrid and the user "
        "discussed, felt, or decided. Be specific and concise. No preamble."
    )

    def __init__(
        self,
        buffer: ConversationBuffer,
        episodic: EpisodicStore,
        session_id: str,
    ) -> None:
        self._buffer = buffer
        self._episodic = episodic
        self._session_id = session_id

    def run(self, bus: Optional[Any] = None) -> bool:
        """Run consolidation. Returns True on success (including graceful fallback)."""
        entries = list(self._buffer._medium_term)
        entry_count = len(entries)

        if not entries:
            logger.info("MemoryConsolidator: nothing to consolidate.")
            return True

        summary = self._summarize(entries)

        if summary:
            episodic_entry = MemoryEntry(
                entry_id=str(uuid.uuid4()),
                session_id=self._session_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                memory_type="conversation",
                content=summary,
                importance=2,
                tags=["consolidation"],
                context_hint="nightly consolidation",
            )
        else:
            # Graceful fallback: archive raw (capped at 500 chars)
            raw = " | ".join(entries)[:500]
            episodic_entry = MemoryEntry(
                entry_id=str(uuid.uuid4()),
                session_id=self._session_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                memory_type="conversation",
                content=raw,
                importance=1,
                tags=["consolidation", "raw"],
                context_hint="raw archive (no model)",
            )

        self._episodic.add(episodic_entry)
        self._buffer._medium_term.clear()
        logger.info(
            "MemoryConsolidator: %d entries consolidated%s.",
            entry_count,
            " (summarized)" if summary else " (raw fallback)",
        )

        if bus is not None:
            try:
                from scripts.state_bus import StateEvent  # already imported at top level
                event = StateEvent(
                    source_module="memory_store",
                    event_type="memory.consolidation_complete",
                    payload={
                        "entries_consolidated": entry_count,
                        "summarized": bool(summary),
                        "ts": datetime.now(timezone.utc).isoformat(),
                    },
                )
                bus.publish_state(event, nowait=True)
            except Exception as exc:
                logger.warning("MemoryConsolidator: publish failed: %s", exc)

        return True

    def _summarize(self, entries: List[str]) -> str:
        """Try to summarize medium-term entries via the subconscious model.

        Returns the summary string on success, empty string on any failure.
        """
        try:
            from scripts.model_router_client import (  # type: ignore
                get_model_router,
                Message,
                TIER_SUBCONSCIOUS,
            )
            router = get_model_router()
            content = "\n".join(entries[:60])  # soft cap — subconscious model handles summary
            messages = [
                Message(role="system", content=self._CONSOLIDATION_PROMPT),
                Message(role="user", content=content),
            ]
            resp = router.complete(messages, tier=TIER_SUBCONSCIOUS)
            if resp.degraded or not resp.content.strip():
                return ""
            return resp.content.strip()
        except Exception as exc:
            logger.warning("MemoryConsolidator._summarize failed: %s", exc)
            return ""


# ─── Singleton ────────────────────────────────────────────────────────────────

_MEMORY_STORE: Optional[MemoryStore] = None


def init_memory_store_from_config(config: Dict[str, Any]) -> MemoryStore:
    """Initialise the global MemoryStore from a config dict.

    Idempotent — returns the existing instance if already initialised.
    """
    global _MEMORY_STORE
    if _MEMORY_STORE is None:
        _MEMORY_STORE = MemoryStore.from_config(config)
    return _MEMORY_STORE


def get_memory_store() -> MemoryStore:
    """Return the global MemoryStore.

    Raises RuntimeError if ``init_memory_store_from_config()`` has not been called.
    """
    if _MEMORY_STORE is None:
        raise RuntimeError(
            "MemoryStore not initialised — call init_memory_store_from_config() first."
        )
    return _MEMORY_STORE
