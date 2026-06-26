# ~~Memory Crystal Phase 2 — Cloudflare Worker + Multi-Agent Setup~~

> **SUPERSEDED** — This plan was replaced by the ephemeral relay architecture on 2026-02-25.
> See `phase2-ephemeral-relay.md` for the current design.
> The cloud-mirror approach (D1 + Vectorize + search on Worker) was abandoned in favor of
> a blind dead drop with client-side encryption. The Worker has no database, no search,
> no ability to read the data it holds.

**Date:** 2026-02-25
**Agent:** cc-mba (Claude Code on MacBook Air)
**Repo:** `memory-crystal` → branch `cc-mba/phase2-worker` (superseded by `cc-air/phase2-relay`)

## The Problem

Three agents need shared memory:
- **cc-a** — Claude Code on MacBook Air (this machine)
- **cc** — Claude Code on Mac Mini
- **Lesa** — OpenClaw agent on Mac Mini

Today, memory-crystal runs locally on the Mac Mini. cc and Lesa share `crystal.db` directly. cc-a (me) has no access to that database. The bridge (`lesa-bridge`) only works localhost — it can't reach across machines.

## The Solution

Build the Cloudflare Worker mirror that's already specced in `PLAN.md`. This gives all three agents a shared memory layer via HTTPS, with the Mac Mini remaining source of truth.

```
cc-a (MacBook Air)  ──HTTPS──→  Cloudflare Worker  ←──HTTPS──  cc (Mac Mini)
                                      ↕
                                 Lesa (Mac Mini)
                                      ↕
                              Mac Mini pulls daily
                              (source of truth)
```

## Architecture

### Cloudflare Stack
- **Worker** — REST API (`/search`, `/remember`, `/ingest`, `/health`, `/status`)
- **D1** — SQLite database (chunks, memories, metadata)
- **Vectorize** — Vector index for semantic search
- **R2** — Snapshot storage for daily sync from Mini

### Sync Model
1. **04:00 daily** — Mini exports `crystal.db` snapshot → R2
2. **04:05** — Worker rebuilds D1 + Vectorize from snapshot
3. **All day** — All agents read/write via Worker
4. **Every 4-6h** — Mini pulls new remote writes
5. **Breach protocol** — `wrangler delete` nukes everything. Mini untouched.

### Auth
- Bearer token per agent (stored in 1Password)
- Tokens: `cc-a`, `cc`, `lesa` — each identified in requests
- Worker validates token + extracts agent_id

### Security
- Worker → Mini: NEVER (Mini pulls, Worker never pushes)
- Mini → Worker: HTTPS only
- R2: private, Worker-binding only
- All tokens in 1Password `Agent Secrets` vault

## What We're Building

### Phase 2a: Worker + Remote Access (cc-a can search and write)

1. **`src/worker.ts`** — Cloudflare Worker with endpoints:
   - `POST /search` — hybrid search (D1 FTS5 + Vectorize cosine)
   - `POST /remember` — store explicit memories
   - `POST /ingest` — ingest conversation chunks (used by cc-hook)
   - `GET /health` — alive check
   - `GET /status` — chunk count, agent list, last sync

2. **`wrangler.toml`** — D1 binding, Vectorize index, R2 bucket, secrets

3. **`src/core.ts` update** — add `--remote` mode:
   - When `CRYSTAL_REMOTE_URL` is set, HTTP calls to Worker instead of local SQLite
   - Same interface, different backend

4. **`src/cc-hook.ts` update** — support remote ingestion:
   - After chunking, POST to Worker `/ingest` endpoint
   - Falls back to local if Worker unreachable

5. **`crystal push` / `crystal pull`** — sync commands for Mini

### Phase 2b: MacBook Air Setup (cc-a is live)

1. **1Password** — ensure `Agent Secrets` vault has:
   - `OpenAI API` → embedding key
   - `Memory Crystal Remote` → Worker URL + auth token for cc-a

2. **memory-crystal on MacBook Air** — install locally:
   - `npm install && npm run build`
   - Configure `.env` with remote URL + token
   - Register MCP server in Claude Code's `.mcp.json`
   - Register Stop hook in `~/.claude/settings.json`

3. **Test cycle:**
   - cc-a writes a memory → Worker stores it
   - cc-a searches → gets results from all agents
   - Mini pulls → cc-a's memories now in source of truth

## 1Password Setup (for this machine)

### What's Needed
- Service account token at `~/.openclaw/secrets/op-sa-token`
- `Agent Secrets` vault with API keys
- The `op://` resolution pattern for config files

### For memory-crystal specifically:
```
op://Agent Secrets/OpenAI API/api key          → embedding API key
op://Agent Secrets/Memory Crystal Remote/token  → Worker bearer token
op://Agent Secrets/Memory Crystal Remote/url    → Worker URL
```

### Resolution in memory-crystal:
- memory-crystal's `resolveConfig()` already checks: programmatic → env → .env file → 1Password
- We add Worker URL + token to the same resolution chain

## Environment Variables (cc-a MacBook Air)

```bash
# .env at ~/.openclaw/memory-crystal/.env
CRYSTAL_EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=op://Agent Secrets/OpenAI API/api key
CRYSTAL_REMOTE_URL=https://memory-crystal.wipcomputer.workers.dev
CRYSTAL_REMOTE_TOKEN=op://Agent Secrets/Memory Crystal Remote/token
```

Or resolve via 1Password service account (preferred — no plaintext on disk).

## MCP Registration (cc-a MacBook Air)

```json
// ~/.claude/settings.json (or wherever Claude Code reads MCP config)
{
  "mcpServers": {
    "memory-crystal": {
      "command": "node",
      "args": ["/Users/parker/Documents/dev-wip/repos/memory-crystal/dist/mcp-server.js"],
      "env": {
        "CRYSTAL_REMOTE_URL": "https://memory-crystal.wipcomputer.workers.dev",
        "CRYSTAL_REMOTE_TOKEN": "the-token"
      }
    }
  }
}
```

## Stop Hook Registration (cc-a MacBook Air)

```json
// ~/.claude/settings.json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "node /Users/parker/Documents/dev-wip/repos/memory-crystal/dist/cc-hook.js",
        "timeout": 30
      }]
    }]
  }
}
```

## Build Order

1. **Worker** — `worker.ts` + `wrangler.toml` + D1 schema + Vectorize index
2. **Core update** — remote mode in `core.ts` (HTTP calls when `CRYSTAL_REMOTE_URL` set)
3. **cc-hook update** — POST chunks to Worker instead of local DB
4. **MCP update** — tools use remote mode transparently
5. **Sync commands** — `crystal push` / `crystal pull` for Mini
6. **Deploy** — `wrangler deploy`, set secrets, test end-to-end
7. **MacBook Air setup** — install, configure, register MCP + hook
8. **Verify** — cc-a writes → Worker stores → Mini pulls → all agents see it

## What Parker Needs To Do

- [ ] Cloudflare account (may already have one)
- [ ] `wrangler login`
- [ ] 1Password: ensure `Agent Secrets` vault exists and has OpenAI key
- [ ] 1Password: create service account token for MacBook Air (if not already done)
- [ ] Save token to `~/.openclaw/secrets/op-sa-token` on MacBook Air
- [ ] Approve the Worker deploy when ready

## Success Criteria

- cc-a (me on MacBook Air) can `crystal_search` and get results from all three agents
- cc-a can `crystal_remember` and the memory shows up for cc and Lesa
- Every cc-a conversation auto-ingests via the Stop hook
- Mini remains source of truth — `crystal push/pull` works
- `wrangler delete` kills cloud, Mini unaffected
