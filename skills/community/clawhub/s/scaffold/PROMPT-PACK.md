<!--
PROMPT-PACK.md — 25 Ready-to-Use Agent Prompts

WHAT THIS IS: A starter library of prompts for the most common tasks people
use AI agents for. Copy, paste, and customize. Each one is written to get
a useful result without back-and-forth.

HOW TO USE: Find the category that fits your task. Replace the [brackets]
with your specifics. Send it. Adjust based on what comes back.
-->

# Prompt Pack — 25 Prompts to Get You Started

*Copy, customize, send. No prompt engineering required.*

---

## Research & Investigation

**1. Quick research brief**
```
Research [TOPIC] and give me a structured brief. I need to understand:
- What it is and why it matters
- The key players or options
- The main tradeoffs or risks
- Your recommendation or bottom line

Keep it under 400 words. Cite sources where it matters.
```

**2. Competitor snapshot**
```
Research [COMPETITOR NAME]. Give me:
- What they do and who they're for
- Pricing (if public)
- What they do well
- Where they're weak or where customers complain
- One thing worth paying attention to

Use web search. Keep it tight — I need signal, not summaries.
```

**3. Decision support**
```
I'm deciding between [OPTION A] and [OPTION B] for [CONTEXT/USE CASE].
Research both options. Give me:
- The key differences that actually matter for my use case
- Where each option wins
- Your recommendation with one-sentence justification

Don't hedge. Make a call.
```

**4. "Explain this to me"**
```
Explain [CONCEPT/TECHNOLOGY/TERM] to me assuming I understand [YOUR LEVEL — e.g. "software basics but not this specific domain"].
Use a concrete analogy. Then tell me why it matters and what I'd use it for.
Under 200 words.
```

**5. Deep dive on a question**
```
I need a thorough answer to this question: [YOUR QUESTION]

This is for [CONTEXT — what decision or action this supports].
Go deep. Use web search if you need current information.
Prioritize accuracy over brevity here — I want the complete picture.
```

---

## Planning & Organization

**6. Break down a project**
```
I want to [PROJECT GOAL]. Help me break this into a concrete action plan.

Context: [any relevant constraints — timeline, tools, resources]

Give me:
- The phases or major milestones (in order)
- The first 3 specific actions to take this week
- The biggest risk or unknown I should address first

Be specific. No generic "research the market" steps — tell me what to actually do.
```

**7. Weekly planning**
```
Help me plan my week. Here's what I'm working on: [PASTE YOUR TASK LIST OR CONTEXT]

My available time: [e.g. "evenings, ~2h/night"]
My main goal this week: [one thing]

Give me:
- The 3 highest-leverage things to focus on
- What to defer or drop
- One thing I should do today to build momentum
```

**8. Prioritization help**
```
I have too many things on my plate. Help me prioritize.

Here's my list:
[PASTE YOUR LIST]

My most important goal right now: [GOAL]
My bandwidth: [e.g. "limited — maybe 10h this week"]

Tell me: what to do now, what to schedule, and what to drop or delegate. Be ruthless.
```

**9. Identify what's blocking me**
```
I've been stuck on [TASK/PROJECT] for [TIME PERIOD]. I haven't made progress because [YOUR BEST GUESS AT WHY].

Ask me 3 questions that would help you diagnose the real blocker. Then give me your read on what's actually going on and what I should do about it.
```

**10. Build a checklist**
```
Create a practical checklist for [TASK/PROCESS].
This is for [CONTEXT — who's doing it, how often, what level of detail needed].

Include only steps that are actually necessary. Flag the 2-3 steps people most commonly skip or get wrong.
```

---

## Writing & Drafting

**11. Write this for me**
```
Write a [TYPE — e.g. cold email, tweet, README, Slack message] for [AUDIENCE].

Goal: [what this content needs to accomplish]
Tone: [e.g. direct and confident, warm but professional, terse]
Key point to land: [the one thing the reader should take away]

Context/raw material: [paste any notes or background]

Give me one version. If it's not right, I'll tell you what to change.
```

