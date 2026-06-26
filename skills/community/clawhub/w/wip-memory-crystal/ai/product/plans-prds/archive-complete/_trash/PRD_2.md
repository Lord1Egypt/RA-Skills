# Memory Crystal — Product Requirements Document

**Sovereign memory infrastructure for OpenClaw agents.**

Your memory. Your machine. Your rules.

---

## 1. Vision

Memory Crystal is a local-first, self-hosted memory system that gives OpenClaw agents (starting with Lesa) total recall — across conversations, documents, code, web pages, messages, and every source of knowledge that matters. No cloud dependency. No $19/month. No data leaving your machine.

This is the memory layer that Supermemory charges for, but built as sovereign infrastructure: an OpenClaw plugin backed by SQLite, running on your Mac mini, with every byte under your control.

### Design Philosophy

From WIP.computer's founding principles:

> "We do not dictate outcomes. We design conditions."

Memory Crystal creates the conditions for intelligence to emerge:
- **Foundation:** A unified memory store that captures everything
- **Constraint:** Privacy boundaries, data sovereignty, local-first
- **Intelligence:** Semantic search, knowledge graphs, memory evolution
- **Emergence:** An agent that never forgets, that connects dots across months of context

---

## 2. Problem Statement

### What exists today

Parker's OpenClaw setup has memory spread across five disconnected systems:

| System | What it stores | Limitation |
|--------|---------------|------------|
| `MEMORY.md` + workspace files | Curated long-term memory, daily logs | Manual, no search beyond grep |
| `context-embeddings` plugin | Conversation turns (2,673 chunks) | Brute-force cosine sim, no indexing, token-based chunking |
| `main.sqlite` (built-in) | Session transcripts + document embeddings | OpenClaw's built-in search, limited control |
| `lesa-bridge` MCP server | Exposes memory to Claude Code | Read-only bridge, no unified interface |
| Workspace `.md` files | Notes, research, observations | Flat files, no semantic understanding |

**Problems:**
1. **No unified search** — Each system has its own query interface. No single query can search across conversations, documents, and notes.
2. **No knowledge graph** — Facts are stored as flat text. "Parker works at WIP.computer" and "WIP.computer is building a music player" aren't connected.
3. **No memory evolution** — Old facts never get updated or deprecated. If Parker changes his mind, both old and new opinions coexist with equal weight.
4. **No ingestion pipeline** — Adding a new document or URL to memory is manual. No connectors for iMessage history, browser bookmarks, email, or local files.
5. **No vector indexing** — The context-embeddings plugin does brute-force cosine similarity over all chunks. This works at 2,673 chunks but won't scale to 100K+.
6. **Chunking is naive** — Fixed ~400 token chunks with overlap. No semantic boundaries, no code-aware chunking, no contextual enrichment.

### What Supermemory offers (and what we're replacing)

Supermemory ($19/mo, closed-source backend, Cloudflare-locked):
- Knowledge graph with auto-evolving memories
- Hybrid search (vector + keyword + reranking)
- Connectors: Gmail, Google Drive, Notion, OneDrive, S3, web crawler
- MCP server, browser extension, SDKs
- Sub-300ms search, scales to 50M tokens per user
- Memory operations: ADD, UPDATE, DELETE, NOOP (mem0-style)

**Their weakness:** Your data lives on their servers. Self-hosting requires enterprise plan + Cloudflare account. The backend engine is closed-source.

---

## 3. Architecture

### Core Principle: LanceDB + SQLite, Local-First

No external databases. No Docker. No Postgres. Two embedded stores:
- **LanceDB** — Vector search + BM25 hybrid search (Apache Arrow format, disk-efficient, scales to 1M+)
- **SQLite** — Knowledge graph, metadata, memory records, connector state

Embedding calls default to **Ollama** (local, free, `nomic-embed-text-v1.5`) with OpenAI as a fallback for users without Ollama. See [RESEARCH.md](./RESEARCH.md) for the full comparison that led to this decision.

