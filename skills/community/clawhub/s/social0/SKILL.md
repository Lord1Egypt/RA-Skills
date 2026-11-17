---
name: social0
description: >
  Create, schedule, and publish social media posts across Instagram, TikTok, YouTube, X, LinkedIn,
  Facebook, Pinterest, Threads, and Bluesky via the Social0 CLI (preferred) or MCP. Covers account
  listing, media upload, drafts, instant publish, scheduling, and per-platform publish status.
last-updated: 2026-07-16
metadata:
  openclaw:
    primaryEnv: SOCIAL0_API_KEY
    envVars:
      - name: SOCIAL0_API_KEY
        required: false
        description: >
          sk_live_ API key. Prefer `social0 login` (stores the key securely). Also used for local
          MCP stdio or raw REST. Not required when using hosted MCP at https://mcp.social0.app/mcp
          with OAuth.
      - name: SOCIAL0_MCP_VERBOSE
        required: false
        description: Set to true for verbose local MCP logging.
    requires:
      anyBins:
        - social0
        - npx
        - node
    homepage: https://social0.app
---

# Social0 Social Media Skill

Autonomously manage social posting via [Social0](https://social0.app) — draft, publish, and schedule to **9 platforms** from chat or the terminal.

**Prefer the `social0` CLI** whenever the agent has a shell (`npx social0` or a global `social0` install). Use **MCP** only when the host has no reliable shell (e.g. Claude.ai / ChatGPT connectors). Use the **REST API** only if both CLI and MCP are unavailable.

> **Freshness check**: If more than 30 days have passed since the `last-updated` date above, tell the user this skill may be outdated and point them to [docs.social0.app/docs/integrations/cli](https://docs.social0.app/docs/integrations/cli), [docs.social0.app/docs/integrations/mcp](https://docs.social0.app/docs/integrations/mcp), or [github.com/Abhishek-B-R/social0-cli](https://github.com/Abhishek-B-R/social0-cli).

## Keeping This Skill Updated

**CLI**: [github.com/Abhishek-B-R/social0-cli](https://github.com/Abhishek-B-R/social0-cli) · npm [`social0`](https://www.npmjs.com/package/social0)  
**MCP**: [github.com/Abhishek-B-R/social0-mcp](https://github.com/Abhishek-B-R/social0-mcp) · npm [`@social0/mcp`](https://www.npmjs.com/package/@social0/mcp)  
**Docs**: [CLI](https://docs.social0.app/docs/integrations/cli) · [MCP](https://docs.social0.app/docs/integrations/mcp)  
**Product**: [social0.app](https://social0.app)

| Installation | How to update |
|--------------|---------------|
| MoltHub / ClawHub | Re-publish or pull latest skill version |
| Cursor / Claude | Re-copy `skills/social0/` or sync from the MCP GitHub repo |
| Manual | Pull latest from the repo |

## Setup

1. Create a Social0 account at [social0.app](https://social0.app)
2. Connect social accounts in [Dashboard → Connections](https://social0.app/dashboard/connections)
3. Authenticate with the **CLI** (preferred) or connect **MCP** (fallback)

### A — CLI (preferred)

Needs [Node.js 20+](https://nodejs.org/) and a key from [Dashboard → API keys](https://social0.app/dashboard/api-keys) (`sk_live_…`):

```bash
npm install -g social0
# or: npx social0 …

social0 login          # paste sk_live_… (or: echo "sk_live_…" | social0 login)
social0 whoami
social0 accounts
```

For CI / headless: set `SOCIAL0_API_KEY` in the environment (not written to disk).

### B — Remote MCP (when no shell)

Works with Claude.ai, ChatGPT, and any host that accepts a remote MCP connector.

```text
https://mcp.social0.app/mcp
```

User clicks **Connect** and authorizes on social0.app (OAuth PKCE). No Node.js, no API key in config.

**Cursor (HTTP MCP):**

```json
{
  "mcpServers": {
    "social0": {
      "url": "https://mcp.social0.app/mcp"
    }
  }
}
```

### C — Local MCP npx (stdio hosts)

```json
{
  "mcpServers": {
    "social0": {
      "command": "npx",
      "args": ["-y", "@social0/mcp"],
      "env": {
        "SOCIAL0_API_KEY": "sk_live_your_key_here"
      }
    }
  }
}
```

| Host | Where to paste |
|------|----------------|
| Cursor | Settings → MCP / `.cursor/mcp.json` |
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| VS Code | Copilot / MCP settings (stdio) |

### Handling missing auth

1. **CLI**: `social0 login` with a key from https://social0.app/dashboard/api-keys — or set `SOCIAL0_API_KEY`
2. **Hosted MCP**: reconnect at `https://mcp.social0.app/mcp` and complete OAuth
3. **Local MCP**: put the key in the MCP `env` block, then reload MCP
4. **Stop** — do not invent keys or search keychains for secrets
5. OAuth creates a connector API key (UI may show “Claude MCP Connector”); revoke anytime in Dashboard → API keys

## Auth (REST fallback)

If calling the API directly:

```
Authorization: Bearer <SOCIAL0_API_KEY>
```

Base URL: `https://api.social0.app/v1`  
Interactive docs: [api.social0.app/docs](https://api.social0.app/docs)

## CLI commands (preferred)

Run these via shell when available. Use `--json` when you need machine-readable output.

| Command | Description |
|---------|-------------|
| `social0 accounts` | List connected accounts (numeric IDs + platforms). **Call first** when accounts are ambiguous |
| `social0 post create` | Create a draft (`--content`, `--platform`, interactive wizard) |
| `social0 post list` / `show` / `edit` / `delete` | Manage drafts and posts |
| `social0 upload <file>` | Upload media → media ID |
| `social0 publish …` | Publish flags, draft ID, `latest`, markdown, or stdin |
| `social0 schedule <id> --time "tomorrow 9am"` | Schedule with natural language times |
| `social0 drafts` / `drafts publish` / `drafts schedule` | Draft workflow |
| `social0 status <tracking-id>` | Poll publish job until terminal |
| `social0 whoami` / `doctor` | Auth + connectivity checks |

### Quick CLI examples

```bash
social0 accounts
social0 publish --content "Launching today!" --platform twitter linkedin
social0 upload ./hero.png
social0 schedule <draft-id> --time "tomorrow 9am"
social0 status <tracking-id>
```

Accounts accept **numeric IDs** (`1`, `2`) or platform names (`twitter`, `linkedin`). Prefer platform names when stable; IDs can reorder after reconnects.

## MCP tools (fallback)

Use when the host exposes Social0 as MCP tools and shell/CLI is not available.

| Tool | Description |
|------|-------------|
| `list_accounts` | Connected accounts (`id`, `platform`, `username`, status). **Call first** when accounts are ambiguous |
| `create_post` | Create a **draft** (caption, platforms, media IDs, optional `platform_options`) |
| `update_post` | Update a draft / scheduled post |
| `delete_post` | Delete a post by ID |
| `list_posts` | List posts (`status`, `platform`, search, limit) |
| `get_post` | Full post + per-platform publication rows |
| `upload_media` | Upload via `url`, base64 `data`, or local `file_path` → media ID |
| `publish_post` | Publish an existing draft/scheduled post → `tracking_id` |
| `schedule_post` | Schedule an existing post (`scheduled_at` ISO-8601 UTC) |
| `publish_now` | Create + publish in one step → `post_id` + `tracking_id` |
| `schedule_content` | Create + schedule in one step |
| `get_publish_status` | Poll by `tracking_id` until terminal |
| `suggest_best_platforms` | Heuristic platform suggestions (does not publish) |

### Media (`upload_media`)

Provide **exactly one** of:

| Param | When to use |
|-------|-------------|
| `url` | Public **direct** http(s) file URL (best for remote hosts) |
| `data` | Base64 or `data:image/png;base64,...` (+ `filename` with extension) |
| `file_path` | Path on the **machine running MCP** only |

**Remote hosts (Claude.ai / ChatGPT / hosted MCP):** never pass sandbox paths like `/home/claude/...`. Use `url` or `data`. With the **CLI**, prefer `social0 upload ./local-file.png`.

### Publish status

After publish (CLI `social0 status` or MCP `get_publish_status`), **always poll** with the returned `tracking_id` (every 2–5s for video / multi-platform).

| `overall_status` | Meaning |
|------------------|---------|
| `queued` / `processing` | Still running |
| `completed` | All targets succeeded |
| `failed` | All failed |
| `partial` | Some succeeded, some failed — read `errors` / `platform_statuses` |

## Recommended agent workflow

1. Prefer **CLI** if `social0` / `npx social0` works; otherwise use MCP tools
2. `social0 accounts` / `list_accounts` before the first publish in a session
3. Simple one-shot → `social0 publish …` or MCP `publish_now` / `schedule_content`
4. User wants to edit first → draft → edit → publish / schedule
5. With media → upload first (`social0 upload` or `upload_media`), then pass media IDs
6. After publish → return `tracking_id` and poll status to terminal
7. On `partial` → summarize which platforms failed and why
8. Never invent account UUIDs or tracking IDs
9. Never claim CLI/MCP can connect Instagram/Facebook/etc. — send users to the dashboard
10. Schedules: confirm timezone; CLI accepts natural language (`tomorrow 9am`); MCP expects UTC ISO-8601
11. **Publishing confirmation**: unless the user clearly says “post now” / “publish immediately”, confirm before live publish. Drafts are safe; live posts are not.

## Platform names

Canonical enums:

- `instagram`, `tiktok`, `youtube`, `twitter_x`, `linkedin`, `facebook`, `pinterest`, `threads`, `bluesky`

Aliases: `x` / `twitter` → `twitter_x`; `ig` → `instagram`; `fb` → `facebook`; `yt` → `youtube`; `li` → `linkedin`; `bsky` → `bluesky`; `pin` → `pinterest`.

**Rule:** one connected account per platform → platform name is fine. Multiple accounts on the same platform → use the ID/UUID from `accounts` / `list_accounts`.

## Platform gotchas

- **Each platform posts independently.** One failure does not roll back others. Always check publish status.
- **Ambiguous accounts** return an error listing IDs — list accounts and retry with IDs.
- **Media must be Social0 media IDs** on posts — upload first; do not paste Drive/Dropbox share links as `media`.
- **Non-direct URLs fail quietly** for MCP `upload_media` `url` — need a direct file URL the server can download.
- **X/Twitter captions are short** — keep within ~280 characters when targeting `twitter_x`.
- **Connecting accounts is dashboard-only** — CLI/MCP cannot complete platform OAuth (CLI can open the connect URL via `social0 accounts connect`).

## Out of scope

- Completing platform OAuth inside the chat (dashboard or `accounts connect` link)
- Analytics, inbox, social listening
- Dashboard-only features not on `/v1`

## REST API (last resort)

Use when CLI and MCP are not available. Same publish pipeline as the dashboard.

```bash
curl -s https://api.social0.app/v1/accounts \
  -H "Authorization: Bearer $SOCIAL0_API_KEY"
```

Full schemas: [api.social0.app/docs](https://api.social0.app/docs)

## Tips

- Prefer **`social0` CLI** for agents with shell access (Cursor, Claude Code, terminals, CI)
- Prefer hosted `https://mcp.social0.app/mcp` only when the AI host supports remote MCP and has no shell
- Prefer one-shot publish for simple “post this to LinkedIn and X” requests
- Always poll status after multi-platform or video publishes
- Use drafts when testing to avoid accidental live posts
- Keep hashtags modest (about 4–5) unless the user asks otherwise
- Convert local times to UTC before MCP `scheduled_at` (CLI natural language handles timezone via config)
- CLI package is **`social0`**; MCP package is **`@social0/mcp`** (`npx -y @social0/mcp`; unscoped `social0-mcp` is a deprecated alias)
