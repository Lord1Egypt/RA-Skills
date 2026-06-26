# Memory Crystal: Sovereign Memory + Four-Door Architecture

## Context

**The problem:** Agents have fragmented memory (sessions isolated, compaction = amnesia, no remote access). And tools are siloed — OpenClaw plugins invisible to Claude Code, MCP servers invisible to OpenClaw, CLIs lack structure.

**Two existing plans converge here:**
1. **memory-crystal** (`repos/memory-crystal/PRD.md`) — sovereign local-first memory with LanceDB + SQLite, semantic search, knowledge graph
2. **refactor-plan** (`repos/refactor-plan.md`) — every tool gets four interfaces: core + CLI + MCP + plugin + skill

**Parker's cloud insight:** Mac mini = source of truth. Cloud (Cloudflare Worker) = ephemeral disposable mirror. Wiped daily, rebuilt from mini. Breach = instant delete, nothing lost.

**Peter Steinberger's philosophy (OpenClaw creator):** "Bot is really good at Unix." CLI is the universal interface. But also: OpenClaw plugins for Lēsa, MCP for Claude Code, skills to teach agents. One codebase, four doors.

## Architecture: Four Doors, One Core

```
memory-crystal/
├── src/
│   ├── core.ts           ← Pure logic. Zero framework deps.
│   │                       search(), remember(), forget(), sync()
│   │                       Talks to local LanceDB/SQLite OR remote Worker API.
│   │
│   ├── cli.ts            ← crystal search "query"
│   │                       crystal search --remote "query"
│   │                       crystal remember "Parker prefers Opus"
│   │                       crystal push / crystal pull / crystal status
│   │
│   ├── mcp-server.ts     ← crystal_search, crystal_remember, crystal_forget
│   │                       For Claude Code via .mcp.json
│   │
│   ├── openclaw.ts       ← api.registerTool() wrappers
│   │                       For Lēsa via OpenClaw plugin system
│   │
│   └── worker.ts         ← Cloudflare Worker (REST API)
│                           POST /search, POST /remember, GET /health
│                           Backed by D1 + Vectorize + R2
│
├── skills/
│   └── memory/SKILL.md   ← Teaches agents when/how to use memory tools
│
├── openclaw.plugin.json  ← Plugin manifest
├── wrangler.toml         ← Cloudflare Worker config
└── package.json          ← bin: { "crystal": "./dist/cli.js" }
```

### How each consumer uses it

| Agent | Native Door | Also available |
|-------|------------|----------------|
| Lēsa (OpenClaw) | Plugin (openclaw.ts) + Skill | CLI via bash |
| Claude Code | MCP (mcp-server.ts) | CLI via Bash tool |
| Claude.ai (web) | Remote MCP (SSE transport) | — |
| ChatGPT / Grok / Gemini | CLI or direct HTTP to Worker | — |
| Any future agent | Whichever door it supports | — |

### Core design rules (from refactor-plan)
- Core has zero framework dependencies
- Core functions return plain TypeScript types, not MCP content arrays
- Config via function params, not framework globals
- Errors: core throws, wrappers catch and format
- `--remote` flag in core switches between local DB and Worker API

## Phase 1: Local Memory Crystal (Mac Mini) — COMPLETE ✅

Built 2026-02-09/10. All four doors live. Running alongside context-embeddings for verification.

### What's deployed
- **Vector DB:** LanceDB with cosine distance search
- **Metadata DB:** SQLite (knowledge graph, provenance, connector state)
- **Embedding:** OpenAI `text-embedding-3-small` (default), configurable to Ollama or Google
- **Chunking:** Paragraph/sentence-aware, 400 token target, 80 token overlap
- **Search:** Vector search with cosine similarity scoring (0-100%)
- **Data:** 5,502 chunks migrated from context-embeddings.sqlite (0 failures)

### What was built
1. ✅ **core.ts** — Crystal class: init, embed, chunkText, ingest, search, remember, forget, status, captureState
2. ✅ **Migration** — imported 5,502 chunks from context-embeddings.sqlite into LanceDB (re-embedded with OpenAI)
3. ✅ **cli.ts** — `crystal search`, `crystal remember`, `crystal forget`, `crystal status` with `--provider` flag
4. ✅ **openclaw.ts** — plugin wrapping core, `agent_end` hook for continuous ingestion
5. ✅ **mcp-server.ts** — MCP tools: crystal_search, crystal_remember, crystal_forget, crystal_status
6. ✅ **skills/memory/SKILL.md** — documents all tools and CLI commands

### Deployed to
- ✅ `~/.openclaw/.mcp.json` — memory-crystal MCP server registered
- ✅ `~/.openclaw/extensions/memory-crystal/` — OpenClaw plugin deployed, gateway loads successfully
- ✅ `~/.openclaw/openclaw.json` — plugin entry added
- ⏳ `repos/lesa-bridge/src/index.ts` — conversation_search/memory_search NOT yet removed (running in parallel)

