---
name: outreach-list-builder
description: Turn a role or ICP spec into a ranked outbound sales list of LinkedIn prospects, each enriched with company context and a one-line personalized opener rationale. Use whenever the user wants prospects, leads, a target-account list, people to sell to, or personalized outreach angles, even if they only describe the buyer ("find me VPs of Sales at fintech startups") without saying "list" or "outreach". For a hiring shortlist use candidate-sourcing instead; for enriching prospects the user already has, use prospect-enrich.
---

# Outreach list building with Veezee

Turn an ICP or role spec into a ranked outbound list: who to contact, why they fit, and what to open with. LinkedIn only; this skill covers no other platform. Veezee returns LinkedIn profile data, never email addresses or phone numbers; if the user expects contact-info extraction, tell them plainly that this skill cannot provide it, same as every other Veezee skill.

This is the sales-outbound counterpart to candidate-sourcing (which builds a hiring shortlist instead of a prospect list); it reuses that skill's search and pagination discipline. Use candidate-sourcing instead if the goal is recruiting, not selling.

## Setup (one free key, no signup)

Every call needs an API key. Minting one is free and human-free: no signup, no card. A call without a key fails with `KEY_REQUIRED` (401) carrying `mint_url`; the fix is the free mint below, never a payment. Two equivalent surfaces; pick whichever your environment has:

- MCP: add the server `https://mcp.veezee.io/linkedin` (streamable-http; `https://mcp.veezee.io/all` exposes every tool). Hosts that support MCP authorization (Claude Code, claude.ai) open a Veezee sign-in on connect (email code, no password): that is the whole auth step. Other hosts: mint a key with `POST https://api.veezee.io/v1/keys/mint` (empty body; the key is shown once) and put it in the connection's `Authorization: Bearer` header.
- SDK: `import { VeezeeClient } from "@veezee/sdk"`; `const client = new VeezeeClient(); await client.mint();` mints and stores the free key the first time and reuses it on later runs. Platform methods live on the namespace (`client.linkedin.getProfile/searchPeople/getCompany/getPosts`); `client.resolveUrl` and `client.getUsage` are top-level. The client sends retries and Idempotency-Keys for you. The `veezee` CLI (`npx @veezee/sdk init`) mints and stores the same key.

A fresh `vz_trial_` key runs under a free per-IP daily budget of 200 credits, cached data only, search capped at 10 results per call, first page only on any cursor sequence. That covers a handful of prospects at most; a list built at real volume, with enrichment and company context per prospect, needs purchased credits. When the budget or a trial cap runs out (`TRIAL_CAP_EXCEEDED`, `INSUFFICIENT_CREDITS`, `BUDGET_EXHAUSTED`), the error carries `upgrade_url` and a machine-readable `offer`: hand that link to your human; purchases credit the same key directly, nothing to reconfigure.

## The workflow

1. Check the budget first: `get_usage` is free, exempt from the rate limit, and works the same on a trial or paid key. Enrichment and company lookups add up fast, so do not start a list you cannot afford to finish.
2. Turn the ICP into `search_people` filters: `keywords` (free text), plus `title`, `current_company`, `past_company`, `school` as the spec supplies them.
3. Pick a `limit` once and prefer it over paginating: a single call at a larger limit is cheaper than several smaller pages. Trial keys cap search at 10 results per call; the larger limits (up to 30) need a paid key. A `current_company` name is matched by LinkedIn natively (fuzzy, typo-tolerant) and works at any limit; a `past_company` NAME or a company URL is resolved server-side and caps the limit, so keep the limit modest with those or pass the company's numeric id or URN (from `get_company`). Ids and URNs also filter exactly, where names are fuzzy.
4. Review the returned prospects and drop any result marked `is_anonymous: true`; it is a private profile that cannot be enriched further. Keep it in the list as "match found, profile private" if the user wants a full count of the ICP's size.
5. Enrich each prospect worth pursuing with `get_profile`. Choose `sections` deliberately: the first two requested sections are included in the base price, so `["experience"]` or `["experience", "about"]` costs nothing extra, while a third or fourth section adds 2 credits each, and on a long list that surcharge multiplies fast.
6. Add company context with `get_company`, using the prospect's current company (by slug, URL, or website domain if the ICP or profile gives you one). This is what turns "VP Sales at a company" into a specific firmographic hook (industry, size, what they do).
7. Pull personalization hooks with `get_posts` on the prospect (what they post about individually) and, when useful, on their company (what the company has said publicly). One page per call; a single page is usually enough to spot a recent topic worth referencing.
8. Write a one-line opener rationale per prospect from what steps 5-7 turned up: a specific post topic, a role change, a company fact. Never invent a hook you did not actually see in the returned data.

## Rules that save credits and errors

- Never call `get_profile` on an `is_anonymous: true` search result; it cannot be dereferenced. Treat it as a confirmed match and move on.
- Set `max_credits` on each call in a large batch; a call whose quote exceeds it is rejected with nothing charged, so you can keep going instead of overspending.
- Default freshness is cached (usually a few hours old) and free. `freshness: "realtime"` costs extra and needs a paid key (trial keys are cached-only and reject realtime with TRIAL_CAP_EXCEEDED); reach for it only when the user needs today's data on a specific prospect.
- A domain identifier on `get_company` quotes base price plus a resolution surcharge (set `max_credits` accordingly); known domains settle at the base price at settlement.
- On KEY_REQUIRED, mint the free key and retry the same call; it is never a payment problem. On TRIAL_CAP_EXCEEDED, INSUFFICIENT_CREDITS, or BUDGET_EXHAUSTED, stop the batch and hand the error's `upgrade_url` to your human; purchases credit the account directly and the same key keeps working afterward. On RATE_LIMITED (429), wait `retry_after_seconds` and continue; it clears on its own and payment only raises the limit.
- A 403 NOT_ENTITLED means the key's account is not enabled for this platform; grants are explicit, write to hello@veezee.io to enable more.
- Veezee has no contact-detail lookup (no email, no phone) and no way to send outreach; it returns LinkedIn profile data only. Do not imply the list includes a way to reach anyone directly, or that Veezee sends anything on the user's behalf.

## Output

A ranked list the human can work top to bottom. Use this shape per prospect:

```
<rank>. <Name> - <current title>, <current company>
   Company: <one-line firmographic note from get_company: industry, size, what they do>
   Opener: <one line grounded in something the prospect or their company actually posted or did>
```

Close with: prospects skipped as private (`is_anonymous: true`, counted but not enriched), and total credits spent (sum the `usage.credits_charged` fields) so the human can budget the next list. The opener line must trace to returned data; if steps 5-7 surfaced nothing personal, say "no recent hook found" rather than inventing one.
