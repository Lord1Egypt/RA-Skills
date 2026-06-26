# Memory Crystal

Sovereign memory system for AI agents. Local-first with ephemeral cloud mirror.

One core, four doors: CLI, MCP server, OpenClaw plugin, Cloudflare Worker.

## What it does

- **Hybrid search** across all agent conversations, files, and stored memories ... BM25 keyword matching + vector similarity + RRF fusion
- **Recency-weighted scoring** ... fresh context wins ties, old stuff still surfaces for strong matches. Linear decay: `max(0.5, 1.0 - age_days * 0.01)`. Freshness flags: fresh (<3d), recent (<7d), aging (<14d), stale (14d+)
- **Content dedup** ... SHA-256 hash prevents duplicate embeddings
- **Remember/forget** explicit facts, preferences, observations
- **Continuous ingestion** ... new conversation turns are automatically embedded after every agent turn
- **Source file indexing** ... add directories as collections, sync to index changed files
- **Configurable embedding** ... OpenAI, Ollama (local/free), or Google

### Relationship to lesa-bridge

Memory Crystal and lesa-bridge are complementary, not overlapping. lesa-bridge searches the context-embeddings SQLite DB (conversation turns only, OpenAI embeddings). Memory Crystal searches its own sqlite-vec store (conversations, files, and explicit memories from both agents). Both apply the same recency decay formula independently. Different stores, same scoring philosophy.

## Search Architecture

