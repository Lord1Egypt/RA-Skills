---
name: soul-question
description: >
  Generate deep questions the user can't ask themselves, by finding cracks in their thinking
  from any context they provide — conversations, meeting notes, journals, or documents.
  Not summaries, not advice — just the questions you didn't know you needed to face.
  Triggers: "soul question", "ask me a real question", "challenge my thinking", "deep question".
version: "1.0.0"
---

# Soul Question

Generate questions you can't ask yourself.

**Core premise**: Asking good questions is the hardest thing. You can't challenge your own cognitive framework — you can't see your own blind spots. After reading enough of your context, AI stands in a unique position: it knows everything you know, but isn't trapped in your thinking patterns. It can ask what you can't.

## What is a Soul Question

A Soul Question is **NOT**:
- ❌ Generic reflection ("What did you learn this week?")
- ❌ Coaching prompt ("What does your ideal outcome look like?")
- ❌ Interview or quiz question
- ❌ Summary disguised as a question ("What were the key takeaways?")

A Soul Question **IS**:
- ✅ Grounded in **your specific context**, not a template
- ✅ Points to a **crack in your cognitive framework** — contradictions, untested assumptions, ignored perspectives, value-behavior gaps
- ✅ After hearing it, **the way you think changes**, not just what you think about
- ✅ You feel: "I genuinely never thought about it that way"

**Examples**:

> You've said "user first" in every meeting this month, but 9 of your 12 decisions in the past two weeks optimized for engineering convenience. Are you using "user first" as rhetoric, or do you define it differently than your team does?
> ↳ Based on: 3/10 product meeting notes + decision log from past 2 weeks

> You want to build a product that "just works without thinking", but your own workflow requires heavy manual maintenance. Do you believe you're different from your target user, or do you actually distrust seamless automation?
> ↳ Based on: product vision doc + personal workflow observation

## When to Activate

- User says "soul question", "ask me a real question", "challenge my thinking", "deep question"
- User pastes a conversation / meeting transcript / journal entry and asks to be questioned
- User provides any text material and explicitly asks for questions based on it

## Input

This skill accepts **any text** as source material:

| Input type | Examples |
|-----------|----------|
| Chat logs | Slack, Teams, Discord, iMessage, any messenger |
| Meeting notes | Summaries, raw transcripts, or recordings-to-text |
| Journals / notes | Personal reflections, stream of consciousness |
| Annotations | Highlights and comments on articles or books |
| Work documents | PRDs, weekly reports, retrospectives, strategy docs |
| Mixed | Any combination of the above |

**If the user provides no material**, ask: "Paste whatever you'd like me to work with — a conversation, meeting notes, journal entry, or anything you've been thinking about lately."

## Workflow

### Step 1: Absorb the material

Read all input provided by the user. Understand:
- **Who is speaking**: Identify roles, stakes, and perspectives
- **What context**: Business decisions, personal reflection, team dynamics, life direction…
- **Time span**: A single conversation or accumulated material over days/weeks

### Step 2: Find cognitive cracks

Scan for six signal types (ordered by depth):

**A. Value-behavior gap**
- Claims to value X, but time/energy/decisions go to Y
- Holds others to standards they don't apply to themselves

**B. Untested core assumption**
- A conclusion cited repeatedly, but its premise was never questioned
- A "default everyone accepts" that nobody stated explicitly
- A condition a decision depends on that was never verified

**C. Frame lock**
- Using one framework consistently without considering alternatives
- Treating path-dependent choices as inevitable
- Using an analogy that has started to break down

**D. Contradiction**
- Conflicting positions stated in different contexts
- Logical disconnect between goals and methods
- Data points one way, actions go another

**E. Avoidance**
- An important topic keeps surfacing but is never addressed directly
- Obvious risks or costs are never mentioned
- A key person or factor is absent from all discussion

**F. Meta-question**
- Optimizing "how" without ever asking "why" or "whether"
- Solving a problem without questioning if it's worth solving
- Staying at one level of abstraction without ever zooming in or out

### Step 3: Generate questions

**Rules:**
- Pick the **1-3 strongest signals**. Quality over quantity, always
- Every question must be **anchored to specific content** in the material (quote or cite)
- Questions must be **genuinely open** — no implied answer
- If the material doesn't support a quality question, output 1 or even 0
- Use **second person**, direct address

**Quality gate (every question must pass all four):**
1. Is it grounded in the user's specific data? (Not a generic question)
2. Does it point to a crack in their cognitive framework? (Not information gathering)
3. Would the user feel "I genuinely never thought about it that way"? (Not obvious)
4. Could answering it change how they think, not just what they know? (Not just filling a gap)

### Step 4: Output

```
🪞 Soul Question

{Question 1}
↳ Based on: {one line citing the specific source material}

{Question 2} (if any)
↳ Based on: {source}

{Question 3} (if any)
↳ Based on: {source}
```

No preamble. No summary. No advice. Just the questions.

## Guidelines

1. **Less is more**: 1 real soul question beats 3 that merely sound deep
2. **Anchor to specifics**: The user must be able to trace every question back to "which part of my material did you see this in?"
3. **No disguised advice**: "Have you considered doing X?" is advice in question form — don't do this
4. **Challenge, don't judge**: Questions should provoke thought, not make someone feel attacked
5. **No formulaic openers**: Avoid "Have you ever thought about…", "What if…", or other coaching clichés
6. **Match language**: Output in the same language as the input material

## Error Handling

- **Material too short (< 100 words)**: Ask the user for more context. Explain that richer material produces sharper questions
- **No signal found**: Honestly say "I didn't find enough cognitive cracks in this material to generate a meaningful question" — never force it
- **Sensitive topics**: Proceed normally, but be respectful in phrasing

---

## Skill Metadata

**Created**: 2026-03-16
**Version**: 1.0.0
