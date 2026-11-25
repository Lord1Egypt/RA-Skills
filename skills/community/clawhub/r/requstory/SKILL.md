---
name: requstory
description: Map how a company works from its public website (customer journey, teams, processes, handoffs), find the gaps that make it hard to buy from or work with, ask questions about the map, and check public ease-of-doing-business scores and AI-agent readiness. Use when the user asks how a company operates, who owns what, where a business loses customers, how easy a company is to deal with, or whether AI agents can use a website.
homepage: https://requstory.com/developers/api/
metadata: {"openclaw":{"primaryEnv":"REQUSTORY_API_KEY","requires":{"env":["REQUSTORY_API_KEY"]}}}
---

# Requstory

Requstory reads a company's public website and drafts its operating model: the customer journey, teams in three bands, processes and handoffs. It scores how easy the company is to do business with and lists the gaps, each with proof.

Base URL: `https://requstory.com/api/public/v1`. JSON in and out. Errors are `{"error": {"code", "message"}}`.

## Setup

1. Sign up free with Google at https://requstory.com/?ref=clawhub
2. Open Profile → API keys → Create key. The key starts with `rqs_` and is shown once.
3. Set `REQUSTORY_API_KEY` to the key. Send it as `Authorization: Bearer $REQUSTORY_API_KEY`.

Public endpoints (companies, scores, AI readiness) also work without a key.

## Which call to use

- Known company, want its score and gaps: `GET /companies?q=<name>` → take `slug` → `GET /companies/{slug}`.
- Any website, quick check of AI-agent readiness: `POST /ai-readiness {"website"}`, then `GET /ai-readiness/{domain}` until `status` is `done`.
- Any website, full map (key): `POST /maps {"website"}` → poll `GET /maps/jobs/{jobId}` every ~5 s until `status` is `complete` → `GET /maps/{mapId}`.
- Question about a saved map (key): `POST /maps/{mapId}/ask {"question"}`. Free answers cite website pages. Add `"ai": true` only if the user agrees to use credits.
- List saved maps: `GET /maps`. Account and limits: `GET /account`.

## Examples

```sh
curl "https://requstory.com/api/public/v1/companies?q=posthog"
curl https://requstory.com/api/public/v1/companies/posthog-com

curl -X POST https://requstory.com/api/public/v1/maps \
  -H "Authorization: Bearer $REQUSTORY_API_KEY" -H "Content-Type: application/json" \
  -d '{"website":"example.com"}'
curl https://requstory.com/api/public/v1/maps/jobs/<jobId> -H "Authorization: Bearer $REQUSTORY_API_KEY"
curl https://requstory.com/api/public/v1/maps/<mapId> -H "Authorization: Bearer $REQUSTORY_API_KEY"
```

## Reading results

- `GET /companies/{slug}`: `score.total` (0–100), `score.parts` (find and understand, get started online, get help, AI-agent ready), `gaps` sorted by `cost` (points lost) with `proof`.
- `GET /maps/{mapId}`: `journey`, `teams` (owner, processes), `missingOwners`, `peerChecks` (things most peers show that this site does not), `agentReady` gaps, `fixes`, `url` to open the map in the app.
- Never invent owners, numbers or teams. Report what the map says and link `url` so the user can check.

## Limits

10 calls a minute without a key, 60 with one. 5 new maps a day per account. 3 new AI-readiness checks an hour. On `429`, wait and retry later.

## Also available

- MCP server: `https://requstory.com/mcp` (same tools)
- CLI: `npx requstory --help`
- OpenAPI: https://requstory.com/api/public/v1/openapi.json
