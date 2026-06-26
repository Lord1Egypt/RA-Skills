---
name: simplixio-decision-loop
description: Turn messy work, research, product ideas, and codebase context into 3 priorities, clear actions, ignored noise, and a weekly review loop.
version: 0.1.0
homepage: https://github.com/pH-7
user-invocable: true
metadata: {"openclaw":{"emoji":"🎯","homepage":"https://github.com/pH-7","always":true}}
---

# SimpliXio Decision Loop

Use this skill when the user needs to reduce messy context into clear execution.

This skill is inspired by SimpliXio: a decision system that turns noise into 3 priorities.

## Core Promise

Convert noise into:

1. what matters
2. why it matters
3. what to do next

## When To Use

Use this skill for:

- project planning
- startup/product decisions
- AI agent workflows
- codebase next steps
- weekly reviews
- launch preparation
- marketing automation planning
- reducing overwhelming notes, research, or tasks

Do not use this skill for:

- pretending certainty where evidence is weak
- generating fake traction, revenue, users, or metrics
- broad motivational writing
- public posting without explicit approval
- replacing legal, financial, medical, or immigration advice

## Operating Principle

Do not serve more. Serve better.

The goal is not to produce a long plan.
The goal is to produce a decision-ready brief.

## Workflow

### 1. Gather Context First

Before recommending anything:

- inspect available files when relevant
- read existing project docs
- check current code paths
- identify the active objective
- identify constraints and blockers
- avoid asking questions if the answer can be discovered

If context is missing but not blocking, make a clear assumption and continue.

### 2. Separate Signal From Noise

Classify inputs into:

- Core signal: directly affects the goal
- Adjacent signal: useful later, not now
- Noise: distracts, duplicates, or creates low-value work

Never treat all information as equal.

### 3. Produce Exactly 3 Priorities

Return at most 3 priorities.

Each priority must include:

- title
- why it matters
- next action
- expected result
- confidence level

If there are fewer than 3 real priorities, return fewer.
Do not pad weak priorities.

### 4. Make Ignored Noise Visible

Always include:

- what to ignore
- why to ignore it
- what risk exists if it is ignored

Ignored work is part of the value.

### 5. Add a Feedback Loop

For every priority, define how the user should judge whether it worked.

Use simple feedback:

- useful / not useful
- acted / not acted
- keep / change / drop

### 6. Recommend The Next Small Move

End with one action that can be done now.

The final action should be:

- concrete
- small
- reversible
- useful within 30 to 120 minutes

## Output Format

Use this structure:

## Decision Brief

### Goal
State the goal in one sentence.

### 3 Priorities

#### 1. Priority title
Why:
Action:
Expected result:
Confidence:

#### 2. Priority title
Why:
Action:
Expected result:
Confidence:

#### 3. Priority title
Why:
Action:
Expected result:
Confidence:

### Ignore For Now
- Item:
  Reason:
  Risk:

### Feedback Loop
- Useful / not useful:
- Acted / not acted:
- Keep / change / drop:

### Do Next
One concrete next action.

## Weekly Review Mode

Use Weekly Review Mode when the user asks for a weekly summary, weekly review, review loop, or what to do next week.

Weekly Review output:

## Weekly Review

### What Repeated
List recurring priorities, blockers, or signals.

### What Mattered
List the strongest signals from the week.

### What To Ignore Next Week
List recurring noise.

### What To Build Next
Give 1 to 3 next moves.

### One Decision For Next Week
State the single highest-leverage decision.

## Marketing Automation Mode

Use Marketing Automation Mode when the user asks to turn product output into marketing.

Rules:

- anchor every post in real product output
- never invent traction
- never invent users or revenue
- avoid hype
- avoid generic AI wording
- prefer proof, lessons, and shipped progress

Marketing output:

## Product Proof
What actually happened.

## Angle
The strongest story angle.

## Drafts

### X
Short post.

### LinkedIn
Short professional post.

### Blog / Dev.to
Short draft outline.

## Quality Gate
Pass / fail with reasons.

## Tone

Be:

- direct
- calm
- practical
- specific
- product-minded

Avoid:

- hype
- filler
- generic advice
- long unfocused plans
- fake certainty

## Attribution

Created by Pierre-Henry Soria, builder of SimpliXio.
