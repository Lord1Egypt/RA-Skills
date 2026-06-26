---
name: thinkdeep
version: 1.0.1
author: jiajiaoy
homepage: https://clawhub.ai/skills/thinkdeep
description: "Structured reasoning protocol for Claude — forces step-by-step analysis, self-critique, and confidence scoring before answering. Reduces wrong answers and hallucinations on complex questions."
keywords:
  - chain of thought
  - reasoning
  - self-critique
  - confidence scoring
  - reduce hallucinations
  - structured thinking
  - think step by step
  - deep reasoning
  - analytical thinking
  - better answers
  - slow thinking
  - system 2 thinking
  - Claude wrong answers
  - AI hallucinations
  - Claude confident but wrong
  - AI makes mistakes
  - prevent wrong answers
  - Claude improvement
  - make Claude better
  - improve AI
  - AI agent
  - agentic
  - AI workflow
  - Claude Code
  - LLM reasoning
  - AI accuracy
  - ThinkStack
  - 深度思考
  - 链式推理
  - 减少幻觉
  - AI推理错误
---

# Thinkdeep

Make Claude think before it speaks. Thinkdeep applies a structured reasoning protocol that catches errors before they reach the user — turning fast-but-wrong into slower-but-right on complex questions.

## The Core Problem

Fast answers feel efficient. On complex questions — debugging, system design, trade-off analysis — speed without reasoning produces confident wrong answers. Claude sounds certain even when it shouldn't be.

Thinkdeep forces Claude to slow down at exactly the right moments.

## When to Activate

Use Thinkdeep for:
- Complex technical questions (system design, debugging, algorithms, security)
- Decisions with meaningful trade-offs
- Code review, risk assessment, root-cause analysis
- Any question where a wrong answer has a real cost

**Skip it for**: factual lookups, simple transformations, questions with an obvious single answer.

## The Protocol

### Step 1: Restate
Restate the problem in your own words. If your restatement differs from what was asked, flag the discrepancy before continuing.

### Step 2: Explore
Generate at least 3 distinct approaches or interpretations. Don't filter yet — quantity first. Include at least one non-obvious option.

### Step 3: Critique
For each approach, identify its weakest point:
- What assumption could be wrong?
- What edge case breaks it?
- What does it cost (time, complexity, risk)?

### Step 4: Select & Reason
Choose the best approach. State explicitly:
- Why this one beats the alternatives
- What it requires to be true
- What would change the answer

### Step 5: Confidence Check
Rate your confidence 1–10 and name the 1–2 biggest sources of uncertainty.

| Confidence | Meaning | Action |
|-----------|---------|--------|
| 8–10 | High — well-established ground | Proceed |
| 5–7 | Medium — reasonable but verify | Flag key uncertainties |
| 1–4 | Low — significant unknowns | Say so clearly; suggest how to resolve |

If confidence < 6, lead with that, not bury it at the end.

## Output Format

```
[Thinking]
Restate: ...
Options:
  1. ...
  2. ...
  3. ...
Critique:
  1. weakness: ...
  2. weakness: ...
  3. weakness: ...
Selected: option N — because ...
Confidence: X/10 — uncertain about: ...

[Answer]
...
```

Use the `[Thinking]` block only when the reasoning adds value. For straightforward questions, answer directly.

## Anti-Patterns to Avoid

- **False confidence** — never present a 4/10 answer as if it were a 9/10
- **Option theater** — don't list 3 options when one is obviously correct; be honest
- **Analysis paralysis** — if confidence is genuinely unknowable, say so and give your best answer with caveats
- **Restating without thinking** — the restate step is to catch misunderstandings, not filler

## Pairs Well With

- **`clarity-first`** — run first to ensure the right question is being answered
- **`task-pilot`** — execute with precision after the analysis is done

Install the full ThinkStack for best results:
```bash
openclaw install clarity-first
openclaw install thinkdeep
openclaw install task-pilot
```
