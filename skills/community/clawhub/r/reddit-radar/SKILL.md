---
name: reddit-radar
description: Research Reddit without a Reddit account or API key. Search posts and comments across Reddit, browse and search any subreddit, read full comment threads, see popular posts and trending searches, and look up users and their history. Use this skill for market research, product feedback, finding real recommendations, or tracking what communities say.
---

# Reddit Radar: Reddit Research

![Reddit Radar: Reddit Research](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/reddit-radar.gif)

Find out what real people say: search all of Reddit or one subreddit, read full threads with every comment, and see what is popular and trending.

No Reddit account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=reddit-radar).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/reddit-radar.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “What does Reddit recommend as a CRM for startups?”
- “Summarise the top posts in r/SaaS”
- “What are people complaining about with Notion?”
- “What's trending on Reddit today?”

## When to Use This Skill

Use it when the user wants public Reddit posts, comments, subreddits or users.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Reddit           │
│   (User Chat)   │     │ (data tools) │     │ (public data)    │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install plugin    │                       │
         │  2. Pair device once  │                       │
         │  3. Ask a question    │                       │
         │                       │  4. Fetch + trim      │
         │                       │  5. Charge credit     │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  Answer  │           │  Credit  │           │ Results  │
   │ in chat  │           │ ($0.50)  │           │ as JSON  │
   └──────────┘           └──────────┘           └──────────┘
```

ClawLink holds the data-provider accounts. The user never pastes a key, and nothing is installed beyond the plugin.

## Install

Install the ClawLink plugin from ClawHub when the user asks for it:

```bash
openclaw plugins install clawhub:clawlink-plugin
```

The install applies to the running Gateway: do not restart it. The ClawLink tools appear on your next turn, so end this turn and tell the user: "ClawLink is installed. Reply ok and I will give you your pairing link." On the next turn call `clawlink_begin_pairing`, give the user the link, and after they approve call `clawlink_get_pairing_status`. Pairing happens once; after that every tool below works with no further setup.

## Tool Reference

Prices are what ClawLink charges per call, from the user's credit. The tool's own description (via `clawlink_describe_tool`) always shows the current price.

### Search

| Tool | What it returns | Price |
|------|-----------------|-------|
| `redditdata_search_posts` | Search all of Reddit for posts about a topic, with title, text, score, comment count and subreddit | $0.00282 |
| `redditdata_search_comments` | Search Reddit comments by keyword across all subreddits: text, score, author, and the post each is on | $0.0015 |
| `redditdata_search_communities` | Find subreddits about a topic: name, description, subscriber count | $0.0015 |
| `redditdata_trending_searches` | What people are searching for on Reddit today | $0.0015 |

### Subreddits

| Tool | What it returns | Price |
|------|-----------------|-------|
| `redditdata_subreddit_posts` | Current posts in a subreddit (hot, new, top or rising) | $0.00282 |
| `redditdata_subreddit_search` | Search inside one subreddit for posts matching a query | $0.00282 |
| `redditdata_subreddit_details` | About a subreddit: description, rules, weekly active users and contributions, creation date | $0.00282 |
| `redditdata_popular_posts` | Posts on Reddit's r/popular feed right now: title, subreddit, score, comment count, upvote ratio, link | $0.0015 |

### Threads & Users

| Tool | What it returns | Price |
|------|-----------------|-------|
| `redditdata_post_comments` | One Reddit post by URL with its full text and its comment tree (author, text, score, replies) | $0.00282 |
| `redditdata_post_transcript` | Captions of a Reddit video post as plain text (transcriptNotAvailable when the video has none) | $0.00282 |
| `redditdata_user_profile` | Public Reddit user by username: post and comment karma, account creation date, post and comment counts, bio,… | $0.0015 |
| `redditdata_user_posts` | Posts a Reddit user submitted: title, text, score, comment count, URL. Page with `after` = endCursor | $0.0015 |
| `redditdata_user_comments` | Comments a Reddit user wrote: the first 300 characters of each, score, date and the post it is on | $0.0015 |

## Recipes

### Find honest recommendations

1. `redditdata_search_posts` with the question people would ask.
2. `redditdata_post_comments` on the 2-3 threads with the most comments.
3. Tally which products get recommended, and why.

## Code Examples

### Search Reddit

```bash
clawlink_call_tool --tool "redditdata_search_posts" \
  --params '{"query": "best CRM for startups", "sort": "top", "timeframe": "year"}'
```

### A subreddit's top posts

```bash
clawlink_call_tool --tool "redditdata_subreddit_posts" \
  --params '{"subreddit": "SaaS", "sort": "top"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `reddit`); public-data tools show as connected for every user.
2. Call `clawlink_describe_tool` before the first call of a tool: it returns the parameters, defaults and price.
3. Treat the live catalog as the source of truth. If a tool named here is missing, say so; do not invent results.

## Execution Workflow

```
┌───────────────────────────────────────────────────────────┐
│  READ-ONLY, PAID PER CALL                                │
│  search → describe → call → summarise for the user       │
│                                                          │
│  Ask before: loops over many items, or a call that costs │
│  more than a few cents (the price is in the description) │
└───────────────────────────────────────────────────────────┘
```

1. Every tool here only reads public data; nothing is posted or changed.
2. Each call costs credit. Before looping over more than about ten items, or before a call priced above a few cents, tell the user what it will cost and ask.
3. A failed call is refunded automatically. Read the error's `hint`: it says what to change. Do not retry the same arguments unchanged.

## Notes

- Subreddit names go without `r/`.
- A thread's comments come with nested replies; `more` lists collapsed ones.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Subreddit not found | Check the spelling, or that it is not private or banned. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=reddit-radar; do not retry. |
| `data_provider_unavailable` | ClawLink's data provider is down. Nothing was charged. Try again later. |
| `no_result` | The provider found nothing for these arguments. Nothing was charged. |
| `invalid_arguments` | A parameter is missing or malformed. Call `clawlink_describe_tool` and fix it. |

## Troubleshooting

### Tools not visible after install

1. The tools appear on the turn after the install, not in the same turn.
2. If they still do not appear, the OpenClaw tool profile may hide plugin tools. This is a config change for the OpenClaw owner; do not change the config yourself. Tell the user: "Your OpenClaw tool profile hides plugin tools. In the Control UI (or `~/.openclaw/openclaw.json`), add `clawlink-plugin` to `tools.alsoAllow`, then ask me again."
3. On OpenClaw versions before 2.0, the tool list can load only in a new chat: tell the user to send `/new` and ask again.

### A tool keeps failing with correct input

Report it with `clawlink_report_issue` (or `clawlink_call_tool --tool "CLAWLINK_REPORT_ISSUE"`) instead of retrying. Reports are free and reach the ClawLink team.

## Resources


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=reddit-radar)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=reddit-radar)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [Brand Listener](https://clawhub.ai/hith3sh/skills/brand-listener)
- [X Pulse](https://clawhub.ai/hith3sh/skills/x-pulse)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=reddit-radar)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
