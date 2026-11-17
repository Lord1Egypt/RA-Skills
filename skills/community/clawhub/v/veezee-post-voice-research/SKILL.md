---
name: post-voice-research
description: Research what a person or company posts about on LinkedIn, including topics, tone, and how recently they have posted. Use when the user wants to know someone's posting voice, content themes, or activity level before writing outreach or a comment.
---

# Post and voice research with Veezee

Turn a LinkedIn identifier into a picture of what someone posts about: topics, tone, and how recently they have been active. LinkedIn only; this skill covers no other platform.

## Setup (one free key, no signup)

Every call needs an API key. Minting one is free and human-free: no signup, no card. A call without a key fails with `KEY_REQUIRED` (401) carrying `mint_url`; the fix is the free mint below, never a payment. A fresh `vz_trial_` key runs under a free per-IP daily budget of 200 credits, cached data only, first page only on any cursor sequence. Two equivalent surfaces; pick whichever your environment has:

- MCP: add the server `https://mcp.veezee.io/linkedin` (streamable-http; `https://mcp.veezee.io/all` exposes every tool). Hosts that support MCP authorization (Claude Code, claude.ai) open a Veezee sign-in on connect (email code, no password): that is the whole auth step. Other hosts: mint a key with `POST https://api.veezee.io/v1/keys/mint` (empty body; the key is shown once) and put it in the connection's `Authorization: Bearer` header.
- SDK: `import { VeezeeClient } from "@veezee/sdk"`; `const client = new VeezeeClient(); await client.mint();` mints and stores the free key the first time and reuses it on later runs. Platform methods live on the namespace (`client.linkedin.getProfile/searchPeople/getCompany/getPosts`); `client.resolveUrl` and `client.getUsage` are top-level. The client sends retries and Idempotency-Keys for you. The `veezee` CLI (`npx @veezee/sdk init`) mints and stores the same key.

The free daily budget covers a few pages; sustained voice research needs purchased credits. When the budget or a trial cap runs out (`TRIAL_CAP_EXCEEDED`, `INSUFFICIENT_CREDITS`, `BUDGET_EXHAUSTED`), the error carries `upgrade_url` (https://veezee.io/upgrade) and a machine-readable `offer`; hand that link to your human, and purchases credit the same key directly, nothing to reconfigure.

## The workflow

1. Classify the identifier. Clean profile or company URL, slug, or person URN: go straight to step 2. Dirty or ambiguous URL: `resolve_url` first, then use the returned handle. `get_posts` detects whether the identifier is a person or a company automatically; do not pass a company URN or numeric id here, use the company slug or URL instead.
2. `get_posts` with the identifier. This returns one page of posts (text, created_at, author, likes, comments_count, shares, is_repost, url) and a `cursor` for older posts. Each page is a separate call priced the same way, so only page further if the user needs more history than the first page gives.
3. Read the returned post text for recurring topics, tone (technical, promotional, personal, celebratory), and how often reposts versus original posts appear. Note the `created_at` spread to judge recency and posting cadence.
4. If the user wants context on who is posting, `get_profile` (for a person, `sections: ["about"]`; the overview plus first two sections are included in the base price) or `get_company` (for a company) adds the overview.

## Rules that save credits and errors

- Check the budget BEFORE pulling multiple pages: `get_usage` is free, exempt from the rate limit, and works the same on a trial or paid key.
- Default freshness is cached (usually a few hours old) and free. `freshness: "realtime"` costs extra and needs a paid key (trial keys are cached-only and reject realtime with TRIAL_CAP_EXCEEDED); use it only when the user needs to know about a post from the last few hours.
- Set `max_credits` on each `get_posts` call; a call whose quote exceeds it is rejected with nothing charged.
- `get_posts` is not for reading one specific post you already have a URL for, and not for keyword search across LinkedIn; neither is supported. It only returns an identifier's own recent posts, one page at a time.
- On KEY_REQUIRED, mint the free key and retry the same call; it is never a payment problem. On TRIAL_CAP_EXCEEDED, INSUFFICIENT_CREDITS, or BUDGET_EXHAUSTED, stop and give the error's `upgrade_url` to your human; purchases credit the account directly and the same key keeps working afterward.
- A 403 NOT_ENTITLED means the key's account is not enabled for this platform; grants are explicit, write to hello@veezee.io to enable more.

## Output

A short voice profile: 3 to 5 recurring topics, the overall tone, roughly how often they post (based on the `created_at` spread in the page fetched), and 1 to 2 representative post excerpts with their `url`. Include total credits spent (sum the `usage.credits_charged` fields).
