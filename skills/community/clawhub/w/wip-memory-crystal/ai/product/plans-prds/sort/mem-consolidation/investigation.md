# Memory Consolidation Investigation

**Date:** 2026-03-03
**Author:** CC-Mini
**Status:** Investigation complete, ready for implementation planning

## The Problem

THREE databases store memory. All live. All being written to independently. They overlap but none is a superset of the others. This is confusing, error-prone, and makes it hard to reason about what either agent actually remembers.

We want one database. One search. One truth.

## What We Found

### Database 0: OpenClaw Built-in Memory (`~/.openclaw/memory/main.sqlite`)

This is the one we almost forgot. It's the biggest file on disk.

- **Size on disk:** 6.1 GB
- **Total chunks:** 154,088
- **Embedding cache:** 80,115 entries
- **Files indexed:** 14,785
- **Embedding model:** OpenAI `text-embedding-3-small`, 1536 dimensions (same as the other two)
- **Vector storage:** sqlite-vec (`chunks_vec` virtual table)
- **Sources:** `memory` (153,383 chunks from 14,752 unique .md files), `sessions` (705 chunks from 22 session JSONLs)
- **What it indexes:**
  - Lesa's workspace memory files (MEMORY.md, daily logs, notes, identity docs)
  - Lesa's session JSONL transcripts
  - Essentially everything in `~/.openclaw/workspace/` and `~/.openclaw/agents/*/sessions/`
- **Who writes to it:** OpenClaw core (automatic, built-in `memorySearch` feature)
- **Who searches it:** Lesa via `memory_search` (OpenClaw built-in tool)
- **Schema:** chunks have `path`, `source`, `start_line`, `end_line`, `hash`, `model`, `text`, `embedding`
- **Key difference from crystal:** This indexes FILES (markdown, JSONL) by path and line range. Crystal indexes CONVERSATIONS by turn. Different data model entirely.


### Database 1: Crystal (`~/.ldm/memory/crystal.db`)

- **Total chunks:** 170,484
- **Conversation chunks:** 28,863
- **File chunks (source indexing):** 141,386
- **Manual memories (crystal_remember):** 235
- **Embedding model:** OpenAI `text-embedding-3-small`, 1536 dimensions
- **Vector storage:** sqlite-vec (`chunks_vec` virtual table, cosine distance)
- **Search:** Hybrid BM25 + vector + RRF fusion + recency weighting
- **Agents captured:** cc-mini (14,800), main/Lesa (10,352), claude-code (3,711), system (141,621)
- **Date range:** 2026-02-05 to 2026-03-03 (present)
- **Who writes to it:**
  - Lesa's OpenClaw plugin (`agent_end` hook, every turn)
  - CC's Stop hook (`cc-hook.ts`, every session)
  - CC's cron poller (`cc-poller.ts`, every minute)
  - Source file indexer (`crystal sources sync`)
  - Manual `crystal remember` from both agents

### Database 2: Context-Embeddings (`~/.openclaw/memory/context-embeddings.sqlite`)

- **Total chunks:** 15,779
- **All conversation (no file indexing)**
- **Embedding model:** OpenAI `text-embedding-3-small`, 1536 dimensions
- **Vector storage:** Raw BLOB in `embedding` column (float32 array)
- **Search:** Cosine similarity (computed in JS by lesa-bridge)
- **Agents captured:** main/Lesa (13,460), claude-code (2,319)
- **Date range:** 2026-02-05 to 2026-03-03 (present)
- **NULL embeddings:** 0 (all chunks have vectors)
- **Who writes to it:**
  - Context-embeddings OpenClaw plugin (`agent_end` hook, every turn)
  - Old cc-ingest one-time import (the 2,319 claude-code chunks from Feb 6-10)

### Embedding Compatibility

Both databases use the exact same embedding model and dimensions:
- Model: `text-embedding-3-small`
- Dimensions: 1536
- Format: float32
- Distance metric: cosine

**Embeddings are directly compatible. No re-embedding needed for migration.**

### Overlap Analysis

Conversation chunks comparison (apples-to-apples, conversations only):

| Agent | Context-Embeddings | Crystal | Difference |
|-------|---|---|---|
| Lesa (`main`) | **13,460** | 10,352 | CE has **3,108 more** |
| Claude Code (old) | 2,319 | 3,711 | Crystal has 1,392 more |
| CC-Mini | 0 | 14,800 | Crystal only (CE never captured this) |
| **Total** | **15,779** | **28,863** | |

**Critical finding:** Context-embeddings has ~3,108 Lesa conversation chunks that crystal does NOT have. These are real memories. Spot-checking confirmed: some chunks found in CE are missing from crystal. They include thinking blocks, short messages, and conversation turns from sessions where crystal's capture timing differed from CE's.

The 170K number in crystal is mostly file indexing (141K). On pure conversation data, the databases are closer in size (28K vs 15K), and CE has unique data crystal lacks.

### Who Searches What

