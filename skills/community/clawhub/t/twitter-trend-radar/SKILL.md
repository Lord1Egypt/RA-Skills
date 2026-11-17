---
name: twitter-trend-radar
description: Find early product, tool, game, and SEO opportunity signals from X/Twitter using the local bird CLI. It searches launch-signal tweets with links, extracts domains, checks domain age via RDAP, scores opportunities, and outputs Markdown/JSON reports. Use for trend scouting, SEO/GEO opportunity discovery, indie game/product monitoring, and landing-page ideation.
---

# Twitter Trend Radar Skill

Use this skill when the user asks to discover emerging products, tools, indie games, browser games, AI apps, SEO/GEO opportunities, or “what is starting to trend on X/Twitter”.

This skill is inspired by the logic of `qiayue/Twitter-Trend-Radar`: scan X for launch-moment tweets that contain links and engagement, extract domains, reverse-check domain age and traffic-like signals, then rank likely early opportunities.

This implementation uses the local `bird` CLI instead of paid Twitter/X API or third-party Twitter search APIs.

## Core logic

1. Build a pool of launch-signal search queries.
2. Run `bird search "<query>" --json` for each query.
3. Parse tweets from bird JSON output.
4. Extract outbound links and domains.
5. Filter noisy domains such as x.com, youtube.com, github.com, producthunt.com, etc.
6. Check domain age through RDAP when available.
7. Score each domain/tweet cluster by:
   - engagement
   - recency
   - link presence
   - domain freshness
   - launch-signal phrase strength
   - repeated mentions
8. Output a report with suggested landing pages and next actions.

## Safety and risk policy

Use this skill read-only by default. Do not post, reply, DM, like, or follow unless the user explicitly asks and accepts platform/account risk.

`bird` can use X/Twitter GraphQL with browser cookies. This is not the official public X API. X can rate-limit, block, or change private endpoints. Keep searches low frequency, cache results, avoid concurrency, and do not run this as a public multi-user SaaS using one account.

## Requirements

Install `bird` and confirm it can read/search X:

```bash
bird --version
bird whoami
bird search "just launched filter:links" -n 5 --json
```

Recommended bird setup:

```bash
bun add -g @steipete/bird
```

If browser cookie extraction fails, configure `bird` according to your environment. Common options:

```bash
bird --chrome-profile "Default" whoami
bird --firefox-profile "default-release" whoami
```

## Main command

Run the bundled script:

```bash
python scripts/twitter_trend_radar.py --topic "browser game" --days 30 --min-likes 20 --limit 30 --format markdown
```

For JSON:

```bash
python scripts/twitter_trend_radar.py --topic "AI agent" --days 14 --min-likes 50 --format json
```

Save a report:

```bash
python scripts/twitter_trend_radar.py --topic "indie game" --days 30 --min-likes 20 --output reports/indie-game-radar.md
```

## Useful topics

For AI/product opportunities:

```bash
python scripts/twitter_trend_radar.py --topic "AI app" --days 14 --min-likes 50
python scripts/twitter_trend_radar.py --topic "AI agent" --days 14 --min-likes 50
python scripts/twitter_trend_radar.py --topic "SaaS" --days 30 --min-likes 30
```

For game SEO opportunities:

```bash
python scripts/twitter_trend_radar.py --topic "browser game" --days 30 --min-likes 20
python scripts/twitter_trend_radar.py --topic "made a game" --days 30 --min-likes 20
python scripts/twitter_trend_radar.py --topic "play online game" --days 30 --min-likes 20
python scripts/twitter_trend_radar.py --topic "indie game" --days 30 --min-likes 20
```

For Meccha/Super Chameleon-like research:

```bash
python scripts/twitter_trend_radar.py --topic "chameleon game" --days 60 --min-likes 5
python scripts/twitter_trend_radar.py --topic "hide and seek game" --days 60 --min-likes 10
python scripts/twitter_trend_radar.py --topic "paint game" --days 60 --min-likes 10
```

## Query design

The script combines the topic with launch phrases:

- just launched
- introducing
- built this
- made this
- made a site
- shipped
- launch day
- now live
- new app
- new tool
- new game
- try it
- play online

It adds link and engagement filters when supported by X search syntax:

```text
filter:links min_faves:<N> since:<YYYY-MM-DD>
```

## Output interpretation

High scores mean “investigate now”, not “build blindly”. Before building a page or product, manually verify:

- Is the linked site real and accessible?
- Is the product/game new or merely being rediscovered?
- Are people asking for alternatives, online version, pricing, or tutorials?
- Is there searchable demand in Google/YouTube/Reddit?
- Is the keyword legally safe and not a protected brand misuse?

## Recommended follow-up prompt

After running the skill, ask:

> Based on this radar output, pick the top 5 SEO/GEO opportunities and generate landing-page briefs with target keywords, page structure, title, H1, FAQ, and CTA.