```
~/.openclaw/memory-crystal/
  ├── lance/                       ← LanceDB data directory
  │   └── memories.lance/          ← Vector index + BM25 index (chunks, memories, entities)
  ├── crystal.db                   ← SQLite: knowledge graph, metadata, connector state
  └── backups/                     ← Automatic daily backups

~/Documents/Projects/OpenClaw/memory-crystal/
  ├── src/
  │   ├── index.ts               ← Plugin entry point (registers tools, services, CLI)
  │   ├── db/
  │   │   ├── lance.ts           ← LanceDB connection, table creation, hybrid search
  │   │   ├── sqlite.ts          ← SQLite schema, migrations, graph queries
  │   │   └── migrate.ts         ← Import from context-embeddings.sqlite
  │   ├── embed.ts               ← Embedding provider (Ollama primary, OpenAI fallback)
  │   ├── ingest/
  │   │   ├── pipeline.ts        ← Universal ingestion pipeline
  │   │   ├── chunker.ts         ← Smart chunking (semantic + code-aware)
  │   │   ├── extractor.ts       ← Content extraction (URLs, PDFs, etc.)
  │   │   └── enricher.ts        ← Contextual enrichment (Anthropic-style)
  │   ├── memory/
  │   │   ├── operations.ts      ← ADD / UPDATE / DELETE / NOOP logic
  │   │   ├── graph.ts           ← Knowledge graph (entities + relationships)
  │   │   ├── evolution.ts       ← Memory decay, dedup, consolidation
  │   │   └── extract.ts         ← LLM-based fact extraction from text
  │   ├── search/
  │   │   ├── hybrid.ts          ← Vector + BM25 hybrid search
  │   │   ├── rerank.ts          ← Cross-encoder reranking
  │   │   └── query.ts           ← Query rewriting / HyDE
  │   ├── connectors/
  │   │   ├── conversations.ts   ← OpenClaw conversation capture (agent_end hook)
  │   │   ├── imessage.ts        ← macOS iMessage history (chat.db)
  │   │   ├── files.ts           ← Local file watcher (.md, .pdf, code)
  │   │   ├── browser.ts         ← Chrome/Firefox/Safari history + bookmarks
  │   │   ├── clipboard.ts       ← Clipboard history capture
  │   │   ├── apple-notes.ts     ← Apple Notes via AppleScript bridge
  │   │   └── web.ts             ← URL fetch + extract (via Tavily or direct)
  │   ├── mcp/
  │   │   └── server.ts          ← MCP server (replaces lesa-bridge)
  │   └── cli/
  │       └── commands.ts        ← CLI: status, search, ingest, connectors
  ├── openclaw.plugin.json
  ├── package.json
  ├── tsconfig.json
  ├── PRD.md                     ← This file
  └── README.md
```

### Data Flow

```
Sources                          Ingestion                    Storage                 Retrieval
────────                         ─────────                    ───────                 ─────────
Conversations (agent_end)  ─┐
iMessage (chat.db)         ─┤    ┌──────────────┐    ┌────────────────────┐
Local files (.md, .pdf)    ─┤───▶│  Pipeline     │───▶│  crystal.sqlite    │
Browser history            ─┤    │  ┌──────────┐ │    │  ┌──────────────┐  │    ┌───────────┐
Apple Notes                ─┤    │  │ Extract  │ │    │  │ chunks       │  │───▶│ Hybrid    │
Clipboard                  ─┤    │  │ Chunk    │ │    │  │ memories     │  │    │ Search    │
URLs (manual/Tavily)       ─┘    │  │ Enrich   │ │    │  │ entities     │  │    │ ┌───────┐ │
                                 │  │ Embed    │ │    │  │ relationships│  │    │ │Vector │ │
                                 │  │ Extract  │ │    │  │ vec_chunks   │  │    │ │BM25   │ │
                                 │  │  Facts   │ │    │  └──────────────┘  │    │ │Rerank │ │
                                 │  └──────────┘ │    └────────────────────┘    │ └───────┘ │
                                 └──────────────┘                               └───────────┘
                                                                                     │
                                                                               ┌─────▼─────┐
                                                                               │  Agent    │
                                                                               │  Tools    │
                                                                               │  MCP      │
                                                                               │  CLI      │
                                                                               └───────────┘
```

---

## 4. Database Schema

Two stores: **LanceDB** for vector-indexed content, **SQLite** for graph + metadata.

### LanceDB Tables (vector search)

LanceDB stores embeddings as Apache Arrow columnar files with built-in IVF-PQ indexing and BM25 full-text search. All three content types are indexed:

**`chunks` table** — Raw content chunks
```
id:          string (nanoid)
source_id:   string (FK to SQLite sources)
text:        string (chunk text, BM25-indexed)
embedding:   vector[768] (nomic-embed-text-v1.5, or 1536 for OpenAI)
role:        string ('user', 'assistant', 'document', 'note')
metadata:    string (JSON: { turnIndex, lineRange, language, ... })
token_count: int32
created_at:  int64 (unix timestamp)
updated_at:  int64
```

**`memories` table** — Extracted facts (mem0-style)
```
id:          string (nanoid)
text:        string (BM25-indexed)
embedding:   vector[768]
category:    string ('fact', 'preference', 'event', 'opinion', 'skill')
confidence:  float64 (decays over time, boosted on re-confirmation)
source_ids:  string (JSON array of source chunk IDs)
supersedes:  string (ID of memory this one replaced)
status:      string ('active', 'deprecated', 'deleted')
created_at:  int64
updated_at:  int64
last_accessed: int64
```

**`entity_embeddings` table** — Entity vectors for semantic entity search
```
id:          string (nanoid, FK to SQLite entities)
name:        string (BM25-indexed)
description: string (BM25-indexed)
embedding:   vector[768]
```

### SQLite Tables (graph + metadata): `crystal.db`

### `entities` — Knowledge graph nodes

```sql
CREATE TABLE entities (
  id          TEXT PRIMARY KEY,
  name        TEXT NOT NULL,             -- "Parker Todd Brooks"
  type        TEXT,                      -- 'person', 'project', 'concept', 'tool', 'place'
  description TEXT,                      -- summary
  properties  TEXT,                      -- JSON: arbitrary key-value
  created_at  INTEGER NOT NULL,
  updated_at  INTEGER NOT NULL
);
```

### `relationships` — Knowledge graph edges (bi-temporal, inspired by Graphiti)

