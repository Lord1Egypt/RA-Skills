# 2026-02-25 — Phase 2 Worker Build

**Agent:** cc-a (Claude Code on MacBook Air)
**Repo:** `memory-crystal`
**Branch:** `cc-mba/phase2-worker`

## What Was Done

### 1. Read & Understood the Entire Codebase
- `core.ts` (1,346 lines) — hybrid search: sqlite-vec + FTS5 + RRF fusion + recency weighting
- `mcp-server.ts` — 7 MCP tools for Claude Code (search, remember, forget, status, sources)
- `cc-hook.ts` — Stop hook with byte-offset watermarking, batched ingestion
- `openclaw.ts` — Lesa's agent_end hook with compaction detection
- `resolveConfig()` — 4-level config resolution (params → env → .env → 1Password)

### 2. Built the Cloudflare Worker (`src/worker.ts`)
- REST API endpoints: `/search`, `/ingest`, `/remember`, `/forget`, `/status`, `/health`
- Sync endpoints: `/sync/push` (Mini uploads snapshot to R2), `/sync/pull` (Mini pulls new remote writes)
- Auth: bearer token per agent (cc-a, cc, lesa) mapped to agent_id
- Search: FTS5 on D1 + Vectorize cosine similarity + RRF fusion + recency weighting
- Deduplication: SHA-256 hash check before ingest
- Embedding: OpenAI text-embedding-3-small via fetch

### 3. Created D1 Schema (`schema.sql`)
- `chunks` table with hash-based dedup, agent_id, source tracking
- `chunks_fts` virtual table (FTS5 with Porter stemming)
- Triggers to keep FTS in sync with chunks
- `memories` table for explicit remember/forget
- `capture_state` and `sync_log` for sync tracking

### 4. Created Wrangler Config (`wrangler.toml`)
- D1 binding (needs database_id after creation)
- Vectorize binding (memory-crystal-chunks, 1536 dimensions)
- R2 bucket binding (memory-crystal-snapshots)
- Secrets: AUTH_TOKEN_CC_A, AUTH_TOKEN_CC, AUTH_TOKEN_LESA, OPENAI_API_KEY

### 5. Added Remote Mode to Core (`core.ts`)
- New `RemoteCrystal` class — same interface as `Crystal`, talks to Worker via HTTP
- `createCrystal()` factory — returns `RemoteCrystal` when `remoteUrl` + `remoteToken` are set, otherwise local `Crystal`
- `chunkText()` method on RemoteCrystal for cc-hook compatibility

### 6. Updated MCP Server (`mcp-server.ts`)
- Uses `createCrystal()` — auto-detects remote mode
- Shows "(REMOTE)" in status when using cloud mirror
- Source indexing tools gracefully return "not available in remote mode"

### 7. Updated CC Hook (`cc-hook.ts`)
- Uses `createCrystal()` for remote ingestion support
- Configurable `CRYSTAL_AGENT_ID` env var (defaults to 'claude-code', set to 'cc-a' on MacBook Air)
- Type-safe with `Crystal | RemoteCrystal` union

### 8. Build Verification
- `npm run build:local` — succeeds, all types pass
- `npm run build:worker` — succeeds, worker.js = 12 KB

## Current Status

**Code: COMPLETE.** All source files written and building clean.

**Not yet deployed.** Needs Cloudflare resources created and secrets set.

## Files Changed/Created

| File | Action |
|------|--------|
| `src/worker.ts` | NEW — Cloudflare Worker |
| `schema.sql` | NEW — D1 database schema |
| `wrangler.toml` | NEW — Cloudflare config |
| `src/core.ts` | MODIFIED — added RemoteCrystal + createCrystal() |
| `src/mcp-server.ts` | MODIFIED — remote mode support |
| `src/cc-hook.ts` | MODIFIED — remote mode + configurable agent_id |
| `package.json` | MODIFIED — added build:worker and build:local scripts |