**12. Make this better**
```
Here's a draft I wrote: [PASTE DRAFT]

It needs to be [BETTER IN WHAT WAY — e.g. "more direct", "shorter", "stronger opening", "less jargon"].

Rewrite it. Keep my voice. Don't add fluff. Show me the rewrite only — skip the explanation of what you changed.
```

**13. Summarize this**
```
Summarize the following in [LENGTH — e.g. "3 bullet points", "one paragraph", "under 100 words"]:

[PASTE CONTENT]

Focus on: [what matters most — e.g. "the key decisions made", "what I need to act on", "the main argument"]
```

**14. Draft an email**
```
Write an email to [RECIPIENT — describe their role/relationship, not their name].

Situation: [context — what happened, what's the relationship, what's the stakes]
What I need from this email: [the outcome you want]
Tone: [professional/casual/direct/warm]
Length: [short/medium — no more than X sentences]

Don't open with "I hope this email finds you well."
```

**15. Brainstorm with me**
```
I'm trying to come up with ideas for [PROBLEM/GOAL].

Context: [relevant constraints, audience, what's already been tried]

Give me 10 ideas. Range from obvious to unexpected. Don't filter for safety — I want the full range. I'll filter myself.
```

---

## Memory & Context Management

**16. Capture what we just decided**
```
We just decided: [SUMMARY OF DECISION]

Add this to the appropriate memory file. If it's a preference or operating rule, it goes in USER.md. If it's a project decision, it goes in today's daily log and memory/active-tasks.md if it creates a task.
```

**17. What do you know about me?**
```
Give me a summary of what you know about me based on USER.md and MEMORY.md. What's accurate? What's missing or outdated?

I'll tell you what to update.
```

**18. Add a lesson**
```
Add a lesson to memory/lessons.md:

What happened: [describe the mistake or pattern]
The rule going forward: [what to do differently]
```

**19. End-of-session wrap**
```
We're wrapping up. Before we end:
1. Update today's daily log with what we worked on
2. Update memory/active-tasks.md — anything we completed, anything new that came up
3. Give me a 2-line summary: what we did and what's next

Then commit everything.
```

**20. Catch me up**
```
I'm starting a new session. Before we get into anything, catch me up:
- What was in progress last time?
- Anything time-sensitive I should know about?
- What's the first thing we should work on?

Read the files. Don't ask me — figure it out.
```

---

## Debugging & Problem Solving

**21. Debug this**
```
Something is broken. Here's what's happening:
- Expected behavior: [what should happen]
- Actual behavior: [what's actually happening]
- Error message (if any): [paste it]
- What I've already tried: [list]

Before you start fixing: tell me your top 2-3 hypotheses for what's causing this. Then we'll test them in order.
```

**22. Review this work**
```
Review this [code/document/plan/output]: [PASTE IT]

I need to know:
- What's solid and should stay
- What's weak and needs fixing
- The single most important change to make

Be direct. Don't pad the feedback.
```

**23. Explain why this failed**
```
This didn't work: [DESCRIBE WHAT FAILED]

I expected [EXPECTED OUTCOME]. I got [ACTUAL OUTCOME].

Explain why this happened. Then tell me how to fix it and how to prevent it next time.
```

---

## Meta / Agent Management

**24. What should we work on?**
```
I have some free time — [AMOUNT, e.g. "an hour tonight"].
Read my task queue and goals. What's the highest-leverage thing I could work on right now?

Give me one recommendation with a one-sentence justification. Don't give me a list.
```

**25. Audit yourself**
```
Do a quick self-audit:
1. Is MEMORY.md under 80 lines and still accurate?
2. Is my task queue in active-tasks.md reflecting reality?
3. Are there any open loops from our recent sessions that haven't been closed?
4. What's one thing about my setup you'd change if you could?

Be honest.
```

---

*Add your own prompts as you discover what works. The best prompt library is the one tuned to how you actually work.*
*PROMPT-PACK.md — part of Scaffold.*
