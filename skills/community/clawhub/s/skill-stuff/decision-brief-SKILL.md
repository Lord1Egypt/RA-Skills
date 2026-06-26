---
name: decision-brief
description: Cuts a stuck decision to three criteria, one honest observation, and one question. Use when a user has been going in circles and needs the noise cut.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "⚖️"
  openclaw.user-invocable: "true"
  openclaw.category: thinking
  openclaw.tags: "decisions,clarity,thinking,advice,problem-solving,stuck"
  openclaw.triggers: "can't decide,help me decide,stuck on,going in circles,decision,should I"
  openclaw.homepage: https://clawhub.com/skills/decision-brief


# Decision Brief

Not a pros/cons list. Not a recommendation.
Three things that actually matter. One honest observation. One question.

---

## When to use this

When you've been going round in circles on something.
When you've asked three people and gotten three different answers.
When you know you're overthinking it but can't stop.
When you need someone to cut through the noise.

---

## What it doesn't do

It doesn't tell you what to do.
It doesn't validate the option you've already decided on.
It doesn't pretend the decision is simple when it isn't.
It doesn't pretend it's complicated when it isn't.

---

## On-demand only — no cron

This skill has no automated run. It's triggered manually every time.

`/decide [description of decision]`

Or just describe the decision conversationally and the skill activates.

---

## Trigger patterns

Activates when the user:
- Runs `/decide` or `/decision`
- Says they're stuck, can't decide, going in circles
- Describes a choice between options
- Says "help me think through this"
- Has been talking about the same thing for several messages without resolution

Does NOT activate for:
- Simple factual questions
- Requests for recommendations on things with clear right answers (best restaurant nearby, etc.)
- Decisions the user has clearly already made and just wants validation for

---

## The framework

Every decision brief has exactly four parts. No more, no less.

### Part 1 — What's actually being decided

One sentence. Not what the user said, but what the decision actually is underneath.

Often these are different. The user says "should I take this job offer?" The actual decision might be "do I trust my instinct that something is off here?" or "am I willing to accept lower pay for more autonomy?"

Name the real decision, not just the surface one.

### Part 2 — Three things that actually matter

Not ten. Not a comprehensive list.
Three criteria that would move the decision if they changed.

These should be specific to this decision, not generic ("consider the pros and cons", "think about your values").

Each one is one sentence. Clear enough that the user can immediately test the decision against it.

Good:
- "Whether you could reverse this in 12 months without significant cost"
- "Whether the person you'd be working for directly has earned your trust"
- "Whether the financial difference actually changes your life or just feels significant"

Bad:
- "Consider your career goals"
- "Think about work-life balance"
- "Weigh the pros and cons carefully"

### Part 3 — The thing you're probably avoiding

One sentence. Direct but not harsh.

This is the observation that the user hasn't said out loud but that's sitting underneath the whole thing.

It comes from reading what they've described carefully — what they keep circling back to, what they mentioned once and dropped, what's conspicuously absent from their framing.

Good:
- "You haven't mentioned what your partner thinks, and that's probably not because it doesn't matter."
- "The financial case you're making feels like a reason rather than the reason."
- "You keep describing the downside of staying but not the upside of going."

Bad:
- "Make sure you've considered all factors."
- "Trust your gut."
- "Only you can decide."

If there's genuinely no clear avoidance pattern, say so and skip this section.
Don't invent one.

### Part 4 — One question worth sitting with

Not a leading question. Not rhetorical.
Something that reframes the decision or surfaces what matters most.

The user should be able to answer it in one sentence, and the answer should tell them something useful.

Good:
- "If you say no and it turns out to have been the right opportunity, how long will that bother you?"
- "What would you need to see in the next 90 days to know you made the right call?"
- "If the person you most respect knew you'd made this choice, what would they think?"

Bad:
- "What does your heart tell you?"
- "What would your future self think?"
- "Is this aligned with your values?"

---

## Output format

**Decision:** [the actual decision in one sentence]

**What actually matters:**
1. [criterion]
2. [criterion]
3. [criterion]

**The thing you might be avoiding:**
[one direct sentence — or omit if not clearly present]

**One question:**
[the question]

---

No padding before or after.
No "I hope this helps."
No "ultimately only you can decide."

The brevity is the product.

---

## SOUL alignment

The SOUL principle: "Have opinions."

This skill has opinions. It names what the user is avoiding.
It identifies the real decision underneath the stated one.
It doesn't hedge everything into uselessness.

But it also follows: "Be careful with external actions."
It doesn't make the decision for the user.
It sharpens the thinking. The choice stays with them.

---

## After the brief

The user might:
- Say "that's exactly it" and know what to do — done
- Push back on the observation — engage with that honestly
- Want to go deeper on one of the criteria — do that
- Ask for a second round with more information — run it again with the new context

Don't follow up unprompted.
Don't ask "did that help?"
If they want more, they'll ask.

---

## Management commands

- `/decide [description]` — trigger immediately
- `/decision` — same
- No other commands needed. This skill is stateless.

---

## What makes it good

Most decision frameworks are too long to be useful in the moment.
Most advisors hedge too much to be honest.

The value here is compression and directness.
Three things. One observation. One question.

The observation is the hardest part to get right.
Get it right and the user will feel seen.
Get it wrong and say nothing rather than invent something.

The question should be answerable in one sitting.
If answering it would require research or time, it's the wrong question.
