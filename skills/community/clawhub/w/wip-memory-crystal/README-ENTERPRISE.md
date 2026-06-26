###### WIP Computer

# Memory Crystal for Enterprise

Agent memory infrastructure. Local-first. Encrypted. Inspectable. *In testing.*

## The Problem

Your organization runs AI agents across teams, departments, and tools. Each agent starts every session with no memory. No continuity. No shared context. Conversations with one agent are invisible to every other.

Your agents can't remember what your people told them. Your people keep re-explaining themselves. Context is lost between sessions, between tools, between teams.

This is not a convenience problem. It's a reliability problem. An auditability problem. A cost problem.

## What Memory Crystal Does

Memory Crystal is a persistent context layer for AI agents. One shared database. Hybrid search. On your machines. Under your control.

- **Local-first.** All data stays on-prem. Nothing leaves your network unless you configure it to.
- **Inspectable.** One SQLite file. Open it with any SQLite tool. Audit it. Query it. Back it up with `cp`.
- **Deterministic search.** Hybrid retrieval (BM25 keyword + vector similarity + Reciprocal Rank Fusion). Same query, same results. No black-box ranking.
- **Encrypted sync.** Multi-site deployments use AES-256-GCM encryption with HMAC-SHA256 signing. The relay sees encrypted noise. Keys never leave your machines.
- **Agent isolation.** Each agent gets its own ID, its own transcript archive, its own session summaries. Shared search across agents, isolated storage per agent.
- **Zero cloud dependency.** Runs fully offline with local embeddings (Ollama). No API keys required. No data exfiltration risk.

## Five-Layer Memory Stack

Memory Crystal implements a full memory pipeline, not just search.

| Layer | What | How |
|-------|------|-----|
| L1: Raw Transcripts | Every conversation archived as JSONL | Automatic. cc-poller (cron), cc-hook (Stop), openclaw.ts (agent_end) |
| L2: Vector Index | Chunks embedded into crystal.db | Automatic. Hybrid search (BM25 + vector + RRF) |
| L3: Structured Memory | Facts, preferences, decisions | `crystal_remember` / `crystal_forget` |
| L4: Narrative Consolidation | Dream Weaver journals, identity, soul | `crystal dream-weave` (imports engine from Dream Weaver Protocol) |
| L5: Active Working Context | Boot sequence files, shared context | Agent reads on startup |

L1-L3 are fully automated. L4 runs on-demand or via Crystal Core gateway. L5 is consumed by the agent's boot sequence.

## Architecture

```
sqlite-vec (vectors) + FTS5 (BM25) + SQLite (metadata)
         |                 |                    |
    core.ts ... pure logic, zero framework deps
    |-- cli.ts            -> crystal search, dream-weave, backfill, serve
    |-- mcp-server.ts     -> MCP protocol (any compatible client)
    |-- openclaw.ts       -> OpenClaw plugin + raw data sync to LDM
    |-- cc-poller.ts      -> Continuous capture (cron, primary)
    |-- cc-hook.ts        -> Claude Code Stop hook (redundancy) + relay commands
    |-- crystal-serve.ts  -> Crystal Core gateway (localhost:18790)
    |-- dream-weaver.ts   -> Dream Weaver integration (narrative consolidation)
    |-- staging.ts        -> New agent staging pipeline
    |-- llm.ts            -> LLM provider cascade (MLX > Ollama > OpenAI > Anthropic)
    |-- search-pipeline.ts -> Deep search (expand, search, RRF, rerank, blend)
    +-- worker.ts         -> Encrypted relay (multi-site sync, 3 channels)
```

One core module. Multiple interfaces. Every interface calls the same search engine. No inconsistency between access paths.

## Security Model

**Data at rest:** Single SQLite file. Standard filesystem permissions. Encrypt the volume if your compliance requires it.

**Data in transit:** AES-256-GCM authenticated encryption. HMAC-SHA256 integrity verification. Shared symmetric key generated on-prem, never transmitted to the relay. The relay is a dead drop with no decryption capability.

