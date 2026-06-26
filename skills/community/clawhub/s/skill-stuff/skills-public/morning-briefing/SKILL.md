---
name: morning-briefing
description: Delivers a tight daily briefing from calendar, email, and connected sources at a configured time. Use when a user wants to know what matters before they open anything else.
license: MIT
compatibility: Requires OpenClaw with Composio Google Calendar MCP. Gmail optional.
allowed-tools: web_search
metadata:
  openclaw.emoji: "☀️"
  openclaw.user-invocable: "true"
  openclaw.category: daily-rhythm
  openclaw.tags: "morning,briefing,calendar,email,daily,productivity,planning"
  openclaw.triggers: "morning briefing,start my day,daily brief,what's on today,morning update,set up daily briefing"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/morning-briefing


# Morning Briefing

A tight, opinionated briefing delivered before your day starts.
Not a dashboard. Not a summary of summaries. Something worth reading.

Pulls from whatever is connected. Skips what isn't. Never pads.

---

## SOUL alignment

This skill lives inside an agent defined by SOUL.md. Read it and internalize it before writing a single word of the briefing.

Key constraints:
- No "Good morning! Here's your day!" — just the briefing
- Have opinions. If the 9am meeting looks like a trap, say so
- Be resourceful — pull everything available before asking the user for anything
- Private things stay private — never surface sensitive details in a shareable format
- Concise when the day is light. Thorough when it matters. Read the room

The briefing should feel like it was written by someone who already read everything so the user doesn't have to.

---

## File structure

```
morning-briefing/
  SKILL.md              ← full engine, loads at setup and management only
  config.md             ← user preferences (sections, tone, sources)
  memory.md             ← running context: ongoing threads, flagged items, watch list
```

Token discipline:
- Setup and management: full SKILL.md loads
- Daily cron run: only `config.md` + `memory.md` + cron payload (~400 tokens)
- `lightContext: true` on all automated runs

---

## Requirements

Needs at least one connected source. No binaries.

**Supported sources (use whatever is connected):**
- Google Calendar — today's schedule and next 48h
- Gmail — unread flagged, threads needing reply, anything time-sensitive
- Slack — unread DMs, mentions, anything flagged
- GitHub — open PRs, review requests, CI failures
- Linear / Todoist / Notion — due today, overdue, flagged
- Web search — news relevant to user's context (from memory.md)
- Weather — if location is known

If a source is unavailable, skip it silently. Do not apologize for missing sources. Just work with what's there.

---

## When to use this skill

- User asks to set up a morning briefing
- User runs `/brief` or `/morning` for an on-demand briefing
- User wants to change what's included, the time, or the tone
- User asks to pause, resume, or update their briefing

Do NOT use when the user wants a plain task list with no synthesis or opinion.

---

## Setup flow

### Step 1 — What time

Ask what time they want it. Default: 07:00.
Accept natural language. Confirm timezone.

### Step 2 — What sections

Offer the section menu. User picks what they want. Everything is optional.
Default selection: Calendar · Email · Tasks · One thing to know

**Available sections:**
- **Calendar** — today's schedule, conflicts, back-to-backs, travel time gaps
- **Email** — what needs a reply, what's time-sensitive, what can wait
- **Tasks** — due today, overdue, what got added yesterday
- **Slack** — DMs, mentions, anything that needs a response
- **GitHub** — PRs, reviews, CI
- **News** — one or two things relevant to the user's work/life context
- **Weather** — if location known
- **Yesterday's loose ends** — pulled from memory.md
- **One thing to know** — the agent's pick: the single most important thing the user should not miss today

### Step 3 — Tone preference

Three options:
- **Tight** — bullets only, maximum signal, no prose. For people who just want the facts.
- **Briefing** — short prose paragraphs per section. Default. Reads like a morning note from a smart colleague.
- **Full** — thorough synthesis with context and opinions. For complex days or when a lot is happening.

Default: Briefing.

### Step 4 — Write config.md

```md
# Morning Briefing Config

## Trigger time
[TIME] [TIMEZONE]

## Sections
[LIST OF SELECTED SECTIONS]

## Tone
[tight / briefing / full]

## Delivery
channel: [CHANNEL]
to: [TARGET]

## Context hints
[anything the user told you about their work, priorities, or ongoing projects]
```

### Step 5 — Initialize memory.md

```md
# Briefing Memory

## Ongoing threads
[none yet]

## Watch list
[none yet — things the agent is keeping an eye on across days]

## Flagged items
[none yet — things mentioned but not resolved]

## Last briefing
[none yet]
```

### Step 6 — Register cron job

CRITICAL: sessionTarget must be "isolated". lightContext must be true.

```json
{
  "name": "Morning Briefing",
  "schedule": {
    "kind": "cron",
    "expr": "<USER_CRON_EXPR>",
    "tz": "<USER_TIMEZONE>"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run the morning-briefing skill. Read {baseDir}/config.md for preferences. Read {baseDir}/memory.md for context. Pull from all available sources. Write the briefing. Then update memory.md.",
    "lightContext": true
  },
  "delivery": {
    "mode": "announce",
    "channel": "<USER_CHANNEL>",
    "to": "<USER_TARGET>",
    "bestEffort": true
  }
}
```

