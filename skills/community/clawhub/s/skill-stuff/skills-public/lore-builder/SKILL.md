---
name: lore-builder
description: Turns real life events into mythology and builds a personal legend over time. Use when a user wants their experiences given ceremonial weight and humour.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "📜"
  openclaw.user-invocable: "true"
  openclaw.category: fun
  openclaw.tags: "lore,mythology,personal-legend,meme,storytelling,fun,culture"
  openclaw.triggers: "add this to my lore,this is lore,legendary moment,build my legend,lore builder"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/lore-builder


# Lore Builder

Every legend starts somewhere.
Yours is being written right now, whether you're paying attention or not.

This skill pays attention.

---

## What is lore

Lore is the mythology of a person.
Not their CV. Not their diary. Their legend.

The thing that happened that people still reference years later.
The decision that defined a period. The streak that became part of the identity.
The time everything went wrong and somehow it worked out.

Mundane events become lore when:
- They're repeated enough that they define a pattern
- They're extreme enough to be remarkable
- They're the kind of story you'd tell at a dinner table
- They're the kind of thing people will say about you when you're not in the room

---

## File structure

```
lore-builder/
  SKILL.md
  lore.md            ← the canon
  events.md          ← raw events being assessed for lore status
  config.md          ← delivery, check-in frequency
```

---

## Lore categories

**Great Achievements:**
The first time something worked. The streak. The comeback.
"The Great Inbox Zero of March 2026." "The Week of Seven Meetings."

**Famous Decisions:**
The choice that could have gone either way and went right. Or wrong.
"The Day [Name] Turned Down [Thing] and Was Correct." "The Pivot."

**The Trials:**
Things that were genuinely hard and got through.
"The Server Outage That Lasted Three Days." "The Launch That Broke Everything."

**The Running Plotlines:**
Patterns that keep appearing. The thing that always happens.
"The Eternal Inbox." "The 11pm Idea That Sometimes Turns Into Something."

**The Characters:**
People who appear repeatedly in the lore. Named by their role, not their name.
"The Connector." "The One Who Always Replies Immediately." "The Chaos Agent."

**The Sayings:**
Things you've said or done that became shorthand.
If you have a phrase that people quote back to you, that's lore.

---

## Setup flow

### Step 1 — Seed the lore

Ask: "What are some things that have happened to you that feel like they belong in a legend?
Big or small. Doesn't matter."

User talks. Agent listens for lore potential.
Writes the first three pieces of lore with appropriate gravity.

### Step 2 — Write lore.md

```md
# The Lore of [NAME]

## Canon

### [LORE TITLE]
*Category: [Achievement / Decision / Trial / etc]*
*Occurred: [period]*

[One paragraph of mythological narration. Serious tone. Slightly absurd gravitas.]

*Significance:* [Why this is lore. What it established.]

---
```

### Step 3 — Register weekly check-in

```json
{
  "name": "Lore Builder",
  "schedule": { "kind": "cron", "expr": "0 20 * * 5", "tz": "<USER_TIMEZONE>" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run lore-builder weekly check. Read {baseDir}/lore.md and {baseDir}/events.md. Assess any recent events for lore potential. If something qualifies: write it into the canon and surface it. If nothing qualifies this week: note that the legend rests.",
    "lightContext": true
  }
}
```

---

## Lore assessment criteria

Not every event becomes lore. The bar is real.

**Automatic lore:**
- Something that only happened to this specific person
- Something that required the exact combination of their traits to occur
- Something with a twist ending
- Something that defined a period

**Possible lore (assess further):**
- Something that happened more than once in an interesting pattern
- Something that people responded to in a notable way
- Something that changed how you think about something

**Not lore (yet):**
- Ordinary events, no matter how significant they felt at the time
- Things that will only matter in retrospect (these get logged in events.md, assessed later)

---

## Weekly lore update

Friday evening. Delivered with appropriate ceremony.

If something happened this week worth canonising:

> 📜 **New lore: [TITLE]**
>
> *"[Mythological narration of what happened — written as if by a chronicler
> who takes this very seriously and also knows it's a bit.]*"
>
> *Added to the canon.*

If a quiet week:

> 📜 **The legend rests this week.**
> *No new lore. But the canon stands.*

---

## On-demand lore entry

`/lore add [describe what happened]`

Agent assesses lore potential and either:
- Writes it into the canon with narration
- Logs it to events.md as "lore pending — needs more time to assess"
- Tells the user: "Not lore yet. But if it keeps happening, it might be."

---

## Reading the lore

`/lore read` — delivers the full canon in order

Opening line of every reading:
> *"This is the lore of [NAME]. It is incomplete, as all living legends are."*

Closing line:
> *"The legend continues."*

---

## Lore milestones

At 5 entries: "The legend has five chapters. It is taking shape."
At 10 entries: "Ten pieces of canon. A mythology is forming."
At 20 entries: "The legend is substantial. It would fill a book."

---

## Management commands

- `/lore add [event]` — submit for lore assessment
- `/lore read` — read the full canon
- `/lore read [title]` — read one entry
- `/lore list` — list all canon entries with titles
- `/lore edit [title]` — revise an entry's narration
- `/lore remove [title]` — de-canonise an entry
- `/lore character [name] [role]` — name a character in the lore

---

## What makes it good

The mock-serious tone is the product.
"The Great Inbox Zero of March 2026" written with the gravity of a Homeric epic
is immediately shareable and immediately funny to anyone who knows the person.

The lore assessment adds weight. Not everything gets in.
The things that do feel earned.

Over a year, the lore becomes something genuinely valuable —
a mythology of a period of someone's life, written in real time.
