---
name: account-research
description: Deep research on one target company before outreach, covering company facts, key people, and recent posts. Use when the user wants to research an account, prepare for a call, or "get up to speed" on a single target company.
---

# Account research with Veezee

Build a briefing on one target account before outreach: what the company is, who matters there, and what they have been posting about. LinkedIn only; this skill covers no other platform. Veezee returns no emails or phone numbers; if the user needs contact details, tell them plainly that this skill cannot provide them.

## Setup (one free key, no signup)

Every call needs an API key. Minting one is free and human-free: no signup, no card. A call without a key fails with `KEY_REQUIRED` (401) carrying `mint_url`; the fix is the free mint below, never a payment. A fresh `vz_trial_` key runs under a free per-IP daily budget of 200 credits, cached data only, first page only on any cursor sequence. Two equivalent surfaces; pick whichever your environment has:

- MCP: add the server `https://mcp.veezee.io/linkedin` (streamable-http; `https://mcp.veezee.io/all` exposes every tool). Hosts that support MCP authorization (Claude Code, claude.ai) open a Veezee sign-in on connect (email code, no password): that is the whole auth step. Other hosts: mint a key with `POST https://api.veezee.io/v1/keys/mint` (empty body; the key is shown once) and put it in the connection's `Authorization: Bearer` header.
- SDK: `import { VeezeeClient } from "@veezee/sdk"`; `const client = new VeezeeClient(); await client.mint();` mints and stores the free key the first time and reuses it on later runs. Platform methods live on the namespace (`client.linkedin.getProfile/searchPeople/getCompany/getPosts`); `client.resolveUrl` and `client.getUsage` are top-level. The client sends retries and Idempotency-Keys for you. The `veezee` CLI (`npx @veezee/sdk init`) mints and stores the same key.

A full account briefing (company, posts, several people) spends more than the free daily budget, so this workflow needs purchased credits. When the budget or a trial cap runs out (`TRIAL_CAP_EXCEEDED`, `INSUFFICIENT_CREDITS`, `BUDGET_EXHAUSTED`), the error carries `upgrade_url` (https://veezee.io/upgrade) and a machine-readable `offer`; hand that link to your human, and purchases credit the same key directly, nothing to reconfigure.

## The workflow, per account

1. Check the budget first: `get_usage` is free, exempt from the rate limit, and works the same on a trial or paid key.
2. Classify the company identifier. Clean LinkedIn company URL, slug, or website domain: go straight to step 3. Dirty or ambiguous URL: `resolve_url` first. Only an approximate name: use `search_people` with a `current_company` filter to resolve it, or ask the user for the URL or domain.
3. `get_company` for the company facts: industry, employee count, headquarters, website, founding year, description, specialities. A domain identifier quotes base price plus a resolution surcharge (set `max_credits` accordingly); known domains settle at the base price.
4. `get_posts` on the company (URL, slug, or website domain all work) for what the company has recently said publicly. One page is one call; follow the `cursor` for older posts only if the user wants more history than the first page covers.
5. Find the key people the user cares about (e.g. the champion, the economic buyer): `search_people` with `current_company` set to this company and `title` or `keywords` narrowing the role. Drop any result marked `is_anonymous: true`; it cannot be fetched further.
6. For each key person worth a closer look, `get_profile` with `sections: ["experience"]` (overview plus the first two sections are included in the base price), and optionally `get_posts` on that person to see what they post about individually.

## Rules that save credits and errors

- Never call `get_profile` on an `is_anonymous: true` search result; it cannot be dereferenced.
- Default freshness is cached (usually a few hours old) and free. Use `freshness: "realtime"` only when the user needs today's data before a call happening soon; it costs extra and needs a paid key (trial keys are cached-only and reject realtime with TRIAL_CAP_EXCEEDED).
- Set `max_credits` on each call so a single account never silently blows the budget.
- Veezee has no contact-detail lookup (no email, no phone) and no way to monitor an account over time; each run is a point-in-time snapshot. Say so if the user expects ongoing alerts.
- On KEY_REQUIRED, mint the free key and retry the same call; it is never a payment problem. On TRIAL_CAP_EXCEEDED, INSUFFICIENT_CREDITS, or BUDGET_EXHAUSTED, stop and give the error's `upgrade_url` to your human; purchases credit the account directly and the same key keeps working afterward.
- A 403 NOT_ENTITLED means the key's account is not enabled for this platform; grants are explicit, write to hello@veezee.io to enable more.

## Output

A one-account briefing: company facts (industry, size, headquarters, website), what the company has recently posted about, and a short list of key people with their current title and recent experience. Include total credits spent (sum the `usage.credits_charged` fields).
