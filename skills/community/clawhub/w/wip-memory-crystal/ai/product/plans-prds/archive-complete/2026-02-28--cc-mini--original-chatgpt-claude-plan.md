# Memory Crystal for ChatGPT + Claude: Implementation Plan

## Context

Memory Crystal is WIP.computer's persistent memory layer. It already runs locally (159K+ chunks, hybrid search, 5 interfaces). Parker wants it available inside ChatGPT and Claude (iOS, macOS, web) as a focused memory tool... not the whole WIP OS.

**Key decisions from discussion:**
- Custom GPT Actions are deprecated. MCP is the only path. One MCP server serves all surfaces.
- ChatGPT and Claude both support remote HTTP MCP servers. One server, six surfaces.
- ChatGPT/Claude sessions are LDM agents (like cc-air, oc-lesa-mini). Agent IDs: `gpt-macos`, `gpt-ios`, `gpt-web`, `claude-macos`, `claude-ios`, `claude-web`.
- Three product tiers with fundamentally different security models.
- The existing relay architecture is the foundation for Tier 1.

---

## Six-Surface Compatibility

One remote HTTP MCP server covers all platforms:

| Surface | Platform | How it connects |
|---------|----------|----------------|
| ChatGPT macOS | Desktop app | Developer Mode / Apps connector |
| ChatGPT iOS | Mobile app | Developer Mode / Apps connector |
| ChatGPT web | chatgpt.com | Developer Mode / Apps connector |
| Claude macOS | Desktop app | Settings > Connectors (remote MCP) |
| Claude iOS | Mobile app | Auto-syncs from web/desktop setup |
| Claude web | claude.ai | Settings > Connectors |

Both use the same MCP protocol, same OAuth 2.0, same tool annotations. No platform-specific code needed.

**Distribution:** Submit to ChatGPT Apps Directory (OpenAI) AND Anthropic Connectors Directory separately. Same server, two listings.

**Claude Desktop bonus:** Also supports local stdio MCP. Memory Crystal already has a local MCP server (mcp-server.ts). Claude Desktop users get both local (full Crystal) and remote (relay/cloud) access.

---

## Three-Tier Product Architecture

### Tier 1: Sovereign (free, default)

**Write-only relay. No searchable cloud data. Maximum privacy.**

ChatGPT conversations flow to the Mini via the existing encrypted relay. The cloud Worker stores nothing readable. Just encrypted blobs in transit.

```
ChatGPT (iOS/macOS) → [MCP server] → [encrypt AES-256-GCM] → Relay Worker (R2) → Mini poller [decrypt] → crystal.db
```

- ChatGPT can WRITE memories (remember) ... encrypted, relayed to Mini
- ChatGPT can NOT SEARCH ... no plaintext in the cloud
- Search only works from devices with local Crystal access (Claude Code CLI, OpenClaw)
- Mini must be online to pick up relayed data (but data waits in R2 if Mini is sleeping)
- Data at cloud: encrypted blobs only. Cloudflare cannot read them.
- Uses the existing relay worker, poller, and crypto modules.

**This is the existing architecture with ChatGPT added as a source.**

### Tier 2: Convenience (paid, opt-in)

**Cloud search enabled. Mirror pushed to D1 + Vectorize. Privacy trade-off disclosed.**

User explicitly opts in to cloud search. A mirror of crystal.db is pushed to Cloudflare D1 + Vectorize. ChatGPT can now search memories.

```
ChatGPT → [MCP server] → D1/Vectorize (plaintext, searchable) → results
                      ↘ [encrypt] → Relay → Mini (also stores)
Mini → [mirror push] → D1/Vectorize (periodic sync)
```

- ChatGPT can WRITE and SEARCH
- Data at cloud: plaintext in D1, vectors in Vectorize. Cloudflare infrastructure encryption only.
- Users are clearly informed: "Cloud search means your memories are readable at the cloud layer."
- Mini is still source of truth. Cloud mirror is a cache.
- If cloud is wiped, Mini still has everything.

### Tier 3: Enterprise (self-hosted)

**Same as Tier 2, but on the customer's own infrastructure.**

Memory Crystal is the software. The customer runs the Worker on their own Cloudflare account (or equivalent). Their D1, their Vectorize, their keys. WIP.computer never sees their data.

- Same codebase as Tier 2, different deployment target
- Customer brings their own: Cloudflare account, domain, OpenAI API key
- WIP.computer provides: software, documentation, support
- Future: could run on AWS (Postgres + pgvector), Azure, or bare metal

