---
name: stream-radar
description: Live-streaming research without accounts or API keys. Twitch profiles, followers, past broadcasts, schedules and clips, Kick clips, and TikTok Live: whether a creator is live, live room stats, live search, and top gifters. Use this skill for streamer research, sponsorship scouting, tracking a streamer's schedule, or monitoring live events.
---

# Stream Radar: Twitch, Kick & TikTok Live

![Stream Radar: Twitch, Kick & TikTok Live](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/stream-radar.gif)

Follow streamers across platforms: Twitch followers, past broadcasts and schedules, Kick clips, and whether a TikTok creator is live right now with their room stats.

No Twitch, Kick or TikTok account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=stream-radar).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/stream-radar.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “How big is Kai Cenat on Twitch and is he live?”
- “When does this streamer go live this week?”
- “Is this TikTok creator live right now?”
- “Find TikTok live streams about cooking”

## When to Use This Skill

Use it when the user wants streamer profiles, schedules, clips or live status on Twitch, Kick or TikTok.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Live streams     │
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

### Twitch

| Tool | What it returns | Price |
|------|-----------------|-------|
| `twitchdata_profile` | Public Twitch channel by handle: followers, description, live status, recent stream info | $0.00282 |
| `twitchdata_user_videos` | Past broadcasts, highlights and uploads of a Twitch channel | $0.00282 |
| `twitchdata_user_schedule` | A Twitch channel's stream schedule | $0.00282 |
| `twitchdata_clip` | A Twitch clip by URL: title, streamer, game, views, duration | $0.00282 |

### Kick

| Tool | What it returns | Price |
|------|-----------------|-------|
| `kickdata_clip` | A Kick clip by URL: title, streamer, category, views, duration | $0.00282 |

### TikTok Live

| Tool | What it returns | Price |
|------|-----------------|-------|
| `tiktokdata_user_live` | Whether a TikTok user is live now, with the room id and live stats | $0.00282 |
| `tiktokdata_live_room` | A TikTok live room's info and stats | $0.00282 |
| `tiktokdata_search_lives` | TikTok live streams on now that match a keyword | $0.0015 |
| `tiktokdata_live_viewers_ranking` | Top gifters and viewers of a TikTok live room | $0.0015 |

## Recipes

### Scout a streamer for a sponsorship

1. `twitchdata_profile` for followers and links.
2. `twitchdata_user_videos` for typical views.
3. `twitchdata_user_schedule` for when they are live.

## Code Examples

### Twitch profile

```bash
clawlink_call_tool --tool "twitchdata_profile" \
  --params '{"handle": "kaicenat"}'
```

### Is a TikToker live

```bash
clawlink_call_tool --tool "tiktokdata_user_live" \
  --params '{"handle": "creator_handle"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `twitch`); public-data tools show as connected for every user.
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

- Twitch handles are the channel name in the URL.
- TikTok live room ids come from `tiktokdata_user_live`.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Not live | Offline creators return no live room; check their schedule instead. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=stream-radar; do not retry. |
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


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=stream-radar)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=stream-radar)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [Creator Scout](https://clawhub.ai/hith3sh/skills/creator-scout)
- [Tube Scout](https://clawhub.ai/hith3sh/skills/tube-scout)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=stream-radar)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
