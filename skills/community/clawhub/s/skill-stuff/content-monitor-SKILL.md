---
name: content-monitor
description: Watches specific people, companies, and topics across the web and alerts when something relevant happens. Use when a user needs targeted intelligence on named targets.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
allowed-tools: web_search web_fetch
metadata:
  openclaw.emoji: "👁️"
  openclaw.user-invocable: "true"
  openclaw.category: intelligence
  openclaw.tags: "monitoring,alerts,competitors,companies,people,news,tracking"
  openclaw.triggers: "monitor,watch for,alert me when,keep tabs on,track what they're doing,competitor monitoring"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/content-monitor


# Content Monitor

Google Alerts are too broad and too slow.
This skill watches specific targets and tells you when something actually matters.

---

## The difference from news-radar

`news-radar` — tracks topics and industries. What's happening in [space].
`content-monitor` — tracks specific entities. What is [person/company] doing.

Different granularity. Different use cases. Often run together.

---

## File structure

```
content-monitor/
  SKILL.md
  targets.md         ← what to watch, with context and alert rules
  config.md          ← check frequency, delivery
  history.md         ← surfaced items (avoid repeats)
```

---

## Scope — public content monitoring only

This skill monitors publicly available web content — news articles, blog posts,
press releases, job listings, public social profiles. It does not:
- Scrape private or authenticated content
- Access data behind login walls
- Build profiles on private individuals
- Enable surveillance of people who have not published publicly

Targets should be public figures, companies, or public topics — not private individuals.

---

## What to watch

**People:**
A founder you follow. An investor. A competitor's CEO. A journalist who covers your space.
What to watch for: new posts, interviews, public statements, company changes.

**Companies:**
A competitor. A potential client. A company you're monitoring for partnership or investment.
What to watch for: press releases, job postings (signal for direction), funding news, product launches.

**Specific content types:**
New blog posts from a site. New papers from a research group. New filings from a company.
New episodes of a podcast.

**Regulatory / official:**
New rules from a regulator. New guidance from a government body. Court filings.

---

## Setup flow

### Step 1 — Build the target list

Ask: "Who or what do you want to keep tabs on?"
For each target: what specifically do you want to know about them?

Different targets warrant different alert thresholds:
- High-priority: alert on anything new
- Medium: alert only on significant developments
- Low: weekly summary only

### Step 2 — Write targets.md

```md
# Targets

## [TARGET NAME]
Type: person / company / publication / regulator / other
Watch for: [specific things — "new blog posts", "fundraising news", "public statements", "job postings"]
Importance: high / medium / low
Alert on: everything / significant only / weekly summary
Context: [why you're watching this — helps the agent assess relevance]
Sources to check: [where they post — Twitter/X, LinkedIn, website, etc.]
```

### Step 3 — Write config.md

```md
# Content Monitor Config

## Check frequency
high-importance: every 6 hours
medium: daily
low: weekly

## Delivery
channel: [CHANNEL]
to: [TARGET]

## Silent when
nothing new for medium/low targets
```

### Step 4 — Register cron jobs

```json
{
  "name": "Content Monitor - Daily",
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "<TZ>" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run content-monitor. Read {baseDir}/targets.md, {baseDir}/config.md, {baseDir}/history.md. For each active target: search for new content published since last check. Filter by relevance and importance. Surface significant items. Exit silently if nothing new worth surfacing. Update history.md.",
    "lightContext": true
  }
}
```

---

## Runtime flow

### For each target

1. Run targeted web_search:
   - "[name] site:twitter.com" / "[name] site:linkedin.com"
   - "[company] announcement" / "[company] press release"
   - "[name] interview" / "[name] wrote" / "[name] published"

2. Check publication date — is this new since last check?

3. Check history.md — have we surfaced this already?

4. Assess relevance to the context in targets.md:
   - Is this the kind of thing they asked to be notified about?
   - Is it significant enough given the alert threshold?

5. Surface or skip.

### Alert format

For a single significant item:

> 👁️ **[TARGET NAME]**
> [What happened — one sentence]
> [Source · time ago]
> [Link]
> [One sentence on why this might matter — optional for obvious things]

For a weekly summary of low-importance targets:

> 👁️ **Weekly monitor — [DATE]**
>
> **[TARGET]:** [Brief on what's new]
> **[TARGET]:** [Brief]
> **[TARGET]:** Nothing new this week.

---

## Job posting monitor (company targets)

Optionally track job postings for a company:
New job postings reveal company direction before any announcement does.

"[Company] just posted 3 ML engineer roles" = they're building something.
"[Company] posted a Head of Sales EMEA" = they're expanding.

Enable per target:
```md
monitor_jobs: true
```

When new relevant jobs appear:
> 👁️ **[COMPANY] — new job postings**
> Posted: [N] new roles including [job titles]
> *Signal:* [what this suggests about their direction]

---

## Management commands

- `/monitor add [target]` — add new target interactively
- `/monitor remove [target]` — stop watching
- `/monitor now [target]` — check one target immediately
- `/monitor list` — show all targets with last activity
- `/monitor history [target]` — show recent surfaced items
- `/monitor weight [target] [high/medium/low]` — change importance
- `/monitor jobs [company] on/off` — toggle job posting monitor

---

## What makes it good

The context field in targets.md is the key.
"Watching this founder because we might partner" produces different filtering than
"watching this CEO because they're a competitor."
The agent assesses relevance against the stated reason.

Job posting monitoring is underused intelligence.
Most people discover company directions from press releases.
Job postings reveal it 6 months earlier.

The deduplication via history.md prevents the same story coming up repeatedly
as it gets covered by multiple outlets over a few days.