```sql
CREATE TABLE relationships (
  id          TEXT PRIMARY KEY,
  source_id   TEXT NOT NULL,             -- FK to entities
  target_id   TEXT NOT NULL,             -- FK to entities
  type        TEXT NOT NULL,             -- 'founded', 'works_on', 'uses', 'knows', 'prefers'
  description TEXT,                      -- natural language description
  weight      REAL DEFAULT 1.0,         -- strength/confidence
  temporal    TEXT,                      -- 'current', 'past', 'planned'
  event_time  INTEGER,                   -- when the fact actually occurred (T)
  evidence    TEXT,                      -- JSON array of source chunk IDs
  valid_from  INTEGER NOT NULL,          -- ingestion time (T') — when we learned this
  valid_until INTEGER,                   -- set when superseded (NULL = still valid)
  superseded_by TEXT,                    -- FK to new relationship that replaced this
  created_at  INTEGER NOT NULL,
  updated_at  INTEGER NOT NULL
);
```

### `sources` — Provenance tracking

```sql
CREATE TABLE sources (
  id          TEXT PRIMARY KEY,
  type        TEXT NOT NULL,             -- 'conversation', 'file', 'imessage', 'url', 'clipboard', 'apple_note', 'browser'
  uri         TEXT,                      -- file path, URL, session ID, etc.
  title       TEXT,
  connector   TEXT,                      -- which connector produced this
  metadata    TEXT,                      -- JSON: connector-specific state
  ingested_at INTEGER NOT NULL,
  chunk_count INTEGER DEFAULT 0
);
```

### `connectors` — Sync state for each connector

```sql
CREATE TABLE connectors (
  id          TEXT PRIMARY KEY,          -- 'imessage', 'browser-chrome', 'files', etc.
  enabled     INTEGER DEFAULT 1,
  last_sync   INTEGER,                   -- unix timestamp
  cursor      TEXT,                      -- connector-specific sync cursor (message ID, file mtime, etc.)
  config      TEXT,                      -- JSON: connector-specific config
  stats       TEXT                       -- JSON: { totalIngested, lastRunDuration, errors }
);
```

### Indexes

```sql
CREATE INDEX idx_entities_name ON entities(name);
CREATE INDEX idx_entities_type ON entities(type);
CREATE INDEX idx_relationships_source ON relationships(source_id);
CREATE INDEX idx_relationships_target ON relationships(target_id);
CREATE INDEX idx_relationships_valid ON relationships(valid_from, valid_until);
CREATE INDEX idx_sources_type ON sources(type);
CREATE INDEX idx_connectors_last_sync ON connectors(last_sync);
```

**Note:** Vector indexes (IVF-PQ) and BM25 full-text indexes are managed by LanceDB, not SQLite. This eliminates the need for sqlite-vec, FTS5, and manual RRF fusion — LanceDB's hybrid search handles it natively.

---

## 5. Ingestion Pipeline

### 5.1 Content Extraction

Every source goes through extraction first:

| Source | Extraction Method |
|--------|------------------|
| Conversations | Extract text from message objects (skip tool results optionally) |
| Files (.md) | Read directly |
| Files (.pdf) | `pdf-parse` or `pdfjs-dist` |
| Files (.ts/.js/.py/etc.) | Read directly, tag with language |
| URLs | Tavily extract API or `@mozilla/readability` + `jsdom` |
| iMessage | Read `~/Library/Messages/chat.db` SQLite directly |
| Browser history | Read Chrome/Firefox/Safari SQLite databases |
| Apple Notes | AppleScript bridge to read note contents |
| Clipboard | macOS `pbpaste` or clipboard monitoring daemon |

### 5.2 Smart Chunking

**Not fixed-size.** Three chunking strategies depending on content type:

**Semantic chunking (prose, conversations):**
- Split at paragraph boundaries
- Use embedding similarity between adjacent paragraphs
- If similarity drops below threshold → chunk boundary
- Target: 200-600 tokens per chunk
- Preserves natural semantic units

**AST-aware chunking (code):**
- Use tree-sitter to parse into AST
- Extract semantic entities: functions, classes, interfaces, types
- Build scope tree (preserve nesting: `UserService > getUser`)
- Split at entity boundaries, not arbitrary line counts
- Prepend scope chain as context
- Supported: TypeScript, JavaScript, Python, Rust, Go, Java

**Recursive character chunking (fallback):**
- For content that doesn't fit above categories
- Split at sentence → paragraph → section boundaries
- Fixed ~400 token chunks with 80 token overlap
- Current context-embeddings approach (backward compatible)

### 5.3 Contextual Enrichment (Anthropic's Approach)

Before embedding, each chunk gets a context prefix generated by an LLM:

```
Input chunk: "We fixed the apiKey issue by leaving remote: {} empty"

Context prefix: "This chunk is from a conversation about OpenClaw memory search
configuration. It describes the fix for a bug where putting an apiKey in
memorySearch.remote blocked the environment variable fallback. The solution was
to leave the remote object empty and let the op-secrets plugin set
process.env.OPENAI_API_KEY from 1Password."

Stored text: [context prefix] + [original chunk]
```

