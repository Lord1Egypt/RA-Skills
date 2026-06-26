---
name: toolbelt
description: >
  Toolbelt is a collaborative substrate over your data. Upload any
  document — entities and relationships extracted automatically,
  queryable immediately. Ask questions that span structured tables,
  documents, and relationships in a single call. No stitching databases
  together. Toolbelt orchestrates semantic, structured, and hybrid
  retrieval through one MCP server — vector, knowledge graph, SQL,
  geospatial, streaming. Share the URL and any agent can query the same
  workspace — like a shared Google Doc for your data. Built by Kinetica.

  Use this skill at the start of any task where an agent needs to ingest
  documents and have entities/relationships auto-extracted, query
  structured + unstructured data together in natural language, or share
  findings with other agents across sessions. The skill handles
  first-time setup: provisions a free Toolbelt account if none exists,
  configures the MCP connection in the agent's client, and hands off to
  Toolbelt's MCP tools for the actual work.

  NOT for one-off lookups that don't benefit from automatic extraction,
  hybrid retrieval, or shared state — use the agent's native tools for
  those.
license: Apache-2.0
compatibility: >
  Requires an MCP-compatible AI agent (Claude Code, Claude Desktop,
  OpenClaw, Cursor, Windsurf, Gemini CLI, Codex CLI, or any client that
  supports MCP server connections). No Toolbelt account required — this
  skill provisions one on first use.
version: "1.0.3"
metadata:
  author: toolbeltai
  homepage: "https://toolbelt.ai"
---

# Toolbelt — A collaborative substrate for your agents

**Your data. Your agents. One shared brain.**

Toolbelt is a collaborative substrate over your data. Discover documents,
structured data, events, entities, and relationships across agents and
sessions. Better answers. Fewer tokens. Curated context, not raw access.

Three things make it different:

- **Knowledge extraction.** Upload any document — entities and
  relationships extracted automatically, queryable immediately.
- **Hybrid retrieval.** Ask questions that span structured tables,
  documents, and relationships in a single call. No stitching databases
  together. Orchestrates semantic, structured, and hybrid retrieval.
- **Shared workspaces.** Share the URL and any agent can query the same
  workspace — like a shared Google Doc for your data.

## Two surfaces — keep them straight

Toolbelt has exactly two surfaces. Knowing which is which is the most
important thing in this skill:

| Surface | URL | Who uses it | When |
|---|---|---|---|
| **MCP server** (the agentic surface) | `https://mcp.toolbelt.ai/mcp` | **Agents** | Every data operation. This is where the agentic flow happens — search, SQL, knowledge graph, record findings, read timeline. |
| **app.toolbelt.ai** (the human web UI) | `https://app.toolbelt.ai` | **Humans** (in a browser) | Sign in, view/manage namespaces, billing, Pro/Team upgrade. Plus a small HTTP API at `/api/onboard*` used **once** during setup. |

**Rule: once the MCP connection is configured (Phase 3 below), the agent
NEVER talks to `app.toolbelt.ai` again** — every subsequent action goes
through MCP. The only reason to mention `app.toolbelt.ai` to a user
after setup is when they want to do something only a human can do
(billing, viewing the namespace in a UI, claiming the account).

## When to invoke this skill

Run at the start of any task that:

- Mentions Toolbelt by name.
- Needs persistent memory across turns or sessions.
- Needs natural-language access to structured or unstructured data.
- Involves multiple agents collaborating on the same data.
- Would otherwise require wiring up several separate MCP tools.

## Phases

