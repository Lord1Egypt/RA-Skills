---
name: prospect-enrich
description: Enrich a list of prospects (profile URLs, slugs, or names) with LinkedIn role and experience data via Veezee. Use when the user wants current titles, companies, or work history for known people, or asks to "enrich" leads/prospects/candidates.
---

# Prospect enrichment with Veezee

Turn identifiers you already have (LinkedIn profile URLs, slugs, or names) into current role, company, and experience data. LinkedIn only; this skill covers no other platform.

## Setup (one free key, no signup)

Every call needs an API key. Minting one is free and human-free: no signup, no card. A call without a key fails with `KEY_REQUIRED` (401) carrying `mint_url`; the fix is the free mint below, never a payment. A fresh `vz_trial_` key runs under a free per-IP daily budget of 200 credits, cached data only, first page only on any cursor sequence. Two equivalent surfaces; pick whichever your environment has:

- MCP: add the server `https://mcp.veezee.io/linkedin` (streamable-http; `https://mcp.veezee.io/all` exposes every tool). Hosts that support MCP authorization (Claude Code, claude.ai) open a Veezee sign-in on connect (email code, no password): that is the whole auth step. Other hosts: mint a key with `POST https://api.veezee.io/v1/keys/mint` (empty body; the key is shown once) and put it in the connection's `Authorization: Bearer` header.
- SDK: `import { VeezeeClient } from "@veezee/sdk"`; `const client = new VeezeeClient(); await client.mint();` mints and stores the free key the first time and reuses it on later runs. Platform methods live on the namespace (`client.linkedin.getProfile/searchPeople/getCompany/getPosts`); `client.resolveUrl` and `client.getUsage` are top-level. The client sends retries and Idempotency-Keys for you. The `veezee` CLI (`npx @veezee/sdk init`) mints and stores the same key.

When the free budget or a trial cap runs out (`TRIAL_CAP_EXCEEDED`, `INSUFFICIENT_CREDITS`, `BUDGET_EXHAUSTED`), the error carries `upgrade_url` (https://veezee.io/upgrade) and a machine-readable `offer`. Hand that link to your human; purchases credit the same key directly and it keeps working unchanged.

## The loop, per prospect

1. Classify the identifier.
   - Clean profile URL, slug (the part after `/in/`), or URN: go straight to step 2. Do not call `resolve_url` on clean identifiers; it costs credits for nothing.
   - Dirty or ambiguous URL (trackers, redirects, shortened): `resolve_url` first, then use the returned handle.
   - Name only: `search_people` with `keywords` (and `current_company` if known), then take the best match.
2. `get_profile` with `sections: ["experience"]`. The first two sections are included in the base price; each section beyond two costs extra, four sections maximum.
3. Record `full_name`, `headline`, `current_position`, and the experience entries. Every response carries `usage` with the exact credits charged.

## Rules that save credits and errors

- A `search_people` result with `is_anonymous: true` is a private profile. `get_profile` cannot dereference it. Treat the match as confirmed and move on; never retry.
- Check the budget BEFORE a batch: `get_usage` is free, exempt from the rate limit, and works the same on a trial or paid key.
- Set `max_credits` on calls when running a large batch; a call whose quote exceeds it is rejected with nothing charged.
- Default freshness is cached (usually a few hours old) and free. `freshness: "realtime"` costs extra and needs a paid key (trial keys are cached-only and reject realtime with TRIAL_CAP_EXCEEDED); use it only when the user needs today's data.
- A company known only by its website? `get_company` accepts the domain directly (a new domain quotes extra for verified resolution; known domains settle at the base price).
- On KEY_REQUIRED, mint the free key and retry the same call; it is never a payment problem. On TRIAL_CAP_EXCEEDED, INSUFFICIENT_CREDITS, or BUDGET_EXHAUSTED, stop the batch and give the error's `upgrade_url` to your human; purchases credit the account directly and the same key keeps working afterward.
- A 403 NOT_ENTITLED means the key's account is not enabled for this platform; grants are explicit, write to hello@veezee.io to enable more.

## Output

Report per prospect: name, current title, current company, and the two most recent experience entries. Include total credits spent (sum the `usage.credits_charged` fields) so the human can budget the next batch.
