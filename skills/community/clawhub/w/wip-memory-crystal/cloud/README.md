# Memory Crystal Cloud

Remote MCP server for ChatGPT + Claude. Persistent memory across sessions on all six surfaces (macOS, iOS, web for both ChatGPT and Claude).

## Architecture

One MCP server, two tiers:

**Tier 1 (Sovereign):** Write-only relay. Memories are encrypted (AES-256-GCM) and relayed to your home machine. The cloud cannot read your data. Search is available only on local devices.

**Tier 2 (Convenience):** Cloud search enabled. A mirror of your memory database is pushed to Cloudflare D1 + Vectorize. ChatGPT/Claude can search your memories directly. Privacy trade-off is clearly disclosed.

## Data Flow

Every conversation turn, attachment, and explicit memory flows to the Mini:

```
ChatGPT/Claude → memory_log (every turn)     → [encrypt] → R2 relay → Mini poller → crystal.db
                 memory_remember (explicit)   → [encrypt] → R2 relay → Mini poller → crystal.db
                 memory_upload (files/media)   → [encrypt] → R2 relay → Mini poller → attachments/
                 memory_forget (deprecation)   → [encrypt] → R2 relay → Mini poller → crystal.db
```

The Mini receives the same data it would have if this was a local Claude Code or OpenClaw session:
- Full conversation JSON (raw messages, tool calls, results)
- Inline images and file references
- Binary attachments (images, audio, video, documents)
- Explicit memories and deprecations

## Setup

```bash
# From the memory-crystal-private root:

# 1. Create D1 database
cd cloud && npx wrangler d1 create memory-crystal-cloud
# Copy the database_id into cloud/wrangler.toml

# 2. Run migrations
npm run cloud:db:migrate

# 3. Set secrets
cd cloud
npx wrangler secret put CRYSTAL_RELAY_KEY     # base64, 32 bytes (same as relay)
npx wrangler secret put OAUTH_SIGNING_SECRET  # any random string
npx wrangler secret put OPENAI_API_KEY        # for Tier 2 embeddings

# 4. Deploy
npm run cloud:deploy
```

## Development

```bash
npm run cloud:dev          # local dev server
npm run cloud:db:migrate   # apply D1 migrations locally
```

## Endpoints

| Path | Method | Auth | Description |
|------|--------|------|-------------|
| `/health` | GET | No | Health check |
| `/.well-known/oauth-protected-resource` | GET | No | OAuth resource metadata |
| `/.well-known/oauth-authorization-server` | GET | No | OAuth server metadata |
| `/oauth/register` | POST | No | Dynamic Client Registration |
| `/oauth/authorize` | GET/POST | No | Authorization + consent page |
| `/oauth/token` | POST | No | Token exchange (PKCE S256) |
| `/mcp` | POST | Bearer | MCP JSON-RPC endpoint |

## MCP Tools

| Tool | Description | Annotation |
|------|-------------|-----------|
| `memory_search` | Search memories | readOnly |
| `memory_remember` | Store a memory (fact, preference, event, opinion, skill) | write |
| `memory_forget` | Deprecate a memory by ID | destructive |
| `memory_status` | Show status, pending drops, tier info | readOnly |
| `memory_log` | Log a conversation turn (call every exchange) | write, idempotent |
| `memory_upload` | Upload a file attachment (image, audio, video, doc) | write |

### memory_log

This is the key tool for full data capture. The system prompt instructs the AI to call `memory_log` after every exchange with:
- `role` + `content` (the text)
- `raw_json` (the complete message object as JSON string)
- `tool_calls` (any tools called in the turn)
- `attachments` (inline images, files, audio)
- `session_id` + `turn_index` (for conversation grouping)

The Mini processes these through the same chunking and embedding pipeline used for local sessions.

### memory_upload

Handles binary files. The AI encodes the file as base64 and calls this tool. The file is encrypted (AES-256-GCM) and stored as a separate R2 object. A metadata drop references the blob. The Mini poller picks up both.

Supports: images (png, jpg, webp, gif), audio (mp3, mp4, wav, ogg), video (mp4, webm, mov), documents (pdf, txt, csv).

Max file size: 100MB (R2 single-put limit).

## Files

```
cloud/
  wrangler.toml           -- Cloudflare Worker config
  migrations/
    0001_init.sql          -- D1 schema (OAuth + users)
  README.md               -- this file

src/cloud/
  index.ts                -- Worker entry point, request router
  auth.ts                 -- OAuth 2.1 (DCR, authorize, token)
  mcp.ts                  -- MCP tool definitions + handlers (6 tools)
  relay.ts                -- Encrypt + drop to relay (Web Crypto)
  types.ts                -- Shared types
```
