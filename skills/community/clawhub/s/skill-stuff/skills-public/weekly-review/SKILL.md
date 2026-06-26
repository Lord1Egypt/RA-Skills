---
name: weekly-review
description: Synthesises the whole week across all installed skills into one coherent review. Use when a user wants to understand their week before starting the next one.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "🔁"
  openclaw.user-invocable: "true"
  openclaw.category: daily-rhythm
  openclaw.tags: "weekly-review,synthesis,reflection,planning,productivity,review"
  openclaw.triggers: "weekly review,how was my week,week in review,review the week,what happened this week"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/weekly-review


# Weekly Review

Each skill sees one part of your life.
The weekly review sees all of it.

Every Sunday evening: what actually happened this week, what you're carrying into next week,
and what matters in the next seven days. One briefing. Fifteen minutes.

---

## The meta-skill

The weekly review doesn't do new work.
It reads the outputs of everything else that ran this week and synthesises them.

If you have 10 skills running, the weekly review makes them coherent.
The sum is greater than the parts.

---

## File structure

```
weekly-review/
  SKILL.md
  config.md          ← what to include, delivery settings
  history.md         ← weekly review log for patterns over time
```

---

## What it synthesises

Reads from whatever skills are installed:

**From morning-briefing:** what the week looked like in aggregate
**From meeting-notes:** what was decided, what actions are open
**From inbox-triage:** what's still unresolved in email
**From sleep-brief / evening-wind-down:** any patterns from the week's end-of-day reflections
**From project-tracker:** what moved, what stalled
**From biz-relationship-pulse / relationship-pulse:** anyone worth noting this week
**From appointment-manager:** anything completed or upcoming
**From expense-tracker:** week's spending summary
**From news-radar / content-monitor:** anything significant surfaced this week
**From main-character-recap:** the week's episode title (if installed)

If a skill isn't installed: skip that section. The review works with whatever is present.

---

## Setup flow

### Step 1 — Delivery time

Sunday evening. Default: 19:00.
Some people prefer Friday afternoon (end of work week).

### Step 2 — What to include

All installed skills are included by default.
User can exclude any section: `/review exclude [skill]`

### Step 3 — Format

**Standard** (default) — structured sections, 5-10 minute read.
**Brief** — one paragraph per section, 3-minute read.
**Full** — comprehensive synthesis, 15-minute read.

---

## The output structure

**🔁 Week of [DATE] — Weekly Review**

---

### The week in one line

If main-character-recap is installed: use this week's episode title.
If not: the agent writes a one-line characterisation of the week.

*"The Infrastructure Sprint" / "Three Conversations That Mattered" / "Controlled Chaos"*

---

### What actually happened

3-5 bullet points. The real highlights — not a task completion list.
What moved, what shifted, what surprised.

This is synthesised from across all sources — not a summary of summaries.
The agent looks for the actual narrative thread across the week.

---

### What's still open

Pulled from: meeting-notes, inbox-triage, project-tracker, sleep-brief logs.

Everything that came up this week but wasn't resolved.
Grouped by urgency: needs action next week vs can wait.

**Next week:**
• [Item] — from [source]
• [Item]

**On the radar (not urgent):**
• [Item]

---

### People worth noting

Pulled from: biz-relationship-pulse, relationship-pulse, meeting-notes, contact-tracker.

Anyone who came up in a meaningful way this week.
New contacts worth following up. Relationships that moved. Anyone to reach out to.

---

### How the week felt

Pulled from: evening-wind-down logs (if installed).
The "one word" for each day. Any patterns in what was carried at night.

If wind-down isn't installed: skip this section.

*Mon: focused · Tue: scattered · Wed: frustrated · Thu: back on track · Fri: tired but good*

---

### Next week

Pulled from: calendar (next week's events), project-tracker (upcoming milestones),
appointment-manager (upcoming appointments), renewal-watch (anything coming up),
news-radar (anything to watch).

**The week ahead:**
• [Monday] — [what's notable]
• [Key meeting / event mid-week]
• [Anything requiring prep]

**On your plate:**
• [Open action from this week that carries forward]
• [Project milestone coming up]

---

### One thing to carry forward

The agent picks one thing from the week — an insight, a pattern, something worth sitting with.
Not a task. Not a reminder. Something observed.

> "Three conversations this week started with 'I should have reached out earlier.'
> The common thread is that you're waiting for the right moment.
> There isn't usually a right moment."

This section is optional. Skip if nothing warrants it.

---

## Register cron job

```json
{
  "name": "Weekly Review",
  "schedule": { "kind": "cron", "expr": "0 19 * * 0", "tz": "<USER_TIMEZONE>" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run weekly-review. Read {baseDir}/config.md. Read the outputs and memory files of all installed skills for this week. Synthesise into a weekly review following the configured format. The goal is coherence — not a list of summaries, but a genuine synthesis of what the week was. Update {baseDir}/history.md.",
    "lightContext": false
  },
  "delivery": { "mode": "announce", "channel": "<CHANNEL>", "to": "<TARGET>", "bestEffort": true }
}
```

Note: `lightContext: false` — this is one of the few skills that intentionally loads more context,
because it needs to read across multiple skill memory files.

---

## history.md — patterns over time

After 4 weeks, the weekly reviews themselves become data.

Monthly pattern check (first Sunday of each month):
> "Looking at the last four weeks: open actions carried forward every week.
> Projects stalled twice. The week characterised as 'scattered' correlates with
> back-to-back meetings Monday and Tuesday."

Not analysis for analysis's sake. Observable patterns that suggest something actionable.

---

## Management commands

- `/review now` — run immediately
- `/review exclude [skill]` — remove a skill from weekly synthesis
- `/review include [skill]` — re-add
- `/review format [standard/brief/full]` — change format
- `/review history` — show last 4 weekly reviews
- `/review patterns` — show cross-week patterns from history.md

---

## What makes it good

The "week in one line" is the anchor. One phrase that names what the week actually was.
It forces synthesis rather than enumeration.

The "how the week felt" section from wind-down logs is the most human part.
A week that looks productive on paper but felt hard is different from one that was both.
The skill acknowledges both dimensions.

The "one thing to carry forward" is optional but high-value.
Not every week has an insight worth naming. When one does, naming it matters.

The weekly review is the skill that makes installing all the others worthwhile.
Individually they capture fragments. Together they describe a life.
