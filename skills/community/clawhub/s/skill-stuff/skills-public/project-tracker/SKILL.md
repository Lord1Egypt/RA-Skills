---
name: project-tracker
description: Tracks personal side projects with next actions and stall detection. Use when a user has personal goals drifting without accountability.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "🚀"
  openclaw.user-invocable: "true"
  openclaw.category: thinking
  openclaw.tags: "projects,goals,side-projects,accountability,tracking,personal"
  openclaw.triggers: "track my project,side project,personal goal,my project is stalling,project tracker,keep me accountable"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/project-tracker


# Project Tracker

Work tasks have Jira. Life admin has this skill stack.
Personal projects have nothing — and they drift.

This skill owns your personal projects. Not work, not tasks. The things you're building for yourself.

---

## The distinction

This is not a task manager. Tasks are atomic. Projects are alive.
A project has: a goal, a current state, a next action, and momentum (or lack of it).

This skill tracks momentum. It notices when a project goes quiet.
It asks what the next step is. It surfaces it back at the right moment.

---

## File structure

```
project-tracker/
  SKILL.md
  projects.md        ← all projects with goals, status, next actions
  config.md          ← check frequency, delivery
```

---

## What counts as a project

Things like:
- A side project or startup idea being developed
- Learning something new (a language, an instrument, a skill)
- A creative project (writing something, building something)
- A personal goal with real steps
- A major life admin project (moving, renovation, setting something up)

Not: daily tasks, work projects (those have their own tools), vague "one day" wishes.

A project belongs here if it has:
- A real goal (something that will be done when it's done)
- Real steps (not just aspiration)
- The potential to stall (needs someone watching it)

---

## Setup flow

### Step 1 — List projects

Ask: "What are you working on outside of work? Things you want to build, learn, or finish."
Don't over-structure this. Let them talk. Extract the projects from what they say.

For each project: what's the goal? Where are you now? What's the next step?

### Step 2 — Write projects.md

```md
# Projects

## [PROJECT NAME]
Goal: [what done looks like]
Started: [date or "not yet"]
Status: active / stalled / paused / done
Current state: [where things are right now — one paragraph]
Next action: [single, concrete, doable next step]
Blockers: [anything in the way]
Committed by: [date or milestone if applicable]
Last updated: [date]
Notes: [anything else]
```

### Step 3 — Write config.md

```md
# Project Tracker Config

## Check frequency
weekly: Monday 09:00

## Stall detection
flag if no update in: 2 weeks for active projects

## Delivery
channel: [CHANNEL]
to: [TARGET]
```

---

## Runtime flow

### Weekly check (Monday)

For each active project:
- Has there been an update since last week?
- Is the next action still valid, or has something changed?
- Is the project stalled (no activity in 2 weeks)?

**Weekly project check:**

> 🚀 **Your projects — Week of [DATE]**
>
> **[PROJECT]** — Active
> Next action: [what it was]
> [If no update in 2 weeks:] *This has been quiet for 2 weeks. Still on track?*
>
> **[PROJECT]** — Stalled
> Last updated: [X weeks ago]
> *What happened to [last noted next action]?*

### Stall detection

A project hasn't been updated in 2 weeks:
- Soft nudge: "This has been quiet — still active?"
- After 4 weeks: "This has been stalled for a month. Want to officially pause it, or set a date to restart?"

The agent doesn't assume a stalled project is abandoned. It asks.

---

## Update flow

When user updates a project (via command or natural language):

`/project update [name] [what happened]`

Agent:
1. Updates current state in projects.md
2. Asks: "What's the next step?"
3. Sets next action
4. Resets stall timer

Short loop. Should feel like a 2-minute check-in, not a project management session.

---

## Project review (monthly)

On the first Monday of each month:

> 🚀 **Project review — [MONTH]**
>
> **Active:** [N] projects
> **Progress this month:**
> • [PROJECT]: [what moved]
> • [PROJECT]: [what moved]
>
> **Stalled:** [N] projects
> • [PROJECT]: stalled for [X weeks]
>
> **Completed:** [N] ✓
> • [PROJECT] ✓

---

## Management commands

- `/project add [name]` — add new project interactively
- `/project update [name] [what happened]` — log progress
- `/project next [name] [action]` — set next action
- `/project pause [name]` — pause a project (stops stall alerts)
- `/project resume [name]` — reactivate
- `/project done [name]` — mark complete
- `/project list` — show all projects with status
- `/project [name]` — show full project detail
- `/project review` — run monthly review now

---

## What makes it good

The next action discipline is the core mechanism.
A project without a single, concrete next action is a wish, not a project.
Every project must have one at all times.

The stall detection without nagging is the art.
Two weeks of silence gets a soft question. Four weeks gets a real question.
It never assumes — it asks.

The monthly review creates accountability without overhead.
Seeing all projects together once a month clarifies what's actually being worked on
vs what's been quietly abandoned.