**Not built in v1.** The architecture supports it by keeping config external (wrangler.toml, env vars).

---

## What Gets Built (v1 scope)

### Tier 1 is the v1 ship target.

Tier 1 leverages almost everything that already exists:
- Relay worker (`worker.ts`, 210 LOC) ... already built
- Poller (`poller.ts`, 346 LOC) ... already built
- Crypto (`crypto.ts`, 113 LOC) ... already built
- Mirror sync (`mirror-sync.ts`, 176 LOC) ... already built

**What's new for Tier 1:**
1. A remote MCP server that ChatGPT connects to (Streamable HTTP, OAuth + DCR)
2. The MCP tools call the relay to write (encrypted), not D1
3. `memory_search` returns a message like: "Search is available on your local devices. This session's memories have been saved to your Mini."
4. `memory_status` shows relay status (connected, pending drops)

**Wait... that means Tier 1 can't do cloud search at all.** The tool surface changes:

| Tool | Tier 1 Behavior | Tier 2 Behavior |
|------|----------------|----------------|
| `memory_search` | Returns "search available on local devices only" | Full hybrid search |
| `memory_remember` | Encrypts + relays to Mini | Stores in D1/Vectorize AND relays to Mini |
| `memory_forget` | Queues a deprecation command for Mini | Deprecates in D1 AND queues for Mini |
| `memory_status` | Shows relay health, pending drops | Shows memory count, categories, cloud status |

### Tier 2 is the v1.1 follow-up.

Adds: CloudCrystal class (D1 + Vectorize), mirror sync from Mini, real search.

---

## MCP Server Architecture (Both Tiers)

One MCP server. One Worker. Tier determined by user's subscription/config.

**Endpoint:** `https://memory-crystal.wipcomputer.workers.dev/mcp`

**Tool definitions (4 tools, same for both tiers):**

```typescript
memory_search   // readOnlyHint: true, openWorldHint: false
memory_remember // readOnlyHint: false, destructiveHint: false, openWorldHint: false
memory_forget   // readOnlyHint: false, destructiveHint: true, idempotentHint: true
memory_status   // readOnlyHint: true, openWorldHint: false
```

**Input schemas:**
- `memory_search(query: string, limit?: number)` ... limit default 5, max 20
- `memory_remember(text: string, category?: 'fact'|'preference'|'event'|'opinion'|'skill')`
- `memory_forget(id: number)`
- `memory_status()` ... no args

---

## OAuth 2.1 + DCR

Auth server co-located in the MCP Worker. ~300-400 LOC.

**Discovery:**
- `GET /.well-known/oauth-protected-resource`
- `GET /.well-known/oauth-authorization-server`

**Endpoints:**
- `POST /oauth/register` ... DCR (ChatGPT self-registers)
- `GET /oauth/authorize` ... Consent page
- `POST /oauth/token` ... Code exchange with PKCE S256

**State (D1):**
- `oauth_clients`, `authorization_codes`, `access_tokens` tables
- user_id derived from verified email hash

**Redirect URIs:**
- `https://chatgpt.com/connector_platform_oauth_redirect`
- `https://platform.openai.com/apps-manage/oauth`

**Payment gating (designed in, wired later):** The `users.tier` column and consent page are the integration points for wip-agent-pay. Before issuing a token, check subscription status. Free tier gets Tier 1 (relay only). Paid tier gets Tier 2 (cloud search). For v1 launch, all users get both tiers (or just Tier 1). The tier check is a single `if` in the token issuance flow... payment plugs in later without refactoring. The consent page can show a "subscribe for cloud search" button once wip-agent-pay is ready, or link to a website checkout. No corners cut.

---

## Data Model

### Tier 1 (relay only)

No new D1 tables for memory data. OAuth tables only:

```sql
CREATE TABLE oauth_clients (
  client_id TEXT PRIMARY KEY,
  redirect_uris TEXT NOT NULL,
  client_name TEXT,
  created_at TEXT NOT NULL,
  last_used_at TEXT
);

CREATE TABLE authorization_codes (
  code TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  code_challenge TEXT NOT NULL,
  redirect_uri TEXT NOT NULL,
  scope TEXT,
  expires_at TEXT NOT NULL,
  used INTEGER DEFAULT 0
);

CREATE TABLE access_tokens (
  token_hash TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  scope TEXT,
  tier TEXT NOT NULL DEFAULT 'sovereign',
  expires_at TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE users (
  user_id TEXT PRIMARY KEY,
  email TEXT NOT NULL,
  tier TEXT NOT NULL DEFAULT 'sovereign',
  relay_token TEXT,
  created_at TEXT NOT NULL
);
```

