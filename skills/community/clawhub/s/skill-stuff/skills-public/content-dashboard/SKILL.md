---
name: content-dashboard
description: Pulls analytics from Substack, LinkedIn, Twitter, Instagram, and Reddit into one normalised view. Use when a user wants cross-platform performance data in one place.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "📊"
  openclaw.user-invocable: "true"
  openclaw.category: content
  openclaw.tags: "analytics,stats,substack,linkedin,twitter,instagram,reddit,performance"
  openclaw.triggers: "how is my content doing,content stats,analytics,social media numbers,content performance"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/content-dashboard


# Content Dashboard

Every creator has six tabs open.
Substack dashboard. LinkedIn analytics. Twitter analytics. Instagram insights. Reddit profile.

This skill closes five of them.

---

## File structure

```
content-dashboard/
  SKILL.md
  config.md          ← platform credentials, metrics to track, normalisation rules
  data/
    [YYYY-MM-DD].md  ← snapshot per pull
  pieces.md          ← cross-platform performance per piece
```

---

## On-demand only

`/stats` — pull everything now
`/stats [platform]` — pull one platform
`/stats [piece title]` — performance of one piece across all platforms
`/stats week` — last 7 days across all platforms
`/stats month` — last 30 days

No automated runs unless user opts in.

---

## The normalisation problem

Platform metrics are not comparable by default.

| Metric | What it means |
|---|---|
| Substack "opens" | Emails opened — high intent, small audience |
| LinkedIn "impressions" | Times shown in feed — low intent, large audience |
| Twitter "views" | Times anyone saw the tweet — lowest intent |
| Instagram "reach" | Unique accounts who saw the post |
| Reddit "upvotes" | Explicit approval — high signal |

The dashboard doesn't pretend these are the same.
It shows each platform's metrics in their native format AND provides a normalised "resonance score" that accounts for platform context.

**Resonance score formula:**
A weighted score that accounts for platform-appropriate engagement rates.
An 8% engagement rate on Reddit is extraordinary.
An 8% engagement rate on Twitter is average.
The resonance score adjusts for this.

---

## Data collection flow

For each platform, the browser tool:
1. Authenticates (using stored session from content-publisher config)
2. Navigates to the analytics dashboard
3. Extracts the metrics
4. Returns structured data

---

## Platform-specific collection

### Substack

**Navigate to:** Substack dashboard → Stats

**Collect:**
- Total subscribers (free + paid breakdown if applicable)
- Subscriber growth (last 7d, 30d, 90d)
- For each recent post:
  - Sent to N subscribers
  - Opened: N (open rate %)
  - Clicked: N (click rate %)
  - New subscribers from this post: N
  - Top referring sources

**Key Substack metric:** Open rate. Industry average is ~40%. Above 50% is excellent.

---

### LinkedIn

**Navigate to:** LinkedIn Analytics → Posts

**Collect for each post:**
- Impressions
- Engagements (reactions + comments + shares)
- Engagement rate (engagements / impressions)
- Clicks (on link or "see more")
- Follower growth this period

**Key LinkedIn metric:** Engagement rate. Above 3% is good. Above 5% is strong.

---

### Twitter/X

**Navigate to:** Twitter Analytics → Content

**Collect for each tweet/thread:**
- Impressions
- Engagements (replies + likes + retweets + bookmarks)
- Engagement rate
- Profile clicks
- Link clicks (if applicable)
- Follower growth this period

**Key Twitter metric:** Bookmark rate. Bookmarks indicate "I want to come back to this" — high-quality signal.

---

### Instagram

**Navigate to:** Instagram Professional Dashboard → Content

**Collect for each post:**
- Reach (unique accounts)
- Impressions (total views)
- Interactions (likes + comments + saves + shares)
- Save rate (saves / reach) — the highest-signal metric
- Follower growth this period
- Profile visits from post

**Key Instagram metric:** Save rate. Saves = "I want to keep this." Strong signal of value.

