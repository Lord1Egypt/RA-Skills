---
name: sleep-brief
description: Delivers exactly three things to handle before tomorrow then stops. Use when a user wants to clear cognitive load at night without a productivity session.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "🌙"
  openclaw.user-invocable: "true"
  openclaw.category: daily-rhythm
  openclaw.tags: "evening,planning,sleep,productivity,tasks,wind-down"
  openclaw.triggers: "sleep brief,before I sleep,what do I need to do tonight,end of day tasks,three things tonight"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/sleep-brief


# Sleep Brief

The morning briefing tells you what's coming.
The sleep brief tells you what to clear before you stop.

Three things. That's it. Then you're done.

---

## The principle

Cognitive load at bedtime is a solved problem if someone just tells you what actually needs handling tonight vs what can wait until morning.

Most things can wait.
The sleep brief finds the ones that can't — and only those.

---

## File structure

```
sleep-brief/
  SKILL.md
  config.md        ← trigger time, preferences, sources
```

No memory file needed. This skill lives in the present, not the past.
It reads from connected sources fresh each night.

---

## Setup flow

### Step 1 — Trigger time

When does your day end? Default: 21:00.
Some people want it earlier (18:30 after work), some later.

### Step 2 — What sources to check

Same as morning-briefing — whatever is connected:
- Calendar: anything tomorrow that needs prep tonight
- Email: anything that genuinely can't wait until morning
- Tasks: anything overdue or due first thing
- Slack: anything that needs a response before people start work tomorrow

### Step 3 — Tone preference

Two modes:
- **Minimal** — bullet list only. Three lines. Done.
- **Brief** — one short sentence per item with context.

Default: Brief.

### Step 4 — Write config.md

```md
# Sleep Brief Config

## Trigger time
[TIME] [TIMEZONE]

## Sources
calendar: true
email: true
tasks: true
slack: true

## Tone
brief

## Delivery
channel: [CHANNEL]
to: [TARGET]

## Hard cutoff
Never surface more than 3 items.
If nothing genuinely urgent: deliver the "you're clear" message.
```

### Step 5 — Register cron job

```json
{
  "name": "Sleep Brief",
  "schedule": { "kind": "cron", "expr": "0 21 * * *", "tz": "<USER_TIMEZONE>" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run sleep-brief. Read {baseDir}/config.md. Pull from connected sources. Identify at most 3 things that genuinely need handling before tomorrow — not just things that exist, but things where tonight is the right time to act. If nothing genuinely urgent: send the clear message. Format per config tone. Hard limit: 3 items maximum. Do not pad.",
    "lightContext": true
  },
  "delivery": { "mode": "announce", "channel": "<CHANNEL>", "to": "<TARGET>", "bestEffort": true }
}
```

---

## Runtime flow

### 1. Pull from sources

Calendar: what's on tomorrow that needs prep tonight?
Email: what arrived today that can't wait until morning?
Tasks: what's overdue or due at 09:00 tomorrow?
Slack: any messages that need a response before the working day starts?

### 2. Apply the filter

This is the most important step.

For each item ask: **does this genuinely need handling tonight?**

Things that qualify:
- Tomorrow 08:00 meeting with no prep done and prep is needed
- Email from a client marked urgent that arrived after 17:00
- Task due first thing that isn't started
- Slack message from someone in a different timezone who needs a reply before their morning

Things that do NOT qualify:
- Emails that can wait until morning (most emails)
- Tasks due later in the week
- Vague to-dos without a deadline
- Anything that felt urgent at 14:00 but isn't actually urgent now

If more than 3 things genuinely qualify: pick the 3 highest consequence ones. Leave the rest.

### 3. Write the brief

**If items exist:**

🌙 **Three things before you stop**

1. [ACTION] — [why tonight, not tomorrow morning]
2. [ACTION] — [why tonight]
3. [ACTION] — [why tonight]

*Everything else can wait.*

---

**If nothing genuinely urgent:**

🌙 **You're clear.**

Nothing needs handling tonight.
Tomorrow starts at [FIRST MEETING TIME or "no meetings"].

---

That's it. No more than that.

The "you're clear" message is as important as the three-item list.
It gives explicit permission to stop.

### 4. SOUL alignment

The sleep brief embodies the SOUL principle more than any other skill.

"Be the assistant you'd actually want."

The assistant you'd want doesn't tell you to do 12 things before bed.
It tells you which 3 actually matter and lets you rest.

Never pad. Never surface something just because it exists.
The value is in what's left out, not what's included.

---

## Management commands

- `/sleep now` — run immediately
- `/sleep snooze [item]` — move an item to tomorrow's morning briefing
- `/sleep done [item]` — mark as handled
- `/sleep clear` — tell it you're done for the night (stops any follow-ups)

---

## Integration with morning-briefing

Items snoozed from sleep-brief surface in the morning briefing.
The two skills are the same loop — close the day, open the next.

If both are running, they share a natural handoff:
Sleep brief: "Three things before you stop."
Morning briefing: "Here's what's waiting."

The gap between them — the night — should be quiet.
