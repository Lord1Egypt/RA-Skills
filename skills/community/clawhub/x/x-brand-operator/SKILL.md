---
name: x-brand-operator
description: Automate X/Twitter brand account operations using OpenClaw native tools (xurl + browser fallback + cron). Use when setting up or managing automated posting, keyword engagement, weekly reporting, or Substack content generation for a brand account. Triggers on: "set up X posting for [brand]", "automate my Twitter account", "schedule tweets", "keyword engagement on X", "brand social media automation".
---

# X Brand Operator

End-to-end X/Twitter brand account automation using xurl (X API v2) with browser fallback. No extra API keys beyond xurl app config.

## Core Tools

- `xurl --app <app>` — Post, reply, like, follow, search via X API v2
- `browser` — Fallback for posting/replying when xurl fails (profile: user)
- `cron` — Schedule recurring tasks (post, engage, report)
- `message` — Send Telegram alerts on failures or completions

## Posting a Tweet

**Primary (xurl):**
```bash
xurl --app <app> post "<tweet text>"
```

**Fallback (browser, only if xurl fails):**
1. `browser open` → `https://x.com/compose/post` (profile: user)
2. Wait 4 seconds
3. `browser snapshot` → find text input ref
4. `browser act` → click input, type tweet
5. `browser snapshot` → find Post button ref
6. `browser act` → click Post
7. `browser snapshot` → confirm success

**Rule:** Try each method once only. On failure → notify via Telegram, include draft text, then exit. Never loop.

## Replying to a Tweet

**Primary:** `xurl --app <app> reply <tweet_id> "<reply text>"`

**Fallback:** Open tweet URL in browser → snapshot → click Reply → type → submit.

## Content Quality Standard (score before posting)

| Criterion | Weight |
|-----------|--------|
| Hook strength | 25 pts |
| Value density | 25 pts |
| Platform fit | 20 pts |
| CTA clarity | 15 pts |
| Conciseness | 15 pts |

**Minimum score: 70/100.** Rewrite once if below threshold; do not post if still failing.

**Format rules:** Single paragraph, no line breaks, ≤ 280 chars, 1–2 hashtags, end with brand URL.

## Content Pillar Rotation (daily posting)

Rotate through pillars by day of week. See `references/content-strategy.md` for pillar definitions, templates, and tone guide. Adapt pillars to the brand's positioning.

## Keyword Engagement (weekly)

Search target keywords → filter genuine posts (skip bots/ads) → like + reply + follow author.

**Reply quality rules:**
- Acknowledge the person's pain point first
- Add 2–4 sentences of genuine value
- Naturally mention the brand (no hard sell)
- Never use "Great post!" / "So true!" filler

See `references/engagement-playbook.md` for keyword lists and reply templates.

## Cron Job Setup

See `references/cron-config.md` for recommended schedules and full agentTurn prompt templates for:
- Morning post (UTC 14:00 daily)
- Evening post (UTC 20:00 daily)
- Weekly keyword engagement (Monday UTC 10:00)
- Weekly Substack draft (Wednesday UTC 13:00)
- Weekly report (Sunday UTC 21:00)

## Failure Handling

| Situation | Action |
|-----------|--------|
| xurl fails | Switch to browser fallback immediately |
| Browser also fails | Send Telegram alert with draft text, exit |
| Any step in engagement fails | Skip that item, continue to next |
| Always | Send Telegram summary at end of engagement/report runs |

Never retry more than once per method. Never loop.