---

### Reddit

**Navigate to:** Reddit profile → Posts

**Collect for each post:**
- Upvotes
- Upvote ratio (%)
- Comments
- Awards (if any)
- Crosspost count
- Estimated reach (upvotes × subreddit size / typical ratio)

**Key Reddit metric:** Comment quality (assessed by the agent — ratio of engaged discussion vs. quick reactions).

**Reddit note:** Reddit doesn't have a native analytics dashboard. The skill extracts what's visible on the post itself and the profile page.

---

## The unified view

When `/stats` is run, the output is a clean single-screen view:

---

**📊 Content Dashboard — [DATE]**
*Pulled: [timestamp]*

---

**OVERVIEW**

| Platform | Audience | 7d Growth | Best performer |
|---|---|---|---|
| Substack | [N] subscribers | +[N] | [Post title] [open rate]% |
| LinkedIn | [N] followers | +[N] | [Post title] [eng rate]% |
| Twitter/X | [N] followers | +[N] | [Post title] [N] bookmarks |
| Instagram | [N] followers | +[N] | [Post title] [save rate]% |
| Reddit | [N] karma | — | [Post title] [N] upvotes |

---

**TOP PERFORMERS THIS PERIOD**

🏆 **[POST TITLE]**
Cross-platform resonance score: [X/10]
• Substack: [open rate]% open rate ([N] opens)
• LinkedIn: [eng rate]% engagement ([N] impressions)
• Twitter: [N] bookmarks ([N] impressions)
• Instagram: [save rate]% save rate ([N] reach)
• Reddit: [N] upvotes, [upvote ratio]% positive

---