**Agent boundaries:** `CRYSTAL_AGENT_ID` isolates each agent's transcript archive, session summaries, and daily logs. Search spans all agents by default, or filters by agent ID.

**Private mode:** Memory capture can be paused per-agent. When off, nothing is recorded. Resumes from where it left off when re-enabled.

**No background processes that move data.** No telemetry. No analytics. No phone-home. The code is open source. Audit it.

## Retrieval Quality

Hybrid search is not "we added vectors." It's a two-tier retrieval engine with LLM-powered deep search.

### Fast Path (Hybrid Search)
- **FTS5 BM25** for exact keyword matches (Porter stemming)
- **sqlite-vec cosine similarity** for semantic matches
- **Reciprocal Rank Fusion** merges both result lists (k=60, tiered weights: BM25 2x, vector 1x)
- **Recency weighting** ensures fresh context wins decisively: exponential decay `max(0.3, exp(-age_days * 0.1))`
- **Content deduplication** via SHA-256 hash prevents duplicate embeddings
- **Time-filtered search** ... restrict results to last 24h, 7d, 30d, or any date range

### Deep Search (LLM-Powered, default)
- **Query expansion** ... LLM generates 3 search variations (lexical, semantic, hypothetical document). Each runs through hybrid search. Results merged via RRF.
- **Strong signal detection** ... BM25 probe skips expansion when the answer is obvious (saves latency).
- **LLM re-ranking** ... top 40 candidates scored by LLM for relevance to the original query.
- **Position-aware blending** ... trusts RRF for top positions, lets the reranker fix ordering in the tail.

Deep search runs by default. Falls back to fast path silently if no LLM provider is available. For air-gapped environments, MLX (Apple Silicon) or Ollama provides free, fully local deep search with no API keys and no network.

A search for "deployment policy" finds conversations containing those exact words (BM25), conversations about "shipping code to production" (vector similarity), and conversations about "release workflow" that the LLM recognizes as relevant. All three matter. All three surface.

## What Gets Stored

Every agent conversation produces three artifacts:

| Artifact | Format | Location |
|----------|--------|----------|
| Raw transcript | JSONL | `~/.ldm/agents/{id}/memory/transcripts/` |
| Session summary | Markdown | `~/.ldm/agents/{id}/memory/sessions/` |
| Embeddings | sqlite-vec | `~/.ldm/memory/crystal.db` |

Additionally:
- **Explicit memories** stored via `crystal_remember` (facts, preferences, decisions)
- **Source files** indexed as collections (code, documentation, internal knowledge bases)
- **Daily logs** appended per-agent for audit trails
- **Dream Weaver journals** generated by narrative consolidation (identity, soul, context, reference)
- **Workspace files** synced from agent workspace to LDM (OpenClaw .md files)

## Embedding Providers

| Provider | Model | Dimensions | Network Required |
|----------|-------|-----------|-----------------|
| Ollama (recommended for enterprise) | nomic-embed-text | 768 | No. Fully local. |
| OpenAI | text-embedding-3-small | 1536 | Yes. API calls. |
| Google | text-embedding-004 | 768 | Yes. API calls. |

For air-gapped environments, Ollama is the only option. No data leaves the machine. No API keys. No external dependencies.

## Multi-Site Sync

For organizations with multiple offices or remote teams.

**Architecture:** One Crystal Core (the primary embedder), many Crystal Nodes (capture and sync). Core is the only machine that writes embeddings. Nodes capture raw conversations and send them to Core. Core embeds, then pushes deltas back.

**What syncs:**
1. **Delta chunks** ... only new embeddings since last sync (not the full database)
2. **Full file tree** ... the entire `~/.ldm/` directory: workspace files, daily logs, journals, media, everything an embedding references
3. **Commands** ... bidirectional remote operations (run Dream Weaver, trigger backfill, request status)

