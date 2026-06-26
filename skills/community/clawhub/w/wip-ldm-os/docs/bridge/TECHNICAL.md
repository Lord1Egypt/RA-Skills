# Bridge ... Technical Reference

## Architecture

```
Claude Code CLI (cc-mini, cc-air, or any CC session)
  |
  |-- On boot --> registerSession() --> ~/.ldm/sessions/{name}.json (session discovery)
  |
  |-- MCP stdio --> wip-bridge MCP server (single process)
  |                   |
  |                   |-- lesa_send_message --> HTTP POST localhost:18789 (OpenClaw gateway)
  |                   |                          |
  |                   |                          v
  |                   |                        Lesa's agent pipeline
  |                   |                          |
  |                   |                          v
  |                   |                        Response returned
  |                   |
  |                   |-- lesa_check_inbox --> HTTP GET localhost:18790 (Bridge inbox)
  |                   |
  |                   |-- lesa_conversation_search --> SQLite (context-embeddings.sqlite)
  |                   |
  |                   |-- lesa_memory_search --> filesystem (workspace/*.md)
  |                   |
  |                   |-- oc_skill_* --> exec scripts in ~/.openclaw/extensions/*/skills/

CC <-> CC (multi-session):
  CC session A --> registerSession() --> ~/.ldm/sessions/a.json
  CC session B --> registerSession() --> ~/.ldm/sessions/b.json
  CC session A --> listSessions()    --> discovers session B (agent ID, PID, cwd)
  CC session B --> listSessions()    --> discovers session A
  Communication via file-based message bus at ~/.ldm/sessions/
```

## MCP Tools

| Tool | What | Transport |
|------|------|-----------|
| `lesa_send_message` | Send message to OpenClaw agent | HTTP POST to gateway (localhost:18789) |
| `lesa_check_inbox` | Check for pending messages from agent | In-memory queue (drained on read) |
| `lesa_conversation_search` | Semantic search over conversation history | SQLite + OpenAI embeddings |
| `lesa_memory_search` | Keyword search across workspace .md files | Filesystem scan |
| `lesa_read_workspace` | Read a specific workspace file | Filesystem |
| `oc_skill_*` | Execute OpenClaw skill scripts | child_process exec |
| `oc_skills_list` | List all available OpenClaw skills | Filesystem scan |

## Config Resolution

Bridge resolves config in two steps:

1. **LDM OS path** (`~/.ldm/config.json`): checks for `openclawDir`, `workspaceDir`, `dbPath`
2. **Legacy path** (`OPENCLAW_DIR` env or `~/.openclaw`): fallback

Both return the same `BridgeConfig` shape: `openclawDir`, `workspaceDir`, `dbPath`, `inboxPort`, `embeddingModel`, `embeddingDimensions`.

## Gateway Authentication

Bridge reads the gateway auth token from `~/.openclaw/openclaw.json` (`gateway.auth.token`). Every HTTP request to the gateway includes `Authorization: Bearer <token>`.

## Conversation Search

Two modes:
1. **Vector search** (if OpenAI API key available): embeds query, computes cosine similarity against all conversation chunks, applies recency weighting (exponential decay, half-life ~50 days)
2. **Text search** (fallback): SQL LIKE query against chunk text

The API key is resolved from: environment variable > 1Password via service account token.

## Inbox Server

Bridge starts a localhost-only HTTP server on port 18790:
- `POST /message`: push a message (from OpenClaw agent)
- `GET /status`: check pending count

Messages are held in memory. `lesa_check_inbox` drains the queue.

## Session Discovery

On boot, Recall registers the session via `registerSession()` from `lib/sessions.mjs`. Each session writes a JSON file to `~/.ldm/sessions/{name}.json` containing:

- `name` — session identifier
- `agentId` — agent identity (e.g. `cc-mini`, `cc-air`)
- `pid` — process ID (used for liveness checks)
- `startTime` — ISO timestamp
- `cwd` — working directory

`listSessions()` reads all session files, validates PID liveness (signal 0 probe), and auto-cleans stale entries. Filter by `agentId` to find specific agents. `sessionCount()` returns a quick count of live sessions.

CLI: `ldm sessions` lists all active sessions.

This enables CC-to-CC awareness without a broker daemon. Any session can discover any other session on the machine.

## Key Files

