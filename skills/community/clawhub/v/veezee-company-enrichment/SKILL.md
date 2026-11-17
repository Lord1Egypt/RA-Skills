---
name: company-enrichment
description: Enrich a list of companies (names, domains, or LinkedIn URLs) with firmographic data like industry, employee count, headquarters, and founding year. Use when the user wants to enrich, look up, or research a batch of companies.
---

# Company enrichment with Veezee

Turn identifiers you already have (LinkedIn company URLs, slugs, or website domains) into firmographic data: industry, employee count, headquarters, founding year, and description. LinkedIn only; this skill covers no other platform.

## Setup (one free key, no signup)

Every call needs an API key. Minting one is free and human-free: no signup, no card. A call without a key fails with `KEY_REQUIRED` (401) carrying `mint_url`; the fix is the free mint below, never a payment. A fresh `vz_trial_` key runs under a free per-IP daily budget of 200 credits, cached data only, first page only on any cursor sequence. Two equivalent surfaces; pick whichever your environment has:

- MCP: add the server `https://mcp.veezee.io/linkedin` (streamable-http; `https://mcp.veezee.io/all` exposes every tool). Hosts that support MCP authorization (Claude Code, claude.ai) open a Veezee sign-in on connect (email code, no password): that is the whole auth step. Other hosts: mint a key with `POST https://api.veezee.io/v1/keys/mint` (empty body; the key is shown once) and put it in the connection's `Authorization: Bearer` header.
- SDK: `import { VeezeeClient } from "@veezee/sdk"`; `const client = new VeezeeClient(); await client.mint();` mints and stores the free key the first time and reuses it on later runs. Platform methods live on the namespace (`client.linkedin.getProfile/searchPeople/getCompany/getPosts`); `client.resolveUrl` and `client.getUsage` are top-level. The client sends retries and Idempotency-Keys for you. The `veezee` CLI (`npx @veezee/sdk init`) mints and stores the same key.

The free daily budget covers only a handful of companies, so a real batch needs purchased credits. When the budget or a trial cap runs out (`TRIAL_CAP_EXCEEDED`, `INSUFFICIENT_CREDITS`, `BUDGET_EXHAUSTED`), the error carries `upgrade_url` (https://veezee.io/upgrade) and a machine-readable `offer`; hand that link to your human, and purchases credit the same key directly, nothing to reconfigure.

## The loop, per company

1. Classify the identifier.
   - Clean LinkedIn company URL or slug (the part after `/company/`): go straight to step 2.
   - Website domain (e.g. `acme.com`): also go straight to step 2; `get_company` accepts a domain directly.
   - Dirty or ambiguous LinkedIn URL (trackers, redirects, shortened): `resolve_url` first, then use the returned handle.
   - Only an approximate company name, no URL or domain: `get_company` does not search by name, so ask the user for the company's website domain (the most reliable identifier) or LinkedIn URL. `search_people` with a `current_company` filter matches company names natively (fuzzy, typo-tolerant), but it needs `keywords` too and returns people, not the company record.
2. `get_company` with the identifier. A domain identifier quotes base price plus a resolution surcharge (set `max_credits` accordingly); once a domain has been resolved before, that surcharge is refunded at settlement, so known domains settle at the base price. A domain that cannot be verified to a company returns `INVALID_INPUT` with the closest matches instead of a guessed company.
3. Record name, description, industry, employee count, headquarters, website, founding year, and specialities. Every response carries `usage` with the exact credits charged.

## Rules that save credits and errors

- Check the budget BEFORE a batch: `get_usage` is free, exempt from the rate limit, and works the same on a trial or paid key. Do not discover an empty balance mid-run.
- Set `max_credits` on calls when running a large batch; a call whose quote exceeds it is rejected with nothing charged.
- Default freshness is cached (usually a few hours old) and free. `freshness: "realtime"` costs extra and needs a paid key (trial keys are cached-only and reject realtime with TRIAL_CAP_EXCEEDED); use it only when the user needs today's data.
- Do not pass a numeric company id or URN to `get_company`; those are `search_people` filter inputs, not fetch identifiers. Use the slug, URL, or domain.
- For a company's recent posts, use `get_posts` with the same identifier (URL, slug, or website domain all work there too).
- On KEY_REQUIRED, mint the free key and retry the same call; it is never a payment problem. On TRIAL_CAP_EXCEEDED, INSUFFICIENT_CREDITS, or BUDGET_EXHAUSTED, stop the batch and give the error's `upgrade_url` to your human; purchases credit the account directly and you continue afterward with the same key.
- A 403 NOT_ENTITLED means the key's account is not enabled for this platform; grants are explicit, write to hello@veezee.io to enable more.

## Output

Report per company: name, industry, employee count, headquarters, website, and founding year. Flag any identifier that returned `INVALID_INPUT` along with the closest matches Veezee suggested. Include total credits spent (sum the `usage.credits_charged` fields) so the human can budget the next batch.
