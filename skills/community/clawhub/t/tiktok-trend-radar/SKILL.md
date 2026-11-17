---
name: tiktok-trend-radar
description: TikTok trend research with no TikTok account or API key. Trending videos by country, trending hashtags, trending searches, the Top 50 and Viral 50 music charts, TikTok Creator Search Insights (what people search, by age, gender and country), and deep dives on any hashtag, sound or video. Use this skill for content ideas, viral sound picks, niche trend tracking, or social media research.
---

# TikTok Trend Radar: Trends & Viral Sounds

![TikTok Trend Radar: Trends & Viral Sounds](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/tiktok-trend-radar.gif)

Find what is taking off on TikTok right now: trending videos, hashtags, searches and sounds, plus TikTok's own Creator Search Insights on what people are searching for and who searches it.

No TikTok account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=tiktok-trend-radar).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/tiktok-trend-radar.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “What songs are trending on TikTok right now?”
- “Show trending TikTok videos in the UK today”
- “What are people searching for on TikTok in fitness?”
- “Is the sound ‘Espresso’ still growing? Show videos using it”
- “Which hashtags are trending in the US this week?”

## When to Use This Skill

Use it when the user wants TikTok trends, viral sounds, trending hashtags or searches, or public details about a TikTok hashtag, sound or video.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ TikTok           │
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

### Trending Now

| Tool | What it returns | Price |
|------|-----------------|-------|
| `tiktokdata_trending_feed` | Videos trending on TikTok right now, as seen from a country | $0.00282 |
| `tiktokdata_trending_hashtags` | Hashtags trending on TikTok in a country, ranked, with their popularity curve | $0.0018 |
| `tiktokdata_trending_searches` | Today's trending search terms on TikTok | $0.0015 |
| `tiktokdata_explore_feed` | Videos from TikTok's explore page, by category | $0.0015 |
| `tiktokdata_music_charts` | TikTok's music charts: Top 50 (scene 0) or Viral 50 (scene 1) | $0.0015 |

### Creator Search Insights

| Tool | What it returns | Price |
|------|-----------------|-------|
| `tiktokdata_search_insights` | What people search on TikTok (Creator Search Insights): rising searches, content gaps and topics, with query ids for… | $0.0015 |
| `tiktokdata_search_insight_detail` | Who searches one TikTok search term: by gender, age and country, over a time range | $0.0015 |
| `tiktokdata_search_insight_trend` | How searches for one TikTok search term changed over time | $0.0015 |
| `tiktokdata_search_insight_videos` | Videos TikTok shows for a search-insights keyword | $0.0015 |

### Search

| Tool | What it returns | Price |
|------|-----------------|-------|
| `tiktokdata_search_videos` | Search public TikTok videos by keyword | $0.002 |
| `tiktokdata_search_top` | TikTok's Top search tab for a keyword: videos and photo posts ranked together | $0.00282 |
| `tiktokdata_search_hashtags` | Hashtags matching a keyword, with their view counts | $0.0015 |
| `tiktokdata_search_music` | TikTok sounds and songs matching a keyword | $0.0015 |
| `tiktokdata_search_suggestions` | TikTok's autocomplete suggestions for a partial search | $0.00282 |

### Deep Dives

| Tool | What it returns | Price |
|------|-----------------|-------|
| `tiktokdata_hashtag_detail` | A TikTok hashtag's view count, video count and challengeID | $0.0015 |
| `tiktokdata_hashtag_posts` | Videos under a TikTok hashtag | $0.002 |
| `tiktokdata_song` | A TikTok sound or song: title, artist, duration and how many videos use it | $0.00282 |
| `tiktokdata_song_videos` | TikTok videos that use a sound | $0.00282 |
| `tiktokdata_post_detail` | One TikTok video by URL: caption, author, stats, music and hashtags | $0.002 |
| `tiktokdata_comment_keywords` | The most frequent keywords in a TikTok video's comments | $0.0015 |

## Recipes

### Find trends in a niche

1. `tiktokdata_search_insights` with the niche's category to see rising searches and content gaps.
2. `tiktokdata_search_insight_detail` on the best query for who searches it (age, gender, country).
3. `tiktokdata_search_insight_videos` to see what already ranks for it.

### Pick a sound before it peaks

1. `tiktokdata_music_charts` with `scene: 1` for the Viral 50.
2. `tiktokdata_song` for a candidate: how many videos use it.
3. `tiktokdata_song_videos` to see the formats people make with it.

## Code Examples

### Viral 50 chart

```bash
clawlink_call_tool --tool "tiktokdata_music_charts" \
  --params '{"scene": 1}'
```

### Trending videos in a country

```bash
clawlink_call_tool --tool "tiktokdata_trending_feed" \
  --params '{"region": "GB"}'
```

### Trending hashtags

```bash
clawlink_call_tool --tool "tiktokdata_trending_hashtags" \
  --params '{"region": "US", "period": 7}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `tiktok trending`); public-data tools show as connected for every user.
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

- `scene: 0` is the Top 50, `scene: 1` the Viral 50.
- Creator Search Insights returns query ids; pass one as `query_id_str` to the detail and trend tools.
- A sound's `clipId` is the number at the end of its tiktok.com/music URL.
- The trending feed is seen from the country in `region`; it is not filtered to that country's creators.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Empty insights | Try a broader category or the `all` tab; Creator Search Insights covers popular topics only. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=tiktok-trend-radar; do not retry. |
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

- [TikTok Creative Center](https://ads.tiktok.com/business/creativecenter)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=tiktok-trend-radar)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=tiktok-trend-radar)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [Creator Scout](https://clawhub.ai/hith3sh/skills/creator-scout)
- [Transcribe Any Video](https://clawhub.ai/hith3sh/skills/transcribe-any-video)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=tiktok-trend-radar)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
