---
name: news-radar
description: Delivers daily briefings on specific topics, companies, and industries the user tracks. Use when a user wants relevant signal without the noise of a general news feed.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
allowed-tools: web_search web_fetch
metadata:
  openclaw.emoji: "📡"
  openclaw.user-invocable: "true"
  openclaw.category: intelligence
  openclaw.tags: "news,monitoring,industry,topics,alerts,daily,research"
  openclaw.triggers: "track the news about,news radar,keep me informed about,daily news,what's happening with,industry news"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/news-radar


# News Radar

General news apps give you what's popular.
This gives you what's relevant to you specifically.

---

## The difference

Morning briefing → your day (calendar, email, tasks)
News radar → your world (topics, companies, people, industries you track)

They're complementary. Morning briefing is operational. News radar is intelligence.

---

## File structure

```
news-radar/
  SKILL.md
  topics.md          ← what to track, with context and importance weight
  config.md          ← delivery, frequency, format
  history.md         ← surfaced stories (avoid repeats)
```

---

## What to track

Topics can be anything:
- A company ("anything about Anthropic")
- An industry ("European fintech regulation")
- A person ("what is Jensen Huang saying publicly")
- A technology ("agentic AI developments")
- A theme ("remote work trends")
- A geography ("Berlin startup scene")
- A specific situation ("the OpenAI / Apple partnership")

Each topic has:
- A name and description
- An importance weight (high / medium / low)
- Alert threshold (any news, or only significant news)

---

## Setup flow

### Step 1 — What to track

Ask: "What topics, companies, or people do you want to stay informed about?"
Let them list freely. Don't impose structure.

Then ask: "For each one — do you want everything, or only the significant stuff?"

### Step 2 — Format preference

- **Headlines only** — topic + one sentence. Fastest to read.
- **Brief** — topic + 2-3 sentence summary. Default.
- **Deep** — topic + full synthesis of multiple sources. For high-importance topics.

Different topics can have different formats.

### Step 3 — Delivery

Default: every morning as part of morning-briefing (integrates cleanly).
Or: standalone delivery at a different time.
Or: only when something significant happens (event-driven, not daily).

### Step 4 — Write topics.md

```md
# Topics

## [TOPIC NAME]
Description: [what to watch for]
Importance: high / medium / low
Alert on: everything / significant only
Format: headlines / brief / deep
Notes: [any context that helps filter relevance]
```

---

## Runtime flow

### Daily scan

For each topic in topics.md:
1. web_search with targeted query for that topic
2. Check multiple sources (not just one outlet)
3. Filter for genuinely new information (check history.md)
4. Assess significance: is this worth surfacing today?

Significance filter:
- High-importance topics: surface if anything new in last 24h
- Medium topics: surface if something notable (not routine updates)
- Low topics: surface only if something significant happened

### Deduplication

Check history.md. Don't surface the same story twice.
If a developing story gets a meaningful update: surface the update, not the original again.

### Build the briefing

**📡 News Radar — [DATE]**

---

**[TOPIC]** — [source] · [time ago]
[2-3 sentence summary]
*Why it matters:* [one sentence on significance — optional for obvious stories]
[Read more →](link)

---

If nothing significant on a topic: skip it. Don't pad.
If nothing significant on any topic: send a brief "nothing notable today" or skip entirely (user preference).

### Update history.md

Log each surfaced story with URL and date.

---

## Event-driven alerts

For high-importance topics, optionally enable immediate alerts (not just daily).

Configure per topic:
```md
alert_immediately: true
```

When a significant development is detected (via poll or hook):
→ Send an immediate alert regardless of daily schedule.

---

## Management commands

- `/radar add [topic]` — add new topic interactively
- `/radar remove [topic]` — remove topic
- `/radar now` — run scan immediately
- `/radar topics` — list all tracked topics with importance
- `/radar weight [topic] [high/medium/low]` — change importance
- `/radar format [topic] [headlines/brief/deep]` — change format
- `/radar history [topic]` — show recent stories for a topic

---

## Integration with morning-briefing

If both skills are running, news-radar feeds into morning-briefing automatically.
The morning-briefing skill checks for a news-radar output and includes it as a section.

This means one delivery instead of two. Cleaner.

---

## What makes it good

Specificity is everything. "European fintech regulation" beats "fintech news."
The setup conversation is where the skill earns its value — the more specific the topics,
the more useful the output.

The significance filter prevents daily noise on slow-moving topics.
A topic with nothing meaningful happening shouldn't generate a briefing.

Multiple sources per story matter. One outlet's spin vs the actual picture are different things.
Always check at least two sources before surfacing a story.