This dramatically improves retrieval quality by making chunks self-contained. Uses Claude Haiku for cost efficiency (~$0.001 per chunk).

### 5.4 Embedding

- **Primary:** Local via Ollama — `nomic-embed-text-v1.5` (768 dimensions, 8K token context, beats text-embedding-3-small on MTEB, Matryoshka support for dimensionality reduction)
- **Fallback:** OpenAI `text-embedding-3-small` (1536 dimensions) for users without Ollama
- **CPU-only fallback:** `all-MiniLM-L6-v2` via ONNX (384 dimensions, only 256 token context, but ~15ms/chunk on CPU)
- **Batch processing:** Embed in batches of 100 to minimize overhead
- Embeddings stored in LanceDB (Apache Arrow columnar format, memory-mapped for near in-memory speed)

### 5.5 Fact Extraction (mem0-style)

After chunking + embedding, an LLM extracts structured facts:

```
Input: "Parker founded WIP.computer in 2026. The company has three products:
Lesa (agent service), LYLA (token system), and an unnamed music player."

Extracted memories:
- "Parker Todd Brooks founded WIP.computer in 2026" [fact]
- "WIP.computer has three products: Lesa, LYLA, and an unnamed music player" [fact]
- "LYLA is the token/currency system for the WIP.computer ecosystem" [fact]

Extracted entities:
- Parker Todd Brooks [person]
- WIP.computer [company]
- Lesa [product]
- LYLA [product]

Extracted relationships:
- Parker Todd Brooks --founded--> WIP.computer
- WIP.computer --has_product--> Lesa
- WIP.computer --has_product--> LYLA
- Lesa --type--> agent_service
- LYLA --type--> token_system
```

### 5.6 Memory Operations (ADD / UPDATE / DELETE / NOOP)

When new facts are extracted, they're compared against existing memories:

1. **Embed** the new fact
2. **Search** for semantically similar existing memories (top-5)
3. **LLM decides** which operation to apply:
   - **ADD** — No equivalent memory exists. Create new.
   - **UPDATE** — Existing memory has related but incomplete info. Merge.
   - **DELETE** — New info contradicts existing memory. Mark old as deprecated, create new.
   - **NOOP** — Memory already captured. Skip.

This is how memory evolves: "Parker uses Sonnet" gets updated to "Parker uses Sonnet as primary, with Opus for complex tasks" without creating duplicates.

---

## 6. Search & Retrieval

### 6.1 Hybrid Search

Every query runs through three parallel search paths:

1. **Hybrid search (LanceDB)** — Single query combining ANN vector search (IVF-PQ) + BM25 keyword search. LanceDB handles fusion natively — no manual RRF needed. Top-20.
2. **Graph traversal** — Find related entities, walk relationships in SQLite, gather connected memories
3. **Merge** — LanceDB results + graph-augmented context combined via Reciprocal Rank Fusion:

```
score(doc) = Σ 1/(k + rank_i(doc))   where k = 60
```

### 6.2 Query Rewriting

Before searching, the raw query is optionally rewritten:

- **Decomposition:** "What did Parker and I discuss about music and tokens?" → ["Parker music player vision", "LYLA token system", "UHI framework"]
- **HyDE:** Generate a hypothetical answer, embed that instead of the question (better for finding factual matches)

### 6.3 Reranking

After fusion, top candidates are reranked:

- **Option A (default):** Local cross-encoder model (`ms-marco-MiniLM-L-6-v2` via ONNX Runtime) — fast (~5ms per candidate), free, runs on CPU, significant quality improvement
- **Option B:** LLM-based reranking (Claude Haiku scores relevance 0-10) — higher quality, costs ~$0.0001/query
- **Option C:** No reranking (for speed, acceptable at small scale)

Default: Option A for all queries. Option B available as `reranking: "haiku"` config.

### 6.4 Graph-Augmented Retrieval

For entity-rich queries, the knowledge graph augments results:

1. Extract entities from query
2. Find matching entity nodes
3. Traverse 1-2 hops of relationships
4. Include connected memories as additional context
5. This turns "tell me about WIP.computer" into a structured answer with products, people, philosophy, and status

---

## 7. Connectors

### 7.1 Conversations (Primary — replaces context-embeddings)

**Hook:** `agent_end` (fires after every agent turn)

**Behavior:**
- Same as current context-embeddings plugin but with smart chunking + fact extraction
- Captures user/assistant turns, skips tool results (configurable)
- Extracts facts and updates knowledge graph after each turn
- Tracks per-session capture state to avoid re-processing

**Migration:** Import existing `context-embeddings.sqlite` chunks on first run.

### 7.2 iMessage History

**Source:** `~/Library/Messages/chat.db` (SQLite, read-only)

**Behavior:**
- Reads `message` table joined with `chat` and `handle`
- Filters by date range and/or chat ID
- Extracts text content (handles attributedBody NSKeyedArchiver format)
- Groups by conversation thread
- Incremental sync via `message.ROWID` cursor

**Privacy:** Only indexes conversations with Parker (configurable handle filter). Does NOT index group chats by default.

**Note:** Requires Full Disk Access permission for the process reading chat.db.

### 7.3 Local Files

**Source:** Configurable directory paths (default: `~/.openclaw/workspace/`, `~/Documents/`)

