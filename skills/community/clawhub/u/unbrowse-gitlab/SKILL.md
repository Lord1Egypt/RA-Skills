---
name: gitlab
description: "Gitlab (gitlab.com) for agents: View GitLab pricing tiers and plans; Search GitLab explore projects by name; Read a docs.gitlab.com page by name — through Unbrowse's scoped MCP for gitlab.com (unofficial), which replays gitlab.com's own first-party API (no browser, verified results). Use when the user wants anything from gitlab.com, e.g. view gitlab pricing tiers and plans."
---

# Unbrowse for Gitlab (gitlab.com)

Gitlab as tools for your agent. Unofficial: not affiliated with or endorsed by gitlab.com. Unbrowse compiled these from gitlab.com's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no gitlab.com API key.

## Connect the gitlab.com MCP

This server is a tool scope holding only gitlab.com: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on gitlab.com.

```sh
claude mcp add --transport http gitlab https://unbrowse.ai/mcp/gitlab.com
codex mcp add gitlab --url https://unbrowse.ai/mcp/gitlab.com && codex mcp login gitlab
```

```json
{"mcpServers":{"gitlab":{"url":"https://unbrowse.ai/mcp/gitlab.com"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch gitlab.com some other way and present it as this skill's result.

## Tools

### `about_gitlab_com__get_pricing_payload_json` — View GitLab pricing tiers and plans

View GitLab pricing tiers and plans. No inputs. Returns data. Read-only on about.gitlab.com.

- none

```json
{}
```

### `gitlab_com__render_page` — Search GitLab explore projects by name

Search GitLab explore projects by name. Inputs: name. Returns the page's title, readable text and links. Read-only on gitlab.com.

- `name` (string, required) — name — what to search for on gitlab.com

```json
{"name":"<name>"}
```

### `docs_gitlab_com__read_page` — Read a docs.gitlab.com page by name

Read a docs.gitlab.com page by name. Inputs: name. Returns the page's title, readable text and links. Read-only on docs.gitlab.com.

- `name` (string, required)

```json
{"name":"<name>"}
```

Always there too: `unbrowse.run` (a task on gitlab.com in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on gitlab.com), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on gitlab.com → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off gitlab.com is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills gitlab.com's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/about.gitlab.com/call/about_gitlab_com__get_pricing_payload_json \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/about.gitlab.com/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