**How it works:**
1. Each site runs Memory Crystal locally
2. Core embeds all conversations into crystal.db (one source of truth for embeddings)
3. New chunks + changed files are encrypted (AES-256-GCM) and signed (HMAC-SHA256)
4. Encrypted deltas are dropped at a relay (hosted or self-hosted)
5. Other sites poll, decrypt, and insert into their local crystal.db + file tree
6. The relay deletes blobs after pickup

**No cloud search.** Every node has the full database and full file tree. All search is local. The relay is pure transport. Nothing is stored or searchable in the cloud.

**Self-hosted relay:** Deploy the Cloudflare Worker on your own Cloudflare account. Full control. No third-party data exposure.

**Hosted relay:** Use our infrastructure. Free during beta. Your data is encrypted before it reaches us. We cannot read it.

## Compliance

- **Data residency:** All primary data is local. Relay blobs are encrypted and ephemeral.
- **Auditability:** SQLite is inspectable. Every chunk has a timestamp, source, and SHA-256 hash.
- **Right to delete:** `crystal forget <id>` deprecates specific memories. Database can be wiped entirely with standard file operations.
- **Access control:** Filesystem permissions on the SQLite file. No built-in user auth (it's a local tool, not a SaaS).
- **No vendor lock-in:** MIT licensed (local code). Standard SQLite format. Export with any SQLite tool.

## Database

One file: `crystal.db`. Contains:

| Table | Purpose |
|-------|---------|
| `chunks` | Chunk text, metadata, SHA-256 hash, timestamps |
| `chunks_vec` | sqlite-vec virtual table (vector search) |
| `chunks_fts` | FTS5 virtual table (keyword search) |
| `memories` | Explicit facts and preferences |
| `capture_state` | Watermarks for incremental ingestion |
| `source_collections` | Indexed directory collections |
| `source_files` | File records with content hashes |

No migrations server. No schema versioning service. It's SQLite. `sqlite3 crystal.db ".schema"` shows you everything.

## Integration

| Platform | Integration | Auto-Capture |
|----------|------------|-------------|
| Claude Code | Cron poller (`cc-poller.ts`, primary) + Stop hook (`cc-hook.ts`, redundancy) | Yes. Every minute via cron, plus flush on session end. |
| OpenClaw | Plugin (`openclaw.ts`) + `agent_end` hook + raw data sync | Yes. Every turn. Also syncs sessions, workspace, daily logs to LDM. |
| Claude Desktop | MCP server (`mcp-server.ts`) | Search only. Manual capture. |
| Any MCP client | MCP server | Search only. Manual capture. |
| Any shell-accessible tool | CLI (`crystal search`) | Manual. |
| Custom agents | Node.js module (`import from 'memory-crystal'`) | Programmable. |

## Crystal Core Gateway

Crystal Core runs an HTTP gateway (`crystal serve`) on localhost:18790. OpenAI-compatible endpoint for agent-to-agent communication and automated processing.

- `POST /v1/chat/completions` ... invoke `claude -p` through the gateway
- `POST /process` ... trigger backfill, dream-weave, or staging processing
- `GET /status` ... health check and crystal stats

Localhost-only binding. Never exposed to the network. Optional bearer token auth.

## New Agent Onboarding

When a new agent connects via relay, Crystal Core automatically:
1. Detects the unknown agent ID
2. Routes to staging (`~/.ldm/staging/{agent_id}/`)
3. Runs backfill (embed all transcripts)
4. Runs Dream Weaver full mode (generate identity, soul, context, journals)
5. Moves to live capture

No manual intervention. The staging pipeline handles the cold-start problem.

## Deployment

```bash
npm install memory-crystal
crystal init --agent your-agent-id
crystal status
```

For enterprise deployments across multiple machines, see [Relay: Memory Sync](https://github.com/wipcomputer/memory-crystal/blob/main/RELAY.md).

For full technical details, see [Technical Documentation](https://github.com/wipcomputer/memory-crystal/blob/main/TECHNICAL.md).

---

## License

```
src/, skills/, cli.ts, mcp-server.ts   MIT    (use anywhere, no restrictions)
worker/                                AGPL   (relay server)
```

AGPL for personal use is free.

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code CLI (Claude Opus 4.6).
