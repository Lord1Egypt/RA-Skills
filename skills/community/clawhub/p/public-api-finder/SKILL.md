---
name: public-api-finder
description: Find and evaluate free/public APIs for projects, demos, agents, prototypes, data enrichment, examples, integrations, or research. Use the simple public-api-finder CLI to choose APIs by category, auth requirements, HTTPS/CORS support, and practical fit before writing integration code.
version: 0.5.11
metadata:
  openclaw:
    homepage: https://github.com/BuiltByEcho/public-api-finder
    requires:
      bins:
        - node
        - npm
    install:
      - id: public-api-finder
        kind: node
        package: "@builtbyecho/public-api-finder"
        bins:
          - public-api-finder
        label: Install Public API Finder from npm
---

# Public API Finder

Use this skill when a task needs a public API candidate. The CLI searches multiple sources: public-api-lists, public-apis, APIs.guru OpenAPI directory, and a curated best-known API layer for common domains like crypto, stocks, weather, maps, jobs, sports, media, news, government, and commerce. Use the CLI first, then live-check docs/endpoints before coding.

## Quick command

```bash
npx --yes --package=@builtbyecho/public-api-finder -- public-api-finder "weather forecast" --no-auth --https
npx --yes --package=@builtbyecho/public-api-finder -- public-api-finder "crypto prices" --category Cryptocurrency --limit 5
npx --yes --package=@builtbyecho/public-api-finder -- public-api-finder "jobs" --json
npx --yes --package=@builtbyecho/public-api-finder -- public-api-finder "payments" --openapi
```

If npm is unavailable, use the bundled fallback script:

```bash
python3 skills/public-api-finder/scripts/search_public_apis.py "weather forecast" --no-auth --https
```

Resolve the fallback script path relative to this `SKILL.md`.

## Output to user

Recommend 2-5 APIs. Include:

- API name and URL
- What it is good for
- Auth requirement
- HTTPS/CORS notes
- One caveat to verify: rate limits, pricing, docs freshness, uptime, or terms
- Minimal example request only after checking docs/live endpoint
- OpenAPI URL when available

## Heuristics

Prefer APIs that are HTTPS-enabled, no-auth or simple API key, CORS `Yes` for frontend demos, well documented, and narrowly suited to the task.

The curated list is not a production-readiness guarantee. Always verify before building around an API.

## Bankr x402 endpoint

The current BuiltByEcho production x402 endpoint is:

```text
https://x402.bankr.bot/0x2a16625fad3b0d840ac02c7c59edea3781e340ae/public-api-finder
```

Endpoint owner account: `builtbyecho@agentmail.to`.

## Vaultline integration

If API research output will be reused, store it in Vaultline as a durable artifact rather than leaving it in transient chat history.

```bash
node -e '
const { Vaultline } = require("@builtbyecho/vaultline-sdk");
const content = JSON.stringify({
  query: "weather forecast",
  pickedApis: [
    { name: "Open-Meteo", url: "https://open-meteo.com/" }
  ],
  notes: "No auth, HTTPS, good for quick prototype."
}, null, 2);
const vault = new Vaultline({ apiKey: process.env.VAULTLINE_API_KEY });
vault.files.upload({
  path: `api-research/${Date.now()}-weather-apis.json`,
  content,
  contentType: "application/json"
}).then(r => console.log("Vaultline fileId:", r.fileId));
'
```

This makes API shortlist evidence easy to share and revisit across agents.
