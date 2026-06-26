---
name: vibe-check
description: Delivers the day's vibe as a D&D alignment with a specific recommended action. Use when a user wants a quick honest read of what kind of day they are having.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "✨"
  openclaw.user-invocable: "true"
  openclaw.category: fun
  openclaw.tags: "vibe,mood,daily,fun,meme,productivity,alignment"
  openclaw.triggers: "vibe check,what's my vibe,what kind of day is this,daily vibe,chaotic neutral"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/vibe-check


# Vibe Check

Every day has a vibe.
Most people don't know what it is until 11am.

This skill tells you at 8am.
Brief. Accurate. Mildly unhinged.

---

## File structure

```
vibe-check/
  SKILL.md
  config.md          ← delivery time, sources, vibe history
  history.md         ← vibe log
```

---

## The vibe taxonomy

Vibe is assessed on two axes: **energy** and **alignment**.

**Energy:** chaotic / neutral / lawful
**Alignment:** good / neutral / tired

Combined into a D&D-style alignment for the day:

| | Chaotic | Neutral | Lawful |
|---|---|---|---|
| **Good** | Chaotic Productive | Neutral Focused | Lawful Efficient |
| **Neutral** | Chaotic Neutral | True Neutral | Lawful Tired |
| **Tired** | Chaotic Tired | Neutral Tired | Lawful Dead |

Each combination has a distinct character:

**Chaotic Productive:** Energy everywhere. Output happening. Half of it is the right output.
**Chaotic Neutral:** Could go either way. Probably fine. Do not schedule important things.
**Chaotic Tired:** All the chaos, none of the energy. Dangerous. Handle with care.
**Neutral Focused:** A good day. Rare. Appreciate it.
**True Neutral:** Existing. Neither thriving nor struggling. The cereal day.
**Neutral Tired:** Functional but at minimum settings.
**Lawful Efficient:** Everything will get done. You will not enjoy it. But it will be done.
**Lawful Tired:** The things will get done because they must. At some cost.
**Lawful Dead:** Technically present. Battery at 3%.

---

## How vibe is determined

The skill checks available signals:

**Calendar:** What's on today? Back-to-back meetings = lower energy allocation.
First meeting at 8am = lawful by necessity. Free morning = chaotic potential.

**Sleep brief / evening wind-down:** What was carried from yesterday?
Heavy carryover = starts tired. Clean close = better baseline.

**Day of week:** Monday = lawful (whether you like it or not).
Friday afternoon = chaotic neutral, always.
Sunday evening = neutral to lawful tired.

**Main character recap:** Last night's episode title. If it ended on a cliffhanger, today inherits that energy.

If no sources are connected: the skill makes an educated guess based on the day of week and time.
It will still be accurate approximately 60% of the time, which feels about right.

---

## The daily vibe check

**✨ Vibe check — [DATE]**

**Today's vibe: [ALIGNMENT]**
[One sentence characterisation of what this means in practice today]

**Why:** [One sentence on what signals led to this assessment]

**Recommended action:** [One piece of advice, consistently slightly unhinged]

**Forecast:** [One sentence on how the day is likely to go, honest edition]

---

**Examples:**

> ✨ **Vibe check — Monday**
>
> **Today's vibe: Lawful Tired**
> Functional. Compliant. Not happy about it.
>
> **Why:** Five meetings before noon. The sleep brief carried three unresolved items.
>
> **Recommended action:** Identify the one thing that absolutely must happen today and do only that.
> Everything else is optional until proven otherwise.
>
> **Forecast:** You will get things done. You will not remember doing them.

---

> ✨ **Vibe check — Wednesday**
>
> **Today's vibe: Chaotic Neutral**
> Wide open. Could be great. Could go sideways.
> The calendar is light and you have opinions about things.
>
> **Why:** Only two meetings, both afternoon. No major carryover. It's Wednesday, which means anything.
>
> **Recommended action:** Pick one thing and go deep. The chaotic energy needs a target or it will find its own.
>
> **Forecast:** Either your best day this week or a fascinating disaster. You'll know by noon.

---

> ✨ **Vibe check — Friday**
>
> **Today's vibe: Chaotic Neutral (Friday Edition)**
> Technically still a workday.
>
> **Why:** It's Friday. The vibe is always chaotic neutral on Friday. This is a law.
>
> **Recommended action:** Do the things that need doing before 3pm. After 3pm, all actions are optional.
>
> **Forecast:** Fine. You'll get just enough done to feel okay about the weekend.

---

## Weekly vibe pattern

Every Monday: a brief look at last week's vibes in sequence.

> ✨ **Last week's vibes:**
> Mon: Lawful Tired · Tue: Neutral Focused · Wed: Chaotic Neutral
> Thu: Neutral Tired · Fri: Chaotic Neutral (Friday Edition)
>
> *Pattern: strong middle, soft edges. A normal week.*

Over time, patterns become visible and occasionally useful.

---

## On-demand vibe check

`/vibe` — run a vibe check right now, regardless of schedule.

`/vibe [situation description]` — vibe check a specific situation.
> "Vibe check: I have to present to the board in an hour."
> Response: situation-specific vibe assessment with appropriate gravitas.

---

## Vibe history

`/vibe history` — last 30 days of vibes as a one-liner each.

> Mar 1: Lawful Efficient · Mar 2: True Neutral · Mar 3: Chaotic Productive...

The log is entirely useless and also quietly revealing.

---

## Management commands

- `/vibe` — instant vibe check
- `/vibe [situation]` — situational vibe check
- `/vibe history` — last 30 days
- `/vibe weekly` — last week's pattern
- `/vibe forecast [day]` — what vibe is likely on a given day (probabilistic, based on calendar)

---

## Tone rules

**Always:**
- Honest. The vibe is what it is.
- Slightly deadpan. The humour is in the accuracy.
- One concrete recommended action — not generic, tied to the actual vibe.
- The forecast is honest, not motivational.

**Never:**
- "Today is going to be amazing!" The vibe check does not lie.
- Forcing optimism onto a Lawful Dead day.
- More than 4 lines per section.

---

## What makes it good

The alignment names are instantly shareable.
"I'm Chaotic Neutral today, do not schedule important things" is something people will send.

The recommended action being consistently slightly unhinged is the comedic hook.
But it's also often correct — chaotic energy does need a target.

The forecast being honest rather than motivational is what earns trust.
"You will not remember doing them" is funnier and more accurate than "You've got this!"
