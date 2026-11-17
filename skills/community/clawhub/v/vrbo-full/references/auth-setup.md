<!-- generated: DO NOT EDIT BY HAND — produced by apps/web/scripts/export-github-repos.ts from the export script. Edit the config + re-run. -->

# StayingAPI — getting and storing your API key

This guide gets you a StayingAPI key and persists it so it survives across sessions.

## Step 0 — how to store an env var on this system

Figure out the correct way to persist an environment variable on this machine so it is available in every future session (a shell profile, or a config/env file managed by your agent runtime). The variable name is `STAYINGAPI_KEY`.

## Step 1 — get a key

Both key types come from the same place — the dashboard:

1. Create a free account at <https://stayingapi.com/signup> (no credit card).
2. Open <https://stayingapi.com/dashboard/keys> and copy a key.

- **Evaluate with zero friction:** use a **sandbox** key (`stay_test_…`). Sandbox calls return deterministic fixtures and cost **0 credits**. Sandbox keys work **immediately** — you do not need to verify your email first.
- **Live data:** use a live key (`stay_live_…`). Verifying your email is what unlocks live calls and their credits.

> Sandbox fixtures are illustrative, not a mirror of your request — they may echo different dates, occupancy or even a different property than you asked for. Use them to wire up parsing and error handling, then switch to a `stay_live_` key for real data.

The same key works for these skills, the REST API, and the hosted MCP server (`https://mcp.stayingapi.com`).

## Step 2 — store it

```bash
export STAYINGAPI_KEY="stay_live_…"   # or stay_test_… for the sandbox
```

## Step 3 — verify

```bash
curl -s "https://api.stayingapi.com/v1/account" -H "Authorization: Bearer $STAYINGAPI_KEY" | head
```

A `200` with your account envelope means the key works. A missing/invalid key returns `401 authentication_error` (never billed). Full contract: <https://api.stayingapi.com/openapi.json>.