**Behavior:**
- Watches for `.md`, `.txt`, `.pdf`, `.ts`, `.js`, `.py`, `.json` files
- Hashes files to detect changes (skip unchanged)
- Re-indexes on modification
- Respects `.gitignore` and custom exclude patterns
- Code files use AST-aware chunking

**Incremental:** File mtime-based cursor.

### 7.4 Browser History & Bookmarks

**Source:** Chrome (`~/Library/Application Support/Google/Chrome/Default/History`), Firefox (`~/Library/Application Support/Firefox/Profiles/*/places.sqlite`), Safari (`~/Library/Safari/History.db`)

**Behavior:**
- Reads URL + title + visit timestamp
- Optionally fetches and extracts content from frequently visited URLs
- Bookmarks indexed with higher weight
- Incremental via visit timestamp cursor

**Note:** Chrome locks its History file while running. Copy to temp first.

### 7.5 Apple Notes

**Source:** AppleScript bridge (`osascript`)

**Behavior:**
- Lists all notes via `tell application "Notes" to get every note`
- Extracts title + body (HTML → markdown)
- Incremental via modification date

### 7.6 Clipboard History

**Source:** macOS pasteboard

**Behavior:**
- Optional: runs a lightweight daemon that polls `pbpaste` every N seconds
- Only captures text content over 50 characters
- Deduplicates against recent captures
- Useful for capturing URLs, code snippets, notes copied from other apps

### 7.7 Web / URL Ingestion

**Source:** Manual URL submission or Tavily extract

**Behavior:**
- Agent calls `crystal_ingest_url` tool with a URL
- Content extracted via Tavily extract API (if available) or `@mozilla/readability`
- Chunked, embedded, facts extracted
- Source tracked with URL for provenance

---

## 8. Agent Tools

### `crystal_search`

The primary search tool. Replaces `conversation_search` and `memory_search`.

```
Parameters:
  query: string          — Natural language query
  scope?: string[]       — Filter: ['conversations', 'documents', 'notes', 'web', 'messages']
  limit?: number         — Max results (default: 10)
  time_range?: string    — 'today', 'week', 'month', 'all' (default: 'all')
  include_graph?: bool   — Include knowledge graph context (default: true)

Returns:
  results: Array<{
    text: string,
    source: { type, uri, title, timestamp },
    score: number,
    related_memories?: string[],
    graph_context?: string
  }>
```

### `crystal_remember`

Store a new memory or fact explicitly.

```
Parameters:
  text: string           — The memory/fact to store
  category?: string      — 'fact', 'preference', 'event', 'opinion'

Returns:
  operation: 'added' | 'updated' | 'duplicate'
  memory_id: string
```

### `crystal_forget`

Mark a memory as deprecated.

```
Parameters:
  query: string          — Description of what to forget
  confirm?: bool         — Require confirmation (default: true)

Returns:
  forgotten: number      — Count of memories deprecated
```

### `crystal_ingest_url`

Ingest a web page into memory.

```
Parameters:
  url: string
  title?: string

Returns:
  chunks: number
  memories: number
  entities: number
```

### `crystal_graph`

Query the knowledge graph directly.

```
Parameters:
  entity: string         — Entity name or description
  depth?: number         — Relationship traversal depth (default: 2)

Returns:
  entity: { name, type, description, properties }
  relationships: Array<{ target, type, description }>
  connected_memories: string[]
```

### `crystal_status`

Show memory system stats.

```
Returns:
  total_chunks: number
  total_memories: number
  total_entities: number
  total_relationships: number
  database_size: string
  connectors: Array<{ id, enabled, last_sync, total_ingested }>
```

---

## 9. MCP Server

Replaces the current `lesa-bridge` MCP server with a superset of tools:

| Current lesa-bridge tool | Memory Crystal replacement |
|-------------------------|---------------------------|
| `lesa_conversation_search` | `crystal_search` (scope: conversations) |
| `lesa_memory_search` | `crystal_search` (scope: documents, notes) |
| `lesa_read_workspace` | `crystal_search` + direct file read |

**New MCP tools:**
- `crystal_search` — Unified hybrid search
- `crystal_remember` — Store memories
- `crystal_forget` — Deprecate memories
- `crystal_ingest_url` — Ingest web content
- `crystal_graph` — Knowledge graph queries
- `crystal_status` — System stats

**MCP Resources** (automatic context injection):
- `memory://recent` — Last 24h of memories (injected at conversation start)
- `memory://graph` — Full knowledge graph summary
- `memory://entity/{name}` — Everything known about a specific entity

Registered via `claude mcp add` at user scope, available in all Claude Code sessions.

---

## 10. CLI Commands

