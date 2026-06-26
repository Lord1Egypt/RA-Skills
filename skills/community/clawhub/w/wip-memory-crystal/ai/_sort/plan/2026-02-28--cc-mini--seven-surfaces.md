# Memory Crystal: Install Surfaces

*Written 2026-02-28 by Claude Code*

## The Problem

Memory Crystal needs to work from any surface a user starts on. Some users have a Mac with Crystal installed locally. Some users only have an iPhone with ChatGPT. The install experience and data flow must work for every surface, and a user who starts on one should be able to add others later without losing anything.

## Four Install Surfaces

The user sees four distinct install experiences. Each one works for both ChatGPT and Claude.

| # | Install Surface | Platform | Local machine? | AI platforms served |
|---|----------------|----------|---------------|-------------------|
| 1 | Web | Desktop browser | No* | chatgpt.com + claude.ai |
| 2 | iOS app | iPhone/iPad | No | ChatGPT app + Claude app |
| 3 | macOS app | Desktop app | Yes | ChatGPT app + Claude app |
| 4 | OpenClaw | Mac (terminal) | Yes | OpenClaw agents |

*Web runs on a desktop, but the browser itself has no local Crystal. The user could also install Crystal locally on that Mac, making it hybrid.

These four surfaces produce seven connection points (ChatGPT web, Claude web, ChatGPT iOS, Claude iOS, ChatGPT macOS, Claude macOS, OpenClaw). But the user doesn't think in terms of seven things. They think: "I want to use Memory Crystal on my phone" or "I want to add it to my Mac." Four install experiences.

## Three Categories

### Category A: Cloud-Only (no local machine)

**Surfaces:** Web (1), iOS app (2)

The user has no Crystal running locally. Everything lives in the cloud. This is Tier 2 (cloud search) by necessity... there's nowhere else to put the data.

**What happens:**
- User connects Memory Crystal via MCP connector/app (OAuth flow)
- Data stored in D1 (text + metadata) and Vectorize (embeddings)
- Search works immediately
- All tools functional: search, remember, forget, status
- Conversation capture via memory_log / memory_upload

**What they don't get:**
- Local sovereignty (data is in Cloudflare infrastructure)
- Full JSONL transcript archives
- Source file indexing
- Cross-agent search with local agents (none exist)

**Migration path:** When user later gets a Mac and installs Crystal locally, they run `crystal init --pull-cloud` to download their entire cloud history into a local crystal.db. They can then switch to Tier 1 (sovereign) if they want.

### Category B: Hybrid (cloud + local)

**Surface:** macOS app (3)

The user has a Mac. They can install Crystal locally AND connect to the cloud. Best of both worlds.

**What happens:**
- Connect cloud MCP in ChatGPT/Claude Desktop settings (same OAuth flow as Category A)
- Optionally install Crystal locally: `npm install -g memory-crystal && crystal init`
- If local Crystal installed: captures Desktop/CLI sessions via hooks, local search available
- Cloud MCP captures web/mobile sessions
- Relay syncs between cloud and local
- Local crystal.db becomes source of truth

**Two sub-modes:**

**B1: Tier 1 (Sovereign).** Cloud MCP encrypts everything and relays to local machine. No readable data in the cloud. Search only works locally (Desktop/CLI can use local MCP). Remote sessions (iOS, web) can remember but not search.

**B2: Tier 2 (Convenience).** Cloud MCP stores readable data in D1 + Vectorize. Search works everywhere (phone, browser, desktop). Local machine also has everything via mirror sync.

### Category C: Local-Only

**Surface:** OpenClaw (4)

The user runs Crystal on their Mac through OpenClaw. No cloud, no remote surfaces.

**What happens:**
- Install memory-crystal plugin in OpenClaw
- All data in local crystal.db
- agent_end hook captures all conversations automatically
- Search, remember, forget all work locally

**Migration path:** When user wants mobile access, run `crystal init --push-cloud` to upload existing memories to the cloud Worker. Then connect ChatGPT/Claude on mobile.

## Install Flow Per Surface

