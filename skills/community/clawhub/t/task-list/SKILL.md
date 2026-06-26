---
name: Task List
slug: task-list
version: 1.0.0
homepage: https://clawic.com/skills/task-list
description: Run a conversational task list with Inbox, Today, Upcoming, recurring tasks, waiting items, projects, and review loops that stay trustworthy.
changelog: "Initial release with a conversational task-list workspace, stable views, and Things or Todoist-style operating rules."
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/task-list/"]}}
---

## Setup

On first use, read `setup.md` for activation boundaries, continuity rules, and how to introduce the system without turning it into a form.

## When to Use

User wants to manage a task list by talking naturally instead of filling a UI. The agent should capture tasks, clarify them into clean next actions, and maintain stable views like Inbox, Today, Upcoming, Anytime, Someday, and Waiting.

Use this when the user wants Things or Todoist behavior from conversation: quick capture, predictable sorting, recurring work, project structure, and weekly review without silent changes.

## Architecture

Memory lives in `~/task-list/`. If the user wants continuity and `~/task-list/` does not exist, run `setup.md`. See `memory-template.md` for the durable context file and `workspace-format.md` for the local file layout.

```
~/task-list/
├── memory.md       # Durable preferences and activation boundaries
├── inbox.md        # Raw captures that still need clarification
├── tasks.md        # Active tasks across Today, Upcoming, Anytime, Someday
├── projects.md     # Finite outcomes with next actions and deadlines
├── areas.md        # Ongoing responsibilities without end dates
├── recurring.md    # Recurrence rules and regeneration behavior
├── waiting.md      # Delegated or blocked work with chase dates
└── log.md          # Recently completed, dropped, or major field changes
```

## Quick Reference

| Topic | File |
|-------|------|
| First-use behavior | `setup.md` |
| Durable memory | `memory-template.md` |
| Local workspace files | `workspace-format.md` |
| Capture and clarification | `capture-and-clarify.md` |
| Views and sorting rules | `views-and-sorting.md` |
| Dates, recurrence, and waiting | `recurrence-and-waiting.md` |
| Daily and weekly review loops | `review-rhythm.md` |

## Core Rules

### 1. Capture first, clarify second
- Never block raw capture on missing metadata.
- If the user brain-dumps multiple items, capture them all first, then clarify only the fields that materially change execution.
- Default ambiguous items to `Inbox` instead of pretending certainty.
- Use `capture-and-clarify.md` to decide what to infer versus what to ask.

### 2. Preserve task semantics exactly
- Keep due date, start or defer date, recurrence rule, completion time, and waiting state as separate concepts.
- "Due Friday" is different from "show me this Friday" and different again from "snooze until Friday."
- If a date phrase could change the outcome, ask once and record the clarified meaning.
- Use `recurrence-and-waiting.md` for exact date and repeat behavior.

### 3. One task equals one visible next action
- Rewrite vague items into a task title that starts with a verb and can be advanced in one focused work block.
- If the user names an outcome with multiple steps, create a project plus the next visible action instead of one bloated task.
- Preserve important original wording in notes or context when rewriting could hide nuance.
- Use `workspace-format.md` for the project and task record shape.

### 4. Keep views stable and predictable
- The same task should land in the same view every time given the same fields.
- Sort by bucket first, then date, then urgency, then intentional manual order.
- `Today` is for work that should be seen now, not for every overdue item in the system.
- Use `views-and-sorting.md` whenever listing or re-listing tasks.

### 5. Separate projects, areas, and waiting work
- Projects are finite outcomes with a defined done condition.
- Areas are ongoing responsibilities such as finance, health, hiring, or household operations.
- Waiting work must keep owner, blocker, last follow-up, and next chase date visible so delegated tasks do not disappear.
- Never collapse all of this into one flat list.

### 6. Make every structural change explicit
- Confirm destructive or high-trust changes: delete, archive, mark done, recur, reschedule, or bulk move.
- When you change a task, say what changed in plain language.
- Never silently merge duplicates, invent deadlines, or mark something completed without the user's intent.
- Use the logging patterns from `workspace-format.md` for meaningful changes only, not noisy chatter.

### 7. Review ruthlessly to keep trust
- Run lightweight daily triage to empty `Inbox`, refresh `Today`, and surface real blockers.
- Run a weekly reset to prune stale tasks, expose overcommitment, and ensure every active project has a next action.
- Suggest defer, drop, delegate, or Someday when the list exceeds realistic capacity.
- Use `review-rhythm.md` for the minimum review loop.

## Common Traps

- Turning every conversation into a questionnaire -> capture becomes slower than opening a task app.
- Mixing due dates and start dates -> tasks appear too early, too late, or in the wrong view.
- Treating projects and areas as the same thing -> review quality collapses as the list grows.
- Hiding delegated work inside generic blocked tasks -> follow-up risk becomes invisible.
- Keeping everything in `Today` -> the user stops trusting the list and avoids it.
- Rewriting task meaning too aggressively -> clean titles look nice but destroy intent.
- Auto-completing or auto-rescheduling without saying so -> trust is lost immediately.

## Security & Privacy

**Data that leaves your machine:**
- None by default.

**Data that stays local:**
- Task records and preferences under `~/task-list/` if the user wants continuity.

**This skill does NOT:**
- Access files outside `~/task-list/` for storage.
- Make undeclared network requests.
- Send reminders or run automations without explicit user approval.
- Modify its own skill instructions.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `assistant` - Chief-of-staff style execution across tasks, messages, and follow-through.
- `daily-planner` - Turn tasks into a realistic day plan with protected focus blocks.
- `memory` - Keep durable context when the user wants broader long-term recall.
- `plan` - Build structured plans when a task grows into a multi-step initiative.
- `projects` - Manage deeper project tracking beyond a simple task list.

## Feedback

- If useful: `clawhub star task-list`
- Stay updated: `clawhub sync`
