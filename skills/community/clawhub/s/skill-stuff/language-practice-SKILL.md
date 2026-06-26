---
name: language-practice
description: Daily 5-minute language practice woven into your existing routine. Builds on what you struggled with yesterday. No separate app needed. Use when a user is learning a language and wants consistent practice without adding another tool to their life.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "🗣️"
  openclaw.user-invocable: "true"
  openclaw.category: daily-rhythm
  openclaw.tags: "language,learning,practice,vocabulary,grammar,daily,Italian,Spanish,French,German,Portuguese"
  openclaw.triggers: "I'm learning,language practice,practice my Spanish,Italian today,French vocabulary,German practice,daily language,help me learn,language lesson"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/language-practice


# Language Practice

Five minutes a day, woven into your existing routine.
Builds on what you got wrong yesterday.
Requires no separate app.

---

## File structure

```
language-practice/
  SKILL.md
  config.md          ← language, level, focus areas, schedule
  progress.md        ← vocabulary learned, patterns struggled with, streak
```

---

## What makes this different from Duolingo

Duolingo teaches you to want to use Duolingo. The streaks, the gamification,
the owls — they're optimised for engagement, not learning.

This skill is optimised for actual retention:
- Short, daily, consistent — this is what builds a language
- Builds on what you personally struggled with, not a generic curriculum
- Woven into your existing routine rather than a separate app habit
- Adapts to your level and gaps as they develop
- Never shames you for missing a day

---

## Setup flow

### Step 1 — Language and level

Which language?
What's your current level? (rough: none / beginner / conversational / intermediate / advanced)
What do you want to prioritise? (vocabulary / grammar / conversation / reading / all)
Any specific context? (travel to X, business use, personal connection)

### Step 2 — Session format

Default: 5 minutes, delivered as a message to respond to.
Can be set to: 3 minutes (quick), 10 minutes (deeper), or 15 minutes (study mode).

### Step 3 — Delivery time

When do you want your practice? Default: morning, after morning-briefing.
Can be set to any time.

### Step 4 — Write config.md

```md
# Language Practice Config

## Language
target: [Italian / Spanish / French / German / Portuguese / other]
current_level: [beginner / intermediate / advanced]
native: [English]
focus: [vocabulary / grammar / conversation / all]
context: [travel / business / personal / general]

## Session
length: 5 min
delivery_time: 08:15
channel: [CHANNEL]

## Current curriculum position
unit: [tracked automatically]
last_topic: [tracked automatically]
```

### Step 5 — Register cron job

```json
{
  "name": "Language Practice",
  "schedule": { "kind": "cron", "expr": "15 8 * * *", "tz": "<TZ>" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run language-practice. Read {baseDir}/config.md and {baseDir}/progress.md. Generate today's 5-minute practice session. Prioritise any words or patterns from progress.md flagged as struggled-with. Vary the format — don't repeat the same exercise type two days in a row. Deliver as an interactive message.",
    "lightContext": true
  }
}
```

---

## Session formats (rotated daily)

**Vocabulary introduction:**
3-5 new words in context sentences. The user translates or reads.
Saved to progress.md. Tested again in 3 days.

**Recall practice:**
5 words from recent sessions. User translates from their native language.
No peeking. Answer revealed after attempt. Struggled words flagged.

**Grammar pattern:**
One grammar concept (e.g. Italian passato prossimo, Spanish subjunctive).
2-3 example sentences. User fills in the gap.

**Listening/reading:**
A short passage (2-3 sentences) in the target language.
User translates. Agent shows correct version and explains any differences.

**Conversation starter:**
A question in the target language. User responds in the target language.
Agent responds and corrects any errors naturally within the response.

Example for Italian intermediate:

```
🗣️ Italian — today

Recall: how do you say these in Italian?

1. "I had already left when she arrived."
   [try before scrolling]
   ↓
   "Ero già partito quando lei è arrivata." — well done

2. "They've been waiting for an hour."
   [try before scrolling]
   ↓
   "Aspettano da un'ora." — note: Italian uses present tense with "da" here

3. "Would you like to come?"
   ↓
   "Vorresti venire?" — good

Struggled with: the "da + present tense for ongoing actions" pattern.
We'll come back to this tomorrow.

New word today: 'eppure' — "and yet / even so"
"Eppure funziona." (Galileo, allegedly)
```

---

## Progress tracking

progress.md tracks:
- Words introduced (with first seen date and last tested date)
- Words mastered (correct 3+ times without prompting)
- Words struggling (wrong 2+ times — flagged for more frequent review)
- Grammar patterns covered and confidence per pattern
- Total sessions completed

**Spaced repetition (simple):**
- New word: test after 1 day, 3 days, 7 days, 14 days
- If correct each time: graduate to monthly review
- If wrong: reset to 1-day interval

---

## Weekly reflection

Sunday, brief:

```
🗣️ [Language] — week in review

Sessions this week: [N]/7
Words practicing: [N] active, [M] mastered
Grammar patterns: [current focus]

Struggling with: [top 2 patterns from the week]
Mastered this week: [any new words graduated]

Next week will focus more on: [what the skill has noticed needs work]
```

---

## Missing a day

No guilt. No broken streak drama.

If a session is missed: the next session picks up where it left off.
Struggled words that would have been reviewed get pushed to the next day.
That's it.

If multiple days are missed: the session on return asks one question:
"Welcome back — jump straight in, or a quick recap first?"

---


## Privacy rules

Language learning progress and struggles are personal.

**Context boundary:** Practice sessions and progress reports are delivered
only to the owner's private channel. Never surface learning level, errors,
or vocabulary struggles in a group context.

**No external data:** Progress logs stay in the OpenClaw workspace.
Practice content is generated locally — no learning data sent to external services.

---

## Management commands

- `/lang [anything in target language]` — free practice, agent responds and corrects
- `/lang vocab` — show current vocabulary list
- `/lang struggling` — show words and patterns flagged for more practice
- `/lang grammar [topic]` — drill a specific grammar point
- `/lang skip` — skip today without counting as missed
- `/lang progress` — full progress summary
- `/lang level up` — tell it your level has improved
- `/lang pause [days]` — pause practice for travel or busy periods