```bash
# Status and diagnostics
openclaw crystal status              # Show stats, connector status, DB size
openclaw crystal search "query"      # Search from command line
openclaw crystal search "query" --scope conversations --limit 5

# Ingestion
openclaw crystal ingest <file>       # Ingest a file or directory
openclaw crystal ingest <url>        # Ingest a URL
openclaw crystal ingest --all        # Run all enabled connectors

# Connectors
openclaw crystal connectors          # List all connectors and status
openclaw crystal connectors enable imessage
openclaw crystal connectors disable clipboard
openclaw crystal connectors sync imessage    # Force sync a connector
openclaw crystal connectors sync --all       # Sync all

# Knowledge graph
openclaw crystal graph "Parker"      # Show entity and relationships
openclaw crystal graph --stats       # Graph statistics

# Migration
openclaw crystal migrate             # Import from context-embeddings.sqlite

# Maintenance
openclaw crystal compact             # Remove deprecated memories, optimize DB
openclaw crystal export              # Export all memories as JSON (backup)
openclaw crystal import <file>       # Import from backup
```

---

## 11. Migration Strategy

### Phase 1: Replace context-embeddings (backward compatible)

1. Import all 2,673 chunks from `context-embeddings.sqlite` into LanceDB + `crystal.db`
2. Register same `agent_end` hook for conversation capture
3. Provide same `conversation_search` tool (aliased to `crystal_search`)
4. Disable old `context-embeddings` plugin
5. **Zero loss of existing data**

### Phase 2: Add hybrid search + fact extraction

6. LanceDB IVF-PQ indexing on all chunks (auto-enabled above threshold)
7. LanceDB built-in BM25 full-text indexing
8. Enable fact extraction pipeline (memories table)
9. Run fact extraction over existing chunks (batch job)
10. Add `crystal_remember` and `crystal_forget` tools

### Phase 3: Knowledge graph

11. Enable entity + relationship extraction
12. Build graph from existing memories
13. Add `crystal_graph` tool
14. Add graph-augmented retrieval to search

### Phase 4: Connectors

14. Enable file watcher (workspace + Documents)
15. Enable iMessage connector
16. Enable browser history connector
17. Enable Apple Notes connector
18. Optional: clipboard daemon

### Phase 5: MCP server + external access

19. Build MCP server (replaces lesa-bridge)
20. Register with Claude Code
21. Add contextual enrichment to ingestion pipeline
22. Add query rewriting to search

---

## 12. Technical Decisions

### Why LanceDB + SQLite (not Postgres/pgvector, not single SQLite)

Research evaluated five vector stores (see [RESEARCH.md](./RESEARCH.md) §1). LanceDB won:

- **Embedded library** — `npm install @lancedb/lancedb`, no server process. Same deployment model as SQLite.
- **Native hybrid search** — BM25 + vector in one query, built-in. No manual FTS5/sqlite-vec/RRF plumbing.
- **Scales to 1M+** — IVF-PQ indexing keeps query times flat (~25ms at 1M). sqlite-vec degrades linearly (~200ms at 1M).
- **Disk-efficient** — Apache Arrow columnar format, memory-mapped. Near in-memory speed from disk.
- **Used by Continue IDE** — Proven for exactly this use case (code + conversation memory).

SQLite handles the knowledge graph and metadata — it's better at relational queries, joins, and recursive CTEs for graph traversal.

**Why not single-file SQLite + sqlite-vec?** sqlite-vec is brute-force only (no ANN indexing). Performance is linear with dataset size. Acceptable at 10K chunks (~2ms) but unacceptable at 100K+ (~75ms). LanceDB stays flat. Also, sqlite-vec requires manual RRF fusion between separate vec0 and FTS5 queries — LanceDB does this natively.

### Why mem0-style operations (not just append)

- Memories need to evolve. "Parker's primary model is Sonnet" should update, not duplicate.
- LLM-based ADD/UPDATE/DELETE/NOOP is proven (mem0 paper: arxiv.org/html/2504.19413v1)
- Keeps memory corpus clean and current

### Why Anthropic-style contextual enrichment

