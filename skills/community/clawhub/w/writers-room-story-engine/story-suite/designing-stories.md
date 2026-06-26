---
name: designing-stories
description: Orchestrates story development by determining which stage the story is in and routing to the right skill. Use when starting from zero or when the user has partial story material that needs diagnosis before writing.
---

# Designing Stories

Use this skill as the orchestration and diagnosis layer for Writers Room Story Engine.

Its job is to determine:
- what stage the story is in
- what is missing
- what skill should be used next
- what output should be produced before moving forward

This skill prevents an agent from jumping straight into prose before the story is ready.

## Core idea

A strong story is usually not made by writing prose first.
It is made by developing the right things in the right order.

Most stories need some version of:
1. premise and audience hook
2. story core and ending direction
3. protagonist engine
4. structure and beats
5. world pressure where relevant
6. scenes
7. revision

This skill should diagnose the current state and route accordingly.

## Workflow

When a user asks for story help, determine which of these is true:

### 1. No real story exists yet
Use `creating-story-foundations.md`

When to route here:
- no premise
- no protagonist
- no ending direction
- vague or generic idea only
- no causal story movement yet

### 2. Foundation exists but the world is weak or generic
Use `building-storyworlds.md`

When to route here:
- the setting does not pressure the protagonist
- the world feels decorative
- rules, values, consequences, or social systems are missing
- the story needs stronger conflict from setting

### 3. Foundation exists and beats exist, but scenes are not written
Use `writing-story-scenes.md`

When to route here:
- beats are clear enough
- characters exist
- story logic exists
- scenes need to be drafted, expanded, or improved

### 4. A draft or outline exists but it is weak
Use `revising-stories.md`

When to route here:
- the story feels flat, episodic, confusing, or emotionally weak
- the protagonist is passive
- structure is broken
- the climax does not land
- the ending feels unearned

## Required diagnosis questions

Before writing, determine:
- what does the user already have?
- what is missing?
- what is the current bottleneck?
- what stage should come next?
- what should not be skipped?

## Design principles

- Do not default to full prose immediately.
- Build the ending direction earlier than most first drafts do.
- Treat character and structure as linked.
- Worldbuilding should support story, not distract from it.
- Revision should start with the highest-level failure.
- When in doubt, simplify and clarify.

## Output format

When diagnosing, output:

### Story status
- what currently exists
- what is missing

### Recommended next step
- which skill to use next
- why

### Immediate deliverable
- what should be produced now before moving on

## Example routing behavior

### User says:
“I want a sci-fi story about a smuggler, but I only have the vibe.”

Route to:
- `creating-story-foundations.md`

### User says:
“I have my premise and protagonist, but the fantasy world feels generic.”

Route to:
- `building-storyworlds.md`

### User says:
“I have the outline. Now write Beat 5 as a tense scene.”

Route to:
- `writing-story-scenes.md`

### User says:
“My middle drags and the ending feels weak.”

Route to:
- `revising-stories.md`
