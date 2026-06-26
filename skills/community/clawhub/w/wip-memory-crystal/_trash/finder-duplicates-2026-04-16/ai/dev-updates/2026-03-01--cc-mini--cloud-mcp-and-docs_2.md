# Dev Update: Cloud MCP, Docs Overhaul, Todo Convention

**Date:** 2026-03-01
**Agent:** cc-mini
**Branch:** `cc-mini/cloud-mcp`

## What Got Built

### Cloud MCP Server (ChatGPT + Claude on all surfaces)
- `src/worker-mcp.ts` ... OAuth 2.1 with DCR + PKCE S256, Streamable HTTP MCP, 4 tools (memory_search, memory_remember, memory_forget, memory_status). One Worker, six surfaces (macOS/iOS/web for both ChatGPT and Claude).
- `src/cloud-crystal.ts` ... D1 + Vectorize backend. Same hybrid search algorithm as local Crystal (BM25 + vector + RRF fusion + recency weighting). CloudCrystal class with search(), ingest(), remember(), forget(), status().
- `migrations/0001_init.sql` ... OAuth tables (clients, authorization codes, access tokens, users).
- `migrations/0002_cloud_storage.sql` ... Cloud storage (chunks, memories, FTS5 triggers, indexes).
- `wrangler-mcp.toml` ... Separate Worker config for cloud MCP.
- `scripts/deploy-cloud.sh` ... 1Password-driven deployment. All credentials pulled from 1Password. Creates D1 database, Vectorize index, runs migrations, sets Worker secrets, builds and deploys.
- `package.json` ... Added `build:cloud` and `deploy:cloud` scripts, `@cloudflare/workers-types` devDependency.

### Two Tiers
- **Tier 1 (Sovereign):** Encrypted relay only. No cloud search. Cloud MCP tells client "search available on local devices only."
- **Tier 2 (Convenience):** D1 + Vectorize cloud search. Same RRF hybrid search. Home machine is still source of truth.

### Documentation Overhaul
- **README.md** ... Added Cloud Memory section (6 surfaces, 2 tiers), QR pairing mention, fixed license paths.
- **RELAY.md** ... Full rewrite. Two sync paths (encrypted relay + cloud MCP). QR pairing setup. Self-host steps fixed (R2 not KV). Key management table. Architecture file map.
- **TECHNICAL.md** ... Cloud MCP architecture documented. Relay section corrected (R2 not KV). Project structure updated with all new files. Roadmap reflects phases 3-4 complete. D1 + Vectorize design decision added. License section added.

### Todo Convention
- New system: one file per person/agent. Three sections: To Do, Done, Deprecated. Never delete anything.
- `ai/todos/Parker-todo.md` ... only items that block CC-Mini (Cloudflare login, credential entry, device testing, app submissions).
- `ai/todos/CC-Mini-todo.md` ... all code, deploys, verification, builds.
- `ai/todos/OC-Lesa-Mini-todo.md` ... Lesa's tasks.
- Convention also published to wip-dev-tools Dev Guide v1.0.4.

### 1Password Integration
- Created "Parker - Cloudflare Memory Crystal Keys" item in Agent Secrets vault (api-token, account-id fields).
- Deploy script pulls all credentials from 1Password. No keys in env files or code.

## What's Blocked on Parker

1. **Cloudflare credentials** ... log into Cloudflare, get API token + account ID, put in 1Password item.
2. **`wrangler login`** ... browser auth on the Mini. CC-Mini runs everything after.
3. **Review docs** ... README, RELAY, TECHNICAL are open in MDV.

## What's Next (CC-Mini)

1. Build `crystal pair` (QR code pairing for relay key sharing)
2. PR `cc-mini/cloud-mcp` to main after Parker reviews
3. Deploy cloud MCP after Parker provides Cloudflare credentials
4. Release

## Stats

- 159K+ chunks in crystal.db
- 5 local interfaces (CLI, MCP, OpenClaw, CC hook, module)
- 2 Workers (relay dead drop, cloud MCP)
- 3 embedding providers (OpenAI, Ollama, Google)
- 6 supported surfaces (ChatGPT + Claude on macOS/iOS/web)
