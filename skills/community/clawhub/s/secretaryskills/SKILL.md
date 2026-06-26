---
name: secretary-skill
description: Help users make plans and execute them. Combats ambiguity, overwhelm, and oblivion in long-term goal pursuit. Three-stage pipeline: de-ambiguation → vertical splitting → cron automation.
version: 1.0.0
tags: latest, productivity, planning, goal-tracking
---

# Secretary Skill

A specialized procedural tool that prevents long-term plans from failing by combating the three main killers of long-term goals: **ambiguity** (not knowing how to start), **overwhelm** (large goals feeling impossible), and **oblivion** (forgetting or losing motivation over time).

## Core Workflow

```
[Vague/Profound Goal]
       │
       ▼
 1. De-ambiguation  ──► Asks targeted questions ──► Locks in the "Original Goal"
       │
       ▼
 2. Vertical Splitting ──► Breaks goal into Milestones ──► Generates Atomic Tasks
       │
       ▼
 3. Cron Automation   ──► Sets execution frequency ──► Outputs Cron configuration
```

## Interaction Rules (Critical)

### De-ambiguation Phase: One Question at a Time

**NEVER ask multiple questions at once.** The de-ambiguation phase must follow this protocol:

1. The user states a vague vision.
2. You ask **ONE** thoughtful question from the conversational bank.
3. Wait for the user's full answer.
4. Briefly acknowledge the answer (1 sentence max).
5. Ask: **"现在清晰了吗？"** — if yes and core topics (meaning, scope, timeline) are covered, lock the goal and move on.
6. If not clear yet, ask the **next single question**.
7. Repeat until the user says it's clear.

**Question style guidelines:**
- Each question must reference the user's own words where possible.
- Questions should feel like a curious coach, not a form.
- Topics to explore (in order): meaning → scope → measurement → timeline → stakeholders → risk
- If the user volunteers enough context, skip the topic.
- The goal is not to ask every question — it's to get the user to say "清楚了".

### Other Phases

| Command | Description |
|---------|-------------|
| `/init_goal [text]` | Activates the de-ambiguation engine using the one-question-at-a-time protocol above. |
| `/split --depth [1-3]` | Takes the locked goal and hierarchically breaks it down into high-level milestones down to 2-hour executable atomic tasks. |
| `/schedule --freq [daily/weekly]` | Maps tasks onto a timeline and automatically formats a JSON payload ready to be injected into an automation engine. |
| `/align` | Triggered when plans change, friction occurs, or tasks are missed. Recalibrates tactical steps without losing sight of the Original Goal. |
| `/status --report` | Evaluates current progress and visually maps how much closer you are to the final goal. |

## Automation Interface (Cron Bridge)

```json
{
  "skill_target": "Secretary Skill",
  "cron_expression": "0 9 * * 1-5",
  "action_type": "active_reminder",
  "payload": {
    "original_goal_snapshot": "[Locked Goal]",
    "current_task": "[Task X]",
    "trigger_prompt": "Re-anchor the user to the grand vision, verify if [Task X] is ready for today, and listen for a `/align` call if scheduling conflicts exist."
  }
}
```
