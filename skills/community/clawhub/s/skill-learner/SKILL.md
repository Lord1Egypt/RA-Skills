---
name: skill-learner
description: Identify repeated workflows, recurring user asks, common failures, and reusable procedures that should become new skills or improvements to existing skills. Use when patterns repeat, when the user corrects the same kind of mistake, or when a task keeps requiring the same instructions, docs, or tool flow.
---

# Skill Learner

## Overview

Use this skill to turn repeated work into reusable skill knowledge. Focus on extracting patterns, not doing the underlying task again.

## Learning workflow

### 1. Identify the pattern
Look for repeated signals such as:
- the same type of task happening multiple times
- the same correction from the user more than once
- repeated tool sequences
- repeated failures or omissions
- repeated project workflows that should be standardized

### 2. Decide the right outcome
Choose one:
- create a new skill
- improve an existing skill
- add a reference file or script to an existing skill
- record a smaller local operating rule instead of creating a full skill

### 3. Extract the reusable pieces
Capture only what is worth reusing, such as:
- triggers for when the skill should be used
- the core workflow
- decision rules
- scripts or references that would prevent repetition
- common pitfalls and corrections

### 4. Recommend the smallest useful skill shape
Prefer the lightest structure that solves the repeated problem:
- SKILL.md only
- SKILL.md + references
- SKILL.md + scripts

### 5. Report clearly
Use this structure:

### Pattern observed
- what keeps repeating

### Why it should become skill knowledge
- what waste/error it prevents

### Recommended action
- new skill / improve existing skill / local rule only

### Minimal skill shape
- what files/resources are actually needed

## Rules

- Do not create a skill unless the pattern is real and reusable.
- Prefer improving an existing skill over creating duplicates.
- Keep recommendations lean.
- Avoid auxiliary documentation clutter.
- If a local workspace rule is enough, say so instead of forcing a new skill.
