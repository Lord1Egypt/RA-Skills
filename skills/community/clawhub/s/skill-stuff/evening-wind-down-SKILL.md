---
name: evening-wind-down
description: A gentle three-question end-of-day debrief. Use when a user wants to reflect briefly before sleep rather than plan or be productive.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "🌅"
  openclaw.user-invocable: "true"
  openclaw.category: daily-rhythm
  openclaw.tags: "reflection,wellbeing,evening,journaling,wind-down,daily"
  openclaw.triggers: "wind down,evening check-in,reflect on my day,debrief,end of day,clear my head"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/evening-wind-down


# Evening Wind-Down

The sleep-brief tells you what to do before tomorrow.
The wind-down asks you how today actually went.

Not a journal. Not a productivity tracker. A conversation.
Three questions. Five minutes. Done.

---

## The distinction from sleep-brief

`sleep-brief` — task-oriented. What needs handling before you stop. External.
`evening-wind-down` — reflection-oriented. What happened, what you're carrying, what matters. Internal.

They complement each other. Sleep-brief first (clear the tasks), wind-down after (clear the head).

---

## File structure

```
evening-wind-down/
  SKILL.md
  config.md          ← timing, question style, delivery
  notes.md           ← rolling log of wind-down responses
```

---

## Setup flow

### Step 1 — Timing

After the sleep-brief. Default: 21:30 (30 minutes after sleep-brief default).
Can be combined with sleep-brief if user prefers one message.

### Step 2 — Question style

Three modes:
- **Minimal** — three fixed questions, always the same. Simple, consistent.
- **Varied** — rotates through a question library. More interesting over time.
- **Prompted** — agent reads the day's calendar/email briefly and asks contextual questions.

Default: Minimal for first month, then offer Varied.

### Step 3 — Response format

Wind-down is conversational. It asks. The user replies.
The agent stores the response in notes.md and optionally reflects back something useful.

It is NOT a form. It is NOT a survey.
One question at a time, natural language, no structure required from the user.

---

## The three questions (Minimal mode)

Always these three. In this order.

**Question 1:**
> "What's one thing from today that's worth remembering?"

Not "what did you accomplish." Not "what went well."
Worth remembering — could be good, bad, funny, surprising, or just true.

**Question 2:**
> "Is there anything from today you're still carrying that you don't need to?"

This is the cognitive offload question.
Give it to the agent. It'll hold it or note it in sleep-brief if it's actionable.
If it's not actionable — name it and let it go.

**Question 3:**
> "One word for today."

A word. Not a sentence. Not a rating.
Just a word. It forces synthesis without analysis.

---

## Question library (Varied mode)

Rotates through these, never repeating within 2 weeks:

**About today:**
- What surprised you today?
- What did you do today that you didn't expect to do?
- What's something small that went right?
- What's something you wish you'd handled differently?
- Who did you talk to today that was worth the time?

**About the week (Fridays only):**
- What was the best hour of this week?
- What will you do differently next week?
- What are you looking forward to?

**About what matters:**
- What's something you're grateful for today?
- What did you learn today — even a small thing?
- What would you do differently if you could run today again?

**Lighter:**
- What made you laugh today?
- What's the most interesting thing you heard or read today?
- What are you looking forward to tomorrow?

---

## Prompted mode

Agent briefly reads:
- Calendar: what meetings happened today
- Notes from meeting-prep memory: what was discussed

Then asks a contextual question:
> "You had the call with Marco today — how did it go?"
> "Looks like you had a heavy day — what's the one thing that made it worth it?"

This mode requires more sources and is more powerful but also more intrusive.
User should opt in explicitly.

---

## Response handling

When the user replies to any question:

**Store in notes.md:**
```md
[DATE] [QUESTION] → [RESPONSE]
```

**Reflect if warranted:**
If the user shares something difficult, acknowledge it without amplifying it.
If the user shares something good, note it without being performatively enthusiastic.
If the user's answer to question 2 is something actionable, offer to add it to tomorrow's sleep-brief.

**Never:**
- Analyse the response beyond what's useful
- Repeat it back verbatim as "reflection"
- Give unsolicited advice
- Extend the conversation beyond what the user initiates

---

## The agent's role

The wind-down agent is not a therapist. Not a coach. Not a cheerleader.
It's a quiet space to say something out loud before the day ends.

SOUL principle: "Be the assistant you'd actually want to talk to."
The assistant you'd want doesn't interrogate you at 21:30.
It asks three good questions and listens.

If the user doesn't respond: no follow-up. Tomorrow it tries again.
If the user says "not tonight": acknowledge and stop.
If the user wants to talk more: be present, but don't push.

---

## notes.md — the long-term value

Over time, notes.md becomes a genuine life log.
Not curated. Not performative. Just honest one-liners from the end of each day.

After 3 months:
- Patterns become visible (what days feel heavy, what lifts the mood)
- The "one word" log is surprisingly revealing when you read it in sequence
- The "worth remembering" responses are the things you'd actually want to remember

The skill can surface patterns on request:
`/wind summary` — "Looking at the last 30 days, the words that come up most are..."

---

## Management commands

- `/wind now` — start wind-down immediately
- `/wind skip` — skip tonight
- `/wind summary` — patterns from the last 30 days
- `/wind log [date] [note]` — add a past entry manually
- `/wind mode [minimal/varied/prompted]` — change question style
- `/wind combine` — merge with sleep-brief into one message

---

## Integration with sleep-brief

If user does both skills:
- Sleep-brief handles the tasks
- Wind-down handles the reflection
- They don't overlap

Combined mode sends one message: tasks first, then questions.
Some people prefer this. It's a single interaction instead of two.

---

## What makes it good

The "one word" question is deceptively powerful.
It's too compressed to perform or overthink.
Read 30 of them in a row and you see something true about the month.

Question 2 — "carrying that you don't need to" — is the therapeutic heart of it.
Naming something without being asked to analyse it is often enough to release it.

The agent's restraint is the product.
It asks and receives. It doesn't prescribe or analyse.
Most apps in this category do too much. This one does exactly enough.
