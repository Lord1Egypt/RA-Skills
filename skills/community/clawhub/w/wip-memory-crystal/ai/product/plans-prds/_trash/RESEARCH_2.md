# Memory Crystal: Technical Research Document

## Sovereign, Self-Hosted Memory System for AI Agents
### An OpenClaw Plugin Providing Supermemory-Level Functionality, Fully Local

**Date:** 2026-02-07
**Status:** Research Phase
**Target:** OpenClaw plugin (`@openclaw/memory-crystal`)

---

## Table of Contents

1. [Vector Search Infrastructure (Local)](#1-vector-search-infrastructure-local)
2. [Knowledge Graph for Memory](#2-knowledge-graph-for-memory)
3. [Ingestion Pipeline](#3-ingestion-pipeline)
4. [Retrieval Quality](#4-retrieval-quality)
5. [Connectors / Ingestion Sources](#5-connectors--ingestion-sources)
6. [Memory Evolution](#6-memory-evolution)
7. [Existing Open Source Landscape](#7-existing-open-source-landscape)
8. [MCP Integration](#8-mcp-integration)
9. [Recommended Architecture](#9-recommended-architecture)

---

## 1. Vector Search Infrastructure (Local)

### Comparison Matrix

| Feature | sqlite-vec | LanceDB | ChromaDB | Qdrant (self-hosted) | pgvector |
|---|---|---|---|---|---|
| **Embedding** | Yes (SQLite ext) | Yes (library) | Yes (library) | No (server) | No (server) |
| **Node.js/TS SDK** | Yes (`sqlite-vec` npm) | Yes (native TS SDK) | Yes (JS client) | Yes (JS client) | Yes (via pg) |
| **ANN Index** | No (brute-force only) | Yes (IVF-PQ, HNSW) | Yes (HNSW via hnswlib) | Yes (HNSW) | Yes (HNSW, IVF) |
| **Full-Text/BM25** | Via FTS5 (SQLite native) | Yes (built-in BM25) | No (vector only) | Yes (sparse vectors) | Yes (tsvector) |
| **Hybrid Search** | Manual combo | Built-in | No | Built-in | Manual combo |
| **Disk-based** | Yes | Yes (Apache Arrow) | Partially (sqlite backend) | Yes | Yes |
| **Zero-config** | Yes | Yes | Yes | No (Docker) | No (Docker/install) |
| **Binary quantization** | Yes | Yes | No | Yes | No |
| **Matryoshka support** | Yes (truncatable) | Yes | No | Yes | No |

### Performance at Scale

**sqlite-vec (brute-force)**
- 10K chunks (768-dim float): ~2ms query latency
- 100K chunks (768-dim float): ~75ms query latency
- 1M chunks (128-dim float): ~17ms query (static), ~35ms (vec0 virtual table)
- 1M chunks (768-dim float): estimated ~100-200ms
- Bit vectors dramatically faster: 3072-dim bit vectors query in ~11ms at 100K scale
- **Limitation:** No ANN indexing; purely brute-force. Performance degrades linearly with dataset size.

**LanceDB (IVF-PQ + disk)**
- 10K chunks: <5ms query latency
- 100K chunks: ~25ms query latency
- 1M chunks: ~25ms with indexing (near in-memory from disk via memory-mapped Arrow)
- Achieves ~95% recall accuracy with advanced indexing
- **Strength:** Performance remains relatively flat due to IVF-PQ indexing. Best disk-to-query speed ratio.

**ChromaDB (HNSW)**
- 10K chunks: ~5ms query latency
- 100K chunks: ~10-20ms query latency
- 1M chunks: memory pressure issues; HNSW index held in-memory
- 2025 Rust-core rewrite delivers 4x faster writes and queries vs original Python implementation
- **Limitation:** Index must fit in memory for large collections.

**Qdrant (HNSW + quantization)**
- Best absolute performance at all scales
- 10K-1M chunks: consistently <10ms with proper configuration
- **Limitation:** Requires running a separate server (Docker). Overkill for single-user local.

**pgvector (HNSW)**
- Good up to ~10M vectors with <100ms latency
- Requires PostgreSQL installation
- **Limitation:** Heavy dependency for a local-first plugin.

### Recommendation: LanceDB

**LanceDB is the clear winner for memory-crystal.** Rationale:

1. **Embedded library** -- no server process, just `npm install @lancedb/lancedb`. Same deployment model as SQLite.
2. **Native TypeScript SDK** -- first-class Node.js/TS support, used by Continue IDE for exactly this use case.
3. **Built-in hybrid search** -- BM25 full-text search + vector similarity in one query, no manual fusion needed.
4. **Disk-efficient** -- Apache Arrow columnar format with memory-mapped access. Near in-memory speed from disk.
5. **Scales to 1M+** -- IVF-PQ indexing keeps query times flat. sqlite-vec degrades linearly.
6. **SQL-like filtering** -- metadata filtering built-in, important for time-based and source-based queries.

**Fallback consideration:** sqlite-vec is excellent as a lightweight fallback for <100K chunks. Its zero-dependency nature (pure SQLite extension) and bit-vector quantization support make it viable for a "lite mode." Consider offering both backends.

### Embedding Models

| Model | Dims | Context | Local? | Quality (MTEB) | Speed | Cost |
|---|---|---|---|---|---|---|
| **nomic-embed-text-v1.5** | 768 (truncatable to 256/384) | 8,192 tokens | Yes (Ollama) | Beats text-embedding-3-small | ~50ms/chunk (GPU) | Free |
| **all-MiniLM-L6-v2** | 384 | 256 tokens | Yes (ONNX/Ollama) | Lower (-5-8%) | ~15ms/chunk (CPU!) | Free |
| **text-embedding-3-small** | 1536 (truncatable) | 8,191 tokens | No (API) | Good baseline | ~20ms/chunk | $0.02/1M tokens |
| **nomic-embed-text-v2** | 768 | 8,192 tokens | Yes (Ollama) | SOTA open-source | ~60ms/chunk (GPU) | Free |
| **BGE-base-en-v1.5** | 768 | 512 tokens | Yes (ONNX) | Strong | ~30ms/chunk | Free |

### Recommendation: nomic-embed-text-v1.5

- Outperforms OpenAI text-embedding-3-small on both MTEB and long-context (LoCo) benchmarks
- 8,192 token context window (critical for larger chunks)
- Matryoshka representation learning: truncate to 256 dims for fast search, use full 768 for reranking
- Runs locally via Ollama with no API dependency
- **Fallback:** all-MiniLM-L6-v2 for CPU-only environments (384 dims, fast but lower quality, only 256 token context)
- **Optional:** text-embedding-3-small as a cloud option for users who prefer API-based embeddings

---

## 2. Knowledge Graph for Memory

### How Supermemory's Knowledge Graph Works

Based on their [blog post on the memory engine](https://supermemory.ai/blog/memory-engine/):

- **Hierarchical memory layers** inspired by human cognition: working memory, short-term memory, long-term storage
- Hot/recent data stays instantly accessible (uses Cloudflare KV for their hosted version)
- Deeper memories retrieved on-demand
- **Intelligent decay:** information gradually loses priority based on usage patterns
- **Continuous summary updates** across information clusters
- **Connection detection** between seemingly unrelated data
- **Non-literal query support** for semantic understanding
- Target: sub-400ms latency

Supermemory is primarily a cloud service. Their open-source components focus on the MCP server and browser extension, not the core memory engine.

### Mem0's Graph Memory Architecture

Source: [Mem0 Graph Memory docs](https://docs.mem0.ai/open-source/features/graph-memory), [Mem0 paper (arxiv)](https://arxiv.org/html/2504.19413v1)

Mem0g (graph variant) represents memories as a **directed labeled graph**:

- **Nodes** = entities (people, places, concepts, events) with types, embeddings, and metadata
- **Edges** = relationship triplets: `(source_entity, relation, destination_entity)`
- Uses **Neo4j** as the graph database backend

**Three-phase pipeline:**

1. **Extraction Phase:** An LLM-based extractor processes the most recent M messages, identifying entities and extracting candidate memory facts.

2. **Update Phase:** For each candidate fact, retrieves S most similar existing memories from the database. An LLM decides one of four operations via tool calling:
   - `ADD` -- new memory, no semantic equivalent exists
   - `UPDATE` -- augment existing memory with complementary info
   - `DELETE` -- remove memory contradicted by new info
   - `NOOP` -- no change needed

3. **Retrieval Phase:** Two strategies:
   - **Entity-centric:** identify key entities in query, find their nodes and relationships
   - **Semantic triplet:** encode entire query as dense embedding, match against relationship triplet embeddings

**Conflict detection:** When new info conflicts with existing relationships, an LLM-based resolver marks old relationships as obsolete (not deleted), preserving temporal reasoning.

**Performance:** 68.4% accuracy on DMR benchmark, 0.66s median search latency.

### Microsoft GraphRAG

Source: [Microsoft GraphRAG](https://microsoft.github.io/graphrag/)

GraphRAG builds entity-centric knowledge graphs by:
1. Extracting entities and relationships from text using LLMs
2. Grouping entities into thematic clusters ("communities") using graph algorithms (Leiden community detection)
3. Pre-computing LLM-generated summaries of each community
4. At query time, using community summaries + graph structure to augment prompts

**Key insight:** 70-80% superiority over traditional RAG for questions requiring "connecting the dots" across disparate information, while using 97% fewer tokens.

**Limitation for memory-crystal:** GraphRAG is designed for batch processing of static document corpora, not real-time incremental updates. It requires full recomputation when new data arrives.

### Zep/Graphiti Temporal Knowledge Graph

Source: [Graphiti GitHub](https://github.com/getzep/graphiti), [Zep paper (arxiv)](https://arxiv.org/abs/2501.13956)

Graphiti is the most relevant approach for agent memory:

- **Bi-temporal data model:**
  - Event Time (T): when a fact actually occurred
  - Ingestion Time (T'): when the system learned about it
- **Real-time incremental updates** -- no batch recomputation needed
- **Conflict resolution** with temporal awareness
- **Point-in-time queries** -- "What did I know on December 1st?"
- **P95 latency: 300ms**
- 18.5% accuracy improvement over baselines
- Supports Neo4j, FalkorDB, Kuzu as graph backends

**MCP server tools exposed:**
- `add_episode` -- add information to the knowledge graph
- `search_nodes` -- search for relevant entity summaries
- `search_facts` -- search for relevant facts/edges
- `delete_entity_edge` -- remove entities or edges
- `delete_episode` -- remove episodes

### Recommendation: Simplified Graph for memory-crystal

**Do not use Neo4j.** It is too heavy for a local-first, single-user OpenClaw plugin. Instead, implement a lightweight graph structure using SQLite (via better-sqlite3) alongside LanceDB:

```
Proposed Schema (SQLite):

entities:
  - id: TEXT PRIMARY KEY
  - name: TEXT
  - entity_type: TEXT (person, place, concept, project, preference, fact)
  - created_at: INTEGER (unix timestamp)
  - updated_at: INTEGER
  - access_count: INTEGER
  - last_accessed: INTEGER
  - decay_score: REAL (0.0-1.0)
  - summary: TEXT (LLM-generated, updated on consolidation)

relations:
  - id: TEXT PRIMARY KEY
  - source_entity_id: TEXT FK
  - target_entity_id: TEXT FK
  - relation_type: TEXT (e.g., "works_on", "prefers", "knows", "is_located_in")
  - weight: REAL (confidence/strength)
  - created_at: INTEGER
  - updated_at: INTEGER
  - valid_from: INTEGER (temporal: when fact became true)
  - valid_until: INTEGER (NULL = still valid)
  - source_memory_id: TEXT (which memory established this)

observations:
  - id: TEXT PRIMARY KEY
  - entity_id: TEXT FK
  - content: TEXT (atomic fact)
  - created_at: INTEGER
  - source_memory_id: TEXT
  - confidence: REAL

memories:
  - id: TEXT PRIMARY KEY
  - content: TEXT (original text)
  - contextualized_content: TEXT (with prepended context)
  - source_type: TEXT (imessage, browser, file, manual, conversation)
  - source_id: TEXT (file path, URL, chat ID, etc.)
  - chunk_index: INTEGER (position within source document)
  - created_at: INTEGER
  - updated_at: INTEGER
  - access_count: INTEGER
  - last_accessed: INTEGER
  - decay_score: REAL
  - is_active: BOOLEAN
  - superseded_by: TEXT (FK to newer memory, for contradiction handling)
```

**Graph operations** implemented as SQLite queries with recursive CTEs for traversal. This avoids the Neo4j dependency while providing the essential graph capabilities:
- Entity-to-entity traversal (2-3 hops)
- Temporal queries (valid_from/valid_until)
- Decay-weighted retrieval
- Community detection via simple connected-components algorithm

---

## 3. Ingestion Pipeline

### Chunking Strategy Comparison

| Strategy | Quality | Speed | Complexity | Best For |
|---|---|---|---|---|
| **Fixed-size** | Low | Fastest | Trivial | Prototyping only |
| **Recursive character splitting** | Good | Fast | Low | General text, markdown |
| **Semantic chunking** | Best (+2-9% recall) | Slow (needs embeddings) | Medium | Long documents, mixed content |
| **AST-aware (tree-sitter)** | Best for code | Medium | Medium | Source code |
| **Document-structure-aware** | Best for structured docs | Medium | Medium | PDFs, HTML |

### Recommended Chunking Pipeline

**Phase 1: Content-type detection and routing**

```
Input -> detect_content_type() -> route to chunker:
  - .md, .txt         -> MarkdownChunker (recursive, heading-aware)
  - .ts, .js, .py, etc. -> CodeChunker (tree-sitter AST-aware)
  - .pdf               -> PDFChunker (page + paragraph-aware)
  - URL                 -> HTMLChunker (semantic blocks)
  - iMessage, email     -> ConversationChunker (message-group-aware)
```

**Phase 2: Chunking**

Start with **recursive character splitting at 400-512 tokens with 10-20% overlap**, which is the established best practice and LangChain default. Graduate to semantic chunking if retrieval metrics warrant the extra compute cost.

For code, use [supermemory/code-chunk](https://github.com/supermemoryai/code-chunk):
- TypeScript library, AST-aware via tree-sitter
- Splits at semantic boundaries (functions, classes, methods)
- Five-step process: Parse -> Extract -> Build Scope Tree -> Chunk -> Enrich
- Produces `contextualizedText` with scope chain, entity definitions, sibling info, and import dependencies
- Supports: TypeScript, JavaScript, Python, Rust, Go, Java
- Config: `maxChunkSize: 1500`, `contextMode: 'full'`, `overlayLines: 10`

**Phase 3: Contextual enrichment (Anthropic's approach)**

Source: [Anthropic Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)

Before embedding each chunk, prepend a 50-100 token context summary that situates the chunk within the larger document:

```
Prompt template:
"Here is the document: <document>{WHOLE_DOCUMENT}</document>
Here is the chunk we want to situate: <chunk>{CHUNK_CONTENT}</chunk>
Please give a short succinct context to situate this chunk within
the overall document for the purposes of improving search retrieval
of the chunk. Answer only with the succinct context and nothing else."
```

**Performance impact:**
- Contextual Embeddings alone: 35% reduction in retrieval failures
- Contextual Embeddings + Contextual BM25: 49% reduction in failures
- Combined with reranking: **67% reduction** in failures

**Cost optimization:** Use Anthropic's prompt caching (or a smaller/local model) to generate context. Estimated cost: ~$1.02 per million document tokens with prompt caching. For fully local: use a small local LLM (e.g., Llama 3.2 3B via Ollama) for context generation.

**Phase 4: Embedding and indexing**

```
chunk + contextual_prefix -> embed(nomic-embed-text-v1.5) -> store in LanceDB
chunk + contextual_prefix -> tokenize -> BM25 index (LanceDB FTS)
chunk -> extract_entities_and_relations() -> store in SQLite graph
```

### Content-Type Specific Strategies

**Markdown:** Split on headings (##, ###), then recursive split within sections. Preserve heading hierarchy as metadata.

**Code:** Use code-chunk library. Preserve function/class scope chains. Include import context.

**PDFs:** Extract text per page, then recursive split. Preserve page numbers as metadata. Consider table extraction separately.

**URLs/HTML:** Strip boilerplate (navigation, footers), extract main content, split on semantic blocks (paragraphs, sections).

**Conversations (iMessage, email):** Group by conversation thread. Chunk by message groups (not individual messages). Preserve sender and timestamp metadata.

---

## 4. Retrieval Quality

### Hybrid Search Architecture

```
Query
  |
  v
[Query Rewriter] -- optional: rephrase for better retrieval
  |
  v
+---+---+
|       |
v       v
[Vector Search]    [BM25 Keyword Search]
(LanceDB ANN)     (LanceDB FTS)
|       |
v       v
[Reciprocal Rank Fusion]
  |
  v
[Reranker] -- cross-encoder rescore top-K
  |
  v
[Top-N Results]
```

### Hybrid Search: Vector + BM25

LanceDB supports this natively. The fusion approach:

```typescript
// LanceDB hybrid search (conceptual)
const results = await table
  .search(queryEmbedding)    // vector similarity
  .fullTextSearch(queryText)  // BM25
  .rerank(RRF())             // Reciprocal Rank Fusion
  .limit(20)
  .execute();
```

**Reciprocal Rank Fusion (RRF)** formula:
```
RRF_score(d) = sum(1 / (k + rank_i(d))) for each ranking system i
```
Where k=60 is standard. This elegantly combines rankings without needing normalized scores.

An alternative composite scoring approach:
```
FinalScore = (VectorScore * 0.5) + (KeywordScore * 0.3) + (RecencyScore * 0.2)
```

### Query Rewriting / HyDE

Source: [HyDE paper](https://arxiv.org/abs/2212.10496)

**HyDE (Hypothetical Document Embeddings):**
1. Given a user query, use an LLM to generate a hypothetical "ideal answer document"
2. Embed this hypothetical document instead of the raw query
3. Search the vector store with this embedding
4. The hypothetical document captures relevance patterns even if details are inaccurate

**When to use HyDE:** Complex, abstract, or multi-faceted queries where the raw query embedding poorly matches stored chunks. For simple factual queries, direct embedding is sufficient.

**Implementation for memory-crystal:**
```typescript
async function hydeSearch(query: string): Promise<SearchResult[]> {
  const hypothetical = await llm.generate(
    `Write a short paragraph that would be the ideal answer to: "${query}"`
  );
  const embedding = await embed(hypothetical);
  return vectorStore.search(embedding);
}
```

**Cost consideration:** HyDE requires an LLM call per query. Use it selectively -- when the initial retrieval returns low-confidence results, retry with HyDE.

### Reranking

**Options (ranked by preference for local-first):**

1. **Local cross-encoder (recommended):** `cross-encoder/ms-marco-MiniLM-L-6-v2`
   - Runs locally via ONNX runtime or sentence-transformers
   - 200-500ms latency for reranking 20 documents
   - 20-35% accuracy improvement over vector-only retrieval
   - No API dependency

2. **Cohere Rerank 4:** Best quality, but requires API call ($1/1K searches)
   - Self-learning capability (improves with usage)
   - For users who want best-in-class reranking

3. **LLM-as-reranker:** Use the agent's own LLM to score relevance
   - Most flexible, works with any model
   - Higher latency, higher cost

**Recommendation:** Ship with local cross-encoder reranking as default. Retrieve top-50, rerank to top-10, pass to LLM.

### Contextual Retrieval vs Naive RAG

Performance comparison from Anthropic's research:

| Approach | Retrieval Failure Rate | Improvement |
|---|---|---|
| Naive RAG (vector only) | 5.7% | Baseline |
| + BM25 Hybrid | 4.1% | -28% |
| + Contextual Embeddings | 3.7% | -35% |
| + Contextual Embeddings + BM25 | 2.9% | -49% |
| + Contextual + BM25 + Reranking | **1.9%** | **-67%** |

**memory-crystal should implement the full stack:** Contextual embeddings + BM25 hybrid search + reranking. This is the state of the art for retrieval quality.

---

## 5. Connectors / Ingestion Sources

### Priority 1: macOS Native Sources

#### iMessage History

**Location:** `~/Library/Messages/chat.db`

**Access requirements:**
- Full Disk Access permission required (System Settings > Privacy & Security > Full Disk Access)
- SQLite database with WAL mode (three files: chat.db, chat.db-shm, chat.db-wal)

**Schema (key tables):**
- `message` -- message text, timestamps, is_from_me flag
- `handle` -- contacts (phone numbers, email addresses)
- `chat` -- conversation threads
- `chat_message_join` -- links messages to chats
- `chat_handle_join` -- links handles to chats
- `attachment` -- file attachments with local paths

**Important caveat (macOS Ventura+):** Messages are no longer stored as plain text. The `attributedBody` column contains a hex-encoded blob that must be decoded. The `text` column may be NULL for newer messages.

**Implementation approach:**
```typescript
import Database from 'better-sqlite3';

const db = new Database(
  path.join(os.homedir(), 'Library/Messages/chat.db'),
  { readonly: true, fileMustExist: true }
);

// Query messages with contact info
const messages = db.prepare(`
  SELECT
    m.ROWID, m.text, m.attributedBody,
    m.date/1000000000 + 978307200 as unix_timestamp,
    m.is_from_me,
    h.id as contact_id,
    c.display_name as chat_name
  FROM message m
  JOIN chat_message_join cmj ON m.ROWID = cmj.message_id
  JOIN chat c ON cmj.chat_id = c.ROWID
  LEFT JOIN handle h ON m.handle_id = h.ROWID
  ORDER BY m.date DESC
`).all();
```

**Note on WAL:** The main database file may lag several seconds or minutes behind real-time. For near-real-time monitoring, also read from chat.db-wal.

#### Apple Notes

**Location:** `/Users/{username}/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite`

**Challenges:**
- Note content stored in `ZICNOTEDATA.ZDATA` as a gzip-compressed blob
- Decompressed data is in Apple's proprietary protobuf-like binary format
- Requires reverse-engineering or using existing parsers

**Best approach:** Use [dogsheep/apple-notes-to-sqlite](https://github.com/dogsheep/apple-notes-to-sqlite) approach or call AppleScript/JXA to extract notes:
```typescript
// Via osascript (JXA)
const script = `
  const Notes = Application("Notes");
  const notes = Notes.notes();
  return notes.map(n => ({
    name: n.name(),
    body: n.plaintext(),
    created: n.creationDate().toISOString(),
    modified: n.modificationDate().toISOString(),
    folder: n.container().name()
  }));
`;
```

#### Browser History / Bookmarks

**Chrome:**
- History: `~/Library/Application Support/Google/Chrome/Default/History` (SQLite)
- Bookmarks: `~/Library/Application Support/Google/Chrome/Default/Bookmarks` (JSON)
- Key table: `urls` (url, title, visit_count, last_visit_time)

**Firefox:**
- History + Bookmarks: `~/Library/Application Support/Firefox/Profiles/<profile>/places.sqlite`
- Key tables: `moz_places` (url, title, visit_count), `moz_bookmarks`

**Safari:**
- History: `~/Library/Safari/History.db` (SQLite, requires Full Disk Access)
- Bookmarks: `~/Library/Safari/Bookmarks.plist`

**Implementation note:** Chrome and Firefox lock their database files while running. Copy the file first, or open with `SQLITE_OPEN_READONLY` and handle busy errors.

#### Clipboard History

**macOS native (macOS 26+):** macOS 26 introduces native Clipboard History via Spotlight, but programmatic access is limited.

**Privacy changes (macOS 16+):** Apps now require explicit user permission to read the pasteboard. This affects real-time clipboard monitoring.

**Recommended approach:** Rather than trying to access system clipboard history, integrate with existing clipboard managers:
- [Maccy](https://maccy.app/) stores history in a SQLite database
- Or implement a background clipboard watcher that explicitly monitors NSPasteboard changes (requires user consent)

### Priority 2: File System Sources

#### Local Files (Markdown, PDF, Code)

**Implementation:** Use a file watcher (chokidar or fs.watch) on configured directories:
```typescript
const watchPaths = [
  '~/Documents',
  '~/Projects',
  '~/Notes'
];

// On file change: re-ingest
// On new file: ingest
// On delete: mark memories as inactive
```

**PDF extraction:** Use `pdf-parse` or `pdfjs-dist` npm packages for text extraction.

**Code files:** Use the code-chunk library (see Section 3) for AST-aware chunking.

### Priority 3: Network Sources

#### Email (IMAP / Gmail API)

**IMAP approach (self-hosted, no Google dependency):**
```typescript
import Imap from 'imap';
// Connect to any IMAP server
// Fetch messages, extract body text
// Index by sender, subject, date
```

**Gmail API approach:** Requires OAuth2, Google Cloud project setup. More reliable but adds cloud dependency.

**Recommendation:** Start with IMAP for maximum self-hosted compatibility. Add Gmail API as an optional connector.

### Supermemory's Connectors

Supermemory offers: S3, Google Drive, Notion, OneDrive, web pages, custom connectors, browser extension (ChatGPT/Claude/Twitter integration), Raycast extension, and their [apple-mcp](https://github.com/supermemoryai/apple-mcp) which provides MCP tools for Messages, Notes, Contacts, Mail, Reminders, Calendar, and Maps.

### Connector Priority for memory-crystal

| Priority | Connector | Complexity | Value |
|---|---|---|---|
| P0 | Manual add (text/URL) | Low | Foundation |
| P0 | Local files (md, txt, code) | Low | High |
| P0 | Conversation history (agent chats) | Low | Critical |
| P1 | iMessage | Medium | High (personal context) |
| P1 | Browser history/bookmarks | Medium | High |
| P1 | Apple Notes | Medium | High |
| P2 | PDF ingestion | Medium | Medium |
| P2 | URL/webpage scraping | Medium | Medium |
| P2 | Email (IMAP) | High | Medium |
| P3 | Clipboard history | High | Low |
| P3 | Calendar events | Medium | Low |

---

## 6. Memory Evolution

### Handling Contradictory Memories

**Adopt mem0's approach** with temporal graph edges:

1. When new information conflicts with an existing memory:
   - Do NOT delete the old memory
   - Mark the old memory's relation as `valid_until = now`
   - Create a new memory/relation with `valid_from = now`
   - Set `old_memory.superseded_by = new_memory.id`
   - Keep old memory searchable for temporal queries ("What did I think about X last month?")

2. **LLM-based conflict detection:**
```typescript
async function resolveConflict(
  newFact: string,
  existingMemories: Memory[]
): Promise<'ADD' | 'UPDATE' | 'DELETE' | 'NOOP'> {
  const prompt = `Given this new information: "${newFact}"
  And these existing memories:
  ${existingMemories.map(m => `- ${m.content} (from ${m.created_at})`).join('\n')}

  Determine the action:
  - ADD: if this is genuinely new information
  - UPDATE: if this supplements/refines an existing memory
  - DELETE: if this contradicts and replaces an existing memory
  - NOOP: if this is already known

  Respond with the action and which existing memory (if any) is affected.`;

  return llm.generate(prompt);
}
```

### Memory Decay / Relevance Scoring

**Implement a composite decay score:**

```typescript
function calculateDecayScore(memory: Memory): number {
  const now = Date.now();
  const ageHours = (now - memory.created_at) / (1000 * 60 * 60);
  const timeSinceAccess = (now - memory.last_accessed) / (1000 * 60 * 60);

  // Exponential decay based on time since last access
  const temporalDecay = Math.pow(0.995, timeSinceAccess);

  // Access frequency boost (log scale)
  const accessBoost = Math.log2(memory.access_count + 1) / 10;

  // Importance weight (set by user or inferred)
  const importanceWeight = memory.importance || 0.5;

  // Composite score
  return Math.min(1.0, (temporalDecay * 0.5) + (accessBoost * 0.3) + (importanceWeight * 0.2));
}
```

**Decay update schedule:** Run decay recalculation:
- On every access (update `last_accessed`, increment `access_count`)
- Hourly background job for batch decay updates
- On retrieval, boost accessed memories

### Deduplication

**Multi-stage deduplication:**

1. **Exact match:** Hash-based dedup on raw content (SHA-256)
2. **Near-duplicate:** Cosine similarity threshold on embeddings (>0.95 = duplicate)
3. **Semantic duplicate:** LLM-based judgment for memories that express the same fact differently
   - "I'm allergic to shellfish" and "can't eat shrimp" should be detected as related
   - Merge into a consolidated memory with both observations attached

```typescript
async function deduplicateMemory(newMemory: Memory): Promise<DedupeResult> {
  // Stage 1: exact match
  const exactMatch = await findByHash(sha256(newMemory.content));
  if (exactMatch) return { action: 'skip', existing: exactMatch };

  // Stage 2: near-duplicate (vector similarity)
  const similar = await vectorSearch(newMemory.embedding, { threshold: 0.92 });
  if (similar.length > 0 && similar[0].score > 0.95) {
    return { action: 'skip', existing: similar[0] };
  }

  // Stage 3: semantic dedup (only for high-similarity matches)
  if (similar.length > 0 && similar[0].score > 0.85) {
    const isDuplicate = await llm.judge(
      `Are these two memories expressing the same fact?\n1: "${newMemory.content}"\n2: "${similar[0].content}"`
    );
    if (isDuplicate) return { action: 'merge', existing: similar[0] };
  }

  return { action: 'add' };
}
```

### Memory Consolidation

Periodically consolidate related memories into higher-level summaries:

1. **Cluster detection:** Find groups of memories with high mutual similarity
2. **Summary generation:** Use LLM to create a consolidated summary
3. **Hierarchy:** Keep both individual memories (for detail retrieval) and consolidated summaries (for overview retrieval)

```
Individual memories:
- "Prefers TypeScript over JavaScript" (2025-06)
- "Uses Neovim as primary editor" (2025-07)
- "Interested in Rust for performance-critical code" (2025-08)
- "Values type safety highly" (2025-09)

Consolidated memory (auto-generated):
- "Developer who strongly values type safety, primarily uses TypeScript and Neovim,
   with growing interest in Rust for performance-critical work."
```

**Schedule:** Run consolidation weekly or when a cluster exceeds N related memories.

---

## 7. Existing Open Source Landscape

### mem0

**Repository:** [github.com/mem0ai/mem0](https://github.com/mem0ai/mem0)
**License:** Apache 2.0
**Language:** Python (primary) + TypeScript SDK

**How it works:**
- Hybrid data store: vector DB (Qdrant, ChromaDB, pgvector, etc.) + graph DB (Neo4j) + key-value store
- LLM-based extraction: identifies facts, preferences, contextual info from conversations
- Four-operation update cycle: ADD/UPDATE/DELETE/NOOP
- Graph memory (Mem0g): entities + relationship triplets with conflict detection
- Factory pattern for pluggable backends (LlmFactory, EmbedderFactory, VectorStoreFactory, etc.)

**Performance:** 26% accuracy improvement over OpenAI's memory, 91% faster responses, 90% lower token usage vs full-context approaches.

**Relevance to memory-crystal:** Mem0's extraction/update pipeline is the gold standard. The ADD/UPDATE/DELETE/NOOP pattern should be adopted. However, mem0 requires Neo4j for graph memory (too heavy for local-first) and its TypeScript SDK is thinner than the Python implementation.

### Khoj

**Repository:** [github.com/khoj-ai/khoj](https://github.com/khoj-ai/khoj)
**License:** AGPL-3.0
**Language:** Python 51%, TypeScript 36%

**How it works:**
- Full self-hosted AI assistant with memory, search, and chat
- Supports multiple document formats: PDFs, Markdown, Notion, Word docs, org-mode
- Semantic search + RAG
- Docker deployment (docker-compose)
- Supports multiple LLMs: llama3, qwen, gemma, mistral, GPT, Claude, Gemini, Deepseek

**Relevance to memory-crystal:** Khoj is a full application, not a composable library/plugin. Its document ingestion patterns are useful reference, but it is too monolithic to integrate directly. AGPL license is also restrictive.

### Supermemory

**Repository:** [github.com/supermemoryai/supermemory](https://github.com/supermemoryai/supermemory)
**License:** Mixed (some components open-source)

**Key open-source components:**
- [supermemory-mcp](https://github.com/supermemoryai/supermemory-mcp) -- Universal Memory MCP server
- [apple-mcp](https://github.com/supermemoryai/apple-mcp) -- Apple-native MCP tools (Messages, Notes, Contacts, Mail, Reminders, Calendar, Maps)
- [code-chunk](https://github.com/supermemoryai/code-chunk) -- AST-aware code chunking (TypeScript, tree-sitter)

**Relevance to memory-crystal:** The code-chunk library should be used directly as a dependency. The apple-mcp patterns are useful reference for macOS connector implementation. The core memory engine is not open-source.

### Graphiti (Zep)

**Repository:** [github.com/getzep/graphiti](https://github.com/getzep/graphiti)
**License:** Apache 2.0
**Language:** Python

**How it works:**
- Temporal knowledge graph framework for AI agent memory
- Bi-temporal data model (event time + ingestion time)
- Real-time incremental updates (no batch recomputation)
- Supports Neo4j, FalkorDB, Kuzu
- MCP server with add_episode, search_nodes, search_facts tools

**Relevance to memory-crystal:** Best existing implementation of temporal memory graphs. The bi-temporal model should be adopted. However, Python-only and requires a graph database server.

### OpenMemory (CaviraOSS)

**Repository:** [github.com/CaviraOSS/OpenMemory](https://github.com/CaviraOSS/OpenMemory)

**How it works:**
- Dockerized: FastAPI + Postgres + Qdrant
- Uses Mem0 under the hood
- MCP server via SSE
- Tools: add_memories, search_memory, list_memories, delete_all_memories
- Five cognitive sectors for automatic content classification
- Time as a first-class dimension
- Fine-grained access control between apps and memories

**Relevance to memory-crystal:** Good reference for MCP tool design and access control patterns. Too heavy (Docker, Postgres, Qdrant) for embedded local-first use.

### MCP Memory Service (doobidoo)

**Repository:** [github.com/doobidoo/mcp-memory-service](https://github.com/doobidoo/mcp-memory-service)

**How it works:**
- ChromaDB + sentence transformers for semantic memory
- Designed for Claude Desktop, VS Code, Cursor, and 13+ AI tools
- Automatic 24-hour backup cycle
- Content + tag-based retrieval

**Relevance to memory-crystal:** Simplest existing MCP memory implementation. Good starting point for tool API design, but lacks graph memory, hybrid search, and memory evolution.

### Official MCP Knowledge Graph Memory Server

**Repository:** [github.com/modelcontextprotocol/servers/tree/main/src/memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)

**How it works:**
- Entities + Relations + Observations data model
- JSONL file storage
- Nine tools: create_entities, create_relations, add_observations, delete_entities, delete_observations, delete_relations, read_graph, search_nodes, open_nodes
- Simple string matching for search (no vector/semantic search)

**Relevance to memory-crystal:** The entity/relation/observation data model is well-designed and should be adopted. The tool API naming conventions should be followed. But it lacks vector search, embeddings, and any form of intelligence.

---

## 8. MCP Integration

### MCP Tool Design for memory-crystal

Based on analysis of existing MCP memory servers and best practices, memory-crystal should expose these tools:

#### Core Memory Tools

```typescript
// 1. Store a new memory
tool("memory_store", {
  content: string,           // the text content to remember
  source?: string,           // where it came from (file path, URL, "conversation", etc.)
  tags?: string[],           // user-defined tags
  importance?: number,       // 0.0-1.0, how important is this
}) -> { memory_id: string, entities_extracted: Entity[] }

// 2. Search memories (primary retrieval)
tool("memory_search", {
  query: string,             // natural language query
  limit?: number,            // max results (default: 10)
  source_filter?: string,    // filter by source type
  time_range?: { after?: string, before?: string },
  include_graph?: boolean,   // also return related entities/facts
}) -> { memories: Memory[], entities?: Entity[], relations?: Relation[] }

// 3. Recall everything about an entity
tool("memory_recall", {
  entity: string,            // entity name (person, project, concept)
}) -> { entity: Entity, observations: Observation[], relations: Relation[], related_memories: Memory[] }

// 4. Store a fact (structured)
tool("memory_fact", {
  subject: string,           // entity name
  relation: string,          // relationship type
  object: string,            // target entity or value
  source?: string,
}) -> { fact_id: string, action: 'added' | 'updated' | 'duplicate' }
```

#### Memory Management Tools

```typescript
// 5. List recent memories
tool("memory_list", {
  limit?: number,
  offset?: number,
  source_filter?: string,
}) -> { memories: Memory[], total: number }

// 6. Delete a memory
tool("memory_delete", {
  memory_id: string,
}) -> { success: boolean }

// 7. Ingest a file or URL
tool("memory_ingest", {
  path: string,              // file path or URL
  recursive?: boolean,       // for directories
}) -> { chunks_created: number, entities_extracted: number }

// 8. Get memory stats
tool("memory_stats") -> {
  total_memories: number,
  total_entities: number,
  total_relations: number,
  by_source: Record<string, number>,
  storage_size_mb: number,
}
```

#### Advanced Tools (Phase 2)

```typescript
// 9. Consolidate related memories
tool("memory_consolidate", {
  entity?: string,           // consolidate around an entity
  auto?: boolean,            // auto-detect clusters to consolidate
}) -> { consolidated: number, summaries_created: number }

// 10. Memory timeline
tool("memory_timeline", {
  entity?: string,
  time_range?: { after?: string, before?: string },
}) -> { events: TimelineEvent[] }
```

### MCP Resource Exposure

In addition to tools, expose memories as MCP resources:

```typescript
// Expose the full knowledge graph as a resource
resource("memory://graph", "The complete knowledge graph of entities and relations");

// Expose recent memories as a resource for context injection
resource("memory://recent", "Recent memories from the last 24 hours");

// Expose entity summaries as resources
resource("memory://entity/{name}", "Everything known about {name}");
```

### Best Practices for MCP Memory Servers

1. **Automatic context injection:** At the start of each conversation, automatically provide relevant recent memories and entity summaries as context. This is how the official MCP Knowledge Graph Memory server works -- "retrieval of all relevant information from a knowledge graph at the start of chat."

2. **Implicit memory capture:** After each agent conversation, automatically extract and store new facts/memories from the conversation. Do not require explicit "remember this" commands for basic facts.

3. **Transparent operation:** Always tell the user when memories are being stored or retrieved. Include source attribution in retrieved memories.

4. **Graceful degradation:** If the memory system is slow or unavailable, the agent should still function (just without memory context). Memory operations should not block the main conversation flow.

5. **Privacy controls:** Users must be able to:
   - See all stored memories
   - Delete any memory
   - Pause memory collection from specific sources
   - Export all memory data (data sovereignty)

---

## 9. Recommended Architecture

### High-Level Architecture

```
+------------------------------------------------------------------+
|                    memory-crystal OpenClaw Plugin                  |
+------------------------------------------------------------------+
|                                                                    |
|  +------------------+    +------------------+    +---------------+ |
|  |   MCP Server     |    |  Ingestion       |    | Background    | |
|  |   (Tools +       |    |  Pipeline        |    | Workers       | |
|  |    Resources)     |    |                  |    |               | |
|  |                   |    |  - Chunker       |    | - Decay calc  | |
|  |  memory_store     |    |  - Contextualizer|    | - Consolidate | |
|  |  memory_search    |    |  - Embedder      |    | - Dedup       | |
|  |  memory_recall    |    |  - Entity Extract |    | - Re-embed   | |
|  |  memory_fact      |    |  - Graph Builder |    |               | |
|  |  memory_ingest    |    |                  |    |               | |
|  |  memory_list      |    |                  |    |               | |
|  |  memory_delete    |    |                  |    |               | |
|  |  memory_stats     |    |                  |    |               | |
|  +--------+---------+    +--------+---------+    +-------+-------+ |
|           |                       |                       |        |
|  +--------v-----------------------v-----------------------v------+ |
|  |                    Memory Core                                | |
|  |                                                               | |
|  |  +-------------------+  +-------------------+                 | |
|  |  |    LanceDB        |  |    SQLite          |                | |
|  |  |    (Vector Store)  |  |    (Graph + Meta)  |                | |
|  |  |                   |  |                    |                 | |
|  |  |  - Embeddings     |  |  - Entities        |                | |
|  |  |  - BM25 Index     |  |  - Relations       |                | |
|  |  |  - Hybrid Search  |  |  - Observations    |                | |
|  |  |                   |  |  - Memory metadata |                | |
|  |  +-------------------+  +-------------------+                 | |
|  +---------------------------------------------------------------+ |
|                                                                    |
|  +---------------------------------------------------------------+ |
|  |                    Connectors                                  | |
|  |  [iMessage] [Notes] [Browser] [Files] [Email] [Clipboard]    | |
|  +---------------------------------------------------------------+ |
|                                                                    |
|  +---------------------------------------------------------------+ |
|  |                    Embedding Provider                          | |
|  |  [Ollama/nomic-embed] [OpenAI API] [ONNX Local]              | |
|  +---------------------------------------------------------------+ |
+------------------------------------------------------------------+
```

### Technology Stack

| Component | Technology | Rationale |
|---|---|---|
| **Runtime** | Node.js / TypeScript | OpenClaw plugin ecosystem |
| **Build** | tsup | Matches existing OpenClaw plugin pattern |
| **Vector Store** | LanceDB (`@lancedb/lancedb`) | Embedded, TS-native, hybrid search, disk-efficient |
| **Graph/Metadata** | SQLite (`better-sqlite3`) | Embedded, zero-config, performant for graph operations |
| **Embeddings (default)** | nomic-embed-text-v1.5 via Ollama | Local, free, SOTA quality, Matryoshka support |
| **Embeddings (fallback)** | text-embedding-3-small via OpenAI API | For users without GPU/Ollama |
| **Code Chunking** | `@supermemory/code-chunk` | AST-aware, tree-sitter, TypeScript native |
| **Text Chunking** | Custom recursive splitter | 400-512 tokens, heading-aware for markdown |
| **Reranking** | cross-encoder/ms-marco-MiniLM-L-6-v2 (ONNX) | Local, fast, significant quality improvement |
| **BM25** | LanceDB FTS (built-in) | No extra dependency |
| **MCP** | `@modelcontextprotocol/sdk` | Standard MCP server implementation |
| **File watching** | chokidar | Mature, cross-platform file watcher |

### Data Storage Layout

```
~/.openclaw/memory-crystal/
  config.json                  # User configuration
  lance/                       # LanceDB data directory
    memories.lance/            # Vector index + BM25 index
  crystal.db                   # SQLite: graph, metadata, memory records
  backups/                     # Automatic daily backups
    crystal-2026-02-07.db
    lance-2026-02-07/
```

### Configuration Schema (openclaw.plugin.json)

```json
{
  "id": "memory-crystal",
  "name": "Memory Crystal",
  "description": "Sovereign, self-hosted memory system for AI agents",
  "skills": ["./skills"],
  "configSchema": {
    "type": "object",
    "properties": {
      "dataDir": {
        "type": "string",
        "description": "Where to store memory data"
      },
      "embeddingProvider": {
        "type": "string",
        "enum": ["ollama", "openai", "onnx"],
        "default": "ollama"
      },
      "embeddingModel": {
        "type": "string",
        "default": "nomic-embed-text"
      },
      "ollamaBaseUrl": {
        "type": "string",
        "default": "http://localhost:11434"
      },
      "openaiApiKey": {
        "type": "string"
      },
      "autoIngestConversations": {
        "type": "boolean",
        "default": true
      },
      "connectors": {
        "type": "object",
        "properties": {
          "imessage": { "type": "boolean", "default": false },
          "appleNotes": { "type": "boolean", "default": false },
          "browserHistory": { "type": "boolean", "default": false },
          "localFiles": {
            "type": "object",
            "properties": {
              "enabled": { "type": "boolean", "default": false },
              "watchPaths": { "type": "array", "items": { "type": "string" } }
            }
          }
        }
      },
      "decay": {
        "type": "object",
        "properties": {
          "hourlyFactor": { "type": "number", "default": 0.995 },
          "consolidationThreshold": { "type": "number", "default": 10 }
        }
      }
    }
  }
}
```

### Implementation Phases

**Phase 1 (MVP):**
- LanceDB vector store with hybrid search
- SQLite graph (entities, relations, observations)
- Basic chunking (recursive character splitting for text, code-chunk for code)
- Memory CRUD via MCP tools (store, search, recall, delete, list)
- Manual ingestion (text, files, URLs)
- Ollama embedding integration
- Simple decay scoring

**Phase 2 (Intelligence):**
- Contextual retrieval (Anthropic's context-prepending approach)
- Local cross-encoder reranking
- LLM-based entity extraction and conflict resolution (ADD/UPDATE/DELETE/NOOP)
- Memory consolidation
- Semantic deduplication
- HyDE query expansion for complex queries

**Phase 3 (Connectors):**
- iMessage connector
- Apple Notes connector
- Browser history/bookmarks connector
- File watcher for local directories
- Automatic conversation ingestion

**Phase 4 (Advanced):**
- Email (IMAP) connector
- Clipboard history integration
- Memory timeline visualization
- Export/import (data sovereignty)
- Multi-agent memory sharing (with access controls)

---

## Sources

### Vector Databases
- [sqlite-vec GitHub](https://github.com/asg017/sqlite-vec)
- [LanceDB Documentation](https://docs.lancedb.com/)
- [LanceDB Full-Text Search](https://docs.lancedb.com/search/full-text-search)
- [Continue IDE + LanceDB Case Study](https://lancedb.com/blog/the-future-of-ai-native-development-is-local-inside-continues-lancedb-powered-evolution/)
- [ChromaDB vs Qdrant Comparison](https://zenvanriel.nl/ai-engineer-blog/chroma-vs-qdrant-local-development/)
- [SQLite vs Chroma Analysis](https://dev.to/stephenc222/sqlite-vs-chroma-a-comparative-analysis-for-managing-vector-embeddings-4i76)

### Knowledge Graphs and Memory
- [Supermemory Memory Engine Blog](https://supermemory.ai/blog/memory-engine/)
- [Mem0 Graph Memory Documentation](https://docs.mem0.ai/open-source/features/graph-memory)
- [Mem0 Architecture Paper (arXiv)](https://arxiv.org/html/2504.19413v1)
- [Microsoft GraphRAG](https://microsoft.github.io/graphrag/)
- [Zep/Graphiti Temporal Knowledge Graph Paper (arXiv)](https://arxiv.org/abs/2501.13956)
- [Graphiti GitHub](https://github.com/getzep/graphiti)
- [Graphiti + FalkorDB MCP](https://www.falkordb.com/blog/mcp-knowledge-graph-graphiti-falkordb/)
- [Memory in the Age of AI Agents Survey (arXiv)](https://arxiv.org/abs/2512.13564)

### Retrieval and RAG
- [Anthropic Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
- [HyDE Paper (arXiv)](https://arxiv.org/abs/2212.10496)
- [Chunking Strategies for RAG 2025](https://www.firecrawl.dev/blog/best-chunking-strategies-rag-2025)
- [Reranking Guide 2025](https://www.zeroentropy.dev/articles/ultimate-guide-to-choosing-the-best-reranking-model-in-2025)
- [Hybrid Search for AI Memory (Node.js + pgvector)](https://dev.to/the_nortern_dev/under-the-hood-building-a-hybrid-search-engine-for-ai-memory-nodejs-pgvector-3c5k)
- [BM25 Hybrid Search for AI Memory Server](https://dev.to/jakob_sandstrm_a11b3056c/vector-search-is-not-enough-why-i-added-bm25-hybrid-search-to-my-ai-memory-server-3h3l)

### Embedding Models
- [Supermemory: Best Open-Source Embedding Models Benchmarked](https://supermemory.ai/blog/best-open-source-embedding-models-benchmarked-and-ranked/)
- [Comparing Local Embedding Models for RAG](https://medium.com/@jinmochong/comparing-local-embedding-models-for-rag-systems-all-minilm-nomic-and-openai-ee425b507263)
- [Nomic Embed Matryoshka](https://www.nomic.ai/blog/posts/nomic-embed-matryoshka)

### Ingestion and Chunking
- [Supermemory code-chunk](https://github.com/supermemoryai/code-chunk)
- [Weaviate Chunking Strategies](https://weaviate.io/blog/chunking-strategies-for-rag)
- [Document Chunking: 70% Accuracy Boost](https://langcopilot.com/posts/2025-10-11-document-chunking-for-rag-practical-guide)

### macOS Data Sources
- [iMessage SQL Database Access](https://davidbieber.com/snippets/2020-05-20-imessage-sql-db/)
- [Deep Dive into iMessage](https://fatbobman.com/en/posts/deep-dive-into-imessage)
- [Apple Notes to SQLite](https://github.com/dogsheep/apple-notes-to-sqlite)
- [Browser History with SQLite](https://ellen.dev/exploring-browser-history.html)

### MCP and Memory Servers
- [Official MCP Knowledge Graph Memory Server](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)
- [MCP Memory Service (doobidoo)](https://github.com/doobidoo/mcp-memory-service)
- [OpenMemory (CaviraOSS)](https://github.com/CaviraOSS/OpenMemory)
- [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)
- [Mem0 OpenMemory MCP](https://mem0.ai/openmemory)

### Open Source Projects
- [mem0 GitHub](https://github.com/mem0ai/mem0)
- [Khoj GitHub](https://github.com/khoj-ai/khoj)
- [Supermemory GitHub](https://github.com/supermemoryai/supermemory)
- [Supermemory Apple MCP](https://github.com/supermemoryai/apple-mcp)
- [OkapiBM25 npm (Node.js BM25)](https://github.com/FurkanToprak/OkapiBM25)
