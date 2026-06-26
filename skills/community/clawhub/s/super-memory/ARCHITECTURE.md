# Agent Memory Architecture

## Overview
Agent Memory is a structured long-term memory system for AI agents, built on SQLite + sqlite-vec/ChromaDB with a Five-Lane TEMPR architecture.

## Core Architecture

### Five-Lane TEMPR Architecture
Five parallel retrieval lanes fused via Reciprocal Rank Fusion (RRF):

- **Lane 1: FTS5 + LIKE** — Structured full-text search with field filters
- **Lane 1.5: BM25** — Sparse retrieval index (`bm25_index.py`), fallback/supplement when FTS5 unavailable
- **Lane 2: Semantic Vector** — vec0 / ChromaDB cosine similarity search (`embedding_store.py`)
- **Lane 3: Entity Expansion** — Entity relationship graph expansion via `EntityResolver`
- **Lane 4: Causal Chain** — `memory_links` causal chain traversal, max depth 2

RRF formula: `score(d) = Σ_{i=1}^{5} 1/(k + rank_i(d))`, k=60. Multi-lane hits receive score stacking bonus.

### Four Engines
- **IngestEngine** (`engines/ingest.py`): Handles memory ingestion with dedup, quality scoring, and auto-linking
- **RecallEngine** (`recall.py` → `engines/recall_engine.py`): Five-lane TEMPR retrieval + RRF fusion + intent classification + MMR diversity
- **MaintainEngine** (`engines/maintain.py`): Lifecycle management, decay, distillation
- **CognitionEngine** (`engines/cognition.py`): Causal reasoning, knowledge graph

