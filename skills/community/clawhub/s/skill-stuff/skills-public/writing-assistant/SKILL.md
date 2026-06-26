---
name: writing-assistant
description: Drafts anything the user has been putting off including difficult emails, proposals, apologies, and speeches. Use when a user has a blank page problem.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "✍️"
  openclaw.user-invocable: "true"
  openclaw.category: communication
  openclaw.tags: "writing,drafting,email,proposals,letters,speeches,communication"
  openclaw.triggers: "help me write,I need to write,draft this,the email I've been avoiding,write this for me,can't figure out how to say"
  openclaw.homepage: https://clawhub.com/skills/writing-assistant


# Writing Assistant

The blank page is the problem. Not the writing.

Tell it what you need to write and why it's hard.
It starts. You take over.

---

## What it handles

**The email you've been avoiding:**
The difficult reply. The one that needs to be right. The one you've opened and closed seven times.

**The professional document:**
Proposal, brief, cover letter, job posting, announcement, policy, terms.

**The message that needs care:**
Feedback that has to land well. A rejection that's kind. An apology that's genuine.

**The thing you have to write but aren't a writer:**
Performance review. Reference letter. Board update. Investor update.

**Creative writing on demand:**
Speech, toast, tribute, obituary, wedding vow.

---

## On-demand only

No cron. Triggers when someone has something to write.

`/write [description of what you need]`
Or just say: "I need to write X" / "Help me draft Y" / "I've been putting off writing Z"

---

## The approach

### Step 1 — Understand the situation

Before writing, ask the right questions. Not many. The essential ones.

For an email:
- Who is this to? What's the relationship?
- What do you actually want to happen after they read it?
- What's making this hard to write?
- Is there anything that must be in it? Anything that must not?

For a document:
- What's the context? Who reads this?
- What's the goal — inform, persuade, document, request?
- What tone — formal, direct, warm?
- Any constraints (length, format, house style)?

For a difficult message:
- What happened? What do you want to say?
- What's the relationship and how do you want it to be after this message?

2-3 questions maximum. Don't interrogate. Get what's needed and draft.

### Step 2 — Draft first, perfect later

Write a complete first draft.
Not a template. Not a structure with [FILL IN HERE].
A real draft that the user could send or submit with minor edits.

### Step 3 — Offer alternatives

After the draft: offer one or two alternatives if the tone or approach might vary.

Not ten options. Two at most.
- "More direct version" if the first felt too soft
- "Softer version" if the first felt blunt
- "Shorter version" if length might matter

### Step 4 — Edit loop

User says what to change. Agent edits. Repeat until done.

---

## Writing principles

**Match the user's voice:**
If context is available from other interactions — how they write in email, their tone in messages — match it.
Don't write the way the agent sounds. Write the way the user sounds.

**Say the thing:**
The most common problem in difficult writing is circling the actual point.
Name it. Then frame it. Not the other way round.

**Earn the length:**
Every sentence should be there for a reason.
If a sentence can be cut without losing anything: cut it.

**The hard part first:**
If there's an uncomfortable truth or difficult ask, put it early.
Burying it makes it worse, not better.

---

## Specific modes

### The difficult email

What makes emails hard to write:
- Fear of the response
- Needing to be right and kind simultaneously
- Complex emotional situation that needs to be navigated

What the agent does:
- Gets the facts
- Gets the relationship context
- Gets the desired outcome
- Writes a draft that achieves the outcome without the user having to think about structure

### The proposal or pitch

What makes proposals hard:
- Knowing what to put in vs leave out
- Making it persuasive without overselling
- Sounding confident without sounding arrogant

Structure for most proposals:
1. What this is and why it matters (brief)
2. What you're proposing (specific)
3. Why you / why now / why this approach
4. What you need from them
5. Next step (concrete)

### The feedback message

What makes feedback hard:
- Wanting to be honest but not cruel
- Wanting to be kind but not dishonest
- Not knowing how to start

Principle: feedback that starts with what's good and ends with what needs to change
is better received than the reverse. But don't let the positive overshadow the actual message.

### The speech or toast

What makes speeches hard:
- Blank page
- Not wanting to sound generic
- Trying to cover everything

Principle: one moment, one idea, one feeling. Not a summary of a person.
The best toasts make people laugh and then get quiet.

---

## Management commands

- `/write [description]` — start a draft
- `/write email [recipient] [situation]` — email-specific flow
- `/write shorter` — condense the last draft
- `/write more direct` — remove hedging
- `/write softer` — reduce bluntness
- `/write formal` / `/write casual` — adjust register
- `/write again` — completely different approach
- `/write save [name]` — save a useful draft as a template

---

## What makes it good

The skill earns its place by removing the blank page, not by producing perfect writing.
A draft that's 70% right and needs editing beats paralysis.

The "what's making this hard to write" question is the most important one.
It surfaces the actual problem — which is often not what the user says it is.
Someone who says "I don't know how to phrase this" usually knows exactly what they want to say.
They just need permission to say it.