Hybrid search (BM25 full-text + vector similarity + RRF fusion) is inspired by and
partially ported from [QMD](https://github.com/tobi/qmd) by Tobi Lutke
(MIT License, 2024-2026. License snapshot taken 2026-02-16).

- **sqlite-vec** for cosine vector search (single-file, inspectable, backupable)
- **FTS5** with Porter stemming for BM25 keyword search
- **Reciprocal Rank Fusion** to merge both ranked result lists
- **Recency weighting** on top: `max(0.5, 1.0 - age_days * 0.01)`
- **Content dedup** via SHA-256 hash of chunk text before embedding
- **LanceDB** retained as dual-write safety net during transition

### How hybrid search works

1. Query goes to both FTS5 (keyword match) and sqlite-vec (vector similarity)
2. FTS5 returns BM25-ranked results, normalized to [0..1) via `|score| / (1 + |score|)`
3. sqlite-vec returns cosine-distance results via two-step query (MATCH first, then JOIN separately... sqlite-vec hangs with JOINs in the same query)
4. RRF fusion merges both lists: `weight / (k + rank + 1)` with k=60, plus top-rank bonus
5. Recency weighting applied on top of fused scores
6. Final results sorted by combined score

## Architecture

```
sqlite-vec (vectors) + FTS5 (BM25) + SQLite (metadata/graph)
         |                 |                    |
    core.ts ... pure logic, zero framework deps
    |-- cli.ts          -> crystal search "query"
    |-- mcp-server.ts   -> crystal_search (Claude Code)
    |-- openclaw.ts     -> plugin (Lesa / OpenClaw)
    |-- cc-hook.ts      -> Claude Code Stop hook (auto-capture)
    +-- worker.ts       -> Cloudflare Worker (Phase 2)
```

LanceDB is maintained as a dual-write target during transition. Once sqlite-vec is proven stable, LanceDB will be removed.

**Mac mini = source of truth.** Cloud = ephemeral mirror, wiped daily, rebuilt from mini.

## Quick start

```bash
# Install
npm install

# Build
npm run build

# Search
node dist/cli.js search "what did Parker say about robots"

# Remember something
node dist/cli.js remember "Parker prefers Opus for complex tasks"

# Status
node dist/cli.js status
```

## CLI

```
crystal search <query> [-n limit] [--agent <id>] [--provider <openai|ollama|google>]
crystal remember <text> [--category fact|preference|event|opinion|skill]
crystal forget <id>
crystal status [--provider <openai|ollama|google>]
crystal sources add <path> --name <name>
crystal sources sync [name]
crystal sources status
```

## MCP server (Claude Code)

Registered in `~/.openclaw/.mcp.json`. Tools:

| Tool | Description |
|------|-------------|
| `crystal_search` | Hybrid search across all memories |
| `crystal_remember` | Store a fact or observation |
| `crystal_forget` | Deprecate a memory by ID |
| `crystal_status` | Chunk count, provider, agents |

## OpenClaw plugin (Lesa)

Deployed to `~/.openclaw/extensions/memory-crystal/`. Registers tools + `agent_end` hook for continuous conversation ingestion.

## Auto dev updates

Memory Crystal automatically writes dev updates to `wip-dev-updates/` when repos have changed. Triggered by:

- **Lēsa:** `before_compaction` hook (fires at 90% context ... captures work before memory is wiped)
- **Claude Code:** Stop hook (fires after every session, throttled to once per hour)

Scans all repos under `staff/` for recent git commits and uncommitted changes. Writes dated updates per repo: `{who}-dev-update-{MM-DD-YYYY}--{HH-MM-SS}.md`. Auto-commits and pushes to `wipcomputer/wip-dev-updates`.

Source: `src/dev-update.ts`

## Claude Code Stop hook

`cc-hook.ts` auto-captures every Claude Code turn into Memory Crystal. Runs as a [Stop hook](https://docs.anthropic.com/en/docs/claude-code) ... fires after every Claude Code response, independent of the OpenClaw gateway.

**How it works:**
- Reads Claude Code's JSONL transcript via byte-offset watermarking (no re-reading old data)
- Extracts user/assistant/thinking blocks, chunks them, embeds into sqlite-vec (+ LanceDB dual-write)
- Tags chunks with `agent_id: "claude-code"` for filtering
- Respects private mode (checks `memory-capture-state.json`)
- First run seeds watermark at current file size (skips old history)
- After ingestion, runs auto-dev-update for changed repos (throttled to once/hour)

**Configuration:** `~/.claude/settings.json`
```json
{
  "hooks": {
    "Stop": [{ "hooks": [{ "type": "command", "command": "node ~/.openclaw/extensions/memory-crystal/dist/cc-hook.js", "timeout": 30 }] }]
  }
}
```

**CLI:**
```bash
node dist/cc-hook.js --on      # Enable capture
node dist/cc-hook.js --off     # Pause capture (resumes from where it left off)
node dist/cc-hook.js --status  # Check status
```

## Embedding providers

| Provider | Model | Dimensions | Cost |
|----------|-------|-----------|------|
| OpenAI (default) | text-embedding-3-small | 1536 | ~$0.02/1M tokens |
| Ollama | nomic-embed-text | 768 | free (local) |
| Google | text-embedding-004 | 768 | free tier available |

Set via `CRYSTAL_EMBEDDING_PROVIDER` env var or `--provider` flag.

## Setup: API keys

Two options ... pick one:

### Option A: `.env` file

```bash
cp .env.example ~/.openclaw/memory-crystal/.env
# Edit and add your API key
```

### Option B: 1Password

No config needed. Keys auto-resolve from the `Agent Secrets` vault via the `op-secrets` OpenClaw plugin (inside OpenClaw) or the `op` CLI (standalone).

| 1Password Item | Field | Used for |
|----------------|-------|----------|
| `OpenAI API` | `api key` | OpenAI embeddings |
| `Google AI` | `api key` | Google embeddings |
| `Memory Crystal Remote` | `token` | Cloudflare Worker auth (Phase 2) |

Requires SA token at `~/.openclaw/secrets/op-sa-token`.

### Resolution order

1. Explicit override (programmatic)
2. `process.env` (set by op-secrets plugin or by you)
3. `.env` file (`~/.openclaw/memory-crystal/.env`)
4. 1Password CLI fallback

### All environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CRYSTAL_EMBEDDING_PROVIDER` | `openai` | `openai`, `ollama`, or `google` |
| `OPENAI_API_KEY` | ... | OpenAI key |
| `GOOGLE_API_KEY` | ... | Google AI key |
| `CRYSTAL_OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `CRYSTAL_OLLAMA_MODEL` | `nomic-embed-text` | Ollama model |
| `CRYSTAL_REMOTE_URL` | ... | Cloudflare Worker URL (Phase 2) |
| `CRYSTAL_REMOTE_TOKEN` | ... | Worker auth token (Phase 2) |

## Data

All data lives in `~/.openclaw/memory-crystal/`:

```
memory-crystal/
├── lance/          <- LanceDB vector store (dual-write safety net)
└── crystal.db      <- SQLite: chunks + vectors (sqlite-vec) + FTS5 + metadata
```

`crystal.db` is a single file containing everything: chunk text, embeddings (via sqlite-vec), full-text index (FTS5), memories, entities, relationships, and capture state. Inspectable with any SQLite tool. Backupable with `cp`.

### Schema overview

| Table | Purpose |
|-------|---------|
| `chunks` | Chunk text, metadata, SHA-256 hash, timestamps |
| `chunks_vec` | sqlite-vec virtual table (cosine distance vectors) |
| `chunks_fts` | FTS5 virtual table (Porter stemming, BM25 scoring) |
| `memories` | Explicit remember/forget facts |
| `entities` | Knowledge graph nodes |
| `relationships` | Knowledge graph edges |
| `capture_state` | Watermarks for incremental ingestion |
| `sources` | Ingestion source metadata |
| `source_collections` | Directory collections for file indexing |
| `source_files` | Indexed file records with content hashes |

## Source file indexing

Add directories as "collections", sync to index/re-index changed files. All source chunks get `source_type='file'` so they're searchable alongside conversations and memories.

```bash
# Add a directory tree to index
crystal sources add /path/to/project --name wipcomputer

# Sync (re-index changed files)
crystal sources sync wipcomputer

# Status
crystal sources status
# => wipcomputer: 15,492 files, 145,738 chunks, last sync 2m ago
```

Files are chunked, embedded, and tagged with file path + collection name. Incremental sync detects changed files via SHA-256 content hashing.

## Migration

### LanceDB to sqlite-vec

If you have existing data in LanceDB, migrate it to sqlite-vec:

```bash
# Dry run (check counts)
node scripts/migrate-lance-to-sqlite.mjs --dry-run

# Full migration (reads vectors directly from LanceDB, no re-embedding)
node scripts/migrate-lance-to-sqlite.mjs
```

The migration reads vectors directly from LanceDB and inserts them into sqlite-vec. No API calls needed. Deduplicates by SHA-256 hash. ~5,000 chunks/sec on M4 Pro.

### context-embeddings.sqlite

Import from the older context-embeddings format (requires re-embedding):

```bash
node dist/migrate.js [--dry-run] [--provider openai]
```

## Roadmap

- **Phase 1** ... Complete. Local memory with all four doors.
- **Phase 2a** ... Complete. Source file indexing + QMD hybrid search integration (sqlite-vec + FTS5 + RRF).
- **Phase 2b** ... Complete. Historical session backfill (152K+ chunks).
- **Phase 3** ... Planned. Cloudflare Worker mirror (D1 + Vectorize + R2).
- **Phase 4** ... Planned. Remote MCP, GPT Action, multi-agent access.
- **Cleanup** ... Planned. Remove LanceDB once sqlite-vec is proven stable.

See [PLAN.md](PLAN.md) for full architecture and roadmap.
