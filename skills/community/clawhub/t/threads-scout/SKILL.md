---
name: threads-scout
description: Read Meta Threads and Bluesky without an account or API key. Search Threads posts and accounts, read any Threads profile and its posts, open a post with its replies, and read Bluesky profiles and posts. Use this skill for social listening on Threads, creator research, or tracking conversations on the newer text-first networks.
---

# Threads Scout: Threads & Bluesky

![Threads Scout: Threads & Bluesky](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/threads-scout.gif)

Search and read the text-first networks: Threads posts and accounts, any profile and its replies, plus Bluesky profiles and posts.

No Threads or Bluesky account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=threads-scout).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/threads-scout.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “What is being posted about AI agents on Threads?”
- “Show @zuck's latest Threads posts”
- “Find Threads accounts about indie hacking”
- “Read this Bluesky profile's last posts”

## When to Use This Skill

Use it when the user wants public posts or accounts from Threads or Bluesky.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Threads/Bluesky  │
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

### Threads

| Tool | What it returns | Price |
|------|-----------------|-------|
| `threadsdata_search` | Search Threads posts by keyword, optionally within a date range | $0.00282 |
| `threadsdata_search_users` | Find Threads accounts by name or username | $0.00282 |
| `threadsdata_profile` | Public Threads profile by handle: name, bio, follower count, verified, links | $0.00282 |
| `threadsdata_user_posts` | Recent posts of a Threads account by handle, with text and like count | $0.00282 |
| `threadsdata_post` | One Threads post by URL with its replies and the rest of the thread | $0.00282 |

### Bluesky

| Tool | What it returns | Price |
|------|-----------------|-------|
| `blueskydata_profile` | Public Bluesky profile by handle: followers, following, post count, bio | $0.00282 |
| `blueskydata_user_posts` | Recent posts of a Bluesky account by handle | $0.00282 |
| `blueskydata_post` | One Bluesky post by URL with likes, reposts and replies | $0.00282 |

## Recipes

### Find voices on a topic

1. `threadsdata_search` for the topic.
2. `threadsdata_profile` on the authors who come up most.
3. `threadsdata_user_posts` to see how consistently they post about it.

## Code Examples

### Search Threads

```bash
clawlink_call_tool --tool "threadsdata_search" \
  --params '{"query": "AI agents"}'
```

### A Threads profile

```bash
clawlink_call_tool --tool "threadsdata_profile" \
  --params '{"handle": "zuck"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `threads`); public-data tools show as connected for every user.
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

- Threads search can be limited by date with `start_date` / `end_date` (YYYY-MM-DD).
- Bluesky handles look like `name.bsky.social`.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Profile not found | Check the handle; private accounts return nothing. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=threads-scout; do not retry. |
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


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=threads-scout)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=threads-scout)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [X Pulse](https://clawhub.ai/hith3sh/skills/x-pulse)
- [Brand Listener](https://clawhub.ai/hith3sh/skills/brand-listener)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=threads-scout)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
