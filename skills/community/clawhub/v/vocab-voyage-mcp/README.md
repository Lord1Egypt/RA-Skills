# Vocab Voyage MCP Server

Hosted MCP (Model Context Protocol) server providing vocabulary tools for standardized test prep — **SAT, ISEE, SSAT, GRE, GMAT, LSAT, PSAT** — and general vocabulary learning.

> 🌐 **Hosted endpoint** (no install required): `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server`
> 📚 **Docs & live demo**: https://vocab.voyage/mcp
> 🔐 **Auth + scopes reference**: https://vocab.voyage/developers/auth
> 🃏 **Server card**: https://vocab.voyage/.well-known/mcp/server-card.json
> 🤖 **Agent card**: https://vocab.voyage/.well-known/agent-card.json

---

## What's included in 1.0

This is the first public release. It already ships with:

- **7 vocabulary tools** (definition, quiz, study plan, courses, word-of-the-day, in-context explainer)
- **MCP Apps UI resources** for `get_definition`, `generate_quiz`, `study_plan_preview` — manifest at `/.well-known/mcp/apps.json`
- **Scoped personal tokens** with four scopes: `mcp.read`, `mcp.tools`, `profile.read`, `progress.read`
- **OAuth Protected Resource Metadata** at `/.well-known/oauth-protected-resource`
- **Canonical auth docs** at https://vocab.voyage/developers/auth (rotation, revocation, error codes)
- **NLWeb `/ask` endpoint** for natural-language queries with optional SSE streaming
- **Markdown content negotiation** on the public REST API, MCP metadata, and API catalog (`Accept: text/markdown`)
- **Schemamap + JSONL feeds** for crawler/agent indexing (`/schemamap.xml`, `/feeds/*.jsonl`)
- **Structured JSON errors** with stable `error_code` values agents can branch on
- **Rate limit headers** (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`)

---

## What it does

Vocab Voyage exposes **7 tools** any MCP-compatible AI assistant can call:

| Tool | Purpose | UI widget |
|---|---|---|
| `get_word_of_the_day` | Today's vocabulary word, optionally scoped to a test family | — |
| `get_definition` | Definition, part of speech, example sentence, synonyms/antonyms | `ui://vocab-voyage/definition` |
| `generate_quiz` | Multiple-choice quiz (1–10 questions) for any test family | `ui://vocab-voyage/quiz` |
| `get_course_word_list` | Sample words from a specific Vocab Voyage course | — |
| `list_courses` | All 13 test-prep courses with slugs and descriptions | — |
| `explain_word_in_context` | Explain a word inside a specific sentence | — |
| `study_plan_preview` | 7-day, 5-words-per-day sample plan for a target test | `ui://vocab-voyage/study-plan` |

---

## Install

### Claude Desktop

**Easiest** — Settings → Connectors → *Add Custom Connector*, paste:

```
https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server
```

**Power users** — Claude Desktop's `claude_desktop_config.json` only accepts stdio commands, so use the [`mcp-remote`](https://github.com/geelen/mcp-remote) bridge. Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "vocab-voyage": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server"]
    }
  }
}
```

To use a personal token, add the `Authorization` header:

```json
{
  "mcpServers": {
    "vocab-voyage": {
      "command": "npx",
      "args": [
        "-y", "mcp-remote",
        "https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server",
        "--header", "Authorization: Bearer vv_mcp_REPLACE_ME"
      ]
    }
  }
}
```

Restart Claude Desktop. The 7 tools appear in the tool tray. Transport is Streamable HTTP (modern); legacy SSE is not used.

### ChatGPT (custom MCP)

Add a custom MCP server in Settings → Connectors:
- **URL**: `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server`
- **Transport**: streamable-http
- **Auth**: None (anonymous) or Bearer token

### OpenClaw

```bash
openclaw skills install vocab-voyage
```

### Cursor / Continue / any MCP client

Use the URL above with transport `streamable-http`.

---

## Authentication

- **Anonymous** (default) — Rate limit 60 requests/minute per IP. All public tools work.
- **Personal token** — Generate a `vv_mcp_…` token at https://vocab.voyage/mcp, choose the scopes you need, and pass as `Authorization: Bearer vv_mcp_…`. Rate limit 600 requests/hour per user. Unlocks personalized tools.

### Scopes

| Scope | Grants |
|---|---|
| `mcp.read` | Read MCP metadata and public tool results. Required for any MCP usage. |
| `mcp.tools` | Invoke public MCP tools (definition, quiz, courses, study plan). |
| `profile.read` | Read connected user's display name, account type, preferred course. |
| `progress.read` | Read mastery, streaks, and recent sessions for the connected user. |

Full reference (rotation, revocation, error codes): https://vocab.voyage/developers/auth

---

## Discovery surfaces

| Surface | URL |
|---|---|
| Server card | https://vocab.voyage/.well-known/mcp/server-card.json |
| Agent card | https://vocab.voyage/.well-known/agent-card.json |
| MCP Apps manifest | https://vocab.voyage/.well-known/mcp/apps.json |
| OAuth protected resource | https://vocab.voyage/.well-known/oauth-protected-resource |
| OpenAPI | https://vocab.voyage/openapi.json |
| API catalog (linkset) | https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/api-catalog |
| NLWeb `/ask` | https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/nlweb-ask |
| Schemamap | https://vocab.voyage/schemamap.xml |
| llms-full | https://vocab.voyage/llms-full.txt |

---

## Architecture

- **Server**: TypeScript on Supabase Edge Functions (Deno runtime)
- **Library**: [`mcp-lite`](https://github.com/fiberplane/mcp-lite) + [`hono`](https://hono.dev)
- **Transport**: `streamable-http`
- **Database**: PostgreSQL (Supabase) for vocabulary content + per-user state
- **Discovery**: RFC 8288 Link headers, RFC 9728 OAuth Protected Resource Metadata, MCP server card, MCP Apps manifest, agent card, schemamap, JSONL feeds

The server source code lives in the main Vocab Voyage application (private repo). This repository is the **distribution manifest** — it's what registries (MCP Registry, Smithery, ClawHub, Glama) read to list us.

---

## Manifests in this repo

| File | Purpose |
|---|---|
| `server.json` | Official MCP Registry manifest (`mcp-publisher publish`) |
| `server-card.json` | MCP server card published at `/.well-known/mcp/server-card.json` |
| `smithery.yaml` | Smithery registry manifest |
| `clawhub.json` | OpenClaw / ClawHub skill manifest |
| `SKILL.md` | OpenClaw skill description (markdown) |
| `SUBMISSION_LINKS.md` | Per-channel `?ref=` URLs for attribution |

---

## Try it live, no install

Open https://vocab.voyage/mcp and use the "Try it live" panel — calls hit the same hosted endpoint your AI assistant will use.

---

## License

MIT — see `LICENSE`.

## Credits

Built by the team behind [Vocab Voyage](https://vocab.voyage), an AI-powered adaptive vocabulary learning platform for grades 1–12 and standardized test prep.

## Publish to the MCP Registry

This repo includes a [`server.json`](./server.json) manifest. To publish to https://registry.modelcontextprotocol.io/:

```bash
brew install mcp-publisher          # macOS / Linux
mcp-publisher login github          # device flow
mcp-publisher publish               # publishes server.json in CWD
```

Verify:
```bash
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=vocab-voyage"
```

The namespace `io.github.jaideepdhanoa/*` is verified via GitHub OAuth — only the owner of that GitHub account can publish under it.