### Tier 2 (adds cloud storage)

Same as local Crystal schema, with user_id:

```sql
CREATE TABLE chunks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT NOT NULL,
  text TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'user',
  source_type TEXT NOT NULL DEFAULT 'chatgpt',
  source_id TEXT NOT NULL DEFAULT '',
  agent_id TEXT NOT NULL DEFAULT 'gpt',
  token_count INTEGER DEFAULT 0,
  created_at TEXT NOT NULL
);

CREATE TABLE memories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT NOT NULL,
  text TEXT NOT NULL,
  category TEXT NOT NULL DEFAULT 'fact',
  confidence REAL NOT NULL DEFAULT 1.0,
  source_ids TEXT DEFAULT '[]',
  status TEXT NOT NULL DEFAULT 'active',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE VIRTUAL TABLE chunks_fts USING fts5(text, content='chunks', content_rowid='id');
```

Vectorize index: `memory-crystal-vectors` (1536 dims, cosine).

---

## LDM Agent Integration

ChatGPT and Claude sessions appear as agents in the LDM tree:

```
~/.ldm/agents/
  cc-mini/           -- Claude Code on Mac Mini
  cc-air/            -- Claude Code on MacBook Air
  oc-lesa-mini/      -- OpenClaw (Lesa) on Mac Mini
  gpt-macos/         -- ChatGPT on macOS (NEW)
  gpt-ios/           -- ChatGPT on iOS (NEW)
  gpt-web/           -- ChatGPT on web (NEW)
  claude-macos/      -- Claude Desktop connector (NEW)
  claude-ios/        -- Claude iOS connector (NEW)
  claude-web/        -- Claude web connector (NEW)
```

The relay poller ingests drops into crystal.db with agent_id from source metadata. Same chunking, same embedding, same search index. All conversations become searchable from any local device.

---

## Phased Build

### Phase 0: Project Setup (1 day)
- Create `repos/memory-crystal-cloud-private/` (new repo, private/public pattern)
- `wrangler init`, configure D1 binding (OAuth tables only for Tier 1)
- Port types from core.ts
- Set up R2 binding to existing relay bucket (or new channel)

### Phase 1: MCP Server + OAuth (3-4 days)
- Streamable HTTP MCP server on Cloudflare Workers
- OAuth 2.1 with DCR, PKCE S256, consent page
- All four tool stubs (Tier 1 behavior)
- `memory_remember` encrypts + drops to relay
- `memory_forget` queues deprecation to relay
- `memory_search` returns "available on local devices"
- `memory_status` returns relay health
- Deploy to Cloudflare

### Phase 2: Poller Integration (1-2 days)
- Extend existing poller to handle ChatGPT drops (new channel: `chatgpt`)
- Agent ID assignment (gpt-macos, gpt-ios based on source metadata)
- LDM scaffolding for new agent IDs
- Test: remember from ChatGPT, verify it appears in local `crystal search`

### Phase 3: Testing + Custom GPT + Claude Connector (1-2 days)
- Test in ChatGPT Developer Mode (all four tools)
- Test as Claude connector (Settings > Connectors, same server URL)
- Create Custom GPT "Memory Crystal" with MCP server
- Write system instructions for deterministic memory behavior
- Test on iOS, macOS, and web for both ChatGPT and Claude
- Verify end-to-end: remember from any surface → relay → Mini → searchable locally

### Phase 4: Directory Submissions (1-2 days)
- Privacy policy, ToS, support contact
- Developer verification with OpenAI + Anthropic
- Submit to ChatGPT Apps Directory
- Submit to Anthropic Connectors Directory
- Same server, two listings

### Phase 5: Tier 2 Cloud Search (3-5 days, v1.1)
- CloudCrystal class (D1 + Vectorize, ported from core.ts)
- Mirror sync from Mini to cloud D1/Vectorize
- `memory_search` upgraded to real hybrid search for Tier 2 users
- Tier gating in auth (check user.tier before serving search)
- wip-agent-pay integration at consent page

**v1 total: 6-9 days.** v1.1 adds 3-5 days.

---

## File Map

