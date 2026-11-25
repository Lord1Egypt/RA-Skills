# Space Duck MCP Client — Spec (v1, 2026-08-10)

The reverse direction of `mcp_server.py`: the duck **consumes** external MCP
servers as tool sources. `mcp_server.py` makes the duck a USB *port*;
`mcp_client.py` gives the duck USB *plugs*.

## Constitution

1. **Owner adds, owner holds creds.** Servers are registered only by the
   owner on the duck's own box (Lane A) or in the duck's own config (Lane B).
   Secrets live in `~/.space-duck/mcp_secrets.json` (0600), NEVER in the
   platform, NEVER in the skill repo, NEVER on argv (HARDEN-071).
2. **Default-closed allowlist.** A newly added server exposes ZERO tools to
   the duck until the owner runs `allow`. Same doctrine as `update_senders`.
3. **Lane immutability.** Nothing here changes lanes. A Lane A duck's MCP
   clients run on the owner's box; the platform never proxies them.
4. **Stdlib only.** No pip deps. Transports: Streamable HTTP
   (single-response + SSE-formatted response bodies) and stdio
   (newline-delimited JSON-RPC over a spawned subprocess).
5. **Honest passthrough.** Upstream errors/status surface verbatim
   (truncated); no local retry magic beyond one connect attempt.

## Config schema (in `~/.space-duck/config.json`)

```json
"mcp_clients": [
  {
    "name": "github",
    "preset": "github",
    "transport": "stdio",              // or "http"
    "command": ["npx", "-y", "@modelcontextprotocol/server-github"],
    "url": null,                        // http transport only
    "bearer_secret": null,              // key name in mcp_secrets.json
    "env_secrets": {"GITHUB_PERSONAL_ACCESS_TOKEN": "github_pat"},
    "allowed_tools": [],                // DEFAULT-CLOSED
    "added_at": "2026-08-10T02:30:00Z"
  }
]
```

`mcp_secrets.json` maps secret-key-name → value, 0600, local-only.

## CLI (`scripts/mcp_client.py`)

| Command | Does |
|---|---|
| `list-presets` | Catalog of pre-wired servers (below) |
| `add <preset> [--name N] [--arg k=v]` | Consent prompt → secret prompts (getpass) → write config |
| `add-custom <name> (--url U [--bearer] \| --command "...")` | Any MCP server |
| `remove <name>` | Unregister (secrets kept unless `--purge-secrets`) |
| `list` | Configured servers + allowlist state |
| `tools <name>` | Live `tools/list` from the server, marked ✅ allowed / 🔒 blocked |
| `allow <name> <tool...> \| --all` | Open tools (owner action) |
| `deny <name> <tool...>` | Close tools |
| `call <name> <tool> ['{json args}']` | Enforced call — blocked tool = hard refuse |
| `status` | Per-server reachability probe |

## Pre-wired presets (the "Claude Connect" catalog)

| Preset | Transport | Needs | Notes |
|---|---|---|---|
| `duck` | http | peer MCP url + bearer | **Duck-to-duck** — consume another duck's 6 tools |
| `github` | stdio npx | `GITHUB_PERSONAL_ACCESS_TOKEN` | repos, PRs, issues |
| `filesystem` | stdio npx | `--arg dir=/path` | Lane A only — local files |
| `git` | stdio uvx | `--arg repo=/path` | local repo ops |
| `playwright` | stdio npx | — | real browser automation |
| `stripe` | stdio npx | `STRIPE_SECRET_KEY` | payments, customers |
| `postgres` | stdio npx | `POSTGRES_URL` (as secret) | read-mostly SQL |
| `sqlite` | stdio uvx | `--arg db=/path.db` | local DB |
| `gdrive` | stdio npx | Google OAuth (server-managed) | Drive files |
| `notion` | stdio npx | `NOTION_TOKEN` | pages, databases |
| `airtable` | stdio npx | `AIRTABLE_API_KEY` | bases, records |
| `slack` | stdio npx | `SLACK_BOT_TOKEN` (+team id arg) | channels, messages |
| `brave-search` | stdio npx | `BRAVE_API_KEY` | web search |
| `exa` | stdio npx | `EXA_API_KEY` | semantic web search |
| `fetch` | stdio uvx | — | web page fetch/convert |
| `memory` | stdio npx | — | persistent KG scratch space |
| `sentry` | http | bearer (OAuth token) | error monitoring (remote) |
| `cloudflare-docs` | http | — | Cloudflare docs (remote, no auth) |
| `aws-docs` | stdio uvx | — | AWS documentation |
| `zapier` | http | personal url (+bearer) from zapier.com/mcp | 9,000+ apps incl. Gmail/Calendar/Sheets |
| `hubspot` | stdio npx | `PRIVATE_APP_ACCESS_TOKEN` | CRM: contacts, deals, tickets |
| `supabase` | stdio npx | `SUPABASE_ACCESS_TOKEN` | projects, tables, SQL |
| `shopify-dev` | stdio npx | — | Shopify dev docs + Admin schema |
| `google-calendar` | stdio npx | OAuth creds JSON path | events, availability |
| `snowflake` | stdio uvx | account/user/password + `--arg config=…` | Cortex + SQL |

Wave 2 [MCPC-081] package names verified on npm/PyPI 2026-08-10.

Gmail/Google Workspace: no official first-party MCP server yet — use
`add-custom` with a bridge (e.g. Composio/Pipedream URL) when the owner has
one. Documented, not pre-wired.

## Duck-to-duck flow (zero new infra)

Peer duck (Lane B): url `https://beak.spaceduckling.com/beak/duck/mcp`,
bearer = that duck's token. Peer duck (Lane A): the peer's owner exposes
their local `mcp_server.py` via their own tunnel and hands over url+bearer.
Then: `add duck --name sam --arg url=... ` → `allow sam duck_status
send_peck` → the duck can call Sam's tools. Pecks become tool calls.

## Security posture

- Consent at add-time (interactive y/N, or `SPACEDUCK_MCP_CONSENT=yes` env
  for scripted setups — owner-run only).
- Allowlist enforced at `call` time in code, not by convention.
- Secrets via getpass → 0600 file; injected into stdio child env or HTTP
  Authorization header at call time only; never logged, never on argv.
- stdio children get a **minimal env** (PATH/HOME + declared secrets), not
  the full duck environment — the duck's beak_key is NOT visible to
  third-party MCP servers.
- 30s default timeout per call; 1MB response cap; output truncated to 64KB.

## Non-goals (v1)

- No SSE streaming sessions (single-response only, matching our server).
- No OAuth dance handling — remote servers needing OAuth take a pre-issued
  bearer via `--bearer`.
- No automatic tool → brain wiring; the duck's brain calls
  `mcp_client.py call ...` like any other script (OpenClaw exec path).
