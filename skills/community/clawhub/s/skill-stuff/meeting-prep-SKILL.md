---
name: meeting-prep
description: Delivers a briefing before every external meeting covering attendees, last conversation, and open commitments. Use when a user wants to stop walking in unprepared.
license: MIT
compatibility: Requires OpenClaw with Composio Gmail and Google Calendar MCP connected.
allowed-tools: web_search
metadata:
  openclaw.emoji: "📎"
  openclaw.user-invocable: "true"
  openclaw.category: daily-rhythm
  openclaw.tags: "meetings,preparation,briefing,calendar,contacts,professional"
  openclaw.triggers: "prep for my meeting,who is in this meeting,meeting brief,prepare for,what do I know about"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/meeting-prep


# Meeting Prep

Arrives 30 minutes before every external meeting.
Who's in it. Last conversation. What you owe them. What they've been up to.

You show up prepared without doing any preparation.

---

## File structure

```
meeting-prep/
  SKILL.md
  config.md        ← preferences, lead time, what to include
  memory.md        ← past meeting notes, commitments made, people context
```

Token discipline: hook-triggered runs read only `config.md` + `memory.md`.

---

## How it triggers

Two modes. User picks one at setup:

**Hook mode (recommended):** Fires automatically when a calendar event starts approaching. Uses OpenClaw's hooks to watch the calendar and trigger on upcoming events.

**Cron mode:** Runs every morning, identifies external meetings that day, sends prep for each one at the configured lead time.

Default: cron mode (simpler, more reliable). Hook mode for users who want real-time delivery.

---

## Setup flow

### Step 1 — What counts as a meeting worth prepping

Not every calendar event needs prep. Ask:
- Internal standups? (usually no)
- 1-1s with direct reports? (optional)
- External calls, client meetings, new contacts? (yes)
- Everything? (yes if they want it)

Default: prep for any meeting with at least one external attendee, or any meeting flagged with a specific calendar label.

### Step 2 — Lead time

Default: 30 minutes before.
Some people want it the night before for morning meetings.
Ask or default to 30 minutes.

### Step 3 — What to include

Options:
- **Attendee context** — who they are, role, company, recent activity
- **Last conversation** — what was discussed last time
- **Open commitments** — what you said you'd do, what they said they'd do
- **Recent news** — anything notable about their company since you last spoke
- **Agenda** — what the meeting is supposed to be about

Default: all of the above, compressed tightly.

### Step 4 — Sources

What to pull from:
- Google Calendar — event title, attendees, description, location
- Gmail — previous emails with attendees
- Memory.md — past meeting notes stored by the skill
- Web search — recent news about attendee's company (optional, toggle off for private meetings)

### Step 5 — Write config.md

```md
# Meeting Prep Config

## Trigger
mode: cron
check time: 07:00 daily (sends preps at correct lead time throughout day)
lead time: 30 minutes before

## Include
attendee context: true
last conversation: true
open commitments: true
recent company news: true
agenda: true

## Filter
only external meetings: true
minimum attendees: 1
skip recurring internal standups: true

## Delivery
channel: [CHANNEL]
to: [TARGET]

## Web search for company news
enabled: true
skip for: personal / private meetings
```

### Step 6 — Register cron job

```json
{
  "name": "Meeting Prep",
  "schedule": { "kind": "cron", "expr": "0 7 * * 1-5", "tz": "<USER_TIMEZONE>" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run meeting-prep. Read {baseDir}/config.md and {baseDir}/memory.md. Check calendar for today's meetings matching config filters. For each qualifying meeting: calculate prep delivery time (meeting time minus lead time). Generate prep briefing for each. Schedule delivery at correct times using cron or deliver now if meeting is within lead time window. Update memory.md with any new people encountered.",
    "lightContext": true
  },
  "delivery": { "mode": "announce", "channel": "<CHANNEL>", "to": "<TARGET>", "bestEffort": true }
}
```

---

## Runtime flow

### 1. Pull today's calendar

Fetch all events for today.
Filter by config rules (external only, skip standups, etc.)
Sort by start time.

### 2. For each qualifying meeting

**Identify attendees:**
- Parse attendee list from calendar event
- Separate internal (same domain) from external
- Focus context-gathering on external attendees

**Pull context:**
- Gmail: search for email threads with each external attendee
- Memory.md: check for past meeting notes with these people
- Calendar: find previous meetings with same attendees
- Web search (if enabled): search "[attendee name] [company]" for recent news

**Extract what matters:**
- Last conversation: what was the subject, what was discussed, any decisions
- Open commitments: anything said that implies a follow-up ("I'll send that over", "let's discuss next time")
- Company news: funding, new product, leadership change, anything in the last 30 days

### 3. Write the brief

Tight. No padding. Fits on a phone screen.

---

📎 **[MEETING TITLE]** — [TIME] ([X] min)

**Who:** [NAME], [Role] at [Company]
[One sentence about them — what they do, how you know them]

**Last time:** [DATE]
[Two sentences max on what was discussed]

**You owe them:** [if anything]
**They owe you:** [if anything]

**Since then:** [any notable news about them or their company — one line]

**Meeting is about:** [agenda from calendar description, or "no agenda set"]

---

If multiple attendees, lead with the most important external person.
Mention others briefly: "Also joining: [NAME] (CFO)"

### 4. Update memory.md

Add new people encountered.
Log that this meeting was prepped.

### 5. Post-meeting follow-up (optional)

If enabled: 1 hour after meeting end, send a prompt:
"[MEETING TITLE] just ended — anything to log? Commitments made, decisions, next steps?"

User replies in natural language. Agent extracts and stores in memory.md.

---

## Memory system

memory.md grows over time into a genuine relationship log.

```md
# Meeting Memory

## [NAME] — [Company]
Role: [title]
First met: [date]
Last meeting: [date]
Context: [who they are, what you work on together]

### Meeting log
[DATE] — [TOPIC]
Discussed: [brief]
Commitments (you): [any]
Commitments (them): [any]
Follow-up needed: [yes/no and what]
```

The longer this runs, the sharper the briefings become.
After 3 months, it knows your relationships better than you do.

---

## Management commands

- `/prep now [meeting name or time]` — generate prep immediately
- `/prep log [name] [notes]` — log notes from a past meeting
- `/prep commit [name] [commitment]` — log a commitment made
- `/prep done [commitment]` — mark a commitment as completed
- `/prep history [name]` — show all logged meetings with a person
- `/prep skip [meeting]` — skip prep for a specific meeting
- `/prep toggle news` — turn web search for company news on/off

---

## What makes it good

The open commitments section is the most valuable part.
"You said you'd send the proposal by Friday" — that's the thing that would have been forgotten.

The briefing has to be short enough to read in 2 minutes.
If it's longer than that, cut it.

Post-meeting logging is what makes it compound.
Each note makes the next briefing sharper.
A prep skill with 3 months of memory is a different product from one running for a week.
