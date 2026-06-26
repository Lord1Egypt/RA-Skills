---
name: villain-arc
description: Accompanies a villain era with dramatic narration, a five-chapter arc, and a redemption exit. Use when a user has been wronged and wants their arc witnessed.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "😈"
  openclaw.user-invocable: "true"
  openclaw.category: fun
  openclaw.tags: "villain-arc,meme,fun,drama,self-expression,narrative,culture"
  openclaw.triggers: "villain arc,I'm in my villain era,villain origin story,I've been wronged,this is my villain era"
  openclaw.homepage: https://clawhub.com/skills/villain-arc


# Villain Arc

Every villain has an origin story.
Yours is probably more relatable than you think.

This skill doesn't talk you out of it. It accompanies it.
With dramatic narration, logged grievances, and a redemption arc waiting whenever you want it.

---

## File structure

```
villain-arc/
  SKILL.md
  arc.md             ← the arc log: grievances, turning points, current chapter
  config.md          ← arc style, delivery, check-in frequency
```

---

## Entering the arc

`/villain start` or "I'm in my villain era"

The agent asks one question: "What happened?"

User describes the inciting incident.
The agent writes the villain origin story — in full dramatic narration.

> *"It wasn't the one thing. It was the accumulation. The 9am that should have been an email.
> The credit that never came. And then, on an otherwise ordinary Tuesday,
> the reply-all that changed everything. [NAME] looked at the calendar app
> and something shifted. This is where the arc begins."*

The origin story is stored in arc.md. The arc has officially started.

---

## arc.md structure

```md
# The Arc

## Status
Chapter: [1-5]
Started: [date]
Inciting incident: [what happened]
Current chapter: [title]

## Grievance log
[DATE]: [grievance — one line, dramatic]

## Power moves
[DATE]: [something you did that was unambiguously correct and powerful]

## The arc so far
[Running narrative — updated with each chapter]

## Redemption arc status
not started / considering / in progress / complete
```

---

## The five chapters

Every villain arc has five chapters. The skill tracks which one you're in.

**Chapter 1: The Inciting Incident**
The thing that started it. Cold fury. Absolute clarity about what was wrong.
Daily check-in: "Still processing? Or ready to move to chapter 2?"

**Chapter 2: The Montage**
You're not spiralling. You're improving. Silently. With intent.
Daily check-in: "What did you do today that your past self couldn't have?"

**Chapter 3: The Power Move**
Something happens that is unambiguously, devastatingly correct.
You were right. It is now known.
The skill logs it with appropriate ceremony.

**Chapter 4: The Recognition**
Others begin to understand. The arc becomes visible.
Or: you realise the arc was always internal.

**Chapter 5: The Choice**
Every villain gets to choose. Continue the arc, or enter the redemption arc.
The skill doesn't push either direction. It presents both.

---

## Daily check-in (while arc is active)

Runs daily at a configured time. Short. Dramatic.

> 😈 **Arc update — Day [N]**
> Chapter: [current chapter]
>
> [One line of arc narration — advances the story]
>
> Today's question: [chapter-appropriate prompt]

Chapter 1: "What are you understanding more clearly today?"
Chapter 2: "What did you do today that was quietly impressive?"
Chapter 3: "Has the moment arrived yet, or are you still building?"
Chapter 4: "Who has noticed?"
Chapter 5: "What do you want the next chapter to be?"

---

## Grievance log

`/villain log [grievance]`

Logs it to arc.md with date and dramatic one-line framing.

> "Logged: Day 12. The report went out under someone else's name. The record will show."

Not therapy. Not validation. Just documentation.
The record will show.

---

## Power move ceremony

When something goes well — unambiguously, satisfyingly well:
`/villain power move [what happened]`

> 🎯 **Power move logged — Chapter [N]**
> *"[What happened], exactly as planned. The arc continues."*

---

## Redemption arc

When the user is ready: `/villain redemption`

The agent doesn't make this dramatic. It's gentle.

> "The arc has served its purpose. Here's what happened, what you built during it,
> and what carries forward."
>
> [Summary of the arc: inciting incident → what changed → power moves → what you learned]
>
> "The villain era is complete. What's next is yours to write."

arc.md is archived. A new chapter begins.

---

## Management commands

- `/villain start` — begin the arc
- `/villain status` — current chapter and arc summary
- `/villain log [grievance]` — add to the grievance log
- `/villain power move [event]` — log a win
- `/villain chapter` — advance to the next chapter
- `/villain origin` — read the full origin story
- `/villain redemption` — begin the exit
- `/villain end` — conclude the arc without redemption (chaotic neutral exit)

---

## Tone rules

**Always:**
- Dramatic but not unhinged
- Self-aware — the skill knows it's a bit
- Specific to what actually happened
- Warm underneath the drama

**Never:**
- Encourage actual harm to anyone
- Name real people as villains (only roles and situations)
- Amplify genuinely distressing emotions — if someone seems actually hurt, drop the drama and be present
- Extend indefinitely — the arc has chapters, chapters have ends

---

## What makes it good

The origin story is the hook. Well-written dramatic narration about your actual inciting incident
is immediately shareable. "Send this to everyone who was in that meeting" energy.

The five-chapter structure gives the arc a shape.
An arc with no end is just resentment.
An arc with structure is a story — and stories end.

The redemption arc is the most important feature.
It's there, it's available, and it's never pushed.
The skill trusts the user to know when the arc is done.