| File | What |
|------|------|
| `src/bridge/core.ts` | Pure logic: config, messaging, search, skills |
| `src/bridge/mcp-server.ts` | MCP server: tool registration, inbox HTTP server |
| `src/bridge/cli.ts` | CLI wrapper (`lesa` command) |
| `lib/sessions.mjs` | Session registration, discovery, PID liveness |
| `dist/bridge/` | Compiled output (ships with npm package) |

## ChatCompletions Routing (Fork Patches)

OpenClaw's gateway exposes an OpenAI-compatible chatCompletions endpoint at `http://localhost:18789/v1/chat/completions`. Upstream OpenClaw does not route these requests to the main agent session. We carry 4 patches on our fork to make this work.

**Patch 1: Session routing via `user=main`.**
When a CC session or external client sends a chatCompletions request, the gateway needs to know which OpenClaw session to route it to. This patch reads the `user` field from the request body. If `user=main` (or `user=openclaw`), the request routes to the main agent session (`agent:main:main`). Without this, bridge messages get "no session found" errors.

```
POST /v1/chat/completions
Authorization: Bearer <gateway-token>
Content-Type: application/json

{"model":"openclaw","messages":[{"role":"user","content":"hi"}],"user":"main"}
```

**Patch 2-3: Steer-backlog queue integration.**
When the agent is already busy (processing an iMessage from Parker), a concurrent chatCompletions request would fail or get dropped. These patches wire the chatCompletions endpoint into OpenClaw's `steer-backlog` queue (config: `messages.queue.mode: "steer-backlog"`). The message waits and gets processed after the current turn finishes. Works for both streaming and non-streaming responses. The gateway returns an `x-openclaw-queued: next-turn` header when a message is queued.

**Patch 4: Header rename.**
Cosmetic rename of the queue response header from `x-openclaw-queued: steer` to `x-openclaw-queued: next-turn` for clarity.

**Source:** `src/gateway/openai-http.ts`. Total patch size: ~100 lines. Carried on branch `cc-mini/chat-completions-v<version>`, rebased on each OpenClaw upgrade.

**Why not upstream:** OpenClaw's chatCompletions endpoint is designed for external API compatibility, not for multi-agent bridge routing. Our use case (CC sessions talking to an OpenClaw agent on the same machine) is specific to the LDM OS architecture.

## Cooperative Push Architecture (Shipped Apr 11)

The original bridge used a pull model: CC sessions called `lesa_check_inbox` to check for messages. Messages sat unread until the next manual check. This was replaced with a cooperative push system where messages are delivered automatically.

### Four Delivery Layers

Messages flow through four layers in order of priority. All four cooperate via shared `read: true` state on disk so a message delivered by one layer is skipped by the others.

| # | Layer | Fires when | Hook type | File |
|---|-------|-----------|-----------|------|
| 1 | **asyncRewake** (Stop hook) | New message arrives while session is idle | `fs.watch` on `~/.ldm/messages/` | `src/hooks/inbox-rewake-hook.mjs` |
| 2 | **UserPromptSubmit** | Next user prompt (typed or automated) | Claude Code hook | `src/hooks/inbox-check-hook.mjs` |
| 3 | **SessionStart** | New CC session boots | Claude Code hook | `src/hooks/boot-hook.mjs` |
| 4 | **Manual** | Explicit tool call | MCP tool | `lesa_check_inbox` |

**Layer 1 (asyncRewake)** is the autonomous push mechanism. It holds a long-lived `fs.watch` on `~/.ldm/messages/`, uses a per-session lockfile to prevent watcher stacking, and exits code 2 on a match to wake the idle model via Claude Code's task-notification path. It fires `fireBatch()` to deliver all pending matches in one wake cycle (cost linear in unique messages, not in layers).

**Layer 2 (UserPromptSubmit)** surfaces messages as `additionalContext` before each prompt. Messages appear in the session context without the user calling `lesa_check_inbox`.

**Deduplication:** Each layer marks messages `read: true` on disk after delivery. Subsequent layers check this flag and skip already-delivered messages. No double delivery. Cost is linear in unique messages, not in layers.

### File Inbox

Messages live as JSON files at `~/.ldm/messages/`:

```json
{
  "id": "uuid",
  "type": "chat",
  "from": "lesa",
  "to": "cc-mini:session-name",
  "body": "message text",
  "read": false,
  "timestamp": "2026-04-11T19:05:00-07:00"
}
```

### Addressing

