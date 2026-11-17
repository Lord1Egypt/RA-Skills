---
name: shuxia-skill-library
description: Use when creating, reviewing, or refining an agent skill and the goal is to make the skill more obedient, better bounded, and harder to misuse. Especially useful when extracting reusable ideas from strong external skills, turning them into boundary rules, constraint patterns, review checklists, and concrete revisions for local skills.
---

# Shuxia Skill Library

## Overview

This skill is a `skill-for-skills`.

Use it to study why a strong skill behaves well, extract its reusable boundary design, and apply those lessons to improve local skills. The focus is not content quality alone, but whether a skill is:

- clearly bounded
- operationally constrained
- hard to hijack
- easy to trigger correctly
- consistent in output

This skill also acts as a normalization reviewer for new or existing skills in the local library.

## When to Use

Use when:

- creating a new skill and you want stricter boundaries
- reviewing an existing skill that feels too loose, too generic, or too easy to misuse
- studying an external skill and wanting to absorb its good ideas
- extracting reusable patterns for `scope`, `fallback`, `output contract`, or `anti-slop` behavior
- building a local skill library that should get stronger over time

Do not use when:

- the task is only to explain what a skill says
- the task is only to copy a skill verbatim
- the problem should be solved by code enforcement or tooling instead of documentation

## Core Principle

A strong skill does not become obedient by sounding strict.

It becomes obedient by turning judgment into structure:

- define what it **is**
- define what it **is not**
- define when it must **stop**, **fallback**, or **ask**
- define what evidence must come **before** generation
- define what output shape is **required**

If a rule is important, it should appear in the workflow, not only in prose.

## Review Lens

Always review a target skill across these dimensions:

1. `Identity Boundary`
   - Does the skill clearly say what role it plays?
   - Example: “HTML-native designer, not production frontend engineer.”

2. `Task Boundary`
   - Does it list valid use cases and invalid use cases?
   - Can a caller tell when to route elsewhere?

3. `Execution Boundary`
   - Are the constraints encoded in order?
   - Example: search first, verify assets second, produce output last.

4. `Fallback Boundary`
   - When context is insufficient, does the skill degrade safely?
   - Example: switch to exploration mode instead of hallucinated hi-fi output.

5. `Output Boundary`
   - Does it force a response shape, artifact shape, or evidence format?

6. `Anti-Slop Boundary`
   - Does it explicitly block common generic behavior?
   - Example: ban default gradients, fake brand assets, or vague summaries.

7. `Transferability`
   - Is the good idea reusable in other skills, or is it too domain-specific?

## Workflow

### Step 1 — Classify the target skill

Identify:

- what the skill claims to do
- what medium it operates in
- what failure mode it is trying to prevent
- whether it is a `technique`, `workflow`, `reviewer`, `orchestrator`, or `domain skill`

### Step 2 — Extract boundary mechanisms, not just nice wording

Look for mechanisms such as:

- explicit “use / do not use” lists
- ordered steps
- required evidence sources
- mandatory checkpoints
- fallback modes
- negative lists
- output contracts
- role framing

If a strength is only stylistic, do not over-credit it.
Prefer mechanism over tone.

### Step 3 — Convert observations into reusable patterns

For every strong idea, rewrite it as:

- `Pattern name`
- `Why it works`
- `Where to reuse`
- `How to encode it in a skill`

Store distilled ideas in [skill-patterns.md](/Users/xiaomao11/.codex/skills/shuxia-skill-library/skill-patterns.md).

### Step 4 — Audit the local target skill

When reviewing a local skill, report:

- boundary gaps
- ambiguity points
- loopholes that invite misuse
- rules that exist only in prose but not in flow
- missing fallback behavior
- missing output contract

### Step 5 — Rewrite toward obedience

Prefer these repairs:

- replace vague authority language with explicit routing rules
- move critical constraints into ordered workflow
- add “do not use when” lists
- add fallback modes for missing context
- add output contract sections
- add anti-pattern or anti-slop sections

## Output Contract

When this skill is used for analysis, produce:

- `Skill Type`
- `Primary Boundary`
- `Boundary Mechanisms`
- `What Makes It Obedient`
- `Reusable Patterns`
- `Local Improvements`

When this skill is used to review a local skill, produce:

- `PASS`, `WARNING`, or `ERROR`
- each finding tied to one of the seven review dimensions
- a concrete rewrite suggestion, not only criticism

When this skill is used to create or revise a skill, the revised skill must include:

- frontmatter with a trigger-focused description
- explicit use / do-not-use scope
- workflow with ordered constraints
- fallback behavior if context is insufficient
- output contract

## Seed Patterns

The following ideas are already accepted into this library and should be reused when applicable:

- `Role Lock`
  - Declare what the skill is and what it is not.

- `Scope Split`
  - Explicitly separate valid scenarios from invalid scenarios.

- `Constraint In Workflow`
  - Important rules must appear in execution order, not only in principles.

- `Fallback Instead Of Hallucination`
  - When context is weak, switch mode rather than fabricate high-confidence output.

- `Negative List`
  - Ban the most common low-quality defaults explicitly.

- `Evidence Before Output`
  - Require retrieval, assets, or source-of-truth before synthesis.

- `Output Contract`
  - Force the structure of the final answer or artifact.

- `Pattern Harvesting`
  - Strong external skills should be mined for reusable mechanisms, not copied blindly.

`huashu-design` is a reference example for:

- strong role lock
- scope split
- brand asset protocol
- fallback via design-direction mode
- anti-slop negative lists

## Common Mistakes

- Confusing strict tone with real constraint
- Praising wording while missing execution loopholes
- Copying domain-specific rules into unrelated skills
- Writing principles without fallback behavior
- Letting descriptions summarize workflow instead of trigger conditions

## Real-World Goal

The local skill library should improve over time.

Each good external skill should leave behind reusable boundary patterns so future local skills become more precise, more obedient, and easier to trust.
