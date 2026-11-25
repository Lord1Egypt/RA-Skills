---
name: talktoads
description: Run Meta (Facebook + Instagram) ads by talking to your AI agent. Lists ad accounts, campaigns, ad sets and ads, reports spend, ROAS and cost per result, audits an account for wasted spend, boosts an Instagram reel or post into a campaign, creates campaigns, ad sets and ads (always paused), changes budgets, pauses and activates. Use when the user asks about Facebook ads, Instagram ads, Meta ads, boosting a reel or post, ad spend, ROAS, CPA, CTR, campaign performance, launching, pausing or scaling ads, or auditing an ad account.
license: MIT
compatibility: Needs the TalkToAds MCP server (https://talktoads.com/mcp, streamable HTTP, OAuth sign-in with Facebook, no API key). Free plan includes 15 tasks a month.
metadata:
  author: IndianAppGuy
  version: "1.0.0"
  homepage: https://talktoads.com/?ref=skill
  openclaw: {"emoji":"📣","homepage":"https://talktoads.com/?ref=openclaw"}
  hermes: {"tags":["meta-ads","facebook-ads","instagram-ads","marketing","advertising"],"category":"marketing"}
---

# TalkToAds: run Meta ads from your agent

TalkToAds connects the user's Facebook ad account to the agent. The agent can read performance, audit the account, and build campaigns, ad sets and ads. Everything it creates starts **paused**. Nothing spends money until the user says go live.

## Connect (once)

Check in this order:

1. **MCP tools already present** (`list_ad_accounts`, `get_performance`, `boost_instagram_post`, … possibly prefixed like `mcp__talktoads__list_ad_accounts`): use them.
2. **Otherwise add the MCP server** (remote, streamable HTTP, sign in with Facebook):
   - Claude Code: `claude mcp add --transport http talktoads https://talktoads.com/mcp`, then `/mcp` to sign in
   - Codex: `codex mcp add talktoads --url https://talktoads.com/mcp`, then `codex mcp login talktoads`
   - Claude.ai / Claude Desktop: Settings → Connectors → Add custom connector → `https://talktoads.com/mcp`
   - Any other client: server URL `https://talktoads.com/mcp`

The user signs in with the Facebook account that manages the ads. More at https://talktoads.com/?ref=skill.

## Start of every session

1. `recall_brand_memory` for the ad account you are working on. Follow what it says (target CPA, brand voice, margins, words to avoid).
2. `list_ad_accounts` if you do not know the account id or currency. Budgets are in the account's currency, major units (500 = ₹500 or $500).

## Common jobs

- **"How are my ads doing?"** → `get_performance` on the account with `level: "campaign"` (or `adset` / `ad`) for the period asked. Report spend, results, cost per result, ROAS, CTR in a short table. Say which campaigns to scale and which to cut.
- **"Audit my account" / "where am I wasting money?"** → `audit_account`. Lead with the score, then the top 3 fixes.
- **"Boost this reel to my page"** → `boost_instagram_post` with the post URL, link, daily budget and audience. It creates campaign + ad set + ad, all paused.
- **New campaign from scratch** → `list_pages` (and `list_pixels` for sales), `search_interests` / `estimate_audience` for targeting, then `create_campaign` → `create_ad_set` → `create_ad`. All paused.
- **Scale or cut** → `update_budget` (move at most ~20% at a time on ad sets out of learning), `pause`.
- **Rejected ads** → `list_ads` shows review feedback.
- **What changed?** → `get_change_log`. **Plan and tasks left** → `get_usage`.

## Going live: always ask

After creating anything, show a short draft and wait for a clear yes:

```
Campaign: Reel boost – Diwali sale (Sales, paused)
Budget: ₹500/day
Audience: India, 22–40, interests: online shopping, fashion
Creative: your reel instagram.com/reel/DelyrM6CoFO
Link: https://example.com/sale
Go live?
```

Only call `go_live` after the user says launch / go live / activate in this conversation. A yes for one campaign is not a yes for the next. If anything changes (budget, audience, creative, link), ask again. Pass ids parent-first: campaign, then ad set, then ad.

## Rules

- Never raise a budget, go live or delete without the user asking in this conversation.
- Respect the user's spend cap. If a budget is above it, tell them and let them raise it with `set_spend_cap`.
- When the user states a lasting preference (target CPA, tone, banned words, audiences that work), save it with `remember_brand_fact`.
- Report numbers as they come back. Do not round away losses or invent conversions.

## Examples

- "How did my Meta ads do last 7 days? Which campaign should I kill?"
- "Audit act_123 for the last 30 days."
- "Boost my latest reel to talktoads.com at ₹500 a day, India, 25–45."
- "Pause every ad set with cost per purchase above ₹800."
- "Raise the budget on the winning ad set by 20%."
- "Remember: target CPA is ₹300, never say 'guaranteed'."
