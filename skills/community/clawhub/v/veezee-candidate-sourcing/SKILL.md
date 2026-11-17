---
name: candidate-sourcing
description: Find LinkedIn candidates matching a role spec, shortlist them, and enrich the shortlist with current role and experience. Use when the user wants to source, find, or search for candidates, talent, or people matching criteria like title, school, or current/past employer (e.g. "engineers at Shopify who used to work at Amazon").
---

# Candidate sourcing with Veezee

Turn a role spec (title, company, school, or keywords) into a ranked shortlist with enriched profiles. LinkedIn only; this skill covers no other platform. Veezee returns no emails or phone numbers; if the user needs contact details, tell them plainly that this skill cannot provide them.

## Setup (one free key, no signup)

Every call needs an API key. Minting one is free and human-free: no signup, no card. A call without a key fails with `KEY_REQUIRED` (401) carrying `mint_url`; the fix is the free mint below, never a payment. A fresh `vz_trial_` key runs under a free per-IP daily budget of 200 credits, cached data only, first page only on any cursor sequence. Two equivalent surfaces; pick whichever your environment has:

- MCP: add the server `https://mcp.veezee.io/linkedin` (streamable-http; `https://mcp.veezee.io/all` exposes every tool). Hosts that support MCP authorization (Claude Code, claude.ai) open a Veezee sign-in on connect (email code, no password): that is the whole auth step. Other hosts: mint a key with `POST https://api.veezee.io/v1/keys/mint` (empty body; the key is shown once) and put it in the connection's `Authorization: Bearer` header.
- SDK: `import { VeezeeClient } from "@veezee/sdk"`; `const client = new VeezeeClient(); await client.mint();` mints and stores the free key the first time and reuses it on later runs. Platform methods live on the namespace (`client.linkedin.getProfile/searchPeople/getCompany/getPosts`); `client.resolveUrl` and `client.getUsage` are top-level. The client sends retries and Idempotency-Keys for you. The `veezee` CLI (`npx @veezee/sdk init`) mints and stores the same key.

When the free budget or a trial cap runs out (`TRIAL_CAP_EXCEEDED`, `INSUFFICIENT_CREDITS`, `BUDGET_EXHAUSTED`), the error carries `upgrade_url` (https://veezee.io/upgrade) and a machine-readable `offer`. Hand that link to your human; purchases credit the same key directly and it keeps working unchanged. Note: one search plus a couple of profile fetches makes a real dent in the free daily budget, so sourcing runs at any real volume need purchased credits.

## The workflow

1. Check the budget first: `get_usage` is free, exempt from the rate limit, and works the same on a trial or paid key. Do not start a search you cannot afford to enrich.
2. Turn the role spec into `search_people` filters: `keywords` (free text), plus `title`, `current_company`, `past_company`, `school` as the spec supplies them. "Engineers at Shopify who used to work at Amazon" becomes `title: "engineer"`, `current_company: "Shopify"`, `past_company: "Amazon"`.
3. Pick a `limit` once and prefer it over paginating: a single call at a larger limit is cheaper than several smaller pages. A `current_company` name is matched by LinkedIn natively (fuzzy, typo-tolerant) and works at any limit; a `past_company` NAME or a company URL is resolved server-side and caps the limit, so keep the limit modest with those or pass the company's numeric id or URN (from `get_company`). Ids and URNs also filter exactly, where names are fuzzy.
4. Review the returned candidates: name, position, location, and identifier. Drop any result marked `is_anonymous: true` from the enrichment list; it is a private profile that cannot be fetched further. Keep it in the shortlist as "match found, profile private" if the user wants a count.
5. Shortlist the candidates worth enriching, then call `get_profile` for each with `sections: ["experience"]`. The overview plus the first two sections are included in the base price.
6. If a candidate's identifier is a dirty or shortened URL rather than a clean slug or URN, run `resolve_url` first. Skip it for clean slugs or URNs; it only spends credits for nothing there.

## Rules that save credits and errors

- Never call `get_profile` on an `is_anonymous: true` search result; it cannot be dereferenced. Treat it as a confirmed match and move on.
- Set `max_credits` on each call in a large batch; a call whose quote exceeds it is rejected with nothing charged, so you can keep going instead of overspending.
- Default freshness is cached (usually a few hours old) and free. `freshness: "realtime"` costs extra and needs a paid key (trial keys are cached-only and reject realtime with TRIAL_CAP_EXCEEDED); reach for it only when the user needs today's data.
- On KEY_REQUIRED, mint the free key and retry the same call; it is never a payment problem. On TRIAL_CAP_EXCEEDED, INSUFFICIENT_CREDITS, or BUDGET_EXHAUSTED, stop the batch and hand the error's `upgrade_url` to your human; purchases credit the account directly and the same key keeps working afterward.
- A 403 NOT_ENTITLED means the key's account is not enabled for this platform; grants are explicit, write to hello@veezee.io to enable more.
- Veezee has no contact-detail lookup (no email, no phone). Do not imply the shortlist includes a way to reach anyone directly.

## Output

Report a shortlist ranked by fit: name, current title, current company, and the two most recent experience entries per candidate. Note any candidates skipped because their profile was private. Include total credits spent (sum the `usage.credits_charged` fields) so the human can budget the next search.