| Format | Meaning |
|--------|---------|
| `cc-mini` | Default session of agent cc-mini |
| `cc-mini:brainstorm` | Named session "brainstorm" on cc-mini |
| `cc-mini:*` | Broadcast to ALL sessions of cc-mini |
| `*` | Broadcast to all agents on the machine |
| `lesa` | The OpenClaw agent (routes through gateway chatCompletions) |

**Known issue (Apr 11):** Agent-broadcast without session specifier (`to: cc-mini`) fans out to ALL matching sessions. Three sessions replied independently to the same message. The addressing logic needs dedup for agent-broadcast targeting.

### Tools

| Tool | Direction | Transport |
|------|-----------|-----------|
| `ldm_send_message` | Any agent → file inbox | Writes JSON to `~/.ldm/messages/` |
| `lesa_send_message` | CC → OpenClaw agent | HTTP POST to gateway chatCompletions |
| `lesa_check_inbox` | CC ← OpenClaw agent | Reads + drains `~/.ldm/messages/` for this session |

### Plan Document

Full architecture: `ai/product/plans-prds/bridge/2026-04-11--cc-mini--autonomous-push-architecture.md` (377 lines, 8 open questions, Phase A shipped, Phase B deferred for CloudKit cross-machine transport).

## Node Communication (Future)

Bridge currently works localhost only (Core). For Node -> Core communication:
- Phase 7 (Cloud Relay) handles messaging via encrypted Cloudflare R2 dead drops
- Search, workspace read, and skill execution from a Node are NOT yet covered
- Two proposed solutions: proxy pattern (Node sends requests through relay) and sync pattern (replicate crystal.db to Node)

See `ai/products/plans-prds/current/ldm-stack-spec.md` for the full platform matrix.

## CLI Usage

```bash
lesa send "What are you working on?"     # Message the OpenClaw agent
lesa search "API key resolution"          # Semantic search (recency-weighted)
lesa memory "compaction"                  # Keyword search across workspace files
lesa read MEMORY.md                       # Read a workspace file
lesa read memory/2026-02-10.md            # Read a daily log
lesa status                               # Show bridge configuration
lesa diagnose                             # Check gateway, inbox, DB, skills health
```

## Skill Bridge

On startup, Bridge scans OpenClaw's skill directories and exposes them as MCP tools. Claude Code gets the same skills the OpenClaw agent has.

1. Scans `extensions/*/node_modules/openclaw/skills/` (built-in) and `extensions/*/skills/` (custom)
2. Parses each `SKILL.md` frontmatter for name, description, requirements
3. Skills with a `scripts/` folder get registered as executable `oc_skill_{name}` tools
4. All skills show up in `oc_skills_list`

Skills that need API keys get them from the environment. The op-secrets plugin sets these from 1Password.

## Inbox Watcher (Auto-Relay)

Polls the inbox endpoint and auto-injects messages into a running Claude Code tmux session.

```bash
bash scripts/watch.sh                    # Alert mode (notification only)
bash scripts/watch.sh --auto claude:0.0  # Auto-inject into tmux pane
```

| Setting | Default | Description |
|---------|---------|-------------|
| `POLL_INTERVAL` | `5` | Seconds between inbox checks |
| `COOLDOWN` | `30` | Minimum seconds between alerts |
| `INBOX_URL` | `http://127.0.0.1:18790/status` | Inbox status endpoint |

## OpenClaw Skills (Lesa -> CC)

Two skills shipped with Bridge for the reverse direction:

| Skill | What |
|-------|------|
| `claude-code` | Invoke Claude Code CLI for coding tasks (`claude -p`) |
| `send-to-claude-code` | Push messages into CC's live inbox (POST localhost:18790) |

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENCLAW_DIR` | Yes | `~/.openclaw` | Path to OpenClaw installation |
| `OPENAI_API_KEY` | For semantic search | Resolved from 1Password | OpenAI API key for embeddings |
| `LESA_BRIDGE_INBOX_PORT` | No | `18790` | Inbox HTTP server port |

## Ports

| Port | Service | Bound to |
|------|---------|----------|
| 18789 | OpenClaw gateway | localhost (managed by OpenClaw) |
| 18790 | Bridge inbox | localhost (managed by Bridge) |

## Requirements

- OpenClaw running with gateway enabled
- `gateway.auth.token` set in `openclaw.json`
- `gateway.http.endpoints.chatCompletions.enabled: true`
- OpenAI API key for semantic search (falls back to text search without it)
