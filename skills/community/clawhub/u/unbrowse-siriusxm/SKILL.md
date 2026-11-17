---
name: siriusxm
description: "Siriusxm (siriusxm.com) for agents: Search SiriusXM; Open a channel page; Read a page on siriusxm.com — through Unbrowse's scoped MCP for siriusxm.com (unofficial), which replays siriusxm.com's own first-party API (no browser, verified results). Use when the user wants anything from siriusxm.com, e.g. search siriusxm."
---

# Unbrowse for Siriusxm (siriusxm.com)

Siriusxm as tools for your agent. Unofficial: not affiliated with or endorsed by siriusxm.com. Unbrowse compiled these from siriusxm.com's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no siriusxm.com API key.

## Connect the siriusxm.com MCP

This server is a tool scope holding only siriusxm.com: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on siriusxm.com.

```sh
claude mcp add --transport http siriusxm https://unbrowse.ai/mcp/siriusxm.com
codex mcp add siriusxm --url https://unbrowse.ai/mcp/siriusxm.com && codex mcp login siriusxm
```

```json
{"mcpServers":{"siriusxm":{"url":"https://unbrowse.ai/mcp/siriusxm.com"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch siriusxm.com some other way and present it as this skill's result.

## Tools

### `siriusxm_com__get_search` — Search SiriusXM

Search SiriusXM. Inputs: query. Returns hits, nbHits, page, nbPages, hitsPerPage, exhaustiveNbHits, exhaustiveTypo, exhaustive. Read-only on siriusxm.com.

- `query` (string, required) — query (typed during “fill Search SiriusXM”)
- `hitsPerPage` (integer) — optional, e.g. "20"

```json
{"query":"<query>"}
```

### `siriusxm_com__get_mountain_purejazz` — Open a channel page

Open a channel page. Inputs: channel. Returns utcExpireTime, channels. Read-only on siriusxm.com.

- `channel` (string, required)

```json
{"channel":"<channel>"}
```

### `siriusxm_com__read_page` — Read a page on siriusxm.com

Read any page on siriusxm.com — a path such as /news/2026/some-story, or a full siriusxm.com URL — and get its title, readable text and links. One first-party HTTP request, no browser. Follow a returned link by passing its href back as the path. Inputs: path e.g. "/". Returns the page's title, readable text and links. Read-only on siriusxm.com.

- `path` (string, required) — A page on siriusxm.com: a path like /about, or a full URL on siriusxm.com

```json
{"path":"/"}
```

Always there too: `unbrowse.run` (a task on siriusxm.com in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on siriusxm.com), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on siriusxm.com → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off siriusxm.com is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills siriusxm.com's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/siriusxm.com/call/siriusxm_com__get_search \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"query":"<query>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/siriusxm.com/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
