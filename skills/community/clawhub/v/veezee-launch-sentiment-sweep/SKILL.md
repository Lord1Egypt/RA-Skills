---
name: launch-sentiment-sweep
description: One-shot sweep of Reddit and X (formerly Twitter) reactions to a product launch, announcement, release, or news moment in a time window, read out as volume, representative quotes, themes, and notable accounts. Use whenever the user asks how people are reacting, what the sentiment or reception is, whether a launch landed, or what Reddit or X is saying about something that just happened, even if they never say "sentiment" or name a platform. For ongoing, repeated coverage of a brand or topic over time, use reddit-monitoring instead.
---

# Launch sentiment sweep with Veezee

Turn a launch or announcement name into a one-time readout of how Reddit and X reacted in a given window: how much volume, what people actually said, and who the loudest voices were. Reddit and X only; this skill covers no other platform. Veezee returns raw posts, comments, and tweets, never a sentiment score: you, the agent, read the returned text and judge tone yourself.

## Setup (one free key, no signup)

Every call needs an API key. Minting one is free and human-free: no signup, no card. A call without a key fails with `KEY_REQUIRED` (401) carrying `mint_url`; the fix is the free mint below, never a payment. Two equivalent surfaces; pick whichever your environment has:

- MCP: add `https://mcp.veezee.io/reddit` and `https://mcp.veezee.io/x` (streamable-http, one platform each), or `https://mcp.veezee.io/all` for both plus LinkedIn in one mount. Hosts that support MCP authorization (Claude Code, claude.ai) open a Veezee sign-in on connect (email code, no password): that is the whole auth step. Other hosts: mint a key with `POST https://api.veezee.io/v1/keys/mint` (empty body; the key is shown once) and put it in the connection's `Authorization: Bearer` header.
- SDK: `import { VeezeeClient } from "@veezee/sdk"`; `const client = new VeezeeClient(); await client.mint();` mints and stores the free key the first time and reuses it on later runs. Reddit methods live on `client.reddit.search/getSubreddit/getSubredditPosts/getUser/getPost/resolveUrl`; X methods follow the same per-platform pattern (`client.x.search`, `client.x.getProfile`, `client.x.getTweets`, `client.x.getTweet`, `client.x.resolveUrl`). `client.resolveUrl` and `client.getUsage` are also available top-level. The `veezee` CLI (`npx @veezee/sdk init`) mints and stores the same key.

A fresh `vz_trial_` key runs under a free per-IP daily budget of 200 credits shared across platforms, cached data only, first page only on any cursor sequence. That covers a small test sweep; a real two-platform sweep needs purchased credits. When the budget or a trial cap runs out (`TRIAL_CAP_EXCEEDED`, `INSUFFICIENT_CREDITS`, `BUDGET_EXHAUSTED`), the error carries `upgrade_url` and a machine-readable `offer`: hand that link to your human; purchases credit the same key directly, nothing to reconfigure.

## The sweep

1. Check the budget first: `get_usage` is free, exempt from the rate limit, and works the same on a trial or paid key.
2. Pick the window. `reddit_search` accepts `range` (past_hour..all_time) for `type: "posts"` only; comment search has no server-side time filter, so for `type: "comments"` fetch with `sort: "new"` and filter results yourself by `created_at`. `x_search` has no date parameter either: put `since:`/`until:` operators directly in the query string.
3. Sweep Reddit: `reddit_search` with `type: "posts"`, the launch name as `query`, and `range` set to the window, for what people are posting; a second `reddit_search` with `type: "comments"`, `sort: "new"` for reactions buried inside other discussions, the more unique signal. Decompose a broad or generic launch name into narrower queries (an exact phrase, the product name plus a qualifier) if one query looks capped near its result depth.
4. Sweep X: `x_search` with `type: "recent"` for the chronological deep sweep (follow `cursor` as far as the volume warrants; on the free tier only the first page is served, deeper pages need purchased credits); `type: "popular"` for the highest-engagement takes, which are usually worth quoting even at low volume.
5. Drill into the threads and tweets that carry the most signal (most comments, most engagement, or clearly representative of a theme). Batch-fetch Reddit bodies with `reddit_get_post` (up to 100 ids per call, first 10 included in the base price); reserve `detail: "full"` (+4 credits, one id only) for the one or two threads worth reading end to end. For a specific high-engagement tweet, `x_get_tweet` gets full metrics.
6. For accounts that matter (an account whose take is driving the conversation, or whose follower count makes them worth naming), `x_get_profile` for bio and follower count. Do not profile every author; that is not what the budget is for.
7. Read the returned text yourself and sort it into positive, negative, and neutral. Veezee has no sentiment-scoring endpoint; the API returns raw text and engagement counts, and judging tone is your job as the agent, not a field in the response.

## Rules that save credits and errors

- Default freshness is cached (`recent`, usually refreshing every 10-20 minutes) and free. Launch-day windows often justify `freshness: "realtime"` (+2 credits per call) to catch reactions from the last few minutes rather than the last cache cycle, but it needs a PAID key: trial keys are cached-only and reject realtime with TRIAL_CAP_EXCEEDED.
- Set `max_credits` on each call; a call whose quote exceeds it is rejected with nothing charged, so a sweep can keep going instead of overspending on one query.
- On KEY_REQUIRED, mint the free key and retry the same call; this one is never a payment problem. On TRIAL_CAP_EXCEEDED, INSUFFICIENT_CREDITS, or BUDGET_EXHAUSTED, stop and hand the error's `upgrade_url` to your human; purchases credit the account directly and the same key keeps working afterward. On RATE_LIMITED (429), wait `retry_after_seconds` and continue; it clears on its own and payment only raises the limit.
- A 403 NOT_ENTITLED means the key's account is not enabled for that platform; grants are explicit, write to hello@veezee.io to enable more.
- This is a one-shot sweep of a fixed window, run once and reported, not a running loop. For ongoing, deduped-across-polls coverage of a topic or brand over time, use the reddit-monitoring skill instead.

## Output

A structured readout the human can act on without re-reading the raw data. Use this shape:

```
# <Launch name> reaction sweep (<window>)

Volume: <n> Reddit posts, <n> Reddit comments, <n> tweets (list each query and the window it covered)

Positive / Negative / Neutral: 2-3 representative quotes per bucket, each with author and link
(`permalink` for Reddit, `url` for X)

Themes: 3-5 recurring topics, one line each

Notable accounts: name, follower count, stance, why they matter to this launch

Credits spent: <sum of usage.credits_charged across all calls>
```

Quotes must be verbatim from returned text with real links; never paraphrase into the quote slot. Report credits spent so the human can budget the next sweep.