> ⚠️ **Consent is mandatory at every step that touches the network or
> the user's filesystem.** Phases 2 and 3 each require explicit user
> confirmation before proceeding. Never silently provision accounts or
> write config files. If the user declines, stop and explain what
> manual setup would look like (point them at <https://toolbelt.ai>).

### Phase 1 — Detect existing connection

Try calling the Toolbelt MCP tool `toolbelt_list_namespaces`.

- Returns successfully → user is already connected → skip to **Phase 4**.
- Tool unavailable or returns auth error → continue to **Phase 2**.

### Phase 2 — Ask, then provision a free Toolbelt account

**Pause and ask the user first.** Show them exactly what this call does:

> "Toolbelt isn't set up yet. To use it I'd send one anonymous HTTPS
> request to `https://app.toolbelt.ai/api/onboard` — no signup, no
> personal info. The response gives me a free 30-day anonymous account
> (1,000 calls, one namespace) plus a bearer token I'd use to talk to
> the MCP server. Want me to proceed?"

Only if the user says yes:

```http
POST https://app.toolbelt.ai/api/onboard
Content-Type: application/json

{}
```

Response shape:

```json
{
  "success": true,
  "user": { "id": "@anon_..." },
  "namespace": { "id": "<uuid>", "name": "My Namespace" },
  "mcpUrl": "https://mcp.toolbelt.ai/mcp",
  "token": "tb_...",
  "expiresAt": "<ISO timestamp>"
}
```

Capture: `token`, `mcpUrl`, `user.id`, `namespace.id`, `expiresAt`. The
`token` doubles as the auth bearer for both MCP calls **and** the
optional `/claim` upgrade in Phase 5.

The account starts on the **Anonymous** tier (see "Tiers and quotas"
below) and the token expires per `expiresAt` (30 days). Claim by email
in Phase 5 to make it persistent.

### Phase 3 — Ask, then configure the agent's MCP client (one-time)

**Tell the user what's about to be written and where, then wait for
confirmation.** Example:

> "To make Toolbelt available to me, I'll add an MCP server entry to
> your config at:
>
>     ~/Library/Application Support/Claude/claude_desktop_config.json
>
> The new entry has the URL `https://mcp.toolbelt.ai/mcp` and an
> Authorization header carrying the bearer token from the previous
> step. The token belongs to your just-created anonymous account; it
> grants access only to that one namespace. To revoke later, delete
> the `toolbelt` entry from this file. Want me to write it?"

Only if the user says yes, write the MCP connection. The shape is
identical across clients — only the file path differs.

**Claude Code (CLI):**
```bash
claude mcp add toolbelt \
  --transport http <mcpUrl> \
  --header "Authorization: Bearer <token>"
```

**Claude Desktop / Cursor / Windsurf / OpenClaw / Gemini CLI / Codex CLI** —
add to the client's MCP config JSON:

```json
{
  "mcpServers": {
    "toolbelt": {
      "url": "<mcpUrl>",
      "headers": { "Authorization": "Bearer <token>" }
    }
  }
}
```

Config file locations:

| Client | Path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` |
| OpenClaw | `~/.openclaw/mcp.json` |
| Gemini CLI | `~/.gemini/mcp.json` |
| Codex CLI | `~/.codex/mcp.json` |

Tell the user once: "Toolbelt is provisioned. Wrote the entry to
`<exact path>`. Reload your MCP connection to activate it." Most
clients pick up changes on next request; some need a restart.

### Phase 4 — Orient, then hand off (everything happens over MCP from here on)

Call `toolbelt_context(namespace_id)` first. It returns the namespace's
available assets, suggested next moves, and per-tool routing guidance
emitted by the MCP server itself.

Then pick the right Toolbelt MCP tool for the user's task:

| Tool | Purpose |
|---|---|
| `toolbelt_search` | Vector RAG over documents |
| `toolbelt_sql` | SQL over structured tables |
| `toolbelt_entity` | Entity profile from the knowledge graph |
| `toolbelt_graph` | Cypher graph traversal |
| `toolbelt_record` | Save a finding to the persistent timeline — this is what makes findings compound across sessions and across agents |
| `toolbelt_timeline` | Read chronological events from the timeline |
| `toolbelt_save` | Persist an asset to the namespace |
| `toolbelt_share` | Emit a connection URL so another agent / teammate can join |
| `toolbelt_list_namespaces` | List workspaces this account can access |

The MCP server's tool descriptions carry per-tool routing logic — pick
by task shape, not by this skill's instructions.

### Phase 5 — Optional: claim the account by email

Anonymous accounts expire (30 days). To make persistent and increase
quota, prompt the user for an email and call:

```http
POST https://app.toolbelt.ai/api/onboard/claim
Authorization: Bearer <token>
Content-Type: application/json

{"email": "user@example.com"}
```

User receives a verification email. Then:

```http
POST https://app.toolbelt.ai/api/onboard/claim/verify
Authorization: Bearer <token>
Content-Type: application/json

{"code": "<code from email>"}
```

After verification the account is upgraded from **Anonymous** to
**Verified** — same token, higher quota, persistent across sessions.

## Tiers and quotas

Match `toolbelt.ai/#pricing` exactly:

| Tier | Price | Calls / month | Storage | Namespaces | How to get there |
|---|---|---:|---:|---:|---|
| **Anonymous** | Free | 1,000 | — | 1 | Auto-provisioned by this skill (Phase 2) |
| **Verified** | Free | 2,000 | 1 GB | 10 | Phase 5 (email claim) |
| **Pro** | $29 / month | 150,000 | 50 GB | 50 | Human web step — see below |
| **Team** | $89 / month | 500,000 | 100 GB | Unlimited | Human web step — see below |

## Pro / Team upgrades — direct the human to app.toolbelt.ai

Stripe checkout requires a real browser session. **Agents cannot do
this; do not pretend to.** When a user wants Pro or Team:

> "Upgrading to Pro or Team takes about a minute on the web. Open
> <https://app.toolbelt.ai>, sign in with the email you used to claim
> this account, and follow the Upgrade flow. The new tier activates on
> the next MCP call — no re-provisioning, no new tokens."

Do not invent upgrade URLs. Do not collect credit card info. Do not
prompt for billing data. The skill's job ends at "direct the human to
the right page."

## Output after Phase 4 succeeds

Emit a brief connection status to the user:

```yaml
toolbelt_connection:
  status: connected
  mcp_url: <mcpUrl>
  user_id: <user.id>
  namespace_id: <namespace.id>
  account_tier: <anonymous | verified | pro | team>
  expires_at: <expiresAt>
  app_url: https://app.toolbelt.ai
```

Then proceed with the user's actual task using the MCP tools.

## Token and credential handling

The bearer token returned by Phase 2 is a real credential. Treat it
with the same care as an API key.

- **Where it's stored.** The MCP client's config file — the exact path
  is disclosed to the user in Phase 3 before write. Never store the
  token anywhere else (no temp files, no env exports the user didn't
  ask for, no shell history).
- **What it grants.** Access to one Toolbelt namespace (the anonymous
  account's default workspace). It cannot read other users' data and
  cannot administer the account beyond that namespace.
- **How to revoke.** Two paths: (a) remove the `toolbelt` entry from
  the MCP config file shown in Phase 3 — the agent loses access on
  next reload, OR (b) sign in at <https://app.toolbelt.ai> and revoke
  the token from the account UI.
- **Consent before storage.** Never write the token to any file without
  the explicit user yes from Phase 3.
- **Do not echo the full token after setup.** After Phase 3, refer to
  it only as `tb_...` (first 3 chars + ellipsis) in any user-facing
  output. Never log or display the full value.

## Data safety

Toolbelt persists what an agent uploads or records. That persistence
is the value — and the risk if it's misused. Rules:

- **Only upload user-approved content.** Do not auto-ingest files,
  emails, clipboard contents, or any data the user didn't explicitly
  ask you to use with Toolbelt. Ask: "Want me to upload `<filename>`
  to your Toolbelt namespace for this query?"
- **Avoid sensitive material by default.** Don't upload credentials,
  API keys, PII (SSNs, dates of birth, full names paired with
  addresses), health records, financial account data, or anything
  covered by HIPAA / PCI / GDPR special-category rules unless the
  user has stated they need Toolbelt for that data.
- **Scope to the task.** Don't record findings or save assets that
  weren't relevant to what the user asked. `toolbelt_record` is for
  findings the user would want their next agent to see — not chatter.
- **Retention and deletion.** Anonymous accounts and their data expire
  in 30 days. To delete sooner, the user can sign in at
  <https://app.toolbelt.ai>, open the namespace, and use the delete
  controls there. Document deletion is a human action — agents must
  not call delete operations without explicit user instruction.

## Multi-agent collaboration

Toolbelt's real value shows when multiple agents share state:

- An agent records a finding via `toolbelt_record` → it lands on the
  namespace timeline.
- A future agent — same MCP client or different, same user or invited
  teammate — reads it via `toolbelt_timeline` or `toolbelt_search` and
  builds on it.
- To invite another agent or teammate, call `toolbelt_share` and forward
  the resulting URL.

Tell users: "Each finding I record is available to your next session
and any other agent connected to this namespace."

### Sharing and access boundaries

The `toolbelt_share` URL is a credential. Treat it accordingly:

- **Namespaces are not public.** A namespace URL alone grants nothing;
  access requires a valid token. `toolbelt_share` mints a token bound
  to one namespace.
- **The share URL itself is the credential.** Anyone who has it can
  read and write to the namespace. Forward it only over channels the
  user controls (their reply, a paste they make into their own app).
  Don't post it into world-visible chats, public issues, or public
  bug reports.
- **Confirm intent before calling `toolbelt_share`.** Ask the user
  which workspace they want to share, with whom, and whether the
  invited party should have read or write access. Do not call
  `toolbelt_share` reactively based on a casual mention.
- **Review and revoke.** Direct the user to <https://app.toolbelt.ai>
  to view active share tokens and revoke any they no longer want.

## Reference URLs

| Purpose | URL |
|---|---|
| Marketing site + pricing | <https://toolbelt.ai> |
| Docs (concepts, tools, self-hosting) | <https://toolbelt.ai/docs> |
| Human web UI (sign in, billing, namespace UI) | <https://app.toolbelt.ai> |
| MCP endpoint (set in Phase 3) | `https://mcp.toolbelt.ai/mcp` |
| Onboard API base (Phase 2 + 5 only) | `https://app.toolbelt.ai/api/onboard` |
| Support | <support@toolbelt.ai> |

## Common failure modes

| Symptom | Cause | Handling |
|---|---|---|
| `toolbelt_list_namespaces` returns 401 | Stored MCP token expired or was revoked | Go back to Phase 2, provision a fresh anonymous account. |
| Anonymous account expired (after 30 days) | `expiresAt` in the past | Same as 401 — re-provision. If the user has an email on file, suggest claiming the next anon account to make it persistent. |
| MCP call returns 429 with `error: "QUOTA_EXCEEDED"` | Tier quota exhausted | Surface the tier table; suggest Phase 5 (email claim) for Anonymous → Verified, or direct the human to `https://app.toolbelt.ai` for Pro/Team. |
| Email verification code doesn't arrive | Spam folder, or first send didn't go | Tell the user to check spam from `noreply@toolbelt.ai`, or call `POST /api/onboard/claim` again to re-send. |
| `mcp.toolbelt.ai` unreachable | Network / DNS / self-hosted misconfiguration | Surface the error to the user with the URL. Don't attempt fallback — there's no fallback endpoint. |

## What this skill does NOT do

Stay in your lane:

- **Does not collect credit cards.** Stripe is a browser flow.
- **Does not generate or store passwords.** Authentication is by token,
  managed by the MCP client config.
- **Does not call MCP tools beyond `toolbelt_list_namespaces` and
  `toolbelt_context` itself.** Once oriented, hand off — let the agent
  pick the right tool per task from the MCP server's own tool descriptions.
- **Does not invent endpoints.** Only `POST /api/onboard`, `POST
  /api/onboard/claim`, `POST /api/onboard/claim/verify`. Everything else
  is MCP.