```
repos/memory-crystal-cloud-private/
  src/
    index.ts              -- Worker entry, request router
    auth.ts               -- OAuth 2.1 (DCR, authorize, token, verify)
    mcp.ts                -- MCP tool definitions + annotations
    relay.ts              -- Encrypt + drop to relay (reuses crypto.ts patterns)
    types.ts              -- Shared types (from core.ts)
    storage.ts            -- CloudCrystal class (Tier 2, D1 + Vectorize)
    embed.ts              -- OpenAI embedding wrapper (Tier 2)
  migrations/
    0001_init.sql          -- OAuth tables + users
    0002_cloud_storage.sql -- Chunks + memories (Tier 2)
  wrangler.toml
  package.json
  tsconfig.json
  docs/
    privacy-policy.md
    terms-of-service.md
    gpt-system-instructions.md
    security-disclosure.md  -- "What cloud search means for your data"
```

---

## Critical Source Files (What to Reuse)

| Existing File | Reuse For |
|--------------|-----------|
| `memory-crystal-private/src/crypto.ts` | AES-256-GCM encryption for relay drops |
| `memory-crystal-private/src/worker.ts` | Cloudflare Worker patterns, relay channel handling |
| `memory-crystal-private/src/poller.ts` | Extend to handle ChatGPT channel |
| `memory-crystal-private/src/core.ts` | RRF fusion, search algorithm (Tier 2 port) |
| `memory-crystal-private/src/mcp-server.ts` | MCP tool definition patterns |
| `memory-crystal-private/wrangler.toml` | Cloudflare account bindings |

---

## Security Model

| Layer | Tier 1 (Sovereign) | Tier 2 (Convenience) |
|-------|-------------------|---------------------|
| In transit | HTTPS + AES-256-GCM encrypted payload | HTTPS |
| At cloud | Encrypted blobs only (R2) | Plaintext in D1, vectors in Vectorize |
| Cloudflare can read | No | Yes (infrastructure encryption only) |
| Mini offline | Data waits in R2 (24h TTL) | Cloud still serves search |
| Nuke cloud | Lose nothing (Mini has all) | Lose cache (Mini has all) |

**Tier 2 disclosure (mandatory):** "When cloud search is enabled, your memories are stored in readable form at Cloudflare's edge. This is the same security model as Notion, Slack, and most SaaS products. Cloudflare applies infrastructure-level encryption. If you need zero-cloud storage, use Tier 1 (Sovereign)."

---

## Known Challenges + Mitigations

1. **Workers + MCP SDK:** Use `@cloudflare/agents` package or implement minimal JSON-RPC handler.
2. **Tier 1 search limitation:** ChatGPT can't search in Tier 1. Mitigate with clear messaging. The value is still: "your ChatGPT conversations are captured and searchable from your local devices."
3. **D1 lacks sqlite-vec (Tier 2):** Vectorize replaces it. Two-step: Vectorize for IDs, D1 for metadata.
4. **OAuth complexity:** ~300-400 LOC. PKCE verification is ~50 lines. JWT signing native to Workers.
5. **Relay key distribution:** ChatGPT MCP server needs the encryption key to drop to relay. Store as Wrangler secret. Same key as existing relay.

---

## Verification

### Tier 1 (v1)
```
[ ] OAuth flow works (DCR, authorize, token)
[ ] memory_remember encrypts and drops to relay
[ ] Mini poller picks up drops from all surfaces
[ ] Ingested chunks appear in local crystal search with correct agent_id
[ ] memory_search returns sovereign-mode message
[ ] memory_status shows relay health
[ ] Works in ChatGPT Developer Mode
[ ] Works as Claude connector (web, macOS, iOS)
[ ] Custom GPT functional on iOS, macOS, web
[ ] Privacy policy published
[ ] Both directory submissions prepared
```

### Tier 2 (v1.1)
```
[ ] D1 + Vectorize created and migrated
[ ] memory_search returns hybrid ranked results
[ ] Mirror sync from Mini populates cloud
[ ] Tier gating works (sovereign users can't search cloud)
[ ] wip-agent-pay integration at consent page
[ ] Apps Directory submission accepted
```

## Business Readiness

```
[ ] OpenAI developer/org verification
[ ] Privacy policy with tier-specific disclosures
[ ] Terms of service
[ ] Support contact
[ ] App metadata: "Memory Crystal" / Productivity
[ ] Tool annotations correct
[ ] Security disclosure document published
[ ] Rate limits per tier
```