### Dual Timeline Fact Management
`temporal.py` — Phase 2.1 dual-timeline reasoning inspired by Zep (t_event + t_valid) and Hindsight (occurrence + mention):
- **valid_from / valid_until**: Fact validity period (like Zep's t_valid)
- **occurrence_time**: When the event actually happened (like Hindsight's occurrence)
- **mention_time**: When the user first mentioned this fact (like Hindsight's mention)
- **time_ts**: System write timestamp (existing field)
- `TemporalReasoner` extracts time signals, checks fact validity, and detects invalidation signals to mark old facts as expired

### Entity Resolution Engine
`entity.py` — Phase 2.2 entity resolution:
- Rule-based extraction (Chinese names, organizations, locations, English names)
- Three-level resolution: Exact match → Alias match → Fuzzy match (Levenshtein, threshold 0.75)
- Entity-memory association and inter-entity relationship graph
- Alias inverted index with lazy construction (O(1) lookup)

### Unified Configuration Layer
`config/settings.py` — Aggregates all config sources with priority: Environment variables > JSON config file > Code defaults:
- database, llm, embedding, mcp, smart, tier, auth, logging, compliance, server
- Lazy-loaded sub-configs: `MCPConfig`, `SmartConfig`

### Encrypted Storage
`storage/crypto_store.py` — Transparent encryption proxy over MemoryStore:
- Fernet symmetric encryption (AES-128-CBC + HMAC-SHA256) for `confidential` / `private` memories
- Key source priority: `AGENT_MEMORY_ENCRYPTION_KEY` env var > `.encryption_key` file
- Graceful degradation: if `cryptography` not installed, falls back to passthrough mode with warning
- Strict mode (`AGENT_MEMORY_ENCRYPTION_STRICT=true`, default): raises ValueError if encryption fails on sensitive content

### Mixin Composition
AgentMemory uses 13 Mixins for behavior composition:
- MemoryMixin, RecallMixin, SessionMixin, MaintenanceMixin
- DistillMixin, EncyclopediaMixin, TimelineMixin, StatsMixin
- PersonaMixin, RoleMixin, MediaStyleMixin, ReactorMixin, ExportMixin

### Dependency Injection
ComponentContainer manages component lifecycle with lazy instantiation via factory lambdas.

### Storage Layer
- **Primary**: SQLite with WAL mode (`store/` package)
  - `_core.py` — MemoryStore: Core CRUD operations, query engine
  - `_schema.py` — SchemaMigrator: Database schema creation and migrations
  - `_tasks.py` — TaskManager: Memory-related TODOs and reminders
  - `_maintenance.py` — MaintenanceManager: Optimize, vacuum, integrity check
  - `_file_lock.py` — _FileLock: Cross-process file locking (non-SQLite resources)
- **Vectors**: sqlite-vec extension (`embedding_store.py`), with ChromaDB fallback (v12)
- **Encrypted**: CryptoStore proxy (`storage/crypto_store.py`)
- **Alternative backends**: AbstractMemoryStore → SqliteMemoryStore / PostgresMemoryStore

### Data Flow
1. **Write**: User → AgentMemory.remember() → IngestPipeline → CryptoStore → Store + EmbeddingStore
2. **Read**: User → AgentMemory.recall() → RecallEngine → FTS5 + BM25 + Semantic + Entity + Causal → 5-Lane RRF Fusion → Temporal Filter → Ranked Results
3. **Maintain**: Scheduled → MaintainEngine → Decay + Distill + SelfHealing

### Spirit Butler
Dual-LLM security protocol with natural language command interface.
Isolated from core via SpiritInterface.

### Preference Memory
Structured preference tracking with 8-dimension design (food, music, work_style, communication, technology, entertainment, lifestyle, learning):
- Three-layer storage (raw → curated → explicit)
- Confidence decay with 180-day half-life
- Conflict detection and resolution
- Negative sample learning

### SkillEngine
`engines/skill.py` — Dynamic skill registration and execution framework.
Discovers, loads, and manages reusable skill modules that extend agent capabilities at runtime.

### MCP Server
`mcp_server.py` — V12 MCP Server exposing 11 tools for MCP-compatible agents:
- Supports official MCP SDK (stdio / streamable-http) and HTTP fallback
- Tools: remember, recall, context_for, correct, delete, spirit_check, get_profile, report, share_skill, learn_skill, command
- Rate limiting, authentication, and agent identity isolation
- Configured via `mcp_config.py` (MCPConfig dataclass)

### Protocol Interfaces
`protocols.py` — Defines 7 Protocol definitions (ABC interfaces) that decouple engine contracts from implementations:
MemoryStoreProtocol, EmbeddingStoreProtocol, RecallProtocol, IngestProtocol,
MaintainProtocol, CognitionProtocol, SkillProtocol.

### Sub-Managers
Specialized managers that handle cross-cutting concerns:
- **FTSManager** (`fts_manager.py`): Full-text search index lifecycle and rebuild
- **StoreCacheManager** (`store_cache_manager.py`): LRU cache layer over MemoryStore
- **AgentManager** (`agent_manager.py`): Multi-agent identity, routing, and isolation
- **SchemaMigrator** (`store/_schema.py`): Database schema creation and version migrations
- **TaskManager** (`store/_tasks.py`): Memory-related TODOs, reminders, and deadlines
- **MaintenanceManager** (`store/_maintenance.py`): Database optimize, vacuum, integrity check, stats

### DecayPolicy
Unified decay system (`decay_policy.py`) replacing per-engine decay logic.
Configurable policies (linear, exponential, step) with half-life parameters per memory tier.

### Recall Post-Processing Pipeline
`recall.py` — 7-step post-processing pipeline applied after TEMPR 5-lane retrieval and RRF fusion:

1. **_RankingStep** — Multi-dimensional quality ranking (importance × recency × feedback)
2. **_TemporalFilterStep** — Dual-timeline validity filtering (valid_from/valid_until)
3. **_FeedbackStep** — Feedback-based weight adjustments (useful/not-useful signals)
4. **_EmotionStep** — Emotion resonance bonus (capped at 0.10)
5. **_RerankStep** — Cross-encoder reranking (if FlagEmbedding reranker available)
6. **_MMRStep** — Maximal Marginal Relevance diversity reranking
7. **_EnrichmentStep** — Enrich results with version counts, links, cultural/phonetic associations, entity context

### Resilience Module
`resilience/` package providing fault-tolerance patterns for external service calls:

- **CircuitBreaker** (`resilience/circuit_breaker.py`): Three-state circuit breaker (CLOSED → OPEN → HALF_OPEN) with configurable failure threshold and recovery timeout. Prevents cascading failures when LLM/embedding services are down.
- **timeout_call** (`resilience/timeout.py`): Thread-based timeout wrapper for synchronous calls. Returns a default value if the call exceeds the deadline. Used in recall_engine to prevent slow queries from blocking.
- **CircuitOpenError**: Raised when a circuit is open and the request is rejected.
- **TimeoutError**: Raised when a call exceeds its deadline.

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      AgentMemory (13 Mixins)                     │
├─────────────────────────────────────────────────────────────────┤
│  IngestEngine  │  RecallEngine (TEMPR 5-Lane)  │  MaintainEngine│  CognitionEngine
│                │  ┌──────────────────────────┐  │                │
│                │  │ Lane 1: FTS5 + LIKE       │  │                │
│                │  │ Lane 1.5: BM25 Index      │  │                │
│                │  │ Lane 2: Semantic Vector    │  │                │
│                │  │ Lane 3: Entity Expansion   │  │                │
│                │  │ Lane 4: Causal Chain       │  │                │
│                │  │ ─────────────────────────  │  │                │
│                │  │ 5-Lane RRF Fusion          │  │                │
│                │  │ ─────────────────────────  │  │                │
│                │  │ 7-Step Post-Processing:    │  │                │
│                │  │  Ranking → Temporal →      │  │                │
│                │  │  Feedback → Emotion →      │  │                │
│                │  │  Rerank → MMR → Enrichment │  │                │
│                │  └──────────────────────────┘  │                │
├─────────────────────────────────────────────────────────────────┤
│  TemporalReasoner  │  EntityResolver  │  MetacognitiveEngine     │
│  (Dual Timeline)   │  (3-Level Match) │  (Reflect & Correct)     │
├─────────────────────────────────────────────────────────────────┤
│  CryptoStore (Encryption Proxy)  │  DecayPolicy (Unified)       │
├─────────────────────────────────────────────────────────────────┤
│  Resilience: CircuitBreaker + timeout_call                      │
├─────────────────────────────────────────────────────────────────┤
│                     Storage Layer (store/ package)               │
│  ┌──────────────────────────────────────────────────┐           │
│  │  MemoryStore (_core.py)                           │           │
│  │  SchemaMigrator (_schema.py)  TaskManager (_tasks)│           │
│  │  MaintenanceManager (_maintenance.py)             │           │
│  │  _FileLock (_file_lock.py)                        │           │
│  └──────────────────────────────────────────────────┘           │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │ EmbeddingStore│  │ PostgreSQL   │                            │
│  │ vec0/ChromaDB │  │ (Optional)   │                            │
│  └──────────────┘  └──────────────┘                            │
├─────────────────────────────────────────────────────────────────┤
│  Unified Config (settings.py)  │  MCP Server (mcp_server.py)    │
│  Env > JSON > Defaults         │  11 Tools / stdio / HTTP       │
└─────────────────────────────────────────────────────────────────┘
```

## Migration Status (v12.x)
Root modules (recall.py, pipeline.py, decay.py, etc.) are deprecated in favor of engines/ equivalents.
See individual class docstrings for migration guidance.