**WHAT'S WORKING**
[2-3 observations from the data — patterns across platforms, what's resonating]

**WHAT ISN'T**
[1-2 honest observations — what underperformed and a hypothesis why]

---

**GROWTH TREND**
[7-day and 30-day trajectory per platform — growing / flat / declining]

---

## Per-piece view

`/stats [piece title]`

Shows the performance of one piece across all platforms where it was published:

```
📊 "[PIECE TITLE]" — Cross-platform performance

Published: [date]
Days since publication: [N]

Substack
• Sent: [N] · Opened: [N] ([open rate]%) · Clicked: [N] ([click rate]%)
• New subscribers from this post: [N]

LinkedIn
• Impressions: [N] · Engagements: [N] ([eng rate]%)
• Shares: [N] · Comments: [N]

Twitter/X
• Impressions: [N] · Engagements: [N]
• Bookmarks: [N] · Retweets: [N]

Instagram
• Reach: [N] · Impressions: [N]
• Saves: [N] ([save rate]%) · Comments: [N]

Reddit (r/[subreddit])
• Upvotes: [N] · Ratio: [%] · Comments: [N]

RESONANCE SCORE: [X/10]
Best platform for this piece: [platform]
Weakest: [platform] — [one sentence hypothesis]
```

---

## Comparative analysis

`/stats compare [piece 1] vs [piece 2]`

Side-by-side performance of two pieces.
Useful for: understanding what topics or formats resonated more.

`/stats topic [topic]`

Groups all pieces about a similar topic and shows aggregate performance.
Reveals which topics consistently resonate vs. which don't.

---

## pieces.md — the performance log

Every piece published via content-publisher gets an entry in pieces.md.
The dashboard populates performance data over time.

```md
# Piece Performance Log

## [PIECE TITLE]
Slug: [slug]
Published: [date]
Platforms: [list]

### Performance snapshots
[DATE]: Substack [N]% open · LinkedIn [N]% eng · Twitter [N] bookmarks
[DATE + 7d]: [updated stats]
[DATE + 30d]: [30-day snapshot]

### Resonance score
7d: [X/10]
30d: [X/10]

### Notes
[Any manually added observations]
```

---

## Scheduled pulls (optional)

If the user wants automated stats:
`/stats schedule [weekly/monthly]`

Registers a cron job to pull stats on a schedule.
Results delivered to the configured channel.

Default: off. The skill is on-demand.

---

## Thought-leader integration

After every stats pull, the dashboard writes a summary back to `pieces.md`
in a format that `thought-leader` can read at the start of the next ideation session.

### What gets written to pieces.md after each pull

```md
## Intelligence summary
Last updated: [timestamp]
Based on: [N] pieces across [N] platforms

### Topic resonance (high → low)
[TOPIC]: avg resonance [X/10] across [N] pieces
[TOPIC]: avg resonance [X/10] across [N] pieces
[TOPIC]: avg resonance [X/10] — underperforming, consider rethinking approach

### Format resonance
Substack long-form (1000+ words): avg [X/10]
Substack short-form (<800 words): avg [X/10]
LinkedIn narrative: avg [X/10]
LinkedIn list: avg [X/10]
Twitter thread: avg [X/10]
Twitter single: avg [X/10]
Instagram single: avg [X/10]
Instagram carousel: avg [X/10]

### Platform performance ranking
1. [PLATFORM]: highest resonance per piece
2. [PLATFORM]
3. [PLATFORM]
4. [PLATFORM]
5. [PLATFORM]: lowest resonance per piece — consider different approach or content type

### Growth momentum
Fastest growing: [PLATFORM] (+[N] followers/subscribers last 30d)
Slowest: [PLATFORM]

### The top 3 pieces overall
1. "[TITLE]" — resonance [X/10] — strongest on [PLATFORM]
2. "[TITLE]" — resonance [X/10]
3. "[TITLE]" — resonance [X/10]

### Gaps worth exploring
[Topics adjacent to high performers that haven't been covered]
[Platform with growth but underused]

### What to do less of
[Topics or formats consistently underperforming]
```

This summary is read by `thought-leader` at the start of every new piece.
It makes the outline conversation evidence-based rather than instinct-based.

### `/stats suggest`

Generates piece ideas based on what's worked:

```
💡 Based on your performance data:

**High-confidence ideas** (topics that consistently resonate for you):
1. [Idea — directly in your strongest topic area]
2. [Idea — format that performs best for you on your best platform]

**Adjacent ideas** (topics near your best performers):
3. [Idea — related to high-performer topic but not yet covered]

**Platform opportunity** (underused channel with growth potential):
4. [Idea specifically designed for your fastest-growing platform]

**Risky but interesting** (new territory, no data yet):
5. [Idea in a topic area you haven't explored — could break through or not]
```

---

## Management commands

- `/stats` — full dashboard now
- `/stats [platform]` — one platform
- `/stats [piece]` — one piece across all platforms
- `/stats week` — last 7 days
- `/stats month` — last 30 days
- `/stats compare [piece1] vs [piece2]` — comparison
- `/stats topic [topic]` — topic performance
- `/stats schedule [frequency]` — set up automated pulls
- `/stats history` — list all snapshots in data/
- `/stats auth [platform]` — re-authenticate
- `/stats suggest` — generate piece ideas based on performance patterns
- `/stats update pieces` — force-write intelligence summary to pieces.md

---

## What makes it good

The normalisation layer is the key insight.
Raw numbers across platforms are meaningless without context.
An 8% engagement rate on Reddit and an 8% engagement rate on Twitter
are completely different things. The resonance score accounts for this.

The "what's working / what isn't" section does the analysis.
Data without interpretation is just numbers.
The skill reads the patterns and surfaces the useful observations.

The per-piece cross-platform view is what creators actually need.
"How did this piece do?" — not "how's my LinkedIn doing?"
Understanding performance by piece reveals what topics and formats resonate.
Understanding performance by platform just reveals which platform you're best at performing on.

The pieces.md log is the long-term value.
After 6 months of data, patterns emerge that aren't visible in any single pull.
The skill surfaces these when asked.
