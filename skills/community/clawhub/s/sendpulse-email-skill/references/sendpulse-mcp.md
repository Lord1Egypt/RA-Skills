# SendPulse MCP server — manage campaigns without writing code

> Read this when the user's AI client supports MCP (Claude, ChatGPT, Cursor, and
> other MCP-compatible clients). Connected once, the assistant calls SendPulse
> actions as tools — manage address books, contacts, and campaigns straight from
> chat, no API code needed. Docs: sendpulse.com/features/mcp.

## 1. What it is

SendPulse runs a hosted MCP server at **`https://mcp.sendpulse.com/mcp`**.
Cloud-hosted, nothing to install. Once connected, SendPulse tools appear in the
session and this skill can drive the whole campaign lifecycle through them instead
of generating API code — the right default for **interactive, chat-driven work**
("create a book, add these contacts, send the campaign").

Rule of thumb for choosing the path:

| Situation | Use |
|---|---|
| User works interactively in an AI chat/agent | **MCP tools** (this file) |
| User builds an app/integration that runs on its own | **REST API** ([api-reference.md](api-reference.md), [examples/](../examples/)) |

## 2. Connecting (one-time, ≈10 min)

1. In the AI client, open MCP/connector settings and add the server URL
   `https://mcp.sendpulse.com/mcp`.
2. Authenticate with the SendPulse account — a **Single API Key**
   (*Settings → API → API keys*) is the preferred credential; account login also
   works.
3. Grant access and enable the tool groups the user needs (email address books,
   campaigns, templates).

## 3. Tools relevant to this skill

Tool names follow a `domain_action` pattern, e.g. `email_addressbooks_get` (list
mailing lists) and `email_template_create` (save a template). The exact list
depends on what the user enabled and the current MCP version — **discover the
available `email_*` tools at runtime** instead of hardcoding names; they may
evolve.

Everything this skill teaches still applies when working through MCP tools: pick a
segment instead of the whole base, verified sender, test first, check the cost,
tracking + UTM, and the review expectations from [campaigns.md](campaigns.md).

## 4. Safety rule — sending is outward-facing

Creating books, adding contacts, saving templates, reading stats — safe to do
directly. **Launching a campaign sends real email to real people.** Before
triggering any send via MCP, always confirm with the user: the exact list/segment,
sender, subject, and scheduled time. Never auto-send as a side effect of another
request.

## 5. When MCP isn't connected

Don't fail — offer the fallbacks in order:

1. **Connect MCP** (walk through §2) — best for ongoing interactive work.
2. **REST API** — generate code from [examples/](../examples/) with their API key.
3. **Dashboard** — point them to the exact screens (Email → Mailing lists /
   Campaigns) with the pre-flight checklist from [quickstart.md](quickstart.md).
