# Short-Form Market Research Brain

Your AI agent's brain for short-form video market research, powered by the [Virlo API](https://dev.virlo.ai).

## What This Skill Does

Gives your OpenClaw agent deep expertise in social media market research across TikTok, YouTube Shorts, and Instagram Reels. Everything runs through the unified **Content Research Agents API** (`POST /v1/agents`): set `is_recurring: false` for a one-shot niche search, or `is_recurring: true` for recurring monitoring: one resource, one set of read paths.

- **Niche Research**: Search any topic and get AI-generated intelligence reports covering trends, creators, platform dynamics, sentiment, and viral patterns
- **Creator Discovery**: Find rising creators who outperform their follower count, analyze any creator's profile and engagement metrics
- **Trend Tracking**: Topic Trends show what people are talking about (news and pop culture, by region); Content Trends show the video formats creators are copying right now. Drill into hashtag performance
- **Ad Intelligence**: See what Meta ads are running for any topic or niche
- **Automated Monitoring**: Set up recurring agents that run daily, weekly, or monthly. Autopilot, on by default, keeps tuning their keywords and never removes the ones you set

> The older `/v1/orbit` and `/v1/comet` endpoints are **deprecated**. They still respond today, but don't build on them: migrate to `/v1/agents` (IDs are interchangeable).

## Install

```bash
clawhub install short-form-market-research-brain
```

## Setup

1. Get a Virlo API key at [dev.virlo.ai/dashboard](https://dev.virlo.ai/dashboard)
2. Add funds to your prepaid balance at [dev.virlo.ai/dashboard/billing](https://dev.virlo.ai/dashboard/billing) (the page shows the minimum). No subscriptions, and the balance never expires
3. Provide the key as the `VIRLO_API_KEY` environment variable. In `~/.openclaw/openclaw.json`:

```json5
{
  skills: {
    entries: {
      "short-form-market-research-brain": {
        env: { VIRLO_API_KEY: "virlo_tkn_YOUR_KEY" }
      }
    }
  }
}
```

The skill declares `VIRLO_API_KEY` as a required env var, so OpenClaw keeps it hidden until the key is configured: once set, it activates automatically.

## Example Prompts

- "Research the TikTok Shop niche: give me a full market analysis"
- "Find trending content about AI coding tools across all platforms"
- "Analyze the TikTok creator @username: how are they performing?"
- "What's trending on social media today?"
- "Set up weekly monitoring for wedding photography content"
- "Is this video an outlier? [paste URL]"
- "Show me the top performing hashtags on YouTube this week"
- "Find creators making content about personal injury law"
- "Compare what's working on TikTok vs YouTube for meal prep content"

## Pricing (1 credit = $0.01)

| Action | Cost |
|--------|------|
| Raw live reads (`/v1/raw/*`: search, hashtag, video, comments, transcript, creator, creator videos) | $0.01 per page |
| Hashtag stats (`/v1/hashtags`, hashtag performance) | $0.05 |
| Sound detail / usage history | $0.05 |
| One Content Trend (`/v1/content-trends/:id`, all examples + 30-day series) | $0.05 |
| Sound search / hook templates | $0.10 |
| Video digest / Topic Trends (`/v1/topic-trends`, incl. emerging) / Trending sounds / Breakout sounds / Trending hooks / Hook search | $0.25 |
| Content Trends list (`/v1/content-trends`, video formats creators are copying right now) | $0.25 |
| Tracking a creator or video | $0.25 to start, then $0.25 per check |
| Agent one-shot search (`is_recurring: false`, full niche analysis) | $0.50 |
| Agent recurring monitor (`is_recurring: true`) | Free to create, $0.50 per run (the first run starts right away) |
| Data Intelligence add-on (per search / run) | +$1.00 |
| Creator profile lookup | $0.50 (up to $1.75 with add-ons) |
| Batch creator lookup | $0.50 per creator looked up, cached ones free |
| Sound lookup | $0.50 ($1.00 with trend analysis) |
| Hashtag lookup (deep dive) | $0.50 to $2.50 |
| Video outlier analysis | $0.50 |
| Keyword suggestions, agent autopilot (activity log, on/off switch, deprecated proposals) | Free |
| Retrieving results (videos, ads, outliers, analysis, sounds, saved lookups) | Free (agent hooks $0.25 unless Data Intelligence is on or the agent has no hooks yet) |

Failed requests are never charged. A creator, sound, or hashtag lookup that fails, a trend analysis that finds no trends, and a post collection that finds no posts are refunded automatically.

## Links

- [API Documentation](https://dev.virlo.ai/docs)
- [Full API Reference for Agents](https://dev.virlo.ai/llms-full.txt)
- [Pricing](https://dev.virlo.ai/pricing)
- [Dashboard](https://dev.virlo.ai/dashboard)