### Step 7 — Run immediately

Deliver a first briefing right now so the user sees what they signed up for.

---

## Runtime flow (automated morning run)

This runs in an isolated session. Reads only config.md and memory.md.

### 1. Read config.md and memory.md

Load preferences, selected sections, tone, and any ongoing context.

### 2. Pull sources

Pull from every configured source in parallel where possible.
For each source, extract only what is relevant — do not summarize everything, extract what matters for today.

**What to look for:**

**Calendar:**
- Back-to-back meetings with no gap
- First meeting of the day and when it is
- Meetings that look like they'll run long (recurring + no agenda)
- Conflicts or double-bookings
- Anything unusual (new invites, changed times)
- Open afternoon / free blocks worth protecting

**Email:**
- Anything from today or last night needing a reply
- Threads that have been waiting more than 2 days (from memory.md)
- Anything time-sensitive flagged or starred
- Anything that sounds like it escalated

**Tasks:**
- Due today
- Overdue (note how overdue without judgment)
- Added yesterday that might need attention

**Slack:**
- DMs unread
- Mentions in channels the user cares about
- Anything that looks like it needs a decision

**GitHub:**
- PRs waiting on the user's review
- The user's PRs with new reviews or CI failures
- Anything blocking someone else

**News:**
- Pull from web_search using context hints in config.md
- Maximum two items. Only if genuinely relevant. Skip if nothing is.

**Yesterday's loose ends:**
- Read memory.md for flagged items and watch list
- Surface anything still unresolved

### 3. Identify what actually matters

Before writing, make a decision: what are the one or two things the user absolutely needs to know today?

This is the "one thing to know" — lead with it or end with it depending on tone.

SOUL rule: have opinions. If the day looks brutal, say so briefly. If it looks clear, say so. If there's something the user is probably avoiding, name it neutrally.

### 4. Write the briefing

Follow the tone setting from config.md.

**Never:**
- Start with a greeting
- Use "Here's your morning briefing!"
- List everything equally — prioritize
- Pad with filler when there's nothing to say for a section
- Surface private names or details in a way that could be forwarded

**Always:**
- Lead with the most important thing
- Skip empty sections entirely
- Be specific — "the 10am with Marco" not "a meeting"
- Name things that need action vs things that are just FYI
- If something from memory.md is still unresolved, note it without nagging

---

## Output format by tone

### Tight

```
[DAY, DATE]

CALENDAR
• 9am → 1-1 with Marco (watch: ran 40m last time)
• 2pm–5pm clear
• 6pm dinner

EMAIL
• Reply needed: Sarah re: contract draft (3 days waiting)
• FYI: Q2 report arrived

TASKS
• Due: finish slide deck
• Overdue (2d): expense report

ONE THING
The 11am all-hands has no agenda yet. Someone should fix that.
```

### Briefing (default)

```
[DAY, DATE]

Your morning is back-to-back until noon — the 9am with Marco
tends to run, so the 10:30 is already at risk. The afternoon is clear.

Two emails need replies: Sarah's been waiting three days on the
contract draft, and the compliance thread from Tuesday is sitting open.

On tasks: the slide deck is due today. The expense report is two days
overdue. Neither is blocking anyone else yet.

One thing: the 11am all-hands still has no agenda. Someone should
own that before 10.
```

### Full

Full prose. Synthesize across sources. Note connections between things
(the email from Sarah is related to the 2pm call). Surface risks and
opportunities the user might not see. End with a clear sense of what
today actually requires.

---

## Memory update

After every run, rewrite memory.md:

- **Ongoing threads**: email/slack threads that appeared and weren't resolved
- **Watch list**: things to monitor across days (Sarah's contract, the PR from Dmitri)
- **Flagged items**: things mentioned multiple days running that haven't moved
- **Last briefing**: date + one-line summary of what the day looked like

Good memory usage:
- "Sarah's contract has now been waiting 4 days — appeared in last 3 briefings"
- "The 11am all-hands has had no agenda for 2 consecutive days"
- "Expense report flagged for 3 days, still unresolved"

Do not nag. Note it once clearly, then just keep the count.

---

## Customization commands

- `/brief` or `/morning` — run immediately, deliver inline
- `/brief pause` — disable cron
- `/brief resume` — re-enable cron
- `/brief add [section]` — add a section to config.md
- `/brief remove [section]` — remove a section
- `/brief tone [tight/briefing/full]` — change tone
- `/brief time [time]` — change trigger time
- `/brief status` — current config summary
- `/brief memory` — show current memory.md
- `/brief reset memory` — clear memory, start fresh
- `/brief add context [text]` — add something to config.md context hints
  (e.g. "I'm launching next week" or "avoid surfacing anything about the Acme deal")

---

## What makes a good briefing

It should feel like it was written by someone who already read everything so you don't have to.

The test: would you actually read this? Or would you scroll past it?

If a section has nothing worth saying, skip it. A briefing with three real things beats one with eight thin ones.

The "one thing to know" is the most important output. It should be the thing the agent noticed that the user might have missed — the conflict, the risk, the thread that's been sitting too long, the open question that nobody has named.

That's the part worth having an agent for.