### Surface 1: Web (Desktop Browser)

Same experience on chatgpt.com and claude.ai.

```
User opens chatgpt.com or claude.ai in browser
  -> Settings -> Apps/Connectors
  -> Search "Memory Crystal" (or paste server URL)
  -> OAuth consent page opens
  -> Sign up (email) or sign in
  -> Authorize Memory Crystal
  -> Token issued, connection established
  -> Tools appear in chat: search, remember, forget, status
  -> First use: memory_status shows "0 memories, cloud mode"
  -> User starts using. Data stored in D1 + Vectorize.
```

**Category:** A (cloud-only)
**Tier:** 2 (cloud search, only option)
**Data location:** Cloudflare D1 + Vectorize
**Agent IDs:** `gpt-web` or `claude-web` (from OAuth metadata)
**Time to first use:** ~30 seconds

### Surface 2: iOS App

Same experience on ChatGPT and Claude iOS apps.

```
User opens ChatGPT or Claude on iPhone
  -> Settings -> Apps/Connectors
  -> Search "Memory Crystal" (or paste server URL)
  -> OAuth consent page opens in Safari
  -> Sign up or sign in (same account as web if they have one)
  -> Authorize
  -> Back to app, tools appear
  -> Cloud-only, Tier 2
```

**Category:** A (cloud-only)
**Tier:** 2 (only option)
**Data location:** Cloudflare D1 + Vectorize
**Agent IDs:** `gpt-ios` or `claude-ios`
**Time to first use:** ~30 seconds

**Key detail:** If user already connected on web (Surface 1), their memories are already there. Same account, same data. Adding iOS is just connecting another surface.

### Surface 3: macOS App

Same experience on ChatGPT and Claude Desktop apps. Plus optional local install.

```
User opens ChatGPT or Claude Desktop on Mac
  -> Settings -> Apps/Connectors
  -> Search "Memory Crystal" (or paste server URL)
  -> OAuth flow (same as web/iOS)
  -> Tools appear (cloud-backed)

OPTIONAL (recommended for power users):
  -> Open Terminal
  -> npm install -g memory-crystal
  -> crystal init
  -> Installer detects ChatGPT/Claude Desktop
  -> Registers local stdio MCP server (faster, sovereign)
  -> Registers Stop hook for conversation capture
  -> Installs .claude/rules/memory-crystal.md (Claude only)
  -> Prompts for embedding API key (OpenAI or Ollama)
  -> Offers to pull cloud data: crystal init --pull-cloud
  -> Local MCP takes priority for search
  -> Cloud connection stays active for iOS/web sync
```

**Category:** B (hybrid) or A (cloud-only if they skip local install)
**Tier:** User's choice (1 or 2)
**Data location:** Local crystal.db (primary if installed) + cloud (synced)
**Agent IDs:** `gpt-macos` / `claude-macos` (cloud), `cc-mini` or custom (local)
**Time to first use:** ~30 seconds (cloud), ~5 minutes (with local install)

### Surface 4: OpenClaw

Local plugin install on Mac. No cloud involved by default.

```
User has OpenClaw installed
  -> Install memory-crystal plugin:
     cd ~/.openclaw
     # copy plugin files to extensions/memory-crystal/
     npm install --omit=dev
  -> openclaw gateway restart
  -> Plugin registers tools: crystal_search, crystal_remember, crystal_forget
  -> agent_end hook captures all conversations automatically
  -> Data goes to local crystal.db
  -> Works immediately, no account needed

OPTIONAL (for multi-device):
  -> crystal init --push-cloud
  -> Creates cloud account
  -> Uploads existing memories
  -> Configures relay for ongoing sync
  -> Connect ChatGPT/Claude on phone for mobile access
```

**Category:** C (local-only) or B (if cloud enabled later)
**Tier:** 1 (sovereign, default)
**Data location:** Local crystal.db
**Agent ID:** `oc-{agent}-{machine}` (from OpenClaw config)
**Time to first use:** ~5 minutes

## The Matrices

### Install Experience Matrix

