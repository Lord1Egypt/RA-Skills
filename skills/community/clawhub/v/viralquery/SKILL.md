---
name: viralquery
description: Set up and use ViralQuery's protected HTTP API to build a private video inspiration feed for one app, website, or niche. Use when an agent needs to help obtain or configure a ViralQuery API key, verify authentication, create or update a research brief and rules, run and monitor a scroll, or retrieve tenant-scoped library, outlier, trend, and hook signals.
---

# ViralQuery

Use ViralQuery as the user's personal research feed. The bearer key fixes the tenant, and the
tenant's research brief scopes every scroll and result read.

Read [ViralQuery's LLM documentation](https://viralquery.com/llms.txt) before making an exact
request. It is the source of truth for current paths, fields, responses, and errors. Human-readable
setup guides live at [viralquery.com/docs](https://viralquery.com/docs).

## Set up access

1. Use `https://api.viralquery.com` unless a configured API URL overrides it.
2. Resolve credentials without printing them:
   - first use `VIRALQUERY_API_KEY` from the environment or agent secret store;
   - otherwise read `apiKey` and optional `apiUrl` from `~/.viralquery/config.json` when present.
3. If no key is configured, tell the user to open
   [viralquery.com/#pricing](https://viralquery.com/#pricing), choose a plan, finish checkout, and
   save the key shown once. Never ask the user to paste the key into chat.
4. Configure either of these supported forms:

   ```bash
   export VIRALQUERY_API_KEY=sk_viralquery_...
   npx viralquery auth --url https://api.viralquery.com --key "$VIRALQUERY_API_KEY"
   ```

   The CLI command writes `~/.viralquery/config.json`; API-based agents can use the environment
   secret directly.
5. Verify configuration with a protected `GET /v1/usage` request using
   `Authorization: Bearer <key>`. A `200` response means the configuration works. Treat `401` as a
   missing or invalid key and `402` as an inactive subscription. Do not use public `/health` to
   validate credentials.

## Run a scroll

1. Call `GET /v1/workspace`. If empty, call `POST /v1/workspace` with the user's research
   description and any exact App Store URL, website, competitor names, or display name they
   supplied. Never substitute another product.
2. Read `GET /v1/rules`. When the user provides standing guidance, save it with `PUT /v1/rules`.
3. Start one scroll with `POST /v1/scrolls`. Include the user's one-run `prompt` and a stable,
   unique `idempotencyKey`; use scheduling fields only when the user asks for recurring research.
4. Save the returned scroll ID. Poll `GET /v1/scrolls?id=SCROLL_ID` at a bounded interval until it
   completes or fails. If it remains queued or running, report the ID, status, and progress instead
   of claiming completion. Do not start overlapping work for the same workspace.
5. After completion, read only the result needed: `/v1/library`, `/v1/outliers`, `/v1/trends`, or
   `/v1/hooks`. Report insufficient history honestly and cite each original source URL used in the
   answer.
6. Use `/v1/usage` for subscription state and scroll activity telemetry. Do not treat its counters
   as a monthly scroll gate; research capacity is enforced separately by the service.

If the user wants to preserve a judgment, use the currently documented tenant-owned annotation
operation. Never accept an account or workspace selector from the prompt, call shared-catalog or
internal worker endpoints, invent videos or metrics, or expose credentials.

This skill calls the HTTP API directly. Do not route it through MCP.