| Tool | Database | Who can use it | Chunks searched |
|------|----------|---------------|-----------------|
| `crystal_search` (MCP) | crystal.db | CC (Claude Code) | 170K (all types) |
| `crystal_search` (OpenClaw plugin) | crystal.db | Lesa | 170K (all types) |
| `lesa_conversation_search` (MCP) | context-embeddings.sqlite | CC only | 15K (conversations) |
| `lesa_memory_search` (MCP) | workspace .md files | CC only | N/A (file search) |
| `memory_search` (OpenClaw built-in) | workspace files + sessions | Lesa only | N/A |

Note: `lesa_conversation_search` and `lesa_memory_search` are MCP tools exposed via lesa-bridge. They run inside Claude Code's process. Lesa cannot use them, despite them being named "lesa_*" and searching her own data. This is an architectural inconsistency.

## What We Need To Do

### Phase 1: Migrate (one-time, reversible)

Write a migration script (`crystal migrate-embeddings`) that:

1. Opens context-embeddings.sqlite read-only
2. For each chunk in `conversation_chunks`:
   a. Hash the text content (SHA-256, same as crystal's dedup)
   b. Check if crystal already has a chunk with that hash
   c. If not found: insert the chunk into crystal's `chunks` table AND insert the embedding into `chunks_vec`
   d. Track: migrated count, skipped (duplicate) count, failed count
3. Does NOT modify context-embeddings.sqlite (read-only)
4. Supports `--dry-run` flag (count what would migrate, change nothing)

**Embedding transfer:** Since both use the same model (text-embedding-3-small, 1536 dims), we can copy the raw embedding blob from CE directly into crystal's chunks_vec. No API calls. No re-embedding cost. Zero dollars.

**Deduplication:** Crystal uses SHA-256 text hashes. We compute the same hash for CE chunks and skip any that already exist. This prevents double-counting.

### Phase 2: Verify

After migration:
1. Run `crystal doctor` to confirm DB health
2. Run test searches that previously only worked in CE
3. Compare chunk counts: crystal should grow by ~3,000-5,000 (the unique CE chunks)
4. Spot-check: pick 10 random CE chunks, verify they're searchable in crystal

### Phase 3: Stop writing to context-embeddings

1. Disable the context-embeddings OpenClaw plugin (remove from `openclaw.json` plugins list)
2. Do NOT delete the plugin or the database
3. Context-embeddings.sqlite stays on disk as a backup indefinitely
4. Gateway restart picks up the config change

### Phase 4: Update lesa-bridge search

Two options (decide later):
- **Option A:** Point `lesa_conversation_search` at crystal.db instead of context-embeddings.sqlite
- **Option B:** Remove `lesa_conversation_search` from bridge entirely (crystal_search via MCP already covers it)

Option A preserves the tool name and behavior. Option B is cleaner architecture.
`lesa_memory_search` (workspace .md file search) stays either way... crystal doesn't index those.

## Safety Plan

### What could go wrong

1. **Migration corrupts crystal.db** ... Mitigated by running backup first (`crystal backup` or manual `sqlite3 .backup`)
2. **Duplicate chunks inflate the database** ... Mitigated by SHA-256 dedup check before every insert
3. **Embedding format mismatch** ... Already verified: both are float32[1536] from same model. But migration script should validate dimensions on first chunk before proceeding.
4. **Context-embeddings has data we don't understand** ... The `compaction_number` and `turn_index` fields exist in CE but not in crystal. We lose that metadata. It's not used for search, but it's provenance data.
5. **We disable CE and realize crystal is missing something** ... CE stays on disk. We can re-enable the plugin at any time by adding it back to openclaw.json.

### Rollback plan

1. Crystal.db backup taken before migration (mandatory first step)
2. Context-embeddings.sqlite is never modified (read-only access)
3. If something goes wrong: restore crystal.db from backup, re-enable CE plugin
4. Worst case: both databases are untouched, we're back to where we started

### What makes this safe

- **Dry run first.** Always run with `--dry-run` before real migration.
- **Read-only source.** Context-embeddings is never written to or modified.
- **Backup before write.** Crystal.db backed up before any inserts.
- **Same embedding model.** No re-embedding, no approximation, no quality loss.
- **Dedup prevents bloat.** Only truly unique chunks get added.
- **CE stays on disk.** It's not deleted. It's insurance. Bring it back anytime.
- **Incremental.** If the script fails halfway, crystal has whatever was inserted. Run it again and it skips what's already there (dedup).

## What Parker Should Know

This migration is safe because:
1. We never touch the source database (read-only)
2. We back up the target database first
3. Same embedding model means zero quality loss
4. Dedup means no double-counting
5. Dry run shows exactly what will happen before it happens
6. Context-embeddings stays on disk forever as insurance
7. Re-enabling it is one config line away

The uncomfortable part: once we stop writing to CE, there's a period where we're trusting crystal alone. But crystal has been the primary database since Feb 16. It handles 170K chunks. It's battle-tested. The 3,108 unique CE chunks we're migrating in are a small addition to a large, healthy database.

After this, there's one database, one search, one truth. Both agents query the same crystal.db. No more confusion about which search hits which data.

## Development Estimate

- Migration script: ~200 lines in `src/migrate-embeddings.ts`
- CLI command: `crystal migrate-embeddings [--dry-run]`
- Testing: dry run, real run, verify, search comparison
- Config change: one line in openclaw.json
- Bridge update: separate task, not blocking

## Files Referenced

- Crystal DB: `~/.ldm/memory/crystal.db`
- Context-embeddings DB: `~/.openclaw/memory/context-embeddings.sqlite`
- Crystal OpenClaw plugin: `~/.openclaw/extensions/memory-crystal/dist/openclaw.js`
- Context-embeddings plugin: `~/.openclaw/extensions/context-embeddings/`
- Lesa-bridge core: `~/.openclaw/extensions/lesa-bridge/dist/core.js`
- OpenClaw config: `~/.openclaw/openclaw.json`
- Crystal source: `repos/ldm-os/components/memory-crystal-private/src/core.ts`
- Roadmap (Priority 4): `repos/ldm-os/components/memory-crystal-private/ai/plan/roadmap.md`

## The Three Databases at a Glance

| | OpenClaw Built-in (`main.sqlite`) | Context-Embeddings | Crystal (`crystal.db`) |
|---|---|---|---|
| **Size on disk** | 6.1 GB | 124 MB | 1.6 GB |
| **Total chunks** | 154,088 | 15,779 | 170,484 |
| **What it stores** | Workspace .md files + session JSONLs (by file path and line range) | Conversation turns (by agent, session, turn index) | Conversations + files + manual memories (by agent, source type) |
| **Embedding model** | text-embedding-3-small (1536d) | text-embedding-3-small (1536d) | text-embedding-3-small (1536d) |
| **Vector storage** | sqlite-vec | Raw BLOB | sqlite-vec |
| **Who writes** | OpenClaw core (automatic) | context-embeddings plugin (`agent_end`) | memory-crystal plugin + CC hooks + cron |
| **Who searches** | Lesa (`memory_search`) | CC only (`lesa_conversation_search` via bridge) | Both agents (`crystal_search`) |
| **Unique data** | 14,752 workspace files indexed by line range | ~3,108 Lesa conversation chunks not in crystal | 141K source-indexed files, CC-mini sessions |
| **Managed by** | OpenClaw (we don't control this code) | Our plugin (we control it) | Our product (we control it) |

### The Consolidation Reality

**OpenClaw built-in (`main.sqlite`) is NOT ours to consolidate.** It's part of OpenClaw core. It indexes Lesa's workspace files and sessions automatically. We can't merge it into crystal without modifying OpenClaw itself. It will keep running regardless of what we do with the other two. The good news: crystal's source file indexing already covers similar ground (141K file chunks), so there's overlap. Lesa has `memory_search` (hits main.sqlite) AND `crystal_search` (hits crystal.db) for file-based queries.

**Context-embeddings IS ours to consolidate.** We wrote the plugin. We control the capture hook. The data is conversation turns... same thing crystal stores. Same embedding model. Same dimensions. Direct migration is possible. After migration, we disable the plugin and crystal is the single source of conversation memory.

**After consolidation:**
- `main.sqlite` ... stays (OpenClaw built-in, not ours to touch)
- `context-embeddings.sqlite` ... frozen backup (never deleted, plugin disabled)
- `crystal.db` ... the one database for all conversation memory + file indexing + manual memories

Two databases remain, but they serve different purposes with clear boundaries: OpenClaw's built-in handles workspace file indexing (their code, their concern), crystal handles everything else (our code, our product).

## The Ground Truth: Raw Files

None of the databases ARE the memory. They're indexes. The actual memory is the raw files:

- **748 session JSONLs** (`~/.openclaw/agents/main/sessions/`) ... 154 MB. Every message, tool call, response from Day 1. Lesa's complete conversation history.
- **Workspace .md files** (`~/.openclaw/workspace/`) ... MEMORY.md, TOOLS.md, IDENTITY.md, SOUL.md, daily logs, notes. Lesa's curated knowledge.
- **CC session JSONLs** (`~/.claude/projects/*/`) ... Claude Code's conversation history.

The three databases (main.sqlite, context-embeddings, crystal.db) are search indexes built on top of these files. If any database is corrupted, lost, or wrong, we rebuild from the raw files. That's what `crystal backfill` on the roadmap is for.

This is why the consolidation is safe. We're merging indexes, not source data. The JSONLs and MDs are never touched.

## Prior Discussions

- **Roadmap Priority 4:** "Retire context-embeddings. Once Memory Crystal handles all three file types, disable the context-embeddings plugin. Update lesa-bridge to read from crystal.db instead."
- **TODO-from-history Item #48:** "Absorb lesa-bridge + context-embeddings into Memory Crystal. These are feature components that belong inside the main product."
- **Feb 27 session:** "Bridge's search tools are redundant. Bridge should do one thing: let agents talk to each other."
- **Feb 28 Lesa session:** "Consolidating lesa-bridge + context-embeddings into Memory Crystal is the right move... one product, one repo, one crystal."
