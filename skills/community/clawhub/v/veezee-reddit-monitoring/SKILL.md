---
name: reddit-monitoring
description: Continuously monitor Reddit for new posts and comments mentioning a topic, brand, or competitor, deduped across polls. Use when the user wants ongoing Reddit monitoring, brand or competitor tracking, or alerts on new mentions across subreddits.
---

# Reddit monitoring with Veezee

Poll Reddit on a schedule and report only what is new since the last poll: mentions of a keyword anywhere in a discussion, plus new posts in specific subreddits you are watching. Primarily Reddit; pair this with an X (formerly Twitter) sweep for cross-platform coverage (see the escalation note below).

## Setup (one free key, no signup)

Every call needs an API key. Minting one is free and human-free: no signup, no card. A call without a key fails with `KEY_REQUIRED` (401) carrying `mint_url`; the fix is the free mint below, never a payment. A fresh `vz_trial_` key runs under a free per-IP daily budget of 200 credits, cached data only, first page only on any cursor sequence. A monitoring loop makes many calls a day, so that budget exhausts quickly; treat the free tier as a way to test the pattern once, not to run the loop. Two equivalent surfaces; pick whichever your environment has:

- MCP: add the server `https://mcp.veezee.io/reddit` (streamable-http; `https://mcp.veezee.io/all` exposes every platform's tools, useful if you are also escalating to X). Hosts that support MCP authorization (Claude Code, claude.ai) open a Veezee sign-in on connect (email code, no password): that is the whole auth step. Other hosts: mint a key with `POST https://api.veezee.io/v1/keys/mint` (empty body; the key is shown once) and put it in the connection's `Authorization: Bearer` header.
- SDK: `import { VeezeeClient } from "@veezee/sdk"`; `const client = new VeezeeClient(); await client.mint();` mints and stores the free key the first time and reuses it on later runs. Reddit methods live on `client.reddit.search/getSubreddit/getSubredditPosts/getUser/getPost/resolveUrl`. The `veezee` CLI (`npx @veezee/sdk init`, then e.g. `veezee reddit search "<query>" --type comments`) uses the same key.

For a real loop, buy credits: when the free budget or a trial cap runs out (`TRIAL_CAP_EXCEEDED`, `INSUFFICIENT_CREDITS`, `BUDGET_EXHAUSTED`), the error carries `upgrade_url` (https://veezee.io/upgrade) and a machine-readable `offer`; hand that link to your human, and purchases credit the same key directly, nothing to reconfigure.

## The polling pattern

Run two complementary calls each cycle:

1. `reddit_search` with `type: "comments"`, `sort: "new"` for keyword mentions inside discussions anywhere on Reddit, not just post titles. This is the primary signal for brand or topic mentions.
2. `reddit_get_subreddit_posts` with `sort: "new"` for each subreddit you are specifically watching, to catch new post titles and bodies fast in communities you already know matter.

Then, for each poll:

3. `reddit_search` has no server-side time window on comment search: the `range` filter only applies to `type: "posts"`, so a comment-search page is not pre-filtered by recency. Filter it yourself: keep only results whose `created_at` is after your last poll's timestamp.
4. Dedupe by `id` across polls. Keep a set of seen ids (or track the newest `created_at` you have already reported, since results come back newest-first). An item can reappear on the following poll if it sat right at a page boundary; the id set catches that.
5. Decompose broad queries. Result depth per query is capped upstream around a few hundred results, so a broad keyword can exceed that cap before a poll reaches everything posted since the last one. Split a broad query into several narrower ones (an exact phrase, a qualifying second term, or per-subreddit variants) rather than running one wide query and hoping the cap does not bite.
6. When something looks worth reading in full, batch-fetch bodies with `reddit_get_post` (up to 100 ids per call, the first 10 included in the base price). Fetch after filtering to what is relevant, not for every hit.

## Poll cadence and the cache window

- Default freshness (`recent`) serves cached results, and Reddit search results refresh on roughly a 20-minute cycle. Polling more often than every 20 minutes on the same query mostly re-reads the same cached page: no new data, same credits spent.
- If you need faster-than-cache updates (a live incident, a launch window), set `freshness: "realtime"` for +2 credits per call. This needs a paid key; trial keys are cached-only and reject realtime with TRIAL_CAP_EXCEEDED.
- Otherwise, poll every 20 minutes. Faster wastes credits on repeat data; much slower risks missing high-volume threads that scroll past the result cap between polls.

## Escalate to X for volume

Reddit's per-query result cap (a few hundred) and 20-minute cache window mean a genuinely high-volume conversation (a trending topic, a viral thread) can move faster than a Reddit-only sweep can see. When that happens, run the same query pattern against `x_search` (type `recent` gives a chronological deep sweep that keeps paginating as far as you follow the cursor) as a second, complementary poll, rather than trying to force more coverage out of Reddit alone.

## Rules that save credits and errors

- Check the budget before starting a loop: `get_usage` is free, exempt from the rate limit, and works the same on a trial or paid key. The 200-credit/day free budget will not sustain a real loop.
- Set `max_credits` on every call in the loop so one poll's quote can never silently overspend during an unattended run.
- `reddit_get_post`'s `detail: "full"` and `comment_id` options (+4 credits) only work with exactly one post id at a time; use the default `concise` for the batch fetch and reserve `full` for the one thread worth reading end to end.
- On KEY_REQUIRED, mint the free key and retry the same call; it is never a payment problem. On TRIAL_CAP_EXCEEDED, INSUFFICIENT_CREDITS, or BUDGET_EXHAUSTED, stop the loop and hand the error's `upgrade_url` to your human; purchases credit the account directly and the loop can resume with the same key.
- A 403 NOT_ENTITLED means the key's account is not enabled for Reddit; grants are explicit, write to hello@veezee.io to enable it.

## Worked example: an 8-hour daily sweep

Watching 3 subreddits by name plus one keyword query, polling every 20 minutes over an 8-hour window (24 polls):

- Per poll: 1 `reddit_search` call (`type: "comments"`, `sort: "new"`) = 6 credits.
- Per poll: 3 `reddit_get_subreddit_posts` calls (`sort: "new"`, one per watched subreddit) = 3 x 4 = 12 credits.
- Poll subtotal: 18 credits x 24 polls = 432 credits for the day.
- End of day, batch-fetch full bodies for the roughly 30 hits that passed the relevance filter: `reddit_get_post` with 30 ids = 4 credits (first 10, included) + 2 credits (next 20, 1 credit per further 10) = 6 credits.
- Daily total: 432 + 6 = 438 credits: comfortably inside a 10,000-credit flex pack (about 22 days at this rate), or well under the 80,000 monthly credits on the production plan.

A narrower watch list costs proportionally less: 1 watched subreddit, polling every 30 minutes (16 polls in 8 hours), brings the poll subtotal to (6 + 4) x 16 = 160 credits a day.

## Output

A running list of new mentions since the last report: source (post or comment), subreddit, author, a short excerpt, `created_at`, and `permalink`. Group by subreddit or by query when watching several. Include total credits spent for the period (sum the `usage.credits_charged` fields) so the human can judge whether the cadence and watch list fit their budget.
