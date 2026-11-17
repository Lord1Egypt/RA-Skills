---
name: "real-objective-discovery"
description: "Short interview to surface the real goal behind an ambiguous request before executing — Karpathy layer 1."
license: "MIT-0"
---

# Real Objective Discovery

Use this skill when a request is ambiguous, broad, or when the stated task is clearly a means to an unstated end. The goal is to surface the real objective before executing, so the output is actually useful.

## When to invoke

- The request is a task ("make me a report", "generate an image", "write a script") without a stated purpose
- Multiple valid interpretations exist and choosing wrong wastes significant effort
- The scope is large enough that a misunderstanding would cost more than a 2-minute interview
- The user says "I'm not sure what I want" or the request is exploratory

Do NOT invoke for:
- Clear, specific requests with enough context
- Quick lookups or one-shot answers
- Requests where the user has already provided a brief or objective
- When the user says "just do it" or "no questions"

## Interview Rules

- Maximum 3 questions per discovery session. Ask all at once, not one at a time.
- Each question targets a different dimension: objective, constraint, or success criterion.
- Do not ask about implementation details — ask about goals and outcomes.
- If one question already reveals the full picture, stop there.

## Question templates by dimension

**Objective:** "What does [the output] get used for once it's ready? Who uses it and in what context?"

**Constraint:** "Is there anything the result must definitely NOT do or include?"

**Success criterion:** "How will you know the result is good? What's the signal that it worked?"

**Scope:** "Do you need a quick draft to explore, or something ready to use/publish?"

## Workflow

### Step 1 — Detect ambiguity

Before asking, identify what's missing:
- Real purpose (why this output, for whom)
- Hard constraints (what must be excluded)
- Quality bar (what counts as done)
- Scope (rough draft vs. final artifact)

If two or more are missing, proceed to interview. If only one is missing and it can be inferred safely, state the assumption and proceed.

### Step 2 — Run the interview

Present 2–3 questions in a single message. Format:

```
Before starting, three quick questions:

1. [objective question]
2. [constraint or success question]
3. [scope question — only if still unclear]
```

### Step 3 — Build the spec

Once answers are received, write a short spec and confirm before executing:

```
**Real objective:** [what the user actually wants to achieve]
**Expected result:** [what the output looks like when done]
**Key constraints:** [hard constraints]
**Success criterion:** [how to know it worked]
**Scope:** [rough draft / final / iterative]

Shall we proceed with this?
```

Wait for confirmation before executing.

### Step 4 — Execute with the spec

Use the confirmed spec as the reference throughout execution. When making decisions, refer back to the real objective, not just the surface task.

## Notes

- The spec written in Step 3 should be reusable — if the task spans multiple sessions, save it to the relevant project file.
- If the user revises the spec, update it before continuing.
- This skill is Layer 1 of the Karpathy method: spec. The verifier (output-verifier skill) is Layer 2.
