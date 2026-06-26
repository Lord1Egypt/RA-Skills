---
name: gift-radar
description: Alerts 14 days before birthdays and occasions with specific researched gift ideas. Use when a user wants to stop sending generic gifts or missing occasions.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
allowed-tools: web_search
metadata:
  openclaw.emoji: "🎁"
  openclaw.user-invocable: "true"
  openclaw.category: relationships
  openclaw.tags: "gifts,birthdays,occasions,anniversaries,presents,reminders"
  openclaw.triggers: "birthday coming up,gift ideas,what should I get,occasion reminder,gift for,anniversary"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/gift-radar


# Gift Radar

14 days before any occasion, you get an alert with specific ideas.
Not "a nice candle." Something that fits the person.

Runs daily. Delivers only when something is coming up.

---

## File structure

```
gift-radar/
  SKILL.md
  occasions.md     ← people, dates, relationship context, past gifts
  config.md        ← preferences, budget ranges, delivery settings
```

Token discipline: cron runs read only `occasions.md` + `config.md`. Full SKILL.md loads at setup only.

---

## Setup flow

### Step 1 — Build the occasions list

Pull from:
- Google Calendar — birthdays, anniversaries flagged as recurring
- Contacts — birthday fields if accessible
- User input — "my mum's birthday is March 14, my partner's is November 2"

For each person, also ask or infer:
- Relationship (partner, parent, close friend, colleague)
- Interests, hobbies, things they've mentioned wanting
- Budget range
- Past gifts if known

### Step 2 — Write occasions.md

```md
# Occasions

## [NAME]
Relationship: [partner / parent / close friend / etc]
Date: [recurring date]
Interests: [what they're into]
Budget: [rough range]
Past gifts: [if known]
Notes: [anything else worth knowing]
```

### Step 3 — Write config.md

```md
# Gift Radar Config

## Lead time
Alert 14 days before. Remind again 3 days before if not acknowledged.

## Delivery
channel: [CHANNEL]
to: [TARGET]

## Sources for ideas
web_search: true
```

### Step 4 — Register cron job

Daily check, lightweight, only delivers when something is within 14 days.

```json
{
  "name": "Gift Radar",
  "schedule": { "kind": "cron", "expr": "0 8 * * *", "tz": "<USER_TIMEZONE>" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run gift-radar. Read {baseDir}/occasions.md and {baseDir}/config.md. Check if any occasion is within 14 days. If yes: generate specific, thoughtful gift ideas for that person. If no occasion is coming up, do nothing and exit silently.",
    "lightContext": true
  },
  "delivery": { "mode": "announce", "channel": "<CHANNEL>", "to": "<TARGET>", "bestEffort": true }
}
```

Silent exit when nothing is coming up. No noise on empty days.

---

## Runtime flow

### 1. Check occasions.md

Calculate days until each occasion.
If nothing within 14 days: exit silently, no delivery.
If something within 14 days: proceed.

### 2. Build context for the person

Read their entry from occasions.md:
- Interests
- Budget
- Past gifts (avoid repeating)
- Relationship type
- Any notes

### 3. Generate ideas

Use web_search to find current options — not generic lists from training data.
Search for specific, purchasable things that match the person.

Rules:
- 3-5 ideas, different price points within the budget range
- Each idea needs a reason — why this, why for them
- At least one experience (not just a physical object)
- At least one under £30 / €30 / $30
- Never repeat a past gift
- Never suggest a gift card unless specifically asked

### 4. Format the output

**🎁 [NAME]'s [OCCASION] — [X] days away**

[One sentence about why this matters / who they are]

**Ideas:**

1. **[Item/Experience]** — £[price]
   [Why this fits them specifically]
   [Where to get it or how to book]

2. **[Item/Experience]** — £[price]
   [Why this fits them specifically]

3. **[Item/Experience]** — £[price]
   [Why this fits them specifically — budget-friendly option]

*Also worth considering:* [one left-field idea]

*Reminder:* [date], [X] days away.

### 5. 3-day reminder

If the occasion is within 3 days and there's no record of acknowledgment, send a shorter nudge:
"[NAME]'s [OCCASION] is in [X] days. Did you sort a gift?"

---

## Management commands

- `/gift add [name] [date] [context]` — add a new occasion
- `/gift update [name] [field] [value]` — update details
- `/gift log [name] [gift given]` — record what you actually gave
- `/gift preview [name]` — see ideas for someone now regardless of date
- `/gift list` — show all upcoming occasions in the next 90 days
- `/gift skip [name] [year]` — skip this year's alert for someone

---

## What makes it good

The ideas have to be specific to the person, not to the occasion.
"Spa day" is not a gift idea. It's a category.
"A two-hour ceramics class at [studio near them] — they mentioned wanting to try something hands-on" is a gift idea.

The reason is more important than the item.
A £20 thing with a real reason beats a £100 thing without one.

web_search is essential. Training data goes stale. Prices change. New things exist.
Always search before generating ideas.