| Surface | Install steps | Account needed? | Local install? | Time to first use |
|---------|--------------|----------------|---------------|-------------------|
| Web | 3 clicks + OAuth | Yes (email) | No | ~30 sec |
| iOS app | 3 taps + OAuth | Yes (email) | No | ~30 sec |
| macOS app | 3 clicks + OAuth | Yes (email) | Optional | ~30 sec (cloud), ~5 min (local) |
| OpenClaw | Plugin copy + restart | No | Yes (required) | ~5 min |

### Data Flow Matrix

| Surface | Writes to | Reads from | Relay? | Works offline? |
|---------|----------|-----------|--------|---------------|
| Web (ChatGPT + Claude) | D1 + Vectorize | D1 + Vectorize | No | No |
| iOS (ChatGPT + Claude) | D1 + Vectorize | D1 + Vectorize | No | No |
| macOS app (cloud only) | D1 + Vectorize | D1 + Vectorize | Optional | No |
| macOS app (local installed) | crystal.db | crystal.db | Yes (to/from cloud) | Yes |
| OpenClaw | crystal.db | crystal.db | Optional | Yes |

### Tool Availability Matrix

| Tool | Cloud-only (Web, iOS) | Hybrid (macOS with local) | Local-only (OpenClaw) |
|------|----------------------|--------------------------|---------------------|
| search | Cloud search (D1 + Vectorize) | Local hybrid search (BM25 + vector + RRF) | Local hybrid search |
| remember | Stores in D1 | Stores in crystal.db (+ syncs to cloud) | Stores in crystal.db |
| forget | Deprecates in D1 | Deprecates locally (+ syncs) | Deprecates locally |
| status | Cloud stats | Local + cloud stats | Local stats |
| memory_log | Stores turns in D1 | Relay to local (encrypted) | N/A (hooks capture) |
| memory_upload | Stores in R2 | Relay to local (encrypted) | N/A (local files) |
| sources_add/sync | Not available | Local only | Local only |

### Tier Availability Matrix

| Surface | Tier 1 (Sovereign) | Tier 2 (Cloud Search) |
|---------|-------------------|----------------------|
| Web | Not possible (no local) | Default, only option |
| iOS app | Not possible (no local) | Default, only option |
| macOS app (cloud only) | Not possible | Default |
| macOS app (local installed) | Yes (user's choice) | Yes (user's choice) |
| OpenClaw | Default | Yes (if cloud enabled) |

### Agent ID Matrix

| Connection | Agent ID | How assigned |
|-----------|---------|-------------|
| ChatGPT web | `gpt-web` | OAuth token metadata |
| ChatGPT iOS | `gpt-ios` | OAuth token metadata |
| ChatGPT macOS | `gpt-macos` | OAuth token metadata |
| Claude web | `claude-web` | OAuth token metadata |
| Claude iOS | `claude-ios` | OAuth token metadata |
| Claude macOS (remote) | `claude-macos` | OAuth token metadata |
| Claude macOS (local CLI) | `cc-mini` or custom | CRYSTAL_AGENT_ID env var |
| OpenClaw | `oc-{agent}-{machine}` | OpenClaw agent config |

## Migration Paths

### Cloud -> Local ("I got a Mac")

User has been using Memory Crystal on iOS/web. Now they have a Mac.

```
1. npm install -g memory-crystal
2. crystal init --pull-cloud
   -> Authenticates with cloud Worker (same OAuth account)
   -> Downloads all chunks from D1 into local crystal.db
   -> Downloads all memories
   -> Downloads attachments from R2
   -> Sets up relay for ongoing sync
3. User now has full local Crystal with their entire history
4. Can switch to Tier 1 (sovereign) if desired
5. Optional: crystal cloud wipe (delete cloud copies)
```

### Local -> Cloud ("I want it on my phone")

User has Crystal on their Mac (OpenClaw or local install). Wants mobile access.

```
1. crystal init --push-cloud
   -> Creates cloud account (OAuth)
   -> Uploads crystal.db contents to D1 + Vectorize
   -> Configures relay for ongoing sync
2. Connect Memory Crystal in ChatGPT/Claude on phone
3. Same account. All memories already there.
4. New mobile sessions sync back to local crystal.db
```