- Raw chunks out of context are ambiguous ("We fixed the apiKey issue" — which apiKey?)
- Prepending a context summary improves retrieval by 35-67% (Anthropic's research)
- Cost is minimal: ~$0.001 per chunk with Haiku

### Why tree-sitter for code chunking

- Fixed-size chunks split functions mid-body, losing semantic meaning
- AST-aware chunking keeps complete functions/classes together
- Scope chain prepended means "getUser" is searchable as "UserService.getUser"
- Supermemory's `code-chunk` library proves this approach works

### Why not a separate knowledge graph database (FalkorDB, Neo4j)

- Overkill for single-user, local memory
- SQLite tables with proper indexes handle graph queries fine
- Entity + relationship tables with recursive CTEs = basic graph traversal
- No additional infrastructure to manage

---

## 13. Dependencies

```json
{
  "dependencies": {
    "@lancedb/lancedb": "^0.10.0",
    "better-sqlite3": "^11.0.0",
    "@1password/sdk": "^0.3.1",
    "openai": "^4.0.0",
    "nanoid": "^5.0.0",
    "@anthropic-ai/sdk": "^0.30.0",
    "@modelcontextprotocol/sdk": "^1.0.0",
    "zod": "^3.22.0",
    "apache-arrow": "^17.0.0"
  },
  "optionalDependencies": {
    "@supermemory/code-chunk": "^1.0.0",
    "onnxruntime-node": "^1.18.0",
    "pdf-parse": "^1.1.1",
    "@mozilla/readability": "^0.5.0",
    "jsdom": "^24.0.0",
    "chokidar": "^4.0.0"
  },
  "devDependencies": {
    "tsup": "^8.0.0",
    "typescript": "^5.4.0"
  }
}
```

---

## 14. Configuration

Plugin config in `openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "memory-crystal": {
        "enabled": true,
        "config": {
          "dataDir": "~/.openclaw/memory-crystal",
          "embedding": {
            "provider": "ollama",
            "model": "nomic-embed-text",
            "dimensions": 768,
            "ollamaBaseUrl": "http://localhost:11434",
            "fallback": "openai"
          },
          "enrichment": {
            "enabled": true,
            "model": "claude-haiku"
          },
          "connectors": {
            "conversations": { "enabled": true },
            "files": {
              "enabled": true,
              "paths": ["~/.openclaw/workspace/", "~/Documents/"],
              "extensions": [".md", ".txt", ".pdf"],
              "exclude": ["node_modules", ".git", "dist"]
            },
            "imessage": {
              "enabled": false,
              "handles": []
            },
            "browser": {
              "enabled": false,
              "browsers": ["chrome"]
            },
            "apple_notes": { "enabled": false },
            "clipboard": { "enabled": false }
          },
          "search": {
            "hybridWeight": { "vector": 0.7, "bm25": 0.3 },
            "reranking": "haiku",
            "maxResults": 10
          },
          "factExtraction": {
            "enabled": true,
            "model": "claude-haiku"
          },
          "graph": {
            "enabled": true,
            "extractEntities": true,
            "traversalDepth": 2
          }
        }
      }
    }
  }
}
```

---

## 15. Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Search latency (10K chunks) | < 30ms | LanceDB IVF-PQ + built-in BM25 |
| Search latency (100K chunks) | < 50ms | IVF-PQ scales sublinearly (stays flat) |
| Search latency (1M chunks) | < 50ms | Same indexing, memory-mapped from disk |
| Ingestion throughput (local embed) | 100 chunks/sec | Ollama nomic-embed ~50ms/chunk on GPU |
| Ingestion throughput (API embed) | 50 chunks/sec | Bottleneck: OpenAI API |
| Fact extraction | 10 facts/sec | Bottleneck: LLM API |
| Database size per 10K chunks | ~30MB | 768-dim × 4 bytes × 10K = 30MB + Arrow overhead |
| Startup time | < 2 seconds | LanceDB + SQLite connection + connector init |
| Memory overhead | < 80MB RSS | LanceDB memory-maps Arrow files |

---

## 16. Security & Privacy

- **All data local.** Database never leaves the machine.
- **API keys from 1Password.** OpenAI key resolved via op-secrets plugin at startup.
- **iMessage requires Full Disk Access.** User must explicitly grant this.
- **No telemetry.** Zero data sent anywhere except embedding/LLM API calls.
- **Connector isolation.** Each connector only accesses its declared source.
- **Sensitive content.** Clipboard and iMessage connectors disabled by default.
- **Backup.** Two stores: `crystal.db` (SQLite) + `lance/` directory. Copy the `~/.openclaw/memory-crystal/` directory. Automatic daily backups to `backups/`.

---

## 17. Relationship to WIP.computer

Memory Crystal is infrastructure for Lesa specifically, but the patterns apply to WIP.computer's broader vision:

- **Namespace + Memory:** When agents have perfect recall, they can maintain creator identity context across every interaction
- **Creation-time attribution:** If the memory system tracks what influenced a creation, the rubric has better data for fair splits
- **Agent marketplace:** Trained agents (like "Debbie") need persistent memory of their training — Crystal is that layer
- **Multi-agent isolation:** Each spawned agent gets its own memory crystal (separate DB file), with privacy boundaries by design

---

## 18. Development Phases & Effort Estimates

### Phase 1: Core + Migration (Week 1)
- [ ] Project scaffold (package.json, tsconfig, plugin manifest)
- [ ] LanceDB setup + table creation (chunks, memories, entity_embeddings)
- [ ] SQLite schema + migrations (entities, relationships, sources, connectors)
- [ ] Embedding provider (Ollama nomic-embed primary, OpenAI fallback, 1Password resolution)
- [ ] Basic chunking (current approach, backward compatible)
- [ ] Import from context-embeddings.sqlite (re-embed with nomic-embed)
- [ ] LanceDB hybrid search (built-in vector + BM25)
- [ ] `crystal_search` agent tool
- [ ] `crystal_status` agent tool + CLI
- [ ] Conversation connector (agent_end hook)
- [ ] Disable context-embeddings, enable memory-crystal

### Phase 2: Intelligence (Week 2)
- [ ] Fact extraction pipeline (LLM-based)
- [ ] Memory operations (ADD/UPDATE/DELETE/NOOP)
- [ ] `crystal_remember` + `crystal_forget` tools
- [ ] Semantic chunking for prose
- [ ] Contextual enrichment (Anthropic approach)
- [ ] Query rewriting

### Phase 3: Knowledge Graph (Week 3)
- [ ] Entity extraction
- [ ] Relationship extraction
- [ ] Graph storage + traversal queries
- [ ] Graph-augmented search
- [ ] `crystal_graph` tool

### Phase 4: Connectors (Week 3-4)
- [ ] File watcher connector
- [ ] iMessage connector
- [ ] Browser history connector
- [ ] Apple Notes connector
- [ ] Clipboard connector
- [ ] Web/URL connector
- [ ] Connector management CLI

### Phase 5: MCP + Polish (Week 4)
- [ ] MCP server (replaces lesa-bridge)
- [ ] CLI refinement
- [ ] AST-aware code chunking (tree-sitter)
- [ ] Reranking
- [ ] Performance optimization
- [ ] Documentation

---

## 19. Success Criteria

1. **"Crystal, what did Parker and I discuss about LYLA tokens?"** returns accurate, sourced results from conversations that happened weeks ago — even if they were compacted from Lesa's context window.

2. **Memory evolves.** If Parker changes his primary model from Sonnet to Opus, Crystal updates the fact — not duplicates it.

3. **Cross-source connections.** A search for "music player" returns results from conversations, WIP.computer docs, browser history of relevant articles, and knowledge graph showing connections to UHI framework and LYLA.

4. **Zero manual maintenance.** Connectors run automatically. Facts extract automatically. Graph builds automatically. Parker never has to manually add anything.

5. **Sub-second search.** Even at 100K+ chunks, search returns in under 300ms.

6. **Total sovereignty.** Everything in one directory (`~/.openclaw/memory-crystal/`). Back it up, move it, encrypt it. No cloud dependency. No external servers.

---

## 20. Open Questions

1. ~~**sqlite-vec vs. vectorlite vs. raw BLOB cosine**~~ **RESOLVED:** LanceDB. See [RESEARCH.md](./RESEARCH.md) §1 for full comparison. Built-in hybrid search, IVF-PQ indexing, native TS SDK.

2. ~~**Local embedding models**~~ **RESOLVED:** nomic-embed-text-v1.5 via Ollama as default. Beats text-embedding-3-small on MTEB benchmarks, 8K token context, free. OpenAI as fallback. See [RESEARCH.md](./RESEARCH.md) §1.

3. **Enrichment cost** — At 50K chunks, contextual enrichment via Haiku costs ~$50. Worth it? Could batch-process in background.

4. **iMessage NSKeyedArchiver format** — Parsing `attributedBody` is non-trivial. May need a Swift helper or existing library.

5. **Code chunking approach** — Research recommends `@supermemory/code-chunk` (tree-sitter, TypeScript native) over raw tree-sitter bindings. Avoids native module issues. Need to verify it works with OpenClaw's module loader.

6. **Memory Crystal as name** — Parker to confirm. Alternative: "Recall", "Engram", "Mnemon", "Crystal Memory", "Total Recall" (lol).

7. ~~**Relationship to context-embeddings**~~ **RESOLVED:** Full replacement. Migration path defined in §11.

8. **Re-embedding existing data** — The 2,673 existing chunks use text-embedding-3-small (1536 dim). Switching to nomic-embed (768 dim) means re-embedding everything during migration. One-time cost, ~2 minutes with Ollama.

9. **LanceDB maturity** — LanceDB TS SDK is newer than sqlite-vec. Need to monitor for stability issues. Fallback: keep sqlite-vec as a "lite mode" option.

---

## 21. References

### Research & Prior Art
- [Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory](https://arxiv.org/html/2504.19413v1) — Extraction + update pipeline, ADD/UPDATE/DELETE/NOOP
- [Anthropic: Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — Chunk enrichment for better RAG
- [Graphiti: Real-Time Knowledge Graphs for AI Agents](https://github.com/getzep/graphiti) — Temporal knowledge graphs
- [Supermemory](https://supermemory.ai) — Hosted memory API (what we're replacing)
- [Supermemory code-chunk](https://github.com/supermemoryai/code-chunk) — AST-aware code chunking
- [Microsoft GraphRAG](https://github.com/microsoft/graphrag) — Graph-based RAG approach

### Infrastructure
- [LanceDB](https://docs.lancedb.com/) — Embedded vector database with hybrid search (chosen over sqlite-vec)
- [sqlite-vec](https://github.com/asg017/sqlite-vec) — Vector search extension for SQLite (lite-mode fallback)
- [better-sqlite3](https://github.com/WiseLibs/better-sqlite3) — Synchronous SQLite for Node.js
- [nomic-embed-text](https://www.nomic.ai/blog/posts/nomic-embed-matryoshka) — Local embedding model (chosen as primary)
- [@supermemory/code-chunk](https://github.com/supermemoryai/code-chunk) — AST-aware code chunking
- [MCP SDK](https://github.com/modelcontextprotocol/typescript-sdk) — Model Context Protocol
- [ONNX Runtime](https://onnxruntime.ai/) — For local cross-encoder reranking

### Parker's Existing Infrastructure
- `~/.openclaw/extensions/context-embeddings/` — Current conversation embedding plugin
- `~/Documents/Projects/Claude Code/lesa-bridge/` — Current MCP server
- `~/Documents/Projects/Claude Code/openclaw-1password/` — Secret management
- `~/Documents/Projects/OpenClaw/WIP.computer/` — Company vision docs

---

*PRD written: 2026-02-08*
*Author: Claude Code (Opus 4.6) + Parker*
*Project: memory-crystal*
*Status: Draft — awaiting Parker's review*