### Embedding providers (configurable)
| Provider | Model | Dimensions | Cost | Set via |
|----------|-------|-----------|------|---------|
| OpenAI (default) | text-embedding-3-small | 1536 | paid | `CRYSTAL_EMBEDDING_PROVIDER=openai` |
| Ollama (local) | nomic-embed-text | 768 | free | `CRYSTAL_EMBEDDING_PROVIDER=ollama` |
| Google | text-embedding-004 | 768 | paid | `CRYSTAL_EMBEDDING_PROVIDER=google` |

### Still to do (Phase 1 cleanup)
- [ ] Verify agent_end hook captures new turns (check chunk count after Lēsa conversations)
- [ ] Install CLI globally (`npm link`)
- [ ] Disable context-embeddings once memory-crystal proven stable (~few days)
- [ ] Remove lesa-bridge conversation_search/memory_search tools

## Phase 2: Cloudflare Worker Mirror

Ephemeral cloud mirror. Wiped daily, rebuilt from mini.

### Architecture
```
Mac Mini (source of truth)          Cloudflare (ephemeral mirror)
┌──────────────────────┐            ┌─────────────────────────┐
│ memory-crystal       │   push     │ Worker (REST API)       │
│ ├── LanceDB (local)  │ ────────► │ ├── D1 (SQLite)         │
│ ├── SQLite (local)   │           │ ├── Vectorize (vectors)  │
│ └── sync-state.json  │ ◄──────── │ └── R2 (DB snapshot)    │
└──────────────────────┘   pull     └─────────────────────────┘
                                              ▲
                                    Any remote agent
                                    (CLI / MCP / HTTP)
```

### Daily cycle
1. **04:00** — Mini exports DB snapshot → R2 bucket
2. **04:05** — Worker rebuilds D1 + Vectorize from snapshot
3. **All day** — Remote agents read/write via Worker
4. **Every 4-6h** — Mini pulls new remote writes
5. **Next 04:00** — Wipe, re-upload. Repeat.

### Security model
- Worker auth: bearer token per agent
- Mini → Worker: HTTPS only
- Worker → Mini: NEVER (mini pulls, Worker never pushes)
- R2: private, Worker-binding only
- **Breach protocol:** `wrangler delete` — everything gone in seconds. Mini untouched.

### Why Cloudflare Workers (not VPS)
- Ephemeral by design — no persistent state to defend
- No server to maintain (no SSH, no OS, no patches)
- D1 = managed SQLite on edge
- Vectorize = managed vector search
- R2 = blob storage for snapshots
- Free tier covers it: 100K req/day, 5M rows D1, 5M vectors, 10GB R2

### Build order
1. **worker.ts** — REST endpoints: `/search`, `/remember`, `/health`, `/sync`
2. **wrangler.toml** — D1 binding, Vectorize binding, R2 bucket, secrets
3. **core.ts update** — add remote mode (HTTP calls to Worker when `--remote`)
4. **Sync script** — `crystal push` / `crystal pull` / `crystal reset`
5. **Cron on mini** — daily upload + periodic pull

### Parker does
- Cloudflare account (if needed)
- `wrangler login`
- Set Worker secrets (agent tokens)

## Phase 3: Multi-Agent Access

Any agent anywhere connects via its native door.

### Remote MCP server (for Claude.ai web, remote Claude Code)
- Thin MCP server wrapping Worker HTTP calls
- Embeds locally before pushing (Ollama or OpenAI)
- Config: Worker URL + agent token

### GPT Action (for ChatGPT)
- OpenAPI spec pointing at Worker REST endpoints
- Zero additional code — just a schema file

### CLI (universal)
- `crystal search --remote "query"` hits Worker
- Any agent with shell access can use it
- `npm install -g memory-crystal` for remote machines

## Verification

### Phase 1 (verified)
- [x] `crystal search "OpenAI API key"` returns relevant results with proper scoring
- [x] All four doors work: CLI, MCP, plugin, skill
- [x] `openclaw gateway restart` — no errors (plugin loads)
- [x] Original context-embeddings.sqlite preserved (41MB, untouched)
- [x] Search scores positive and sensible (cosine distance, 0-100%)
- [ ] Verify agent_end hook ingests new conversation turns
- [ ] Ollama provider tested (`crystal search --provider ollama`)

### Phase 2 (not started)
- [ ] `crystal search --remote` hits Worker and returns results
- [ ] Remote agent pushes chunk → mini pulls it within sync window
- [ ] `wrangler delete` nukes cloud — mini data intact
- [ ] Daily reset cycle works end-to-end

## Risk

- **LanceDB maturity** — newer than SQLite. Mitigation: context-embeddings running in parallel as fallback
- **Dual embedding cost** — both plugins embed every turn until context-embeddings disabled. Temporary.
- **Plugin API compatibility** — OpenClaw plugin format required: object export with `register()` method, `api.on()` for hooks, `api.registerTool()` with `execute` method, `configSchema` in manifest