### Adding a Surface ("I also want it in Claude")

User already has Memory Crystal on ChatGPT. Wants to add Claude (or vice versa).

```
1. Open Claude (or ChatGPT)
2. Settings -> Connectors/Apps
3. Connect Memory Crystal
4. Same OAuth account
5. Same data. Same memories. Different agent ID.
6. No migration. Just connect.
```

## Cloud Architecture

One Worker serves all four install surfaces and all seven connection points:

```
Cloud Worker (memory-crystal.wipcomputer.workers.dev)
  |
  |-- /mcp                    <- MCP endpoint (all tools)
  |-- /oauth/register         <- DCR (ChatGPT/Claude auto-register)
  |-- /oauth/authorize        <- Consent page + signup
  |-- /oauth/token            <- Token exchange (PKCE)
  |
  |-- D1: memory_crystal_db
  |   |-- users              <- accounts, tier, relay config
  |   |-- oauth_clients      <- registered MCP clients
  |   |-- access_tokens      <- active sessions (scoped per user)
  |   |-- chunks             <- conversation data (per user_id)
  |   |-- memories           <- explicit memories (per user_id)
  |
  |-- Vectorize: memory-crystal-vectors
  |   |-- embeddings         <- vector index (per user namespace)
  |
  |-- R2: memory-crystal-relay
      |-- {user}/relay/      <- encrypted drops (Tier 1 users)
      |-- {user}/attachments/<- binary files
```

User isolation via user_id on every query. One Worker, one D1, one Vectorize, one R2.

## Impact on v1 Scope

The previous plan assumed Tier 1 (relay only) for v1, with Tier 2 (cloud search) as v1.1. That doesn't work anymore.

**Cloud search (Tier 2) must be in v1.** Because:
- 2 of 4 install surfaces have no local machine (Web, iOS)
- "Remember only, can't search" is not a product on mobile
- Users who start on their phone will bounce if they can't search their own memories

**Revised v1 scope:**
1. Cloud MCP server with OAuth + DCR (in progress, PR #10)
2. D1 + Vectorize for cloud search (moved from v1.1 to v1)
3. Encrypted relay for hybrid users (Tier 1 option)
4. `crystal init` standalone installer for macOS
5. `crystal init --pull-cloud` and `--push-cloud` migration

**Still v1.1 or later:**
- Claude Code auto memory indexing (local-only feature)
- .claude/rules/ file (local-only feature)
- npm public distribution
- OpenAI/Anthropic directory submissions
- Tier 3 (enterprise/self-hosted)

## Verification

```
Surface 1 (Web):
[ ] OAuth flow works in desktop browser
[ ] Works on chatgpt.com
[ ] Works on claude.ai
[ ] Search returns results
[ ] Remember stores in D1 + embeds in Vectorize
[ ] Same account works across both AI platforms

Surface 2 (iOS App):
[ ] OAuth flow works in mobile Safari redirect
[ ] Works in ChatGPT iOS app
[ ] Works in Claude iOS app
[ ] Tools appear and function
[ ] Same account as web (shared data)

Surface 3 (macOS App):
[ ] Cloud connection works (same as web)
[ ] Optional local install (crystal init) works
[ ] Local MCP registers for Claude Desktop
[ ] Stop hook captures CLI sessions
[ ] Cloud and local don't conflict
[ ] Relay syncs between cloud and local

Surface 4 (OpenClaw):
[ ] Plugin installs and loads
[ ] agent_end hook captures conversations
[ ] crystal init --push-cloud uploads to cloud
[ ] Relay syncs ongoing changes

Cross-surface:
[ ] One account works across all surfaces
[ ] Agent IDs correctly differentiate sources
[ ] Search returns results from all connected surfaces
[ ] Cloud -> local migration preserves everything
[ ] Local -> cloud migration preserves everything
[ ] Adding a new surface to existing account works seamlessly
```
