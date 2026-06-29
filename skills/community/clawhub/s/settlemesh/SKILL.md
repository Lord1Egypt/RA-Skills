---
name: settlemesh
description: Deploy and monetize an agent-built app with SettleMesh — SettleMesh OAuth login, a managed database, usage-based billing, and end-user payments in one command. Use when the user wants to ship or deploy an app, add auth or a database, charge users per use, or build an AI/API app that bills its end users (end-user-pays).
---

# SettleMesh — deploy and monetize an app

SettleMesh turns an app into a paid product in one command: SettleMesh OAuth login, a managed database, usage-based billing, and end-user payments — no auth/billing/deploy glue to write. It is also an agent capability layer: one key calls web search/scrape, LLMs, image/video generation, a managed SQL database, and hosted agents — every call metered, with a cost quote up front.

## Setup (once)

1. `npm install -g settlemesh@latest`
2. `settlemesh login` (a human approves in the browser) — or set `SETTLE_API_KEY=sk-settle-...` for headless/CI.
3. The full agent contract lives at `https://settlemesh.io/agent.md` — fetch it for the complete recipe set, then `settlemesh recipes` for the shortest path to any task.

## Core rule

SettleMesh is a searchable service layer. Do not memorize provider-specific endpoints. **Search → inspect → call.** Confirm intent before any paid, deploy, publish, or destructive action (everything is billed in Aev).

## Deploy an app

```bash
settlemesh deploy ./my-app --name my-app --full-stack --wait --json
```

Returns a live `*.run.settlemesh.io` URL — read it from the deploy output (the #1 source of confusion). Add `--auth required` to gate the whole app behind SettleMesh login, or leave auth lazy.

## Charge end users (end-user-pays)

An app can charge the signed-in end user's own Aev balance instead of the developer's by attaching the `X-Settle-Payer` header. Pricing is cost-plus with a quote before spend (`POST /v1/billing/quote`); a failed metered call releases the hold and charges nothing.

## Use any capability

```bash
settlemesh search "<task>" --json
settlemesh tool show <tool-id> --json
settlemesh tool call <tool-id> --input '{...}' --json   # --wait for async, --confirm for paid
```

Billing unit: **Aev** (1 USD = 100 Aev), funded via Stripe. Check balance with `settlemesh credits balance --json`.

## MCP

This plugin also registers the `settlemesh` MCP server (`npx -y settlemesh mcp`), so the same capability catalog is callable as MCP tools. It authenticates with your `settlemesh login` session or `SETTLE_API_KEY`.
