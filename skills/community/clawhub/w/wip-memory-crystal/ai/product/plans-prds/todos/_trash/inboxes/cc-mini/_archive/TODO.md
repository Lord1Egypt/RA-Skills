# Memory Crystal — TODO

## Phase 1 — Done
All four doors live, Lēsa confirmed, 5,543+ chunks and growing.

### Phase 1 cleanup (small)
- [ ] `npm link` to install `crystal` CLI globally
- [ ] Disable `context-embeddings` plugin (saves double embedding cost per turn) — or keep both for a few more days
- [ ] Remove `conversation_search`/`memory_search` from lesa-bridge (crystal replaces them)

## Phase 2 — Cloudflare Worker mirror (big)
- [ ] `worker.ts` — REST API backed by D1 + Vectorize + R2
- [ ] `crystal push` / `crystal pull` / `crystal reset` sync commands
- [ ] Daily cron: mini uploads, Worker rebuilds, mini pulls new writes
- [ ] **Needs:** Parker's Cloudflare account + `wrangler login`

## Phase 3 — Remote multi-agent access
- [ ] Remote MCP for Claude.ai web
- [ ] OpenAPI spec for ChatGPT/Grok
- [ ] `crystal search --remote` from anywhere

## Other stuff on the board
- [ ] GitHub setup (Lēsa's account)
- [ ] Repo renames
- [ ] cc-persistence (Pi RPC sidecar)
